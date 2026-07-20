# Linked List Practice Problems

## Easy Problems

### 1. Reverse Linked List
**Problem**: Reverse a singly linked list.

**Approach**: Use three pointers - prev, current, next. Reverse each node's pointer.

**Solution**:
```python
def reverse_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    return prev
```

**Complexity**: O(n) time, O(1) space

---

### 2. Merge Two Sorted Lists
**Problem**: Merge two sorted linked lists into one sorted list.

**Approach**: Use dummy node and compare nodes from both lists.

**Solution**:
```python
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    current = dummy
    
    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next
    
    current.next = l1 if l1 else l2
    return dummy.next
```

**Complexity**: O(n + m) time, O(1) space

---

### 3. Linked List Cycle
**Problem**: Determine if a linked list has a cycle.

**Approach**: Use Floyd's cycle detection (slow and fast pointers).

**Solution**:
```python
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    
    return True
```

**Complexity**: O(n) time, O(1) space

---

### 4. Middle of Linked List
**Problem**: Find the middle node of a linked list.

**Approach**: Use slow and fast pointers. When fast reaches end, slow is at middle.

**Solution**:
```python
def find_middle(head):
    if not head:
        return None
    
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow
```

**Complexity**: O(n) time, O(1) space

---

### 5. Remove Duplicates from Sorted List
**Problem**: Remove all duplicates from a sorted linked list.

**Approach**: Compare current node with next node, skip duplicates.

**Solution**:
```python
def delete_duplicates(head):
    current = head
    
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next
    
    return head
```

**Complexity**: O(n) time, O(1) space

---

## Medium Problems

### 6. Add Two Numbers
**Problem**: Add two numbers represented as linked lists (digits in reverse order).

**Approach**: Traverse both lists, add digits with carry.

**Solution**:
```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        current.next = ListNode(total % 10)
        current = current.next
        
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next
```

**Complexity**: O(max(n, m)) time, O(max(n, m)) space

---

### 7. Remove Nth Node From End
**Problem**: Remove the nth node from the end of a linked list.

**Approach**: Use two pointers with n gap. When fast reaches end, slow is at node to remove.

**Solution**:
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

**Complexity**: O(L) time, O(1) space

---

### 8. Reorder List
**Problem**: Reorder list: L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → ...

**Approach**: Find middle, reverse second half, merge alternating.

**Solution**:
```python
def reorder_list(head):
    if not head or not head.next:
        return
    
    # Find middle
    slow = head
    fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    # Reverse second half
    prev = None
    current = slow.next
    slow.next = None
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    
    # Merge alternating
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

**Complexity**: O(n) time, O(1) space

---

### 9. Swap Nodes in Pairs
**Problem**: Swap every two adjacent nodes.

**Approach**: Use dummy node and swap pointers in pairs.

**Solution**:
```python
def swap_pairs(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    
    while prev.next and prev.next.next:
        first = prev.next
        second = first.next
        
        # Swap
        first.next = second.next
        second.next = first
        prev.next = second
        
        prev = first
    
    return dummy.next
```

**Complexity**: O(n) time, O(1) space

---

### 10. Copy List with Random Pointer
**Problem**: Copy a linked list where each node has next and random pointer.

**Approach**: Use hash map to store mapping from original to copied nodes.

**Solution**:
```python
class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random

def copy_random_list(head):
    if not head:
        return None
    
    # Create mapping
    mapping = {}
    current = head
    
    while current:
        mapping[current] = RandomNode(current.val)
        current = current.next
    
    # Set pointers
    current = head
    while current:
        if current.next:
            mapping[current].next = mapping[current.next]
        if current.random:
            mapping[current].random = mapping[current.random]
        current = current.next
    
    return mapping[head]
```

**Complexity**: O(n) time, O(n) space

---

## Hard Problems

### 11. Merge k Sorted Lists
**Problem**: Merge k sorted linked lists into one sorted list.

**Approach**: Use min-heap to always get the smallest element.

**Solution**:
```python
import heapq

def merge_k_lists(lists):
    dummy = ListNode(0)
    current = dummy
    min_heap = []
    
    # Initialize heap
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(min_heap, (node.val, i, node))
    
    while min_heap:
        val, idx, node = heapq.heappop(min_heap)
        current.next = node
        current = current.next
        
        if node.next:
            heapq.heappush(min_heap, (node.next.val, idx, node.next))
    
    return dummy.next
```

**Complexity**: O(N log k) time, O(k) space

---

### 12. Reverse Nodes in k-Group
**Problem**: Reverse nodes in groups of k.

**Approach**: Check if k nodes exist, reverse segment, repeat.

**Solution**:
```python
def reverse_k_group(head, k):
    def reverse_segment(start, end):
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

**Complexity**: O(n) time, O(1) space

---

### 13. Sort List
**Problem**: Sort a linked list in O(n log n) time.

**Approach**: Use merge sort (divide and conquer).

**Solution**:
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
    slow.next = None
    
    # Sort halves
    left = sort_list(head)
    right = sort_list(mid)
    
    # Merge
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

**Complexity**: O(n log n) time, O(log n) space

---

### 14. Flatten a Multilevel Linked List
**Problem**: Flatten a linked list with child pointers.

**Approach**: Recursively flatten children and connect to next.

**Solution**:
```python
class MultiLevelNode:
    def __init__(self, val=0, next=None, child=None):
        self.val = val
        self.next = next
        self.child = child

def flatten(head):
    if not head:
        return head
    
    current = head
    
    while current:
        if current.child:
            # Save next
            next_node = current.next
            
            # Flatten child
            child_head = flatten(current.child)
            current.next = child_head
            
            # Find tail
            tail = child_head
            while tail.next:
                tail = tail.next
            
            # Connect to saved next
            tail.next = next_node
            
            # Remove child
            current.child = None
        else:
            current = current.next
    
    return head
```

**Complexity**: O(n) time, O(d) space (d = depth)

---

### 15. LRU Cache
**Problem**: Design a data structure that follows LRU cache constraints.

**Approach**: Use HashMap + Doubly Linked List for O(1) operations.

**Solution**:
```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}
        self.head = DoublyListNode(0)
        self.tail = DoublyListNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val
    
    def put(self, key, value):
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = DoublyListNode(value)
        node.val = value
        self.cache[key] = node
        self._add_to_front(node)
        
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.val]
```

**Complexity**: O(1) for both get and put operations

---

## Summary Table

| # | Problem | Difficulty | Time | Space |
|---|---------|------------|------|-------|
| 1 | Reverse Linked List | Easy | O(n) | O(1) |
| 2 | Merge Two Sorted Lists | Easy | O(n+m) | O(1) |
| 3 | Linked List Cycle | Easy | O(n) | O(1) |
| 4 | Middle of Linked List | Easy | O(n) | O(1) |
| 5 | Remove Duplicates | Easy | O(n) | O(1) |
| 6 | Add Two Numbers | Medium | O(max(n,m)) | O(max(n,m)) |
| 7 | Remove Nth From End | Medium | O(L) | O(1) |
| 8 | Reorder List | Medium | O(n) | O(1) |
| 9 | Swap Nodes in Pairs | Medium | O(n) | O(1) |
| 10 | Copy List with Random | Medium | O(n) | O(n) |
| 11 | Merge k Sorted Lists | Hard | O(N log k) | O(k) |
| 12 | Reverse in k-Groups | Hard | O(n) | O(1) |
| 13 | Sort List | Hard | O(n log n) | O(log n) |
| 14 | Flatten Multilevel | Hard | O(n) | O(d) |
| 15 | LRU Cache | Hard | O(1) | O(capacity) |
