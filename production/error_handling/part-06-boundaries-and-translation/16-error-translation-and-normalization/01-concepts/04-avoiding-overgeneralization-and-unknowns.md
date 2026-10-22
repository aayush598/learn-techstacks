# Avoiding Overgeneralization and Handling Unknowns

> Part VI · Chapter 16 · Sections 16.13–16.14 · _Estimated reading time: 16 min_
> **Prerequisite:** [Preserving Cause and Recoverability](./03-preserving-cause-and-recoverability.md)

## In one sentence

Translation fails in two opposite ways — **overgeneralization** (collapsing distinct errors into
one vague code, losing meaning) and **under-handling unknowns** (letting an unrecognized vendor
format through, or crashing on it) — and both are fixed by keeping the cause and defaulting to a
**safe, non-leaking, generic** mapping.

## Why this matters in production

Overgeneralization quietly destroys the contracts that recovery and UX depend on: if every DB error
becomes `DB_ERROR` and every provider error becomes `PROVIDER_ERROR`, then HTTP statuses are wrong,
users get unusable messages, and retry logic cannot distinguish permanent from transient. Unknown
formats are the mirror problem: a provider changes its error shape, and your adapter either throws
inside the catch (an outage) or passes the raw payload through (a leak).

## 16.13 — Avoiding overgeneralization

Overgeneralization is mapping **many distinct errors to the same code**. It feels safe ("we never
miss a case") but it erases the very distinction the consumer needs.

### The two failure modes of collapse

```text
❌ Too general:      every DB error  ─▶ DB_ERROR            (status? retry? unknown)
❌ Too specific:     every column    ─▶ its own top-level code (registry explosion)
✅ Right:            error *class*   ─▶ one code per class, details in meta
```

### A collapse test

For each proposed code, ask: *would any consumer ever treat two errors mapped to this code
differently?* If yes, the collapse is wrong.

| Distinct errors | Same code? | Consumer that breaks |
| --------------- | ---------- | -------------------- |
| `23505` unique vs `23503` FK | ❌ if collapsed | HTTP (409 vs 404) and UX differ |
| `400` vs `401` vs `403` | ❌ if collapsed | auth retry/redirect logic |
| LLM `429` vs `context_length_exceeded` | ❌ if collapsed | retry vs terminate |
| `ENOENT` vs `EACCES` | ❌ if collapsed | "not found" vs "permission" messaging |

### The right grain: class, not instance

Translate at the **class** level, and put the instance detail in `details`/`meta`:

```ts
// ✅ One code per meaningful class; instance detail preserved for the client.
if (e.code === "23505") {
  // The class is ALREADY_EXISTS; *which* field is instance detail.
  throw new DomainError("ALREADY_EXISTS", {
    details: { field: fieldFromConstraint(e.constraint) }, // e.g. "email"
    cause: e,
  });
}
```

Validation is the main exception worth granularity: field-level details **must** survive even when
the top-level code is one (`VALIDATION_FAILED`). See Ch. 17.

## 16.14 — Unknown third-party formats

Vendors change their error shapes, add fields, and introduce new codes without warning. Your adapter
must treat "unknown" as a first-class case, not a crash or a pass-through.

### The unknown-error contract

For any error your adapter does not recognize, produce:

1. A **stable generic code** (`PROVIDER_ERROR`, `UNKNOWN_PROVIDER_ERROR`).
2. A **safe message** ("The provider returned an unexpected error.").
3. A **default classification** — usually `transient: false` (safer: retrying unknown things can
   storm; but provider 5xx commonly maps transient).
4. The **raw error as `cause`** (server-side only).
5. An **alert/log** so the new format is noticed.

```python
def from_provider(resp) -> AppError:
    try:
        body = resp.json()
    except ValueError:
        # Provider returned non-JSON (HTML error page, empty body) — unknown format.
        return AppError("PROVIDER_MALFORMED_RESPONSE", "DEPENDENCY",
                        transient=resp.status_code >= 500,
                        safe_message="The provider returned an unexpected response.",
                        cause=resp)

    code = body.get("error", {}).get("code") or body.get("type")
    mapped = KNOWN.get(code)
    if mapped is None:
        # New/unknown vendor code: safe generic + alert; never pass the raw body through.
        log.warning("unknown provider error code", extra={"code": code, "status": resp.status_code})
        return AppError("PROVIDER_ERROR", "DEPENDENCY",
                        transient=500 <= resp.status_code < 600,
                        safe_message="The provider returned an unexpected error.",
                        cause=resp)
    return mapped
```

### Rules for unknowns

| Rule | Rationale |
| ---- | --------- |
| **Never throw inside the translator** | A bug in error handling during error handling is an outage |
| **Never pass the raw payload through** | Leaks vendor internals and PII |
| **Default transient by status when possible** | 5xx unknown → transient; 4xx unknown → permanent |
| **Record the unknown code** | So you can add a mapping before it becomes common |
| **Keep the cause server-side** | Full payload for debugging, none for clients |

### Unknown *local* errors

The same principle applies to base exceptions in your own code. An unrecognized `Exception` at a
boundary maps to `INTERNAL_ERROR` with `transient: false` and an alert — not to a retry, and not to
the raw object.

```ts
} catch (err) {
  if (err instanceof AppError) throw err;         // already normalized
  log.error({ err }, "unexpected error");          // alert-worthy
  throw new AppError({ code: "INTERNAL_ERROR", category: "INTERNAL",
                       transient: false, cause: err });
}
```

### Unknown codes on the *client* (forward compatibility)

A client receiving a code it does not know must degrade gracefully — never crash. This is the
forward-compatibility rule (Ch. 19): **unknown codes fall back to the status-based behavior.**
Keep the status meaningful so an old client can still act.

## Key data / numbers

- Default for unknowns: `transient = (status >= 500)`; never default all-unknowns to retryable.
- Distinct classes that must not collapse: `409` vs `404` (unique vs FK), `429` vs
  `context_length_exceeded`, `404` vs `403`.
- Provider formats that vary: Stripe uses `error.type` + `error.code`; AWS uses XML `<Code>`;
  OpenAI uses `error.code`/`error.type`; Anthropic uses `error.type`.

## Real-world use case — AgentRun

`AgentRun`'s LLM adapter mapped exactly three provider codes. When the provider introduced an
undocumented `overloaded_error`, the adapter's `switch` fell through and threw — **inside the catch**
— turning every overloaded request into an unhandled crash. The fix added an explicit unknown
branch: stable `PROVIDER_ERROR`, `transient = true` for 5xx, cause preserved, and a `warn` log. The
next new code the provider shipped was handled automatically.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map at the class level; keep instance detail in `details` | Collapse all DB/provider errors into one |
| Have an explicit unknown branch with a safe default | Let the adapter throw on an unknown code |
| Alert on unknown codes | Silently pass the raw payload through |
| Default unknown 5xx → transient, 4xx → permanent | Default everything to retryable |
| Make clients degrade on unknown codes | Crash the client on an unrecognized code |

## Common mistakes

- **`default: throw err`** in a translator — error handling that itself fails.
- **`DB_ERROR`/`PROVIDER_ERROR` for everything** — statuses and retries become guesses.
- **Passing the vendor body through** "to be helpful" — a leak and a coupling.
- **Not logging unknowns** — the new format is discovered via an incident.

## Checklist

- [ ] Each translated code passes the collapse test.
- [ ] Field-level validation details survive collapse.
- [ ] Every adapter has an explicit unknown branch with a safe default.
- [ ] Unknown codes are logged/alerted for mapping.
- [ ] Clients degrade gracefully on unknown codes.

## Related

- [Vendor Codes, Tables, and Versioning](./05-vendor-codes-tables-and-versioning.md)
- [Methodology for unknown local errors](../02-deep-dive/01-translation-tables-and-policies.md)
- [Part VIII — HTTP Error Semantics](../../../part-08-http-and-api/19-http-error-semantics/README.md)
