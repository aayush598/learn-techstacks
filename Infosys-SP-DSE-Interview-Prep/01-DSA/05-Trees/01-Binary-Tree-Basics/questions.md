# 01 Binary Tree Basics — Trees

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a binary tree.**
   - A hierarchical data structure where each node has at most two children, conventionally labelled left and right. It has a root, and every non-root node has exactly one parent.

2. **What are the properties of a binary tree (levels, height)?**
   - Level of root = 0; height = max edges from root to leaf; a tree with n nodes has at most n-1 edges, and height can range from ~log2(n) (balanced) to n-1 (skewed).

3. **Name the basic types of binary trees.**
   - Full (each node 0 or 2 children), complete (all levels full except possibly last, filled left-to-right), perfect (all levels full), balanced (height O(log n)), and skewed.

4. **How do you count the number of nodes in a tree?**
   - Recurrence: size(node)=size(left)+size(right)+1, base node is None returns 0. O(n).

5. **How do you compute the height of a tree?**
   - height(node)=1+max(height(left),height(right)), None returns -1 (edges) or 0 (nodes) depending on convention. O(n).

6. **What is the time complexity of traversals and why?**
   - Preorder/inorder/postorder/level-order each visit every node once: O(n) time; recursion stack or explicit queue adds O(h)/O(w) space.

7. **How do you identify leaves and internal nodes?**
   - Leaf: left and right both None; internal: has at least one child. Check node.left is None and node.right is None.

8. **What is a 'skewed tree' and its traversal cost?**
   - Each node has one child; height = n-1; recursion depth hits n which can overflow the stack for large trees — an interviewer favourite edge case.

9. **Explain the recursive base-case discipline for tree functions.**
   - Always handle None first (the base case), then combine results of left/right subproblems. Every tree DFS follows this shape; forgetting the None check causes crashes.

10. **How do you check if a tree is balanced (height-balanced)?**
   - Post-order: compute heights while verifying |hl-hr|≤1 at every node; propagate -1 on violation. O(n) time.

11. **What is the diameter of a binary tree and how to compute it?**
   - Longest path between any two nodes (may pass through root). Post-order: track max(1+hl+hr) while returning height; O(n).

12. **How do you find the deepest/max-depth node?**
   - Recurrence max_depth = 1 + max(depth(left), depth(right)) — same as height. For the Node value, carry it alongside.

13. **What is the intuition behind the 01 binary tree basics technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

14. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

15. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

16. **What common edge cases must be handled in 01 binary tree basics implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

17. **How would you dry-run your 01 binary tree basics code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

18. **Give a real-world analogy for 01 binary tree basics.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

19. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

20. **What is the role of a prefix/suffix precomputation in 01 binary tree basics?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

21. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

22. **How is 01 binary tree basics asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

23. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

24. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

25. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

26. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

27. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

28. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

29. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

30. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

31. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

32. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

33. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

34. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

35. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

36. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

37. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

38. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

39. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

40. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

41. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

42. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

43. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

44. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

45. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

46. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

47. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

48. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

49. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

50. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

51. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

52. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

53. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

54. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

55. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

56. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

57. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

58. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

59. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

60. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

61. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

62. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

63. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

64. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

65. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

66. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

67. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

68. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

69. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

70. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

71. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

72. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

73. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

74. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

75. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

76. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

77. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

78. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

79. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

80. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

81. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

82. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

83. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

84. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

85. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

86. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

87. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

88. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

89. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

90. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

91. **Explain the optimisation step you would mention after writing the naive version for 01 binary tree basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

92. **How is 01 binary tree basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

93. **What is the intuition behind the 01 binary tree basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

94. **Write the brute-force approach for a typical 01 binary tree basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

95. **State the time and space complexity of the optimal solution for most 01 binary tree basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

96. **What common edge cases must be handled in 01 binary tree basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

97. **How would you dry-run your 01 binary tree basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

98. **Give a real-world analogy for 01 binary tree basics. Extend your answer with a second example.**
   - Analogy: 01 binary tree basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

99. **How do you decide between a hash map, sorting, or two pointers as tools for 01 binary tree basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

100. **What is the role of a prefix/suffix precomputation in 01 binary tree basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

</details>