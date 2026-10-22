# Threshold Reference

> Section 00 · Exam Blueprint · Marks Threshold And Stream Choice · _Estimated reading time: 12 min_
> **Prerequisite:** [../01-concepts/01-threshold-arithmetic.md](../01-concepts/01-threshold-arithmetic.md)

## In one sentence
**One page: the gate number, the composition models, the five streams, and the penalty rule of thumb.**

## Why the pre-test tests this
- **Single-page revision:** every threshold fact in one place.
- **Mid-test reference:** the models and penalty rules you need under pressure.
- **Practice calibration:** check a mock against these numbers.
- **Clarity:** separates raw from net at a glance.

## Core concept

### The gate
| Item | Value |
|------|-------|
| Total | 60 |
| Pass mark | 65% |
| Raw needed | 39 |
| Safe target | 40 |
| Comfortable target | 42+ |

### Composition models to 40
| Model | Java | English | DBMS | Aptitude | Total |
|-------|------|---------|------|----------|-------|
| A balanced | 15 | 11 | 8 | 6 | 40 |
| B Java-heavy | 18 | 9 | 7 | 5 | 39 |
| C DBMS-heavy | 13 | 11 | 9 | 6 | 39 |
| D English-heavy | 12 | 12 | 8 | 7 | 39 |
| E wide | 14 | 11 | 8 | 7 | 40 |

### Streams after clearing
| Stream |
|--------|
| Java + Angular |
| Data Science & Agentic AI |
| UI Stack |
| Data Engineering |
| Microsoft Azure + .NET |

### The penalty rule of thumb
| Penalty x | Blind guess | Educated guess (2 eliminated) |
|-----------|-------------|-------------------------------|
| 0 | always | always |
| 0.25 | marginal | yes |
| 0.33 | no | yes |
| 1.0 | no | marginal |

**Always verify against the live instructions.**

## Worked example
**Applying the reference to a mock.** A candidate scores 43 correct, 8 wrong, 9 blank.
- Under `x = 0`: score 43 ✅.
- Under `x = 0.25`: `43 − 2 = 41` ✅.
- Under `x = 0.5`: `43 − 4 = 39` ✅ at the line.
- Under `x = 1.0`: `43 − 8 = 35` ❌ fails.

The reference table shows instantly that this candidate passes under 0, 0.25, and 0.5 but fails under 1.0 — which is exactly the kind of conclusion you need to draw in five seconds on test day.

## Quick rules
- **39 gate, 40 target.**
- **Net = correct − x × wrong.**
- **Five streams unlock.**
- **Accuracy beats volume under penalties.**
- **Aim for margin, not the line.**
- **Verify the live policy.**

## Common traps
- **Confusing raw and net.**
- **Assuming a fixed penalty.**
- **Ignoring stream seat variability.**

## Checklist
- [ ] You know the gate is 39/60.
- [ ] You have chosen a composition model.
- [ ] You know the five streams.
- [ ] You know the penalty rule of thumb.
- [ ] You verify the live penalty policy.
- [ ] You target 40 or more.

## Related
- [../01-concepts/01-threshold-arithmetic.md](../01-concepts/01-threshold-arithmetic.md)
- [../04-pitfalls/01-negative-marking-risk-table.md](../04-pitfalls/01-negative-marking-risk-table.md)
- [../../02-Sectional-Analysis/05-reference/01-section-weight-table.md](../../02-Sectional-Analysis/05-reference/01-section-weight-table.md)
