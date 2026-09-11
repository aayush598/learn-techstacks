# Quantitative — Number System Interview Questions and Answers

## Q1: What is a prime number and how do you test for primes quickly?
**A:** A number >1 divisible only by 1 and itself. Test divisors up to sqrt(n) only: if none divide, it is prime — O(sqrt(n)); sieve up to N gives all primes in O(N log log N).

## Q2: What is the divisibility rule for 11?
**A:** A number is divisible by 11 if the alternating sum of its digits is a multiple of 11 (e.g., 918082: 9-1+8-0+8-2=22, divisible).

## Q3: What digit replaces * so that 5*91 is divisible by 9?
**A:** Divisibility by 9 requires digit sum divisible by 9: 5+*+9+1 = 15+* → nearest multiple is 18, so *=3. Method: sum digits, add the shortcut.

## Q4: What is the HCF and LCM of two numbers and its relation?
**A:** HCF divides both; LCM is the least common multiple. Product rule: a*b = HCF(a,b) * LCM(a,b) — the working theorem for both calculations.

## Q5: What is the remainder of 2^100 when divided by 5?
**A:** 2^4 = 16 ≡ 1 (mod 5); 100 = 4*25, so 2^100 = (2^4)^25 ≡ 1^25 = 1. Remainders cycle — the cyclic-pattern technique for powers.

## Q6: What is a perfect square's word property?
**A:** A perfect square ends only in 0,1,4,5,6,9 and its digital root is 0,1,4,7,9 — quick filters to reject candidates in elimination questions.

## Q7: What are the common number-system formulas?
**A:** Sum of first n naturals n(n+1)/2; squares n(n+1)(2n+1)/6; cubes (n(n+1)/2)^2; number of divisors via prime-factor exponents — the three formulas aptitude lean on.

## Q8: What is the difference between 'by which' and 'of which' phrasing?
**A:** 'x is what percent OF y' = x/y*100; 'y is what percent MORE THAN x' = (y-x)/x*100 — read the base carefully; the base changes the answer.

## Q9: Convert 0.125 into a fraction.
**A:** 0.125 = 125/1000 = 1/8. Recognise common decimal-fraction pairs (1/8, 1/4, 3/8, 5/8) as speed shortcuts.

## Q10: What is the last two digits of 7^25?
**A:** Cycles of 7^1..7^4 last two digits: 07,49,43,01 and repeat every 4; 25 mod 4 = 1 → last two digits are 07. Cycle-length technique again.

## Q11: State the formula used to solve 01 number system problems quickly in aptitude tests.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q12: Describe a shortcut technique for 01 number system.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q13: Give a practice problem for 01 number system and solve it step by step.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q14: What are the typical mistakes students make in 01 number system?
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q15: How would you allocate time if 01 number system questions appear in the aptitude section?
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q16: Explain the concept of 01 number system to a non-mathematical friend.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q17: Which branch of 01 number system is most frequently combined with data interpretation?
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q18: What reference materials and practice frequency do you recommend for 01 number system?
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q19: How do negative values, fractions, or percentages interplay in 01 number system?
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q20: Create your own derivation of the key result used in 01 number system.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q21: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q22: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q23: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q24: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q25: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q26: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q27: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q28: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q29: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q30: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q31: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q32: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q33: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q34: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q35: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q36: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q37: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q38: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q39: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q40: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q41: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q42: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q43: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q44: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q45: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q46: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q47: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q48: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q49: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q50: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q51: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q52: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q53: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q54: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q55: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q56: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q57: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q58: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q59: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q60: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q61: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q62: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q63: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q64: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q65: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q66: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q67: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q68: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q69: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q70: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q71: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q72: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q73: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q74: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q75: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q76: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q77: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q78: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q79: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q80: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q81: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q82: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q83: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q84: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q85: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q86: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q87: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q88: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q89: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q90: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

## Q91: State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.
**A:** Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

## Q92: Describe a shortcut technique for 01 number system. Extend your answer with a second example.
**A:** Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

## Q93: Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.
**A:** Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

## Q94: What are the typical mistakes students make in 01 number system? Extend your answer with a second example.
**A:** Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

## Q95: How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.
**A:** Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

## Q96: Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.
**A:** Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

## Q97: Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.
**A:** Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

## Q98: What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.
**A:** Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

## Q99: How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.
**A:** Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

## Q100: Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.
**A:** Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.
