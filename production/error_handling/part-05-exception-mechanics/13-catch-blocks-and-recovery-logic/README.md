# Chapter 13 — Catch Blocks and Recovery Logic

> Part V · _Estimated reading time: 55–75 min_
> **Prerequisite:** [Chapter 12 — Exception Propagation and Control Flow](../12-exception-propagation-and-control-flow/README.md)

## One-sentence summary

A `catch` block is not "where errors go to be quiet" — it is a **decision point** where you choose
to recover, translate, rethrow, or terminate, and every choice must leave the system's state
valid.

## Why this chapter matters

Most production error-handling defects live inside catch blocks: the empty catch that swallows an
outage, the broad `catch (Exception)` that hides a bug, the recovery path that corrupts state, the
retry that recurses forever. Catch blocks are where good intentions go wrong. This chapter gives
you a decision procedure for *whether* to catch, *what* to catch, and *what to do* when you do.

## Chapter map

The chapter has 17 sections, grouped into 10 files:

| File | Subsections covered | What you learn |
| ---- | ------------------- | -------------- |
| [`01-concepts/01-when-to-catch-and-when-not.md`](./01-concepts/01-when-to-catch-and-when-not.md) | 13.1, 13.2, 13.17 | The decision to catch; catches as architecture |
| [`01-concepts/02-catching-specific-types-and-categories.md`](./01-concepts/02-catching-specific-types-and-categories.md) | 13.3, 13.4, 13.5 | Specific types, multiple categories, known vs unknown |
| [`01-concepts/03-recovery-inside-catch.md`](./01-concepts/03-recovery-inside-catch.md) | 13.6, 13.7, 13.8, 13.14, 13.15, 13.16 | Recovery, rethrow after partial recovery, translation, preconditions, state safety, decide |
| [`01-concepts/04-catch-anti-patterns.md`](./01-concepts/04-catch-anti-patterns.md) | 13.9, 13.10, 13.11, 13.12, 13.13 | Empty catch, broad suppression, repeated catch/rethrow, errors in recovery, recursion |
| [`02-deep-dive/01-typed-handlers-and-discrimination.md`](./02-deep-dive/01-typed-handlers-and-discrimination.md) | mechanics | Typed handlers, pattern matching, discriminating known failures |
| [`02-deep-dive/02-recovery-failure-and-recursion.md`](./02-deep-dive/02-recovery-failure-and-recursion.md) | mechanics | When recovery itself fails; preventing loops |
| [`03-practical-examples/01-typed-catch-and-recovery-patterns.md`](./03-practical-examples/01-typed-catch-and-recovery-patterns.md) | 13.3–13.8 | ts, python, go, java catch patterns |
| [`03-practical-examples/02-recovery-preconditions-and-state-guards.md`](./03-practical-examples/02-recovery-preconditions-and-state-guards.md) | 13.14–13.16 | Preconditions, state validation, rollback-before-recover |
| [`04-dos-and-donts/README.md`](./04-dos-and-donts/README.md) | all | Rules of thumb and anti-patterns |
| [`05-reference/README.md`](./05-reference/README.md) | all | Catch-vs-propagate decision tree, glossary |

## Learning objectives

By the end you can:

- Decide whether a given catch block should exist at all.
- Catch the most specific type and handle multiple known categories without a catch-all.
- Design recovery that fails safely and does not corrupt state.
- Recognize and fix empty catches, broad suppression, and infinite recovery loops.

## Key takeaways

1. **A catch block is an architectural decision.** It decides the observable outcome of a failure;
   put it where you have enough information (13.17).
2. **Catch the specific, plan for the unknown.** Handle known categories explicitly; log and
   rethrow the rest (13.3–13.5).
3. **Recovery may be partial.** If you recovered the resource but not the operation, rethrow with
   the cause and note what was already done (13.7).
4. **Validate before you recover.** Check preconditions; recovery that assumes good state corrupts
   data (13.14–13.15).
5. **Recovery can fail and can loop.** Attach secondary failures; bound retries; never recurse
   unbounded (13.12–13.13).

## Exercises

1. List every `catch` in one service and label it: recover / translate / rethrow / delete.
2. Find a catch that suppresses broadly; name the specific error it hides.
3. Take a recovery path and write its preconditions explicitly.

## Related

- [Chapter 12 — Exception Propagation and Control Flow](../12-exception-propagation-and-control-flow/README.md)
- [Chapter 14 — Resource Cleanup and Failure-Safe Execution](../14-resource-cleanup-and-failure-safe-execution/README.md)
- [Part VI — Error Boundaries and Translation](../../part-06-boundaries-and-translation/README.md)
- [Glossary: recover, propagate, terminate](../../GLOSSARY.md)
