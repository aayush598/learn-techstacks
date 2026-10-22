# Data Sufficiency — 8 Solved Questions

> Section 1 · Aptitude · Data Sufficiency · _Estimated reading time: 12 min_
> **Prerequisite:** [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)

## In one sentence

Every data-sufficiency answer reduces to a **branch of one decision tree**, so you should be able to
say *why* an option is right, not just *which* one is.

## Why the pre-test tests this

- The pre-test's aptitude section is 10 questions. If 2 of them are data-sufficiency, 2 marks ride on
  a 60-second decision each.
- Each of the 8 questions below covers one branch: A, B, C, D, E-by-contradiction, E-by-no-link,
  and two A cases that hide a shared quantity.
- Read the reasoning for the option you got wrong. That is the actual study.

## Core concept

The answer letter is fully determined by three binary facts:

| Statement I alone | Statement II alone | Together | Answer |
|---|---|---|---|
| Unique | Not unique | — | **B** |
| Not unique | Unique | — | **C** |
| Unique | Unique | Same value | **D** |
| Unique | Unique | Different values | **E** |
| Not unique | Not unique | Unique | **A** |
| Not unique | Not unique | Not unique | **E** |

That table is the entire topic. The 8 worked examples below are just the table in disguise.

## Worked example

### Q1 — Answer **A** (both together, neither alone)

**What is the value of x?**

Statement I: `x² − 5x + 6 = 0`
Statement II: `x > 2`

A. Both statements together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**Solution**

| Step | Test | Result |
|---|---|---|
| 1 | I alone: `(x−2)(x−3)=0` → x = 2 or x = 3 | Two values → not sufficient |
| 2 | II alone: x > 2 → 3, 4, 5 … | Not sufficient |
| 3 | Together: only root > 2 is x = 3 | Unique → **A** |

**Distractors**

- B / C: each statement alone leaves the value open.
- D: neither statement works alone.
- E: together they do work — the quadratic gives only two candidates and II removes one.

---

### Q2 — Answer **B** (Statement I alone; II silently needs I)

**How many litres of milk are in the mixture?**

Statement I: The mixture contains milk and water in the ratio 3 : 2, and the total mixture is 25 litres.
Statement II: Water constitutes 40% of the mixture.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both together are not sufficient.

**Solution**

- **I alone:** total 25 litres in 3 : 2 → 5 parts → 1 part = 5 litres → milk = 3 × 5 = **15 litres**.
  Exactly one value → I alone is sufficient.
- **II alone:** "water is 40% of the mixture" — but the *size* of the mixture is unknown. 40% of what?
  Not sufficient.
- Together: 40% water ⇒ 60% milk ⇒ 0.6 × 25 = 15 litres. Consistent with I.

**Answer: B.**

**Distractors**

- C: II has no base quantity of its own — it is a percentage of an unknown total.
- D: II alone does not work.
- A: I alone already works, so "neither alone" is false.
- E: Both together give 15 litres.

---

### Q3 — Answer **C** (Statement II alone; I is a decoy)

**What was the total amount Meera paid for the meal?**

Statement I: Meera ordered a biryani and a cold drink, and the biryani cost ₹180.
Statement II: The cold drink cost ₹40, and the total bill including 5% GST was ₹231.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both together are not sufficient.

**Solution**

- **I alone:** biryani ₹180, but the drink's price is unknown → total unknown. Not sufficient.
- **II alone:** the total bill is stated as ₹231 → exactly one value → sufficient.

**Answer: C.**

**Distractors**

- A / B: I never names the total, so it can never be "sufficient" for this stem.
- D: I alone is not sufficient.
- E: II alone names the answer directly.

---

### Q4 — Answer **D** (each alone, and they agree)

**How many litres of acid are in 30 litres of the mixture?**

Statement I: The mixture is 20% acid and 80% water.
Statement II: In the 30 litres of mixture, the water is 24 litres.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**Solution**

- **I alone:** 20% of 30 litres = **6 litres of acid** → unique → sufficient.
- **II alone:** water = 24 of 30 litres → acid = 30 − 24 = **6 litres** → unique → sufficient.
- The two agree (6 = 6), so there is no contradiction.

**Answer: D.**

**Distractors**

- A: Both statements work on their own, so "neither alone" is false.
- B / C: each statement alone *is* sufficient, so both are false.
- E: They agree, so together they are certainly sufficient.

---

### Q5 — Answer **E** (each alone sufficient, but they contradict)

**How many aptitude questions did Ananya answer correctly?**

Statement I: Ananya answered 8 of the 10 aptitude questions correctly.
Statement II: Ananya scored 6 marks out of 10 in the aptitude section, where every question carried
exactly 1 mark.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**Solution**

- **I alone:** 8 correct → sufficient.
- **II alone:** 6 marks at 1 mark each → 6 correct → sufficient.
- **Together:** I says 8, II says 6. The two statements cannot both be true. There is no consistent
  single answer.

**Answer: E.** (D would need the two answers to agree.)

**Distractors**

- B / C: each statement *is* sufficient alone, so both are false.
- D: the classic lure — both statements "give a number", but they give *different* numbers.
- A: neither alone is false too; they each work alone.

---

### Q6 — Answer **E** (the information never connects)

**What was Rahul's average speed on the Mumbai–Pune trip?**

Statement I: The distance covered was 150 km.
Statement II: The car consumed 12 litres of diesel on the trip.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**Solution**

- Speed = distance ÷ time. I gives distance, II gives fuel. **No time is available anywhere.**
- I alone: no time → insufficient. II alone: no distance, no time → insufficient. Together: still
  no time → insufficient.

**Answer: E.**

**Distractors**

- A: Together still lacks time, so this is the tempting wrong answer.
- B / C: neither statement mentions speed.
- D: Neither works alone.

**Why this matters:** "even both together" literally means *the pair of statements together* still does
not determine the answer. Missing link, not missing arithmetic.

---

### Q7 — Answer **A** (each statement contributes one missing piece)

**How many days did Karthik work during July 2025?**

Statement I: Karthik worked on every day of July except the 4 Sundays.
Statement II: July 2025 has 31 days.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**Solution**

- **I alone:** "every day of July except 4 Sundays" → days worked = (days in July) − 4. The month
  length is not stated → insufficient.
- **II alone:** 31 days, but no information about Sundays → insufficient.
- **Together:** 31 − 4 = **27 days** → unique → sufficient.

**Answer: A.**

**Distractors**

- B: I needs the month length.
- C: II needs the number of non-working days.
- D: Neither alone works.
- E: Together they work.

---

### Q8 — Answer **A** (a two-step undo)

**How many sweets were originally in the box?**

Statement I: Rahul ate 12 sweets and then ate half of what remained.
Statement II: Meera counted the sweets left in the box and found 9.

A. Both together are sufficient; neither alone is.
B. Statement I alone is sufficient; Statement II alone is not.
C. Statement II alone is sufficient; Statement I alone is not.
D. Either statement alone is sufficient.
E. Even both statements together are not sufficient.

**Solution**

- **I alone:** remaining = (N − 12) ÷ 2 → N unknown → insufficient.
- **II alone:** 9 sweets remain, but the original count is unknown → insufficient.
- **Together:** (N − 12) ÷ 2 = 9 → N − 12 = 18 → N = **30** → unique → sufficient.

**Answer: A.**

**Distractors**

- B: I alone only gives a formula, not a number.
- C: II alone gives the *remaining*, not the *original*.
- D / E: Together they do work.

## Quick rules

- Judge each statement on **uniqueness**, not on difficulty.
- If a statement states the answer outright (Q3, Q4), that statement alone is sufficient.
- If a statement states a percentage or a ratio, check that its **base** is also given (Q2).
- Contradiction between the two statements is answer **E**, even though both "look sufficient" (Q5).
- Missing link (distance without time) is answer **E** (Q6).
- Two statements each carrying half the needed facts is answer **A** (Q7, Q8).

## Common traps

| Trap | Seen in | Fix |
|---|---|---|
| Assuming a formula means sufficiency | Q2, Q7 | Ask "can I name one number?" |
| Reading "before noon" as a value | Q1 | A bound is not a value |
| Choosing D when the two answers differ | Q5 | D requires agreement |
| Forgetting to run the together-test | Q1, Q7, Q8 | Neither-alone ⇒ test together before answering E |
| Believing "both together" means "add more arithmetic" | Q6 | Together cannot create missing information |

## Checklist

- [ ] I can state, for each of the 8 questions, which branch of the decision tree produced the answer.
- [ ] I got Q5 right (contradiction → E) without hesitating.
- [ ] I got Q6 right (no link → E).
- [ ] I can explain why Q2 is B and not C.
- [ ] I finished all 8 inside 12 minutes (≈ 90 s each).

## Related

- [What data sufficiency asks](../01-concepts/01-what-data-sufficiency-asks.md)
- [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)
- [Data-sufficiency traps](../04-pitfalls/01-data-sufficiency-traps.md)
- [Data-sufficiency one-pager](../05-reference/01-data-sufficiency-one-pager.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
