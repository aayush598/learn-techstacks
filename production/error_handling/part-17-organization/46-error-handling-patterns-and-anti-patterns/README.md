# Chapter 46 — Error-Handling Patterns and Anti-Patterns

> Part XVII · _Estimated reading time: 80–100 min_
> **Prerequisite:** [Chapter 45 — Organizing Error-Handling Modules](../45-organizing-error-handling-modules/README.md), [Chapter 13 — Catch Blocks and Recovery Logic](../../part-05-exception-mechanics/13-catch-blocks-and-recovery-logic/README.md)

## One-sentence summary

Every production codebase converges on a small set of recurring **structural patterns** (global
handler, adapter, result type, registry, translation, retry, breaker, fallback, boundary,
compensation, fail-fast, fail-safe) and an equally small set of recurring **anti-patterns**
(empty catch, swallow-and-continue, success-shaped failures, retry-everything…) — so this
chapter names both catalogs, teaches selection between the patterns, and shows the before/after
refactors that remove the anti-patterns.

## Why this chapter matters

You have already seen the architecture (Parts III–IV) and the placement rules (Chapter 45). What
kills implementations in practice is *repetition of the same small mistakes*: a catch that logs
and drops, a retry loop pasted at every call site, a 200 response carrying
`{"success": false}`. These are not exotic — they are the modal defects in error-handling code
review. A shared vocabulary lets your team say "that's 46.22" and refactor in one sitting
instead of re-litigating design every PR. The patterns half of the chapter is equally
pragmatic: most systems need ~12 patterns and nothing more.

## Chapter map

The chapter has 26 sections. They are grouped into eleven files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-structural-patterns.md`](./01-concepts/01-structural-patterns.md) | 46.1, 46.2, 46.9, 46.10 | Global handler, error adapter, error boundary, compensation |
| [`01-concepts/02-modeling-patterns.md`](./01-concepts/02-modeling-patterns.md) | 46.3, 46.4, 46.5 | Result type, code registry, translation |
| [`01-concepts/03-resilience-and-control-flow-patterns.md`](./01-concepts/03-resilience-and-control-flow-patterns.md) | 46.6, 46.7, 46.8, 46.11, 46.12, 46.26 | Retry policy, circuit breaker, fallback, fail-fast, fail-safe, and the simplest pattern |
| [`01-concepts/04-handling-anti-patterns.md`](./01-concepts/04-handling-anti-patterns.md) | 46.13–46.16, 46.18, 46.19, 46.21, 46.22 | The eight code-level anti-patterns: catch-all, empty catch, swallow-and-continue, exception-driven flow, generic messages, deep wrappers, catch-log-without-rethrow, success-shaped failures |
| [`01-concepts/05-design-anti-patterns.md`](./01-concepts/05-design-anti-patterns.md) | 46.17, 46.20, 46.23, 46.24, 46.25 | The five design-level anti-patterns: excessive custom classes, repeated retry logic, retry-all, retry-non-idempotent, overengineering |
| [`02-deep-dive/01-pattern-selection-trade-offs.md`](./02-deep-dive/01-pattern-selection-trade-offs.md) | 46.1–46.12 (selection) | Result vs exception, global vs local, retry vs compensate, breaker vs fallback — decision tables |
| [`02-deep-dive/02-anti-pattern-compounding-and-remediation.md`](./02-deep-dive/02-anti-pattern-compounding-and-remediation.md) | 46.13–46.25 (remediation) | How anti-patterns compound into incidents, and the ordered remediation playbook |
| [`03-practical-examples/01-acme-patterns-wired-in.md`](./03-practical-examples/01-acme-patterns-wired-in.md) | 46.1–46.12 (applied) | All twelve patterns wired into one Acme request + job + saga path |
| [`03-practical-examples/02-before-after-anti-pattern-refactors.md`](./03-practical-examples/02-before-after-anti-pattern-refactors.md) | 46.13–46.25 (applied) | Six before/after refactors straight from Acme's backlog |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | 46.1–46.26 | Per-family do/don't tables for the twelve patterns, the full anti-pattern catalog (46.13–46.26) with symptom/cause/fix, review questions, escalation criteria, chapter checklist |
| [`05-reference/README.md`](./05-reference/README.md) | 46.1–46.26 | Pattern-selection decision table, anti-pattern quick reference, the "simplest pattern that satisfies the requirement" rule, status mapping, chapter glossary + signposts |

## Learning objectives

By the end you can:

- Name and place all twelve patterns; for each, state what problem it solves and what it must
  not be asked to do.
- Select between competing patterns (result vs throw, global vs local handler, retry vs
  compensation) using explicit trade-off criteria, not habit.
- Recognize all thirteen anti-patterns on sight and execute the matching before/after refactor.
- Audit a codebase: produce a list of live anti-pattern instances ranked by incident risk.

## Key takeaways

1. **Twelve patterns are enough.** A production SaaS typically needs: one global handler, one
   adapter per vendor, one registry, one serializer per transport, named retry policies, a
   breaker per critical dependency, fallbacks for optional features, boundaries per request/job,
   and compensations per saga. Everything else is local `try/catch` on typed errors.
2. **Anti-patterns cluster.** Empty catch → swallow-and-continue → success-shaped failures are
   one disease at three severities; treat the cluster, not the line.
3. **Retries are where money burns.** 46.23 and 46.24 (retry-all, retry-non-idempotent) turn
   provider incidents into double-charges and storms; they are the highest-severity
   anti-patterns in this chapter.
4. **Overengineering is also an anti-pattern** (46.25). The bar for a new abstraction is three
   call sites and a measured saving — the simplest pattern (46.26) is a legitimate, production-
   grade destination.

## Exercises

1. Grep your repo for `catch` blocks with only a `console.log` (46.21) and empty catches
   (46.14). Count them; file one refactor PR per count of ten.
2. Find every retry loop (`attempt`, `retry`, `for` near a catch). List which reference a
   named policy (46.6) and which inline numbers (46.20).
3. For each API endpoint returning 200, check whether any 200 body carries
   `success: false` or an `error` field (46.22). Those are contract bugs.
4. Sketch which of the twelve patterns your system already has, one per name. The gaps are your
   roadmap — resist filling gaps with machinery you do not need (46.25).

## Related

- [Chapter 45 — Organizing Error-Handling Modules](../45-organizing-error-handling-modules/README.md)
- [Choosing Between Competing Approaches](../../part-22-design-decisions/56-choosing-between-competing-approaches/README.md)
- [Anti-pattern entries in the master catalog](../../part-24-repeatable-blueprint/62-final-reference-materials/README.md)
