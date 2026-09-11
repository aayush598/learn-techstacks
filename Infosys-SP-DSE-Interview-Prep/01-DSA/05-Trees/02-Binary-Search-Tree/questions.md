# Trees — Binary Search Tree Interview Questions and Answers

## Q1: Define a binary search tree (BST).
**A:** A binary tree ordered so that all values in the left subtree < node < all values in the right subtree (keys distinct per convention). Supports O(log n) expected search.

## Q2: What is the expected vs worst-case height of a BST?
**A:** Balanced: O(log n). Unbalanced insertion order (sorted input) makes it degenerate to O(n) height — the reason AVL/Red-Black trees exist.

## Q3: How do you search in a BST?
**A:** Compare target with root; go left if smaller, right if greater; None means absent. O(h), best O(log n). Recursion or iteration both work.

## Q4: How do you insert into a BST?
**A:** Walk like search; attach the new node at the None spot. Recursive returns the new subtree root; O(h) time.

## Q5: How do you delete a node from a BST? (3 cases)
**A:** Leaf: remove directly. One child: replace with the child. Two children: replace value with inorder-successor (leftmost of right subtree), delete that successor. O(h).

## Q6: What is the inorder successor of a node?
**A:** The smallest value greater than node's value: if right child exists, leftmost in that subtree; else walk ancestors until taking a left turn. O(h).

## Q7: How do you validate whether a tree is a BST?
**A:** Pass (lo, hi) bounds down recursion: every node must satisfy lo<val<hi. Do NOT just compare at children. O(n).

## Q8: How do you convert a sorted array to a balanced BST?
**A:** Pick the middle element as root, recurse on left/right halves; yields a balanced tree O(n). This is a classic SP/DSE question.

## Q9: What is the Kth smallest element in a BST?
**A:** Inorder traversal produces sorted order; the Kth visited element is the answer — iterative stack for O(h+k). Or augment nodes with subtree sizes for O(h).

## Q10: What does the TreeMap analogy imply in the Infosys question?
**A:** In Java, TreeMap is a red-black BST: operations O(log n), sorted iteration, comparison-based. HashMap is O(1) average but unordered — that is the exact 'HashMap vs TreeMap' answer.

## Q11: How do you find the lowest common ancestor in a BST?
**A:** Walk from root: if p,q both smaller go left; both larger go right; otherwise current is the LCA. O(h).

## Q12: How do you compute the sum/range queries on BST values?
**A:** Range sum [lo,hi]: recursive pruning — go left only if val>lo, right only if val<hi, include node if in range. O(h + nodes touched).

## Q13: What is the 'two nodes swapped' BST recovery problem?
**A:** Inorder traversal to detect two out-of-order neighbours (one violation possibly two) and swap their values to restore the BST. O(n).

## Q14: How do you make a BST from preorder traversal?
**A:** Stack-based construction using the strictly-increasing upper bounds (or recurse with bounds across preorder indices). O(n).

## Q15: What is the difference between a BST and a heap?
**A:** BST orders left<root<right (searchable), heap orders parent vs children extreme only (extreme-fast, no general search). BST supports order statistics; heaps support extreme queries.

## Q16: What is the intuition behind the 02 binary search tree technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q17: Write the brute-force approach for a typical 02 binary search tree problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q18: State the time and space complexity of the optimal solution for most 02 binary search tree problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q19: What common edge cases must be handled in 02 binary search tree implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q20: How would you dry-run your 02 binary search tree code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q21: Give a real-world analogy for 02 binary search tree.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q22: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q23: What is the role of a prefix/suffix precomputation in 02 binary search tree?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q24: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q25: How is 02 binary search tree asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q26: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q27: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q28: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q29: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q30: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q31: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q32: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q33: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q34: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q35: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q36: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q37: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q38: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q39: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q40: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q41: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q42: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q43: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q44: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q45: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q46: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q47: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q48: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q49: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q50: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q51: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q52: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q53: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q54: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q55: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q56: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q57: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q58: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q59: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q60: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q61: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q62: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q63: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q64: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q65: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q66: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q67: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q68: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q69: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q70: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q71: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q72: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q73: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q74: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q75: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q76: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q77: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q78: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q79: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q80: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q81: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q82: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q83: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q84: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q85: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q86: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q87: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q88: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q89: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q90: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q91: Give a real-world analogy for 02 binary search tree. Extend your answer with a second example.
**A:** Analogy: 02 binary search tree is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q92: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search tree? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q93: What is the role of a prefix/suffix precomputation in 02 binary search tree? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q94: Explain the optimisation step you would mention after writing the naive version for 02 binary search tree. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q95: How is 02 binary search tree asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q96: What is the intuition behind the 02 binary search tree technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q97: Write the brute-force approach for a typical 02 binary search tree problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q98: State the time and space complexity of the optimal solution for most 02 binary search tree problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q99: What common edge cases must be handled in 02 binary search tree implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q100: How would you dry-run your 02 binary search tree code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.
