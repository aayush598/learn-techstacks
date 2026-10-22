# Layer Contracts and Translation Points

> Part IV · Chapter 9 · Sections 9.3–9.8, 9.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [Responsibilities per Layer](../01-concepts/02-responsibilities-per-layer.md)

## In one sentence

Each layer has a **contract**: a fixed set of error representations it accepts, an allowed set it
emits, and **translation points** where one becomes the other — and the contract, not taste, is
what keeps layers from leaking.

## Why this matters in production

Without contracts, "layering" is a folder convention. A controller grows a `catch (e: any)` that
inspects `e.code === "23505"`; a repository starts returning HTTP statuses "to help"; six months
later the domain imports `express`. Contracts turn the architecture from a diagram into something
a linter and a code reviewer can enforce — and they make onboarding finite: a new engineer learns
*what a layer accepts and emits*, not tribal lore.

## Core concept — the in/out contract table

For layers 9.3–9.8, the contract for a request path looks like this:

| Layer | Accepts (in) | Emits (out) | Translation point |
| ----- | ------------ | ----------- | ----------------- |
| **Controller** (9.3) | application/domain errors (`DomainError`, `Conflict`, `NotFound`, `TransientError`) | HTTP status + RFC 9457 body | outcome → status/body map |
| **Application service** (9.4) | domain errors, repository errors, integration errors, `Conflict`, `TransientError` | the same, enriched with operation context; **or** a decided outcome | normalization of mixed sources; retry/compensate verdict |
| **Domain** (9.5) | plain inputs + domain objects | **only** domain errors (`InvalidStateTransition`, `InsufficientFunds`) | none — the domain has zero translation points |
| **Repository** (9.6) | application persistence requests | persistence errors (`RecordNotFound`, `DuplicateKey`, `QueryTimeout`, `DbUnavailable`) | driver exception → persistence error |
| **Infrastructure** (9.7) | driver/SDK calls | raw driver/SDK/OS errors (kept internal, `cause` intact) | OS/driver codes surfaced, never classified |
| **Integration** (9.8) | vendor SDK/HTTP responses | normalized vendor-independent codes (`UPSTREAM_RATE_LIMITED`, `PAYMENT_CARD_DECLINED`) | vendor payload → internal code + recoverability flag |

Two properties make this table work:

- **Narrowing:** each layer emits a *smaller, more stable* vocabulary than it accepts. Drivers have
  hundreds of codes; the application has dozens; the public API has fewer still.
- **Closure:** a layer never emits a representation it also accepts. If the repository both
  accepted and emitted driver errors, callers could never tell translated from raw.

## How it works — declaring contracts in code

TypeScript makes the contract compile-time checkable:

```ts
// core/errors.ts — the vocabulary layers share (Part III owns the shape)
export type AppError =
  | { code: "RECORD_NOT_FOUND";          cause?: unknown }
  | { code: "DUPLICATE_KEY";             key: string; cause?: unknown }
  | { code: "DB_UNAVAILABLE";            retryable: true; cause?: unknown }
  | { code: "UPSTREAM_RATE_LIMITED";      retryAfterSec?: number; cause?: unknown }
  | { code: "PAYMENT_CARD_DECLINED";      declineCode: string }
  | { code: "WORKSPACE_SLUG_TAKEN" }      // domain
  | { code: "TRIAL_NOT_ELIGIBLE" };       // domain

// Repository contract: raw driver errors are not in its signature — by construction
export interface WorkspaceRepo {
  findBySlug(slug: string): Promise<Workspace>;           // throws RECORD_NOT_FOUND
  insert(cmd: NewWorkspace): Promise<Workspace>;          // throws DUPLICATE_KEY / DB_UNAVAILABLE
}
```

Because `WorkspaceRepo` cannot *name* `SequelizeUniqueConstraintError` in its signature, a leak
is a type error. The translation point is visible in exactly one function:

```ts
// infra/postgres/workspace-repo.ts — THE translation point for persistence
async insert(cmd: NewWorkspace): Promise<Workspace> {
  try {
    return mapRow(await this.pool.one(SQL_INSERT, cmd));
  } catch (err) {
    if (isSqlState(err, "23505")) throw { code: "DUPLICATE_KEY", key: "workspaces_slug", cause: err };
    if (isSqlState(err, "40001") || isSqlState(err, "40P01"))
      throw { code: "DB_UNAVAILABLE", retryable: true, cause: err };
    throw { code: "DB_UNAVAILABLE", retryable: true, cause: err }; // connection-class failures
  }
}
```

For integration (9.8) the same shape applies with vendor payloads:

```ts
// integration/stripe.ts — vendor → internal, recoverability decided HERE
export function normalizeStripe(e: Stripe.StripeError): AppError {
  const type = e.type ?? "StripeError";
  if (type === "StripeCardError") return { code: "PAYMENT_CARD_DECLINED", declineCode: e.code ?? "unknown" };
  if (type === "StripeRateLimitError") return { code: "UPSTREAM_RATE_LIMITED", retryAfterSec: 2 };
  if (type === "StripeConnectionError") return { code: "UPSTREAM_UNAVAILABLE", retryable: true, cause: e };
  return { code: "UPSTREAM_ERROR", retryable: false, cause: e };
}
```

## The translation-point inventory

Write these down; they are the only places in the codebase allowed to change an error's shape:

| # | From → To | File location | Owner |
| - | --------- | ------------- | ----- |
| T1 | driver → persistence | `infra/postgres/*-repo.ts` | repository |
| T2 | vendor SDK → internal | `integration/*` | integration |
| T3 | OS/FS/config → operational | `infra/*` | infrastructure |
| T4 | mixed sources → normalized `AppError` | `app/normalize.ts` | application |
| T5 | outcome → HTTP status/body | `http/problem.ts` | controller |
| T6 | outcome → job attempt record | `workers/attempt.ts` | background worker |

Anything outside T1–T6 that constructs or rewrites an error is a candidate duplicate handler —
and code review should treat it as such.

## Key data / numbers

- Controller status map (stable defaults): `RECORD_NOT_FOUND` → `404`, `DUPLICATE_KEY` → `409`,
  `VALIDATION_*` → `422`, `UPSTREAM_RATE_LIMITED` → `429` + `Retry-After`, `DB_UNAVAILABLE` →
  `503` + `Retry-After`, unclassified → `500`.
- Postgres SQLSTATEs legal **only** inside T1: `23505`, `23503`, `23502`, `40001`, `40P01`,
  `53300`, `08xxx` (connection exceptions).
- Vendor error types legal **only** inside T2: Stripe `StripeCardError`,
  `StripeRateLimitError`, `StripeConnectionError`; gRPC transport failures surface as
  `UNAVAILABLE` (14) / `DEADLINE_EXCEEDED` (4).
- A good narrowing budget: driver ~hundreds of codes → application registry ~50–150 codes →
  public subset documented per endpoint (recommendation, grows with API surface).

## Real-world use case — Acme SaaS `Checkout`

An Acme engineer added a "helpful" check in the controller: `if (e.name === "SequelizeTimeoutError")`.
Two failures followed: (1) the queue worker had no such check, so the same timeout was terminal
there; (2) a Sequelize upgrade renamed the class and the controller silently fell through to `500`.
Moving the check into T1 (repository → `DB_UNAVAILABLE`, `retryable: true`) and T5 (controller →
`503` + `Retry-After`) fixed both: one translation point, one class rename impact, worker and HTTP
paths behaved identically.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Typed contracts (shown) | Leaks fail at compile time; inventory obvious | Mapping boilerplate | Medium/large codebases |
| Documented-only contracts | Zero code cost | Rot silently; reviewed only when someone reads docs | Tiny teams, short-lived code |
| Generic `Error` pass-through | No vocabulary to maintain | No classification, no enforcement | Never in production |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| List every translation point (T1–T6) in your architecture doc | Let translation emerge "wherever needed" |
| Keep the domain out of the inventory entirely | Give the domain a status-code mapper |
| Type each layer's emitted error set | Type everything as `unknown`/`any` |
| Preserve `cause` at every translation point | Drop the original when narrowing codes |

## Common mistakes

- **Two translation points for one boundary** — repo *and* middleware both map `23505`; the second
  overwrites the first's code. One boundary, one translator.
- **Contract drift without a test** — add a test per translation point that feeds the raw error in
  and asserts the emitted code and `cause`.
- **Widening the vocabulary to avoid mapping** — adding `RAW_SQL_ERROR` to the shared type is
  surrendering the contract.

## Checklist

- [ ] Every layer has a written accepts/emits row.
- [ ] Translation points T1–T6 exist as named functions with tests.
- [ ] Domain modules reference none of the inventory's "From" representations.
- [ ] `cause` survives every point in the chain (assert it in tests).

## Related

- [Responsibilities per Layer](../01-concepts/02-responsibilities-per-layer.md)
- [Preventing Leakage Across Layers](../01-concepts/04-preventing-leakage-across-layers.md)
- [Part VI — Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Part IX — Repository and Data Access Error Handling](../../../part-09-database-and-transactions/24-repository-and-data-access-error-handling/README.md)
