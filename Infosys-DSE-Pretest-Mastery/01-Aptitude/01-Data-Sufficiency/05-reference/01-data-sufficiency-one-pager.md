# Data Sufficiency — One-Page Revision Sheet

> Section 1 · Aptitude · Data Sufficiency · _Estimated reading time: 4 min_
> **Prerequisite:** [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)

## In one sentence

Print this page, and the whole topic collapses to **one table and one rule**: test I alone, test II
alone, test together, and make sure the two values agree before you say D.

## Why the pre-test tests this

- Data sufficiency is worth 1–2 marks in a 10-question section and needs no formulas.
- This page is the entire revision surface for the topic. If you can redo the decision table from
  memory, you are ready.

## Core concept

### The decision table (memorise this)

| I alone | II alone | Together | Answer |
|---|---|---|---|
| Unique | Not unique | — | **B** |
| Not unique | Unique | — | **C** |
| Unique | Unique | Same value | **D** |
| Unique | Unique | Different values | **E** |
| Not unique | Not unique | Unique | **A** |
| Not unique | Not unique | Not unique | **E** |

### Option glossary

| Option | Exact claim |
|---|---|
| A | Both statements together are sufficient, but neither alone is |
| B | Statement I alone is sufficient, but Statement II alone is not |
| C | Statement II alone is sufficient, but Statement I alone is not |
| D | Either statement alone is sufficient |
| E | Even both statements together are not sufficient |

### Three probes for "is this statement sufficient?"

| Probe | Ask yourself | If yes → |
|---|---|---|
| Counterexample | Can I name a second value that also fits? | Not sufficient |
| Free variable | Is any unknown left unconstrained? | Not sufficient |
| Direct statement | Does the statement literally state the answer? | Sufficient |

### Time budget for one DS question

| Phase | Seconds | Action |
|---|---|---|
| Read stem | 10 | Name the quantity that must be unique |
| Test I alone | 10 | One counterexample probe |
| Test II alone | 10 | One counterexample probe |
| Together test (if needed) | 10 | Combine, look for a single value |
| Compare values (if both work) | 5 | Agree → D, differ → E |
| Read options, mark | 15 | Pick the letter |
| **Total** | **~60** | Leave 30 s of slack inside the 90-second rule |

## Worked example

**Q. What is the value of n?**

Statement I: `n² + 3n = 18`
Statement II: `n > 2`

- I alone: `n² + 3n − 18 = 0` → `(n+6)(n−3) = 0` → n = 3 or n = −6 → two values → not sufficient.
- II alone: n > 2 → many values → not sufficient.
- Together: the only root > 2 is n = 3 → unique → **A**.

**Answer: A.** (Practice the table on this one: it is the same shape as Q1 in the solved set.)

## Quick rules

- **Answer with a letter.** No DS option contains a number.
- "Alone" = without the other statement.
- Sufficient = exactly one possible value.
- Both-alone-sufficient + agreement → **D**; + disagreement → **E**.
- Neither-alone → together-test → **A** or **E**.
- Percentage/ratio needs a base in the same statement to work alone.
- Contradiction between statements → **E**.
- Missing link (no time for a speed question) → **E**.

## Common traps

| Trap | Fix |
|---|---|
| Choosing the numeric-looking option | Re-read the stem; find the letter |
| Treating "40% of the mixture" as sufficient | Find the base |
| D for a contradiction | Compare the two numbers |
| E without the together-test | Combine and look again |
| 3 minutes on one DS question | Hard-cap at 60 s |

## Checklist

- [ ] I can recite the decision table without looking.
- [ ] I can recite all five option claims word for word.
- [ ] I know that D requires agreement and E covers contradiction.
- [ ] I know the time budget: 60 seconds, 5 phases.
- [ ] I can explain why "each alone insufficient" does not automatically mean E.

## Related

- [What data sufficiency asks](../01-concepts/01-what-data-sufficiency-asks.md)
- [The 5-option decision procedure](../02-techniques/01-five-option-decision-procedure.md)
- [8 solved data-sufficiency questions](../03-worked-examples/01-solved-data-sufficiency-set.md)
- [Data-sufficiency traps](../04-pitfalls/01-data-sufficiency-traps.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
