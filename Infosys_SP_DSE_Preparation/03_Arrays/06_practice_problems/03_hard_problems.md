# Hard Practice Problems - Arrays — Detailed Guide

> **What makes these "hard"?** Easy/medium patterns (two pointer, hash map) still apply, but you need to combine them with advanced techniques like monotonic stacks, merge sort counting, or pigeonhole principle. The key is recognizing which pattern fits.

---

## Problem 1: Trapping Rain Water (LeetCode 42)

### Problem Statement

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Constraints:**
- `n == height.length`
- `0 <= n <= 2 * 10^4`
- `0 <= height[i] <= 10^5`

**Example 1:**
```
Input: height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Output: 6

Visual:
         │
     3   │         █
     2   │     █   █ █   █
     1   │ █ █ █ █ █ █ █ █ █
     0 ──█─█─█─█─█─█─█─█─█─█─█─█──
         0 1 2 3 4 5 6 7 8 9 10 11
         
Water trapped at each position:
Index:   0  1  2  3  4  5  6  7  8  9  10 11
Water:   0  0  1  0  1  2  1  0  1  0   0  0
         -  -  ▓  -  ▓  ▓  ▓  -  ▓  -   -  -
Total: 6 units of water
```

### Why Brute Force Fails

```
Brute Force: For each index, scan left max and right max → O(n²)
             Not acceptable for n = 20,000.

Prefix Array: Precompute left_max[] and right_max[] → O(n) time, O(n) space.
              Good, but we can do better with O(1) space.
```

### Approach 1: Two Pointer (Optimal)

**Key Insight:** At each position, water = `min(left_max, right_max) - height[i]`. Instead of precomputing max arrays, we maintain `left_max` and `right_max` as pointers move inward. The pointer with the SMALLER max is the bottleneck — it determines the water level.

```
Why move the pointer with smaller max?
┌─────────────────────────────────────────────────────┐
│ If left_max < right_max:                           │
│   - Water at left = min(left_max, right_max) - h   │
│                    = left_max - height[left]        │
│   - We KNOW the right side has a wall ≥ right_max  │
│     which is ≥ left_max, so water is guaranteed.   │
│   - We can safely compute water for position left. │
│                                                     │
│ If we moved right instead:                          │
│   - Water at right = min(left_max, right_max) - h  │
│                    = left_max - height[right]       │
│   - But we DON'T know if there's a wall on the LEFT│
│     tall enough. We'd need to scan left → O(n²).   │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step Walkthrough

```
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
          0  1  2  3  4  5  6  7  8  9 10 11

left=0, right=11, left_max=0, right_max=0, water=0

Step 1:  height[0]=0 < height[11]=1
         height[0]=0 >= left_max=0 → left_max=0 (no water, just updating max)
         left=1

Step 2:  height[1]=1 < height[11]=1? No, equal
         height[11]=1 >= right_max=0 → right_max=1
         right=10

Step 3:  height[1]=1 < height[10]=2? Yes
         height[1]=1 >= left_max=0 → left_max=1
         left=2

Step 4:  height[2]=0 < height[10]=2? Yes
         height[2]=0 < left_max=1 → water += 1-0 = 1
         left=3

Step 5:  height[3]=2 < height[10]=2? No, equal
         height[10]=2 >= right_max=1 → right_max=2
         right=9

Step 6:  height[3]=2 >= left_max=1 → left_max=2
         left=4

Step 7:  height[4]=1 < height[9]=1? No, equal
         height[9]=1 < right_max=2 → water += 2-1 = 1 (total=2)
         right=8

Step 8:  height[4]=1 < height[8]=2? Yes
         height[4]=1 < left_max=2 → water += 2-1 = 1 (total=3)
         left=5

Step 9:  height[5]=0 < height[8]=2? Yes
         height[5]=0 < left_max=2 → water += 2-0 = 2 (total=5)
         left=6

Step 10: height[6]=1 < height[8]=2? Yes
         height[6]=1 < left_max=2 → water += 2-1 = 1 (total=6)
         left=7

Step 11: height[7]=3 >= left_max=2 → left_max=3
         left=8

left=8, right=8 → STOP

Final water = 6 ✓
```

### Visual Walkthrough

```
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

         │         
     3   │         █
     2   │     █   █ █   █
     1   │ █ █ █ █ █ █ █ █ █
     0 ──█─█─█─█─█─█─█─█─█─█─█─█──

left→                        ←right
l_max=0                      r_max=0

After Step 3 (left moves to 2, left_max becomes 1):
     Water at index 2 = left_max(1) - height(0) = 1  ▓

After Steps 5-6 (right_max becomes 2):
     Water at index 9 = right_max(2) - height(1) = 1  ▓

After Steps 8-10 (left_max stays 2):
     Water at index 4 = 2-1=1 ▓
     Water at index 5 = 2-0=2 ▓▓
     Water at index 6 = 2-1=1 ▓

     Total: 1 + 1 + 1 + 2 + 1 = 6 ✓
```

### The Code (Two Pointer):
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

### Approach 2: Stack

**Key Insight:** Use a monotonic decreasing stack. When we find a taller bar, we pop shorter bars and calculate water trapped for each.

```
Stack processes bars left to right:
- Push bars onto stack (decreasing heights)
- When a taller bar appears, pop and calculate water for each popped bar

For popped bar 'bottom':
  water = width × (min(current_height, stack_top_height) - bottom_height)
  width = current_index - stack_top_index - 1
```

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

### Common Mistakes
- **Mistake:** Confusing "water" with "area" — water is trapped BETWEEN bars, not on bars.
- **Mistake:** Using `<=` instead of `<` when comparing heights in the stack approach.
- **Mistake:** Forgetting the empty height check at the start.
- **Edge case:** `[4, 2, 0, 3, 2, 5]` → 9 units of water.
- **Edge case:** Empty array → return 0.

**Time:** O(n) | **Space:** O(1) two-pointer / O(n) stack

**Similar Problems:**
- Container With Most Water
- Largest Rectangle in Histogram
- Maximal Rectangle

---

## Problem 2: Maximum Subarray Min-Product (LeetCode 1856)

### Problem Statement

The **min-product** of an array is defined as the minimum value in the array multiplied by the sum of the array. Given an integer array `nums`, return the maximum min-product of any non-empty subarray. Return the answer modulo `10^9 + 7`.

**Constraints:**
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^7`

**Example:**
```
Input: nums = [1, 2, 3, 2]
Output: 14

Explanation:
  Subarray [1,2,3,2]: min=1, sum=8 → 1×8=8
  Subarray [2,3,2]:   min=2, sum=7 → 2×7=14 ← MAX
  Subarray [3,2]:     min=2, sum=5 → 2×5=10
  Subarray [1,2,3]:   min=1, sum=6 → 1×6=6
  Subarray [2,3]:     min=2, sum=5 → 2×5=10
  Subarray [3]:       min=3, sum=3 → 3×3=9
```

### Why Brute Force Fails

```
Brute Force: For each subarray [i..j], find min and sum → O(n³)
             With prefix sums: O(n²) — still too slow for n=10⁵.
```

### Approach: Monotonic Stack + Prefix Sum

**Key Insight:** For each element `nums[i]`, find the RANGE where it is the minimum. Then compute `min × sum_of_range` for each element and take the max.

```
Why this works:
┌─────────────────────────────────────────────────┐
│ For any subarray, the min-product is determined │
│ by the MINIMUM element in that subarray.       │
│                                                 │
│ So for each element, if we find the LARGEST    │
│ range where it is the minimum, we can compute  │
│ the min-product for that range.                 │
│                                                 │
│ The answer is the max across all elements.     │
└─────────────────────────────────────────────────┘
```

### Step-by-Step Walkthrough

```
nums = [1, 2, 3, 2]

Step 1: Prefix sums
  prefix = [0, 1, 3, 6, 8]
  prefix[i] = sum of nums[0..i-1]

Step 2: Find LEFT boundary for each element
  (first element to the LEFT that is SMALLER)
  
  i=0: nums[0]=1, stack empty → left[0]=-1, push 0
  i=1: nums[1]=2, stack top=0 (nums[0]=1 < 2) → left[1]=0, push 1
  i=2: nums[2]=3, stack top=1 (nums[1]=2 < 3) → left[2]=1, push 2
  i=3: nums[3]=2, stack top=2 (nums[2]=3 >= 2) POP
       stack top=1 (nums[1]=2 >= 2) POP
       stack top=0 (nums[0]=1 < 2) → left[3]=0, push 3
  
  left = [-1, 0, 1, 0]

Step 3: Find RIGHT boundary for each element
  (first element to the RIGHT that is SMALLER or EQUAL)
  
  i=3: nums[3]=2, stack empty → right[3]=4, push 3
  i=2: nums[2]=3, stack top=3 (nums[3]=2 < 3) → right[2]=3, push 2
  i=1: nums[1]=2, stack top=2 (nums[2]=3 > 2) POP
       stack top=3 (nums[3]=2 >= 2) POP
       stack empty → right[1]=4, push 1
  i=0: nums[0]=1, stack top=1 (nums[1]=2 > 1) → right[0]=1, push 0
  
  right = [1, 4, 3, 4]

Step 4: Compute min-product for each element
  i=0: range = [0..0], sum = prefix[1]-prefix[0] = 1,   prod = 1×1 = 1
  i=1: range = [1..3], sum = prefix[4]-prefix[1] = 7,   prod = 2×7 = 14 ← MAX
  i=2: range = [2..2], sum = prefix[3]-prefix[2] = 3,   prod = 3×3 = 9
  i=3: range = [1..3], sum = prefix[4]-prefix[1] = 7,   prod = 2×7 = 14

Result: 14 ✓
```

### Visual

```
nums = [1, 2, 3, 2]

For nums[1]=2:
  Left boundary: index 0 (value 1, which is smaller)
  Right boundary: index 4 (out of bounds)
  
  Range where 2 is minimum: [1, 2, 3]
                              ↑
                           nums[1]=2 is min
  
  Range sum = 2+3+2 = 7
  Min-product = 2 × 7 = 14

  ┌─────────────────────┐
  │  [1, 2, 3, 2]      │
  │     ↑              │
  │  min=2 in [1..3]   │
  │  sum=7, prod=14    │
  └─────────────────────┘
```

### The Code:
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

### Common Mistakes
- **Mistake:** Using `>=` in both left AND right boundary searches → double-counts equal elements.
  - Use `>=` for left, `>` for right (or vice versa) to handle duplicates correctly.
- **Mistake:** Forgetting modulo operation — result can overflow.
- **Mistake:** Off-by-one in prefix sum indexing (`prefix[right[i]] - prefix[left[i]+1]`).
- **Edge case:** All elements same → answer = `n × nums[0]`.
- **Edge case:** Single element → answer = `nums[0] × nums[0]`.

**Time:** O(n) | **Space:** O(n)

**Similar Problems:**
- Largest Rectangle in Histogram
- Sum of Subarray Minimums

---

## Problem 3: Count of Range Sum (LeetCode 327)

### Problem Statement

Given an integer array `nums` and two integers `lower` and `upper`, return the number of range sums that lie in `[lower, upper]` inclusive. Range sum `S(i, j)` is defined as the sum of the elements in `nums` between indices `i` and `j` inclusive.

**Constraints:**
- `-2^31 <= nums[i] <= 2^31 - 1`
- `0 <= nums.length <= 10^5`
- `-10^9 <= lower <= upper <= 10^9`

**Example:**
```
Input: nums = [-2, 5, -1], lower = -2, upper = 2
Output: 3

Range sums:
  S(0,0) = -2   → in [-2,2] ✓
  S(0,1) = 3    → not in range
  S(0,2) = 2    → in [-2,2] ✓
  S(1,1) = 5    → not in range
  S(1,2) = 4    → not in range
  S(2,2) = -1   → in [-2,2] ✓

Total: 3 range sums
```

### Why Brute Force Fails

```
Brute Force: Compute all O(n²) subarray sums, check each → O(n²)
             Too slow for n=10⁵.

Key Insight: Subarray sum S(i,j) = prefix[j+1] - prefix[i]
             We need to count pairs (i, j) where:
               lower <= prefix[j+1] - prefix[i] <= upper
             This is like counting "inversions in a range".
```

### Approach: Prefix Sum + Modified Merge Sort

**Key Insight:** Convert the problem to counting pairs in prefix sum array where `prefix[j] - prefix[i]` is in `[lower, upper]`. Use modified merge sort to count these pairs in O(n log n).

```
Why merge sort works here:
┌─────────────────────────────────────────────────────┐
│ During merge, the left and right halves are sorted. │
│ For each element in left half, we can use two       │
│ pointers to count how many elements in the right    │
│ half satisfy:                                       │
│   lower <= right[j] - left[i] <= upper             │
│                                                     │
│ Since both halves are sorted, we can advance the    │
│ pointers efficiently → O(n) per merge level        │
│ → O(n log n) total.                                │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step Walkthrough

```
nums = [-2, 5, -1], lower = -2, upper = 2

Step 1: Compute prefix sums
  prefix = [0, -2, 3, 2]
           indices: 0  1  2  3

Step 2: We need to count pairs (i, j) where i < j and
        lower <= prefix[j] - prefix[i] <= upper
        
  All pairs (i,j) with i < j:
    (0,1): prefix[1]-prefix[0] = -2-0 = -2  → in range ✓
    (0,2): prefix[2]-prefix[0] = 3-0 = 3    → not in range
    (0,3): prefix[3]-prefix[0] = 2-0 = 2    → in range ✓
    (1,2): prefix[2]-prefix[1] = 3-(-2) = 5 → not in range
    (1,3): prefix[3]-prefix[1] = 2-(-2) = 4 → not in range
    (2,3): prefix[3]-prefix[2] = 2-3 = -1   → in range ✓
    
  Count: 3 ✓

The merge sort counts these without enumerating all pairs.
```

### The Code:
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

### Common Mistakes
- **Mistake:** Forgetting the empty prefix `prefix[0] = 0` — it represents the sum before the array starts.
- **Mistake:** Off-by-one in the `while` loops — `k` finds first index where `prefix[k] - prefix[left] >= lower`, `j` finds first index where `prefix[j] - prefix[left] > upper`.
- **Mistake:** Not modifying the prefix array during merge — the sorted order is needed for the two-pointer counting to work.
- **Edge case:** Empty array → return 0.
- **Edge case:** `lower == upper` — still counts valid subarrays.
- **Edge case:** All zeros with `lower=0, upper=0` → every subarray counts.

**Time:** O(n log n) | **Space:** O(n)

**Similar Problems:**
- Count of Smaller Numbers After Self
- Reverse Pairs

---

## Problem 4: Maximum Gap (LeetCode 122)

### Problem Statement

Given an integer array `nums`, return the maximum difference between two successive elements in its sorted form. If the array contains less than two elements, return 0. You must solve it in O(n) time.

**Constraints:**
- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`

**Example:**
```
Input: nums = [3, 6, 9, 1]
Sorted: [1, 3, 6, 9]
Gaps:   2  3  3
Maximum gap: 3
```

### Why Brute Force Fails

```
Brute Force: Sort → O(n log n), scan gaps → O(n)
             But the problem REQUIRES O(n) time!
             
             Even if we use counting/radix sort, values up to 10^9
             make counting sort infeasible.
```

### Approach: Bucket Sort (Pigeonhole Principle)

**Key Insight:** If we create `n-1` buckets to cover the range `[min, max]`, the maximum gap MUST occur between buckets (not within a bucket). This is because by pigeonhole principle, if all elements fit in `n-1` buckets, at least one bucket is empty, creating a gap.

```
Why max gap is between buckets:
┌─────────────────────────────────────────────────────┐
│ Range = max_val - min_val                           │
│ Bucket count = n - 1                                │
│ Bucket size = ceil(range / (n-1))                   │
│                                                     │
│ If bucket_size = range / (n-1), then:               │
│   n elements in n-1 buckets → at least 1 empty     │
│   All elements within a bucket are ≤ bucket_size    │
│   apart. So the max gap can't be within a bucket.  │
│                                                     │
│ Therefore: max gap = max of (bucket[i].min -        │
│                              bucket[i-1].max)      │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step Walkthrough

```
nums = [3, 6, 9, 1]

Step 1: Find range
  min_val = 1, max_val = 9
  range = 9 - 1 = 8

Step 2: Create buckets
  bucket_count = n - 1 = 3 buckets
  bucket_size = ceil(8 / 3) = 3 (approximately)
  
  Bucket 0: covers [1, 3]  → elements: 1, 3
  Bucket 1: covers [4, 6]  → elements: 6
  Bucket 2: covers [7, 9]  → elements: 9

Step 3: Record min/max per bucket
  Bucket 0: min=1, max=3
  Bucket 1: min=6, max=6
  Bucket 2: min=9, max=9

Step 4: Compute gaps between consecutive non-empty buckets
  Gap 1: bucket[1].min - bucket[0].max = 6 - 3 = 3
  Gap 2: bucket[2].min - bucket[1].max = 9 - 6 = 3
  
  Max gap = 3 ✓
```

### Visual

```
nums = [3, 6, 9, 1]
Sorted: [1, 3, 6, 9]

Number line:
  1    2    3    4    5    6    7    8    9
  ●───────────●──────────────────●───────────●
  |  Bucket 0  |    Bucket 1     |  Bucket 2  |
  | min=1,max=3|  min=6,max=6    | min=9,max=9|
  
Gaps:
  bucket[0].max=3  →  bucket[1].min=6  →  gap = 3
  bucket[1].max=6  →  bucket[2].min=9  →  gap = 3
  
Max gap = 3 ✓
```

### The Code:
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

### Common Mistakes
- **Mistake:** Using `bucket_count = n` instead of `n-1` — the pigeonhole principle requires `n-1` buckets.
- **Mistake:** Forgetting to handle `min_val == max_val` (all same elements) — return 0.
- **Mistake:** Using `int` division without `max(1, ...)` — bucket size can't be 0.
- **Edge case:** Two elements → gap = difference between them.
- **Edge case:** `[1, 1000000000]` → gap = 999999999 (large values, but still O(n)).
- **Edge case:** All same values → return 0.

**Time:** O(n) | **Space:** O(n)

**Similar Problems:**
- Sort Colors (counting sort variant)
- Top K Frequent Elements

---

## Problem 5: First Missing Positive (LeetCode 41)

### Problem Statement

Given an unsorted integer array `nums`, return the smallest missing positive integer. You must implement an algorithm that runs in O(n) time and uses O(1) extra space.

**Constraints:**
- `1 <= nums.length <= 10^5`
- `-2^31 <= nums[i] <= 2^31 - 1`

**Example 1:**
```
Input: nums = [1, 2, 0]
Output: 3
Explanation: 1 and 2 are present, 3 is missing.

Example 2:
Input: nums = [3, 4, -1, 1]
Output: 2
Explanation: 1 is present, 2 is missing.

Example 3:
Input: nums = [7, 8, 9, 11, 12]
Output: 1
Explanation: No positive integer <= 5 is present.
```

### Why Brute Force Fails

```
Brute Force (Hash Set): Put all numbers in a set, check 1, 2, 3... → O(n) time, O(n) space
                         Violates O(1) space requirement!

Brute Force (Sort): Sort, scan for gap → O(n log n) time
                     Violates O(n) time requirement!
```

### Approach: Cyclic Sort (In-Place Rearrangement)

**Key Insight:** The answer must be in `[1, n+1]` for an array of size `n`. We can rearrange the array so that `nums[i] = i+1` for valid positive integers. Then scan for the first position where `nums[i] != i+1`.

```
The algorithm:
┌─────────────────────────────────────────────────────┐
│ For each index i:                                   │
│   If nums[i] is in range [1, n] and                 │
│   nums[i] is not already at its correct position    │
│   (nums[nums[i]-1] != nums[i]):                     │
│     SWAP nums[i] with nums[nums[i]-1]              │
│                                                     │
│ After all swaps:                                    │
│   nums[0] should be 1                               │
│   nums[1] should be 2                               │
│   ...                                               │
│   nums[n-1] should be n                             │
│                                                     │
│ Scan for first i where nums[i] != i+1 → answer=i+1 │
│ If all match → answer = n+1                         │
└─────────────────────────────────────────────────────┘
```

### Step-by-Step Walkthrough

```
Example: nums = [3, 4, -1, 1]

Step 1: i=0, nums[0]=3
  3 is in [1,4]? Yes
  nums[3-1] = nums[2] = -1 ≠ 3? Yes → swap
  nums = [-1, 4, 3, 1]
  i stays at 0 (don't increment, need to check swapped value)

Step 2: i=0, nums[0]=-1
  -1 is in [1,4]? No → move to next
  i=1

Step 3: i=1, nums[1]=4
  4 is in [1,4]? Yes
  nums[4-1] = nums[3] = 1 ≠ 4? Yes → swap
  nums = [-1, 1, 3, 4]
  i stays at 1

Step 4: i=1, nums[1]=1
  1 is in [1,4]? Yes
  nums[1-1] = nums[0] = -1 ≠ 1? Yes → swap
  nums = [1, -1, 3, 4]
  i stays at 1

Step 5: i=1, nums[1]=-1
  -1 is in [1,4]? No → move to next
  i=2

Step 6: i=2, nums[2]=3
  3 is in [1,4]? Yes
  nums[3-1] = nums[2] = 3 = 3 → already correct, move on
  i=3

Step 7: i=3, nums[3]=4
  4 is in [1,4]? Yes
  nums[4-1] = nums[3] = 4 = 4 → already correct, move on
  i=4 → STOP

Final array: [1, -1, 3, 4]

Step 8: Scan for first missing positive
  nums[0]=1 = 0+1 ✓
  nums[1]=-1 ≠ 1+1=2 ✗ → ANSWER = 2 ✓
```

### Visual

```
Initial:    [3, 4, -1, 1]

After swap:  [-1, 4, 3, 1]   ← swapped 3↔-1
After swap:  [-1, 1, 3, 4]   ← swapped 4↔1
After swap:  [1, -1, 3, 4]   ← swapped 1↔-1

Final positions:
  Index:  0   1   2   3
  Value:  1  -1   3   4
          ✓       ✓   ✓
              ↑
          Should be 2, but it's -1
          → Answer: 2 ✓
```

### The Code:
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
print(first_missing_positive([1, 2, 0]))         # 3
print(first_missing_positive([3, 4, -1, 1]))     # 2
print(first_missing_positive([7, 8, 9, 11, 12])) # 1
```

### Common Mistakes
- **Mistake:** Incrementing `i` after a swap — you must check the swapped value at the same position.
- **Mistake:** Using `while nums[i] != i + 1` without the range check — infinite loop if `nums[i]` is out of bounds.
- **Mistake:** Forgetting that the answer can be `n+1` (all numbers 1..n are present).
- **Edge case:** `[1]` → answer = 2.
- **Edge case:** `[-1, -2, -3]` → answer = 1 (no positive integers at all).
- **Edge case:** `[1, 2, 3]` → answer = 4 (all present, answer is n+1).
- **Edge case:** Duplicates like `[1, 1]` → answer = 2 (the second 1 stays out of place).

**Time:** O(n) | **Space:** O(1)

**Similar Problems:**
- Missing Number (uses XOR or sum)
- Find All Numbers Disappeared in an Array
- Find the Duplicate Number (cycle detection variant)

---

## Summary Table

| # | Problem | Key Technique | Time | Space | Difficulty |
|---|---------|---------------|------|-------|------------|
| 1 | Trapping Rain Water | Two Pointer / Stack | O(n) | O(1) / O(n) | Classic Hard |
| 2 | Max Subarray Min-Product | Monotonic Stack + Prefix Sum | O(n) | O(n) | Stack Pattern |
| 3 | Count of Range Sum | Prefix Sum + Merge Sort | O(n log n) | O(n) | Divide & Conquer |
| 4 | Maximum Gap | Bucket Sort / Pigeonhole | O(n) | O(n) | Sorting Trick |
| 5 | First Missing Positive | Cyclic Sort | O(n) | O(1) | In-Place Swap |

---

## Key Patterns for Hard Array Problems

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. MONOTONIC STACK                                               │
│    When: You need to find "next greater/smaller" for each element│
│    Examples: Rain Water, Min-Product, Largest Rectangle           │
│                                                                   │
│ 2. PREFIX SUM + SORTING                                           │
│    When: Subarray sums with range constraints                    │
│    Examples: Count Range Sum, Subarray Sum Equals K               │
│                                                                   │
│ 3. BUCKET SORT (Pigeonhole)                                      │
│    When: O(n) time required AND values are bounded                │
│    Examples: Maximum Gap, Sort Colors                             │
│                                                                   │
│ 4. CYCLIC SORT (In-Place Rearrangement)                          │
│    When: Find missing/duplicate in [1,n] with O(1) space         │
│    Examples: First Missing Positive, Find Duplicate               │
│                                                                   │
│ 5. TWO POINTER with STATE                                         │
│    When: Two pointers maintain "max seen so far"                  │
│    Examples: Trapping Rain Water                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes & Edge Cases (All Hard Problems)

### General
- **Mistake:** Not reading constraints carefully — many hard problems have specific O(n) time or O(1) space requirements.
- **Mistake:** Skipping edge cases — empty arrays, single elements, all same values.

### Trapping Rain Water
- **Mistake:** Treating bars as "filled" — water is BETWEEN bars, not on them.
- **Mistake:** In stack approach, using `<=` instead of `<` when popping.

### Maximum Subarray Min-Product
- **Mistake:** Off-by-one in prefix sum calculation.
- **Mistake:** Using same comparison for both left and right boundaries.

### Count of Range Sum
- **Mistake:** Not including `prefix[0] = 0` in the prefix array.
- **Mistake:** Not merging the prefix array during merge sort.

### Maximum Gap
- **Mistake:** Using `n` buckets instead of `n-1` buckets.
- **Mistake:** Not handling the case where all elements are the same.

### First Missing Positive
- **Mistake:** Incrementing index after swap instead of rechecking.
- **Mistake:** Not checking range `[1, n]` before swapping.

---

## Tips for Hard Problems

1. **Two pointer** is often the key for water trapping problems
2. **Monotonic stack** for range-based min/max problems
3. **Prefix sum + merge sort** for counting inversions/ranges
4. **Cyclic sort** for missing/first missing positive
5. **Bucket sort** for maximum gap (O(n) requirement)
6. Always ask: "Can I do better than O(n²)?"
7. Think about **space-time tradeoffs**: O(n) space for O(n) time
8. **Read constraints first** — they often hint at the approach (e.g., "O(1) space" → in-place rearrangement)
9. **Practice the patterns** — hard problems are combinations of known patterns applied in new ways
