# Linked Lists

## Problem 1: Reverse a Linked List
**Difficulty: Easy | Marks: 20**

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev

# Recursive
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

## Problem 2: Detect Cycle in Linked List
**Difficulty: Easy | Marks: 20**

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

---

## Problem 3: Find Cycle Start
**Difficulty: Medium | Marks: 30**

```python
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

---

## Problem 4: Merge Two Sorted Lists
**Difficulty: Easy | Marks: 20**

```python
def merge_two_lists(l1, l2):
    dummy = ListNode()
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

---

## Problem 5: Merge K Sorted Lists
**Difficulty: Hard | Marks: 50**

```python
import heapq

def merge_k_lists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))
    dummy = curr = ListNode()
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

---

## Problem 6: Remove Nth Node From End
**Difficulty: Medium | Marks: 30**

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next
```

---

## Problem 7: Middle of Linked List
**Difficulty: Easy | Marks: 20**

```python
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

## Problem 8: Intersection of Two Linked Lists
**Difficulty: Medium | Marks: 30**

```python
def get_intersection_node(headA, headB):
    if not headA or not headB:
        return None
    a, b = headA, headB
    while a != b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a
```

---

## Problem 9: Palindrome Linked List
**Difficulty: Medium | Marks: 30**

```python
def is_palindrome(head):
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # Reverse second half
    prev = None
    while slow:
        next_temp = slow.next
        slow.next = prev
        prev = slow
        slow = next_temp
    # Compare
    left, right = head, prev
    while right:
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True
```

---

## Problem 10: Add Two Numbers (Reversed List)
**Difficulty: Medium | Marks: 30**

```python
def add_two_numbers(l1, l2):
    dummy = curr = ListNode()
    carry = 0
    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry = total // 10
        curr.next = ListNode(total % 10)
        curr = curr.next
        if l1: l1 = l1.next
        if l2: l2 = l2.next
    return dummy.next
```

---

## Problem 11: Copy List with Random Pointer
**Difficulty: Medium | Marks: 30**

```python
def copy_random_list(head):
    if not head:
        return None
    # Interleave copied nodes
    curr = head
    while curr:
        new_node = ListNode(curr.val, curr.next)
        curr.next = new_node
        curr = new_node.next
    # Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
    # Separate lists
    curr = head
    new_head = head.next
    while curr:
        copy = curr.next
        curr.next = copy.next
        curr = curr.next
        if copy.next:
            copy.next = copy.next.next
    return new_head
```

---

## Problem 12: Reorder List
**Difficulty: Medium | Marks: 30**

```python
def reorder_list(head):
    if not head or not head.next:
        return
    # Find middle
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    # Reverse second half
    prev = None
    curr = slow.next
    slow.next = None
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    # Merge
    first, second = head, prev
    while second:
        temp1, temp2 = first.next, second.next
        first.next = second
        second.next = temp1
        first = temp1
        second = temp2
```

---

## Problem 13: Rotate List
**Difficulty: Medium | Marks: 30**

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
    k = k % length
    if k == 0:
        return head
    # Find new tail (length - k - 1)
    new_tail = head
    for _ in range(length - k - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    tail.next = head
    return new_head
```

---

## Problem 14: Odd Even Linked List
**Difficulty: Medium | Marks: 30**

```python
def odd_even_list(head):
    if not head or not head.next:
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

---

## Problem 15: Flatten a Multilevel Doubly Linked List
**Difficulty: Medium | Marks: 30**

```python
def flatten(head):
    if not head:
        return None
    def dfs(node):
        last = node
        while node:
            if node.child:
                original_next = node.next
                node.next = node.child
                node.child.prev = node
                child_last = dfs(node.child)
                node.child = None
                if original_next:
                    child_last.next = original_next
                    original_next.prev = child_last
                last = child_last
            else:
                last = node
            node = node.next
        return last
    dfs(head)
    return head
```
