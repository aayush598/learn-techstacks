# 02-techniques — Exceptions & Error Handling

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 16 min_

## What lives here

The **how**: a step-by-step trace procedure, an implicit-throw lookup table, a compile-vs-run
triage, and the catch-matching/ordering decision tables.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-trace-the-exception-path.md](01-trace-the-exception-path.md) | 202 | The 6-step trace, the 4 question types and the steps each needs, compile-vs-run triage, the 45-second output table |
| [02-choose-the-right-catch-strategy.md](02-choose-the-right-catch-strategy.md) | 199 | Catch matching rule, ordering rule, the 3 catch compile-error families, multi-catch rules, "what should I catch" decision table, cause chains |

## Use them like this

1. **Output question** → `01-trace-the-exception-path.md`, 6 steps, ~60 s.
2. **"Which catch?" question** → `02-choose-the-right-catch-strategy.md`, matching table + ordering
   rule.
3. **"Does it compile?" question** → the triage box in `01-trace-the-exception-path.md`, then the
   three compile-error families in `02`.

## Related

- [Topic overview](../README.md)
- [Concepts: try/catch/finally](../01-concepts/02-try-catch-finally-and-resource-management.md)
