# Singly Linked List - Complete Beginner Guide

## What is a Linked List?

A linked list is a data structure where elements (called **nodes**) are stored in a chain. Each node contains:
1. **Data** (the value we want to store)
2. **Next** (a pointer/reference to the next node)

Unlike arrays, linked list nodes are NOT stored next to each other in memory. They can be anywhere in memory, connected by these "next" pointers.

## Why Use Linked Lists?

**Problem with Arrays:**
```
Array: [10, 20, 30, 40, 50]
        ↑ stored in contiguous memory

To insert 25 at position 2, we need to SHIFT everything:
[10, 20, __, 30, 40, 50]  ← shift right
[10, 20, 25, 30, 40, 50]  ← insert

This takes O(n) time because we move n elements!
```

**Solution with Linked Lists:**
```
To insert 25 between 20 and 30:
Just change the "next" pointers! No shifting needed!

Before:  [20] → [30]
After:   [20] → [25] → [30]

This takes O(1) time if we're already at the position!
```

---

## Visual: What Does a Node Look Like?

Each node is a box with TWO parts:

```
┌─────────────┐
│  Data: 10   │  ← stores the value
│  Next: ─────┼──→ (points to next node)
└─────────────┘
```

In Python, we create a node like this:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val      # The data part
        self.next = next    # The pointer part (default is None)
```

**What does `next=None` mean?**
- `None` means "this node doesn't point to anything"
- It's the LAST node in the list (tail node)

---

## Visual: A Complete Linked List

Let's create a linked list with values: 10 → 20 → 30 → 40 → None

```
HEAD
  │
  ▼
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ val: 10 │    │ val: 20 │    │ val: 30 │    │ val: 40 │
│ next: ──┼───→│ next: ──┼───→│ next: ──┼───→│ next: None│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
  Node 1         Node 2         Node 3         Node 4
```

**Key observations:**
- `HEAD` is a pointer to the first node (10)
- Each node's `next` points to the next node
- The last node's `next` is `None` (end of list)
- We can only traverse from HEAD to TAIL (one direction)

---

## Step-by-Step: Creating a Linked List

Let's build the list: 10 → 20 → 30

### Step 1: Create the first node (10)
```python
node1 = ListNode(10)
```
```
HEAD → [10 | None]
```
- `node1.val = 10`
- `node1.next = None` (no next node yet)

### Step 2: Create the second node (20)
```python
node2 = ListNode(20)
```
```
[10 | None]    [20 | None]
  ↑               ↑
node1           node2
```
- Now we have two separate nodes, not connected yet!

### Step 3: Connect node1 to node2
```python
node1.next = node2
```
```
[10 | ●───→]  [20 | None]
  ↑               ↑
node1           node2
```
- `node1.next` now points to `node2`

### Step 4: Create and connect the third node (30)
```python
node3 = ListNode(30)
node2.next = node3
```
```
[10 | ●───→]  [20 | ●───→]  [30 | None]
  ↑               ↑               ↑
node1           node2           node3
```

### Final Result:
```
HEAD → [10] → [20] → [30] → None
```

---

## The LinkedList Class

In practice, we don't manually create nodes. We use a LinkedList class:

```python
class LinkedList:
    def __init__(self):
        self.head = None    # Points to first node (empty list has no head)
        self.size = 0       # Track number of nodes
    
    def is_empty(self):
        """Check if list has any nodes"""
        return self.head is None
    
    def __len__(self):
        """Return number of nodes"""
        return self.size
```

**How to use it:**
```python
ll = LinkedList()       # Create empty list
print(ll.is_empty())    # True (no nodes yet)
print(len(ll))          # 0 (size is 0)
```

```
Empty List:
HEAD → None
```

---

## Insertion Operation 1: Insert at Head (Beginning)

**What it does:** Adds a new node at the BEGINNING of the list

**Why useful:** O(1) time - instant! No need to traverse the list.

### The Code:
```python
def insert_at_head(self, val):
    # Step 1: Create new node with the value
    new_node = ListNode(val)
    
    # Step 2: Point new node to current head
    new_node.next = self.head
    
    # Step 3: Update head to point to new node
    self.head = new_node
    
    # Step 4: Increment size
    self.size += 1
```

### Visual Walkthrough: Insert 5 at head of [10, 20, 30]

**Before insertion:**
```
HEAD → [10] → [20] → [30] → None
```

**Step 1: Create new node (5)**
```
[5 | None]  (new_node)

HEAD → [10] → [20] → [30] → None
```

**Step 2: new_node.next = self.head (point new node to 10)**
```
[5 | ●───→]  [10] → [20] → [30] → None
   │           ↑
   └───────────┘  (new_node.next points to head)
```

**Step 3: self.head = new_node (move head to new node)**
```
HEAD → [5] → [10] → [20] → [30] → None
```

**Final result:** List is now: 5 → 10 → 20 → 30

### Complete Example:
```python
ll = LinkedList()
ll.insert_at_head(10)    # List: 10
ll.insert_at_head(20)    # List: 20 → 10
ll.insert_at_head(30)    # List: 30 → 20 → 10
```

---

## Insertion Operation 2: Insert at Tail (End)

**What it does:** Adds a new node at the END of the list

**Why useful:** To add elements in order

### The Code:
```python
def insert_at_tail(self, val):
    # Step 1: Create new node
    new_node = ListNode(val)
    
    # Step 2: If list is empty, new node becomes head
    if not self.head:
        self.head = new_node
        self.size += 1
        return
    
    # Step 3: Otherwise, traverse to the last node
    current = self.head
    while current.next:           # Keep going until we find the last node
        current = current.next
    
    # Step 4: Link last node to new node
    current.next = new_node
    self.size += 1
```

### Visual Walkthrough: Insert 40 at tail of [10, 20, 30]

**Before insertion:**
```
HEAD → [10] → [20] → [30] → None
```

**Step 1: Create new node (40)**
```
[40 | None]  (new_node)
```

**Step 2-3: Traverse to last node (30)**
```
HEAD → [10] → [20] → [30] → None
                       ↑
                    current
```

**Step 4: Link 30 to new node**
```
HEAD → [10] → [20] → [30] → [40] → None
```

**Final result:** List is now: 10 → 20 → 30 → 40

### Complete Example:
```python
ll = LinkedList()
ll.insert_at_tail(10)    # List: 10
ll.insert_at_tail(20)    # List: 10 → 20
ll.insert_at_tail(30)    # List: 10 → 20 → 30
```

---

## Insertion Operation 3: Insert at Position

**What it does:** Adds a new node at a specific position (0-indexed)

**Why useful:** Precise control over where element goes

### The Code:
```python
def insert_at_position(self, val, position):
    # Edge case: empty list or position 0
    if position == 0 or not self.head:
        self.insert_at_head(val)
        return
    
    # Edge case: position beyond list size
    if position >= self.size:
        self.insert_at_tail(val)
        return
    
    # Step 1: Create new node
    new_node = ListNode(val)
    
    # Step 2: Traverse to the node BEFORE the position
    current = self.head
    for _ in range(position - 1):
        current = current.next
    
    # Step 3: Link new node to current's next
    new_node.next = current.next
    
    # Step 4: Link current to new node
    current.next = new_node
    
    self.size += 1
```

### Visual Walkthrough: Insert 25 at position 2 of [10, 20, 30, 40]

**Before insertion:**
```
Position:  0     1     2     3
HEAD → [10] → [20] → [30] → [40] → None
```

**Step 1: Traverse to position 1 (one before target)**
```
HEAD → [10] → [20] → [30] → [40] → None
                       ↑
                    current (at position 1)
```

**Step 2: Create new node and link it**
```
[25 | ●───→]  [30]
     │          ↑
     └──────────┘
```

**Step 3: Link current (20) to new node (25)**
```
HEAD → [10] → [20] → [25] → [30] → [40] → None
```

**Final result:** List is now: 10 → 20 → 25 → 30 → 40

---

## Deletion Operation 1: Delete from Head

**What it does:** Removes the first node

**Why useful:** O(1) time - instant!

### The Code:
```python
def delete_from_head(self):
    if not self.head:
        return None  # List is empty
    
    # Step 1: Save the value to return
    val = self.head.val
    
    # Step 2: Move head to next node
    self.head = self.head.next
    
    # Step 3: Decrement size
    self.size -= 1
    
    return val
```

### Visual Walkthrough: Delete head of [10, 20, 30]

**Before deletion:**
```
HEAD → [10] → [20] → [30] → None
```

**Step 1: Save value (10)**
```
val = 10
```

**Step 2: Move head to next node (20)**
```
HEAD → [20] → [30] → None
       [10] → (disconnected, will be garbage collected)
```

**Final result:** List is now: 20 → 30

---

## Deletion Operation 2: Delete from Tail

**What it does:** Removes the last node

**Why useful:** To remove elements from end

### The Code:
```python
def delete_from_tail(self):
    if not self.head:
        return None  # List is empty
    
    # Edge case: only one node
    if not self.head.next:
        val = self.head.val
        self.head = None
        self.size -= 1
        return val
    
    # Step 1: Traverse to second-to-last node
    current = self.head
    while current.next.next:
        current = current.next
    
    # Step 2: Save value and remove last node
    val = current.next.val
    current.next = None
    
    self.size -= 1
    return val
```

### Visual Walkthrough: Delete tail of [10, 20, 30]

**Before deletion:**
```
HEAD → [10] → [20] → [30] → None
```

**Step 1: Traverse to second-to-last node (20)**
```
HEAD → [10] → [20] → [30] → None
                       ↑
                    current
```

**Step 2: Remove last node**
```
HEAD → [10] → [20] → None
       [30] → (disconnected)
```

**Final result:** List is now: 10 → 20

---

## Deletion Operation 3: Delete by Value

**What it does:** Removes first occurrence of a value

**Why useful:** Remove specific elements

### The Code:
```python
def delete_by_value(self, val):
    if not self.head:
        return False  # List is empty
    
    # Edge case: delete head
    if self.head.val == val:
        self.head = self.head.next
        self.size -= 1
        return True
    
    # Step 1: Find the node BEFORE the one to delete
    current = self.head
    while current.next and current.next.val != val:
        current = current.next
    
    # Step 2: If found, delete it
    if current.next:
        current.next = current.next.next
        self.size -= 1
        return True
    
    return False  # Value not found
```

### Visual Walkthrough: Delete value 20 from [10, 20, 30]

**Before deletion:**
```
HEAD → [10] → [20] → [30] → None
```

**Step 1: Find node before 20 (which is 10)**
```
HEAD → [10] → [20] → [30] → None
       ↑
    current (10's next is 20, which matches!)
```

**Step 2: Skip over 20**
```
HEAD → [10] → [30] → None
       [20] → (disconnected)
```

**Final result:** List is now: 10 → 30

---

## Search Operation

**What it does:** Find if a value exists and get its position

### The Code:
```python
def search(self, val):
    current = self.head
    position = 0
    
    while current:
        if current.val == val:
            return position  # Found! Return position
        current = current.next
        position += 1
    
    return -1  # Not found
```

### Visual Walkthrough: Search for 30 in [10, 20, 30, 40]

**Step 1:** Check node 0 (10) → Not 30, move next
```
HEAD → [10] → [20] → [30] → [40] → None
       ↑
    current
```

**Step 2:** Check node 1 (20) → Not 30, move next
```
HEAD → [10] → [20] → [30] → [40] → None
               ↑
            current
```

**Step 3:** Check node 2 (30) → Found! Return position 2
```
HEAD → [10] → [20] → [30] → [40] → None
                       ↑
                    current
```

---

## Reverse a Linked List

**What it does:** Reverses the direction of all pointers

**Why useful:** Common interview question, O(n) time

### The Code (Iterative):
```python
def reverse(self):
    prev = None           # Will become new head
    current = self.head   # Start from head
    
    while current:
        next_node = current.next   # Save next node
        current.next = prev        # Reverse the pointer
        prev = current              # Move prev forward
        current = next_node         # Move current forward
    
    self.head = prev    # Update head to new first node
```

### Visual Walkthrough: Reverse [10, 20, 30]

**Initial state:**
```
prev = None
current → [10] → [20] → [30] → None
```

**Iteration 1:**
```
next_node = 20 (save what comes after 10)
current.next = None (reverse: 10 now points to None)
prev = 10 (move prev forward)
current = 20 (move current forward)

None ← [10]    [20] → [30] → None
       ↑        ↑
      prev    current
```

**Iteration 2:**
```
next_node = 30 (save what comes after 20)
current.next = 10 (reverse: 20 now points to 10)
prev = 20 (move prev forward)
current = 30 (move current forward)

None ← [10] ← [20]    [30] → None
              ↑        ↑
             prev    current
```

**Iteration 3:**
```
next_node = None (save what comes after 30)
current.next = 20 (reverse: 30 now points to 20)
prev = 30 (move prev forward)
current = None (move current forward, loop ends)

None ← [10] ← [20] ← [30]
                      ↑
                     prev (new head!)
```

**Final result:** List is now: 30 → 20 → 10

---

## Find Middle of Linked List

**What it does:** Finds the middle node using slow/fast pointers

**Why useful:** O(n) time, O(1) space - no extra memory!

### The Code:
```python
def find_middle(self):
    slow = self.head      # Moves 1 step
    fast = self.head      # Moves 2 steps
    
    while fast and fast.next:
        slow = slow.next           # Move 1 step
        fast = fast.next.next      # Move 2 steps
    
    return slow  # When fast reaches end, slow is at middle
```

### Visual Walkthrough: Find middle of [10, 20, 30, 40, 50]

**Step 1:** Both start at head
```
HEAD → [10] → [20] → [30] → [40] → [50] → None
       ↑
      slow, fast
```

**Step 2:** slow moves 1, fast moves 2
```
HEAD → [10] → [20] → [30] → [40] → [50] → None
               ↑             ↑
              slow          fast
```

**Step 3:** slow moves 1, fast moves 2
```
HEAD → [10] → [20] → [30] → [40] → [50] → None
                       ↑                     ↑
                      slow                  fast (reached end!)
```

**Step 4:** fast.next is None, loop stops. Return slow (30)!

**Middle node:** 30 ✓

---

## Print/Display the Linked List

### The Code:
```python
def display(self):
    elements = []
    current = self.head
    while current:
        elements.append(str(current.val))
        current = current.next
    return " → ".join(elements) + " → None"
```

**Example:**
```python
ll = LinkedList()
ll.insert_at_tail(10)
ll.insert_at_tail(20)
ll.insert_at_tail(30)
print(ll.display())  # Output: 10 → 20 → 30 → None
```

---

## Complete Working Example

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def insert_at_head(self, val):
        new_node = ListNode(val)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_at_tail(self, val):
        new_node = ListNode(val)
        if not self.head:
            self.head = new_node
            self.size += 1
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        self.size += 1
    
    def delete_from_head(self):
        if not self.head:
            return None
        val = self.head.val
        self.head = self.head.next
        self.size -= 1
        return val
    
    def search(self, val):
        current = self.head
        position = 0
        while current:
            if current.val == val:
                return position
            current = current.next
            position += 1
        return -1
    
    def display(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.val))
            current = current.next
        return " → ".join(elements) + " → None"

# Test it!
ll = LinkedList()
ll.insert_at_tail(10)
ll.insert_at_tail(20)
ll.insert_at_tail(30)
print(ll.display())        # 10 → 20 → 30 → None
print(f"Size: {len(ll)}")  # Size: 3
print(f"Search 20: {ll.search(20)}")  # Search 20: 1
print(f"Delete head: {ll.delete_from_head()}")  # Delete head: 10
print(ll.display())        # 20 → 30 → None
```

---

## Time Complexity Summary

| Operation | Time | Why |
|-----------|------|-----|
| Insert at Head | O(1) | Just change 2 pointers |
| Insert at Tail | O(n) | Must traverse to end |
| Insert at Position | O(n) | Must traverse to position |
| Delete from Head | O(1) | Just move head pointer |
| Delete from Tail | O(n) | Must traverse to second-to-last |
| Search | O(n) | Must check each node |
| Reverse | O(n) | Visit each node once |

## Common Mistakes to Avoid

1. **Forgetting edge cases:** Empty list, single node, delete head
2. **Losing reference:** When connecting nodes, always save the next node first
3. **Infinite loops:** Make sure your while loop has a way to exit
4. **Off-by-one errors:** Be careful with position indices (0-based)

## Key Insights for Interview

1. **Slow/Fast pointer technique:** Used for cycle detection, finding middle
2. **Dummy head node:** Simplifies edge cases in insertion/deletion
3. **Two-pass approach:** First count nodes, then operate (if needed)
4. **In-place operations:** Always prefer O(1) space solutions
