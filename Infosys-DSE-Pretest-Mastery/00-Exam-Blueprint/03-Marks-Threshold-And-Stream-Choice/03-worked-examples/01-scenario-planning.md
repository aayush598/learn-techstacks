# Scenario Planning Walkthrough (Three Candidates)

> Section 00 · Exam Blueprint · Marks Threshold And Stream Choice · _Estimated reading time: 20 min_
> **Prerequisite:** [../01-concepts/02-scenario-planning.md](../01-concepts/02-scenario-planning.md)

## In one sentence
**Same paper, three candidates, three outcomes — the difference is whether the threshold arithmetic was pre-planned or improvised.**

## Why the pre-test tests this
- **Illustrates the model:** it shows weak, average, and strong days in action.
- **Decision timing:** it demonstrates exactly when to switch to cheap marks.
- **Streams follow:** each outcome maps to a different stream decision.
- **Recall:** it mirrors Ananya, Rahul, and Meera so the patterns stick.

## Core concept

### The setup
All three attempt the same 60-question mock with the reported structure: Aptitude 10, English & L&D 15, DBMS/SQL 10, Java 25. No negative marking is stated in this mock. The gate is 39.

### Candidate summaries
| Candidate | Java | English | DBMS | Aptitude | Total | Outcome |
|-----------|------|---------|------|----------|-------|---------|
| Ananya (average) | 15 | 11 | 8 | 6 | 40 | ✅ clears |
| Rahul (Java-strong) | 18 | 8 | 7 | 5 | 38 | ❌ just misses |
| Meera (DBMS-strong) | 13 | 11 | 9 | 6 | 39 | ✅ at the line |

### Rahul's failure analysis
| Factor | Detail |
|--------|--------|
| Strength | Java 18/25 — excellent |
| Weakness | English 8/15 — below his 9 target |
| Error | Left 2 behavioural questions blank "because English is hard" |
| Impact | Those 2 were cheap, high-probability marks |
| Fix | Never skip behavioural or etiquette; they need no grammar skill |

### Meera's line-miss risk
Meera cleared at exactly 39, with no margin. One slip would have failed her. Her correction: raise English to 12 by drilling error correction, which builds the margin.

### Ananya's balanced path
Ananya's 40 came from no single hero section: 15 + 11 + 8 + 6. This is the most robust route, because no section is a single point of failure.

### Threshold checks over time
| Minute | Ananya projected | Rahul projected | Meera projected |
|--------|------------------|-----------------|-----------------|
| 30 | 20 | 19 | 19 |
| 60 | 33 | 30 | 32 |
| 75 | 37 | 34 | 36 |
| 90 | 40 | 38 | 39 |

Rahul saw "34 at minute 75" and should have switched to cheap-mark mode (behavioural English, DBMS theory) rather than spending his last 15 minutes on two hard Java traces that never resolved.

## Worked example
**Rahul's correct 75-90 minute plan.**

1. Skip the two hard Java traces (already flagged).
2. Answer the 2 blank behavioural questions: +2 likely.
3. Do one DBMS normalization question he skipped: +1.
4. Re-trace one known Java output pattern: +1.

**Net effect:** 38 → 42 projected. His knowledge was enough; his threshold technique was not.

### The general recovery template
| Situation at minute 75 | Action |
|------------------------|--------|
| Projected ≥ 42 | Convert flags only |
| Projected 39-41 | Convert flags + 2 cheap marks |
| Projected < 39 | Cheap-mark mode: behavioural, DBMS theory, DS, ranking |
| Projected < 33 | Cheap-mark mode plus elimination-based guesses |

## Quick rules
- **Never skip behavioural or etiquette questions.**
- **Switch to cheap marks at minute 75 if behind projection.**
- **Robustness: spread meaning across all four sections.**
- **If you are at the line at 90, you had no margin — fix it next mock.**
- **Identify your projected shortfall before the last 15 minutes.**
- **Use the recovery template, not instinct.**

## Common traps
- **Leaving cheap blanks.**
- **Spending the final 15 minutes on unresolved hard questions.**
- **Celebrating a 39 without noting the zero margin.**
- **Failing to project mid-test.**

## Checklist
- [ ] You never skip behavioural or etiquette questions.
- [ ] You switch to cheap marks at 75 minutes if behind.
- [ ] You aim for a spread, not one hero section.
- [ ] You build margin above 39.
- [ ] You project at every checkpoint.
- [ ] You know the recovery template by heart.

## Related
- [../01-concepts/02-scenario-planning.md](../01-concepts/02-scenario-planning.md)
- [../02-techniques/01-threshold-arithmetic-technique.md](../02-techniques/01-threshold-arithmetic-technique.md)
- [../04-pitfalls/01-negative-marking-risk-table.md](../04-pitfalls/01-negative-marking-risk-table.md)
- [../../02-Sectional-Analysis/03-worked-examples/01-section-score-reconstruction.md](../../02-Sectional-Analysis/03-worked-examples/01-section-score-reconstruction.md)
