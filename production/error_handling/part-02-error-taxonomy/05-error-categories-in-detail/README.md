# Chapter 5 — Error Categories in Detail

> Part II · _Estimated reading time: 90–120 min_
> **Prerequisite:** [Chapter 4 — Designing a Comprehensive Error Taxonomy](../04-designing-a-comprehensive-error-taxonomy/README.md)

## One-sentence summary

This chapter is the **catalog**: all 35 error categories a SaaS actually encounters, each with its
trigger, real codes, default HTTP mapping, retry verdict, and the recurring-cast scenario that
exercises it.

## Why this chapter matters

Chapter 4 gave you the axes. This chapter gives you the values. Most "we handled it wrong"
incidents come from misclassifying one of these 35 categories — retrying a `409 conflict`,
alerting on a declined card, returning `500` for a validation error, or swallowing a partial
completion. Recognizing the category by name is the fastest path to the right policy.

## Chapter map

The 35 sections are grouped into five files by family:

| File | Subsections covered | Family |
| ---- | ------------------- | ------ |
| [`01-concepts/01-input-auth-and-business-errors.md`](./01-concepts/01-input-auth-and-business-errors.md) | 5.1–5.9 | Input, auth, and business rules |
| [`01-concepts/02-limits-concurrency-and-data.md`](./01-concepts/02-limits-concurrency-and-data.md) | 5.10–5.15, 5.28 | Limits, concurrency, and persistence |
| [`01-concepts/03-external-network-and-config.md`](./01-concepts/03-external-network-and-config.md) | 5.16–5.21, 5.32 | External, network, config, dependencies |
| [`01-concepts/04-runtime-lifecycle-and-resources.md`](./01-concepts/04-runtime-lifecycle-and-resources.md) | 5.22, 5.25–5.27, 5.31 | Runtime, resources, and lifecycle |
| [`01-concepts/05-async-jobs-partial-and-specialized.md`](./01-concepts/05-async-jobs-partial-and-specialized.md) | 5.23, 5.24, 5.29, 5.30, 5.33–5.35 | Async jobs, partial failure, specialized SaaS |
| [`02-deep-dive/01-category-interactions-and-overlaps.md`](./02-deep-dive/01-category-interactions-and-overlaps.md) | 5.1–5.35 | Where categories overlap and how to disambiguate |
| [`02-deep-dive/02-classification-decision-tree.md`](./02-deep-dive/02-classification-decision-tree.md) | 5.1–5.35 | A decision tree from raw failure to category |
| [`03-practical-examples/01-taxonomy-in-code.md`](./03-practical-examples/01-taxonomy-in-code.md) | 5.1–5.35 | The full category catalog as code + a classifier |
| [`03-practical-examples/02-scenario-classification-drills.md`](./03-practical-examples/02-scenario-classification-drills.md) | all | Worked drills with the recurring cast |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules and anti-patterns per family |
| [`05-reference/README.md`](./05-reference/README.md) | all | Big category cheat-sheet with codes and policies |

## Learning objectives

By the end you can:

- Name the category of any failure and state its default HTTP status and retry verdict.
- Recognize when a failure belongs to two categories and pick the **dominant** one.
- Map each category to a **stable app code** (e.g. `PAYMENT_CARD_DECLINED`) — the bridge to
  Chapter 8.
- Distinguish categories that look alike: `conflict` vs `duplicate operation` vs
  `concurrency/optimistic locking`; `timeout` vs `network` vs `external API`.
- Apply the specialized categories (webhook, file upload, AI/tool) that generic frameworks miss.

## Key takeaways

1. **Category ≠ message.** A `23505` is `duplicate operation` regardless of its SQL text.
2. **The same HTTP status hides many categories.** `409` covers conflict, duplicate, state
   transition, and optimistic locking — the app code disambiguates.
3. **Retry verdict is a property of the category**, not of the endpoint.
4. **Specialized categories are where systems fail silently** — AI token limits, webhook replays,
   partial multipart uploads.
5. **Every category should exist in Chapter 4's taxonomy** with an owner.

## Exercises

1. Pick five categories and find a real occurrence of each in your logs.
2. For each of your public API endpoints, list which categories can occur.
3. Take three errors currently sharing one generic code and assign distinct app codes.
4. Classify a partial `Checkout` failure across every category it touches.

## Related

- [Chapter 4 — Designing a Comprehensive Error Taxonomy](../04-designing-a-comprehensive-error-taxonomy/README.md)
- [Chapter 8 — Error Codes and Error Registries](../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Glossary: error taxonomy, error code](../../GLOSSARY.md)
