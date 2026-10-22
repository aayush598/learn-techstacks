# 03-worked-examples — Strings, Immutability, equals & hashCode

> Section 4 · Java · Strings, Immutability, equals & hashCode · _Estimated reading time: 16 min_

## What lives here

9 fully solved string questions with the **exact printed output** as a quoted string, plus a
breakdown of why every wrong option is wrong.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-solved-string-set.md](01-solved-string-set.md) | 366 | 9 questions: literals vs `new String`, `HashSet` de-duplication, `"Java".hashCode()` = 2301506, runtime concatenation vs constant folding, `equals` vs `equalsIgnoreCase` vs `compareTo`, `null` concatenation and NPE, `replace` vs `replaceAll`, `matches` scope, `split` trailing empties, `String` vs `StringBuilder` mutation |

## The questions at a glance

| Q | Archetype | Answer |
|---|---|---|
| Q1 | literals vs `new String` | `true`, `true` |
| Q2 | `HashSet` + `==` | `1`, `false`, `true` |
| Q3 | `String.hashCode()` | `2301506`, `2301506`, `true` |
| Q4 | runtime concatenation | `true`, `false`, `true` |
| Q5 | case-sensitive comparison | `false`, `true`, `false`, `true` |
| Q6 | `null` concatenation | `null!`, `!null`, `null`, then NPE |
| Q7 | regex vs literal | `a#b#`, `a1b2`, `true`, `false` |
| Q8 | `split` trailing empties | `2`, `4` |
| Q9 | immutability vs mutation | `Java`, `JavaScript` |

## Related

- [Topic overview](../README.md)
- [Techniques: string API decision table](../02-techniques/01-string-api-decision-table.md)
