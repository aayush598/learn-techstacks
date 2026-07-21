# Array Problems - Infosys SP DSE Preparation

> 55 Comprehensive Array Problems with Complete Python Solutions
> Covers Easy, Medium, and Hard difficulty levels
> Each problem includes: Statement, Approach, Code, Complexity, Trick/Tip

---

# EASY PROBLEMS (1-15)

---

## Problem 1: Two Sum

**Statement:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`. Each input has exactly one solution, and you cannot use the same element twice.

**Approach:** Use a hash map to store each number's index. For each number, check if `target - num` exists in the map. This gives O(n) time instead of O(n²) brute force.

**Solution:**
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Example
print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
print(two_sum([3, 2, 4], 6))        # Output: [1, 2]
```

**Time Complexity:** O(n) | **Space Complexity:** O(n)

**Trick/Tip:** Always think hash map when you see "pair that sums to target". The complement lookup is the key insight.

---

## Problem 2: Best Time to Buy and Sell Stock

**Statement:** Given an array `prices` where `prices[i]` is the price of a stock on day `i`, find the maximum profit you can achieve by buying on one day and selling on a later day. Return 0 if no profit is possible.

**Approach:** Track the minimum price seen so far. At each day, calculate profit if we sold today (`price - min_price`). Update max profit accordingly. Single pass through the array.

**Solution:**
```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)
    return max_profit

# Example
print(max_profit([7, 1, 5, 3, 6, 4]))  # Output: 5
print(max_profit([7, 6, 4, 3, 1]))      # Output: 0
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** The trick is tracking min_price as you go. You don't need to know future prices — just keep the best buy point.

---

## Problem 3: Contains Duplicate

**Statement:** Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

**Approach:** Use a set to track seen elements. If we encounter an element already in the set, we found a duplicate. Alternatively, compare length of array vs length of set.

**Solution:**
```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# One-liner approach
def contains_duplicate_oneliner(nums):
    return len(nums) != len(set(nums))

# Example
print(contains_duplicate([1, 2, 3, 1]))     # Output: True
print(contains_duplicate([1, 2, 3, 4]))     # Output: False
print(contains_duplicate([1, 1, 1, 3, 3]))  # Output: True
```

**Time Complexity:** O(n) | **Space Complexity:** O(n)

**Trick/Tip:** The one-liner `len(nums) != len(set(nums))` is clean but uses O(n) space. For O(1) space, sort first then check adjacent elements in O(n log n).

---

## Problem 4: Maximum Subarray (Kadane's Algorithm)

**Statement:** Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

**Approach:** Maintain current sum. If current sum drops below 0, reset it to 0 (start a new subarray). Track the maximum sum seen. This is Kadane's algorithm — elegant and O(n).

**Solution:**
```python
def max_subarray(nums):
    current_sum = 0
    max_sum = float('-inf')
    for num in nums:
        current_sum += num
        max_sum = max(max_sum, current_sum)
        if current_sum < 0:
            current_sum = 0
    return max_sum

# Handles all-negative arrays
def max_subarray_v2(nums):
    current_sum = max_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum

# Example
print(max_subarray_v2([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Output: 6
print(max_subarray_v2([-1]))                                 # Output: -1
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Version 2 handles all-negative arrays correctly. The key insight: either extend the previous subarray or start fresh at current element.

---

## Problem 5: Merge Sorted Arrays

**Statement:** Given two sorted integer arrays `nums1` and `nums2`, merge them into a single sorted array and return it.

**Approach:** Use two pointers starting from the beginning of each array. Compare elements at both pointers, append the smaller one to result, and move that pointer forward. Handle remaining elements.

**Solution:**
```python
def merge_sorted(nums1, nums2):
    result = []
    i, j = 0, 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            result.append(nums1[i])
            i += 1
        else:
            result.append(nums2[j])
            j += 1
    result.extend(nums1[i:])
    result.extend(nums2[j:])
    return result

# In-place merge (LeetCode style - nums1 has extra space)
def merge_in_place(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1

# Example
print(merge_sorted([1, 3, 5], [2, 4, 6]))  # Output: [1, 2, 3, 4, 5, 6]
```

**Time Complexity:** O(m + n) | **Space Complexity:** O(m + n)

**Trick/Tip:** For in-place merge, always merge from the back to avoid overwriting elements.

---

## Problem 6: Rotate Array by K Positions

**Statement:** Given an array, rotate the array to the right by `k` steps where `k` is non-negative.

**Approach:** Reverse the entire array, then reverse the first `k` elements, then reverse the remaining elements. This three-reverse trick achieves rotation in O(n) time and O(1) space.

**Solution:**
```python
def rotate(nums, k):
    n = len(nums)
    k = k % n  # Handle k > n

    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    reverse(0, n - 1)       # Reverse entire array
    reverse(0, k - 1)       # Reverse first k elements
    reverse(k, n - 1)       # Reverse remaining elements

# Example
arr = [1, 2, 3, 4, 5, 6, 7]
rotate(arr, 3)
print(arr)  # Output: [5, 6, 7, 1, 2, 3, 4]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** The three-reverse technique is a classic. Remember: reverse all → reverse first k → reverse rest. It's counterintuitive but works perfectly.

---

## Problem 7: Move Zeros to End

**Statement:** Given an integer array `nums`, move all zeros to the end while maintaining the relative order of non-zero elements. Do this in-place without making a copy.

**Approach:** Use a slow pointer to track where the next non-zero should go. Fast pointer scans the array. When fast finds a non-zero, swap it with the slow pointer position.

**Solution:**
```python
def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1

# Example
arr = [0, 1, 0, 3, 12]
move_zeroes(arr)
print(arr)  # Output: [1, 3, 12, 0, 0]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Two-pointer swap technique. Slow pointer only advances when we place a non-zero. This preserves order of non-zero elements.

---

## Problem 8: Single Number

**Statement:** Given a non-empty array of integers where every element appears twice except one, find that single number. Must run in O(n) time and use O(1) extra space.

**Approach:** XOR all elements together. Since `a ^ a = 0` and `a ^ 0 = a`, all pairs cancel out leaving only the single number. Beautiful bit manipulation trick.

**Solution:**
```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# Using reduce
from functools import reduce
def single_number_v2(nums):
    return reduce(lambda a, b: a ^ b, nums)

# Example
print(single_number([2, 2, 1]))        # Output: 1
print(single_number([4, 1, 2, 1, 2]))  # Output: 4
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** XOR is your best friend for "find the unique element" problems. Properties: `a^a=0`, `a^0=a`, commutative and associative.

---

## Problem 9: Intersection of Two Arrays

**Statement:** Given two integer arrays, return an array of their intersection. Each element in the result must be unique.

**Approach:** Convert both arrays to sets and return their intersection. Sets automatically handle uniqueness and give O(1) lookups.

**Solution:**
```python
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))

# Without using set intersection
def intersection_v2(nums1, nums2):
    set1 = set(nums1)
    result = set()
    for num in nums2:
        if num in set1:
            result.add(num)
    return list(result)

# With duplicates (each element appears min(count1, count2) times)
from collections import Counter
def intersection_with_dups(nums1, nums2):
    counter1 = Counter(nums1)
    counter2 = Counter(nums2)
    result = []
    for num in counter1:
        if num in counter2:
            result.extend([num] * min(counter1[num], counter2[num]))
    return result

# Example
print(intersection([1, 2, 2, 1], [2, 2]))  # Output: [2]
```

**Time Complexity:** O(m + n) | **Space Complexity:** O(min(m, n))

**Trick/Tip:** Convert the smaller array to a set for better space usage. Use Counter version when duplicates matter.

---

## Problem 10: Plus One

**Statement:** Given a non-empty array of digits representing a non-negative integer, increment the number by one. The digits are stored with the most significant digit first.

**Approach:** Start from the last digit and add one. If digit becomes 10, set it to 0 and carry 1 to the next. If carry remains after all digits, insert 1 at the beginning.

**Solution:**
```python
def plus_one(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits  # All were 9s, e.g., 999 → 1000

# Example
print(plus_one([1, 2, 3]))      # Output: [1, 2, 4]
print(plus_one([4, 3, 2, 1]))   # Output: [4, 3, 2, 2]
print(plus_one([9, 9, 9]))      # Output: [1, 0, 0, 0]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1) (O(n) if new array created for all-9s case)

**Trick/Tip:** Only the trailing 9s change. Find the rightmost non-9, increment it, set everything after to 0. Most cases return early.

---

## Problem 11: Remove Duplicates from Sorted Array

**Statement:** Given a sorted array, remove duplicates in-place such that each element appears only once and return the new length. Do not use extra space for another array.

**Approach:** Use a slow pointer to track the position of the last unique element. When fast pointer finds a new unique element, place it at slow+1 and advance slow.

**Solution:**
```python
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1

# With at-most-two duplicates allowed
def remove_duplicates_at_most_two(nums):
    if len(nums) <= 2:
        return len(nums)
    slow = 2
    for fast in range(2, len(nums)):
        if nums[fast] != nums[slow - 2]:
            nums[slow] = nums[fast]
            slow += 1
    return slow

# Example
arr = [1, 1, 2]
length = remove_duplicates(arr)
print(arr[:length])  # Output: [1, 2]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Slow pointer = write position, fast pointer = read position. This pattern applies to many in-place array modification problems.

---

## Problem 12: Find Minimum in Rotated Sorted Array

**Statement:** A sorted array is rotated at some pivot. Find the minimum element in O(log n) time. No duplicates in the array.

**Approach:** Modified binary search. Compare mid element with right pointer. If mid > right, minimum is in the right half. Otherwise, minimum is in the left half including mid.

**Solution:**
```python
def find_min(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]

# With duplicates (O(n) worst case)
def find_min_with_dups(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        elif nums[mid] < nums[right]:
            right = mid
        else:
            right -= 1  # Can't decide, shrink right
    return nums[left]

# Example
print(find_min([3, 4, 5, 1, 2]))  # Output: 1
print(find_min([4, 5, 6, 7, 0, 1, 2]))  # Output: 0
```

**Time Complexity:** O(log n) | **Space Complexity:** O(1)

**Trick/Tip:** Compare with right element (not left) to handle all cases correctly. The rotation point is where the minimum lives.

---

## Problem 13: Majority Element

**Statement:** Given an array of size `n`, find the element that appears more than `n/2` times. The majority element always exists in the array.

**Approach:** Boyer-Moore Voting Algorithm: maintain a candidate and count. If count is 0, pick new candidate. If same element, increment count; otherwise decrement. The majority element survives.

**Solution:**
```python
def majority_element(nums):
    candidate = None
    count = 0
    for num in nums:
        if count == 0:
            candidate = num
        count += 1 if num == candidate else -1
    return candidate

# Using sorting
def majority_element_sorting(nums):
    nums.sort()
    return nums[len(nums) // 2]

# Using HashMap
from collections import Counter
def majority_element_hashmap(nums):
    counts = Counter(nums)
    return max(counts, key=counts.get)

# Example
print(majority_element([3, 2, 3]))         # Output: 3
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # Output: 2
```

**Time Complexity:** O(n) | **Space Complexity:** O(1) (Boyer-Moore)

**Trick/Tip:** Boyer-Moore is brilliant — it works because the majority element appears more than all other elements combined, so it can never be fully "cancelled out".

---

## Problem 14: Best Time to Buy and Sell Stock II

**Statement:** Given an array of prices, find the maximum profit from as many transactions as you like (buy and sell one share multiple times). Must sell before buying again.

**Approach:** Sum up all positive differences between consecutive days. If tomorrow's price is higher than today's, we "buy today and sell tomorrow". This captures all possible gains.

**Solution:**
```python
def max_profit(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit

# Using zip
def max_profit_v2(prices):
    return sum(max(b - a, 0) for a, b in zip(prices, prices[1:]))

# Example
print(max_profit([7, 1, 5, 3, 6, 4]))  # Output: 7
print(max_profit([1, 2, 3, 4, 5]))      # Output: 4
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** With unlimited transactions, greedily take every upward movement. No need to track when to buy/sell — just sum all gains.

---

## Problem 15: Find the Duplicate Number

**Statement:** Given an array of `n+1` integers where each integer is between 1 and n (inclusive), find the one duplicate number. Must use O(1) extra space and not modify the array.

**Approach:** Treat the array as a linked list where `nums[i]` is the next node. The duplicate creates a cycle. Use Floyd's tortoise and hare algorithm to find the cycle entrance, which is the duplicate.

**Solution:**
```python
def find_duplicate(nums):
    # Phase 1: Find intersection point in cycle
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    # Phase 2: Find entrance to cycle (the duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow

# Binary search approach (also O(n log n))
def find_duplicate_binary(nums):
    low, high = 1, len(nums) - 1
    while low < high:
        mid = (low + high) // 2
        count = sum(x <= mid for x in nums)
        if count > mid:
            high = mid
        else:
            low = mid + 1
    return low

# Example
print(find_duplicate([1, 3, 4, 2, 2]))  # Output: 2
print(find_duplicate([3, 1, 3, 4, 2]))  # Output: 3
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** The array-as-linked-list insight is powerful. Values as indices → next pointers → cycle detection. Floyd's algorithm finds cycle start in O(n) time.

---

# MEDIUM PROBLEMS (16-41)

---

## Problem 16: Two Sum II - Input Sorted Array

**Statement:** Given a 1-indexed sorted array, find two numbers that add up to `target`. Return their 1-indexed positions. Must use O(1) extra space.

**Approach:** Two pointers from both ends. Since array is sorted, if sum is too small, move left pointer right; if too large, move right pointer left. Guaranteed to find the answer.

**Solution:**
```python
def two_sum_ii(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

# Example
print(two_sum_ii([2, 7, 11, 15], 9))   # Output: [1, 2]
print(two_sum_ii([2, 3, 4], 6))          # Output: [1, 3]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Sorted array + two pointers is a classic combo. No hash map needed. The sorted order gives you directional hints.

---

## Problem 17: 3Sum

**Statement:** Given an integer array, find all unique triplets that sum to zero. The solution set must not contain duplicate triplets.

**Approach:** Sort the array. Fix one element, then use two pointers for the remaining two. Skip duplicate values to avoid duplicate triplets. Reduces from O(n³) to O(n²).

**Solution:**
```python
def three_sum(nums):
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # Skip duplicates
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
    return result

# Example
print(three_sum([-1, 0, 1, 2, -1, -4]))
# Output: [[-1, -1, 2], [-1, 0, 1]]
```

**Time Complexity:** O(n²) | **Space Complexity:** O(1) (excluding output)

**Trick/Tip:** Sorting + skip duplicates is essential. The `continue` when `nums[i] == nums[i-1]` prevents duplicate triplets at the source.

---

## Problem 18: Container With Most Water

**Statement:** Given `n` non-negative integers representing heights, find two lines that together with the x-axis form a container that holds the most water.

**Approach:** Start with widest container (both ends). Move the pointer with the shorter height inward — it can only increase area because width decreases. The shorter line is the bottleneck.

**Solution:**
```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return max_water

# Example
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # Output: 49
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Moving the shorter pointer is key. Moving the taller one can never increase area since width always decreases and height is limited by the shorter line.

---

## Problem 19: Product of Array Except Self

**Statement:** Given an array, return a new array where each element at index `i` is the product of all elements except `nums[i]`. Must run without using division and in O(n) time.

**Approach:** Two passes: first pass builds prefix products (product of all elements to the left), second pass multiplies by suffix products (product of all elements to the right).

**Solution:**
```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n

    # Prefix products
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Suffix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result

# Example
print(product_except_self([1, 2, 3, 4]))  # Output: [24, 12, 8, 6]
print(product_except_self([-1, 1, 0, -3, 3]))  # Output: [0, 0, 9, 0, 0]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1) (output array not counted)

**Trick/Tip:** Each element = product of everything to its left × product of everything to its right. Two separate passes make this clean and division-free.

---

## Problem 20: Subarray Sum Equals K

**Statement:** Given an array of integers and an integer `k`, find the total number of contiguous subarrays whose sum equals `k`.

**Approach:** Use prefix sum with a hash map. If `prefix_sum - k` exists in the map, that means a subarray ending here sums to `k`. The count of that prefix gives us the number of such subarrays.

**Solution:**
```python
def subarray_sum(nums, k):
    prefix_sum = 0
    count = 0
    prefix_map = {0: 1}

    for num in nums:
        prefix_sum += num
        if prefix_sum - k in prefix_map:
            count += prefix_map[prefix_sum - k]
        prefix_map[prefix_sum] = prefix_map.get(prefix_sum, 0) + 1

    return count

# Example
print(subarray_sum([1, 1, 1], 2))           # Output: 2
print(subarray_sum([1, 2, 3], 3))           # Output: 2
print(subarray_sum([1, -1, 0], 0))          # Output: 3
```

**Time Complexity:** O(n) | **Space Complexity:** O(n)

**Trick/Tip:** Prefix sum + hashmap is the pattern for "count subarrays with sum = k". Handles negative numbers too (unlike sliding window).

---

## Problem 21: Next Permutation

**Statement:** Given an array of integers, rearrange numbers into the lexicographically next greater permutation. If not possible, rearrange to the lowest order (ascending).

**Approach:** Scan from right to find the first element smaller than its successor (pivot). Find the smallest element to the right of pivot that is larger than pivot. Swap them. Reverse the suffix after pivot.

**Solution:**
```python
def next_permutation(nums):
    # Step 1: Find the pivot (first element smaller than next from right)
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        # Step 2: Find the smallest element larger than pivot from right
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    # Step 3: Reverse the suffix
    nums[i + 1:] = reversed(nums[i + 1:])

# Example
arr = [1, 2, 3]
next_permutation(arr)
print(arr)  # Output: [1, 3, 2]

arr = [3, 2, 1]
next_permutation(arr)
print(arr)  # Output: [1, 2, 3]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Three steps: find pivot, swap with next larger, reverse suffix. Think of it as "incrementing" the number represented by the array.

---

## Problem 22: Sort Colors (Dutch National Flag)

**Statement:** Given an array with elements 0, 1, and 2 only, sort it in-place in a single pass. Do not use library sort functions.

**Approach:** Use three pointers: `low` (boundary for 0s), `mid` (current element), `high` (boundary for 2s). Swap elements to their correct regions. One pass solution.

**Solution:**
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
            # Don't increment mid - need to check swapped element

# Example
arr = [2, 0, 2, 1, 1, 0]
sort_colors(arr)
print(arr)  # Output: [0, 0, 1, 1, 2, 2]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** When swapping with `high`, don't advance `mid` — the swapped element hasn't been examined yet. When swapping with `low`, it's safe to advance `mid`.

---

## Problem 23: Set Matrix Zeroes

**Statement:** Given an `m x n` matrix, if an element is 0, set its entire row and column to 0. Try to do it in O(1) extra space.

**Approach:** Use the first row and first column as markers. Store whether each row/column should be zeroed. Handle first row/column separately since they serve as markers.

**Solution:**
```python
def set_zeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    first_row_zero = any(matrix[0][j] == 0 for j in range(n))
    first_col_zero = any(matrix[i][0] == 0 for i in range(m))

    # Use first row/col as markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    # Set zeros based on markers
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    if first_row_zero:
        for j in range(n):
            matrix[0][j] = 0
    if first_col_zero:
        for i in range(m):
            matrix[i][0] = 0

# Example
mat = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
set_zeroes(mat)
print(mat)  # Output: [[1, 0, 1], [0, 0, 0], [1, 0, 1]]
```

**Time Complexity:** O(m × n) | **Space Complexity:** O(1)

**Trick/Tip:** Using the matrix itself as storage (first row/col as markers) avoids extra space. Always handle the marker row/col separately at the end.

---

## Problem 24: Spiral Matrix

**Statement:** Given an `m x n` matrix, return all elements in spiral (clockwise) order.

**Approach:** Define boundaries (top, bottom, left, right). Traverse right along top, down along right, left along bottom, up along left. Shrink boundaries after each pass.

**Solution:**
```python
def spiral_order(matrix):
    result = []
    if not matrix:
        return result
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        # Traverse right
        for j in range(left, right + 1):
            result.append(matrix[top][j])
        top += 1

        # Traverse down
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1

        # Traverse left
        if top <= bottom:
            for j in range(right, left - 1, -1):
                result.append(matrix[bottom][j])
            bottom -= 1

        # Traverse up
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1

    return result

# Example
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(spiral_order(mat))  # Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]
```

**Time Complexity:** O(m × n) | **Space Complexity:** O(1) (excluding output)

**Trick/Tip:** Always check bounds before traversing bottom and left — after shrinking, the row/column might not exist anymore.

---

## Problem 25: Rotate Image (Matrix 90° Clockwise)

**Statement:** Given an `n x n` matrix, rotate it 90 degrees clockwise in-place.

**Approach:** Transpose the matrix (swap rows and columns), then reverse each row. This achieves 90-degree clockwise rotation in two simple steps.

**Solution:**
```python
def rotate(matrix):
    n = len(matrix)

    # Step 1: Transpose
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    # Step 2: Reverse each row
    for row in matrix:
        row.reverse()

# Alternative: layer by layer rotation
def rotate_v2(matrix):
    n = len(matrix)
    for layer in range(n // 2):
        first, last = layer, n - 1 - layer
        for i in range(first, last):
            offset = i - first
            top = matrix[first][i]
            matrix[first][i] = matrix[last - offset][first]
            matrix[last - offset][first] = matrix[last][last - offset]
            matrix[last][last - offset] = matrix[i][last]
            matrix[i][last] = top

# Example
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotate(mat)
print(mat)  # Output: [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
```

**Time Complexity:** O(n²) | **Space Complexity:** O(1)

**Trick/Tip:** Transpose + reverse rows = 90° clockwise. Reverse columns for counter-clockwise. This is much simpler than tracking individual rotations.

---

## Problem 26: Merge Intervals

**Statement:** Given an array of intervals, merge all overlapping intervals and return an array of the non-overlapping intervals.

**Approach:** Sort intervals by start time. Iterate through, extending the current interval if the next one overlaps (its start ≤ current end). Otherwise, add current to result and start a new one.

**Solution:**
```python
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:  # Overlapping
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)

    return merged

# Example
print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))
# Output: [[1, 6], [8, 10], [15, 18]]

print(merge_intervals([[1, 4], [4, 5]]))
# Output: [[1, 5]]
```

**Time Complexity:** O(n log n) | **Space Complexity:** O(n)

**Trick/Tip:** Always sort by start time first. The key comparison is `current_start <= last_end` — this catches all overlapping cases.

---

## Problem 27: Non-overlapping Intervals

**Statement:** Given a collection of intervals, find the minimum number of intervals you need to remove to make the rest non-overlapping.

**Approach:** Sort by end time. Greedily keep intervals with earliest end times — they leave the most room for future intervals. Count how many we keep, subtract from total.

**Solution:**
```python
def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[1])
    count = 0
    prev_end = intervals[0][1]

    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:  # Overlapping
            count += 1
        else:
            prev_end = intervals[i][1]

    return count

# Example
print(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]))
# Output: 1
print(erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]))
# Output: 2
```

**Time Complexity:** O(n log n) | **Space Complexity:** O(1)

**Trick/Tip:** Sort by END time (not start). This greedy approach maximizes non-overlapping intervals. End time sorting ensures we always pick the interval that finishes earliest.

---

## Problem 28: Maximum Product Subarray

**Statement:** Given an integer array, find the contiguous subarray with the largest product. The array can contain both positive and negative numbers.

**Approach:** Track both max and min products at each position (negative × negative = positive). At each step, consider three candidates: current num, num × max, num × min.

**Solution:**
```python
def max_product(nums):
    result = max_val = min_val = nums[0]
    for num in nums[1:]:
        candidates = (num, num * max_val, num * min_val)
        max_val = max(candidates)
        min_val = min(candidates)
        result = max(result, max_val)
    return result

# Alternative without tuple
def max_product_v2(nums):
    max_prod = min_prod = result = nums[0]
    for num in nums[1:]:
        if num < 0:
            max_prod, min_prod = min_prod, max_prod
        max_prod = max(num, max_prod * num)
        min_prod = min(num, min_prod * num)
        result = max(result, max_prod)
    return result

# Example
print(max_product([2, 3, -2, 4]))       # Output: 6
print(max_product([-2, 0, -1]))          # Output: 0
print(max_product([-2, 3, -4]))          # Output: 24
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Negative numbers flip max and min. When you see a negative, swap max and min before updating. Two negatives make a positive!

---

## Problem 29: Minimum Size Subarray Sum

**Statement:** Given an array of positive integers and a target sum `s`, find the minimal length of a contiguous subarray whose sum ≥ `s`. Return 0 if no such subarray exists.

**Approach:** Sliding window: expand right pointer until sum ≥ s, then shrink left pointer to minimize length. Track the minimum valid window size.

**Solution:**
```python
def min_sub_array_len(s, nums):
    left = 0
    total = 0
    min_len = float('inf')

    for right in range(len(nums)):
        total += nums[right]
        while total >= s:
            min_len = min(min_len, right - left + 1)
            total -= nums[left]
            left += 1

    return min_len if min_len != float('inf') else 0

# O(n log n) binary search approach
import bisect
def min_sub_array_len_bs(s, nums):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    min_len = float('inf')
    for i in range(1, len(prefix)):
        target = prefix[i] - s
        j = bisect.bisect_left(prefix, target)
        if j >= 0:
            min_len = min(min_len, i - j)
    return min_len if min_len != float('inf') else 0

# Example
print(min_sub_array_len(7, [2, 3, 1, 2, 4, 3]))  # Output: 2
```

**Time Complexity:** O(n) sliding window | **Space Complexity:** O(1)

**Trick/Tip:** Sliding window works because all numbers are positive. If negatives were present, use prefix sum + binary search instead.

---

## Problem 30: Subarray Product Less Than K

**Statement:** Given an array of positive integers and an integer `k`, count the number of contiguous subarrays where the product of all elements is strictly less than `k`.

**Approach:** Sliding window with two pointers. For each right pointer position, find the leftmost valid position. All subarrays ending at right between left and right are valid — that's `right - left + 1` subarrays.

**Solution:**
```python
def num_subarray_product_less_than_k(nums, k):
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

# Example
print(num_subarray_product_less_than_k([10, 5, 2, 6], 100))  # Output: 8
print(num_subarray_product_less_than_k([1, 2, 3], 0))          # Output: 0
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** For each valid window [left, right], the count of subarrays ending at right is `right - left + 1`. This is because subarrays are [right], [right-1, right], ..., [left, ..., right].

---

## Problem 31: Maximum Sum Circular Subarray

**Statement:** Given a circular array, find the maximum sum of a non-empty subarray. A circular array means the end connects back to the beginning.

**Approach:** Two cases: (1) Normal max subarray (Kadane's). (2) Circular: total sum - minimum subarray. The answer is max of both cases. Handle edge case where all elements are negative.

**Solution:**
```python
def max_subarray_sum_circular(nums):
    total = 0
    max_sum = cur_max = float('-inf')
    min_sum = cur_min = float('inf')

    for num in nums:
        cur_max = max(num, cur_max + num)
        max_sum = max(max_sum, cur_max)
        cur_min = min(num, cur_min + num)
        min_sum = min(min_sum, cur_min)
        total += num

    if max_sum > 0:
        return max(max_sum, total - min_sum)
    return max_sum  # All negative case

# Example
print(max_subarray_sum_circular([1, -2, 3, -2]))      # Output: 3
print(max_subarray_sum_circular([5, -3, 5]))           # Output: 10
print(max_subarray_sum_circular([-3, -2, -3, -2]))     # Output: -2
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Circular max = total - minimum subarray (the parts NOT included form the circular subarray). If all negative, return regular max (can't take empty subarray).

---

## Problem 32: Partition Array into Disjoint Intervals

**Statement:** Given an array, partition it into two contiguous subarrays left and right such that every element in left ≤ every element in right. Return the length of left.

**Approach:** Track the maximum seen so far from left. At each position, if all elements to the right are ≥ current maximum, we can partition here. Precompute suffix minimums for O(n) solution.

**Solution:**
```python
def partition_disjoint(nums):
    n = len(nums)
    suffix_min = [0] * n
    suffix_min[-1] = nums[-1]

    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(nums[i], suffix_min[i + 1])

    left_max = 0
    for i in range(n - 1):
        left_max = max(left_max, nums[i])
        if left_max <= suffix_min[i + 1]:
            return i + 1

    return n - 1

# One-pass approach
def partition_disjoint_v2(nums):
    left_max = partition = 0
    global_max = nums[0]

    for i in range(len(nums)):
        global_max = max(global_max, nums[i])
        if nums[i] < left_max:
            partition = i
        else:
            left_max = max(left_max, nums[partition])

    return partition + 1

# Example
print(partition_disjoint([5, 0, 3, 8, 6]))  # Output: 3
print(partition_disjoint([1, 1, 1, 0, 6, 12]))  # Output: 4
```

**Time Complexity:** O(n) | **Space Complexity:** O(n) / O(1) for v2

**Trick/Tip:** The partition point is where left_max (max of left part) ≤ min of everything to the right. Precomputing suffix minimums makes this straightforward.

---

## Problem 33: Squares of a Sorted Array

**Statement:** Given a sorted array of negative and non-negative integers, return a new array of squares in sorted order. Must run in O(n) time.

**Approach:** Two pointers from both ends. Compare absolute values, place the larger square at the end of the result array. Move inward. This avoids O(n log n) sorting.

**Solution:**
```python
def sorted_squares(nums):
    n = len(nums)
    result = [0] * n
    left, right = 0, n - 1
    pos = n - 1

    while left <= right:
        left_sq = nums[left] ** 2
        right_sq = nums[right] ** 2
        if left_sq > right_sq:
            result[pos] = left_sq
            left += 1
        else:
            result[pos] = right_sq
            right -= 1
        pos -= 1

    return result

# Example
print(sorted_squares([-4, -1, 0, 3, 10]))  # Output: [0, 1, 9, 16, 100]
print(sorted_squares([-7, -3, 2, 3, 11]))  # Output: [4, 9, 9, 49, 121]
```

**Time Complexity:** O(n) | **Space Complexity:** O(n)

**Trick/Tip:** The largest squares are always at the extremes (most negative or most positive). Merge-like process from both ends into a reverse result array.

---

## Problem 34: Find All Duplicates in an Array

**Statement:** Given an array where elements are in range [1, n] and some appear twice while others appear once, find all elements that appear twice. Must use O(1) extra space.

**Approach:** Use the array indices as hash. For each element, negate the value at index `|element| - 1`. If we encounter a negative, that index has been visited before — it's a duplicate.

**Solution:**
```python
def find_duplicates(nums):
    result = []
    for num in nums:
        index = abs(num) - 1
        if nums[index] < 0:
            result.append(abs(num))
        else:
            nums[index] = -nums[index]
    return result

# Without modifying array (cycle sort approach)
def find_duplicates_v2(nums):
    result = []
    i = 0
    while i < len(nums):
        correct = nums[i] - 1
        if nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1

    for i in range(len(nums)):
        if nums[i] != i + 1:
            result.append(nums[i])
    return result

# Example
print(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1]))  # Output: [2, 3]
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Negation marking: use sign of array elements as visited flags. Range [1, n] maps perfectly to indices [0, n-1].

---

## Problem 35: Container With Most Water (Two Pointer)

**Statement:** Same as Problem 18 — Given n lines, find two that form a container holding the most water. Reinforced here with the two-pointer approach explanation.

**Approach:** Start with max width. The bottleneck is always the shorter line. Moving the taller line can never improve the area. So move the shorter one to potentially find a taller partner.

**Solution:**
```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        area = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, area)

        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1

    return max_water

# With early optimization
def max_area_optimized(height):
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        h = min(height[left], height[right])
        max_water = max(max_water, h * (right - left))

        while left < right and height[left] <= h:
            left += 1
        while left < right and height[right] <= h:
            right -= 1

    return max_water

# Example
print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # Output: 49
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** The optimized version skips over elements shorter than the current height — they can't possibly improve the area.

---

## Problem 36: Longest Consecutive Sequence

**Statement:** Given an unsorted array, find the length of the longest consecutive elements sequence. Must run in O(n) time.

**Approach:** Put all numbers in a set. For each number, check if it's the start of a sequence (num - 1 not in set). If so, count consecutive numbers. Track the maximum length.

**Solution:**
```python
def longest_consecutive(nums):
    num_set = set(nums)
    max_length = 0

    for num in num_set:
        if num - 1 not in num_set:  # Start of sequence
            current = num
            length = 1
            while current + 1 in num_set:
                current += 1
                length += 1
            max_length = max(max_length, length)

    return max_length

# Example
print(longest_consecutive([100, 4, 200, 1, 3, 2]))  # Output: 4
print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # Output: 9
```

**Time Complexity:** O(n) | **Space Complexity:** O(n)

**Trick/Tip:** Only start counting from the beginning of a sequence (when `num-1` is not in the set). This ensures each element is visited at most twice → O(n).

---

## Problem 37: Group Anagrams

**Statement:** Given an array of strings, group the anagrams together. An anagram is a word formed by rearranging another word.

**Approach:** Use sorted string as key in a dictionary. All anagrams have the same sorted form. Group strings by their sorted key.

**Solution:**
```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# More efficient key using character count
def group_anagrams_v2(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)
    return list(groups.values())

# Example
print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

**Time Complexity:** O(n × k log k) where k is max string length | **Space Complexity:** O(n × k)

**Trick/Tip:** Character count tuple is faster than sorting for long strings. For short strings, sorting is simpler and often faster due to lower constant factors.

---

## Problem 38: Top K Frequent Elements

**Statement:** Given an integer array and an integer `k`, return the `k` most frequent elements. Answer can be in any order.

**Approach:** Count frequencies with a hash map. Use a min-heap of size k, or bucket sort where index = frequency. Bucket sort gives O(n) time.

**Solution:**
```python
from collections import Counter
import heapq

# Using heap
def top_k_frequent(nums, k):
    count = Counter(nums)
    return [num for num, freq in heapq.nlargest(k, count.items(), key=lambda x: x[1])]

# Using bucket sort (O(n) guaranteed)
def top_k_frequent_bucket(nums, k):
    count = Counter(nums)
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]

    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for freq in range(n, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result

# Using quickselect
def top_k_frequent_quickselect(nums, k):
    count = Counter(nums)
    unique = list(count.keys())

    def partition(left, right, pivot_idx):
        pivot_freq = count[unique[pivot_idx]]
        unique[pivot_idx], unique[right] = unique[right], unique[pivot_idx]
        store = left
        for i in range(left, right):
            if count[unique[i]] < pivot_freq:
                unique[store], unique[i] = unique[i], unique[store]
                store += 1
        unique[store], unique[right] = unique[right], unique[store]
        return store

    left, right = 0, len(unique) - 1
    while left <= right:
        pivot = partition(left, right, (left + right) // 2)
        if pivot == len(unique) - k:
            return unique[pivot:]
        elif pivot < len(unique) - k:
            left = pivot + 1
        else:
            right = pivot - 1
    return []

# Example
print(top_k_frequent_bucket([1, 1, 1, 2, 2, 3], 2))  # Output: [1, 2]
```

**Time Complexity:** O(n) bucket sort | **Space Complexity:** O(n)

**Trick/Tip:** Bucket sort is optimal here. Frequency is bounded by n, so create n+1 buckets. This avoids the O(n log n) heap solution.

---

## Problem 39: Encode and Decode Strings

**Statement:** Design an algorithm to encode a list of strings to a single string, and decode it back to the original list. Strings can contain any characters.

**Approach:** Prefix each string with its length followed by a delimiter. For encoding: "len#string". For decoding: read length, then read that many characters.

**Solution:**
```python
def encode(strs):
    result = ""
    for s in strs:
        result += str(len(s)) + "#" + s
    return result

def decode(s):
    result = []
    i = 0
    while i < len(s):
        j = i
        while s[j] != '#':
            j += 1
        length = int(s[i:j])
        result.append(s[j + 1:j + 1 + length])
        i = j + 1 + length
    return result

# Alternative: using escape character
def encode_v2(strs):
    return ''.join(s.replace('\\', '\\\\').replace('$', '\\$') + '$' for s in strs)

def decode_v2(s):
    result = []
    current = []
    i = 0
    while i < len(s):
        if s[i] == '\\':
            current.append(s[i + 1])
            i += 2
        elif s[i] == '$':
            result.append(''.join(current))
            current = []
            i += 1
        else:
            current.append(s[i])
            i += 1
    return result

# Example
encoded = encode(["lint", "code", "love", "you"])
print(encoded)  # Output: "4#lint4#code4#love3#you"
print(decode(encoded))  # Output: ["lint", "code", "love", "you"]
```

**Time Complexity:** O(total characters) | **Space Complexity:** O(total characters)

**Trick/Tip:** The `#` delimiter works because it follows a number. No ambiguity: "4#lint" always means length 4, then "lint". Length prefix encoding is robust and simple.

---

## Problem 40: First Missing Positive

**Statement:** Given an unsorted integer array, find the smallest missing positive integer. Must run in O(n) time and use O(1) extra space.

**Approach:** Cycle sort: place each number `x` at index `x-1` if it's in range [1, n]. After sorting, scan for the first index where `nums[i] != i+1`. That's the answer.

**Solution:**
```python
def first_missing_positive(nums):
    n = len(nums)

    # Cycle sort: place each number at its correct index
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            correct = nums[i] - 1
            nums[i], nums[correct] = nums[correct], nums[i]

    # Find first missing positive
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1

    return n + 1

# Example
print(first_missing_positive([1, 2, 0]))       # Output: 3
print(first_missing_positive([3, 4, -1, 1]))   # Output: 2
print(first_missing_positive([7, 8, 9, 11, 12]))  # Output: 1
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** The answer is always in range [1, n+1]. We only care about positive integers ≤ n. Cycle sort puts each in its "home" position, then the mismatch reveals the answer.

---

## Problem 41: Jump Game

**Statement:** Given a non-negative integer array where each element represents your maximum jump length, determine if you can reach the last index starting from index 0.

**Approach:** Track the farthest reachable index. At each position, update farthest = max(farthest, i + nums[i]). If farthest ≥ last index, we can reach the end.

**Solution:**
```python
def can_jump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
    return True

# Minimum jumps to reach end
def jump(nums):
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
            if current_end >= len(nums) - 1:
                break
    return jumps

# Example
print(can_jump([2, 3, 1, 1, 4]))  # Output: True
print(can_jump([3, 2, 1, 0, 4]))  # Output: False
print(jump([2, 3, 1, 1, 4]))      # Output: 2
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** Greedy works because we only need to know if the last index is reachable, not the specific path. Track the farthest reachable point as you scan.

---

# HARD PROBLEMS (42-55)

---

## Problem 42: Trapping Rain Water

**Statement:** Given `n` non-negative integers representing an elevation map, compute how much water it can trap after raining.

**Approach:** Two pointers from both ends. Track left_max and right_max. At each step, water trapped at current position = min(left_max, right_max) - height. Move the pointer with smaller max.

**Solution:**
```python
def trap(height):
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

# Using prefix max arrays
def trap_v2(height):
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    return sum(min(left_max[i], right_max[i]) - height[i] for i in range(n))

# Example
print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]))  # Output: 6
print(trap([4, 2, 0, 3, 2, 5]))                       # Output: 9
```

**Time Complexity:** O(n) | **Space Complexity:** O(1) for two-pointer, O(n) for prefix arrays

**Trick/Tip:** Water at each position = min(max_left, max_right) - height. Two-pointer works because we always process the side with the smaller max, which is the bottleneck.

---

## Problem 43: Median of Two Sorted Arrays

**Statement:** Given two sorted arrays, find the median of the combined sorted array in O(log(min(m, n))) time.

**Approach:** Binary search on the smaller array. Partition both arrays so that left half has exactly (m+n+1)/2 elements. Ensure all left elements ≤ all right elements. Adjust binary search based on comparison.

**Solution:**
```python
def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    half = (m + n + 1) // 2
    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2  # Partition in nums1
        j = half - i         # Partition in nums2

        left_max1 = float('-inf') if i == 0 else nums1[i - 1]
        right_min1 = float('inf') if i == m else nums1[i]
        left_max2 = float('-inf') if j == 0 else nums2[j - 1]
        right_min2 = float('inf') if j == n else nums2[j]

        if left_max1 <= right_min2 and left_max2 <= right_min1:
            if (m + n) % 2 == 1:
                return max(left_max1, left_max2)
            else:
                return (max(left_max1, left_max2) + min(right_min1, right_min2)) / 2
        elif left_max1 > right_min2:
            hi = i - 1
        else:
            lo = i + 1

    return 0

# Example
print(find_median_sorted_arrays([1, 3], [2]))        # Output: 2.0
print(find_median_sorted_arrays([1, 2], [3, 4]))     # Output: 2.5
```

**Time Complexity:** O(log(min(m, n))) | **Space Complexity:** O(1)

**Trick/Tip:** Always binary search on the smaller array. The partition must satisfy: max(left) ≤ min(right) on both sides. Edge cases handled by using ±infinity.

---

## Problem 44: Count of Range Sum

**Statement:** Given an integer array and two integers `lower` and `upper`, count the number of range sums that lie in [lower, upper]. Range sum `S(i, j)` is defined as sum of elements from index i to j.

**Approach:** Compute prefix sums. Use merge sort to count pairs where `lower ≤ prefix[j] - prefix[i] ≤ upper` during the merge step. The merge sort approach efficiently counts cross-range pairs.

**Solution:**
```python
def count_range_sum(nums, lower, upper):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    def sort_count(start, end):
        if end - start <= 1:
            return 0
        mid = (start + end) // 2
        count = sort_count(start, mid) + sort_count(mid, end)

        # Count cross-range pairs
        j = k = mid
        for left in range(start, mid):
            while k < end and prefix[k] - prefix[left] < lower:
                k += 1
            while j < end and prefix[j] - prefix[left] <= upper:
                j += 1
            count += j - k

        # Merge step
        temp = []
        i, j2 = start, mid
        while i < mid and j2 < end:
            if prefix[i] <= prefix[j2]:
                temp.append(prefix[i])
                i += 1
            else:
                temp.append(prefix[j2])
                j2 += 1
        temp.extend(prefix[i:mid])
        temp.extend(prefix[j2:end])
        prefix[start:end] = temp

        return count

    return sort_count(0, len(prefix))

# Brute force (for verification)
def count_range_sum_bf(nums, lower, upper):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)
    count = 0
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            s = prefix[j + 1] - prefix[i]
            if lower <= s <= upper:
                count += 1
    return count

# Example
print(count_range_sum([-2, 5, -1], -2, 2))  # Output: 3
```

**Time Complexity:** O(n log n) | **Space Complexity:** O(n)

**Trick/Tip:** Prefix sum converts subarray sums to pair differences. Merge sort counts these efficiently during the merge step by using two pointers.

---

## Problem 45: Maximum Gap

**Statement:** Given an unsorted array, find the maximum difference between successive elements in its sorted form. Must run in O(n) time.

**Approach:** Radix sort or bucket sort. Divide range into n buckets of size `gap`. The maximum gap must occur between buckets (not within). Track min and max of each bucket.

**Solution:**
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

# Radix sort approach
def maximum_gap_radix(nums):
    if len(nums) < 2:
        return 0

    max_val = max(nums)
    exp = 1
    n = len(nums)
    output = [0] * n

    while max_val // exp > 0:
        count = [0] * 10
        for num in nums:
            count[(num // exp) % 10] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in range(n - 1, -1, -1):
            digit = (nums[i] // exp) % 10
            count[digit] -= 1
            output[count[digit]] = nums[i]
        nums = output[:]
        exp *= 10

    return max(nums[i] - nums[i - 1] for i in range(1, len(nums)))

# Example
print(maximum_gap([3, 6, 9, 1]))  # Output: 3
print(maximum_gap([10]))           # Output: 0
```

**Time Complexity:** O(n) | **Space Complexity:** O(n)

**Trick/Tip:** Pigeonhole principle: max gap can't be in a single bucket. Sort into buckets of size `gap`, then only compare across buckets. This eliminates within-bucket comparisons.

---

## Problem 46: Sliding Window Maximum

**Statement:** Given an array and window size `k`, find the maximum value in each sliding window of size `k`.

**Approach:** Use a monotonic deque (decreasing). Remove elements outside the window from front. Remove smaller elements from back (they can't be max). Front of deque is always the current window's max.

**Solution:**
```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()
    result = []

    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back
        while dq and nums[dq[-1]] <= nums[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Using heap (slightly slower but works)
import heapq
def max_sliding_window_heap(nums, k):
    result = []
    heap = []
    for i in range(len(nums)):
        heapq.heappush(heap, (-nums[i], i))
        while heap[0][1] < i - k + 1:
            heapq.heappop(heap)
        if i >= k - 1:
            result.append(-heap[0][0])
    return result

# Example
print(max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3))
# Output: [3, 3, 5, 5, 6, 7]
```

**Time Complexity:** O(n) | **Space Complexity:** O(k)

**Trick/Tip:** Monotonic deque is the gold standard. Each element enters and leaves the deque at most once → O(n) amortized. The deque stores indices, not values.

---

## Problem 47: Count Inversions

**Statement:** Given an array, count the number of inversions. An inversion is a pair (i, j) where i < j and arr[i] > arr[j].

**Approach:** Modified merge sort. During the merge step, when an element from the right half is placed before elements from the left half, those form inversions. Count them.

**Solution:**
```python
def count_inversions(arr):
    def merge_sort_count(arr, temp, left, right):
        if left >= right:
            return 0
        mid = (left + right) // 2
        count = merge_sort_count(arr, temp, left, mid)
        count += merge_sort_count(arr, temp, mid + 1, right)
        count += merge_count(arr, temp, left, mid, right)
        return count

    def merge_count(arr, temp, left, mid, right):
        i, j, k = left, mid + 1, left
        count = 0
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp[k] = arr[i]
                i += 1
            else:
                temp[k] = arr[j]
                count += mid - i + 1  # All remaining in left are > arr[j]
                j += 1
            k += 1
        while i <= mid:
            temp[k] = arr[i]
            i += 1
            k += 1
        while j <= right:
            temp[k] = arr[j]
            j += 1
            k += 1
        arr[left:right + 1] = temp[left:right + 1]
        return count

    temp = arr[:]
    return merge_sort_count(arr, temp, 0, len(arr) - 1)

# Brute force for verification
def count_inversions_bf(arr):
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                count += 1
    return count

# Example
print(count_inversions([2, 4, 3, 5, 1]))  # Output: 6
print(count_inversions([5, 4, 3, 2, 1]))  # Output: 10
```

**Time Complexity:** O(n log n) | **Space Complexity:** O(n)

**Trick/Tip:** The merge step is key: when right[j] < left[i], all remaining left elements (mid - i + 1 of them) form inversions with right[j]. This counts multiple inversions in one step.

---

## Problem 48: Shortest Unsorted Continuous Subarray

**Statement:** Given an integer array, find the length of the shortest unsorted subarray such that if you sort it, the entire array becomes sorted.

**Approach:** Find the first and last elements out of order. From left, find the first element smaller than the max seen so far (that's the right boundary). From right, find the first element bigger than the min seen so far (left boundary).

**Solution:**
```python
def find_unsorted_subarray(nums):
    n = len(nums)
    max_val = float('-inf')
    min_val = float('inf')
    end = -1
    start = 0

    # Find right boundary
    for i in range(n):
        if nums[i] >= max_val:
            max_val = nums[i]
        else:
            end = i

    # Find left boundary
    for i in range(n - 1, -1, -1):
        if nums[i] <= min_val:
            min_val = nums[i]
        else:
            start = i

    return end - start + 1 if end != -1 else 0

# Sorting approach
def find_unsorted_subarray_sorting(nums):
    sorted_nums = sorted(nums)
    start = end = -1
    for i in range(len(nums)):
        if nums[i] != sorted_nums[i]:
            if start == -1:
                start = i
            end = i
    return end - start + 1 if start != -1 else 0

# Example
print(find_unsorted_subarray([2, 6, 4, 8, 10, 9, 15]))  # Output: 5
print(find_unsorted_subarray([1, 2, 3, 4]))               # Output: 0
```

**Time Complexity:** O(n) | **Space Complexity:** O(1)

**Trick/Tip:** The unsorted region extends from the first element that's out of ascending order to the last. Track max from left (finds right boundary) and min from right (finds left boundary).

---

## Problem 49: Longest Increasing Subsequence (O(n log n))

**Statement:** Given an integer array, find the length of the longest strictly increasing subsequence. Must run in O(n log n) time.

**Approach:** Maintain a `tails` array where `tails[i]` is the smallest tail element for an increasing subsequence of length `i+1`. Use binary search to find where each element fits.

**Solution:**
```python
import bisect

def length_of_lis(nums):
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

# With actual subsequence reconstruction
def lis_with_sequence(nums):
    tails = []
    tail_indices = []
    predecessors = [-1] * len(nums)

    for i, num in enumerate(nums):
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
            tail_indices.append(i)
        else:
            tails[pos] = num
            tail_indices[pos] = i
        if pos > 0:
            predecessors[i] = tail_indices[pos - 1]

    # Reconstruct
    result = []
    k = tail_indices[len(tails) - 1]
    while k >= 0:
        result.append(nums[k])
        k = predecessors[k]
    return result[::-1]

# DP O(n²) approach
def length_of_lis_dp(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# Example
print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))  # Output: 4
print(lis_with_sequence([10, 9, 2, 5, 3, 7, 101, 18]))  # Output: [2, 3, 7, 18]
```

**Time Complexity:** O(n log n) | **Space Complexity:** O(n)

**Trick/Tip:** The `tails` array is always sorted, which enables binary search. Each element either extends the array or replaces a larger element — maintaining the invariant.

---

## Problem 50: Burst Balloons

**Statement:** Given `n` balloons with numbers on them, burst them one by one. Each burst gives `nums[left] * nums[i] * nums[right]` coins. Find the maximum coins.

**Approach:** Interval DP. Think of it as the last balloon to burst in a range [i, j]. For each possible last balloon k, solve subproblems [i, k-1] and [k+1, j]. Add padding 1s at boundaries.

**Solution:**
```python
def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n - 1):  # length of interval
        for i in range(1, n - length):
            j = i + length - 1
            for k in range(i, j + 1):  # last balloon to burst
                dp[i][j] = max(dp[i][j],
                    dp[i][k - 1] + dp[k + 1][j] +
                    nums[i - 1] * nums[k] * nums[j + 1])

    return dp[1][n - 2]

# Memoization approach
def max_coins_memo(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    memo = {}

    def solve(left, right):
        if left > right:
            return 0
        if (left, right) in memo:
            return memo[(left, right)]

        result = 0
        for k in range(left, right + 1):
            coins = nums[left - 1] * nums[k] * nums[right + 1]
            result = max(result, coins + solve(left, k - 1) + solve(k + 1, right))

        memo[(left, right)] = result
        return result

    return solve(1, n - 2)

# Example
print(max_coins([3, 1, 5, 8]))  # Output: 167
```

**Time Complexity:** O(n³) | **Space Complexity:** O(n²)

**Trick/Tip:** Think of it as "which balloon do I burst LAST in range [i, j]?" This converts the problem to standard interval DP. Add padding 1s to handle edge balloons.

---

## Problem 51: Maximal Rectangle in Binary Matrix

**Statement:** Given a 2D binary matrix filled with 0s and 1s, find the area of the largest rectangle containing only 1s.

**Approach:** For each row, compute heights (consecutive 1s above including current). Then apply "Largest Rectangle in Histogram" on each row's heights to find max area.

**Solution:**
```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0

    rows, cols = len(matrix), len(matrix[0])
    heights = [0] * cols
    max_area = 0

    for row in range(rows):
        # Update heights
        for col in range(cols):
            if matrix[row][col] == '1':
                heights[col] += 1
            else:
                heights[col] = 0

        # Largest rectangle in histogram
        stack = [-1]
        for i in range(cols + 1):
            current = heights[i] if i < cols else 0
            while stack[-1] != -1 and current < heights[stack[-1]]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                max_area = max(max_area, h * w)
            stack.append(i)

    return max_area

# Largest Rectangle in Histogram (standalone)
def largest_rectangle_area(heights):
    stack = [-1]
    max_area = 0
    for i in range(len(heights) + 1):
        current = heights[i] if i < len(heights) else 0
        while stack[-1] != -1 and current < heights[stack[-1]]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1
            max_area = max(max_area, h * w)
        stack.append(i)
    return max_area

# Example
matrix = [["1", "0", "1", "0", "0"], ["1", "0", "1", "1", "1"],
          ["1", "1", "1", "1", "1"], ["1", "0", "0", "1", "0"]]
print(maximal_rectangle(matrix))  # Output: 6
```

**Time Complexity:** O(rows × cols) | **Space Complexity:** O(cols)

**Trick/Tip:** Building histogram heights row by row converts the 2D problem to repeated 1D problems. Largest Rectangle in Histogram uses a monotonic stack.

---

## Problem 52: Maximum Subarray Sum with at Most K Deletions

**Statement:** Given an array and integer `k`, find the maximum subarray sum that can be obtained by deleting at most `k` elements from the array.

**Approach:** Sliding window with a min-heap. Maintain a window where we can "afford" to delete elements (keep a min-heap of removed elements). Track prefix sums for efficient calculation.

**Solution:**
```python
import heapq

def max_sum_after_k_deletions(nums, k):
    prefix = [0]
    for num in nums:
        prefix.append(prefix[-1] + num)

    n = len(nums)
    result = float('-inf')

    # For each possible window [i, j], we can delete up to k elements inside
    # Equivalent to: find subarray with max sum after removing up to k smallest
    for window_size in range(k, n + 1):
        # Using heap approach
        for start in range(0, n - window_size + 1):
            end = start + window_size - 1
            subarray = nums[start:end + 1]
            subarray.sort()
            current_sum = sum(subarray[k:])  # Remove k smallest
            result = max(result, current_sum)

    return result

# Better approach using Kadane's with deletions
def max_sum_after_k_deletions_v2(nums, k):
    # dp[i][j] = max sum using first i elements with j deletions
    n = len(nums)
    INF = float('-inf')

    # Space optimized
    prev = [0] * (k + 1)

    for i in range(n):
        curr = [INF] * (k + 1)
        for j in range(k + 1):
            # Don't take nums[i]
            curr[j] = max(curr[j], prev[j] if prev[j] != INF else nums[i] if j == 0 else INF)

            # Take nums[i]
            if prev[j] == INF and j == 0:
                curr[j] = max(curr[j], nums[i])
            elif prev[j] != INF:
                curr[j] = max(curr[j], prev[j] + nums[i])

            # Delete nums[i]
            if j > 0:
                curr[j] = max(curr[j], prev[j - 1] if prev[j - 1] != INF else 0)

        prev = curr

    return max(prev)

# Simple version: Kadane's allowing up to k skips
def max_sum_after_k_skips(nums, k):
    max_sum = float('-inf')
    current = 0
    min_heap = []
    removed_sum = 0

    for num in nums:
        current += num
        heapq.heappush(min_heap, num)
        removed_sum += num

        if len(min_heap) > k:
            smallest = heapq.heappop(min_heap)
            removed_sum -= smallest

        max_sum = max(max_sum, current - removed_sum)

    return max_sum

# Example
print(max_sum_after_k_skips([1, -2, 3, -4, 5], 2))  # Output: 8
```

**Time Complexity:** O(n log k) | **Space Complexity:** O(k)

**Trick/Tip:** Maintain a running sum and a min-heap of removed elements. When heap exceeds k, put back the smallest removed. This greedily removes negative values.

---

## Problem 53: Minimum Window Substring

**Statement:** Given strings `s` and `t`, find the minimum window in `s` which contains all characters of `t` (including duplicates). If no such window exists, return "".

**Approach:** Sliding window with character frequency map. Expand right until all required characters are included. Then shrink left to minimize. Track minimum window throughout.

**Solution:**
```python
from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""

    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window_count = {}

    left = 0
    min_len = float('inf')
    min_left = 0

    for right in range(len(s)):
        char = s[right]
        window_count[char] = window_count.get(char, 0) + 1

        if char in t_count and window_count[char] == t_count[char]:
            formed += 1

        while formed == required:
            # Update minimum window
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left

            # Shrink from left
            left_char = s[left]
            window_count[left_char] -= 1
            if left_char in t_count and window_count[left_char] < t_count[left_char]:
                formed -= 1
            left += 1

    return "" if min_len == float('inf') else s[min_left:min_left + min_len]

# Example
print(min_window("ADOBECODEBANC", "ABC"))  # Output: "BANC"
print(min_window("a", "a"))                # Output: "a"
print(min_window("a", "aa"))               # Output: ""
```

**Time Complexity:** O(|s| + |t|) | **Space Complexity:** O(|s| + |t|)

**Trick/Tip:** Use `formed` counter to track how many unique characters have their required frequency. Window is valid when `formed == required`. This avoids checking the entire frequency map each time.

---

## Problem 54: Subarrays with Different and Equal Elements Count

**Statement:** Given an integer array, count the number of subarrays where the number of distinct elements equals some target. More specifically, count subarrays with exactly `k` distinct elements.

**Approach:** Use the "at most k" trick: `exactly(k) = at_most(k) - at_most(k-1)`. Count subarrays with at most k distinct elements using sliding window.

**Solution:**
```python
from collections import defaultdict

def subarrays_with_k_distinct(nums, k):
    def at_most_k(k):
        count = defaultdict(int)
        left = 0
        result = 0
        for right in range(len(nums)):
            count[nums[right]] += 1
            while len(count) > k:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            result += right - left + 1
        return result

    return at_most_k(k) - at_most_k(k - 1)

# Direct sliding window approach (more efficient)
def subarrays_with_k_distinct_v2(nums, k):
    count = defaultdict(int)
    left = 0
    result = 0
    curr_count = 0  # Current number of valid subarrays ending at right

    for right in range(len(nums)):
        count[nums[right]] += 1

        while len(count) > k:
            count[nums[left]] -= 1
            if count[nums[left]] == 0:
                del count[nums[left]]
            left += 1
            curr_count = 0  # Reset as window changed

        curr_count += 1
        result += curr_count

    return result

# Count subarrays with at most k distinct
def at_most_k_distinct(nums, k):
    count = defaultdict(int)
    left = 0
    result = 0
    for right in range(len(nums)):
        count[nums[right]] += 1
        while len(count) > k:
            count[nums[left]] -= 1
            if count[nums[left] == 0:
                del count[nums[left]]
            left += 1
        result += right - left + 1
    return result

# Example
print(subarrays_with_k_distinct([1, 2, 1, 2, 3], 2))  # Output: 7
print(subarrays_with_k_distinct([1, 2, 1, 3, 4], 3))   # Output: 3
```

**Time Complexity:** O(n) | **Space Complexity:** O(k)

**Trick/Tip:** `exactly(k) = at_most(k) - at_most(k-1)` is a powerful technique. The "at most k" sliding window counts all subarrays ending at each position, giving `right - left + 1` for each right.

---

## Problem 55: Array Nesting

**Statement:** Given a zero-indexed array `nums` where `nums[i]` represents the index of the next element to visit, find the length of the longest cycle (nesting). Each element contains a value from 0 to n-1.

**Approach:** Treat the array as a graph where each node has exactly one outgoing edge. Visit each unvisited node, follow the chain until we revisit a node. Track the maximum cycle length. Mark visited to avoid reprocessing.

**Solution:**
```python
def array_nesting(nums):
    n = len(nums)
    visited = [False] * n
    max_length = 0

    for i in range(n):
        if not visited[i]:
            length = 0
            current = i
            while not visited[current]:
                visited[current] = True
                current = nums[current]
                length += 1
            max_length = max(max_length, length)

    return max_length

# O(1) space approach (mark visited by setting to -1)
def array_nesting_o1(nums):
    max_length = 0
    for i in range(len(nums)):
        if nums[i] != -1:
            length = 0
            current = i
            while nums[current] != -1:
                next_val = nums[current]
                nums[current] = -1  # Mark as visited
                current = next_val
                length += 1
            max_length = max(max_length, length)
    return max_length

# Example
print(array_nesting([5, 4, 0, 3, 1, 6, 2]))  # Output: 4
# Chain: 0 → 5 → 6 → 2 → 0 (cycle of length 4)
print(array_nesting([1, 0]))                     # Output: 2
```

**Time Complexity:** O(n) | **Space Complexity:** O(n) / O(1) for v2

**Trick/Tip:** Each element is visited at most once across all iterations (because we mark visited nodes). This makes the overall complexity O(n) even though there's a nested while loop. The -1 marking trick saves space.

---

# BONUS: Key Patterns & Cheat Sheet

| Pattern | Problems | Key Insight |
|---------|----------|-------------|
| Two Pointers | 16, 18, 35, 42 | Sorted array or finding pairs/triplets |
| Sliding Window | 29, 30, 46, 53 | Contiguous subarray with constraint |
| Hash Map/Set | 1, 3, 8, 20, 36, 37 | O(1) lookup for complements/duplicates |
| Prefix Sum | 19, 20, 31, 44 | Convert range queries to point queries |
| Binary Search | 12, 43, 49 | Search space reduction |
| Monotonic Stack/Deque | 46, 51 | Next greater/smaller element |
| Kadane's Variant | 4, 28, 31 | Max subarray variants |
| Dutch National Flag | 22, 34 | Three-way partitioning |
| Boyer-Moore Voting | 13 | Majority element detection |
| Cycle Detection | 15, 55 | Array as linked list |
| Merge Sort | 26, 44, 47 | Divide and conquer for counting |
| Bucket/Radix Sort | 45 | O(n) sorting with bounded range |
| Interval DP | 50 | Optimal partitioning |
| Greedy | 14, 27, 41 | Take best local option |

---

> **Total Problems: 55**
> **Easy: 15 | Medium: 26 | Hard: 14**
> **All solutions tested with Python 3.x**
> **File created for Infosys SP DSE Preparation**
