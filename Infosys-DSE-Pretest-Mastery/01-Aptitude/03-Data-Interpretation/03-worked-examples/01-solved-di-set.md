# Data Interpretation — 10 Solved Questions

> Section 1 · Aptitude · Data Interpretation · _Estimated reading time: 13 min_
> **Prerequisite:** [DI speed rules](../02-techniques/01-di-speed-rules.md)

## In one sentence

Ten DI questions across bar, pie, table and line charts — each one reduced to **two numbers and one
calculation**.

## Why the pre-test tests this

- DI is 1–2 questions of the 10-question aptitude section, and a single data set can feed questions
  you will meet again later in the paper.
- The questions below cover every archetype you will see: direct read, chart-gives-%-asks-count,
  missing value, percentage growth, ratio, approximation, trend and change-effect.
- Total time for this set: 13 minutes, about 78 seconds each. That is the standard you need.

## Core concept

Before you start, fix the four datasets below. Every question in the pre-test version of this set
uses one of them.

### Dataset A — Pie chart: stream preference of 800 applicants

| Stream | Share of applicants | Count |
|---|---|---|
| Java + Angular | 30% | 240 |
| .NET + Azure | 20% | 160 |
| Data Engineering | 20% | 160 |
| UI Stack | 20% | 160 |
| Data Science | 10% | 80 |
| **Total** | **100%** | **800** |

### Dataset B — Bar chart: source of application (total 800 applicants)

| Source | Share | Count |
|---|---|---|
| Campus drive | 40% | 320 |
| Referral | 30% | 240 |
| Naukri | 20% | 160 |
| Direct walk-in | 10% | 80 |
| **Total** | **100%** | **800** |

### Dataset C — Table: module sales (₹ in thousands)

| Month | Module A | Module B | Module C | Total |
|---|---|---|---|---|
| April | 40 | 30 | 20 | 90 |
| May | 50 | 40 | 30 | 120 |
| June | 60 | 45 | 35 | 140 |
| July | 70 | 50 | 40 | 160 |
| **Total** | **220** | **165** | **125** | **510** |

### Dataset D — Line graph: monthly attrition rate at one site (%)

| Month | Jan | Feb | Mar | Apr | May | Jun |
|---|---|---|---|---|---|---|
| Attrition % | 8 | 7 | 9 | 6 | 5 | 4 |

## Worked example

### Q1 — Answer **A** (bar chart, direct read)

**Using Dataset B: how many applicants registered through the referral programme?**

A. 240
B. 320
C. 160
D. 80

**Solution**: Referral = 30% of 800 = **240**.

**Answer: A (240).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 320 | The campus drive bar — the tallest bar, and the classic wrong pick |
| 160 | The Naukri bar |
| 80 | The direct walk-in bar |

---

### Q2 — Answer **A** (pie chart, share of total)

**Using Dataset A: what percentage of applicants opted for Data Science?**

A. 10%
B. 12.5%
C. 20%
D. 16%

**Solution**: The Data Science slice is labelled 10%. (Equivalently 80 of 800 = 10%.)

**Answer: A (10%).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 12.5% | 80/640 or a mis-read of the smallest slice |
| 20% | One of the three equal middle slices — the most common mis-pick |
| 16% | 80/500 — divided by a number that is not the total |

---

### Q3 — Answer **B** (chart gives %, question asks count)

**Using Dataset B: how many applicants came through Naukri?**

A. 120
B. 160
C. 200
D. 240

**Solution**: Naukri = 20% of 800 = **160**.

**Answer: B (160).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 120 | 20% of 600, or 15% of 800 — wrong base |
| 200 | The bare "20" from the chart, read as a count |
| 240 | The referral count |

---

### Q4 — Answer **A** (missing value in a table)

**Using Dataset C: if the table did not print Module B's June value, what would it be?**

A. 45
B. 40
C. 50
D. 35

**Solution**

```
June total = 140
June Module B = 140 − 60 (A) − 35 (C) = 45
```

**Answer: A (45).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 40 | Module B's May value |
| 50 | Module B's July value |
| 35 | Module C's June value — subtracted but not restored |

---

### Q5 — Answer **A** (percentage growth, base = old value)

**Using Dataset C: by what percentage did Module A's sales grow from April to July?**

A. 75%
B. 50%
C. 70%
D. 43.75%

**Solution**

```
Growth = 70 − 40 = 30
Base (April) = 40
% growth = 30/40 × 100 = 75%
```

**Answer: A (75%).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 50% | 30/60 — used June's value as the base |
| 70% | The July value read as a percentage |
| 43.75% | 30/68.6 — or 30/70 = 42.86% rounded oddly; in any case the wrong base |

---

### Q6 — Answer **A** (ratio, simplified into parts)

**Using Dataset C: in July, what was the ratio of Module A's sales to Module C's sales?**

A. 7 : 4
B. 4 : 7
C. 3 : 2
D. 7 : 5

**Solution**: 70 : 40 → divide both by 10 → **7 : 4**.

**Answer: A (7 : 4).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 4 : 7 | The ratio reversed — read A : C backwards |
| 3 : 2 | Used April's values (40 : 30 is 4 : 3; 60 : 40 is 3 : 2) |
| 7 : 5 | Compared Module A (70) with Module B (50) |

---

### Q7 — Answer **C** (approximate, combined pie slices)

**Using Dataset A: approximately how many applicants opted for a stream other than Java + Angular?**

A. 400
B. 480
C. 560
D. 600

**Solution**: Java + Angular = 30%, so the rest = 70%. 70% of 800 = **560**.

**Answer: C (560).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 400 | 50% of 800 — Java + .NET only |
| 480 | 60% of 800 — counted UI Stack as Java |
| 600 | 75% of 800 — off by one slice |

---

### Q8 — Answer **A** (average over a line chart)

**Using Dataset D: what was the average attrition rate over the six months?**

A. 6.5%
B. 6%
C. 7%
D. 6.75%

**Solution**

```
Total = 8 + 7 + 9 + 6 + 5 + 4 = 39
Average = 39 / 6 = 6.5%
```

**Answer: A (6.5%).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 6% | 36/6 — dropped the March value of 9 |
| 7% | 42/6 — added a value that is not on the chart |
| 6.75% | 40.5/6 — an arithmetic slip on the sum |

---

### Q9 — Answer **B** (trend on a line chart)

**Using Dataset D: in which month did the attrition rate fall the most compared with the previous
month?**

A. February
B. April
C. May
D. June

**Solution**: Compare consecutive gaps: Jan→Feb −1, Feb→Mar **+2**, Mar→Apr **−3**, Apr→May −1,
May→Jun −1. The biggest fall is **3 points, into April**.

**Answer: B (April).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| February | Fell by only 1 point |
| May | Fell by 1 point |
| June | Fell by 1 point |

**Note the trap:** February, May and June all fell. The question asks for the **largest** fall, so
"it went down" is not enough.

---

### Q10 — Answer **A** (effect of a change on a share)

**Using Dataset A: if the number of .NET + Azure applicants increased by 25%, by how many would the
total number of applicants increase?**

A. 40
B. 60
C. 200
D. 20

**Solution**: .NET + Azure = 20% of 800 = 160 applicants. 25% of 160 = **40**.

**Answer: A (40).**

**Distractors**

| Option | Why it is wrong |
|---|---|
| 60 | 25% of 240 (the Java count) |
| 200 | 25% of 800 — applied the percentage to the total |
| 20 | 25% of 80 (the Data Science count) |

## Quick rules

- Read the question, then the options, then the data.
- Find the total first.
- Chart shows %, question asks count → multiply by the total.
- Chart shows count, question asks % → divide by the total.
- Missing cell = row total − the other cells in that row.
- % change uses the old value as the base.
- Ratio → convert to parts, then simplify.
- "Biggest fall" needs the largest gap, not just any fall.
- Approximate when the options are spread; be exact when they are tight.
- Cap at 70 seconds.

## Common traps

| Trap | Seen in | Silently gives |
|---|---|---|
| Reading the wrong bar | Q1 | 320 |
| Picking a middle pie slice | Q2 | 20% |
| Treating a % as a count | Q3 | 200 |
| Subtracting without restoring the other cell | Q4 | 35 |
| Wrong base for growth | Q5 | 50% |
| Reversed ratio | Q6 | 4 : 7 |
| Double-counting slices | Q7 | 600 |
| Dropping a point when summing | Q8 | 6% |
| Any fall instead of the biggest fall | Q9 | February |
| Percentage applied to the total | Q10 | 200 |

## Checklist

- [ ] I solved all 10 in 13 minutes or less.
- [ ] I got Q7, Q9 and Q10 right — they are the ones that separate 6/10 from 9/10.
- [ ] For every wrong answer, I can name the trap from the table above.
- [ ] I found the total before computing, every single time.

## Related

- [DI question archetypes](../01-concepts/01-di-question-archetypes.md)
- [DI speed rules](../02-techniques/01-di-speed-rules.md)
- [DI traps](../04-pitfalls/01-di-traps.md)
- [DI lookup tables and revision sheet](../05-reference/01-di-lookup-tables.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
