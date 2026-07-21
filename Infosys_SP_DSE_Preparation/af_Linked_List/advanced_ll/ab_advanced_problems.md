# Advanced Linked List Problems

## Flatten a Linked List with Next, Child, and Random Pointers - O(n)
```python
class SpecialNode:
    def __init__(self, val=0, next=None, child=None, random=None):
        self.val = val
        self.next = next
        self.child = child
        self.random = random

def flatten_with_random(head):
    """
    Flatten a multilevel doubly linked list with random pointers
    """
    if not head:
        return head
    
    # Step 1: Create mapping for random pointers
    mapping = {}
    current = head
    while current:
        mapping[id(current)] = current
        current = current.next
    
    # Step 2: Flatten the list
    current = head
    while current:
        if current.child:
            next_node = current.next
            
            # Connect to child
            current.next = current.child
            current.child.prev = current
            
            # Find tail of child
            tail = current.child
            while tail.next:
                tail = tail.next
            
            # Connect tail to next
            tail.next = next_node
            if next_node:
                next_node.prev = tail
            
            # Remove child pointer
            current.child = None
        else:
            current = current.next
    
    return head
```

## Merge Sort on Linked List - O(n log n)
```python
def merge_sort_list(head):
    if not head or not head.next:
        return head
    
    # Find middle
    slow = head
    fast = head.next
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    
    # Split list
    mid = slow.next
    slow.next = None
    
    # Recursively sort both halves
    left = merge_sort_list(head)
    right = merge_sort_list(mid)
    
    # Merge sorted halves
    return merge_sorted(left, right)

def merge_sorted(l1, l2):
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

## Quick Sort on Linked List - O(n log n) average
```python
def quick_sort_list(head):
    if not head or not head.next:
        return head
    
    # Partition around pivot
    pivot = head.val
    less_head = less_tail = ListNode(0)
    equal_head = equal_tail = ListNode(0)
    greater_head = greater_tail = ListNode(0)
    
    current = head
    while current:
        if current.val < pivot:
            less_tail.next = current
            less_tail = less_tail.next
        elif current.val == pivot:
            equal_tail.next = current
            equal_tail = equal_tail.next
        else:
            greater_tail.next = current
            greater_tail = greater_tail.next
        current = current.next
    
    # Terminate lists
    less_tail.next = None
    equal_tail.next = None
    greater_tail.next = None
    
    # Recursively sort less and greater
    sorted_less = quick_sort_list(less_head.next)
    sorted_greater = quick_sort_list(greater_head.next)
    
    # Concatenate: less + equal + greater
    return concatenate(sorted_less, equal_head.next, sorted_greater)

def concatenate(list1, list2, list3):
    dummy = ListNode(0)
    current = dummy
    
    for lst in [list1, list2, list3]:
        if lst:
            current.next = lst
            while current.next:
                current = current.next
    
    return dummy.next
```

## Reverse a Linked List in Groups of K - O(n)
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

## Remove Duplicates from Sorted Linked List - O(n)
```python
def remove_duplicates(head):
    current = head
    
    while current and current.next:
        if current.val == current.next.val:
            current.next = current.next.next
        else:
            current = current.next
    
    return head

# Remove all duplicates (return unique values only)
def remove_duplicates_all(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    current = head
    
    while current:
        if current.next and current.val == current.next.val:
            # Skip all duplicates
            while current.next and current.val == current.next.val:
                current = current.next
            prev.next = current.next
        else:
            prev = prev.next
        current = current.next
    
    return dummy.next
```

## Swap Nodes in Linked List Without Swapping Data - O(n)
```python
def swap_nodes(head, k):
    # Find kth node from beginning
    first = head
    for _ in range(k - 1):
        first = first.next
    
    # Find kth node from end using two pointers
    fast = head
    slow = head
    
    for _ in range(k):
        fast = fast.next
    
    while fast:
        fast = fast.next
        slow = slow.next
    
    second = slow
    
    # Swap values
    first.val, second.val = second.val, first.val
    
    return head

# Alternative: Swap by changing pointers (more complex but true swap)
def swap_nodes_pointers(head, k):
    if not head or not head.next:
        return head
    
    # Find length
    length = 0
    current = head
    while current:
        length += 1
        current = current.next
    
    # Find positions
    pos1 = k - 1
    pos2 = length - k
    
    if pos1 == pos2:
        return head
    
    # Ensure pos1 < pos2
    if pos1 > pos2:
        pos1, pos2 = pos2, pos1
    
    # Find nodes and their predecessors
    dummy = ListNode(0)
    dummy.next = head
    prev1 = dummy
    prev2 = dummy
    
    for _ in range(pos1):
        prev1 = prev1.next
    
    for _ in range(pos2):
        prev2 = prev2.next
    
    node1 = prev1.next
    node2 = prev2.next
    next2 = node2.next
    
    # Perform swap
    prev1.next = node2
    node2.next = node1.next
    
    if pos2 - pos1 == 1:
        node1.next = node2
    else:
        node1.next = next2
        prev2.next = node1
    
    return dummy.next
```

## Rotate Linked List - O(n)
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

def rotate_left(head, k):
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
    steps_to_new_tail = k - 1
    
    new_tail = head
    for _ in range(steps_to_new_tail):
        new_tail = new_tail.next
    
    new_head = new_tail.next
    new_tail.next = None
    
    return new_head
```

## Odd-Even Linked List - O(n)
```python
def odd_even_list(head):
    if not head:
        return head
    
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

## Linked List Cycle II (Find Start) - O(n)
```python
def detect_cycle_start(head):
    if not head or not head.next:
        return None
    
    # Phase 1: Detect cycle
    slow = head
    fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None
    
    # Phase 2: Find start of cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow
```

## Complete Example Usage
```python
def create_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    current = head
    for val in arr[1:]:
        current.next = ListNode(val)
        current = current.next
    return head

def print_list(head):
    elements = []
    while head:
        elements.append(str(head.val))
        head = head.next
    return " -> ".join(elements) + " -> None"

# Test merge sort
head = create_list([4, 2, 1, 3])
sorted_head = merge_sort_list(head)
print(f"Merge sorted: {print_list(sorted_head)}")  # 1 -> 2 -> 3 -> 4

# Test odd-even list
head = create_list([1, 2, 3, 4, 5])
result = odd_even_list(head)
print(f"Odd-even: {print_list(result)}")  # 1 -> 3 -> 5 -> 2 -> 4

# Test reverse in groups of 2
head = create_list([1, 2, 3, 4, 5])
result = reverse_k_group(head, 2)
print(f"Reverse in groups of 2: {print_list(result)}")  # 2 -> 1 -> 4 -> 3 -> 5
```
