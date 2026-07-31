# Difference Array Technique

## Concept

A difference array `diff` lets you perform **range update operations in O(1)** instead of O(n).

```
arr = [0, 0, 0, 0, 0, 0]  (n=6)

To add 5 to arr[2..4]:
  diff[2] += 5  → diff = [0, 0, 5, 0, 0, 0, 0]
  diff[5] -= 5  → diff = [0, 0, 5, 0, 0,-5, 0]

Prefix sum of diff → [0, 0, 5, 5, 5, 0, 0]
Result:             [0, 0, 5, 5, 5, 0]
```

---

## When to Use

- Multiple range update operations
- Need to apply all updates then read final array once
- Offline queries (all updates known beforehand)
- LeetCode: Range Addition, Corporate Flight Bookings

---

## Building Difference Array

```python
def build_diff(arr):
    """Build difference array from original array."""
    n = len(arr)
    diff = [0] * (n + 1)
    diff[0] = arr[0]
    for i in range(1, n):
        diff[i] = arr[i] - arr[i - 1]
    return diff
# diff[i] = arr[i] - arr[i-1] for i > 0
```

---

## Range Update in O(1)

```python
def range_update(diff, left, right, val):
    """Add val to all elements in arr[left..right]."""
    diff[left] += val
    if right + 1 < len(diff):
        diff[right + 1] -= val
# O(1) per update!
```

---

## Apply Prefix Sum to Get Final Array

```python
def apply_diff(diff, n):
    """Convert difference array to actual array."""
    result = [0] * n
    result[0] = diff[0]
    for i in range(1, n):
        result[i] = result[i - 1] + diff[i]
    return result
```

---

## Problem 1: Range Addition (LeetCode 370)

**Problem:** Given n elements (all 0), perform multiple range add operations.

```python
def get_modified_array(n, updates):
    diff = [0] * n
    
    for left, right, val in updates:
        diff[left] += val
        if right + 1 < n:
            diff[right + 1] -= val
    
    # Prefix sum
    for i in range(1, n):
        diff[i] += diff[i - 1]
    
    return diff

# Example: n=5, updates=[[1,3,2],[2,4,3],[0,2,-2]]
# After updates: diff = [-2, 2, 5, 2, -3]
# Prefix sum:     [-2, 0, 5, 7, 4]
# Time: O(n + q), Space: O(n)
```

---

## Problem 2: Corporate Flight Bookings (LeetCode 1109)

```python
def corp_flight_bookings(bookings, n):
    diff = [0] * (n + 1)
    
    for first, last, seats in bookings:
        diff[first - 1] += seats  # 1-indexed to 0-indexed
        diff[last] -= seats
    
    result = [0] * n
    result[0] = diff[0]
    for i in range(1, n):
        result[i] = result[i - 1] + diff[i]
    
    return result
# bookings = [[1,2,10],[2,3,20],[2,5,25]], n=5
# diff = [10, 10+20+25=55, -20+... ]
# Time: O(n + b), Space: O(n)
```

---

## Problem 3: Minimum Operations to Make Array Equal

```python
def min_operations_equal(n):
    """Make all elements equal using range increment operations."""
    # Each operation increments a range by 1
    # If we know the target (max element), operations = sum of differences
    # This is just the diff array concept
    pass

# More practical: make all elements equal to target
def operations_to_target(arr, target):
    diff = [0] * len(arr)
    diff[0] = arr[0]
    for i in range(1, len(arr)):
        diff[i] = arr[i] - arr[i - 1]
    
    # Count operations needed
    ops = 0
    for i in range(len(arr)):
        if diff[i] < target:
            ops += target - diff[i]
        elif diff[i] > target:
            ops += diff[i] - target
    return ops
```

---

## Problem 4: Multiple Range Updates

```python
def apply_multiple_updates(n, updates):
    """Apply all updates and return final array."""
    diff = [0] * (n + 1)
    
    for left, right, val in updates:
        diff[left] += val
        diff[right + 1] -= val
    
    # Single pass to get result
    result = [0] * n
    curr = 0
    for i in range(n):
        curr += diff[i]
        result[i] = curr
    
    return result

# Example: n=10, updates=[[2,5,3],[0,3,1],[7,9,4]]
# Time: O(n + q), Space: O(n)
```

---

## Problem 5: Range Update + Point Query

```python
def range_update_point_query(n, updates, queries):
    """Process range updates, then answer point queries."""
    diff = [0] * n
    
    for left, right, val in updates:
        diff[left] += val
        if right + 1 < n:
            diff[right + 1] -= val
    
    # Build prefix sum
    prefix = [0] * n
    prefix[0] = diff[0]
    for i in range(1, n):
        prefix[i] = prefix[i - 1] + diff[i]
    
    # Answer point queries
    return [prefix[q] for q in queries]
```

---

## Problem 6: Range Increment + Range Sum

```python
def range_increment_range_sum(arr, updates, queries):
    """Combined range increment and range sum queries."""
    n = len(arr)
    diff = [0] * (n + 1)
    
    # Process all updates
    for left, right, val in updates:
        diff[left] += val
        diff[right + 1] -= val
    
    # Apply to array
    for i in range(n):
        arr[i] += diff[i]
    
    # Build prefix sum for queries
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Answer queries
    return [prefix[r + 1] - prefix[l] for l, r in queries]
```

---

## Summary

| Operation | Without Diff | With Diff Array |
|-----------|-------------|-----------------|
| Single update | O(n) | O(1) |
| Multiple updates + read once | O(n * q) | O(n + q) |
| Multiple updates + many queries | O(n * q) | O(n + q) per query type |

**Pattern:** If problem says "perform q updates then read array once" -> Difference Array.
