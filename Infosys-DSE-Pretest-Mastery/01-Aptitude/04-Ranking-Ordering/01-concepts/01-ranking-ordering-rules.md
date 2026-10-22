# Ranking and Ordering — The Rules

> Section 1 · Aptitude · Ranking & Ordering · _Estimated reading time: 8 min_
> **Prerequisite:** none

## In one sentence

Ranking and ordering puzzles are **position bookkeeping**: translate every clue into a seat number or a
`<` sign, then fill slots — you never need to guess.

## Why the pre-test tests this

- The DSE pre-test's aptitude section regularly includes **1 ranking/ordering question**, usually a
  row-arrangement puzzle with a "if all turn to face south" twist, or an age/height/rank chain.
- These puzzles look like logic but are arithmetic in disguise. Candidates who try to "reason it out"
  burn 3 minutes; candidates who build a position table finish in 70 seconds.
- The failures are always the same: off-by-one on "second to the left of" versus "second from the
  left", and forgetting that a row facing south reverses left and right.

## Core concept

### The one translation table you must own

| Phrase in the question | What it means | Position rule |
|---|---|---|
| "A is **second to the left of** B" | A is 2 seats left of B | `pos(A) = pos(B) − 2` |
| "A is **second from the left end**" | A is in seat 2 | `pos(A) = 2` |
| "A is **immediately / just to the left of** B" | A is 1 seat left of B | `pos(A) = pos(B) − 1` |
| "A is **immediately to the right of** B" | A is 1 seat right of B | `pos(A) = pos(B) + 1` |
| "A is **somewhere to the left of** B" | A is anywhere left of B | `pos(A) < pos(B)` |
| "A is **third from the right end**" | A is in seat `n − 2` | `pos(A) = n − 2` |
| "A is **at the extreme left / right**" | A is in seat 1 or seat n | `pos(A) = 1` or `n` |

**The trap lives in this table.** "Second to the left of B" and "second from the left end" are
completely different clues, and the exam uses both.

### Chain ordering: taller / older / faster

| Clue | Translation |
|---|---|
| "A is taller than B but shorter than C" | `B < A < C` |
| "A is older than B" | `B < A` (in age) |
| "Ananya scored more than Rahul but less than Meera" | `Rahul < Ananya < Meera` |
| "Karthik is not the fastest" | Karthik is somewhere except first |
| "A is the second oldest" | exactly one person above A |

Two-anchor chains are the whole question. Draw the chain, then answer.

### Rank arithmetic

| Situation | Formula |
|---|---|
| Rank from top `r` and rank from bottom `s` | Total students = `r + s − 1` |
| Rank from top only, total `n` | Rank from bottom = `n − r + 1` |
| Score improves by `k` ranks | New rank = old rank − k |

The `−1` is because the person is counted in both rankings.

### Facing north / facing south

Draw the row on paper with seats 1 … n from **left to right as you see it**.

| Facing | The person at their extreme LEFT is | The person at their extreme RIGHT is |
|---|---|---|
| **North** | seat 1 (paper-left) | seat n (paper-right) |
| **South** | seat n (paper-right) | seat 1 (paper-left) |

So when a row that faced north turns to face south, **the two ends swap from each person's point of
view**. A person at seat 1 was at the extreme left when facing north and is at the extreme right when
facing south.

### Three question shapes you will meet

| Shape | What is asked | What you must produce |
|---|---|---|
| **Position puzzle** | "Who is 4th from the left?" | The complete order |
| **North/south puzzle** | "If they turn, who is at the extreme right?" | The complete order, then the flip |
| **"Must be true"** | "Which statement is always correct?" | Every valid order, then the statement true in all of them |

The third shape is the hardest and the most common. If the clues allow two different orders, a
statement must hold in **both** to be the answer.

## Worked example

**Six friends — Suresh, Karthik, Rahul, Meera, Divya and Ananya — sit in a row of 6 seats facing
north.**

- Suresh is at the extreme left end.
- Karthik is immediately to the right of Suresh.
- Ananya is at the extreme right end.
- Divya is immediately to the left of Ananya.
- Rahul and Meera occupy the two remaining seats, with Rahul to the left of Meera.

**Q. Who sits in the 4th seat from the left?**

A. Rahul
B. Meera
C. Divya
D. Karthik

**Solution — fill slots from the fixed anchors first**

| Seat | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Person | Suresh | Karthik | ? | ? | Divya | Ananya |

Remaining seats 3 and 4 go to Rahul and Meera, and Rahul is to the left of Meera → seat 3 = Rahul,
seat 4 = **Meera**.

**Answer: B (Meera).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| Rahul | He is in seat 3, one place too early — the classic off-by-one |
| Divya | She is in seat 5, immediately left of Ananya |
| Karthik | He is in seat 2, immediately right of Suresh |

**The follow-up the exam loves:** *"If all six turn to face south, who sits at the extreme right
end?"* Facing south, the extreme right is seat 1 → **Suresh**. That is a free mark if you fixed the
order correctly.

## Quick rules

- **Anchor first.** Place anyone at an extreme end or in a fixed seat before using relative clues.
- **Translate, don't reason.** Every clue becomes `pos(X) = pos(Y) ± k` or `pos(X) < pos(Y)`.
- "Second **to the** left of B" = B − 2; "second **from the** left end" = seat 2. Never confuse them.
- Rank from top + rank from bottom **− 1** = total.
- Facing north → their left is your left. Facing south → their left is your right.
- In a "must be true" question, build **every** valid order and pick the statement true in all of
  them.
- If two orders are possible and the options assume one order, you have misread a clue.
- Cap the puzzle at 90 seconds. If you are writing full sentences, draw the slot table instead.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| "second to the left" vs "second from the left" | Off by one on every relative clue | Use the translation table |
| Excluding the person from the rank count | Total = r + s | Always subtract 1 |
| North/south flip | Says the answer "stays the same" | Redraw the row facing south |
| Assuming a unique order | Picks an option that only holds in one arrangement | Build all valid orders |
| "Immediately" ignored | Treats adjacent as "somewhere near" | `±1` vs `<` |
| Counting seats inclusively | "Third from the left" = seat 3 vs seat 2 | Seats are 1-indexed |
| Solving by intuition | 3 minutes gone | Draw the 6-column table |

## Checklist

- [ ] I drew a slot table before placing anyone.
- [ ] I placed all extreme-end and fixed-position people first.
- [ ] I converted every relative clue into `pos ± k`.
- [ ] I checked `r + s − 1` for rank questions.
- [ ] For a north/south question, I redrew the row after the flip.
- [ ] For a "must be true" question, I verified the statement against every valid order.
- [ ] I finished the puzzle inside 90 seconds.

## Related

- [Ranking and ordering techniques](../02-techniques/01-ordering-solving-procedures.md)
- [Solved ranking and ordering set](../03-worked-examples/01-solved-ranking-set.md)
- [Ranking and ordering traps](../04-pitfalls/01-ranking-traps.md)
- [Ranking one-pager](../05-reference/01-ranking-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
