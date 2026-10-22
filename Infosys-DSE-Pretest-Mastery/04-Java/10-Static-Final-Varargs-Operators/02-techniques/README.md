# 02-techniques — Static, Final, Varargs & Operators

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 9 min_

## What lives here

The **how**: six lookup tables that turn any "which overload / which operator / what value?"
question into a table read, plus the 60-second procedure that uses them.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-decision-tables-for-overloads-and-operators.md](01-decision-tables-for-overloads-and-operators.md) | 174 | Table 1 overload resolution, Table 2 `==` on two objects, Table 3 the caches, Table 4 rounding, Table 5 division and modulo, Table 6 compound assignment, the 6-step 60-second procedure, a worked overload example |

## The 6 steps

1. Is it a method call? → Table 1.
2. Is it `==`? → Table 2, then Table 3 if both sides are wrappers.
3. Is it a rounding function? → Table 4.
4. Is it `/` or `%`? → Table 5.
5. Is it `+=` or similar? → Table 6.
6. Is it `static`/`final`? → the constant-variable rule.

## Related

- [Topic overview](../README.md)
- [Concepts: varargs and wrapper types](../01-concepts/02-varargs-and-wrapper-types.md)
