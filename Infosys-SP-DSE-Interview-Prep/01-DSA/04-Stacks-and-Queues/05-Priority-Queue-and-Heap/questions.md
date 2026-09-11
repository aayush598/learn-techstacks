# Stacks And Queues — Priority Queue And Heap Interview Questions and Answers

## Q1: Define a binary heap and its properties.
**A:** A complete binary tree stored in an array where parent ≤ children (min-heap) or ≥ (max-heap); heap[0] is the extreme. Height O(log n), operations on root path.

## Q2: State the complexity of heap operations.
**A:** Insert O(log n), extract-min/max O(log n), peek O(1), build-heap O(n) (down-heap from first non-leaf).

## Q3: How do you implement heapify (sift-down)?
**A:** Compare node with children, swap with the extreme child violating order, recurse down until heap property restored. Called on indices n/2-1..0 to build in O(n).

## Q4: What is the difference between a heap and a priority queue?
**A:** A priority queue is an interface (insert element with priority, delete the extreme); a heap is the usual array-backed implementation. Same concepts, different abstraction layers.

## Q5: How do you find the K largest elements with a heap?
**A:** Min-heap of size k: push, and when size>k pop the smallest; the heap holds the k largest. O(n log k) time, O(k) space.

## Q6: How do you merge k sorted arrays with a heap?
**A:** Push (value, listIdx, elemIdx) into a min-heap; repeatedly pop min, place in result, push next element from that list. O(N log k).

## Q7: How do you implement a median-of-stream using two heaps?
**A:** Max-heap for the lower half, min-heap for the upper; rebalance so sizes differ by ≤ 1; median is top of bigger (or average). O(log n) per number.

## Q8: How do you find the top-k frequent elements?
**A:** Counter frequencies, then a min-heap of k (keyed by frequency) or bucket sort by frequency count. O(n log k) or O(n).

## Q9: What is heap sort and its complexity?
**A:** Build max-heap then repeatedly swap root to end and heapify the shrinking prefix — O(n log n) worst, O(1) extra space, NOT stable.

## Q10: How do you implement a priority queue in Python?
**A:** heapq provides min-heap on lists; push/pop pairs of (priority, item) for custom priorities; a counter disambiguates ties. queue.PriorityQueue adds thread-safe locking.

## Q11: How do you implement a max-heap in Python?
**A:** Negate keys (heapq.min-heap with -value), or wrap entries in a class with __lt__ inverted. No dedicated max-heap exists in heapq.

## Q12: What is a 'd-ary heap' and its trade-off?
**A:** Each node has d children: faster key-decrease (O(log_d n)) but slower each child scan; used in Dijkstra optimisations for dense graphs.

## Q13: How do you find the K smallest pair sums?
**A:** Min-heap seeded with (a[0]+b[i]) for each i; pop, push next by advancing a-pointer; dedupe with visited set. O(k log k).

## Q14: What is a Fibonacci heap and why is it advanced?
**A:** Supports decrease-key O(1) amortised, used in optimised Dijkstra/Prim; complex pointer-based structure rarely required in interviews but shows depth.

## Q15: How does a heap enable Huffman coding?
**A:** Merge the two smallest-frequency symbols repeatedly using a min-heap; the tree's leaves encode variable-length optimal prefix codes. O(n log n).

## Q16: What is the intuition behind the 05 priority queue and heap technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q17: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q18: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q19: What common edge cases must be handled in 05 priority queue and heap implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q20: How would you dry-run your 05 priority queue and heap code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q21: Give a real-world analogy for 05 priority queue and heap.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q22: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q23: What is the role of a prefix/suffix precomputation in 05 priority queue and heap?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q24: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q25: How is 05 priority queue and heap asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q26: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q27: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q28: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q29: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q30: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q31: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q32: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q33: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q34: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q35: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q36: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q37: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q38: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q39: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q40: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q41: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q42: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q43: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q44: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q45: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q46: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q47: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q48: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q49: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q50: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q51: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q52: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q53: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q54: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q55: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q56: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q57: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q58: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q59: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q60: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q61: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q62: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q63: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q64: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q65: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q66: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q67: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q68: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q69: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q70: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q71: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q72: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q73: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q74: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q75: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q76: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q77: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q78: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q79: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q80: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q81: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q82: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q83: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q84: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q85: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q86: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q87: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q88: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q89: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q90: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q91: Give a real-world analogy for 05 priority queue and heap. Extend your answer with a second example.
**A:** Analogy: 05 priority queue and heap is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q92: How do you decide between a hash map, sorting, or two pointers as tools for 05 priority queue and heap? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q93: What is the role of a prefix/suffix precomputation in 05 priority queue and heap? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q94: Explain the optimisation step you would mention after writing the naive version for 05 priority queue and heap. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q95: How is 05 priority queue and heap asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q96: What is the intuition behind the 05 priority queue and heap technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q97: Write the brute-force approach for a typical 05 priority queue and heap problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q98: State the time and space complexity of the optimal solution for most 05 priority queue and heap problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q99: What common edge cases must be handled in 05 priority queue and heap implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q100: How would you dry-run your 05 priority queue and heap code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.
