# The Reusable Core Library

> Part XXI · Chapter 54 · Sections 54.1, 54.2, 54.3, 54.5 · _Estimated reading time: 20 min_
> **Prerequisite:** [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)

## In one sentence

The reusable core is **four things**: an error type, a typed factory, a set of stable
interfaces, and a registry of standard metadata — with no vendor knowledge and no
configuration.

## Why this matters in production

A shared error package earns its place by removing work that *every* service would otherwise
do. That work is narrow and well understood:

1. Representing an error in a way that survives being logged, serialised, and shipped
   across a queue.
2. Classifying it into a small, stable set of categories.
3. Deciding what the outside world sees.
4. Deciding whether it is safe to retry and what the recovery is.

Anything beyond those four is service-specific, and putting it in the shared package makes
every consumer pay for a feature it does not need. The whole design of a good core is
**what it refuses to contain**.

## Core concept

### 54.1 — The reusable core library

The core has exactly four responsibilities, and the boundaries between them are the design:

```text
  ┌──────────────────────────────────────────────────────────────────┐
  │  CORE  (@acme/errors/core)                                       │
  │                                                                  │
  │   1. TYPE      the shape of an error (what it can carry)          │
  │   2. FACTORY   how an error is created (with the right fields)   │
  │   3. INTERFACES  the extension points (mapping, policy, boundary) │
  │   4. REGISTRY  the standard metadata (category → status/retry/…)  │
  │                                                                  │
  │  Knows: categories, codes, contracts, policies.                  │
  │  Does not know: HTTP, queues, Stripe, Postgres, your domain.     │
  └──────────────────────────────────────────────────────────────────┘
```

The **"does not know"** list is the load-bearing part. A core that imports a framework
becomes unusable in a service that uses a different framework, and the framework's upgrade
cycle becomes your upgrade cycle.

### The error type

One type, not a class hierarchy. The type is a **data record** because data is what survives
serialisation, comparison, and code generation.

```ts
export type ErrorCategory =
  | "validation" | "business" | "conflict" | "auth" | "not_found"
  | "external_api_permanent" | "external_api_transient" | "external_api_ambiguous"
  | "database_transient" | "data_integrity" | "dependency_unavailable"
  | "resource_exhausted" | "rate_limit" | "cancellation" | "internal";

export interface AppError {
  readonly kind: "domain" | "dependency" | "internal";
  readonly code: string;              // stable, registered
  readonly category: ErrorCategory;
  readonly message: string;           // internal, safe to log
  readonly publicMessage?: string;    // safe to return to a client
  readonly retryable: boolean;
  readonly cause?: SerializedCause;   // structured, not a raw Error
  readonly context: Readonly<Record<string, unknown>>;   // redacted
  readonly occurredAt: string;        // ISO-8601
  readonly correlationId?: string;
  readonly meta?: Readonly<Record<string, unknown>>;      // non-sensitive extras
}
```

Six properties of this type are deliberate:

- **`cause` is a structured record, not an `Error`.** A serialised cause survives a queue
  boundary. A native `Error` does not, and rehydrating one is where most "we lost the cause"
  bugs live.
- **`context` is redacted at construction.** Redaction is not something a caller can forget
  to do at the boundary, because the boundary never sees the raw value.
- **`retryable` is data, not a policy.** The policy that *uses* it lives in the registry; the
  error just states its nature.
- **`code` and `category` are separate.** The code is specific and public; the category is
  coarse and drives policy. Conflating them is why code tables get 200 rows.
- **`kind`** distinguishes a domain error from an internal bug, which is what the security
  layer needs to decide what may be disclosed.
- **Everything is `readonly`.** An error that mutates after creation is an error whose log
  line and whose response body can disagree.

### 54.2 — Standard interfaces

The core defines **four interfaces**, and they are the entire extension surface. A consumer
implements one of them; the core never needs to know how.

```ts
/** Translates a foreign error into one of ours. */
export interface ErrorMapper<E = unknown> {
  readonly name: string;
  canMap(err: unknown): err is E;
  map(err: E): AppError;
}

/** Answers: is this failure safe to retry, and how? */
export interface RetryPolicy {
  readonly maxAttempts: number;
  readonly baseDelayMs: number;
  readonly maxDelayMs: number;
  readonly jitter: boolean;
  readonly totalDeadlineMs: number;
  readonly honourRetryAfter: boolean;
}

/** Answers: what does the system do about this failure? */
export interface RecoveryPolicy {
  readonly action: "fail" | "retry" | "degrade" | "compensate" | "terminate" | "resolve_later";
  readonly maxAttempts?: number;
  readonly note?: string;
}

/** The boundary contract: turn an error into whatever this transport returns. */
export interface ErrorBoundary<TRequest, TResponse> {
  handle(err: unknown, ctx: BoundaryContext<TRequest>): TResponse;
}
```

The design rule: **interfaces describe *questions*, not *implementations*.** `ErrorMapper`
asks "what is this?"; it does not say how to detect the vendor error. `RetryPolicy` asks
"how many times and how long?"; it does not say how to sleep. That keeps the core free of
side effects, which is what makes it testable and reusable.

### 54.3 — Factory conventions

A factory is not a convenience; it is the **enforcement point** for the core's invariants.

```ts
export function createError<C extends string>(
  code: C,
  message: string,
  opts: {
    category?: ErrorCategory;
    cause?: unknown;
    context?: Record<string, unknown>;
    publicMessage?: string;
    retryable?: boolean;
    kind?: "domain" | "dependency" | "internal";
  } = {},
): AppError {
  const registry = registryEntry(code);
  return {
    kind: opts.kind ?? "domain",
    code,
    category: opts.category ?? registry.category,
    message,
    publicMessage: opts.publicMessage ?? registry.publicMessage,
    retryable: opts.retryable ?? registry.retryable,
    cause: serializeCause(opts.cause),
    context: redact(opts.context ?? {}),
    occurredAt: new Date().toISOString(),
    correlationId: currentCorrelationId(),
    meta: { ...registry.meta, ...opts.meta },
  };
}
```

The factory conventions, in order of importance:

| Convention | Rule | Enforced by |
| ---------- | ---- | ----------- |
| **C1** | The code is looked up in the registry; the registry decides category, retryability, and the public message | runtime lookup + CI check |
| **C2** | The context is redacted inside the factory | always |
| **C3** | The cause is serialised inside the factory | always |
| **C4** | A code not in the registry throws at creation | registry lookup |
| **C5** | Callers may override category only with a documented reason | review + the `meta` field |
| **C6** | The factory never throws for a *known* code, and always throws for an *unknown* one | registry lookup |

C4 is the one that matters most. A code that is not in the registry is a bug at the moment
it is written, not at the moment it is deployed. Failing at creation turns a 3 a.m.
incident into a compile-time-ish error at 2 p.m.

### 54.5 — Standard metadata

Standard metadata is the **shared vocabulary** that makes policies possible without
negotiation. It is a table, and it is the package's most valuable asset.

```ts
export interface RegistryEntry {
  readonly code: string;
  readonly category: ErrorCategory;
  readonly publicMessage: string;
  readonly retryable: boolean;
  readonly httpStatus: number;
  readonly recovery: RecoveryPolicy;
  readonly owner: string;
  readonly since: string;          // the version the code appeared in
  readonly deprecated?: string;    // the version it will be removed in
}
```

The metadata carries five things a service cannot invent for itself:

| Field | Why it is standard |
| ----- | ------------------ |
| `httpStatus` | Two services must not answer the same category differently |
| `retryable` | The starting point for the retry policy; refined by the policy, not the caller |
| `publicMessage` | The user-facing wording, so a wording change is a package change, not 11 |
| `owner` | Who is paged when it fires |
| `since` / `deprecated` | The version history that makes deprecation possible |

And the standard **category table**, which is the package's real contract:

```ts
export const CATEGORY_POLICY: Record<ErrorCategory, {
  httpStatus: number; publicCode: string; recovery: RecoveryPolicy; retryable: boolean;
}> = {
  validation:             { httpStatus: 422, publicCode: "VALIDATION_FAILED",           recovery: { action: "fail" },         retryable: false },
  business:               { httpStatus: 422, publicCode: "BUSINESS_RULE_VIOLATION",   recovery: { action: "fail" },         retryable: false },
  conflict:               { httpStatus: 409, publicCode: "CONFLICT",                 recovery: { action: "fail" },         retryable: false },
  auth:                   { httpStatus: 401, publicCode: "UNAUTHENTICATED",          recovery: { action: "fail" },         retryable: false },
  not_found:              { httpStatus: 404, publicCode: "NOT_FOUND",                recovery: { action: "fail" },         retryable: false },
  external_api_permanent: { httpStatus: 502, publicCode: "PROVIDER_REJECTED",        recovery: { action: "fail" },         retryable: false },
  external_api_transient: { httpStatus: 503, publicCode: "DEPENDENCY_UNAVAILABLE",   recovery: { action: "retry" },        retryable: true },
  external_api_ambiguous: { httpStatus: 202, publicCode: "RESOLUTION_PENDING",       recovery: { action: "resolve_later" }, retryable: false },
  database_transient:     { httpStatus: 503, publicCode: "DATABASE_UNAVAILABLE",     recovery: { action: "retry" },        retryable: true },
  data_integrity:         { httpStatus: 500, publicCode: "INTERNAL_ERROR",           recovery: { action: "terminate" },    retryable: false },
  dependency_unavailable: { httpStatus: 503, publicCode: "DEPENDENCY_UNAVAILABLE",   recovery: { action: "retry" },        retryable: true },
  resource_exhausted:     { httpStatus: 503, publicCode: "RESOURCE_EXHAUSTED",       recovery: { action: "degrade" },      retryable: true },
  rate_limit:             { httpStatus: 429, publicCode: "RATE_LIMITED",             recovery: { action: "fail" },         retryable: true },
  cancellation:           { httpStatus: 499, publicCode: "CLIENT_CLOSED_REQUEST",    recovery: { action: "fail" },         retryable: false },
  internal:               { httpStatus: 500, publicCode: "INTERNAL_ERROR",           recovery: { action: "fail" },         retryable: false },
};
```

**Every category has a status, a public code, a recovery, and a retryability.** There is no
"we'll decide at the boundary", because a boundary that decides is a boundary that
disagrees.

### The package's export surface

A reusable package has a **small** export surface. Every exported symbol is a promise to
every consumer.

| Export | Count | Purpose |
| ------ | ----- | ------- |
| Types (`AppError`, `ErrorCategory`, interfaces) | 8 | The contract |
| `createError` | 1 | The factory |
| `CATEGORY_POLICY` | 1 | The category table |
| `registryEntry`, `isRegistered` | 2 | Registry access |
| `redact`, `serializeCause` | 2 | Safety helpers |
| `withFallback`, `decideRetry` | 2 | Runtime helpers |
| **Total** | **16** | — |

A package with 16 exports is learnable in an afternoon. A package with 60 exports is
learnable in a quarter, which means it is not learned.

## How it works (mechanics)

How a service uses the core, end to end:

```text
  1. Register its domain codes into a registry (its own file, not the package).
  2. Implement an ErrorMapper per vendor.
  3. Use createError() to raise domain errors.
  4. Let the shared HTTP/job adapter translate at the boundary.
  5. Never write a status literal.
```

The service's own registry **extends** the package's, rather than replacing it:

```ts
// src/features/checkout/registry.ts
import { defineRegistry } from "@acme/errors/core";

export const checkoutRegistry = defineRegistry("checkout", {
  CHECKOUT_DUPLICATE_ORDER: { category: "conflict", publicMessage: "Order already exists", owner: "payments" },
  CHECKOUT_CARD_DECLINED:   { category: "external_api_permanent", publicMessage: "Your card was declined", owner: "payments" },
});
```

The service adds **codes**, not **categories**. The categories — and therefore the statuses,
recoveries, and retry policies — stay shared and consistent.

## Worked example

`WebhookIngest` raising a domain error, with the package doing the safety work:

```ts
import { createError } from "@acme/errors/core";

throw createError("WEBHOOK_SIGNATURE_INVALID", "signature mismatch for event evt_123", {
  context: { eventId: "evt_123", signature: receivedSignature, expected: expectedSignature },
});
```

What the package did that the service would not have done:

- **Redacted the context.** `signature` and `expected` are credential material; the factory's
  allowlist dropped both. Without the factory, they would have been logged and shipped to
  the error tracker, and a webhook secret ends up in a third party's log store.
- **Resolved the category.** `WEBHOOK_SIGNATURE_INVALID` is registered as `auth`, so the
  status is `401` and the recovery is `fail` — not `500`.
- **Recorded the version.** `since: "1.2.0"` is in the registry, so a consumer can tell
  whether a code is new.

The result, at the boundary:

```json
{
  "type": "https://acme.internal/problems/auth-error",
  "title": "Unauthenticated",
  "status": 401,
  "detail": "Webhook signature could not be verified.",
  "instance": "/webhooks/stripe",
  "code": "WEBHOOK_SIGNATURE_INVALID",
  "request_id": "req_7f2c"
}
```

No stack trace, no signature, no internal table names.

## Key data / numbers

- **Core responsibilities: 4** (type, factory, interfaces, registry).
- **Standard interfaces: 4** (`ErrorMapper`, `RetryPolicy`, `RecoveryPolicy`, `ErrorBoundary`).
- **Category count: 15**, each with a status, public code, recovery, and retryability.
- **Export surface: 16 symbols** across 8 files. The ceiling for a core package is **25**.
- **Vendor dependencies in the core: 0.** Vendor knowledge lives in adapters only.
- **Configuration points in the core: 0.** A core with configuration is a framework.
- **Categories are never added by consumers.** A consumer that needs a new category proposes
  it in the package, because a new category means a new status and a new policy.
- **Registry lookups happen in the factory**, so an unregistered code throws at creation.
- **Redaction is an allowlist**, not a denylist: unknown context keys are dropped, not
  filtered.
- **Acme's `@acme/errors`: 1,240 lines, 10 modules, 16 exports, 11 consuming services**,
  **0 configuration points**, adopted in **4 days** for the first three services.

## Real-world use case — Acme SaaS, three repositories, one package

Acme's platform team maintained three repositories: the API, the workers, and the billing
service. Each had its own error type, its own mapping code, and its own HTTP adapter. The
consequences were the usual ones, plus one that only appeared at scale: **the same category
produced different status codes in different services**, so a client retrying on `503`
sometimes got a `500` and sometimes a `429`.

The package that replaced them was deliberately small:

| Module | Lines | Contents |
| ------ | ----- | -------- |
| `core/types.ts` | 165 | `AppError`, `ErrorCategory`, interfaces |
| `core/factory.ts` | 115 | `createError`, redaction, cause serialisation |
| `core/registry.ts` | 90 | `defineRegistry`, `registryEntry`, coverage check |
| `core/category-policy.ts` | 65 | `CATEGORY_POLICY` |
| `core/retry.ts` | 95 | `RETRY_POLICIES`, `decideRetry`, `withRetry` |
| `adapters/http.ts` | 160 | RFC 9457 problem-details adapter |
| `adapters/jobs.ts` | 135 | Job failure adapter, DLQ contract |
| `adapters/pg.ts` | 145 | Postgres SQLSTATE mapping |
| `adapters/stripe.ts` | 160 | Stripe error mapping |
| `adapters/llm.ts` | 110 | LLM provider error mapping |
| **Total** | **1,240** | **16 exports** |

The rule that kept it small: **every module is either core (no vendors) or an adapter (one
vendor)**. There is no "utils" module, and there is no shared "helper" module — when a
helper was proposed, it was either promoted to a core interface or pushed into one adapter.

The measurable result after the three repositories migrated:

- Status-code divergences across services: **7 → 0**.
- Time to add a new provider adapter: **3 days** (adapter + registry rows + test), versus
  **11 files / 2 sprints** before.
- New-engineer onboarding to "can add a new error code": from **3 days** to **under 1 hour**.
- Cross-service error-contract drift issues: **0** in the following two quarters.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One shared package, one version | Maximum consistency; simple | Couples release cycles | One team owns the platform |
| One package per domain | Domains evolve independently | Category policies can diverge | Many teams, conflicting release needs |
| Monorepo workspace package | Instant cross-cutting changes | Couples builds; big blast radius | A single deployment unit |
| Copy a template per service | Total isolation | Divergence within two quarters | Services with genuinely different contracts |
| A framework with plugins | Maximum flexibility | Configuration surface; hard to adopt | Rarely; only with a dedicated owner |
| No shared package | No coordination | Full duplication | Services with < 3 copies of any decision |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the core free of vendor and framework imports | Import a Stripe SDK in the core |
| Export a small, stable surface | Export every helper "for convenience" |
| Let services add codes, not categories | Let services define their own category table |
| Redact by allowlist inside the factory | Redact at the boundary where it can be forgotten |
| Fail fast on an unregistered code | Default an unknown code to `internal` silently |
| Keep the error type immutable | Mutate an error after creating it |
| Serialise the cause into a record | Attach a native `Error` and hope it survives |

## Common mistakes

- **The core that imports a framework.** The first consumer on a different framework cannot
  use the package, and the framework's upgrade cycle becomes everyone's.
- **The category per service.** A service that defines its own category table re-creates the
  original divergence problem inside the package.
- **The mutable error.** An error enriched after creation can have a log line and a response
  body that disagree.
- **The serialisation gap.** A native `Error` cause is lost the moment the error crosses a
  queue boundary, and the rehydrated error reads "unknown".
- **The catch-all core.** The moment the core contains an "application errors" section, it is
  an application, not a core.

## Checklist

- [ ] The core imports no vendor SDK and no web framework.
- [ ] The export surface is ≤ 25 symbols.
- [ ] The factory redacts context by allowlist and serialises the cause.
- [ ] Every category has a status, public code, recovery, and retryability.
- [ ] Consumers add codes; categories are proposed to the package.
- [ ] An unregistered code throws at creation time.
- [ ] There are no configuration points in the core.

## Related

- [Mapping Interfaces and Adapters](./02-mapping-interfaces-and-adapters.md)
- [Shared Retry and Recovery Policies](./03-shared-retry-and-recovery-policies.md)
- [The `@acme/errors` Package Skeleton](../03-practical-examples/01-the-acme-errors-package-skeleton.md)
- [Chapter 6 — Designing the Application's Error Model](../../part-03-error-models/06-designing-the-applications-error-model/README.md)
