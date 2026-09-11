# 01 Recursion Fundamentals — Recursion / And / Backtracking

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What is recursion?**
   - A function solving a problem by calling itself on a smaller instance, combined with a base case that stops the chain. Every recursive problem can be written iteratively with an explicit stack.

2. **What are the two mandatory parts of a correct recursive function?**
   - A base case that terminates without recursing, and a recursive case that moves toward the base. Omitting or corrupting the base case causes infinite recursion / stack overflow.

3. **Explain the recursion call-stack model.**
   - Each invocation pushes a frame (parameters, locals, return address); the deepest call resolves first and unwinds — the LIFO call stack. Depth is bounded by stack memory.

4. **How do you find the factorial / Fibonacci recursively?**
   - fact(n)=n*fact(n-1), fact(0)=1. fib(n)=fib(n-1)+fib(n-2), fib(0)=0, fib(1)=1 — plain recursion is O(2^n); memoisation fixes it.

5. **What is the recursion depth limit in Python and how do you raise it?**
   - sys.getrecursionlimit() default ~1000. sys.setrecursionlimit(n) can raise it, but the C stack can still segfault — prefer iteration for very deep recursion.

6. **How do you prevent exponential blow-up in recursion (memoisation)?**
   - Cache results per state (dict). Fibonacci becomes O(n) instead of O(2^n). Memoisation is the bridge between recursion and DP.

7. **Give real examples of natural recursion.**
   - Tree traversal, quicksort/mergesort, backtracking (permutations, N-Queens), parsing nested expressions, and divide-and-conquer — all fit recursion cleanly.

8. **How do you convert an iterative algorithm to recursion and back?**
   - Identify the explicit loop state and the base condition. Recursion: function(state)->call(state+1) duplicate the loop body. Iteration: replace recursion with a stack, pushing each call's parameters.

9. **What is tail recursion and why does Python not optimise it?**
   - Tail recursion returns only the recursive call's result with no remaining work. CPython intentionally does not perform tail-call optimisation, so deep tail recursion still overflows.

10. **How do you write a recursive power function (fast power)?**
   - pow2(x,n): n==0→1; n even→pow2(x,n//2)^2; n odd→x*pow2(x,n//2)^2. O(log n) — the divide-and-conquer exponential.

11. **What is a recursive helper payload pattern?**
   - Wrap the recursion with an outer function holding a shared accumulator/visited set, so the recursive helper can mutate shared state without exposing it.

12. **When should you choose recursion over iteration in an interview?**
   - When the structure is naturally recursive (trees, nested) or the state is combinatorial; otherwise iteration avoids stack limits. Defend the choice with complexity and depth constraints.

13. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

14. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

15. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

16. **What common edge cases must be handled in 01 recursion fundamentals implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

17. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

18. **Give a real-world analogy for 01 recursion fundamentals.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

19. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

20. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

21. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

22. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

23. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

24. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

25. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

26. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

27. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

28. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

29. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

30. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

31. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

32. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

33. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

34. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

35. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

36. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

37. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

38. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

39. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

40. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

41. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

42. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

43. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

44. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

45. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

46. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

47. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

48. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

49. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

50. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

51. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

52. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

53. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

54. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

55. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

56. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

57. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

58. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

59. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

60. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

61. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

62. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

63. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

64. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

65. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

66. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

67. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

68. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

69. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

70. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

71. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

72. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

73. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

74. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

75. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

76. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

77. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

78. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

79. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

80. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

81. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

82. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

83. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

84. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

85. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

86. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

87. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

88. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

89. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

90. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

91. **Explain the optimisation step you would mention after writing the naive version for 01 recursion fundamentals. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

92. **How is 01 recursion fundamentals asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

93. **What is the intuition behind the 01 recursion fundamentals technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

94. **Write the brute-force approach for a typical 01 recursion fundamentals problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

95. **State the time and space complexity of the optimal solution for most 01 recursion fundamentals problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

96. **What common edge cases must be handled in 01 recursion fundamentals implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

97. **How would you dry-run your 01 recursion fundamentals code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

98. **Give a real-world analogy for 01 recursion fundamentals. Extend your answer with a second example.**
   - Analogy: 01 recursion fundamentals is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

99. **How do you decide between a hash map, sorting, or two pointers as tools for 01 recursion fundamentals? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

100. **What is the role of a prefix/suffix precomputation in 01 recursion fundamentals? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

</details>