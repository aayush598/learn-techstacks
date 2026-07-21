# Greedy Practice Problems - Complete Guide

## Easy Problems

### 1. Maximum Units on a Truck

**Problem**: You have `n` boxes, each with `boxTypes[i] = [numberOfBoxesi, numberOfUnitsPerBox]`. Return maximum units that can be put on a truck with capacity `boxCapacity`.

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
