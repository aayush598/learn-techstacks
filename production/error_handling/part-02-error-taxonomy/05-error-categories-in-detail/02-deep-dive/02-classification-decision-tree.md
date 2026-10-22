# The Classification Decision Tree

> Part II · Chapter 5 · Sections 5.1–5.35 · _Estimated reading time: 20 min_
> **Prerequisite:** [Category Interactions and Overlaps](./01-category-interactions-and-overlaps.md)

## In one sentence

A **first-match decision tree** turns a raw failure into exactly one primary category in a few
questions, so every engineer and every service classifies identically.

## Why this matters in production

Ad-hoc classification is the root of inconsistent policy. A decision tree is the executable
version of the taxonomy: it can be reviewed, unit-tested, and encoded once. If two people walk the
same tree with the same inputs, they get the same category — that is the whole point.

## The tree

```text
START: a failure occurred
 │
 ├─ Did the caller/whoever initiate stop or leave?
 │     └─ YES → cancellation                    [5.27]
 │
 ├─ Is config/env/secret wrong or missing?
 │     └─ YES → configuration                   [5.20]
 │
 ├─ Did a required dependency fail to initialize?
 │     └─ YES → dependency_initialization       [5.21]
 │
 ├─ Is it a defect in our own code/state?
 │     ├─ programmatic (NPE, assertion) → internal_programming [5.25]
 │     └─ otherwise unexpected           → unexpected_runtime   [5.26]
 │
 ├─ Is it an input/contract problem?
 │     ├─ cannot even parse → request_parsing   [5.2]
 │     ├─ parses but invalid → validation       [5.1]
 │     ├─ not authenticated → authentication   [5.3]
 │     └─ not permitted     → authorization    [5.4]
 │
 ├─ Is it a legitimate business outcome?
 │     ├─ rule violated        → business_rule      [5.5]
 │     ├─ does not exist       → not_found          [5.6]
 │     ├─ conflicts with state → conflict           [5.7]
 │     ├─ same op resubmitted  → duplicate_operation[5.8]
 │     └─ invalid for lifecycle→ state_transition   [5.9]
 │
 ├─ Is a limit reached?
 │     ├─ transient rate → rate_limit       [5.10]
 │     ├─ plan/usage     → quota            [5.11]
 │     └─ resource gone  → resource_exhaustion [5.22]
 │
 ├─ Is it a data/store problem?
 │     ├─ race/deadlock (40001/40P01) → concurrency   [5.12]
 │     ├─ constraint/connection       → database      [5.13]
 │     ├─ optional cache              → cache         [5.14]
 │     ├─ object storage              → file_storage  [5.15]
 │     ├─ file content/processing     → file_processing [5.35]
 │     └─ wrong data/invariant        → data_integrity[5.28]
 │
 ├─ Is it an external/remote problem?
 │     ├─ we stopped waiting       → timeout            [5.18]
 │     ├─ connection/DNS/TLS fault → network            [5.17]
 │     ├─ bad serialization        → serialization      [5.19]
 │     ├─ LLM/tool/token limit     → ai_provider/ai_tool/ai_token_limit [5.33]
 │     ├─ webhook delivery         → webhook            [5.34]
 │     └─ generic provider error   → external_api       [5.16]/third_party [5.32]
 │
 ├─ Is it an async/job context?
 │     ├─ job failed                    → background_job [5.23]
 │     ├─ scheduled run missed/overlap  → scheduled_task [5.24]
 │     ├─ some steps done, some not     → partial        [5.29]
 │     ├─ must undo completed step      → compensation   [5.30]
 │     └─ process is going down         → shutdown_lifecycle [5.31]
 │
 └─ DEFAULT → unexpected_runtime [5.26]
```

## How to use it

1. Walk top-to-bottom; **stop at the first match**.
2. Record the matched category as **primary**.
3. Add the other true axes as **tags** (e.g. `partial`, `transient`, `dependency:stripe`).
4. Hand off to the category→policy table (Chapter 4.03 practical example).

Because it is first-match, ordering matters: **cancellation and configuration precede generic
runtime**, and **specific external categories (ai/webhook) precede generic `external_api`**.

## Worked examples

```text
(1) "Postgres 40001 serialization_failure during invoice write"
    config? no → defect? no → input? no → business? no
    data race (40001)? YES → concurrency        tags: [transient, database]

(2) "Stripe webhook signature verification failed (missing header)"
    cancellation? no → config? maybe (secret) → but verify code itself ran
    input/contract? YES → authentication        tags: [external, webhook, sensitive]
    (route to WebhookIngest; public code AUTH_SIGNATURE_INVALID)

(3) "OpenAI returned context_length_exceeded"
    external? YES → ai_token_limit              tags: [external, permanent, ai]
    (NOT timeout, NOT generic external_api)

(4) "Client disconnected mid-export; write may have applied"
    cancellation? YES → cancellation            tags: [ambiguous, partial]
    (do NOT mark failed; reconcile with idempotency key)
```

## Key data / numbers

- The tree has **~7 top-level gates**; most failures resolve in 2–4 questions.
- Encode it as a pure function and unit-test each branch with a fixture — classification bugs then
  become test failures, not incidents.
- Ambiguity (`unknown` transactional outcome) is recorded as a **tag**, never as a separate
  category.

## Real-world use case — Acme SaaS

Acme had three services classify the same provider `429` as `rate_limit`, `external_api`, and
`quota`. The decision tree fixed the order: limit reached → transient → `rate_limit`; if the code
indicates plan limits, `quota`. One pure function, shared across services, and the disagreement
disappeared in a sprint.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| Decision tree function | Deterministic, testable | Requires maintenance |
| Human judgment | Flexible | Inconsistent |
| Status-code mapping | Trivial | Wrong for shared codes |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| First-match, documented order | Let each service reorder |
| Unit-test every branch | Trust classification untested |
| Default to `unexpected_runtime` | Leave a failure uncategorized |
| Record ambiguity as a tag | Invent a new category for it |

## Common mistakes

- **Wrong ordering** — checking `unexpected_runtime` before specifics.
- **Middle-of-tree categories** (partial) treated as leaves that shadow the real cause.
- **Two divergent trees** in two services.
- **No default branch** — unclassified failures default to `500` with no code.

## Checklist

- [ ] Is the tree a single shared function?
- [ ] Is ordering documented and reviewed?
- [ ] Is every branch unit-tested?
- [ ] Is there a guaranteed default category?

## Related

- [Category Interactions and Overlaps](./01-category-interactions-and-overlaps.md)
- [The Multi-Axis Classification Model (Ch. 4)](../../04-designing-a-comprehensive-error-taxonomy/02-deep-dive/01-multi-axis-classification-model.md)
- [Taxonomy in Code](../03-practical-examples/01-taxonomy-in-code.md)
