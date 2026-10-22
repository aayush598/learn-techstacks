# Percentage Speed Tricks — Finish in 20 Seconds

> Section 1 · Aptitude · Percentages, Profit/Loss & Discount · _Estimated reading time: 7 min_
> **Prerequisite:** [Percentage fundamentals](../01-concepts/01-percentage-fundamentals.md)

## In one sentence

Convert the percentage to a **fraction**, apply it to the base, and you finish most percentage
questions before the 90-second rule can hurt you.

## Why the pre-test tests this

- The aptitude section is 10 questions in ~15 minutes. Two or three will be percentage questions, and
  they should be your *fastest* points, not your slowest.
- Rahul loses marks here by attempting decimal division (`36/500`) instead of recognising the
  fraction (0.72).
- These tricks are pure memorisation, so they are cheap to learn and 100% reliable in the exam.

## Core concept

### The fraction table you must know cold

| Fraction | % | Fraction | % | Fraction | % |
|---|---|---|---|---|---|
| 1/2 | 50% | 1/8 | 12.5% | 2/5 | 40% |
| 1/3 | 33⅓% | 1/9 | 11.11% | 3/5 | 60% |
| 1/4 | 25% | 1/10 | 10% | 3/4 | 75% |
| 1/5 | 20% | 1/12 | 8.33% | 4/5 | 80% |
| 1/6 | 16⅔% | 1/15 | 6.67% | 5/6 | 83⅓% |
| 1/7 | 14.29% | 1/16 | 6.25% | 5/8 | 62.5% |
| 1/11 | 9.09% | 1/20 | 5% | 2/3 | 66⅔% |

Reciprocal table (reverse the %): 25% ↔ 1/4, 12.5% ↔ 1/8, 16⅔% ↔ 1/6, 33⅓% ↔ 1/3, 62.5% ↔ 5/8,
66⅔% ↔ 2/3, 75% ↔ 3/4, 80% ↔ 4/5, 40% ↔ 2/5, 60% ↔ 3/5, 20% ↔ 1/5, 50% ↔ 1/2.

### The nine shortcuts

| # | Shortcut | Rule | Example |
|---|---|---|---|
| 1 | **Divide the base** | `x% of N` → `N ÷ (100/x)` | 25% of 480 = 480 ÷ 4 = 120 |
| 2 | **Tenth = 10%** | `x% of N` → `N ÷ 10` then scale | 30% of 500 = 50 × 3 = 150 |
| 3 | **Percentage change** | `old × (1 ± p/100)` | 20% rise on 350 = 350 × 1.2 = 420 |
| 4 | **Successive change** | multiply multipliers | +10% then −10% → ×0.99 |
| 5 | **Symmetric change** | loss = `x²/100 %` | 40% up, 40% down → −16% |
| 6 | **Profit to SP** | `CP × (1 + p/100)` | 20% profit on 450 → 540 |
| 7 | **Discount chain** | multiply `(1 − d/100)` | 20% then 10% → ×0.8 × 0.9 = 0.72 |
| 8 | **Two-year CI** | `P(1 + r/100)²` | 10,000 @ 10% → 12,100 |
| 9 | **% of %** | `N × x × y / 10000` | 20% of 30% of 5,000 → 300 |

### Reading a question backwards

When the question asks "what percent is X of Y", do **not** compute `X/Y` as a decimal and convert.
Instead ask: "X/Y = which fraction from the table?"

| Ratio | Percentage |
|---|---|
| 3/8 | 37.5% |
| 5/8 | 62.5% |
| 7/8 | 87.5% |
| 9/16 | 56.25% |
| 11/16 | 68.75% |

### The "difference is a percentage" trick

If two quantities differ and one is given as a percentage of the other, you do not need the base.

| Statement | Asked | Instant answer |
|---|---|---|
| B is 25% more than A | B as % of A | 125% |
| B is 20% less than A | B as % of A | 80% |
| A is 50% of B | A as % of B | 50% |
| B is 60% of A | B as % of A | 60% |

Also useful: if A is 25% more than B, then **B is 20% less than A** (1/1.25 = 0.8). The "reverse
percentage" trap.

## Worked example

**Q. A shopkeeper marks a jacket 20% above the cost price and then offers a 10% discount during a
sale. What is his profit percent?**

- A. 8%
- B. 10%
- C. 12%
- D. 2%

**Fast route (no base needed):**

```
SP = CP × 1.20 × 0.90 = CP × 1.08
```

So SP is 108% of CP → **8% profit**.

**Answer: A (8%).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 10% | The naive "markup minus discount" answer. Percentages of two different bases do not subtract |
| 12% | Someone multiplied 1.2 × 0.9 wrongly, or halved something |
| 2% | A sign/digit slip |

**Time: 20 seconds.** Recognise the two multipliers and multiply.

**Second example (speed check).** Price rises 25% and then falls 20%. Net multiplier
`1.25 × 0.80 = 1.00` → **no net change**. Answer choices around zero catch the majority of candidates
who answer "+5%".

## Quick rules

- `x% of N` → convert to a fraction and divide the base.
- `x%` change → multiply by `1 ± x/100`; never add or subtract the raw percentages.
- Successive changes multiply; the symmetric up-then-down case loses `x²/100 %`.
- Reverse percentages invert: 25% more ⇒ 20% less.
- Two successive discounts multiply; the effective discount is less than the sum.
- Profit/loss percent always uses cost price as the base.
- If a question has no base at all, the answer must be computable from multipliers only.
- Sanity-check the answer: it should sit between the plausible extremes offered.

## Common traps

| Trap | Effect | Fix |
|---|---|---|
| Converting `x/100` to a decimal by long division | 20 s wasted | Use the fraction table |
| Adding the two changes | +10% + +10% = +20% | Multiply multipliers |
| Treating "20% more" and "20% less" as symmetric | Wrong | Use the reciprocal rule |
| Forgetting that CP and MP are different bases | Wrong profit % | Label the base every time |
| Ignoring that a percentage of a percentage needs two multiplications | 20% of 30% → 50% | `N × 0.2 × 0.3` |

## Checklist

- [ ] I can list the fraction table (1/2 to 1/20 and the eighths) from memory.
- [ ] I convert the percentage to a fraction before computing.
- [ ] I use multipliers for any pair of changes.
- [ ] I check the reverse-percentage case (x% more ↔ y% less).
- [ ] I never subtract two percentages that have different bases.
- [ ] I finished 10 percentage questions in under 4 minutes.

## Related

- [Percentage fundamentals](../01-concepts/01-percentage-fundamentals.md)
- [Solved percentage, profit/loss and discount set](../03-worked-examples/01-solved-percentage-set.md)
- [Percentage traps](../04-pitfalls/01-percentage-traps.md)
- [Percentage formula sheet](../05-reference/01-percentage-formula-sheet.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
