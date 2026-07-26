# Linked List Practice Problems - Detailed Guide

## Problem 1: Reverse Linked List (Easy)

**Statement:** Reverse a singly linked list.

**Why important:** This is the most fundamental linked list problem. Master this first!

### Visual Walkthrough: [1, 2, 3, 4]

**Step-by-step pointer changes:**
```
Initial:
None ← [1] → [2] → [3] → [4] → None
        ↑
      head
      prev=None, current=1

Iteration 1: Reverse 1→2 to 1←2
None ← [1] → None    [2] → [3] → [4] → None
        ↑              ↑
      prev          current
      (prev=1)      (current=2)
      
Action: 1.next = None (prev)
        prev = 1
        current = 2

Iteration 2: Reverse 2→3 to 2←3
None ← [1] ← [2] → None    [3] → [4] → None
               ↑              ↑
             prev          current
             
Action: 2.next = 1 (prev)
        prev = 2
        current = 3

Iteration 3: Reverse 3→4 to 3←4
None ← [1] ← [2] ← [3] → None    [4] → None
                    ↑              ↑
                  prev          current
                  
Action: 3.next = 2 (prev)
        prev = 3
        current = 4

Iteration 4: Reverse 4→None to 4←None
None ← [1] ← [2] ← [3] ← [4] → None
                         ↑
                       prev (new head!)
                       
Action: 4.next = 3 (prev)
        prev = 4
        current = None (loop ends)

Final Result:
None ← [4] ← [3] ← [2] ← [1] → None
        ↑
      head
```

### The Code (With Explanations):
```python
def reverse_list(head):
    prev = None      # Will become new head
    current = head   # Start at original head
    
    while current:
        next_node = current.next   # Save next node (we'll break this link)
        current.next = prev        # Reverse the pointer!
        prev = current             # Move prev forward
        current = next_node        # Move current forward
    
    return prev    # prev is now the new head
```

### Python Tutor Visualization:
```
Step 1: prev=None, current=1
        None ← [1]    [2] → [3] → [4]

Step 2: prev=1, current=2
        None ← [1] ← [2]    [3] → [4]

Step 3: prev=2, current=3
        None ← [1] ← [2] ← [3]    [4]

Step 4: prev=3, current=4
        None ← [1] ← [2] ← [3] ← [4]

Step 5: prev=4, current=None
        DONE! Return prev (4)
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 2: Merge Two Sorted Lists (Easy)

**Statement:** Merge two sorted linked lists into one sorted list.

**Example:**
```
l1: 1 → 3 → 5
l2: 2 → 4 → 6

Merged: 1 → 2 → 3 → 4 → 5 → 6
```

### Visual Walkthrough:

**Initial:**
```
l1: [1] → [3] → [5]
l2: [2] → [4] → [6]
dummy: [0] → None
current = dummy
```

**Iteration 1:** Compare 1 vs 2
```
1 < 2, so add 1
dummy → [1]
current = [1]
l1 = [3]

l1: [3] → [5]
l2: [2] → [4] → [6]
dummy → [1]
```

**Iteration 2:** Compare 3 vs 2
```
3 > 2, so add 2
dummy → [1] → [2]
current = [2]
l2 = [4]

l1: [3] → [5]
l2: [4] → [6]
```

**Iteration 3:** Compare 3 vs 4
```
3 < 4, so add 3
dummy → [1] → [2] → [3]
current = [3]
l1 = [5]
```

**Iteration 4:** Compare 5 vs 4
```
5 > 4, so add 4
dummy → [1] → [2] → [3] → [4]
current = [4]
l2 = [6]
```

**Iteration 5:** Compare 5 vs 6
```
5 < 6, so add 5
dummy → [1] → [2] → [3] → [4] → [5]
current = [5]
l1 = None
```

**Iteration 6:** l1 is None, add remaining l2 (6)
```
dummy → [1] → [2] → [3] → [4] → [5] → [6]
```

### The Code:
```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)     # Dummy node to simplify
    current = dummy          # Pointer to build result
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1      # Take from l1
            l1 = l1.next
        else:
            current.next = l2      # Take from l2
            l2 = l2.next
        current = current.next
    
    # Attach remaining nodes
    current.next = l1 if l1 else l2
    
    return dummy.next    # Skip dummy node
```

**Key Insight:** Dummy node eliminates edge cases for empty result list!

**Time:** O(n + m) | **Space:** O(1)

---

## Problem 3: Linked List Cycle (Easy)

**Statement:** Determine if a linked list has a cycle.

**Floyd's Algorithm (Tortoise and Hare):**
- Slow pointer moves 1 step
- Fast pointer moves 2 steps
- If they meet, there's a cycle!

### Visual: Cycle in [1, 2, 3, 4, 2]

```
Without cycle:  1 → 2 → 3 → 4 → None

With cycle:     1 → 2 → 3 → 4
                    ↑         ↓
                    └─────────┘
```

**Floyd's Algorithm Step-by-Step:**
```
Start: slow=1, fast=1

Step 1: slow=2, fast=3
        1 → [2] → 3 → 4
              ↑    ↑
            slow  fast

Step 2: slow=3, fast=2 (cycle back to 2)
        1 → 2 → [3] → 4
              ↑         ↓
            fast     slow
              └─────────┘

Step 3: slow=4, fast=4 (MEET!)
        They met → Cycle exists!
```

### The Code:
```python
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head      # Tortoise
    fast = head.next # Hare (one step ahead to start)
    
    while slow != fast:
        if not fast or not fast.next:
            return False    # Reached end, no cycle
        slow = slow.next
        fast = fast.next.next
    
    return True    # They met, cycle exists!
```

**Why start fast at head.next?**
- Avoids immediate equality check
- Cleaner loop condition

**Time:** O(n) | **Space:** O(1) - No extra space needed!

---

## Problem 4: Middle of Linked List (Easy)

**Statement:** Find the middle node of a linked list.

**Approach:** Two pointers - slow moves 1 step, fast moves 2 steps.

### Visual: [1, 2, 3, 4, 5]

```
Start: slow=1, fast=1

Step 1: slow=2, fast=3
        [1] → [2] → [3] → [4] → [5]
         ↑           ↑
        slow        fast

Step 2: slow=3, fast=5
        1 → 2 → [3] → 4 → [5]
                    ↑        ↑
                  slow      fast (at end)

fast.next is None → STOP
Middle is slow = 3 ✓
```

### For Even Length [1, 2, 3, 4, 5, 6]:

```
Start: slow=1, fast=1

Step 1: slow=2, fast=3
Step 2: slow=3, fast=5
Step 3: slow=4, fast=None (fast.next.next)

fast is None → STOP
Middle is slow = 4 ✓ (second middle for even)
```

### The Code:
```python
def find_middle(head):
    if not head:
        return None
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow    # slow is at middle
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 5: Remove Duplicates from Sorted List (Easy)

**Statement:** Remove all duplicates from a sorted linked list.

### Visual: [1, 1, 2, 3, 3]

```
Initial: [1] → [1] → [2] → [3] → [3] → None

Step 1: Compare 1 vs 1 (equal!)
        Skip next node
        [1] → [2] → [3] → [3] → None

Step 2: Compare 1 vs 2 (not equal!)
        Move forward
        [1] → [2] → [3] → [3] → None

Step 3: Compare 2 vs 3 (not equal!)
        Move forward
        [1] → [2] → [3] → [3] → None

Step 4: Compare 3 vs 3 (equal!)
        Skip next node
        [1] → [2] → [3] → None

Result: 1 → 2 → 3
```

### The Code:
```python
def delete_duplicates(head):
    current = head
    
    while current and current.next:
        if current.val == current.next.val:
            # Found duplicate! Skip it
            current.next = current.next.next
        else:
            # No duplicate, move forward
            current = current.next
    
    return head
```

**Key Insight:** Since list is sorted, duplicates are always adjacent!

**Time:** O(n) | **Space:** O(1)

---

## Problem 6: Add Two Numbers (Medium)

**Statement:** Add two numbers represented as linked lists (digits in reverse order).

**Example:**
```
Number 1: 342 → represented as 2 → 4 → 3
Number 2: 465 → represented as 5 → 6 → 4
Sum: 807 → represented as 7 → 0 → 8
```

### Visual Walkthrough:

```
l1: [2] → [4] → [3] → None  (342)
l2: [5] → [6] → [4] → None  (465)
carry = 0

Step 1: 2 + 5 + 0 = 7, carry = 0
        result: [7]
        
Step 2: 4 + 6 + 0 = 10, carry = 1
        result: [7] → [0]
        
Step 3: 3 + 4 + 1 = 8, carry = 0
        result: [7] → [0] → [8]
        
Step 4: Both lists None, carry = 0
        DONE!

Result: 7 → 0 → 8 (807) ✓
```

### The Code:
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        # Get values (0 if list ended)
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        # Calculate sum and carry
        total = val1 + val2 + carry
        carry = total // 10        # Integer division for carry
        digit = total % 10         # Remainder for current digit
        
        # Create new node
        current.next = ListNode(digit)
        current = current.next
        
        # Move lists forward
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next
```

**Time:** O(max(n, m)) | **Space:** O(max(n, m))

---

## Problem 7: Remove Nth Node From End (Medium)

**Statement:** Remove the nth node from the end of a linked list.

**Example:** n=2, List = [1, 2, 3, 4, 5]
```
Before: 1 → 2 → 3 → 4 → 5
After:  1 → 2 → 3 → 5 (removed 4, which is 2nd from end)
```

### Two Pointer Technique:

```
Start: dummy → 1 → 2 → 3 → 4 → 5
       ↑
      fast
      slow (both at dummy)

Step 1: Move fast n+1 steps ahead
        fast moves 3 steps: dummy → 1 → 2 → 3
        slow stays at dummy
        
        dummy → 1 → 2 → [3] → 4 → 5
       ↑                    ↑
      slow                 fast

Step 2: Move both until fast reaches end
        fast=3, slow=dummy
        
        [dummy] → 1 → 2 → [3] → 4 → 5
           ↑                    ↑
         slow                 fast
         
        fast=4, slow=1
        
        dummy → [1] → 2 → 3 → [4] → 5
                  ↑              ↑
                slow           fast
                
        fast=5, slow=2
        
        dummy → 1 → [2] → 3 → 4 → [5]
                       ↑           ↑
                     slow        fast (at end)
                     
        fast=None → STOP

Step 3: Remove slow.next (node 3)
        slow is at node 2
        slow.next = slow.next.next
        
        1 → 2 → 4 → 5 (3 is removed)
```

### The Code:
```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0)
    dummy.next = head
    fast = dummy
    slow = dummy
    
    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next
    
    # Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    # Remove the nth node
    slow.next = slow.next.next
    
    return dummy.next
```

**Key Insight:** Gap of n between fast and slow means when fast reaches end, slow is at nth from end!

**Time:** O(L) | **Space:** O(1)

---

## Problem 8: Reorder List (Medium)

**Statement:** Reorder list: L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...

**Example:** [1, 2, 3, 4, 5]
```
Before: 1 → 2 → 3 → 4 → 5
After:  1 → 5 → 2 → 4 → 3
```

### Three-Step Approach:

**Step 1: Find middle**
```
1 → 2 → 3 → 4 → 5
          ↑
        middle (3)
```

**Step 2: Reverse second half**
```
First half: 1 → 2 → 3
Second half: 4 → 5 → None (reversed from 5 → 4)
```

**Step 3: Merge alternating**
```
1 → 5 → 2 → 4 → 3
```

### The Code:
```python
def reorder_list(head):
    if not head or not head.next:
        return
    
    # Step 1: Find middle
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Reverse second half
    prev = None
    current = slow.next
    slow.next = None    # Cut the list
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    # Step 3: Merge alternating
    first = head
    second = prev
    
    while second:
        next1 = first.next
        next2 = second.next
        
        first.next = second
        second.next = next1
        
        first = next1
        second = next2
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 9: Swap Nodes in Pairs (Medium)

**Statement:** Swap every two adjacent nodes.

**Example:** [1, 2, 3, 4]
```
Before: 1 → 2 → 3 → 4
After:  2 → 1 → 4 → 3
```

### Visual Walkthrough:

```
Initial: dummy → 1 → 2 → 3 → 4
               ↑
              prev

Iteration 1: Swap 1 and 2
        prev.next = 2
        1.next = 2.next (=3)
        2.next = 1
        
        dummy → 2 → 1 → 3 → 4
                      ↑
                    prev (moved to 1)

Iteration 2: Swap 3 and 4
        prev.next = 4
        3.next = 4.next (=None)
        4.next = 3
        
        dummy → 2 → 1 → 4 → 3
```

### The Code:
```python
def swap_pairs(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    while prev.next and prev.next.next:
        first = prev.next
        second = first.next
        
        # Perform swap
        first.next = second.next
        second.next = first
        prev.next = second
        
        # Move prev forward
        prev = first
    
    return dummy.next
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 10: Copy List with Random Pointer (Medium)

**Statement:** Deep copy a list with next and random pointers.

### The Hash Map Approach:

```
Original: 1 → 2 → 3
          ↑   ↑   ↑
random:   3   1   2

Step 1: Create mapping
        {1: copy1, 2: copy2, 3: copy3}

Step 2: Set pointers
        copy1.next = mapping[1.next] = copy2
        copy1.random = mapping[1.random] = copy3
        copy2.next = mapping[2.next] = copy3
        copy2.random = mapping[2.random] = copy1
        copy3.next = None
        copy3.random = mapping[3.random] = copy2

Result:
Copy: 1' → 2' → 3'
      ↑    ↑    ↑
random: 3'  1'  2'
```

### The Code:
```python
def copy_random_list(head):
    if not head:
        return None
    
    # Create mapping: original -> copy
    mapping = {}
    current = head
    
    while current:
        mapping[current] = RandomNode(current.val)
        current = current.next
    
    # Set next and random pointers
    current = head
    while current:
        if current.next:
            mapping[current].next = mapping[current.next]
        if current.random:
            mapping[current].random = mapping[current.random]
        current = current.next
    
    return mapping[head]
```

**Time:** O(n) | **Space:** O(n)

---

## Problem 11: Merge k Sorted Lists (Hard)

**Statement:** Merge k sorted linked lists into one sorted list.

**Approach:** Use min-heap to always get the smallest element across all lists.

### Visual: Merge [1→4→5], [1→3→4], [2→6]

```
Heap initially: [(1, list1), (1, list2), (2, list3)]

Step 1: Pop (1, list1), add 1 to result
        Push (4, list1)
        Heap: [(1, list2), (2, list3), (4, list1)]
        Result: 1

Step 2: Pop (1, list2), add 1 to result
        Push (3, list2)
        Heap: [(2, list3), (3, list2), (4, list1)]
        Result: 1 → 1

Step 3: Pop (2, list3), add 2 to result
        Push (6, list3)
        Heap: [(3, list2), (4, list1), (6, list3)]
        Result: 1 → 1 → 2

Continue until heap is empty...
Final: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6
```

### The Code:
```python
import heapq

def merge_k_lists(lists):
    dummy = ListNode(0)
    current = dummy
    heap = []
    
    # Initialize heap with first node of each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = ListNode(val)
        current = current.next
        
        # Push next node from same list
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

**Time:** O(N log k) | **Space:** O(k)

---

## Problem 12: Reverse Nodes in k-Group (Hard)

**Statement:** Reverse nodes in groups of k.

**Example:** k=2, [1, 2, 3, 4]
```
Before: 1 → 2 → 3 → 4
After:  2 → 1 → 4 → 3
```

**Example:** k=3, [1, 2, 3, 4, 5]
```
Before: 1 → 2 → 3 → 4 → 5
After:  3 → 2 → 1 → 4 → 5  (last group kept as is)
```

### The Code:
```python
def reverse_k_group(head, k):
    def reverse_segment(start, end):
        """Reverse from start to end (exclusive)"""
        prev = None
        current = start
        while current != end:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        return prev
    
    dummy = ListNode(0)
    dummy.next = head
    prev_group_end = dummy
    
    while True:
        # Check if k nodes exist
        kth = prev_group_end
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next
        
        group_next = kth.next
        group_start = prev_group_end.next
        
        # Reverse the group
        prev_group_end.next = reverse_segment(group_start, group_next)
        group_start.next = group_next
        
        prev_group_end = group_start
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 13: Sort List (Hard)

**Statement:** Sort a linked list in O(n log n) time.

**Approach:** Merge sort (divide and conquer).

### Visual: [4, 2, 1, 3]

```
Divide:
        [4, 2, 1, 3]
           /     \
      [4, 2]   [1, 3]
       /  \     /  \
     [4] [2]  [1] [3]

Conquer (Merge):
     [4] [2]  [1] [3]
       \  /     \  /
      [2, 4]   [1, 3]
           \     /
        [1, 2, 3, 4]
```

### The Code:
```python
def sort_list(head):
    if not head or not head.next:
        return head
    
    # Find middle
    slow = head
    fast = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    mid = slow.next
    slow.next = None    # Cut the list
    
    # Sort halves recursively
    left = sort_list(head)
    right = sort_list(mid)
    
    # Merge sorted halves
    dummy = ListNode(0)
    current = dummy
    
    while left and right:
        if left.val <= right.val:
            current.next = left
            left = left.next
        else:
            current.next = right
            right = right.next
        current = current.next
    
    current.next = left if left else right
    return dummy.next
```

**Time:** O(n log n) | **Space:** O(log n) recursion stack

---

## Problem 14: LRU Cache (Hard)

**Statement:** Design a data structure that follows LRU cache constraints.

**Operations:**
- `get(key)`: Return value if key exists, else -1
- `put(key, value)`: Insert/update. If capacity exceeded, remove least recently used.

### How it Works:

```
LRU Cache with capacity 2:

put(1, 1): Cache: {1:1}, Order: [1]
put(2, 2): Cache: {1:1, 2:2}, Order: [2, 1]
get(1):    Cache: {1:1, 2:2}, Order: [1, 2] (moved 1 to front)
put(3, 3): Cache: {1:1, 3:3}, Order: [3, 1] (removed 2, LRU)
```

### The Code:
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = DoublyListNode(0)  # dummy head
        self.tail = DoublyListNode(0)  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """Remove node from list"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_front(self, node):
        """Add node right after head (most recent)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)  # Move to front (most recent)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = DoublyListNode(value)
        self.cache[key] = node
        self._add_to_front(node)
        
        if len(self.cache) > self.capacity:
            # Remove LRU (tail.prev)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.val]
```

**Key Insight:** Doubly linked list allows O(1) removal and insertion!

**Time:** O(1) for both get and put | **Space:** O(capacity)

---

## Summary Table

| # | Problem | Difficulty | Time | Space | Key Technique |
|---|---------|------------|------|-------|---------------|
| 1 | Reverse List | Easy | O(n) | O(1) | Three pointers |
| 2 | Merge Sorted | Easy | O(n+m) | O(1) | Dummy node |
| 3 | Cycle Detection | Easy | O(n) | O(1) | Floyd's algorithm |
| 4 | Middle Node | Easy | O(n) | O(1) | Slow/fast pointers |
| 5 | Remove Duplicates | Easy | O(n) | O(1) | Compare adjacent |
| 6 | Add Two Numbers | Medium | O(max(n,m)) | O(max(n,m)) | Carry propagation |
| 7 | Remove Nth From End | Medium | O(L) | O(1) | Two pointer gap |
| 8 | Reorder List | Medium | O(n) | O(1) | Find middle + reverse + merge |
| 9 | Swap Pairs | Medium | O(n) | O(1) | Dummy node + swap |
| 10 | Copy Random | Medium | O(n) | O(n) | Hash map mapping |
| 11 | Merge k Lists | Hard | O(N log k) | O(k) | Min-heap |
| 12 | Reverse k-Group | Hard | O(n) | O(1) | Segment reversal |
| 13 | Sort List | Hard | O(n log n) | O(log n) | Merge sort |
| 14 | LRU Cache | Hard | O(1) | O(capacity) | HashMap + DLL |

## Interview Tips

1. **Always clarify** if list is sorted, has cycles, etc.
2. **Use dummy nodes** to simplify edge cases
3. **Draw the list** before coding
4. **Two pointers** (slow/fast) solve many problems
5. **Practice explaining** your approach before coding
