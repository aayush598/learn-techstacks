# Linked Lists — Last-Minute Revision

Copy-paste ready, tested Python 3 templates for all essential singly-linked-list problems.

## The One Mental Model

Most linked-list problems reduce to a single 3-pointer slide. Keep a dummy node in front so you never special-case the head, and slide `prev / curr / next`:

```python
def slide(head):
    dummy = ListNode(0, head)
    prev, curr = dummy, head
    while curr:
        nxt = curr.next
        # ... rewire prev/curr/nxt here ...
        prev, curr = curr, nxt
    return dummy.next
```

Rules that solve 90% of problems:
- Always return `dummy.next`, never `head` (head may have been removed/rewired).
- Save `nxt = curr.next` BEFORE you mutate `curr.next`.
- On delete/reverse, `prev` always points one node behind `curr`.

## ListNode Class (use everywhere)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

```python
def build(arr):
    dummy = ListNode()
    tail = dummy
    for v in arr:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next

def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out

# build([1,2,3]) -> 1->2->3   |   to_list(head) -> [1,2,3]
```

| Operation | Time | Space |
|---|---|---|
| build / to_list | O(n) | O(n) for the array copy |

## Traversal

```python
def traverse(head):
    cur = head
    while cur:
        print(cur.val)
        cur = cur.next
```

| Operation | Time | Space |
|---|---|---|
| traverse | O(n) | O(1) |

## Insert at Head

```python
def insert_at_head(head, val):
    node = ListNode(val, head)
    return node
# or: head = ListNode(val, head)
```

| Operation | Time | Space |
|---|---|---|
| insert at head | O(1) | O(1) |

## Insert at Tail

```python
def insert_at_tail(head, val):
    node = ListNode(val)
    if not head:
        return node
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = node
    return head
```

| Operation | Time | Space |
|---|---|---|
| insert at tail | O(n) | O(1) |

## Delete Node Given Head (delete by value / by index)

The dummy-node trick: deleting anything (including the head) is identical once you start one node before.

```python
def delete_by_value(head, target):
    dummy = ListNode(0, head)
    prev, cur = dummy, head
    while cur and cur.val != target:
        prev, cur = cur, cur.next
    if cur:
        prev.next = cur.next      # unlink; cur is garbage-collected
    return dummy.next

def delete_by_index(head, idx):   # 0-based
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(idx):
        prev = prev.next
    if prev.next:
        prev.next = prev.next.next
    return dummy.next
```

| Operation | Time | Space |
|---|---|---|
| delete by value / index | O(n) | O(1) |

## Reverse Linked List — Iterative (prev/curr/next 3-pointer)

The canonical template. Commit to memory.

```python
def reverse_iter(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

| Operation | Time | Space |
|---|---|---|
| reverse iterative | O(n) | O(1) |

## Reverse Linked List — Recursive

```python
def reverse_rec(head):
    if not head or not head.next:
        return head
    new_head = reverse_rec(head.next)
    head.next.next = head      # make the next node point back at us
    head.next = None           # old head becomes new tail
    return new_head
```

| Operation | Time | Space |
|---|---|---|
| reverse recursive | O(n) | O(n) call stack |

## Find Middle (Slow/Fast — also the cycle/loop detector core)

`slow` ends exactly at the middle. With `fast` moving twice as fast:
- odd-length `1,2,3,4,5` -> slow stops at `3`.
- even-length `1,2,3,4` -> slow stops at `3` (the right-middle / second middle).

```python
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

| Operation | Time | Space |
|---|---|---|
| find middle | O(n) | O(1) |

## Detect Cycle (Floyd's Tortoise and Hare) + Find Cycle Start

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            break
    if not fast or not fast.next:   # no cycle
        return None
    # distance from head to cycle start == distance from meeting point to cycle start
    slow = head
    while slow is not fast:
        slow = slow.next
        fast = fast.next
    return slow
```

| Operation | Time | Space |
|---|---|---|
| cycle detection | O(n) | O(1) |

## Merge Two Sorted Lists

```python
def merge_two(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next, l1 = l1, l1.next
        else:
            tail.next, l2 = l2, l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next
```

| Operation | Time | Space |
|---|---|---|
| merge two sorted | O(n + m) | O(1) |

## Remove Nth Node From End (dummy node + slow/fast gap)

Classic dummy-node use case: when the node to delete IS the head, a dummy saves you.

```python
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    slow = fast = dummy
    for _ in range(n + 1):   # advance fast n+1 so slow ends BEFORE the target
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next
```

| Operation | Time | Space |
|---|---|---|
| remove nth from end | O(n) | O(1) |

## Remove Duplicates From Sorted List (keep one copy)

```python
def remove_duplicates_sorted(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head
```

| Operation | Time | Space |
|---|---|---|
| remove duplicates (sorted) | O(n) | O(1) |

## Add Two Numbers (digits stored in reverse, return reverse)

```python
def add_two_numbers(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    carry = 0
    while l1 or l2 or carry:
        s = carry
        if l1:
            s += l1.val
            l1 = l1.next
        if l2:
            s += l2.val
            l2 = l2.next
        carry, digit = divmod(s, 10)
        tail.next = ListNode(digit)
        tail = tail.next
    return dummy.next
```

| Operation | Time | Space |
|---|---|---|
| add two numbers | O(max(n, m)) | O(max(n, m)) for the new list |

## Merge K Sorted Lists (heapq)

```python
import heapq

def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):   # (val, index) — index breaks ties so no comparisons on ListNode
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    dummy = ListNode(0)
    tail = dummy
    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

| Operation | Time | Space |
|---|---|---|
| merge k lists | O(n log k) | O(k) heap |

## Palindrome Check (reverse second half — O(1) space)

Find middle, reverse the second half in place, compare, then (optionally) restore.

```python
def is_palindrome(head):
    if not head or not head.next:
        return True
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    prev = None
    while slow:               # reverse second half (starts at slow)
        nxt = slow.next
        slow.next = prev
        prev = slow
        slow = nxt

    left, right = head, prev
    while right:              # compare halves
        if left.val != right.val:
            return False
        left = left.next
        right = right.next
    return True
```

| Operation | Time | Space |
|---|---|---|
| palindrome check | O(n) | O(1) |

## Copy List With Random Pointer — Basics (hashmap mapping)

```python
class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random

def copy_random_list(head):
    old_to_new = {}
    cur = head
    while cur:
        old_to_new[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        if cur.next:
            old_to_new[cur].next = old_to_new[cur.next]
        if cur.random:
            old_to_new[cur].random = old_to_new[cur.random]
        cur = cur.next
    return old_to_new.get(head)
```

| Operation | Time | Space |
|---|---|---|
| copy with random ptr | O(n) | O(n) map |

## Quick Reference Table

| Template | Key idea | Time | Space |
|---|---|---|---|
| Traverse / insert tail | walk to end | O(n) | O(1) |
| Insert head | wrap node | O(1) | O(1) |
| Delete (given head) | dummy node | O(n) | O(1) |
| Reverse iterative | prev/curr/nxt | O(n) | O(1) |
| Reverse recursive | n.next.next = n | O(n) | O(n) |
| Find middle / cycle | slow+fast | O(n) | O(1) |
| Merge two | dummy + tail | O(n+m) | O(1) |
| Remove nth from end | dummy + n-gap | O(n) | O(1) |
| Merge k | heap of (val,i,node) | O(n log k) | O(k) |
| Palindrome | reverse 2nd half | O(n) | O(1) |
| Copy with random | hashmap | O(n) | O(n) |

Recite the dummy-node rule before writing any code: **return `dummy.next`, start `prev` at `dummy`, save `nxt` before rewiring.**
