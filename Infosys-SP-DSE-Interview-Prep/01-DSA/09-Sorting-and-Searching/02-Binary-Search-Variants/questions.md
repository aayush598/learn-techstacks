# Sorting And Searching — Binary Search Variants Interview Questions and Answers

## Q1: Explain classic binary search and its complexity.
**A:** On a sorted array, repeatedly halve the range comparing mid. O(log n) time, O(1) space — the textbook example of logarithmic search.

## Q2: When can binary search be used beyond arrays?
**A:** On any monotonic predicate: answer-space binary search (search on answer), rotated arrays, floating-point search, and 'first/last true' boundaries.

## Q3: How do you find the first and last occurrence of target?
**A:** Binary search with equality handling: first occurrence keeps moving right on equal; last moves left on equal — or use bisect_left/bisect_right. O(log n) each.

## Q4: How do you search in a rotated sorted array?
**A:** Compare mid with the low pointer to identify the sorted half, check if target lies in it, then walk the half. Handles duplicates with high-- fallback. O(log n) typical.

## Q5: How do you find the rotation point (min element)?
**A:** If arr[mid] > arr[high] the pivot is in the right half, else the left — a modified binary search. For duplicates, shrink boundary carefully. O(log n).

## Q6: What is binary search on answer?
**A:** When the answer is numeric and feasible(x) is monotone, binary search the answer space: e.g., kth smallest, minimum max-speed to within deadline. O(log(range)·cost(feas)).

## Q7: How do you find the square root (integer and floating precision)?
**A:** Binary search the answer: lo=0, hi=n; while feasible(hi-lo)>eps, mid; ans = greatest m*m<=n. Floating version uses epsilon. O(log n).

## Q8: How do you find the kth smallest pair distance?
**A:** Sort, binary search the distance answer, count pairs with distance <= x via a two-pointer counter — the count is monotonic in x. O(n log MAX).

## Q9: What is the 'ship within D days', 'koko bananas', 'minimum capacity' family?
**A:** Binary search the capacity (answer); check feasibility by greedy simulation; because capacity-monotonic, binary search works — SUPER popular in SP/DSE rounds.

## Q10: How do you search in a 2D sorted matrix (rows and cols sorted)?
**A:** Start at top-right; move left if target < cell, down if >. O(n+m). Or treat as flattened sorted if row-major fully sorted — then plain binary search.

## Q11: How do you find a peak in a bitonic array?
**A:** Compare mid with mid+1; rising→peak to the right, falling→left. The bitonic-peak binary search = variant of monotone peak in arrays. O(log n).

## Q12: How do you find the inserted position (lower_bound)?
**A:** bisect_left returns the first index where x could be inserted to keep order; bisect_right the last. These are your O(log n) building blocks in Python.

## Q13: How do you handle duplicates correctly in rotated search?
**A:** When arr[low]==arr[mid]==arr[high], we can't decide the side; decrement high and continue — worst-case O(n) but averages O(log n).

## Q14: What are integer-overflow-safe binary search midpoints?
**A:** mid = lo + (hi-lo)//2 avoids lo+hi overflow in languages with fixed ints (C++/Java). Python ints don't suffer it, but state the practice anyway.

## Q15: How do you check if binary search replaces a linear scan in interviews?
**A:** Whenever the problem asks for min/max/given a bound with a monotonic checker, or sorted arrays, reach for binary search and justify O(log n) over O(n).

## Q16: What is the intuition behind the 02 binary search variants technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q17: Write the brute-force approach for a typical 02 binary search variants problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q18: State the time and space complexity of the optimal solution for most 02 binary search variants problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q19: What common edge cases must be handled in 02 binary search variants implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q20: How would you dry-run your 02 binary search variants code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q21: Give a real-world analogy for 02 binary search variants.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q22: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q23: What is the role of a prefix/suffix precomputation in 02 binary search variants?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q24: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q25: How is 02 binary search variants asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q26: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q27: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q28: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q29: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q30: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q31: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q32: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q33: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q34: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q35: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q36: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q37: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q38: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q39: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q40: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q41: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q42: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q43: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q44: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q45: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q46: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q47: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q48: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q49: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q50: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q51: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q52: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q53: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q54: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q55: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q56: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q57: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q58: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q59: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q60: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q61: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q62: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q63: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q64: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q65: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q66: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q67: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q68: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q69: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q70: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q71: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q72: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q73: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q74: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q75: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q76: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q77: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q78: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q79: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q80: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q81: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q82: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q83: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q84: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q85: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q86: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q87: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q88: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q89: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q90: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q91: Give a real-world analogy for 02 binary search variants. Extend your answer with a second example.
**A:** Analogy: 02 binary search variants is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q92: How do you decide between a hash map, sorting, or two pointers as tools for 02 binary search variants? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q93: What is the role of a prefix/suffix precomputation in 02 binary search variants? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q94: Explain the optimisation step you would mention after writing the naive version for 02 binary search variants. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q95: How is 02 binary search variants asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q96: What is the intuition behind the 02 binary search variants technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q97: Write the brute-force approach for a typical 02 binary search variants problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q98: State the time and space complexity of the optimal solution for most 02 binary search variants problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q99: What common edge cases must be handled in 02 binary search variants implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q100: How would you dry-run your 02 binary search variants code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.
