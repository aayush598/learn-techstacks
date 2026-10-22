# 01-concepts — Output Prediction Patterns

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 30 min_

## What lives here

The **what**: the evaluation-order model (12 constructs, one rule each) and the three-way taxonomy
(compile error / runtime exception / normal output).

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-the-evaluation-order-model.md](01-the-evaluation-order-model.md) | 285 | The master order, 12 rules with tables: init order, `super()` first, overload resolution, short-circuit, `++`/`--`, compound assignment, boxing/cache/`==`, switch fall-through, for vs for-each, break/continue/labels, `instanceof`/cast, numeric promotion and char arithmetic |
| [02-compile-vs-run-taxonomy.md](02-compile-vs-run-taxonomy.md) | 181 | The three states, the 10-second decision, the 5 compile-error families, the widening/narrowing table, the 6 runtime exceptions, how to read the exam's options |

## Read in this order

1. `01-the-evaluation-order-model.md` — this is the core. Read it twice.
2. `02-compile-vs-run-taxonomy.md` — you need it for the "does it compile?" archetype.

## Related

- [Topic overview](../README.md)
- [Techniques: 10-second triage](../02-techniques/01-ten-second-triage.md)
