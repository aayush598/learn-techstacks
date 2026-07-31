# Sorting Algorithms - Complete Guide

## Table of Contents
1. [Bubble Sort](#1-bubble-sort)
2. [Selection Sort](#2-selection-sort)
3. [Insertion Sort](#3-insertion-sort)
4. [Merge Sort](#4-merge-sort)
5. [Quick Sort](#5-quick-sort)
6. [Counting Sort](#6-counting-sort)
7. [Radix Sort](#7-radix-sort)
8. [Bucket Sort](#8-bucket-sort)
9. [Python's Timsort](#9-pythons-timsort)
10. [When to Use Which](#10-when-to-use-which)
11. [Comparison Table](#11-comparison-table)

---

## 1. Bubble Sort

### How Bubble Sort Works - Visual Walkthrough

Bubble sort repeatedly steps through the list, compares adjacent elements,
and swaps them if they are in the wrong order. Larger elements "bubble up"
to the end.

```
arr = [64, 34, 25, 12]

PASS 1: Bubble the largest to the end
═══════════════════════════════════════
[64, 34, 25, 12]
  ^^  ^^              64 > 34? YES -> SWAP
[34, 64, 25, 12]
     ^^  ^^           64 > 25? YES -> SWAP
[34, 25, 64, 12]
        ^^  ^^        64 > 12? YES -> SWAP
[34, 25, 12, 64]              <- 64 is now in place!

PASS 2: Bubble next largest
═══════════════════════════════════════
[34, 25, 12, 64]
  ^^  ^^              34 > 25? YES -> SWAP
[25, 34, 12, 64]
     ^^  ^^           34 > 12? YES -> SWAP
[25, 12, 34, 64]              <- 34 is now in place!

PASS 3: Bubble next largest
═══════════════════════════════════════
[25, 12, 34, 64]
  ^^  ^^              25 > 12? YES -> SWAP
[12, 25, 34, 64]              <- 25 is now in place!

PASS 4: No swaps needed -> DONE!

Result: [12, 25, 34, 64] ✓
```

### Visual: Elements "Bubbling Up"

```
Initial:    64  34  25  12
After P1:   34  25  12  [64]    64 bubbled to end
After P2:   25  12  [34] [64]   34 bubbled to 2nd-to-last
After P3:   12  [25] [34] [64]  25 bubbled to position 2
Done:       [12] [25] [34] [64] All sorted!

The bracketed elements are "sorted" after each pass.
Each pass places one more element in its final position.
```

```python
def bubble_sort(arr):
    """Basic bubble sort."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

### Optimized Version - O(n²) worst, O(n) best

```python
def bubble_sort_optimized(arr):
    """Optimized bubble sort - stops if no swaps in a pass."""
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        
        # If no swaps, array is sorted
        if not swapped:
            break
    
    return arr

# Example
arr = [64, 34, 25, 12, 22, 11, 90]
print(bubble_sort_optimized(arr))  # [11, 12, 22, 25, 34, 64, 90]
```

### Properties
- **Time Complexity**: Best O(n), Average O(n²), Worst O(n²)
- **Space Complexity**: O(1)
- **Stable**: Yes
- **In-place**: Yes
- **Adaptive**: Yes (with optimization)

---

## 2. Selection Sort

### How Selection Sort Works - Visual Walkthrough

Selection sort divides the array into sorted and unsorted regions.
It repeatedly FINDS THE MINIMUM from the unsorted region and SWAPS
it with the first unsorted element.

```
arr = [64, 25, 12, 22, 11]

PASS 1: Find minimum in [64, 25, 12, 22, 11]
═══════════════════════════════════════════════
[64, 25, 12, 22, 11]
  ↓
  64 > 25 -> min=25 (idx=1)
  25 > 12 -> min=12 (idx=2)
  12 < 22
  12 < 11? NO -> min=11 (idx=4)
  Minimum = 11 at index 4
  Swap arr[0] and arr[4]:
[11, 25, 12, 22, 64]     <- 11 is now sorted!

PASS 2: Find minimum in [25, 12, 22, 64]
═══════════════════════════════════════════════
[11, 25, 12, 22, 64]
      ↓
      25 > 12 -> min=12 (idx=2)
      12 < 22
      12 < 64
  Minimum = 12 at index 2
  Swap arr[1] and arr[2]:
[11, 12, 25, 22, 64]     <- 12 is now sorted!

PASS 3: Find minimum in [25, 22, 64]
═══════════════════════════════════════════════
[11, 12, 25, 22, 64]
         ↓
         25 > 22 -> min=22 (idx=3)
         22 < 64
  Minimum = 22 at index 3
  Swap arr[2] and arr[3]:
[11, 12, 22, 25, 64]     <- 22 is now sorted!

PASS 4: Only 25 and 64 left
═══════════════════════════════════════════════
[11, 12, 22, 25, 64]     <- Already in order!

Result: [11, 12, 22, 25, 64] ✓
```

### Selection Sort vs Bubble Sort

```
Selection Sort: Makes FEWER swaps (only 1 per pass)
Bubble Sort:    Makes MANY swaps (potentially n-1 per pass)

Selection: [64, 25, 12, 22, 11]
           Find min=11, swap once -> [11, 25, 12, 22, 64]
           Only 1 swap per pass!

Bubble:    [64, 25, 12, 22, 11]
           64>25 swap, 64>12 swap, 64>22 swap, 64>11 swap
           Up to n-1 swaps per pass!

Use Selection when: Write operations are expensive (e.g., flash memory)
Use Bubble when: You need to detect if array is already sorted
```

### Properties
- **Time Complexity**: Best O(n²), Average O(n²), Worst O(n²)
- **Space Complexity**: O(1)
- **Stable**: No (can be made stable)
- **In-place**: Yes
- **Adaptive**: No

---

## 3. Insertion Sort

### How Insertion Sort Works - Visual Walkthrough

Insertion sort builds the sorted array one element at a time by
INSERTING each new element into its correct position.

Think of it like sorting a hand of playing cards!

```
arr = [12, 11, 13, 5, 6]

Start: [12] | 11  13   5   6
        ───    ──────────────
       sorted   unsorted

PASS 1: Insert 11
═══════════════════
[12] | 11
 11 < 12? YES -> shift 12 right, insert 11
[11, 12] | 13   5   6

PASS 2: Insert 13
═══════════════════
[11, 12] | 13
 13 > 12? YES -> already in place
[11, 12, 13] | 5   6

PASS 3: Insert 5
═══════════════════
[11, 12, 13] | 5
 5 < 13 -> shift 13 right
 5 < 12 -> shift 12 right
 5 < 11 -> shift 11 right
 Insert 5 at beginning
[5, 11, 12, 13] | 6

PASS 4: Insert 6
═══════════════════
[5, 11, 12, 13] | 6
 6 < 13 -> shift 13 right
 6 < 12 -> shift 12 right
 6 < 11 -> shift 11 right
 6 > 5 -> insert after 5
[5, 6, 11, 12, 13]

Result: [5, 6, 11, 12, 13] ✓
```

### Card Sorting Analogy

```
Imagine holding cards in your hand:

  Hand: [12]
  Table: 11  13   5   6

  Pick up 11, insert before 12:
  Hand: [11, 12]
  Table: 13   5   6

  Pick up 13, insert after 12:
  Hand: [11, 12, 13]
  Table: 5   6

  Pick up 5, insert at beginning:
  Hand: [5, 11, 12, 13]
  Table: 6

  Pick up 6, insert after 5:
  Hand: [5, 6, 11, 12, 13]
  Table: (empty)

Done! This is exactly how insertion sort works.
```

### When Insertion Sort is FAST

```
BEST CASE: Array is already sorted
  Each element is compared once and stays in place
  Time: O(n) !!!

WORST CASE: Array is in reverse order
  Each element must shift all previous elements
  Time: O(n²)

NEARLY SORTED: Only a few elements out of place
  Most elements stay, few shift
  Time: O(n + d) where d = number of inversions

This is why Insertion Sort is used as the base case
in Timsort and other hybrid sorts!
```

### Properties
- **Time Complexity**: Best O(n), Average O(n²), Worst O(n²)
- **Space Complexity**: O(1)
- **Stable**: Yes
- **In-place**: Yes
- **Adaptive**: Yes
- **Best for**: Small arrays or nearly sorted arrays

---

## 4. Merge Sort

### How Merge Sort Works - Visual Walkthrough

Merge sort uses DIVIDE AND CONQUER: split the array in half,
recursively sort each half, then merge the sorted halves.

```
DIVIDE PHASE - Split until single elements:
═══════════════════════════════════════════════

                  [38, 27, 43, 3, 9, 82, 10]
                 /                            \
        [38, 27, 43, 3]                [9, 82, 10]
        /              \                /          \
    [38, 27]      [43, 3]          [9, 82]      [10]
    /      \       /    \          /      \
  [38]   [27]   [43]   [3]      [9]     [82]

MERGE PHASE - Combine sorted halves:
═══════════════════════════════════════

  [38] + [27] -> compare 38 vs 27 -> [27, 38]
  [43] + [3]  -> compare 43 vs 3  -> [3, 43]

  [27, 38] + [3, 43] -> merge:
    27 < 3? NO  -> take 3,  result=[3]
    27 < 43? YES -> take 27, result=[3, 27]
    38 < 43? YES -> take 38, result=[3, 27, 38]
    remaining 43    -> result=[3, 27, 38, 43]

  [9] + [82] -> [9, 82]
  [9, 82] + [10] -> merge:
    9 < 10? YES -> take 9,  result=[9]
    82 < 10? NO  -> take 10, result=[9, 10]
    remaining 82    -> result=[9, 10, 82]

  [3, 27, 38, 43] + [9, 10, 82] -> final merge:
    3 < 9?   YES -> [3]
    27 < 9?  NO  -> [3, 9]
    27 < 10? NO  -> [3, 9, 10]
    27 < 82? YES -> [3, 9, 10, 27]
    38 < 82? YES -> [3, 9, 10, 27, 38]
    43 < 82? YES -> [3, 9, 10, 27, 38, 43]
    remaining 82 -> [3, 9, 10, 27, 38, 43, 82]

Result: [3, 9, 10, 27, 38, 43, 82] ✓
```

### Merge Operation - Detailed View

```
Merging [27, 38] and [3, 43]:

  Left:  [27, 38]    Right: [3, 43]
           ↑                ↑
           i                j

  Step 1: Compare 27 vs 3
          3 is smaller -> take from Right
          Left:  [27, 38]    Right: [3, 43]
                    ↑                ↑
                    i                j
          Result: [3]

  Step 2: Compare 27 vs 43
          27 is smaller -> take from Left
          Left:  [27, 38]    Right: [3, 43]
                       ↑              ↑
                       i              j
          Result: [3, 27]

  Step 3: Compare 38 vs 43
          38 is smaller -> take from Left
          Left:  [27, 38]    Right: [3, 43]
                            ↑            ↑
                            i            j
          Result: [3, 27, 38]

  Step 4: Left exhausted, copy remaining Right
          Result: [3, 27, 38, 43]
```

### In-place Merge Sort

```python
def merge_sort_inplace(arr, left, right):
    """In-place merge sort using auxiliary array only for merging."""
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_inplace(arr, left, mid, right)

def merge_inplace(arr, left, mid, right):
    """Merge two sorted subarrays in-place."""
    left_arr = arr[left:mid + 1]
    right_arr = arr[mid + 1:right + 1]
    
    i = j = 0
    k = left
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1

# Usage
arr = [38, 27, 43, 3, 9, 82, 10]
merge_sort_inplace(arr, 0, len(arr) - 1)
print(arr)  # [3, 9, 10, 27, 38, 43, 82]
```

### Iterative Merge Sort

```python
def merge_sort_iterative(arr):
    """Iterative merge sort using bottom-up approach."""
    n = len(arr)
    width = 1
    
    while width < n:
        for i in range(0, n, 2 * width):
            left = i
            mid = min(i + width - 1, n - 1)
            right = min(i + 2 * width - 1, n - 1)
            
            if mid < right:
                merge_inplace(arr, left, mid, right)
        
        width *= 2
    
    return arr

# Example
arr = [38, 27, 43, 3, 9, 82, 10]
print(merge_sort_iterative(arr))  # [3, 9, 10, 27, 38, 43, 82]
```

### Properties
- **Time Complexity**: Best O(n log n), Average O(n log n), Worst O(n log n)
- **Space Complexity**: O(n)
- **Stable**: Yes
- **In-place**: No (unless modified)
- **Best for**: Linked lists, external sorting

---

## 5. Quick Sort

### How Quick Sort Works - Visual Walkthrough

Quick sort picks a PIVOT element and PARTITIONS the array so that
elements smaller than pivot go LEFT and larger go RIGHT.

```
arr = [10, 7, 8, 9, 1, 5]     pivot = 5 (last element)

PARTITION (Lomuto scheme):
═══════════════════════════

Initial:  [10, 7, 8, 9, 1, |5|]
           i = -1 (before start)
           j scans from left to right-1

Compare arr[j] with pivot:
  j=0: arr[0]=10 > 5? YES -> skip (10 stays on right)
  j=1: arr[1]=7 > 5?  YES -> skip
  j=2: arr[2]=8 > 5?  YES -> skip
  j=3: arr[3]=9 > 5?  YES -> skip
  j=4: arr[4]=1 <= 5? YES -> i++, swap arr[i] and arr[j]
       swap arr[0] and arr[4]: [1, 7, 8, 9, 10, 5]

After scan:  i=0, place pivot after i
  swap arr[1] and arr[5]: [1, 5, 8, 9, 10, 7]

  Wait, let me redo this more carefully...

Actually with Lomuto (pivot=5):
  [10, 7, 8, 9, 1, 5]  pivot=5

  i = -1
  j=0: 10 <= 5? No
  j=1: 7 <= 5?  No
  j=2: 8 <= 5?  No
  j=3: 9 <= 5?  No
  j=4: 1 <= 5?  Yes -> i=0, swap arr[0] and arr[4]
       [1, 7, 8, 9, 10, 5]

  Place pivot: swap arr[i+1] and arr[high]
  swap arr[1] and arr[5]: [1, 5, 8, 9, 10, 7]

  Pivot 5 is now at index 1!
  Left of pivot:  [1]    <- all <= 5 ✓
  Right of pivot: [8, 9, 10, 7]  <- all > 5 ✓

  Pivot is in its FINAL position!
```

### Quick Sort Recursion Tree

```
                    [10, 7, 8, 9, 1, 5]
                           pivot=5
                    /                    \
              [1]                    [8, 9, 10, 7]
            (sorted)                    pivot=7
                                   /              \
                              [8]          [9, 10]
                           (sorted)          pivot=10
                                            /       \
                                         [9]       []
                                        (sorted)  (sorted)

Combined: [1, 5, 7, 8, 9, 10] ✓

Each partition places the pivot in its FINAL position.
Recursion continues on left and right subarrays.
```

### Hoare Partition

```python
def quicksort_hoare(arr, low, high):
    """Quick sort using Hoare partition."""
    if low < high:
        pi = hoare_partition(arr, low, high)
        quicksort_hoare(arr, low, pi)
        quicksort_hoare(arr, pi + 1, high)
    
    return arr

def hoare_partition(arr, low, high):
    """Hoare partition scheme - more efficient than Lomuto."""
    pivot = arr[low]
    i = low - 1
    j = high + 1
    
    while True:
        # Move right pointer to element <= pivot
        j -= 1
        while arr[j] > pivot:
            j -= 1
        
        # Move left pointer to element >= pivot
        i += 1
        while arr[i] < pivot:
            i += 1
        
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
        else:
            return j

# Usage
arr = [10, 7, 8, 9, 1, 5]
quicksort_hoare(arr, 0, len(arr) - 1)
print(arr)  # [1, 5, 7, 8, 9, 10]
```

### Quick Select (Kth Smallest)

```python
import random

def quickselect(arr, k):
    """Find kth smallest element using quickselect."""
    if len(arr) == 1:
        return arr[0]
    
    pivot = random.choice(arr)
    
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]
    
    if k <= len(lows):
        return quickselect(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return quickselect(highs, k - len(lows) - len(pivots))

# Example
arr = [3, 2, 1, 5, 4]
k = 3
print(f"{k}rd smallest: {quickselect(arr, k)}")  # 3
```

### Properties
- **Time Complexity**: Best O(n log n), Average O(n log n), Worst O(n²)
- **Space Complexity**: O(log n) recursion stack
- **Stable**: No
- **In-place**: Yes
- **Best for**: General purpose, cache efficient

### Quick Select (Kth Smallest)

Quick select is a variant of quick sort that only recurses into ONE partition,
giving O(n) average time for finding the kth smallest element.

```
Finding 3rd smallest in [3, 2, 1, 5, 4]:

Partition with pivot=4:
  Left: [3, 2, 1]   Pivot: [4]   Right: [5]
  Left has 3 elements, k=3 <= 3 → recurse into LEFT

Partition [3, 2, 1] with pivot=2:
  Left: [1]   Pivot: [2]   Right: [3]
  Left has 1 element, k=3 > 1+1=2 → k becomes 3-1-1=1, recurse into RIGHT

[3] has k=1 → 3 is the 3rd smallest! ✓
```

```python
import random

def quickselect(arr, k):
    """Find kth smallest element using quickselect."""
    if len(arr) == 1:
        return arr[0]

    pivot = random.choice(arr)

    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k <= len(lows):
        return quickselect(lows, k)
    elif k <= len(lows) + len(pivots):
        return pivot
    else:
        return quickselect(highs, k - len(lows) - len(pivots))

# Example
arr = [3, 2, 1, 5, 4]
k = 3
print(f"{k}rd smallest: {quickselect(arr, k)}")  # 3
```

### How Counting Sort Works - Visual Walkthrough

Counting sort counts occurrences of each element, then uses cumulative
counts to place elements directly in their correct positions.

```
arr = [4, 2, 2, 8, 3, 3, 1]

STEP 1: Count occurrences
═══════════════════════════
Element:  1  2  3  4  5  6  7  8
Count:   [1, 2, 2, 1, 0, 0, 0, 1]
          ↑  ↑  ↑  ↑              ↑
          1  two twos  4  zeros  8

STEP 2: Compute cumulative count
═══════════════════════════════════
Element:  1  2  3  4  5  6  7  8
Cumul:   [1, 3, 5, 6, 6, 6, 6, 7]
          ↑  ↑  ↑  ↑
          1  1+2  3+2  5+1

Cumulative count tells us: "Elements <= this value
end at this position in the output"

STEP 3: Build output (traverse input in REVERSE for stability)
═════════════════════════════════════════════════════════════════

arr = [4, 2, 2, 8, 3, 3, 1]
               ← ← ← ← ← ← ←  (process right to left)

Process arr[6]=1: cumul[1]=1, place at output[0], decrement cumul[1] to 0
Process arr[5]=3: cumul[3]=5, place at output[4], decrement cumul[3] to 4
Process arr[4]=3: cumul[3]=4, place at output[3], decrement cumul[3] to 3
Process arr[3]=8: cumul[8]=7, place at output[6], decrement cumul[8] to 6
Process arr[2]=2: cumul[2]=3, place at output[2], decrement cumul[2] to 2
Process arr[1]=2: cumul[2]=2, place at output[1], decrement cumul[2] to 1
Process arr[0]=4: cumul[4]=6, place at output[5], decrement cumul[4] to 5

Output: [1, 2, 2, 3, 3, 4, 8] ✓
```

### Why Reverse Traversal Matters (Stability)

```
If we traverse LEFT to RIGHT:
  arr = [4a, 2a, 2b, 8, 3a, 3b, 1]
  4a goes to position 5
  2a goes to position 1
  2b goes to position 2 (AFTER 2a) ✓ stable
  ...

If we traverse RIGHT to LEFT (correct for stability):
  1 goes to position 0
  3b goes to position 4
  3a goes to position 3 (BEFORE 3b) ✓ stable
  8 goes to position 6
  2b goes to position 2
  2a goes to position 1 (BEFORE 2b) ✓ stable
  4a goes to position 5

Stability: Equal elements maintain their original relative order.
This matters when sorting objects by multiple keys!
```

### Counting Sort with Negative Numbers

```python
def counting_sort_negative(arr):
    """Counting sort that handles negative numbers."""
    if not arr:
        return arr
    
    max_val = max(arr)
    min_val = min(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    output = [0] * len(arr)
    
    for num in arr:
        count[num - min_val] += 1
    
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    for i in range(len(arr) - 1, -1, -1):
        output[count[arr[i] - min_val] - 1] = arr[i]
        count[arr[i] - min_val] -= 1
    
    return output

# Example
arr = [-5, -1, -3, 0, 2, 4, 1]
print(counting_sort_negative(arr))  # [-5, -3, -1, 0, 1, 2, 4]
```

### Properties
- **Time Complexity**: O(n + k) where k = range of input
- **Space Complexity**: O(n + k)
- **Stable**: Yes
- **Best for**: Integer arrays with small range

---

## 7. Radix Sort

### How Radix Sort Works - Visual Walkthrough

Radix sort sorts numbers digit by digit, from LEAST significant to
MOST significant (LSD), using a stable sort (counting sort) at each digit.

```
arr = [170, 45, 75, 90, 802, 24, 2, 66]

ROUND 1: Sort by ONES digit
═══════════════════════════════
170 → ones=0    45 → ones=5    75 → ones=5
90  → ones=0    802 → ones=2   24 → ones=4
2   → ones=2    66 → ones=6

Bucket by ones digit:
  0: [170, 90]
  1: []
  2: [802, 2]
  3: []
  4: [24]
  5: [45, 75]    ← note: 45 before 75 (stable!)
  6: [66]
  7: []
  8: []
  9: []

After Round 1: [170, 90, 802, 2, 24, 45, 75, 66]

ROUND 2: Sort by TENS digit
═══════════════════════════════
170 → tens=7    90 → tens=9    802 → tens=0
2   → tens=0    24 → tens=2    45 → tens=4
75  → tens=7    66 → tens=6

Bucket by tens digit:
  0: [802, 2]
  1: []
  2: [24]
  3: []
  4: [45]
  5: []
  6: [66]
  7: [170, 75]   ← stable! 170 before 75
  8: []
  9: [90]

After Round 2: [802, 2, 24, 45, 66, 170, 75, 90]

ROUND 3: Sort by HUNDREDS digit
═════════════════════════════════
802 → hundreds=8    2 → hundreds=0    24 → hundreds=0
45  → hundreds=0    66 → hundreds=0   170 → hundreds=1
75  → hundreds=0    90 → hundreds=0

Bucket by hundreds digit:
  0: [2, 24, 45, 66, 75, 90]  ← all 0-hundreds, stable order
  1: [170]
  2: []
  ...
  8: [802]

After Round 3: [2, 24, 45, 66, 75, 90, 170, 802] ✓ SORTED!
```

### Why LSD (Least Significant Digit) First?

```
If we did MSD first (most significant digit first):

Round 1 (hundreds): [2, 24, 45, 66, 75, 90, 170, 802]
  Groups: {0: [2,24,45,66,75,90], 1: [170], 8: [802]}

Round 2 (tens) WITHIN group 0:
  {0: [2], 2: [24], 4: [45], 6: [66], 7: [75], 9: [90]}

This would require RECURSIVE sorting within each group.
LSD is simpler: just do n passes, each time sorting by one digit.
```

### Properties
- **Time Complexity**: O(d × (n + k)) where d = number of digits, k = base
- **Space Complexity**: O(n + k)
- **Stable**: Yes
- **Best for**: Integer arrays with many digits

---

## 8. Bucket Sort

### How Bucket Sort Works - Visual Walkthrough

Bucket sort distributes elements into "buckets", sorts each bucket,
then concatenates the results.

```
arr = [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
n = 7 elements

STEP 1: Create n empty buckets
═══════════════════════════════
Bucket: [0] [1] [2] [3] [4] [5] [6]
         ↓   ↓   ↓   ↓   ↓   ↓   ↓
        []  []  []  []  []  []  []

STEP 2: Distribute elements into buckets
══════════════════════════════════════════
Formula: bucket_idx = int(n * element)

  0.42 → int(7 * 0.42) = int(2.94) = 2 → bucket[2]
  0.32 → int(7 * 0.32) = int(2.24) = 2 → bucket[2]
  0.23 → int(7 * 0.23) = int(1.61) = 1 → bucket[1]
  0.52 → int(7 * 0.52) = int(3.64) = 3 → bucket[3]
  0.25 → int(7 * 0.25) = int(1.75) = 1 → bucket[1]
  0.47 → int(7 * 0.47) = int(3.29) = 3 → bucket[3]
  0.51 → int(7 * 0.51) = int(3.57) = 3 → bucket[3]

Bucket: [0] [1]     [2]       [3]
        [] [0.23,   [0.42,    [0.52,
            0.25]    0.32]     0.47,
                               0.51]

STEP 3: Sort each bucket (insertion sort or any sort)
═══════════════════════════════════════════════════════
Bucket[1]: [0.23, 0.25] ← already sorted
Bucket[2]: [0.32, 0.42] ← sorted
Bucket[3]: [0.47, 0.51, 0.52] ← sorted

STEP 4: Concatenate all buckets
═══════════════════════════════
Result: [] + [0.23, 0.25] + [0.32, 0.42] + [0.47, 0.51, 0.52] + []
      = [0.23, 0.25, 0.32, 0.42, 0.47, 0.51, 0.52] ✓
```

### When Bucket Sort is Fast vs Slow

```
UNIFORM DISTRIBUTION (Fast - O(n)):
  Elements spread evenly across buckets
  Each bucket has ~n/k elements
  Total work: O(n) to distribute + O(n) to sort small buckets

  Example: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  Bucket[0]: [0.1]
  Bucket[1]: [0.2]
  Bucket[2]: [0.3]
  ...each bucket has 1 element -> O(1) sort each!

SKEWED DISTRIBUTION (Slow - O(n²)):
  All elements end up in one bucket
  Degradess to whatever sort used for individual buckets

  Example: [0.01, 0.01, 0.01, 0.01, 0.01]
  ALL in bucket[0] -> O(n²) if using insertion sort
```

### Bucket Sort for Integers

```python
def bucket_sort_integers(arr, num_buckets=10):
    """Bucket sort for integers."""
    if not arr:
        return arr
    
    min_val = min(arr)
    max_val = max(arr)
    bucket_range = (max_val - min_val + 1) / num_buckets
    
    buckets = [[] for _ in range(num_buckets)]
    
    # Distribute elements
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        idx = min(idx, num_buckets - 1)  # Handle edge case
        buckets[idx].append(num)
    
    # Sort individual buckets
    for i in range(num_buckets):
        buckets[i].sort()
    
    # Concatenate
    result = []
    for bucket in buckets:
        result.extend(bucket)
    
    return result

# Example
arr = [29, 25, 3, 49, 9, 37, 21, 43]
print(bucket_sort_integers(arr))  # [3, 9, 21, 25, 29, 37, 43, 49]
```

### Properties
- **Time Complexity**: Best O(n + k), Average O(n + k), Worst O(n²)
- **Space Complexity**: O(n + k)
- **Stable**: Yes (if using stable sort for buckets)
- **Best for**: Uniformly distributed data

---

## 9. Python's Timsort

Python's built-in `sort()` and `sorted()` use **Timsort**, a hybrid of merge sort and insertion sort.

### How Timsort Works

```
TIMSORT INSIGHT: Real-world data is often PARTIALLY sorted.

Timsort finds existing sorted subsequences ("runs") and
extends them, then merges the runs together.

Example: [3, 5, 7, 1, 2, 4, 6, 8]
          ─────────  ─────────────
          run 1       run 2
          (ascending)  (ascending)

Merge the two runs:
  [3, 5, 7] + [1, 2, 4, 6, 8]
  → [1, 2, 3, 4, 5, 6, 7, 8]

If a run is too short, use INSERTION SORT to extend it.
This is why Timsort is adaptive: it's fast on nearly sorted data!
```

```python
# Timsort is built into Python
arr = [5, 2, 8, 1, 9, 3]

# In-place sort (uses Timsort)
arr.sort()
print(arr)  # [1, 2, 3, 5, 8, 9]

# Returns new sorted list (also Timsort)
arr = [5, 2, 8, 1, 9, 3]
sorted_arr = sorted(arr)
print(sorted_arr)  # [1, 2, 3, 5, 8, 9]

# Custom key function
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
students.sort(key=lambda x: x[1], reverse=True)
print(students)  # [('Bob', 92), ('Alice', 85), ('Charlie', 78)]

# Stable sort (maintains relative order of equal elements)
data = [("b", 2), ("a", 1), ("c", 2), ("d", 1)]
data.sort(key=lambda x: x[1])
print(data)  # [('a', 1), ('d', 1), ('b', 2), ('c', 2)]
             #  ↑ a before d (both key=1, maintained order)
             #  ↑ b before c (both key=2, maintained order)
```

### Why Timsort Wins in Practice

```
BEST CASE: Already sorted array
  Timsort: O(n) - finds one big run, done!
  Merge: O(n log n) - still does all the work
  Quick: O(n log n) - still partitions everything

AVERAGE CASE: Random data
  Timsort: O(n log n) - same as merge sort
  But with BETTER constants due to insertion sort on small chunks

WORST CASE: O(n log n) - guaranteed!

Timsort = Merge sort's guarantees + Insertion sort's speed on small data
        = The best of both worlds!
```

### Properties
- **Time Complexity**: Best O(n), Average O(n log n), Worst O(n log n)
- **Space Complexity**: O(n)
- **Stable**: Yes
- **Adaptive**: Yes (efficient for partially sorted data)

---

## 10. When to Use Which

| Scenario | Recommended Sort | Why |
|----------|------------------|-----|
| Small array (n < 50) | Insertion Sort | Low overhead, simple |
| Nearly sorted | Insertion Sort / Timsort | Adaptive |
| General purpose | Quick Sort / Timsort | Fast average case |
| Need stability | Merge Sort / Timsort | Stable |
| Memory constrained | Quick Sort | In-place |
| Linked list | Merge Sort | No random access needed |
| Integers with small range | Counting Sort | O(n + k) |
| Integers with many digits | Radix Sort | O(d × (n + k)) |
| Uniformly distributed | Bucket Sort | O(n + k) average |
| External sorting | Merge Sort | Disk-friendly |

---

## 11. Comparison Table

| Sort | Best | Average | Worst | Space | Stable | In-place |
|------|------|---------|-------|-------|--------|----------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No | Yes |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes |
| Counting | O(n + k) | O(n + k) | O(n + k) | O(n + k) | Yes | No |
| Radix | O(dn) | O(dn) | O(dn) | O(n + k) | Yes | No |
| Bucket | O(n + k) | O(n + k) | O(n²) | O(n + k) | Yes | No |
| Timsort | O(n) | O(n log n) | O(n log n) | O(n) | Yes | No |

---

## Key Insights

1. **Quick Sort** is fastest in practice due to cache efficiency
2. **Merge Sort** guarantees O(n log n) but uses extra space
3. **Insertion Sort** beats other sorts on small or nearly sorted data
4. **Counting/Radix/Bucket** sorts can beat comparison sorts for specific inputs
5. **Python's Timsort** is the best general-purpose sort for real-world data

---

## Visual Summary - Sorting Algorithms at a Glance

```
COMPARISON SORTS (compare elements to decide order):
═══════════════════════════════════════════════════════

O(n²) sorts:
  Bubble Sort:    Swap adjacent if wrong order, bubble up
  Selection Sort: Find min, swap to front
  Insertion Sort: Insert element into correct position

  When to use: Small arrays (n < 50) or nearly sorted data

O(n log n) sorts:
  Merge Sort:     Split in half, sort halves, merge
  Quick Sort:     Pick pivot, partition, recurse

  When to use: General purpose (Quick) or need stability (Merge)

NON-COMPARISON SORTS (don't compare elements):
═══════════════════════════════════════════════

  Counting Sort:  Count each value, place directly     O(n + k)
  Radix Sort:     Sort digit by digit using counting    O(dn)
  Bucket Sort:    Distribute to buckets, sort each      O(n + k)

  When to use: Integers with limited range, or uniform floats

HYBRID:
═══════
  Timsort: Merge sort + insertion sort = Python's default
```

### Complexity Comparison - Visual

```
For n = 1,000,000 elements:

Algorithm      Operations        Time (1 GHz)
─────────      ──────────        ────────────
Bubble O(n²)   1,000,000,000,000 ~1000 seconds
Selection O(n²) 1,000,000,000,000 ~1000 seconds
Insertion O(n²) ~500,000,000,000  ~500 seconds (if random)
Merge O(n logn) ~20,000,000      ~0.02 seconds
Quick O(n logn) ~20,000,000      ~0.02 seconds
Counting O(n+k) ~1,000,000       ~0.001 seconds (if k small)
Radix O(dn)     ~7,000,000       ~0.007 seconds

The difference between O(n²) and O(n log n) is ENORMOUS
for large inputs!
```
