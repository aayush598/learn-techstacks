# What To Do When Stuck

> Section 00 · Exam Blueprint · Test Day Strategy · _Estimated reading time: 15 min_
> **Prerequisite:** [01-flagging-and-review-strategy.md](01-flagging-and-review-strategy.md)

## In one sentence
**When stuck, run a fixed 5-step unstick procedure instead of staring** — elimination, estimate, flag, move, and return only with surplus time.

## Why the pre-test tests this
- **Stuck is normal:** every candidate hits 5-10 such questions in a 60-question paper.
- **Cost of staring:** 30 extra seconds usually changes nothing but always costs something.
- **Procedure removes panic:** a fixed script replaces the urge to freeze.
- **Cheap-mark mode recovers the loss:** the next question should restore rhythm.

## Core concept

### The 5-step unstick procedure
| Step | Action | Time |
|------|--------|------|
| 1 | Re-read the stem, not the options | 10s |
| 2 | Eliminate obviously wrong options | 15s |
| 3 | Estimate/approximate or pick by parity/pattern | 15s |
| 4 | Flag and move | 10s |
| 5 | Return only if surplus time after the final third | — |

### Stuck type → countermeasure
| Stuck type | Countermeasure |
|-----------|----------------|
| Cannot recall a formula | Estimate order-of-magnitude; eliminate extremes |
| Cannot see a series pattern | Parity/alternation check; flag |
| Java output unclear | Trace the first 2 lines; if uncertain at 70s, flag |
| SQL join confusing | Trace only the columns needed |
| Ambiguous English | Pick the most professional answer |
| Time anxiety itself | 3-breath reset, then step 1 |

### Recover the loss
After the stuck question, immediately do one **cheap** question — DBMS theory, a behavioural English item, or a data-sufficiency item — to restore rhythm and marks.

### Why this works
The procedure converts an open-ended "solve it" into a bounded sequence with a guaranteed exit (flag and move). Bounded steps stop the rumination loop; the cheap question afterwards restores both confidence and pace.

## Worked example
**Rahul stuck on a two-table SQL query at minute 55.**

- **40 seconds in**, he cannot decide the join order.
- **Step 1:** he re-reads the stem — it asks for rows where `city = 'Pune'`.
- **Step 2:** he eliminates two options that ignore the `WHERE`.
- **Step 3:** he estimates that only option C counts city-filtered rows.
- **Step 4:** he flags C and moves.
- **Step 5:** at minute 82 he returns, traces a 3-row example, and confirms C.

**Net:** one mark earned, no rhythm lost. Immediately after, he answers an ACID question to reset.

### Counterfactual
Had Rahul restarted from scratch at 40 seconds, he might have spent 2.5 minutes and still guessed — losing the two easier Java questions he did instead. The procedure saved roughly 100 seconds, about one question of time.

## Quick rules
- **Re-read the stem first.**
- **Eliminate before estimating.**
- **Estimate beats staring.**
- **Flag and move.**
- **Do one cheap question right after.**
- **Return only with surplus time.**

## Common traps
- **Re-reading options instead of the stem.**
- **Restarting from scratch mid-question.**
- **Not flagging**, so the question is lost entirely.
- **Skipping the rhythm-restoring cheap question.**

## Checklist
- [ ] You know the 5-step procedure.
- [ ] You know your stuck-type countermeasure.
- [ ] You always flag before moving.
- [ ] You do a cheap question immediately after.
- [ ] You return only with surplus time.
- [ ] You never restart a question mid-way.

## Related
- [01-flagging-and-review-strategy.md](01-flagging-and-review-strategy.md)
- [../01-concepts/02-test-day-mindset.md](../01-concepts/02-test-day-mindset.md)
- [../04-pitfalls/01-stuck-question-traps.md](../04-pitfalls/01-stuck-question-traps.md)
