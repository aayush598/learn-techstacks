# Ranking and Ordering — One-Page Revision Sheet

> Section 1 · Aptitude · Ranking & Ordering · _Estimated reading time: 4 min_
> **Prerequisite:** [Ranking and ordering rules](../01-concepts/01-ranking-ordering-rules.md)

## In one sentence

Print this page: the phrase translation table, the rank formulas, the north/south flip, and the
"must be true" test — the entire archetype on one sheet.

## Why the pre-test tests this

- One ranking question per paper. It should be one of your fastest marks.
- Every point of this topic is a translation error or an assumption. Both are avoidable with a table.

## Core concept

### Phrase translation table

| Phrase | Rule |
|---|---|
| X is second **to the left of** Y | `pos(X) = pos(Y) − 2` |
| X is second **from the left end** | `pos(X) = 2` |
| X is immediately left of Y | `pos(X) = pos(Y) − 1` |
| X is immediately right of Y | `pos(X) = pos(Y) + 1` |
| X is somewhere left of Y | `pos(X) < pos(Y)` |
| X is third from the right end | `pos(X) = n − 2` |
| X is at the extreme left / right | `pos(X) = 1` / `n` |

### Rank arithmetic

| Quantity | Formula |
|---|---|
| Total from two ranks | `r_top + r_bottom − 1` |
| Bottom rank from top rank | `n − r_top + 1` |
| Rank after gaining k marks | `r − k` |

### North / south flip

| Row faces | Extreme LEFT is | Extreme RIGHT is |
|---|---|---|
| North | seat 1 | seat n |
| South | seat n | seat 1 |

### Chain quick answers

```
Meera < Karthik < Ananya < Divya
```

| Question | Read |
|---|---|
| Tallest / oldest / fastest | Right end of the chain |
| Shortest / youngest / slowest | Left end |
| Second from the right | The one just before the last |
| How many are greater than X? | Count the signs to the right of X |

### "Must be true" test

1. Build arrangement 1.
2. Try to build arrangement 2.
3. If a second arrangement exists, the option must hold in **both**.
4. If only one arrangement exists, read it directly.

### Slot table template

```
Seat:   1     2     3     4     5     6
Person: __   __   __   __   __   __
```

Fill order: extreme ends → fixed seats → `pos ± k` clues → leftovers.

### Time budget

| Phase | Seconds |
|---|---|
| Draw the table | 10 |
| Place anchors | 15 |
| Place relative clues | 30 |
| Fill leftovers | 10 |
| Verify clues | 15 |
| Answer (incl. flip) | 10 |
| **Total** | **~90** |

## Worked example

**Q. Ananya scored 5th highest and 7th lowest. How many participants?**

```
5 + 7 − 1 = 11
```

**Answer: 11.** (Forgetting the `− 1` gives 12, which is the trap option.)

**Second check.** "Rahul is 12th from the top and 30th from the bottom." → `12 + 30 − 1 = 41`
students. Cross-check: `41 − 12 + 1 = 30` ✅.

## Quick rules

- Draw before you place.
- Anchors first, relative clues second.
- `to the left of Y` is relative; `from the left end` is absolute.
- `r + s − 1` for ranks.
- Facing south, the extreme right is seat 1.
- Chains: draw and read.
- "Must" = true in every arrangement.
- 90-second cap.

## Common traps

| Trap | Fix |
|---|---|
| "Second to the left" read as seat 2 | `pos(Y) − 2` |
| Rank without `− 1` | Subtract 1 |
| No south flip | Redraw |
| "Immediately" as "somewhere" | `±1` |
| Assumed uniqueness | Build a second order |
| "Must" read as "could" | Check all orders |

## Checklist

- [ ] I can recite the phrase translation table.
- [ ] I remember `r + s − 1`.
- [ ] I know the north/south flip rule.
- [ ] I draw a slot table every time.
- [ ] I check all valid orders for a "must be true" question.
- [ ] I finished a 10-question ranking drill in under 14 minutes.

## Related

- [Ranking and ordering rules](../01-concepts/01-ranking-ordering-rules.md)
- [Ranking and ordering techniques](../02-techniques/01-ordering-solving-procedures.md)
- [Solved ranking and ordering set](../03-worked-examples/01-solved-ranking-set.md)
- [Ranking and ordering traps](../04-pitfalls/01-ranking-traps.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
