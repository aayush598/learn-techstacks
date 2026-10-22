# The 5-Option Decision Procedure — A 60-Second Algorithm

> Section 1 · Aptitude · Data Sufficiency · _Estimated reading time: 6 min_
> **Prerequisite:** [What data sufficiency asks](../01-concepts/01-what-data-sufficiency-asks.md)

## In one sentence

**Test I alone → test II alone → test them together → compare answers** is a fixed four-step procedure
that turns a data-sufficiency question into a decision you can finish in 60 seconds.

## Why the pre-test tests this

- Data sufficiency is the only aptitude archetype where the answer is a *procedure*, not a computation.
  Learning the procedure is learning the whole topic.
- Under the 90-second rule, DS questions must be *fast*. Meera loses 4 minutes on DS because she tries
  to solve the numbers before deciding whether she is allowed to solve them.
- The decision tree is self-checking: if you mislabel one branch, you cannot reach the answer the
  key expects, so a wrong turn becomes visible immediately.

## Core concept

### The decision tree

```
                        ┌───────────────────────────┐
                        │ Read the STEM. Name the   │
                        │ quantity that must be     │
                        │ unique.                   │
                        └─────────────┬─────────────┘
                                      v
                    ┌──────────────────────────────────┐
                    │ TEST 1: Statement I ALONE       │
                    │ Can I name exactly ONE value?   │
                    └───┬──────────────────────┬───────┘
                      NO │                    YES │
                          v                       v
              ┌───────────────────────┐   ┌─────────────────────────┐
              │ TEST 2: Statement II  │   │ Compare I's value with  │
              │ ALONE. Unique?        │   │ II's value.            │
              └──┬────────────────┬───┘   └───────┬─────────┬───────┘
               NO │             YES │             SAME     DIFFER
                  v                v                 v         v
        ┌───────────────┐  ┌────────────┐       ┌──────┐  ┌──────┐
        │ TEST 3: BOTH  │  │ → Answer C │       │  D   │  │  E   │
        │ together.     │  │ (and B is  │       └──────┘  └──────┘
        │ Unique?       │  │  dead)     │
        └──┬─────────┬──┘  └────────────┘
         YES │       │ NO
             v       v
         ┌─────┐  ┌─────┐
         │  A  │  │  E  │
         └─────┘  └─────┘
```

### The three "counterexample" probes

A statement is insufficient the moment you can produce **one counterexample** — a second assignment
of the unknown that satisfies the statement but gives a different answer. You do not need a full
solution; you need one rival value.

| Probe | How you use it | Example |
|---|---|---|
| **Two-value probe** | Name two values that fit the statement | `x + y = 10` → (1,9) and (2,8) both fit → insufficient |
| **Free-variable probe** | If one unknown in the stem is never constrained, it is insufficient | "What is x?" with `x + y = 10` only → y floats → insufficient |
| **Contradiction probe** | If the two statements produce different values, the set is inconsistent | I → x = 8, II → x = 6 → contradiction → **E** |

### "Statement alone" traps in concrete form

Statement II is very often *almost* sufficient — it looks like it names the answer but quietly
borrows a quantity from Statement I.

| Statement I | Statement II | Stem asks | II alone sufficient? |
|---|---|---|---|
| Total mixture is 25 litres | Water is 40% of the mixture | Litres of milk | **No** — the base (25) lives in I |
| Rahul worked 3 hours per day | Total week was 30 hours | Hours on Monday | **No** — 30 h over 7 days is 4.28 h/day, contradicts I, so it does not even agree |
| Price of a pen is ₹50 | Discount was 10% | Selling price | **No** — you still need the marked price |
| 40 students in the class | Boys outnumber girls by 8 | Number of boys | **No** — two equations, two unknowns, but the *stem* asks for one, so I *is* sufficient → answer **B** |

The last row is the one to memorise: a system of two equations in two unknowns **is** sufficient even
though the stem asks for only one of them. You are allowed to use I to help you answer I's own
question.

## Worked example

**Q. What is the number of hours Karthik took to finish the UI assignment?**

Statement I: Karthik started the assignment at 9:00 a.m. and finished it before noon on the same day.
Statement II: Karthik took 2 hours and 30 minutes to finish the assignment.

- A. Both together are sufficient; neither alone is.
- B. Statement I alone is sufficient; Statement II alone is not.
- C. Statement II alone is sufficient; Statement I alone is not.
- D. Either statement alone is sufficient.
- E. Even both together are not sufficient.

**Step 1 — Statement I alone.** 9:00 a.m. to "before noon" spans 3 hours, but the finishing point is
unspecified — it could be 10:30 a.m. or 11:45 a.m. Two values survive → **I alone insufficient.**

**Step 2 — Statement II alone.** "2 hours 30 minutes" = 2.5 hours. Exactly one value → **II alone is
sufficient.** Option **C** is the candidate.

**Step 3 — Consistency check.** Does I contradict II? I says the work happened between 9:00 a.m. and
noon — a 2.5-hour task fits comfortably inside a 3-hour window. Consistent. The answer stays **C**.

**Step 4 — Rule out D.** D would need I alone to work too. It does not. Done.

**Answer: C.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| A | II alone already fixes the duration at 2.5 hours, so "neither alone" is false |
| B | I only bounds the time (9 a.m.–12 noon); it never names 2.5 hours |
| D | I alone is not sufficient, so "either alone" is false |
| E | II alone settles the answer; nothing is missing |

**Time budget for this question: 55 seconds.** Read stem (10 s) → I alone (10 s) → II alone (10 s) →
consistency check (10 s) → read options, mark (15 s). If you are still at 90 seconds, you have
overthought it.

## Quick rules

- Name the target quantity first: "the answer must be a single number for x".
- Test in the fixed order **I alone → II alone → together**. Changing the order is how candidates end
  up choosing A when B was right.
- Use counterexamples, not solutions. Two rival values = insufficient. One value = sufficient.
- A statement that looks "almost enough" usually borrows its base from the other statement → it is
  insufficient alone.
- Both alone sufficient + different values → **E**. Both alone sufficient + same value → **D**.
- Neither alone + together works → **A**. Neither alone + together fails → **E**.
- If Statement I alone works, you can stop at step 2 — but only after you have checked the two
  statements do not contradict each other, because a contradiction downgrades D to E.
- Mark the letter, move on. One DS question is worth 1 mark; the next three questions are worth 3.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| **Solving the whole system** | You spend 60 s finding x = 17 | Name one counterexample instead |
| **Ignoring the "before noon" vagueness** | You read 9 a.m.–12 noon as exactly 3 hours | "Before noon" is a bound, not a value |
| **Calling contradictions D** | Both statements "give a number" so you pick D | D requires agreement, so verify the two numbers match |
| **Skipping the together-test** | I alone fails, II alone fails, you pick E | Together may still work → A |
| **Spending 90 s on one DS question** | Clock shows 8 minutes gone on a 10-question section | DS is a 60-second archetype; the arithmetic will not pay off |

## Checklist

- [ ] I named the target quantity from the stem before reading Statement I.
- [ ] I tested I alone with a counterexample probe, not by fully solving.
- [ ] I tested II alone the same way.
- [ ] I ran the together-test whenever both single tests failed.
- [ ] I confirmed the two statements do not contradict before choosing D.
- [ ] I marked a letter and moved on inside 90 seconds.

## Related

- [What data sufficiency asks](../01-concepts/01-what-data-sufficiency-asks.md)
- [8 solved data-sufficiency questions](../03-worked-examples/01-solved-data-sufficiency-set.md)
- [Data-sufficiency traps](../04-pitfalls/01-data-sufficiency-traps.md)
- [Data-sufficiency one-pager](../05-reference/01-data-sufficiency-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
