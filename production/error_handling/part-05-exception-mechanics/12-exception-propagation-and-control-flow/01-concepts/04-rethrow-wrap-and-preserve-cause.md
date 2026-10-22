# Rethrow, Wrap, and Preserve Cause

> Part V · Chapter 12 · Sections 12.12, 12.13, 12.14, 12.15, 12.18 · _Estimated reading time: 17 min_
> **Prerequisite:** [Propagation Through Call Stacks](./01-propagation-through-call-stacks.md)

## In one sentence

**Wrapping** attaches meaningful context to an error while the **original cause and stack stay
attached underneath**; anything that replaces the cause, or rethrows a fresh error, is masking and
destroys the trail you will need at 3 a.m.

## Why this matters in production

A single `throw new Error("something failed")` in a hot path can turn a five-minute incident into
a five-hour one. The wrapper points at a line that never failed; the real cause (an expired token,
a unique-constraint violation) is gone. Conversely, a consistent wrap discipline gives you a
readable *story*: what the code was trying to do, at each level, down to the driver error.

## Core concept

There are four distinct actions, often confused:

| Action | What it does | Keeps original cause? | When |
| ------ | ------------ | --------------------- | ---- |
| **Rethrow original** | `throw err` / `return err` | ✅ Yes | You caught only to run cleanup or log |
| **Wrap with context** | New error with `cause: err` | ✅ Yes | You can name the operation that failed |
| **Translate** | Map to a domain/transport error | ✅ Must preserve | At a boundary (Chapter 16) |
| **Replace (mask)** | New error, no cause | ❌ No | ❌ Almost never |

> **Rule.** The *cause is immutable*. You may add a layer of context above it; you may not throw
> the cause away.

### Rethrowing the original (12.12)

If a catch block does not change the error, rethrow the **same object**. In languages with checked
or typed semantics, `throw err` preserves identity, where `throw new Error(err.message)` does not.

### Wrapping with context (12.13)

Wrap to answer "what was the code trying to do?". The wrapper message names the *operation*, the
cause names the *failure*. Do **not** copy the cause's message into the wrapper — that duplicates
text and hides structure.

```text
ExportJobChunkFailed: exporting chunk 42 of orders.csv
  caused by: S3PutObjectError: Access Denied (403)
    caused by: error: AuthorizationHeaderMalformed
```

### Preserving stack/cause (12.14)

Different runtimes preserve differently:
- **JS/TS**: `new Error(msg, { cause })`; the `cause` chain is walked manually or by the logger.
- **Python**: `raise NewError(...) from err` sets `__cause__`; `raise ... ` alone sets
  `__context__`.
- **Go**: `fmt.Errorf("doing X: %w", err)` wraps; `%v` does **not** wrap.
- **Java**: `new XException("...", cause)`; `initCause` for legacy.
- **Rust**: `#[source]`/`Error::source()` via `thiserror`; or `anyhow::Context`.

### Avoiding masking (12.15)

Masking is when the original error is unrecoverable from the new one. Symptoms: the stack starts
at the wrapper, the cause is `undefined`/empty, or the message says "error occurred". Masking is
the single most common cause of un-diagnosable incidents.

### Nested failures (12.18)

A failure *inside a catch block* (recovery itself failing) creates a nested failure. Preserve the
primary, attach the recovery failure as **suppressed** (Chapter 13.12, Chapter 14.13).

## How it works (mechanics)

Wrapping builds a **cause chain** (a linked list). Good loggers and `errors.Is/As`, `instanceof`,
and `__cause__` traversal walk the whole chain.

```text
top:  CheckoutFailed
        │ cause
        ▼
      PaymentDeclined
        │ cause
        ▼
      GatewayHTTPError 502
        │ cause
        ▼
      TLSHandshakeTimeout
```

`errors.Is(err, context.DeadlineExceeded)` in Go will find the deadline deep in the chain. In
JS, `err.cause` gives you the next node; loop until `undefined`.

## Worked example

Before (masking) and after (preserving), same failure:

```ts
// ❌ Before — masks everything
try {
  await gateway.charge(payment);       // throws TLSHandshakeTimeout
} catch (err) {
  throw new Error("Charge failed");    // stack now points HERE; cause lost
}

// ✅ After — context above, cause intact
try {
  await gateway.charge(payment);
} catch (err) {
  throw new PaymentFailed("charging card for order " + order.id, { cause: err });
}
```

Python equivalent:

```python
try:
    gateway.charge(payment)
except TLSError as err:
    raise PaymentFailed(f"charging card for order {order.id}") from err
```

Go equivalent:

```go
if err := gateway.Charge(ctx, payment); err != nil {
    return fmt.Errorf("charging card for order %s: %w", order.ID, err)
}
```

All three produce a chain: `PaymentFailed → TLSError → net timeouts`, with the original stack.

## Key data / numbers

- **JS `Error.cause`** — standard since ES2022; loggers like pino serialize it when configured.
- **Python `__cause__` / `__context__`** — `raise X from Y` sets `__cause__`; implicit during
  `except` sets `__context__` (set `from None` to suppress, rarely correct).
- **Go `%w`** — wraps a single error; use `errors.Join` for multiple; `%v` drops the chain.
- **Java** — always pass `cause` to the constructor; `getCause()`/`getSuppressed()`.
- **Rust `anyhow`** — `.context("...")` wraps and keeps the source chain.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` wrapped every failure as `new Error("webhook failed")`. When Stripe
changed a signature header, the on-call engineer could not tell a *signature mismatch* from a
*body parse error* — both read "webhook failed". They adopted a `WebhookError` type with a
`code` and preserved the underlying parser/verifier error as `cause`. Mean time to diagnose
dropped from ~40 minutes to under 5.

## Trade-offs

| Approach | Pros | Cons | When |
| -------- | ---- | ---- | ---- |
| Rethrow original | Zero loss; identity preserved | Caller sees low-level error | Cleanup-only catch |
| Wrap with operation name | Readable story; cause intact | One more type to know | Every meaningful layer |
| Translate to domain | Stable contract | Must carry cause | Boundaries |
| Replace | "Clean" single message | Destroys diagnosis | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Rethrow the same object when unchanged | `throw new Error(err.message)` |
| Name the operation in the wrapper | Copy the cause message verbatim |
| Always pass `cause`/`from`/`%w` | Build a fresh error with no cause |
| Attach secondary failures as suppressed | Overwrite the primary with the recovery error |
| Keep messages structured (code + context) | Use "an error occurred" |

## Common mistakes

- **Wrap-then-mask**: creating a richer type but forgetting to pass `cause`.
- **Double-wrapping the same meaning** at every layer: `CheckoutError → CheckoutError → ...`.
- **String-wrapping** in logs: `log.error("failed: " + err)` loses the object and the chain.
- **Losing the stack in async hops** by constructing a new error *after* the await boundary
  without the cause.

## Checklist

- [ ] Every catch that changes the error passes the original as `cause`.
- [ ] No `throw new Error(err.message)` anywhere.
- [ ] Wrapper messages name the failed operation, not the symptom.
- [ ] Loggers traverse and print the full cause chain.
- [ ] Recovery failures are attached as suppressed, not thrown over the primary.

## Related

- [Propagation Through Call Stacks](./01-propagation-through-call-stacks.md)
- [Stack Traces and Cause Chains](../02-deep-dive/01-stack-traces-and-cause-chains.md)
- [Preserving Cause — Before/After](../03-practical-examples/02-preserving-cause-before-after.md)
- [Error Translation and Normalization (Part VI)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
