# The 90-Second Rule

> Section 00 · Exam Blueprint · Exam Pattern And Timing · _Estimated reading time: 17 min_
> **Prerequisite:** [../01-concepts/01-full-pattern-breakdown.md](../01-concepts/01-full-pattern-breakdown.md)

## In one sentence
**The 90-second rule is: know (≤45s) → eliminate (45-70s) → best guess + flag + move (70-90s), and never exceed 90 seconds on any question.**

## Why the pre-test tests this
- **Time scarcity:** 60 questions in 90 minutes leaves no room for rumination — the average is exactly 90 seconds.
- **Volume:** the test spans four unrelated domains, so you will hit unfamiliar material regardless of preparation.
- **Selection:** the pre-test filters for disciplined decision-making, not stubbornness.
- **Stakes:** a single 110-second stall costs more than the question is worth if it makes you rush two easier ones.

## Core concept

### The decision tree
| Time | State | Action | Exit |
|------|-------|--------|------|
| 0-45s | You see the method instantly | Solve, mark the answer, move | Answered |
| 45-70s | You know the approach but the steps need work, OR you can eliminate options | Eliminate wrong options; if a clear answer emerges, mark and move | Answered or down to 2 options |
| 70-90s | Stuck, but you can eliminate ≥1 option or have a hunch | Pick the least-wrong/best guess, flag for review, move. Do **not** restart | Flagged |
| >90s | Over the cap | Stop. If nothing is marked, select a best guess, flag, move. Never cross the cap in practice | Flagged |

### Why each boundary exists
- **45s:** if you cannot see the method in 45 seconds, more staring rarely reveals it. The method either surfaces fast or belongs to the elimination phase.
- **70s:** this is the flag point. Flagging is an *action*; staring is not. Flagging lets you return later without losing the question.
- **90s:** this is the hard cap. In practice you treat 90s as absolute, so that in the real test your worst case is still on budget.

### Application per section
| Section | Adaptation |
|---------|------------|
| Aptitude | Elimination-heavy on number series and inequalities; skip long DI at 70s |
| English & L&D | Read the stem first; the professional answer is usually quick once you know the intended tone |
| DBMS / SQL | Trace small joins/output; if the trace is unclear at 70s, guess and flag |
| Java | Trace the key variables with a small table; for theory, eliminate; if scoping confuses you past 70s, guess and flag |

### The practice drill
1. Set a visible 90-second timer per question on a 10-question bank.
2. Enforce a flag at 70 seconds even if you think you are close.
3. Review only the flagged questions at the end.
4. Count your "time violations" (any question that crossed 90s).
5. Repeat until a full 10-question set has zero violations.

### What to do with saved time
Saved seconds are not a reward to spend on the next hard question; they are a buffer. Bank them for the sections where you are genuinely strong, so that a strong section reaches high accuracy rather than being cut short.

## Worked example
**Ananya's two questions.**

*Question 1.* A mixture/alligation problem. At 40 seconds she recognises the alligation cross method and completes it at 55 seconds. She marks and moves, having used 55 of her 90 seconds — a 35-second surplus.

*Question 2.* A number series: `2, 6, 12, 20, 30, ?`. At 60 seconds she has not found the rule. At 70 seconds she eliminates two options using the parity/alternation check (differences are 4, 6, 8, 10 → next difference 12 → 42). She marks **42**, flags it, and moves.

**Outcome:** she finishes her allocated Aptitude budget with time to spare and uses the surplus on an easy percentage question later. Had she stared at the series to 150 seconds, she would have lost the percentage question's guaranteed mark. The rule converted a would-be cascade into a net gain.

### Common arithmetic traps inside the rule
| Trap | Example | Correct handling |
|------|---------|------------------|
| "One more step" | You are one operation from the answer at 80s | Flag at 70s; return only with surplus |
| Restarting | You abandon method A and try method B at 75s | Do not restart; guess and flag |
| Sunk cost | "I've spent 80s, I can't quit now" | Sunk time is gone; move on |

## Quick rules
- **Read the stem before the options.**
- **≤45s = solve and move.**
- **45-70s = eliminate to a decision.**
- **70s = flag point.**
- **90s = hard cap, no exceptions in practice.**
- **Flag, don't freeze.**
- **Review only with surplus time.**

## Common traps
- **"Just one more step."** The single most expensive sentence in a timed test.
- **Flagging everything.** Over-flagging means your final review is unfocused. Aim for 5-10 flags in a 60-question paper.
- **Reviewing unflagged questions** and wasting the surplus you banked.
- **Going over 90s in practice.** This trains the exact habit that fails the real test.
- **Blind guessing without elimination.** If the live test has negative marking, blind guesses are expensive. Eliminate first.

## Checklist
- [ ] You can run the four-step tree from memory.
- [ ] You use a visible timer in practice.
- [ ] You flag at 70 seconds, every time.
- [ ] You never exceed 90 seconds in drills.
- [ ] You review only flagged questions, and only with surplus time.
- [ ] You keep your total flags in the 5-10 range.

## Related
- [../README.md](../README.md)
- [../03-worked-examples/01-simulated-90-minute-timeline.md](../03-worked-examples/01-simulated-90-minute-timeline.md)
- [../04-pitfalls/01-timing-traps.md](../04-pitfalls/01-timing-traps.md)
- [../../04-Test-Day-Strategy/02-techniques/01-flagging-and-review-strategy.md](../../04-Test-Day-Strategy/02-techniques/01-flagging-and-review-strategy.md)
