# Threshold Arithmetic Technique

> Section 00 · Exam Blueprint · Marks Threshold And Stream Choice · _Estimated reading time: 15 min_
> **Prerequisite:** [../01-concepts/01-threshold-arithmetic.md](../01-concepts/01-threshold-arithmetic.md)

## In one sentence
**Run the threshold arithmetic in 30 seconds: count your projected correct per section, sum, then compare the net to 39.**

## Why the pre-test tests this
- **Live feedback:** it lets you judge mid-test whether you are pacing to pass.
- **Penalty awareness:** it separates raw correct from net score.
- **Recovery trigger:** it tells you exactly when to switch to cheap-mark mode.
- **Calm:** it replaces vague anxiety with a number you can act on.

## Core concept

### The procedure
1. After each section (or at each 15-minute checkpoint), estimate your **projected correct** for that section.
2. Sum across sections to get **projected raw**.
3. If a penalty `x` is stated, estimate wrongs and compute **net = correct − x × wrong**.
4. Compare net to 39.
5. If net < 39 and time remains, switch to cheap-mark mode.

### The projection table
| Section | Done | Projected correct | Running total |
|---------|------|-------------------|---------------|
| Aptitude | 10 | 6 | 6 |
| English & L&D | 15 | 11 | 17 |
| DBMS / SQL | 10 | 8 | 25 |
| Java | 25 | 15 | 40 |
| **Net (no penalty)** | | | **40 ✅** |

### Penalty example
| Correct | Wrong | Penalty | Net | Verdict |
|---------|-------|---------|-----|---------|
| 40 | 5 | 0.25 | 38.75 | ⚠️ below |
| 40 | 3 | 0.25 | 39.25 | ✅ above |
| 42 | 8 | 0.25 | 40 | ✅ safe |
| 39 | 0 | 0 | 39 | ✅ at line |

### Cheapest revert moves when below
1. Bank DBMS theory (ACID, normalization).
2. Bank behavioural / etiquette English.
3. Do structural Aptitude (data sufficiency, ranking, inequalities).
4. Do recognised Java output patterns.

## Worked example
**Rahul at minute 60.**

- Projected: Java 12, English 9, DBMS 7, Aptitude 4 = **32 raw**.
- Estimated wrongs: 10. Penalty: 0.25.
- Net = `32 − 2.5 = 29.5` → **below 39.**

He switches to cheap-mark mode:
- Finishes two DBMS theory questions he skipped → +2.
- Does three more behavioural English questions he knows → +3.
- Picks up two easy Java output patterns → +2.

Projected net climbs to `29.5 + 7 = 36.5` with 20 minutes left. He now spends the remaining time on elimination-based guesses to push above 39.

**Numbers:** the projection at minute 60 gave him 30 minutes of warning. Without it, he would have discovered the shortfall at minute 85 and had no time to recover.

### Re-projection cadence
| Checkpoint | Action |
|------------|--------|
| 30 min | Rough projection; note if behind |
| 45 min | Confirm or switch to cheap-mark mode |
| 60 min | Final projection; commit remaining plan |
| 75 min | Only flagged conversions and guesses |

## Quick rules
- **Project after every section or checkpoint.**
- **Compute net, not raw.**
- **39 is the line.**
- **Below the line → cheap-mark mode immediately.**
- **Above the line → protect, do not gamble.**
- **Re-project at 30, 45, and 60 minutes.**

## Common traps
- **Projecting optimistically** to feel better.
- **Forgetting the penalty** when computing net.
- **Switching to cheap-mark mode too late.**
- **Over-guessing when already above the line.**

## Checklist
- [ ] You can project your net score in 30 seconds.
- [ ] You compute net under any stated penalty.
- [ ] You know the cheap-mark revert moves in order.
- [ ] You switch to cheap-mark mode promptly when behind.
- [ ] You do not gamble when above 39.
- [ ] You re-project at 30, 45, and 60 minutes.

## Related
- [../01-concepts/01-threshold-arithmetic.md](../01-concepts/01-threshold-arithmetic.md)
- [02-stream-decision-support.md](02-stream-decision-support.md)
- [../04-pitfalls/01-negative-marking-risk-table.md](../04-pitfalls/01-negative-marking-risk-table.md)
