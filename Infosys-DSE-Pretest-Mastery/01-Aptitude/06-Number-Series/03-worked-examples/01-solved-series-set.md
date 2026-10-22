# Number Series — 10 Solved Questions

> Section 1 · Aptitude · Number Series · _Estimated reading time: 13 min_
> **Prerequisite:** [Series solving techniques](../02-techniques/01-series-solving-techniques.md)

## In one sentence

Ten series, ten different pattern families — each solved by writing the differences first and then
extending the rule by exactly one step.

## Why the pre-test tests this

- Series questions are 1–2 of the 10 aptitude questions and are worth banking.
- The set below covers every family: arithmetic, geometric, difference-of-difference, squares, cubes,
  Fibonacci, alternating operations, prime-based, digit-based, plus the **wrong-term** format.
- The correct answers are spread across four option positions on purpose.

## Core concept

The habit that separates a 70-second series from a 3-minute series:

> **Write the difference row. Extend one step. Match to an option. If it does not match, your family
> is wrong — do not extend further.**

## Worked example

### Q1 — Answer **B** (geometric)

**What comes next: 3, 6, 12, 24, ?**

A. 36
B. 48
C. 42
D. 50

**Solution**: Ratios are 2, 2, 2 → `× 2` → 24 × 2 = **48**.

**Answer: B (48).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 36 | Added 12 (the previous difference) instead of multiplying |
| 42 | 24 + 18 — an arbitrary add |
| 50 | Added 26 |

---

### Q2 — Answer **C** (wrong term, n(n+1))

**Find the wrong term: 2, 6, 12, 20, 30, 44, 56**

A. 20
B. 30
C. 44
D. 56

**Solution**: Differences are 4, 6, 8, 10, **14**, 12 — should be 4, 6, 8, 10, 12, 14.
The series is `n(n+1)`: 2, 6, 12, 20, 30, **42**, 56. So 44 is wrong.

**Answer: C (44).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 20 | Correct term (4 × 5) |
| 30 | Correct term (5 × 6) |
| 56 | Correct term (7 × 8) |

---

### Q3 — Answer **A** (Fibonacci-like, missing middle)

**Find the missing term: 1, 1, 2, 3, 5, ?, 13**

A. 8
B. 6
C. 7
D. 9

**Solution**: Each term = sum of the previous two: 5 + ? = 13 → ? = **8**. Check: 3 + 5 = 8 ✅ and
1 + 2 = 3, 2 + 3 = 5.

**Answer: A (8).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 6 | 1 + 5 — used the wrong pair |
| 7 | 2 + 5 — used the wrong pair |
| 9 | 4 + 5 — a term that does not exist in the series |

---

### Q4 — Answer **D** (squares, missing middle)

**Find the missing term: 1, 4, 9, 16, ?, 36**

A. 20
B. 24
C. 26
D. 25

**Solution**: 1², 2², 3², 4², **5²**, 6² → **25**.

**Answer: D (25).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 20 | 4 × 5 — the pronic family, not squares |
| 24 | 4² + 8, or the average of 16 and 36 |
| 26 | 16 + 10 — extending by 10 |

---

### Q5 — Answer **C** (cubes)

**What comes next: 1, 8, 27, 64, 125, ?**

A. 144
B. 150
C. 216
D. 215

**Solution**: 1³, 2³, 3³, 4³, 5³, **6³ = 216**.

**Answer: C (216).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 144 | 12² — confused squares with cubes |
| 150 | 125 + 25 — added the previous square |
| 215 | 216 − 1 — an off-by-one on the cube |

---

### Q6 — Answer **B** (difference of difference)

**Find the missing term: 2, 5, 10, 17, 26, ?, 50**

A. 35
B. 37
C. 38
D. 39

**Solution**

```
Terms:   2    5   10   17   26   ?   50
Diffs:      3    5    7    9   ?    ?
2nd:          2    2    2    ?    ?
```

Second differences are constant at 2, so the differences run 3, 5, 7, 9, 11, 13.
Missing term = 26 + 11 = **37**. Check: 37 + 13 = 50 ✅

**Answer: B (37).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 35 | Added the previous difference (9) instead of the next one (11) |
| 38 | Added 12 — a second-difference error |
| 39 | Added 13 — used the difference *after* the missing term |

---

### Q7 — Answer **A** (alternating operations)

**What comes next: 5, 20, 19, 76, 75, ?**

A. 300
B. 299
C. 74
D. 76

**Solution**: `×4, −1, ×4, −1` → 75 × 4 = **300**.

**Answer: A (300).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 299 | 75 × 4 − 1 — two operations in one step |
| 74 | Applied the −1 step twice |
| 76 | Repeated the previous value |

---

### Q8 — Answer **B** (squares of primes)

**What comes next: 4, 9, 25, 49, 121, ?**

A. 144
B. 169
C. 196
D. 121

**Solution**: 2², 3², 5², 7², 11², **13² = 169**.

**Answer: B (169).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 144 | 12² — 12 is not prime |
| 196 | 14² — 14 is not prime |
| 121 | Repeated 11² |

---

### Q9 — Answer **B** (digit-based)

**What comes next: 19, 28, 37, 46, ?**

A. 54
B. 55
C. 56
D. 64

**Solution**: Each term is the previous term plus 9 → 46 + 9 = **55**.

**Answer: B (55).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 54 | Added 8 — the last digit repeated instead of incrementing |
| 56 | Added 10 — repeated the tens digit |
| 64 | Reversed the digits |

**Cross-check with the digit-sum rule**: 1+9 = 10, 2+8 = 10, 3+7 = 10, 4+6 = 10, so the next term
also needs digit sum 10 — 55 ✅ (54 sums to 9, 56 sums to 11).

---

### Q10 — Answer **C** (wrong term, geometric)

**Find the wrong term: 3, 9, 27, 81, 243, 730, 729**

A. 243
B. 729
C. 730
D. 81

**Solution**: The pattern is `× 3`: 3, 9, 27, 81, 243, **729**, 2187. The 6th term should be 729, but
it is printed as 730.

**Answer: C (730).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 243 | Correct term (3⁵) |
| 729 | Correct term (3⁶) — it belongs in position 6 |
| 81 | Correct term (3⁴) |

## Quick rules

- Write the difference row; then the ratio row.
- Constant differences → arithmetic. Constant ratios → geometric.
- Constant second differences → extend the difference, then the term.
- Two interleaved rules → split odd and even positions.
- Squares, cubes, n(n+1) and primes of primes are memorised, not derived.
- Digit sums constant → digit-based rule.
- Extend one step only; if it does not match an option, the family is wrong.
- Wrong-term questions: find the rule, compute the correct value, the printed term is the answer.
- 70-second cap.

## Common traps

| Trap | Seen in | Silently gives |
|---|---|---|
| Adding instead of multiplying | Q1 | 36 |
| Picking the "odd-looking" term | Q2 | 20 or 30 |
| Wrong Fibonacci pair | Q3 | 6 or 7 |
| Pronic family instead of squares | Q4 | 20 |
| Squares instead of cubes | Q5 | 144 |
| Using the difference after the gap | Q6 | 39 |
| Two operations in one step | Q7 | 299 |
| Non-prime base | Q8 | 144 |
| Digit carry error | Q9 | 54 or 56 |
| Fixing the rule instead of the term | Q10 | 729 |

## Checklist

- [ ] I wrote the difference row for every series.
- [ ] I extended only one step each time.
- [ ] I got Q2 and Q10 right — wrong-term questions are the ones that cost marks.
- [ ] I finished all 10 in 13 minutes or less.

## Related

- [Number series pattern families](../01-concepts/01-series-pattern-types.md)
- [Series solving techniques](../02-techniques/01-series-solving-techniques.md)
- [Series traps](../04-pitfalls/01-series-traps.md)
- [Pattern catalogue](../05-reference/01-series-pattern-catalogue.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
