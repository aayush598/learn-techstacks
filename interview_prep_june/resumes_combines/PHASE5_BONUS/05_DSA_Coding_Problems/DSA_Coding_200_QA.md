# DSA Coding Problems - 200+ Interview Q&A

## Arrays (Q1-Q40)

### Q1: Two Sum
**Problem:** Find indices of two numbers that sum to target.
**Solution:** HashMap. For each num, check if target-num in map. O(n).
```
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```

### Q2: Maximum Subarray (Kadane)
**Problem:** Find contiguous subarray with max sum.
**Solution:** curr = max(num, curr+num), max_sum = max(max_sum, curr). O(n).
```
def maxSubArray(nums):
    curr = max_sum = nums[0]
    for num in nums[1:]:
        curr = max(num, curr + num)
        max_sum = max(max_sum, curr)
    return max_sum
```

### Q3: Product of Array Except Self
**Problem:** Output array where output[i] = product of all elements except nums[i]. No division.
**Solution:** Left products + right products. O(n) time, O(1) space (output excluded).
```
def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    right = 1
    for i in range(n-1, -1, -1):
        result[i] *= right
        right *= nums[i]
    return result
```

## Strings (Q41-Q70)

### Q4: Longest Substring Without Repeating Characters
**Problem:** Find length of longest substring without repeating chars.
**Solution:** Sliding window with set/dict. O(n).
```
def lengthOfLongestSubstring(s):
    used = {}
    start = max_len = 0
    for i, c in enumerate(s):
        if c in used and used[c] >= start:
            start = used[c] + 1
        used[c] = i
        max_len = max(max_len, i - start + 1)
    return max_len
```

### Q5: Valid Anagram
**Problem:** Check if two strings are anagrams.
**Solution:** Count chars (Counter) or sort both. O(n).
```
def isAnagram(s, t):
    return Counter(s) == Counter(t)
```

## Linked Lists (Q71-Q90)

### Q6: Reverse Linked List
**Problem:** Reverse a singly linked list.
**Solution:** Three pointers iterative or recursive.
```
def reverseList(head):
    prev = None
    curr = head
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    return prev
```

### Q7: Merge Two Sorted Lists
**Problem:** Merge two sorted linked lists.
**Solution:** Dummy head, compare nodes. O(n+m).
```
def mergeTwoLists(l1, l2):
    dummy = curr = ListNode()
    while l1 and l2:
        if l1.val < l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next
```

## Trees (Q91-Q130)

### Q8: Maximum Depth of Binary Tree
**Problem:** Find maximum depth.
**Solution:** Recursive: 1 + max(maxDepth(left), maxDepth(right)). O(n).

### Q9: Validate Binary Search Tree
**Problem:** Check if tree is valid BST.
**Solution:** Inorder traversal should be sorted. Or recursive with min/max bounds.

### Q10: Level Order Traversal
**Problem:** Return nodes level by level.
**Solution:** BFS with queue. Track level size.

## Dynamic Programming (Q131-Q160)

### Q11: Climbing Stairs
**Problem:** n steps, climb 1 or 2 at a time. How many ways?
**Solution:** DP[i] = DP[i-1] + DP[i-2]. Fibonacci.

### Q12: Coin Change
**Problem:** Minimum coins to make amount.
**Solution:** DP[amount] = min(DP[amount-coin] + 1) for all coins. O(amount * coins).

## Graphs (Q161-Q180)

### Q13: Number of Islands
**Problem:** Count islands in grid (1=land, 0=water).
**Solution:** DFS/BFS on each unvisited 1. O(m*n).

### Q14: Course Schedule (Topological Sort)
**Problem:** Can you finish all courses given prerequisites?
**Solution:** Detect cycle in directed graph. Kahn's algorithm (BFS in-degree).

## Heap & Stack (Q181-Q200)

### Q15: Top K Frequent Elements
**Problem:** Return k most frequent elements.
**Solution:** Counter + heap (nlargest). Or bucket sort.

### Q16: Valid Parentheses
**Problem:** Check bracket string validity.
**Solution:** Stack. Opening → push, closing → pop if matching.
