# Deadline Propagation

> Part XI · Chapter 29 · Sections 29.2–29.4, 29.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [Why Timeouts and Deadlines](../01-concepts/01-why-timeouts-and-deadlines.md)

## In one sentence

A deadline is a **shrinking budget that travels with the request**; every hop must compute
`remaining = deadline − now`, clamp its timeout to that value, and refuse work that can no longer
finish.

## Why this matters in production

Per-hop timeouts look reasonable in isolation and compose terribly. A 30s gateway, a 20s service, and
a 15s repository timeout mean a client can wait 30s while the server has already done 35s of work it
will never return. Deadline propagation keeps the *whole* call inside the caller's budget, and the
early rejection it enables is one of the cheapest forms of load protection you can add.

## The budget model

```text
client deadline: D
  gateway:  remaining = D - now
  service:  remaining = min(received_deadline, D) - now
  repo:     remaining = received_deadline - now
  provider: remaining = received_deadline - now - safety_margin
```

Every layer subtracts its own elapsed time. No layer invents a fresh budget.

### Concrete example

```text
t=0.00  client sets deadline t=10.00s
t=0.05  gateway receives; remaining 9.95s; calls service with deadline 10.00s
t=0.30  service receives; remaining 9.70s
t=0.35  service reads DB (bounded 2s)
t=2.40  DB done; remaining 7.60s
t=2.45  service calls provider with timeout min(5s, 7.60s - 0.5s) = 5s
t=7.50  provider times out; remaining 2.50s
t=7.55  retry? next backoff 0.4s + timeout 2.1s = 2.5s → no room → fail
t=7.60  return 504 within the client's 10s budget
```

The client gets a response before its own timeout, and no work is started that cannot finish.

## Transport mechanisms

### gRPC

gRPC has first-class deadlines:

```go
ctx, cancel := context.WithTimeout(parentCtx, 5*time.Second)
defer cancel()
resp, err := client.GetUser(ctx, req)
```

The client serializes the deadline into the `grpc-timeout` header. The server's `ctx.Deadline()` is
the absolute time; use it directly rather than adding another timeout.

```go
func handler(ctx context.Context, req *pb.Request) (*pb.Response, error) {
    if dl, ok := ctx.Deadline(); ok && time.Until(dl) < 50*time.Millisecond {
        return nil, status.Error(codes.DeadlineExceeded, "no time left")
    }
    // derive a child timeout that cannot exceed the parent
    ctx, cancel := context.WithTimeout(ctx, time.Until(dl))
    defer cancel()
    return svc.Handle(ctx, req)
}
```

### HTTP

There is no standard HTTP deadline header. Common conventions:

| Header | Meaning |
| ------ | ------- |
| `X-Request-Deadline` | Absolute epoch milliseconds |
| `X-Request-Timeout-Ms` | Remaining budget in ms |
| `grpc-timeout` | gRPC only |
| `Request-Timeout` (some proxies) | Seconds |

Pick one convention internally and document it. If a caller does not send one, apply your own default
deadline at the edge.

```ts
function remainingFrom(req: Request, fallbackMs = 10_000): number {
  const raw = req.header("X-Request-Timeout-Ms");
  const ms = raw ? Number(raw) : fallbackMs;
  return Number.isFinite(ms) ? Math.max(0, ms) : fallbackMs;
}

function withDeadline<T>(fn: (signal: AbortSignal) => Promise<T>, remainingMs: number) {
  const c = new AbortController();
  const t = setTimeout(() => c.abort(), remainingMs);
  return fn(c.signal).finally(() => clearTimeout(t));
}
```

### Queues

A queued message may wait a long time before processing. Store the deadline **at enqueue time** and
check it at dequeue:

```json
{ "job_id": "j_1", "deadline_ms": 1730000000000, "payload": {} }
```

If `now > deadline_ms`, send the job to the DLQ or mark it expired instead of doing work whose result
is no longer wanted.

## Clamping

The central rule:

```text
effective_timeout = min(configured_timeout, remaining_budget - safety_margin)
```

- If `effective_timeout <= 0`, **do not call**.
- Reserve a safety margin for serialization and the response path (often 50–200ms).
- Never pass a timeout larger than the remaining budget "to be safe"; it guarantees a late failure.

```python
def clamp_timeout(configured_s: float, deadline: float, safety_s: float = 0.15) -> float:
    remaining = deadline - time.monotonic() - safety_s
    if remaining <= 0:
        raise DeadlineExceeded()
    return min(configured_s, remaining)
```

## Cancellation and cleanup

When a deadline expires:

1. Cancel the in-flight request (abort signal / context cancel).
2. Stop consuming the response body.
3. Release the bulkhead slot and connection.
4. Run cleanup (Chapter 14), bounded by a **separate short cleanup timeout**.
5. Return `504` (or `499` if the client disconnected) with a correlation id.

Do not let cleanup inherit the expired deadline; it would immediately fail. Use a fixed short budget
(e.g. 500ms) for cleanup.

## Worked example — nested retries with one deadline

```ts
async function handle(req: Request) {
  const deadline = Date.now() + remainingFrom(req);
  const attempts = 3;

  for (let i = 0; i < attempts; i++) {
    const remaining = deadline - Date.now();
    if (remaining < 100) throw new DeadlineExceeded();

    try {
      return await withDeadline(
        (signal) => provider.call(req.body, signal),
        Math.min(2_000, remaining),   // clamp per attempt
      );
    } catch (err) {
      if (!isRetryable(err) || i === attempts - 1) throw err;
      const delay = backoffDelay(i);
      if (Date.now() + delay + 100 >= deadline) throw err; // no room
      await sleep(delay);
    }
  }
}
```

## Key data / numbers

- Reserve **50–200ms** safety margin per hop for serialization.
- Minimum useful remaining time: **50–100ms**; below that, reject.
- gRPC: `grpc-timeout` header; absolute deadline in-process.
- HTTP convention: `X-Request-Timeout-Ms` (remaining) or `X-Request-Deadline` (absolute).
- Cleanup timeout: **500ms–1s**, independent of the expired deadline.
- Queue messages should carry an absolute `deadline_ms`.

## Real-world use case — Acme SaaS

Acme's gateway had a 30s timeout, the project service a 15s timeout, and the export API another 20s.
An export request could therefore run for 65s while the client had already given up at 30s, holding a
worker and writing to an S3 object nobody would read. The team switched to an edge deadline
(`X-Request-Timeout-Ms`), clamped every downstream call to the remaining budget, and stored absolute
deadlines on queued export steps. Average worker occupancy during large exports dropped by 38%, and
`504`s arrived within the client's budget instead of after it.

## Trade-offs

| Mechanism | Pros | Cons |
| --------- | ---- | ---- |
| Per-hop fixed timeout | Simple | Total exceeds client budget |
| Propagated deadline | Bounded total | Requires discipline |
| Absolute (epoch) | Robust to clock skew? No — needs synced clocks | Clock skew risk |
| Relative (remaining ms) | No clock-sync dependency | Must subtract per hop |

Use **relative remaining milliseconds** when clock skew is a concern; use absolute deadlines when
your infrastructure has reliable clock sync (NTP).

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Propagate remaining time | Reset a fresh timeout per hop |
| Clamp to `min(config, remaining)` | Use a timeout larger than the budget |
| Reject when remaining < minimum | Start doomed work |
| Cancel the in-flight request | Let it run after timeout |
| Use a separate cleanup timeout | Reuse the expired deadline |
| Store deadlines on queued work | Process stale messages |

## Common mistakes

- **Resetting the deadline** at a service boundary.
- **Ignoring `grpc-timeout`**, adding a new 5s timeout inside a 100ms budget.
- **No safety margin**, so serialization pushes past the deadline.
- **Cleanup using the expired context**, so it never runs.
- **Queue jobs without deadlines**, doing work for a result nobody wants.

## Checklist

- [ ] The edge assigns a deadline if none is provided.
- [ ] Every hop computes `remaining = deadline − now`.
- [ ] Timeouts are clamped to the remaining budget.
- [ ] Work is rejected below a minimum useful time.
- [ ] Cancellation aborts in-flight calls.
- [ ] Cleanup has its own short timeout.
- [ ] Queued messages carry an absolute deadline.

## Related

- [Why Timeouts and Deadlines](../01-concepts/01-why-timeouts-and-deadlines.md)
- [Admission Control and Combining Mechanisms](../01-concepts/04-admission-control-and-combining-mechanisms.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
- [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../../../part-05-exception-mechanics/14-resource-cleanup-and-failure-safe-execution/README.md)
