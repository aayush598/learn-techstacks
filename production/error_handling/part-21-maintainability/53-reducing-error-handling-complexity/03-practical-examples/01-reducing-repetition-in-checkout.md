# Reducing Repetition in the Checkout Flow

> Part XXI · Chapter 53 · Sections 53.1, 53.5, 53.6, 53.7 · _Estimated reading time: 24 min_
> **Prerequisite:** [Finding and Measuring Repetition](../01-concepts/01-finding-and-measuring-repetition.md), [Simplifying Conditionals, Translation, and Retries](../01-concepts/03-simplifying-conditionals-translation-and-retries.md)

## In one sentence

Checkout's four duplicated mapping blocks became **one registry, one status table, one retry
table** — and the flow's error surface shrank from **11 decision sites to 4** in one
afternoon.

## Why this matters in production

Checkout is where duplication is most expensive, because it is the flow with the most
decision types *and* the most consumers: an HTTP handler, a receipt job, a webhook consumer,
and a reconciliation job. Four consumers, each with its own copy of "what does a card
decline mean", is four chances to disagree — and the disagreement surfaces as a wrong status
code, a wrong retry decision, or a duplicate charge.

The measurement below is the actual one Acme ran. It is included in full because the
*measurement* is the lesson; the refactor is routine once the measurement exists.

## Core concept

### Step 1 — The duplication report

The question chosen was: **"what does a failure mean, and what do we do about it?"** — a
question with four decision sites in Checkout.

```text
DECISION                     COPIES  LOC       DRIFT OBSERVED
postgres unique → conflict      3    18 LOC   yes (409 / 400 / 500)
provider 429 → retry            2    12 LOC   yes (one honours Retry-After)
provider 4xx → permanent        2    10 LOC   no
timeout → retry vs fail         2     9 LOC   yes (job retries, request fails)
http status by category         2    14 LOC   yes (500 for declines)
retry attempts by category      2     8 LOC   no
─────────────────────────────────────────────────────────────
TOTAL                          13    71 LOC   4 divergences
```

**Thirteen decision sites, four of them diverged.** Two of the divergences were costing
money and users, so the refactor was prioritised there first.

### Step 2 — The three duplicated blocks, before

```ts
// ── Block 1: the repository ───────────────────────────────────────────
async function insertOrder(order: Order): Promise<void> {
  try {
    await db.insert("orders", order);
  } catch (err) {
    if (isPg(err) && err.code === "23505") {
      throw new ConflictError("duplicate order", { code: "CHECKOUT_DUPLICATE" });
    }
    if (isPg(err) && err.code === "23503") {
      throw new BusinessError("tenant not found", { code: "CHECKOUT_TENANT_UNKNOWN" });
    }
    throw err;                       // everything else escapes raw
  }
}

// ── Block 2: the HTTP handler ─────────────────────────────────────────
try {
  const order = await service.createOrder(req.body);
  res.status(201).json(order);
} catch (err) {
  if (err instanceof ConflictError) {
    res.status(409).json({ code: "CHECKOUT_DUPLICATE", message: "Order already exists" });
  } else if (err instanceof BusinessError) {
    res.status(422).json({ code: err.code, message: err.message });
  } else if (err instanceof GatewayError) {
    res.status(402).json({ code: "CHECKOUT_CARD_DECLINED", message: "Card declined" });
  } else {
    res.status(500).json({ code: "INTERNAL", message: "Something went wrong" });
  }
}

// ── Block 3: the receipt job ──────────────────────────────────────────
try {
  await sendReceipt(order);
} catch (err) {
  if (err.code === "429") {
    await sleep(1000);
    await sendReceipt(order);        // one retry, hard-coded, no jitter
  } else if (err.code === "500") {
    await queue.add("receipt", { orderId });   // defer to the queue
  } else {
    throw err;
  }
}

// ── Block 4: the reconciliation job ───────────────────────────────────
catch (err) {
  if (err.status === 429) {
    await sleep(60_000);             // 60 seconds, no cap
    await reconcile();
  }
  if (err.status >= 500) {
    await sleep(500);
    await reconcile();
  }
}
```

### Step 3 — The three duplicated blocks, after

**One registry** — the codes and their categories, in the Checkout domain module:

```ts
// src/features/checkout/errors.ts
export const CHECKOUT_CODES = {
  CHECKOUT_DUPLICATE_ORDER: "conflict",
  CHECKOUT_TENANT_UNKNOWN: "business",
  CHECKOUT_CARD_DECLINED: "external_api_permanent",
  CHECKOUT_PROVIDER_RATE_LIMITED: "external_api_transient",
  CHECKOUT_PROVIDER_UNAVAILABLE: "external_api_transient",
  CHECKOUT_AMOUNT_MISMATCH: "validation",
} as const satisfies Record<string, Category>;

export type CheckoutCode = keyof typeof CHECKOUT_CODES;
```

**One status table** — shared by every Checkout consumer, keyed by category:

```ts
// src/platform/errors/http-mapping.ts
export const CATEGORY_HTTP: Record<Category, { status: number; publicCode: string }> = {
  validation:             { status: 422, publicCode: "VALIDATION_FAILED" },
  business:               { status: 422, publicCode: "BUSINESS_RULE_VIOLATION" },
  conflict:               { status: 409, publicCode: "CONFLICT" },
  external_api_permanent: { status: 402, publicCode: "PROVIDER_REJECTED" },
  external_api_transient: { status: 503, publicCode: "DEPENDENCY_UNAVAILABLE" },
  database_transient:     { status: 503, publicCode: "DATABASE_UNAVAILABLE" },
  internal:               { status: 500, publicCode: "INTERNAL_ERROR" },
};
```

**One retry table** — keyed by category, with a deadline and a server-hint rule:

```ts
export const RETRY_POLICIES: Partial<Record<Category, RetryPolicy>> = {
  external_api_transient: { maxAttempts: 3, baseDelayMs: 250, maxDelayMs: 4_000, jitter: true, totalDeadlineMs: 10_000, honourRetryAfter: true },
  database_transient:     { maxAttempts: 3, baseDelayMs: 100, maxDelayMs: 1_000, jitter: true, totalDeadlineMs: 5_000, honourRetryAfter: false },
};

export const NO_RETRY: RetryPolicy = { maxAttempts: 1, baseDelayMs: 0, maxDelayMs: 0, jitter: false, totalDeadlineMs: 0, honourRetryAfter: false };
```

**One fallback helper** — used by the jobs, so the interactive request and the background job
share the policy while differing only in the *context* they pass:

```ts
// src/platform/errors/fallback.ts
export async function withFallback<T>(
  call: () => Promise<T>,
  ctx: FallbackContext<T>,
): Promise<{ value: T; degraded: boolean }> {
  try {
    return { value: await call(), degraded: false };
  } catch (err) {
    const category = categoryOf(err);
    if (category !== "external_api_transient" && category !== "external_api_permanent") throw err;
    return { value: ctx.fallbackValue(), degraded: true };
  }
}
```

### Step 4 — The consumers, after

```ts
// HTTP handler — no status literal, no category knowledge.
try {
  const order = await service.createOrder(req.body);
  res.status(201).json(order);
} catch (err) {
  const appErr = toAppError(err);
  res.status(statusFor(appErr.category)).json(problemFor(appErr));
}

// Receipt job — one policy, no hard-coded sleep.
const result = await withFallback(() => sendReceipt(order), { fallbackValue: () => undefined });
if (result.degraded) await queue.add("receipt", { orderId: order.id, deferred: true });

// Reconciliation job — bounded, jittered, deadline-limited.
await retry(() => reconcile(), RETRY_POLICIES.external_api_transient!);
```

**Lines: 4 blocks (71 LOC) → 3 tables + 1 helper (38 LOC). Decision sites: 13 → 4.**

## How it works (mechanics)

The migration was run in a specific order, and the order is the reusable part:

```text
  Day 1, step 1   Add the registry, the status table, the retry table. Nothing calls them.
  Day 1, step 2   Add the exhaustiveness lint rule. It reports on the NEW tables only.
  Day 1, step 3   Migrate the repository (the layer that owns Postgres). Delete its branches.
  Day 1, step 4   Migrate the HTTP handler. Delete its branches.
  Day 2, step 5   Migrate the receipt job and the reconciliation job. Delete their branches.
  Day 2, step 6   Turn the lint rule up: no status literal outside http-mapping.ts, anywhere.
  Day 2, step 7   Add a registry-coverage test: every code emitted in the codebase has a row.
```

Two details made the difference:

- **Step 3 before step 4.** The repository owns the Postgres mapping, so it is the natural
  owner of the normalisation. Migrating it first means the HTTP handler never has to know
  about `23505`.
- **Step 6 after step 5.** Turning the lint rule on globally before the migration finishes
  blocks everyone. Turning it on after means the rule has no exceptions to negotiate.

## Worked example

The measurable outcome of the Checkout refactor, over the **8 weeks** after it landed:

| Metric | Before | After |
| ------ | ------ | ----- |
| Decision sites in Checkout | 13 | **4** |
| Status codes produced by the same failure | 4 (`402/409/422/500`) | **1** (`402` for declines) |
| Error-handling lines in the feature | 71 | **38** |
| Files touched to add a new Checkout code | 5 | **2** |
| Review time, error-handling PRs | 22 min | **8 min** |
| Pages from Checkout | 6/month | **0** |
| Duplicate charges caused by a retry storm | 1/quarter | **0** |

The two divergences that were costing money:

1. **The card decline mapped to `500`** in one of the four blocks. Every declined card
   produced an internal-error alert. Acme's on-call rota received **6 pages/month**, and the
   customer saw "Something went wrong" instead of "Your card was declined". After the
   refactor: `402` with a stable public code, **0 pages**.
2. **The reconciliation job's uncapped 60-second sleep.** During a provider rate limit, the
   job slept 60 s, woke, called again, got rate-limited, and slept again — with no attempt
   cap and no jitter. Across 24 reconciliation workers, this produced a **2.1× request
   amplification** at the provider and extended a 4-minute rate-limit window into a
   **38-minute** one. The retry table's `maxAttempts: 3` and jitter removed the amplification.

## Key data / numbers

- **Decision sites in Checkout: 13 → 4**; error-handling lines **71 → 38**.
- **Statuses produced by one failure: 4 → 1.**
- **Change cost of a new Checkout code: 5 files → 2 files** (domain registry + test).
- **Refactor effort: 1.5 days** (two engineers, one of them unfamiliar with the code).
- **Review time: 22 min → 8 min** per error-handling PR (40 PRs).
- **Pages: 6/month → 0.**
- **Retry amplification removed: 2.1× → 1.0×** (bounded attempts + jitter).
- **Provider rate-limit window: 38 min → 4 min** (the original window).
- **Table sizes:** 6 Checkout codes, 7 categories in the HTTP table, 2 categories in the
  retry table.
- **Exhaustiveness check:** `satisfies Record<string, Category>` makes an unclassified code a
  compile error; the lint rule makes a stray status literal a build failure.

## Real-world use case — Acme SaaS, the Checkout that paged the on-call every Friday

Every Friday afternoon, between 14:00 and 16:00, Acme's Checkout produced a burst of `500`s
and paged the on-call engineer. The burst was not random: Friday is when Acme's enterprise
customers ran their month-end billing batch, and the batch triggered a high rate of card
declines.

The on-call engineer could never reproduce it, because the declining path was fine in the
service and broken in the **HTTP handler** — the handler had been extended during a previous
refactor to add a new error branch, and the new branch was inserted **above** the decline
branch, so a `GatewayError` was caught by the generic `500` arm. The decline branch below it
was unreachable.

This is the most expensive form of duplication: the correct answer existed, twice, and the
copy that ran was the wrong one.

The refactor in this file removed the possibility entirely, because the branch order no
longer existed — the handler asks `statusFor(appErr.category)`, and the category is decided
once, at the layer that owns the meaning. There is no ordering to get wrong.

Result: Friday pages went from **6/month to 0**, and the on-call rota no longer has a
Friday duty. The team added one rule to their review checklist: **"if you add an error
branch, you have added a decision site — is this the only place that answers this question?"**

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| One shared registry for the whole service | Maximum consistency | Every team blocked on one file | Small teams; ≤ 30 codes |
| Registry per domain + shared category tables | Domains stay independent; scales | Two-level lookup | Most services; Acme's choice |
| One table per consumer (HTTP, job, webhook) | Each consumer is self-contained | The same decision in three tables — the original problem | Never, for the same question |
| Keep the branches, add a test | Cheapest | The order-dependence bug remains possible | Temporary; with a follow-up date |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Measure before refactoring | Refactor the file that "looks worst" |
| Migrate the owning layer first | Migrate the outermost layer first |
| Delete the old branches in the same PR | Keep them "in case" |
| Turn on the lint rule after the migration | Block the team on day one |
| Make the table exhaustive | Leave holes and rely on a `default` for known categories |
| Ask "is this the only place that answers this?" | Add a branch because the existing one does not fit |

## Common mistakes

- **Migrating the HTTP layer first.** The handler then needs to know about `23505`, and the
  repository keeps its branch — you end up with both.
- **Unifying the status codes by fiat.** Merging `422` and `409` "to be consistent" broke a
  documented public contract. Converge on the *decision*, not on the *value*.
- **Forgetting the jobs.** The HTTP handler was clean; the receipt job still had a
  hard-coded `sleep(1000)`.
- **Making the table partial and adding a permissive default.** The default then silently
  maps a transient dependency failure to `500`.
- **Measuring only lines.** Lines fell 47%; the number that mattered was *decision sites*
  (13 → 4).

## Checklist

- [ ] A duplication report exists for the flow, with drift observed or not observed.
- [ ] Each extracted table is exhaustive or has a named conservative default.
- [ ] The owning layer was migrated first.
- [ ] Every old branch was deleted, not commented out.
- [ ] The lint rule that prevents re-introduction is enabled and passing.
- [ ] The change cost of a new code was re-measured after the refactor.

## Related

- [Finding and Measuring Repetition](../01-concepts/01-finding-and-measuring-repetition.md)
- [Simplifying Conditionals, Translation, and Retries](../01-concepts/03-simplifying-conditionals-translation-and-retries.md)
- [Localizing Decisions and Conventions](../01-concepts/04-localizing-decisions-and-conventions.md)
- [A Complexity Budget for a Feature](./02-a-complexity-budget-for-a-feature.md)
