# 06 Advanced Ll Problems — Linked / Lists

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What makes an advanced linked-list problem?**
   - Multi-pointer relocation, cycle math, reversing sub-ranges, or combining LL with recursion/hashing/problems like reorder list, k-group reverse, rotate.

2. **How do you reverse a linked list between two given positions (left-right)?**
   - Dummy + prev; skip to left, then reverse the sub-range tail-by-tail inserting each after prev; fix the start's next to the remaining tail. O(n).

3. **How do you reverse nodes in alternating k-groups?**
   - Track group order; reverse odd groups, skip even groups; reuse k-group reverse on the effective remainder. O(n).

4. **How do you find the starting node of the intersection of two linked lists?**
   - Length-align or two-pointer swap-tails approach; intersection node equals where the two pointers converge after swapping. O(n+m).

5. **How do you add two huge numbers as lists without consuming (no big ints)?**
   - Reverse both lists, add with carry; reverse the result. O(n) time and O(n) output space.

6. **How do you flatten a multi-level doubly linked list?**
   - DFS over child pointers: splice each child sub-list between current and next; maintain child's tail to last. O(n) overall.This mirrors real problems asked in product interviews.

7. **How do you copy a linked list with each node having random pointers?**
   - Three passes: interleave clones, set random pointers via next-of-original's random, then unweave. O(n) time, O(n) space (or hash map).

8. **What is the 'odd-even linked list' problem?**
   - Segregate nodes by index parity into odd and even lists, then connect odd-tail to even-head. O(n), single pass.

9. **How do you sort a linked list in O(n log n)?**
   - Merge sort with slow/fast split and merge — the only guaranteed O(n log n) LL sort. Quicksort suffers pivot/pointer overhead.

10. **How do you remove duplicates from an unsorted linked list without a set?**
   - Nested loops comparing each node against its suffix (O(n^2)); required when space is bound. A hash set reduces to O(n) time.

11. **How do you detect if a linked list is a palindrome with O(1) space?**
   - Mid + reverse-second-half + compare; optionally restore. This is the accepted in-place dictation answer.

12. **How do you find the fractional (n/k-th) node from the end?**
   - Advance one pointer k steps or use slow/fast ratio; for 1/k from the tail, use a block-based two-pointer.

13. **How do you join two sorted lists and merge duplicates?**
   - Merge then dedupe adjacent equal values in a final pass; or dedupe during merge by skipping equal nexts. O(n+m).

14. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

15. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

16. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

17. **What common edge cases must be handled in 06 advanced ll problems implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

18. **How would you dry-run your 06 advanced ll problems code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

19. **Give a real-world analogy for 06 advanced ll problems.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

20. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

21. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

22. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

23. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

24. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

25. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

26. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

27. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

28. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

29. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

30. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

31. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

32. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

33. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

34. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

35. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

36. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

37. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

38. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

39. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

40. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

41. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

42. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

43. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

44. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

45. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

46. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

47. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

48. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

49. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

50. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

51. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

52. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

53. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

54. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

55. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

56. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

57. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

58. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

59. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

60. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

61. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

62. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

63. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

64. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

65. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

66. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

67. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

68. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

69. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

70. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

71. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

72. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

73. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

74. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

75. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

76. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

77. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

78. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

79. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

80. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

81. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

82. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

83. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

84. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

85. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

86. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

87. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

88. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

89. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

90. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

91. **What is the role of a prefix/suffix precomputation in 06 advanced ll problems? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

92. **Explain the optimisation step you would mention after writing the naive version for 06 advanced ll problems. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

93. **How is 06 advanced ll problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

94. **What is the intuition behind the 06 advanced ll problems technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

95. **Write the brute-force approach for a typical 06 advanced ll problems problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

96. **State the time and space complexity of the optimal solution for most 06 advanced ll problems problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

97. **What common edge cases must be handled in 06 advanced ll problems implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

98. **How would you dry-run your 06 advanced ll problems code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

99. **Give a real-world analogy for 06 advanced ll problems. Extend your answer with a second example.**
   - Analogy: 06 advanced ll problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

100. **How do you decide between a hash map, sorting, or two pointers as tools for 06 advanced ll problems? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

</details>