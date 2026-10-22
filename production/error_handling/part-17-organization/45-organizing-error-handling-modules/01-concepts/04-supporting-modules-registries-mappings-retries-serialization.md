# Supporting Modules: Registries, Mapping, Retry, Recovery, Serialization

> Part XVII · Chapter 45 · Sections 45.7–45.11 · _Estimated reading time: 16 min_
> **Prerequisite:** [The Four Zones](./03-core-zones-primitives-domain-infra-transport.md)

## In one sentence

Five *supporting* module types — **code registry, mapping modules, retry modules, recovery
modules, serialization modules** — hold the cross-cutting policy that must exist exactly once
per concern, and each has a single correct home relative to the four zones.

## Why this matters in production

The four zones tell you where errors are *defined and translated*. They do not, by themselves,
stop the next three classic production defects:

1. **Status drift.** The same code returns `409` from one controller and `400` from another
   because the mapping lives in two places (no registry).
2. **Retry divergence.** ExportJob retries a Stripe call three times with fixed delay; the
   worker retries five times with no jitter; a Stripe incident turns into a retry storm (no
   shared retry module).
3. **Contract drift.** The API returns RFC 9457 problem details, but the job runner writes
   `{error: err.message}` into the DLQ payload — so replay tooling cannot parse failures (no
   serialization module per transport).

Each defect is organizational: the policy exists, but in the wrong number of places (many) or
the wrong place (inline). These five module types pin each policy down to one location.

## Core concept: the five modules and their homes

| Module | What it holds | Home zone | Consumers | Must NOT contain |
| ------ | ------------- | --------- | --------- | ---------------- |
| **Code registry** (45.7) | Code → { httpStatus, retryable, publicTitle, docsAnchor } as **pure data** | Shared data module (imports kernel types only) | Transport handlers, docs generator, client SDK build | Control flow, vendor types, message formatting |
| **Mapping modules** (45.8) | Per-dependency translation tables (`fromPgError`, `fromStripeError`) | Zone 3 — inside each adapter folder | That adapter's callers | Retries, business decisions, serialization |
| **Retry modules** (45.9) | Named retry policies: attempts, backoff, jitter, budget, per-dependency overrides | Shared resilience module (Zone 1/3 boundary) | Job runner, HTTP client wrappers, sagas | Error *classification* (that's the domain/adapter), logging sinks |
| **Recovery modules** (45.10) | Fallback providers and compensation actions (saga undo steps) | Owned by the workflow that needs them (`checkout/saga/compensations.ts`) | The workflow engine / saga runner | Generic retry logic, transport serialization |
| **Serialization modules** (45.11) | Error → external bytes, per transport: RFC 9457 JSON, DLQ payload, webhook response, CLI stderr | Zone 4 — one file per transport | That transport's handler only | Classification, translation, new codes |

```text
   features/*/errors.ts ──(codes)──▶ registry (pure data) ──(metadata)──▶ transport serializers
          ▲                                ▲                                   │
          │ classified as                  │ read by                          ▼
   infra/<vendor>/mapping.ts ──────────────┘                          external contract
          │
          └── wrapped by ──▶ resilience/retry-policies.ts ──▶ used by job runner / HTTP client
                                    │
                                    └──▶ checkout/saga/compensations.ts (workflow-owned recovery)
```

## How it works (mechanics)

**45.7 Registry.** One file (or generated JSON) listing every public code with its metadata.
Because it is pure data, it can be consumed by three very different consumers without coupling:
the HTTP handler (status selection), the docs pipeline (error reference page), and the client
SDK generator (typed error unions). Keep it a `switch`-free `Record<string, Entry>`.

**45.8 Mapping modules.** Live *inside* the adapter folder so they cannot be imported across
dependencies by accident. Export one function per vendor. Attach the vendor payload as `cause`.
Register unknown vendor codes into a stable `*_UNEXPECTED` bucket rather than inventing codes at
runtime.

**45.9 Retry modules.** One named policy per dependency class:
`stripeHttp`, `postgresTx`, `queueJob`, `llmProvider`. Call sites reference the *name*, never
inline numbers. This is where attempts (e.g. 3), base delay (e.g. 200 ms), multiplier (2),
full jitter, and per-hour retry budgets live. The module decides *how* to retry; the classifier
(45.8 + domain semantics) decides *whether* to retry.

**45.10 Recovery modules.** Compensation is business logic and therefore feature-owned: the
refund call that undoes a CaptureStep belongs to Checkout, not to a global "recovery" library.
Group compensations next to the saga steps they undo, with one exported function per step.

**45.11 Serialization modules.** One per transport. The HTTP serializer is the only place that
emits RFC 9457 problem details. The job serializer is the only place that formats the DLQ
failure payload (code, category, attempts, last cause, correlation id). The webhook serializer
maps retryable → non-2xx so the provider's own retry machinery behaves. Shared rule: **serialize
once, at the edge, from registry metadata.**

## Worked example

```ts
// shared/registry/error-codes.ts — PURE DATA. No functions except lookups.
export const REGISTRY = {
  CHECKOUT_CARD_DECLINED:      { httpStatus: 402, retryable: false, publicTitle: "Card declined" },
  PROJECT_SLUG_TAKEN:          { httpStatus: 409, retryable: false, publicTitle: "Slug already in use" },
  EXPORT_ROW_LIMIT_EXCEEDED:   { httpStatus: 422, retryable: false, publicTitle: "Export too large" },
  DEP_STRIPE_UNAVAILABLE:      { httpStatus: 503, retryable: true,  publicTitle: "Payment provider unavailable" },
  DEP_LLM_RATE_LIMITED:        { httpStatus: 503, retryable: true,  publicTitle: "AI provider busy" },
} as const satisfies Record<string, RegistryEntry>;

// shared/resilience/retry-policies.ts — named policies, one home for the numbers.
export const RETRY_POLICIES = {
  stripeHttp:  { attempts: 3, baseDelayMs: 200, multiplier: 2, jitter: "full",
                 retryOn: (e: AppError) => e.retryable },
  postgresTx:  { attempts: 3, baseDelayMs: 50,  multiplier: 2, jitter: "full",
                 retryOn: (e: AppError) => e.code.startsWith("PG_") && e.retryable },
  queueJob:    { attempts: 5, baseDelayMs: 1_000, multiplier: 4, jitter: "full",
                 retryOn: (e: AppError) => e.retryable },   // exhausted → DLQ
  llmProvider: { attempts: 2, baseDelayMs: 1_000, multiplier: 3, jitter: "full",
                 retryOn: (e: AppError) => e.code === "LLM_RATE_LIMITED" },
} as const;

// jobs/serializer.ts — the ONLY writer of DLQ failure payloads.
export function toJobFailure(err: AppError, attempt: number, correlationId: string) {
  return {
    code: err.code, category: err.category, retryable: err.retryable,
    attempt, maxAttempts: RETRY_POLICIES.queueJob.attempts,
    message: err.message, correlationId,
    // cause serialized shallowly & redacted; never the raw stack
  };
}
```

## Key data

- **Registry entry minimum fields:** `httpStatus`, `retryable`, `publicTitle`. Optional:
  `docsAnchor`, `sinceVersion`, `deprecatedSince`.
- **Retry policy defaults worth copying:** attempts 3 for sync calls, 5 for queue jobs; base
  200 ms–1 s; exponential multiplier 2–4; **full jitter** (delay = random(0, base × mult^n));
  provider-instructed `Retry-After` overrides computed delay when present.
- **Compensation naming:** one exported `compensate<StepName>` per saga step; a saga with N
  steps has ≤ N compensation functions — if yours has more, you are compensating partial steps
  (see Chapter 39).
- **Serialization outputs at Acme:** HTTP RFC 9457 (`type`, `title`, `status`, `detail`,
  `instance`, `request-id`), DLQ JSON (code, category, attempt, correlationId), webhook
  (`2xx` only when the event was durably processed; `503` retryable; `400` permanent).

## Real-world use case — Acme SaaS

During a Stripe degradation, Acme's `Checkout` retried captures with inline constants
(`for (let i = 0; i < 5; i++)`) in two services, while `WebhookIngest` retried event
replay with `i < 10`. Stripe's incident generated ~40k Acme-side requests where the published
budget allowed ~8k. The fix was organizational: all three call sites were rewired to
`RETRY_POLICIES.stripeHttp` (3 attempts, full jitter) and the job runner's `queueJob` policy
gained a per-hour retry budget. Peak retry volume during the next Stripe incident fell by ~80%,
and no call site could silently diverge again because the numbers no longer lived at call sites.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Registry as pure data (recommended) | One source for handler/docs/SDK; codegen-friendly | Must be kept in sync with codes (CI check) | Any project with an external contract |
| Metadata on error classes only | No separate file; colocated | Docs and SDK can't consume without instantiating; runtime-only | Tiny internal tools |
| Shared retry module with named policies | Consistent budgets; auditability | One more shared module to version | ≥ 2 call sites per dependency class |
| Per-call-site retry constants | Zero indirection | Divergence → storms | One-off scripts |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the registry free of functions and vendor imports | Put `formatStripeMessage` in the registry |
| Name retry policies and reference them by name | Inline `attempts: 5` at call sites |
| Colocate compensations with their saga steps | Build a global `CompensationService` |
| Serialize per transport in one file | Let each controller invent its error JSON |

## Common mistakes

- **Registry with behavior.** Adding `retryable` *logic* (functions) to the registry makes it
  un-consumable by the docs pipeline and the SDK generator. Data only.
- **Retry module doing classification.** `retryOn` predicates should read metadata, not call
  vendor APIs. If you need vendor knowledge to classify, that belongs in the adapter's mapping.
- **Recovery module swallowing.** A compensation function that catches its own failure and
  returns success converts a partial rollback into silent inconsistency — compensation failures
  must surface to the saga log (Chapter 39).
- **Serialization drift.** Two serializers for the same transport = contract bugs. One file per
  transport, exported through the boundary handler only.

## Checklist

- [ ] Every public code appears in exactly one registry entry.
- [ ] Every retry loop in the repo references a named policy — CI greps for numeric `attempts`.
- [ ] Each dependency adapter exports exactly one translation function.
- [ ] Each saga step has a colocated compensation with a tested failure path.
- [ ] Each transport has exactly one error serializer.

## Related

- [Core Zones: Primitives, Domain, Infra, Transport](./03-core-zones-primitives-domain-infra-transport.md)
- [Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Acme SaaS Error Module Tree](../03-practical-examples/01-acme-error-module-tree.md)
