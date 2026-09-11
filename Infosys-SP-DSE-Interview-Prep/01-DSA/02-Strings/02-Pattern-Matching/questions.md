# 02 Pattern Matching — Strings

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What is string pattern matching and when do naive checks fail?**
   - Finding a pattern P in text T. Naive tries P at every position costing O(n*m); it degrades badly on repetitive text. Advanced algorithms (KMP/Rabin-Karp/Z) run O(n+m).

2. **Explain the KMP failure function conceptually.**
   - lps[i] = length of the longest proper prefix of P[0..i] that is also a suffix. On mismatch, instead of restarting, the algorithm resumes from lps[prev] — each char is processed O(1).

3. **State KMP time and space complexity.**
   - O(n+m) time and O(m) space for the lps array; it is the canonical optimal single-pattern matcher.

4. **Explain Rabin-Karp rolling hash and collision handling.**
   - Hash a window using base + modulo; slide by removing outbound char and adding inbound. On hash match, verify with direct compare to guard collisions; average O(n+m).

5. **What is Z-array and how is it computed in linear time?**
   - Z[i] is the longest substring starting at i matching the prefix. Maintain [L,R] box; reuse internal comparisons. Compose as P+'#'+T, pattern found where Z[i] == len(P).

6. **When would you prefer Boyer-Moore in a real system?**
   - Boyer-Moore skips ahead using bad-character and good-suffix heuristics, excelling on large alphabets and long text; used in grep-like search engines for patterns.

7. **How do you implement wildcard matching (* and ?)?**
   - DP over (i,j): '?' matches one char, '*' matches empty or any sequence (dp[i][j]=dp[i-1][j] or dp[i][j-1]). Greedy two-pointer version also exists. O(n*m) time.

8. **How do you implement regular expression matching supporting '.' and '*'?**
   - DP with states (i,j): '.' matches any char; 'x*' can match zero (dp[i][j-2]) or more copies. O(n*m). This exact problem frequently enters SP/DSE coding tests.

9. **How do you find all occurrences of a pattern?**
   - Run KMP and record every index where j == m (then j=lps[j-1] to allow overlaps). Rabin-Karp records hash matches after verification.

10. **Explain string hashing and why collisions matter.**
   - Hash text windows to compare prefix equality in O(1); collisions make the algorithm incorrect unless verified, so use double hashes or check equality directly.

11. **How would you count distinct substrings of a string?**
   - Suffix array + LCP: total = n(n+1)/2 - sum(LCP). Or a trie of all suffixes. O(n^2) worst on trie; suffix-array sort gives O(n log n).

12. **What is the suffix automaton and its advantage?**
   - A minimal DFA accepting all substrings of a string. Built in O(n) with 2n states; answers substring-presence and occurrences in O(1)/O(occ).

13. **What is the intuition behind the 02 pattern matching technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

14. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

15. **State the time and space complexity of the optimal solution for most 02 pattern matching problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

16. **What common edge cases must be handled in 02 pattern matching implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

17. **How would you dry-run your 02 pattern matching code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

18. **Give a real-world analogy for 02 pattern matching.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

19. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

20. **What is the role of a prefix/suffix precomputation in 02 pattern matching?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

21. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

22. **How is 02 pattern matching asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

23. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

24. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

25. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

26. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

27. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

28. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

29. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

30. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

31. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

32. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

33. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

34. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

35. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

36. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

37. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

38. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

39. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

40. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

41. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

42. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

43. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

44. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

45. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

46. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

47. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

48. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

49. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

50. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

51. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

52. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

53. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

54. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

55. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

56. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

57. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

58. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

59. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

60. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

61. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

62. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

63. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

64. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

65. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

66. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

67. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

68. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

69. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

70. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

71. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

72. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

73. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

74. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

75. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

76. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

77. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

78. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

79. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

80. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

81. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

82. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

83. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

84. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

85. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

86. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

87. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

88. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

89. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

90. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

91. **Explain the optimisation step you would mention after writing the naive version for 02 pattern matching. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

92. **How is 02 pattern matching asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

93. **What is the intuition behind the 02 pattern matching technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

94. **Write the brute-force approach for a typical 02 pattern matching problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

95. **State the time and space complexity of the optimal solution for most 02 pattern matching problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

96. **What common edge cases must be handled in 02 pattern matching implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

97. **How would you dry-run your 02 pattern matching code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

98. **Give a real-world analogy for 02 pattern matching. Extend your answer with a second example.**
   - Analogy: 02 pattern matching is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

99. **How do you decide between a hash map, sorting, or two pointers as tools for 02 pattern matching? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

100. **What is the role of a prefix/suffix precomputation in 02 pattern matching? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

</details>