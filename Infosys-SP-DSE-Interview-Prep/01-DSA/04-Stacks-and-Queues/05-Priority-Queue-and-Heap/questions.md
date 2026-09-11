# 05 Priority Queue And Heap — Stacks / And / Queues

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a binary heap and its properties.**
   - A complete binary tree stored in an array where parent ≤ children (min-heap) or ≥ (max-heap); heap[0] is the extreme. Height O(log n), operations on root path.

2. **State the complexity of heap operations.**
   - Insert O(log n), extract-min/max O(log n), peek O(1), build-heap O(n) (down-heap from first non-leaf).

3. **How do you implement heapify (sift-down)?**
   - Compare node with children, swap with the extreme child violating order, recurse down until heap property restored. Called on indices n/2-1..0 to build in O(n).

4. **What is the difference between a heap and a priority queue?**
   - A priority queue is an interface (insert element with priority, delete the extreme); a heap is the usual array-backed implementation. Same concepts, different abstraction layers.

5. **How do you find the K largest elements with a heap?**
   - Min-heap of size k: push, and when size>k pop the smallest; the heap holds the k largest. O(n log k) time, O(k) space.

6. **How do you merge k sorted arrays with a heap?**
   - Push (value, listIdx, elemIdx) into a min-heap; repeatedly pop min, place in result, push next element from that list. O(N log k).

7. **How do you implement a median-of-stream using two heaps?**
   - Max-heap for the lower half, min-heap for the upper; rebalance so sizes differ by ≤ 1; median is top of bigger (or average). O(log n) per number.

8. **How do you find the top-k frequent elements?**
   - Counter frequencies, then a min-heap of k (keyed by frequency) or bucket sort by frequency count. O(n log k) or O(n).

9. **What is heap sort and its complexity?**
   - Build max-heap then repeatedly swap root to end and heapify the shrinking prefix — O(n log n) worst, O(1) extra space, NOT stable.

10. **How do you implement a priority queue in Python?**
   - heapq provides min-heap on lists; push/pop pairs of (priority, item) for custom priorities; a counter disambiguates ties. queue.PriorityQueue adds thread-safe locking.

11. **How do you implement a max-heap in Python?**
   - Negate keys (heapq.min-heap with -value), or wrap entries in a class with __lt__ inverted. No dedicated max-heap exists in heapq.

12. **What is a 'd-ary heap' and its trade-off?**
   - Each node has d children: faster key-decrease (O(log_d n)) but slower each child scan; used in Dijkstra optimisations for dense graphs.

13. **How do you find the K smallest pair sums?**
   - Min-heap seeded with (a[0]+b[i]) for each i; pop, push next by advancing a-pointer; dedupe with visited set. O(k log k).

14. **What is a Fibonacci heap and why is it advanced?**
   - Supports decrease-key O(1) amortised, used in optimised Dijkstra/Prim; complex pointer-based structure rarely required in interviews but shows depth.

15. **How does a heap enable Huffman coding?**
   - Merge the two smallest-frequency symbols repeatedly using a min-heap; the tree's leaves encode variable-length optimal prefix codes. O(n log n).

16. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

17. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

18. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

19. **What common edge cases must be handled in 05 priority queue and heap implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

20. **How would you dry-run your 05 priority queue and heap code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

21. **Give a real-world analogy for 05 priority queue and heap.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

22. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

23. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

24. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

25. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

26. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

27. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

28. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

29. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

30. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

31. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

32. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

33. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

34. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

35. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

36. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

37. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

38. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

39. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

40. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

41. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

42. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

43. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

44. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

45. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

46. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

47. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

48. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

49. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

50. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

51. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

52. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

53. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

54. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

55. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

56. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

57. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

58. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

59. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

60. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

61. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

62. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

63. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

64. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

65. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

66. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

67. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

68. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

69. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

70. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

71. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

72. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

73. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

74. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

75. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

76. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

77. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

78. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

79. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

80. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

81. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

82. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

83. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

84. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

85. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

86. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

87. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

88. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

89. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

90. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

91. **Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.**
   - Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

92. **How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

93. **What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

94. **Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

95. **How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

96. **What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

97. **Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

98. **State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

99. **What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

100. **How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

</details>