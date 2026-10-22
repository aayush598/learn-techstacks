# Decision Tables for Overloads, Wrappers, and Operators

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 9 min_
> **Prerequisite:** [Varargs and wrapper types](../01-concepts/02-varargs-and-wrapper-types.md)

## In one sentence

Three lookup tables — **which overload**, **which comparison**, **which rounding** — plus a
60-second procedure that turns any operator question into a table lookup.

## Why the pre-test tests this

- These are the "which method / which operator" questions: fast marks if you own the table, lost
  marks if you improvise.
- The tables are exactly the shape of the exam's options, so you can match them one-to-one.

## Core concept

### Table 1 — overload resolution

Work down the table; the **first** row that matches wins.

| Row | Situation | Example | Chosen |
|---|---|---|---|
| 1 | Exact match on the argument's type | `m(String)` called with a `String` | `m(String)` |
| 2 | Widening primitive conversion | `m(long)` called with an `int` | `m(long)` |
| 3 | Widening reference conversion | `m(Object)` called with a `String` | `m(Object)` |
| 4 | Boxing then widening | `m(Integer)` called with an `int` | `m(Integer)` |
| 5 | Varargs (last resort) | `m(int...)` called with an `int` | `m(int...)` |

**Tie-break inside a row:** the **most specific** method wins (`Integer` beats `Object`).

### Table 2 — `==` on two objects

| Left type | Right type | Comparison is | Result |
|---|---|---|---|
| primitive | primitive | numeric | `5 == 5` → `true` |
| wrapper | primitive | numeric (wrapper unboxed) | `Integer i = 5; i == 5` → `true` |
| wrapper | wrapper | **reference**, subject to the cache | `Integer a = 127, b = 127; a == b` → `true` |
| `String` | `String` | reference (pool) | `"a" == "a"` → `true` |
| `String` | `String` built at runtime | reference | `s + "" == "a"` → `false` |
| any | `null` | reference | `s == null` → `true`/`false`, never NPE |

### Table 3 — the `Integer` cache and other caches

| Type | Cached range | `a == b` for values in range |
|---|---|---|
| `Integer` | **−128..127** | `true` |
| `Long` | **−128..127** | `true` |
| `Short` | **−128..127** | `true` |
| `Byte` | **all** (`byte` range) | `true` |
| `Character` | **0..127** | `true` |
| `Boolean` | `TRUE` / `FALSE` only | `true` |
| `Double` | **none** | `false` |
| `Float` | **none** | `false` |

### Table 4 — rounding

| Method | Direction | `2.5` | `-2.5` | `2.4` | `-2.4` |
|---|---|---|---|---|---|
| `Math.round(double)` | half **up** (toward +∞) | `3` | `-2` | `2` | `-2` |
| `Math.floor` | toward −∞ | `2.0` | `-3.0` | `2.0` | `-3.0` |
| `Math.ceil` | toward +∞ | `3.0` | `-2.0` | `3.0` | `-2.0` |

### Table 5 — division and modulo

| Expression | Result | Rule |
|---|---|---|
| `7 / 2` | `3` | truncation toward zero |
| `-7 / 2` | `-3` | truncation toward zero |
| `7 % 2` | `1` | sign of the dividend |
| `-7 % 2` | `-1` | sign of the dividend |
| `7 % -2` | `1` | sign of the dividend |
| `-7 % -2` | `-1` | sign of the dividend |
| `7 / 2.0` | `3.5` | any `double` operand → floating division |
| `7 / 0` | `ArithmeticException` | |
| `7.0 / 0` | `Infinity` | |

### Table 6 — compound assignment

| Statement | Equivalent to | Result |
|---|---|---|
| `byte b = 10; b += 5;` | `b = (byte)(b + 5)` | `15` |
| `int i = 10; i += 1.9;` | `i = (int)(i + 1.9)` | `11` |
| `char c = 'a'; c += 1;` | `c = (char)(c + 1)` | `'b'` |
| `byte b = 10; b = b + 5;` | — | **compile error** |

### The 60-second "which X?" procedure

1. **Is the question about a method call?** → Table 1, then the tie-break rule.
2. **Is it about `==`?** → Table 2, then Table 3 if both sides are wrappers.
3. **Is it about a rounding function?** → Table 4.
4. **Is it about `/` or `%`?** → Table 5.
5. **Is it about `+=` or similar?** → Table 6.
6. **Is it about `static`/`final`?** → the constant-variable rule:
   `final` + primitive/`String` + constant-expression initialiser ⇒ compile-time constant.

## Worked example

**Q. Which method does `m(5)` call?**

```java
public class Main {
    static void m(Object o)  { System.out.println("Object"); }
    static void m(double d)  { System.out.println("double"); }
    static void m(Integer i) { System.out.println("Integer"); }
    static void m(long l)    { System.out.println("long"); }
    static void m(int... x)  { System.out.println("int..."); }
    public static void main(String[] args) {
        m(5);
    }
}
```

**Solution** — walk Table 1 from the top.

| Row | Applicable? |
|---|---|
| 1 — exact match | no (`int` matches no parameter exactly) |
| 2 — widening primitive | **yes** → `m(long)` |
| — | the walk stops here; rows 3–5 are never reached |

**Answer: `m(long)`**, so the output is:

```
long
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `Integer` | Boxing is row 4 — row 2 already matched |
| `int...` | Varargs is the last resort |
| `double` | `int` → `double` is also widening, but `long` is reached first in the widening order (`int` → `long` → `float` → `double`), and `m(long)` is more specific |
| `Object` | Boxing + widening reference — later than plain widening |

## Quick rules

- Overloads: exact → widening primitive → widening reference → boxing → varargs. First match wins.
- Inside a phase, the most specific method wins.
- `==` on two wrappers is a reference comparison, subject to the cache.
- `Integer` cache = −128..127; `Double`/`Float` have **no** cache.
- `Math.round` rounds half **up**; `floor` → −∞; `ceil` → +∞.
- Integer division truncates toward zero; `%` follows the dividend.
- `x op= y` casts back to the declared type of `x`.

## Common traps

| Trap | Fix |
|---|---|
| Boxing beats widening | Widening comes first |
| Varargs beats everything | Varargs is last |
| `Integer` 128 is cached | −128..127 only |
| `round(-2.5)` is `-3` | `round` is half up → `-2` |
| `floor` rounds to nearest | `floor` goes down, `ceil` goes up |

## Checklist

- [ ] I can recite Table 1 in order.
- [ ] I know the cache ranges for `Integer`, `Character`, `Boolean`, `Double`.
- [ ] I know `round`/`floor`/`ceil` on both `2.5` and `-2.5`.
- [ ] I know the modulo sign rule.
- [ ] I can state the constant-variable rule in one sentence.

## Related

- [Static and final](../01-concepts/01-static-and-final.md)
- [Varargs and wrapper types](../01-concepts/02-varargs-and-wrapper-types.md)
- [Operator precedence and arithmetic](../01-concepts/03-operator-precedence-and-arithmetic.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
- [Static/final/varargs traps](../04-pitfalls/01-static-final-varargs-traps.md)
- [Static/final/varargs one-pager](../05-reference/01-static-final-varargs-one-pager.md)
- [Topic overview](../README.md)
