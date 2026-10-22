# Negative Marking Decision Rules

> Section 00 · Exam Blueprint · Sectional Analysis · _Estimated reading time: 15 min_
> **Prerequisite:** [01-cheapest-marks-first.md](01-cheapest-marks-first.md)

## In one sentence
**Never assume negative marking — read the live instructions, then apply the guessing rule that matches the stated policy.**

## Why the pre-test tests this
- **Batch variance:** negative marking is reported to vary between batches, and the live test decides.
- **Blanks vs guesses:** the correct strategy flips entirely depending on whether a penalty exists.
- **Expected value:** with no negative marking, a blank is strictly worse than an educated guess.
- **Risk control:** with a heavy penalty, blind guessing can cost you the pass even when your knowledge was sufficient.

## Core concept

### Policy → action table
| Live policy (as stated) | Blank answer | Educated guess (2 options eliminated) | Blind guess (4 options) |
|--------------------------|--------------|----------------------------------------|--------------------------|
| No negative marking | **Never leave blank** — worst outcome | Always guess: positive EV | Always guess: positive EV |
| +1 / −0 (i.e., none) | Fill everything | Fill everything | Fill everything |
| +1 / −0.25 | Guess if you can eliminate ≥1 | Strongly guess: EV positive | EV ≈ 0; low value |
| +1 / −0.33 | Guess only if you eliminate ≥1 | Guess: EV positive | EV ≈ 0; skip if possible |
| +1 / −1 | Guess only if you eliminate ≥2 | Marginal; use judgment | Skip: EV negative |

### How to read the rules
1. Open the live instruction page before answering anything.
2. Find the marker allocation, e.g., "each correct = 1, each wrong = 0" or "each wrong = −0.25".
3. If it is ambiguous, assume the most conservative (worst-case negatives).
4. Record the policy on your rough sheet so you do not forget it mid-test.

### Expected value quick math
```
EV = (p_correct × mark) − (p_wrong × penalty)
```
- Four options, eliminate none: `p = 0.25` → `EV = 0.25 − 0.75 × penalty`.
- Eliminate two: `p = 0.5` → `EV = 0.5 − 0.5 × penalty`.
- **Rule of thumb:** a guess is worthwhile while `penalty < 0.33` if you cannot eliminate any option, or `penalty < 1.0` if you can eliminate two.

### EV worked table (mark = 1)
| Penalty | Blind EV (p=0.25) | Two-eliminated EV (p=0.5) | Decision |
|---------|-------------------|---------------------------|----------|
| 0 | +0.25 | +0.5 | Always guess |
| 0.25 | +0.0625 | +0.375 | Guess with elimination; blind marginal |
| 0.33 | +0.0025 | +0.335 | Guess with elimination; blind ~0 |
| 0.5 | −0.125 | +0.25 | Elimination only |
| 1.0 | −0.5 | 0 | Eliminate two minimum |

## Worked example
**Rahul faces two policy scenarios.**

*Scenario A — no negative marking.* He blind-guesses three questions at 25% each. Expected marks: `3 × 0.25 = 0.75`. Blanks would give 0. **Guess everything.**

*Scenario B — +1 / −0.25.* On a question where he eliminates two options (`p = 0.5`): `EV = 0.5 − 0.25 × 0.5 = +0.375` → **guess**. On a blind four-option guess (`p = 0.25`): `EV = 0.25 − 0.25 × 0.75 = +0.0625` → slightly positive, but low value. **Prefer blanks over blind guesses only when time is better spent elsewhere; otherwise the elimination guess is clearly worth it.**

### The one-line summary
| Policy | Rule |
|--------|------|
| No penalty | Fill every blank |
| Small penalty (−0.25) | Guess only with elimination |
| Large penalty (−1.0) | Guess only when two options are eliminated |

## Quick rules
- **Read the live policy first** — the entire strategy depends on it.
- **No negatives → never leave a blank.**
- **Negatives → only guess with eliminations.**
- **Conservative default if the policy is unclear.**
- **Compute EV, not instinct.**
- **Record the policy before you start.**

## Common traps
- **Assuming no negative marking because a previous batch had none.**
- **Assuming negative marking when there is none** and leaving cheap marks blank.
- **Blind guessing under a −1 penalty.**
- **Forgetting the policy after reading it once.**

## Checklist
- [ ] You read the live marker allocation before starting.
- [ ] You recorded the policy somewhere you can see.
- [ ] You know your elimination-based guess rule.
- [ ] You never leave blanks when there is no penalty.
- [ ] You avoid blind guesses under heavy penalties.
- [ ] You can compute EV for a guess in your head.

## Related
- [01-cheapest-marks-first.md](01-cheapest-marks-first.md)
- [../../03-Marks-Threshold-And-Stream-Choice/04-pitfalls/01-negative-marking-risk-table.md](../../03-Marks-Threshold-And-Stream-Choice/04-pitfalls/01-negative-marking-risk-table.md)
- [../../05-Pretest-History-And-Variants/01-concepts/03-what-stays-constant.md](../../05-Pretest-History-And-Variants/01-concepts/03-what-stays-constant.md)
