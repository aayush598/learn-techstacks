# Reusable Retry Utility with Jitter

> Part XI · Chapter 27 · Section 27.25 (and all) · _Estimated reading time: 24 min_
> **Prerequisite:** [Attempts, Delays, and Jitter](../01-concepts/03-attempts-delays-and-jitter.md)

## In one sentence

A good retry utility is **small, policy-driven, and boring**: it takes an operation, a classification
function, a backoff schedule, a deadline, and an optional budget, and it returns either the result or
a terminal error that still carries the last real cause.

## Why this matters in production

Most retry bugs are copy-paste bugs. Each service writes its own loop; one forgets jitter, one forgets
the deadline, one retries everything, one throws away the cause. A shared utility makes the *correct*
path the *easy* path and gives every caller the same observable behavior: one span per attempt, one
metric per outcome, one error shape at exhaustion. It also gives you a single place to enforce the
retry budget and to audit amplification.

## Design goals

| Goal | Implementation |
| ---- | -------------- |
| Retry only what the caller classifies | `isRetryable(err)` callback |
| Bound attempts | `maxAttempts` (counts the first try) |
| Bound time | absolute `deadline` + `perAttemptTimeoutMs` |
| Spread load | full/equal jitter |
| Honor server hints | `retryAfterMs(err)` callback |
| Bound fleet load | optional `budget.tryAcquire()` |
| Preserve failure | `RetryExhaustedError` with `cause` and attempt metadata |
| Observe | `onAttempt`, `onRetry` hooks (traces + metrics) |

## The utility

```ts
// retry.ts — dependency-free; inject sleep/clock/random for tests.

export type Jitter = "none" | "full" | "equal";

export interface RetryPolicy {
  maxAttempts: number;              // includes the first attempt
  deadline: number;                 // absolute epoch ms
  perAttemptTimeoutMs: number;
  baseDelayMs?: number;
  capDelayMs?: number;
  multiplier?: number;
  jitter?: Jitter;
  random?: () => number;            // injectable for tests
  sleep?: (ms: number) => Promise<void>;
  now?: () => number;
}

export interface RetryHooks<E> {
  isRetryable: (err: E) => boolean;
  retryAfterMs?: (err: E) => number | undefined;
  budget?: { tryAcquire: () => boolean };
  onAttempt?: (attempt: number, err?: E) => void;
  onRetry?: (attempt: number, delayMs: number, err: E) => void;
}

export class RetryExhaustedError<E = unknown> extends Error {
  constructor(
    readonly attempts: number,
    readonly elapsedMs: number,
    readonly lastError: E,
  ) {
    super(`retry exhausted after ${attempts} attempt(s)`);
    this.name = "RetryExhaustedError";
    this.cause = lastError;
  }
}

const defaultSleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

export function computeDelay(attempt: number, p: RetryPolicy): number {
  const base = p.baseDelayMs ?? 200;
  const cap = p.capDelayMs ?? 10_000;
  const mul = p.multiplier ?? 2;
  const jitter = p.jitter ?? "full";
  const rand = p.random ?? Math.random;

  const raw = Math.min(cap, base * Math.pow(mul, attempt));
  if (jitter === "none") return raw;
  if (jitter === "equal") return raw / 2 + rand() * (raw / 2);
  return rand() * raw; // full jitter
}

export async function retry<T, E = unknown>(
  op: (signal: AbortSignal) => Promise<T>,
  policy: RetryPolicy,
  hooks: RetryHooks<E>,
): Promise<T> {
  const now = policy.now ?? Date.now;
  const sleep = policy.sleep ?? defaultSleep;
  const started = now();
  let lastError: E | undefined;
  let attempts = 0;

  for (let attempt = 0; attempt < policy.maxAttempts; attempt++) {
    const remaining = policy.deadline - now();
    if (remaining <= 0) break;

    attempts++;
    hooks.onAttempt?.(attempt);

    try {
      return await withTimeout(op, Math.min(policy.perAttemptTimeoutMs, remaining));
    } catch (err) {
      const e = err as E;
      lastError = e;

      const isLast = attempt === policy.maxAttempts - 1;
      if (isLast || !hooks.isRetryable(e)) break;

      const hinted = hooks.retryAfterMs?.(e);
      const delay = Math.max(computeDelay(attempt, policy), hinted ?? 0);

      const remainingAfter = policy.deadline - now();
      // Must fit the delay plus at least a minimal attempt.
      if (delay + 1 >= remainingAfter) break;

      if (hooks.budget && !hooks.budget.tryAcquire()) break;

      hooks.onRetry?.(attempt + 1, delay, e);
      await sleep(delay);
    }
  }

  throw new RetryExhaustedError<E>(attempts, now() - started, lastError as E);
}

function withTimeout<T>(
  op: (signal: AbortSignal) => Promise<T>,
  ms: number,
): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  return op(controller.signal).finally(() => clearTimeout(timer));
}
```

## Using it at a boundary

```ts
const charge = (input: ChargeInput, key: string) =>
  retry(
    (signal) => gateway.charge({ ...input, idempotencyKey: key }, { signal }),
    {
      maxAttempts: 3,
      deadline: Date.now() + 8_000,
      perAttemptTimeoutMs: 2_000,
      baseDelayMs: 250,
      capDelayMs: 2_000,
      jitter: "full",
    },
    {
      isRetryable: (e) => e.retryClass === "retryable",
      retryAfterMs: (e) => e.retryAfterMs,
      budget: paymentRetryBudget,
      onAttempt: (n) => span.setAttribute("retry.attempt", n),
      onRetry: (n, ms, e) => log.warn({ attempt: n, delayMs: ms, code: e.code }, "retrying"),
    },
  );
```

Note what the caller does **not** do: it does not decide jitter, does not parse `Retry-After`, does
not count attempts, and does not rebuild the error. Those are policy concerns owned by the utility.

## Why the deadline check comes before sleep

The loop computes the delay, then verifies it fits before sleeping. This prevents the common bug:

```ts
// Wrong: sleeps past the deadline, then fails anyway.
await sleep(delay);
if (Date.now() > deadline) throw err;
```

The correct order fails fast, freeing the worker and returning an honest error.

## Testability

Inject the clock, sleep, and RNG so tests are deterministic:

```ts
const delays: number[] = [];
await expect(
  retry(
    async () => { throw { retryClass: "retryable", code: "X" }; },
    {
      maxAttempts: 4,
      deadline: 10_000,
      perAttemptTimeoutMs: 1_000,
      random: () => 0.5,
      now: () => 0,
      sleep: async (ms) => { delays.push(ms); },
    },
    { isRetryable: (e) => e.retryClass === "retryable" },
  ),
).rejects.toBeInstanceOf(RetryExhaustedError);

expect(delays).toEqual([100, 200, 400]); // full jitter × 0.5
```

Testing policy — not implementation details — is what keeps the utility trustworthy as callers grow.

## Key data / numbers

- `maxAttempts` includes the initial call; 3 means 1 + 2 retries.
- Default schedule: `base=200ms`, `multiplier=2`, `cap=10s`, full jitter.
- Deadline must exceed `attempts × perAttempt + Σ delays` for the retries to be meaningful.
- Provider `Retry-After` clamps the delay upward, never downward.
- Every attempt should emit one trace span and one outcome metric.

## Real-world use case — Acme SaaS

Acme had 14 hand-written retry loops across its services. Three lacked jitter; two retried `422`s;
one slept after its final attempt; none preserved the cause. After adopting a shared utility, the 14
loops became 14 policy declarations. During the next provider incident, retries dropped by 60%
(budget + correct classification), and every exhaustion log carried `code`, `attempts`, `elapsedMs`,
and the provider's `request-id`. Mean time to diagnose dependency incidents fell from ~40 minutes to
under 10.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Shared utility | Consistent, testable | One more abstraction to own |
| Callback-based policy | Flexible per call site | Easy to misuse |
| Budget inside utility | Enforced automatically | Shared mutable state |
| Built-in timeout | Bounds each attempt | Might duplicate caller timeout |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep policy declarative | Encode retries as nested `while` loops |
| Inject clock/RNG/sleep | Use real time in unit tests |
| Return structured exhaustion | Throw a fresh generic error |
| Place budget at the utility | Re-implement budgets per caller |
| Emit an attempt hook | Log only the final outcome |

## Common mistakes

- **`maxAttempts` treated as retries.** Off-by-one doubles call volume.
- **Wrapping the whole operation including serialization** in the retry, repeating non-network work.
- **Passing a new idempotency key per attempt.** It defeats duplicate detection.
- **Not propagating the abort signal**, so a timed-out attempt keeps running.
- **Sleeping without checking the deadline**, delaying the terminal error.

## Checklist

- [ ] Policy declares attempts, deadline, per-attempt timeout, base, cap, jitter.
- [ ] `isRetryable` is the only retryability check.
- [ ] The same idempotency key is reused across attempts.
- [ ] Abort signal is passed to the operation.
- [ ] Exhaustion preserves the last cause and attempt metadata.
- [ ] Clock, sleep, and RNG are injectable for tests.
- [ ] Budget and hooks are optional, not required, for simple callers.

## Related

- [Attempts, Delays, and Jitter](../01-concepts/03-attempts-delays-and-jitter.md)
- [Backoff and Jitter Math](../02-deep-dive/01-backoff-and-jitter-math.md)
- [Retries for DB, Providers, and Jobs](./02-retries-for-db-provider-and-jobs.md)
- [Chapter 28 — Idempotency and Duplicate-Operation Safety](../../28-idempotency-and-duplicate-operation-safety/README.md)
