# The Multi-Axis Classification Model

> Part II · Chapter 4 · Sections 4.2–4.16 · _Estimated reading time: 22 min_
> **Prerequisite:** [Classification Axes: Origin through Retry](../01-concepts/02-classification-axes-origin-through-retry.md)

## In one sentence

Every error is a **point in multi-dimensional space**, but routing requires a single **primary
axis**; the skill is choosing the primary axis deliberately and deriving the rest.

## Why this matters in production

When two engineers classify the same failure differently, it is almost always because they picked
different primary axes without saying so. One called a Stripe `429` an `external_api` error; the
other called it a `rate_limit` error. Both are true. If the routing table expects one, the other
falls through to `500`. A documented primary-axis convention removes the ambiguity.

## Core concept — axes vs categories vs tags

Keep three things separate:

| Concept | Cardinality | Purpose |
| ------- | ----------- | ------- |
| **Axis** | the dimension (e.g. permanence) | Describe |
| **Axis value** | one of many (e.g. transient) | Describe |
| **Primary category** | exactly one | Route |
| **Tags** | zero or more | Enrich/filter |

```text
A Stripe 429:
  axes   = { origin: dependency, permanence: transient, dependency: stripe, domain: billing }
  primary_category = rate_limit
  tags   = ["transient", "retryable", "dependency:stripe", "external"]
  derived = { http: 429, retry: true, alert: warn, sensitive: false }
```

The same axes exist on *every* error; only the **primary category** is chosen.

## How it works — choosing the primary axis

Use a fixed precedence so classification is deterministic:

```text
1. Is it a defect in our code/runtime?        → runtime / internal_programming
2. Is it an input/contract problem?            → validation / parsing / auth / authz
3. Is it a business-rule outcome?              → business_rule / conflict / state_transition / not_found
4. Is it resource/limit related?               → rate_limit / quota / resource_exhaustion
5. Is it a dependency/network problem?         → external_api / network / timeout / cache / database
6. Is it asynchronous job/partial related?     → background_job / partial / compensation
7. Otherwise                                    → unexpected_runtime
```

This is a **first-match** tree: stop at the first "yes". It guarantees one primary category per
error while preserving all the descriptive axes as tags.

> ⚠️ **Hazard.** Do not let the *HTTP status* choose the category. A vendor can return `400` for a
> transient problem; classify by cause, then derive the status.

## Deriving the rest

Once the primary category is fixed, everything else is a **pure function** of it plus context:

```ts
function derivePolicy(category: Category, ctx: Context): Policy {
  const base = CATEGORY_POLICY[category];        // fixed table
  return {
    http: base.http,
    retryable: base.retryable && ctx.idempotent,  // retry adds idempotency
    alert: ctx.impact === "data_loss" ? "page" : base.alert,
    redact: base.sensitive || ctx.hasPii,
  };
}
```

No handler should ever recompute the HTTP status or retry verdict by hand — that is how
inconsistency is born.

## Worked example — three ways to classify one timeout

Acme calls the LLM provider for a summary. It times out after 10s.

| Choice of primary | Tags | Derived policy | Comment |
| ----------------- | ---- | -------------- | ------- |
| `timeout` | transient, dependency:llm, optional | retry once, degrade to cached | ✅ best for this feature |
| `external_api` | transient, dependency:llm | retry, then 502 | reasonable but coarser |
| `ai_model` | non-deterministic | provider-specific fallback | too specific for routing |

The convention: **primary = the mechanism (`timeout`)**, **dependency = a tag**, and the *feature*
decides the fallback. This keeps the routing table small.

## Multi-axis classification is idempotent

A classifier must be **idempotent**: classifying an already-classified error returns the same
category, not a new one derived from context.

```ts
function ensureClassified(err: unknown): Categorized {
  if (isCategorized(err)) return err;          // already has a category — trust it
  return categorize(err);                      // classify exactly once
}
```

This single guard eliminates the most common inconsistency: a boundary re-running the classifier
and producing a *different* answer than the origin. Because the category is a property of the
origin's knowledge, only the origin may set it.

## Key data / numbers

- A precedence tree with ~7 levels covers the overwhelming majority of SaaS failures.
- RFC 9457's `type` field is effectively a URI for the **primary category**, which is why the
  taxonomy and the HTTP contract align.
- Keep the category→policy table **data, not code** (a map/JSON) so it can be reviewed and diffed.

```json
{
  "timeout":      { "http": 504, "retryable": true,  "alert": "warn", "sensitive": false },
  "validation":   { "http": 422, "retryable": false, "alert": "none", "sensitive": false },
  "database":     { "http": 500, "retryable": true,  "alert": "page", "sensitive": true }
}
```

## Real-world use case — Acme SaaS

Acme's incidents showed the same Postgres `40001` serialization failure classified as `database`,
`conflict`, and `concurrency` by three teams. The global handler retried two of them and not the
third. After adopting the precedence tree, `40001` is always `database` (primary), tagged
`transient` + `concurrency`. One policy table, one behavior, across services.

## Trade-offs

| Approach | Pros | Cons |
| -------- | ---- | ---- |
| Single category + tags | Deterministic routing | Slight modeling effort |
| Multiple categories | "Expressive" | Ambiguous routing, drift |
| No precedence rule | Flexible | Two engineers, three answers |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Fix a precedence order for primary category | Let each handler choose |
| Store all axes as tags | Collapse axes into the category name |
| Derive policy via a table | Recompute status/retry in code |
| Keep primary based on mechanism | Base it on the calling feature |

## Common mistakes

- **Encoding axes into category names** (`TRANSIENT_EXTERNAL_TIMEOUT`) — combinatorial explosion.
- **Letting the boundary reassign the category** — classify once, at creation.
- **Treating HTTP status as the primary axis** — vendor statuses lie.
- **Forgetting idempotency** when deriving `retryable`.

## Checklist

- [ ] Is there a documented precedence for the primary category?
- [ ] Are all other axes stored as tags?
- [ ] Is the category→policy table a reviewable data file?
- [ ] Does `retryable` incorporate idempotency?

## Related

- [Mutual Exclusivity, Growth, and Governance](../01-concepts/04-mutual-exclusivity-growth-governance.md)
- [Taxonomy Governance and Evolution](./02-taxonomy-governance-and-evolution.md)
- [Classification Decision Tree (Ch. 5)](../../05-error-categories-in-detail/02-deep-dive/02-classification-decision-tree.md)
- [Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
