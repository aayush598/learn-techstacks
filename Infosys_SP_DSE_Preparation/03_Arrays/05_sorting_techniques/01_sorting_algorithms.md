# Sorting Algorithms for Competitive Programming

> **Goal:** Understand *how* each algorithm sorts, *why* it works, and *when* to use it.
> Every algorithm below includes a visual walkthrough, complexity breakdown, and a real-world analogy.

---

## Quick Reference — Which Algorithm Should I Use?

```
                        ┌─────────────────────┐
                        │  Need to sort data?  │
                        └─────────┬───────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Is n small (n < 50)?       │
                    └──────┬──────────────┬──────┘
                      Yes  │              │  No
                           ▼              ▼
                   ┌──────────────┐  ┌──────────────────────────┐
                   │Insertion Sort│  │ Are values integers with  │
                   └──────────────┘  │ a small range (k < 10n)? │
                                     └────┬─────────────┬──────┘
                                       Yes│             │No
                                          ▼             ▼
                                  ┌──────────────┐ ┌────────────────┐
                                  │Counting Sort │ │Is data nearly  │
                                  └──────────────┘ │  sorted?       │
                                                   └──┬─────────┬──┘
                                                   Yes│         │No
                                                      ▼         ▼
                                              ┌──────────┐ ┌────────────┐
                                              │  Tim Sort │ │ Quick Sort  │
                                              │ (built-in)│ │ /  Merge    │
                                              └──────────┘ └────────────┘
```

**In competitive programming, 99% of the time `arr.sort()` (Tim Sort) is the right choice.** Learn the others for interviews and when the problem specifically requires a particular algorithm.

---

## 1. Bubble Sort

### Analogy
Imagine bubbles rising in water — the largest element "bubbles up" to its correct position at the end in each pass. Just like heavy bubbles rise to the surface, large values float to the right.

### How It Works (Visual Walkthrough)

```
Input: [5, 3, 8, 1, 2]

Pass 1 (bubble up the largest = 8):
  [5, 3, 8, 1, 2]   compare 5,3 → swap
  [3, 5, 8, 1, 2]   compare 5,8 → ok
  [3, 5, 8, 1, 2]   compare 8,1 → swap
  [3, 5, 1, 8, 2]   compare 8,2 → swap
  [3, 5, 1, 2, 8]   ← 8 is now in final position ✓

Pass 2 (bubble up the next largest = 5):
  [3, 5, 1, 2, 8]   compare 3,5 → ok
  [3, 5, 1, 2, 8]   compare 5,1 → swap
  [3, 1, 5, 2, 8]   compare 5,2 → swap
  [3, 1, 2, 5, 8]   ← 5,8 in final position ✓

Pass 3 (bubble up = 3):
  [3, 1, 2, 5, 8]   compare 3,1 → swap
  [1, 3, 2, 5, 8]   compare 3,2 → swap
  [1, 2, 3, 5, 8]   ← 3,5,8 in final position ✓

Pass 4 (check = no swaps → STOP early!)
  [1, 2, 3, 5, 8]   ← already sorted, break!

Result: [1, 2, 3, 5, 8] ✓
```

### The `swapped` Optimization

```
Without optimization: Always does n passes     → O(n²) even if sorted
With swapped flag:    Stops when no swaps done → O(n)  if already sorted

    ┌─────────────────────────────────────────┐
    │  If no element was swapped in a pass,   │
    │  the array is already sorted — STOP!    │
    └─────────────────────────────────────────┘
```

### Annotated Code

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):                     # Each pass bubbles one element
        swapped = False                    # Track if any swap happened
        for j in range(n - 1 - i):         # Last i elements are already sorted
            if arr[j] > arr[j + 1]:        # Compare adjacent elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]  # Swap if out of order
                swapped = True             # Mark that a swap occurred
        if not swapped:                    # No swaps = array is sorted
            break                          # Early termination!
    return arr
# Time: O(n²) worst, O(n) best (already sorted)
# Space: O(1) — in-place
# Stable: Yes — equal elements keep their relative order
# Use: Nearly sorted data, educational purposes, tiny arrays
```

### Complexity Breakdown

| Case       | Swaps per pass | Passes | Total        | When?           |
|------------|----------------|--------|--------------|-----------------|
| Best       | 0              | 1      | **O(n)**     | Already sorted  |
| Average    | ~n/2           | n      | **O(n²)**    | Random order    |
| Worst      | n-1            | n      | **O(n²)**    | Reverse sorted  |

---

## 2. Selection Sort

### Analogy
Like sorting playing cards in your hand — you scan through all the remaining cards, find the smallest one, and place it at the beginning. You never move a card once it's placed.

### How It Works (Visual Walkthrough)

```
Input: [5, 3, 8, 1, 2]

Pass 1: Find minimum in [5,3,8,1,2] → min=1 at index 3
  [5, 3, 8, 1, 2]   scan from index 0 → min=5
                     scan from index 1 → min=3
                     scan from index 2 → min=3
                     scan from index 3 → min=1  ← found!
                     scan from index 4 → min=1
  Swap index 0 and index 3:
  [1, 3, 8, 5, 2]   ← 1 in final position ✓

Pass 2: Find minimum in [_, 3, 8, 5, 2] → min=2 at index 4
  [1, 3, 8, 5, 2]   scan from index 1 → min=3
                     scan from index 2 → min=3
                     scan from index 3 → min=3
                     scan from index 4 → min=2  ← found!
  Swap index 1 and index 4:
  [1, 2, 8, 5, 3]   ← 1,2 in final position ✓

Pass 3: Find minimum in [_, _, 8, 5, 3] → min=3 at index 4
  [1, 2, 8, 5, 3]   scan from index 2 → min=8
                     scan from index 3 → min=5
                     scan from index 4 → min=3  ← found!
  Swap index 2 and index 4:
  [1, 2, 3, 5, 8]   ← 1,2,3 in final position ✓

Pass 4: Find minimum in [_, _, _, 5, 8] → min=5 at index 3
  No swap needed (already in place)

Result: [1, 2, 3, 5, 8] ✓
```

### Key Insight: Minimum Swaps

```
Selection Sort ALWAYS makes exactly (n-1) swaps — the fewest possible!
This is important when WRITES are expensive (e.g., flash memory, EEPROM)

    Bubble Sort:    up to n*(n-1)/2 swaps  (terrible for writes)
    Selection Sort: exactly n-1 swaps       (optimal for writes)
```

### Annotated Code

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):                     # Place one element at a time
        min_idx = i                        # Assume current position has minimum
        for j in range(i + 1, n):          # Scan remaining unsorted portion
            if arr[j] < arr[min_idx]:      # Found a smaller element?
                min_idx = j                # Update minimum index
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # Place minimum at position i
    return arr
# Time: O(n²) always — no best case! (always scans full remaining array)
# Space: O(1) — in-place
# Stable: No — swapping can change relative order of equal elements
#         (Can be made stable with O(n) extra space)
# Use: When memory writes are expensive, when you need exactly n-1 swaps
```

### Why Selection Sort is NOT Stable (Counter-Example)

```
Input:  [(5,a), (3,b), (5,c), (1,d)]
         ↑               ↑
         These two 5s have a specific order: (5,a) before (5,c)

After pass 1 (min=1 at index 3):
  [(1,d), (3,b), (5,c), (5,a)]   ← (5,a) moved AFTER (5,c)!
                                      Stability broken!
```

---

## 3. Insertion Sort

### Analogy
Like sorting a hand of cards — you pick up one card at a time and slide it into its correct position among the already-sorted cards to the left.

### How It Works (Visual Walkthrough)

```
Input: [5, 3, 8, 1, 2]

Start: [5 | 3, 8, 1, 2]
        ↑ sorted  ↑ unsorted

Step 1: key=3, insert into [5]
  [5, 3, 8, 1, 2]   3 < 5, so shift 5 right
  [5, 5, 8, 1, 2]
  [3, 5, 8, 1, 2]   ← insert 3 at position 0

Step 2: key=8, insert into [3, 5]
  [3, 5, 8, 1, 2]   8 > 5, no shifting needed
  [3, 5, 8, 1, 2]   ← 8 stays at position 2

Step 3: key=1, insert into [3, 5, 8]
  [3, 5, 8, 1, 2]   1 < 8, shift 8 right
  [3, 5, 8, 8, 2]
  [3, 5, 5, 8, 2]   1 < 5, shift 5 right
  [3, 5, 5, 8, 2]
  [3, 3, 5, 8, 2]   1 < 3, shift 3 right
  [3, 3, 5, 8, 2]
  [1, 3, 5, 8, 2]   ← insert 1 at position 0

Step 4: key=2, insert into [1, 3, 5, 8]
  [1, 3, 5, 8, 2]   2 < 8, shift 8 right
  [1, 3, 5, 8, 8]
  [1, 3, 5, 5, 8]   2 < 5, shift 5 right
  [1, 3, 5, 5, 8]
  [1, 3, 3, 5, 8]   2 < 3, shift 3 right
  [1, 3, 3, 5, 8]
  [1, 2, 3, 5, 8]   ← insert 2 at position 1

Result: [1, 2, 3, 5, 8] ✓
```

### Annotated Code

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):            # Start from 2nd element
        key = arr[i]                        # Element to be inserted
        j = i - 1                           # Start comparing with element to the left

        # Shift elements of sorted portion that are greater than key
        while j >= 0 and arr[j] > key:      # While element to the left is bigger
            arr[j + 1] = arr[j]             # Shift it one position to the right
            j -= 1                          # Move to the next element on the left

        arr[j + 1] = key                    # Insert key in its correct position
    return arr
# Time: O(n²) worst, O(n) best (already sorted)
# Space: O(1) — in-place
# Stable: Yes
# Use: Small arrays (n < 50), nearly sorted data, online sorting
#      (elements arrive one at a time)
```

### Why Insertion Sort Wins on Small Arrays

```
For n < ~50, Insertion Sort beats Quick Sort and Merge Sort:

    Quick Sort overhead: function calls, pivot selection, partitioning
    Insertion Sort:      simple comparisons and shifts, no overhead

    ┌──────────────────────────────────────────┐
    │  n=10: Insertion ~25 ops vs Quick ~40 ops │
    │  n=50: Insertion ~1250 ops vs Quick ~500  │
    │  n=100: Insertion ~5000 ops vs Quick ~700 │
    │                                           │
    │  Hybrid sorts (TimSort, IntroSort) use    │
    │  Insertion Sort for small subarrays!       │
    └──────────────────────────────────────────┘
```

---

## 4. Merge Sort

### Analogy
Like the game of dividing a deck of cards in half, sorting each half separately, then merging two sorted halves back together. This is "divide and conquer" — you keep splitting until each pile has one card, then merge upward.

### How It Works (Visual Walkthrough)

```
Input: [5, 3, 8, 1, 2]

DIVIDE PHASE (split until single elements):

                    [5, 3, 8, 1, 2]
                   /                \
            [5, 3, 8]              [1, 2]
           /        \             /      \
        [5, 3]      [8]        [1]      [2]
       /      \
    [5]      [3]


MERGE PHASE (combine sorted halves):

    [5]    [3]     → merge →     [3, 5]
       \      /
        [3, 5]      [8]    → merge →    [3, 5, 8]
            \          /
             [3, 5, 8]      [1]    [2]  → merge → [1, 2]
                                 \        /
                                  [1, 2]
                   \              /
                    [1, 2, 3, 5, 8]

Result: [1, 2, 3, 5, 8] ✓
```

### Detailed Merge Step

```
Merging [3, 5, 8] and [1, 2]:

  left=[3,5,8]  right=[1,2]  result=[]

  Compare 3 vs 1 → 1 is smaller → result=[1]
  Compare 3 vs 2 → 2 is smaller → result=[1,2]
  right exhausted → copy rest of left → result=[1,2,3,5,8]
```

### Annotated Code — Recursive

```python
def merge_sort(arr):
    if len(arr) <= 1:                       # Base case: already sorted
        return arr

    mid = len(arr) // 2                     # Find the middle point
    left = merge_sort(arr[:mid])            # Recursively sort left half
    right = merge_sort(arr[mid:])           # Recursively sort right half
    return merge(left, right)               # Merge two sorted halves

def merge(left, right):
    result = []                             # Result array
    i = j = 0                               # Pointers for left and right

    # Compare elements from both arrays, pick the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:             # <= ensures stability
            result.append(left[i])          # Take from left
            i += 1
        else:
            result.append(right[j])         # Take from right
            j += 1

    # One array is exhausted, copy remaining elements
    result.extend(left[i:])                 # Remaining left elements
    result.extend(right[j:])               # Remaining right elements
    return result
# Time: O(n log n) ALWAYS — no worst case!
# Space: O(n) — needs extra array
# Stable: Yes
# Use: Guaranteed O(n log n), linked lists, external sorting, stability needed
```

### Annotated Code — In-Place (CP Template)

```python
def merge_sort_inplace(arr, left, right):
    if left < right:                        # More than one element
        mid = (left + right) // 2           # Find middle
        merge_sort_inplace(arr, left, mid)      # Sort left half
        merge_sort_inplace(arr, mid + 1, right) # Sort right half
        merge_arr(arr, left, mid, right)        # Merge in-place

def merge_arr(arr, left, mid, right):
    # Copy to temporary arrays
    left_arr = arr[left:mid + 1]            # Left subarray
    right_arr = arr[mid + 1:right + 1]      # Right subarray

    i = j = 0                               # Pointers for temp arrays
    k = left                                # Pointer for main array

    # Merge back into main array
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] <= right_arr[j]:     # <= for stability
            arr[k] = left_arr[i]            # Take from left
            i += 1
        else:
            arr[k] = right_arr[j]           # Take from right
            j += 1
        k += 1

    # Copy remaining elements
    while i < len(left_arr):                # Leftover from left
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < len(right_arr):              # Leftover from right
        arr[k] = right_arr[j]
        j += 1
        k += 1

# Usage: merge_sort_inplace(arr, 0, len(arr) - 1)
```

### Why Merge Sort is O(n log n) Always

```
Splitting:  n → n/2 → n/4 → ... → 1    (log n levels)
Merging:    Each level processes all n elements (n comparisons)
Total:      n × log n = O(n log n)      ← SAME for best, average, worst!

    Level 0:  [5, 3, 8, 1, 2]                    ← n elements
    Level 1:  [5, 3, 8] [1, 2]                   ← n elements total
    Level 2:  [5, 3] [8] [1] [2]                 ← n elements total
    Level 3:  [5] [3] [8] [1] [2]                ← n elements total
    Merge 3→ [3,5] [8] [1] [2]                   ← n comparisons
    Merge 2→ [3,5,8] [1,2]                       ← n comparisons
    Merge 1→ [1,2,3,5,8]                         ← n comparisons
              ─────────────────
              log(n) levels × n = n log n
```

---

## 5. Quick Sort

### Analogy
Like organizing a bookshelf by picking one book as a "pivot" — books shorter than the pivot go to the left, taller ones go to the right, then you sort each side. It's fast because you avoid comparing every pair.

### Lomuto Partition (Visual Walkthrough)

```
Input: [5, 3, 8, 1, 2]    pivot = last element = 2

Partition step-by-step:

  pivot=2, i=-1

  j=0: arr[0]=5 > 2 → skip
  j=1: arr[1]=3 > 2 → skip
  j=2: arr[2]=8 > 2 → skip
  j=3: arr[3]=1 ≤ 2 → i=0, swap arr[0] and arr[3]

  [1, 3, 8, 5, 2]   i=0

  After loop: swap arr[i+1] and arr[high]
  [1, 2, 8, 5, 3]   pivot=2 is now at index 1

  Left of pivot: [1]     → all ≤ 2 ✓
  Right of pivot: [8,5,3] → all > 2 ✓

  Recursively sort [1] → [1] (trivial)
  Recursively sort [8,5,3]:
    pivot=3, partition → [3,5,8]
    Recursively sort [3] → [3]
    Recursively sort [5,8] → already sorted

Result: [1, 2, 3, 5, 8] ✓
```

### Hoare Partition (Visual Walkthrough)

```
Input: [5, 3, 8, 1, 2]    pivot = first element = 5

  i=-1, j=5

  i moves right until arr[i] ≥ 5:  i=0 (arr[0]=5)
  j moves left until arr[j] ≤ 5:  j=3 (arr[3]=1)

  Swap: [1, 3, 8, 5, 2]   i=0, j=3

  i moves right: i=2 (arr[2]=8 ≥ 5)
  j moves left:  j=1 (arr[1]=3 ≤ 5)

  Swap: [1, 3, 8, 5, 2]   i=2, j=1

  i ≥ j → return j=1

  Left:  [1, 3]    Right: [8, 5, 2]
  (Note: pivot 5 is in the RIGHT partition)

  Hoare makes ~n/3 swaps on average (vs ~n in Lomuto)
```

### Annotated Code — Lomuto Partition

```python
def quicksort_lomuto(arr, low, high):
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)  # Partition around pivot
        quicksort_lomuto(arr, low, pivot_idx - 1)     # Sort left part
        quicksort_lomuto(arr, pivot_idx + 1, high)     # Sort right part

def partition_lomuto(arr, low, high):
    pivot = arr[high]                       # Choose last element as pivot
    i = low - 1                             # i tracks the boundary of elements ≤ pivot

    for j in range(low, high):              # Scan from low to high-1
        if arr[j] <= pivot:                 # Element belongs in left part
            i += 1                          # Expand the boundary
            arr[i], arr[j] = arr[j], arr[i] # Swap element into left part

    # Place pivot in its correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1                            # Return pivot's final index
```

### Annotated Code — Hoare Partition

```python
def quicksort_hoare(arr, low, high):
    if low < high:
        p = partition_hoare(arr, low, high)  # Find partition point
        quicksort_hoare(arr, low, p)          # Sort left (includes partition point)
        quicksort_hoare(arr, p + 1, high)     # Sort right

def partition_hoare(arr, low, high):
    pivot = arr[low]                        # Choose first element as pivot
    i = low - 1                             # Left pointer (starts before array)
    j = high + 1                            # Right pointer (starts after array)

    while True:
        i += 1                              # Move right until arr[i] >= pivot
        while arr[i] < pivot:
            i += 1

        j -= 1                              # Move left until arr[j] <= pivot
        while arr[j] > pivot:
            j -= 1

        if i >= j:                          # Pointers crossed — done
            return j

        arr[i], arr[j] = arr[j], arr[i]    # Swap out-of-place elements
    return j
```

### Randomized Quick Sort (Best for CP)

```python
def quicksort_random(arr, low, high):
    import random
    if low < high:
        # Randomly choose pivot and move it to end
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        p = partition_lomuto(arr, low, high)  # Partition as usual
        quicksort_random(arr, low, p - 1)     # Sort left
        quicksort_random(arr, p + 1, high)     # Sort right

# Why random pivot?
# ┌─────────────────────────────────────────────────────────┐
# │ Worst case O(n²) happens with already-sorted input     │
# │ and bad pivot choices (first/last element).             │
# │ Random pivot makes worst case概率 ≈ 0                   │
# │ Expected time: O(n log n) with high probability         │
# └─────────────────────────────────────────────────────────┘
```

### Quick Sort vs Merge Sort

```
┌──────────────────┬───────────────────┬────────────────────┐
│                  │   Quick Sort       │   Merge Sort        │
├──────────────────┼───────────────────┼────────────────────┤
│ Best case        │ O(n log n)         │ O(n log n)          │
│ Average case     │ O(n log n)         │ O(n log n)          │
│ Worst case       │ O(n²) ← BAD!      │ O(n log n) ← SAFE   │
│ Space            │ O(log n) ← BETTER │ O(n) ← WORSE        │
│ Stable           │ No                │ Yes                 │
│ In-place         │ Yes               │ No (needs temp)     │
│ Cache friendly   │ Yes ← BETTER      │ No                  │
│ Practical speed  │ Fastest in practice│ Guaranteed          │
└──────────────────┴───────────────────┴────────────────────┘
```

---

## 6. Counting Sort

### Analogy
Like a teacher counting exam scores — instead of comparing scores, you make a tally sheet (count array) for each possible score, then read out the tally. No comparisons needed!

### How It Works (Visual Walkthrough)

```
Input: [4, 2, 2, 8, 3, 3, 1]
min=1, max=8, range=8

Step 1: Count occurrences
  Value:  1  2  3  4  5  6  7  8
  Count: [1, 2, 2, 1, 0, 0, 0, 1]
           ↑  ↑  ↑  ↑              ↑
          one two two one          one

Step 2: Cumulative count (prefix sum)
  Count: [1, 3, 5, 6, 6, 6, 6, 7]
           ↑  ↑  ↑  ↑
          1  1+2 1+2+2 1+2+2+1

Step 3: Build result (traverse BACKWARDS for stability)
  arr[6]=1 → count[0]=1, place at index 0 → count[0]=0
  arr[5]=3 → count[2]=5, place at index 4 → count[2]=4
  arr[4]=3 → count[2]=4, place at index 3 → count[2]=3
  arr[3]=8 → count[7]=7, place at index 6 → count[7]=6
  arr[2]=2 → count[1]=3, place at index 2 → count[1]=2
  arr[1]=2 → count[1]=2, place at index 1 → count[1]=1
  arr[0]=4 → count[3]=6, place at index 5 → count[3]=5

Result: [1, 2, 2, 3, 3, 4, 8] ✓
```

### Why Traverse Backwards?

```
Stability = equal elements maintain their original relative order

  arr = [(4,a), (2,b), (2,c), (8,d), (3,e), (3,f), (1,g)]

  Backwards traversal:  (2,c) placed at index 2, (2,b) at index 1
  → (2,b) comes before (2,c) in result → STABLE ✓

  Forwards traversal:   (2,b) placed at index 2, (2,c) at index 1
  → (2,c) comes before (2,b) in result → UNSTABLE ✗
```

### Annotated Code

```python
def counting_sort(arr):
    if not arr:
        return arr

    min_val, max_val = min(arr), max(arr)   # Find range
    range_val = max_val - min_val + 1

    # Step 1: Count occurrences
    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1           # Offset by min_val for negative numbers

    # Step 2: Cumulative count (prefix sum)
    for i in range(1, range_val):
        count[i] += count[i - 1]           # Each position = count of elements ≤ it

    # Step 3: Build result (backwards for stability)
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):  # Traverse input BACKWARDS
        count[arr[i] - min_val] -= 1        # Decrement count
        result[count[arr[i] - min_val]] = arr[i]  # Place at correct position

    return result
# Time: O(n + k) where k = range of values
# Space: O(n + k)
# Stable: Yes
# Use: Small range of integer values (k << n²)
#      Also used as subroutine inside Radix Sort
```

### When Counting Sort is Optimal

```
┌─────────────────────────────────────────────────────────┐
│  Counting Sort beats comparison sorts when:             │
│                                                         │
│    k (range) is small relative to n²                    │
│                                                         │
│  Example:                                               │
│    n = 1,000,000 elements, range = 0 to 999             │
│    Comparison sort: O(n log n) ≈ 20,000,000 ops         │
│    Counting sort:   O(n + k)  ≈  1,001,000 ops  ← 20x! │
│                                                         │
│  But if range = 0 to 10^9:                              │
│    Counting sort: O(n + 10^9) → TOO MUCH MEMORY!        │
│    Use Radix Sort instead (O(d*n))                      │
└─────────────────────────────────────────────────────────┘
```

---

## 7. Radix Sort

### Analogy
Like sorting a deck of cards by first grouping by suit (least significant), then sorting within each suit by number. You process one digit at a time, from least significant to most significant, using a stable sort (Counting Sort) at each step.

### How It Works (Visual Walkthrough)

```
Input: [170, 45, 75, 90, 802, 24, 2, 66]

Pass 1 — Sort by Ones digit (exp=1):
  [170, 45, 75, 90, 802, 24, 2, 66]
   0    5   5   0    2   4   2   6
  → [170, 90, 802, 2, 24, 45, 75, 66]

Pass 2 — Sort by Tens digit (exp=10):
  [170, 90, 802, 2, 24, 45, 75, 66]
   7    9   0   0   2   4   7   6
  → [802, 2, 24, 45, 66, 170, 75, 90]

Pass 3 — Sort by Hundreds digit (exp=100):
  [802, 2, 24, 45, 66, 170, 75, 90]
   8    0   0   0   0   1   0   0
  → [2, 24, 45, 66, 75, 90, 170, 802]

Result: [2, 24, 45, 66, 75, 90, 170, 802] ✓
```

### Why Least Significant Digit First?

```
If we sorted by MOST significant digit first:
  [802, 2, 24, 45, 66, 170, 75, 90]
  Then within each group by next digit...
  → The groups might not be equal size, causing uneven work

By sorting LEAST significant first with a STABLE sort:
  Each pass preserves the order from previous passes
  → When we process the next digit, previous ordering is maintained

  This is the KEY insight: stable sort + digit-by-digit = correct result
```

### Annotated Code

```python
def radix_sort(arr):
    if not arr:
        return arr

    max_val = max(arr)                      # Find the maximum number
    exp = 1                                 # Current digit position (1s, 10s, 100s...)

    # Process each digit position
    while max_val // exp > 0:               # While there are digits left
        counting_sort_by_digit(arr, exp)    # Sort by current digit
        exp *= 10                           # Move to next digit position

    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10                        # Only 10 possible digits (0-9)

    # Count occurrences of each digit
    for num in arr:
        idx = (num // exp) % 10            # Extract digit at position exp
        count[idx] += 1

    # Cumulative count
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build output (backwards for stability)
    for i in range(n - 1, -1, -1):
        idx = (arr[i] // exp) % 10         # Extract digit again
        count[idx] -= 1
        output[count[idx]] = arr[i]

    # Copy back to original array
    for i in range(n):
        arr[i] = output[i]

# Time: O(d × (n + k)) where d = number of digits, k = 10 (base)
# Space: O(n + k)
# Stable: Yes
# Use: When range is large but number of digits is small
#      Example: Sort 1,000,000 numbers with values 0 to 999,999
#      d=6, so O(6n) = O(n) — faster than O(n log n)!
```

---

## 8. Bucket Sort

### Analogy
Like sorting coins by denomination — you put all pennies in one bucket, nickels in another, dimes in another, then sort within each bucket. If the data is evenly distributed, most buckets will have about the same number of items.

### How It Works (Visual Walkthrough)

```
Input: [0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51]
Range: 0.23 to 0.52, using 5 buckets

Step 1: Distribute into buckets (value * num_buckets)
  Bucket 0 (0.20-0.29): [0.23, 0.25]
  Bucket 1 (0.30-0.39): [0.32]
  Bucket 2 (0.40-0.49): [0.42, 0.47]
  Bucket 3 (0.50-0.59): [0.52, 0.51]
  Bucket 4 (0.60+):     []

Step 2: Sort each bucket
  Bucket 0: [0.23, 0.25]  (already sorted)
  Bucket 1: [0.32]        (single element)
  Bucket 2: [0.42, 0.47]  (already sorted)
  Bucket 3: [0.51, 0.52]  (sorted)
  Bucket 4: []

Step 3: Concatenate buckets
  [0.23, 0.25, 0.32, 0.42, 0.47, 0.51, 0.52] ✓
```

### Annotated Code

```python
def bucket_sort(arr, num_buckets=10):
    if not arr:
        return arr

    min_val, max_val = min(arr), max(arr)
    # Calculate range per bucket
    bucket_range = (max_val - min_val) / num_buckets + 1

    # Create empty buckets
    buckets = [[] for _ in range(num_buckets)]

    # Distribute elements into buckets
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        buckets[idx].append(num)

    # Sort each bucket and concatenate
    result = []
    for bucket in buckets:
        bucket.sort()                       # Use any sort (Insertion for small)
        result.extend(bucket)

    return result
# Time: O(n + k) average (uniform distribution), O(n²) worst
# Space: O(n + k)
# Stable: Depends on the inner sort used
# Use: Uniformly distributed data, floating-point numbers
```

### When Bucket Sort Fails

```
If data is NOT uniformly distributed:
  Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10000]
  Bucket 0 (0-999):     [1,2,3,4,5,6,7,8,9]     ← most items
  Bucket 1 (1000-1999): []
  ...
  Bucket 9 (9000+):     [10000]

  → Degenerates to sorting one bucket with almost all elements
  → Worst case: O(n²) if all elements in one bucket

  ┌────────────────────────────────────────────────┐
  │ Bucket Sort: GREAT for uniform data            │
  │            TERRIBLE for skewed data             │
  │ Use Counting Sort or Radix Sort for integers    │
  └────────────────────────────────────────────────┘
```

---

## 9. Tim Sort (Python's Built-in)

### Analogy
Like a smart librarian who notices some shelves are already organized (natural "runs") and only sorts the messy parts. Tim Sort combines the best of Merge Sort and Insertion Sort.

### How Tim Sort Works

```
Step 1: Find natural runs (already sorted subsequences)
  Input: [4, 8, 12, 15, 3, 7, 11, 14, 2, 6, 10, 13]
          ───────────────────  ← run 1 (ascending)
                            ───────────────────  ← run 2 (ascending)

Step 2: Extend runs to minimum run size (~32-64)
  If a run is too short, pad it with Insertion Sort

Step 3: Merge runs using modified merge (like Merge Sort)
  Merge run 1 and run 2 → sorted result
```

### Python Usage

```python
# Python's sorted() and list.sort() use Tim Sort
# It's a hybrid of Merge Sort and Insertion Sort

arr = [5, 2, 8, 1, 9]
arr.sort()           # In-place sort (modifies original)
result = sorted(arr) # Returns new sorted list (original unchanged)

# Custom key — sort by a derived value
arr.sort(key=lambda x: -x)              # Descending order
arr.sort(key=lambda x: (x % 10, x))     # Sort by last digit, then value

# Custom comparator (Python 3 requires cmp_to_key wrapper)
from functools import cmp_to_key
arr.sort(key=cmp_to_key(lambda a, b: a - b))  # Ascending
arr.sort(key=cmp_to_key(lambda a, b: b - a))  # Descending

# Sorting tuples — sorts by first element, then second, etc.
pairs = [(1, 'b'), (2, 'a'), (1, 'a')]
pairs.sort(key=lambda x: (x[0], x[1]))
# [(1, 'a'), (1, 'b'), (2, 'a')]
# Time: O(n log n) guaranteed
# Space: O(n)
# Stable: Yes
```

---

## Sorting with Custom Key

### Common Patterns

```python
# Sort by absolute value
arr = [-3, 1, -4, 1, 5]
arr.sort(key=lambda x: abs(x))
# [-3, 1, 1, -4, 5]  (sorted by |x|)

# Sort by frequency (least frequent first)
from collections import Counter
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
freq = Counter(arr)  # {3:1, 1:2, 4:1, 5:2, 9:1, 2:1, 6:1}
arr.sort(key=lambda x: (freq[x], -x))
# Sort by frequency ascending, then by value descending within same freq

# Sort strings by length
words = ["apple", "hi", "banana", "ok"]
words.sort(key=len)
# ['hi', 'ok', 'apple', 'banana']

# Sort with operator.itemgetter (faster than lambda for simple cases)
from operator import itemgetter
data = [(1, 'c'), (2, 'a'), (1, 'b')]
data.sort(key=itemgetter(0, 1))  # Sort by index 0, then index 1
# [(1, 'b'), (1, 'c'), (2, 'a')]
```

### Visual: Multi-Level Sorting

```
Sorting students by (grade DESC, name ASC):

  Input:  [("Alice", "B"), ("Bob", "A"), ("Charlie", "B"), ("Dave", "A")]

  Step 1: Sort by grade ASC (then we reverse)
  Step 2: Within same grade, sort by name ASC

  Result: [("Bob", "A"), ("Dave", "A"), ("Alice", "B"), ("Charlie", "B")]
           ────────────────────  ──────────────────────────────
           Grade A, alphabetical  Grade B, alphabetical
```

---

## Sorting Tricks for CP

```python
# 1. Sort only part of array (useful for partial operations)
arr = [5, 3, 8, 1, 9, 2]
arr[1:4] = sorted(arr[1:4])  # Sort only indices 1 to 3
# [5, 1, 3, 8, 9, 2]

# 2. Stable sort preserves order of equal elements
# Use for multi-level sorting WITHOUT tuples (saves time):
#   First sort by secondary key, then sort by primary key (stable)

# 3. argsort — get indices that would sort the array
arr = [3, 1, 4, 1, 5]
indices = sorted(range(len(arr)), key=lambda i: arr[i])
# indices = [1, 3, 0, 2, 4]  (positions of sorted elements)

# 4. Sort and deduplicate in one step
arr = [3, 1, 4, 1, 5, 3, 4]
unique_sorted = sorted(set(arr))  # [1, 3, 4, 5]

# 5. Find kth smallest without full sort — O(n log k)
import heapq
kth = heapq.nsmallest(k, arr)[-1]  # Get k smallest, pick the last

# 6. Top k elements without full sort — O(n log k)
top_k = heapq.nlargest(k, arr)     # Get k largest elements
```

---

## Complete Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable | In-Place | When to Use |
|-----------|------|---------|-------|-------|--------|----------|-------------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Nearly sorted, tiny arrays |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No | Yes | Minimize write operations |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes | Yes | Small arrays (n<50), online |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | No | Guaranteed performance, stability |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No | Yes | General purpose, fastest in practice |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(n+k) | Yes | No | Small integer range (k << n²) |
| Radix | O(dn) | O(dn) | O(dn) | O(n+k) | Yes | No | Large range, small digit count |
| Bucket | O(n+k) | O(n+k) | O(n²) | O(n+k) | Depends | No | Uniformly distributed data |
| Tim Sort | O(n) | O(n log n) | O(n log n) | O(n) | Yes | No | **Use this in CP!** |

---

## Interview/CP Decision Flowchart

```
  ┌─────────────────────────────────────────────────┐
  │          What constraint does the problem        │
  │               give about time?                   │
  └──────────────────┬──────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    O(n log n)    O(n)        O(n²) ok
         │           │           │
    ┌────▼────┐  ┌───▼───┐  ┌───▼──────────┐
    │Use built│  │What?  │  │Any O(n²) sort │
    │arr.sort()│  └───┬───┘  │works (Insert  │
    └─────────┘      │      │for small n)   │
         │     ┌─────┼─────┐└───────────────┘
         │     ▼     ▼     ▼
         │  Counting Radix Bucket
         │  (small   (large  (uniform
         │  range)   range)  data)
         │
    ┌────▼──────────────┐
    │ Need stability?   │
    │  Yes → Merge Sort │
    │  No  → Quick Sort │
    └───────────────────┘
```

**For CP:** Use Python's built-in `sort()` (Tim Sort) unless specifically asked to implement another algorithm.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Early termination
            break
    return arr
# Time: O(n²) worst, O(n) best (already sorted)
# Space: O(1)
# Stable: Yes
# Use: Nearly sorted data, educational purposes
```

---

## 2. Selection Sort

```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
# Time: O(n²) always
# Space: O(1)
# Stable: No (can be made stable)
# Use: When memory writes are expensive (minimizes swaps)
```

---

## 3. Insertion Sort

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
# Time: O(n²) worst, O(n) best
# Space: O(1)
# Stable: Yes
# Use: Small arrays (n < 50), nearly sorted data, online sorting
```

---

## 4. Merge Sort

### Recursive

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
# Time: O(n log n) always
# Space: O(n)
# Stable: Yes
# Use: Guaranteed O(n log n), linked lists, external sorting
```

### In-Place Merge Sort (for CP)

```python
def merge_sort_inplace(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)
        merge_arr(arr, left, mid, right)

def merge_arr(arr, left, mid, right):
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

# Usage: merge_sort_inplace(arr, 0, len(arr) - 1)
```

---

## 5. Quick Sort

### Lomuto Partition

```python
def quicksort_lomuto(arr, low, high):
    if low < high:
        pivot_idx = partition_lomuto(arr, low, high)
        quicksort_lomuto(arr, low, pivot_idx - 1)
        quicksort_lomuto(arr, pivot_idx + 1, high)

def partition_lomuto(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### Hoare Partition (Fewer Swaps)

```python
def quicksort_hoare(arr, low, high):
    if low < high:
        p = partition_hoare(arr, low, high)
        quicksort_hoare(arr, low, p)
        quicksort_hoare(arr, p + 1, high)

def partition_hoare(arr, low, high):
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
    return j

# Quick Sort: O(n²) worst, O(n log n) average
# Space: O(log n) average (recursion stack)
# Stable: No
# Use: General purpose, fastest in practice
# For CP: Use random pivot to avoid worst case

def quicksort_random(arr, low, high):
    import random
    if low < high:
        pivot_idx = random.randint(low, high)
        arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]
        p = partition_lomuto(arr, low, high)
        quicksort_random(arr, low, p - 1)
        quicksort_random(arr, p + 1, high)
```

---

## 6. Counting Sort

```python
def counting_sort(arr):
    if not arr:
        return arr
    min_val, max_val = min(arr), max(arr)
    range_val = max_val - min_val + 1
    
    count = [0] * range_val
    for num in arr:
        count[num - min_val] += 1
    
    # Cumulative count
    for i in range(1, range_val):
        count[i] += count[i - 1]
    
    # Build result (traverse backwards for stability)
    result = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        count[arr[i] - min_val] -= 1
        result[count[arr[i] - min_val]] = arr[i]
    
    return result
# Time: O(n + k) where k = range of values
# Space: O(n + k)
# Stable: Yes
# Use: Small range of integer values
```

---

## 7. Radix Sort

```python
def radix_sort(arr):
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    
    while max_val // exp > 0:
        counting_sort_by_digit(arr, exp)
        exp *= 10
    
    return arr

def counting_sort_by_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    
    for num in arr:
        idx = (num // exp) % 10
        count[idx] += 1
    
    for i in range(1, 10):
        count[i] += count[i - 1]
    
    for i in range(n - 1, -1, -1):
        idx = (arr[i] // exp) % 10
        count[idx] -= 1
        output[count[idx]] = arr[i]
    
    for i in range(n):
        arr[i] = output[i]

# Time: O(d * (n + k)) where d = digits, k = 10
# Space: O(n + k)
# Stable: Yes
# Use: When range is large but number of digits is small
```

---

## 8. Bucket Sort

```python
def bucket_sort(arr, num_buckets=10):
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    bucket_range = (max_val - min_val) / num_buckets + 1
    
    buckets = [[] for _ in range(num_buckets)]
    
    for num in arr:
        idx = int((num - min_val) / bucket_range)
        buckets[idx].append(num)
    
    result = []
    for bucket in buckets:
        bucket.sort()  # Use insertion sort or any sort
        result.extend(bucket)
    
    return result
# Time: O(n + k) average, O(n²) worst
# Space: O(n + k)
# Stable: Depends on inner sort
# Use: Uniformly distributed data
```

---

## 9. Tim Sort (Python's Built-in)

```python
# Python's sorted() and list.sort() use Tim Sort
# It's a hybrid of Merge Sort and Insertion Sort

arr = [5, 2, 8, 1, 9]
arr.sort()           # In-place
result = sorted(arr) # Returns new list

# Custom key
arr.sort(key=lambda x: -x)  # Descending
arr.sort(key=lambda x: (x % 10, x))  # Sort by last digit, then value

# Custom comparator (Python 3)
from functools import cmp_to_key
arr.sort(key=cmp_to_key(lambda a, b: a - b))  # Ascending
arr.sort(key=cmp_to_key(lambda a, b: b - a))  # Descending

# Sorting tuples
pairs = [(1, 'b'), (2, 'a'), (1, 'a')]
pairs.sort(key=lambda x: (x[0], x[1]))  # Sort by first, then second
# Time: O(n log n) guaranteed
# Space: O(n)
# Stable: Yes
```

---

## Sorting with Custom Key

```python
# Sort by absolute value
arr = [-3, 1, -4, 1, 5]
arr.sort(key=lambda x: abs(x))
# [-3, 1, 1, -4, 5] -> [-3, 1, 1, -4, 5] by abs

# Sort by frequency
from collections import Counter
freq = Counter([3, 1, 4, 1, 5, 9, 2, 6, 5])
arr = [3, 1, 4, 1, 5, 9, 2, 6, 5]
arr.sort(key=lambda x: (freq[x], -x))
# Sort by frequency ascending, then by value descending

# Sort strings by length
words = ["apple", "hi", "banana", "ok"]
words.sort(key=len)
# ['hi', 'ok', 'apple', 'banana']

# Sort with operator.itemgetter
from operator import itemgetter
data = [(1, 'c'), (2, 'a'), (1, 'b')]
data.sort(key=itemgetter(0, 1))  # Sort by index 0, then index 1
```

---

## Sorting Tricks for CP

```python
# 1. Sort only part of array
arr = [5, 3, 8, 1, 9, 2]
arr[1:4] = sorted(arr[1:4])  # Sort only indices 1 to 3
# [5, 1, 3, 8, 9, 2]

# 2. Stable sort preserves order of equal elements
# Use for multi-level sorting without tuples

# 3. argsort - get indices that would sort array
import numpy as np  # (or implement manually)
arr = [3, 1, 4, 1, 5]
indices = sorted(range(len(arr)), key=lambda i: arr[i])
# [1, 3, 0, 2, 4]

# 4. Sort and deduplicate
arr = [3, 1, 4, 1, 5, 3, 4]
unique_sorted = sorted(set(arr))
# [1, 3, 4, 5]

# 5. Find kth smallest without full sort
import heapq
kth = heapq.nsmallest(k, arr)[-1]  # O(n log k)

# 6. Partial sort for top k
top_k = heapq.nlargest(k, arr)  # O(n log k)
```

---

## Comparison Table

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Merge | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Quick | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Counting | O(n+k) | O(n+k) | O(n+k) | O(n+k) | Yes |
| Radix | O(dn) | O(dn) | O(dn) | O(n+k) | Yes |
| Bucket | O(n+k) | O(n+k) | O(n²) | O(n+k) | Depends |
| Tim Sort | O(n) | O(n log n) | O(n log n) | O(n) | Yes |

**For CP:** Use Python's built-in `sort()` (Tim Sort) unless specifically asked to implement another.
