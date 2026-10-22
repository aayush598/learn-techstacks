# Abstraction Cost Analysis

> Part XXI · Chapter 53 · Sections 53.3, 53.16 · _Estimated reading time: 20 min_
> **Prerequisite:** [Extracting Policies Without Over-Abstraction](../01-concepts/02-extracting-policies-without-over-abstraction.md)

## In one sentence

An abstraction cost analysis **prices an extraction before you write it** — the complexity it
removes versus the complexity it adds — and refuses the extraction when the second is larger.

## Why this matters in production

The most expensive error-handling refactor is not a wrong one. It is an **expensive one that
was approved by consensus**. Five engineers agree that centralising error handling is right,
three weeks go into a shared framework, and the result is a package nobody fully understands,
which nobody dares change, which therefore keeps duplicating the logic it was meant to remove.

The alternative is to make the decision **before** the code, with numbers. That is what this
analysis is: a small, repeatable calculation you run in a code review or a planning session.

## Core concept

### The cost model

An extraction has two sides. Both must be counted **in the same unit** — the unit that the
reader of the code pays in.

```text
  COST OF THE ABSTRACTION (what you add)      BENEFIT (what you remove)

    A1  implementation lines                     B1  duplicated lines removed
    A2  call-site changes (per site)             B2  decision sites collapsed
    A3  new concepts / vocabulary                B3  drift risk removed
    A4  indirection cost per reader              B4  onboarding time saved
    A5  maintenance cost (one owner, forever)    B5  review time saved
    ────────────────────────────                 ────────────────────────────
    A = A1 + 2·A2 + 3·A3 + A4 + A5                B = B1 + 2·B2 + 3·B3 + B4 + B5
```

The weights are not arbitrary; they express how expensive each kind of cost is **per unit of
reader attention**:

| Weight | Why |
| ------ | --- |
| `2×` for call-site changes | Every call site is a place a future change can be forgotten |
| `3×` for new vocabulary | A new word is paid by every reader, forever, and cannot be deleted |
| `2×` for a collapsed decision site | One site removed is worth more than one site added, because it is a *guarantee* of agreement |
| `1×` for implementation lines | Implementation lines are the cheapest thing to write and the easiest to review |

### The four questions

**Q1 — How many call sites share the decision?**
Below **3**, the abstraction is a parameter bag. Two call sites always diverge eventually,
and the abstraction gains a flag to cover the difference, and the flag is now a fifth decision
site. This is the most common failure.

**Q2 — Can the same arguments serve every call site?**
If each call site passes different values for most parameters, the abstraction is not a shared
policy; it is a configuration surface wearing a policy's clothes.

**Q3 — Does the abstraction introduce a word the domain does not have?**
New vocabulary is the most expensive cost, because it is paid by everyone who reads the code
and it can never be removed without a deprecation. A "retry scope" or "error tier" that only
exists in the error-handling module is a permanent tax.

**Q4 — What happens if it is deleted?**
The removal test: paste the body back at each call site. If no call site becomes harder to
read, the abstraction was ceremony. If one call site becomes obviously duplicated again, the
abstraction is earning its keep — and only that one call site needs it.

### The scorecard

```text
  ABSTRACTION COST ANALYSIS

  Subject:  map Postgres unique-violation to a domain conflict
  ------------------------------------------------------------------
  A1  implementation lines                  18        18
  A2  call-site changes (3 sites × 2)       3×2=6      12
  A3  new concepts ("DbErrorTranslator")    1×3=3       9
  A4  indirection per reader (1 hop)        1          1
  A5  maintenance (1 owner, 8 h/yr)         1          1
  A = 41
  ------------------------------------------------------------------
  B1  duplicated lines removed              12        12
  B2  decision sites collapsed (2 → 1)      1×2=2       4
  B3  drift risk removed (1 observed)       1×3=3       9
  B4  onboarding time saved                 1          1
  B5  review time saved                     1          1
  B = 27
  ------------------------------------------------------------------
  NET = A - B = +14  →  REJECT (or reduce scope)
```

Note the outcome: the numbers say **reject**. The subject is a *reasonable* extraction — three
call sites, one decision — but the vocabulary cost of naming a new concept, plus the
per-call-site change cost, exceeds the duplication it removes.

The correct response to a negative result is **not** "never abstract". It is **reduce the
scope**: name it less, call it less, and try again.

```text
  REVISED SUBJECT:  map Postgres unique-violation to a domain conflict
  ------------------------------------------------------------------
  A1  implementation lines (table row + helper)  8      8
  A2  call-site changes (3 sites × 1)           3×1=3     6
  A3  new concepts (none — uses existing codes) 0       0
  A4  indirection per reader                    0        0
  A5  maintenance                               1        1
  A = 15
  ------------------------------------------------------------------
  B = 27 (unchanged)
  ------------------------------------------------------------------
  NET = A - B = -12  →  ACCEPT
```

The revised version extracts the *decision* (a registry row) instead of the *mechanism* (a
translator class). Same behaviour, one-third of the cost, and no new vocabulary.

### The break-even thresholds

| Threshold | Value | Basis |
| --------- | ----- | ----- |
| Minimum call sites | **3** | Below this, an abstraction needs a flag per variation |
| Minimum LOC saved | **80** | Below this, the indirection cost rivals the duplication |
| Maximum new concepts | **1** | Two new concepts usually means a framework is forming |
| Maximum parameters in a policy object | **5** | Beyond five, use a table keyed by subject |
| Maximum indirection depth | **1 hop** | Two hops means the reader must hold two files in their head |
| Net score for acceptance | **≤ 0** (benefit ≥ cost) | The only rule that matters |
| Minimum drift evidence | **1 observed** | Unobserved drift is a hypothesis, not a cost |

The **drift-evidence** rule is the one teams resist. "We might need this later" is not a cost.
The analysis has to be run on a real duplication, in a real codebase, with a real number.

### What the analysis is not

- **Not a style debate.** The scores settle arguments about *cost*; they do not settle
  arguments about *taste*. If two extractions score the same, choose the one with fewer new
  concepts.
- **Not a one-time gate.** Re-run it when the call-site count changes by 2× or when a new
  consumer adopts the abstraction.
- **Not applicable to a decision that must be made once.** A single decision — "does this
  request get a `429`?" — is not worth an analysis. Only *repeated* decisions are candidates.

## How it works (mechanics)

Run the analysis in a review, in this order:

```text
  1. Write the subject as a question + subject key.
     "What does <subject> mean, and who decides?"
  2. Find the call sites. Count them. (Q1)
  3. List the arguments each call site would pass. (Q2)
  4. Name the abstraction. Count the new words. (Q3)
  5. Paste the body at each call site and compare readability. (Q4)
  6. Count the lines you would delete. (B1)
  7. Count the decision sites you would collapse. (B2)
  8. Apply the weights. Compute A and B.
  9. If NET > 0, reduce the scope and re-run — do not proceed at step 1 with the same design.
```

Step 9 is the discipline that keeps this honest. The point of the analysis is not to
*approve* an extraction; it is to **force the extraction to become the smallest thing that
works**.

## Worked example

Acme's `Checkout` service had a candidate extraction: a `FailureAdvisor` class that would
encapsulate "what to do when something fails in checkout". The proposal was written in a
design doc and reviewed favourably by four engineers.

The analysis:

| Cost | Item | Score |
| ---- | ---- | ----- |
| A1 | 240 lines of implementation (advisor, 6 strategies, builder) | 240 |
| A2 | 7 call sites × 2 changes each | 28 |
| A3 | 3 new concepts (`FailureAdvisor`, `FailureStrategy`, `AdviceScope`) | 9 |
| A4 | 2 hops of indirection (service → advisor → strategy) | 2 |
| A5 | Maintenance: 1 owner, ~16 h/quarter | 1 |
| **A** | | **280** |

| Benefit | Item | Score |
| ------- | ---- | ----- |
| B1 | 95 duplicated lines removed | 95 |
| B2 | 5 decision sites collapsed to 1 | 10 |
| B3 | 2 observed drift incidents avoided | 6 |
| B4 | Onboarding time saved (~10 min per new engineer) | 1 |
| B5 | Review time saved (~6 min/PR) | 1 |
| **B** | | **113** |

**NET = +167 → reject.**

The team's reaction was to scope it down, and the second version was a **table**:

```ts
// A: 12 lines, 0 new concepts, 1 hop
const CHECKOUT_RECOVERY: Partial<Record<Category, Recovery>> = {
  external_api_transient: { action: "retry", maxAttempts: 3 },
  external_api_permanent: { action: "fail" },
};
```

Re-run: **A = 15, B = 113, NET = −98 → accept.** The behaviour the team wanted was
identical; the cost was **265 lines lower**. The analysis did not stop an abstraction; it
stopped a *framework* and delivered the abstraction the team actually needed.

## Key data / numbers

- **Minimum call sites for an extraction: 3.** Two call sites are not enough evidence.
- **Break-even LOC saved: 80.** Below this, inline the duplication and note the date.
- **New-concept budget: 1.** Two new words means a framework is forming; stop and re-scope.
- **Indirection depth: 1 hop.** The reader should hold one file, not two, in mind.
- **Weights:** call-site change **2×**, new concept **3×**, collapsed decision site **2×**,
  drift removed **3×**, everything else **1×**.
- **Acceptance rule: NET ≤ 0.**
- **Measured outcomes at Acme (6 extractions analysed):** 2 accepted as proposed, 3 accepted
  after re-scoping, 1 rejected outright. Average lines removed: **74**; average lines added:
  **19**. The re-scoping step changed the outcome in **3 of 6** cases.
- **Review-time effect:** PRs containing an extracted policy reviewed in **6 min** versus
  **17 min** for the equivalent inline version (40 PRs sampled).
- **Drift evidence:** at least **one observed** incident or divergence is required to count
  `B3`; hypothetical drift scores **0**.

## Real-world use case — Acme SaaS, the framework that was never built

Acme's platform team proposed a shared `ErrorFramework` package: a base class, a strategy
registry, a policy DSL, and plugin hooks for logging, metrics, and translation. The design
doc was **19 pages**. The estimate was **3,500 lines** and **6 weeks**.

The cost analysis, run in one hour:

| Cost | Item | Score |
| ---- | ---- | ----- |
| A1 | Implementation | 3,500 |
| A2 | Call-site changes (11 sites × 3) | 66 |
| A3 | 7 new concepts | 21 |
| A4 | 3 hops | 3 |
| A5 | Maintenance (2 owners, ~40 h/quarter) | 2 |
| **A** | | **3,592** |

| Benefit | Item | Score |
| ------- | ---- | ----- |
| B1 | 210 duplicated lines removed | 210 |
| B2 | 9 decision sites collapsed | 18 |
| B3 | 4 observed drift incidents avoided | 12 |
| B4 | Onboarding time saved | 1 |
| B5 | Review time saved | 1 |
| **B** | | **242** |

**NET = +3,350.** The proposal was rejected, and the team was asked for a smaller design. The
replacement was **two files** — an error registry and a mapping table — inside the existing
`@acme/errors` package, which the team had already started. It took **3 days** instead of
6 weeks, and it solved **all four** of the observed drift incidents, because the drift was
always a *mapping* problem, never a *framework* problem.

The lesson recorded in the decision log: **the duplication that motivates an abstraction is
usually narrower than the abstraction proposed to remove it.** Find the narrowest thing that
removes the duplication.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Always extract | Uniform | Costly; over-abstracts | Never as a default |
| Never extract | Simple | Drift; copy-paste | Systems with < 3 copies of any decision |
| Score-based analysis | Repeatable; evidence-based | Takes an hour; can be gamed | Any extraction of a *repeated* decision |
| Intuition only | Fast | Argument-driven; hindsight-blind | Trivial local helpers |
| Post-hoc review | Catches over-abstraction late | Cost already paid | Legacy frameworks only |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Run the analysis before writing the code | Write the framework and analyse it later |
| Count call sites precisely | Assume "several" is enough |
| Weight new vocabulary heavily | Ignore the cost of a new word |
| Re-scope a rejected extraction and re-run | Abandon the goal when the first design fails |
| Require observed drift as evidence | Count hypothetical drift as a benefit |
| Keep the analysis in the PR description | Run it once and forget the numbers |

## Common mistakes

- **Analysing the wrong subject.** "Centralise error handling" is not a subject. "Map a
  Postgres unique violation to a conflict" is.
- **Counting implementation lines as the only cost.** The indirection and vocabulary costs
  dominate in every framework that has ever been built.
- **Ignoring maintenance cost.** A1 is a one-time cost; A5 recurs forever, and it is paid by
  someone who did not write the abstraction.
- **Using the analysis to justify a predetermined answer.** "Let us score it 10 points" is
  not scoring.
- **Never re-running it.** An abstraction adopted by 3 services must be re-analysed at 6.

## Checklist

- [ ] The subject is written as a question plus a subject key.
- [ ] The call sites are counted, not estimated.
- [ ] The arguments at every call site are listed and compared.
- [ ] New vocabulary is named and counted.
- [ ] The removal test has been performed.
- [ ] The net score is ≤ 0, or the design was re-scoped and re-scored.
- [ ] The drift benefit is backed by an observed divergence, not a hypothesis.

## Related

- [Extracting Policies Without Over-Abstraction](../01-concepts/02-extracting-policies-without-over-abstraction.md)
- [When Abstractions Earn Their Cost](./02-when-abstractions-earn-their-cost.md)
- [Finding and Measuring Repetition](../01-concepts/01-finding-and-measuring-repetition.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
