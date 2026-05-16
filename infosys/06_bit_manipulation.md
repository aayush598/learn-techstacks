# Bit Manipulation

## Problem 1: Maximum XOR Subset (at most N/2 elements)
**Difficulty: Hard | Marks: 50**

Asked in Infosys SP/DSE exam - Khaled's maximum XOR with at most N/2 elements.

```python
from itertools import combinations

def max_xor_subset(arr):
    n = len(arr)
    max_xor = 0
    limit = n // 2

    # Split array into two halves (Meet in the Middle)
    left = arr[:n // 2]
    right = arr[n // 2:]

    # Generate all XORs for left half with their sizes
    left_xors = {}
    for r in range(len(left) + 1):
        for combo in combinations(left, r):
            x = 0
            for val in combo:
                x ^= val
            size = r
            if x not in left_xors or left_xors[x] > size:
                left_xors[x] = size

    # Generate all XORs for right half with their sizes
    right_xors = {}
    for r in range(len(right) + 1):
        for combo in combinations(right, r):
            x = 0
            for val in combo:
                x ^= val
            size = r
            if x not in right_xors or right_xors[x] > size:
                right_xors[x] = size

    # Combine
    for xor1, size1 in left_xors.items():
        for xor2, size2 in right_xors.items():
            if size1 + size2 <= limit:
                max_xor = max(max_xor, xor1 ^ xor2)

    return max_xor

print(max_xor_subset([1, 2]))
print(max_xor_subset([1, 2, 4, 7]))
```

### DP Solution (Alternative)

```python
def max_xor_subset_dp(arr):
    n = len(arr)
    M = 1 << 20
    dp = [float('inf')] * M
    dp[0] = 0
    for num in arr:
        if num == 0:
            continue
        new_dp = dp[:]
        for x in range(M):
            if dp[x] != float('inf'):
                new_dp[x ^ num] = min(new_dp[x ^ num], dp[x] + 1)
        dp = new_dp
    limit = n // 2
    for x in range(M - 1, -1, -1):
        if dp[x] <= limit:
            return x
    return 0

print(max_xor_subset_dp([1, 2]))
print(max_xor_subset_dp([1, 2, 4, 7]))
```

---

## Problem 2: Find the Number Appearing Once (Others Thrice)
**Difficulty: Medium | Marks: 30**

```python
def single_number_thrice(nums):
    ones = twos = 0
    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones
    return ones

nums = [2, 2, 3, 2]
print(single_number_thrice(nums))
```

---

## Problem 3: Single Number (Others Twice)
**Difficulty: Easy | Marks: 20**

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

nums = [4, 1, 2, 1, 2]
print(single_number(nums))
```

---

## Problem 4: Maximum XOR of Two Numbers in Array
**Difficulty: Medium | Marks: 30**

```python
def find_maximum_xor(nums):
    mask = max_xor = 0
    for i in range(31, -1, -1):
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}
        candidate = max_xor | (1 << i)
        for prefix in prefixes:
            if candidate ^ prefix in prefixes:
                max_xor = candidate
                break
    return max_xor

nums = [3, 10, 5, 25, 2, 8]
print(find_maximum_xor(nums))
```

---

## Problem 5: Count Set Bits
**Difficulty: Easy | Marks: 20**

```python
def count_set_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Brian Kernighan's Algorithm
def count_set_bits_kernighan(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count

print(count_set_bits_kernighan(29))
```

---

## Problem 6: Power of Two
**Difficulty: Easy | Marks: 20**

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

print(is_power_of_two(16))
print(is_power_of_two(18))
```

---

## Problem 7: Find Two Non-Repeating Numbers
**Difficulty: Medium | Marks: 30**

```python
def two_non_repeating(nums):
    xor_all = 0
    for num in nums:
        xor_all ^= num
    rightmost = xor_all & -xor_all
    x = y = 0
    for num in nums:
        if num & rightmost:
            x ^= num
        else:
            y ^= num
    return [x, y]

nums = [1, 2, 3, 2, 1, 4]
print(two_non_repeating(nums))
```

---

## Problem 8: Bitwise AND of Numbers Range
**Difficulty: Medium | Marks: 30**

```python
def range_bitwise_and(left, right):
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift

print(range_bitwise_and(5, 7))
print(range_bitwise_and(0, 0))
```

---

## Problem 9: Reverse Bits
**Difficulty: Easy | Marks: 20**

```python
def reverse_bits(n):
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result

print(reverse_bits(43261596))
```

---

## Problem 10: Subsets (Power Set)
**Difficulty: Medium | Marks: 30**

```python
def subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    return result

nums = [1, 2, 3]
print(subsets(nums))
```

---

## Problem 11: Smallest Power of 2 >= Each Number
**Difficulty: Easy | Marks: 20**

Asked in Infosys SP/DSE exam.

```python
def smallest_power_of_2(nums):
    result = []
    for num in nums:
        if num == 0:
            result.append(1)
        elif num & (num - 1) == 0:
            result.append(num)
        else:
            p = 1
            while p < num:
                p <<= 1
            result.append(p)
    return result

nums = [1, 10, 3, 16]
print(smallest_power_of_2(nums))
```

---

## Problem 12: Gray Code
**Difficulty: Medium | Marks: 30**

```python
def gray_code(n):
    result = []
    for i in range(1 << n):
        result.append(i ^ (i >> 1))
    return result

print(gray_code(2))
print(gray_code(3))
```

---

## Problem 13: XOR Queries of Subarray
**Difficulty: Medium | Marks: 30**

```python
def xor_queries(arr, queries):
    prefix = [0]
    for num in arr:
        prefix.append(prefix[-1] ^ num)
    return [prefix[l] ^ prefix[r + 1] for l, r in queries]

arr = [1, 3, 4, 8]
queries = [[0, 1], [1, 2], [0, 3], [3, 3]]
print(xor_queries(arr, queries))
```

---

## Problem 14: Count Number of Maximum Bitwise OR Subsets
**Difficulty: Medium | Marks: 30**

```python
def count_max_or_subsets(nums):
    max_or = 0
    for num in nums:
        max_or |= num
    count = 0
    n = len(nums)
    for mask in range(1 << n):
        curr_or = 0
        for i in range(n):
            if mask & (1 << i):
                curr_or |= nums[i]
        if curr_or == max_or:
            count += 1
    return count

nums = [3, 1]
print(count_max_or_subsets(nums))
```

---

## Problem 15: Minimize XOR
**Difficulty: Medium | Marks: 30**

```python
def minimize_xor(num1, num2):
    bits = bin(num2).count('1')
    result = 0
    for i in range(31, -1, -1):
        if bits == 0:
            break
        if num1 & (1 << i):
            result |= (1 << i)
            bits -= 1
    for i in range(32):
        if bits == 0:
            break
        if not (result & (1 << i)):
            result |= (1 << i)
            bits -= 1
    return result

print(minimize_xor(3, 5))
print(minimize_xor(1, 12))
```
