# 03-worked-examples — Exceptions & Error Handling

> Section 4 · Java · Exceptions & Error Handling · _Estimated reading time: 16 min_

## What lives here

10 fully solved exception questions, each with the **exact printed output** as a quoted string and a
breakdown of why every wrong option is wrong.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-solved-exception-set.md](01-solved-exception-set.md) | 365 | 10 solved questions: `finally` vs `return`, catch ordering (compile error), `System.exit`, exception in `finally`, never-thrown checked catch, short-circuit `||`, try-with-resources, `ClassCastException`, pending return + `finally` print, `throws` + `getMessage` |

## The questions at a glance

| Q | Archetype | Answer |
|---|---|---|
| Q1 | `finally` with `return` | prints `finally` |
| Q2 | catch ordering | does not compile |
| Q3 | `System.exit()` | prints `A` only |
| Q4 | exception in `finally` | `IllegalStateException`, original lost |
| Q5 | checked catch never thrown | does not compile |
| Q6 | short-circuit `\|\|` | prints `true` then `2` |
| Q7 | try-with-resources | prints `init`, `use`, `close` |
| Q8 | bad cast | `ClassCastException` |
| Q9 | `finally` without `return` | prints `F1` |
| Q10 | `throws` + `getMessage()` | prints `file missing` |

## Related

- [Topic overview](../README.md)
- [Techniques: trace the exception path](../02-techniques/01-trace-the-exception-path.md)
