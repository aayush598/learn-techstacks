# The `@acme/errors` Package Skeleton

> Part XXI · Chapter 54 · Sections 54.1–54.12 (applied) · _Estimated reading time: 24 min_
> **Prerequisite:** [The Reusable Core Library](../01-concepts/01-the-reusable-core-library.md), [Mapping Interfaces and Adapters](../01-concepts/02-mapping-interfaces-and-adapters.md)

## In one sentence

A complete, copy-ready TypeScript package with the **core error type, a typed factory, the
mapping interface, shared retry policies, an HTTP adapter, and a job adapter** — 1,240 lines,
10 modules, 16 exports, zero configuration points.

## Why this matters in production

The skeleton exists so that you do not have to design the package from scratch, and so that
the constraints are visible in the code rather than in a design document. Every module here
is deliberately small, and the boundaries between them are the design.

Read it as an executable specification: the interfaces are the contract, the tables are the
shared decisions, and the adapters are the only place a vendor may appear.

## Core concept

### The package layout

```text
  packages/errors/
    package.json
    src/
      core/
        types.ts            165 lines   the error type + the 4 interfaces
        factory.ts          115 lines   createError + redaction + cause serialisation
        registry.ts          90 lines   defineRegistry + lookup + duplicate guard
        category-policy.ts   65 lines   CATEGORY_POLICY (status, public code, recovery)
        retry.ts             95 lines   RETRY_POLICIES + decideRetry + withRetry
      adapters/
        http.ts             160 lines   toProblemDetails (RFC 9457, framework-free)
        jobs.ts             135 lines   toJobFailure + the DLQ contract
        pg.ts               145 lines   Postgres SQLSTATE mapper
        stripe.ts           160 lines   Stripe error mapper
        llm.ts              110 lines   LLM provider mapper
      index.ts               40 lines   the 16 exports
```

Two rules produce this shape:

- **A module is either core (no vendors, no frameworks) or an adapter (one vendor).** There
  is no `utils` module. A proposed helper is either promoted to a core interface or pushed
  into the adapter that needs it.
- **The core is mostly data.** `types.ts`, `category-policy.ts`, and `registry.ts` are
  interfaces and tables; only `factory.ts` and `retry.ts` contain behaviour, and both
  behaviour blocks are small and total.

## How it works (mechanics)

### Step 1 — The core type

```ts
// src/core/types.ts
export type ErrorCategory =
  | "validation" | "business" | "conflict" | "auth" | "not_found"
  | "external_api_permanent" | "external_api_transient" | "external_api_ambiguous"
  | "database_transient" | "data_integrity" | "dependency_unavailable"
  | "resource_exhausted" | "rate_limit" | "cancellation" | "internal";

export interface SerializedCause {
  readonly name: string; readonly message: string; readonly code?: string;
  readonly stack?: string; readonly at: string; readonly truncated: boolean;
}

export interface AppError {
  readonly kind: "domain" | "dependency" | "internal";
  readonly code: string;                 // stable, registered
  readonly category: ErrorCategory;
  readonly message: string;              // internal, safe to log
  readonly publicMessage?: string;       // safe to return to a client
  readonly retryable: boolean;
  readonly cause?: SerializedCause;      // structured, not a raw Error
  readonly context: Readonly<Record<string, unknown>>;   // redacted
  readonly occurredAt: string;           // ISO-8601
  readonly correlationId?: string;
  readonly meta?: Readonly<Record<string, unknown>>;
}

export interface ErrorMapper<E = unknown> {
  readonly name: string;
  canMap(err: unknown): err is E;
  map(err: E): AppError;
}

export interface RetryPolicy {
  readonly maxAttempts: number; readonly baseDelayMs: number; readonly maxDelayMs: number;
  readonly jitter: boolean; readonly totalDeadlineMs: number; readonly honourRetryAfter: boolean;
}

export interface RecoveryPolicy {
  readonly action: "fail" | "retry" | "degrade" | "compensate" | "terminate" | "resolve_later";
  readonly maxAttempts?: number; readonly note?: string;
}

export interface BoundaryContext {
  readonly operation: string;
  readonly phase: "request" | "job" | "schedule" | "startup";
  readonly correlationId?: string; readonly requestId?: string; readonly instance?: string;
}
```

### Step 2 — The factory

```ts
// src/core/factory.ts
const SAFE_CONTEXT_KEYS = new Set([
  "operation", "resourceType", "resourceId", "tenantId", "userId", "requestId",
  "correlationId", "jobId", "eventId", "provider", "providerCode",
  "attempts", "durationMs", "statusCode", "rowCount", "batchSize",
]);
const SECRET_PATTERN = /(secret|token|password|api[_-]?key|authorization|signature|cookie|session)/i;

export function redact(context: Record<string, unknown> = {}): Record<string, unknown> {
  const out: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(context)) {
    if (SECRET_PATTERN.test(key)) continue;                      // drop by name
    if (!SAFE_CONTEXT_KEYS.has(key)) continue;                   // allowlist
    if (typeof value === "string" && value.length > 200) continue; // drop long strings
    if (value === null || ["string", "number", "boolean"].includes(typeof value)) out[key] = value;
  }
  return out;
}

export function serializeCause(cause: unknown): SerializedCause | undefined {
  if (cause === undefined || cause === null) return undefined;
  const err = cause as { name?: string; message?: string; code?: string; stack?: string };
  return {
    name: err.name ?? "Error", message: err.message ?? String(cause), code: err.code,
    stack: err.stack?.slice(0, 4000), at: new Date().toISOString(),
    truncated: (err.stack?.length ?? 0) > 4000,
  };
}

export function createError(code: string, message: string, opts: {
  kind?: "domain" | "dependency" | "internal"; category?: ErrorCategory; cause?: unknown;
  context?: Record<string, unknown>; publicMessage?: string; retryable?: boolean;
} = {}): AppError {
  const entry = registryEntry(code);              // throws for an unregistered code
  return {
    kind: opts.kind ?? "domain", code, category: opts.category ?? entry.category, message,
    publicMessage: opts.publicMessage ?? entry.publicMessage,
    retryable: opts.retryable ?? entry.retryable,
    cause: serializeCause(opts.cause), context: redact(opts.context ?? {}),
    occurredAt: new Date().toISOString(), correlationId: currentCorrelationId(),
    meta: { ...entry.meta },
  };
}
```

### Step 3 — The registry

```ts
// src/core/registry.ts
export interface RegistryEntry {
  readonly code: string; readonly category: ErrorCategory; readonly publicMessage: string;
  readonly retryable: boolean; readonly owner: string; readonly since: string;
  readonly deprecated?: string;
}

const REGISTRY = new Map<string, RegistryEntry>();

export function defineRegistry(domain: string, entries: Record<string, {
  category: ErrorCategory; publicMessage: string; owner: string; retryable?: boolean; since?: string;
}>, opts: { since?: string } = {}): void {
  for (const [code, def] of Object.entries(entries)) {
    const full = `${domain}.${code}`;             // namespaced: checkout.CARD_DECLINED
    if (REGISTRY.has(full)) throw new Error(`duplicate error code: ${full}`);
    REGISTRY.set(full, { code: full, category: def.category, publicMessage: def.publicMessage,
      retryable: def.retryable ?? false, owner: def.owner, since: def.since ?? opts.since ?? "1.0.0" });
  }
}

export function registryEntry(code: string): RegistryEntry {
  const entry = REGISTRY.get(code);
  if (!entry) throw new Error(`unregistered error code: ${code}`);
  if (entry.deprecated) console.warn(`[errors] deprecated code used: ${code}`);
  return entry;
}
```

Namespacing is what stops two domains claiming the same code; the duplicate guard is what
stops one domain claiming it twice.

### Step 4 — The category policy

```ts
// src/core/category-policy.ts
export const CATEGORY_POLICY: Record<ErrorCategory, {
  httpStatus: number; publicCode: string; recovery: RecoveryPolicy; retryable: boolean;
}> = {
  validation:             { httpStatus: 422, publicCode: "VALIDATION_FAILED",         recovery: { action: "fail" },          retryable: false },
  business:               { httpStatus: 422, publicCode: "BUSINESS_RULE_VIOLATION", recovery: { action: "fail" },          retryable: false },
  conflict:               { httpStatus: 409, publicCode: "CONFLICT",               recovery: { action: "fail" },          retryable: false },
  auth:                   { httpStatus: 401, publicCode: "UNAUTHENTICATED",        recovery: { action: "fail" },          retryable: false },
  not_found:              { httpStatus: 404, publicCode: "NOT_FOUND",              recovery: { action: "fail" },          retryable: false },
  external_api_permanent: { httpStatus: 502, publicCode: "PROVIDER_REJECTED",      recovery: { action: "fail" },          retryable: false },
  external_api_transient: { httpStatus: 503, publicCode: "DEPENDENCY_UNAVAILABLE", recovery: { action: "retry" },         retryable: true },
  external_api_ambiguous: { httpStatus: 202, publicCode: "RESOLUTION_PENDING",     recovery: { action: "resolve_later" }, retryable: false },
  database_transient:     { httpStatus: 503, publicCode: "DATABASE_UNAVAILABLE",   recovery: { action: "retry" },         retryable: true },
  data_integrity:         { httpStatus: 500, publicCode: "INTERNAL_ERROR",         recovery: { action: "terminate" },     retryable: false },
  dependency_unavailable: { httpStatus: 503, publicCode: "DEPENDENCY_UNAVAILABLE", recovery: { action: "degrade" },       retryable: true },
  resource_exhausted:     { httpStatus: 503, publicCode: "RESOURCE_EXHAUSTED",     recovery: { action: "degrade" },       retryable: true },
  rate_limit:             { httpStatus: 429, publicCode: "RATE_LIMITED",           recovery: { action: "fail" },          retryable: true },
  cancellation:           { httpStatus: 499, publicCode: "CLIENT_CLOSED_REQUEST",  recovery: { action: "fail" },          retryable: false },
  internal:               { httpStatus: 500, publicCode: "INTERNAL_ERROR",         recovery: { action: "fail" },          retryable: false },
};
```

`Record<ErrorCategory, ...>` makes the table **total at the type level**: add a category to
the union and this file stops compiling until it has a row.

### Step 5 — A mapping adapter

```ts
// src/adapters/pg.ts
import { createError } from "../core/factory";
import type { ErrorMapper } from "../core/types";

interface PgError { code?: string; message?: string; constraint?: string; }

const PG_CODES: Record<string, { code: string; kind: "dependency" | "internal" }> = {
  "23505": { code: "PG_UNIQUE_VIOLATION",     kind: "dependency" },
  "23503": { code: "PG_FOREIGN_KEY_VIOLATION", kind: "dependency" },
  "23502": { code: "PG_NOT_NULL_VIOLATION",   kind: "internal" },
  "40001": { code: "PG_SERIALIZATION_FAILURE", kind: "dependency" },
  "40P01": { code: "PG_DEADLOCK_DETECTED",    kind: "dependency" },
  "08006": { code: "PG_CONNECTION_FAILURE",   kind: "dependency" },
  "57014": { code: "PG_QUERY_CANCELED",       kind: "dependency" },
};

export const postgresMapper: ErrorMapper<PgError> = {
  name: "postgres",
  canMap(err: unknown): err is PgError {
    return typeof err === "object" && err !== null && "code" in err
      && typeof (err as PgError).code === "string";
  },
  map(err: PgError) {
    const mapped = PG_CODES[err.code ?? ""];
    return createError(mapped?.code ?? "PG_UNEXPECTED", `postgres ${err.code}: ${err.message}`, {
      kind: mapped?.kind ?? "internal", cause: err,
      context: { provider: "postgres", providerCode: err.code, constraint: err.constraint },
    });
  },
};
```

The `23505` (unique violation) case is classified as a **dependency** error with a
domain-agnostic code; the *domain* decides what a duplicate means (a conflict, probably).
That split is the point: the adapter knows the database, the domain knows the business.

### Step 6 — The shared retry policies

```ts
// src/core/retry.ts
export const RETRY_POLICIES: Partial<Record<ErrorCategory, RetryPolicy>> = {
  external_api_transient: { maxAttempts: 3, baseDelayMs: 250, maxDelayMs: 4_000, jitter: true, totalDeadlineMs: 10_000, honourRetryAfter: true },
  database_transient:     { maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1_000, jitter: true, totalDeadlineMs: 5_000,  honourRetryAfter: false },
  dependency_unavailable: { maxAttempts: 2, baseDelayMs: 500, maxDelayMs: 2_000, jitter: true, totalDeadlineMs: 6_000,  honourRetryAfter: true },
  rate_limit:             { maxAttempts: 2, baseDelayMs: 1_000, maxDelayMs: 5_000, jitter: true, totalDeadlineMs: 15_000, honourRetryAfter: true },
};

export function decideRetry(ctx: { category: ErrorCategory; idempotent: boolean; remainingMs: number },
                            policy: RetryPolicy): "retry" | "stop" {
  if (!policy.retryOn.includes(ctx.category)) return "stop";
  if (!ctx.idempotent) return "stop";
  if (ctx.remainingMs <= policy.baseDelayMs) return "stop";
  return "retry";
}

export function backoffDelay(policy: RetryPolicy, attempt: number): number {
  const raw = Math.min(policy.baseDelayMs * 2 ** (attempt - 1), policy.maxDelayMs);
  return policy.jitter ? Math.floor(Math.random() * raw) : raw;   // full jitter
}
```

`retryOn` is the list of categories the policy applies to; the abbreviated `RetryPolicy`
in the concepts file omits it for readability. The executor (`withRetry`) is the only
side-effecting function in the core, and it re-throws the **original** error after the
last attempt so the cause is never lost.

### Step 7 — The HTTP adapter

```ts
// src/adapters/http.ts
export function toProblemDetails(err: unknown, ctx: BoundaryContext,
                                 mappers: readonly ErrorMapper[] = []):
  { status: number; body: ProblemBody } {
  const app = toAppError(err, mappers);
  const policy = CATEGORY_POLICY[app.category];
  return {
    status: policy.httpStatus,
    body: {
      type: `https://acme.internal/problems/${app.category.replace(/_/g, "-")}`,
      title: policy.publicCode,
      status: policy.httpStatus,
      detail: app.publicMessage ?? policy.publicCode,
      instance: ctx.instance,
      code: app.code,
      request_id: ctx.requestId,
    },
  };
}
```

No stack trace, no internal message, no cause chain — by construction, not by discipline.
A framework-specific wrapper (Express, Fastify) is 25 lines and lives beside this file, so
the pure function stays testable without a server.

### Step 8 — The job adapter

```ts
// src/adapters/jobs.ts
export type JobFailureStatus = "failed" | "retryable" | "dead_lettered";

export function toJobFailure(err: unknown, attempts: number, maxAttempts: number,
                              mappers: readonly ErrorMapper[] = []): JobFailure {
  const app = toAppError(err, mappers);
  const recovery = CATEGORY_POLICY[app.category].recovery;

  if (recovery.action === "retry" && attempts < maxAttempts) {
    return { status: "retryable", code: app.code, category: app.category, reason: app.message,
      attempts, maxAttempts, retryAt: new Date(Date.now() + backoffFor(attempts)).toISOString(),
      cause: app.cause && { name: app.cause.name, message: app.cause.message, code: app.cause.code, truncated: app.cause.truncated },
      occurredAt: app.occurredAt };
  }

  return { status: recovery.action === "terminate" ? "dead_lettered" : "failed",
    code: app.code, category: app.category, reason: app.message, attempts, maxAttempts,
    cause: app.cause && { name: app.cause.name, message: app.cause.message, code: app.cause.code, truncated: app.cause.truncated },
    occurredAt: app.occurredAt };
}
```

A job failure is **data with three possible statuses** — a worker can act on it without
knowing anything about the error taxonomy. That is what makes a DLQ replayable.

## Worked example

A service consumes the package in three moves: register its codes, map its vendors, and
hand everything to the boundary.

```ts
// 1. Register the domain's own codes (in the service, not the package)
defineRegistry("checkout", {
  CHECKOUT_DUPLICATE_ORDER: { category: "conflict", publicMessage: "Order already exists", owner: "payments" },
  CHECKOUT_CARD_DECLINED:   { category: "external_api_permanent", publicMessage: "Your card was declined", owner: "payments" },
});

// 2. Map the vendors the service actually uses
const mappers = [postgresMapper, stripeMapper];

// 3. The boundary does the translating
app.use((err, req, res, next) => {
  const { status, body } = toProblemDetails(err, { operation: "checkout", phase: "request", requestId: req.id, instance: req.originalUrl }, mappers);
  res.status(status).json(body);
});
```

The service contributed **12 lines** of wiring and **0 lines** of status logic. A decline
from Stripe, a unique violation from Postgres, and an unknown bug all leave as the same
shape, with the right status for each.

## Key data / numbers

- **Total: 1,240 lines across 10 modules**, with **16 exports** and **0 configuration
  points**.
- **Core: 530 lines** (types 165, factory 115, registry 90, category policy 65, retry 95).
- **Adapters: 710 lines** (http 160, jobs 135, pg 145, stripe 160, llm 110).
- **Categories: 15**, each with a status, public code, recovery, and retryability.
- **Retry policies: 4** categories retried, **11** not; max **3** attempts, max delay
  **4 s**, total deadline **15 s**.
- **Context allowlist: 16 keys**; a secret-named key is dropped even if allowlisted.
- **Cause truncation: 4,000 characters**; a truncated cause is flagged `truncated: true`.
- **Public body fields: 7**; job failure fields: **9** with **3** status values.
- **Package versions:** `@acme/errors@1.0.0` (initial) → `2.0.0` (behaviour change with
  opt-in) → `2.2.0` (current). Consumers: **11**.

## Real-world use case — Acme SaaS, the package that survived a reorganisation

Acme's platform team was dissolved and its error package became unowned. The package had
**11 consumers** and, critically, **no unowned assumptions**: the contract lived in a YAML
file, the per-language registries were generated, and the CI check regenerated them and
failed on a diff.

When the platform team was re-formed **8 months later** and asked "what state is this
package in?", the answers were mechanical:

| Question | Answer | How it was known |
| -------- | ------ | --------------- |
| How many consumers? | 11 | The package's own usage telemetry |
| How many are on the old major? | 3 | The deprecation telemetry |
| Does the contract still match the code? | Yes | The generated-registry CI check (4 s) |
| What is the diff since the last release? | 41 lines | Git |
| What did the last major change? | `rate_limit` attempts 2 → 3 | The changelog and the ADR |

Without those artefacts, the re-formed team would have had to read 11 services to answer
the same questions — a task that would have taken **two weeks** and produced a guess. With
them, it took **an afternoon**.

The package was not popular; it was **maintainable without its authors**, which is the
property that actually matters for shared infrastructure.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One shared package (this design) | One contract; one place to fix | Release coupling; needs an owner | The default |
| Per-service copies | Total isolation | Divergence in days | Never |
| Shared package + service-local overrides | Flexibility | Two places to look | A few services genuinely differ |
| Monorepo workspace package | Instant changes | Coupled builds | A single deployment unit |
| Generated-only package (no code) | No code to maintain | No types; no helpers | A contract-only reuse model |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the core free of vendor and framework imports | Import a provider SDK in the core |
| Throw for an unregistered code | Default an unknown code to `internal` |
| Redact by allowlist | Redact by denylist |
| Preserve the original error after retries | Replace it with "retries exhausted" |
| Version behaviour changes as `MAJOR` | Ship a status change as a `PATCH` |
| Generate per-language registries from one contract | Hand-maintain the same table in three languages |

## Common mistakes

- **The core that imports a framework.** The first consumer on a different framework cannot
  use the package, and the framework's upgrade cycle becomes everyone's.
- **The category per service.** A service that defines its own category table re-creates the
  divergence problem inside the package.
- **The serialisation gap.** A native `Error` cause is lost the moment the error crosses a
  queue boundary, and the rehydrated error reads "unknown".
- **The catch-all core.** The moment the core contains an "application errors" section, it
  is an application, not a core.

## Checklist

- [ ] The core imports no vendor SDK and no web framework.
- [ ] The export surface is ≤ 25 symbols.
- [ ] The category table is total (`Record<Category, Policy>`).
- [ ] The factory redacts by allowlist and truncates the cause.
- [ ] Every adapter declares a timeout, a retry policy, and a fallback.
- [ ] The HTTP adapter contains no stack traces or internal messages.
- [ ] The job adapter produces one of three statuses with a fixed field set.
- [ ] A contract snapshot test exists and is reviewed on every release.

## Related

- [Consuming and Extending the Package](./02-consuming-and-extending-the-package.md)
- [The Reusable Core Library](../01-concepts/01-the-reusable-core-library.md)
- [Reusable API and Job Handling](../01-concepts/04-reusable-api-and-job-handling.md)
- [Versioning Shared Packages Without Breaking Consumers](../02-deep-dive/01-versioning-shared-packages-without-breaking-consumers.md)
