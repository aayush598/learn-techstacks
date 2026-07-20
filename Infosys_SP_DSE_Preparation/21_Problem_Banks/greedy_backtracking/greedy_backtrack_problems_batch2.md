# Greedy & Backtracking Problems - Batch 2
## Infosys SP DSE Preparation | 40 Problems (20 Greedy + 20 Backtracking)
## Total: 40 problems with complete Python solutions

---

# PART A: GREEDY ALGORITHMS (20 Problems)

---

## Problem 1: Best Time to Buy and Sell Stock

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
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        min_price = min(min_price, price)
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

---

## Problem 2: Best Time to Buy and Sell Stock II

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
    profit = 0
    for i in range(1, len(prices)):
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

---

## Problem 3: Maximum 69 Number

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
    s = list(str(num))
    for i in range(len(s)):
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

---

## Problem 4: Minimum Sum of Four Digits After Splitting

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

---

## Problem 5: Maximum Product of Two Elements in Array

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

---

## Problem 6: Minimum Sum of Three Numbers to Form a Number

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
    digits.sort()
    a, b, c = digits[0], digits[1], digits[2]
    place = 10
    for i in range(3, len(digits), 3):
        a += digits[i] * place
        if i + 1 < len(digits):
            b += digits[i + 1] * place
        if i + 2 < len(digits):
            c += digits[i + 2] * place
        place *= 10
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

---

## Problem 7: Count Pairs With Maximum XOR

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
    max_xor = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            max_xor = max(max_xor, arr[i] ^ arr[j])
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
- **Time:** O(n^2) — check all pairs twice
- **Space:** O(1)

---

## Problem 8: Minimum Cost of Buying Candies With Discount

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
    cost.sort(reverse=True)
    total = 0
    for i in range(0, len(cost), 3):
        total += cost[i]
        if i + 1 < len(cost):
            total += cost[i + 1]
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

---

## Problem 9: Maximum Swap

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
    last = {int(d): i for i, d in enumerate(digits)}
    for i, d in enumerate(digits):
        for k in range(9, int(d), -1):
            if k in last and last[k] > i:
                digits[i], digits[last[k]] = digits[last[k]], digits[i]
                return int(''.join(digits))
    return num

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

---

## Problem 10: Minimum Number of Platforms Required for Railway

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
    arrival.sort()
    departure.sort()
    platforms = max_platforms = 0
    i = j = 0
    while i < len(arrival):
        if arrival[i] <= departure[j]:
            platforms += 1
            i += 1
            max_platforms = max(max_platforms, platforms)
        else:
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

---

## Problem 11: Job Sequencing Problem

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
    jobs.sort(key=lambda x: x[2], reverse=True)
    max_deadline = max(j[1] for j in jobs)
    slots = [-1] * (max_deadline + 1)
    total_profit = count = 0
    for job in jobs:
        jid, deadline, profit = job
        for t in range(deadline, 0, -1):
            if slots[t] == -1:
                slots[t] = jid
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
- **Time:** O(n^2) — worst case checking slots
- **Space:** O(d) where d is max deadline

---

## Problem 12: Fractional Knapsack

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
    items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0
    for v, w in items:
        if capacity >= w:
            total_value += v
            capacity -= w
        else:
            total_value += v * (capacity / w)
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

---

## Problem 13: Minimum Number of Coins

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
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
    return count if amount == 0 else -1

# Test cases
print(minCoins([1, 5, 10, 25], 30))   # 2
print(minCoins([1, 2, 5], 11))         # 3
print(minCoins([2], 3))                 # -1
print(minCoins([1], 0))                 # 0
print(minCoins([1, 2, 5], 100))        # 20
```

### Complexity
- **Time:** O(n * amount) worst case
- **Space:** O(1)

---

## Problem 14: Activity Selection Problem

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
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    count = 1
    last_finish = activities[0][1]
    for i in range(1, len(activities)):
        if activities[i][0] >= last_finish:
            count += 1
            last_finish = activities[i][1]
    return count

# Test cases
print(activitySelection([1,3,0,5,8,5], [2,4,6,7,9,9]))  # 4
print(activitySelection([1,2,3], [2,3,4]))                 # 2
print(activitySelection([1,1,1], [2,2,2]))                 # 1
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(1)

---

## Problem 15: Minimum Absolute Sum Pair

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
    arr.sort()
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

---

## Problem 16: Minimum Cost to Process Requests

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
    requests.sort(reverse=True)
    servers = []
    for req in requests:
        placed = False
        for i in range(len(servers)):
            if servers[i] >= req:
                servers[i] -= req
                placed = True
                break
        if not placed:
            servers.append(capacity - req)
    return len(servers)

# Test cases
print(minServers([4, 2, 5, 3], 8))  # 3
print(minServers([2, 3, 4], 5))     # 2
print(minServers([1, 1, 1, 1], 2))  # 2
print(minServers([5], 5))            # 1
```

### Complexity
- **Time:** O(n^2) — best-fit search for each request
- **Space:** O(n) for server array

---

## Problem 17: Optimal Account Balancing

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
    for frm, to, amt in transactions:
        balance[frm] -= amt
        balance[to] += amt
    non_zero = [v for v in balance.values() if v != 0]
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

---

## Problem 18: Create Maximum Number from Two Arrays

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
        stack = []
        drop = len(nums) - t
        for num in nums:
            while stack and drop > 0 and stack[-1] < num:
                stack.pop()
                drop -= 1
            stack.append(num)
        return stack[:t]

    def merge(a, b):
        result = []
        i = j = 0
        while i < len(a) or j < len(b):
            if a[i:] > b[j:]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        return result

    best = []
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
- **Time:** O(k * (n + m)) for each split
- **Space:** O(k) for result

---

## Problem 19: Minimum Cost to Make Array Equal

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
    pairs = sorted(zip(nums, cost))
    total = sum(cost)
    cumulative = 0
    target = 0
    for num, c in pairs:
        cumulative += c
        if cumulative >= (total + 1) // 2:
            target = num
            break
    return sum(abs(num - target) * c for num, c in pairs)

# Test cases
print(minCost([1,3,5,2], [2,3,1,14]))     # 18
print(minCost([2,2,2,2,2], [4,2,8,1,3]))   # 0
print(minCost([1,2,3], [1,1,1]))            # 2
```

### Complexity
- **Time:** O(n log n) — sorting
- **Space:** O(n) for pairs

---

## Problem 20: Maximum Performance of a Team

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
    engineers = sorted(zip(efficiency, speed), reverse=True)
    speed_heap = []
    total_speed = 0
    result = 0
    for eff, spd in engineers:
        total_speed += spd
        heapq.heappush(speed_heap, spd)
        if len(speed_heap) > k:
            total_speed -= heapq.heappop(speed_heap)
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

---

# PART B: BACKTRACKING (20 Problems)

---

## Problem 21: Subsets

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
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
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
- **Time:** O(n * 2^n) — 2^n subsets, each up to n length
- **Space:** O(n) recursion depth

---

## Problem 22: Subsets II

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
    nums.sort()
    result = []
    def backtrack(start, current):
        result.append(current[:])
        for i in range(start, len(nums)):
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
- **Time:** O(n * 2^n) worst case
- **Space:** O(n) recursion depth

---

## Problem 23: Permutations

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
            result.append(nums[:])
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]
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
- **Time:** O(n * n!) — n! permutations
- **Space:** O(n) recursion depth

---

## Problem 24: Permutations II

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
- **Time:** O(n * n!) worst case
- **Space:** O(n) recursion depth + visited array

---

## Problem 25: Combinations

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
        if len(current) == k:
            result.append(current[:])
        for i in range(start, n + 1):
            current.append(i)
            backtrack(i + 1, current)
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
- **Time:** O(k * C(n,k)) — combinations
- **Space:** O(k) recursion depth

---

## Problem 26: Combination Sum

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
                break
            current.append(candidates[i])
            backtrack(i, current, remaining - candidates[i])
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
- **Time:** O(N^(T/M)) where N=candidates, T=target, M=min candidate
- **Space:** O(T/M) recursion depth

---

## Problem 27: Combination Sum II

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
            if i > start and candidates[i] == candidates[i-1]:
                continue
            if candidates[i] > remaining:
                break
            current.append(candidates[i])
            backtrack(i + 1, current, remaining - candidates[i])
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
- **Time:** O(2^n) — each element included or excluded
- **Space:** O(target/min) recursion depth

---

## Problem 28: Combination Sum III

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
                break
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

---

## Problem 29: Palindrome Partitioning

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
        return sub == sub[::-1]
    def backtrack(start, current):
        if start == len(s):
            result.append(current[:])
        for end in range(start + 1, len(s) + 1):
            if is_palindrome(s[start:end]):
                current.append(s[start:end])
                backtrack(end, current)
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
- **Time:** O(n * 2^n) — 2^n partitions, palindrome check O(n)
- **Space:** O(n) recursion depth

---

## Problem 30: Word Search

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
        board[r][c] = '#'
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            if backtrack(r+dr, c+dc, idx+1):
                return True
        board[r][c] = temp
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
- **Time:** O(m * n * 4^l) where l is word length
- **Space:** O(l) recursion depth

---

## Problem 31: N-Queens

### Problem Statement
Place n queens on an n×n chessboard such that no two queens attack each other. Return all distinct solutions.

### Examples
- Input: n=4 → Output: 2 solutions
- Input: n=1 → Output: 1 solution

### Approach
Backtracking: place queens row by row. Check column, diagonal (row-col), and anti-diagonal (row+col) conflicts using sets.

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

---

## Problem 32: Sudoku Solver

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

---

## Problem 33: Generate Parentheses

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
- **Time:** O(4^n / sqrt(n)) — Catalan number
- **Space:** O(n) recursion depth

---

## Problem 34: Restore IP Addresses

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

---

## Problem 35: Letter Combinations of Phone Number

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

---

## Problem 36: Word Search II

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

---

## Problem 37: Expression Add Operators

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

---

## Problem 38: N-Queens II

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

---

## Problem 39: Factor Combinations

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

---

## Problem 40: Unique Paths III

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
    def backtrack(r, c, visited):
        if (r, c) == end and visited == empty:
            result[0] += 1
            return
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != -1 and (nr, nc) not in visited:
                visited.add((nr, nc))
                backtrack(nr, nc, visited + 1)
                visited.remove((nr, nc))
    backtrack(start[0], start[1], {(start[0], start[1])})
    return result[0]

# Test cases
print(uniquePathsIII([[1,0,0,0],[0,0,0,0],[0,0,2,-1]]))  # 2
print(uniquePathsIII([[0,1],[2,0]]))                       # 0
print(uniquePathsIII([[1]]))                                # 1 (start=end)
```

### Complexity
- **Time:** O(3^(m*n)) — at most 3 directions per cell
- **Space:** O(m*n) for visited set

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
