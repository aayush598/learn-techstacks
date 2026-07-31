# Easy Practice Problems - Arrays - Detailed Guide

## Problem 1: Two Sum (LeetCode 1)

**Problem Statement:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

**Constraints:**
- Each input has exactly one solution
- Cannot use the same element twice
- Return answer in any order

**Example:**
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

### Approach: Hash Map

**Why Hash Map?**
- We need to find two numbers that add to target
- For each number, we need to check if its complement exists
- Hash map gives O(1) lookup!

### Step-by-Step Walkthrough:

```
nums = [2, 7, 11, 15], target = 9

Step 1: Check num=2
        complement = 9 - 2 = 7
        Is 7 in hash map? No (map is empty)
        Store: {2: 0}
        
Step 2: Check num=7
        complement = 9 - 7 = 2
        Is 2 in hash map? Yes! (at index 0)
        Found! Return [0, 1]
```

### Visual:

```
Index:    0    1    2    3
Value:  [ 2 ] [ 7 ] [ 11 ] [ 15 ]
          ↑
       complement=7 (need)
       
Hash map after step 1: {2: 0}

       [ 2 ] [ 7 ] [ 11 ] [ 15 ]
               ↑
            complement=2 (need)
            Found in hash map!

Result: [0, 1] ✓
```

### The Code:
```python
def two_sum(nums, target):
    seen = {}  # num -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        
        # Check if complement exists in hash map
        if complement in seen:
            return [seen[complement], i]  # Found!
        
        # Store current number and its index
        seen[num] = i
    
    return []  # No solution found

# Example usage:
print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
```

**Time:** O(n) | **Space:** O(n)

---

## Problem 2: Best Time to Buy and Sell Stock (LeetCode 121)

**Problem Statement:** Given an array `prices` where `prices[i]` is the price of stock on day `i`, find maximum profit from one buy and one sell.

**Constraints:**
- Must buy before selling
- If no profit possible, return 0

**Example:**
```
Input: prices = [7, 1, 5, 3, 6, 4]
Output: 5
Explanation: Buy on day 1 (price=1), sell on day 4 (price=6), profit = 6-1 = 5
```

### Approach: Track Minimum Price

**Key Insight:** To maximize profit, buy at lowest price and sell at highest price after buying.

### Step-by-Step Walkthrough:

```
prices = [7, 1, 5, 3, 6, 4]

Day 0: price=7
       min_price = 7
       profit = 7 - 7 = 0
       max_profit = 0
       
Day 1: price=1
       min_price = 1 (new minimum!)
       profit = 1 - 1 = 0
       max_profit = 0
       
Day 2: price=5
       min_price = 1 (still minimum)
       profit = 5 - 1 = 4
       max_profit = 4 (new maximum!)
       
Day 3: price=3
       min_price = 1
       profit = 3 - 1 = 2
       max_profit = 4 (unchanged)
       
Day 4: price=6
       min_price = 1
       profit = 6 - 1 = 5
       max_profit = 5 (new maximum!)
       
Day 5: price=4
       min_price = 1
       profit = 4 - 1 = 3
       max_profit = 5 (unchanged)

Result: 5 ✓
```

### Visual:

```
prices = [7, 1, 5, 3, 6, 4]

    7 |  █
    6 |  █           █
    5 |  █   █       █
    4 |  █   █   █   █   █
    3 |  █   █   █   █   █
    2 |  █   █   █   █   █
    1 |  █   █   █   █   █
    0 +---+---+---+---+---+---
        0   1   2   3   4   5
            ↑           ↑
          BUY         SELL
        (min)        (max)
        
Profit = 6 - 1 = 5
```

### The Code:
```python
def max_profit(prices):
    min_price = float('inf')  # Start with infinity
    max_profit = 0
    
    for price in prices:
        # Update minimum price seen so far
        min_price = min(min_price, price)
        
        # Calculate profit if selling at current price
        profit = price - min_price
        
        # Update maximum profit
        max_profit = max(max_profit, profit)
    
    return max_profit

# Example usage:
print(max_profit([7, 1, 5, 3, 6, 4]))  # Output: 5
print(max_profit([7, 6, 4, 3, 1]))      # Output: 0 (no profit)
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 3: Majority Element (LeetCode 169)

**Problem Statement:** Find element appearing more than ⌊n/2⌋ times. (Majority element always exists.)

**Constraints:**
- Array is non-empty
- Majority element always exists

**Example:**
```
Input: nums = [2, 2, 1, 1, 1, 2, 2]
Output: 2
Explanation: 2 appears 4 times, which is > 7/2 = 3
```

### Approach: Boyer-Moore Voting Algorithm

**Key Insight:** Majority element appears more than n/2 times, so it will survive the "cancellation" process.

### Step-by-Step Walkthrough:

```
nums = [2, 2, 1, 1, 1, 2, 2]

Step 1: candidate=2, count=1

Step 2: num=2 (same as candidate)
        count = 2
        
Step 3: num=1 (different from candidate)
        count = 1
        
Step 4: num=1 (different from candidate)
        count = 0 → RESET!
        candidate=1, count=1
        
Step 5: num=1 (same as candidate)
        count = 2
        
Step 6: num=2 (different from candidate)
        count = 1
        
Step 7: num=2 (different from candidate)
        count = 0 → RESET!
        candidate=2, count=1

Final candidate: 2 ✓
```

### Visual:

```
nums = [2, 2, 1, 1, 1, 2, 2]
       
Step 1: [2] 2 1 1 1 2 2  → candidate=2, count=1
         ↑
         
Step 2: [2] [2] 1 1 1 2 2  → candidate=2, count=2
         ↑   ↑
         
Step 3: [2] [2] [1] 1 1 2 2  → candidate=2, count=1
         ↑   ↑   ↑
         
Step 4: 2  2  [1] [1] 1 2 2  → count=0, candidate=1, count=1
                  ↑
                  
Step 5: 2  2  1  [1] [1] 2 2  → candidate=1, count=2
                     ↑   ↑
                     
Step 6: 2  2  1  1  1  [2] 2  → candidate=1, count=1
                           ↑
                           
Step 7: 2  2  1  1  1  2  [2]  → count=0, candidate=2, count=1
                              ↑

Final candidate: 2
```

### Why it works:

```
Majority element (2) appears 4 times
Minority elements (1) appear 3 times

Even if all minority elements "cancel" one majority element:
4 - 3 = 1 majority element remains!

This is why majority element survives!
```

### The Code:
```python
def majority_element(nums):
    candidate = nums[0]
    count = 1
    
    for i in range(1, len(nums)):
        if nums[i] == candidate:
            count += 1
        elif count == 0:
            # No candidate, pick current element
            candidate = nums[i]
            count = 1
        else:
            count -= 1  # Cancel one majority with one minority
    
    return candidate

# Example usage:
print(majority_element([2, 2, 1, 1, 1, 2, 2]))  # Output: 2
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 4: Best Time to Buy and Sell Stock II (LeetCode 122)

**Problem Statement:** Find maximum profit with unlimited transactions.

**Constraints:**
- Cannot hold more than one share at a time
- Must sell before buying again

**Example:**
```
Input: prices = [7, 1, 5, 3, 6, 4]
Output: 7
Explanation: Buy@1, Sell@5 (profit=4), Buy@3, Sell@6 (profit=3)
             Total = 4 + 3 = 7
```

### Approach: Capture Every Upward Movement

**Key Insight:** We can make profit on every price increase!

### Step-by-Step Walkthrough:

```
prices = [7, 1, 5, 3, 6, 4]

Day 0→1: 7→1 (decrease) → no profit
Day 1→2: 1→5 (increase) → profit += 5-1 = 4
Day 2→3: 5→3 (decrease) → no profit
Day 3→4: 3→6 (increase) → profit += 6-3 = 3
Day 4→5: 6→4 (decrease) → no profit

Total profit = 4 + 3 = 7
```

### Visual:

```
prices = [7, 1, 5, 3, 6, 4]

    7 |  █
    6 |  █           █ ← SELL
    5 |  █   █ ← SELL █
    4 |  █   █   █   █   █
    3 |  █   █   █ ← BUY  █
    2 |  █   █   █   █   █
    1 |  █ ← BUY █   █   █
    0 +---+---+---+---+---+---
        0   1   2   3   4   5

Transactions: Buy@1, Sell@5, Buy@3, Sell@6
Profit: (5-1) + (6-3) = 4 + 3 = 7
```

### The Code:
```python
def max_profit_ii(prices):
    profit = 0
    
    for i in range(1, len(prices)):
        # Add profit whenever price increases
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    
    return profit

# Example usage:
print(max_profit_ii([7, 1, 5, 3, 6, 4]))  # Output: 7
print(max_profit_ii([1, 2, 3, 4, 5]))      # Output: 4
```

**Time:** O(n) | **Space:** O(1)

---

## Problem 5: Contains Duplicate (LeetCode 217)

**Problem Statement:** Return true if any value appears at least twice.

**Example:**
```
Input: nums = [1, 2, 3, 1]
Output: true (1 appears twice)

Input: nums = [1, 2, 3, 4]
Output: false (all unique)
```

### Approach 1: Hash Set

**Key Insight:** If set size < array size, there must be duplicates!

```python
def contains_duplicate(nums):
    return len(nums) != len(set(nums))
```

### Approach 2: Hash Set (Early Exit)

```python
def contains_duplicate_set(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True  # Found duplicate!
        seen.add(num)
    return False
```

### Approach 3: Sort + Check Adjacent

```python
def contains_duplicate_sort(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False
```

### Visual:

```
nums = [1, 2, 3, 1]

Set approach:
Step 1: num=1, seen={1}
Step 2: num=2, seen={1,2}
Step 3: num=3, seen={1,2,3}
Step 4: num=1, 1 in seen? Yes! Return True

Sort approach:
After sort: [1, 1, 2, 3]
Check: nums[0]=1 == nums[1]=1? Yes! Return True
```

**Time:** O(n) set / O(n log n) sort | **Space:** O(n) set / O(1) sort

---

## Summary Table

| # | Problem | Key Technique | Time | Space |
|---|---------|---------------|------|-------|
| 1 | Two Sum | Hash Map | O(n) | O(n) |
| 2 | Buy Sell Stock | Track Minimum | O(n) | O(1) |
| 3 | Majority Element | Boyer-Moore | O(n) | O(1) |
| 4 | Buy Sell Stock II | Greedy | O(n) | O(1) |
| 5 | Contains Duplicate | Hash Set | O(n) | O(n) |

## Common Mistakes & Edge Cases (All Easy Problems)

### Two Sum
- **Mistake:** Forgetting that the same element cannot be used twice.
  - If `nums = [3, 3]` and `target = 6`, you cannot use index 0 twice.
  - The hash map solve this naturally because we check BEFORE storing.
- **Mistake:** Using the value as key and index as value (wrong direction).
  - Always store `seen[num] = i` (number → index).
- **Edge case:** Two elements only → works fine, returns immediately at step 2.

### Best Time to Buy and Sell Stock
- **Mistake:** Updating `max_profit` before updating `min_price`.
  - Always update `min_price` FIRST in the loop.
- **Edge case:** Strictly decreasing prices `[7,6,4,3,1]` → profit = 0 (never sell at a loss).
- **Edge case:** Single price → profit = 0 (cannot buy and sell).

### Majority Element
- **Mistake:** Forgetting to handle `count == 0` check BEFORE the `else`.
  - If count is 0, the NEXT element becomes the new candidate, regardless of whether it matches.
- **Edge case:** Single element array → returns that element.

### Buy Sell Stock II
- **Mistake:** Confusing with Stock I — here we CAN hold multiple transactions.
- **Edge case:** `[1,2,3,4,5]` → Buy@1, Sell@5 → profit=4. Greedy catches all increases.
- **Edge case:** `[5,4,3,2,1]` → profit=0. No increases = no profit.

### Contains Duplicate
- **Mistake:** Using `set()` without considering it requires O(n) space.
- **Mistake:** In sort approach, forgetting to check `nums[i] == nums[i-1]` not `nums[i] == nums[i+1]`.
- **Edge case:** Empty array or single element → return False.

---

## Brute Force vs Optimal Comparison

```
┌─────────────────────────┬──────────────────┬──────────────────┐
│ Problem                 │ Brute Force      │ Optimal          │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Two Sum                 │ O(n²) nested     │ O(n) hash map    │
│                         │ loops checking   │ complement       │
│                         │ all pairs        │                  │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Buy Sell Stock I        │ O(n²) try every  │ O(n) track min   │
│                         │ buy-sell pair    │ in single pass   │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Majority Element        │ O(n) counting    │ O(n) Boyer-Moore │
│                         │ with extra hash  │ O(1) space       │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Buy Sell Stock II       │ O(n²) try every  │ O(n) greedy      │
│                         │ combination      │ capture all ↑    │
├─────────────────────────┼──────────────────┼──────────────────┤
│ Contains Duplicate      │ O(n²) nested     │ O(n) hash set    │
│                         │ comparison       │ or O(n log n)    │
└─────────────────────────┴──────────────────┴──────────────────┘
```

---

## Tips for Easy Problems

1. **Hash map** is your best friend for O(n) lookups
2. **Sorting** often simplifies the problem
3. **Single pass** solutions exist for many problems
4. Always check for **edge cases**: empty array, single element, all same elements
5. **Boyer-Moore** algorithm is the gold standard for majority element
6. **Pattern recognition:** If you need to find a pair with some property, think hash map or two pointer
7. **Always ask:** "Can I solve this in one pass?" before jumping to two-pass solutions
