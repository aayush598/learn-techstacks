# Advanced Binary Search - Complete Guide

## Table of Contents
1. [Binary Search on Floating Point](#1-binary-search-on-floating-point)
2. [Binary Search on Predicate Function](#2-binary-search-on-predicate-function)
3. [Find Peak Element](#3-find-peak-element)
4. [Capacity to Ship Packages](#4-capacity-to-ship-packages-within-d-days)
5. [Split Array Largest Sum](#5-split-array-largest-sum)
6. [Magnetic Between Balls](#6-magnetic-between-balls)
7. [Aggressive Cows / Painter's Partition](#7-aggressive-cows--painters-partition)
8. [Koko Eating Bananas](#8-koko-eating-bananas)

---

## The "Binary Search on Answer" Framework

Before diving into individual problems, understand the MASTER PATTERN:

```
BINARY SEARCH ON ANSWER - THE UNIVERSAL TEMPLATE
═══════════════════════════════════════════════════

Step 1: Identify the SEARCH SPACE
         What range of answers is possible?
         (min_possible ... max_possible)

Step 2: Define the PREDICATE (is_valid / can_do)
         Given a candidate answer "mid", can we check
         if it's feasible? This is a YES/NO question.

Step 3: Observe the PATTERN
         As the candidate answer increases:
         ┌──────────────────────────────────────┐
         │  FALSE FALSE FALSE ... TRUE TRUE TRUE │
         │  ──────────────┼───────────────────── │
         │           the "boundary" we seek      │
         └──────────────────────────────────────┘

         We binary search for the TRANSITION POINT.

Step 4: Choose the right template:
         - Minimize the maximum → find leftmost TRUE
         - Maximize the minimum → find rightmost TRUE
```

---

## 1. Binary Search on Floating Point

Instead of searching integers, we search REAL NUMBERS until we reach
the desired precision.

```
FINDING sqrt(2) WITH PRECISION 0.1:

Search space: [0.0, 2.0]

Step 1: L=0.0, R=2.0, M=1.0
        1.0*1.0 = 1.0 <= 2.0 -> L=1.0

Step 2: L=1.0, R=2.0, M=1.5
        1.5*1.5 = 2.25 > 2.0 -> R=1.5

Step 3: L=1.0, R=1.5, M=1.25
        1.25*1.25 = 1.5625 <= 2.0 -> L=1.25

Step 4: L=1.25, R=1.5, M=1.375
        1.375*1.375 = 1.89 <= 2.0 -> L=1.375

Step 5: L=1.375, R=1.5, M=1.4375
        1.4375*1.4375 = 2.066 > 2.0 -> R=1.4375

R - L = 1.4375 - 1.375 = 0.0625 > 0.1? NO -> STOP

Answer: L = 1.375 (actual sqrt(2) = 1.414...)

With smaller precision (1e-9), we get much more accurate results.
```

```python
def sqrt_precision(x, precision=1e-9):
    """Find square root with given precision."""
    if x < 0:
        raise ValueError("Cannot compute sqrt of negative number")
    if x == 0:
        return 0.0

    left, right = 0.0, max(1.0, x)

    # Continue until the search space is smaller than precision
    while right - left > precision:
        mid = (left + right) / 2

        if mid * mid <= x:
            left = mid       # Answer is mid or larger
        else:
            right = mid      # Answer is smaller than mid

    return left  # Left is the approximate answer

# Example
print(f"sqrt(2) = {sqrt_precision(2):.10f}")  # 1.4142135624
print(f"sqrt(10) = {sqrt_precision(10):.10f}")  # 3.1622776602
```

### Find Nth Root

```python
def nth_root(n, x, precision=1e-9):
    """Find nth root of x with given precision."""
    if x == 0:
        return 0.0
    if x < 0 and n % 2 == 0:
        raise ValueError("Even root of negative number")
    
    left, right = 0.0, max(1.0, abs(x))
    if x < 0:
        left, right = -abs(x), 0.0
    
    while right - left > precision:
        mid = (left + right) / 2
        
        if mid ** n <= abs(x):
            left = mid
        else:
            right = mid
    
    result = left
    return -result if x < 0 else result

# Example
print(f"Cube root of 27 = {nth_root(3, 27):.6f}")  # 3.0
print(f"4th root of 16 = {nth_root(4, 16):.6f}")  # 2.0
```

---

## 2. Binary Search on Predicate Function

### General Template

```python
def binary_search_predicate(predicate, left, right):
    """
    Find the leftmost index where predicate becomes True.
    Assumes predicate goes from False to True as index increases.
    """
    while left < right:
        mid = left + (right - left) // 2
        
        if predicate(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example: Find first number >= target in sorted array
def first_geq(arr, target):
    """Find first element >= target."""
    def predicate(i):
        return arr[i] >= target
    
    return binary_search_predicate(predicate, 0, len(arr) - 1)

arr = [1, 3, 5, 7, 9, 11]
print(first_geq(arr, 6))  # 3 (index of 7)
```

### Find First True in Boolean Array

```python
def first_true(arr):
    """Find first True in sorted boolean array (False...False, True...True)."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        mid = left + (right - left) // 2
        
        if arr[mid]:
            right = mid
        else:
            left = mid + 1
    
    return left if arr[left] else -1

# Example
arr = [False, False, False, True, True, True]
print(first_true(arr))  # 3
```

---

## 3. Find Peak Element

**Problem**: Find a peak element where arr[i] > arr[i-1] and arr[i] > arr[i+1].

```
VISUAL - What is a Peak?

arr = [1, 2, 1, 3, 5, 6, 4]

Value
  6 |           *         <- Peak (index 5)
  5 |         *
  4 |                   *
  3 |       *
  2 |     *
  1 |   *       *
    └────────────────────
      0  1  2  3  4  5  6

Peaks are at index 1 (value=2) and index 5 (value=6).
The problem asks for ANY one peak.

KEY INSIGHT: If arr[mid] < arr[mid+1], we are on an
UPHILL slope, so a peak MUST exist to the RIGHT.
If arr[mid] > arr[mid+1], we are on a DOWNHILL slope,
so a peak MUST exist at mid or to the LEFT.
```

### Walkthrough

```
arr = [1, 2, 1, 3, 5, 6, 4]

Step 1: L=0, R=6, M=3
        arr[M]=3 < arr[M+1]=5 -> UPHILL, peak is RIGHT
        L=4

Step 2: L=4, R=6, M=5
        arr[M]=6 > arr[M+1]=4 -> DOWNHILL, peak is at M or LEFT
        R=5

Step 3: L=4, R=5, M=4
        arr[M]=5 < arr[M+1]=6 -> UPHILL, peak is RIGHT
        L=5

L == R -> return index 5 (value=6) ✓
```

### Find All Peaks

```python
def find_all_peaks(arr):
    """Find all peak elements."""
    peaks = []
    
    if len(arr) == 1:
        return [0]
    
    for i in range(len(arr)):
        is_peak = True
        
        if i > 0 and arr[i] <= arr[i - 1]:
            is_peak = False
        if i < len(arr) - 1 and arr[i] <= arr[i + 1]:
            is_peak = False
        
        if is_peak:
            peaks.append(i)
    
    return peaks

# Example
arr = [1, 3, 2, 4, 1]
print(find_all_peaks(arr))  # [1, 3] (indices of 3 and 4)
```

---

## 4. Capacity to Ship Packages Within D Days

**Problem**: Find minimum capacity to ship all packages within D days.

```
PROBLEM VISUALIZATION:
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]    days = 5

Packages must be shipped IN ORDER (contiguous groups).
We want to find the MINIMUM ship capacity.

If capacity = 15:
  Day 1: [1, 2, 3, 4, 5] = 15 <= 15 ✓
  Day 2: [6, 7] = 13 <= 15 ✓
  Day 3: [8] = 8 <= 15 ✓
  Day 4: [9] = 9 <= 15 ✓
  Day 5: [10] = 10 <= 15 ✓
  All shipped in 5 days! ✓

If capacity = 14:
  Day 1: [1, 2, 3, 4] = 10 <= 14 ✓
  Day 2: [5, 6] = 11 <= 14 ✓
  Day 3: [7] = 7 <= 14 ✓
  Day 4: [8] = 8 <= 14 ✓
  Day 5: [9] = 9 <= 14 ✓
  Day 6: [10] = 10 <= 14 ✓
  Needs 6 days > 5! ✗
```

```python
def ship_within_days(weights, days):
    """Find minimum shipping capacity."""
    def can_ship(capacity):
        """Check if we can ship within given capacity."""
        current_load = 0
        days_needed = 1
        
        for weight in weights:
            if current_load + weight > capacity:
                days_needed += 1
                current_load = weight
                
                if days_needed > days:
                    return False
            else:
                current_load += weight
        
        return True
    
    # Search space: [max(weights), sum(weights)]
    left, right = max(weights), sum(weights)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5
print(ship_within_days(weights, days))  # 15
```

---

## 5. Split Array Largest Sum

**Problem**: Split array into m subarrays to minimize the largest sum.

```python
def split_array(nums, m):
    """Find minimum largest sum after splitting into m subarrays."""
    def can_split(max_sum):
        """Check if we can split with given max sum."""
        count = 1
        current_sum = 0
        
        for num in nums:
            if current_sum + num > max_sum:
                count += 1
                current_sum = num
                
                if count > m:
                    return False
            else:
                current_sum += num
        
        return True
    
    # Search space: [max(nums), sum(nums)]
    left, right = max(nums), sum(nums)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example
nums = [7, 2, 5, 10, 8]
m = 2
print(split_array(nums, m))  # 18
```

---

## 6. Magnetic Between Balls

**Problem**: Find maximum possible minimum distance between any two balls.

```python
def max_distance(positions, m):
    """Find maximum minimum distance between m balls."""
    positions.sort()
    
    def can_place(distance):
        """Check if we can place m balls with given min distance."""
        count = 1
        last_position = positions[0]
        
        for i in range(1, len(positions)):
            if positions[i] - last_position >= distance:
                count += 1
                last_position = positions[i]
                
                if count >= m:
                    return True
        
        return False
    
    # Search space: [1, max_distance]
    left, right = 1, positions[-1] - positions[0]
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if can_place(mid):
            left = mid + 1
        else:
            right = mid - 1
    
    return right

# Example
positions = [1, 2, 4, 8, 16]
m = 3
print(max_distance(positions, m))  # 5
```

---

## 7. Aggressive Cows / Painter's Partition

**Problem**: Place cows in stalls to maximize minimum distance between any two cows.

```
PROBLEM VISUALIZATION:
stalls = [1, 2, 4, 8, 16]     cows = 3

Position:  1     2     4           8                 16
           *     *     *           *                 *

Place 3 cows to MAXIMIZE the minimum distance between any pair.

Option A (distance=3):
  Cows at positions: 1, 4, 8
  Distances: |4-1|=3, |8-4|=4
  Minimum distance = 3

Option B (distance=5):
  Cows at positions: 1, 8, 16
  Distances: |8-1|=7, |16-8|=8
  Minimum distance = 7

Option C (distance=7):
  Cows at positions: 1, 8, 16
  Can we place 3 cows with min distance 7?
  Cow 1 at position 1
  Cow 2 at position 8 (8-1=7 >= 7) ✓
  Cow 3 at position 16 (16-8=8 >= 7) ✓
  YES! Minimum distance = 7

Answer: 7 (maximum possible minimum distance)
```

### Greedy Predicate Visualization

```
can_place(distance) - Check if we can place all cows

Algorithm (Greedy):
  1. Place first cow at first stall
  2. For each subsequent cow, place it at the first stall
     that is at least 'distance' away from the last placed cow
  3. If we can place all cows -> TRUE, else -> FALSE

stalls = [1, 2, 4, 8, 16], distance = 5

  Cow 1: placed at position 1
         |
  1     2     4           8                 16
  C1

  Cow 2: first stall >= 1+5=6? -> position 8
                    |
  1     2     4           8                 16
  C1               C2

  Cow 3: first stall >= 8+5=13? -> position 16
                                        |
  1     2     4           8                 16
  C1               C2               C3

  All 3 cows placed! -> TRUE ✓

stalls = [1, 2, 4, 8, 16], distance = 6

  Cow 1: at 1
  Cow 2: at 8 (8-1=7 >= 6) ✓
  Cow 3: need stall >= 8+6=14 -> only 16 left (16-8=8 >= 6) ✓
  All 3 cows placed! -> TRUE ✓

stalls = [1, 2, 4, 8, 16], distance = 8

  Cow 1: at 1
  Cow 2: at 8 (8-1=7 >= 8)? NO! Try 16 (16-1=15 >= 8) ✓
  Cow 3: need stall >= 16+8=24 -> none left! ✗
  Only 2 cows placed -> FALSE ✗
```

```python
def aggressive_cows(stalls, cows):
    """Find maximum minimum distance between cows."""
    stalls.sort()
    
    def can_place(min_distance):
        """Check if we can place cows with given min distance."""
        count = 1
        last_stall = stalls[0]
        
        for i in range(1, len(stalls)):
            if stalls[i] - last_stall >= min_distance:
                count += 1
                last_stall = stalls[i]
                
                if count >= cows:
                    return True
        
        return False
    
    # Search space: [1, max_distance]
    left, right = 1, stalls[-1] - stalls[0]
    result = 0
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if can_place(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Example
stalls = [1, 2, 4, 8, 16]
cows = 3
print(aggressive_cows(stalls, cows))  # 5
```

### Painter's Partition

```python
def painter_partition(boards, painters):
    """Find minimum time to paint all boards with k painters."""
    def can_paint(max_time):
        """Check if we can paint within given time."""
        count = 1
        current_time = 0
        
        for board in boards:
            if current_time + board > max_time:
                count += 1
                current_time = board
                
                if count > painters:
                    return False
            else:
                current_time += board
        
        return True
    
    # Search space: [max(boards), sum(boards)]
    left, right = max(boards), sum(boards)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_paint(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example
boards = [10, 20, 30, 40]
painters = 2
print(painter_partition(boards, painters))  # 60
```

---

## 8. Koko Eating Bananas

**Problem**: Find minimum eating speed to finish all piles within h hours.

```
PROBLEM VISUALIZATION:
piles = [3, 6, 7, 11]     h = 8 hours

Koko eats at speed k bananas/hour.
Each pile takes ceil(pile_size / k) hours.
She must finish ALL piles within h hours.

If speed = 4:
  Pile 1 (3 bananas):  ceil(3/4) = 1 hour
  Pile 2 (6 bananas):  ceil(6/4) = 2 hours
  Pile 3 (7 bananas):  ceil(7/4) = 2 hours
  Pile 4 (11 bananas): ceil(11/4) = 3 hours
  Total: 1+2+2+3 = 8 hours <= 8 ✓

If speed = 3:
  Pile 1: ceil(3/3) = 1 hour
  Pile 2: ceil(6/3) = 2 hours
  Pile 3: ceil(7/3) = 3 hours
  Pile 4: ceil(11/3) = 4 hours
  Total: 1+2+3+4 = 10 hours > 8 ✗

Answer: 4 (minimum speed that works)
```

### Speed vs Hours Graph

```
Speed:  1    2    3    4    5    6    7    8    9   10   11
Hours: 27   14   10    8    7    6    5    5    4    4    4

Hours
 27 | *
 14 |   *
 10 |     *
  8 |       *  <- threshold (h=8)
  7 |         *
  6 |           *
  5 |             *  *
  4 |                   *  *  *
    └──────────────────────────────
      1  2  3  4  5  6  7  8  9  10  11  Speed

As speed INCREASES, hours DECREASE (monotonic!)
We binary search for the minimum speed where hours <= 8.
```

```python
def min_eating_speed(piles, h):
    """Find minimum eating speed to finish within h hours."""
    def can_finish(speed):
        """Check if Koko can finish with given speed."""
        hours = 0
        
        for pile in piles:
            # Ceiling division: (pile + speed - 1) // speed
            hours += (pile + speed - 1) // speed
            
            if hours > h:
                return False
        
        return True
    
    # Search space: [1, max(piles)]
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left

# Example
piles = [3, 6, 7, 11]
h = 8
print(min_eating_speed(piles, h))  # 4

piles = [30, 11, 23, 4, 20]
h = 5
print(min_eating_speed(piles, h))  # 30
```

### Alternative: Using math.ceil

```python
import math

def min_eating_speed_v2(piles, h):
    """Alternative using math.ceil."""
    def can_finish(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h
    
    left, right = 1, max(piles)
    
    while left < right:
        mid = left + (right - left) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

---

## Quick Reference: Advanced Binary Search Patterns

| Problem | Search Space | Predicate | Time |
|---------|--------------|-----------|------|
| Floating point | Continuous | mid*mid <= x | O(log(precision)) |
| Peak element | Array indices | arr[mid] < arr[mid+1] | O(log n) |
| Ship packages | [max, sum] | can_ship(mid) | O(n log(sum)) |
| Split array | [max, sum] | can_split(mid) | O(n log(sum)) |
| Magnetic balls | [1, max_dist] | can_place(mid) | O(n log(max_dist)) |
| Aggressive cows | [1, max_dist] | can_place(mid) | O(n log(max_dist)) |
| Koko bananas | [1, max_pile] | can_finish(mid) | O(n log(max_pile)) |

---

## Common Patterns

### Pattern 1: Minimize Maximum

```python
def minimize_maximize(arr, constraint):
    """When you need to minimize the maximum value."""
    left, right = min(arr), max(arr)  # or appropriate bounds
    
    while left < right:
        mid = left + (right - left) // 2
        
        if is_valid(mid):  # Check if mid works
            right = mid    # Try smaller
        else:
            left = mid + 1  # Need larger
    
    return left
```

### Pattern 2: Maximize Minimum

```python
def maximize_minimize(arr, constraint):
    """When you need to maximize the minimum value."""
    left, right = min(arr), max(arr)  # or appropriate bounds
    
    while left < right:
        mid = left + (right - left) // 2 + 1  # +1 to avoid infinite loop
        
        if is_valid(mid):  # Check if mid works
            left = mid     # Try larger
        else:
            right = mid - 1  # Need smaller
    
    return left
```

---

## Tips

1. **Always define the search space clearly** - what do left and right represent?
2. **Identify the monotonic property** - when does the predicate change from False to True?
3. **Be careful with boundary conditions** - use `left < right` vs `left <= right`
4. **For floating point**, iterate until precision is met
5. **For answer space**, verify the final answer satisfies all constraints
