# Section Score Reconstruction (Meera's Mock)

> Section 00 · Exam Blueprint · Sectional Analysis · _Estimated reading time: 20 min_
> **Prerequisite:** [../01-concepts/05-score-model-building-39.md](../01-concepts/05-score-model-building-39.md)

## In one sentence
**Reconstructing a mock section by section shows exactly which attempts earned marks and which archetypes wasted time** — and it separates a knowledge gap from a pacing gap.

## Why the pre-test tests this
- **Feedback loop:** raw scores hide where the marks actually came from.
- **Targeted fixes:** the reconstruction points to the next hour of study.
- **Time audit:** it ties marks to minutes spent, exposing over-investment.
- **Threshold check:** it verifies whether your per-section targets are realistic for you.

## Core concept

### Meera's mock result (60 Q in 90 min)
| Section | Attempted | Correct | Wrong | Unattempted | Minutes spent |
|---------|-----------|---------|-------|-------------|---------------|
| Aptitude | 8 | 5 | 3 | 2 | 17 |
| English & L&D | 15 | 11 | 4 | 0 | 21 |
| DBMS / SQL | 10 | 9 | 1 | 0 | 16 |
| Java | 24 | 12 | 12 | 1 | 36 |
| **Total** | **57** | **37** | **20** | **3** | **90** |

**Raw score: 37 → below the 39 gate.**

### The archetype audit
| Section | Cheap marks earned | Expensive marks lost | Diagnosis |
|---------|--------------------|----------------------|-----------|
| Aptitude | DS, ranking (5) | DI + 1 series (skipped) | Correct to skip DI; lost 3 to rushed wrong answers |
| English & L&D | Behaviour + etiquette (11) | Error correction (4 wrong) | Grammar weakness, not judgment |
| DBMS / SQL | ACID, normalization, joins (9) | 1 query writing | The model worked |
| Java | Definitions + simple output (12) | Nested/inner + trace errors (12 wrong) | Time pressure caused the rush |

### Where the two missing marks were
1. **Aptitude:** 3 wrong answers were rushed (not attempted carefully) because Java over-ran by roughly 3 minutes.
2. **Java:** 12 wrong — at least 4 were trace questions she knows how to do but rushed.
3. **English:** 4 error-correction wrong — cheap to relearn with 20 minutes a day.

### The corrected plan
| Section | Old target | New target | Fix |
|---------|-----------|-----------|-----|
| Aptitude | 5 | 6 | Stop rushing; apply the 70s flag instead |
| English & L&D | 11 | 12 | Drill error correction 20 min/day |
| DBMS / SQL | 9 | 9 | Stable |
| Java | 12 | 15 | Time-box; trace with a variable table |
| **Total** | **37** | **42** | Above the gate |

## Worked example
**The reconstruction procedure, step by step.**

1. List every question by section.
2. Mark each as correct / wrong / skipped.
3. Tag each with its archetype (cheap / medium / expensive).
4. Sum marks earned per archetype.
5. Find the gap to 39.
6. Map the gap to the cheapest *fixable* archetypes.
7. Write a new per-section target.

Meera's step 5 found a 2-mark gap. Step 6 localized it to rushed Aptitude and rushed Java tracing — both pacing problems, not knowledge gaps. That is why her correction is "apply the flag rule", not "study more Java".

### Distinguishing pacing gaps from knowledge gaps
| Symptom in the audit | Gap type | Fix |
|----------------------|----------|-----|
| Wrong on cheap archetypes you usually get right | Pacing | Flag at 70s |
| Wrong on the same topic across mocks | Knowledge | Study the topic |
| Skipped a cheap question | Pacing / order | Cheap-marks first |
| Ran out of time on the last section | Pacing | Section time-box |
| Wrong on error correction every time | Knowledge | Grammar drill |

## Quick rules
- **Reconstruct every mock section by section.**
- **Tag by archetype, not just right/wrong.**
- **Find the gap to 39 and name the fix.**
- **Separate knowledge gaps from pacing gaps.**
- **Write new targets after each reconstruction.**

## Common traps
- **Only noting the total score.**
- **Blaming knowledge when the issue is speed.**
- **Ignoring skipped questions** — they hide both a failure and a correct strategy.
- **Not updating targets** after the reconstruction.

## Checklist
- [ ] You reconstruct mocks by section.
- [ ] You tag every question by archetype.
- [ ] You distinguish pacing gaps from knowledge gaps.
- [ ] You compute the gap to 39.
- [ ] You rewrite per-section targets after each mock.
- [ ] You act on the cheapest fixable archetype first.

## Related
- [../01-concepts/05-score-model-building-39.md](../01-concepts/05-score-model-building-39.md)
- [../02-techniques/01-cheapest-marks-first.md](../02-techniques/01-cheapest-marks-first.md)
- [../../03-Marks-Threshold-And-Stream-Choice/03-worked-examples/01-scenario-planning.md](../../03-Marks-Threshold-And-Stream-Choice/03-worked-examples/01-scenario-planning.md)
