# Two Sum Problems

## Master Overview: Two Sum Family

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                    TWO SUM PROBLEM FAMILY                                │
 ├────────────────────────────┬────────────┬──────────┬───────────────────┤
 │ Problem                    │ Time       │ Space    │ Key Technique     │
 ├────────────────────────────┼────────────┼──────────┼───────────────────┤
 │ Basic Two Sum (LeetCode 1) │ O(n)       │ O(n)     │ Hash map lookup   │
 │ Sorted Array (LeetCode 167)│ O(n)       │ O(1)     │ Two pointers      │
 │ Three Sum (LeetCode 15)    │ O(n²)     │ O(n)     │ Sort + 2-pointer  │
 │ Four Sum (LeetCode 18)     │ O(n³)     │ O(n)     │ Sort + 2 loops    │
 │ Subarray Sum = K (LeetCode │ O(n)       │ O(n)     │ Prefix sum + map  │
 │    560)                     │            │          │                   │
 │ Divisible by K (LeetCode   │ O(n)       │ O(k)     │ Remainder + map   │
 │    523)                     │            │          │                   │
 │ Min Subarray Sum (LC 209)  │ O(n)       │ O(1)     │ Sliding window    │
 └────────────────────────────┴────────────┴──────────┴───────────────────┘

 CORE IDEA: Use hash map to convert O(n²) pair search into O(n) lookup
```

## 1. Two Sum (LeetCode 1)

### Visual Walkthrough: Hash Map Approach

```
 INPUT: nums = [2, 7, 11, 15], target = 9

 STEP-BY-STEP:
 ┌──────┬───────┬────────────┬──────────────────────┬──────────────────┐
 │  i   │ num   │ complement │  seen (hash map)     │ found?           │
 ├──────┼───────┼────────────┼──────────────────────┼──────────────────┤
 │  0   │   2   │  9-2 = 7   │  {2: 0}              │ No, 7 not seen   │
 │  1   │   7   │  9-7 = 2   │  {2: 0}              │ YES! 2 in seen   │
 └──────┴───────┴────────────┴──────────────────────┴──────────────────┘

 OUTPUT: [0, 1]  (indices of 2 and 7)

 WHY THIS WORKS:
   For each num, check if (target - num) was seen before
   ┌───────────────────────────────────────────────────────┐
   │   We need: nums[i] + nums[j] = target                 │
   │   Rearrange: nums[j] = target - nums[i]              │
   │                                                       │
   │   At index j, check: is (target - nums[j]) in seen?  │
   │   If yes → we found our pair!                         │
   └───────────────────────────────────────────────────────┘
```

```python
def two_sum(nums, target):
    """
    Find two numbers that add up to target, return their indices.

    APPROACH: Hash map stores {num: index} as we iterate
    - For each num, compute complement = target - num
    - Check if complement is in hash map (O(1) lookup!)
    - If found → return both indices

    Time: O(n) — single pass, O(1) hash lookups
    Space: O(n) — hash map stores up to n elements
    """
    seen = {}  # key = number, value = index

    for i, num in enumerate(nums):
        complement = target - num    # What number do I need?

        if complement in seen:       # O(1) hash lookup!
            return [seen[complement], i]

        seen[num] = i                # Store for future lookups

    return []  # No solution found

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
print(two_sum([3, 2, 4], 6))        # [1, 2]
print(two_sum([3, 3], 6))           # [0, 1]
```

## 2. Two Sum II - Sorted Array (LeetCode 167)

### Visual: Two Pointer Approach

```
 INPUT: numbers = [2, 7, 11, 15], target = 9
 Array is SORTED → use two pointers!

 ┌─────┬─────┬─────┬─────┐
 │  2  │  7  │ 11  │ 15  │
 └──▲──┴─────┴─────┴──▲──┘
    │                 │
   left=0           right=3

 Step 1: left=0, right=3 → sum = 2+15 = 17 > 9 → move right left
 Step 2: left=0, right=2 → sum = 2+11 = 13 > 9 → move right left
 Step 3: left=0, right=1 → sum = 2+7  = 9  ✓  → FOUND!

 OUTPUT: [1, 2] (1-indexed!)

 WHY TWO POINTERS WORK ON SORTED ARRAY:
   - If sum too small → move left right (increase sum)
   - If sum too big  → move right left (decrease sum)
   - Time: O(n), Space: O(1) — no hash map needed!
```

```python
def two_sum_ii(numbers, target):
    """
    Find two numbers in SORTED array that add up to target.
    Returns 1-indexed positions.

    APPROACH: Two pointers from both ends
    - Sorted array lets us decide which pointer to move
    - Sum too small → move left right (bigger numbers)
    - Sum too big  → move right left (smaller numbers)

    Time: O(n) — single pass from both ends
    Space: O(1) — only two pointers, no extra data structure
    """
    left, right = 0, len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed!
        elif current_sum < target:
            left += 1     # Need bigger sum → move left right
        else:
            right -= 1    # Need smaller sum → move right left

    return []

# Test
print(two_sum_ii([2, 7, 11, 15], 9))  # [1, 2]
print(two_sum_ii([2, 3, 4], 6))        # [1, 3]
```

## 3. Three Sum (LeetCode 15)

### Visual Walkthrough

```
 INPUT: nums = [-1, 0, 1, 2, -1, -4]

 STEP 1: SORT → [-4, -1, -1, 0, 1, 2]

 STEP 2: Fix first element, two-pointer for remaining two:

   i=0, nums[i]=-4:         i=1, nums[i]=-1:
   [-4, -1, -1, 0, 1, 2]    [-4, -1, -1, 0, 1, 2]
    ▲   ▲            ▲        ▲  ▲           ▲
    i   L            R        i  L           R
   sum=-4-1+2=-3<0→L++     sum=-1-1+2=0✓ → [-1,-1,2]
   sum=-4-1+2=-3<0→L++     Skip duplicate: L++ R--
   sum=-4+0+2=-2<0→L++     sum=-1+0+1=0✓ → [-1,0,1]
   sum=-4+1+2=-1<0→L++     All done, i++

   i=2: nums[i]=-1 (same as prev) → SKIP (avoid duplicates!)

 OUTPUT: [[-1, -1, 2], [-1, 0, 1]]
```

```python
def three_sum(nums):
    """
    Find all unique triplets that sum to zero.

    APPROACH: Sort + Fix one + Two-pointer for other two
    1. Sort the array
    2. For each element nums[i], find pairs in remaining array that sum to -nums[i]
    3. Use two pointers (left=i+1, right=n-1) to find pairs
    4. Skip duplicates to avoid repeated triplets

    Time: O(n²) — O(n log n) sort + O(n) for each of n fixed elements
    Space: O(n) — for sorting (Python's Timsort)
    """
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        # SKIP DUPLICATES: Don't use same first element twice
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Two pointers to find two numbers that sum to -nums[i]
        left, right = i + 1, n - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])

                # SKIP DUPLICATES: Don't use same left/right twice
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1
            elif total < 0:
                left += 1      # Need bigger sum
            else:
                right -= 1     # Need smaller sum

    return result

# Test
print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1, -1, 2], [-1, 0, 1]]
print(three_sum([0, 0, 0]))               # [[0, 0, 0]]
```

## 4. Four Sum (LeetCode 18)

```python
def four_sum(nums, target):
    """
    Find all unique quadruplets that sum to target
    Time: O(n^3), Space: O(n)
    """
    nums.sort()
    result = []
    n = len(nums)
    
    for i in range(n - 3):
        # Skip duplicates
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        for j in range(i + 1, n - 2):
            # Skip duplicates
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            
            left, right = j + 1, n - 1
            
            while left < right:
                total = nums[i] + nums[j] + nums[left] + nums[right]
                
                if total == target:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    
                    left += 1
                    right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
    
    return result

# Test
print(four_sum([1, 0, -1, 0, -2, 2], 0))
# [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
```

## 5. Two Sum III - Data Structure Design (LeetCode 170)

```python
class TwoSum:
    """
    Design a data structure that supports:
    - add(value): Add value to internal data structure
    - find(value): Return true if any two numbers sum to value
    """
    
    def __init__(self):
        self.num_count = {}
    
    def add(self, value):
        self.num_count[value] = self.num_count.get(value, 0) + 1
    
    def find(self, value):
        for num in self.num_count:
            complement = value - num
            
            if complement in self.num_count:
                # Check if same element is used twice
                if complement != num or self.num_count[num] > 1:
                    return True
        
        return False

# Test
ts = TwoSum()
ts.add(1)
ts.add(3)
ts.add(5)
print(ts.find(4))   # True (1 + 3)
print(ts.find(7))   # True (2 + 5)
print(ts.find(10))  # False
```

## 6. Two Sum IV - BST (LeetCode 653)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_target(root, k):
    """
    Find if two nodes in BST sum to k
    Time: O(n), Space: O(n)
    """
    seen = set()
    
    def dfs(node):
        if not node:
            return False
        
        if (k - node.val) in seen:
            return True
        
        seen.add(node.val)
        
        return dfs(node.left) or dfs(node.right)
    
    return dfs(root)

# Build BST
#       5
#      / \
#     3   6
#    / \   \
#   2   4   7
root = TreeNode(5)
root.left = TreeNode(3)
root.right = TreeNode(6)
root.left.left = TreeNode(2)
root.left.right = TreeNode(4)
root.right.right = TreeNode(7)

print(find_target(root, 9))   # True (2 + 7 or 4 + 5)
print(find_target(root, 28))  # False
```

## 7. Subarray Sum Equals K (LeetCode 560)

### Visual: Prefix Sum + Hash Map

```
 INPUT: nums = [1, 1, 1], k = 2

 PREFIX SUMS: [0, 1, 2, 3]
               ▲
               │ empty prefix (sum = 0, count = 1)

 STEP-BY-STEP:
 ┌──────┬───────┬────────────┬────────────────────┬──────────────────┐
 │  i   │ num   │ prefix_sum │ seen (sum: count)  │ count +=         │
 ├──────┼───────┼────────────┼────────────────────┼──────────────────┤
 │ init │  ---  │     0      │ {0: 1}             │ ---              │
 │  0   │   1   │     1      │ {0:1, 1:1}         │ 1-2=-1 ∉ seen   │
 │  1   │   1   │     2      │ {0:1, 1:1, 2:1}    │ 2-2=0 ∈ seen ✓  │
 │  2   │   1   │     3      │ {0:1, 1:1, 2:1,3:1}│ 3-2=1 ∈ seen ✓  │
 └──────┴───────┴────────────┴────────────────────┴──────────────────┘

 FOUND:
   i=1: prefix_sum=2, need prefix_sum-k=0, seen at index before 0 → [0..1]
   i=2: prefix_sum=3, need prefix_sum-k=1, seen at index 0      → [1..2]

 OUTPUT: 2

 WHY THIS WORKS:
   If prefix_sum[j] - prefix_sum[i] = k
   → subarray from index i+1 to j sums to k
   → We store all prefix sums and check for (current_sum - k)
```

```python
def subarray_sum(nums, k):
    """
    Count subarrays with sum equal to k.

    KEY INSIGHT: prefix_sum[j] - prefix_sum[i] = k
    → subarray [i+1 .. j] sums to k
    → Store prefix sums in hash map, check for (current - k)

    Time: O(n) — single pass
    Space: O(n) — hash map stores prefix sums
    """
    count = 0
    prefix_sum = 0
    seen = {0: 1}    # Empty prefix has sum 0, appears once

    for num in nums:
        prefix_sum += num

        # How many earlier prefixes give us (prefix_sum - k)?
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]

        # Record this prefix sum
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1

    return count

# Test
print(subarray_sum([1, 1, 1], 2))          # 2
print(subarray_sum([1, 2, 3], 3))          # 2
print(subarray_sum([1, -1, 0], 0))         # 3
```

## 8. Continuous Subarray Sum (LeetCode 523)

### Visual: Remainder Pattern

```
 INPUT: nums = [23, 2, 4, 6, 7], k = 6

 KEY INSIGHT: If prefix_sum[j] % k == prefix_sum[i] % k
   → subarray [i+1..j] has sum divisible by k

 PREFIX SUMS:   0   23   25   29   35   42
 REMAINDERS %6: 0    5    1    5    5    0

 ┌──────┬───────┬────────────┬─────────────┬───────────────────┐
 │  i   │ num   │ prefix_sum │ remainder%6 │ seen (rem→index)  │
 ├──────┼───────┼────────────┼─────────────┼───────────────────┤
 │ init │  ---  │     0      │      0      │ {0: -1}           │
 │  0   │  23   │    23      │      5      │ {0:-1, 5:0}       │
 │  1   │   2   │    25      │      1      │ {0:-1, 5:0, 1:1}  │
 │  2   │   4   │    29      │      5      │ 5∈seen, 2-0=2≥2 ✓ │
 └──────┴───────┴────────────┴─────────────┴───────────────────┘

 FOUND: remainder 5 seen at index 0, again at index 2
        → subarray [1..2] = [2, 4], sum = 6, divisible by 6 ✓

 OUTPUT: True
```

```python
def check_subarray_sum(nums, k):
    """
    Check if there's a continuous subarray with sum divisible by k.

    KEY INSIGHT: Same remainder → subarray between them is divisible by k
    Proof: If (prefix[j] - prefix[i]) % k == 0
           → prefix[j] % k == prefix[i] % k

    Time: O(n) — single pass
    Space: O(k) — at most k different remainders
    """
    seen = {0: -1}     # Remainder 0 at "index" -1 (empty prefix)
    prefix_sum = 0

    for i, num in enumerate(nums):
        prefix_sum += num
        remainder = prefix_sum % k

        if remainder in seen:
            if i - seen[remainder] >= 2:    # Need at least 2 elements
                return True
        else:
            seen[remainder] = i             # First occurrence of this remainder

    return False

# Test
print(check_subarray_sum([23, 2, 4, 6, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 6))  # True
print(check_subarray_sum([23, 2, 6, 4, 7], 13)) # False
```

## 9. Count of Subarrays with Sum K

```python
def count_subarrays_with_sum_k(nums, k):
    """
    Count subarrays with sum exactly k
    Time: O(n), Space: O(n)
    """
    count = 0
    prefix_sum = 0
    seen = {0: 1}
    
    for num in nums:
        prefix_sum += num
        
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    
    return count

def subarrays_with_sum_k(nums, k):
    """Find all subarrays with sum k"""
    result = []
    prefix_sum = 0
    seen = {0: [-1]}
    
    for i, num in enumerate(nums):
        prefix_sum += num
        
        if prefix_sum - k in seen:
            for start in seen[prefix_sum - k]:
                result.append(nums[start + 1:i + 1])
        
        if prefix_sum not in seen:
            seen[prefix_sum] = []
        seen[prefix_sum].append(i)
    
    return result

# Test
print(count_subarrays_with_sum_k([1, 1, 1], 2))  # 2
print(subarrays_with_sum_k([1, 2, 3, 4, 5], 5))  # [[2, 3], [5]]
```

## 10. Minimum Size Subarray Sum (LeetCode 209)

### Visual: Sliding Window for Minimum Length

```
 INPUT: target = 7, nums = [2, 3, 1, 2, 4, 3]

 GOAL: Find shortest subarray with sum >= 7

 ┌─────┬─────┬─────┬─────┬─────┬─────┐
 │  2  │  3  │  1  │  2  │  4  │  3  │
 └─────┴─────┴─────┴─────┴─────┴─────┘

 Step 1: Expand right until sum >= 7
   [2,3,1,2] = 8 >= 7 → length 4

 Step 2: Try shrinking from left
   [3,1,2] = 6 < 7 → can't shrink more

 Step 3: Expand right again
   [3,1,2,4] = 10 >= 7 → length 4
   [1,2,4] = 7 >= 7 → length 3 ✓ (better!)
   [2,4] = 6 < 7 → stop shrinking

 Step 4: Expand right
   [2,4,3] = 9 >= 7 → length 3
   [4,3] = 7 >= 7 → length 2 ✓✓ (best!)
   [3] = 3 < 7 → stop

 OUTPUT: 2 (subarray [4,3])
```

```python
def min_subarray_len(target, nums):
    """
    Find minimal length of subarray with sum >= target.

    APPROACH: Sliding window
    - Expand right to increase sum
    - Shrink left when sum >= target (try to minimize length)
    - Track minimum length seen

    Time: O(n) — each element visited at most twice (once by right, once by left)
    Space: O(1) — just variables
    """
    left = 0
    total = 0
    min_len = float('inf')

    for right in range(len(nums)):
        total += nums[right]              # Expand window right

        while total >= target:            # Window valid → try to shrink
            min_len = min(min_len, right - left + 1)
            total -= nums[left]           # Shrink from left
            left += 1

    return min_len if min_len != float('inf') else 0

# Test
print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]))  # 2
```

## 11. Additional Two Sum Variants

```python
from collections import defaultdict

# Problem: Two Sum Less Than K (LeetCode 1099)
def two_sum_less_than_k(nums, k):
    """Find max sum of two elements less than k"""
    nums.sort()
    left, right = 0, len(nums) - 1
    max_sum = -1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum < k:
            max_sum = max(max_sum, current_sum)
            left += 1
        else:
            right -= 1
    
    return max_sum

# Problem: Max Number of K-Sum Pairs (LeetCode 1679)
def max_operations(nums, k):
    """Find max number of operations to make sum k"""
    count = Counter(nums)
    operations = 0
    
    for num in list(count.keys()):
        complement = k - num
        
        if complement in count:
            if num == complement:
                operations += count[num] // 2
                count[num] = 0
            else:
                pairs = min(count[num], count[complement])
                operations += pairs
                count[num] = 0
                count[complement] = 0
    
    return operations

# Problem: Subarray Product Less Than K (LeetCode 713)
def num_subarray_product_less_than_k(nums, k):
    """Count subarrays with product less than k"""
    if k <= 1:
        return 0
    
    count = 0
    product = 1
    left = 0
    
    for right in range(len(nums)):
        product *= nums[right]
        
        while product >= k:
            product //= nums[left]
            left += 1
        
        count += right - left + 1
    
    return count

# Test
print(two_sum_less_than_k([34, 23, 1, 24, 75, 33, 54, 8], 60))  # 58
print(max_operations([1, 2, 3, 4], 5))  # 2
print(num_subarray_product_less_than_k([10, 5, 2, 6], 100))  # 8
```

## Decision Guide: Which Two Sum Variant to Use?

```
 ┌─────────────────────────────────────────────────────────────────────┐
 │              TWO SUM DECISION FLOWCHART                             │
 ├─────────────────────────────────────────────────────────────────────┤
 │                                                                     │
 │  Need exactly 2 numbers summing to target?                         │
 │  ├─ YES → Is array sorted?                                         │
 │  │   ├─ YES → Two Pointers (O(n) time, O(1) space)                │
 │  │   └─ NO  → Hash Map (O(n) time, O(n) space)                    │
 │  │                                                                 │
 │  Need 3 numbers summing to 0?                                      │
 │  └─ YES → Sort + Fix one + Two-pointer (O(n²))                    │
 │                                                                     │
 │  Need 4 numbers summing to target?                                 │
 │  └─ YES → Sort + 2 nested loops + Two-pointer (O(n³))             │
 │                                                                     │
 │  Count subarrays with sum = k?                                     │
 │  └─ YES → Prefix Sum + Hash Map (O(n))                             │
 │                                                                     │
 │  Check if subarray sum divisible by k?                              │
 │  └─ YES → Remainder Pattern + Hash Map (O(n))                      │
 │                                                                     │
 │  Find minimum length subarray with sum >= target?                   │
 │  └─ YES → Sliding Window (O(n))                                    │
 │                                                                     │
 └─────────────────────────────────────────────────────────────────────┘
```
