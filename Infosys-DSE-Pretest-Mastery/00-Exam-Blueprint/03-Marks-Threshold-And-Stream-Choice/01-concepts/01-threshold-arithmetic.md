# Threshold Arithmetic

> Section 00 · Exam Blueprint · Marks Threshold And Stream Choice · _Estimated reading time: 16 min_
> **Prerequisite:** [../README.md](../README.md)

## In one sentence
**39/60 is 65% of the paper, and the fastest way to see it is 15 Java + 11 English + 8 DBMS + 6 Aptitude = 40.**

## Why the pre-test tests this
- **A concrete target removes ambiguity:** "clear 39" is a number you can plan against.
- **Section math shows which sections must carry:** not every section needs the same contribution.
- **Margin planning:** aiming at 40 absorbs a single slip that would otherwise fail you.
- **Confidence:** when you always know how far from the line you are, you stop guessing.

## Core concept

### The threshold numbers
| Concept | Value |
|---------|-------|
| Raw marks needed | 39 |
| Total marks | 60 |
| Percentage | 65% |
| Safe target | 40 |
| Comfortable target | 42+ |

### Composition models to 39-40
| Model | Java | English | DBMS | Aptitude | Total |
|-------|------|---------|------|----------|-------|
| A (balanced) | 15 | 11 | 8 | 6 | 40 |
| B (Java-heavy) | 18 | 9 | 7 | 5 | 39 |
| C (DBMS-heavy) | 13 | 11 | 9 | 6 | 39 |
| D (English-heavy) | 12 | 12 | 8 | 7 | 39 |
| E (wide balance) | 14 | 11 | 8 | 7 | 40 |

Any row clears the gate. Choose the row that matches your strengths.

### The algebra check
- Assuming no negative marking, each correct question is 1 mark.
- To hit 39 you need 39 correct in the worst case.
- If negative marking is `x` per wrong, you need `correct − x × wrong ≥ 39`.

### Net vs raw table
| Correct | Wrong | Penalty x | Net | Verdict |
|---------|-------|-----------|-----|---------|
| 42 | 5 | 0.25 | 40.75 | ✅ clears |
| 40 | 8 | 0.25 | 38 | ⚠️ below |
| 40 | 3 | 0.25 | 39.25 | ✅ clears |
| 41 | 19 | 0.25 | 36.25 | ❌ fails despite "41" |

The last row is the trap: **a raw 41 can fail.** Always convert to net.

## Worked example
**Meera under a penalty.** With `+1/−0.25`, Meera gets 45 correct and 12 wrong, leaving 3 blank.
- Net = `45 − 0.25 × 12 = 45 − 3 = 42` → **clears.**

Now a weaker candidate, same paper: 41 correct, 19 wrong, 0 blank.
- Net = `41 − 0.25 × 19 = 41 − 4.75 = 36.25` → **fails while "answering" 41 questions.**

Both candidates "did" a similar number of questions. The difference is accuracy. Under penalties, **accuracy beats volume** — the opposite of the no-penalty world.

### Decision rule
| Situation | Action |
|-----------|--------|
| No penalty stated | Fill everything; volume helps |
| Small penalty | Guess only with elimination; protect accuracy |
| Large penalty | Do not guess blindly; blank is often better |

## Quick rules
- **Need 39, target 40.**
- **Java 15 + English 11 + DBMS 8 + Aptitude 6** is one clean route.
- **With penalties, compute net, not raw.**
- **Know your composition model (A-E).**
- **Recheck after each mock.**
- **Read the live penalty rule before answering.**

## Common traps
- **Reading raw correct as your score** when penalties apply.
- **Targeting exactly 39** so one slip fails you.
- **Forgetting the marks-per-question value** if the live test differs.
- **Assuming all questions carry equal weight** if the live rules say otherwise.

## Checklist
- [ ] You know 39/60 = 65%.
- [ ] You have chosen a composition model.
- [ ] You can compute net under any penalty in your head.
- [ ] You target 40 or more.
- [ ] You verify the model with each mock.
- [ ] You read the live penalty rule first.

## Related
- [02-scenario-planning.md](02-scenario-planning.md)
- [04-stream-choice-gating.md](04-stream-choice-gating.md)
- [../02-techniques/01-threshold-arithmetic-technique.md](../02-techniques/01-threshold-arithmetic-technique.md)
- [../../02-Sectional-Analysis/01-concepts/05-score-model-building-39.md](../../02-Sectional-Analysis/01-concepts/05-score-model-building-39.md)
