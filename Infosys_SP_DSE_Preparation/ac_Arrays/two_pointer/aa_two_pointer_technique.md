# Complete Two Pointer Technique Guide

## What is Two Pointer?

Two pointer uses **two indices** moving through an array to solve problems in O(n) instead of O(n²).

**When to use:**
- Sorted array (strongest signal)
- Pair/triplet finding
- Palindrome checking
- Partition problems
- Merging sorted arrays
- Sliding window (special case of two pointer)

---

## 1. Opposite Direction Two Pointer

**Pattern:** Left starts at 0, right starts at end. Move inward.

### Pair Sum in Sorted Array (LeetCode 167)

```python
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
# Time: O(n), Space: O(1)
# Key insight: sorted array -> sum too small -> move left forward
#                              sum too big  -> move right backward
```

---

## 2. Same Direction Two Pointer (Fast/Slow)

**Pattern:** Both start at same end. Fast explores, slow catches up.

### Remove Duplicates from Sorted Array (LeetCode 26)

```python
def remove_duplicates(nums):
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
# slow: position to place next unique element
# fast: explores new elements
# Time: O(n), Space: O(1)
```

### Remove Element (LeetCode 27)

```python
def remove_element(nums, val):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != val:
            nums[slow] = nums[fast]
            slow += 1
    return slow
```

---

## 3. Two Pointer on Unsorted Array

### Move Zeroes (LeetCode 283)

```python
def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
# slow tracks position for next non-zero
```

### Sort Colors / Dutch National Flag (LeetCode 75)

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
    # Three regions: [0..low-1]=0, [low..mid-1]=1, [mid..high]=unknown, [high+1..]=2
# Time: O(n), Space: O(1), One pass
```

---

## 4. Container With Most Water (LeetCode 11)

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
# Why move the shorter one?
# If we move the taller one, width decreases and height is limited by shorter,
# so area can only decrease. Moving shorter one might find a taller wall.
# Time: O(n), Space: O(1)
```

---

## 5. Trapping Rain Water (LeetCode 42)

### Approach 1: Two Pointer (Optimal)

```python
def trap_rain_water(height):
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
# Time: O(n), Space: O(1)
# Key: water[i] = min(left_max[i], right_max[i]) - height[i]
```

### Approach 2: Stack

```python
def trap_rain_water_stack(height):
    stack = []
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = height[stack.pop()]
            if stack:
                width = i - stack[-1] - 1
                height_diff = min(h, height[stack[-1]]) - bottom
                water += width * height_diff
        stack.append(i)
    return water
# Time: O(n), Space: O(n)
```

---

## 6. 3Sum (LeetCode 15)

```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:  # Skip duplicates
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
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
# Time: O(n^2), Space: O(1) excluding output
```

---

## 7. 4Sum (LeetCode 18)

```python
def four_sum(nums, target):
    nums.sort()
    result = []
    n = len(nums)
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, n - 2):
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
# Time: O(n^3), Space: O(1)
```

---

## 8. Partition Array

```python
# Partition around pivot value
def partition_array(nums, pivot):
    small = 0
    for large in range(len(nums)):
        if nums[large] < pivot:
            nums[small], nums[large] = nums[large], nums[small]
            small += 1
    return small
# All elements < pivot are before index 'small'
```

---

## 9. Merge Sorted Arrays In-Place

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
    nums1[:p2 + 1] = nums2[:p2 + 1]
# Merge from the back to avoid overwriting
```

---

## 10. Valid Palindrome (LeetCode 125)

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

### Valid Palindrome II (LeetCode 680) - Remove at most one char

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
            return is_pal(left + 1, right) or is_pal(left, right - 1)
        left += 1
        right -= 1
    return True
# Time: O(n), Space: O(1)
```

---

## Key Insight

> **When array is sorted, THINK TWO POINTER.**
>
> - Pair with sum? -> Two pointer from both ends
> - Triplet? -> Fix one, two pointer on rest
> - Palindrome? -> Two pointer from both ends
> - Partition? -> Same direction two pointer
> - Container/Water? -> Two pointer from both ends

---

## 10 Practice Problems

| # | Problem | Pattern | Difficulty |
|---|---------|---------|------------|
| 1 | Two Sum Sorted | Opposite direction | Easy |
| 2 | Valid Palindrome | Opposite direction | Easy |
| 3 | Move Zeroes | Same direction | Easy |
| 4 | Container Most Water | Opposite direction | Medium |
| 5 | Sort Colors | Three pointer | Medium |
| 6 | 3Sum | Sort + Two pointer | Medium |
| 7 | 4Sum | Sort + Two pointer | Medium |
| 8 | Trapping Rain Water | Two pointer / Stack | Hard |
| 9 | Merge Sorted Arrays | Backward two pointer | Easy |
| 10 | Partition Array | Same direction | Medium |
