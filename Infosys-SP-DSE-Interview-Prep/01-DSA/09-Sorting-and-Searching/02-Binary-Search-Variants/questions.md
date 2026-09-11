# 02 Binary Search Variants — Sorting / And / Searching

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Explain classic binary search and its complexity.**
   - On a sorted array, repeatedly halve the range comparing mid. O(log n) time, O(1) space — the textbook example of logarithmic search.

2. **When can binary search be used beyond arrays?**
   - On any monotonic predicate: answer-space binary search (search on answer), rotated arrays, floating-point search, and 'first/last true' boundaries.

3. **How do you find the first and last occurrence of target?**
   - Binary search with equality handling: first occurrence keeps moving right on equal; last moves left on equal — or use bisect_left/bisect_right. O(log n) each.

4. **How do you search in a rotated sorted array?**
   - Compare mid with the low pointer to identify the sorted half, check if target lies in it, then walk the half. Handles duplicates with high-- fallback. O(log n) typical.

5. **How do you find the rotation point (min element)?**
   - If arr[mid] > arr[high] the pivot is in the right half, else the left — a modified binary search. For duplicates, shrink boundary carefully. O(log n).

6. **What is binary search on answer?**
   - When the answer is numeric and feasible(x) is monotone, binary search the answer space: e.g., kth smallest, minimum max-speed to within deadline. O(log(range)·cost(feas)).

7. **How do you find the square root (integer and floating precision)?**
   - Binary search the answer: lo=0, hi=n; while feasible(hi-lo)>eps, mid; ans = greatest m*m<=n. Floating version uses epsilon. O(log n).

8. **How do you find the kth smallest pair distance?**
   - Sort, binary search the distance answer, count pairs with distance <= x via a two-pointer counter — the count is monotonic in x. O(n log MAX).

9. **What is the 'ship within D days', 'koko bananas', 'minimum capacity' family?**
   - Binary search the capacity (answer); check feasibility by greedy simulation; because capacity-monotonic, binary search works — SUPER popular in SP/DSE rounds.

10. **How do you search in a 2D sorted matrix (rows and cols sorted)?**
   - Start at top-right; move left if target < cell, down if >. O(n+m). Or treat as flattened sorted if row-major fully sorted — then plain binary search.

11. **How do you find a peak in a bitonic array?**
   - Compare mid with mid+1; rising→peak to the right, falling→left. The bitonic-peak binary search = variant of monotone peak in arrays. O(log n).

12. **How do you find the inserted position (lower_bound)?**
   - bisect_left returns the first index where x could be inserted to keep order; bisect_right the last. These are your O(log n) building blocks in Python.

13. **How do you handle duplicates correctly in rotated search?**
   - When arr[low]==arr[mid]==arr[high], we can't decide the side; decrement high and continue — worst-case O(n) but averages O(log n).

14. **What are integer-overflow-safe binary search midpoints?**
   - mid = lo + (hi-lo)//2 avoids lo+hi overflow in languages with fixed ints (C++/Java). Python ints don't suffer it, but state the practice anyway.

15. **How do you check if binary search replaces a linear scan in interviews?**
   - Whenever the problem asks for min/max/given a bound with a monotonic checker, or sorted arrays, reach for binary search and justify O(log n) over O(n).

16. **What is the intuition behind the 02 binary search variants technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

17. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

18. **State the time and space complexity of the optimal solution for most 02 binary search variants problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

19. **What common edge cases must be handled in 02 binary search variants implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

20. **How would you dry-run your 02 binary search variants code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

21. **Give a real-world analogy for 02 binary search variants.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

22. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

23. **What is the role of a prefix/suffix precomputation in 02 binary search variants?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

24. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

25. **How is 02 binary search variants asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

26. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

27. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

28. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

29. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

30. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

31. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

32. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

33. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

34. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

35. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

36. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

37. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

38. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

39. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

40. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

41. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

42. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

43. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

44. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

45. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

46. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

47. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

48. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

49. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

50. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

51. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

52. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

53. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

54. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

55. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

56. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

57. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

58. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

59. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

60. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

61. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

62. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

63. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

64. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

65. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

66. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

67. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

68. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

69. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

70. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

71. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

72. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

73. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

74. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

75. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

76. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

77. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

78. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

79. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

80. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

81. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

82. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

83. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

84. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

85. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

86. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

87. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

88. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

89. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

90. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

91. **Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.**
   - Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

92. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

93. **What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

94. **Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

95. **How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

96. **What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

97. **Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

98. **State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

99. **What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

100. **How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

</details>