# Static, Final, Varargs & Operators — Traps

> Section 4 · Java · Static, Final, Varargs & Operators · _Estimated reading time: 12 min_
> **Prerequisite:** [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)

## In one sentence

12 traps, each written as **the wrong answer you will pick → the right answer → the one-line
guard**.

## Why the pre-test tests this

These traps are the *distractors* you will meet in Section 4. If you can name the trap, you will
eliminate the wrong option on sight.

## Core concept

### The 12 traps

| # | Trap | The wrong answer you pick | The right answer | The one-line guard |
|---|---|---|---|---|
| 1 | Static blocks run at program start | "statics first" | They run at **first use** of the class | "Initialised on first active use" |
| 2 | A static block sees the final field value | `x = 20` | It sees the value at that point in source order | "Textual order, interleaved" |
| 3 | Instance initialiser runs after the constructor | `15` | Field initialisers and instance blocks run **before** the constructor body | "Initialisers → constructor" |
| 4 | A method call is a constant expression | `C` is a constant | Only literals and constant variables are | "`final` + type + constant expression" |
| 5 | Boxing beats widening | `m(Integer)` | Widening primitive comes first | "Exact → widen → box → varargs" |
| 6 | Varargs beats widening | `m(String...)` | Varargs is the **last** phase | "Varargs is the fallback" |
| 7 | `Integer` 128 is cached | `true` | Only **−128..127** is | "Cache range" |
| 8 | `Integer + Integer` adds | `3` | It concatenates → `"12"` | "`+` is text if any operand is a `String`" |
| 9 | `final` makes the array immutable | compile error | `final` freezes the **reference** | "Reference vs contents" |
| 10 | `Math.round(-2.5)` is `-3` | `-3` | `-2` — round is half **up** | "Half up, not half even" |
| 11 | `-7 / 2` floors to `-4` | `-4` | `-3` — truncation is toward **zero** | "Truncate, don't floor" |
| 12 | `>>>` preserves the sign | `-4` | `>>>` zero-fills → `2147483644` | "`>>` sign, `>>>` zeros" |

### The traps grouped

| Group | Traps | Shared root cause |
|---|---|---|
| Initialisation order | 1, 2, 3 | "When" vs "where in the source" |
| Constants | 4 | Missing one of the three conditions |
| Overloads | 5, 6 | Wrong phase order |
| Wrappers | 7, 8 | Cache range and `+` semantics |
| `final` | 9 | Reference vs object |
| Arithmetic | 10, 11, 12 | Sign and fill rules |

### Two traps that appear together

`Math.round`, `Math.floor`, and `Math.ceil` disagree **only on exact halves**, so a question designer
will always pick `2.5` or `-2.5`:

| Input | `round` | `floor` | `ceil` |
|---|---|---|---|
| `2.5` | `3` | `2.0` | `3.0` |
| `-2.5` | `-2` | `-3.0` | `-2.0` |

Read the **sign** off the answer, not just the magnitude.

### The two-sided `%` trap

```java
System.out.println(-7 % 2);    // -1
System.out.println(7 % -2);    //  1
System.out.println(-7 % -2);   // -1
```

The sign follows the **dividend** (the left operand) in all three cases. Java does **not** use the
mathematical "always non-negative" rule.

### The `final` + mutability trap

```java
final List<String> list = new ArrayList<>();
list.add("x");        // legal — the list's contents changed
list = new ArrayList<>();  // compile error — the reference cannot change
```

The same shape appears with arrays, `StringBuilder`, and `Date`.

## Worked example

**The trap in action.** A question says:

> What is printed?
> ```java
> class A {
>     static int x = 10;
>     static { x = x * 3; }
>     static int y = x;
> }
> ```
> Options: `30`, `10`, `90`, `3`.

**The trap:** you think the static block sees the *final* `x` (90) and pick `90`.

**The right reasoning:**

| Step | Statement | `x` |
|---|---|---|
| 1 | `static int x = 10;` | 10 |
| 2 | `static { x = x * 3; }` | 30 |
| 3 | `static int y = x;` | `y = 30` |

**Answer: `30`.**

## Quick rules

- Static init: first use, superclass first, textual order.
- Instance init: field initialisers → instance blocks → constructor body.
- Constant variable = `final` + primitive/`String` + constant expression.
- Overloads: exact → widening primitive → widening reference → boxing → varargs.
- `Integer` cache = −128..127; `Double`/`Float` = none.
- `+` is concatenation when any operand is a `String`.
- `final` freezes the reference.
- `round` = half up; division truncates toward zero; `%` follows the dividend; `>>>` zero-fills.

## Common traps

See the 12-row table above — each row is a one-line guard you can recite.

## Checklist

- [ ] I can name all 12 traps and their guards.
- [ ] I know the constant-variable conditions without hesitation.
- [ ] I know the overload phase order.
- [ ] I know the cache ranges.
- [ ] I know the rounding and sign rules for negative halves.

## Related

- [Static and final](../01-concepts/01-static-and-final.md)
- [Varargs and wrapper types](../01-concepts/02-varargs-and-wrapper-types.md)
- [Operator precedence and arithmetic](../01-concepts/03-operator-precedence-and-arithmetic.md)
- [Decision tables for overloads and operators](../02-techniques/01-decision-tables-for-overloads-and-operators.md)
- [Solved static/final/varargs set](../03-worked-examples/01-solved-static-final-varargs-set.md)
- [Static/final/varargs one-pager](../05-reference/01-static-final-varargs-one-pager.md)
- [Topic overview](../README.md)
