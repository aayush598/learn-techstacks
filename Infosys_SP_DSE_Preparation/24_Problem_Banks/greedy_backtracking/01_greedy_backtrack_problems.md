# Greedy & Backtracking Problems — Infosys SP DSE Preparation

> **38 Problems** | Greedy (18) + Backtracking (20)
> Every problem: Statement → Approach → Code → Complexity → Tip

---

# ═══════════════════════════════════════════════════════════════
# PART A: GREEDY PROBLEMS (18)
# ═══════════════════════════════════════════════════════════════

---

## Problem 1 — Maximum Units on a Truck (Easy)

**Problem Explanation:**
You're loading a truck with boxes. Each box type tells you how many boxes of that type you have and how many units each box contains. Your truck has a limited box capacity. You want to maximize total units loaded. The greedy insight: since boxes are interchangeable, always take boxes that give the most units first.

**Algorithm Steps:**
1. Sort `boxTypes` by units per box in descending order (highest-value boxes first)
2. Initialize `total = 0` for tracking total units loaded
3. For each box type `[boxes, units]`:
   a. Take as many as possible: `take = min(boxes, truckCapacity)`
   b. Add `take * units` to total
   c. Reduce truck capacity by `take`
   d. If truck is full (`truckCapacity == 0`), stop early
4. Return total units

**Step-by-Step Walkthrough:**
```
boxTypes = [[1,3], [2,2], [3,1]], truckCapacity = 4
Sorted by units desc: [[1,3], [2,2], [3,1]]

Iteration 1: boxes=1, units=3
  take = min(1, 4) = 1
  total += 1*3 = 3
  truckCapacity = 4-1 = 3

Iteration 2: boxes=2, units=2
  take = min(2, 3) = 2
  total += 2*2 = 7
  truckCapacity = 3-2 = 1

Iteration 3: boxes=3, units=1
  take = min(3, 1) = 1
  total += 1*1 = 8
  truckCapacity = 1-1 = 0 → break

Result: 8 units
```

**Key Insight:**
Since all boxes of the same type are identical, the optimal strategy is to take the highest-value boxes first. Sorting by value descending ensures we fill the truck with the most valuable mix. This works because boxes are discrete but fungible — we don't need fractional amounts, just the best combination.

**Solution:**
```python
def maximumUnits(boxTypes, truckCapacity):
    # Sort box types by units per box descending (greedy: best first)
    boxTypes.sort(key=lambda x: x[1], reverse=True)
    total = 0
    for boxes, units in boxTypes:
        # Take as many boxes as capacity allows (but not more than available)
        take = min(boxes, truckCapacity)
        total += take * units
        truckCapacity -= take
        if truckCapacity == 0:  # Truck is full, stop early
            break
    return total
```

**Complexity Analysis:**
- **Time:** O(n log n) — dominated by sorting; the loop is O(n)
- **Space:** O(1) — sorting may use O(log n) stack space but no extra data structures

**Edge Cases:**
- `truckCapacity = 0`: Return 0 immediately (truck can't carry anything)
- All boxes have same units: Order doesn't matter, any selection works
- More capacity than boxes: Take all boxes
- Single box type: Take min(boxes, capacity) of that type

**Common Mistakes:**
- Sorting by boxes count instead of units per box (wrong optimization target)
- Not using `min(boxes, truckCapacity)` — either index out of bounds or over-counting
- Forgetting to decrement capacity and breaking on zero (infinite loop risk)

**Pattern Recognition:**
- "Maximum of something with capacity constraint" → Sort by value descending, fill greedily
- Similar to: Fractional Knapsack (but discrete here, not fractional)
- This is a "load balancing" variant where item value is uniform per type

---

## Problem 2 — Best Time to Buy and Sell Stock (Easy)

**Problem Explanation:**
You have stock prices day-by-day. You can buy once and sell once later. Find the maximum profit possible. If prices only go down, return 0. The trick: you track the cheapest price seen so far and check if selling today would give maximum profit.

**Algorithm Steps:**
1. Initialize `min_price` to infinity (no price seen yet)
2. Initialize `max_profit` to 0
3. Loop through each day's price:
   a. Update `min_price = min(min_price, current_price)`
   b. Calculate profit if sold today: `current_price - min_price`
   c. Update `max_profit = max(max_profit, profit)`
4. Return `max_profit`

**Key Insight:**
You don't need to track both buy and sell days separately. By tracking the minimum price seen so far, you implicitly know the best possible buy day. At each step, computing `price - min_price` gives the profit if you sold today — and taking the max over all days gives the answer. This transforms a nested-loop problem into a single pass.

**Solution:**
```python
def maxProfit(prices):
    # Start with a sentinel high value so first price becomes min
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        # Track the lowest price seen so far (best day to buy)
        min_price = min(min_price, p)
        # Compute profit if we sell today and update max
        max_profit = max(max_profit, p - min_price)
    return max_profit
```

**Complexity Analysis:**
- **Time:** O(n) — single pass through the array
- **Space:** O(1) — just two integer variables

**Edge Cases:**
- `prices = []`: Return 0 (no transactions possible)
- `prices = [5]`: Return 0 (single price, no sell possible)
- Strictly decreasing `[5,4,3,2,1]`: Return 0 (no profitable transaction)
- All same prices `[3,3,3]`: Return 0 (no profit)

**Common Mistakes:**
- Thinking you need to track both buy and sell days (not needed — just track min price)
- Setting `min_price` to `prices[0]` without checking for empty array (runtime error)
- Using `max` instead of `min` for tracking buy price (wrong direction)

**Pattern Recognition:**
- "Maximum profit from single transaction" → Track minimum so far
- Similar to: "Maximum subarray" (Kadane's algorithm variant)
- This is a "best time" pattern where you need optimal buy/sell timing

---

## Problem 2 — Best Time to Buy and Sell Stock (Easy)

**Statement:** Given `prices[i]` = price on day `i`. You may buy once and sell once. Return the **maximum profit**. Return 0 if no profit possible.

**Approach:** Track minimum price seen so far. At each day, compute `price - min_so_far` and update max profit.

```python
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit
```

- **Time:** O(n) | **Space:** O(1)
- **Tip:** This is the classic "track the minimum" greedy. You don't need to actually buy — just track the best possible profit.

---

## Problem 3 — Jump Game (Easy)

**Problem Explanation:**
You're at the start of an array. Each number tells you the maximum steps you can jump forward from that position. Can you reach the last index? Think of it as: maintain the furthest position you could possibly reach so far. If you ever land on a spot beyond your reachable range, you're stuck.

**Algorithm Steps:**
1. Initialize `farthest = 0` (furthest index reachable so far)
2. Loop through each index `i` with jump value `jump`:
   a. If `i > farthest`: current position is beyond reach → return False
   b. Update `farthest = max(farthest, i + jump)` — extend reachable range
   c. Optional: if `farthest >= len(nums)-1`, return True early
3. Return True (completed loop without getting stuck)

**Step-by-Step Walkthrough:**
```
nums = [2, 3, 1, 1, 4], last_index = 4

i=0: jump=2, farthest = max(0, 0+2) = 2
i=1: jump=3, farthest = max(2, 1+3) = 4 → farthest >= 4, can reach end!
Result: True

nums = [3, 2, 1, 0, 4], last_index = 4
i=0: jump=3, farthest = max(0, 0+3) = 3
i=1: jump=2, farthest = max(3, 1+2) = 3
i=2: jump=1, farthest = max(3, 2+1) = 3
i=3: jump=0, farthest = max(3, 3+0) = 3
i=4: i(4) > farthest(3) → Stuck! Return False
```

**Key Insight:**
You don't need to simulate actual jumps — just track the furthest index reachable. If at any point the current index exceeds the furthest reachable index, you're stuck. This works because all jumps move forward; if you can reach index `i`, you can also reach every index before it.

**Solution:**
```python
def canJump(nums):
    # farthest tracks the maximum index reachable so far
    farthest = 0
    for i, jump in enumerate(nums):
        # If current index is beyond what we can reach, we're stuck
        if i > farthest:
            return False
        # Extend the reachable window using current jump
        farthest = max(farthest, i + jump)
    return True  # Completed the array, we can reach the end
```

**Complexity Analysis:**
- **Time:** O(n) — single pass through the array
- **Space:** O(1) — only one variable

**Edge Cases:**
- `nums = [0]`: At last index already, return True
- `nums = [0, 1]`: Stuck at index 0 (cannot move), return False
- `nums = [1, 0, 0, ...]`: Gets stuck at index 2
- Large jumps: `nums = [10, 0, 0, 0, 0]` — first jump clears everything, return True

**Common Mistakes:**
- Returning True as soon as `farthest >= last_index` without considering that you might skip earlier unreachable spots — this is fine since `i > farthest` check would have caught it already
- Thinking you need to find the actual path (not needed — just check reachability)
- Using `if farthest >= len(nums):` instead of `if farthest >= len(nums)-1:`

**Pattern Recognition:**
- "Can you reach the end" → Track the maximum reachable index
- Variants: Jump Game II (minimum jumps), Jump Game III (with specific rules)
- This is a "reachability" problem that greedy solves because all jumps go forward

---

## Problem 4 — Lemonade Change (Easy)

**Problem Explanation:**
Each lemonade is $5. Customers pay with $5, $10, or $20 bills. You start with no change in the register. Can you give correct change to every customer? The greedy rule: always use a $10 bill (instead of two $5s) when giving change for $20 to preserve $5 bills.

**Algorithm Steps:**
1. Initialize `fives = 0, tens = 0`
2. For each bill `b`:
   a. **$5 bill**: Just increment `fives`
   b. **$10 bill**: Need $5 change. If `fives == 0`, fail. Else decrement `fives`, increment `tens`
   c. **$20 bill**: Need $15 change. Prefer `$10 + $5` over `$5 + $5 + $5`. If neither possible, fail
3. Return True (all customers served)

**Step-by-Step Walkthrough:**
```
bills = [5, 5, 5, 10, 20]

b=5:  fives=1, tens=0
b=5:  fives=2, tens=0
b=5:  fives=3, tens=0
b=10: need $5 change → fives=2, tens=1
b=20: need $15 change → tens>0 && fives>0 → give $10+$5
      fives=1, tens=0
Result: True

bills = [5, 5, 10, 10, 20]
b=5:  fives=1
b=5:  fives=2
b=10: fives=1, tens=1
b=10: fives=0, tens=2
b=20: need $15 → tens>0 but fives=0, fives>=3? No → Return False
```

**Key Insight:**
The greedy rule for $20 change is to give $10+$5 first (not three $5s). This preserves $5 bills, which are the most versatile — $5s are needed for both $10 and $20 change, while $10s only help with $20. This is a classic example of "use the largest denomination possible to preserve smaller ones."

**Solution:**
```python
def lemonadeChange(bills):
    fives = tens = 0  # Track available $5 and $10 bills
    for b in bills:
        if b == 5:
            fives += 1  # No change needed, just collect
        elif b == 10:
            if fives == 0:  # Need $5 change but have none
                return False
            fives -= 1
            tens += 1
        else:  # $20 bill
            if tens > 0 and fives > 0:
                # Prefer $10+$5 to preserve $5s for future customers
                tens -= 1
                fives -= 1
            elif fives >= 3:
                fives -= 3  # Fallback: three $5s
            else:
                return False  # Cannot make $15 change
    return True
```

**Complexity Analysis:**
- **Time:** O(n) — single pass through bills array
- **Space:** O(1) — only two counters

**Edge Cases:**
- First customer pays $10 or $20: Impossible (no change available), return False
- All customers pay $5: Always possible, return True
- Many $20 bills with few $5s: Likely fails unless $10s are available
- `bills = []`: Return True (vacuously true)

**Common Mistakes:**
- Using three $5s for $20 even when $10 is available (wastes $5s unnecessarily)
- Forgetting to increment `tens` when receiving $10
- Not checking `fives == 0` before giving change for $10

**Pattern Recognition:**
- "Can you make change" → Track bill counts, use largest denominations first
- Cashier/billing problems where greedy is optimal because denominations are canonical
- Similar to: Coin change in canonical coin systems

---

## Problem 5 — Assign Cookies (Easy)

**Problem Explanation:**
Children have greed factors (minimum cookie size they'll accept). Cookies have sizes. A child is content if they get a cookie at least as big as their greed. Each child gets at most one cookie. Maximize content children. Greedy insight: match the smallest adequate cookie to the least greedy child.

**Algorithm Steps:**
1. Sort both `g` (greed) and `s` (cookie sizes) in ascending order
2. Use two pointers: `child` for greed array, `cookie` for sizes array
3. While both pointers are valid:
   a. If `s[cookie] >= g[child]`: This cookie satisfies this child → move both pointers
   b. Else: Cookie too small → try next cookie (move cookie pointer)
4. Return `child` (number of content children)

**Step-by-Step Walkthrough:**
```
g = [1, 2, 3], s = [1, 1]
Sorted: g=[1,2,3], s=[1,1]

child=0, cookie=0: s[0]=1 >= g[0]=1 → content! child=1, cookie=1
child=1, cookie=1: s[1]=1 >= g[1]=2? No → cookie=2 (loop ends)
Result: 1 content child

g = [1, 2], s = [1, 2, 3]
Sorted: g=[1,2], s=[1,2,3]
child=0, cookie=0: s[0]=1 >= g[0]=1 → content! child=1, cookie=1
child=1, cookie=1: s[1]=2 >= g[1]=2 → content! child=2, cookie=2
Result: 2 content children
```

**Key Insight:**
By sorting both arrays and matching the smallest adequate cookie to the least greedy child, you avoid wasting large cookies on small-greed children. This is a classic "two-pointer on sorted arrays" pattern — the greedy choice of giving the smallest sufficient cookie at each step naturally maximizes total content children.

**Solution:**
```python
def findContentChildren(g, s):
    # Sort both arrays to use two-pointer matching
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        # If this cookie satisfies this child, count the child
        if s[cookie] >= g[child]:
            child += 1
        # Move to next cookie regardless (current cookie is used or too small)
        cookie += 1
    return child
```

**Complexity Analysis:**
- **Time:** O(n log n + m log m) — sorting both arrays. The matching pass is O(n + m)
- **Space:** O(1) — sorting may use O(log n) stack space

**Edge Cases:**
- No cookies (`s = []`): Return 0 (no child can be satisfied)
- No children (`g = []`): Return 0
- All cookies too small: Return 0
- More cookies than children: Can satisfy all children if every cookie >= corresponding greed
- Duplicate greed values: Handled naturally by sorting

**Common Mistakes:**
- Not sorting (matching won't be optimal without order)
- Trying to match largest cookie to greediest child first — same result but different approach
- Forgetting to increment cookie pointer when a child is NOT satisfied (infinite loop risk)
- Sorting in descending order but using ascending pointer logic (inconsistent)

**Pattern Recognition:**
- "Maximize satisfied demand with limited supply" → Sort both, greedy match smallest adequate
- Classic "matching" problem solvable greedily because we only care about count, not which child gets which cookie
- Two-pointer on sorted arrays is a common pattern

---

## Problem 6 — Maximum 69 Number (Easy)

**Problem Explanation:**
You get a number made of only digits 6 and 9. You can flip at most one digit (6→9 or 9→6) to make the number as large as possible. Since 9 > 6, you always flip the leftmost 6 to 9 to maximize the number's value.

**Algorithm Steps:**
1. Convert number to string, then to list of characters
2. Find the first occurrence of '6' (leftmost)
3. Change that '6' to '9'
4. Convert back to integer and return

**Step-by-Step Walkthrough:**
```
num = 9669
String: ['9','6','6','9']
i=0: '9' → skip
i=1: '6' → change to '9', break
Result: 9969

num = 9999
String: ['9','9','9','9']
No '6' found → return original 9999
```

**Key Insight:**
The leftmost digit has the highest positional value (thousands > hundreds > tens > ones). Changing the leftmost '6' to '9' gives the maximum possible increase. This is a special case of the Maximum Swap problem — here we only flip 6→9 (not 9→6), making it simpler.

**Solution:**
```python
def maximum69Number(num):
    # Convert to list of characters for mutation
    s = list(str(num))
    for i in range(len(s)):
        # Flip the leftmost 6 to 9 for maximum value
        if s[i] == '6':
            s[i] = '9'
            break
    return int(''.join(s))
```

**Complexity Analysis:**
- **Time:** O(d) where d = number of digits (max ~10 for integer range)
- **Space:** O(d) for the character list

**Edge Cases:**
- Single digit `6`: Flip to `9`
- Single digit `9`: Already maximum, return as-is
- All `9`s: No flip needed
- Leading digit is `6`: Always flip it (highest positional value)
- `num = 0`: Can't happen (problem says only 6 and 9)

**Common Mistakes:**
- Flipping the first digit regardless (might already be 9, should flip the first 6)
- Flipping the rightmost 6 (less gain than leftmost)
- Trying to do it with math operations instead of string (much more complex)
- Flipping a 9 to 6 (would decrease the number)

**Pattern Recognition:**
- "Maximum number by changing one digit" → Change leftmost smaller digit to larger one
- Positional value makes leftmost changes most significant
- This is a special case of the Maximum Swap problem (Problem 9 in Batch 2)

---

## Problem 7 — Jump Game II (Medium)

**Problem Explanation:**
You're at the start of an array where each number tells you the maximum jump length from that position. You need to find the **minimum number of jumps** to reach the last index. Unlike Jump Game I, you are guaranteed to be able to reach the end. The question asks: what's the fewest jumps needed?

**Algorithm Steps:**
1. Initialize `jumps = 0` (count of jumps taken), `end = 0` (boundary of current jump), `farthest = 0` (furthest reachable)
2. Loop through indices from 0 to n-2 (don't need to jump from last index):
   a. Update `farthest = max(farthest, i + nums[i])`
   b. If `i == end`: reached the boundary of the current jump level → increment `jumps`, set `end = farthest` (new boundary)
3. Return `jumps`

**Visual Walkthrough:**
```
nums = [2, 3, 1, 1, 4]

i=0: farthest = max(0, 0+2) = 2
     i == end(0) → jumps=1, end=2
     State: farthest=2, can reach [1, 2] in 1 jump

i=1: farthest = max(2, 1+3) = 4
     i(1) != end(2) → still within current jump zone

i=2: farthest = max(4, 2+1) = 4
     i == end(2) → jumps=2, end=4
     State: farthest=4, can reach end!

i=3: farthest = max(4, 3+1) = 4
     i(3) != end(4) → still in zone

Loop ends (i < len-1 = 4)
Result: 2 jumps
  Jump 1: [0→1] (reach up to index 2)
  Jump 2: [1→4] (reach up to index 4) Done!
```

**Key Insight:**
This is BFS in disguise. Each "jump" defines a range of indices you can reach. The end of one range becomes the start of the next. You track `farthest` to see how far the current jump can take you, and `end` marks when you must take a new jump. This "level-by-level" approach gives the minimum number of jumps without explicitly building a graph.

**Solution:**
```python
def jump(nums):
    # jumps: count of jumps taken
    # end: boundary of current jump range
    # farthest: furthest index reachable within current jump
    jumps = end = farthest = 0
    # Loop until second-to-last index (no jump needed from last)
    for i in range(len(nums) - 1):
        # Extend the reachable range for the current jump
        farthest = max(farthest, i + nums[i])
        # Reached the boundary of current jump → must take another
        if i == end:
            jumps += 1
            end = farthest  # New boundary = furthest reachable
    return jumps
```

- **Time:** O(n) — single pass through the array
- **Space:** O(1) — just integer variables
- **Edge Cases:** Single element `[0]` → return 0 (already at end). Two elements `[1, 0]` → return 1. All zeros except start `[2, 0, 0]` → return 2.
- **Common Mistakes:** Forgetting to stop at n-2 (jumping from last index is unnecessary). Confusing `end` (current boundary) with `farthest` (maximum reachable).
- **Pattern Recognition:** "Minimum jumps to reach end" → BFS-level greedy; similar to "minimum steps to reach target" where each step has a range.

---

## Problem 8 — Gas Station (Medium)

**Problem Explanation:**
You're driving around a circular route with `n` gas stations. Each station `i` has `gas[i]` fuel you can take, but it costs `cost[i]` fuel to drive to station `i+1`. You start with an empty tank. Find a starting station such that you can complete the full circuit without running out of fuel. Return -1 if impossible.

**Algorithm Steps:**
1. Initialize `total_tank = curr_tank = start = 0`
2. For each station `i`:
   a. Compute `diff = gas[i] - cost[i]` (surplus/deficit at this leg)
   b. Add to both `total_tank` and `curr_tank`
   c. If `curr_tank < 0`: this station (and all before) cannot be start → set `start = i + 1`, reset `curr_tank = 0`
3. If `total_tank >= 0`, return `start`; else return -1

**Visual Walkthrough:**
```
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
diff = [-2, -2, -2, 3, 3]

i=0: diff=-2, total=-2, curr=-2 < 0 → start=1, curr=0
i=1: diff=-2, total=-4, curr=-2 < 0 → start=2, curr=0
i=2: diff=-2, total=-6, curr=-2 < 0 → start=3, curr=0
i=3: diff=+3, total=-3, curr=+3
i=4: diff=+3, total=0,  curr=+6

total_tank(0) >= 0 → return start=3

Verification from station 3:
  3→4: tank=3 (gas=4-cost=1)
  4→0: tank=6 (gas=5-cost=2)
  0→1: tank=4 (gas=1-cost=3)
  1→2: tank=2 (gas=2-cost=4)
  2→3: tank=0 (gas=3-cost=5) → Complete circuit!
```

**Key Insight:**
If total gas >= total cost across all stations, a solution MUST exist. The proof: you can think of running out of fuel at a station as "proof that every station before this one fails as a starting point." By resetting `curr_tank` at each failure, you only check the remaining candidates. This turns O(n²) into O(n).

**Solution:**
```python
def canCompleteCircuit(gas, cost):
    # total_tank: overall surplus/deficit across all stations
    # curr_tank: running tank level from current start candidate
    # start: the current best candidate for starting station
    total_tank = curr_tank = start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]  # Net gain/loss at this station
        total_tank += diff
        curr_tank += diff
        # If we run out of fuel, no station up to i can be start
        if curr_tank < 0:
            start = i + 1         # Try next station as candidate
            curr_tank = 0         # Reset tank for new candidate
    return start if total_tank >= 0 else -1
```

- **Time:** O(n) | **Space:** O(1)
- **Edge Cases:** Only one station: check if `gas[0] >= cost[0]`. All stations with net deficit: return -1. All stations with surplus: return 0.
- **Common Mistakes:** Returning `start` even when `total_tank < 0` (no solution exists). Using `if curr_tank <= 0` instead of `< 0` (resetting at zero is wrong — zero means you barely made it, not failed).
- **Pattern Recognition:** "Circular route feasibility" → track cumulative deficit with reset. Similar to finding subarray with maximum sum (Kadane's algorithm variant).

---

## Problem 9 — Task Scheduler (Medium)

**Problem Explanation:**
You have a list of tasks (each task is a letter) and a cooldown period `n`. Between two executions of the **same** task, at least `n` other intervals must pass. During each interval, you can either run a task or be idle. Find the minimum number of intervals needed to finish all tasks.

**Algorithm Steps:**
1. Count frequency of each task using `Counter`
2. Find `max_freq` — the highest frequency among all tasks
3. Find `max_count` — how many tasks have that maximum frequency
4. Compute formula: `(max_freq - 1) * (n + 1) + max_count`
5. Return `max(len(tasks), formula_result)`

**Visual Walkthrough:**
```
tasks = ['A','A','A','B','B','B'], n = 2

freq: A=3, B=3
max_freq = 3
max_count = 2 (both A and B appear 3 times)

Formula: (3-1)*(2+1)+2 = 2*3+2 = 8
len(tasks) = 6
Result = max(6, 8) = 8

Layout (n=2 cooldown means 2 other tasks between same tasks):
  A _ _ A _ _ A     (A's positions)
  B _ _ B _ _ B     (B's positions)
  Merged: A B _ A B _ A B
  So 8 intervals total (A,B,idle,A,B,idle,A,B)
```

**Key Insight:**
The most frequent task is the bottleneck — it defines the minimum schedule length. The formula `(max_freq - 1) * (n + 1)` creates frames with `n` gaps between frames, then `+ max_count` fills the last partial frame. If other tasks happen to fill all the gaps, the answer is simply the total number of tasks (no idle needed).

**Solution:**
```python
from collections import Counter

def leastInterval(tasks, n):
    freq = Counter(tasks)                 # Count occurrences of each task
    max_freq = max(freq.values())         # How many times the most frequent task appears
    max_count = sum(1 for v in freq.values() if v == max_freq)  # How many tasks have max freq
    
    # Formula: frames for max-freq tasks with n gaps, plus the last row
    result = max(len(tasks), (max_freq - 1) * (n + 1) + max_count)
    return result
```

- **Time:** O(n) | **Space:** O(1) (at most 26 letters)
- **Edge Cases:** `n = 0`: Return `len(tasks)` (no cooldown needed). All tasks are the same `['A', 'A', 'A'], n=2`: Return `(3-1)*(2+1)+1 = 7`. Only one task type: the formula handles it naturally.
- **Common Mistakes:** Forgetting `max_count` (multiple tasks with same max frequency fill the last row differently). Using `(max_freq) * (n + 1)` instead of `(max_freq - 1) * (n + 1)`. Not taking `max()` with `len(tasks)`.
- **Pattern Recognition:** "Schedule with cooldown" → formula-based greedy; counting + max-frequency analysis is common in scheduling problems.

---

## Problem 10 — Queue Reconstruction by Height (Medium)

**Problem Explanation:**
You have an array of people described as `[height, k]` where `k` is the number of people in front of this person who are **taller or same height**. The queue is jumbled; you need to reconstruct the correct ordering. The key property: taller people are visible over shorter ones, so shorter people don't affect `k` counts of taller people.

**Algorithm Steps:**
1. Sort `people` by height descending (tallest first), and for ties, by `k` ascending
2. Initialize an empty result list
3. For each person `p` in sorted order:
   a. Insert `p` at index `p[1]` in the result list
4. Return the result list

**Visual Walkthrough:**
```
people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]
Sorted by (-height, k): [[7,0],[7,1],[6,1],[5,0],[5,2],[4,4]]

Insert [7,0] at index 0:  [[7,0]]
Insert [7,1] at index 1:  [[7,0],[7,1]]
Insert [6,1] at index 1:  [[7,0],[6,1],[7,1]]
Insert [5,0] at index 0:  [[5,0],[7,0],[6,1],[7,1]]
Insert [5,2] at index 2:  [[5,0],[7,0],[5,2],[6,1],[7,1]]
Insert [4,4] at index 4:  [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
                          ✓✓✓✓✓✓
```

**Key Insight:**
Taller people are "invisible" to shorter people — a short person's `k` only counts people taller than them. So if you place taller people first, the shorter person can just be inserted at position `k`, and they'll end up with exactly `k` taller people before them. This works because all previously placed people are already >= current height.

**Solution:**
```python
def reconstructQueue(people):
    # Sort by height descending (tallest first), then by k ascending
    people.sort(key=lambda x: (-x[0], x[1]))
    queue = []
    for p in people:
        # Insert at index k — taller people already placed won't be affected
        queue.insert(p[1], p)
    return queue
```

- **Time:** O(n²) — list insertions are O(n) each
- **Space:** O(n) for the result list
- **Edge Cases:** All same height `[[5,0],[5,1],[5,2]]`: Just sort by `k` ascending → works. Single person: Insert at index 0, return. People with `k` larger than current list length: Not possible in valid input.
- **Common Mistakes:** Sorting ascending instead of descending by height. Forgetting tie-breaker (ascending `k`). Using `queue.insert(-1, p)` or `queue.append(p)` instead of inserting at index `k`.
- **Pattern Recognition:** "Reconstruct from relative ordering" → insert tallest/smallest first; similar to building a tree from inorder/postorder.

---

## Problem 11 — Hand of Straights (Medium)

**Problem Explanation:**
You have an integer array of cards. Can you rearrange them into groups of size `groupSize` where each group forms a consecutive sequence (like 2,3,4 or 7,8,9)? Each card can be used once. The order doesn't matter — you can reorder freely.

**Algorithm Steps:**
1. If `len(hand) % groupSize != 0`: impossible, return False
2. Count frequency of each card value using `Counter`
3. Build a min-heap of unique card values
4. While heap is not empty:
   a. Peek at the smallest card value (`heap[0]`)
   b. For `i` from 0 to `groupSize - 1`:
      - Card needed = `first + i`
      - If count of needed card is 0: return False
      - Decrement count
      - If count becomes 0 and card is NOT the heap's minimum: return False (gap!)
      - If count becomes 0: pop from heap (this value is exhausted)
5. Return True

**Visual Walkthrough:**
```
hand = [1,2,3,6,2,3,4,7,8], groupSize = 3
len(hand)=9, 9%3=0 ✓

Count: {1:1, 2:2, 3:2, 4:1, 6:1, 7:1, 8:1}
Heap: [1,2,3,4,6,7,8]

Group 1: first=1
  need 1 → count[1]=0, pop 1
  need 2 → count[2]=1
  need 3 → count[3]=1
  Result: [1,2,3]

Group 2: first=2 (heap[0]=2)
  need 2 → count[2]=0, pop 2
  need 3 → count[3]=0, pop 3
  need 4 → count[4]=0, pop 4
  Result: [2,3,4]

Group 3: first=6 (heap[0]=6)
  need 6 → count[6]=0, pop 6
  need 7 → count[7]=0, pop 7
  need 8 → count[8]=0, pop 8
  Result: [6,7,8]

Heap empty → Return True
```

**Key Insight:**
Always start a group from the smallest remaining card. If you don't, the smallest card will eventually be left without consecutive companions. The min-heap gives O(1) access to the smallest card. The check `count[card] == 0 and card != heap[0]` detects gaps — if a card in the middle of a sequence runs out before the first card, there's a hole that can't be filled.

**Solution:**
```python
import heapq
from collections import Counter

def isNStraightHand(hand, groupSize):
    # If total cards aren't divisible by groupSize, impossible
    if len(hand) % groupSize != 0:
        return False
    
    # Count occurrences of each card value
    count = Counter(hand)
    # Min-heap of unique card values (sorted for smallest-first access)
    heap = list(count.keys())
    heapq.heapify(heap)
    
    while heap:
        first = heap[0]  # Smallest card value currently available
        # Try to form a consecutive group starting from 'first'
        for i in range(groupSize):
            card = first + i
            if count[card] == 0:       # Missing required card
                return False
            count[card] -= 1
            # If we just exhausted a middle card while first still exists → gap
            if count[card] == 0 and card != heap[0]:
                return False
            if count[card] == 0:       # This card value is fully used
                heapq.heappop(heap)    # Remove from heap
    return True
```

- **Time:** O(n log n) — each card processed once, heap operations O(log n)
- **Space:** O(n) — Counter and heap
- **Edge Cases:** Empty hand: return True (vacuously). Single card with groupSize=1: return True. Duplicates `[1,1,1], groupSize=3`: Need three different consecutive numbers, only 1's → False. Large groupSize > max spread: may have gaps.
- **Common Mistakes:** Forgetting the modulo check (impossible group sizes). Not checking for gaps when a middle card is exhausted (`count[card] == 0 and card != heap[0]`). Sorting the hand and iterating linearly (fails with duplicates/overlapping groups).
- **Pattern Recognition:** "Partition into consecutive sequences" → min-heap + frequency count; similar to "Divide Array in Sets of K Consecutive Numbers" (identical problem).

---

## Problem 12 — Minimum Number of Arrows to Burst Balloons (Medium)

**Problem Explanation:**
Balloons are represented as intervals `[start, end]` on a number line. An arrow shot at position `x` bursts every balloon whose interval `[start, end]` contains `x`. You can shoot arrows anywhere. Find the minimum number of arrows needed to burst all balloons.

**Algorithm Steps:**
1. Sort balloons by their end coordinate (ascending)
2. Initialize `arrows = 1` (at least one arrow needed) and `end = points[0][1]` (shoot at first balloon's end)
3. For each remaining balloon `[s, e]`:
   a. If `s > end`: balloon starts after last arrow's range → need new arrow → `arrows += 1`, update `end = e`
   b. Else: balloon overlaps with current arrow range → skip (arrow bursts it too)
4. Return `arrows`

**Visual Walkthrough:**
```
points = [[10,16],[2,8],[1,6],[7,12]]

Sorted by end: [[1,6],[2,8],[7,12],[10,16]]

arrows=1, end=6 (shoot at x=6)
  [2,8]: 2 <= 6? Yes (overlaps) → skip (burst by same arrow)
  [7,12]: 7 > 6? Yes (no overlap) → new arrow at x=12, arrows=2
  [10,16]: 10 > 12? No (overlaps) → skip

Answer: 2 arrows
  Arrow 1 at x=6 bursts [1,6] and [2,8]
  Arrow 2 at x=12 bursts [7,12] and [10,16]
```

**Key Insight:**
By shooting at the end of the first balloon, you burst all balloons that overlap with that point. Since the first balloon ends earliest, any balloon that overlaps with it MUST start before or at its end. Sorting by end ensures each arrow is placed as far right as possible while still bursting the leftmost remaining balloon — this maximizes arrow coverage.

**Solution:**
```python
def findMinArrowShots(points):
    # Sort intervals by end coordinate (greedy: shoot at earliest end)
    points.sort(key=lambda x: x[1])
    arrows = 1                      # At least one arrow needed
    end = points[0][1]              # Shoot at the first balloon's end
    for s, e in points[1:]:
        if s > end:                 # Balloon starts after current arrow's range
            arrows += 1
            end = e                 # New arrow at this balloon's end
        # else: balloon is burst by current arrow (overlapping)
    return arrows
```

- **Time:** O(n log n) — sorting dominates; traversal is O(n)
- **Space:** O(1) — in-place sorting
- **Edge Cases:** Single balloon: return 1. Non-overlapping balloons `[[1,2],[3,4],[5,6]]`: Each needs own arrow → return 3. All overlapping `[[1,6],[2,5],[3,4]]`: One arrow at x=4 bursts all → return 1. Negative coordinates: works the same way.
- **Common Mistakes:** Sorting by start instead of end (incorrect — earliest-ending balloons constrain the arrow the most). Using `<` instead of `<=` for overlap check — careful: `s > end` means no overlap. Not handling empty `points` array.
- **Pattern Recognition:** "Minimum number of arrows/points to cover all intervals" → sort by end, greedy overlap check; identical to "Maximum number of non-overlapping intervals" (Problem 13) and "Activity Selection" (Batch 2, Problem 14).

---

## Problem 13 — Non-overlapping Intervals (Medium)

**Problem Explanation:**
You're given a list of intervals `[start, end]`. You need to remove the minimum number of intervals so that the remaining intervals are non-overlapping (they can touch at endpoints). This is equivalent to: find the maximum number of intervals you can KEEP that don't overlap — then answer = total - kept.

**Algorithm Steps:**
1. Sort intervals by end coordinate (ascending)
2. Initialize `end = intervals[0][1]` (end of first interval), `kept = 1`
3. For each remaining interval `[s, e]`:
   a. If `s >= end`: interval doesn't overlap → keep it, update `end = e`, increment `kept`
   b. Else: interval overlaps → skip (would need removal)
4. Return `len(intervals) - kept`

**Visual Walkthrough:**
```
intervals = [[1,2],[2,3],[3,4],[1,3]]
Sorted by end: [[1,2],[2,3],[1,3],[3,4]]

kept=1, end=2
  [2,3]: 2 >= 2? Yes → kept=2, end=3
  [1,3]: 1 >= 3? No (overlaps) → skip
  [3,4]: 3 >= 3? Yes → kept=3, end=4

Kept = 3 ([1,2], [2,3], [3,4])
Remove = 4 - 3 = 1 (remove [1,3])
```

**Key Insight:**
This is the dual of Problem 12. Instead of minimizing arrows (which equals minimizing non-overlapping groups), here we maximize non-overlapping intervals. Both use the same sorting-by-end strategy. Picking intervals that end earliest leaves the most room for subsequent intervals — this is the "interval scheduling" greedy that guarantees optimality via exchange argument.

**Solution:**
```python
def eraseOverlapIntervals(intervals):
    # Sort by end time — earliest-finishing intervals leave most room
    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]   # End of the last kept interval
    kept = 1                # First interval is always kept
    for s, e in intervals[1:]:
        if s >= end:        # No overlap → safe to keep
            kept += 1
            end = e         # Update end to this interval
    # Total - kept = number we must remove
    return len(intervals) - kept
```

- **Time:** O(n log n) | **Space:** O(1)
- **Edge Cases:** Single interval: return 0. All overlapping `[[1,5],[2,3],[3,4]]`: Keep 1, remove 2. No overlapping `[[1,2],[2,3],[3,4]]`: Keep all, return 0. Empty list: return 0.
- **Common Mistakes:** Using `>` instead of `>=` for the non-overlap check (touching at endpoints counts as non-overlapping in this version). Sorting by start instead of end. Calculating `kept` incorrectly (off-by-one on the first interval).
- **Pattern Recognition:** "Remove minimum to make non-overlapping" → sort by end, count non-overlapping; "Maximum number of non-overlapping intervals" is the underlying greedy pattern.

---

## Problem 14 — Meeting Rooms II (Medium)

**Problem Explanation:**
You have meeting time intervals `[start, end]`. A meeting room can host only one meeting at a time. Find the minimum number of conference rooms required to accommodate all meetings. This is a classic "overlap counting" problem — you need a room for each overlapping meeting at any given time.

**Algorithm Steps:**
1. Sort intervals by start time
2. Initialize a min-heap to track end times of ongoing meetings
3. For each meeting `[s, e]`:
   a. If heap is not empty and the earliest-ending meeting ends by `s`: free that room (heapreplace)
   b. Else: no rooms free → add a new one (heappush)
4. Return heap size (number of rooms in use)

**Visual Walkthrough:**
```
intervals = [[0,30],[5,10],[15,20]]
Sorted by start: [[0,30],[5,10],[15,20]]

[0,30]: heap empty → push end=30  → heap=[30], rooms=1
[5,10]: heap[0]=30 > 5? Yes → room not free → push end=10 → heap=[10,30], rooms=2
[15,20]: heap[0]=10 ≤ 15? Yes → room free → heapreplace → heap=[20,30], rooms=2

Result: 2 rooms needed
```

**Key Insight:**
At any moment, the number of concurrent meetings equals the number of rooms needed. By processing meetings in start-time order and freeing rooms when meetings end, we simulate the real-time usage. The min-heap efficiently tracks which meeting ends next — if the next meeting starts after the earliest-ending meeting finishes, we reuse that room.

**Solution:**
```python
import heapq

def minMeetingRooms(intervals):
    # Sort by start time to process meetings in chronological order
    intervals.sort()
    # Min-heap stores end times of currently ongoing meetings
    heap = []
    for s, e in intervals:
        # If the earliest-ending meeting is done by now → free its room
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)  # Replace with new meeting's end
        else:
            heapq.heappush(heap, e)     # Need a new room
    # Heap size = number of concurrent meetings = rooms needed
    return len(heap)
```

- **Time:** O(n log n) — sorting + heap operations
- **Space:** O(n) — heap can hold all meetings if they all overlap
- **Edge Cases:** No meetings: return 0. Single meeting: return 1. All non-overlapping `[[1,2],[2,3],[3,4]]`: return 1 (one room reused). All overlapping `[[1,10],[2,9],[3,8]]`: return 3.
- **Common Mistakes:** Not sorting by start time (chronological order is essential). Using `heap[0] < s` instead of `heap[0] <= s` (can end exactly when next starts → room is free). Pop + push instead of heapreplace (less efficient but works).
- **Pattern Recognition:** "Minimum rooms/platforms" → two-pointer sweep-line or min-heap of end times; same as "Minimum Platforms" (Batch 2, Problem 10).

---

## Problem 15 — Candy (Hard)

**Problem Explanation:**
`n` children stand in a line, each with a rating. You must give each child at least 1 candy. Children with a **higher rating** than their neighbor must get **more candy** than that neighbor. Neighbors with equal ratings have no constraint (they can have any number, but must be at least 1). Find the minimum total candies needed.

**Algorithm Steps:**
1. Initialize `candies = [1] * n` (everyone gets at least 1)
2. **Left-to-Right pass:** For `i` from 1 to n-1: if `ratings[i] > ratings[i-1]`, set `candies[i] = candies[i-1] + 1` (ensure right child gets more than left if higher rated)
3. **Right-to-Left pass:** For `i` from n-2 down to 0: if `ratings[i] > ratings[i+1]`, set `candies[i] = max(candies[i], candies[i+1] + 1)` (ensure left child gets more than right if higher rated)
4. Return `sum(candies)`

**Visual Walkthrough:**
```
ratings = [1, 3, 2, 2, 1]

Pass 1 (left → right):
  candies = [1, 1, 1, 1, 1]
  i=1: r=3 > r[0]=1 → c[1] = c[0]+1 = 2
  i=2: r=2 < r[1]=3 → c[2] = 1 (no change)
  i=3: r=2 = r[2]=2 → c[3] = 1 (no change)
  i=4: r=1 < r[3]=2 → c[4] = 1 (no change)
  After pass 1: [1, 2, 1, 1, 1]

Pass 2 (right → left):
  i=3: r=2 > r[4]=1 → c[3] = max(1, 1+1) = 2
  i=2: r=2 = r[3]=2 → no change (c[2]=1)
  i=1: r=3 > r[2]=2 → c[1] = max(2, 1+1) = 2
  i=0: r=1 < r[1]=3 → no change (c[0]=1)
  After pass 2: [1, 2, 1, 2, 1]

Total = 1+2+1+2+1 = 7
```

**Key Insight:**
The constraint is bidirectional — each child compares to both left and right neighbors. A single pass can only capture one direction. Two passes (forward + backward) handle both directions independently. The `max` in the second pass ensures we don't reduce a candy count that was correctly set by the first pass. This elegantly handles "valleys" (ratings like 3, 1, 2 where the middle child is lower than both neighbors).

**Solution:**
```python
def candy(ratings):
    n = len(ratings)
    # Give each child at least 1 candy
    candies = [1] * n
    
    # Left-to-right: ensure right neighbor gets more if higher rated
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    
    # Right-to-left: ensure left neighbor gets more if higher rated
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    
    return sum(candies)
```

- **Time:** O(n) — two linear passes
- **Space:** O(n) — candy array
- **Edge Cases:** Single child: return 1. Strictly increasing `[1,2,3]`: candies = [1,2,3], sum=6. All equal `[2,2,2]`: all get 1, sum=n. Decreasing `[3,2,1]`: candies = [3,2,1] after two passes, sum=6.
- **Common Mistakes:** Only doing one pass (missing the reverse constraint). Using `candies[i] = candies[i+1] + 1` without `max()` (may override correct value from first pass). Forgetting that equal ratings have no constraint (not treating > vs >= correctly).
- **Pattern Recognition:** "Distribute with neighbor constraints" → two-pass greedy; similar to "trapping rain water" (two-pointer) and "product of array except self."

---

## Problem 16 — IPO (Hard)

**Problem Explanation:**
You start with capital `w`. There are `n` projects, each requiring `capital[i]` to fund and giving `profits[i]` in return. You can fund at most `k` projects (you can do them in any order). The profit from a project adds to your capital, letting you afford more expensive projects later. Maximize your total capital after at most `k` projects.

**Algorithm Steps:**
1. Pair each project as `(capital, profit)` and sort by capital (ascending)
2. Initialize a max-heap (use negative values for Python's min-heap) to store profits of affordable projects
3. Repeat up to `k` times:
   a. Push all projects whose capital requirement ≤ current capital into the max-heap
   b. If heap is empty: break (no affordable projects)
   c. Pop the most profitable project, add its profit to capital
4. Return total capital

**Visual Walkthrough:**
```
k=2, w=0, profits=[1,2,3], capital=[0,1,1]

Projects sorted by capital: [(0,1), (1,2), (1,3)]

Iteration 1 (w=0):
  Push projects with cap ≤ 0: (0,1) → heap=[-1]
  Pop -1 → profit=1, w = 0+1 = 1

Iteration 2 (w=1):
  Push projects with cap ≤ 1: (1,2), (1,3) → heap=[-3,-2]
  Pop -3 → profit=3, w = 1+3 = 4

k=2 iterations done → return 4
```

**Key Insight:**
The two-heap (or heap + sorted list) approach separates the problem into two phases: finding which projects are affordable (sorted by capital, incremental sweep) and picking the best among them (max-heap of profits). As capital grows, more projects become available — the heap dynamically manages the candidate pool. This "affordability + profitability" split is the core pattern.

**Solution:**
```python
import heapq

def findMaximizedCapital(k, w, profits, capital):
    # Sort projects by capital requirement (ascending)
    projects = sorted(zip(capital, profits))
    # Max-heap to store profits of affordable projects (use negative)
    max_heap = []
    idx = 0  # Pointer to next project in sorted list
    
    for _ in range(k):
        # Add all projects we can now afford to the heap
        while idx < len(projects) and projects[idx][0] <= w:
            heapq.heappush(max_heap, -projects[idx][1])  # Negative for max-heap
            idx += 1
        # If no projects are affordable, we're done
        if not max_heap:
            break
        # Take the most profitable affordable project
        w -= heapq.heappop(max_heap)  # Subtract negative = add profit
    return w
```

- **Time:** O(n log n) — sorting + at most n heap operations
- **Space:** O(n) — heap and sorted list
- **Edge Cases:** No project affordable initially: if `w < min(capital)`, return `w`. k larger than n: still fine, just exhaust all projects. All profits are zero: capital stays the same.
- **Common Mistakes:** Not sorting by capital (can't efficiently find affordable projects). Using `w += profit` instead of `w -= -profit` (or equivalently `w += heapq.heappop(max_heap)` where heap stores negatives). Forgetting to break when no affordable projects exist.
- **Pattern Recognition:** "Maximum capital with k selections" → dynamic selection via two-heap; similar to "Maximum Performance of a Team" (Batch 2, Problem 20).

---

## Problem 17 — Minimum Cost to Hire K Workers (Hard)

**Problem Explanation:**
You have `n` workers, each with a `quality` score and a minimum `wage` they'll accept. You want to hire exactly `k` workers. The rule: all hired workers are paid according to the same ratio (wage/quality). This means if you set a ratio `r`, each worker gets `r * quality[i]`. The constraint is that every hired worker must receive at least their minimum wage, so `r >= wage[i]/quality[i]` for each hired worker. Minimize total cost.

**Algorithm Steps:**
1. For each worker, compute ratio = wage/quality. Sort workers by ratio (ascending)
2. Initialize max-heap (negative values) for quality, `total_q = 0`, `result = infinity`
3. For each worker (ratio, quality) in sorted order:
   a. Push quality to heap (as negative), add to total_q
   b. If heap size > k: remove the worker with highest quality (pop negative heap)
   c. If heap size == k: compute cost = ratio * total_q, update result = min(result, cost)
4. Return result

**Visual Walkthrough:**
```
quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3

Workers sorted by ratio (wage/quality):
  (2.0, 10), (2.0, 1), (2.33, 3), (2.67, 1), (7.0, 1)

Iter 1: ratio=2.0, q=10 → heap=[-10], total_q=10, size=1<3
Iter 2: ratio=2.0, q=1  → heap=[-10,-1], total_q=11, size=2<3
Iter 3: ratio=2.33, q=3 → heap=[-10,-1,-3], total_q=14, size=3=k
        cost = 2.33*14 = 32.67 → result=32.67
Iter 4: ratio=2.67, q=1 → heap=[-10,-1,-3,-1], total_q=15
        size>k → pop -10 (qual=10), total_q=5, heap=[-3,-1,-1]
        size=3 → cost = 2.67*5 = 13.33 → result=13.33
Iter 5: ratio=7.0, q=1 → heap=[-3,-1,-1,-1], total_q=6
        size>k → pop -3 (qual=3), total_q=3, heap=[-1,-1,-1]
        size=3 → cost = 7.0*3 = 21.0 → result=13.33

Answer: 13.33
```

**Key Insight:**
If you fix the ratio `r`, the cost is `r * sum(qualities)`. The ratio must be at least as large as every hired worker's minimum ratio. So the maximum ratio among hired workers determines `r`. By sorting workers by ratio and iterating, each worker becomes the "ratio-setter" (the one with highest ratio in the group). For each ratio-setter, we want the `k-1` smallest qualities among workers with lower (or equal) ratios — a max-heap efficiently maintains these smallest qualities.

**Solution:**
```python
import heapq

def mincostToHireWorkers(quality, wage, k):
    # Sort by ratio (wage/quality) — ascending
    # The highest ratio in the group sets the pay rate for everyone
    workers = sorted([(w / q, q) for q, w in zip(quality, wage)])
    # Max-heap quality (negative) to keep K smallest qualities
    heap = []
    total_q = 0          # Sum of qualities currently in heap
    result = float('inf')
    
    for ratio, q in workers:
        heapq.heappush(heap, -q)  # Add current worker
        total_q += q
        # If we have more than K, remove the largest quality
        if len(heap) > k:
            total_q += heapq.heappop(heap)  # Pop negative = subtract quality
        # If we have exactly K, compute cost with current ratio
        if len(heap) == k:
            # ratio * total_q = cost for this group
            result = min(result, ratio * total_q)
    return result
```

- **Time:** O(n log n) — sorting + heap operations
- **Space:** O(n) — heap and sorted list
- **Edge Cases:** k = n: All workers hired, no quality dropping needed. k = 1: Pick the worker with minimum wage (not minimum quality).
- **Common Mistakes:** Forgetting that the ratio is determined by the highest-ratio worker in the group. Using a min-heap instead of max-heap for quality (we want to drop the LARGEST quality when exceeding k). Computing result before heap reaches size k.
- **Pattern Recognition:** "Hire K workers with minimum cost" → sort by ratio + max-heap for smallest K qualities; similar to "IPO" (Problem 16) and "Maximum Performance" (Batch 2, Problem 20) — all use heap to dynamically select best subset.

---

## Problem 18 — Course Schedule III (Hard)

**Problem Explanation:**
You have `n` courses, each with a `duration` (how long it takes) and a `lastDay` (deadline by which it must be completed). You can take courses in any order. You can only take one course at a time. You must finish a course before or on its lastDay. Return the maximum number of courses you can complete.

**Algorithm Steps:**
1. Sort courses by their lastDay (deadline) ascending
2. Initialize max-heap (negative values) for course durations, `total = 0`
3. For each course `[duration, lastDay]`:
   a. If `total + duration <= lastDay`: can fit → push to heap, add to total
   b. Else if heap exists and longest duration in heap > current duration:
      - Swap: remove longest course, add current course
      - Update total: `total = total - longest + current`
4. Return heap size (number of courses taken)

**Visual Walkthrough:**
```
courses = [[5,5],[2,6],[100,101],[10,10]]
Sorted by lastDay: [[5,5],[2,6],[10,10],[100,101]]

[5,5]:  total+dur=0+5=5 ≤ 5 → heap=[-5], total=5
[2,6]:  total+dur=5+2=7 > 6 → can't fit
        heap[0]=5 > 2? Yes → swap: pop -5 → total=5-5=0, push -2 → total=0+2=2
        heap=[-2], total=2
[10,10]: total+dur=2+10=12 > 10 → can't fit
         heap[0]=2 > 10? No → skip
[100,101]: total+dur=2+100=102 > 101 → can't fit
           heap[0]=2 > 100? No → skip

Answer: 1 course (the [2,6] one)
```

**Key Insight:**
This is an "exchange argument" greedy. When adding a new course would exceed its deadline, check if replacing it with a longer course already in your schedule helps. If the current course is shorter than the longest course you've already selected, swapping frees up time without reducing course count. This maintains the invariant: at any point, you have the maximum number of courses with minimum total duration among all possible schedules up to that deadline.

**Solution:**
```python
import heapq

def scheduleCourse(courses):
    # Sort by deadline (earliest deadline first)
    courses.sort(key=lambda x: x[1])
    # Max-heap (negative) to store durations of selected courses
    heap = []
    total = 0  # Total time spent on selected courses
    
    for dur, end in courses:
        # If we can add this course without missing its deadline
        if total + dur <= end:
            heapq.heappush(heap, -dur)
            total += dur
        # If not, but swapping with a longer course helps
        elif heap and -heap[0] > dur:
            # Remove the longest course from schedule
            total += heapq.heappop(heap)  # Pop negative = subtract
            # Add the current (shorter) course
            heapq.heappush(heap, -dur)
            total += dur
    
    # Number of courses we can take
    return len(heap)
```

- **Time:** O(n log n) — sorting + heap operations
- **Space:** O(n) — heap for selected courses
- **Edge Cases:** All courses have tight deadlines: only the shortest ones before each deadline can be taken. Courses with very long durations: may never fit or may be swapped out. No courses: return 0.
- **Common Mistakes:** Sorting by duration instead of deadline. Adding a course without checking the deadline. Using the swap check condition incorrectly — we swap only if the current course is SHORTER than the longest selected course. Thinking you need to maximize some profit (this is count maximization, not profit/cost).
- **Pattern Recognition:** "Maximum number of tasks before deadlines" → sort by deadline + max-heap of durations for optimal swaps; classic "exchange argument" problem seen in variants of "Maximum Profit in Job Scheduling."

---

# ═══════════════════════════════════════════════════════════════
# PART B: BACKTRACKING PROBLEMS (20)
# ═══════════════════════════════════════════════════════════════

---

## Problem 19 — Subsets (Easy)

**Problem Explanation:**
Given a list of unique integers, generate every possible subset (the power set). This includes the empty set and the full set. Order doesn't matter — `[1,2]` and `[2,1]` are considered the same subset. The total number of subsets for n elements is 2ⁿ.

**Algorithm Steps:**
1. Initialize result list
2. Define recursive function `backtrack(start, path)`:
   a. Add current path to result (including empty path for the empty set)
   b. For each index `i` from `start` to n-1:
      - Include nums[i] in path
      - Recurse with `i + 1` (next element)
      - Exclude nums[i] (pop) — backtrack
3. Call `backtrack(0, [])` and return result

**Visual Walkthrough:**
```
nums = [1, 2, 3]

Backtrack tree (each node = a subset added to result):
         []
       / |  \
    [1]  [2]  [3]
   /  \    |
[1,2] [1,3] [2,3]
  |
[1,2,3]

Execution trace:
backtrack(0, [])          → add [], i=0: [1]
  backtrack(1, [1])       → add [1], i=1: [1,2]
    backtrack(2, [1,2])   → add [1,2], i=2: [1,2,3]
      backtrack(3, [1,2,3]) → add [1,2,3], loop ends
    backtrack(2, [1,2])   → pop 3 → i=3: loop ends
  backtrack(1, [1])       → pop 2 → i=2: [1,3]
    backtrack(2, [1,3])   → add [1,3], loop ends
  backtrack(1, [1])       → pop 3 → loop ends
backtrack(0, [])          → pop 1 → i=1: [2]
  ... continues for [2], [2,3], [3]

Result: [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
8 = 2³ subsets
```

**Key Insight:**
The key pattern for subsets vs permutations: subsets use a `start` index that only moves forward — this prevents both reusing elements and generating duplicate permutations. Each element is either included or excluded exactly once. The path is added to result at **every** node, not just leaves. This is the foundation for all "combination-type" backtracking problems.

**Solution:**
```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        # Add current subset to result (at every node, not just leaves)
        result.append(path[:])
        # Try including each remaining element
        for i in range(start, len(nums)):
            path.append(nums[i])      # Choose: include this element
            backtrack(i + 1, path)    # Explore: recurse with next index
            path.pop()                # Unchoose: remove for backtracking
    
    backtrack(0, [])
    return result
```

- **Time:** O(n × 2ⁿ) — 2ⁿ subsets, each copied O(n) time
- **Space:** O(n) — recursion depth
- **Edge Cases:** Empty input `[]`: Return `[[]]` (just the empty set). Single element `[1]`: Return `[[], [1]]`. Large n: 2ⁿ grows exponentially; n > 20 may be computationally heavy.
- **Common Mistakes:** Adding path ONLY at leaf nodes (missing intermediate subsets like `[1]`). Not copying path with `path[:]` (storing a reference that mutates later). Using `start = 0` in recursive call without incrementing (causes infinite recursion with permutations).
- **Pattern Recognition:** "Generate all subsets/combinations" → backtracking with `start` index; fundamental template for: Subsets II, Combinations, Combination Sum I/II/III.

---

## Problem 20 — Subsets II (Easy)

**Problem Explanation:**
Same as Subsets (Problem 19), but the input may contain **duplicate** numbers. You must return only **unique** subsets — `[1,2]` should appear only once even if there are multiple ways to form it from the input.

**Algorithm Steps:**
1. Sort `nums` (duplicates will be adjacent)
2. Initialize result list
3. Define `backtrack(start, path)`:
   a. Add current path to result
   b. For `i` from `start` to n-1:
      - Skip if `i > start and nums[i] == nums[i-1]` (duplicate at same level)
      - Include nums[i], recurse with `i+1`, then pop/backtrack
4. Call `backtrack(0, [])` and return result

**Visual Walkthrough:**
```
nums = [1, 2, 2]
Sorted: [1, 2, 2]

Backtrack tree (X = skipped duplicate):
         []
       /    \
    [1]      [2]
   /   \       |
[1,2] [1,2,2] [2,2]
   |      |      |
(dup X) (end)  (end)

Execution:
backtrack(0, [])        → add []
  i=0: v=1 → [1]
    backtrack(1, [1])   → add [1]
    i=1: v=2 → [1,2]
      backtrack(2, [1,2]) → add [1,2]
      i=2: v=2 → [1,2,2]
        backtrack(3, [1,2,2]) → add [1,2,2], end
      pop → [1,2]
    i=2: v=2, i(2)>start(1) and nums[2]==nums[1]? Yes → SKIP
    pop → [1]
  i=1: v=2 → [2]
    backtrack(2, [2])   → add [2]
    i=2: v=2 → [2,2]
      backtrack(3, [2,2]) → add [2,2], end
    pop → [2]
  i=2: v=2, i(2)>start(0) and nums[2]==nums[1]? Yes → SKIP

Result: [[], [1], [1,2], [1,2,2], [2], [2,2]]
Notice: No duplicate [2] or [1,2] despite having two 2's!
```

**Key Insight:**
The `i > start` check is crucial — it skips duplicates only at the **same recursion level**. If `i == start`, that's the first time we're using this element at this level, which is fine. The skip only fires when we've already made a choice with the same value at the same level, ensuring we don't generate identical subsets from different positions of duplicate values.

**Solution:**
```python
def subsetsWithDup(nums):
    # Sort so duplicates are adjacent — enables duplicate skipping
    nums.sort()
    result = []
    
    def backtrack(start, path):
        # Add current subset (every node, not just leaves)
        result.append(path[:])
        for i in range(start, len(nums)):
            # Skip duplicate at the same recursion level
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])      # Choose
            backtrack(i + 1, path)    # Explore
            path.pop()                # Unchoose
    
    backtrack(0, [])
    return result
```

- **Time:** O(n × 2ⁿ) — worst case all distinct (same as Subsets)
- **Space:** O(n) — recursion depth
- **Edge Cases:** All duplicates `[1,1,1]`: Return `[[], [1], [1,1], [1,1,1]]`. Single element `[1]`: Return `[[], [1]]`. Already sorted vs unsorted: function sorts anyway.
- **Common Mistakes:** Forgetting to sort first (duplicate skip logic requires adjacent duplicates). Using `if nums[i] == nums[i-1]: continue` without `i > start` (this skips ALL duplicates even across different levels, losing valid subsets). Not understanding the difference from Permutations II (different skip condition).
- **Pattern Recognition:** "Unique subsets with duplicates" → sort + skip duplicates at same level with `i > start`; same pattern used in Combination Sum II.

---

## Problem 21 — Permutations (Easy)

**Problem Explanation:**
Given a list of **unique** integers, generate every possible ordering (permutation). Unlike subsets, `[1,2]` and `[2,1]` are different. For n elements, there are n! permutations. Each element must appear exactly once in each permutation.

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(path, used)`:
   a. If `len(path) == len(nums)`: add copy of path to result (base case)
   b. For each index `i` from 0 to n-1:
      - Skip if already used (`used[i]`)
      - Mark as used, append to path
      - Recurse
      - Unmark, pop (backtrack)
3. Call `backtrack([], [False] * len(nums))` and return result

**Visual Walkthrough:**
```
nums = [1, 2, 3]
Factorial: 3! = 6 permutations

Backtrack tree (depth-first):
                      []
        ┌─────────────┼─────────────┐
      [1]            [2]            [3]
     /    \         /    \         /    \
  [1,2]  [1,3]   [2,1]  [2,3]   [3,1]  [3,2]
    |      |       |      |       |      |
[1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]

Execution trace (partial):
backtrack([], [F,F,F])
  i=0: n=1 → used[0]=T, path=[1]
    backtrack([1], [T,F,F])
    i=0: skip (used)
    i=1: n=2 → used[1]=T, path=[1,2]
      backtrack([1,2], [T,T,F])
      i=0: skip, i=1: skip, i=2: n=3 → path=[1,2,3]
        backtrack([1,2,3], [T,T,T]) → len==3 → ADD [1,2,3]!
        pop → [1,2], used[2]=F
      pop → [1], used[1]=F
    i=2: n=3 → used[2]=T, path=[1,3]
      ... → ADD [1,3,2]!
    pop → [], used[0]=F
  i=1: n=2 → ... → ADD [2,1,3]!
  i=2: n=3 → ... → ADD [3,1,2]! etc.
```

**Key Insight:**
The fundamental difference from subsets: permutations use a `used[]` array (or swap-based approach) that allows picking **any** unused element at each step, rather than moving forward with a `start` index. This creates n! leaf nodes (complete permutations) instead of 2ⁿ nodes. Each element must be used exactly once — the `used[]` array enforces this.

**Solution:**
```python
def permute(nums):
    result = []
    
    def backtrack(path, used):
        # Base case: all elements used → permutation complete
        if len(path) == len(nums):
            result.append(path[:])
            return
        # Try every unused element as the next in permutation
        for i in range(len(nums)):
            if used[i]:
                continue          # Already placed this element
            used[i] = True        # Choose: mark as used
            path.append(nums[i])  # Add to current permutation
            backtrack(path, used) # Explore: fill remaining positions
            path.pop()            # Unchoose
            used[i] = False       # Unmark
    
    backtrack([], [False] * len(nums))
    return result
```

- **Time:** O(n × n!) — n! permutations, each copied O(n)
- **Space:** O(n) — recursion depth + used array
- **Edge Cases:** Single element `[1]`: Return `[[1]]`. Empty input `[]`: Return `[[]]` (one permutation of nothing). n=10: 10! ≈ 3.6M permutations (large but computable).
- **Common Mistakes:** Using a `start` index like subsets (produces combinations, not permutations). Not copying path in the base case (result stores reference to mutating list). Swapping approach (alternative) is more memory-efficient but harder to understand.
- **Pattern Recognition:** "Generate all arrangements" → `used[]` array backtracking; same pattern for: Permutations II, N-Queens (used columns), Generate Parentheses (used count).

---

## Problem 22 — Permutations II (Medium)

**Problem Explanation:**
Same as Permutations (Problem 21), but the input may contain **duplicate** integers. Return only unique permutations. For example, `[1, 1, 2]` should produce only 3 unique permutations (not 6), because swapping the two 1's doesn't create a new arrangement.

**Algorithm Steps:**
1. Sort `nums` (duplicates become adjacent)
2. Initialize result list
3. Define `backtrack(path, used)`:
   a. If `len(path) == len(nums)`: add copy to result
   b. For each index `i` from 0 to n-1:
      - Skip if `used[i]`
      - Skip if `i > 0 and nums[i] == nums[i-1] and not used[i-1]`
      - Mark used, append, recurse, unmark, pop
4. Call `backtrack([], [False] * len(nums))`

**Visual Walkthrough:**
```
nums = [1, 1, 2]
Sorted: [1, 1, 2]

Backtrack tree (X = skipped duplicate):
                  []
        ┌─────────┼─────────┐
      [1i=0]    [1i=1]X    [2]
      /    \       (dup)
  [1,1]  [1,2]      ✗
    |      |
[1,1,2] [1,2,1]

Valid permutations: [1,1,2], [1,2,1], [2,1,1]  (3 = 3!/2!)

Key: at the root, i=1 (second 1) is skipped because
nums[1]=nums[0] and used[0] is False (not selected by THIS path yet)
```

**Key Insight:**
The condition `nums[i] == nums[i-1] and not used[i-1]` is different from Subsets II. In permutations, we skip a duplicate when the **previous identical element is NOT used**. This ensures that among identical elements, we only consider them in order (first occurrence first), preventing duplicate permutations. If `used[i-1]` is True, that means the previous identical element is already in the current path, so the current one can still be used (as a different position in the same permutation).

**Solution:**
```python
def permuteUnique(nums):
    nums.sort()  # Sort so duplicates are adjacent
    result = []
    
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            # Skip duplicate: only allow the first among identical values
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    
    backtrack([], [False] * len(nums))
    return result
```

- **Time:** O(n × n!) worst case (all distinct = same as Permutations)
- **Space:** O(n) — recursion depth + used array
- **Edge Cases:** All same `[1,1,1]`: Return `[[1,1,1]]` (only 1 permutation). Two same, one different `[1,1,2]`: 3 permutations.
- **Common Mistakes:** Using the Subsets II skip condition (`i > start and nums[i] == nums[i-1]`) which doesn't work for permutations (no `start` parameter). Forgetting `used[i-1]` check — `nums[i] == nums[i-1]` alone skips too many cases. Not sorting (duplicates need to be adjacent).
- **Pattern Recognition:** "Unique permutations with duplicates" → sort + `not used[i-1]` skip; contrasting condition with Subsets II (`i > start` skip).

---

## Problem 23 — Letter Combinations of a Phone Number (Easy)

**Problem Explanation:**
Given a string of digits from 2-9 (like "23"), return every possible letter combination based on a phone keypad mapping (2=abc, 3=def, 4=ghi, etc.). Each digit maps to 3-4 letters. You pick one letter per digit to form combinations. The number of combinations equals the product of each digit's letter count.

**Algorithm Steps:**
1. Handle base case: if digits is empty, return []
2. Create mapping dict: digit → letters
3. Initialize result list
4. Define `backtrack(index, path)`:
   a. If `index == len(digits)`: join path to string, add to result
   b. For each letter in `mapping[digits[index]]`:
      - Append letter to path, recurse with `index + 1`, pop
5. Call `backtrack(0, [])` and return result

**Visual Walkthrough:**
```
digits = "23"

Phone keypad:
  2: abc    3: def

Backtrack tree:
                   ""
         ┌─────────┼─────────┐
        a          b          c
        |          |          |
     ┌──┼──┐    ┌──┼──┐    ┌──┼──┐
    ad  ae  af  bd  be  bf  cd  ce  cf

Result (9 combinations):
  "ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"

For each digit at index 0 (choices: a,b,c):
  For each digit at index 1 (choices: d,e,f):
    → 3 × 3 = 9 combinations
```

**Key Insight:**
This is a simple "product of choices" problem — at each digit, the number of branches equals the mapping size (3 or 4). The recursion depth equals the number of digits. No pruning needed (all branches are valid). This is the simplest form of backtracking: at each level, iterate over a fixed set of valid choices.

**Solution:**
```python
def letterCombinations(digits):
    if not digits:
        return []
    # Phone keypad mapping
    mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
               '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
    result = []
    
    def backtrack(index, path):
        # Base: built a complete combination
        if index == len(digits):
            result.append(''.join(path))
            return
        # Try each possible letter for the current digit
        for ch in mapping[digits[index]]:
            path.append(ch)
            backtrack(index + 1, path)  # Move to next digit
            path.pop()
    
    backtrack(0, [])
    return result
```

- **Time:** O(4ⁿ × n) — up to 4 choices per digit, string join is O(n)
- **Space:** O(n) — recursion depth
- **Edge Cases:** Empty digits: Return [] (not [""]). Digits containing 0 or 1: Not valid (problem says 2-9 only). Long digits (n=7): max 4⁷ = 16384 combinations.
- **Common Mistakes:** Not handling empty input (returning [""] instead of []). Forgetting to convert path list to string with `''.join(path)`. Using a `start` index approach (each digit is an independent choice, not a selection from a pool).
- **Pattern Recognition:** "Generate letter combinations from digits" → product-of-choices backtracking; similar to: Generate Parentheses, Combination Sum (simple branching at each level).

---

## Problem 24 — Combination Sum (Medium)

**Problem Explanation:**
Given an array of **unique** integers (candidates) and a `target` sum, find all unique combinations where the numbers sum to target. You may **reuse** each candidate **unlimited** times. For example, `[2,3,6,7]` with target 7 gives `[2,2,3]` and `[7]`. The same combination in different orders is considered the same (so `[2,2,3]` and `[2,3,2]` are duplicates).

**Algorithm Steps:**
1. Sort candidates (for pruning — early break when exceeding remaining)
2. Initialize result list
3. Define `backtrack(start, path, remaining)`:
   a. If `remaining == 0`: add path copy to result (base case)
   b. For `i` from `start` to n-1:
      - If `candidates[i] > remaining`: break (prune — sorted, rest will be larger too)
      - Append candidate, recurse with `backtrack(i, ...)` (NOT i+1 — allow reuse!)
      - Pop (backtrack)
4. Call `backtrack(0, [], target)` and return result

**Visual Walkthrough:**
```
candidates = [2, 3, 6, 7], target = 7

Backtrack tree (X = pruned because candidate > remaining):
                    []
       ┌────────────┼────────────┐
      [2]          [3]           [6]         [7]✓
    ┌──┼──┐       ┌──┼──┐       ┌──┐
 [2,2] [2,3]    [3,3]X [3,6]X  [6,6]X
   |     |        ✗       ✗       ✗
[2,2,2] [2,2,3]✓
   |
[2,2,2,?]X

Valid combinations: [2,2,3], [7]

Detailed trace:
backtrack(0, [], rem=7)
  i=0: 2 ≤ 7 → [2], rem=5
    i=0: 2 ≤ 5 → [2,2], rem=3
      i=0: 2 ≤ 3 → [2,2,2], rem=1
        i=0: 2 > 1 → break
      pop → [2,2]
      i=1: 3 > 1 → break
    pop → [2]
    i=1: 3 ≤ 5 → [2,3], rem=2
      i=1: 3 > 2 → break
    pop → [2]
    i=2: 6 > 5 → break
    i=3: 7 > 5 → break
  pop → []
  i=1: 3 ≤ 7 → [3], rem=4
    i=1: 3 ≤ 4 → [3,3], rem=1
      i=1: 3 > 1 → break
    pop → [3]
    i=2: 6 > 4 → break
  pop → []
  i=2: 6 ≤ 7 → [6], rem=1 → 6 > 1 → break
  pop → []
  i=3: 7 ≤ 7 → [7], rem=0 → ADD [7]!
```

**Key Insight:**
The critical design choice: `backtrack(i, ...)` (not `i+1`) allows reusing the same candidate multiple times. The `start` parameter ensures non-decreasing order, preventing duplicates like `[2,3]` and `[3,2]`. Sorting + `break` on exceeding remaining is a powerful pruning technique that dramatically reduces the search space.

**Solution:**
```python
def combinationSum(candidates, target):
    result = []
    # Sort for early break pruning
    candidates.sort()
    
    def backtrack(start, path, remaining):
        # Base: found a valid combination
        if remaining == 0:
            result.append(path[:])
            return
        # Try each candidate starting from 'start' (non-decreasing order)
        for i in range(start, len(candidates)):
            # Prune: sorted, so if this is too big, rest are too
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            # Pass i (not i+1) to allow reusing this candidate
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result
```

- **Time:** O(N^(T/M)) — branching factor N, depth T/M (T=target, M=min candidate)
- **Space:** O(T/M) — recursion stack depth
- **Edge Cases:** target=0: Return [[]] (empty combination sums to 0). Very small candidates `[1]` with large target: Deep recursion (target levels deep). No candidates: Return [].
- **Common Mistakes:** Using `i+1` instead of `i` in the recursive call (disables reuse, becoming subset sum). Not sorting before pruning (break doesn't work on unsorted array). Forgetting to copy path with `path[:]` in the base case.
- **Pattern Recognition:** "Combinations summing to target with reuse" → `backtrack(i, ...)` allows reuse; same pattern extended in Combination Sum II (no reuse, `i+1`) and III (fixed set 1-9).

---

## Problem 25 — Combination Sum II (Medium)

**Problem Explanation:**
Same as Combination Sum, but candidates **may contain duplicates** and each candidate can be used **at most once**. Return all unique combinations that sum to target. For example, `[10,1,2,7,6,1,5]` with target 8 gives `[1,1,6], [1,2,5], [1,7], [2,6]`.

**Algorithm Steps:**
1. Sort candidates
2. Define `backtrack(start, path, remaining)`:
   a. If `remaining == 0`: add path to result
   b. For `i` from `start` to n-1:
      - Skip if `i > start and candidates[i] == candidates[i-1]` (duplicate at same level)
      - If `candidates[i] > remaining`: break (pruning)
      - Append, recurse with `backtrack(i + 1, ...)` (no reuse!), pop
3. Call `backtrack(0, [], target)`

**Visual Walkthrough:**
```
candidates = [10,1,2,7,6,1,5], target = 8
Sorted: [1, 1, 2, 5, 6, 7, 10]

backtrack(0, [], rem=8)
  i=0: v=1 → [1], rem=7
    i=1: v=1 → [1,1], rem=6
      i=2: v=2 → [1,1,2], rem=4
        i=3: v=5 > 4 → break
      → ADD [1,1,6] at i=4! (1+1+6=8)
    i=2: v=2 → [1,2], rem=5
      i=3: v=5 → [1,2,5], rem=0 → ADD [1,2,5]!
    i=3: v=5 → [1,5], rem=2 → 5>2 break
    i=4: v=6 → [1,6], rem=1 → 6>1 break
  i=1: v=1, i=1>start=0 and nums[1]=nums[0]? Yes → SKIP (duplicate at root)
  i=2: v=2 → [2], rem=6
    i=3: v=5 → [2,5], rem=1 → break
    i=4: v=6 → [2,6], rem=0 → ADD [2,6]!
  i=3: v=5, i=3>start=0 and nums[3]=nums[2]? No (5≠2) → ... → ADD [1,7] at i=5!
  i=4: v=6 → [6], rem=2
    i=5: v=7 > 2 → break
  i=5: v=7 → [7], rem=1 → 7>1 break
  i=6: v=10 > 8 → break

Result: [[1,1,6], [1,2,5], [1,7], [2,6]]
```

**Key Insight:**
Two changes from Combination Sum: (1) `i+1` instead of `i` prevents reusing the same element, and (2) `i > start and nums[i] == nums[i-1]` skips duplicates at the same recursion level (same as Subsets II). The sorting handles the duplicate adjacency, and the skip prevents generating `[1,2,5]` twice (once for each 1 in the input).

**Solution:**
```python
def combinationSum2(candidates, target):
    candidates.sort()  # Sort for duplicate skipping and pruning
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            # Skip duplicates at the same recursion level
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            # Prune: remaining candidates are too large
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            # i+1: each candidate used at most once
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()
    
    backtrack(0, [], target)
    return result
```

- **Time:** O(2ⁿ) — each element either included or excluded
- **Space:** O(target) — recursion depth bounded by target
- **Edge Cases:** Large duplicates `[1,1,1,1,1,1,1]` target=2: Only result is `[1,1]` (appears once). Empty candidates: Return []. target smaller than smallest candidate: Return [].
- **Common Mistakes:** Using `i` instead of `i+1` (allows infinite reuse — breaks the "at most once" rule). Not sorting (duplicate skip requires adjacent duplicates, and pruning requires sorted order). Confusing with Combination Sum's reuse pattern.
- **Pattern Recognition:** "Combinations with duplicates, no reuse" → sort + `i+1` + same-level duplicate skip; hybrid of Subsets II and Combination Sum patterns.

---

## Problem 26 — Combination Sum III (Medium)

**Problem Explanation:**
Find all combinations of exactly `k` numbers (each 1-9, used at most once) that sum to exactly `n`. This is a restricted Combination Sum: the candidate pool is fixed as `[1,...,9]`, exactly `k` numbers must be chosen, and no reuse is allowed. If no combination exists, return [].

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(start, path, remaining)`:
   a. Base case: if `len(path) == k` and `remaining == 0`: add path to result
   b. Prune: if `len(path) > k` or `remaining < 0`: return (dead end)
   c. For `i` from `start` to 9:
      - Append i, recurse with `i+1`, pop
3. Call `backtrack(1, [], n)` and return result

**Visual Walkthrough:**
```
k=3, n=7

Numbers 1-9, choose exactly 3 that sum to 7

Backtrack trace:
backtrack(1, [], 7)
  i=1: [1], rem=6
    i=2: [1,2], rem=4
      i=3: [1,2,3], rem=1 → len=3, rem≠0
      i=4: [1,2,4], rem=0 → len=3, rem=0 → ADD [1,2,4]!
      i=5: [1,2,5], rem=-1 → prune (rem<0)
      ...
    i=3: [1,3], rem=3
      i=4: [1,3,4], rem=-1 (7-1-3-4=-1) → prune
    i=4: [1,4], rem=2 → can't reach sum with just 1 more number ≥5
    ...
  i=2: [2], rem=5
    i=3: [2,3], rem=2
      i=4: [2,3,4], rem=-2 → prune
    i=4: [2,4], rem=1 → can't reach sum (min remaining = 5)
    ...
  i=3: [3], rem=4
    i=4: [3,4], rem=0 → len=2 < k=3, but remaining=0 already
    ... (no 3-number combination starting with 3 sums to 7)

Result: [[1,2,4]]
```

**Key Insight:**
The search space is bounded: only numbers 1-9, and k ≤ 9. Two pruning strategies work together: (1) `len(path) > k` prevents exceeding the size limit, and (2) `remaining < 0` prevents overshooting the target. Since numbers are positive, if `remaining` reaches 0 before we have k numbers, we can't add any more (they'd all be positive and ruin the sum).

**Solution:**
```python
def combinationSum3(k, n):
    result = []
    
    def backtrack(start, path, remaining):
        # Base: correct size and exact sum
        if len(path) == k and remaining == 0:
            result.append(path[:])
            return
        # Prune: too many numbers or overshot target
        if len(path) > k or remaining < 0:
            return
        # Try numbers from start to 9 (each used at most once)
        for i in range(start, 10):
            path.append(i)
            backtrack(i + 1, path, remaining - i)
            path.pop()
    
    backtrack(1, [], n)  # Start from 1 (not 0)
    return result
```

- **Time:** O(C(9, k)) — combinatorial, but 9 choose k is at most 126
- **Space:** O(k) — recursion depth
- **Edge Cases:** Impossible sum (k=2, n=18): Max sum of 2 from 1-9 is 9+8=17, so return []. k=9, n=45: Only [1,2,3,4,5,6,7,8,9] works. k=9, n=44: Impossible. k=1, n=5: Return [[5]].
- **Common Mistakes:** Not pruning by path length (exploring beyond k numbers). Including 0 in the range (problem says 1-9). Forgetting that start=1 (not 0). Not checking that sum is achievable (trying combinations that can never work due to bounds).
- **Pattern Recognition:** "Fixed-size combinations from 1-9" → simple bounded backtracking; extension of the combination sum family with fixed pool.

---

## Problem 27 — Palindrome Partitioning (Medium)

**Problem Explanation:**
Given a string `s`, partition it into substrings (contiguous segments) such that every substring is a palindrome. Return all possible ways to partition the string. For example, "aab" can be partitioned as ["a","a","b"] or ["aa","b"] because "a", "aa", and "b" are all palindromes.

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(start, path)`:
   a. If `start == len(s)`: add path copy to result (base case — partitioned entire string)
   b. For each `end` from `start + 1` to `len(s)`:
      - Extract substring `s[start:end]`
      - If palindrome: append to path, recurse from `end`, pop
3. Call `backtrack(0, [])` and return result

**Visual Walkthrough:**
```
s = "aab"

Backtrack tree:
                    ""
        ┌───────────┼───────────┐
      "a"✓         "aa"✓       "aab"✗
        |             |
      "ab"✗       ["aa","b"]
      ["a",?]
        |
      ["a","a"]
        |
    ["a","a","b"]✓

Execution:
backtrack(0, [])
  end=1: sub="a" → palindrome ✓ → path=["a"]
    backtrack(1, ["a"])
      end=2: sub="a" → palindrome ✓ → path=["a","a"]
        backtrack(2, ["a","a"])
          end=3: sub="b" → palindrome ✓ → path=["a","a","b"]
            backtrack(3, ["a","a","b"]) → start==len → ADD ["a","a","b"]!
          pop → ["a","a"]
        pop → ["a"]
      end=3: sub="ab" → palindrome ✗ → skip
    pop → []
  end=2: sub="aa" → palindrome ✓ → path=["aa"]
    backtrack(2, ["aa"])
      end=3: sub="b" → palindrome ✓ → path=["aa","b"]
        backtrack(3, ["aa","b"]) → ADD ["aa","b"]!
    pop → []
  end=3: sub="aab" → palindrome ✗ → skip

Result: [["a","a","b"], ["aa","b"]]
```

**Key Insight:**
This problem combines string traversal with palindrome checking. At each position, we try all possible ending positions, checking if each substring is a palindrome. When we find one, we recurse on the remainder. This is essentially a "partition" problem — we make cuts between characters, and each cut creates a substring that must be a palindrome.

**Solution:**
```python
def partition(s):
    result = []
    
    def backtrack(start, path):
        # Base: partitioned entire string into palindromes
        if start == len(s):
            result.append(path[:])
            return
        # Try every possible ending for the current substring
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if sub == sub[::-1]:  # Check if substring is palindrome
                path.append(sub)          # Choose this palindrome segment
                backtrack(end, path)      # Recurse on the remainder
                path.pop()                # Backtrack
    
    backtrack(0, [])
    return result
```

- **Time:** O(n × 2ⁿ) — up to 2ⁿ possible partitions, each substring check O(n)
- **Space:** O(n) — recursion depth
- **Edge Cases:** Single character "a": Return [["a"]]. Empty string "": Return [[]]. All palindrome "aaa": 4 partitions. No palindrome possible: Can't happen — every single character is a palindrome.
- **Common Mistakes:** Off-by-one in `range(start+1, len(s)+1)` — the +1 for end is critical for slicing (Python slice end is exclusive). Not copying path in base case. Forgetting that single characters are always palindromes (base case is always reachable).
- **Pattern Recognition:** "Partition string with constraints" → backtracking on substring boundaries; similar to: Restore IP Addresses, Word Break (different DP approach).

---

## Problem 28 — Word Search (Medium)

**Problem Explanation:**
Given an m×n grid of characters and a word, determine if the word can be found in the grid by moving up, down, left, or right. You can use each cell **at most once**. The word must be formed by adjacent (not diagonal) cells in sequence. For example, "ABCCED" exists in the classic board but "ABCB" does not.

**Algorithm Steps:**
1. Store board dimensions
2. Define recursive `dfs(r, c, idx)`:
   a. If `idx == len(word)`: found entire word → return True
   b. If out of bounds or character doesn't match: return False
   c. Save current cell, mark as visited (`'#'`)
   d. Recursively explore 4 directions: up, down, left, right
   e. Restore cell value
   f. Return True if any direction found the word
3. For each cell in grid, if `dfs(r, c, 0)` returns True: return True
4. Return False if no path found

**Visual Walkthrough:**
```
board = [['A','B','C','E'],
         ['S','F','C','S'],
         ['A','D','E','E']]
word = "ABCCED"

DFS from (0,0)='A':
  idx=0: 'A' matches → mark as '#'
    → down (1,0)='S' ≠ 'B' ✗
    → up out of bounds ✗
    → right (0,1)='B' matches → mark '#' → idx=2
        → down (1,1)='F' ≠ 'C' ✗
        → right (0,2)='C' matches → mark '#' → idx=3
            → down (1,2)='C' matches → mark '#' → idx=4
                → down (2,2)='E' matches → mark '#' → idx=5
                    → down out ✗ up (1,2)='#' ✗ right (2,3)='E' matches! → idx=6
                        → idx==len(word)=6 → return True!
                restore (2,2)='E'
            restore (1,2)='C'
        restore (0,2)='C'
    restore (0,1)='B'
  restore (0,0)='A'

Result: True
```

**Key Insight:**
In-place marking (`'#'`) eliminates the need for a separate visited set, reducing memory overhead. The 4-direction DFS explores all possible paths. Backtracking (restoring the cell) ensures each cell can be reused in different search branches. Early exit via `return True` short-circuits the search as soon as any valid path is found.

**Solution:**
```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        # Found entire word
        if idx == len(word):
            return True
        # Out of bounds or character mismatch
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
        
        # Mark as visited (in-place)
        temp = board[r][c]
        board[r][c] = '#'
        
        # Explore all 4 directions
        found = (dfs(r + 1, c, idx + 1) or  # down
                 dfs(r - 1, c, idx + 1) or  # up
                 dfs(r, c + 1, idx + 1) or  # right
                 dfs(r, c - 1, idx + 1))    # left
        
        # Restore cell (backtrack)
        board[r][c] = temp
        return found

    # Start DFS from every cell
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

- **Time:** O(m × n × 4^L) — each starting cell explores up to 4 branches per character
- **Space:** O(L) — recursion stack depth (word length)
- **Edge Cases:** Empty word: return True (always exists). Word longer than total cells: return False quickly (but algorithm still explores). Single cell board with matching single char: return True.
- **Common Mistakes:** Not restoring cell after recursive call (visited cells stay marked for other search branches, causing false negatives). Checking bounds after marking (must check before accessing `board[r][c]`). Using `board[r][c]` instead of `temp` for restoration.
- **Pattern Recognition:** "Word existence in 2D grid" → DFS + backtracking with in-place marking; same traversal pattern in Word Search II (with Trie optimization).

---

## Problem 29 — N-Queens (Medium)

**Problem Explanation:**
Place `n` queens on an n×n chessboard so that no two queens attack each other. Queens attack along rows, columns, and both diagonals. Return all distinct board configurations. This is the classic constraint satisfaction problem. For n=4, there are 2 solutions.

**Algorithm Steps:**
1. Initialize result list, column set, positive diagonal set (`row + col`), negative diagonal set (`row - col`)
2. Initialize board as n×n grid of `'.'`
3. Define `backtrack(row)`:
   a. If `row == n`: all queens placed → add board snapshot to result
   b. For each `col` in 0..n-1:
      - Skip if column, positive diagonal, or negative diagonal is already used
      - Place queen: add to sets, set board cell to 'Q'
      - Recurse on next row
      - Remove queen: clear sets, set board cell to '.'
4. Call `backtrack(0)` and return result

**Visual Walkthrough:**
```
n=4, solving for valid queen positions:

Row 0: Try col=0
  Place Q at (0,0): cols={0}, pos_diag={0}, neg_diag={0}
  Row 1:
    col=0: in cols → skip
    col=1: pos_diag=2, neg_diag=0 (0 in neg_diag) → skip
    col=2: pos_diag=3, neg_diag=-1 → valid! Place Q
      cols={0,2}, pos_diag={0,3}, neg_diag={0,-1}
      Row 2:
        col=0,1,2: in cols → skip
        col=3: pos_diag=5, neg_diag=-1 (-1 in neg_diag) → skip
        → dead end! Backtrack
    col=3: pos_diag=4, neg_diag=-2 → valid! Place Q
      cols={0,3}, pos_diag={0,4}, neg_diag={0,-2}
      Row 2: Try col=1
        pos_diag=3 ✓, neg_diag=-1 ✓ → valid! Place Q at (2,1)
        cols={0,1,3}, pos_diag={0,1,4}, neg_diag={0,-1,-2}
        Row 3: Try col=2
          pos_diag=5 ✓, neg_diag=1 ✓ → valid! Place Q at (3,2)
          → FOUND SOLUTION!
            . Q . .
            . . . Q
            Q . . .
            . . Q .

(Similar process for Solution 2 starting with Q at (0,1))
```

**Key Insight:**
The diagonal encoding is the key insight: cells on the same `/` diagonal share the same `row + col` value, and cells on the same `\` diagonal share the same `row - col` value. Using sets for columns and diagonals gives O(1) conflict checks. Placing queens row by row ensures no two queens share a row.

**Solution:**
```python
def solveNQueens(n):
    result = []
    cols = set()          # Columns that have queens
    pos_diag = set()      # Positive diagonals (row + col) — '/' direction
    neg_diag = set()      # Negative diagonals (row - col) — '\' direction
    board = [['.'] * n for _ in range(n)]
    
    def backtrack(row):
        # All queens placed successfully
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            # Skip if attacked by another queen
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            # Place queen
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = 'Q'
            backtrack(row + 1)
            # Remove queen (backtrack)
            board[row][col] = '.'
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)
    
    backtrack(0)
    return result
```

- **Time:** O(n!) — first row has n choices, second at most n-1, etc.
- **Space:** O(n²) — board storage + O(n) for sets
- **Edge Cases:** n=1: Return `[["Q"]]`. n=2,3: Return [] (no solutions). n=8: 92 solutions.
- **Common Mistakes:** Forgetting to restore board state (both sets and board cells). Using `row + col` and `row - col` correctly (not swapping them). Not joining list to string in result. Off-by-one in `range(n)`.
- **Pattern Recognition:** "Constraint satisfaction on grid" → row-by-row backtracking with O(1) conflict sets; same pattern: Sudoku Solver (row, col, box constraints), N-Queens II (count only).

---

## Problem 30 — Sudoku Solver (Hard)

**Problem Explanation:**
You're given a partially filled 9×9 Sudoku board (empty cells are `'.'`). Fill all empty cells so that each row, column, and 3×3 box contains digits 1-9 exactly once. The puzzle is guaranteed to have exactly one solution. This is the classic "constraint satisfaction" backtracking problem.

**Algorithm Steps:**
1. Define `is_valid(row, col, num)`: check if `num` can be placed at (row, col):
   a. Check row: no other cell in `board[row]` has `num`
   b. Check column: no other cell in `board[:][col]` has `num`
   c. Check 3×3 box: compute box start indexes, check all 9 cells
2. Define `solve()`:
   a. Find the first empty cell (nested loop over r, c)
   b. If no empty cell: board is solved → return True
   c. For each digit `'1'` to `'9'`:
      - If valid: place digit, recursively call solve()
      - If recursion returns True: solution found → return True
      - If not: undo placement (backtrack), try next digit
   d. If no digit works: return False (trigger backtrack)
3. Call `solve()` (modifies board in-place)

**Visual Walkthrough:**
```
Initial board (partial):
[["5","3",".",".","7",".",".",".","."],
 ["6",".",".","1","9","5",".",".","."],
 [".","9","8",".",".",".",".","6","."],
 ["8",".",".",".","6",".",".",".","3"],
 ["4",".",".","8",".","3",".",".","1"],
 ["7",".",".",".","2",".",".",".","6"],
 [".","6",".",".",".",".","2","8","."],
 [".",".",".","4","1","9",".",".","5"],
 [".",".",".",".","8",".",".","7","9"]]

solve() starts scanning:
  (0,0)='5' → skip, (0,1)='3' → skip, (0,2)='.' → try digits 1-9
  Try '1': is_valid(0,2,'1')? 
    row0 has 5,3,7 → 1 not in row ✓
    col2 has 8 → 1 not in col ✓
    box (0-2,0-2) has 5,3,6,9,8 → 1 not in box ✓
    Place '1' at (0,2)
    Recursively solve...
    If failure, try '2', '3', ...
```

**Key Insight:**
The simple "find first empty cell, try 1-9" strategy, combined with immediate validation, is surprisingly effective for standard 9×9 Sudoku due to constraint propagation. Each placed digit eliminates options for other cells, quickly pruning invalid branches. The key optimizations are: (1) only check empty cells, and (2) the triple-constraint (row, column, box) validation.

**Solution:**
```python
def solveSudoku(board):
    def is_valid(row, col, num):
        """Check if num can be placed at board[row][col]."""
        for i in range(9):
            # Check row and column simultaneously
            if board[row][i] == num or board[i][col] == num:
                return False
            # Check 3x3 box using i to iterate its 9 cells
            br = 3 * (row // 3) + i // 3
            bc = 3 * (col // 3) + i % 3
            if board[br][bc] == num:
                return False
        return True

    def solve():
        # Find the first empty cell
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    # Try digits 1-9
                    for ch in '123456789':
                        if is_valid(r, c, ch):
                            board[r][c] = ch  # Place digit
                            if solve():       # Recurse
                                return True
                            board[r][c] = '.'  # Undo (backtrack)
                    return False  # No digit works → dead end
        return True  # No empty cells → solved!

    solve()  # Board is modified in-place
```

- **Time:** O(9^(empty cells)) worst case — pruning makes it far faster in practice
- **Space:** O(1) — recursion stack up to 81 levels (negligible)
- **Edge Cases:** Fully filled board already: solve() immediately returns True. Single empty cell: Try 9 digits, one will pass is_valid.
- **Common Mistakes:** Forgetting to undo placement (board cell stays filled on backtrack). Using `0` vs `'0'` — digits are strings. Not checking all three constraints (row, column, box). Off-by-one in box calculation (3*(r//3) + i//3 is correct for 0-indexed).
- **Pattern Recognition:** "Constraint satisfaction with grid" → find-first-empty + try-all-values + validate; same as N-Queens approach. Advanced version: use backtracking + constraint propagation (like MRV heuristic).

---

## Problem 31 — Restore IP Addresses (Medium)

**Problem Explanation:**
Given a string of digits, insert dots to form a valid IP address. A valid IPv4 address has exactly 4 segments separated by dots, each segment is a number 0-255, and no segment has leading zeros (unless the segment is exactly "0"). Return all possible valid IP addresses.

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(start, path)`:
   a. If `len(path) == 4`: if `start == len(s)`, join with dots and add to result; return
   b. For `length` in 1 to 3:
      - If `start + length > len(s)`: break (not enough remaining chars)
      - Extract segment `s[start:start+length]`
      - Skip if length > 1 and starts with '0' (leading zero invalid)
      - Skip if int > 255
      - Append segment, recurse with `start+length`, pop
3. Call `backtrack(0, [])` and return result

**Visual Walkthrough:**
```
s = "25525511135"

Backtrack tree (X = invalid segment):
              ""
   ┌──────────┼──────────┐
  "2"        "25"       "255"
   |          |           |
   X        X        ┌────┼────┐
                   "2"  "25" "255"
                    |     |    ...
                 ┌──┼──┐  X
               "5" "55" "551"
                       ┌──┼──┐
                     "1" "11" "113"
                         |
                       "1" "13" "135"
                         |    |
                        ✓     X

Execution:
backtrack(0, [])
  len=1: seg="2"
    len=2: seg="25"
      len=3: seg="255"
        backtrack(3, ["255"])
          len=1: seg="2" → ... → dead end
          len=2: seg="25" → ... → dead end
          len=3: seg="255"
            backtrack(6, ["255","255"])
              len=1: seg="1" → ... → dead end (not enough for 4 segs)
              len=2: seg="11"
                backtrack(8, ["255","255","11"])
                  len=1: seg="1" → ... → dead end
                  len=2: seg="13" → int=13 ≤ 255 ✓
                    backtrack(10, ["255","255","11","13"])
                      start(10)≠len(11) → seg len=1: "1"
                        backtrack(11, [...])
                          len(path)=4, start=11=len → ADD "255.255.11.135"!
                  len=3: seg="135" → int=135 ≤ 255 ✓
                    backtrack(11, ["255","255","11","135"])
                      len(path)=4, start=11=len → ADD "255.255.111.35"!

Result: ["255.255.11.135", "255.255.111.35"]
```

**Key Insight:**
The search space is bounded: at most 3 choices per segment (length 1, 2, or 3), and exactly 4 segments, so at most 3⁴ = 81 combinations. The constraints (leading zero, max 255) prune invalid branches immediately. This is a rare example of a backtracking problem with O(1) complexity.

**Solution:**
```python
def restoreIpAddresses(s):
    result = []
    
    def backtrack(start, path):
        # Base: 4 segments placed
        if len(path) == 4:
            if start == len(s):           # Used all characters
                result.append('.'.join(path))
            return
        
        # Try segment lengths 1, 2, 3
        for length in range(1, 4):
            if start + length > len(s):   # Not enough characters
                break
            seg = s[start:start + length]
            # Leading zeros are invalid (except "0" itself)
            if len(seg) > 1 and seg[0] == '0':
                break
            # Segment must be 0-255
            if int(seg) > 255:
                continue
            
            path.append(seg)
            backtrack(start + length, path)
            path.pop()
    
    backtrack(0, [])
    return result
```

- **Time:** O(1) — at most 3⁴ = 81 combinations
- **Space:** O(1) — recursion depth at most 4
- **Edge Cases:** s length < 4 or > 12: Return [] (not enough or too many digits for 4 segments). All zeros "0000": Return ["0.0.0.0"]. "010010": Returns ["0.10.0.10", "0.100.1.0"].
- **Common Mistakes:** Using `break` instead of `continue` for the >255 check — smaller lengths might still work (e.g., seg "25" in "255" → 25 ≤ 255, continue to length 2). Forgetting leading zero check (segments like "01" are invalid). Treating "0" as invalid leading zero (it's valid as a single-digit segment).
- **Pattern Recognition:** "Restore addresses from string" → bounded backtracking with segment validation; similar to Palindrome Partitioning (partition with constraints).

---

## Problem 32 — Generate Parentheses (Medium)

**Problem Explanation:**
Given `n` pairs of parentheses, generate all **well-formed** combinations. A well-formed string has matching open/close parentheses — at any point, the number of closing parentheses never exceeds the number of opening ones. Example for n=3: "((()))", "(()())", "(())()", "()(())", "()()()".

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(path, open_count, close_count)`:
   a. If `len(path) == 2*n`: add joined string to result
   b. If `open_count < n`: add `(`, recurse with `open_count+1`, pop
   c. If `close_count < open_count`: add `)`, recurse with `close_count+1`, pop
3. Call `backtrack([], 0, 0)` and return result

**Visual Walkthrough:**
```
n=3, target = 2*n = 6 characters

Backtrack tree (depth-first):
                    ""
          ┌─────────┴─────────┐
         "("               (close<open? No)
     ┌────┴────┐
   "(("       "()"
   ┌─┴─┐     ┌─┴─┐
 "(((" "(()" "()(" "(())"
   |     |     |
... ... ... ...

Detailed trace:
backtrack("", o=0, c=0)
  add '(' → "(", o=1
    add '(' → "((", o=2
      add '(' → "(((", o=3
        can't add '(' (o=n)
        add ')' → "((()", c=1
          add ')'→ "((())", c=2
            add ')'→ "((()))", c=3 → len=6 → ADD!
      pop → "(()", remove '(' attempt
      add ')' → "(()", o=2, c=1
        add '(' → "(()(", o=3
          add ')'→ "(()()", c=2
            add ')'→ "(()())", c=3 → ADD!
        add ')' → "(())", o=2, c=2
          add '(' → "(())(", o=3
            add ')'→ "(())()", c=3 → ADD!
    ...
  (continues to find "()(())" and "()()()")

5 total combinations = Catalan(3) = 5
```

**Key Insight:**
Two simple rules guarantee well-formed parentheses: (1) you can add `(` as long as you haven't used all n; (2) you can add `)` as long as there's an unmatched `(` (close_count < open_count). This elegantly avoids invalid strings without explicit validation. The number of valid strings is the Catalan number C(n) = (2n)!/((n+1)!×n!).

**Solution:**
```python
def generateParenthesis(n):
    result = []
    
    def backtrack(path, open_count, close_count):
        # Base: used all 2*n characters
        if len(path) == 2 * n:
            result.append(''.join(path))
            return
        # Add '(' if we can still open a new pair
        if open_count < n:
            path.append('(')
            backtrack(path, open_count + 1, close_count)
            path.pop()
        # Add ')' if we have an unmatched '(' to close
        if close_count < open_count:
            path.append(')')
            backtrack(path, open_count, close_count + 1)
            path.pop()
    
    backtrack([], 0, 0)
    return result
```

- **Time:** O(4ⁿ/√n) — Catalan number; for n=8, only 1430 combinations
- **Space:** O(n) — recursion depth
- **Edge Cases:** n=0: Return [""] (one empty string). n=1: Return ["()"]. Large n: Catalan numbers grow quickly (n=12 → 208012 combinations).
- **Common Mistakes:** Using `open_count <= close_count` instead of `<` for the `)` rule (would allow `)(` which is invalid). Not converting path list to string before adding. Adding `)` when `close_count == open_count` (no unmatched open paren).
- **Pattern Recognition:** "Generate balanced parentheses" → tracking open/close counts; same pattern used in: checking valid parentheses (stack), different bracket types problems. Catalan number structure appears in: Unique BSTs, valid parentheses, Dyck paths.

---

## Problem 33 — Expression Add Operators (Hard)

**Problem Explanation:**
Given a string of digits (like "123") and a target number, insert the operators `+`, `-`, or `*` between some digits (not necessarily between every pair) to form expressions that evaluate to the target. Return all valid expressions. For example, "123" with target 6 gives "1+2+3" and "1*2*3".

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(index, path, prev, curr)`:
   a. If `index == len(num)`: if `curr == target`, add path to result
   b. For `i` from `index` to `len(num)-1`:
      - Break if multi-digit segment starts with '0' (leading zero invalid)
      - Extract segment `num[index:i+1]`, convert to `val`
      - If `index == 0`: start with first number (no operator before it)
      - Else: try `+`, `-`, `*`:
        - `+`: curr + val, prev = val
        - `-`: curr - val, prev = -val
        - `*`: undo previous op, apply multiplication: `curr - prev + prev * val`, `prev = prev * val`
3. Call `backtrack(0, '', 0, 0)` and return result

**Visual Walkthrough:**
```
num = "123", target = 6

Backtrack tree (showing significant paths only):

index=0: segment "1" → start path="1", prev=1, curr=1
  index=1: segment "2"
    +: path="1+2", prev=2, curr=3
      index=2: segment "3"
        +: path="1+2+3", prev=3, curr=6 → target=6 ✓ → ADD!
        -: path="1+2-3", prev=-3, curr=0
        *: undo prev=2 → curr=3-2+2*3=7, prev=6
    -: path="1-2", prev=-2, curr=-1
      index=2: segment "3"
        +: path="1-2+3", prev=3, curr=2
        -: path="1-2-3", prev=-3, curr=-4
        *: undo prev=-2 → curr=-1-(-2)+(-2*3)=-5
    *: path="1*2", prev=2, curr=2
      index=2: segment "3"
        +: path="1*2+3", prev=3, curr=5
        -: path="1*2-3", prev=-3, curr=-1
        *: path="1*2*3", prev=6, curr=6 → target=6 ✓ → ADD!

  index=1: segment "23" (i=1, len=2)
    val=23 → "1+23"=24, "1-23"=-22, "1*23"=23

Result: ["1+2+3", "1*2*3"]
```

**Key Insight:**
Multiplication has higher precedence than addition/subtraction, so `1+2*3` should be 7, not 9. To handle this without building an AST: track `prev` (the last operand with its sign). For `+` and `-`, `prev` is just `val` or `-val`. For `*`, we undo the previous operation's effect on curr: `curr - prev + prev * val`. This effectively "replaces" the previous operand with the multiplied result.

**Solution:**
```python
def addOperators(num, target):
    result = []

    def backtrack(index, path, prev, curr):
        # Base: used all digits
        if index == len(num):
            if curr == target:
                result.append(path)
            return
        
        for i in range(index, len(num)):
            # Skip leading zeros (e.g., "05" is invalid)
            if i != index and num[index] == '0':
                break
            seg = num[index:i + 1]
            val = int(seg)
            
            if index == 0:
                # First number — no operator before it
                backtrack(i + 1, seg, val, val)
            else:
                # Addition: prev=val, curr += val
                backtrack(i + 1, path + '+' + seg, val, curr + val)
                # Subtraction: prev=-val, curr -= val
                backtrack(i + 1, path + '-' + seg, -val, curr - val)
                # Multiplication: undo prev, apply multiply
                backtrack(i + 1, path + '*' + seg, prev * val,
                          curr - prev + prev * val)

    backtrack(0, '', 0, 0)
    return result
```

- **Time:** O(4ⁿ) — at each split point, choose: end-segment or one of 3 operators
- **Space:** O(n) — recursion depth
- **Edge Cases:** Leading zeros: "105" with target 5 allows "1*0+5" and "10-5" but not "1*05". Single digit "5" with target 5: Return ["5"]. Very large numbers (inputs up to 10 digits) can cause integer overflow in some languages.
- **Common Mistakes:** Incorrect multiplication handling — `curr += val` doesn't account for precedence. Using `int(seg)` on very long segments (Python handles big ints but other languages may not). Forgetting the leading zero check (`num[index] == '0'` for segments longer than 1).
- **Pattern Recognition:** "Add operators to form target" → backtracking with `prev` tracking for precedence; advanced version of: Target Sum, Expression Evaluation.

---

## Problem 34 — Word Search II (Hard)

**Problem Explanation:**
Given an m×n board of characters and a list of words, find all words from the list that exist on the board. Each cell can be used at most once per word, and you can move up/down/left/right. This is Word Search (Problem 28) with multiple words. Using a simple DFS per word would be too slow — we need a Trie to check all words simultaneously.

**Algorithm Steps:**
1. Build a Trie from the word list (each node has children dict and optional `word` marker)
2. Initialize result list
3. Define `dfs(r, c, node)`:
   a. Get character `ch` at board[r][c]
   b. If `ch` not in node.children: return (no word has this prefix)
   c. Move to child node
   d. If node has a word: add to result, set node.word = None (deduplicate)
   e. Mark cell as visited (`'#'`)
   f. Explore 4 directions (if within bounds and not visited)
   g. Restore cell
4. For each cell, call `dfs(r, c, root)`
5. Return result

**Visual Walkthrough:**
```
board = [['o','a','a','n'],
         ['e','t','a','e'],
         ['i','h','k','r'],
         ['i','f','l','v']]
words = ["oath","pea","eat","rain"]

Trie structure:
        root
       / |  \
      o  p   r
      |  |   |
      a  e   a
      |  |   |
      t  a   i
      |      |
      h(oath) t(pea?) → no, e→a→t? no (but "eat" is at e→a→t)
      
DFS from (0,0)='o':
  node=root's child 'o'
    'o'→'a'→'t'→'h': found "oath"! result=["oath"]
    Continue DFS...

DFS from (1,0)='e':
  node=root's child 'e' → 'a' (1,1) → 't' (1,2) → found "eat"!
  result=["oath", "eat"]

"pea": starts at (1,0)='e' ≠ 'p', (1,1)='t' ≠ 'p'... never matches
"rain": (2,3)='r'... r→a→i→n? (3,3)='v' ≠ 'n' → fails

Result: ["oath", "eat"]
```

**Key Insight:**
Without a Trie, you'd run DFS once per word (O(words × board × 4^L)). With a Trie, a single DFS explores all word prefixes simultaneously — if the current DFS path doesn't match any prefix in the Trie, you prune immediately. This reduces complexity to O(board × 3^L) regardless of the number of words. Setting `node.word = None` after finding a word prevents adding it twice.

**Solution:**
```python
class TrieNode:
    def __init__(self):
        self.children = {}  # Character → TrieNode mapping
        self.word = None    # Set to the word when this node is a word end

def buildTrie(words):
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = w  # Store word at the terminal node
    return root

def findWords(board, words):
    root = buildTrie(words)
    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return                   # No word with this prefix
        node = node.children[ch]     # Move to child node
        if node.word:                # Found a complete word
            result.append(node.word)
            node.word = None         # Prevent duplicate addition
        # Mark visited and explore 4 directions
        board[r][c] = '#'
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, node)
        board[r][c] = ch  # Restore (backtrack)

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return result
```

- **Time:** O(m × n × 3^L) — each cell starts DFS, 3 directions per step (not 4, since one is "back")
- **Space:** O(total chars in all words) — Trie storage
- **Edge Cases:** Empty word list: Return []. Words not on board: Return []. Words that are prefixes of other words: Both should be found if they exist.
- **Common Mistakes:** Forgetting to restore board cell after DFS (breaks subsequent searches). Not removing found words from Trie (adds duplicates). Starting DFS from cells that don't match the first character of any word (wasteful).
- **Pattern Recognition:** "Multiple word search in grid" → Trie + DFS backtracking; combines Problem 28 (Word Search) with Trie data structure. Also useful for: autocomplete, spell checking, prefix matching.

---

## Problem 35 — N-Queens II (Hard)

**Problem Explanation:**
Same as N-Queens (Problem 29), but instead of returning all distinct board configurations, just return the **count** of valid solutions. For n=8, the answer is 92. This is a counting-only version that avoids storing boards, using less memory.

**Algorithm Steps:**
1. Initialize `count = [0]` (use list for mutable closure), column and diagonal sets
2. Define `backtrack(row)`:
   a. If `row == n`: increment count, return
   b. For each `col` in 0..n-1:
      - Skip if column/diagonal conflict
      - Place queen (add to sets), recurse, remove queen
3. Call `backtrack(0)` and return count

**Key Insight:**
The algorithm is identical to N-Queens — same recursive structure, same conflict detection. The only difference is we increment a counter instead of building a board representation. This is slightly faster and uses O(n) instead of O(n²) space since we don't store the board.

**Solution:**
```python
def totalNQueens(n):
    # Use a list to allow mutation in nested function
    count = [0]
    cols = set()
    pos_diag = set()  # row + col — '/' diagonals
    neg_diag = set()  # row - col — '\' diagonals
    
    def backtrack(row):
        if row == n:
            count[0] += 1   # Found one valid placement
            return
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            backtrack(row + 1)
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)
    
    backtrack(0)
    return count[0]
```

- **Time:** O(n!) — same as N-Queens
- **Space:** O(n) — sets only, no board storage
- **Edge Cases:** Known values: 1→1, 2→0, 3→0, 4→2, 5→10, 6→4, 7→40, 8→92, 9→352.
- **Common Mistakes:** Using a plain integer `count` instead of a list (closures in Python can't rebind non-local integers without `nonlocal` keyword). Forgetting to backtrack by removing from sets. Using `=` instead of `+=` to increment (resets count).
- **Pattern Recognition:** "Count solutions to constraint problem" → backtracking with counter; same as N-Queens but without board storage. Variants: count solutions to Sudoku, count ways to place non-attacking rooks.

---

## Problem 36 — Alien Dictionary (Hard)

**Problem Explanation:**
You have a list of words from an alien language, sorted lexicographically according to some unknown character order. Determine the order of characters in the alien alphabet. For example, given `["wrt", "wrf", "er", "ett", "rftt"]`, the order might be `"wertf"`. This is essentially a topological sort problem — each pair of adjacent words gives a directed edge between characters.

**Algorithm Steps:**
1. Build adjacency list and in-degree map for all unique characters in words
2. For each adjacent pair `(w1, w2)`:
   a. If `w1` is longer than `w2` and `w1` starts with `w2`: invalid → return ""
   b. Find first differing character `(c1, c2)`: add edge `c1 → c2` (if not already present), increment in-degree of `c2`
3. Kahn's algorithm for topological sort:
   a. Initialize queue with all nodes having in-degree 0
   b. Pop node, add to order, decrement in-degree of neighbors, add to queue if in-degree becomes 0
4. If order length equals total unique characters: return order string. Else: return "" (cycle detected)

**Visual Walkthrough:**
```
words = ["wrt", "wrf", "er", "ett", "rftt"]

All unique chars: {w, r, t, f, e}

Comparing adjacent words:
  "wrt" vs "wrf": first diff at index 2: 't' vs 'f' → t → f
  "wrf" vs "er":  first diff at index 0: 'w' vs 'e' → w → e
  "er" vs "ett":  first diff at index 1: 'r' vs 't' → r → t
  "ett" vs "rftt": first diff at index 0: 'e' vs 'r' → e → r

Graph: t → f, w → e, r → t, e → r

In-degree: w:0, e:1, r:1, t:1, f:1

Kahn's algorithm:
  Queue: [w] (in-degree 0)
  Pop w → order=[w], neighbor e in-degree=0 → queue=[e]
  Pop e → order=[w,e], neighbor r in-degree=0 → queue=[r]
  Pop r → order=[w,e,r], neighbor t in-degree=0 → queue=[t]
  Pop t → order=[w,e,r,t], neighbor f in-degree=0 → queue=[f]
  Pop f → order=[w,e,r,t,f]

len(order)=5 = len(unique chars) ✓
Result: "wertf"
```

**Key Insight:**
Comparing adjacent words in a sorted list reveals the order relationships. The first differing character between adjacent words gives a direct edge `char_before → char_after`. The special case where a longer word appears before its prefix (`"abc"` before `"ab"`) is always invalid — no ordering can make this work. Topological sort (Kahn's algorithm) then gives the character order, or detects a cycle if the input is contradictory.

**Solution:**
```python
from collections import defaultdict, deque

def alienOrder(words):
    # Adjacency list and in-degree for each unique character
    adj = defaultdict(set)
    in_degree = {c: 0 for w in words for c in w}
    
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        # Invalid: longer word before its prefix
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""
        # Find first differing character → add directed edge
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in adj[c1]:
                    adj[c1].add(c2)
                    in_degree[c2] += 1
                break  # Only first diff matters
    
    # Kahn's topological sort
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If cycle exists, order won't include all chars
    return ''.join(order) if len(order) == len(in_degree) else ""
```

- **Time:** O(C) — total characters across all words
- **Space:** O(1) — at most 26 unique characters
- **Edge Cases:** Only one word: Return all unique chars in any order (no constraints). Words not providing enough information: May return partial order. Cycle detection: If input contradicts itself (e.g., w→e and e→w), return "".
- **Common Mistakes:** Not handling the prefix case (`w1.startswith(w2)` and `len(w1) > len(w2)`). Adding edges for ALL differing characters (only the FIRST difference matters). Forgetting to break after adding the edge. Not checking for cycles after topological sort.
- **Pattern Recognition:** "Derive order from sorted words" → character-level topological sort; classic problem that combines two patterns: pairwise comparison and graph traversal.

---

## Problem 37 — Factor Combinations (Hard)

**Problem Explanation:**
Given an integer `n > 1`, find all possible ways to factor it into integers greater than 1. The factors in each combination should be in non-decreasing order. For example, 12 can be factored as [2,6], [2,2,3], and [3,4]. Prime numbers have no valid factorizations.

**Algorithm Steps:**
1. Initialize result list
2. Define `backtrack(start, remaining, path)`:
   a. If `path` is not empty: add `path + [remaining]` as a valid factorization
   b. For `i` from `start` to `sqrt(remaining)`:
      - If `remaining % i == 0`:
        - Append i, recurse with `backtrack(i, remaining // i, path)`, pop
3. Call `backtrack(2, n, [])` and return result

**Visual Walkthrough:**
```
n = 12

backtrack(2, 12, [])
  i=2: 12%2=0 → path=[2]
    backtrack(2, 6, [2])
      path non-empty → add [2, 6] to result
      sqrt(6)=2.44, i=2: 6%2=0 → path=[2,2]
        backtrack(2, 3, [2,2])
          path non-empty → add [2,2,3] to result
          sqrt(3)=1.73, loop: i=2 > 1.73 → no iterations
        pop → [2]
      i=3: 3 > 2.44 → loop ends
    pop → []
  i=3: 12%3=0 → path=[3]
    backtrack(3, 4, [3])
      path non-empty → add [3,4] to result
      sqrt(4)=2, i=3 > 2 → no iterations
    pop → []
  i=4: sqrt(12)=3.46, i=4 > 3.46 → loop ends

Result: [[2,6], [2,2,3], [3,4]]
```

**Key Insight:**
The factorization is recursive: if `i` divides `remaining`, then `(i, remaining//i)` is a factor pair, and we can further factor `remaining//i`. The √n bound on trial division is crucial: if `i` is a factor, `i <= sqrt(remaining)`, and the complement `remaining//i` is already captured by the recursive call or added directly. Starting from `i` (not 2) prevents duplicate factorizations like `[2,2,3]` and `[2,3,2]`.

**Solution:**
```python
def getFactors(n):
    result = []
    
    def backtrack(start, remaining, path):
        # Every non-empty path produces a valid factorization
        if path:
            result.append(path + [remaining])
        # Try factors from start to sqrt(remaining)
        for i in range(start, int(remaining**0.5) + 1):
            if remaining % i == 0:
                path.append(i)
                # Recurse with quotient, using i as new start
                backtrack(i, remaining // i, path)
                path.pop()
    
    backtrack(2, n, [])
    return result
```

- **Time:** O(√n^(log n)) — branching factor decreases with depth
- **Space:** O(log n) — recursion depth (number of factors)
- **Edge Cases:** Prime numbers (like 37): Return [] (no factorizations). n=2: Return [] (no factor > 1). n=1: Return [] (input constraint says n>1). Large prime n: Loop still runs √n steps but no factors found.
- **Common Mistakes:** Including n itself as a factor (like `[12]`). Allowing factor 1 (invalid — factors must be > 1). Not adding `path + [remaining]` when path is non-empty (misses complete factorizations). Using `range(2, ...)` instead of `range(start, ...)` (creates duplicate factorizations in different orders).
- **Pattern Recognition:** "All factorizations of a number" → recursive factorization with √n bound; similar pattern to: prime factorization, combination sum (with multiplication instead of addition).

---

## Problem 38 — Crossword Solver (Hard)

**Problem Explanation:**
You have a crossword grid where `'+'` represents blocked cells, `'-'` represents empty cells, and letters represent pre-filled cells. You also have a list of words to place. Words can go across (left to right) or down (top to bottom). Each word must be placed in a slot that exactly matches its length, and letters must match any pre-filled cells. Find a placement for all words that fills all empty cells.

**Algorithm Steps:**
1. `find_slots()`: Scan board for horizontal and vertical consecutive `'-'` sequences (length > 1). Return list of slots with direction, start position, and length
2. `can_place(slot, word)`: Check if word fits in slot — exact length match, and any filled cells match corresponding word letters
3. `place(slot, word)`: Fill slot with word letters, tracking which cells were newly filled
4. `unplace(placed)`: Restore newly filled cells back to `'-'`
5. `backtrack(idx, remaining_words)`:
   a. If no remaining words: return True
   b. Find all slots; if none: return `len(remaining_words) == 0`
   c. Pick the first slot (or most constrained)
   d. For each word that fits: place it, recurse, unplace if fails
6. Call `backtrack(0, set(words))`, return solved board

**Key Insight:**
The most important optimization is picking slots strategically — choosing the shortest slot or the one with the most pre-filled letters reduces branching. The backtracking structure here is a "constraint assignment" problem: assign words to slots, checking compatibility. The slot-finding algorithm scans the board each time to handle the dynamic nature (placing a word in one slot may affect overlapping slots).

**Solution:**
```python
def solveCrossword(board, words):
    rows, cols = len(board), len(board[0])

    def find_slots():
        """Find all unfilled horizontal and vertical slots."""
        slots = []
        # Horizontal slots (scan each row)
        for r in range(rows):
            count = 0
            for c in range(cols + 1):
                if c < cols and board[r][c] == '-':
                    count += 1
                else:
                    if count > 1:
                        slots.append(('h', r, c - count, count))
                    count = 0
        # Vertical slots (scan each column)
        for c in range(cols):
            count = 0
            for r in range(rows + 1):
                if r < rows and board[r][c] == '-':
                    count += 1
                else:
                    if count > 1:
                        slots.append(('v', r - count, c, count))
                    count = 0
        return slots

    def can_place(slot, word):
        """Check if word fits in the given slot."""
        direction, r, c, length = slot
        if len(word) != length:
            return False
        for i in range(length):
            cr = r + (i if direction == 'v' else 0)
            cc = c + (i if direction == 'h' else 0)
            # Cell must match if pre-filled
            if board[cr][cc] != '-' and board[cr][cc] != word[i]:
                return False
        return True

    def place(slot, word):
        """Place word into slot, return list of newly filled cells."""
        direction, r, c, length = slot
        placed = []
        for i in range(length):
            cr = r + (i if direction == 'v' else 0)
            cc = c + (i if direction == 'h' else 0)
            if board[cr][cc] == '-':
                board[cr][cc] = word[i]
                placed.append((cr, cc))
        return placed

    def unplace(placed):
        """Restore cells back to empty."""
        for cr, cc in placed:
            board[cr][cc] = '-'

    def backtrack(idx, remaining_words):
        if not remaining_words:
            return True                     # All words placed
        slots = find_slots()                # Find current empty slots
        if not slots:
            return len(remaining_words) == 0
        
        slot = slots[0]  # Pick first slot (can be optimized: pick most constrained)
        for word in list(remaining_words):
            if can_place(slot, word):
                placed = place(slot, word)
                remaining_words.remove(word)
                if backtrack(idx + 1, remaining_words):
                    return True
                remaining_words.add(word)   # Restore word
                unplace(placed)             # Restore board
        return False

    word_set = set(words)
    backtrack(0, word_set)
    return board  # Board is modified in-place
```

- **Time:** O(m! × n) factorial in worst case — but heavily pruned by constraints
- **Space:** O(m × n) — board size
- **Edge Cases:** No words left but empty slots: backtrack returns false. All words placed and no empty slots: success. Overlapping slots (across + down at same cell) must agree on the shared letter.
- **Common Mistakes:** Not placing words correctly (direction confusion with r/c indexing). Not tracking which cells were newly filled vs pre-filled (restoring pre-filled cells ruins the board). Finding slots once at the beginning instead of dynamically (slots change as words are placed). Forgetting to convert to list when iterating over `remaining_words` set during modification.
- **Pattern Recognition:** "Crossword/word placement on grid" → constraint satisfaction with backtracking; similar to Sudoku and N-Queens (assign values to constrained positions). Optimization tactic: "most constrained variable" heuristic is common in CSP problems.

---

# ═══════════════════════════════════════════════════════════════
# CHEAT SHEET: GREEDY vs BACKTRACKING
# ═══════════════════════════════════════════════════════════════

| Aspect | Greedy | Backtracking |
|--------|--------|--------------|
| **Strategy** | Pick locally optimal, hope for global | Explore all paths, prune invalid |
| **When to use** | Matroid problems, exchange arguments | Constraint satisfaction, combinatorial |
| **Time** | Usually O(n log n) | Usually exponential |
| **Space** | Usually O(1) | O(depth of recursion) |
| **Key proof** | Exchange argument / greedy choice property | Pruning correctness |
| **Examples** | Interval scheduling, coin change (canonical), Huffman | N-Queens, Sudoku, Subset/Permutation |

---

# ═══════════════════════════════════════════════════════════════
# KEY PATTERNS FOR INFOSYS SP DSE
# ═══════════════════════════════════════════════════════════════

### Greedy Patterns:
1. **Sort by end → interval scheduling** (Problems 12, 13)
2. **Sort by value/ratio → priority queue** (Problems 16, 17, 18)
3. **Track min/max while scanning** (Problems 2, 3, 7, 8)
4. **Two-heap approach** (Problems 14, 16, 17)
5. **Frequency-based** (Problems 4, 9, 11)
6. **Two-pass scan** (Problem 15)

### Backtracking Patterns:
1. **Subset/Combination with start index** (Problems 19, 20, 24, 25, 26)
2. **Permutation with visited array** (Problems 21, 22)
3. **Grid DFS with in-place marking** (Problems 28, 34)
4. **Constraint satisfaction** (Problems 29, 30, 35)
5. **String partitioning** (Problems 27, 31, 32, 33)
6. **Trie + DFS** (Problem 34)

---

# ═══════════════════════════════════════════════════════════════
# COMPLEXITY QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════

| # | Problem | Time | Space |
|---|---------|------|-------|
| 1 | Maximum Units Truck | O(n log n) | O(1) |
| 2 | Buy Sell Stock | O(n) | O(1) |
| 3 | Jump Game | O(n) | O(1) |
| 4 | Lemonade Change | O(n) | O(1) |
| 5 | Assign Cookies | O(n log n) | O(1) |
| 6 | Max 69 Number | O(d) | O(d) |
| 7 | Jump Game II | O(n) | O(1) |
| 8 | Gas Station | O(n) | O(1) |
| 9 | Task Scheduler | O(n) | O(1) |
| 10 | Queue Reconstruction | O(n²) | O(n) |
| 11 | Hand of Straights | O(n log n) | O(n) |
| 12 | Min Arrows Balloons | O(n log n) | O(1) |
| 13 | Non-overlapping Intervals | O(n log n) | O(1) |
| 14 | Meeting Rooms II | O(n log n) | O(n) |
| 15 | Candy | O(n) | O(n) |
| 16 | IPO | O(n log n) | O(n) |
| 17 | Min Cost K Workers | O(n log n) | O(n) |
| 18 | Course Schedule III | O(n log n) | O(n) |
| 19 | Subsets | O(n×2ⁿ) | O(n) |
| 20 | Subsets II | O(n×2ⁿ) | O(n) |
| 21 | Permutations | O(n×n!) | O(n) |
| 22 | Permutations II | O(n×n!) | O(n) |
| 23 | Letter Combinations | O(4ⁿ×n) | O(n) |
| 24 | Combination Sum | O(N^(T/M)) | O(T/M) |
| 25 | Combination Sum II | O(2ⁿ) | O(target) |
| 26 | Combination Sum III | O(C(9,k)) | O(k) |
| 27 | Palindrome Partition | O(n×2ⁿ) | O(n) |
| 28 | Word Search | O(m×n×4^L) | O(L) |
| 29 | N-Queens | O(n!) | O(n²) |
| 30 | Sudoku Solver | O(9^empty) | O(1) |
| 31 | Restore IP | O(1) | O(1) |
| 32 | Generate Parentheses | O(4ⁿ/√n) | O(n) |
| 33 | Expression Add Operators | O(4ⁿ) | O(n) |
| 34 | Word Search II | O(m×n×3^L) | O(total chars) |
| 35 | N-Queens II | O(n!) | O(n) |
| 36 | Alien Dictionary | O(C) | O(1) |
| 37 | Factor Combinations | O(√n×log n) | O(log n) |
| 38 | Crossword Solver | O(m!×n) | O(m×n) |

---

# ═══════════════════════════════════════════════════════════════
# INTERVIEW TIPS
# ═══════════════════════════════════════════════════════════════

### Greedy Problems — What to Say:
1. "Can I prove the greedy choice property?"
2. "Does sorting help reveal the structure?"
3. "Can I use an exchange argument to prove optimality?"
4. "Is this a matroid structure?"

### Backtracking Problems — What to Say:
1. "This is a combinatorial problem — let me think about the state space."
2. "At each step, I choose from a set of valid options."
3. "Let me define what 'valid' means and prune early."
4. "The base case is when I've made all n choices."

### Common Mistakes to Avoid:
- Greedy: Assuming greedy works when it doesn't (always verify or prove)
- Backtracking: Forgetting to undo state after recursive call (the pop/unplace step)
- Greedy: Not handling edge cases (empty input, single element)
- Backtracking: Not sorting input when duplicate handling is needed

---

> **Total: 38 problems | ~2100 lines | Ready for Infosys SP DSE**

# ═══════════════════════════════════════════════════════════════
# STEP-BY-STEP DRY RUNS (KEY PROBLEMS)
# ═══════════════════════════════════════════════════════════════

### Dry Run: Problem 2 — Buy Sell Stock
```
prices = [7, 1, 5, 3, 6, 4]

Day 0: p=7, min_price=7, max_profit=0
Day 1: p=1, min_price=1, max_profit=0
Day 2: p=5, min_price=1, max_profit=4  (buy@1 sell@5)
Day 3: p=3, min_price=1, max_profit=4
Day 4: p=6, min_price=1, max_profit=5  (buy@1 sell@6)
Day 5: p=4, min_price=1, max_profit=5

Answer: 5
Key insight: We never actually track buy/sell day,
just the running maximum profit.
```

### Dry Run: Problem 3 — Jump Game
```
nums = [2, 3, 1, 1, 4]

i=0: jump=2, farthest = max(0, 0+2) = 2
i=1: jump=3, farthest = max(2, 1+3) = 4
  4 >= last_index(4) => can reach end!

nums = [3, 2, 1, 0, 4]

i=0: jump=3, farthest = max(0, 0+3) = 3
i=1: jump=2, farthest = max(3, 1+2) = 3
i=2: jump=1, farthest = max(3, 2+1) = 3
i=3: jump=0, farthest = max(3, 3+0) = 3
i=4: i(4) > farthest(3) => return False!
  Cannot jump over the zero-gap at index 3.
```

### Dry Run: Problem 4 — Lemonade Change
```
bills = [5, 5, 5, 10, 20]

b=5:  fives=1, tens=0
b=5:  fives=2, tens=0
b=5:  fives=3, tens=0
b=10: fives=2, tens=1  (give one $5 change)
b=20: tens>0 && fives>0 => give $10+$5
      fives=1, tens=0

All customers served! Return True.

bills = [5, 5, 10, 10, 20]

b=5:  fives=1
b=5:  fives=2
b=10: fives=1, tens=1
b=10: fives=0, tens=2
b=20: need change for $20
  tens>0 && fives>0? No (fives=0)
  fives>=3? No (fives=0)
  => Return False!

Cannot give change for the $20 bill.
```

### Dry Run: Problem 7 — Jump Game II
```
nums = [2, 3, 1, 1, 4]

jumps=0, end=0, farthest=0

i=0: farthest = max(0, 0+2) = 2
  i==end(0) => jumps=1, end=2
i=1: farthest = max(2, 1+3) = 4
i=2: farthest = max(4, 2+1) = 4
  i==end(2) => jumps=2, end=4
i=3: farthest = max(4, 3+1) = 4

Loop ends (i < len-1 = 4)
Answer: 2 jumps
  Jump 1: index 0 -> index 1 (can reach up to index 2)
  Jump 2: index 1 -> index 4 (can reach up to index 4) done!
```

### Dry Run: Problem 8 — Gas Station
```
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]

diff = [-2, -2, -2, 3, 3]
total_tank = 0

i=0: curr_tank=-2 < 0 => start=1, curr_tank=0
i=1: curr_tank=-2 < 0 => start=2, curr_tank=0
i=2: curr_tank=-2 < 0 => start=3, curr_tank=0
i=3: curr_tank=3
i=4: curr_tank=6

total_tank=6 >= 0 => answer=3

Verification from station 3:
  3->4: gas=4, cost=1, tank=3
  4->0: gas=5, cost=2, tank=6
  0->1: gas=1, cost=3, tank=4
  1->2: gas=2, cost=4, tank=2
  2->3: gas=3, cost=5, tank=0  (Complete circuit!)
```

### Dry Run: Problem 9 — Task Scheduler
```
tasks = ['A','A','A','B','B','B'], n = 2

freq: A=3, B=3
max_freq = 3
max_count = 2 (both A and B have freq 3)

formula = (3-1) * (2+1) + 2 = 2*3 + 2 = 8
actual  = len(tasks) = 6
result  = max(6, 8) = 8

Layout with n=2 cooldown:
  Slot: 0  1  2  3  4  5  6  7
  A:    A  .  .  A  .  .  A  .
  B:    .  B  .  .  B  .  .  B
  Merged: A B . A B . A B = 8 intervals

Without formula: you might think 6 intervals work,
but the cooldown constraint forces idle slots.
```

### Dry Run: Problem 12 — Min Arrows Balloons
```
points = [[10,16],[2,8],[1,6],[7,12]]

Sorted by end: [[1,6],[2,8],[7,12],[10,16]]

arrows=1, end=6
  [2,8]:  2 <= 6? Yes (overlap) => skip
  [7,12]: 7 > 6?  Yes (no overlap) => arrows=2, end=12
  [10,16]: 10 > 12? No (overlap) => skip

Answer: 2 arrows
  Arrow 1 at x=6 bursts [1,6] and [2,8]
  Arrow 2 at x=12 bursts [7,12] and [10,16]
```

### Dry Run: Problem 15 — Candy
```
ratings = [1, 3, 2, 2, 1]

Pass 1 (left to right):
  candies = [1, 2, 1, 1, 1]
  r[1]=3 > r[0]=1 => c[1] = c[0]+1 = 2
  r[2]=2 < r[1]=3 => c[2] = 1 (no change)
  r[3]=2 = r[2]=2 => c[3] = 1 (no change)
  r[4]=1 < r[3]=2 => c[4] = 1 (no change)

Pass 2 (right to left):
  candies = [1, 2, 1, 2, 1]
  r[3]=2 > r[4]=1 => c[3] = max(1, c[4]+1) = 2
  r[2]=2 = r[3]=2 => no change
  r[1]=3 > r[2]=2 => c[1] = max(2, c[2]+1) = 2
  r[0]=1 < r[1]=3 => no change

Total = 1+2+1+2+1 = 7
```

### Dry Run: Problem 17 — Min Cost to Hire K Workers
```
quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3

Workers sorted by ratio (wage/quality):
  (2.0, 10), (2.0, 1), (2.33, 3), (2.67, 1), (7.0, 1)

Step 1: ratio=2.0, q=10 => heap=[-10], total_q=10
Step 2: ratio=2.0, q=1  => heap=[-10,-1], total_q=11
  len(2) < k(3) => no result yet
Step 3: ratio=2.33, q=3 => heap=[-10,-1,-3], total_q=14
  len==k => result = min(inf, 2.33*14) = 32.67
Step 4: ratio=2.67, q=1 => heap=[-10,-1,-3,-1], total_q=15
  len>k => pop -10 => total_q=5, heap=[-3,-1,-1]
  result = min(32.67, 2.67*5) = 13.33
Step 5: ratio=7.0, q=1 => heap=[-3,-1,-1,-1], total_q=6
  len>k => pop -3 => total_q=3, heap=[-1,-1,-1]
  result = min(13.33, 7.0*3) = 13.33

Answer: 13.33
```

### Dry Run: Problem 32 — Generate Parentheses (n=3)
```
backtrack(path="", open=0, close=0)
|-- add '(' => path="(", open=1, close=0
|   |-- add '(' => path="((", open=2, close=0
|   |   |-- add '(' => path="(((", open=3, close=0
|   |   |   |-- add ')' => path="((()", open=3, close=1
|   |   |   |   |-- add ')' => path="((())", open=3, close=2
|   |   |   |   |   |-- add ')' => "((()))" -- SOLUTION 1
|   |   |   |   |-- add '(' => open=3==n => skip
|   |   |   |-- add '(' => open=3==n => skip
|   |   |-- add ')' => path="(()", open=2, close=1
|   |       |-- add ')' => path="(())", open=2, close=2
|   |       |   |-- add ')' => open closed, can't
|   |       |   |-- add '(' => path="(()(", open=3, close=2
|   |       |       |-- add ')' => "(()())" -- SOLUTION 2
|   |       |-- add '(' => path="(()(", open=3, close=1
|   |           |-- add ')' => path="(()()", open=3, close=2
|   |               |-- add ')' => "(())" -- nope...
|   |               (continue until "()(())" found)
|   |-- add ')' => path="()", open=1, close=1
|       |-- add '(' => path="()(", open=2, close=1
|       |   |-- add '(' => path="()((", open=3, close=1
|       |   |   |-- add ')' => "()(())" -- SOLUTION 4
|       |   |-- add ')' => path="()()", open=2, close=2
|       |       |-- add '(' => "()()(" , open=3, close=2
|       |       |   |-- add ')' => "()()()" -- SOLUTION 5
|       |-- add ')' => close>open => skip

Result: ["((()))","(()())","(())()","()(())","()()()"]
Count = C(3) = 5
```

### Dry Run: Problem 29 — N-Queens (n=4)
```
Board 4x4, backtrack row by row:

Row 0: Try col=0
  Place Q at (0,0): cols={0}, pos={0}, neg={0}
  Row 1: Try col=1 => pos_diag=2 in set? No
    Place Q at (1,1): cols={0,1}, pos={0,2}, neg={0,0}
    Row 2: col=0 in cols, col=1 in cols, col=2 pos_diag=4, col=3 pos_diag=5
      All fail => backtrack
  Row 1: Try col=2
    Place Q at (1,2): cols={0,2}, pos={0,3}, neg={0,-1}
    Row 2: Try col=1 => pos_diag=3 in set? Yes => skip
      Try col=3 => pos_diag=5, neg_diag=-1 in set! => skip
      No valid => backtrack
  Row 1: Try col=3
    Place Q at (1,3): cols={0,3}, pos={0,4}, neg={0,-2}
    Row 2: Try col=1
      Place Q at (2,1): cols={0,1,3}, pos={0,1,4}, neg={0,-1,-2}
      Row 3: col=2 => pos_diag=5 not in set, neg_diag=1 not in set
        Place Q at (3,2)! cols={0,1,2,3}
        Row 4: row==n => SOLUTION FOUND!
          . Q . .
          . . . Q
          Q . . .
          . . Q .

(Continue exploring to find solution 2...)
```

---

# ═══════════════════════════════════════════════════════════════
# BACKTRACKING TEMPLATE (REUSABLE PATTERN)
# ═══════════════════════════════════════════════════════════════

```python
def backtrack_template(candidates, target, start, path, result):
    """
    Universal backtracking skeleton.
    Modify: the 'for' range, the validity check, and the recursive call.
    """
    # BASE CASE: when to add path to result
    if is_complete(path):
        result.append(path[:])  # or path.copy()
        return

    # PRUNING: early termination
    if is_impossible(path):
        return

    # CHOICE LOOP: iterate over valid options
    for i in range(start, len(candidates)):
        # PRUNE: skip invalid/duplicate choices
        if should_skip(i, candidates, start):
            continue

        # CHOOSE
        path.append(candidates[i])

        # RECURSE (go deeper)
        backtrack(candidates, target, i + 1, path, result)

        # UNCHOOSE (backtrack)
        path.pop()
```

### Template Adaptations by Problem Type:

| Problem Type | start | Loop Range | Reuse? | Duplicate Skip |
|---|---|---|---|---|
| Subsets | 0 | i+1 to n | No | `i > start` check |
| Permutations | 0 | 0 to n (all) | No | `used[]` array |
| Combinations | 0 | i+1 to n | No | `i > start` check |
| Combination Sum | 0 | i to n (reuse) | Yes | Not needed (unique input) |
| Word Search | each cell | 4 directions | No | In-place `'#'` mark |
| N-Queens | row 0 | 0 to n cols | No | `cols`, `diags` sets |

---

# ═══════════════════════════════════════════════════════════════
# GREEDY PROOF TECHNIQUES
# ═══════════════════════════════════════════════════════════════

### 1. Exchange Argument (Problems 12, 13, 18)
```
To prove greedy is optimal:
1. Assume optimal solution O differs from greedy G
2. Find the first point where they differ
3. Show you can "exchange" O's choice for G's choice
   without making the solution worse
4. This means G is at least as good as O
```

Example (Interval Scheduling -- Problem 12):
- Greedy picks interval with earliest end
- If optimal picks a different first interval, we can swap it
  for the greedy one (ends earlier, leaving more room)
- No intervals are lost, so the swap does not hurt

### 2. Greedy Choice Property (Problems 1, 5, 16)
```
There exists an optimal solution that includes
the greedy choice. Once the greedy choice is made,
the remaining subproblem has the same structure.
```

Example (Assign Cookies -- Problem 5):
- Give the smallest cookie to the least greedy child
- If an optimal solution does not do this, we can swap
  cookies without reducing the count of content children

### 3. Matroid Structure (Problems 12, 13)
```
A problem has optimal greedy solution if it has
matroid structure:
1. Empty set is independent
2. Subsets of independent sets are independent (hereditary)
3. If |A| < |B| for independent sets, there exists
   b in B\A such that A union {b} is independent (exchange)
```

Interval scheduling on a matroid means greedy is optimal.

---

# ═══════════════════════════════════════════════════════════════
# PRUNING TECHNIQUES IN BACKTRACKING
# ═══════════════════════════════════════════════════════════════

### 1. Feasibility Pruning
```
If remaining < 0 or remaining < smallest candidate -> prune
Used in: Combination Sum, Combination Sum II/III
Example: if remaining=3 and next candidate=5, skip all remaining (sorted)
```

### 2. Duplicate Pruning
```
Sort input. At each level, skip same value as previous.
Condition: if i > start and nums[i] == nums[i-1]: skip
Used in: Subsets II, Permutations II, Combination Sum II
```

### 3. Symmetry Breaking
```
When choices produce symmetric results, fix one dimension.
Used in: N-Queens (place row by row, not all cells)
         Sudoku (fill cells left-to-right, top-to-bottom)
```

### 4. Constraint Propagation
```
After making a choice, immediately eliminate impossible
options for other cells.
Used in: Sudoku Solver (eliminate from row/col/box)
         N-Queens (eliminate diagonals)
```

### 5. Ordering Heuristic
```
Try the most constrained option first.
If it fails, fail fast. If it succeeds, likely optimal.
Used in: Crossword Solver (pick shortest/most-filled slot)
         Sudoku (try digit with fewest possibilities)
```

---

# ═══════════════════════════════════════════════════════════════
# COMMON PITFALLS AND DEBUGGING TIPS
# ═══════════════════════════════════════════════════════════════

### Greedy Mistakes:
```
1. Assuming greedy works without proof
   - Always verify: does local optimal lead to global optimal?
   - Counter: Coin change with coins [1, 3, 4] and target 6
     Greedy: 4+1+1 = 3 coins (optimal: 3+3 = 2 coins)

2. Wrong sorting criterion
   - Problem 12/13: Sort by END, not by START or LENGTH
   - Problem 10: Sort by HEIGHT descending, then K ascending
   - Problem 17: Sort by RATIO (wage/quality), not by quality

3. Not handling ties properly
   - Problem 9: Multiple tasks with same max frequency
   - Formula uses count_of_max, not just max_freq

4. Forgetting the "total" check
   - Problem 8: Always check total_gas >= total_cost first
   - Without this, you might return an invalid start index
```

### Backtracking Mistakes:
```
1. Forgetting to undo state (the pop/unplace step)
   - Most common bug in backtracking
   - Every append must have a matching pop
   - Every place() must have a matching unplace()

2. Not sorting when handling duplicates
   - Problems 20, 22, 25 all need sorted input
   - Without sorting, duplicate skipping does not work

3. Wrong "start" index causing duplicates or missing solutions
   - Subsets/Combinations: start = i+1 (no reuse)
   - Combination Sum: start = i (allow reuse)
   - Permutations: no start index, use used[] array

4. Off-by-one in base case
   - Subsets: add path at EVERY node, not just leaves
   - Permutations: add path only when len(path) == len(nums)
   - Combinations: add path when remaining == 0

5. Modifying a shared data structure without copying
   - result.append(path) stores a REFERENCE (will change later!)
   - Always use result.append(path[:]) or path.copy()
```

---

# ═══════════════════════════════════════════════════════════════
# INFOSYS SP DSE INTERVIEW SCENARIOS
# ═══════════════════════════════════════════════════════════════

### Scenario 1: "Tell me about greedy algorithms"
```
Good answer:
"Greedy algorithms make locally optimal choices at each step
with the hope of finding a global optimum. They work when
the problem has greedy choice property and optimal substructure.
I've solved problems like interval scheduling (sort by end),
activity selection, and job scheduling using greedy."

Follow-up: "When does greedy fail?"
"Greedy fails when local optimum does not lead to global optimum.
For example, coin change with non-canonical denominations.
In such cases, we need dynamic programming."
```

### Scenario 2: "Explain backtracking with an example"
```
Good answer:
"Backtracking is a systematic way to explore all possible
solutions by building candidates incrementally and abandoning
a candidate as soon as it determines it cannot lead to a valid
solution. For example, in N-Queens, we place queens row by row.
If placing a queen at (row, col) conflicts with an existing
queen, we prune that entire subtree and try the next column."

Follow-up: "How is it different from brute force?"
"Backtracking prunes the search space. Brute force explores
all n^n possibilities for N-Queens. Backtracking only explores
valid partial solutions, reducing it to roughly O(n!)."
```

### Scenario 3: "Which problems use two-pointer technique?"
```
- Assign Cookies (Problem 5): two sorted arrays, two pointers
- Jump Game: implicit two-pointer (i and farthest)
- Non-overlapping Intervals (Problem 13): one pass with end pointer
- Buy Sell Stock (Problem 2): track min, compute max diff
```

### Scenario 4: "When would you use a heap in greedy?"
```
Two-heap pattern (Problems 14, 16, 17):
- Min-heap to filter/select candidates
- Max-heap to greedily pick the best among candidates
- Useful when you need to dynamically select the best
  from a changing set of options

Examples:
- Meeting Rooms II: min-heap tracks end times of active meetings
- IPO: min-heap for affordable, max-heap for profitable
- Min Cost K Workers: max-heap to keep K smallest qualities
```

### Scenario 5: "Walk me through solving Sudoku with backtracking"
```
1. Find the first empty cell (marked '.')
2. Try digits '1' through '9'
3. For each digit, check if valid (row, column, 3x3 box)
4. If valid, place the digit and recurse on next empty cell
5. If recursion returns True, solution found
6. If no digit works, return False (trigger backtracking)
7. The previous cell will try its next digit
8. When all cells are filled, we have a solution

Key optimization: precompute which cells are empty
and iterate only over them, avoiding repeated scanning.
```

---

# ═══════════════════════════════════════════════════════════════
# RECOMMENDED PRACTICE ORDER
# ═══════════════════════════════════════════════════════════════

### Week 1: Foundation (Easy Greedy + Easy Backtracking)
```
Day 1-2: Problems 2, 3, 6 (one-pass greedy)
Day 3-4: Problems 1, 5 (sort-based greedy)
Day 5: Problem 4 (counting greedy)
Day 6-7: Problems 19, 21, 23 (basic backtracking templates)
```

### Week 2: Intermediate (Medium Greedy + Medium Backtracking)
```
Day 1-2: Problems 7, 8 (advanced one-pass greedy)
Day 3: Problems 12, 13 (interval scheduling family)
Day 4: Problems 9, 11 (frequency-based greedy)
Day 5: Problem 10 (insertion-based greedy)
Day 6: Problem 14 (two-heap greedy)
Day 7: Problems 24, 25, 26 (combination family)
```

### Week 3: Advanced (Hard Greedy + Medium/Hard Backtracking)
```
Day 1-2: Problems 15, 16 (two-pass and two-heap greedy)
Day 3: Problems 17, 18 (exchange argument greedy)
Day 4: Problems 27, 28, 29 (grid and string backtracking)
Day 5: Problems 30, 31, 32 (constraint and string backtracking)
Day 6: Problems 33, 34, 35 (advanced backtracking)
Day 7: Problems 36, 37, 38 (graph and complex backtracking)
```

### Week 4: Mock Interviews
```
Day 1: Pick 3 random greedy problems, solve under 15 min each
Day 2: Pick 3 random backtracking problems, solve under 20 min each
Day 3: Pick 1 hard greedy + 1 hard backtracking, solve under 40 min
Day 4: Practice explaining approach before coding (5 min talk)
Day 5: Full mock: 2 problems in 45 minutes
Day 6: Review all mistakes and weak areas
Day 7: Final revision of templates and patterns
```

---

# ═══════════════════════════════════════════════════════════════
# EXPECTED COMPLEXITIES CHEAT SHEET
# ═══════════════════════════════════════════════════════════════

| Pattern | Typical Time | Typical Space | Example Problems |
|---------|-------------|---------------|------------------|
| Sort + linear scan | O(n log n) | O(1) | 1, 5, 12, 13 |
| Single pass | O(n) | O(1) | 2, 3, 4, 7, 8 |
| Sort + heap | O(n log n) | O(n) | 11, 14, 16, 17, 18 |
| Two-pass | O(n) | O(n) | 15 |
| Formula-based | O(n) | O(1) | 9 |
| Insertion-based | O(n^2) | O(n) | 10 |
| Subset enumeration | O(n * 2^n) | O(n) | 19, 20 |
| Permutation | O(n * n!) | O(n) | 21, 22 |
| Backtrack with pruning | Varies widely | O(depth) | 24-38 |
| Trie + DFS | O(m * n * 3^L) | O(words) | 34 |
| Topological sort | O(V + E) | O(V) | 36 |

---

# ═══════════════════════════════════════════════════════════════
# QUICK REFERENCE: WHEN TO USE WHAT
# ═══════════════════════════════════════════════════════════════

### Use GREEDY when:
- Problem asks for min/max of something
- Sorting reveals a natural order
- You can prove local optimal = global optimal
- Problems involve intervals, scheduling, or ratios
- You see "minimum arrows", "minimum removals", "maximum profit"

### Use BACKTRACKING when:
- Problem asks for ALL solutions (not just count/optimal)
- You need to generate combinations, permutations, subsets
- Grid traversal with word matching
- Constraint satisfaction (N-Queens, Sudoku)
- Problem says "find all", "generate all", "return all valid"

### Use HEAP + GREEDY when:
- You need the Kth largest/smallest dynamically
- You are selecting from a changing set of candidates
- Problems involve "minimum rooms", "most profitable", "best ratio"

### Use TWO-PASS when:
- You need information from both directions
- Left-to-right and right-to-left constraints
- Example: Candy problem (rating > left neighbor AND right neighbor)

---

> **Total: 38 problems | Comprehensive preparation guide | Ready for Infosys SP DSE**
