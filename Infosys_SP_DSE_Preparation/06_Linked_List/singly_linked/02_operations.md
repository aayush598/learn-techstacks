# Linked List Operations - Complete Guide

## Operation 1: Merge Two Sorted Linked Lists

**Problem:** Given two sorted linked lists, merge them into one sorted list.

**Why useful:** Fundamental operation, used in merge sort and many other algorithms.

### Visual Example: Merge [1, 3, 5] and [2, 4, 6]

```
List 1:  1 → 3 → 5 → None
List 2:  2 → 4 → 6 → None

Merged:  1 → 2 → 3 → 4 → 5 → 6 → None
```

### The Code:
```python
def merge_two_lists(l1, l2):
    # Create a dummy node to simplify the logic
    dummy = ListNode(0)
    current = dummy  # pointer to build the merged list
    
    # Compare and link nodes
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1    # Link l1's node
            l1 = l1.next         # Move l1 forward
        else:
            current.next = l2    # Link l2's node
            l2 = l2.next         # Move l2 forward
        current = current.next   # Move current forward
    
    # Attach remaining nodes (one list might be longer)
    current.next = l1 if l1 else l2
    
    return dummy.next  # Skip dummy, return actual head
```

### Step-by-Step Walkthrough:

**Iteration 1:**
```
List 1:  1 → 3 → 5
List 2:  2 → 4 → 6

Compare 1 vs 2: 1 is smaller
Link 1 to merged list
Move l1 forward

dummy → 1
         ↑
        current
```

**Iteration 2:**
```
List 1:  3 → 5
List 2:  2 → 4 → 6

Compare 3 vs 2: 2 is smaller
Link 2 to merged list
Move l2 forward

dummy → 1 → 2
              ↑
            current
```

**Iteration 3:**
```
List 1:  3 → 5
List 2:  4 → 6

Compare 3 vs 4: 3 is smaller
Link 3 to merged list
Move l1 forward

dummy → 1 → 2 → 3
                  ↑
                current
```

**Iteration 4:**
```
List 1:  5
List 2:  4 → 6

Compare 5 vs 4: 4 is smaller
Link 4 to merged list
Move l2 forward

dummy → 1 → 2 → 3 → 4
                      ↑
                    current
```

**Iteration 5:**
```
List 1:  5
List 2:  6

Compare 5 vs 6: 5 is smaller
Link 5 to merged list
Move l1 forward

dummy → 1 → 2 → 3 → 4 → 5
                          ↑
                        current
```

**Iteration 6: l1 is None, exit loop**

**Step: Attach remaining**
```
l2 still has: 6 → None
Link it: 6 to merged list

dummy → 1 → 2 → 3 → 4 → 5 → 6 → None
```

**Return dummy.next (node 1)**

---

## Operation 2: Add Two Numbers (as Linked Lists)

**Problem:** Add two numbers represented as linked lists (digits in reverse order).

**Example:** 342 + 465 = 807
```
List 1:  2 → 4 → 3 → None  (represents 342 in reverse)
List 2:  5 → 6 → 4 → None  (represents 465 in reverse)
Result:  7 → 0 → 8 → None  (represents 807 in reverse)
```

### The Code:
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    # Add digit by digit
    while l1 or l2 or carry:
        # Get values (0 if list is exhausted)
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        # Calculate sum and carry
        total = val1 + val2 + carry
        carry = total // 10      # e.g., 15 // 10 = 1
        digit = total % 10       # e.g., 15 % 10 = 5
        
        # Create new node with digit
        current.next = ListNode(digit)
        current = current.next
        
        # Move forward in lists
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next
```

### Step-by-Step Walkthrough: Add 342 + 465

**Iteration 1:**
```
l1: 2, l2: 5, carry: 0
total = 2 + 5 + 0 = 7
carry = 0, digit = 7

Create node with 7
dummy → 7
```

**Iteration 2:**
```
l1: 4, l2: 6, carry: 0
total = 4 + 6 + 0 = 10
carry = 1, digit = 0

Create node with 0
dummy → 7 → 0
```

**Iteration 3:**
```
l1: 3, l2: 4, carry: 1
total = 3 + 4 + 1 = 8
carry = 0, digit = 8

Create node with 8
dummy → 7 → 0 → 8
```

**Iteration 4:** l1 and l2 are None, carry is 0 → Loop ends

**Result:** 7 → 0 → 8 → None (represents 807)

---

## Operation 3: Remove Nth Node From End

**Problem:** Remove the Nth node from the end of the list.

**Why useful:** Common interview question, uses two-pointer technique.

### Visual Example: Remove 2nd from end of [1, 2, 3, 4, 5]

```
Before:  1 → 2 → 3 → 4 → 5 → None
                    ↑
                Remove this (2nd from end)

After:   1 → 2 → 3 → 5 → None
```

### The Code:
```python
def remove_nth_from_end(head, n):
    # Step 1: Create dummy node (handles edge case of removing head)
    dummy = ListNode(0)
    dummy.next = head
    
    # Step 2: Use two pointers with gap of n
    fast = dummy
    slow = dummy
    
    # Move fast n+1 steps ahead
    for _ in range(n + 1):
        fast = fast.next
    
    # Step 3: Move both until fast reaches end
    while fast:
        fast = fast.next
        slow = slow.next
    
    # Step 4: Remove the node after slow
    slow.next = slow.next.next
    
    return dummy.next
```

### Step-by-Step: Remove 2nd from end of [1, 2, 3, 4, 5]

**Initial state:**
```
dummy → 1 → 2 → 3 → 4 → 5 → None
 ↑       ↑
dummy   fast, slow
```

**Move fast 3 steps (n+1 = 2+1 = 3):**
```
dummy → 1 → 2 → 3 → 4 → 5 → None
 ↑               ↑
dummy           fast
                    ↑
                   slow
```

**Move both until fast reaches None:**
```
dummy → 1 → 2 → 3 → 4 → 5 → None
                         ↑     ↑
                        slow  fast (None)
```

**Remove slow.next (node 4):**
```
dummy → 1 → 2 → 3 → 5 → None
```

**Result:** 1 → 2 → 3 → 5 → None

---

## Operation 4: Reorder List

**Problem:** Reorder: L0 → Ln → L1 → Ln-1 → L2 → Ln-2...

**Example:**
```
Before:  1 → 2 → 3 → 4 → 5 → None
After:   1 → 5 → 2 → 4 → 3 → None
```

### The Code:
```python
def reorder_list(head):
    if not head or not head.next:
        return
    
    # Step 1: Find middle
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Reverse second half
    prev, curr = None, slow.next
    slow.next = None  # Cut the list
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    # Step 3: Merge two halves
    first, second = head, prev
    while second:
        temp1, temp2 = first.next, second.next
        first.next = second
        second.next = temp1
        first = temp1
        second = temp2
```

### Visual Walkthrough: Reorder [1, 2, 3, 4, 5]

**Step 1: Find middle (3)**
```
1 → 2 → 3 → 4 → 5
          ↑
        slow (middle)
```

**Step 2: Reverse second half (4 → 5 becomes 5 → 4)**
```
First half:  1 → 2 → 3
Second half: 5 → 4 (reversed)
```

**Step 3: Merge alternately**
```
Take 1 from first:  1
Take 5 from second: 1 → 5
Take 2 from first:  1 → 5 → 2
Take 4 from second: 1 → 5 → 2 → 4
Take 3 from first:  1 → 5 → 2 → 4 → 3
```

**Result:** 1 → 5 → 2 → 4 → 3 → None

---

## Operation 5: Copy List with Random Pointer

**Problem:** Deep copy a linked list where each node has next and random pointer.

**Why useful:** Tests understanding of pointer manipulation and hash maps.

### Visual Example:
```
Original:  1 → 2 → 3
           ↑   ↑   ↑
           |   |   |
           3   1   1  (random pointers)

Copy:      1' → 2' → 3'
           ↑    ↑    ↑
           |    |    |
           3'   1'   1'  (random pointers to COPIED nodes)
```

### The Code (HashMap Approach):
```python
def copy_random_list(head):
    if not head:
        return None
    
    # Step 1: Create mapping of old nodes to new nodes
    mapping = {}
    current = head
    while current:
        mapping[current] = ListNode(current.val)
        current = current.next
    
    # Step 2: Connect next and random pointers
    current = head
    while current:
        if current.next:
            mapping[current].next = mapping[current.next]
        if current.random:
            mapping[current].random = mapping[current.random]
        current = current.next
    
    return mapping[head]
```

### Step-by-Step:

**Step 1: Create all new nodes**
```
Original:  1 → 2 → 3
Mapping:   {1: 1', 2: 2', 3: 3'}
```

**Step 2: Connect next pointers**
```
1'.next = mapping[1.next] = mapping[2] = 2'
2'.next = mapping[2.next] = mapping[3] = 3'
3'.next = None
```

**Step 3: Connect random pointers**
```
1'.random = mapping[1.random] = mapping[3] = 3'
2'.random = mapping[2.random] = mapping[1] = 1'
3'.random = mapping[3.random] = mapping[1] = 1'
```

**Result:** Complete deep copy with independent nodes!

---

## Operation 6: Reverse Nodes in k-Group

**Problem:** Reverse every k consecutive nodes in the list.

**Example:** k=2, list = [1, 2, 3, 4, 5]
```
Before:  1 → 2 → 3 → 4 → 5 → None
After:   2 → 1 → 4 → 3 → 5 → None
         ↑───↑   ↑───↑   ↑
         rev   rev   (not enough for k=2)
```

### The Code:
```python
def reverse_k_group(head, k):
    # Check if k nodes exist
    def has_k_nodes(node, k):
        count = 0
        while node and count < k:
            node = node.next
            count += 1
        return count == k
    
    # Reverse k nodes
    def reverse_group(start, k):
        prev, curr = None, start
        for _ in range(k):
            next_temp = curr.next
            curr.next = prev
            prev = curr
            curr = next_temp
        return prev, start  # new_head, tail
    
    dummy = ListNode(0)
    dummy.next = head
    prev_group_tail = dummy
    
    while has_k_nodes(prev_group_tail.next, k):
        group_head = prev_group_tail.next
        new_head, tail = reverse_group(group_head, k)
        prev_group_tail.next = new_head
        prev_group_tail = tail
    
    return dummy.next
```

### Visual Walkthrough: k=2, [1, 2, 3, 4, 5]

**Reverse first group (1, 2):**
```
Before:  dummy → 1 → 2 → 3 → 4 → 5
After:   dummy → 2 → 1 → 3 → 4 → 5
```

**Reverse second group (3, 4):**
```
Before:  dummy → 2 → 1 → 3 → 4 → 5
After:   dummy → 2 → 1 → 4 → 3 → 5
```

**Last group (5) has fewer than k nodes → leave as is**

**Result:** 2 → 1 → 4 → 3 → 5 → None

---

## Operation 7: Sort List (Merge Sort)

**Problem:** Sort a linked list in O(n log n) time.

**Why useful:** Merge sort is the most efficient sort for linked lists.

### The Code:
```python
def sort_list(head):
    if not head or not head.next:
        return head
    
    # Step 1: Find middle
    slow, fast = head, head.next
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Split into two halves
    mid = slow.next
    slow.next = None  # Cut
    
    # Step 3: Recursively sort both halves
    left = sort_list(head)
    right = sort_list(mid)
    
    # Step 4: Merge sorted halves
    return merge_two_lists(left, right)
```

### Visual Walkthrough: Sort [4, 2, 1, 3]

**Step 1: Split**
```
[4, 2, 1, 3] → left=[4, 2], right=[1, 3]
```

**Step 2: Recursively sort left [4, 2]**
```
Split: left=[4], right=[2]
Merge: [2, 4]
```

**Step 3: Recursively sort right [1, 3]**
```
Split: left=[1], right=[3]
Merge: [1, 3]
```

**Step 4: Merge [2, 4] and [1, 3]**
```
Compare 2 vs 1: take 1
Compare 2 vs 3: take 2
Compare 4 vs 3: take 3
Remaining: take 4

Result: 1 → 2 → 3 → 4
```

---

## Operation 8: Odd-Even Linked List

**Problem:** Group all odd-indexed nodes together, then even-indexed.

**Example:**
```
Before:  1 → 2 → 3 → 4 → 5 → None
After:   1 → 3 → 5 → 2 → 4 → None
         ↑───↑   ↑   ↑───↑
         odd     odd  even
```

### The Code:
```python
def odd_even_list(head):
    if not head:
        return None
    
    odd = head
    even = head.next
    even_head = even  # Save reference to connect later
    
    while even and even.next:
        odd.next = odd.next.next    # Skip even node
        odd = odd.next              # Move odd forward
        even.next = even.next.next  # Skip odd node
        even = even.next            # Move even forward
    
    # Connect odd list to even list
    odd.next = even_head
    
    return head
```

### Visual Walkthrough: [1, 2, 3, 4, 5]

**Initial:**
```
odd: 1, even: 2, even_head: 2
1 → 2 → 3 → 4 → 5
↑   ↑
odd even
```

**Iteration 1:**
```
odd.next = 3 (skip 2)
odd = 3
even.next = 4 (skip 3)
even = 4

1 → 3 → 5    2 → 4
    ↑         ↑
   odd       even
```

**Iteration 2:**
```
odd.next = 5 (skip None? No, 3.next = 5)
odd = 5
even.next = None (5.next = None)
even = None (loop ends)
```

**Connect odd to even_head:**
```
5.next = 2

1 → 3 → 5 → 2 → 4 → None
```

---

## Summary: Key Patterns for Linked List

| Pattern | When to Use | Time |
|---------|-------------|------|
| Slow/Fast Pointer | Find middle, detect cycle | O(n) |
| Dummy Node | Simplify insertion/deletion | O(n) |
| Two Pointers | Merge, find intersection | O(n) |
| Reverse In-Place | Reverse list or parts | O(n) |
| HashMap | Copy with random pointers | O(n) |
| Merge Sort | Sort linked list | O(n log n) |

## Common Edge Cases to Handle

1. **Empty list** (head is None)
2. **Single node** (head.next is None)
3. **Two nodes** (special case for some operations)
4. **Removing head** (use dummy node)
5. **List length < k** (for k-group operations)
6. **Circular reference** (cycle detection)
