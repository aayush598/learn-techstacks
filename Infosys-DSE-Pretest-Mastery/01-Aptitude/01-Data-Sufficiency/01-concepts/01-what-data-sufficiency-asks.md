# Data Sufficiency — What the Question Is Actually Asking

> Section 1 · Aptitude · Data Sufficiency · _Estimated reading time: 6 min_
> **Prerequisite:** none

## In one sentence

A data-sufficiency question never asks you to *find* a value — it asks you to decide whether the
information given forces **exactly one** value, so the answer is a letter (A–E), never a number.

## Why the pre-test tests this

- The DSE pre-test's 10-question aptitude set regularly carries 1–2 data-sufficiency questions with
  five options (A–E). It is the cheapest point in the paper if you own the decision tree.
- It is a trap for the fast reader: the options contain tempting numbers, and candidates who hunt for
  "the answer" instead of "the judgement" lose 90 seconds and the point.
- It is the one aptitude archetype where **guessing is punished hardest** — the option letters are not
  random, they encode a logical structure you can verify.

## Core concept

### The five options and what each one claims

| Option | The claim it makes | You choose it when |
|---|---|---|
| **A** | Both statements together are sufficient; neither alone is | Each statement alone leaves 2+ possible values; together they force exactly 1 |
| **B** | Statement I alone is sufficient; Statement II alone is not | I alone forces exactly 1 value, II alone does not |
| **C** | Statement II alone is sufficient; Statement I alone is not | II alone forces exactly 1 value, I alone does not |
| **D** | Either statement alone is sufficient | Each statement alone forces exactly 1 value, **and they agree** |
| **E** | Even both statements together are not sufficient | After using I and II together you still have 2+ values, **or the two statements contradict each other** |

### Three words that decide the whole question

| Word | Operational meaning | Test |
|---|---|---|
| **Sufficient** | The information forces one and only one answer | Could two different values satisfy the same statement? If yes → not sufficient |
| **Alone** | You may use that statement *without* the other | Mentally blank out the other statement |
| **Together** | You may use both statements | Both blanks on the table |

That third row is the one candidates miss. "Statement alone is insufficient" does **not** mean the
answer is E. It means you must now ask: *does the combination succeed?* If yes → **A**. If no → **E**.

### The two official ways to land on E

Both are tested in the pre-test. Note that **D requires agreement**.

| Situation | What happens | Answer |
|---|---|---|
| Each statement alone is sufficient but they produce **different** values | The two statements contradict; no consistent single answer exists | **E** |
| Neither statement alone nor both together connect to the quantity asked | The information is simply irrelevant or incomplete | **E** |

If a statement alone already gives the answer, you never reach the "together" test — and if it gives
a *different* answer from the other statement, the pair is self-defeating. That is E, not D.

### A statement is "insufficient" the moment two values survive

Do not test sufficiency by asking "can I do algebra with this?" Test it by asking:

> If I try to name the answer, can I name **exactly one** number, or at least two?

- `x + y = 10` — you can name (1,9), (2,8), (3,7) → insufficient.
- `x + y = 10` **and** `x − y = 4` — you can name only (7,3) → sufficient.
- `x² = 49` — you can name 7 and −7 → insufficient for "the value of x".
- `x² = 49` **and** `x > 0` — you can name only 7 → sufficient.

Two values that both fit = insufficient. Always. Even if one of them "looks more likely".

## Worked example

**Q. What is the value of x?**

Statement I: `x² − 5x + 6 = 0`
Statement II: `x > 2`

- A. Both statements together are sufficient, but neither alone is.
- B. Statement I alone is sufficient, but Statement II alone is not.
- C. Statement II alone is sufficient, but Statement I alone is not.
- D. Either statement alone is sufficient.
- E. Even both statements together are not sufficient.

**Step 1 — Statement I alone.** `x² − 5x + 6 = (x − 2)(x − 3) = 0`, so `x = 2` **or** `x = 3`.
Two values survive → **I alone is not sufficient.** (B and C are dead.)

**Step 2 — Statement II alone.** `x > 2` allows x = 3, 4, 5, 100 … → **II alone is not sufficient.**
(C is dead.)

**Step 3 — Together.** The only root of the quadratic that is also greater than 2 is `x = 3`.
Exactly one value survives → both statements together are sufficient, neither alone is.

**Answer: A.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| B | I alone leaves x = 2 or x = 3 — two answers, so I alone does not settle it |
| C | II alone is just "x is greater than 2"; it never pins x down |
| D | Neither statement alone works, so "either alone" is false |
| E | Together they do settle x = 3, so "even both together" is false |

## Quick rules

- Read the **stem first**. The stem tells you *which quantity* must be unique. Knowing you need
  "the value of x" and not "the value of x − y" saves a step.
- Never solve for the answer value. You need one *test value* per statement, and the fastest test is
  "can I name a second value that also works?"
- "Alone" means alone. Blank the other statement out and check.
- Each statement alone insufficient → check together → **A** if together works, **E** if not.
- Each statement alone sufficient → compare the two answers. Same → **D**. Different → **E**.
- If any option could ever be true, it is not the answer. Pick the option that is true *every time*.
- The answer to a data-sufficiency question is a **letter**. If you are calculating a number at the
  90-second mark, you have already lost the question.

## Common traps

| Trap | What it looks like | What to do |
|---|---|---|
| **Solving instead of judging** | You compute x = 3, feel good, and hunt for the option that says 3 | There is no numeric option. Re-read the stem; you need the *letter* |
| **"I need II's total"** | Statement II says "60% of the mixture is water" and you think it is enough because 60% is a number | Check what II is a percentage **of**. If the base is missing, II alone is insufficient |
| **Assuming a statement must be "good enough" to be true** | You decide a statement is useless because it does not mention x | A statement can be sufficient indirectly (e.g. "x > 2" combined with a quadratic) |
| **Ignoring the "different answers" case** | Both statements give you a number, so you pick D | If the two numbers differ, the pair is contradictory → **E**, never D |
| **Confusing E with A** | "Each statement alone is insufficient" → you jump to E | E requires that even **together** it fails. Together succeeding = **A** |

## Checklist

- [ ] I read the stem first and know exactly which quantity must be unique.
- [ ] I tested Statement I alone and said out loud "unique" or "not unique".
- [ ] I tested Statement II alone the same way.
- [ ] If neither alone worked, I explicitly tested them together before choosing A or E.
- [ ] If both alone worked, I checked whether the two answers **agree** (D) or **differ** (E).
- [ ] I did not compute a final numeric answer — I selected a letter.

## Related

- [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)
- [8 solved data-sufficiency questions](../03-worked-examples/01-solved-data-sufficiency-set.md)
- [Data-sufficiency traps](../04-pitfalls/01-data-sufficiency-traps.md)
- [Data-sufficiency one-pager](../05-reference/01-data-sufficiency-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
