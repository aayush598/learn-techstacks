# Strings — Dynamic Programming On Strings Interview Questions and Answers

## Q1: Overview of DP on strings and standard state design.
**A:** State is typically (i,j) = position in string A and string B. Transitions come from char match/mismatch, gap, or replace choices — forming LCS, edit-distance, palindromes and interleaving problems.

## Q2: How is Longest Common Subsequence defined and solved?
**A:** LCS keeps order without adjacency. Recurrence: if a[i]==b[j]: dp[i][j]=dp[i-1][j-1]+1 else max of dp[i-1][j], dp[i][j-1]. O(n*m) DP; reconstruct by backtracking.

## Q3: Explain edit distance (Levenshtein).
**A:** Min ops (insert/delete/replace) to turn a into b. dp[i][j]=min(insert, delete, replace). If chars equal, carry dp[i-1][j-1]. O(n*m).

## Q4: How do you find the longest palindromic subsequence?
**A:** LCS of s with reversed(s), or DP palindrome recurrence: if s[i]==s[j]: dp[i][j]=dp[i+1][j-1]+2 else max(dp[i+1][j],dp[i][j-1]). Fill by increasing length.

## Q5: How do you find the minimum insertions to make a string a palindrome?
**A:** Insertions needed = len(s) - longest_palindromic_subsequence(s). The complement of already-matching characters is what must be added symmetrically.

## Q6: How do you check if a string is an interleaving of two others?
**A:** dp[i][j] True if s3[0:i+j] is an interleaving of s1[0:i] and s2[0:j]; transitions consume from s1 or s2 when chars match s3. O(n*m).

## Q7: What is a substring edit-distance variant (segment change)?
**A:** Common variants restrict operations (e.g., only delete), early-exit when distance>k, or ask for distinct edits — adapt states accordingly and add pruning.

## Q8: How do you compute edit distance with O(m) space?
**A:** Roll dp arrays: only two rows are needed because transitions reference i-1 row only. From row to row, keep prev and current. O(n*m) time, O(m) space.

## Q9: How does the 'delete operation for two strings' problem work?
**A:** Min deletions to make s and t equal = n + m - 2*LCS(s,t). Only delete operations allowed means unchanged parts are exactly the common subsequence.

## Q10: How do you find the longest common substring?
**A:** DP where dp[i][j]=dp[i-1][j-1]+1 only when chars match (reset on mismatch). Keep global max. O(n*m) time; suffix array gives O(n log n).

## Q11: How do you build all distinct LCS (or DP backtracking) answers?
**A:** Backtrack through equal-value transitions collecting paths; dedupe with a set. Exponential worst-case output, so report count or all with memoised sets.

## Q12: What is the shortest common supersequence problem?
**A:** SCS(a,b) length = n+m-LCS(a,b). Reconstruction merges a and b avoiding duplicate overlap of the LCS portion. Classic interview follow-up to LCS.

## Q13: How do you solve 'longest repeating subsequence'?
**A:** LCS with i!=j constraint: apply LCS recurrence but only carry dp[i-1][j-1]+1 when a[i]==b[j] and i!=j (same string). O(n^2).

## Q14: How do you count distinct palindromic substrings (Manacher-based DP)?
**A:** Count centres O(n) with Manacher's radius array; total distinct substrings via set of all palindromes found in O(n) radius scan.

## Q15: Explain memoisation vs tabulation on string DP problems.
**A:** Memoisation (top-down recursion + cache) is intuitive and skips unreachable states; tabulation (bottom-up loops) is iterative and faster. Both give identical answers; choose by clarity in interviews.

## Q16: How do you handle large strings in DP without timeouts?
**A:** Use O(1)-space row compaction, prune unreachable states, early-exit when result threshold reached, and avoid slicing strings inside loops (index instead).

## Q17: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q18: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q19: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q20: What common edge cases must be handled in 03 dynamic programming on strings implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q21: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q22: Give a real-world analogy for 03 dynamic programming on strings.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q23: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q24: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q25: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q26: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q27: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q28: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q29: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q30: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q31: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q32: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q33: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q34: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q35: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q36: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q37: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q38: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q39: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q40: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q41: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q42: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q43: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q44: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q45: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q46: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q47: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q48: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q49: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q50: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q51: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q52: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q53: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q54: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q55: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q56: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q57: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q58: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q59: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q60: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q61: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q62: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q63: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q64: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q65: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q66: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q67: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q68: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q69: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q70: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q71: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q72: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q73: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q74: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q75: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q76: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q77: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q78: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q79: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q80: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q81: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q82: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q83: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q84: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q85: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q86: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q87: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q88: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q89: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q90: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q91: How would you dry-run your 03 dynamic programming on strings code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q92: Give a real-world analogy for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** Analogy: 03 dynamic programming on strings is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q93: How do you decide between a hash map, sorting, or two pointers as tools for 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q94: What is the role of a prefix/suffix precomputation in 03 dynamic programming on strings? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q95: Explain the optimisation step you would mention after writing the naive version for 03 dynamic programming on strings. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q96: How is 03 dynamic programming on strings asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q97: What is the intuition behind the 03 dynamic programming on strings technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q98: Write the brute-force approach for a typical 03 dynamic programming on strings problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q99: State the time and space complexity of the optimal solution for most 03 dynamic programming on strings problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q100: What common edge cases must be handled in 03 dynamic programming on strings implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.
