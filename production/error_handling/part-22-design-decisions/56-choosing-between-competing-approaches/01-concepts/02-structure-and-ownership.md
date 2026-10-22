# Structure and Ownership: Centralized vs Local, Global vs Domain, Generic vs Specific

> Part XXII · Chapter 56 · Sections 56.2, 56.3, 56.9, 56.10, 56.11, 56.12 · _Estimated reading time: 24 min_
> **Prerequisite:** [Chapter 45 — Organizing Error-Handling Modules](../../../part-17-organization/45-organizing-error-handling-modules/README.md)

## In one sentence

**Centralize decisions, localize effects** — the registry, classifier, and policy belong in one
place; the fallback, the user message, and the catch block belong where the failure is
understood.

## Why this matters in production

This group of six subsections is really one question wearing six costumes: *who owns
error-handling decisions?*

Get it wrong and you get one of two classic failures:

- **Duplication drift.** Four layers each classify "timeout" slightly differently. The
  repository says transient, the service says permanent, the HTTP layer says `504`. The
  customer sees `503` sometimes and `500` other times for the same outage, and nobody can
  answer "is this retryable?" without reading code.
- **God-handler drift.** Everything is centralized into one global handler that catches all
  errors, maps them to `500`, and logs them. Now business decisions — "a card decline is not
  an internal error" — are hidden in a file that no feature team owns, and the domain's
  vocabulary is gone.

Both extremes are *locally* reasonable. The resolution is a split: **decisions are shared
facts; effects are local responses.**

## Core concept

### 56.2 — Centralized vs local handling

| | Centralized | Local |
| - | ----------- | ----- |
| Good for | Classification, registry, serialization, retry policy, redaction | Fallbacks, user-facing wording, compensating actions, retry ownership |
| Bad for | Business decisions, per-call context | Duplicated classification, inconsistent codes, redaction logic |
| Test | "Would this policy be identical in every call site?" | "Does this fallback differ from the default?" |

The rule:

> **Centralize a decision if every call site would make it identically. Localize a decision if
> any call site would make it differently.**

- *Is `StripeError` a permanent failure?* → identical everywhere → **centralize**.
- *Should a declined card show "try another card" or "contact support"?* → differs per
  surface → **localize**.

Concretely, this is the difference between a **central error handler** (bad: catches
everything, decides everything) and a **central error registry** (good: data that handlers
read).

```ts
// ❌ Centralized handling that hides business decisions.
app.use((err, req, res, next) => {
  res.status(500).json({ error: "Internal error" });
});

// ✅ Centralized *policy*, localized *effect*.
app.use(errorHandler);   // reads registry; only handles errors with no domain decision

// in the checkout route:
if (!outcome.ok && outcome.error.code === "PAYMENT_CARD_DECLINED") {
  return res.status(402).json(declineMessage(outcome.error));   // local effect
}
```

> ⚠️ **Hazard.** "Centralize everything" produces a handler that cannot be tested without
> standing up the whole application, and a team that cannot test a handler will not trust it.
> Keep the central layer pure (registry, classifier, serializer) so it can be tested in
> isolation.

### 56.3 — Global vs domain error classes

Two different axes hide here:

**Axis 1 — the base type.** Every error in a codebase should share one base so that
`catch (e) { if (e instanceof AppError) ... }` works. That base is *global* (one per
codebase). It carries only universal fields: `code`, `category`, `cause`, `correlationId`,
`safeContext`, `retryable`.

**Axis 2 — the domain types.** `CheckoutError`, `ExportError`, `WebhookError` are *domain
classes* that carry domain vocabulary: which step failed, which plan, which attempt number.

| | Global class only | Domain class only | Global base + domain subclasses |
| - | ----------------- | ----------------- | ------------------------------- |
| Catchable uniformly | Yes | No | Yes (via the base) |
| Expresses domain vocabulary | No | Yes | Yes |
| Cost | One god class | N classes, no common contract | Two layers |
| Use when | Very small codebase | — | **Default** |

```ts
// ✅ Global base: universal metadata only.
export class AppError extends Error {
  readonly code: string;
  readonly category: Category;
  readonly retryable: boolean;
  readonly correlationId: string;
  readonly safeContext: Record<string, string | number>;
  constructor(init: AppErrorInit, options?: { cause?: unknown }) {
    super(init.message, options);
    this.name = new.target.name;
    this.code = init.code;
    this.category = init.category;
    this.retryable = init.retryable;
    this.correlationId = init.correlationId;
    this.safeContext = init.safeContext;
  }
}

// ✅ Domain subclass: domain vocabulary only.
export class CheckoutError extends AppError {
  readonly step: "reserve" | "charge" | "activate";
  readonly providerRequestId?: string;
}
```

The anti-pattern to avoid is a **global class that grows domain fields**: `AppError` with
`planId`, `exportId`, `eventId`, `tenantId`, `agentId`. That is a class nobody can use
correctly and everybody must extend.

### 56.9 — Generic vs specific

"Should this be a generic `IntegrationError` or a specific `StripeCardDeclinedError`?"

**Generic** wins when:
- The caller genuinely treats all instances the same (log and retry a timeout, whatever the
  dependency).
- The specificity would only be used in the adapter and the log.
- You are at the edge of the system and the external contract must be stable.

**Specific** wins when:
- The caller must **branch**: retry the provider outage but not the decline.
- The error maps to a different HTTP status, a different user message, or a different
  compensation.
- Compliance requires distinguishing "card declined" from "insufficient funds".

The default is **specific**, because specificity is what lets a policy table exist. But
specificity has a cost: every specific class is a branch someone must maintain. Rule of
thumb: **be specific until you have three call sites that branch on the same distinction** —
then collapse them into a generic type with a `code` discriminator.

```ts
// ✅ Specific enough to branch, generic enough to not explode:
// one class, a discriminated code, no subclass explosion.
export class PaymentError extends AppError {
  readonly kind:
    | "declined"
    | "insufficient_funds"
    | "provider_unavailable"
    | "authentication_failed";
}
```

### 56.10 — Inheritance vs composition

Inheritance for error types is mostly a legacy pattern. The trade-off:

| | Inheritance | Composition |
| - | ----------- | ----------- |
| Adds a field to all instances | Easy | Easy |
| Adds a *behavior* that varies by type | Easy (override) | Harder (strategy field) |
| Multiple parents | Impossible | Possible |
| Compile-time exhaustiveness | Weak (any subclass) | Strong (union of shapes) |
| Cost of a deep tree | High | Low |

**Recommendation:** use **composition** for data and behavior (a `retryable` field, a
`compensation` strategy), and use **inheritance sparingly** for the one thing it does well —
a base class that lets a global handler treat all errors uniformly.

The deeper problem with inheritance is the **deep hierarchy**: `AppError → TransientError →
DatabaseError → PostgresError → ConstraintViolationError`. It sounds expressive; in practice it
means every `catch` has to know where in the tree to look, and the tree grows a branch per
vendor. Bounded hierarchies are the next subsection.

### 56.11 — Universal vs bounded hierarchy

| | Universal hierarchy | Bounded hierarchy |
| - | -------------------- | ------------------- |
| Shape | One tree for the whole company | One small tree per domain, sharing a base |
| Works when | Error vocabulary is genuinely shared | Domains have distinct vocabularies |
| Failure mode | 200-class god tree; "general" branch for everything | Slight duplication at the base |
| Use when | < ~20 error classes total | **Default** for SaaS** |

The test for "is this vocabulary shared?": **can you write the domain's error sentence without
using the other domain's nouns?** "The export job failed because the plan was not purchasable"
— no. That is a signal the two hierarchies are fused.

```text
  ❌ Universal                     ✅ Bounded
  AppError                        AppError (base: code, category, retryable, cause)
   ├─ ValidationError               ├─ CheckoutError
   ├─ DatabaseError                 ├─ ExportError
   ├─ StripeError                   ├─ WebhookError
   ├─ ExportError                   └─ AgentRunError
   ├─ WebhookError                (each with 3–7 variants, discriminated unions)
   ├─ AgentError
   └─ GeneralError  ← where things go to die
```

### 56.12 — Shared infra vs feature-owned

This is the shared-kernel question from Chapter 45, restated as a decision with a cost.

**Feature-owned** (the default): `features/checkout/errors.ts` owns `CHECKOUT_*`.

**Shared** (`packages/errors-core`): only when **all three** hold:

1. At least **3 independent modules** consume it today — not "will soon".
2. The concept is **product-neutral** — no product codes, no vendor types, no business nouns.
3. A new engineer can use it **without learning Acme's domain** (Chapter 45's promotion
   checklist).

The failure mode of premature sharing is worse than duplication: a shared package that
encodes one team's assumption becomes everyone else's constraint, and the first team to
disagree forks it. The failure mode of never sharing is duplicated code — annoying but local,
and cheap to fix later. **Prefer the fixable failure.**

## How it works (mechanics)

### A layering that satisfies all six decisions

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │ Transport (HTTP / job / webhook)                                │
  │   - catches ONCE per request                                     │
  │   - owns the external contract (status, headers, body)          │
  │   - owns LOCAL fallbacks (degrade the widget, ack the event)     │
  ├───────────────────────────────────────────────────────────────────┤
  │ Application / domain                                            │
  │   - returns closed outcome types                                │
  │   - owns domain error classes (CheckoutError, ExportError)      │
  │   - owns compensation decisions                                  │
  ├───────────────────────────────────────────────────────────────────┤
  │ Adapters (Postgres, Stripe, S3, LLM)                            │
  │   - translate vendor errors -> domain errors (preserve cause)   │
  │   - own vendor retry/timeout/breaker configuration               │
  │   - never decide user-facing outcomes                            │
  ├───────────────────────────────────────────────────────────────────┤
  │ Shared kernel (errors-core)                                     │
  │   - AppError base, Result type, guards, redaction, classification│
  │   - registry data (code -> status, retryable, title)            │
  │   - NO product codes                                             │
  └───────────────────────────────────────────────────────────────────┘
```

Read the six decisions against this diagram:

| Decision | Where it lands |
| -------- | -------------- |
| 56.2 centralized vs local | Policy in kernel/registry; fallback in transport |
| 56.3 global vs domain | `AppError` in kernel; `CheckoutError` in the feature |
| 56.9 generic vs specific | One class per domain, discriminated `code` |
| 56.10 inheritance vs composition | Inheritance for the base only; composition for behavior |
| 56.11 universal vs bounded | Bounded: kernel base + one small tree per domain |
| 56.12 shared vs feature | Kernel shared (neutral); codes feature-owned |

## Worked example — `Acme SaaS` (multi-tenant)

Acme started with one file, `src/errors.ts`, containing 31 classes for payments, exports,
webhooks, and the agent. Symptoms appeared within a quarter:

1. `AcmeError` had 14 optional fields — `planId?`, `exportId?`, `eventId?`, `agentId?` —
   because it was serving as both base and domain type.
2. Three layers each had a `catch` that mapped `err.code` to a status, and they disagreed:
   the repository mapped `DB_UNIQUE_VIOLATION` to `409`, the service to `500`, the controller
   to `409` again.
3. A new feature team needed to add one error and discovered that `src/errors.ts` was owned by
   a different team, so they added `src/errors2.ts`.

The refactor (three steps, two weeks):

**Step 1 — split the base from the domain types.** Move the universal fields into
`packages/errors-core` (`AppError`, `Category`, `Result`, `classify`). Delete the 14 optional
fields.

**Step 2 — move domain errors to their features.** `features/checkout/errors.ts` holds
`CheckoutError`; `features/export/errors.ts` holds `ExportError`. Each has 3–6 variants
expressed as a discriminated union, not a subclass tree.

**Step 3 — centralize the decisions, not the handling.** One registry maps every code to
`{ httpStatus, retryable, publicTitle, category }`. The repository and the controller now both
read it, so the disagreement is structurally impossible.

The measurable result: adding a new error code now touches **two** files (the feature's
`errors.ts` and the registry entry) instead of three layers that each had to agree, and the
number of catch blocks dropped from 63 to 19 — the remaining ones are genuine recovery
points, not classification.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Domain error classes per feature | 1 (with 3–7 variants) | More than one class per feature usually means a missing union |
| Error hierarchy depth | ≤ 2 (`AppError` → feature class) | Depth 3+ is the point where `catch` order starts mattering |
| Max error classes per feature | 8 | Past this, the feature has two sub-domains |
| Shared-kernel promotion threshold | 3 real consumers | Counted from production imports, not from intent |
| Max codes in a single registry file | 300 | Past this, split per domain and keep an index |
| `catch` blocks per service | Aim < 25 | Above 50, most are classification, not recovery |
| Central handler line budget | ~150 lines | Beyond that it is a god module (Chapter 45) |
| Variants per discriminated union | 3–7 | Above 7, split into "known" and "unknown" unions |

## Real-world use case — `AgentRun` (Acme SaaS)

The `AgentRun` feature runs an LLM tool-calling loop. Its errors are unlike anything else in
Acme:

- The provider returns `429 Too Many Requests` with a `Retry-After` header.
- The model returns output that fails the tool-call schema.
- A tool times out.

If `AgentRun` had used the shared global error class with a generic
`IntegrationError`, the retry policy could not be expressed: "retry the provider rate limit,
but never retry the schema violation" requires distinguishing them.

With a bounded hierarchy (`AgentRunError` in `features/agent/errors.ts`), the variants are
explicit:

```ts
export type AgentRunError =
  | { code: "AGENT_PROVIDER_RATE_LIMITED"; retryable: true; retryAfterSeconds: number }
  | { code: "AGENT_OUTPUT_SCHEMA_INVALID"; retryable: false; toolName: string }
  | { code: "AGENT_TOOL_TIMEOUT"; retryable: true; toolName: string }
  | { code: "AGENT_TOKEN_LIMIT_EXCEEDED"; retryable: false; used: number; limit: number };
```

Note that this is **not** an `AgentRunError` class hierarchy — it is a union. The retry policy
is then a lookup, not a chain of `instanceof` checks, and the transport maps
`AGENT_PROVIDER_RATE_LIMITED` to `429` with the provider's `Retry-After` propagated verbatim
(Chapter 19, §19.12).

The payoff showed up during a provider incident: only `AGENT_PROVIDER_RATE_LIMITED` and
`AGENT_TOOL_TIMEOUT` were retried, so the run consumed exactly the traffic the provider said
it could accept, and the other failure classes failed fast instead of hammering the provider
into a longer outage.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Fully centralized handler | One place to change | Hides business decisions; hard to test | Very small systems only |
| Fully local handling | Full context | Divergent classification; duplicated logic | Never as a policy |
| Central policy + local effect | Consistent, contextual | Needs discipline and a written rule | **Default** |
| One global error class | Simple | Becomes a god class with optional fields | < ~20 error classes |
| Per-feature hierarchies | Clear vocabulary | Slight duplication of the base | **Default** |
| Deep inheritance | Expressive | Unmaintainable; weak exhaustiveness | Avoid |
| Discriminated unions | Compiler-checked | Verbose; needs `assertNever` | Domain layers |
| Premature shared kernel | DRY | Locks in one team's assumptions | Avoid |
| Shared kernel after 3 consumers | DRY without lock-in | Needs versioning discipline | Once the threshold is met |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Centralize classification, registry, and redaction | Centralize business decisions and user messages |
| Keep one base class with **universal fields only** | Add domain fields to the global class |
| Express variants as a **discriminated union** | Build a 5-level exception tree |
| Keep the hierarchy **2 levels deep** | Rely on `catch` ordering in a deep tree |
| Own codes in the feature that can explain them | Put `CHECKOUT_*` codes in the shared kernel |
| Promote to shared at **3 real consumers** | Extract on first use "for consistency" |
| Test the central layer as a pure function | Require the whole app to test a handler |

## Common mistakes

- **One `catch` at the top of the request.** It is fast to write and it destroys the
  information that the failure needed. The top-level handler should be the *last* resort, not
  the *only* handler.
- **The god base class.** `AppError` with 14 optional fields is a class that every caller must
  interrogate, and whose fields are all `undefined` most of the time.
- **Duplicating classification per layer.** The disagreement between repository and controller
  is the direct cause of "same outage, different status code" support tickets.
- **Sharing the package before the concept exists.** Two teams need a *different* concept and
  you ship one shared version that is wrong for both.
- **Using `instanceof` chains for exhaustive handling.** `if (e instanceof A) ... else if (e
  instanceof B) ...` silently accepts a new type. Use `assertNever` on a union instead.

## Checklist

- [ ] The central layer contains **policy**, not business decisions.
- [ ] Every error class inherits from exactly one base carrying only universal fields.
- [ ] The hierarchy is at most 2 levels deep per domain.
- [ ] Domain error variants are expressed as a discriminated union with `assertNever`.
- [ ] Every code is owned by the feature that can explain it.
- [ ] Shared-kernel code has **no** product codes and **no** vendor types.
- [ ] Each shared abstraction has 3+ real consumers, counted from production imports.
- [ ] The registry is the single source of truth for status, retryability, and public title.

## Related

- [Control-Flow Shape (56.1, 56.7, 56.14)](./01-control-flow-shape.md)
- [Fidelity and Risk (56.8, 56.13, 56.17, 56.18)](./04-fidelity-and-risk.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../../part-17-organization/45-organizing-error-handling-modules/README.md)
- [Chapter 10 — Centralized and Distributed Error Handling](../../../part-04-architecture/10-centralized-and-distributed-error-handling/README.md)
