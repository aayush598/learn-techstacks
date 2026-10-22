# Translation Directions

> Part VI · Chapter 16 · Sections 16.3–16.9 · _Estimated reading time: 22 min_
> **Prerequisite:** [Why Translate and Normalize](./01-why-translate-and-normalize.md)

## In one sentence

There are seven translation directions — **native→application, DB→domain, external→internal,
framework→application, domain→transport, worker→job failure, OS→application** — and each one has a
canonical input, output, and preserved field.

## Why this matters in production

Translation is directional. Translating *inbound* infrastructure errors into the domain is a
different job from translating *outbound* domain errors into the transport contract. Mixing the
directions (e.g. trying to map a domain error to SQLSTATE) produces coupling and confusion. This
file gives each direction its exact source, target, and invariants.

## The directions at a glance

| # | Direction | From | To | Preserve |
| - | --------- | ---- | -- | -------- |
| 16.3 | native→application | language exceptions (`TypeError`, `ValueError`) | `AppError` | cause |
| 16.4 | DB→domain | driver errors (`SQLSTATE`) | `DomainError` | cause, retry class |
| 16.5 | external→internal | vendor errors (Stripe, S3, LLM) | `AppError` | cause, retryability |
| 16.6 | framework→application | framework exceptions | `AppError` | cause, field details |
| 16.7 | domain→transport | `DomainError` | HTTP/gRPC/JSON | code, category, details |
| 16.8 | worker→job failure | task error | job failure outcome | cause, retry vs DLQ |
| 16.9 | OS→application | `errno` / `OSError` | `AppError` | cause, transient class |

---

## 16.3 — Native → application

Language built-ins (`TypeError`, `ValueError`, `KeyError`, `IndexError`, `nil` deref, panic) are
**programming-error signals**. Translate them to an `INTERNAL_ERROR`/bug category, preserve the
cause, and **do not** map them to a user-actionable code.

```ts
// At a request boundary: never leak a TypeError as a 4xx.
try {
  return handle(req);
} catch (err) {
  if (err instanceof SyntaxError) {
    // thrown while parsing an upstream payload — a bug or a bad provider
    return internal(res, "PARSE_ERROR", err);
  }
  return internal(res, "INTERNAL_ERROR", err);
}
```

The subtlety: some native errors *are* expected. `JSON.parse` on user input throwing `SyntaxError`
is a **validation** failure (→ `400`); the same on a provider response is a **dependency bug**
(→ `502`). The *direction* is the same; the *context* picks the target.

## 16.4 — DB → domain

The highest-value translation. Driver exceptions become domain errors; **constraint identity** (not
just the SQLSTATE) selects the precise domain code.

```go
// constraint identity → precise domain error; cause preserved via %w.
if errors.As(err, &pgErr) {
    switch {
    case pgErr.Code == "23505" && pgErr.ConstraintName == "users_email_key":
        return fmt.Errorf("%w: %v", ErrEmailTaken, pgErr)
    case pgErr.Code == "23503":
        return fmt.Errorf("%w: %v", ErrReferenceMissing, pgErr)
    case pgErr.Code == "40001" || pgErr.Code == "40P01":
        return fmt.Errorf("%w: %v", ErrRetryableConflict, pgErr)
    }
}
```

Invariants for this direction:

- **Never** expose `SQLSTATE`, `constraint`, `table`, or the SQL text outward.
- **Always** map class-40/class-08 to a transient error.
- **Distinguish** unique (`23505`) from FK (`23503`) from check (`23514`).

(Full table in [the SQLSTATE map](../03-practical-examples/01-postgres-sqlstate-to-domain-to-http.md).)

## 16.5 — External → internal

Vendor SDK errors become internal errors. This direction is where **vendor coupling dies**.

```ts
// Stripe → internal; the domain never sees "card_declined" as a type string.
function fromStripe(e: StripeError): AppError {
  switch (e.type) {
    case "card_error":          return new DomainError("PAYMENT_CARD_DECLINED", { cause: e });
    case "rate_limit_error":    return new TransientError("PAYMENT_RATE_LIMITED", { cause: e });
    case "api_connection_error":return new TransientError("PAYMENT_UNAVAILABLE", { cause: e });
    case "authentication_error":return new ConfigError("PAYMENT_AUTH_FAILED", { cause: e });
    default:                    return new DependencyError("PAYMENT_PROVIDER_ERROR", { cause: e });
  }
}
```

Key rules:

- Map **vendor → stable internal code** (16.15), so a provider swap does not change consumers.
- Preserve the vendor's retry hint (`Retry-After`, `rate_limit`) as `transient` + `retryAfterMs`.
- Handle **unknown vendor codes** safely (16.14) with a default dependency error.

## 16.6 — Framework → application

Frameworks throw their own exceptions: Spring `DataAccessException`, Django `IntegrityError`,
Rails `RecordNotUnique`, Express body-parser `SyntaxError`, ASP.NET `ValidationException`. Translate
at the framework adapter so the rest of the app sees your model.

```python
# Django: framework error → application error at the view/adapter edge.
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError

def translate_framework(err: Exception) -> AppError:
    if isinstance(err, DjangoValidationError):
        return AppError("VALIDATION_FAILED", "VALIDATION", False,
                        details={"fields": err.message_dict})
    if isinstance(err, IntegrityError):
        return AppError("CONFLICT", "CONFLICT", False, safe_message="Conflicting change.")
    return AppError("INTERNAL_ERROR", "INTERNAL", False)
```

Framework errors often carry **field-level details** (useful for validation responses) — extract
them into `details` before the translation is done.

## 16.7 — Domain → transport

The outbound direction: a domain error becomes an HTTP/gRPC response. This must **not** invent
meaning; it maps the domain `code`/`category` to a protocol.

```ts
function toHttp(err: DomainError): { status: number; body: Problem } {
  const status = STATUS_BY_CATEGORY[err.category] ?? 500; // CONFLICT→409, VALIDATION→422, ...
  return {
    status,
    body: {
      type: `https://errors.acme.example/${err.category.toLowerCase()}`,
      title: err.code,
      status,
      detail: err.safeMessage,
      instance: err.meta.requestId,
    },
  };
}
```

Rules:

- **Status comes from the error's classification**, not from a per-handler guess.
- Include **field details** for validation, **safeMessage** for humans, **code** for machines.
- Never include `cause`, stack, or vendor text.

## 16.8 — Worker → job failure

A task that failed inside a worker must be translated into a **job failure outcome**: retry,
dead-letter, or terminal — plus enough context to replay safely.

```ts
// Job boundary: task error → job outcome.
async function runJob(job: Job) {
  try {
    await handler(job);
    return { outcome: "done" };
  } catch (err) {
    const app = normalize(err);
    if (app.transient && job.attempt < job.maxAttempts) {
      return { outcome: "retry", delayMs: backoff(job.attempt), cause: app.cause };
    }
    return { outcome: "dead-letter", code: app.code, cause: app.cause }; // preserve context
  }
}
```

Critical: **preserve `cause` and `code` into the dead-letter record** so a human can diagnose and
replay (Ch. 32). A DLQ entry that says only `"failed"` is useless.

## 16.9 — OS → application

The OS reports errors via `errno` / `err.code`: `ENOENT`, `EACCES`, `ECONNREFUSED`, `ECONNRESET`,
`ETIMEDOUT`, `EMFILE`, `ENOSPC`, `EPIPE`. Translate to meaningful application errors and classify
transient vs permanent.

| `err.code` | Meaning | Category | Transient |
| ---------- | ------- | -------- | --------- |
| `ENOENT` | file not found | NOT_FOUND | No |
| `EACCES` | permission denied | AUTH/CONFIG | No |
| `ECONNREFUSED` | nothing listening | DEPENDENCY | Yes (may be restart) |
| `ECONNRESET` | connection reset | DEPENDENCY | Yes |
| `ETIMEDOUT` | timed out | DEPENDENCY | Yes |
| `EMFILE` | fd exhaustion | RESOURCE | Yes (after relief) |
| `ENOSPC` | disk full | RESOURCE | No (until relieved) |
| `EPIPE` | broken pipe | DEPENDENCY | Usually yes |

```python
import errno
def from_os(err: OSError) -> AppError:
    if err.errno == errno.ECONNREFUSED:
        return AppError("UPSTREAM_UNAVAILABLE", "DEPENDENCY", transient=True, cause=err)
    if err.errno == errno.ENOENT:
        return AppError("FILE_NOT_FOUND", "NOT_FOUND", transient=False, cause=err)
    if err.errno == errno.EMFILE:
        return AppError("FD_EXHAUSTED", "RESOURCE", transient=True, cause=err)
    return AppError("IO_ERROR", "INTERNAL", transient=False, cause=err)
```

## Direction pitfalls

| Pitfall | Why it hurts |
| ------- | ------------ |
| Translating domain→DB (reverse direction) | Couples domain to storage |
| Mapping native `TypeError` to `400` | Hides a bug as user error |
| Passing vendor `type` outward | Coupling; client breaks on provider change |
| Dropping framework field details | Loses actionable validation info |
| DLQ entry with no `cause`/`code` | Unreplayable, undiagnosable |

## Key data / numbers

- OS: `ECONNREFUSED`/`ECONNRESET`/`ETIMEDOUT` transient; `EACCES`/`ENOENT` permanent; `EMFILE`/
  `ENOSPC` resource.
- DB: class 23 permanent, class 40/08 transient, class 42 deploy fault.
- Vendor: map `Retry-After` (Stripe/OpenAI 429) to `retryAfterMs`.
- Transport: `category` → status (`CONFLICT→409`, `VALIDATION→422`, `NOT_FOUND→404`, `AUTH→401/403`).

## Real-world use case — AgentRun

`AgentRun` calls an LLM provider and tools. Three directions meet: the provider error becomes an
internal error (16.5), a tool's OS/socket error becomes an internal dependency error (16.9), and a
domain rule ("token budget exceeded") becomes a transport response (16.7). Before translation, the
agent retried `context_length_exceeded` (a permanent provider error) forever. After mapping
provider codes → internal codes with `transient=false`, the run terminated cleanly with a
`TOKEN_LIMIT_EXCEEDED` outcome.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate each direction at its boundary | Mix directions (domain→DB, SQL→user) |
| Preserve cause, retry class, and field details | Discard details and cause |
| Map vendor → stable internal code | Leak vendor `type` to clients |
| Preserve `cause`/`code` into the DLQ | Store an unhelpful `"failed"` |

## Common mistakes

- **One-directional normalization.** Handling inbound but never defining the outbound transport map.
- **Treating a native parse error uniformly** regardless of user vs provider context.
- **Losing `Retry-After`** during external→internal translation.

## Checklist

- [ ] Every inbound dialect has a named translation function.
- [ ] Each direction preserves cause and retry class.
- [ ] Domain→transport maps from classification, not per-handler guesses.
- [ ] Job failures preserve `code` + `cause` for replay.
- [ ] OS/vendor codes are never exposed outward.

## Related

- [Preserving Cause and Recoverability](./03-preserving-cause-and-recoverability.md)
- [Vendor Codes, Tables, and Versioning](./05-vendor-codes-tables-and-versioning.md)
- [Part IX — Repository and Data Access Error Handling](../../../part-09-database-and-transactions/24-repository-and-data-access-error-handling/README.md)
