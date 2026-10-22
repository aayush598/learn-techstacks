# Preserving Cause and Recoverability

> Part VI · Chapter 16 · Sections 16.10–16.12 · _Estimated reading time: 18 min_
> **Prerequisite:** [Translation Directions](./02-translation-directions.md)

## In one sentence

Every translation must preserve two things — the **original cause** (for debugging) and the
**retry/recoverability class** (for behavior) — and must not **lose information** that a downstream
consumer needs.

## Why this matters in production

Translation has a failure mode that looks like success: the error is now "clean," but the cause is
gone (nobody can debug it) or the retry class is gone (transient errors now fail permanently, or
vice versa). Both are silent and expensive. This file makes the two preservation requirements
concrete, per language.

## 16.10 — Preserving the root cause

Translation replaces the representation; it must **not** replace the history. Attach the original
error to the new one so it stays one `unwrap()`/`stack` away.

| Language | Mechanism | Access |
| -------- | --------- | ------ |
| JavaScript/TypeScript | `new Error(msg, { cause })` (ES2022) | `err.cause` |
| Python | `raise NewError(...) from original` | `e.__cause__` |
| Go | `fmt.Errorf("...: %w", err)` | `errors.Is` / `errors.As` / `errors.Unwrap` |
| Java | `new X(msg, cause)` / `initCause` | `getCause()` chain |
| C#/.NET | `new X(msg, innerException)` | `InnerException` |
| Rust | `#[source]` (thiserror) / `anyhow::Context` | `Error::source()` |

```ts
// ✅ Preserve cause across translation.
try {
  await db.insert(user);
} catch (err) {
  throw new DomainError("EMAIL_ALREADY_USED", {
    safeMessage: "That email is already in use.",
    cause: err, // original driver error, for logs only
  });
}
```

```python
# ✅ Python: `from err` sets __cause__; the traceback shows both.
try:
    db.insert(user)
except UniqueViolation as err:
    raise DomainError("EMAIL_ALREADY_USED", cause=err) from err
```

⚠️ **The cause is server-side only.** It is for logs and deep debugging. It must never be
serialized to the client: `JSON.stringify(err)` that walks `.cause` re-leaks exactly what
translation removed (see boundary leakage, Ch. 15.14).

### Chain depth and noise

Every translation adds a link. A useful chain has **2–4 links** (origin → domain → transport).
Deeper chains are a smell: translation happening in too many places. If you cannot read the chain
top-down and understand the origin, there are too many redundant wraps (Ch. 12.15).

## 16.11 — Preserving retry and recoverability

The **retry class** is the part of the classification (Part I) that says "try again" vs "do not."
It is *semantic*, not textual: the word "timeout" in a message does not make an error transient.

Rules:

1. **Carry `transient` (or equivalent) through translation.** A Boolean is usually enough; a small
   enum (`TRANSIENT | PERMANENT | RETRY_AFTER`) is better when you have a server hint.
2. **Never let the default be "transient."** Defaulting to retryable causes retry storms on
   permanent errors (e.g. retrying `23505` or `401`). Default to **not transient** and opt in.
3. **Preserve the retry-after hint.** If the vendor sent `Retry-After: 30`, keep it.
4. **Do not change the class mid-chain.** If `40001` is transient at the repository, it must not
   become permanent when it reaches the job boundary.

```ts
interface AppError {
  // ...
  transient: boolean;      // default FALSE; set TRUE only for genuinely retryable causes
  retryAfterMs?: number;   // preserved from Retry-After / rate limit
}

function fromHttp(status: number, retryAfter?: string): AppError {
  if (status === 429) return { /* ... */ transient: true, retryAfterMs: parseRetryAfter(retryAfter) };
  if (status === 503) return { /* ... */ transient: true };
  if (status >= 500)  return { /* ... */ transient: true };
  return { /* 4xx */ transient: false }; // 400/401/403/404/409/422 are permanent
}
```

@ table:

| Source | Transient | Why |
| ------ | --------- | --- |
| `SQLSTATE 40001` / `40P01` | Yes | retry resolves the conflict |
| `SQLSTATE 53300` / `08006` | Yes | connection available later |
| HTTP `429` / `503` / `504` | Yes | server hint / overload |
| HTTP `400`/`401`/`403`/`404`/`409`/`422` | No | will recur identically |
| AWS `SlowDown` | Yes | back off, retry |
| Stripe `card_error` | No | business decline |
| LLM `context_length_exceeded` | No | retry never helps |
| `ECONNRESET` / `ETIMEDOUT` | Yes | network blip |

## 16.12 — Avoiding information loss

Transforming an error can silently drop fields a consumer relies on. Common losses:

| Field | Lost when… | Consequence |
| ----- | ---------- | ----------- |
| **Field-level details** | validation error → generic code | client cannot highlight the field |
| **Retry-after** | vendor error → generic transient | retry storms |
| **Constraint identity** | `23505` → `ALREADY_EXISTS` only | cannot tell email vs slug conflict |
| **Cause** | rethrow with a new message, no chaining | undebuggable incident |
| **Request/correlation ID** | not carried into `meta` | cannot trace end-to-end |
| **Tenant ID** | not carried | multi-tenant diagnosis breaks |

```python
# ❌ Information loss: field details and cause dropped.
raise AppError("VALIDATION_FAILED")
# ✅ Preserved: fields + cause intact for both client and logs.
raise AppError("VALIDATION_FAILED",
               details={"fields": {"email": ["must be a valid address"]}},
               cause=original) from original
```

A useful invariant: **translation is lossless for the server (cause, ids, metadata) and lossy only
for sensitive/vendor detail that must not cross.** If you lose something the server needs, the
translation is wrong.

## Cause vs information vs classification

Keep the three separate:

- **Cause** = the original error object → debugging.
- **Information** = safe context (field details, correlation IDs) → behavior/UX.
- **Classification** = `category` + `transient` → policy.

Translation must preserve all three; a "clean" error missing any of them is not done.

## Key data / numbers

- Default `transient` to **false**; opt in only for the classes in the table above.
- Preserve `Retry-After` (seconds or HTTP-date, per RFC 9110) as `retryAfterMs`.
- Keep the cause chain to 2–4 links; deeper is a translation-smell.
- Carry `requestId`/`correlationId` and `tenantId` in `meta` across every boundary.

## Real-world use case — Checkout

`Checkout` translated Stripe's `rate_limit_error` into a generic `PAYMENT_FAILED` **without** the
`transient` flag or the `Retry-After` value. Result: a rate-limited charge was reported to the user
as a hard decline, and one user retried manually 14 times. The fix preserved `transient: true` and
`retryAfterMs`; the Checkout saga now waits the instructed interval and completes the payment
transparently. The only change was *not losing* fields during translation.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Attach the original error as `cause` | Rethrow a new error without chaining |
| Carry `transient` and `retryAfterMs` | Default to retryable, or drop the hint |
| Preserve field details and IDs in `meta` | Replace a detailed error with a generic one |
| Keep the cause server-side only | Serialize the cause nest to the client |
| Keep chains to 2–4 links | Wrap at every layer |

## Common mistakes

- **`throw new Error("failed")`** in a catch — the cause and everything else is gone.
- **Retry class flips** mid-chain, so the job retries what the repository marked permanent.
- **Silent field-detail loss** making validation responses unhelpful.
- **Serializing the cause tree** in a debug build that then ships.

## Checklist

- [ ] Every translation attaches the original as `cause`.
- [ ] `transient` is explicitly set; default is false.
- [ ] `Retry-After` hints are preserved as `retryAfterMs`.
- [ ] Field details, requestId, and tenantId survive translation.
- [ ] Cause chains stay 2–4 links and never serialize outward.

## Related

- [Translation Directions](./02-translation-directions.md)
- [Preserving Cause and Circular Chains (deep dive)](../02-deep-dive/02-preserving-cause-and-circular-chains.md)
- [Part XI — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
