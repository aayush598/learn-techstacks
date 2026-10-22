# 02-techniques — Output Prediction Patterns

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 21 min_

## What lives here

The **how**: a 10-second triage procedure, the exact-output contract, the overload-resolution
tables, and the short-circuit / `++` / compound-assignment rule sets.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-ten-second-triage.md](01-ten-second-triage.md) | 203 | The 6-step triage, the 12 triage markers, the number-to-string table, 7 question shapes with their fastest attack, the "guess the option shape" shortcut, the threads exception |
| [02-method-resolution-and-short-circuit.md](02-method-resolution-and-short-circuit.md) | 239 | The 3 overload phases, the classic four-way overload table, varargs rules, short-circuit truth tables, `++` semantics, compound-assignment cast rules, `instanceof`/cast rules, ternary typing table |

## Use them like this

1. **Any output question** → `01-ten-second-triage.md`, 6 steps, ~50 s.
2. **"Which method is called?"** → `02-method-resolution-and-short-circuit.md`, phase table.
3. **Anything with `++`, `&&`, `||`, `?:`** → the same file's rule tables.

## Related

- [Topic overview](../README.md)
- [Concepts: the evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
