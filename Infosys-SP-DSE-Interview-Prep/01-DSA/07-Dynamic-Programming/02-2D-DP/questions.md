# Dynamic Programming — 2D Dp Interview Questions and Answers

## Q1: When do you need a 2D DP table?
**A:** When the state has two independent dimensions (position in two strings, (i,j) cell, row+column, left+right subarray). The classic instances are grid paths and string DPs.

## Q2: How do you solve unique paths on a grid?
**A:** dp[i][j]=dp[i-1][j]+dp[i][j-1]; first row/column are 1. O(rows·cols); can compress to O(cols) with a 1-row sweep.

## Q3: How do you solve min-path-sum on a grid?
**A:** dp[i][j]=grid[i][j]+min(dp[i-1][j], dp[i][j-1]); handle first row/column specially. O(n·m) with O(n·m) or O(n) space.

## Q4: Explain the 0/1 knapsack DP.
**A:** dp[i][w]=max(dp[i-1][w], dp[i-1][w-wt[i]]+val[i]); either skip or take item i. Fill weights ascending per item; optimise to 1D descending.

## Q5: How do you compress the knapsack table to one array?
**A:** For 0/1 knapsack iterate weight capacity DOWNWARD so each item is used once; for unbounded knapsack iterate UPWARD so items repeat. This is the classic dimension-trick.

## Q6: What is the 'edit distance' DP and its transitions?
**A:** dp[i][j]=min(insert dp[i][j-1]+1, delete dp[i-1][j]+1, replace dp[i-1][j-1]+(0/1)); matches chars carry the diagonal. O(n·m).

## Q7: What is the 'longest common subsequence' recurrence?
**A:** If a[i]==b[j]: dp[i][j]=dp[i-1][j-1]+1 else max(dp[i-1][j], dp[i][j-1]). Base row 0/col 0 = 0. O(n·m).

## Q8: What is the 'longest common substring' recurrence?
**A:** dp[i][j]=dp[i-1][j-1]+1 only when chars match; reset to 0 otherwise; track global max — adjacent runs differ from subsequence.

## Q9: How do you solve 'maximal square of 1s'?
**A:** dp[i][j]=1+min(dp[i-1][j],dp[i][j-1],dp[i-1][j-1]) for '1' cells; track max side squared for area. O(n·m).

## Q10: How do you solve 'surrounded regions / matrix DP with boundaries'?
**A:** DP over cells with boundary conditions; often the transform is dynamic on edges — run corner-propagating DP or union-find boundary flood first.

## Q11: How do you reconstruct the solution path in 2D DP (e.g., LCS sequence)?
**A:** Backtrack from dp[n][m]: if chars equal move diagonal and record; else move toward the higher DP neighbour. Collect reversed. O(n+m).

## Q12: How do you solve 'word break' (dictionary segmentation)?
**A:** dp[i]=true if any dp[j] and s[j:i] in dict; scan ends. O(n^2) with set lookup. Follow-up often wants a word count or all segments.

## Q13: What is the 'partition equal subset sum'?
**A:** Reduce to target = total/2; boolean knapsack with 1D descending-window; true iff reachable. O(n·target).

## Q14: How do you solve 'target sum' (± assignment)?
**A:** Rewrite as subset-sum on (sum+target)/2 with positivity guard; count ways via knapsack DP. O(n·target).

## Q15: How do you solve 'interleaving string' DP?
**A:** dp[i][j] true if s3[:i+j] is interleaving of s1[:i], s2[:j]; transition consumes s1 or s2 when character matches s3. O(n·m).

## Q16: What is the 'minimum path sum with obstacles'?
**A:** Same DP with blocked cells forced to 0 (or INF); the first cell sets the seed. O(n·m).

## Q17: How do you solve 'palindromic partitioning' (min cuts) with 2D palindrome table?
**A:** First precompute isPal[i][j] via DP (s[i]==s[j] and (j-i<=1 or isPal[i+1][j-1])), then dp-cuts over prefixes. O(n^2).

## Q18: How do you handle grid DP with obstacles in count-of-paths?
**A:** Paths through blocked cells become 0; otherwise dp[i][j]=dp[i-1][j]+dp[i][j-1]; seed dp[0][0] only when open.

## Q19: What is the 'minimum cost to make two strings identical' (delete ops)?
**A:** cost = (n+m-2*LCS) as in delete-operation-for-two-strings; or a custom cost matrix — the LCS form is the standard.

## Q20: What is the 'max profit with at most k transactions' 2D DP?
**A:** dp[t][d]=max(dp[t][d-1], prices[d]+max_{j<d}(dp[t-1][j]-prices[j])) — maintain a running best-sell; O(k·n) with the sell-day DP.

## Q21: What is the intuition behind the 02 2d dp technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q22: Write the brute-force approach for a typical 02 2d dp problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q23: State the time and space complexity of the optimal solution for most 02 2d dp problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q24: What common edge cases must be handled in 02 2d dp implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q25: How would you dry-run your 02 2d dp code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q26: Give a real-world analogy for 02 2d dp.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q27: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q28: What is the role of a prefix/suffix precomputation in 02 2d dp?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q29: Explain the optimisation step you would mention after writing the naive version for 02 2d dp.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q30: How is 02 2d dp asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q31: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q32: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q33: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q34: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q35: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q36: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q37: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q38: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q39: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q40: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q41: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q42: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q43: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q44: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q45: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q46: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q47: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q48: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q49: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q50: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q51: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q52: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q53: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q54: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q55: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q56: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q57: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q58: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q59: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q60: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q61: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q62: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q63: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q64: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q65: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q66: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q67: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q68: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q69: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q70: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q71: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q72: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q73: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q74: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q75: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q76: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q77: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q78: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q79: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q80: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q81: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q82: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q83: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q84: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q85: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q86: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q87: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q88: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q89: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q90: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q91: What is the intuition behind the 02 2d dp technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q92: Write the brute-force approach for a typical 02 2d dp problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q93: State the time and space complexity of the optimal solution for most 02 2d dp problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q94: What common edge cases must be handled in 02 2d dp implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q95: How would you dry-run your 02 2d dp code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q96: Give a real-world analogy for 02 2d dp. Extend your answer with a second example.
**A:** Analogy: 02 2d dp is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q97: How do you decide between a hash map, sorting, or two pointers as tools for 02 2d dp? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q98: What is the role of a prefix/suffix precomputation in 02 2d dp? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q99: Explain the optimisation step you would mention after writing the naive version for 02 2d dp. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q100: How is 02 2d dp asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.
