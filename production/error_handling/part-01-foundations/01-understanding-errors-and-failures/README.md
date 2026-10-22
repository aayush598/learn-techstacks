# Chapter 1 — Understanding Errors and Failures

> Part I · _Estimated reading time: 55–75 min_
> **Prerequisite:** none

## One-sentence summary

An **error** is a state, a **fault** is its cause, and a **failure** is its observable effect —
and production-grade handling begins the moment you stop treating those three words as synonyms.

## Why this chapter matters

Teams that blur these concepts ship systems where a database outage is "handled" the same way as
a missing form field. The result is retried invalid input, swallowed outages, lost payments, and
alerts that cry wolf. Precise vocabulary is not pedantry — it is the input to every routing,
retry, and disclosure decision you will make for the rest of this book.

## Chapter map

The chapter has 18 sections. They are grouped into five files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-error-fault-failure-exception.md`](./01-concepts/01-error-fault-failure-exception.md) | 1.1–1.3 | The core vocabulary and why the distinction matters |
| [`01-concepts/02-the-fifteen-dimensions.md`](./01-concepts/02-the-fifteen-dimensions.md) | 1.4–1.15 | The twelve classification axes of any failure |
| [`02-deep-dive/01-failure-domains-and-fault-boundaries.md`](./02-deep-dive/01-failure-domains-and-fault-boundaries.md) | 1.16, 1.18 | Failure domains, blast radius, what "production-grade" means |
| [`03-practical-examples/01-cost-of-poor-error-handling.md`](./03-practical-examples/01-cost-of-poor-error-handling.md) | 1.17 | Concrete money/reputation cost with real-world scenarios |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Cheat sheet, decision table, chapter glossary |

## Learning objectives

By the end you can:

- Define error, fault, failure, and exception and use each correctly.
- Place any real failure on all fifteen classification dimensions in under a minute.
- Explain a failure domain and estimate blast radius.
- Justify why a given failure should fail-fast, fail-safe, retry, degrade, or terminate.

## Key takeaways

1. **Fault → Error → Failure** is a causal chain: fix faults, detect errors, contain failures.
2. **Classification drives policy.** Retry/validate/degrade/alert are direct consequences of the
   dimensions in `01-concepts/02-the-fifteen-dimensions.md`.
3. **Failures propagate across boundaries**, so boundaries — not individual lines — are where you
   design containment.
4. **Poor error handling costs money** through downtime, data loss, support load, and security

## Exercises

1. Take three recent incidents from your own product and label each as fault, error, and failure.
2. For each of the 15 dimensions, write one example from your system.
3. Draw your request's path and mark every boundary it crosses.

## Related

- [Chapter 2 — Principles of High-Quality Error Handling](../02-principles-of-high-quality-error-handling/README.md)
- [Part II — Error Taxonomy](../../part-02-error-taxonomy/README.md)
- [Glossary: error, fault, failure](../../GLOSSARY.md)
