# 01-concepts — Exceptions & Error Handling

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 19 min_

## What lives here

The **what**: the `Throwable` hierarchy, the checked/unchecked rule, `throw` vs `throws`, custom
exceptions, and the precise semantics of `try` / `catch` / `finally` / try-with-resources.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-throwable-hierarchy-and-checked-vs-unchecked.md](01-throwable-hierarchy-and-checked-vs-unchecked.md) | 186 | The hierarchy tree, checked vs unchecked table, `throw` vs `throws`, custom exception template, the compiler's rule |
| [02-try-catch-finally-and-resource-management.md](02-try-catch-finally-and-resource-management.md) | 233 | The execution table, `finally` vs `return`, `System.exit()`, exception-in-`finally`, try-with-resources, propagation, multi-catch |

## Read in this order

1. `01-throwable-hierarchy-and-checked-vs-unchecked.md` — you need the tree before any catch rule.
2. `02-try-catch-finally-and-resource-management.md` — you need the execution table before any
   output question.

## Related

- [Topic overview](../README.md)
- [Techniques: trace the exception path](../02-techniques/01-trace-the-exception-path.md)
