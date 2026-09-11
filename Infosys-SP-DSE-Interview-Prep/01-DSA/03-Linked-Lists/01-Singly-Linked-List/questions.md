# 01 Singly Linked List — Linked / Lists

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **Define a singly linked list node.**
   - Each node holds data and a pointer/reference to the next node; the list is traversed from a head pointer. Insertion/deletion at the head is O(1); access by index is O(n).

2. **Why is linked-list access slower than array access?**
   - No contiguous memory, so random access is impossible; you must follow next pointers from the head, giving O(n) worst-case element access.

3. **How do you insert a node at the head of a singly linked list?**
   - nxt = head; head = Node(val); head.next = nxt. Constant time O(1), no reallocation needed.

4. **Write code for inserting into the middle (after a given node).**
   - new.next = prev.next; prev.next = new. O(1) given the previous node reference; otherwise find it first (O(n)).

5. **How do you delete a node given only a pointer to it (no head)?**
   - Copy the next node's value into the current node, then delete the next node (skip it). This works only when node is not the tail.

6. **How do you reverse a singly linked list iteratively?**
   - prev=None; while curr: nxt=curr.next; curr.next=prev; prev=curr; curr=nxt; return prev. O(n) time, O(1) space.

7. **What recursion pitfalls arise when reversing a linked list?**
   - Deep recursion could stack-overflow on long lists; also be careful to set head.next=None to avoid cycles. Iterative is preferred for interviews unless asked for recursion.

8. **How do you find the middle node using two pointers?**
   - slow += 1, fast += 2; when fast or fast.next is None, slow is the middle (upper-middle for even length). O(n).

9. **How do you detect and find the start of a cycle (Floyd's)?**
   - slow/fast collide -> cycle exists. Reset one pointer to head; advance both one step; their meeting point is the cycle's start node. O(n).

10. **How do you find the length of a cycle?**
   - Once Floyd detects a meeting point, keep one pointer fixed and walk the other around until it returns; count steps. That length is the cycle length.

11. **How do you remove the Nth node from the end?**
   - Advance a fast pointer n steps, then move slow and fast together; when fast reaches end, slow's next is the node to delete. Single pass, O(n).

12. **How do you merge two sorted linked lists?**
   - Dummy head + two-pointer: attach the smaller of l1/l2 and advance; drain the remainder. O(n+m) time, O(1) space (reuses nodes).

13. **How do you merge k sorted lists (priority-queue approach)?**
   - Push all list heads into a min-heap; repeatedly pop the smallest, append, and push its next. O(total * log k).

14. **How do you find if two linked lists intersect?**
   - Align lengths (advance the longer by the difference) or swap pointers after each hits its tail; the node where they meet is the intersection. O(n+m).

15. **How do you find the Kth node from the end without extra space?**
   - Move a first pointer k steps ahead; then walk both until first is null — second now sits at the kth-from-end. O(n) single pass.

16. **What is the dummy-head technique and why is it useful?**
   - A sentinel node precedes the real head, so insertions/deletions at the front don't need special cases; return dummy.next at the end.

17. **How do you check if a linked list is a palindrome?**
   - Find the middle, reverse the second half, compare halves node-by-node; optionally restore the list. O(n) time, O(1) space.

18. **How do you remove duplicates from a sorted linked list?**
   - Walk comparing node.val with node.next.val; if equal, skip the next node. O(n). For unsorted, use a seen-set (O(n) space).

19. **How do you remove all nodes equal to a given value?**
   - Dummy head + prev pointer; if node.val == val, skip; else advance prev. Handles head deletion cleanly. O(n).

20. **How do you add two numbers represented by reversed linked lists?**
   - Iterate both lists with carry; create a node for each digit sum%10, carry=sum//10; drain remaining plus final carry. O(n).

21. **How do you rotate a linked list right by k?**
   - Compute length, k%=len; if 0 return. Find tail and (len-k)th node; relink tail to head and split there; update head. O(n).

22. **How do you reorder a list (L0,Ln,L1,Ln-1,...)?**
   - Find middle, reverse the second half, then interleave the two halves at the head. O(n).

23. **How do you detect a cycle with O(1) space other than Floyd?**
   - Floyd's is the classic O(1)-space option. Alternative: reverse traversal marking is destructive and invalid; so Floyd's is the answer for the space constraint.

24. **How do you split a circular linked list into two halves?**
   - Find the middle (slow/fast) and the tail; break links and close each half into its own circular list. O(n).

25. **When would you use a linked list over a dynamic array?**
   - Frequent insertions/deletions in the middle or head at scale, no random access needed, and when memory must not be wasted pre-allocating. Trade-off: cache-unfriendly pointers.

26. **Why are linked lists cache-unfriendly?**
   - Nodes are scattered in memory, defeating CPU cache prefetching; arrays exploit spatial locality, so in practice arrays often win even when asymptotics look worse.

27. **How do you delete a middle node given only current node?**
   - value copy + skip the successor is the standard 2-step; this is the 'Delete Node in a Linked List' problem.

28. **How do you swap nodes in pairs?**
   - Iterative: prev/dummy + first/second; relink pairs: second.next=first, first.next=rest, prev.next=second. O(n).

29. **How do you reverse nodes in k-group?**
   - Count k nodes; if present, reverse the group and recurse/iterate on the remainder; otherwise leave as-is. O(n).

30. **Explain insertion sort on a linked list.**
   - Build a new sorted list by inserting each node at its sorted position using dummy head comparisons. O(n^2) worst but O(1) space.

31. **How do you partition a linked list around a value x?**
   - Build two lists (less-than and greater-or-equal), connect them, ensure the tail is None. Stable partition, O(n).

32. **What is a self-looped linked list and a dangerous consequence?**
   - A cycle or wrong tail references; infinite traversal loops and memory leaks in releases. Always terminate loops on None checks.

33. **What is the intuition behind the 01 singly linked list technique used in coding interviews?**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

34. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

35. **State the time and space complexity of the optimal solution for most 01 singly linked list problems.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

36. **What common edge cases must be handled in 01 singly linked list implementations?**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

37. **How would you dry-run your 01 singly linked list code on a small example in an interview?**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

38. **Give a real-world analogy for 01 singly linked list.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

39. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list?**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

40. **What is the role of a prefix/suffix precomputation in 01 singly linked list?**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

41. **Explain the optimisation step you would mention after writing the naive version for 01 singly linked list.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

42. **How is 01 singly linked list asked differently in an online assessment versus a live interview?**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

43. **What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

44. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

45. **State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

46. **What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

47. **How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

48. **Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

49. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

50. **What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

51. **Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

52. **How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

53. **What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

54. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

55. **State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

56. **What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

57. **How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

58. **Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

59. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

60. **What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

61. **Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

62. **How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

63. **What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

64. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

65. **State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

66. **What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

67. **How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

68. **Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

69. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

70. **What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

71. **Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

72. **How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

73. **What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

74. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

75. **State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

76. **What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

77. **How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

78. **Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

79. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

80. **What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

81. **Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

82. **How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

83. **What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

84. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

85. **State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

86. **What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

87. **How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

88. **Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

89. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

90. **What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

91. **Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.**
   - First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

92. **How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.**
   - In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

93. **What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.**
   - The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

94. **Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.**
   - Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

95. **State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.**
   - The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

96. **What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.**
   - Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

97. **How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.**
   - Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

98. **Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.**
   - Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

99. **How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.**
   - Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

100. **What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.**
   - Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

</details>