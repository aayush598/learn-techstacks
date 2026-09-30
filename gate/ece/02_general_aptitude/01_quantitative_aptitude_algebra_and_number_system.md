# General Aptitude — Part 1: Quantitative Aptitude, Algebra & Number System

> Part 1 of 5 of the GATE ECE General Aptitude question bank · Questions Q1–Q232 of this file
> Read this file top to bottom, in order. It is followed by
> `02_geometry_and_mensuration.md`, `03_data_interpretation_and_logical_reasoning.md`,
> `04_verbal_ability_and_comprehension.md` and `05_mixed_timed_drills.md`.

**What this file is.** This is the whole of "quantitative aptitude" in the GATE General
Aptitude paper: commercial arithmetic (percentage, profit–loss, ratio, mixture, average), rate
problems (time–work, pipes, speed, trains, boats), the number system (divisibility, HCF/LCM,
prime factorisation, base and modular arithmetic), counting, probability, and the GATE-style
data-sufficiency sets that tie them together. The four following parts are named above so the
boundary is explicit: **Part 2 Geometry & Mensuration**, **Part 3 Data Interpretation &
Logical Reasoning**, **Part 4 Verbal Ability & Comprehension**, **Part 5 Mixed Timed Drills**.
Nothing here touches them — no area or volume of triangles, circles and solids, no syllogisms
or seating arrangements, no reading passages, and no timed answer sheets.

**Covers:** percentages, profit–loss, discount, markup and successive percentage change;
ratio and proportion, mixtures and the alligation rule; averages, weighted averages and
combined averages from a split group; time–work, efficiency and pipes/cisterns;
time–speed–distance with trains, boats, streams and relative speed; divisibility, remainders,
HCF/LCM, factors, prime factorisation and base conversion; modular arithmetic and last-digit
and last-two-digit problems; arithmetic, geometric, Fibonacci-like and mixed series;
permutations, combinations, circular arrangements and distinguishable objects; probability,
odds, dice and cards; sets, relations, functions and the pigeonhole principle; and
quantitative reasoning with data-sufficiency statement sets.

**Assumes:** school arithmetic only — fractions, decimals, percentage, ratio, prime factors of
small integers, and the ability to evaluate a small power or square root by hand. No prior
notes are needed. Every rule is written out inside the solution the first time it is used, and
every numeric answer is either exact or marked `≈` to two decimal places.

**Volume:** 232 questions across 12 sections, followed by a 32-bullet quick-revision block.
Roughly 20% definition/short-rule recall, 30% quick formula application, 25% medium multi-step
problems, 15% GATE 1-mark MCQs (tagged `GATE-1`) and 10% GATE 2-mark MCQs (tagged `GATE-2`).

---

## Section 1. Percentages, profit–loss, discount, markup and successive percentage change

### Q1. A trader marks an article 25% above its cost price and then allows a discount of 10% on the marked price. If the cost price is ₹640, what is the selling price, and what is his gain percentage?

> **Type:** Numerical
> **Answer:** Selling price ₹720; gain 12.5% (both exact).
> **Solution:** Marked price = 640 × 1.25 = ₹800. The customer pays 90% of that, so the selling price is 800 × 0.9 = ₹720. The gain is 720 − 640 = ₹80, and 80 / 640 = 12.5%. The 25% markup and the 10% discount do not cancel because they are taken on *different* bases — the markup on the cost price, the discount on the marked price.
> **Key point:** Net SP/CP = (1 + markup) × (1 − discount); here 1.25 × 0.9 = 1.125.

### Q2. The marked price of an article is ₹2,500 and two successive discounts of 15% and 10% are allowed. Find the final selling price and the single discount percentage equivalent to both.

> **Type:** Numerical
> **Answer:** Selling price ₹1,912.50; equivalent single discount 23.5% (both exact).
> **Solution:** 2500 × 0.85 = 2125, and 2125 × 0.9 = ₹1,912.50. The overall retained fraction is 0.85 × 0.9 = 0.765, so the overall discount is 1 − 0.765 = 0.235 = 23.5%. Note that 15% + 10% = 25% is wrong: the correct figure is 15 + 10 − (15 × 10)/100 = 23.5.
> **Key point:** Successive discounts are not additive: d_total = d₁ + d₂ − d₁d₂/100 = 23.5%.

### Q3. An article bought for ₹1,360 is sold at a profit of 25%. Find the selling price, and then find what the cost price would have been if that same selling price represented a 20% loss instead.

> **Type:** Numerical
> **Answer:** Selling price ₹1,700; the cost price in the second case would be ₹2,125 (both exact).
> **Solution:** 1360 × 1.25 = ₹1,700. If instead 1.20 × CP = 1700, then CP = 1700 / 1.2 = ₹2,125. The same selling price corresponds to wildly different cost prices depending on whether it is measured above or below the base, so always solve for whichever quantity is unknown.
> **Key point:** Profit gives SP = 1.25·CP; loss gives SP = 0.8·CP — invert, never add.

### Q4. A trader sells an article at a profit of 30%. Had the selling price been ₹91 lower, his profit would have been 20% only. Find the cost price.

> **Type:** Numerical
> **Answer:** ₹910 (exact).
> **Solution:** Let the cost price be c. Then 1.3c − 91 = 1.2c, so 0.1c = 91 and c = ₹910. Check: 1.3 × 910 = 1183; 1183 − 91 = 1092 = 1.2 × 910 ✓. The general pattern is that a fixed rupee gap g between two profit percentages p₁ and p₂ gives c = g / ((p₁ − p₂)/100).
> **Key point:** A rupee difference between two CP-percentages gives c = 100g/(p₁ − p₂).

### Q5. A number is increased by 30% and the result is then decreased by 30%. What is the net change, and why is it not zero?

> **Type:** Numerical
> **Answer:** A net decrease of 9% (exact).
> **Solution:** Take the number as 100. It becomes 130, and then 130 × 0.7 = 91. The loss is 9% of the original. The 30% decrease is applied to 130, not to 100, so the two operations are not inverses. In general, +x% followed by −x% gives a net change of −x²/100 %, which here is −900/100 = −9%.
> **Key point:** +x% then −x% nets −x²/100 %; the operations are inverses only if x = 0.

### Q6. By what percent must the number 400 be increased to become 520, and by what percent must 520 be decreased to return to 400?

> **Type:** Comparison
> **Answer:** Increase of 30%; decrease of 23.08% (≈ 30/130).
> **Solution:** The rise is 120 on a base of 400, so 120/400 = 30%. The fall is 120 on a base of 520, so 120/520 = 0.23077 = 23.08%. The two percentages differ because the base differs, which is precisely the asymmetry described in Q5.
> **Key point:** The same absolute change is a smaller percentage of the larger number.

### Q7. A man sells two articles for the same selling price. On one he gains 20% and on the other he loses 20%. What is his overall gain or loss percentage?

> **Type:** Numerical
> **Answer:** An overall loss of 4% (exactly 1/25).
> **Solution:** Let each selling price be 100. Then the costs are 100/1.2 = 83.33 and 100/0.8 = 125, totalling 208.33 against a total selling price of 200. The loss is 8.33, and 8.33 / 208.33 = 1/25 = 4%. The closed form is: with equal selling prices s and rates +x% and −x%, the loss percentage is always exactly x²/100 %.
> **Key point:** "Same SP, +x% and −x%" always loses exactly x²/100 %.

### Q8. A dishonest dealer claims to sell at cost price but uses a weight of 800 g in place of 1 kg. If the true cost of a kilogram is ₹120, what is his gain percentage?

> **Type:** Numerical
> **Answer:** 25% (exact).
> **Solution:** He charges the cost of 1 kg, ₹120, but hands over only 800 g, which really costs 120 × 0.8 = ₹96. His gain is 120 − 96 = ₹24 on an actual outlay of ₹96, so 24/96 = 25%. In general a false weight of w grams instead of 1000 gives a gain of (1000 − w)/w × 100 %, not (1000 − w) %.
> **Key point:** False weight of w g in place of 1 kg gives gain (1000 − w)/w × 100 %.

### Q9. Two successive discounts of 20% and 25% are offered on a marked price. What single discount percentage is equivalent?

> **Type:** MCQ `GATE-1`
> **Answer:** 40% [a]
>
> (a) 40%
> (b) 45%
> (c) 35%
> (d) 42.5%
>
> **Solution:** The customer retains 0.80 × 0.75 = 0.60 of the marked price, so the equivalent discount is 1 − 0.60 = 40% ✓. The general formula confirms it: d₁ + d₂ − d₁d₂/100 = 20 + 25 − (20 × 25)/100 = 45 − 5 = 40. Option (b) 45% is the trap of simply adding the two discounts, which ignores that each is applied to a successively reduced price.
> **Key point:** Equivalently, x% then y% off gives a total of (x + y − xy/100) % = 40%.

### Q10. A shopkeeper buys an article for ₹1,250, marks it 60% above the cost price and allows a discount of ₹250. Find his profit or loss percentage.

> **Type:** Numerical
> **Answer:** 40% profit (exact).
> **Solution:** Marked price = 1250 × 1.6 = ₹2,000, so the selling price is 2000 − 250 = ₹1,750. The profit is 1750 − 1250 = ₹500, and 500 / 1250 = 40%. The rupee discount removes 250/2000 = 12.5% of the marked price, but since the markup was 60% the net multiplier is 1.6 × 0.875 = 1.40.
> **Key point:** A fixed-rupee discount must be converted to a percentage of the marked price before combining.

### Q11. A quantity is first increased by 20% and then decreased by x%. The net result is a 2% decrease. Find x.

> **Type:** Numerical
> **Answer:** x = 18.33% (≈ 55/3 %).
> **Solution:** 1.20 × (1 − x/100) = 0.98, so 1 − x/100 = 0.98 / 1.2 = 0.816667, giving x/100 = 0.183333 and x = 18.33%. Note that x is *less* than 20% because the 20% increase first made the base larger, so a slightly smaller cut is needed to return to 0.98 of the original.
> **Key point:** To undo a net factor, divide by the first multiplier: 0.98 / 1.2.

### Q12. A student scores 60 marks in two subjects and 80 marks in a third. If the subjects carry weights in the ratio 2 : 2 : 1, find the weighted average.

> **Type:** Numerical
> **Answer:** 64 marks (exact).
> **Solution:** Weighted score = 60×2 + 60×2 + 80×1 = 320, and the total weight is 5, so the weighted average is 320/5 = 64. A plain average would give (60+60+80)/3 = 66.67, which over-weights the single high-scoring subject — the whole point of weighting.
> **Key point:** Weighted average = Σ(mark × weight) / Σ(weight); weights, not counts, decide influence.

### Q13. The population of a town increases by 25% in the first year and then decreases by 20% in the second year. What is the net change over the two years?

> **Type:** Numerical
> **Answer:** No net change (exactly 0%).
> **Solution:** Take the population as 100. After year one it is 125, and after year two it is 125 × 0.8 = 100. The chain multiplier is 1.25 × 0.8 = 1.00. This is not a coincidence: a rise of 25% is exactly undone by a fall of 25/125 = 20%, because the fall is measured on the enlarged base.
> **Key point:** A rise of p% is undone by a fall of 100p/(100+p) %; for p = 25 that is 20%.

### Q14. A shopkeeper offers "buy 3, get 1 free" on an article priced at ₹480. What is the effective discount per unit, and what would the price per unit be?

> **Type:** Numerical
> **Answer:** Effective discount 25%; effective price per unit ₹360.
> **Solution:** For four units the customer pays for three, so the cost is 3 × 480 = ₹1,440 instead of 4 × 480 = ₹1,920. The saving is 480 on 1920, i.e. 25%, and the effective unit price is 1440/4 = ₹360. Buy-one-get-one-free would have been exactly 50%; "3 get 1 free" is weaker because the free unit is only one of four.
> **Key point:** "Buy m get n free" gives an effective discount of n/(m+n) only when the free items are identical in value.

### Q15. An article is marked 25% above the cost price and the shopkeeper allows two successive discounts of 20% and 10%. What is his overall gain or loss percentage?

> **Type:** MCQ `GATE-1`
> **Answer:** A loss of 10% [d]
>
> (a) A gain of 10%
> (b) A gain of 2.5%
> (c) A loss of 2.5%
> (d) A loss of 10%
>
> **Solution:** Take the cost price as 100, so the marked price is 125. The two successive discounts leave 125 × 0.80 × 0.90 = 90, so the selling price is 90 against a cost of 100 — a loss of 10% ✓. Option (b) 2.5% is the trap of assuming the 25% markup and the two discounts partly cancel, and option (c) comes from adding 20% + 10% = 30% and subtracting it from 25%.
> **Key point:** Reduce everything to a single multiplier on the cost price: 1.25 × 0.8 × 0.9 = 0.90, a 10% loss.

### Q16. A trader gains 25% by selling an article for ₹1,300. What was the cost price, and what would the selling price be if he had sold it at a 20% loss on that same cost price?

> **Type:** Numerical
> **Answer:** Cost price ₹1,040; loss-price selling price ₹832 (both exact).
> **Solution:** 1.25 × CP = 1300, so CP = 1300 / 1.25 = ₹1,040. At a 20% loss the selling price is 1040 × 0.8 = ₹832. The two selling prices differ by a factor of 1300/832 = 1.5625, which is 1.25/0.8 — the ratio of the two multipliers.
> **Key point:** Same cost price, two different multipliers: 1.25 vs 0.80.

### Q17. A dealer buys a machine for ₹40,000 and installs it at a further cost of ₹4,000. He then sells it for ₹53,200. Find (a) the total cost price and (b) the profit percentage on the total cost.

> **Type:** Numerical
> **Answer:** Total cost price ₹44,000; profit ≈ 20.91% (exact value 9,200/44,000 = 23/110).
> **Solution:** Installation is a genuine cost of acquiring the machine, so the total cost price is 40,000 + 4,000 = ₹44,000. The profit is 53,200 − 44,000 = ₹9,200, and 9,200 / 44,000 = 23/110 ≈ 0.2091, i.e. 20.91% ✓. Computing the profit on the purchase price alone would give 9,200/40,000 = 23%, which overstates the margin because it ignores the installation cost.
> **Key point:** Freight, installation and repair all belong in the cost price before taking a percentage.

### Q18. A number is increased by 10% and the result is increased by 10% again. By what single percentage was the original number increased overall?

> **Type:** Numerical
> **Answer:** 21% (exact).
> **Solution:** Taking the original as 100, the first increase gives 110 and the second gives 110 × 1.1 = 121. The overall increase is therefore 21 out of the original 100, i.e. 21% ✓. Note that the base for the overall change is the *original* value; measuring the shortfall against the final value instead would give the different figure 21/121 ≈ 17.36%.
> **Key point:** Successive increases of x% and y% give an overall (x + y + xy/100) % = 10 + 10 + 1 = 21% rise, measured against the original.

### Q19. An article is marked 33⅓% above the cost price, and the shopkeeper allows a 33⅓% discount on the marked price. What is his gain or loss percentage?

> **Type:** Common-mistake
> **Answer:** A loss of 11.11% (exactly 1/9, i.e. 11.111…%).
> **Solution:** Write 33⅓% as 1/3 and take the cost price as 90, so the marked price is 120. The discount of 1/3 of 120 is 40, leaving a selling price of 80. The loss is 90 − 80 = 10, which is 10/90 = 1/9 ≈ 11.11% ✓. The trap is assuming a 33⅓% markup and a 33⅓% discount cancel, which fails because the discount is applied to the marked price rather than the cost price.
> **Key point:** Identical percentages on different bases do not cancel: (4/3) × (2/3) = 8/9, a loss of 1/9.

### Q20. A shopkeeper's profit is 33⅓% of his selling price. What is his gain percentage on the cost price?

> **Type:** Numerical
> **Answer:** 50% (exact).
> **Solution:** Let SP = 100. The profit is 33⅓% of 100, i.e. 100/3, so CP = 100 − 100/3 = 200/3 = ₹66.67. The gain on cost = (100/3) / (200/3) = 1/2 = 50%. The same rupee profit is 33.33% of the selling price but 50% of the cost price. The general rule is that a gain of g% on SP equals a gain of 100g/(100 − g) % on CP, which here is 3333.33/66.67 = 50.
> **Key point:** A gain of g% on SP is a gain of 100g/(100 − g) % on CP.

### Q21. A shopkeeper marks an article 40% above the cost price and then allows a discount of 40%. What is his gain or loss? Now consider the alternative of marking 30% above cost and allowing a 30% discount.

> **Type:** Comparison
> **Answer:** A loss of 16% in the first case and a loss of 9% in the second case (both exact).
> **Solution:** The net multiplier is (1 + d)(1 − d) = 1 − d², so the loss is exactly d². For d = 0.4 the multiplier is 0.84, a 16% loss; for d = 0.3 it is 0.91, a 9% loss. The larger the matched pair, the larger the loss, which is why the smaller matched pair is the better deal for the customer. The trap is to assume the markup and discount cancel, giving zero.
> **Key point:** Matched markup m% and discount m% always give a loss of exactly m²/100 % of cost.

### Q22. A dealer marks an article 33% above the cost price in order to give a discount of 8%. What is his gain percentage?

> **Type:** Numerical
> **Answer:** A gain of 22.36% (exact to two decimals).
> **Solution:** The net multiplier is 1.33 × 0.92 = 1.2236, so the gain is 22.36%. Since 33% is close to 1/3, the approximation 4/3 × 0.92 = 1.2267 (22.67%) is a common but inexact substitute; using 1.33 rather than 4/3 keeps the answer exact.
> **Key point:** Multiply the two multipliers to four decimal places, then subtract 1.

### Q23. Two successive percentage changes take a value of ₹500 to ₹605, and the first of them is a 20% increase. What is the second percentage change?

> **Type:** Numerical
> **Answer:** An increase of ≈ 0.83% (exactly 1/120 of the intermediate value).
> **Solution:** After the 20% increase, ₹500 becomes 500 × 1.2 = ₹600. The final value is ₹605, so the second change takes 600 to 605, an increase of 5/600 = 1/120 ≈ 0.83% ✓. In multiplier form the total is 605/500 = 1.21, and dividing by the known first factor gives 1.21 / 1.20 = 1.00833…, confirming the 0.83% rise. Successive changes are never added or subtracted directly, because each is applied to a different base.
> **Key point:** Find one factor from a product by dividing: 1.21 / 1.20 = 1.00833, i.e. a 0.83% increase.

### Q24. Divide ₹1,440 in the ratio 5 : 7 : 4. What are the three shares, and what is the ratio of the smallest share to the largest?

> **Type:** Numerical
> **Answer:** ₹450, ₹630 and ₹360 respectively; smallest : largest = 4 : 7.
> **Solution:** The ratio has 5 + 7 + 4 = 16 parts, so one part is 1440/16 = ₹90. The shares are 5 × 90 = ₹450, 7 × 90 = ₹630 and 4 × 90 = ₹360, and they sum to 1,440 ✓. The smallest share is ₹360 and the largest is ₹630, so the ratio of smallest to largest is 4 : 7 — already in lowest terms, since 4 and 7 are coprime ✓.
> **Key point:** One part = total ÷ sum of ratio terms = 90; the smallest-to-largest ratio just reorders the original parts 4 : 7.

### Q25. The ratio of the number of boys to the number of girls in a school is 5 : 8 and there are 260 students in all. How many boys are there?

> **Type:** Numerical
> **Answer:** 100 boys (exact).
> **Solution:** 5 + 8 = 13 parts cover 260 students, so one part is 260/13 = 20. Boys = 5 × 20 = 100 and girls = 8 × 20 = 160; 100 + 160 = 260 ✓. A frequent error is to use 5 as the divisor and get 52 boys, which ignores the second term of the ratio.
> **Key point:** The unit is total ÷ (sum of all ratio terms), not total ÷ the term you want.

### Q26. The ratio of A to B is 4 : 7. If 12 is added to A and 15 is subtracted from B, the two become equal. Find A and B.

> **Type:** Numerical
> **Answer:** A = 36 and B = 63 (exact).
> **Solution:** Write A = 4k and B = 7k. The condition gives 4k + 12 = 7k − 15, so 27 = 3k and k = 9. Hence A = 36 and B = 63. Check: 36 + 12 = 48 and 63 − 15 = 48 ✓. The ratio 36 : 63 reduces by 9 to 4 : 7, as required.
> **Key point:** Introduce a single unknown k, apply the offsets with the correct signs, then verify the new values are equal.

### Q27. Two numbers are in the ratio 3 : 5 and their difference is 14. Find the numbers.

> **Type:** Numerical
> **Answer:** 21 and 35 (exact).
> **Solution:** The two parts differ by 5 − 3 = 2, and that gap corresponds to 14. So one part is 14/2 = 7, giving 3×7 = 21 and 5×7 = 35; 35 − 21 = 14 ✓. The method is: divide the given difference by the *difference of the ratio terms*.
> **Key point:** For a "difference given" problem, part = difference ÷ (difference of ratio terms).

### Q28. A bag contains red and blue balls in the ratio 3 : 5. If 12 red balls are added, the ratio becomes 1 : 1. How many blue balls were originally there?

> **Type:** Numerical
> **Answer:** 30 blue balls (exact).
> **Solution:** Let red = 3k and blue = 5k. Adding 12 red balls makes red equal to blue, so 3k + 12 = 5k, giving 2k = 12 and k = 6. Red = 18, blue = 30, and 18 + 12 = 30 ✓.
> **Key point:** Additions and removals must be expressed in the same "k units" before solving.

### Q29. In a mixture of 45 litres of milk and water, the ratio of milk to water is 7 : 2. How much water must be added to change the ratio to 7 : 3?

> **Type:** Numerical
> **Answer:** 5 litres (exact).
> **Solution:** 45 L splits into 9 parts, so one part is 5 L: milk = 35 L, water = 10 L. The milk is not disturbed by adding water, so the new water must be 35/7 × 3 = 15 L, i.e. 5 L must be added. Check: 35 : (10 + 5) = 35 : 15 = 7 : 3 ✓.
> **Key point:** Adding water leaves the milk fixed; solve the new ratio for the water alone.

### Q30. How many kilograms of a 40% salt solution must be mixed with 60 kg of a 15% salt solution to obtain a 25% solution?

> **Type:** Numerical
> **Answer:** 40 kg (exact).
> **Solution:** Let x kg of the 40% solution be used and set salt in = salt out: 0.40x + 0.15 × 60 = 0.25(x + 60). This gives 0.40x + 9 = 0.25x + 15, so 0.15x = 6 and x = 40. Check: salt = 0.40(40) + 0.15(60) = 16 + 9 = 25 kg in 100 kg of mixture = 25% ✓.
> **Key point:** One equation, one unknown: 0.40x + 0.15(60) = 0.25(x + 60).

### Q31. In what ratio must milk costing ₹60 per litre be mixed with water costing ₹0 per litre to obtain a mixture worth ₹45 per litre?

> **Type:** Numerical
> **Answer:** Milk : water = 3 : 1.
> **Solution:** Take 100 L of mixture, worth 100 × 45 = ₹4,500. Only the milk carries value, so the milk must be 4500 / 60 = 75 L and the water 25 L, giving 75 : 25 = 3 : 1. Alligation gives the same answer: cheaper : dearer = (dearer − mean) : (mean − cheaper) = (60 − 45) : (45 − 0) = 15 : 45 = 1 : 3, i.e. 3 parts milk to 1 part water.
> **Key point:** Alligation: cheaper : dearer = (dearer − mean) : (mean − cheaper).

### Q32. A milkman mixes 40 litres of milk costing ₹40 per litre with 60 litres of milk costing ₹60 per litre. What is the price of the mixture per litre, and how would it change if the quantities were reversed?

> **Type:** Comparison
> **Answer:** ₹52 per litre in both cases — the order of mixing has no effect.
> **Solution:** (40 × 40 + 60 × 60)/100 = (1600 + 3600)/100 = ₹52. Reversed: (60 × 40 + 40 × 60)/100 = (2400 + 2400)/100 = ₹52. The weighted mean is symmetric in the two quantities, so swapping the amounts between the two prices cannot change the result.
> **Key point:** A two-component weighted mean is symmetric; "cheap with dear" and "dear with cheap" both give the same mean.

### Q33. In what ratio must rice costing ₹30 per kg be mixed with rice costing ₹45 per kg so that the mixture is worth ₹40 per kg? What mixture would the fixed amounts 20 kg and 30 kg actually produce?

> **Type:** Numerical
> **Answer:** The required ratio of the ₹30 rice to the ₹45 rice is 1 : 2; the fixed amounts 20 kg and 30 kg produce a mixture worth ₹39 per kg.
> **Solution:** Alligation gives cheaper : dearer = (45 − 40) : (40 − 30) = 5 : 10 = 1 : 2. Verification: (1 × 30 + 2 × 45)/3 = 120/3 = ₹40 ✓. But the amounts on hand, 20 kg and 30 kg, are in the ratio 2 : 3, which yields (2 × 30 + 3 × 45)/5 = (60 + 135)/5 = 195/5 = ₹39. So the stated inventory cannot produce the ₹40 target.
> **Key point:** Alligation gives cheaper : dearer = (dearer − mean) : (mean − cheaper); always re-verify against the quantities actually available.

### Q34. A solution of 40 litres contains acid and water in the ratio 3 : 17. If 8 litres of water is added, what is the new ratio of acid to water?

> **Type:** Numerical
> **Answer:** 1 : 7 (exact).
> **Solution:** 40 L splits into 20 parts, so one part is 2 L: acid = 6 L, water = 34 L. Adding 8 L of water gives 34 + 8 = 42 L of water while the acid stays at 6 L. The new ratio is 6 : 42, which reduces to 1 : 7. The acid coefficient falls from 3 to 1 while the water coefficient rises from 17 to 21, because the ratio is rebuilt from the new actual quantities.
> **Key point:** After adding one component, recompute the ratio from actual quantities — do not rescale the old coefficients.

### Q35. A mixture of 45 kg contains 20% water. How much water must be evaporated to leave 40 kg of mixture, and what percentage of water is in the result?

> **Type:** Numerical
> **Answer:** Evaporate 5 kg of water; the result is 10% water (exact).
> **Solution:** Water = 0.20 × 45 = 9 kg and milk = 45 − 9 = 36 kg. To leave 40 kg, exactly 5 kg must evaporate, and since only water evaporates the water left is 9 − 5 = 4 kg. Check: 4/40 = 10% and the milk is unchanged at 36/40 = 90% ✓. Because only one component evaporates, the milk fraction rises from 80% to 90%.
> **Key point:** When water evaporates the milk is fixed at 36 kg, so the new total fixes the new percentage directly.

### Q36. In a group of 60 students, 35 study Mathematics and 25 study Physics, and every student studies at least one of the two. How many study both?

> **Type:** Numerical
> **Answer:** 0 students (exact).
> **Solution:** By inclusion–exclusion, both = 35 + 25 − 60 = 0. Since 35 + 25 = 60 equals the group size and no one studies neither, the two sets are disjoint. The trap is to assume that a positive overlap must exist simply because both subjects are popular.
> **Key point:** |A ∩ B| = |A| + |B| − |A ∪ B|; if the sum equals the union, the sets are disjoint.

### Q37. Two grades of fertilizer are mixed in the ratio 3 : 5. The first contains 20% nitrogen and the second 50%. What nitrogen percentage does the mixture have, and what ratio would give exactly 40%?

> **Type:** Numerical
> **Answer:** The 3 : 5 mixture has 38.75% nitrogen; the ratio for exactly 40% is 1 : 2.
> **Solution:** In 3 : 5 take 60 kg and 100 kg. Nitrogen = 0.20(60) + 0.50(100) = 12 + 50 = 62 kg in 160 kg, i.e. 62/160 = 38.75%. For a true 40%, alligation gives cheaper : dearer = (50 − 40) : (40 − 20) = 10 : 20 = 1 : 2, verified by (1 × 20 + 2 × 50)/3 = 120/3 = 40 ✓.
> **Key point:** Confirm any claimed ratio with a direct nutrient balance: 0.20(60) + 0.50(100) = 62 kg in 160 kg = 38.75%.

### Q38. A shopkeeper mixes two qualities of rice in the ratio 2 : 3 and sells the mixture at ₹45 per kg, making a profit of 25% over the total cost. If the cheaper rice costs ₹30 per kg, what does the costlier rice cost per kg?

> **Type:** Numerical
> **Answer:** ₹40 per kg (exact).
> **Solution:** A 25% profit on cost means the mixture costs 45 / 1.25 = ₹36 per kg. With the ratio 2 : 3 and the cheaper price at ₹30, let the costlier price be p: (2 × 30 + 3p)/5 = 36, so 60 + 3p = 180 and 3p = 120, giving p = ₹40. Check: (60 + 120)/5 = ₹36, and 36 × 1.25 = ₹45 ✓.
> **Key point:** Remove the profit first (mixture cost = SP / 1.25), then use the ratio to recover the unknown price.

### Q39. A dealer mixes 30 kg of one grade of cement with 70 kg of another and sells it at a profit of 20% over the total cost. If the total cost is ₹5,000, what is the cost per kg of the mixture, and what is its selling price per kg?

> **Type:** Numerical
> **Answer:** Cost ₹50 per kg; selling price ₹60 per kg (both exact).
> **Solution:** Total weight is 100 kg and total cost ₹5,000, so the cost per kg is 5000/100 = ₹50. A 20% profit gives 50 × 1.2 = ₹60 per kg. The 30 : 70 split is irrelevant to this particular question — it matters only when the two grades have different prices, which is a useful check that you have identified what the data actually determines.
> **Key point:** Total cost ÷ total weight gives the mixture cost per kg; splits are irrelevant unless prices differ.

### Q40. On a map, 1 cm represents 25 km. Two towns are 13.5 cm apart on the map. What is their actual distance, and what would the map distance be if the scale were 1 cm to 50 km?

> **Type:** Numerical
> **Answer:** 337.5 km; 6.75 cm at the 1 cm : 50 km scale.
> **Solution:** At 1 cm : 25 km the actual distance is 13.5 × 25 = 337.5 km. At 1 cm : 50 km the same real distance needs 337.5 / 50 = 6.75 cm. Halving the scale denominator doubles the map distance required, which is why 6.75 cm is exactly half of 13.5 cm.
> **Key point:** Real distance = map distance × scale; halving the scale denominator doubles the map distance needed.

### Q41. Two quantities are in the ratio 5 : 7 and their product is 2,835. Find the quantities.

> **Type:** MCQ `GATE-1`
> **Answer:** 45 and 63 [c]
>
> (a) 35 and 49
> (b) 40 and 56
> (c) 45 and 63
> (d) 50 and 70
>
> **Solution:** Write the numbers as 5k and 7k. Then 35k² = 2,835, so k² = 81 and k = 9. The quantities are 5 × 9 = 45 and 7 × 9 = 63 ✓. The ratio alone is not enough — every option satisfies 5 : 7 — so the product is what selects the scale, and only option (c) gives 45 × 63 = 2,835 while the others give 1,715, 2,240 and 3,500.
> **Key point:** A ratio fixes only the shape; the product fixes the scale, giving k = √(2835/35) = 9.

### Q42. Fifteen workers can build a wall in 20 days. How many workers are needed to build the same wall in 15 days, assuming all workers work at the same constant rate?

> **Type:** Numerical
> **Answer:** 20 workers (exact).
> **Solution:** The total work is 15 × 20 = 300 worker-days. To finish in 15 days, the number of workers n must satisfy 15n = 300, so n = 20. This is an inverse proportion: workers and time vary inversely as their product stays fixed.
> **Key point:** For constant-rate work, workers × days is invariant; n₁d₁ = n₂d₂.

### Q43. A and B invest in a business in the ratio 3 : 5 and the annual profit is ₹16,000. If A additionally receives a fixed salary of ₹2,000 out of that profit, what are A's and B's shares of the total profit?

> **Type:** Numerical
> **Answer:** A receives ₹7,250 and B receives ₹8,750 (both exact).
> **Solution:** The salary is taken out first, leaving 16,000 − 2,000 = ₹14,000 to be shared in the ratio 3 : 5. That is 8 parts of 14,000/8 = ₹1,750, so the ratio shares are 3 × 1750 = ₹5,250 and 5 × 1750 = ₹8,750. Adding A's salary back gives 5,250 + 2,000 = ₹7,250 for A, and B receives ₹8,750. The two shares sum to 16,000 ✓.
> **Key point:** Deduct a fixed salary *before* applying the ratio; the ratio then acts on the remainder only.

---

## Section 3. Averages, weighted averages and combined averages from a split group

### Q44. The average of 8 numbers is 15. If one of the numbers, 23, is replaced by 5, what is the new average?

> **Type:** Numerical
> **Answer:** 12.75 (exact).
> **Solution:** The original sum is 8 × 15 = 120. Replacing 23 by 5 lowers the sum by 18, giving 102, and 102 / 8 = 12.75. The general form is: new average = old average + (new value − old value) / count.
> **Key point:** Only the changed value matters: Δavg = (new − old)/count.

### Q45. The average age of 30 students is 12 years. When the teacher's age of 45 years is included, what is the average age of all 31 persons?

> **Type:** Numerical
> **Answer:** ≈13.06 years (405/31).
> **Solution:** Total age of students = 30 × 12 = 360, plus 45 gives 405, over 31 people: 405 / 31 = 13.0645. Note the average rose by more than the naive (12 + 45)/2 = 28.5 would suggest, because 45 is compared against a much larger block of 12-year-olds.
> **Key point:** Combined average = (Σ of each group) / (total count) — never the average of the averages unless the groups are equal in size.

### Q46. A student scores 70, 80 and 90 in three subjects with weights 2, 3 and 4. What is the weighted average?

> **Type:** Numerical
> **Answer:** 82.22 (≈ 740/9).
> **Solution:** Weighted sum = 2(70) + 3(80) + 4(90) = 140 + 240 + 360 = 740, and total weight = 9, giving 740/9 = 82.22. A plain average would be 80, and the weighted average is higher because the heaviest weight multiplies the highest score.
> **Key point:** Weighted average = Σ(weight × value) / Σ(weight); here 740/9.

### Q47. A class of 40 students has an average mark of 60. If 10 more students with an average of 75 join, what is the new average?

> **Type:** Numerical
> **Answer:** 63 (exact).
> **Solution:** Original total = 40 × 60 = 2,400; the newcomers contribute 10 × 75 = 750, so the new total is 3,150 over 50 students: 3150/50 = 63. The result lies between 60 and 75 but is much closer to 60 because the new group is a quarter of the class.
> **Key point:** The combined average is pulled toward the larger group; weight by headcount, not equally.

### Q48. The average of the first 10 terms of a sequence is 12, and the average of the first 20 terms is 15. What is the average of terms 11 to 20?

> **Type:** Numerical
> **Answer:** 18 (exact).
> **Solution:** Sum of the first 10 = 120; sum of the first 20 = 300, so terms 11 to 20 sum to 300 − 120 = 180 over 10 terms, giving 18. The trap is to report 15, which is the average of the *first* 20 and says nothing about the last block.
> **Key point:** Averages of blocks must be converted to sums before subtracting: S₂₀ − S₁₀ = 180.

### Q49. Five consecutive odd numbers have an average of 37. What are the numbers, and what is their sum?

> **Type:** Numerical
> **Answer:** 33, 35, 37, 39, 41; sum 185.
> **Solution:** For an odd number of consecutive values the mean is the middle value, so the middle term is 37 and the terms run 37 − 4 = 33 up to 37 + 4 = 41. The sum is 5 × 37 = 185. The reason the mean is the centre term is that the values are symmetric about it.
> **Key point:** For consecutive integers (or APs) the mean of an odd count equals the middle term.

### Q50. A student's average over 5 tests is 80. In the 6th test he scores 92. What is his average over 6 tests?

> **Type:** MCQ `GATE-1`
> **Answer:** 82 [b]
>
> (a) 84.4
> (b) 82
> (c) 86
> (d) 80.8
>
> **Solution:** The total over 5 tests is 5 × 80 = 400, and adding 92 gives 492 over 6 tests, so the new average is 492 / 6 = 82 exactly ✓. Option (c) 86 is the trap of taking the simple mean of the two averages, (80 + 92)/2, which is wrong because the 80 represents 5 tests and the 92 only one; option (d) 80.8 comes from adding 92/5 to 80.
> **Key point:** New average = (old total + new score)/(old count + 1) = 492/6 = 82, never the mean of the two averages.

### Q51. The average of 6 numbers is 30. If each number is increased by 4 and then one extra number, 25, is added, what is the average of the resulting 7 numbers?

> **Type:** Numerical
> **Answer:** ≈32.71 (229/7).
> **Solution:** The original total is 6 × 30 = 180. Raising each of the six by 4 adds 24, giving 204 — equivalently the new mean of those six is 34, and 6 × 34 = 204 ✓. Adding 25 makes the total 229 over 7 numbers, and 229 / 7 = 32.714 ≈ 32.71. The new number is below the mean of the six, so it drags the combined average down from 34.
> **Key point:** Adding c to every element raises the mean by c; adding a *new* element also changes the count.

### Q52. A group of 30 employees has an average salary of ₹20,000. The 5 highest-paid employees are removed, and their average salary was ₹45,000. What is the average salary of the remaining 25 employees?

> **Type:** Numerical
> **Answer:** ₹15,000 (exact).
> **Solution:** The total salary is 30 × 20,000 = ₹6,00,000. The five removed account for 5 × 45,000 = ₹2,25,000, so ₹3,75,000 remains spread over 25 people, giving 375,000 / 25 = ₹15,000 ✓. The average falls well below the original ₹20,000 precisely because the highest earners left, and it must be computed from the residual sum rather than estimated.
> **Key point:** Removing a subgroup whose average exceeds the overall average always pulls the new average down; here 3,75,000/25 = ₹15,000.

### Q53. A car travels at 30 km/h for the first half of the journey and at 60 km/h for the second half, covering equal distances. What is the average speed for the whole journey?

> **Type:** Numerical
> **Answer:** 40 km/h (exact).
> **Solution:** For equal distances the average speed is the harmonic mean, 2v₁v₂/(v₁ + v₂) = 2 × 30 × 60/90 = 40 km/h. A direct check: suppose each half is 60 km, so the journey is 120 km in 2 h + 1 h = 3 h, giving 120/3 = 40 km/h ✓. The arithmetic mean of 45 km/h is wrong because more time is spent at the slower speed.
> **Key point:** Equal distances ⇒ harmonic mean, 2v₁v₂/(v₁+v₂); the arithmetic mean is always too high.

### Q54. A cyclist rides at 20 km/h for 2 hours and at 30 km/h for 1 hour. What is the average speed?

> **Type:** Comparison
> **Answer:** 23.33 km/h (≈ 70/3).
> **Solution:** Distance = 20 × 2 + 30 × 1 = 40 + 30 = 70 km over 3 hours, so the average is 70/3 = 23.33 km/h. The plain mean of 20 and 30 is 25 km/h, which would be correct only if the two speeds were maintained for equal times. Here the slower speed occupies twice as long as the faster one, so the true average is pulled down towards 20.
> **Key point:** Equal *times* ⇒ arithmetic mean; equal *distances* ⇒ harmonic mean. Identify which is fixed first.

### Q55. The average of 5 consecutive odd numbers is 39. What is the average of the 5 consecutive even numbers immediately following them?

> **Type:** Numerical
> **Answer:** 40 (exact).
> **Solution:** The mean of an odd number of consecutive values is the middle value, so the odd numbers are 35, 37, 39, 41, 43. The five consecutive even numbers immediately after 43 are 44, 46, 48, 50, 52, whose mean is the middle one, 48. Check by summation: (44 + 46 + 48 + 50 + 52)/5 = 240/5 = 48 ✓.
> **Key point:** The mean of consecutive integers is the centre value, so each answer is found by locating the middle term.

---

## Section 4. Time and work, pipes and cisterns, efficiency and work-rate problems

### Q56. A can complete a piece of work in 12 days and B in 18 days. Working together, how long do they take?

> **Type:** Numerical
> **Answer:** 7.2 days (exact, 36/5).
> **Solution:** A's daily rate is 1/12 of the work and B's is 1/18. Together the rate is 1/12 + 1/18 = 3/36 + 2/36 = 5/36, so the time is 36/5 = 7.2 days. The time is always less than the faster man's 12 days but not as small as half of it, because the work is additive in *rates*, not in times.
> **Key point:** Add rates 1/a + 1/b, then invert: together = ab/(a+b).

### Q57. A and B together finish a job in 6 days. A alone takes 10 days. How long does B alone take?

> **Type:** Numerical
> **Answer:** 15 days (exact).
> **Solution:** The combined rate is 1/6 and A's is 1/10, so B's rate is 1/6 − 1/10 = 5/30 − 3/30 = 2/30 = 1/15, i.e. 15 days. Check: 1/10 + 1/15 = 3/30 + 2/30 = 5/30 = 1/6 ✓.
> **Key point:** Subtract the known rate from the combined rate to get the missing rate; never subtract the times.

### Q58. Three taps A, B and C fill a tank in 6, 8 and 12 hours respectively. How long do all three take together?

> **Type:** Numerical
> **Answer:** 8/3 hours ≈ 2.67 hours.
> **Solution:** The combined rate is 1/6 + 1/8 + 1/12. With a common denominator of 24 this is 4/24 + 3/24 + 2/24 = 9/24 = 3/8 of the tank per hour, so the time is 8/3 ≈ 2.67 hours. That is faster than the fastest single tap (6 h), as it must be, and much faster than the slowest (12 h).
> **Key point:** Sum the rates, then invert: 1/6 + 1/8 + 1/12 = 3/8, so the time is 8/3 h.

### Q59. A pipe fills a tank in 20 minutes and another empties it in 30 minutes. With both open, how long will the tank take to fill?

> **Type:** Numerical
> **Answer:** 60 minutes (exact).
> **Solution:** The filling rate is 1/20 per minute and the emptying rate is 1/30, so the net rate is 1/20 − 1/30 = 3/60 − 2/60 = 1/60 per minute. The tank fills in 60 minutes. Because the emptying pipe is slower, the net rate is positive and the tank does fill; had the emptying pipe been faster, the tank would never fill.
> **Key point:** For a filling and an emptying pipe, net rate = 1/t_fill − 1/t_empty; a positive result means the tank fills.

### Q60. A cistern can be filled by two pipes in 6 hours. A leak can empty the full cistern in 12 hours. If both pipes and the leak are open, how long will the cistern take to fill?

> **Type:** Numerical
> **Answer:** 12 hours (exact).
> **Solution:** The two pipes fill at 1/6 per hour and the leak drains at 1/12, so the net rate is 1/6 − 1/12 = 2/12 − 1/12 = 1/12 of the cistern per hour, giving 12 hours. Without the leak the cistern would fill in 6 h, so the leak exactly doubles the time because it removes half the filling rate.
> **Key point:** Net rate = 1/t_inlets − 1/t_leak; a leak at half the inlet rate doubles the fill time.

### Q61. A and B working together complete a job in 12 days. They work together for 4 days and then A leaves. If B alone would take 30 days for the whole job, how many more days does B take to finish the remainder?

> **Type:** Numerical
> **Answer:** 20 more days (24 days in total).
> **Solution:** The combined rate is 1/12, and in the first 4 days they complete 4/12 = 1/3 of the job, leaving 2/3 undone. B works at 1/30 per day, so covering 2/3 takes (2/3) × 30 = 20 days, and the total elapsed time is 4 + 20 = 24 days ✓. Note that A's individual rate is never needed, since B alone finishes the remainder.
> **Key point:** Remaining fraction × B's solo time: (2/3) × 30 = 20 more days.

### Q62. A can do a piece of work in 20 days and B in 30 days. They work together for 5 days and then B leaves. In how many more days will A finish the remaining work?

> **Type:** Numerical
> **Answer:** 11.67 more days (exactly 35/3), 16.67 days in total.
> **Solution:** Together they work at 1/20 + 1/30 = 3/60 + 2/60 = 1/12 per day, so 5 days of joint work complete 5/12 of the job. The remainder is 7/12, and at A's rate of 1/20 per day this takes (7/12) × 20 = 140/12 = 35/3 ≈ 11.67 days ✓. The total elapsed time is 5 + 11.67 = 16.67 days.
> **Key point:** Multiply the remaining fraction by the solo time of whoever continues: (7/12) × 20 = 11.67 days.

### Q63. A takes 12 days and B takes 18 days to complete a work. What additional information is needed to find how long they take together, and why is it not derivable from the given data?

> **Type:** Conceptual
> **Answer:** None — the two solo times are sufficient, and together they take 7.2 days.
> **Solution:** The combined rate is 1/12 + 1/18 = 3/36 + 2/36 = 5/36, so the joint time is 36/5 = 7.2 days. Working in parallel assumes both men start simultaneously, attend the whole job, and contribute at constant independent rates; if either man does not work continuously the answer would change, but under the standard assumption the two times fully determine the joint time.
> **Key point:** Two solo times always determine the joint time — there is no missing information under the standard constant-rate assumption.

### Q64. A work is completed by 12 men in 15 days. How many men are required to complete the same work in 20 days?

> **Type:** Numerical
> **Answer:** 9 men (exact).
> **Solution:** The total work is 12 × 15 = 180 man-days, which must equal n × 20, giving n = 9. This is an inverse proportion: the number of men varies inversely as the time. Equivalently, 12/9 = 15/20 gives the same relation.
> **Key point:** Men × days is invariant: 12 × 15 = 180 = 9 × 20.

### Q65. A pipe fills a tank in 10 hours. Another fills it in 15 hours. If both are opened and, after 2 hours, the first is closed, how long does the second pipe then take to finish the tank, and what is the total time?

> **Type:** Numerical
> **Answer:** The second pipe takes 10 more hours; the total time is 12 hours (both exact).
> **Solution:** Both together fill 2 × (1/10 + 1/15) = 2 × (3/30 + 2/30) = 2 × 5/30 = 1/3 of the tank, leaving 2/3. The second pipe alone works at 1/15 per hour, so it needs (2/3) × 15 = 10 hours to finish the remainder. Adding the initial 2 hours gives a total of 12 hours.
> **Key point:** Fraction filled in the joint phase, then remaining fraction × solo time of the continuing pipe.

### Q66. A and B together can finish a work in 10 days, while A alone takes 15 days. How long does B alone take, and how long would they take together if both worked at 80% of their usual efficiency?

> **Type:** MCQ `GATE-1`
> **Answer:** B alone takes 30 days; at 80% efficiency together they take 12.5 days [c]
>
> (a) 20 days; 12.5 days
> (b) 30 days; 15 days
> (c) 30 days; 12.5 days
> (d) 6 days; 7.5 days
>
> **Solution:** The joint rate is 1/10 and A's is 1/15, so B's rate is 1/10 − 1/15 = 3/30 − 2/30 = 1/30, i.e. B alone takes 30 days. At 80% efficiency both rates scale by 0.8, so the joint rate becomes 0.8/10 = 0.08 per day and the time is 1/0.08 = 12.5 days ✓. Option (b) 15 days is the trap of scaling only one worker's rate instead of both.
> **Key point:** A uniform efficiency factor k scales the time by 1/k, so an 80% rate turns 10 days into 10/0.8 = 12.5 days.

### Q67. Four taps can fill a tank in 20 minutes. How long will it take if only 3 taps are working?

> **Type:** Numerical
> **Answer:** 26.67 minutes (≈ 80/3).
> **Solution:** The work is 4 × 20 = 80 tap-minutes. With 3 taps the time is 80/3 = 26.67 minutes. Because fewer workers means a proportionally lower rate, the time increases but by less than the drop in tap count (a drop from 4 to 3 taps, i.e. 25% fewer, raises the time by only 33% because 20 → 26.67 is a 33.3% rise).
> **Key point:** Taps × time is invariant; here 4 × 20 = 80 = 3 × 26.67.

### Q68. A worker completes 1/5 of a job in 3 days. How long does the whole job take at the same rate?

> **Type:** Numerical
> **Answer:** 15 days (exact).
> **Solution:** If 1/5 of the work takes 3 days, the whole work takes 5 × 3 = 15 days. Equivalently the rate is (1/5)/3 = 1/15 of the job per day, so the time is 15 days.
> **Key point:** Rate = (fraction of work)/time; invert to get the time for the whole job.

### Q69. A and B can do a work in 14 and 21 days. They work together, but A leaves after 4 days. How long does B take to finish the rest alone?

> **Type:** Numerical
> **Answer:** 11 more days (15 days in total).
> **Solution:** The joint rate is 1/14 + 1/21 = 3/42 + 2/42 = 5/42 per day, so in 4 days they complete 4 × 5/42 = 20/42 = 10/21 of the job, leaving 11/21. B works alone at 1/21 per day, so he needs (11/21) × 21 = 11 days to finish. The total elapsed time is 4 + 11 = 15 days.
> **Key point:** Remainder after the joint phase, scaled by the solo time of the worker who continues.

### Q70. In how many hours will 6 machines produce 240 items if each machine produces 4 items per hour?

> **Type:** Numerical
> **Answer:** 10 hours (exact).
> **Solution:** The combined rate is 6 × 4 = 24 items per hour, so the time is 240 / 24 = 10 hours. Machines × rate × time = items is the governing relation, and dividing the target by the combined rate gives the time directly.
> **Key point:** Time = total items ÷ (machines × rate per machine).

### Q71. If 5 workers can build a wall in 12 days, how many days will 4 workers take?

> **Type:** Comparison
> **Answer:** 15 days (exact).
> **Solution:** The work is 5 × 12 = 60 worker-days, so 4 workers need 60 / 4 = 15 days. Note that the 20% reduction in workers raises the time by 25%, not 20% — the relationship is inverse, not proportional.
> **Key point:** Fewer workers ⇒ proportionally more time; the changes are not equal in percentage.

### Q72. A tank is filled by a pipe in 15 hours but a leak empties it in 10 hours. With both open, what happens?

> **Type:** Conceptual
> **Answer:** The leak is faster than the pipe, so the net rate is negative and the tank can never be filled.
> **Solution:** The filling rate is 1/15 per hour and the draining rate is 1/10, so the net is 1/15 − 1/10 = 2/30 − 3/30 = −1/30 per hour. The negative sign means the level falls. A tank can only be filled when the inlet time is strictly less than the outlet time.
> **Key point:** A net rate is positive only when the pipe fills faster (smaller time) than the leak empties.

### Q73. A completes half a work in 10 days and B completes one-third of a work in 6 days. How long do they take working together on the whole work?

> **Type:** Numerical
> **Answer:** ≈9.47 days (180/19).
> **Solution:** A's rate is (1/2)/10 = 1/20 of the work per day and B's is (1/3)/6 = 1/18. With a common denominator of 180 the joint rate is 9/180 + 10/180 = 19/180 per day, so the time is 180/19 ≈ 9.47 days. A alone would need 20 days and B alone 18, so a joint figure of 9.47 days is comfortably faster than either, as it must be.
> **Key point:** Convert "fraction done in t days" to a rate by dividing first: (1/2)/10 = 1/20, (1/3)/6 = 1/18.

### Q74. A job requires 12 machines for 15 days. If 4 machines are added, how long will the job take?

> **Type:** Numerical
> **Answer:** 11.25 days (exact).
> **Solution:** The work is 12 × 15 = 180 machine-days. With 16 machines the time is 180 / 16 = 11.25 days. Adding a quarter more machines (4 on 12) reduces the time by a quarter (15 → 11.25), because both the machine count and its inverse appear symmetrically here.
> **Key point:** Machines × days is invariant, so t₂ = 180/16 = 11.25 days.

### Q75. P is twice as efficient as Q, and Q is three times as efficient as R. How long does R take if P alone takes 6 days?

> **Type:** Numerical
> **Answer:** 36 days (exact).
> **Solution:** P's rate is twice Q's and Q's is three times R's, so P's rate is 6 times R's. P takes 6 days, so R takes 6 × 6 = 36 days. Equivalently Q takes 12 days and R takes 36 days.
> **Key point:** Efficiency chains multiply: P : Q : R = 6 : 3 : 2, and times are the reciprocals.

---

## Section 5. Time–speed–distance, trains, boats and streams, relative speed

### Q76. A train 180 m long travelling at 54 km/h crosses a pole. How long does the crossing take?

> **Type:** Numerical
> **Answer:** 12 seconds (exact).
> **Solution:** Crossing a pole covers only the train's own length. Convert the speed: 54 × 5/18 = 15 m/s. Then 180 / 15 = 12 seconds. The 5/18 factor converts km/h to m/s by dividing by 3.6.
> **Key point:** Crossing a pole: time = train length ÷ speed; 1 km/h = 5/18 m/s.

### Q77. Two trains 150 m and 100 m long run at 40 km/h and 60 km/h in opposite directions on the same track. How long do they take to cross each other?

> **Type:** Numerical
> **Answer:** 9 seconds (exact).
> **Solution:** In opposite directions the relative speed is 40 + 60 = 100 km/h, which converts to 100 × 5/18 = 27.78 m/s. The distance to be covered is the sum of the lengths, 150 + 100 = 250 m, so the time is 250 / 27.78 = 9 seconds exactly, since 27.78 × 9 = 250 ✓.
> **Key point:** Opposite directions: add the speeds and add the two train lengths.

### Q78. Two trains 200 m and 150 m long travel at 30 km/h and 45 km/h in the same direction. How long does the faster train take to overtake the slower one completely?

> **Type:** Numerical
> **Answer:** 420 seconds (exact, 7 minutes).
> **Solution:** In the same direction the relative speed is 45 − 30 = 15 km/h = 15 × 5/18 = 5/6 m/s. To pass completely the faster train must gain the sum of the lengths, 200 + 150 = 350 m, so the time is 350 ÷ (5/6) = 350 × 6/5 = 420 seconds. Using 4.1667 m/s instead gives 84 s, which is the trap of dividing by the relative speed in km/h without converting units.
> **Key point:** Same direction: subtract the speeds, but still add the two train lengths; keep the units consistent.

### Q79. A train 200 m long crosses a platform 300 m long in 20 seconds. What is the train's speed in km/h?

> **Type:** Numerical
> **Answer:** 90 km/h (exact).
> **Solution:** Crossing a platform requires covering the train's own length plus the platform's, i.e. 200 + 300 = 500 m, in 20 s, giving 25 m/s. Converting: 25 × 18/5 = 90 km/h. The trap is to divide only the train's length, which would give 36 km/h.
> **Key point:** Crossing a platform: distance = train + platform; here 500 m / 20 s = 25 m/s = 90 km/h.

### Q80. A boat's speed in still water is 12 km/h and the stream flows at 3 km/h. What are the downstream and upstream speeds?

> **Type:** Numerical
> **Answer:** Downstream 15 km/h; upstream 9 km/h.
> **Solution:** The stream adds to the boat going downstream and opposes it going upstream, so the speeds are 12 + 3 = 15 and 12 − 3 = 9 km/h. These two speeds also give the still-water speed as (15 + 9)/2 = 12 and the stream speed as (15 − 9)/2 = 3, which is the standard way to recover the two unknowns from a pair of measured speeds.
> **Key point:** Downstream = b + s, upstream = b − s; hence b = (d + u)/2 and s = (d − u)/2.

### Q81. A man rows to a place 30 km downstream in 3 hours and returns upstream in 5 hours. Find the speed of the boat in still water and of the stream.

> **Type:** Numerical
> **Answer:** Boat 8 km/h, stream 2 km/h (both exact).
> **Solution:** Downstream speed = 30/3 = 10 km/h and upstream = 30/5 = 6 km/h. The still-water speed is (10 + 6)/2 = 8 and the stream speed is (10 − 6)/2 = 2 km/h. Check: 8 + 2 = 10 and 8 − 2 = 6 ✓.
> **Key point:** Derive d and u from distance/time, then average and half-difference them.

### Q82. A train is 1.5 times as fast as a car, and a car is 20 km/h faster than a bicycle. If the bicycle moves at 20 km/h, what are the car and train speeds?

> **Type:** Numerical
> **Answer:** Car 40 km/h; train 60 km/h (both exact).
> **Solution:** The car is 20 km/h faster than a 20 km/h bicycle, so the car does 40 km/h. The train is 1.5 × 40 = 60 km/h. The chain of "is k times as fast" statements must be applied in order, since each one feeds the next.
> **Key point:** Apply chained comparisons in sequence; each result becomes the next input.

### Q83. A car covers 300 km in 5 hours. At the same speed, how far will it travel in 8 hours, and what is its speed in m/s?

> **Type:** Numerical
> **Answer:** 480 km; 16.67 m/s.
> **Solution:** The speed is 300/5 = 60 km/h, so in 8 hours the car covers 60 × 8 = 480 km. In metres per second, 60 × 5/18 = 16.67 m/s.
> **Key point:** Speed × time = distance, and 1 km/h = 5/18 m/s for the reverse conversion.

### Q84. A train running at 36 km/h crosses a man standing on the platform in 5 seconds. How long is the train?

> **Type:** Numerical
> **Answer:** 50 m (exact).
> **Solution:** 36 km/h = 36 × 5/18 = 10 m/s. In 5 s the train covers 10 × 5 = 50 m, which is the train's own length, since a standing man is treated as a pole.
> **Key point:** A stationary observer is a pole; only the train's length is covered.

### Q85. A man can row upstream at 3 km/h and downstream at 9 km/h. Find the speed of the stream, the still-water speed, and the time to row 18 km upstream.

> **Type:** Numerical
> **Answer:** Stream 3 km/h; still-water speed 6 km/h; 6 hours upstream.
> **Solution:** The still-water speed is the average of the two directional speeds, (3 + 9)/2 = 6 km/h, and the stream speed is their half-difference, (9 − 3)/2 = 3 km/h. These are consistent: 6 − 3 = 3 upstream and 6 + 3 = 9 downstream ✓. The time to cover 18 km against the current is 18 / 3 = 6 hours.
> **Key point:** b = (d + u)/2 = 6 and s = (d − u)/2 = 3; the upstream time is 18/3 = 6 hours.

### Q86. A train 250 m long overtakes a person walking at 10 km/h in the same direction, running at 60 km/h. How long does the overtaking take?

> **Type:** Numerical
> **Answer:** 18 seconds (exact).
> **Solution:** The relative speed is 60 − 10 = 50 km/h = 50 × 5/18 = 13.89 m/s. Only the train's length is covered, 250 m, so the time is 250 / 13.89 = 18 seconds exactly, since 13.89 × 18 = 250 ✓.
> **Key point:** Overtaking a person covers only the train's length; the relative speed is the difference.

### Q87. A cyclist covers 24 km in 1 hour 20 minutes. At the same speed, how long will he take to cover 45 km?

> **Type:** Numerical
> **Answer:** 2 hours 30 minutes.
> **Solution:** 1 hour 20 minutes is 4/3 hours, so the speed is 24 ÷ (4/3) = 18 km/h. The time for 45 km is 45 / 18 = 2.5 hours = 2 hours 30 minutes. Mixed units must be converted to a single one before any division.
> **Key point:** Convert 1 h 20 min to 4/3 h before using it as a divisor.

### Q88. A train starts from A at 40 km/h and reaches B, and another starts from B at the same time at 60 km/h. If A and B are 300 km apart, when and where do they meet?

> **Type:** Numerical
> **Answer:** They meet after 3 hours, 120 km from A.
> **Solution:** The closing speed is 40 + 60 = 100 km/h, so the time is 300 / 100 = 3 hours. The first train covers 40 × 3 = 120 km, leaving 180 km to B. The split of the distance 120 : 180 = 2 : 3 matches the inverse ratio of the speeds, as it must.
> **Key point:** Distance split is the inverse of the speed ratio: 40 : 60 = 2 : 3 means 120 km and 180 km.

### Q89. A bus travelling at 50 km/h meets a car travelling at 70 km/h in the opposite direction. How far apart are they 1 hour before the meeting?

> **Type:** MCQ `GATE-1`
> **Answer:** 120 km [c]
>
> (a) 20 km
> (b) 50 km
> (c) 120 km
> (d) 140 km
>
> **Solution:** Travelling in opposite directions, the gap closes at the sum of the speeds, 50 + 70 = 120 km/h, so 1 hour before the meeting they were 120 km apart ✓. Options (a) 20 km and (b) 50 km come from subtracting the speeds, which would apply only if both were moving in the same direction, and option (d) 140 km comes from adding the wrong pair of figures.
> **Key point:** Opposite directions add the speeds: 50 + 70 = 120 km closed per hour.

### Q90. A ship travels 240 km downstream in 6 hours and the same distance upstream in 8 hours. Find the speed of the stream.

> **Type:** Numerical
> **Answer:** 5 km/h (exact).
> **Solution:** The downstream speed is 240/6 = 40 km/h and the upstream speed is 240/8 = 30 km/h. The stream speed is their half-difference, (40 − 30)/2 = 5 km/h, and the still-water speed is (40 + 30)/2 = 35 km/h. Check: 35 + 5 = 40 and 35 − 5 = 30 ✓.
> **Key point:** s = (d − u)/2; here (40 − 30)/2 = 5 km/h.

### Q91. Two trains of equal length, 150 m each, are running in opposite directions at 45 km/h and 25 km/h. How long do they take to cross each other?

> **Type:** Numerical
> **Answer:** 15.43 seconds (≈ 5400/350).
> **Solution:** The relative speed is 45 + 25 = 70 km/h = 70 × 5/18 = 350/18 m/s. The total distance to be covered is 150 + 150 = 300 m, so the time is 300 ÷ (350/18) = 300 × 18/350 = 5400/350 = 15.43 seconds. The trap is dividing 300 by 19.44 and rounding too early, or forgetting that both train lengths must be covered.
> **Key point:** Equal lengths mean the total distance is 300 m; 300 ÷ (350/18) = 15.43 s.

### Q92. A bridge is 1 km long. How fast must a vehicle travel to cross it in 10 minutes?

> **Type:** Numerical
> **Answer:** 6 km/h.
> **Solution:** The bridge is 1 km and the crossing time is 10 minutes = 1/6 hour, so the speed is 1 ÷ (1/6) = 6 km/h. Only distance and time matter here; the question adds no other speed, and converting 10 minutes to 1/6 hour is the only step required. In the related train version the train's own length must be added to the platform's before dividing.
> **Key point:** Speed = distance ÷ time; convert 10 minutes to 1/6 hour first.

### Q93. A car goes from P to Q at 60 km/h and returns at 40 km/h. What is the average speed for the whole trip?

> **Type:** Numerical
> **Answer:** 48 km/h (exact).
> **Solution:** For equal distances the average speed is the harmonic mean, 2xy/(x + y) = 2 × 60 × 40/100 = 48 km/h. A direct check over a 240 km leg: 4 h out and 6 h back, so 480 km in 10 h = 48 km/h ✓. The arithmetic mean of 50 km/h is wrong because the slower half takes longer.
> **Key point:** Equal distances ⇒ harmonic mean 2xy/(x+y) = 48 km/h, not the arithmetic mean 50.

---

## Section 6. Number system: divisibility, remainders, HCF/LCM, factors, prime factorisation, base conversion

### Q94. What is the smallest 3-digit number divisible by both 7 and 9, and what is the next one after it?

> **Type:** Numerical
> **Answer:** 126; the next is 189.
> **Solution:** Since 7 and 9 are coprime, a number divisible by both is a multiple of 63. The first 3-digit multiple is 2 × 63 = 126, and the next is 3 × 63 = 189. The gaps between consecutive common multiples are always 63, the LCM.
> **Key point:** A number divisible by two coprime integers is a multiple of their product, here 63.

### Q95. What is the HCF of 36 and 84, and what is their LCM?

> **Type:** Numerical
> **Answer:** HCF 12; LCM 252.
> **Solution:** 36 = 2² × 3² and 84 = 2² × 3 × 7, so the HCF takes the lowest powers: 2² × 3 = 12, and the LCM takes the highest: 2² × 3² × 7 = 252. The check HCF × LCM = 12 × 252 = 3,024 = 36 × 84 ✓.
> **Key point:** HCF takes the *lowest* powers of each prime, LCM the *highest*, and HCF × LCM = product of the numbers.

### Q96. What is the largest 4-digit number divisible by 11?

> **Type:** Numerical
> **Answer:** 9,999 (exact).
> **Solution:** 11 × 909 = 9,999, and 9,999 is itself the largest 4-digit number, so no search is needed. The divisibility rule for 11 confirms it: the alternating sum of the digits is (9 − 9 + 9 − 9) = 0, which is a multiple of 11 ✓.
> **Key point:** The 11-test is the alternating digit sum; 9,999 gives 0, so it is divisible.

### Q97. Express 2024 in its prime factorisation, and state how many positive factors it has.

> **Type:** Numerical
> **Answer:** 2024 = 2³ × 11 × 23, giving (3+1)(1+1)(1+1) = 16 positive factors.
> **Solution:** Dividing successively: 2024 / 2 = 1012, / 2 = 506, / 2 = 253, and 253 = 11 × 23. So 2024 = 2³ × 11 × 23. The number of positive factors of n = p₁^a₁ p₂^a₂ … is (a₁+1)(a₂+1)…, here 4 × 2 × 2 = 16.
> **Key point:** Number of factors of p₁^a₁ p₂^a₂ … pₖ^aₖ equals ∏(aᵢ + 1).

### Q98. What is the remainder when 7²⁰²⁴ is divided by 5?

> **Type:** Numerical
> **Answer:** 1 (exact).
> **Solution:** 7 ≡ 2 (mod 5), and 2⁴ = 16 ≡ 1 (mod 5), so the powers of 2 repeat with period 4. Since 2024 = 4 × 506 exactly, 7²⁰²⁴ ≡ 2²⁰²⁴ = (2⁴)^506 ≡ 1 (mod 5).
> **Key point:** For the last digit, find the period of the cycle and reduce the exponent modulo it; 2024 mod 4 = 0 gives 1.

### Q99. Convert the binary number 1011₂ to decimal, and the decimal number 45 to binary.

> **Type:** Numerical
> **Answer:** 1011₂ = 11; 45 = 101101₂.
> **Solution:** 1011₂ = 1×8 + 0×4 + 1×2 + 1×1 = 11. Going the other way, 45 = 32 + 8 + 4 + 1, and these are the values of the binary places 2⁵, 2³, 2², 2⁰, giving 101101₂. The two answers are independent conversions, not inverses of each other.
> **Key point:** Binary place values are 2⁰, 2¹, 2², … = 1, 2, 4, 8, 16, 32; write 1 where the place is used and 0 elsewhere.

### Q100. What is the smallest number that must be added to 2,600 to make it divisible by 17?

> **Type:** Numerical
> **Answer:** 3 (exact).
> **Solution:** 17 × 152 = 2,584, so 2,600 − 2,584 = 16 is the remainder, and adding 17 − 16 = 3 reaches 2,603 = 17 × 153 ✓.
> **Key point:** Required addition = divisor − remainder (and 0 if the remainder is already 0).

### Q101. The numbers 2⁴ and 4³ are written in decimal. What is their HCF, their LCM, and the sum of all distinct prime factors appearing in either number?

> **Type:** Numerical
> **Answer:** HCF 16; LCM 64; sum of distinct prime factors 2.
> **Solution:** 2⁴ = 16 and 4³ = (2²)³ = 2⁶ = 64. Both are powers of the single prime 2, so the HCF takes the lower exponent, 2⁴ = 16, and the LCM takes the higher, 2⁶ = 64. Check: 16 × 64 = 1,024 = 16 × 64 ✓. The only distinct prime factor is 2, so the sum is 2.
> **Key point:** HCF takes the lower exponent and LCM the higher; 2⁴ and 2⁶ give 16 and 64, sharing one distinct prime.

### Q102. A number leaves a remainder 3 when divided by 5 and a remainder 2 when divided by 7. What is the smallest such number greater than 100?

> **Type:** Numerical
> **Answer:** 128 (exact).
> **Solution:** List the numbers above 100 that are 3 more than a multiple of 5: 103, 108, 113, 118, 123, 128. Testing each modulo 7 gives remainders 5, 3, 1, 6, 4 and 2, and the first match is 128 = 7 × 18 + 2 ✓. Finally 128 mod 5 = 3, since 128 = 5 × 25 + 3, so both conditions hold and no smaller candidate qualifies.
> **Key point:** Enumerate candidates for the smaller modulus and test the other: 128 = 7×18 + 2 and 128 = 5×25 + 3.

### Q103. What is the remainder when 2¹⁰⁰ is divided by 9?

> **Type:** Numerical
> **Answer:** 7 (exact).
> **Solution:** 2¹ = 2, 2² = 4, 2³ = 8 ≡ −1 (mod 9), and 2⁶ ≡ 1 (mod 9). Since 100 = 6×16 + 4, we have 2¹⁰⁰ ≡ 2⁴ = 16 ≡ 7 (mod 9) ✓.
> **Key point:** 2³ ≡ −1 (mod 9) gives a period of 6; 100 mod 6 = 4, and 2⁴ = 16 ≡ 7.

### Q104. How many 3-digit numbers are divisible by both 4 and 6, and hence by 12?

> **Type:** Numerical
> **Answer:** 75 (exact).
> **Solution:** Since 4 and 6 share a factor of 2, being divisible by both means being divisible by 12. The 3-digit multiples of 12 run from 108 = 9×12 to 996 = 83×12, so the count is 83 − 9 + 1 = 75. The floor-function check gives floor(999/12) − floor(99/12) = 83 − 8 = 75 ✓.
> **Key point:** Count of n-digit multiples of d = floor((10ⁿ−1)/d) − floor((10ⁿᐟ¹−1)/d) = 75 here.

### Q105. The sum of two numbers is 60 and their product is 899. What are the numbers?

> **Type:** Numerical
> **Answer:** 29 and 31 (exact).
> **Solution:** Let the numbers be a and b. Then a + b = 60 and ab = 899, and (a − b)² = (a + b)² − 4ab = 3600 − 3596 = 4, so a − b = 2. Solving, a = 31 and b = 29, and 31 × 29 = 899 ✓.
> **Key point:** (a − b)² = (a + b)² − 4ab; here 3600 − 3596 = 4, giving a difference of 2.

### Q106. What is the remainder when 3⁵⁰ is divided by 7?

> **Type:** Numerical
> **Answer:** 2 (exact).
> **Solution:** 3⁶ = 729 = 7×104 + 1, so 3⁶ ≡ 1 (mod 7) and the powers repeat with period 6. Since 50 = 6×8 + 2, 3⁵⁰ = (3⁶)⁸ × 3² ≡ 1 × 9 ≡ 2 (mod 7) ✓.
> **Key point:** 3⁶ ≡ 1 (mod 7); reduce 50 mod 6 to 2 and compute 3² = 9 ≡ 2.

### Q107. What is the HCF of 2³ × 3² × 5 and 2² × 3⁴ × 7?

> **Type:** Numerical
> **Answer:** 36 (exact).
> **Solution:** The HCF takes the lowest power of every prime that appears in both numbers: 2² × 3² = 4 × 9 = 36. The prime 5 appears in only one number and 7 in only the other, so neither contributes. The LCM, by contrast, would be 2³ × 3⁴ × 5 × 7 = 3,780.
> **Key point:** HCF = 2² × 3² = 36; primes appearing in only one number are excluded entirely.

### Q108. Express 72 in binary, and then state what 1011000₂ equals in decimal.

> **Type:** Numerical
> **Answer:** 72 = 1001000₂; 1011000₂ = 88.
> **Solution:** 72 = 64 + 8 = 2⁶ + 2³, so the binary form is 1001000₂, with 1s in the 2⁶ and 2³ places only. Reading 1011000₂ gives 64 + 16 + 8 = 88, which is a different number — the extra 1 in the 2⁴ place is what accounts for the difference of 16. Writing the binary digits left to right from 2⁶ down to 2⁰ is the step most often miscounted.
> **Key point:** 72 = 2⁶ + 2³ = 1001000₂; 1011000₂ = 64 + 16 + 8 = 88.

### Q109. What is the remainder when 5²⁰ is divided by 13?

> **Type:** Numerical
> **Answer:** 1 (exact).
> **Solution:** 5² = 25 ≡ −1 (mod 13), so 5⁴ ≡ 1 (mod 13) and the period is 4. Since 20 = 4 × 5 exactly, 5²⁰ ≡ 1 (mod 13) ✓.
> **Key point:** 5² ≡ −1 (mod 13) gives a period of 4; 20 mod 4 = 0, so the remainder is 1.

### Q110. Two bells ring every 18 minutes and every 24 minutes. If they ring together at 9 a.m., when do they next ring together?

> **Type:** Numerical
> **Answer:** 10:12 a.m. (72 minutes later).
> **Solution:** The next simultaneous ringing is after the LCM of 18 and 24. Since 18 = 2 × 3² and 24 = 2³ × 3, the LCM is 2³ × 3² = 72 minutes. Adding 72 minutes to 9:00 a.m. gives 10:12 a.m. The gap of 72 must be divisible by both 18 and 24, and 72 = 4×18 = 3×24 ✓.
> **Key point:** Simultaneous events recur after the LCM; LCM(18, 24) = 72 minutes.

### Q111. What is the smallest positive integer that leaves remainder 2 when divided by 3, 4, 5 and 6, and what is that integer?

> **Type:** Numerical
> **Answer:** 62.
> **Solution:** The integer must be 2 more than a multiple of the LCM of 3, 4, 5 and 6, which is 60. So the smallest one is 60 + 2 = 62. Check: 62 mod 3 = 2, 62 mod 4 = 2, 62 mod 5 = 2 and 62 mod 6 = 2 ✓.
> **Key point:** "Remainder r on division by each of a set of numbers" means n = r + k·LCM, here 2 + 60 = 62.

### Q112. What is the remainder when 7⁵⁰ is divided by 6?

> **Type:** MCQ `GATE-1`
> **Answer:** 1 [a]
>
> (a) 1
> (b) 5
> (c) 7
> (d) 0
>
> **Solution:** 7 ≡ 1 (mod 6), so every positive power of 7 is also ≡ 1 (mod 6), and 7⁵⁰ ≡ 1. Option (b) is the trap of computing 7 mod 6 = 1 and then mis-deriving 5, and option (c) is invalid because a remainder must be smaller than the divisor 6.
> **Key point:** If a ≡ 1 (mod d) then aⁿ ≡ 1 (mod d) for all n; here 7 ≡ 1 (mod 6).

### Q113. What is the next number after 30 in the sequence 2, 6, 12, 20, 30, ...?

> **Type:** Numerical
> **Answer:** 42.
> **Solution:** The successive differences are 4, 6, 8, 10, so the pattern is n(n+1): 1×2 = 2, 2×3 = 6, 3×4 = 12, 4×5 = 20, 5×6 = 30, and the next is 6×7 = 42 ✓. The terms are the products of consecutive integers, which is a far more reliable pattern than "add 4, 6, 8…" guessed from the first two gaps.
> **Key point:** 1×2, 2×3, 3×4 … gives n(n+1); after 30 the next is 6×7 = 42.

---

## Section 7. Modular arithmetic basics and last-digit / last-two-digit problems

### Q114. What is the unit digit of 3⁷⁸?

> **Type:** Numerical
> **Answer:** 9 (exact).
> **Solution:** The unit digits of powers of 3 cycle as 3, 9, 7, 1 with period 4. Since 78 = 4×19 + 2, the units digit is the second in the cycle, 9. Reducing the exponent modulo the period is far faster than computing 3⁷⁸.
> **Key point:** Powers of 3 cycle 3, 9, 7, 1 with period 4; 78 mod 4 = 2 gives 9.

### Q115. What is the unit digit of 7³⁴?

> **Type:** Numerical
> **Answer:** 9 (exact).
> **Solution:** The unit digits of powers of 7 cycle as 7, 9, 3, 1 with period 4. Since 34 = 4×8 + 2, the units digit is the second in the cycle, 9. The cycle for 7 is the reverse of that for 3 after the first term, but the period of 4 is the same for all bases coprime to 10.
> **Key point:** Powers of 7 cycle 7, 9, 3, 1 with period 4; 34 mod 4 = 2 gives 9.

### Q116. What is the unit digit of 2¹⁰⁰⁰?

> **Type:** Numerical
> **Answer:** 6 (exact).
> **Solution:** The unit digits of powers of 2 cycle as 2, 4, 8, 6 with period 4. Since 1000 = 4×250 exactly, 1000 mod 4 = 0, and the fourth entry of the cycle is 6. A shortcut worth remembering: every positive power of 2 ends in 2, 4, 8 or 6, and any power with an exponent divisible by 4 ends in 6.
> **Key point:** Powers of 2 cycle 2, 4, 8, 6 with period 4; exponent ≡ 0 (mod 4) always gives 6.

### Q117. What is the last two digits of 3¹⁰⁰?

> **Type:** Numerical
> **Answer:** 01 (exact).
> **Solution:** The last two digits of powers of 3 cycle with period 20: 3¹⁰⁰ = (3²⁰)⁵, and 3²⁰ = 3,486,784,401 ends in 01. Since 100 is a multiple of 20, 3¹⁰⁰ also ends in 01 ✓. The last-two-digit cycle for 3 is 3, 9, 27, 81, 43, 29, 87, 61, 83, 49, 47, 41, 23, 69, 7, 21, 63, 89, 67, 1 — twenty terms returning to 1.
> **Key point:** Last-two-digit cycles have period 20; 100 mod 20 = 0 gives 01.

### Q118. What is the last two digits of 7¹⁵?

> **Type:** Numerical
> **Answer:** 07 (exact).
> **Solution:** 7² = 49, 7³ = 343, so 7⁵ ends in 43 and 7¹⁰ ends in 43² = 1849, i.e. 49. Then 7¹⁵ ends in 49 × 43 = 2,107, i.e. 07 ✓. Building the answer by successive squaring of the last two digits avoids any large arithmetic.
> **Key point:** Work only with the last two digits: 7⁵ → 43, 7¹⁰ → 49, 7¹⁵ → 49 × 43 = 2107 → 07.

### Q119. What is the remainder when 2⁰⁰ is divided by 10, and how does it relate to the last digit of 2²⁰⁰?

> **Type:** Comparison
> **Answer:** The remainder is 6, and it is identical to the last digit of 2²⁰⁰.
> **Solution:** The remainder on division by 10 is by definition the units digit, so the two questions are the same question. The units digits of powers of 2 cycle 2, 4, 8, 6 with period 4, and 200 mod 4 = 0, giving 6. This identity — remainder mod 10 = last digit — is the foundation of every last-digit problem.
> **Key point:** The remainder on division by 10 *is* the last digit; the problems are identical.

### Q120. A number leaves remainder 1 when divided by 2, 3, 4, 5, 6 and 7. What is the smallest such number greater than 1?

> **Type:** Numerical
> **Answer:** 421.
> **Solution:** The number is 1 more than a multiple of LCM(2, 3, 4, 5, 6, 7) = 420, so the smallest is 421. Check: 421 mod 2 = 1, 421 mod 3 = 1 (420 divisible by 3), and similarly for 4, 5, 6 and 7 ✓. This is the form behind the "n+1 divisible by 2..k" puzzles.
> **Key point:** Remainder 1 on division by each of 2…7 gives n = 1 + LCM = 421.

### Q121. What is the last digit of 7⁸ + 3⁸?

> **Type:** Numerical
> **Answer:** 2 (exact).
> **Solution:** The units digits of powers of 7 and of 3 both cycle with period 4 (7, 9, 3, 1 and 3, 9, 7, 1). Since 8 = 4×2 exactly, both terms end in the fourth entry of their cycle, which is 1. The sum therefore ends in 1 + 1 = 2. Direct check: 7⁸ = 5,764,801 and 3⁸ = 6,561, and their sum 5,771,362 ends in 2 ✓.
> **Key point:** An exponent divisible by 4 gives a last digit of 1 for both 7 and 3, so the sum ends in 2.

### Q122. What is the remainder when 3ⁿ is divided by 10, expressed in terms of n, for n = 1, 2, 3, 4?

> **Type:** Conceptual
> **Answer:** The remainder cycles as 3, 9, 7, 1 and then repeats; in general it is 3, 9, 7 or 1 according as n mod 4 is 1, 2, 3 or 0.
> **Solution:** Computing directly: 3¹ = 3, 3² = 9, 3³ = 27 → 7, 3⁴ = 81 → 1, and 3⁵ = 243 → 3, which is the first term again. The cycle length is therefore 4, and the remainder depends only on n mod 4. This is the general statement that every last-digit problem reduces to.
> **Key point:** Units digits are periodic in n; for base 3 the period is 4 with values 3, 9, 7, 1.

### Q123. What is the last digit of 12⁵ + 13⁵?

> **Type:** Numerical
> **Answer:** 5 (exact).
> **Solution:** Only the units digits matter, so this is 2⁵ + 3⁵. The units digits of 2 cycle 2, 4, 8, 6, so 2⁵ ≡ 2; those of 3 cycle 3, 9, 7, 1, so 3⁵ ≡ 3. The sum ends in 2 + 3 = 5 ✓.
> **Key point:** Reduce each base to its units digit first: 12⁵ + 13⁵ behaves like 2⁵ + 3⁵ = 32 + 243, which ends in 5.

### Q124. What is the remainder when 10³ + 11³ + 12³ is divided by 9?

> **Type:** Numerical
> **Answer:** 0 (exact).
> **Solution:** 10 ≡ 1, 11 ≡ 2 and 12 ≡ 3 (mod 9), so the expression is congruent to 1³ + 2³ + 3³ = 1 + 8 + 27 = 36 ≡ 0 (mod 9) ✓. The identity 1³ + 2³ + 3³ = 36 being divisible by 9 is not a coincidence, since 1+2+3 = 6 and the sum of cubes formula gives 6² = 36.
> **Key point:** Reduce each term modulo 9 first: 1 + 8 + 27 = 36 ≡ 0.

### Q125. What is the last digit of 7 × 7 × 7 × 7 × 7 × 7?

> **Type:** MCQ `GATE-1`
> **Answer:** 9 [b]
>
> (a) 7
> (b) 9
> (c) 3
> (d) 1
>
> **Solution:** The product is 7⁶. The units-digit cycle for 7 is 7, 9, 3, 1 with period 4, and 6 mod 4 = 2, so the digit is the second entry, 9. Option (a) is the trap of assuming the first digit of the cycle always repeats, and option (d) comes from reducing 6 to 0 mod 4 incorrectly.
> **Key point:** 7⁶ with 6 mod 4 = 2 lands on the second entry of the cycle 7, 9, 3, 1, giving 9.

### Q126. Find the remainder when 2⁰⁰⁵ is divided by 3 and, separately, when 2⁰⁰⁵ is divided by 5.

> **Type:** Comparison
> **Answer:** Remainder 2 on division by 3; remainder 2 on division by 5.
> **Solution:** Modulo 3, 2 ≡ −1, so 2²⁰⁰⁵ ≡ (−1)²⁰⁰⁵ = −1 ≡ 2 (mod 3). Modulo 5, 2⁴ = 16 ≡ 1, and 2005 = 4×501 + 1, so 2²⁰⁰⁵ ≡ 2¹ = 2 (mod 5). Both remainders are 2, even though the two moduli are unrelated — coincidence, not a general rule.
> **Key point:** Modulo 3 use 2 ≡ −1 (parity of the exponent); modulo 5 use the period 4. Here both give 2.

### Q127. What is the remainder when 5⁰⁰ is divided by 26?

> **Type:** Numerical
> **Answer:** 1 (exact).
> **Solution:** 5² = 25 ≡ −1 (mod 26), so 5⁴ ≡ 1 (mod 26) and the period divides 4. Since 500 = 4×125 exactly, 5⁵⁰⁰ ≡ 1 (mod 26) ✓. The trick is spotting that 25 is one less than the modulus, which makes squaring give −1.
> **Key point:** 5² = 25 ≡ −1 (mod 26) forces a period of 4, and 500 mod 4 = 0 gives remainder 1.

### Q128. What is the remainder when 2⁶ + 3⁶ is divided by 5?

> **Type:** Numerical
> **Answer:** 3 (exact).
> **Solution:** Modulo 5, 2⁴ ≡ 1 and 3⁴ ≡ 1, so 2⁶ ≡ 2² = 4 and 3⁶ ≡ 3² = 9 ≡ 4. Their sum is 4 + 4 = 8 ≡ 3 (mod 5) ✓. A direct check: 2⁶ + 3⁶ = 64 + 729 = 793, and 793 = 5×158 + 3.
> **Key point:** Reduce the exponents modulo the period 4 first: 6 mod 4 = 2, giving 4 + 4 = 8 ≡ 3.

### Q129. What is the remainder when 2024² is divided by 7?

> **Type:** Numerical
> **Answer:** 1 (exact).
> **Solution:** 2024 mod 7: 7×289 = 2,023, leaving remainder 1, so 2024 ≡ 1 (mod 7). Then 2024² ≡ 1² = 1 (mod 7) ✓. Squaring a small residue is much easier than squaring the full number before reducing.
> **Key point:** Reduce first: 2024 ≡ 1 (mod 7), so 2024² ≡ 1.

### Q130. What is the last digit of 999⁹⁹?

> **Type:** Numerical
> **Answer:** 9 (exact).
> **Solution:** 999 ends in 9, and the units digits of powers of 9 alternate 9, 1, 9, 1, … with period 2. Since 99 is odd, 999⁹⁹ ends in 9. Equivalently, 999 ≡ −1 (mod 10) and an odd power of −1 is −1 ≡ 9 (mod 10) ✓.
> **Key point:** A number ending in 9 is −1 mod 10, so odd powers end in 9 and even powers in 1.

### Q131. What is the remainder when 4⁴⁴ is divided by 10?

> **Type:** Comparison
> **Answer:** 6, and this holds for every positive exponent of 4.
> **Solution:** The units digits of powers of 4 cycle 4, 6, 4, 6, … with period 2, and 44 is even, so the digit is 6. The general reason is that 4² = 16 ends in 6 and 4 × 6 = 24 also ends in 6, so once a 6 appears it repeats forever. Odd powers end in 4 and even powers in 6.
> **Key point:** Powers of 4 alternate 4, 6 with period 2; even exponents always give 6.

---

## Section 8. Series and patterns: arithmetic, geometric, Fibonacci-like and mixed; sum of n terms

### Q132. The sum of the first n natural numbers is n(n+1)/2. Find the sum of the first 30 natural numbers.

> **Type:** Numerical
> **Answer:** 465 (exact).
> **Solution:** 30 × 31/2 = 465. The formula pairs the first and last terms (1+30, 2+29, …), each pair summing to 31, and there are 15 such pairs, giving 15 × 31 = 465 ✓.
> **Key point:** Σ_{k=1}^{n} k = n(n+1)/2; for n = 30 that is 15 × 31 = 465.

### Q133. An arithmetic progression has first term 7 and common difference 5. What is its 20th term, and what is the sum of its first 20 terms?

> **Type:** Numerical
> **Answer:** 20th term 102; sum 1,090.
> **Solution:** a₂₀ = a₁ + 19d = 7 + 95 = 102. The sum is n/2 × (first + last) = 20/2 × (7 + 102) = 10 × 109 = 1,090 ✓. A common error is to use 20d instead of 19d, since the 20th term involves only 19 steps.
> **Key point:** aₙ = a + (n−1)d and Sₙ = n(a + aₙ)/2; for n = 20 that is 102 and 1,090.

### Q134. A geometric progression has first term 3 and common ratio 2. What is its 10th term, and what is the sum of its first 10 terms?

> **Type:** Numerical
> **Answer:** 10th term 1,536; sum 3,069.
> **Solution:** a₁₀ = 3 × 2⁹ = 3 × 512 = 1,536. The sum of a GP is a(rⁿ − 1)/(r − 1) = 3(2¹⁰ − 1)/(2 − 1) = 3 × 1,023 = 3,069 ✓. A useful check: the sum of a GP is 2 × the last term minus the first, 2 × 1,536 − 3 = 3,069.
> **Key point:** aₙ = arⁿ⁻¹ and Sₙ = a(rⁿ − 1)/(r − 1); here 1,536 and 3,069 = 2(1,536) − 3.

### Q135. The Fibonacci-like sequence starts 1, 1, 2, 3, 5, 8, … What is the 12th term, and what is the sum of the first 12 terms?

> **Type:** Numerical
> **Answer:** 12th term 144; sum 376.
> **Solution:** The sequence continues 13, 21, 34, 55, 89, 144, so the 12th term is 144. The sum of the first 12 terms is 1+1+2+3+5+8+13+21+34+55+89+144 = 376 ✓. A fast identity gives this: the sum of the first n Fibonacci numbers equals F(n+2) − 1 = F₁₄ − 1 = 377 − 1 = 376.
> **Key point:** Each term is the sum of the two before it; Σ first n = F(n+2) − 1 = 377 − 1 = 376.

### Q136. What is the next term in the series 1, 4, 9, 16, 25, 36, ...?

> **Type:** Numerical
> **Answer:** 49.
> **Solution:** The terms are the squares of the natural numbers, so the next is 7² = 49. The first differences (3, 5, 7, 9, 11) are the odd numbers, which is the reliable way to recognise a square series rather than guessing from two terms.
> **Key point:** Differences 3, 5, 7, 9, 11 are the odd numbers, so the series is squares and the next term is 49.

### Q137. What is the next term in the series 2, 3, 5, 8, 13, 21, ...?

> **Type:** Numerical
> **Answer:** 34.
> **Solution:** Each term is the sum of the two preceding ones: 13 + 21 = 34. The differences are 1, 2, 3, 5, 8, which are the previous terms shifted, confirming the Fibonacci rule rather than an arithmetic pattern.
> **Key point:** Fibonacci-like series add the two previous terms, so after 13, 21 comes 34.

### Q138. What is the next term in the series 5, 11, 23, 47, 95, ...?

> **Type:** Numerical
> **Answer:** 191.
> **Solution:** The rule is "double and add 1": 5×2+1 = 11, 11×2+1 = 23, 23×2+1 = 47, 47×2+1 = 95, so 95×2+1 = 191 ✓. Equivalently, each term is one more than twice its predecessor, so aₙ + 1 doubles each time: 6, 12, 24, 48, 96, 192.
> **Key point:** "Double and add 1" is spotted by adding 1 to every term, which turns the series into a pure GP.

### Q139. What is the next term in the series 7, 10, 16, 25, 37, ...?

> **Type:** Numerical
> **Answer:** 52.
> **Solution:** The differences are 3, 6, 9, 12, so the second differences are constant at 3, which means the next difference is 15 and the next term is 37 + 15 = 52 ✓. A constant second difference of 3 identifies a quadratic law, in which case the nth term is (3n² + 3n + 4)/2, and this reproduces the listed values.
> **Key point:** Differences 3, 6, 9, 12 grow by 3, so the next difference is 15 and the next term is 52.

### Q140. What is the next term in the series 2, 6, 12, 20, 30, ...?

> **Type:** Numerical
> **Answer:** 42.
> **Solution:** The terms are n(n+1): 1×2, 2×3, 3×4, 4×5, 5×6, so the sixth is 6×7 = 42 ✓. The differences 4, 6, 8, 10 are consecutive even numbers, which is the observable signature of this law.
> **Key point:** Terms are n(n+1) with differences 4, 6, 8, 10, so after 30 comes 6×7 = 42.

### Q141. What is the next term in the series 1, 8, 27, 64, 125, ...?

> **Type:** Numerical
> **Answer:** 216.
> **Solution:** These are the cubes 1³, 2³, 3³, 4³, 5³, so the next is 6³ = 216 ✓. Their first differences are 7, 19, 37, 61 and the second differences are 12, 18, 24, rising by 6 each time — the signature of a cubic law.
> **Key point:** The terms are perfect cubes, so the sixth is 6³ = 216.

### Q142. What is the next term in the series 6, 10, 18, 34, 66, ...?

> **Type:** Numerical
> **Answer:** 130.
> **Solution:** The rule is "double, then subtract 2": 6×2−2 = 10, 10×2−2 = 18, 18×2−2 = 34 and 34×2−2 = 66, so 66×2−2 = 130 ✓. A reliable way to see the rule is to subtract 2 from every term, giving 4, 8, 16, 32, 64 — a pure geometric progression with ratio 2 — which confirms the doubling law.
> **Key point:** Subtracting 2 turns the series into 4, 8, 16, 32, 64, so the next term is 66×2 − 2 = 130.

### Q143. What is the next term in the series 4, 9, 19, 39, 79, ...?

> **Type:** Numerical
> **Answer:** 159.
> **Solution:** The rule is "double and add 1": 4×2+1 = 9, 9×2+1 = 19, 19×2+1 = 39, 39×2+1 = 79, so 79×2+1 = 159 ✓. Subtracting 1 from every term gives 3, 8, 18, 38, 78, which does not form a clean GP, so the "+1 after doubling" reading is the consistent one.
> **Key point:** aₙ = 2aₙ₋₁ + 1, so after 79 comes 79×2 + 1 = 159.

### Q144. In the series 1, 3, 6, 10, 15, 21, … what is the 10th term and what is the sum of the first 10 terms?

> **Type:** Numerical
> **Answer:** 10th term 55; sum 220.
> **Solution:** The differences are 2, 3, 4, 5, 6, so the terms are the triangular numbers n(n+1)/2 and the 10th is 10×11/2 = 55 ✓. The sum of the first n triangular numbers is n(n+1)(n+2)/6, which for n = 10 gives 10 × 11 × 12/6 = 220 ✓.
> **Key point:** Triangular numbers have nth term n(n+1)/2 and total n(n+1)(n+2)/6 = 220 for n = 10.

### Q145. What is the next term in the series 1, 4, 7, 10, 13, ...?

> **Type:** MCQ `GATE-1`
> **Answer:** 16 [d]
>
> (a) 14
> (b) 15
> (c) 18
> (d) 16
>
> **Solution:** The constant difference is 3, so the series is the arithmetic progression 1, 4, 7, 10, 13 with aₙ = 1 + 3(n−1), and the sixth term is 1 + 15 = 16 ✓. Option (a) 14 is the trap of adding 1, and option (b) 15 is the trap of adding 2.
> **Key point:** A constant difference of 3 gives a₆ = 1 + 3×5 = 16.

### Q146. The sum of the first 20 terms of an arithmetic progression is 210. If the first term is 1, what is the 20th term?

> **Type:** Numerical
> **Answer:** 20 (exact).
> **Solution:** S₂₀ = 20/2 × (1 + a₂₀) = 10(1 + a₂₀) = 210, so 1 + a₂₀ = 21 and a₂₀ = 20 ✓. This is the natural-number sequence, whose 20th term is 20, matching the sum formula n(n+1)/2 = 210 for n = 20.
> **Key point:** Sₙ = n(a₁ + aₙ)/2, so 210 = 10(1 + a₂₀) gives a₂₀ = 20.

### Q147. An arithmetic progression has 10th term 52 and 1st term 4. What is the common difference, and what is the sum of the first 10 terms?

> **Type:** Numerical
> **Answer:** Common difference 16/3 (≈ 5.33); sum 280.
> **Solution:** a₁₀ = a₁ + 9d, so 52 = 4 + 9d and 9d = 48, giving d = 16/3 ≈ 5.33. The sum is 10/2 × (4 + 52) = 5 × 56 = 280 ✓. A fractional common difference is perfectly legitimate and does not affect the sum formula, which only needs the first and last terms.
> **Key point:** d = (aₙ − a₁)/(n−1) = 48/9 = 16/3, and Sₙ = n(a₁ + aₙ)/2 = 280 regardless of d.

### Q148. What is the next term in the series 1, 3, 6, 10, 15, 21, 28, ...?

> **Type:** Numerical
> **Answer:** 36.
> **Solution:** The differences are 2, 3, 4, 5, 6, 7, so the next difference is 8 and 28 + 8 = 36 ✓. These are the triangular numbers, whose nth term is n(n+1)/2, and 8 × 9/2 = 36 confirms it.
> **Key point:** Triangular numbers; the differences run 2, 3, 4, … so after 28 comes 36.

### Q149. What is the next term in the series 1, 2, 6, 24, 120, ...?

> **Type:** Numerical
> **Answer:** 720.
> **Solution:** Each term multiplies by an increasing integer: ×2, ×3, ×4, ×5, so the next is ×6, giving 120 × 6 = 720 ✓. These are the factorials, n!, and the next one is 6! = 720.
> **Key point:** The terms are factorials 1!, 2!, 3!, 4!, 5!, so the next is 6! = 720.

---

## Section 9. Counting: permutations, combinations, circular arrangements, distinguishable objects

### Q150. In how many ways can 5 people be seated in a row of 5 chairs?

> **Type:** Numerical
> **Answer:** 120 (5! = 5 × 4 × 3 × 2 × 1).
> **Solution:** The first person has 5 choices, the second 4, and so on, giving 5! = 120. Permutation counts multiply because each choice leaves a correspondingly smaller pool for the next.
> **Key point:** n! = n(n−1)(n−2)···1; for n = 5 that is 120.

### Q151. In how many ways can 3 boys and 2 girls be arranged in a row if the two girls must stand together?

> **Type:** Numerical
> **Answer:** 48 (exact).
> **Solution:** Treat the two girls as a single block. That leaves 4 units to arrange — the block plus the 3 boys — giving 4! = 24, and the two girls can swap inside the block in 2! = 2 ways. The total is 24 × 2 = 48. Direct check: the block occupies one of 4 positions relative to the boys, so 4 × 3! × 2! = 4 × 6 × 2 = 48 ✓.
> **Key point:** The "must be together" trick gives (n−1)! × k!; here 4! × 2! = 48.

### Q152. In how many ways can a committee of 3 be chosen from 6 men and 4 women if it must contain at least one woman?

> **Type:** Numerical
> **Answer:** 100 (exact).
> **Solution:** Choosing any 3 from the 10 people gives 10C3 = 120, and the committees that break the rule are the all-male ones, of which there are 6C3 = 20. So 120 − 20 = 100. A case check confirms it: one woman and two men gives 4C1 × 6C2 = 4 × 15 = 60, two women and one man gives 4C2 × 6C1 = 6 × 6 = 36, and three women gives 4C3 = 4; 60 + 36 + 4 = 100 ✓.
> **Key point:** Total minus the complement: 10C3 − 6C3 = 120 − 20 = 100.
### Q153. In how many ways can 6 people be seated around a circular table, and how does that change if two particular people must sit next to each other?

> **Type:** Numerical
> **Answer:** 120 around the table; 48 with the two particular people together.
> **Solution:** Circular arrangements count as (n−1)! because rotations are identical, so (6−1)! = 120. With the pair treated as one block there are 5 units around the circle, giving (5−1)! = 24, and the pair can swap in 2! = 2 ways, so 24 × 2 = 48 ✓.
> **Key point:** Circular ⇒ (n−1)!; with a block, (n−2)! × 2! = 48 here.

### Q154. How many distinct 4-letter words can be formed from the letters of the word "LEVEL"?

> **Type:** Numerical
> **Answer:** 30.
> **Solution:** "LEVEL" has 5 letters with L repeated twice and E repeated twice, so the count is 5!/(2! × 2!) = 120/4 = 30 ✓. Dividing by the factorial of each repetition removes the overcounting caused by treating identical letters as distinct.
> **Key point:** Distinct arrangements = n!/(m₁! m₂! …); here 5!/(2!2!) = 30.

### Q155. A bag contains 3 red, 4 green and 5 blue balls. How many ways can 3 balls be drawn such that all three are of different colours?

> **Type:** Numerical
> **Answer:** 60.
> **Solution:** Choose one ball of each colour, multiplying the independent choices: 3 × 4 × 5 = 60 ✓. Order is irrelevant, and because the colours distinguish the three selections there is no factorial to divide out.
> **Key point:** One of each colour gives the product of the three counts, 3 × 4 × 5 = 60.

### Q156. In how many ways can 4 identical balls be distributed among 3 distinct boxes?

> **Type:** Numerical
> **Answer:** 15.
> **Solution:** The stars-and-bars formula for distributing n identical items into k distinct boxes without restriction is (n+k−1 choose k−1) = (4+3−1 choose 2) = 6C2 = 15 ✓. Enumerating the box triples (b₁,b₂,b₃) with b₁+b₂+b₃ = 4 gives exactly 15 solutions, confirming the count.
> **Key point:** Identical items into distinct boxes: (n+k−1)C(k−1); here 6C2 = 15.

### Q157. In how many ways can the letters of the word "BANANA" be arranged?

> **Type:** MCQ `GATE-1`
> **Answer:** 60 [c]
>
> (a) 120
> (b) 240
> (c) 60
> (d) 720
>
> **Solution:** "BANANA" has 6 letters with A repeated 3 times and N repeated twice, so the count is 6!/(3! × 2!) = 720/12 = 60 ✓. Option (d) is the trap of ignoring all repetition, and option (b) comes from dividing by 2! only, forgetting the three A's.
> **Key point:** Divide by the factorial of *each* repetition: 6!/(3!2!) = 60.

### Q158. In how many ways can 4 identical pens be distributed among 3 students so that every student gets at least one?

> **Type:** Numerical
> **Answer:** 3 (exact).
> **Solution:** Give one pen to each student, using 3 of the 4; the remaining pen goes to any one of the 3 students, giving 3 distributions. Stars-and-bars confirms it: x₁+x₂+x₃ = 4 with xᵢ ≥ 1 becomes y₁+y₂+y₃ = 1 in non-negative integers, whose number of solutions is (1+3−1)C(3−1) = 3C2 = 3 ✓. Equivalently, the possible triples are (2,1,1), (1,2,1) and (1,1,2).
> **Key point:** Shift each variable down by 1, then apply stars-and-bars: 3C2 = 3.

### Q159. How many 3-digit numbers can be formed from the digits 1, 2, 3, 4, 5 without repetition?

> **Type:** Numerical
> **Answer:** 60.
> **Solution:** The units-of-choice differ per position: 5 for the hundreds place, 4 for the tens, 3 for the units, so 5 × 4 × 3 = 60 ✓. This is a permutation count 5P3, and no division is needed because the digits are all distinct.
> **Key point:** 5P3 = 5 × 4 × 3 = 60; each position's count drops by one.

### Q160. In how many ways can 10 identical balls be placed in 4 distinct boxes if every box must contain at least 2 balls?

> **Type:** Numerical
> **Answer:** 10.
> **Solution:** Put 2 balls in each box, using 8, and distribute the remaining 2 among the 4 boxes without restriction. By stars-and-bars that is (2+4−1)C(4−1) = 5C3 = 10 ✓. Enumerating the residue patterns (2,0,0,0) and (1,1,0,0) gives 4 + 6 = 10, which matches.
> **Key point:** Remove the mandatory 2 per box, then stars-and-bars on the residue 2: 5C3 = 10.

### Q161. How many ways can a group of 4 be selected from 6 men and 5 women if the group must contain at least 2 women?

> **Type:** Numerical
> **Answer:** 215 (exact).
> **Solution:** Split into the three admissible cases. Exactly 2 women and 2 men gives 5C2 × 6C2 = 10 × 15 = 150; exactly 3 women and 1 man gives 5C3 × 6C1 = 10 × 6 = 60; and all 4 women gives 5C4 × 6C0 = 5. These cases are disjoint, so 150 + 60 + 5 = 215. A complement check agrees: the 4-person groups from 11 people number 11C4 = 330, and those with at most 1 woman number 6C4 + 5C1 × 6C3 = 15 + 100 = 115, leaving 330 − 115 = 215 ✓.
> **Key point:** Remember the all-women case: 150 + 60 + 5 = 215, or 11C4 − 6C4 − 5C1·6C3 = 330 − 115.

### Q162. In how many ways can 3 books be chosen from 8 different books?

> **Type:** Numerical
> **Answer:** 56.
> **Solution:** 8C3 = 8 × 7 × 6/(3 × 2 × 1) = 336/6 = 56 ✓. Since the order of choosing books is irrelevant, a combination is used rather than a permutation; using 8P3 = 336 would overcount each group 3! = 6 times.
> **Key point:** 8C3 = 8 × 7 × 6/6 = 56; divide the permutation count by 3!.

### Q163. In how many ways can 6 different books be distributed among 3 students if each student gets at least one book and the order of books on a shelf is irrelevant?

> **Type:** Numerical
> **Answer:** 540.
> **Solution:** Count all distributions and remove those leaving a student empty. All distributions number 3⁶ = 729. Subtracting the cases where a particular student gets nothing: C(3,1) × 2⁶ = 3 × 64 = 192. Adding back the doubly-overcounted cases: C(3,2) × 1⁶ = 3. So 729 − 192 + 3 = 540 ✓.
> **Key point:** Inclusion–exclusion on onto assignments: 3⁶ − 3·2⁶ + 3 = 729 − 192 + 3 = 540.

### Q164. In how many ways can the letters of the word "MONDAY" be arranged in a row?

> **Type:** Numerical
> **Answer:** 720.
> **Solution:** "MONDAY" has 6 distinct letters, so the count is 6! = 720 ✓. No division is needed since no letter repeats; the word being a weekday is irrelevant to the count.
> **Key point:** 6 distinct letters give 6! = 720; repetition would force a division by the factorials.

### Q165. In how many ways can 5 different balls be distributed among 3 boxes if no box may be empty?

> **Type:** MCQ `GATE-1`
> **Answer:** 150 [b]
>
> (a) 243
> (b) 150
> (c) 60
> (d) 125
>
> **Solution:** Assign each of the 5 distinct balls to one of 3 boxes with all boxes used. By inclusion–exclusion this is 3⁵ − 3 × 2⁵ + 3 = 243 − 96 + 3 = 150 ✓. Option (a) 243 is the trap of ignoring the "no empty box" condition, and option (c) 60 comes from wrongly imposing a one-ball-per-box style count.
> **Key point:** Onto functions from 5 balls to 3 boxes: 3⁵ − 3·2⁵ + 3 = 150.

### Q166. How many different ways can the letters of the word "ENGINE" be arranged in a row?

> **Type:** Numerical
> **Answer:** 180.
> **Solution:** "ENGINE" has 6 letters with E appearing 3 times, so the count is 6!/3! = 720/6 = 180 ✓. Only E repeats; the N, G and I are each distinct, so no further division applies.
> **Key point:** Divide by the factorial of each repeat: 6!/3! = 180.

### Q167. A committee of 3 is to be formed from 5 men and 4 women, with at least one woman on it, and a chair must be chosen from among the men on the committee. How many ways?

> **Type:** Numerical
> **Answer:** 110 (exact).
> **Solution:** Split by the number of men. With 2 men and 1 woman, the committee is 5C2 × 4C1 = 10 × 4 = 40, and any of the 2 men may chair, giving 40 × 2 = 80. With 1 man and 2 women, the committee is 5C1 × 4C2 = 5 × 6 = 30, and the single man must chair, adding 30. The cases are disjoint, so 80 + 30 = 110 ✓.
> **Key point:** The chair multiplies the two-men case by 2 but the one-man case by 1: 80 + 30 = 110.

### Q168. In how many ways can 8 people be seated around a round table if two of them refuse to sit next to each other?

> **Type:** Numerical
> **Answer:** 3,600.
> **Solution:** Total circular arrangements number (8−1)! = 5,040. The arrangements where the pair sits together treat them as a block, giving 2 × (7−1)! = 2 × 720 = 1,440. Subtracting, 5,040 − 1,440 = 3,600 ✓.
> **Key point:** (n−1)! total, minus 2 × (n−2)! for the blocked pair: 5,040 − 1,440 = 3,600.

### Q169. How many distinct permutations are there of the letters in "GEESE"?

> **Type:** Numerical
> **Answer:** 60.
> **Solution:** "GEESE" has 5 letters with E repeated 3 times and G and S appearing once each, so the count is 5!/3! = 120/6 = 60 ✓. Verifying by another route: choose the 3 positions for the E's in 5C3 = 10 ways, then arrange G and S in the remaining 2 positions in 2! = 2 ways, giving 10 × 2 = 60 ✓.
> **Key point:** 5!/3! = 60, equivalently 5C3 × 2! = 10 × 2.

### Q170. A box contains 4 red, 5 blue and 6 green balls. How many ways can 2 balls be drawn if they must be of different colours?

> **Type:** Numerical
> **Answer:** 74.
> **Solution:** Pair up the colour choices: red-blue gives 4 × 5 = 20, red-green gives 4 × 6 = 24, and blue-green gives 5 × 6 = 30. These cases are disjoint, so 20 + 24 + 30 = 74 ✓. Order is irrelevant, so each unordered colour pair is counted once.
> **Key point:** Sum the products of unlike-colour pairs: 20 + 24 + 30 = 74.

### Q171. In how many ways can 12 identical sweets be distributed among 4 children if each child must receive at least 2 sweets?

> **Type:** Numerical
> **Answer:** 35 (exact).
> **Solution:** Give 2 sweets to each child, using 8 of the 12, and distribute the remaining 4 without restriction. By stars-and-bars the number of non-negative solutions to y₁+y₂+y₃+y₄ = 4 is (4+4−1)C(4−1) = 7C3 = 35 ✓. As a check, 7C3 = 7 × 6 × 5/6 = 35.
> **Key point:** Shift each variable down by 2, then stars-and-bars on residue 4: 7C3 = 35.

### Q172. How many ways can 4 different prizes be awarded to 3 students if a student may receive more than one prize?

> **Type:** Numerical
> **Answer:** 81.
> **Solution:** Each of the 4 distinct prizes independently goes to one of 3 students, giving 3⁴ = 81 ✓. Since multiple prizes per student are allowed, there is no need to exclude empty recipients; the restriction-free count applies directly.
> **Key point:** Unrestricted distribution of 4 distinct prizes to 3 students is 3⁴ = 81.

### Q173. In how many ways can 3 boys and 3 girls be seated in a row so that no two girls sit together?

> **Type:** MCQ `GATE-1`
> **Answer:** 144 [d]
>
> (a) 720
> (b) 36
> (c) 72
> (d) 144
>
> **Solution:** Arrange the 3 boys first, which is 3! = 6 ways. This creates 4 gaps — before, between and after them — and the 3 girls must occupy 3 distinct gaps, chosen in 4C3 = 4 ways, and arranged among themselves in 3! = 6 ways. The total is 6 × 4 × 6 = 144 ✓. Option (b) 36 is the trap of forgetting the choice of gaps.
> **Key point:** 3! × 4C3 × 3! = 6 × 4 × 6 = 144; the boys create 4 gaps and no two girls may share one.

---

## Section 10. Probability: classical, on dice and cards, complements, independence and conditional probability

### Q174. A fair die is rolled once. What is the probability of getting a prime number?

> **Type:** Numerical
> **Answer:** 1/2 (≈ 0.50).
> **Solution:** The primes on a die are 2, 3 and 5, so 3 of the 6 equally likely outcomes qualify, giving 3/6 = 1/2 ✓. Note that 1 is neither prime nor composite, and 4 and 6 are composite, leaving exactly three primes.
> **Key point:** Primes on a die are 2, 3, 5, so P = 3/6 = 1/2.

### Q175. Two fair dice are rolled. What is the probability that the sum of the two numbers is 8?

> **Type:** Numerical
> **Answer:** 5/36 (≈ 0.14).
> **Solution:** The ordered pairs summing to 8 are (2,6), (3,5), (4,4), (5,3) and (6,2) — five of the 36 equally likely outcomes, so P = 5/36 ≈ 0.14 ✓. A common error is to list only three pairs and forget the symmetric ones.
> **Key point:** Count ordered pairs: 5 pairs sum to 8 out of 36, so P = 5/36.

### Q176. Two fair coins are tossed. What is the probability of getting exactly one head?

> **Type:** Numerical
> **Answer:** 1/2 (≈ 0.50).
> **Solution:** The four equally likely outcomes are HH, HT, TH and TT, of which HT and TH have exactly one head, so P = 2/4 = 1/2 ✓. Using combinations, P = 2C1 × 1C1 / 2C2 = 2/2 = 1.
> **Key point:** Exactly one head in two tosses is HT or TH, so P = 2/4 = 1/2.

### Q177. A card is drawn at random from a standard 52-card deck. What is the probability that it is a king or a heart?

> **Type:** Numerical
> **Answer:** 4/13 (≈ 0.31).
> **Solution:** There are 4 kings and 13 hearts, but the king of hearts is counted in both, so the favourable count is 4 + 13 − 1 = 16. Hence P = 16/52 = 4/13 ≈ 0.31 ✓. Omitting the overlap gives 17/52, which is the standard trap in these questions.
> **Key point:** |A ∪ B| = |A| + |B| − |A ∩ B| = 4 + 13 − 1 = 16, so P = 4/13.

### Q178. A fair die is rolled. What is the probability of NOT getting a 6?

> **Type:** MCQ `GATE-1`
> **Answer:** 5/6 [c]
>
> (a) 1/6
> (b) 1/3
> (c) 5/6
> (d) 2/3
>
> **Solution:** By the complement rule, P(not 6) = 1 − P(6) = 1 − 1/6 = 5/6 ✓. Option (a) 1/6 is the probability of the event itself, and option (b) 1/3 is the trap of counting only the even non-sixes.
> **Key point:** Use the complement: 1 − 1/6 = 5/6.

### Q179. Two fair dice are rolled. What is the probability that the sum is at most 3?

> **Type:** Numerical
> **Answer:** 1/12 (≈ 0.08).
> **Solution:** A sum of 2 arises only from (1,1), and a sum of 3 from (1,2) and (2,1), so there are 3 favourable ordered pairs out of 36 equally likely outcomes. Thus P = 3/36 = 1/12 ≈ 0.08 ✓. The trap here is including sums of 4, which are (1,3), (2,2) and (3,1) and are *not* allowed by "at most 3".
> **Key point:** Enumerate the qualifying pairs — (1,1), (1,2), (2,1) — to get 3/36 = 1/12.

### Q180. Two balls are drawn at random without replacement from a bag containing 4 red and 6 blue balls. What is the probability that both are red?

> **Type:** Numerical
> **Answer:** 2/15 (≈ 0.13).
> **Solution:** The probability of red on the first draw is 4/10, and given that, 3 red remain among 9 balls, so the second is 3/9. Multiplying, P = (4/10)(3/9) = 12/90 = 2/15 ≈ 0.13 ✓. The combination route agrees: 4C2/10C2 = 6/45 = 2/15. The events are dependent precisely because the balls are not replaced.
> **Key point:** Without replacement the draws are dependent: 4/10 × 3/9 = 2/15.

### Q181. What is the probability that a randomly chosen 2-digit number formed from the digits 1 to 9 without repetition is divisible by 5?

> **Type:** Numerical
> **Answer:** 1/9 (≈ 0.11).
> **Solution:** There are 9 × 8 = 72 ordered pairs of distinct digits from 1 to 9, all equally likely. Divisibility by 5 forces the units digit to be 5, and the tens digit can then be any of the remaining 8 digits, giving 8 favourable numbers. Hence P = 8/72 = 1/9 ≈ 0.11 ✓.
> **Key point:** The units digit is forced to be 5, so there are 8 favourable pairs out of 72: P = 1/9.

### Q182. A die is thrown twice. What is the probability that the first throw shows a 4 and the second shows a 5?

> **Type:** Comparison
> **Answer:** 1/36 (≈ 0.03), the same as the probability of any other specific ordered pair.
> **Solution:** The two throws are independent, so the joint probability is the product 1/6 × 1/6 = 1/36 ≈ 0.03 ✓. Every one of the 36 ordered outcomes has probability 1/36, so a named pair is no more or less likely than any other.
> **Key point:** Independent throws multiply: 1/6 × 1/6 = 1/36 for any named ordered pair.

### Q183. What is the probability of getting at least one head in three fair coin tosses?

> **Type:** Numerical
> **Answer:** 7/8 (≈ 0.88).
> **Solution:** Work by complement: the only outcome with no head is TTT, of probability 1/8. So P(at least one H) = 1 − 1/8 = 7/8 ≈ 0.88 ✓. Counting directly gives 2³ − 1 = 7 favourable outcomes out of 8.
> **Key point:** "At least one" is a complement: 1 − (1/2)³ = 7/8.

### Q184. A number is chosen at random from 1 to 20 inclusive. What is the probability that it is a perfect square?

> **Type:** Numerical
> **Answer:** 1/10 (0.10).
> **Solution:** The perfect squares in this range are 1, 4, 9 and 16, so 4 favourable numbers out of 20, giving 4/20 = 1/10 ✓. The next square, 25, lies outside the range, which is what bounds the count at four.
> **Key point:** Only 1, 4, 9, 16 qualify, so P = 4/20 = 1/10.

### Q185. One card is drawn from a well-shuffled deck of 52. What is the probability that it is an ace or a red card?

> **Type:** MCQ `GATE-1`
> **Answer:** 7/13 (≈ 0.54) [c]
>
> (a) 4/52
> (b) 13/52
> (c) 7/13
> (d) 1/2
>
> **Solution:** There are 26 red cards and 4 aces, but 2 of the aces are themselves red, so the union has 26 + 4 − 2 = 28 cards. Hence P = 28/52 = 7/13 ≈ 0.54 ✓. Option (d) 1/2 is the trap of assuming "ace or red" is half the deck.
> **Key point:** 26 + 4 − 2 = 28 favourable cards, so P = 28/52 = 7/13.

### Q186. Three fair dice are rolled. What is the probability that all three show different numbers?

> **Type:** Numerical
> **Answer:** 5/9 (≈ 0.56).
> **Solution:** The first die is free, the second must differ from it (5 of 6 options) and the third must differ from both (4 of 6), so P = 1 × (5/6) × (4/6) = 20/36 = 5/9 ≈ 0.56 ✓. The combination form 6 × 5 × 4 / 6³ = 120/216 = 5/9 gives the same value.
> **Key point:** Sequential without replacement from the outcome set: (5/6)(4/6) = 5/9.

### Q187. A number is drawn at random from the set {1, 2, ..., 12}. What is the probability that the chosen number divides 12 evenly?

> **Type:** Numerical
> **Answer:** 1/4 (0.25).
> **Solution:** The divisors of 12 lying between 1 and 12 are 1, 2, 3, 4, 6 and 12 — six numbers out of 12, so P = 6/12 = 1/4 ✓. Every positive divisor of 12 is at most 12, so no divisor is excluded by the range.
> **Key point:** Divisors of 12 are 1, 2, 3, 4, 6, 12, so P = 6/12 = 1/4.

### Q188. If two dice are rolled and the sum is 8, what is the conditional probability that the first die showed 4?

> **Type:** Numerical
> **Answer:** 1/5 (0.20).
> **Solution:** The conditioned sample space is the five ordered pairs (2,6), (3,5), (4,4), (5,3), (6,2), all equally likely once the sum is fixed. Only (4,4) has first die 4, so P = 1/5 ✓. This is the P(A|B) = P(A ∩ B)/P(B) form: 1/36 divided by 5/36 gives 1/5.
> **Key point:** Conditioning on the sum leaves 5 equally likely pairs, and only (4,4) qualifies: 1/5.

### Q189. Two fair coins are tossed. Given that at least one head appeared, what is the probability that both are heads?

> **Type:** Numerical
> **Answer:** 1/3 (≈ 0.33).
> **Solution:** The conditioned sample space is {HH, HT, TH}, three outcomes of equal weight, and only HH has both heads, so P = 1/3 ✓. Formally, P(HH | at least one H) = (1/4) / (3/4) = 1/3. Note this differs from the unconditional 1/4, since conditioning has removed the TTT-style outcome.
> **Key point:** P = (1/4)/(3/4) = 1/3; the conditional space drops TTT.

### Q190. A letter is chosen at random from the word "PROBABILITY" and found to be a vowel. What is the probability that it is a 'B'?

> **Type:** Numerical
> **Answer:** 0 (exact).
> **Solution:** 'B' is a consonant, so given that the letter is a vowel it cannot be 'B' — the conditional probability is 0. The word "PROBABILITY" has 11 letters with vowels A, O, A and I, so 4 vowels, and none of them is 'B' ✓. The conditional probability P(B | vowel) = 0 since the intersection of {B} and {vowels} is empty.
> **Key point:** When the two events are disjoint, the conditional probability is 0 regardless of their individual probabilities.

### Q191. A fair die is rolled three times. What is the probability that the sum of the three numbers is 6?

> **Type:** MCQ `GATE-1`
> **Answer:** 5/108 (≈ 0.046) [a]
>
> (a) 5/108
> (b) 1/36
> (c) 5/216
> (d) 1/27
>
> **Solution:** There are 6³ = 216 equally likely ordered triples. The positive triples summing to 6 are (1,1,4), (1,4,1), (4,1,1), (1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1) and (2,2,2) — ten of them, all with every entry between 1 and 6, so none is excluded. Hence P = 10/216 = 5/108 ≈ 0.046 ✓. Option (c) 5/216 is the trap of counting the three permutations of (1,1,4) and forgetting the rest.
> **Key point:** Ten ordered triples sum to 6 out of 216 outcomes, so P = 10/216 = 5/108.

### Q192. What is the probability of drawing a red ball from a bag of 3 red and 5 green balls, given that the ball drawn is not green?

> **Type:** Numerical
> **Answer:** 1 (exact).
> **Solution:** The event "not green" consists exactly of the 3 red balls, since the only colours present are red and green. So conditioning on not-green forces the ball to be red, and P = 3/3 = 1 ✓. This is the general fact that P(A | A) = 1.
> **Key point:** "Not green" is exactly "red" here, so the conditional probability is 1.

### Q193. Two distinct cards are drawn at random from a standard deck. What is the probability that both are aces?

> **Type:** Numerical
> **Answer:** 1/221 (≈ 0.0045).
> **Solution:** The probability of an ace first is 4/52, and given that, 3 aces remain among 51 cards, so P = (4/52)(3/51) = 12/2652 = 1/221 ≈ 0.0045 ✓. The combination form 4C2/52C2 = 6/1326 = 1/221 confirms it.
> **Key point:** (4/52)(3/51) = 1/221; equivalently 4C2/52C2.

---

## Section 11. Sets, functions and pigeonhole principle

### Q194. Let A = {1, 2, 3, 4} and B = {3, 4, 5}. What are A ∩ B and A ∪ B?

> **Type:** Numerical
> **Answer:** A ∩ B = {3, 4}; A ∪ B = {1, 2, 3, 4, 5}.
> **Solution:** The intersection holds the elements common to both sets, 3 and 4, while the union holds every distinct element appearing in either, which is 1, 2, 3, 4 and 5. A useful check is |A| + |B| = 4 + 3 = 7 = |A ∪ B| + |A ∩ B| = 5 + 2 ✓.
> **Key point:** |A ∪ B| + |A ∩ B| = |A| + |B|; here 5 + 2 = 7 = 4 + 3.

### Q195. A survey of 100 students found 60 study physics, 50 study chemistry and 20 study both. How many study neither?

> **Type:** Numerical
> **Answer:** 10.
> **Solution:** By inclusion–exclusion, the number studying at least one of the two is 60 + 50 − 20 = 90. So the number studying neither is 100 − 90 = 10 ✓.
> **Key point:** Subtract the overlap once: 60 + 50 − 20 = 90 study something, leaving 10 who study neither.

### Q196. If A and B are two sets with |A| = 12, |B| = 8 and A ∩ B = 5, what is |A ∪ B|?

> **Type:** Numerical
> **Answer:** 15.
> **Solution:** |A ∪ B| = |A| + |B| − |A ∩ B| = 12 + 8 − 5 = 15 ✓. The subtraction is essential because the 5 common elements are counted twice in 12 + 8.
> **Key point:** 12 + 8 − 5 = 15.

### Q197. How many subsets does a set with 4 elements have, and how many of them are proper?

> **Type:** Numerical
> **Answer:** 16 subsets in total; 15 proper subsets.
> **Solution:** A set with n elements has 2ⁿ subsets, because each element is independently in or out, so 2⁴ = 16. The set itself is the only subset that is not proper, so 16 − 1 = 15 proper subsets ✓. The empty set counts as a subset.
> **Key point:** 2ⁿ subsets, and exactly one — the set itself — is not proper.

### Q198. If f(x) = x² + 1, what are f(2), f(−2) and f(2) + f(−2)?

> **Type:** Numerical
> **Answer:** f(2) = 5; f(−2) = 5; f(2) + f(−2) = 10.
> **Solution:** f(2) = 4 + 1 = 5 and f(−2) = 4 + 1 = 5, so the sum is 10 ✓. The function is even, since (−x)² = x², which is why the two values coincide.
> **Key point:** f(x) = x² + 1 is even, so f(2) = f(−2) = 5 and the sum is 10.

### Q199. How many onto (surjective) functions exist from a 2-element set to a 2-element set?

> **Type:** Numerical
> **Answer:** 2.
> **Solution:** A function from 2 elements to 2 elements is onto only if both images are distinct and cover the target, so it must be either the identity or the swap. Both choices work, giving 2 ✓. The other two functions map both inputs to a single target and are not onto.
> **Key point:** Onto requires the images to cover the target, so 2! = 2 such functions here.

### Q200. If f: R → R is defined by f(x) = 3x − 2, what is the value of f⁻¹(7)?

> **Type:** Numerical
> **Answer:** 3.
> **Solution:** Solve 3x − 2 = 7 for x, which gives 3x = 9 and x = 3 ✓. In general, for f(x) = ax + b the inverse is f⁻¹(y) = (y − b)/a, and here (7 + 2)/3 = 3.
> **Key point:** f⁻¹(y) = (y − b)/a; f⁻¹(7) = (7 + 2)/3 = 3.

### Q201. By the pigeonhole principle, what is the minimum number of socks one must draw from a drawer containing 5 black and 5 white socks to guarantee a matching pair?

> **Type:** Numerical
> **Answer:** 3.
> **Solution:** Two draws could be one black and one white, which do not match. On the third draw the colour must repeat one of the two already present, since only two colours exist, so 3 draws guarantee a pair ✓. The principle states that drawing one more item than the number of categories forces a repeat.
> **Key point:** With k colours, k + 1 items guarantee a match; here 3.

### Q202. What is the largest number of integers that can be chosen from 1, 2, …, 18 so that no two chosen numbers differ by a multiple of 9?

> **Type:** Numerical
> **Answer:** 9.
> **Solution:** Group the 18 integers by their residue modulo 9: {1,10}, {2,11}, …, {9,18}, giving 9 classes. Two numbers whose difference is a multiple of 9 lie in the same class, so at most one number may be taken from each class, capping the selection at 9. Taking 1, 2, …, 9 achieves this, and no pair among them differs by 9 ✓. So 9 is both the maximum and the pigeonhole guarantee threshold: 10 chosen numbers would force a repeat.
> **Key point:** Residues mod 9 give 9 classes, so 9 numbers can avoid a multiple-of-9 difference but the 10th forces one.

### Q203. If the universal set has 15 elements and a set A has 8, how many elements are in Aᶜ?

> **Type:** Numerical
> **Answer:** 7.
> **Solution:** The complement of A contains every element of the universal set that is not in A, so |Aᶜ| = 15 − 8 = 7 ✓. In general |A| + |Aᶜ| = |U|.
> **Key point:** |Aᶜ| = |U| − |A| = 15 − 8 = 7.

### Q204. How many ordered pairs (x, y) of positive integers satisfy x + y = 6?

> **Type:** Numerical
> **Answer:** 5.
> **Solution:** Since x ranges over 1, 2, 3, 4, 5 and y is then determined as 5, 4, 3, 2, 1 respectively, there are 5 ordered pairs: (1,5), (2,4), (3,3), (4,2), (5,1) ✓. The order matters, so (1,5) and (5,1) are counted separately.
> **Key point:** Ordered pairs with x + y = n and positive entries number n − 1, here 5.

### Q205. In a group of 30 students, every student studies at least one of French or German, and 12 study both. How many study exactly one of the two languages?

> **Type:** Numerical
> **Answer:** 18.
> **Solution:** Let F and G be the sets of French and German students. Since every student is in F ∪ G, that union has 30 elements, and the overlap F ∩ G has 12. The symmetric difference F △ G, which is exactly those studying one language but not both, has 30 − 12 = 18 ✓.
> **Key point:** |F △ G| = |F ∪ G| − |F ∩ G| = 30 − 12 = 18.

### Q206. What is the value of the number of functions from a 1-element set to a 3-element set?

> **Type:** Numerical
> **Answer:** 3.
> **Solution:** The single input must map to one of the 3 target elements, and any of these choices defines a function, so there are 3 ✓. In general the number of functions from an m-element set to an n-element set is nᵐ, and here that is 3¹ = 3.
> **Key point:** Number of functions = nᵐ; from 1 element to 3 elements, 3¹ = 3.

### Q207. A drawer holds 4 pairs of socks, each pair a different colour. If 3 socks are drawn at random, what is the probability that a complete pair is among them?

> **Type:** Numerical
> **Answer:** 3/14 (≈ 0.21).
> **Solution:** The total ways to choose 3 socks from 8 is 8C3 = 56. For a favourable draw, pick which pair is complete in 4 ways and then choose the third sock from the remaining 6, giving 4 × 6 = 24. Hence P = 24/56 = 3/14 ≈ 0.21 ✓. No double-counting occurs, since with only 3 socks drawn at most one complete pair can appear.
> **Key point:** P = 4 × 6 / 8C3 = 24/56 = 3/14.

### Q208. If f(x) = x² and g(x) = 2x + 1, what is the composition (f ∘ g)(2)?

> **Type:** Numerical
> **Answer:** 25.
> **Solution:** (f ∘ g)(x) = f(g(x)), so evaluate g first: g(2) = 2×2 + 1 = 5, and then f(5) = 5² = 25 ✓. The order matters — (g ∘ f)(2) = g(4) = 9 — which is the whole point of distinguishing compositions.
> **Key point:** f ∘ g applies g first: g(2) = 5, then f(5) = 25; the reverse order gives 9.

---

## Section 12. Data sufficiency and logical reasoning (statement-based, system of equations, coding, inequalities, counting by cases)

### Q209. The ages of A and B sum to 40 and their product is 375. What are their ages?

> **Type:** Data Sufficiency
> **Answer:** 15 years and 25 years.
> **Solution:** Two independent equations in two unknowns are sufficient. Writing a + b = 40 and ab = 375, we get (a − b)² = 1600 − 1500 = 100, so a − b = 10. Adding and subtracting gives a = 25 and b = 15, and 25 × 15 = 375 ✓. Only statement II is needed if it instead gave the product directly, since a + b = 40 with ab = 375 is exactly the pair of independent conditions used here.
> **Key point:** A sum and a product are two independent equations, so the system is uniquely determined: 15 and 25.

### Q210. In a certain code, FLOWER is written as GMPXFS. How is GARDEN written in that code?

> **Type:** Logical reasoning
> **Answer:** HBSGFO.
> **Solution:** Compare position by position: F→G, L→M, O→P, W→X, E→F and R→S. Every letter is replaced by its immediate successor in the alphabet, a uniform shift of +1. Applying it to GARDEN gives G→H, A→B, R→S, D→E, E→F, N→O, so the code is HBSGFO ✓.
> **Key point:** A uniform +1 alphabet shift; GARDEN becomes HBSGFO.

### Q211. In a certain code, if BOOK is written as CPPL, how is PEN written?

> **Type:** Logical reasoning
> **Answer:** QFO.
> **Solution:** Each letter is shifted forward by one place: B→C, O→P, O→P, K→L. The same shift sends P→Q, E→F, N→O, so the answer is QFO ✓.
> **Key point:** The rule is "next letter" for every character, so PEN → QFO.

### Q212. A certain sum doubles in 6 years at simple interest. In how many years will it become three times itself at simple interest?

> **Type:** Numerical
> **Answer:** 12 years.
> **Solution:** Doubling in 6 years means the interest accrued in 6 years equals P itself, so the interest per year is P/6. Tripling requires total interest of 2P, which takes 2P ÷ (P/6) = 12 years ✓. Under simple interest the earned amount grows linearly, so doubling at year 6 implies tripling at year 12, not 18.
> **Key point:** Simple interest is linear: doubling in 6 years puts 2P of interest — triple the sum — at year 12.

### Q213. Point P lies strictly between A and B on a line, with AP = 4 and PB = 7. A moves 2 units toward P and B moves 3 units toward P. What is the new distance between A and P?

> **Type:** Numerical
> **Answer:** 2.
> **Solution:** Place A at 0 on a number line, so P is at 4 and B at 4 + 7 = 11. After the shifts, A sits at 2 and B at 8, giving a new gap of 6 between them. P has not moved, so its distance from the new A position is 4 − 2 = 2 ✓. The reduction from 4 to 2 is exactly the 2 units A moved, and the remaining gap P to B is 7 − 3 = 4, and 2 + 4 = 6 matches the new gap.
> **Key point:** Fixing P at 4 and A at 0, moving A by 2 makes the new distance 4 − 2 = 2, consistent with the shrunken gap of 6.

### Q214. Three friends split a bill of ₹1,200 so that the first pays 1/3 of it, the second pays 1/4 of the remainder, and the third pays the rest. How much does the third pay?

> **Type:** Numerical
> **Answer:** ₹600.
> **Solution:** The first pays 1200/3 = ₹400, leaving ₹800. The second pays a quarter of the remainder, 800/4 = ₹200, leaving ₹600 for the third ✓. The word "remainder" makes the fractions sequential rather than simultaneous.
> **Key point:** Sequential shares: 400 first, 200 second, and 600 remaining.

### Q215. Statements: I — 2x + 3y = 19. II — 3x + 2y = 21. If x and y are positive integers, what is x + y?

> **Type:** Data Sufficiency `GATE-1`
> **Answer:** 8.
> **Solution:** Each statement alone is one equation in two unknowns and admits many integer solutions, but together they determine the pair. Multiply I by 3 and II by 2 to eliminate y: 6x + 9y = 57 and 6x + 4y = 42, so 5y = 15 and y = 3. Then 2x + 9 = 19 gives x = 5, and 3×5 + 2×3 = 21 checks the second statement. Thus x + y = 8 ✓.
> **Key point:** Two independent linear equations fix x = 5 and y = 3, so x + y = 8; either statement alone would not suffice.

### Q216. In a certain code, 1 is written as A, 2 as B, 3 as C and 12 as L. How is 20 written in that code?

> **Type:** Logical reasoning
> **Answer:** T.
> **Solution:** Each number is coded by the letter occupying that position in the alphabet: 1 → A, 2 → B and 12 → L, since L is the 12th letter. The 20th letter is T, so 20 is written as T ✓. Such codes are read off by finding the rule in the sample pairs, then extending it — here the rule is simply "same position in the alphabet".
> **Key point:** The code is alphabet position for position, and the 20th letter is T.

### Q217. How many of the integers from 1 to 100 are neither perfect squares nor perfect cubes?

> **Type:** Numerical
> **Answer:** 88.
> **Solution:** There are 10 squares (1² to 10²) and 4 cubes (1³ to 4³) up to 100, and numbers that are both are the sixth powers: 1 and 64, so 2. By inclusion–exclusion the count that is a square or a cube is 10 + 4 − 2 = 12, and therefore 100 − 12 = 88 ✓.
> **Key point:** Squares and cubes overlap only at sixth powers; here 1 and 64, so 100 − (10 + 4 − 2) = 88.

### Q218. If 2x + 5 < 17 and 3x − 1 > 11, which of the following intervals contains every value of x satisfying both?

> **Type:** MCQ `GATE-2`
> **Answer:** 4 < x < 6 [c]
>
> (a) x < 4
> (b) x > 6
> (c) 4 < x < 6
> (d) 3 < x < 12
>
> **Solution:** From 2x + 5 < 17 we get 2x < 12, hence x < 6. From 3x − 1 > 11 we get 3x > 12, hence x > 4. Together these give exactly 4 < x < 6, which is option (c) ✓. Options (a) and (b) each contradict one of the two inequalities, and option (d) is true but far weaker, since it admits values such as 3.5 or 11 that violate the conditions.
> **Key point:** Solve each inequality separately — x < 6 and x > 4 — to get the tight interval 4 < x < 6.

### Q219. A bag of marbles contains only red, blue and green marbles in the ratio 4 : 3 : 2. If there are 36 marbles in total, how many are green?

> **Type:** Numerical
> **Answer:** 8.
> **Solution:** The ratio parts total 4 + 3 + 2 = 9, so each part is 36/9 = 4 marbles. Green corresponds to 2 parts, giving 2 × 4 = 8 ✓.
> **Key point:** Total parts 9, each worth 4 marbles, so green = 2 × 4 = 8.

### Q220. How many integers between 1 and 200 (inclusive) are divisible by 3 but not by 5?

> **Type:** Numerical
> **Answer:** 53 (exact).
> **Solution:** There are floor(200/3) = 66 multiples of 3 in the range. Those that are also multiples of 5 are exactly the multiples of 15, numbering floor(200/15) = 13. Subtracting gives 66 − 13 = 53 ✓. Listing the first few — 3, 6, 9, 12, 18 — confirms the pattern: 15, 30, 45 and so on are the ones excluded.
> **Key point:** Count multiples of 3 and remove multiples of lcm(3,5) = 15: 66 − 13 = 53.

### Q221. In a certain code, if each letter of a word is replaced by the letter two places after it in the alphabet, how is TIGER written?

> **Type:** Logical reasoning
> **Answer:** VKIGR.
> **Solution:** Advancing each letter by two gives T → V, I → K, G → I, E → G and R → T, so the code is VKIGR ✓. Such codes are read off by converting every sample letter and confirming that a single constant shift explains all of them, then extending that shift to the new word.
> **Key point:** A uniform +2 shift turns TIGER into VKIGR.

### Q222. Statements: I — The average of 5 numbers is 12. II — Three of the numbers are 10, 12 and 15. If the remaining two numbers are equal, what is each of them?

> **Type:** Data Sufficiency
> **Answer:** 11.5.
> **Solution:** Statement I gives the total as 5 × 12 = 60. Statement II fixes three of the numbers at 10 + 12 + 15 = 37, leaving 60 − 37 = 23 for the two equal numbers, so each is 23/2 = 11.5 ✓. Both statements are required: neither the total alone nor the partial list alone fixes the answer.
> **Key point:** Total 60 minus the known 37 leaves 23, split equally as 11.5 each.

### Q223. A shopkeeper buys an article for ₹240 and marks it at 25% above cost. If he sells it at a 10% discount on the marked price, what is his profit percent?

> **Type:** Numerical
> **Answer:** 12.5%.
> **Solution:** The marked price is 240 × 1.25 = ₹300, and the discount of 10% gives a selling price of 300 × 0.9 = ₹270. The profit is 270 − 240 = ₹30, which is 30/240 = 12.5% of cost ✓. Note that 25 − 10 = 15 is not the answer, since the two percentages act on different bases.
> **Key point:** CP 240 → MP 300 → SP 270, so the gain is 30/240 = 12.5%.

### Q224. If the HCF of two numbers is 12 and their LCM is 336, and one number is 48, what is the other number?

> **Type:** Numerical
> **Answer:** 84.
> **Solution:** For two positive integers the product equals the HCF times the LCM, so the other number is 12 × 336 / 48 = 4,032/48 = 84 ✓. Verification: gcd(48, 84) = 12 and lcm(48, 84) = 48 × 84/12 = 336, matching both conditions.
> **Key point:** a × b = HCF × LCM, so b = 12 × 336/48 = 84.

### Q225. A and B can do a piece of work in 12 and 18 days respectively. Working together, how long do they take?

> **Type:** Numerical
> **Answer:** 7.2 days.
> **Solution:** Their daily rates are 1/12 and 1/18, and together these give (3 + 2)/36 = 5/36 of the work per day. The time is therefore 36/5 = 7.2 days ✓. A useful check is that it must lie between half of 12 and all of 12, which 7.2 does.
> **Key point:** Rates add: 1/12 + 1/18 = 5/36, so the time is 36/5 = 7.2 days.

### Q226. What is the smallest positive integer n for which n! is divisible by 100?

> **Type:** Numerical
> **Answer:** 10.
> **Solution:** 100 = 2² × 5², so n! needs at least two factors of 5. The factorial 5! contains just one factor of 5, while 10! contains two (from 5 and 10), so 10! = 3,628,800 is divisible by 100 while 9! = 362,880 is not — it ends in 80 ✓. Each multiple of 5 contributes one factor, so n must reach 10.
> **Key point:** Two factors of 5 are needed, and the second appears at 10, so the smallest n is 10.

### Q227. Statements: I — Twice a number is 6 more than the number. II — The sum of the number and 5 is 11. Is the number uniquely determined?

> **Type:** Data Sufficiency
> **Answer:** Yes, the number is 6, and each statement alone suffices.
> **Solution:** Statement I gives 2n = n + 6, hence n = 6. Statement II gives n + 5 = 11, hence n = 6 as well. Both agree, and each is independently sufficient, so the number is uniquely determined as 6 ✓. In data-sufficiency terms this is the "either statement alone is enough" case, and the two are consistent, which is what a well-posed item requires.
> **Key point:** Each statement alone gives n = 6, so the data are both sufficient and mutually consistent.

### Q228. A car travels the first half of a journey at 40 km/h and the second half at 60 km/h. What is the average speed for the whole journey?

> **Type:** Numerical
> **Answer:** 48 km/h.
> **Solution:** Let each half be d km. The total time is d/40 + d/60 = d(3 + 2)/120 = 5d/120 = d/24 hours, and the total distance is 2d, so the average speed is 2d ÷ (d/24) = 48 km/h ✓. The naive average of 50 is wrong because the slower half occupies more time.
> **Key point:** For equal distances use the harmonic mean: 2 × 40 × 60/(40 + 60) = 48 km/h.

### Q229. The average of 5 consecutive even numbers is 26. What is the largest of them?

> **Type:** Numerical
> **Answer:** 30.
> **Solution:** For an odd number of consecutive terms the average is the middle term, so the numbers are 22, 24, 26, 28 and 30 and the largest is 30 ✓. Verification: their sum is 130, and 130/5 = 26 matches the given average.
> **Key point:** With an odd count of equally spaced terms the average equals the middle one, so the largest is 26 + 4 = 30.

### Q230. If the 8th term of an arithmetic progression is 37 and the 12th is 61, what is the common difference?

> **Type:** Numerical
> **Answer:** 6.
> **Solution:** From the 8th to the 12th term there are 4 steps, and the terms rise by 61 − 37 = 24, so d = 24/4 = 6 ✓. Dividing by the number of gaps rather than by the difference in indices is the step that matters here.
> **Key point:** d = (61 − 37)/(12 − 8) = 24/4 = 6; count the gaps, not the terms.

### Q231. Two numbers are in the ratio 5 : 7. If 8 is added to each, the new ratio is 3 : 4. What is the smaller number?

> **Type:** Numerical
> **Answer:** 40.
> **Solution:** Let the numbers be 5k and 7k. Then (5k + 8)/(7k + 8) = 3/4, so 4(5k + 8) = 3(7k + 8), giving 20k + 32 = 21k + 24 and k = 8. The numbers are 40 and 56, and adding 8 gives 48 and 64, which is indeed 3 : 4 ✓.
> **Key point:** Set the numbers as 5k and 7k and clear the fractions; k = 8, so the smaller number is 40.

### Q232. A vessel holds 60 litres of milk. If 12 litres of milk and 8 litres of water are poured into it, what fraction of the resulting mixture is water?

> **Type:** Numerical
> **Answer:** 1/10 (0.10).
> **Solution:** The additions are 12 + 8 = 20 litres, so the final volume is 60 + 20 = 80 litres, of which 8 are water. The fraction is therefore 8/80 = 1/10 = 0.10 ✓. Only the new water counts towards the numerator; the 72 litres of milk contribute nothing to it.
> **Key point:** Final volume 60 + 12 + 8 = 80, water fraction 8/80 = 1/10.

---

## Quick Revision — 30 Essential Results

- **Successive percentage change:** multiply the factors, never add them. Two rises of 10% give 1.1 × 1.1 = 1.21, i.e. 21%.
- **Successive discounts:** x% then y% off equals a total of x + y − xy/100 percent; 20% then 25% is 40%, not 45%.
- **Marked price, discount, gain:** fix CP = 100, set MP = CP(1 + markup), then SP = MP(1 − discount), and read the gain or loss as SP − 100.
- **Markup and discount never cancel** unless both act on the same base: (4/3) × (2/3) = 8/9, a loss of 1/9 ≈ 11.11%.
- **Profit on selling price** rather than cost: if profit is 1/3 of SP then SP − SP/3 = CP, so CP = (2/3)SP and profit = 1/2 CP.
- **Partnership time** is inversely proportional to capital: P₁/P₂ = T₂/T₁, so doubling the capital halves the time.
- **Alligation:** the ratio of the quantities of two ingredients equals the ratio of the differences between the mean price and each price, i.e. q₁/q₂ = (m − p₂)/(p₁ − m).
- **Alligation is a weighted average** — the mean price always lies between the cheapest and the dearest ingredient.
- **Ratio parts:** one part = total ÷ sum of ratio terms, then multiply by each term.
- **New ratio after equal change:** if (5k + a)/(7k + b) equals a known ratio, clear the fraction and solve for k first.
- **Averages:** new average = (old total + new item)/(old count + 1); the mean of the two averages is always wrong.
- **Removing a subgroup:** new average = (old total − removed total)/(old count − removed count), and removing an above-average group always lowers the average.
- **Average speed:** equal distances use the harmonic mean, 2v₁v₂/(v₁ + v₂); equal times use the simple mean.
- **Time and work:** rates add, times never do. If A takes a days and B takes b days, together they need ab/(a + b).
- **Work done in d days by a pair** is d/a + d/b of the job, and the remaining fraction is what the survivor must finish.
- **Pipes and cisterns:** with n similar pipes, the time is inversely proportional to n; the leak means the net rate is fill rate − leak rate.
- **Efficiency:** if A is twice as efficient as B, T_A = T_B/2. A chain of "p times as efficient" statements must be converted to a time ratio at the end.
- **Speed–distance–time:** speed = distance/time, and every quantity must be in a consistent unit before substitution.
- **Trains:** relative speed = sum of speeds in opposite directions and difference in the same direction; train length adds to the distance covered.
- **Boats and streams:** still-water speed = (up + down)/2, stream speed = (down − up)/2, and upstream time uses the smaller speed.
- **HCF** takes the lowest power of each common prime; **LCM** takes the highest power of every prime present in either.
- **a × b = HCF × LCM**, so one unknown can always be recovered from the other three.
- **Remainder by Fermat/Euler:** if p is prime and a is coprime to p, a^(p−1) ≡ 1 (mod p); reduce the exponent mod (p−1).
- **Smallest number with remainder r** on division by each of a set of numbers is LCM + r.
- **Unit digits cycle** with period dividing 4 for the digits 2, 3, 7, 8; powers of 0, 1, 4, 5, 6, 9 are constant.
- **Divisibility shortcuts:** a number is divisible by 9 (or 3) when its digit sum is, and by 11 when the alternating digit sum is.
- **Probability of union:** P(A ∪ B) = P(A) + P(B) − P(A ∩ B); the king of hearts is the classic double count.
- **Complements:** "at least one" is 1 − P(none), and conditional probability P(A|B) = P(A ∩ B)/P(B) shrinks the sample space.
- **Without replacement the draws are dependent**, so multiply the successive shrinking fractions rather than squaring the first.
- **Counting:** order irrelevant means combination, order relevant means permutation; circular arrangements give (n−1)!.
- **Identical objects into distinct boxes** use stars-and-bars, (n+k−1)C(k−1), and every box gets one first if each must be non-empty.
- **Pigeonhole:** k categories force a repeat at k+1 objects, and residues modulo m are the categories in "difference divisible by m" problems.
