# Readable Business Logic and the Easy Path

> Part XXI · Chapter 53 · Sections 53.13, 53.14, 53.15 · _Estimated reading time: 16 min_
> **Prerequisite:** [Localizing Decisions and Conventions](./04-localizing-decisions-and-conventions.md)

## In one sentence

Business logic is readable when the **failure cases are visible as data next to the happy
case** — and the easiest path for a developer must be the path that produces correct errors.

## Why this matters in production

Error handling inside business logic has two costs that are hard to see in a diff:

- **Reading cost.** A function whose control flow is dominated by error branches is harder to
  read than the domain rule it implements. The reviewer re-reads it, and the bug in the
  domain rule is missed.
- **Compliance cost.** When the *only* easy way to add a new failure is to write a branch in
  the feature, engineers write branches in the feature — and every branch is a decision site
  that escapes the tables.

The second cost is the one that compounds. A codebase where the convention requires seven
edits will accumulate seven-edit deviations, each individually reasonable.

## Core concept

### 53.13 — Readable business logic

The rule: **the business rule is the code; the failure handling is the data around it.**

```ts
// ❌ Before: the domain rule is buried between branches.
async function completeCheckout(order: Order, card: Card): Promise<Receipt> {
  if (order.status === "paid") throw new Error("already paid");
  if (order.status !== "pending") throw new Error("bad state");
  if (order.totalCents > card.limitCents) throw new Error("over limit");
  const charge = await gateway.charge(order.totalCents, card);
  if (!charge.ok) {
    if (charge.reason === "insufficient_funds") throw new Error("no funds");
    if (charge.reason === "do_not_honor") throw new Error("declined");
    throw new Error("charge failed");
  }
  const receipt = await receipts.issue(charge.id);
  if (!receipt) throw new Error("no receipt");
  return receipt;
}
```

Every failure is an `Error` with a string message, so:

- The HTTP layer cannot map them without string matching.
- The `catch` block cannot distinguish "already paid" (a conflict, `409`) from "declined" (a
  business decline, `402`).
- The string messages are the contract, so they cannot be changed safely.

```ts
// ✅ After: the domain rule reads straight down; failures are typed.
type CheckoutOutcome =
  | { kind: "ok"; receipt: Receipt }
  | { kind: "already_paid" }
  | { kind: "invalid_state"; current: OrderStatus }
  | { kind: "over_limit" }
  | { kind: "card_declined"; reason: DeclineReason }
  | { kind: "charge_failed"; cause: AppError };
```

The happy path is now the shape of the code, and every failure is a **named variant** the
compiler can check for. The `switch` at the boundary becomes total:

```ts
function toHttp(outcome: CheckoutOutcome): Response {
  switch (outcome.kind) {
    case "ok":             return ok(outcome.receipt);
    case "already_paid":   return fail("CHECKOUT_ALREADY_PAID", 409);
    case "invalid_state":  return fail("CHECKOUT_INVALID_STATE", 409);
    case "over_limit":     return fail("CHECKOUT_OVER_LIMIT", 422);
    case "card_declined":  return fail("CHECKOUT_CARD_DECLINED", 402);
    case "charge_failed":  return failFrom(outcome.cause);
  }
}
```

This is the "result type" pattern from Chapter 7 applied for a reason: **not** to avoid
exceptions, but to make the *set of expected failures* part of the function's signature. The
reviewer can see the contract without reading the implementation.

Exceptions remain correct for the unexpected: a null dereference, a failed invariant. The
distinction is **expected outcome** (a value) versus **unexpected fault** (a throw).

### 53.14 — The easiest path is the correct path

This is the organising principle of the whole chapter. For every convention you introduce,
ask: **is following it easier than not following it?**

| Convention | Easy path (correct) | Hard path (incorrect) | Adopted? |
| ----------- | ------------------- | --------------------- | -------- |
| Register the code | The registry row is required by the type signature | — | ✅ |
| Map the status | The table lookup is the only way to get a status | Write `res.status(422)` | ❌ without a lint rule |
| Use the shared retry | `retryPolicyFor(category)` is one call | Hand-rolled loop | ❌ unless hand-rolling is longer |
| Put errors in the domain module | The domain module exports the code | Import from `utils/errors` | ✅ |

Three techniques make the correct path the easy one:

1. **Make the wrong thing impossible to type.** If `res.status()` is not available in feature
   handlers (the response type only accepts a `Problem` object), the incorrect path does not
   compile.
2. **Make the correct thing shorter.** A one-line table lookup beats a four-line branch, even
   if the branch is "only used once".
3. **Make the incorrect path loud.** A lint rule that reports `res.status(` inside
   `src/features/**` costs nothing and catches the drift.

```ts
// The type makes the correct path the only path.
export type ProblemStatus = 400 | 401 | 403 | 404 | 409 | 410 | 413 | 415 | 422 | 429 | 500 | 502 | 503 | 504;

// Feature handlers cannot invent a status; they must ask the table.
export function problemFor(err: AppError): { status: ProblemStatus; body: ProblemBody };
```

A `ProblemStatus` union of **14** members is small enough to be exhaustive and large enough
to prevent typos. It also makes the API surface reviewable: a new status is an explicit
decision.

### 53.15 — Avoiding boilerplate

Boilerplate is the part of error handling that is the same in every file. The rule from
Chapter 2 (minimise boilerplate) applies: **each piece of boilerplate should be removed by a
mechanism, not by discipline.**

| Boilerplate | Lines (typical) | Removal mechanism |
| ----------- | --------------- | ----------------- |
| Constructing the error object with fields | 6–10 | A factory with a required shape |
| Attaching context (request id, tenant, operation) | 4–8 | A boundary that enriches automatically |
| Mapping to an HTTP response | 8–15 | One shared mapper |
| Logging + rethrowing | 4–6 | A boundary that logs once, at the end |
| Redacting context | 3–5 | A shared allowlist in the enrichment step |

The **factory** is the key mechanism. A factory that requires a code (not a free-form string)
removes the entire class of "typo in the error code" bugs, and it makes the registry lookup
automatic:

```ts
// The code is a member of a union, not a string — so it cannot be misspelled.
export function domainError<C extends DomainCode>(
  code: C,
  message: string,
  meta?: Record<string, unknown>,
): DomainError<C> {
  return { kind: "domain", code, message, meta: redact(meta) };
}
```

With a union of **~40 domain codes** in one file, a typo is a compile error, and an
unregistered code cannot be constructed at all.

**What not to remove:** the *semantic* content. A factory that takes only a code and a
message is fine; a factory that takes the message and hides the code is not — the code is the
part that must not be duplicated.

## How it works (mechanics)

The refactor that makes business logic readable again:

```text
  1. List the expected failures of the function.        → 6 failures
  2. Separate expected failures from unexpected faults.  → 6 expected, rest = throw
  3. Give each expected failure a named variant.         → 6 variants
  4. Move the mapping to the boundary, once.             → 1 switch, total
  5. Keep the domain module free of transport imports.   → no res, no status
```

Step 2 is the one that requires judgement, and it is the one that matters. A "database
unavailable" inside a domain function is an *unexpected fault* from the domain's point of
view — the domain did not decide that the database could be down. It stays a throw, and the
infrastructure layer translates it.

## Worked example

Acme's `ExportJob` runner was 210 lines, of which **78** were error handling, and the domain
rule ("read rows in batches, write to S3, record a checkpoint") was hard to find inside it.
The rewrite:

```ts
// The domain rule, readable.
export async function runExport(job: ExportJob, deps: ExportDeps): Promise<ExportOutcome> {
  const page = await deps.source.readPage(job.cursor, EXPORT_PAGE_SIZE);
  if (page.rows.length === 0) return { kind: "done", bytesWritten: job.bytesWritten };

  const written = await deps.sink.write(job.partKey, page.rows);
  await deps.checkpoint.save(job.id, { cursor: page.nextCursor, bytesWritten: written.total });

  return { kind: "continued", cursor: page.nextCursor };
}
```

Every failure — a missing tenant, a revoked S3 token, a row that failed schema validation, a
sink that returned a short write — became a typed outcome. The 78 lines of error handling
became **19 lines** in one place:

```ts
export type ExportOutcome =
  | { kind: "done"; bytesWritten: number }
  | { kind: "continued"; cursor: string }
  | { kind: "tenant_not_found"; tenantId: string }
  | { kind: "schema_invalid"; row: number; columns: string[] }
  | { kind: "sink_unauthorized"; cause: AppError }
  | { kind: "sink_short_write"; expected: number; actual: number };
```

The measurable result: the runner went from **210 lines to 96**, and the time to review a
change to it fell from **26 min to 9 min** — because the reviewer now reads the domain rule
in one pass and checks the outcome table in a second pass, instead of simulating six
interleaved branches.

## Key data / numbers

- **Target: failure branches ≤ 20% of a function's lines** in business logic. Acme's
  `ExportJob` runner was **37%** before the rewrite; **8%** after.
- **Target: ≤ 6 expected failure variants** per function. More than six usually means the
  function does two things.
- **Target: nesting depth ≤ 2** in business logic, **0** in the failure mapping.
- **Domain code (`res.status`, `statusCode`, HTTP imports) in feature modules: 0.** Enforceable
  with an ESLint `no-restricted-imports` rule.
- **`ProblemStatus` union size: 14** status codes — small enough to be exhaustive, large
  enough to prevent typos.
- **Factory-generated codes: ~40** domain codes in a single union file; a typo is a compile
  error, and an unregistered code cannot be constructed.
- **Boilerplate target:** ≤ **20 lines** of error handling per feature file; Acme's features
  averaged **57** before the factories.
- **Review-time impact:** a change to a rewritten feature: **26 min → 9 min** (65% reduction);
  error-handling review across 40 PRs: **22 min → 8 min** (64% reduction).
- **Compile-time check:** a misspelled error code fails the build in **< 3 s**; the same typo
  found in production cost **~45 min** of incident triage in one case.

## Real-world use case — Acme SaaS, the `ExportJob` that took four days to change

Acme's export runner was the file nobody wanted to touch. It was 210 lines, it had been
modified **14 times in a year**, and **every** modification was a merge conflict. The reason:
error handling was interleaved with the domain rule, and the error branches were the
contested part — each one added by a different engineer, each with a slightly different
response format.

The business consequence was not a crash; it was **slowness**. Features that depended on
exports (the CSV report, the audit extract, the analytics snapshot) shipped an average of
**6 days** behind schedule, and the export runner was on the critical path of **4 of 9**
scheduled product releases in one quarter.

The rewrite to a typed outcome took **one day** and did three things:

1. Made the domain rule readable, so new contributors could modify it without a mentor.
2. Reduced merge conflicts, because the error branches stopped being edited.
3. Turned the six expected failures into a table that the **API and job adapters** consume
   directly — so the same outcome is reported identically whether the export was triggered
   by a user or by the nightly schedule.

After the rewrite, the runner changed **11 times** in the following year with **2 merge
conflicts**, and one of the four blocked releases became unblocked.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Exceptions for everything | Familiar; no type churn | Failure set invisible; string-matched at boundaries | Small systems, mostly unexpected failures |
| Result type for expected failures | Failure set is in the signature; total mapping | More types; verbose call sites | Business logic with known, named outcomes |
| Result type + exceptions for faults | Best of both; faults still exceptional | Two mechanisms to learn | Mature systems with a taxonomy (the default here) |
| Feature-local error classes | Self-contained feature | Duplication; no central registry | Feature teams that own their contract end to end |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return named outcomes for expected failures | Throw an `Error` for every business rule |
| Map outcomes once, at the boundary | Map the same failure in three layers |
| Make the wrong thing fail to compile | Rely on review to catch `res.status(422)` |
| Use factories with typed codes | Build error objects field by field |
| Keep domain modules free of transport imports | Import `Response` into a domain file |
| Keep the happy path the shape of the code | Bury the domain rule between failure branches |

## Common mistakes

- **Result types for faults.** A `Result` variant for "the database was down" leaks
  infrastructure into the domain signature and forces every caller to handle it.
- **A union that grows forever.** 30 variants in one union means the function does too much.
  Split the function.
- **Moving errors out of the feature entirely.** The feature knows which failures are its own;
  removing that knowledge produces a generic error that nobody can act on.
- **String messages as the contract.** Changing "Card declined" to "Your card was declined"
  breaks every client that matched on it.
- **Boilerplate removal that removes meaning.** A factory that hides the code so nobody has
  to think about it also means nobody registers it.

## Checklist

- [ ] Every business function's expected failures are visible in its signature.
- [ ] Failure branches are ≤ 20% of a business function's lines.
- [ ] The mapping from outcome to external contract happens in exactly one place per boundary.
- [ ] Domain modules import no transport types.
- [ ] Error codes are typed members of a union, produced by a factory.
- [ ] A lint rule or type restriction prevents raw status literals in feature code.

## Related

- [Localizing Decisions and Conventions](./04-localizing-decisions-and-conventions.md)
- [A Complexity Budget for a Feature](../03-practical-examples/02-a-complexity-budget-for-a-feature.md)
- [Chapter 7 — Error Classes, Types, and Structured Results](../../part-03-error-models/07-error-classes-types-and-structured-results/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
