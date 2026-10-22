# Preserving Signals — Cause, Transparency, and the Anti-Patterns That Erase Errors

> Part I · Chapter 2 · Sections 2.12, 2.13, 2.14, 2.15, 2.16, 2.17 · _Estimated reading time: 26 min_

## In one sentence

An error is evidence: **preserve its cause, do not swallow it, never turn failure into success, and
do not bury it under redundant or ceremonial handling** — because every erased signal is a bug you
will diagnose twice.

## Why this matters in production

The most expensive production bugs are not the crashes — those are loud. They are the **silent**
ones: a payment "succeeds" but nothing was charged; a webhook "processes" but the event is lost; a
retry "handles" an error by returning the stale cache forever. These all share one root cause: a
signal was erased somewhere between where the problem occurred and where someone could act on it.

This file is the defensive core of the chapter. The principles here are mostly *don'ts*, because
these mistakes are easy, invisible, and catastrophic.

## Core concept — six principles

### 2.12 Error transparency vs abstraction

You must balance two goods:

- **Transparency** — the error's cause and context are available for debugging.
- **Abstraction** — callers see a stable, meaningful error, not driver internals.

The rule: **abstract the interface, not the evidence.** The public contract can be
`PAYMENT_PROVIDER_UNAVAILABLE`; the preserved cause can still be the raw `ECONNRESET`.

```ts
// ✅ Abstract outward, preserve inward.
throw new PaymentProviderUnavailable({
  cause: rawErr,               // preserved for logs/diagnostics
  provider: "stripe",
});
```

### 2.13 Preserve the original cause

When you wrap or translate, keep the original error attached.

| Language | Mechanism |
| -------- | --------- |
| JS/TS | `new Error(msg, { cause })` (ES2022) |
| Python | `raise AppError(...) from exc` (`__cause__`) |
| Java | `new AppException(msg, cause)` |
| Go | `fmt.Errorf("...: %w", err)` (wrapping) |
| Rust | `thiserror` `#[source]` / `anyhow::Context` |

Losing the cause means the on-call engineer sees `AppError: failed` and nothing else.

### 2.14 Avoid swallowing errors

**Swallowing** = catching and doing nothing meaningful: no rethrow, no record, no recovery.

```ts
// ❌ Swallowed: bugs vanish, data may be lost.
try { await persist(order); } catch { /* ignore */ }
```

A catch block must do at least one of: **handle** (recover), **translate**, **rethrow**, or
**record and terminate**. If it does none, it is a bug.

### 2.15 Avoid silently changing failure into success

The worst pattern. Returning a success-shaped result when the operation failed.

```ts
// ❌ Failure disguised as success.
async function archive(orderId: string): Promise<void> {
  try { await s3.upload(orderId); }
  catch { return; } // caller believes the archive succeeded
}
```

This corrupts downstream state, breaks audits, and hides outages. It is a *correctness* violation,
not just a style issue.

### 2.16 Avoid redundant exception handling

Handling the same condition at multiple layers causes double-logging, double-retry, and conflicting
decisions.

```text
  DB error → repo logs & retries → service logs & retries → controller logs & retries
  = 3 logs, 3 retries, 1 incident report you cannot read
```

**Handle once, at the layer that owns the decision.** Other layers propagate.

### 2.17 Avoid excessive catch-and-rethrow

A `catch` that only rethrows adds noise and can reset or fragment the stack.

```ts
// ❌ Ceremonial: adds nothing, may damage the stack.
try { doWork(); }
catch (e) { throw e; }         // pointless
// ❌ Worse: wraps without cause, losing the original.
try { doWork(); }
catch (e) { throw new Error("work failed"); }
```

Catch-and-rethrow is justified only when you **add context or translate** — and then you preserve
the cause (2.13).

## How it works (mechanics) — the erasure funnel

Errors rarely vanish in one step; they are diluted:

```text
  Raw error (ECONNRESET, SQLSTATE 23505)
        │  wrapped "something failed"        ← cause dropped (2.13)
        ▼
  AppError (vague code)
        │  catch { log.debug(...) }          ← swallowed (2.14)
        ▼
  (no signal reaches metrics)
        │  catch { return null }             ← failure → success (2.15)
        ▼
  Corrupt downstream state discovered weeks later
```

Each arrow is a principle violation. Preventing any one of them would have preserved the trail.

## Worked example

**WebhookIngest** — inbound Stripe webhooks. A `charge.succeeded` event must be processed exactly
once (idempotent) and never dropped.

```ts
// ❌ Multiple erasures: swallow + failure→success + no cause.
app.post("/webhooks/stripe", (req, res) => {
  try {
    verifySignature(req);          // could throw
    processEvent(req.body);
  } catch (e) {
    // swallowed; returns 200 so Stripe never retries; event lost
  }
  res.status(200).send("ok");
});
```

```ts
// ✅ Preserve cause, fail loudly, idempotent, let Stripe retry on real failures.
app.post("/webhooks/stripe", async (req, res) => {
  let event;
  try {
    event = verifyAndParse(req);          // throws SignatureError — handled below
  } catch (err) {
    return res.status(400).json({ code: "WEBHOOK_SIGNATURE_INVALID" }); // terminal, no retry
  }
  if (await alreadyProcessed(event.id)) {
    return res.status(200).json({ duplicate: true, eventId: event.id }); // idempotent success
  }
  try {
    await processEvent(event, { idempotencyKey: event.id });
    return res.status(200).json({ ok: true });
  } catch (err) {
    // Real processing failure: surface it and let Stripe retry (at-least-once).
    log.error({ err, eventId: event.id, type: event.type }, "webhook processing failed");
    return res.status(500).json({ code: "WEBHOOK_PROCESSING_FAILED" });
  }
});
```

The difference: a bad signature is **terminal** (`400`, no retry), a duplicate is a **success**
(idempotent), and a genuine processing failure is **preserved and retryable** (`500`). No signal is
erased; the cause is attached; failure never masquerades as success.

## Key data / numbers

| Item | Value | Why |
| ---- | ----- | --- |
| Stripe signature header | `Stripe-Signature`, default 300s tolerance | Fail-safe on stale/replayed events |
| Duplicate webhook response | `200` (idempotent) | Stripe stops retrying on 2xx |
| Processing-failure response | `500` | Stripe retries with backoff |
| Invalid-signature response | `400` | Terminal; do not retry |
| ES2022 `Error.cause` | Node 16.9+ | Native cause preservation |
| SQLSTATE unique violation | `23505` | Must be preserved, not overwritten |

## Real-world use case — Acme SaaS

Acme's `ExportJob` wrote a CSV to S3. The upload call was wrapped in `catch { return; }` — a
failure→success violation. When S3 throttled (`503 SlowDown`) during a peak, the job reported
`completed` while the object was never written. Customers opened tickets ("export says done, file
missing") for three weeks before anyone connected the dots, because the error had left no trace.
The fix was three principles: **preserve cause** (`fmt.Errorf("upload: %w", err)`), **don't swallow**
(log + mark job failed so it lands in the DLQ), and **never fake success** (only mark `completed`
after a 2xx from S3). Silent export failures went to zero.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Preserve full cause internally | Great diagnostics | Slight memory/CPU | Always (internally) |
| Abstract the public error | Stable contract, safe | May hide detail | All external responses |
| Catch-and-rethrow with context | Adds actionable info | Minor overhead | Boundary translation |
| Catch-and-rethrow bare | — | Noise, stack damage | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Attach `cause` on every wrap | `throw new Error("failed")` |
| Handle once, at the owning layer | Double-log/double-retry the same error |
| Let failures fail (surface them) | `catch { return success }` |
| Catch only to add context or translate | Ceremonial try/catch that only rethrows |

## Common mistakes

- **`catch (e) { console.log(e) }`** with no rethrow — swallowed with a false sense of diligence.
- **Wrapping without cause** — "helpful" new error that destroys the original.
- **Retry in three layers** — amplification (Chapter 27).
- **Debug-level logging of errors** — signals that never reach alerting.

## Checklist

- [ ] Every wrap preserves `cause`/`%w`/`from exc`.
- [ ] No catch block swallows silently.
- [ ] No failure path returns a success-shaped result.
- [ ] Each condition is handled at exactly one layer.
- [ ] Catch-and-rethrow blocks add context or translate.

## Related

- [Implicit Behavior and Error Erasure — Deep Dive](../02-deep-dive/02-implicit-behavior-and-error-erasure.md)
- [Chapter 12 — Exception Propagation and Control Flow](../../../part-05-exception-mechanics/12-exception-propagation-and-control-flow/README.md)
- [Chapter 16 — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Glossary: error translation](../../../GLOSSARY.md)
