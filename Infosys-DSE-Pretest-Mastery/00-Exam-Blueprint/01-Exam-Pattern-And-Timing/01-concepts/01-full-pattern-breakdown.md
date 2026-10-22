# Full Pattern Breakdown

> Section 00 · Exam Blueprint · Exam Pattern And Timing · _Estimated reading time: 18 min_
> **Prerequisite:** [../README.md](../README.md)

## In one sentence
**The pre-test is 4 sections, 60 questions, 90 minutes — the weight distribution matters far more than memorising exact question counts, because counts drift between batches.**

## Why the pre-test tests this
- **Asymmetry:** Java is reported at 25/60 (over 40% of the paper) while Aptitude is reported at 10/60. Where the questions are tells you where the marks are.
- **Mixed skills:** it tests logic (Aptitude), workplace judgment (English & L&D), data handling (DBMS/SQL), and coding fundamentals (Java) — no single skill carries you.
- **Filtering:** designed so 65% (39/60) is achievable but tight without pacing discipline.
- **Variance:** counts, order, and negative marking are reported to change batch to batch, so the blueprint gives you the *pattern*, never a guarantee.

## Core concept

### Canonical pattern (reported consistently by candidates)
| # | Section | Count (reported) | Focus | Nature of questions |
|---|---------|------------------|-------|---------------------|
| 1 | Aptitude | 10 | data sufficiency, percentages, data interpretation, ranking, inequalities, number series, mixtures/alligations | Calculation + logic |
| 2 | English & L&D | 15 | behavioural/scenarios, workplace professionalism/etiquette, error correction | Judgment + language |
| 3 | DBMS / SQL | 10 | SQL up to JOINs, two-table query, SQL output, normalization, ACID, DBMS theory | Conceptual + query-based |
| 4 | Java problem-solving | 25 | OOPs, interfaces/inner classes, packages/access modifiers, collections, errors/exceptions, pseudo-code output, compile/execute | Code reading + output |
| | **Total** | **60** | | **90 minutes** |

### The three things you must never confuse
| Thing | Value | Why it matters |
|-------|-------|----------------|
| Total questions | 60 | Defines the 90-second average |
| Total time | 90 minutes | The hard constraint |
| Pass mark | 65% = 39/60 | The gate to stream selection |

### What stays vs what varies
| Element | Stability | Notes |
|---------|-----------|-------|
| Total 60 / 90 | High | Reported across recent intakes |
| 65% pass (39/60) | High | Commonly reported for unlocking stream selection |
| 4 sections | High | Aptitude, English & L&D, DBMS/SQL, Java |
| Section topics | High | The topic lists above recur |
| Exact counts | Low | Can shift by batch — read live |
| Section order | Low | Can differ on the day |
| Negative marking | Low | Reported to vary; never assume |

### Weight → time allocation
| Section | Q | Share of paper | Reported time budget | Seconds/question |
|---------|---|----------------|----------------------|------------------|
| Aptitude | 10 | 16.7% | ~15 min | 90 |
| English & L&D | 15 | 25.0% | ~22 min | 88 |
| DBMS / SQL | 10 | 16.7% | ~18 min | 108 |
| Java | 25 | 41.7% | ~35 min | 84 |
| **Total** | **60** | **100%** | **90 min** | **90 avg** |

The budgets above are **planning baselines**. They are not mandated by the test. Their only job is to stop one section from quietly eating another's time.

### Negative marking note
If negative marking is present, it changes the whole guessing calculus — a wrong answer costs you part of a correct one. If it is absent, leaving a blank is strictly worse than an educated guess. **You cannot know which world you are in until you read the live instructions.** Plan for "avoid blind guessing" and adjust after reading.

### Why the topics are what they are
| Section | Why these topics |
|---------|------------------|
| Aptitude | The classic Indian campus-reasoning pool: sufficiency, percentages, DI, ranking, inequalities, series, alligation |
| English & L&D | DSE trains for client-facing delivery, so the test screens judgment and communication |
| DBMS/SQL | Data Engineering and Data Science streams need SQL; joins are the natural cut-off for screening |
| Java | The dominant DSE training language; output prediction is fast and objective to grade |

## Worked example
**Meera's case.** Meera is strong in DBMS/SQL (10 questions) but panics on time. Walk the arithmetic:

1. If she spends 25 minutes on the first 15 questions (a mix of Aptitude and English), she has cleared 15 of 60 questions but used 27.8% of the clock for 25% of the questions — roughly on pace, but she has not yet touched Java.
2. Java is 25 questions. At ~84s/question it needs about 35 minutes. If only 65 minutes remain when she reaches Java, she is fine — but if she stalls in Aptitude and reaches Java with 30 minutes, she is 5 minutes short and will rush output questions she could have solved.
3. The fix is not "go faster everywhere" — it is to **time-box each section to its budget** and flag anything that overruns.

**Numbers:** 35 minutes for 25 Java questions = 84 seconds each. Overshooting to 95 seconds each costs `25 × 11 = 275 seconds` ≈ 4.6 minutes — more than one full English sub-section's worth of time.

## Quick rules
- **60 questions, 90 minutes, 90 seconds average.** Everything else is detail.
- **Java is the biggest pool (25 reported, ~41.7%).** Protect its time.
- **Aptitude is the smallest pool (10 reported).** Do not over-invest.
- **The gate is 39/60 (65%).** No clearing, no stream selection.
- **Read the live instructions.** Counts, order, and negative marking are the live test's decision, not this file's.
- **Topics are more stable than counts.** Drill the topics even if counts shift.
- **Never leave blanks if there is no negative marking.**

## Common traps
- **Treating all sections as equally weighted.** They are not — Java is more than double Aptitude.
- **Ignoring English & L&D because it "isn't technical".** It is 25% of the paper and often the fastest marks.
- **Assuming a fixed section order.** Candidates report different orders; attack by solvability, not by the order you expected.
- **Forgetting batch variance.** The single most common cause of "but last time it was different" is expecting one batch's counts to hold for another.
- **Memorising 39 as "39 correct" without checking the penalty.** Under penalties your net score is what counts.

## Checklist
- [ ] You can state 60 questions / 90 minutes / 90 seconds / 39-to-pass without checking.
- [ ] You know the four sections and the reported counts.
- [ ] You know the topic list inside each section.
- [ ] You know Java is the largest reported section and Aptitude the smallest.
- [ ] You will read the live instructions before answering anything.
- [ ] You will work by 90-second chunks regardless of order.

## Related
- [../README.md](../README.md)
- [02-timing-by-section.md](02-timing-by-section.md)
- [../02-techniques/01-ninety-second-rule.md](../02-techniques/01-ninety-second-rule.md)
- [../05-reference/01-per-second-budget-table.md](../05-reference/01-per-second-budget-table.md)
