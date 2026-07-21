# Infosys SP DSE - Previous Year Questions (Easy Level)

> 15 frequently asked easy-level questions from Infosys coding rounds.

---

## 1. Binary Array Conversion (Min Cost to All 0s or All 1s)

**Problem Statement:** Given a binary array, find the minimum cost to convert all elements to either all 0s or all 1s, where cost of flipping element at index i is abs(i - j) for swapping indices i and j.

**Approach:** Count positions of 0s and 1s. For each prefix, calculate running cost to make all elements same. Take minimum of two results.

```python
def min_cost_binary_conversion(arr):
    n = len(arr)
    count1 = sum(arr)
    count0 = n - count1

    cost0 = 0
    cost1 = 0
    for i in range(n):
        if arr[i] == 0:
            cost1 += i
        else:
            cost0 += i

    res = float('inf')
    c0, c1 = 0, 0
    for i in range(n):
        if arr[i] == 0:
            c0 += 1
            cost1 -= (n - 1 - i)
        else:
            c1 += 1
            cost0 -= (n - 1 - i)
        if c0 == count0 or c1 == count1:
            res = min(res, cost0, cost1)

    return res

# Alternative simpler approach
def min_cost_simple(arr):
    cost_to_all_ones = sum(1 for x in arr if x == 0)
    cost_to_all_zeros = sum(1 for x in arr if x == 1)
    return min(cost_to_all_ones, cost_to_all_zeros)

arr = [1, 0, 1, 0, 1]
print(min_cost_simple(arr))  # Output: 2
```

**Complexity:** O(n) time, O(1) space

**Tips:** For Infosys, always clarify if flipping means swapping or toggling. This question appeared in Infosys 2023.

---

## 2. Find Number of Pairs with Given Sum

**Problem Statement:** Given an array of integers and a target sum, find the number of pairs whose sum equals the target.

**Approach:** Use hash map to store frequency of each element. For each element, check if (target - element) exists.

```python
def count_pairs_with_sum(arr, target):
    from collections import Counter
    freq = Counter(arr)
    count = 0
    visited = set()

    for num in arr:
        complement = target - num
        if complement in freq:
            if num == complement:
                count += freq[num] * (freq[num] - 1) // 2
            elif num not in visited:
                count += freq[num] * freq[complement]
            visited.add(num)

    return count

arr = [1, 5, 7, -1, 5]
target = 6
print(count_pairs_with_sum(arr, target))  # Output: 3
```

**Complexity:** O(n) time, O(n) space

**Tips:** Handle duplicate elements carefully. When num == complement, use combination formula nC2.

---

## 3. Rotate Array by K Positions

**Problem Statement:** Given an array, rotate it to the right by k positions.

**Approach:** Use three reverses technique. Reverse entire array, then reverse first k elements, then reverse remaining.

```python
def rotate_array(arr, k):
    n = len(arr)
    k = k % n

    def reverse(nums, start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1

    reverse(arr, 0, n - 1)
    reverse(arr, 0, k - 1)
    reverse(arr, k, n - 1)
    return arr

arr = [1, 2, 3, 4, 5, 6, 7]
k = 3
print(rotate_array(arr, k))  # Output: [5, 6, 7, 1, 2, 3, 4]
```

**Complexity:** O(n) time, O(1) space

**Tips:** Always take k modulo n to handle k > n.

---

## 4. Find Majority Element

**Problem Statement:** Find the element that appears more than n/2 times in the array.

**Approach:** Boyer-Moore voting algorithm. Maintain a candidate and counter.

```python
def majority_element(arr):
    candidate = None
    count = 0

    for num in arr:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    # Verify candidate is actually majority
    if arr.count(candidate) > len(arr) // 2:
        return candidate
    return -1

arr = [2, 2, 1, 1, 1, 2, 2]
print(majority_element(arr))  # Output: 2
```

**Complexity:** O(n) time, O(1) space

**Tips:** Always verify the candidate after finding it. Infosys sometimes adds this twist.

---

## 5. Valid Palindrome (Remove at Most One Character)

**Problem Statement:** Check if string can be a palindrome after removing at most one character.

**Approach:** Use two pointers. When mismatch found, try skipping left or right character.

```python
def valid_palindrome(s):
    def is_palindrome(s, left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_palindrome(s, left + 1, right) or is_palindrome(s, left, right - 1)
        left += 1
        right -= 1
    return True

s = "abca"
print(valid_palindrome(s))  # Output: True
```

**Complexity:** O(n) time, O(1) space

**Tips:** This is a very common Infosys question. Practice edge cases like single character and empty string.

---

## 6. Find Missing Number in Array

**Problem Statement:** Given an array containing n distinct numbers from 0 to n, find the missing number.

**Approach:** Use XOR or formula sum of first n natural numbers.

```python
def find_missing_number(arr):
    n = len(arr)
    # Using formula
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum

# Using XOR (avoids overflow for very large arrays)
def find_missing_xor(arr):
    n = len(arr)
    xor_all = 0
    xor_arr = 0
    for i in range(n + 1):
        xor_all ^= i
    for num in arr:
        xor_arr ^= num
    return xor_all ^ xor_arr

arr = [3, 0, 1]
print(find_missing_number(arr))  # Output: 2
print(find_missing_xor(arr))     # Output: 2
```

**Complexity:** O(n) time, O(1) space

**Tips:** XOR approach is preferred in interviews as it demonstrates understanding of bit manipulation.

---

## 7. Maximum Subarray Sum (Kadane's Algorithm)

**Problem Statement:** Find the contiguous subarray with the largest sum.

**Approach:** Kadane's algorithm - maintain current sum and max sum.

```python
def max_subarray_sum(arr):
    max_sum = arr[0]
    current_sum = arr[0]

    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)

    return max_sum

# Variant: return the subarray itself
def max_subarray(arr):
    max_sum = arr[0]
    current_sum = arr[0]
    start = end = temp_start = 0

    for i in range(1, len(arr)):
        if arr[i] > current_sum + arr[i]:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum += arr[i]

        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i

    return arr[start:end + 1]

arr = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray_sum(arr))  # Output: 6
print(max_subarray(arr))      # Output: [4, -1, 2, 1]
```

**Complexity:** O(n) time, O(1) space

**Tips:** Infosys loves this question. Practice variants: max product subarray, circular max subarray sum.

---

## 8. Two Sum

**Problem Statement:** Given an array and target, find indices of two numbers that add up to target.

**Approach:** Hash map storing complement -> index.

```python
def two_sum(arr, target):
    seen = {}
    for i, num in enumerate(arr):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

arr = [2, 7, 11, 15]
target = 9
print(two_sum(arr, target))  # Output: [0, 1]
```

**Complexity:** O(n) time, O(n) space

**Tips:** Most asked question across all companies. Infosys may ask to return all pairs or count of pairs.

---

## 9. Best Time to Buy and Sell Stock

**Problem Statement:** Given prices array, find maximum profit by buying and selling once.

**Approach:** Track minimum price seen so far, calculate profit at each step.

```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        profit = price - min_price
        max_profit = max(max_profit, profit)

    return max_profit

prices = [7, 1, 5, 3, 6, 4]
print(max_profit(prices))  # Output: 5
```

**Complexity:** O(n) time, O(1) space

**Tips:** Practice variant: buy and sell multiple times (Greedy approach).

---

## 10. Contains Duplicate

**Problem Statement:** Check if array contains any duplicate element.

**Approach:** Use set and compare length.

```python
def contains_duplicate(arr):
    return len(arr) != len(set(arr))

# Without extra space (sorting approach)
def contains_duplicate_sort(arr):
    arr.sort()
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            return True
    return False

arr = [1, 2, 3, 1]
print(contains_duplicate(arr))  # Output: True
```

**Complexity:** O(n) time, O(n) space (set) or O(n log n) time, O(1) space (sort)

**Tips:** Simple but asked frequently. Always mention both approaches.

---

## 11. Merge Two Sorted Arrays

**Problem Statement:** Merge two sorted arrays into one sorted array.

**Approach:** Two pointer technique.

```python
def merge_sorted(arr1, arr2):
    result = []
    i = j = 0

    while i < len(arr1) and j < len(arr2):
        if arr1[i] <= arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1

    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result

arr1 = [1, 3, 5]
arr2 = [2, 4, 6]
print(merge_sorted(arr1, arr2))  # Output: [1, 2, 3, 4, 5, 6]
```

**Complexity:** O(n + m) time, O(n + m) space

**Tips:** Also practice merge in-place (when arr1 has enough space at end).

---

## 12. Move Zeros to End

**Problem Statement:** Move all zeros to end while maintaining order of non-zero elements.

**Approach:** Two pointer - one for position to place non-zero, one for scanning.

```python
def move_zeros(arr):
    pos = 0
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[pos], arr[i] = arr[i], arr[pos]
            pos += 1
    return arr

arr = [0, 1, 0, 3, 12]
print(move_zeros(arr))  # Output: [1, 3, 12, 0, 0]
```

**Complexity:** O(n) time, O(1) space

**Tips:** Do not use extra array. In-place solution is expected.

---

## 13. Plus One (Digit Array)

**Problem Statement:** Given a number represented as array of digits, increment it by one.

**Approach:** Start from last digit, handle carry.

```python
def plus_one(digits):
    n = len(digits)
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits

digits = [1, 2, 3]
print(plus_one(digits))  # Output: [1, 2, 4]

digits = [9, 9, 9]
print(plus_one(digits))  # Output: [1, 0, 0, 0]
```

**Complexity:** O(n) time, O(1) space (O(n) if new array created)

**Tips:** Edge case: all 9s requires returning new array with leading 1.

---

## 14. Single Number (XOR)

**Problem Statement:** Every element appears twice except one. Find the single number.

**Approach:** XOR all elements. a ^ a = 0, 0 ^ a = a.

```python
def single_number(arr):
    result = 0
    for num in arr:
        result ^= num
    return result

arr = [4, 1, 2, 1, 2]
print(single_number(arr))  # Output: 4
```

**Complexity:** O(n) time, O(1) space

**Tips:** Variants: single number appears once, others thrice (use bit counting).

---

## 15. Valid Parentheses

**Problem Statement:** Check if string of brackets is valid.

**Approach:** Use stack. Push opening brackets, pop on closing and match.

```python
def valid_parentheses(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)

    return len(stack) == 0

print(valid_parentheses("()[]{}"))  # Output: True
print(valid_parentheses("(]"))      # Output: False
```

**Complexity:** O(n) time, O(n) space

**Tips:** Infosys may add custom brackets or nested conditions.

---

## Summary Table

| # | Problem | Time | Space | Difficulty |
|---|---------|------|-------|------------|
| 1 | Binary Array Conversion | O(n) | O(1) | Easy |
| 2 | Pairs with Given Sum | O(n) | O(n) | Easy |
| 3 | Rotate Array | O(n) | O(1) | Easy |
| 4 | Majority Element | O(n) | O(1) | Easy |
| 5 | Valid Palindrome II | O(n) | O(1) | Easy |
| 6 | Missing Number | O(n) | O(1) | Easy |
| 7 | Kadane's Algorithm | O(n) | O(1) | Easy |
| 8 | Two Sum | O(n) | O(n) | Easy |
| 9 | Buy Sell Stock | O(n) | O(1) | Easy |
| 10 | Contains Duplicate | O(n) | O(n) | Easy |
| 11 | Merge Sorted Arrays | O(n+m) | O(n+m) | Easy |
| 12 | Move Zeros | O(n) | O(1) | Easy |
| 13 | Plus One | O(n) | O(1) | Easy |
| 14 | Single Number | O(n) | O(1) | Easy |
| 15 | Valid Parentheses | O(n) | O(n) | Easy |

> **Pro Tip:** Infosys SP L3 expects you to solve all easy questions in under 10 minutes each. Practice until these become second nature.
