# Ranking and Ordering — 10 Solved Questions

> Section 1 · Aptitude · Ranking & Ordering · _Estimated reading time: 14 min_
> **Prerequisite:** [Ranking and ordering techniques](../02-techniques/01-ordering-solving-procedures.md)

## In one sentence

Ten puzzles across row arrangements, north/south flips, height chains, rank arithmetic and
"must be true" — every one solved by **positions, not prose**.

## Why the pre-test tests this

- Ranking/ordering is 1 of the 10 aptitude questions, and it is the one most often abandoned on time.
- The set below deliberately includes the two variants that cost marks: the "second **to the** left"
  phrasing and the north/south flip.
- Work through this set with a pen and a slot table. Practice without drawing the table is practice
  without the skill.

## Core concept

The three tools you will use again and again:

| Tool | Use it for | The rule |
|---|---|---|
| **Slot table** | Row arrangements | Anchor first, then `pos ± k` |
| **Chain** | Taller / older / faster | Draw `<` and read off |
| **Rank arithmetic** | Rank from top and bottom | `total = r + s − 1` |

## Worked example

### Q1 — Answer **B** (row arrangement, position question)

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

**Solution**

| Seat | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Person | Suresh | Karthik | ? | ? | Divya | Ananya |

Seats 3 and 4 belong to Rahul and Meera; Rahul is left of Meera → seat 3 = Rahul, seat 4 = **Meera**.

**Answer: B (Meera).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| Rahul | He is in seat 3 — the classic off-by-one |
| Divya | She is in seat 5 |
| Karthik | He is in seat 2 |

---

### Q2 — Answer **A** (north/south flip)

**Using the same arrangement in Q1: if all six turn to face south, who sits at the extreme right
end?**

A. Suresh
B. Karthik
C. Rahul
D. Ananya

**Solution**: Facing north, their left is your left, so seat 1 is the extreme left. Facing south, their
left is your right, so seat 1 becomes the extreme **right**.

Seat 1 = Suresh.

**Answer: A (Suresh).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| Karthik | Seat 2 — a near miss, and the most common wrong pick |
| Rahul | Seat 3 |
| Ananya | Seat 6 — she was the extreme right when facing north, which is exactly the trap |

---

### Q3 — Answer **A** (height chain)

**Five friends — Ananya, Rahul, Meera, Karthik and Divya — are arranged from shortest to tallest.**

- Meera is taller than Karthik.
- Ananya is taller than Meera but shorter than Divya.
- Rahul is shorter than Karthik.

**Q. Who is the tallest?**

A. Divya
B. Ananya
C. Meera
D. Karthik

**Solution**

```
Rahul < Karthik < Meera < Ananya < Divya
```

**Answer: A (Divya).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| Ananya | Taller than Meera, but Divya is taller than Ananya |
| Meera | Third in the chain |
| Karthik | Second in the chain |

---

### Q4 — Answer **B** (rank from top and bottom)

**Ananya scored 5th highest and 7th lowest among all participants in a coding test. How many
participants were there in all?**

A. 10
B. 11
C. 12
D. 13

**Solution**: `total = 5 + 7 − 1 = 11`.

**Answer: B (11).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 10 | Forgot the `−1` — you counted Ananya twice |
| 12 | Added 1 instead of subtracting it |
| 13 | Added the two ranks and then added 1 more |

---

### Q5 — Answer **A** (rank shift, then count below)

**In an exam of 800 candidates, Meera ranked 45th from the top. Karthik ranked 10 ranks below Meera.
How many candidates ranked below Karthik?**

A. 745
B. 755
C. 764
D. 800

**Solution**

```
Karthik's rank = 45 + 10 = 55th
Below Karthik    = 800 − 55 = 745
```

**Answer: A (745).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 755 | Used 45 instead of 55: 800 − 45 |
| 764 | Used a rank of 36: 800 − 36 |
| 800 | The whole candidate list — no one is below the last rank |

---

### Q6 — Answer **A** (ordering by finish)

**In a race, Meera finished before Ananya, and Ananya finished before Rahul. Karthik finished after
Rahul, and Divya finished last. Who finished first?**

A. Meera
B. Ananya
C. Divya
D. Karthik

**Solution**

```
Meera < Ananya < Rahul < Karthik < Divya (last)
```

Divya is last, so the remaining four fill the first four places in that order.

**Answer: A (Meera).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| Ananya | Second |
| Divya | Explicitly last |
| Karthik | Fourth |

---

### Q7 — Answer **A** (age chain with an average)

**Rahul is 3 years older than Meera, and Meera is 3 years older than Ananya. The average age of the
three is 21 years. What is Ananya's age?**

A. 18 years
B. 21 years
C. 24 years
D. 20 years

**Solution**: Let Ananya = `x`. Then Meera = `x + 3`, Rahul = `x + 6`.
`x + x + 3 + x + 6 = 63` → `3x = 54` → `x = 18`.

**Answer: A (18 years).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 21 years | Meera's age — the middle of the chain equals the average here |
| 24 years | Rahul's age |
| 20 years | A guess that ignores the 3-year gaps |

---

### Q8 — Answer **B** ("must be true")

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

- **B** is stated in the first clue → true in every arrangement. ✅
- **A**: Divya could be in seat 7, 2, 3 or 4 → not forced.
- **C**: Suresh could be in seat 4, but could equally be in 2, 3 or 7 → not forced.
- **D**: Ananya is pinned to seat 6, so she is never at the extreme right → always false.

**Answer: B.**

**Distractors**

| Option | Why it is wrong |
|---|---|
| A | Possible, not forced — three other seats also work |
| C | Possible, not forced — same reason |
| D | Always false: Ananya is in seat 6 |

---

### Q9 — Answer **A** (ages in a ratio)

**The ages of Ananya, Rahul and Meera are in the ratio 3 : 4 : 5, and the average age of the three is
24 years. What is the difference between the ages of Meera and Rahul?**

A. 6 years
B. 4 years
C. 8 years
D. 12 years

**Solution**

```
Total = 3 × 24 = 72   (3 × 24 = sum of the three ages)
Parts = 3 + 4 + 5 = 12  →  1 part = 6
Ages = 18, 24, 30
Difference (Meera − Rahul) = 30 − 24 = 6
```

**Answer: A (6 years).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 4 years | The raw difference between the ratio numbers (5 − 4 = 1... times something wrong) |
| 8 years | Meera − Ananya would be 12; 8 comes from 30 − 22 |
| 12 years | Meera − Ananya = 30 − 18 = 12 — the wrong pair of people |

---

### Q10 — Answer **A** (money chain)

**Rahul has more money than Meera but less than Ananya. Karthik has less money than Meera. Who has the
least money?**

A. Karthik
B. Meera
C. Rahul
D. Ananya

**Solution**

```
Karthik < Meera < Rahul < Ananya
```

**Answer: A (Karthik).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| Meera | Second from the bottom |
| Rahul | Third |
| Ananya | The most money |

## Quick rules

- Draw the slot table; fill anchors first.
- `pos(X) = pos(Y) ± k` for every relative clue.
- "Second **to the** left of Y" = Y − 2; "second **from the** left end" = seat 2.
- Rank from top + rank from bottom − 1 = total.
- Facing south, the extreme right is the person who was at seat 1.
- Chain questions: draw the `<` chain.
- "Must be true" = true in every valid order; "could be true" = true in at least one.
- 90-second cap per puzzle.

## Common traps

| Trap | Seen in | Silently gives |
|---|---|---|
| Off-by-one on the seat | Q1 | Rahul |
| Not flipping for south | Q2 | Ananya |
| Missing the `−1` in ranks | Q4 | 10 |
| Rank arithmetic before the shift | Q5 | 755 |
| Reading "must" as "could" | Q8 | A or C |
| Comparing the wrong pair of ages | Q9 | 12 years |

## Checklist

- [ ] I drew a slot table for every arrangement question.
- [ ] I answered Q2 (north/south) and Q8 (must be true) correctly.
- [ ] I finished all 10 in 14 minutes or less.
- [ ] For each wrong answer, I can name the specific clue I mis-translated.

## Related

- [Ranking and ordering rules](../01-concepts/01-ranking-ordering-rules.md)
- [Ranking and ordering techniques](../02-techniques/01-ordering-solving-procedures.md)
- [Ranking and ordering traps](../04-pitfalls/01-ranking-traps.md)
- [Ranking one-pager](../05-reference/01-ranking-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
