# Simplifying Conditionals, Translation, and Retries

> Part XXI · Chapter 53 · Sections 53.4, 53.5, 53.6, 53.8 · _Estimated reading time: 19 min_
> **Prerequisite:** [Extracting Policies Without Over-Abstraction](./02-extracting-policies-without-over-abstraction.md)

## In one sentence

Error-handling branches are usually a **decision table that was written as a chain of `if`s** —
and rewriting it as a table removes branches, makes the default explicit, and makes the missing
case visible.

## Why this matters in production

Nested conditionals in error handling are where three of the five production-grade properties
quietly break:

- **Determinism** breaks when the branch order encodes an unstated precedence, so the same error
  takes a different path depending on which check happens to come first.
- **Totality** breaks when there is no explicit default, so an unknown error falls through the
  chain and does whatever the last branch happened to do.
- **Reviewability** breaks when a reviewer must simulate five branches to answer "what does a
  timeout do here?".

In Acme's codebase, error-handling branches averaged **4.6 levels of nesting** and **38 lines**
per site. The branches were not complicated; they were **untabulated**.

## Core concept

### 53.4 — Reducing nested conditionals

The classic shape of an untabulated policy:

```ts
// ❌ Before: precedence hidden in the branch order, no default.
function handle(err: unknown) {
  if (isTimeout(err)) {
    if (isCriticalOperation) {
      return retry(err, 3);
    } else {
      return degrade(err);
    }
  } else if (isAuthError(err)) {
    if (hasRefreshToken) return refresh();
    return unauthorized();
  } else if (isProviderError(err)) {
    if (isPermanent(err)) return fail(err);
    if (hasBudget(err)) return retry(err, 2);
    return degrade(err);
  }
  return unknown(err);   // the default is hiding at the bottom
}
```

The same policy as a table:

```ts
// ✅ After: one lookup, explicit default, exhaustively checkable.
type Handler = (err: AppError) => Outcome;

const HANDLERS: Partial<Record<Category, Handler>> = {
  timeout:             (e) => (e.meta.critical ? retry(e, 3) : degrade(e)),
  auth:                (e) => (e.meta.hasRefreshToken ? refresh() : unauthorized()),
  external_api_permanent: (e) => fail(e),
  external_api_transient: (e) => (hasBudget(e) ? retry(e, 2) : degrade(e)),
};

const UNKNOWN: Handler = (e) => unknown(e);

function handle(err: AppError): Outcome {
  const handler = HANDLERS[err.category] ?? UNKNOWN;
  return handler(err);
}
```

What changed:

| Property | Before | After |
| -------- | ------ | ----- |
| Nesting depth | 4 | 1 |
| Lines | 38 | 12 |
| Default | implicit, at the bottom | explicit, one constant |
| Missing category | falls through silently | resolves to `UNKNOWN` |
| Review question | "simulate the branches" | "read one row" |

The **default is the point**. In a table, "what happens to a category nobody thought about?" is
a single named constant. In a chain, it is "whatever falls off the end", which is how
`unknown` errors end up being treated as `500` in one path and swallowed in another.

### 53.5 — Simplifying translation

Translation is where complexity concentrates, because it is a **function of two variables**: the
incoming error and the outgoing contract. Written as branches, it becomes a cross-product.

```ts
// ❌ Before: a cross-product of provider status and our category.
function toHttp(err: ProviderError): HttpResponse {
  if (err.status === 429) {
    if (err.provider === "stripe") return http(429, "RATE_LIMITED");
    if (err.provider === "openai") return http(429, "AI_RATE_LIMITED");
    return http(429, "RATE_LIMITED");
  }
  if (err.status >= 500) {
    if (err.provider === "stripe") return http(503, "PAYMENT_PROVIDER_UNAVAILABLE");
    if (err.provider === "openai") return http(503, "AI_PROVIDER_UNAVAILABLE");
    return http(503, "DEPENDENCY_UNAVAILABLE");
  }
  ...
}
```

**Normalize first, map second.** Translation is two sequential steps, not one big branch:

```ts
// Step 1: normalize the vendor error into our category. One table per provider.
const STRIPE_CATEGORIES: Record<string, Category> = {
  rate_limit: "external_api_transient",
  api_connection_error: "external_api_transient",
  card_error: "external_api_permanent",
  authentication_error: "external_api_permanent",
};

// Step 2: map our category to our contract. One table for everyone.
const CATEGORY_HTTP: Record<Category, { status: number; code: string }> = {
  external_api_transient: { status: 503, code: "DEPENDENCY_UNAVAILABLE" },
  external_api_permanent: { status: 502, code: "PROVIDER_REJECTED" },
  ...
};
```

Now the provider table is the only thing that changes when a provider changes. The contract
table is the only thing that changes when the API contract changes. **Two tables, one
decision each**, instead of a cross-product of branches.

The rule from Chapter 16 applies with full force here: **never re-export a vendor error
verbatim**, and never let a vendor's status code reach the client untranslated.

### 53.6 — Simplifying retry decisions

Retry decisions have four inputs — is it transient, is it idempotent, how much budget is left,
what does the server say — and they are usually written as four nested branches.

| Question | Where the answer comes from | Shape |
| -------- | --------------------------- | ----- |
| Is it transient? | the error's category | table lookup |
| Is it safe to repeat? | the operation's idempotency | a flag on the operation, not the error |
| How much budget is left? | the caller's deadline | a parameter |
| What did the server say? | `Retry-After` header | an override, bounded by the budget |

The simplification is to make the retry decision a **pure function of a context object**:

```ts
export interface RetryContext {
  readonly category: Category;
  readonly idempotent: boolean;
  readonly remainingMs: number;
  readonly serverHintMs?: number;   // Retry-After
}

export function decideRetry(ctx: RetryContext, policy: RetryPolicy): "retry" | "stop" {
  if (!policy.retryOn.includes(ctx.category)) return "stop";
  if (!ctx.idempotent) return "stop";
  if (ctx.remainingMs <= policy.baseDelayMs) return "stop";
  if (ctx.serverHintMs !== undefined && ctx.serverHintMs > ctx.remainingMs) return "stop";
  return "retry";
}
```

Every branch is now a **named, testable condition**, and the function has no side effects. The
server hint is respected but bounded by the remaining budget — the two rules that prevent
retry storms and honor `Retry-After` at the same time.

### 53.8 — Avoiding inconsistent fallback

Fallback decisions drift because they are usually written at the *call site*, where the context
is available but the policy is not.

| Drift pattern | What happens | Fix |
| ------------- | ------------ | --- |
| One call site degrades, another fails | The same dependency failure produces two different user experiences | Fallback lives in the adapter, not the call site |
| One degrades, another silently continues | The feature returns stale/empty data with no signal | Degrade with a marker, never silently |
| Different timeout values per call site | One call hangs for 30 s, another for 2 s | Timeout is a property of the dependency, not the call |
| One retries, another does not | Traffic doubles on one path | Retry policy is per category, not per call site |
| Fallback chain differs per feature | A shared dependency's outage produces a different shape in each feature | The chain belongs to the adapter |

The general rule: **a fallback is a property of the dependency, not of the caller**. If the
caller chooses the fallback, the caller must know the dependency's failure modes — and it will
know them slightly wrong.

```ts
// ✅ The adapter owns the fallback; the caller cannot get it wrong.
export interface FallbackPolicy<T> {
  readonly on: readonly Category[];
  readonly value: () => T;                 // computed fresh, may throw
  readonly signal: "degraded" | "stale" | "empty";
}

export async function withFallback<T>(
  call: () => Promise<T>,
  fallback: FallbackPolicy<T>,
): Promise<{ value: T; degraded: boolean }> {
  try {
    return { value: await call(), degraded: false };
  } catch (err) {
    if (!fallback.on.includes(categoryOf(err))) throw err;
    return { value: fallback.value(), degraded: true };
  }
}
```

Note the shape: the fallback result **carries a `degraded` flag** rather than pretending to be
a normal success. Silent degradation is a correctness problem, not a feature (Chapter 30).

## How it works (mechanics)

The rewrite, in order:

```text
  1. List the questions the branch chain answers.        → 4 questions
  2. Name each question and find its subject.             → category, operation, budget, server
  3. For each question, write the answer as a table.      → 4 tables
  4. Write the default for each table, conservatively.    → 4 defaults
  5. Replace the chain with lookups.                      → 12 lines
  6. Delete the chain.                                   → -38 lines
  7. Add a test per table asserting the default.          → 4 tests
```

Step 3 is where most of the thinking happens, and where the real bugs surface. Writing the
table forces you to notice that two of your branches were **the same branch with different
spellings** — which was the drift all along.

## Worked example

Acme's `WebhookIngest` had a 46-line branch chain deciding what to do with a Stripe webhook
that failed processing. The chain answered four questions, all in one place, in the wrong
order.

```ts
// ❌ Before (excerpt): 46 lines, 4 nesting levels.
if (err) {
  if (isSignatureError(err)) {
    return res.status(400).json({ error: "bad signature" });
  } else {
    if (isDuplicate(err)) {
      return res.status(200).json({ received: true });   // ack duplicates
    } else {
      if (err.code === "STRIPE_5XX") {
        throw err;                                      // let the queue retry
      } else {
        if (isRateLimited(err)) {
          return res.status(429).json({ error: "slow down" });
        } else {
          if (isProcessingError(err)) {
            return res.status(202).json({ received: true });
          } else {
            return res.status(500).json({ error: "internal" });
          }
        }
      }
    }
  }
}
```

After the rewrite, the same behaviour is expressed as four tables and one dispatcher:

```ts
const WEBHOOK_OUTCOMES: Partial<Record<Category, { status: number; body: unknown }>> = {
  webhook_signature_invalid: { status: 400, body: { code: "WEBHOOK_SIGNATURE_INVALID" } },
  webhook_duplicate:          { status: 200, body: { received: true } },
  external_api_transient:     { status: 202, body: { received: true } },   // queue retries
  rate_limit_exceeded:        { status: 429, body: { code: "RATE_LIMITED" } },
  processing_transient:       { status: 202, body: { received: true } },
};

const WEBHOOK_DEFAULT = { status: 500, body: { code: "INTERNAL_ERROR" } };
```

**Lines: 46 → 18. Nesting: 4 → 0. Decisions: 6 scattered → 6 rows in one table.** The
behaviour is identical, and now a new category is a one-line diff.

## Key data / numbers

- **Target nesting depth in error handling: ≤ 2**; **0** inside policy functions (a lookup is
  not nesting).
- **Target branch count per decision site: ≤ 4.** More than four means the question is really
  two questions.
- **Target lines per decision site: ≤ 20** (before: Acme's average was **38**).
- **Table coverage target: 100%** of categories, with a conservative default row.
- **Retry decision inputs: 4** (category, idempotency, remaining budget, server hint) — a
  fifth input is a sign the policy needs splitting, not the function growing.
- **`Retry-After` bound:** the server hint is honoured only while it fits inside the
  **remaining** budget; otherwise the operation stops.
- **Acme's `WebhookIngest` result:** 46 lines → **18**; error-handling review time for that
  handler fell from **14 min** to **4 min**; the `500` rate for signature failures dropped to
  **0** (it was previously reported as an internal error and paged the team).
- **Fallback rule:** the fallback belongs to the adapter; the caller may only choose between
  *strict* and *degraded* modes, never invent a third.

## Real-world use case — Acme SaaS, the `500` that paged the team every night

Acme's `WebhookIngest` paged the on-call engineer **every night at 03:00 UTC** for six weeks.
The page said "internal error in webhook handler". The cause was not an internal error at all:
Stripe was sending a webhook with a **rotated signing secret** during a key rotation, and the
handler's branch chain mapped signature errors to `500` because the signature branch was
written *after* the "unknown" fallthrough in an earlier version of the file.

The rewrite fixed the immediate bug, but the real fix was structural: **the outcome table
made the default explicit**, so a new category that nobody classified produced
`500` by *design* and was visible in review, while a category that was classified produced its
own status. After the rewrite, a missing classification is a **table row that does not exist**
— detectable by a lint rule that asserts every category in the taxonomy has a row.

The nightly page stopped. The measurable result: **0 pages in the following 11 weeks**, against
**31 in the previous 6**.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Nested branches | Local, no indirection | Hidden precedence, no default, hard to review | Genuinely linear logic with ≤ 3 branches |
| Switch on category | Exhaustive, compiler-checkable | Only works for a single subject | One subject, closed set of cases |
| Table + default | Diffable, total, reviewable | Needs a stable key; functions are less "pure" than a switch | The default choice for policy questions |
| Predicate chain | Handles precedence | Hidden ordering | Precedence genuinely matters and is documented |
| Strategy per subject | Maximum flexibility | Hard to enumerate; hard to document | Behaviour varies per tenant or feature flag |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write the decision as a table first | Nest `if`s and hope the order is right |
| Make the default an explicit named constant | Let the fallthrough be the default |
| Normalize first, map second | Write one branch per (provider, status) pair |
| Keep retry decisions pure and side-effect free | Read the clock and the flags inside the policy |
| Let the adapter own the fallback | Let each call site choose its own fallback |
| Mark degraded results as degraded | Return a fallback that looks like a normal success |

## Common mistakes

- **Table with an implicit default.** A `Record<Category, X>` where the type says every key
  exists but the runtime has holes produces `undefined` downstream instead of a clean default.
- **Over-normalizing.** A single "universal" category for every provider error destroys the
  ability to distinguish a card decline from a token limit.
- **Timeouts as call-site arguments.** The timeout becomes a per-call-site decision, and two
  call sites disagree.
- **Retrying inside a loop and a policy.** Two retry layers multiply; the outer one must be
  visible in the decision function.
- **Fallback that throws.** A fallback that fails must not replace the original error; see
  Chapter 58 for the "error while handling an error" cases.

## Checklist

- [ ] Every error-handling decision site is a table lookup or a ≤ 3-branch switch.
- [ ] Every table has a named, conservative default.
- [ ] The default for an unclassified category is visible in the source.
- [ ] Provider normalisation and contract mapping are two separate steps.
- [ ] Retry decisions are pure functions of a context object.
- [ ] Fallbacks are owned by the adapter and signal that they were used.

## Related

- [Finding and Measuring Repetition](./01-finding-and-measuring-repetition.md)
- [Extracting Policies Without Over-Abstraction](./02-extracting-policies-without-over-abstraction.md)
- [Chapter 16 — Error Translation and Normalization](../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Chapter 27 — Retry Policies](../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 30 — Graceful Degradation and Fallbacks](../../part-11-retry-and-resilience/30-graceful-degradation-and-fallbacks/README.md)
