# Number Series — Solving Techniques

> Section 1 · Aptitude · Number Series · _Estimated reading time: 7 min_
> **Prerequisite:** [Number series pattern families](../01-concepts/01-series-pattern-types.md)

## In one sentence

One procedure — **difference table → ratio check → family test → extend** — plus three shortcut
checks that crack most pre-test series in under 70 seconds.

## Why the pre-test tests this

- Series questions have an unbounded number of possible rules, which is why candidates panic. In
  practice the pre-test uses the same eight families again and again.
- The fastest candidates are not smarter, they just run the **same four steps in the same order**,
  every time, and they stop at 70 seconds.
- Karthik's retrospective: "I used to stare at series until the section ended. Now I write the
  differences, and if nothing falls out in 60 seconds I mark and move."

## Core concept

### The four-step procedure

| Step | Action | Time |
|---|---|---|
| 1 | Write the **difference row** under the series | 15 s |
| 2 | If the differences are not constant, write the **ratio row** | 15 s |
| 3 | Identify the **family** from the pattern catalogue | 20 s |
| 4 | Extend by one step and match to an option | 20 s |

### Step 1 in detail — the difference table

```
Series:    5    12    23    40    63
Diff:         7    11    17    23
2nd diff:        4     6     6
```

Read the table top-down: the first row that is constant tells you the family.

| What you see | Family | How to extend |
|---|---|---|
| Differences constant | Arithmetic | Add the constant |
| Ratios constant | Geometric | Multiply |
| 2nd differences constant | Difference of difference | Increase the difference by the constant |
| 3rd differences constant | Higher-order polynomial | Increase the 2nd difference |
| Two interleaved patterns | Alternating | Split odd/even |
| Nothing constant | Square/cube/prime/digit family | Check the catalogue |

### Step 2 in detail — the ratio row

Write each term divided by the previous one. If the quotients are equal (or nearly equal), the series
is geometric.

```
3, 6, 12, 24, 48   ratios  2, 2, 2, 2
```

Ratios that are not integers (like 1.5 or 1.33) usually mean you should look for squares or an
alternating pattern instead.

### Step 3 — family test, in order

Test the families in this order. It is the order that fails fastest:

1. Arithmetic (constant difference)
2. Geometric (constant ratio)
3. Difference of difference
4. Squares / cubes / n(n+1)
5. Fibonacci-like
6. Alternating operations
7. Prime-based
8. Digit-based

### Step 4 — extend and match

Extend **one step only**. Then compare with the options. If your extended value is not an option, you
have the wrong family — do not extend further to "reach" an option.

### The three shortcut checks

**Check 1 — the last-two-term test.** Take the difference between the last two terms. If it is a
small familiar number (4, 5, 6, 7, 10, 12, 15, 20, 25), you are probably looking at an arithmetic or
second-difference series.

**Check 2 — the ratio test.** If the last term divided by the second-to-last is 2, 3, 1.5, 4 or 0.5,
the family is geometric or alternating.

**Check 3 — the "one weird term" test for wrong-term questions.** If exactly one term breaks an
otherwise clean rule, that is the answer. If two or three terms break it, you have the wrong rule
entirely — go back to step 1.

### The "wrong term" procedure

| Step | Action |
|---|---|
| 1 | Ignore the suspect term and build the difference row for the rest |
| 2 | Find the rule that fits the rest perfectly |
| 3 | Compute what the suspect term should be |
| 4 | The suspect term in the question is the answer |

| Mistake | Result |
|---|---|
| Picking the term that "looks different" | Often wrong — several terms look odd |
| Changing the rule to fit all terms | The rule becomes nonsense |
| Forgetting to check the corrected series | You may have found a rule that fits a *different* series |

### The 70-second rule for series

| Elapsed | Action |
|---|---|
| 0–20 s | Write the difference row |
| 20–40 s | Write the ratio row; test arithmetic and geometric |
| 40–70 s | Test squares/cubes/Fibonacci/alternating/digit |
| 70 s | If nothing fits, pick the option that continues the *closest* pattern and move on |

## Worked example

**Q. What comes next: 5, 20, 19, 76, 75, ?**

A. 74
B. 299
C. 300
D. 76

**Step 1 — difference row**

```
5, 20, 19, 76, 75, ?
   15, −1, 57, −1
```

The differences alternate between a large positive and −1. That is the signature of **alternating
operations**.

**Step 2 — confirm the rule**

```
5 × 4 = 20
20 − 1 = 19
19 × 4 = 76
76 − 1 = 75
75 × 4 = 300
```

**Step 3 — answer**: 300.

**Answer: C (300).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 74 | Applied the −1 step twice (75 − 1 = 74) |
| 299 | 75 × 4 − 1 = 299 — applied two operations instead of one |
| 76 | Repeated the previous result |

**Timing: 35 seconds.** The alternating pattern is visible from the raw series once you notice 20, 76
and the two −1 steps. You did not need the difference row — but writing it takes 10 seconds and
guarantees you see it.

**Second example — second differences.**

**Q. Find the missing term: 2, 5, 10, 17, 26, ?, 50**

```
Terms:   2   5   10   17   26   ?   50
Diffs:      3    5    7    9   ?    ?
2nd:          2    2    2    ?    ?
```

Second differences are constant at 2, so the differences go 3, 5, 7, 9, 11, 13.
Missing term = 26 + 11 = **37**. Check: 37 + 13 = 50 ✅

**Answer: 37.** (Options: 35, 36, 37, 38 → 37.)

## Quick rules

- Difference row first, ratio row second.
- Read the first constant row you find: differences, then 2nd differences.
- Test families in the order: arithmetic → geometric → difference-of-difference → squares/cubes →
  Fibonacci → alternating → primes → digit-based.
- Extend one step only; if it is not an option, the family is wrong.
- For wrong-term questions: find the rule, compute the correct value, the given term is the answer.
- If exactly one term breaks a clean rule, that is the wrong term. If several do, the rule is wrong.
- 70-second cap, then mark and move.

## Common traps

| Trap | Effect | Fix |
|---|---|---|
| Extending until an option appears | You invent a rule | Extend one step only |
| Continuing the last difference | Wrong when differences change | Look at the whole difference row |
| Missing alternating operations | You see only half the pattern | Split odd/even positions |
| Assuming arithmetic for a geometric series | Wrong next term | Always compute the ratio row too |
| Changing the rule to fit a wrong term | Nonsense rule | Exclude the suspect term, find the rule |
| Assuming one weird-looking term is the wrong one | Wrong answer | The rule decides, not the look |

## Checklist

- [ ] I wrote the difference row before I guessed.
- [ ] I wrote the ratio row when the differences were not constant.
- [ ] I tested the families in the standard order.
- [ ] I extended only one step.
- [ ] For a wrong-term question, I found the rule and recomputed the correct value.
- [ ] I finished inside 70 seconds.

## Related

- [Number series pattern families](../01-concepts/01-series-pattern-types.md)
- [Solved number-series set](../03-worked-examples/01-solved-series-set.md)
- [Series traps](../04-pitfalls/01-series-traps.md)
- [Pattern catalogue](../05-reference/01-series-pattern-catalogue.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
