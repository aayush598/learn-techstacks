# General Aptitude — Part 5: Mixed Timed Drills & Previous-Year Pattern Sets

> Part 5 of 5 of the GATE ECE General Aptitude question bank · Questions 1–233 of this file
> This is the practice-and-speed file, and the only file in the bank that is *not* arranged
> as a syllabus. It is a set of themed, exam-realistic drill sets meant to be attacked under
> a stopwatch. It assumes the four teaching parts of this bank have already been worked
> through — **Part 1 — Numbers, Arithmetic and the Number System**, **Part 2 — Algebra,
> Equations and Functions**, **Part 3 — Geometry and Mensuration**, **Part 4 — Reasoning and
> Verbal Ability** — and it adds no new theory. Every drill below is fully self-contained:
> all data needed is inlined in the question, so any set can be attempted cold, out of
> order, or in a single timed sitting.

**Covers:** Twelve drill sets — arithmetic and estimation, algebra and equations, number
system and modular arithmetic, geometry under time pressure, data interpretation from
inlined tables and charts, reasoning (syllogisms, coding, blood relations, direction sense,
series), verbal ability (synonyms, antonyms, error spotting, inlined comprehension),
1-mark rapid-fire recall, 2-mark GATE-style mixed problems, a common-mistake trap set, a
section-wise previous-year pattern paper, and a final 25-question sweep — closing with a
blind-revision bullet list.

**Assumes:** Basic arithmetic (fractions, percentages, ratio, order of operations),
algebra of linear and quadratic equations, AP/GP, standard mensuration formulae,
syllogistic rules, and the ability to read an ASCII table. Nothing here needs calculus,
matrices, or any engineering content.

**Volume:** 233 questions across 12 sets, numbered Q1–Q233 with no gaps and no two
questions sharing a solution path. Weighted towards speed: roughly 15% recall, 35% quick
application, 25% medium, 15% GATE 1-mark MCQ (tagged `GATE-1`) and 10% GATE 2-mark
(tagged `GATE-2`).

---

## Section 1. Set A — Arithmetic and estimation drills

### Q1. Find the value of (3/7) of 448 + (5/8) of 512, working without a calculator.

> **Type:** Numerical
> **Answer:** 512
> **Solution:** (3/7) × 448 = 3 × 64 = 192, because 448 ÷ 7 = 64. Then (5/8) × 512 = 5 × 64 = 320, because 512 ÷ 8 = 64. The sum is 192 + 320 = 512. The drill is to cancel first: if the number divides cleanly by the denominator, divide the number before multiplying by the numerator.
> **Key point:** In (a/b) × c, cancel b out of c first — it is faster and it kills the large product.

### Q2. A shopkeeper raises the price of an article by 20% and then, in a later sale, cuts it by 20%. What is the net percentage change?

> **Type:** Numerical
> **Answer:** A net decrease of 4%
> **Solution:** Take the original price as 100. After the increase it is 120. After the decrease it is 120 × 0.80 = 96. The final value is 96, so the net change is −4%. The two percentages do not cancel because they are applied to *different* base amounts — the second 20% is taken off 120, not off 100.
> **Key point:** Successive percentage changes multiply: ×1.20 × 0.80 = 0.96, so the net is −4%, never 0%.

### Q3. What percentage of 40 is 12% of 75?

> **Type:** Numerical
> **Answer:** 22.5%
> **Solution:** 12% of 75 = 0.12 × 75 = 9. Now 9 as a percentage of 40 is (9/40) × 100 = 22.5%. Always collapse the inner percentage into a plain number first; the outer "what percent of" is then a single division.
> **Key point:** "A% of B is what percent of C" reduces to A × B / C percent.

### Q4. Three consignments in the ratio 5 : 7 : 10 must be packed into equal-weight bags. If the three consignments together weigh 4400 kg, what is the weight of the bag holding the 10-part consignment?

> **Type:** Numerical
> **Answer:** 2000 kg
> **Solution:** 5 + 7 + 10 = 22 equal parts carry 4400 kg, so one part = 4400 ÷ 22 = 200 kg. The three individual bag weights are 1000 kg, 1400 kg and 2000 kg, and the heaviest, asked for here, is 10 parts = 200 × 10 = 2000 kg.
> **Key point:** In any ratio question, convert to "weight of one part" first; the LCM of the ratio terms keeps it an integer.

### Q5. A train 180 m long runs at 72 km/h. How many seconds does it take to pass a pole?

> **Type:** Numerical
> **Answer:** 9 seconds
> **Solution:** Convert the speed: 72 km/h = 72 × 5/18 = 20 m/s. To pass a pole the train must cover exactly its own length, 180 m. Time = 180 ÷ 20 = 9 s. The conversion 1 km/h = 5/18 m/s is the single most useful arithmetic fact in speed questions.
> **Key point:** Passing a pole covers the train's own length only; multiply km/h by 5/18 to get m/s.

### Q6. A and B can together finish a job in 12 days, and A alone takes 20 days. How many days does B alone take?

> **Type:** Numerical
> **Answer:** 30 days
> **Solution:** Together they work at 1/12 of the job per day; A works at 1/20. So B works at 1/12 − 1/20 = (5 − 3)/60 = 2/60 = 1/30 of the job per day, and B alone takes 30 days. Check: 1/20 + 1/30 = 3/60 + 2/60 = 5/60 = 1/12.
> **Key point:** Work rates add as *fractions of the job per unit time*; subtract one rate to isolate the other.

### Q7. Pipe A fills a tank in 10 minutes, pipe B in 15 minutes and pipe C in 30 minutes. With all three open, how long does the tank take to fill?

> **Type:** Numerical
> **Answer:** 5 minutes
> **Solution:** In 30 minutes A delivers 3 units, B delivers 2 units and C delivers 1 unit — 6 units in total, where 6 units is one full tank. The combined rate is therefore 6/30 = 1/5 tank per minute, so the tank fills in 5 minutes. Choosing 30 as the common denominator (the LCM of the three times) is the standard first move.
> **Key point:** Rewrite every rate as "units per LCM-time" and add the numerators; the denominator is the answer.

### Q8. A boat travels downstream at 15 km/h and upstream at 9 km/h. It goes from A to B downstream in 3 hours. How far is A from B, and how long is the return trip?

> **Type:** Numerical
> **Answer:** A to B is 36 km; the return upstream takes 4 hours
> **Solution:** The boat's own speed is the mean of the two observed speeds, (15 + 9)/2 = 12 km/h, and the stream speed is (15 − 9)/2 = 3 km/h. Distance A to B = 12 × 3 = 36 km. The return is upstream at 9 km/h, so it takes 36 ÷ 9 = 4 hours.
> **Key point:** Boat speed = mean of the downstream and upstream speeds; stream speed = half their difference.

### Q9. Two trains, 300 m and 200 m long, move towards each other at 40 km/h and 20 km/h. How long until they completely cross?

> **Type:** Numerical
> **Answer:** 30 seconds
> **Solution:** In opposite directions the relative speed is the sum, 40 + 20 = 60 km/h = 60 × 5/18 = 16.667 m/s. To cross completely the trains must cover the sum of their lengths, 300 + 200 = 500 m. Time = 500 ÷ 16.667 = 30 s. In the same direction you would subtract the speeds but still add the lengths.
> **Key point:** Opposite directions: add speeds, add lengths. Same direction: subtract speeds, still add lengths.

### Q10. The mean of five numbers is 27. If the number 35 is replaced by another number, the mean falls by 2. What is the new number?

> **Type:** Numerical
> **Answer:** 25
> **Solution:** Original total = 5 × 27 = 135. The new mean is 25, so the new total is 5 × 25 = 125. Replacing 35 by x gives 135 − 35 + x = 125, hence x = 25. Since the size of the set is unchanged, the total must drop by 5 × 2 = 10, so the new entry is exactly 10 less than the old one.
> **Key point:** In a fixed-size set, replacing one item changes the total by (change in mean) × size — here −2 × 5 = −10.

### Q11. A shopkeeper marks an article 40% above cost price and then allows a 10% discount. If the cost price is ₹100, what is the profit percentage?

> **Type:** Numerical
> **Answer:** 26%
> **Solution:** Marked price = 100 + 40% of 100 = ₹140. Selling price after a 10% discount = 140 × 0.90 = ₹126. Profit = 126 − 100 = ₹26, which is 26% of the cost price. The tempting wrong answer is 30% (40 − 10) obtained by simple subtraction.
> **Key point:** Profit % = (mark-up factor × discount factor − 1) × 100; never subtract the two percentages.

### Q12. A dealer offers two successive discounts of 25% and then 10% on a marked price. What is the single equivalent discount percentage?

> **Type:** Numerical
> **Answer:** 32.5%
> **Solution:** On a marked price of 100 the first discount leaves 75, and the second leaves 75 × 0.90 = 67.5. The total reduction is 100 − 67.5 = 32.5%. The wrong answer 35% comes from adding the two discounts.
> **Key point:** Successive discounts a and b combine to a + b − ab/100; here 25 + 10 − 2.5 = 32.5.

### Q13. In a vessel the ratio of milk to water is 5 : 3. If 40 litres of milk is added, the ratio becomes 7 : 3. How much water was there originally?

> **Type:** Numerical
> **Answer:** 60 litres
> **Solution:** Let the original milk and water be 5k and 3k. After the milk is added the water is still 3k, and a ratio of 7 : 3 then means the milk is 7k. So 5k + 40 = 7k, giving 2k = 40 and k = 20. Water = 3k = 60 litres. Check: originally 100 L : 60 L = 5 : 3; after adding 40 L, 140 : 60 = 7 : 3.
> **Key point:** When the quantity that does *not* change is fixed, use it as the anchor for writing the second ratio.

### Q14. Two numbers are in the ratio 3 : 7. If 12 is added to each, the ratio becomes 1 : 2. What are the two numbers?

> **Type:** Numerical
> **Answer:** 36 and 84
> **Solution:** Let the numbers be 3k and 7k. A ratio of 1 : 2 means the first is half the second, so 2(3k + 12) = 7k + 12, giving 6k + 24 = 7k + 12 and hence k = 12. The numbers are 36 and 84. Check: 36 + 12 = 48 and 84 + 12 = 96, and 48 : 96 = 1 : 2.
> **Key point:** For "add the same number, ratio becomes 1 : 2" you need 2 × (first term) < second term; here 2 × 3 = 6 < 7.

### Q15. At simple interest a sum doubles itself in 12 years. In how many years will it become five times itself?

> **Type:** Numerical
> **Answer:** 48 years
> **Solution:** Doubling in 12 years means the interest earned in 12 years equals the principal P, so the interest rate is P/12 per year. Becoming five times means earning interest equal to 4P, which takes 4 × 12 = 48 years. Under simple interest the amount grows linearly, so every equal step in interest takes an equal step in time.
> **Key point:** Under simple interest, time is proportional to the interest earned — 2× in 12 years, so 4P of interest in 48 years.

### Q16. Express 0.2 with a bar over the digits 45 (that is, 0.245454545…) as a fraction in lowest terms.

> **Type:** Numerical
> **Answer:** 27/110
> **Solution:** For a mixed recurring decimal, subtract the number formed by the non-repeating digits from the number formed by the digits up to one full repeat: (245 − 2) / (10¹ × 99) = 243/990. Dividing numerator and denominator by 9 gives 27/110. Check: 27 ÷ 110 = 0.245454545….
> **Key point:** Mixed recurring decimals use (digits through one repeat − non-repeating part) / (10ⁿ × 99), n = number of non-repeating digits.

### Q17. A person spends 1/3 of his monthly income on rent, 1/4 on food and 1/5 on travel. If his income is ₹7,800, how much does he save in a month?

> **Type:** Numerical
> **Answer:** ₹1,690
> **Solution:** Total spent = 1/3 + 1/4 + 1/5 = 20/60 + 15/60 + 12/60 = 47/60. The saved fraction is 13/60, so the saving = 7800 × 13/60 = 130 × 13 = ₹1,690.
> **Key point:** Convert every fraction to 60ths (the LCM of 3, 4, 5) before adding; 7800 ÷ 60 = 130 makes the last step trivial.

### Q18. A car travels the first 40 km at 60 km/h and the next 40 km at 40 km/h. What is its average speed for the whole trip?

> **Type:** Numerical
> **Answer:** 48 km/h
> **Solution:** Time for the first half is 40/60 = 2/3 h; time for the second half is 40/40 = 1 h. The total distance of 80 km is covered in 1⅔ h, so the average speed = 80 ÷ (5/3) = 80 × 3/5 = 48 km/h. Simply averaging the two speeds (which gives 50 km/h) is wrong because the two halves do not take equal time.
> **Key point:** Never average speeds directly — total distance ÷ total time; the slow half is always over-weighted.

### Q19. Which of the following is closest to (1.01)¹⁰⁰?

(a) 1.10
(b) 2.00
(c) 2.70
(d) 3.00

> **Type:** MCQ (GATE-1)
> **Answer:** 2.70 (Option c)
> **Solution:** Use (1 + x/n)ⁿ → e^x with x = 1 and n = 100, so (1.01)¹⁰⁰ ≈ e¹ = 2.71828. The true value is 2.70481, and among the options 2.70 is by far the closest; 2.00 and 3.00 are 0.7 and 0.3 away while 1.10 is 1.6 away.
> **Key point:** (1 + 1/n)ⁿ → e ≈ 2.718; know this so a hundred-fold 1% increase roughly doubles rather than increases by 1%.

### Q20. If 15% of a number x is 27, what is 45% of x?

(a) 54
(b) 81
(c) 96
(d) 108

> **Type:** MCQ (GATE-1)
> **Answer:** 81 (Option b)
> **Solution:** 0.15x = 27, so x = 180. Then 45% of 180 is 0.45 × 180 = 81. The trap option 108 comes from multiplying 27 by 4 (as though 45% were 60% = 4 × 15%); 54 is 2 × 27, as though 45% were 30%.
> **Key point:** When both percentages refer to the same base x, scale by their ratio: 45/15 = 3, so 3 × 27 = 81.

### Q21. Give √2 + √3 to four decimal places.

> **Type:** Numerical
> **Answer:** ≈ 3.1463
> **Solution:** √2 = 1.41421356 and √3 = 1.73205081, so the sum is 3.14626437, which rounds to 3.1463. The value is above 3.14 = π, so the answer is slightly larger than π.
> **Key point:** Memorise √2 = 1.4142, √3 = 1.7321, √5 = 2.2361 — three values that answer a large share of GATE estimation options.

### Q22. The number 1.732 is a two-decimal approximation to √n. What is n?

(a) 2
(b) 3
(c) 4
(d) 5

> **Type:** MCQ (GATE-1)
> **Answer:** 3 (Option b)
> **Solution:** Square 1.732: 1.732² = 1.732 × 1.732 = 2.999824, which is 3 to within 0.0002 — a very good approximation. n = 2 would give 1.414, n = 4 would give exactly 2, and n = 5 would give 2.236, so only 3 matches.
> **Key point:** To identify the integer under a square root, square the given value: 1.732² ≈ 3, and its distinctively flat-looking value 1.414² ≈ 2.

---

## Section 2. Set B — Algebra and equation drills

### Q23. Solve for x: 3x − 7 = 2x + 11.

> **Type:** Numerical
> **Answer:** x = 18
> **Solution:** Subtract 2x from both sides: x − 7 = 11. Add 7: x = 18. Check: 3(18) − 7 = 54 − 7 = 47 and 2(18) + 11 = 36 + 11 = 47.
> **Key point:** Collect like terms on one side first, then isolate; always substitute the answer back into the original form.

### Q24. The roots of the quadratic x² − 9x + 14 = 0 are α and β. Find α² + β².

> **Type:** Numerical
> **Answer:** 53
> **Solution:** By the sum–product relations for a monic quadratic, α + β = 9 and αβ = 14. Then α² + β² = (α + β)² − 2αβ = 81 − 28 = 53. The roots are 7 and 2, and 49 + 4 = 53 confirms it.
> **Key point:** α² + β² = (α + β)² − 2αβ — never multiply out the roots unless you have to.

### Q25. The roots of x² − px + q = 0 differ by exactly 3. If p = 11, find q.

> **Type:** Numerical
> **Answer:** q = 28
> **Solution:** The square of the difference is (α − β)² = (α + β)² − 4αβ. Here (α + β)² = 121, and αβ = q, so 9 = 121 − 4q, giving 4q = 112 and q = 28. Check: x² − 11x + 28 = (x − 4)(x − 7), whose roots differ by exactly 3.
> **Key point:** (α − β)² = (α + β)² − 4αβ is the formula to reach for whenever the *difference* of roots is given.

### Q26. If x > 2 and x < 5, which interval contains −3x?

> **Type:** Comparison
> **Answer:** −15 < −3x < −6
> **Solution:** Multiplying an inequality by a negative number reverses it. From x < 5 we get −3x > −15, and from x > 2 we get −3x < −6. Combining: −15 < −3x < −6. For example x = 3 gives −9, which does lie in that interval.
> **Key point:** Multiplying an inequality by a negative flips both the inequality signs and the order of the bounds.

### Q27. How many integral values of x satisfy 2x − 9 ≤ 5 < 3x + 4?

> **Type:** Numerical
> **Answer:** 7
> **Solution:** Solve the first part: 2x ≤ 14, so x ≤ 7. The second: 5 < 3x + 4, so 1 < 3x and x > 1/3. For integral x the range is 1 ≤ x ≤ 7, which is the seven values 1, 2, 3, 4, 5, 6, 7.
> **Key point:** A chained "≤ … <" statement is two independent inequalities; solve each and intersect the ranges.

### Q28. If the sum of the first n terms of an arithmetic progression is Sₙ = 3n² + 5n, what is its common difference?

> **Type:** Numerical
> **Answer:** 6
> **Solution:** The first term is a₁ = S₁ = 3 + 5 = 8. The second term is a₂ = S₂ − S₁ = (3·4 + 5·2) − 8 = 22 − 8 = 14. The common difference is a₂ − a₁ = 14 − 8 = 6. (As a check, Sₙ − Sₙ₋₁ = 6n + 2 is itself an AP with difference 6.)
> **Key point:** From a closed form for Sₙ, get a = S₁ and a₂ = S₂ − S₁, then d = a₂ − a₁.

### Q29. In a geometric progression the ratio of the third term to the fifth term is 1 : 9. What is the common ratio?

> **Type:** Numerical
> **Answer:** 3
> **Solution:** With first term a and ratio r, t₃ = ar² and t₅ = ar⁴, so t₃/t₅ = 1/r². Setting 1/r² = 1/9 gives r² = 9, so r = 3 (the positive root). A ratio of terms two places apart is simply r².
> **Key point:** In a GP, tₙ/tₙ₋ₖ = rᵏ; two places apart means r², three places apart means r³.

### Q30. If 5ˣ = 125, what is the value of 25ˣ?

> **Type:** Numerical
> **Answer:** 15625
> **Solution:** 5ˣ = 125 = 5³, so x = 3. Then 25ˣ = (5²)³ = 5⁶ = 15625. Working through 25 = 5² is what makes the answer a power of 5 rather than a large multiplication.
> **Key point:** Convert the second base to a power of the first base, match exponents, and read off a power table.

### Q31. Simplify √50 + √18 − √8.

> **Type:** Numerical
> **Answer:** 6√2 ≈ 8.485
> **Solution:** Pull out the largest square from each: √50 = √(25·2) = 5√2, √18 = √(9·2) = 3√2, √8 = √(4·2) = 2√2. Adding gives (5 + 3 − 2)√2 = 6√2, and 6 × 1.41421356 = 8.485.
> **Key point:** Every surd here shares the factor 2; collect the coefficients and leave one surd.

### Q32. Between which two consecutive integers does √20 lie?

> **Type:** Numerical
> **Answer:** Between 4 and 5
> **Solution:** √20 = √(4·5) = 2√5 ≈ 2 × 2.2361 = 4.4721, which is greater than 4 and less than 5. A square-root-free check: 4² = 16 < 20 < 25 = 5².
> **Key point:** Locate a surd between integers by squaring the bounds — 16 < 20 < 25 needs no decimal work at all.

### Q33. Evaluate (4^(1/2))³ + 27^(2/3).

> **Type:** Numerical
> **Answer:** 17
> **Solution:** 4^(1/2) = 2, so 2³ = 8. And 27^(2/3) = (∛27)² = 3² = 9. The sum is 8 + 9 = 17. A fractional index means "take the root first, then raise to the power" — the reverse order gives 8^(3/2), a different number.
> **Key point:** For a^(p/q), take the q-th root first and then raise to the p-th power; the order is not interchangeable.

### Q34. If x + 1/x = 3, find the value of x² + 1/x².

> **Type:** Numerical
> **Answer:** 7
> **Solution:** Square both sides: (x + 1/x)² = x² + 2 + 1/x² = 9. Therefore x² + 1/x² = 9 − 2 = 7. The cross term 2 comes from x · (1/x) = 1 counted twice.
> **Key point:** (x ± 1/x)² = x² + 1/x² ± 2; the middle term is always 2, so subtract or add 2 and you are done.

### Q35. What is the minimum value of x + 8/x for x > 0?

(a) 4
(b) 4√2
(c) 8
(d) 16

> **Type:** MCQ (GATE-1)
> **Answer:** 4√2 (Option b)
> **Solution:** The minimum of x + k/x for x > 0 occurs at x = √k and equals 2√k. With k = 8 this is 2√8 = 2 × 2√2 = 4√2 ≈ 5.657. Direct check: at x = 2√2 the two terms are both 2√2, so the sum is 4√2, the least possible by the arithmetic–geometric mean inequality √(x · 8/x) = √8 = 2√2 giving a sum of at least 2 × 2√2.
> **Key point:** x + k/x is minimised at x = √k with value 2√k, by AM–GM; it has no maximum.

### Q36. For what value of k does the equation x² + kx + 9 = 0 have two equal real roots?

(a) 3
(b) 6
(c) 6 or −6
(d) 4 or −4

> **Type:** MCQ (GATE-1)
> **Answer:** 6 or −6 (Option c)
> **Solution:** Equal roots require the discriminant to vanish: k² − 4·1·9 = 0, so k² = 36 and k = ±6. Both signs are acceptable because the x-term has no linear asymmetry; the roots are −3 and 3 in both cases, just swapped. Option (a) is the trap: 3 gives x² + 3x + 9 = 0 with discriminant 9 − 36 < 0, i.e. no real roots at all.
> **Key point:** Equal roots ⇔ discriminant = 0; for x² + kx + c = 0 that is k = ±2√c.

### Q37. Solve the simultaneous equations 2x + 3y = 12 and 3x + 2y = 13.

> **Type:** Numerical
> **Answer:** x = 3, y = 2
> **Solution:** Multiply the first equation by 2 and the second by 3: 4x + 6y = 24 and 9x + 6y = 39. Subtracting eliminates y and gives 5x = 15, so x = 3. Substituting into 2(3) + 3y = 12 gives 3y = 6, so y = 2. Check the second equation: 9 + 4 = 13.
> **Key point:** When the two equations have coefficients that swap (2,3) and (3,2), doubling one and trebling the other cancels the same unknown cleanly.

### Q38. The equation x² + (k + 1)x + 1 = 0 has one root equal to 1. Find k and the other root.

> **Type:** Numerical
> **Answer:** k = −3, and the other root is also 1
> **Solution:** The product of the roots is 1, so if one root is 1 the other is 1/1 = 1 as well — the equation has a double root at 1. The sum of the roots is −(k + 1) = 1 + 1 = 2, so k + 1 = −2 and k = −3. Check: x² − 2x + 1 = (x − 1)².
> **Key point:** With constant term 1 in a monic quadratic, a root of 1 forces the other root to be 1 too.

### Q39. Three distinct numbers are in both an arithmetic progression and a geometric progression in the same order. What can you say about them?

> **Type:** Theory
> **Answer:** No three distinct positive numbers can satisfy both conditions simultaneously; the only common case is three equal numbers (common ratio 1, common difference 0).
> **Solution:** Let the numbers be a, a + d, a + 2d. Being in GP as well requires (a + d)² = a(a + 2d) — the middle-term-squared condition. Expanding: a² + 2ad + d² = a² + 2ad, so d² = 0 and d = 0. Hence all three numbers are equal.
> **Key point:** In a three-term GP the middle term squared equals the product of the ends; combining that with an AP forces the common difference to be zero.

### Q40. Find the value of 1³ + 2³ + 3³ + … + 10³.

> **Type:** Numerical
> **Answer:** 3025
> **Solution:** The standard identity is that the sum of the first n cubes equals the square of the sum of the first n natural numbers. Here 1 + 2 + … + 10 = 10 × 11/2 = 55, so the sum of cubes is 55² = 3025.
> **Key point:** Σk³ = (n(n + 1)/2)² — always square the triangular number, and check the result has the right magnitude.

### Q41. What is the solution set of |2x − 5| < 3?

(a) x < 4 only
(b) 1 < x < 4
(c) 1 < x < 8
(d) x < 1 or x > 4

> **Type:** MCQ (GATE-1)
> **Answer:** 1 < x < 4 (Option b)
> **Solution:** −3 < 2x − 5 < 3. Adding 5 throughout: 2 < 2x < 8. Dividing by 2: 1 < x < 4. Note the strictness is preserved because the original inequality is strict; option (d) is the set for |2x − 5| > 3, not < 3.
> **Key point:** |y| < a is the double inequality −a < y < a; |y| > a is the union of the two outside intervals.

### Q42. How many real roots does the equation x³ − 3x + 1 = 0 have?

(a) 0
(b) 1
(c) 2
(d) 3

> **Type:** MCQ (GATE-2)
> **Answer:** 3 (Option d)
> **Solution:** Look for sign changes of f(x) = x³ − 3x + 1. At x = −2, f = −8 + 6 + 1 = −1; at x = −1, f = −1 + 3 + 1 = 3, so a root lies in (−2, −1). At x = 0, f = 1; at x = 1, f = 1 − 3 + 1 = −1, so a root lies in (0, 1). At x = 2, f = 8 − 6 + 1 = 3, so a third root lies in (1, 2). Three disjoint sign changes give three distinct real roots, which is the maximum a cubic can have.
> **Key point:** Count sign changes of the function over disjoint intervals; that alone certifies the number of real roots of any polynomial.

---

## Section 3. Set C — Number system and modular drills

### Q43. What is the units digit of 7²³?

> **Type:** Numerical
> **Answer:** 3
> **Solution:** The units digits of powers of 7 run 7, 9, 3, 1 and then repeat with period 4. Since 23 = 4 × 5 + 3, the answer is the third entry of the cycle, which is 3.
> **Key point:** Powers of 7 have a units-digit cycle of length 4: 7, 9, 3, 1 — take the exponent mod 4.

### Q44. What is the units digit of 3²⁰⁰⁶?

> **Type:** Numerical
> **Answer:** 9
> **Solution:** Powers of 3 have units digits 3, 9, 7, 1, repeating with period 4. 2006 = 4 × 501 + 2, so the units digit is the second entry, 9.
> **Key point:** The four cyclic units-digit sets worth memorising are 2,3,8 → 2,4,8,6; 3,7 → 3,9,7,1; 4,9 → 4,6; and the ending digits 0,1,5,6 which never change.

### Q45. What is the remainder when 7²⁰²⁵ is divided by 5?

> **Type:** Numerical
> **Answer:** 2
> **Solution:** Reduce the base first: 7 ≡ 2 (mod 5). The powers of 2 modulo 5 cycle 2, 4, 3, 1 with period 4. 2025 = 4 × 506 + 1, so the remainder is the first entry, 2.
> **Key point:** Reduce the base modulo m before touching the exponent — the cycle of the small number is far easier to hold in the head.

### Q46. What is the remainder when 2¹⁰ + 3¹⁰ is divided by 5?

> **Type:** Numerical
> **Answer:** 3
> **Solution:** Modulo 5, 2¹⁰ cycles with period 4 and 10 mod 4 = 2, giving 2² = 4. For 3¹⁰, 10 mod 4 = 2, giving 3² = 9 ≡ 4 (mod 5). The sum is 4 + 4 = 8 ≡ 3 (mod 5).
> **Key point:** Reduce each term separately and add the residues; never form the huge numbers.

### Q47. Find the greatest number that divides 1155, 1575 and 1995 exactly.

> **Type:** Numerical
> **Answer:** 105
> **Solution:** This is the HCF. 1575 − 1155 = 420. Then 1155 = 2 × 420 + 315; 420 = 315 + 105; and 315 = 3 × 105, so HCF(1155, 1575) = 105. Now 1995 = 19 × 105, so 105 also divides the third number and remains the HCF. Check: 1155/105 = 11, 1575/105 = 15, 1995/105 = 19 — all integers.
> **Key point:** Repeated subtraction (or the Euclidean algorithm) gives the HCF; if the numbers factor as 105 × 11, 105 × 15, 105 × 19, the answer is obvious by inspection.

### Q48. What is the smallest number which, when divided by 12, 15 and 18, leaves the same remainder 3 in each case?

> **Type:** Numerical
> **Answer:** 183
> **Solution:** If N leaves remainder 3 on division by each of 12, 15 and 18, then N − 3 is divisible by all three, so N − 3 is a common multiple. The least common multiple is LCM(12, 15, 18) = 2² × 3² × 5 = 180. Hence N = 180 + 3 = 183. Check: 183 ÷ 12 = 15 r 3, 183 ÷ 15 = 12 r 3, 183 ÷ 18 = 10 r 3.
> **Key point:** "Same remainder r on division by each" ⇒ answer = LCM + r, provided r is smaller than the smallest divisor.

### Q49. How many integers from 1 to 1000 are divisible by neither 2 nor 3?

> **Type:** Numerical
> **Answer:** 333
> **Solution:** Count the complement by inclusion–exclusion. Multiples of 2: ⌊1000/2⌋ = 500. Multiples of 3: ⌊1000/3⌋ = 333. Multiples of both (i.e. of 6): ⌊1000/6⌋ = 166. So divisible by 2 or 3 there are 500 + 333 − 166 = 667, and the rest number 1000 − 667 = 333.
> **Key point:** "Neither A nor B" is easiest as total − |A ∪ B|, with |A ∪ B| = |A| + |B| − |A ∩ B|.

### Q50. Two bells ring every 42 seconds and every 63 seconds. If they are rung together at 9:00 a.m., when do they next ring together?

> **Type:** Numerical
> **Answer:** 9:02:06 a.m.
> **Solution:** LCM(42, 63) = 2 × 3² × 7 = 126 seconds. So the bells coincide after 126 s = 2 min 6 s, at 9:02:06 a.m.
> **Key point:** Coincidence interval = LCM of the periods; decompose the LCM into prime powers to get it quickly.

### Q51. What is the remainder when 7²⁰²⁴ is divided by 13?

> **Type:** Numerical
> **Answer:** 3
> **Solution:** 13 is prime, so by Fermat's theorem 7¹² ≡ 1 (mod 13). Reduce the exponent: 2024 = 12 × 168 + 8, so 7²⁰²⁴ ≡ 7⁸ (mod 13). Now 7² = 49 ≡ 10, 7⁴ ≡ 10² = 100 ≡ 9, and 7⁸ ≡ 9² = 81 ≡ 81 − 78 = 3 (mod 13).
> **Key point:** For a prime modulus p, cut the exponent to its value mod (p − 1) — Fermat's little theorem.

### Q52. What is the units digit of 3²⁰²⁴ + 7²⁰²⁴?

> **Type:** Numerical
> **Answer:** 2
> **Solution:** For 3, 2024 mod 4 = 0, so the units digit is the fourth entry of 3, 9, 7, 1, which is 1. For 7, 2024 mod 4 = 0, so the units digit is the fourth entry of 7, 9, 3, 1, which is also 1. The sum ends in 1 + 1 = 2.
> **Key point:** When the exponent is a multiple of 4, a base in the cyclic set has units digit 1 — no cycle tracing needed.

### Q53. How many zeros are there at the end of 100! (100 factorial)?

> **Type:** Numerical
> **Answer:** 24
> **Solution:** Each trailing zero comes from a factor of 10 = 2 × 5, and 2s are abundant, so count only 5s. In 100! the multiples of 5 contribute ⌊100/5⌋ = 20, the multiples of 25 contribute ⌊100/25⌋ = 4 more, and 125 is too large. Total = 20 + 4 = 24.
> **Key point:** Trailing zeros = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + …; the deeper floors must not be omitted.

### Q54. How many three-digit numbers have all three digits distinct?

> **Type:** Numerical
> **Answer:** 648
> **Solution:** The hundreds digit has 9 choices (1 to 9). The tens digit has 9 choices (0 to 9 except the hundreds digit). The units digit then has 8 choices. The product is 9 × 9 × 8 = 648.
> **Key point:** For distinct-digit counts, the leading digit loses the 0 option while later digits do not: 9 × 9 × 8 for three digits, 9 × 9 × 8 × 7 for four.

### Q55. Which of the following numbers divides 4444 exactly?

(a) 3
(b) 4
(c) 6
(d) 9

> **Type:** MCQ (GATE-1)
> **Answer:** 4 (Option b)
> **Solution:** 4444 ÷ 4 = 1111, an integer, so 4 divides it — the last two digits 44 are divisible by 4. The digit sum is 4 + 4 + 4 + 4 = 16, which is not a multiple of 3 or of 9, so 3 and 9 fail, and since 4444 is even but not divisible by 3 it also fails divisibility by 6. Option (a) is the classic trap: 4444 *looks* like a multiple of 4 (many 4s) but its digit sum rules out 3.
> **Key point:** Check the digit sum for 3 and 9, the last two digits for 4 and 11, and the last three digits for 8, 7, 13 — never count digits as evidence.

### Q56. The number 19 is written in binary as a four-bit string. What is it?

(a) 10011
(b) 10101
(c) 11001
(d) 10010

> **Type:** MCQ (GATE-1)
> **Answer:** 10011 (Option a)
> **Solution:** The place values of a four-bit binary number are 8, 4, 2, 1. 19 = 16 + 2 + 1, and 16 + 2 + 1 needs five bits (10011). Equivalently, halving repeatedly: 19 → 9 r1, 9 → 4 r1, 4 → 2 r0, 2 → 1 r0, 1 → 0 r1, giving the remainders 1,1,0,0,1 read upwards.
> **Key point:** Binary place values are powers of 2; writing n in base 2 is just expressing it as a sum of distinct powers of 2.

### Q57. How many integers strictly between 100 and 200 are divisible by 7?

> **Type:** Numerical
> **Answer:** 14
> **Solution:** The first multiple of 7 above 100 is 105 and the last below 200 is 196, since 7 × 14 = 98 and 7 × 29 = 203. The count is an arithmetic run: (196 − 105)/7 + 1 = 91/7 + 1 = 13 + 1 = 14. Equivalently, ⌊199/7⌋ − ⌊100/7⌋ = 28 − 14 = 14.
> **Key point:** Counting multiples of k in (a, b) is ⌊b/k⌋ − ⌊a/k⌋ — quicker than listing them.

### Q58. What are the last two digits of 3²⁰²⁴?

> **Type:** Numerical
> **Answer:** 81
> **Solution:** Work modulo 100. 3¹⁰ ≡ 43 (mod 100) and 3²⁰ ≡ 43² = 1849 ≡ 49 (mod 100); also 3²⁰⁰ ≡ 1 (mod 100) and 3²⁰²⁰ ≡ 1. Since 2024 = 2000 + 24 and 3²⁰⁰⁰ ≡ 1, we need 3²⁴. With 3²⁰ ≡ 1 we get 3²⁴ = 3²⁰ · 3⁴ ≡ 1 × 81 = 81 (mod 100).
> **Key point:** Last two digits means working modulo 100, where the cycle of 3 has period 20; 2024 mod 20 = 4 gives 3⁴ = 81.

### Q59. What is the largest three-digit number exactly divisible by 17?

> **Type:** Numerical
> **Answer:** 986
> **Solution:** Divide 999 by 17: 17 × 58 = 986 and 17 × 59 = 1003, so the largest multiple of 17 not exceeding 999 is 986. Equivalently, 17 × 58 = (17 × 60) − 34 = 1020 − 34 = 986.
> **Key point:** The largest n-digit multiple of k is k × ⌊(10ⁿ − 1)/k⌋; find the quotient by estimation and check one less.

### Q60. What is the smallest number that must be added to 2468 to make it a perfect square?

> **Type:** Numerical
> **Answer:** 32
> **Solution:** The squares bracketing 2468 are 49² = 2401 and 50² = 2500. Since 2468 lies between them, the nearest perfect square above is 2500, and 2500 − 2468 = 32.
> **Key point:** Take the square root, then round up: 50² − 2468 = 32, with no other working needed.

### Q61. How many prime numbers lie between 1 and 30?

> **Type:** Numerical
> **Answer:** 10
> **Solution:** The primes below 30 are 2, 3, 5, 7, 11, 13, 17, 19, 23 and 29, which is 10 of them. Note that 1 is not prime and 9, 15, 21, 25 and 27 are divisible by 3 while 4, 8, 10, 14, 16, 20, 22, 26 and 28 are excluded by 2.
> **Key point:** Memorise the primes up to 30 (2, 3, 5, 7, 11, 13, 17, 19, 23, 29) and know that 1 is neither prime nor composite.

### Q62. How many perfect squares divide 6! = 720 exactly? (Count 1 as a perfect square.)

> **Type:** Numerical
> **Answer:** 6
> **Solution:** Prime-factorise: 720 = 2⁴ × 3² × 5. A perfect-square divisor must have an even exponent of every prime, so the exponent of 2 can be 0, 2 or 4 (three choices), the exponent of 3 can be 0 or 2 (two choices), and the exponent of 5 must be 0 (one choice). The number of such divisors is 3 × 2 × 1 = 6, namely 1, 4, 9, 16, 36, 144. The tempting wrong approach is to list every square n² ≤ 720, of which there are 26, but many of them (49, 25, 100 and so on) do not divide 720.
> **Key point:** Count square divisors of N = ∏ pᵉ as ∏ (⌊e/2⌋ + 1) over its distinct primes; never enumerate squares up to N.

---

## Section 4. Set D — Geometry speed drills

### Q63. A rectangle has perimeter 36 cm and its length is twice its breadth. What is its area in cm²?

(a) 96
(b) 108
(c) 120
(d) 72

> **Type:** MCQ (GATE-1)
> **Answer:** 72 (Option d)
> **Solution:** Put breadth b and length 2b. Then 2(L + B) = 36, so L + B = 18, giving 3b = 18 and b = 6, L = 12. The area is 12 × 6 = 72 cm². The trap options come from squaring the semi-perimeter (18² = 324, halved wrongly) or from forgetting the factor 2 in the perimeter formula.
> **Key point:** With perimeter P, L + B = P/2; for a fixed perimeter the area is largest when L = B.

### Q64. A circular wire is bent to form a circle whose circumference is 44 cm (take π = 22/7). What is the area of the circle in cm²?

> **Type:** Numerical
> **Answer:** 154 cm²
> **Solution:** From C = 2πr = 44 we get r = 44/(2 × 22/7) = 44 × 7/44 = 7 cm. Then A = πr² = (22/7) × 49 = 22 × 7 = 154 cm².
> **Key point:** When π = 22/7 is given, always expect r to be a multiple of 7 — extract r from the circumference before computing the area.

### Q65. A cuboid measures 12 cm × 8 cm × 5 cm. What is its total surface area in cm²?

> **Type:** Numerical
> **Answer:** 392 cm²
> **Solution:** TSA = 2(lw + lh + wh) = 2(12×8 + 12×5 + 8×5) = 2(96 + 60 + 40) = 2 × 196 = 392 cm². Each of the three distinct face areas must be found once and then doubled, because every face has an opposite twin.
> **Key point:** TSA of a cuboid is twice the sum of the three pairwise products; volume is the product of all three.

### Q66. A cylinder and a cone have the same base radius and the same height. What is the ratio of the volume of the cone to the volume of the cylinder?

> **Type:** Numerical
> **Answer:** 1 : 3
> **Solution:** Cylinder volume = πr²h; cone volume = (1/3)πr²h. The base area and height are identical, so the ratio is exactly (1/3)πr²h : πr²h = 1 : 3. No numbers are needed.
> **Key point:** A cone is exactly one-third of the cylinder on the same base and height; conversely a cone's volume triples into the equivalent cylinder.

### Q67. A sphere has radius 7 cm. Taking π = 22/7, what is its volume in cm³?

> **Type:** Numerical
> **Answer:** 4312/3 ≈ 1437.33 cm³
> **Solution:** V = (4/3)πr³ = (4/3) × (22/7) × 343 = (4/3) × 22 × 49 = 4312/3 ≈ 1437.33 cm³. The neat cancellation is 343/7 = 49, which is why a radius that is a multiple of 7 is always chosen.
> **Key point:** Sphere volume = (4/3)πr³ — a sphere has twice the surface area but only twice-thirds the volume of its own cube of side 2r.

### Q68. Two similar triangles have areas 49 cm² and 121 cm². What is the ratio of their corresponding sides?

> **Type:** Numerical
> **Answer:** 7 : 11
> **Solution:** For similar figures the ratio of corresponding lengths is the square root of the ratio of areas. √49 : √121 = 7 : 11. It follows that their perimeters are also in the ratio 7 : 11.
> **Key point:** Similar figures: length ratio = √(area ratio), so area ratios are always squares — a non-square area ratio signals an error.

### Q69. A triangle is enlarged so that its area becomes exactly four times the original. By what factor does each side change?

> **Type:** Numerical
> **Answer:** 2
> **Solution:** Doubling every side multiplies the area by 2² = 4, by the square law for similar figures. So the linear scale factor is √4 = 2. Note the converse trap: doubling the area alone would only give a factor of √2 ≈ 1.414 on each side.
> **Key point:** Area scales as the square of the length scale factor; perimeter scales as the length itself.

### Q70. The angles of a triangle are in the ratio 2 : 3 : 4. What is the largest angle in degrees?

(a) 60°
(b) 72°
(c) 80°
(d) 90°

> **Type:** MCQ (GATE-1)
> **Answer:** 80° (Option c)
> **Solution:** The three parts sum to 9, and the angles of a triangle sum to 180°, so one part = 20°. The angles are 40°, 60° and 80°, and the largest is 80°. Option (a) is the trap: 180/3 = 60 assumes the ratios are equal.
> **Key point:** For angles in ratio a : b : c, each part is 180/(a + b + c) degrees.

### Q71. Two parallel lines are cut by a transversal. One of the angles formed is 65°. What are the measures of its co-interior (allied) angle and its alternate angle?

> **Type:** Numerical
> **Answer:** Co-interior angle 115°; alternate angle 65°
> **Solution:** Co-interior (same-side interior) angles between parallel lines are supplementary, so the allied angle is 180° − 65° = 115°. Alternate angles are equal, so the alternate angle is 65° itself. Corresponding angles are likewise equal to 65°, while vertically opposite angles equal 65° and the co-exterior angle is 115°.
> **Key point:** Parallel-line families: equal pairs are alternate, corresponding, vertically opposite and alternate-exterior; supplementary pairs are co-interior and co-exterior.

### Q72. An exterior angle of a triangle is 120°, and one of the two interior angles opposite to it is 45°. What is the other interior angle opposite to the exterior angle?

> **Type:** Numerical
> **Answer:** 75°
> **Solution:** The exterior angle of a triangle equals the sum of the two interior angles opposite to it, so 120° = 45° + x, giving x = 75°. Check: the third angle is 180° − 45° − 75° = 60°, and the exterior angle 180° − 60° = 120° agrees.
> **Key point:** Exterior angle = sum of the two remote interior angles; the interior angle adjacent to it is supplementary to it.

### Q73. The angles of a quadrilateral are x, x + 10°, x + 20° and x + 50°. Find the value of x in degrees.

> **Type:** Numerical
> **Answer:** 70°
> **Solution:** The interior angles of any quadrilateral sum to 360°. So 4x + 80° = 360°, giving 4x = 280° and x = 70°. The angles are 70°, 80°, 90° and 120°, which sum to 360°.
> **Key point:** Interior-angle sums: triangle 180°, quadrilateral 360°, pentagon 540°, hexagon 720° — that is (n − 2) × 180°.

### Q74. A chord of a circle subtends an angle of 40° at the centre. What angle does it subtend at any point on the major arc?

> **Type:** Numerical
> **Answer:** 20°
> **Solution:** The angle at the centre is twice the angle subtended by the same chord at the circumference in the same segment, so the angle at the circumference on the major arc is 40°/2 = 20°. On the *minor* arc the angle would instead be (360° − 40°)/2 = 160°, since the two inscribed angles are supplementary.
> **Key point:** Inscribed angle = half the central angle on the same arc; angles on opposite arcs sum to 180°.

### Q75. From an external point P, two tangents PA and PB are drawn to a circle touching it at A and B. If angle APB = 60°, what is the central angle AOB subtended by the same chord?

> **Type:** Numerical
> **Answer:** 120°
> **Solution:** A tangent is perpendicular to the radius at the point of contact, so the angle at A is 90° and the angle at B is 90°. In quadrilateral OAPB the angles sum to 360°, giving angle AOB = 360° − 90° − 90° − 60° = 120°. This matches the general result that the angle between two tangents equals 180° minus the angle subtended by the chord at the centre.
> **Key point:** Angle between two tangents from an external point = 180° − (central angle subtended by the chord of contact).

### Q76. A cube has edge 6 cm. What is the length of its space diagonal, in cm?

> **Type:** Numerical
> **Answer:** 6√3 ≈ 10.39 cm
> **Solution:** The space diagonal of a cube of edge a is a√3, obtained by applying Pythagoras twice: the base diagonal is a√2 and the vertical rise is a, so the total is √(2a² + a²) = a√3. With a = 6: 6 × 1.7320508 = 10.39 cm.
> **Key point:** Cube: face diagonal a√2, space diagonal a√3; a cuboid's space diagonal is √(l² + b² + h²).

### Q77. A trapezium has parallel sides 14 cm and 8 cm and a perpendicular height of 6 cm. What is its area in cm²?

> **Type:** Numerical
> **Answer:** 66 cm²
> **Solution:** A = (1/2) × (sum of parallel sides) × height = (1/2) × (14 + 8) × 6 = (1/2) × 22 × 6 = 66 cm². The trap is to add the bases and multiply by the height without the factor 1/2, which would give 132.
> **Key point:** Trapezium area = ½(a + b)h; it is exactly half of the parallelogram with the same base sum and height.

### Q78. A circular ring is formed by two concentric circles of outer radius 9 cm and inner radius 5 cm. Taking π = 22/7, what is the area of the ring in cm²?

> **Type:** Numerical
> **Answer:** 176 cm²
> **Solution:** Area of the ring = π(R² − r²) = (22/7) × (81 − 25) = (22/7) × 56 = 22 × 8 = 176 cm². Computing the two areas separately and subtracting is slower and invites the classic πR² − πr² = π(R − r)² error.
> **Key point:** Annulus area = π(R² − r²) = π(R − r)(R + r), never π(R − r)².

### Q79. A right-angled triangle has perpendicular sides 6 cm and 8 cm. What are its hypotenuse and its inradius?

> **Type:** Numerical
> **Answer:** Hypotenuse 10 cm; inradius 2 cm
> **Solution:** The hypotenuse is √(36 + 64) = √100 = 10 cm, a 3-4-5 scaled by 2. For a right triangle the inradius is (a + b − c)/2, so r = (6 + 8 − 10)/2 = 4/2 = 2 cm. (Equivalently, r = area/semi-perimeter = 24/12 = 2.)
> **Key point:** Inradius of a right triangle = (a + b − c)/2 = area / semi-perimeter — the same fact in two disguises.

### Q80. A square of side 12 cm has a square of side 4 cm cut out of one corner. What is the perimeter of the remaining figure in cm?

> **Type:** Numerical
> **Answer:** 48 cm
> **Solution:** The original perimeter is 4 × 12 = 48 cm. Cutting a square notch from a corner removes 4 cm of one edge but exposes 4 cm of new edge, and the corner is removed from a second edge similarly, so the two lengths exactly cancel and the perimeter is unchanged at 48 cm. This is true for any corner notch; the area, by contrast, drops by 4² = 16 cm².
> **Key point:** Cutting a square or rectangular notch out of a *corner* leaves the perimeter unchanged; cutting from the middle of one side adds twice the notch depth.

### Q81. A map is drawn to a scale of 1 : 50,000. Two towns 8 cm apart on the map are how far apart on the ground?

> **Type:** Numerical
> **Answer:** 4 km
> **Solution:** Scale 1 : 50,000 means 1 cm on the map is 50,000 cm on the ground = 500 m. So 8 cm represents 8 × 500 = 4000 m = 4 km. The trap is to convert to metres and stop at 400,000 cm, or to forget that 100,000 cm = 1 km.
> **Key point:** Scale 1 : n converts cm to metres by n/100, then metres to kilometres by another /1000; here 50,000 cm = 500 m.

### Q82. A cone has base radius 7 cm and height 24 cm. Find its slant height and its curved surface area, taking π = 22/7.

> **Type:** Numerical
> **Answer:** Slant height 25 cm; curved surface area 550 cm²
> **Solution:** The slant height is √(r² + h²) = √(49 + 576) = √625 = 25 cm — a 7-24-25 triple. The curved surface area is πrl = (22/7) × 7 × 25 = 22 × 25 = 550 cm². The total surface area would add the base, πr² = 154, giving 704 cm².
> **Key point:** Cone: l = √(r² + h²), CSA = πrl, TSA = πr(l + r); look for a Pythagorean triple in the given r and h.

---

## Section 5. Set E — Data interpretation drill set

The following table shows the number of books issued from a public library on six days. Use it for Q83 to Q86.

```
Day        Mon   Tue   Wed   Thu   Fri   Sat
Books      120   150    90   200   180   240
```

### Q83. What is the total number of books issued over the six days?

> **Type:** Numerical
> **Answer:** 980 books
> **Solution:** Add the six columns: 120 + 150 = 270, + 90 = 360, + 200 = 560, + 180 = 740, + 240 = 980. A useful check is to pair symmetric entries: (120 + 240) = 360 and (150 + 180) = 330, which give 690, plus the middle pair 90 + 200 = 290, totalling 980.
> **Key point:** In a DI table, total several columns by pairing opposite ends — it is faster and it is a free check.

### Q84. What is the mean number of books issued per day over the six days?

> **Type:** Numerical
> **Answer:** ≈ 163.33 books per day
> **Solution:** The total is 980 over 6 days, so the mean is 980/6 = 163.33 (exactly 490/3). The mean need not be a whole number. The sorted values are 90, 120, 150, 180, 200, 240, whose median is (150 + 180)/2 = 165, while the mean is 163.33 — the 90 drags the mean below the median.
> **Key point:** Mean = total / count; an unusually small value drags the mean down, so it need not equal the median.

### Q85. On which day was the highest number of books issued, and what percentage of the six-day total was that day's figure?

> **Type:** Numerical
> **Answer:** Saturday, with 24.49% of the total
> **Solution:** The largest entry is 240 on Saturday. Its share of the 980 total is 240/980 × 100 = 24.4898… ≈ 24.49%. Simplify first: 240/980 = 24/98 = 12/49, and 12/49 × 100 = 24.49%.
> **Key point:** "What percentage of the total" is always (part / total) × 100; reduce the fraction before multiplying by 100.

### Q86. If books were also issued on Sunday, and Sunday's figure equalled Monday's figure of 120, what would be the mean issue over the full seven days?

> **Type:** Numerical
> **Answer:** 157.14 books per day
> **Solution:** The seven-day total becomes 980 + 120 = 1100, spread over 7 days, so the mean is 1100/7 = 157.14 (exactly 157 1/7). Adding a value below the old mean of 163.33 pulls the new mean down, as it must.
> **Key point:** A new mean lies between the old mean and the new value added; use that as a sanity check.

The following table gives the marks scored by five students in three subjects, each out of 100. Use it for Q87 to Q90.

```
Student   Math   Physics   Chemistry
  A        72       65         58
  B        65       78         70
  C        80       70         82
  D        58       84         66
  E        90       72         75
```

### Q87. Which subject has the highest total marks across the five students?

> **Type:** Numerical
> **Answer:** Physics, with 369 marks
> **Solution:** Mathematics totals 72 + 65 + 80 + 58 + 90 = 365. Physics totals 65 + 78 + 70 + 84 + 72 = 369. Chemistry totals 58 + 70 + 82 + 66 + 75 = 351. Physics is the largest at 369, with Chemistry the smallest at 351.
> **Key point:** Column sums settle "which subject" questions instantly; always sum all columns so the ranking is honest.

### Q88. What is the mean mark in Mathematics?

> **Type:** Numerical
> **Answer:** 73 marks
> **Solution:** The Mathematics total is 365 across 5 students, so the mean is 365/5 = 73. The division comes out exact here, which is a good sign that the table was built consistently.
> **Key point:** Row totals give per-student performance; column totals give per-subject performance — read the question to know which you need.

### Q89. How many students scored above 75 in at least one subject?

> **Type:** Numerical
> **Answer:** 4 students
> **Solution:** Student A's best is 72, so A does not qualify. B scores 78 in Physics, C scores 80 and 82, D scores 84 in Physics, and E scores 90 in Mathematics — so B, C, D and E all qualify, giving 4 students. "At least one subject" means count each student once, however many subjects they cleared.
> **Key point:** "At least one" questions are counted per person, not per cell — go row by row and tally.

### Q90. Which student has the highest total across the three subjects, and what is that total?

> **Type:** Numerical
> **Answer:** Student E, with 237 marks
> **Solution:** Row totals: A = 72 + 65 + 58 = 195; B = 65 + 78 + 70 = 213; C = 80 + 70 + 82 = 232; D = 58 + 84 + 66 = 208; E = 90 + 72 + 75 = 237. The largest is E's 237. Note that D has the best Physics mark of all yet the second-lowest total, which is exactly the trap in a row-total question.
> **Key point:** "Best in one column" and "best overall" are different questions — D is best in Physics but E wins on the row total.

The following table shows monthly unit sales of two products. Use it for Q91 to Q93.

```
Month      Jan   Feb   Mar   Apr   May   Jun
Product A  200   250   180   300   260   350
Product B  150   180   220   240   300   320
```

### Q91. In which months did Product B outsell Product A?

> **Type:** Numerical
> **Answer:** March and May
> **Solution:** Compare the two rows month by month: Jan 200 vs 150 (A ahead), Feb 250 vs 180 (A ahead), Mar 180 vs 220 (B ahead), Apr 300 vs 240 (A ahead), May 260 vs 300 (B ahead), Jun 350 vs 320 (A ahead). So B exceeds A in March (220 > 180) and in May (300 > 260).
> **Key point:** "Which columns does one row beat another in?" needs a full column-by-column scan, not a comparison of row totals.

### Q92. What is the total number of units of Product A sold over the six months?

> **Type:** Numerical
> **Answer:** 1540 units
> **Solution:** 200 + 250 + 180 + 300 + 260 + 350. Pairing: (200 + 350) = 550, (250 + 300) = 550, (180 + 260) = 440, giving 550 + 550 + 440 = 1540 units.
> **Key point:** Pairing the first and last columns first is the fastest reliable way to sum a six-column row.

### Q93. In which month was the combined sale of both products the highest, and what was it?

> **Type:** Numerical
> **Answer:** June, with 670 units
> **Solution:** Combined monthly figures: Jan 350, Feb 430, Mar 400, Apr 540, May 560, Jun 670. The largest is June at 350 + 320 = 670 units. March is a trap because it is the month where the *gap* between the products is largest, not the total.
> **Key point:** To compare combined totals you must actually add the columns; do not eyeball the largest single entries.

A company's revenue for one financial year is divided as shown in the pie chart below, and the total revenue is Rs. 400,000. Use it for Q94 to Q96.

```
Division        Product A   Services   Exports   Other
Share of total      45%        30%        15%      10%
```

### Q94. What is the revenue from Services?

> **Type:** Numerical
> **Answer:** Rs. 120,000
> **Solution:** Services is 30% of Rs. 400,000, so the revenue is 0.30 × 400,000 = Rs. 120,000. A quick route: 10% is 40,000, so 30% is three such slices, 3 × 40,000 = 120,000.
> **Key point:** Convert a pie chart into rupees by finding one percentage point's value and then multiplying; 10% is almost always a clean slice.

### Q95. By how much does the revenue from Product A exceed that from Services?

> **Type:** Numerical
> **Answer:** Rs. 60,000
> **Solution:** Product A is 45%, which is 0.45 × 400,000 = Rs. 180,000. Services is Rs. 120,000 from Q94. The excess is 180,000 − 120,000 = Rs. 60,000. In percentage-point terms the gap is 45% − 30% = 15 points, and 15% of 400,000 is also 60,000.
> **Key point:** Differences between pie slices can be taken in percentage points first and converted once, which saves a multiplication.

### Q96. Next year the total revenue grows by 20% while every division keeps the same share. What will the Exports revenue be?

> **Type:** Numerical
> **Answer:** Rs. 72,000
> **Solution:** This year's Exports revenue is 15% of 400,000 = Rs. 60,000. A 20% rise in the total with unchanged shares means every division's revenue rises by 20%: 60,000 × 1.20 = Rs. 72,000. Equivalently, the new total is 480,000 and 15% of that is 72,000.
> **Key point:** If pie-chart shares are unchanged, every slice scales by exactly the growth factor of the total.

The following table shows how a company's total production cost is split in two years. The total production cost was Rs. 200,000 in 2019 and Rs. 260,000 in 2024. Use it for Q97 to Q99.

```
Cost head     2019 share   2024 share
Raw material      40%         45%
Labour            25%         20%
Power             15%         22%
Others            20%         13%
```

### Q97. Which cost head increased the most in absolute rupees between 2019 and 2024, and by how much?

> **Type:** Numerical
> **Answer:** Raw material, by Rs. 37,000
> **Solution:** Compute the rupee figures. In 2019: raw material 40% of 200,000 = 80,000; labour 25% = 50,000; power 15% = 30,000; others 20% = 40,000. In 2024: raw material 45% of 260,000 = 117,000; labour 20% = 52,000; power 22% = 57,200; others 13% = 33,800. The changes are: raw material +37,000, labour +2,000, power +27,200, others −6,200. Raw material rises the most, by Rs. 37,000 — even though power gained more percentage points (+7 against +5), because the base is larger.
> **Key point:** "Largest increase" is ambiguous — check whether the question means rupees or percentage points, because they can give different winners.

### Q98. In 2024, what fraction of the total production cost was spent on labour and power together, in rupees?

> **Type:** Numerical
> **Answer:** Rs. 109,200, which is 42% of the cost
> **Solution:** Labour is 20% and power 22%, together 42% of Rs. 260,000. So 0.42 × 260,000 = Rs. 109,200. In pieces this is 52,000 + 57,200 = 109,200, which agrees.
> **Key point:** Add the shares first, then convert once; never convert each share separately and add.

### Q99. In 2024 the power cost falls to 15% of the same total of Rs. 260,000, and all the money released is transferred to raw material. What would the new raw material cost be?

> **Type:** Numerical
> **Answer:** Rs. 135,200
> **Solution:** Power currently costs 22% of 260,000 = Rs. 57,200. At 15% it would cost 0.15 × 260,000 = Rs. 39,000, releasing 57,200 − 39,000 = Rs. 18,200. Raw material was Rs. 117,000, so it becomes 117,000 + 18,200 = Rs. 135,200. As a check, the new shares are raw material 135,200/260,000 = 52%, power 15%, and labour and others unchanged at 20% and 13%, summing to 100%.
> **Key point:** A transfer between two slices keeps the total fixed, so the gain of one equals the loss of the other — recheck that the new shares sum to 100%.

### Q100. The average mark of five students in a test is 68, so the total is 340. Four of them scored 62, 74, 58 and 81. What did the fifth student score?

> **Type:** Numerical
> **Answer:** 65 marks
> **Solution:** Work from the total rather than from the average. The five marks sum to 5 × 68 = 340. The four known marks sum to 62 + 74 + 58 + 81 = 275. The fifth mark is 340 − 275 = 65. The mean of the four known marks is 68.75, so 65 is a plausible fifth value and no entry is inconsistent.
> **Key point:** In a "missing value" DI question, multiply to get the total first, then subtract the known sum.

### Q101. Four candidates in an election received 25%, 30% and 35% of the first three shares of the 80,000 votes cast, with the fourth taking the remainder. How many votes did the fourth candidate get?

> **Type:** Numerical
> **Answer:** 8,000 votes
> **Solution:** The first three shares total 25% + 30% + 35% = 90%, so the fourth candidate has the remaining 10%. Ten per cent of 80,000 = 8,000 votes. The other three got 20,000, 24,000 and 28,000, and 20,000 + 24,000 + 28,000 + 8,000 = 80,000, confirming the total.
> **Key point:** A "remainder" slice in a pie chart is 100% minus the sum of the stated shares — and if one share is missing, the total must reconcile to the vote count.

### Q102. A help desk logged the following number of calls each day:

```
Day          1    2    3    4    5    6
Calls       120  180  240  300  360  420
```

What is the ratio of the total calls on days 1 to 3 to the total on days 4 to 6?

> **Type:** Numerical
> **Answer:** 1 : 2
> **Solution:** Days 1 to 3 total 120 + 180 + 240 = 540. Days 4 to 6 total 300 + 360 + 420 = 1080. The ratio is 540 : 1080, which reduces to 1 : 2. Equivalently, the second block's three days are each exactly 60 calls more than the corresponding first-block days, so the second total is exactly double.
> **Key point:** Always reduce a ratio to coprime integers before reporting it; 540 : 1080 is not an acceptable final answer.

---

## Section 6. Set F — Reasoning drill set

### Q103. Statements: All pens are tools. Some tools are blue. Which conclusions follow? I — Some pens are blue. II — Some tools are blue.

(a) Only I
(b) Only II
(c) Both I and II
(d) Neither I nor II

> **Type:** MCQ (GATE-1)
> **Answer:** Only II (Option b)
> **Solution:** Conclusion II restates the second statement directly, so it certainly follows. Conclusion I does not: the blue tools could all be non-pens, for example blue hammers, with no blue pen in existence. "All pens are tools" only guarantees that pens lie inside the tool set, not that they occupy the blue part of it.
> **Key point:** A particular conclusion ("some A are B") is supported only if the two sets are forced to overlap; "all A are B" plus "some B are C" never yields "some A are C".

### Q104. Statements: Some apples are fruits. All fruits are healthy foods. Which conclusions follow? I — Some apples are healthy. II — All healthy things are apples.

(a) Only I
(b) Only II
(c) Both I and II
(d) Neither I nor II

> **Type:** MCQ (GATE-1)
> **Answer:** Only I (Option a)
> **Solution:** The apples mentioned in statement 1 are fruits, and every fruit is a healthy food, so those particular apples are healthy — I follows. II reverses a universal statement: "all fruits are healthy" does not say that everything healthy is a fruit, since vegetables and nuts are healthy but not fruits.
> **Key point:** A chain "some A are B, all B are C" always licenses "some A are C"; a universal "all B are C" never licenses "all C are B".

### Q105. In a certain code, the word GATE is written as HBUF, so that each letter is replaced by the next letter of the alphabet. How is EXAM written in that code?

> **Type:** Numerical
> **Answer:** FYBN
> **Solution:** The rule is a shift of +1: G→H, A→B, T→U, E→F, which reproduces HBUF. Applying the same rule to EXAM gives E→F, X→Y, A→B, M→N, so the code is FYBN.
> **Key point:** Before decoding, verify your rule against every letter of the one example you are given.

### Q106. In a certain code, each vowel is replaced by the next vowel and each consonant by the next consonant. How is DOG coded?

(a) EPH
(b) EOH
(c) FPH
(d) EPU

> **Type:** MCQ (GATE-1)
> **Answer:** EPH (Option a)
> **Solution:** D is a consonant and the next consonant is E. O is a vowel and the next vowel is P (cyclic, so A follows U). G is a consonant and the next consonant is H. So DOG becomes EPH. Option (c) is the trap of moving the second letter on as if it were a consonant.
> **Key point:** In "next vowel, next consonant" codes the vowel cycle is closed (A → E → I → O → U → A); a vowel never codes to a consonant.

### Q107. In a certain code, CAT is written as TAC and DOG is written as GOD. How is LIGHT written in that code?

> **Type:** Numerical
> **Answer:** THGIL
> **Solution:** Both examples simply reverse the order of the letters, so the rule is reversal. Reversing LIGHT (L-I-G-H-T) gives T-H-G-I-L, i.e. THGIL.
> **Key point:** Test reversal rules on a three-letter word first: it is the fastest way to confirm a positional rule before committing.

### Q108. Pointing to a photograph, Meera said, "He is the son of the only daughter of the father of my brother." How is the person in the photograph related to Meera?

(a) Brother
(b) Nephew
(c) Son
(d) Cousin

> **Type:** MCQ (GATE-1)
> **Answer:** Nephew (Option b)
> **Solution:** Work from the inside out. The father of Meera's brother is Meera's own father. The only daughter of Meera's father is Meera's sister (assuming Meera is a daughter too, the phrase is ambiguous, but the standard reading is the sister). The son of that daughter is Meera's sister's son, which is her nephew.
> **Key point:** Solve blood-relation chains from the innermost phrase outward, one relationship at a time.

### Q109. A is the brother of B. B is the sister of C. C is the son of D. How is D related to A?

(a) Brother
(b) Uncle
(c) Father
(d) Son

> **Type:** MCQ (GATE-1)
> **Answer:** Father (Option c)
> **Solution:** B and C are siblings, so they share both parents, and C is a son of D, making D a parent. Since A is a brother of B, A is also a child of D. As A is male (stated as "brother") and D is the parent referred to, D is A's father.
> **Key point:** Siblings share parents, so any parent of one is a parent of all — that single rule resolves most of these chains.

### Q110. P is the mother of Q. Q is the sister of R. R is the father of S. How is P related to S?

(a) Mother
(b) Aunt
(c) Grandmother
(d) Sister

> **Type:** MCQ (GATE-1)
> **Answer:** Mother (Option a)
> **Solution:** Q and R are siblings and R is a child of P, so P is also a parent of R. R is the father of S, so S is R's child; P, being R's parent, is therefore S's mother. Note that Q is P's child too, so S is Q's child as well — P is the mother of both Q and S, which is why "aunt" is the trap.
> **Key point:** Grandmother arises only after two full parent steps; here the path P → R → S is one step to S from P, i.e. mother.

### Q111. Ravi walks 3 km towards the north, then 4 km towards the east, then 3 km towards the south. How far is he from the starting point, and in which direction?

> **Type:** Numerical
> **Answer:** 4 km to the east
> **Solution:** Taking east as +x and north as +y, the walk gives a net displacement of (+4, 0): the northward 3 km and the southward 3 km cancel exactly, leaving 4 km east. The distance actually walked is 3 + 4 + 3 = 10 km, which is the trap — the question asks for the displacement from the start.
> **Key point:** Always distinguish distance walked from displacement; south and north legs of equal size cancel.

### Q112. A man starts facing north. He turns 90° clockwise, then 180°, and then 90° anticlockwise. Which direction is he finally facing?

(a) South
(b) East
(c) West
(d) North

> **Type:** MCQ (GATE-1)
> **Answer:** South (Option a)
> **Solution:** Starting north, a 90° clockwise turn faces him east. A 180° turn then faces him west. A 90° anticlockwise turn from west faces him south. Clockwise turns are subtracted when measuring anticlockwise, or: 90 − 180 − 90 = −180°, i.e. a half turn from north, which is south.
> **Key point:** Convert every turn to one signed number — clockwise positive, anticlockwise negative — and add from north.

### Q113. The bearing of a point P from a station O is N 37° E. What is the back bearing of P from P, i.e. the bearing of O from P?

> **Type:** Numerical
> **Answer:** S 37° W
> **Solution:** A back bearing is obtained by reversing both letters of the quadrant: N becomes S and E becomes W, with the angle unchanged. So N 37° E becomes S 37° W. As a check, if P is at 37° east of north from O, then O is at 37° west of south from P.
> **Key point:** Back bearing = same angle with the quadrant reversed, N↔S and E↔W.

### Q114. Find the next term of the series 2, 6, 12, 20, 30, ...

> **Type:** Numerical
> **Answer:** 42
> **Solution:** The differences between consecutive terms are 4, 6, 8, 10 — rising by 2 each time, so the next difference is 12 and the next term is 30 + 12 = 42. This is n(n + 1) for n = 1, 2, 3, 4, 5.
> **Key point:** Before hunting for a formula, always compute the first differences; a second-difference pattern is a quadratic in disguise.

### Q115. Find the next term of the series 5, 11, 23, 47, ...

> **Type:** Numerical
> **Answer:** 95
> **Solution:** Each term is double the previous one plus 1: 5 → 11, 11 → 23, 23 → 47, so 47 → 95. The same pattern appears as a − 1 = 4, 10, 22, 46, which is itself a GP with ratio 2.
> **Key point:** A rule of the form "double and add a constant" shows up often in GATE series; check 2a + k for the same k at every step.

### Q116. Complete the series AZ, BY, CX, ...

> **Type:** Numerical
> **Answer:** DW
> **Solution:** In the first position the letters advance A, B, C, so the next is D. In the second position the letters go backwards Z, Y, X, so the next is W. The term is therefore DW.
> **Key point:** Treat each character position as its own sequence; mixed forwards/backwards letter series are common in GATE.

### Q117. Which number does not belong with the others: 121, 144, 169, 200, 225?

(a) 121
(b) 144
(c) 169
(d) 200

> **Type:** MCQ (GATE-1)
> **Answer:** 200 (Option d)
> **Solution:** 121 = 11², 144 = 12², 169 = 13² and 225 = 15² are all perfect squares, whereas 200 is not — √200 = 14.14 is irrational. The sequence of roots is 11, 12, 13, [14], 15, which makes the gap at 200 obvious.
> **Key point:** In an odd-one-out, look for the underlying pattern; the intruder usually also breaks a simple ordering.

### Q118. Complete the analogy: Doctor is to Hospital as Teacher is to ...

(a) Student
(b) School
(c) Class
(d) Lecture

> **Type:** MCQ (GATE-1)
> **Answer:** School (Option b)
> **Solution:** The relation is profession to workplace. A doctor works in a hospital; a teacher works in a school. "Student" and "class" are the people taught rather than the place, and "lecture" is an activity.
> **Key point:** Identify the *type* of relation (person : place, tool : function, part : whole) before hunting for the answer; analogies are a relation-matching exercise.

### Q119. Which conclusion follows from the statement: "Please do not litter the campus; it is an offence." I — Littering attracts a punishment. II — People want a clean campus.

(a) Only I
(b) Only II
(c) Both I and II
(d) Neither I nor II

> **Type:** MCQ (GATE-1)
> **Answer:** Only I (Option a)
> **Solution:** Calling littering an "offence" presupposes a penalty, so I follows. Nothing in the statement appeals to a desire for cleanliness — the appeal is to the deterrent of punishment, so II is not implicit. In a statement–assumption question, test each conclusion as something the speaker could not avoid believing.
> **Key point:** An assumption must be true for the statement to make sense; the speaker's motive (guilt, fear, morality) is the usual discriminator.

### Q120. Statements: All roses are flowers. Some flowers are red. All red things are beautiful. Which conclusions follow? I — Some roses are beautiful. II — Some flowers are beautiful. III — All red things are flowers.

(a) Only I
(b) Only II
(c) Only I and II
(d) Only II and III

> **Type:** MCQ (GATE-2)
> **Answer:** Only II (Option b)
> **Solution:** Some flowers are red, and every red thing is beautiful, so at least those flowers are beautiful — II follows. I fails because the red flowers may all be non-roses, and the statement never says any red thing is a rose. III fails because "all red things are beautiful" says nothing about which *class* red things belong to; beautiful red objects could be apples or cars.
> **Key point:** Chain only along statements that share a class; a gap in the chain (rose → red) kills every conclusion that needs it.

### Q121. Which is the odd one out: B, D, F, I, L?

(a) B
(b) D
(c) F
(d) I

> **Type:** MCQ (GATE-1)
> **Answer:** I (Option d)
> **Solution:** B, D, F and L all occupy even-numbered positions in the alphabet (2, 4, 6, 12), while I is the 9th letter, an odd position. The pattern is positional parity, not shape.
> **Key point:** In letter odd-one-out, check alphabet positions — odd/even position is a common hidden rule.

### Q122. A can complete a piece of work alone in 10 days and B alone in 15 days. They work on alternate days, A starting on the first day. How many days will the work take to finish?

> **Type:** Numerical
> **Answer:** 12 days
> **Solution:** Take the whole work as 1 unit, so A does 1/10 per day and B does 1/15 per day. In each two-day cycle A and B together complete 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 of the work, so six cycles are needed. Six cycles of two days each is 12 days, and in that time A works on days 1, 3, 5, 7, 9, 11 (six days) while B works on days 2, 4, 6, 8, 10, 12 (six days).
> **Key point:** In alternating-day work, group the days into two-day cycles; each cycle delivers A's rate plus B's rate, and the number of cycles decides who finishes the last day.

---

## Section 7. Set G — Verbal drill set

### Q123. Choose the word that is most nearly the *synonym* of FRUGAL.

(a) wasteful
(b) thrifty
(c) lavish
(d) generous

> **Type:** MCQ (GATE-1)
> **Answer:** thrifty (Option b)
> **Solution:** Frugal means sparing with money or resources, which is exactly thrifty. The other three all mean the opposite: wasteful, lavish and generous all imply liberal spending. A synonym test should be instant recognition; if you hesitate, the word is probably in the wrong part of speech.
> **Key point:** Frugal = thrifty = economical; its antonym is extravagant.

### Q124. Choose the word that is most nearly the *antonym* of BENEVOLENT.

(a) generous
(b) hostile
(c) malevolent
(d) gracious

> **Type:** MCQ (GATE-1)
> **Answer:** malevolent (Option c)
> **Solution:** Benevolent means well-meaning and kindly, so its opposite is malevolent, meaning wishing harm on others. "Hostile" is close in effect but describes behaviour rather than intent; GATE answers are normally the word built on the same root with the opposite prefix, so malevolent is the precise antonym.
> **Key point:** The exact antonym of a prefixed word is usually the same root with the opposite prefix: bene- ↔ male-, in- ↔ ex-, inter- ↔ intra-.

### Q125. Choose the word that is most nearly the *synonym* of ABATE.

(a) intensify
(b) diminish
(c) postpone
(d) accelerate

> **Type:** MCQ (GATE-1)
> **Answer:** diminish (Option b)
> **Solution:** Abate means to lessen in intensity or amount, i.e. to diminish. Intensify is the direct opposite. Postpone and accelerate describe time and speed respectively, which is a different axis entirely.
> **Key point:** ABATE, ABATABLE and SUBSIDE all mean "to decrease"; a good synonym is nearly always on the same axis of meaning.

### Q126. Choose the word that is most nearly the *antonym* of EPHEMERAL.

(a) transient
(b) permanent
(c) momentary
(d) fleeting

> **Type:** MCQ (GATE-1)
> **Answer:** permanent (Option b)
> **Solution:** Ephemeral means lasting a very short time, so its opposite is permanent. Transient, momentary and fleeting are all synonyms of ephemeral, which makes the other three options the trap in a well-built MCQ.
> **Key point:** In a synonym/antonym MCQ, one option is correct and the rest are usually the *other* pole — reading all four as if they might be correct is what causes errors.

### Q127. A person who compiles dictionaries is called a lexicographer. What is a person who studies birds called?

(a) ornithologist
(b) botanist
(c) geologist
(d) anthropologist

> **Type:** MCQ (GATE-1)
> **Answer:** ornithologist (Option a)
> **Solution:** Bird study is ornithology and its practitioner an ornithologist. Botany is plants, geology is the Earth's structure and anthropology is human societies, so those three are the distractors.
> **Key point:** Learn the -logy suffixes: bio- life, geo- earth, anthro- human, ornitho- bird, entomo- insect, astro- star.

### Q128. Which term describes government by the people themselves?

(a) aristocracy
(b) democracy
(c) monarchy
(d) oligarchy

> **Type:** MCQ (GATE-1)
> **Answer:** democracy (Option b)
> **Solution:** Democracy is rule by the many, exercised directly or through representatives. Monarchy is rule by one, aristocracy and oligarchy are rule by a privileged few.
> **Key point:** -cracy means rule: democracy (people), aristocracy (nobles), oligarchy (few), autocracy (self), bureaucracy (office).

### Q129. In the sentence "The speaker's argument was cogent, and it forced the audience to reconsider its position," the word cogent means:

(a) confused
(b) weak
(c) convincing
(d) lengthy

> **Type:** MCQ (GATE-1)
> **Answer:** convincing (Option c)
> **Solution:** "Cogent" means clear, logical and persuasive. The clause "it forced the audience to reconsider" is direct contextual evidence: an argument that changes minds must have been persuasive, not weak or confused. "Lengthy" is an accidental near-miss because the word looks long.
> **Key point:** Use the surrounding clause as the definition — in an in-context vocabulary question the context is authoritative over your memory.

### Q130. Choose the word that best completes the sentence: "Despite the INTENSE scrutiny of the proposal, the board APPROVED it without amendment."

(a) mild
(b) cursory
(c) routine
(d) nominal

> **Type:** MCQ (GATE-1)
> **Answer:** mild (Option a)
> **Solution:** "Despite" sets up a contrast, and the board approved the proposal despite the scrutiny — so the scrutiny must have been severe, and intense is correct as written. The question asks for the word *most nearly opposite* in meaning to INTENSE, and that is mild. Cursory means hasty, routine means usual, nominal means existing in name only; none of them is the antonym.
> **Key point:** Watch for a contrastive signal such as "despite" or "although" — it tells you the clause is the opposite of what the main clause suggests.

Read the following passage carefully and answer Q131 to Q133.

> A hundred years ago the handloom weavers of Kanchipuram supplied almost every household in the region. The craft required a loom, a pit, and a family that had learned the pattern-reading from childhood. When powerlooms arrived, the weavers did not stop at once; they lowered their prices, worked longer hours, and accepted smaller margins for nearly a decade. What finally ended the weaving families was not the arrival of the machines but the arrival of a supplier in the neighbouring town who could supply a synthetic thread that no handloom could handle. The families moved, the pits filled in, and the market vanished.

### Q131. The primary purpose of the first paragraph is to:

(a) describe the technique of reading loom patterns
(b) contrast an earlier, self-contained craft economy with its collapse
(c) argue that powerlooms were cheaper than handlooms
(d) list the reasons people left Kanchipuram

> **Type:** MCQ (GATE-1)
> **Answer:** (b) contrast an earlier, self-contained craft economy with its collapse (Option b)
> **Solution:** The paragraph opens with the weavers supplying every household, shows a self-sufficient system built on family skill, and closes with the families moving out and the market vanishing. That is a before-and-after contrast. Option (a) describes one clause only, option (c) is contradicted — the machines were the *slow* cause, not the cheap one — and option (d) attributes the cause to a supplier, whereas the passage's real point is the thread, not the supplier.
> **Key point:** Main-idea options are judged by scope: the correct one must cover the whole paragraph, not a single sentence of it.

### Q132. The author says the final blow to the weaving families was the arrival of a supplier. This suggests that:

(a) the powerloom was technologically inferior to the handloom
(b) the collapse depended on an unforeseen market gap as much as on machinery
(c) suppliers are more dangerous than machines in all trades
(d) the weavers had refused to adopt the new machinery

> **Type:** MCQ (GATE-2)
> **Answer:** (b) the collapse depended on an unforeseen market gap as much as on machinery (Option b)
> **Solution:** The author explicitly says the end came not from the machines but from a thread supply that handlooms could not handle. That is the author's argument for a compound cause, so (b) is the inference. (a) and (d) have no support anywhere in the passage, and (c) overreaches by generalising to "all trades" from one case.
> **Key point:** An inference must be *entailed* by the passage, not merely consistent with it; a word like "all" in an option is a reliable warning.

### Q133. The word "vanished" in the last sentence is closest in meaning to:

(a) expanded
(b) disappeared completely
(c) was recorded
(d) was renamed

> **Type:** MCQ (GATE-1)
> **Answer:** (b) disappeared completely (Option b)
> **Solution:** The sequence is "the families moved, the pits filled in, and the market vanished" — a cumulative list of losses, so the market ceased to exist altogether. Expanded contradicts the sentence, and "recorded" or "renamed" introduce meanings the word does not have.
> **Key point:** For in-context word meaning, read the whole sentence — the neighbouring items in a list usually set the sense.

Read the following passage and answer Q134 and Q135.

> Sleep is not lost time. During deep sleep the body repairs tissue and consolidates the memory laid down during the day, which is why a student who studies until 2 a.m. and then sleeps three hours typically recalls less than one who studies for fewer hours and sleeps seven. The same holds for the physical system: growth hormone is released in pulses during deep sleep, so growth cannot be compressed into a short night no matter how efficient the rest of the routine is. Sleep is maintenance, and maintenance cannot be done in a fraction of the time.

### Q134. The comparison of sleep to maintenance is used to show that:

(a) maintenance work is more tiring than other work
(b) the body can be trained to need less sleep
(c) a required activity cannot simply be done faster
(d) sleep is the only activity that matters for health

> **Type:** MCQ (GATE-1)
> **Answer:** (c) a required activity cannot simply be done faster (Option c)
> **Solution:** The closing sentence says maintenance "cannot be done in a fraction of the time". The earlier examples — memory consolidation and growth-hormone pulses — are the evidence: both are tied to the *duration and depth* of sleep, so compressing the night cannot reproduce the effect. (b) is contradicted outright, (a) is never claimed, and (d) overreaches by making sleep the only thing that matters.
> **Key point:** The author's own metaphor is usually the thesis; look at the sentence that generalises from the examples.

### Q135. According to the passage, a student who studies until 2 a.m. and sleeps only three hours will:

(a) still consolidate memory because study is the dominant factor
(b) recall less than a student who studies less and sleeps seven hours
(c) grow faster provided the routine is efficient
(d) perform identically if the total hours are equal

> **Type:** MCQ (GATE-2)
> **Answer:** (b) recall less than a student who studies less and sleeps seven hours (Option b)
> **Solution:** The passage states this almost verbatim: such a student "typically recalls less than one who studies for fewer hours and sleeps seven". (a) contradicts it, (c) is refuted by the growth-hormone sentence, and (d) ignores the passage's central claim that the *distribution* of hours matters, not merely the total.
> **Key point:** A question whose wording nearly matches a sentence in the passage is usually the correct one; paraphrase-matching beats inference here.

### Q136. Choose the correctly spelt word.

(a) accomodate
(b) accommodate
(c) acommodate
(d) accomodate

> **Type:** MCQ (GATE-1)
> **Answer:** (b) accommodate (Option b)
> **Solution:** The spelling is accommodate — two c's, two m's, and a single c before the final e. Options (a) and (d) drop a c and (c) drops an m, so all three are misspellings. AC-COM-MO-DATE makes the doubling easy to remember.
> **Key point:** Check the fixed points of a word: double consonants are what spell-checkers most often reject in a correctly spelled answer.

### Q137. "He was reluctant to commit, so he gave only a qualified approval of the proposal." What does "qualified" mean in this sentence?

(a) highly trained
(b) limited or conditional
(c) deliberately vague for lack of time
(d) legally certified

> **Type:** MCQ (GATE-2)
> **Answer:** (b) limited or conditional (Option b)
> **Solution:** "Qualified" here means restricted or conditional, and "reluctant to commit" in the preceding clause confirms it: the approval carried conditions. "Highly trained" is a different sense of the word (a qualified engineer), which is the trap in this question.
> **Key point:** Many words have a professional sense and a general sense; let the rest of the sentence decide which one is live.

### Q138. In the sentence "The results were inconclusive; nevertheless the team proceeded with the trial," what does "nevertheless" do?

(a) shows a contrast between the clauses
(b) shows a cause and effect
(c) shows a sequence in time
(d) shows a comparison of quantities

> **Type:** MCQ (GATE-1)
> **Answer:** (a) shows a contrast between the clauses (Option a)
> **Solution:** "Nevertheless" is a connective of concession: it sets an expected conclusion against the one actually taken. Inconclusive results would normally stop a trial, yet the team proceeded, so the two clauses are in contrast. It is not causal (the results did not cause the decision) and it is not a temporal or quantitative connective.
> **Key point:** Learn the six connectives: but/however/nevertheless (contrast), so/because/therefore (cause), then/afterwards (time), like/such as (comparison), moreover (addition), otherwise (condition).

### Q139. "The professor is an authority on medieval poetry, and he is also a competent tutor." What does this sentence suggest?

(a) The professor is a poet.
(b) The professor is skilled at teaching.
(c) The professor's students write poetry.
(d) The professor dislikes teaching.

> **Type:** MCQ (GATE-1)
> **Answer:** (b) The professor is skilled at teaching (Option b)
> **Solution:** "A competent tutor" states directly that the professor teaches competently, so (b) is stated rather than merely suggested. (a) confuses being an authority on a subject with writing it; (c) is a further step not mentioned; (d) is contradicted by the tone.
> **Key point:** Distinguish "is an authority on X" (knows about X) from "does X" — this distinction generates a large share of reading-comprehension errors.

### Q140. Which word best fills the blank: "The government apologised for the leak without ____ the underlying cause."

(a) explaining
(b) exaggerating
(c) escaping
(d) ignoring

> **Type:** MCQ (GATE-2)
> **Answer:** (a) explaining (Option a)
> **Solution:** An apology that "without explaining the underlying cause" is an incomplete apology, which is the natural reading and makes the sentence meaningful. Exaggerating and escaping do not fit the sense, and "without ignoring the cause" would be odd since an apology normally does address the cause.
> **Key point:** In a fill-in-the-blank, pick the word that makes the sentence say something sensible; the "without + verb" frame usually wants a verb that negates the expected action.

### Q141. "He decided to make a long story short and left the meeting early." What does the idiom mean?

(a) he told a lengthy joke
(b) he told it briefly
(c) he cut the story short by lying
(d) he left before finishing the story

> **Type:** MCQ (GATE-1)
> **Answer:** (b) he told it briefly (Option b)
> **Solution:** "To make a long story short" is a fixed expression meaning to relate something in brief, so the man summarised his account and left. Option (d) is a plausible misreading that ignores the idiom entirely.
> **Key point:** Idioms must be matched as whole units; splitting them into their individual words produces exactly the wrong answer.

### Q142. Which of the following sentences is grammatically correct?

(a) Neither of the two candidates have submitted their documents.
(b) Each of the students have a different background.
(c) The number of applicants were large.
(d) The committee has decided to postpone the meeting.

> **Type:** MCQ (GATE-1)
> **Answer:** (d) The committee has decided to postpone the meeting (Option d)
> **Solution:** (d) is correct because a single collective noun used as one body takes a singular verb. In (a), "neither" is singular, so the verb must be "has". In (b), "each" is singular, so it must be "has". In (c), "the number of" takes a singular verb, so it should be "was"; "a number of" would take "were".
> **Key point:** Neither, each, every and one of take singular verbs; "the number of" is singular while "a number of" is plural.

---

## Section 8. Set H — Mixed 1-mark rapid-fire recall set

Answer each in under thirty seconds. These are pure recall and quick-computation items.

### Q143. What is 1% of 1% of 10,000?

> **Type:** Numerical
> **Answer:** 1
> **Solution:** 1% of 10,000 is 100, and 1% of 100 is 1. The two 1%s multiply to 1/10,000, and 10,000/10,000 = 1.
> **Key point:** Percentages of percentages multiply: 1% of 1% = 0.01%, not 2% and not 1%.

### Q144. What is √625?

> **Type:** Numerical
> **Answer:** 25
> **Solution:** 25² = 625, so √625 = 25. Recognise squares of 5, 10, 15, 20 and 25 — 5² = 25, 10² = 100, 15² = 225, 20² = 400, 25² = 625 — and most integer square roots need no work at all.
> **Key point:** Memorise the squares up to 30; they cover most GATE options that are perfect squares.

### Q145. What is the sum of the first 30 natural numbers?

> **Type:** Numerical
> **Answer:** 465
> **Solution:** Sum = n(n + 1)/2 = 30 × 31/2 = 15 × 31 = 465.
> **Key point:** Σ1 to n = n(n + 1)/2; the answer must be a whole number, so one of n, n + 1 must be even.

### Q146. What is 15% of one-third of 600?

> **Type:** Numerical
> **Answer:** 30
> **Solution:** One-third of 600 is 200, and 15% of 200 is 30. Working the other way: 15% of 600 is 90, and one-third of 90 is 30 — the two operations commute because they are a scalar and a scaling.
> **Key point:** "a% of (1/n) of X" can be done in either order; take whichever intermediate is a whole number.

### Q147. A body travels 72 km at a uniform speed of 18 m/s. How many seconds does it take?

> **Type:** Numerical
> **Answer:** 4000 seconds
> **Solution:** Convert 72 km to metres: 72,000 m. Time = 72,000 ÷ 18 = 4000 s. Note that 18 m/s is exactly 5/18 × 54 = ... more usefully, 18 m/s is the same as 64.8 km/h, so converting to km/h first gives 72 ÷ 64.8 h = 1.111 h = 4000 s.
> **Key point:** If the speed is already in m/s, convert the *distance* to metres, not the speed to km/h.

### Q148. How many minutes are there in 3.5 hours?

> **Type:** Numerical
> **Answer:** 210 minutes
> **Solution:** 3.5 × 60 = 210 minutes. The .5 hour is exactly 30 minutes, so 3 hours 30 minutes = 210 minutes.
> **Key point:** Multiply by 60 to go to minutes; 0.5 h = 30 min and 0.25 h = 15 min are worth memorising.

### Q149. What is the cube root of 1331?

> **Type:** Numerical
> **Answer:** 11
> **Solution:** 11³ = 11 × 11 × 11 = 121 × 11 = 1331. The cubes worth knowing are 2³ = 8, 3³ = 27, 4³ = 64, 5³ = 125, 6³ = 216, 7³ = 343, 8³ = 512, 9³ = 729, 10³ = 1000, 11³ = 1331.
> **Key point:** Memorise cubes to 11³ = 1331 and squares to 31² = 961; cube-root options in GATE are always round numbers.

### Q150. What is the value of (1/2)⁻²?

> **Type:** Numerical
> **Answer:** 4
> **Solution:** A negative power means reciprocal: (1/2)⁻² = 1/((1/2)²) = 1/(1/4) = 4. Equivalently, (1/2)⁻¹ = 2 and squaring gives 4.
> **Key point:** a⁻ⁿ = 1/aⁿ; a negative exponent flips a fraction over rather than making it negative.

### Q151. What is the HCF of 24 and 36?

> **Type:** Numerical
> **Answer:** 12
> **Solution:** 24 = 2³ × 3 and 36 = 2² × 3². The HCF takes the lowest power of every common prime: 2² × 3 = 12. The LCM, by contrast, would be 2³ × 3² = 72.
> **Key point:** HCF = lowest powers, LCM = highest powers; this pair is the standard one to test both on.

### Q152. One radian is approximately equal to how many degrees?

> **Type:** Numerical
> **Answer:** 57.3°
> **Solution:** A full circle is 2π radians and 360°, so one radian = 360/(2π) = 180/π ≈ 180/3.1416 ≈ 57.296°, i.e. 57.3°. Conversely π radians = 180°.
> **Key point:** 180° = π rad and 1 rad = 57.3°; the conversion factor 180/π is the only one you ever need.

### Q153. A right triangle has a base of 10 cm and a height of 6 cm. What is its area in cm²?

> **Type:** Numerical
> **Answer:** 30 cm²
> **Solution:** Area of a triangle = ½ × base × height = ½ × 10 × 6 = 30 cm². The trap is to omit the ½ and answer 60.
> **Key point:** Triangle area always carries the ½; rectangle, parallelogram and rhombus do not.

### Q154. A cone has base radius 3 cm and vertical height 4 cm. What is its slant height?

> **Type:** Numerical
> **Answer:** 5 cm
> **Solution:** The slant height is √(r² + h²) = √(9 + 16) = √25 = 5 cm, a 3-4-5 right triangle formed by the radius, the height and the slant height meeting at the apex.
> **Key point:** r, h and l always form a right triangle with l as the hypotenuse; spot a Pythagorean triple instantly.

### Q155. What is 5! + 4!?

> **Type:** Numerical
> **Answer:** 144
> **Solution:** 5! = 120 and 4! = 24, so the sum is 144.
> **Key point:** n! = n × (n − 1)!; knowing 4! = 24 and 5! = 120 is enough for most factorial options.

### Q156. What is the SI unit of luminous intensity?

> **Type:** Numerical
> **Answer:** The candela (cd)
> **Solution:** Luminous intensity is measured in candela. The related quantities are illuminance in lux (lumens per square metre) and luminous flux in the lumen, so the three are easy to confuse.
> **Key point:** candela = intensity, lumen = flux, lux = illuminance; "candle power" is the obsolete name for the candela.

### Q157. What is the SI unit of electrical resistance?

> **Type:** Numerical
> **Answer:** The ohm (Ω)
> **Solution:** Resistance is measured in ohms. Conductance is its reciprocal, the siemens; current is the ampere and voltage the volt.
> **Key point:** V = IR links volt, ampere and ohm, and R = V/I is the quickest way to recall the unit of any of the three.

### Q158. How many minutes are there in 1.25 hours?

> **Type:** Numerical
> **Answer:** 75 minutes
> **Solution:** 1.25 × 60 = 75 minutes, i.e. 1 hour 15 minutes.
> **Key point:** Quarter-hours are the common case: 0.25 h = 15 min, 0.5 h = 30 min, 0.75 h = 45 min.

### Q159. What is 7.5% of 480?

> **Type:** Numerical
> **Answer:** 36
> **Solution:** 7.5% is 3/40, and 480 × 3/40 = 12 × 3 = 36. Equivalently, 10% of 480 is 48, and 7.5% is three-quarters of 10%, so 48 × 0.75 = 36.
> **Key point:** Convert 7.5% to 3/40 whenever the quantity is a multiple of 40 — it turns a decimal into a one-step division.

### Q160. A rectangle measures 0.6 m by 50 cm. What is its area in square centimetres?

> **Type:** Numerical
> **Answer:** 3000 cm²
> **Solution:** Convert the length to centimetres: 0.6 m = 60 cm. Then the area is 60 × 50 = 3000 cm². Mixing units without converting (0.6 × 50 = 30) is the trap and would give an area in inconsistent units.
> **Key point:** Convert *all* lengths to the same unit before multiplying; 1 m = 100 cm is the conversion that removes metres.

---

## Section 9. Set I — Mixed 2-mark GATE-style set

Each of these combines two topics, as real GATE Section A questions do.

### Q161. A train 240 m long runs at 90 km/h on a parallel track. A man walking at 18 km/h in the same direction is 120 m ahead of the train's engine. How long does the train take to overtake him completely?

> **Type:** Numerical
> **Answer:** 18 seconds
> **Solution:** Same direction, so the relative speed is 90 − 18 = 72 km/h = 72 × 5/18 = 20 m/s. To pass the man completely, the rear of the train must get 240 m past him; the engine must therefore close the initial 120 m gap and then cover the train's own 240 m, a relative distance of 360 m. Time = 360 ÷ 20 = 18 s.
> **Key point:** In an overtaking problem the distance is the gap *plus* the full length of the overtaking vehicle; the relative speed is the difference of the two speeds.

### Q162. A cylindrical tank of radius 7 m and height 5 m is filled by a pump at 154 m³ per hour. How long does it take to fill completely? (Take π = 22/7.)

> **Type:** Numerical
> **Answer:** 5 hours
> **Solution:** Volume = πr²h = (22/7) × 49 × 5 = 22 × 7 × 5 = 770 m³. At 154 m³/h the time is 770 ÷ 154 = 5 hours. The numbers are chosen so that the radius being a multiple of 7 cancels π and the division comes out exact.
> **Key point:** With π = 22/7 given, expect a radius that is a multiple of 7 — then the volume calculation leaves only simple arithmetic.

### Q163. What is the compound interest on ₹20,000 at 10% per annum for 2 years, compounded annually?

> **Type:** Numerical
> **Answer:** ₹4,200
> **Solution:** Amount = 20000 × (1.1)² = 20000 × 1.21 = ₹24,200. The compound interest is 24,200 − 20,000 = ₹4,200. The simple interest would be only 20000 × 0.10 × 2 = ₹4,000, so the second-year interest is ₹200 more under compounding — that difference is exactly why the question specifies "compounded".
> **Key point:** CI = P[(1 + r/100)ⁿ − 1]; the CI−SI gap for 2 years is P(r/100)², here 20000 × 0.01 = ₹200.

### Q164. A can do a piece of work in 12 days and B in 18 days. They start together, and A leaves after 4 days. How many more days does B take to finish the work?

> **Type:** Numerical
> **Answer:** 12 days
> **Solution:** In 4 days A completes 4/12 = 1/3 of the work, leaving 2/3. B works at 1/18 per day, so the remaining work takes (2/3) × 18 = 12 days. The total elapsed time is 4 + 12 = 16 days.
> **Key point:** Do the departing worker's share first, then divide the remainder by the survivor's rate; the "days after leaving" answer excludes the shared days.

### Q165. Two concentric circles have areas in the ratio 9 : 16. If the area of the ring between them is 154 cm², what is the area of the inner circle in cm²?

> **Type:** Numerical
> **Answer:** 198 cm²
> **Solution:** Write the areas as 9k and 16k. The ring is the difference, 16k − 9k = 7k = 154, so k = 22. The inner area is 9k = 9 × 22 = 198 cm². The outer area is 16k = 352 cm², and 352 − 198 = 154 confirms the ring.
> **Key point:** With area ratios given, work in units of k and find k from the quantity you are given; no π or radius is needed.

### Q166. Two fair dice are thrown together. What is the probability that the sum of the numbers shown is 8?

> **Type:** Numerical
> **Answer:** 5/36
> **Solution:** There are 36 equally likely ordered outcomes. A sum of 8 comes from (2,6), (3,5), (4,4), (5,3) and (6,2) — five outcomes. The probability is 5/36, which is irreducible. Counting the reverse pairs as distinct is essential, since (2,6) and (6,2) are different outcomes on two dice.
> **Key point:** On two dice there are 36 ordered outcomes, never 21; a "sum 8" count of 5 is the standard figure.

### Q167. A bag holds 4 red and 6 black balls. Two balls are drawn at random without replacement. What is the probability that both are red?

> **Type:** Numerical
> **Answer:** 2/15
> **Solution:** Without replacement the probabilities compound: P(first red) = 4/10 = 2/5, and after that 3 red remain out of 9, so P(second red) = 3/9 = 1/3. The product is (2/5) × (1/3) = 2/15. Sampling *with* replacement would have given (2/5)² = 4/25 instead, which is larger — the usual direction of the error.
> **Key point:** Without replacement, the counts change after the first draw, so multiply the conditional probabilities; with replacement, square the single-draw probability.

### Q168. The mean of ten numbers is 18.5. If two numbers, 15 and 25, are removed and replaced by 30 and 20, what is the new mean?

> **Type:** Numerical
> **Answer:** 19.5
> **Solution:** The original total is 10 × 18.5 = 185. Removing 15 and 25 removes 40, leaving 145. Adding 30 and 20 adds 50, giving 195. The count is still 10, so the new mean is 195/10 = 19.5.
> **Key point:** Track the *total*, not the mean — the mean is the total divided by the count, and the count only changes if items are added or removed outright.

### Q169. In an examination 30% of the students failed. The number of failures is 90. If 100 more students are admitted and all of them pass, what percentage of the new batch fails?

> **Type:** Numerical
> **Answer:** 22.5%
> **Solution:** 30% of the batch is 90, so the batch is 90/0.30 = 300 students. Admitting 100 new students who all pass gives a batch of 400, of whom 90 still fail. The new failure percentage is 90/400 × 100 = 22.5%.
> **Key point:** Turn the percentage into an absolute count first; every later question about "what percentage" needs a new count, and the failures stay fixed while the total grows.

### Q170. A circular park has radius 35 m. A path 7 m wide is laid inside it, along the whole circumference. What is the area of the path in m²? (Take π = 22/7.)

> **Type:** Numerical
> **Answer:** 1386 m²
> **Solution:** The inner radius of the path is 35 − 7 = 28 m, so the path area is π(35² − 28²) = π(1225 − 784) = 441π = 441 × 22/7 = 1386 m². The difference of squares can be taken as (35 − 28)(35 + 28) = 7 × 63 = 441, which is the fastest route.
> **Key point:** Ring area = π(R − r)(R + r); computing the difference of squares as a product of sum and difference is quicker than squaring twice.

### Q171. Revisiting the library table of Q83 to Q86: if the Thursday figure falls by 25% and Sunday then issues exactly as many books as Monday, what is the mean issue over the full seven days?

> **Type:** Numerical
> **Answer:** 150 books per day
> **Solution:** The six-day total is 980. Thursday's 200 falls by 25% to 150, a loss of 50, so the six-day total becomes 930. Sunday then adds 120 (equal to Monday), giving a seven-day total of 1050 over 7 days, and 1050/7 = 150 books per day.
> **Key point:** A 25% fall is a quarter exactly, so 200 → 150 costs no division; adjust the total, then re-divide by the new number of days.

### Q172. The intensity of light from a point source follows an inverse-square law. If the source is moved to twice its original distance from a screen, the intensity on the screen becomes:

(a) 4 times
(b) 2 times
(c) one-half
(d) one-fourth

> **Type:** MCQ (GATE-1)
> **Answer:** one-fourth (Option d)
> **Solution:** The inverse-square law says intensity ∝ 1/d². Doubling the distance multiplies the intensity by 1/2² = 1/4. The trap options (a) and (b) come from forgetting to square, or from applying the law twice by mistake.
> **Key point:** Inverse-square quantities drop by the *square* of the distance ratio: double the distance, quarter the quantity.

### Q173. In how many ways can 5 persons be seated in a row of 5 chairs?

> **Type:** Numerical
> **Answer:** 120
> **Solution:** The first chair has 5 choices, the second 4, and so on down to 1, so the number of arrangements is 5 × 4 × 3 × 2 × 1 = 5! = 120.
> **Key point:** Seating n persons in a row is n!; if the row is circular it is (n − 1)!, because rotations are then identical.

### Q174. From a group of 8 men and 5 women, a committee of 3 is to be chosen. How many committees contain at least one woman?

> **Type:** Numerical
> **Answer:** 230
> **Solution:** The total number of committees is C(13,3) = 13 × 12 × 11/(3 × 2 × 1) = 286. Committees with no women come from the 8 men alone: C(8,3) = 8 × 7 × 6/6 = 56. So committees with at least one woman number 286 − 56 = 230.
> **Key point:** "At least one" is easiest as total minus none; the complementary case here is all-men, which is a single binomial coefficient.

### Q175. A cyclist rides at 12 km/h and a walker at 5 km/h. A man spends exactly half his travelling time cycling and half walking on a 68 km journey. How far has he travelled in the first 2 hours?

> **Type:** Numerical
> **Answer:** 17 km
> **Solution:** Half of 2 hours is 1 hour cycling and 1 hour walking, so the distance is 12 × 1 + 5 × 1 = 17 km. Since the question defines the split by *time* rather than by distance, the average speed is simply (12 + 5)/2 = 8.5 km/h, and 8.5 × 2 = 17 km. The 68 km figure only fixes the total journey time, which is irrelevant to the first-2-hours question.
> **Key point:** When time is split equally, average speed is the simple mean of the speeds; when distance is split equally, it is the harmonic mean.

### Q176. The length of a rectangle is 5 m more than its breadth. If its area is 84 m², what is its perimeter in metres?

> **Type:** Numerical
> **Answer:** 38 m
> **Solution:** Let the breadth be b, so the length is b + 5 and b(b + 5) = 84, i.e. b² + 5b − 84 = 0. Factoring, (b + 12)(b − 7) = 0, so b = 7 m and the length is 12 m. The perimeter is 2(7 + 12) = 38 m.
> **Key point:** In a "length = breadth + k, area = A" problem, factorise b² + kb − A; the two roots differ by k and their product is −A.

### Q177. A square field of side 60 m has a path 2 m wide laid inside it along all four sides. What is the area of the path in m²?

> **Type:** Numerical
> **Answer:** 464 m²
> **Solution:** The inner square has side 60 − 2 × 2 = 56 m, because a path of width w on all four sides reduces the side by 2w. The path area is 60² − 56² = 3600 − 3136 = 464 m². Via the difference of squares, (60 − 56)(60 + 56) = 4 × 116 = 464.
> **Key point:** A border of width w on all four sides reduces each side of a square field by 2w, not by w — the classic error is to use 58 and get the wrong area.

### Q178. Two pipes deliver 15 litres/min and 10 litres/min into a 3000-litre tank. Both are opened, and after 18 minutes the 15-litre pipe is closed. How long does the 10-litre pipe then take to fill the rest?

> **Type:** Numerical
> **Answer:** 255 minutes
> **Solution:** In 18 minutes both pipes deliver (15 + 10) × 18 = 25 × 18 = 450 litres, leaving 3000 − 450 = 2550 litres. At 10 litres/min the remaining work takes 2550 ÷ 10 = 255 minutes. The total elapsed time is 18 + 255 = 273 minutes.
> **Key point:** Solve the phases separately: shared period first, then the single-pipe period; "how long afterwards" excludes the shared phase.

### Q179. A gear wheel with 45 teeth meshes with another having 30 teeth. The first turns at 60 revolutions per minute. What is the speed and direction of the second?

> **Type:** Numerical
> **Answer:** 90 revolutions per minute, in the opposite direction
> **Solution:** Meshed gears have equal tangential speed, so teeth × rpm is the same for both: 45 × 60 = 30 × n, giving n = 90 rpm. Meshed external gears always rotate in opposite directions, so the second turns the other way.
> **Key point:** For meshed gears, teeth × rpm is constant and the directions are opposite; inside a gear train the direction flips once per external mesh.

### Q180. A solid sphere of radius 7 cm is melted completely and recast into a cylinder of the same radius, 7 cm. What is the height of the cylinder in cm? (Take π = 22/7.)

> **Type:** Numerical
> **Answer:** 28/3 ≈ 9.33 cm
> **Solution:** Volume is conserved on melting, so (4/3)πr³ = πr²h, which gives h = 4r/3 = 4 × 7/3 = 28/3 ≈ 9.33 cm. Notice the result is 1.333 r, comfortably less than the sphere's own diameter of 2r = 14 cm, which is what the volume ratio requires.
> **Key point:** Melting-and-recast problems are pure volume equations — set the volumes equal, cancel π, and the linear dimension follows directly.

---

## Section 10. Set J — Common-mistake trap set

Each question here is built so that one realistic error produces one specific wrong answer. Read the Solution to see where the trap lies.

### Q181. Three numbers have a mean of 20. A fourth number is added to the set and the new mean is 24. What is the fourth number?

> **Type:** Numerical
> **Answer:** 36
> **Solution:** The original total is 3 × 20 = 60. The new total is 4 × 24 = 96, so the added number is 96 − 60 = 36. The trap answer is 24, obtained by simply writing down the new mean, or 4, by subtracting the means — both ignore that the count changed.
> **Key point:** When the count of items changes, means cannot be subtracted to find an item; convert both to totals first.

### Q182. A car covers a certain distance in 4 hours at 60 km/h. A second car covers the same distance in 6 hours. What is the second car's speed?

> **Type:** Numerical
> **Answer:** 40 km/h
> **Solution:** The distance is 60 × 4 = 240 km. At 6 hours the speed is 240 ÷ 6 = 40 km/h. The trap answer is 90 km/h, obtained by adding the two times (4 + 6) or by multiplying rather than dividing (60 × 6/4 = 90 comes from the wrong pairing).
> **Key point:** For the *same distance*, speed is inversely proportional to time — a longer time means a lower speed, so any answer above 60 is already wrong.

### Q183. A sum grows at 10% compounded annually. By what fraction does the simple interest on the same sum for 2 years fall short of the compound interest?

> **Type:** Numerical
> **Answer:** 1/100 of the principal (1%)
> **Solution:** Let the principal be P. Simple interest for 2 years is P × 10/100 × 2 = 0.2P. Compound interest is P[(1.1)² − 1] = P(1.21 − 1) = 0.21P. The shortfall is 0.21P − 0.20P = 0.01P = P/100. The general identity is that the gap equals P(r/100)², and here r = 10 gives P/100.
> **Key point:** CI − SI for 2 years is exactly P(r/100)²; the common error is to forget that the second year's interest is also compounded.

### Q184. A pipe delivers water at 2.5 cubic metres per minute. How long does it take to fill a tank of volume 12,000 litres? (Take 1 m³ = 1000 litres.)

> **Type:** Numerical
> **Answer:** 288 seconds
> **Solution:** Convert the tank volume to cubic metres: 12,000 litres = 12,000/1000 = 12 m³. At 2.5 m³/min the time is 12 ÷ 2.5 = 4.8 min, and 4.8 min × 60 s/min = 288 s. The trap answer is 4800, obtained by treating 12,000 litres as 12,000 m³ — that is, using the numerator as though it were already in cubic metres.
> **Key point:** Match the units before dividing: a rate in m³/min needs a volume in m³, and 1000 L = 1 m³.

### Q185. The angles of a quadrilateral are in the ratio 1 : 2 : 3 : 4. What is the largest angle?

(a) 90°
(b) 108°
(c) 120°
(d) 144°

> **Type:** MCQ (GATE-1)
> **Answer:** 144° (Option d)
> **Solution:** The four parts sum to 10, and the interior angles of a quadrilateral sum to 360°, so one part is 360/10 = 36°. The angles are 36°, 72°, 108° and 144°, and the largest is 144°. The trap is 90°, which is what you get by dividing 360° by 4 — i.e. by assuming the four angles are equal, which is only true for a square, not for any ratio.
> **Key point:** Anchor every angle-ratio question on the polygon's angle sum: 180°, 360°, 540°, 720° for n = 3, 4, 5, 6. Then the largest part is the largest multiple of 360/(sum of parts).

### Q186. The radius of a circle is doubled. By what factor does its area change?

(a) 2
(b) 3
(c) 4
(d) 8

> **Type:** MCQ (GATE-1)
> **Answer:** 4 (Option c)
> **Solution:** A = πr², so the area scales as the square of the radius: 2² = 4 times. The trap is option (a) = 2, the linear answer, obtained by forgetting the square. Note that the *circumference* would merely double, so doubling the radius doubles the circumference but quadruples the area.
> **Key point:** Radius doubled ⇒ circumference ×2, area ×4. This one distinction is the most commonly tested point in mensuration MCQs.

### Q187. What is the greatest number that divides 1326 and 1575 exactly?

> **Type:** Numerical
> **Answer:** 3
> **Solution:** Both numbers are divisible by 3 (1326 = 3 × 442 and 1575 = 3 × 525), so the HCF is at least 3. To test a larger candidate, note 1326 ÷ 9 = 147.33, so 9 does not divide 1326. Running the algorithm: 1575 − 1326 = 249; 1326 = 5 × 249 + 81; 249 = 3 × 81 + 6; 81 = 13 × 6 + 3; 6 = 2 × 3. The HCF is 3. The trap answer is 9, spotted because both numbers are divisible by 3 and the digit sums (1+3+2+6 = 12, 1+5+7+5 = 18) are multiples of 3 — a test that proves divisibility by 3, never by 9.
> **Key point:** A digit sum divisible by 3 proves only divisibility by 3; 9 needs the sum divisible by 9, and 1326's sum of 12 fails that test.

### Q188. What is the sum 1 + 2 + 4 + 8 + … + 1024?

> **Type:** Numerical
> **Answer:** 2047
> **Solution:** This is a geometric series with first term 1, ratio 2, and last term 1024 = 2¹⁰, so there are 11 terms. The sum is a(2ⁿ − 1)/(2 − 1) = 1 × (2¹¹ − 1)/1 = 2048 − 1 = 2047. The trap answers are 1024 (someone stops at the last term) and 2048 (someone forgets the −1).
> **Key point:** A geometric series 1 + 2 + 4 + … + 2ⁿ sums to 2ⁿ⁺¹ − 1; the "minus one" is exactly the thing that gets dropped.

### Q189. Two vessels hold milk and water in the ratios 3 : 1 and 5 : 3 respectively. If 12 litres from the first vessel and 27 litres from the second are mixed, what is the ratio of milk to water in the mixture?

> **Type:** Numerical
> **Answer:** 69 : 35
> **Solution:** From the first vessel, milk = 12 × 3/4 = 9 L and water = 12 × 1/4 = 3 L. From the second, milk = 27 × 5/8 = 135/8 = 16.875 L and water = 27 × 3/8 = 81/8 = 10.125 L. Total milk = 9 + 135/8 = 72/8 + 135/8 = 207/8, and total water = 3 + 81/8 = 24/8 + 81/8 = 105/8. The ratio is 207 : 105, which reduces by 3 to 69 : 35.
> **Key point:** In an alligation question, convert *both* vessels to absolute litres first and only then form the ratio; combining part-ratios directly is the standard trap.

### Q190. A machine produces 5 units in 6 minutes and 10 units in 12 minutes. How long does it take to produce 15 units?

> **Type:** Numerical
> **Answer:** 18 minutes
> **Solution:** A machine at a constant rate gives a consistent rate in both cases: 5 units in 6 min and 10 units in 12 min are both 5/6 units per minute. So 15 units take 15 ÷ (5/6) = 15 × 6/5 = 18 min. The trap answer is 21 minutes, from adding the two times (6 + 12) on the assumption that the work is additive.
> **Key point:** A uniform rate means the times are in direct proportion to the work; 15 units is three times 5 units, so the time is three times 6 minutes.

### Q191. A fair coin is tossed twice. What is the probability of getting exactly one head?

(a) 1/4
(b) 1/3
(c) 1/2
(d) 3/4

> **Type:** MCQ (GATE-1)
> **Answer:** 1/2 (Option c)
> **Solution:** The four equally likely outcomes are HH, HT, TH and TT. Exactly one head occurs in HT and TH, so the probability is 2/4 = 1/2. The trap answer is 1/4, from counting only HT and forgetting that TH is a different outcome.
> **Key point:** On two tosses the sample space is 4, not 2; "exactly one head" counts HT *and* TH.

### Q192. What is √0.25 + √0.04?

> **Type:** Numerical
> **Answer:** 0.7
> **Solution:** √0.25 = 0.5 and √0.04 = 0.2, so the sum is 0.7. The trap answer is √0.29 ≈ 0.539, from wrongly pushing the addition under the single square root.
> **Key point:** √a + √b ≠ √(a + b); take each root separately. This is the most common surd error in the paper.

### Q193. A cube of side 3 cm is cut into 27 cubes of side 1 cm. What is the total surface area of the 27 small cubes together, in cm²?

> **Type:** Numerical
> **Answer:** 162 cm²
> **Solution:** Each small cube has surface area 6 × 1² = 6 cm², and there are 27 of them, so the combined surface area is 27 × 6 = 162 cm². The original cube's surface area was 6 × 3² = 54 cm², so cutting has tripled the total exposed area because the internal cut faces add up.
> **Key point:** Cutting a solid into n³ small cubes multiplies the total surface area by n; here 3³ = 27 pieces, and 27 × 6 = 162 against the original 54.

### Q194. If x + 1/x = 4, find the value of x³ + 1/x³.

> **Type:** Numerical
> **Answer:** 52
> **Solution:** Use the cube expansion: (x + 1/x)³ = x³ + 3x + 3/x + 1/x³, so x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x). Substituting 4: 64 − 12 = 52. The trap answer is 64, from merely cubing the given value and forgetting the cross terms.
> **Key point:** a³ + b³ = (a + b)³ − 3ab(a + b); with a·b = 1 here, the correction is 3 × 4 = 12.

### Q195. A man walks 4 m north, turns right and walks 3 m, turns right again and walks 4 m, then turns right a third time and walks 3 m. How far is he from the starting point?

> **Type:** Numerical
> **Answer:** 0 m — he is back at the starting point
> **Solution:** Tracing the path with east as +x and north as +y: north 4 gives (0, 4); right from north faces east, so 3 east gives (3, 4); right again faces south, so 4 south gives (3, 0); right again faces west, so 3 west gives (0, 0). The four legs trace a closed rectangle, so he returns exactly to the start. The trap answer is 10 m, the total distance walked, or 2 m, from cancelling only one pair of legs.
> **Key point:** In a closed rectangular walk, opposite legs cancel one pair at a time; track the coordinates rather than the total distance.

### Q196. An analog clock shows 3:15. What is the angle between the hour and minute hands, in degrees?

(a) 0°
(b) 7.5°
(c) 90°
(d) 180°

> **Type:** MCQ (GATE-1)
> **Answer:** 7.5° (Option b)
> **Solution:** The minute hand at 15 minutes points at 3, i.e. 15 × 6° = 90° from 12. The hour hand is not at 3 exactly: it moves 0.5° per minute, so at 3:15 it is at 3 × 30° + 15 × 0.5° = 90° + 7.5° = 97.5°. The angle between them is 97.5° − 90° = 7.5°. The trap answer 90° is the error of treating the hour hand as fixed at the numeral.
> **Key point:** The hour hand moves 30° per hour *and* 0.5° per minute; forgetting the 0.5° per minute is the single most common clock-angle error.

### Q197. What is 40% of 50% of 200?

> **Type:** Numerical
> **Answer:** 40
> **Solution:** 50% of 200 is 100, and 40% of 100 is 40. Working in one line: 0.40 × 0.50 × 200 = 0.20 × 200 = 40. The trap answers are 90 (40 + 50) and 20 (treating the two percentages as a single combined discount of 20% and mis-scaling).
> **Key point:** Percentages of percentages multiply: 40% of 50% is 20% of the base, not 90% and not 0.2% of the base.

### Q198. How many perfect squares lie strictly between 20 and 80?

(a) 4
(b) 5
(c) 6
(d) 7

> **Type:** MCQ (GATE-1)
> **Answer:** 4 (Option a)
> **Solution:** √20 ≈ 4.47 and √80 ≈ 8.94, so the integers n with 20 < n² < 80 are n = 5, 6, 7, 8, giving 25, 36, 49 and 64. That is 4 squares. The trap is 5, from including 16 (which is below 20) or 81 (above 80) because they are near the bounds.
> **Key point:** Convert the interval to a range of *roots* first — from √20 to √80 is 4.47 to 8.94, so count the integers 5, 6, 7, 8 in between.

---

## Section 11. Set K — Previous-year pattern set

Ten questions arranged exactly as a real GATE Section A paper, in the order the paper presents them, with the section tag noted. Attempt in 60 minutes.

### Q199. [Section: Quantitative Aptitude] What is the value of three-fourths of 60% of 500?

(a) 225
(b) 250
(c) 275
(d) 300

> **Type:** MCQ (GATE-1)
> **Answer:** 225 (Option a)
> **Solution:** 60% of 500 is 300, and three-fourths of 300 is 225. Doing it in one line: 0.75 × 0.60 × 500 = 0.45 × 500 = 225. The trap is 250, obtained by taking 60% and then subtracting a quarter wrongly, or 300 by stopping at the 60%.
> **Key point:** A chain of fractions and percentages multiplies in one step: 0.75 × 0.60 = 0.45, so the answer is 45% of 500.

### Q200. [Section: Quantitative Aptitude] If the roots of x² − 5x + 3 = 0 are α and β, find α³ + β³.

> **Type:** Numerical
> **Answer:** 80
> **Solution:** By Vieta's relations, α + β = 5 and αβ = 3. Then α³ + β³ = (α + β)³ − 3αβ(α + β) = 125 − 3 × 3 × 5 = 125 − 45 = 80. The trap answer is 125 (or 98), from cubing the sum without the correction term.
> **Key point:** For roots of a quadratic, α³ + β³ = (α + β)³ − 3αβ(α + β); the product term is what a GATE question is testing.

### Q201. [Section: Quantitative Aptitude] A, B and C divide a sum of money in the ratio 2 : 3 : 4. If B's share is ₹3,600, what is the total sum?

> **Type:** Numerical
> **Answer:** ₹10,800
> **Solution:** The 9 total parts correspond to ₹3,600 × 3 = ₹10,800, since B holds 3 parts and 3 parts' worth is 3/9 of the whole. One part is 3600 ÷ 3 = ₹1,200, and 9 × 1200 = ₹10,800. A gets ₹2,400 and C gets ₹4,800, and 2400 + 3600 + 4800 = ₹10,800 checks out.
> **Key point:** The total equals a given share multiplied by the total number of parts divided by that share's own parts.

### Q202. [Section: Data Interpretation] Three students wrote the same test. Read the table and answer.

```
Subject        Physics   Mathematics   Chemistry
Maximum marks      100         100           100
Marks obtained     68          75            58
```

Which subject did the student perform worst in, and by how many marks?

> **Type:** Numerical
> **Answer:** Chemistry, by 10 marks
> **Solution:** The lowest mark obtained is 58 in Chemistry. The next lowest is Physics at 68, and 68 − 58 = 10 marks. Mathematics at 75 is the best performance, and the full spread from best to worst is 75 − 58 = 17 marks.
> **Key point:** "Perform worst" means the lowest absolute mark, and the margin is the gap to the *next* lowest, not the gap to the highest.

### Q203. [Section: Verbal Ability] Choose the word most nearly opposite in meaning to FRUGAL.

(a) extravagant
(b) prudent
(c) sparing
(d) modest

> **Type:** MCQ (GATE-1)
> **Answer:** extravagant (Option a)
> **Solution:** Frugal means economical in spending, and extravagant means excessively expensive, which is its opposite. Prudent, sparing and modest are all synonyms or near-synonyms of frugal, so all three are traps: three of the four options sit on the same side of the question.
> **Key point:** When three options are synonyms, they are the trap and the odd one out is the answer — read all four options before deciding.

### Q204. [Section: Verbal Ability] Read the passage and answer.

> A city that introduced a congestion charge in its central district saw average traffic speed rise from 14 km/h to 22 km/h in the first year, but the total number of vehicle trips into the district did not fall. The gain in speed came almost entirely from drivers who had previously been trapped in stop-start traffic on the approach roads, not from a reduction in the number of cars. City officials have since conceded that the scheme moved the problem rather than solving it, since the traffic displaced to the ring roads lengthens journeys for residents of the neighbourhoods through which it now passes.

Why does the author call the scheme a success at first?

(a) Because it reduced the total number of trips into the district.
(b) Because it substantially increased average traffic speed in the district.
(c) Because it saved the city money from road repairs.
(d) Because it was popular with central-district businesses.

> **Type:** MCQ (GATE-2)
> **Answer:** (b) Because it substantially increased average traffic speed in the district (Option b)
> **Solution:** The passage states the speed rose from 14 km/h to 22 km/h, which is a rise of about 57%, and the author then immediately undercuts it by noting the trip count did not fall and the problem was merely displaced. (a) is directly contradicted by "the total number of vehicle trips into the district did not fall". (c) and (d) appear nowhere in the passage.
> **Key point:** A "but" or "however" clause after an apparent success marks it as the setup for the author's real verdict — the achievement is real, the conclusion about it is not.

### Q205. [Section: Logical Reasoning] Statements: All roses are flowers. Some flowers are red. All red things are beautiful. Which conclusion(s) follow? I — Some roses are beautiful. II — Some flowers are beautiful. III — Some beautiful things are flowers.

(a) Only I and II
(b) Only II and III
(c) Only II
(d) None

> **Type:** MCQ (GATE-2)
> **Answer:** Only II (Option c)
> **Solution:** "Some flowers are red" and "all red things are beautiful" give II directly. I fails, since the red flowers need not be roses. III is the converse of II — "some beautiful things are flowers" does not follow, because beauty need not arise only from red things; a blue rose would be beautiful without being red.
> **Key point:** "Some A are B" and "Some B are A" are *not* interchangeable; only existential statements guarantee the reverse, universals never do.

### Q206. [Section: Logical Reasoning] In a certain code, HEART is written as IFBSU. How is EARTH written in that code?

> **Type:** Numerical
> **Answer:** FBSUI
> **Solution:** The rule is that each letter is replaced by the next letter: H→I, E→F, A→B, R→S, T→U, which reproduces IFBSU. Applying it to EARTH: E→F, A→B, R→S, T→U, H→I, giving FBSUI.
> **Key point:** Always validate a coding rule against every letter of the given example before coding the target word.

### Q207. [Section: Logical Reasoning] A man starts facing north, turns 45° anticlockwise, then 90° clockwise, and finally 135° anticlockwise. Which direction is he facing at the end?

(a) East
(b) West
(c) South
(d) North-West

> **Type:** MCQ (GATE-1)
> **Answer:** West (Option b)
> **Solution:** Take clockwise as positive. Starting at 0° (north): 45° anticlockwise gives −45°, which is north-west; 90° clockwise gives −45 + 90 = 45°, which is north-east; 135° anticlockwise gives 45 − 135 = −90°, which is 270° clockwise from north, i.e. **west**.
> **Key point:** Add every turn as a signed number from north; 0° = north, 90° = east, 180° = south, 270° = west.

### Q208. [Section: Data Interpretation] Read the table and answer.

```
Year              2019   2020   2021   2022
Units of A sold    120    150    170    200
Units of B sold    130    145    180    190
```

In which year was the difference between the two products sold the largest, and what was it?

> **Type:** Numerical
> **Answer:** 2022, with a difference of 10 units
> **Solution:** Take A minus B for each year: 2019, 120 − 130 = −10; 2020, 150 − 145 = +5; 2021, 170 − 180 = −10; 2022, 200 − 190 = +10. The largest gap in favour of A is 10 units, in 2022, and that is the only year with a positive gap of that size.
> **Key point:** Compute the requested difference for every column and compare all of them; never pick the year with the biggest single entries.

---

## Section 12. Set L — Final sweep: 25 mixed questions

One question from every topic in the bank. Time yourself: 25 questions should take under 20 minutes.

### Q209. What is 37.5% of 64?

> **Type:** Numerical
> **Answer:** 24
> **Solution:** 37.5% = 3/8, and 64 × 3/8 = 8 × 3 = 24. Equivalently, 12.5% of 64 is 8, and three such parts make 24.
> **Key point:** 37.5% = 3/8, 62.5% = 5/8, 12.5% = 1/8, 6.25% = 1/16 — recognise these so a decimal percentage becomes a one-step division.

### Q210. If 3ˣ = 243, what is the value of 9ˣ?

> **Type:** Numerical
> **Answer:** 59049
> **Solution:** 243 = 3⁵, so x = 5. Then 9ˣ = (3²)⁵ = 3¹⁰ = 59049. Alternatively 9ˣ = (3ˣ)² = 243² = 59049, which avoids finding x at all.
> **Key point:** When both bases are powers of the same prime, 9ˣ = (3ˣ)² — square the given value instead of solving for the exponent.

### Q211. What is the HCF of 108 and 144?

> **Type:** Numerical
> **Answer:** 36
> **Solution:** 108 = 2² × 3³ and 144 = 2⁴ × 3². The HCF uses the lowest common powers: 2² × 3² = 36.
> **Key point:** Prime-factorise both numbers and take the minimum exponent for the HCF and the maximum for the LCM; here the LCM would be 2⁴ × 3³ = 432.

### Q212. An equilateral triangle has a side of 10 cm. What is its area in cm²? (Take √3 = 1.732.)

> **Type:** Numerical
> **Answer:** 25√3 ≈ 43.30 cm²
> **Solution:** Area = (√3/4) × s² = (1.732/4) × 100 = 43.3 cm². The height is 10 × (√3/2) = 8.66 cm, and ½ × 10 × 8.66 = 43.3, confirming it. The trap is 50 cm², obtained by using ½ × base × side.
> **Key point:** Equilateral triangle area = (√3/4)s² and height = (√3/2)s; the height is not the side, which is what produces the 50 cm² trap.

### Q213. In a row of 40 students, 15 study physics, 20 study mathematics and 8 study both. How many study at least one of the two subjects?

> **Type:** Numerical
> **Answer:** 27 students
> **Solution:** Inclusion–exclusion gives 15 + 20 − 8 = 27. The 8 who study both have been counted twice and must be subtracted once.
> **Key point:** "At least one of A and B" = |A| + |B| − |A ∩ B|; "both" = the intersection, "either" is ambiguous and usually means the union.

### Q214. Statement: "Applications must be submitted before 5 p.m. today, as the portal closes at 6 p.m." Which assumption is implicit? I — Late applications are not accepted after 6 p.m. II — The portal is the only route for applying.

(a) Only I
(b) Only II
(c) Both I and II
(d) Neither I nor II

> **Type:** MCQ (GATE-2)
> **Answer:** Only I (Option a)
> **Solution:** The advice to apply before 5 p.m. only makes sense if there is a real deadline at 6 p.m., so I is implicit. Nothing in the statement claims the portal is the sole route; a paper submission could exist, so II is not implicit. In an assumption question, the test is necessity: drop the assumption and see whether the statement collapses.
> **Key point:** The correct assumption is the one that must be true for the advice to make sense, not merely the one that sounds reasonable.

### Q215. Choose the word most nearly opposite in meaning to CANDID.

(a) reticent
(b) outspoken
(c) frank
(d) open

> **Type:** MCQ (GATE-1)
> **Answer:** reticent (Option a)
> **Solution:** Candid means truthful and direct in expression, so its opposite is reticent — reluctant to speak freely. Outspoken, frank and open are all synonyms of candid, which makes three of the four options the trap.
> **Key point:** When three options are synonyms, the odd one out is the antonym; always classify all four options by meaning before choosing.

### Q216. What is the SI unit of power?

> **Type:** Numerical
> **Answer:** The watt (W)
> **Solution:** Power is measured in watts, where 1 W = 1 J/s. The related units are joule for energy, newton for force and ampere for current, and 1 W = 1 V × 1 A.
> **Key point:** Power = energy/time = voltage × current; the watt is defined so that 1 W = 1 V·A, which links three units in one line.

### Q217. How many minutes are there in 2.5 hours?

> **Type:** Numerical
> **Answer:** 150 minutes
> **Solution:** 2.5 × 60 = 150 minutes, that is 2 hours 30 minutes.
> **Key point:** Halves of an hour are 30 minutes each, so any *.5 in an hours figure converts by adding 30.

### Q218. A circle has a circumference of 62.8 cm. Taking π = 3.14, what is its diameter in cm?

> **Type:** Numerical
> **Answer:** 20 cm
> **Solution:** C = πd, so d = C/π = 62.8/3.14 = 20 cm. The division is exact because 3.14 × 20 = 62.8.
> **Key point:** Work with the *diameter* when you have the circumference — C = πd saves finding the radius and doubling it.

### Q219. A man buys 12 pens at ₹18 each and sells them all at ₹25 each. What is his total profit in rupees, and his profit percentage?

> **Type:** Numerical
> **Answer:** ₹84 profit, a profit of 38.89%
> **Solution:** Cost = 12 × 18 = ₹216. Revenue = 12 × 25 = ₹300. Profit = 300 − 216 = ₹84. The profit percentage is 84/216 × 100 = 38.888… ≈ 38.89%. The percentage is measured on the *cost* price, not on the selling price, and not on the number of pens.
> **Key point:** Profit % is always (profit / cost price) × 100; measuring it on the selling price gives 28%, the standard trap.

### Q220. If x + y = 10 and xy = 21, what is the value of x² + y²?

> **Type:** Numerical
> **Answer:** 58
> **Solution:** (x + y)² = x² + 2xy + y², so 100 = x² + y² + 42, giving x² + y² = 58. (The individual values are 3 and 7, and 9 + 49 = 58 confirms it.)
> **Key point:** (x + y)² = x² + y² + 2xy — subtract 2xy to isolate the sum of squares.

### Q221. What is the remainder when 5²⁰²⁴ is divided by 7?

> **Type:** Numerical
> **Answer:** 4
> **Solution:** The powers of 5 modulo 7 cycle with period 6: 5, 4, 6, 2, 3, 1, then repeat (5⁶ = 15,625 = 2232 × 7 + 1). Since 2024 = 6 × 337 + 2, the remainder equals that of 5² = 25, which is 4 modulo 7. Equivalently, by Fermat's theorem 5⁶ ≡ 1 (mod 7), so reduce the exponent to 2.
> **Key point:** Modulo 7 the powers of any number have period dividing 6; cut the exponent to its value mod 6 before computing.

### Q222. A cuboid measures 15 cm × 8 cm × 6 cm. What are its total surface area and its volume?

> **Type:** Numerical
> **Answer:** Total surface area 516 cm²; volume 720 cm³
> **Solution:** TSA = 2(15×8 + 15×6 + 8×6) = 2(120 + 90 + 48) = 2 × 258 = 516 cm². Volume = 15 × 8 × 6 = 720 cm³. Note that TSA of this solid happens to be 720 too, which is a coincidence worth noticing rather than confusing.
> **Key point:** TSA = 2(lw + lh + wh) and volume = lwh; keep the units separate — cm² for the first, cm³ for the second.

### Q223. The following table gives a country's imports for one year, in ₹ crore.

```
Item          Coal   Crude oil   Gold   Electronics
Value           320       480     260         540
```

Which item had the highest value, and what was the share of the four items taken together, to one decimal place?

> **Type:** Numerical
> **Answer:** Electronics, with 33.8% of the total
> **Solution:** The total is 320 + 480 + 260 + 540 = 1600. Electronics at 540 is the largest single value, and its share is 540/1600 × 100 = 33.75 ≈ 33.8%. Crude oil at 480 is the second largest but only 30% of the total.
> **Key point:** In a single-row table, sum for the total first, then take the required fraction; rounding to one decimal place is usually required.

### Q224. A sum of ₹12,000 earns simple interest at 7.5% per annum. What is the interest earned in 3 years?

> **Type:** Numerical
> **Answer:** ₹2,700
> **Solution:** SI = PRT/100 = 12000 × 7.5 × 3/100 = 12000 × 22.5/100 = 2700. As a shortcut, 7.5% of 12,000 is 900 per year, and 3 years gives 2700.
> **Key point:** Simple interest is proportional to time, so compute one year's interest and multiply; 7.5% = 3/40 is easy on 12,000.

### Q225. The present ages of A and B are in the ratio 4 : 5. Five years ago the ratio was 3 : 4. What are their present ages?

> **Type:** Numerical
> **Answer:** A is 20 years old and B is 25 years old
> **Solution:** Let the present ages be 4k and 5k. Five years ago they were 4k − 5 and 5k − 5, and 4k − 5 : 5k − 5 = 3 : 4. Cross-multiplying, 4(4k − 5) = 3(5k − 5), so 16k − 20 = 15k − 15, giving k = 5. Hence A = 20 and B = 25. Check: five years ago they were 15 and 20, and 15 : 20 = 3 : 4.
> **Key point:** For an age ratio that changes, subtract the elapsed time from *both* terms before cross-multiplying — subtracting from only the first breaks the ratio.

### Q226. Choose the word that best fills the blank: "The report was so _____ that even the experts found it difficult to follow."

(a) lucid
(b) convoluted
(c) terse
(d) lucid and brief

> **Type:** MCQ (GATE-2)
> **Answer:** convoluted (Option b)
> **Solution:** "So … that even the experts found it hard to follow" demands a word meaning complicated or hard to follow, which is convoluted. Lucid means clear and is the opposite; terse means brief, which is a different property. Option (d) is a compound trap containing the antonym.
> **Key point:** The "so … that" clause states the *consequence*, and only one option can plausibly produce it; match the consequence, not the topic.

### Q227. Which one of the following expresses the circumference of a circle in terms of its radius r?

(a) πr²
(b) 2πr
(c) πr/2
(d) 4πr

> **Type:** MCQ (GATE-1)
> **Answer:** 2πr (Option b)
> **Solution:** Circumference = 2 × π × r, since a circle of radius r has a diameter of 2r and π × diameter gives the circumference. Option (a) is the *area*, and it is the commonest mix-up in mensuration MCQs.
> **Key point:** For a circle: circumference 2πr, area πr² — the only difference between the two options is whether a factor of 2 r is there.

### Q228. Which is the largest of 2¹⁰, 3⁶ and 10³?

(a) 2¹⁰
(b) 3⁶
(c) 10³
(d) they are all equal

> **Type:** MCQ (GATE-2)
> **Answer:** 2¹⁰ (Option a)
> **Solution:** 2¹⁰ = 1024, 3⁶ = 729 and 10³ = 1000. The largest is 1024, only 24 above 10³ — a deliberate near-tie, so rough estimation is not enough and the values must be computed. Note that 1024 and 1000 are close precisely because 2¹⁰ is the first power of 2 above 1000.
> **Key point:** For "which is largest" options that are close, compute all of them exactly; order-of-magnitude estimates will mislead you here.

### Q229. A triangle has sides 5 cm, 9 cm and 13 cm. What is the median (middle) side?

> **Type:** Numerical
> **Answer:** 9 cm
> **Solution:** Arranging the sides in ascending order gives 5, 9, 13, so the median side is 9 cm. The triangle inequality holds, since 5 + 9 = 14 > 13, so the sides are geometrically valid.
> **Key point:** "Median" here is just the middle value of an ordered list; always check 5 + 9 > 13 before using a triple as a triangle at all.

### Q230. A worker earns ₹480 for 8 hours at a fixed hourly wage. The same worker is paid 1.5 times that wage for each hour of overtime, and works 4 hours of overtime. What is the total earnings in rupees?

> **Type:** Numerical
> **Answer:** ₹840
> **Solution:** The hourly wage is 480/8 = ₹60. The overtime rate is 1.5 × 60 = ₹90 per hour, so 4 hours of overtime earns 4 × 90 = ₹360. Total = 480 + 360 = ₹840.
> **Key point:** Apply the multiplier to the *overtime hours only*; taking 1.5 times the whole day's pay would give 720, the standard trap.

### Q231. The temperature at 6 a.m. is 10 °C and it rises at a constant 2 °C per hour. What is the temperature at 11 a.m.?

> **Type:** Numerical
> **Answer:** 20 °C
> **Solution:** From 6 a.m. to 11 a.m. is 5 hours, so the rise is 5 × 2 = 10 °C, and the temperature is 10 + 10 = 20 °C. Because the rate is constant, the position of the 5-hour span on the clock does not matter.
> **Key point:** For a constant rate, only the *elapsed time* matters — convert clock times to a difference before multiplying.

### Q232. What is the value of sin 30° + cos 60°?

> **Type:** Numerical
> **Answer:** 1
> **Solution:** sin 30° = 1/2 and cos 60° = 1/2, so the sum is 1. The identity behind it is that sin θ = cos(90° − θ), and 60° is the complement of 30°, so the two terms are always equal in a complementary pair.
> **Key point:** The standard values are sin 30° = cos 60° = 1/2, sin 45° = cos 45° = 1/√2, sin 60° = cos 30° = √3/2 — and complementary angles always give equal sines and cosines.

### Q233. The sum of the first eight terms of the sequence 1, 3, 6, 10, 15, 21, 28, 36 is:

> **Type:** Numerical
> **Answer:** 120
> **Solution:** Adding the eight terms: 1 + 3 = 4, + 6 = 10, + 10 = 20, + 15 = 35, + 21 = 56, + 28 = 84, + 36 = 120. These are the triangular numbers, whose n-th term is n(n + 1)/2.
> **Key point:** 1, 3, 6, 10, 15, … are triangular numbers with differences 2, 3, 4, 5; the differences of a sequence are often the fastest way to spot its rule.

---

## Quick revision — Mixed Drills & Previous-Year Patterns

- Relative speed: add for opposite directions, subtract for the same direction — and in overtaking the distance is the gap *plus* the overtaking length.
- Work rates add as fractions of the job per unit time: 1/12 − 1/20 = 1/30. Convert every rate to a common LCM-time before adding.
- Time and work never scale linearly with headcount: if one pipe fills in t, two identical pipes fill in t/2, not t/4.
- Boat speed = mean of downstream and upstream; stream speed = half their difference.
- Never average speeds directly: equal *distances* at two speeds give the harmonic mean, not the arithmetic mean. 40 km at 60 then 40 km at 40 is 48 km/h, not 50.
- Under simple interest time is proportional to interest earned: doubling in 12 years means 5× (4P of interest) in 48 years.
- "Same remainder r on division by each" ⇒ LCM + r. "Same remainder" is not the same question as "greatest number dividing all".
- Trailing zeros of n! = ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + … — do not stop at the first term.
- Units-digit cycles have period at most 4: 2,3,8 → 2,4,8,6 and 3,7 → 3,9,7,1. An exponent that is a multiple of 4 gives units digit 1.
- For a prime modulus p, cut the exponent to its value mod (p − 1) — Fermat's little theorem. 7²⁰²⁴ mod 13 is 7⁸ mod 13 = 3.
- Last two digits means working modulo 100, where the cycle of 3 has period 20; do not use a units-digit cycle for a two-digit question.
- "Neither A nor B" = total − (|A| + |B| − |A ∩ B|). 1000 integers, divisible by neither 2 nor 3, is exactly 333.
- Square divisors of N = ∏ pᵉ: multiply (⌊e/2⌋ + 1) over the primes. For 720 = 2⁴·3²·5 the answer is 6, not 26.
- A digit sum divisible by 3 proves only divisibility by 3. 1326 and 1575 have HCF 3, never 9.
- Mixed recurring decimals: (digits through one repeat − non-repeating part) / (10ⁿ × 99). 0.2 with a bar over 45 is 27/110.
- Percentages of percentages multiply: 40% of 50% of 200 is 40, not 90 and not 20.
- If a number is 1% of 1% of 10,000, the answer is 1 — the cleanest 1-mark item in the bank.
- α² + β² = (α + β)² − 2αβ; α³ + β³ = (α + β)³ − 3αβ(α + β). Both GATE favourites, and both are missed by omitting the correction term.
- (α − β)² = (α + β)² − 4αβ is the route when the *difference* of roots is given.
- For a monic quadratic with constant 1, a root of 1 forces the other root to be 1 as well.
- Multiplying an inequality by a negative reverses it: x ∈ (2, 5) gives −3x ∈ (−15, −6).
- "Neither", "each", "every" and "the number of" take singular verbs; "a number of" takes a plural.
- |y| < a is −a < y < a, while |y| > a is the union of the two outside intervals — reading the symbol wrongly swaps the answer set.
- x + k/x is minimised at x = √k with value 2√k, by AM–GM, and has no maximum.
- Similar figures: length ratio = √(area ratio). A non-square area ratio always signals an error, and area ratio 4 means length ratio 2.
- Radius doubled ⇒ circumference ×2 but area ×4. That single distinction is the most tested point in mensuration MCQs.
- A path of width w inside all four sides of a square field reduces the inner side by 2w, not w — the 60 m field with a 2 m path gives 464 m², not 336 m².
- Ring area = π(R − r)(R + r), never π(R − r)²; the difference of squares taken as a product is the fast route.
- The sphere-to-cylinder identity h = 4r/3 comes from (4/3)πr³ = πr²h; melt-and-recast questions are volume equations with the linear dimension falling out.
- Interior-angle sums: 180°, 360°, 540°, 720° for n = 3, 4, 5, 6. A ratio like 1 : 2 : 3 : 4 is a *quadrilateral*, not a triangle.
- An angle at the centre is twice the inscribed angle on the same arc; the angle between two tangents is 180° minus the central angle.
- Section A is 10 questions in 60 minutes: about 6 minutes each, and that budget is better spent on the four quant MCQs and the DI question than on a hard reasoning item.
- Attack order that works: DI and quant MCQs first, then verbal 1-marks, then syllogisms and direction sense last, marking two for review instead of burning 10 minutes on one question.
