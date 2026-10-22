# Ranking and Ordering — Solving Procedures

> Section 1 · Aptitude · Ranking & Ordering · _Estimated reading time: 7 min_
> **Prerequisite:** [Ranking and ordering rules](../01-concepts/01-ranking-ordering-rules.md)

## In one sentence

Use one of three procedures — **slot table**, **chain diagram** or **rank arithmetic** — and never
rely on prose reasoning to "figure it out".

## Why the pre-test tests this

- The puzzle looks like logic and behaves like arithmetic. Pros who are fast with positions are
  disproportionately good at this archetype.
- Meera's failure mode is prose: she re-reads each clue three times and never draws anything.
- A slot table converts six sentences into six numbers, which is what the 90-second rule needs.

## Core concept

### Procedure 1 — the slot table (for row arrangements)

```
Clues → anchor → translate → fill → verify
```

| Step | Action | Time |
|---|---|---|
| 1 | Write the number of seats `n` and draw `n` empty slots | 10 s |
| 2 | Place everyone pinned to an extreme end or a fixed seat | 15 s |
| 3 | Convert each relative clue into `pos ± k` and place it | 30 s |
| 4 | Place the leftovers using the "somewhere to the left/right" clues | 10 s |
| 5 | Re-read the clues once and confirm every one still holds | 15 s |
| 6 | Answer the actual question (position, flip, or "must be true") | 10 s |

### Procedure 2 — the chain diagram (for taller / older / faster)

Draw the chain left to right with the signs:

```
Rahul < Ananya < Meera < Karthik
```

Then the question is a reading task:

| Question | Answer from the chain |
|---|---|
| Who is the tallest / oldest? | Right end |
| Who is the shortest / youngest? | Left end |
| Who is second from the right? | The one before the last |
| How many are taller than X? | Count everything to the right of X |

### Procedure 3 — rank arithmetic

```
total = rank from top + rank from bottom − 1
rank from bottom = total − rank from top + 1
```

Worked example: "Rahul ranked 12th from the top and 30th from the bottom in a class."
`12 + 30 − 1 = 41` students. Rahul's rank from the bottom is also `41 − 12 + 1 = 30` ✅ — the
cross-check that catches a misread.

### Procedure 4 — the north/south flip

After the order is fixed, draw the row twice:

```
Facing NORTH:      [1][2][3][4][5][6]
Their left  →  seat 1        Their right → seat 6

Facing SOUTH:      [6][5][4][3][2][1]   (from their point of view)
Their left  →  seat 6        Their right → seat 1
```

So the extreme-right person when facing south is **the person who was at seat 1**.

### Procedure 5 — "must be true" with multiple valid orders

1. Build the arrangement.
2. If the clues force a unique order, there is exactly one order — test each option against it.
3. If more than one order is possible, list the free slots and see what is fixed in **all** orders.
4. An option is the answer only if it holds in every valid order.

| Option type | Verdict |
|---|---|
| "P sits at the extreme right end" | Must be checked against all orders |
| "Q sits to the immediate left of P" | Often forced by the clues |
| "R sits at the extreme left end" | Only if no order allows otherwise |
| "S and T sit next to each other" | Needs all orders checked |

## Worked example

**Seven friends — Meera, Rahul, Ananya, Karthik, Divya, Suresh and Vinay — sit in a row of 7 seats
facing north.**

- Meera is at the extreme left end.
- Rahul is third from the right end.
- Ananya sits immediately to the right of Rahul.
- Karthik, Divya, Suresh and Vinay occupy the remaining seats in no fixed order.

**Q. Which of the following must be true?**

A. Divya sits at the extreme right end.
B. Meera sits at the extreme left end.
C. Suresh sits immediately to the left of Rahul.
D. Ananya sits at the extreme right end.

**Solution**

| Seat | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Person | Meera | ? | ? | ? | Rahul | Ananya | ? |

- **B** is given directly by the first clue → true in every order. ✅
- **A**: Divya *could* be in seat 7, but she could also be in seat 2, 3 or 4 → not always true.
- **C**: Suresh *could* be in seat 4 (immediately left of Rahul), but he could also be in seat 2, 3 or
  7 → not always true.
- **D**: Ananya is in seat 6, and the extreme right is seat 7 → **always false**.

**Answer: B.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | Possible but not forced — 3 of the 4 free seats also work |
| C | Possible but not forced — same reason |
| D | Ananya is pinned to seat 6; seat 7 is free |

**Key insight:** "must be true" asks for what is **forced**, and only one option was given in the
clues. Most candidates pick C because it "sounds" like a puzzle answer.

## Quick rules

- Draw the slot table before you read the clues twice.
- Anchors first (extreme ends, fixed seats), then relative clues.
- `pos(X) = pos(Y) ± k` for every relative clue.
- Chain questions: draw the `<` chain and read off the answer.
- Rank questions: `r + s − 1`, then cross-check.
- North/south: redraw the row; the extreme right becomes seat 1.
- "Must be true" = true in **every** valid order.
- 90-second cap.

## Common traps

| Trap | Effect | Fix |
|---|---|---|
| Prose reasoning instead of a table | 3 minutes | Draw slots |
| Placing relative clues before anchors | Fewer free slots resolved | Anchor first |
| "Second to the left of" read as "second from the left" | Off by one | Translation table |
| Rank without the `−1` | Total off by one | `r + s − 1` |
| North/south flip skipped | Ends not swapped | Redraw the row |
| "Must be true" read as "could be true" | Wrong option | Check all orders |

## Checklist

- [ ] I drew the slot table first.
- [ ] I placed the anchors before the relative clues.
- [ ] I converted every clue into a position equation.
- [ ] I verified the finished arrangement against every clue.
- [ ] For a flip question, I redrew the row facing south.
- [ ] For a "must be true" question, I checked all valid orders.
- [ ] I finished inside 90 seconds.

## Related

- [Ranking and ordering rules](../01-concepts/01-ranking-ordering-rules.md)
- [Solved ranking and ordering set](../03-worked-examples/01-solved-ranking-set.md)
- [Ranking and ordering traps](../04-pitfalls/01-ranking-traps.md)
- [Ranking one-pager](../05-reference/01-ranking-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
