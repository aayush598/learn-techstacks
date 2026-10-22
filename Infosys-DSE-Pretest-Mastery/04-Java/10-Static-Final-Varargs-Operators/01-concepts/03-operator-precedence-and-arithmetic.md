# Operator Precedence, Arithmetic, and the Math Class

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 12 min_
> **Prerequisite:** none

## In one sentence

Java's operators have a fixed **precedence ladder** and a few **exceptions** (the ternary and the
compound assignments) — knowing the ladder is worth several marks on their own.

## Why the pre-test tests this

- "What is the value of `a + b * c`?" and "What does `x |= y` do?" are cheap 4-option questions.
- `Math.round` vs `Math.floor` vs `Math.ceil` is a classic trap — they disagree on negative
  halves.
- Integer division and negative modulo are asked repeatedly.

## Core concept

### The precedence ladder (highest first)

| Level | Operators | Associativity |
|---|---|---|
| 1 | postfix `++` `--`, unary `+` `-`, `~`, `!`, cast `(type)` | right-to-left |
| 2 | `*` `/` `%` | left-to-right |
| 3 | `+` `-` | left-to-right |
| 4 | `<<` `>>` `>>>` | left-to-right |
| 5 | `<` `>` `<=` `>=` `instanceof` | left-to-right |
| 6 | `==` `!=` | left-to-right |
| 7 | `&` | left-to-right |
| 8 | `^` | left-to-right |
| 9 | `\|` | left-to-right |
| 10 | `&&` | left-to-right |
| 11 | `\|\|` | left-to-right |
| 12 | `? :` | right-to-left |
| 13 | `= += -= *= /= %= &= \|= ^= <<= >>= >>>=` | right-to-left |

**Practical notes**

- `+` and `-` are **left-associative**: `10 - 3 - 2` = `(10 - 3) - 2` = **5**.
- The ternary `?:` binds **looser** than every arithmetic operator but **tighter** than assignment.
- Compound assignment is an expression, not a statement — `a = b += c` is legal.
- A **cast binds tighter** than any binary operator: `(int) a / b` is `((int) a) / b`.
- `instanceof` sits at relational level, above `==`.

### Arithmetic rules

| Expression | Result | Rule |
|---|---|---|
| `7 / 2` | `3` | integer division truncates toward zero |
| `-7 / 2` | `-3` | truncation is toward **zero**, not down |
| `7 % 2` | `1` | remainder |
| `-7 % 2` | `-1` | the sign of the result follows the **dividend** |
| `7 % -2` | `1` | same rule |
| `-7 % -2` | `-1` | same rule |
| `7 / 2.0` | `3.5` | one `double` operand → floating division |
| `7 / 0` | `ArithmeticException` | `/ by zero` |
| `7 % 0` | `ArithmeticException` | `/ by zero` |
| `7.0 / 0.0` | `Infinity` | floating point |
| `0.0 / 0.0` | `NaN` | floating point |
| `Math.sqrt(-1)` | `NaN` | |

**The `%` rule in one line:** `a % b` has the **sign of `a`** and a magnitude less than `|b|`.

### Bitwise operators

| Operator | Name | `5 OP 3` (binary `101` and `011`) |
|---|---|---|
| `&` | AND | `1` (`001`) |
| `\|` | OR | `7` (`111`) |
| `^` | XOR | `6` (`110`) |
| `~` | NOT (unary) | `~5` = `-6` |
| `<<` | left shift | `5 << 1` = `10` (multiply by 2) |
| `>>` | arithmetic right shift (sign-preserving) | `-8 >> 1` = `-4` |
| `>>>` | logical right shift (zero-fill) | `-8 >>> 1` = `2147483644` |

`>>>` on an `int` shifts in zeros from the left; `>>` copies the sign bit. Both are common
"which operator" questions.

### `&&` vs `&`, `||` vs `|`

| | `&&` / `\|\|` | `&` / `\|` |
|---|---|---|
| Operands | `boolean` only | `boolean` **or** integral |
| Short-circuits | ✅ | ❌ — both operands always evaluated |
| Use | conditions | bit masks, flags, `boolean` with no short-circuit |

```java
int i = 0;
boolean b = (i++ > 0) && (i++ > 0);   // i = 1
boolean c = (i++ > 0) & (i++ > 0);    // both sides run
```

### Compound assignment

```
x op= y     ≡     x = (T)(x op y)      T = declared type of x
```

| Statement | Result |
|---|---|
| `int i = 10; i += 1.9;` | `i == 11` |
| `byte b = 10; b += 5;` | `b == 15` (implicit `(byte)` cast) |
| `byte b = 10; b = b + 5;` | **compile error** |
| `char c = 'a'; c += 1;` | `c == 'b'` |
| `int i = 10; i *= 2.5;` | `i == 25` |
| `short s = 1; s <<= 2;` | `s == 4` |

### Ternary numeric promotion

The two branches of `c ? a : b` are unified by **binary numeric promotion** if both are numeric.

| Expression | Type | Value |
|---|---|---|
| `true ? 1 : 2` | `int` | `1` |
| `true ? 1 : 2.0` | `double` | `2.0` |
| `false ? 1 : 2.0` | `double` | `2.0` |
| `true ? 'a' : 98` | `int` | `97` |
| `true ? 1 : 'a'` | `int` | `1` |

If **one** branch is `null` and the other is a reference type, the result type is that reference
type.

### `instanceof`

| Expression | Result |
|---|---|
| `"abc" instanceof String` | `true` |
| `null instanceof String` | `false` — never throws |
| `obj instanceof String` where `obj` is an `Object` holding a `String` | `true` (runtime check) |

### The Math class

| Method | Returns | Notes |
|---|---|---|
| `Math.abs(-5)` | `5` (`int`) | `abs(double)` returns `double` |
| `Math.max(3, 5)` | `5` (`int`) | `max(int,int)` → `int`; mixed args → `double` |
| `Math.min(3, 5)` | `3` (`int`) | |
| `Math.max(3, 4.5)` | `4.5` (`double`) | promotion |
| `Math.round(2.5)` | `3` (`long`) | **rounds half up**, not half to even |
| `Math.round(-2.5)` | `-2` (`long`) | half up toward +∞ |
| `Math.round(2.4)` | `2` (`long`) | |
| `Math.floor(2.7)` | `2.0` (`double`) | toward −∞ |
| `Math.floor(-2.5)` | `-3.0` (`double`) | |
| `Math.ceil(2.1)` | `3.0` (`double`) | toward +∞ |
| `Math.ceil(-2.5)` | `-2.0` (`double`) | |
| `Math.sqrt(16)` | `4.0` (`double`) | |
| `Math.pow(2, 3)` | `8.0` (`double`) | |
| `Math.random()` | `[0.0, 1.0)` | never exactly 1.0 |
| `Math.cbrt(27)` | `3.0` | Java 8+ |

**The `round` vs `floor` vs `ceil` trap:**

| Input | `round` | `floor` | `ceil` |
|---|---|---|---|
| `2.5` | `3` | `2.0` | `3.0` |
| `-2.5` | `-2` | `-3.0` | `-2.0` |

`round` rounds **half up** (toward positive infinity), so `round(-2.5)` is `-2`, **not** `-3`.

### `++` / `--` on non-`int` types

`++` and `--` work on `byte`, `short`, `char`, and `long` — they are defined as compound assignments
with an implicit cast.

```java
byte b = 127;
b++;                 // b = (byte)(127 + 1) = -128  (overflow wraps)
char c = 'z';
c++;                 // c = '{'
```

## Worked example

**Q. What is printed?**

```java
public class Main {
    public static void main(String[] args) {
        int a = 7, b = 2;
        System.out.println(a / b);
        System.out.println(a % b);
        System.out.println(-a % b);
        System.out.println(a / b * 2 + 1);
        System.out.println(Math.round(2.5));
        System.out.println(Math.floor(-2.5));
        System.out.println(5 & 3);
        System.out.println(5 | 3);
        System.out.println(5 ^ 3);
        System.out.println(-8 >>> 1);
    }
}
```

**Solution**

| Expression | Result | Rule |
|---|---|---|
| `a / b` | `3` | integer division, truncation toward zero |
| `a % b` | `1` | 7 = 2×3 + 1 |
| `-a % b` | `-1` | sign follows the dividend |
| `a / b * 2 + 1` | `7` | left to right: `(7/2)*2 + 1` = `3*2 + 1` = 7 |
| `Math.round(2.5)` | `3` | rounds half up; returns `long` |
| `Math.floor(-2.5)` | `-3.0` | toward −∞ |
| `5 & 3` | `1` | `101 & 011 = 001` |
| `5 \| 3` | `7` | `101 \| 011 = 111` |
| `5 ^ 3` | `6` | `101 ^ 011 = 110` |
| `-8 >>> 1` | `2147483644` | zero-fill shift |

`a / b * 2 + 1`: `7 / 2` is **3** (integer division), then `3 * 2` is 6, then `6 + 1` is **7**.

**Output (exact):**

```
3
1
-1
7
3
-3.0
1
7
6
2147483644
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `4` for `a / b * 2 + 1` | `7 / 2` is **3**, not 3.5 — so `3 * 2 + 1` = 7 |
| `-3` for `Math.round(-2.5)` | `round` rounds half **up** (toward +∞) → `-2` |
| `-4` for `-8 >>> 1` | `>>>` fills with **zeros**, giving `2147483644`; `>>` would give `-4` |

## Quick rules

- `*` `/` `%` beat `+` `-`; everything beats the ternary; the ternary beats assignment.
- `+`/`-` are left-associative.
- Integer division truncates **toward zero**.
- `%` takes the sign of the **dividend**.
- `x op= y` = `x = (T)(x op y)`.
- `&&`/`||` short-circuit; `&`/`|` do not.
- `Math.round` rounds half **up**; `floor` goes to −∞; `ceil` goes to +∞.
- `>>` preserves the sign; `>>>` fills with zeros.
- `null instanceof X` is `false`.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| `-7 / 2` floors to `-4` | `-4` | It truncates to `-3` |
| `-7 % 2` is `1` | `1` | It is `-1` |
| `Math.round(-2.5)` is `-3` | `-3` | It is `-2` |
| `>>>` preserves the sign | `-4` | `>>>` fills zeros |
| `&` short-circuits | short-circuit | Only `&&` does |

## Checklist

- [ ] I can write the precedence ladder from memory.
- [ ] I know the truncation and modulo-sign rules.
- [ ] I know `round` vs `floor` vs `ceil` on negative halves.
- [ ] I know `>>` vs `>>>`.
- [ ] I know compound assignment casts back to the declared type.

## Related

- [Static and final](01-static-and-final.md)
- [Varargs and wrapper types](02-varargs-and-wrapper-types.md)
- [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
- [Static/final/varargs traps](../04-pitfalls/01-static-final-varargs-traps.md)
- [Static/final/varargs one-pager](../05-reference/01-static-final-varargs-one-pager.md)
- [Topic overview](../README.md)
