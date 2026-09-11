# 01 Sorting Algorithms — Sorting / And / Searching

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **List the comparison-based sorting algorithms and their complexities.**
   - Bubble O(n^2), selection O(n^2), insertion O(n^2), merge O(n log n), quick O(n log n) avg / O(n^2) worst, heap O(n log n). Stable variants differ per algorithm.

2. **Explain merge sort.**
   - Divide into halves, recursively sort each, merge two sorted halves with two pointers. O(n log n) time guaranteed, O(n) space for the merge buffer. Stable.

3. **Explain quicksort and its partition step.**
   - Pick a pivot; partition so smaller elements precede it and larger follow; recurse on each side. Average O(n log n), worst O(n^2) for bad pivots; in-place but unstable.

4. **How does heap sort work?**
   - Build a max-heap, repeatedly swap the max to the end and heapify the shrinking prefix. O(n log n), O(1) extra space, not stable. It uses the heap data structure.

5. **Compare merge sort vs quicksort.**
   - Merge: guaranteed O(n log n), stable, needs O(n) space. Quick: in-place, faster constants, unstable, worst O(n^2) — choose by guarantee vs speed requirement.

6. **What is counting sort and when is it applicable?**
   - Non-comparison sort over integer keys in range k: counts→prefix→place. O(n+k) time/space; linear only when k is small and keys are integers/naturals.

7. **What is radix sort?**
   - Sorts integer keys by digit positions (LSD first) with a stable counting sort per digit. O(d·(n+k)); linear when digits are few.

8. **What is bucket sort?**
   - Distributes elements into n buckets, sorts each (usually insertion), concatenates. O(n) average for uniformly distributed keys — used in floating-point and histogram problems.

9. **What is Timsort (Python's sort)?**
   - Hybrid of merge+insertion optimised for real data: finds natural runs, merges with galloping; stable, adaptive O(n) on already-sorted data.

10. **How do you sort with a custom comparator in Python?**
   - key=lambda x: expr computes a sortable key; for multi-criteria use tuples; for order-reversal negate numerics or use functools.cmp_to_key for comparison semantics.

11. **What does stability mean and why does it matter?**
   - Stable sorting preserves the relative order of equal elements — needed when sorting by multiple keys where earlier sorts must not be scrambled (e.g., radix LSD).

12. **How do you sort nearly-sorted arrays efficiently?**
   - Insertion sort is O(n·k) for k-offset arrays; or use a k-size heap for the heap-sort variant. Expected from the interviewer: recognise near-sortedness.

13. **How do you detect if a sorted array is a valid non-descending sequence?**
   - One pass checking arr[i] <= arr[i+1] for all i; any violation returns false. O(n).

14. **How do you sort strings by frequency?**
   - Count via Counter, then sort keys by (-count, char); or bucket by frequency. O(n log n) or O(n) with buckets.

15. **What is the difference between stable unstable examples?**
   - Stable: bubble, insertion, merge, counting, Timsort. Unstable: quick, heap, selection (with naive swaps). State this — interviewers ask directly.

16. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

17. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

18. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

19. **What common edge cases must be handled in 01 sorting algorithms implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

20. **How would you dry-run your 01 sorting algorithms code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

21. **Give a real-world analogy for 01 sorting algorithms.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

22. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

23. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

24. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

25. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

26. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

27. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

28. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

29. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

30. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

31. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

32. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

33. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

34. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

35. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

36. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

37. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

38. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

39. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

40. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

41. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

42. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

43. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

44. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

45. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

46. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

47. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

48. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

49. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

50. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

51. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

52. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

53. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

54. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

55. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

56. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

57. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

58. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

59. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

60. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

61. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

62. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

63. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

64. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

65. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

66. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

67. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

68. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

69. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

70. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

71. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

72. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

73. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

74. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

75. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

76. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

77. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

78. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

79. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

80. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

81. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

82. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

83. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

84. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

85. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

86. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

87. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

88. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

89. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

90. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

91. **Give a real-world analogy for 01 sorting algorithms. Extend your answer with a second example.**
   - Analogy: 01 sorting algorithms is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

92. **How do you decide between a hash map, sorting, or two pointers as tools for 01 sorting algorithms? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

93. **What is the role of a prefix/suffix precomputation in 01 sorting algorithms? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

94. **Explain the optimisation step you would mention after writing the naive version for 01 sorting algorithms. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

95. **How is 01 sorting algorithms asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

96. **What is the intuition behind the 01 sorting algorithms technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

97. **Write the brute-force approach for a typical 01 sorting algorithms problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

98. **State the time and space complexity of the optimal solution for most 01 sorting algorithms problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

99. **What common edge cases must be handled in 01 sorting algorithms implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

100. **How would you dry-run your 01 sorting algorithms code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

</details>