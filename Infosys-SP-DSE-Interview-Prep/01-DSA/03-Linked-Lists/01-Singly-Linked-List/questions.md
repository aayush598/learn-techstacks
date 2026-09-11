# Linked Lists — Singly Linked List Interview Questions and Answers

## Q1: Define a singly linked list node.
**A:** Each node holds data and a pointer/reference to the next node; the list is traversed from a head pointer. Insertion/deletion at the head is O(1); access by index is O(n).

## Q2: Why is linked-list access slower than array access?
**A:** No contiguous memory, so random access is impossible; you must follow next pointers from the head, giving O(n) worst-case element access.

## Q3: How do you insert a node at the head of a singly linked list?
**A:** nxt = head; head = Node(val); head.next = nxt. Constant time O(1), no reallocation needed.

## Q4: Write code for inserting into the middle (after a given node).
**A:** new.next = prev.next; prev.next = new. O(1) given the previous node reference; otherwise find it first (O(n)).

## Q5: How do you delete a node given only a pointer to it (no head)?
**A:** Copy the next node's value into the current node, then delete the next node (skip it). This works only when node is not the tail.

## Q6: How do you reverse a singly linked list iteratively?
**A:** prev=None; while curr: nxt=curr.next; curr.next=prev; prev=curr; curr=nxt; return prev. O(n) time, O(1) space.

## Q7: What recursion pitfalls arise when reversing a linked list?
**A:** Deep recursion could stack-overflow on long lists; also be careful to set head.next=None to avoid cycles. Iterative is preferred for interviews unless asked for recursion.

## Q8: How do you find the middle node using two pointers?
**A:** slow += 1, fast += 2; when fast or fast.next is None, slow is the middle (upper-middle for even length). O(n).

## Q9: How do you detect and find the start of a cycle (Floyd's)?
**A:** slow/fast collide -> cycle exists. Reset one pointer to head; advance both one step; their meeting point is the cycle's start node. O(n).

## Q10: How do you find the length of a cycle?
**A:** Once Floyd detects a meeting point, keep one pointer fixed and walk the other around until it returns; count steps. That length is the cycle length.

## Q11: How do you remove the Nth node from the end?
**A:** Advance a fast pointer n steps, then move slow and fast together; when fast reaches end, slow's next is the node to delete. Single pass, O(n).

## Q12: How do you merge two sorted linked lists?
**A:** Dummy head + two-pointer: attach the smaller of l1/l2 and advance; drain the remainder. O(n+m) time, O(1) space (reuses nodes).

## Q13: How do you merge k sorted lists (priority-queue approach)?
**A:** Push all list heads into a min-heap; repeatedly pop the smallest, append, and push its next. O(total * log k).

## Q14: How do you find if two linked lists intersect?
**A:** Align lengths (advance the longer by the difference) or swap pointers after each hits its tail; the node where they meet is the intersection. O(n+m).

## Q15: How do you find the Kth node from the end without extra space?
**A:** Move a first pointer k steps ahead; then walk both until first is null — second now sits at the kth-from-end. O(n) single pass.

## Q16: What is the dummy-head technique and why is it useful?
**A:** A sentinel node precedes the real head, so insertions/deletions at the front don't need special cases; return dummy.next at the end.

## Q17: How do you check if a linked list is a palindrome?
**A:** Find the middle, reverse the second half, compare halves node-by-node; optionally restore the list. O(n) time, O(1) space.

## Q18: How do you remove duplicates from a sorted linked list?
**A:** Walk comparing node.val with node.next.val; if equal, skip the next node. O(n). For unsorted, use a seen-set (O(n) space).

## Q19: How do you remove all nodes equal to a given value?
**A:** Dummy head + prev pointer; if node.val == val, skip; else advance prev. Handles head deletion cleanly. O(n).

## Q20: How do you add two numbers represented by reversed linked lists?
**A:** Iterate both lists with carry; create a node for each digit sum%10, carry=sum//10; drain remaining plus final carry. O(n).

## Q21: How do you rotate a linked list right by k?
**A:** Compute length, k%=len; if 0 return. Find tail and (len-k)th node; relink tail to head and split there; update head. O(n).

## Q22: How do you reorder a list (L0,Ln,L1,Ln-1,...)?
**A:** Find middle, reverse the second half, then interleave the two halves at the head. O(n).

## Q23: How do you detect a cycle with O(1) space other than Floyd?
**A:** Floyd's is the classic O(1)-space option. Alternative: reverse traversal marking is destructive and invalid; so Floyd's is the answer for the space constraint.

## Q24: How do you split a circular linked list into two halves?
**A:** Find the middle (slow/fast) and the tail; break links and close each half into its own circular list. O(n).

## Q25: When would you use a linked list over a dynamic array?
**A:** Frequent insertions/deletions in the middle or head at scale, no random access needed, and when memory must not be wasted pre-allocating. Trade-off: cache-unfriendly pointers.

## Q26: Why are linked lists cache-unfriendly?
**A:** Nodes are scattered in memory, defeating CPU cache prefetching; arrays exploit spatial locality, so in practice arrays often win even when asymptotics look worse.

## Q27: How do you delete a middle node given only current node?
**A:** value copy + skip the successor is the standard 2-step; this is the 'Delete Node in a Linked List' problem.

## Q28: How do you swap nodes in pairs?
**A:** Iterative: prev/dummy + first/second; relink pairs: second.next=first, first.next=rest, prev.next=second. O(n).

## Q29: How do you reverse nodes in k-group?
**A:** Count k nodes; if present, reverse the group and recurse/iterate on the remainder; otherwise leave as-is. O(n).

## Q30: Explain insertion sort on a linked list.
**A:** Build a new sorted list by inserting each node at its sorted position using dummy head comparisons. O(n^2) worst but O(1) space.

## Q31: How do you partition a linked list around a value x?
**A:** Build two lists (less-than and greater-or-equal), connect them, ensure the tail is None. Stable partition, O(n).

## Q32: What is a self-looped linked list and a dangerous consequence?
**A:** A cycle or wrong tail references; infinite traversal loops and memory leaks in releases. Always terminate loops on None checks.

## Q33: What is the intuition behind the 01 singly linked list technique used in coding interviews?
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q34: Write the brute-force approach for a typical 01 singly linked list problem and analyse it.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q35: State the time and space complexity of the optimal solution for most 01 singly linked list problems.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q36: What common edge cases must be handled in 01 singly linked list implementations?
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q37: How would you dry-run your 01 singly linked list code on a small example in an interview?
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q38: Give a real-world analogy for 01 singly linked list.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q39: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list?
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q40: What is the role of a prefix/suffix precomputation in 01 singly linked list?
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q41: Explain the optimisation step you would mention after writing the naive version for 01 singly linked list.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q42: How is 01 singly linked list asked differently in an online assessment versus a live interview?
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q43: What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q44: Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q45: State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q46: What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q47: How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q48: Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q49: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q50: What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q51: Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q52: How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q53: What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q54: Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q55: State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q56: What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q57: How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q58: Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q59: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q60: What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q61: Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q62: How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q63: What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q64: Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q65: State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q66: What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q67: How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q68: Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q69: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q70: What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q71: Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q72: How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q73: What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q74: Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q75: State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q76: What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q77: How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q78: Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q79: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q80: What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q81: Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q82: How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q83: What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q84: Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q85: State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q86: What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q87: How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q88: Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q89: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q90: What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.

## Q91: Explain the optimisation step you would mention after writing the naive version for 01 singly linked list. Extend your answer with a second example.
**A:** First remove redundant recomputation via memoisation or prefix arrays; next, exploit monotonicity with two pointers/sliding window; finally, reduce space by keeping running variables instead of full tables — always closing with the improved complexity.

## Q92: How is 01 singly linked list asked differently in an online assessment versus a live interview? Extend your answer with a second example.
**A:** In the assessment only correctness/speed of the final code matters and hidden tests matter; in the live round the interviewer wants your thought process, complexity analysis, edge cases, and a hand trace — both must be practiced.

## Q93: What is the intuition behind the 01 singly linked list technique used in coding interviews? Extend your answer with a second example.
**A:** The core idea is to avoid brute force by exploiting structure: leftover wasted compares are removed, and each element is processed a small constant number of times, driving complexity down to an optimal bound that interviewers expect you to justify.

## Q94: Write the brute-force approach for a typical 01 singly linked list problem and analyse it. Extend your answer with a second example.
**A:** Brute force enumerates every candidate configuration, e.g., every subarray/combination/permutation, giving O(n^2), O(n^3) or O(2^n). It is correct but only useful for small inputs; the interview follow-up is to optimise it to linear or O(n log n).

## Q95: State the time and space complexity of the optimal solution for most 01 singly linked list problems. Extend your answer with a second example.
**A:** The optimal solution is usually O(n) time with O(n) space, or O(n) time with O(1) space when a monotonic/pointer trick applies. Always state constants and best/worst cases explicitly.

## Q96: What common edge cases must be handled in 01 singly linked list implementations? Extend your answer with a second example.
**A:** Empty input, single-element input, all-equal values, negative numbers, duplicates, off-by-one at the last index, and large values where intermediate sums/products can overflow — every one must be tested.

## Q97: How would you dry-run your 01 singly linked list code on a small example in an interview? Extend your answer with a second example.
**A:** Pick a tiny input, walk index by index while updating each variable, and show the invariants hold at every step. This proves both correctness and that you truly understand the algorithm, which Infosys interviewers probe by asking you to trace code by hand.

## Q98: Give a real-world analogy for 01 singly linked list. Extend your answer with a second example.
**A:** Analogy: 01 singly linked list is like scanning a line of people for a specific property while remembering a few key facts — each person is visited once and relevant state is carried forward, exactly how the optimal solution behaves.

## Q99: How do you decide between a hash map, sorting, or two pointers as tools for 01 singly linked list? Extend your answer with a second example.
**A:** Hash map when you need membership/paired lookup in O(1) and space is affordable; sorting when order gives a monotonic advantage (two pointers, binary search); pointers directly when the input is already sorted. Trade space for speed only when constraints allow.

## Q100: What is the role of a prefix/suffix precomputation in 01 singly linked list? Extend your answer with a second example.
**A:** Precomputation turns repeated subcomputations into O(1) lookups, converting an O(n^2) nested loop into O(n). Common wherever the value at index i depends on an aggregate over a range around i.
