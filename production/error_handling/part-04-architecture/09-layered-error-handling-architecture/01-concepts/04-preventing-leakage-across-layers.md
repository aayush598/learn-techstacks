# Preventing Leakage Across Layers

> Part IV · Chapter 9 · Sections 9.14–9.15 · _Estimated reading time: 17 min_
> **Prerequisite:** [The Layers of an Error-Handling Architecture](./01-layered-architecture-overview.md)

## In one sentence

**Infrastructure detail must never travel up into the domain**, and **domain meaning must never
be erased by an infrastructure wrapper** — leakage runs in both directions, and both directions
are bugs.

## Why this matters in production

Leaks are silent until they are expensive:

- **Upward leak (infra → domain → user).** A Postgres error text reaches an HTTP body. Besides
  disclosing schema (`relation "tenants_email_key" does not exist`), it makes your API contract
  depend on your database vendor — swap Postgres and clients break.
- **Downward erasure (wrapper destroys meaning).** A repository catches everything and rethrows
  `Error("db error")`. Now the application cannot distinguish a duplicate key (`409`, expected,
  user-fixable) from a connection reset (`503`, transient) — so it either retries everything or
  fails everything. Both are wrong.

Both failures share one root cause: **a layer passed along a representation it was supposed to
own.**

## Core concept — the two leak directions

```text
  UPWARD LEAK (exposure)                 DOWNWARD ERASURE (meaning loss)
  infrastructure ──▶ domain ──▶ API       infrastructure ──▶ repository ──▶ application
  ┌─────────────┐   ┌──────────┐         ┌──────────────┐   ┌───────────────────────┐
  │ SQLSTATE /  │   │ imports  │         │ "error:      │   │ cannot tell duplicate │
  │ vendor SDK  │   │ driver   │         │  connection  │   │ from timeout from     │
  │ exception   │   │ types    │         │  refused"    │   │ not-found             │
  └─────────────┘   └──────────┘         └──────────────┘   └───────────────────────┘
   fix: TRANSLATE at the boundary        fix: TRANSLATE with a typed result, keep cause
```

**Rule A — Nothing crosses upward un-translated.** Driver exceptions, HTTP client errors, cloud
SDK errors, and config errors must be converted to *application* error types at the boundary layer
(repository, integration) before anything above them sees them.

**Rule B — Nothing crosses downward un-named.** Every error leaving a lower layer must carry a
*stable application code* that tells the caller what class of problem occurred — not a stringified
message.

**Rule C — The cause survives both.** Translation is a change of *representation*, not of
*history*. The original driver/SDK error stays attached as `cause` for logs and support; it just
never appears in a public contract.

## How it works — enforcement techniques

Detection is easy to state, hard to keep honest. Use all three layers of defense:

1. **Structural**: domain modules import only from `domain/` and shared primitives. No `pg`,
   `stripe`, `axios`, `express` imports. Dependency direction is one-way.
2. **Mechanical**: an ESLint `no-restricted-imports` rule (or import-boundary linter such as a
   dependency-cruiser rule) fails CI when a domain file imports infrastructure.
3. **Contract**: public responses are produced by one serializer that only accepts the error
   registry — an unregistered code cannot be serialized, so a leak becomes a build/test failure.

```ts
// Repository boundary — the only place SQLSTATE is legal
try {
  await tx.one(sql.insertWorkspace(cmd));
} catch (err) {
  if (isSqlState(err, "23505")) throw new Conflict("WORKSPACE_SLUG_TAKEN", { cause: err });
  if (isSqlState(err, "40001") || isSqlState(err, "40P01"))
    throw new TransientError("WORKSPACE_WRITE_CONFLICT", { cause: err });
  throw new PersistenceError("WORKSPACE_WRITE_FAILED", { cause: err });
}
```

```ts
// Domain file — a grep for forbidden imports must return nothing
// ❌ import { Stripe } from "stripe";        ❌ import pg from "pg";
// ✅ import { DomainError } from "../../core/errors";
export class Workspace {
  rename(to: string) {
    if (to.trim().length === 0) throw new DomainError("WORKSPACE_NAME_EMPTY");
    this.name = to;
  }
}
```

## The mirror test

For every layer crossing, ask two questions:

| Question | If "no" |
| -------- | ------- |
| Does anything above this layer know this layer's *technology*? | Upward leak: translate here |
| Can anything above this layer tell *which* failure this is? | Downward erasure: give it a code |

A wrapper that answers "no" to both has erased the error *and* leaked its internals.

## Key data / numbers

- Postgres codes that must never appear in a response: `23505` (unique), `23503` (FK), `23502`
  (not-null), `40001` (serialization_failure), `40P01` (deadlock_detected), `53300`
  (too_many_connections).
- HTTP statuses an application layer should never invent from a driver message: `500` for
  constraint violations (should be `409`/`422`), `500` for auth config problems (should be
  `503` + alert).
- gRPC canonical codes that *are* vendor-neutral equivalents worth mapping to: `ALREADY_EXISTS`
  (6), `FAILED_PRECONDITION` (9), `UNAVAILABLE` (14), `RESOURCE_EXHAUSTED` (8).
- Disclosed schema errors appear verbatim in driver messages — treat every un-translated driver
  error as an information-disclosure incident in waiting (see Chapter 34).

## Real-world use case — Acme SaaS repository wrapper

Acme's `WorkspaceRepo.get()` wrapped every query:

```ts
// before — meaning erased, leak intact
catch (e) { console.error(e); throw new Error("db error"); }
```

Support could not triage tickets ("db error" told them nothing), and one endpoint *did* leak raw
SQL because a different path re-threw `e.message` directly. The fix:

1. Repository translated to `RECORD_NOT_FOUND`, `WORKSPACE_SLUG_TAKEN`, `DB_UNAVAILABLE`,
   `DB_QUERY_FAILED` — four codes, four policies (`404`, `409`, `503`, `500`).
2. `cause: e` preserved the driver error for logs only.
3. An import-linter rule made `import ... from "pg"` outside `infra/` a CI failure.

Triage time on database tickets dropped from "page the DBA" to a code lookup, and the raw-SQL
leak path disappeared from the codebase.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Translate at every boundary (recommended) | Clean layers, portable, safe | Mapping code per boundary | Any layered service |
| Pass errors through and map at the edge only | Almost no mapping code | Domain/infra entangle; leaks by default | Toy apps |
| Generic wrapper (`Error("failed")`) everywhere | Trivial | Erases classification; forces catch-all policy | Never for production |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Map `SQLSTATE` → application code in the repository | Let `err.message` reach an HTTP response |
| Keep `cause` pointing at the original error | Throw `new Error("something went wrong")` |
| Lint import boundaries in CI | Trust code review alone to catch leaks |
| Give each wrapper failure a distinct code | Collapse every failure into one string |

## Common mistakes

- **Translating in the controller** because "it's fastest" — the domain now depends on HTTP and
  the worker path has no translator.
- **Logging at the wrapper and rethrowing generic** — logs have the cause, callers have nothing;
  classification dies at the wrapper.
- **Sanitizing by deleting the code** — an error with no code is an erasure, not a sanitization.
  Sanitize the *message shown to users*, keep the *code for machines*.

## Checklist

- [ ] `grep` finds no driver/SDK imports outside the infrastructure and integration folders.
- [ ] Every `catch` that rethrows preserves `cause` and sets a stable code.
- [ ] No public response body contains SQL, driver text, hostnames, or vendor error objects.
- [ ] Application code can name every failure it must branch on (no generic "db error").

## Related

- [Where to Handle, Translate, and Propagate](./03-where-to-handle-translate-and-propagate.md)
- [Layer Contracts and Translation Points](../02-deep-dive/01-layer-contracts-and-translation-points.md)
- [Part VI — Error Boundaries and Translation](../../../part-06-boundaries-and-translation/README.md)
- [Part XIII — Security-Aware Error Handling](../../../part-13-security-aware/README.md)
