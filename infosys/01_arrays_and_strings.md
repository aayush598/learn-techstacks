# Arrays & Strings

## Problem 1: Second Largest Element
**Difficulty: Easy | Marks: 20**

Find the second largest element in an array.

```python
def second_largest(arr):
    first = second = float('-inf')
    for num in arr:
        if num > first:
            second = first
            first = num
        elif first > num > second:
            second = num
    return second

arr = [10, 5, 8, 20, 3]
print(second_largest(arr))
```

---

## Problem 2: Kadane's Algorithm (Maximum Subarray Sum)
**Difficulty: Easy | Marks: 20**

Find the contiguous subarray with maximum sum.

```python
def max_subarray_sum(arr):
    max_ending_here = max_so_far = arr[0]
    for num in arr[1:]:
        max_ending_here = max(num, max_ending_here + num)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_sum(arr))
```

---

## Problem 3: Sliding Window - Maximum Sum Subarray of Size K
**Difficulty: Easy-Medium | Marks: 20**

```python
def max_sum_subarray_k(arr, k):
    n = len(arr)
    if n < k:
        return -1
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(n - k):
        window_sum = window_sum - arr[i] + arr[i + k]
        max_sum = max(max_sum, window_sum)
    return max_sum

arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
k = 4
print(max_sum_subarray_k(arr, k))
```

---

## Problem 4: Sliding Window - Longest Substring Without Repeating Characters
**Difficulty: Medium | Marks: 30**

```python
def longest_unique_substring(s):
    char_set = set()
    left = max_len = 0
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
    return max_len

s = "abcabcbb"
print(longest_unique_substring(s))
```

---

## Problem 5: Two Sum
**Difficulty: Easy | Marks: 20**

```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))
```

---

## Problem 6: Three Sum
**Difficulty: Medium | Marks: 30**

```python
def three_sum(nums):
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return result

nums = [-1, 0, 1, 2, -1, -4]
print(three_sum(nums))
```

---

## Problem 7: Container With Most Water
**Difficulty: Medium | Marks: 30**

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        h = min(height[left], height[right])
        w = right - left
        max_water = max(max_water, h * w)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water

height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print(max_area(height))
```

---

## Problem 8: Trapping Rain Water
**Difficulty: Hard | Marks: 50**

```python
def trap_rain_water(height):
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    return water

height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(trap_rain_water(height))
```

---

## Problem 9: Rotate Array
**Difficulty: Easy | Marks: 20**

```python
def rotate(arr, k):
    n = len(arr)
    k = k % n
    arr.reverse()
    arr[:k] = reversed(arr[:k])
    arr[k:] = reversed(arr[k:])
    return arr

arr = [1, 2, 3, 4, 5, 6, 7]
k = 3
print(rotate(arr, k))
```

---

## Problem 10: Longest Palindromic Substring
**Difficulty: Medium | Marks: 30**

```python
def longest_palindrome(s):
    n = len(s)
    if n < 2:
        return s
    start = max_len = 0
    def expand(l, r):
        nonlocal start, max_len
        while l >= 0 and r < n and s[l] == s[r]:
            l -= 1
            r += 1
        if r - l - 1 > max_len:
            max_len = r - l - 1
            start = l + 1
    for i in range(n):
        expand(i, i)
        expand(i, i + 1)
    return s[start:start + max_len]

s = "babad"
print(longest_palindrome(s))
```

---

## Problem 11: Minimum Swaps to Group Odd/Even (Summer Array)
**Difficulty: Easy-Medium | Marks: 20**

Asked in Infosys SP/DSE exam.

```python
def min_swaps_to_summer_array(arr):
    n = len(arr)
    swaps = 0
    # Bring all odds to left
    odd_pos = 0
    for i in range(n):
        if arr[i] % 2 == 1:
            arr[i], arr[odd_pos] = arr[odd_pos], arr[i]
            swaps += i - odd_pos
            odd_pos += 1
    return swaps

# Alternative: count inversions of even-odd pairs
def min_swaps_alternative(arr):
    n = len(arr)
    odds = [i for i in range(n) if arr[i] % 2 == 1]
    swaps = 0
    for i, pos in enumerate(odds):
        swaps += pos - i
    return swaps

arr = [1, 2, 3, 4, 5, 6]
print(min_swaps_alternative(arr))
```

---

## Problem 12: Minimize Ugliness of Binary String
**Difficulty: Medium-Hard | Marks: 50**

Asked in Infosys SP/DSE exam - swap and flip to minimize binary value.

```python
MOD = 10**9 + 7

def minimize_ugliness(N, S, cash, A, B):
    s = list(S)
    n = len(s)

    if A < B:
        # swap cheaper - bring 0s to front
        i = 0
        for j in range(n - 1, -1, -1):
            if cash < A:
                break
            if s[j] == '0':
                while i < n and s[i] == '0':
                    i += 1
                if i < j:
                    s[i], s[j] = s[j], s[i]
                    cash -= A
                    i += 1

        # flip remaining 1s to 0
        for i in range(n):
            if cash < B:
                break
            if s[i] == '1':
                s[i] = '0'
                cash -= B
    else:
        # flip cheaper - flip 1s to 0 starting from MSB
        for i in range(n):
            if cash < B:
                break
            if s[i] == '1':
                s[i] = '0'
                cash -= B

        # swap to bring remaining 0s to front
        i = 0
        for j in range(n - 1, -1, -1):
            if cash < A:
                break
            if s[j] == '0':
                while i < n and s[i] == '0':
                    i += 1
                if i < j:
                    s[i], s[j] = s[j], s[i]
                    cash -= A
                    i += 1

    return int(''.join(s), 2) % MOD

print(minimize_ugliness(4, "1111", 7, 1, 2))
```

---

## Problem 13: Maximum Sum Subarray with K Swaps
**Difficulty: Medium-Hard | Marks: 50**

Asked in Infosys SP exam.

```python
import heapq

def max_sum_with_k_swaps(arr, k):
    n = len(arr)
    # For each position, track max element we can bring here using at most k swaps
    for i in range(n):
        max_val = arr[i]
        max_pos = i
        for j in range(i + 1, min(n, i + k + 1)):
            if arr[j] > max_val:
                max_val = arr[j]
                max_pos = j
        if max_pos != i:
            # Rotate to bring max to position i
            k -= (max_pos - i)
            arr[i+1:max_pos+1] = arr[i:max_pos]
            arr[i] = max_val
    return sum(arr)

arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
k = 3
print(max_sum_with_k_swaps(arr, k))
```

---

## Problem 14: Product of Array Except Self
**Difficulty: Medium | Marks: 30**

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    left = 1
    for i in range(n):
        result[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right
        right *= nums[i]
    return result

nums = [1, 2, 3, 4]
print(product_except_self(nums))
```

---

## Problem 15: First Missing Positive
**Difficulty: Hard | Marks: 50**

```python
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            nums[nums[i] - 1], nums[i] = nums[i], nums[nums[i] - 1]
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1

nums = [3, 4, -1, 1]
print(first_missing_positive(nums))
```

---

## Problem 16: Merge Intervals
**Difficulty: Medium | Marks: 30**

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
print(merge_intervals(intervals))
```

---

## Problem 17: Next Permutation
**Difficulty: Medium | Marks: 30**

```python
def next_permutation(nums):
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1:] = reversed(nums[i + 1:])
    return nums

nums = [1, 2, 3]
print(next_permutation(nums))
```

---

## Problem 18: Group Anagrams
**Difficulty: Medium | Marks: 30**

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams(strs))
```

---

## Problem 19: Minimum Window Substring
**Difficulty: Hard | Marks: 50**

```python
from collections import Counter

def min_window(s, t):
    if not s or not t:
        return ""
    need = Counter(t)
    have = {}
    left = 0
    matched = 0
    min_len = float('inf')
    min_start = 0
    for right in range(len(s)):
        char = s[right]
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            matched += 1
        while matched == len(need):
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_start = left
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                matched -= 1
            left += 1
    return "" if min_len == float('inf') else s[min_start:min_start + min_len]

s = "ADOBECODEBANC"
t = "ABC"
print(min_window(s, t))
```

---

## Problem 20: Longest Consecutive Sequence
**Difficulty: Medium | Marks: 30**

```python
def longest_consecutive(nums):
    num_set = set(nums)
    longest = 0
    for num in num_set:
        if num - 1 not in num_set:
            curr = num
            length = 1
            while curr + 1 in num_set:
                curr += 1
                length += 1
            longest = max(longest, length)
    return longest

nums = [100, 4, 200, 1, 3, 2]
print(longest_consecutive(nums))
```

---

## Problem 21: Find All Duplicates in Array
**Difficulty: Medium | Marks: 30**

```python
def find_duplicates(nums):
    result = []
    for num in nums:
        idx = abs(num) - 1
        if nums[idx] < 0:
            result.append(abs(num))
        else:
            nums[idx] *= -1
    return result

nums = [4, 3, 2, 7, 8, 2, 3, 1]
print(find_duplicates(nums))
```

---

## Problem 22: Find Character Frequencies
**Difficulty: Easy | Marks: 20**

Asked in Infosys SP interview.

```python
def char_frequencies(s):
    freq = {}
    for ch in s:
        freq[ch] = freq.get(ch, 0) + 1
    return freq

s = "aaabbbcc"
result = char_frequencies(s)
for ch, count in result.items():
    print(f"{ch}={count}")
```
