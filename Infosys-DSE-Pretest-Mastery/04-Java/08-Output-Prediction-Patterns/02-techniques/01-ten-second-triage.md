# The 10-Second Triage for Output Questions

> Section 4 · Java · Output Prediction Patterns · _Estimated reading time: 9 min_
> **Prerequisite:** [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)

## In one sentence

Do not simulate the program — **find the one interesting line, name its construct, apply one rule,
write the string**.

## Why the pre-test tests this

- You get 90 seconds. A 15-line program with a `for` loop, a `switch` and a `try` cannot be
  simulated line by line in 90 seconds.
- But every output question has exactly **one** construct doing the work. The rest is noise.
- This procedure is also how you solve "does this compile?" questions in under 20 seconds.

## Core concept

### The triage

**Step 1 (3 s) — Scan for the interesting line.** Look for these 12 markers:

| Marker | Construct |
|---|---|
| `++` / `--` | pre/post increment |
| `+=` or any compound assignment | implicit cast |
| `==` between objects | `==` vs `equals` |
| `+` with a `String` anywhere in the expression | concatenation |
| `/` or `%` | integer division / negative modulo |
| `switch` | fall-through |
| `break` / `continue` | loop control |
| `catch` / `finally` | exception path |
| `static {` | class initialisation order |
| `new X(` where `X` has overloads | method resolution |
| `instanceof` / a cast | type test |
| `? :` | ternary + promotion |
| `for (T x : ...)` | for-each copy semantics |

**Step 2 (2 s) — Name the construct.** Twelve options. Say the name in your head.

**Step 3 (20 s) — Apply exactly one rule.** Pull it from
[the evaluation-order model](../01-concepts/01-the-evaluation-order-model.md). Resist the urge to
check every other line.

**Step 4 (5 s) — Check the compile gate.** Did the snippet contain a construct from the compile-error
catalogue? If yes, the output is nothing.

**Step 5 (10 s) — Write the output as a quoted string.** Include trailing spaces if there are any.

**Step 6 (10 s) — Match.** Compare character by character. If nothing matches, you mis-identified
the construct — go back to step 2, not to step 3.

Total: ~50 seconds, leaving 40 seconds of slack.

### The "exact output" contract

The exam writes options like:

```
A. "5"
B. "55"
C. "5 5"
D. "6"
```

Three things decide between them:

| Trap | Example |
|---|---|
| Missing newline | `println` adds `\n`; `print` does not |
| Missing space | `print("a "); print("b");` → `"a b"`, not `"ab"` |
| Wrong type in the string | `int` 5 → `"5"`; `char` '5' → `"5"`; `double` 5.0 → `"5.0"` |

**Number formatting rules you need:**

| Value | Printed as |
|---|---|
| `int` 5 | `5` |
| `long` 5L | `5` |
| `double` 5.0 | `5.0` |
| `float` 5.0f | `5.0` |
| `double` 5.5 | `5.5` |
| `double` 5.0 / 2 | `2.5` |
| `char` 'a' | `a` |
| `boolean` true | `true` |
| `null` (String concat) | `null` |

Note `5.0 / 2` → `2.5`, but `5 / 2` → `2` (int) and `(double) 5 / 2` → `2.5`.

### Question shapes and their fastest attack

| Question shape | Fastest attack | Typical time |
|---|---|---|
| "What does this print?" with one `println` | Find the variable's final value; trace only its assignments | 30 s |
| "What does this print?" with a loop | Write the loop's first and last iteration by hand | 45 s |
| "Which method is called?" | Apply the 3-phase overload rule | 30 s |
| "Does this compile?" | Scan for the 5 compile-error families | 20 s |
| "What is thrown?" | Find the throw site, name the type | 25 s |
| "What is the order of output?" | Apply the init-order table | 35 s |
| "Which statement is TRUE?" (threads) | Pick the only *guaranteed* statement | 20 s |

### The "guess the option shape" shortcut

If your computed string matches no option, do **not** pick the closest. Instead:

1. Re-read the stem — did it ask for the output *including* the exception text?
2. Did you miss a `println` vs `print` newline?
3. Did you miss that the code **does not compile**?
4. Did you mis-name the construct?

### The one case you cannot triage: threads

If the snippet creates a `Thread` and calls `start()`, **the interleaving is not guaranteed**. The
right answer to such a question is the option that states a **guaranteed** fact, e.g.:

- "The `run()` body executes exactly once, on a thread other than the caller."
- "`main` completes after `t.start()` returns."

Never pick "Main always prints last" or "Child always prints first". See
[Threads (Basic)](../../12-Threads-Basic/).

## Worked example

**Q. What is printed?**

```java
public class Main {
    public static void main(String[] args) {
        int i = 1;
        int[] a = {10, 20, 30};
        a[i++] = i;
        System.out.println(a[1] + " " + a[2]);
    }
}
```

**Triage** — markers: `i++` (post increment) and `+` with a `String`. Construct: **pre/post
increment** + **string concatenation**.

**Step 3 — Apply the rule.** `a[i++] = i;`

Java evaluates the **array reference** and the **index** of the left-hand side first, then the
**right-hand side**, then performs the store.

1. Index expression: `i++` → yields **1** (old value), and `i` becomes **2**.
2. Right-hand side: `i` → **2**.
3. Store: `a[1] = 2`.

**Step 5 — The output.**

`a[1]` is `2`, `a[2]` is `30`. `"2" + " " + "30"` → `"2 30"`.

**Output (exact):**

```
2 30
```

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `1 30` | The index is the old value (1) but the stored value is the new value (2) |
| `2 20` | `a[2]` was never written to; it is still 30 |
| `1 20` | Both halves wrong |
| `2 30` with a different order | `a[1]` is printed first |

## Quick rules

- Triage in 3 seconds, then apply **one** rule.
- A compile error means **no output**.
- Check `println` vs `print` and trailing spaces before you match options.
- `int` prints `5`; `double` prints `5.0`; `char` prints the character.
- If nothing matches, change the **construct**, not the arithmetic.
- Threads: only the guaranteed statement is correct.

## Common traps

| Trap | Fix |
|---|---|
| Simulating the whole program | Find the interesting line |
| Forgetting `println` adds a newline | Write the exact string |
| Forgetting `5.0` vs `5` | Check the declared type |
| Picking the closest option | Re-check the construct |
| Believing threads print in a fixed order | Only guaranteed statements are correct |

## Checklist

- [ ] I can list the 12 triage markers from memory.
- [ ] I know the number-to-string rules (`5` vs `5.0` vs `a`).
- [ ] I write the output as a quoted string before looking at the options.
- [ ] I check the compile gate before computing output.
- [ ] I know the thread exception to the whole procedure.

## Related

- [The evaluation-order model](../01-concepts/01-the-evaluation-order-model.md)
- [Compile vs run taxonomy](../01-concepts/02-compile-vs-run-taxonomy.md)
- [Method resolution and short-circuit](02-method-resolution-and-short-circuit.md)
- [Solved output set A](../03-worked-examples/01-solved-output-set-a.md)
- [Output traps](../04-pitfalls/01-output-traps.md)
- [Topic overview](../README.md)
