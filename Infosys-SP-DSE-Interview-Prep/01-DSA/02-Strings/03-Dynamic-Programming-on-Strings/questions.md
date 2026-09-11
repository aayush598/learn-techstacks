# 03 Dynamic Programming On Strings — Strings

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Overview of DP on strings and standard state design.**
   - State is typically (i,j) = position in string A and string B. Transitions come from char match/mismatch, gap, or replace choices — forming LCS, edit-distance, palindromes and interleaving problems.

2. **How is Longest Common Subsequence defined and solved?**
   - LCS keeps order without adjacency. Recurrence: if a[i]==b[j]: dp[i][j]=dp[i-1][j-1]+1 else max of dp[i-1][j], dp[i][j-1]. O(n*m) DP; reconstruct by backtracking.

3. **Explain edit distance (Levenshtein).**
   - Min ops (insert/delete/replace) to turn a into b. dp[i][j]=min(insert, delete, replace). If chars equal, carry dp[i-1][j-1]. O(n*m).

4. **How do you find the longest palindromic subsequence?**
   - LCS of s with reversed(s), or DP palindrome recurrence: if s[i]==s[j]: dp[i][j]=dp[i+1][j-1]+2 else max(dp[i+1][j],dp[i][j-1]). Fill by increasing length.

5. **How do you find the minimum insertions to make a string a palindrome?**
   - Insertions needed = len(s) - longest_palindromic_subsequence(s). The complement of already-matching characters is what must be added symmetrically.

6. **How do you check if a string is an interleaving of two others?**
   - dp[i][j] True if s3[0:i+j] is an interleaving of s1[0:i] and s2[0:j]; transitions consume from s1 or s2 when chars match s3. O(n*m).

7. **What is a substring edit-distance variant (segment change)?**
   - Common variants restrict operations (e.g., only delete), early-exit when distance>k, or ask for distinct edits — adapt states accordingly and add pruning.

8. **How do you compute edit distance with O(m) space?**
   - Roll dp arrays: only two rows are needed because transitions reference i-1 row only. From row to row, keep prev and current. O(n*m) time, O(m) space.

9. **How does the 'delete operation for two strings' problem work?**
   - Min deletions to make s and t equal = n + m - 2*LCS(s,t). Only delete operations allowed means unchanged parts are exactly the common subsequence.

10. **How do you find the longest common substring?**
   - DP where dp[i][j]=dp[i-1][j-1]+1 only when chars match (reset on mismatch). Keep global max. O(n*m) time; suffix array gives O(n log n).

11. **How do you build all distinct LCS (or DP backtracking) answers?**
   - Backtrack through equal-value transitions collecting paths; dedupe with a set. Exponential worst-case output, so report count or all with memoised sets.

12. **What is the shortest common supersequence problem?**
   - SCS(a,b) length = n+m-LCS(a,b). Reconstruction merges a and b avoiding duplicate overlap of the LCS portion. Classic interview follow-up to LCS.

13. **How do you solve 'longest repeating subsequence'?**
   - LCS with i!=j constraint: apply LCS recurrence but only carry dp[i-1][j-1]+1 when a[i]==b[j] and i!=j (same string). O(n^2).

14. **How do you count distinct palindromic substrings (Manacher-based DP)?**
   - Count centres O(n) with Manacher's radius array; total distinct substrings via set of all palindromes found in O(n) radius scan.

15. **Explain memoisation vs tabulation on string DP problems.**
   - Memoisation (top-down recursion + cache) is intuitive and skips unreachable states; tabulation (bottom-up loops) is iterative and faster. Both give identical answers; choose by clarity in interviews.

16. **How do you handle large strings in DP without timeouts?**
   - Use O(1)-space row compaction, prune unreachable states, early-exit when result threshold reached, and avoid slicing strings inside loops (index instead).

17. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

18. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

19. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

20. **What common edge cases must be handled in 03 dynamic programming on strings implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

21. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

22. **Give a real-world analogy for 03 dynamic programming on strings.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

23. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

24. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

25. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

26. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

27. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

28. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

29. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

30. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

31. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

32. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

33. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

34. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

35. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

36. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

37. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

38. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

39. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

40. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

41. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

42. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

43. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

44. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

45. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

46. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

47. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

48. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

49. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

50. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

51. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

52. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

53. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

54. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

55. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

56. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

57. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

58. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

59. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

60. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

61. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

62. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

63. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

64. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

65. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

66. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

67. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

68. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

69. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

70. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

71. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

72. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

73. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

74. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

75. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

76. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

77. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

78. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

79. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

80. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

81. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

82. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

83. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

84. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

85. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

86. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

87. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

88. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

89. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

90. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

91. **How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

92. **Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.**
   - Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

93. **How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

94. **What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

95. **Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

96. **How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

97. **What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

98. **Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

99. **State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

100. **What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

</details>