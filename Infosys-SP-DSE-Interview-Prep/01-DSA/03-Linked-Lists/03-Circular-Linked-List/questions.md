# 03 Circular Linked List — Linked / Lists

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a circular linked list.**
   - The tail node's next pointer points back to the head (or the list has no null terminator). Advantage: from any node you can reach the whole list.

2. **What distinct advantage does a circular list offer over linear?**
   - Round-robin scheduling, playlist rotation, and continuous iteration without resetting; head deletion can be O(1) since tail->head is known.

3. **How do you traverse a circular linked list safely?**
   - Start at head and iterate until the pointer returns to head (compare with the starting node reference) — never rely on None.

4. **How do you split a circular list into two equal halves?**
   - Use slow/fast to find the middle, locate the node before it, break the link, and reconnect each half into its own circle. O(n).

5. **How do you insert at the end of a circular list when only head known?**
   - Walk to the tail (node.next==head), set tail.next=new, new.next=head. Without a tail pointer this is O(n); keep a tail pointer for O(1).

6. **How do you implement Josephus elimination with a circular list?**
   - Count steps and remove every kth node until one remains; update neighbours before deleting. O(n*k) naive, or index arithmetic for large k.

7. **How do you detect whether a singly list is actually circular?**
   - Floyd's slow/fast pointers — if they meet, there's a cycle; or compare with the expected tail condition tail.next==head.

8. **How do you reverse a circular linked list?**
   - Reverse pointers exactly like singly, then reconnect: new head becomes old tail (its next now points back to the new tail), preserving circularity.

9. **Where does the circular list beat queus in implementation?**
   - Implementing a ring buffer: with a fixed array plus modulo index the circular structure gets used directly for audio streams and caches.

10. **What is the intuition behind the 03 circular linked list technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

11. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

12. **State the time and space complexity of the optimal solution for most 03 circular linked list problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

13. **What common edge cases must be handled in 03 circular linked list implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

14. **How would you dry-run your 03 circular linked list code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

15. **Give a real-world analogy for 03 circular linked list.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

16. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

17. **What is the role of a prefix/suffix precomputation in 03 circular linked list?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

18. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

19. **How is 03 circular linked list asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

20. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

21. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

22. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

23. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

24. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

25. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

26. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

27. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

28. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

29. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

30. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

31. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

32. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

33. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

34. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

35. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

36. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

37. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

38. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

39. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

40. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

41. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

42. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

43. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

44. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

45. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

46. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

47. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

48. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

49. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

50. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

51. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

52. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

53. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

54. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

55. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

56. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

57. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

58. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

59. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

60. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

61. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

62. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

63. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

64. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

65. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

66. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

67. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

68. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

69. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

70. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

71. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

72. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

73. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

74. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

75. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

76. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

77. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

78. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

79. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

80. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

81. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

82. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

83. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

84. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

85. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

86. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

87. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

88. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

89. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

90. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

91. **Write the brute-force approach for a typical 03 circular linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

92. **State the time and space complexity of the optimal solution for most 03 circular linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

93. **What common edge cases must be handled in 03 circular linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

94. **How would you dry-run your 03 circular linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

95. **Give a real-world analogy for 03 circular linked list. Extend your answer with a second example.**
   - Analogy: 03 circular linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

96. **How do you decide between a hash map, sorting, or two pointers as tools for 03 circular linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

97. **What is the role of a prefix/suffix precomputation in 03 circular linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

98. **Explain the optimisation step you would mention after writing the naive version for 03 circular linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

99. **How is 03 circular linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

100. **What is the intuition behind the 03 circular linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

</details>