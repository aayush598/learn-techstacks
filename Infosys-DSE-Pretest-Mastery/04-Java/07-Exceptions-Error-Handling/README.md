# Exceptions & Error Handling — Topic Guide

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 90 min for the full topic_

## What the pre-test asks in this topic

The Java section is 25 questions in ~35 minutes. Reported archetypes in this topic are
**errors & exceptions** and **"does this code compile / does this run"**. Concretely, the pre-test
asks you to recognise, in this order:

1. **Which catch block wins** — given a `try` body and several `catch` clauses, name the one that
   catches the thrown exception.
2. **Compile error or runtime error** — "does this code compile?", "what happens when it runs?".
3. **What does it print** — the output of a `try/catch/finally` block, especially the
   `finally`-overrides-`return` trap.
4. **Which exception type** — checked vs unchecked, `Throwable` vs `Exception` vs `RuntimeException`.
5. **What does the method declare** — `throws` vs `throw`, propagation up the call stack.

You never need to write exception-handling code in the pre-test. You need to **trace** it.

## Learning objectives

After this topic you should be able to:

- Draw the `Throwable` hierarchy from memory and label which branch is checked and which is unchecked.
- Decide in under 5 seconds whether a `catch` clause is a **compile error** (unreachable catch, checked
  exception never thrown) or a **runtime** event.
- Trace the execution order of `try` → `catch` → `finally` and state the **exact printed output** for
  any given combination of `return`, `throw` and `finally`.
- Explain why `finally` overrides a `return` in the `try` block, and why `System.exit()` skips
  `finally` entirely.
- Distinguish `throw` (raise) from `throws` (declare) and state which one belongs in a method signature.
- Use `getMessage()` and `getCause()` correctly, and say when `printStackTrace()` is the wrong tool.
- Write a custom checked exception in 3 lines and say why it is checked.

## File index

| File | What it gives you |
|---|---|
| [01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md](01-concepts/01-throwable-hierarchy-and-checked-vs-unchecked.md) | The hierarchy, checked vs unchecked, `throws` vs `throw`, custom exceptions |
| [01-concepts/02-try-catch-finally-and-resource-management.md](01-concepts/02-try-catch-finally-and-resource-management.md) | Block semantics, `finally` vs `return`, try-with-resources, propagation |
| [02-techniques/01-trace-the-exception-path.md](02-techniques/01-trace-the-exception-path.md) | The 6-step trace procedure and the "execution table" method |
| [02-techniques/02-choose-the-right-catch-strategy.md](02-techniques/02-choose-the-right-catch-strategy.md) | Which catch wins, multi-catch, catch ordering rules, decision tables |
| [03-worked-examples/01-solved-exception-set.md](03-worked-examples/01-solved-exception-set.md) | 10 fully solved questions with exact output strings and distractor breakdowns |
| [04-pitfalls/01-exception-traps.md](04-pitfalls/01-exception-traps.md) | 9 named traps, each with the wrong answer and the right answer |
| [05-reference/01-exception-one-pager.md](05-reference/01-exception-one-pager.md) | The printable one-page sheet: hierarchy, rules, 60-second budget |

## Quick procedure — trace any `try/catch/finally` question in 60 seconds

1. **List the throw sites.** Every `throw`, every call that can throw, every operation that can throw
   (divide by zero, array index, null dereference, cast).
2. **For each throw site, name the exception type** and whether it is checked or unchecked.
3. **Find the first matching catch** — top to bottom. The first `catch` whose parameter type is a
   supertype of the thrown type wins. If none matches, the exception **propagates**.
4. **Run the `finally` block** if there is one — it runs on the normal path, on the catch path, and on
   the propagating path. It does **not** run after `System.exit()`.
5. **Resolve the return value**: if `finally` has a `return`, it wins. Otherwise the pending value
   (from `try` or `catch`) is returned.
6. **Write the output as a quoted string** and compare it to the options character by character.

## Key takeaways

- ✅ **Unchecked = `RuntimeException` + `Error`.** Everything else under `Exception` is checked and
  must be caught or declared.
- ✅ **A checked exception that is never thrown in the `try` body is a compile error.** Catching
  `Exception` or `Throwable` is always allowed.
- ✅ **Catch order is top-to-bottom.** A subclass catch placed after its superclass catch is a compile
  error — "exception has already been caught".
- ✅ **`finally` runs last, always — except after `System.exit()`.** And a `return` inside `finally`
  **discards** the value from `try`/`catch`.
- ✅ **An exception thrown inside `finally` replaces the original** and the original is lost.
- ✅ **`throw` raises; `throws` declares.** `throws` only appears in the method signature.
- ✅ **`printStackTrace()` prints to stderr and does not stop the program.** `getMessage()` returns
  only the message; `getCause()` returns the wrapped exception.
- ⚠️ **Karthik's retro:** he lost 3 marks to "finally overrides return" and 2 to "catch the
  superclass first". Memorise the two tables on the one-pager, not the theory.

## Related

- [Output Prediction Patterns](../08-Output-Prediction-Patterns/) — output questions are where
  exception handling usually shows up
- [Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/) — `static` initialisation
  order and `final` constants show up in `static`/instance init questions
- [Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/) — `ArrayIndexOutOfBoundsException` and
  `ConcurrentModificationException` live here
- [Java question bank](../13-Question-Bank/) — 90+ questions across every Java archetype
- [Master README](../../README.md)
