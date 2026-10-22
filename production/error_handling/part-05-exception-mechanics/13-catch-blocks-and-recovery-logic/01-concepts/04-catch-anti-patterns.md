# Catch Anti-Patterns

> Part V · Chapter 13 · Sections 13.9, 13.10, 13.11, 13.12, 13.13 · _Estimated reading time: 16 min_
> **Prerequisite:** [Recovery Inside Catch](./03-recovery-inside-catch.md)

## In one sentence

The five classic catch defects — **empty catch, broad suppression, repeated catch/rethrow, errors
inside recovery, and unbounded recursion** — all convert loud failures into silent or catastrophic
ones, and each has a mechanical fix.

## Why this matters in production

These patterns pass code review because they *look* careful — a `catch` is present, so the code
"handles" errors. In practice they hide outages, mask bugs, amplify logs, and occasionally crash
the process via stack overflow. Knowing their signatures lets you find them by grep.

## Core concept

| Anti-pattern | Look for | Consequence |
| ------------ | -------- | ----------- |
| **Empty catch** (13.9) | `catch {}`, `except: pass` | Failure vanishes |
| **Broad suppression** (13.10) | `catch (e)` / `catch (Exception)` | Bugs, cancellation, outages hidden |
| **Repeated catch/rethrow** (13.11) | Catch-log-rethrow at every layer | Log flood; no added value |
| **Errors in recovery** (13.12) | Recovery throws unhandled | Secondary failure masks primary |
| **Recursive recovery** (13.13) | Retry inside retry, unbounded | Stack overflow / livelock |

### Empty catch (13.9)

No action, no log, no rethrow. Fix: delete it, or replace with an explicit, justified outcome
(e.g. best-effort cleanup where failure is truly harmless — and add a comment saying why).

### Avoiding broad suppression (13.10)

Catching a supertype (or bare `except`) intercepts unrelated errors. Fix: catch specific types;
keep an unknown branch that rethrows (Chapter 13.5).

### Avoiding repeated catch/rethrow (13.11)

The "log and rethrow at every layer" pattern produces N log lines per failure and no extra
information. Fix: catch where you add meaning; log once at the boundary.

### Errors in recovery (13.12)

Recovery code runs on the failure path and can itself fail. If that failure is unhandled, it
replaces the primary error. Fix: wrap recovery in its own try; attach its failure as **suppressed**;
preserve the primary (Chapter 14.13).

### Preventing recursion (13.13)

Recovery that calls the operation that failed, without a bound, can recurse:
- `f()` catches and retries `f()` with no attempt limit → infinite.
- A fallback that throws the same error and is caught by the same handler → loop.
Fix: bound attempts/deadline; make the retry a loop with a counter, not recursion; ensure the
fallback cannot re-enter the same catch.

## How it works (mechanics)

Why empty catch is so dangerous: it terminates propagation without producing any observable. The
error's cause chain is garbage-collected; nothing records it. The only fix is to *not* stop there.

```text
throw → catch {} → nothing recorded, nothing returned, caller continues with bad assumptions
```

Why repeated catch/rethrow floods: each layer independently decides to "log the error". With a
4-layer stack that is 4 lines; at 10k RPS that is 40k lines/s for one outage.

Why recursion happens: recovery is written as "call the function again", and the function's catch
calls recovery again. Without a guard, the stack grows until overflow (or the runtime's retry
policy is unbounded).

## Worked example

```ts
// ❌ Empty catch
try { await cleanup(); } catch {}

// ✅ Explicit: best-effort cleanup that truly cannot fail the request
try {
  await cleanup();
} catch (err) {
  logger.warn({ err }, "cleanup failed; ignoring (best effort)"); // observable, intentional
}
```

```ts
// ❌ Repeated catch/rethrow at every layer
async function repo() { try { /*...*/ } catch (e) { log(e); throw e; } }
async function domain() { try { await repo(); } catch (e) { log(e); throw e; } }
async function service() { try { await domain(); } catch (e) { log(e); throw e; } }
// → 3 identical logs for one failure

// ✅ Add context where meaningful; log once at the boundary
async function domain() {
  try { return await repo(); }
  catch (e) { throw new OrderStoreError("load order", { cause: e }); } // no log here
}
```

```ts
// ❌ Recursive recovery with no bound
async function fetchWithFallback(url: string): Promise<Data> {
  try { return await fetch(url); }
  catch (e) { return fetchWithFallback(url); } // infinite recursion on permanent failure
}

// ✅ Bounded retry loop with a final error
async function fetchWithRetry(url: string, max = 3): Promise<Data> {
  let lastErr: unknown;
  for (let i = 1; i <= max; i++) {
    try { return await fetch(url); }
    catch (e) { lastErr = e; if (!isTransient(e)) break; await sleep(backoff(i)); }
  }
  throw new FetchFailed(url, { cause: lastErr, attempts: max });
}
```

```ts
// ❌ Recovery failure replaces the primary
try { await charge(); }
catch (e) {
  await refund();               // if this throws, `e` is lost
  throw e;
}

// ✅ Preserve both; primary stays primary
try { await charge(); }
catch (e) {
  try { await refund(); }
  catch (refundErr) {
    throw new CheckoutFailed("charge failed and refund failed", {
      cause: e, suppressed: refundErr,
    });
  }
  throw e; // refunded, but the operation still failed
}
```

## Key data / numbers

- **Stack overflow**: unbounded recursion throws `RangeError: Maximum call stack size exceeded`
  (JS) or `RecursionError` (Python), or exhausts the goroutine stack (Go grows until it hits the
  1 GB default limit, then panics).
- **Retry attempts**: choose a small cap (commonly 3–5); unlimited retries is a denial-of-service
  against your own dependency and yourself.
- **Log amplification**: N layers × M RPS = N·M lines/s per error; keep N = 1 at the boundary.

## Real-world use case — Acme SaaS

Acme's `AgentRun` had a "self-healing" retry that recursively called the whole agent step on any
error. When the LLM provider returned a permanent `401` (revoked key), the recursion retried until
the worker ran out of stack and crashed — taking down the whole worker process and every other
tenant's run with it. They replaced recursion with a bounded loop, classified `401` as permanent,
and moved the retry to the job layer. The worker never crashed again.

## Trade-offs

| Pattern | Short-term appeal | Long-term cost |
| ------- | ----------------- | -------------- |
| Empty catch | "Never crashes" | Undiagnosable corruption |
| Broad catch | Fewer crash paths | Hides bugs and cancellation |
| Log-rethrow everywhere | "Visibility" | Log flood, no signal |
| Recursive recovery | Compact code | Overflow / livelock |
| Unhandled recovery error | Looks simple | Primary cause erased |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make every catch observable or purposeful | `catch {}` |
| Catch specific types | `catch (Exception)` / bare `except` |
| Log once at the boundary | Log-and-rethrow at every layer |
| Wrap recovery in its own try | Let recovery throw over the primary |
| Bound retries in a loop | Recurse without a limit |

## Common mistakes

- **`catch { return null }`** — the "safe" default that hides failures.
- **Treating all catch-and-rethrow as harmless** — it doubles logs with no benefit.
- **Refund/cleanup inside catch with no guard** — one failure becomes two.
- **Assuming the retry loop terminates** — no counter, no deadline.
- **Catching `CancellationException`** and continuing — the user already left.

## Checklist

- [ ] No empty catch blocks (or each has a comment justifying harmlessness).
- [ ] No supertype-only catches without a rethrowing unknown branch.
- [ ] Logging happens once, at the boundary.
- [ ] Recovery errors are caught and attached as suppressed.
- [ ] Every retry is a bounded loop with a deadline.

## Related

- [When to Catch and When Not To](./01-when-to-catch-and-when-not.md)
- [Recovery Failure and Recursion](../02-deep-dive/02-recovery-failure-and-recursion.md)
- [Resource Cleanup and Failure-Safe Execution](../../14-resource-cleanup-and-failure-safe-execution/README.md)
- [Error-Handling Patterns and Anti-Patterns (Part XVII)](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
