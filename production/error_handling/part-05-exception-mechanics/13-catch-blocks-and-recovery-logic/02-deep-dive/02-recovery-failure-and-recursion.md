# Recovery Failure and Recursion

> Part V · Chapter 13 · Sections 13.12–13.16 (mechanics) · _Estimated reading time: 18 min_
> **Prerequisite:** [Recovery Inside Catch](../01-concepts/03-recovery-inside-catch.md)

## In one sentence

Recovery runs on the **failure path**, so it can fail too and can loop — you must wrap it, attach
its failure as **suppressed** while preserving the primary, and bound every retry so it always
terminates.

## Why this matters in production

Two failure modes dominate recovery incidents. First, the "double fault": the operation fails,
the recovery (refund, rollback, cleanup) also fails, and the recovery error overwrites the
original — you no longer know what actually went wrong. Second, "recovery recursion": retry logic
written as recursion with no bound, which overflows the stack or livelocks the worker. Both are
preventable with a small amount of structure.

## Core concept

### Errors in recovery logic (13.12)

Recovery is code. It can fail because:

- the fallback dependency is also down (calling a cache that is unreachable),
- the compensating action is invalid (refunding a charge that never settled),
- the resource is gone (the connection used for rollback is dead).

When recovery fails, you now have **two** errors. The caller cares most about the **primary**; the
recovery failure is diagnostic. Keep both, in that order.

### Preventing recursion (13.13)

Recursion arises when:

1. **Retry calls the failing function** (`retry(work)` where `work` calls `retry`), or
2. **The fallback re-enters the catch**, or
3. **A global handler re-runs the request** on error.

Any of these without a bound grows the stack or spins forever. Bounds are: max attempts, total
deadline, and a "no re-entry" guard for the same operation.

## How it works (mechanics)

### Preserving the primary with suppressed errors

Java has first-class `addSuppressed`:

```java
try {
    charge();
} catch (Exception primary) {
    try {
        refund();                       // recovery
    } catch (Exception secondary) {
        primary.addSuppressed(secondary); // attach, do NOT throw
    }
    throw primary;                      // primary remains the reported failure
}
```

Python surfaces both via the implicit `__context__` / explicit `__cause__` when recovery runs
inside `except`:

```python
try:
    charge()
except Exception as primary:
    try:
        refund()
    except Exception as secondary:
        raise CheckoutFailed("charge failed; refund failed") from primary
        # secondary is attached as __context__ automatically
    raise  # re-raise the primary
```

Node/TS has no built-in suppressed list; carry it explicitly:

```ts
try { await charge(); }
catch (primary) {
  let suppressed: unknown;
  try { await refund(); }
  catch (secondary) { suppressed = secondary; }
  throw new CheckoutFailed("charge failed", { cause: primary, suppressed });
}
```

Go joins with `errors.Join` (1.20+):

```go
if err := charge(); err != nil {
    primary := err
    if rerr := refund(); rerr != nil {
        return errors.Join(primary, fmt.Errorf("refund failed: %w", rerr))
    }
    return primary
}
```

### Bounding retries

```text
attempts ≤ max
elapsed   ≤ deadline
retry only if transient AND idempotent
reset state between attempts
```

A correct retry is a **loop with counters**, not a recursive call:

```ts
async function withRetry<T>(op: () => Promise<T>, opts: { max: number; deadlineMs: number }) {
  const start = Date.now();
  let lastErr: unknown;
  for (let attempt = 1; attempt <= opts.max; attempt++) {
    try { return await op(); }
    catch (err) {
      lastErr = err;
      if (!isTransient(err)) throw err;                       // permanent → stop
      if (Date.now() - start >= opts.deadlineMs) break;       // deadline → stop
      await sleep(backoffWithJitter(attempt));
    }
  }
  throw new RetryExhausted({ cause: lastErr, attempts: opts.max });
}
```

A recursion *guard* for fallbacks that could re-enter:

```ts
const inRecovery = new WeakSet<object>();

async function recover(ctx: object, err: unknown) {
  if (inRecovery.has(ctx)) {
    throw new RecoveryLoopDetected({ cause: err }); // refuse to recurse
  }
  inRecovery.add(ctx);
  try {
    await doRecovery(ctx);
  } finally {
    inRecovery.delete(ctx);
  }
}
```

## Worked example — the double fault, fixed

```ts
// ❌ Before: refund failure overwrites the charge failure; also can recurse
async function checkout(cmd: CheckoutCmd) {
  try {
    return await charge(cmd);
  } catch (err) {
    await refund(cmd);   // if this fails, `err` is lost
    throw err;
  }
}

// ✅ After: primary preserved, secondary suppressed, no recursion
async function checkout(cmd: CheckoutCmd) {
  try {
    return await charge(cmd);
  } catch (primary) {
    try {
      await refund(cmd);
    } catch (secondary) {
      // Both are recorded; the charge failure is what the caller needs.
      throw new CheckoutFailed("charge failed; refund also failed", {
        cause: primary,
        suppressed: secondary,
        orderId: cmd.orderId,
      });
    }
    throw primary; // refunded successfully, but checkout still failed
  }
}
```

Log (structured) shows both, with the primary first and clearly identified as the cause.

## Key data / numbers

- **Java `addSuppressed`** — introduced in Java 7 specifically for try-with-resources and
  recovery; retrievable via `getSuppressed()`.
- **Go `errors.Join`** — Go 1.20+; returns a multi-error whose `errors.Is/As` traverse all
  children.
- **Node**: no native suppressed; carry an explicit field (e.g. `suppressed`) and have the logger
  serialize it.
- **Recursion limits**: JS ≈ 10k–15k frames (engine-dependent); Python default `recursionlimit`
  1000; Go goroutine stacks grow to a 1 GB default then panic.
- **Retry caps**: typical 3–5 attempts; pair with a **deadline** so slow dependencies cannot extend
  a request indefinitely.

## Real-world use case — Acme SaaS

Acme's saga for `Checkout` did `reserve → charge → confirm`, and on any error called `undo()` which
itself called the saga from the start on failure. A persistent inventory error caused `undo()`,
`undo()`, … until the worker stack overflowed and the pod restarted, replaying the whole thing. The
fix: (1) `undo()` performs a bounded, idempotent compensation only; (2) recovery failures are
attached as suppressed; (3) the retry loop lives in exactly one place and is bounded by attempts
and deadline. The pod stopped crash-looping.

## Trade-offs

| Recovery failure handling | Pros | Cons | When |
| ------------------------- | ---- | ---- | ---- |
| Let recovery error propagate | Simple | Primary cause lost | Never for compensation |
| Suppress (attach to primary) | Keeps both | Needs a suppressed store | Java, Go; TS/Python custom |
| Log secondary, throw primary | Simple in all languages | Secondary not structured | Acceptable if logged well |
| Return a combined error | One object | Bigger type; must design | Rich diagnostics needed |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Wrap recovery in its own try | Let recovery throw over the primary |
| Attach recovery failure as suppressed | Discard the recovery failure |
| Bound retries by attempts AND deadline | Retry forever |
| Use a loop, not recursion | Call the failing function again recursively |
| Guard fallbacks against re-entry | Let the fallback re-enter the same catch |

## Common mistakes

- **No guard on recursive retry** — hidden stack overflow under load.
- **Throwing the recovery error** — the wrong error reaches the caller.
- **Retrying without a deadline** — a slow dependency stalls the request.
- **"Self-healing" that re-runs the whole workflow** — re-introduces side effects.
- **Assuming recovery always succeeds** — the second fault is the interesting one.

## Checklist

- [ ] Every recovery block is wrapped in its own try.
- [ ] Recovery failures are attached as suppressed (or logged structurally).
- [ ] The primary error is what is thrown/returned.
- [ ] Retries are loop-based, bounded by attempts and deadline.
- [ ] Fallbacks have a re-entry guard.

## Related

- [Recovery Inside Catch](../01-concepts/03-recovery-inside-catch.md)
- [Catch Anti-Patterns](../01-concepts/04-catch-anti-patterns.md)
- [Errors During Cleanup (Part XXIII)](../../../part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)
- [Retry Policies (Part XI)](../../../part-11-retry-and-resilience/27-retry-policies/README.md)
