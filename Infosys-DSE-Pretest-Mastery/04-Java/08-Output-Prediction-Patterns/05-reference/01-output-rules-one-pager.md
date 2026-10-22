# Output Rules — One-Page Revision Sheet

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 6 min_
> **Prerequisite:** [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)

## In one sentence

Print this page and the entire output-prediction topic is **ten rules and one triage**.

## Why the pre-test tests this

- Output questions are the single biggest cluster in the Java section.
- This page is the whole revision surface. If you can apply the ten rules, you own this archetype.

## Core concept

### The ten rules

| # | Rule | One-line form |
|---|---|---|
| 1 | Init order | static (super→sub) → instance (super→sub) → ctor (super→sub) |
| 2 | `super()` first | the parent constructor completes before the child's field initialisers |
| 3 | Overloads | strict → boxing → varargs; most specific wins inside a phase |
| 4 | Short-circuit | `&&` needs the right side only if the left is true; `||` only if the left is false; the ternary evaluates one branch |
| 5 | `++` | post yields the old value, pre yields the new; operands evaluate left to right |
| 6 | `+=` | `x += y` ≡ `x = (T)(x + y)` |
| 7 | Boxing | `Integer` −128..127 cached; `String` literals interned; `new String(...)` is not |
| 8 | `switch` | falls through; `default` is reached by falling into it |
| 9 | Loops | for-each copies elements; `break` leaves the innermost loop; `continue` skips one iteration; labels change the target |
| 10 | Types | `char`→`int`; a `String` operand forces concatenation; `int` division truncates; `%` follows the dividend; ternary promotes numerically |

### Operator precedence (highest first) — the short version

```
postfix   ++ --  !  (cast)
unary     + -  ~  ++ --
multiplicative   * / %
additive         + -
shift            << >> >>>
relational       < > <= >= instanceof
equality         == !=
bitwise AND      &
bitwise XOR      ^
bitwise OR       |
logical AND      &&
logical OR       ||
ternary          ? :
assignment       = += -= *= /= %= &= |= ^= <<= >>= >>>=
```

**`+` and `-` are left-associative**, so `10 - 3 - 2` = `5`, not `9`.

### The number-to-string table

| Value | Printed |
|---|---|
| `int` 5 | `5` |
| `long` 5L | `5` |
| `double` 5.0 | `5.0` |
| `float` 5.0f | `5.0` |
| `char` 'a' | `a` |
| `boolean` true | `true` |
| `null` in a concatenation | `null` |

### 60-second budget for one output question

| Phase | Seconds | Action |
|---|---|---|
| Triage | 3 | Find the interesting line, name the construct |
| Compile gate | 5 | Any compile-error construct? → answer "does not compile" |
| Apply one rule | 20 | Pull it from the table |
| Format | 10 | `println` adds `\n`; `print` does not; `5` vs `5.0` |
| Write the string | 7 | Quoted, spaces included |
| Match | 10 | Character by character |
| **Total** | **~55** | 35 s of slack |

## Worked example

**Q. What is printed?**

```java
public class Main {
    public static void main(String[] args) {
        int i = 0;
        int[] a = new int[3];
        a[i++] = ++i;
        System.out.println(a[0] + " " + a[1] + " " + i);
    }
}
```

- Index expression `i++` → yields **0**, and `i` becomes 1.
- Right-hand side `++i` → `i` becomes **2**, yields **2**.
- Store: `a[0] = 2`. `a[1]` is still `0`. `i` is 2.

**Output (exact):**

```
2 0 2
```

## Quick rules

- Triage first, then apply exactly **one** rule.
- A compile error produces **no output**.
- `println` adds a newline, `print` does not.
- Write the answer as a quoted string before you look at the options.
- If no option matches, change the **construct**, not the arithmetic.
- Threads are the exception: only the **guaranteed** statement is correct.

## Common traps

| Trap | Fix |
|---|---|
| Simulating the whole program | Triage |
| Missing a trailing space | Quote the string exactly |
| `5` vs `5.0` | Check the declared type |
| Picking the closest option | Re-check the construct |
| Believing threads are ordered | Only guaranteed statements count |

## Checklist

- [ ] I can recite the ten rules.
- [ ] I can write the precedence table from memory.
- [ ] I know the number-to-string table.
- [ ] I know the 60-second budget.
- [ ] I can produce the worked example's output (`2 0 2`) without running it.

## Related

- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)
- [10-second triage](../02-techniques/01-ten-second-triage.md)
- [Method resolution and short-circuit](../02-techniques/02-method-resolution-and-short-circuit.md)
- [Solved output set A](../03-worked-examples/01-solved-output-set-a.md)
- [Solved output set B](../03-worked-examples/02-solved-output-set-b.md)
- [Output traps](../04-pitfalls/01-output-traps.md)
- [Compile-error catalogue](02-compile-error-catalogue.md)
- [Topic overview](../README.md)
