# Repository Responsibilities and the Domain Boundary (24.1, 24.2, 24.11)

> Part IX · Chapter 24 · Sections 24.1, 24.2, 24.11 · _Estimated reading time: 18 min_
> **Prerequisite:** [Layered Error-Handling Architecture (Ch. 9)](../../../part-04-architecture/09-layered-error-handling-architecture/README.md)

## In one sentence

A repository **owns persistence mechanics and error translation** — it does not own business
policy — and the domain boundary is the line past which **no driver type, SQL fragment, or
constraint name may travel**.

## Why this matters in production

When repositories leak, the consequences compound. A service that catches
`psycopg2.errors.UniqueViolation` now depends on Postgres; swapping to MySQL or adding a cache
breaks it. A controller that switches on `err.code === "23505"` has re-implemented classification
in the transport layer. A domain entity that imports `SQLAlchemyError` cannot be tested without a
database. And when a repository swallows detail into `RepositoryError`, the service can no longer
tell a duplicate from an outage. The boundary is not aesthetic — it is what lets retry, HTTP
mapping, and tests stay correct.

## Core concept

```text
Controller / API        application errors, HTTP mapping
      ▲
Service                 orchestration, retry policy, transactions
      ▲                 (sees domain errors only)
Repository              driver errors → domain errors  ← the translation boundary
      ▲                 (sees SQL, SQLSTATE, constraints)
Driver / DB             SQLSTATE, errno, result sets
```

| Layer | Knows | Must not know |
| ----- | ----- | ------------- |
| Controller | HTTP, DTOs, problem details | SQL, SQLSTATE, ORM types |
| Service | domain rules, transactions, retry | driver exception classes |
| Repository | SQL/ORM, `SQLSTATE`, constraints | HTTP status, business copy |
| Domain | invariants, value objects | any persistence type |

### 24.1 Repository responsibilities

A repository:

- **executes** queries and returns domain-shaped data;
- **translates** persistence failures into application/domain errors;
- **preserves** the original cause for logs and debugging;
- **declares** intent (`insert`, `findById`, `findByIdOrFail`, `updateIfVersion`);
- **keeps** transaction participation explicit (accepts a `tx`, does not own the boundary).

A repository does **not**:

- decide HTTP status codes or user-facing messages;
- retry (that is the service/transaction wrapper's job);
- enforce business rules that belong in the domain;
- hide failures behind a single opaque error.

### 24.2 Repository vs domain errors

Two families, deliberately distinct:

| Family | Examples | Owner | Contains |
| ------ | -------- | ----- | -------- |
| **Repository/application errors** | `NOT_FOUND`, `CONFLICT`, `DB_UNAVAILABLE` | persistence adapter | retry class, safe metadata |
| **Domain errors** | `OutOfStock`, `PlanLimitExceeded`, `InvalidStateTransition` | domain | business meaning, user action |

They can meet: a repository returns `CONFLICT { field: "email" }`, and the *service* may translate
it into the domain's `EmailAlreadyRegistered`. But the repository should not know that
`EmailAlreadyRegistered` exists, and the domain should not know what `23505` is.

### 24.11 Preventing leaks through layers

The leak paths are predictable:

| Leak | Example | Fix |
| ---- | ------- | --- |
| Driver exception | `except psycopg2.Error` in service | repository translates |
| SQLSTATE in API | `"23505"` in response | map to app code |
| Constraint name | `projects_slug_key` in message | allowlist → `field` |
| SQL text | `SELECT ...` in error detail | log server-side only |
| Table/column names | `relation "users" does not exist` | generic `500` |
| ORM entity with lazy loading | entity escapes, triggers queries in controller | map to DTO/domain object |
| Transaction handle | `tx` passed to controller | keep in service |

## How it works (mechanics)

1. Repository calls the driver inside the service's transaction.
2. Driver raises a vendor error.
3. Repository **normalizes** (one function per driver) and **classifies** (one table).
4. Repository throws a repository error carrying `code`, `category`, `transient`,
   `retryScope`, `safeMessage`, `field`, `cause`, `op`.
5. Service decides: retry, translate to domain, compensate, or propagate.
6. Controller maps the application error to HTTP.

Every step narrows the vocabulary. By the controller, only your codes exist.

## Worked example

```ts
// ❌ Leaks driver + SQL to the service and API
async function findProject(id: string) {
  const res = await pool.query("SELECT * FROM projects WHERE id = $1", [id]);
  if (res.rowCount === 0) throw new Error("no rows in result set");
  return res.rows[0];                    // raw row, snake_case, db types
}

// ✅ Intent + translation + domain shape
async function findProject(tx: Tx, id: ProjectId): Promise<Project | null> {
  try {
    const row = await tx.maybeOne(
      `SELECT id, tenant_id, slug, budget FROM projects WHERE id = $1`,
      [id],
    );
    return row ? toProject(row) : null;   // null is a legitimate result
  } catch (err) {
    throw translate(normalize(err), { op: "projects.findById" });
  }
}
```

The second version never exposes `rowCount`, `pgcode`, or snake_case, and it distinguishes
"absent" (`null`) from "failed" (throw).

## Key data / numbers

- Postgres driver errors carry **`code`** (SQLSTATE), `constraint`, `table`, `column`; these are
  **server-side only**.
- A repository should expose **≤ 8 stable error codes** (`NOT_FOUND`, `CONFLICT`, `VALIDATION`,
  `DB_UNAVAILABLE`, `DB_TIMEOUT`, `SCHEMA_MISMATCH`, `DATA_INTEGRITY`, `INTERNAL`).
- `cause` retention costs nothing and saves hours: always attach the driver error.
- One translation boundary per process; if you find `SQLSTATE` in two modules, you have two.

## Real-world use case — Acme SaaS

Acme's `ProjectService` caught `psycopg2.errors.UniqueViolation` directly. When the team added a
read-through cache and later a second datastore, every `except` clause silently stopped matching,
and duplicates became `500`s. Moving translation into `ProjectRepository` — returning
`CONFLICT { field: "slug" }` — made the service datastore-agnostic and cut the error-handling
code in the service by half. The domain's `ProjectSlugTaken` is now raised in one place, from the
repository's stable code.

## Trade-offs

| Choice | Pros | Cons | When to use |
| ------ | ---- | ---- | ----------- |
| Thin repository (raw rows) | flexible, little code | leaks shape and types | never past the adapter |
| Translating repository | stable, testable | small mapping layer | default |
| Rich repository (domain objects) | clean service | mapping overhead | DDD codebases |
| Generic `RepositoryError` only | simple | loses classification | prototype only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate at the repository | Let driver errors reach the service |
| Return domain-shaped objects | Return raw rows with DB column names |
| Accept the transaction from the service | Open an implicit transaction per call |
| Expose intent-named methods | One generic `query(sql)` method everywhere |
| Keep `cause` on the translated error | Build a new error and discard the cause |

## Common mistakes

- **Catching the vendor error in the service** — recreates the coupling.
- **Returning raw rows** — snake_case and DB types leak into the API.
- **Owning the transaction in the repository** — prevents composing multiple repository calls.
- **A single `RepositoryError`** — destroys retry and status decisions.
- **Lazy-loaded entities escaping** — queries run in the controller, after the tx closed.

## Checklist

- [ ] Only repositories import the driver/ORM.
- [ ] No `SQLSTATE`, SQL text, or constraint names outside the adapter.
- [ ] Repository methods are intent-named and transaction-aware.
- [ ] Domain and repository error families are distinct.
- [ ] Every translated error carries `cause` and `op`.

## Related

- [Mapping Persistence to Application Errors (24.3, 24.12, 24.13)](./02-mapping-persistence-to-application-errors.md)
- [Leak Prevention and Metadata Preservation](../02-deep-dive/01-leak-prevention-and-metadata-preservation.md)
- [Error Boundaries (Ch. 15)](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Chapter 24 Reference](../05-reference/README.md)
