# Handling Anti-Patterns: The Eight Code-Level Sins

> Part XVII · Chapter 46 · Sections 46.13–46.16, 46.18, 46.19, 46.21, 46.22 · _Estimated reading time: 18 min_
> **Prerequisite:** [Structural Patterns](./01-structural-patterns.md), [Catch Blocks and Recovery Logic](../../../part-05-exception-mechanics/13-catch-blocks-and-recovery-logic/README.md)

## In one sentence

Eight recurring **code-level anti-patterns** — catch-all, empty catch, swallow-and-continue,
exception-driven business flow, generic messages, deep wrappers, catch-log-without-rethrow, and
success-shaped failures — account for most error-handling defects found in review, and each has
a one-sitting refactor.

## Why this matters in production

These anti-patterns share a property: they *look* like error handling while destroying
information. The catch swallows the cause; the log line without rethrow converts an outage into
a mystery; the 200-with-error-body converts a contract into a guessing game. Because they
compile, pass happy-path tests, and even silence alerting, they survive reviews. Naming them is
the intervention: "that's 46.21" resolves a design debate into a 10-minute refactor.

Severity ordering used below (also in the reference catalog): **46.22 and 46.15 can corrupt
data; 46.21 and 46.14 hide outages; 46.13 and 46.19 destroy debuggability; 46.16 and 46.18 tax
every future reader.**

## 46.13 — Catch-all anti-pattern

**What:** A blanket `catch` (often with a catch-all error type) that flattens every failure into
one undifferentiated outcome — typically at the wrong layer.

```ts
// ❌ 46.13 — controller flattens everything to 500, including declines and validation.
try { res.json(await svc.create(req.body)); }
catch { res.status(500).json({ error: "Something went wrong" }); }
```

**Why it hurts:** A card decline (`402`), a slug conflict (`409`), and a Postgres outage
(`503`) become the same `500`. Clients cannot branch; Stripe retries the wrong classes; support
cannot triage. **Refactor:** delete the local catch; let the typed error reach the one global
handler that reads registry metadata.

## 46.14 — Empty catch

**What:** `catch (e) {}` — or `catch {}` — with no logging, no rethrow, no state handling.

```ts
// ❌ 46.14 — cache write failure vanishes; stale data served forever, invisibly.
try { await redis.set(key, value); } catch {}
```

**Why it hurts:** The failure does not exist anywhere: not in logs, not in metrics, not in the
return value. The most charitable reading is "the author believed this was optional"; the
uncharitable truth is usually "the author needed the compiler to shut up." **Refactor:** if the
operation is genuinely optional, log at debug with the error and a comment stating the accepted
degradation; if not, rethrow (or return a typed failure).

## 46.15 — Swallow-and-continue

**What:** Catch, maybe log, then continue the happy path **with invalid or missing state** —
turning an error into silent wrong behavior.

```ts
// ❌ 46.15 — audit write fails; checkout continues; compliance gap discovered months later.
try { await audit.record("checkout.charged", { tenantId, amount }); }
catch (e) { log.warn(e); }
await fulfill(order);   // continues regardless — audit trail now has a hole
```

**Why it hurts:** This is the anti-pattern that corrupts data: the system *believes* it
completed a workflow whose required side effect did not happen. **Refactor:** classify. If the
side effect is required for correctness (audit, outbox, entitlement), it is part of the unit of
work — fail the unit or use a transactional outbox so the write cannot be lost. If it is truly
optional, swallow *explicitly*, with the degradation documented at the catch site.

## 46.16 — Exception-driven business flow

**What:** Throwing and catching exceptions to implement **expected, in-contract** control flow
— where the language's result/branching mechanisms are the right tool.

```ts
// ❌ 46.16 — "not found" is an expected outcome, thrown and caught across three layers.
try { return repo.getCart(id); }
catch (NotFoundError) { return createEmptyCart(id); }
```

**Why it hurts:** Expected outcomes pay exception construction and stack-capture costs; the
signature hides the failure mode from callers; and the same throw site gets "handled" differently
by four callers. Reserve throws for exceptional conditions (Chapter 1). **Refactor:** return
`Cart | null` / `Result` for expected absence; throw only when absence is a bug at that point.

## 46.18 — Generic messages

**What:** Errors whose user-visible or log-visible text carries no discriminating information —
`"An error occurred"`, `"Operation failed"`, `"Invalid input"` — often paired with a code that
is equally generic (`ERR_1001`).

**Why it hurts:** Users cannot act ("what input?"); engineers cannot grep; the registry entry
and the message disagree in usefulness. **Refactor:** message states the condition and the
salient values (sanitized); code states the machine routing; public title lives in the
registry. Every message should pass the test: *could support distinguish this from its five
nearest sibling errors using only this line?*

## 46.19 — Deep wrappers

**What:** Wrapping-and-rethrowing at every layer, so the same failure accumulates
`ErrorWrapper(…(…(original)))` chains with no added meaning.

```ts
// ❌ 46.19 — each layer wraps without adding a decision; cause chain is 5 hops deep.
try { await repo.save(x); }
catch (e) { throw new RepoLayerError("save failed", { cause: e }); }   // no new info
// …three more identical layers…
```

**Why it hurts:** Signal-to-noise in every stack trace and DLQ payload; support time grows
with chain length; the wrappers masquerade as handling ("we do catch there!"). **Refactor:**
wrap **only at translation boundaries** where the type and meaning actually change
(adapter → domain); elsewhere rethrow the original untouched, or add context fields (operation
name, ids) without a new wrapper type.

## 46.21 — Catch-log-without-rethrow

**What:** `catch (e) { log.error(e); }` — the error is *observed* but not propagated or
resolved. Distinct from empty catch: the log creates the illusion of handling.

**Why it hurts:** Alerting may fire (or may not, if the log level is wrong), but the caller
proceeds as if nothing happened — swallow-and-continue with a receipt. During incidents, the
log says "we saw it"; the business state says "we didn't act." It is the anti-pattern most
often defended with "but we have the logs." **Refactor:** after logging, either rethrow,
return a typed failure, or execute a documented recovery — pick one; logging alone is not an
outcome.

## 46.22 — Success-shaped failures

**What:** Encoding failure inside a success response — HTTP `200` with
`{"success": false, "error": …}`, or a `Result` whose error branch is ignored because the
function "always returns 200 anyway."

```ts
// ❌ 46.22 — card declined as 200; client SDKs treat it as a paid invoice.
res.status(200).json({ success: false, error: { code: "CHECKOUT_CARD_DECLINED" } });
```

**Why it hurts:** It breaks every consumer that uses status as the contract: retries, caches,
gateways, SDKs, monitoring (your 5xx dashboard is blind). It is a *contract* violation with
data consequences — billing sync jobs mark the invoice paid because the HTTP call "succeeded."
**Refactor:** map category/code → proper status via the registry (`402` here). If a
batch/partial endpoint needs per-item outcomes, use `207`-style semantics or an explicit
results array *with* a non-2xx top-level status when the request as a whole failed.

## Key data

- **Detection greps (first-pass audit):** `catch\s*\(\w*\)\s*\{\s*\}` (46.14);
  `catch` blocks containing only `log` (46.21); JSON bodies with `"success":\s*false` paired
  with 200 (46.22); `new \w+Error` inside catch blocks that only re-wrap (46.19).
- **Typical audit yield:** an initial sweep of a mid-size SaaS surfaces 20–60 instances,
  clustered in controllers and worker bodies; roughly a fifth are 46.21, the largest single
  category.
- **Information destroyed per swallow:** the cause chain, the classification (`retryable`),
  and the correlation id reach neither the DLQ nor the alert — three data points lost per
  instance.

## Real-world use case — Acme SaaS

A support escalation: enterprise customer reported missing weekly digest emails. Root cause
chain, reconstructed from the anti-patterns in order: the digest worker's per-user loop wrapped
each send in `catch (e) { log.warn(e); }` (**46.21**) and continued; the mail provider adapter
had a catch-all that flattened `429` rate limits and `400` bad-addresses into one generic
"send failed" (**46.13** + **46.18**); the job itself returned HTTP-style `{success: true}`
records for users whose sends had failed (**46.22** at the job-contract level), so the job's
success metric showed 100%. Three refactors: per-user sends now return typed results
(collect-all for batches), rate limits retry via the named policy, permanent address failures
emit `WEBHOOK/MAIL_ADDRESS_INVALID` codes into a dead-letter list the customer admin can fix.
Post-fix, the same failure mode is visible within one job attempt instead of one quarter.

## Trade-offs

| If you "fix" by… | You buy | You pay | Verdict |
| ---------------- | ------- | ------- | ------- |
| Deleting all local catches | Forces global-handler discipline | Must add real boundaries where degradation is wanted | Right direction; add boundaries deliberately |
| Catching and rethrowing everywhere | Nothing | Wrapper noise (46.19) | Wrong |
| Returning `null` everywhere | No exceptions | Silent branches; callers forget checks | Only for truly optional lookups |
| Proper classification + boundary + contract | Debuggable, routable, honest | Up-front design minutes | The actual fix |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Log **and** rethrow, log **and** recover, or log **and** document-optional — never log-only | Treat a log line as an outcome (46.21) |
| Return/throw typed errors for expected outcomes | Throw for in-contract branching (46.16) |
| Wrap only where the type changes (translation) | Add a wrapper layer per call stack frame (46.19) |
| Map failures to non-2xx via the registry | Ship `200 + success:false` (46.22) |

## Common mistakes

- **Fixing 46.22 by changing one endpoint.** The same pattern lives in the CLI and the job
  result contract; audit all transports in one pass.
- **Converting 46.16 to results without updating callers.** The throw was load-bearing; a
  half-migrated codebase both throws and returns null for the same condition — worse than
  either alone.
- **Adding context fields while keeping the wrapper type.** Prefer plain rethrow with
  `err.details` enrichment over new wrapper classes; wrapper classes multiply.

## Checklist

- [ ] Zero empty catches in the repo (CI grep).
- [ ] Zero catch blocks whose only statement is a log call.
- [ ] No API or job contract returns success-status with an in-body failure marker.
- [ ] Every thrown exception corresponds to an *exceptional* condition in that layer.
- [ ] Every error message can be distinguished from its five nearest siblings by support.

## Related

- [Design Anti-Patterns](./05-design-anti-patterns.md)
- [Before/After Anti-Pattern Refactors](../03-practical-examples/02-before-after-anti-pattern-refactors.md)
- [Anti-Pattern Compounding and Remediation](../02-deep-dive/02-anti-pattern-compounding-and-remediation.md)
