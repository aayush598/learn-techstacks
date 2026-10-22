# 01-concepts — Static, Final, Varargs & Operators

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 33 min_

## What lives here

The **what**: what `static` does to a member's lifetime, what `final` freezes, what a compile-time
constant is, how varargs and autoboxing change overload resolution, and how Java's operators
actually group.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-static-and-final.md](01-static-and-final.md) | 241 | The static-vs-instance table, class initialisation order with a traced example, the four flavours of `final`, the three conditions of a constant variable, blank finals, effectively final, `static final`, static imports |
| [02-varargs-and-wrapper-types.md](02-varargs-and-wrapper-types.md) | 214 | The 6 varargs rules, the array-vs-varargs overload trap, the ambiguity trap, the 9 wrapper types and autoboxing, the 5 places autoboxing bites, the −128..127 `Integer` cache, the `Boolean`/`Character`/`Double` caches |
| [03-operator-precedence-and-arithmetic.md](03-operator-precedence-and-arithmetic.md) | 273 | The 13-level precedence ladder, associativity rules, integer division and modulo sign, bitwise operators, `&&` vs `&`, compound assignment with the cast rule, ternary numeric promotion, `instanceof`, the full `Math` table |

## Read in this order

1. `01-static-and-final.md` — the init order and the constant-variable rule.
2. `02-varargs-and-wrapper-types.md` — varargs and the cache.
3. `03-operator-precedence-and-arithmetic.md` — the ladder and the sign rules.

## Related

- [Topic overview](../README.md)
- [Techniques: decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
