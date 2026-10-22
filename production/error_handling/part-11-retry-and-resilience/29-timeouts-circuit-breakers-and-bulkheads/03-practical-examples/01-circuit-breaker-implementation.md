# Circuit Breaker Implementation

> Part XI · Chapter 29 · Sections 29.5–29.9, 29.14 · _Estimated reading time: 24 min_
> **Prerequisite:** [Breaker State Machine](../02-deep-dive/01-breaker-state-machine.md)

## In one sentence

This is a **small, dependency-free circuit breaker** with a sliding failure window, jittered
exponential cooldown, serialized half-open probes, and enough metrics to see every transition.

## Why this matters in production

Breaker libraries exist, but the behavior that matters is in the policy: what counts as a failure,
how the window is computed, how probes are admitted, and what the caller sees when the breaker is
open. This implementation makes those decisions explicit and testable, and it composes with the retry
utility from Chapter 27 by exposing `isOpen()` and a `rejected` error.

## The implementation

```ts
export type BreakerState = "closed" | "open" | "half_open";
export type BreakerTransition = `${BreakerState}->${BreakerState}`;

export interface BreakerOptions {
  failureThreshold?: number;   // 0..1, e.g. 0.5
  minRequests?: number;        // e.g. 30
  windowMs?: number;           // e.g. 30_000
  baseCooldownMs?: number;     // e.g. 10_000
  maxCooldownMs?: number;      // e.g. 300_000
  closeAfterSuccesses?: number;// e.g. 3
  probeConcurrency?: number;   // e.g. 1
  isFailure?: (err: unknown) => boolean;
  now?: () => number;
  random?: () => number;
}

export class CircuitOpenError extends Error {
  constructor(readonly retryAfterMs: number) {
    super("circuit open");
    this.name = "CircuitOpenError";
    this.cause = { code: "CIRCUIT_OPEN", retryable: true, retryAfterMs };
  }
}

interface Sample { at: number; ok: boolean; }

export class CircuitBreaker {
  private state: BreakerState = "closed";
  private samples: Sample[] = [];
  private openedAt = 0;
  private openCount = 0;
  private probeSuccesses = 0;
  private probesInFlight = 0;

  private readonly failureThreshold: number;
  private readonly minRequests: number;
  private readonly windowMs: number;
  private readonly baseCooldownMs: number;
  private readonly maxCooldownMs: number;
  private readonly closeAfterSuccesses: number;
  private readonly probeConcurrency: number;
  private readonly isFailure: (err: unknown) => boolean;
  private readonly now: () => number;
  private readonly random: () => number;

  constructor(
    private readonly name: string,
    private readonly metrics: {
      state: (name: string, state: BreakerState) => void;
      transition: (name: string, t: BreakerTransition) => void;
      rejected: (name: string) => void;
    },
    opts: BreakerOptions = {},
  ) {
    this.failureThreshold = opts.failureThreshold ?? 0.5;
    this.minRequests = opts.minRequests ?? 30;
    this.windowMs = opts.windowMs ?? 30_000;
    this.baseCooldownMs = opts.baseCooldownMs ?? 10_000;
    this.maxCooldownMs = opts.maxCooldownMs ?? 300_000;
    this.closeAfterSuccesses = opts.closeAfterSuccesses ?? 3;
    this.probeConcurrency = opts.probeConcurrency ?? 1;
    this.isFailure = opts.isFailure ?? defaultIsFailure;
    this.now = opts.now ?? Date.now;
    this.random = opts.random ?? Math.random;
    metrics.state(name, this.state);
  }

  /** Check before each attempt; does not consume a probe. */
  isOpen(): boolean {
    this.maybeHalfOpen();
    return this.state === "open";
  }

  get currentState(): BreakerState {
    return this.state;
  }

  async exec<T>(fn: () => Promise<T>): Promise<T> {
    this.maybeHalfOpen();

    if (this.state === "open") {
      const retryAfterMs = this.cooldownMs() - (this.now() - this.openedAt);
      this.metrics.rejected(this.name);
      throw new CircuitOpenError(Math.max(0, retryAfterMs));
    }

    if (this.state === "half_open" && this.probesInFlight >= this.probeConcurrency) {
      this.metrics.rejected(this.name);
      throw new CircuitOpenError(500);
    }

    if (this.state === "half_open") this.probesInFlight++;

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      this.onFailure(err);
      throw err;
    } finally {
      if (this.state === "half_open") this.probesInFlight--;
    }
  }

  private onSuccess() {
    if (this.state === "half_open") {
      this.probeSuccesses++;
      if (this.probeSuccesses >= this.closeAfterSuccesses) this.close();
      return;
    }
    this.record(true);
    this.evaluate();
  }

  private onFailure(err: unknown) {
    if (!this.isFailure(err)) {
      // Not a dependency failure (e.g. 4xx): do not count it.
      if (this.state === "closed") this.record(true);
      return;
    }
    if (this.state === "half_open") {
      this.open("probe failed");
      return;
    }
    this.record(false);
    this.evaluate();
  }

  private record(ok: boolean) {
    const now = this.now();
    this.samples.push({ at: now, ok });
    const cutoff = now - this.windowMs;
    while (this.samples.length && this.samples[0].at < cutoff) this.samples.shift();
  }

  private evaluate() {
    if (this.state !== "closed") return;
    const total = this.samples.length;
    if (total < this.minRequests) return;
    const failures = this.samples.filter((s) => !s.ok).length;
    if (failures / total >= this.failureThreshold) this.open("failure rate");
  }

  private maybeHalfOpen() {
    if (this.state !== "open") return;
    if (this.now() - this.openedAt < this.cooldownMs()) return;
    this.transition("half_open");
    this.probeSuccesses = 0;
    this.probesInFlight = 0;
  }

  private open(reason: string) {
    this.openCount++;
    this.openedAt = this.now();
    this.samples = [];
    this.transition("open");
    void reason;
  }

  private close() {
    this.openCount = 0;
    this.probeSuccesses = 0;
    this.samples = [];
    this.transition("closed");
  }

  private cooldownMs(): number {
    const exp = Math.min(20, Math.max(0, this.openCount - 1));
    const base = Math.min(this.maxCooldownMs, this.baseCooldownMs * 2 ** exp);
    return base * (0.8 + this.random() * 0.4); // ±20% jitter
  }

  private transition(to: BreakerState) {
    if (this.state === to) return;
    const from = this.state;
    this.state = to;
    this.metrics.transition(this.name, `${from}->${to}`);
    this.metrics.state(this.name, to);
  }
}

function defaultIsFailure(err: unknown): boolean {
  const e = err as { status?: number; code?: string; name?: string };
  if (e?.code === "CIRCUIT_OPEN") return false;
  if (e?.name === "AbortError") return false;      // cancellation, not dependency failure
  if (typeof e?.status === "number") {
    if (e.status === 429) return true;
    if (e.status >= 500) return true;
    if (e.status >= 400) return false;             // 4xx is the caller's fault
  }
  return true;                                     // timeouts, connection errors
}
```

## Composing with retry

The breaker must be checked **before each attempt**, not just once outside the loop:

```ts
async function callWithResilience<T>(fn: () => Promise<T>) {
  return retry(
    async () => {
      if (stripeBreaker.isOpen()) {
        throw new CircuitOpenError(stripeBreaker.retryAfterMs());
      }
      return stripeBreaker.exec(fn);
    },
    { maxAttempts: 3, deadline: Date.now() + 8_000, perAttemptTimeoutMs: 2_000 },
    { isRetryable: (e) => e.retryable === true || e.code === "CIRCUIT_OPEN" },
  );
}
```

When the breaker opens mid-loop, the next iteration throws `CircuitOpenError`, which is retryable only
after the cooldown — so cap the deadline so retries cannot outlast it.

## Metrics wiring

```ts
const stripeBreaker = new CircuitBreaker("stripe", {
  state: (name, state) =>
    gauge.set({ dependency: name }, state === "closed" ? 0 : state === "half_open" ? 1 : 2),
  transition: (name, t) => counter.inc({ dependency: name, transition: t }),
  rejected: (name) => counter.inc({ dependency: name, event: "rejected" }),
}, { failureThreshold: 0.5, minRequests: 30, windowMs: 30_000 });
```

Alert on `state == 2` (open) for longer than the expected recovery window, and on a high rate of
`open->half_open->open` transitions (flapping).

## Testing the transitions

```ts
let t = 0;
const breaker = new CircuitBreaker("test", noopMetrics, {
  minRequests: 3, failureThreshold: 0.5, windowMs: 10_000,
  baseCooldownMs: 1_000, closeAfterSuccesses: 2,
  now: () => t, random: () => 0.5,
});

// Open after 2/3 failures.
for (const ok of [false, true, false]) {
  await breaker.exec(async () => { if (!ok) throw { status: 503 }; return 1; }).catch(() => {});
}
expect(breaker.currentState).toBe("open");

// Half-open after cooldown.
t += 1_000;
expect(breaker.isOpen()).toBe(false);

// Close after 2 probe successes.
await breaker.exec(async () => 1);
await breaker.exec(async () => 1);
expect(breaker.currentState).toBe("closed");
```

## Key data / numbers

- Failure threshold **0.5**, minimum **30** requests, window **30s**.
- Base cooldown **10s**, exponential to **5min**, ±20% jitter.
- Half-open: **1** concurrent probe, **3** consecutive successes to close.
- Count `429`, `5xx`, timeouts, connection errors; exclude `4xx` and cancellation.
- Open response: `CircuitOpenError` with `retryAfterMs`.

## Real-world use case — Acme SaaS

Acme wrapped its LLM provider with this breaker. During a provider incident, failures crossed 50%
within ~5s; the breaker opened and the `AgentRun` path switched to a cached/fallback response instead
of sending 3 retries per request. When the provider recovered, serialized probes closed the breaker
after three successes, and traffic resumed gradually. Provider `429` volume during the incident fell
by ~70% compared with the previous unbounded-retry behavior.

## Trade-offs

| Choice | Pros | Cons |
| ------ | ---- | ---- |
| Serial probes | Safest recovery | Slower |
| Limited probes (2–5) | Faster | More load during recovery |
| Short window | Fast reaction | Noise |
| Long cooldown | Protects dependency | Slow recovery |
| Count `429` | Protects overloaded provider | Opens during rate spikes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Check the breaker before each attempt | Check once outside a retry loop |
| Exclude `4xx` and cancellation | Count every non-2xx |
| Jitter the cooldown | Use a fixed interval |
| Serialize probes | Send full traffic on half-open |
| Export state metrics | Log only open events |
| Test transitions with an injected clock | Depend on real time |

## Common mistakes

- **One breaker per request**, so the window never fills.
- **Rejected calls counted as failures**, keeping the breaker open forever.
- **Half-open allowing all traffic**, causing a recovery stampede.
- **Reset cooldown on every open**, probing too frequently.
- **No failure predicate**, so validation errors trip the breaker.

## Checklist

- [ ] One breaker instance per dependency per process.
- [ ] Sliding window with min requests and failure rate.
- [ ] Failure predicate excludes `4xx`/cancellation.
- [ ] Cooldown grows and is jittered.
- [ ] Half-open probes are limited with a close threshold.
- [ ] Checked before every retry attempt.
- [ ] State and transition metrics exported.
- [ ] Transitions tested deterministically.

## Related

- [Breaker State Machine](../02-deep-dive/01-breaker-state-machine.md)
- [Circuit Breaker States and Conditions](../01-concepts/02-circuit-breaker-states-and-conditions.md)
- [Timeouts and Bulkheads for Acme](./02-timeouts-and-bulkheads-for-acme.md)
- [Chapter 27 — Retry Policies](../../27-retry-policies/README.md)
