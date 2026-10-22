# Chapter 29 — Do's and Don'ts

> Part XI · Chapter 29 · All sections

A condensed rule set distilled from the chapter. Use it as a resilience review checklist.

## Timeouts and deadlines

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set a connect, request, and operation timeout | Rely on the OS default |
| Propagate the remaining budget | Reset a fresh timeout per hop |
| Clamp downstream to `min(config, remaining)` | Pass a timeout larger than the budget |
| Reject when remaining < 50–100ms | Start work that cannot finish |
| Cancel in-flight work on timeout | Abandon it and keep the connection |
| Give cleanup its own short timeout | Reuse the expired deadline |

## Circuit breakers

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Count timeouts, `5xx`, `429`, connection errors | Count every non-2xx |
| Open on a failure *rate* with a minimum sample | Open on one failure |
| Use a sliding window | Use a boundary-sensitive tumbling window |
| Jitter and grow the cooldown | Probe at a fixed interval |
| Limit half-open probes | Send full traffic on probe |
| Require consecutive successes to close | Close after one success |
| Check the breaker before every attempt | Check once outside the retry loop |
| Export state and transition metrics | Only log on open |

## Bulkheads

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Partition by dependency and tenant | Share one pool for everything |
| Derive limits from Little's Law | Guess a round number |
| Bound the queue | Let it grow unbounded |
| Reject with `503`/`429` + `Retry-After` | Accept work that will time out |
| Keep 20–30% pool headroom | Run at 100% utilization |
| Evict idle tenant state | Leak a semaphore per tenant |

## Admission control

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Reject doomed requests before starting | Queue them and time out later |
| Shed low-priority work first | Treat all traffic equally |
| Check capacity before enqueueing | Discover overload after the fact |
| Return a retry hint | Return a bare `500` |

## Combining mechanisms

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Order: deadline → breaker → bulkhead → call → retry → fallback | Retry before checking the breaker |
| Keep one retry owner per path | Let gateway and service both retry |
| Hold a bulkhead slot only during the call | Hold it across backoff |
| Bound worst-case calls = retry attempts | Accept `attempts^layers` amplification |
| Document worst-case latency | Assume timeouts are additive-safe |
| Write one policy per dependency | Rely on tribal knowledge |

## Fallbacks and errors

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Surface `CircuitOpenError` with `retryAfterMs` | Treat open as an unknown failure |
| Fail closed for payments and auth | Degrade past correctness |
| Fail open only for optional features | Hide a failed dependency behind `200` |
| Distinguish timeout from cancellation | Report client aborts as outages |
| Include a correlation id | Leak internal hostnames/stack traces |

## Policy and operations

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep policy in code/config, reviewed | Keep it in a wiki only |
| Review worst-case latency and load | Test only the happy path |
| Load-test with a failing dependency | Assume failure behavior from the happy path |
| Alert on open breakers and queue depth | Only alert on request error rate |
| Revisit limits as latency changes | Set them once and forget |
