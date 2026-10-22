# Explicitness, Consistency, First-Class Errors, and Predictability

> Part I · Chapter 2 · Sections 2.1, 2.2, 2.3, 2.18 · _Estimated reading time: 22 min_

## In one sentence

Errors must be **stated explicitly** in code and contracts, handled the **same way** wherever the
same situation recurs, treated as **architectural artifacts** with owners and documented outcomes,
so that their behavior is **predictable** to anyone reading or operating the system.

## Why this matters in production

Implicit behavior is where errors go to disappear. `null` meaning "not found or failed or empty",
a function that returns `undefined` on both success-with-no-value and failure, a convention that
"we always retry DB errors" that one service silently ignores — each turns a debuggable incident
into a multi-hour archaeology session.

The cost is concrete:

- **Incident time.** Engineers spend the first 20 minutes discovering *what* happened because the
  error type does not say it.
- **Inconsistent clients.** The frontend treats a 409 as "retry" for one endpoint and "show error"
  for another because the codebase never agreed.
- **Reviewer load.** Every new `catch` needs a fresh debate because there is no standard.

Consistency is not aesthetics; it is the difference between a system you can reason about at 3 a.m.
and one you cannot.

## Core concept — four principles

### 2.1 Explicitness over implicit behavior

Make the failure visible in the type, the signature, the return value, or the response. Do not rely
on convention, out-of-band state, or "everyone knows."

| Implicit (❌) | Explicit (✅) |
| ------------- | ------------- |
| Return `null` for both "absent" and "failed" | Return `Result<T, E>` or a typed error |
| `throw new Error("something went wrong")` | `throw new ValidationError({ field, code })` |
| A boolean `false` meaning any of 6 problems | An error code per problem |
| "Retries are handled somewhere in the middleware" | A documented retry policy on the client call |

Explicitness has a cost: more types, more code. It pays back the first time someone else debugs it.

### 2.2 Consistency across the codebase

The same *situation* must produce the same *behavior*, everywhere. Not the same *message*, but the
same classification, status, retry eligibility, and outcome shape.

```ts
// ❌ Inconsistent: two endpoints, two behaviors for "duplicate"
// Endpoint A
if (isDuplicate) return res.status(200).json({ created: false });
// Endpoint B
if (isDuplicate) throw new ConflictError(); // becomes 409
```

```ts
// ✅ Consistent: one rule, defined once
// idempotent create → 200 with the existing resource
// non-idempotent create → 409 Conflict
```

Consistency is enforced at three levels:

1. **Naming/format** — one error envelope (Chapter 20).
2. **Semantics** — one mapping from category → HTTP/status/retry (Chapters 8, 19).
3. **Placement** — one place where a category is decided (Chapter 15).

### 2.3 Errors as first-class architectural concerns

An error is not an afterthought bolted on after the happy path. It has the same design weight as a
feature:

- It has an **identifier** (code), **owner** (team), and **documented outcome**.
- It appears in the **error registry** (Chapter 8) and the **public contract** (Chapter 49).
- It has a **defined lifecycle**: where it originates, where it is translated, where it ends
  (Chapter 11).
- It is **testable**: you can trigger it deliberately.

> A useful smell test: if you cannot name the owner of an error code, it has no architecture and
> will be handled by accident.

### 2.18 Make error behavior predictable

A caller should be able to answer, without reading the implementation:

1. Can this fail? Under which conditions?
2. Is the failure retryable?
3. What will the status/outcome be?
4. Does it leave partial state?

Predictability comes from the other three principles plus a written **policy** (Chapter 50). Where
predictability is impossible — genuinely ambiguous external failures — you make the *ambiguity
explicit* rather than pretending certainty.

## How it works (mechanics)

The four principles reinforce each other in a specific order:

```text
  Explicitness ──► Consistency ──► First-class ──► Predictability
  (state it)       (repeat it)     (own/register)   (reason about it)
        ▲                                                   │
        └───────────── feedback: predictable systems ───────┘
                       are easier to make explicit
```

1. You make a failure explicit (typed, coded, documented).
2. You repeat that shape consistently for the same category.
3. You register and own it, so it does not drift.
4. The result is a system whose failure behavior an operator can predict.

## Worked example

A `GET /invoices/{id}` in **Acme SaaS**. Three implementations of "invoice not found."

```ts
// ❌ Implicit + inconsistent + unpredictable
async function getInvoice(id: string) {
  const row = await db.invoices.find(id);
  return row; // null if missing — caller guesses what null means
}
```

```ts
// ✅ Explicit + consistent + predictable
class NotFoundError extends DomainError {
  readonly code = "INVOICE_NOT_FOUND";
  readonly httpStatus = 404;
  readonly retryable = false;
}

async function getInvoice(id: string): Promise<Invoice> {
  const row = await db.invoices.find(id);
  if (!row) throw new NotFoundError({ resource: "invoice", id });
  return row;
}
```

The second version tells the caller (and the global handler) exactly what happened, and any
endpoint retrieving an invoice behaves identically.

## Key data / numbers

| Item | Value | Why it matters |
| ---- | ----- | -------------- |
| Not-found status | `404` (RFC 9110) | The predictable HTTP outcome for `INVOICE_NOT_FOUND` |
| Duplicate-create status | `409 Conflict` | Consistent, non-retryable |
| Validation status | `422 Unprocessable Content` (RFC 9110) | Distinct from `400` (malformed syntax) |
| Error envelope | RFC 9457 `type`, `title`, `status`, `detail`, `instance` | One consistent public shape |
| Retry-After | RFC 9110 HTTP-date or seconds | Predictable retry guidance on `429`/`503` |
| Idempotency key TTL | Stripe keys are retained **24 hours** | Makes duplicate-create behavior predictable |
| gRPC consistency | `NOT_FOUND`=5, `ALREADY_EXISTS`=6, `FAILED_PRECONDITION`=9 | Same semantics across transports |

## Real-world use case — Acme SaaS

Acme's API originally returned `200 { "success": false, "error": "not found" }` for missing
resources on some routes and `404` on others. Mobile clients had to special-case both. Once Acme
standardized: **explicit** (`NotFoundError`), **consistent** (`404` + registered code across every
route), **first-class** (an owner + registry entry), and **predictable** (documented "not found is
never retried"), the mobile team deleted 40 lines of guesswork and incident time for 404s dropped to
near zero. The errors were the same; only the *contract* changed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fully explicit typed errors | Predictable, testable, safe | More types/boilerplate | Domain and boundary code |
| Implicit (null/boolean) | Less code, fast to write | Ambiguous, incident-prone | Throwaway scripts only |
| One global convention | Consistent, easy review | Can be rigid | All production code |
| Per-team conventions | Autonomy | Drift, integration pain | Never for shared contracts |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Encode failure in the type/signature | Use `null`/`false` to mean many things |
| Define one mapping and reuse it | Invent a new status per endpoint |
| Give every error code an owner | Ship codes with no registry entry |
| Document retryability | Let callers guess |

## Common mistakes

- **"Obvious" conventions.** The convention is obvious to the author, invisible to the on-call
  engineer six months later.
- **Silent divergence.** A new service re-implements the mapping "close enough"; clients break.
- **Predictability theater.** A doc says "retryable" but the code retries a permanent 422 anyway.
- **Registering codes but never reading the registry.** The registry must drive behavior, not just
  list names.

## Checklist

- [ ] Can every function's failure be read from its signature or return type?
- [ ] Do the same situations produce the same status/outcome everywhere?
- [ ] Does every error code have an owner and a registry entry?
- [ ] Can an operator predict retryability and outcome without reading source?

## Related

- [Structure, Separation, and Responsibility](./02-structure-separation-and-responsibility.md)
- [Preserving and Not Swallowing Errors](./04-preserving-and-not-swallowing-errors.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Glossary: error code, registry](../../../GLOSSARY.md)
