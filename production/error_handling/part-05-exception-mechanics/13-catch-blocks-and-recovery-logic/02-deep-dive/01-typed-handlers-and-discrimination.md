# Typed Handlers and Error Discrimination

> Part V · Chapter 13 · Sections 13.3–13.5 (mechanics) · _Estimated reading time: 19 min_
> **Prerequisite:** [Catching Specific Types and Categories](../01-concepts/02-catching-specific-types-and-categories.md)

## In one sentence

**Discrimination** — telling one kind of error from another inside a catch — is the foundation of
correct recovery, and it must be based on **stable machine identity** (type or code), never on
human-readable message text.

## Why this matters in production

If two errors are indistinguishable in a catch, they get the same handling. A retryable timeout and
a permanent validation error that look alike will be retried together — one wasted, one harmful. A
card-declined and an auth-failure that look alike produce the wrong user experience. Discrimination
is what makes the catch *specific* rather than approximate.

## Core concept

Four discrimination mechanisms, weakest to strongest:

| Mechanism | Example | Robustness |
| --------- | ------- | ---------- |
| **Message text** | `err.message.includes("timeout")` | ❌ Brittle; localizable; changes |
| **Status/errno** | `err.code === "ETIMEDOUT"`, HTTP `504` | ✅ Stable per surface |
| **Type/instance** | `instanceof TimeoutError` | ✅ Local; ⚠️ realm-sensitive |
| **Discriminated union** | `match e { Timeout => …, _ => … }` | ✅✅ Exhaustive, compiler-checked |

The strongest design is a **discriminated union** (Rust enum, TS discriminated union, sealed
class), because the compiler forces the unknown branch to exist.

### Handling multiple categories (13.4)

Normalize diverse errors into a small set of **categories** with distinct policies:

```text
raw errors                              categories (policy)
TimeoutError, ETIMEDOUT, 504     ──▶    Transient   → retry
23505, ConflictError, 409        ──▶    Conflict    → surface
ValidationError, 400, 422        ──▶    Invalid     → 4xx field errors
401, 403, AuthError              ──▶    Auth        → deny, no retry
everything else                  ──▶    Unknown     → log + rethrow
```

### Known vs unknown (13.5)

The category set must have a **default**: the Unknown bucket. Its handler logs context and
rethrows. Without it, an unmodeled error is silently mis-handled.

## How it works (mechanics)

### By type (Java)

```java
try {
    handler.handle(request);
} catch (ValidationException e) {       // most specific first
    respond(422, e.getErrors());
} catch (ConflictException e) {
    respond(409, "conflict");
} catch (Exception e) {                  // unknown — must rethrow/log
    log.error("unhandled", e);
    throw e;
}
```

The compiler enforces ordering for checked exceptions.

### By code (Go)

```go
func classify(err error) Category {
    var netErr net.Error
    switch {
    case errors.As(err, &netErr) && netErr.Timeout():
        return Transient
    case errors.Is(err, ErrConflict):
        return Conflict
    case errors.Is(err, ErrValidation):
        return Invalid
    default:
        return Unknown
    }
}
```

`errors.As` finds a typed error in the `%w` chain; `errors.Is` matches a sentinel. Both traverse
wraps, so classification survives translation.

### By discriminated union (Rust)

```rust
match err {
    AppError::Transient { .. } => retry(),
    AppError::Conflict       => respond(409),
    AppError::Validation(v)  => respond_fields(422, v),
    // no wildcard needed — the match is exhaustive
}
```

Adding a new variant forces every handler to be updated — the compiler is your unknown-branch
tracker.

### By tag (TS across boundaries)

For errors crossing a network or a duplicated module, `instanceof` is unreliable. Use a tag:

```ts
type AppError =
  | { kind: "transient"; retryAfter?: number }
  | { kind: "conflict"; resourceId: string }
  | { kind: "invalid"; fields: Record<string, string> };

function isAppError(e: unknown): e is AppError {
  return typeof e === "object" && e !== null && "kind" in e;
}
```

## Worked example — one classify function, used everywhere

```ts
type Category = "transient" | "conflict" | "invalid" | "auth" | "unknown";

function classify(err: unknown): Category {
  const code = (err as any)?.code ?? (err as any)?.name;
  switch (code) {
    case "ETIMEDOUT":
    case "ECONNRESET":
    case "TRANSIENT":
    case "40001":            // PostgreSQL serialization_failure
      return "transient";
    case "23505":            // PostgreSQL unique_violation
    case "CONFLICT":
      return "conflict";
    case "VALIDATION":
    case "23502":            // not_null_violation
      return "invalid";
    case "401":
    case "403":
      return "auth";
    default:
      return "unknown";
  }
}
```

Then every catch in the codebase is tiny and consistent:

```ts
try {
  return await op();
} catch (err) {
  switch (classify(err)) {
    case "transient": return retryPolicy.run(() => op());
    case "conflict":  return { ok: false, reason: "version_conflict" };
    case "invalid":   return { ok: false, reason: "invalid", cause: err };
    case "auth":      throw err;      // deny; never retry
    default:          logger.error({ err }, "unclassified"); throw err;
  }
}
```

One `classify` function = one place to add new codes, and the unknown branch is centralized.

## Key data / numbers

- **PostgreSQL SQLSTATEs**: `23505` unique_violation, `23502` not_null_violation, `40001`
  serialization_failure, `40P01` deadlock_detected.
- **POSIX errno via Node**: `ETIMEDOUT`, `ECONNRESET`, `ECONNREFUSED`, `EAI_AGAIN` (DNS, retryable).
- **gRPC**: `DEADLINE_EXCEEDED (4)`, `UNAVAILABLE (14)` transient; `INVALID_ARGUMENT (3)`,
  `PERMISSION_DENIED (7)` permanent.
- **HTTP**: `429`, `502`, `503`, `504` transient candidates; `400`, `401`, `403`, `404`, `409`,
  `422` permanent.

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` retried *every* webhook failure, including signature mismatches. Because
discrimination was `err.message.includes("signature")` (brittle), a wording change in the Stripe
SDK broke it silently and mismatches were retried forever. They introduced a `classify()` keyed on
stable codes: signature → `auth` (no retry, reject), duplicate → `conflict` (idempotent ack),
timeout → `transient` (retry). Retry storms stopped and security posture improved.

## Trade-offs

| Discrimination | Pros | Cons | When |
| -------------- | ---- | ---- | ---- |
| Message text | Quick | Brittle, unsafe | Never |
| Error code | Stable across boundaries | Needs registry discipline | External/driver errors |
| `instanceof` type | Ergonomic locally | Realm/module pitfalls | In-process only |
| Discriminated union | Exhaustive, safe | More upfront modeling | New internal code |
| Central `classify()` | One place to maintain | Another indirection | All production services |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Discriminate on type or stable code | `message.includes(...)` |
| Centralize classification | Re-derive categories per handler |
| Model unknown distinctly | Use a wildcard that silently handles all |
| Normalize driver codes → categories | Compare raw vendor strings inline |
| Use tagged unions across boundaries | Rely on `instanceof` cross-realm |

## Common mistakes

- **Message matching** — breaks on any wording/localization change.
- **Scattered classification** — five handlers, five slightly different rule sets.
- **No default category** — new errors are mishandled silently.
- **Comparing vendor codes directly everywhere** — vendor coupling, hard to change.
- **Assuming `instanceof` works across serialization** — it does not; serialize a `kind`.

## Checklist

- [ ] All discrimination uses types or stable codes.
- [ ] A single `classify()`/registry maps codes → categories.
- [ ] Categories have distinct policies.
- [ ] An explicit unknown category logs and rethrows.
- [ ] Cross-boundary errors carry a serialized `kind`/`code`.

## Related

- [Catching Specific Types and Categories](../01-concepts/02-catching-specific-types-and-categories.md)
- [Recovery Failure and Recursion](./02-recovery-failure-and-recursion.md)
- [Error Codes and Error Registries (Part III)](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Error Translation and Normalization (Part VI)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
