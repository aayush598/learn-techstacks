# DI Lookup Tables and Revision Sheet

> Section 1 · Aptitude · Data Interpretation · _Estimated reading time: 4 min_
> **Prerequisite:** [DI speed rules](../02-techniques/01-di-speed-rules.md)

## In one sentence

One page of datasets, shares, unit conversions and approximation rules — everything a DI question can
need that is not arithmetic.

## Why the pre-test tests this

- DI is only 1–2 questions, but a data set can feed more than one question across the paper.
- Having the standard datasets and unit conversions printed removes the two slowest parts of a DI
  question: reading and normalising.

## Core concept

### Standard practice datasets (from the worked examples)

**A — Stream preference, 800 applicants**

| Stream | Share | Count | Fraction of total |
|---|---|---|---|
| Java + Angular | 30% | 240 | 3/10 |
| .NET + Azure | 20% | 160 | 1/5 |
| Data Engineering | 20% | 160 | 1/5 |
| UI Stack | 20% | 160 | 1/5 |
| Data Science | 10% | 80 | 1/10 |

**B — Source of application, 800 applicants**

| Source | Share | Count |
|---|---|---|
| Campus drive | 40% | 320 |
| Referral | 30% | 240 |
| Naukri | 20% | 160 |
| Direct walk-in | 10% | 80 |

**C — Module sales (₹ in thousands)**

| Month | A | B | C | Total |
|---|---|---|---|---|
| April | 40 | 30 | 20 | 90 |
| May | 50 | 40 | 30 | 120 |
| June | 60 | 45 | 35 | 140 |
| July | 70 | 50 | 40 | 160 |
| Total | 220 | 165 | 125 | 510 |

**D — Attrition % by month**

| Jan | Feb | Mar | Apr | May | Jun |
|---|---|---|---|---|---|
| 8 | 7 | 9 | 6 | 5 | 4 |

### Share-of-total quick table (total 800)

| Value | Share | Value | Share |
|---|---|---|---|
| 80 | 10% | 240 | 30% |
| 120 | 15% | 320 | 40% |
| 160 | 20% | 400 | 50% |
| 200 | 25% | 480 | 60% |

### Share-of-total quick table (total 510)

| Value | Share | Value | Share |
|---|---|---|---|
| 51 | 10% | 220 | 43.1% |
| 102 | 20% | 255 | 50% |
| 127.5 | 25% | 165 | 32.4% |
| 178.5 | 35% | 125 | 24.5% |

### Unit conversion table

| Written as | In rupees | Written as | In rupees |
|---|---|---|---|
| 1 thousand | 1,000 | 1 lakh | 1,00,000 |
| 10 thousand | 10,000 | 2 lakh | 2,00,000 |
| 100 thousand | 1,00,000 | 1 crore | 1,00,00,000 |
| 690 (₹ '000) | 6,90,000 | 6.9 lakh | 6,90,000 |
| 2.4 (₹ lakh) | 2,40,000 | 0.24 crore | 24,00,000 |

### Chart type → question type map

| Chart | Fastest question | Slowest question | Trap |
|---|---|---|---|
| Bar | Direct read of one bar | % of total | Reading the wrong bar |
| Pie | Slice % | Count from slice % | Treating % as count |
| Table | Row/column total | Missing cell | Wrong row/column |
| Line | Month of max/min | Average, biggest change | "It went down" ≠ biggest fall |

### Approximation table

| You want | Round to | Example |
|---|---|---|
| A percentage | Nearest 5% | 43.1% → 45% or 43% if offered |
| A count | Nearest 10 | 165 → 160 or 170 |
| A difference | Nearest 10 after subtracting | 165 − 125 ≈ 40 |
| Options 5 apart | Nearest 5 | 6.5 → 5 or 10 |
| Options 10 apart | Nearest 10 | 43 → 40 |

## Worked example

**Q. Using Dataset A, what percentage of applicants chose .NET + Azure, Data Engineering and UI Stack
together?**

```
Shares = 20% + 20% + 20% = 60%
```

**Answer: 60%.**

**Speed note:** you never need the count. When a question asks for a percentage of the total and the
chart is a pie, the shares add directly.

## Quick rules

- Question → options → data.
- Find the total first.
- One unit for everything.
- Row totals beat column sums.
- % of total: divide by the total. Count from %: multiply by the total.
- Missing cell = row total − the rest of the row.
- % change: old value is the base.
- Ratios: convert to parts first.
- Round when options are spread; be exact when they are tight.
- 70-second cap.

## Common traps

| Trap | Fix |
|---|---|
| Data before question | Question first |
| Unit mismatch | Normalise first |
| % read as count | Multiply by the total |
| Wrong base for % change | Old value |
| Over-precision | Round to nearest 5/10 |
| Missing cell that is not determined | Say "cannot be determined" |
| Timeout | 70-second cap |

## Checklist

- [ ] I can reproduce the four practice datasets from memory.
- [ ] I know the share-of-total tables for 800 and 510.
- [ ] I can convert thousands ↔ lakh ↔ crore in under 10 seconds.
- [ ] I always find the total before computing.
- [ ] I can name the trap for every DI question I got wrong.

## Related

- [DI question archetypes](../01-concepts/01-di-question-archetypes.md)
- [DI speed rules](../02-techniques/01-di-speed-rules.md)
- [Solved data-interpretation set](../03-worked-examples/01-solved-di-set.md)
- [DI traps](../04-pitfalls/01-di-traps.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
