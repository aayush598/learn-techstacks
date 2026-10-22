# 01-concepts — Strings, Immutability, equals & hashCode

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 21 min_

## What lives here

The **what**: why `String` is immutable, what the string pool is and when a string lands in it, and
the exact `equals` / `hashCode` / `compareTo` semantics.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-string-immutability-and-pool.md](01-string-immutability-and-pool.md) | 237 | Immutability and its 3 consequences, the pool table, `intern()`, constant folding and constant variables, `StringBuilder` vs `StringBuffer`, `substring` in Java 6 vs 7+, `valueOf` vs `toString` vs `+`, `char[]` vs `String` |
| [02-equals-hashcode-and-comparison.md](02-equals-hashcode-and-comparison.md) | 218 | The comparison-operator table, `compareTo` return values, the equals/hashCode contract in both directions, the `String.hashCode` formula with a worked number, the null behaviour table, `HashSet` de-duplication |

## Read in this order

1. `01-string-immutability-and-pool.md` — the pool rules decide every `==` question.
2. `02-equals-hashcode-and-comparison.md` — the contract decides every `hashCode` question.

## Related

- [Topic overview](../README.md)
- [Techniques: string API decision table](../02-techniques/01-string-api-decision-table.md)
