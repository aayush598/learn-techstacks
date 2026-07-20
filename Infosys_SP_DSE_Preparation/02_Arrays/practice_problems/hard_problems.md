# Hard Practice Problems - Arrays

## Problem 1: Trapping Rain Water (LeetCode 42)

**Problem:** Given n non-negative integers, compute how much water it can trap after raining.

**Constraints:**
- n >= 0
- 0 <= height[i] <= 10^5

**Approach 1: Two Pointer (Optimal)**
1. Track left_max and right_max as pointers move inward
2. Water at each position = min(left_max, right_max) - height[i]
3. Move pointer with smaller max (it's the bottleneck)

```python
def trap(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
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

# Example
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # 6
```

**Time:** O(n) | **Space:** O(1)

**Approach 2: Stack**
```python
def trap_stack(height):
    stack = []
    water = 0
    
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = height[stack.pop()]
            if stack:
                width = i - stack[-1] - 1
                water += width * (min(h, height[stack[-1]]) - bottom)
        stack.append(i)
    
    return water
# Time: O(n), Space: O(n)
```

**Similar Problems:**
- Container With Most Water
- Largest Rectangle in Histogram
- Maximal Rectangle

---

## Problem 2: Maximum Subarray Min-Product (LeetCode 1856)

**Problem:** Maximize min-product of a subarray. min-product = min(subarray) * sum(subarray).

**Constraints:**
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^7

**Approach:**
1. Use monotonic stack to find range where each element is minimum
2. Use prefix sum to get range sum in O(1)
3. For each element as minimum, compute min-product with its range

```python
def max_sum_min_product(nums):
    MOD = 10**9 + 7
    n = len(nums)
    
    # Prefix sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    
    # Find left and right boundaries using monotonic stack
    left = [-1] * n
    right = [n] * n
    stack = []
    
    for i in range(n):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        left[i] = stack[-1] if stack else -1
        stack.append(i)
    
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] > nums[i]:
            stack.pop()
        right[i] = stack[-1] if stack else n
        stack.append(i)
    
    # Compute max min-product
    result = 0
    for i in range(n):
        total = prefix[right[i]] - prefix[left[i] + 1]
        result = max(result, nums[i] * total)
    
    return result % MOD

# Example
print(max_sum_min_product([1, 2, 3, 2]))  # 14
```

**Time:** O(n) | **Space:** O(n)

**Similar Problems:**
- Largest Rectangle in Histogram
- Sum of Subarray Minimums

---

## Problem 3: Count of Range Sum (LeetCode 327)

**Problem:** Count range sums in given range [lower, upper].

**Constraints:**
- -2^31 <= nums[i] <= 2^31 - 1
- 0 <= n <= 10^5

**Approach (Prefix Sum + Merge Sort):**
1. Compute prefix sums
2. Count pairs where prefix[j] - prefix[i] is in [lower, upper]
3. Use modified merge sort to count

```python
def count_range_sum(nums, lower, upper):
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]
    
    def merge_sort_count(start, end):
        if end - start <= 1:
            return 0
        
        mid = (start + end) // 2
        count = merge_sort_count(start, mid) + merge_sort_count(mid, end)
        
        # Count range sums crossing mid
        j = k = mid
        for left in range(start, mid):
            while k < end and prefix[k] - prefix[left] < lower:
                k += 1
            while j < end and prefix[j] - prefix[left] <= upper:
                j += 1
            count += j - k
        
        # Merge
        temp = []
        i1, i2 = start, mid
        while i1 < mid and i2 < end:
            if prefix[i1] <= prefix[i2]:
                temp.append(prefix[i1])
                i1 += 1
            else:
                temp.append(prefix[i2])
                i2 += 1
        temp.extend(prefix[i1:mid])
        temp.extend(prefix[i2:end])
        prefix[start:end] = temp
        
        return count
    
    return merge_sort_count(0, n + 1)

# Example
print(count_range_sum([-2, 5, -1], -2, 2))  # 3
```

**Time:** O(n log n) | **Space:** O(n)

**Similar Problems:**
- Count of Smaller Numbers After Self
- Reverse Pairs

---

## Problem 4: Maximum Gap (LeetCode 122)

**Problem:** Find maximum difference between successive elements in sorted form. Must be O(n) time.

**Constraints:**
- 1 <= nums.length <= 10^5
- 0 <= nums[i] <= 10^9

**Approach (Bucket Sort / Pigeonhole Principle):**
1. If we use n+1 buckets for n elements, max gap must be between buckets
2. Sort into buckets by min/max values
3. Answer is max of (bucket[i].min - bucket[i-1].max)

```python
def maximum_gap(nums):
    if len(nums) < 2:
        return 0
    
    min_val, max_val = min(nums), max(nums)
    if min_val == max_val:
        return 0
    
    n = len(nums)
    bucket_size = max(1, (max_val - min_val) // (n - 1))
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
            continue
        max_gap = max(max_gap, bucket_min[i] - prev_max)
        prev_max = bucket_max[i]
    
    return max_gap

# Example
print(maximum_gap([3, 6, 9, 1]))  # 3
```

**Time:** O(n) | **Space:** O(n)

**Similar Problems:**
- Sort Colors (counting sort variant)
- Top K Frequent Elements

---

## Problem 5: First Missing Positive (LeetCode 41)

**Problem:** Find the smallest missing positive integer in unsorted array.

**Constraints:**
- Must run in O(n) time, O(1) space

**Approach (Cyclic Sort):**
1. For each index i, if nums[i] is in range [1, n], put it at index nums[i]-1
2. After rearranging, scan for first index where nums[i] != i+1

```python
def first_missing_positive(nums):
    n = len(nums)
    
    # Place each number in its correct position
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            correct_idx = nums[i] - 1
            nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
    
    # Find first missing
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    
    return n + 1

# Example
print(first_missing_positive([1, 2, 0]))  # 3
print(first_missing_positive([3, 4, -1, 1]))  # 2
print(first_missing_positive([7, 8, 9, 11, 12]))  # 1
```

**Time:** O(n) | **Space:** O(1)

**Similar Problems:**
- Missing Number
- Find All Numbers Disappeared in an Array
- Find the Duplicate Number

---

## Tips for Hard Problems

1. **Two pointer** is often the key for water trapping problems
2. **Monotonic stack** for range-based min/max problems
3. **Prefix sum + merge sort** for counting inversions/ranges
4. **Cyclic sort** for missing/first missing positive
5. **Bucket sort** for maximum gap (O(n) requirement)
6. Always ask: "Can I do better than O(n²)?"
7. Think about **space-time tradeoffs**: O(n) space for O(n) time
