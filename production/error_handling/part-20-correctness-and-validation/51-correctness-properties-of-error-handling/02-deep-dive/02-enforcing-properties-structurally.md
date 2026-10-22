# Enforcing Properties Structurally (51.1–51.18)

> Part XX · Chapter 51 · Deep dive · _Estimated reading time: 22 min_
> **Prerequisite:** [Determinism and Completeness (51.1–51.4)](../01-concepts/01-determinism-and-completeness.md)

## In one sentence

Some properties are cheap to **guarantee** with types, scope guards, policy tables, and CI checks —
and a guaranteed property is worth ten tested ones, because it cannot be broken by the next
refactor.

## Why this matters in production

Tests are a snapshot. They tell you the code was correct when the test was written. Structures tell
you the code **cannot be wrong** — and they keep telling you after the next engineer, who did not
read the test, refactors the handler.

The prioritization rule:

```text
   cost of proof  ─────────────────────────────▶  cost of prevention

   cheap + strong prevention  >  cheap + weak prevention  >  expensive + strong prevention
   (type system)               (a test)                (a review rule)
```

A `Result` type makes "returns `undefined` on failure" unrepresentable. A test proves it was not
returned on the day you wrote it.

## Core concept

### Four layers of prevention

| Layer | Mechanism | Properties it protects | Cost |
| ----- | --------- | ---------------------- | ---- |
| **Types** | `Result`, closed unions, `never`, branded types | 51.1, 51.3, 51.11, 51.15 | Low, up front |
| **Runtime guards** | Scope guards, invariant assertions, schema validation | 51.7, 51.10, 51.8 | Low, localized |
| **Policy tables** | One classifier, one recovery table, one contract map | 51.3, 51.4, 51.16, 51.17 | Medium |
| **Process** | Lint rules, CI gates, registry checks, review templates | 51.2, 51.3, 51.5 | Medium, organizational |

### Property → mechanism map

| Property | Structural mechanism | If absent |
| -------- | --------------------- | --------- |
| 51.1 Defined outcome | Closed union + `assertNever` | Orphan states, `undefined` returns |
| 51.2 No silent discard | Lint rule banning empty catch + return-value check | Invisible failures |
| 51.3 Deterministic classification | Single pure classifier + golden-corpus CI test | Divergent routing |
| 51.4 Causes recoverable | `cause` required in the error constructor | Untraceable incidents |
| 51.5 No sensitive exposure | Public DTO type + serialization allowlist | Leaks |
| 51.6 Retries terminate | Retry helper with mandatory bounds in its type | Infinite loops |
| 51.7 Cleanup occurs | Scope-managed resources (`await using`) | Pool exhaustion |
| 51.8 Consistency preserved | Invariant assertion at the state transition | Silent corruption |
| 51.9 No duplicate side effects | Unique constraint + `ON CONFLICT DO NOTHING` | Double charges |
| 51.10 Responses follow contracts | Schema-validated response builder | Client breakage |
| 51.11 Safe fallback for unknown | Total policy table with a reviewed default row | Outages hidden |
| 51.12 No unbounded recursion | Depth counters + cycle detection in the translator | Stack overflow |
| 51.13 Concurrency-safe | Atomic DB operations; no shared mutable error state | Duplicate effects |
| 51.14 Partial failures accurate | Batch result type with a checked invariant | Misreported results |
| 51.15 Cancellation not success | `cancelled` in the outcome union + abort checks | False success |
| 51.16 Recovery preconditions | `decideRecovery()` with a stop-reason return | Wrong recovery |
| 51.17 Transformations preserve metadata | Translation table with explicit field mapping | Lost information |
| 51.18 Predictable during dependency failures | One policy object per dependency, loaded from config | Emergent behaviour |

## How it works (mechanics)

### Types that forbid wrong answers

```ts
// 51.1 + 51.11 + 51.15: the outcome union contains every legal terminal state.
// Adding a state without handling it is a compile error (assertNever).
export type Outcome<T> =
  | { status: "success"; value: T }
  | { status: "recovered"; value: T; attempts: number }
  | { status: "degraded"; value: T | null; reason: string }
  | { status: "failed"; error: AppError }
  | { status: "cancelled" }
  | { status: "unknown"; error: AppError; resolveBy: string };

export function assertNever(x: never): never {
  throw new Error(`unhandled outcome: ${JSON.stringify(x)}`);
}

export function render(o: Outcome<Receipt>): string {
  switch (o.status) {
    case "success": return `ok ${o.value.id}`;
    case "recovered": return `ok ${o.value.id} after ${o.attempts} attempt(s)`;
    case "degraded": return `partial: ${o.reason}`;
    case "failed": return `failed: ${o.error.code}`;
    case "cancelled": return "cancelled";
    case "unknown": return `unknown, resolve by ${o.resolveBy}`;
    default: return assertNever(o);       // 51.1: no orphan states
  }
}
```

### Scope-managed resources

```ts
// 51.7: the type system + the runtime guarantee that release happens on every path,
// including cancellation and exceptions from the body.
export class PooledConnection implements AsyncDisposable {
  constructor(private conn: PgClient, private pool: Pool) {}
  async [Symbol.asyncDispose]() {
    try { await this.conn.query("ROLLBACK"); } catch { /* the txn may be gone */ }
    finally { this.pool.release(this.conn); }   // 51.7: idempotent release
  }
}

// Usage — release is not optional and not forgotten:
await using conn = await pool.acquire();
await conn.query("SELECT ...");
```

### Policy tables instead of scattered conditionals

Scattered `if (err instanceof ...)` chains are where determinism dies. One table, one place, one
review surface.

```ts
// 51.3 + 51.16 + 51.18: one table drives classification, recovery, and alerting.
type PolicyRow = {
  code: string;
  category: Category;
  retryable: boolean;
  maxAttempts: number;
  recovery: "retry" | "compensate" | "degrade" | "fail" | "terminate";
  alert: boolean;
  httpStatus: number;
};

const POLICIES: Record<string, PolicyRow> = {
  PAYMENT_CARD_DECLINED:     { code: "PAYMENT_CARD_DECLINED", category: "business", retryable: false, maxAttempts: 0, recovery: "fail",      alert: false, httpStatus: 402 },
  PAYMENT_PROVIDER_TIMEOUT:  { code: "PAYMENT_PROVIDER_TIMEOUT", category: "transient", retryable: true,  maxAttempts: 3, recovery: "retry",     alert: true,  httpStatus: 503 },
  PAYMENT_OUTCOME_UNKNOWN:   { code: "PAYMENT_OUTCOME_UNKNOWN",  category: "ambiguous", retryable: false, maxAttempts: 0, recovery: "degrade",   alert: true,  httpStatus: 202 },
  DB_SERIALIZATION:          { code: "DB_SERIALIZATION",         category: "transient", retryable: true,  maxAttempts: 3, recovery: "retry",     alert: false, httpStatus: 503 },
  WEBHOOK_SIGNATURE_INVALID: { code: "WEBHOOK_SIGNATURE_INVALID", category: "security", retryable: false, maxAttempts: 0, recovery: "fail",      alert: true,  httpStatus: 401 },
  UNCLASSIFIED:              { code: "UNCLASSIFIED",             category: "internal",  retryable: false, maxAttempts: 0, recovery: "fail",      alert: true,  httpStatus: 500 },
};
```

Because the table is total, an unregistered code **cannot** exist at runtime — the constructor
validates against it:

```ts
function policyFor(code: string): PolicyRow {
  const row = POLICIES[code];
  if (!row) throw new Error(`error code not in policy table: ${code}`);  // fail at creation time
  return row;
}
```

### CI and lint: the cheap, wide net

| Check | Mechanism | Blocks |
| ----- | --------- | ------ |
| No empty catch | `no-empty` + custom rule banning `catch {}` | 51.2 |
| No catch returning `undefined`/`null` | Custom lint rule | 51.2, 51.1 |
| Every error code is registered | CI script diffing the code registry | 51.3, 51.4 |
| Every registered code has a policy row | CI script asserting table coverage | 51.3, 51.11 |
| Every registered code has a test | CI script mapping codes → test files | 51.3 |
| Public responses validate against a schema | Contract test over all error branches | 51.10 |
| No secret literal in error paths | Secret scanner on error construction sites | 51.5 |

```yaml
# .github/workflows/error-contracts.yml — the "error contract" gate
name: error-contracts
on: [pull_request]
jobs:
  contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint -- --rule no-empty-catch
      - name: Every error code has a policy row
        run: node scripts/check-policy-coverage.mjs
      - name: Every error code has a test
        run: node scripts/check-code-test-coverage.mjs
      - name: Public error bodies match the schema
        run: npm run test -- --suite contracts
```

## Worked example — turning a property into a CI gate

Property 51.10 ("responses follow contracts") was, in one quarter, violated **nine times** — each
time by a different handler with a slightly different body shape. The fix was not a review rule.

1. **One response builder.** `errorResponse(err)` is the only function that produces an error body.
   Handlers call it; they never build bodies.
2. **One schema.** JSON Schema for the public error envelope; the builder's output is validated
   against it *at runtime* in non-production builds, so a malformed body fails loudly in CI.
3. **One contract test.** It enumerates every registered error code, forces the handler that
   produces it, and asserts status + body against the schema and the policy table.

```ts
// scripts/check-policy-coverage.mjs — the gate in one file
import { ERROR_CODES } from "./src/errors/registry.mjs";
import { POLICIES } from "./src/errors/policies.mjs";

const missing = ERROR_CODES.filter((c) => !POLICIES[c.code]);
if (missing.length) {
  console.error(`error codes without a policy row:\n${missing.map((c) => `  - ${c.code}`).join("\n")}`);
  process.exit(1);
}
```

Result: new error codes without a policy row cannot merge. The nine violations became structurally
impossible in one afternoon.

## Key data / numbers

- **Properties preventable by types alone: 6** (51.1, 51.3, 51.11, 51.15, plus partial 51.14).
- **Policy table must be total**: every registered code has exactly one row; `UNCLASSIFIED` is the
  only default.
- **Registry size** for a mid-size SaaS: **80–200 codes**; beyond ~300, split by domain.
- **CI gate budget**: the contract gate should run in **< 60 s** to stay in the pre-merge path.
- **Lint coverage**: `no-empty` catches the majority of silent discards; custom rules cover the
  `return null` variant.
- **Assertion cost**: invariant assertions in hot paths cost **< 1% CPU**; keep them on, and gate
  them behind a flag only in the hottest loops.
- **Code-to-test mapping**: a registry → test-file map catches **100%** of newly added codes
  without asking anyone.

## Real-world use case — Acme SaaS `ExportJob`

Acme's job runner had a `catch` that set `status = 'failed'` and logged — but the *message* was
the only diagnostic, and the message changed with library versions. The runner also had three
different places that decided "retryable", and they disagreed: the queue's own redelivery policy
retried `PermanentError` too, so poison jobs burned 5 attempts each.

Three structural changes, each mapping to a property:

- **Typed outcomes** on the job handler (`Outcome<ExportResult>`) removed the possibility of a
  job ending in a state the runner did not understand (51.1).
- **A single policy table** replaced the three scattered `instanceof` checks; the queue's
  redelivery policy now reads `outcome.status` instead of guessing from the error type (51.3,
  51.16).
- **A CI gate** on the registry forced every new error code to declare its retry policy and to
  name a test (51.3).

Measured effect: poison-job retries dropped from 5 attempts to 1 (the DLQ now receives them on the
first permanent failure), and queue redelivery volume fell by ~40%, because permanent errors stopped
being redelivered.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Types + closed unions | Compiler-enforced, survives refactors | Verbosity; onboarding cost | Core domain and boundary layers |
| Runtime policy tables | One review surface, easy to change | Runtime lookup; drift between code and table | Any system with a registry |
| CI gates | Catches new violations automatically | Requires maintenance; can annoy reviewers | Mature teams with a registry |
| Code review only | Cheap to start | Inconsistent; depends on reviewer attention | Early-stage products |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Make the correct path the type-checked path | Rely on comments to forbid wrong returns |
| Keep one total policy table per concern | Scatter `instanceof` checks across layers |
| Turn recurring review findings into CI gates | Repeat the same finding in review forever |
| Register codes in one registry and validate at construction | Allow ad-hoc string codes |
| Keep runtime assertions cheap and always on | Gate all assertions behind a debug flag |

## Common mistakes

- **A policy table that drifts from the registry.** The table is right in production and wrong in
  review; the CI gate is what keeps them equal.
- **Types that describe intent but not enforcement.** `Outcome<T>` with a `catch` that returns
  `null` still compiles.
- **Over-typing internal code.** Making every internal helper return a six-variant union adds
  ceremony without adding safety. Type the boundaries.
- **CI gates that fail for unrelated reasons.** A slow gate gets ignored, and then it protects
  nothing.

## Checklist

- [ ] Domain and boundary APIs return closed unions, not `T | undefined` with error semantics.
- [ ] `assertNever` covers every union at its render/exhaustive-match site.
- [ ] Resources are scope-managed, not manually released.
- [ ] One total policy table drives classification, recovery, alerting, and HTTP status.
- [ ] Every error code is in the registry and validated at construction.
- [ ] CI blocks: empty catch, unregistered codes, codes without policy rows, codes without tests.
- [ ] Public error bodies are produced by exactly one builder and validated against a schema.

## Related

- [Verifying Properties with Failure Injection](./01-verifying-properties-with-failure-injection.md)
- [Checkout Correctness Audit](../03-practical-examples/01-checkout-correctness-audit.md)
- [Chapter 50 — Error Handling as an Engineering Standard](../../../part-19-contracts-and-governance/50-error-handling-as-an-engineering-standard/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
