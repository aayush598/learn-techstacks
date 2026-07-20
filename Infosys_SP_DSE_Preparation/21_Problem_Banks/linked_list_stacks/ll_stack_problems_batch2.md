# Linked List, Stack & Queue Problems — Batch 2

## 40 More Problems for Infosys SP DSE Preparation

---

## ListNode Definition (Used Throughout)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Node:
    """Doubly linked list node with random pointer"""
    def __init__(self, x):
        self.val = x
        self.next = None
        self.random = None

class DLLNode:
    """Doubly linked list node"""
    def __init__(self, val=0, prev=None, next=None, child=None):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child
```

---

# PART A: LINKED LIST (20 Problems)

---

## Problem 1: Delete Node in a Linked List

**Difficulty: Easy**

### Problem Statement

Write a function to delete a node (except the tail) in a singly linked list, given only access to that node. The head node and the node to be deleted are guaranteed not to be `None` and the linked list has at least two nodes.

### Approach

Since we only have access to the node to delete (not its predecessor), we **copy the next node's value into the current node**, then skip over the next node. This effectively deletes the current node by overwriting it.

```
Before: 1 -> 2 -> 3 -> 4, delete node with val 2
Copy 3 into node 2: 1 -> 3 -> 3 -> 4
Skip: 1 -> 3 -> 4
```

### Solution

```python
def deleteNode(node):
    node.val = node.next.val
    node.next = node.next.next

# Time: O(1) - only pointer operations
# Space: O(1) - no extra space
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
deleteNode(head.next)  # delete node with val 2
# List is now 1 -> 3
```

---

## Problem 2: Middle of the Linked List

**Difficulty: Easy**

### Problem Statement

Given the head of a singly linked list, return the middle node of the linked list. If there are two middle nodes, return the second middle node.

### Approach

Use **slow and fast pointer** technique. Slow pointer moves 1 step, fast pointer moves 2 steps. When fast reaches the end, slow is at the middle. For even-length lists, this naturally gives the second middle.

```
1 -> 2 -> 3 -> 4 -> 5
S: 1   S: 2   S: 3   (fast reaches end, slow at 3)

1 -> 2 -> 3 -> 4 -> 5 -> 6
S: 1   S: 2   S: 3   S: 4  (fast reaches end, slow at 4)
```

### Solution

```python
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# Time: O(n) - single pass
# Space: O(1) - two pointers only
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
mid = middleNode(head)
print(mid.val)  # 3
```

---

## Problem 3: Palindrome Linked List

**Difficulty: Easy**

### Problem Statement

Given the head of a singly linked list, return `True` if it is a palindrome, `False` otherwise.

### Approach

1. Find the middle using slow/fast pointers
2. **Reverse** the second half of the list
3. Compare the first half with the reversed second half
4. If all values match, it is a palindrome

```
1 -> 2 -> 3 -> 2 -> 1
First half: 1 -> 2
Second half reversed: 1 -> 2
Match -> palindrome
```

### Solution

```python
def isPalindrome(head):
    if not head or not head.next:
        return True
    slow = fast = head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    prev = None
    curr = slow.next
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    slow.next = None
    first, second = head, prev
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    return True

# Time: O(n) - finding middle + reversing + comparing
# Space: O(1) - in-place reversal
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(2)
head.next.next.next = ListNode(1)
print(isPalindrome(head))  # True

head2 = ListNode(1)
head2.next = ListNode(2)
print(isPalindrome(head2))  # False
```

---

## Problem 4: Remove Linked List Elements

**Difficulty: Easy**

### Problem Statement

Given the `head` of a linked list and an integer `val`, remove all nodes of the linked list that have `Node.val == val`, and return the new head.

### Approach

Use a **dummy node** before the head to handle cases where the head itself needs to be removed. Traverse the list; when you find a node with the target value, skip it by linking the previous node to the next node.

```
1 -> 2 -> 6 -> 3 -> 6, val = 6
Result: 1 -> 2 -> 3
```

### Solution

```python
def removeElements(head, val):
    dummy = ListNode(0)
    dummy.next = head
    prev, curr = dummy, head
    while curr:
        if curr.val == val:
            prev.next = curr.next
        else:
            prev = curr
        curr = curr.next
    return dummy.next

# Time: O(n) - single pass
# Space: O(1) - in-place removal
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(6)
head.next.next.next = ListNode(3)
head.next.next.next.next = ListNode(6)
result = removeElements(head, 6)
# 1 -> 2 -> 3
```

---

## Problem 5: Linked List Components

**Difficulty: Easy**

### Problem Statement

We are given `head`, the head node of a linked list containing unique integer values. We are also given the list `nums`, a subset of the values in the linked list. Return the number of connected components in `nums` where two values are connected if they appear consecutively in the linked list.

### Approach

Traverse the linked list. Track whether the current node's value is in the `nums` set. A new component starts when we transition from a value **not** in `nums` to a value **in** `nums`. Count these transitions.

```
List: 0 -> 1 -> 2 -> 3, nums = [0, 1, 3]
Components: [0,1] and [3] = 2 components
```

### Solution

```python
def numComponents(head, nums):
    num_set = set(nums)
    count = 0
    in_component = False
    while head:
        if head.val in num_set:
            if not in_component:
                count += 1
                in_component = True
        else:
            in_component = False
        head = head.next
    return count

# Time: O(n + m) where n = list length, m = nums length
# Space: O(m) for the set
```

### Test

```python
head = ListNode(0)
head.next = ListNode(1)
head.next.next = ListNode(2)
head.next.next.next = ListNode(3)
print(numComponents(head, [0, 1, 3]))  # 2
```

---

## Problem 6: Convert Binary Number in a Linked List to Integer

**Difficulty: Easy**

### Problem Statement

Given `head` which is a reference node to a singly-linked list. The linked list stores the binary representation of a number. Return the decimal value of the number.

### Approach

Traverse the list from head to tail. For each node, shift the accumulated result left by 1 (multiply by 2) and add the current bit. This builds the number from most significant bit to least.

```
1 -> 0 -> 1
Result = 0
Step 1: 0*2 + 1 = 1
Step 2: 1*2 + 0 = 2
Step 3: 2*2 + 1 = 5
```

### Solution

```python
def getDecimalValue(head):
    result = 0
    while head:
        result = result * 2 + head.val
        head = head.next
    return result

# Time: O(n) - single pass
# Space: O(1) - only accumulator variable
```

### Test

```python
head = ListNode(1)
head.next = ListNode(0)
head.next.next = ListNode(1)
print(getDecimalValue(head))  # 5

head2 = ListNode(0)
print(getDecimalValue(head2))  # 0
```

---

## Problem 7: Split Linked List in Parts

**Difficulty: Easy**

### Problem Statement

Given the `head` of a singly linked list and an integer `k`, split the linked list into `k` consecutive linked list parts. The lengths of the parts should be as equal as possible: no two parts should have a size differing by more than one. Parts should be in the order of occurrence in the input list.

### Approach

1. Count total nodes `n`
2. Each part gets `n // k` nodes
3. The first `n % k` parts get one extra node
4. Traverse and split the list accordingly

```
1 -> 2 -> 3 -> 4 -> 5, k = 3
Parts: [1,2], [3,4], [5]  (sizes 2, 2, 1)
```

### Solution

```python
def splitListToParts(head, k):
    n = 0
    curr = head
    while curr:
        n += 1
        curr = curr.next
    width, extra = divmod(n, k)
    result = []
    curr = head
    for i in range(k):
        part_head = curr
        part_size = width + (1 if i < extra else 0)
        for j in range(part_size - 1):
            if curr:
                curr = curr.next
        if curr:
            nxt = curr.next
            curr.next = None
            curr = nxt
        result.append(part_head)
    return result

# Time: O(n + k) - count nodes + split
# Space: O(1) extra (excluding output)
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
parts = splitListToParts(head, 3)
# parts[0]: 1->2, parts[1]: 3->4, parts[2]: 5
```

---

## Problem 8: Remove Duplicates from Unsorted Linked List

**Difficulty: Easy**

### Problem Statement

Given an unsorted linked list, remove all duplicate nodes so that each value appears only once.

### Approach

Use a **hash set** to track values we have seen. Traverse the list; if a value is already in the set, skip the node. Otherwise, add it to the set and keep the node.

```
1 -> 3 -> 3 -> 4 -> 4 -> 5
Seen: {1, 3, 4, 5}
Result: 1 -> 3 -> 4 -> 5
```

### Solution

```python
def removeDuplicates(head):
    if not head:
        return None
    seen = set()
    prev, curr = None, head
    while curr:
        if curr.val in seen:
            prev.next = curr.next
        else:
            seen.add(curr.val)
            prev = curr
        curr = curr.next
    return head

# Time: O(n) - single pass with set lookup
# Space: O(n) - for the hash set
```

### Test

```python
head = ListNode(1)
head.next = ListNode(3)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(4)
head.next.next.next.next.next = ListNode(5)
result = removeDuplicates(head)
# 1 -> 3 -> 4 -> 5
```

---

## Problem 9: Rotate List

**Difficulty: Medium**

### Problem Statement

Given the `head` of a linked list, rotate the list to the right by `k` places.

### Approach

1. Find the length of the list and connect the tail to the head (make it circular)
2. The new tail is at position `length - k % length - 1` from the head
3. Break the circle after the new tail

```
1 -> 2 -> 3 -> 4 -> 5, k = 2
Circular: 1->2->3->4->5->1
New tail at index 5-2-1=2 (node 3)
Result: 4 -> 5 -> 1 -> 2 -> 3
```

### Solution

```python
def rotateRight(head, k):
    if not head or not head.next or k == 0:
        return head
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1
    k = k % length
    if k == 0:
        return head
    tail.next = head
    steps_to_new_tail = length - k
    new_tail = head
    for _ in range(steps_to_new_tail - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return new_head

# Time: O(n) - find length + traverse to new tail
# Space: O(1) - in-place rotation
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
result = rotateRight(head, 2)
# 4 -> 5 -> 1 -> 2 -> 3
```

---

## Problem 10: Swap Nodes in Pairs

**Difficulty: Medium**

### Problem Statement

Given a linked list, swap every two adjacent nodes and return its head. You must solve it without modifying the values in the nodes (i.e., only nodes themselves may be changed).

### Approach

Use a **dummy node** and three pointers. For each pair, reverse the link between them. Specifically, rearrange the pointers so that the second node points to the first, and the first points to the next pair's first node.

```
1 -> 2 -> 3 -> 4
After swap pairs: 2 -> 1 -> 4 -> 3
```

### Solution

```python
def swapPairs(head):
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    while prev.next and prev.next.next:
        first = prev.next
        second = first.next
        first.next = second.next
        second.next = first
        prev.next = second
        prev = first
    return dummy.next

# Time: O(n) - single pass
# Space: O(1) - in-place swap
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
result = swapPairs(head)
# 2 -> 1 -> 4 -> 3
```

---

## Problem 11: Odd Even Linked List

**Difficulty: Medium**

### Problem Statement

Given the `head` of a singly linked list, group all the nodes with odd indices together followed by the nodes with even indices, and return the reordered list. The first node is considered odd, the second node even, and so on.

### Approach

Maintain two separate chains: one for odd-indexed nodes and one for even-indexed nodes. Connect the tail of the odd chain to the head of the even chain at the end.

```
1 -> 2 -> 3 -> 4 -> 5
Odd: 1 -> 3 -> 5
Even: 2 -> 4
Result: 1 -> 3 -> 5 -> 2 -> 4
```

### Solution

```python
def oddEvenList(head):
    if not head:
        return None
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

# Time: O(n) - single pass
# Space: O(1) - in-place rearrangement
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
result = oddEvenList(head)
# 1 -> 3 -> 5 -> 2 -> 4
```

---

## Problem 12: Add Two Numbers II

**Difficulty: Medium**

### Problem Statement

You are given two non-empty linked lists representing two non-negative integers. The most significant digit comes first. Add the two numbers and return the sum as a linked list.

### Approach

1. Use two **stacks** to push the digits of each number
2. Pop from both stacks, adding digits with carry
3. Build the result list by prepending each new digit

```
342 + 465 = 807
Stack1: [2, 4, 3], Stack2: [5, 6, 4]
Pop and add: 2+5=7, 4+6=10(carry), 3+4+1=8
Result: 8 -> 0 -> 7
```

### Solution

```python
def addTwoNumbers(l1, l2):
    stack1, stack2 = [], []
    while l1:
        stack1.append(l1.val)
        l1 = l1.next
    while l2:
        stack2.append(l2.val)
        l2 = l2.next
    carry = 0
    result = None
    while stack1 or stack2 or carry:
        val = carry
        if stack1:
            val += stack1.pop()
        if stack2:
            val += stack2.pop()
        carry, digit = divmod(val, 10)
        node = ListNode(digit)
        node.next = result
        result = node
    return result

# Time: O(m + n) where m, n are lengths of l1, l2
# Space: O(m + n) for the stacks
```

### Test

```python
l1 = ListNode(3)
l1.next = ListNode(4)
l1.next.next = ListNode(2)
l2 = ListNode(4)
l2.next = ListNode(6)
l2.next.next = ListNode(5)
result = addTwoNumbers(l1, l2)
# 8 -> 0 -> 7
```

---

## Problem 13: Copy List with Random Pointer

**Difficulty: Medium**

### Problem Statement

A linked list of length `n` is given such that each node contains an additional random pointer. Make a deep copy of the list.

### Approach

**O(1) space approach using interleaving:**
1. Insert a copy of each node right after itself: `A -> A' -> B -> B' -> C -> C'`
2. Set random pointers for the copied nodes using the original nodes' random pointers
3. Separate the original and copied lists

### Solution

```python
def copyRandomList(head):
    if not head:
        return None
    curr = head
    while curr:
        new_node = Node(curr.val)
        new_node.next = curr.next
        curr.next = new_node
        curr = new_node.next
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next
    new_head = head.next
    curr = head
    while curr:
        copy = curr.next
        curr.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        curr = curr.next
    return new_head

# Time: O(n) - three passes through the list
# Space: O(1) - no extra space for new nodes' connections
```

### Test

```python
head = Node(7)
head.next = Node(13)
head.next.next = Node(11)
head.next.next.next = Node(10)
head.next.next.next.next = Node(1)
head.random = None
head.next.random = head
head.next.next.random = head.next.next.next.next
head.next.next.next.random = head.next.next
head.next.next.next.next.random = head
copied = copyRandomList(head)
```

---

## Problem 14: Flatten a Multilevel Doubly Linked List

**Difficulty: Medium**

### Problem Statement

Given a doubly linked list where in addition to the next and previous pointers, each node has a child pointer. Flatten the list so that all the nodes appear in a single-level doubly linked list.

### Approach

Use **recursion**. Traverse the list. When a node has a child:
1. Save the next node
2. Recursively flatten the child
3. Connect the child's flattened list between the current node and the saved next
4. Connect the tail of the flattened child to the saved next

### Solution

```python
def flatten(head):
    def flatten_helper(node):
        curr = node
        tail = node
        while curr:
            if curr.child:
                child_head = flatten_helper(curr.child)
                nxt = curr.next
                curr.next = child_head
                child_head.prev = curr
                curr.child = None
                t = child_head
                while t.next:
                    t = t.next
                t.next = nxt
                if nxt:
                    nxt.prev = t
                tail = t
                curr = nxt
            else:
                tail = curr
                curr = curr.next
        return node
    if head:
        flatten_helper(head)
    return head

# Time: O(n) - each node visited once
# Space: O(d) where d is max depth of child chains (recursion stack)
```

### Test

```python
head = DLLNode(1)
head.next = DLLNode(2)
head.next.next = DLLNode(3)
head.next.next.child = DLLNode(7)
head.next.next.child.next = DLLNode(8)
result = flatten(head)
```

---

## Problem 15: Partition List

**Difficulty: Medium**

### Problem Statement

Given the `head` of a linked list and a value `x`, partition it such that all nodes less than `x` come before nodes greater than or equal to `x`. The relative order of nodes in each partition should be preserved.

### Approach

Create two separate lists: one for nodes less than `x`, one for nodes greater than or equal to `x`. Connect the two lists at the end. Use dummy heads for both lists.

```
1 -> 4 -> 3 -> 2 -> 5 -> 2, x = 3
Less: 1 -> 2 -> 2
Greater: 4 -> 3 -> 5
Result: 1 -> 2 -> 2 -> 4 -> 3 -> 5
```

### Solution

```python
def partition(head, x):
    less_dummy = ListNode(0)
    greater_dummy = ListNode(0)
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
    greater.next = None
    less.next = greater_dummy.next
    return less_dummy.next

# Time: O(n) - single pass
# Space: O(1) - rearranging pointers
```

### Test

```python
head = ListNode(1)
head.next = ListNode(4)
head.next.next = ListNode(3)
head.next.next.next = ListNode(2)
head.next.next.next.next = ListNode(5)
head.next.next.next.next.next = ListNode(2)
result = partition(head, 3)
# 1 -> 2 -> 2 -> 4 -> 3 -> 5
```

---

## Problem 16: Reverse Linked List II

**Difficulty: Medium**

### Problem Statement

Given the `head` of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`.

### Approach

1. Use a dummy node; move a pointer to the node just before position `left`
2. Reverse the sublist from `left` to `right` using standard reversal
3. Reconnect the reversed portion with the rest of the list

```
1 -> 2 -> 3 -> 4 -> 5, left=2, right=4
After: 1 -> 4 -> 3 -> 2 -> 5
```

### Solution

```python
def reverseBetween(head, left, right):
    if not head or left == right:
        return head
    dummy = ListNode(0)
    dummy.next = head
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next
    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt
    return dummy.next

# Time: O(n) - traverse to position + reverse
# Space: O(1) - in-place reversal
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
result = reverseBetween(head, 2, 4)
# 1 -> 4 -> 3 -> 2 -> 5
```

---

## Problem 17: Merge k Sorted Lists (Using Min-Heap)

**Difficulty: Hard**

### Problem Statement

Given an array of `k` linked lists, each linked list is sorted in ascending order. Merge all the linked lists into one sorted linked list.

### Approach

Use a **min-heap** of size at most `k`. Push the head of each list into the heap. Pop the smallest, add it to the result, and push its next node if it exists. Repeat until the heap is empty.

```
Lists: [1->4->5], [1->3->4], [2->6]
Heap pops: 1, 1, 2, 3, 4, 4, 5, 6
Result: 1->1->2->3->4->4->5->6
```

### Solution

```python
import heapq

def mergeKLists(lists):
    heap = []
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(heap, (l.val, i, l))
    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, idx, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, idx, node.next))
    return dummy.next

# Time: O(N log k) where N is total nodes, k is number of lists
# Space: O(k) for the heap
```

### Test

```python
l1 = ListNode(1)
l1.next = ListNode(4)
l1.next.next = ListNode(5)
l2 = ListNode(1)
l2.next = ListNode(3)
l2.next.next = ListNode(4)
l3 = ListNode(2)
l3.next = ListNode(6)
result = mergeKLists([l1, l2, l3])
# 1->1->2->3->4->4->5->6
```

---

## Problem 18: Reverse Nodes in k-Group

**Difficulty: Hard**

### Problem Statement

Given the `head` of a linked list, reverse the nodes `k` at a time and return the modified list. If the number of nodes is not a multiple of `k`, the remaining nodes should stay in original order.

### Approach

1. Count nodes to check if we have at least `k` nodes remaining
2. If yes, reverse the first `k` nodes
3. Connect the reversed portion to the rest
4. Repeat for remaining groups

```
1 -> 2 -> 3 -> 4 -> 5, k = 2
After: 2 -> 1 -> 4 -> 3 -> 5
```

### Solution

```python
def reverseKGroup(head, k):
    def reverse(start, end):
        prev, curr = None, start
        while curr != end:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
    count = 0
    node = head
    while node:
        count += 1
        node = node.next
    if count < k:
        return head
    prev_end = None
    curr = head
    result = None
    while count >= k:
        group_start = curr
        for _ in range(k - 1):
            curr = curr.next
        group_end = curr.next
        new_head = reverse(group_start, group_end)
        if not result:
            result = new_head
        if prev_end:
            prev_end.next = new_head
        prev_end = group_start
        curr = group_end
        count -= k
    return result

# Time: O(n) - each node visited twice at most
# Space: O(1) - in-place reversal
```

### Test

```python
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
head.next.next.next = ListNode(4)
head.next.next.next.next = ListNode(5)
result = reverseKGroup(head, 2)
# 2 -> 1 -> 4 -> 3 -> 5
```

---

## Problem 19: LRU Cache

**Difficulty: Hard**

### Problem Statement

Design a data structure that follows the constraints of a **Least Recently Used (LRU) Cache**. Implement `LRUCache` with `get(key)` and `put(key, value)` in O(1) time.

### Approach

Use a **hash map** for O(1) key lookup and a **doubly linked list** for O(1) eviction. The doubly linked list maintains order from most to least recently used. On access, move the node to the front. On eviction, remove from the back.

### Solution

```python
class DLLNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.head = DLLNode()
        self.tail = DLLNode()
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
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.cap:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = DLLNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)

# Time: O(1) for both get and put
# Space: O(capacity) for the cache
```

### Test

```python
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))      # 1
cache.put(3, 3)           # evicts key 2
print(cache.get(2))       # -1
print(cache.get(3))       # 3
```

---

## Problem 20: LFU Cache

**Difficulty: Hard**

### Problem Statement

Design and implement a **Least Frequently Used (LFU) Cache**. Implement `get(key)` and `put(key, value)` in O(1) time. When the cache is full and a new item needs to be inserted, evict the least frequently used item. If there is a tie, evict the least recently used among them.

### Approach

Use:
- A hash map for key -> value lookup
- A hash map for key -> frequency
- A hash map for frequency -> OrderedDict of keys (ordered by recency)
- A variable tracking the minimum frequency

On access, update frequency: remove from old freq list, add to new freq list. On eviction, remove from the min frequency list's first item (LRU within same frequency).

### Solution

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)
        self.min_freq = 0

    def _update(self, key):
        freq = self.key_to_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            del self.freq_to_keys[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        self.key_to_freq[key] = freq + 1
        self.freq_to_keys[freq + 1][key] = None

    def get(self, key):
        if key not in self.key_to_val:
            return -1
        self._update(key)
        return self.key_to_val[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._update(key)
            return
        if len(self.key_to_val) >= self.cap:
            old_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[old_key]
            del self.key_to_freq[old_key]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

# Time: O(1) for both get and put
# Space: O(capacity) for the cache
```

### Test

```python
cache = LFUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))   # 1 (freq of 1 becomes 2)
cache.put(3, 3)        # evicts key 2 (freq 1, LRU)
print(cache.get(2))   # -1
print(cache.get(3))   # 3
```

---

# PART B: STACK & QUEUE (20 Problems)

---

## Problem 21: Valid Parentheses

**Difficulty: Easy**

### Problem Statement

Given a string `s` containing only the characters `(`, `)`, `{`, `}`, `[` and `]`, determine if the input string is valid. An input string is valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order

### Approach

Use a **stack**. Push opening brackets. When encountering a closing bracket, check if the top of the stack is the matching opener. If not, return False. At the end, the stack must be empty.

### Solution

```python
def isValid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0

# Time: O(n) - single pass
# Space: O(n) - worst case all opening brackets
```

### Test

```python
print(isValid("()"))       # True
print(isValid("()[]{}"))   # True
print(isValid("(]"))       # False
print(isValid("([)]"))     # False
print(isValid("{[]}"))     # True
```

---

## Problem 22: Min Stack

**Difficulty: Easy**

### Problem Statement

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

### Approach

Use **two stacks**: one for all values and one to track the current minimum. When pushing, also push onto the min stack if the value is <= current minimum. When popping, pop from min stack if the values match.

### Solution

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]

# Time: O(1) for all operations
# Space: O(n) for the auxiliary stack
```

### Test

```python
ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
print(ms.getMin())  # -3
ms.pop()
print(ms.top())     # 0
print(ms.getMin())  # -2
```

---

## Problem 23: Max Stack

**Difficulty: Easy**

### Problem Statement

Design a stack that supports push, pop, top, popMax (removes the maximum element), and peekMax (retrieves the maximum element).

### Approach

Use two stacks: one for the main stack and one to track the maximum. On push, if the value >= current max, push onto the max stack. On popMax, if values match, pop from max stack. For peekMax, return the top of the max stack.

### Solution

```python
class MaxStack:
    def __init__(self):
        self.stack = []
        self.max_stack = []

    def push(self, val):
        self.stack.append(val)
        if not self.max_stack or val >= self.max_stack[-1]:
            self.max_stack.append(val)

    def pop(self):
        val = self.stack.pop()
        if val == self.max_stack[-1]:
            self.max_stack.pop()
        return val

    def top(self):
        return self.stack[-1]

    def peekMax(self):
        return self.max_stack[-1]

    def popMax(self):
        max_val = self.max_stack.pop()
        buffer = []
        while self.stack[-1] != max_val:
            buffer.append(self.stack.pop())
        self.stack.pop()
        while buffer:
            self.push(buffer.pop())
        return max_val

# Time: O(1) for push/pop/top/peekMax, O(n) worst case for popMax
# Space: O(n)
```

### Test

```python
ms = MaxStack()
ms.push(5)
ms.push(1)
ms.push(5)
print(ms.popMax())  # 5
print(ms.top())     # 1
print(ms.peekMax()) # 5
```

---

## Problem 24: Implement Queue using Stacks

**Difficulty: Easy**

### Problem Statement

Implement a FIFO queue using only two stacks. Supported operations: `push`, `pop`, `peek`, and `empty`.

### Approach

Use **amortized approach** with two stacks: `inbox` for push and `outbox` for pop/peek. When `outbox` is empty and we need to pop/peek, transfer all elements from `inbox` to `outbox` (reversing the order). Each element is moved at most once, giving amortized O(1).

### Solution

```python
class MyQueue:
    def __init__(self):
        self.inbox = []
        self.outbox = []

    def push(self, x):
        self.inbox.append(x)

    def _transfer(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())

    def pop(self):
        self._transfer()
        return self.outbox.pop()

    def peek(self):
        self._transfer()
        return self.outbox[-1]

    def empty(self):
        return not self.inbox and not self.outbox

# Time: O(1) amortized for all operations
# Space: O(n)
```

### Test

```python
q = MyQueue()
q.push(1)
q.push(2)
print(q.peek())   # 1
print(q.pop())    # 1
print(q.empty())  # False
```

---

## Problem 25: Implement Stack using Queues

**Difficulty: Easy**

### Problem Statement

Implement a LIFO stack using only queues. Supported operations: `push`, `top`, `pop`, and `empty`.

### Approach

On `push`, add the new element to the queue, then rotate the queue (dequeue and enqueue) `n-1` times to bring the new element to the front. This makes the queue behave like a stack.

### Solution

```python
from collections import deque

class MyStack:
    def __init__(self):
        self.q = deque()

    def push(self, x):
        self.q.append(x)
        for _ in range(len(self.q) - 1):
            self.q.append(self.q.popleft())

    def pop(self):
        return self.q.popleft()

    def top(self):
        return self.q[0]

    def empty(self):
        return len(self.q) == 0

# Time: O(n) for push, O(1) for pop/top/empty
# Space: O(n)
```

### Test

```python
s = MyStack()
s.push(1)
s.push(2)
print(s.top())    # 2
print(s.pop())    # 2
print(s.empty())  # False
```

---

## Problem 26: Backspace String Compare

**Difficulty: Easy**

### Problem Statement

Given two strings `s` and `t`, return `True` if they are equal when both are typed into empty text editors. `#` means a backspace character.

### Approach

Use a **stack** for each string. Push characters onto the stack. When encountering `#`, pop from the stack (if non-empty). After processing both strings, compare the stacks.

```
s = "ab#c", t = "ad#c"
Stack s: ['a', 'b'] -> pop b -> ['a'] -> push c -> ['a', 'c']
Stack t: ['a', 'd'] -> pop d -> ['a'] -> push c -> ['a', 'c']
Equal -> True
```

### Solution

```python
def backspaceCompare(s, t):
    def build(text):
        stack = []
        for char in text:
            if char == '#':
                if stack:
                    stack.pop()
            else:
                stack.append(char)
        return stack
    return build(s) == build(t)

# Time: O(n + m) where n, m are lengths of s, t
# Space: O(n + m) for the stacks
```

### Test

```python
print(backspaceCompare("ab#c", "ad#c"))  # True
print(backspaceCompare("ab##", "c#d#"))  # True
print(backspaceCompare("a#c", "b"))      # False
```

---

## Problem 27: Final Prices With a Special Discount in a Shop

**Difficulty: Easy**

### Problem Statement

Given an array `prices` where `prices[i]` is the price of the `ith` item, you get a discount equal to `prices[j]` where `j` is the minimum index such that `j > i` and `prices[j] <= prices[i]`. If no such `j` exists, no discount. Return the final prices.

### Approach

Use a **monotonic stack** storing indices. For each price, pop from the stack while the top element's price is >= current price. The current price is the discount for each popped element. Push the current index.

```
prices = [8, 4, 6, 2, 3]
Result: [4, 2, 4, 2, 3]
```

### Solution

```python
def finalPrices(prices):
    stack = []
    result = prices[:]
    for i in range(len(prices)):
        while stack and prices[stack[-1]] >= prices[i]:
            result[stack.pop()] -= prices[i]
        stack.append(i)
    return result

# Time: O(n) - each element pushed/popped at most once
# Space: O(n) - for the stack
```

### Test

```python
print(finalPrices([8, 4, 6, 2, 3]))  # [4, 2, 4, 2, 3]
print(finalPrices([1, 2, 3, 4, 5]))  # [1, 2, 3, 4, 5]
print(finalPrices([10, 1, 1, 6]))    # [9, 0, 1, 6]
```

---

## Problem 28: Make The String Great

**Difficulty: Easy**

### Problem Statement

Given a string `s` of lower and upper case English letters, a "good" string has no two adjacent characters that are the same letter but with different cases (e.g., `'a'` and `'A'`). Remove bad adjacent pairs until the string is good.

### Approach

Use a **stack**. For each character, check if it forms a bad pair with the top of the stack (same letter, different case). If yes, pop from the stack. Otherwise, push the character. The remaining stack is the answer.

```
s = "leEeetCode"
Push l, e, E (e and E are bad pair, pop both)
Push e, e, t, c, o, d, e
Result: "leetcode"
```

### Solution

```python
def makeGood(s):
    stack = []
    for char in s:
        if stack and stack[-1] != char and stack[-1].lower() == char.lower():
            stack.pop()
        else:
            stack.append(char)
    return ''.join(stack)

# Time: O(n) - single pass
# Space: O(n) - for the stack
```

### Test

```python
print(makeGood("leEeetCode"))  # "leetcode"
print(makeGood("abBAcC"))      # ""
print(makeGood("s"))           # "s"
```

---

## Problem 29: Daily Temperatures

**Difficulty: Medium**

### Problem Statement

Given an array of integers `temperatures` representing daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `ith` day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0`.

### Approach

Use a **monotonic decreasing stack** that stores indices. For each day, while the stack's top index has a temperature less than today's, pop it and set its answer to `today - popped_index`. Push today's index.

```
temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
Answer:       [1,  1,  4,  2,  1,  1,  0,  0]
```

### Solution

```python
def dailyTemperatures(temperatures):
    n = len(temperatures)
    answer = [0] * n
    stack = []
    for i in range(n):
        while stack and temperatures[stack[-1]] < temperatures[i]:
            prev = stack.pop()
            answer[prev] = i - prev
        stack.append(i)
    return answer

# Time: O(n) - each index pushed/popped once
# Space: O(n) - for the stack
```

### Test

```python
print(dailyTemperatures([73,74,75,71,69,72,76,73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

---

## Problem 30: Next Greater Element I

**Difficulty: Medium**

### Problem Statement

You are given two integer arrays `nums1` (subset) and `nums2` (unique values). For each element in `nums1`, find the next greater element in `nums2`. Return the answer array.

### Approach

Use a **monotonic decreasing stack** on `nums2`. Build a map of `value -> next greater element`. For each element in `nums1`, look up the map.

```
nums1 = [4, 1, 2], nums2 = [1, 3, 4, 2]
Map: {1: 3, 3: -1, 4: -1, 2: -1}
Answer: [-1, 3, -1]
```

### Solution

```python
def nextGreaterElement(nums1, nums2):
    stack = []
    next_greater = {}
    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)
    while stack:
        next_greater[stack.pop()] = -1
    return [next_greater[num] for num in nums1]

# Time: O(m + n) where m, n are lengths of nums1, nums2
# Space: O(n) for the map and stack
```

### Test

```python
print(nextGreaterElement([4,1,2], [1,3,4,2]))  # [-1, 3, -1]
print(nextGreaterElement([2,4], [1,2,3,4]))     # [3, -1]
```

---

## Problem 31: Next Greater Element II

**Difficulty: Medium**

### Problem Statement

Given a circular integer array `nums`, return the next greater element for each element. The next greater element is the first element you encounter that is strictly greater, moving circularly.

### Approach

Use a **monotonic decreasing stack** and iterate through the array **twice** (simulating circular traversal using `i % n`). This ensures all elements find their next greater even across the circular boundary.

```
nums = [1, 2, 1]
Result: [2, -1, 2]
```

### Solution

```python
def nextGreaterElements(nums):
    n = len(nums)
    result = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            result[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return result

# Time: O(n) - each element pushed/popped at most twice
# Space: O(n) - for the stack
```

### Test

```python
print(nextGreaterElements([1, 2, 1]))       # [2, -1, 2]
print(nextGreaterElements([1, 2, 3, 4, 3])) # [2, 3, 4, -1, 4]
```

---

## Problem 32: Stock Span Problem

**Difficulty: Medium**

### Problem Statement

The stock span problem is a financial problem. Given an array of prices, the span of the stock's price on a given day is the maximum number of consecutive days (including the current day) for which the price was less than or equal to the current day's price.

### Approach

Use a **monotonic decreasing stack** storing indices. For each day, pop from the stack while the price at the stack's top is less than or equal to today's price. The span is `today's index - stack's top index` (or `today's index + 1` if stack is empty).

```
prices = [100, 80, 60, 70, 60, 75, 85]
spans  = [1,   1,  1,  2,  1,  4,  6]
```

### Solution

```python
def calculateSpan(prices):
    n = len(prices)
    spans = [0] * n
    stack = []
    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        spans[i] = i + 1 if not stack else i - stack[-1]
        stack.append(i)
    return spans

# Time: O(n) - each element pushed/popped once
# Space: O(n) - for the stack
```

### Test

```python
print(calculateSpan([100, 80, 60, 70, 60, 75, 85]))
# [1, 1, 1, 2, 1, 4, 6]
```

---

## Problem 33: Asteroid Collision

**Difficulty: Medium**

### Problem Statement

Given an array `asteroids` of integers representing asteroids in a line. A positive value means moving right, negative means moving left. When two asteroids collide, the smaller one explodes. If they are the same size, both explode. Return the state of the asteroids after all collisions.

### Approach

Use a **stack**. Push right-moving asteroids (`> 0`). When encountering a left-moving asteroid (`< 0`), pop from the stack while the top is right-moving and smaller than the current. Handle equal sizes and surviving left-movers.

```
asteroids = [5, 10, -5]
Result: [5, 10]  (10 destroys -5)
```

### Solution

```python
def asteroidCollision(asteroids):
    stack = []
    for ast in asteroids:
        if ast > 0:
            stack.append(ast)
        else:
            while stack and stack[-1] > 0 and stack[-1] < abs(ast):
                stack.pop()
            if not stack or stack[-1] < 0:
                stack.append(ast)
            elif stack[-1] == abs(ast):
                stack.pop()
    return stack

# Time: O(n) - each asteroid pushed/popped at most once
# Space: O(n) - for the stack
```

### Test

```python
print(asteroidCollision([5, 10, -5]))       # [5, 10]
print(asteroidCollision([8, -8]))            # []
print(asteroidCollision([10, 2, -5]))        # [10]
print(asteroidCollision([-2, -1, 1, 2]))    # [-2, -1, 1, 2]
```

---

## Problem 34: Using a Robot to Print the Lexicographically Smallest String

**Difficulty: Medium**

### Problem Statement

Given a string `s`, a robot at position 0 can: move right, push current char to stack, or pop from stack and print. Print the lexicographically smallest string possible.

### Approach

Use a **stack**. Precompute the minimum character to the right of each position. If the top of the stack is <= the smallest remaining character, pop and print it. Otherwise, move right (push to stack). This ensures we print the smallest available character as early as possible.

### Solution

```python
def robotWithString(s):
    n = len(s)
    min_right = [''] * (n + 1)
    min_right[n - 1] = s[n - 1]
    for i in range(n - 2, -1, -1):
        min_right[i] = min(s[i], min_right[i + 1])
    stack = []
    result = []
    for i, char in enumerate(s):
        stack.append(char)
        while stack and stack[-1] <= min_right[i + 1] if i + 1 < n else True:
            result.append(stack.pop())
            if not (i + 1 < n):
                break
    while stack:
        result.append(stack.pop())
    return ''.join(result)

# Time: O(n) - each character pushed/popped at most once
# Space: O(n) - for stack and min_right array
```

### Test

```python
print(robotWithString("zza"))       # "azz"
print(robotWithString("bac"))       # "abc"
print(robotWithString("cbacdcbc"))  # "abcdcbca"
```

---

## Problem 35: Minimum Remove to Make Valid Parentheses

**Difficulty: Medium**

### Problem Statement

Given a string `s` of `'('`, `')'`, and lowercase English characters, remove the minimum number of parentheses to make the string valid. Return any valid string.

### Approach

Use a **stack** to track indices of unmatched opening parentheses. Also track indices to remove. For unmatched closing parentheses, add their index to the remove set. After processing, remove all marked indices from the string.

### Solution

```python
def minRemoveToMakeValid(s):
    stack = []
    to_remove = set()
    for i, char in enumerate(s):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                stack.pop()
            else:
                to_remove.add(i)
    while stack:
        to_remove.add(stack.pop())
    result = []
    for i, char in enumerate(s):
        if i not in to_remove:
            result.append(char)
    return ''.join(result)

# Time: O(n) - single pass + string construction
# Space: O(n) - for the stack and result
```

### Test

```python
print(minRemoveToMakeValid("lee(t(c)o)de)"))    # "lee(t(c)o)de"
print(minRemoveToMakeValid("a b(c)d"))           # "ab(c)d"  (no change needed)
print(minRemoveToMakeValid("))(("))              # ""
```

---

## Problem 36: Reorder Routes to Make All Paths Lead to City Zero

**Difficulty: Medium**

### Problem Statement

Given `n` cities numbered `0` to `n-1` and `connections` where `connections[i] = [a, b]` represents a one-way road from `a` to `b`, return the minimum number of roads to reverse so that every city can reach city `0`.

### Approach

Build the graph treating all edges as undirected, but track the original direction. Use **BFS** from city 0. If we traverse an edge in the original direction (away from 0), it costs 1 reversal. If we traverse it towards 0, it costs 0. Find the minimum cost to reach all nodes.

### Solution

```python
from collections import deque

def minReorder(n, connections):
    adj = [[] for _ in range(n)]
    for a, b in connections:
        adj[a].append((b, 1))
        adj[b].append((a, 0))
    visited = [False] * n
    visited[0] = True
    queue = deque([0])
    reversals = 0
    while queue:
        node = queue.popleft()
        for neighbor, cost in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                reversals += cost
                queue.append(neighbor)
    return reversals

# Time: O(n) - BFS traverses all nodes
# Space: O(n) - for the adjacency list and visited array
```

### Test

```python
print(minReorder(6, [[0,1],[1,3],[2,3],[4,0],[4,5]]))  # 3
print(minReorder(5, [[1,0],[1,2],[3,2],[3,4]]))          # 2
print(minReorder(3, [[1,0],[2,0]]))                      # 0
```

---

## Problem 37: Largest Rectangle in Histogram

**Difficulty: Hard**

### Problem Statement

Given an array of integers `heights` representing the histogram's bar width where the width of each bar is 1, find the area of the largest rectangle in the histogram.

### Approach

Use a **monotonic increasing stack** of indices. For each bar, while the current bar is shorter than the stack's top, pop and calculate the area with the popped bar as the shortest bar. The width extends from the current index to the new stack top. Push the current index.

```
heights = [2,1,5,6,2,3]
Largest rectangle = 10 (bars at index 2 and 3, height 5)
```

### Solution

```python
def largestRectangleArea(heights):
    stack = [-1]
    max_area = 0
    for i in range(len(heights)):
        while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)
    while stack[-1] != -1:
        h = heights[stack.pop()]
        w = len(heights) - stack[-1] - 1
        max_area = max(max_area, h * w)
    return max_area

# Time: O(n) - each index pushed/popped once
# Space: O(n) - for the stack
```

### Test

```python
print(largestRectangleArea([2,1,5,6,2,3]))  # 10
print(largestRectangleArea([2,4]))           # 4
print(largestRectangleArea([1]))             # 1
```

---

## Problem 38: Maximal Rectangle

**Difficulty: Hard**

### Problem Statement

Given a `m x n` binary matrix filled with 0s and 1s, find the largest rectangle containing only 1s and return its area.

### Approach

Convert each row into a **histogram** of heights. For each row, compute the largest rectangle in the histogram (using Problem 37). The maximum across all rows is the answer.

```
Matrix:
1 0 1 0 0
1 0 1 1 1
1 1 1 1 1
1 0 0 1 0
Heights for row 2: [4, 1, 3, 4, 1]
Largest rectangle in row 2's histogram = 6
```

### Solution

```python
def maximalRectangle(matrix):
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * (cols + 1)
    max_area = 0
    for row in range(rows):
        for col in range(cols):
            heights[col] = heights[col] + 1 if matrix[row][col] == '1' else 0
        stack = [-1]
        for i in range(cols + 1):
            while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                max_area = max(max_area, h * w)
            stack.append(i)
    return max_area

# Time: O(m * n) - process each row with histogram algorithm
# Space: O(n) - for the heights array and stack
```

### Test

```python
print(maximalRectangle([
    ["1","0","1","0","0"],
    ["1","0","1","1","1"],
    ["1","1","1","1","1"],
    ["1","0","0","1","0"]
]))  # 6
```

---

## Problem 39: Trapping Rain Water

**Difficulty: Hard**

### Problem Statement

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

### Approach

Use a **monotonic decreasing stack**. For each bar, while the current bar is taller than the stack's top, pop the top (this is the trapped water's bottom). The width is the distance between the current index and the new stack top. The height is `min(current_height, stack_top_height) - popped_height`.

```
height = [0,1,0,2,1,0,1,3,2,1,2,1]
Water = 6 units
```

### Solution

```python
def trap(height):
    stack = []
    water = 0
    for i in range(len(height)):
        while stack and height[stack[-1]] < height[i]:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            h = min(height[i], height[stack[-1]]) - height[bottom]
            water += width * h
        stack.append(i)
    return water

# Time: O(n) - each element pushed/popped once
# Space: O(n) - for the stack
```

### Test

```python
print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # 6
print(trap([4,2,0,3,2,5]))               # 9
print(trap([1,0,1]))                      # 1
```

---

## Problem 40: Sliding Window Maximum

**Difficulty: Hard**

### Problem Statement

Given an array `nums` and a sliding window of size `k` moving from left to right, return the max value in each window position.

### Approach

Use a **monotonic decreasing deque** (double-ended queue) storing indices. For each element:
1. Remove indices outside the window from the front
2. Remove all smaller elements from the back (they will never be the max)
3. Push current index
4. The front of the deque is the max for the current window

```
nums = [1,3,-1,-3,5,3,6,7], k = 3
Result: [3,3,5,5,6,7]
```

### Solution

```python
from collections import deque

def maxSlidingWindow(nums, k):
    dq = deque()
    result = []
    for i in range(len(nums)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# Time: O(n) - each element pushed/popped at most once
# Space: O(k) - for the deque
```

### Test

```python
print(maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3))  # [3,3,5,5,6,7]
print(maxSlidingWindow([1], 1))                     # [1]
print(maxSlidingWindow([9,11], 2))                  # [11]
print(maxSlidingWindow([4,3,2,1], 2))               # [4,3,2]
```

---

# Summary Table

| # | Problem | Difficulty | Time | Space |
|---|---------|-----------|------|-------|
| 1 | Delete Node in Linked List | Easy | O(1) | O(1) |
| 2 | Middle of Linked List | Easy | O(n) | O(1) |
| 3 | Palindrome Linked List | Easy | O(n) | O(1) |
| 4 | Remove Linked List Elements | Easy | O(n) | O(1) |
| 5 | Linked List Components | Easy | O(n+m) | O(m) |
| 6 | Binary to Decimal | Easy | O(n) | O(1) |
| 7 | Split Linked List in Parts | Easy | O(n+k) | O(1) |
| 8 | Remove Duplicates Unsorted | Easy | O(n) | O(n) |
| 9 | Rotate List | Medium | O(n) | O(1) |
| 10 | Swap Nodes in Pairs | Medium | O(n) | O(1) |
| 11 | Odd Even Linked List | Medium | O(n) | O(1) |
| 12 | Add Two Numbers II | Medium | O(m+n) | O(m+n) |
| 13 | Copy List Random Pointer | Medium | O(n) | O(1) |
| 14 | Flatten Multilevel DLL | Medium | O(n) | O(d) |
| 15 | Partition List | Medium | O(n) | O(1) |
| 16 | Reverse Linked List II | Medium | O(n) | O(1) |
| 17 | Merge k Sorted Lists | Hard | O(N log k) | O(k) |
| 18 | Reverse Nodes in k-Group | Hard | O(n) | O(1) |
| 19 | LRU Cache | Hard | O(1) | O(cap) |
| 20 | LFU Cache | Hard | O(1) | O(cap) |
| 21 | Valid Parentheses | Easy | O(n) | O(n) |
| 22 | Min Stack | Easy | O(1) | O(n) |
| 23 | Max Stack | Easy | O(1)* | O(n) |
| 24 | Queue using Stacks | Easy | O(1) amortized | O(n) |
| 25 | Stack using Queues | Easy | O(n) push | O(n) |
| 26 | Backspace String Compare | Easy | O(n+m) | O(n+m) |
| 27 | Final Prices Discount | Easy | O(n) | O(n) |
| 28 | Make The String Great | Easy | O(n) | O(n) |
| 29 | Daily Temperatures | Medium | O(n) | O(n) |
| 30 | Next Greater Element I | Medium | O(m+n) | O(n) |
| 31 | Next Greater Element II | Medium | O(n) | O(n) |
| 32 | Stock Span Problem | Medium | O(n) | O(n) |
| 33 | Asteroid Collision | Medium | O(n) | O(n) |
| 34 | Robot Lexicographically Smallest | Medium | O(n) | O(n) |
| 35 | Min Remove Valid Parentheses | Medium | O(n) | O(n) |
| 36 | Reorder Routes City Zero | Medium | O(n) | O(n) |
| 37 | Largest Rectangle Histogram | Hard | O(n) | O(n) |
| 38 | Maximal Rectangle | Hard | O(m*n) | O(n) |
| 39 | Trapping Rain Water | Hard | O(n) | O(n) |
| 40 | Sliding Window Maximum | Hard | O(n) | O(k) |

> *MaxStack popMax is O(n) worst case but O(1) amortized
