# Complete Two Pointer Technique Guide - Detailed Version

## What is Two Pointer?

Two pointer uses **two indices** moving through an array to solve problems in O(n) instead of O(n²).

**When to use:**
- Sorted array (strongest signal!)
- Pair/triplet finding
- Palindrome checking
- Partition problems
- Container/water problems

---

## 1. Opposite Direction Two Pointer

**Pattern:** Left starts at 0, right starts at end. Move inward.

### Example: Pair Sum in Sorted Array

**Problem:** Find two numbers that add up to target.

**Input:** nums = [2, 7, 11, 15], target = 9

### Visual Walkthrough:

```
Initial: [2, 7, 11, 15]
          ↑           ↑
         left       right

Sum = 2 + 15 = 17 > 9 → move right left

[2, 7, 11, 15]
  ↑        ↑
 left    right

Sum = 2 + 11 = 13 > 9 → move right left

[2, 7, 11, 15]
  ↑     ↑
 left right

Sum = 2 + 7 = 9 ✓ FOUND!

Return [left+1, right+1] = [1, 2]
```

### The Code:
```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        
        if curr_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif curr_sum < target:
            left += 1      # Need bigger sum, move left forward
        else:
            right -= 1     # Need smaller sum, move right backward
    
    return [-1, -1]  # Not found
```

**Why it works:**
- Array is sorted
- If sum < target: left pointer must increase
- If sum > target: right pointer must decrease

**Time:** O(n) | **Space:** O(1)

---

## 2. Same Direction Two Pointer (Fast/Slow)

**Pattern:** Both start at same end. Fast explores, slow catches up.

### Example: Remove Duplicates from Sorted Array

**Problem:** Remove duplicates in-place, return new length.

**Input:** nums = [1, 1, 2, 3, 3, 4]

### Visual Walkthrough:

```
Initial: slow=0, fast=1
[1, 1, 2, 3, 3, 4]
 ↑  ↑
slow fast

fast=1: nums[1]==nums[0] (both 1), skip
        [1, 1, 2, 3, 3, 4]
        ↑  ↑
      slow fast (no change)

fast=2: nums[2]!=nums[0] (2≠1)
        slow=1, nums[1]=2
        [1, 2, 2, 3, 3, 4]
           ↑     ↑
         slow   fast

fast=3: nums[3]!=nums[1] (3≠2)
        slow=2, nums[2]=3
        [1, 2, 3, 3, 3, 4]
              ↑        ↑
            slow      fast

fast=4: nums[4]==nums[2] (both 3), skip

fast=5: nums[5]!=nums[2] (4≠3)
        slow=3, nums[3]=4
        [1, 2, 3, 4, 3, 4]
              ↑           ↑
            slow         fast

Result: [1, 2, 3, 4, _, _], return slow+1 = 4
```

### The Code:
```python
def remove_duplicates(nums):
    if not nums:
        return 0
    
    slow = 0  # Points to last unique element
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1
```

**Key Insight:**
- `slow` always points to the last unique element
- `fast` explores new elements
- When fast finds new unique, slow moves forward to place it

**Time:** O(n) | **Space:** O(1)

---

## 3. Dutch National Flag (Three Way Partition)

**Problem:** Sort array with only 0s, 1s, and 2s.

**Input:** nums = [2, 0, 2, 1, 1, 0]

### The Code:
```python
def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

### Visual Walkthrough:

```
Initial: [2, 0, 2, 1, 1, 0]
          ↑        ↑        ↑
         low      mid     high

Regions:
[0..low-1] = 0s (red)
[low..mid-1] = 1s (white)
[mid..high] = unknown (to be processed)
[high+1..] = 2s (blue)

Step 1: mid=0, nums[0]=2
        Swap with high, high--
        [0, 0, 2, 1, 1, 2]
          ↑     ↑     ↑
         low   mid  high

Step 2: mid=0, nums[0]=0
        Swap with low, low++, mid++
        [0, 0, 2, 1, 1, 2]
            ↑     ↑     ↑
          low   mid   high

Step 3: mid=1, nums[1]=0
        Swap with low, low++, mid++
        [0, 0, 2, 1, 1, 2]
              ↑  ↑     ↑
            low mid   high

Step 4: mid=2, nums[2]=2
        Swap with high, high--
        [0, 0, 1, 1, 2, 2]
              ↑  ↑  ↑
            low mid high

Step 5: mid=2, nums[2]=1
        Just mid++
        [0, 0, 1, 1, 2, 2]
              ↑     ↑  ↑
            low   mid high

Step 6: mid=3, nums[3]=1
        Just mid++
        [0, 0, 1, 1, 2, 2]
              ↑        ↑  ↑
            low      mid high

Step 7: mid=4, mid > high → STOP

Result: [0, 0, 1, 1, 2, 2] ✓
```

**Time:** O(n) | **Space:** O(1) | **One pass!**

---

## 4. Container With Most Water

**Problem:** Find two lines that together with x-axis form a container that holds the most water.

**Input:** height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

### Visual:

```
8 |     █           █
7 |     █           █   █
6 |     █   █       █   █
5 |     █   █   █   █   █
4 |     █   █   █   █   █
3 |     █   █   █   █   █ █
2 |     █   █ █ █   █   █ █
1 | █   █   █ █ █   █   █ █
  +---+---+---+---+---+---+---+---+--
    0   1   2   3   4   5   6   7   8
```

### The Code:
```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate water at current position
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        
        # Move the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water
```

### Why move the shorter line?

```
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]

left=0 (height=1), right=8 (height=7)
Water = min(1, 7) * 8 = 8

If we move right (taller one):
  left=0 (height=1), right=7 (height=3)
  Water = min(1, 3) * 7 = 7 (DECREASED!)

If we move left (shorter one):
  left=1 (height=8), right=8 (height=7)
  Water = min(8, 7) * 7 = 49 (INCREASED!)

Moving shorter line might find taller line → more water!
Moving taller line can only decrease water (width decreases)
```

**Time:** O(n) | **Space:** O(1)

---

## 5. Trapping Rain Water

**Problem:** Calculate how much water can be trapped after rain.

**Input:** height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

### Visual:

```
3 |                 █
2 |         █   █   █ █   █
1 |     █   █ █ █ █ █ █ █ █ █
0 | █   █ █ █ █ █ █ █ █ █ █ █
  +---+---+---+---+---+---+---+---+---+---+---+--
    0   1   2   3   4   5   6   7   8   9  10  11

Water at each position = min(left_max, right_max) - height
```

### The Code (Two Pointer):
```python
def trap_rain_water(height):
    if not height:
        return 0
    
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            # Water depends on left_max
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            # Water depends on right_max
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```

### Key Insight:
```
Water at position i = min(left_max[i], right_max[i]) - height[i]

left_max[i] = max(height[0..i])
right_max[i] = max(height[i..n-1])

For index 5 (height=0):
left_max = max(0,1,0,2,1) = 2
right_max = max(0,1,3,2,1,2,1) = 3
Water = min(2, 3) - 0 = 2
```

**Time:** O(n) | **Space:** O(1)

---

## 6. 3Sum

**Problem:** Find all unique triplets that sum to zero.

**Input:** nums = [-1, 0, 1, 2, -1, -4]

### The Code:
```python
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    
    return result
```

### Visual Walkthrough:

```
nums = [-1, 0, 1, 2, -1, -4]
After sort: [-4, -1, -1, 0, 1, 2]

i=0 (nums[i]=-4):
  left=1 (-1), right=5 (2)
  sum = -4 + -1 + 2 = -3 < 0 → left++
  left=2 (-1), right=5 (2)
  sum = -4 + -1 + 2 = -3 < 0 → left++
  left=3 (0), right=5 (2)
  sum = -4 + 0 + 2 = -2 < 0 → left++
  left=4 (1), right=5 (2)
  sum = -4 + 1 + 2 = -1 < 0 → left++
  left=5, STOP

i=1 (nums[i]=-1):
  left=2 (-1), right=5 (2)
  sum = -1 + -1 + 2 = 0 ✓ FOUND!
  Add [-1, -1, 2]
  
  left=3 (0), right=4 (1)
  sum = -1 + 0 + 1 = 0 ✓ FOUND!
  Add [-1, 0, 1]

i=2 (nums[i]=-1): Skip (same as i=1)

Result: [[-1, -1, 2], [-1, 0, 1]]
```

**Time:** O(n²) | **Space:** O(1) excluding output

---

## 7. Valid Palindrome

**Problem:** Check if string is palindrome (alphanumeric only).

**Input:** "A man, a plan, a canal: Panama"

### The Code:
```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare characters
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

### Visual Walkthrough:

```
s = "A man, a plan, a canal: Panama"

Ignore non-alphanumeric:
a m a n a p l a n a c a n a l p a n a m a

left=0 (a), right=20 (a): equal ✓
left=1 (m), right=19 (m): equal ✓
left=2 (a), right=18 (a): equal ✓
...
All match! → Palindrome ✓
```

**Time:** O(n) | **Space:** O(1)

---

## 8. Valid Palindrome II (Remove at most one char)

**Problem:** Check if palindrome after removing at most one character.

**Input:** "abca"

### The Code:
```python
def valid_palindrome_ii(s):
    def is_pal(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True
    
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            # Try removing left OR right character
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    
    return True
```

### Visual:

```
s = "abca"

left=0 (a), right=3 (a): equal
left=1 (b), right=2 (c): NOT equal!

Try removing left (b): check "ca" → not palindrome
Try removing right (c): check "ba" → not palindrome

Wait, let me check again:
Remove left (index 1): "aca" → palindrome ✓
Return True
```

**Time:** O(n) | **Space:** O(1)

---

## 9. Merge Sorted Arrays In-Place

**Problem:** Merge nums2 into nums1 (nums1 has enough space).

**Input:** nums1 = [1,2,3,0,0,0], m=3, nums2 = [2,5,6], n=3

### The Code:
```python
def merge(nums1, m, nums2, n):
    p1, p2, p = m - 1, n - 1, m + n - 1
    
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    
    # Copy remaining nums2 elements
    nums1[:p2 + 1] = nums2[:p2 + 1]
```

### Visual Walkthrough:

```
nums1 = [1, 2, 3, 0, 0, 0]
nums2 = [2, 5, 6]

p1=2 (3), p2=2 (6), p=5
Compare 3 vs 6: 6 is bigger
nums1[5] = 6
nums1 = [1, 2, 3, 0, 0, 6]
p2=1, p=4

p1=2 (3), p2=1 (5), p=4
Compare 3 vs 5: 5 is bigger
nums1[4] = 5
nums1 = [1, 2, 3, 0, 5, 6]
p2=0, p=3

p1=2 (3), p2=0 (2), p=3
Compare 3 vs 2: 3 is bigger
nums1[3] = 3
nums1 = [1, 2, 3, 3, 5, 6]
p1=1, p=2

p1=1 (2), p2=0 (2), p=2
Compare 2 vs 2: equal (use nums2)
nums1[2] = 2
nums1 = [1, 2, 2, 3, 5, 6]
p2=-1, p=1

p2 < 0, DONE!

Result: [1, 2, 2, 3, 5, 6]
```

**Key Insight:** Merge from the BACK to avoid overwriting!

**Time:** O(n+m) | **Space:** O(1)

---

## 10. Partition Array

**Problem:** Partition around pivot value.

**Input:** nums = [9, 12, 3, 5, 14, 10, 10], pivot = 10

### The Code:
```python
def partition_array(nums, pivot):
    small = 0
    for large in range(len(nums)):
        if nums[large] < pivot:
            nums[small], nums[large] = nums[large], nums[small]
            small += 1
    return small
```

### Visual Walkthrough:

```
nums = [9, 12, 3, 5, 14, 10, 10], pivot=10

large=0: 9 < 10, swap(0,0), small=1
         [9, 12, 3, 5, 14, 10, 10]

large=1: 12 >= 10, skip

large=2: 3 < 10, swap(1,2), small=2
         [9, 3, 12, 5, 14, 10, 10]

large=3: 5 < 10, swap(2,3), small=3
         [9, 3, 5, 12, 14, 10, 10]

large=4: 14 >= 10, skip

large=5: 10 >= 10, skip

large=6: 10 >= 10, skip

Result: [9, 3, 5, 12, 14, 10, 10]
              ↑
           small=3 (partition point)

All elements before index 3 are < 10 ✓
```

**Time:** O(n) | **Space:** O(1)

---

## Summary: When to Use What

| Scenario | Pattern | Example |
|----------|---------|---------|
| Sorted array, find pair | Opposite direction | Two Sum Sorted |
| Remove duplicates | Same direction | Remove Duplicates |
| Palindrome check | Opposite direction | Valid Palindrome |
| Container/trapping | Opposite direction | Container With Most Water |
| Find triplet | Sort + Fix one + Two pointer | 3Sum |
| Sort 0s/1s/2s | Three pointer | Sort Colors |
| Merge from back | Backward two pointer | Merge Sorted Arrays |

## Key Insights

1. **Sorted array → Think two pointer!**
2. **Opposite direction** for pair problems
3. **Same direction** for partition/remove problems
4. **Move shorter pointer** in container problems
5. **Sort first** for triplet/quad problems
6. **Merge from back** to avoid overwriting

## Practice Problems

| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Two Sum Sorted | Opposite | Easy |
| 2 | Valid Palindrome | Opposite | Easy |
| 3 | Move Zeroes | Same direction | Easy |
| 4 | Container Most Water | Opposite | Medium |
| 5 | Sort Colors | Three pointer | Medium |
| 6 | 3Sum | Sort + Two pointer | Medium |
| 7 | 4Sum | Sort + Two pointer | Medium |
| 8 | Trapping Rain Water | Two pointer | Hard |
| 9 | Merge Sorted Arrays | Backward | Easy |
| 10 | Partition Array | Same direction | Medium |
