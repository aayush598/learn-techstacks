# Data Interpretation — The Question Archetypes

> Section 1 · Aptitude · Data Interpretation · _Estimated reading time: 8 min_
> **Prerequisite:** [Percentages, Profit/Loss & Discount](../../02-Percentages-Profit-Loss-Discount/README.md)

## In one sentence

Data interpretation gives you a **data set** (chart or table) and asks one or two arithmetic
questions about it — so your real skill is reading the data fast, not doing advanced maths.

## Why the pre-test tests this

- The DSE pre-test's aptitude section regularly includes **1–2 DI questions**, sometimes with a shared
  data set that feeds 3–4 questions across the paper.
- DI looks like the easiest archetype (just read a chart) and is where the 90-second rule breaks
  most often: candidates re-read the whole chart four times instead of reading the *question* first.
- Every DI question reduces to a percentage, a ratio, a difference or a missing value. You already
  own the tools; the exam only tests whether you can find the right two numbers.

## Core concept

### The four chart types and what each one is best at

| Chart type | What it shows | Fastest way to read it | Typical question |
|---|---|---|---|
| **Bar / column** | Magnitude per category | Match the bar to the label, read the scale | "How many applied from X?" |
| **Pie** | Share of a total | Slice angle → % of total | "What % chose Y?" |
| **Table** | Exact values in a grid | Find the row and column, use the total row | "What is the missing value?" |
| **Line** | A quantity over time | Find the trend, the max and the min | "In which month did it peak?" |

### The five question archetypes

| # | Archetype | What it asks | The one move that solves it |
|---|---|---|---|
| 1 | **Direct read** | A value straight off the chart | Find the category, read the number |
| 2 | **Missing value** | The blank cell in a table | Subtract the knowns from the total row/column |
| 3 | **Percentage** | "What % of the total…" | Convert the value to a share of the total |
| 4 | **Ratio-based** | "What is the ratio of A to B?" | Use the ratio chain, then simplify |
| 5 | **Approximate** | "Approximately how much…" | Round to the nearest 5 or 10 and pick the closest option |

### Percentage-of-total: the workhorse

Most DI percentage questions are one line once you have the total:

```
share % = value / total × 100
```

For a total of 800: 240 → 30%, 160 → 20%, 80 → 10%. Memorise nothing; compute one and read the rest.
For a total of 510: 220 → 43.1%, 165 → 32.4%, 125 → 24.5%.

### Ratio-based DI without raw numbers

When the total is split into parts, work in **parts**, not in the numbers:

```
Java 240, .NET 160, Data Eng 160  →  divide by 80  →  3 : 2 : 2
```

Then any ratio question becomes a ratio of small integers. 240 : 160 = 3 : 2 in two seconds.

### Missing-value problems: three moves

| Move | When |
|---|---|
| Subtract the knowns from the **total row** (or column) | The total for that row/column is given |
| Cross-check with the **total column** | Two totals are given and you must verify |
| Use a printed % or ratio of the total | The table gives a percentage instead of a total |

If the table gives you **neither** a total nor a percentage, the value is not determined — that is a
data-sufficiency question, not a DI question.

### Reading a chart correctly

| Detail | Why it matters | Check |
|---|---|---|
| Axis scale | A bar of "60" could be 600 or 6 | Find the axis labels, not the bar height |
| Units | ₹ thousand vs ₹ lakh vs ₹ crore | Convert everything to one unit before comparing |
| Row vs column | Table questions hide the direction | Trace the header row and the header column |
| Time direction | Line graphs may run right-to-left | Confirm which end is the first month |
| Rounding | The chart may show 2.4 but mean 2.4 lakh | Keep the chart's own precision |

### The shared-data-set reality

In the pre-test, one data set often serves several questions:

```
   ┌──────────────────────┐
   │   One chart or table │
   └──────────┬───────────┘
              │
   ┌──────────┼──────────┬────────────┐
   ▼          ▼          ▼            ▼
 Q1: read   Q2: %     Q3: missing  Q4: ratio
 (easy)    (medium)   value        (hard)
```

**Strategy:** do the easiest question in the set first — the direct read. It costs 20 seconds, builds
your confidence with the data, and warms up the total you will need for the harder ones.

## Worked example

**The table below shows the modules sold by a training centre over four months (₹ in thousands).**

| Month | Module A | Module B | Module C | Total |
|---|---|---|---|---|
| April | 40 | 30 | 20 | 90 |
| May | 50 | 40 | 30 | 120 |
| June | 60 | 45 | 35 | 140 |
| July | 70 | 50 | 40 | 160 |
| **Total** | **220** | **165** | **125** | **510** |

**Q. What is the value of Module C in May?**

- A. 30
- B. 40
- C. 25
- D. 50

**Solution**

```
May total = 120
Module C (May) = 120 − 50 (A) − 40 (B) = 30
```

**Answer: A (30).**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| 40 | The Module B value in May — the neighbouring column |
| 25 | A subtraction slip (120 − 50 − 45, borrowing June's value) |
| 50 | The Module A value in May |

**Why this archetype is easy to lose:** the missing cell is a *May, Module C* cell, and the table
around it is full of numbers that look plausible. Trace both headers before subtracting.

## Quick rules

- **Read the question first**, then find the two numbers you need. Never read the whole chart.
- Find the **total** first — it powers 60% of DI questions.
- Convert **all units to one** before you compare or divide.
- Approximate to the nearest **5 or 10** when the options are spaced; the options tell you the
  precision.
- For ratios, work in **parts** (divide everything by a common factor) instead of raw values.
- Missing value = total − knowns. Cross-check with the other total if one exists.
- Pie chart: slice % × total = the value; value ÷ total = the slice %.
- Line graph: find the **trend** and the **extreme**, not every point.
- Do the **easiest question first** when a data set feeds several questions.
- Cap each DI question at **70 seconds**. If you have computed four things, you have misread the
  question.

## Common traps

| Trap | Symptom | Fix |
|---|---|---|
| Reading the whole chart first | 2 minutes gone, no answer | Question first, then the two numbers |
| Unit mismatch | 240 treated as 240,000 against a total of 800 | Normalise units in the first 10 seconds |
| Reading the wrong row/column | A neighbouring value | Trace headers twice |
| Treating a pie slice as a count | "30%" used as the number | Convert with the total |
| Assuming the largest slice is half | Wrong share | Read the actual angle/label |
| Using the wrong base for % change | Off by a factor | Old value is the base |
| Over-precise approximation | "43.13%" | Round to the nearest 5 or 10 |
| Missing the total row | Endless subtraction | Hunt for the total first |

## Checklist

- [ ] I read the question before I read the chart.
- [ ] I located the total (row or column) before computing anything.
- [ ] I checked the units and normalised them.
- [ ] I chose the two columns/rows by tracing the headers, not by position.
- [ ] I approximated rather than chasing exact decimals when the options are spaced.
- [ ] I finished each DI question inside 70 seconds.

## Related

- [DI speed rules](../02-techniques/01-di-speed-rules.md)
- [Solved data-interpretation set](../03-worked-examples/01-solved-di-set.md)
- [DI traps](../04-pitfalls/01-di-traps.md)
- [DI lookup tables and revision sheet](../05-reference/01-di-lookup-tables.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
