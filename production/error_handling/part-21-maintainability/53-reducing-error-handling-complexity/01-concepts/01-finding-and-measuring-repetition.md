# Finding and Measuring Repetition

> Part XXI · Chapter 53 · Sections 53.1, 53.7 · _Estimated reading time: 16 min_
> **Prerequisite:** [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)

## In one sentence

Repetition in error handling is **the same decision made in more than one place** — and you
find it by counting decision sites, not by counting lines.

## Why this matters in production

Duplicated error decisions fail in a specific, expensive way: **they drift**. One copy gets
updated for a new provider behaviour, the other three do not, and the difference is invisible
until a request takes one path and not the other.

Concrete costs:

- **Inconsistent user-visible behaviour.** The same validation failure returns `422` from the
  service that owns validation and `400` from the service that re-validates.
- **Slow fixes.** A bug in the mapping has to be found in all copies. Teams report "we fixed it
  in three places" as a routine annoyance.
- **Un-reviewable diffs.** A reviewer cannot tell whether two similar blocks are meant to be
  identical. They approve both, and one of them is wrong.
- **Silent policy drift.** A retry limit changes in one service; the other keeps five attempts
  for a year. Nothing detects it because nothing compares them.

## Core concept

### 53.1 — Repetition is a duplication of *decisions*

There are two kinds of repeated code:

| Kind | What repeats | Cost of duplication | Example |
| ---- | ------------ | ------------------ | -------- |
| **Mechanical repetition** | The *syntax* — the same five lines of boilerplate | Low; usually fine to keep | Building an error object with the same fields |
| **Decision repetition** | The *choice* — "a unique violation means conflict" | High; the copies disagree | Mapping SQLSTATE `23505` to `409` |

The second kind is the one that matters. Mechanical repetition is cheap to fix (see
[Chapter 15 — Avoiding Boilerplate](./05-readable-business-logic-and-the-easy-path.md)), but
decision repetition is a **correctness risk**, because two copies of a decision can hold
different values.

```ts
// ── Decision site A (repository, Acme SaaS) ────────────────────────────
if (pgErr.code === "23505") return new ConflictError("duplicate", { code: "CONFLICT" });

// ── Decision site B (admin API, Acme SaaS) ────────────────────────────
if (error.name === "PrismaClientKnownRequestError" && error.code === "P2002") {
  throw new HttpError(400, "Already exists");   // 400, not 409
}
```

Same decision ("this is a duplicate"), two answers (`409` vs `400`). Nothing breaks loudly.
Customers see an inconsistent API, and the team sees a "front-end bug" report.

### The measurement that works: decision sites

A **decision site** is any place in the code where the system answers one of these questions:

- What category is this error?
- What does the outside world see (status, code, message)?
- Is it safe to retry?
- What is the recovery (fail, degrade, compensate, terminate)?
- What context is attached?

Count the sites that answer the *same* question about the *same* subject.

```bash
# A crude but effective first pass: find the same decision expressed many ways.
rg -n "23505|P2002" --type ts src/          # duplicate detection → conflict?
rg -n "status:\s*409|statusCode:\s*409" src/ # duplicate → status mapping
rg -n "maxAttempts|attempts:\s*[0-9]" src/   # retry limits
```

You do not need a perfect tool. You need a **number** you can act on.

### The duplication report

A duplication report is four columns and fits on one screen:

```text
DECISION                COPIES  LOC SAVED IF EXTRACTED   DRIFT OBSERVED
pg unique → conflict       4          ~40 LOC              yes (400 vs 409)
provider 429 → retry       3          ~25 LOC              yes (one honours Retry-After)
http status by category    2          ~30 LOC              no
retry attempts by category 3          ~20 LOC              yes (3 vs 5 vs 5)
```

**Drift observed** is the column that matters. Duplication without drift is a smell;
duplication with drift is a defect that already reached production.

### 53.7 — Avoiding duplicated mappings

There are three ways to remove a duplicated mapping, in increasing order of cost:

| Approach | What you do | Cost | Use when |
| -------- | ----------- | ---- | -------- |
| **Delete** | Remove the duplicate by not doing the work twice | Free | The second copy was accidental |
| **Delegate** | The second copy calls the first | ~5 LOC | The first copy is already correct and stable |
| **Extract** | Both copies call a new shared function | ~30–60 LOC + call sites | ≥ 3 copies, or the decision is likely to change |

**Delete** is the under-used option. A surprising number of duplicated mappings exist because
two layers both translate the same error. The fix is to let one layer own the translation and
let the other pass the error through unchanged — which is Chapter 16 (translation) discipline
applied to complexity.

> ⚠️ **Hazard.** Delegating in the wrong direction creates a dependency from a low-level module
> to a high-level one. If the repository delegates to the HTTP layer to learn the status code,
> the dependency arrow now points outward and the domain is no longer testable in isolation.

### When duplication is the right answer

Duplication is not a sin. It is the right answer when:

- The two copies belong to **different bounded contexts** that will diverge (Acme's public API
  error shape versus its internal job vocabulary may legitimately differ).
- The shared abstraction would need **a configuration flag per call site** to remain useful —
  at that point you have built a framework with a flag, not a shared function.
- The decision is **likely to change for one copy and not the other** (the internal retry policy
  for a background job differs from the interactive request policy, on purpose).
- The cost of the shared version exceeds the cost of the drift, and you can **measure** that
  the drift has never mattered.

The rule: **document deliberate divergence in the same place the copies live**, so the next
engineer sees the intent rather than assuming an oversight.

## How it works (mechanics)

The measurement loop, run once per quarter:

```text
   ┌───────────────────────┐
   │ 1. Pick a question    │   "what does a unique violation mean?"
   └───────────┬───────────┘
               ▼
   ┌───────────────────────┐
   │ 2. Find the sites     │   rg "23505|P2002|duplicate"
   └───────────┬───────────┘
               ▼
   ┌───────────────────────┐
   │ 3. Record the answers │   4 sites, answers: 409 / 400 / 409 / 422
   └───────────┬───────────┘
               ▼
   ┌───────────────────────┐
   │ 4. Decide             │   delete? delegate? extract? keep-and-document?
   └───────────┬───────────┘
               ▼
   ┌───────────────────────┐
   │ 5. Verify the change  │   one test asserts every site agrees
   └───────────────────────┘
```

Step 5 is what stops the drift from returning. A single test that asserts the mapping is
identical in all callers is cheaper than any framework.

## Worked example

Acme's `Checkout` flow had four separate places that decided what a card decline means. The
decision sites were in the Stripe adapter, the checkout service, the HTTP handler, and the
receipt job. Their answers had diverged:

| Site | Code | HTTP | User message | Retryable |
| ---- | ---- | ---- | ------------ | --------- |
| Stripe adapter | `CARD_DECLINED` | — | — | `false` |
| Checkout service | `PAYMENT_DECLINED` | `402` | "Card declined" | `false` |
| HTTP handler | — | `500` | "Something went wrong" | `false` |
| Receipt job | `PAYMENT_DECLINED` | — | — | `false` |

The HTTP handler mapping the decline to `500` is the expensive one: **every declined card
became an internal error**, which triggered an alert, a page, and an error-budget burn. The
customer saw "Something went wrong" instead of "Your card was declined".

The fix followed the measurement, not a redesign: the Stripe adapter already produced a
correct category, so the other three sites were made to **delegate** to one registry lookup
rather than each deciding. No new abstraction was created — one function was extracted and
three call sites were deleted.

```ts
// The single remaining decision site.
const CHECKOUT_CARD_DECLINED = "CHECKOUT_CARD_DECLINED";

function statusFor(code: string): number {
  const entry = ERROR_REGISTRY[code];
  if (!entry) throw new Error(`unregistered error code: ${code}`);
  return entry.httpStatus;
}
```

## Key data / numbers

- **Trigger for extraction: ≥ 3 copies** of the same decision. Two copies are reviewed
  individually; three is where the review burden and the drift risk both jump.
- **Break-even for a shared helper: ≥ 80 LOC saved** across call sites, in addition to the
  ≥ 3 call sites (see the
  [abstraction cost analysis](../02-deep-dive/01-abstraction-cost-analysis.md)).
- **Typical drift window: 1–2 quarters** between a decision being changed in one place and
  the same decision being changed everywhere else.
- **Acme's Checkout measurement:** 4 decision sites for "what does a decline mean", **19 lines**
  of duplicated logic, **1 divergence found** (the `500`), fixed in **1 hour**.
- **Review cost of duplication:** error-handling review time measured **22 min/PR** before the
  cleanup, **8 min/PR** after, across 40 pull requests.
- **Registry coverage target:** 100% of error codes resolvable in one lookup. A site that
  decides for itself is a site that will disagree.

## Real-world use case — Acme SaaS, three repositories, one decision

Acme had three repositories (API, Workers, Billing) and each had its own `mapDatabaseError`
function. Over **nine months**, the divergence was:

- API: unique violation → `409 Conflict`
- Workers: unique violation → `500 Internal` (the job retried, creating more duplicates)
- Billing: unique violation → `422 Unprocessable` (clients thought their payload was wrong)

The measurable damage: **1,240 duplicate subscription rows** in Billing over the quarter, each
one requiring a manual refund and a support reply. A single duplicate-mapping decision was
worth more than every other error-handling issue in the backlog combined.

The fix was not a framework. It was a **shared package** (`@acme/errors`) with one mapping
table, released at `1.0.0`, adopted by all three repositories in **four days** because the
API surface was six functions and one table. The divergence ended the day the last repository
switched. The story is repeated in
[Chapter 54](../54-reusable-error-handling-infrastructure/README.md), because the packaging
is where the fix actually landed.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Delete the duplicate | Removes code and drift | Requires a layer to stop deciding | The duplicate was accidental |
| Delegate to an existing site | Cheapest fix; no new API | Can invert dependency direction | A correct, stable site already exists |
| Extract a shared function | One decision, one place | Costs indirection and a new API | ≥ 3 copies; decision likely to change |
| Keep both, documented | Zero cost | Drift continues by design | Different bounded contexts |
| Build a framework | Maximum uniformity | Highest cost; slowest adoption | Many teams, many repos, stable domain |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Count decision sites, not lines | Judge complexity by file length |
| Record the drift you actually observed | Assume duplicated code is duplicated *and* correct |
| Delete accidental duplicates | Extract a helper for a single call site |
| Document deliberate divergence next to the copies | Let "we meant it to differ" live only in someone's head |
| Add one test asserting all sites agree | Rely on review to catch drift |

## Common mistakes

- **Extracting a helper for two call sites.** The indirection costs more than the duplication
  and the helper acquires a flag within a month.
- **Delegating upward.** The repository learning the HTTP status from the transport layer breaks
  the dependency direction from Chapter 45.
- **Counting the wrong duplication.** Boilerplate that looks identical is cheap; two similar
  conditionals that answer different questions are not duplication.
- **Fixing the symptom.** Deleting a copy without asking "which copy was right?" can convert a
  visible `500` into an invisible `409` — better for the customer, but still wrong.
- **Never re-measuring.** A duplication report is a snapshot; drift accumulates between
  measurements.

## Checklist

- [ ] You can name, for your codebase, the top five duplicated error decisions and their copy
      counts.
- [ ] You have checked whether the copies currently *agree*.
- [ ] Every extracted helper has ≥ 3 call sites or a documented reason.
- [ ] Deliberate divergence is written down in the module, not only in a chat message.
- [ ] One test asserts the copies that must agree actually agree.

## Related

- [Extracting Policies Without Over-Abstraction](./02-extracting-policies-without-over-abstraction.md)
- [Simplifying Conditionals, Translation, and Retries](./03-simplifying-conditionals-translation-and-retries.md)
- [Chapter 16 — Error Translation and Normalization](../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
- [Chapter 45 — Organizing Error-Handling Modules](../../part-17-organization/45-organizing-error-handling-modules/README.md)
