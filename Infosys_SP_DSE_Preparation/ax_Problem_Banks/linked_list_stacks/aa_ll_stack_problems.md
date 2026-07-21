# Linked List, Stack & Queue Problem Bank - Infosys SP DSE Preparation

---

## Common Class Definitions

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random

class DLLNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None
```

## Helper Functions for Testing

```python
def create_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def linked_list_to_array(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

def create_cycle(head, pos):
    if not head or pos == -1:
        return head
    cycle_node = head
    for _ in range(pos):
        cycle_node = cycle_node.next
    tail = head
    while tail.next:
        tail = tail.next
    tail.next = cycle_node
    return head
```

---

---

# PART A: LINKED LIST PROBLEMS (20)

---

## Problem 1: Reverse Linked List (Easy)

**Problem Statement:** Given the head of a singly linked list, reverse the list and return the reversed list.

**Example:**
```
Input: 1 -> 2 -> 3 -> 4 -> 5
Output: 5 -> 4 -> 3 -> 2 -> 1
```

**Approach:** Use three pointers — prev, current, next. At each step, store next, point current's next to prev, move prev to current, and current to next. Think of it as rewiring a chain link by link.

**Detailed Walkthrough:**
- Start: prev=None, curr=1
- Step 1: Save next=2, point 1->None, prev=1, curr=2
- Step 2: Save next=3, point 2->1, prev=2, curr=3
- Continue until curr becomes None, then prev is new head.

**Python Code:**
```python
def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

**Complexity:** Time O(n), Space O(1) iterative / O(n) recursive  
**Trick:** Always save `curr.next` before overwriting it. Think of it as rewiring a chain.  
**Edge Cases:** Empty list (return None), single node (return head).

---

## Problem 2: Merge Two Sorted Lists (Easy)

**Problem Statement:** Merge two sorted linked lists into one sorted list by splicing together the nodes.

**Example:**
```
Input: l1 = 1->2->4, l2 = 1->3->4
Output: 1->1->2->3->4->4
```

**Approach:** Use a dummy head to simplify edge cases. Compare heads of both lists, attach the smaller node to result, advance that pointer. When one list is exhausted, attach the remaining of the other.

**Detailed Walkthrough:**
- Create dummy node (0)
- Compare 1 vs 1: pick l1's 1, advance l1
- Compare 2 vs 1: pick l2's 1, advance l2
- Compare 2 vs 3: pick l1's 2, advance l1
- Continue until one list empty, then append the rest.

**Python Code:**
```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

**Complexity:** Time O(n+m), Space O(1)  
**Trick:** Dummy node eliminates edge cases for empty lists. Never forget to return `dummy.next`.  
**Edge Cases:** One or both lists empty.

---

## Problem 3: Linked List Cycle (Easy)

**Problem Statement:** Given head, determine if the linked list has a cycle in it using O(1) memory.

**Example:**
```
Input: 3 -> 2 -> 0 -> -4 (cycle at node 2)
Output: True
```

**Approach:** Floyd's Tortoise and Hare — slow pointer moves 1 step, fast moves 2 steps. If they meet, there's a cycle. If fast reaches None, no cycle.

**Detailed Walkthrough:**
- slow = head, fast = head
- Iteration 1: slow=2, fast=0
- Iteration 2: slow=0, fast=2
- Iteration 3: slow=-4, fast=-4 → They meet! Return True.

**Python Code:**
```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** If no cycle, fast reaches `None`. If cycle exists, they MUST meet inside the cycle.  
**Edge Cases:** Empty list, single node with no cycle.

---

## Problem 4: Middle of the Linked List (Easy)

**Problem Statement:** Given head of a singly linked list, return the middle node. If two middle nodes, return the second.

**Example:**
```
Input: 1 -> 2 -> 3 -> 4 -> 5
Output: Node with value 3

Input: 1 -> 2 -> 3 -> 4 -> 5 -> 6
Output: Node with value 4 (second middle)
```

**Approach:** Slow pointer moves 1 step, fast moves 2 steps. When fast reaches end, slow is at middle.

**Python Code:**
```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** For even-length lists, this naturally returns the second middle node (LeetCode convention).  
**Edge Cases:** Single node (return that node), two nodes (return second).

---

## Problem 5: Remove Duplicates from Sorted List (Easy)

**Problem Statement:** Given a sorted linked list, delete all duplicates such that each element appears only once.

**Example:**
```
Input: 1 -> 1 -> 2 -> 3 -> 3
Output: 1 -> 2 -> 3
```

**Approach:** Traverse with a pointer. If current.val equals next.val, skip next. Otherwise, advance current.

**Python Code:**
```python
def delete_duplicates(head):
    curr = head
    while curr and curr.next:
        if curr.val == curr.next.val:
            curr.next = curr.next.next
        else:
            curr = curr.next
    return head
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** Only advance `curr` when values differ. When skipping, don't advance — check the new next too.  
**Edge Cases:** Empty list, all duplicates, no duplicates.

---

## Problem 6: Add Two Numbers (Easy)

**Problem Statement:** Two numbers represented as reversed linked lists. Return their sum as a linked list.

**Example:**
```
Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8 (342 + 465 = 807)
```

**Approach:** Traverse both lists simultaneously, add corresponding digits plus carry. Create new nodes for each digit. Handle remaining carry at end.

**Python Code:**
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    carry = 0
    while l1 or l2 or carry:
        val = carry
        if l1:
            val += l1.val
            l1 = l1.next
        if l2:
            val += l2.val
            l2 = l2.next
        carry, digit = divmod(val, 10)
        curr.next = ListNode(digit)
        curr = curr.next
    return dummy.next
```

**Complexity:** Time O(max(m,n)), Space O(max(m,n))  
**Trick:** Using `divmod` makes carry and digit extraction clean. Don't forget the final carry.  
**Edge Cases:** Different length lists, carry at the most significant digit.

---

## Problem 7: Intersection of Two Linked Lists (Easy)

**Problem Statement:** Given two singly linked lists, find the node where they intersect (by reference, not value). Return null if no intersection.

**Example:**
```
A:     a1 -> a2
              \
               c1 -> c2
              /
B: b1 -> b2 -> b3
Output: Node c1
```

**Approach:** Use two pointers. When a pointer reaches the end, redirect it to the other list's head. They will meet at the intersection or both become null.

**Python Code:**
```python
def get_intersection_node(headA, headB):
    if not headA or not headB:
        return None
    pA, pB = headA, headB
    while pA is not pB:
        pA = pA.next if pA else headB
        pB = pB.next if pB else headA
    return pA
```

**Complexity:** Time O(m+n), Space O(1)  
**Trick:** Two pointers travel equal total distances (a+b+c), so they align at intersection.  
**Edge Cases:** No intersection (both become null), lists of different lengths.

---

## Problem 8: Linked List Cycle II (Easy)

**Problem Statement:** Given head of a linked list, return the node where the cycle begins. If no cycle, return null.

**Example:**
```
Input: 3 -> 2 -> 0 -> -4 (cycle at node 2)
Output: Node with value 2
```

**Approach:** Floyd's algorithm in two phases. Phase 1: detect meeting point. Phase 2: reset one pointer to head, move both 1 step at a time — they meet at cycle start.

**Python Code:**
```python
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow is not fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** Math proof: distance from head to cycle start equals distance from meeting point to cycle start.  
**Edge Cases:** No cycle, cycle at head.

---

## Problem 9: Remove Nth Node From End of List (Medium)

**Problem Statement:** Given head of a linked list, remove the nth node from the end and return the head.

**Example:**
```
Input: 1 -> 2 -> 3 -> 4 -> 5, n = 2
Output: 1 -> 2 -> 3 -> 5
```

**Approach:** Use two pointers with n gap. Move fast n steps ahead, then move both until fast reaches end. Slow's next is the node to delete.

**Python Code:**
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
```

**Complexity:** Time O(L), Space O(1)  
**Trick:** Dummy node handles the edge case of removing the head (first node). One pass with two pointers.  
**Edge Cases:** Removing the only node, removing the head.

---

## Problem 10: Reorder List (Medium)

**Problem Statement:** Reorder list as L0→Ln→L1→Ln-1→L2→Ln-2...

**Example:**
```
Input: 1 -> 2 -> 3 -> 4
Output: 1 -> 4 -> 2 -> 3

Input: 1 -> 2 -> 3 -> 4 -> 5
Output: 1 -> 5 -> 2 -> 4 -> 3
```

**Approach:** Three steps: (1) Find middle with slow/fast, (2) Reverse second half, (3) Merge alternating nodes from both halves.

**Python Code:**
```python
def reorder_list(head):
    if not head or not head.next:
        return
    # Find middle
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    # Reverse second half
    prev, curr = None, slow.next
    slow.next = None
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    # Merge two halves
    first, second = head, prev
    while second:
        tmp1, tmp2 = first.next, second.next
        first.next = second
        second.next = tmp1
        first = tmp1
        second = tmp2
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** Breaking the list at middle's `next` (not middle) is crucial. `slow.next = None` splits the list.  
**Edge Cases:** Empty list, single node, two nodes.

---

## Problem 11: Swap Nodes in Pairs (Medium)

**Problem Statement:** Swap every two adjacent nodes and return the reordered list. Do not change values — swap nodes themselves.

**Example:**
```
Input: 1 -> 2 -> 3 -> 4
Output: 2 -> 1 -> 4 -> 3
```

**Approach:** Use a dummy node and three pointers. For each pair, reverse the connection between them while maintaining links to the rest.

**Python Code:**
```python
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        first = prev.next
        second = first.next
        first.next = second.next
        second.next = first
        prev.next = second
        prev = first
    return dummy.next
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** Think of it as pointer rewiring: `prev→second→first→rest`. Move `prev` to `first` after each swap.  
**Edge Cases:** Odd number of nodes (last node stays), empty list.

---

## Problem 12: Rotate List (Medium)

**Problem Statement:** Given head, rotate the list to the right by k places.

**Example:**
```
Input: 1 -> 2 -> 3 -> 4 -> 5, k = 2
Output: 4 -> 5 -> 1 -> 2 -> 3
```

**Approach:** Make the list circular (connect tail to head). Find the new tail at position `len - k % len` from start. Break the circle there.

**Python Code:**
```python
def rotate_right(head, k):
    if not head or not head.next or k == 0:
        return head
    # Find length and tail
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1
    k %= length
    if k == 0:
        return head
    # Make circular and find new break point
    tail.next = head
    steps_to_new_tail = length - k
    new_tail = head
    for _ in range(steps_to_new_tail - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** `k % length` avoids unnecessary rotations. Finding new tail at `length - k` steps from head.  
**Edge Cases:** k=0, k=length (no change), single node.

---

## Problem 13: Copy List with Random Pointer (Medium)

**Problem Statement:** A linked list where each node has a next and random pointer. Create a deep copy.

**Example:**
```
Node1: val=7, next=Node2, random=Node1
Node2: val=13, next=Node3, random=Node1
Output: Exact copy with same structure but independent nodes
```

**Approach:** Three passes: (1) Interleave new nodes between originals, (2) Set random pointers for new nodes, (3) Separate the two lists.

**Python Code:**
```python
def copy_random_list(head):
    if not head:
        return None
    # Step 1: Interleave copies
    curr = head
    while curr:
        copy = Node(curr.val, curr.next, None)
        curr.next = copy
        curr = copy.next
    # Step 2: Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
    # Step 3: Separate lists
    copy_head = head.next
    curr = head
    while curr:
        copy = curr.next
        curr.next = copy.next
        copy.next = copy.next.next if copy.next else None
        curr = curr.next
    return copy_head
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** Interleaving technique avoids using a hash map. `curr.random.next` accesses the copy of the random node.  
**Edge Cases:** Empty list, nodes with random=None.

---

## Problem 14: Sort List (Medium)

**Problem Statement:** Sort a linked list in O(n log n) time using constant space.

**Example:**
```
Input: 4 -> 2 -> 1 -> 3
Output: 1 -> 2 -> 3 -> 4
```

**Approach:** Use merge sort on linked list. Find middle, recursively sort halves, merge sorted halves.

**Python Code:**
```python
def sort_list(head):
    if not head or not head.next:
        return head
    # Find middle
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None
    # Sort halves
    left = sort_list(head)
    right = sort_list(mid)
    # Merge
    dummy = ListNode(0)
    curr = dummy
    while left and right:
        if left.val <= right.val:
            curr.next = left
            left = left.next
        else:
            curr.next = right
            right = right.next
        curr = curr.next
    curr.next = left or right
    return dummy.next
```

**Complexity:** Time O(n log n), Space O(log n) for recursion stack  
**Trick:** For linked list, merge sort is preferred over quicksort (no random access needed, stable).  
**Edge Cases:** Already sorted, reverse sorted, single element.

---

## Problem 15: Add Two Numbers II (Medium)

**Problem Statement:** Numbers stored in forward order. Return sum as a linked list (also forward order).

**Example:**
```
Input: (7 -> 2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 8 -> 0 -> 7 (3424 + 465 = 3889)
```

**Approach:** Use stacks to reverse the digit order, perform addition like Problem 6, then reverse the result.

**Python Code:**
```python
def add_two_numbers_ii(l1, l2):
    s1, s2 = [], []
    while l1:
        s1.append(l1.val)
        l1 = l1.next
    while l2:
        s2.append(l2.val)
        l2 = l2.next
    carry = 0
    head = None
    while s1 or s2 or carry:
        val = carry
        if s1:
            val += s1.pop()
        if s2:
            val += s2.pop()
        carry, digit = divmod(val, 10)
        node = ListNode(digit)
        node.next = head
        head = node
    return head
```

**Complexity:** Time O(m+n), Space O(m+n)  
**Trick:** Stacks naturally reverse the order. Building result by prepending gives correct forward order.  
**Edge Cases:** Different length numbers, final carry overflow.

---

## Problem 16: Odd Even Linked List (Medium)

**Problem Statement:** Group all odd-indexed nodes together followed by even-indexed nodes. First node is odd.

**Example:**
```
Input: 1 -> 2 -> 3 -> 4 -> 5
Output: 1 -> 3 -> 5 -> 2 -> 4
```

**Approach:** Maintain two separate chains (odd and even). Connect odd tail to even head at the end.

**Python Code:**
```python
def odd_even_list(head):
    if not head:
        return None
    odd = head
    even = head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return head
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** Two separate pointers grow the odd and even chains simultaneously. Always check `even` and `even.next` before advancing.  
**Edge Cases:** Single node, two nodes, all same values.

---

## Problem 17: Merge k Sorted Lists (Hard)

**Problem Statement:** Merge k sorted linked lists into one sorted list.

**Example:**
```
Input: lists = [1->4->5, 1->3->4, 2->6]
Output: 1->1->2->3->4->4->5->6
```

**Approach:** Use a min-heap. Push the head of each list. Pop the smallest, add to result, push its next if exists. Repeat until heap is empty.

**Python Code:**
```python
import heapq

def merge_k_lists(lists):
    dummy = ListNode(0)
    curr = dummy
    heap = []
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(heap, (l.val, i, l))
    while heap:
        val, idx, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    return dummy.next
```

**Complexity:** Time O(N log k) where N = total nodes, Space O(k)  
**Trick:** Tuple comparison uses `val` as primary key, `idx` as tiebreaker to avoid comparing ListNode objects.  
**Edge Cases:** Empty input, some empty lists, single list.

---

## Problem 18: Reverse Nodes in k-Group (Hard)

**Problem Statement:** Reverse every k consecutive nodes. If remaining nodes < k, leave as is.

**Example:**
```
Input: 1->2->3->4->5, k = 2
Output: 2->1->4->3->5

Input: 1->2->3->4->5, k = 3
Output: 3->2->1->4->5
```

**Approach:** Check if k nodes exist. If yes, reverse k nodes. Recurse or iterate for the next group. Connect groups together.

**Python Code:**
```python
def reverse_k_group(head, k):
    def reverse(start, end):
        prev, curr = None, start
        while curr is not end:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
    count = 0
    node = head
    while node and count < k:
        node = node.next
        count += 1
    if count < k:
        return head
    new_head = reverse(head, node)
    head.next = reverse_k_group(node, k)
    return new_head
```

**Complexity:** Time O(n), Space O(1) iterative / O(n/k) recursive  
**Trick:** First count k nodes to ensure a full group exists. `reverse(head, node)` reverses up to but not including `node`.  
**Edge Cases:** k=1 (no change), k=length, k>length.

---

## Problem 19: LRU Cache (Hard)

**Problem Statement:** Implement an LRU (Least Recently Used) cache with O(1) get and put operations.

**Example:**
```
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
cache.get(1)      # returns 1
cache.put(3, 3)   # evicts key 2
cache.get(2)      # returns -1 (not found)
```

**Approach:** Use a HashMap mapping keys to DLL nodes, plus a doubly linked list for order. Most recent at head, least at tail. On access, move to head. On capacity exceeded, remove from tail.

**Python Code:**
```python
class DLLNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.head = DLLNode()
        self.tail = DLLNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        node = DLLNode(key, value)
        self._add_to_head(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

**Complexity:** Time O(1) for get/put, Space O(capacity)  
**Trick:** Store key in DLLNode so we can delete from hashmap when evicting from tail. Dummy head/tail simplify edge cases.  
**Edge Cases:** Capacity 1, get on empty cache, put existing key.

---

## Problem 20: Flatten a Multilevel Doubly Linked List (Hard)

**Problem Statement:** A doubly linked list where some nodes have a child pointer to a separate doubly linked list. Flatten all levels into a single list.

**Example:**
```
1 - 2 - 3 - 4 - 5 - 6 - NULL
        |
        7 - 8 - 9 - 10 - NULL
            |
            11 - 12 - NULL
Output: 1-2-3-7-8-11-12-9-10-4-5-6-NULL
```

**Approach:** Iterate through the list. When a node has a child, recurse to flatten the child list. Splice it between current and next. Connect child list's tail to the remaining list.

**Python Code:**
```python
def flatten(head):
    if not head:
        return head
    curr = head
    while curr:
        if curr.child:
            child_head = flatten(curr.child)
            nxt = curr.next
            curr.next = child_head
            child_head.prev = curr
            # Find tail of child list
            tail = child_head
            while tail.next:
                tail = tail.next
            tail.next = nxt
            if nxt:
                nxt.prev = tail
            curr.child = None
        curr = curr.next
    return head
```

**Complexity:** Time O(n), Space O(d) where d = max depth  
**Trick:** Flatten child first, then splice. Always nullify the child pointer after flattening.  
**Edge Cases:** No children, multiple levels, child at the end.

---

---

# PART B: STACK & QUEUE PROBLEMS (20)

---

## Problem 21: Valid Parentheses (Easy)

**Problem Statement:** Given a string containing only `(){}[]`, determine if the input is valid.

**Example:**
```
Input: "()" → True
Input: "()[]{}" → True
Input: "(]" → False
Input: "([)]" → False
Input: "{[]}" → True
```

**Approach:** Push opening brackets onto stack. When encountering a closing bracket, check if stack top matches. Stack must be empty at the end.

**Python Code:**
```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Dict maps closing to opening brackets for O(1) lookup. Check stack empty before accessing top.  
**Edge Cases:** Empty string (True), single bracket (False), unmatched opening (False).

---

## Problem 22: Implement Queue using Stacks (Easy)

**Problem Statement:** Implement a FIFO queue using only two stacks.

**Example:**
```
MyQueue q = new MyQueue();
q.push(1);
q.push(2);
q.peek();    // returns 1
q.pop();     // returns 1
q.empty();   // returns false
```

**Approach:** Use input and output stacks. On dequeue, if output is empty, transfer all from input to output (reversing order). Amortized O(1) per operation.

**Python Code:**
```python
class MyQueue:
    def __init__(self):
        self.input = []
        self.output = []

    def push(self, x):
        self.input.append(x)

    def pop(self):
        self.peek()
        return self.output.pop()

    def peek(self):
        if not self.output:
            while self.input:
                self.output.append(self.input.pop())
        return self.output[-1]

    def empty(self):
        return not self.input and not self.output
```

**Complexity:** Push O(1), Pop/Peek amortized O(1), Space O(n)  
**Trick:** Each element is moved from input to output at most once, giving amortized O(1).  
**Edge Cases:** Pop from empty queue, peek before any push.

---

## Problem 23: Implement Stack using Queues (Easy)

**Problem Statement:** Implement a LIFO stack using only one queue.

**Example:**
```
MyStack stack = new MyStack();
stack.push(1);
stack.push(2);
stack.top();   // returns 2
stack.pop();   // returns 2
stack.empty(); // returns false
```

**Approach:** On push, enqueue the element, then rotate the queue (dequeue and re-enqueue) size-1 times to bring the new element to front.

**Python Code:**
```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]

    def empty(self):
        return len(self.q) == 0
```

**Complexity:** Push O(n), Pop O(1), Space O(n)  
**Trick:** Rotation makes the last pushed element the first in queue, simulating LIFO.  
**Edge Cases:** Pop from empty stack, single element stack.

---

## Problem 24: Min Stack (Easy)

**Problem Statement:** Design a stack that supports push, pop, top, and retrieving the minimum element in O(1).

**Example:**
```
MinStack ms = new MinStack();
ms.push(-2);
ms.push(0);
ms.push(-3);
ms.getMin(); // returns -3
ms.pop();
ms.top();    // returns 0
ms.getMin(); // returns -2
```

**Approach:** Maintain a helper stack that tracks minimums. When pushing, also push the current min. When popping, pop from both stacks.

**Python Code:**
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def get_min(self):
        return self.min_stack[-1]
```

**Complexity:** Time O(1) for all ops, Space O(n)  
**Trick:** `min_stack[-1]` always holds the current minimum. Push `min(val, current_min)` every time.  
**Edge Cases:** Pop when stack has one element, getMin on empty stack.

---

## Problem 25: Baseball Game (Easy)

**Problem Statement:** Calculate score from operations: integer = add, "+" = sum of last two, "D" = double of last, "C" = remove last.

**Example:**
```
Input: ["5","2","C","D","+"]
Output: 30
Explanation: 5 + 2*2 + (5+2*2) = 5 + 4 + 21 = 30
```

**Approach:** Use a stack. Push integer values. On "+", push sum of top two. On "D", push 2*top. On "C", pop. Sum stack at end.

**Python Code:**
```python
def cal_points(operations):
    stack = []
    for op in operations:
        if op == '+':
            stack.append(stack[-1] + stack[-2])
        elif op == 'D':
            stack.append(2 * stack[-1])
        elif op == 'C':
            stack.pop()
        else:
            stack.append(int(op))
    return sum(stack)
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Stack naturally handles the "remove last" and "access previous" operations.  
**Edge Cases:** "C" on empty stack, multiple consecutive "C" operations.

---

## Problem 26: Crawler Log Folder (Easy)

**Problem Statement:** Given a list of folder operations ("../" go up, "./" stay, "x/" go into folder x), find final depth from root.

**Example:**
```
Input: logs = ["d1/","d2/","../","d21/","./"]
Output: 2
Explanation: root -> d1 -> d2 -> (up) d2 -> d21 -> (stay) d21
```

**Approach:** Use a counter (or stack). "../" decrements (min 0), "./" does nothing, anything else increments.

**Python Code:**
```python
def min_operations(logs):
    depth = 0
    for log in logs:
        if log == '../':
            depth = max(0, depth - 1)
        elif log == './':
            continue
        else:
            depth += 1
    return depth
```

**Complexity:** Time O(n), Space O(1)  
**Trick:** A simple counter suffices — no need for a full stack. `max(0, depth-1)` prevents going below root.  
**Edge Cases:** All "../" operations, empty logs array.

---

## Problem 27: Daily Temperatures (Medium)

**Problem Statement:** Given daily temperatures, find how many days you must wait for a warmer temperature. If none, use 0.

**Example:**
```
Input: [73,74,75,71,69,72,76,73]
Output: [1,1,4,2,1,1,0,0]
```

**Approach:** Monotonic decreasing stack storing indices. When a warmer temperature is found, pop from stack and calculate the difference in indices.

**Python Code:**
```python
def daily_temperatures(temperatures):
    n = len(temperatures)
    result = [0] * n
    stack = []  # indices of temperatures awaiting warmer day
    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)
    return result
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Each index is pushed and popped at most once, giving O(n). Stack stores indices waiting for warmer temps.  
**Edge Cases:** All same temperatures, strictly increasing, strictly decreasing.

---

## Problem 28: Stock Span Problem (Medium)

**Problem Statement:** For each day's stock price, find the number of consecutive days (including today) with price <= today's price.

**Example:**
```
Input: [100,80,60,70,60,75,85]
Output: [1,1,1,2,1,4,6]
```

**Approach:** Monotonic decreasing stack of (price, span) pairs. For each price, accumulate spans from previous smaller/equal prices.

**Python Code:**
```python
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span)

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            s_price, s_span = self.stack.pop()
            span += s_span
        self.stack.append((price, span))
        return span
```

**Complexity:** Amortized O(1) per call, Space O(n)  
**Trick:** Store (price, span) pairs instead of just indices — collapses consecutive smaller prices into one entry.  
**Edge Cases:** First call, prices in strictly decreasing order.

---

## Problem 29: Evaluate Reverse Polish Notation (Medium)

**Problem Statement:** Evaluate arithmetic expression in reverse Polish notation (postfix). Operators: +, -, *, /.

**Example:**
```
Input: ["2","1","+","3","*"]
Output: 9
Explanation: ((2 + 1) * 3) = 9
```

**Approach:** Use a stack. Push numbers. When operator encountered, pop two operands, apply operator, push result.

**Python Code:**
```python
def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token in '+-*/':
            b, a = stack.pop(), stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Order matters for `-` and `/`: `a` is the second popped (left operand), `b` is first popped (right operand). Use `int(a/b)` for truncation toward zero.  
**Edge Cases:** Division by zero (not in input), single number input.

---

## Problem 30: Simplify Path (Medium)

**Problem Statement:** Given an absolute Unix path, simplify it (resolve `.`, `..`, and consecutive slashes).

**Example:**
```
Input: "/home/user/../Documents"
Output: "/home/Documents"

Input: "/a//b/../c/"
Output: "/a/c"
```

**Approach:** Split path by `/`. Use a stack: push valid names, pop on `..`, skip `.` and empty strings. Join with `/`.

**Python Code:**
```python
def simplify_path(path):
    stack = []
    parts = path.split('/')
    for part in parts:
        if part == '..':
            if stack:
                stack.pop()
        elif part and part != '.':
            stack.append(part)
    return '/' + '/'.join(stack)
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Splitting by `/` naturally handles consecutive slashes (produces empty strings which are skipped).  
**Edge Cases:** Root path only "/a", path with only "..".

---

## Problem 31: Decode String (Medium)

**Problem Statement:** Decode a string like `"3[a2[c]]"` into `"accaccacc"`.

**Example:**
```
Input: "3[a2[c]]"
Output: "accaccacc"

Input: "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

**Approach:** Use two stacks: one for counts, one for strings. On `[`, push current state. On `]`, pop and repeat. On digits, build number. On letters, build current string.

**Python Code:**
```python
def decode_string(s):
    stack = []
    curr_str = ''
    curr_num = 0
    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == '[':
            stack.append((curr_str, curr_num))
            curr_str = ''
            curr_num = 0
        elif char == ']':
            prev_str, num = stack.pop()
            curr_str = prev_str + curr_str * num
        else:
            curr_str += char
    return curr_str
```

**Complexity:** Time O(n), Space O(n) (output length can be exponential, so space is technically O(output))  
**Trick:** Push both the string and number on `[` so you can restore context when `]` is found.  
**Edge Cases:** Nested brackets, single character strings.

---

## Problem 32: Next Greater Element I (Medium)

**Problem Statement:** Given two arrays (nums1 is subset of nums2), for each element in nums1, find the next greater element in nums2.

**Example:**
```
Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
Output: [-1,3,-1]
Explanation: 4 has no next greater, 1's next greater is 3, 2 has no next greater.
```

**Approach:** Build a next greater map for nums2 using monotonic decreasing stack. Then look up each nums1 element in the map.

**Python Code:**
```python
def next_greater_element(nums1, nums2):
    stack = []
    next_greater = {}
    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)
    return [next_greater.get(num, -1) for num in nums1]
```

**Complexity:** Time O(m+n), Space O(n)  
**Trick:** Monotonic stack processes each element once. Hash map gives O(1) lookup for nums1 queries.  
**Edge Cases:** nums1 empty, all elements in nums2 have no greater.

---

## Problem 33: Next Greater Element II (Medium)

**Problem Statement:** Find the next greater element for each element in a circular array.

**Example:**
```
Input: [1,2,1]
Output: [2,-1,2]
Explanation: Next greater for 1 (index 0) is 2, for 2 is -1, for 1 (index 2) is 2 (wraps around).
```

**Approach:** Iterate through the array twice (modular indexing) with a monotonic stack. Second pass handles wrap-around cases.

**Python Code:**
```python
def next_greater_elements(nums):
    n = len(nums)
    result = [-1] * n
    stack = []  # indices
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return result
```

**Complexity:** Time O(2n) = O(n), Space O(n)  
**Trick:** Only push indices from first pass (i < n). Second pass only pops — never pushes.  
**Edge Cases:** All same elements, single element array.

---

## Problem 34: Car Fleet (Medium)

**Problem Statement:** Cars at different positions travel toward a target at different speeds. A faster car behind a slower one becomes a fleet. Count total fleets.

**Example:**
```
Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
Output: 3
Explanation: Cars at positions 10 and 8 form fleet 1, car at 0 forms fleet 2, cars at 5 and 3 form fleet 3.
```

**Approach:** Sort cars by position descending. Calculate time to reach target. If current car's time > top of stack, it's a new fleet (push). Otherwise, it catches up (don't push).

**Python Code:**
```python
def car_fleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    for pos, spd in cars:
        time = (target - pos) / spd
        if not stack or time > stack[-1]:
            stack.append(time)
    return len(stack)
```

**Complexity:** Time O(n log n), Space O(n)  
**Trick:** Process from closest to target. If a car's time is <= top of stack, it merges into that fleet.  
**Edge Cases:** All cars at same position, single car.

---

## Problem 35: Largest Rectangle in Histogram (Hard)

**Problem Statement:** Find the area of the largest rectangle in a histogram with bars of given heights.

**Example:**
```
Input: [2,1,5,6,2,3]
Output: 10
Explanation: Rectangle with height 5 and width 2 (indices 2-3) has area 10.
```

**Approach:** Monotonic increasing stack of indices. When a shorter bar is found, pop and calculate area using popped bar's height with width extending to current position.

**Python Code:**
```python
def largest_rectangle_area(heights):
    stack = [-1]
    max_area = 0
    for i in range(len(heights)):
        while stack[-1] != -1 and heights[i] < heights[stack[-1]]:
            height = heights[stack.pop()]
            width = i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    while stack[-1] != -1:
        height = heights[stack.pop()]
        width = len(heights) - stack[-1] - 1
        max_area = max(max_area, height * width)
    return max_area
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Stack stores indices in increasing height order. `-1` as sentinel handles the left boundary.  
**Edge Cases:** Empty array, all same heights, strictly increasing heights.

---

## Problem 36: Maximal Rectangle (Hard)

**Problem Statement:** Find the largest rectangle containing only 1s in a binary matrix.

**Example:**
```
Input: [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
Output: 6
```

**Approach:** Build a histogram of heights per row. For each row, apply Largest Rectangle in Histogram (Problem 35).

**Python Code:**
```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0

    def largest_area(h):
        stack = [-1]
        area = 0
        for i in range(len(h)):
            while stack[-1] != -1 and h[i] < h[stack[-1]]:
                height = h[stack.pop()]
                width = i - stack[-1] - 1
                area = max(area, height * width)
            stack.append(i)
        while stack[-1] != -1:
            height = h[stack.pop()]
            width = len(h) - stack[-1] - 1
            area = max(area, height * width)
        return area

    for r in range(rows):
        for c in range(cols):
            heights[c] = heights[c] + 1 if matrix[r][c] == '1' else 0
        max_area = max(max_area, largest_area(heights))
    return max_area
```

**Complexity:** Time O(rows × cols), Space O(cols)  
**Trick:** Treat each row as a histogram base. Heights accumulate downward — reset to 0 on seeing '0'.  
**Edge Cases:** Empty matrix, single row, single column.

---

## Problem 37: Trapping Rain Water (Hard)

**Problem Statement:** Given n non-negative integers representing elevation, compute how much water it can trap after rain.

**Example:**
```
Input: [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

**Approach:** Monotonic decreasing stack. When a taller bar is found, pop and calculate trapped water between current and popped bars.

**Python Code:**
```python
def trap(height):
    stack = []
    water = 0
    for i in range(len(height)):
        while stack and height[i] > height[stack[-1]]:
            bottom = stack.pop()
            if stack:
                width = i - stack[-1] - 1
                h = min(height[i], height[stack[-1]]) - height[bottom]
                water += width * h
        stack.append(i)
    return water
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Water above each popped bar = `(width) × (min(left_bound, right_bound) - bar_height)`. Stack gives us the left bound.  
**Edge Cases:** Empty array, no water trapped, all same heights.

---

## Problem 38: Sliding Window Maximum (Hard)

**Problem Statement:** Given an array and window size k, find the maximum in each sliding window.

**Example:**
```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
```

**Approach:** Monotonic decreasing deque storing indices. Remove indices outside window from front. Remove smaller elements from back. Front always holds max.

**Python Code:**
```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    result = []
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result
```

**Complexity:** Time O(n), Space O(k)  
**Trick:** Deque stores indices in decreasing order of values. Each element is pushed/popped at most once.  
**Edge Cases:** k=1 (return array), k=length (return single max), all same values.

---

## Problem 39: Sliding Window Median (Hard)

**Problem Statement:** Find the median of each sliding window of size k in an array.

**Example:**
```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [1.0,-1.0,-1.0,3.0,5.0,6.0]
```

**Approach:** Use two heaps (max-heap for lower half, min-heap for upper half) with lazy deletion. Balance heaps and compute median from top elements.

**Python Code:**
```python
import heapq

def median_sliding_window(nums, k):
    from sortedcontainers import SortedList
    window = SortedList()
    result = []

    for i, num in enumerate(nums):
        window.add(num)
        if len(window) > k:
            window.remove(nums[i - k])
        if len(window) == k:
            if k % 2 == 1:
                result.append(window[k // 2])
            else:
                result.append((window[k // 2 - 1] + window[k // 2]) / 2)
    return result

def median_sliding_window_heap(nums, k):
    import heapq
    lo, hi = [], []
    delayed = {}
    lo_size = 0
    hi_size = 0
    result = []

    def make_balance():
        nonlocal lo_size, hi_size
        while lo_size > (k + 1) // 2:
            val = -heapq.heappop(lo)
            lo_size -= 1
            heapq.heappush(hi, val)
            hi_size += 1
        while lo_size < (k + 1) // 2 and hi:
            val = heapq.heappop(hi)
            hi_size -= 1
            heapq.heappush(lo, -val)
            lo_size += 1

    def prune(heap, is_max):
        while heap:
            val = heap[0] if not is_max else -heap[0]
            if delayed.get(val, 0) > 0:
                delayed[val] -= 1
                heapq.heappop(heap)
            else:
                break

    for i, num in enumerate(nums):
        if not lo or num <= -lo[0]:
            heapq.heappush(lo, -num)
            lo_size += 1
        else:
            heapq.heappush(hi, num)
            hi_size += 1

        if i >= k:
            out = nums[i - k]
            delayed[out] = delayed.get(out, 0) + 1
            if out <= -lo[0] if lo else False:
                lo_size -= 1
            else:
                hi_size -= 1
            prune(lo, True)
            prune(hi, False)

        make_balance()
        if i >= k - 1:
            result.append(float(-lo[0]))
    return result
```

**Complexity:** Time O(n log k), Space O(k)  
**Trick:** `SortedList` from sortedcontainers gives O(log k) insert/delete. Pure heap approach needs lazy deletion for O(1) window sliding.  
**Edge Cases:** k=1, k=length, all same values.

---

## Problem 40: Car Fleet II (Hard)

**Problem Statement:** Given cars at positions with speeds heading right, find the time at which each car catches up to the car in front of it. If none, return -1.

**Example:**
```
Input: position = [3,5,2], speed = [3,2,4]
Output: [2.0, -1.0, -1.0]
Explanation: Car 0 catches car 1 at time 2.0.
```

**Approach:** Process cars from right to left using a stack. For each pair, compute collision time. Use stack to skip cars that are already part of a faster fleet.

**Python Code:**
```python
def get_collision_times(positions, speeds):
    n = len(positions)
    result = [-1.0] * n
    stack = []  # indices of cars to the right

    for i in range(n - 1, -1, -1):
        while stack:
            j = stack[-1]
            # Cannot catch up if same speed or slower
            if speeds[i] <= speeds[j]:
                stack.pop()
                continue
            # Time to catch car j
            time = (positions[j] - positions[i]) / (speeds[i] - speeds[j])
            # If j catches k before we catch j, skip j
            if result[j] != -1 and time >= result[j]:
                stack.pop()
                continue
            result[i] = time
            break
        stack.append(i)
    return result
```

**Complexity:** Time O(n), Space O(n)  
**Trick:** Each car is pushed/popped at most once. If car j catches car k before car i catches j, then i never catches j directly (it catches the fleet).  
**Edge Cases:** All cars same speed, single car, cars already sorted by position.

---

---

# Quick Reference: Complexity Cheat Sheet

| # | Problem | Time | Space | Key Technique |
|---|---------|------|-------|---------------|
| 1 | Reverse Linked List | O(n) | O(1) | Three pointer reversal |
| 2 | Merge Two Sorted Lists | O(n+m) | O(1) | Dummy node merge |
| 3 | Linked List Cycle | O(n) | O(1) | Floyd's tortoise & hare |
| 4 | Middle of Linked List | O(n) | O(1) | Slow/fast pointers |
| 5 | Remove Duplicates | O(n) | O(1) | Skip duplicate links |
| 6 | Add Two Numbers | O(max(m,n)) | O(max(m,n)) | Digit-by-digit addition |
| 7 | Intersection of Two Lists | O(m+n) | O(1) | Two-pass pointer swap |
| 8 | Linked List Cycle II | O(n) | O(1) | Floyd's phase 2 |
| 9 | Remove Nth From End | O(L) | O(1) | Two pointer gap |
| 10 | Reorder List | O(n) | O(1) | Split + reverse + merge |
| 11 | Swap Nodes in Pairs | O(n) | O(1) | Pointer rewiring |
| 12 | Rotate List | O(n) | O(1) | Circular list trick |
| 13 | Copy Random Pointer | O(n) | O(1) | Interleave copies |
| 14 | Sort List | O(n log n) | O(log n) | Merge sort |
| 15 | Add Two Numbers II | O(m+n) | O(m+n) | Stack reversal |
| 16 | Odd Even Linked List | O(n) | O(1) | Two chain merge |
| 17 | Merge k Sorted Lists | O(N log k) | O(k) | Min-heap |
| 18 | Reverse k-Group | O(n) | O(1) | Count + reverse + recurse |
| 19 | LRU Cache | O(1) | O(cap) | DLL + HashMap |
| 20 | Flatten Multilevel | O(n) | O(d) | Recursive splice |
| 21 | Valid Parentheses | O(n) | O(n) | Stack matching |
| 22 | Queue using Stacks | O(1) amortized | O(n) | Input/output stack |
| 23 | Stack using Queues | O(n) push | O(n) | Queue rotation |
| 24 | Min Stack | O(1) | O(n) | Auxiliary min stack |
| 25 | Baseball Game | O(n) | O(n) | Stack operations |
| 26 | Crawler Log Folder | O(n) | O(1) | Depth counter |
| 27 | Daily Temperatures | O(n) | O(n) | Monotonic stack |
| 28 | Stock Span | O(1) amortized | O(n) | Monotonic stack + span |
| 29 | RPN Evaluation | O(n) | O(n) | Stack computation |
| 30 | Simplify Path | O(n) | O(n) | Stack of path components |
| 31 | Decode String | O(n) | O(n) | Dual stack |
| 32 | Next Greater Element I | O(m+n) | O(n) | Monotonic stack + map |
| 33 | Next Greater Element II | O(n) | O(n) | Circular monotonic stack |
| 34 | Car Fleet | O(n log n) | O(n) | Sort + greedy stack |
| 35 | Largest Rectangle Histogram | O(n) | O(n) | Monotonic stack |
| 36 | Maximal Rectangle | O(rows×cols) | O(cols) | Histogram per row |
| 37 | Trapping Rain Water | O(n) | O(n) | Monotonic stack water calc |
| 38 | Sliding Window Max | O(n) | O(k) | Monotonic deque |
| 39 | Sliding Window Median | O(n log k) | O(k) | Two heaps / sorted list |
| 40 | Car Fleet II | O(n) | O(n) | Reverse order + stack |

---

# Key Patterns to Remember

1. **Floyd's Algorithm** → Cycle detection & finding (Problems 3, 8)
2. **Slow/Fast Pointers** → Middle, cycle, intersection (Problems 3, 4, 7, 8)
3. **Dummy Node** → Simplifies edge cases for linked lists (Problems 2, 9, 11, etc.)
4. **Monotonic Stack** → Next greater element, area problems (Problems 27, 28, 32-38)
5. **Two Stacks** → Decode string, queue implementation (Problems 22, 31)
6. **Min/Max Heap** → Merge k sorted, sliding window median (Problems 17, 39)
7. **Two Heaps** → Median maintenance (Problem 39)
8. **DLL + HashMap** → LRU/LFU cache O(1) operations (Problem 19)
9. **Merge Sort on LL** → O(n log n) without random access (Problem 14)
10. **Interleave Technique** → Copy list without extra space (Problem 13)

---

# Interview Tips for Infosys SP DSE

## Linked List Tips
- Always ask: Is the list sorted? Is there a cycle? Can you modify the list?
- Use dummy nodes to avoid null pointer edge cases
- Slow/fast pointer is your Swiss army knife (middle, cycle, intersection)
- Practice pointer manipulation — visualize the rewiring on paper
- For complex problems (reorder, merge k), break into smaller sub-problems you know

## Stack & Queue Tips
- Monotonic stack is the key pattern — learn it well (Problems 27, 28, 32-38)
- For "next greater" type problems, always think monotonic stack
- Stack is ideal for: matching, nested structures, undo operations
- Deque for sliding window max — it's O(n), not O(nk)
- For LRU Cache, DLL + HashMap is the standard O(1) solution

## General Tips
- Start with brute force, then optimize
- Clarify constraints before coding (can you use extra space?)
- Test with small examples first
- Edge cases: empty input, single element, all same values
- Time complexity matters — O(n) vs O(n²) is the difference between passing and failing

---

---

# Bonus: Quick Problem Identification Guide

| If you see... | Think about... |
|---------------|----------------|
| "reverse a linked list" | Three pointer reversal (Problem 1) |
| "detect cycle" or "has cycle" | Floyd's algorithm (Problem 3) |
| "find middle" | Slow/fast pointers (Problem 4) |
| "merge sorted" | Dummy node merge (Problem 2) |
| "nth from end" | Two pointer gap (Problem 9) |
| "next greater element" | Monotonic decreasing stack (Problems 32, 33) |
| "largest rectangle area" | Monotonic increasing stack (Problem 35) |
| "trapping rain water" | Monotonic stack + area calc (Problem 37) |
| "sliding window max" | Monotonic deque (Problem 38) |
| "valid parentheses" | Stack matching (Problem 21) |
| "decode string" | Dual stack (Problem 31) |
| "LRU cache" | DLL + HashMap (Problem 19) |
| "median of sliding window" | Two heaps or SortedList (Problem 39) |
| "car fleet" | Sort + greedy stack (Problems 34, 40) |

---

*Total: 40 Problems | 20 Linked List + 20 Stack/Queue | Complete Python Solutions*
