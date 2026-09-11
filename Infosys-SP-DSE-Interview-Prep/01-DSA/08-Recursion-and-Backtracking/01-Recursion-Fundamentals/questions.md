# Recursion And Backtracking — Recursion Fundamentals Interview Questions and Answers

## Q1: What is recursion?
**A:** A function solving a problem by calling itself on a smaller instance, combined with a base case that stops the chain. Every recursive problem can be written iteratively with an explicit stack.

## Q2: What are the two mandatory parts of a correct recursive function?
**A:** A base case that terminates without recursing, and a recursive case that moves toward the base. Omitting or corrupting the base case causes infinite recursion / stack overflow.

## Q3: Explain the recursion call-stack model.
**A:** Each invocation pushes a frame (parameters, locals, return address); the deepest call resolves first and unwinds — the LIFO call stack. Depth is bounded by stack memory.

## Q4: How do you find the factorial / Fibonacci recursively?
**A:** fact(n)=n*fact(n-1), fact(0)=1. fib(n)=fib(n-1)+fib(n-2), fib(0)=0, fib(1)=1 — plain recursion is O(2^n); memoisation fixes it.

## Q5: What is the recursion depth limit in Python and how do you raise it?
**A:** sys.getrecursionlimit() default ~1000. sys.setrecursionlimit(n) can raise it, but the C stack can still segfault — prefer iteration for very deep recursion.

## Q6: How do you prevent exponential blow-up in recursion (memoisation)?
**A:** Cache results per state (dict). Fibonacci becomes O(n) instead of O(2^n). Memoisation is the bridge between recursion and DP.

## Q7: Give real examples of natural recursion.
**A:** Tree traversal, quicksort/mergesort, backtracking (permutations, N-Queens), parsing nested expressions, and divide-and-conquer — all fit recursion cleanly.

## Q8: How do you convert an iterative algorithm to recursion and back?
**A:** Identify the explicit loop state and the base condition. Recursion: function(state)->call(state+1) duplicate the loop body. Iteration: replace recursion with a stack, pushing each call's parameters.

## Q9: What is tail recursion and why does Python not optimise it?
**A:** Tail recursion returns only the recursive call's result with no remaining work. CPython intentionally does not perform tail-call optimisation, so deep tail recursion still overflows.

## Q10: How do you write a recursive power function (fast power)?
**A:** pow2(x,n): n==0→1; n even→pow2(x,n//2)^2; n odd→x*pow2(x,n//2)^2. O(log n) — the divide-and-conquer exponential.

## Q11: What is a recursive helper payload pattern?
**A:** Wrap the recursion with an outer function holding a shared accumulator/visited set, so the recursive helper can mutate shared state without exposing it.

## Q12: When should you choose recursion over iteration in an interview?
**A:** When the structure is naturally recursive (trees, nested) or the state is combinatorial; otherwise iteration avoids stack limits. Defend the choice with complexity and depth constraints.

## Q13: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q14: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q15: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q16: What common edge cases must be handled in 01 recursion fundamentals implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q17: How would you dry-run your 01 recursion fundamentals code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q18: Give a real-world analogy for 01 recursion fundamentals.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q19: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q20: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q21: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q22: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q23: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q24: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q25: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q26: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q27: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q28: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q29: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q30: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q31: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q32: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q33: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q34: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q35: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q36: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q37: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q38: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q39: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q40: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q41: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q42: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q43: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q44: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q45: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q46: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q47: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q48: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q49: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q50: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q51: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q52: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q53: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q54: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q55: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q56: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q57: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q58: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q59: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q60: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q61: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q62: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q63: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q64: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q65: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q66: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q67: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q68: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q69: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q70: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q71: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q72: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q73: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q74: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q75: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q76: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q77: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q78: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q79: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q80: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q81: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q82: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q83: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q84: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q85: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q86: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q87: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q88: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q89: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q90: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q91: Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q92: How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q93: What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q94: Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q95: State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q96: What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q97: How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q98: Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.
**A:** Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q99: How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q100: What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.
