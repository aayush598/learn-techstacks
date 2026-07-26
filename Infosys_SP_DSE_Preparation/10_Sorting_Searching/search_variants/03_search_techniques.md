# Search Techniques - Complete Guide

## Table of Contents
1. [Ternary Search](#1-ternary-search)
2. [Exponential Search](#2-exponential-search)
3. [Interpolation Search](#3-interpolation-search)
4. [Jump Search](#4-jump-search)

---

## 1. Ternary Search

**Use Case**: Finding maximum/minimum of a unimodal function (increases then decreases, or vice versa).

### How Ternary Search Works

Unlike binary search which divides into 2 parts, ternary search divides into 3 parts.

```
UNIMODAL FUNCTION (one peak):

f(x)
  |        *  *
  |      *      *
  |    *          *
  |  *              *
  | *                 *
  |*                    *
  └──────────────────────── x
  L      M1    M2      R

We pick TWO midpoints: M1 and M2
  M1 = L + (R - L) / 3      (one-third from left)
  M2 = R - (R - L) / 3      (one-third from right)

If f(M1) < f(M2):
  The peak CANNOT be in [L, M1] → eliminate left third
  New range: [M1, R]

If f(M1) > f(M2):
  The peak CANNOT be in [M2, R] → eliminate right third
  New range: [L, M2]

Each step eliminates 1/3 of the search space!
```

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

```
BITONIC ARRAY (increases then decreases):
arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
Index: 0  1  2  3  4  5  6  7  8

Step 1: L=0, R=8, M1=2, M2=6
        arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
               L        M1       M2       R
        arr[M1]=5 < arr[M2]=6 -> eliminate [L, M1]
        New: L=3

Step 2: L=3, R=8, M1=5, M2=6
        arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
                     L     M1  M2       R
        arr[M1]=8 > arr[M2]=6 -> eliminate [M2, R]
        New: R=6

Step 3: L=3, R=6, M1=4, M2=5
        arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
                     L  M1  M2     R
        arr[M1]=9 > arr[M2]=8 -> eliminate [M2, R]
        New: R=5

Step 4: L=3, R=5, M1=3, M2=5
        arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
                     L  M1     M2  R
        arr[M1]=7 < arr[M2]=8 -> eliminate [L, M1]
        New: L=4

R - L = 5 - 4 = 1 <= 2 -> Check remaining elements
        arr[4]=9, arr[5]=8 -> max at index 4 (value=9)

Answer: 4 ✓
```

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

    # Check remaining elements (at most 3)
    max_idx = left
    for i in range(left + 1, right + 1):
        if arr[i] > arr[max_idx]:
            max_idx = i

    return max_idx

# Example
arr = [1, 3, 5, 7, 9, 8, 6, 4, 2]
print(ternary_search_discrete(arr))  # 4 (index of 9)
```

### Ternary Search vs Binary Search

```
                    Ternary Search           Binary Search
                    ─────────────            ─────────────
Divides into:       3 parts                  2 parts
Comparisons/step:   2 (f(M1) vs f(M2))      1 (arr[mid] vs target)
Eliminates:         1/3 of space             1/2 of space
Time complexity:    O(log₃ n)               O(log₂ n)

Since log₃ n = log₂ n / log₂ 3 ≈ 0.63 * log₂ n
Ternary does FEWER iterations but MORE work per iteration.
Overall: Binary search is faster for simple comparisons.
Ternary is only better when evaluation is "cheap" and you
need to minimize the number of function evaluations.
```

### Properties
- **Time Complexity**: O(log₃ n) - slower than binary search
- **Use when**: Function is unimodal but not easily differentiable
- **Not suitable for**: Arrays with plateaus or multiple peaks

---

## 2. Exponential Search

**Use Case**: Finding element in unbounded or infinite sorted array.

### How Exponential Search Works

The problem: You don't know the array size. Binary search needs bounds.
Solution: Find the bounds FIRST using exponential jumps!

```
arr = [2, 3, 4, 10, 40, 50, 60, 70, 80, 90, 100, ...]
target = 40

PHASE 1: Find the range by doubling index
═══════════════════════════════════════════

Check index 1:  arr[1]=3 <= 40 ✓ -> continue
Check index 2:  arr[2]=4 <= 40 ✓ -> continue
Check index 4:  arr[4]=40 <= 40 ✓ -> continue
Check index 8:  arr[8]=80 > 40 ✗ -> STOP!

Range found: [index 4/2 .. min(8, n-1)] = [4..8]
             = [40, 50, 60, 70, 80]

PHASE 2: Binary search in the found range
═══════════════════════════════════════════

Binary search [40, 50, 60, 70, 80] for 40
  → Found at index 0 of subarray → index 4 of original

Total work: O(log(4)) to find range + O(log(4)) to search = O(log n)
```

### Visual Timeline

```
Index:  0    1    2    3    4    5    6    7    8    9   10
Value:  2    3    4   10   40   50   60   70   80   90  100

Doubling phase:
  Check idx=1: ✓ (arr[1]=3 <= 40)
  Check idx=2: ✓ (arr[2]=4 <= 40)
  Check idx=4: ✓ (arr[4]=40 <= 40)
  Check idx=8: ✗ (arr[8]=80 > 40) -> STOP

  Range: [4, 8]
         ┌────────────────────────┐
         │ 40   50   60   70   80│
         └────────────────────────┘

Binary search in [4, 5, 6, 7, 8]:
  L=4, R=8, M=6 -> arr[6]=60 > 40 -> R=5
  L=4, R=5, M=4 -> arr[4]=40 == 40 -> FOUND at index 4!
```

```python
def exponential_search(arr, target):
    """Search in unbounded sorted array."""
    n = len(arr)

    if n == 0:
        return -1

    if arr[0] == target:
        return 0

    # Phase 1: Find range by doubling
    index = 1
    while index < n and arr[index] <= target:
        index *= 2

    # Phase 2: Binary search in found range [index/2, min(index, n-1)]
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

### How Interpolation Search Works

Binary search always checks the MIDDLE. Interpolation search ESTIMATES
where the target might be based on its value.

```
BINARY SEARCH: Always picks middle
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
       L                   M                    R
       Always mid = (L+R)/2 regardless of target

INTERPOLATION SEARCH: Picks position based on value
arr = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

To find target=90:
  Binary: starts at index 4 (value=50) -> 5 steps
  Interpolation: estimates position near the end -> 1-2 steps!

Formula:
  pos = L + ((target - arr[L]) * (R - L)) / (arr[R] - arr[L])

For target=90, L=0, R=9:
  pos = 0 + ((90-10) * (9-0)) / (100-10)
      = 0 + (80 * 9) / 90
      = 0 + 720/90
      = 8
  arr[8] = 90 -> FOUND in 1 step!
```

### When It Works Well vs Poorly

```
UNIFORM DISTRIBUTION (works great):
Value:  10  20  30  40  50  60  70  80  90  100
        ──  ──  ──  ──  ──  ──  ──  ──  ──  ──
        Even spacing → interpolation estimates well

EXPONENTIAL DISTRIBUTION (works poorly):
Value:  1   2   4   8  16  32  64  128  256  512
        ─ ─ ─  ──  ── ─── ──── ───── ──────
        Uneven spacing → interpolation estimates poorly
        Could degenerate to O(n)!
```

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

### How Jump Search Works

Instead of checking every element (linear) or halving (binary),
we JUMP ahead by fixed blocks, then do linear search within the block.

```
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]     target = 7
n = 10, jump = sqrt(10) ≈ 3

PHASE 1: Jump to find the block containing target
════════════════════════════════════════════════════

Block size = 3

Jump 0: Check arr[2] = 3  < 7 -> Jump forward
Jump 1: Check arr[5] = 6  < 7 -> Jump forward
Jump 2: Check arr[8] = 9  >= 7 -> STOP! Target is in block [5, 8]

Index: 0  1  2  3  4  5  6  7  8  9
Value: 1  2  3  4  5  6  7  8  9  10
                │  BLOCK  │
Jump 0→        Jump 1→        Jump 2→ (stop, 9 >= 7)
     arr[2]=3       arr[5]=6       arr[8]=9

PHASE 2: Linear search within the block [5, 8]
═════════════════════════════════════════════════

Check arr[5]=6 < 7 -> next
Check arr[6]=7 == 7 -> FOUND at index 6!
```

### Why Optimal Jump Size is sqrt(n)

```
Total cost = (number of jumps) + (linear search in block)
           = (n / jump_size) + (jump_size - 1)

To minimize: take derivative, set to 0
  d/d(jump_size) [n/jump_size + jump_size] = 0
  -n/jump_size^2 + 1 = 0
  jump_size = sqrt(n)

For n=100: jump_size = 10
  Jumps: 100/10 = 10
  Linear: 10 - 1 = 9
  Total: ~19 (vs 100 for linear, vs ~7 for binary)
```

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
