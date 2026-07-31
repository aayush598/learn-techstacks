# Greedy & Backtracking Problems - Batch 2
## Infosys SP DSE Preparation | 40 Problems (20 Greedy + 20 Backtracking)
## Total: 40 problems with complete Python solutions

---

# PART A: GREEDY ALGORITHMS (20 Problems)

---

## Problem 1: Best Time to Buy and Sell Stock

**Problem Explanation:**
Given daily stock prices, find the maximum profit from buying once and selling once later. If no profit is possible (prices only decrease), return 0. The key insight: you don't need to track both buy and sell days — just track the minimum price seen so far and compute the maximum difference.

**Algorithm Steps:**
1. Initialize `min_price = infinity`, `max_profit = 0`
2. For each price in prices:
   a. Update `min_price = min(min_price, price)` (best day to buy so far)
   b. Compute `profit = price - min_price`
   c. Update `max_profit = max(max_profit, profit)`
3. Return `max_profit`

**Key Insight:**
The "minimum so far" greedy tracks the best possible buy price in a single pass. At each day, selling at today's price against the best past buy price gives the optimal profit for that sell day. Taking the maximum across all days finds the global optimum. This is Kadane's algorithm specialized for stock trading.

### Problem Statement
Given an array `prices` where `prices[i]` is the price of a stock on the i-th day, find the maximum profit from one buy-sell transaction. You must buy before you sell. If no profit possible, return 0.

### Examples
- Input: prices = [7,1,5,3,6,4] → Output: 5 (buy at 1, sell at 6)
- Input: prices = [7,6,4,3,1] → Output: 0 (no profit possible)

### Approach
Greedy single-pass: track the minimum price seen so far. At each day, calculate profit if sold today and update max profit. The key insight is that we only need to find the best buy-sell pair in one pass.

### Step-by-Step Trace
```
prices = [7, 1, 5, 3, 6, 4]
Day 0: min_price=7, profit=0
Day 1: min_price=1, profit=max(0, 1-1)=0
Day 2: min_price=1, profit=max(0, 5-1)=4
Day 3: min_price=1, profit=max(4, 3-1)=4
Day 4: min_price=1, profit=max(4, 6-1)=5
Day 5: min_price=1, profit=max(5, 4-1)=5
Result: 5
```

### Solution
```python
def maxProfit(prices):
    # min_price: cheapest price seen so far (best buy opportunity)
    min_price = float('inf')
    # max_profit: best profit seen so far
    max_profit = 0
    for price in prices:
        # Update the minimum price seen so far
        min_price = min(min_price, price)
        # Check if selling today gives a better profit
        max_profit = max(max_profit, price - min_price)
    return max_profit

# Test cases
print(maxProfit([7,1,5,3,6,4]))   # 5
print(maxProfit([7,6,4,3,1]))     # 0
print(maxProfit([1,2]))            # 1
print(maxProfit([2,4,1]))          # 2
print(maxProfit([]))               # 0
```

### Edge Cases
- Empty array → return 0
- Single element → return 0
- All decreasing prices → return 0
- Two elements, increasing → return difference

### Complexity
- **Time:** O(n) — single pass through array
- **Space:** O(1) — only two variables used

### Interview Tips
- Clarify: can we do multiple transactions? (No, this is single transaction version)
- Follow-up: what about transaction fee? (Different problem)
- **Common Mistakes:** Setting `min_price = prices[0]` without checking for empty array. Thinking you need nested loops to compare all buy-sell pairs.
- **Pattern Recognition:** "Best single transaction" → track min-so-far + Kadane's algorithm variant. Same as: Maximum Subarray (Problem 53), Maximum Difference Between Two Elements.

---

## Problem 2: Best Time to Buy and Sell Stock II

**Problem Explanation:**
Same stock prices as Problem 1, but now you can make **unlimited transactions** (buy, sell, buy again, etc.). You must sell before buying again. The greedy insight: capture every upward price movement by buying at local minima and selling at local maxima. Summing all positive day-to-day differences gives the maximum profit.

**Algorithm Steps:**
1. Initialize `profit = 0`
2. For each day `i` from 1 to n-1:
   a. If `prices[i] > prices[i-1]`: add the difference to profit
3. Return profit

**Key Insight:**
With unlimited transactions, every time the price goes up from day i-1 to day i, you could have bought at day i-1 and sold at day i. Summing all these "upward increments" equals buying at every local minimum and selling at every local maximum. This works because transactions can be back-to-back (sell on day i, buy on day i). Example: [1,2,3] → profit = (2-1)+(3-2) = 2 (same as buying at 1 and selling at 3).

### Problem Statement
Given an array `prices`, find the maximum profit from unlimited buy-sell transactions. You must sell before buying again.

### Examples
- Input: prices = [7,1,5,3,6,4] → Output: 7 (buy@1,sell@5 + buy@3,sell@6)
- Input: prices = [1,2,3,4,5] → Output: 4 (buy@1,sell@5)

### Approach
Greedy: collect every upward slope. Add all positive differences between consecutive days. This works because we can make unlimited transactions.

### Solution
```python
def maxProfit(prices):
    # Accumulate every positive price increase as profit
    profit = 0
    for i in range(1, len(prices)):
        # If price went up, capture that gain
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit

# Test cases
print(maxProfit([7,1,5,3,6,4]))   # 7
print(maxProfit([1,2,3,4,5]))     # 4
print(maxProfit([7,6,4,3,1]))     # 0
print(maxProfit([1]))              # 0
print(maxProfit([3,3,5,0,0,3,1,4]))  # 8
```

### Edge Cases
- Empty or single element → return 0
- Strictly increasing → sum of all differences
- All decreasing → return 0

### Complexity
- **Time:** O(n) — single pass
- **Space:** O(1) — one variable
- **Common Mistakes:** Thinking you need to track buy/sell days (not needed — just sum positive diffs). Using `max(0, prices[i] - prices[i-1])` which is equivalent but less explicit.
- **Pattern Recognition:** "Unlimited transactions" → sum all positive consecutive differences; Variant: with transaction fee (add fee to cost).

---

## Problem 3: Maximum 69 Number

**Problem Explanation:**
You're given a number containing only digits 6 and 9. You can flip at most one digit (6→9 only) to make the number as large as possible. Since 9 > 6, flipping any 6 to 9 increases the number. The leftmost 6 has the highest positional value, so flipping it gives the maximum increase.

**Algorithm Steps:**
1. Convert number to string, then to a mutable list
2. Find the first occurrence of '6' (leftmost)
3. Change that '6' to '9'
4. Convert back to integer and return

**Key Insight:**
Place value is everything — changing the thousands digit adds more value than changing the hundreds digit. So always flip the leftmost 6. This is a simpler special case of Maximum Swap (Problem 9).

### Problem Statement
Given a positive integer `num` consisting only of digits 6 and 9, return the maximum number you can get by changing at most one digit (6 to 9).

### Examples
- Input: 9669 → Output: 9969 (change first 6 to 9)
- Input: 9996 → Output: 9999 (change last 6 to 9)
- Input: 9999 → Output: 9999 (no change needed)

### Approach
Greedy: find the leftmost 6 and change it to 9. Leftmost change gives maximum value since it affects the highest place value.

### Solution
```python
def maximum69Number(num):
    # Convert to list of chars for mutation
    s = list(str(num))
    for i in range(len(s)):
        # Flip the leftmost 6 to 9 for maximum value gain
        if s[i] == '6':
            s[i] = '9'
            break
    return int(''.join(s))

# Test cases
print(maximum69Number(9669))   # 9969
print(maximum69Number(9996))   # 9999
print(maximum69Number(9999))   # 9999
print(maximum69Number(6))      # 9
print(maximum69Number(966969)) # 996969
```

### Complexity
- **Time:** O(d) where d is number of digits
- **Space:** O(d) for the list conversion
- **Edge Cases:** Single digit 6 → 9. All 9s → no change, return original.
- **Common Mistakes:** Flipping rightmost 6 instead of leftmost. Flipping a 9 to 6 (would decrease value).
- **Pattern Recognition:** "Maximize number by changing digit" → change leftmost upgradeable digit; Special case of Maximum Swap (Problem 9).

---

## Problem 4: Minimum Sum of Four Digits After Splitting

**Problem Explanation:**
You have a 4-digit number. Insert a '+' somewhere between digits to split it into two 2-digit numbers. Find the minimum possible sum. Since you can reorder digits (by forming any two numbers from the four digits), the greedy strategy is to put the two smallest digits in the tens place and the two largest in the ones place.

**Algorithm Steps:**
1. Extract all 4 digits, sort ascending
2. Form first number: `10 * smallest + second_smallest`
3. Form second number: `10 * third_smallest + largest`
4. Return their sum

**Key Insight:**
To minimize the sum of two 2-digit numbers, put the smallest digits in the tens place (they contribute 10× their value) and the largest in the ones place (they contribute 1×). So sort: [a,b,c,d] → numbers are `10a+b` and `10c+d`.

### Problem Statement
Given a four-digit integer `num`, split it into two two-digit numbers by adding a `+` between two digits. Find the minimum possible sum.

### Examples
- Input: 2932 → Output: 52 (23 + 29)
- Input: 4009 → Output: 13 (04 + 09)

### Approach
Greedy: sort all four digits. Smallest two form one number, largest two form another. Pairing smallest with smallest minimizes the sum.

### Solution
```python
def minimumSum(num):
    # Sort digits: smallest in tens place minimizes sum
    digits = sorted([int(d) for d in str(num)])
    return (digits[0] * 10 + digits[1]) + (digits[2] * 10 + digits[3])

# Test cases
print(minimumSum(2932))   # 52
print(minimumSum(4009))   # 13
print(minimumSum(1111))   # 22
print(minimumSum(9999))   # 198
```

### Complexity
- **Time:** O(1) — fixed 4 digits
- **Space:** O(1)
- **Edge Cases:** Leading zeros allowed (04 is valid). All same digits → result is `11+11=22` for 1111.
- **Common Mistakes:** Not sorting (trying to cut the original number in half). Confusing tens/ones placement.
- **Pattern Recognition:** "Minimum sum from digit rearrangement" → sort + place smallest in highest place value positions.

---

## Problem 5: Maximum Product of Two Elements in Array

**Problem Explanation:**
Given an array, pick two distinct elements to maximize `(nums[i]-1) * (nums[j]-1)`. Since the function is monotonic (larger nums[i] always gives larger product), the answer is simply the two largest elements. Find them efficiently.

**Algorithm Steps:**
1. Find the two largest distinct values in the array
2. Return `(largest - 1) * (second_largest - 1)`

**Key Insight:**
The function `f(x) = (x-1)` is increasing for all x ≥ 1. So maximizing the product means picking the two largest numbers. No need to check combinations.

### Problem Statement
Given an array `nums`, find the maximum value of `(nums[i]-1) * (nums[j]-1)` where i != j.

### Examples
- Input: [3,5,6,7] → Output: 30 ((7-1)*(6-1))
- Input: [1,5,4,5] → Output: 16 ((5-1)*(5-1))

### Approach
Track the two largest elements. Their product (minus 1 each) gives max result. Can use sorting or single-pass tracking.

### Solution
```python
def maxProduct(nums):
    import heapq
    # Two largest elements give maximum product
    a, b = heapq.nlargest(2, nums)
    return (a - 1) * (b - 1)

# Test cases
print(maxProduct([3, 5, 6, 7]))   # 30
print(maxProduct([1, 5, 4, 5]))   # 16
print(maxProduct([3, 3]))         # 4
print(maxProduct([10, 2, 8, 9]))  # 72
```

### Complexity
- **Time:** O(n) — single pass for two largest
- **Space:** O(1)
- **Edge Cases:** Only two elements: return `(nums[0]-1)*(nums[1]-1)`. Duplicate largest values: use both (like [5,5] → (5-1)*(5-1)=16).
- **Common Mistakes:** Sorting for O(n log n) when O(n) is possible. Forgetting the `-1` in the formula.
- **Pattern Recognition:** "Maximum product of two elements" → find two largest; same as finding top-2 in array.

---

## Problem 6: Minimum Sum of Three Numbers to Form a Number

**Problem Explanation:**
Given an array of digits, form three numbers using all digits (each exactly once) such that their sum is minimized. To minimize the sum, put the largest digits in the least significant positions (ones, tens, etc.) and the smallest in the most significant positions.

**Algorithm Steps:**
1. Sort digits ascending
2. Round-robin assign smallest three to ones place of three numbers
3. Next three to tens place, then hundreds, etc.
4. Sum the three numbers

**Key Insight:**
The weight of a digit in a number is its place value × digit value. To minimize total sum, assign the largest digits to the smallest place values (ones). Round-robin assignment (smallest→a, next→b, next→c, next→a, ...) distributes larger digits evenly.

### Problem Statement
Given a digit array `digits` (0-9), form three numbers from all digits such that their sum is minimized.

### Examples
- Input: [6,8,9,5,2] → Output: 246
- Input: [5,3,0,7,4] → Output: 57

### Approach
Greedy: sort digits. Assign largest digits to least significant positions of each number to minimize sum. Round-robin assign from least significant.

### Solution
```python
def minimumSum(digits):
    digits.sort()  # Ascending
    # Start with smallest digits as the first (most significant) digit of each number
    a, b, c = digits[0], digits[1], digits[2]
    place = 10  # Tens place
    # Distribute remaining digits in round-robin
    for i in range(3, len(digits), 3):
        a += digits[i] * place
        if i + 1 < len(digits):
            b += digits[i + 1] * place
        if i + 2 < len(digits):
            c += digits[i + 2] * place
        place *= 10  # Move to next place value
    return a + b + c

# Test cases
print(minimumSum([6, 8, 9, 5, 2]))   # 246
print(minimumSum([5, 3, 0, 7, 4]))   # 57
print(minimumSum([1, 2, 3]))          # 6
print(minimumSum([0, 0, 0, 0, 0]))   # 0
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)
- **Edge Cases:** Less than 3 digits: still works (remaining numbers are the initial ones). All zeros: sum=0.
- **Common Mistakes:** Not sorting in ascending order. Assigning digits to wrong place values. Off-by-one in round-robin loop.
- **Pattern Recognition:** "Minimum sum from digits" → sort + distribute smallest digits to highest place values.

---

## Problem 7: Count Pairs With Maximum XOR

**Problem Explanation:**
Given an array, count how many pairs have the maximum possible XOR value. XOR of two numbers is maximized when their bits differ as much as possible. First find the max XOR among all pairs, then count how many pairs achieve it.

**Algorithm Steps:**
1. First pass: find the maximum XOR value by checking all pairs (O(n²))
2. Second pass: count pairs whose XOR equals the maximum

**Key Insight:**
XOR is maximized when bits are opposite. The maximum XOR value is determined by the pair with the most different bit patterns. Since we need to both find the max and count occurrences, a two-pass brute force is the simplest approach. For optimization: Trie-based approach for O(n) max XOR.

### Problem Statement
Given an array `arr`, count the number of pairs (i, j) where i < j such that `arr[i] XOR arr[j]` is the maximum XOR value possible among all pairs.

### Examples
- Input: [1,2,3,4,5] → Output: 1
- Input: [5,9,5,6] → Output: 2

### Approach
Find the maximum XOR value first by checking all pairs. Then count pairs achieving that maximum XOR.

### Solution
```python
def countMaxXorPairs(arr):
    # First pass: find maximum XOR among all pairs
    max_xor = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            max_xor = max(max_xor, arr[i] ^ arr[j])
    # Second pass: count pairs achieving max XOR
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if (arr[i] ^ arr[j]) == max_xor:
                count += 1
    return count

# Test cases
print(countMaxXorPairs([1, 2, 3, 4, 5]))  # 1
print(countMaxXorPairs([5, 9, 5, 6]))     # 2
print(countMaxXorPairs([1, 1]))            # 0
print(countMaxXorPairs([3, 10, 5, 25, 2, 8]))  # 2
```

### Complexity
- **Time:** O(n²) — check all pairs twice
- **Space:** O(1)
- **Edge Cases:** All same numbers: XOR is always 0, max XOR = 0, count all pairs. Single element: no pairs → return 0.
- **Common Mistakes:** Only one pass (can't count max before knowing what max is). Forgetting i < j when counting.
- **Pattern Recognition:** "Maximum XOR pair" → brute force or Trie-based optimization; For O(n) solution, build binary Trie of numbers and query max XOR for each.

---

## Problem 8: Minimum Cost of Buying Candies With Discount

**Problem Explanation:**
You buy candies with a "buy 2, get the cheapest free" offer. You can group candies in any way. Find the minimum cost to buy all candies. The greedy strategy: sort by price descending, buy the two most expensive, get the next one free, and repeat.

**Algorithm Steps:**
1. Sort prices in descending order
2. Loop with step 3: take the first two in each group (pay for them), skip the third (free)
3. Return total

**Key Insight:**
To maximize savings, apply the "free" to the most expensive items you can avoid paying for. The third most expensive in each group of three is free. Sorting descending and processing in groups of three achieves this optimally.

### Problem Statement
Given an array `cost` where `cost[i]` is the price of the i-th candy, you get the cheapest free when buying two. Find the minimum cost to buy all candies.

### Examples
- Input: [6,5,7,9,2,2] → Output: 23
- Input: [5,5] → Output: 10
- Input: [1] → Output: 1

### Approach
Greedy: sort descending. Buy most expensive two, get third free. Repeat for all groups of three.

### Solution
```python
def minimumCost(cost):
    # Sort descending: maximize savings by making expensive items free
    cost.sort(reverse=True)
    total = 0
    # Take 2, skip 1 (free)
    for i in range(0, len(cost), 3):
        total += cost[i]          # Pay for first in group
        if i + 1 < len(cost):
            total += cost[i + 1]  # Pay for second in group
        # Third item is free — skip it
    return total

# Test cases
print(minimumCost([6, 5, 7, 9, 2, 2]))  # 23
print(minimumCost([5, 5]))               # 10
print(minimumCost([1]))                   # 1
print(minimumCost([1, 2, 3]))            # 3
print(minimumCost([7, 6, 5, 4, 3, 2, 1]))  # 19
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)
- **Edge Cases:** 1 or 2 candies: pay for all (no free candy). All same price: any grouping gives the same savings.
- **Common Mistakes:** Sorting ascending instead of descending. Including the third item in the total.
- **Pattern Reasoning:** "Buy 2 get 1 free" optimization → sort descending, group by 3; similar discount-pattern problems where grouping strategy matters.

---

## Problem 9: Maximum Swap

**Problem Explanation:**
Given a non-negative integer, you can swap any two digits at most once to create the maximum possible number. Unlike Maximum 69 Number (Problem 3), you can swap any two digits (not just 6→9). The strategy: find a position where a larger digit exists to its right — swap the leftmost such digit with the rightmost occurrence of the largest possible digit.

**Algorithm Steps:**
1. Convert to list of digits
2. Build a map: digit → last index where it appears
3. For each digit at index `i`:
   a. Check digits 9 down to (current digit + 1)
   b. If such a digit exists to the right: swap, return result
4. If no swap improves the number, return original

**Key Insight:**
To maximize the number, find the leftmost position where a larger digit exists on the right. Among those larger digits, pick the largest one; if multiple, use the rightmost occurrence (makes the number as large as possible after the swap).

### Problem Statement
Given a non-negative integer `num`, you can swap two digits at most once to get the maximum number. Return the maximum number.

### Examples
- Input: 2736 → Output: 7236 (swap 2 and 7)
- Input: 9973 → Output: 9973 (already maximum)
- Input: 98368 → Output: 98863 (swap 3 and 8)

### Approach
Greedy: for each position, find the largest digit to its right. If a larger digit exists, swap the rightmost occurrence of that largest digit with current position. Use last-occurrence map for efficiency.

### Solution
```python
def maximumSwap(num):
    digits = list(str(num))
    # Track the last index where each digit (0-9) appears
    last = {int(d): i for i, d in enumerate(digits)}
    # Scan left to right, try to find a larger digit to swap
    for i, d in enumerate(digits):
        # Try digits larger than current, from 9 down to (d+1)
        for k in range(9, int(d), -1):
            if k in last and last[k] > i:
                # Swap with the rightmost occurrence of the largest digit
                digits[i], digits[last[k]] = digits[last[k]], digits[i]
                return int(''.join(digits))
    return num  # Already maximum

# Test cases
print(maximumSwap(2736))    # 7236
print(maximumSwap(9973))    # 9973
print(maximumSwap(98368))   # 98863
print(maximumSwap(999))     # 999
print(maximumSwap(0))       # 0
```

### Complexity
- **Time:** O(n) where n is number of digits
- **Space:** O(n) for the last-position map
- **Edge Cases:** Single digit: return as-is. Already maximum (descending digits): return original. Zero: just return 0.
- **Common Mistakes:** Swapping with the first larger digit found (rightmost is better). Not checking for digits 9 down to current+1. Swapping when no improvement is possible.
- **Pattern Recognition:** "Maximum after one swap" → last-occurrence map + scan leftmost improvable position; generalization of Maximum 69 Number.

---

## Problem 10: Minimum Number of Platforms Required for Railway

**Problem Explanation:**
Given arrival and departure times of trains, find the minimum number of platforms needed at any time. When a train arrives, one platform is occupied. When it departs, the platform is freed. The peak concurrent usage determines the minimum platforms needed.

**Algorithm Steps:**
1. Sort arrival and departure times separately
2. Use two pointers: `i` for arrivals, `j` for departures
3. While there are more arrivals:
   a. If next arrival ≤ next departure: platform needed → increment count, move arrival pointer
   b. Else: platform freed → decrement count, move departure pointer
4. Track the maximum count reached

**Key Insight:**
By sorting both arrays, we simulate a sweep line over time. When an arrival happens before the next departure, we need an additional platform. When a departure happens first, a platform frees up. The maximum concurrent platforms is the answer. This avoids checking every time interval explicitly.

### Problem Statement
Given arrival and departure times of trains at a station, find the minimum number of platforms needed so that no train waits.

### Examples
- Input: arr=[900,940,950,1100,1500,1800], dep=[920,1200,1120,1130,1900,2000]
- Output: 3

### Approach
Sort both arrival and departure arrays. Use two pointers. Increment count when train arrives before one departs, decrement when one departs before next arrives.

### Solution
```python
def minPlatforms(arrival, departure):
    # Sort both arrays for sweep-line simulation
    arrival.sort()
    departure.sort()
    platforms = 0        # Current platforms in use
    max_platforms = 0    # Peak platforms required
    i = j = 0            # Pointers for arrival and departure
    
    while i < len(arrival):
        if arrival[i] <= departure[j]:
            # Train arrives before the next departure → need platform
            platforms += 1
            i += 1
            max_platforms = max(max_platforms, platforms)
        else:
            # Train departs before next arrival → platform freed
            platforms -= 1
            j += 1
    return max_platforms

# Test cases
print(minPlatforms([900, 940, 950, 1100, 1500, 1800],
                   [920, 1200, 1120, 1130, 1900, 2000]))  # 3
print(minPlatforms([100, 200, 300], [200, 300, 400]))       # 1
print(minPlatforms([100, 200], [100, 200]))                  # 2
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)
- **Edge Cases:** Single train: return 1. All trains arrive before any departs: platforms = n. Same arrival and departure times: departure happens first → platform freed before next arrival uses it.
- **Common Mistakes:** Not sorting (order must be chronological). Using `if arrival[i] < departure[j]` instead of `<=` (equal times = departure frees, then arrival uses). Off-by-one in loop bounds.
- **Pattern Recognition:** "Minimum platforms/rooms" → sweep-line with two pointers or min-heap; same as: Meeting Rooms II (Problem 14 in File 1).

---

## Problem 11: Job Sequencing Problem

**Problem Explanation:**
You have jobs, each with a deadline (must finish by that time) and a profit. Each job takes exactly 1 unit of time. You can do at most one job per time slot. Schedule jobs to maximize total profit. The greedy insight: process jobs in descending profit order and assign each to the latest possible free slot before its deadline.

**Algorithm Steps:**
1. Sort jobs by profit descending
2. Find the maximum deadline among all jobs
3. Create slots array (size = max deadline + 1), initialized to -1 (empty)
4. For each job: try to assign it to the latest free slot at or before its deadline
5. Return count of jobs scheduled and total profit

**Key Insight:**
Greedy by profit works because there's an exchange argument: if an optimal schedule doesn't include the highest-profit job, you can swap it in. Placing each job at the latest possible slot preserves earlier slots for other jobs with tighter deadlines.

### Problem Statement
Given jobs with deadlines and profits, schedule jobs to maximize profit. Each job takes 1 unit of time. A job earns profit only if completed by its deadline.

### Examples
- Input: jobs = [(1,2,100),(2,1,19),(3,2,27),(4,1,25),(5,1,15)]
- Output: (2, 127) — 2 jobs, profit 127

### Approach
Greedy: sort jobs by profit descending. For each job, assign it to the latest available slot before its deadline.

### Solution
```python
def jobSequencing(jobs):
    # Sort jobs by profit descending (greedy: most profitable first)
    jobs.sort(key=lambda x: x[2], reverse=True)
    max_deadline = max(j[1] for j in jobs)
    slots = [-1] * (max_deadline + 1)  # -1 = empty slot
    total_profit = count = 0
    for job in jobs:
        jid, deadline, profit = job
        # Find the latest free slot before deadline
        for t in range(deadline, 0, -1):
            if slots[t] == -1:   # Slot available
                slots[t] = jid   # Schedule job
                total_profit += profit
                count += 1
                break
    return count, total_profit

# Test cases
jobs = [(1,2,100), (2,1,19), (3,2,27), (4,1,25), (5,1,15)]
print(jobSequencing(jobs))  # (2, 127)
jobs2 = [(1,4,20), (2,1,10), (3,2,40), (4,2,30)]
print(jobSequencing(jobs2))  # (3, 90)
```

### Complexity
- **Time:** O(n²) — worst case checking slots
- **Space:** O(d) where d is max deadline
- **Edge Cases:** All jobs have deadline 1: only one job can be done (the most profitable). Max deadline large: slots array size = max deadline + 1.
- **Common Mistakes:** Not sorting by profit descending. Assigning to earliest slot instead of latest (earliest slot may be needed by a tighter-deadline job). Using 0-indexed slots incorrectly.
- **Pattern Recognition:** "Schedule jobs with deadlines" → sort by profit + latest-fit slot assignment; classic greedy problem from algorithmic lore.

---

## Problem 12: Fractional Knapsack

**Problem Explanation:**
You have items with weights and values, and a knapsack with capacity W. You can take fractions of items (unlike 0/1 Knapsack). Maximize the total value. The greedy: take items with the highest value-per-unit-weight first. Since you can take fractions, greedy is optimal here.

**Algorithm Steps:**
1. Pair each item by (value, weight)
2. Sort by value/weight ratio descending
3. For each item: take as much as capacity allows (whole item if possible, fraction otherwise)
4. Return total value

**Key Insight:**
Unlike 0/1 Knapsack (which requires DP), Fractional Knapsack is solvable by greedy because you can take any portion of an item. The optimal strategy is to always take the item with the best "bang for your buck" (value/weight ratio). Take it fully if it fits; otherwise take a fraction to fill the remaining capacity.

### Problem Statement
Given items with weights and values, and a knapsack of capacity W, maximize value. You can take fractions of items.

### Examples
- Input: weights=[10,20,30], values=[60,100,120], capacity=50
- Output: 240.0 (take all of item 1, all of item 2, half of item 3)

### Approach
Greedy: sort items by value-to-weight ratio descending. Take as much as possible of highest ratio items first.

### Solution
```python
def fractionalKnapsack(weights, values, capacity):
    # Sort by value/weight ratio descending
    items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0
    for v, w in items:
        if capacity >= w:
            total_value += v   # Take the whole item
            capacity -= w
        else:
            total_value += v * (capacity / w)  # Take a fraction
            break
    return total_value

# Test cases
print(fractionalKnapsack([10, 20, 30], [60, 100, 120], 50))  # 240.0
print(fractionalKnapsack([5, 10, 15], [10, 30, 20], 100))     # 80.0
print(fractionalKnapsack([1, 2, 3], [6, 8, 10], 5))           # 18.66...
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)
- **Edge Cases:** Capacity 0: Return 0. All items fit: take all. Single item: take min(full, fraction).
- **Common Mistakes:** Sorting by value instead of ratio. Forgetting to break after taking a fraction (capacity becomes 0). Using integer division.
- **Pattern Recognition:** "Fractional selection with capacity" → sort by ratio + greedy fill; fundamental greedy problem. Contrast: 0/1 Knapsack requires DP.

---

## Problem 13: Minimum Number of Coins

**Problem Explanation:**
Given coin denominations and a target amount, find the minimum number of coins needed. Greedy (taking largest coins first) works for standard coin systems like US/Indian denominations (1, 2, 5, 10, 25) but may fail for non-standard ones like [1, 3, 4] for amount 6 (greedy gives 4+1+1=3, optimal is 3+3=2).

**Algorithm Steps:**
1. Sort coins descending
2. For each coin: take as many as possible (while amount ≥ coin)
3. If amount reaches 0, return count; else return -1

**Key Insight:**
Greedy coin change works when the coin system is "canonical" — each coin is larger than the sum of all smaller coins (or has the "greedy choice property"). For arbitrary denominations, DP is needed. Always clarify with the interviewer if greedy is safe.

### Problem Statement
Given coin denominations and a target amount, find the minimum number of coins needed to make the amount.

### Examples
- Input: coins=[1,5,10,25], amount=30 → Output: 2 (25+5)
- Input: coins=[1,2,5], amount=11 → Output: 3 (5+5+1)

### Approach
Greedy: sort coins descending. Take as many of largest coin as possible, then move to next. Works for standard denominations.

### Solution
```python
def minCoins(coins, amount):
    # Sort descending for greedy (largest coins first)
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
    # If amount not zero, denominations couldn't make the change
    return count if amount == 0 else -1

# Test cases
print(minCoins([1, 5, 10, 25], 30))   # 2
print(minCoins([1, 2, 5], 11))         # 3
print(minCoins([2], 3))                 # -1
print(minCoins([1], 0))                 # 0
print(minCoins([1, 2, 5], 100))        # 20
```

### Complexity
- **Time:** O(n × amount) worst case (if coin=1, loop runs amount times)
- **Space:** O(1)
- **Edge Cases:** amount=0: Return 0. No combination possible: Return -1. Single coin type: works if coin divides amount, else -1.
- **Common Mistakes:** Assuming greedy always works (it doesn't for arbitrary denominations). Not checking if amount becomes 0 (return -1 case).
- **Pattern Recognition:** "Minimum coin change" → greedy for standard denominations, DP for general case; classic DP problem "Coin Change" (Leetcode 322) uses DP.

---

## Problem 14: Activity Selection Problem

**Problem Explanation:**
Given activities with start and finish times, select the maximum number of non-overlapping activities. This is the classic "interval scheduling" problem. The greedy: always pick the activity that finishes earliest, then skip all that overlap with it, and repeat.

**Algorithm Steps:**
1. Pair activities by (start, finish), sort by finish time ascending
2. Start with the first activity (earliest finish), set `last_finish`
3. For each remaining activity: if its start ≥ last_finish, select it and update `last_finish`
4. Return count

**Key Insight:**
Choosing the earliest-finishing activity leaves the most remaining time for other activities. This is provably optimal via exchange argument: any optimal solution can be transformed to include the earliest-finishing activity without reducing count.

### Problem Statement
Given n activities with start and finish times, select the maximum number of non-overlapping activities.

### Examples
- Input: start=[1,3,0,5,8,5], finish=[2,4,6,7,9,9]
- Output: 4

### Approach
Greedy: sort activities by finish time. Always pick the activity with earliest finish time that starts after the last selected activity ends.

### Solution
```python
def activitySelection(start, finish):
    # Sort by finish time (earliest finishing first)
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    count = 1  # Always pick the first activity
    last_finish = activities[0][1]
    for i in range(1, len(activities)):
        if activities[i][0] >= last_finish:
            count += 1          # This activity fits
            last_finish = activities[i][1]  # Update to its finish
    return count

# Test cases
print(activitySelection([1,3,0,5,8,5], [2,4,6,7,9,9]))  # 4
print(activitySelection([1,2,3], [2,3,4]))                 # 2
print(activitySelection([1,1,1], [2,2,2]))                 # 1
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)
- **Edge Cases:** Single activity: return 1. All overlapping: return 1. All non-overlapping: return n.
- **Common Mistakes:** Sorting by start instead of finish. Using `>` instead of `>=` for the start check (activity can start exactly when previous finishes).
- **Pattern Recognition:** "Maximum non-overlapping intervals" → sort by end, greedy pick; same as: Non-overlapping Intervals (File 1, Problem 13), Minimum Arrows (File 1, Problem 12).

---

## Problem 15: Minimum Absolute Sum Pair

**Problem Explanation:**
Given an array, find the pair of elements with the minimum absolute difference. After sorting, the closest elements in value will be adjacent. So just scan consecutive pairs in the sorted array.

**Algorithm Steps:**
1. Sort the array
2. Initialize `min_diff = infinity`
3. For each consecutive pair (i, i+1): compute absolute difference, update minimum
4. Return the pair with minimum difference

**Key Insight:**
In a sorted array, the closest values must be adjacent — a non-adjacent pair (i, i+2) has a difference at least as large as min(|arr[i+1]-arr[i]|, |arr[i+2]-arr[i+1]|). So the answer is always among adjacent elements.

### Problem Statement
Given an array, find a pair whose absolute difference is minimum.

### Examples
- Input: [1,5,3,19,18,25] → Output: (18, 19)
- Input: [4,1,-1,7,2] → Output: (-1, 1)

### Approach
Greedy: sort the array. Minimum difference must be between consecutive elements in sorted array.

### Solution
```python
def minAbsSumPair(arr):
    arr.sort()  # Sort: closest elements become adjacent
    min_diff = float('inf')
    result = (-1, -1)
    for i in range(len(arr) - 1):
        diff = abs(arr[i + 1] - arr[i])
        if diff < min_diff:
            min_diff = diff
            result = (arr[i], arr[i + 1])
    return result

# Test cases
print(minAbsSumPair([1, 5, 3, 19, 18, 25]))  # (18, 19)
print(minAbsSumPair([4, 1, -1, 7, 2]))        # (-1, 1)
print(minAbsSumPair([10, 20, 30, 40]))        # (10, 20)
print(minAbsSumPair([5, 5, 5]))               # (5, 5)
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)
- **Edge Cases:** Less than 2 elements: return (-1, -1) or handle separately. All equal elements: difference 0, return (x, x) for any pair.
- **Common Mistakes:** Using `<=` instead of `<` for updating (if there are ties, you might want the first or last pair). Not sorting (checking all pairs is O(n²) but also works).
- **Pattern Recognition:** "Closest pair in array" → sort + scan adjacent; same as: Minimum Difference Between Any Two Elements.

---

## Problem 16: Minimum Cost to Process Requests

**Problem Explanation:**
You have server requests (each with a size) and servers with a given capacity. Assign each request to a server. Minimize the number of servers used. This is a bin-packing variant: sort requests descending (largest first), assign each to the server with the most remaining capacity that can fit it ("best-fit").

**Algorithm Steps:**
1. Sort requests descending (largest first)
2. For each request: find a server with enough remaining capacity (best-fit: minimum remaining capacity ≥ request)
3. If found, deduct; else create a new server
4. Return total servers

**Key Insight:**
Processing largest requests first reduces waste — large items are harder to fit, so placing them early prevents them from being left out. The "best-fit" variant (placing each request in the tightest-fitting server) reduces fragmentation compared to "first-fit."

### Problem Statement
Given an array of request sizes and a server with processing capacity, find minimum number of servers needed using best-fit decreasing approach.

### Examples
- Input: requests=[4,2,5,3], capacity=8 → Output: 3
- Input: requests=[2,3,4], capacity=5 → Output: 2

### Approach
Greedy: sort requests descending. For each request, assign to server with most remaining capacity (best-fit). Create new server if none can accommodate.

### Solution
```python
def minServers(requests, capacity):
    # Sort descending: place largest requests first
    requests.sort(reverse=True)
    servers = []  # Remaining capacity of each server
    for req in requests:
        placed = False
        # Find server with enough remaining capacity (best-fit)
        for i in range(len(servers)):
            if servers[i] >= req:
                servers[i] -= req  # Place request on this server
                placed = True
                break
        if not placed:
            servers.append(capacity - req)  # Create new server
    return len(servers)

# Test cases
print(minServers([4, 2, 5, 3], 8))  # 3
print(minServers([2, 3, 4], 5))     # 2
print(minServers([1, 1, 1, 1], 2))  # 2
print(minServers([5], 5))            # 1
```

### Complexity
- **Time:** O(n²) — best-fit search for each request
- **Space:** O(n) for server array
- **Edge Cases:** Single request: return 1. All requests fit one server: return 1. Request exceeds capacity: impossible (assumed valid input).
- **Common Mistakes:** Not sorting (placement quality degrades significantly). Using "first-fit" instead of "best-fit" (may use more servers). Not updating remaining capacity correctly.
- **Pattern Recognition:** "Bin packing" → sort descending + best-fit; NP-hard problem, but greedy "first-fit decreasing" is a good approximation.

---

## Problem 17: Optimal Account Balancing

**Problem Explanation:**
Given money transfers between people, find the minimum number of additional settlements needed so everyone is settled (net balance = 0). Compute each person's net balance (total sent - total received). People with non-zero balance need to settle. Minimum settlements = non-zero count - 1 (one person can settle with everyone else).

**Algorithm Steps:**
1. Compute net balance for each person (sender pays, receiver gets)
2. Count people with non-zero balance
3. Return `max(0, non_zero_count - 1)`

**Key Insight:**
If k people have non-zero balances, at most k-1 transactions settle all debts. Think of it as: one person acts as the "bank" — everyone who owes pays them, and they pay everyone who is owed. This requires at most k-1 transfers.

### Problem Statement
Given a list of transactions where `transactions[i] = [from, to, amount]`, find the minimum number of settlements needed to settle all debts.

### Examples
- Input: [[0,1,10],[2,0,5]] → Output: 2
- Input: [[0,1,5],[1,2,5],[2,0,10]] → Output: 1

### Approach
Calculate net balance for each person. Count non-zero balances. Answer is `non_zero_count - 1`.

### Solution
```python
def minTransfers(transactions):
    from collections import Counter
    balance = Counter()
    # Compute net balance: sender loses money, receiver gains
    for frm, to, amt in transactions:
        balance[frm] -= amt
        balance[to] += amt
    # People with non-zero balance need to settle
    non_zero = [v for v in balance.values() if v != 0]
    # At most non_zero - 1 transfers needed
    return max(0, len(non_zero) - 1)

# Test cases
print(minTransfers([[0,1,10],[2,0,5]]))                  # 2
print(minTransfers([[0,1,5],[1,2,5],[2,0,10]]))          # 1
print(minTransfers([[0,1,5]]))                            # 1
print(minTransfers([[0,1,5],[0,2,5]]))                    # 2
```

### Complexity
- **Time:** O(n) where n is number of transactions
- **Space:** O(p) where p is number of people
- **Edge Cases:** All balanced already (all net = 0): return 0. Single transaction: 2 people, 1 non-zero? Actually 2 non-zero (one owes, one is owed) → 2-1=1 settlement needed.
- **Common Mistakes:** Halving the non-zero count (the formula is `count - 1`, not `count/2`). Forgetting the `max(0, ...)` for empty cases.
- **Pattern Reasoning:** "Minimum debt settlements" → net balance calculation; the `k-1` bound is a well-known result in debt simplification.

---

## Problem 18: Create Maximum Number from Two Arrays

**Problem Explanation:**
Given two arrays, form the maximum possible number of length k by taking some digits from each array in order (preserving original relative order within each array). This combines two subproblems: (1) picking the maximum subsequence of a given length from each array, and (2) merging two sequences to form the maximum overall sequence.

**Algorithm Steps:**
1. `pick_max(nums, t)`: extract the maximum subsequence of length t using a monotonic stack
2. `merge(a, b)`: greedily merge two sequences, always picking the larger remaining element
3. Try all possible splits of k between the two arrays, pick the best merged result

**Key Insight:**
The "monotonic stack" picks the maximum subsequence of length t by discarding smaller digits when larger ones appear later (if enough digits remain). The merge step uses lexicographic comparison: `if a[i:] > b[j:]` picks from the array that would give a lexicographically larger continuation.

### Problem Statement
Given two arrays `nums1` (length n) and `nums2` (length m), form a number of length k using at most n digits from nums1 and m from nums2, preserving relative order, to create the maximum number.

### Examples
- Input: nums1=[3,4,6,5], nums2=[9,1,2,5,8], k=3 → Output: [9,8,6]
- Input: nums1=[6,7], nums2=[6,0,4], k=5 → Output: [6,7,6,0,4]

### Approach
Greedy with monotonic stack. Extract top-k from each array for each possible split of k between arrays, then merge greedily.

### Solution
```python
def maxNumber(nums1, nums2, k):
    def pick_max(nums, t):
        """Get the max subsequence of length t from nums (monotonic stack)."""
        stack = []
        drop = len(nums) - t  # How many we can discard
        for num in nums:
            while stack and drop > 0 and stack[-1] < num:
                stack.pop()   # Discard smaller earlier digits
                drop -= 1
            stack.append(num)
        return stack[:t]  # Trim to exactly t elements

    def merge(a, b):
        """Merge two arrays to form the lexicographically largest result."""
        result = []
        i = j = 0
        while i < len(a) or j < len(b):
            # Pick from the array that gives a larger continuation
            if a[i:] > b[j:]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        return result

    best = []
    # Try all possible splits: take i from nums1, k-i from nums2
    for i in range(max(0, k - len(nums2)), min(len(nums1), k) + 1):
        a = pick_max(nums1, i)
        b = pick_max(nums2, k - i)
        merged = merge(a, b)
        if merged > best:
            best = merged
    return best

# Test cases
print(maxNumber([3,4,6,5], [9,1,2,5,8], 3))  # [9,8,6]
print(maxNumber([6,7], [6,0,4], 5))           # [6,7,6,0,4]
print(maxNumber([1], [1], 2))                  # [1,1]
```

### Complexity
- **Time:** O(k × (n + m)) for each split + O(k) per merge
- **Space:** O(k) for result
- **Edge Cases:** k = n + m: must use all digits from both arrays. k = 0: return [].
- **Common Mistakes:** Using simple sorting instead of monotonic stack (order must be preserved). Naive merge (picking locally max instead of lexicographically). Not considering all valid splits of k.
- **Pattern Recognition:** "Maximum number preserving order" → monotonic stack + greedy merge; Leetcode 321 (Hard) — combines two classic patterns.

---

## Problem 19: Minimum Cost to Make Array Equal

**Problem Explanation:**
Given an array of numbers and their per-unit change costs, find the value to make all elements equal that minimizes total cost. Changing an element by 1 unit costs `cost[i]`. The optimal target is the **weighted median** — the point where the cumulative cost crosses half of the total cost.

**Algorithm Steps:**
1. Pair (num, cost) and sort by num
2. Compute total cost
3. Find the weighted median: scan sorted pairs, accumulate cost until cumulative ≥ (total+1)//2
4. The weighted median is the target value
5. Compute sum of |num - target| × cost for each element

**Key Insight:**
For minimizing weighted absolute deviations, the optimal point is the weighted median (not the mean). The weighted median is the value where the cumulative weight first reaches or exceeds half the total weight. For equal costs, this reduces to the regular median.

### Problem Statement
Given arrays `nums` and `cost`, return the minimum total cost to make all elements equal. You can increase or decrease any element, paying `cost[i]` per unit change.

### Examples
- Input: nums=[1,3,5,2], cost=[2,3,1,14] → Output: 18
- Input: nums=[2,2,2,2,2], cost=[4,2,8,1,3] → Output: 0

### Approach
Greedy: the optimal target is the weighted median. Sort by nums, compute prefix sums of costs, find where cumulative cost crosses half.

### Solution
```python
def minCost(nums, cost):
    # Pair and sort by num to find weighted median
    pairs = sorted(zip(nums, cost))
    total = sum(cost)  # Total weight
    cumulative = 0
    target = 0
    # Find weighted median
    for num, c in pairs:
        cumulative += c
        if cumulative >= (total + 1) // 2:
            target = num  # Weighted median
            break
    # Compute total cost to move all elements to target
    return sum(abs(num - target) * c for num, c in pairs)

# Test cases
print(minCost([1,3,5,2], [2,3,1,14]))     # 18
print(minCost([2,2,2,2,2], [4,2,8,1,3]))   # 0
print(minCost([1,2,3], [1,1,1]))            # 2
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(n) for pairs
- **Edge Cases:** All same nums: return 0. Large cost variance: weighted median may differ significantly from regular median.
- **Common Mistakes:** Using regular median instead of weighted median. Not sorting before finding cumulative. Confusing `(total+1)//2` with `total//2`.
- **Pattern Recognition:** "Minimum cost to make equal" → weighted median; same as: Best Meeting Point (Leetcode 296) — 1D case.

---

## Problem 20: Maximum Performance of a Team

**Problem Explanation:**
You have engineers, each with a speed and efficiency score. Choose at most k engineers to form a team. The team's performance is (sum of speeds) × (minimum efficiency among chosen members). Maximize this value. The strategy: sort by efficiency descending, consider each engineer as the "minimum efficiency" of the team, and pick the k highest speeds among those with efficiency ≥ current.

**Algorithm Steps:**
1. Pair (efficiency, speed) and sort by efficiency descending
2. Maintain a min-heap of speeds (size ≤ k) and total_speed
3. For each engineer (as the minimum efficiency):
   a. Add speed to heap and total
   b. If heap size > k: remove smallest speed
   c. Compute performance = total_speed × current efficiency
   d. Track maximum
4. Return max % (10⁹+7)

**Key Insight:**
By sorting by efficiency descending, each engineer we process becomes the "worst" (minimum) efficiency in the team. We keep the k largest speeds among engineers with efficiency ≥ current. This transforms a 2D optimization into a 1D sweep.

### Problem Statement
Given n engineers with speed and efficiency, and integer k, choose at most k engineers to maximize (sum of speeds) * (minimum efficiency).

### Examples
- Input: n=6, speed=[2,10,3,1,5,8], efficiency=[5,4,3,9,7,2], k=3
- Output: 60

### Approach
Sort by efficiency descending. Use a min-heap to track top k speeds. At each efficiency level, compute team performance.

### Solution
```python
def maxPerformance(n, speed, efficiency, k):
    import heapq
    # Sort by efficiency descending: each becomes the "minimum" as we iterate
    engineers = sorted(zip(efficiency, speed), reverse=True)
    speed_heap = []      # Min-heap to keep k largest speeds
    total_speed = 0
    result = 0
    for eff, spd in engineers:
        total_speed += spd
        heapq.heappush(speed_heap, spd)
        if len(speed_heap) > k:
            # Remove smallest speed — we only keep top k
            total_speed -= heapq.heappop(speed_heap)
        # Current engineer's efficiency is the minimum (since we go descending)
        result = max(result, total_speed * eff)
    return result % (10**9 + 7)

# Test cases
print(maxPerformance(6, [2,10,3,1,5,8], [5,4,3,9,7,2], 3))  # 60
print(maxPerformance(6, [2,10,3,1,5,8], [5,4,3,9,7,2], 2))  # 60
print(maxPerformance(3, [2,3,5], [5,3,3], 2))                 # 24
```

### Complexity
- **Time:** O(n log n) — sorting + heap operations
- **Space:** O(n) for heap
- **Edge Cases:** k = n: Use all engineers (no speed dropping needed). k = 1: Pick engineer with max speed × efficiency. Large numbers: use modulo.
- **Common Mistakes:** Sorting by speed instead of efficiency. Using max-heap instead of min-heap for the speed tracking. Not considering teams with fewer than k members (allowed: "at most k").
- **Pattern Recognition:** "Maximum sum × min value" → sort by the "min" dimension + heap for top values; same technique as Min Cost to Hire K Workers (File 1, Problem 17) and IPO (File 1, Problem 16).

---

# PART B: BACKTRACKING (20 Problems)

---

## Problem 21: Subsets

**Problem Explanation:**
Given distinct integers, generate every possible subset (power set). Each element can be either included or excluded, giving 2ⁿ subsets. The empty set and the full set are both valid subsets. Add subsets at every node of the recursion tree (not just leaves).

**Algorithm Steps:**
1. Initialize result list
2. `backtrack(start, path)`: add current path to result, then for i from start to n-1: include nums[i], recurse with i+1, pop
3. Call backtrack(0, []) and return result

**Key Insight:**
The `start` index ensures each element is considered exactly once, preventing both reuse and duplicate orderings. Adding `path[:]` at every node (not just leaves) generates all 2ⁿ subsets.

### Problem Statement
Given a set of distinct integers `nums`, return all possible subsets (power set).

### Examples
- Input: [1,2,3] → Output: [[],[1],[1,2],[1,2,3],[1,3],[2],[2,3],[3]]
- Input: [0] → Output: [[],[0]]

### Approach
Backtracking: at each index, choose to include or exclude the current element. Build subset incrementally and add to result at each step.

### Backtracking Tree
```
[] 
├── [1]
│   ├── [1,2]
│   │   └── [1,2,3]
│   └── [1,3]
├── [2]
│   └── [2,3]
└── [3]
```

### Solution
```python
def subsets(nums):
    result = []
    def backtrack(start, current):
        # Add current subset at every node (not just leaves)
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)  # Explore with next index
            current.pop()              # Backtrack
    backtrack(0, [])
    return result

# Test cases
print(subsets([1, 2, 3]))
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
print(subsets([0]))
# [[], [0]]
print(subsets([]))
# [[]]
```

### Complexity
- **Time:** O(n × 2ⁿ) — 2ⁿ subsets, each copied O(n)
- **Space:** O(n) recursion depth
- **Common Mistakes:** Adding only at leaf nodes (missing intermediate subsets). Not copying path.
- **Pattern Recognition:** "All subsets/combinations" → backtrack with `start` index; fundamental template.

---

## Problem 22: Subsets II

**Problem Explanation:**
Same as Subsets but input may have duplicates. Avoid generating duplicate subsets (e.g., [1,2] should appear only once even if there are two 2's). Solution: sort first, skip duplicates at the same recursion level using `i > start and nums[i] == nums[i-1]`.

**Algorithm Steps:**
1. Sort nums (duplicates become adjacent)
2. Same backtracking as Subsets, but add: `if i > start and nums[i] == nums[i-1]: continue`
3. Call backtrack(0, []) and return result

**Key Insight:**
The skip condition `i > start` ensures we only skip at the same recursion level. If `i == start`, it's the first time we're using this value at this level, which is valid. The skip fires when we've already used the same value earlier at the same level.

### Problem Statement
Given a set of integers `nums` that may contain duplicates, return all unique subsets.

### Examples
- Input: [1,2,2] → Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
- Input: [0] → Output: [[],[0]]

### Approach
Backtracking with sorting. Skip duplicate elements at the same recursion level to avoid duplicate subsets.

### Solution
```python
def subsetsWithDup(nums):
    nums.sort()  # Sort so duplicates are adjacent
    result = []
    def backtrack(start, current):
        result.append(current[:])
        for i in range(start, len(nums)):
            # Skip duplicates at the SAME recursion level
            if i > start and nums[i] == nums[i - 1]:
                continue
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result

# Test cases
print(subsetsWithDup([1, 2, 2]))
# [[], [1], [1,2], [1,2,2], [2], [2,2]]
print(subsetsWithDup([0]))
# [[], [0]]
print(subsetsWithDup([1, 1, 2, 2]))
# [[],[1],[1,1],[1,1,2],[1,1,2,2],[1,2],[1,2,2],[2],[2,2]]
```

### Complexity
- **Time:** O(n × 2ⁿ) worst case (all distinct)
- **Space:** O(n) recursion depth
- **Common Mistakes:** Forgetting to sort. Using `if nums[i] == nums[i-1]` without `i > start` (skips too much).
- **Pattern Recognition:** "Unique subsets with duplicates" → sort + same-level skip with `i > start`.

---

## Problem 23: Permutations

**Problem Explanation:**
Given distinct integers, generate every possible ordering (permutation). Unlike subsets, [1,2] and [2,1] are different. Use swap-based backtracking — swap each element into the current position, recurse for the rest, then swap back.

**Algorithm Steps:**
1. Base: if `start == len(nums)`, add copy of nums to result
2. For i from start to n-1: swap nums[start] and nums[i], recurse on start+1, swap back
3. Call backtrack(0) and return result

**Key Insight:**
The swap approach avoids a separate `used[]` array by modifying the array in-place. Each element gets placed exactly once at each position, generating all n! permutations.

### Problem Statement
Given a collection of distinct integers `nums`, return all possible permutations.

### Examples
- Input: [1,2,3] → Output: 6 permutations
- Input: [0,1] → Output: [[0,1],[1,0]]

### Approach
Backtracking: swap elements to place each number at current position, then recurse for remaining positions.

### Solution
```python
def permute(nums):
    result = []
    def backtrack(start):
        if start == len(nums):
            # Copy current arrangement
            result.append(nums[:])
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]  # Swap i into start position
            backtrack(start + 1)                          # Permute remaining
            nums[start], nums[i] = nums[i], nums[start]  # Swap back (backtrack)
    backtrack(0)
    return result

# Test cases
print(permute([1, 2, 3]))
# [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,2,1],[3,1,2]]
print(permute([0, 1]))
# [[0,1],[1,0]]
print(permute([1]))
# [[1]]
```

### Complexity
- **Time:** O(n × n!) — n! permutations
- **Space:** O(n) recursion depth
- **Common Mistakes:** Not copying nums before appending. Swap approach modifies original array.
- **Pattern Recognition:** "All arrangements" → swap-based or used[]-based backtracking; n! complexity.

---

## Problem 24: Permutations II

**Problem Explanation:**
Same as Permutations but input may have duplicates. Avoid duplicate permutations. The skip condition differs from Subsets II: for permutations, use `used[i-1] is False` to skip duplicates at the same level.

**Algorithm Steps:**
1. Sort nums
2. `backtrack(path, used)`: if len(path)==len(nums), add. For each i: skip if used[i] or if `nums[i]==nums[i-1] and not used[i-1]`
3. Call backtrack([], [False]*len(nums))

**Key Insight:**
The condition `nums[i]==nums[i-1] and not used[i-1]` ensures we only allow the first occurrence of a duplicate value at each recursion level. If the previous identical element is NOT used, it means we're starting a new level where the previous occurrence was already processed — skip.

### Problem Statement
Given a collection of integers `nums` that may contain duplicates, return all unique permutations.

### Examples
- Input: [1,1,2] → Output: [[1,1,2],[1,2,1],[2,1,1]]
- Input: [1,2,3] → Output: same as Permutations

### Approach
Backtracking with sorting. Skip duplicate elements at the same recursion level using visited array and duplicate check.

### Solution
```python
def permuteUnique(nums):
    nums.sort()
    result = []
    def backtrack(current, used):
        if len(current) == len(nums):
            result.append(current[:])
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: only allow first among equal values at this level
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            used[i] = True
            current.append(nums[i])
            backtrack(current, used)
            current.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result

# Test cases
print(permuteUnique([1, 1, 2]))
# [[1,1,2],[1,2,1],[2,1,1]]
print(permuteUnique([1, 2, 3]))
# [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
```

### Complexity
- **Time:** O(n × n!) worst case
- **Space:** O(n) recursion depth + visited array
- **Common Mistakes:** Using Subsets II skip (`i > start`) which doesn't work without a `start` parameter.
- **Pattern Recognition:** "Unique permutations with duplicates" → `not used[i-1]` skip condition.

---

## Problem 25: Combinations

**Problem Explanation:**
Given n (numbers 1..n) and k (size), generate all combinations of k numbers. Order doesn't matter — [1,2] and [2,1] are the same. Use backtracking with a `start` parameter to avoid duplicates and only move forward.

**Algorithm Steps:**
1. `backtrack(start, path)`: if len(path)==k, add to result
2. For i from start to n: append i, recurse with i+1, pop
3. Call backtrack(1, [])

**Key Insight:**
Same as subsets, but only add to result at leaf nodes (when path length = k). The `start = i+1` prevents reusing numbers and ensures combinations are in ascending order, avoiding duplicates.

### Problem Statement
Given two integers n and k, return all possible combinations of k numbers from 1 to n.

### Examples
- Input: n=4, k=2 → Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
- Input: n=1, k=1 → Output: [[1]]

### Approach
Backtracking: build combination incrementally, start from previous number + 1 to avoid duplicates.

### Solution
```python
def combine(n, k):
    result = []
    def backtrack(start, current):
        # Only add at leaf (when we have k elements)
        if len(current) == k:
            result.append(current[:])
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)  # Move to next number
            current.pop()
    backtrack(1, [])
    return result

# Test cases
print(combine(4, 2))
# [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
print(combine(1, 1))
# [[1]]
print(combine(5, 3))
# [[1,2,3],[1,2,4],[1,2,5],[1,3,4],[1,3,5],[1,4,5],[2,3,4],[2,3,5],[2,4,5],[3,4,5]]
```

### Complexity
- **Time:** O(k × C(n,k)) — combinations
- **Space:** O(k) recursion depth
- **Common Mistakes:** Adding path at every node (like subsets) instead of only at leaf nodes.
- **Pattern Recognition:** "All combinations of size k" → backtrack with `start = i+1`, leaf-node addition; subset of the subset/combination family.

---

## Problem 26: Combination Sum

**Problem Explanation:**
Given unique candidates and a target, find all unique combinations summing to target. Candidates can be **reused unlimited times**. Sort + backtrack with `i` (not i+1) in recursive call to allow reuse. Early break when candidate > remaining.

**Algorithm Steps:**
1. Sort candidates (for pruning)
2. `backtrack(start, path, remaining)`: if remaining==0, add. For i from start: if candidate > remaining, break. Append, recurse with i (reuse!), pop
3. Call backtrack(0, [], target)

**Key Insight:**
The key design: `backtrack(i, ...)` (with i, not i+1) allows reusing the same candidate. The `start` parameter ensures non-decreasing order preventing duplicates like [2,3] and [3,2].

### Problem Statement
Given candidate numbers (no duplicates) and a target, find all unique combinations where candidates sum to target. Same number may be reused unlimited times.

### Examples
- Input: candidates=[2,3,6,7], target=7 → Output: [[2,2,3],[7]]
- Input: candidates=[2,3,5], target=8 → Output: [[2,2,2,2],[2,3,3],[3,5]]

### Approach
Backtracking: at each step, try each candidate >= last chosen. Allow reuse by not incrementing start index. Prune when remaining < candidate.

### Solution
```python
def combinationSum(candidates, target):
    result = []
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # Prune: sorted, so rest are too large
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])  # i (not i+1) = reuse!
            current.pop()
    candidates.sort()
    backtrack(0, [], target)
    return result

# Test cases
print(combinationSum([2,3,6,7], 7))
# [[2,2,3],[7]]
print(combinationSum([2,3,5], 8))
# [[2,2,2,2],[2,3,3],[3,5]]
print(combinationSum([1], 1))
# [[1]]
print(combinationSum([1], 2))
# [[1,1]]
```

### Complexity
- **Time:** O(N^(T/M)) — branching factor N, depth T/M
- **Space:** O(T/M) recursion depth
- **Common Mistakes:** Using `i+1` (disables reuse). Not sorting (break optimization fails).
- **Pattern Recognition:** "Combinations with unlimited reuse" → backtrack with i (not i+1).

---

## Problem 27: Combination Sum II

**Problem Explanation:**
Same as Combination Sum I but candidates may have duplicates and each can be used at most once. Combines the "no reuse" (i+1) from combinations with the "skip duplicates" (i > start) from Subsets II.

**Algorithm Steps:**
1. Sort candidates
2. `backtrack(start, path, remaining)`: if remaining==0, add. For i from start: skip duplicates at same level, break if too large. Append, recurse with i+1, pop.
3. Call backtrack(0, [], target)

**Key Insight:**
Two differences from Combination Sum I: (1) `i+1` prevents reuse, (2) `i > start and candidates[i]==candidates[i-1]` skips same-level duplicates.

### Problem Statement
Given candidate numbers (may contain duplicates) and a target, find unique combinations summing to target. Each number used at most once.

### Examples
- Input: candidates=[10,1,2,7,6,1,5], target=8
- Output: [[1,1,6],[1,2,5],[1,7],[2,6]]

### Approach
Backtracking with sorting. Skip duplicates at same recursion level. Increment start index (no reuse).

### Solution
```python
def combinationSum2(candidates, target):
    candidates.sort()
    result = []
    def backtrack(start, current, remaining):
        if remaining == 0:
            result.append(current[:])
        for i in range(start, len(candidates)):
            # Skip duplicates at same recursion level
            if i > start and candidates[i] == candidates[i-1]:
                continue
            if candidates[i] > remaining:
                break  # Prune: sorted, rest too large
            current.append(candidates[i])
            backtrack(i + 1, current, remaining - candidates[i])  # i+1 = no reuse
            current.pop()
    backtrack(0, [], target)
    return result

# Test cases
print(combinationSum2([10,1,2,7,6,1,5], 8))
# [[1,1,6],[1,2,5],[1,7],[2,6]]
print(combinationSum2([2,5,2,1,2], 5))
# [[1,2,2],[5]]
print(combinationSum2([1,1,1,1,1,1,1,1,1,1], 2))
# [[1,1]]
```

### Complexity
- **Time:** O(2ⁿ) — each element included or excluded
- **Space:** O(target/min) recursion depth
- **Common Mistakes:** Using `i` instead of `i+1` (enables reuse). Not sorting (duplicate skip fails).
- **Pattern Recognition:** "Combinations with duplicates, no reuse" → hybrid of Subsets II and Combination Sum I patterns.

---

## Problem 28: Combination Sum III

**Problem Explanation:**
Find all combinations of exactly k distinct numbers from 1-9 that sum to n. Numbers 1-9, each at most once. Fixed small search space (9 choose k ≤ 126). Backtrack with pruning.

**Algorithm Steps:**
1. `backtrack(start, path, remaining)`: if len==k and remaining==0, add. For i from start to 9: if i > remaining, break. Append, recurse with i+1, pop.
2. Call backtrack(1, [], n)

**Key Insight:**
The search space is bounded (1-9, max depth 9). Pruning: if remaining < i, break (since sorted, all later numbers are larger too). No need for duplicate skipping since numbers are unique.

### Problem Statement
Find all combinations of k numbers that sum to n, using numbers 1-9 only once each.

### Examples
- Input: k=3, n=7 → Output: [[1,2,4]]
- Input: k=3, n=9 → Output: [[1,2,6],[1,3,5],[2,3,4]]

### Approach
Backtracking: try numbers 1-9, skip if already used. Prune when sum exceeds target or remaining numbers insufficient.

### Solution
```python
def combinationSum3(k, n):
    result = []
    def backtrack(start, current, remaining):
        if len(current) == k and remaining == 0:
            result.append(current[:])
        for i in range(start, 10):
            if i > remaining:
                break  # Prune: rest are also > remaining
            current.append(i)
            backtrack(i + 1, current, remaining - i)
            current.pop()
    backtrack(1, [], n)
    return result

# Test cases
print(combinationSum3(3, 7))
# [[1,2,4]]
print(combinationSum3(3, 9))
# [[1,2,6],[1,3,5],[2,3,4]]
print(combinationSum3(2, 18))
# [] (max sum of 2 from 1-9 is 17)
print(combinationSum3(4, 10))
# [[1,2,3,4]]
```

### Complexity
- **Time:** O(C(9,k)) — combinations of 9 choose k
- **Space:** O(k) recursion depth
- **Common Mistakes:** Starting from 0 instead of 1. Not pruning when i > remaining.
- **Pattern Recognition:** "Fixed-set combinations" → bounded backtracking with 1-9 range.

---

## Problem 29: Palindrome Partitioning

**Problem Explanation:**
Given a string, partition it into substrings where each substring is a palindrome. Return all possible partitions. At each position, try all possible ending positions where the substring is a palindrome, then recurse on the remainder.

**Algorithm Steps:**
1. `backtrack(start, path)`: if start==len(s), add. For end from start+1 to len(s): if s[start:end] is palindrome, append, recurse from end, pop.
2. Call backtrack(0, [])

**Key Insight:**
Try every possible cut point. Each palindrome substring is a valid segment. Recurse on the rest. Since single characters are always palindromes, every string has at least one valid partition. This is a "partition" problem analogous to Restore IP Addresses.

### Problem Statement
Given a string `s`, partition it such that every substring is a palindrome. Return all valid partitionings.

### Examples
- Input: "aab" → Output: [["a","a","b"],["aa","b"]]
- Input: "a" → Output: [["a"]]

### Approach
Backtracking: try every possible partition point. Check if substring is palindrome, then recurse on remainder.

### Solution
```python
def partition(s):
    result = []
    def is_palindrome(sub):
        return sub == sub[::-1]  # Check palindrome
    def backtrack(start, current):
        if start == len(s):
            result.append(current[:])
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                current.append(s[start:end])
                backtrack(end, current)  # Recurse on remainder
                current.pop()
    backtrack(0, [])
    return result

# Test cases
print(partition("aab"))
# [["a","a","b"],["aa","b"]]
print(partition("a"))
# [["a"]]
print(partition("aba"))
# [["a","b","a"],["aba"]]
print(partition("aaa"))
# [["a","a","a"],["a","aa"],["aa","a"],["aaa"]]
```

### Complexity
- **Time:** O(n × 2ⁿ) — 2ⁿ partitions, palindrome check O(n)
- **Space:** O(n) recursion depth
- **Common Mistakes:** Off-by-one in `range(start+1, len(s)+1)`. Not handling single-character palindromes.
- **Pattern Recognition:** "String partitioning with constraints" → substring-boundary backtracking; same pattern: Restore IP Addresses.

---

## Problem 30: Word Search

**Problem Explanation:**
Given a 2D grid of letters and a word, can you trace the word through adjacent (up/down/left/right) cells? Each cell used at most once. Classic DFS + backtracking: start from each matching cell, explore 4 directions with in-place visited marking.

**Algorithm Steps:**
1. For each cell: if character matches first letter, start DFS
2. DFS: if idx==len(word): return True. If out of bounds or mismatch: return False. Mark cell '#', explore 4 directions, restore cell.
3. Return True if any DFS finds the word

**Key Insight:**
In-place marking with `'#'` avoids a separate visited set. The 4-directional DFS explores all paths. Backtracking (restoring the cell) is critical — without it, valid paths through different branches would be blocked.

### Problem Statement
Given a 2D board and a word, find if the word exists in the grid. Letters must be adjacent (not diagonal) and each cell used at most once.

### Examples
- Board: [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word="ABCCED" → True
- Same board, word="ABCB" → False

### Approach
Backtracking: start from each cell matching first letter. Explore 4 directions, mark visited cells with '#'.

### Solution
```python
def exist(board, word):
    rows, cols = len(board), len(board[0])
    def backtrack(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False
        temp = board[r][c]
        board[r][c] = '#'  # Mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            if backtrack(r+dr, c+dc, idx+1):
                return True
        board[r][c] = temp  # Restore (backtrack)
        return False
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0):
                return True
    return False

# Test cases
print(exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED"))  # True
print(exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB"))    # False
print(exist([["a","b"],["c","d"]], "acdb"))  # True
```

### Complexity
- **Time:** O(m × n × 4^L) — each start cell, 4 branches per character
- **Space:** O(L) recursion depth
- **Common Mistakes:** Not restoring cell after DFS. Checking bounds after marking. Forgetting that single-cell boards can match single-char words.
- **Pattern Recognition:** "Word in grid" → DFS + in-place marking; extension: Word Search II (uses Trie for multiple words).

---

## Problem 31: N-Queens

**Problem Explanation:**
Place n queens on an n×n chessboard so no two queens threaten each other (same row, column, or diagonal). Return all distinct board configurations. Use backtracking row by row: for each row, try every column that doesn't conflict with already placed queens. Track conflicts using sets for columns and two diagonals (row-col and row+col are constant along diagonals).

**Algorithm Steps:**
1. Initialize result list and empty board of '.' characters
2. Create three sets: `cols` (used columns), `diag1` (row-col differences), `diag2` (row+col sums)
3. `backtrack(row)`:
   a. If row == n: convert board to strings and add to result
   b. For each col in 0..n-1:
      - Skip if col in cols or (row-col) in diag1 or (row+col) in diag2
      - Place 'Q', add to sets, recurse with row+1
      - Remove 'Q' from sets (backtrack)
4. Start backtrack(0) and return result

**Key Insight:**
The diagonal indices are the key mathematical insight: on a diagonal, `row - col` is constant; on an anti-diagonal, `row + col` is constant. This O(1) conflict check replaces the naive O(n) scan for each placement.

### Problem Statement
Place n queens on an n×n chessboard such that no two queens attack each other. Return all distinct solutions.

### Examples
- Input: n=4 → Output: 2 solutions
- Input: n=1 → Output: 1 solution

### Approach
Backtracking: place queens row by row. Check column, diagonal (row-col), and anti-diagonal (row+col) conflicts using sets.

### Backtracking Tree (n=4)
```
Row 0 → Q at col 1: 
  Row 1 → Q at col 3:
    Row 2 → Q at col 0:
      Row 3 → Q at col 2: [.Q.., ...Q, Q..., ..Q.] ✔
  (other branches explored)
```

### Solution
```python
def solveNQueens(n):
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            board[row][col] = 'Q'
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1)
            board[row][col] = '.'
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    backtrack(0)
    return result

# Test cases
print(f"n=4: {len(solveNQueens(4))} solutions")  # 2
for sol in solveNQueens(4):
    for row in sol:
        print(row)
    print()
print(f"n=1: {len(solveNQueens(1))} solution")   # 1
print(f"n=8: {len(solveNQueens(8))} solutions")  # 92
```

### Complexity
- **Time:** O(n!) — prune many branches
- **Space:** O(n) recursion + sets
- **Edge Cases:** n=1 → one valid solution (Q). n=2,3 → zero solutions.
- **Common Mistakes:** Forgetting to convert board rows to strings. Using list for conflict check (O(n)) instead of sets (O(1)). Not resetting board cell after recursion.
- **Pattern Recognition:** "Place objects with conflict constraints" → row-by-row backtracking with set-based conflict tracking; same structure: Sudoku Solver, N-Queens II.

---

## Problem 32: Sudoku Solver

**Problem Explanation:**
Fill a partially filled 9×9 Sudoku grid so every row, column, and 3×3 box contains digits 1-9 exactly once. Empty cells are given as '.'. Use backtracking: find an empty cell, try digits 1-9, check validity, and recurse. If stuck, backtrack and try the next digit. The grid is modified in-place.

**Algorithm Steps:**
1. `is_valid(r, c, num)`: check row r, column c, and 3×3 box for num
2. `backtrack()`: scan all 81 cells; find first '.'; try digits '1'..'9':
   a. If valid, place digit and recurse
   b. If recursion returns True, puzzle solved → propagate True upward
   c. If not valid or recursion fails, reset to '.' and try next digit
3. If no '.' found, return True (base case: solved)

**Key Insight:**
The box index calculation `3*(r//3) + c//3` maps any cell to its 3×3 box. The termination check is implicit: when backtrack returns True, the puzzle is fully filled. Using a find-first-empty approach avoids passing positions around.

### Problem Statement
Fill a 9×9 Sudoku grid so each row, column, and 3×3 box contains digits 1-9 exactly once. Empty cells are '.'.

### Examples
- Standard sudoku puzzle → filled correctly

### Approach
Backtracking: try digits 1-9 in each empty cell. Validate row, column, and 3×3 box constraints.

### Solution
```python
def solveSudoku(board):
    def is_valid(r, c, num):
        for i in range(9):
            if board[r][i] == num or board[i][c] == num:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if board[i][j] == num:
                    return False
        return True
    def backtrack():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for num in '123456789':
                        if is_valid(r, c, num):
                            board[r][c] = num
                            if backtrack():
                                return True
                            board[r][c] = '.'
                    return False
        return True
    backtrack()

# Test case
board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"]
]
solveSudoku(board)
for row in board:
    print(row)
```

### Complexity
- **Time:** O(9^(empty cells)) worst case — pruning makes it much faster
- **Space:** O(1) in-place (recursion stack O(81))
- **Edge Cases:** Empty board (all '.'): fills completely. Already solved board: returns immediately (no '.' found → True).
- **Common Mistakes:** Not resetting cell on backtrack. Box index calculation off by one. Using `int(num)` comparisons instead of string comparisons.
- **Pattern Recognition:** "Constraint satisfaction puzzle" → backtracking with constraint validation; same structure: N-Queens, Crossword Solver.

---

## Problem 33: Generate Parentheses

**Problem Explanation:**
Generate all valid (well-formed) combinations of `n` pairs of parentheses. A string is well-formed if every opening '(' has a matching ')' that closes it, and at no point are there more closing than opening parentheses. Use backtracking: track counts of open and close parentheses used so far. Add '(' if open < n, add ')' if close < open.

**Algorithm Steps:**
1. Initialize result list
2. `backtrack(current, open_count, close_count)`:
   a. If len(current) == 2*n: add to result and return
   b. If open_count < n: add '(' and recurse (open_count + 1)
   c. If close_count < open_count: add ')' and recurse (close_count + 1)
3. Start backtrack('', 0, 0) and return result

**Key Insight:**
Two constraints produce all valid strings: (1) you can't use more than n opens, and (2) you can't close more than you've opened. The recursion naturally generates all 2n-length strings that satisfy these rules — no explicit validation needed after construction.

### Problem Statement
Given n pairs of parentheses, generate all combinations of well-formed parentheses.

### Examples
- Input: n=3 → Output: ["((()))","(()())","(())()","()(())","()()()"]
- Input: n=1 → Output: ["()"]

### Approach
Backtracking: track count of open and close. Add '(' if open < n, add ')' if close < open.

### Solution
```python
def generateParenthesis(n):
    result = []
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    backtrack('', 0, 0)
    return result

# Test cases
print(generateParenthesis(3))
# ["((()))","(()())","(())()","()(())","()()()"]
print(generateParenthesis(1))
# ["()"]
print(generateParenthesis(2))
# ["(())","()()"]
```

### Complexity
- **Time:** O(4^n / sqrt(n)) — Catalan number sequence
- **Space:** O(n) recursion depth
- **Edge Cases:** n=0 → return [""] (or [] depending on spec — Leetcode returns [""]). Large n (e.g., n=8) → 1430 combinations.
- **Common Mistakes:** Using `close_count <= open_count` instead of `<` (wastes branches). Allowing close before open (generates invalid strings like ")(").
- **Pattern Recognition:** "Generate well-formed strings with balance constraint" → backtrack with two counters; variations: Leetcode 22 (classic), Valid Parentheses (Leetcode 20) uses stack.

---

## Problem 34: Restore IP Addresses

**Problem Explanation:**
Given a string of digits, insert dots to form valid IP addresses. Each of the 4 segments must: (1) be in range [0,255], (2) not have leading zeros unless the segment is exactly "0". Use backtracking: try taking 1-3 digits as the next segment, validate, and recurse. At most 3⁴ = 81 possibilities, so brute force is fine.

**Algorithm Steps:**
1. Initialize result list
2. `backtrack(start, segments)`:
   a. If 4 segments collected: if start == len(s), join with '.' and add to result
   b. For length in 1..3:
      - If start+length > len(s): break
      - seg = s[start:start+length]
      - Skip if leading zero (len>1 and seg[0]=='0')
      - Skip if int(seg) > 255
      - Recurse with start+length and segments+[seg]
3. Start backtrack(0, []) and return result

**Key Insight:**
The branching factor is bounded (3 choices per segment) and the depth is fixed (exactly 4 segments). This makes the search space tiny (81 leaves max). The leading-zero check `len(seg) > 1 and seg[0] == '0'` is a critical pruning rule — "0" is valid but "01" is not.

### Problem Statement
Given a string `s` containing only digits, return all valid IP addresses that can be formed by inserting dots.

### Examples
- Input: "25525511135" → Output: ["255.255.11.135","255.255.111.35"]
- Input: "0000" → Output: ["0.0.0.0"]
- Input: "1111" → Output: ["1.1.1.1"]

### Approach
Backtracking: try 1-3 digits per segment (max value 255, no leading zeros). Build segments recursively.

### Solution
```python
def restoreIpAddresses(s):
    result = []
    def backtrack(start, segments):
        if len(segments) == 4:
            if start == len(s):
                result.append('.'.join(segments))
            return
        for length in range(1, 4):
            if start + length > len(s):
                break
            segment = s[start:start + length]
            if len(segment) > 1 and segment[0] == '0':
                break
            if int(segment) > 255:
                break
            backtrack(start + length, segments + [segment])
    backtrack(0, [])
    return result

# Test cases
print(restoreIpAddresses("25525511135"))
# ["255.255.11.135","255.255.111.35"]
print(restoreIpAddresses("0000"))
# ["0.0.0.0"]
print(restoreIpAddresses("1111"))
# ["1.1.1.1"]
print(restoreIpAddresses("010010"))
# ["0.10.0.10","0.100.1.0"]
```

### Complexity
- **Time:** O(1) — at most 3^4 = 81 possibilities
- **Space:** O(1) — bounded recursion
- **Edge Cases:** String too short (< 4 chars) or too long (> 12 chars) → no valid IPs. Leading zeros like "01" are invalid (but "0" alone is valid).
- **Common Mistakes:** Using `int()` and catching errors instead of checking leading zeros explicitly. Allowing segments > 255. Forgetting that exact 4 segments are required (not fewer).
- **Pattern Recognition:** "String partitioning with fixed parts and validation" → bounded backtracking with segment validation; same structure: Palindrome Partitioning.

---

## Problem 35: Letter Combinations of Phone Number

**Problem Explanation:**
Map a string of digits (2-9) to all possible letter combinations using the phone keypad mapping (2→abc, 3→def, ... 9→wxyz). Each digit maps to 3-4 letters. Build combinations by choosing one letter per digit. Use backtracking: for each digit position, iterate over its mapped letters and recurse.

**Algorithm Steps:**
1. Define mapping dict for digits '2'..'9'
2. If digits is empty, return []
3. Initialize result list
4. `backtrack(idx, current)`:
   a. If idx == len(digits): add current to result and return
   b. For each letter in mapping[digits[idx]]: recurse with idx+1, current+letter
5. Start backtrack(0, '') and return result

**Key Insight:**
This is a Cartesian product of sets — every combination of exactly one letter from each digit's mapping. The recursion depth equals the number of digits, and branching factor varies from 3 to 4. The problem is the simplest form of combinatorial enumeration: each level adds one choice from a fixed set.

### Problem Statement
Given a string of digits (2-9), return all possible letter combinations that the number could represent (like phone keypad).

### Examples
- Input: "23" → Output: ["ad","ae","af","bd","be","bf","cd","ce","cf"]
- Input: "79" → 16 combinations

### Approach
Backtracking: map each digit to letters. Build combination by choosing one letter per digit.

### Solution
```python
def letterCombinations(digits):
    if not digits:
        return []
    mapping = {'2':'abc','3':'def','4':'ghi','5':'jkl',
               '6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
    result = []
    def backtrack(idx, current):
        if idx == len(digits):
            result.append(current)
            return
        for letter in mapping[digits[idx]]:
            backtrack(idx + 1, current + letter)
    backtrack(0, '')
    return result

# Test cases
print(letterCombinations("23"))
# ["ad","ae","af","bd","be","bf","cd","ce","cf"]
print(letterCombinations("79"))
# ["pw","px","py","pz","qw","qx","qy","qz","rw","rx","ry","rz","sw","sx","sy","sz"]
print(letterCombinations(""))
# []
print(letterCombinations("2"))
# ["a","b","c"]
```

### Complexity
- **Time:** O(4^n * n) where n is number of digits
- **Space:** O(n) recursion depth
- **Edge Cases:** Empty input → []. Single digit → 3-4 strings.
- **Common Mistakes:** Forgetting the empty input case. Using wrong key mapping (standard mapping has 7→pqrs, 9→wxyz).
- **Pattern Recognition:** "Cartesian product of sets" → backtrack with fixed mapping per position; same structure: Generate Parentheses (different constraint).

---

## Problem 36: Word Search II

**Problem Explanation:**
Given a 2D board of letters and a list of words, find all words that can be formed by adjacent (4-directional) cells without reusing cells. Use a Trie for efficient prefix matching across all words simultaneously. DFS from each cell, following Trie branches. Prune words from Trie when found to avoid duplicates.

**Algorithm Steps:**
1. Build Trie from words: for each word, insert characters as nested dict nodes; mark end with '#': word
2. For each cell (r, c): call backtrack(r, c, trie_root)
3. `backtrack(r, c, node)`:
   a. If '#' in node: word found → add to result, remove from Trie (prune)
   b. If out of bounds or cell char not in node: return
   c. Mark cell as visited ('#'), recurse on 4 neighbors with node[ch]
   d. Restore cell char
   e. If node[ch] is empty (no children): delete it from parent (prune dead branches)

**Key Insight:**
Using a Trie with pruning (`node.pop('#')` and removing empty child nodes) is the key optimization. Without the Trie, searching each word independently is O(N * m * n * 4^L). With the Trie, overlapping prefixes are shared, and found words are removed to prevent redundant searches. The pruning of empty child nodes keeps the Trie shrinking as words are found.

### Problem Statement
Given a 2D board and a list of words, find all words that exist on the board. Each letter cell used at most once per word.

### Examples
- Board: [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
- Words: ["oath","pea","eat","rain"] → Output: ["oath","eat"]

### Approach
Backtracking + Trie. Build a Trie from words. For each cell, DFS following Trie branches. Prune dead branches by removing from Trie.

### Solution
```python
def findWords(board, words):
    trie = {}
    for word in words:
        node = trie
        for ch in word:
            node = node.setdefault(ch, {})
        node['#'] = word
    result = []
    rows, cols = len(board), len(board[0])
    def backtrack(r, c, node):
        if '#' in node:
            result.append(node.pop('#'))
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        ch = board[r][c]
        if ch not in node:
            return
        board[r][c] = '#'
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            backtrack(r+dr, c+dc, node[ch])
        board[r][c] = ch
        if not node[ch]:
            node.pop(ch)
    for r in range(rows):
        for c in range(cols):
            backtrack(r, c, trie)
    return result

# Test case
print(findWords([["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]],
                ["oath","pea","eat","rain"]))
# ["oath","eat"]
```

### Complexity
- **Time:** O(m * n * 4 * 3^(l-1)) per cell — with Trie pruning
- **Space:** O(N) for Trie where N = total chars in words
- **Edge Cases:** Empty board or empty words → []. Word longer than board cells → not found. Identical words in list → only returned once (pruned after first find).
- **Common Mistakes:** Not pruning found words (leads to duplicates). Restoring cell before children are done recursing. Forgetting the `if not node[ch]: node.pop(ch)` pruning (slows down dramatically).
- **Pattern Recognition:** "Multiple word search" → Trie + DFS; same structure: Word Search I (single word, no Trie needed).

---

## Problem 37: Expression Add Operators

**Problem Explanation:**
Given a string of digits and a target value, insert operators '+', '-', or '*' between digits (or concatenate digits to form larger numbers) to create expressions that evaluate to target. Key challenge: '*' has higher precedence than '+' and '-', so we must track the previous operand to undo its effect when multiplying.

**Algorithm Steps:**
1. Initialize result list
2. `backtrack(idx, prev_operand, current_value, path)`:
   a. If idx == len(num) and current_value == target: add path to result
   b. For i from idx to len(num)-1:
      - Skip if leading zero (i > idx and num[idx] == '0')
      - s = num[idx:i+1], val = int(s)
      - If idx == 0: first operand — no operator needed, recurse
      - Else:
        * '+' → prev = val, curr = curr + val, path = path + '+' + s
        * '-' → prev = -val, curr = curr - val, path = path + '-' + s
        * '*' → curr = curr - prev + prev * val, prev = prev * val, path = path + '*' + s
3. Start backtrack(0, 0, 0, '') and return result

**Key Insight:**
For multiplication, we can't just `curr * val` because of precedence. Instead, undo the previous operand's contribution (`curr - prev`) and add the multiplied version (`prev * val`). The `prev` tracks the last operand for the next multiplication. For '-' the prev is `-val` so that multiplying after subtraction works correctly.

### Problem Statement
Given a string `num` of digits and a target integer `target`, insert '+', '-', or '*' between digits to form expressions evaluating to target.

### Examples
- Input: num="123", target=6 → Output: ["1+2+3","1*2*3"]
- Input: num="232", target=8 → Output: ["2*3+2","2+3*2"]
- Input: num="105", target=5 → Output: ["1*0+5","10-5"]

### Approach
Backtracking: try each operator at each position. Track current value and previous operand for multiplication precedence.

### Solution
```python
def addOperators(num, target):
    result = []
    def backtrack(idx, prev, curr, path):
        if idx == len(num):
            if curr == target:
                result.append(path)
            return
        for i in range(idx, len(num)):
            if i > idx and num[idx] == '0':
                break
            s = num[idx:i+1]
            val = int(s)
            if idx == 0:
                backtrack(i + 1, val, val, s)
            else:
                backtrack(i + 1, val, curr + val, path + '+' + s)
                backtrack(i + 1, -val, curr - val, path + '-' + s)
                backtrack(i + 1, prev * val, curr - prev + prev * val, path + '*' + s)
    backtrack(0, 0, 0, '')
    return result

# Test cases
print(addOperators("123", 6))
# ["1+2+3","1*2*3"]
print(addOperators("232", 8))
# ["2*3+2","2+3*2"]
print(addOperators("105", 5))
# ["1*0+5","10-5"]
print(addOperators("00", 0))
# ["0+0","0-0","0*0"]
```

### Complexity
- **Time:** O(3^n) — three choices at each position
- **Space:** O(n) recursion depth
- **Edge Cases:** Leading zeros in multi-digit numbers ("05" invalid → break). Single digit: only check if int == target (no operators needed).
- **Common Mistakes:** Incorrect precedence handling for '*'. Sending `prev` instead of `-prev` for subtraction (breaks subsequent multiplication). Not breaking on leading zeros.
- **Pattern Recognition:** "Expression evaluation with operator precedence" → backtracking with prev operand tracking; Leetcode 282 (Hard premium).

---

## Problem 38: N-Queens II

**Problem Explanation:**
Same as N-Queens (Problem 31) but only count the number of solutions instead of storing all board configurations. Use the same backtracking with set-based conflict tracking, but increment a counter at leaf nodes instead of building board strings.

**Algorithm Steps:**
1. Initialize count = [0], cols, diag1, diag2 sets
2. `backtrack(row)`:
   a. If row == n: count[0] += 1, return
   b. For each col in 0..n-1:
      - Skip if col in cols or (row-col) in diag1 or (row+col) in diag2
      - Add to sets, recurse with row+1, remove from sets
3. Start backtrack(0) and return count[0]

**Key Insight:**
This is purely a counting problem — we don't need to store the board, only track conflicts with sets. The counter is wrapped in a list so the nested function can mutate it. The same pruning makes this O(n!) but n=16 is the practical limit.

### Problem Statement
Given an integer n, return the number of distinct solutions to the n-queens puzzle.

### Examples
- Input: n=4 → Output: 2
- Input: n=8 → Output: 92
- Input: n=1 → Output: 1

### Approach
Same as N-Queens but only count solutions instead of storing them. Use sets for column and diagonal tracking.

### Solution
```python
def totalNQueens(n):
    count = [0]
    cols = set()
    diag1 = set()
    diag2 = set()
    def backtrack(row):
        if row == n:
            count[0] += 1
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
    backtrack(0)
    return count[0]

# Test cases
print(totalNQueens(1))   # 1
print(totalNQueens(2))   # 0
print(totalNQueens(3))   # 0
print(totalNQueens(4))   # 2
print(totalNQueens(8))   # 92
```

### Complexity
- **Time:** O(n!) — with pruning
- **Space:** O(n) for sets + recursion
- **Edge Cases:** n=1 → 1 solution. n=2,3 → 0 solutions. n=12+ → solution count grows rapidly (14200 for n=12).
- **Common Mistakes:** Using an integer directly (can't reassign in nested scope) — must use list wrapper or `nonlocal`. Not resetting sets after recursion.
- **Pattern Recognition:** "Counting constrained placements" → row-by-row backtracking with O(1) conflict sets; optimization over N-Queens I (no board storage).

---

## Problem 39: Factor Combinations

**Problem Explanation:**
Given an integer n, find all unique ways to factor it into integers > 1. The factors in each combination must multiply to n. Order does not matter (e.g., [2,6] and [6,2] are the same). Use backtracking with a `start` parameter to ensure non-decreasing order, preventing duplicate combinations. Only try divisors from start to sqrt(remaining) for efficiency.

**Algorithm Steps:**
1. Initialize result list
2. `backtrack(start, remaining, current)`:
   a. If current is non-empty: add current[:] to result (this intermediate factorization)
   b. For i from start to sqrt(remaining):
      - If remaining % i == 0:
        - Append i, recurse with start=i, remaining//i, then pop
   c. If current is non-empty and remaining > 1: append remaining, add to result, pop
3. Start backtrack(2, n, []) and return result

**Key Insight:**
The three key techniques: (1) `start` parameter ensures non-decreasing order (prevents duplicates like [2,6] and [6,2]), (2) iterating only to sqrt(remaining) reduces the search space, (3) storing intermediate factorizations (not just leaf nodes) captures all combinations like [2,6] and [2,2,3] for n=12.

### Problem Statement
Given an integer n, find all possible ways to factor n into integers > 1. Return all unique factor combinations.

### Examples
- Input: 12 → Output: [[2,6],[2,2,3],[3,4]]
- Input: 32 → Output: [[2,16],[2,2,8],[2,2,2,4],[2,2,2,2,2],[2,4,4],[4,8]]
- Input: 37 (prime) → Output: []

### Approach
Backtracking: try divisors from 2 to sqrt(remainder). Include factor, recurse with quotient. Only try factors >= last factor to avoid duplicates.

### Solution
```python
def getFactors(n):
    result = []
    def backtrack(start, remaining, current):
        if current:
            result.append(current[:])
        for i in range(start, int(remaining**0.5) + 1):
            if remaining % i == 0:
                current.append(i)
                backtrack(i, remaining // i, current)
                current.pop()
        if current and remaining > 1:
            current.append(remaining)
            result.append(current[:])
            current.pop()
    backtrack(2, n, [])
    return result

# Test cases
print(getFactors(12))
# [[2,6],[2,2,3],[3,4]]
print(getFactors(32))
# [[2,16],[2,2,8],[2,2,2,4],[2,2,2,2,2],[2,4,4],[4,8]]
print(getFactors(37))
# []
print(getFactors(1))
# []
```

### Complexity
- **Time:** O(sqrt(n)^(log n)) — factor combinations
- **Space:** O(log n) recursion depth
- **Edge Cases:** Prime numbers → []. n=1 → []. Large prime (e.g., 97) → only sqrt bound loop, found no factors → [].
- **Common Mistakes:** Missing intermediate factorizations (e.g., [2,6] when n=12). Allowing duplicate factorizations by using i+1 instead of i as start. Including n itself as a factor (e.g., [12] is not valid for n=12).
- **Pattern Recognition:** "Number factorization" → backtrack with start parameter for non-decreasing order; combinatorial decomposition pattern.

---

## Problem 40: Unique Paths III

**Problem Explanation:**
On an m×n grid, you start at cell 1, must reach cell 2, visiting every empty cell (0) exactly once. Obstacles (-1) block the path. Count all such Hamiltonian paths. Use backtracking: count total walkable cells (0s + start + end), then DFS from start trying all 4 directions, tracking visited count.

**Algorithm Steps:**
1. Count total empty cells (grid[r][c] != -1) and locate start (1) and end (2)
2. Initialize result counter
3. `backtrack(r, c, visited_count)`:
   a. If (r,c) == end and visited_count == empty: increment result
   b. For each of 4 directions:
      - Compute nr, nc
      - If in bounds, not obstacle, not visited:
        - Mark (nr,nc) as visited, recurse with visited_count+1, unmark
4. Start backtrack(start_r, start_c, 1) — start counts as visited
5. Return result

**Key Insight:**
The "visit every empty cell exactly once" constraint turns this into a Hamiltonian path problem. Without this constraint it would be a simple count of all paths from start to end. The visited set ensures cells are not reused. The pruning is implicit: if we reach the end before visiting all cells, we don't count it.

### Problem Statement
Given an m×n grid with start (1), end (2), empty (0), and obstacles (-1), find all paths from start to end that visit every empty cell exactly once.

### Examples
- Input: [[1,0,0,0],[0,0,0,0],[0,0,2,-1]] → Output: 2
- Input: [[0,1],[2,0]] → Output: 0

### Approach
Backtracking: count total non-obstacle cells. DFS from start, mark visited, count steps. Reach end only when all cells visited.

### Solution
```python
def uniquePathsIII(grid):
    rows, cols = len(grid), len(grid[0])
    empty = 0
    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                start = (r, c)
            elif grid[r][c] == 2:
                end = (r, c)
            if grid[r][c] != -1:
                empty += 1
    result = [0]
    visited = [[False] * cols for _ in range(rows)]
    def backtrack(r, c, visited_count):
        if (r, c) == end and visited_count == empty:
            result[0] += 1
            return
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != -1 and not visited[nr][nc]:
                visited[nr][nc] = True
                backtrack(nr, nc, visited_count + 1)
                visited[nr][nc] = False
    visited[start[0]][start[1]] = True
    backtrack(start[0], start[1], 1)
    return result[0]

# Test cases
print(uniquePathsIII([[1,0,0,0],[0,0,0,0],[0,0,2,-1]]))  # 2
print(uniquePathsIII([[0,1],[2,0]]))                       # 0
print(uniquePathsIII([[1]]))                               # 1 (start=end)
```

### Complexity
- **Time:** O(3^(m*n)) — at most 3 directions per cell (can't go back to parent)
- **Space:** O(m*n) for visited set
- **Edge Cases:** Start == end (1x1 grid with 1) → count = 1 (already at end, visited all cells). No path reaching all empties → 0. Obstacle blocking all routes → 0.
- **Common Mistakes:** Not marking start as visited before DFS. Using `visited_count` without incrementing after visiting a cell. Counting paths that reach end before visiting all cells.
- **Pattern Recognition:** "Hamiltonian path counting in grid" → backtracking with visited tracking; Leetcode 980 (Hard). Related: Unique Paths I/II (DP without the "all cells" constraint).

---

# Summary Table

## Greedy Problems (1-20)
| # | Problem | Difficulty | Time | Space |
|---|---------|-----------|------|-------|
| 1 | Best Time to Buy/Sell Stock | Easy | O(n) | O(1) |
| 2 | Best Time to Buy/Sell Stock II | Easy | O(n) | O(1) |
| 3 | Maximum 69 Number | Easy | O(d) | O(d) |
| 4 | Min Sum of Four Digits | Easy | O(1) | O(1) |
| 5 | Max Product of Two Elements | Easy | O(n) | O(1) |
| 6 | Min Sum Three Numbers | Easy | O(n log n) | O(1) |
| 7 | Count Pairs Maximum XOR | Easy | O(n^2) | O(1) |
| 8 | Min Cost Candies | Easy | O(n log n) | O(1) |
| 9 | Maximum Swap | Medium | O(n) | O(n) |
| 10 | Railway Platforms | Medium | O(n log n) | O(1) |
| 11 | Job Sequencing | Medium | O(n^2) | O(d) |
| 12 | Fractional Knapsack | Medium | O(n log n) | O(1) |
| 13 | Minimum Coins | Medium | O(n*amt) | O(1) |
| 14 | Activity Selection | Medium | O(n log n) | O(1) |
| 15 | Min Absolute Sum Pair | Medium | O(n log n) | O(1) |
| 16 | Min Cost Process Requests | Medium | O(n^2) | O(n) |
| 17 | Optimal Account Balancing | Hard | O(n) | O(p) |
| 18 | Max Number Two Arrays | Hard | O(k*(n+m)) | O(k) |
| 19 | Min Cost Make Array Equal | Hard | O(n log n) | O(n) |
| 20 | Max Performance Team | Hard | O(n log n) | O(n) |

## Backtracking Problems (21-40)
| # | Problem | Difficulty | Time | Space |
|---|---------|-----------|------|-------|
| 21 | Subsets | Easy | O(n*2^n) | O(n) |
| 22 | Subsets II | Easy | O(n*2^n) | O(n) |
| 23 | Permutations | Easy | O(n*n!) | O(n) |
| 24 | Permutations II | Easy | O(n*n!) | O(n) |
| 25 | Combinations | Easy | O(k*C(n,k)) | O(k) |
| 26 | Combination Sum | Medium | O(N^(T/M)) | O(T/M) |
| 27 | Combination Sum II | Medium | O(2^n) | O(target/min) |
| 28 | Combination Sum III | Medium | O(C(9,k)) | O(k) |
| 29 | Palindrome Partitioning | Medium | O(n*2^n) | O(n) |
| 30 | Word Search | Medium | O(m*n*4^l) | O(l) |
| 31 | N-Queens | Medium | O(n!) | O(n) |
| 32 | Sudoku Solver | Medium | O(9^empty) | O(1) |
| 33 | Generate Parentheses | Medium | O(4^n/√n) | O(n) |
| 34 | Restore IP Addresses | Medium | O(1) | O(1) |
| 35 | Letter Combinations Phone | Medium | O(4^n * n) | O(n) |
| 36 | Word Search II | Hard | O(m*n*3^l) | O(N) |
| 37 | Expression Add Operators | Hard | O(3^n) | O(n) |
| 38 | N-Queens II | Hard | O(n!) | O(n) |
| 39 | Factor Combinations | Hard | O(√n^logn) | O(log n) |
| 40 | Unique Paths III | Hard | O(3^(m*n)) | O(m*n) |
