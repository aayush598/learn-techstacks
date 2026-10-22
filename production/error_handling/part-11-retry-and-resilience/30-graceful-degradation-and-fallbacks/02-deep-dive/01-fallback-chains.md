# Fallback Chains

> Part XI · Chapter 30 · Sections 30.3–30.9 · _Estimated reading time: 22 min_
> **Prerequisite:** [Fallback Responses and Cached Fallbacks](../01-concepts/02-fallback-responses-and-cached-fallbacks.md)

## In one sentence

A fallback chain is an **ordered, budgeted sequence of substitutes** that ends in a terminal state —
and its quality is determined by the *worst* step, not the best one.

## Why this matters in production

Most teams implement fallbacks one at a time and discover the chain accidentally. The cache fallback
calls the replica "just in case"; the replica call has no timeout; the static default is returned when
both fail. In an incident, the chain takes longer than the user's deadline, hits the database the
primary already overloaded, and still ends with a value nobody can identify. Treating the chain as a
designed artifact — with a budget, an order, skip rules, and provenance — prevents all of that.

## Anatomy of a chain

```text
request (deadline D)
  │
  ├─ step 1: live source          budget b1, needs = primary
  │    └─ success → return {source: live}
  │
  ├─ step 2: cache                budget b2, needs = cache
  │    └─ success → return {source: cache, asOf: cached.at, degraded}
  │
  ├─ step 3: derived/cheaper      budget b3, needs = secondary
  │    └─ success → return {source: derived, degraded}
  │
  └─ step 4: static default       budget ≈ 0
       └─ success → return {source: static, degraded}
  │
  └─ terminal: UnavailableError
```

### Properties of a good chain

| Property | Meaning |
| -------- | ------- |
| **Ordered** | Cheapest, most correct first |
| **Budgeted** | `Σ bᵢ ≤ D − safety` |
| **Dependency-aware** | Skips steps whose dependency is down |
| **Non-recursive** | Never revisits the primary or a failed step |
| **Terminal** | Always ends in a value or an explicit error |
| **Provenanced** | Every result says where it came from |
| **Eligible** | Only used where policy permits |

## Ordering strategy

### Default order

```text
live → cache → derived → static → error
```

### When to reorder

| Situation | Order |
| --------- | ----- |
| Live is slow but cache is fresh | cache-first for reads |
| Security data | live → error (no cache) |
| High fan-out page | cache → live (parallel, first wins) |
| Cost-sensitive | cache → cheaper model → static |
| Regulatory freshness | live → error |

### Parallel hedged chain

For latency-sensitive reads, issue the live and cached reads concurrently and take the first
successful result, with the cache result labelled:

```ts
const [live, cached] = await Promise.allSettled([
  withTimeout(provider.get(), 800),
  cache.get(key),
]);

if (live.status === "fulfilled") return { value: live.value, source: "live" };
if (cached.status === "fulfilled" && cached.value) {
  return { value: cached.value, source: "cache", asOf: cached.value.at, degraded: true };
}
throw new UnavailableError("NO_SOURCE");
```

Hedging doubles load on the primary; use it only when the primary is healthy and latency matters.

## Budgeting a chain

The chain shares one deadline:

```text
D = 8s (user deadline)
safety = 200ms

step 1 live:    2500ms
step 2 cache:    200ms
step 3 derived: 1000ms
step 4 static:     0ms
Σ = 3700ms ≤ 7800ms ✓
```

But the *expected* path is what matters for UX. If step 1 usually succeeds in 900ms, the chain is fast.
The budget exists to bound the failure path.

### Shrinking budgets

Each step should get less time than the one before, because a later step is a more desperate
substitute:

```text
b1 = 2500ms
b2 = min(500ms, remaining / 3)
b3 = min(1000ms, remaining / 2)
b4 = 0
```

### Time-based cutoffs

If the remaining budget is below the minimum useful time for a step, skip it:

```ts
if (deadline - Date.now() < step.minUsefulMs) continue;
```

A stale cache read that takes 300ms is not useful when the user has 100ms left; better to return the
static default or an error.

## The chain evaluator

```ts
interface Step<T> {
  name: string;
  minUsefulMs: number;
  needs?: string;                 // breaker key
  run: (signal: AbortSignal) => Promise<T>;
}

interface ChainResult<T> {
  value: T;
  source: string;
  degraded: boolean;
  asOf: number;
  skipped: string[];
}

export async function evaluateChain<T>(
  steps: Step<T>[],
  deadline: number,
  opts: {
    breakers?: Map<string, { isOpen(): boolean }>;
    perStepCapMs?: number;
    safetyMs?: number;
  } = {},
): Promise<ChainResult<T>> {
  const skipped: string[] = [];
  const cap = opts.perStepCapMs ?? 2_000;
  const safety = opts.safetyMs ?? 50;

  for (const step of steps) {
    if (step.needs && opts.breakers?.get(step.needs)?.isOpen()) {
      skipped.push(`${step.name}:breaker_open`);
      continue;
    }
    const remaining = deadline - Date.now() - safety;
    if (remaining < step.minUsefulMs) {
      skipped.push(`${step.name}:no_budget`);
      continue;
    }

    const controller = new AbortController();
    const budget = Math.min(cap, remaining);
    const timer = setTimeout(() => controller.abort(), budget);

    try {
      const value = await step.run(controller.signal);
      return {
        value,
        source: step.name,
        degraded: step.name !== steps[0].name,
        asOf: Date.now(),
        skipped,
      };
    } catch {
      skipped.push(`${step.name}:failed`);
    } finally {
      clearTimeout(timer);
    }
  }

  throw new UnavailableError("ALL_FALLBACKS_EXHAUSTED", { skipped });
}
```

Note the evaluator never re-runs a step and never consults the primary indirectly. The `skipped` list
is valuable for debugging: it explains *why* the chain ended where it did.

## Provenance

Every step returns a different confidence level. Encode it:

| Source | `degraded` | `asOf` | Confidence |
| ------ | ---------- | ------ | ---------- |
| live | false | now | high |
| cache | true | cached.at | medium (depends on age) |
| derived | true | now | medium |
| static | true | n/a | low |
| error | — | — | none |

```ts
const result = await evaluateChain(steps, deadline);
res.setHeader("X-Data-Source", result.source);
res.setHeader("X-Data-As-Of", new Date(result.asOf).toISOString());
if (result.degraded) res.setHeader("X-Degraded", "true");
```

## Worked example — LLM summary chain

```text
Budget: 8s (user waits for the page)
  step 1: large model, 5s        (p99 4.2s)
  step 2: small model, 2s        (p99 1.1s)
  step 3: extractive summary, 300ms
  step 4: static "Summary unavailable" template, 0ms
```

Trace during a large-model outage:

```text
t=0.00  step 1 starts
t=5.00  abort; step 2 starts (3s budget left, cap 2s)
t=6.10  step 2 succeeds
result: {source: small-model, degraded: true, asOf: t=6.1}
```

The user sees a summary within 6.1s, labelled "Generated with reduced quality." Without the chain, they
would have waited 5s and then received a `503`.

## Testing the chain

| Test | Assertion |
| ---- | --------- |
| Primary healthy | returns `live`, no fallback metric |
| Primary fails | returns next step, `degraded=true` |
| Cache stale beyond tolerance | cache step skipped |
| All steps fail | `ALL_FALLBACKS_EXHAUSTED` |
| Deadline nearly expired | later steps skipped |
| Breaker open for step 2 | step 2 skipped, step 3 tried |
| Fallback hangs | aborted at its budget |
| Chain latency | ≤ deadline − safety |

```ts
it("skips a step whose breaker is open", async () => {
  const breakers = new Map([["cache", { isOpen: () => true }]]);
  const result = await evaluateChain(
    [
      { name: "live", minUsefulMs: 50, run: async () => { throw new Error("down"); } },
      { name: "cache", minUsefulMs: 10, needs: "cache", run: async () => "cached" },
      { name: "static", minUsefulMs: 0, run: async () => "static" },
    ],
    Date.now() + 1_000,
    { breakers },
  );
  expect(result.source).toBe("static");
  expect(result.skipped).toContain("cache:breaker_open");
});
```

## Key data / numbers

- Chain length: **2–4** steps.
- Shared deadline, safety margin **50–200ms**.
- Per-step cap: **≤ 2s** for interactive, larger for async.
- Shrinking budget: later steps get **⅓–½** of the previous.
- Static/terminal step: **0ms**.
- Hedging: only when primary is healthy; **2×** load.

## Real-world use case — Acme SaaS

Acme's `AgentRun` summarizer used a single 30s LLM call. On timeout the whole run failed, even when a
smaller model could have answered. The team built a four-step chain (large model 5s → small model 2s →
extractive 300ms → template) with a shared 8s budget. Chain success rose from 91% to 99.7%, p99 for
degraded responses stayed under 7s, and `fallback_used_total{step="small"}` became the early warning
for large-model degradation.

## Trade-offs

| Decision | Benefit | Cost |
| -------- | ------- | ---- |
| More steps | Higher success | More paths, more latency |
| Hedged reads | Low latency | 2× primary load |
| Cache-first | Fast, cheap | Staleness risk |
| Static last step | Never errors | Low-quality output |
| Long per-step caps | Higher success | Misses the deadline |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Share one deadline across the chain | Give each step a fresh timeout |
| Skip steps whose breaker is open | Try every step blindly |
| Record skipped steps | Silently swallow each failure |
| Label the source and age | Return every step identically |
| End with a terminal error | Loop back to the primary |
| Test each step failing | Test only the happy path |

## Common mistakes

- **Fresh timeout per step**, so the chain exceeds the user's budget.
- **Cache step that queries the primary on miss**, recreating the outage.
- **No terminal state**, so failures hang.
- **Static step before a better substitute**, returning low-quality data unnecessarily.
- **No provenance**, so clients cannot tell degraded from live.

## Checklist

- [ ] Chain order is documented and justified.
- [ ] All steps share one deadline with a safety margin.
- [ ] Later steps get smaller budgets.
- [ ] Steps with open breakers are skipped.
- [ ] Steps below minimum useful time are skipped.
- [ ] Chain length is bounded and non-recursive.
- [ ] Every result carries source, age, and degraded flag.
- [ ] Each step's failure is tested.

## Related

- [Fallback Responses and Cached Fallbacks](../01-concepts/02-fallback-responses-and-cached-fallbacks.md)
- [Partial Features, Degraded Mode, and Disabling Work](../01-concepts/03-partial-features-degraded-mode-and-disabling.md)
- [Fallback Chain for LLM Summary](../03-practical-examples/02-fallback-chain-llm-summary.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
