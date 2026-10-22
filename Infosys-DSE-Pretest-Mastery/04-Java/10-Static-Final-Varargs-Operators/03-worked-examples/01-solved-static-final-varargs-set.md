# Solved Set — Static, Final, Varargs & Operators

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 24 min_
> **Prerequisite:** [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)

## In one sentence

10 fully solved questions: static initialisation order, constant variables, overload phases, varargs
rules, the `Integer` cache, and operator arithmetic.

## Why the pre-test tests this

Every question here is a direct imitation of the exam's Section 4 style: a code block, four
options, and an exact printed output. Read the breakdown after each answer — the breakdown is
where the marks live.

## Core concept

- **Static initialisation** happens at *first use*, superclass first, textual order.
- **Constant variables** are `final` + primitive/`String` + constant-expression initialiser.
- **Overload resolution** order: exact → widening primitive → widening reference → boxing → varargs.
- **The `Integer` cache** covers −128..127 only.

## Worked example

### Q1 — Static block order

```java
class A {
    static int x = 10;
    static { x += 5; }
    static int y = x * 2;
}
public class Main {
    public static void main(String[] args) {
        System.out.println(A.y);
        System.out.println(A.x);
    }
}
```

**Options**

| # | Option |
|---|---|
| A | `20` then `15` |
| B | `30` then `15` |
| C | `30` then `30` |
| D | `20` then `20` |

**Answer: B** — `30` then `15`.

**Breakdown**

| Step | Statement | Effect |
|---|---|---|
| 1 | `static int x = 10;` | `x = 10` |
| 2 | `static { x += 5; }` | `x = 15` |
| 3 | `static int y = x * 2;` | `y = 30` — it reads `x` **now**, which is 15 |

**Why not A:** `y` is initialised *after* the static block, so it sees 15, not 10.
**Why not C:** `x` ends at 15; the block already ran.
**Why not D:** both mistakes at once.

---

### Q2 — Instance initialiser vs constructor

```java
class B {
    int x = 5;
    { x += 10; }
    B() { x += 20; }
}
public class Main {
    public static void main(String[] args) {
        System.out.println(new B().x);
    }
}
```

**Options**

| # | Option |
|---|---|
| A | `5` |
| B | `15` |
| C | `35` |
| D | `30` |

**Answer: C** — `35`.

**Breakdown**

| Order | Statement | `x` |
|---|---|---|
| 1 | `int x = 5;` (instance field initialiser) | 5 |
| 2 | `{ x += 10; }` (instance initialiser block) | 15 |
| 3 | `B() { x += 20; }` (constructor body) | 35 |

**Why not D:** the field initialiser runs **before** the instance block — textual order, all of it
before the constructor body.

---

### Q3 — Is it a compile-time constant?

```java
final int A = 10;
final int B = A * 2;
final String S = "Hi";
final String T = S + "!";
final int C = someMethod();
```

**Options**

| # | Option |
|---|---|
| A | `A` and `B` only are constants |
| B | `A`, `B`, `S`, and `T` are constants; `C` is not |
| C | All five are constants |
| D | None are constants |

**Answer: B.**

**Breakdown** — a constant variable needs `final` **and** a primitive/`String` type **and** a
constant-expression initialiser.

| Name | Constant expression? | Verdict |
|---|---|---|
| `A` | literal `10` | ✅ constant |
| `B` | `A * 2` where `A` is constant | ✅ constant |
| `S` | literal `"Hi"` | ✅ constant |
| `T` | `S + "!"` where `S` is constant | ✅ constant |
| `C` | a method call — **not** a constant expression | ❌ not constant |

**Why not C:** method calls are never constant expressions, so `C` is a `final` field, not a
constant variable.

---

### Q4 — Which overload does `m(5)` pick?

```java
static void m(Object o)  { }
static void m(double d)  { }
static void m(Integer i) { }
static void m(long l)    { }
static void m(int... x)  { }
```

`m(5);`

**Options**

| # | Option |
|---|---|
| A | `m(Object)` |
| B | `m(double)` |
| C | `m(Integer)` |
| D | `m(long)` |

**Answer: D** — `m(long)`.

**Breakdown** — walk the phases in order:

| Phase | Applicable? |
|---|---|
| 1 — exact match | ❌ |
| 2 — widening primitive (`int` → `long`) | ✅ **stop here** |
| 3 — widening reference | not reached |
| 4 — boxing | not reached |
| 5 — varargs | not reached |

**Why not B:** `int` → `double` is also widening, but `long` is nearer to `int` in the widening
order (`int` → `long` → `float` → `double`), so `m(long)` is more specific.
**Why not C:** boxing comes after plain widening.

---

### Q5 — Varargs rules

```java
static void m(int... xs) { System.out.println(xs.length); }
public static void main(String[] args) {
    m();
    m(1);
    m(1, 2, 3);
    m(new int[]{1, 2});
}
```

**Options**

| # | Option |
|---|---|
| A | `0`, `1`, `3`, `2` |
| B | `0`, `1`, `3`, `2` — all on separate lines |
| C | A compile error: varargs must be the last parameter |
| D | A compile error: only one varargs parameter allowed |

**Answer: A** — `0`, `1`, `3`, `2`.

**Breakdown**

| Call | `xs.length` |
|---|---|
| `m()` | `0` — an **empty array**, not `null` |
| `m(1)` | `1` |
| `m(1, 2, 3)` | `3` |
| `m(new int[]{1, 2})` | `2` — an array may be passed directly |

**Why not C / D:** those rules apply to the *declaration*, and this declaration satisfies both.

---

### Q6 — `Integer` cache and `==`

```java
Integer a = 127, b = 127;
Integer c = 128, d = 128;
Integer e = 1000, f = 1000;
int g = 1000;
System.out.println(a == b);
System.out.println(c == d);
System.out.println(e == f);
System.out.println(e == g);
```

**Options**

| # | Option |
|---|---|
| A | `true`, `false`, `false`, `true` |
| B | `true`, `true`, `true`, `true` |
| C | `true`, `false`, `false`, `false` |
| D | `true`, `true`, `false`, `true` |

**Answer: A** — `true`, `false`, `false`, `true`.

**Breakdown**

| Expression | Why |
|---|---|
| `a == b` | 127 is inside the −128..127 cache → same object → `true` |
| `c == d` | 128 is outside the cache → two objects → `false` |
| `e == f` | 1000 is outside the cache → two objects → `false` |
| `e == g` | `g` is a primitive `int`, so `e` is **unboxed** → numeric comparison → `true` |

**Why not C:** the last line unboxes.
**Why not D:** 128 is not cached.

---

### Q7 — `Integer` addition vs concatenation

```java
Integer a = 1, b = 2;
System.out.println(a + b);
System.out.println(a + "");
```

**Options**

| # | Option |
|---|---|
| A | `3` then `1` |
| B | `12` then `1` |
| C | `12` then `12` |
| D | A compile error |

**Answer: A** — `3` then `1`.

**Breakdown** — `+` is **numeric addition** as long as neither operand is a `String`. Both `Integer`
operands are unboxed to `int`, so `a + b` is `1 + 2` → `3`. The second line has a `String` operand,
so `a + ""` concatenates → `"1"`.

**Why not B or C:** two `Integer` operands never turn into text on their own — a `String` has to be
involved.
**Why not D:** it compiles fine, and `int x = a + b;` also compiles and gives `x == 3`.

---

### Q8 — `final` and object mutability

```java
final int[] a = {1, 2, 3};
a[0] = 99;
System.out.println(a[0]);
```

**Options**

| # | Option |
|---|---|
| A | A compile error: cannot modify a `final` array |
| B | `1` |
| C | `99` |
| D | A compile error: cannot assign a value to final variable `a` |

**Answer: C** — `99`.

**Breakdown** — `final` freezes the **reference**, not the object's contents. The array object
still exists and its elements are still writable. Only `a = new int[5];` would be a compile error.

---

### Q9 — Operator arithmetic

```java
int a = 7, b = 2;
System.out.println(a / b);
System.out.println(-a % b);
System.out.println(a / b * 2 + 1);
System.out.println(Math.round(-2.5));
System.out.println(-8 >>> 1);
```

**Options**

| # | Option |
|---|---|
| A | `3`, `-1`, `7`, `-2`, `2147483644` |
| B | `3`, `1`, `7`, `-2`, `2147483644` |
| C | `4`, `-1`, `7`, `-3`, `-4` |
| D | `3`, `-1`, `4`, `-2`, `2147483644` |

**Answer: A** — `3`, `-1`, `7`, `-2`, `2147483644`.

**Breakdown**

| Expression | Value | Rule |
|---|---|---|
| `a / b` | `3` | integer division truncates toward zero |
| `-a % b` | `-1` | the result takes the sign of the dividend |
| `a / b * 2 + 1` | `7` | left to right: `3 * 2 + 1` = 7 |
| `Math.round(-2.5)` | `-2` | rounds half **up** (toward +∞) |
| `-8 >>> 1` | `2147483644` | `>>>` fills the high bits with zeros |

**Why not B:** `-7 % 2` is `-1`, not `1`.
**Why not C:** `7/2` is 3, `round` is half up, and `>>>` zero-fills.
**Why not D:** `7 / 2 * 2 + 1` is 7, not 4.

---

### Q10 — Varargs vs widening

```java
static void m(Object o)  { System.out.print("Object "); }
static void m(String... s) { System.out.print("String... "); }
public static void main(String[] args) {
    m("hi");
    m((String) null);
}
```

**Options**

| # | Option |
|---|---|
| A | `Object Object` |
| B | `String... String...` |
| C | `Object String...` |
| D | A compile error: ambiguous method call |

**Answer: A** — `Object Object`.

**Breakdown**

| Call | Chosen | Why |
|---|---|---|
| `m("hi")` | `m(Object)` | phase 1: `String` → `Object` is a widening reference conversion, so phase 1 already matches |
| `m((String) null)` | `m(Object)` | same reason — the cast to `String` still widens to `Object` in phase 1 |

**Why not B:** varargs is the **last** phase; phase 1 already matched.
**Why not D:** an ambiguity error arises for `m(null)` (no cast) when both `m(Object...)` and
`m(String...)` exist — but here the single-parameter `m(Object)` resolves it in phase 1.

## Quick rules

- Static init: superclass first, then textual order, at first use.
- Instance init: field initialisers, then instance blocks, then the constructor body.
- Constant variable = `final` + primitive/`String` + constant expression.
- Overload phases: exact → widening primitive → widening reference → boxing → varargs.
- `Integer` cache = −128..127; `Double`/`Float` have none.
- `+` with a wrapper on the left and a `String` anywhere → concatenation.
- `final` freezes the reference.
- Integer division truncates toward zero; `%` follows the dividend.
- `Math.round` rounds half up; `>>>` zero-fills.

## Common traps

| Trap | Where it appears |
|---|---|
| Static block sees the final field value | Q1 |
| Instance initialiser after the constructor | Q2 |
| A method call is a constant expression | Q3 |
| Boxing beats widening | Q4, Q6 |
| Varargs beats widening | Q10 |
| `final` makes the array immutable | Q8 |
| `round(-2.5)` is `-3` | Q9 |
| `Integer + Integer` | Q7 |

## Checklist

- [ ] I can order static and instance initialisation without hesitating.
- [ ] I can state the three constant-variable conditions.
- [ ] I can walk the overload phases in order.
- [ ] I know the `Integer` cache boundary exactly.
- [ ] I know `round`, `floor`, `ceil` on negative halves.

## Related

- [Static and final](../01-concepts/01-static-and-final.md)
- [Varargs and wrapper types](../01-concepts/02-varargs-and-wrapper-types.md)
- [Operator precedence and arithmetic](../01-concepts/03-operator-precedence-and-arithmetic.md)
- [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
- [Static/final/varargs traps](../04-pitfalls/01-static-final-varargs-traps.md)
- [Static/final/varargs one-pager](../05-reference/01-static-final-varargs-one-pager.md)
- [Topic overview](../README.md)
