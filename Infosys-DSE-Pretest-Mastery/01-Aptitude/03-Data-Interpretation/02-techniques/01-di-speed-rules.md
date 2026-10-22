# DI Speed Rules — Read Less, Compute Less, Answer More

> Section 1 · Aptitude · Data Interpretation · _Estimated reading time: 7 min_
> **Prerequisite:** [DI question archetypes](../01-concepts/01-di-question-archetypes.md)

## In one sentence

Ten fixed rules turn a chart into two numbers and a one-line calculation — the whole point of DI is
**selection speed**, not arithmetic speed.

## Why the pre-test tests this

- DI is the archetype where the 90-second rule is most often broken, because it *feels* like reading
  rather than solving.
- Rahul's weakness: he reads every number on the chart "to be safe". Meera's weakness: she panics at
  the first unfamiliar chart and forgets to find the total.
- The rules below are mechanical on purpose. Mechanics survive pressure; intuition does not.

## Core concept

### The ten rules

| # | Rule | How to apply it | Saves |
|---|---|---|---|
| 1 | **Question first** | Read the stem, then name the two numbers you need | ~30 s |
| 2 | **Total first** | Find the total row/column before any calculation | ~20 s |
| 3 | **One unit** | Convert ₹ thousand / lakh / crore to a single unit | Errors |
| 4 | **Trace the headers twice** | Row header down, column header across, before reading | Errors |
| 5 | **Nearest 5 or 10** | If the options are 5–10 apart, round and pick the closest | ~20 s |
| 6 | **Options set the precision** | Look at the options first: are they tight (exact) or spread (approximate)? | ~15 s |
| 7 | **Parts, not numbers** | For ratios, divide all values by a common factor | ~20 s |
| 8 | **Trend, not points** | On a line graph, find max, min and direction | ~25 s |
| 9 | **Easiest first** | When one data set feeds several questions, bank the direct read | Marks |
| 10 | **70-second cap** | Over 70 s → you misread the question; re-read the stem | Marks |

### Rule 6 in detail — read the options before the chart

| Option spacing | What it tells you | What you do |
|---|---|---|
| 10.4%, 20.8%, 31.2% | Exact computation expected | Compute precisely |
| 10%, 20%, 30% | Rounded answer expected | Estimate to the nearest 5 or 10 |
| 300, 320, 340, 360 | You are close; check the base | Compute, then sanity check |
| 240, 960, 1200, 1440 | Wide spread | Estimate from the chart, no precision needed |

This one rule alone tells you how much work to do — and it is why "read the options first" beats
"read the chart first".

### Rule 7 in detail — the ratio chain

For a pie chart or a split table, convert to parts once:

```
Total 800:  240 | 160 | 160 | 160 | 80
Divide by 80:  3  |  2  |  2  |  2  | 1
```

Now every ratio question is a ratio of small integers:
- Java : .NET = 3 : 2
- Java + .NET : rest = 5 : 3
- Data Science : total = 1 : 10 → 10%

### Rule 8 in detail — line graph reading

| You need | You do this |
|---|---|
| The month with the highest value | Scan for the highest point |
| The month with the lowest value | Scan for the lowest point |
| Total increase over the period | Last value − first value |
| Biggest single-month change | Compare consecutive gaps |
| Average over n months | Add the values, divide by n |

Do not read every point unless the question literally asks for every point.

### Approximation rules for a 70-second DI

| Situation | Rule | Example |
|---|---|---|
| "Approximately what % of the total?" | Take the fraction of the total by eye, round to nearest 5 | 240/800 ≈ 30% |
| "Approximately how many?" | Round the value to the nearest 10 or to the nearest option | 165 ≈ 160 or 170 |
| "Approximately how much more?" | Subtract after rounding | 165 − 125 ≈ 40 |
| Options 5 apart | Round to the nearest 5 | 6.5% → 6.5 (if offered) else 6 or 7 |
| Options 10 apart | Round to the nearest 10 | 43% → 40% |

## Worked example

**The pie chart shows how 800 applicants chose a stream:**

| Stream | Share |
|---|---|
| Java + Angular | 30% |
| .NET + Azure | 20% |
| Data Engineering | 20% |
| UI Stack | 20% |
| Data Science | 10% |

**Q. Approximately how many applicants opted for Java + Angular or .NET + Azure together?**

A. 300
B. 320
C. 400
D. 480

**Step 1 — Read the options.** They are 40–80 apart → this is an estimate question, so no precision
needed.

**Step 2 — Combine the shares.** 30% + 20% = **50%**.

**Step 3 — Apply to the total.** 50% of 800 = **400**. Even by eye, half of 800 is 400.

**Answer: C (400).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 300 | Applied 30% + 20% as 30% of 800 + 20% of 800 with a units slip (240 + 20) |
| 320 | Took 40% of 800 — the two shares are 30% and 20%, so 50%, not 40% |
| 480 | Used 60% — counted Java + .NET + UI by mistake |

**Time: 35 seconds.** The whole calculation is one addition and one halving.

**Second example — table with a missing cell.** From the module table (total 510 for four months):
"Module B's sales grew from 30 in April to 50 in July. What is the percentage increase?" →
(50 − 30)/30 × 100 = 66.67%. Options: 66.67%, 50%, 20%, 40% → **66.67%**. The base is April (the old
value), which is the one rule that decides this archetype.

## Quick rules

- Question → options → data. Never data first.
- Find the total before anything else.
- Normalise the units in the first 10 seconds.
- Approximate to the nearest 5 or 10 when the options are spread.
- Convert to **parts** before any ratio question.
- Missing value = total − knowns; cross-check with the second total.
- Line graph: max, min, trend, endpoints — not every point.
- Bank the easiest question in a shared data set first.
- Hard-cap at 70 seconds per DI question.

## Common traps

| Trap | Signal | Fix |
|---|---|---|
| Reading the chart before the question | You have read numbers you do not need | Question first |
| Unit mismatch | 240 vs 800 | One-unit rule |
| Precision chasing | 15 seconds on 43.137% | Round |
| Ratio from raw numbers | 240:160 | Divide by 80 first |
| Missing the total | Two minutes of subtraction | Total first |
| Re-reading a chart 4 times | Clock pressure | Name the two numbers, then compute once |
| Treating DI as the "easy" question and moving on later | You come back with 20 s left | Do DI while you still have time |

## Checklist

- [ ] I read the question and the options before the chart.
- [ ] I found the total first.
- [ ] I normalised units.
- [ ] I converted to parts for any ratio question.
- [ ] I rounded instead of chasing decimals when the options were spread.
- [ ] I capped each DI question at 70 seconds.

## Related

- [DI question archetypes](../01-concepts/01-di-question-archetypes.md)
- [Solved data-interpretation set](../03-worked-examples/01-solved-di-set.md)
- [DI traps](../04-pitfalls/01-di-traps.md)
- [DI lookup tables and revision sheet](../05-reference/01-di-lookup-tables.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
