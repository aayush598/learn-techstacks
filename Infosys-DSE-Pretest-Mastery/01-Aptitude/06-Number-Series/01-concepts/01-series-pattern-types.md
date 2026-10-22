# Number Series — The Pattern Families

> Section 1 · Aptitude · Number Series · _Estimated reading time: 8 min_
> **Prerequisite:** none

## In one sentence

A number series question is a **pattern-recognition** question: identify which of a small number of
pattern families the series uses, then extend it by one step.

## Why the pre-test tests this

- The DSE pre-test's aptitude section regularly includes **1–2 number-series questions**: usually
  "find the next number" and sometimes "find the wrong term".
- The arithmetic is trivial. The marks are for pattern recognition — and for not burning three
  minutes on a series you have not cracked.
- The set of patterns that actually appear in these papers is small. Learn the families, not infinite
  series.

## Core concept

### The eight pattern families

| # | Family | Shape | Example |
|---|---|---|---|
| 1 | **Arithmetic** | Constant difference | 3, 7, 11, 15, **19** (+4) |
| 2 | **Geometric** | Constant ratio | 3, 6, 12, 24, **48** (×2) |
| 3 | **Difference of difference** | Differences themselves form an AP | 2, 5, 10, 17, 26 (diffs 3,5,7,9) |
| 4 | **Square / cube** | n², n³, n(n+1) | 1, 4, 9, 16, **25** (n²) |
| 5 | **Fibonacci-like** | Each term = sum of two before | 1, 1, 2, 3, 5, **8** |
| 6 | **Alternating operations** | Two operations alternate | 5, 20, 19, 76, 75, **300** (×4, −1) |
| 7 | **Prime-based** | Primes, or squares of primes | 4, 9, 25, 49, 121, **169** |
| 8 | **Digit-based** | Digits themselves follow a rule | 19, 28, 37, 46, **55** (+9) |

### The three question types

| Type | Stem | What you must do |
|---|---|---|
| **Next number** | "… , ?, what comes next?" | Extend the rule by one step |
| **Missing middle term** | "…, ?, …" in the middle | Rebuild the rule and fill the gap |
| **Wrong term** | "Which term is wrong?" | Find the rule, then find the term that breaks it |

The wrong-term type is the reverse of the other two: the rule is present but **one term breaks it**, so
you must locate the break.

### Family 3 in detail — the difference table

Build the difference table before you guess:

```
Terms:      2    5   10   17   26   37
Diffs:        3    5    7    9   11
2nd diffs:      2    2    2    2
```

A constant second difference means a quadratic sequence: add 3, 5, 7, 9, 11…

| Second difference | Pattern |
|---|---|
| Constant | Quadratic — add increasing odd/even steps |
| Constant at the second level | Cubic — differences of differences of differences constant |
| All zeros | Arithmetic |
| Varying | Something else — go back to the ratio check |

### Family 6 in detail — alternating operations

Two operations alternate. Split the series into **odd-position** and **even-position** terms:

```
5, 20, 19, 76, 75, ?
│   │   │   │   │   └── next
×4  −1  ×4  −1  ×4
```

Odd positions: 5, 19, 75 (×4, −1, ×4). Even positions: 20, 76, … (×4, −1). Either view gives the
answer: 75 × 4 = 300.

### Family 8 in detail — digit-based rules

| Rule | Example | Next |
|---|---|---|
| Constant increment | 19, 28, 37, 46 | 55 |
| Digit sum constant | 47, 56, 65, 74 | 83 (sum always 11) |
| Digit reversal alternation | 12, 21, 13, 31 | 14 |
| One digit fixed, one incrementing | 12, 23, 34, 45 | 56 |

Check the **digit sum** when the increments look irregular: 47 → 4+7 = 11, 56 → 11, 65 → 11, 74 → 11.
That is a much stronger signal than "the numbers increase".

### Recognising squares and cubes fast

| Square | Value | Cube | Value |
|---|---|---|---|
| 1² | 1 | 2³ | 8 |
| 2² | 4 | 3³ | 27 |
| 3² | 9 | 4³ | 64 |
| 4² | 16 | 5³ | 125 |
| 5² | 25 | 6³ | 216 |
| 6² | 36 | 7³ | 343 |
| 7² | 49 | 8³ | 512 |
| 8² | 64 | 9³ | 729 |
| 9² | 81 | 10³ | 1000 |

Also useful: `n(n+1)` = 2, 6, 12, 20, 30, 42, 56 and `n(n−1)` = 0, 2, 6, 12, 20, 30.

## Worked example

**Q. Find the wrong term in the series: 2, 6, 12, 20, 30, 44, 56**

A. 20
B. 30
C. 44
D. 56

**Solution**

- Check the shape: differences are 4, 6, 8, 10, 14, 12. The differences should be consecutive even
  numbers: 4, 6, 8, 10, 12, 14.
- The differences break at the 5th difference: from 30 to 44 is **+14**, but it should be **+12**;
  from 44 to 56 is +12, but it should be +14. The series is `n(n+1)`: 1×2, 2×3, 3×4, 4×5, 5×6, 6×7,
  7×8 → 2, 6, 12, 20, 30, **42**, 56.
- So the wrong term is **44**.

**Answer: C (44).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 20 | Fits `n(n+1)` exactly (4 × 5) |
| 30 | Fits exactly (5 × 6) |
| 56 | Fits exactly (7 × 8) |

**Second check.** Replace 44 with 42: differences become 4, 6, 8, 10, 12, 14 — clean. ✅

## Quick rules

- **Build the difference table first.** One column of differences reveals more than ten seconds of
  guessing.
- If the ratio of consecutive terms is constant → geometric. If the difference is constant →
  arithmetic.
- Second differences constant → the differences form an AP. Extend the difference, then the term.
- Two operations alternating → split the series into odd and even positions.
- Squares and cubes: check the last two or three terms against the table.
- Digit sums constant → digit-based rule.
- For "wrong term": find the rule **first**, then find the break. Never just pick the odd-looking
  term.
- Cap at 70 seconds. If the rule has not appeared by then, mark the most plausible option and move.
  One series question is 1 mark; the next two are worth more.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| Continuing the last difference blindly | The 5th difference is wrong | Check the whole difference row |
| Arithmetic when it is geometric | Adding a constant that does not fit | Check the ratio too |
| Missing interleaved sequences | One rule fits half the terms | Split odd/even positions |
| Forcing a pattern | You jump from 2 differences to 3 | Try the standard families in order |
| Picking the odd-looking term | The wrong term is not always the "ugly" one | Find the rule first |
| Squares confused with cubes | 27 treated as 3³ when the pattern is squares | Check two terms, not one |
| Fibonacci off by one | You add the wrong pair | term(n) = term(n−1) + term(n−2) |
| Sinking 4 minutes | You are still writing numbers at the 3-minute mark | 70-second cap |

## Checklist

- [ ] I wrote the difference row before guessing.
- [ ] I checked the ratio row for a geometric pattern.
- [ ] I tried odd/even position splitting when a single rule did not fit.
- [ ] I identified the family before extending the series.
- [ ] For a wrong-term question, I found the rule before choosing.
- [ ] I finished inside 70 seconds.

## Related

- [Series solving techniques](../02-techniques/01-series-solving-techniques.md)
- [Solved number-series set](../03-worked-examples/01-solved-series-set.md)
- [Series traps](../04-pitfalls/01-series-traps.md)
- [Pattern catalogue](../05-reference/01-series-pattern-catalogue.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
