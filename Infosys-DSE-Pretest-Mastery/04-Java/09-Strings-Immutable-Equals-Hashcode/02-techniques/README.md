# 02-techniques — Strings, Immutability, equals & hashCode

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 10 min_

## What lives here

The **how**: a method-by-method decision table for "which method does X" questions, the regex vs
literal rules, the null-safety table, and a 60-second procedure.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-string-api-decision-table.md](01-string-api-decision-table.md) | 219 | The main decision table (20 rows), `replace` vs `replaceAll` with examples, `matches` vs `find`, the `split` regex and trailing-empty rules, `trim` vs `strip`, the null-safety table, text blocks, the 5-step "which method?" procedure, worked example |

## Use it like this

1. Read the decision table row that matches the question's intent.
2. Check the "Gotcha" column.
3. Check the null-safety table if a `null` is involved.

## Related

- [Topic overview](../README.md)
- [Concepts: string immutability and the pool](../01-concepts/01-string-immutability-and-pool.md)
