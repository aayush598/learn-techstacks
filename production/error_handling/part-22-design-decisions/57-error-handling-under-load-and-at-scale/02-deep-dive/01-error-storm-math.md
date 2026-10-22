# Error-Storm Math: Amplification Factors, Budgets, and Breakpoints

> Part XXII · Chapter 57 · Sections 57.1, 57.2, 57.3, 57.12 · _Estimated reading time: 22 min_
> **Prerequisite:** [Failure Amplification and Error Storms](../01-concepts/01-failure-amplification-and-error-storms.md)

## In one sentence

Every error-handling policy has a **numeric amplification factor**, and an outage is what
happens when that factor meets a system already running near capacity.

## Why this matters in production

Most incident reviews describe amplification qualitatively — "the retries overwhelmed the
provider". That description is not actionable, because it cannot be compared against a
design change. The arithmetic can be:

> "Our amplification factor was 12. With one retry owner and a 10% retry budget it would
> have been 3. At 10% provider errors, that is the difference between 190% and 40% extra
> load — and the difference between recovery and collapse."

This deep dive gives you the formulas, the breakpoints, and the way to compute them from
your own topology.

## The formulas

### The amplification factor

```text
  A = attempts × nested_layers × fan_out
```

| Symbol | Meaning | How to measure |
| ------ | ------- | -------------- |
| `attempts` | Total attempts per operation, including the first | Count in the retry policy: `max_attempts` |
| `nested_layers` | Number of layers that each retry independently | Count the call stack of retries |
| `fan_out` | Downstream calls per request | Count the calls in the request path |

`A` is the multiplier applied to **downstream** load when the error rate is `e`:

```text
  downstream_load_factor = (1 − e) + e × A = 1 + e × (A − 1)
```

For `e = 0.10` and `A = 12`: `1 + 0.10 × 11 = 2.1` — downstream load **doubles**.
For `e = 0.30` and `A = 12`: `1 + 0.30 × 11 = 4.3` — downstream load **quadruples**.

### The retry fraction

```text
  retry_fraction = (e × (A − 1)) / (1 + e × (A − 1))
```

For `e = 0.30`, `A = 12`: `retry_fraction = 3.3 / 4.3 = 0.77` — **77% of all traffic is
retries**. The system is mostly retrying itself.

### The capacity breakpoint

Let `C` be the dependency's healthy capacity (requests/second it can serve) and `L` the
caller's offered load. The system collapses when:

```text
  L × (1 + e × (A − 1)) > C
```

Solving for `e`:

```text
  e_collapse = (C/L − 1) / (A − 1)
```

**This is the number that matters.** If the dependency runs at 70% utilization
(`C/L = 1/0.7 = 1.43`), then:

| `A` | `e_collapse` | Meaning |
| --- | ------------- | ------- |
| 1 (no retries) | 0.43 | Collapses at a 43% error rate |
| 3 | 0.21 | Collapses at 21% |
| 6 | 0.086 | Collapses at 8.6% |
| 12 | 0.039 | Collapses at 3.9% |
| 27 | 0.016 | Collapses at 1.6% |

> **The higher your amplification factor, the smaller your margin.** An `A` of 12 means a
> dependency that is only 4% broken will take you down — before your error-rate alert
> (commonly at 5%) even fires.

### The feedback-loop gain

A retry storm is a feedback loop: extra load slows the dependency, which raises the error
rate, which adds more retries. The loop gain is:

```text
  gain = (∂extra_load / ∂error_rate) × (∂error_rate / ∂load)
```

In practice, the gain is roughly proportional to `A`: with `A = 12`, a 1% increase in load
can raise the error rate by several percent, and the loop diverges.

The only way to make the gain < 1 is to **remove the feedback**: a circuit breaker (load
decoupled from the error rate) or a retry budget (retry volume capped regardless of the
error rate).

## Worked scenarios

### Scenario A — the checkout service (Acme SaaS)

**Topology:**

```text
  client ──▶ API ──▶ CheckoutService ──▶ StripeAdapter ──▶ Stripe
            (retry 2)   (retry 3)          (SDK retry 2)
```

| Layer | Attempts | Note |
| ----- | -------- | ---- |
| HTTP client library | 2 | Retries `5xx` and connection errors |
| API gateway | 2 | Retries on connection reset |
| CheckoutService | 3 | Retries `503` from the adapter |
| Stripe SDK | 2 | Retries network errors |

**Step 1 — find the amplification factor.**

```text
  attempts        = 2 × 2 × 3 × 2 = 24
  nested_layers   = 4
  fan_out         = 1
  A = 24
```

**Step 2 — compute the collapse breakpoint.** Stripe is running at 60% utilization during
peak (`C/L = 1.67`):

```text
  e_collapse = (1.67 − 1) / (24 − 1) = 0.029
```

A **2.9% error rate** at Stripe collapses Acme's checkout. During Acme's 2025 incident,
Stripe's error rate reached 8% for 14 minutes — well past the breakpoint.

**Step 3 — compute the load at 8% errors.**

```text
  factor = 1 + 0.08 × 23 = 2.84
```

Stripe received **2.84× its normal checkout traffic**. The provider, which was already
degraded, went fully down. Acme's retries were a large part of the provider's outage.

**Step 4 — design the fix and re-compute.**

| Change | New `attempts` | New `A` | New `e_collapse` |
| ------ | -------------- | ------- | ---------------- |
| Disable the SDK's internal retries | 12 | 12 | 0.061 |
| Disable the gateway retries for 5xx | 6 | 6 | 0.133 |
| One retry owner (the adapter only) | 3 | 3 | 0.333 |
| Add a circuit breaker (load → 0 when open) | 3 + breaker | — | breakpoint no longer applies |
| Add a retry budget (10%) | capped | — | — |

With `A = 3`, Stripe would need to be **33% broken** to collapse Acme — a 10× improvement in
margin, achieved by removing 21 of 24 attempts.

### Scenario B — the AI summary feature (Acme SaaS)

**Topology:**

```text
  request ──▶ DashboardService ──▶ AgentService ──▶ LLM provider
                 (1 call)            (12 calls/run, 3 attempts, retry budget 5)
```

Here `fan_out` is the dominant factor:

```text
  attempts      = 3
  nested_layers = 1
  fan_out       = 12
  A = 36
```

At `e = 0.20` (a provider rate-limit wave):

```text
  factor = 1 + 0.20 × 35 = 8.0
```

The LLM provider would receive **8× its normal traffic** from Acme. Combined with the retry
budget (5 retries per run, 20 requests per run), the worst case is:

```text
  per_run_max_requests = 12 calls + 8 retries = 20
  20 requests/run ÷ 12 useful calls = 1.67 effective waste factor
```

With the budget alone (no A from the retry layer), the provider sees at most **1.67×** the
calls it needs — survivable. Without the budget, it sees 8× — fatal.

**Conclusion:** for a fan-out workload, the **per-run budget** is the primary control, and
the retry count is secondary.

### Scenario C — the webhook endpoint (Acme SaaS)

**Topology:** `Stripe → WebhookIngest → Postgres + task queue`.

```text
  attempts      = 3 (client retry) × 3 (Stripe redelivery) = 9
  nested_layers = 2
  fan_out       = 1
  A = 9
```

`e_collapse = (1.67 − 1) / 8 = 0.084` — an 8.4% internal error rate would collapse the
handler.

The mitigation was not to reduce `A` (Stripe's redelivery is out of Acme's control) but to
**decouple** it: the circuit breaker reduces `fan_out` to 0 for the failing dependency, and
the retry budget caps the rest.

## How it works (mechanics)

### Computing `A` for your own topology

```text
  1. Draw the request path, client → ... → leaf dependency.
  2. At each layer, ask: "does this layer retry?"
  3. Record the max attempts (including the first try).
  4. Count the leaf dependencies per request (fan_out).
  5. A = Π(attempts) × fan_out
  6. For each dependency, compute e_collapse with the formula above.
  7. Any dependency with e_collapse below your alert threshold is a finding.
```

Step 7 is the review rule: **if the collapse breakpoint is below your error-rate alert
threshold, the alert fires after the collapse has already happened.** For Acme's alert
threshold of 5%, any dependency needs `A ≤ (1/0.05) ≈ 13` to be safe at 70% utilization —
which is why the target is `A ≤ 3`.

### Choosing the retry budget

Given `A` and the alert threshold `t`, the budget `b` must satisfy:

```text
  retry_fraction ≤ b  and  e_collapse > t

  ⇒ b ≤ e_max × (A − 1) / (1 + e_max × (A − 1))
```

With `e_max = 0.05` (the alert threshold) and `A = 3`:

```text
  b ≤ 0.05 × 2 / (1 + 0.05 × 2) = 0.095  →  b = 9.5%
```

So a **10% budget** is exactly right for `A = 3` and a 5% alert threshold. The common
recommendation of 5–10% is not folklore; it falls out of the formula.

### Making the gain < 1

| Control | Effect on the feedback loop |
| ------- | ---------------------------- |
| Circuit breaker | Breaks the loop: load → 0 when the dependency fails |
| Retry budget | Caps the retry volume regardless of the error rate |
| Shorter timeout | Reduces the time each failure holds resources |
| Deadline propagation | Prevents a slow upstream from holding a downstream slot |
| Fail fast on permanent errors | Removes the retryable fraction of the error rate |

A breaker is the only control that *disconnects* load from the error rate. A budget caps
the *magnitude* but not the *coupling*.

## Key data / numbers

| Item | Value | Notes |
| ---- | ----- | ----- |
| Target amplification factor `A` | ≤ 3 | Per dependency path |
| Maximum acceptable `A` | ≤ 13 | So the 5% alert fires before the collapse |
| Recommended retry budget | 5–10% of traffic | Derived from the alert threshold |
| Retry budget window | 10 s | Smooths bursts without lagging |
| Max nested retry layers | 1 | One owner per dependency |
| Retry attempts (standard) | 3 | |
| Retry attempts (fan-out workloads) | 2–3 + a per-run budget | The budget dominates |
| Per-run request budget (agent-style) | 20 requests, 5 retries | 12 useful calls |
| Breakpoint at `A = 3`, 70% utilization | 33% error rate | Comfortable margin |
| Breakpoint at `A = 12`, 70% utilization | 3.9% error rate | Alert fires too late |
| Alert threshold | 5% over 1 min | Must be below the breakpoint |
| Error budget burn-rate alert | 14.4×/1 h and 6×/6 h | Multi-window |

## Real-world use case — the postmortem number

Acme's most useful postmortem artifact was a **one-line amplification table** in the
incident review:

| Dependency | Attempts | Layers | Fan-out | `A` | Utilization | `e_collapse` | Alert threshold | Margin |
| --------- | -------- | ------ | ------- | --- | ----------- | ------------- | --------------- | ------ |
| Stripe | 24 | 4 | 1 | 24 | 60% | 2.9% | 5% | **−2.1%** |
| Postgres | 9 | 3 | 1 | 9 | 75% | 10.0% | 5% | +5.0% |
| LLM | 3 | 1 | 12 | 36 | 30% | 1.8% | 5% | **−3.2%** |

The negative margins were the finding: **both dependencies could collapse the service
before the alert fired.** The postmortem action items were not "add alerts" but "reduce `A`":
disable the SDK retries (24 → 12), add a kill switch, and add a retry budget.

After the fixes, the table reads `A = 3` for Stripe and `A = 3` (with a 20-request budget)
for the LLM, and the margins became +28% and +23%.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Compute `A` for every dependency path | Assume retries are "only 3" |
| Compute `e_collapse` and compare it to your alert threshold | Set the alert threshold without checking the breakpoint |
| Keep `A ≤ 3` | Accept `A > 10` anywhere |
| Use a breaker to disconnect load from the error rate | Rely on a budget alone to stop a feedback loop |
| Set the budget from the alert threshold (5–10%) | Copy a budget number without checking the math |
| Re-compute `A` after every new dependency or client | Let the SDK defaults change silently |

## Checklist

- [ ] Every dependency path has a documented amplification factor.
- [ ] Every `A` is ≤ 3.
- [ ] For each dependency, `e_collapse` is above the error-rate alert threshold.
- [ ] The alert threshold (5%) is below the lowest `e_collapse`.
- [ ] A retry budget exists per dependency, sized from the formula.
- [ ] SDK-internal retries are explicitly disabled or accounted for.
- [ ] A circuit breaker exists for every slow, frequently-failing dependency.

## Related

- [Failure Amplification and Error Storms](../01-concepts/01-failure-amplification-and-error-storms.md)
- [Retry Budget and Queue Bounding](./02-retry-budget-and-queue-bounding.md)
- [Chapter 27 — Retry Policies](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../../part-11-retry-and-resilience/29-timeouts-circuit-breakers-and-bulkheads/README.md)
