# 01 Basics — Arrays

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define an array and state how elements are stored in memory.**
   - An array is a linear, homogeneous data structure storing elements in contiguous memory locations. Element i is at address base + i*element_size, which gives O(1) random access by index.

2. **Why does an array give O(1) access time?**
   - Because index maps directly to a memory address via base + index*size; the CPU does one addition and one multiply, no traversal needed.

3. **Compare a Python list with a classic C array.**
   - C arrays are fixed-size, homogeneous, contiguous raw memory. A Python list is a dynamic array of PyObject pointers: it can mix types, resizes automatically (amortised O(1) append), and supports slicing/negative indexes.

4. **What is the time complexity of appending to a Python list?**
   - Amortised O(1). When full, CPython allocates a larger buffer (~1.125x growth) and copies elements, spreading that O(n) cost across appends.

5. **How does list.insert(0, x) compare with list.append(x)?**
   - append is amortised O(1); insert(0,x) is O(n) because every element shifts right by one. For frequent head insertions use collections.deque (O(1) both ends).

6. **Explain array slice semantics: arr[1:4].**
   - Returns a NEW list containing elements from index 1 up to (not including) index 4; original unchanged. Slicing copies references, so it costs O(k) time and memory.

7. **What is the result of arr[::-1]?**
   - A new list with the array reversed — the step -1 traverses from the end to the start. It never mutates the original.

8. **Why is complexity analysis of array problems critical in the SP/DSE online round?**
   - Constraints (n up to 10^5/10^6) make O(n^2) solutions time out; partial scoring means passing 60-100% hidden cases hinges on optimal or near-optimal solutions.

9. **Write code to find the second largest element in an array.**
   - Track largest and second_largest in one pass: if x>mx: sec=mx; mx=x; elif sec<x<mx: sec=x. Return sec; handle n<2 as error or -inf.

10. **How do you find the third maximum (distinct) element?**
   - Keep three running variables for 1st/2nd/3rd max, skipping duplicates; if fewer than 3 distinct values exist, return the maximum instead (per problem statement).

11. **What is Kadane's algorithm?**
   - Maximum subarray sum in O(n): cur = max(x, cur + x); best = max(best, cur). It works because any subarray straddling a negative prefix can be dropped.

12. **What is the subarray vs subsequence distinction?**
   - Subarray is contiguous (n(n+1)/2 possibilities); subsequence preserves order but skips elements (2^n possibilities). Algorithms and complexity differ drastically.

13. **How do you reverse an array in place?**
   - Two-pointer: swap arr[l] and arr[r], then l++, r--, until l>=r. O(n) time, O(1) space. Python also has arr.reverse().

14. **How do you rotate an array by k positions?**
   - k%=n; reverse(0,n-k-1); reverse(n-k,n-1); reverse(0,n-1). O(n) time O(1) space. This reversal rotation is the canonical answer.

15. **Explain the missing-number problem (array 1..n missing one).**
   - Sum formula: expected n*(n+1)//2 minus current sum. XOR variant: XOR all indices+values, duplicates cancel. Both O(n) time, O(1) space.

16. **How do you find duplicates in an array of length n with values in [1,n]?**
   - Cycle-detection/negative-marking: if values allowed in range, set nums[nums[i]-1] to negative as marker; the duplicated index resurfaces. Or use a set for O(n) space.

17. **Explain Boyer-Moore voting for the majority element.**
   - Pair off different elements; the element surviving cancellation is the only possible majority, then verify by count. O(n) time, O(1) space, requires majority (>n/2).

18. **Why does the majority candidate need a verification pass?**
   - Voting only guarantees no OTHER majority exists; it never asserts the candidate actually is majority. A second pass counting occurrences confirms it.

19. **What is a prefix-sum array and its main use?**
   - prefix[i] = sum of arr[0..i]. Range query sum(l,r)=prefix[r]-prefix[l-1] in O(1) after O(n) preprocessing. Core tool for subarray-sum problems.

20. **Given prefix sums, how do you detect a zero-sum subarray?**
   - If any prefix value repeats (or equals 0), the stretch between the two occurrences sums to zero. Track seen prefix values in a set/dict.

21. **What is a suffix or postfix array used for?**
   - Stores aggregates from the right (e.g., suffix max). Pairing prefix+suffix lets you compute 'element excluding range' answers, like Product of Array Except Self, in O(n).

22. **Write Product of Array Except Self in O(n) with O(1) extra space.**
   - First pass: res[i]=product of all left elements using a running product. Second pass from right: multiply by running right product. Output array itself is not counted as extra space.

23. **How do you merge two sorted arrays into a third sorted array?**
   - Two-pointer merge comparing heads; append smaller, advance that pointer, then drain the remaining tail. O(m+n) time, O(m+n) space.

24. **How does the in-place Merge Sorted Array (LeetCode 88) work?**
   - Work backwards: i=m-1, j=n-1, k=m+n-1. Put the larger of nums1[i], nums2[j] at k, decrement; no overwriting of unprocessed data.

25. **How do you find the majority of an array using a hash map?**
   - Count frequencies in a dict, then return the key whose count > n//2. Simple, O(n) time and O(n) space; Boyer-Moore improves space to O(1).

26. **Explain the two-pointer move-zeros technique.**
   - Write-index w and scan i; if arr[i]!=0, assign arr[w]=arr[i] and w++. After the pass, fill 0 from w onward. Preserves relative order, O(n) time O(1) space.

27. **What is the maximum subarray sum when the window is circular?**
   - Compute max subarray via Kadane and min subarray via inverted Kadane; circular_max = max(kadane, total - min_subarray). Edge case: if all negative, return max element.

28. **How do you find the Kth largest element?**
   - Options: sort+index O(n log n); min-heap of size k O(n log k); quickselect O(n) avg. For SP/DSE, quickselect or heap demonstrates depth.

29. **What is quickselect and its worst-case complexity?**
   - Variation of quicksort that partitions and recurses only into the side containing the kth element. Average O(n), worst O(n^2) with bad pivots; use random pivot in practice.

30. **How do you count inversions in an array?**
   - An inversion is a pair i<j with arr[i]>arr[j]. Modified merge sort counts inversions while merging: when right element is placed, add remaining left count. O(n log n).

31. **Explain the concept of a monotonic stack and where it is used.**
   - A stack that keeps elements in increasing/decreasing order; used for next-greater/smaller element, largest rectangle in histogram, trapping rain water. Each element pushed/popped once, O(n).

32. **How do you find the next greater element for each index?**
   - Monotonic decreasing stack storing indices. While arr[stack.top()] < arr[i], pop and record arr[i] as NGE. Remaining stack elements have no NGE.

33. **What is the intuition behind the 01 basics technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

34. **Write the brute-force approach for a typical 01 basics problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

35. **State the time and space complexity of the optimal solution for most 01 basics problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

36. **What common edge cases must be handled in 01 basics implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

37. **How would you dry-run your 01 basics code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

38. **Give a real-world analogy for 01 basics.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

39. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

40. **What is the role of a prefix/suffix precomputation in 01 basics?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

41. **Explain the optimisation step you would mention after writing the naive version for 01 basics.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

42. **How is 01 basics asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

43. **What is the intuition behind the 01 basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

44. **Write the brute-force approach for a typical 01 basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

45. **State the time and space complexity of the optimal solution for most 01 basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

46. **What common edge cases must be handled in 01 basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

47. **How would you dry-run your 01 basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

48. **Give a real-world analogy for 01 basics. Extend your answer with a second example.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

49. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

50. **What is the role of a prefix/suffix precomputation in 01 basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

51. **Explain the optimisation step you would mention after writing the naive version for 01 basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

52. **How is 01 basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

53. **What is the intuition behind the 01 basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

54. **Write the brute-force approach for a typical 01 basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

55. **State the time and space complexity of the optimal solution for most 01 basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

56. **What common edge cases must be handled in 01 basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

57. **How would you dry-run your 01 basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

58. **Give a real-world analogy for 01 basics. Extend your answer with a second example.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

59. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

60. **What is the role of a prefix/suffix precomputation in 01 basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

61. **Explain the optimisation step you would mention after writing the naive version for 01 basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

62. **How is 01 basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

63. **What is the intuition behind the 01 basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

64. **Write the brute-force approach for a typical 01 basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

65. **State the time and space complexity of the optimal solution for most 01 basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

66. **What common edge cases must be handled in 01 basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

67. **How would you dry-run your 01 basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

68. **Give a real-world analogy for 01 basics. Extend your answer with a second example.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

69. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

70. **What is the role of a prefix/suffix precomputation in 01 basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

71. **Explain the optimisation step you would mention after writing the naive version for 01 basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

72. **How is 01 basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

73. **What is the intuition behind the 01 basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

74. **Write the brute-force approach for a typical 01 basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

75. **State the time and space complexity of the optimal solution for most 01 basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

76. **What common edge cases must be handled in 01 basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

77. **How would you dry-run your 01 basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

78. **Give a real-world analogy for 01 basics. Extend your answer with a second example.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

79. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

80. **What is the role of a prefix/suffix precomputation in 01 basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

81. **Explain the optimisation step you would mention after writing the naive version for 01 basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

82. **How is 01 basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

83. **What is the intuition behind the 01 basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

84. **Write the brute-force approach for a typical 01 basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

85. **State the time and space complexity of the optimal solution for most 01 basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

86. **What common edge cases must be handled in 01 basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

87. **How would you dry-run your 01 basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

88. **Give a real-world analogy for 01 basics. Extend your answer with a second example.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

89. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

90. **What is the role of a prefix/suffix precomputation in 01 basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

91. **Explain the optimisation step you would mention after writing the naive version for 01 basics. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

92. **How is 01 basics asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

93. **What is the intuition behind the 01 basics technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

94. **Write the brute-force approach for a typical 01 basics problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

95. **State the time and space complexity of the optimal solution for most 01 basics problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

96. **What common edge cases must be handled in 01 basics implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

97. **How would you dry-run your 01 basics code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

98. **Give a real-world analogy for 01 basics. Extend your answer with a second example.**
   - Analogy: 01 basics is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

99. **How do you decide between a hash map, sorting, or two pointers as tools for 01 basics? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

100. **What is the role of a prefix/suffix precomputation in 01 basics? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

</details>