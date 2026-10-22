# Percentages, Profit/Loss and Discount — The Rules

> Section 1 · Aptitude · Percentages, Profit/Loss & Discount · _Estimated reading time: 8 min_
> **Prerequisite:** none

## In one sentence

**Every percentage question reduces to one multiplication** — `part = base × rate` — and the only real
skill is knowing which base, which rate, and whether the changes stack.

## Why the pre-test tests this

- Percentages are the highest-frequency archetype in the DSE aptitude section, usually 2–3 of the 10
  questions, and they share a formula set with profit/loss, discount and interest.
- The arithmetic is trivial; candidates lose marks on **direction** (which base?) and **stacking**
  (do two changes add or multiply?).
- Percentage questions are also the ones you can convert to fractions and finish in 20 seconds, which
  makes them the best value-per-second questions in the paper.

## Core concept

### 1. The one formula

| Thing | Formula | Watch out |
|---|---|---|
| x% of N | `N × x / 100` | The base is N, never the answer |
| Percentage change | `(new − old) / old × 100` | Always divide by the **old** value |
| Fraction to percentage | `numerator / denominator × 100` | Memorise the common ones (see 05-reference) |

### 2. Successive percentage change — changes **multiply**, not add

If a value changes by `a%` and then by `b%`, the net change is:

```
net % = a + b + (a × b / 100)
```

Equivalently, multiply the multipliers: `+10%` then `−10%` gives `1.10 × 0.90 = 0.99` → **1% decrease**.

| Change 1 | Change 2 | Multiplier | Net effect |
|---|---|---|---|
| +20% | +20% | 1.2 × 1.2 = 1.44 | +44% |
| +20% | −20% | 1.2 × 0.8 = 0.96 | −4% |
| +50% | −50% | 1.5 × 0.5 = 0.75 | −25% |
| +x% | −x% | `1 − x²/10000` | loss of `x²/100 %` |

The symmetric case is worth memorising: **a rise of x% followed by a fall of x% always loses
`x²/100 %`.** 20% up then 20% down loses 4%; 50% up then 50% down loses 25%.

### 3. Percentage of a percentage

```
x% of y% of N  =  (x × y / 100)% of N  =  N × x × y / 10000
```

20% of 30% of 5,000 = 5,000 × 0.20 × 0.30 = 300. Treat the two percentages as 0.2 and 0.3.

### 4. Profit, loss and selling price

| Quantity | Formula |
|---|---|
| Selling price (profit p%) | `SP = CP × (1 + p/100)` |
| Selling price (loss l%) | `SP = CP × (1 − l/100)` |
| Profit % | `(SP − CP) / CP × 100` — **always on cost price** |
| Loss % | `(CP − SP) / CP × 100` |

Profit percent is defined on **cost price**. A question that asks "profit on selling price" is
explicit and rare; when you see plain "profit percent", the base is CP.

### 5. Discount and marked price

| Quantity | Formula |
|---|---|
| Discount amount | `d% of marked price` |
| Selling price | `SP = MP × (1 − d/100)` |
| Two successive discounts d1, d2 | overall discount = `d1 + d2 − d1×d2/100` |
| Three successive discounts | multiply all three multipliers |

20% then 10% ⇒ overall discount 28%, **not 30%**. Always multiply: `0.8 × 0.9 = 0.72`.

### 6. Markup and discount together

```
SP = CP × (1 + markup/100) × (1 − discount/100)
```

A 20% markup and a 10% discount gives `1.2 × 0.9 = 1.08` → **8% profit**, not 10%.

### 7. Simple vs compound interest

| Type | Amount after n years | Interest |
|---|---|---|
| Simple | `P (1 + n·r/100)` | `P·n·r/100` |
| Compound | `P (1 + r/100)ⁿ` | `P[(1 + r/100)ⁿ − 1]` |

Two-year shortcut:

```
CI − SI = P × (r/100)²
```

For P = 10,000, r = 10%: `10000 × 0.01 = ₹100`. And the two-year compound amount is
`P × (1 + r/100)²` — one multiplication, no formula needed.

### 8. Percentage points vs percentage change

| Change | Correct wording | Value |
|---|---|---|
| 30% → 40% | +10 **percentage points**, or +33.33% **change** | two different numbers |
| A rate of 25% → 22% | −3 percentage points, or −12% change | — |

The exam asks "what percentage change" 90% of the time. The base is the old value.

### 9. Weighted average of percentages

Never average percentages directly. Use the base:

```
40% of students scored 80%; the rest scored 60%   → 0.4 × 80 + 0.6 × 60 = 68%
```

## Worked example

**Q. Rahul scored 360 marks out of 500 in a mock. How many marks must he score out of 800 in
another mock to keep the same percentage?**

- A. 460
- B. 576
- C. 720
- D. 608

**Step 1 — Get the percentage.** 360 out of 500 = `360/500 = 0.72` = 72%.

**Step 2 — Apply it to the new base.** 72% of 800 = `800 × 0.72` = **576**.

**Answer: B (576).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 460 | This is 57.5% of 800 — a different percentage, arrived at by confusing 360/800 |
| 720 | This is 90% of 800 — the "same marks" instinct; marks did not stay the same, the percentage did |
| 608 | This is 76% of 800 — a mid-point guess with no rule behind it |

**Faster route:** 360/500 = 0.72, and 800 × 0.72 = 576. Two operations, about 15 seconds.

## Quick rules

- `part = base × rate`. Identify the base in the first 5 seconds; most errors are base errors.
- Successive changes **multiply**. `a + b + ab/100` is the arithmetic version.
- `+x%` then `−x%` = loss of `x²/100 %`.
- Profit % is on **cost price**. Selling price = CP × (1 ± p/100).
- Discounts chain by **multiplication**; `20% + 10%` is 28%, never 30%.
- Marked price and cost price are two different anchors — do not mix them.
- Two-year CI − SI = `P(r/100)²`. Two-year CI amount = `P(1 + r/100)²`.
- `x% of y% of N = N × x × y / 10000`.
- Never average percentages; weight them by the base.
- Convert to fractions when you can: 25% = 1/4, 12.5% = 1/8, 16⅔% = 1/6.

## Common traps

| Trap | What you get | What you should get |
|---|---|---|
| Adding successive percentage changes | +10% then +10% → +20% | +21% |
| `+20%` then `−20%` treated as 0% | 0% | −4% |
| Profit % computed on selling price | 16.67% instead of 20% | 20% (on CP) |
| Two discounts added | 30% | 28% |
| 20% of 30% read as 50% | 2,500 | 300 |
| `30% → 40%` called a 40% change | 40% | 33.33% |
| CI and SI swapped for 2 years | — | SI: `P(1+2r/100)`, CI: `P(1+r/100)²` |
| Markup and discount added instead of multiplied | 10% | 8% |

## Checklist

- [ ] I can state the base for every percentage in the question before computing.
- [ ] I used multiplication (or `a + b + ab/100`) for any two successive changes.
- [ ] I checked whether the two changes were + and − of the same size and used the `x²/100` rule.
- [ ] I computed profit and loss percentage on cost price.
- [ ] I multiplied the discount chain rather than adding the discounts.
- [ ] I converted the percentage to a fraction when it was a common one.

## Related

- [Percentage speed tricks](../02-techniques/01-percentage-speed-tricks.md)
- [Solved percentage, profit/loss and discount set](../03-worked-examples/01-solved-percentage-set.md)
- [Percentage traps](../04-pitfalls/01-percentage-traps.md)
- [Percentage formula sheet](../05-reference/01-percentage-formula-sheet.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
