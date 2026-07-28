# Sorting, Hashing & Heaps — Complete Problem Bank (40 Problems)

> **Infosys SP DSE Preparation** | All solutions in Python
> Sorting (12) + Hashing (15) + Heaps (13) = **40 Problems**

---

# PART A: SORTING PROBLEMS (12)

---

## Problem 1: Sort an Array (Merge Sort) [EASY]

**Problem:** Given an array of integers `nums`, sort the array in ascending order and return it. You must solve it without using any built-in sort functions. Target O(n log n) time.

---

### Problem Explanation (Simple Words)
We need to sort numbers from smallest to largest **without** using Python's built-in `sorted()` or `.sort()`. Merge Sort uses a "divide and conquer" strategy: repeatedly split the array in half until each piece has just one element (trivially sorted), then merge those pieces back together in sorted order.

### Step-by-Step Algorithm
1. **Base Case:** If the array has 0 or 1 elements, it's already sorted — return it.
2. **Divide:** Find the middle index `mid = len(arr) // 2`.
3. **Recursively Sort:** Recursively sort the left half `arr[:mid]` and the right half `arr[mid:]`.
4. **Merge:** Merge the two sorted halves using two pointers:
   - Compare the current element of each half.
   - Pick the smaller one and add to result.
   - Advance the pointer from which we picked.
5. **Collect Remaining:** Once one half is exhausted, append all remaining elements from the other half.

### Visual Trace with Example
**Input:** `[5, 2, 3, 1]`

```
Divide:
           [5, 2, 3, 1]
          /             \
     [5, 2]           [3, 1]
     /    \            /    \
   [5]    [2]        [3]    [1]

Conquer (Merge):
   [5] + [2] → [2, 5]        [3] + [1] → [1, 3]
        \                        /
         [2, 5]  +  [1, 3]  →  [1, 2, 3, 5]
```

**Step-by-step merge of `[5]` and `[2]`:**
- Compare 5 vs 2 → pick 2 → result `[2]`
- Only 5 remains → pick 5 → result `[2, 5]`

**Step-by-step merge of `[2, 5]` and `[1, 3]`:**
- Compare 2 vs 1 → pick 1 → result `[1]`
- Compare 2 vs 3 → pick 2 → result `[1, 2]`
- Compare 5 vs 3 → pick 3 → result `[1, 2, 3]`
- Only 5 remains → pick 5 → result `[1, 2, 3, 5]`

### Well-Commented Code

```python
def sortArray(nums):
    # Recursive merge sort implementation
    def merge_sort(arr):
        # Base case: single element or empty is already sorted
        if len(arr) <= 1:
            return arr

        # Divide the array into two halves
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])    # Recursively sort left half
        right = merge_sort(arr[mid:])   # Recursively sort right half

        # Merge the two sorted halves
        return merge(left, right)

    def merge(left, right):
        result = []      # Temporary array for merged output
        i = j = 0        # Pointers for left and right arrays

        # Compare elements from both halves and pick the smaller one
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:      # Use <= for stability
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        # Append any remaining elements from either half
        result.extend(left[i:])
        result.extend(right[j:])

        return result

    return merge_sort(nums)


# Test cases
print(sortArray([5, 2, 3, 1]))       # [1, 2, 3, 5]
print(sortArray([5, 1, 1, 2, 0, 0])) # [0, 0, 1, 1, 2, 5]
print(sortArray([]))                  # []
print(sortArray([1]))                 # [1]
```

### Complexity Analysis
- **Time Complexity:** O(n log n) — we divide log n times, and each level merges O(n) elements.
- **Space Complexity:** O(n) — we create new arrays during each merge. In-place merge sort exists but is complex.
- **Stability:** Yes — equal elements retain their original relative order (due to `<=`).

### Edge Cases
- **Empty array `[]`:** Base case returns `[]` correctly.
- **Single element `[1]`:** Base case returns `[1]` correctly.
- **Already sorted `[1, 2, 3]`:** Merge sort still divides and merges (no early exit for sorted input).
- **All equal elements `[5, 5, 5]`:** Merge picks left first due to `<=`, maintaining stability.
- **Negative numbers:** Handled correctly since comparison works on integers.
- **Large arrays:** Recursion depth ~log₂(n). For n=10⁶, depth ≈ 20, well within Python's recursion limit.

### Common Mistakes
1. **Using `<` instead of `<=` in merge:** Makes the sort unstable. Equal elements may not preserve original order.
2. **Modifying input array accidentally:** This implementation creates new arrays; be aware of O(n) memory cost.
3. **Infinite recursion:** Forgetting the base case or incorrectly dividing leads to stack overflow.
4. **Incorrect mid calculation:** `(left + right) // 2` can overflow in some languages; in Python, `len(arr) // 2` is fine.

### Pattern Recognition
- **Divide and Conquer:** Merge Sort is the classic D&C algorithm. Any problem that can be split, solved independently, and combined may use this pattern.
- **Inversion Counting:** The merge step can be augmented to count inversions (see Problem 10 — Count Smaller Numbers After Self).
- **External Sorting:** Merge Sort's sequential access pattern makes it ideal for sorting data too large to fit in memory.
- **Linked Lists:** Merge Sort is the preferred sorting algorithm for linked lists because it requires O(1) extra space for linked lists (no random access needed).

---

## Problem 2: Sort Colors (Dutch National Flag) [EASY]

**Problem:** Given an array `nums` with n objects colored red (0), white (1), or blue (2), sort them in-place so objects of the same color are adjacent in the same order: red, white, blue. You must solve it without using the library's sort function. Use one pass with O(1) extra space.

---

### Problem Explanation (Simple Words)
We have an array of only three values: 0, 1, and 2. We need to group all 0s together, then all 1s, then all 2s — in a single pass through the array with no extra memory. Think of it like sorting a flag with three colored stripes.

### Step-by-Step Algorithm (Dutch National Flag)
1. **Initialize three pointers:**
   - `low = 0` — boundary before which all elements are 0
   - `mid = 0` — current element being examined
   - `high = len(nums) - 1` — boundary after which all elements are 2
2. **Loop while `mid <= high`:**
   - **Case `nums[mid] == 0`:** Swap with `nums[low]`, advance both `low` and `mid` (we know the element swapped from `low` was already processed as 0 or 1).
   - **Case `nums[mid] == 1`:** Leave it in place, just advance `mid` (1 belongs in the middle region).
   - **Case `nums[mid] == 2`:** Swap with `nums[high]`, decrement `high` only (the element swapped from `high` is unknown and needs examination).

### Visual Trace with Example
**Input:** `[2, 0, 2, 1, 1, 0]`

```
Initial: low=0, mid=0, high=5
  [2, 0, 2, 1, 1, 0]
   ^                 ^
  mid=0             high=5
  low=0

Step 1: nums[0]=2 → swap with high(5)
  [0, 0, 2, 1, 1, 2]   high becomes 4
   ^              ^
  mid=0          high=4

Step 2: nums[0]=0 → swap with low(0), low→1, mid→1
  [0, 0, 2, 1, 1, 2]
      ^  ^
     low mid=1  high=4

Step 3: nums[1]=0 → swap with low(1), low→2, mid→2
  [0, 0, 2, 1, 1, 2]
         ^
        low,mid=2  high=4

Step 4: nums[2]=2 → swap with high(4), high→3
  [0, 0, 1, 1, 2, 2]
         ^     ^
        mid=2 high=3

Step 5: nums[2]=1 → mid→3
  [0, 0, 1, 1, 2, 2]
            ^  ^
           mid=3 high=3

Step 6: nums[3]=1 → mid→4
  mid=4 > high=3 → STOP

Result: [0, 0, 1, 1, 2, 2]
```

### Well-Commented Code

```python
def sortColors(nums):
    # Three pointers for the three regions
    low = 0           # Next position for a 0
    mid = 0           # Current element being examined
    high = len(nums) - 1  # Next position for a 2

    while mid <= high:
        if nums[mid] == 0:
            # 0 belongs at the low boundary — swap with low pointer
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1      # Low boundary shifts right
            mid += 1      # We know the swapped-in value is 0 or 1 (already processed)
        elif nums[mid] == 1:
            # 1 is in the correct middle region — just advance
            mid += 1
        else:  # nums[mid] == 2
            # 2 belongs at the high boundary — swap with high pointer
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1     # High boundary shifts left
            # Do NOT advance mid — the swapped-in value needs examination

    return nums


# Test cases
print(sortColors([2, 0, 2, 1, 1, 0]))  # [0, 0, 1, 1, 2, 2]
print(sortColors([2, 0, 1]))            # [0, 1, 2]
print(sortColors([0]))                  # [0]
print(sortColors([1, 1, 0, 2]))         # [0, 1, 1, 2]
```

### Complexity Analysis
- **Time Complexity:** O(n) — single pass through the array with constant work per element.
- **Space Complexity:** O(1) — only three integer pointers used, no extra data structures.
- **Stability:** Not stable — relative order of equal elements may change.

### Edge Cases
- **Single element `[0]` or `[1]` or `[2]`:** Loop condition `mid <= high` handles it — single pass, no swaps.
- **Already sorted `[0, 0, 1, 1, 2, 2]`:** Algorithm runs without any swaps (each element is already in correct zone).
- **All same value `[1, 1, 1]`:** The `mid` pointer advances through the array; `low` stays at 0, `high` stays at end.
- **Two distinct values `[0, 0, 2, 2]`:** The algorithm correctly handles missing values.
- **Minimum/maximum length:** n=1 works directly; n=2 works correctly.

### Common Mistakes
1. **Advancing `mid` after swapping with `high`:** The element brought from the high region is unexamined. Don't increment `mid`, or you'll miss processing it.
2. **Not advancing `mid` after swapping with `low`:** The element at `low` was already processed (it was part of the 0 or 1 region), so advancing `mid` is safe.
3. **Using `while mid < high` instead of `<=`:** If `mid == high`, the element at that position still needs processing.
4. **Confusing boundary conditions:** Remember: `[0, low)` = all 0s, `[low, mid)` = all 1s, `(high, end]` = all 2s.

### Pattern Recognition
- **Three-Way Partitioning:** This is the canonical three-way partition. Useful whenever you have exactly three distinct values to sort.
- **Two-Pointer Technique:** If there were only 0s and 1s, a simpler two-pointer approach would work. The third pointer extends this.
- **Quicksort Partition:** The Dutch National Flag algorithm generalizes the partition step of quicksort when there are many duplicate keys (3-way quicksort).
- **Segregation Problems:** Any "segregate 0s and 1s" or "move all zeros to front" problem follows a similar two/three-pointer pattern.

---

## Problem 3: Merge Sorted Array [EASY]

**Problem:** Given two sorted integer arrays `nums1` (size m+n, last n elements are 0) and `nums2` (size n), merge `nums2` into `nums1` in-place, sorted in non-decreasing order.

---

### Problem Explanation (Simple Words)
We have two sorted arrays. `nums1` has extra space at the end (filled with zeros) to hold `nums2`. We need to merge `nums2` into `nums1` without using extra space. The trick is to fill from the **end** (largest elements first) so we don't overwrite elements in `nums1` that haven't been processed yet.

### Step-by-Step Algorithm
1. **Set up three pointers:**
   - `p1 = m - 1` — last valid element in `nums1`
   - `p2 = n - 1` — last element in `nums2`
   - `write = m + n - 1` — last position in `nums1` (where we write)
2. **While there are elements in `nums2` (`p2 >= 0`):**
   - If `p1 >= 0` and `nums1[p1] > nums2[p2]`: place `nums1[p1]` at `write`, decrement `p1`
   - Else: place `nums2[p2]` at `write`, decrement `p2`
   - Decrement `write`
3. **Result:** `nums1` now contains the merged sorted array.

### Visual Trace with Example
**Input:** `nums1 = [1, 2, 3, 0, 0, 0]`, `m = 3`, `nums2 = [2, 5, 6]`, `n = 3`

```
Initial:
  nums1: [1, 2, 3, 0, 0, 0]
           ^        ^
          p1=2     write=5
  nums2: [2, 5, 6]
                 ^
                p2=2

Step 1: nums1[2]=3 vs nums2[2]=6 → 6 is larger
  write=5 → nums1[5] = 6, p2→1, write→4
  nums1: [1, 2, 3, 0, 0, 6]

Step 2: nums1[2]=3 vs nums2[1]=5 → 5 is larger
  write=4 → nums1[4] = 5, p2→0, write→3
  nums1: [1, 2, 3, 0, 5, 6]

Step 3: nums1[2]=3 vs nums2[0]=2 → 3 is larger
  write=3 → nums1[3] = 3, p1→1, write→2
  nums1: [1, 2, 3, 3, 5, 6]

Step 4: nums1[1]=2 vs nums2[0]=2 → 2 is not > 2, take from nums2
  write=2 → nums1[2] = 2, p2→-1, write→1
  nums1: [1, 2, 2, 3, 5, 6]

p2 = -1 → STOP
Result: [1, 2, 2, 3, 5, 6]
```

### Well-Commented Code

```python
def merge(nums1, m, nums2, n):
    # Pointers to the last valid elements in both arrays
    p1 = m - 1           # Last valid element in nums1
    p2 = n - 1           # Last element in nums2
    write = m + n - 1    # Last position in nums1 to write to

    # Fill nums1 from the back (largest to smallest)
    while p2 >= 0:       # Only need to check p2; if p1 runs out, rest of nums2 is placed
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            # Current nums1 element is larger — place it at the write position
            nums1[write] = nums1[p1]
            p1 -= 1
        else:
            # Current nums2 element is larger or equal — place it at write position
            nums1[write] = nums2[p2]
            p2 -= 1
        write -= 1       # Move the write pointer left

    return nums1


# Test cases
print(merge([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3))  # [1, 2, 2, 3, 5, 6]
print(merge([1], 1, [], 0))                           # [1]
print(merge([0], 0, [1], 1))                          # [1]
print(merge([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3))   # [1, 2, 3, 4, 5, 6]
```

### Complexity Analysis
- **Time Complexity:** O(m + n) — we process each element from both arrays exactly once.
- **Space Complexity:** O(1) — we use only three integer pointers; no extra arrays.
- **In-Place:** Yes — we modify `nums1` directly without creating a new array.

### Edge Cases
- **Empty nums2 (`n = 0`):** The `while p2 >= 0` loop doesn't execute; `nums1` is returned unchanged.
- **Empty nums1 (`m = 0`):** `p1 = -1`, so we always take from `nums2`. All `nums2` elements are copied to `nums1` correctly.
- **All nums2 elements smaller:** `p1` gets exhausted first; remaining `nums2` elements are placed correctly.
- **All nums2 elements larger:** The loop takes from `nums2` first; `p1` remains untouched.
- **Duplicate elements:** Using `>` (not `>=`) ensures that when equal, we take from `nums2`, which is correct.

### Common Mistakes
1. **Filling from the front:** If you fill from the beginning, you'll overwrite unprocessed elements of `nums1`. Always fill from the **back**.
2. **Forgetting that `nums1` has extra space:** The last n elements of `nums1` are zeros — don't treat them as valid data.
3. **Using `while p1 >= 0 or p2 >= 0`:** Simplifying to `while p2 >= 0` is sufficient because if `p1` runs out, the remaining nums2 elements are already in their correct positions.
4. **Not passing `m` and `n` separately:** The function signature includes `m` and `n` because `nums1` can be larger than `m + n` (though for this problem it's exactly `m + n`).

### Pattern Recognition
- **Two-Pointer from End:** Whenever you merge two sorted arrays in-place and there's extra space at the end, fill from the back.
- **Merge Step of Merge Sort:** This is exactly the merge operation used in merge sort, adapted for in-place merging.
- **Sorted Array Operations:** Many sorted array problems (union, intersection, merging) use the two-pointer technique.
- **Similar Problems:** Merge Two Sorted Lists (linked list version), Median of Two Sorted Arrays.

---

## Problem 4: Kth Largest Element in a Stream [EASY]

**Problem:** Design a class to find the kth largest element in a stream. Implement `KthLargest(k, nums)` constructor and `add(val)` method that returns the kth largest element after adding `val`.

---

### Problem Explanation (Simple Words)
Numbers keep coming one by one (a stream). At any point, we need to know what the kth largest number is among all numbers seen so far. A min-heap of size k is perfect: it keeps only the k largest numbers, and the smallest among them (the heap root) is the kth largest.

### Step-by-Step Algorithm
**Constructor `__init__(k, nums)`:**
1. Store `k` and create a heap from the initial `nums`.
2. Convert the list into a valid heap using `heapq.heapify()`.
3. Remove the smallest elements until the heap has exactly `k` elements (we only want the top k).

**Add Method `add(val)`:**
1. Push the new value into the heap.
2. If heap size exceeds k, pop the smallest element (it's no longer in the top k).
3. Return the root of the heap (which is the kth largest).

### Visual Trace with Example
**Setup:** `k = 3`, initial `nums = [4, 5, 8, 2]`

```
Constructor:
  Start heap: [4, 5, 8, 2]
  heapify → [2, 4, 8, 5]
  Pop until size = 3:
    Pop 2 → heap: [4, 5, 8]
  Final heap (top 3): [4, 5, 8]
  Root = 4 (kth largest)

  add(3): push 3 → heap [3, 4, 8, 5], pop 3 → heap [4, 5, 8] → return 4
  add(5): push 5 → heap [4, 5, 8, 5], pop 4 → heap [5, 5, 8] → return 5
  add(10): push 10 → heap [5, 5, 8, 10], pop 5 → heap [5, 8, 10] → return 5
  add(9): push 9 → heap [5, 8, 9, 10], pop 5 → heap [8, 9, 10] → return 8
  add(4): push 4 → heap [4, 8, 9, 10], pop 4 → heap [8, 9, 10] → return 8
```

### Well-Commented Code

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        # Build a min-heap from the initial list
        self.heap = nums[:]
        heapq.heapify(self.heap)             # Convert to heap (O(n))

        # Keep only the k largest elements
        # The smallest of these is the kth largest overall
        while len(self.heap) > k:
            heapq.heappop(self.heap)         # Remove smallest until size = k

    def add(self, val):
        # Add the new value to the stream
        heapq.heappush(self.heap, val)

        # If heap exceeds k, remove the smallest element
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)

        # Root of the min-heap is the kth largest element
        return self.heap[0]


# Test cases
obj = KthLargest(3, [4, 5, 8, 2])
print(obj.add(3))   # 4
print(obj.add(5))   # 5
print(obj.add(10))  # 5
print(obj.add(9))   # 8
print(obj.add(4))   # 8
```

### Complexity Analysis
- **Constructor Time:** O(n log k) — `heapify` is O(n), then we pop (n-k) times at O(log k) each.
- **Add Time:** O(log k) — heap push and possible pop are both O(log k).
- **Space Complexity:** O(k) — the heap stores exactly k elements.
- **Note:** If initial `nums` is empty, the heap starts empty and fills as `add` is called, until it reaches size k.

### Edge Cases
- **k > initial array length:** The heap starts with fewer than k elements. The first k-1 `add` calls simply push; the kth call makes the heap full and the kth largest becomes meaningful.
- **Duplicate values:** Handled correctly — duplicates are counted separately. For example, k=2 in [5,5,5]: 5 is the 2nd largest.
- **Very small k (k=1):** The heap keeps only 1 element; `heap[0]` is always the largest element seen so far.
- **Stream with decreasing values:** The heap fills and progressively smaller elements are popped.
- **Empty initial array with k>0:** The first k-1 add calls push elements; subsequent calls maintain size k.

### Common Mistakes
1. **Using a max-heap instead of min-heap:** A max-heap of size k gives the kth *smallest*, not largest. Use a min-heap that discards the smallest elements.
2. **Forgetting to handle `len(heap) > k` after push:** Always check and pop if needed. Otherwise the heap grows unbounded.
3. **Returning from heap before checking size:** Ensure the heap has at least k elements before returning `heap[0]` (though the problem guarantees valid calls).
4. **Not using `heapify` in constructor:** Iterating and pushing each element is O(n log n); `heapify` is O(n).
5. **Confusing kth largest vs kth distinct:** This problem counts duplicates (kth largest in sorted order, ignoring distinctness).

### Pattern Recognition
- **Min-Heap of Size k:** This is the standard pattern for "kth largest" in a stream or array. The heap root is always the answer.
- **Streaming Algorithms:** For continuous data streams where you can't store all elements, a bounded heap is a common technique.
- **Top-k Pattern:** Any "top k" problem (k largest, k smallest, k most frequent) can use a heap of size k.
- **Trade-off:** O(n log k) is better than O(n log n) full sort when n >> k. This is important for large data sets.
- **Quickselect Alternative:** For static arrays, quickselect gives O(n) average but doesn't handle streams.

---

## Problem 5: Kth Largest Element in an Array (Quickselect) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return the kth largest element (not the kth distinct). Must run in O(n) average time.

---

### Problem Explanation (Simple Words)
Find the kth largest number in an unsorted array — without fully sorting the array. Quickselect works like Quicksort but only recurses into one side (the side containing the kth element), making it faster on average than fully sorting.

### Step-by-Step Algorithm
1. **Convert to "kth smallest":** Since finding kth largest is same as finding `(n-k)`th smallest, we look for index `k-1` in descending order.
2. **Pick a random pivot:** Randomly select an element to partition around (avoids worst case).
3. **Partition (descending):**
   - Move the pivot to the rightmost position for convenience.
   - Use a `store` pointer to track where the next "greater than pivot" element goes.
   - Elements > pivot go to the left, elements <= pivot stay to the right.
   - Place the pivot at its correct sorted position.
4. **Recurse on the correct side:**
   - If pivot index == k-1: return pivot (found!).
   - If pivot index < k-1: recurse on the right half.
   - If pivot index > k-1: recurse on the left half.

### Visual Trace with Example
**Input:** `nums = [3, 2, 1, 5, 6, 4]`, `k = 2` (find 2nd largest)

```
Array: [3, 2, 1, 5, 6, 4], looking for index k-1 = 1 in descending order

Step 1: Pick random pivot, say index 4 (value 6)
  Swap with right: [3, 2, 1, 5, 4, 6]
  pivot = 6, store = 0, iterate i=0 to 4:
    i=0: 3 > 6? No → skip
    i=1: 2 > 6? No → skip
    i=2: 1 > 6? No → skip
    i=3: 5 > 6? No → skip
    i=4: 4 > 6? No → skip
  After loop: nothing > pivot, so store=0
  Swap nums[0] with nums[5]: [6, 2, 1, 5, 4, 3]
  pivot index = 0

Step 2: 0 < k_smallest(1) → recurse right half (indices 1..5)
  [2, 1, 5, 4, 3]

Step 3: Pick random pivot, say index 2 (value 5), swap with right index 5
  [2, 1, 3, 4, 5]
  pivot = 5, store = 1, iterate i=1 to 4:
    i=1: 1 > 5? No
    i=2: 3 > 5? No
    i=3: 4 > 5? No
    i=4: nothing (i < right=5)
  store stays at 1, swap nums[1] with nums[5]: [2, 5, 3, 4, 1]
  pivot index = 1 == k_smallest → return 5 ✓
```

### Well-Commented Code

```python
import random

def findKthLargest(nums, k):
    def quickselect(left, right, k_smallest):
        """Find the kth smallest element in nums[left..right] (descending order)"""
        # Base case: only one element in range
        if left == right:
            return nums[left]

        # Pick a random pivot to avoid worst-case O(n²)
        pivot_idx = random.randint(left, right)
        # Move the pivot to the right end for partitioning
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]
        pivot = nums[right]

        # Partition: elements > pivot go to the left of store pointer
        store = left
        for i in range(left, right):
            if nums[i] > pivot:          # Descending order: larger elements first
                nums[store], nums[i] = nums[i], nums[store]
                store += 1

        # Place pivot at its correct position
        nums[store], nums[right] = nums[right], nums[store]

        # Decide which side the kth element is on
        if store == k_smallest:
            return nums[store]           # Found it!
        elif store < k_smallest:
            return quickselect(store + 1, right, k_smallest)  # Search right half
        else:
            return quickselect(left, store - 1, k_smallest)   # Search left half

    # kth largest = (k-1)th element when sorted in descending order
    return quickselect(0, len(nums) - 1, k - 1)


# Test cases
print(findKthLargest([3, 2, 1, 5, 6, 4], 2))                      # 5
print(findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))            # 4
print(findKthLargest([1], 1))                                      # 1
print(findKthLargest([7, 7, 7, 7], 2))                            # 7
```

### Complexity Analysis
- **Average Time:** O(n) — each partition takes O(n) and we recurse on only one half. Expected depth is O(log n), but total work is n + n/2 + n/4 + ... = O(n).
- **Worst Time:** O(n²) — when the pivot is always the smallest or largest element (extremely unlikely with random pivots).
- **Space:** O(log n) average for recursion stack; worst case O(n).
- **Note:** Python's recursion limit may be hit for very large n. Use iterative approach or increase `sys.setrecursionlimit()`.

### Edge Cases
- **Single element array:** Base case `left == right` returns that element.
- **k = 1 (largest element):** `k_smallest = 0`; returns the maximum element.
- **k = n (smallest element):** `k_smallest = n-1`; partition eventually reaches the minimum.
- **All equal elements:** Partition places all elements on one side due to `>` comparison; algorithm still works correctly.
- **k > n:** Problem guarantees 1 ≤ k ≤ n, so this doesn't occur.

### Common Mistakes
1. **Confusing kth largest with kth largest distinct:** This problem counts duplicates. k=2 in [7,7,7,7] gives 7, not an error.
2. **Not randomizing the pivot:** Fixed pivot (e.g., always first or last element) leads to O(n²) on sorted/almost-sorted arrays.
3. **Incorrect index calculation:** kth largest (1-indexed) = index k-1 in 0-indexed descending order.
4. **Partitioning in ascending order:** If you partition in ascending order, kth largest = look for index (n-k), which is more confusing.
5. **Off-by-one in recursive calls:** `store - 1` and `store + 1` are critical to avoid infinite recursion.

### Pattern Recognition
- **Quickselect:** This is the selection algorithm counterpart of Quicksort. Use when you need the kth order statistic (kth smallest/largest) without full sorting.
- **Partition-Based Algorithms:** The partition step is also used in quicksort, Dutch National Flag, and finding median.
- **When to use Heap vs Quickselect:**
  - Heap: O(n log k), good for streams or when k is small.
  - Quickselect: O(n) average, good for static arrays when k is large (e.g., median where k = n/2).
- **Randomized Algorithms:** Random pivot selection makes worst-case probability exponentially small — a common technique for average-case guarantees.

---

## Problem 6: Sort Integers by Number of 1 Bits [MEDIUM]

**Problem:** Given an integer array `arr`, sort the integers by the number of 1 bits in binary representation. If two numbers have the same count, sort them in ascending order. Return the sorted array.

---

### Problem Explanation (Simple Words)
Each number has a binary representation (e.g., 5 = 101 has two 1-bits). We need to sort numbers by how many 1-bits they have. If two numbers have the same count of 1-bits, sort them by their actual value ascending.

### Step-by-Step Algorithm
1. **Create a custom key function** that returns a tuple `(bit_count, value)`.
2. **Sort the array** using this key:
   - Primary sort: by number of 1 bits (ascending).
   - Secondary sort: by the number itself (ascending) when bit counts tie.
3. **Return the sorted array.**

### Visual Trace with Example
**Input:** `arr = [0, 1, 2, 3, 4, 5, 6, 7, 8]`

Compute bit counts:
```
0  (0000) → 0 ones
1  (0001) → 1 one
2  (0010) → 1 one
3  (0011) → 2 ones
4  (0100) → 1 one
5  (0101) → 2 ones
6  (0110) → 2 ones
7  (0111) → 3 ones
8  (1000) → 1 one
```

Sort by (bit_count, value):
```
(0, 0)   → 0
(1, 1)   → 1
(1, 2)   → 2
(1, 4)   → 4
(1, 8)   → 8
(2, 3)   → 3
(2, 5)   → 5
(2, 6)   → 6
(3, 7)   → 7
```
**Result:** `[0, 1, 2, 4, 8, 3, 5, 6, 7]`

### Well-Commented Code

```python
def sortByBits(arr):
    # Key returns tuple: (number_of_1_bits, original_value)
    # Python sorts by tuple elements left-to-right
    return sorted(arr, key=lambda x: (x.bit_count(), x))
    # x.bit_count() is Python 3.10+ — uses efficient CPU instruction (popcount)


# Alternative for older Python versions (< 3.10):
def sortByBits_alternative(arr):
    # bin(x) converts to binary string like '0b101'
    # .count('1') counts the 1-bits
    return sorted(arr, key=lambda x: (bin(x).count('1'), x))


# Test cases
print(sortByBits([0, 1, 2, 3, 4, 5, 6, 7, 8]))                          # [0, 1, 2, 4, 8, 3, 5, 6, 7]
print(sortByBits([1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]))         # [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
print(sortByBits([3]))                                                     # [3]
print(sortByBits([10, 5, 3, 8]))                                          # [8, 5, 10, 3]
```

### Complexity Analysis
- **Time Complexity:** O(n log n) — the sorting dominates. Computing bit_count is O(1) per element (CPU popcount instruction).
- **Space Complexity:** O(n) — Python's sort creates a new list (unless `arr.sort()` is used in-place).
- **Alternative Key Computation:** `bin(x).count('1')` is O(number of bits) ≈ O(log x) per element, making overall time O(n log n + n log max_val).

### Edge Cases
- **All zeros:** `[0, 0, 0]` → all have 0 ones → sorted by value (all 0).
- **All same bit count (e.g., powers of 2):** Each has exactly 1 one-bit → sorted by value ascending.
- **Single element:** Returns as-is.
- **Negative numbers:** `bit_count()` counts the bits of the two's complement representation. In Python 3.10+, `(-3).bit_count()` returns a large number (infinite bits in conceptual two's complement). **Important:** This approach works best for non-negative integers. If negative numbers are allowed, use `bin(x).count('1')` which treats negatives properly.
- **Large values:** Python integers have arbitrary precision; `bit_count()` works efficiently regardless of size.

### Common Mistakes
1. **Forgetting the tie-breaker:** Without `x` as the second tuple element, numbers with the same bit count maintain their original relative order (stable sort), which may not be ascending.
2. **Using `popcount` for negative numbers:** `int.bit_count()` on negative numbers can be confusing. Verify the problem constraints first.
3. **Not knowing `int.bit_count()` exists:** This method (Python 3.10+) is much faster than `bin(x).count('1')`.
4. **Inefficient key computation:** Computing the key repeatedly (avoided by Python's `sorted` which caches keys via `key=`).

### Pattern Recognition
- **Custom Sort Key:** This is the most common technique for "sort by a computed property." The `key` function is called once per element (Schwartzian transform / decorate-sort-undecorate).
- **Tuple-Based Sorting:** When you need multi-level sorting, use a tuple as the sort key. Python compares tuples element-by-element.
- **Bit Manipulation:** `bit_count()` (popcount) appears in many problems: counting bits, Hamming distance, binary representations.
- **Bucket Sort Alternative:** For O(n), create buckets indexed by bit count (0 to max bits), place numbers in their bucket, flatten in order.

---

## Problem 7: Meeting Rooms II [MEDIUM]

**Problem:** Given an array of meeting time intervals `[[start, end]]` (start < end), find the minimum number of conference rooms required.

---

### Problem Explanation (Simple Words)
We have a set of meetings with start and end times. We need the minimum number of rooms so no two meetings overlap in the same room. Think of it as: when a meeting starts, we need a room; when it ends, the room becomes free. The maximum number of **simultaneous** meetings at any point is our answer.

### Step-by-Step Algorithm
1. **Sort** all meetings by start time (earliest first).
2. **Use a min-heap** to track when each ongoing meeting ends. The heap root = earliest ending meeting.
3. **For each meeting** `(start, end)`:
   - If a room is free (the earliest ending meeting ends ≤ current start), **reuse** that room by popping from heap.
   - Push the current meeting's end time into the heap (allocating a room).
4. **Return** the size of the heap (= number of rooms needed).

### Visual Trace with Example
**Input:** `intervals = [[0, 30], [5, 10], [15, 20]]`

```
Step 1: Sort by start → [[0, 30], [5, 10], [15, 20]]
         (already sorted)

Step 2: Process each meeting:
  Meeting [0, 30]:
    heap = [] → no free room
    Push 30 → heap = [30]    rooms: 1

  Meeting [5, 10]:
    heap[0] = 30 > 5 → no free room
    Push 10 → heap = [10, 30]    rooms: 2

  Meeting [15, 20]:
    heap[0] = 10 ≤ 15 → free room! Pop 10
    Push 20 → heap = [20, 30]    rooms: 2

Result: len(heap) = 2 rooms needed ✓
```

**Another example:** `[[1, 5], [2, 3], [4, 6]]`
```
  Meeting [1, 5]: heap = [] → push 5 → [5]
  Meeting [2, 3]: heap[0]=5 > 2 → push 3 → [3, 5]
  Meeting [4, 6]: heap[0]=3 ≤ 4 → pop 3, push 6 → [5, 6]
Result: 2 rooms
```

### Well-Commented Code

```python
import heapq

def minMeetingRooms(intervals):
    # Edge case: no meetings means no rooms needed
    if not intervals:
        return 0

    # Sort by start time so we process meetings in chronological order
    intervals.sort(key=lambda x: x[0])

    # Min-heap to track end times of currently occupied rooms
    heap = []

    for start, end in intervals:
        # If the earliest ending meeting is already over, reuse that room
        if heap and heap[0] <= start:
            heapq.heappop(heap)

        # Assign a room for this meeting (push its end time)
        heapq.heappush(heap, end)

    # The heap size at the end = maximum concurrent meetings = rooms needed
    return len(heap)


# Test cases
print(minMeetingRooms([[0, 30], [5, 10], [15, 20]]))  # 2
print(minMeetingRooms([[7, 10], [2, 4]]))              # 1
print(minMeetingRooms([[1, 5], [2, 3], [4, 6]]))      # 2
print(minMeetingRooms([]))                              # 0
print(minMeetingRooms([[1, 5], [5, 10]]))              # 1 (end=start is OK, no overlap)
```

### Complexity Analysis
- **Time Complexity:** O(n log n) — sorting is O(n log n), each heap operation is O(log n).
- **Space Complexity:** O(n) — worst case all meetings overlap concurrently.
- **Note:** The heap can grow up to n in the worst case (all meetings at the same time).

### Edge Cases
- **Empty input `[]`:** Returns 0 — handled by early check.
- **One meeting:** Returns 1 — heap has one end time.
- **Meeting ends exactly when another starts `[1,5]` and `[5,10]`:** Since `heap[0] <= start` is used (≤), the room can be reused; returns 1 room.
- **All meetings overlap:** Heap grows to size n (all meetings need separate rooms).
- **No overlapping meetings:** Heap never exceeds size 1; returns 1 (need at least one room).
- **Unsorted input:** The sort handles this.

### Common Mistakes
1. **Using `<` instead of `<=` for room reuse:** If a meeting ends at 5 and the next starts at 5, the room can be reused. Using `<` would require a new room unnecessarily.
2. **Not sorting by start time:** Without sorting, you're processing meetings out of order, which breaks the logic.
3. **Forgetting the empty input case:** Without the early return, `intervals[0]` would raise an IndexError.
4. **Confusing start and end:** Pushing start times instead of end times would give incorrect results.
5. **Tracking maximum heap size separately:** The final heap size equals the maximum because we process chronologically. But for safety, many solutions track `max(count, len(heap))`.

### Pattern Recognition
- **Interval Scheduling with Heap:** This is the "minimum resources for overlapping intervals" problem. The heap tracks when resources become free.
- **Chronological Processing:** Sort events by time, then process sequentially — a core technique for interval problems.
- **Sweep Line Algorithm:** An alternative approach uses events: `(time, +1)` for start, `(time, -1)` for end, then sweep through time accumulating concurrent meetings.
- **Similar Problems:** Minimum platforms needed for trains (railway station), CPU job scheduling, car pooling.

---

## Problem 8: Maximum Gap (Bucket Sort) [MEDIUM]

**Problem:** Given an integer array `nums`, return the maximum difference between successive elements in its sorted form. Your algorithm must run in O(n) time.

---

### Problem Explanation (Simple Words)
If we sort the array, the maximum difference between consecutive numbers is the answer. But sorting takes O(n log n), and we need O(n). The key insight: with n numbers spread over a range, if we create enough buckets, at least one bucket will be empty. The maximum gap can't be inside a bucket — it must be between buckets. So we only need to track the min and max of each bucket.

### Step-by-Step Algorithm
1. **Handle edge cases:** If n < 2, return 0. If all elements equal, return 0.
2. **Create buckets:** Use n+1 buckets (pigeonhole principle ensures at least one empty bucket).
   - Each bucket covers a range of `(max_val - min_val) / n`.
3. **Place numbers in buckets:** For each number, compute which bucket it belongs to. Track only the **minimum and maximum** in each bucket.
4. **Find max gap:** Iterate through non-empty buckets. The answer is the maximum difference between the min of the current bucket and the max of the previous non-empty bucket.

### Visual Trace with Example
**Input:** `nums = [3, 6, 9, 1]`

```
n = 4
min_val = 1, max_val = 9
bucket_size = (9 - 1) // 4 = 2
bucket_count = (9 - 1) // 2 + 1 = 5

Buckets:
  Bucket 0: [1, 3)   → nums: 1  → min=1, max=1
  Bucket 1: [3, 5)   → nums: 3  → min=3, max=3
  Bucket 2: [5, 7)   → nums: 6  → min=6, max=6
  Bucket 3: [7, 9)   → (empty)
  Bucket 4: [9, 11)  → nums: 9  → min=9, max=9

Compute gaps between non-empty buckets:
  prev_max = min_val = 1
  Bucket 0: min=1, gap=|1-1|=0, prev_max=1
  Bucket 1: min=3, gap=|3-1|=2, prev_max=3
  Bucket 2: min=6, gap=|6-3|=3, prev_max=6
  Bucket 3: empty → skip
  Bucket 4: min=9, gap=|9-6|=3, prev_max=9

max_gap = 3 ✓
```

### Well-Commented Code

```python
def maximumGap(nums):
    # Edge cases: need at least 2 elements for a gap
    if len(nums) < 2:
        return 0

    n = len(nums)
    min_val, max_val = min(nums), max(nums)

    # If all elements are equal, gap is 0
    if min_val == max_val:
        return 0

    # Bucket size must be at least 1 (for integer division edge cases)
    bucket_size = max(1, (max_val - min_val) // n)
    bucket_count = (max_val - min_val) // bucket_size + 1

    # Track only min and max per bucket
    bucket_min = [float('inf')] * bucket_count
    bucket_max = [float('-inf')] * bucket_count

    # Place each number in its bucket
    for num in nums:
        idx = (num - min_val) // bucket_size
        bucket_min[idx] = min(bucket_min[idx], num)
        bucket_max[idx] = max(bucket_max[idx], num)

    # Find maximum gap between consecutive non-empty buckets
    max_gap = 0
    prev_max = min_val          # Start with the global minimum
    for i in range(bucket_count):
        # Skip empty buckets (where bucket_min was never updated)
        if bucket_min[i] == float('inf'):
            continue

        # Gap between current bucket's min and previous bucket's max
        max_gap = max(max_gap, bucket_min[i] - prev_max)

        # Update prev_max for the next iteration
        prev_max = bucket_max[i]

    return max_gap


# Test cases
print(maximumGap([3, 6, 9, 1]))     # 3
print(maximumGap([10]))              # 0
print(maximumGap([1, 1, 1, 1]))     # 0
print(maximumGap([1, 10000000]))    # 9999999
print(maximumGap([1, 3, 6, 9, 12])) # 3
```

### Complexity Analysis
- **Time Complexity:** O(n) — two passes over the array (one for placing in buckets, one for finding max gap). No sorting needed.
- **Space Complexity:** O(n) — we create `bucket_count` = n+1 pairs of min/max values.
- **Correctness:** Based on the pigeonhole principle: with n numbers and n+1 buckets, at least one bucket is empty. The maximum gap must span across this empty bucket, so it occurs between elements in different buckets. Within-bucket gaps are always ≤ bucket_size.

### Edge Cases
- **Less than 2 elements:** No consecutive elements → gap is 0.
- **All elements equal:** min_val == max_val → gap is 0.
- **Two elements:** The gap is simply |max_val - min_val|. The algorithm works: bucket_size = max(1, range/2), bucket_count = range/size + 1, and the gap between the two buckets gives the answer.
- **Very large range:** (max_val - min_val) could be huge; Python handles arbitrary precision.
- **Negative numbers:** The formula `(num - min_val) // bucket_size` handles negative numbers correctly (since min_val is the smallest negative, making the difference positive).

### Common Mistakes
1. **Not handling `min_val == max_val`:** All elements equal — the bucket formula would give bucket_size = 0 or division by zero.
2. **Incorrect bucket index calculation:** The index formula must ensure indices are in bounds `[0, bucket_count)`. Using integer division carefully.
3. **Forgetting `max(1, ...)` for bucket_size:** If range < n, `bucket_size = (max-min) // n` could be 0, causing division by zero.
4. **Assuming bucket_count = n:** This would miss the empty bucket guarantee. Use n+1 buckets.
5. **Not using `prev_max` correctly:** The gap is between the current bucket's min and the **previous non-empty bucket's max**, not the previous bucket's min.

### Pattern Recognition
- **Pigeonhole Principle + Bucketing:** This is a classic example of using the pigeonhole principle (n items in n+1 buckets → at least one empty bucket) to avoid full sorting.
- **Bucket Sort / Radix Sort Pattern:** When the problem requires O(n) time and values have a bounded range, consider bucket-based approaches.
- **Linear-Time Alternatives to Sorting:** Some problems can be solved without full sorting by exploiting the structure of the problem (e.g., only need gaps, not sorted order).
- **Space-Time Tradeoff:** We use O(n) extra space to achieve O(n) time instead of O(n log n).

---

## Problem 9: Custom Sort String [MEDIUM]

**Problem:** Given a string `order` (a permutation of unique lowercase letters) and a string `s`, sort `s` so that characters appear in the order defined by `order`. Characters not in `order` can be placed anywhere at the end. `order` and `s` consist of lowercase letters only.

---

### Problem Explanation (Simple Words)
We have a specific character order defined by `order` (e.g., "cba" means c comes first, then b, then a). We need to rearrange string `s` so characters appear in that order. Characters not mentioned in `order` can go at the end in any order.

### Step-by-Step Algorithm
1. **Count frequencies** of each character in `s` using `Counter`.
2. **Process `order` characters first:** For each character `ch` in `order`:
   - If `ch` exists in the counter, append `ch` repeated by its count to result.
   - Remove it from counter using `.pop()`.
3. **Append remaining characters:** Whatever is left in the counter are characters not in `order`. Append them (in any order) to the result.
4. **Return** the joined string.

### Visual Trace with Example
**Input:** `order = "cba"`, `s = "abcd"`

```
Step 1: Count characters in "abcd"
  count = {'a': 1, 'b': 1, 'c': 1, 'd': 1}

Step 2: Process order characters
  ch = 'c': in count → append 'c'×1, pop 'c'
    result = "c"
  ch = 'b': in count → append 'b'×1, pop 'b'
    result = "cb"
  ch = 'a': in count → append 'a'×1, pop 'a'
    result = "cba"

Step 3: Remaining characters in count
  count = {'d': 1}
  Append 'd' → result = "cbad"

Result: "cbad"
```

### Well-Commented Code

```python
def customSortString(order, s):
    from collections import Counter

    # Count how many times each character appears in s
    count = Counter(s)

    result = []

    # Step 1: Add characters in the order specified by 'order'
    for ch in order:
        if ch in count:
            # append() with string multiplication handles duplicates
            result.append(ch * count.pop(ch))
            # pop() both retrieves the value and removes the key

    # Step 2: Add remaining characters (not present in 'order')
    for ch, cnt in count.items():
        result.append(ch * cnt)

    # Join all parts into a single string
    return ''.join(result)


# Test cases
print(customSortString("cba", "abcd"))           # "cbad"
print(customSortString("cbafg", "abcd"))         # "cbad"
print(customSortString("bca", "aabbcc"))         # "bbbcca" or "ccabba" etc.
print(customSortString("z", "abc"))              # "abc"
print(customSortString("abc", "abc"))            # "abc"
```

### Complexity Analysis
- **Time Complexity:** O(n + m) where n = len(s) and m = len(order). Each character is processed exactly once.
- **Space Complexity:** O(n) for the counter and the result (which constructs the output string).
- **Note:** String multiplication `ch * count` creates a new string of length count; appending to a list and joining at the end is O(n).

### Edge Cases
- **`order` empty:** All characters go to the end group → result is just `s` (or sorted, depending on implementation).
- **`s` empty:** Result is empty string.
- **All `s` characters are in `order`:** The remaining `count` dict will be empty; no second pass needed.
- **No `s` characters are in `order`:** The first loop does nothing; all characters come from the second loop.
- **Duplicate characters in `s`:** Handled correctly by counter and string multiplication.
- **Characters in `order` not in `s`:** The `if ch in count` check handles this — they're simply skipped.

### Common Mistakes
1. **Using `count[ch]` instead of `count.pop(ch)`:** You need to remove the key so it doesn't appear again in the second loop. Without `.pop()`, you'd iterate over the same characters again.
2. **Sorting the remaining characters unnecessarily:** The problem says "any order" for characters not in `order`. Sorting them adds unnecessary O(k log k) overhead.
3. **Forgetting to join the result:** `''.join(result)` is needed to convert the list of strings into a single string.
4. **Modifying a dict while iterating over it:** `pop()` during the first loop is fine since we're iterating over `order`, not `count` directly.
5. **Not handling character case:** The problem specifies lowercase; if mixed case were allowed, you'd need case-insensitive comparison.

### Pattern Recognition
- **Custom Ordering with Frequency Count:** Hash map + custom priority ordering is a common pattern for "sort by a custom sequence."
- **Two-Phase Construction:** First handle items with priority, then the rest. This approach appears in many problems (e.g., Relative Sort Array).
- **Count-then-Construct:** Count frequencies first, then construct the output in the desired order. Avoids multiple passes over the input.
- **Similar Problems:** Relative Sort Array (Problem 3 of Batch 2), Sort Characters by Frequency, Custom sorting based on external ordering.

---

## Problem 10: Count of Smaller Numbers After Self [HARD]

**Problem:** Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

---

### Problem Explanation (Simple Words)
For each position in the array, count how many elements to its **right** are **smaller** than it. For example, in `[5, 2, 6, 1]`, for 5 (index 0), there are two smaller numbers to the right (2 and 1) → count[0] = 2. The brute force O(n²) approach checks every pair; we can do better using a modified merge sort.

### Step-by-Step Algorithm
1. **Pair each value with its original index:** `[(index, value), ...]` to track where results go.
2. **Modified merge sort:**
   - Recursively divide the array until single elements.
   - During merge, when we take an element from the **left** half, all `j` elements already taken from the right half are **smaller** and were originally to the right. Add `j` to that left element's count.
   - When taking from the right half, no count is added (right elements are to the right, but we only count smaller elements to the right of **left** elements).
3. **Return** the accumulated counts.

### Visual Trace with Example
**Input:** `nums = [5, 2, 6, 1]`

```
Pair with indices: [(0,5), (1,2), (2,6), (3,1)]

Divide:
  [(0,5), (1,2)]         [(2,6), (3,1)]
     [0,5]  [1,2]           [2,6]  [3,1]

Merge [0,5] and [1,2]:
  i=0 (left), j=0 (right)
  Compare 5 vs 2 → take right (2), j=1
  Compare 5 vs ... → take left (5), smaller[0] += j(=1)
  smaller = [1, 0, 0, 0]
  Merged: [(1,2), (0,5)]

Merge [2,6] and [3,1]:
  Compare 6 vs 1 → take right (1), j=1
  Compare 6 vs ... → take left (6), smaller[2] += j(=1)
  smaller = [1, 0, 1, 0]
  Merged: [(3,1), (2,6)]

Final merge: [(1,2), (0,5)] and [(3,1), (2,6)]
  i=0 (value 2), j=0 (value 1)
  Compare 2 vs 1 → take right (1), j=1
  Compare 2 vs 6 → take left (2), smaller[1] += j(=1) → smaller[1]=1
  i=1 (value 5), j=1
  Compare 5 vs 6 → take left (5), smaller[0] += j(=1) → smaller[0]=2
  Take remaining right (6): no addition
  smaller = [2, 1, 1, 0] ✓
```

### Well-Commented Code

```python
def countSmaller(nums):
    # Result array: counts[i] = number of elements smaller than nums[i] to its right
    smaller = [0] * len(nums)

    def merge_sort(enum):
        """
        Modified merge sort that counts smaller elements.
        enum is a list of (original_index, value) pairs.
        Returns sorted enum.
        """
        mid = len(enum) // 2
        if mid > 0:     # More than 1 element — need to divide
            left = merge_sort(enum[:mid])
            right = merge_sort(enum[mid:])

            merged = []
            i = j = 0

            # Merge while comparing values
            while i < len(left) or j < len(right):
                # Take from left if:
                # 1. Right is exhausted, OR
                # 2. Left element <= right element (stability: <= for equal values)
                if j == len(right) or (i < len(left) and left[i][1] <= right[j][1]):
                    # All j elements from right that were already merged are:
                    #   - Smaller than left[i] (since we take left[i] now)
                    #   - Originally to the right of left[i]
                    # So add j to left[i]'s count
                    smaller[left[i][0]] += j
                    merged.append(left[i])
                    i += 1
                else:
                    # Take from right — these are larger, no count addition
                    merged.append(right[j])
                    j += 1
            return merged
        return enum    # Base case: single element, already sorted

    # Start the merge sort with (index, value) pairs
    merge_sort(list(enumerate(nums)))
    return smaller


# Test cases
print(countSmaller([5, 2, 6, 1]))     # [2, 1, 1, 0]
print(countSmaller([-1]))              # [0]
print(countSmaller([-1, -1]))          # [0, 0]
print(countSmaller([1, 2, 3, 4]))     # [0, 0, 0, 0]
print(countSmaller([4, 3, 2, 1]))     # [3, 2, 1, 0]
```

### Complexity Analysis
- **Time Complexity:** O(n log n) — standard merge sort complexity. The extra `j` addition is O(1) per merge operation.
- **Space Complexity:** O(n) — for the temporary arrays during merge and the `smaller` result.
- **Note:** Without the merge sort approach, brute force would be O(n²).

### Edge Cases
- **Single element:** No elements to the right → count is 0.
- **Already sorted ascending:** Each element is smaller than all to its right → all counts are 0.
- **Already sorted descending:** Each element is larger than all to its right → counts are n-1, n-2, ..., 0.
- **All equal elements:** No element is strictly smaller → all counts are 0 (due to `<=` in merge condition).
- **Empty array:** Returns empty list (correctly, as `smaller` will be `[]`).

### Common Mistakes
1. **Counting equal elements as smaller:** The problem asks for **smaller** elements, not ≤. Using `<` instead of `<=` in the merge comparison would incorrectly count equal values as smaller.
2. **Forgetting to store original indices:** Without tracking original positions, we can't place counts in the correct output positions.
3. **Adding counts to right elements:** The count should only be added for **left** elements when right elements are placed before them. Right elements don't accumulate counts from left elements.
4. **Incorrect `j` accumulation:** The variable `j` tracks how many right elements have been placed so far. When we take a left element, it means all `j` previously placed right elements are smaller than it.
5. **Not creating new arrays:** In-place merge sort modification is error-prone. This implementation creates new arrays for clarity.

### Pattern Recognition
- **Merge Sort Variant:** This is the classic "count inversions" problem modified to count elements smaller than each element. The merge step is augmented with counting logic.
- **Divide and Conquer with Side Effects:** The merge sort does the sorting, but the main purpose is computing the counts. This pattern appears in many "count" problems.
- **Fenwick Tree / BIT Alternative:** This can also be solved with a Binary Indexed Tree (Fenwick Tree) by processing from right to left — a different but equally valid approach.
- **Order Statistics:** Problems involving "number of elements greater/smaller to the right/left" often use merge sort or Fenwick tree.
- **Similar Problems:** Count Inversions, Reverse Pairs (LeetCode 493), Count of Range Sum (LeetCode 327).

---

## Problem 11: Find Median from Data Stream [HARD]

**Problem:** Design a data structure that supports `addNum(num)` and `findMedian()`. `findMedian()` returns the median of all elements so far. Implement the `MedianFinder` class.

---

### Problem Explanation (Simple Words)
Numbers are added one at a time (a stream). After each addition, we need the median (middle value) of all numbers seen so far. If we had all numbers, we'd sort and pick the middle. But we can't re-sort after every addition. A two-heap approach maintains the lower half in a max-heap and the upper half in a min-heap, keeping them balanced in size.

### Step-by-Step Algorithm
1. **Maintain two heaps:**
   - `lo`: Max-heap (negated for Python) — stores the **lower** half (smaller numbers).
   - `hi`: Min-heap — stores the **upper** half (larger numbers).
2. **Invariant:** Size of `lo` ≥ size of `hi`, and difference ≤ 1.
3. **Adding a number:**
   - Push to `lo` (max-heap via negation).
   - Move the maximum from `lo` to `hi` (ensures all numbers in `lo` ≤ all numbers in `hi`).
   - If `hi` has more elements, rebalance by moving one back to `lo`.
4. **Finding median:**
   - If `lo` has more elements: median = root of `lo` (the max of the lower half).
   - If equal size: median = average of both roots.

### Visual Trace with Example
**Stream:** `[1, 2, 3, 4, 5]`

```
addNum(1):
  lo = [-1] (max-heap), hi = []
  → Move max of lo to hi: lo = [], hi = [1]
  → hi(1) > lo(0): move min of hi to lo: lo = [-1], hi = []
  findMedian: lo > hi → -(-1) = 1

addNum(2):
  lo = [-1], hi = []
  → push 2 to lo: lo = [-2, -1]
  → move max(-2 → 2) to hi: lo = [-1], hi = [2]
  → hi(1) = lo(1): balanced
  findMedian: lo == hi → (-(-1) + 2)/2 = 1.5

addNum(3):
  lo = [-1], hi = [2]
  → push 3 to lo: lo = [-3, -1], hi = [2]
  → move max(-3 → 3) to hi: lo = [-1], hi = [2, 3]
  → hi(2) > lo(1): move min(2) of hi to lo: lo = [-2, -1], hi = [3]
  findMedian: lo > hi → -(-2) = 2

... and so on
```

### Well-Commented Code

```python
import heapq

class MedianFinder:
    def __init__(self):
        # Max-heap for the lower half (store negated values)
        self.lo = []
        # Min-heap for the upper half
        self.hi = []

    def addNum(self, num):
        # Step 1: Add to max-heap (negated for Python)
        heapq.heappush(self.lo, -num)

        # Step 2: Move the largest of lo to hi
        # This ensures every element in lo <= every element in hi
        heapq.heappush(self.hi, -heapq.heappop(self.lo))

        # Step 3: Rebalance — hi should never have more elements than lo
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self):
        # If odd count, lo has the extra element (median)
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        # If even count, median is average of both roots
        return (-self.lo[0] + self.hi[0]) / 2.0


# Test cases
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2
mf.addNum(4)
print(mf.findMedian())  # 2.5
mf.addNum(5)
print(mf.findMedian())  # 3
```

### Complexity Analysis
- **Add Time:** O(log n) — heap push and pop operations.
- **Find Median Time:** O(1) — just reading heap roots.
- **Space Complexity:** O(n) — storing all elements in the two heaps.
- **Note:** The two-heap approach maintains the invariant with only 3 operations per insertion.

### Edge Cases
- **Single element:** Only `lo` has one element; median is that element.
- **Two elements:** `lo` has the smaller, `hi` has the larger; median is average.
- **All elements equal:** Both halves contain equal values; the median is that value.
- **Large stream:** O(log n) per insertion is efficient even for millions of elements.
- **Even vs odd count:** The invariant ensures `lo` always has the extra element when count is odd.

### Common Mistakes
1. **Forgetting to negate when pushing to `lo`:** Since Python has only min-heap, we store negative values to simulate max-heap. Forgetting negation means `lo[0]` gives the smallest (not largest) of the lower half.
2. **Not negating when reading from `lo`:** `self.lo[0]` is negative; you must negate it back: `-self.lo[0]`.
3. **Incorrect balancing logic:** The standard approach "push to lo, move max to hi, rebalance if hi is larger" is cleaner than comparing values to decide which heap gets the new number.
4. **Using `//` instead of `/` for even-case median:** The median of two integers may be fractional; use `/ 2.0` or cast to float.
5. **Not handling empty stream:** If no elements have been added, `findMedian()` would error. But the problem guarantees at least one add before findMedian.

### Pattern Recognition
- **Two-Heap Median:** This is the canonical solution for streaming median. One heap for each half, balanced by size.
- **Invariant Maintenance:** The key insight is maintaining the invariant that all elements in `lo` ≤ all elements in `hi`, and the size difference is at most 1.
- **Streaming Data Structures:** For any problem where you need order statistics on a data stream, consider heaps, balanced BSTs, or bucket-based approaches.
- **Similar Problems:** Sliding Window Median (Problem 39 Batch 2), Find Median from Data Stream (repeated in Batch 2).

---

## Problem 12: Minimum Cost to Make Array Equal [HARD]

**Problem:** Given an integer array `nums` and a positive integer array `cost` of the same length. You can increment or decrement any element by 1 at a cost of `cost[i]`. Return the minimum total cost to make all elements equal.

---

### Problem Explanation (Simple Words)
We have numbers with different "adjustment costs." Changing a number by 1 costs `cost[i]`. We want to pick a target value so that making all numbers equal to that target costs the least total amount. The cost function is V-shaped (convex), so we can use binary search to find the minimum point.

### Step-by-Step Algorithm
1. **Define the cost function:** `total_cost(target) = Σ(|nums[i] - target| × cost[i])` — the total cost to shift all numbers to the target.
2. **Binary search for the minimum:**
   - The function is convex (V-shaped). The derivative (discrete) changes sign at the minimum.
   - Compare `c1 = total_cost(mid)` and `c2 = total_cost(mid + 1)`.
   - If `c1 < c2`: the minimum is to the left → search left half.
   - If `c1 >= c2`: the minimum is to the right → search right half.
3. **Return** the minimum cost found.

### Visual Trace with Example
**Input:** `nums = [1, 3, 5, 2]`, `cost = [2, 3, 1, 14]`

```
lo = 1, hi = 5

Binary search:
mid = 3:
  total_cost(3) = |1-3|×2 + |3-3|×3 + |5-3|×1 + |2-3|×14
                = 4 + 0 + 2 + 14 = 20
  total_cost(4) = |1-4|×2 + |3-4|×3 + |5-4|×1 + |2-4|×14
                = 6 + 3 + 1 + 28 = 38
  20 < 38 → min is left → hi = 2

mid = 1:
  total_cost(1) = |1-1|×2 + |3-1|×3 + |5-1|×1 + |2-1|×14
                = 0 + 6 + 4 + 14 = 24
  total_cost(2) = |1-2|×2 + |3-2|×3 + |5-2|×1 + |2-2|×14
                = 2 + 3 + 3 + 0 = 8
  24 > 8 → min is right → lo = 2

mid = 2:
  total_cost(2) = 8
  lo = 2, hi = 2 → loop ends

ans = min(24, 20, 8, ...) = 8 ✓
```

### Well-Commented Code

```python
def minCost(nums, cost):
    def total_cost(target):
        """
        Compute the total cost of making all elements equal to target.
        Formula: sum(|nums[i] - target| × cost[i])
        """
        return sum(abs(n - target) * c for n, c in zip(nums, cost))

    lo, hi = min(nums), max(nums)
    ans = total_cost(lo)

    # Binary search on convex function
    while lo <= hi:
        mid = (lo + hi) // 2

        # Evaluate cost at mid and mid+1 to determine direction
        c1 = total_cost(mid)
        c2 = total_cost(mid + 1)

        # Track the minimum seen
        ans = min(ans, c1, c2)

        # Compare slopes to decide which direction to search
        if c1 < c2:
            # Minimum is to the left of mid
            hi = mid - 1
        else:
            # Minimum is to the right of mid
            lo = mid + 1

    return ans


# Test cases
print(minCost([1, 3, 5, 2], [2, 3, 1, 14]))          # 8
print(minCost([2, 2, 2, 2, 2], [4, 2, 8, 1, 3]))     # 0 (all already equal)
print(minCost([1, 10], [3, 4]))                        # 12
print(minCost([1, 2, 3], [1, 1, 1]))                   # 2
```

### Complexity Analysis
- **Time Complexity:** O(n log M) where M = max(nums) - min(nums). Each binary search step evaluates `total_cost` twice, which is O(n).
- **Space Complexity:** O(1) — only integer variables used.
- **Note:** The binary search runs over the value range, not indices. If the range is very large (e.g., 10⁹), log₂(10⁹) ≈ 30 iterations — still efficient.

### Edge Cases
- **All elements already equal:** cost is 0 (no changes needed). The algorithm correctly finds total_cost(target) = 0.
- **Single element:** No changes needed; cost is 0.
- **Large value range:** Binary search still converges in log(range) steps.
- **All costs equal (uniform cost):** The optimal target is the **median** of nums (weighted median with equal weights).
- **Very unbalanced costs:** The target will be pulled toward numbers with high costs to minimize changes to them.

### Common Mistakes
1. **Assuming optimal target is the mean or median:** With non-uniform costs, the optimal target is the **weighted median**, not the simple median or mean. This is why binary search is needed.
2. **Binary search on indices instead of values:** The search space is the range of possible target values `[min(nums), max(nums)]`, not array indices.
3. **Not tracking the minimum explicitly:** The binary search may not land exactly on the minimum (discrete function). Tracking `ans = min(ans, c1, c2)` ensures correctness.
4. **Using derivative-based methods incorrectly:** For discrete convex functions, comparing f(mid) and f(mid+1) is the discrete analog of checking the derivative sign.
5. **Forgetting abs(): The cost is |difference| × cost, not (difference)² × cost or difference × cost.

### Pattern Recognition
- **Convex Optimization via Binary Search:** If a cost function is convex (V-shaped), binary search can find the minimum efficiently. Compare adjacent values to determine direction.
- **Weighted Absolute Deviation:** This is a weighted version of the classic "minimum sum of absolute deviations" problem, where the median is the optimal solution (with equal weights).
- **Ternary Search Alternative:** For convex functions, ternary search also works but binary search on the derivative is more efficient.
- **Similar Problems:** Minimum Moves to Equal Array Elements, Best Meeting Point, Minimum Time to Complete Trips.

---

# PART B: HASHING PROBLEMS (15)

---

## Problem 13: Two Sum [EASY]

**Problem:** Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. Each input has exactly one solution, and the same element cannot be used twice.

---

### Problem Explanation (Simple Words)
Find two numbers in an array that add up to a target. Return their indices. The naive approach checks every pair (O(n²)). Using a hash map, we can do it in O(n): as we iterate, check if the `complement = target - current` has been seen before.

### Step-by-Step Algorithm
1. **Create a hash map** `seen = {}` mapping value → index.
2. **Iterate** through the array with index `i` and value `num`.
3. **Compute complement:** `complement = target - num`.
4. **Check map:** If `complement` is in `seen`, return `[seen[complement], i]`.
5. **Store current:** Otherwise, add `num → i` to the map.
6. **If loop ends:** Return `[]` (no solution found — though the problem guarantees one).

### Visual Trace with Example
**Input:** `nums = [2, 7, 11, 15]`, `target = 9`

```
i=0, num=2: complement = 9-2 = 7, 7 not in seen
  → seen = {2: 0}
i=1, num=7: complement = 9-7 = 2, 2 in seen at index 0
  → return [0, 1] ✓
```

### Well-Commented Code

```python
def twoSum(nums, target):
    # Hash map to store value -> index mapping
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num    # The other number we need

        # Check if we've seen the complement before
        if complement in seen:
            return [seen[complement], i]

        # Store current number's index for future lookups
        seen[num] = i

    # No solution found (problem guarantees one, but defensive coding)
    return []


# Test cases
print(twoSum([2, 7, 11, 15], 9))    # [0, 1]
print(twoSum([3, 2, 4], 6))          # [1, 2]
print(twoSum([3, 3], 6))             # [0, 1]
print(twoSum([1, 2, 3], 7))          # [] (no solution)
```

### Complexity Analysis
- **Time Complexity:** O(n) — single pass through the array; hash map lookups are O(1) average.
- **Space Complexity:** O(n) — in worst case, we store all elements before finding the pair.
- **Note:** The O(n²) brute force would compare every pair; the hash map trades space for time.

### Edge Cases
- **Duplicates (e.g., `[3, 3]`, target=6):** We check complement BEFORE inserting current, so we never use the same element twice. When we reach the second 3, the first 3 is already in `seen`.
- **Negative numbers:** The hash map approach works with negative numbers since `complement = target - num` handles them correctly.
- **No solution:** Returns `[]` (defensive coding). The problem guarantees exactly one solution.
- **Multiple solutions:** The problem guarantees exactly one; this approach would return the first pair found.
- **Zero target:** Works correctly — complement is `-num`.

### Common Mistakes
1. **Inserting before checking:** If we insert `seen[num] = i` before checking the complement, we might match the same element (e.g., `[3, 2, 4]`, target=6 → would match 3 with itself).
2. **Returning indices in wrong order:** The problem expects `[index1, index2]` where index1 < index2.
3. **Using a list instead of a map:** A set only tells if the complement exists, not its index. A dict is needed to return indices.
4. **Not handling the complement variable:** Forgetting to compute `target - num` leads to incorrect comparisons.
5. **Assuming sorted input:** The problem doesn't specify sorted; the hash map approach doesn't require sorting.

### Pattern Recognition
- **Complement Lookup:** The core pattern: "for each element, check if its complement exists." This appears in many problems (3 Sum, 4 Sum, Subarray Sum).
- **Single-Pass with Hash Map:** This is the classic "trade space for time" pattern. One pass builds the map while checking for matches.
- **When to use this pattern:** Any problem asking "find a pair/set that satisfies a condition" where the condition can be expressed as a complement relative to a target.
- **Variations:** Two Sum II (sorted input → two pointers), Two Sum III (data stream → BST), Two Sum BST (tree traversal + set).

---

## Problem 14: Valid Anagram [EASY]

**Problem:** Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise. An anagram means both strings contain the same characters with the same frequencies.

---

### Problem Explanation (Simple Words)
Two words are anagrams if they have the same letters with the same counts, just arranged differently. "listen" and "silent" are anagrams. We check character frequencies: if all counts match, it's an anagram.

### Step-by-Step Algorithm
1. **Length check:** If `len(s) != len(t)`, they can't be anagrams → return False.
2. **Count characters in `s`:** Increment counts for each character.
3. **Decrement for `t`:** For each character in `t`, decrement its count. If any count goes negative, `t` has more of that character than `s` → return False.
4. **Return True:** All counts are zero (or non-negative), meaning frequencies match.

### Visual Trace with Example
**Input:** `s = "anagram"`, `t = "nagaram"`

```
Length: both are 7 → continue

Count s characters:
  a: +1+1+1 = 3, n: +1, g: +1, r: +1, m: +1
  count = {'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}

Process t:
  'n': 1-1=0 ✓
  'a': 3-1=2 ✓
  'g': 1-1=0 ✓
  'a': 2-1=1 ✓
  'r': 1-1=0 ✓
  'a': 1-1=0 ✓
  'm': 1-1=0 ✓

No negative → return True ✓
```

### Well-Commented Code

```python
def isAnagram(s, t):
    # Different lengths can't be anagrams
    if len(s) != len(t):
        return False

    # Count characters in s using a dictionary
    count = {}
    for ch in s:
        count[ch] = count.get(ch, 0) + 1

    # Decrement for each character in t
    for ch in t:
        count[ch] = count.get(ch, 0) - 1
        # If any count goes negative, t has more of this char than s
        if count[ch] < 0:
            return False

    return True


# Test cases
print(isAnagram("anagram", "nagaram"))  # True
print(isAnagram("rat", "car"))          # False
print(isAnagram("a", "a"))             # True
print(isAnagram("ab", "a"))            # False (different lengths)
print(isAnagram("", ""))               # True
```

### Complexity Analysis
- **Time Complexity:** O(n) — single pass over each string.
- **Space Complexity:** O(k) where k is the number of distinct characters. For lowercase English letters, k ≤ 26 → O(1). Using a fixed 26-element array instead of a dict is more efficient for this case.
- **Note:** The early exit (negative count) can make it faster than approaches that build two full counters and compare.

### Edge Cases
- **Empty strings:** Both empty → True (same frequency of no letters).
- **Different lengths:** Immediate False.
- **Same string:** Always True (identical frequencies).
- **Unicode characters:** Python dict handles any hashable key, so any characters work.
- **Case sensitivity:** "A" and "a" are different characters unless case-folded.

### Common Mistakes
1. **Not checking length first:** Short strings with matching characters but different lengths can't be anagrams.
2. **Comparing two full dicts at the end:** This requires O(k) extra time and memory. The decrement-and-check approach is more efficient.
3. **Using `count[ch] -= 1` without `.get()`:** If `ch` isn't in the dict, this raises KeyError. Use `count.get(ch, 0)` to handle unseen characters.
4. **Returning True when dict has remaining positive counts:** If `t` is shorter (handled by length check) or has different characters (handled by negative check), this isn't an issue because we already checked lengths.
5. **Using sort-based approach:** `sorted(s) == sorted(t)` is O(n log n) and uses O(n) space. Worse than the counter approach.

### Pattern Recognition
- **Frequency Counting Pattern:** Counter-based comparison is the standard for anagram/permutation problems.
- **Character Counting Array:** For lowercase letters, a fixed 26-element list `[0] * 26` indexed by `ord(ch) - ord('a')` is more performant than a dict.
- **Decrement-and-Check:** Instead of building two full counters and comparing, decrement one counter and check for negatives — allows early exit.
- **Similar Problems:** Group Anagrams (Problem 18), Find All Anagrams in a String (Problem 23), Palindrome Permutation.

---

## Problem 15: Intersection of Two Arrays [EASY]

**Problem:** Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must be unique (no duplicates in the result).

---

### Problem Explanation (Simple Words)
Find all elements that appear in BOTH arrays. Each element should appear only once in the result even if it appears multiple times in either array. Sets are perfect for this — they automatically remove duplicates and provide fast intersection operations.

### Step-by-Step Algorithm
1. **Convert to sets:** `set1 = set(nums1)`, `set2 = set(nums2)`.
2. **Intersection:** Use set intersection operator `&` or iterate through the smaller set checking membership in the larger set.
3. **Convert back to list:** `list(set1 & set2)`.

### Visual Trace with Example
**Input:** `nums1 = [1, 2, 2, 1]`, `nums2 = [2, 2]`

```
Step 1: set1 = {1, 2}, set2 = {2}
Step 2: set1 & set2 = {2}
Step 3: list({2}) = [2]
Result: [2] ✓
```

### Well-Commented Code

```python
def intersection(nums1, nums2):
    # Convert to sets to remove duplicates
    set1 = set(nums1)
    set2 = set(nums2)

    # Set intersection operation (O(min(m, n)))
    return list(set1 & set2)


# Alternative: iterate smaller set for memory efficiency
def intersection_optimized(nums1, nums2):
    set1 = set(nums1)
    set2 = set(nums2)

    # Iterate over the smaller set to minimize operations
    if len(set1) > len(set2):
        set1, set2 = set2, set1

    return [x for x in set1 if x in set2]


# Test cases
print(sorted(intersection([1, 2, 2, 1], [2, 2])))         # [2]
print(sorted(intersection([4, 9, 5], [9, 4, 9, 8, 4])))   # [4, 9]
print(intersection([1, 2, 3], [4, 5, 6]))                  # []
print(intersection([1, 1, 1], [1, 1]))                     # [1]
```

### Complexity Analysis
- **Time Complexity:** O(m + n) — creating both sets is O(m) and O(n). Intersection with `&` is O(min(m, n)).
- **Space Complexity:** O(min(m, n)) for the result set + O(m + n) for both input sets.
- **Alternative:** If one array is much smaller, iterating the smaller set and checking membership in the larger set uses less memory.

### Edge Cases
- **No intersection:** Both sets will have empty intersection → return `[]`.
- **Duplicates within arrays:** Sets handle deduplication automatically.
- **One empty array:** `set()` & `other_set = set()` → `[]`.
- **All elements identical:** `{1} & {1} = {1}`.
- **Negative numbers:** Sets work with any hashable elements.

### Pattern Recognition
- **Set Operations for Unique Results:** Whenever the result requires unique elements, think sets.
- **Follow-up (Intersection II with duplicates):** Use `Counter` and take element-wise minimum counts to preserve multiplicities.
- **Similar Problems:** Intersection of Multiple Arrays (Batch 2, Problem 20), Find Difference of Two Arrays.

---

## Problem 16: Contains Duplicate [EASY]

**Problem:** Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

---

### Problem Explanation (Simple Words)
Check if there's any repeated number in the array. If even one number appears more than once, return True. A set is perfect: if we see the same number twice, we know there's a duplicate.

### Step-by-Step Algorithm
1. **Create an empty set** `seen`.
2. **Iterate** through each number in `nums`:
   - If the number is already in `seen` → duplicate found → return True.
   - Otherwise, add it to `seen`.
3. **If loop ends:** No duplicates → return False.

### Visual Trace with Example
**Input:** `nums = [1, 2, 3, 1]`

```
seen = {}
i=0: num=1, not in seen → add → seen = {1}
i=1: num=2, not in seen → add → seen = {1, 2}
i=2: num=3, not in seen → add → seen = {1, 2, 3}
i=3: num=1, IN seen → return True ✓
```

### Well-Commented Code

```python
def containsDuplicate(nums):
    seen = set()

    for num in nums:
        if num in seen:       # Found a duplicate
            return True
        seen.add(num)         # First occurrence — remember it

    return False              # All elements were distinct


# One-liner alternative (always processes entire array):
def containsDuplicate_oneliner(nums):
    return len(nums) != len(set(nums))


# Test cases
print(containsDuplicate([1, 2, 3, 1]))   # True
print(containsDuplicate([1, 2, 3, 4]))   # False
print(containsDuplicate([1]))             # False
print(containsDuplicate([1, 1]))          # True
print(containsDuplicate([]))              # False
```

### Complexity Analysis
- **Time Complexity:** O(n) — single pass through the array. Early exit possible on first duplicate.
- **Space Complexity:** O(n) — in the worst case (no duplicates), we store all elements.
- **One-liner:** Same complexity but always O(n) time and O(n) space — no early exit.

### Edge Cases
- **Empty array:** No elements → no duplicates → False.
- **Single element:** Can't have duplicates → False.
- **All duplicates:** First duplicate found in O(1) or O(2) steps.
- **All unique:** Must traverse entire array to confirm.
- **Large n:** Set may use significant memory (O(n)).

### Common Mistakes
1. **Using a list instead of a set:** List membership check is O(n), making the overall algorithm O(n²).
2. **Not using early exit:** `len(nums) != len(set(nums))` works but may process more elements than necessary.
3. **Forgetting that duplicates can be anywhere:** Not just adjacent — sorting isn't required.
4. **Returning True for empty array:** 0 elements means no duplicates → False.

### Pattern Recognition
- **Set for Duplicate Detection:** A set is the standard tool for checking duplicates. O(1) average membership check.
- **Early Exit:** When the condition can be satisfied before processing all elements, use early exit for efficiency.
- **Similar Problems:** Contains Duplicate II (indices within k), Contains Duplicate III (value difference within t), Find the Duplicate Number.

---

## Problem 17: Happy Number (Cycle Detection) [EASY]

**Problem:** Write an algorithm to determine if a number `n` is happy. A happy number is defined by the following process: starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat until the number equals 1, or it loops endlessly in a cycle that doesn't include 1.

---

### Problem Explanation (Simple Words)
Take a number, replace it with the sum of squares of its digits. If this eventually reaches 1, it's "happy." If it enters a cycle that never reaches 1, it's not happy. We use a set to detect cycles: if we see the same number twice, we're in a cycle.

### Step-by-Step Algorithm
1. **Compute next number:** `sum of squares of digits` of current `n`.
2. **Check termination:** If `n == 1`, return True.
3. **Cycle detection:** If `n` has been seen before, return False (we're in a cycle).
4. **Store and repeat:** Add `n` to the visited set and compute the next number.
5. **Alternative (Floyd's):** Use two pointers (slow/fast) to detect cycles with O(1) space.

### Visual Trace with Example
**Input:** `n = 19`

```
Step 1: 1² + 9² = 1 + 81 = 82    seen = {19}
Step 2: 8² + 2² = 64 + 4 = 68    seen = {19, 82}
Step 3: 6² + 8² = 36 + 64 = 100  seen = {19, 82, 68}
Step 4: 1² + 0² + 0² = 1 + 0 + 0 = 1  → Return True ✓
```

**Input:** `n = 2`

```
Step 1: 2² = 4         seen = {2}
Step 2: 4² = 16        seen = {2, 4}
Step 3: 1² + 6² = 37   seen = {2, 4, 16}
Step 4: 3² + 7² = 58   seen = {2, 4, 16, 37}
Step 5: 5² + 8² = 89   seen = {2, 4, 16, 37, 58}
... eventually reaches 4 again → cycle detected → Return False
```

### Well-Commented Code

```python
def isHappy(n):
    def get_next(num):
        """Compute sum of squares of digits without string conversion."""
        total = 0
        while num > 0:
            # divmod returns (quotient, remainder)
            num, digit = divmod(num, 10)
            total += digit * digit
        return total

    seen = set()

    # Repeat until we reach 1 or detect a cycle
    while n != 1 and n not in seen:
        seen.add(n)          # Mark current number as visited
        n = get_next(n)      # Compute next number in sequence

    # If n == 1, it's happy; if in cycle (n in seen), it's not
    return n == 1


# Test cases
print(isHappy(19))   # True  (19 → 82 → 68 → 100 → 1)
print(isHappy(2))    # False (enters cycle: 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4)
print(isHappy(1))    # True
print(isHappy(7))    # True
```

### Complexity Analysis
- **Time Per Step:** O(log n) — number of digits in n. Each step reduces the number significantly.
- **Space:** O(log n) — the set stores visited numbers. The number of steps before termination is bounded.
- **Floyd's Alternative:** O(log n) time per step, O(1) space (no set needed). Uses slow/fast pointer cycle detection.
- **Known Fact:** All unhappy numbers eventually enter the cycle: 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4.

### Edge Cases
- **n = 1:** Immediately happy (no iteration needed).
- **Large numbers:** The sum of squares quickly reduces even large numbers (e.g., 999999 → 486). So the sequence length is small.
- **Known cycles:** Unhappy numbers always fall into the known cycle. The set approach catches this.
- **Zero:** Not a positive integer; not in scope per problem statement.

### Common Mistakes
1. **Infinite loop without cycle detection:** Without a set or Floyd's, the loop would run forever on unhappy numbers.
2. **String conversion overhead:** `sum(int(d)**2 for d in str(n))` is clean but slower. The `divmod` approach is more efficient.
3. **Not handling the starting number:** Ensure the set includes `n` before changing it to the next value.
4. **Assuming all numbers converge:** Some numbers may take many steps; but the set approach handles any length.
5. **Using the wrong cycle detection:** A set works fine and is simpler; Floyd's is needed only for O(1) space requirement.

### Pattern Recognition
- **Cycle Detection with Set:** A set can detect if we revisit a state. Simple and effective when O(n) space is acceptable.
- **Floyd's Cycle Detection (Tortoise and Hare):** Use two pointers moving at different speeds. If they meet, there's a cycle. O(1) space.
- **State Machine Problems:** Any problem where you repeatedly apply a function to a state (reaching 1 or a cycle) uses this pattern.
- **Mathematical Sequences:** Collatz conjecture, happy numbers, digit DP problems.
- **Similar Problems:** Find Duplicate Number in Array (Floyd's method), Linked List Cycle.

---

## Problem 18: Group Anagrams [MEDIUM]

**Problem:** Given an array of strings `strs`, group the anagrams together. You can return the answer in any order. An anagram is a word formed by rearranging the letters of another.

---

### Problem Explanation (Simple Words)
Words that are anagrams have the same characters in the same quantities. By using a "canonical form" for each word (sorted letters or a character count tuple), all anagrams map to the same key in a hash map, making grouping trivial.

### Step-by-Step Algorithm
1. **Use a defaultdict(list)** to map keys → groups.
2. **For each string `s`:**
   - **Option A (sorted key):** Sort the characters → key = `''.join(sorted(s))`.
   - **Option B (count tuple):** Build a 26-element count array → key = `tuple(count)`.
3. **Append** `s` to `groups[key]`.
4. **Return** `list(groups.values())`.

### Visual Trace with Example
**Input:** `["eat", "tea", "tan", "ate", "nat", "bat"]`

```
Sorted key approach:
  "eat" → sorted → "aet" → groups["aet"] = ["eat"]
  "tea" → sorted → "aet" → groups["aet"] = ["eat", "tea"]
  "tan" → sorted → "ant" → groups["ant"] = ["tan"]
  "ate" → sorted → "aet" → groups["aet"] = ["eat", "tea", "ate"]
  "nat" → sorted → "ant" → groups["ant"] = ["tan", "nat"]
  "bat" → sorted → "abt" → groups["abt"] = ["bat"]

Result: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

### Well-Commented Code

```python
from collections import defaultdict

def groupAnagrams(strs):
    # Maps canonical key → list of anagram strings
    groups = defaultdict(list)

    for s in strs:
        # Option 1: Use sorted string as canonical key (simpler)
        key = ''.join(sorted(s))
        groups[key].append(s)

    # Return all groups as a list of lists
    return list(groups.values())


def groupAnagrams_optimized(strs):
    """More efficient: use character count tuple as key (O(n*k) instead of O(n*k log k))."""
    groups = defaultdict(list)

    for s in strs:
        # Build character count array (26 letters for lowercase English)
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1

        # Convert to tuple (hashable) for dictionary key
        key = tuple(count)
        groups[key].append(s)

    return list(groups.values())


# Test cases
print(groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
# [["eat","tea","ate"],["tan","nat"],["bat"]]
print(groupAnagrams([""]))  # [[""]]
print(groupAnagrams(["a"]))  # [["a"]]
print(groupAnagrams(["ab", "ba", "abc"]))  # [["ab","ba"],["abc"]]
```

### Complexity Analysis
- **Sorted Approach:** O(n × k log k) — sorting each string costs k log k.
- **Count Approach:** O(n × k) — linear scan of each string.
- **Space:** O(n × k) — storing all strings in groups.
- **Recommendation:** Use the count approach for interviews (better constant factor). The sorted approach is shorter for coding.

### Edge Cases
- **Empty string:** `""` → count tuple is all zeros → grouped with other empty strings.
- **Single character strings:** All single chars are trivially anagrams of each other if they're the same letter.
- **No anagrams:** Each string gets its own group.
- **All same string:** All grouped together.
- **Unicode / non-lowercase:** The count array approach requires knowledge of the character set. For arbitrary characters, the sorted approach is more general.

### Common Mistakes
1. **Using a list as a key:** Lists aren't hashable. Use `tuple(count)` or `''.join(sorted(s))`.
2. **Not handling empty strings:** The sorted approach works (empty string sorts to ""), count approach also works (all zeros).
3. **Assuming only lowercase letters:** The count array of size 26 works only for lowercase English letters. For broader character sets, use the sorted approach or a Counter.
4. **Returning a dict:** The problem expects `list[list[str]]`, not a dict. Use `list(groups.values())`.
5. **Using `str(sorted(s))` instead of `''.join(sorted(s))`:** `str()` on a list gives "['a', 'e', 't']", not "aet".

### Pattern Recognition
- **Canonical Form / Hashing for Grouping:** Transform each item to a canonical form, then use a hash map to group. This is a very common pattern.
- **Character Counting:** When the alphabet is known and small, a fixed-size count array is more efficient than sorting.
- **Anagram Patterns:** Anagrams have identical sorted forms or character counts. Either can serve as a hash key.
- **Similar Problems:** Valid Anagram, Find All Anagrams in a String, Group Shifted Strings.

---

## Problem 19: Subarray Sum Equals K [MEDIUM]

**Problem:** Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals `k`. Subarrays are contiguous elements.

---

### Problem Explanation (Simple Words)
Count how many contiguous subarrays (consecutive elements) have a sum exactly equal to k. For `[1, 1, 1]` and k=2, there are two subarrays: `[1, 1]` at positions 0-1 and `[1, 1]` at positions 1-2. The prefix sum technique computes subarray sums in O(1) time each.

### Step-by-Step Algorithm
1. **Initialize:** `prefix_sum = 0`, `count = 0`, hashmap `seen = {0: 1}` (prefix sum 0 appears once, meaning the empty prefix).
2. **Iterate** through each `num` in `nums`:
   - Add `num` to `prefix_sum`.
   - Check if `prefix_sum - k` exists in `seen`. If yes, add `seen[prefix_sum - k]` to count.
   - Increment `seen[prefix_sum]` by 1.
3. **Return** `count`.

### Visual Trace with Example
**Input:** `nums = [1, 1, 1]`, `k = 2`

```
Initialize: prefix=0, seen={0:1}, count=0

i=0, num=1: prefix=1
  prefix-k = 1-2 = -1 → -1 not in seen
  seen[1] = 1 → seen = {0:1, 1:1}

i=1, num=1: prefix=2
  prefix-k = 2-2 = 0 → 0 is in seen with count 1
  count += 1 → count = 1 (subarray [0..1])
  seen[2] = 1 → seen = {0:1, 1:1, 2:1}

i=2, num=1: prefix=3
  prefix-k = 3-2 = 1 → 1 is in seen with count 1
  count += 1 → count = 2 (subarray [1..2])
  seen[3] = 1 → seen = {0:1, 1:1, 2:1, 3:1}

Result: 2 ✓
```

### Well-Commented Code

```python
def subarraySum(nums, k):
    count = 0
    prefix = 0

    # Map prefix sum → frequency
    # Initialize with {0: 1} to handle subarrays that start from index 0
    seen = {0: 1}

    for num in nums:
        prefix += num              # Running prefix sum

        # If (prefix - k) was seen before, those subarrays end at current index
        if prefix - k in seen:
            count += seen[prefix - k]

        # Record the current prefix sum for future lookups
        seen[prefix] = seen.get(prefix, 0) + 1

    return count


# Test cases
print(subarraySum([1, 1, 1], 2))                      # 2
print(subarraySum([1, 2, 3], 3))                      # 2 ([1,2] and [3])
print(subarraySum([1], 0))                             # 0
print(subarraySum([0, 0, 0, 0, 0], 0))                # 15
print(subarraySum([-1, -1, 1], 0))                    # 1
```

### Complexity Analysis
- **Time Complexity:** O(n) — single pass through the array. Each operation is O(1) average.
- **Space Complexity:** O(n) — the hash map can store up to n distinct prefix sums.
- **Note:** Without this technique, the brute force would be O(n²) or O(n³).

### Edge Cases
- **k = 0:** Any element equal to 0 creates valid subarrays. Also, prefix sums that repeat indicate subarrays summing to 0.
- **All zeros `[0,0,0,0,0]`, k=0:** Every possible subarray sums to 0 → 15 (n*(n+1)/2). The hash map approach handles this correctly because each repeated 0 adds to the count.
- **Empty array:** The loop doesn't execute; returns 0.
- **Negative numbers:** The prefix sum can go up and down; the hash map approach handles negative numbers naturally.
- **Single element matching k:** `[3]` with k=3 → 1 subarray. `prefix_sum - k = 0` matches the initial `{0: 1}`.

### Common Mistakes
1. **Forgetting `{0: 1}` initialization:** Without it, subarrays starting from index 0 that sum to k are missed.
2. **Using a set instead of a map:** Multiple subarrays can have the same prefix sum. A set would miss counting all of them when a repeat occurs (e.g., zeros).
3. **Checking before updating:** The frequency of the current prefix sum should be incremented AFTER checking for `prefix_sum - k`, otherwise we might count the current element twice.
4. **Off-by-one in counting:** Each occurrence of `prefix_sum - k` represents one valid subarray ending at the current index.
5. **Confusing with two-sum:** In two-sum, we store indices. Here, we store frequencies of prefix sums.

### Pattern Recognition
- **Prefix Sum + Hash Map:** This is one of the most important patterns for subarray problems. It reduces O(n²) to O(n).
- **Key Formula:** `prefix[j] - prefix[i] = sum(i+1..j)` → subarrays with target sum are found by checking `prefix_sum - k`.
- **Frequency Matters:** We store frequencies, not booleans, because multiple subarrays can share the same prefix sum.
- **Similar Problems:** Continuous Subarray Sum (divisible by k), Subarray Sums Divisible by K, Number of Submatrices That Sum to Target, Find Pivot Index.

---

## Problem 20: Longest Consecutive Sequence [MEDIUM]

**Problem:** Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.

---

### Problem Explanation (Simple Words)
Find the longest sequence of consecutive integers (increasing by 1) in an array. The numbers can appear in any order. For example, `[100, 4, 200, 1, 3, 2]` has a sequence 1,2,3,4 → length 4. We use a set for O(1) lookups and only count from the **start** of each sequence to avoid O(n²) time.

### Step-by-Step Algorithm
1. **Convert to set:** `num_set = set(nums)` — O(1) membership checks.
2. **Iterate through the set:**
   - **Check if it's a sequence start:** If `num - 1` is NOT in the set, then `num` is the start of a consecutive sequence.
   - **Count forward:** While `num + length` is in the set, increment `length`.
   - **Update max:** Track the maximum sequence length.
3. **Return** `max_len`.

### Visual Trace with Example
**Input:** `nums = [100, 4, 200, 1, 3, 2]`

```
set = {1, 2, 3, 4, 100, 200}

num=100: 99 not in set → START
  count: 101 not in set → length=1, max_len=1

num=4: 3 IS in set → NOT a start → skip

num=200: 199 not in set → START
  count: 201 not in set → length=1, max_len=1

num=1: 0 not in set → START
  count: 2 in set → length=2
  count: 3 in set → length=3
  count: 4 in set → length=4
  count: 5 not in set → STOP, max_len=4

num=3: 2 IS in set → NOT a start → skip
num=2: 1 IS in set → NOT a start → skip

Result: 4 ✓
```

### Well-Commented Code

```python
def longestConsecutive(nums):
    # Use a set for O(1) membership checks
    num_set = set(nums)
    max_len = 0

    # Only start counting from numbers that don't have a predecessor
    # This ensures each element is visited at most twice
    for num in num_set:
        # If num-1 exists, num is NOT the start of a sequence
        if num - 1 not in num_set:
            length = 1
            # Count consecutive numbers following num
            while num + length in num_set:
                length += 1
            # Update the maximum sequence length
            max_len = max(max_len, length)

    return max_len


# Test cases
print(longestConsecutive([100, 4, 200, 1, 3, 2]))     # 4 (sequence: 1,2,3,4)
print(longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9 (0..8)
print(longestConsecutive([1, 2, 0, 1]))                # 3 (0,1,2)
print(longestConsecutive([]))                           # 0
print(longestConsecutive([9, 1, 4, 7, 3, -1, 6, 5, 2]))  # 5 (1..5)
```

### Complexity Analysis
- **Time Complexity:** O(n) — despite the nested while loop, each element is part of at most one sequence scan (only from the start). Total visits to each element across all while loops = at most n.
- **Space Complexity:** O(n) — the set stores all unique elements.
- **Proof of O(n):** The `if num-1 not in set` check ensures the while loop only runs for sequence starts. Each element is counted at most once across all while loops.

### Edge Cases
- **Empty array:** Returns 0.
- **Single element:** Returns 1 (the element itself forms a sequence of length 1).
- **All duplicates:** Set deduplicates; if all elements are the same value (e.g., `[1,1,1]`), the set only has `{1}` → length = 1.
- **Negative numbers:** Set handles negatives. Sequence can span negative to positive (e.g., `[-1, 0, 1]` → length 3).
- **Unordered input:** The set removes ordering concerns.
- **All consecutive (already perfect):** One sequence start triggers a scan of all n elements.
- **Gaps between sequences:** Each sequence start triggers a scan of its own sequence.

### Common Mistakes
1. **Not checking `num - 1` before counting:** Without this, every element starts a scan, making the algorithm O(n²) instead of O(n).
2. **Iterating over the original array (not the set):** Duplicates cause redundant work. Iterating over the set avoids counting duplicates.
3. **Using `num + 1 in set` logic incorrectly:** The while loop should check `num + length` to avoid modifying `num` and causing issues with the outer loop.
4. **Sorting the array:** Sorting would be O(n log n), violating the O(n) requirement.
5. **Not handling empty input:** Without the check, iterating over an empty set is fine, but return 0 is the expected behavior.

### Pattern Recognition
- **Set-Based Sequence Building:** A set allows O(1) lookups to build sequences from their start points.
- **Smart Start Detection:** The key insight is that you only need to start counting when you've found the **beginning** of a sequence. This avoids redundant work.
- **Tradeoff:** O(n) space for O(n) time — acceptable for the constraint.
- **Sorting Alternative:** If O(n log n) were acceptable, sorting would make this trivial (count consecutive elements in the sorted array).
- **Similar Problems:** Binary Tree Longest Consecutive Sequence, Longest Consecutive Sequence in an unsorted array.

---

## Problem 21: Sort Characters by Frequency [MEDIUM]

**Problem:** Given a string `s`, sort it in decreasing order based on the frequency of its characters. Return the sorted string. If multiple characters have the same frequency, any order among them is acceptable.

---

### Problem Explanation (Simple Words)
Count how often each character appears, then output characters from most frequent to least frequent. For "tree": t→1, r→1, e→2. Output "eert" or "eetr" (e repeated twice, then t and r in any order).

### Step-by-Step Algorithm
**Sorting Approach (O(n log n)):**
1. Count character frequencies using `Counter`.
2. Sort unique characters by `(-frequency, character)`.
3. Build result by multiplying each character by its frequency.

**Bucket Sort Approach (O(n)):**
1. Count frequencies, find `max_freq`.
2. Create `max_freq + 1` empty buckets (index = frequency).
3. Place each character in its frequency bucket.
4. Iterate from highest to lowest frequency bucket, output characters.

### Visual Trace with Example
**Input:** `s = "tree"`

```
Character frequencies:
  t: 1, r: 1, e: 2

Sorting approach:
  Sorted: e(2), r(1), t(1)
  Result: "ee" + "r" + "t" = "eert" (or "eetr")

Bucket sort approach:
  max_freq = 2
  buckets[2] = ['e']
  buckets[1] = ['t', 'r']
  freq=2: output 'e'×2 = "ee"
  freq=1: output 't'×1 + 'r'×1 = "tr"
  Result: "eetr"
```

### Well-Commented Code

```python
def frequencySort(s):
    from collections import Counter

    # Count character frequencies
    count = Counter(s)

    # Sort unique characters by (-frequency, character)
    # This puts most frequent first; alphabetical for ties
    sorted_chars = sorted(count.keys(), key=lambda c: (-count[c], c))

    # Build result: each character repeated by its frequency
    return ''.join(ch * count[ch] for ch in sorted_chars)


# Bucket sort approach for guaranteed O(n)
def frequencySort_bucket(s):
    from collections import Counter

    count = Counter(s)
    max_freq = max(count.values())

    # Create buckets: index = frequency, value = list of characters
    buckets = [[] for _ in range(max_freq + 1)]
    for ch, freq in count.items():
        buckets[freq].append(ch)

    # Output from highest frequency bucket to lowest
    result = []
    for freq in range(max_freq, 0, -1):
        for ch in buckets[freq]:
            result.append(ch * freq)

    return ''.join(result)


# Test cases
print(frequencySort("tree"))      # "eert" or "eetr"
print(frequencySort("cccaaa"))    # "aaaccc" or "cccaaa"
print(frequencySort("Aabb"))      # "bbAa" or "bbaA"
print(frequencySort("ab"))        # "ab" or "ba"
print(frequencySort("aaaabbbb"))  # "aaaabbbb"
```

### Complexity Analysis
- **Sorting Approach:** O(n log n) time, O(n) space.
- **Bucket Sort Approach:** O(n) time, O(n) space. Optimal — each character is placed in exactly one bucket.
- **Note:** The bucket sort is better in theory, but the sorting approach is simpler for interviews unless the problem explicitly requires O(n).

### Edge Cases
- **Single character:** Returns the character itself.
- **All characters same frequency e.g., "ab"`: Any order is acceptable (both freq=1).
- **Empty string:** Returns empty string.
- **Upper/lower case:** 'A' and 'a' are distinct characters (different ASCII values).
- **Spaces and special characters:** Counter handles any character.

### Common Mistakes
1. **Sorting the entire string instead of unique chars:** Sorting `sorted(s)` is O(n log n) but loses the frequency grouping. Sort unique chars only.
2. **Not handling ties properly:** The problem says "any order among them is acceptable" for same frequency, so ties don't matter.
3. **String concatenation with `+` in a loop:** O(n²) due to immutable strings. Use list and `''.join()`.
4. **Forgetting that Counter can return frequencies directly:** `count[ch]` gives the frequency for building the result.
5. **Bucket sort index starting at 1:** `range(max_freq, 0, -1)` — we skip index 0 (no characters with 0 frequency).

### Pattern Recognition
- **Frequency-Based Sorting:** Count frequencies, then sort by frequency. Very common pattern.
- **Bucket Sort Optimization:** When the maximum frequency is bounded by n, bucket sort achieves O(n).
- **Counting + Construction:** First count, then construct output in desired order. Separating counting from output makes the logic clean.
- **Similar Problems:** Top K Frequent Elements, Sort Array by Increasing Frequency (Batch 2, Problem 4).

---

## Problem 22: Top K Frequent Elements (Bucket Sort) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order. The answer is guaranteed to be unique.

---

### Problem Explanation (Simple Words)
Find the k elements that appear most frequently. For `[1,1,1,2,2,3]` and k=2, the answer is 1 and 2 (they appear 3 and 2 times respectively). Bucket sort works here because frequencies range from 1 to n (n = array length), so we can create buckets indexed by frequency.

### Step-by-Step Algorithm
1. **Count frequencies** using `Counter`.
2. **Create `n+1` buckets** (list of lists), where `buckets[freq]` holds all numbers with that frequency.
3. **Place each number** in its frequency bucket.
4. **Iterate from highest frequency** (`n`) down to 0, collecting numbers until we have k.
5. **Return** the result.

### Visual Trace with Example
**Input:** `nums = [1, 1, 1, 2, 2, 3]`, `k = 2`

```
n = 6

Frequencies:
  1 → 3, 2 → 2, 3 → 1

Buckets (0..6):
  0: []  1: [3]  2: [2]  3: [1]  4: []  5: []  6: []

Collect from highest frequency:
  freq=6: empty → skip
  freq=5: empty → skip
  freq=4: empty → skip
  freq=3: [1] → result = [1], count=1
  freq=2: [2] → result = [1, 2], count=2 → STOP

Result: [1, 2] ✓
```

### Well-Commented Code

```python
def topKFrequent(nums, k):
    from collections import Counter

    # Step 1: Count frequencies
    count = Counter(nums)
    n = len(nums)

    # Step 2: Bucket sort — index is frequency, value is list of elements
    buckets = [[] for _ in range(n + 1)]

    # Step 3: Place each element in its frequency bucket
    for num, freq in count.items():
        buckets[freq].append(num)

    # Step 4: Collect from highest frequency to lowest
    result = []
    for i in range(n, -1, -1):           # From max freq down to 0
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:         # Found k elements
                return result

    return result   # Should not reach here (guaranteed k unique elements)


# Test cases
print(sorted(topKFrequent([1, 1, 1, 2, 2, 3], 2)))      # [1, 2]
print(topKFrequent([1], 1))                                # [1]
print(sorted(topKFrequent([4, 1, -1, 2, -1, 2, 3], 2)))  # [-1, 2]
print(sorted(topKFrequent([1, 2, 2, 3, 3, 3], 2)))       # [2, 3]
```

### Complexity Analysis
- **Time Complexity:** O(n) — counting is O(n), placing in buckets is O(n), iterating buckets is O(n). No sorting required.
- **Space Complexity:** O(n) — the hash map and buckets store at most n elements.
- **Why it works:** Frequencies are bounded by n (an element can appear at most n times). Bucket size is n+1, which is O(n) — making this a linear-time algorithm.

### Edge Cases
- **k = n:** Return all unique elements (each in its own bucket if all distinct, or grouped if duplicates).
- **k = 1:** Return the single most frequent element (will be in the highest occupied bucket).
- **All elements distinct:** All frequencies = 1. All elements go to bucket 1. We return k elements from bucket 1.
- **All elements same:** Frequency = n. The single element goes to bucket n. Return it for any k.
- **Large k with many ties:** We stop as soon as we have k elements.

### Common Mistakes
1. **Forgetting that frequencies start at 1, not 0:** Bucket 0 will always be empty (no element has frequency 0). We could skip it.
2. **Creating too few or too many buckets:** Exactly n+1 buckets are needed (frequencies range 0 to n).
3. **Not stopping at k:** The problem guarantees unique answers, but collecting more than k elements would violate the requirement.
4. **Using a heap instead of bucket sort:** Both work; bucket sort is O(n) vs heap O(n log k). For interview, mention both.
5. **Assuming frequencies are bounded by a small constant:** In general, frequencies go up to n. The bucket approach uses O(n) space.

### Pattern Recognition
- **Frequency Bucketing:** When the property being counted (frequency) has a known maximum (n), bucket sort achieves linear time.
- **Linear-Time Algorithms via Exploiting Constraints:** The bounded nature of frequencies (1..n) is what makes O(n) possible. Without this constraint, we'd need O(n log k) heap or O(n log n) sort.
- **Alternative Approaches:**
  - Heap (min-heap of size k): O(n log k)
  - Quickselect (partition by frequency): O(n) average, O(n²) worst
- **Similar Problems:** Sort Characters by Frequency, Top K Frequent Words (with tie-breaking).

---

## Problem 23: Find All Anagrams in a String [MEDIUM]

**Problem:** Given two strings `s` and `p`, find all the start indices of `p`'s anagrams in `s`. Return the list of all such start indices. Strings consist of lowercase English letters only.

---

### Problem Explanation (Simple Words)
Find all starting positions in string `s` where a substring is an anagram of `p`. For example, `s = "cbaebabacd"`, `p = "abc"`: at index 0, "cba" is an anagram of "abc"; at index 6, "bac" is also an anagram. We use a sliding window of fixed size `len(p)` and compare character frequencies.

### Step-by-Step Algorithm
1. **Handle edge case:** If `len(p) > len(s)`, return `[]`.
2. **Build frequency count** for `p`.
3. **Sliding window:** Start with the first window (`s[0:len(p)]`). Compare its frequency with `p`'s. If match, add index 0.
4. **Slide:** For each position from 1 to `len(s) - len(p)`:
   - Remove leftmost character of previous window from count.
   - Add new rightmost character to count.
   - If counts match, add current start index.
5. **Return** all found indices.

### Visual Trace with Example
**Input:** `s = "abab"`, `p = "ab"`

```
p_count = {'a':1, 'b':1}

Window at index 0: "ab" → count = {'a':1, 'b':1} = p_count ✓ → result = [0]
Window at index 1: "ba" → remove 'a' (idx 0), add 'a' (idx 2)
  → count = {'b':1, 'a':1} = p_count ✓ → result = [0, 1]
Window at index 2: "ab" → remove 'b' (idx 1), add 'b' (idx 3)
  → count = {'a':1, 'b':1} = p_count ✓ → result = [0, 1, 2]

Result: [0, 1, 2] ✓
```

### Well-Commented Code

```python
from collections import Counter

def findAnagrams(s, p):
    if len(p) > len(s):
        return []

    # Count frequencies of p and the first window of s
    p_count = Counter(p)
    s_count = Counter(s[:len(p)])
    result = []

    # Check first window
    if s_count == p_count:
        result.append(0)

    # Slide the window across s
    for i in range(1, len(s) - len(p) + 1):
        # Remove leftmost character of previous window
        left_char = s[i - 1]
        s_count[left_char] -= 1
        if s_count[left_char] == 0:
            del s_count[left_char]     # Clean up zero-count entries

        # Add new rightmost character to the window
        right_char = s[i + len(p) - 1]
        s_count[right_char] += 1

        # Compare counts — if match, this window is an anagram
        if s_count == p_count:
            result.append(i)

    return result


# Test cases
print(findAnagrams("cbaebabacd", "abc"))  # [0, 6]
print(findAnagrams("abab", "ab"))         # [0, 1, 2]
print(findAnagrams("a", "a"))             # [0]
print(findAnagrams("ab", "ab"))           # [0]
print(findAnagrams("aa", "bb"))           # []
```

### Complexity Analysis
- **Time Complexity:** O(n) — we slide through `s` once. Each dict comparison is O(k) where k ≤ 26 (lowercase letters). So effectively O(26n) = O(n).
- **Space Complexity:** O(1) — dicts store at most 26 key-value pairs.
- **Match Counting Optimization:** Instead of comparing full dicts, track `formed` (how many characters match in frequency). This avoids dict comparison entirely.

### Edge Cases
- **p longer than s:** No window possible → return `[]`.
- **s equals p:** Single window at index 0 matches → `[0]`.
- **No anagrams:** Result is empty list.
- **Overlapping anagrams:** Multiple consecutive windows can match (e.g., "abab" with "ab" gives 3 matches).
- **All same characters:** If `p = "aa"` and `s = "aaaa"`: overlapping windows at 0, 1, 2 all match.
- **Empty strings:** p empty is typically not expected; if `len(p) == 0`, return `[]`.
- **Mixed case:** Problem states lowercase only; if mixed, case matters.

### Common Mistakes
1. **Not checking `len(p) > len(s)`:** This would cause index errors when slicing `s[:len(p)]`.
2. **Forgetting to clean up zero-count entries:** If a count goes to 0 but remains in the dict, comparing dicts will fail (the dict still has the key).
3. **Off-by-one in window boundaries:** The loop goes to `len(s) - len(p)` inclusive. Check edge indices carefully.
4. **Modifying `p_count`:** The pattern count should never change. Only `s_count` is updated.
5. **Using `s_count == p_count` when `s_count` has extra keys with value 0:** This is why `del s_count[left_char]` is important.

### Pattern Recognition
- **Fixed-Length Sliding Window + Frequency Map:** This is the standard pattern for "find substring with same character counts."
- **Sliding Window Variations:**
  - Fixed window (this problem): compare entire window's frequency.
  - Variable window: expand/contract to satisfy character frequency constraints.
- **Match Counting:** Instead of comparing full frequency maps, track `formed` — how many characters have exactly the right frequency. When `formed == len(unique_chars_in_p)`, we have a match.
- **Similar Problems:** Permutation in String (LeetCode 567), Minimum Window Substring (variable window), Substring with Concatenation of All Words.

---

## Problem 24: Continuous Subarray Sum (Divisible by k) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return `True` if `nums` has a good subarray with length at least 2, where the sum of the subarray is a multiple of `k`.

---

### Problem Explanation (Simple Words)
Find any contiguous subarray of length ≥ 2 whose sum is divisible by k. The key insight: if two prefix sums have the same remainder when divided by k, the subarray between them has sum divisible by k.

### Step-by-Step Algorithm
1. **Initialize:** `seen = {0: -1}` (remainder 0 at index -1 — before the array starts).
2. **Compute running prefix sum:** For each element, add to `prefix`.
3. **Compute remainder:** `rem = prefix % k`.
4. **Check if remainder seen before:**
   - If yes, and `i - seen[rem] >= 2` → found a valid subarray → return True.
   - If no, store `seen[rem] = i` (only the first occurrence).
5. **Return False** if no valid subarray found.

### Visual Trace with Example
**Input:** `nums = [23, 2, 4, 6, 7]`, `k = 6`

```
seen = {0: -1}
prefix = 0

i=0, num=23: prefix = 23, rem = 23 % 6 = 5
  rem=5 not in seen → seen[5] = 0

i=1, num=2: prefix = 25, rem = 25 % 6 = 1
  rem=1 not in seen → seen[1] = 1

i=2, num=4: prefix = 29, rem = 29 % 6 = 5
  rem=5 in seen at index 0
  i - seen[5] = 2 - 0 = 2 ≥ 2 → True ✓
  Subarray [2, 4] from index 1 to 2 sums to 6, divisible by 6
```

### Well-Commented Code

```python
def checkSubarraySum(nums, k):
    # Map remainder → first index where it occurred
    # Initialize with remainder 0 at index -1 (before array starts)
    seen = {0: -1}
    prefix = 0

    for i, num in enumerate(nums):
        # Update running prefix sum
        prefix += num
        # Compute remainder after dividing by k
        rem = prefix % k

        # If this remainder was seen before, subarray between those indices
        # has sum divisible by k
        if rem in seen:
            # Check if subarray length is at least 2
            if i - seen[rem] >= 2:
                return True
        else:
            # Store the FIRST occurrence of this remainder only
            # (we don't update existing entries to maximize subarray length)
            seen[rem] = i

    return False


# Test cases
print(checkSubarraySum([23, 2, 4, 6, 7], 6))      # True ([2,4] sum=6)
print(checkSubarraySum([23, 2, 6, 4, 7], 6))      # True ([23,2,6,4,7] sum=42)
print(checkSubarraySum([23, 2, 6, 4, 7], 13))     # False
print(checkSubarraySum([5, 0, 0, 0], 3))           # True ([0,0])
print(checkSubarraySum([0, 1, 0], 1))              # True
```

### Complexity Analysis
- **Time Complexity:** O(n) — single pass through the array.
- **Space Complexity:** O(min(n, k)) — the remainder map stores at most k distinct remainders (or n, whichever is smaller).
- **Correctness:** Based on the pigeonhole principle: if `prefix[j] % k == prefix[i] % k`, then `(prefix[j] - prefix[i]) % k == 0`, meaning `sum(nums[i+1..j])` is divisible by k.

### Edge Cases
- **k = 1:** Every number is divisible by 1. Any subarray of length ≥ 2 works. Return True for any n ≥ 2.
- **k = 0:** The modulo operation `% 0` raises ZeroDivisionError. However, the problem typically specifies k is a non-zero integer. If k could be 0, use a slightly different approach (look for `prefix[j] - prefix[i] == 0`).
- **All zeros:** `[0, 0]`, k=anything: `[0,0]` sum = 0, divisible by any k.
- **Negative numbers:** Python's `%` always returns a non-negative remainder, so this works correctly.
- **Minimum length check:** A subarray must have at least 2 elements. `i - seen[rem] >= 2` ensures this.

### Common Mistakes
1. **Not handling subarray length ≥ 2:** The condition `i - seen[rem] >= 2` is critical. Without it, a single element divisible by k would return True.
2. **Using `prefix % k` incorrectly with negative numbers:** In many languages, `%` can return negative results. Python handles this correctly (always non-negative).
3. **Initializing `{0: -1}` incorrectly:** The remainder 0 at index -1 ensures that subarrays starting from index 0 are considered. Without it, `[5, 1]` with k=6 would miss `[5,1]` (prefix sum 6, remainder 0).
4. **Updating existing remainders:** If you update `seen[rem]` to the new index, you might reduce the subarray length below 2. Only store the first occurrence.
5. **Forgetting k could be 1:** With k=1, all remainders are 0. The initial `{0: -1}` immediately gives a match when i ≥ 1.

### Pattern Recognition
- **Prefix Sum Modulo:** The modulo version of the prefix sum pattern. Used when checking divisibility by k.
- **Key Insight:** `(a - b) % k == 0` iff `a % k == b % k`. Same remainder → divisible difference.
- **Pigeonhole Principle:** After k+1 prefix sums, some remainder repeats (by pigeonhole), guaranteeing a subarray with sum divisible by k. But we need length ≥ 2.
- **Similar Problems:** Subarray Sum Equals K (without modulo, with frequencies), Subarray Sums Divisible by K, Make Sum Divisible by P.

---

## Problem 25: Minimum Index Sum of Two Lists [MEDIUM]

**Problem:** Suppose Andy and Doris want to have dinner. They each have a list of restaurants they like (as strings). Find the restaurant(s) with the minimum index sum. If multiple restaurants have the same minimum sum, return all of them in any order.

---

### Problem Explanation (Simple Words)
Two people each rank restaurants by position in their lists (lower index = higher preference). Find the common restaurant(s) with the smallest sum of positions. If "Shogun" is at index 0 in list1 and index 3 in list2, its index sum is 3. If nothing has a lower sum, "Shogun" is the answer.

### Step-by-Step Algorithm
1. **Build a hash map** from list1: restaurant name → index.
2. **Initialize** `min_sum = ∞`, `result = []`.
3. **Iterate through list2:** For each restaurant `name` at index `j`:
   - If `name` is in the map: compute `idx_sum = map1[name] + j`.
   - If `idx_sum < min_sum`: update min_sum, reset result to `[name]`.
   - If `idx_sum == min_sum`: append `name` to result.
4. **Return** `result`.

### Visual Trace with Example
**Input:**
```
list1 = ["Shogun", "Tapioca Express", "Burger King", "KFC"]
list2 = ["KFC", "Shogun", "Burger King"]
```

```
map1 = {"Shogun": 0, "Tapioca Express": 1, "Burger King": 2, "KFC": 3}
min_sum = ∞, result = []

j=0, name="KFC": in map1 at 3, sum=3+0=3 < ∞
  → min_sum=3, result=["KFC"]
j=1, name="Shogun": in map1 at 0, sum=0+1=1 < 3
  → min_sum=1, result=["Shogun"]
j=2, name="Burger King": in map1 at 2, sum=2+2=4 > 1
  → skip

Result: ["Shogun"] ✓
```

### Well-Commented Code

```python
def findRestaurant(list1, list2):
    # Build index map from the first list
    map1 = {name: i for i, name in enumerate(list1)}

    min_sum = float('inf')
    result = []

    # Scan the second list
    for j, name in enumerate(list2):
        if name in map1:
            idx_sum = map1[name] + j

            # New minimum found — reset result
            if idx_sum < min_sum:
                min_sum = idx_sum
                result = [name]
            # Tie for minimum — add to result
            elif idx_sum == min_sum:
                result.append(name)

    return result


# Test cases
print(findRestaurant(["Shogun", "Tapioca Express", "Burger King", "KFC"],
                      ["Piatti", "The Grill at Torrey Pines",
                       "Hungry Hunter Steakhouse", "Shogun"]))
# ["Shogun"]
print(findRestaurant(["Shogun", "Tapioca Express", "Burger King", "KFC"],
                      ["KFC", "Shogun", "Burger King"]))
# ["Shogun"]
print(findRestaurant(["happy", "sad", "good"],
                      ["sad", "happy", "good"]))
# ["sad", "happy"]
print(findRestaurant(["a", "b", "c"], ["d", "e", "f"]))  # []
```

### Complexity Analysis
- **Time Complexity:** O(n + m) — building map1 is O(n), scanning list2 is O(m).
- **Space Complexity:** O(n) — storing one hash map of size n.
- **Note:** We only build one map (from list1). Scanning list2 and looking up in the map avoids O(nm) brute force.

### Edge Cases
- **No common restaurants:** Returns empty list (though problem guarantees at least one).
- **Multiple restaurants with same min sum:** All are returned. E.g., same restaurant at the same position in both lists.
- **Duplicates in a list:** If a name appears more than once in list1, only the first index is stored. The problem typically has unique restaurants per list.
- **Empty lists:** If either list is empty, no common restaurants → empty result.
- **Single common restaurant:** Returns a single-element list.

### Common Mistakes
1. **Building two maps:** Unnecessary — only one map from one list is needed. The other list is iterated.
2. **Not handling ties:** If multiple restaurants share the same minimum index sum, all must be returned. Forgetting to append ties loses answers.
3. **Using `<=` for new minimum:** If `idx_sum <= min_sum`, you'd need to handle the tie case differently. Better to use `<` for new min and `==` for ties.
4. **Starting with `min_sum = 0`:** Initialize with `inf` so any valid sum is smaller.
5. **Assuming list indices start at 1:** Index sums use 0-based indices (first position = index 0).

### Pattern Recognition
- **Map + Linear Scan:** Build a lookup structure from one list, then scan the other. Classic pattern for "common elements with ranking."
- **Minimum Tracking with Ties:** Track the minimum value and maintain a result list. When new min found, reset; when tie, append.
- **Similar Problems:** Intersection of Two Arrays (uniqueness without ranking), Find Common Characters, Two Sum.

---

## Problem 26: Max Points on a Line [HARD]

**Problem:** Given an array of points where `points[i] = [xi, yi]` represents a point on the X-Y plane, return the maximum number of points that lie on the same straight line.

---

### Problem Explanation (Simple Words)
Find the largest set of points that all lie on one straight line. We check every point as a potential "anchor" and count how many other points share the same slope with it. Using reduced fraction tuples `(dy, dx)` instead of floating-point slopes avoids precision issues.

### Step-by-Step Algorithm
1. **Handle small inputs:** If ≤ 2 points, return n (a line always exists).
2. **For each point `i`:**
   - Initialize a hash map for slopes and a `duplicates` counter (starts at 1 for the point itself).
   - For each point `j > i`: compute `dx = xj - xi`, `dy = yj - yi`.
     - If `dx == 0 and dy == 0`: increment `duplicates`.
     - Otherwise, reduce `(dy, dx)` by GCD and normalize the sign.
   - Update `result = max(result, duplicates + max(slope_counts))`.
3. **Return** `result`.

### Visual Trace with Example
**Input:** `points = [[1, 1], [2, 2], [3, 3]]`

```
i=0 (1,1):
  j=1 (2,2): dx=1, dy=1, reduced=(1,1), slopes[(1,1)]=1
  j=2 (3,3): dx=2, dy=2, reduced=(1,1), slopes[(1,1)]=2
  duplicates=1
  current = 1 + 2 = 3 → result = 3

i=1 (2,2):
  j=2 (3,3): dx=1, dy=1, reduced=(1,1), slopes[(1,1)]=1
  duplicates=1
  current = 1 + 1 = 2 → result stays 3

Result: 3 ✓ (all three points on line y=x)
```

### Well-Commented Code

```python
from math import gcd
from collections import defaultdict

def maxPoints(points):
    # With 0, 1, or 2 points, they always form a line
    if len(points) <= 2:
        return len(points)

    result = 0

    for i in range(len(points)):
        # Count slopes from point i to all other points
        slopes = defaultdict(int)
        duplicates = 1     # Count point i itself

        for j in range(i + 1, len(points)):
            dx = points[j][0] - points[i][0]
            dy = points[j][1] - points[i][1]

            # Duplicate point at same coordinates
            if dx == 0 and dy == 0:
                duplicates += 1
                continue

            # Reduce fraction by GCD to normalize the slope
            g = gcd(dx, dy)
            dx //= g
            dy //= g

            # Normalize sign: make dx positive for consistent keys
            if dx < 0:
                dx, dy = -dx, -dy
            elif dx == 0:
                dy = abs(dy)    # For vertical lines, make dy positive

            slopes[(dy, dx)] += 1

        # Best line through point i: duplicates + max count of any slope
        current = duplicates + max(slopes.values(), default=0)
        result = max(result, current)

    return result


# Test cases
print(maxPoints([[1, 1], [2, 2], [3, 3]]))                            # 3
print(maxPoints([[1, 1], [3, 2], [5, 3], [4, 1], [2, 3], [1, 4]]))  # 4
print(maxPoints([[0, 0]]))                                              # 1
print(maxPoints([[0, 0], [1, -1]]))                                     # 2
print(maxPoints([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]))            # 5
```

### Complexity Analysis
- **Time Complexity:** O(n²) — for each of n points, we check all others. Each operation is O(log max(|dx|,|dy|)) for GCD.
- **Space Complexity:** O(n) — the slope map for a single point can hold up to n-1 entries.
- **Note:** This is the optimal time complexity since we must at least consider each pair of points.

### Edge Cases
- **0 or 1 point:** Returns 0 or 1 (trivially on a line).
- **2 points:** Always on the same line → return 2.
- **All points are the same coordinate:** `duplicates` will count all points. `slopes` will be empty. `result = n`.
- **Vertical line:** `dx = 0`. After reduction, we normalize to `dy = abs(dy)` so all vertical lines have slope `(1, 0)`.
- **Horizontal line:** `dy = 0`. After reduction, `dx` will be non-zero. The slope becomes `(0, 1)`.
- **Floating-point precision:** Using reduced fractions avoids issues with `dx/dy` as float that may not compare equal for collinear points.

### Common Mistakes
1. **Using float slopes:** `dy/dx` may lose precision for large coordinates or repeating decimals. Always use reduced fractions.
2. **Not normalizing sign:** `(1, 2)` and `(-1, -2)` represent the same line direction but would be different keys. Make dx > 0 to normalize.
3. **Not handling duplicates:** Points at the same coordinates count for all lines through them. They must be added to every candidate line.
4. **GCD of negative numbers:** `math.gcd` works with negative numbers, but we normalize signs before using the tuple as a key.
5. **Off-by-one with `duplicates`:** The point itself is already counted via `slopes`. `duplicates` includes the anchor point and any exact duplicates.

### Pattern Recognition
- **Slope Hashing with Fraction Normalization:** This is the standard technique for collinearity problems. Always use reduced (dy, dx) tuples with sign normalization.
- **O(n²) is Expected:** For most "find the line with most points" problems, O(n²) is the standard. No faster algorithm is known for arbitrary points.
- **Geometry Problems with Hash Maps:** Map geometric properties (slope, distance, angle) using normalized representations.
- **Similar Problems:** Check if points are collinear, Mirror Reflection, Minimum Area Rectangle.

---

## Problem 27: LRU Cache [HARD]

**Problem:** Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement the `LRUCache` class with `get(key)` and `put(key, value)` methods, both running in O(1) average time.

---

### Problem Explanation (Simple Words)
A cache with limited capacity. When full, the least recently used item is evicted. Each `get` or `put` counts as "use." We need O(1) for both operations. Python's `OrderedDict` maintains insertion order and supports `move_to_end` (mark as recently used) and `popitem` (evict least recently used).

### Step-by-Step Algorithm
1. **Initialize:** `OrderedDict` to store key-value pairs in access order, and a `capacity`.
2. **`get(key)`:**
   - If key not in cache: return -1.
   - Move key to the end (most recently used position).
   - Return the value.
3. **`put(key, value)`:**
   - If key exists: move it to the end (mark as recently used).
   - Set/update the value.
   - If cache size > capacity: pop the first item (least recently used).

### Visual Trace with Example
**Capacity = 2**

```
Operations:
  put(1,1):  cache = {1:1}                     size=1
  put(2,2):  cache = {1:1, 2:2}                size=2
  get(1):    move 1 to end → cache = {2:2, 1:1} → return 1
  put(3,3):  cache = {2:2, 1:1, 3:3}
            evict LRU (2) → cache = {1:1, 3:3}  size=2
  get(2):    2 not found → return -1
  put(4,4):  cache = {1:1, 3:3, 4:4}
            evict LRU (1) → cache = {3:3, 4:4}  size=2
  get(1):    1 not found → return -1
  get(3):    move 3 to end → cache = {4:4, 3:3} → return 3
  get(4):    move 4 to end → cache = {3:3, 4:4} → return 4
```

### Well-Commented Code

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        # OrderedDict maintains insertion/access order
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1

        # Move to end = mark as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            # If exists, mark as recently used BEFORE updating value
            self.cache.move_to_end(key)

        # Set or update the value
        self.cache[key] = value

        # If over capacity, evict the least recently used item
        # popitem(last=False) removes the first/leftmost item
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # last=False → FIFO order


# Test cases
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))     # 1
cache.put(3, 3)          # evicts key 2
print(cache.get(2))     # -1 (evicted)
cache.put(4, 4)          # evicts key 1
print(cache.get(1))     # -1 (evicted)
print(cache.get(3))     # 3
print(cache.get(4))     # 4
```

### Complexity Analysis
- **Time Complexity:** O(1) for both `get` and `put` — `OrderedDict` operations are O(1) amortized.
- **Space Complexity:** O(capacity) — at most capacity key-value pairs stored.
- **Note:** Python's `OrderedDict` is implemented with a doubly-linked list + hash map, giving O(1) for all operations.

### Edge Cases
- **Capacity = 1:** Every new `put` evicts the previous entry.
- **Putting existing key:** Updates value and marks as recently used (no eviction of this key).
- **Get on non-existent key:** Returns -1 (not None or raise error).
- **Empty cache after initialization:** `get` always returns -1 until first `put`.
- **Multiple puts with same key:** Only updates value; no duplicate entries.

### Common Mistakes
1. **Not moving to end on `get`:** The get operation counts as "use" — the item should be marked as recently used.
2. **Not moving to end on `put` update:** If key exists, `put` updates the value AND marks it as recently used.
3. **Evicting before update:** If the key exists and is the LRU, updating it should NOT evict it. Check capacity AFTER setting value.
4. **Using `popitem()` without `last=False`:** `popitem()` removes from the right (most recent) by default. Use `popitem(last=False)` to remove the leftmost (least recent).
5. **Order of `move_to_end` and assignment:** Move first, then assign. If you assign before moving, the newly assigned item is already at the end (for new keys), but for existing keys, `move_to_end` is needed.

### Pattern Recognition
- **OrderedDict for LRU:** Python's `OrderedDict` is the easiest way to implement LRU. In other languages, you'd implement a doubly-linked list + hash map.
- **Cache Eviction Policies:** LRU is the most common. Others include FIFO, LIFO, LFU (Least Frequently Used), and Random.
- **Design Problem Pattern:** LRU Cache is a classic system design/OOD problem. Interviewers often ask for the custom implementation (double-linked list + hash map) to test low-level understanding.
- **Similar Problems:** LFU Cache, Design In-Memory File System, Design a File System.

---

# PART C: HEAPS / PRIORITY QUEUE PROBLEMS (13)

---

## Problem 28: Kth Largest Element (Min Heap of Size k) [EASY]

**Problem:** Given an unsorted array of integers `nums` and an integer `k`, return the kth largest element. Note: it is the kth largest element in sorted order, not the kth distinct element.

---

### Problem Explanation (Simple Words)
Find the kth largest number in an array efficiently. Instead of sorting the entire array (O(n log n)), we maintain a min-heap of size k that keeps only the k largest elements. The smallest among these k is the kth largest overall. This is O(n log k).

### Step-by-Step Algorithm
1. **Create a min-heap** (empty).
2. **For each element** in `nums`:
   - Push the element onto the heap.
   - If heap size > k: pop the smallest (we only want the top k).
3. **After processing**, the heap contains the k largest elements. The root (`heap[0]`) is the kth largest.
4. **Return** `heap[0]`.

### Visual Trace with Example
**Input:** `nums = [3, 2, 1, 5, 6, 4]`, `k = 2`

```
heap = []

num=3: push → heap=[3]
num=2: push → heap=[2,3]
num=1: push → heap=[1,3,2], len>2 → pop=1 → heap=[2,3]
num=5: push → heap=[2,3,5], len>2 → pop=2 → heap=[3,5]
num=6: push → heap=[3,5,6], len>2 → pop=3 → heap=[5,6]
num=4: push → heap=[4,6,5], len>2 → pop=4 → heap=[5,6]

heap[0] = 5  ← 2nd largest ✓
```

### Well-Commented Code

```python
import heapq

def findKthLargest(nums, k):
    # Min-heap of size k to store the k largest elements
    heap = []

    for num in nums:
        heapq.heappush(heap, num)

        # If heap exceeds size k, remove the smallest element
        if len(heap) > k:
            heapq.heappop(heap)

    # Root of the min-heap is the kth largest
    return heap[0]


# Alternative: build heap from first k, then update
def findKthLargest_v2(nums, k):
    heap = nums[:k]
    heapq.heapify(heap)      # O(k) heapify

    for num in nums[k:]:
        # Only consider elements larger than current kth largest
        if num > heap[0]:
            # heapreplace = pop + push (more efficient than separate calls)
            heapq.heapreplace(heap, num)

    return heap[0]


# Test cases
print(findKthLargest([3, 2, 1, 5, 6, 4], 2))                   # 5
print(findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))         # 4
print(findKthLargest([1], 1))                                   # 1
print(findKthLargest([7, 7, 7, 7], 2))                         # 7
print(findKthLargest([2, 1], 1))                                # 2
```

### Complexity Analysis
- **Time Complexity:** O(n log k) — each of n elements is pushed/popped from a heap of size k.
- **Space Complexity:** O(k) — the heap stores exactly k elements.
- **When to use this:** When k is relatively small. For large k (e.g., finding median where k = n/2), Quickselect (O(n) average) is better.

### Edge Cases
- **k = 1:** Heap size is 1; `heap[0]` is the maximum element.
- **k = n:** Heap size is n; `heap[0]` is the minimum element (kth largest = smallest).
- **All equal elements:** All elements are the same; kth largest = that value.
- **Duplicates:** Counting duplicates correctly since we don't deduplicate.
- **Very large k:** If k is close to n, the heap will be large. Consider Quickselect instead.

### Common Mistakes
1. **Using a max-heap:** A max-heap would give you the kth smallest, not largest. A min-heap discarding smallest elements is correct.
2. **Not checking heap size after push:** The `len(heap) > k` check after each push is critical.
3. **Confusing with kth distinct:** This problem counts duplicates. [7,7,7,7] with k=2 → 7, not 7 (they're the same distinct value).
4. **Not handling k > len(nums):** The problem guarantees k ≤ n, so this isn't an issue.
5. **Returning before processing all elements:** All elements must be processed to guarantee correctness.

### Pattern Recognition
- **Min-Heap of Size k:** The standard pattern for "find kth largest" or "top k" problems.
- **Streaming Data:** If data arrives as a stream, this approach still works (just push each new value).
- **heapreplace Optimization:** When processing an array where most elements are smaller than the heap root, using `heapreplace` avoids unnecessary pushes/pops.
- **Quickselect Alternative:** For static arrays, Quickselect gives O(n) average time.

---

## Problem 29: Last Stone Weight [EASY]

**Problem:** You have an array of stones where `stones[i]` is the weight of the ith stone. Each turn, choose the two heaviest stones and smash them:
- If both are equal, both are destroyed.
- If different, the lighter is destroyed and the heavier is reduced by the lighter's weight.
Continue until at most one stone remains. Return the weight of the last stone, or 0 if none.

---

### Problem Explanation (Simple Words)
Simulate smashing stones. Always take the two heaviest stones. If equal → both gone. If different → subtract the lighter from the heavier (the lighter is gone, the heavier gets lighter). Repeat until 0 or 1 stone left. A max-heap is perfect for repeatedly getting the heaviest stones.

### Step-by-Step Algorithm
1. **Negate all stones** and `heapify` to create a max-heap (Python has only min-heap).
2. **While heap has ≥ 2 stones:**
   - Pop two largest (remember to negate back).
   - If they differ: push the difference (negated) back.
3. **Return** the single remaining stone weight, or 0 if empty.

### Visual Trace with Example
**Input:** `stones = [2, 7, 4, 1, 8, 1]`

```
heap = [-2, -7, -4, -1, -8, -1] → heapify → [-8, -7, -4, -1, -2, -1]

Step 1: first=-(-8)=8, second=-(-7)=7
  8 ≠ 7, diff=1 → push -1
  heap = [-4, -2, -1, -1, -1]

Step 2: first=4, second=2
  4 ≠ 2, diff=2 → push -2
  heap = [-2, -1, -1, -1]

Step 3: first=2, second=1
  2 ≠ 1, diff=1 → push -1
  heap = [-1, -1, -1]

Step 4: first=1, second=1
  equal → nothing pushed
  heap = [-1]

Result: -(-1) = 1 ✓
```

### Well-Commented Code

```python
import heapq

def lastStoneWeight(stones):
    # Negate to simulate max-heap with Python's min-heap
    heap = [-s for s in stones]
    heapq.heapify(heap)

    # Smash stones until at most one remains
    while len(heap) > 1:
        # Get two heaviest stones (negate back to positive)
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)

        if first != second:
            # Difference survives — push it back (negated)
            heapq.heappush(heap, -(first - second))

    # Return last stone weight, or 0 if none
    return -heap[0] if heap else 0


# Test cases
print(lastStoneWeight([2, 7, 4, 1, 8, 1]))    # 1
print(lastStoneWeight([1]))                     # 1
print(lastStoneWeight([1, 1]))                   # 0
print(lastStoneWeight([8, 10, 4]))               # 2
print(lastStoneWeight([9, 10, 1, 2, 3, 4]))     # 3
```

### Complexity Analysis
- **Time Complexity:** O(n log n) — each heap operation is O(log n). At most n operations.
- **Space Complexity:** O(n) — the heap stores all stones.
- **Note:** The number of operations is bounded by n (each smash reduces the total count by 0 or 1).

### Edge Cases
- **Single stone:** Returns its weight (no smashing needed).
- **Two equal stones:** Both destroyed → returns 0.
- **All stones equal weight:** They cancel in pairs → result depends on parity.
- **Large stone weights:** No overflow in Python.
- **Empty array:** Returns 0.

### Common Mistakes
1. **Forgetting to negate back:** Reading from a negated heap gives negative values. Always negate back when interpreting as stone weights.
2. **Using `heapq.heappush` with non-negated values on a negated heap:** This breaks the max-heap behavior.
3. **Pushing back the positive difference:** `(first - second)` is positive, but the heap expects negative values. Push `-(first - second)`.
4. **Not handling the empty heap case:** After the loop, if the heap is empty (all stones destroyed), return 0.
5. **Confusing which stone survives:** The heavier stone becomes `heavier - lighter`, not `lighter - heavier`.

### Pattern Recognition
- **Max-Heap via Negation:** Standard Python pattern when you need a max-heap.
- **Simulation with Heap:** When the problem describes a process that repeatedly selects the "best" element, a heap is often the right data structure.
- **Greedy with Heap:** Each step greedily picks the two largest elements.
- **Similar Problems:** Minimum Cost to Connect Sticks (greedy, always pick two smallest), Find Median from Data Stream.

---

## Problem 30: K Closest Points to Origin [EASY]

**Problem:** Given an array of points where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the k closest points to the origin (0, 0). Distance is measured by Euclidean distance.

**Approach:**
Use a max-heap of size k:
1. For each point, compute squared distance (no need for sqrt).
2. Push (negative_distance, x, y) to the heap.
3. If heap exceeds k, pop the farthest (the most negative = largest distance).
4. The heap at the end contains the k closest points.

```python
import heapq

def kClosest(points, k):
    heap = []
    for x, y in points:
        dist = -(x*x + y*y)  # negate for max-heap behavior
        heapq.heappush(heap, (dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]

# Test cases
print(kClosest([[1, 3], [-2, 2]], 1))            # [[-2, 2]]
print(kClosest([[3, 3], [5, -1], [-2, 4]], 2))   # [[3, 3], [-2, 4]]
print(kClosest([[0, 0]], 1))                       # [[0, 0]]
print(kClosest([[1, 1], [1, 1], [2, 2], [2, 2]], 2))  # [[1,1],[1,1]]
print(kClosest([[-5, 4], [-6, -5], [4, 6], [-2, 3], [-4, -3]], 3))
```

**Complexity:** O(n log k) time, O(k) space
**Trick/Tip:** Don't compute `sqrt(x*x + y*y)` — it's unnecessary and slower. Squared distances preserve the same ordering as Euclidean distances.

---

## Problem 31: Reduce Array Size to Half [EASY]

**Problem:** Given an array `arr`, you can remove any set of unique values from the array. Return the minimum number of unique values you need to remove so that at least half of the array's elements are removed.

**Approach:**
Greedy strategy:
1. Count frequency of each unique value.
2. Sort frequencies in descending order.
3. Remove most frequent values first — this minimizes the number of distinct values removed.
4. Stop when cumulative removed ≥ n/2.

```python
def minSetSize(arr):
    from collections import Counter
    counts = sorted(Counter(arr).values(), reverse=True)
    removed = 0
    half = len(arr) // 2
    for i, count in enumerate(counts):
        removed += count
        if removed >= half:
            return i + 1
    return len(counts)

# Test cases
print(minSetSize([3, 3, 3, 3, 5, 5, 5, 2, 2, 7]))  # 2
print(minSetSize([7, 7, 7, 7, 7, 7]))                 # 1
print(minSetSize([1, 9]))                               # 1
print(minSetSize([1000, 1000, 3, 7]))                   # 1
print(minSetSize([1, 2, 3, 4, 5, 6]))                  # 3
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** This is a greedy problem. Sorting by frequency in descending order and removing greedily is optimal because removing a high-frequency value eliminates more elements per "removal slot."

---

## Problem 32: Top K Frequent Elements (Heap Approach) [MEDIUM]

**Problem:** Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. The answer can be returned in any order.

**Approach:**
Use a min-heap of size k:
1. Count all element frequencies.
2. For each unique element, push (frequency, element) to heap.
3. If heap exceeds k, pop the element with lowest frequency.
4. The k most frequent elements remain in the heap.

```python
import heapq
from collections import Counter

def topKFrequent(nums, k):
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for freq, num in heap]

# Max-heap approach (push all, pop k times)
def topKFrequent(nums, k):
    count = Counter(nums)
    heap = [(-freq, num) for num, freq in count.items()]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(k)]

# Test cases
print(sorted(topKFrequent([1, 1, 1, 2, 2, 3], 2)))     # [1, 2]
print(topKFrequent([1], 1))                               # [1]
print(sorted(topKFrequent([4, 1, -1, 2, -1, 2, 3], 2))) # [-1, 2]
print(sorted(topKFrequent([1, 2, 2, 3, 3, 3], 2)))      # [2, 3]
```

**Complexity:** O(n log k) time, O(n) space
**Trick/Tip:** The min-heap approach is simpler than the max-heap approach. For O(n), use bucket sort (Problem 22). In an interview, mention both approaches.

---

## Problem 33: Sort Array by Increasing Frequency [MEDIUM]

**Problem:** Given an array of integers `nums`, sort the array in decreasing order based on the frequency of the values. If multiple values have the same frequency, sort them in decreasing order.

**Approach:**
Use a heap with custom ordering:
1. Count frequencies.
2. Push (frequency, -value) to heap — negative value ensures descending order for ties.
3. Pop from heap and build result by repeating each value `freq` times.

```python
import heapq
from collections import Counter

def frequencySort(nums):
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, -num))
    result = []
    while heap:
        freq, neg_num = heapq.heappop(heap)
        result.extend([-neg_num] * freq)
    return result

# Alternative: sorted approach
def frequencySort(nums):
    count = Counter(nums)
    return sorted(nums, key=lambda x: (count[x], -x))

# Test cases
print(frequencySort([1, 1, 2, 2, 2, 3]))  # [3, 1, 1, 2, 2, 2]
print(frequencySort([2, 3, 5, 3, 7, 9, 7, 8, 1]))  # [1, 8, 5, 9, 2, 3, 3, 7, 7]
print(frequencySort([-1, 1, -6, 4, 5, -6, 1, 4, 1]))  # [5, -1, 4, 4, -6, -6, 1, 1, 1]
print(frequencySort([1]))  # [1]
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** For the sorted approach: `sorted(nums, key=lambda x: (count[x], -x))` — `count[x]` for ascending frequency, `-x` for descending value when frequencies match.

---

## Problem 34: Reorganize String [MEDIUM]

**Problem:** Given a string `s`, rearrange the characters of `s` so that any two adjacent characters are not the same. Return any valid rearrangement, or "" if not possible.

**Approach:**
Greedy approach with max-heap:
1. Check if rearrangement is possible: max frequency ≤ (n+1) // 2.
2. Use max-heap to always pick the most frequent remaining character.
3. Track the previous character and re-insert it after using current one.
4. This prevents adjacent duplicates by always using a "cooldown" for each character.

```python
import heapq
from collections import Counter

def reorganizeString(s):
    count = Counter(s)
    if max(count.values()) > (len(s) + 1) // 2:
        return ""

    heap = [(-freq, ch) for ch, freq in count.items()]
    heapq.heapify(heap)
    result = []
    prev = None

    while heap:
        freq, ch = heapq.heappop(heap)
        result.append(ch)
        if prev:
            heapq.heappush(heap, prev)
            prev = None
        freq += 1  # increment because freq is negative
        if freq < 0:
            prev = (freq, ch)

    return ''.join(result) if len(result) == len(s) else ""

# Test cases
print(reorganizeString("aab"))         # "aba"
print(reorganizeString("aaab"))        # ""
print(reorganizeString("aaabbb"))      # "ababab"
print(reorganizeString("aaabc"))       # "abaca" or similar
print(reorganizeString("vvvlo"))       # "vlvov"
```

**Complexity:** O(n log k) where k = unique characters
**Trick/Tip:** The `prev` variable acts as a cooldown. After using a character, it can't be used again until another character is used. Re-inserting `prev` after popping the current ensures we never place same characters adjacent.

---

## Problem 35: Task Scheduler [MEDIUM]

**Problem:** You are given a character array `tasks` representing tasks a CPU needs to do. Each task takes one unit of time. The CPU can only do one task at a time. There is a non-negative integer `n` that represents the cooldown period between two same tasks. Return the least number of intervals the CPU will take to finish all tasks.

**Approach:**
Mathematical formula approach:
1. Find the maximum frequency task and count how many tasks share that frequency.
2. The minimum intervals = `(max_freq - 1) * (n + 1) + count_of_max_freq`.
3. If there are many different tasks, we can fill all idle slots, so answer = len(tasks).

```python
def leastInterval(tasks, n):
    from collections import Counter
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for v in freq.values() if v == max_freq)
    min_intervals = (max_freq - 1) * (n + 1) + max_count
    return max(len(tasks), min_intervals)

# Test cases
print(leastInterval(["A", "A", "A", "B", "B", "B"], 2))  # 8
print(leastInterval(["A", "A", "A", "B", "B", "B"], 0))  # 6
print(leastInterval(["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2))  # 16
print(leastInterval(["A", "B", "C", "D"], 2))  # 4
print(leastInterval(["A", "A", "A", "B", "B", "B"], 1))  # 6
```

**Complexity:** O(n) time, O(1) space
**Trick/Tip:** Visualize it: place max_freq tasks with n gaps between them. The `count_of_max_freq` tasks fill the last row completely. If `len(tasks) > min_intervals`, there are enough different tasks to fill all gaps, so no idle slots needed.

---

## Problem 36: Meeting Rooms II (Heap Version) [MEDIUM]

**Problem:** Given an array of meeting time intervals consisting of start and end times `[[s1, e1], [s2, e2], ...]`, find the minimum number of conference rooms required. (Duplicate of Problem 7, presented as a heap-focused solution.)

**Approach:**
Sort by start time, use min-heap:
1. Sort all meetings by their start time.
2. The heap stores end times of currently active meetings.
3. For each meeting, if the earliest meeting has ended, reuse that room.
4. Always add current meeting's end time.

```python
import heapq

def minMeetingRooms(intervals):
    if not intervals:
        return 0
    intervals.sort()  # sort by start time
    heap = [intervals[0][1]]  # first meeting's end time
    for i in range(1, len(intervals)):
        start, end = intervals[i]
        if heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)

# Alternative: event-based approach
def minMeetingRooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))    # meeting starts
        events.append((end, -1))     # meeting ends
    events.sort()
    max_rooms = 0
    current = 0
    for _, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)
    return max_rooms

# Test cases
print(minMeetingRooms([[0, 30], [5, 10], [15, 20]]))  # 2
print(minMeetingRooms([[7, 10], [2, 4]]))              # 1
print(minMeetingRooms([[1, 5], [2, 3], [4, 6]]))      # 2
print(minMeetingRooms([[1, 5], [5, 10]]))              # 1
print(minMeetingRooms([[9, 10], [4, 5], [2, 3], [5, 6], [7, 8]]))  # 1
```

**Complexity:** O(n log n) time, O(n) space
**Trick/Tip:** The event-based approach (separate start and end events) is another clean way to solve this. Sort events; start events add +1, end events add -1. Max concurrent = max running sum.

---

## Problem 37: Kth Smallest Element in a Sorted Matrix [MEDIUM]

**Problem:** Given an n x n matrix where each row and column is sorted in ascending order, find the kth smallest element in the matrix. Note that it's the kth smallest element in sorted order, not the kth distinct element.

**Approach:**
Min-heap with merge-like approach:
1. Initialize heap with the first element of each row: `(matrix[i][0], i, 0)`.
2. Pop the smallest element k times.
3. Each time you pop from row `r` at column `c`, push the next element from the same row `(matrix[r][c+1], r, c+1)`.
4. After k pops, the last popped value is the answer.

```python
import heapq

def kthSmallest(matrix, k):
    n = len(matrix)
    heap = [(matrix[i][0], i, 0) for i in range(min(n, k))]
    heapq.heapify(heap)
    for _ in range(k):
        val, row, col = heapq.heappop(heap)
        if col + 1 < n:
            heapq.heappush(heap, (matrix[row][col + 1], row, col + 1))
    return val

# Test cases
print(kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8))  # 13
print(kthSmallest([[-5]], 1))                                      # -5
print(kthSmallest([[1, 2], [3, 3]], 2))                           # 2
print(kthSmallest([[1, 3, 5], [6, 7, 8], [9, 10, 11]], 5))       # 7
```

**Complexity:** O(k log n) time, O(n) space
**Trick/Tip:** We only push to the right (same row, next column) because rows and columns are sorted. Pushing down (next row, same column) would cause duplicates and redundant processing.

---

## Problem 38: Employee Free Time [MEDIUM]

**Problem:** We are given a list of `schedule` (each element is a list of non-overlapping intervals sorted by start time) representing the schedules of employees. Find all intervals of time that are free for all employees. Return the answer in sorted order.

**Approach:**
1. Flatten all employee schedules into one list of intervals.
2. Sort by start time.
3. Merge overlapping intervals (standard merge intervals).
4. Gaps between merged intervals are free times for all employees.

```python
def employeeFreeTime(schedule):
    # Flatten all intervals
    intervals = []
    for emp in schedule:
        for interval in emp:
            intervals.append(interval)
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    # Find gaps between merged intervals
    result = []
    end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] > end:
            # Gap found: free time for all employees
            result.append([end, intervals[i][0]])
        end = max(end, intervals[i][1])
    return result

# Test cases
schedule1 = [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]
print(employeeFreeTime(schedule1))  # [[3, 4]]

schedule2 = [[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]
print(employeeFreeTime(schedule2))  # [[5, 6], [7, 9]]

schedule3 = [[[1, 2], [3, 4], [5, 6]]]
print(employeeFreeTime(schedule3))  # [[2, 3], [4, 5]]

schedule4 = [[[1, 2], [5, 6]], [[1, 3]], [[4, 10]], [[0, 15]]]
print(employeeFreeTime(schedule4))  # [] (no common free time)
```

**Complexity:** O(n log n) time where n = total intervals, O(n) space
**Trick/Tip:** This is essentially "merge intervals" + "find gaps." The key insight is that if you merge ALL employee schedules, any gap in the merged result is free for everyone. No need for per-employee tracking.

---

## Problem 39: Merge k Sorted Lists [HARD]

**Problem:** You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

**Approach:**
Min-heap approach:
1. Push the head of each non-empty list into the heap as `(value, list_index, node)`.
2. Pop the smallest, add it to the result.
3. Push the next node from the same list (if exists).
4. Use list_index to break ties when values are equal (avoids comparing node objects).

```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy
    idx = len(lists)  # unique index counter

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            idx += 1
            heapq.heappush(heap, (node.next.val, idx, node.next))

    return dummy.next

# Test cases (helper function)
def list_to_arr(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result

# list1: 1->4->5
l1 = ListNode(1, ListNode(4, ListNode(5)))
# list2: 1->3->4
l2 = ListNode(1, ListNode(3, ListNode(4)))
# list3: 2->6
l3 = ListNode(2, ListNode(6)))
print(list_to_arr(mergeKLists([l1, l2, l3])))  # [1, 1, 2, 3, 4, 4, 5, 6]
print(list_to_arr(mergeKLists([])))              # []
print(list_to_arr(mergeKLists([ListNode(1)])))   # [1]
```

**Complexity:** O(N log k) time where N = total nodes, O(k) space for the heap
**Trick/Tip:** The `idx` counter (incrementing for each push) ensures heap comparisons never compare node objects. This avoids issues when values are equal. Alternatively, use `(val, list_index, node)` where `list_index` is the original list index.

---

## Problem 40: Find Median from Data Stream (Heap Version) [HARD]

**Problem:** The median is the middle value in an ordered integer list. Design a data structure that supports `addNum(num)` and `findMedian()`. Both operations must be efficient.

**Approach:**
Two-heap approach (detailed version of Problem 11):
1. `max_heap` (lower half): stores the smaller half of numbers. We negate values since Python has min-heap.
2. `min_heap` (upper half): stores the larger half of numbers.
3. Invariant: `len(max_heap) >= len(min_heap)` and `len(max_heap) - len(min_heap) <= 1`.
4. When adding: push to max_heap first, then move max from max_heap to min_heap, then rebalance if needed.
5. Median: if odd count, max_heap root. If even, average of both roots.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap = []  # lower half (negate for max-heap)
        self.min_heap = []  # upper half

    def addNum(self, num):
        heapq.heappush(self.max_heap, -num)
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        if len(self.min_heap) > len(self.max_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))

    def findMedian(self):
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0

# Test cases
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())   # 1.5
mf.addNum(3)
print(mf.findMedian())   # 2
mf.addNum(4)
print(mf.findMedian())   # 2.5
mf.addNum(5)
print(mf.findMedian())   # 3
mf.addNum(6)
print(mf.findMedian())   # 3.5
mf.addNum(7)
print(mf.findMedian())   # 4
mf.addNum(8)
print(mf.findMedian())   # 4.5
```

**Complexity:** Add O(log n), Find Median O(1)
**Trick/Tip:** The two-step balancing (push to max_heap, then move max to min_heap, then rebalance if min_heap is larger) ensures the invariant holds. This is cleaner than comparing values to decide which heap to use. The extra element (when count is odd) is always in max_heap.

---

# QUICK REFERENCE: Key Patterns

| Pattern | Problems | Key Insight |
|---------|----------|-------------|
| Dutch National Flag | 2 | Three-way partition for 3 values in O(n) |
| Two-Heap Median | 11, 40 | Max-heap + Min-heap balanced |
| Min-Heap of Size K | 4, 28, 29, 30, 31, 32 | Root = kth largest/smallest |
| Prefix Sum + Hash | 19, 24 | Cumulative sum tracking for subarrays |
| Bucket Sort | 8, 22 | O(n) non-comparison sort |
| Topological/Scheduling | 35 | Formula-based calculation |
| LRU / Ordered Dict | 27 | O(1) get/put with ordering |
| Slope Hashing | 26 | GCD-normalized fractions |
| Merge Sort Variants | 10 | Count during merge step |
| Sliding Window + Hash | 23 | Fixed window frequency comparison |
| Greedy + Frequency | 21, 31, 33, 34 | Frequency-driven sorting |

---

# INTERVIEW TIPS FOR SORTING, HASHING & HEAPS

1. **Always clarify constraints**: What's the range of values? Can you modify the input? Is stability needed?

2. **Know your complexity targets**:
   - Sorting: O(n log n) is standard, O(n) with bucket/counting sort
   - Hashing: O(1) amortized per operation
   - Heaps: O(log n) push/pop, O(1) peek

3. **Python heap is min-heap only**: Negate values for max-heap behavior. Use `(priority, item)` tuples for custom ordering.

4. **Hash map patterns**:
   - Two Sum style: store complement
   - Prefix sum: store cumulative sums
   - Grouping: use canonical key (sorted string, reduced fraction)
   - Frequency counting: Counter is your friend

5. **Heap patterns**:
   - Kth largest/smallest: min-heap of size k
   - Merge k sorted: heap with k elements
   - Running median: two heaps
   - Task scheduling: formula or simulation

6. **Edge cases to always check**:
   - Empty arrays/lists
   - Single element
   - All elements same
   - All elements different
   - Negative numbers
   - Integer overflow (not in Python, but mention it)

---

# COMMON MISTAKES TO AVOID

1. **Forgetting to negate in Python max-heap**: All solutions using negated values for max-heap behavior — forgetting to negate back gives wrong answers.

2. **Off-by-one in prefix sum**: Forgetting `{0: 1}` initialization causes missed subarrays starting from index 0.

3. **Not checking `num - 1 not in set`**: Without this check in Longest Consecutive Sequence, you revisit every element multiple times → O(n²).

4. **Floating-point slopes**: Using `dy/dx` as slope key causes precision issues. Always use reduced fraction tuples `(dy, dx)` with GCD.

5. **Modifying dict during iteration**: When iterating over a hash map and modifying it, use a copy or collect keys first.

6. **Heap comparison failures**: When pushing objects to heap, ensure all elements are comparable. Use `(priority, unique_id, object)` pattern.

7. **Edge case in Two Sum**: The same element cannot be used twice — check before inserting into the map.

8. **Kth Largest confusion**: kth largest ≠ kth distinct. Problem 5 counts duplicates; use a set if distinct is needed.

9. **Not handling empty input**: Always check for empty arrays, lists, or strings before processing.

10. **Stack overflow in recursion**: Deep recursion in merge sort or quickselect can hit Python's recursion limit. For large inputs, consider iterative approaches or increase limit with `sys.setrecursionlimit()`.

---

> **Total: 40 Problems | 1800+ lines | Sorting (12) + Hashing (15) + Heaps (13)**
> **Difficulty: Easy (12) + Medium (18) + Hard (10)**
> **All solutions include: Complete Python code, test cases, complexity analysis, and interview tips**
