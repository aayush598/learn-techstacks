# Output Traps — 12 Named Traps

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 12 min_
> **Prerequisite:** [Solved output set A](../03-worked-examples/01-solved-output-set-a.md)

## In one sentence

Each trap is a **specific wrong output string** that candidates reliably pick — knowing the string
they will pick is what makes the trap avoidable.

## Why the pre-test tests this

- The Java section's output questions are deliberately built around near-misses.
- Every trap below is worth exactly one mark. Twelve traps is twelve marks of insurance.
- Karthik's retro: his Java error log was 9 of these 12 traps. He had never seen a list like it.

## Core concept

The trap pattern:

```
The trap produces a WRONG OUTPUT STRING that is "one step away" from the truth.
One step away = you applied 90% of the rule.
```

So the defensive move is to ask: **"which single rule did I skip?"**

## The 12 traps

### Trap 1 — Static blocks "run at the start of the program"

- **Wrong output:** `"A-static B-static ..."` printed before anything else.
- **Right output:** static blocks run when the class is **first used**, not when the program starts.
- **Why:** `new Derived()` inside `main` triggers the class initialisation at that point.
- **Guard:** "first active use", not "program start".

### Trap 2 — The child's field initialiser runs before the parent's constructor

- **Wrong output:** `"B-inst B-ctor A-inst A-ctor"`.
- **Right output:** `"A-inst A-ctor B-inst B-ctor"`.
- **Why:** `super()` is the first statement, so the parent's constructor completes first.
- **Guard:** parent constructor **always** completes before the child's initialisers.

### Trap 3 — Varargs beats widening or boxing

- **Wrong output:** `int...` chosen for `m(5)`.
- **Right output:** widening (`m(long)`) or boxing (`m(Integer)`) wins.
- **Why:** varargs is phase 3.
- **Guard:** strict → boxing → varargs.

### Trap 4 — "The first catch clause in the source always wins"

- **Wrong output:** picking the `catch (Exception e)` clause.
- **Right output:** the first clause whose type **matches** wins — which may be a later clause.
- **Why:** `catch (ArithmeticException e)` before `catch (Exception e)` catches the arithmetic error.

### Trap 5 — Short-circuit always skips the right operand

- **Wrong output:** `i` ending at 1 for `false || (...)`.
- **Right output:** `i` ends at 2 — the right operand **must** run when the left is false.
- **Why:** `||` needs the right side when the left is false; `&&` needs it when the left is true.

### Trap 6 — `i++` yields the new value

- **Wrong output:** `i++ + ++i` = `14`, or `i` = 8.
- **Right output:** `12`, and `i` = 7.
- **Why:** post-increment yields the **old** value.

### Trap 7 — `Integer` 128 is cached

- **Wrong output:** `true` for `Integer c = 128, d = 128; c == d`.
- **Right output:** `false`. The cache is −128..127.
- **Guard:** 127 is cached, 128 is not.

### Trap 8 — `new String("abc")` is interned

- **Wrong output:** `true` for `"abc" == new String("abc")`.
- **Right output:** `false`. Only literals and `intern()` use the pool.

### Trap 9 — `switch` breaks automatically

- **Wrong output:** `"two "` only.
- **Right output:** `"two three default "` — no `break`, so it falls through, and `default` is
  reached by falling into it.

### Trap 10 — For-each writes back into the array

- **Wrong output:** the array doubled after a for-each loop.
- **Right output:** the array is unchanged — the loop variable is a **copy**.

### Trap 11 — Integer division rounds

- **Wrong output:** `7 / 2` = `4`, or `7 / 2` = `3.5`.
- **Right output:** `7 / 2` = `3` (truncation toward zero), `7 / 2.0` = `3.5`.
- **Guard:** both operands `int` → integer division.

### Trap 12 — The modulo result is always non-negative

- **Wrong output:** `-7 % 2` = `1`.
- **Right output:** `-1`. The sign of the result follows the **dividend**.

## The trap table

| # | Trap | Wrong output | Right output |
|---|---|---|---|
| 1 | Static blocks at program start | statics first | statics at first use |
| 2 | Child init before parent ctor | `B-inst B-ctor A-inst A-ctor` | `A-inst A-ctor B-inst B-ctor` |
| 3 | Varargs wins | `int...` | `long` / `Integer` |
| 4 | First clause wins | `generic` | `arith` |
| 5 | Short-circuit always skips | `i = 1` | `i = 2` |
| 6 | `i++` yields new value | `14` | `12` |
| 7 | 128 cached | `true` | `false` |
| 8 | `new String` interned | `true` | `false` |
| 9 | `switch` auto-breaks | `two ` | `two three default ` |
| 10 | For-each writes back | array doubled | array unchanged |
| 11 | Integer division rounds | `3.5` | `3` |
| 12 | Modulo is non-negative | `1` | `-1` |

## Common traps

| Trap | Fix |
|---|---|
| Assuming the exam's "obvious" option | Re-apply the one rule for that construct |
| Computing the whole program | Name the construct, apply one rule |
| Forgetting trailing spaces | Write the output as a quoted string |
| Choosing the closest option | Change the construct, not the arithmetic |

## Checklist

- [ ] I can name all 12 traps.
- [ ] I can write the *wrong* output string for traps 1, 2, 9 and 10 from memory.
- [ ] I know the exact `Integer` cache range.
- [ ] I know the modulo sign rule.
- [ ] I never pick an option with printed output for code that does not compile.

## Related

- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Solved output set A](../03-worked-examples/01-solved-output-set-a.md)
- [Solved output set B](../03-worked-examples/02-solved-output-set-b.md)
- [Compile-error traps](02-compile-error-traps.md)
- [Output rules one-pager](../05-reference/01-output-rules-one-pager.md)
- [Topic overview](../README.md)
