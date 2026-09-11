# 03 Tree Traversal — Trees

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **List the three DFS traversals and their order of visiting.**
   - Preorder (node,left,right), inorder (left,node,right), postorder (left,right,node). All O(n); concurrency of order tells reconstruction stories in interviews.

2. **Write the recursive inorder traversal.**
   - def inorder(n): if n is None: return; inorder(n.left); visit(n); inorder(n.right). Simple; recursive visits keep natural ordering in BSTs (sorted).

3. **Write the iterative inorder traversal using an explicit stack.**
   - Stack algorithm: push left chain; on pop, visit node, then move to right child and repeat. Avoids recursion depth limits; O(n) time, O(h) space.

4. **Write the iterative preorder traversal.**
   - An easy one: push root, then while stack: pop node, visit, push right then left (right first so left pops first). O(n).

5. **Write the iterative postorder traversal.**
   - Either two-stack (push root; pop node into result, push left,right) then reverse result — or a single-stack with lastVisited tracking. O(n).

6. **How does level-order (BFS) traversal work?**
   - Queue of nodes with levels: dequeue, visit, enqueue children. Track level by queue-size snapshot for level-wise results. O(n) time, O(w) space.

7. **How do you detect zigzag (spiral) level ordering?**
   - Queue with a direction flag; at each level, reverse collection order on odd levels. O(n).

8. **How do you compute left-view and right-view of a tree?**
   - Level-order or DFS recording the first node of each depth (left-view) / last node (right-view). O(n).

9. **How do you find bottom view / top view of a binary tree?**
   - BFS with horizontal distance (hd): keep map hd->value, updating for bottom (or first for top) at each hd. Use deque with hd tracking. O(n).

10. **What is Morris traversal and its advantage?**
   - Inorder with O(1) space using threaded pointers (temporary right links from inorder predecessor to node). Non-trivial; shows rare depth.

11. **How do you reconstruct a tree from two traversals?**
   - Inorder + preorder (or + postorder): recursively split inorder by the root taken from pre/post; ++index each level. O(n) with hash map of inorder positions.

12. **What is the iterative vs recursive DFS space tradeoff?**
   - Recursive DFS uses O(h) call-stack memory; iterative avoids stack overflow on pathological depth at the cost of explicit bookkeeping.

13. **How do you perform a perfect-level sum or average per level?**
   - Level-order with per-level accumulation (sum/count) then average; O(n).

14. **What is the intuition behind the 03 tree traversal technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

15. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

16. **State the time and space complexity of the optimal solution for most 03 tree traversal problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

17. **What common edge cases must be handled in 03 tree traversal implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

18. **How would you dry-run your 03 tree traversal code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

19. **Give a real-world analogy for 03 tree traversal.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

20. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

21. **What is the role of a prefix/suffix precomputation in 03 tree traversal?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

22. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

23. **How is 03 tree traversal asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

24. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

25. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

26. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

27. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

28. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

29. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

30. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

31. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

32. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

33. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

34. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

35. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

36. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

37. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

38. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

39. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

40. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

41. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

42. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

43. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

44. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

45. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

46. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

47. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

48. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

49. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

50. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

51. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

52. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

53. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

54. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

55. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

56. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

57. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

58. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

59. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

60. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

61. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

62. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

63. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

64. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

65. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

66. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

67. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

68. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

69. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

70. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

71. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

72. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

73. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

74. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

75. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

76. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

77. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

78. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

79. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

80. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

81. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

82. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

83. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

84. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

85. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

86. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

87. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

88. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

89. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

90. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

91. **What is the role of a prefix/suffix precomputation in 03 tree traversal? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

92. **Explain the optimisation step you would mention after writing the naive version for 03 tree traversal. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

93. **How is 03 tree traversal asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

94. **What is the intuition behind the 03 tree traversal technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

95. **Write the brute-force approach for a typical 03 tree traversal problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

96. **State the time and space complexity of the optimal solution for most 03 tree traversal problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

97. **What common edge cases must be handled in 03 tree traversal implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

98. **How would you dry-run your 03 tree traversal code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

99. **Give a real-world analogy for 03 tree traversal. Extend your answer with a second example.**
   - Analogy: 03 tree traversal is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

100. **How do you decide between a hash map, sorting, or two pointers as tools for 03 tree traversal? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

</details>