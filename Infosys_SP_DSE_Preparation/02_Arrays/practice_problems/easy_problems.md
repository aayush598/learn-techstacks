# Easy Practice Problems - Arrays

## Problem 1: Two Sum (LeetCode 1)

**Problem:** Given an array of integers and a target, return indices of two numbers that add up to target.

**Constraints:**
- Each input has exactly one solution
- Cannot use the same element twice
- Return answer in any order

**Approach:**
1. Use hash map to store seen numbers and their indices
2. For each number, check if `target - num` exists in map
3. If yes, return both indices

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
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

**Time:** O(n) | **Space:** O(n)

**Similar Problems:**
- Two Sum II (sorted array) - use two pointer
- Three Sum - fix one, two pointer on rest
- Four Sum - two nested loops + two pointer

---

## Problem 2: Best Time to Buy and Sell Stock (LeetCode 121)

**Problem:** Find maximum profit from buying and selling a stock once.

**Constraints:**
- Must buy before selling
- If no profit possible, return 0

**Approach:**
1. Track minimum price seen so far
2. At each step, calculate profit if selling now
3. Update maximum profit

```python
def max_profit(prices):
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        min_price = min(min_price, price)
        profit = price - min_price
        max_profit = max(max_profit, profit)
    
    return max_profit

# Example
print(max_profit([7, 1, 5, 3, 6, 4]))  # 5 (buy at 1, sell at 6)
print(max_profit([7, 6, 4, 3, 1]))      # 0
```

**Time:** O(n) | **Space:** O(1)

**Similar Problems:**
- Best Time to Buy Sell Stock II (multiple transactions)
- Best Time to Buy Sell Stock with Cooldown
- Best Time to Buy Sell Stock with Transaction Fee

---

## Problem 3: Majority Element (LeetCode 169)

**Problem:** Find element appearing more than n/2 times. (Majority element always exists.)

**Constraints:**
- Array is non-empty
- Majority element always exists

**Approach (Boyer-Moore Voting Algorithm):**
1. Pick first element as candidate, count = 1
2. If same as candidate, count++. If different, count--
3. When count reaches 0, pick new candidate
4. Candidate at end is the majority element

```python
def majority_element(nums):
    candidate = nums[0]
    count = 1
    
    for i in range(1, len(nums)):
        if nums[i] == candidate:
            count += 1
        elif count == 0:
            candidate = nums[i]
            count = 1
        else:
            count -= 1
    
    return candidate

# Example
print(majority_element([3, 2, 3]))  # 3
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # 2
```

**Time:** O(n) | **Space:** O(1)

**Similar Problems:**
- Majority Element II (elements appearing > n/3 times)
- Check if majority element exists

---

## Problem 4: Best Time to Buy and Sell Stock II (LeetCode 122)

**Problem:** Find maximum profit with unlimited transactions (buy/sell multiple times).

**Constraints:**
- Cannot hold more than one share at a time
- Must sell before buying again

**Approach:**
1. Capture every upward price movement
2. Sum all positive differences between consecutive days

```python
def max_profit_ii(prices):
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit

# Example
print(max_profit_ii([7, 1, 5, 3, 6, 4]))  # 7 (buy@1 sell@5, buy@3 sell@6)
print(max_profit_ii([1, 2, 3, 4, 5]))      # 4 (buy@1 sell@5)
```

**Time:** O(n) | **Space:** O(1)

**Similar Problems:**
- Best Time to Buy Sell Stock (single transaction)
- Best Time to Buy Sell Stock III (at most 2 transactions)

---

## Problem 5: Contains Duplicate (LeetCode 217)

**Problem:** Return true if any value appears at least twice.

**Constraints:**
- Array length 1 to 10^5
- Values -10^9 to 10^9

**Approach 1 (Set):**
```python
def contains_duplicate(nums):
    return len(nums) != len(set(nums))
```

**Approach 2 (Sort + Check Adjacent):**
```python
def contains_duplicate_sort(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False
```

**Approach 3 (Hash Set - Early Exit):**
```python
def contains_duplicate_set(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

**Time:** O(n) set / O(n log n) sort | **Space:** O(n) set / O(1) sort

**Similar Problems:**
- Contains Duplicate II (within k distance)
- Contains Duplicate III (within index and value range)

---

## Tips for Easy Problems

1. **Hash map** is your best friend for O(n) lookups
2. **Sorting** often simplifies the problem
3. **Single pass** solutions exist for many problems
4. Always check for **edge cases**: empty array, single element, all same elements
5. **Boyer-Moore** algorithm is the gold standard for majority element
