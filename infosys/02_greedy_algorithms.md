# Greedy Algorithms

## Problem 1: Maximum Monsters Defeated
**Difficulty: Medium-Hard | Marks: 30-50**

Asked in Infosys SP/DSE exam - RPG game with monsters requiring minimum power.

```python
def max_monsters_defeated(n, exp, power, bonus):
    monsters = sorted(zip(power, bonus))
    count = 0
    for p, b in monsters:
        if exp < p:
            break
        exp += b
        count += 1
    return count

n = 3
exp = 100
power = [101, 100, 304]
bonus = [100, 1, 524]
print(max_monsters_defeated(n, exp, power, bonus))
```

---

## Problem 2: Activity Selection
**Difficulty: Easy-Medium | Marks: 20-30**

```python
def activity_selection(start, finish):
    n = len(start)
    activities = sorted(zip(start, finish), key=lambda x: x[1])
    selected = [activities[0]]
    last_finish = activities[0][1]
    for i in range(1, n):
        if activities[i][0] >= last_finish:
            selected.append(activities[i])
            last_finish = activities[i][1]
    return len(selected), selected

start = [1, 3, 0, 5, 8, 5]
finish = [2, 4, 6, 7, 9, 9]
print(activity_selection(start, finish))
```

---

## Problem 3: Coin Change - Minimum Coins (Greedy)
**Difficulty: Easy-Medium | Marks: 20-30**

Note: Greedy works for canonical coin systems (Indian/US currency).

```python
def min_coins_greedy(coins, amount):
    coins.sort(reverse=True)
    count = 0
    for coin in coins:
        if amount == 0:
            break
        count += amount // coin
        amount %= coin
    return count if amount == 0 else -1

coins = [1, 2, 5, 10, 20, 50, 100, 200, 500, 2000]
amount = 786
print(min_coins_greedy(coins, amount))
```

---

## Problem 4: Fractional Knapsack
**Difficulty: Easy-Medium | Marks: 20-30**

```python
def fractional_knapsack(weights, values, capacity):
    items = [(v / w, w, v) for w, v in zip(weights, values)]
    items.sort(reverse=True, key=lambda x: x[0])
    total_value = 0
    for ratio, weight, value in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            total_value += ratio * capacity
            break
    return total_value

weights = [10, 20, 30]
values = [60, 100, 120]
capacity = 50
print(fractional_knapsack(weights, values, capacity))
```

---

## Problem 5: Job Sequencing with Deadlines
**Difficulty: Medium | Marks: 30**

```python
def job_sequencing(jobs):
    # jobs: list of (profit, deadline)
    jobs.sort(reverse=True, key=lambda x: x[0])
    max_deadline = max(job[1] for job in jobs)
    slots = [-1] * (max_deadline + 1)
    total_profit = 0
    for profit, deadline in jobs:
        for j in range(deadline, 0, -1):
            if slots[j] == -1:
                slots[j] = profit
                total_profit += profit
                break
    return total_profit, [p for p in slots if p != -1]

jobs = [(100, 2), (19, 1), (27, 2), (25, 1), (15, 3)]
print(job_sequencing(jobs))
```

---

## Problem 6: Huffman Encoding
**Difficulty: Medium | Marks: 30**

```python
import heapq

def huffman_encoding(chars, freq):
    heap = [[f, [c, ""]] for c, f in zip(chars, freq)]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heap[0][1:], key=lambda p: len(p[1]))

chars = ['a', 'b', 'c', 'd', 'e', 'f']
freq = [5, 9, 12, 13, 16, 45]
print(huffman_encoding(chars, freq))
```

---

## Problem 7: Minimum Platforms Required
**Difficulty: Medium | Marks: 30**

```python
def min_platforms(arrival, departure):
    arrival.sort()
    departure.sort()
    n = len(arrival)
    i = j = 0
    platforms = max_platforms = 0
    while i < n and j < n:
        if arrival[i] <= departure[j]:
            platforms += 1
            i += 1
            max_platforms = max(max_platforms, platforms)
        else:
            platforms -= 1
            j += 1
    return max_platforms

arrival = [900, 940, 950, 1100, 1500, 1800]
departure = [910, 1200, 1120, 1130, 1900, 2000]
print(min_platforms(arrival, departure))
```

---

## Problem 8: Minimum Number of Arrows to Burst Balloons
**Difficulty: Medium | Marks: 30**

```python
def find_min_arrow_shots(points):
    if not points:
        return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    for start, finish in points[1:]:
        if start > end:
            arrows += 1
            end = finish
    return arrows

points = [[10, 16], [2, 8], [1, 6], [7, 12]]
print(find_min_arrow_shots(points))
```

---

## Problem 9: Maximum Length of Pair Chain
**Difficulty: Medium | Marks: 30**

```python
def find_longest_chain(pairs):
    pairs.sort(key=lambda x: x[1])
    curr_end = float('-inf')
    count = 0
    for start, end in pairs:
        if start > curr_end:
            count += 1
            curr_end = end
    return count

pairs = [[1, 2], [2, 3], [3, 4]]
print(find_longest_chain(pairs))
```

---

## Problem 10: Candy Distribution
**Difficulty: Hard | Marks: 50**

```python
def candy(ratings):
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)

ratings = [1, 0, 2]
print(candy(ratings))
```

---

## Problem 11: Gas Station
**Difficulty: Medium | Marks: 30**

```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    total = start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < 0:
            total = 0
            start = i + 1
    return start

gas = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]
print(can_complete_circuit(gas, cost))
```

---

## Problem 12: Maximum Swap
**Difficulty: Medium | Marks: 30**

```python
def maximum_swap(num):
    arr = list(str(num))
    n = len(arr)
    last = {int(d): i for i, d in enumerate(arr)}
    for i in range(n):
        for d in range(9, int(arr[i]), -1):
            if last.get(d, -1) > i:
                arr[i], arr[last[d]] = arr[last[d]], arr[i]
                return int(''.join(arr))
    return num

print(maximum_swap(2736))
print(maximum_swap(9973))
```

---

## Problem 13: Remove K Digits
**Difficulty: Medium | Marks: 30**

```python
def remove_k_digits(num, k):
    stack = []
    for digit in num:
        while k and stack and stack[-1] > digit:
            stack.pop()
            k -= 1
        stack.append(digit)
    while k:
        stack.pop()
        k -= 1
    return ''.join(stack).lstrip('0') or '0'

print(remove_k_digits("1432219", 3))
print(remove_k_digits("10200", 1))
```

---

## Problem 14: Jump Game II
**Difficulty: Medium | Marks: 30**

```python
def jump(nums):
    n = len(nums)
    if n == 1:
        return 0
    jumps = curr_end = curr_farthest = 0
    for i in range(n - 1):
        curr_farthest = max(curr_farthest, i + nums[i])
        if i == curr_end:
            jumps += 1
            curr_end = curr_farthest
    return jumps

nums = [2, 3, 1, 1, 4]
print(jump(nums))
```

---

## Problem 15: Partition Labels
**Difficulty: Medium | Marks: 30**

```python
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    result = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            result.append(end - start + 1)
            start = i + 1
    return result

s = "ababcbacadefegdehijhklij"
print(partition_labels(s))
```
