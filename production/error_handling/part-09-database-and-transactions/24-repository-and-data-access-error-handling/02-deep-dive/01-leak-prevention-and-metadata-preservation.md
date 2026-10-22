# Leak Prevention and Metadata Preservation (24.11–24.13)

> Part IX · Chapter 24 · Sections 24.11–24.13 · _Estimated reading time: 22 min_
> **Prerequisite:** [Mapping Persistence to Application Errors](../01-concepts/02-mapping-persistence-to-application-errors.md)

## In one sentence

Every leak is a **path**, not an accident: find the routes by which driver errors, SQL, and schema
names leave the adapter, close them with **one translation function**, and make sure the
information the server needs (`cause`, `op`, `SQLSTATE`) is preserved on the inside.

## Why this matters in production

Leaks are asymmetric. Exposing `relation "users" does not exist` hands an attacker your schema;
exposing `pgcode` makes your API contract depend on Postgres; exposing `DETAIL: Key
(email)=(a@b.com) already exists` leaks personal data into client logs and error trackers.
Meanwhile, the opposite failure — scrubbing too aggressively — destroys the only evidence that
would let you debug at 3 a.m. The goal is a **membrane**: information flows inward, not outward.

## Core concept

```text
  driver error ──────────────┐
    SQLSTATE 23505           │  INWARD: full detail allowed
    constraint projects_...  │  (cause, op, table, statement)
    DETAIL "Key (email)=..." │
                             ▼
                    ┌──────────────────┐
                    │  translate()     │   the membrane
                    └──────────────────┘
                             │
                             ▼  OUTWARD: allowlisted facts only
                    { code, category, transient,
                      safeMessage, field?, op }
```

### 24.11 The leak paths

| # | Path | How it happens | Close it by |
| - | ---- | -------------- | ----------- |
| 1 | **Exception type** | service catches `psycopg2.errors.*` | repo throws `RepoError` |
| 2 | **Raw message** | `safeMessage = str(exc)` | authored messages only |
| 3 | **Code passthrough** | API returns `err.code = "23505"` | map to app code |
| 4 | **Constraint/table names** | `field = exc.constraint` | allowlist lookup |
| 5 | **SQL text** | `sql` included in problem `detail` | omit / log only |
| 6 | **ORM entity** | entity escapes, lazy-loads after tx | map to DTO |
| 7 | **Stack trace** | `includeStack: true` in prod | server-side only |
| 8 | **Error tracker** | Sentry `extra` includes `exc.diag` | scrub before capture |
| 9 | **Logs → support tooling** | logs shipped to a customer-visible portal | redact PII |
| 10 | **Debug endpoints** | `/debug/last-error` echoes `cause` | never serialize cause |

Path 5 and 8 are the ones teams miss: the API is clean, but the error tracker or a log-based
support console becomes a second, unversioned API.

### 24.12 The error contract

One type, frozen, versioned:

```ts
interface RepoError extends Error {
  readonly code: RepoCode;          // NOT_FOUND | CONFLICT | ...
  readonly category: Category;      // CONFLICT | VALIDATION | DEPENDENCY | INTERNAL
  readonly transient: boolean;
  readonly retryScope: "none" | "statement" | "transaction";
  readonly alert: boolean;
  readonly safeMessage: string;
  readonly field?: string;          // public name
  readonly op: string;              // "projects.insert"
  readonly resource: string;        // "projects"
  readonly cause: unknown;          // server-side ONLY
}
```

`cause` is **non-enumerable** or excluded by the serializer. The simplest guarantee: the
serializer only knows the allowlisted fields, so `cause` cannot be serialized by accident.

### 24.13 Metadata preservation

| Fact | Needed for | Where it lives |
| ---- | ---------- | -------------- |
| `SQLSTATE` / errno | root-cause triage | `cause` |
| constraint | field mapping, debugging | `cause` (+ derived `field`) |
| statement / params | reproducing | `cause` (never `safeMessage`) |
| `op`, `resource` | metrics, grouping | first-class |
| retry class | retry policy | first-class |
| `requestId`, `traceId` | correlation | context, not error |
| transaction outcome | ambiguity resolution | first-class `retryScope` |

## How it works (mechanics)

1. A single `translate()` is the **only** constructor of `RepoError`.
2. `normalize()` extracts dialect facts into a neutral shape; `translate()` never touches the
   driver.
3. The serializer has an explicit **allowlist** (no spread of the error object).
4. `cause` is attached but never enumerable.
5. Tests assert both directions: (a) API body has no internals, (b) `cause` is present in-process.

## Worked example

```ts
// normalize.ts — only file that imports the driver's error type
export function normalize(err: unknown): DbFailure {
  const e = err as { code?: string; constraint?: string; sql?: string; detail?: string };
  return { sqlstate: e.code, constraint: e.constraint, sql: e.sql, detail: e.detail, raw: err };
}
```

```ts
// translate.ts — the membrane
const FIELD_BY_CONSTRAINT: Record<string, string> = {
  projects_slug_key: "slug",
  users_email_key: "email",
  memberships_user_tenant_key: "userId",
};

export function translate(db: DbFailure, op: string, resource: string): RepoError {
  const base = { op, resource, cause: db.raw };          // inward
  switch (db.sqlstate) {
    case "23505":
      return repoError({
        ...base, code: "CONFLICT", category: "CONFLICT",
        transient: false, retryScope: "none", alert: false,
        safeMessage: "That value is already taken.",
        field: db.constraint ? FIELD_BY_CONSTRAINT[db.constraint] : undefined,
      });
    case "23503":
      return repoError({ ...base, code: "REFERENCE_MISSING", category: "VALIDATION",
        transient: false, retryScope: "none", alert: false,
        safeMessage: "A referenced record does not exist." });
    case "40001":
      return repoError({ ...base, code: "SERIALIZATION_FAILURE", category: "DEPENDENCY",
        transient: true, retryScope: "transaction", alert: false,
        safeMessage: "The request conflicted with another change; retry." });
    case "53300":
      return repoError({ ...base, code: "DB_UNAVAILABLE", category: "DEPENDENCY",
        transient: true, retryScope: "transaction", alert: true,
        safeMessage: "The service is temporarily unavailable." });
    default:
      return repoError({ ...base, code: "INTERNAL", category: "INTERNAL",
        transient: false, retryScope: "none", alert: true,
        safeMessage: "An internal error occurred." });
  }
}
```

```ts
// serialize.ts — the allowlist; cause is structurally unreachable
export function toProblem(e: RepoError) {
  return {
    type: `/problems/${e.code.toLowerCase()}`,
    title: e.code,
    detail: e.safeMessage,
    ...(e.field ? { errors: { field: e.field } } : {}),
  };
}
```

```text
API:   409 {"type":"/problems/conflict","title":"CONFLICT",
            "detail":"That value is already taken.","errors":{"field":"slug"}}
Sentry: {op:"projects.insert", resource:"projects", cause:{code:"23505",
            constraint:"projects_slug_key", sql:"INSERT INTO projects ..."}}
```

## Key data / numbers

- **One** `translate()` function; grep for the driver import — it should appear in one directory.
- Allowlisted response fields: `type`, `title`, `detail`, `errors.field` — four keys.
- `cause` retention: 100%; `cause` serialization: 0%.
- `op`/`resource` cardinality: bounded (`< 200` combinations) so metrics stay usable.
- Redaction list for logs: `password`, `token`, `authorization`, `email`, `DETAIL`.

## Real-world use case — Acme SaaS

Acme's API was clean, but errors were sent to an error tracker with the full exception object.
A constraint `users_email_key` and the duplicate email appeared in the tracker's issue titles,
visible to the whole engineering org and a contractor. Meanwhile, the repository's generic
`RepositoryError` meant the tracker had no `op` or `resource`, so triage required reading stack
traces. Introducing a single `translate()` with an allowlisted serializer and a scrubbed tracker
payload fixed both: the issue title became `CONFLICT projects.insert`, and PII stopped leaving the
service.

## Trade-offs

| Approach | Security | Debuggability | Effort |
| -------- | -------- | ------------- | ------ |
| Return raw error | poor | excellent | none |
| Generic error, log raw | good API, good logs | callers blind | low |
| Translate + preserve `cause` | good | excellent | medium |
| Translate + drop `cause` | good | poor | low |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Centralize translation in one function | Translate in controllers/services too |
| Serialize from an allowlist | `{...err}` into the response |
| Keep `cause` in-process only | Send `cause` to the client or tracker unscrubbed |
| Map constraint → public field | Echo constraint names |
| Test the negative space | Only test happy-path messages |

## Common mistakes

- **`cause` in `toJSON()`** — deep-serializing errors leaks everything.
- **Two translation sites** — classifications drift; fix one and not the other.
- **Constraint allowlist with fallback to the name** — leak by default; omit instead.
- **Scrubbing the API but not Sentry** — the tracker becomes the leak.
- **Dropping `op` to "simplify"** — incidents become a stack-trace archaeology exercise.

## Checklist

- [ ] The driver is imported only in the adapter package.
- [ ] Exactly one `translate()` builds `RepoError`.
- [ ] Serializer uses an allowlist; `cause` is non-serializable.
- [ ] Constraint → field uses an allowlist with an "omit" fallback.
- [ ] Error tracker payloads are scrubbed for PII and SQL.
- [ ] Tests assert no SQLSTATE/constraint/SQL in API output.
- [ ] Tests assert `cause` is present in-process.

## Related

- [Mapping Persistence to Application Errors (24.3, 24.12, 24.13)](../01-concepts/02-mapping-persistence-to-application-errors.md)
- [Error Translation and Normalization (Ch. 16)](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Error Boundaries (Ch. 15)](../../../part-06-boundaries-and-translation/15-error-boundaries/README.md)
- [Sensitive Data and Error Context (Ch. 36)](../../../part-13-security-aware/36-sensitive-data-and-error-context/README.md)
