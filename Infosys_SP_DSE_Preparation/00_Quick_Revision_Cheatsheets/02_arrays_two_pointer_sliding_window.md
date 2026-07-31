# Arrays, Two Pointers, Sliding Window

Dense, tested templates for array problems. Understand the skeleton, then modify the highlighted parts per problem.

## Array operation syntax

```python
a = [3, 1, 2]
arr = [(1, 2), (3, 4)]
nums = [-5, 3, -1]
n, m = 2, 3
a.reverse()                    # in-place, O(n)
rev = a[::-1]                  # reversed copy, O(n)
a.sort(); a.sort(reverse=True) # in-place, O(n log n)

# Rotate right by k (LeetCode 189) — in-place via triple reverse
def rotate(nums, k):
    n = len(nums); k %= n
    def rev(i, j):
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1; j -= 1
    rev(0, n - 1); rev(0, k - 1); rev(k, n - 1)

# max / min with key
best = max(arr)                                # O(n)
best = max(arr, key=lambda x: x[1])            # max by element (x[1])
best = max(nums, key=abs)                      # max absolute value

# Prefix sums — prefix[i] = sum of arr[0..i-1]
def prefix_sums(arr):
    p = [0]
    for x in arr:
        p.append(p[-1] + x)
    return p
# p[i] - p[j] = sum of arr[j..i-1]  -> subarray sum in O(1)
# p = [0,1,3,6,10] for [1,2,3,4]; sum(arr[1:4]) = p[4]-p[1] = 9

# 2D array — create with comprehension (NEVER [[0]*n]*m)
grid = [[0] * n for _ in range(m)]
```

## Two pointer templates

### 1. Opposite ends — sorted 2-sum (pairs/target)
```python
def two_sum_sorted(arr, target):          # input SORTED, distinct handled naturally
    i, j = 0, len(arr) - 1
    while i < j:
        s = arr[i] + arr[j]
        if s == target:
            return [i, j]                 # modify: collect pairs, count pairs, etc.
        elif s < target:
            i += 1                        # sum too small -> need bigger value
        else:
            j -= 1                        # sum too big -> need smaller value
    return [-1, -1]
```
Complexity: O(n) time, O(1) space.
Usage: count pairs with sum = k, three-sum, container with most water, square of sorted array (two ends toward middle).

### 2. Slow–fast pointers
```python
def middle(arr):                          # middle of linked list / array
    slow = fast = 0
    while fast < len(arr) - 1 and fast < len(arr):
        slow += 1
        fast += 2
    return slow
# Cycle detection (linked list): advance slow by 1, fast by 2,
# if slow == fast there is a cycle. Linked-list nodes, not arrays.
```
Complexity: O(n) time, O(1) space.

### 3. Partition around pivot (Hoare / Lomuto)
```python
def partition(arr, lo, hi):               # picks arr[hi] as pivot
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] <= pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i                              # pivot now at final index i
# Usage: quicksort, quickselect (kth smallest), move zeros,
# Dutch flag (use 3-way partition), sort colors.
```
Complexity: O(n) time per partition, O(1) space.

## Sliding window templates

### 1. Fixed window size k — for loop over window end
```python
def fixed_window_sum(arr, k):             # e.g. max sum subarray of size k
    cur = sum(arr[:k])                    # seed first window
    best = cur
    for i in range(k, len(arr)):          # i = new element entering window
        cur += arr[i] - arr[i - k]        # add right, drop left
        best = max(best, cur)
    return best
```
Complexity: O(n) time, O(1) space.
Modify: track `avg` instead of `best`, collect every window value, count windows matching condition.

### 2. Variable window — while-shrink (longest valid window)
```python
def longest_le(arr, target):              # longest subarray with sum <= target
    left = 0
    cur = 0
    best = 0
    for right, x in enumerate(arr):       # right = window end
        cur += x
        while cur > target:               # shrink while INVALID
            cur -= arr[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```
Complexity: O(n) time, O(1) space (each element enters/exits once).
Modify: change the `while` condition to the problem's invalid-state predicate; return `left` for "minimum length" variants.

### 3. Variable window with hashmap — at most k distinct chars
```python
def at_most_k(s, k):                      # longest substring, <= k distinct chars
    from collections import defaultdict
    cnt = defaultdict(int)
    left = ans = 0
    for right, ch in enumerate(s):
        cnt[ch] += 1
        while len(cnt) > k:               # too many distinct -> shrink
            cnt[s[left]] -= 1
            if cnt[s[left]] == 0:
                del cnt[s[left]]          # MUST delete 0-count keys, len() depends on it
            left += 1
        ans = max(ans, right - left + 1)
    return ans
```
Complexity: O(n) time, O(k) space.

## Canonical templates

### Kadane — maximum subarray sum (LeetCode 53)
```python
def max_subarray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)             # extend best subarray OR restart at x
        best = max(best, cur)
    return best
```
Complexity: O(n) time, O(1) space. Works with all-negative arrays (returns max element).
Variants: circular subarray (max of Kadane and total−min-subarray); max product (track min and max product).

### Two-pointer 2-sum (indices)
```python
def two_sum(nums, target):
    d = {}
    for i, x in enumerate(nums):
        if target - x in d:
            return [d[target - x], i]     # complement seen earlier
        d[x] = i
    return []
```
Complexity: O(n) time, O(n) space. For SORTED input, use the opposite-ends template for O(1) space.

### Fixed sliding window max — monotonic deque (LeetCode 239)
```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()                          # stores INDICES, values decreasing
    res = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:   # pop smaller values (useless now)
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:                # index fell out of window
            dq.popleft()
        if i >= k - 1:                    # window full -> record max
            res.append(nums[dq[0]])
    return res
```
Complexity: O(n) time (each index pushed/popped once), O(k) space.
Same deque trick solves sliding window minimum (flip the `<=` to `>=`).

### Variable window — longest substring without repeating chars (LeetCode 3)
```python
def length_of_longest_substring(s):
    last = {}                             # char -> last seen index
    left = ans = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:   # duplicate INSIDE window
            left = last[ch] + 1           # jump left past the duplicate
        last[ch] = right
        ans = max(ans, right - left + 1)
    return ans
```
Complexity: O(n) time, O(1) space (alphabet bounded).
Why `last[ch] >= left`: keep stale entries from earlier windows harmless.

### Subarray sum equals k (LeetCode 560)
```python
def subarray_sum(nums, k):
    pref = {0: 1}                         # prefix sum -> count of occurrences
    total = ans = 0
    for x in nums:
        total += x
        ans += pref.get(total - k, 0)     # how many starts give sum k
        pref[total] = pref.get(total, 0) + 1
    return ans
```
Complexity: O(n) time, O(n) space.
Key idea: `pref[j] - pref[i] = k` so we look for `pref[i] = pref[j] - k`. The `{0: 1}` sentinel handles the whole-array case.
Modify: count subarrays divisible by k → `pref[total % k]`; longest subarray with sum k → store `first index` per prefix instead of count; 2D version (matrix sum = k) → collapse rows to prefix sums.

## Subarray patterns quick map

| Problem | Pattern | Complexity |
|---|---|---|
| Max subarray sum | Kadane (track cur, best) | O(n), O(1) |
| Fixed window k | Sliding window, add-right/drop-left | O(n), O(1) |
| Longest valid window | Variable window, while-shrink | O(n), O(1–k) |
| Sliding window max | Monotonic deque | O(n), O(k) |
| # subarrays with sum k | Prefix sum dict | O(n), O(n) |
| # subarrays divisible by k | Prefix sum mod dict | O(n), O(n) |
| Max subarray product | Kadane w/ min+max tracking | O(n), O(1) |
| Container with most water | Two pointers from both ends | O(n), O(1) |
