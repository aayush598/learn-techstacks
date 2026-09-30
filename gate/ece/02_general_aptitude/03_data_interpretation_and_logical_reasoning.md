# General Aptitude — Part 3: Data Interpretation & Logical Reasoning

> Part 3 of 5 of the GATE ECE General Aptitude question bank · Questions 1–230 of this file
> Read this file top to bottom, in order. It continues from
> `02_geometry_and_mensuration.md` and is followed by
> `04_verbal_ability_and_comprehension.md`.

**Other four parts of this subject:** `01_quantitative_aptitude.md` (percentages, ratio,
average, algebra and the number system), `02_geometry_and_mensuration.md` (mensuration,
triangles, circles, polygons), `04_verbal_ability_and_comprehension.md` (reading
comprehension, vocabulary, sentence completion) and `05_mixed_timed_drills.md` (mixed
timed test sheets that mix all of the above).

**Covers:** reading and interpreting tables, bar/line/pie charts, frequency distributions
and grouped data, data comparison and ranking, Venn diagrams, categorical syllogisms,
blood relations, direction sense, coding–decoding, series completion, statement–
conclusion and statement–assumption, and logical connectives with truth tables.

**Assumes:** only ordinary arithmetic — addition, subtraction, multiplication, division,
percentages, ratio, and simple averages. Every data set used in this file is printed
inline in the question itself as a small text table or list, so no figure, graph or
separate dataset is needed. No prior reasoning chapter is required.

**Volume:** 230 questions across 12 sections. Roughly 20% rule/recall, 30% quick
application, 25% medium, 15% GATE 1-mark MCQ (tagged `GATE-1`) and 10% GATE 2-mark
(tagged `GATE-2`).

---

## Section 1. Tables: direct and derived reading, totals, growth rates

### Q1. In the table below, which household recorded the highest electricity consumption?

```
Household | Units consumed (kWh)
A        | 120
B        | 200
C        | 175
D        | 240
```

> **Type:** Conceptual
> **Answer:** Household D, with 240 kWh.
> **Solution:** This is a direct lookup: compare the four values 120, 200, 175 and 240 in the single data column. The largest is 240, which sits on row D. No arithmetic is required, and no rate or total is involved.
> **Key point:** For a "largest/smallest" question on one column, read the column and compare the entries directly.

### Q2. By what percentage did production increase from 2018 to 2020?

```
Year | Production (tonnes)
2018 | 400
2019 | 500
2020 | 600
```

> **Type:** Numerical
> **Answer:** 50 %
> **Solution:** Percentage change = (new − old)/old × 100 = (600 − 400)/400 × 100 = 200/400 × 100 = 50 %. The intermediate 2019 value is a distractor: the question asks about 2018 to 2020, so only the two end years enter the formula. A common error is to average the two annual growth rates (25 % and 20 %) to get 22.5 %, which is not the overall change.
> **Key point:** Percentage change always uses the *starting* value as the denominator, never the ending one.

### Q3. In the league table below, how many matches did team B lose?

```
Team | Won | Lost | Total
A    | 12  | 5    | 17
B    | 9   | ?    | 22
C    | 15  | 8    | 23
```

> **Type:** Numerical
> **Answer:** 13 matches.
> **Solution:** Every row satisfies Won + Lost = Total. For team B, 9 + Lost = 22, so Lost = 22 − 9 = 13. A sanity check: 13 is larger than the losses of A (5) and C (8), which is consistent with B winning the fewest of the three matches (9).
> **Key point:** A "?" entry is recovered by applying the row's own internal rule — one equation, one unknown.

### Q4. Which column of the table has the greater total, and by how much?

```
Item | Q1 sales | Q2 sales
P    | 40       | 60
Q    | 55       | 50
R    | 35       | 70
S    | 60       | 45
```

> **Type:** Numerical
> **Answer:** The Q2 column, by 35 units.
> **Solution:** Q1 total = 40 + 55 + 35 + 60 = 190. Q2 total = 60 + 50 + 70 + 45 = 225. The difference is 225 − 190 = 35, so Q2 is the greater column. Note that although the single largest entry in the whole table is 70 (item R, Q2 column), the column total is what the question asks for.
> **Key point:** Column totals require adding *down* a column; adding *across* a row answers a different question.

### Q5. Which product generated the highest revenue, and what was the total revenue of all three products?

```
Product | Units sold | Price per unit (₹)
X       | 200        | 50
Y       | 150        | 40
Z       | 300        | 25
```

> **Type:** Numerical
> **Answer:** Product X, with ₹10,000; total revenue of all three = ₹23,500.
> **Solution:** Revenue = units × price. X: 200 × 50 = 10,000. Y: 150 × 40 = 6,000. Z: 300 × 25 = 7,500. X has the highest revenue even though Z sold the most units, because revenue depends on the product of the two columns. The overall total is 10,000 + 6,000 + 7,500 = 23,500.
> **Key point:** Never rank on units sold alone — the price column changes the order.

### Q6. What is the average mark of the five students listed below?

```
Marks obtained: 72, 85, 64, 90, 79
```

> **Type:** Numerical
> **Answer:** 78 marks.
> **Solution:** Sum = 72 + 85 + 64 + 90 + 79 = 390. Average = sum / number of entries = 390 / 5 = 78. A useful check: the mean must lie between the smallest value (64) and the largest (90), which 78 satisfies.
> **Key point:** The average of a list always lies between its minimum and its maximum.

### Q7. What is the percentage decrease in sales from 2018 to 2019?

```
Year | Sales (units)
2017 | 800
2018 | 1000
2019 | 900
```

> **Type:** Numerical
> **Answer:** 10 %.
> **Solution:** Percentage decrease = (old − new)/old × 100 = (1000 − 900)/1000 × 100 = 100/1000 × 100 = 10 %. Sales in 2019 are still 12.5 % above 2017 (900 vs 800), so the fall is only a dip and not a return to the starting level.
> **Key point:** A fall from 1000 to 900 is a 10 % fall, because 100 is 10 % of 1000 — the base, not the new value.

### Q8. Which item gives the highest total profit?

```
Item | Units sold | Selling price/unit (₹) | Cost price/unit (₹)
A    | 100        | 60                     | 42
B    | 400        | 30                     | 28
C    | 250        | 45                     | 30
```

> **Type:** Comparison
> **Answer:** Item C, with a total profit of ₹3,750.
> **Solution:** Profit per unit = SP − CP, so A = 18, B = 2, C = 15. Total profit = profit per unit × units: A = 18 × 100 = 1,800; B = 2 × 400 = 800; C = 15 × 250 = 3,750. The largest total profit is C's ₹3,750. Note the trap: item A earns the highest profit *per unit* (₹18) but not the highest total profit, because C sells far more units at a decent margin.
> **Key point:** Highest margin and highest total profit are usually different items — check both before answering.

### Q9. If the total sales over the four months were 1350 units, how many units were sold in April?

```
Month | Units sold
Jan   | 340
Feb   | 275
Mar   | 385
April | ?
Total | 1350
```

> **Type:** Numerical
> **Answer:** 350 units.
> **Solution:** The three known months total 340 + 275 + 385 = 1000. April = 1350 − 1000 = 350 units. A quick plausibility check: 350 is close to the neighbouring months' 340 and 385, which is what one expects of a monthly figure.
> **Key point:** With a grand total given, subtract the known parts rather than re-adding the whole table.

### Q10. What is the average cost of one pencil?

```
Item    | Quantity sold
Pen     | 120
Pencil  | 200
Eraser  | 150
```

> **Type:** Conceptual
> **Answer:** It cannot be determined from the table.
> **Solution:** Average cost per pencil = total cost of pencils / 200, and the table gives no cost data at all — no unit price, no total cost, no revenue from which a cost could be backed out. Quantities alone carry no price information, so the quantity is irrelevant to the answer. This is the standard "insufficient data" trap in data-interpretation sets.
> **Key point:** A table of quantities only can never yield a per-unit price; price or cost data is a hard requirement.

### Q11. What percentage of all customers are in the Delhi and Mumbai branches together?

```
Branch   | Customers (thousands)
Delhi    | 240
Mumbai   | 180
Chennai  | 120
Kolkata  | 60
```

> **Type:** Numerical
> **Answer:** 70 %.
> **Solution:** Total customers = 240 + 180 + 120 + 60 = 600 thousand. Delhi + Mumbai = 240 + 180 = 420 thousand. Share = 420/600 × 100 = 70 %. As a check, the two remaining branches together hold 180/600 = 30 %, and 70 % + 30 % = 100 %.
> **Key point:** A percentage share is always (part ÷ whole) × 100; the whole is the total of *all* rows, not just the ones named.

### Q12. Which state has the highest population density?

```
State | Area (km²)     | Population (millions)
X     | 1000           | 2.0
Y     | 2500           | 5.0
Z     | 4000           | 12.0
```

> **Type:** Comparison
> **Answer:** State Z, at 3000 persons per km².
> **Solution:** Density = population ÷ area, with the population converted to persons: X = 2,000,000/1000 = 2000 per km²; Y = 5,000,000/2500 = 2000 per km²; Z = 12,000,000/4000 = 3000 per km². Z is highest. The trap is that Y has both the largest area and a large population; density can rise while area rises faster, and here Z wins on population without having the largest area.
> **Key point:** Density is population per *area*, so the largest area does not imply the largest density.

### Q13. `GATE-1`. Which company recorded the highest revenue growth rate from 2020 to 2021?

```
Company | Revenue 2020 (₹ cr) | Revenue 2021 (₹ cr) | Growth %
P       | 200                 | 250                 | 25 %
Q       | 400                 | 440                 | 10 %
R       | 100                 | 115                 | 15 %
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Company P
> (b) Company Q
> (c) Company R
> (d) It cannot be determined
> ```
> **Answer:** Company P (Option a).
> **Solution:** The growth rates are given directly: P = (250 − 200)/200 = 25 %, Q = (440 − 400)/400 = 10 %, R = (115 − 100)/100 = 15 %. The largest is P's 25 %. The classic trap is option (b): Q had the largest *absolute* increase (₹40 crore) but the smallest *rate*, because it started from the largest base.
> **Key point:** Absolute increase and growth rate rank companies differently; the rate normalises by the starting value.

### Q14. On which day was the difference between the evening peak and the morning peak the greatest?

```
Day | Morning peak (MW) | Evening peak (MW)
Mon | 100               | 140
Tue | 120               | 155
Wed | 90                | 135
```

> **Type:** Numerical
> **Answer:** Wednesday, with a difference of 45 MW.
> **Solution:** Differences: Monday 140 − 100 = 40 MW; Tuesday 155 − 120 = 35 MW; Wednesday 135 − 90 = 45 MW. Wednesday is the largest. Note that Wednesday has the *lowest* morning peak of the three days, so its large difference is driven by the low starting point rather than by a high evening peak.
> **Key point:** A difference is always a subtraction in a fixed order; decide which value is the minuend before subtracting.

### Q15. If 20 % more mangoes (by mass) had been sold, by what percentage would the weekly total have increased?

```
Fruit sold in one week (kg): Mango 40, Banana 55, Apple 25, Guava 10
```

> **Type:** Numerical
> **Answer:** ≈ 6.15 % (about 6.2 %).
> **Solution:** Original total = 40 + 55 + 25 + 10 = 130 kg. An extra 20 % of mangoes = 0.20 × 40 = 8 kg, giving a new total of 138 kg. The increase relative to the original total is 8/130 × 100 = 6.1538 % ≈ 6.15 %. The percentage change in the total is much smaller than 20 % because the increase is spread over the whole 130 kg base, not just the 40 kg of mangoes.
> **Key point:** A change in one component changes the total by less than the same percentage, in general.

### Q16. Which material costs the most per millimetre of thickness per metre?

```
Material   | Thickness (mm) | Cost per metre (₹)
Copper     | 2.5            | 480
Aluminium  | 3.0            | 210
Steel      | 4.0            | 95
```

> **Type:** Comparison
> **Answer:** Copper, at ₹192 per mm per metre.
> **Solution:** Cost per mm per metre = cost per metre ÷ thickness. Copper: 480/2.5 = 192. Aluminium: 210/3.0 = 70. Steel: 95/4.0 = 23.75. Copper is highest by a wide margin, so the answer is not simply the most expensive raw material — it is also the thinnest.
> **Key point:** A two-step "per unit of X" question needs the numerator divided by the denominator, and both must be from different columns.

### Q17. `GATE-1`. Which city recorded the largest percentage increase in expenditure?

```
City | 2019 (₹ lakh) | 2020 (₹ lakh) | Change (₹ lakh)
X    | 400           | 500           | +100
Y    | 20            | 70            | +50
Z    | 300           | 320           | +20
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) City X
> (b) City Y
> (c) City Z
> (d) All three increased by the same percentage
> ```
> **Answer:** City Y (Option b).
> **Solution:** Percentage increases: X = 100/400 = 25 %; Y = 50/20 = 250 %; Z = 20/300 ≈ 6.67 %. Y is largest. The trap is option (a): X had the largest *absolute* increase of ₹100 lakh, but its percentage increase is only 25 %, because it began from a much larger base. Y's ₹50 lakh increase looks smaller but is 250 % of what it started with.
> **Key point:** A small absolute change on a small base can be a very large percentage change.

### Q18. The length of the Yamuna is approximately what fraction of the length of the Ganga?

```
River  | Length (km)
Ganga  | 2525
Yamuna | 1376
```

> **Type:** Numerical
> **Answer:** ≈ 0.545, i.e. about 54.5 % (a little over one half).
> **Solution:** Fraction = 1376/2525 = 0.5450. So the Yamuna is about 0.545 times the Ganga, or 54.5 % of it. The reverse statement, Ganga ÷ Yamuna, gives 2525/1376 = 1.835, which is the factor by which the Ganga is longer.
> **Key point:** "A is what fraction of B" means A ÷ B — the order of the division follows the order of the words in the question.

### Q19. A sum of ₹5000 earns simple interest at 10 % in year 1, 11 % in year 2 and 12 % in year 3. What is the total interest earned over the three years?

```
Year | Principal (₹) | Interest (₹)
1    | 5000          | 500
2    | 5000          | 550
3    | 5000          | 600
```

> **Type:** Numerical
> **Answer:** ₹1650.
> **Solution:** Total interest = 500 + 550 + 600 = 1650. Each figure is principal × rate: 5000 × 0.10 = 500, 5000 × 0.11 = 550, 5000 × 0.12 = 600, which confirms the table. Equivalently, total interest = 5000 × (0.10 + 0.11 + 0.12) = 5000 × 0.33 = 1650.
> **Key point:** With simple interest the interest does not compound, so the yearly amounts can simply be added.

### Q20. `GATE-2`. What is the overall achievement percentage across all four branches, and which branch has the lowest individual achievement?

```
Branch | Target | Achieved | Achievement %
A      | 500    | 450      | 90 %
B      | 400    | 340      | 85 %
C      | 600    | 600      | 100 %
D      | 450    | 405      | 90 %
```

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) 92.05 % overall, and Branch B is the lowest individually
> (b) 90 % overall, and Branch B is the lowest individually
> (c) 92.05 % overall, and Branch C is the lowest individually
> (d) 89 % overall, and Branch A is the lowest individually
> ```
> **Answer:** 92.05 % overall with Branch B lowest individually (Option a).
> **Solution:** Total target = 500 + 400 + 600 + 450 = 1950. Total achieved = 450 + 340 + 600 + 405 = 1795. Overall achievement = 1795/1950 × 100 = 92.05 %. The overall figure is *not* the simple average of the four percentages (90 + 85 + 100 + 90)/4 = 91.25 %, because the branches have different targets and must be weighted. The lowest individual achievement is B at 85 %; C is the highest at 100 %, which rules out option (c).
> **Key point:** An overall percentage is total-achieved ÷ total-target, never the unweighted mean of the row percentages.

### Q21. An alarm threshold is set at 50 °C. How many of the sensors below exceed the threshold?

```
Sensor | Reading
A      | 45 °C
B      | 52 °C
C      | 38 °C
```

> **Type:** Conceptual
> **Answer:** One sensor (B).
> **Solution:** Compare each reading with 50: A is 45, which is below; B is 52, which exceeds; C is 38, which is below. Exactly one reading is above the threshold. Note that "exceed" is strict — a reading of exactly 50 would *not* count, though no reading here is exactly 50.
> **Key point:** "Exceeds" is a strict inequality; = does not satisfy it.

---

## Section 2. Bar graphs, line graphs and pie charts

### Q22. Each block in the bar chart below represents 50 units. In which month was output the highest, and by how much did it exceed the lowest month?

```
Each █ = 50 units
Jan | ███      150
Feb | ██████   300
Mar | ████     200
Apr | █████    250
```

> **Type:** Conceptual
> **Answer:** February, at 300 units, which exceeds January's 150 units by 150 units.
> **Solution:** Read the block counts: January 3 blocks = 150, February 6 blocks = 300, March 4 blocks = 200, April 5 blocks = 250. February is the tallest bar. The excess over the shortest bar (January, 150) is 300 − 150 = 150 units, which is itself 3 blocks wide.
> **Key point:** With a constant block size, the block count converts directly to a value; subtract the shortest bar for the excess.

### Q23. Each block represents 25 units. What was the percentage increase in output from 2019 to 2021?

```
Each █ = 25 units
2019 | ████        100
2020 | ████████    200
2021 | ██████████  250
```

> **Type:** Numerical
> **Answer:** 150 %.
> **Solution:** The 2019 bar is 4 blocks = 100 and the 2021 bar is 10 blocks = 250. Increase = 250 − 100 = 150. Percentage increase = 150/100 × 100 = 150 %. Over the same two years the 2019-to-2020 rise alone was 100 %, so the second year adds only another 25 % on top of the new base of 200.
> **Key point:** A two-year percentage change is not the sum of the two annual rates; compound, not add.

### Q24. By how many units, and by what percentage, does plant A exceed plant B?

```
Each █ = 10 units
Plant A | ███████████  110
Plant B | ████████       80
```

> **Type:** Numerical
> **Answer:** By 30 units, which is 37.5 % of plant B's output.
> **Solution:** A = 11 blocks = 110, B = 8 blocks = 80. Difference = 110 − 80 = 30. Percentage by which A exceeds B = 30/80 × 100 = 37.5 %. Expressed the other way round, B is 30/110 = 27.3 % below A, so the direction of the division matters when reporting a percentage.
> **Key point:** "A exceeds B by x %" always divides x by B, the base being exceeded.

### Q25. `GATE-1`. In which year was the year-on-year increase in sales the largest?

```
Year: 2016  2017  2018  2019  2020
Sales: 120  145   140   190   230
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) 2017
> (b) 2018
> (c) 2019
> (d) 2020
> ```
> **Answer:** 2019 (Option c).
> **Solution:** Compute the four consecutive differences: 2016→2017 = +25; 2017→2018 = −5; 2018→2019 = +50; 2019→2020 = +40. The largest increase is +50, which is the rise *into* 2019. The largest raw value (230) is in 2020, but the question asks for the largest increase, not the highest level — that distinction is the whole point of the question.
> **Key point:** "Largest increase" means the biggest year-on-year *difference*, which need not occur in the year of the highest value.

### Q26. In which year did the price fall most steeply?

```
Year:  2016  2017  2018  2019  2020
Price: 340   360   300   275   290
```

> **Type:** Numerical
> **Answer:** 2018, when the price fell by 60 units (from 360 to 300).
> **Solution:** Year-on-year changes: 2017 = +20; 2018 = −60; 2019 = −25; 2020 = +15. Only two years show a fall, 2018 and 2019, and 2018's fall of 60 is the larger. The fall is attributed to the year in which it *ends*, so 2018 rather than 2017.
> **Key point:** A change is labelled by the year it lands in, not the year it starts from.

### Q27. Over how many of the four year-to-year steps did the value increase?

```
Year:  2016  2017  2018  2019  2020
Value: 250   310   295   340   400
```

> **Type:** Numerical
> **Answer:** 3 of the 4 steps.
> **Solution:** There are four steps for five data points. The changes are +60 (into 2017), −15 (into 2018), +45 (into 2019) and +60 (into 2020). Three of these are increases and one is a fall, so 3 of the 4 steps show an increase. A common miscount is to answer 4 by looking only at the endpoints.
> **Key point:** With n data points there are only n − 1 year-to-year steps, and every step must be checked.

### Q28. In which year were the two plotted lines equal, and what was the common value?

```
Year | Line P | Line Q
2018 |   30   |   90
2019 |   60   |   60
2020 |   90   |   30
```

> **Type:** Numerical
> **Answer:** 2019, at 60 units.
> **Solution:** Compare the two entries year by year: 2018 has 30 vs 90, 2019 has 60 vs 60, 2020 has 90 vs 30. The lines are exactly equal only in 2019, where both read 60. The crossover falls at a single plotted year because Line P rises by 30 per year while Line Q falls by 30 per year, meeting head-on.
> **Key point:** Find the intersection by comparing the two series year by year, not by eyeballing the drawn lines.

### Q29. What percentage of total exports was contributed by spices?

```
Exports (₹ crore): Rice 450, Sugar 300, Spices 150, Tea 100
```

> **Type:** Numerical
> **Answer:** 15 %.
> **Solution:** Total = 450 + 300 + 150 + 100 = 1000 crore. The share of spices is 150/1000 × 100 = 15 %. On a pie chart of total 1000, spices would occupy 15 % of the circle.
> **Key point:** Compute the whole first, then take the part ÷ whole × 100; here the total is conveniently 1000.

### Q30. A budget of ₹80 lakh is allocated as Salaries 50 %, Equipment 25 %, Travel 15 % and Maintenance 10 %. What angle, in degrees, does the Equipment sector occupy on a pie chart?

> **Type:** Numerical
> **Answer:** 90°.
> **Solution:** A full pie is 360°, so a 25 % share occupies 25/100 × 360 = 90°. Equivalently, equipment receives 0.25 × 80 = ₹20 lakh, and 20/80 × 360 = 90°. The four shares must sum to 100 % (50 + 25 + 15 + 10 = 100), which confirms the chart is complete.
> **Key point:** Sector angle = (share ÷ 100) × 360; percentages convert to angles by this one rule.

### Q31. In the pie chart below, the largest sector exceeds the smallest by how many degrees?

```
Sales (units): Alpha 500, Beta 300, Gamma 150, Delta 50
```

> **Type:** Numerical
> **Answer:** 162° (180° − 18°).
> **Solution:** Total = 500 + 300 + 150 + 50 = 1000, so each unit is worth 0.1 % of the circle. Alpha (500 units) takes 500/1000 × 360 = 180°, a half circle. Delta (50 units) takes 50/1000 × 360 = 18°. The difference is 180 − 18 = 162°, which is 45 % of the full circle.
> **Key point:** With a total of 1000, the angle equals the value × 0.36; always convert both sectors before subtracting.

### Q32. Lighting, Motors and Heating together account for what percentage of the energy consumed?

```
Energy consumption (kWh): Lighting 800, Motors 1200, Heating 600, Cooling 400
```

> **Type:** Numerical
> **Answer:** 86.7 % (2600 kWh out of 3000 kWh).
> **Solution:** The three named items total 800 + 1200 + 600 = 2600 kWh. Overall total = 2600 + 400 = 3000 kWh. Share = 2600/3000 × 100 = 86.67 % ≈ 86.7 %. Equivalently, the omitted item, Cooling, is 400/3000 = 13.3 %, and 100 − 13.3 = 86.7 %.
> **Key point:** "A, B and C together" is often easiest via the complement, 100 % minus the remaining share.

### Q33. Express, as a fraction in lowest terms, the share of the library's issues that were fiction books.

```
Books issued (thousands): Fiction 350, Non-fiction 250, Reference 150, Periodicals 250
```

> **Type:** Numerical
> **Answer:** 7/20 (that is, 0.35).
> **Solution:** Total = 350 + 250 + 150 + 250 = 1000 thousand. Fiction share = 350/1000 = 35/100 = 7/20 after dividing numerator and denominator by 5. Note that 7 and 20 share no common factor, so 7/20 is already in lowest terms.
> **Key point:** Reduce a fraction to lowest terms by dividing top and bottom by their greatest common divisor.

### Q34. What is the ratio of the tallest to the shortest bar in the chart?

```
Each █ = 5 units
Low   | ██          10
Med   | ██████      30
High  | ██████████  50
```

> **Type:** Numerical
> **Answer:** 5 : 1.
> **Solution:** Tallest = 50, shortest = 10, so the ratio is 50 : 10 = 5 : 1 once divided by 10. A ratio is written with the "reference" quantity second, so "tallest to shortest" is 5 : 1 and not 1 : 5.
> **Key point:** The order of a ratio follows the order named in the question; then reduce by the common factor.

### Q35. Branch D handled some units. Given the total across all four branches was 500 units, how many did branch D handle?

```
Each █ = 20 units
Branch A | ████████  160
Branch B | ██████    120
Branch C | ████       80
Branch D | ████       ?
```

> **Type:** Numerical
> **Answer:** 140 units.
> **Solution:** The three known branches total 160 + 120 + 80 = 360. Branch D = 500 − 360 = 140 units, which is 7 blocks of 20. D is then the second largest of the four, between A's 160 and B's 120.
> **Key point:** A missing value in a total-all row is found by subtracting the known parts from the grand total.

### Q36. What is the average of the four yearly output figures?

```
Year:   2016  2017  2018  2019
Output: 220   260   280   240
```

> **Type:** Numerical
> **Answer:** 250 units.
> **Solution:** Sum = 220 + 260 + 280 + 240 = 1000. Average = 1000/4 = 250. This coincides with the mean of the highest (280) and lowest (220) values divided by two, 250, which is a coincidence here and not a general rule.
> **Key point:** Average = sum ÷ count; with four values the median is the average of the middle two, which is a separate calculation.

### Q37. `GATE-1`. For the bar chart below, which one of the four statements is correct?

```
Each █ = 10 units
Q1 | ██████      60
Q2 | ████████    80
Q3 | ███████     70
Q4 | ██████████ 100
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Q2 and Q4 together = 180 units
> (b) Q1 is greater than Q3
> (c) Q4 is exactly twice Q1
> (d) The average of the four quarters = 70 units
> ```
> **Answer:** (a), since 80 + 100 = 180.
> **Solution:** Check each option against the values 60, 80, 70, 100. (a) 80 + 100 = 180 ✓. (b) 60 < 70, so false. (c) twice Q1 is 120, not 100, so false. (d) the average is (60 + 80 + 70 + 100)/4 = 310/4 = 77.5, not 70, so false. Exactly one option survives.
> **Key point:** In a single-correct MCQ, verify every option arithmetically; three of four are built from near-misses.

### Q38. `GATE-1`. For the sales series below, which one of the four statements is correct?

```
Year:  2016  2017  2018  2019  2020
Sales: 300   360   330   400   450
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Sales increased in every year from 2016 to 2020
> (b) The largest single-year increase occurred in 2020
> (c) Sales in 2018 were higher than in 2017
> (d) Total sales over the five years = 1840 units
> ```
> **Answer:** (d).
> **Solution:** The four changes are +60, −30, +70 and +50, so (a) is false because of the 2018 fall, and (b) is false because the largest rise was +70 into 2019, not into 2020. For (c), 330 < 360, so 2018 was lower, making (c) false. The total is 300 + 360 + 330 + 400 + 450 = 1840, so (d) is correct.
> **Key point:** A rising-then-falling series still has a higher final value than initial; do not read "overall trend" as "rose every year".

### Q39. `GATE-2`. Imports are broken into four categories by value. What percentage of import value comes from textiles and spares together, and what is that share expressed as a fraction?

```
Imports by value (₹ lakh): Machinery 500, Chemicals 300, Textiles 150, Spares 50
```

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) 20 % and 1/5
> (b) 25 % and 1/4
> (c) 20 % and 1/4
> (d) 30 % and 1/3
> ```
> **Answer:** (a), 20 % and 1/5.
> **Solution:** Total = 500 + 300 + 150 + 50 = 1000 lakh. Textiles and spares together are 150 + 50 = 200 lakh, so their share is 200/1000 = 0.2 = 20 %. As a fraction, 200/1000 reduces to 2/10 = 1/5. Option (c) pairs the correct percentage with a fraction that is actually 25 %, which is the intended distractor.
> **Key point:** Convert the same quantity to percentage and to fraction, and check that they agree (20 % = 0.20 = 1/5).

### Q40. What was the cumulative total sold by the end of Wednesday?

```
Each █ = 5 units
Mon | ████      20
Tue | ██████    30
Wed | ██████    30
Thu | ████████  40
Fri | ██████    30
```

> **Type:** Numerical
> **Answer:** 80 units.
> **Solution:** Cumulative sums: after Monday 20; after Tuesday 20 + 30 = 50; after Wednesday 50 + 30 = 80. The answer is 80, not 30 (Wednesday's own bar alone) and not 50 (the total through Tuesday). The remaining two days add 70, taking the week's total to 150.
> **Key point:** A cumulative total is a running sum — add every bar from the start up to and including the bar asked about.

### Q41. If the year-on-year increase continues unchanged, what will the 2021 figure be?

```
Year:  2018  2019  2020
Units: 500   650   800
```

> **Type:** Numerical
> **Answer:** 950 units.
> **Solution:** The increases are 650 − 500 = 150 and 800 − 650 = 150, a constant annual addition of 150. Continuing it, 2021 = 800 + 150 = 950. The extrapolation is valid only because the two observed increments are equal; had they differed, an average increment would have to be assumed instead.
> **Key point:** A constant *additive* step is projected by adding; a constant *percentage* step by multiplying.

### Q42. By what percentage is product A's profit greater than product B's?

```
Profit (₹ lakh): A 240, B 180, C 120
```

> **Type:** Numerical
> **Answer:** 33.3 % (approximately one third).
> **Solution:** The excess is 240 − 180 = 60 lakh. As a percentage of B's profit: 60/180 × 100 = 33.33 % ≈ 33.3 %. A check: the three profits are in the ratio 240 : 180 : 120 = 2 : 1.5 : 1, so A is 2/1.5 = 4/3 times B, i.e. 1/3 = 33.3 % more.
> **Key point:** To convert a ratio p : q into a percentage increase, compute (p − q)/q × 100.

### Q43. In which region was the year-on-year change the largest, and what was its size?

```
         2019   2020
Region A  120    150
Region B  180    165
Region C   95    110
```

> **Type:** Numerical
> **Answer:** Region A, with an increase of 30 units.
> **Solution:** Changes: A = 150 − 120 = +30; B = 165 − 180 = −15; C = 110 − 95 = +15. The largest change in magnitude is Region A's +30. Note that if "largest" is read as "largest percentage", A still wins (30/120 = 25 %, against C's 15/95 ≈ 15.8 %), so both readings agree here.
> **Key point:** Take the difference with its sign; "largest change" can mean largest increase or largest magnitude, and they differ when there are falls.

### Q44. `GATE-2`. What is the average of all ten plotted values across the two lines?

```
Year | Line X | Line Y
2018 |   30   |   45
2019 |   45   |   50
2020 |   60   |   55
2021 |   75   |   60
2022 |   90   |   65
```

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) 55
> (b) 57.5
> (c) 60
> (d) 65
> ```
> **Answer:** (b) 57.5.
> **Solution:** Line X sums to 30 + 45 + 60 + 75 + 90 = 300 and averages 60. Line Y sums to 45 + 50 + 55 + 60 + 65 = 275 and averages 55. The ten values together total 300 + 275 = 575, and 575/10 = 57.5. Options (a) and (c) are the separate per-line averages, which is the intended trap: averaging the two averages is valid only when both lines contribute the same number of points, and here it would give 57.5 anyway, but the correct procedure is to pool the sums and divide by the pooled count.
> **Key point:** To average a combined set, total every value and divide by the total number of values.

### Q45. Express, as a fraction of the total, the land under forest.

```
Land use (hectares): Crop 400, Forest 300, Grass 200, Built-up 100
```

> **Type:** Numerical
> **Answer:** 3/10 (that is, 0.30).
> **Solution:** Total land = 400 + 300 + 200 + 100 = 1000 hectares. Forest share = 300/1000 = 3/10. A pie chart of this data would show forest occupying 3/10 of the circle, that is 108°, since 0.3 × 360 = 108°.
> **Key point:** A fraction of a pie is a fraction of the area; multiply it by 360 to get the angle.

---

## Section 3. Frequency distributions, histograms and cumulative frequency

### Q46. Which is the modal class in the distribution below?

```
Marks obtained | Number of students
10-20          | 4
20-30          | 9
30-40          | 14
40-50          | 11
50-60          | 2
```

> **Type:** Conceptual
> **Answer:** The class 30–40.
> **Solution:** The mode of a grouped distribution is estimated by the *modal class*, the class interval carrying the highest frequency. The frequencies are 4, 9, 14, 11 and 2, and the maximum is 14, which belongs to 30–40. The total number of observations is 4 + 9 + 14 + 11 + 2 = 40, of which 14, that is 35 %, fall in that class.
> **Key point:** For grouped data the "mode" is the *modal class* — the interval of greatest frequency, not a specific value.

### Q47. What fraction of the observations lie below 25?

```
Class  | Frequency
5-15   | 9
15-25  | 16
25-35  | 12
35-45  | 7
```

> **Type:** Numerical
> **Answer:** 25/44 (≈ 0.568).
> **Solution:** Total N = 9 + 16 + 12 + 7 = 44. Observations below 25 are those in 5-15 and 15-25, so 9 + 16 = 25. The fraction is 25/44, which does not reduce further. As a percentage it is 25/44 × 100 ≈ 56.8 %.
> **Key point:** "Below 25" means strictly less than 25, so the class that *ends* at 25 is included but the one that *starts* at 25 is not.

### Q48. `GATE-1`. The classes below have unequal widths. Which class has the greatest frequency density?

```
Class  | Width | Frequency | Frequency density
0-10   | 10    | 60        | 6.0
10-20  | 10    | 40        | 4.0
20-40  | 20    | 100       | 5.0
40-50  | 10    | 30        | 3.0
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) 0-10
> (b) 10-20
> (c) 20-40
> (d) 40-50
> ```
> **Answer:** (a), the class 0–10.
> **Solution:** Frequency density = frequency ÷ class width. The four densities are 60/10 = 6.0, 40/10 = 4.0, 100/20 = 5.0 and 30/10 = 3.0, so 0-10 is the densest at 6.0. The trap is option (c): 20-40 has the largest raw frequency (100) but is twice as wide, so it is spread over 20 units of the axis and reaches only 5.0.
> **Key point:** With unequal class widths, compare frequency *density* (frequency ÷ width), not raw frequency.

### Q49. How many observations have a value of at least 20?

```
Class  | Frequency | Less-than cumulative frequency
0-10   | 6         | 6
10-20  | 10        | 16
20-30  | 15        | 31
30-40  | 9         | 40
```

> **Type:** Numerical
> **Answer:** 24 observations.
> **Solution:** The total N = 40. The cumulative frequency below 20 is 16, so everything not below 20 is at or above 20: 40 − 16 = 24. This is confirmed directly by adding the two remaining classes, 15 + 9 = 24. The subtraction works because the "less than 20" and "at least 20" groups partition the whole distribution.
> **Key point:** Complement of "less than x" is "at least x", so the count is N − cf(below x).

### Q50. Find the median of the grouped distribution by interpolation.

```
Class  | Frequency
0-20   | 4
20-40  | 10
40-60  | 20
60-80  | 10
```

> **Type:** Numerical
> **Answer:** 48.
> **Solution:** N = 4 + 10 + 20 + 10 = 44, so N/2 = 22. Cumulative frequencies are 4, 14, 34, 44, so the 22nd observation falls in the class 40–60. Using Median = l + [(N/2 − cf)/f] × h with lower limit l = 40, cf = 14, frequency f = 20 and class height h = 20: Median = 40 + [(22 − 14)/20] × 20 = 40 + 8 = 48.
> **Key point:** Grouped median = lower limit + [(N/2 − previous cf)/class frequency] × class width; the 22nd of 44 items lands 8 units into the class.

### Q51. What is the mean of the distribution?

```
Value | Frequency
2     | 3
4     | 5
6     | 7
8     | 3
10    | 2
```

> **Type:** Numerical
> **Answer:** 5.6.
> **Solution:** N = 3 + 5 + 7 + 3 + 2 = 20. The weighted sum Σfx = 2×3 + 4×5 + 6×7 + 8×3 + 10×2 = 6 + 20 + 42 + 24 + 20 = 112. Mean = Σfx/N = 112/20 = 5.6, which lies between the smallest value 2 and the largest 10, as it must.
> **Key point:** Mean of a frequency table = Σfx ÷ Σf, i.e. weight each value by how often it occurs.

### Q52. The lowest value recorded in a data set is 34 and the highest is 118. If classes of width 7 are used, how many classes are required?

> **Type:** Numerical
> **Answer:** 12 classes.
> **Solution:** Range = highest − lowest = 118 − 34 = 84. Number of classes = range ÷ class width = 84 ÷ 7 = 12 exactly. The classes would be 34–41, 41–48, … , 111–118, and 12 × 7 = 84 confirms full coverage with no remainder.
> **Key point:** Number of classes = range ÷ class width; the range is the difference of the extreme values, not their sum.

### Q53. What fraction of all observations lie above 30?

```
Class  | Frequency | More-than cumulative frequency
0-10   | 8         | 34
10-20  | 12        | 22
20-30  | 14        | 8
30-40  | 8         | 0
```

> **Type:** Numerical
> **Answer:** 4/21 (≈ 0.190).
> **Solution:** N = 8 + 12 + 14 + 8 = 42. The more-than cumulative frequency at 30 is 8, so 8 of the 42 observations lie above 30. The fraction is 8/42 = 4/21, and 8 and 42 share the factor 2 but no larger one, so 4/21 is in lowest terms. A check on the data itself: the individual class frequencies 8 + 12 + 14 + 8 = 42 do sum to the total, which is what a more-than column is built from.
> **Key point:** A "more than" cumulative column is read downward; its bottom entry is the top-class frequency and the total N is the sum of the raw frequencies.

### Q54. `GATE-2`. The mean of the distribution is 23. Find the missing frequency.

```
Class  | Frequency | Class mark
0-10   | 2         | 5
10-20  | 5         | 15
20-30  | x         | 25
30-40  | 6         | 35
```

> **Type:** Numerical `GATE-2`
> **Answer:** x = 2.
> **Solution:** The class mark of each interval is its midpoint, and Mean = Σfx ÷ Σf. With the unknown x: Σf = 2 + 5 + x + 6 = 13 + x, and Σfx = 5×2 + 15×5 + 25x + 35×6 = 10 + 75 + 25x + 210 = 295 + 25x. Setting the mean to 23 gives (295 + 25x)/(13 + x) = 23, so 295 + 25x = 299 + 23x, giving 2x = 4 and x = 2. Verification: Σf = 15, Σfx = 295 + 50 = 345, and 345/15 = 23.
> **Key point:** To recover a missing frequency from a known mean, write Σfx and Σf with the unknown, set the ratio, and solve the linear equation.

### Q55. What is the median of the seven observations below?

```
Data: 12, 7, 25, 14, 9, 18, 11
```

> **Type:** Numerical
> **Answer:** 12.
> **Solution:** Arrange the data in ascending order: 7, 9, 11, 12, 14, 18, 25. There are 7 values, an odd number, so the median is the single middle value, the (7 + 1)/2 = 4th one, which is 12. No averaging is needed, which is the special case of an odd-sized data set.
> **Key point:** For odd n the median is the ((n+1)/2)th ordered value; for even n it is the mean of the n/2th and (n/2 + 1)th.

### Q56. A distribution runs from a minimum of 8 to a maximum of 92. If inclusive classes 8–18, 18–28, … are used, how many classes are needed and what is the class mark of the first class?

> **Type:** Numerical
> **Answer:** 9 classes, and the first class mark is 13.
> **Solution:** Range = 92 − 8 = 84. With inclusive classes of width 10 the sequence runs 8–18, 18–28, 28–38, 38–48, 48–58, 58–68, 68–78, 78–88, 88–98 — that is 9 classes, since 9 × 10 = 90 covers the 84-unit range with 6 units of margin. The class mark of the first class is (8 + 18)/2 = 13.
> **Key point:** With inclusive classes consecutive intervals share a boundary value, so the count is one more than range ÷ width when the range divides exactly.

### Q57. An interval of data runs from 15 to 20, both ends included. State the continuous class boundaries and the class mark.

> **Type:** Conceptual
> **Answer:** Continuous boundaries 14.5 to 20.5, with a class mark of 17.5.
> **Solution:** A continuous (real) class boundary is obtained by moving half a unit below the lower limit and half a unit above the upper limit: 15 − 0.5 = 14.5 and 20 + 0.5 = 20.5. The width is 20.5 − 14.5 = 6, exactly the span of 15 to 20. The class mark, being the midpoint, is (14.5 + 20.5)/2 = 17.5, identical to (15 + 20)/2.
> **Key point:** The class mark is unchanged by the ±0.5 shift, but the width is preserved only because both limits shift by 0.5.

### Q58. In a histogram, which class has the greatest area under its bar, and which has the greatest frequency density? They are not the same class.

```
Class  | Width | Frequency
0-5    | 5     | 20
5-10   | 5     | 30
10-20  | 10    | 40
```

> **Type:** Comparison
> **Answer:** Greatest area: the class 10–20. Greatest frequency density: the class 5–10.
> **Solution:** Area under a histogram bar = frequency (frequency per unit width × width = f), so the areas are 20, 30 and 40, and 10-20 is largest. Density = frequency ÷ width gives 20/5 = 4, 30/5 = 6 and 40/10 = 4, so 5-10 is densest at 6.0. The two answers differ because the 10-20 class buys its larger area by being twice as wide.
> **Key point:** In a histogram, bar *area* equals frequency while bar *height* equals frequency density; they coincide only when all classes are equally wide.

### Q59. Describe the shape of the distribution below.

```
Class  | Frequency
0-10   | 5
10-20  | 14
20-30  | 6
30-40  | 15
40-50  | 4
```

> **Type:** Conceptual
> **Answer:** It is bimodal, with two modal classes, 10–20 and 30–40.
> **Solution:** The frequencies 5, 14, 6, 15, 4 have two clear local peaks: 14 in the class 10-20 and 15 in the class 30-40, with a dip to 6 in between. Two peaks separated by a trough make the distribution bimodal, so there is no single mode. A unimodal distribution would have one clear peak with frequencies rising then falling.
> **Key point:** Two local maxima separated by a local minimum means bimodal; "the mode" is then not unique.

### Q60. A grouped distribution has a class interval running from 34 to 46. What is its class mark?

> **Type:** Numerical
> **Answer:** 40.
> **Solution:** The class mark, or class midpoint, is the average of the lower and upper limits: (34 + 46)/2 = 80/2 = 40. It is the value that stands in for every observation recorded in that interval, and the class width is 46 − 34 = 12.
> **Key point:** Class mark = (lower limit + upper limit) ÷ 2, and class width = upper − lower.

### Q61. `GATE-2`. Find the third quartile (75th percentile) of the grouped data by interpolation.

```
Class  | Frequency | Cumulative frequency
0-10   | 4         | 4
10-20  | 8         | 12
20-30  | 12        | 24
30-40  | 10        | 34
40-50  | 6         | 40
```

> **Type:** Numerical `GATE-2`
> **Answer:** 36.
> **Solution:** N = 40, so the position of the 75th percentile is 3N/4 = 3 × 40/4 = 30. Cumulative frequencies are 4, 12, 24, 34, 40, so the 30th observation falls in the class 30–40. Applying the interpolation Q3 = l + [(3N/4 − cf)/f] × h with l = 30, cf = 24, f = 10, h = 10 gives 30 + [(30 − 24)/10] × 10 = 30 + 6 = 36.
> **Key point:** The percentile position is 3N/4; locate the class with cf just below it, then interpolate using the same formula as the median.

### Q62. What fraction of the observations lie below 30?

```
Class  | Frequency
0-15   | 7
15-30  | 13
30-45  | 10
45-60  | 5
```

> **Type:** Numerical
> **Answer:** 4/7 (≈ 0.571).
> **Solution:** N = 7 + 13 + 10 + 5 = 35. Observations below 30 fall in the classes 0-15 and 15-30, giving 7 + 13 = 20. The fraction is 20/35, and dividing both by 5 gives 4/7. A check on the complement: those at or above 30 number 15, and 4/7 + 3/7 = 1.
> **Key point:** Add the frequencies of every class lying entirely below the threshold, then reduce the resulting fraction.

### Q63. What is the relative frequency of the modal class?

```
Class  | Frequency | Relative frequency
0-10   | 3         | 0.06
10-20  | 7         | 0.14
20-30  | 12        | 0.24
30-40  | 15        | 0.30
40-50  | 13        | 0.26
```

> **Type:** Numerical
> **Answer:** 0.30.
> **Solution:** The largest frequency is 15, in the class 30–40, so that is the modal class. The total is 3 + 7 + 12 + 15 + 13 = 50, and the relative frequency of the modal class is 15/50 = 0.30. The whole relative-frequency column sums to 0.06 + 0.14 + 0.24 + 0.30 + 0.26 = 1.00, confirming the total of 50.
> **Key point:** Relative frequency = class frequency ÷ total, and a full set of relative frequencies always sums to 1.

### Q64. `GATE-1`. For the cumulative frequency table below, which one of the four statements is correct?

```
Class  | Frequency | Cumulative frequency
0-10   | 8         | 8
10-20  | 14        | 22
20-30  | 19        | 41
30-40  | 13        | 54
40-50  | 6         | 60
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) The total number of observations is 60
> (b) The median lies in the class 10-20
> (c) The modal class is 30-40
> (d) Exactly 20 observations lie below 20
> ```
> **Answer:** (a).
> **Solution:** The last cumulative frequency is 60, so N = 60 and (a) is true. For (b), N/2 = 30 and the cumulative frequency first reaches or passes 30 at the end of the class 20-30 (41), so the median lies in 20-30, not 10-20. For (c), the largest frequency is 19, which is in 20-30. For (d), observations below 20 number 22, not 20. Only (a) holds.
> **Key point:** The median class is the first one whose cumulative frequency reaches N/2; the modal class is the one with the largest frequency — they are often different.

## Section 4. Data comparison, ranking and "by what factor" reasoning

### Q65. Which is the largest of the following values?

```
Values: 42, 57, 63, 38, 71, 55
```

> **Type:** Conceptual
> **Answer:** 71.
> **Solution:** Compare the six entries one at a time: the largest so far builds up as 42 → 57 → 63, is beaten by 71, and 55 does not surpass it. The maximum is 71, and the minimum is 38, so the range is 71 − 38 = 33. No operation beyond comparison is needed.
> **Key point:** A "largest" question is a comparison, not a calculation; a range needs both extremes.

### Q66. A component dissipates 0.6 W in one operating condition and 4.2 W in another. By what factor is the second value larger than the first?

> **Type:** Numerical
> **Answer:** 7.
> **Solution:** Factor = larger ÷ smaller = 4.2/0.6 = 7. The two powers are in the ratio 4.2 : 0.6, which clears to 42 : 6 and then to 7 : 1. A factor is dimensionless, so the answer is the plain number 7 with no unit.
> **Key point:** "By what factor" is always larger ÷ smaller, expressed as a dimensionless ratio.

### Q67. Which two of the values below sum to exactly 100?

```
35, 22, 65, 48, 76, 41
```

> **Type:** Numerical
> **Answer:** 35 and 65.
> **Solution:** Test each value against its complement 100 minus itself. For 35 the complement is 65, and 65 is present, so {35, 65} works. For 22 the complement is 78, absent. For 65 the complement is 35, already found. For 48 the complement is 52, absent. For 76 the complement is 24, absent. For 41 the complement is 59, absent. Exactly one pair qualifies.
> **Key point:** To find a pair with a fixed sum, look for each value's complement rather than trying all pairs.

### Q68. What is the second largest of the following five numbers?

```
128, 94, 156, 137, 112
```

> **Type:** Numerical
> **Answer:** 137.
> **Solution:** In descending order the values are 156, 137, 128, 112, 94. The largest is 156 and the runner-up is 137, sitting just 19 below it. A quick alternative is to note that 156 and 137 are the only entries above 128, and of those 137 is the smaller.
> **Key point:** The second largest is the largest of everything except the maximum — check that exactly two values lie above the runner-up.

### Q69. Which measurement is closest to the mean of the five?

```
Measurements: 12, 19, 21, 26, 32
```

> **Type:** Numerical
> **Answer:** 21.
> **Solution:** Sum = 12 + 19 + 21 + 26 + 32 = 110, so the mean is 110/5 = 22. Deviations from 22: 12 is 10 away, 19 is 3 away, 21 is 1 away, 26 is 4 away and 32 is 10 away. The smallest deviation is 1, so 21 is closest. A value equal to the mean would have zero deviation, but no value here is exactly 22.
> **Key point:** "Closest to the mean" = smallest absolute deviation |x − mean|.

### Q70. Which two entries in the list are exactly equal?

```
Component values: 4.5, 7.2, 4.5, 9.1, 3.3
```

> **Type:** Conceptual
> **Answer:** The two entries of 4.5 (the first and the third).
> **Solution:** Read the list against itself: 4.5 recurs in the first and third positions, while 7.2, 9.1 and 3.3 each appear only once. So the repeated value is 4.5. Rounding is not needed here because the match is exact; had the entries been 4.5 and 4.50 they would also match.
> **Key point:** Scan the list against itself; a value that appears exactly twice is the duplicate.

### Q71. What is the ratio of the smallest to the largest of the following plot areas?

```
Areas (m²): 240, 360, 180, 420
```

> **Type:** Numerical
> **Answer:** 3 : 7.
> **Solution:** The smallest is 180 and the largest is 420. The ratio is 180 : 420, and dividing both by 60 gives 3 : 7. The decimals would give the same answer, 0.4286 : 1, so the ratio 3/7 is the exact value.
> **Key point:** A ratio is reduced by dividing both terms by their greatest common divisor.

### Q72. By what percentage did the output increase from 1450 tonnes to 1740 tonnes?

> **Type:** Numerical
> **Answer:** 20 %.
> **Solution:** Increase = 1740 − 1450 = 290. Percentage increase = 290/1450 × 100 = 0.2 × 100 = 20 %. The reverse statement, 290/1740 = 16.7 %, would describe the drop needed to return to the old level, a different question.
> **Key point:** Percentage increase divides by the original (smaller) value; percentage decrease from a new level divides by the new one.

### Q73. The five values 4, 6, 8, 10, 12 are grouped. State the mean and the median, and explain why they coincide.

> **Type:** Conceptual
> **Answer:** Both are 8, because the data are perfectly symmetric about 8.
> **Solution:** Sum = 4 + 6 + 8 + 10 + 12 = 40, so the mean = 40/5 = 8. The median is the third of five ordered values, which is also 8. The two agree because the values pair off symmetrically about the centre: (4, 12) and (6, 10) each have midpoint 8, so the centre of mass sits exactly on the middle value.
> **Key point:** Mean and median coincide for a symmetric distribution; they diverge once values pile up at one end.

### Q74. Two items both increased by 30 % in value, from ₹250 to ₹325 and from ₹400 to ₹520. By how many rupees did the second increase exceed the first?

> **Type:** Numerical
> **Answer:** By ₹45.
> **Solution:** The first increase is 325 − 250 = ₹75, which is 0.30 × 250. The second is 520 − 400 = ₹120, which is 0.30 × 400. The excess is 120 − 75 = ₹45. Both grew at the same *rate* precisely because the rate is measured against their own bases, so the rupee gains differ in proportion to the starting values.
> **Key point:** Equal percentage growth on different bases produces absolute changes in the same ratio as the bases.

### Q75. `GATE-1`. For the speeds recorded below, which one of the four statements is correct?

```
Speeds (km/h): 45, 60, 52, 68, 55
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) The fastest vehicle travelled at 68 km/h
> (b) The mean speed of the five vehicles is 58 km/h
> (c) The range of the speeds is 25 km/h
> (d) Two of the vehicles travelled at the same speed
> ```
> **Answer:** (a).
> **Solution:** The maximum entry is 68, so (a) is true. The mean is (45 + 60 + 52 + 68 + 55)/5 = 280/5 = 56, not 58, so (b) is false. The range is 68 − 45 = 23, not 25, so (c) is false. All five speeds are distinct, so (d) is false.
> **Key point:** Three of these four options are near-misses on a correctly computed statistic; compute each before choosing.

### Q76. Of the three values 140, 95 and 180, which is closest to the average of the other two?

> **Type:** Numerical
> **Answer:** 140.
> **Solution:** For 140, the other two are 95 and 180, averaging (95 + 180)/2 = 137.5, so the deviation is 2.5. For 95, the other two average (140 + 180)/2 = 160, a deviation of 65. For 180, the others average (140 + 95)/2 = 117.5, a deviation of 62.5. The smallest deviation is 2.5, so 140 is closest to the average of the other two.
> **Key point:** "Closest to the average of the other two" compares each element against the mean of the remaining pair.

### Q77. `GATE-1`. By what factor is the largest gain in the list greater than the smallest?

```
Signal gains (dB): 12, 18, 24, 30
```

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) 2
> (b) 2.5
> (c) 3
> (d) 6
> ```
> **Answer:** (b) 2.5.
> **Solution:** The largest gain is 30 dB and the smallest is 12 dB, so the factor is 30/12 = 2.5. Option (a) 2 is the ratio of two adjacent entries (24/12), which compares neighbours rather than extremes. Option (c) 3 comes from 24 − 12 + 12, or from mistaking the fourth entry for the maximum. Option (d) 6 is the difference 30 − 24, a subtraction where the question asked for a ratio.
> **Key point:** Always identify the true maximum and true minimum of the list before dividing.

### Q78. Which two of the payouts below sum to exactly 200?

```
Payouts (₹ thousand): 45, 90, 130, 70, 75
```

> **Type:** Numerical
> **Answer:** 130 and 70.
> **Solution:** The complement of 130 is 70, and 70 is present, so the pair works. The complement of 45 is 155, absent; of 90 is 110, absent; of 75 is 125, absent. Only the pair {130, 70} sums to 200, and 130 + 70 = 200 confirms it.
> **Key point:** With five numbers there are ten pairs; testing complements is faster and misses nothing.

### Q79. All three values below increase by 20 %. Which pair's difference grows by the largest amount, and by how much?

```
A = 340, B = 210, C = 150
```

> **Type:** Numerical
> **Answer:** The pair A and C, whose difference grows by 38 (from 190 to 228).
> **Solution:** After a 20 % increase the values become 408, 252 and 180. The original differences are A − B = 130, A − C = 190 and B − C = 60; the new ones are 408 − 252 = 156, 408 − 180 = 228 and 252 − 180 = 72. The increases are therefore 26, 38 and 12. The largest is 38, from the pair A and C. This must be so in general: every difference is multiplied by the same factor 1.2, so the difference that gains the most is simply the one that was largest to begin with.
> **Key point:** Under a common percentage change every difference scales by the same factor, so the largest difference grows the most.

### Q80. A district's crop output was Rice 480, Wheat 430, Sugarcane 460 and Millets 90 tonnes. Which crop is the smallest, and is it also the smallest share of the total?

> **Type:** Comparison
> **Answer:** Millets, at 90 tonnes, and yes — they are also the smallest share, about 6.2 % of the total.
> **Solution:** The smallest output is millets at 90 tonnes. Total output = 480 + 430 + 460 + 90 = 1460 tonnes, and the millets share is 90/1460 × 100 ≈ 6.16 %. Since the total is the same denominator for every crop, ranking by output and by share always gives the same order; that is why the second question always confirms the first.
> **Key point:** Ranking by value and by percentage share of a common total always agree.

### Q81. `GATE-2`. Three models were produced in two years as shown. Which model had the largest percentage increase, and which had the largest absolute increase?

```
Model | 2019 (units) | 2020 (units)
X     | 2000         | 2450
Y     | 500          | 700
Z     | 800          | 850
```

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) Largest percentage increase: X; largest absolute increase: X
> (b) Largest percentage increase: Y; largest absolute increase: X
> (c) Largest percentage increase: Y; largest absolute increase: Y
> (d) Largest percentage increase: Z; largest absolute increase: Z
> ```
> **Answer:** (b).
> **Solution:** Percentage increases: X = 450/2000 = 22.5 %; Y = 200/500 = 40 %; Z = 50/800 = 6.25 %. So Y leads on percentage. Absolute increases: X = +450, Y = +200, Z = +50, so X leads on absolute gain. The two measures disagree because X started from four times Y's base, so the same rupee effort buys Y a far larger percentage return.
> **Key point:** Percentage rank and absolute rank can and do disagree; always state which measure is meant.

## Section 5. Venn diagrams: two-set and three-set regions

*In every question the diagram is given as a list of labelled regions. A two-set diagram has the regions `A only`, `B only`, `A and B`, `neither`; a three-set diagram has the seven non-empty regions `A only`, `B only`, `C only`, `A∩B only`, `B∩C only`, `A∩C only`, `A∩B∩C`, plus `neither`.*

### Q82. In a survey of 100 students, 45 study physics, 35 study chemistry and 20 study both. How many study neither?

> **Type:** Numerical
> **Answer:** 40 students.
> **Solution:** By inclusion–exclusion, n(P ∪ C) = n(P) + n(C) − n(P ∩ C) = 45 + 35 − 20 = 60. The 20 who study both are counted twice in 45 + 35 = 80, so subtracting them once gives the true union. Those studying neither = 100 − 60 = 40.
> **Key point:** n(A ∪ B) = n(A) + n(B) − n(A ∩ B); the intersection is subtracted because it is counted twice.

### Q83. In the two-set diagram the region values are: `A only` = 28, `B only` = 23, `A and B` = 12, `neither` = 37. What are n(A), n(B) and n(A ∪ B)?

> **Type:** Numerical
> **Answer:** n(A) = 40, n(B) = 35, n(A ∪ B) = 63.
> **Solution:** A circle contains everything inside it, so n(A) = `A only` + `A and B` = 28 + 12 = 40 and n(B) = 23 + 12 = 35. The union is everything except the `neither` region, so n(A ∪ B) = 28 + 23 + 12 = 63. The universal set has 63 + 37 = 100 members, and the overlap of 12 is the single region counted in both circles.
> **Key point:** A circle's total = its "only" region + the shared region; the union = universal set − the "neither" region.

### Q84. Sets A, B and C have n(A) = 50, n(B) = 40, n(C) = 30, n(A ∩ B) = 15, n(B ∩ C) = 12, n(A ∩ C) = 8, n(A ∩ B ∩ C) = 5 and 6 people are in none. Find n(A ∪ B ∪ C).

> **Type:** Numerical
> **Answer:** 96 people.
> **Solution:** The three-set inclusion–exclusion formula is n(A ∪ B ∪ C) = n(A) + n(B) + n(C) − n(A ∩ B) − n(B ∩ C) − n(A ∩ C) + n(A ∩ B ∩ C). Substituting: 50 + 40 + 30 − 15 − 12 − 8 + 5 = 120 − 35 + 5 = 90. Adding the 6 who are in none gives the universal set total of 96. The final +5 restores the all-three group, which was subtracted three times and needs to appear once.
> **Key point:** For three sets: sum the singles, subtract the pairs, add the triple back once.

### Q85. A three-set Venn diagram has the following region values. Find the total number of elements in the union.

```
A only       = 10
B only       = 15
C only       = 8
A∩B only     = 6
B∩C only     = 4
A∩C only     = 3
A∩B∩C        = 5
neither      = 0
```

> **Type:** Numerical
> **Answer:** 51.
> **Solution:** Every element of the union sits in exactly one of the seven non-empty regions, so the union is simply their sum: 10 + 15 + 8 + 6 + 4 + 3 + 5 = 51. Note the trap when reading this back as circle totals: n(A) would be 10 + 6 + 3 + 5 = 24, and adding the three circle totals 24 + 30 + 32 = 86 double-counts the shared regions.
> **Key point:** The union is the sum of the seven disjoint regions; adding circle totals triple-counts overlaps.

### Q86. In a class, n(A) = 30, n(B) = 25 and n(A ∩ B) = 10. What are the values of `A only`, `B only` and `A and B`?

> **Type:** Numerical
> **Answer:** `A only` = 20, `B only` = 15, `A and B` = 10.
> **Solution:** n(A) = `A only` + `A and B`, so `A only` = 30 − 10 = 20. Similarly `B only` = 25 − 10 = 15. The shared region is given as 10. Check: 20 + 15 + 10 = 45 = 30 + 25 − 10, matching inclusion–exclusion. The fourth region, `neither`, cannot be found because the class size is not given.
> **Key point:** Each "only" region is the circle total minus the shared region; subtract the shared part, never the other circle.

### Q87. A ⊆ B and n(B) = 60 while n(A) = 25. What is the value of the region `B only`?

> **Type:** Numerical
> **Answer:** 35.
> **Solution:** If A ⊆ B then every element of A is also in B, so the whole of A lies in the overlap region and `A only` = 0. Hence n(A ∩ B) = 25, and `B only` = n(B) − n(A) = 60 − 25 = 35. Equivalently, n(A ∪ B) = n(B) = 60 because the union of a set with its superset is just the superset.
> **Key point:** When one set is a subset of another, the subset sits entirely inside the overlap and the union equals the larger set.

### Q88. If A ⊆ B, B ⊆ C and n(C) = 90, what is n(A) at most?

> **Type:** Numerical
> **Answer:** 90.
> **Solution:** By transitivity of inclusion, A ⊆ C as well, so A can never contain more elements than C. The maximum is therefore 90, attained when A = C. Anything smaller is possible, so the only statement that must be true is n(A) ≤ 90.
> **Key point:** Subset relations are transitive: A ⊆ B and B ⊆ C together give A ⊆ C, hence n(A) ≤ n(C).

### Q89. `GATE-1`. In a three-set Venn diagram, n(A ∩ B) = 6 and n(A ∩ B ∩ C) = 0. What is the value of the region `A∩B only`?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) 0
> (b) 6
> (c) 3
> (d) It cannot be determined
> ```
> **Answer:** (b) 6.
> **Solution:** The intersection A ∩ B as a whole is made up of the part that is also in C plus the part that is not, that is n(A ∩ B) = `A∩B only` + n(A ∩ B ∩ C). With n(A ∩ B) = 6 and the triple region empty, `A∩B only` = 6 − 0 = 6. The general rule is that the pairwise region is the whole pairwise intersection minus the triple part.
> **Key point:** `A∩B only` = n(A ∩ B) − n(A ∩ B ∩ C), because the triple region is carved out of both pairwise overlaps.

### Q90. The complement of (A ∪ B) is the intersection of the complements. If n(A ∪ B) = 50 and the universal set has 80 elements, what is n(Aᶜ ∩ Bᶜ)?

> **Type:** Numerical
> **Answer:** 30.
> **Solution:** n(Aᶜ ∩ Bᶜ) = n(A ∪ B)ᶜ = 80 − 50 = 30. De Morgan's law makes the complement of a union the intersection of the complements, and the complement of a union is simply the elements outside it. The size depends only on the union, not on how A and B split it internally.
> **Key point:** By De Morgan, (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ, and the size of any complement is |U| minus the size of the set complemented.

### Q91. In a group of 80 people, 30 own a car, 25 own a two-wheeler and 10 own both. How many own neither?

> **Type:** Numerical
> **Answer:** 35 people.
> **Solution:** n(C ∪ T) = 30 + 25 − 10 = 45. The 10 who own both are counted in both the 30 and the 25, so they must be subtracted once. Those owning neither = 80 − 45 = 35. The complementary region Aᶜ ∩ Bᶜ therefore has 35 elements.
> **Key point:** Count the union first, then subtract from the total to get the "neither" region.

### Q92. Two sets are known to be disjoint. If n(A) = 18 and n(B) = 27, what is n(A ∩ B) and n(A ∪ B)?

> **Type:** Numerical
> **Answer:** n(A ∩ B) = 0 and n(A ∪ B) = 45.
> **Solution:** Disjoint sets share no element, so n(A ∩ B) = 0. Inclusion–exclusion then reduces to n(A ∪ B) = 18 + 27 − 0 = 45, which is just the sum of the two sizes because nothing is counted twice. The Venn diagram for this case is two non-touching circles, with no overlap lens.
> **Key point:** For disjoint sets, n(A ∪ B) = n(A) + n(B) exactly; the subtraction term vanishes.

### Q93. How many distinct regions are created by drawing three overlapping circles, ignoring the empty ones?

> **Type:** Conceptual
> **Answer:** 8 regions: the three "only" regions, the three pairwise-only regions, the all-three region, and the outside-everything region.
> **Solution:** Three circles give 3 singly-occupied regions (A only, B only, C only), 3 doubly-occupied regions (A∩B only, B∩C only, A∩C only), 1 triply-occupied region, and 1 region outside all three, making 3 + 3 + 1 + 1 = 8. The general count for n circles is 2ⁿ, so two circles give 4 and four circles would give 16.
> **Key point:** n circles in general position create 2ⁿ regions; for n = 3 that is 8.

### Q94. In a three-set diagram, `A∩B only` = 9 and `A∩C only` = 7 and `A∩B∩C` = 4. What is n(A ∩ B) + n(A ∩ C)?

> **Type:** Numerical
> **Answer:** 24.
> **Solution:** n(A ∩ B) counts the A∩B-only region plus the triple region, so 9 + 4 = 13. Likewise n(A ∩ C) = 7 + 4 = 11. Their sum is 13 + 11 = 24. The triple region is counted twice, once inside each pairwise intersection, which is exactly why 8 appears twice in the arithmetic.
> **Key point:** Each pairwise intersection includes the triple region, so add it to both regions when forming the pairwise totals.

### Q95. `GATE-2`. In a three-set diagram the region values are: `A only` = 14, `B only` = 9, `C only` = 11, `A∩B only` = 5, `B∩C only` = 7, `A∩C only` = 3, `A∩B∩C` = 6. How many elements are in exactly two sets, and how many are in at least two sets?

> **Type:** Numerical `GATE-2`
> **Answer:** Exactly two sets: 15. At least two sets: 21.
> **Solution:** "Exactly two" means the three pairwise-only regions, since those elements lie in two circles and not the third: 5 + 7 + 3 = 15. "At least two" adds the triple region: 15 + 6 = 21. As a check, n(A) = 14 + 5 + 3 + 6 = 28, n(B) = 9 + 5 + 7 + 6 = 27 and n(C) = 11 + 7 + 3 + 6 = 37.
> **Key point:** "Exactly two" excludes the triple region; "at least two" includes it — they differ by n(A ∩ B ∩ C).

### Q96. `GATE-1`. Statements I: n(A ∪ B) = n(A) + n(B) − n(A ∩ B). II: n(A ∪ B) ≤ n(A) + n(B). Which of the following is correct?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Only I is true
> (b) Only II is true
> (c) Both I and II are true
> (d) Neither I nor II is true
> ```
> **Answer:** (c).
> **Solution:** Statement I is the inclusion–exclusion formula and always holds. Statement II follows immediately from it, because n(A ∩ B) ≥ 0 makes the right-hand side of I no greater than n(A) + n(B). Equality in II occurs exactly when the sets are disjoint. Both statements are therefore valid, and II is a direct consequence of I.
> **Key point:** A union never exceeds the sum of the two set sizes; the excess is exactly the double-counted intersection.

## Section 6. Syllogisms: categorical reasoning

*The standard statements and their meanings: "All A are B" means every A is a B (A ⊆ B). "No A is B" means A and B share no member. "Some A are B" means at least one element lies in both. A conclusion follows only if it must be true in **every** situation consistent with the statements — a possibility is not enough.*

### Q97. Statements: All pens are pencils. All pencils are books. Conclusion: All pens are books. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** Take any pen. Since all pens are pencils, it is a pencil. Since all pencils are books, it is a book. So every pen is a book, with no gap in the reasoning. Formally, pens ⊆ pencils ⊆ books implies pens ⊆ books by transitivity. This is the syllogism traditionally called *Barbara*.
> **Key point:** Two universal affirmatives in a chain imply a third: A ⊆ B and B ⊆ C give A ⊆ C.

### Q98. Statements: All pens are pencils. No pencil is a rubber. Conclusion: No pen is a rubber. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** Every pen is a pencil, and the set of pencils is completely disjoint from the set of rubbers. A pen is therefore inside the pencil set and so cannot also be in the disjoint rubber set. This is the form *Celarent*: All A are B and No B is C give No A is C. The disjointness must be stated for the middle term B; disjointness between A and something else would not transfer.
> **Key point:** *Celarent* — "All A are B" plus "No B is C" gives "No A is C".

### Q99. Statements: Some apples are fruits. All fruits are healthy. Conclusion: Some apples are healthy. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** "Some apples are fruits" guarantees at least one apple that is a fruit. Every fruit is healthy, so that particular apple — being a fruit — is healthy. Hence at least one apple is healthy, which is exactly what the conclusion claims. This is the form *Darii*: Some A are B plus All B are C gives Some A are C.
> **Key point:** *Darii* — a particular witness supplied by "Some" can be carried through a universal statement.

### Q100. Statements: All roses are flowers. Some flowers are red. Conclusion: Some roses are red. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** The red flowers might all be daisies, while every rose is white. Nothing in the statements prevents a second, red, set of flowers, so the conclusion is *possible* but not *necessary*. A conclusion that holds in one imagined situation but not in another is not valid. The invalid move here is illicit conversion of "All roses are flowers" into "All flowers are roses".
> **Key point:** A particular exists in the middle term need not be in the whole term; a universal affirmative cannot be converted.

### Q101. Statements: No cats are dogs. All dogs are animals. Conclusion: All cats are animals. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** The statements tell us that cats lie entirely outside dogs, and that dogs lie inside animals. They say nothing about where cats lie: all cats could be animals, or all could be non-animals, or a mix of the two, and both cases satisfy the premises. The disjointness is on the wrong side — it excludes cats from *dogs*, not from animals.
> **Key point:** "No A is B" with "All B are C" does not place A inside C; nothing forces A into C.

### Q102. Statements: All A are B. All B are C. Some C are D. Conclusion: Some D are A. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** The chain places every A inside C, so the C set certainly contains A elements. But the D elements supplied by "Some C are D" may lie in the part of C that is not A. A concrete case: let A = {1}, B = {1}, C = {1, 2}, D = {2}. Every premise holds — A ⊆ B, B ⊆ C, and 2 ∈ C ∩ D — yet no D is an A. The conclusion is not forced.
> **Key point:** A particular in a superset may sit outside the subset, so "Some C are D" never reaches back into A.

### Q103. Statements: Some doctors are engineers. All engineers are graduates. Conclusion: Some doctors are graduates. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** Pick a doctor who is an engineer, whose existence "Some doctors are engineers" guarantees. Every engineer is a graduate, so this doctor is a graduate. At least one doctor is therefore a graduate, which is the conclusion. The reasoning mirrors Q99: a particular introduced by "Some" survives being carried through a universal statement.
> **Key point:** The witness named by "Some A are B" is a real element of B, so any property true of all of B is true of it.

### Q104. Statements: No A is B. Some B are C. Conclusion: Some A are C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** "Some B are C" places a B element in C, and "No A is B" excludes A from B. But that B-and-C element is not in A — indeed, nothing says it is. For a counterexample, take A = {1}, B = {2}, C = {2}. Then A ∩ B = ∅ and B ∩ C = {2} ≠ ∅, so both premises hold, while A ∩ C = ∅ and the conclusion fails.
> **Key point:** Two existential statements about overlapping sets do not join up unless a subset relation connects the terms.

### Q105. Statements: All A are B. No B is C. Conclusion: No A is C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** Any element of A is in B by the first statement. Any element of C is outside B by the second. Since A ⊆ B and C ∩ B = ∅, A and C cannot share an element, which is precisely "No A is C". This is the same *Celarent* form as Q98; the letters are arbitrary and the argument does not depend on what they denote.
> **Key point:** If A is wholly inside B and C is wholly outside B, then A and C are wholly outside each other.

### Q106. Statements: All pens are pencils. Some pencils are blue. Conclusion: Some pens are blue. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** This is the *particular-conclusion* trap in its commonest form. The blue pencils may all be outside the set of pens. Concrete case: pens = {p1, p2}, pencils = {p1, p2, p3}, blue = {p3}. Every premise holds and no pen is blue. The "some" in the premise therefore cannot be transferred across the subset relation in this direction.
> **Key point:** "Some B are C" plus "All A are B" gives "Some A are C"; swapping the two statements breaks the argument.

### Q107. Statements: Some A are not B. All B are C. Conclusion: Some A are not C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** The elements that are in A but not in B might still be in C: the second statement only tells us about B elements, and says nothing about non-B elements. For a counterexample, take A = {1}, B = {2}, C = {1, 2}. Then Some A are not B holds (1 ∉ B), and all B are C holds, but no A is outside C, so the conclusion fails.
> **Key point:** A universal statement about B leaves the non-B part of A completely unconstrained.

### Q108. Statements: All A are B. Some B are not C. Conclusion: Some A are not C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** "Some B are not C" identifies a B element outside C, but it may lie in the part of B that is outside A. Counterexample: A = {1}, B = {1, 2}, C = {1}. Then All A are B holds, and 2 ∈ B with 2 ∉ C so Some B are not C holds, yet every A element is in C and the conclusion is false. The valid arrangement of these two statements is the other way round: "Some A are not C" follows from "Some A are B" with "No B is C".
> **Key point:** A particular must sit in the *narrower* set; a witness from the wider set says nothing about the subset.

### Q109. Statements: No A is B. Some A are C. Conclusion: Some C are not B. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** "Some A are C" gives an element that is in A and in C. "No A is B" says nothing in the whole of A is in B, so that same element is outside B. It is therefore an element of C that is not in B, which is exactly the conclusion. The reasoning is symmetric: some C exists that is excluded from B.
> **Key point:** Combining "Some A are C" with "No A is B" yields "Some C are not B".

### Q110. Statements: All squares are rectangles. All rectangles are quadrilaterals. No circle is a quadrilateral. Conclusion: No square is a circle. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** Chain the two universal affirmatives to place every square inside the set of quadrilaterals. The third statement puts every circle outside that set. A shape cannot be both inside and outside the same set, so no square is a circle. The middle term doing the work is "quadrilateral", which the first two statements put inside and the third puts outside.
> **Key point:** A chain of universals followed by a negative about the final term is a valid *Celarent*-type argument.

### Q111. Statements: Some of the pens are red. No pen is made of plastic. Conclusion: Some of the pens are not made of plastic. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** Yes, the conclusion follows.
> **Solution:** "Some of the pens are red" guarantees at least one pen exists. "No pen is made of plastic" says no pen of any kind is made of plastic, so in particular that guaranteed pen is not. Since the pen has been shown to exist and to be a non-plastic pen, the conclusion follows. The universal negative carries the whole class, not just part of it.
> **Key point:** "Some A exist" plus a property true of *all* A gives that property for at least one A.

### Q112. Statements: Some A are B. Some B are C. Conclusion: Some A are C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** Two "some" statements may refer to completely different elements of B. For a counterexample, A = {1}, B = {1, 2}, C = {2}: element 1 witnesses "Some A are B" and element 2 witnesses "Some B are C", yet A ∩ C = ∅. The overlap required by the conclusion is never asserted.
> **Key point:** "Some A are B" and "Some B are C" need not be witnessed by the *same* element of B.

### Q113. Statements: All A are B. All C are B. Conclusion: All A are C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** Both statements merely place two different groups inside B, side by side, with no relation between them. Counterexample: A = {1}, B = {1, 2}, C = {2}. All A are B and All C are B both hold, but 1 ∉ C, so the conclusion is false. This is the inverse error in its clearest form: two subsets of the same superset need not contain each other.
> **Key point:** Common membership of a superset is not a relation between the subsets themselves.

### Q114. Statements: No A is B. No B is C. Conclusion: No A is C. Does the conclusion follow?

> **Type:** Conceptual
> **Answer:** No, the conclusion does not follow.
> **Solution:** Disjointness is not transitive. Take A = {1}, C = {1} and B = {2}. Then A ∩ B = ∅, so "No A is B" holds, and B ∩ C = ∅, so "No B is C" holds. But A ∩ C = {1} is non-empty, so the conclusion "No A is C" is false. Both premises merely rule out B; they never rule out an element that lies in A and C while avoiding B altogether.
> **Key point:** "No A is B" and "No B is C" give no information about A versus C — three sets can be mutually arranged so that A and C overlap outside B.

### Q115. `GATE-1`. Statements: All economists are graduates. Some graduates are engineers. Conclusion: Some economists are engineers. Which option is correct?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) The conclusion follows
> (b) The conclusion does not follow
> (c) The conclusion follows only if all graduates are economists
> (d) The conclusion follows only if no graduate is an engineer
> ```
> **Answer:** (b).
> **Solution:** "Some graduates are engineers" identifies graduates who are engineers, and the premises nowhere say those particular graduates are economists. Counterexample: economists = {e1}, graduates = {e1, g1}, engineers = {g1}. All premises hold and no economist is an engineer, so the conclusion fails. It would follow from "Some economists are engineers" with "All engineers are graduates", not from the arrangement given.
> **Key point:** The particular must be introduced in the term that the universal covers, at the correct end of the argument.

### Q116. `GATE-1`. Statements: Some books are novels. All novels are fiction. Conclusion: Some books are fiction. Which option is correct?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) The conclusion follows
> (b) The conclusion does not follow
> (c) The conclusion follows only if all books are fiction
> (d) The conclusion follows only if some fiction is a book
> ```
> **Answer:** (a).
> **Solution:** "Some books are novels" gives a book that is a novel. Every novel is fiction, so that book is fiction. Hence some book is fiction, which is the conclusion — the form *Darii*. Option (d) is a trap: "Some fiction is a book" is the same claim restated and adds nothing; the conclusion is already established by the premises.
> **Key point:** *Darii* needs no extra assumption; the conclusion is already entailed.

### Q117. `GATE-2`. Statements: All A are B. No B is C. Some A are D. Conclusions: I — Some A are not C. II — No A is C. Which conclusion(s) follow?

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) Only I follows
> (b) Only II follows
> (c) Both I and II follow
> (d) Neither I nor II follows
> ```
> **Answer:** (c).
> **Solution:** All A are B and no B is C give, by *Celarent*, that no A is C — so II follows. Since "Some A are D" guarantees that A is not empty, at least one A exists, and that element is not in C, which establishes I. The two conclusions are not redundant: II is the universal statement while I is the existential one, and I depends on the extra premise "Some A are D" while II does not.
> **Key point:** A universal negative conclusion needs only the two universal premises; the existential conclusion also needs A to be non-empty.

### Q118. `GATE-2`. Statements: Some A are B. All B are C. No C is D. Conclusions: I — Some A are C. II — Some A are not D. Which conclusion(s) follow?

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) Only I follows
> (b) Only II follows
> (c) Both I and II follow
> (d) Neither I nor II follows
> ```
> **Answer:** (c).
> **Solution:** "Some A are B" gives an element x in A ∩ B. All B are C, so x ∈ C, establishing I. No C is D, so x ∉ D, which — since x is in A — establishes II. Both conclusions are about the same witness element, which is why both hold; the argument is *Darii* followed by an application of the negative universal to that element.
> **Key point:** One witness element can satisfy several conclusions at once when it is carried through a chain of universals.

## Section 7. Blood relations: family-tree reasoning

*Every family here is described in words, and each relationship is a single fixed parent–child link unless stated otherwise. "A is the son of B" makes A male; "the daughter of" makes the person female. Where a person's gender is not stated, the answer may depend on it, and this is flagged explicitly.*

### Q119. A is the brother of B. B is the daughter of C. C has only one child. How is A related to C?

> **Type:** Conceptual
> **Answer:** A is the son of C.
> **Solution:** B is C's child, and C has only one child, so B is the only child. A is B's brother, that is, a child of the same parents as B — and a brother is male. Since A is also C's child and is male, A is C's son. The "only one child" detail is what forces A to be a child of C rather than merely B's sibling by some other route.
> **Key point:** A sibling of someone's child is that person's child; the sibling's gender fixes son or daughter.

### Q120. P is the son of Q. Q is the sister of R. R is the father of S. How is P related to S?

> **Type:** Conceptual
> **Answer:** P is the cousin of S.
> **Solution:** Q and R are siblings. P is Q's child, so P is one of the children of R's sister, while S is R's own son. The children of one's siblings are cousins, so P and S are cousins. Nothing in the statements makes them brothers, since the two parents are not the same pair.
> **Key point:** Children of a parent's siblings are cousins; siblings' children are never siblings to each other.

### Q121. A is the son of B. B is the daughter of C. C is the son of D. How is A related to D?

> **Type:** Conceptual
> **Answer:** A is the grandson of D.
> **Solution:** C is D's son. B is C's daughter, making B the next generation down. A is B's son, one generation below that. Counting up from A: A's parent is B, B's parent is C, and C's parent is D — three links, so D is A's grandparent. Since A is male, the specific term is grandson.
> **Key point:** Count parent–child links: one link = parent, two = grandparent, three = great-grandparent.

### Q122. M is the mother of N. N is the brother of O. O is the daughter of P. How is M related to O?

> **Type:** Conceptual
> **Answer:** M is the mother of O.
> **Solution:** N and O are siblings, and M is N's mother. The children of a couple share both parents, so M is also O's mother — this is the usual convention, since the problem already identifies P as a parent of O and a child has only one mother. The word "brother" for N and "daughter" for O guarantee they are siblings of the same generation, so the same mother applies to both.
> **Key point:** Siblings share both parents, so a mother of one is the mother of the other.

### Q123. R is the father of T. T is the daughter of S, and S is the wife of R. What is the relation of S to T?

> **Type:** Conceptual
> **Answer:** S is the mother of T.
> **Solution:** S is expressly stated to be R's wife, and R is expressly T's father. A man's wife is his children's mother, and S is also named as a parent of T in "T is the daughter of S". All three statements agree, so S is T's mother. Notice that no inference was needed beyond reading the direct statement.
> **Key point:** When a statement names a parent directly, prefer it over any inference that could be drawn from another relationship.

### Q124. J is the husband of K. K is the daughter of L. M is the son of L. How is M related to J?

> **Type:** Conceptual
> **Answer:** M is the brother-in-law of J.
> **Solution:** J is married to K, so J's wife's brother is his brother-in-law. M is a son of L and K is L's daughter, so M and K are siblings. Hence M is the brother of J's wife, that is J's brother-in-law. The "husband" wording fixes J as the spouse side of the relationship, which is why the answer is in-law rather than a blood relation.
> **Key point:** A blood relation to one's spouse is an in-law relation, named for the spouse's relative.

### Q125. Pointing to a woman, Neha said, "Her mother is the only daughter of my mother." How is the woman related to Neha?

> **Type:** Conceptual
> **Answer:** The woman is the sister of Neha.
> **Solution:** Neha's mother has exactly one daughter — and since Neha is that mother's daughter, the only daughter is Neha herself. So the woman's mother is Neha. A girl whose mother is Neha is Neha's daughter, and since the person pointed at is a woman, she is Neha's sister. The chain is: woman's mother = Neha's mother = Neha.
> **Key point:** "The only daughter of my mother" is the speaker herself, so the person described is the speaker's sibling.

### Q126. A's father is B's brother. How is A related to B?

> **Type:** Conceptual
> **Answer:** It cannot be determined; A may be B's brother or B's sister.
> **Solution:** B's brother is a male sibling of B, and A is that brother's child. Whether A is male or female is never stated. If A is a boy, he and B are both children of the same pair of parents, so A is B's brother. If A is a girl, A is B's sister. Both possibilities satisfy every statement, so no single relationship can be asserted.
> **Key point:** When the gender of the person is not stated, a sibling relationship has two possible answers and the question is undetermined.

### Q127. Ravi's mother is the only daughter of Mr. Suresh. How is Ravi related to Mr. Suresh?

> **Type:** Conceptual
> **Answer:** Ravi is the grandson of Mr. Suresh.
> **Solution:** Mr. Suresh's only daughter is Ravi's mother, so Ravi's mother is a daughter of Mr. Suresh. Ravi is one generation below his mother, making Mr. Suresh Ravi's maternal grandfather. The phrase "only daughter" also excludes Ravi having a maternal uncle, but the grandfather link holds regardless.
> **Key point:** A link through the mother is a maternal grandparent, through the father a paternal one.

### Q128. If P is the son of Q, Q is the son of R and R is the brother of S, how is S related to P?

> **Type:** Conceptual
> **Answer:** S is the great-uncle of P.
> **Solution:** P's father is Q, and Q's father is R, so R is P's grandfather. S is R's brother, which places S one generation above the grandparent level. A grandparent's brother is a great-uncle, since counting up from P, S sits three links away along the sibling line. It is worth noticing that the usual exam trap is to answer "uncle" by analogy with the single-generation case, but here the middle term already sits two generations up.
> **Key point:** A grandparent's sibling is a great-uncle, not an uncle — always count the generation of the middle term first.

### Q129. X is the mother of Y. Y is the brother of Z. Z is the mother of W. How is X related to W?

> **Type:** Conceptual
> **Answer:** X is the grandmother of W.
> **Solution:** Y and Z are siblings, and X is Y's mother, so X is also Z's mother by the shared-parent convention. Z is W's mother, so W's mother is X's daughter, making X the grandmother of W. Two parent–child links separate X from W, which is the definition of a grandparent.
> **Key point:** Count upward links from the person: one parent, two grandparent.

### Q130. `GATE-1`. P and Q are brothers. R is the son of P. S is the son of Q. How is S related to R?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Brother
> (b) Cousin
> (c) Nephew
> (d) Uncle
> ```
> **Answer:** (b) Cousin.
> **Solution:** P and Q are brothers, so they are a sibling pair and each is the other one's parent of children. R is P's son and S is Q's son, so R and S are the children of two brothers. Children of siblings are cousins. Options (a) and (c) would require R and S to be in the same generation with one being the other's parent's sibling, and option (d) would require S to be in an older generation than R — none of which the statements support.
> **Key point:** Two children of two brothers are cousins; they are never brothers to each other.

### Q131. `GATE-1`. A says to B, "Your mother's husband is my father." How is A related to B?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) A is B's brother
> (b) A is B's father
> (c) A is B's maternal uncle
> (d) A is B's maternal grandfather
> ```
> **Answer:** (a) A is B's brother.
> **Solution:** "Your mother's husband" is B's father, since a woman's husband is her children's father. A says this man is A's own father. So B's father and A's father are the same man, which makes A and B children of the same parents. A refers to himself as a man, hence a male child, so A is B's brother. Option (c) would be right if A were the mother's *brother* rather than her husband.
> **Key point:** "Your mother's husband" is your father, not your uncle — a common but decisive misreading.

### Q132. `GATE-1`. F is the daughter of G, and G is the husband of H. How is H related to F?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Father
> (b) Brother
> (c) Husband
> (d) Maternal grandfather
> ```
> **Answer:** (a) Father.
> **Solution:** G is F's parent (stated directly), and G is H's husband. A man's wife is his children's mother, so H is also a parent of F. H is male, being G's husband, so H is F's father. Two parents per child is the standard convention, and no statement contradicts it.
> **Key point:** A spouse of a parent is the child's other parent, and the gender of the spouse fixes which one.

### Q133. K is the son of L. L is the sister of M. M is the daughter of N. How is K related to N?

> **Type:** Conceptual
> **Answer:** K is the grandson of N.
> **Solution:** L and M are siblings. M is N's daughter, so N is the parent of M. Since L and M share both parents, N is also L's parent. K is L's son, one generation below. N is therefore K's grandparent, and because the chain runs through K's mother L, N is a maternal grandfather of K.
> **Key point:** Siblings share parents, so a relation established through one sibling holds for the other.

### Q134. Two families are described: in the first, X is the son of Y, and in the second, Z is the son of W, with Y and W being sisters. How is X related to Z?

> **Type:** Conceptual
> **Answer:** X is the cousin of Z.
> **Solution:** Y and W are sisters, so Y is a sibling of Z's father W. X is Y's son, and Z is W's son. The children of two siblings — here one sister Y and one brother W — are cousins. This mirrors Q120 but with the parents of the same gender, which changes nothing: the cousin relation follows from the parents being siblings.
> **Key point:** It is the *parents'* relationship that determines the children's relationship, not the parents' genders.

### Q135. `GATE-1`. Pointing to a man, Meera said, "He is the son of my grandfather's only son." How is the man related to Meera?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) Brother
> (b) Father
> (c) Nephew
> (d) Uncle
> ```
> **Answer:** (a) Brother.
> **Solution:** Meera's grandfather's only son is Meera's father, since a grandfather's son is a father and the "only son" condition rules out uncles. The man's mother is therefore Meera's mother, making him a child of Meera's parents — that is, Meera's brother, as he is male. Note the structural trap: the phrase does not name a generation explicitly, so the chain must be followed link by link rather than read as "grandson".
> **Key point:** "My grandfather's only son" is my father; a son of my father is my brother.

---

## Section 8. Direction sense: compass problems and displacement

*The convention used throughout: North is up, East is right, South is down and West is left. A turn to the **right** (or clockwise) of 90° moves N→E→S→W; a turn to the **left** (anticlockwise) of 90° reverses that. On a clock face 12 o'clock is North, 3 o'clock is East, 6 o'clock is South and 9 o'clock is West.*

### Q136. A person facing North turns 90° to the right and then 45° to the left. Which direction is he now facing?

> **Type:** Numerical
> **Answer:** North-East.
> **Solution:** From North a right turn of 90° gives East. From East a left turn of 45° gives the compass point halfway between East and North, which is North-East. Measuring clockwise from North: the first turn reaches 90° and the second subtracts 45°, leaving 45°, and 45° is North-East.
> **Key point:** Right turns add degrees clockwise, left turns subtract them, measured from North.

### Q137. A person facing South turns 90° to the right. Which direction is he now facing?

> **Type:** Conceptual
> **Answer:** West.
> **Solution:** Turning right means turning clockwise. Starting from South (180° clockwise from North), adding 90° gives 270°, which is West. A useful check: facing South, your right hand points to the West, exactly as facing North your right hand points East.
> **Key point:** Right turn from South gives West; the four clockwise turns are N→E→S→W→N.

### Q138. A man walks 4 km due North and then 3 km due East. How far is he from the starting point, and in which direction?

> **Type:** Numerical
> **Answer:** 5 km, in the direction North-East.
> **Solution:** The two legs are perpendicular, so the straight-line displacement is the hypotenuse of a right triangle: √(4² + 3²) = √(16 + 9) = √25 = 5 km. Since he has moved both North and East, the displacement points North-East. The distance actually walked, 4 + 3 = 7 km, is larger than the 5 km displacement, as it always is when the path changes direction.
> **Key point:** Displacement is the straight-line start-to-finish distance, not the total distance walked.

### Q139. A woman walks 5 km due South, then 4 km due East, then 3 km due North. What is her displacement from the start?

> **Type:** Numerical
> **Answer:** ≈ 4.47 km, in the direction South-East.
> **Solution:** Net North–South movement is 5 − 3 = 2 km South, since the 3 km North partly cancels the 5 km South. Net East–West movement is 4 km East. The displacement is √(2² + 4²) = √(4 + 16) = √20 ≈ 4.47 km, pointing South-East. The total walked is 5 + 4 + 3 = 12 km, far more than the 4.47 km net separation.
> **Key point:** Cancel opposing North–South and East–West moves first, then apply Pythagoras to what remains.

### Q140. A person facing East turns around through 180° and then turns 90° to the left. Which direction is he now facing?

> **Type:** Conceptual
> **Answer:** South.
> **Solution:** A 180° turn from East gives West. A left turn of 90° from West, measured anticlockwise, gives South. In degree terms: East is 90° clockwise from North, +180° gives 270° (West), and −90° gives 180° (South).
> **Key point:** A 180° turn reverses the facing; a left turn from West goes to South.

### Q141. A man walks 3 km North, turns right and walks 4 km, then turns left and walks 3 km. How far and in which direction is he from the start?

> **Type:** Numerical
> **Answer:** ≈ 7.21 km, in the direction North-East.
> **Solution:** After 3 km North he is at (east 0, north 3). Facing North, a right turn faces East, so 4 km East takes him to (4, 3). Facing East, a left turn faces North, so the final 3 km takes him to (4, 6). The displacement is √(4² + 6²) = √(16 + 36) = √52 ≈ 7.21 km towards North-East. The total walked is 10 km.
> **Key point:** Track position in (east, north) coordinates; turns change the facing, not the position.

### Q142. At what time does the hour hand of a clock point in the direction North-East?

> **Type:** Numerical
> **Answer:** 1:30.
> **Solution:** The hour hand makes a full 360° turn in 12 hours, so it sweeps 30° per hour. North-East is 45° clockwise from 12 o'clock, and 45/30 = 1.5 hours after 12 is 1:30, at which moment the hand points exactly halfway between 1 and 2. The minute hand is irrelevant to the question.
> **Key point:** The hour hand moves 30° per hour, so a compass direction converts to a clock time by dividing its angle by 30.

### Q143. In the northern hemisphere on a clear day, in which direction does a vertical object's shadow point at 9:00 a.m.?

> **Type:** Conceptual
> **Answer:** West.
> **Solution:** The Sun rises in the East and travels across the southern sky, so at 9:00 a.m. it is still in the eastern part of the sky. A shadow always points directly away from the Sun, so at that hour it points West. A shadow points East at 6:00 p.m., and is shortest around solar noon when the Sun is highest.
> **Key point:** A shadow points opposite the Sun; with the Sun in the East in the morning, morning shadows point West.

### Q144. A person facing South turns 90° anticlockwise. Which direction is he now facing?

> **Type:** Conceptual
> **Answer:** East.
> **Solution:** An anticlockwise (left) turn from South moves against the clockwise order N→E→S→W, so from South it goes to East. In degrees: South is 180° clockwise from North, and a left turn subtracts 90°, giving 90°, which is East. As a physical check, facing South your left hand points East.
> **Key point:** Anticlockwise from South gives East — the reverse of the clockwise turn, which gives West.

### Q145. A boy walks 10 m North, 6 m East, 6 m South and 6 m West. Where does he end up relative to the start?

> **Type:** Numerical
> **Answer:** 4 m due North of the starting point.
> **Solution:** The 6 m East and 6 m West cancel exactly, and the 6 m South partly cancels the 10 m North, leaving 10 − 6 = 4 m North. The boy is therefore 4 m due North of the start — he has "returned" on one axis but not the other. The total distance walked is 28 m for a net 4 m.
> **Key point:** In a walk that looks closed, opposing legs still leave a residual; cancel them first instead of adding all legs.

### Q146. Two friends start from the same point. A walks 6 km North and B walks 8 km East. How far apart do they end up, and in which direction is B from A?

> **Type:** Numerical
> **Answer:** They are 10 km apart, and B is to the South-East of A.
> **Solution:** Put the start at the origin: A ends 6 km North and B ends 8 km East. The separation is √(6² + 8²) = √(36 + 64) = √100 = 10 km. Relative to A, B lies 8 km East and 6 km South, so B is to the South-East of A. The statement is not symmetric — A is to the North-West of B — and both descriptions are correct at once.
> **Key point:** "X is in which direction of Y" fixes X as the starting point of the vector; the reverse statement gives the opposite compass point.

### Q147. P is 5 km due East of Q. R is 12 km due North of P. How far is R from Q, and in which direction?

> **Type:** Numerical
> **Answer:** 13 km, in the direction North-East.
> **Solution:** Taking Q as the origin, P is at (5, 0) in (east, north) coordinates and R is at (5, 12). The displacement from Q is √(5² + 12²) = √(25 + 144) = √169 = 13 km, and since both coordinates are positive R lies to the North-East of Q. The route taken was two legs of 5 km and 12 km, but the single straight-line distance asked for is 13 km.
> **Key point:** Locate the final point in coordinates, then take the straight-line distance from the origin, not the two-leg route.

### Q148. A person facing North turns 135° in the clockwise direction. Which direction is he now facing?

> **Type:** Numerical
> **Answer:** South-East.
> **Solution:** Measured clockwise from North, 90° is East and 180° is South. A turn of 135° lies between the two, so the direction is the intermediate compass point, South-East. Compass points fall at 45° intervals: 0° N, 45° NE, 90° E, 135° SE, 180° S, 225° SW, 270° W, 315° NW.
> **Key point:** Compass points sit at multiples of 45° clockwise from North; 135° is South-East.

### Q149. How many degrees are in a full turn, a right angle and a straight angle?

> **Type:** Conceptual
> **Answer:** A full turn is 360°, a right angle is 90°, and a straight angle is 180°.
> **Solution:** A full turn brings a ray back to its starting direction, so it measures 360°. A quarter of that — a right angle — is 90°, which is also the angular gap between two adjacent cardinal compass directions. Half of a full turn — a straight angle — is 180°, the amount needed to reverse one's facing.
> **Key point:** Full turn 360° = 4 right angles = 2 straight angles; adjacent compass points are 90° apart.

### Q150. A clock shows 5:20. In which direction does the minute hand point?

> **Type:** Numerical
> **Answer:** South-East.
> **Solution:** The minute hand completes a full circle in 60 minutes, so 20 minutes corresponds to 20/60 × 360° = 120° clockwise from 12. On the clock face, 3 o'clock (90°) is East and 6 o'clock (180°) is South, and 120° lies between them, on the South-East diagonal. The hour hand's position is irrelevant, since only the minute hand is being asked about.
> **Key point:** Minute-hand angle = minutes × 6°, read clockwise from 12 o'clock, which is North.

### Q151. A man walks 4 km West, turns right and walks 3 km North, then turns right and walks 4 km East. Where is he relative to the start?

> **Type:** Numerical
> **Answer:** 3 km due North of the starting point.
> **Solution:** Start at (0, 0) in (east, north) coordinates. Walking 4 km West gives (−4, 0); facing West, a right turn faces North, so 3 km North gives (−4, 3); facing North, a right turn faces East, so 4 km East gives (0, 3). The net displacement is 3 km due North — the 4 km West is exactly undone by the 4 km East, leaving only the northward leg. The total walked is 11 km.
> **Key point:** Equal opposing legs cancel exactly, so only the unbalanced component survives in the net displacement.

### Q152. `GATE-1`. A person facing North turns 45° anticlockwise and then 90° clockwise. Which direction is he now facing?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) North-West
> (b) North-East
> (c) North
> (d) West
> ```
> **Answer:** (b) North-East.
> **Solution:** From North, a 45° anticlockwise turn reaches North-West, that is −45° measured clockwise from North. Adding the 90° clockwise turn gives −45 + 90 = +45° clockwise from North, which is North-East. The two turns do not cancel because they are of different sizes — the net effect is a single 45° clockwise turn from the starting direction.
> **Key point:** Convert both turns into one signed measure from North (anticlockwise negative, clockwise positive) and add them.

---

## Section 9. Coding–decoding: letter codes, number codes and mixed codes

*Each question defines its own coding rule explicitly. A code is only worth solving once you can restate the rule in one sentence, and the answer must be re-encodable using that same rule.*

### Q153. In a certain code, the first and the last letter of the alphabet are interchanged, the second and the second-last are interchanged, and so on (A↔Z, B↔Y, C↔X, …). Under this code, what does MATE become?

> **Type:** Numerical
> **Answer:** NZGV.
> **Solution:** The rule maps a letter to its mirror image in the alphabet, A(1)↔Z(26), B(2)↔Y(25), and so on, so the partner of a letter of position p is position 27 − p. M(13) maps to 27 − 13 = 14 = N; A(1) maps to 26 = Z; T(20) maps to 7 = G; E(5) maps to 22 = V. The coded word is NZGV. This code is its own inverse, so decoding uses exactly the same step.
> **Key point:** The mirror code replaces position p by 27 − p, and is its own inverse.

### Q154. In a certain code, every letter is replaced by the letter two places after it in the alphabet, with X, Y and Z wrapping round to A, B and C. If MATRIX is coded as OCVTKZ, how is COMET coded?

> **Type:** Numerical
> **Answer:** EQOGV.
> **Solution:** Apply the shift of +2 to each letter of COMET: C→E, O→Q, M→O, E→G, T→V. The code is therefore EQOGV. The given example confirms the rule — M→O, A→C, T→V, R→T, I→K, X→Z all agree with a shift of two places.
> **Key point:** A uniform letter shift is verified by re-encoding the supplied example before applying it to the new word.

### Q155. In a certain code, a word is first written in reverse order and then every letter is moved one place forward in the alphabet. How is STAGE coded?

> **Type:** Numerical
> **Answer:** FHBUT.
> **Solution:** STAGE reversed is EGATS. Shifting each letter one place forward gives E→F, G→H, A→B, T→U, S→T, giving FHBUT. Reversal and a uniform letter shift do commute here: shifting STAGE first gives TUBHF, whose reverse is FHBUT, the same code. That is a useful check, since it means an order slip would not change the answer for this particular word.
> **Key point:** Reversal and a uniform shift commute, so their order is irrelevant — but always write the intermediate string to be sure which one the question asked for.

### Q156. In a certain code, a word is replaced by the sum of the alphabetical positions of its letters (A = 1, …, Z = 26). If CAT is coded as 24, how is DOG coded?

> **Type:** Numerical
> **Answer:** 26.
> **Solution:** The example checks the rule: C + A + T = 3 + 1 + 20 = 24. Applying the same sum, D + O + G = 4 + 15 + 7 = 26. Note that the code carries no information about the order of the letters, so it is a poor code — CAT, ACT and TAC all give 24.
> **Key point:** A sum-of-positions code is order-insensitive, so anagrams become indistinguishable.

### Q157. In a certain code, every vowel is replaced by its position in the alphabet as a digit, and every consonant is replaced by the next letter in the alphabet. How is BRAVE coded, and how is CHAIR coded under the same rule?

> **Type:** Numerical
> **Answer:** BRAVE is coded as CS1W5, and CHAIR as DI19S.
> **Solution:** For BRAVE: B is a consonant, so → C; R is a consonant, so → S; A is a vowel of position 1, so → 1; V is a consonant, so → W; E is a vowel of position 5, so → 5. The code is CS1W5. For CHAIR: C→D, H→I, A→1, I→9 (a vowel, so it becomes a digit, not a letter), R→S, giving DI19S. The I in CHAIR is the test of the rule.
> **Key point:** Check whether a letter is a vowel before shifting it; A, E, I, O and U never become shifted letters.

### Q158. In a certain code, a word is written as its number of letters, followed by its first letter, followed by its last letter. Under this rule, MONKEY becomes 6MY. How is ORANGE coded?

> **Type:** Numerical
> **Answer:** 6OE.
> **Solution:** ORANGE has 6 letters, begins with O and ends with E, so its code is 6OE. The supplied example checks the rule: MONKEY has 6 letters, starts with M and ends with Y, giving 6MY. The middle letters contribute only through the length, so BAN and BAT both code as 3BT.
> **Key point:** A code using only length and the end letters discards the interior of the word entirely.

### Q159. In a certain code, every letter is moved three places back in the alphabet and the resulting word is then written in reverse order. How is HOUSE coded?

> **Type:** Numerical
> **Answer:** BPRLE.
> **Solution:** Moving each letter three places back gives H→E, O→L, U→R, S→P, E→B, producing ELRPB. Reversing that gives BPRLE. Checking letter by letter, every character of BPRLE is three places *after* the corresponding character of HOUSE read backwards, which is exactly the code reversed back.
> **Key point:** A shift followed by a reversal can be undone by reversing first and then shifting the opposite way.

### Q160. In a certain code, the code for a word is the product of its number of letters and its number of vowels. Under this rule BAT = 3, SHIP = 4 and TEEN = 8. How is CHAIR coded?

> **Type:** Numerical
> **Answer:** 10.
> **Solution:** CHAIR has 5 letters (C, H, A, I, R) and 2 vowels (A and I), so the code is 5 × 2 = 10. The three given examples confirm the rule: BAT is 3 × 1 = 3, SHIP is 4 × 1 = 4, and TEEN is 4 × 2 = 8.
> **Key point:** When a code is a product of two counts, count both quantities carefully before multiplying.

### Q161. In a certain code, every letter is replaced by the next letter in the alphabet. Under this rule, CAT is coded as DBU. How is DARK coded?

> **Type:** Numerical
> **Answer:** EBSL.
> **Solution:** Move each letter one place forward: D→E, A→B, R→S, K→L, giving EBSL. The example confirms the rule: C→D, A→B, T→U is exactly DBU. This is the simplest possible code and, like every fixed-shift code, it fails only at Z, which would have to wrap to A.
> **Key point:** The simplest letter code is a shift by one; confirm with the supplied example, then apply it to the new word.

### Q162. In a certain code, a word is written as three numbers: the number of vowels, the number of consonants, and the total number of letters. Under this rule STUDENT becomes 2-5-7. How is ENGINEERING coded?

> **Type:** Numerical
> **Answer:** 5-6-11.
> **Solution:** ENGINEERING has 11 letters: E, N, G, I, N, E, E, R, I, N, G. The vowels are E, I, E, E and I — 5 of them — and the remaining N, G, N, R, N, G are 6 consonants. The code is therefore 5-6-11, and 5 + 6 = 11 confirms the total. The example STUDENT has vowels U and E (2) and consonants S, T, D, N, T (5), giving 2-5-7.
> **Key point:** Y is a vowel only when it functions as one; here the vowel and consonant counts must always sum to the length.

### Q163. In a certain code, a word is written with its odd-position letters first and its even-position letters afterwards. Under this rule FISH becomes FSIH. How is TIGER coded?

> **Type:** Numerical
> **Answer:** TGRIE.
> **Solution:** Number the positions of TIGER: 1=T, 2=I, 3=G, 4=E, 5=R. The odd positions 1, 3, 5 give T, G, R and the even positions 2, 4 give I, E, so the code is TGRIE. The example FISH checks the rule: positions 1, 3 are F, S and positions 2, 4 are I, H, giving FSIH.
> **Key point:** Interleaved rearrangements are easiest to verify by numbering the positions of the original word first.

### Q164. In a certain code, each vowel is replaced by the next letter of the alphabet and each consonant by the previous letter. Under this rule ROAD becomes QPBC. How is CREAM coded?

> **Type:** Numerical
> **Answer:** BQFBL.
> **Solution:** CREAM is C (consonant → B), R (consonant → Q), E (vowel → F), A (vowel → B), M (consonant → L), giving BQFBL. The supplied example confirms the direction of each rule: R→Q and D→C are consonants moving back, while O→P and A→B are vowels moving forward.
> **Key point:** Opposite rules for vowels and consonants mean you must classify every letter before substituting.

### Q165. In a certain code, the odd numbers 1, 3, 5, 7, 9, 11, 13, 15, … are written as A, B, C, D, E, F, G, H, … respectively. How is 21 written in this code?

> **Type:** Numerical
> **Answer:** K.
> **Solution:** The code assigns the n-th letter of the alphabet to the n-th odd number: 1st odd = 1 → A, 2nd = 3 → B, 3rd = 5 → C, and so on. The 11th odd number is 21, because the n-th odd number is 2n − 1 and 2(11) − 1 = 21. The 11th letter is K, so 21 is written as K. Equivalently, the letter index n equals (number + 1)/2.
> **Key point:** The n-th odd number is 2n − 1, so the letter index is (number + 1)/2.

### Q166. In a certain code, a word of n letters has every letter shifted n places forward in the alphabet. Under this rule, BAT becomes EDW. How is MICE coded?

> **Type:** Numerical
> **Answer:** QMGI.
> **Solution:** BAT has 3 letters, so each letter shifts 3 forward: B→E, A→D, T→W, giving EDW — the supplied example. MICE has 4 letters, so each shifts 4: M→Q, I→M, C→G, E→I, giving QMGI. The shift amount is set by the word's own length, so it differs from word to word and cannot be carried over from the example.
> **Key point:** A shift keyed to the word's length must be recomputed for every new word.

### Q167. In a certain code, letters A to M are each moved three places forward in the alphabet, while letters N to Z are each moved three places back. Under this rule, HANDS becomes KDKGP. How is CHAIR coded?

> **Type:** Numerical
> **Answer:** FKDLO.
> **Solution:** CHAIR is C (A–M → F), H (A–M → K), A (A–M → D), I (A–M → L), R (N–Z → O), giving FKDLO. The example checks the rule in both halves: H→K and D→G are forward moves, while N→K and S→P are backward moves, so a word may mix both directions in one code.
> **Key point:** A rule that switches behaviour at a letter boundary must be applied letter by letter, not word by word.

### Q168. In a certain code the alphabet is reordered as K, E, Y, W, O, R, D, A, B, C, F, G, H, I, J, L, M, N, P, Q, S, T, U, V, X, Z, and letters are replaced by the letter occupying the same position in this reordered list. How is MANGO coded?

> **Type:** Numerical
> **Answer:** QHPLO.
> **Solution:** Number the reordered list: K1, E2, Y3, W4, O5, R6, D7, A8, B9, C10, F11, G12, H13, I14, J15, L16, M17, N18, P19, Q20, S21, T22, U23, V24, X25, Z26. M sits at position 17, which holds Q; A is at position 8, holding H; N is at position 18, holding P; G is at position 12, holding L; O is at position 5, holding O. The code is QHPLO.
> **Key point:** A keyword cipher is just a lookup table: find the letter's slot, then read off what occupies that slot.

### Q169. In a certain code, the first two letters of a word are interchanged and all other letters keep their positions. Under this rule, TIGER becomes ITGER. How is SPARK coded?

> **Type:** Numerical
> **Answer:** PSARK.
> **Solution:** SPARK has S in position 1 and P in position 2. Interchanging them puts P first and S second, leaving A, R and K untouched, which gives PSARK. The supplied example shows the same swap in TIGER, where T and I trade places to give ITGER.
> **Key point:** A fixed-position swap is checked by confirming that every other letter is untouched.

### Q170. In a certain code, each letter is replaced by the number of letters in the English name of that letter. Under this rule, B is coded 3 (as in "bee") and E is coded 2 (as in "ee"). How is FEED coded?

> **Type:** Numerical
> **Answer:** 2-2-2-3.
> **Solution:** F is named "ef", 2 letters, so → 2; E is named "ee", 2 letters, so → 2; E again → 2; D is named "dee", 3 letters, so → 3. The code is therefore 2-2-2-3. The two given examples fix the convention: single-letter names like A ("a") give 1, so the code is never zero.
> **Key point:** A name-based code needs a stated convention for the letter names themselves, since "B" and "bee" differ in length.

### Q171. In a certain code, each letter of a word is replaced by its alphabetical position and the resulting numbers are then written in reverse order. Under this rule, GIVE is coded as 5-22-9-7. How is LAMP coded?

> **Type:** Numerical
> **Answer:** 16-13-1-12.
> **Solution:** LAMP has positions L=12, A=1, M=13, P=16, giving the forward list 12-1-13-16. Reversing the order gives 16-13-1-12. The example GIVE checks the rule: G=7, I=9, V=22, E=5 forwards is 7-9-22-5, and reversed it is 5-22-9-7, exactly as given.
> **Key point:** Reversing a sequence of numbers is the mirror operation of reversing a word; check the direction against the supplied example.

### Q172. `GATE-2`. In a certain code, a word beginning with a vowel has its first and last letters interchanged; a word beginning with a consonant is written in full reverse order. Under this rule, APPLE becomes EPPLA and PEN becomes NEP. How is ORANGE coded?

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) ERANGO
> (b) EGNARO
> (c) ORANGE
> (d) OGRANE
> ```
> **Answer:** (a) ERANGO.
> **Solution:** ORANGE begins with O, a vowel, so only the first and last letters are interchanged. Starting from O R A N G E, the ends swap to give E R A N G O, that is ERANGO, with R, A, N and G untouched. Option (b), EGNARO, is the *full* reversal, which is the branch reserved for consonant-initial words such as PEN and so does not apply here. Option (c) applies no rule at all, and option (d) swaps the first two letters, a different operation again.
> **Key point:** A conditional code must branch on the stated condition before applying the rule; PEN shows the consonant branch produces a full reversal.

---

## Section 10. Series completion, alphanumeric series and figure problems

*In every question the figure or series is written out completely in the question text, so nothing has to be looked up. For series, always compute the differences (first differences, then second differences) before guessing a rule, and check that the rule reproduces every term already given.*

### Q173. Find the next term: 2, 6, 12, 20, 30, ?

> **Type:** Numerical
> **Answer:** 42.
> **Solution:** The first differences are 4, 6, 8, 10, which themselves rise by 2 each time — the series is built on consecutive even numbers, being 2×1, 2×3, 2×5, 2×7, 2×9. The next term is 2×11 = 22, added to 30 to give 42. A constant second difference of 2 is the signature of a quadratic pattern and is the most reliable test.
> **Key point:** A series with constant second differences follows a quadratic rule; add the next difference to the last term.

### Q174. Find the next term: 3, 6, 11, 18, 27, ?

> **Type:** Numerical
> **Answer:** 38.
> **Solution:** The first differences are 3, 5, 7, 9 — consecutive odd numbers. The next difference is 11, so the next term is 27 + 11 = 38. As a check, the terms are n² + 2: 1 + 2 = 3, 4 + 2 = 6, 9 + 2 = 11, 16 + 2 = 18, 25 + 2 = 27, 36 + 2 = 38.
> **Key point:** When first differences run through consecutive odd numbers, the rule is n² + c, verifiable at every index.

### Q175. Find the next term: 1, 2, 6, 24, 120, ?

> **Type:** Numerical
> **Answer:** 720.
> **Solution:** Each term is the previous one multiplied by the next integer: 1×2 = 2, 2×3 = 6, 6×4 = 24, 24×5 = 120. The multipliers 2, 3, 4, 5 are consecutive, so the next multiplier is 6, giving 120 × 6 = 720. The terms are the factorials 1!, 2!, 3!, 4!, 5!, 6!.
> **Key point:** A multiplying series with consecutive multipliers is a factorial; find the next multiplier before multiplying.

### Q176. Find the next term: 0, 1, 4, 9, 16, 25, ?

> **Type:** Numerical
> **Answer:** 36.
> **Solution:** The terms are the perfect squares in order: 0², 1², 2², 3², 4², 5². The first differences 1, 3, 5, 7, 9 are the consecutive odd numbers that separate consecutive squares. The next square is 6² = 36. The series begins at 0 rather than 1, but that only shifts the indexing, not the rule.
> **Key point:** Identify square series by their odd-number first differences, not by where the series starts.

### Q177. Find the next term: 1, 8, 27, 64, 125, ?

> **Type:** Numerical
> **Answer:** 216.
> **Solution:** The terms are the perfect cubes 1³, 2³, 3³, 4³, 5³, so the next is 6³ = 6 × 6 × 6 = 216. The first differences 7, 19, 37, 61 confirm a cubic pattern, since the second differences 12, 18, 24 rise by 6 each time, the same signature that any cube series shows.
> **Key point:** In a cube series the gap between consecutive terms is 3n² + 3n + 1, and that gap itself grows by 6n + 6 at each step.

### Q178. Find the next term: 2, 5, 11, 23, 47, ?

> **Type:** Numerical
> **Answer:** 95.
> **Solution:** Each term is double the previous term plus 1: 2×2 + 1 = 5, 5×2 + 1 = 11, 11×2 + 1 = 23, 23×2 + 1 = 47. Applying the rule once more gives 47×2 + 1 = 95. The rule can also be written as aⁿ = 2ⁿ − 1, the Mersenne family, which is why every term here is one below a power of two: 3, 5, 11, 23, 47 are 2²−1, 2³−1, 2⁴−1, 2⁵−1, 2⁶−1.
> **Key point:** A "multiply by k, then add c" rule is found by dividing successive terms; here the ratio tends to 2 with a constant +1 remainder.

### Q179. Find the next term: 7, 10, 8, 11, 9, 12, ?

> **Type:** Numerical
> **Answer:** 10.
> **Solution:** The steps alternate: +3, −2, +3, −2, +3. Since the last given step is +3, the next step is −2, so the next term is 12 − 2 = 10. The two odd-indexed terms 7, 8, 9, 10 form their own +1 series and the even-indexed terms 10, 11, 12 form another, which is the same pattern seen from the other side.
> **Key point:** An alternating-difference series is two interleaved series; identify the repeat length of the step pattern.

### Q180. Find the next term: 1, 1, 2, 3, 5, 8, ?

> **Type:** Numerical
> **Answer:** 13.
> **Solution:** Each term is the sum of the two terms before it: 1 + 1 = 2, 1 + 2 = 3, 2 + 3 = 5, 3 + 5 = 8. The next term is therefore 5 + 8 = 13. This is the Fibonacci sequence, and the rule is the only one needed — no closed form is required to find a single term.
> **Key point:** In a Fibonacci-type series, the next term is always the sum of the previous two.

### Q181. Find the next term: 0, 7, 26, 63, 124, ?

> **Type:** Numerical
> **Answer:** 215.
> **Solution:** Each term is one less than a consecutive cube: 1³ − 1 = 0, 2³ − 1 = 7, 3³ − 1 = 26, 4³ − 1 = 63, 5³ − 1 = 124. The next term is 6³ − 1 = 216 − 1 = 215. The first differences 7, 19, 37, 61 confirm the cubic pattern, since the second differences 12, 18, 24 rise by 6 each time.
> **Key point:** When second differences rise by a constant, the terms are built from cubes; subtract 1 and check against the first terms.

### Q182. Find the next term: 360, 180, 120, 90, 72, ?

> **Type:** Numerical
> **Answer:** 60.
> **Solution:** Each term is 360 divided by the consecutive integers 1, 2, 3, 4, 5: 360/1 = 360, 360/2 = 180, 360/3 = 120, 360/4 = 90, 360/5 = 72. The next term is 360/6 = 60. Another way to see the rule is that the ratios between successive terms are 1/2, 2/3, 3/4, 4/5, so the next ratio is 5/6 and 72 × 5/6 = 60.
> **Key point:** A series of fractions of a constant is identified by the successive ratios, not by differences.

### Q183. Find the next term: 4, 9, 19, 39, 79, ?

> **Type:** Numerical
> **Answer:** 159.
> **Solution:** Examine the gaps between consecutive terms: 9 − 4 = 5, 19 − 9 = 10, 39 − 19 = 20, 79 − 39 = 40. The gaps themselves double each time — 5, 10, 20, 40 — so the next gap is 80, giving 79 + 80 = 159. Checking back, every gap is indeed twice the one before, which is what makes the rule certain rather than merely plausible. This is a second-difference structure in disguise, and it is why a candidate rule must be tested against every given term before it is accepted.
> **Key point:** When the gaps between terms form their own pattern, extend the gaps first and then add; here doubling gaps beat the superficially similar doubling rule.

### Q184. Find the next term: 2, 4, 8, 16, 32, ?

> **Type:** Numerical
> **Answer:** 64.
> **Solution:** Each term is twice the one before: 2×2 = 4, 4×2 = 8, 8×2 = 16, 16×2 = 32, so 32×2 = 64. This is a pure geometric series with common ratio 2, also 2¹, 2², 2³, 2⁴, 2⁵, 2⁶. The first differences 2, 4, 8, 16 are not constant, which rules out an arithmetic rule.
> **Key point:** Constant *ratios* (not constant differences) mark a geometric series.

### Q185. Find the next letter in the series: A, C, E, G, ?

> **Type:** Conceptual
> **Answer:** I.
> **Solution:** The letters are taken at every second position of the alphabet: A(1), C(3), E(5), G(7), so the next is I(9). The step is +2 alphabet positions, uniform throughout. Continuing the series would give K(11), M(13) and so on.
> **Key point:** A letter series with a uniform step in alphabet positions continues by the same step.

### Q186. Find the next letter in the series: Z, X, V, T, ?

> **Type:** Conceptual
> **Answer:** R.
> **Solution:** The letters run backwards through the alphabet at every second position: Z(26), X(24), V(22), T(20), a step of −2. The next is 20 − 2 = 18, which is R. After that would come P(16) and N(14).
> **Key point:** A descending letter series uses a negative step; converting to alphabet positions removes any guesswork.

### Q187. Find the next term in the alphanumeric series: A1, B2, C3, D4, ?

> **Type:** Conceptual
> **Answer:** E5.
> **Solution:** The letter advances one place in the alphabet while the number advances by 1 in step with it, so after D4 the pair is E5. The same pattern continues to Z26, at which point the 27th term has no letter left and the sequence would need a second letter per number.
> **Key point:** Pair a letter index with an equal number index; check what happens at the end of the alphabet.

### Q188. Find the next term in the series: AZ, BY, CX, ?

> **Type:** Numerical
> **Answer:** DW.
> **Solution:** The first letter moves one place forward (A, B, C, D) while the second moves one place backward (Z, Y, X, W). The next term is therefore DW. Check by alphabet position: A(1) with Z(26) sums to 27, B(2) with Y(25) sums to 27, C(3) with X(24) sums to 27, and D(4) with W(23) also sums to 27, which is the invariant the whole series obeys.
> **Key point:** Constant-sum or constant-difference pairings across a two-letter term reveal the rule immediately.

### Q189. Find the next term in the series: 3C, 5E, 7G, 9I, ?

> **Type:** Numerical
> **Answer:** 11K.
> **Solution:** The number rises by 2 each time (3, 5, 7, 9) and the letter rises by 2 each time (C, E, G, I). Continuing both together gives 11 and K, so the term is 11K. The two progressions stay in step throughout, and the number is always exactly one more than the letter's alphabetical position: C is 3 paired with 3, E is 5 paired with 5, I is 9 paired with 9. The pairing is preserved at the next step, since K is 11.
> **Key point:** In an alphanumeric series, track the number and letter progressions separately, then confirm they stay in step.

### Q190. A figure is built from 4 horizontal lines, 3 vertical lines, 6 circles and 2 squares. If 2 more horizontal lines and 1 more square are added, how many shapes will the figure then contain in total?

> **Type:** Numerical
> **Answer:** 18.
> **Solution:** The original figure contains 4 + 3 + 6 + 2 = 15 shapes. After the additions the horizontal lines become 6 and the squares become 3, so the new total is 6 + 3 + 6 + 3 = 18, an increase of 3 shapes. Circles and vertical lines are unchanged. Note that the count treats each drawn element as one shape, and no claim is made about the larger figures the lines may form between them.
> **Key point:** In figure-counting, restate the figure as a list of counts before and after the change, then add; count the elements named, not any shapes they might outline.

### Q191. `GATE-1`. A design contains 5 rectangles and 3 circles, and every rectangle has 4 straight sides. How many straight sides does the design contain in total?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) 20
> (b) 23
> (c) 27
> (d) 32
> ```
> **Answer:** (a) 20.
> **Solution:** Five rectangles contribute 5 × 4 = 20 straight sides, and three circles contribute no straight sides at all, because a circle is entirely curved. The total number of straight sides is therefore exactly 20. Option (b) 23 results from adding the 3 circles as if each had one side, and option (c) 27 from adding 3 × 4 = 12 for the circles as if they were squares.
> **Key point:** A circle has zero straight sides; in side-counting problems, treat curved figures as contributing nothing to the side total.

---

## Section 11. Statement–conclusion and statement–assumption

*Two related but distinct tests appear here. A **conclusion** is checked by asking whether it must be true given the statement. An **assumption** is checked by asking whether the statement could be acted upon without it — if the statement collapses when the assumption is false, the assumption is implicit.*

### Q192. Statement: All the trains that leave from platform 3 are express trains. Conclusion: All express trains leave from platform 3. Which follows?

> **Type:** Conceptual
> **Answer:** Neither the conclusion nor its negation follows; the conclusion is invalid.
> **Solution:** The statement places platform-3 departures inside the express class, that is E ⊆ P3. The conclusion asserts the reverse inclusion P3 ⊆ E, which is the classic error of illicit conversion of a universal affirmative. A counterexample satisfies the statement: an express train may depart from platform 7, leaving the conclusion false, and equally the conclusion could be true. Only the one-way inclusion is established.
> **Key point:** "All A are B" never licenses "All B are A"; the converse is a separate claim needing its own evidence.

### Q193. Statement: The road is wet. Conclusion: It has rained. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion does not follow.
> **Solution:** A wet road has many causes — rain, a sprinkler, a burst pipe, a cleaning vehicle, or dew. The statement is compatible with rain having fallen, but also with rain never occurring, so the conclusion is possible without being necessary. This is the standard gap between a *sufficient* and a *necessary* condition: rain is sufficient to wet the road but not necessary for it.
> **Key point:** A conclusion must be necessary, not merely possible; "the effect happened" never identifies the cause uniquely.

### Q194. Statement: This year's student admissions rose by 20 % over last year. Conclusion: This year's admissions were greater than last year's. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion follows.
> **Solution:** A rise of 20 % over a positive base means the new figure is 1.2 times the old one, which is necessarily larger. The conclusion is simply a restatement of the same fact in non-numerical form, and the two can never disagree. This is the pattern to look for: the conclusion adds no new information, so it must be true whenever the statement is.
> **Key point:** If the conclusion is a plain-language restatement of the statement, it necessarily follows.

### Q195. Statement: In each of the last five years the number of tourists visiting the museum exceeded the previous year's number. Conclusion: More tourists visited the museum in the fifth year than in the first. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion follows.
> **Solution:** The statement asserts a chain of five strict increases, so year 5 exceeds year 4 exceeds year 3 exceeds year 2 exceeds year 1. A chain of inequalities is transitive, so the fifth-year figure must exceed the first. Notice the statement gives *no* absolute numbers, so the size of the increase cannot be found — only the ordering.
> **Key point:** A chain of successive increases fixes the ordering of the endpoints, but never the magnitude of the gap.

### Q196. Statement: The average rainfall this season was below the normal for the area. Conclusion: The crop yield this year will be below normal. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion does not follow.
> **Solution:** Reduced rainfall may still be enough for the crops, and other factors — irrigation, fertiliser, crop choice, temperature — can keep yields at or above normal. Nothing in the statement links rainfall to yield, so the conclusion is possible but not necessary. A statement about an input does not by itself determine the output.
> **Key point:** A single stated cause does not license a conclusion about the final outcome; other variables intervene.

### Q197. Statement: In a circle, chord AB is longer than chord CD. Conclusion: The perpendicular from the centre meeting AB bisects it. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion follows.
> **Solution:** In a circle the line from the centre to a chord is perpendicular to that chord, and it bisects the chord — this is a standard circle theorem that holds for every chord regardless of its length, so the information about relative lengths is a distraction. Because AB is a chord of the circle, the conclusion must hold.
> **Key point:** A theorem that applies to every instance of a class makes the conclusion certain, whatever the extra information says.

### Q198. Statement: The temperature in Chennai is higher than the temperature in Delhi today. Conclusion: Chennai lies to the south of Delhi. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion does not follow.
> **Solution:** Chennai does lie to the south of Delhi in fact, but the statement gives a temperature comparison only, and nothing about latitude. On any given day, latitude is only one of several influences on temperature, so the geographic inference is not licensed by the statement. A conclusion must be derived from what is stated, not from what happens to be true.
> **Key point:** A conclusion that is factually true but not derivable from the statement is still invalid in this test.

### Q199. Statement: In the class, 30 students play cricket, 20 play football and 10 play both. Conclusion: Some students play neither game. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion does not follow.
> **Solution:** The numbers alone cannot show that the union is smaller than the class. If the class has 40 students, the union is 30 + 20 − 10 = 40 and the "neither" group is empty; if the class has 50, the union is still 40 and 10 students play neither. Since the class size is not given, the conclusion holds in one case and fails in the other, so it is not necessary.
> **Key point:** Without the size of the whole set, no "neither" conclusion can be drawn; state the missing datum explicitly.

### Q200. Statement: The company will shift its plant to a rural area because land there costs one third of the land in the city. Conclusion: Labour in the rural area will be available at lower cost. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion does not follow.
> **Solution:** The stated reason concerns land cost alone. The company may not have mentioned labour because it is *not* cheaper there, or because it plans to move existing staff, or because labour cost is simply not a deciding factor. A reason given in support of a conclusion need not be the only consideration, so the company is not obliged to believe the second claim.
> **Key point:** An argument does not disclose everything the speaker believes; it discloses only what is needed to support the stated conclusion.

### Q201. Statement: The library will be closed on Sundays so that the staff can rest. Assumption: Staff need adequate rest to work properly. Which assumption is implicit?

> **Type:** Conceptual
> **Answer:** Staff need adequate rest to work properly.
> **Solution:** The measure (closing on Sundays) and the stated purpose (staff rest) are connected only if rest actually benefits the staff and hence the work. Remove the assumption and the closure becomes a purposeless act, so it is genuinely implicit. Note that the assumption is not "the staff want a holiday", which would concern convenience rather than the reason given for the closure.
> **Key point:** An implicit assumption links the proposed step to the goal it is offered as achieving.

### Q202. Statement: The government should increase funding for sanitation in the city. Assumption: Current sanitation funding is inadequate. Which assumption is implicit?

> **Type:** Conceptual
> **Answer:** Current sanitation funding is inadequate.
> **Solution:** An increase is only warranted if the present level is insufficient; if funding were already ample, raising it would be unjustified and the recommendation would collapse. The argument therefore rests on the premise of inadequacy. The assumption concerns the *present* level, not whether more funding will be used efficiently, which is a separate question.
> **Key point:** A recommendation to increase something implies the current amount is insufficient for the goal.

### Q203. Statement: Children should be taught coding at an early age. Assumption: Learning coding early is beneficial. Which assumption is implicit?

> **Type:** Conceptual
> **Answer:** None is implicit — the stated assumption is the conclusion itself, not a premise.
> **Solution:** The claim is that coding should be taught early, and the proposed assumption is that early coding is good, which simply restates the recommendation. An implicit assumption must be *different* from the conclusion: it is the missing premise that connects the evidence to the claim. If the "assumption" is just the claim in other words, it should be rejected.
> **Key point:** A restatement of the conclusion is not an implicit assumption; look for the unstated bridge from evidence to claim.

### Q204. Statement: If we deposit 10 % of our income in a fixed deposit, it will grow at 9 % per annum. Assumption: Fixed deposit rates will remain at least 9 % in future years. Which assumption is implicit?

> **Type:** Conceptual
> **Answer:** Fixed deposit rates will remain at least 9 % in future years.
> **Solution:** The projected growth depends entirely on the rate being maintained. If banks cut the rate to 5 %, the final amount would be smaller than projected and the statement's promise would fail, so the assumption is genuinely implicit. A useful check is that the assumption must be about the future, since a deposit's yield is locked in only for the tenure chosen.
> **Key point:** A projection is always conditional on the conditions used to make it continuing to hold.

### Q205. Statement: The machine has been running for 12 hours without a break and is due for maintenance. Conclusion: The machine should be shut down now. Which follows?

> **Type:** Conceptual
> **Answer:** The conclusion follows.
> **Solution:** The statement supplies a factual gap — 12 hours of continuous running — and a pending obligation — maintenance that is due. The only sensible response to running an overdue machine longer is to stop it, and the conclusion is a direct practical consequence of the stated facts. No new factual premise is required to reach it.
> **Key point:** A conclusion that merely draws the obvious practical action from stated facts is a valid consequence.

### Q206. `GATE-1`. Statement: Every year since 2010 the number of bank branches has increased. Conclusion: The number of bank branches in 2024 is greater than in 2010. Which follows?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) The conclusion follows
> (b) The conclusion does not follow
> (c) The conclusion follows only if no branches closed in any year
> (d) The conclusion follows only if the increases were equal each year
> ```
> **Answer:** (a).
> **Solution:** The statement asserts a strict increase every year, so the 2024 figure must exceed every earlier one, including 2010. Option (c) adds a condition that is already covered: the branches count is a net figure, so a closure is already netted out and cannot break the chain. Option (d) is unnecessary, since only the direction of change matters, not its size. None of this says anything about *why* branches increased, and the conclusion makes no such claim.
> **Key point:** A strict monotonic statement guarantees the ordering of the endpoints; extra conditions about size or cause are irrelevant.

### Q207. `GATE-1`. Statement: Of the 400 students in a school, 250 take the bus and 150 walk to school. Conclusion: At least one student both takes the bus and walks. Which follows?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) The conclusion follows
> (b) The conclusion does not follow
> (c) The conclusion follows only if some students use other means
> (d) The conclusion follows only if more than 250 take the bus
> ```
> **Answer:** (b).
> **Solution:** The two counts add to exactly 400, the size of the whole school. If the two groups were disjoint they would already account for every student, so the overlap must be zero. The conclusion asserts the opposite of what the arithmetic forces: if a student took both, the total would fall below 400 and some student would be unaccounted for. The conclusion is therefore not merely unsupported but impossible on the stated data.
> **Key point:** If two counts sum exactly to the total, the two groups must be disjoint — the conclusion claiming an overlap is ruled out.

### Q208. `GATE-2`. Statements: Each of 50 students chose exactly one sport. 30 chose football and 25 chose cricket. Conclusion: At most 5 students chose both sports. Which follows?

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) The conclusion follows
> (b) The conclusion does not follow
> (c) The conclusion follows only if every student chose a sport other than these two
> (d) The conclusion follows only if the 50 students are all boys
> ```
> **Answer:** (a).
> **Solution:** The two sport counts total 30 + 25 = 55, which is 5 more than the 50 students in all. Every student counted in both the football group and the cricket group contributes one extra to that total, so the number counted twice is at most 55 − 50 = 5. Equivalently, in a two-set Venn diagram n(F ∪ C) ≤ n(F) + n(C) always, and the 50 chosen at least one sport form the whole, so n(F ∩ C) ≤ 5. Options (c) and (d) are irrelevant to the counting bound.
> **Key point:** When group counts exceed the total, the excess is an upper bound on the overlap; use n(A ∪ B) ≤ n(A) + n(B).

---

## Section 12. Logical connectives: negation, implication and truth tables

*Symbols used throughout: `~P` is NOT P, `P ∧ Q` is P AND Q, `P ∨ Q` is P OR Q (inclusive), `P → Q` is the material implication "if P then Q", and `P ↔ Q` is the biconditional. A compound statement is a **tautology** if it is true in every row of the truth table, a **contradiction** if it is false in every row, and a **contingency** otherwise.*

### Q209. Given P = True and Q = True, what is the truth value of ~(P ∧ Q)?

> **Type:** Conceptual
> **Answer:** False.
> **Solution:** With P and Q both true, P ∧ Q is true, and the negation of a true statement is false. Equivalently, ~(P ∧ Q) is the same statement as Pᶜ ∨ Qᶜ by De Morgan's law, which is false ∨ false = false here. This is the only row of the four-row truth table in which the conjunction is true, so it is the only row where its negation fails.
> **Key point:** ~(P ∧ Q) = Pᶜ ∨ Qᶜ; it is true in three of the four rows and false only when both P and Q are true.

### Q210. Given P = False and Q = False, what is the truth value of P ∨ Q?

> **Type:** Conceptual
> **Answer:** False.
> **Solution:** A disjunction is true if at least one of its parts is true. Here both parts are false, so there is nothing making the statement true and P ∨ Q is false. This is the single row in which the OR is false, which is why "P ∨ Q" is false *only* when both operands are false.
> **Key point:** P ∨ Q is false in exactly one case: P = F and Q = F.

### Q211. Given P = True and Q = False, what is the truth value of P → Q?

> **Type:** Conceptual
> **Answer:** False.
> **Solution:** The implication "if P then Q" fails exactly when the antecedent P is true and the consequent Q is false, because then the statement asserts something that has not happened. This is the only row in the four-row truth table in which an implication is false. The other three rows — (T,T), (F,T) and (F,F) — all give a true implication.
> **Key point:** P → Q is false in exactly one case: P = T and Q = F.

### Q212. `GATE-1`. Given P = False and Q = True, what is the truth value of P → Q?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) True
> (b) False
> (c) It depends on the context
> (d) Undefined
> ```
> **Answer:** (a) True.
> **Solution:** In everyday language a false antecedent might sound as though nothing is being asserted, but the material implication P → Q is defined as ~(P ∧ ~Q), and with P false the conjunction P ∧ ~Q is false, so the implication is true. The third row of the truth table is therefore true. In ordinary English, "if you are a fish then you can breathe" is considered vacuously true even of a person, and logic formalises exactly that.
> **Key point:** An implication with a false antecedent is always true; this is the single most misjudged row of the truth table.

### Q213. Given P = True and Q = False, what is the truth value of P ↔ Q?

> **Type:** Conceptual
> **Answer:** False.
> **Solution:** The biconditional P ↔ Q means (P → Q) ∧ (Q → P), that is, the two statements have the same truth value. Here they differ — P is true while Q is false — so at least one direction fails and the biconditional is false. A biconditional is true in the two rows where P and Q agree, (T,T) and (F,F), and false in the two rows where they disagree.
> **Key point:** P ↔ Q is true exactly when P and Q have the same truth value.

### Q214. Translate "At least one of P and Q is true" into logical notation.

> **Type:** Conceptual
> **Answer:** P ∨ Q.
> **Solution:** "At least one" includes the possibility of both, so the disjunction must be the inclusive OR, P ∨ Q, and not the exclusive OR. The inclusive reading is confirmed by the fact that P ∨ Q is true in three of the four rows, including (T,T), whereas an exclusive reading would be false there. The same sentence with "but not both" would instead require the exclusive disjunction.
> **Key point:** "At least one" = inclusive OR; "but not both" or "exactly one" = exclusive OR.

### Q215. Translate "Exactly one of P and Q is true" into logical notation.

> **Type:** Conceptual
> **Answer:** (P ∨ Q) ∧ ~(P ∧ Q).
> **Solution:** The statement has two requirements: at least one must be true, and they must not both be true. The first is P ∨ Q and the second is ~(P ∧ Q), so the compound is (P ∨ Q) ∧ ~(P ∧ Q). Testing it: (T,T) gives true ∧ false = false, (F,F) gives false ∧ true = false, and the two mixed rows both give true, which is exactly the behaviour required of "exactly one".
> **Key point:** "Exactly one" is inclusive OR combined with the negation of the conjunction.

### Q216. Translate "P only if Q" into logical notation.

> **Type:** Conceptual
> **Answer:** P → Q.
> **Solution:** "Only if" introduces a necessary condition: P can occur only in the circumstances where Q also occurs, so P requires Q. That is precisely the implication P → Q, and its contrapositive ~Q → ~P is equally valid. The wording is asymmetric: "P only if Q" never licenses Q → P, unlike the biconditional.
> **Key point:** "A only if B" = A → B; the arrow points from the sufficient to the necessary condition.

### Q217. Translate "Q if P" into logical notation.

> **Type:** Conceptual
> **Answer:** P → Q.
> **Solution:** "Q if P" means Q happens whenever P happens, with P as the condition and Q as the outcome, which is the implication P → Q. Note that this is the same formula as Q216, reached from the opposite word order: the "if" clause always becomes the antecedent. The reverse reading, Q → P, is not licensed by either sentence.
> **Key point:** In "B if A", A is the antecedent; the same statement can be written as ~B → ~A.

### Q218. Translate "Neither P nor Q is true" into logical notation.

> **Type:** Conceptual
> **Answer:** ~P ∧ ~Q.
> **Solution:** "Neither … nor …" asserts that both are false, so a conjunction of the two negations is required: ~P ∧ ~Q. A disjunction would be wrong, since P ∨ Q asserts that at least one holds, the exact opposite. By De Morgan's law this compound equals ~(P ∨ Q), which is another acceptable form.
> **Key point:** "Neither P nor Q" = ~P ∧ ~Q = ~(P ∨ Q).

### Q219. Translate "P, and not Q" into logical notation.

> **Type:** Conceptual
> **Answer:** P ∧ ~Q.
> **Solution:** The statement places two demands on the same situation: P must hold and Q must fail. Joining them with a conjunction and attaching the negation to Q gives P ∧ ~Q. It is false in three of the four rows and true only in the row (T, F), which is the row already identified as the failing case of the implication in Q211.
> **Key point:** Negation binds to the single proposition it is attached to; P ∧ ~Q is a conjunction of a positive and a negated term.

### Q220. Is the following equivalence true: (P ∨ Q)ᶜ ≡ Pᶜ ∧ Qᶜ?

> **Type:** Conceptual
> **Answer:** Yes, the equivalence holds.
> **Solution:** This is the first of De Morgan's laws. Checking row by row: with P = T, Q = T the left side is ~(T) = F and the right side is F ∧ F = F; with P = T, Q = F the left is ~(T) = F and the right is F ∧ T = F; with P = F, Q = T the left is ~(T) = F and the right is T ∧ F = F; with P = F, Q = F the left is ~(F) = T and the right is T ∧ T = T. The two sides agree in all four rows, so the equivalence is a tautological identity.
> **Key point:** De Morgan: (P ∨ Q)ᶜ = Pᶜ ∧ Qᶜ — the complement of a union is the intersection of the complements.

### Q221. Is the following equivalence true: ~(P ∧ Q) ≡ Pᶜ ∨ Qᶜ?

> **Type:** Conceptual
> **Answer:** Yes, the equivalence holds.
> **Solution:** This is the second of De Morgan's laws, and it is obtained from the first by substituting ~P and ~Q into (P ∨ Q)ᶜ = Pᶜ ∧ Qᶜ. Row check: (T,T) gives ~T = F on the left and F ∨ F = F on the right; (T,F) gives ~F = T and F ∨ T = T; (F,T) gives T and T; (F,F) gives T and T. All four rows agree. The two laws are the reason a negated conjunction becomes a disjunction and a negated disjunction becomes a conjunction.
> **Key point:** De Morgan: ~(P ∧ Q) = Pᶜ ∨ Qᶜ — a negated conjunction flips to OR and vice versa.

### Q222. Is the following equivalence true: (P ∧ Q) ∨ (P ∧ R) ≡ P ∧ (Q ∨ R)?

> **Type:** Conceptual
> **Answer:** Yes, this is the distributive law of conjunction over disjunction.
> **Solution:** Row check: with P = T, both sides reduce to Q ∨ R and agree whatever Q and R are. With P = F, the left side is F ∨ F = F and the right side is F ∧ (Q ∨ R) = F. The two sides match in all eight rows. The law says that requiring P once and (Q or R) separately is the same as accepting P together with either Q or R.
> **Key point:** P ∧ (Q ∨ R) = (P ∧ Q) ∨ (P ∧ R); the common factor distributes into both branches.

### Q223. Is the following equivalence true: P ∨ (Q ∧ R) ≡ (P ∨ Q) ∧ (P ∨ R)?

> **Type:** Conceptual
> **Answer:** Yes, this is the distributive law of disjunction over conjunction.
> **Solution:** Row check: with P = T, both sides are true. With P = F, the left side is Q ∧ R and the right side is (F ∨ Q) ∧ (F ∨ R) = Q ∧ R, so they agree. All eight rows match. It is the mirror image of Q222 — the same algebra with ∧ and ∨ interchanged — and both must be true because each connective distributes over the other in this dual form.
> **Key point:** P ∨ (Q ∧ R) = (P ∨ Q) ∧ (P ∨ R); the looser connective on the left pulls apart on the right.

### Q224. Is the following equivalence true: (P → Q) ≡ (Pᶜ ∨ Q)?

> **Type:** Conceptual
> **Answer:** Yes, the equivalence holds.
> **Solution:** Rewrite P → Q as ~(P ∧ ~Q) and apply De Morgan's law to get Pᶜ ∨ ~~Q, which is Pᶜ ∨ Q. Row check: (T,T) gives T and F ∨ T = T; (T,F) gives F and F ∨ F = F; (F,T) gives T and T ∨ T = T; (F,F) gives T and T ∨ F = T. All four rows agree, and the form Pᶜ ∨ Q is the standard way of turning any implication into a clause.
> **Key point:** P → Q is exactly Pᶜ ∨ Q; an implication is a disjunction with a negated antecedent.

### Q225. Is the following equivalence true: (P → Q) ≡ (~Q → ~P)?

> **Type:** Conceptual
> **Answer:** Yes, this is the contrapositive, which is logically equivalent to the original implication.
> **Solution:** Rewrite both sides: P → Q becomes Pᶜ ∨ Q, and ~Q → ~P becomes ~~Q ∨ ~P, which is Q ∨ ~P. Since ∨ is commutative, Pᶜ ∨ Q and Q ∨ Pᶜ are the same disjunction, so the two are identical. The contrapositive is a restatement of the original, whereas the converse Q → P is *not* equivalent and is a separate claim.
> **Key point:** An implication is equivalent to its contrapositive ~Q → ~P, but never to its converse Q → P.

### Q226. Is the statement P → (Q → P) a tautology, a contradiction, or a contingency?

> **Type:** Conceptual
> **Answer:** It is a tautology.
> **Solution:** Rewrite the nested implication from the inside out: Q → P is Qᶜ ∨ P, and P → (Qᶜ ∨ P) is Pᶜ ∨ Qᶜ ∨ P. Since Pᶜ ∨ P is already true, the whole expression is true in every row. Row check confirms it: (F,T) gives F → (T → F) = F → F = T; (F,F) gives F → (F → F) = F → T = T; (T,T) gives T → T = T; (T,F) gives T → (F → T) = T → T = T. All four rows are true.
> **Key point:** P → (Q → P) is a tautology; a nested implication collapses by the law Pᶜ ∨ Qᶜ ∨ P.

### Q227. Is the statement P ∧ ~P a tautology, a contradiction, or a contingency?

> **Type:** Conceptual
> **Answer:** It is a contradiction.
> **Solution:** P and ~P can never both be true, so the conjunction is false in all four rows of the truth table, whatever Q does. Row check: (F,F) gives F ∧ T = F; (F,T) gives F ∧ F = F; (T,F) gives T ∧ F = F; (T,T) gives T ∧ F = F. A contradiction is the dual of a tautology — a form such as this can never be made true, and it is the form used to state an outright contradiction in an argument.
> **Key point:** P ∧ ~P is a contradiction, false in every row; P ∨ ~P is a tautology, true in every row.

### Q228. `GATE-1`. Is the statement "P ∨ Q is false only when P is false and Q is false" true?

> **Type:** MCQ `GATE-1`
> Options:
> ```
> (a) True
> (b) False
> (c) True only if P and Q have different truth values
> (d) It cannot be determined without knowing P and Q
> ```
> **Answer:** (a) True.
> **Solution:** Work through the rows: (T,T) gives a true OR, (T,F) gives a true OR, (F,T) gives a true OR, and only (F,F) gives a false OR. The condition named in the statement matches the one and only failing row, so the biconditional P ∨ Q ↔ ~(~P ∧ ~Q) holds. Option (d) is the trap that the statement describes the disjunction in all cases, so no particular values of P and Q are needed.
> **Key point:** P ∨ Q fails in exactly one row; any statement identifying that row as the unique condition is true.

### Q229. Translate "No P is a Q" and "No P is not a Q" into set and logical notation, and state how they differ.

> **Type:** Conceptual
> **Answer:** "No P is a Q" means P ∩ Q = ∅, while "No P is not a Q" means P ⊆ Q.
> **Solution:** The first statement says every element of P fails to be a Q, that is Pᶜ contains Q, or equivalently P ∩ Q = ∅. The second says every element of P is a non-Q; since a non-Q is an element of Qᶜ, that is P ⊆ Qᶜ, which would be a strange reading. The intended sense of "No P is not a Q" is that nothing in P lies outside Q, giving P ⊆ Q. The two differ completely: the first is a disjointness, the second an inclusion, and inclusion is a far weaker condition.
> **Key point:** "No A is B" means A ∩ B = ∅; "No A is not a B" means A ⊆ B. A double negative is a containment, not a disjointness.

### Q230. `GATE-2`. Is the compound statement (P ∨ Q) ∧ (~P ∨ ~Q) equivalent to the biconditional P ↔ Q?

> **Type:** MCQ `GATE-2`
> Options:
> ```
> (a) Yes, the two are equivalent
> (b) No, the compound is always true
> (c) No, the compound is always false
> (d) No, the compound is equivalent to P ∨ Q
> ```
> **Answer:** (a).
> **Solution:** The clause ~P ∨ ~Q is the negation of P ∧ Q by De Morgan, so the compound reads "at least one of P, Q holds, but not both". Row check: (T,T) gives T ∧ F = F, (F,F) gives F ∧ T = F, and the two mixed rows both give T ∧ T = T. That is exactly the truth pattern of P ↔ Q, which is true when the two values agree. Option (b) is wrong because the compound is not true in the (T,T) row, and option (d) is wrong because the compound is false whenever P and Q agree, which P ∨ Q is not.
> **Key point:** (P ∨ Q) ∧ (~P ∨ ~Q) is the expanded form of P ↔ Q: they hold when the two values agree, and fail when they differ.

---

## Quick revision — Data Interpretation & Logical Reasoning

- Percentage change always divides by the **starting** value: 1450 → 1740 is +20 %, not +16.7 %.
- An overall percentage is total-part ÷ total-whole, never the unweighted mean of the row percentages.
- Percentage share = part ÷ sum of **all** rows × 100; the complement is a faster check.
- Biggest absolute rise and highest growth rate usually belong to different items — always say which is meant.
- Pie sector angle = (share ÷ 100) × 360; a fraction of a pie becomes degrees by multiplying by 360.
- In a histogram, bar **area** = frequency and bar **height** = frequency density; with unequal widths these disagree.
- Frequency density = frequency ÷ class width — this, not raw frequency, is what unequal-width histograms compare.
- Grouped median = l + [(N/2 − previous cf) ÷ f] × h; Q3 uses the position 3N/4 instead of N/2.
- The median class is the first whose cumulative frequency reaches N/2; the modal class is simply the largest frequency — they often differ.
- Inclusive classes need continuous boundaries at 14.5 / 20.5 style, but the class mark is unchanged by the ±0.5 shift.
- Bimodal = two local maxima separated by a trough; then there is no single mode.
- n(A ∪ B) = n(A) + n(B) − n(A ∩ B); the subtraction removes the double count exactly once.
- For three sets: add the singles, subtract the three pairs, add the triple back once.
- `A∩B only` = n(A ∩ B) − n(A ∩ B ∩ C); each pairwise intersection contains the triple region.
- A ⊆ B ⊆ C gives A ⊆ C, hence n(A) ≤ n(C); and n(A ∪ B) = n(B).
- Disjointness is **not** transitive: "No A is B" and "No B is C" say nothing about A versus C.
- Syllogism rule: a conclusion is valid only if it must be true in every situation the statements allow.
- *Barbara* A⊆B⊆C ⟹ A⊆C; *Celarent* A⊆B, B∩C=∅ ⟹ A∩C=∅; *Darii* Some A are B, B⊆C ⟹ Some A are C.
- "All A are B" is never convertible to "All B are A" — that invalid move is the commonest syllogism trap.
- Count parent–child links: 1 = parent, 2 = grandparent, 3 = great-grandparent; a spouse's blood relative is an in-law, and a **grandparent's** sibling is a *great*-uncle.
- "My grandfather's only son" is my **father**; "your mother's husband" is your **father**, not your uncle.
- If a question never states the person's gender, a sibling relationship has two answers and is undetermined.
- Right turn = clockwise (N→E→S→W); compass points sit at multiples of 45° from North, so 135° = South-East.
- Displacement is the straight-line start-to-finish distance; cancel opposing legs before applying Pythagoras.
- In any coding-decoding question, re-encode the **supplied example** first; a code that does not reproduce it is the wrong rule.
- (P ∨ Q) is false only when both are false; (P → Q) is false only when P = T and Q = F; so P → Q is true whenever P is false.
- De Morgan: (P ∨ Q)ᶜ = Pᶜ ∧ Qᶜ and ~(P ∧ Q) = Pᶜ ∨ Qᶜ — a negated connective flips to the other one.
- (P → Q) ≡ (Pᶜ ∨ Q) ≡ its contrapositive (~Q → ~P); the converse Q → P is **not** equivalent.
- P ↔ Q ≡ (P ∨ Q) ∧ (~P ∨ ~Q): true when the two values agree, false when they differ.
- Series: constant second differences signal a quadratic rule; constant ratios signal a geometric one; test any candidate rule against **every** given term.
- Statement–conclusion: a conclusion must be **necessary**, not merely possible, and must be derivable from the statement alone.
- Statement–assumption: reject any "assumption" that merely restates the conclusion; the real assumption is the unstated bridge.
