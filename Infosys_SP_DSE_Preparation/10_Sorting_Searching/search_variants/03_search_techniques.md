# Search Techniques - Complete Guide

## Table of Contents
1. [Ternary Search](#1-ternary-search)
2. [Exponential Search](#2-exponential-search)
3. [Interpolation Search](#3-interpolation-search)
4. [Jump Search](#4-jump-search)

---

## 1. Ternary Search

**Use Case**: Finding maximum/minimum of a unimodal function (increases then decreases, or vice versa).

### For Maximum of Unimodal Function

```python
def ternary_search_max(f, left, right, precision=1e-9):
    """Find maximum of unimodal function using ternary search."""
    while right - left > precision:
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3
        
        if f(mid1) < f(mid2):
            left = mid1
        else:
            right = mid2
    
    return (left + right) / 2

# Example: Find maximum of f(x) = -(x-3)^2 + 10
def f(x):
    return -(x - 3) ** 2 + 10

max_x = ternary_search_max(f, 0, 10)
print(f"Maximum at x = {max_x:.6f}, f(x) = {f(max_x):.6f}")
# Output: Maximum at x = 3.000000, f(x) = 10.000000
```

### For Minimum of Unimodal Function

```python
def ternary_search_min(f, left, right, precision=1e-9):
    """Find minimum of unimodal function using ternary search."""
    while right - left > precision:
        mid1 = left + (right - left) / 3
        mid2 = right - (right - left) / 3
        
        if f(mid1) > f(mid2):
            left = mid1
        else:
            right = mid2
    
    return (left + right) / 2

# Example: Find minimum of f(x) = (x-5)^2 + 3
def g(x):
    return (x - 5) ** 2 + 3

min_x = ternary_search_min(g, 0, 10)
print(f"Minimum at x = {min_x:.6f}, f(x) = {g(min_x):.6f}")
# Output: Minimum at x = 5.000000, f(x) = 3.000000
```

### Ternary Search on Discrete Array

```python
def ternary_search_discrete(arr):
    """Find maximum in a bitonic array (increases then decreases)."""
    left, right = 0, len(arr) - 1
    
    while right - left > 2:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        if arr[mid1] < arr[mid2]:
            left = mid1
        else:
            right = mid2
    
    # Check remaining elements
    max_idx = left
    for i in range(left + 1, right + 1):
        if arr[i] > arr[max_idx]:
            max_idx = i
    
    return max_idx

# Example
arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
print(ternary_search_discrete(arr))  # 4 (index of 9)
```

### Properties
- **Time Complexity**: O(log₃ n) - slower than binary search
- **Use when**: Function is unimodal but not easily differentiable
- **Not suitable for**: Arrays with plateaus or multiple peaks

---

## 2. Exponential Search

**Use Case**: Finding element in unbounded or infinite sorted array.

```python
def exponential_search(arr, target):
    """Search in unbounded sorted array."""
    n = len(arr)
    
    if n == 0:
        return -1
    
    if arr[0] == target:
        return 0
    
    # Find range by doubling
    index = 1
    while index < n and arr[index] <= target:
        index *= 2
    
    # Binary search in the found range
    left = index // 2
    right = min(index, n - 1)
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Example
arr = [2, 3, 4, 10, 40, 50, 60, 70, 80, 90, 100]
target = 10
print(exponential_search(arr, target))  # 3
```

### Finding First Occurrence in Unbounded Array

```python
def exponential_search_first(arr, target):
    """Find first occurrence in unbounded sorted array."""
    n = len(arr)
    
    if n == 0:
        return -1
    
    # Find range
    index = 1
    while index < n and arr[index] < target:
        index *= 2
    
    # Binary search for first occurrence
    left = index // 2
    right = min(index, n - 1)
    result = -1
    
    while left <= right:
        mid = left + (right - left) // 2
        
        if arr[mid] == target:
            result = mid
            right = mid - 1  # Continue searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return result

# Example
arr = [2, 3, 4, 4, 4, 10, 40]
print(exponential_search_first(arr, 4))  # 2
```

### Properties
- **Time Complexity**: O(log n)
- **Best for**: Unbounded/infinite sorted arrays
- **Combines**: Exponential search + binary search

---

## 3. Interpolation Search

**Use Case**: Uniformly distributed sorted arrays. Improved binary search.

```python
def interpolation_search(arr, target):
    """Search in uniformly distributed sorted array."""
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        if arr[left] == arr[right]:
            if arr[left] == target:
                return left
            break
        
        # Estimate position using linear interpolation
        pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return -1

# Example - works best with uniform distribution
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
target = 70
print(interpolation_search(arr, target))  # 6
```

### Recursive Version

```python
def interpolation_search_recursive(arr, target, left, right):
    """Recursive interpolation search."""
    if left > right or arr[left] > target or arr[right] < target:
        return -1
    
    if arr[left] == arr[right]:
        return left if arr[left] == target else -1
    
    # Estimate position
    pos = left + ((target - arr[left]) * (right - left)) // (arr[right] - arr[left])
    
    if arr[pos] == target:
        return pos
    elif arr[pos] < target:
        return interpolation_search_recursive(arr, target, pos + 1, right)
    else:
        return interpolation_search_recursive(arr, target, left, pos - 1)

# Example
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
target = 70
print(interpolation_search_recursive(arr, target, 0, len(arr) - 1))  # 6
```

### Properties
- **Time Complexity**: Best O(log log n), Average O(log log n), Worst O(n)
- **Best for**: Uniformly distributed data
- **Worst case**: When data is exponentially distributed

---

## 4. Jump Search

**Use Case**: Sorted array, when jumping ahead is more efficient than linear scan.

```python
import math

def jump_search(arr, target):
    """Jump search in sorted array."""
    n = len(arr)
    jump = int(math.sqrt(n))  # Optimal jump size
    
    # Find the block where element is present
    prev = 0
    while arr[min(jump, n) - 1] < target:
        prev = jump
        jump += int(math.sqrt(n))
        
        if prev >= n:
            return -1
    
    # Linear search within the block
    while arr[prev] < target:
        prev += 1
        
        if prev == min(jump, n):
            return -1
    
    if arr[prev] == target:
        return prev
    
    return -1

# Example
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 7
print(jump_search(arr, target))  # 6
```

### Optimized Jump Search

```python
import math

def jump_search_optimized(arr, target):
    """Optimized jump search with better boundary handling."""
    n = len(arr)
    jump = int(math.sqrt(n))
    
    prev = 0
    curr = jump
    
    # Find block
    while curr < n and arr[curr] < target:
        prev = curr
        curr += jump
    
    # Linear search in block
    for i in range(prev, min(curr + 1, n)):
        if arr[i] == target:
            return i
    
    return -1

# Example
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 7
print(jump_search_optimized(arr, target))  # 6
```

### Properties
- **Time Complexity**: O(√n)
- **Space Complexity**: O(1)
- **Best for**: When jumping back is expensive (e.g., linked list)
- **Optimal jump size**: √n

---

## Comparison Table

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Use Case |
|-----------|-------------|------------|--------------|-------|----------|
| Binary Search | O(1) | O(log n) | O(log n) | O(1) | Sorted array |
| Ternary Search | O(1) | O(log₃ n) | O(log₃ n) | O(1) | Unimodal function |
| Exponential Search | O(1) | O(log n) | O(log n) | O(1) | Unbounded array |
| Interpolation Search | O(1) | O(log log n) | O(n) | O(1) | Uniform distribution |
| Jump Search | O(1) | O(√n) | O(√n) | O(1) | When jump back is costly |

---

## When to Use Which

| Scenario | Recommended | Why |
|----------|-------------|-----|
| Sorted array, known size | Binary Search | Simple and efficient |
| Unbounded/infinite array | Exponential Search | Finds range first |
| Uniformly distributed | Interpolation Search | Better average case |
| Unimodal function | Ternary Search | Handles non-differentiable |
| Linked list / costly jump back | Jump Search | Minimizes jumps |

---

## Key Insights

1. **Binary search** is the default choice for sorted arrays
2. **Exponential search** handles unknown array sizes
3. **Interpolation search** is optimal for uniform data but degrades to O(n)
4. **Ternary search** is for optimization problems, not direct search
5. **Jump search** is useful when backward movement is expensive
6. Always consider the **data distribution** and **access pattern** when choosing
