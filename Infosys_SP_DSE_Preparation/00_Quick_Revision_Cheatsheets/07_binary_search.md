# Binary Search — Last-Minute Revision

Copy-paste ready, tested Python 3 templates for every binary search flavor, plus the `bisect` module.

## bisect Module — Exact Behavior

`bisect` works on any sorted list. On DUPLICATES the behavior is what matters:

```python
from bisect import bisect_left, bisect_right, insort_left, insort_right

arr = [1, 3, 3, 5, 7]

bisect_left(arr, 3)   # 1  -> first position where 3 can be inserted (leftmost match / lower bound)
bisect_right(arr, 3)  # 3  -> first position AFTER the last 3 (upper bound)
bisect_left(arr, 4)   # 3  -> where 4 would go (no match, same as right)
bisect_right(arr, 4)  # 3
bisect_left(arr, 0)   # 0  (before everything)
bisect_right(arr, 9)  # 5  (after everything)

insort_left(arr, 3)   # arr -> [1,3,3,3,5,7] inserts before existing 3s
insort_right(arr, 3)  # arr -> [1,3,3,3,3,5,7] inserts after existing 3s (stable for equal keys)
```

Common tricks built on bisect:
```python
def first_ge(arr, x):   return bisect_left(arr, x)          # first index with value >= x
def first_gt(arr, x):   return bisect_right(arr, x)         # first index with value > x
def last_le(arr, x):    return bisect_right(arr, x) - 1     # last index with value <= x
def last_lt(arr, x):    return bisect_left(arr, x) - 1      # last index with value < x
def contains(arr, x):   i = bisect_left(arr, x); return i < len(arr) and arr[i] == x
```

| Function | Returns | Time |
|---|---|---|
| `bisect_left(a, x)` | leftmost insertion point (lower bound) | O(log n) |
| `bisect_right(a, x)` | insertion point after all equal (upper bound) | O(log n) |
| `insort_left/right(a, x)` | insert preserving order | O(n) shift |

## Custom Binary Search — The Single Canonical Template

The `while lo < hi` form (searching for the boundary between "no" and "yes"). With `mid = lo + (hi - lo) // 2`, you need a matching `lo = mid + 1` / `hi = mid` pair. NEVER mix `hi = mid - 1` with this formula (infinite loop risk).

**Lower-bound template (find first index where `predicate(i)` is True):**

```python
def first_true(predicate, lo, hi):     # [lo, hi) or [lo, hi] both fine with these rules
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if predicate(mid):
            hi = mid                   # mid is valid, keep looking left
        else:
            lo = mid + 1               # mid is invalid, move right
    return lo                          # first True index (or lo==hi == len if none)
```

**Upper-bound template (find last index where `predicate(i)` is True):**

```python
def last_true(predicate, lo, hi):
    while lo < hi:
        mid = lo + (hi - lo + 1) // 2  # CEILING mid — required when lo = mid
        if predicate(mid):
            lo = mid
        else:
            hi = mid - 1
    return lo                          # last True index (or lo == -1 if none)
```

Decision table (memorize):
| If you use | Your matching moves are |
|---|---|
| `mid = (lo + hi) // 2` (floor) | `lo = mid + 1` and `hi = mid` |
| `mid = (lo + hi + 1) // 2` (ceil) | `lo = mid` and `hi = mid - 1` |
| classic `<=` over a target | `lo = mid + 1`, `hi = mid - 1`, `return -1` |

## First and Last Occurrence of Target (lower/upper bound)

```python
from bisect import bisect_left, bisect_right

def first_last(nums, target):
    lo = bisect_left(nums, target)
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]
    return [lo, bisect_right(nums, target) - 1]

# first_last([5,7,7,8,8,10], 8) -> [3,4]   |   first_last([5,7,7,8,8,10], 6) -> [-1,-1]
```

## Find Minimum in Rotated Sorted Array

```python
def find_min_rotated(nums):          # [4,5,6,7,0,1,2] -> 0
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1             # min is in the right half
        else:
            hi = mid                 # min is at mid or left
    return nums[lo]
```

## Search Target in Rotated Sorted Array

```python
def search_rotated(nums, target):    # [4,5,6,7,0,1,2], target=0 -> 4
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:            # left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                                # right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
```

## Search in 2D Sorted Matrix (flatten mentally)

```python
def search_matrix(matrix, target):   # rows and columns both sorted ascending
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // n][mid % n]
        if val == target:
            return True
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
```

## Square Root (integer) — binary search on answer

```python
def my_sqrt(x):
    if x < 2:
        return x
    lo, hi = 1, x // 2
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi                     # largest mid with mid*mid <= x

# my_sqrt(8) -> 2   |   my_sqrt(16) -> 4   |   my_sqrt(0) -> 0
```

## Peak Element (any peak in an unsorted array)

```python
def find_peak(nums):               # nums[-1] = nums[n] = -infinity assumed
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1           # uphill to the right, peak is right
        else:
            hi = mid               # mid is itself a candidate peak
    return lo                      # index of a peak

# find_peak([1,2,3,1]) -> 2   |   find_peak([1,2,1,3,5,6,4]) -> 5 (one valid peak)
```

## Binary Search on Answer — minimize-max / maximize-min

Use when the answer is a NUMBER in a range and you can test "is answer X feasible?" cheaply. Classic tells: "minimum capacity such that", "maximum minimum distance", "least number of days".

**Feasible-predicate pattern:**

```python
def minimize_max_feasible(nums, k, candidate):   # <= k partitions, each sum <= candidate
    count = 1
    cur_sum = 0
    for x in nums:
        if cur_sum + x <= candidate:
            cur_sum += x
        else:
            count += 1
            cur_sum = x
    return count <= k
```

**Capacity to Ship Packages Within D Days (minimize the max daily load):**

```python
def ship_within_days(weights, days):
    lo = max(weights)              # each package must fit
    hi = sum(weights)              # ship everything in one day

    def feasible(cap):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d += 1
                load = 0
            load += w
        return d <= days

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid               # can do it -> try smaller
        else:
            lo = mid + 1
    return lo
# ship_within_days([1,2,3,4,5,6,7,8,9,10], 5) -> 15
```

**Koko Eating Bananas (minimize eating speed):**

```python
import math

def min_eating_speed(piles, h):
    lo, hi = 1, max(piles)

    def feasible(speed):
        return sum(math.ceil(p / speed) for p in piles) <= h

    while lo < hi:
        mid = lo + (hi - lo) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
# min_eating_speed([3,6,7,11], 8) -> 4
```

**Maximize the minimum distance (aggressive cows / place k balls):**

```python
def max_min_distance(positions, k):   # positions sorted; place k items, maximize min gap
    positions.sort()
    lo, hi = 1, positions[-1] - positions[0]

    def feasible(gap):
        count, last = 1, positions[0]
        for p in positions[1:]:
            if p - last >= gap:
                count += 1
                last = p
        return count >= k

    while lo < hi:
        mid = lo + (hi - lo + 1) // 2   # CEILING because we search the LAST feasible
        if feasible(mid):
            lo = mid                    # gap works -> try bigger
        else:
            hi = mid - 1
    return lo
# max_min_distance([1,2,3,4,7], 3) -> 3
```

| Template | Time | Space |
|---|---|---|
| bisect on sorted array | O(log n) | O(1) |
| first/last occurrence | O(log n) | O(1) |
| rotated min / search | O(log n) | O(1) |
| search 2D matrix | O(log(m·n)) | O(1) |
| sqrt / peak | O(log n) | O(1) |
| binary search on answer | O(log(range) · cost(feasible)) | O(1) |

## The 3 Rules That Prevent Bugs

1. **`mid = lo + (hi - lo) // 2`** avoids integer overflow (matters in C++/Java; harmless in Python).
2. **Pair the formula with the moves:** floor-mid pairs with `lo = mid + 1` / `hi = mid`; ceil-mid pairs with `lo = mid` / `hi = mid - 1`. If you ever write `lo = mid` with floor-mid, you can infinite-loop.
3. **When the answer is a minimum, search the FIRST feasible (floor-mid + `hi = mid`).** When it's a maximum, search the LAST feasible (ceil-mid + `lo = mid`).
