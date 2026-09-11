# 04 Anagrams And Permutations — Strings

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define anagram and the two standard detection techniques.**
   - Anagrams have identical character multisets: same length and same frequency map. Techniques: sorted equality or Counter equality — both O(n) after prechecks.

2. **Group a list of strings into anagram groups.**
   - Map key = tuple(sorted(s)) or a 26-count tuple (O(26n)) to the group list. Return grouping. O(n*26) with count-key avoids sorting.

3. **How do you find all anagram-start indices of p in s?**
   - Sliding window of length len(p) with a running frequency map; compare against target Counter with equality of lengths of non-zero entries or full equality. O(|s|).

4. **Explain permutations of a string via recursion/backtracking.**
   - Swap-based: fix each position, recurse on remainder; or pick/remove approach. Complexity O(n!) worst, dedupe with set when characters repeat.

5. **How do you generate the NEXT lexicographic permutation of a string?**
   - Find the longest decreasing suffix, pivot before it; swap pivot with the smallest greater character in the suffix; reverse the suffix. That is std::next_permutation logic, O(n).

6. **What is the kth permutation problem?**
   - Build factorial number system: for position i, group size = factorial of remaining; pick block = k//group, set k%=group. Skip used chars. O(n^2) with list removal.

7. **How do you check if one word can be formed by letters of another?**
   - Ensure requirement chars are a sub-multiset: for every char, need[ch] <= have[ch]. Counter supports Counter(a)<=Counter(b).

8. **How do you find the minimum window substring for a target multiset?**
   - Sliding window tracking required vs found counts; expand to satisfy, then shrink to minimise length. O(n) with two pointers; classic 'minimum window substring'.

9. **Explain word pattern / isomorphic strings checks.**
   - Both map characters/words consistently: build dicts for bijection and check both directions to avoid two keys mapping to one value. O(n).

10. **How do you check if two strings are anagrams ignoring case/spaces?**
   - Filter to alnum, lower both, compare Counters. Separating preprocessing from comparison makes the intention explicit.

11. **How do you count distinct permutations with repeated characters?**
   - Permutations = n! / (product of factorials of each character count). Demonstrates combinatorial reasoning with multiplicities.

12. **How do you check permutation existence larger than given string?**
   - Easiest: sort all candidates and compare; or sliding-window multiset equality plus greedy for lexicographic order. Clarify which criterion with the interviewer.

13. **What is a valid-anagram-as-palindrome condition?**
   - A string can be rearranged into a palindrome iff at most one character has an odd count. From that test derive suitability for palindrome permutations.

14. **How do you find all unlocked-and-mutual anagram words (word squares)?**
   - This is a backtracking + prefix check problem: build a trie of prefixes; place words row by row ensuring column prefixes exist — as in 'Word Squares'.

15. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

16. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

17. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

18. **What common edge cases must be handled in 04 anagrams and permutations implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

19. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

20. **Give a real-world analogy for 04 anagrams and permutations.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

21. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

22. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

23. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

24. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

25. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

26. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

27. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

28. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

29. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

30. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

31. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

32. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

33. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

34. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

35. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

36. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

37. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

38. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

39. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

40. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

41. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

42. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

43. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

44. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

45. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

46. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

47. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

48. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

49. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

50. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

51. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

52. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

53. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

54. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

55. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

56. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

57. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

58. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

59. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

60. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

61. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

62. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

63. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

64. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

65. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

66. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

67. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

68. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

69. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

70. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

71. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

72. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

73. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

74. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

75. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

76. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

77. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

78. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

79. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

80. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

81. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

82. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

83. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

84. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

85. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

86. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

87. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

88. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

89. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

90. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

91. **How do you decide between a hash map, sorting, or two pointers as tools for 04 anagrams and permutations? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

92. **What is the role of a prefix/suffix precomputation in 04 anagrams and permutations? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

93. **Explain the optimisation step you would mention after writing the naive version for 04 anagrams and permutations. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

94. **How is 04 anagrams and permutations asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

95. **What is the intuition behind the 04 anagrams and permutations technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

96. **Write the brute-force approach for a typical 04 anagrams and permutations problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

97. **State the time and space complexity of the optimal solution for most 04 anagrams and permutations problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

98. **What common edge cases must be handled in 04 anagrams and permutations implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

99. **How would you dry-run your 04 anagrams and permutations code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

100. **Give a real-world analogy for 04 anagrams and permutations. Extend your answer with a second example.**
   - Analogy: 04 anagrams and permutations is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

</details>