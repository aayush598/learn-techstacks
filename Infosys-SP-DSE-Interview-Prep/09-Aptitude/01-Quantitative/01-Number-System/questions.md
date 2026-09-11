# 01 Number System — Quantitative

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What is a prime number and how do you test for primes quickly?**
   - A number >1 divisible only by 1 and itself. Test divisors up to sqrt(n) only: if none divide, it is prime — O(sqrt(n)); sieve up to N gives all primes in O(N log log N).

2. **What is the divisibility rule for 11?**
   - A number is divisible by 11 if the alternating sum of its digits is a multiple of 11 (e.g., 918082: 9-1+8-0+8-2=22, divisible).

3. **What digit replaces * so that 5*91 is divisible by 9?**
   - Divisibility by 9 requires digit sum divisible by 9: 5+*+9+1 = 15+* → nearest multiple is 18, so *=3. Method: sum digits, add the shortcut.

4. **What is the HCF and LCM of two numbers and its relation?**
   - HCF divides both; LCM is the least common multiple. Product rule: a*b = HCF(a,b) * LCM(a,b) — the working theorem for both calculations.

5. **What is the remainder of 2^100 when divided by 5?**
   - 2^4 = 16 ≡ 1 (mod 5); 100 = 4*25, so 2^100 = (2^4)^25 ≡ 1^25 = 1. Remainders cycle — the cyclic-pattern technique for powers.

6. **What is a perfect square's word property?**
   - A perfect square ends only in 0,1,4,5,6,9 and its digital root is 0,1,4,7,9 — quick filters to reject candidates in elimination questions.

7. **What are the common number-system formulas?**
   - Sum of first n naturals n(n+1)/2; squares n(n+1)(2n+1)/6; cubes (n(n+1)/2)^2; number of divisors via prime-factor exponents — the three formulas aptitude lean on.

8. **What is the difference between 'by which' and 'of which' phrasing?**
   - 'x is what percent OF y' = x/y*100; 'y is what percent MORE THAN x' = (y-x)/x*100 — read the base carefully; the base changes the answer.

9. **Convert 0.125 into a fraction.**
   - 0.125 = 125/1000 = 1/8. Recognise common decimal-fraction pairs (1/8, 1/4, 3/8, 5/8) as speed shortcuts.

10. **What is the last two digits of 7^25?**
   - Cycles of 7^1..7^4 last two digits: 07,49,43,01 and repeat every 4; 25 mod 4 = 1 → last two digits are 07. Cycle-length technique again.

11. **State the formula used to solve 01 number system problems quickly in aptitude tests.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

12. **Describe a shortcut technique for 01 number system.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

13. **Give a practice problem for 01 number system and solve it step by step.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

14. **What are the typical mistakes students make in 01 number system?**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

15. **How would you allocate time if 01 number system questions appear in the aptitude section?**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

16. **Explain the concept of 01 number system to a non-mathematical friend.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

17. **Which branch of 01 number system is most frequently combined with data interpretation?**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

18. **What reference materials and practice frequency do you recommend for 01 number system?**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

19. **How do negative values, fractions, or percentages interplay in 01 number system?**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

20. **Create your own derivation of the key result used in 01 number system.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

21. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

22. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

23. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

24. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

25. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

26. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

27. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

28. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

29. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

30. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

31. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

32. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

33. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

34. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

35. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

36. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

37. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

38. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

39. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

40. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

41. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

42. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

43. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

44. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

45. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

46. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

47. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

48. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

49. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

50. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

51. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

52. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

53. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

54. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

55. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

56. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

57. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

58. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

59. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

60. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

61. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

62. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

63. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

64. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

65. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

66. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

67. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

68. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

69. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

70. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

71. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

72. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

73. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

74. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

75. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

76. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

77. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

78. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

79. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

80. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

81. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

82. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

83. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

84. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

85. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

86. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

87. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

88. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

89. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

90. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

91. **State the formula used to solve 01 number system problems quickly in aptitude tests. Extend your answer with a second example.**
   - Every aptitude topic rests on a small set of formulas and unit-adjustments; write the formula, plug the numbers, and always sanity-check the units (hours/minutes, percent, ratio) before finalising — most errors are unit errors.

92. **Describe a shortcut technique for 01 number system. Extend your answer with a second example.**
   - Look for symmetric/divisible structure, cancellation in fractions, or base-value anchoring (e.g., assume a convenient total like 100 or LCM). Shortcuts reduce arithmetic but should not skip the conceptual check.

93. **Give a practice problem for 01 number system and solve it step by step. Extend your answer with a second example.**
   - Illustrative solved step-by-step with setup -> arithmetic -> final answer and a one-line verification; solving aloud with structured steps is exactly what the assessment expects.

94. **What are the typical mistakes students make in 01 number system? Extend your answer with a second example.**
   - Misreading what is asked, unit mix-ups, ignoring 'approximate' vs 'exact', and arithmetic slips under time pressure. Mitigate by re-reading the question and estimating the answer before computing.

95. **How would you allocate time if 01 number system questions appear in the aptitude section? Extend your answer with a second example.**
   - Attempt easy-familiar ones first, leave hard ones for review, and never exceed the per-question budget. Question order does not reflect difficulty; strategy beats speed.

96. **Explain the concept of 01 number system to a non-mathematical friend. Extend your answer with a second example.**
   - Reduce it to a story with everyday quantities; once the story is clear the numbers are just bookkeeping. This oral-reasoning skill is exactly what Infosys gauges in HR/communication checks.

97. **Which branch of 01 number system is most frequently combined with data interpretation? Extend your answer with a second example.**
   - Often paired in DI charts; combining contexts raises difficulty, so practice reading graphs/tables and converting them into the formula under test.

98. **What reference materials and practice frequency do you recommend for 01 number system? Extend your answer with a second example.**
   - Standard quantitative books for concepts, daily timed drills for speed, and topic-wise mock tests to build accuracy; consistency over quantity is what increases the score.

99. **How do negative values, fractions, or percentages interplay in 01 number system? Extend your answer with a second example.**
   - Convert everything to one consistent representation first (fractions -> percentages or vice versa), maintain signs rigorously, and test the boundary case to confirm direction of change.

100. **Create your own derivation of the key result used in 01 number system. Extend your answer with a second example.**
   - Derive from first principles using a simple example, then generalise to the formula. This proves understanding; memorised formulas without derivation collapse under a twist.

</details>