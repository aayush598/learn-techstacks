# Method Resolution, Short-Circuit, and Compound Assignment

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 12 min_
> **Prerequisite:** [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)

## In one sentence

Overload resolution is a **3-phase contest** — strict widening beats boxing, boxing beats varargs —
and short-circuit operators **skip one whole side of the expression**.

## Why the pre-test tests this

- "Which method will be called?" is a standard 4-option question with a definite answer.
- Short-circuit and `++` produce the largest output differences per character changed.
- These two rules together explain most of the output questions that candidates get wrong.

## Core concept

### Overload resolution — the 3 phases

For a call `m(args)` where `m` is overloaded, `javac` tries the phases **in order** and stops at the
first phase that finds at least one applicable method.

| Phase | Allowed conversions | Applies to |
|---|---|---|
| **1. Strict invocation** | identity, **widening primitive**, widening reference | `m(long)` for an `int` argument |
| **2. Loose invocation** | boxing / unboxing, then widening | `m(Integer)` for an `int` argument |
| **3. Varargs** | the trailing parameter is treated as an array | `m(int...)` for an `int` argument |

Within a phase, the **most specific** method wins. A method with more specific parameter types is
more specific.

### The classic four-way table

Given these four overloads:

```java
static void m(Object o)  { }
static void m(String s)  { }
static void m(Integer i) { }
static void m(int... x)  { }
```

| Call | Phase | Chosen | Why |
|---|---|---|---|
| `m("hi")` | 1 | `m(String)` | Exact match beats widening to `Object` |
| `m(5)` | 2 | `m(Integer)` | Phase 1 finds nothing — see the note below |
| `m((Object) "hi")` | 1 | `m(Object)` | Exact match on the declared type |
| `m(5, 6)` | 3 | `m(int...)` | Only the varargs method takes two arguments |
| `m("hi", "x")` | — | **compile error** | No overload accepts two `String`s — `m(int...)` cannot take `String` arguments |

> **Careful on `m(5)` with `m(Object)`, `m(Integer)` and `m(int...)`:**
> Phase 1 (strict): `m(Object)` needs `int` → `Object`. That is boxing + widening reference, which is
> **not** a strict invocation. `m(Integer)` needs boxing. `m(int...)` is phase 3. So **phase 1 finds
> nothing**.
> Phase 2 (loose): `m(Integer)` is applicable via boxing; `m(Object)` is also applicable via boxing
> + widening reference. Between the two, `m(Integer)` is **more specific** (Integer is a subtype of
> Object) → **`m(Integer)` is chosen**.

**The rule that surprises people:** with `m(Object)` and `m(int...)` only, `m(5)` calls `m(Object)`,
because phase 2 (boxing to `Integer`, then widening to `Object`) is reached before phase 3.

### Varargs rules

| Rule | Detail |
|---|---|
| Must be last | `void m(int a, String... s)` is legal; `void m(String... s, int a)` is not |
| One per method | `void m(int... a, String... b)` → compile error |
| Zero arguments | `m()` is legal and gives an **empty array**, not `null` |
| Compiles to an array | `void m(int... x)` is exactly `void m(int[] x)` at the bytecode level |
| Erasure clash | `void m(int... a)` and `void m(int[] a)` in the same class → compile error ("same erasure") |
| Ambiguity | `m(Object...)` and `m(String...)` called with `null` → **ambiguous**, compile error |
| More specific wins | `m("x")` with both `m(Object...)` and `m(String...)` → `m(String...)` |

### Short-circuit truth tables

| Expression | Left evaluated | Right evaluated | Result |
|---|---|---|---|
| `a && b` | always | only if `a` is **true** | `a && b` |
| `a \|\| b` | always | only if `a` is **false** | `a \|\| b` |
| `c ? x : y` | `c` always | only the **taken** branch | value of that branch |

The untaken branch is **not evaluated**. It has no side effect, no exception, no `++`.

**Trap shape:**

```java
int i = 0;
boolean r = (i++ > 0) && (i++ > 0);   // i ends at 1
boolean s = (i++ > 0) || (i++ > 0);   // with i = 0: both sides run, i ends at 2
```

### `++` / `--` in expressions

| Form | Yields | Variable after |
|---|---|---|
| `i++` | old value | old ± 1 |
| `++i` | new value | new value |

Operand evaluation in a binary expression is **left to right**.

```java
int i = 5;
int j = i++ + ++i;    // (5) + (7) = 12, and i == 7
```

```java
int[] a = {10, 20, 30};
int k = 0;
System.out.println(a[k++]);   // 10  (index is the old value 0)
System.out.println(k);        // 1
```

### Compound assignment — the cast rule

```
x += y      ≡      x = (T)(x + y)       T = declared type of x
x -= y      ≡      x = (T)(x - y)
x *= y      ≡      x = (T)(x * y)
```

| Code | Result | Why |
|---|---|---|
| `byte b = 10; b += 5;` | `b == 15` | `(byte)(10+5)` |
| `byte b = 10; b = b + 5;` | **compile error** | plain expression, `int` → `byte` needs a cast |
| `int i = 10; i += 1.9;` | `i == 11` | `(int)(10 + 1.9)` = `(int) 11.9` = 11 |
| `char c = 'a'; c += 1;` | `c == 'b'` | `(char)('a' + 1)` |
| `int i = 10; i *= 2.5;` | `i == 25` | `(int)(10 * 2.5)` = `(int) 25.0` = 25 |

`++` and `--` on a `byte`/`short`/`char` also work, because they are defined as compound assignments.

### `instanceof` and casts

```java
Object o = "hello";
if (o instanceof String) {
    String s = (String) o;       // Java 8 requires the cast
    System.out.println(s.length());   // 5
}
```

- `null instanceof String` → **false**.
- A cast between unrelated reference types **compiles** and throws `ClassCastException` at runtime.
- Casting a `null` reference is legal and yields `null`.
- `int x = (int) someLong;` → narrowing cast, allowed with an explicit cast.
- `int x = someLong;` → compile error.

### Ternary typing

The type of `c ? a : b` is computed by **binary numeric promotion** when both branches are numeric.

| Expression | Result type | Value |
|---|---|---|
| `true ? 1 : 2` | `int` | `1` |
| `true ? 1 : 2.0` | `double` | `2.0` |
| `false ? 1 : 2.0` | `double` | `2.0` |
| `true ? 'a' : 98` | `int` | `97` |
| `flag ? "a" : "b"` | `String` | `"a"` |
| `flag ? null : "b"` | `String` | `null` |

## Worked example

**Q. Which method is called?**

```java
public class Main {
    static void m(Object o)  { System.out.println("Object"); }
    static void m(Integer i) { System.out.println("Integer"); }
    static void m(int... x)  { System.out.println("int..."); }
    public static void main(String[] args) {
        m(5);
    }
}
```

**Solution**

| Phase | Applicable? |
|---|---|
| 1 — strict | `m(Object)`: `int` → `Object` needs boxing → not applicable. `m(Integer)`: needs boxing → not applicable. `m(int...)`: phase 3. → **none** |
| 2 — loose (boxing) | `m(Integer)`: boxing, applicable. `m(Object)`: boxing then widening reference, applicable. → both applicable |
| Most specific | `Integer` is a subtype of `Object` → `m(Integer)` wins |

**Output (exact):**

```
Integer
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `Object` | `m(Integer)` is more specific in phase 2 |
| `int...` | Varargs is phase 3; phase 2 already found a match |
| Compile error | The call is unambiguous |

**Variant:** delete the `m(Integer)` overload and `m(5)` prints `Object` (phase 2, boxing to
`Integer` then widening to `Object`) — **not** `int...`.

## Quick rules

- Overloads: **strict → boxing → varargs**. First phase with a match wins.
- Within a phase, the **most specific** method wins.
- `m(5)` with `m(Integer)` + `m(Object)` → `m(Integer)`.
- `m(5)` with `m(Object)` + `m(int...)` → `m(Object)`.
- `m("hi")` with `m(Object)` + `m(String...)` → `m(Object)` (phase 1, widening reference).
- `&&` needs the right side only when the left is true; `||` only when the left is false.
- The ternary evaluates **one** branch.
- `x += y` = `x = (T)(x + y)`.
- `i++ + ++i` with `i = 5` → `12`, and `i` becomes `7`.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| Varargs wins | `int...` | Widening/boxing wins |
| `m("hi")` → `m(Object)` because `Object` is "safer" | `Object` | With `m(String)` present, `m(String)` wins; `m(Object)` only wins if it is the **only** applicable one |
| `&&` always skips the right side | skips | It skips only when the left is false |
| `i += 1.9` gives 11.9 | `11.9` | `11` |
| `byte b = 10; b = b + 5;` compiles | compiles | Compile error |

## Checklist

- [ ] I can state the 3 phases in order.
- [ ] I know the "most specific wins" tie-break.
- [ ] I can list which overload wins for `m(5)` and for `m("hi")` in the four-way table.
- [ ] I know the short-circuit direction of `&&` vs `||`.
- [ ] I know `x += y` casts back to the declared type of `x`.

## Related

- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [10-second triage](01-ten-second-triage.md)
- [Solved output set A](../03-worked-examples/01-solved-output-set-a.md)
- [Solved output set B](../03-worked-examples/02-solved-output-set-b.md)
- [Output traps](../04-pitfalls/01-output-traps.md)
- [Output rules one-pager](../05-reference/01-output-rules-one-pager.md)
- [Topic overview](../README.md)
