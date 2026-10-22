# Per-Second Budget Table

> Section 00 · Exam Blueprint · Exam Pattern And Timing · _Estimated reading time: 12 min_
> **Prerequisite:** [../01-concepts/02-timing-by-section.md](../01-concepts/02-timing-by-section.md)

## In one sentence
**The budget table converts section totals into per-question seconds, so you always know instantly whether you are ahead of or behind the pace line.**

## Why the pre-test tests this
- **Instant calibration:** the 90-second average hides the fact that different sections need different per-question budgets.
- **Checkpoint math:** questions-done divided by minutes-elapsed gives a single comparable number.
- **Section priority:** larger budgets protect larger score pools.
- **Practice targets:** every drill should be run against these numbers.

## Core concept

### The master budget
| Section | Q | Minutes | Total seconds | Seconds/Q | Rolling checkpoint |
|---------|---|---------|---------------|-----------|--------------------|
| Aptitude | 10 | 15 | 900 | 90 | 10 Q by min 15 |
| English & L&D | 15 | 22 | 1320 | 88 | +15 Q by min 37 |
| DBMS / SQL | 10 | 18 | 1080 | 108 | +10 Q by min 55 |
| Java | 25 | 35 | 2100 | 84 | +25 Q by min 90 |
| **Total** | **60** | **90** | **5400** | **90** | 60 Q by min 90 |

### The pace line
```
questions_done / minutes_elapsed   vs   60 / 90 = 0.667 questions per minute
```
- If your rate is **below 0.667**, you are behind — tighten immediately, do not wait.
- If your rate is **above 0.667**, you have a margin — bank it, but do not relax entirely.

### Speed tiers to target in practice
| Tier | Seconds/Q | Verdict |
|------|-----------|---------|
| Fast | 45-60 | Bank time for hard questions |
| On pace | 75-90 | Sustainable across the paper |
| Slow | 90-120 | Risk of a cascade in the later sections |
| Danger | >120 | Guarantees a shortfall; you will not finish |

### Diagnostic table
| Minute | Questions you should have done (0.667/min) |
|--------|--------------------------------------------|
| 15 | 10 |
| 30 | 20 |
| 45 | 30 |
| 60 | 40 |
| 75 | 50 |
| 90 | 60 |

Use this table at each checkpoint to compare your actual count against the target count.

## Worked example
**Meera at minute 30.** She has completed 18 questions. The pace line says she should have done `0.667 × 30 = 20`. Her rate is `18 / 30 = 0.6`, slightly behind.

The correction:
1. She identifies one flagged time-sink (a DI question) and skips it entirely for now.
2. She plans to recover the pace by minute 45: she aims for 30 done, and has 27 plus 3 fast English questions queued.
3. She hits 30 at minute 45 and is back on the line.

**Numbers:** recovering 2 questions over 15 minutes requires only a 0.067 questions-per-minute improvement — a single avoided 90-second stall. Small, early correction prevents a 39 → 36 failure later.

### When behind, pick from this recovery list
| Gap | Fastest recovery |
|-----|------------------|
| 1-2 Q | DBMS theory, behavioural English |
| 3-4 Q | Add data sufficiency, ranking, inequalities |
| 5+ Q | Add recognised Java output patterns; stop all new derivations |

## Quick rules
- **The pace line is 0.667 questions per minute.**
- **Check your rate at every 15-minute checkpoint.**
- **Protect Java's 25-question pool** — it is the largest.
- **Bank fast-section time; do not relax in it.**
- **Slow tier (90-120s/Q) means act now, not at minute 80.**
- **Recover from the recovery list, in order.**

## Common traps
- **Ignoring the rate until late** and discovering a 5-question deficit at minute 75.
- **Using the flat 90-second average for every section** — DBMS/SQL legitimately needs more per question.
- **Confusing pace with accuracy.** Hitting the rate by blind guessing is not hitting the rate.
- **Banking time and then stalling anyway** on the next hard question.

## Checklist
- [ ] You have memorised the pace line, 0.667 questions per minute.
- [ ] You know the four section budgets in seconds per question.
- [ ] You check your rate at every 15-minute checkpoint.
- [ ] You know which practice speed tier you currently sit in.
- [ ] You correct the moment your rate dips below the line.
- [ ] You use the recovery list when behind.

## Related
- [../01-concepts/02-timing-by-section.md](../01-concepts/02-timing-by-section.md)
- [../03-worked-examples/01-simulated-90-minute-timeline.md](../03-worked-examples/01-simulated-90-minute-timeline.md)
- [../../04-Test-Day-Strategy/05-reference/01-minute-by-minute-plan.md](../../04-Test-Day-Strategy/05-reference/01-minute-by-minute-plan.md)
