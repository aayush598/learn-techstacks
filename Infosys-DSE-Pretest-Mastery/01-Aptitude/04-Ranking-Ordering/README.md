# Ranking and Ordering — Topic Guide

> Section 1 · Aptitude · Ranking & Ordering · _Estimated reading time: 30 min for the full topic_

## What the pre-test asks in this topic

The DSE pre-test's aptitude section typically includes **1 ranking/ordering question** in one of three
shapes:

1. **Row arrangement** — "Five friends sit in a row. A is at the extreme left, B is immediately to the
   right of A… Who sits fourth from the left?"
2. **North/south flip** — the same arrangement, then "if they all turn to face south, who is at the
   extreme right end?"
3. **Ordering chain** — "Meera is taller than Karthik, Ananya is taller than Meera but shorter than
   Divya. Who is the tallest?" or a rank-from-top/bottom problem.

The question may also be framed as "which of the following must be true?", where the arrangement is
not fully determined and you must find what holds in every valid order.

## Learning objectives

After this topic you should be able to:

- Translate **every** arrangement phrase into a position equation: `pos(X) = pos(Y) ± k`.
- Tell apart "second **to the** left of Y" (relative) and "second **from the** left end" (absolute).
- Fill a slot table in a fixed order: anchors first, relative clues second, leftovers last.
- Solve chain questions (taller, older, faster, richer) by drawing the `<` chain.
- Compute total candidates from two ranks with `r + s − 1`, and cross-check it.
- Compute a rank change (`10 ranks below`) and count candidates below a rank.
- Flip a north-facing row to south correctly and identify the new extreme right and left.
- Use the **all-valid-orders test** to answer "must be true" questions.
- Finish a ranking question in **90 seconds** with a pen-drawn table.

## File index

| File | Lines | What it gives you |
|---|---|---|
| [01-concepts/01-ranking-ordering-rules.md](01-concepts/01-ranking-ordering-rules.md) | 166 | Phrase translation table, chain rules, rank arithmetic, the north/south table, three question shapes |
| [02-techniques/01-ordering-solving-procedures.md](02-techniques/01-ordering-solving-procedures.md) | 173 | Five procedures: slot table, chain diagram, rank arithmetic, north/south flip, all-orders test |
| [03-worked-examples/01-solved-ranking-set.md](03-worked-examples/01-solved-ranking-set.md) | 371 | 10 fully solved questions: position, flip, chain, ranks, race, ages, ratio, money |
| [04-pitfalls/01-ranking-traps.md](04-pitfalls/01-ranking-traps.md) | 161 | 7 wrong turns with the option each one produces, plus the phrase-pair table |
| [05-reference/01-ranking-one-pager.md](05-reference/01-ranking-one-pager.md) | 138 | Phrase table, rank formulas, flip table, slot template, 90-second budget |

## Quick 3-step solving procedure

1. **Draw the slot table** (10 s). Number the seats and write the names into a header row.
2. **Place the anchors** (15 s). Extreme ends and fixed seats first. Then apply each relative clue as
   `pos ± k`.
3. **Fill, verify, answer** (60 s). Place the leftovers, re-read each clue once to confirm, then
   answer the actual question — including the north/south flip if asked.

## Key takeaways

- ✅ **Translate, don't reason.** Every clue is a position equation.
- ✅ **Anchors first.** Extreme ends and fixed seats reduce the puzzle fastest.
- ✅ **`r + s − 1`** for ranks — the person is counted in both rankings.
- ✅ **North vs south flips the ends** from the people's point of view.
- ✅ **"Must be true" means true in every valid order** — try to build a second arrangement.
- ✅ **Chains are one line:** draw `<` and read the answer off.
- ✅ **A table beats prose.** 60 seconds of drawing replaces 3 minutes of thinking.
- ⚠️ **Meera's warning:** she re-reads every clue and never writes a seat number. She finishes the
  puzzle at 3 minutes with an answer she cannot verify.

## Related

- [Aptitude section index](../README.md)
- [Inequalities & Relations](../05-Inequalities-Relations/README.md) — the sibling archetype: chains of
  symbols instead of seats
- [Number Series](../06-Number-Series/README.md) — the other pattern-recognition archetype
- [Question Bank](../09-Question-Bank/README.md) — timed ranking drills
- [Master README](../../README.md)
