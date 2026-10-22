# Timing Traps

> Section 00 · Exam Blueprint · Exam Pattern And Timing · _Estimated reading time: 15 min_
> **Prerequisite:** [../02-techniques/01-ninety-second-rule.md](../02-techniques/01-ninety-second-rule.md)

## In one sentence
**Almost every timing trap is the same mistake wearing a different mask:** spending the next question's time on this question.

## Why the pre-test tests this
- **Known failure mode:** candidates who fail the 39/60 gate most often fail on pacing rather than knowledge.
- **Compounding effect:** one stall causes a cascade of rushed guesses, each costing another mark.
- **Section asymmetry:** over-running Java — the largest section — steals directly from Aptitude and English.
- **Recoverability:** pacing errors are entirely avoidable with a handful of rules.

## Core concept

### The trap table
| Trap | How it looks | Wrong outcome | Right move |
|------|--------------|---------------|------------|
| "One more step" | At 80s, convinced you are close | Cross 100s; lose a later question | Flag at 70s, best guess, move |
| Section lock-in | Refuse to leave Aptitude until every question is done | Java gets rushed | Time-box each section |
| Blank-and-freeze | You don't know it, so you stare | Two minutes lost | Move immediately, return if surplus |
| Double-checking | Re-reading questions you already answered | Eats the final-15 sweep | Check once, move |
| Time-check loops | Glancing at the clock after every question | Kills rhythm, raises anxiety | Check every 15 minutes |
| No flag system | You cannot recall what was uncertain | Final sweep is unfocused | Flag every uncertain question at 70s |
| Perfectionism | Must solve every question fully | Runs out of time | Bank points, guess the rest |

### The cascade, quantified
Suppose you stall 110 seconds on one Java question (20 seconds over the cap that bleeds into the next: really 110 vs 84 budget = 26s over). Then you rush the next three questions to recover and get two wrong. Net effect:
- Time lost: ~26s (small).
- Marks lost: 2 (large), because the rushed questions were ones you would have gotten right.

**The real cost of a stall is not the seconds — it is the accuracy damage to the questions that follow.**

### Section-specific traps
| Section | Trap | Fix |
|---------|------|-----|
| Aptitude | Deriving a long DI set | Skip at 70s if no clear path |
| English & L&D | Over-reading a scenario three times | One careful read, then answer |
| DBMS / SQL | Tracing a large join mentally | Trace only the columns you need |
| Java | Restarting a trace with a new hypothesis | Flag and move; do not restart |

## Worked example
**Right vs wrong on the same question.**

A Java inner-class question, at the 75-second mark.

- **Wrong:** "I'll just work out the outer-class access rule." He spends to 130 seconds and gets it right. But he loses 40 seconds later on a percentage question and gets it wrong. Net: **0 or −1.**
- **Right:** at 70 seconds, he eliminates two options, picks the one consistent with outer-class access rules, flags it, and moves. He answers the percentage question correctly. At minute 82, with surplus time, he returns to the flagged question and confirms it. Net: **+1 or +2.**

Same knowledge, same question — the difference is one decision at 70 seconds.

## Quick rules
- **70 seconds = decide and flag.**
- **90 seconds = hard cap, no exceptions in practice.**
- **Time-box every section.**
- **Check the clock every 15 minutes.**
- **Return only to flagged questions.**
- **Margin over perfection.**

## Common traps
- **Believing your section is "the slow one".** Usually the slow section is whichever one you over-invested in today.
- **Assuming no negative marking without reading.** The guessing policy changes if the live rules say so.
- **Treating flags as failures.** Flags are part of the system, not an admission of defeat.
- **Never checking the clock at all.** This is the opposite failure; check at the checkpoints.

## Checklist
- [ ] You can name your personal 70-second flag trigger.
- [ ] You time-box all four sections before you start.
- [ ] You check the clock every 15 minutes and no more often.
- [ ] You revisit only flagged questions at the end.
- [ ] You prioritise margin over completeness.
- [ ] You have a rule for what to do after a stall (do one cheap question).

## Related
- [../02-techniques/01-ninety-second-rule.md](../02-techniques/01-ninety-second-rule.md)
- [../03-worked-examples/01-simulated-90-minute-timeline.md](../03-worked-examples/01-simulated-90-minute-timeline.md)
- [../../04-Test-Day-Strategy/04-pitfalls/01-stuck-question-traps.md](../../04-Test-Day-Strategy/04-pitfalls/01-stuck-question-traps.md)
