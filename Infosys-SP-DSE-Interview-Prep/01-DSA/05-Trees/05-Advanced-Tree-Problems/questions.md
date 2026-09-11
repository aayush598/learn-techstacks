# Trees — Advanced Tree Problems Interview Questions and Answers

## Q1: How do you find the maximum path sum in a binary tree?
**A:** Post-order returning max 'arm' (node + best single child path) while tracking global max including both children: candidate = node + leftarm + rightarm. O(n).

## Q2: How do you check if two trees are symmetric / mirror?
**A:** Recursive check that left.left mirrors right.right and left.right mirrors right.left with equal values; None on both sides is the base. O(n).

## Q3: How do you check if a tree is a subtree of another?
**A:** DFS on main tree checking isSameTree for each candidate root, with null-safe comparisons. O(m*n) naive; KMP on serialised traversal improves to O(m+n).

## Q4: How do you flatten a binary tree into a linked list (preorder)?
**A:** Morris-like: for each node, connect inorder predecessor's right to current.right, move left to right. O(n) time O(1) extra space.

## Q5: How do you find the kth largest element in a BST?
**A:** Reverse-inorder (right,node,left) counting to k, or subtree-size augmentation. O(h+k).

## Q6: How do you find the closest value to a target in a BST?
**A:** Walk left/right based on comparison, tracking best at each node. Closest = minimum absolute difference. O(h).

## Q7: How do you find the lowest common ancestor in a binary tree (not BST)?
**A:** DFS: if root None or matches p/q return root; else collect left/right LCA results; if both non-None current is LCA, else return the non-None side. O(n).

## Q8: How do you count nodes in a complete binary tree faster than O(n)?
**A:** Use the height property: if left and right heights equal, left subtree is perfect (2^h - 1); else recurse on right and imperfect side. O(log^2 n).

## Q9: How do you find the boundary traversal of a tree?
**A:** Left boundary (excluding leaf), then leaves (inorder order), then right boundary reversed. Avoid duplicate corner nodes. O(n).

## Q10: How do you verify identical trees?
**A:** Compare both None (equal), one None (not equal), values equal, then recurse on left and right simultaneously. O(n).

## Q11: What is the 'binary tree maximum width' problem?
**A:** Treat tree as heap-indices array; BFS tracking index = 2*i, 2*i+1; width = last - first + 1 per level. Watch overflow with huge indices — use relative indices.

## Q12: How do you find all root-to-leaf paths?
**A:** DFS with path list; when leaf reached, copy the path to results; backtrack on return. O(n * path copies).

## Q13: What is the 'sum of root-to-leaf numbers' problem?
**A:** DFS carrying cur = cur*10 + val at each node; at a leaf, add to total. Standard recursion test. O(n).

## Q14: How do you convert a binary tree to its mirror?
**A:** Swap left/right children recursively (post-order swap); the tree becomes its mirror in place. O(n).

## Q15: How do you find a node's inorder successor with parent pointers?
**A:** If right child exists: leftmost of right subtree; else climb until coming from a left child (node == parent.left). O(h).

## Q16: What is the intuition behind the 05 advanced tree problems technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q17: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q18: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q19: What common edge cases must be handled in 05 advanced tree problems implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q20: How would you dry-run your 05 advanced tree problems code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q21: Give a real-world analogy for 05 advanced tree problems.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q22: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q23: What is the role of a prefix/suffix precomputation in 05 advanced tree problems?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q24: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q25: How is 05 advanced tree problems asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q26: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q27: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q28: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q29: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q30: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q31: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q32: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q33: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q34: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q35: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q36: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q37: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q38: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q39: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q40: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q41: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q42: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q43: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q44: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q45: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q46: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q47: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q48: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q49: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q50: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q51: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q52: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q53: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q54: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q55: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q56: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q57: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q58: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q59: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q60: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q61: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q62: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q63: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q64: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q65: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q66: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q67: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q68: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q69: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q70: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q71: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q72: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q73: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q74: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q75: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q76: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q77: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q78: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q79: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q80: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q81: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q82: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q83: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q84: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q85: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q86: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q87: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q88: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q89: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q90: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q91: Give a real-world analogy for 05 advanced tree problems. Extend your answer with a second example.
**A:** Analogy: 05 advanced tree problems is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q92: How do you decide between a hash map, sorting, or two pointers as tools for 05 advanced tree problems? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q93: What is the role of a prefix/suffix precomputation in 05 advanced tree problems? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q94: Explain the optimisation step you would mention after writing the naive version for 05 advanced tree problems. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q95: How is 05 advanced tree problems asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q96: What is the intuition behind the 05 advanced tree problems technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q97: Write the brute-force approach for a typical 05 advanced tree problems problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q98: State the time and space complexity of the optimal solution for most 05 advanced tree problems problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q99: What common edge cases must be handled in 05 advanced tree problems implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q100: How would you dry-run your 05 advanced tree problems code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.
