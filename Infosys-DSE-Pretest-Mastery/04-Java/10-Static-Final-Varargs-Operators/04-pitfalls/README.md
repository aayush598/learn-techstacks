# 04-pitfalls — Static, Final, Varargs & Operators

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 12 min_

## What lives here

12 traps, each written as **the wrong answer you will pick → the right answer → the one-line
guard**. Every trap here appears as a real distractor in the exam.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-static-final-varargs-traps.md](01-static-final-varargs-traps.md) | 136 | The 12-trap table, the trap groups, the rounding trap on exact halves, the two-sided `%` trap, the `final` + mutability trap, a worked trap, and the checklist |

## The 12 traps in one line each

1. Static blocks run at program start → first use.
2. A static block sees the final field value → it sees the value at that point in source order.
3. Instance initialiser runs after the constructor → it runs before.
4. A method call is a constant expression → it is not.
5. Boxing beats widening → widening comes first.
6. Varargs beats widening → varargs is last.
7. `Integer` 128 is cached → only −128..127.
8. `Integer + Integer` adds → it concatenates.
9. `final` makes the array immutable → it freezes the reference.
10. `Math.round(-2.5)` is `-3` → it is `-2`.
11. `-7 / 2` floors to `-4` → it truncates to `-3`.
12. `>>>` preserves the sign → it zero-fills.

## Related

- [Topic overview](../README.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
