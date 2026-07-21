# Two Pointer Similar Problems Collection

## 1. Pair with Given Difference (LeetCode 532 / GFG)

**Problem:** Find count of pairs in array with difference equal to target k.

```python
def count_pairs_with_difference(arr, k):
    arr.sort()
    count = 0
    left, right = 0, 1
    while right < len(arr):
        diff = arr[right] - arr[left]
        if left != right and diff == k:
            count += 1
            left += 1
            right += 1
        elif diff < k:
            right += 1
        else:
            left += 1
        if left == right:
            right += 1
    return count
# Time: O(n log n), Space: O(1)
```

---

## 2. Pair with Given Sum (LeetCode 1)

**Problem:** Find two numbers that add up to target.

```python
# Two pointer (sorted array)
def two_sum_sorted(arr, target):
    arr.sort()
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]

# Hash map (unsorted array) - O(n) time
def two_sum_hash(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

---

## 3. Sort Array by Parity (LeetCode 905)

**Problem:** Put all even numbers before odd numbers.

```python
def sort_by_parity(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        if nums[left] % 2 == 0:
            left += 1
        elif nums[right] % 2 == 1:
            right -= 1
        else:
            nums[left], nums[right] = nums[right], nums[left]
            left += 1
            right -= 1
    return nums
# Time: O(n), Space: O(1)
# Same direction variant:
def sort_by_parity_v2(nums):
    even = 0
    for i in range(len(nums)):
        if nums[i] % 2 == 0:
            nums[even], nums[i] = nums[i], nums[even]
            even += 1
    return nums
```

---

## 4. Squares of Sorted Array (LeetCode 977)

**Problem:** Return sorted squares of sorted array (may have negatives).

```python
def sorted_squares(nums):
    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    pos = n - 1  # Fill from end (largest first)
    while left <= right:
        if abs(nums[left]) > abs(nums[right]):
            result[pos] = nums[left] ** 2
            left += 1
        else:
            result[pos] = nums[right] ** 2
            right -= 1
        pos -= 1
    return result
# Time: O(n), Space: O(n)
# Largest square is at one of the two ends
```

---

## 5. Remove Element In-Place (LeetCode 27)

**Problem:** Remove all occurrences of val, return new length.

```python
def remove_element(nums, val):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow
# [3,2,2,3] val=3
# fast=0: 3==3, skip
# fast=1: 2!=3, nums[0]=2, slow=1
# fast=2: 2!=3, nums[1]=2, slow=2
# fast=3: 3==3, skip
# Return 2, nums=[2,2,_,_]
```

---

## 6. Valid Palindrome II (LeetCode 680)

**Problem:** Can string be palindrome by removing at most one character?

```python
def valid_palindrome_ii(s):
    def is_pal(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True
    
    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return is_pal(l + 1, r) or is_pal(l, r - 1)
        l += 1
        r -= 1
    return True
# Time: O(n), Space: O(1)
```

---

## 7. Shortest Unsorted Continuous Subarray (LeetCode 581)

**Problem:** Find length of shortest unsorted subarray to sort whole array.

```python
def find_unsorted_subarray(nums):
    n = len(nums)
    left, right = -1, -1
    
    # Find first dip from left
    max_seen = nums[0]
    for i in range(1, n):
        if nums[i] < max_seen:
            right = i
        max_seen = max(max_seen, nums[i])
    
    # Find first rise from right
    min_seen = nums[n - 1]
    for i in range(n - 2, -1, -1):
        if nums[i] > min_seen:
            left = i
        min_seen = min(min_seen, nums[i])
    
    return right - left + 1 if right != -1 else 0
# Time: O(n), Space: O(1)
```

---

## 8. Max Consecutive Ones After Flip (Variant)

**Problem:** Find max consecutive 1s if you can flip at most k zeros.

```python
def longest_ones(nums, k):
    left = 0
    max_len = 0
    zeros = 0
    for right in range(len(nums)):
        if nums[right] == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        max_len = max(max_len, right - left + 1)
    return max_len
# Time: O(n), Space: O(1)
```

---

## 9. Subarray with Given Sum (Positive Numbers Only)

**Problem:** Find subarray with sum equal to target (all positive).

```python
def subarray_sum_positive(arr, target):
    left = 0
    current_sum = 0
    for right in range(len(arr)):
        current_sum += arr[right]
        while current_sum > target and left <= right:
            current_sum -= arr[left]
            left += 1
        if current_sum == target:
            return [left, right]
    return [-1, -1]
# Time: O(n), Space: O(1)
# Only works with positive numbers (shrinking window)
```

---

## 10. Is Subsequence (LeetCode 392)

**Problem:** Check if s is subsequence of t.

```python
def is_subsequence(s, t):
    i = j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
# Time: O(n), Space: O(1)
```

---

## Quick Reference Table

| Problem | Key Insight | Time |
|---------|------------|------|
| Pair with difference | Sort + two pointer with gap | O(n log n) |
| Pair with sum | Sort + opposite direction | O(n log n) |
| Sort by parity | Partition like Dutch flag | O(n) |
| Squares sorted | Largest at ends, fill backwards | O(n) |
| Remove element | Fast/slow pointer | O(n) |
| Valid palindrome II | Try removing from either end | O(n) |
| Shortest unsorted subarray | Find boundaries using max/min scan | O(n) |
| Max ones flip k | Sliding window with zero count | O(n) |
| Subarray positive sum | Shrink window when sum > target | O(n) |
| Is subsequence | Greedy two pointer | O(n) |
