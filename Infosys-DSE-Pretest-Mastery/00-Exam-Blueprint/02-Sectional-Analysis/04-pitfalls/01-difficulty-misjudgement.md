# Difficulty Misjudgement

> Section 00 · Exam Blueprint · Sectional Analysis · _Estimated reading time: 14 min_
> **Prerequisite:** [../02-techniques/01-cheapest-marks-first.md](../02-techniques/01-cheapest-marks-first.md)

## In one sentence
**Most sectional losses come from misjudging a question's difficulty in the first ten seconds and then refusing to re-classify it.**

## Why the pre-test tests this
- **First-impression trap:** a short question can hide a long derivation, and a wordy one can be trivial.
- **Sunk cost:** once you start a hard question, it feels wrong to leave it.
- **Cost asymmetry:** a misclassified data-interpretation set can consume three normal questions' time.
- **Recoverability:** re-classifying early is cheap; re-classifying mid-way is not.

## Core concept

### The misclassification table
| Looks like | Often actually is | Warning sign |
|-----------|-------------------|--------------|
| Short DI question | A multi-step calculation | Numbers need three or more operations |
| Simple number series | A non-obvious pattern | No pattern in the first 20 seconds |
| One-line SQL | A careful JOIN trace | Two tables, multiple conditions |
| Short Java snippet | A nested scoping puzzle | Inner class / generics |
| Wordy data-sufficiency question | Actually easy | It only needs one condition |

### The rule
- **Re-classify at 45 seconds.** If the question now looks harder than first thought, flag it and move.
- **Never upgrade a question from "easy" to "worth three minutes"** in the middle of answering it.

### The three-question cost test
Before committing, ask: "If I spend three more minutes here, which three other questions am I giving up?" If the honest answer is "two easy ones", flag the current question.

### Why short ≠ fast
Short questions are often short *because* the setup is compressed, hiding the work. The stem "What percentage of the town's second-quarter revenue came from the third store?" is one line but can require three chained operations. Wordy data-sufficiency stems, by contrast, are long but structurally simple.

## Worked example
**Karthik's retrospective.**

"A short data-interpretation question looked like 40 seconds. It needed a three-step percentage-of-a-percentage with a shared base. I burned 2.5 minutes and still guessed. In the recap I saw two ranking questions later that I never reached. Net: about −3 marks.

The fix: if the second step of a question is not obvious at 45 seconds, flag it and move. I now treat any question where I cannot see the whole path in 45 seconds as a flag, no matter how short the stem looked."

### Walk the math
| Action | Time | Marks likely |
|--------|------|--------------|
| Burn 150s on the DI set | 150s | 0 or 1 |
| Flag at 70s, use 80s saved on 2 ranking questions | 80s | +2 (ranking is near-certain) |
| **Difference** | | **+2 marks** for 1.3 fewer minutes on the DI set |

## Quick rules
- **Re-classify at 45 seconds.**
- **Beware short-looking derivations.**
- **Never upgrade a question's cost mid-answer.**
- **Flag the moment the cost doubles.**
- **Trust the 70-second rule over finishing.**
- **Apply the three-question cost test.**

## Common traps
- **"It's short, so it's fast."**
- **Sunk-cost completion** — finishing because you already started.
- **Ignoring the second-step signal** at 45 seconds.
- **Forgetting that DBMS/SQL tracing can be long** despite a short query.

## Checklist
- [ ] You re-classify every question at 45 seconds.
- [ ] You flag the moment a question's cost doubles.
- [ ] You avoid sunk-cost completion.
- [ ] You can spot the three-operation warning sign.
- [ ] You apply the three-question cost test.
- [ ] You protect later questions over finishing the current one.

## Related
- [../02-techniques/01-cheapest-marks-first.md](../02-techniques/01-cheapest-marks-first.md)
- [../../01-Exam-Pattern-And-Timing/04-pitfalls/01-timing-traps.md](../../01-Exam-Pattern-And-Timing/04-pitfalls/01-timing-traps.md)
