# Partial Features, Degraded Mode, and Disabling Work

> Part XI · Chapter 30 · Sections 30.6–30.8 · _Estimated reading time: 18 min_
> **Prerequisite:** [Fallback Responses and Cached Fallbacks](./02-fallback-responses-and-cached-fallbacks.md)

## In one sentence

Instead of treating the system as fully up or fully down, **partial features and degraded mode** let
you keep the core working by turning off specific capabilities — often automatically, driven by the
state of the dependency they need.

## Why this matters in production

A single dependency often powers several features: the LLM provider powers summaries, semantic search,
and agent runs; the email provider powers receipts, digests, and alerts. If you only have "on" and
"off," one failing feature drags the rest with it. Feature-level kill switches and a named degraded
mode let you shed exactly the work that cannot succeed, keep the capacity for what can, and give
operators a single lever during an incident.

## 30.6 — Partial features

A **partial feature** returns a reduced version of itself rather than failing.

| Feature | Full | Partial |
| ------- | ---- | ------- |
| Search | Personalized + semantic | Keyword-only |
| Dashboard | Live + trends | Cached summary |
| Invoice list | Live totals | Last exported snapshot |
| Recommendations | Personalized | Popular items |
| LLM summary | Generated | Extractive first paragraph |
| Notifications | Real-time push | Batched email |
| File preview | Rendered | Download-only |

### Implementing a partial feature

```ts
type SearchMode = "full" | "keyword_only" | "unavailable";

async function search(q: string, user: User): Promise<SearchResult> {
  let mode: SearchMode = "full";
  let results: Item[];

  if (semanticBreaker.isOpen()) {
    mode = "keyword_only";
    results = await keywordSearch(q);
  } else {
    try {
      results = await semanticSearch(q, user);
    } catch (err) {
      if (!isRetryable(err)) throw err;
      mode = "keyword_only";
      results = await keywordSearch(q);
    }
  }

  return {
    results,
    mode,
    degraded: mode !== "full",
    notice: mode === "keyword_only"
      ? "Showing basic results — personalized ranking is unavailable."
      : undefined,
  };
}
```

The client renders the same list; only ranking and the notice differ. That is what makes the
degradation graceful.

## 30.7 — Disabling non-essential work

When capacity is scarce, stop doing work that does not affect the core task.

### Candidates for shedding

| Work | Impact of disabling |
| ---- | ------------------- |
| Analytics/telemetry events | Loss of metrics (counter it) |
| Digest/prefetch jobs | Delayed, not lost |
| Image thumbnailing | Placeholder shown |
| Search indexing | Slightly stale index |
| Recommendation refresh | Older recommendations |
| Audit enrichment | Core audit record remains |
| Non-critical webhooks | Retried later |
| Warmup/backfill | Deferred |

### Never shed

- Authorization and audit of security-relevant actions.
- Payment authorization and ledger writes.
- Data durability writes.
- Anything whose absence causes silent corruption.

### Feature flags vs circuit-driven shedding

| Mechanism | Trigger | Speed | Use |
| --------- | ------- | ----- | --- |
| **Feature flag** | Human decision | Seconds–minutes | Planned degradation, incidents |
| **Breaker-driven** | Automatic | Milliseconds | Dependency failure |
| **Load-driven (utilization)** | Automatic | Seconds | Traffic spikes |
| **Time-based** | Schedule | Planned | Known peak windows |

Use automatic shedding for fast reaction; use flags for judgment calls and for features that should
stay off while a dependency recovers.

```ts
const flags = await flagsClient.getAll();

if (flags.disable_recommendations || utilization() > 0.85) {
  return { items: [], disabled: true };
}
```

> ⚠️ **Hazard.** A flag service outage must not disable the flags themselves. Cache the last-known
> flag values and fail **open to the last state**, not to "everything on" or "everything off."

## 30.8 — Degraded mode

**Degraded mode** is a named, system-wide operating state with a documented feature matrix. It turns
many small decisions into one.

### Define levels

| Level | Name | Trigger | Behavior |
| ----- | ---- | ------- | -------- |
| 0 | Normal | All healthy | Full features |
| 1 | Reduced | One optional dependency down | Hide optional features, label |
| 2 | Essential | Critical-adjacent dependency down | Core only, no personalization |
| 3 | Read-only | Primary DB read replica only | Writes rejected with `503` |
| 4 | Unavailable | Core DB/auth down | Maintenance page, `503` |

### Declaring mode

```yaml
degraded_mode:
  level: 2
  reason: "primary_database_failover"
  started_at: "2026-10-21T09:15:00Z"
  features:
    checkout: "enabled"
    auth: "enabled"
    search: "keyword_only"
    recommendations: "disabled"
    llm_summary: "disabled"
    exports: "deferred"
  user_notice: "Some features are temporarily limited while we recover."
```

### Entering and leaving

```text
automatic: dependency health aggregator computes level every 5s
manual:    incident commander can pin a level higher (never lower than auto)
exit:      automatic when all required dependencies are healthy for 2× the breaker cooldown
hysteresis: do not flap between levels faster than once per 60s
```

Manual pins prevent an operator from accidentally forcing "normal" while a dependency is still
unhealthy; the effective level is `max(auto, manual)`.

### Mode must reach every surface

| Surface | How mode appears |
| ------- | ---------------- |
| HTTP responses | `X-Degraded-Mode: 2`, `Warning` |
| UI | Banner + per-widget "unavailable" states |
| Status page | Level and affected features |
| Logs | `degraded_mode=2` on every request |
| Metrics | `degraded_mode{level=2}` gauge |
| Alerts | Annotated with current mode |

If the mode is only in a config file, it is not a real operating mode.

## Worked example — LLM provider outage

```text
09:00 LLM error rate > 40% for 20s → breaker opens
09:00 health aggregator sets level 1
      ├─ summaries → template
      ├─ semantic search → keyword
      └─ agent runs → queued for later
      checkout/auth unaffected; banner: "AI features limited"
09:12 provider recovers; probes succeed
09:14 health aggregator waits 2× cooldown (40s) → level 0
09:14 banner dismissed; queued agent runs drain with backoff
```

## Key data / numbers

- Mode recomputation: every **5s**; hysteresis **60s**.
- Exit requires healthy for **2×** breaker cooldown.
- Load-shed thresholds: **70%** batch, **85%** interactive, **95%** critical-only.
- Flag cache: last-known values, TTL **5min**.
- Mode surfaces: **6** (HTTP, UI, status, logs, metrics, alerts).

## Real-world use case — Acme SaaS

Acme's `WebhookIngest` shared a worker pool with `ExportJob`. During a webhook burst, exports
starved and customers saw stuck jobs. The team introduced a level-1 mode: when webhook queue depth
exceeded a threshold, exports were **deferred** (not failed) and a banner explained the delay. They
also disabled recommendation refresh above 85% utilization. The next burst delayed 300 exports by
minutes instead of failing 40 of them, and the dashboard stayed responsive.

## Trade-offs

| Mechanism | Pros | Cons |
| --------- | ---- | ---- |
| Partial features | Keeps task usable | More code paths |
| Feature flags | Human control | Stale flags, config risk |
| Automatic shedding | Fast | Can overreact |
| Named mode levels | Simple operations | Coarse-grained |
| Per-feature toggles | Precise | Harder to reason about |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Define named levels with a matrix | Invent states during an incident |
| Cache flag values | Fail "on" or "off" when flags are down |
| Shed non-essential work first | Disable auth or payments to save capacity |
| Use hysteresis between levels | Flap modes every few seconds |
| Surface the mode everywhere | Keep it in a config file only |
| Defer instead of fail when possible | Drop exports silently |

## Common mistakes

- **Kill switch disables the health check** along with the feature.
- **No flag cache**, so a flag outage changes behavior unpredictably.
- **Level flapping**, confusing users and operators.
- **Shedding audit or auth** as "non-essential."
- **Partial feature with a different response shape**, breaking clients.

## Checklist

- [ ] Optional features have partial or disabled states.
- [ ] Non-essential work can be shed automatically.
- [ ] Feature flags are cached with last-known values.
- [ ] Named degraded levels have a feature matrix.
- [ ] Mode changes are automatic with hysteresis.
- [ ] Manual pins cannot force a lower level than auto.
- [ ] Mode appears in responses, UI, logs, metrics, and alerts.

## Related

- [Fallback Failure, Silent Inaccuracy, and Communication](./04-fallback-failure-silent-inaccuracy-and-communication.md)
- [Degraded Mode for Acme](../03-practical-examples/01-degraded-mode-for-acme.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
