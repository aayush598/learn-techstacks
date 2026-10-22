# DI Traps — Where the Time and the Marks Go

> Section 1 · Aptitude · Data Interpretation · _Estimated reading time: 6 min_
> **Prerequisite:** [DI speed rules](../02-techniques/01-di-speed-rules.md)

## In one sentence

The DI trap is rarely a wrong sum — it is **reading the wrong cell, using the wrong unit, or
spending 150 seconds on a question that needed 40**.

## Why the pre-test tests this

- Candidates who prepare "quant" aptitude forget that DI rewards *data hygiene*, not arithmetic.
- The most common DI failure in the pre-test is a timeout, not a mistake. Ten questions in 15 minutes
  does not allow one 4-minute DI question.
- Every trap below has a one-line preventive habit attached to it.

## Core concept

### The eight traps

| # | Trap | Why it bites | Prevention |
|---|---|---|---|
| 1 | **Reading the data before the question** | You read 12 numbers you do not need | Question first, always |
| 2 | **Unit mismatch** | ₹ thousand vs ₹ lakh vs ₹ crore | One-unit rule |
| 3 | **Wrong row / wrong column** | Adjacent cells look plausible | Trace headers twice |
| 4 | **Treating a % as a count** | "20%" used as 20 applicants | Convert with the total |
| 5 | **Wrong base for % change** | The result is off by a factor | Old value is the base |
| 6 | **Over-precision** | You chase 43.137% | Round to the nearest 5 or 10 |
| 7 | **Missing-value without a total** | The value is not determined | Check the total row/column first |
| 8 | **The 4-minute DI question** | You lose three other questions | 70-second cap |

### Trap 2 in detail — the unit trap

Indian charts love units. A single DI set may show:

| Written as | Means | In single units |
|---|---|---|
| 240 (₹ '000) | ₹2,40,000 | 240,000 |
| 2.4 lakh | ₹2,40,000 | 240,000 |
| 0.24 crore | ₹24,00,000 | 2,400,000 |

Converting everything to a single unit takes 10 seconds. Not converting takes one wrong answer.

### Trap 7 in detail — when a missing value is NOT missing

If a table cell is blank and the row total, column total and grand total are all present, the cell is
determined **only if the row and column totals are consistent**. If the row total is missing but the
column total and grand total exist, the cell is determined too. If neither a total nor a percentage
pins it down, the question is really a data-sufficiency question and the correct response is
"cannot be determined".

## Worked example

**The table shows sales of three modules (₹ in thousands):**

| Month | Module A | Module B | Module C | Total |
|---|---|---|---|---|
| April | 40 | 30 | 20 | 90 |
| May | 50 | 40 | 30 | 120 |
| June | 60 | 45 | 35 | 140 |
| July | 70 | 50 | 40 | 160 |
| **Total** | **220** | **165** | **125** | **510** |

**Q. What was the total number of units sold across all modules in April and May together?**

A. 200
B. 210
C. 220
D. 190

**Traps in this question**

| Trap | Where it shows up |
|---|---|
| Adding the wrong cells | Option D (90 + 100) uses a May figure that does not exist |
| Adding across the wrong direction | Option C (220) is the four-month Module A total |
| Reading "April and May" as "April only" | Option A |

**Correct reasoning**: April total = 90, May total = 120. 90 + 120 = **210**.

**Answer: B (210).**

**The habit this question rewards:** read the *stem* to see which rows you need (April, May), then
take the **row totals** directly. You do not need to touch Module A, B or C at all. Candidates who
added the three modules in each month got 90 + 120 by luck — but candidates who added the three
module columns got 220, which is option C.

**Second example — the unit trap.**

**Q. A bar chart shows departmental training spend in ₹ thousands: Java 240, .NET 180, Data
Engineering 150, UI Stack 120. The question asks for the total spend in rupees. What is it?**

Total = 240 + 180 + 150 + 120 = 690 thousand = **₹6,90,000**. If an option says "690", that option
means "₹ in thousands". Read the unit in the question, not just in the chart.

## Quick rules

- Question first, options second, data third.
- Normalise units before you compare or divide.
- Row total + row total is faster than summing columns.
- A % in the chart is not a count; a count in the chart is not a %.
- % change divides by the old value.
- If the options are 5 or 10 apart, the answer is approximate — stop chasing decimals.
- A blank cell with no total and no percentage cannot be determined.
- 70-second cap, no exceptions.

## Common traps

| Trap | Your likely wrong answer | Right answer |
|---|---|---|
| Read the chart first | wasted 60 s | question first |
| Unit mismatch | 690 | 6,90,000 (if the question says rupees) |
| Wrong column | 220 | 210 |
| % read as count | 20 | 160 |
| Wrong base for growth | 50% | 75% |
| Over-precision | 43.137% | 43% |
| Sought a missing cell that is not determined | a number | "cannot be determined" |
| 4 minutes on one DI question | 1 mark | 3 marks you would have scored |

## Checklist

- [ ] I read the stem and the options before the chart.
- [ ] I checked the unit in the chart and in the question.
- [ ] I used the row/column totals whenever the stem allowed it.
- [ ] I converted % to counts and counts to % only with the total in hand.
- [ ] I rounded when the options were spread.
- [ ] I stayed under 70 seconds on every DI question in a 10-question drill.

## Related

- [DI question archetypes](../01-concepts/01-di-question-archetypes.md)
- [DI speed rules](../02-techniques/01-di-speed-rules.md)
- [Solved data-interpretation set](../03-worked-examples/01-solved-di-set.md)
- [DI lookup tables and revision sheet](../05-reference/01-di-lookup-tables.md)
- [Topic overview](../README.md)
- [Aptitude section index](../../README.md)
