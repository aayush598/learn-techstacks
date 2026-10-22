# Exception Traps — 9 Named Traps

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 10 min_
> **Prerequisite:** [Solved exception set](../03-worked-examples/01-solved-exception-set.md)

## In one sentence

Every trap below is a **near-miss option** the exam writes on purpose — each one produces a
*plausible* printed string that is wrong.

## Why the pre-test tests this

- Reported archetypes in the Java section include "errors & exceptions" and "does this code run".
- A trap question is worth exactly what you know: the wrong option is designed to be attractive to
  candidates who half-remember the rule.
- Karthik's retrospective: his error log for the Java section was 5 traps, all in this file's list.

## Core concept

The trap pattern is always the same:

```
Correct rule  →  Option B  (plainly correct, easy to spot)
Trap reading  →  Option C  (what you get if you half-remember)
Common misread →  Option D  (what you get if you skim)
Nonsense       →  Option A
```

So the fastest defensive move is: **do not look for the option that "sounds like the topic". Look for
the option that survives the exact rule.**

## The 9 traps

### Trap 1 — "Finally always runs"

- **Wrong answer:** the option that shows the `finally` output *after* `System.exit()`.
- **Right answer:** `System.exit()` skips `finally` entirely.
- **Why:** JVM shutdown does not unwind Java frames.
- **Guard:** the *only* thing that skips `finally` is `System.exit()` (or JVM halt). Everything else
  — including an uncaught exception — runs `finally`.

### Trap 2 — "Finally's return is overridden by try's return"

- **Wrong answer:** `try` wins because it appears first.
- **Right answer:** `finally`'s `return` wins.
- **Why:** a `return` in `finally` performs its own return; the pending value is discarded.
- **Guard:** ask "does `finally` contain a `return`?" If yes → `finally` wins. If no → the pending
  value survives.

### Trap 3 — "The catch after the catch that already covers it is fine"

- **Wrong answer:** "It compiles."
- **Right answer:** compile error — `exception X has already been caught`.
- **Why:** an unreachable `catch` is a compile error.
- **Guard:** superclass first + subclass later = error. Subclass first = fine.

### Trap 4 — "Catch checked exception never thrown is harmless"

- **Wrong answer:** "It compiles; the catch is just dead code."
- **Right answer:** compile error — `exception X is never thrown in body of corresponding try statement`.
- **Why:** checked exceptions must be *reachable*. `catch (Exception e)` is the escape hatch because
  unchecked exceptions are always possible.

### Trap 5 — "Catch Exception catches Error"

- **Wrong answer:** "One `catch (Exception e)` handles everything."
- **Right answer:** `Error` is a **sibling** of `Exception` under `Throwable`; only
  `catch (Throwable e)` catches both.

### Trap 6 — "An exception in finally keeps the original"

- **Wrong answer:** the option showing the original exception's message.
- **Right answer:** the `finally` exception replaces it; the original is lost.
- **Guard:** the "suppressed exception" mechanism only exists in try-with-resources, for the
  `close()` failure. A throw *inside* the `finally` body always replaces.

### Trap 7 — "Short-circuit always skips the second operand"

- **Wrong answer:** for `false || X`, the answer "the second operand does not run".
- **Right answer:** `||` skips the right operand only when the left is **true**; `&&` skips it only
  when the left is **false**.
- **Guard:** `||` needs the right side when the left is false. `&&` needs it when the left is true.

### Trap 8 — "getMessage gives the whole exception description"

- **Wrong answer:** `java.io.IOException: file missing`.
- **Right answer:** `file missing`.
- **Guard:** `getMessage()` → message only. `toString()` / `printStackTrace()` → `type: message`.

### Trap 9 — "Uncaught exception prints and the program continues"

- **Wrong answer:** the option showing the line after the throw being printed.
- **Right answer:** the stack trace goes to stderr, the JVM exits with a non-zero status, and
  nothing after the throw point runs.
- **Guard:** `printStackTrace()` inside a `catch` continues the program; an **uncaught** exception
  does not.

## Common traps (summary table)

| # | Trap | Wrong option says | Right option says |
|---|---|---|---|
| 1 | `finally` after `System.exit()` | B printed | Only A printed |
| 2 | `return` in `finally` | `try` wins | `finally` wins |
| 3 | catch ordering | compiles | compile error: already caught |
| 4 | checked catch never thrown | compiles | compile error: never thrown |
| 5 | `catch (Exception)` vs `Error` | catches everything | need `Throwable` |
| 6 | exception in `finally` | original survives | original replaced |
| 7 | short-circuit | right operand always skipped | skipped only per truth value |
| 8 | `getMessage()` | `Type: message` | `message` |
| 9 | uncaught exception | program continues | program ends, non-zero exit |

## Checklist

- [ ] I can name the 9 traps without looking.
- [ ] I know the exact difference between `getMessage()` and `toString()` output.
- [ ] I know that `finally` is skipped **only** by `System.exit()`.
- [ ] I can state both javac messages for catch errors.
- [ ] I know that `||` and `&&` short-circuit in *opposite* directions.

## Related

- [Throwable hierarchy, checked vs unchecked](../01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md)
- [try/catch/finally and resource management](../01-concepts/02-try-catch-finally-and-resource-management.md)
- [Trace the exception path](../02-techniques/01-trace-the-exception-path.md)
- [Choose the right catch strategy](../02-techniques/02-choose-the-right-catch-strategy.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
- [Exception one-pager](../05-reference/01-exception-one-pager.md)
- [Topic overview](../README.md)
