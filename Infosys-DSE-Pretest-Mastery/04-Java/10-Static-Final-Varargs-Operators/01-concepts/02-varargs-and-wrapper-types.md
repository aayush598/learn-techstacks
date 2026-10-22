# Varargs and Wrapper Types

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 10 min_
> **Prerequisite:** [Static and final](01-static-and-final.md)

## In one sentence

Varargs are **syntactic sugar for an array parameter**, and the wrapper classes add **autoboxing**,
the **−128..127 `Integer` cache**, and a set of `==` traps.

## Why the pre-test tests this

- "What is the type of the varargs parameter?" → `int[]`. "Can a method have two varargs
  parameters?" → no.
- `Integer` `==` vs `equals` is a standard MCQ with the −128..127 boundary as the trap.
- Autoboxing changes overload resolution, so it shows up in "which method is called?" questions.

## Core concept

### Varargs — the rules

```java
void m(int... xs) { }      // exactly equivalent to  void m(int[] xs) { }
```

| Rule | Detail | Error if broken |
|---|---|---|
| Must be the **last** parameter | `void m(int a, String... s)` is legal | `varargs parameter must be the last parameter` |
| Only **one** per method | `void m(int... a, String... b)` is not | `only one varargs parameter allowed` |
| Zero arguments allowed | `m()` gives `xs` = an **empty array** (not `null`) | |
| Can be called with an array | `m(new int[]{1,2})` works | |
| Cannot be generic | `void m(T... xs)` is illegal | `illegal generic type for varargs parameter` |
| Two varargs overloads clash | `m(int...)` and `m(long...)` are fine; `m(int...)` and `m(int[])` clash | `name clash: ... have the same erasure` |

**The array-vs-varargs overload trap:**

```java
static void m(Object o)  { System.out.println("Object"); }
static void m(String... s){ System.out.println("String..."); }
m("hi");     // prints "Object"  — phase 1 widening reference beats varargs
m((Object) null);  // prints "Object"
m((String) null);  // prints "String..."  — the cast makes it a single String argument
```

**Ambiguity trap:**

```java
static void m(Object... o) { }
static void m(String... s) { }
m(null);      // COMPILE ERROR: reference to m is ambiguous
```

Because `null` is compatible with both `Object[]` and `String[]` in the varargs phase, and neither
is more specific in the right way, the call is ambiguous. Casting resolves it: `m((Object) null)` or
`m((String) null)`.

### Autoboxing and unboxing

Java 5+ converts automatically between primitives and their wrapper types:

| Primitive | Wrapper | Autoboxing | Unboxing |
|---|---|---|---|
| `int` | `Integer` | `Integer i = 5;` | `int x = i;` |
| `long` | `Long` | | |
| `double` | `Double` | | |
| `char` | `Character` | | |
| `boolean` | `Boolean` | | |
| `byte` | `Byte` | | |
| `short` | `Short` | | |
| `float` | `Float` | | |
| `void` | `Void` | | |

**Where it bites:**

1. **Unboxing `null` → `NullPointerException`.**
   ```java
   Integer i = null;
   int x = i;          // NPE
   ```
2. **`Integer` compared with `==` unboxes.** `Integer i = 10; int j = 10; i == j` → `true`.
3. **The `Integer` cache.** `Integer.valueOf(x)` returns a cached object for **−128..127**;
   outside that range it creates a new object each time.
4. **Ternary with mixed wrapper types** can produce `NullPointerException`:
   ```java
   Integer a = null;
   int b = true ? a : 5;    // NPE — the result is unboxed
   Object c = true ? a : 5; // fine — the result is an Object
   ```
5. **`+` is numeric unless a `String` is involved.** Two `Integer` operands are **unboxed** and
   added; concatenation happens only when one operand has type `String`.
   ```java
   Integer a = 1, b = 2;
   System.out.println(a + b);   // 3   (unboxed to int, then added)
   int c = a + b;               // fine — c is 3
   System.out.println(a + "x"); // "1x" (a String operand forces concatenation)
   System.out.println("x" + b); // "x2"
   ```
   So `Integer + Integer` is **addition** (`3`), and `Integer + String` is **concatenation** (`"1x"`).

### The `Integer` cache in detail

| Expression | Result | Why |
|---|---|---|
| `Integer a = 127, b = 127; a == b` | `true` | cached |
| `Integer a = 128, b = 128; a == b` | `false` | not cached |
| `Integer a = -128, b = -128; a == b` | `true` | −128 is the lower boundary |
| `Integer a = -129, b = -129; a == b` | `false` | below the boundary |
| `Integer a = 10; int b = 10; a == b` | `true` | `a` is unboxed |
| `Integer a = 10, b = 10; a.equals(b)` | `true` | content comparison |
| `Integer a = 200; Integer b = 200; a.equals(b)` | `true` | content comparison |
| `new Integer(128) == new Integer(128)` | `false` | `new` bypasses the cache |

The cache is a JVM implementation detail, but the **−128..127** range is specified in the Java
Language Specification for `Integer.valueOf`, so it is safe to test.

**`Integer` vs `int` in a comparison — the mental shortcut:**

> If **either** side of `==` is a primitive `int`, the comparison is **numeric**.
> If **both** sides are `Integer`, the comparison is by **reference** (subject to the cache).

### The wrapper `equals` and `hashCode`

All wrapper types override `equals` and `hashCode` by **value**, so `Integer.valueOf(5).equals(5)` is
`true` and `new Integer(5).equals(5)` is `true`.

### `Boolean`, `Character` and `Double` caches

`Boolean.valueOf` always returns one of two cached instances (`TRUE`, `FALSE`), so
`Boolean b1 = true, b2 = true; b1 == b2` is `true`. `Character` caches only **0..127**. `Double` and
`Float` have **no** cache at all — `Double d1 = 1.0, d2 = 1.0; d1 == d2` is `false`.

## Worked example

**Q. What is printed?**

```java
public class Main {
    static void m(Object o)  { System.out.print("Object "); }
    static void m(String... s) { System.out.print("String... "); }
    public static void main(String[] args) {
        m("hi");
        m((Object) null);
        m((String) null);
        Integer i = 127;
        Integer j = 127;
        Integer k = 128;
        Integer l = 128;
        System.out.println();
        System.out.println(i == j);
        System.out.println(k == l);
    }
}
```

**Solution**

| Call | Phase | Chosen | Why |
|---|---|---|---|
| `m("hi")` | 1 (strict) | `m(Object)` | `String` → `Object` is a widening reference conversion, allowed in phase 1 |
| `m((Object) null)` | 1 (strict) | `m(Object)` | exact match |
| `m((String) null)` | 1 (strict) | `m(Object)` | `String` → `Object` widening reference, again in phase 1 |

**Output (exact):**

```
Object Object Object 
true
false
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `String...` for `m("hi")` | Varargs is the **last** phase; phase 1 already matched |
| `true` for `k == l` | 128 is outside the −128..127 cache |

## Quick rules

- Varargs **is** an array parameter: `int...` ≡ `int[]`.
- A varargs parameter must be the **last** parameter and there can be only **one**.
- `m()` with varargs → an **empty array**, not `null`.
- Unchecked → widening → boxing → varargs: **varargs is always last**.
- `Integer` −128..127 is cached; outside that range `==` on two `Integer`s is `false`.
- If either side of `==` is a primitive `int`, the comparison is **numeric**.
- Unboxing a `null` `Integer` → `NullPointerException`.
- `Integer + Integer` is **numeric addition** (`3`); concatenation needs a `String` operand.
- `Boolean` is cached; `Character` is cached for 0..127; `Double`/`Float` are **not** cached.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| Varargs beats widening | `String...` | Phase 1 wins |
| `Integer` 128 is cached | `true` | Only −128..127 |
| `Integer + Integer` concatenates | `"12"` | Both are unboxed and added → `3` |
| Unboxing `null` is fine | `null` | NPE |
| Two varargs parameters | compiles | Only one allowed |

## Checklist

- [ ] I know varargs compiles to an array parameter.
- [ ] I know the two varargs rules (last position, one per method).
- [ ] I know the `Integer` cache range exactly.
- [ ] I know that `Integer + Integer` adds, and only a `String` operand triggers concatenation.
- [ ] I know unboxing `null` throws NPE.

## Related

- [Static and final](01-static-and-final.md)
- [Operator precedence and arithmetic](03-operator-precedence-and-arithmetic.md)
- [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
- [Static/final/varargs traps](../04-pitfalls/01-static-final-varargs-traps.md)
- [Static/final/varargs one-pager](../05-reference/01-static-final-varargs-one-pager.md)
- [Topic overview](../README.md)
