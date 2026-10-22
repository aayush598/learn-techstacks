# Retry Amplification and Budgets

> Part XI · Chapter 27 · Sections 27.10, 27.15–27.18 · _Estimated reading time: 19 min_
> **Prerequisite:** [Backoff and Jitter Math](./01-backoff-and-jitter-math.md)

## In one sentence

Amplification is **multiplication, not addition**: every retrying layer multiplies the load on the
dependency, and a retry budget is the aggregate valve that keeps that product from exceeding what the
dependency can survive.

## Why this matters in production

A team reasons about one retry loop at a time: "3 attempts is modest." They forget the SDK's 3, the
gateway's 2, and the worker's 5. During a partial outage, the dependency sees orders of magnitude
more traffic than the request rate implies — and the retries arrive exactly when it is least able to
serve them. Understanding the arithmetic is what turns "we added retries" into "we bounded
amplification."

## The multiplication model

Let each layer `i` have `a_i` attempts. The number of calls reaching the dependency for one logical
operation is:

```text
A = Π a_i
```

If each call fans out to `f` downstream items, total dependency calls:

```text
T = f × Π a_i
```

| Layers | Attempts each | Product | With fan-out 5 |
| ------ | ------------- | ------- | -------------- |
| API gateway → service | 2 × 3 | 6 | 30 |
| + SDK retries | 2 × 3 × 3 | 18 | 90 |
| + worker retries | 5 × 2 × 3 × 3 | 90 | 450 |

The last row is not hypothetical: it is what a "small" retry on each layer becomes.

## Where amplification hides

| Hidden retry source | How to find it |
| ------------------- | -------------- |
| HTTP client defaults | Read the client config (`retries`, `maxRetries`) |
| Provider SDK | Check constructor options / docs |
| Load balancer / gateway | Inspect retry policy |
| Queue redelivery | Visibility timeout + max receives |
| Database driver | Connection retry on `08xxx` |
| Framework middleware | Retry decorators/interceptors |
| Service mesh | Envoy retry policy |

> ⚠️ **Hazard.** Two silently retrying layers are worse than one visible one. Audit defaults before
> adding your own policy.

## Retry budgets as a valve

A retry budget caps retries relative to successes, independent of per-request attempts. The token
bucket model:

```text
On each successful request:  tokens = min(max, tokens + 1)
On each retry:               require tokens >= cost; tokens -= cost
If insufficient tokens:      fail fast (do not retry)
```

During normal operation, successes replenish tokens and retries flow. During an outage, successes
stop, the bucket drains, and retries stop — automatically reducing load on the dependency.

```python
class RetryBudget:
    def __init__(self, max_tokens=100, ratio=0.1, cost=1):
        self.tokens = max_tokens
        self.max_tokens = max_tokens
        self.ratio = ratio       # retries per success
        self.cost = cost

    def on_success(self):
        # Earn a fraction of a token per success; integer bucket for clarity.
        self.tokens = min(self.max_tokens, self.tokens + max(1, int(1 / max(self.ratio, 1e-9))))

    def try_acquire(self) -> bool:
        if self.tokens >= self.cost:
            self.tokens -= self.cost
            return True
        return False
```

In practice, implement the bucket with floats or a sliding window; the invariant is the same: **the
retry rate cannot exceed `ratio × success rate`** for long.

### Budget parameters

| Parameter | Starting value | Notes |
| --------- | -------------- | ----- |
| Ratio | 10–20% | Retries per successful request |
| Bucket max | ~100 retries | Burst allowance |
| Cost | 1 | Increase for expensive calls |
| Scope | Per dependency per caller | Never global |

A global budget lets a single noisy tenant or endpoint starve everyone else's retries.

## Worked example — containing a nested stack

Before:

```text
Checkout service  3 attempts
  └─ Stripe SDK   3 attempts (default)
      └─ HTTP     2 attempts (default)
A = 3 × 3 × 2 = 18 calls per charge
```

After:

```text
Checkout service  3 attempts  ← sole owner
  └─ Stripe SDK   1 attempt   (retries disabled)
      └─ HTTP     1 attempt   (retries disabled)
A = 3
```

The service already holds the idempotency key and the deadline, so it is the correct owner. The total
worst-case calls drop by 83%, and the provider sees a predictable maximum during incidents.

## Budget math under failure

Suppose the dependency starts failing 50% of requests. With no budget:

```text
successful ops: 0.5R
failed ops:     0.5R → each retried up to 3 times → 1.5R extra calls
total calls ≈ 2.0R (plus jitter timing effects)
```

With a 20% budget:

```text
retries allowed ≈ 0.2 × successes = 0.1R
total calls ≈ 0.5R + 0.1R = 0.6R
```

The budget cuts the added load by roughly an order of magnitude during the exact window that matters.

## Retry ownership as an amplification control

Ownership is not bureaucracy; it is the only reliable way to keep `Π a_i` small. Assign ownership by
capability:

| Decision needs | Owner |
| -------------- | ----- |
| Classification of provider errors | Provider adapter |
| Idempotency key | Business service |
| Deadline | Request/job boundary |
| DLQ policy | Job worker |
| Transport-level transient retry | HTTP client (if no one else retries) |

If two layers claim ownership, one must be disabled. Document it in the integration's README or
config so the next engineer does not re-enable a default.

## Key data / numbers

- Amplification `A = Π attempts` across layers; with fan-out `T = f × A`.
- Budget ratio commonly **10–20%**; bucket burst ~100 retries.
- Disabling SDK and client retries can cut worst-case calls by **5–10×**.
- Example: 3 × 3 × 2 = 18 calls per logical operation.
- Queue redelivery counts as a retry layer (visibility timeout × max receives).

## Real-world use case — ExportJob

`ExportJob` ran on a queue configured for 5 receives. Its HTTP client defaulted to 3 retries, and
the page-fetch helper wrapped that in another 3. During a provider slowdown, one job produced up to
`5 × 3 × 3 = 45` requests per page. The provider rate-limited the tenant, and the queue backed up.
The fix reduced the queue to 3 receives, disabled client retries, and made the page helper the sole
owner with a retry budget of 15% per tenant. Provider request volume during the next incident fell
by roughly 80%, and jobs drained instead of accumulating.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| Cap attempts per request | Simple | Ignores fleet-wide load |
| Retry budget | Adapts to health | Tuning, state per dependency |
| Single owner | Predictable product | Requires cross-team agreement |
| Disable SDK retries | Eliminates hidden multiplication | Loses SDK-specific handling |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Calculate the attempt product | Reason about layers in isolation |
| Audit SDK/client defaults | Assume retries are off by default |
| Scope budgets per dependency | Share one global budget |
| Document the retry owner | Let every layer retry "just in case" |
| Include queue redelivery in the math | Treat the queue as retry-free |

## Common mistakes

- **Counting only your own loop.** The SDK silently triples it.
- **Budget with no floor.** Low-traffic services never retry and look fragile.
- **Budget evaluated per attempt** instead of per logical operation.
- **Disabling retries everywhere** to fix amplification, losing transient recovery entirely.
- **Forgetting fan-out** in the multiplication.

## Checklist

- [ ] Every retrying layer is inventoried.
- [ ] The attempt product is computed and acceptable.
- [ ] Exactly one owner per dependency is documented.
- [ ] A retry budget exists per dependency and caller.
- [ ] Queue redelivery is counted as a layer.
- [ ] SDK/client retry defaults are explicitly configured.

## Related

- [Storms, Ownership, and Exhaustion](../01-concepts/05-storms-ownership-and-exhaustion.md)
- [Budgets, Deadlines, and Server Guidance](../01-concepts/04-budgets-deadlines-and-server-guidance.md)
- [Chapter 29 — Timeouts, Circuit Breakers, and Bulkheads](../../29-timeouts-circuit-breakers-and-bulkheads/README.md)
- [Chapter 57 — Error Handling Under Load and at Scale](../../../part-22-design-decisions/57-error-handling-under-load-and-at-scale/README.md)
