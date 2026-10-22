# What an Error Boundary Is (and Why You Need One)

> Part VI · Chapter 15 · Sections 15.1, 15.2, 15.14 · _Estimated reading time: 18 min_
> **Prerequisite:** none

## In one sentence

An **error boundary** is a deliberate architectural line where an error is caught, translated,
contained, or deliberately propagated — the place where **the representation and the owner of the
error change**, and the last place you can stop a leak.

## Why this matters in production

Consider a single missing `try/catch` around a Postgres call in a repository. The driver throws a
`UniqueViolation` carrying the SQL, the table name, and a constraint name. Without a boundary, it
propagates: the service layer rethrows it, the HTTP handler serializes it, and the client receives
a `500` whose JSON body contains **your schema**. One boundary — a repository-level translation —
would have returned a clean `409 EMAIL_ALREADY_USED`. Boundaries are simultaneously a
**reliability** control and a **security** control.

Concretely, without boundaries:

- **Blast radius grows.** A recommendations timeout 500s the whole dashboard.
- **Leakage happens.** Stack traces, SQL, hostnames, and upstream payloads reach users.
- **Decisions get made at the wrong layer.** A global handler guesses business policy it cannot know.
- **Retries are lost or added incorrectly.** A transient deadlock dies as a generic `500`.

## The three jobs of a boundary

Every boundary does at least one of these, and usually two or three together:

| Job | Question | Output |
| --- | -------- | ------ |
| **Contain** | Can the operation continue with a safe substitute? | A fallback value or a degraded path |
| **Translate** | What does this error mean in *this* layer's vocabulary? | A domain/application/transport error |
| **Decide** | Recover, retry, compensate, or terminate? | A chosen outcome, not a rethrow |

If a `try/catch` does none of these three, it is not a boundary — it is noise. Delete it.

## A boundary is a line, not a keyword

`try/catch`, `Result` matching, middleware, `defer`, and framework error handlers are all
*mechanisms*. The boundary is the **conceptual line** you choose. You can draw it without any
language keyword at all — for example, a proxy that converts every non-2xx upstream response into
a typed error.

```text
┌──────────── handler / controller ────────────┐  ← boundary: request
│   catches all, maps to HTTP, never leaks      │
│  ┌──────── application service ───────────┐   │  ← boundary: transaction
│  │  owns the unit of work + compensation   │   │
│  │  ┌──────── domain ──────────────────┐   │   │  ← boundary: domain decision
│  │  │  throws DomainError (no infra)   │   │   │
│  │  └──────────────────────────────────┘   │   │
│  │  ┌──────── repository ──────────────┐   │   │  ← boundary: DB→domain translation
│  │  │  catches driver error, preserves │   │   │
│  │  │  cause, throws DomainError       │   │   │
│  │  └──────────────────────────────────┘   │   │
│  └─────────────────────────────────────────┘   │
└────────────────────────────────────────────────┘
```

Each line is a **fate boundary**: on one side, code that may see driver exceptions; on the other,
code that must never see them.

## Why necessary (15.2)

### 1. Failure isolation

A boundary confines a failure to the smallest set of components that share fate. The unit is the
**failure domain** (Part I): a function, a request, a job, a tenant. Isolation is what converts a
100% outage into a 2% degradation.

### 2. Single ownership of decisions

Recovery requires context: does the caller care? Is the operation idempotent? Is there a fallback?
Only one layer has that context for a given failure. Boundaries make that layer explicit instead of
leaving the decision to "wherever it happens to be caught."

### 3. A translation choke point

Translation must happen exactly once. Boundaries are where you guarantee that: after the line,
everything is in the internal error model (Part III) and no vendor dialect escapes.

### 4. Security containment

The outermost boundary is the last chance to strip internals. If a driver error reaches it
untranslated, the safest outcome is a generic `500` — but you have still lost the ability to give
the caller anything actionable.

## Preventing leakage across a boundary (15.14)

Leakage is any information crossing a boundary that the other side should not hold. It takes four
common forms:

| Leak | Example | Stops at |
| ---- | ------- | -------- |
| **Schema/query** | `column "users.email_ci" does not exist` | repository boundary |
| **Infrastructure** | hostname, driver name, connection string | integration boundary |
| **Secrets/PII** | API key echoed in a provider error; email in a message | translation/redaction |
| **Vendor coupling** | `code: "card_declined"` reaching the domain | integration boundary |

```ts
// ❌ Leaky: driver error object is serialized straight to the client.
try {
  await db.insert(user);
} catch (err) {
  return res.status(500).json({ error: err }); // pg driver leaks SQL + column names
}

// ✅ Boundary + translation: the repository owns the mapping; the handler owns the status.
// repository
try {
  await db.insert(user);
} catch (err) {
  if (err instanceof pg.errors.UniqueViolation) {
    throw new DomainError("EMAIL_ALREADY_USED", { cause: err });

  }
  throw new InfrastructureError("DB_WRITE_FAILED", { cause: err });
}
```

The rule: **translate at the boundary and attach the raw error as the *cause*, never as the payload.**
The cause stays server-side for logs; the payload crosses the line.

> ⚠️ **Hazard.** A boundary that "rethrows with more context" but does not translate is not
> preventing leakage — it is delaying it. The outermost handler still receives a raw driver error.

## Key data / numbers

- PostgreSQL `SQLSTATE` `23505` = `unique_violation`; `23503` = `foreign_key_violation`;
  `23502` = `not_null_violation`; `40P01` = `deadlock_detected`. These must be caught by the
  repository boundary, never surfaced.
- Node.js OS errors carry `err.code` such as `ECONNREFUSED`, `ETIMEDOUT`, `ENOENT`; Go's
  `database/sql` exposes `sql.ErrNoRows`; Java's `SQLException.getSQLState()`. All are boundary inputs.
- HTTP statuses are decided at the **transport/request boundary**, not the repository: `409`, `422`,
  `404`, `503`.

## Real-world use case — Acme SaaS

Acme's `POST /users` endpoint used one global error handler that returned `err.message` for any
error. A failed unique insert produced `500` bodies containing
`duplicate key value violates unique constraint "users_email_key"`. Support began fielding
questions about "users_email_key." The fix was a **repository boundary**: catch `UniqueViolation`
(`23505`), translate to `DomainError("EMAIL_ALREADY_USED")` while keeping the driver error as
`cause`, and let the request boundary map that domain error to `409`. Leakage stopped, the status
became correct, and the domain no longer imported the Postgres driver.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Place a boundary where the fallback differs from propagating | Wrap every line in `try/catch` |
| Translate at the boundary; keep raw errors as `cause` | Serialize the raw error to callers |
| Give each boundary exactly one owner | Let two layers both decide the same outcome |
| Make the boundary's fallback explicit in code | Rely on comments to document intent |

## Common mistakes

- **Catch-and-rethrow as a "boundary."** Adds context but makes no containment or translation
  decision; the real boundary is elsewhere.
- **Translating too late.** By the time the global handler sees a driver error, the domain is
  already coupled to the DB.
- **Swallowing at the wrong layer.** Catching in the domain something only the request layer can
  fall back on.
- **Leaking via `cause` serialization.** A `JSON.stringify(err)` that walks `.cause` re-leaks
  everything you translated away.

## Checklist

- [ ] Does every boundary do at least one of contain / translate / decide?
- [ ] Can you name the single owner of each boundary in your request path?
- [ ] Is every raw driver/vendor error kept as `cause` and never as the payload?
- [ ] Do you have a boundary that stops schema and infrastructure leakage?

## Related

- [Code-Level Boundaries](./02-code-level-boundaries.md)
- [Nested Boundaries](../02-deep-dive/01-nested-boundaries.md)
- [Boundary Placement Guide](../05-reference/README.md)
