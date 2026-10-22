# The Evaluation-Order Model

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 20 min_
> **Prerequisite:** none

## In one sentence

Every output question is one of **12 constructs**, and each construct has exactly **one** rule set —
so the fastest path is to name the construct, not to simulate the program.

## Why the pre-test tests this

- "What does this print?" is a reported archetype of the 25-question Java section.
- The exam gives you 90 seconds. Simulating a 15-line program line by line does not fit. Naming the
  construct does.
- The same constructs reappear inside "does this code compile?" questions, so this file pays twice.

## Core concept

### The master order

```
1. Class loading        →  static field initialisers and static blocks, in SOURCE ORDER
2. Instance creation    →  super() → parent instance init → parent constructor body
                            → child instance init → child constructor body
3. Method body          →  statement by statement, left to right within a statement
```

### Rule 1 — static vs instance initialisation

| Order | What runs | When |
|---|---|---|
| 1 | Static field initialisers of the superclass | Class is initialised (first active use) |
| 2 | Static blocks of the superclass | ditto |
| 3 | Static field initialisers of the subclass | ditto |
| 4 | Static blocks of the subclass | ditto |
| 5 | Instance field initialisers + instance blocks of the superclass | `new` executes |
| 6 | Superclass constructor body | ditto |
| 7 | Instance field initialisers + instance blocks of the subclass | ditto |
| 8 | Subclass constructor body | ditto |

**The rule inside the rule:** static members and instance members are each initialised **in textual
(source) order**, and the two groups are interleaved if they appear in the same class:

```java
class A {
    static int s1 = print("static field");   // 1st
    static { print("static block"); }        // 2nd
    int i1 = print("instance field");         // 3rd (at new)
    { print("instance block"); }              // 4th (at new)
    A() { print("constructor"); }             // 5th (at new)
}
```

### Rule 2 — `super()` must be first

`super(...)` or `this(...)` **must be the first statement** of a constructor. Otherwise:

```
error: constructor call must be first statement in constructor
```

Because `super()` runs first, the parent's constructor body runs **before** the child's instance
initialisers. That is the classic surprise:

```java
class P { P() { System.out.println("P ctor"); } }
class C extends P { int x = print("C field"); C() { super(); System.out.println("C ctor"); } }
```

Output order: `P ctor`, then `C field`, then `C ctor`. (The `C field` initialiser runs after the
parent constructor completes.)

### Rule 3 — method resolution (overloads)

Three phases, in order. The **first phase that yields any applicable method wins**.

| Phase | Name | What it allows | Example |
|---|---|---|---|
| 1 | Strict invocation | Exact match, **widening primitive**, widening reference | `m(5)` → `m(long)` wins over `m(Integer)` |
| 2 | Loose invocation | Boxing / unboxing, then widening | `m(5)` → `m(Integer)` wins over `m(int...)` |
| 3 | Varargs | The varargs parameter treated as an array | `m(5)` → `m(int...)` only if phases 1–2 found nothing |

Within a phase, the **most specific** applicable method is chosen. `String...` beats `Object...`.

### Rule 4 — short-circuit

| Expression | Right operand evaluated when |
|---|---|
| `a && b` | `a` is **false** |
| `a \|\| b` | `a` is **true** |
| `c ? x : y` | only the **taken** branch is evaluated |

The untaken branch is **not evaluated at all** — no side effects, no exceptions, no `++`.

### Rule 5 — `++` and `--`

| Form | Value of the expression | Value of the variable afterwards |
|---|---|---|
| `i++` (post) | old value | old + 1 |
| `++i` (pre) | new value | new value |

In `a + b`, **`a` is evaluated first** (left to right). So `i++ + ++i` with `i = 5` gives
`5 + 7 = 12`, and `i` ends at 7.

### Rule 6 — compound assignment (`+=` etc.) is a cast

```
x += y    ≡    x = (T)(x + y)      where T is the DECLARED type of x
```

That is why these compile and these do not:

```java
byte b = 10;
b += 5;        // OK  → b = (byte)(10 + 5) = 15
b = b + 5;     // ERROR → int cannot be converted to byte
```

And it is why `int i = 10; i += 1.9;` gives **11**, not 11.9.

### Rule 7 — boxing, the `Integer` cache, and `==`

| Value | `Integer a = 127, b = 127; a == b` |
|---|---|
| −128..127 | **true** (the cache reuses the same object) |
| 128+ | **false** (two separate objects) |

`Integer.valueOf(x)` uses the cache for −128..127; `new Integer(x)` never does. Autoboxing uses
`valueOf`, so `Integer i = 10; i == 10` is `true`.

### Rule 8 — `switch` fall-through

`switch` does **not** break automatically. Execution starts at the matching `case` and runs onward
until a `break`, `return`, `throw`, or the end of the switch. If no `case` matches, `default` runs
(if present). If there is **no** `default` and nothing matches, **nothing happens**.

`break` exits the switch. `continue` inside a switch inside a loop continues the **loop**.

### Rule 9 — `for` vs `for-each` vs `enhanced `for` over arrays

| | Indexed `for` | For-each |
|---|---|---|
| Index available | Yes | No |
| Modifies elements | Yes (`a[i] = ...`) | Yes — `for (int x : a) x = 0;` does **not** change the array (it copies each element) |
| Skips elements | Yes | No |
| Works on | Arrays, `Iterable` | Arrays, `Iterable` |
| Null risk | None | Null pointer if the array/list is `null` |

### Rule 10 — `break` vs `continue` vs labels

| Keyword | Effect |
|---|---|
| `break` | Leaves the **innermost** loop or switch |
| `continue` | Skips to the **next iteration** of the innermost loop |
| `break label;` | Leaves the loop/switch named by `label` |
| `continue label;` | Next iteration of the loop named by `label` |

### Rule 11 — `instanceof` and casting

```java
Object o = "hello";
if (o instanceof String) {
    String s = (String) o;     // cast needed in Java 8
    System.out.println(s.length());   // 5
}
```

- `null instanceof String` → **false** (never throws).
- A cast between unrelated reference types compiles but throws `ClassCastException` at runtime.
- Pattern matching for `instanceof` (`if (o instanceof String s)`) is **Java 16+**; in Java 8 you
  must cast.

### Rule 12 — numeric promotion and `char` arithmetic

| Expression | Result | Why |
|---|---|---|
| `'a' + 1` | `98` (`int`) | `char` promotes to `int` |
| `'a' + "x"` | `"ax"` | `String` on the right → concatenation |
| `"x" + 'a'` | `"xa"` | `String` on the left → concatenation |
| `'a' + 1 + "x"` | `"98x"` | Left to right: `('a' + 1)` = 98, then concat |
| `true ? 1 : 2.0` | `2.0` (`double`) | Binary numeric promotion of the two branches |
| `true ? 1 : 2` | `1` (`int`) | Both branches `int` |
| `7 / 2` | `3` | Integer division |
| `7 / 2.0` | `3.5` | One operand `double` |
| `-7 / 2` | `-3` | Truncation toward zero |
| `-7 % 2` | `-1` | Sign follows the dividend |
| `7 % -2` | `1` | Sign follows the dividend |

## Worked example

**Q. What is printed?**

```java
public class Main {
    static class Base {
        static { System.out.print("BS"); }
        { System.out.print("BI"); }
        Base() { System.out.print("BC"); }
    }
    static class Derived extends Base {
        static { System.out.print("DS"); }
        { System.out.print("DI"); }
        Derived() { System.out.print("DC"); }
    }
    public static void main(String[] args) {
        System.out.print("M");
        new Derived();
    }
}
```

**Solution**

| # | Event | Output |
|---|---|---|
| 1 | `Main` class initialised, `main` starts | `M` |
| 2 | `new Derived()` → initialise `Base` (superclass first) | `BS` |
| 3 | initialise `Derived` | `DS` |
| 4 | `Base` instance init: instance block | `BI` |
| 5 | `Base` constructor body | `BC` |
| 6 | `Derived` instance init: instance block | `DI` |
| 7 | `Derived` constructor body | `DC` |

**Output (exact):**

```
MBSDSBIBCDIDC
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `BSDSMBIBCDC` | The static blocks run when `Derived` is first *used*, which is after `M` is printed |
| `MBSBSDS...` | The superclass is initialised before the subclass, not after |
| `MBSDSBIDCBC` | The child's instance block runs **after** the parent's constructor, not before |
| `BSDSMIBIDCC` | Both constructors run last, and in parent-then-child order |

## Quick rules

- Static init (superclass first) → instance init (superclass first) → constructor bodies.
- `super()` is the first statement; the parent constructor body runs before the child's field
  initialisers.
- Overloads: **strict → boxing → varargs**.
- `&&` needs the right side only when the left is false; `||` only when the left is true; the
  ternary evaluates one branch.
- `x += y` casts back to the type of `x`.
- `Integer` −128..127 is cached → `==` works there.
- `switch` falls through; `break` ends the switch.
- For-each copies each element; you cannot write back through it.
- `char` + `int` = `int`; `char`/`int` + `String` = concatenation.
- Integer division truncates toward zero; `%` takes the sign of the dividend.

## Common traps

| Trap | Wrong output | Right output |
|---|---|---|
| Static blocks run before `main` | `BSDS...` first | They run at first *use* of the class |
| Child field initialiser before parent constructor | `DI` before `BC` | `BC` then `DI` |
| Varargs wins over widening | `m(int...)` chosen | Widening (`m(long)`) wins |
| `i++ + ++i` = 11 | 11 | 12, and `i` = 7 |
| `Integer` 128 `==` 128 | true | false |
| `switch` without `break` stops at the case | stops | falls through to the next case |
| `for-each` writing back | array updated | array unchanged |

## Checklist

- [ ] I can name all 12 constructs and the single rule that decides each.
- [ ] I can state the 3 overload phases and their order.
- [ ] I know exactly what `i++ + ++i` evaluates to when `i = 5`.
- [ ] I know `x += y` is `x = (T)(x + y)`.
- [ ] I know the `Integer` cache range is −128..127.
- [ ] I can predict the exact output of the worked example above.

## Related

- [Compile vs run taxonomy](02-compile-vs-run-taxonomy.md)
- [10-second triage](../02-techniques/01-ten-second-triage.md)
- [Method resolution and short-circuit](../02-techniques/02-method-resolution-and-short-circuit.md)
- [Solved output set A](../03-worked-examples/01-solved-output-set-a.md)
- [Solved output set B](../03-worked-examples/02-solved-output-set-b.md)
- [Output traps](../04-pitfalls/01-output-traps.md)
- [Output rules one-pager](../05-reference/01-output-rules-one-pager.md)
- [Topic overview](../README.md)
