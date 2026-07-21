# Sorting, Hashing & Heaps — Complete Problem Bank (40 Problems)

> **Infosys SP DSE Preparation** | All solutions in Python
> Sorting (12) + Hashing (15) + Heaps (13) = **40 Problems**

---

# PART A: SORTING PROBLEMS (12)

---

## Problem 1: Sort an Array (Merge Sort) [EASY]

**Problem:** Given an array of integers `nums`, sort the array in ascending order and return it. You must solve it without using any built-in sort functions. Target O(n log n) time.

**Approach:**
Merge sort is a divide-and-conquer algorithm:
1. **Divide** the array into two halves until each subarray has 0 or 1 elements.
2. **Conquer** by recursively sorting each half.
3. **Combine** by merging two sorted halves using a two-pointer technique.
The key insight is that merging two sorted arrays takes linear time. Since we divide log(n) times, total is O(n log n).

```python
def sortArray(nums):
    def merge_sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        return merge(left, right)

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    return merge_sort(nums)

# Test cases
print(sortArray([5, 2, 3, 1]))       # [1, 2, 3, 5]
print(sortArray([5, 1, 1, 2, 0, 0])) # [0, 0, 1, 1, 2, 5]
print(sortArray([]))                  # []
print(sortArray([1]))                 # [1]
```

**Complexity:** O(n log n) time, O(n) space (due to auxiliary arrays)
**Trick/Tip:** Use `<=` (not `<`) in merge to maintain stability — equal elements preserve their original relative order.

---

## Problem 2: Sort Colors (Dutch National Flag) [EASY]

**Problem:** Given an array `nums` with n objects colored red (0), white (1), or blue (2), sort them in-place so objects of the same color are adjacent in the same order: red, white, blue. You must solve it without using the library's sort function. Use one pass with O(1) extra space.

**Approach:**
The Dutch National Flag algorithm by Dijkstra uses three pointers:
- `low` — boundary for 0s (everything before `low` is 0)
- `mid` — current element being examined
- `high` — boundary for 2s (everything after `high` is 2)

When `nums[mid] == 0`: swap with `low`, advance both `low` and `mid`
When `nums[mid] == 1`: just advance `mid`
When `nums[mid] == 2`: swap with `high`, decrement `high` only (swapped element needs examination)

```python
def sortColors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums

# Test cases
print(sortColors([2, 0, 2, 1, 1, 0]))  # [0, 0, 1, 1, 2, 2]
print(sortColors([2, 0, 1]))            # [0, 1, 2]
print(sortColors([0]))                  # [0]
print(sortColors([1, 1, 0, 2]))         # [0, 1, 1, 2]
```

**Complexity:** O(n) time, O(1) space — single pass
**Trick/Tip:** When swapping with `high`, don't increment `mid` because the element brought from `high` hasn't been examined yet. When swapping with `low`, both can advance because the element from `low` was already processed (it's a 0).

---

## Problem 3: Merge Sorted Array [EASY]

**Problem:** Given two sorted integer arrays `nums1` (size m+n, last n elements are 0) and `nums2` (size n), merge `nums2` into `nums1` in-place, sorted in non-decreasing order.

**Approach:**
Fill from the back to avoid overwriting elements in `nums1` that haven't been processed yet:
1. Three pointers: `p1` at end of valid `nums1` (m-1), `p2` at end of `nums2` (n-1), `write` at end of `nums1` (m+n-1).
2. Compare `nums1[p1]` and `nums2[p2]`, place the larger at `write`, decrement the respective pointer.
3. If `p1` goes below 0, copy remaining `nums2` elements.

```python
def merge(nums1, m, nums2, n):
    p1, p2, write = m - 1, n - 1, m + n - 1
    while p2 >= 0:
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[write] = nums1[p1]
            p1 -= 1
        else:
            nums1[write] = nums2[p2]
            p2 -= 1
        write -= 1
    return nums1

# Test cases
print(merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3))  # [1, 2, 2, 3, 5, 6]
print(merge([1], 1, [], 0))                           # [1]
print(merge([0], 0, [1], 1))                          # [1]
print(merge([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3))   # [1, 2, 3, 4, 5, 6]
```

**Complexity:** O(m+n) time, O(1) space
**Trick/Tip:** Only the `while p2 >= 0` condition is needed — if `p1` runs out, remaining `nums2` elements are already in correct position since we're filling backwards.

---

## Problem 4: Kth Largest Element in a Stream [EASY]

**Problem:** Design a class to find the kth largest element in a stream. Implement `KthLargest(k, nums)` constructor and `add(val)` method that returns the kth largest element after adding `val`.

**Approach:**
Maintain a min-heap of size k. The heap stores the k largest elements seen so far. The root (smallest in the heap) is always the kth largest overall. When a new value arrives:
1. Push it to the heap.
2. If heap size exceeds k, pop the smallest (root).
3. Return root as the kth largest.

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]

# Test cases
obj = KthLargest(3, [4, 5, 8, 2])
print(obj.add(3))   # 4
print(obj.add(5))   # 5
print(obj.add(10))  # 5
print(obj.add(9))   # 8
print(obj.add(4))   # 8
```

**Complexity:** Constructor O(n log k), Add O(log k)
**Trick/Tip:** Min-heap of size k gives kth largest at root. A max-heap would give 1st largest (the maximum). Think: "keep only the top k, discard the rest."

---

## Problem 5: Kth Largest Element in an Array (Quickselect) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return the kth largest element (not the kth distinct). Must run in O(n) average time.

**Approach:**
Quickselect is based on the partition step of quicksort:
1. Pick a random pivot and partition: elements > pivot go left, == pivot in middle, < pivot go right.
2. If the pivot is at position k-1 (0-indexed), return it.
3. If pivot index < k-1, recurse right; else recurse left.

Random pivot ensures O(n) average time. We partition in descending order to find kth largest directly.

```python
import random

def findKthLargest(nums, k):
    def quickselect(left, right, k_smallest):
        if left == right:
            return nums[left]
        pivot_idx = random.randint(left, right)
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]
        store = left
        for i in range(left, right):
            if nums[i] > pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1
        nums[store], nums[right] = nums[right], nums[store]
        if store == k_smallest:
            return nums[store]
        elif store < k_smallest:
            return quickselect(store + 1, right, k_smallest)
        else:
            return quickselect(left, store - 1, k_smallest)

    return quickselect(0, len(nums) - 1, k - 1)

# Test cases
print(findKthLargest([3, 2, 1, 5, 6, 4], 2))  # 5
print(findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # 4
print(findKthLargest([1], 1))  # 1
print(findKthLargest([7, 7, 7, 7], 2))  # 7
```

**Complexity:** O(n) average, O(n²) worst case
**Trick/Tip:** Random pivot makes worst case extremely unlikely. For guaranteed O(n), use median-of-medians (but rarely needed in interviews).

---

## Problem 6: Sort Integers by Number of 1 Bits [MEDIUM]

**Problem:** Given an integer array `arr`, sort the integers by the number of 1 bits in binary representation. If two numbers have the same count, sort them in ascending order. Return the sorted array.

**Approach:**
Use Python's sort with a custom key. The key is a tuple `(bit_count, value)` — Python sorts tuples element by element, so it first sorts by bit count, then by value for ties.

```python
def sortByBits(arr):
    return sorted(arr, key=lambda x: (x.bit_count(), x))

# Alternative for older Python:
def sortByBits(arr):
    return sorted(arr, key=lambda x: (bin(x).count('1'), x))

# Test cases
print(sortByBits([0, 1, 2, 3, 4, 5, 6, 7, 8]))  # [0, 1, 2, 4, 8, 3, 5, 6, 7]
print(sortByBits([1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]))  # [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
print(sortByBits([3]))  # [3]
print(sortByBits([10, 5, 3, 8]))  # [8, 5, 10, 3]
```

**Complexity:** O(n log n) time, O(n) space (for the sort)
**Trick/Tip:** Python 3.10+ has `int.bit_count()`. For O(n) time, use bucket sort — create n+1 buckets indexed by bit count.

---

## Problem 7: Meeting Rooms II [MEDIUM]

**Problem:** Given an array of meeting time intervals `[[start, end]]` (start < end), find the minimum number of conference rooms required.

**Approach:**
1. Sort meetings by start time.
2. Use a min-heap to track end times of currently ongoing meetings.
3. For each meeting: if it starts after the earliest ending meeting (heap root), that room is freed — pop it.
4. Push current meeting's end time. Heap size = concurrent meetings.
5. The maximum heap size during the process = minimum rooms needed.

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])
    heap = []  # min-heap of end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)  # reuse room
        heapq.heappush(heap, end)
    return len(heap)

# Test cases
print(minMeetingRooms([[0, 30], [5, 10], [15, 20]]))  # 2
print(minMeetingRooms([[7, 10], [2, 4]]))              # 1
print(minMeetingRooms([[1, 5], [2, 3], [4, 6]]))      # 2
print(minMeetingRooms([]))                              # 0
print(minMeetingRooms([[1, 5], [5, 10]]))              # 1
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** The heap size at any point = number of concurrent meetings. We don't need to track the maximum explicitly — final heap size works because we process in sorted order. But for safety in unordered processing, track max heap size.

---

## Problem 8: Maximum Gap (Bucket Sort) [MEDIUM]

**Problem:** Given an integer array `nums`, return the maximum difference between successive elements in its sorted form. Your algorithm must run in O(n) time.

**Approach:**
Pigeonhole principle: with n numbers, if we create n+1 buckets, at least one bucket is empty. The max gap must be between buckets (not within a bucket).

Algorithm:
1. Find min and max of the array.
2. Create n+1 buckets, each covering range `(max-min)/n`.
3. For each number, place it in the appropriate bucket. Track only min and max per bucket.
4. The max gap = max of (current bucket min - previous bucket max) across non-empty buckets.

```python
def maximumGap(nums):
    if len(nums) < 2:
        return 0
    n = len(nums)
    min_val, max_val = min(nums), max(nums)
    if min_val == max_val:
        return 0

    bucket_size = max(1, (max_val - min_val) // n)
    bucket_count = (max_val - min_val) // bucket_size + 1
    bucket_min = [float('inf')] * bucket_count
    bucket_max = [float('-inf')] * bucket_count

    for num in nums:
        idx = (num - min_val) // bucket_size
        bucket_min[idx] = min(bucket_min[idx], num)
        bucket_max[idx] = max(bucket_max[idx], num)

    max_gap = 0
    prev_max = min_val
    for i in range(bucket_count):
        if bucket_min[i] == float('inf'):
            continue  # empty bucket
        max_gap = max(max_gap, bucket_min[i] - prev_max)
        prev_max = bucket_max[i]
    return max_gap

# Test cases
print(maximumGap([3, 6, 9, 1]))     # 3
print(maximumGap([10]))              # 0
print(maximumGap([1, 1, 1, 1]))     # 0
print(maximumGap([1, 10000000]))    # 9999999
print(maximumGap([1, 3, 6, 9, 12])) # 3
```

**Complexity:** O(n) time, O(n) space
**Trick/Tip:** The gap between elements within the same bucket is always ≤ bucket_size. So the answer must be a gap between consecutive non-empty buckets. This eliminates the need to sort.

---

## Problem 9: Custom Sort String [MEDIUM]

**Problem:** Given a string `order` (a permutation of unique lowercase letters) and a string `s`, sort `s` so that characters appear in the order defined by `order`. Characters not in `order` can be placed anywhere at the end. `order` and `s` consist of lowercase letters only.

**Approach:**
1. Count character frequencies in `s` using a hash map.
2. Iterate through `order`: for each character, append it `freq` times to result and remove from the map.
3. Append all remaining characters (those not in `order`) in any order.

```python
def customSortString(order, s):
    from collections import Counter
    count = Counter(s)
    result = []
    for ch in order:
        if ch in count:
            result.append(ch * count.pop(ch))
    # Append remaining characters not in order
    for ch, cnt in count.items():
        result.append(ch * cnt)
    return ''.join(result)

# Test cases
print(customSortString("cba", "abcd"))    # "cbad"
print(customSortString("cbafg", "abcd"))  # "cbad"
print(customSortString("bca", "aabbcc"))  # "bbbcca" or "ccabba" etc.
print(customSortString("z", "abc"))       # "abc"
print(customSortString("abc", "abc"))     # "abc"
```

**Complexity:** O(n + m) time where n=len(s), m=len(order), O(n) space
**Trick/Tip:** Using `count.pop(ch)` both retrieves the count and removes it, so remaining items in `count` are exactly those not in `order`. This avoids a second pass to filter.

---

## Problem 10: Count of Smaller Numbers After Self [HARD]

**Problem:** Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

**Approach:**
Modified merge sort preserves the inversion counting idea:
1. Pair each element with its original index: `[(value, original_index)]`.
2. During merge, when we pick an element from the right half before the left half element, all remaining elements in the left half are smaller than the current right element.
3. We track how many right elements have been placed (variable `j`) and add that count to the left element's result.

```python
def countSmaller(nums):
    def merge_sort(enum):
        mid = len(enum) // 2
        if mid > 0:
            left = merge_sort(enum[:mid])
            right = merge_sort(enum[mid:])
            merged = []
            i = j = 0
            while i < len(left) or j < len(right):
                if j == len(right) or (i < len(left) and left[i][1] <= right[j][1]):
                    # left[i] is smaller or equal, all j right elements already placed
                    # are smaller than left[i]'s value
                    smaller[left[i][0]] += j
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1
            return merged
        return enum

    smaller = [0] * len(nums)
    merge_sort(list(enumerate(nums)))
    return smaller

# Test cases
print(countSmaller([5, 2, 6, 1]))   # [2, 1, 1, 0]
print(countSmaller([-1]))            # [0]
print(countSmaller([-1, -1]))        # [0, 0]
print(countSmaller([1, 2, 3, 4]))   # [0, 0, 0, 0]
print(countSmaller([4, 3, 2, 1]))   # [3, 2, 1, 0]
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** Store original indices to map results back. The key insight: during merge, `j` represents how many right-side elements have been placed before the current left element, meaning those `j` elements are all ≤ left element and were to its right originally.

---

## Problem 11: Find Median from Data Stream [HARD]

**Problem:** Design a data structure that supports `addNum(num)` and `findMedian()`. `findMedian()` returns the median of all elements so far. Implement the `MedianFinder` class.

**Approach:**
Two-heap technique:
1. `max_heap` (stored as negated values) — holds the lower half of numbers.
2. `min_heap` — holds the upper half of numbers.
3. Invariant: `len(max_heap) >= len(min_heap)` and difference ≤ 1.
4. For addNum: push to max_heap, balance by moving max to min_heap, then rebalance sizes.
5. For findMedian: if sizes differ, median = max_heap root. Otherwise, average of both roots.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap (negate values)
        self.hi = []  # min-heap

    def addNum(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0

# Test cases
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2
mf.addNum(4)
print(mf.findMedian())  # 2.5
mf.addNum(5)
print(mf.findMedian())  # 3
```

**Complexity:** Add O(log n), Find Median O(1)
**Trick/Tip:** Python only has min-heap. Negate values to simulate max-heap. The push-to-lo-then-balance approach is cleaner than comparing values to decide which heap to push into.

---

## Problem 12: Minimum Cost to Make Array Equal [HARD]

**Problem:** Given an integer array `nums` and a positive integer array `cost` of the same length. You can increment or decrement any element by 1 at a cost of `cost[i]`. Return the minimum total cost to make all elements equal.

**Approach:**
The total cost as a function of the target value is convex (V-shaped). This means we can binary search on the target:
1. For a given target, compute `sum(cost[i] * |nums[i] - target|)`.
2. The derivative tells us which direction to search.
3. Binary search between min and max of nums to find the optimal target.

```python
def minCost(nums, cost):
    def total_cost(target):
        return sum(abs(n - target) * c for n, c in zip(nums, cost))

    lo, hi = min(nums), max(nums)
    ans = total_cost(lo)
    while lo <= hi:
        mid = (lo + hi) // 2
        c1 = total_cost(mid)
        c2 = total_cost(mid + 1)
        ans = min(ans, c1, c2)
        if c1 < c2:
            hi = mid - 1  # minimum is to the left
        else:
            lo = mid + 1  # minimum is to the right
    return ans

# Test cases
print(minCost([1, 3, 5, 2], [2, 3, 1, 14]))  # 8
print(minCost([2, 2, 2, 2, 2], [4, 2, 8, 1, 3]))  # 0
print(minCost([1, 10], [3, 4]))  # 12
print(minCost([1, 2, 3], [1, 1, 1]))  # 2
```

**Complexity:** O(n log M) where M = max(nums) - min(nums)
**Trick/Tip:** The cost function is convex because it's a sum of absolute value functions (each convex). For binary search on convex functions, compare f(mid) and f(mid+1) to determine direction. No need for derivatives.

---

# PART B: HASHING PROBLEMS (15)

---

## Problem 13: Two Sum [EASY]

**Problem:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and the same element cannot be used twice.

**Approach:**
Single-pass hash map approach:
1. As you iterate, for each number, check if `target - num` is already in the map.
2. If found, return both indices.
3. Otherwise, store `num → index` in the map.

This avoids the O(n²) brute force by trading space for time.

```python
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test cases
print(twoSum([2, 7, 11, 15], 9))    # [0, 1]
print(twoSum([3, 2, 4], 6))          # [1, 2]
print(twoSum([3, 3], 6))             # [0, 1]
print(twoSum([1, 2, 3], 7))          # [] (no solution)
```

**Complexity:** O(n) time, O(n) space
**Trick/Tip:** The map stores value → index (not index → value). Check for complement BEFORE inserting current element to avoid using the same element twice.

---

## Problem 14: Valid Anagram [EASY]

**Problem:** Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise. An anagram means both strings contain the same characters with the same frequencies.

**Approach:**
1. If lengths differ, immediately return False.
2. Count characters in `s` (increment), then decrement for characters in `t`.
3. If any count goes negative, return False.
4. Return True at the end.

```python
def isAnagram(s, t):
    if len(s) != len(t):
        return False
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1
    for ch in t:
        count[ch] = count.get(ch, 0) - 1
        if count[ch] < 0:
            return False
    return True

# Test cases
print(isAnagram("anagram", "nagaram"))  # True
print(isAnagram("rat", "car"))          # False
print(isAnagram("a", "a"))             # True
print(isAnagram("ab", "a"))            # False
print(isAnagram("", ""))               # True
```

**Complexity:** O(n) time, O(1) space (bounded by alphabet size, max 26 for lowercase)
**Trick/Tip:** Decrement-and-check-negative is faster than comparing full counts because it can exit early. For lowercase-only strings, a 26-element array is faster than a dict.

---

## Problem 15: Intersection of Two Arrays [EASY]

**Problem:** Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must be unique (no duplicates in the result).

**Approach:**
Convert both arrays to sets and return their intersection. Set operations automatically handle uniqueness.

```python
def intersection(nums1, nums2):
    set1 = set(nums1)
    set2 = set(nums2)
    return list(set1 & set2)

# Alternative: iterate smaller set
def intersection(nums1, nums2):
    set1 = set(nums1)
    set2 = set(nums2)
    if len(set1) > len(set2):
        set1, set2 = set2, set1
    return [x for x in set1 if x in set2]

# Test cases
print(sorted(intersection([1, 2, 2, 1], [2, 2])))       # [2]
print(sorted(intersection([4, 9, 5], [9, 4, 9, 8, 4]))) # [4, 9]
print(intersection([1, 2, 3], [4, 5, 6]))                # []
print(intersection([1, 1, 1], [1, 1]))                   # [1]
```

**Complexity:** O(m + n) time, O(min(m, n)) space
**Trick/Tip:** `set1 & set2` creates a new set. For the follow-up (Intersection II with duplicates), use Counter and take min counts.

---

## Problem 16: Contains Duplicate [EASY]

**Problem:** Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

**Approach:**
Iterate through the array, adding each element to a set. If an element is already in the set, we found a duplicate.

```python
def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# One-liner alternative:
def containsDuplicate(nums):
    return len(nums) != len(set(nums))

# Test cases
print(containsDuplicate([1, 2, 3, 1]))     # True
print(containsDuplicate([1, 2, 3, 4]))     # False
print(containsDuplicate([1]))               # False
print(containsDuplicate([1, 1]))            # True
print(containsDuplicate([]))                # False
```

**Complexity:** O(n) time, O(n) space
**Trick/Tip:** The one-liner `len(nums) != len(set(nums))` is clean but always processes the entire array. The iterative approach can exit early on the first duplicate found.

---

## Problem 17: Happy Number (Cycle Detection) [EASY]

**Problem:** Write an algorithm to determine if a number `n` is happy. A happy number is defined by the following process: starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat until the number equals 1, or it loops endlessly in a cycle that doesn't include 1.

**Approach:**
Use a hash set to detect cycles:
1. Compute sum of squares of digits.
2. If result is 1, return True.
3. If we've seen this number before, it's a cycle — return False.
4. Otherwise, add to seen set and repeat.

```python
def isHappy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1

# More efficient: avoid string conversion
def isHappy(n):
    def get_next(num):
        total = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total += digit * digit
        return total

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)
    return n == 1

# Test cases
print(isHappy(19))   # True (1²+9²=82, 8²+2²=68, 6²+8²=100, 1²+0²+0²=1)
print(isHappy(2))    # False
print(isHappy(1))    # True
print(isHappy(7))    # True
```

**Complexity:** O(log n) per step, O(log n) space
**Trick/Tip:** Unhappy numbers always eventually reach the cycle 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4. Floyd's cycle detection (tortoise and hare) gives O(1) space.

---

## Problem 18: Group Anagrams [MEDIUM]

**Problem:** Given an array of strings `strs`, group the anagrams together. You can return the answer in any order. An anagram is a word formed by rearranging the letters of another.

**Approach:**
All anagrams of a string have the same sorted representation. Use the sorted string as a hash key to group them.

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# More efficient: use character count tuple as key
def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())

# Test cases
print(groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [["eat","tea","ate"],["tan","nat"],["bat"]]
print(groupAnagrams([""]))  # [[""]]
print(groupAnagrams(["a"]))  # [["a"]]
print(groupAnagrams(["ab", "ba", "abc"]))  # [["ab","ba"],["abc"]]
```

**Complexity:** O(n * k log k) for sorted approach, O(n * k) for count approach, where n = number of strings, k = max string length
**Trick/Tip:** For interview, the count tuple approach is more efficient. Use `tuple(count)` because lists aren't hashable. Both approaches work well for constraints up to 10⁴ strings of length 100.

---

## Problem 19: Subarray Sum Equals K [MEDIUM]

**Problem:** Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals `k`. Subarrays are contiguous elements.

**Approach:**
Prefix sum with hash map:
1. Maintain a running prefix sum.
2. If `prefix - k` has been seen before, those subarrays sum to k.
3. Store frequency of each prefix sum.

The key insight: `prefix[j] - prefix[i] = k` means subarray from i+1 to j sums to k.

```python
def subarraySum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}  # base case: prefix sum 0 seen once
    for num in nums:
        prefix += num
        if prefix - k in seen:
            count += seen[prefix - k]
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

# Test cases
print(subarraySum([1, 1, 1], 2))                    # 2
print(subarraySum([1, 2, 3], 3))                    # 2 ([1,2] and [3])
print(subarraySum([1], 0))                           # 0
print(subarraySum([0, 0, 0, 0, 0], 0))              # 15
print(subarraySum([-1, -1, 1], 0))                   # 1
```

**Complexity:** O(n) time, O(n) space
**Trick/Tip:** Initialize `{0: 1}` to handle subarrays from index 0 that sum to k. The map stores frequency, not just presence, because multiple subarrays can have the same prefix sum (e.g., with zeros).

---

## Problem 20: Longest Consecutive Sequence [MEDIUM]

**Problem:** Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.

**Approach:**
1. Put all numbers in a set.
2. For each number, check if it's the START of a sequence (`num - 1` NOT in set).
3. If it's a start, count consecutive numbers forward.
4. Track the maximum length.

This ensures each element is visited at most twice (once in outer loop, once in while loop).

```python
def longestConsecutive(nums):
    num_set = set(nums)
    max_len = 0
    for num in num_set:
        if num - 1 not in num_set:  # start of sequence
            length = 1
            while num + length in num_set:
                length += 1
            max_len = max(max_len, length)
    return max_len

# Test cases
print(longestConsecutive([100, 4, 200, 1, 3, 2]))  # 4 (sequence: 1,2,3,4)
print(longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9
print(longestConsecutive([1, 2, 0, 1]))  # 3 (0,1,2)
print(longestConsecutive([]))  # 0
print(longestConsecutive([9, 1, 4, 7, 3, -1, 6, 5, 2]))  # 5 (1,2,3,4,5)
```

**Complexity:** O(n) time, O(n) space
**Trick/Tip:** The condition `num - 1 not in set` is crucial. Without it, every element starts a new scan, making it O(n²). With it, only sequence starts trigger scans, and each element is part of at most one scan.

---

## Problem 21: Sort Characters by Frequency [MEDIUM]

**Problem:** Given a string `s`, sort it in decreasing order based on the frequency of its characters. Return the sorted string. If multiple characters have the same frequency, any order among them is acceptable.

**Approach:**
Count frequencies, then sort characters by their frequency in descending order. Build the result by repeating each character by its count.

```python
def frequencySort(s):
    from collections import Counter
    count = Counter(s)
    # Sort by frequency descending, then by character for stability
    sorted_chars = sorted(count.keys(), key=lambda c: (-count[c], c))
    return ''.join(ch * count[ch] for ch in sorted_chars)

# Bucket sort approach for O(n)
def frequencySort(s):
    from collections import Counter
    count = Counter(s)
    max_freq = max(count.values())
    buckets = [[] for _ in range(max_freq + 1)]
    for ch, freq in count.items():
        buckets[freq].append(ch)
    result = []
    for freq in range(max_freq, 0, -1):
        for ch in buckets[freq]:
            result.append(ch * freq)
    return ''.join(result)

# Test cases
print(frequencySort("tree"))     # "eert" or "eetr"
print(frequencySort("cccaaa"))   # "aaaccc" or "cccaaa"
print(frequencySort("Aabb"))     # "bbAa" or "bbaA"
print(frequencySort("ab"))       # "ab" or "ba"
print(frequencySort("aaaabbbb")) # "aaaabbbb"
```

**Complexity:** O(n log n) for sort approach, O(n) for bucket sort approach
**Trick/Tip:** Bucket sort is optimal here. Create buckets indexed by frequency. Iterate from highest frequency bucket to lowest. Each character appears exactly in one bucket.

---

## Problem 22: Top K Frequent Elements (Bucket Sort) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order. The answer is guaranteed to be unique.

**Approach:**
Bucket sort achieves O(n):
1. Count frequencies with a hash map.
2. Create n+1 buckets (index = frequency, 0 to n).
3. Place each element in the bucket corresponding to its frequency.
4. Iterate buckets from highest to lowest frequency, collecting k elements.

```python
def topKFrequent(nums, k):
    from collections import Counter
    count = Counter(nums)
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for i in range(n, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result

# Test cases
print(sorted(topKFrequent([1, 1, 1, 2, 2, 3], 2)))  # [1, 2]
print(topKFrequent([1], 1))                            # [1]
print(sorted(topKFrequent([4, 1, -1, 2, -1, 2, 3], 2)))  # [-1, 2]
print(sorted(topKFrequent([1, 2, 2, 3, 3, 3], 2)))   # [2, 3]
```

**Complexity:** O(n) time, O(n) space
**Trick/Tip:** Bucket sort is the only way to beat O(n log n) for this problem — but it works because frequencies are bounded by n, not arbitrary. This exploits the constraint that we're counting frequencies of n elements.

---

## Problem 23: Find All Anagrams in a String [MEDIUM]

**Problem:** Given two strings `s` and `p`, find all the start indices of `p`'s anagrams in `s`. Return the list of all such start indices. Strings consist of lowercase English letters only.

**Approach:**
Sliding window with frequency comparison:
1. Build frequency count for `p` and for the first window in `s` of size `len(p)`.
2. Slide the window: remove the leftmost character, add the new rightmost character.
3. After each slide, compare frequency maps.
4. For efficiency, track the number of matched characters instead of full map comparison.

```python
from collections import Counter

def findAnagrams(s, p):
    if len(p) > len(s):
        return []
    p_count = Counter(p)
    s_count = Counter(s[:len(p)])
    result = []
    if s_count == p_count:
        result.append(0)

    for i in range(1, len(s) - len(p) + 1):
        # Remove leftmost character of previous window
        left_char = s[i - 1]
        s_count[left_char] -= 1
        if s_count[left_char] == 0:
            del s_count[left_char]
        # Add new rightmost character
        right_char = s[i + len(p) - 1]
        s_count[right_char] += 1
        if s_count == p_count:
            result.append(i)
    return result

# O(n) approach with match counting
def findAnagrams(s, p):
    if len(p) > len(s):
        return []
    p_count = Counter(p)
    s_count = {}
    result = []
    required = len(p_count)
    formed = 0
    window = len(p)

    for i in range(len(s)):
        ch = s[i]
        s_count[ch] = s_count.get(ch, 0) + 1
        if ch in p_count and s_count[ch] == p_count[ch]:
            formed += 1
        if i >= window:
            left = s[i - window]
            s_count[left] -= 1
            if left in p_count and s_count[left] == p_count[left] - 1:
                formed -= 1
            if s_count[left] == 0:
                del s_count[left]
        if formed == required:
            result.append(i - window + 1)
    return result

# Test cases
print(findAnagrams("cbaebabacd", "abc"))  # [0, 6]
print(findAnagrams("abab", "ab"))         # [0, 1, 2]
print(findAnagrams("a", "a"))             # [0]
print(findAnagrams("ab", "ab"))           # [0]
print(findAnagrams("aa", "bb"))           # []
```

**Complexity:** O(n) time (with match counting), O(k) space where k = alphabet size
**Trick/Tip:** Comparing entire dicts each time is O(26) = O(1) for lowercase letters, so both approaches are effectively O(n). The match counting approach avoids dict comparison entirely.

---

## Problem 24: Continuous Subarray Sum (Divisible by k) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return `True` if `nums` has a good subarray with length at least 2, where the sum of the subarray is a multiple of `k`.

**Approach:**
Prefix sum modulo k:
1. Compute running prefix sum modulo k.
2. If the same remainder appears at positions i and j (j - i ≥ 2), the subarray from i+1 to j has sum divisible by k.
3. Store first occurrence of each remainder (we want the earliest start for maximum subarray length).

```python
def checkSubarraySum(nums, k):
    seen = {0: -1}  # remainder 0 at index -1 (before start)
    prefix = 0
    for i, num in enumerate(nums):
        prefix += num
        rem = prefix % k
        if rem in seen:
            if i - seen[rem] >= 2:
                return True
        else:
            seen[rem] = i
    return False

# Test cases
print(checkSubarraySum([23, 2, 4, 6, 7], 6))      # True ([2, 4] sum=6)
print(checkSubarraySum([23, 2, 6, 4, 7], 6))      # True ([23, 2, 6, 4, 7] sum=42)
print(checkSubarraySum([23, 2, 6, 4, 7], 13))     # False
print(checkSubarraySum([5, 0, 0, 0], 3))           # True ([0, 0])
print(checkSubarraySum([0, 1, 0], 1))              # True
```

**Complexity:** O(n) time, O(k) space
**Trick/Tip:** Initialize `{0: -1}` to handle subarrays starting from index 0. Only store the first occurrence — we never update it, which ensures the subarray is as long as possible.

---

## Problem 25: Minimum Index Sum of Two Lists [MEDIUM]

**Problem:** Suppose Andy and Doris want to have dinner. They each have a list of restaurants they like (as strings). Find the restaurant(s) with the minimum index sum. If multiple restaurants have the same minimum sum, return all of them in any order.

**Approach:**
1. Build a map of restaurant → index for list1.
2. Iterate list2, checking each restaurant against the map.
3. Compute index sum, track minimum, collect all restaurants with that sum.

```python
def findRestaurant(list1, list2):
    map1 = {name: i for i, name in enumerate(list1)}
    min_sum = float('inf')
    result = []
    for j, name in enumerate(list2):
        if name in map1:
            idx_sum = map1[name] + j
            if idx_sum < min_sum:
                min_sum = idx_sum
                result = [name]
            elif idx_sum == min_sum:
                result.append(name)
    return result

# Test cases
print(findRestaurant(["Shogun", "Tapioca Express", "Burger King", "KFC"],
                      ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"]))
# ["Shogun"]
print(findRestaurant(["Shogun", "Tapioca Express", "Burger King", "KFC"],
                      ["KFC", "Shogun", "Burger King"]))
# ["Shogun"]
print(findRestaurant(["happy", "sad", "good"],
                      ["sad", "happy", "good"]))
# ["sad", "happy"]
print(findRestaurant(["a", "b", "c"], ["d", "e", "f"]))  # []
```

**Complexity:** O(n + m) time, O(n) space where n = len(list1), m = len(list2)
**Trick/Tip:** You could iterate the shorter list and look up in the longer list's map, but both approaches are O(n + m). The key is only building one map, not two.

---

## Problem 26: Max Points on a Line [HARD]

**Problem:** Given an array of points where `points[i] = [xi, yi]` represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.

**Approach:**
For each point i, compute the slope to every other point j. Points on the same line through i have the same slope.

Key considerations:
- Use a fraction (dy, dx) reduced by GCD to avoid floating-point precision issues.
- Normalize sign: make dx always positive (if dx is 0, make dy positive).
- Count duplicate points separately (same coordinates).

```python
from math import gcd
from collections import defaultdict

def maxPoints(points):
    if len(points) <= 2:
        return len(points)
    result = 0
    for i in range(len(points)):
        slopes = defaultdict(int)
        duplicates = 1
        for j in range(i + 1, len(points)):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]
            if dx == 0 and dy == 0:
                duplicates += 1
                continue
            g = gcd(dx, dy)
            dx //= g
            dy //= g
            # Normalize sign
            if dx < 0:
                dx, dy = -dx, -dy
            elif dx == 0:
                dy = abs(dy)
            slopes[(dy, dx)] += 1
        current = duplicates + max(slopes.values(), default=0)
        result = max(result, current)
    return result

# Test cases
print(maxPoints([[1, 1], [2, 2], [3, 3]]))          # 3
print(maxPoints([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))  # 4
print(maxPoints([[0, 0]]))                            # 1
print(maxPoints([[0, 0], [1, -1]]))                   # 2
print(maxPoints([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]))  # 5
```

**Complexity:** O(n²) time, O(n) space
**Trick/Tip:** Normalizing the slope fraction is critical. `gcd(dx, dy)` ensures `(2, 4)` and `(1, 2)` produce the same key `(1, 2)`. Making dx always positive (and dy positive when dx=0) prevents `(1, 2)` and `(-1, -2)` from being different keys.

---

## Problem 27: LRU Cache [HARD]

**Problem:** Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement the `LRUCache` class with `get(key)` and `put(key, value)` methods, both running in O(1) average time.

**Approach:**
Use Python's `OrderedDict` which maintains insertion order:
- `get(key)`: if key exists, move it to end (most recently used) and return value.
- `put(key, value)`: if key exists, move to end and update value. If at capacity, remove leftmost (least recently used) item first.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# Test cases
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))     # 1
cache.put(3, 3)          # evicts key 2
print(cache.get(2))     # -1
cache.put(4, 4)          # evicts key 1
print(cache.get(1))     # -1
print(cache.get(3))     # 3
print(cache.get(4))     # 4
```

**Complexity:** O(1) for both get and put
**Trick/Tip:** `OrderedDict.move_to_end(key)` moves to the right (most recently used end). `popitem(last=False)` removes from the left (least recently used end). For interview implementation without OrderedDict, use a doubly-linked list + hash map.

---

# PART C: HEAPS / PRIORITY QUEUE PROBLEMS (13)

---

## Problem 28: Kth Largest Element (Min Heap of Size k) [EASY]

**Problem:** Given an unsorted array of integers `nums` and an integer `k`, return the kth largest element. Note: it is the kth largest element in sorted order, not the kth distinct element.

**Approach:**
Maintain a min-heap of size k:
1. For each element, push it to the heap.
2. If heap size exceeds k, pop the smallest.
3. After processing all elements, the heap contains the k largest elements.
4. The root (smallest in the heap) = kth largest overall.

```python
import heapq

def findKthLargest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

# Alternative: heapify first n elements, then iterate remaining
def findKthLargest(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)
    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)
    return heap[0]

# Test cases
print(findKthLargest([3, 2, 1, 5, 6, 4], 2))       # 5
print(findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # 4
print(findKthLargest([1], 1))                          # 1
print(findKthLargest([7, 7, 7, 7], 2))                # 7
print(findKthLargest([2, 1], 1))                       # 2
```

**Complexity:** O(n log k) time, O(k) space
**Trick/Tip:** `heapq.heapreplace(heap, num)` is equivalent to pop then push but more efficient (single operation). Use it when you know the new element is larger than the root.

---

## Problem 29: Last Stone Weight [EASY]

**Problem:** You have an array of stones where `stones[i]` is the weight of the ith stone. Each turn, choose the two heaviest stones and smash them:
- If both are equal, both are destroyed.
- If different, the lighter is destroyed and the heavier is reduced by the lighter's weight.
Continue until at most one stone remains. Return the weight of the last stone, or 0 if none.

**Approach:**
Use a max-heap (negate all values for Python's min-heap):
1. Push all stones (negated) into a heap.
2. Pop the two largest (most negative = largest after negation).
3. Compute difference, push back if non-zero.
4. Continue until 0 or 1 stones remain.

```python
import heapq

def lastStoneWeight(stones):
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)   # heaviest
        second = -heapq.heappop(heap)  # second heaviest
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0

# Test cases
print(lastStoneWeight([2, 7, 4, 1, 8, 1]))  # 1
print(lastStoneWeight([1]))                   # 1
print(lastStoneWeight([1, 1]))                 # 0
print(lastStoneWeight([8, 10, 4]))             # 2
print(lastStoneWeight([9, 10, 1, 2, 3, 4]))   # 3
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** Python's `heapq` is a min-heap only. Negate all values to simulate max-heap. Always remember to negate back when reading values.

---

## Problem 30: K Closest Points to Origin [EASY]

**Problem:** Given an array of points where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the k closest points to the origin (0, 0). Distance is measured by Euclidean distance.

**Approach:**
Use a max-heap of size k:
1. For each point, compute squared distance (no need for sqrt).
2. Push (negative_distance, x, y) to the heap.
3. If heap exceeds k, pop the farthest (the most negative = largest distance).
4. The heap at the end contains the k closest points.

```python
import heapq

def kClosest(points, k):
    heap = []
    for x, y in points:
        dist = -(x*x + y*y)  # negate for max-heap behavior
        heapq.heappush(heap, (dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]

# Test cases
print(kClosest([[1, 3], [-2, 2]], 1))            # [[-2, 2]]
print(kClosest([[3, 3], [5, -1], [-2, 4]], 2))   # [[3, 3], [-2, 4]]
print(kClosest([[0, 0]], 1))                       # [[0, 0]]
print(kClosest([[1, 1], [1, 1], [2, 2], [2, 2]], 2))  # [[1,1],[1,1]]
print(kClosest([[-5, 4], [-6, -5], [4, 6], [-2, 3], [-4, -3]], 3))
```

**Complexity:** O(n log k) time, O(k) space
**Trick/Tip:** Don't compute `sqrt(x*x + y*y)` — it's unnecessary and slower. Squared distances preserve the same ordering as Euclidean distances.

---

## Problem 31: Reduce Array Size to Half [EASY]

**Problem:** Given an array `arr`, you can remove any set of unique values from the array. Return the minimum number of unique values you need to remove so that at least half of the array's elements are removed.

**Approach:**
Greedy strategy:
1. Count frequency of each unique value.
2. Sort frequencies in descending order.
3. Remove most frequent values first — this minimizes the number of distinct values removed.
4. Stop when cumulative removed ≥ n/2.

```python
def minSetSize(arr):
    from collections import Counter
    counts = sorted(Counter(arr).values(), reverse=True)
    removed = 0
    half = len(arr) // 2
    for i, count in enumerate(counts):
        removed += count
        if removed >= half:
            return i + 1
    return len(counts)

# Test cases
print(minSetSize([3, 3, 3, 3, 5, 5, 5, 2, 2, 7]))  # 2
print(minSetSize([7, 7, 7, 7, 7, 7]))                 # 1
print(minSetSize([1, 9]))                               # 1
print(minSetSize([1000, 1000, 3, 7]))                   # 1
print(minSetSize([1, 2, 3, 4, 5, 6]))                  # 3
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** This is a greedy problem. Sorting by frequency in descending order and removing greedily is optimal because removing a high-frequency value eliminates more elements per "removal slot."

---

## Problem 32: Top K Frequent Elements (Heap Approach) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer can be returned in any order.

**Approach:**
Use a min-heap of size k:
1. Count all element frequencies.
2. For each unique element, push (frequency, element) to heap.
3. If heap exceeds k, pop the element with lowest frequency.
4. The k most frequent elements remain in the heap.

```python
import heapq
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for freq, num in heap]

# Max-heap approach (push all, pop k times)
def topKFrequent(nums, k):
    count = Counter(nums)
    heap = [(-freq, num) for num, freq in count.items()]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(k)]

# Test cases
print(sorted(topKFrequent([1, 1, 1, 2, 2, 3], 2)))     # [1, 2]
print(topKFrequent([1], 1))                               # [1]
print(sorted(topKFrequent([4, 1, -1, 2, -1, 2, 3], 2))) # [-1, 2]
print(sorted(topKFrequent([1, 2, 2, 3, 3, 3], 2)))      # [2, 3]
```

**Complexity:** O(n log k) time, O(n) space
**Trick/Tip:** The min-heap approach is simpler than the max-heap approach. For O(n), use bucket sort (Problem 22). In an interview, mention both approaches.

---

## Problem 33: Sort Array by Increasing Frequency [MEDIUM]

**Problem:** Given an array of integers `nums`, sort the array in decreasing order based on the frequency of the values. If multiple values have the same frequency, sort them in decreasing order.

**Approach:**
Use a heap with custom ordering:
1. Count frequencies.
2. Push (frequency, -value) to heap — negative value ensures descending order for ties.
3. Pop from heap and build result by repeating each value `freq` times.

```python
import heapq
from collections import Counter

def frequencySort(nums):
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, -num))
    result = []
    while heap:
        freq, neg_num = heapq.heappop(heap)
        result.extend([-neg_num] * freq)
    return result

# Alternative: sorted approach
def frequencySort(nums):
    count = Counter(nums)
    return sorted(nums, key=lambda x: (count[x], -x))

# Test cases
print(frequencySort([1, 1, 2, 2, 2, 3]))  # [3, 1, 1, 2, 2, 2]
print(frequencySort([2, 3, 5, 3, 7, 9, 7, 8, 1]))  # [1, 8, 5, 9, 2, 3, 3, 7, 7]
print(frequencySort([-1, 1, -6, 4, 5, -6, 1, 4, 1]))  # [5, -1, 4, 4, -6, -6, 1, 1, 1]
print(frequencySort([1]))  # [1]
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** For the sorted approach: `sorted(nums, key=lambda x: (count[x], -x))` — `count[x]` for ascending frequency, `-x` for descending value when frequencies match.

---

## Problem 34: Reorganize String [MEDIUM]

**Problem:** Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same. Return any valid rearrangement, or "" if not possible.

**Approach:**
Greedy approach with max-heap:
1. Check if rearrangement is possible: max frequency ≤ (n+1) // 2.
2. Use max-heap to always pick the most frequent remaining character.
3. Track the previous character and re-insert it after using current one.
4. This prevents adjacent duplicates by always using a "cooldown" for each character.

```python
import heapq
from collections import Counter

def reorganizeString(s):
    count = Counter(s)
    if max(count.values()) > (len(s) + 1) // 2:
        return ""

    heap = [(-freq, ch) for ch, freq in count.items()]
    heapq.heapify(heap)
    result = []
    prev = None

    while heap:
        freq, ch = heapq.heappop(heap)
        result.append(ch)
        if prev:
            heapq.heappush(heap, prev)
            prev = None
        freq += 1  # increment because freq is negative
        if freq < 0:
            prev = (freq, ch)

    return ''.join(result) if len(result) == len(s) else ""

# Test cases
print(reorganizeString("aab"))         # "aba"
print(reorganizeString("aaab"))        # ""
print(reorganizeString("aaabbb"))      # "ababab"
print(reorganizeString("aaabc"))       # "abaca" or similar
print(reorganizeString("vvvlo"))       # "vlvov"
```

**Complexity:** O(n log k) where k = unique characters
**Trick/Tip:** The `prev` variable acts as a cooldown. After using a character, it can't be used again until another character is used. Re-inserting `prev` after popping the current ensures we never place same characters adjacent.

---

## Problem 35: Task Scheduler [MEDIUM]

**Problem:** You are given a character array `tasks` representing tasks a CPU needs to do. Each task takes one unit of time. The CPU can only do one task at a time. There is a non-negative integer `n` that represents the cooldown period between two same tasks. Return the least number of intervals the CPU will take to finish all tasks.

**Approach:**
Mathematical formula approach:
1. Find the maximum frequency task and count how many tasks share that frequency.
2. The minimum intervals = `(max_freq - 1) * (n + 1) + count_of_max_freq`.
3. If there are many different tasks, we can fill all idle slots, so answer = len(tasks).

```python
def leastInterval(tasks, n):
    from collections import Counter
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for v in freq.values() if v == max_freq)
    min_intervals = (max_freq - 1) * (n + 1) + max_count
    return max(len(tasks), min_intervals)

# Test cases
print(leastInterval(["A", "A", "A", "B", "B", "B"], 2))  # 8
print(leastInterval(["A", "A", "A", "B", "B", "B"], 0))  # 6
print(leastInterval(["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2))  # 16
print(leastInterval(["A", "B", "C", "D"], 2))  # 4
print(leastInterval(["A", "A", "A", "B", "B", "B"], 1))  # 6
```

**Complexity:** O(n) time, O(1) space
**Trick/Tip:** Visualize it: place max_freq tasks with n gaps between them. The `count_of_max_freq` tasks fill the last row completely. If `len(tasks) > min_intervals`, there are enough different tasks to fill all gaps, so no idle slots needed.

---

## Problem 36: Meeting Rooms II (Heap Version) [MEDIUM]

**Problem:** Given an array of meeting time intervals consisting of start and end times `[[s1, e1], [s2, e2], ...]`, find the minimum number of conference rooms required. (Duplicate of Problem 7, presented as a heap-focused solution.)

**Approach:**
Sort by start time, use min-heap:
1. Sort all meetings by their start time.
2. The heap stores end times of currently active meetings.
3. For each meeting, if the earliest meeting has ended, reuse that room.
4. Always add current meeting's end time.

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort()  # sort by start time
    heap = [intervals[0][1]]  # first meeting's end time
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        if heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)

# Alternative: event-based approach
def minMeetingRooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))    # meeting starts
        events.append((end, -1))     # meeting ends
    events.sort()
    max_rooms = 0
    current = 0
    for _, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)
    return max_rooms

# Test cases
print(minMeetingRooms([[0, 30], [5, 10], [15, 20]]))  # 2
print(minMeetingRooms([[7, 10], [2, 4]]))              # 1
print(minMeetingRooms([[1, 5], [2, 3], [4, 6]]))      # 2
print(minMeetingRooms([[1, 5], [5, 10]]))              # 1
print(minMeetingRooms([[9, 10], [4, 5], [2, 3], [5, 6], [7, 8]]))  # 1
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** The event-based approach (separate start and end events) is another clean way to solve this. Sort events; start events add +1, end events add -1. Max concurrent = max running sum.

---

## Problem 37: Kth Smallest Element in a Sorted Matrix [MEDIUM]

**Problem:** Given an n x n matrix where each row and column is sorted in ascending order, find the kth smallest element in the matrix. Note that it's the kth smallest element in sorted order, not the kth distinct element.

**Approach:**
Min-heap with merge-like approach:
1. Initialize heap with the first element of each row: `(matrix[i][0], i, 0)`.
2. Pop the smallest element k times.
3. Each time you pop from row `r` at column `c`, push the next element from the same row `(matrix[r][c+1], r, c+1)`.
4. After k pops, the last popped value is the answer.

```python
import heapq

def kthSmallest(matrix, k):
    n = len(matrix)
    heap = [(matrix[i][0], i, 0) for i in range(min(n, k))]
    heapq.heapify(heap)
    for _ in range(k):
        val, row, col = heapq.heappop(heap)
        if col + 1 < n:
            heapq.heappush(heap, (matrix[row][col + 1], row, col + 1))
    return val

# Test cases
print(kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8))  # 13
print(kthSmallest([[-5]], 1))                                      # -5
print(kthSmallest([[1, 2], [3, 3]], 2))                           # 2
print(kthSmallest([[1, 3, 5], [6, 7, 8], [9, 10, 11]], 5))       # 7
```

**Complexity:** O(k log n) time, O(n) space
**Trick/Tip:** We only push to the right (same row, next column) because rows and columns are sorted. Pushing down (next row, same column) would cause duplicates and redundant processing.

---

## Problem 38: Employee Free Time [MEDIUM]

**Problem:** We are given a list of `schedule` (each element is a list of non-overlapping intervals sorted by start time) representing the schedules of employees. Find all intervals of time that are free for all employees. Return the answer in sorted order.

**Approach:**
1. Flatten all employee schedules into one list of intervals.
2. Sort by start time.
3. Merge overlapping intervals (standard merge intervals).
4. Gaps between merged intervals are free times for all employees.

```python
def employeeFreeTime(schedule):
    # Flatten all intervals
    intervals = []
    for emp in schedule:
        for interval in emp:
            intervals.append(interval)
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    # Find gaps between merged intervals
    result = []
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] > end:
            # Gap found: free time for all employees
            result.append([end, intervals[i][0]])
        end = max(end, intervals[i][1])
    return result

# Test cases
schedule1 = [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]
print(employeeFreeTime(schedule1))  # [[3, 4]]

schedule2 = [[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]
print(employeeFreeTime(schedule2))  # [[5, 6], [7, 9]]

schedule3 = [[[1, 2], [3, 4], [5, 6]]]
print(employeeFreeTime(schedule3))  # [[2, 3], [4, 5]]

schedule4 = [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]], [[0, 15]]]
print(employeeFreeTime(schedule4))  # [] (no common free time)
```

**Complexity:** O(n log n) time where n = total intervals, O(n) space
**Trick/Tip:** This is essentially "merge intervals" + "find gaps." The key insight is that if you merge ALL employee schedules, any gap in the merged result is free for everyone. No need for per-employee tracking.

---

## Problem 39: Merge k Sorted Lists [HARD]

**Problem:** You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

**Approach:**
Min-heap approach:
1. Push the head of each non-empty list into the heap as `(value, list_index, node)`.
2. Pop the smallest, add it to the result.
3. Push the next node from the same list (if exists).
4. Use list_index to break ties when values are equal (avoids comparing node objects).

```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy
    idx = len(lists)  # unique index counter

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            idx += 1
            heapq.heappush(heap, (node.next.val, idx, node.next))

    return dummy.next

# Test cases (helper function)
def list_to_arr(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# list1: 1->4->5
l1 = ListNode(1, ListNode(4, ListNode(5)))
# list2: 1->3->4
l2 = ListNode(1, ListNode(3, ListNode(4)))
# list3: 2->6
l3 = ListNode(2, ListNode(6)))
print(list_to_arr(mergeKLists([l1, l2, l3])))  # [1, 1, 2, 3, 4, 4, 5, 6]
print(list_to_arr(mergeKLists([])))              # []
print(list_to_arr(mergeKLists([ListNode(1)])))   # [1]
```

**Complexity:** O(N log k) time where N = total nodes, O(k) space for the heap
**Trick/Tip:** The `idx` counter (incrementing for each push) ensures heap comparisons never compare node objects. This avoids issues when values are equal. Alternatively, use `(val, list_index, node)` where `list_index` is the original list index.

---

## Problem 40: Find Median from Data Stream (Heap Version) [HARD]

**Problem:** The median is the middle value in an ordered integer list. Design a data structure that supports `addNum(num)` and `findMedian()`. Both operations must be efficient.

**Approach:**
Two-heap approach (detailed version of Problem 11):
1. `max_heap` (lower half): stores the smaller half of numbers. We negate values since Python has min-heap.
2. `min_heap` (upper half): stores the larger half of numbers.
3. Invariant: `len(max_heap) >= len(min_heap)` and `len(max_heap) - len(min_heap) <= 1`.
4. When adding: push to max_heap first, then move max from max_heap to min_heap, then rebalance if needed.
5. Median: if odd count, max_heap root. If even, average of both roots.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap = []  # lower half (negate for max-heap)
        self.min_heap = []  # upper half

    def addNum(self, num):
        heapq.heappush(self.max_heap, -num)
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def findMedian(self):
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0

# Test cases
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())   # 1.5
mf.addNum(3)
print(mf.findMedian())   # 2
mf.addNum(4)
print(mf.findMedian())   # 2.5
mf.addNum(5)
print(mf.findMedian())   # 3
mf.addNum(6)
print(mf.findMedian())   # 3.5
mf.addNum(7)
print(mf.findMedian())   # 4
mf.addNum(8)
print(mf.findMedian())   # 4.5
```

**Complexity:** Add O(log n), Find Median O(1)
**Trick/Tip:** The two-step balancing (push to max_heap, then move max to min_heap, then rebalance if min_heap is larger) ensures the invariant holds. This is cleaner than comparing values to decide which heap to use. The extra element (when count is odd) is always in max_heap.

---

# QUICK REFERENCE: Key Patterns

| Pattern | Problems | Key Insight |
|---------|----------|-------------|
| Dutch National Flag | 2 | Three-way partition for 3 values in O(n) |
| Two-Heap Median | 11, 40 | Max-heap + Min-heap balanced |
| Min-Heap of Size K | 4, 28, 29, 30, 31, 32 | Root = kth largest/smallest |
| Prefix Sum + Hash | 19, 24 | Cumulative sum tracking for subarrays |
| Bucket Sort | 8, 22 | O(n) non-comparison sort |
| Topological/Scheduling | 35 | Formula-based calculation |
| LRU / Ordered Dict | 27 | O(1) get/put with ordering |
| Slope Hashing | 26 | GCD-normalized fractions |
| Merge Sort Variants | 10 | Count during merge step |
| Sliding Window + Hash | 23 | Fixed window frequency comparison |
| Greedy + Frequency | 21, 31, 33, 34 | Frequency-driven sorting |

---

# INTERVIEW TIPS FOR SORTING, HASHING & HEAPS

1. **Always clarify constraints**: What's the range of values? Can you modify the input? Is stability needed?

2. **Know your complexity targets**:
   - Sorting: O(n log n) is standard, O(n) with bucket/counting sort
   - Hashing: O(1) amortized per operation
   - Heaps: O(log n) push/pop, O(1) peek

3. **Python heap is min-heap only**: Negate values for max-heap behavior. Use `(priority, item)` tuples for custom ordering.

4. **Hash map patterns**:
   - Two Sum style: store complement
   - Prefix sum: store cumulative sums
   - Grouping: use canonical key (sorted string, reduced fraction)
   - Frequency counting: Counter is your friend

5. **Heap patterns**:
   - Kth largest/smallest: min-heap of size k
   - Merge k sorted: heap with k elements
   - Running median: two heaps
   - Task scheduling: formula or simulation

6. **Edge cases to always check**:
   - Empty arrays/lists
   - Single element
   - All elements same
   - All elements different
   - Negative numbers
   - Integer overflow (not in Python, but mention it)

---

# COMMON MISTAKES TO AVOID

1. **Forgetting to negate in Python max-heap**: All solutions using negated values for max-heap behavior — forgetting to negate back gives wrong answers.

2. **Off-by-one in prefix sum**: Forgetting `{0: 1}` initialization causes missed subarrays starting from index 0.

3. **Not checking `num - 1 not in set`**: Without this check in Longest Consecutive Sequence, you revisit every element multiple times → O(n²).

4. **Floating-point slopes**: Using `dy/dx` as slope key causes precision issues. Always use reduced fraction tuples `(dy, dx)` with GCD.

5. **Modifying dict during iteration**: When iterating over a hash map and modifying it, use a copy or collect keys first.

6. **Heap comparison failures**: When pushing objects to heap, ensure all elements are comparable. Use `(priority, unique_id, object)` pattern.

7. **Edge case in Two Sum**: The same element cannot be used twice — check before inserting into the map.

8. **Kth Largest confusion**: kth largest ≠ kth distinct. Problem 5 counts duplicates; use a set if distinct is needed.

9. **Not handling empty input**: Always check for empty arrays, lists, or strings before processing.

10. **Stack overflow in recursion**: Deep recursion in merge sort or quickselect can hit Python's recursion limit. For large inputs, consider iterative approaches or increase limit with `sys.setrecursionlimit()`.

---

> **Total: 40 Problems | 1800+ lines | Sorting (12) + Hashing (15) + Heaps (13)**
> **Difficulty: Easy (12) + Medium (18) + Hard (10)**
> **All solutions include: Complete Python code, test cases, complexity analysis, and interview tips**
