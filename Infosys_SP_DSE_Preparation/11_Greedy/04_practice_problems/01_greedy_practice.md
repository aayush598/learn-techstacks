# Greedy Practice Problems - Complete Guide

## Problem Category Map

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                GREEDY PROBLEMS PATTERN MAP                       │
  ├─────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  SORT-BASED GREEDY:                                             │
  │  ├── Maximum Units on a Truck (sort by units)                   │
  │  ├── Maximum Product (sort, check extremes)                     │
  │  ├── Queue Reconstruction (sort by height desc)                 │
  │  └── Hand of Straights (sort + min-heap)                        │
  │                                                                  │
  │  TRACKING/MONITORING GREEDY:                                    │
  │  ├── Best Time to Buy/Sell Stock (track min)                    │
  │  ├── Jump Game (track max reachable)                            │
  │  ├── Jump Game II (BFS-like greedy)                             │
  │  └── Gas Station (track tank balance)                           │
  │                                                                  │
  │  HEAP-BASED GREEDY:                                             │
  │  ├── Task Scheduler (max-heap + cooldown)                       │
  │  ├── IPO (max-heap of affordable projects)                      │
  │  └── Min Cost K Workers (sort by ratio + max-heap)              │
  │                                                                  │
  │  LINE SWEEP:                                                    │
  │  ├── Car Pooling (event-based)                                  │
  │  └── Meeting Rooms II (concurrent intervals)                    │
  │                                                                  │
  │  TWO-PASS / TWO-POINTER:                                        │
  │  ├── Candy (left pass + right pass)                             │
  │  └── Valid Triangle Number (sort + two pointers)                │
  │                                                                  │
  └─────────────────────────────────────────────────────────────────┘
```

---

## Easy Problems

### 1. Maximum Units on a Truck

**Problem**: You have `n` boxes, each with `boxTypes[i] = [numberOfBoxesi, numberOfUnitsPerBox]`. Return maximum units that can be put on a truck with capacity `boxCapacity`.

### Visual Walkthrough

```
  INPUT: boxTypes = [[1, 3], [2, 2], [3, 1]], truck_size = 4
  
  STEP 1: Sort by units per box (descending):
  ┌────────────┬───────────────────┐
  │ Units/Box  │  Number of Boxes  │
  ├────────────┼───────────────────┤
  │     3      │        1          │ ◄── highest value first
  │     2      │        2          │
  │     1      │        3          │
  └────────────┴───────────────────┘
  
  STEP 2: Fill truck greedily:
  ┌──────────────────────────────────────────────────────┐
  │ Truck capacity remaining: 4                          │
  │                                                      │
  │ Take 1 box of 3 units → 1 × 3 = 3 units             │
  │   Truck remaining: 4 - 1 = 3                         │
  │                                                      │
  │ Take 2 boxes of 2 units → 2 × 2 = 4 units           │
  │   Truck remaining: 3 - 2 = 1                         │
  │                                                      │
  │ Take 1 box of 1 unit → 1 × 1 = 1 unit               │
  │   Truck remaining: 1 - 1 = 0  (FULL!)                │
  └──────────────────────────────────────────────────────┘
  
  TRUCK: [3][2][2][1] → Total units = 3+2+2+1 = 8
  
  OUTPUT: 8
```

```python
def maximum_units(box_types, truck_size):
    """Maximize units on truck by picking boxes with most units first."""
    # Sort by units per box in descending order
    box_types.sort(key=lambda x: x[1], reverse=True)
    
    total_units = 0
    boxes_used = 0
    
    for num_boxes, units_per_box in box_types:
        if boxes_used + num_boxes <= truck_size:
            # Take all boxes of this type
            total_units += num_boxes * units_per_box
            boxes_used += num_boxes
        else:
            # Take only what fits
            remaining = truck_size - boxes_used
            total_units += remaining * units_per_box
            break
    
    return total_units

# Example
box_types = [[1, 3], [2, 2], [3, 1]]
truck_size = 4
print(maximum_units(box_types, truck_size))  # 8
# Take: 1 box of 3 units, 2 boxes of 2 units, 1 box of 1 unit = 3+4+1 = 8
```

**Time Complexity**: O(n log n)  
**Space Complexity**: O(1)

---

### 2. Maximum Product

**Problem**: Given an integer array, find the maximum product of three numbers.

```python
def maximum_product(nums):
    """Find maximum product of three numbers."""
    nums.sort()
    
    # Either product of three largest
    # Or product of two smallest (negative) and largest
    return max(nums[-1] * nums[-2] * nums[-3],
               nums[0] * nums[1] * nums[-1])

# Example
nums = [1, 2, 3, 4]
print(maximum_product(nums))  # 24

nums = [-1, -2, -3, -4]
print(maximum_product(nums))  # -6

nums = [-1, -2, 3, 4]
print(maximum_product(nums))  # 24
```

**Time Complexity**: O(n log n)  
**Space Complexity**: O(1)

---

### 3. Best Time to Buy and Sell Stock

**Problem**: Find maximum profit from buying and selling a stock once.

### Visual Walkthrough

```
  INPUT: prices = [7, 1, 5, 3, 6, 4]
  
  PRICE CHART:
  Price
  7 │ ●
  6 │                 ●
  5 │     ●
  4 │                         ●
  3 │           ●
  2 │
  1 │       ●
  0 └───┬───┬───┬───┬───┬───┬───
        0   1   2   3   4   5
              Day
  
  GREEDY SCAN (track minimum price):
  ┌─────────────────────────────────────────────────────┐
  │ Day 0: price=7, min_price=7, profit=0              │
  │ Day 1: price=1, min_price=1, profit=0              │
  │ Day 2: price=5, min_price=1, profit=5-1=4          │
  │ Day 3: price=3, min_price=1, profit=3-1=2          │
  │ Day 4: price=6, min_price=1, profit=6-1=5  ← MAX  │
  │ Day 5: price=4, min_price=1, profit=4-1=3          │
  └─────────────────────────────────────────────────────┘
  
  RESULT: Buy at day 1 (price=1), sell at day 4 (price=6)
  Maximum profit = 5
  
  KEY INSIGHT: At each day, the best profit is:
  current_price - minimum_price_so_far
  We track the running minimum as we scan left to right.
```

```python
def max_profit(prices):
    """Find maximum profit from single buy-sell."""
    min_price = float('inf')
    max_profit = 0
    
    for price in prices:
        # Update minimum price seen so far
        min_price = min(min_price, price)
        
        # Calculate profit if we sell today
        profit = price - min_price
        
        # Update maximum profit
        max_profit = max(max_profit, profit)
    
    return max_profit

# Example
prices = [7, 1, 5, 3, 6, 4]
print(max_profit(prices))  # 5 (buy at 1, sell at 6)

prices = [7, 6, 4, 3, 1]
print(max_profit(prices))  # 0 (no profit possible)
```

**Time Complexity**: O(n)  
**Space Complexity**: O(1)

---

## Medium Problems

### 4. Jump Game

**Problem**: Determine if you can reach the last index.

### Visual Walkthrough

```
  INPUT: nums = [2, 3, 1, 1, 4]
  
  INDEX:  0   1   2   3   4
  VALUE:  2   3   1   1   4
          ▲
          │
  Start here
  
  GREEDY SCAN (track max reachable):
  ┌────────────────────────────────────────────────────────┐
  │ i=0: max_reach = max(0, 0+2) = 2                      │
  │   Can reach indices 0, 1, 2                            │
  │                                                        │
  │ i=1: max_reach = max(2, 1+3) = 4                      │
  │   Can reach indices 0, 1, 2, 3, 4  ← REACHED END!     │
  │                                                        │
  │ i=2: max_reach = max(4, 2+1) = 4                      │
  │ i=3: max_reach = max(4, 3+1) = 4                      │
  └────────────────────────────────────────────────────────┘
  
  INPUT: nums = [3, 2, 1, 0, 4]
  
  INDEX:  0   1   2   3   4
  VALUE:  3   2   1   0   4
          ▲
          │
  
  GREEDY SCAN:
  ┌────────────────────────────────────────────────────────┐
  │ i=0: max_reach = max(0, 0+3) = 3                      │
  │ i=1: max_reach = max(3, 1+2) = 3                      │
  │ i=2: max_reach = max(3, 2+1) = 3                      │
  │ i=3: max_reach = max(3, 3+0) = 3                      │
  │ i=4: i=4 > max_reach=3 → CAN'T REACH! return False    │
  └────────────────────────────────────────────────────────┘
  
  OUTPUT: False (index 4 is unreachable, stuck at index 3)
```

```python
def can_jump(nums):
    """Check if you can reach the last index."""
    max_reach = 0
    
    for i, jump in enumerate(nums):
        # If current position is unreachable
        if i > max_reach:
            return False
        
        # Update maximum reachable position
        max_reach = max(max_reach, i + jump)
    
    return True

# Example
nums = [2, 3, 1, 1, 4]
print(can_jump(nums))  # True

nums = [3, 2, 1, 0, 4]
print(can_jump(nums))  # False
```

**Time Complexity**: O(n)  
**Space Complexity**: O(1)

---

### 5. Jump Game II

**Problem**: Find minimum number of jumps to reach the last index.

### Visual Walkthrough

```
  INPUT: nums = [2, 3, 1, 1, 4]
  
  INDEX:  0   1   2   3   4
  VALUE:  2   3   1   1   4
  
  BFS-LIKE GREEDY APPROACH:
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  Jump 0 (starting zone): indices [0, 0]                 │
  │    From index 0 (value=2), can reach indices 1-2         │
  │    farthest = max(0, 0+2) = 2                           │
  │                                                          │
  │  Jump 1 (zone): indices [1, 2]                           │
  │    From index 1 (value=3), can reach up to index 4       │
  │    From index 2 (value=1), can reach up to index 3       │
  │    farthest = max(2, 1+3, 2+1) = 4  ← REACHED END!     │
  │                                                          │
  │  jumps = 2                                               │
  └──────────────────────────────────────────────────────────┘
  
  VISUAL OF JUMPS:
  
  Jump 1          Jump 2
  ─────►          ─────►
  [0]───►[1]───►[4]  END!
    │       │
    └──►[2]─┘
  
  KEY VARIABLES:
  ┌────────────────────────────────────────────────┐
  │ current_end:  boundary of current jump zone     │
  │ farthest:     farthest reachable from current  │
  │ jumps:        number of jumps taken             │
  │                                                 │
  │ When i reaches current_end, we MUST jump:      │
  │   jumps++, current_end = farthest              │
  └────────────────────────────────────────────────┘
```

```python
def jump(nums):
    """Find minimum jumps to reach last index."""
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        # Update farthest reachable position
        farthest = max(farthest, i + nums[i])
        
        # If we've reached the end of current jump range
        if i == current_end:
            jumps += 1
            current_end = farthest
            
            # If we can already reach the end
            if current_end >= len(nums) - 1:
                break
    
    return jumps

# Example
nums = [2, 3, 1, 1, 4]
print(jump(nums))  # 2

nums = [2, 3, 0, 1, 4]
print(jump(nums))  # 2
```

**Time Complexity**: O(n)  
**Space Complexity**: O(1)

---

### 6. Gas Station

**Problem**: Find starting gas station to complete a circular tour.

### Visual Walkthrough

```
  INPUT: gas = [1, 2, 3, 4, 5], cost = [3, 4, 5, 1, 2]
  
  CIRCULAR TOUR:
  
             Station 0 (gas=1, cost=3)
            ╱                    ╲
     Station 4                 Station 1
     (gas=5, cost=2)        (gas=2, cost=4)
            ╲                    ╱
             Station 3       Station 2
             (gas=4, cost=1)  (gas=3, cost=5)
  
  NET GAIN AT EACH STATION:
  Station:  0    1    2    3    4
  gas:      1    2    3    4    5
  cost:     3    4    5    1    2
  net:     -2   -2   -2    3    3
  
  GREEDY SCAN:
  ┌────────────────────────────────────────────────────────┐
  │ i=0: current_tank = -2, total_tank = -2               │
  │   current_tank < 0 → restart from station 1           │
  │                                                        │
  │ i=1: current_tank = -2, total_tank = -4               │
  │   current_tank < 0 → restart from station 2           │
  │                                                        │
  │ i=2: current_tank = -2, total_tank = -6               │
  │   current_tank < 0 → restart from station 3           │
  │                                                        │
  │ i=3: current_tank = 3, total_tank = -3                │
  │                                                        │
  │ i=4: current_tank = 6, total_tank = 0                 │
  │   total_tank >= 0 → solution exists!                  │
  └────────────────────────────────────────────────────────┘
  
  Verify starting at station 3:
  Station 3: arrive with 0, +4 gas, -1 cost → 3 remaining
  Station 4: arrive with 3, +5 gas, -2 cost → 6 remaining
  Station 0: arrive with 6, +1 gas, -3 cost → 4 remaining
  Station 1: arrive with 4, +2 gas, -4 cost → 2 remaining
  Station 2: arrive with 2, +3 gas, -5 cost → 0 remaining  ✓
  
  OUTPUT: Start at station 3
  
  KEY INSIGHT: If total gas >= total cost, a solution
  ALWAYS exists. The greedy scan finds the valid start.
```

```python
def can_complete_circuit(gas, cost):
    """Find starting gas station for circular tour."""
    total_tank = 0
    current_tank = 0
    start = 0
    
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_tank += diff
        current_tank += diff
        
        # If current tank negative, restart from next station
        if current_tank < 0:
            start = i + 1
            current_tank = 0
    
    # If total gas >= total cost, solution exists
    return start if total_tank >= 0 else -1

# Example
gas = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
print(can_complete_circuit(gas, cost))  # 3

gas = [2, 3, 4]
cost = [3, 4, 3]
print(can_complete_circuit(gas, cost))  # -1
```

**Time Complexity**: O(n)  
**Space Complexity**: O(1)

---

### 7. Task Scheduler

**Problem**: Find minimum intervals to complete all tasks with cooldown period.

### Visual Walkthrough

```
  INPUT: tasks = ["A", "A", "A", "B", "B", "B"], n = 2
  
  Task frequencies: A=3, B=3
  
  SCHEDULING WITH COOLDOWN n=2:
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  Interval:  1    2    3    4    5    6    7    8        │
  │            ───  ───  ───  ───  ───  ───  ───  ───      │
  │            A    B    idle idle A    B    idle A    B     │
  │                                                          │
  │  Time 1: Execute A (most frequent, freq=3)               │
  │    A enters cooldown until time 1+2+1 = time 4           │
  │                                                          │
  │  Time 2: Execute B (most frequent, freq=3)               │
  │    B enters cooldown until time 2+2+1 = time 5           │
  │                                                          │
  │  Time 3: Both A and B in cooldown → idle                 │
  │                                                          │
  │  Time 4: A ready (cooldown expired) → Execute A          │
  │                                                          │
  │  Time 5: B ready (cooldown expired) → Execute B          │
  │                                                          │
  │  Time 6: Both in cooldown → idle                         │
  │                                                          │
  │  Time 7: A ready → Execute A (last A)                    │
  │                                                          │
  │  Time 8: B ready → Execute B (last B)                    │
  └──────────────────────────────────────────────────────────┘
  
  RESULT: 8 intervals
  
  FORMULA (when enough tasks to fill gaps):
  ┌──────────────────────────────────────────────────────┐
  │  max_freq = 3 (count of most frequent task)          │
  │  num_max = 2 (number of tasks with max freq)         │
  │  result = (max_freq - 1) × (n + 1) + num_max        │
  │         = (3-1) × (2+1) + 2 = 2×3 + 2 = 8          │
  └──────────────────────────────────────────────────────┘
```

```python
import heapq
from collections import Counter

def least_interval(tasks, n):
    """Find minimum intervals for task scheduling."""
    if n == 0:
        return len(tasks)
    
    # Count task frequencies
    count = Counter(tasks)
    
    # Max-heap of frequencies
    max_heap = [-freq for freq in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    cooldown_queue = []  # (remaining_count, available_time)
    
    while max_heap or cooldown_queue:
        time += 1
        
        if max_heap:
            # Execute most frequent task
            freq = heapq.heappop(max_heap)
            if freq + 1 < 0:  # Still has remaining
                cooldown_queue.append((freq + 1, time + n))
        
        # Check if any task is ready from cooldown
        if cooldown_queue and cooldown_queue[0][1] <= time:
            freq, _ = cooldown_queue.pop(0)
            heapq.heappush(max_heap, freq)
    
    return time

# Example
tasks = ["A", "A", "A", "B", "B", "B"]
n = 2
print(least_interval(tasks, n))  # 8
```

**Time Complexity**: O(n log k) where k is unique tasks  
**Space Complexity**: O(k)

---

### 8. Queue Reconstruction by Height

**Problem**: Reconstruct queue where people[i] = [hi, ki] (height, people in front).

### Visual Walkthrough

```
  INPUT: [[7,0], [4,4], [7,1], [5,0], [6,1], [5,2]]
  
  people[i] = [height, people_in_front]
  
  STEP 1: Sort by height DESCENDING, then by k ASCENDING:
  ┌──────────┬──────────┬─────────────┐
  │ Original │ Sorted   │ Explanation │
  ├──────────┼──────────┼─────────────┤
  │ [7,0]    │ [7,0]    │ tallest     │
  │ [7,1]    │ [7,1]    │ tallest     │
  │ [6,1]    │ [6,1]    │ 2nd tallest │
  │ [5,0]    │ [5,0]    │ 3rd tallest │
  │ [5,2]    │ [5,2]    │ 3rd tallest │
  │ [4,4]    │ [4,4]    │ shortest    │
  └──────────┴──────────┴─────────────┘
  
  STEP 2: Insert each person at index k in result:
  ┌───────────────────────────────────────────────────────┐
  │ Insert [7,0] at index 0:                              │
  │   result: [ [7,0] ]                                   │
  │                                                       │
  │ Insert [7,1] at index 1:                              │
  │   result: [ [7,0], [7,1] ]                            │
  │                                                       │
  │ Insert [6,1] at index 1:                              │
  │   result: [ [7,0], [6,1], [7,1] ]                    │
  │                                                       │
  │ Insert [5,0] at index 0:                              │
  │   result: [ [5,0], [7,0], [6,1], [7,1] ]             │
  │                                                       │
  │ Insert [5,2] at index 2:                              │
  │   result: [ [5,0], [7,0], [5,2], [6,1], [7,1] ]     │
  │                                                       │
  │ Insert [4,4] at index 4:                              │
  │   result: [ [5,0], [7,0], [5,2], [6,1], [4,4], [7,1] ]│
  └───────────────────────────────────────────────────────┘
  
  VERIFY:
  [5,0]: 0 people taller/aqual in front → ✓ (none before)
  [7,0]: 0 people taller/aqual in front → ✓ (5 is shorter)
  [5,2]: 2 people taller/aqual in front → ✓ (7,7)
  [6,1]: 1 person taller/aqual in front → ✓ (7)
  [4,4]: 4 people taller/aqual in front → ✓ (7,7,6,5)
  [7,1]: 1 person taller/aqual in front → ✓ (7)
  
  KEY INSIGHT: Insert tallest people first. They don't
  affect shorter people's counts, so insert in height order.
```

```python
def reconstruct_queue(people):
    """Reconstruct queue based on height and count."""
    # Sort by height descending, then by k ascending
    people.sort(key=lambda x: (-x[0], x[1]))
    
    result = []
    for height, k in people:
        result.insert(k, [height, k])
    
    return result

# Example
people = [[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]]
print(reconstruct_queue(people))
# Output: [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]
```

**Time Complexity**: O(n²)  
**Space Complexity**: O(n)

---

### 9. Hand of Straights

**Problem**: Determine if you can rearrange cards into groups of `groupSize`.

```python
import heapq
from collections import Counter

def is_straight_hand(hand, group_size):
    """Check if hand can be rearranged into straights."""
    if len(hand) % group_size != 0:
        return False
    
    count = Counter(hand)
    min_heap = list(count.keys())
    heapq.heapify(min_heap)
    
    while min_heap:
        # Start a new group with the smallest card
        start = min_heap[0]
        
        # Check if we can form a group starting from 'start'
        for i in range(group_size):
            card = start + i
            
            if card not in count or count[card] == 0:
                return False
            
            count[card] -= 1
            if count[card] == 0:
                # Remove from heap (lazy deletion)
                while min_heap and count[min_heap[0]] == 0:
                    heapq.heappop(min_heap)
    
    return True

# Example
hand = [1, 2, 3, 6, 2, 3, 4, 7, 8]
group_size = 3
print(is_straight_hand(hand, group_size))  # True

hand = [1, 2, 3, 4, 5]
group_size = 4
print(is_straight_hand(hand, group_size))  # False
```

**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

---

## Hard Problems

### 10. Candy

**Problem**: Distribute candies to children with ratings. Each child gets at least 1 candy, children with higher ratings get more candies than neighbors.

### Visual Walkthrough

```
  INPUT: ratings = [1, 0, 2]
  
  TWO-PASS APPROACH:
  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  LEFT-TO-RIGHT PASS (ensure right neighbor rule):      │
  │  ratings:  1    0    2                                 │
  │  candies:  1    1    1   (start with all 1s)          │
  │                                                        │
  │  i=1: rating[1]=0 < rating[0]=1 → no bump needed      │
  │  i=2: rating[2]=2 > rating[1]=0 → candies[2] = 2      │
  │                                                        │
  │  After L→R: [1, 1, 2]                                 │
  │                                                        │
  │  RIGHT-TO-LEFT PASS (ensure left neighbor rule):       │
  │  i=0: rating[0]=1 > rating[1]=0 → candies[0] = max(1, 2) = 2  │
  │  i=1: rating[1]=0 < rating[2]=2 → no bump needed      │
  │                                                        │
  │  After R→L: [2, 1, 2]                                 │
  └────────────────────────────────────────────────────────┘
  
  RESULT: 2 + 1 + 2 = 5 candies
  
  VISUAL:
  ratings:  1    0    2
            ▲         ▲
           2 🍬     2 🍬
              ▲
             1 🍬
  
  WHY TWO PASSES?
  ┌────────────────────────────────────────────────────────┐
  │ One pass handles each direction's constraint:          │
  │                                                        │
  │ L→R pass: If rating[i] > rating[i-1],                 │
  │           candies[i] = candies[i-1] + 1                │
  │           (ensures ascending sequences)                │
  │                                                        │
  │ R→L pass: If rating[i] > rating[i+1],                 │
  │           candies[i] = max(candies[i], candies[i+1]+1) │
  │           (ensures descending sequences)               │
  └────────────────────────────────────────────────────────┘
```

```python
def candy(ratings):
    """Distribute candies based on ratings."""
    n = len(ratings)
    
    if n == 0:
        return 0
    
    candies = [1] * n
    
    # Left to right pass
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    
    # Right to left pass
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    
    return sum(candies)

# Example
ratings = [1, 0, 2]
print(candy(ratings))  # 5

ratings = [1, 2, 2]
print(candy(ratings))  # 4
```

**Time Complexity**: O(n)  
**Space Complexity**: O(n)

---

### 11. IPO

**Problem**: Find maximum capital after completing at most k projects.

### Visual Walkthrough

```
  INPUT: k=2, w=0, profits=[1,2,3], capital=[0,1,1]
  
  PROJECTS:
  ┌──────────┬───────────┬─────────┐
  │ Project  │  Capital  │ Profit  │
  ├──────────┼───────────┼─────────┤
  │    1     │     0     │    1    │
  │    2     │     1     │    2    │
  │    3     │     1     │    3    │
  └──────────┴───────────┴─────────┘
  
  GREEDY APPROACH:
  ┌──────────────────────────────────────────────────────────┐
  │                                                          │
  │  Round 1 (k=2 remaining):                                │
  │    Current capital: 0                                     │
  │    Affordable projects: [1] (capital 0 <= 0)              │
  │    Pick most profitable: Project 1 (profit=1)            │
  │    New capital: 0 + 1 = 1                                │
  │                                                          │
  │  Round 2 (k=1 remaining):                                │
  │    Current capital: 1                                     │
  │    Affordable projects: [2, 3] (capital 1 <= 1)          │
  │    Pick most profitable: Project 3 (profit=3)            │
  │    New capital: 1 + 3 = 4                                │
  │                                                          │
  │  RESULT: Maximum capital = 4                             │
  └──────────────────────────────────────────────────────────┘
  
  ALGORITHM:
  1. Sort projects by capital requirement
  2. Use max-heap for profits of affordable projects
  3. Each round: add all affordable projects to heap,
     pop the most profitable one
  
  KEY INSIGHT: Always pick the most profitable project
  you can currently afford. This maximizes capital growth.
```

```python
import heapq

def find_maximized_capital(k, w, profits, capital):
    """Find maximized capital after k projects."""
    # Pair projects by capital requirement
    projects = sorted(zip(capital, profits))
    
    # Max-heap for available profits
    max_heap = []
    project_idx = 0
    current_capital = w
    
    for _ in range(k):
        # Add all affordable projects to max-heap
        while project_idx < len(projects) and projects[project_idx][0] <= current_capital:
            heapq.heappush(max_heap, -projects[project_idx][1])
            project_idx += 1
        
        # If no project available, break
        if not max_heap:
            break
        
        # Take the most profitable project
        current_capital += -heapq.heappop(max_heap)
    
    return current_capital

# Example
k = 2
w = 0
profits = [1, 2, 3]
capital = [0, 1, 1]
print(find_maximized_capital(k, w, profits, capital))  # 4
```

**Time Complexity**: O(n log n + k log n)  
**Space Complexity**: O(n)

---

### 12. Minimum Cost to Hire K Workers

**Problem**: Find minimum cost to hire exactly k workers.

```python
import heapq

def mincost_to_hire_workers(quality, wage, k):
    """Find minimum cost to hire k workers."""
    n = len(quality)
    
    # Calculate wage-to-quality ratio
    workers = sorted([(wage[i] / quality[i], quality[i]) for i in range(n)])
    
    min_cost = float('inf')
    quality_sum = 0
    max_heap = []
    
    for ratio, q in workers:
        # Add current worker
        quality_sum += q
        heapq.heappush(max_heap, -q)
        
        # If we have k workers, try to remove the one with highest quality
        if len(max_heap) > k:
            quality_sum += heapq.heappop(max_heap)  # Remove highest quality
        
        # If we have exactly k workers, calculate cost
        if len(max_heap) == k:
            min_cost = min(min_cost, quality_sum * ratio)
    
    return min_cost

# Example
quality = [10, 20, 5]
wage = [70, 50, 30]
k = 2
print(mincost_to_hire_workers(quality, wage, k))  # 105.0
```

**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

---

### 13. Car Pooling

**Problem**: Determine if a car can pick up and drop off all passengers without exceeding capacity.

### Visual Walkthrough

```
  INPUT: trips = [[2, 1, 5], [3, 3, 7]], capacity = 5
  
  TRIPS:
  Trip 1: 2 passengers, from location 1 to 5
  Trip 2: 3 passengers, from location 3 to 7
  
  LINE SWEEP:
  ┌──────────────────────────────────────────────────────┐
  │ Events:                                               │
  │   (1, +2)  - Pick up 2 passengers at location 1      │
  │   (3, +3)  - Pick up 3 passengers at location 3      │
  │   (5, -2)  - Drop off 2 passengers at location 5     │
  │   (7, -3)  - Drop off 3 passengers at location 7     │
  │                                                       │
  │ Location: 1    2    3    4    5    6    7             │
  │ Passengers: 2    2    5    5    3    3    0           │
  │            ▲         ▲         ▲                     │
  │         +2 at 1   +3 at 3   -2 at 5                  │
  │                                                       │
  │ Max passengers in car: 5 (at locations 3-4)           │
  │ Capacity: 5 → 5 <= 5 ✓                               │
  └──────────────────────────────────────────────────────┘
  
  OUTPUT: True
  
  WITH capacity=4:
  Max passengers = 5 > 4 → False!
```

```python
def car_pooling(trips, capacity):
    """Check if car pooling is possible."""
    events = []
    
    for passengers, start, end in trips:
        events.append((start, passengers))   # Pick up
        events.append((end, -passengers))    # Drop off
    
    # Sort by location, then drop-offs before pick-ups
    events.sort(key=lambda x: (x[0], x[1]))
    
    current_passengers = 0
    
    for location, change in events:
        current_passengers += change
        
        if current_passengers > capacity:
            return False
    
    return True

# Example
trips = [[2, 1, 5], [3, 3, 7]]
capacity = 4
print(car_pooling(trips, capacity))  # False

trips = [[2, 1, 5], [3, 3, 7]]
capacity = 5
print(car_pooling(trips, capacity))  # True
```

**Time Complexity**: O(n log n)  
**Space Complexity**: O(n)

---

### 14. Valid Triangle Number

**Problem**: Count number of triplets that can form a triangle.

```python
def triangle_number(nums):
    """Count valid triangle triplets."""
    nums.sort()
    count = 0
    
    for k in range(2, len(nums)):
        left, right = 0, k - 1
        
        while left < right:
            if nums[left] + nums[right] > nums[k]:
                # All elements from left to right-1 can form triangle with k
                count += right - left
                right -= 1
            else:
                left += 1
    
    return count

# Example
nums = [2, 2, 3, 4]
print(triangle_number(nums))  # 3

nums = [4, 2, 3, 4]
print(triangle_number(nums))  # 4
```

**Time Complexity**: O(n²)  
**Space Complexity**: O(1)

---

## Summary Table

| Problem | Difficulty | Time | Space | Key Technique |
|---------|------------|------|-------|---------------|
| Maximum Units | Easy | O(n log n) | O(1) | Sort by units |
| Maximum Product | Easy | O(n log n) | O(1) | Sort |
| Best Time Buy Sell | Easy | O(n) | O(1) | Track minimum |
| Jump Game | Medium | O(n) | O(1) | Greedy reach |
| Jump Game II | Medium | O(n) | O(1) | BFS-like |
| Gas Station | Medium | O(n) | O(1) | Track balance |
| Task Scheduler | Medium | O(n log k) | O(k) | Max-heap |
| Queue Reconstruction | Medium | O(n²) | O(n) | Sort + insert |
| Hand of Straights | Medium | O(n log n) | O(n) | Min-heap |
| Candy | Hard | O(n) | O(n) | Two passes |
| IPO | Hard | O(n log n) | O(n) | Max-heap |
| Min Cost K Workers | Hard | O(n log n) | O(n) | Sort by ratio |
| Car Pooling | Hard | O(n log n) | O(n) | Line sweep |
| Valid Triangle | Hard | O(n²) | O(1) | Two pointers |

---

## Tips for Greedy Problems

1. **Identify the greedy choice** - what locally optimal decision leads to global optimum?
2. **Prove correctness** - why does greedy work here?
3. **Sort by appropriate criterion** - finish time, profit, ratio, etc.
4. **Use heap when needed** - for maintaining top-k or priority
5. **Consider edge cases** - empty input, single element, all same values
6. **Check if greedy fails** - some problems need DP instead

### Problem-Solving Checklist

```
  ┌──────────────────────────────────────────────────────────────┐
  │              GREEDY PROBLEM SOLVING CHECKLIST                 │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │  □ 1. Can I make a locally optimal choice at each step?      │
  │        → If no, consider DP or backtracking                  │
  │                                                              │
  │  □ 2. Does the greedy choice property hold?                  │
  │        → Can I prove swapping doesn't improve the solution?  │
  │                                                              │
  │  □ 3. What should I sort by?                                 │
  │        → Finish time? Profit? Ratio? Height?                 │
  │                                                              │
  │  □ 4. Do I need a heap?                                      │
  │        → Need top-k? Min/max tracking? Priority scheduling?  │
  │                                                              │
  │  □ 5. Is this a line sweep problem?                          │
  │        → Concurrent events? Start/end at same point?         │
  │                                                              │
  │  □ 6. Edge cases?                                            │
  │        → Empty array? Single element? All same values?       │
  │        → Integer overflow? Negative numbers?                 │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

### Technique Selection Guide

```
  ┌──────────────────────────────────────────────────────────────┐
  │  If problem involves...          Use this technique           │
  ├──────────────────────────────────────────────────────────────┤
  │  Sorting + scanning              Simple greedy               │
  │  Tracking best/worst so far      Running min/max             │
  │  Finding max/min of top-k        Heap (min or max)           │
  │  Matching two sorted arrays      Two pointers                │
  │  Concurrent events               Line sweep / min-heap       │
  │  Decisions with future impact    BFS-like greedy (Jump II)   │
  │  Constraints on both sides       Two-pass (Candy)            │
  │  Binary decisions (include/excl) DP with binary search       │
  └──────────────────────────────────────────────────────────────┘
```

### When Greedy Fails — Use DP Instead

```
  ┌──────────────────────────────────────────────────────────────┐
  │  PROBLEM                      WHY GREEDY FAILS               │
  ├──────────────────────────────────────────────────────────────┤
  │  0/1 Knapsack                 High-ratio item wastes space   │
  │  Coin Change (non-canonical)  Greedy uses more coins         │
  │  Weighted Job Scheduling      Can't just pick highest profit │
  │  Longest Common Subsequence   Need to explore all options    │
  │  Edit Distance                Choices affect future cost     │
  └──────────────────────────────────────────────────────────────┘
```
