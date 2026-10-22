# 04-pitfalls — Exceptions & Error Handling

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 10 min_

## What lives here

The named traps. Each one is written as **wrong answer → right answer → why → guard**, so you can
rebuild it from memory under pressure.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-exception-traps.md](01-exception-traps.md) | 128 | 9 named traps, the trap pattern, a summary table of wrong-vs-right options, a 5-item checklist |

## The 9 traps in one line each

1. `finally` always runs → it does not run after `System.exit()`.
2. `try`'s pending return wins → `finally`'s return wins.
3. Catch order does not matter → it does; wrong order is a compile error.
4. An unreachable checked catch is harmless → compile error.
5. `catch (Exception e)` catches `Error` → it does not.
6. An exception in `finally` keeps the original → it replaces it.
7. Short-circuit always skips the right operand → it skips conditionally.
8. `getMessage()` gives the full description → message only.
9. An uncaught exception lets the program continue → it ends the program.

## Related

- [Topic overview](../README.md)
- [Solved exception set](../03-worked-examples/01-solved-exception-set.md)
