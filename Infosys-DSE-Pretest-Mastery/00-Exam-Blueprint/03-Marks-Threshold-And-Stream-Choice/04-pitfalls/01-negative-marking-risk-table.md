# Negative Marking Risk Table

> Section 00 · Exam Blueprint · Marks Threshold And Stream Choice · _Estimated reading time: 16 min_
> **Prerequisite:** [../02-techniques/01-threshold-arithmetic-technique.md](../02-techniques/01-threshold-arithmetic-technique.md)

## In one sentence
**Never assume no negative marking — if a penalty is applied, a 40 raw can become a 36 net and fail the gate.**

## Why the pre-test tests this
- **The gate is net, not raw:** penalties silently convert passes into fails.
- **Batch variance:** the policy is reported to vary; the live test decides.
- **Blind guessing risk:** a wrong strategy destroys the margin you built.
- **Recoverability:** knowing the table prevents a last-minute panic.

## Core concept

### The net-score risk table
Assumes 1 mark per correct. `x` = penalty per wrong.
| Raw correct | Wrong | Blanks | x=0 | x=0.25 | x=0.33 | x=0.5 | x=1.0 |
|-------------|-------|--------|------|--------|--------|-------|-------|
| 42 | 5 | 13 | 42 ✅ | 40.75 ✅ | 40.35 ✅ | 39.5 ✅ | 37 ❌ |
| 40 | 8 | 12 | 40 ✅ | 38 ⚠️ | 37.36 ❌ | 36 ❌ | 32 ❌ |
| 40 | 3 | 17 | 40 ✅ | 39.25 ✅ | 39.01 ✅ | 38.5 ⚠️ | 37 ❌ |
| 39 | 0 | 21 | 39 ✅ | 39 ✅ | 39 ✅ | 39 ✅ | 39 ✅ |
| 45 | 12 | 3 | 45 ✅ | 42 ✅ | 41.04 ✅ | 39 ✅ | 33 ❌ |
| 41 | 19 | 0 | 41 ✅ | 36.25 ❌ | 34.73 ❌ | 31.5 ❌ | 22 ❌ |

### Reading the table
- **40 correct with 8 wrong fails under any penalty ≥ 0.25.** Accuracy matters as much as volume.
- **A perfectly accurate 39 (0 wrong) passes under every penalty.** You cannot go below 39 with zero wrong.
- **Accuracy beats volume once penalties exist.**

### The decision matrix
| Live policy | Blank | Educated guess (2 eliminated) | Blind guess |
|-------------|-------|-------------------------------|-------------|
| x = 0 | ❌ never blank | ✅ guess | ✅ guess |
| x = 0.25 | ❌ never blank | ✅ guess | ⚠️ marginal |
| x = 0.33 | ⚠️ only if no elimination | ✅ guess | ❌ skip |
| x = 1.0 | ✅ blank if no elimination | ⚠️ marginal | ❌ skip |

### EV reminder
`EV = p_correct × mark − p_wrong × penalty`. With four options and two eliminated (`p = 0.5`), a guess is positive EV while `penalty < 1.0`.

## Worked example
**Two candidates end with 45 correct, 12 wrong, 3 blank.**

- Candidate under `x = 0.25`: `45 − 0.25 × 12 = 42` → ✅ clears.
- Candidate under `x = 0.5`: `45 − 0.5 × 12 = 39` → ✅ at the line.
- Candidate under `x = 1.0`: `45 − 1.0 × 12 = 33` → ❌ fails.

Same answers, three different results — the policy reading decided it. This is why you must read the live instructions before answering a single question.

### The safe habit
| Habit | Why |
|-------|-----|
| Read the marker allocation first | Determines everything |
| Record it on your rough sheet | You will forget mid-test |
| Guess only with elimination under penalties | Protects net |
| Fill everything under no penalty | Volume is free |

## Quick rules
- **Read the policy first, always.**
- **Compute net before concluding.**
- **Accuracy beats volume under penalties.**
- **Never blind guess under `x ≥ 0.33`.**
- **Never leave blanks under `x = 0`.**
- **Record the policy on your rough sheet.**

## Common traps
- **"I got 40, I passed"** without computing net.
- **Blind-guessing a full section under a heavy penalty.**
- **Leaving blanks when there is no penalty.**
- **Assuming the previous batch's policy.**

## Checklist
- [ ] You read and recorded the live policy.
- [ ] You can compute net for any penalty `x`.
- [ ] You know your guessing rule for each policy.
- [ ] You never leave blanks when `x = 0`.
- [ ] You never blind-guess when `x ≥ 0.33`.
- [ ] You verify the policy on your rough sheet mid-test.

## Related
- [../02-techniques/01-threshold-arithmetic-technique.md](../02-techniques/01-threshold-arithmetic-technique.md)
- [../../02-Sectional-Analysis/02-techniques/02-negative-marking-decision.md](../../02-Sectional-Analysis/02-techniques/02-negative-marking-decision.md)
- [../../05-Pretest-History-And-Variants/01-concepts/03-what-stays-constant.md](../../05-Pretest-History-And-Variants/01-concepts/03-what-stays-constant.md)
