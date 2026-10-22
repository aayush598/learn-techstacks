# Data Sufficiency — Traps the Exam Sets for You

> Section 1 · Aptitude · Data Sufficiency · _Estimated reading time: 7 min_
> **Prerequisite:** [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)

## In one sentence

Every data-sufficiency trap is the same trick wearing a different mask — **the option you pick is a
judgement about the information, and the exam offers you a judgement about the numbers instead.**

## Why the pre-test tests this

- Data-sufficiency distractors are engineered, not random. Each wrong option corresponds to a specific
  misreading.
- The traps below account for the majority of lost DS marks in aptitude practice tests.
- A candidate who can name the trap has already stopped making the error.

## Core concept

### The five canonical misreadings

| # | Trap | What the exam gives you | What it wants you to conclude | Correct answer |
|---|---|---|---|---|
| 1 | **Number-hunting** | Options contain numbers like 8, 6, 15 | That some option is "the value" | No numeric option exists — answer is a letter |
| 2 | **Sufficiency-by-feel** | Statement I "looks stronger" than II | That I is therefore sufficient | Judgment, not strength, decides |
| 3 | **Percentage without a base** | "Water is 40% of the mixture" | That the value is determined | The base may live in Statement I |
| 4 | **D for contradictions** | Both statements yield a number | That "either alone works" | Different numbers ⇒ **E** |
| 5 | **A vs E at the fork** | Each statement alone insufficient | That the answer is E | Together may still work ⇒ **A** |

### Trap 1 in detail — the number-hunting trap

Data-sufficiency options are worded, not numeric. If you find yourself comparing "8" with "6" in the
option list, you have misread the options. There is exactly one option that is a *true statement about
the information*, and it must be true for every assignment of the unknowns that satisfies the
statements. This is why the exam can make "sometimes true" options attractive: a number can be
"possible" without being "forced".

### Trap 5 in detail — the fork that decides 30% of DS marks

```
Each statement alone insufficient
            │
            ├── Do they combine to ONE value?  YES → A
            │
            └── NO  → E
```

Candidates who jump straight to E skip half the decision. Measure how often you choose E in a
practice set; if it is more than 1 in 4, you are skipping the together-test. A healthy mix in a
random 8-question set is roughly A×3, B×1, C×1, D×1, E×2.

## Worked example

**Q. What is the number of litres of water in the mixture?**

Statement I: The mixture contains milk and water in the ratio 3 : 2 and the total mixture is 25 litres.
Statement II: Water constitutes 40% of the mixture.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**The trap:** Statement II contains a percentage, and 40% looks like it pins the answer. It does not.
40% of an unknown total is unknown.

**What a candidate who fell for it does:** picks C, because "II gives the percentage, so II decides
the answer".

**The right reasoning:** I alone gives 3 : 2 and the total 25 → milk 15, water 10 → one value for the
stem ("litres of water") → **I alone is sufficient**. II alone gives a fraction with no base → not
sufficient.

**Answer: B.** II is a percentage whose denominator lives in I — the "percentage without a base" trap.

**Second trap in the same question:** a candidate who instead answers A would be reasoning "I gives
the ratio, II gives the percentage, together they are obviously enough". That is right for the
conclusion but wrong for the option: **A requires that neither alone works, and I alone does work.**
Always check whether a single statement already settles it *before* you consider the pair.

## Quick rules

- If an option contains a number, you have misread the question. Data-sufficiency options are claims.
- "Looks stronger" ≠ "sufficient". Only uniqueness matters.
- A percentage or ratio in a statement needs its **base** in the same statement to be sufficient alone.
- Two statements giving two different numbers → **E**. Never D.
- Neither alone → run the together-test before you answer E.
- An option is correct only if it is true for **every** valid assignment. If it holds for one
  assignment only, it is a trap option.
- If you find "all of the above" in a DS question, re-read the stem — it is almost always a
  non-DS question wearing DS options.

## Common traps

| Trap | The wrong answer you would give | The right answer | Signal that you fell for it |
|---|---|---|---|
| Chose the numeric-looking option | e.g. "8" | the letter A–E | You cannot quote a letter |
| Chose C because Statement II has a percentage | C | B or D | You did not look for the base |
| Chose D because both statements "give a number" | D | E | You did not compare the two numbers |
| Chose E because "each statement alone is insufficient" | E | A | You skipped the together-test |
| Chose A because "together they must work" | A | B | I alone already settled it |
| Took 3 minutes on a DS question | — | 60 seconds | You solved instead of judged |

## Checklist

- [ ] I answered with a letter, every time, without hunting for a number.
- [ ] I compared the two answers when both statements looked sufficient.
- [ ] I looked for the base of every percentage and ratio.
- [ ] I ran the together-test in every "neither alone" case.
- [ ] My answer spread on a random set of 8 is not dominated by E.
- [ ] I finished a 8-question DS drill in under 12 minutes.

## Related

- [What data sufficiency asks](../01-concepts/01-what-data-sufficiency-asks.md)
- [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)
- [8 solved data-sufficiency questions](../03-worked-examples/01-solved-data-sufficiency-set.md)
- [Data-sufficiency one-pager](../05-reference/01-data-sufficiency-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
