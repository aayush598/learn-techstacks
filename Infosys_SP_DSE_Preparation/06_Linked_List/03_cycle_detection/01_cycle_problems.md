# Cycle Detection in Linked Lists - Complete Guide

## What is a Cycle?

A cycle (or loop) occurs when a node's `next` pointer points back to a previous node, creating an infinite loop.

### Visual: A Linked List with a Cycle

```
Normal List (No Cycle):
1 → 2 → 3 → 4 → 5 → None

List with Cycle:
1 → 2 → 3 → 4 → 5
    ↑           ↓
    ← ← ← ← ← ←
    
Node 5 points back to Node 2!
If you traverse, you'll go: 1 → 2 → 3 → 4 → 5 → 2 → 3 → 4 → 5 → 2 → ... (forever!)
```

### Why Detect Cycles?

1. **Avoid infinite loops** in your code
2. **Interview question** - very commonly asked!
3. **Real-world:** Detect circular references in data

---

## Method 1: Floyd's Cycle Detection (Tortoise and Hare)

**The Idea:** Use two pointers moving at different speeds:
- **Slow pointer (Tortoise):** Moves 1 step at a time
- **Fast pointer (Hare):** Moves 2 steps at a time

**Why it works:**
- If there's a cycle, fast will eventually "lap" slow and meet it
- If no cycle, fast will reach the end (None)

### The Code:
```python
def has_cycle(head):
    slow = head      # Tortoise - moves 1 step
    fast = head      # Hare - moves 2 steps
    
    while fast and fast.next:
        slow = slow.next           # Move 1 step
        fast = fast.next.next      # Move 2 steps
        
        if slow == fast:           # They met! Cycle exists
            return True
    
    return False  # Fast reached end, no cycle
```

### Visual Walkthrough: Detect cycle in [1, 2, 3, 4, 5 → back to 2]

```
List with cycle:
1 → 2 → 3 → 4 → 5
    ↑           ↓
    ← ← ← ← ← ←
```

**Step 1: Both start at head (1)**
```
1 → 2 → 3 → 4 → 5
↑
slow, fast
```

**Step 2: slow moves to 2, fast moves to 3**
```
1 → 2 → 3 → 4 → 5
    ↑   ↑
  slow fast
```

**Step 3: slow moves to 3, fast moves to 5**
```
1 → 2 → 3 → 4 → 5
        ↑       ↑
      slow    fast
```

**Step 4: slow moves to 4, fast moves to 3 (wraps around!)**
```
1 → 2 → 3 → 4 → 5
    ↑   ↑       ↑
  fast slow    
```
Wait, fast went: 5 → 2 → 3

**Step 5: slow moves to 5, fast moves to 5**
```
1 → 2 → 3 → 4 → 5
            ↑   ↑
          slow fast

slow == fast! Cycle detected! ✓
```

---

## Method 2: Find the Start of the Cycle

**Problem:** If a cycle exists, find WHERE it starts.

**The Idea:**
1. Find meeting point using slow/fast
2. Move one pointer to head
3. Move both at same speed - they meet at cycle start!

### The Code:
```python
def detect_cycle_start(head):
    slow = head
    fast = head
    
    # Step 1: Detect if cycle exists
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None  # No cycle
    
    # Step 2: Find start of cycle
    slow = head  # Reset slow to head
    while slow != fast:
        slow = slow.next
        fast = fast.next  # Both move 1 step now
    
    return slow  # This is the start of the cycle
```

### Visual Walkthrough: Find cycle start in [1, 2, 3, 4, 5 → back to 2]

**Step 1: Find meeting point (same as before)**
```
Meeting point: node 5 (or wherever they meet)
```

**Step 2: Reset slow to head**
```
1 → 2 → 3 → 4 → 5
↑               ↑
slow (head)    fast (meeting point)
```

**Step 3: Move both 1 step at a time**
```
Iteration 1:
slow → 2, fast → 2
They meet! Start of cycle = node 2 ✓
```

### Why This Works (The Math):

Let's say:
- Distance from head to cycle start = `a`
- Distance from cycle start to meeting point = `b`
- Cycle length = `c`

When they meet:
- Slow traveled: `a + b`
- Fast traveled: `a + b + n*c` (fast went around n times)

Since fast = 2 * slow:
```
a + b + n*c = 2(a + b)
n*c = a + b
a = n*c - b
```

So distance from head to start (`a`) equals distance from meeting point going around cycle (`n*c - b`).

When we move both from head and meeting point at same speed, they meet at cycle start!

---

## Method 3: Using Hash Set

**The Idea:** Store visited nodes. If we see a node again, it's a cycle.

### The Code:
```python
def has_cycle_hashset(head):
    visited = set()
    current = head
    
    while current:
        if current in visited:
            return True  # Found it before! Cycle!
        visited.add(current)
        current = current.next
    
    return False  # Reached end, no cycle
```

**Time:** O(n) | **Space:** O(n) - uses extra memory!

**When to use:** When you need to find the actual cycle nodes, not just detect.

---

## Problem: Linked List Cycle II (LeetCode 142)

**Statement:** Given head of linked list, return the node where cycle begins. If no cycle, return None.

```python
def detectCycle(head):
    slow = fast = head
    
    # Phase 1: Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Phase 2: Find start
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    
    return None
```

---

## Problem: Happy Number (Using Cycle Detection)

**Statement:** A happy number is one where repeatedly summing squares of digits eventually reaches 1. Detect if it enters a cycle (not happy).

### Example:
```
19 → 1²+9² = 82 → 8²+2² = 68 → 6²+8² = 100 → 1²+0²+0² = 1 ✓ Happy!

2 → 2² = 4 → 4² = 16 → 1²+6² = 37 → 3²+7² = 58 → 5²+8² = 89 → 8²+9² = 145 → 1²+4²+5² = 42 → 4²+2² = 20 → 2²+0² = 4 → (cycle!)
```

### The Code:
```python
def is_happy(n):
    def get_next(num):
        total = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total += digit ** 2
        return total
    
    slow = n
    fast = get_next(n)
    
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))
    
    return fast == 1
```

---

## Problem: Palindrome Linked List (Using Cycle Detection)

**Statement:** Check if linked list is a palindrome.

**Approach:** Find middle, reverse second half, compare.

### The Code:
```python
def is_palindrome(head):
    if not head or not head.next:
        return True
    
    # Step 1: Find middle
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Step 2: Reverse second half
    prev = None
    curr = slow.next
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    # Step 3: Compare both halves
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    
    return True
```

### Visual Walkthrough: Check if [1, 2, 1] is palindrome

**Step 1: Find middle**
```
1 → 2 → 1
↑   ↑
slow fast
slow is at 2 (middle)
```

**Step 2: Reverse second half [1]**
```
First half:  1 → 2
Second half: 1 (reversed, same since single node)
```

**Step 3: Compare**
```
left: 1, right: 1 → Equal ✓
left: 2, right: None → Done!

Result: True (palindrome!)
```

---

## Problem: Remove Linked List Cycle

**Statement:** If a linked list has a cycle, remove the cycle.

### The Code:
```python
def remove_cycle(head):
    if not head or not head.next:
        return
    
    slow = fast = head
    
    # Find cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return  # No cycle
    
    # Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    # Find last node in cycle
    while fast.next != slow:
        fast = fast.next
    
    # Remove cycle
    fast.next = None
```

### Visual Walkthrough: Remove cycle from [1, 2, 3, 4, 5 → 2]

**Step 1-2: Find cycle start (node 2)**

**Step 3: Find last node in cycle**
```
fast starts at 2, moves until fast.next == 2
fast ends at 5 (since 5.next == 2)
```

**Step 4: Remove cycle**
```
Before: 5 → 2 (cycle)
After:  5 → None (no cycle)
```

---

## Time Complexity Summary

| Algorithm | Time | Space | Use Case |
|-----------|------|-------|----------|
| Floyd's (detect) | O(n) | O(1) | Check if cycle exists |
| Floyd's (find start) | O(n) | O(1) | Find where cycle begins |
| Hash Set | O(n) | O(n) | Find all nodes in cycle |
| Remove cycle | O(n) | O(1) | Fix circular reference |

## Key Insights

1. **Two pointers moving at different speeds** always meet if there's a cycle
2. **Distance formula** proves why resetting to head works
3. **O(1) space** is always better than O(n) for cycle detection
4. **Happy number** is just cycle detection on a number sequence
5. **Palindrome check** uses cycle detection concept (find middle, reverse)

## Common Interview Follow-ups

1. "What if the list is very long?" → Floyd's is O(1) space
2. "Can you find the length of the cycle?" → Yes, after meeting, count steps
3. "Can you find all nodes in the cycle?" → Yes, from meeting point, traverse cycle
4. "What if there are multiple cycles?" → Impossible in singly linked list (each node has only one next)
