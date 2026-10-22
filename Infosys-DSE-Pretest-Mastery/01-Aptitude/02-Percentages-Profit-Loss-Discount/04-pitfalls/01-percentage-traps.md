# Percentage Traps — What the Exam Sets for You

> Section 1 · Aptitude · Percentages, Profit/Loss & Discount · _Estimated reading time: 6 min_
> **Prerequisite:** [Percentage fundamentals](../01-concepts/01-percentage-fundamentals.md)

## In one sentence

Percentage questions fail on **direction and stacking**, not arithmetic — and every distractor in the
option list is built to reward exactly one wrong base or one added pair of percentages.

## Why the pre-test tests this

- In practice sets, the biggest source of lost marks in this archetype is picking the option that
  matches the *naive* reading of the question.
- The distractors below are not random: each one encodes a specific wrong base or a specific wrong
  operation.
- Learning to *see* the trap in the option list is faster than computing carefully every time.

## Core concept

### The nine traps and their signature options

| Trap | The wrong computation | The signature option |
|---|---|---|
| Percentage change on the new base | `change / new` | The reciprocal of the true value (14.29% beside 12.5%) |
| Adding successive changes | `a + b` | A round number like 20% or 30% |
| Symmetric rise/fall | "up x, down x = 0" | 0% / No change |
| Profit % on selling price | `profit / SP` | A value 2–4 points below the correct one |
| Adding discounts | `d1 + d2` | Exactly the sum, e.g. 30% |
| Markup minus discount | `markup − discount` | Exactly the difference, e.g. 15% |
| Reverse percentage | "x% more = x% less" | The same x |
| Reporting an intermediate | stopping one step early | The SP, or the MP |
| Averaging percentages | plain average | The unweighted mean |

Rule of thumb: **if an option is exactly the sum or the difference of two numbers in the question, it
is usually the trap.** The true answer is almost never that tidy. Equally, if an option equals a
number you computed on the way to the answer, check whether the stem asked for that number or the one
after it.

## Worked example

**Q. An article is marked at ₹1,200. It is sold at a discount of 20%, and the shopkeeper still makes
a profit of 20% on cost. What was the cost price?**

A. ₹800
B. ₹960
C. ₹1,000
D. ₹1,440

**The traps in this question**

| Trap | Where it shows up |
|---|---|
| Reporting an intermediate | Option B is the selling price, not the cost price |
| Applying the profit % to the wrong base | Option D multiplies 1,200 by 1.2 instead of solving for CP |
| Halving the discount | Option C comes from `1200 × 0.8 / 0.96` — a percentage slip |

**Correct reasoning**

```
SP = 1200 × 0.80 = ₹960          (discount applies to the marked price)
SP = 1.20 × CP   →   CP = 960 / 1.20 = ₹800
```

**Answer: A (₹800).**

**Second example — the added-percentage trap.**

**Q. A shopkeeper marks an item 25% above the cost price and offers a 10% discount. Profit percent?**

```
SP = CP × 1.25 × 0.90 = CP × 1.125   →   12.5% profit
```

The trap answers are 15% (25 − 10) and 30% (adding the two percentages). The correct answer is
**12.5%**, which is not a tidy number — and that is exactly the signal that you multiplied.

## Quick rules

- Name the base before you compute: old value, CP, MP, or total.
- If two percentages touch different bases, multiply. Never subtract them.
- Never let a tidy option pull you to it.
- Two successive discounts: `d1 + d2 − d1·d2/100`.
- Rise then fall of the same size loses `x²/100 %` — never 0%.
- Profit % is on CP; if a question says "on selling price", it says so explicitly.
- Discount chain then profit: solve backwards, `CP = SP / (1 + p/100)`.
- Before marking, check that your answer answers the **stem**, not a step on the way.

## Common traps

| Trap | How it shows up | Guard rail |
|---|---|---|
| New-value base | 14.29% offered next to 12.5% | Old value is the only legal base for % change |
| Added changes | +20% then +20% → 40% | Multiply: 1.2 × 1.2 = 1.44 |
| Symmetric myth | "up 20, down 20 = no change" | Loss = x²/100 % |
| Profit on SP | 11.76% next to 13.33% | CP = SP − profit, always |
| Added discounts | 30% next to 28% | 0.8 × 0.9 = 0.72 |
| Markup − discount | 15% next to 12.5% | 1.25 × 0.9 = 1.125 |
| Reverse percentage | 25% next to 20% | x/(100 + x) |
| Reporting an intermediate | ₹960 next to ₹800 | Write down what the stem asks for first |
| Percentage of percentage | 50% next to 8% | `N × 0.25 × 0.40` |
| Averaging percentages | 70% next to 68% | Weight by the base |

## Checklist

- [ ] I identified the base before computing anything.
- [ ] I never added two percentages that have different bases.
- [ ] I checked the reverse-percentage case.
- [ ] I did not pick an option because it was tidy.
- [ ] I wrote down what the question asks for and delivered that exact quantity.
- [ ] I can name the trap behind every question I got wrong.

## Related

- [Percentage fundamentals](../01-concepts/01-percentage-fundamentals.md)
- [Percentage speed tricks](../02-techniques/01-percentage-speed-tricks.md)
- [Solved percentage, profit/loss and discount set](../03-worked-examples/01-solved-percentage-set.md)
- [Percentage formula sheet](../05-reference/01-percentage-formula-sheet.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
