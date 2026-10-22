# Static, Final, Varargs & Operators — One-Page Revision Sheet

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 5 min_
> **Prerequisite:** [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)

## In one sentence

Print this page and this topic collapses to **four tables**: initialisation order, constant
variables, overload phases, and the arithmetic sign rules.

## Why the pre-test tests this

Static/`final`/varargs/operator questions are mechanical once you own the tables. They are the
cheapest marks in Section 4 — take them all.

## Core concept

### Table 1 — initialisation order

| Phase | What runs | When |
|---|---|---|
| 1 | Superclass static initialisers | first use of the subclass |
| 2 | Static field initialisers + static blocks, **textual order** | first use of the class |
| 3 | Superclass constructor body | at `new` |
| 4 | Instance field initialisers + instance blocks, **textual order** | at `new` |
| 5 | Constructor body | at `new` |

### Table 2 — constant variable

| Requirement | Yes | No |
|---|---|---|
| `final` | `final int A = 10;` ✅ | `int A = 10;` ❌ |
| Type is primitive or `String` | `final int A = 10;` ✅ | `final Object O = new Object();` ❌ |
| Initialiser is a constant expression | `final int B = A * 2;` ✅ | `final int C = m();` ❌ |

All three ⇒ the value is **inlined at compile time**.

### Table 3 — overload phases (first match wins)

| Phase | Rule |
|---|---|
| 1 | exact match |
| 2 | widening primitive |
| 3 | widening reference |
| 4 | boxing (+ widening) |
| 5 | varargs |

### Table 4 — the arithmetic sign rules

| Expression | Result |
|---|---|
| `7 / 2` | `3` |
| `-7 / 2` | `-3` |
| `7 % 2` | `1` |
| `-7 % 2` | `-1` |
| `7 % -2` | `1` |
| `-7 % -2` | `-1` |
| `Math.round(2.5)` | `3` |
| `Math.round(-2.5)` | `-2` |
| `Math.floor(-2.5)` | `-3.0` |
| `Math.ceil(-2.5)` | `-2.0` |
| `-8 >> 1` | `-4` |
| `-8 >>> 1` | `2147483644` |

### Table 5 — the caches

| Type | Cache |
|---|---|
| `Integer` / `Long` / `Short` | −128..127 |
| `Byte` | all values |
| `Character` | 0..127 |
| `Boolean` | `TRUE`, `FALSE` |
| `Double` / `Float` | **none** |

### Table 6 — varargs rules

| Rule | Detail |
|---|---|
| Syntax | `int... xs` ≡ `int[] xs` |
| Position | must be **last** |
| Count | only **one** per method |
| Zero args | gives an **empty array**, not `null` |
| Priority | **last** phase of overload resolution |

### 60-second budget

| Phase | Seconds | Action |
|---|---|---|
| Classify | 10 | static? final? varargs? wrapper? operator? |
| Table lookup | 20 | Tables 1–6 |
| Sanity check | 15 | signs, cache range, phase order |
| Write | 15 | exact value |
| **Total** | **~60** | |

## Worked example

**Q. What is printed?**

```java
class A {
    static int x = 10;
    static { x += 5; }
    static int y = x * 2;
}
public class Main {
    public static void main(String[] args) {
        System.out.println(A.y + " " + A.x);
        Integer a = 128, b = 128;
        System.out.println(a == b);
        System.out.println(Math.round(-2.5));
    }
}
```

**Output (exact):**

```
30 15
false
-2
```

## Quick rules

- Static init: first use, superclass first, textual order.
- Instance init: initialisers → instance blocks → constructor body.
- Constant variable = `final` + primitive/`String` + constant expression.
- Overloads: exact → widening → boxing → varargs.
- `Integer` cache = −128..127.
- `+` concatenates if any operand is a `String`.
- `final` freezes the reference.
- Division truncates toward zero; `%` follows the dividend.
- `Math.round` rounds half **up**; `>>>` zero-fills.

## Common traps

| Trap | Fix |
|---|---|
| Statics run at program start | First use |
| A method call is a constant expression | No |
| Boxing beats widening | No |
| Varargs beats widening | No |
| `round(-2.5)` is `-3` | `-2` |
| `-7/2` is `-4` | `-3` |

## Checklist

- [ ] I can recite Table 1.
- [ ] I know the three constant-variable conditions.
- [ ] I know the overload phase order.
- [ ] I know the cache ranges.
- [ ] I know `round`/`floor`/`ceil` on negative halves.

## Related

- [Static and final](../01-concepts/01-static-and-final.md)
- [Varargs and wrapper types](../01-concepts/02-varargs-and-wrapper-types.md)
- [Operator precedence and arithmetic](../01-concepts/03-operator-precedence-and-arithmetic.md)
- [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
- [Static/final/varargs traps](../04-pitfalls/01-static-final-varargs-traps.md)
- [Topic overview](../README.md)
