# Ranking and Ordering — Traps and Wrong Turns

> Section 1 · Aptitude · Ranking & Ordering · _Estimated reading time: 6 min_
> **Prerequisite:** [Ranking and ordering techniques](../02-techniques/01-ordering-solving-procedures.md)

## In one sentence

Ranking traps are **translation errors and assumed uniqueness** — you misread one phrase, or you
assume the puzzle has only one solution when it has three.

## Why the pre-test tests this

- Nine out of ten ranking mistakes come from two sentences: one phrase mis-translated, or one
  arrangement assumed when several are possible.
- These puzzles are solvable in 90 seconds once the translation is right, so every lost mark here is
  an avoidable mark.
- Karthik's retrospective point: "the ordering question was the only one I finished in under a minute,
  once I stopped reading it as a story."

## Core concept

### The seven classic wrong turns

| # | Wrong turn | Why it feels right | The fix |
|---|---|---|---|
| 1 | "second **to the** left" → seat 2 | Both phrases start with "second" | `to the left of Y` = Y − 2 |
| 2 | Rank total = `r + s` | You counted the person twice | Always `− 1` |
| 3 | North/south flip ignored | The picture "looks the same" | Redraw the row |
| 4 | "Immediately" read as "somewhere" | The constraint still feels satisfied | `±1`, not `<` |
| 5 | One arrangement assumed | The puzzle "sounds" determined | Build all valid orders |
| 6 | "Must be true" read as "could be true" | The statement *is* sometimes true | It must hold in every order |
| 7 | Prose reasoning, no table | It "made sense" in your head | Draw the slots |

### The five phrase pairs that cause 1 and 4

| Pair | Difference |
|---|---|
| "second to the left of B" vs "second from the left end" | `pos(B) − 2` vs seat `2` |
| "immediately left of B" vs "somewhere left of B" | `pos(B) − 1` vs anything `< pos(B)` |
| "third from the right end" vs "third to the right of B" | seat `n − 2` vs `pos(B) + 3` |
| "between A and B" | Adjacent to both, or anywhere between — check the clue wording |
| "not immediately left of B" | Any seat except `pos(B) − 1` |

### The uniqueness test

Before you pick an answer to a "must be true" question, ask: **can I write down a second valid
arrangement?**

If yes, and the option is not true in both, the option is wrong. If you cannot write a second
arrangement, the arrangement is unique and you just read it off.

| You can build | You can build | An option that holds in only one | An option that holds in both |
|---|---|---|---|
| ✔ | ✔ | not the answer | the answer |
| ✔ | ✘ | — | the answer (unique arrangement) |

## Worked example

**Six friends — Suresh, Karthik, Rahul, Meera, Divya and Ananya — sit in a row of 6 seats facing
north.**

- Suresh is at the extreme left end.
- Karthik is immediately to the right of Suresh.
- Ananya is at the extreme right end.
- Divya is immediately to the left of Ananya.
- Rahul and Meera occupy the two remaining seats, with Rahul to the left of Meera.

**Q. If all six turn to face south, who sits at the extreme right end?**

A. Suresh
B. Karthik
C. Rahul
D. Ananya

**The wrong turns visible in the options**

| Option | Wrong turn it represents |
|---|---|
| D. Ananya | Ignoring the flip — she *was* the extreme right when facing north |
| B. Karthik | Off-by-one — assuming the "next" person becomes the extreme right |
| C. Rahul | Picking the middle-ish name without doing the flip |
| A. Suresh | Correct |

**The right reasoning**

```
Facing NORTH (as drawn):   [Suresh][Karthik][Rahul][Meera][Divya][Ananya]
                             seat 1                              seat 6
Facing SOUTH (their view):   their LEFT  = seat 6   ...   their RIGHT = seat 1
```

When they turn around, seat 1 (Suresh) becomes their extreme right.

**Answer: A (Suresh).**

**Second example — the phrase trap.**

**Q. Five friends — Meera, Rahul, Karthik, Divya and Ananya — sit in a row of 5 seats facing north.
Karthik sits at the extreme left end, and Meera sits second to the left of Rahul. Who sits
immediately to the right of Karthik?**

A. Divya
B. Meera
C. Rahul
D. Cannot be determined

**Solution**: Karthik = seat 1. "Second **to the** left of Rahul" means `pos(Meera) = pos(Rahul) − 2`
— a **relationship**, not a fixed seat. Two arrangements fit the clues:

| Arrangement | Seat 1 | Seat 2 | Seat 3 | Seat 4 | Seat 5 |
|---|---|---|---|---|---|
| Possible 1 | Karthik | Meera | Divya | Rahul | Ananya |
| Possible 2 | Karthik | Divya | Meera | Ananya | Rahul |

In arrangement 1 the person immediately right of Karthik is Meera; in arrangement 2 it is Divya.
No option is forced, so the answer is **D (cannot be determined)**.

**Why this matters:** the exam's favourite ranking trap is a phrase like "second to the left of"
translated by the candidate as "second from the left". The first is relational; the second is
absolute. If a question gives you one relational clue and one absolute clue, check whether the
arrangement is really unique.

## Quick rules

- Translate every phrase before you place anyone.
- `to the left of Y` = relative; `from the left end` = absolute.
- Rank totals always use `− 1`.
- Flip the row for south; do not imagine it.
- "Immediately" means adjacent, one seat.
- Build a second arrangement before believing an option must be true.
- Use a table; 60 seconds of drawing beats 3 minutes of prose.

## Common traps

| Trap | Wrong answer | Right answer |
|---|---|---|
| "Second to the left" read as seat 2 | Off by one | `pos(Y) − 2` |
| Rank without `− 1` | 12 for r=5, s=7 | 11 |
| No south flip | Ananya | Suresh |
| "Immediately" → "somewhere" | Wrong neighbour | Adjacent only |
| Assumed uniqueness | Option true in one arrangement only | Check all orders |
| "Must" read as "could" | A possible-but-not-forced option | The forced one |

## Checklist

- [ ] I translated every clue into a position equation before placing anyone.
- [ ] I checked "to the left of" vs "from the left end".
- [ ] I used `r + s − 1` for rank totals.
- [ ] I redrew the row for any north/south question.
- [ ] I tried to build a second arrangement for a "must be true" question.
- [ ] I finished each puzzle inside 90 seconds.

## Related

- [Ranking and ordering rules](../01-concepts/01-ranking-ordering-rules.md)
- [Ranking and ordering techniques](../02-techniques/01-ordering-solving-procedures.md)
- [Solved ranking and ordering set](../03-worked-examples/01-solved-ranking-set.md)
- [Ranking one-pager](../05-reference/01-ranking-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
