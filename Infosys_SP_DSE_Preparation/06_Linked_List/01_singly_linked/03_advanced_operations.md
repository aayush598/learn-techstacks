# Singly Linked List - Advanced Operations

## Merge Two Sorted Linked Lists - O(n + m)
```python
def merge_two_sorted(l1, l2):
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

## Merge K Sorted Linked Lists - O(N log k)
```python
import heapq

def merge_k_lists(lists):
    dummy = ListNode(0)
    current = dummy
    min_heap = []
    
    # Initialize heap with first node of each list
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

## Remove Nth Node From End - O(n)
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

## Add Two Numbers (as Linked Lists) - O(max(n, m))
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

## Copy List with Random Pointer - O(n)
```python
class RandomNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random

def copy_random_list(head):
    if not head:
        return None
    
    # Step 1: Create mapping of original to copied nodes
    mapping = {}
    current = head
    
    while current:
        mapping[current] = RandomNode(current.val)
        current = current.next
    
    # Step 2: Set next and random pointers
    current = head
    while current:
        if current.next:
            mapping[current].next = mapping[current.next]
        if current.random:
            mapping[current].random = mapping[current.random]
        current = current.next
    
    return mapping[head]
```

## Partition List - O(n)
```python
def partition(head, x):
    dummy_before = ListNode(0)
    dummy_after = ListNode(0)
    
    before = dummy_before
    after = dummy_after
    
    while head:
        if head.val < x:
            before.next = head
            before = before.next
        else:
            after.next = head
            after = after.next
        head = head.next
    
    after.next = None
    before.next = dummy_after.next
    
    return dummy_before.next
```

## Rotate List - O(n)
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
    
    # Make circular
    tail.next = head
    
    # Find new tail position
    k = k % length
    steps_to_new_tail = length - k
    
    new_tail = head
    for _ in range(steps_to_new_tail - 1):
        new_tail = new_tail.next
    
    new_head = new_tail.next
    new_tail.next = None
    
    return new_head
```

## Reverse Nodes in k-Group - O(n)
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

## Swap Nodes in Pairs - O(n)
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

## Complete Example Usage
```python
# Helper function to create list from array
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

# Helper function to print list
def print_list(head):
    elements = []
    while head:
        elements.append(str(head.val))
        head = head.next
    return " -> ".join(elements) + " -> None"

# Example: Merge two sorted lists
l1 = create_list([1, 3, 5])
l2 = create_list([2, 4, 6])
merged = merge_two_sorted(l1, l2)
print(f"Merged: {print_list(merged)}")  # 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> None

# Example: Add two numbers
l1 = create_list([2, 4, 3])  # 342
l2 = create_list([5, 6, 4])  # 465
result = add_two_numbers(l1, l2)
print(f"Sum: {print_list(result)}")  # 7 -> 0 -> 8 -> None (807)

# Example: Rotate list
head = create_list([1, 2, 3, 4, 5])
rotated = rotate_right(head, 2)
print(f"Rotated: {print_list(rotated)}")  # 4 -> 5 -> 1 -> 2 -> 3 -> None
```
