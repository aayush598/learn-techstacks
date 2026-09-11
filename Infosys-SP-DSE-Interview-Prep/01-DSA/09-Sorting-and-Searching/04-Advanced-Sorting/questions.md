# Sorting And Searching — Advanced Sorting Interview Questions and Answers

## Q1: What is the '3-way quicksort' variant?
**A:** Dutch-flag partition splits into <, ==, > pivot groups, recursing only on < and >. Linear for many duplicates — a great optimisation answer.

## Q2: How do you find the kth smallest with quickselect?
**A:** Partition like quicksort; recur into the side containing k. Average O(n), worst O(n^2); introselect mixes medians for worst-case guarantee.

## Q3: What is the 'sort permutation with inversions count' phrase?
**A:** Counting inversions = number of pairs out of order; solved by merge-sort counting, or Fenwick/order-statistics. O(n log n) is the optimal comparison bound.

## Q4: How do you sort very large files (external sort)?
**A:** Split into runs that fit RAM, sort each, then k-way merge with a heap; I/O-bound so block size and buffering matter. The heap-merge is the crux.

## Q5: How does the phrase 'stable sort of tuples by second then first' work?
**A:** Sort by the least significant key first, then by the more significant (stable merge/insert) so equal ties preserve the earlier key order — used in radix-land.

## Q6: What is topological 'sorted order' via Kahn when multiple valid orders?
**A:** If a specific (e.g., lexicographic) order is needed, replace the plain queue with a min-heap of zeros — 'smallest latinum edges first'.

## Q7: How do you sort a nearly-sorted list in O(n log k)?
**A:** k-size min-heap scanning; pop-min into output, push next where i+k in range. O(n log k) with k the max displacement.

## Q8: What is a 'stable bucket/insertion for floats'?
**A:** Scale floats via bucket ranges; each bucket sorted by insertion; concatenation preserves global order — the classic float-bucket-sort.

## Q9: How do you implement an in-place merge without sacrificing asymptotics?
**A:** Use in-place rotational merges (block merge / timsort's galloping) — the classic boundary-then-inplace trick, or accept the stable O(n) space when simpler.

## Q10: How do you know sorting is the right pre-processing in a problem?
**A:** When the problem benefits from adjacency comparisons, two-pointer merging, or binary search — sorting (O(n log n)) unlocks those; always mention the trade-off.

## Q11: What is the intuition behind the 04 advanced sorting technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q12: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q13: State the time and space complexity of the optimal solution for most 04 advanced sorting problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q14: What common edge cases must be handled in 04 advanced sorting implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q15: How would you dry-run your 04 advanced sorting code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q16: Give a real-world analogy for 04 advanced sorting.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q17: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q18: What is the role of a prefix/suffix precomputation in 04 advanced sorting?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q19: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q20: How is 04 advanced sorting asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q21: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q22: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q23: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q24: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q25: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q26: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q27: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q28: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q29: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q30: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q31: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q32: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q33: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q34: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q35: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q36: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q37: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q38: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q39: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q40: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q41: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q42: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q43: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q44: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q45: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q46: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q47: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q48: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q49: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q50: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q51: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q52: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q53: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q54: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q55: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q56: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q57: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q58: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q59: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q60: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q61: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q62: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q63: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q64: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q65: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q66: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q67: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q68: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q69: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q70: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q71: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q72: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q73: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q74: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q75: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q76: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q77: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q78: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q79: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q80: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q81: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q82: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q83: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q84: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q85: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q86: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q87: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q88: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q89: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q90: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q91: What is the intuition behind the 04 advanced sorting technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q92: Write the brute-force approach for a typical 04 advanced sorting problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q93: State the time and space complexity of the optimal solution for most 04 advanced sorting problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q94: What common edge cases must be handled in 04 advanced sorting implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q95: How would you dry-run your 04 advanced sorting code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q96: Give a real-world analogy for 04 advanced sorting. Extend your answer with a second example.
**A:** Analogy: 04 advanced sorting is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q97: How do you decide between a hash map, sorting, or two pointers as tools for 04 advanced sorting? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q98: What is the role of a prefix/suffix precomputation in 04 advanced sorting? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q99: Explain the optimisation step you would mention after writing the naive version for 04 advanced sorting. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q100: How is 04 advanced sorting asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.
