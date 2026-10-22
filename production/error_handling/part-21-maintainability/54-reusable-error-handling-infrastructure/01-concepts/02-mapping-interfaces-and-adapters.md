# Mapping Interfaces and Adapters

> Part XXI · Chapter 54 · Sections 54.4, 54.8, 54.9, 54.10 · _Estimated reading time: 20 min_
> **Prerequisite:** [The Reusable Core Library](./01-the-reusable-core-library.md)

## In one sentence

A **mapping interface** is the one method a vendor adapter implements — and the reason the
core can be reused by a service that has never heard of that vendor.

## Why this matters in production

Every integration brings its own failure vocabulary: HTTP status codes, provider error
strings, SDK exception classes, error codes with five nested levels of sub-code. A codebase
that handles them inline has two problems at once — it cannot reuse the handling, and the
handling leaks into feature code.

The mapping interface fixes both: **the vendor is understood in exactly one file, and the
result of understanding it is one of our categories.** After that, everything downstream
(category → status, category → retry, category → recovery) is shared.

## Core concept

### 54.4 — The mapping interface

The interface is deliberately tiny:

```ts
export interface ErrorMapper<E = unknown> {
  readonly name: string;                       // for logs and diagnostics
  canMap(err: unknown): err is E;              // a type guard
  map(err: E): AppError;                       // translate to ours
}
```

Three members, three jobs:

| Member | Job | Common failure |
| ------ | --- | -------------- |
| `canMap` | Decides "is this error mine?" | Too permissive (`err instanceof Error`) — then every adapter claims every error |
| `map` | Decides "what does it mean?" | Mapping several vendor errors to one category, losing the distinction the caller needs |
| `name` | Decides "who handled it?" | Missing, so logs cannot say which adapter ran |

**`canMap` must be specific.** The rule is: match on the vendor's own discriminator (a
status code, a provider error type, a SQLSTATE), never on the general shape of the error.

```ts
// ❌ Every adapter claims every error.
canMap(err: unknown): err is E { return err instanceof Error; }

// ✅ Claims only this vendor's errors.
canMap(err: unknown): err is StripeError {
  return typeof err === "object" && err !== null && "type" in err && typeof (err as any).type === "string"
    && (err as any).type.startsWith("Stripe");
}
```

### 54.10 — Integration adapters

An **integration adapter** is the only place a vendor is allowed to appear. It has four
parts, and every adapter has all four:

```text
  ADAPTER ANATOMY

    1. DETECT     canMap(): which errors are mine
    2. CLASSIFY   vendor error → our category (+ our code)
    3. CONFIGURE  timeout, retry policy, fallback for this dependency
    4. ENRICH     vendor-safe context (request ids, provider ids, not secrets)
```

The third and fourth parts are the ones teams forget, and they are the reason an adapter is
worth more than a mapping function. An adapter that only translates leaves the timeout, the
retry, and the fallback scattered in the call sites — which is where they drift.

```ts
// adapters/stripe.ts
export const stripeMapper: ErrorMapper<StripeError> = {
  name: "stripe",

  canMap(err: unknown): err is StripeError {
    return typeof err === "object" && err !== null && "type" in err
      && String((err as any).type).startsWith("Stripe");
  },

  map(err: StripeError): AppError {
    const code = STRIPE_CODES[err.type];            // vendor code → our code
    return createError(code, `stripe: ${err.type}`, {
      kind: "dependency",
      cause: err,
      context: { provider: "stripe", providerCode: err.type, providerMessage: err.message },
    });
  },
};

/** The dependency's configuration, owned by the adapter. */
export const stripeDependency = {
  timeoutMs: 8_000,
  retryPolicy: RETRY_POLICIES.external_api_transient,
  fallback: FALLBACKS.external_api_transient,
};
```

`stripeDependency` is what makes the adapter complete. A feature that calls Stripe goes
through the adapter's client, which applies the timeout, the retry, and the fallback. The
feature cannot get them wrong because it cannot see them.

### 54.8 — Standard boundaries

A **boundary** is where an error stops travelling and starts being answered. The core
defines the boundary contract; the transport supplies the shape.

```ts
export interface ErrorBoundary<TRequest, TResponse> {
  handle(err: unknown, ctx: BoundaryContext<TRequest>): TResponse;
}

export interface BoundaryContext<TRequest = unknown> {
  readonly request?: TRequest;
  readonly correlationId?: string;
  readonly operation: string;      // "checkout.create", "export.run"
  readonly phase: "request" | "job" | "schedule" | "startup";
  readonly headersSent?: boolean;
  readonly mappers: readonly ErrorMapper[];   // registered, in priority order
}
```

The standard boundary rules — the same in every service, because they come from the package:

| Rule | Why |
| ---- | --- |
| Boundaries **translate**, they never **re-classify** | One place decides what a category means |
| A boundary **never** logs and rethrows | The outermost boundary logs once |
| A boundary **never** returns a raw `Error` | It returns the contract shape |
| A boundary **always** redacts | Even if the error was already redacted |
| A boundary **never** retries | Retry belongs to the dependency, not the edge |
| A boundary **always** attaches the correlation id | One identifier for one workflow |

### 54.9 — Framework adapters

A **framework adapter** plugs the core into one web framework. The rule that keeps this
sane: the adapter is **thin** and it holds **no policy**.

```ts
// adapters/http-express.ts — a thin adapter over the shared HTTP adapter
export function errorMiddleware() {
  return (err: unknown, req: Request, res: Response, next: NextFunction) => {
    const problem = toProblemDetails(err, {
      operation: `${req.method} ${req.route?.path ?? req.path}`,
      phase: "request",
      correlationId: res.locals.correlationId,
    });
    res.status(problem.status).json(problem.body);
  };
}
```

The adapter contains **no status codes, no categories, and no retry logic**. It converts
"the framework gave me an error" into "the shared adapter turned it into a contract
response". Everything else lives in the shared adapter, so a second framework's adapter is
the same **20 lines**.

The alternative — each framework writing its own handler — produces the divergence the
package was built to remove. Acme's first API used Express and its workers used a different
HTTP client; before the shared adapter, the two produced different bodies for the same
error. After: **one body, two adapters, 20 lines each**.

## How it works (mechanics)

How an error flows through a service that uses the package:

```text
  vendor error
      │
      ▼
  mapper.canMap(err)  ──no──▶ next mapper ──no──▶ internal/unknown handler
      │ yes
      ▼
  mapper.map(err)  →  AppError { code, category, context, cause }
      │
      ▼
  feature code sees OUR error, not the vendor's
      │
      ▼
  boundary: category → status + public code  (CATEGORY_POLICY)
      │
      ▼
  contract response (RFC 9457 body) + one log line
```

The **mapper chain** is important. A service registers several mappers, and the chain
resolves the first match. The order matters, so the registry of mappers is explicit and
ordered by specificity — the most specific vendor first.

```ts
export const mappers: ErrorMapper[] = [stripeMapper, postgresMapper, llmMapper, redisMapper];
```

## Worked example

`AgentRun` calling an LLM provider. The provider's SDK throws three different shapes, and
each used to be handled in the feature:

```ts
// ❌ Before: the feature knew about the provider's exception classes.
try {
  const res = await provider.complete(prompt);
} catch (err) {
  if (err instanceof ProviderRateLimitError) { ... }
  else if (err instanceof ProviderTimeoutError) { ... }
  else if (err.statusCode === 529) { ... }        // overload, vendor-specific
  else throw err;
}
```

```ts
// ✅ After: the feature knows only about our categories.
try {
  const res = await llmClient.complete(prompt);   // the adapter applies timeout + retry
} catch (err) {
  if (categoryOf(err) === "ai_token_limit") {
    return { kind: "tooLong", limit: extractLimit(err) };
  }
  throw err;                                        // unexpected → propagates
}
```

The adapter:

```ts
export const llmMapper: ErrorMapper<LlmProviderError> = {
  name: "llm-provider",
  canMap(err: unknown): err is LlmProviderError {
    return typeof err === "object" && err !== null && "providerCode" in err;
  },
  map(err: LlmProviderError): AppError {
    switch (err.providerCode) {
      case "rate_limit_exceeded":   return createError("LLM_RATE_LIMITED", "provider rate limit", { kind: "dependency", cause: err, context: { provider: err.provider, retryAfterMs: err.retryAfterMs } });
      case "context_length_exceeded": return createError("LLM_TOKEN_LIMIT", "prompt too long", { kind: "dependency", cause: err, context: { provider: err.provider, maxTokens: err.maxTokens } });
      case "overloaded":             return createError("LLM_PROVIDER_OVERLOADED", "provider overloaded", { kind: "dependency", cause: err, context: { provider: err.provider } });
      default:
        return createError("LLM_PROVIDER_ERROR", "provider error", { kind: "dependency", cause: err, context: { provider: err.provider, providerCode: err.providerCode } });
    }
  },
};
```

Note the **`default` arm**: an unrecognised provider error becomes a generic
`LLM_PROVIDER_ERROR` in the `external_api_transient` category, so it is retried and returns
`503` — the safe behaviour for an unknown provider failure, and the behaviour that a
provider can trigger by shipping something new.

The measurable result: `AgentRun`'s feature file lost **31 lines** of provider handling, and
when the provider changed its error shape again (it did, in a later quarter), the fix was
**4 lines in one adapter file** instead of a change in two features.

## Key data / numbers

- **Mapping interface members: 3** (`name`, `canMap`, `map`). More is a design smell.
- **`canMap` rule:** match the vendor's discriminator; never `instanceof Error`.
- **Adapter anatomy: 4 parts** (detect, classify, configure, enrich). An adapter missing
  part 3 or 4 is a mapping function, and the timeout/retry/fallback stay in the call sites.
- **Boundary rules: 6**, all in the package, all identical in every service.
- **Framework adapter size: ~20 lines** per framework, with **zero** policy in it.
- **Mappers per service: 3–6** typical; the chain is ordered by specificity.
- **Vendor dependencies in the core: 0**; vendor dependencies in an adapter: **1**.
- **Unrecognised vendor error → `external_api_transient` → `503` + retry.** The safe default.
- **Acme's adapters:** 5 vendors (Stripe, Postgres, Redis, S3, LLM), **775 lines** total,
  **~155 lines per adapter**.
- **Measured:** `AgentRun` lost **31 lines** of provider handling; a later provider error
  change cost **4 lines in 1 file** instead of **2 features**.

## Real-world use case — Acme SaaS, the provider that changed its errors

Acme's LLM provider changed its error format twice in one year: first from a string field to
a nested `error.code`, then by adding a new `overloaded` case with a `503` status but no
error code at all.

Before the shared package, each change was a **feature-level incident**:

- The first change made `AgentRun` throw a raw provider error, which the boundary mapped to
  `500`. During the afternoon peak, **31%** of summarisation requests returned `500`, and
  the dashboard's summary card showed an error for **~1,400 customer documents**.
- The second change produced a `503` with an empty body, which the provider-specific branch
  did not match, so it fell into the generic handler — a `502`, retried by the client
  **three times** with no backoff, amplifying the load on an already-struggling provider.

After the package, both changes were **adapter-only** edits, and the `default` arm in the
mapper handled the unrecognised shape correctly the first time: it mapped to
`external_api_transient`, returned `503`, and retried with backoff. The dashboard degraded
rather than failed.

The concrete result: the *second* provider change caused **no user-visible error at all**,
because the safe default had already been specified. The first change caused a **4-minute
partial degradation** instead of a 90-minute `500` storm, and the fix was a **one-line**
adapter change.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One adapter per vendor | Clear ownership; no leakage | More files; some vendors barely error | The default |
| One adapter per vendor *type* (all HTTP) | Fewer files | Mixes unrelated vendors; a shared guess | Only when the vendors are interchangeable |
| Translation in feature code | Local; no indirection | Cannot be reused; leaks everywhere | Never, beyond the first two call sites |
| A generic "HTTP mapper" for all HTTP vendors | Very reusable | Loses vendor-specific meaning | Only for the coarse categories (transient/permanent) |
| Vendor error codes published verbatim | No translation needed | Leaks the vendor; breaks when they change | Never |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Match the vendor's own discriminator in `canMap` | Use `instanceof Error` as the test |
| Give every adapter a timeout, a retry policy, and a fallback | Leave the timeout at the call site |
| Map an unknown vendor error to a safe transient category | Let it fall through to `internal` |
| Register mappers in specificity order | Register them in import order and hope |
| Keep framework adapters to ~20 lines | Put status codes in a framework adapter |
| Translate at the boundary only | Translate in the repository and the handler and the job |

## Common mistakes

- **The permissive `canMap`.** Every adapter claims every error, so the first mapper in the
  chain wins and the rest never run.
- **The adapter that only translates.** The timeout and retry stay in the call sites, which
  is where they drift — this is the most common incomplete adapter.
- **The over-broad category.** Mapping "rate limit" and "overloaded" and "bad request" all
  to one category removes the distinction the caller needs to decide whether to retry.
- **Framework adapters with policy.** One framework's adapter grew a `statusMap` and became
  the place every status was decided — the divergence returns, now in a package.
- **Mappers registered by import order.** The order of a `mappers` array is a decision; it
  must be explicit.

## Checklist

- [ ] `canMap` matches a vendor-specific discriminator.
- [ ] Every adapter declares a timeout, a retry policy, and a fallback.
- [ ] An unrecognised vendor error maps to a safe, documented category.
- [ ] The mapper chain is ordered explicitly, most specific first.
- [ ] Framework adapters contain no status codes, categories, or retry logic.
- [ ] The core contains no vendor imports.

## Related

- [The Reusable Core Library](./01-the-reusable-core-library.md)
- [Shared Retry and Recovery Policies](./03-shared-retry-and-recovery-policies.md)
- [Reusable API and Job Handling](./04-reusable-api-and-job-handling.md)
- [The `@acme/errors` Package Skeleton](../03-practical-examples/01-the-acme-errors-package-skeleton.md)
