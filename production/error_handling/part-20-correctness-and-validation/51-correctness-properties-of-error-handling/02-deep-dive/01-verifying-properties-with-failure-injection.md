# Verifying Properties with Failure Injection (51.1–51.18)

> Part XX · Chapter 51 · Deep dive · _Estimated reading time: 24 min_
> **Prerequisite:** [Determinism and Completeness (51.1–51.4)](../01-concepts/01-determinism-and-completeness.md)

## In one sentence

A correctness property is only real if you can **break it on demand** — failure injection is how you
turn "we handle errors" into a reproducible, automated proof.

## Why this matters in production

Most teams test the happy path and a handful of hand-picked errors (bad input, 404). The paths that
break production are the ones nobody injected: the connection that dies *between* two writes, the
provider that answers after the deadline, the worker killed mid-batch, the same webhook delivered
twice while the first copy is still processing.

Failure injection closes that gap systematically. You pick a **failure point**, a **fault mode**, and
an **oracle** (the assertion that tells you the property held), and you run the combination.

## Core concept

### The verification triple

```text
   FAILURE POINT          FAULT MODE            ORACLE
   (where)                (what)                (how you know it was handled)
   ────────────────────────────────────────────────────────────
   DB commit              connection reset      rows == 0, attempt recorded, outcome != success
   Stripe charge          timeout after effect  attempt.status == 'charged', no second charge
   worker loop            process killed        job resumes at checkpoint, no duplicate rows
   webhook handler        duplicate delivery    exactly one effect for N deliveries
```

If you cannot name the oracle, you do not have a test — you have a hope.

### Fault modes

Six modes cover the overwhelming majority of production failures:

| Mode | What it simulates | Typical mechanism |
| ---- | ----------------- | ----------------- |
| **Throw** | An operation returns an error | Wrapped dependency that throws a chosen error |
| **Delay / hang** | A timeout, a stalled network | Wrapper that sleeps past the deadline |
| **Crash** | Process death, OOM, `SIGKILL` | Kill the child process mid-operation |
| **Partial write** | A multi-step write that half-landed | Inject between two commits |
| **Duplicate** | At-least-once delivery | Deliver the same message N times |
| **Wrong data** | A provider returns success with garbage | Stub returning a malformed payload |

> ⚠️ **Hazard.** "Wrong data" is the mode most teams skip, and it is the mode behind the worst
> incidents: the provider returned `200` with an empty body, the code trusted it, and the system
> wrote zeros. Success is not a guarantee of validity.

### The matrix

For one operation with **7 failure points** and **6 fault modes**, you have **42 cells**. You do not
need all 42 to start. The pragmatic split:

| Priority | Cells | What you cover |
| -------- | ----- | -------------- |
| P0 | 7 × 1 (throw) | Every failure point throws its realistic error |
| P1 | 2 × 5 (delay, crash, duplicate) | The irreversible boundaries only: the charge, the commit, the delivery |
| P2 | remaining | Fill in over time |

Coverage is measured as **filled cells ÷ total cells**, per property, not per feature.

## How it works (mechanics)

### A seam you can inject into

Injection needs a seam. The cheapest seam is a **wrapper around the dependency**, not a hook
inside your business logic.

```ts
// A thin seam: every outbound call goes through one adapter interface.
export interface PaymentGateway {
  charge(input: ChargeInput): Promise<ChargeResult>;
}

export class FaultyGateway implements PaymentGateway {
  constructor(private inner: PaymentGateway, private faults: FaultPlan) {}

  async charge(input: ChargeInput): Promise<ChargeResult> {
    await this.faults.maybeDelay("stripe.charge");
    if (this.faults.shouldThrow("stripe.charge")) {
      throw this.faults.errorFor("stripe.charge");
    }
    if (this.faults.shouldReturnGarbage("stripe.charge")) {
      return { id: "", status: "succeeded", amountMinor: 0 } as ChargeResult;  // wrong data
    }
    return this.inner.charge(input);
  }
}
```

Because the seam is at the adapter, your production code is untouched — the fault plan is a test
fixture, not a runtime flag. (A runtime "chaos mode" flag in production code is a different tool,
with different risks; see [Chapter 41](../../../part-15-distributed-failures/41-process-runtime-and-resource-failures/README.md).)

### One test per property, not per scenario

Write tests **per property**, parameterized over failure points. The test name says which property
is being checked, and the fixture supplies the failure point.

```ts
describe("51.9 — no duplicate side effects", () => {
  it.each(caseIds)("charge for %s produces exactly one Stripe charge", async (caseId) => {
    const harness = await harnessFor(caseId, { faults: { duplicateAfterCommit: true } });
    await harness.runCheckout();

    expect(await harness.countStripeCharges()).toBe(1);      // the oracle
    expect(await harness.subscriptionCount()).toBe(1);
  });
});

describe("51.14 — partial failures are accurate", () => {
  it("reports attempted == succeeded + failed + cancelled", async () => {
    const harness = await harnessFor("batch-write", { faults: { throwOnBatch: [3, 7] } });
    const result = await harness.run();

    expect(result.succeeded + result.failed.length + result.cancelled).toBe(result.total);
    expect(result.outcome).toBe("partial");
  });
});
```

### Property-based testing for error handling

Randomized input finds the paths you did not enumerate. Three generators matter:

| Generator | What it varies | Typical property it breaks |
| --------- | -------------- | -------------------------- |
| Error generator | Which error, which layer sees it first | Classification determinism (51.3) |
| Ordering generator | Which of N concurrent requests wins | At-most-once effects (51.9, 51.13) |
| Timing generator | Where the cancellation/fault lands relative to commits | Cancellation semantics (51.15) |

```ts
// Deterministic seeds make a failure reproducible from a CI log line.
function* seedFrom(runId: string) {
  let h = 2166136261;
  for (const ch of runId) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); }
  return h >>> 0;
}

it("51.3 — classification is deterministic for any error", () => {
  for (const seed of [1, 2, 3, 42, 1000]) {
    const err = generateError(seed);
    const a = classify(err);
    const b = classify(err);
    expect(a).toEqual(b);
    expect(a.code).toBe(classify(cloneError(err)).code);
  }
});
```

### Proving the negative properties

Some properties cannot be shown by a positive test; they need a *negative* assertion or an
invariant that must hold at all times.

| Property | Negative proof |
| -------- | -------------- |
| 51.2 No silent discard | Reconciliation query returns 0 unmatched error events |
| 51.6 Retries terminate | Attempt counter is observable and never exceeds the cap |
| 51.7 Cleanup occurs | Pool checked-out count returns to 0 after every scenario |
| 51.12 No unbounded recursion | Fallback/translate depth counters stay below the cap |
| 51.15 Cancellation not success | No recorded outcome equals `success` for a cancelled operation |

```ts
// 51.7 as an invariant, checked after every injected failure.
afterEach(async () => {
  expect(pool.checkedOutCount()).toBe(0);
  expect(openTransactionCount()).toBe(0);
  expect(danglingTimersCount()).toBe(0);
});
```

## Worked example — Checkout injection plan

For `Checkout` with **7 failure points**:

| ID | Failure point | Modes injected | Oracle |
| -- | ------------- | -------------- | ------ |
| FP-01 | Auth token refresh | throw, delay | 401 returned once; no charge attempted |
| FP-02 | Postgres `INSERT checkout_attempts` | throw, partial write | No orphan attempt row; outcome `failed` |
| FP-03 | Stripe charge (network) | delay (past deadline) | Outcome `unknown`; **exactly one** charge recorded by read-back |
| FP-04 | Stripe charge (success, response lost) | wrong data | No subscription created from a garbage response |
| FP-05 | Postgres `UPDATE status='charged'` | throw | Attempt stays `pending`; no duplicate charge on retry |
| FP-06 | Outbox publish | throw | Event published on retry; no duplicate `subscription.created` |
| FP-07 | Receipt email | throw | Email failure does not roll back the subscription; email retried separately |

Two findings from running the matrix, both invisible before:

1. **FP-03 + FP-05**: timeout on the charge, then failure on the status update. The old code
   retried the whole flow and charged twice (51.9). The fix was an idempotency key + read-back.
2. **FP-04**: Stripe returned `200` with an empty body. The old code wrote `amountMinor: 0` and
   created a free subscription. This is the "wrong data" mode, and it had never been tested.

## Key data / numbers

- **Fault modes: 6** (throw, delay/hang, crash, partial write, duplicate, wrong data).
- **Priority cells**: P0 = *points* × 1; P1 = *irreversible points* × 5; P2 = remainder.
- **Seed discipline**: 5–10 fixed seeds per property test, plus one random seed reported in CI.
- **Oracle latency budget**: each injected scenario should complete in **< 2 s** in CI, so a full
  matrix stays under a minute.
- **Property-test runs**: 100–1 000 cases per property is typical; the value is in the *first*
  failing seed, which must be printed and reproducible.
- **Reconciliation SLA**: the "unmatched error events" query should be part of every deploy, and
  the count must be **0**.

## Real-world use case — Acme SaaS `WebhookIngest`

Acme's CI had 400 tests, none of which injected a failure. The staging environment produced
duplicate subscription activations roughly once a fortnight, always "in production only".

The team wrote 12 injected scenarios across the 5 webhook failure points. Two failed on the first
run:

- **Duplicate delivery during processing**: two concurrent deliveries of `invoice.paid` both
  created a subscription, because the dedupe record was written *after* the effect. The fix was to
  insert the dedupe row first, in the same transaction as the effect (51.13).
- **Delay past the deadline**: the handler was still processing when the 10 s deadline expired, so
  Stripe retried while the first copy was still running — producing the same duplicate. The fix
  was a **fencing token** on the attempt row: the second copy's write was rejected because its
  token was stale (51.13, 51.16).

After the fix, duplicate activations were zero for two consecutive months. The injection suite
became the regression test that kept them at zero.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Manual fault injection in staging | Realistic, no code changes | Slow, not reproducible, not in CI | One-off deep validation |
| Wrapper-based injection in tests | Fast, deterministic, in CI | Needs seams | Default choice |
| Chaos engineering (production) | Finds unknown unknowns | Requires authority, blast radius, skills | Mature systems, after CI injection is solid |
| Property-based testing | Explores state space automatically | Seed debugging cost | State machines, classifiers, schedulers |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name the oracle before writing the test | Assert "it didn't throw" as the whole check |
| Inject at irreversible boundaries first | Build a 42-cell matrix before shipping anything |
| Keep the seam in the adapter, not in business logic | Scatter `if (chaosMode)` checks through the domain |
| Print the seed on failure | Hide the random seed in CI output |
| Assert invariants after every injected failure | Only assert the final response body |
| Inject "wrong data", not just "throws" | Assume success responses are valid |

## Common mistakes

- **Testing that the error is thrown, not that it is handled.** A test that expects `rejects.toThrow`
  passes while the system discards the error afterwards.
- **Injecting only library-level errors.** Real failures happen between library calls.
- **No state assertion.** Checking the response body but not the database state misses the entire
  class of "said failed, wrote anyway" bugs.
- **Timing-dependent tests.** `sleep(50)` before asserting is a flaky test that will eventually
  teach your team to ignore red builds.

## Checklist

- [ ] Every failure point in the operation has at least one injected failure.
- [ ] Every irreversible boundary has the delay, crash, duplicate, and wrong-data modes covered.
- [ ] Every property has a named oracle and at least one test that fails without the fix.
- [ ] Invariants (pool, transactions, timers, outcome rows) are asserted after every scenario.
- [ ] Seeds are printed on failure and replayable.
- [ ] The matrix coverage is tracked, not the test count.

## Related

- [Enforcing Properties Structurally](../02-deep-dive/02-enforcing-properties-structurally.md)
- [Checkout Correctness Audit](../03-practical-examples/01-checkout-correctness-audit.md)
- [Chapter 58 — Less Obvious Error-Handling Scenarios](../../../part-23-special-cases/58-less-obvious-error-handling-scenarios/README.md)
- [Glossary](../../../GLOSSARY.md)
