# 02 Binary Search Tree — Trees

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a binary search tree (BST).**
   - A binary tree ordered so that all values in the left subtree < node < all values in the right subtree (keys distinct per convention). Supports O(log n) expected search.

2. **What is the expected vs worst-case height of a BST?**
   - Balanced: O(log n). Unbalanced insertion order (sorted input) makes it degenerate to O(n) height — the reason AVL/Red-Black trees exist.

3. **How do you search in a BST?**
   - Compare target with root; go left if smaller, right if greater; None means absent. O(h), best O(log n). Recursion or iteration both work.

4. **How do you insert into a BST?**
   - Walk like search; attach the new node at the None spot. Recursive returns the new subtree root; O(h) time.

5. **How do you delete a node from a BST? (3 cases)**
   - Leaf: remove directly. One child: replace with the child. Two children: replace value with inorder-successor (leftmost of right subtree), delete that successor. O(h).

6. **What is the inorder successor of a node?**
   - The smallest value greater than node's value: if right child exists, leftmost in that subtree; else walk ancestors until taking a left turn. O(h).

7. **How do you validate whether a tree is a BST?**
   - Pass (lo, hi) bounds down recursion: every node must satisfy lo<val<hi. Do NOT just compare at children. O(n).

8. **How do you convert a sorted array to a balanced BST?**
   - Pick the middle element as root, recurse on left/right halves; yields a balanced tree O(n). This is a classic SP/DSE question.

9. **What is the Kth smallest element in a BST?**
   - Inorder traversal produces sorted order; the Kth visited element is the answer — iterative stack for O(h+k). Or augment nodes with subtree sizes for O(h).

10. **What does the TreeMap analogy imply in the Infosys question?**
   - In Java, TreeMap is a red-black BST: operations O(log n), sorted iteration, comparison-based. HashMap is O(1) average but unordered — that is the exact 'HashMap vs TreeMap' answer.

11. **How do you find the lowest common ancestor in a BST?**
   - Walk from root: if p,q both smaller go left; both larger go right; otherwise current is the LCA. O(h).

12. **How do you compute the sum/range queries on BST values?**
   - Range sum [lo,hi]: recursive pruning — go left only if val>lo, right only if val<hi, include node if in range. O(h + nodes touched).

13. **What is the 'two nodes swapped' BST recovery problem?**
   - Inorder traversal to detect two out-of-order neighbours (one violation possibly two) and swap their values to restore the BST. O(n).

14. **How do you make a BST from preorder traversal?**
   - Stack-based construction using the strictly-increasing upper bounds (or recurse with bounds across preorder indices). O(n).

15. **What is the difference between a BST and a heap?**
   - BST orders left<root<right (searchable), heap orders parent vs children extreme only (extreme-fast, no general search). BST supports order statistics; heaps support extreme queries.

16. **What is the intuition behind the 02 binary search tree technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

17. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

18. **State the time and space complexity of the optimal solution for most 02 binary search tree problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

19. **What common edge cases must be handled in 02 binary search tree implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

20. **How would you dry-run your 02 binary search tree code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

21. **Give a real-world analogy for 02 binary search tree.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

22. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

23. **What is the role of a prefix/suffix precomputation in 02 binary search tree?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

24. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

25. **How is 02 binary search tree asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

26. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

27. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

28. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

29. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

30. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

31. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

32. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

33. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

34. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

35. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

36. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

37. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

38. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

39. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

40. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

41. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

42. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

43. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

44. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

45. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

46. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

47. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

48. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

49. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

50. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

51. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

52. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

53. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

54. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

55. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

56. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

57. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

58. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

59. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

60. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

61. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

62. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

63. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

64. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

65. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

66. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

67. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

68. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

69. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

70. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

71. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

72. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

73. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

74. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

75. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

76. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

77. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

78. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

79. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

80. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

81. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

82. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

83. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

84. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

85. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

86. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

87. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

88. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

89. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

90. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

91. **Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.**
   - Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

92. **How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

93. **What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

94. **Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

95. **How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

96. **What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

97. **Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

98. **State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

99. **What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

100. **How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

</details>