# Infosys SP DSE - Previous Year Questions (Medium Level)

> 15 frequently asked medium-level questions from Infosys coding rounds.

## Quick Reference: All Medium Problems

```
┌────┬──────────────────────────────┬──────────┬───────────┬──────────────────┐
│  # │ Problem                      │ Time     │ Space     │ Pattern          │
├────┼──────────────────────────────┼──────────┼───────────┼──────────────────┤
│  1 │ GET Function (Max Pairs)     │ O(n)     │ O(n)      │ Monotonic Stack  │
│  2 │ Inversion Pairs Deletion     │ O(n^2)   │ O(n)      │ Prefix/Suffix    │
│  3 │ Max Product Subarray         │ O(n)     │ O(1)      │ DP               │
│  4 │ Group Anagrams               │ O(nk lgk)│ O(nk)     │ Hash + Sort      │
│  5 │ Longest Unique Substring     │ O(n)     │ O(n)      │ Sliding Window   │
│  6 │ Subarray Sum Equals K        │ O(n)     │ O(n)      │ Prefix Sum       │
│  7 │ Product Except Self          │ O(n)     │ O(1)      │ Prefix/Suffix    │
│  8 │ Sort Colors (Dutch Flag)     │ O(n)     │ O(1)      │ Three Pointers   │
│  9 │ Container Most Water         │ O(n)     │ O(1)      │ Two Pointers     │
│ 10 │ 3Sum                         │ O(n^2)   │ O(1)      │ Two Pointers     │
│ 11 │ Coin Change (Min)            │ O(n*C)   │ O(n)      │ 1D DP            │
│ 12 │ LIS                          │ O(n lgn) │ O(n)      │ DP + BS          │
│ 13 │ Word Break                   │ O(n^2)   │ O(n)      │ 1D DP            │
│ 14 │ Kth Largest                  │ O(n lgk) │ O(k)      │ Min-Heap         │
│ 15 │ Merge Intervals              │ O(n lgn) │ O(n)      │ Sort + Merge     │
└────┴──────────────────────────────┴──────────┴───────────┴──────────────────┘

EXAM STRATEGY: 15-20 minutes each, focus on explaining approach first!
```

---

## 1. GET Function on Array (Max Value Pairs Problem)

**Problem Statement:** Given an array, you can perform operations: GET(i, j) returns max(arr[i..j]). Find the number of pairs (i, j) where GET(i, j) == arr[i] + arr[j] - arr[i]*arr[j] or similar condition based on the given operation. (Infosys variant: count pairs where max of subarray equals some function of endpoints)

**Approach:** For each element, find the range where it is the maximum using stack-based technique. Then count valid pairs within that range.

```python
def count_valid_pairs(arr):
    n = len(arr)
    count = 0
    stack = []
    left = [0] * n
    right = [0] * n

    # Find left boundary
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        left[i] = stack[-1] + 1 if stack else 0
        stack.append(i)

    stack.clear()
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        right[i] = stack[-1] - 1 if stack else n - 1
        stack.append(i)

    for i in range(n):
        range_size = right[i] - left[i] + 1
        count += range_size * (range_size - 1) // 2

    return count

arr = [1, 3, 2]
print(count_valid_pairs(arr))
```

**Complexity:** O(n) time, O(n) space

**Tips:** Stack-based range problems are common in Infosys. Practice monotonic stack patterns.

---

## 2. Inversion Pairs After Subarray Deletion

**Problem Statement:** Given an array, remove exactly one subarray to minimize the number of inversion pairs. Find the minimum inversions possible.

**Approach:** Count total inversions. For each possible subarray deletion, calculate reduction in inversions efficiently.

```python
def min_inversions_after_deletion(arr):
    n = len(arr)
    total_inversions = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                total_inversions += 1

    min_remaining = total_inversions
    for start in range(n):
        inversions_removed = 0
        for end in range(start, n):
            for i in range(start):
                for j in range(start, end + 1):
                    if arr[i] > arr[j]:
                        inversions_removed += 1
            for i in range(start, end + 1):
                for j in range(end + 1, n):
                    if arr[i] > arr[j]:
                        inversions_removed += 1
            remaining = total_inversions - inversions_removed
            min_remaining = min(min_remaining, remaining)

    return min_remaining

arr = [5, 3, 1, 4]
print(min_inversions_after_deletion(arr))
```

**Complexity:** O(n^3) naive, O(n^2) optimized with prefix/suffix arrays

**Tips:** Infosys SP L3 may ask optimization variants. Precompute prefix and suffix inversion counts.

---

## 3. Maximum Product Subarray

**Problem Statement:** Find contiguous subarray with maximum product.

**Approach:** Track both max and min products at each step (negative numbers can become max when multiplied by negative).

```python
def max_product_subarray(arr):
    result = arr[0]
    max_prod = arr[0]
    min_prod = arr[0]

    for i in range(1, len(arr)):
        if arr[i] < 0:
            max_prod, min_prod = min_prod, max_prod

        max_prod = max(arr[i], max_prod * arr[i])
        min_prod = min(arr[i], min_prod * arr[i])
        result = max(result, max_prod)

    return result

arr = [2, 3, -2, 4]
print(max_product_subarray(arr))  # Output: 6
```

**Complexity:** O(n) time, O(1) space

**Tips:** Key insight: negative * negative = positive. Always track min alongside max.

---

## 4. Group Anagrams

**Problem Statement:** Group strings that are anagrams of each other.

**Approach:** Sort each string as key in dictionary.

```python
from collections import defaultdict

def group_anagrams(strs):
    anagram_map = defaultdict(list)

    for s in strs:
        key = ''.join(sorted(s))
        anagram_map[key].append(s)

    return list(anagram_map.values())

strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams(strs))
# Output: [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

**Complexity:** O(n * k log k) time, O(n * k) space, where k = max string length

**Tips:** Alternative key: character count tuple for O(k) per string.

```python
def group_anagrams_optimized(strs):
    anagram_map = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        anagram_map[key].append(s)
    return list(anagram_map.values())
```

---

## 5. Longest Substring Without Repeating Characters

**Problem Statement:** Find length of longest substring without repeating characters.

### Visual: Sliding Window with Hash Map

```
s = "abcabcbb"

WINDOW EXPANSION AND SHRINKING:
  ┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
  │ a │ b │ c │ a │ b │ c │ b │ b │   │
  └───┴───┴───┴───┴───┴───┴───┴───┴───┘
  
  Step 1: Expand right until duplicate
  [a b c] a b c b b    max_len=3
   L     R
   chars={a:0, b:1, c:2}
   
  Step 2: 'a' duplicate at index 3
  a [b c a] b c b b    max_len=3
     L   R
     chars={b:1, c:2, a:3}
     
  Step 3: 'b' duplicate at index 4
  a b [c a b] c b b    max_len=3
       L   R
       chars={c:2, a:3, b:4}
       
  Step 4: 'c' duplicate at index 5
  a b c [a b c] b b    max_len=3
         L   R
         chars={a:3, b:4, c:5}
         
  Step 5: 'b' duplicate at index 6
  a b c a [b c b] b    max_len=3
           L R
           chars shrink...
           
  Continue until end → max_len = 3 ✅

ALGORITHM:
  For each char at position 'right':
    If char was seen before AND its index >= left:
      Move left to (last_seen_index + 1)
    Update last_seen_index for char
    max_len = max(max_len, right - left + 1)
```

---

```python
def longest_unique_substring(s):
    char_index = {}
    max_length = 0
    start = 0

    for end in range(len(s)):
        if s[end] in char_index and char_index[s[end]] >= start:
            start = char_index[s[end]] + 1
        char_index[s[end]] = end
        max_length = max(max_length, end - start + 1)

    return max_length

s = "abcabcbb"
print(longest_unique_substring(s))  # Output: 3
```

**Complexity:** O(n) time, O(min(n, m)) space, where m = charset size

**Tips:** Very frequently asked. Practice with: longest with at most k duplicates.

---

## 6. Subarray Sum Equals K

**Problem Statement:** Find number of subarrays whose sum equals k.

**Approach:** Prefix sum with hash map. If prefix_sum - k exists in map, that subarray sums to k.

```python
def subarray_sum_k(arr, k):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}

    for num in arr:
        prefix_sum += num
        if prefix_sum - k in sum_count:
            count += sum_count[prefix_sum - k]
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1

    return count

arr = [1, 1, 1]
k = 2
print(subarray_sum_k(arr, k))  # Output: 2
```

**Complexity:** O(n) time, O(n) space

**Tips:** Works with negative numbers too. This is a very popular Infosys question.

---

## 7. Product of Array Except Self

**Problem Statement:** Return array where each element is product of all other elements, without using division.

### Visual: Prefix and Suffix Products

```
arr = [1, 2, 3, 4]

STEP 1: Left products (product of all elements to the left)
  result[0] = 1       (nothing to left)
  result[1] = 1       (= arr[0])
  result[2] = 1*2 = 2 (= arr[0]*arr[1])
  result[3] = 1*2*3=6 (= arr[0]*arr[1]*arr[2])
  
  result after left pass: [1, 1, 2, 6]

STEP 2: Right products (multiply by product of all to the right)
  result[3] *= 1      (nothing to right)  → [1, 1, 2, 6]
  result[2] *= 4      (= arr[3])          → [1, 1, 8, 6]
  result[1] *= 4*3=12 (= arr[3]*arr[2])  → [1, 12, 8, 6]
  result[0] *= 4*3*2=24                    → [24, 12, 8, 6]

VISUAL TABLE:
┌─────────┬───────┬───────┬───────┬───────┐
│         │  i=0  │  i=1  │  i=2  │  i=3  │
├─────────┼───────┼───────┼───────┼───────┤
│ arr     │   1   │   2   │   3   │   4   │
│ left[]  │   1   │   1   │   2   │   6   │
│ right[] │  24   │  12   │   4   │   1   │
│ result  │  24   │  12   │   8   │   6   │
└─────────┴───────┴───────┴───────┴───────┘
           ↑       ↑       ↑       ↑
         2*3*4   1*3*4   1*2*4   1*2*3

WHY NO DIVISION?
  If we used division: result = total_product / arr[i]
  BUT: fails with zeros! (division by zero)
  Also: violates interview constraint
```

---

```python
def product_except_self(arr):
    n = len(arr)
    result = [1] * n

    # Left pass
    left = 1
    for i in range(n):
        result[i] = left
        left *= arr[i]

    # Right pass
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= arr[i]

    return result

arr = [1, 2, 3, 4]
print(product_except_self(arr))  # Output: [24, 12, 8, 6]
```

**Complexity:** O(n) time, O(1) space (excluding output)

**Tips:** Do not use division. Interviewers specifically check for this.

---

## 8. Sort Colors (Dutch National Flag)

**Problem Statement:** Sort array of 0s, 1s, and 2s in single pass.

### Visual: Three Pointer Movement

```
arr = [2, 0, 2, 1, 1, 0]

Three regions:
  [0..low-1]   = all 0s (red)
  [low..mid-1] = all 1s (white)
  [mid..high]  = unprocessed
  [high+1..n-1]= all 2s (blue)

INITIAL STATE:
  low=0, mid=0, high=5
  [2, 0, 2, 1, 1, 0]
   L  M           H

STEP 1: arr[mid]=2 → swap with high, high--
  [0, 0, 2, 1, 1, 2]
   L  M        H
  
STEP 2: arr[mid]=0 → swap with low, low++, mid++
  [0, 0, 2, 1, 1, 2]
      L  M     H
  (now arr[0]=0 ✅)

STEP 3: arr[mid]=0 → swap with low, low++, mid++
  [0, 0, 2, 1, 1, 2]
         L  M  H
  (now arr[1]=0 ✅)

STEP 4: arr[mid]=2 → swap with high, high--
  [0, 0, 1, 1, 2, 2]
         L  M  H
  (now arr[5]=2 ✅)

STEP 5: arr[mid]=1 → just mid++
  [0, 0, 1, 1, 2, 2]
         L     MH
  (now arr[2]=1 ✅)

STEP 6: arr[mid]=1 → just mid++
  [0, 0, 1, 1, 2, 2]
         L     MH
  (mid > high → STOP!)

FINAL: [0, 0, 1, 1, 2, 2] ✅

DECISION RULE:
  arr[mid] == 0: swap with low, advance both
  arr[mid] == 1: just advance mid
  arr[mid] == 2: swap with high, advance high only
```

---

```python
def sort_colors(arr):
    low, mid, high = 0, 0, len(arr) - 1

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1

    return arr

arr = [2, 0, 2, 1, 1, 0]
print(sort_colors(arr))  # Output: [0, 0, 1, 1, 2, 2]
```

**Complexity:** O(n) time, O(1) space

**Tips:** One-pass, constant space is the constraint. Practice explaining pointer movements.

---

## 9. Container with Most Water

**Problem Statement:** Given heights array, find two lines that together with x-axis form container holding most water.

### Visual: Two Pointer Greedy Approach

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

Visual representation:
  8 │█            █        █
  7 │█            █        █  █
  6 │█   █        █        █  █
  5 │█   █     █  █        █  █
  4 │█   █     █  █  █     █  █
  3 │█   █     █  █  █     █  █
  2 │█   █  █  █  █  █     █  █
  1 │█   █  █  █  █  █  █  █  █
    └──────────────────────────────
     0   1  2  3  4  5  6  7  8

TWO POINTER APPROACH:
  L=0, R=8: area = min(1,7)*8 = 8
  L=0, R=7: area = min(1,3)*7 = 3 (smaller, skip)
  
  Actually:
  L=0, R=8: area = min(1,7)*8 = 8  → move L (1<7)
  L=1, R=8: area = min(8,7)*7 = 49 → move R (7<8) ← MAX!
  L=1, R=7: area = min(8,3)*6 = 18 → move R (3<8)
  L=1, R=6: area = min(8,8)*5 = 40 → move R (equal, move either)
  L=1, R=5: area = min(8,4)*4 = 16 → move R (4<8)
  L=1, R=4: area = min(8,5)*3 = 15 → move R (5<8)
  L=1, R=3: area = min(8,2)*2 = 4  → move R (2<8)
  L=1, R=2: area = min(8,6)*1 = 6  → move R (6<8)
  L=1, R=1: STOP (L==R)

  Answer = 49 ✅

WHY MOVE THE SHORTER POINTER?
  Moving the taller pointer NEVER increases area:
  area = min(h[L], h[R]) * width
  If we move taller, min stays same but width decreases!
  Moving shorter gives chance to find taller → bigger min
```

---

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)

        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water

height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print(max_area(height))  # Output: 49
```

**Complexity:** O(n) time, O(1) space

**Tips:** Greedy approach works because moving the taller pointer never increases area.

---

## 10. 3Sum

**Problem Statement:** Find all unique triplets that sum to zero.

**Approach:** Sort array, fix one element, use two pointers for remaining two.

```python
def three_sum(arr):
    arr.sort()
    result = []
    n = len(arr)

    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            total = arr[i] + arr[left] + arr[right]
            if total == 0:
                result.append([arr[i], arr[left], arr[right]])
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result

arr = [-1, 0, 1, 2, -1, -4]
print(three_sum(arr))  # Output: [[-1, -1, 2], [-1, 0, 1]]
```

**Complexity:** O(n^2) time, O(1) space

**Tips:** Skip duplicates carefully. Infosys asks this frequently.

---

## 11. Coin Change (Minimum Coins)

**Problem Statement:** Find minimum number of coins to make given amount.

**Approach:** Bottom-up DP. dp[i] = min coins for amount i.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

coins = [1, 5, 10, 25]
amount = 30
print(coin_change(coins, amount))  # Output: 2
```

**Complexity:** O(amount * coins) time, O(amount) space

**Tips:** Classic DP. Practice both: minimum coins AND number of ways.

---

## 12. Longest Increasing Subsequence

**Problem Statement:** Find length of longest strictly increasing subsequence.

**Approach:** DP with binary search optimization.

```python
import bisect

def lis_dp(arr):
    n = len(arr)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

# O(n log n) with binary search
def lis_binary_search(arr):
    tails = []
    for num in arr:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

arr = [10, 9, 2, 5, 3, 7, 101, 18]
print(lis_dp(arr))            # Output: 4
print(lis_binary_search(arr)) # Output: 4
```

**Complexity:** O(n^2) DP, O(n log n) binary search; O(n) space

**Tips:** Infosys may ask to print the actual subsequence, not just length.

---

## 13. Word Break

**Problem Statement:** Check if string can be segmented into dictionary words.

**Approach:** DP. dp[i] = True if s[0:i] can be segmented.

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]

s = "leetcode"
word_dict = ["leet", "code"]
print(word_break(s, word_dict))  # Output: True
```

**Complexity:** O(n^2 * k) time with k = average word length, O(n) space

**Tips:** Also practice Word Break II (return all valid sentences).

---

## 14. Kth Largest Element

**Problem Statement:** Find kth largest element in unsorted array.

**Approach:** Min-heap of size k or Quickselect.

```python
import heapq

def kth_largest_heap(arr, k):
    min_heap = arr[:k]
    heapq.heapify(min_heap)

    for num in arr[k:]:
        if num > min_heap[0]:
            heapq.heapreplace(min_heap, num)

    return min_heap[0]

# Quickselect approach
def kth_largest_quickselect(arr, k):
    def quickselect(arr, left, right, k_smallest):
        if left == right:
            return arr[left]

        pivot_idx = left
        arr[pivot_idx], arr[right] = arr[right], arr[pivot_idx]
        store_idx = left

        for i in range(left, right):
            if arr[i] < arr[right]:
                arr[store_idx], arr[i] = arr[i], arr[store_idx]
                store_idx += 1

        arr[store_idx], arr[right] = arr[right], arr[store_idx]

        if k_smallest == store_idx:
            return arr[store_idx]
        elif k_smallest < store_idx:
            return quickselect(arr, left, store_idx - 1, k_smallest)
        else:
            return quickselect(arr, store_idx + 1, right, k_smallest)

    return quickselect(arr, 0, len(arr) - 1, len(arr) - k)

arr = [3, 2, 1, 5, 6, 4]
k = 2
print(kth_largest_heap(arr, k))          # Output: 5
print(kth_largest_quickselect(arr[:], k)) # Output: 5
```

**Complexity:** O(n log k) heap, O(n) average quickselect, O(1) space (quickselect)

**Tips:** Quickselect is O(n^2) worst case. Heap is safer for interviews.

---

## 15. Merge Intervals

**Problem Statement:** Merge all overlapping intervals.

**Approach:** Sort by start time, then merge overlapping.

```python
def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged

intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
print(merge_intervals(intervals))  # Output: [[1, 6], [8, 10], [15, 18]]
```

**Complexity:** O(n log n) time, O(n) space

**Tips:** Also practice: insert interval, non-overlapping intervals.

---

## Summary Table

| # | Problem | Time | Space | Difficulty |
|---|---------|------|-------|------------|
| 1 | GET Function (Max Pairs) | O(n) | O(n) | Medium |
| 2 | Inversion Pairs Deletion | O(n^2) | O(n) | Medium |
| 3 | Max Product Subarray | O(n) | O(1) | Medium |
| 4 | Group Anagrams | O(nk log k) | O(nk) | Medium |
| 5 | Longest Unique Substring | O(n) | O(n) | Medium |
| 6 | Subarray Sum Equals K | O(n) | O(n) | Medium |
| 7 | Product Except Self | O(n) | O(1) | Medium |
| 8 | Sort Colors | O(n) | O(1) | Medium |
| 9 | Container Most Water | O(n) | O(1) | Medium |
| 10 | 3Sum | O(n^2) | O(1) | Medium |
| 11 | Coin Change | O(n*coins) | O(n) | Medium |
| 12 | LIS | O(n log n) | O(n) | Medium |
| 13 | Word Break | O(n^2) | O(n) | Medium |
| 14 | Kth Largest | O(n log k) | O(k) | Medium |
| 15 | Merge Intervals | O(n log n) | O(n) | Medium |

> **Pro Tip:** Medium questions should take 15-20 minutes each in Infosys SP L3. Focus on explaining approach before coding.
