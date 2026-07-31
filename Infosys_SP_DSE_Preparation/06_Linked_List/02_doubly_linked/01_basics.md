# Doubly Linked List - Complete Guide

## What is a Doubly Linked List?

A doubly linked list is like a singly linked list, but each node has TWO pointers:
- **Next** pointer (points to next node)
- **Previous** pointer (points to previous node)

### Visual Comparison:

**Singly Linked List:**
```
[10 | ●───→]  [20 | ●───→]  [30 | None]
  ↑              ↑              ↑
Node 1         Node 2         Node 3

Each node only knows about the NEXT node
```

**Doubly Linked List:**
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
         ↑    ↑           ↑    ↑           ↑    ↑
       prev next        prev next        prev next
       Node 1          Node 2          Node 3

Each node knows about BOTH next AND previous nodes!
```

### Why Use Doubly Linked List?

**Advantage over Singly Linked List:**
1. **Bidirectional traversal** - can go forward AND backward
2. **Delete from tail** - O(1) instead of O(n)!
3. **Insert before a node** - O(1) instead of O(n)!

**Disadvantage:**
1. **More memory** - each node stores an extra pointer
2. **More complex** - need to update TWO pointers during operations

---

## Node Structure

Each node has THREE parts:
```
┌─────────────────────────┐
│  prev  │  data  │  next │
│  (←)   │  (10)  │  (→)  │
└─────────────────────────┘
```

### Python Implementation:
```python
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val      # The data
        self.prev = prev    # Pointer to previous node
        self.next = next    # Pointer to next node
```

### Creating a Node:
```python
node = DoublyListNode(10)
# node.val = 10
# node.prev = None (no previous node yet)
# node.next = None (no next node yet)
```

---

## Visual: Building a Doubly Linked List

Let's build: 10 ↔ 20 ↔ 30

### Step 1: Create first node
```python
node1 = DoublyListNode(10)
```
```
None ← [● | 10 | ●] → None
         ↑
       node1
```
- `node1.prev = None`
- `node1.next = None`

### Step 2: Create second node
```python
node2 = DoublyListNode(20)
```
```
None ← [● | 10 | ●] → None

None ← [● | 20 | ●] → None
         ↑
       node2
```

### Step 3: Connect node1 and node2
```python
node1.next = node2      # node1's next points to node2
node2.prev = node1      # node2's prev points to node1
```
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] → None
```

### Step 4: Create and connect third node
```python
node3 = DoublyListNode(30)
node2.next = node3
node3.prev = node2
```
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
```

### Final Result:
```
HEAD → [10] ↔ [20] ↔ [30] ← TAIL
```

---

## DoublyLinkedList Class

```python
class DoublyLinkedList:
    def __init__(self):
        self.head = None    # First node
        self.tail = None    # Last node
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
```

**Key difference from singly linked list:**
- We track BOTH `head` and `tail`!
- This allows O(1) operations at both ends

---

## Operation 1: Insert at Head (O(1))

**What it does:** Adds node at the BEGINNING

### The Code:
```python
def insert_at_head(self, val):
    new_node = DoublyListNode(val)
    
    if self.is_empty():
        # Empty list: both head and tail point to new node
        self.head = new_node
        self.tail = new_node
    else:
        # Connect new node to current head
        new_node.next = self.head
        self.head.prev = new_node
        self.head = new_node  # Update head
    
    self.size += 1
```

### Visual Walkthrough: Insert 5 at head of [10, 20, 30]

**Before:**
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
        ↑ HEAD                                    ↑ TAIL
```

**Step 1: Create new node (5)**
```
None ← [● | 5 | ●] → None  (new_node)
```

**Step 2: new_node.next = self.head (point to 10)**
```
None ← [● | 5 | ●] → [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
```

**Step 3: self.head.prev = new_node (10's prev points to 5)**
```
None ← [● | 5 | ●] ←→ [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
```

**Step 4: self.head = new_node (move head to 5)**
```
HEAD → [5] ↔ [10] ↔ [20] ↔ [30] ← TAIL
```

**Result:** 5 → 10 → 20 → 30

---

## Operation 2: Insert at Tail (O(1))

**What it does:** Adds node at the END

**Why O(1)?** Because we have `self.tail` pointer!

### The Code:
```python
def insert_at_tail(self, val):
    new_node = DoublyListNode(val)
    
    if self.is_empty():
        self.head = new_node
        self.tail = new_node
    else:
        new_node.prev = self.tail
        self.tail.next = new_node
        self.tail = new_node  # Update tail
    
    self.size += 1
```

### Visual Walkthrough: Insert 40 at tail of [10, 20, 30]

**Before:**
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
        ↑ HEAD                                    ↑ TAIL
```

**Step 1: Create new node (40)**
```
None ← [● | 40 | ●] → None
```

**Step 2: new_node.prev = self.tail (point to 30)**
```
[● | 40 | ●] ← [● | 30 | ●]
    ↑ prev
```

**Step 3: self.tail.next = new_node (30's next points to 40)**
```
[● | 30 | ●] ←→ [● | 40 | ●]
```

**Step 4: self.tail = new_node (move tail to 40)**
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] ←→ [● | 40 | ●] → None
        ↑ HEAD                                              ↑ TAIL
```

**Result:** 10 → 20 → 30 → 40

---

## Operation 3: Delete a Node (O(1))

**What it does:** Removes a specific node

**Why O(1)?** Because we can directly access both neighbors via prev/next!

### The Code:
```python
def delete_node(self, node):
    # Case 1: Node is head
    if node == self.head:
        self.head = node.next
    
    # Case 2: Node is tail
    if node == self.tail:
        self.tail = node.prev
    
    # Case 3: Update neighbors' pointers
    if node.prev:
        node.prev.next = node.next
    if node.next:
        node.next.prev = node.prev
    
    self.size -= 1
```

### Visual Walkthrough: Delete node with value 20 from [10, 20, 30]

**Before:**
```
None ← [● | 10 | ●] ←→ [● | 20 | ●] ←→ [● | 30 | ●] → None
```

**Step 1: node.prev (10) should skip over 20**
```
10.next = 30 (skip 20)

[● | 10 | ●] → [● | 30 | ●]
                 [● | 20 | ●] (disconnected)
```

**Step 2: node.next (30) should skip over 20**
```
30.prev = 10 (skip 20)

None ← [● | 10 | ●] ←→ [● | 30 | ●] → None
```

**Result:** 10 → 30

---

## Operation 4: Delete from Head (O(1))

```python
def delete_from_head(self):
    if self.is_empty():
        return None
    
    val = self.head.val
    
    if self.head == self.tail:
        # Only one node
        self.head = None
        self.tail = None
    else:
        self.head = self.head.next
        self.head.prev = None
    
    self.size -= 1
    return val
```

### Visual: Delete head from [10, 20, 30]

**Before:**
```
None ← [10] ↔ [20] ↔ [30] → None
        ↑ HEAD        ↑ TAIL
```

**After:**
```
None ← [20] ↔ [30] → None
        ↑ HEAD        ↑ TAIL
```
- 20's prev becomes None
- head moves to 20

---

## Operation 5: Delete from Tail (O(1))

```python
def delete_from_tail(self):
    if self.is_empty():
        return None
    
    val = self.tail.val
    
    if self.head == self.tail:
        self.head = None
        self.tail = None
    else:
        self.tail = self.tail.prev
        self.tail.next = None
    
    self.size -= 1
    return val
```

### Visual: Delete tail from [10, 20, 30]

**Before:**
```
None ← [10] ↔ [20] ↔ [30] → None
        ↑ HEAD        ↑ TAIL
```

**After:**
```
None ← [10] ↔ [20] → None
        ↑ HEAD    ↑ TAIL
```
- 20's next becomes None
- tail moves to 20

---

## Operation 6: Traverse Forward

```python
def display_forward(self):
    elements = []
    current = self.head
    while current:
        elements.append(str(current.val))
        current = current.next
    return "None ← " + " ↔ ".join(elements) + " → None"
```

**Example:**
```python
dll = DoublyLinkedList()
dll.insert_at_tail(10)
dll.insert_at_tail(20)
dll.insert_at_tail(30)
print(dll.display_forward())
# Output: None ← 10 ↔ 20 ↔ 30 → None
```

---

## Operation 7: Traverse Backward

```python
def display_backward(self):
    elements = []
    current = self.tail
    while current:
        elements.append(str(current.val))
        current = current.prev
    return "None ← " + " ↔ ".join(elements) + " → None"
```

**Example:**
```python
print(dll.display_backward())
# Output: None ← 30 ↔ 20 ↔ 10 → None
```

---

## Operation 8: Insert After a Given Node (O(1))

```python
def insert_after(self, prev_node, val):
    if not prev_node:
        return
    
    new_node = DoublyListNode(val)
    
    new_node.next = prev_node.next
    new_node.prev = prev_node
    
    if prev_node.next:
        prev_node.next.prev = new_node
    
    prev_node.next = new_node
    
    if new_node.next is None:  # Inserted at tail
        self.tail = new_node
    
    self.size += 1
```

### Visual: Insert 25 after node 20 in [10, 20, 30]

**Before:**
```
None ← [10] ↔ [20] ↔ [30] → None
```

**After:**
```
None ← [10] ↔ [20] ↔ [25] ↔ [30] → None
```

---

## LRU Cache Implementation (Uses Doubly Linked List!)

**Problem:** Design a data structure that follows LRU (Least Recently Used) cache constraints.

**Why important:** Very common interview question!

### The Code:
```python
class LRUCache:
    class Node:
        def __init__(self, key=0, val=0):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        self.head = self.Node()  # dummy head
        self.tail = self.Node()  # dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """Remove node from doubly linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node):
        """Add node right after head"""
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
        
        node = self.Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)
        
        if len(self.cache) > self.capacity:
            # Remove from tail (least recently used)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

### How it Works:

```
LRU Cache with capacity 2:

put(1, 1):  cache: {1: Node(1,1)}
            List: head ↔ (1,1) ↔ tail

put(2, 2):  cache: {1: Node(1,1), 2: Node(2,2)}
            List: head ↔ (2,2) ↔ (1,1) ↔ tail

get(1):     Returns 1, moves (1,1) to head
            List: head ↔ (1,1) ↔ (2,2) ↔ tail

put(3, 3):  Capacity exceeded! Remove LRU (2,2)
            cache: {1: Node(1,1), 3: Node(3,3)}
            List: head ↔ (3,3) ↔ (1,1) ↔ tail
```

---

## Complete Working Example

```python
class DoublyListNode:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def __len__(self):
        return self.size
    
    def insert_at_head(self, val):
        new_node = DoublyListNode(val)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def insert_at_tail(self, val):
        new_node = DoublyListNode(val)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def delete_from_head(self):
        if self.is_empty():
            return None
        val = self.head.val
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1
        return val
    
    def display_forward(self):
        elements = []
        current = self.head
        while current:
            elements.append(str(current.val))
            current = current.next
        return " ↔ ".join(elements) if elements else "Empty"
    
    def display_backward(self):
        elements = []
        current = self.tail
        while current:
            elements.append(str(current.val))
            current = current.prev
        return " ↔ ".join(elements) if elements else "Empty"

# Test it!
dll = DoublyLinkedList()
dll.insert_at_tail(10)
dll.insert_at_tail(20)
dll.insert_at_tail(30)

print("Forward: ", dll.display_forward())   # 10 ↔ 20 ↔ 30
print("Backward:", dll.display_backward())  # 30 ↔ 20 ↔ 10

dll.insert_at_head(5)
print("After insert 5 at head:", dll.display_forward())  # 5 ↔ 10 ↔ 20 ↔ 30

dll.delete_from_head()
print("After delete head:", dll.display_forward())  # 10 ↔ 20 ↔ 30
```

---

## Time Complexity Comparison

| Operation | Singly | Doubly | Why |
|-----------|--------|--------|-----|
| Insert at Head | O(1) | O(1) | Both just change pointers |
| Insert at Tail | O(n) | O(1) | Doubly has tail pointer! |
| Delete from Head | O(1) | O(1) | Both just move head |
| Delete from Tail | O(n) | O(1) | Doubly can go backward! |
| Delete by Value | O(n) | O(1) | If you have reference to node |
| Search | O(n) | O(n) | Must traverse either way |
| Traverse Forward | O(n) | O(n) | Same |
| Traverse Backward | Impossible | O(n) | Doubly can go backward! |

## When to Use Doubly vs Singly

**Use Singly When:**
- Memory is tight (one less pointer per node)
- You only need to traverse forward
- Stack implementation (push/pop from head only)

**Use Doubly When:**
- Need to traverse backward
- Need O(1) deletion from tail
- Implementing LRU Cache
- Implementing Browser History
- Need to insert before a given node

## Key Insights for Interview

1. **Dummy head and tail nodes** simplify edge cases (no empty list checks!)
2. **Always update BOTH pointers** when inserting/deleting
3. **LRU Cache** is the most common doubly linked list interview question
4. **Browser back/forward** is implemented with doubly linked list
5. **O(1) operations at both ends** makes it great for queues and deques
