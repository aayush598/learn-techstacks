# Strings — Anagrams And Permutations Interview Questions and Answers

## Q1: Define anagram and the two standard detection techniques.
**A:** Anagrams have identical character multisets: same length and same frequency map. Techniques: sorted equality or Counter equality — both O(n) after prechecks.

## Q2: Group a list of strings into anagram groups.
**A:** Map key = tuple(sorted(s)) or a 26-count tuple (O(26n)) to the group list. Return grouping. O(n*26) with count-key avoids sorting.

## Q3: How do you find all anagram-start indices of p in s?
**A:** Sliding window of length len(p) with a running frequency map; compare against target Counter with equality of lengths of non-zero entries or full equality. O(|s|).

## Q4: Explain permutations of a string via recursion/backtracking.
**A:** Swap-based: fix each position, recurse on remainder; or pick/remove approach. Complexity O(n!) worst, dedupe with set when characters repeat.

## Q5: How do you generate the NEXT lexicographic permutation of a string?
**A:** Find the longest decreasing suffix, pivot before it; swap pivot with the smallest greater character in the suffix; reverse the suffix. That is std::next_permutation logic, O(n).

## Q6: What is the kth permutation problem?
**A:** Build factorial number system: for position i, group size = factorial of remaining; pick block = k//group, set k%=group. Skip used chars. O(n^2) with list removal.

## Q7: How do you check if one word can be formed by letters of another?
**A:** Ensure requirement chars are a sub-multiset: for every char, need[ch] <= have[ch]. Counter supports Counter(a)<=Counter(b).

## Q8: How do you find the minimum window substring for a target multiset?
**A:** Sliding window tracking required vs found counts; expand to satisfy, then shrink to minimise length. O(n) with two pointers; classic 'minimum window substring'.

## Q9: Explain word pattern / isomorphic strings checks.
**A:** Both map characters/words consistently: build dicts for bijection and check both directions to avoid two keys mapping to one value. O(n).

## Q10: How do you check if two strings are anagrams ignoring case/spaces?
**A:** Filter to alnum, lower both, compare Counters. Separating preprocessing from comparison makes the intention explicit.

## Q11: How do you count distinct permutations with repeated characters?
**A:** Permutations = n! / (product of factorials of each character count). Demonstrates combinatorial reasoning with multiplicities.

## Q12: How do you check permutation existence larger than given string?
**A:** Easiest: sort all candidates and compare; or sliding-window multiset equality plus greedy for lexicographic order. Clarify which criterion with the interviewer.

## Q13: What is a valid-anagram-as-palindrome condition?
**A:** A string can be rearranged into a palindrome iff at most one character has an odd count. From that test derive suitability for palindrome permutations.

## Q14: How do you find all unlocked-and-mutual anagram words (word squares)?
**A:** This is a backtracking + prefix check problem: build a trie of prefixes; place words row by row ensuring column prefixes exist — as in 'Word Squares'.

## Q15: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q16: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q17: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q18: What common edge cases must be handled in 04 anagrams and permutations implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q19: How would you dry-run your 04 anagrams and permutations code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q20: Give a real-world analogy for 04 anagrams and permutations.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q21: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q22: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q23: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q24: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q25: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q26: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q27: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q28: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q29: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q30: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q31: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q32: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q33: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q34: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q35: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q36: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q37: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q38: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q39: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q40: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q41: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q42: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q43: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q44: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q45: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q46: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q47: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q48: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q49: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q50: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q51: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q52: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q53: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q54: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q55: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q56: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q57: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q58: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q59: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q60: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q61: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q62: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q63: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q64: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q65: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q66: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q67: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q68: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q69: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q70: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q71: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q72: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q73: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q74: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q75: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q76: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q77: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q78: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q79: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q80: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q81: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q82: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q83: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q84: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q85: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q86: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q87: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q88: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q89: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q90: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q91: How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q92: What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q93: Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q94: How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q95: What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q96: Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q97: State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q98: What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q99: How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q100: Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.
**A:** Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.
