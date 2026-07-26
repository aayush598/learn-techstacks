# Advanced Linked List Problems - Complete Guide

## Problem 1: Merge k Sorted Lists

**Statement:** Merge k sorted linked lists into one sorted list.

**Example:**
```
List 1: 1 → 4 → 5 → None
List 2: 1 → 3 → 4 → None
List 3: 2 → 6 → None

Merged: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6 → None
```

### Why This is Hard:
- Merging 2 lists is easy (compare and link)
- But with k lists, we need an efficient strategy
- Naive approach: merge one by one → O(k*n) time
- Better approach: Use min-heap → O(n*log k) time

### The Code (Using Min-Heap):
```python
import heapq

def merge_k_lists(lists):
    # Create a dummy node to build result
    dummy = ListNode(0)
    current = dummy
    
    # Min-heap: stores (value, index, node)
    heap = []
    
    # Step 1: Add first node of each list to heap
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(heap, (l.val, i, l))
    
    # Step 2: Pop smallest, add to result, push next node
    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = ListNode(val)
        current = current.next
        
        # If this list has more nodes, push the next one
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    
    return dummy.next
```

### Visual Walkthrough:

**Initial:**
```
List 1: 1 → 4 → 5
List 2: 1 → 3 → 4
List 3: 2 → 6

Heap: [(1, 0, node1_1), (1, 1, node2_1), (2, 2, node3_1)]
```

**Iteration 1:** Pop (1, 0, node1_1)
```
Add 1 to result
Push node1_1.next = (4, 0, node1_2)

Heap: [(1, 1, node2_1), (2, 2, node3_1), (4, 0, node1_2)]
Result: 1
```

**Iteration 2:** Pop (1, 1, node2_1)
```
Add 1 to result
Push node2_1.next = (3, 1, node2_2)

Heap: [(2, 2, node3_1), (3, 1, node2_2), (4, 0, node1_2)]
Result: 1 → 1
```

**Iteration 3:** Pop (2, 2, node3_1)
```
Add 2 to result
Push node3_1.next = (6, 2, node3_2)

Heap: [(3, 1, node2_2), (4, 0, node1_2), (6, 2, node3_2)]
Result: 1 → 1 → 2
```

**Continue until heap is empty...**

**Final Result:** 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6

**Time:** O(n log k) where n = total nodes, k = number of lists

---

## Problem 2: Flatten a Multilevel Linked List

**Statement:** Given a linked list where nodes may have next and child pointers, flatten it to a single level.

### Visual Example:
```
Before:
1 → 2 → 3 → 4 → 5 → None
            ↓
            6 → 7 → 8 → None
                ↓
                9 → 10 → None

After:
1 → 2 → 3 → 6 → 7 → 9 → 10 → 8 → 4 → 5 → None
```

### The Code:
```python
def flatten(head):
    if not head:
        return head
    
    current = head
    while current:
        if current.child:
            # Save next node
            next_node = current.next
            
            # Flatten child
            child_head = flatten(current.child)
            
            # Connect current to child
            current.next = child_head
            child_head.prev = current
            
            # Find end of child list
            while current.next:
                current = current.next
            
            # Connect end of child to saved next
            current.next = next_node
            if next_node:
                next_node.prev = current
            
            # Remove child pointer
            current.child = None
        
        current = current.next
    
    return head
```

### Step-by-Step:

**Step 1: At node 3, child exists (6)**
```
Before: 3 → 4 → 5
        ↓
        6 → 7 → 8
```

**Step 2: Flatten child recursively**
```
Child becomes: 6 → 7 → 9 → 10 → 8 (flattened)
```

**Step 3: Connect 3 to child head (6)**
```
3 → 6 → 7 → 9 → 10 → 8
```

**Step 4: Connect child end (8) to saved next (4)**
```
3 → 6 → 7 → 9 → 10 → 8 → 4 → 5
```

**Final Result:**
```
1 → 2 → 3 → 6 → 7 → 9 → 10 → 8 → 4 → 5 → None
```

---

## Problem 3: Reverse Linked List II (Reverse from Position m to n)

**Statement:** Reverse a portion of a linked list from position m to n.

**Example:** m=2, n=4, List = [1, 2, 3, 4, 5]
```
Before:  1 → 2 → 3 → 4 → 5 → None
After:   1 → 4 → 3 → 2 → 5 → None
              ↑───↑
           reversed
```

### The Code:
```python
def reverse_between(head, m, n):
    if not head or m == n:
        return head
    
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    # Step 1: Move to position m-1
    for _ in range(m - 1):
        prev = prev.next
    
    # Step 2: Reverse from m to n
    current = prev.next
    next_node = None
    
    for _ in range(n - m + 1):
        temp = current.next
        current.next = next_node
        next_node = current
        current = temp
    
    # Step 3: Connect reversed portion
    prev.next.next = current    # Connect tail of reversed to rest
    prev.next = next_node       # Connect prev to head of reversed
    
    return dummy.next
```

### Visual Walkthrough: m=2, n=4, [1, 2, 3, 4, 5]

**Step 1: Move to position 1 (m-1)**
```
dummy → 1 → 2 → 3 → 4 → 5
        ↑
      prev (at position 1)
```

**Step 2: Reverse 3 nodes (2, 3, 4)**
```
Before: prev → 2 → 3 → 4 → 5
After:  prev → 4 → 3 → 2 → 5
```

**Step 3: Connect**
```
dummy → 1 → 4 → 3 → 2 → 5
```

**Result:** 1 → 4 → 3 → 2 → 5

---

## Problem 4: Partition List

**Statement:** Partition list around value x (nodes < x come before nodes >= x).

**Example:** x=3, List = [1, 4, 3, 2, 5]
```
Before:  1 → 4 → 3 → 2 → 5
After:   1 → 2 → 4 → 3 → 5
         ↑   ↑   ↑───↑
       (<3) (<3) (>=3)
```

### The Code:
```python
def partition(head, x):
    # Create two dummy heads
    less_dummy = ListNode(0)      # For nodes < x
    greater_dummy = ListNode(0)   # For nodes >= x
    
    less = less_dummy
    greater = greater_dummy
    
    while head:
        if head.val < x:
            less.next = head
            less = less.next
        else:
            greater.next = head
            greater = greater.next
        head = head.next
    
    # Connect the two lists
    greater.next = None          # End the greater list
    less.next = greater_dummy.next  # Connect less to greater
    
    return less_dummy.next
```

### Visual Walkthrough: x=3, [1, 4, 3, 2, 5]

**Step 1: Separate into two lists**
```
Less list:     1 → 2
Greater list:  4 → 3 → 5
```

**Step 2: Connect less to greater**
```
less_dummy → 1 → 2 → 4 → 3 → 5
```

**Result:** 1 → 2 → 4 → 3 → 5

---

## Problem 5: Rotate List

**Statement:** Rotate list to the right by k places.

**Example:** k=2, List = [1, 2, 3, 4, 5]
```
Before:  1 → 2 → 3 → 4 → 5
After:   4 → 5 → 1 → 2 → 3
         ↑───↑   ↑───────↑
        moved   stayed
```

### The Code:
```python
def rotate_right(head, k):
    if not head or not head.next or k == 0:
        return head
    
    # Step 1: Find length and last node
    length = 1
    last = head
    while last.next:
        last = last.next
        length += 1
    
    # Step 2: Make it circular
    last.next = head
    
    # Step 3: Find new tail (length - k % length - 1 steps from head)
    k = k % length
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next
    
    # Step 4: New head is next of new tail
    new_head = new_tail.next
    new_tail.next = None  # Break the circle
    
    return new_head
```

### Visual Walkthrough: k=2, [1, 2, 3, 4, 5]

**Step 1: Find length (5) and last node (5)**
```
1 → 2 → 3 → 4 → 5 → None
                    ↑
                  last
```

**Step 2: Make circular**
```
1 → 2 → 3 → 4 → 5
 ↑               ↓
 └───────────────┘
```

**Step 3: Find new tail**
```
k % 5 = 2
Move (5 - 2 - 1) = 2 steps from head
New tail is at position 2 (value 3)

1 → 2 → 3 → 4 → 5
            ↑
         new_tail
```

**Step 4: Break circle**
```
new_head = 4 (new_tail.next)
new_tail.next = None

4 → 5 → 1 → 2 → 3 → None
```

**Result:** 4 → 5 → 1 → 2 → 3

---

## Problem 6: Swap Nodes in Pairs

**Statement:** Swap every two adjacent nodes.

**Example:**
```
Before:  1 → 2 → 3 → 4
After:   2 → 1 → 4 → 3
```

### The Code:
```python
def swap_pairs(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    while prev.next and prev.next.next:
        # Nodes to swap
        first = prev.next
        second = prev.next.next
        
        # Swap
        first.next = second.next
        second.next = first
        prev.next = second
        
        # Move prev forward
        prev = first
    
    return dummy.next
```

### Visual Walkthrough: [1, 2, 3, 4]

**Iteration 1: Swap 1 and 2**
```
Before: prev → 1 → 2 → 3 → 4
After:  prev → 2 → 1 → 3 → 4
```

**Iteration 2: Swap 3 and 4**
```
Before: prev → 2 → 1 → 3 → 4
After:  prev → 2 → 1 → 4 → 3
```

**Result:** 2 → 1 → 4 → 3

---

## Problem 7: Add Two Numbers II

**Statement:** Add two numbers stored in FORWARD order (not reversed).

**Example:**
```
List 1:  3 → 4 → 2 (represents 342)
List 2:  4 → 6 → 5 (represents 465)
Result:  8 → 0 → 7 (represents 807)
```

### The Code:
```python
def add_two_numbers_II(l1, l2):
    # Step 1: Reverse both lists
    l1 = reverse_list(l1)
    l2 = reverse_list(l2)
    
    # Step 2: Add (like reversed version)
    result = add_two_reversed(l1, l2)
    
    # Step 3: Reverse result back
    return reverse_list(result)

def reverse_list(head):
    prev = None
    while head:
        next_temp = head.next
        head.next = prev
        prev = head
        head = next_temp
    return prev
```

### Why reverse twice?
- Addition is easier from least significant digit (right to left)
- So we reverse, add, then reverse back!

---

## Problem 8: Copy List with Random Pointer (O(1) Space)

**Statement:** Deep copy a list with next and random pointers using O(1) extra space.

### The Code (Interweaving Method):
```python
def copy_random_list(head):
    if not head:
        return None
    
    # Step 1: Interweave - insert copy nodes after original
    current = head
    while current:
        copy = ListNode(current.val)
        copy.next = current.next
        current.next = copy
        current = copy.next
    
    # Step 2: Set random pointers for copies
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next
    
    # Step 3: Separate original and copy lists
    copy_head = head.next
    current = head
    while current:
        copy = current.next
        current.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        current = current.next
    
    return copy_head
```

### Visual Walkthrough: [1, 2, 3] with random pointers

**Step 1: Interweave**
```
Before: 1 → 2 → 3
After:  1 → 1' → 2 → 2' → 3 → 3'
```

**Step 2: Set random pointers**
```
If 1.random = 3, then 1'.random = 3'
If 2.random = 1, then 2'.random = 1'
```

**Step 3: Separate**
```
Original: 1 → 2 → 3
Copy:     1' → 2' → 3'
```

**Time:** O(n) | **Space:** O(1) - no extra data structures!

---

## Summary: Advanced Linked List Patterns

| Problem | Technique | Time | Space |
|---------|-----------|------|-------|
| Merge k Sorted Lists | Min-Heap | O(n log k) | O(k) |
| Flatten Multilevel | Recursion | O(n) | O(d) depth |
| Reverse Sublist | Pointers | O(n) | O(1) |
| Partition List | Two Lists | O(n) | O(1) |
| Rotate List | Circular | O(n) | O(1) |
| Swap Pairs | Iterative | O(n) | O(1) |
| Add Forward | Reverse + Add | O(n) | O(1) |
| Copy Random | Interweave | O(n) | O(1) |

## Key Insights for Interviews

1. **Use dummy nodes** - eliminates edge cases for head operations
2. **Two-pass approach** - first count/measure, then operate
3. **Reverse when needed** - makes operations easier in some cases
4. **Heap for k-way merge** - efficient for merging multiple sorted lists
5. **Interweaving technique** - O(1) space for copying lists
6. **Circular list trick** - useful for rotation problems
