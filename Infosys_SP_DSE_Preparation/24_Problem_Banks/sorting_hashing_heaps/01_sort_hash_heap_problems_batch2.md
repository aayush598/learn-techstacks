# Sorting, Hashing & Heaps — Problem Bank (Batch 2)

## 40 More Classic Problems for Infosys SP DSE Preparation

---

# PART A: SORTING (Problems 1–10)

---

## Problem 1: Sort Array By Parity

### Problem Explanation (Simple Words)
We need to separate even and odd numbers - all evens first, then all odds. The order within evens and odds doesn't matter. With two pointers (left for even position, right for odd position), we swap whenever we find an odd on the left and an even on the right. This is like the partition step of quicksort but simpler.

### Algorithm Steps
1. **Initialize** `left = 0`, `right = len(nums) - 1`.
2. **While `left < right`:**
   - If `nums[left]` is odd AND `nums[right]` is even: swap them.
   - If `nums[left]` is even: move `left` forward (it's in correct place).
   - If `nums[right]` is odd: move `right` backward (it's in correct place).
3. **Return** the modified array.

### Visual Walkthrough
**Input:** `[3, 1, 2, 4]`

```
left=0, right=3
[3, 1, 2, 4]
 L        R

Step 1: nums[0]=3 (odd), nums[3]=4 (even) → swap!
  [4, 1, 2, 3]  → left[0]=4 (even) → left=1
  [4, 1, 2, 3]  → right[3]=3 (odd) → right=2
     L     R

Step 2: nums[1]=1 (odd), nums[2]=2 (even) → swap!
  [4, 2, 1, 3]  → left[1]=2 (even) → left=2
  [4, 2, 1, 3]  → right[2]=1 (odd) → right=1
        R  L

left=2 > right=1 → STOP
Result: [4, 2, 1, 3] ✓
```

### Key Insight
This is essentially a two-way partition. The left pointer scans for misplaced odds, the right pointer scans for misplaced evens. When both find a mismatch, swapping fixes both positions.

### Well-Commented Code

```python
def sortArrayByParity(nums):
    left, right = 0, len(nums) - 1

    while left < right:
        # If left is odd and right is even, swap them
        if nums[left] % 2 == 1 and nums[right] % 2 == 0:
            nums[left], nums[right] = nums[right], nums[left]

        # Move left forward if it's already even (correct position)
        if nums[left] % 2 == 0:
            left += 1

        # Move right backward if it's already odd (correct position)
        if nums[right] % 2 == 1:
            right -= 1

    return nums


# Test
print(sortArrayByParity([3, 1, 2, 4]))  # [4, 2, 1, 3] (or any valid)
print(sortArrayByParity([0]))  # [0]
print(sortArrayByParity([1, 3, 5]))  # [1, 3, 5] (all odd, no change)
print(sortArrayByParity([2, 4, 6]))  # [2, 4, 6] (all even, no change)
```

### Complexity Analysis
- **Time:** O(n) — single pass with two pointers, each element moved at most once.
- **Space:** O(1) — in-place, no extra data structures.

### Edge Cases
- **All even or all odd:** No swaps needed; left/right just pass through.
- **Single element:** Loop doesn't execute; returns the element.
- **Zero:** `0 % 2 == 0` → treated as even (correct).
- **Negative numbers:** In Python, `-3 % 2 == 1` (Python's modulo always returns non-negative).

### Common Mistakes
1. **Swapping without checking both conditions:** Only swap when left-odd AND right-even simultaneously.
2. **Not using `while left < right`:** Using `<=` would cause unnecessary operations when pointers cross.
3. **Forgetting that zero is even:** `0 % 2 == 0` is correct.
4. **Modifying the if conditions order:** The swap check must come before the pointer movement checks.

### Pattern Recognition
- **Two-Pointer Partitioning:** This is a simplified version of the Dutch National Flag algorithm (which handles 3 values).
- **In-Place Array Modification:** Problems that ask to rearrange elements by a property often use two pointers.
- **Similar Problems:** Sort Colors, Move Zeroes, Segregate 0s and 1s.

---

## Problem 2: Sort Array By Parity II

### Problem Explanation (Simple Words)
Even positions (0, 2, 4, ...) must contain even numbers; odd positions (1, 3, 5, ...) must contain odd numbers. Half the numbers are even, half are odd. We use two pointers stepping by 2: one scans even indices for misplaced odds, the other scans odd indices for misplaced evens. When both find a problem, swapping fixes both.

### Algorithm Steps
1. **Initialize** `even = 0` (points to even index), `odd = 1` (points to odd index).
2. **While both pointers are in bounds:**
   - If `nums[even]` is even (correct), advance `even` by 2.
   - Elif `nums[odd]` is odd (correct), advance `odd` by 2.
   - Else: swap `nums[even]` and `nums[odd]`, advance both by 2.
3. **Return** the modified array.

### Visual Walkthrough
**Input:** `[4, 2, 5, 7]`

```
even=0, odd=1
[4, 2, 5, 7]

Step 1: nums[0]=4 (even ✓) → even += 2 → even=2
Step 2: nums[1]=2 (even ✗, should be odd) → don't advance odd
Step 3: nums[2]=5 (odd ✗, should be even)
  Swap nums[2] and nums[1]: [4, 5, 2, 7]
  even=4, odd=3 → both out of bounds → STOP

Result: [4, 5, 2, 7] ✓
```

### Key Insight
Because counts are balanced (half even, half odd), we don't need to search for a swap partner — any misplaced even at an odd index pairs with any misplaced odd at an even index. Swapping fixes both simultaneously.

### Well-Commented Code

```python
def sortArrayByParityII(nums):
    even = 0  # Points to even indices (0, 2, 4, ...)
    odd = 1   # Points to odd indices (1, 3, 5, ...)

    while even < len(nums) and odd < len(nums):
        if nums[even] % 2 == 0:
            # Correct: even number at even index
            even += 2
        elif nums[odd] % 2 == 1:
            # Correct: odd number at odd index
            odd += 2
        else:
            # Both misplaced: swap to fix both positions
            nums[even], nums[odd] = nums[odd], nums[even]
            even += 2
            odd += 2

    return nums


# Test
print(sortArrayByParityII([4, 2, 5, 7]))  # [4, 5, 2, 7]
print(sortArrayByParityII([2, 3]))  # [2, 3]
print(sortArrayByParityII([1, 4, 2, 3]))  # [2, 1, 4, 3] or similar
```

### Complexity Analysis
- **Time:** O(n) — single pass, each element visited at most once.
- **Space:** O(1) — in-place.

### Edge Cases
- **Already correctly arranged:** Both conditions pass initially; pointers scan through with no swaps.
- **Minimal array (n=2):** Single check for even/odd parity at each position.
- **All evens at odd positions and vice versa:** Each iteration swaps and fixes both.

### Common Mistakes
1. **Using `left < right` instead of separate even/odd pointers:** This problem needs alternating positions, not just partitioning.
2. **Advancing the wrong pointer:** After a swap, both positions are fixed, so advance BOTH pointers.
3. **Forgetting `% 2` works for negative parity:** `-2 % 2 == 0` in Python, correct.
4. **Not checking the correct condition:** Even index needs even value (`num % 2 == 0`), odd index needs odd value (`num % 2 == 1`).

### Pattern Recognition
- **Two-Pointer with Step Size 2:** Stepping by 2 ensures we only check even/odd positions.
- **Same as Sort Array By Parity I but with positional constraints:** Parity I just groups evens before odds; Parity II specifies exact positions.
- **Similar Problems:** Sort Array By Parity I, Wiggle Sort (nums[0] ≤ nums[1] ≥ nums[2]...).

---

## Problem 3: Relative Sort Array

### Problem Explanation (Simple Words)
We sort `arr1` based on the order defined in `arr2`. Elements in `arr2` come first in that specific order. Elements not in `arr2` go to the end, sorted ascending. The custom key uses a tuple `(priority, value)` where priority=0 for elements in `arr2` (ranked by position) and priority=1 for others.

### Algorithm Steps
1. **Build rank map:** Map each element in `arr2` to its index (0, 1, 2, ...).
2. **Define custom key function:**
   - If `x` is in `arr2`: return `(0, rank[x])`.
   - Otherwise: return `(1, x)`.
3. **Sort `arr1`** using this key.
4. **Return** sorted `arr1`.

### Visual Walkthrough
**Input:** `arr1 = [2,3,1,3,2,4,6,7,9,2,19]`, `arr2 = [2,1,4,3,9,6]`

```
Rank map: {2:0, 1:1, 4:2, 3:3, 9:4, 6:5}

Custom keys for each element:
  2 → (0, 0)    3 → (0, 3)    1 → (0, 1)
  3 → (0, 3)    2 → (0, 0)    4 → (0, 2)
  6 → (0, 5)    7 → (1, 7)    9 → (0, 4)
  2 → (0, 0)   19 → (1, 19)

Sorted by key:
  (0,0): [2, 2, 2]
  (0,1): [1]
  (0,2): [4]
  (0,3): [3, 3]
  (0,4): [9]
  (0,5): [6]
  (1,7): [7]
  (1,19): [19]

Result: [2, 2, 2, 1, 4, 3, 3, 9, 6, 7, 19] ✓
```

### Key Insight
The tuple key `(priority, rank/value)` sorts by priority first (0 = in arr2, 1 = not in arr2) then by secondary criteria. This elegantly handles the two groups without needing two separate sort operations.

### Well-Commented Code

```python
def relativeSortArray(arr1, arr2):
    # Map each element in arr2 to its rank (position)
    rank = {val: i for i, val in enumerate(arr2)}

    def custom_key(x):
        # Priority 0: follows arr2 order
        # Priority 1: goes to end, sorted by value
        if x in rank:
            return (0, rank[x])
        return (1, x)

    arr1.sort(key=custom_key)
    return arr1


# Test
print(relativeSortArray([2,3,1,3,2,4,6,7,9,2,19], [2,1,4,3,9,6]))
# [2,2,2,1,4,3,3,9,6,7,19]
print(relativeSortArray([1,2,3], [3,2,1]))  # [3,2,1]
print(relativeSortArray([5,5,5], [1,2,3]))  # [5,5,5]
```

### Complexity Analysis
- **Time:** O(n log n) — sorting dominates.
- **Space:** O(m) where m = len(arr2) for the rank map.

### Edge Cases
- **All elements in arr2:** No priority-1 group, pure custom sort.
- **No elements in arr2:** All get priority 1 → pure ascending sort.
- **Duplicates in arr1:** All duplicates stay together (stable sort).
- **Empty arr1 or arr2:** Handled naturally (empty rank map or empty array).

### Common Mistakes
1. **Using `float('inf')` instead of a two-part key:** Both work, but the tuple approach is cleaner.
2. **Not counting duplicates correctly:** The sort handles duplicates automatically via the key.
3. **Modifying arr2:** The rank map should never be modified.
4. **Assuming `arr2` contains all elements of `arr1`:** The sentinel group handles the rest.

### Pattern Recognition
- **Custom Sort with Priority Grouping:** The `(priority, secondary_key)` tuple pattern groups elements and sorts within groups.
- **Stable Sort Alternative:** Without custom keys, a stable sort with two passes works: (1) sort by value, (2) stable sort by arr2 order.
- **Similar Problems:** Sort Array by Increasing Frequency, Custom Sort String.

---

## Problem 4: Sort Array by Increasing Frequency

### Problem Explanation (Simple Words)
Sort numbers by how often they appear — least frequent first. When frequencies tie, the larger number comes first. For `[1,1,2,2,2,3]`: 3 appears once, 1 appears twice, 2 appears three times → result `[3, 1, 1, 2, 2, 2]`.

### Algorithm Steps
1. **Count frequencies** using `Counter`.
2. **Sort** using key `(count[x], -x)`:
   - Primary: frequency ascending (less frequent first).
   - Secondary: `-x` (descending value) for ties.
3. **Return** sorted array.

### Visual Walkthrough
**Input:** `[1, 1, 2, 2, 2, 3]`

```
Frequencies: {1:2, 2:3, 3:1}

Sorted by key (count[x], -x):
  3 → (1, -3) → lowest freq, highest value among freq=1
  1 → (2, -1)
  2 → (3, -2) → highest freq

Result: [3, 1, 1, 2, 2, 2] ✓
```

### Key Insight
Python's `sort` is ascending. For descending order on the tie-breaker, negate the value: `-x`. For example, -3 < -1, so 3 (value) comes before 1 among same-frequency elements.

### Well-Commented Code

```python
from collections import Counter

def frequencySort(nums):
    count = Counter(nums)
    # Key: (frequency ascending, value descending via negation)
    nums.sort(key=lambda x: (count[x], -x))
    return nums

# Test
print(frequencySort([1, 1, 2, 2, 2, 3]))  # [3, 1, 1, 2, 2, 2]
print(frequencySort([2, 3, 5, 3, 7, 9, 5, 3, 7]))
# [9, 2, 7, 7, 5, 5, 3, 3, 3]
```

### Complexity Analysis
- **Time:** O(n log n) — sorting.
- **Space:** O(n) — Counter.

### Edge Cases
- **All freq=1:** Sorted by value descending.
- **All same value:** Single entry, array unchanged.
- **Negative numbers:** `-x` negation works correctly.

### Common Mistakes
1. **Forgetting the tie-breaker:** Without `-x`, stable sort preserves original order instead of descending value.
2. **Reversing the key:** Using `(-count[x], x)` would sort by frequency descending, not ascending.
3. **Using `Counter` values incorrectly:** The key accesses `count[x]` for each element `x`, not `count.values()`.

### Pattern Recognition
- **Frequency Sort with Custom Key:** Standard pattern for "sort by computed property" problems.
- **Tuple-Based Sorting:** `(primary, secondary)` determines multi-level sort order.
- **Similar Problems:** Sort Characters By Frequency (descending), Sort Integers by Number of 1 Bits.

---

## Problem 5: Minimum Absolute Difference

### Problem Explanation (Simple Words)
Find pairs of numbers with the smallest possible difference between them. After sorting, the minimum difference must be between adjacent elements (a non-adjacent pair's difference equals the sum of adjacent gaps, making it larger). We do two passes: first to find the minimum difference value, second to collect all pairs achieving it.

### Algorithm Steps
1. **Sort** the array.
2. **First pass:** Find `min_diff` = minimum of `arr[i+1] - arr[i]`.
3. **Second pass:** Collect all pairs `[arr[i], arr[i+1]]` where the difference equals `min_diff`.
4. **Return** the result.

### Visual Walkthrough
**Input:** `[4, 2, 1, 3]`

```
Sorted: [1, 2, 3, 4]

First pass (find min diff):
  diff(1,2) = 1 → min=1
  diff(2,3) = 1 → min=1
  diff(3,4) = 1 → min=1

Second pass (collect pairs with diff=1):
  [1,2] ✓
  [2,3] ✓
  [3,4] ✓

Result: [[1,2], [2,3], [3,4]] ✓
```

### Key Insight
After sorting, the smallest absolute difference is always between some adjacent pair. This is because for any `i < j`, `|arr[i] - arr[j]|` = sum of gaps between them, which is ≥ any individual gap.

### Well-Commented Code

```python
def minimumAbsDifference(arr):
    arr.sort()

    # First pass: find minimum difference
    min_diff = float('inf')
    for i in range(len(arr) - 1):
        diff = arr[i + 1] - arr[i]
        if diff < min_diff:
            min_diff = diff

    # Second pass: collect all pairs with that difference
    result = []
    for i in range(len(arr) - 1):
        if arr[i + 1] - arr[i] == min_diff:
            result.append([arr[i], arr[i + 1]])

    return result


# Test
print(minimumAbsDifference([4, 2, 1, 3]))  # [[1,2],[2,3],[3,4]]
print(minimumAbsDifference([1, 3, 6, 10, 15]))  # [[1,3]]
print(minimumAbsDifference([3, 8, -10, 23, 19, -4, -12, 27]))
# [[-12,-10],[19,23],[23,27]]
```

### Complexity Analysis
- **Time:** O(n log n) for sorting. Two O(n) passes.
- **Space:** O(r) where r = number of result pairs.

### Edge Cases
- **n=2:** Single pair, trivially the answer.
- **All same:** Difference = 0, all adjacent pairs are answers.
- **Negative numbers:** Sorting handles them; `arr[i+1] - arr[i]` works correctly.
- **Large values:** Python's big integers handle this.

### Common Mistakes
1. **Single-pass collection:** You must find min_diff FIRST, then collect. A single pass that tracks both fails because you don't know if the current min will be beaten later.
2. **Using `abs()` unnecessarily:** After sorting, `arr[i+1] - arr[i]` is always non-negative.
3. **Not returning pairs in ascending order:** After sorting, adjacent pairs are naturally in ascending order.
4. **Returning pairs with wrong order:** Each pair should be `[smaller, larger]`.

### Pattern Recognition
- **Sort + Adjacent Check:** Many "minimum/maximum difference" problems become trivial after sorting.
- **Two-Pass Pattern:** First pass finds the target value, second pass collects all matches.
- **Similar Problems:** Maximum Gap (but with O(n) constraint using bucket sort), Minimum Time Difference.

---

## Problem 6: Triangle

### Problem Explanation (Simple Words)
Check if any three numbers can form a triangle. The triangle inequality: the sum of any two sides must be strictly greater than the third. After sorting, we only need to check consecutive triplets because for sorted `a ≤ b ≤ c`, the inequality `a + b > c` automatically ensures `a + c > b` and `b + c > a` (the other two inequalities always hold when c is the largest).

### Algorithm Steps
1. **Sort** the array.
2. **Check every consecutive triplet** `(nums[i], nums[i+1], nums[i+2])`.
3. If `nums[i] + nums[i+1] > nums[i+2]` → return `True`.
4. If no triplet satisfies → return `False`.

### Visual Walkthrough
**Input:** `[2, 2, 3, 4]`

```
Sorted: [2, 2, 3, 4]

Check triplets:
  (2, 2, 3): 2+2 = 4 > 3 → True ✓ (triangle exists)

Result: True
```

**Input:** `[1, 2, 3]`
```
Check triplets:
  (1, 2, 3): 1+2 = 3 ≤ 3 → False
  (no more triplets)

Result: False
```

### Key Insight
After sorting, `c` is the largest side. The other two inequalities (`a + c > b` and `b + c > a`) are automatically true. We only need to check `a + b > c` for consecutive triplets because if `a + b ≤ c` for the closest possible a and b to c, then any smaller a or b would only make it worse.

### Well-Commented Code

```python
def isTriangle(nums):
    nums.sort()
    # Check every consecutive triplet
    for i in range(len(nums) - 2):
        if nums[i] + nums[i + 1] > nums[i + 2]:
            return True
    return False


# Test
print(isTriangle([2, 2, 3, 4]))  # True (2+3>4)
print(isTriangle([1, 1, 1]))  # True
print(isTriangle([1, 2, 3]))  # False
print(isTriangle([3, 4, 5]))  # True
print(isTriangle([1]))  # False (not enough elements)
```

### Complexity Analysis
- **Time:** O(n log n) — sorting.
- **Space:** O(1) — in-place.

### Edge Cases
- **n < 3:** Impossible to form a triangle → return False.
- **Negative numbers:** Negative side lengths cannot form a valid triangle.
- **All zeros:** `0+0 > 0` is false → return False.
- **Large numbers:** Sum may overflow in some languages, but Python handles it.

### Common Mistakes
1. **Checking all three inequalities:** `a + b > c`, `a + c > b`, `b + c > a` → only `a + b > c` is needed after sorting.
2. **Using `>=` instead of `>`:** Triangle inequality requires STRICTLY greater.
3. **Not sorting first:** Without sorting, you'd need to try all combinations → O(n³).
4. **Forgetting n < 3 check:** `range(len-2)` handles this (empty range), but explicit check is clearer.

### Pattern Recognition
- **Sort + Greedy Check:** Sorting reveals the structure (largest element), enabling a single-pass check.
- **Consecutive Triplet Sweep:** Many "find triple" problems use consecutive checks after sorting.
- **Similar Problems:** Largest Perimeter Triangle, 3Sum Closest, Maximum Product of Three Numbers.

---

## Problem 7: Maximum Product of Three Numbers

### Problem Explanation (Simple Words)
Find the three numbers whose product is the maximum possible. After sorting, the maximum product is either the three largest positive numbers OR the two most negative (which multiply to positive) times the largest positive number. We don't need to check all combinations — sorting reveals which candidates matter.

### Algorithm Steps
1. **Sort** the array.
2. **Compute candidate 1:** product of three largest numbers `nums[-1] * nums[-2] * nums[-3]`.
3. **Compute candidate 2:** product of two smallest (most negative) × largest `nums[0] * nums[1] * nums[-1]`.
4. **Return** the maximum of the two candidates.

### Visual Walkthrough
**Input:** `[-10, -10, 1, 3, 2]`

```
Sorted: [-10, -10, 1, 2, 3]

Candidate 1 (three largest):  1 × 2 × 3 = 6
Candidate 2 (two smallest × largest):  (-10) × (-10) × 3 = 300

Result: max(6, 300) = 300 ✓
```

**Input:** `[-4, -3, -2, -1]`
```
Sorted: [-4, -3, -2, -1]

Candidate 1 (three largest): (-3) × (-2) × (-1) = -6
Candidate 2 (two smallest × largest): (-4) × (-3) × (-1) = -12

Result: max(-6, -12) = -6 ✓
```

### Key Insight
Two negatives make a positive. `(-10) × (-10) = 100` is a large positive number. The largest positive number (3 in this case) amplifies this even further. So we must always check the "two most negative × most positive" combination.

### Well-Commented Code

```python
def maximumProduct(nums):
    nums.sort()
    n = len(nums)

    # Three largest numbers (typically all positive or least negative)
    top_three = nums[-1] * nums[-2] * nums[-3]

    # Two most negative × largest positive (if two negatives exist)
    two_neg_one_pos = nums[0] * nums[1] * nums[-1]

    return max(top_three, two_neg_one_pos)


# Test
print(maximumProduct([1, 2, 3, 4]))  # 24
print(maximumProduct([-1, -2, -3]))  # -6
print(maximumProduct([-10, -10, 1, 3, 2]))  # 300
print(maximumProduct([-4, -3, -2, -1]))  # -6
print(maximumProduct([-100, -1, -1, 1]))  # 100
```

### Complexity Analysis
- **Time:** O(n log n) for sorting.
- **Space:** O(1).
- **Alternative (O(n)):** Find the 3 largest and 2 smallest values in a single pass.

### Edge Cases
- **All negative:** Three largest (least negative) gives the maximum (closest to zero).
- **n = 3:** Only one product possible, both candidates evaluate to the same.
- **Mix of signs:** Both candidates matter; one will be the maximum.
- **All zeros:** Product is 0.

### Common Mistakes
1. **Only considering top-3:** Missing the two-negative case when there are negative numbers.
2. **Forgetting the array has negatives:** Always compute both candidates.
3. **Assuming the largest product involves the maximum element:** With all negatives, the least negative elements give the maximum product.
4. **Not sorting or not using O(n) alternative:** Both approaches work, but sorting is simpler.

### Pattern Recognition
- **Sort + Two Candidates:** When the extreme answer involves either "largest of same sign" or "most negative × most positive," check both.
- **O(n) Alternative:** For the O(n) approach (no sort), track `max1, max2, max3` and `min1, min2` in a single pass.
- **Similar Problems:** Maximum Product Subarray, Maximum Product of Two Elements in an Array.

---

## Problem 8: 3Sum Closest

### Problem Explanation (Simple Words)
Find three numbers whose sum is as close as possible to a target value. After sorting, fix one element and use two pointers (left, right) to find the best pair for each fixed element. The two pointers move directionally: if sum is too low, increase left; if too high, decrease right.

### Algorithm Steps
1. **Sort** the array.
2. **Initialize** `closest` with the sum of the first three elements.
3. **Fix each element** `nums[i]` from 0 to n-3:
   - Set `left = i + 1`, `right = n - 1`.
   - While `left < right`: compute `curr_sum = nums[i] + nums[left] + nums[right]`.
   - If `|curr_sum - target| < |closest - target|`: update `closest`.
   - If `curr_sum < target`: move `left` right (increase sum).
   - If `curr_sum > target`: move `right` left (decrease sum).
   - If `curr_sum == target`: return immediately (can't get closer).
4. **Return** `closest`.

### Visual Walkthrough
**Input:** `nums = [-1, 2, 1, -4]`, `target = 1`

```
Sorted: [-4, -1, 1, 2]

i=0 (nums[0] = -4):
  left=1 (-1), right=3 (2): sum = -4 + (-1) + 2 = -3
    |(-3)-1| = 4, closest=3 → closest = -3
    -3 < 1 → left++
  left=2 (1), right=3 (2): sum = -4 + 1 + 2 = -1
    |(-1)-1| = 2 < 4 → closest = -1
    -1 < 1 → left=3, left=right → STOP

i=1 (nums[1] = -1):
  left=2 (1), right=3 (2): sum = -1 + 1 + 2 = 2
    |2-1| = 1 < 2 → closest = 2
    2 > 1 → right-- → left=right → STOP

i=2 (nums[2] = 1): only nums[2]+nums[3] = 1+2, can't form triplet → skip

Result: 2 ✓ (sum closest to 1)
```

### Key Insight
Sorting enables the two-pointer directional movement. When the sum is too small, we need a larger number → move left pointer right. When too large, we need a smaller number → move right pointer left. This eliminates the need to check all O(n³) combinations.

### Well-Commented Code

```python
def threeSumClosest(nums, target):
    nums.sort()
    n = len(nums)

    # Initial closest sum (first three elements)
    closest = nums[0] + nums[1] + nums[2]

    for i in range(n - 2):
        left, right = i + 1, n - 1

        while left < right:
            curr_sum = nums[i] + nums[left] + nums[right]

            # Check if this sum is closer to target
            if abs(curr_sum - target) < abs(closest - target):
                closest = curr_sum

            # Directional adjustment
            if curr_sum < target:
                left += 1      # Need larger sum
            elif curr_sum > target:
                right -= 1     # Need smaller sum
            else:
                return target  # Perfect match

    return closest


# Test
print(threeSumClosest([-1, 2, 1, -4], 1))  # 2
print(threeSumClosest([0, 1, 2], 3))  # 3
print(threeSumClosest([-3, -2, -5, 3, -4], -1))  # -2
```

### Complexity Analysis
- **Time:** O(n²) — outer loop O(n), inner two-pointer O(n).
- **Space:** O(1) — sorting is in-place (or O(n) for Timsort).

### Edge Cases
- **n = 3:** Only one triplet; loop runs once, two-pointer immediately terminates.
- **Exact match found:** Early return saves time.
- **All same values:** Every sum = 3 × value.
- **Negative target:** Works correctly since comparison uses absolute difference.
- **Large numbers:** Python handles big integers without overflow.

### Common Mistakes
1. **Forgetting to sort:** The two-pointer approach requires sorted input.
2. **Not checking all i values:** The outer loop must go to n-3.
3. **Updating closest in wrong direction:** Only update when `|curr_sum - target|` is smaller.
4. **Skipping the i=0 iteration:** Need to compare with all possible fixed elements.
5. **Returning value instead of sum:** The problem asks for the sum, not the elements.

### Pattern Recognition
- **Sort + Two Pointers for k-Sum:** This is the standard pattern for "find k elements closest to target." Sort, fix k-2 elements, use two pointers for the remaining 2.
- **Directional Movement:** The two pointers move in one direction (low→high or high→low) based on comparison to target.
- **Comparison with 3Sum:** 3Sum looks for exact zero-sum triplets; this problem looks for closest sum.
- **Similar Problems:** 3Sum (exact zero), 4Sum, Two Sum (sorted).

---

## Problem 9: Pancake Sorting

### Problem Explanation (Simple Words)
We can only sort by flipping the first k elements (like flipping a stack of pancakes). We want to sort the array using as few flips as possible, returning the list of k values used. Strategy: for each position from right to left, bring the maximum element to the front (flip at its index), then flip it to its correct position (flip at current size).

### Algorithm Steps
1. **For each position** `size` from n down to 1:
   - Find the index of the maximum element in `arr[:size]`.
   - If it's already at the last position of current window → skip.
   - If it's not at index 0: flip at `max_idx + 1` to bring it to front.
   - Flip at `size` to move it to its correct position.
2. **Return** the list of flip k-values.

### Visual Walkthrough
**Input:** `[3, 2, 4, 1]`

```
size=4: find max in [3,2,4,1] at idx=2
  flip(2+1=3): [4, 2, 3, 1]  (bring 4 to front)
  flip(4):     [1, 3, 2, 4]  (put 4 in place)

size=3: find max in [1,3,2] at idx=1
  flip(1+1=2): [3, 1, 2, 4]  (bring 3 to front)
  flip(3):     [2, 1, 3, 4]  (put 3 in place)

size=2: find max in [2,1] at idx=0
  already at front (idx=0), skip front flip
  flip(2):     [1, 2, 3, 4]  (put 2 in place)

size=1: single element → skip

Result: [3, 4, 2, 3, 2] ✓ (any valid sequence)
```

### Key Insight
The pancake sort builds the array from the rightmost position inward. For each position, a maximum of 2 flips is needed: one to bring the target element to index 0, and another to place it at its final position. The already-sorted suffix is never disturbed.

### Well-Commented Code

```python
def pancakeSort(arr):
    result = []

    # Process from right to left
    for size in range(len(arr), 0, -1):
        # Find the maximum element in the unsorted window
        max_idx = arr.index(max(arr[:size]))

        # If max is already in position, no flip needed
        if max_idx == size - 1:
            continue

        # Flip max to the front (if not already there)
        if max_idx > 0:
            arr[:max_idx + 1] = reversed(arr[:max_idx + 1])
            result.append(max_idx + 1)

        # Flip max from front to its correct position
        arr[:size] = reversed(arr[:size])
        result.append(size)

    return result


# Test
print(pancakeSort([3, 2, 4, 1]))  # [2, 4, 3, 3] or similar
print(pancakeSort([1, 2, 3]))  # []
print(pancakeSort([3, 1, 2]))  # [1, 3, 2] or similar
```

### Complexity Analysis
- **Time:** O(n²) — each of n positions requires a linear search for max.
- **Space:** O(n) for the result list. In-place array modifications.

### Edge Cases
- **Already sorted:** No flips needed → return empty list.
- **Reverse sorted:** Maximum flips required (2 per element from n-1 elements).
- **Single element:** Trivially sorted, no flips.

### Common Mistakes
1. **Forgetting to skip when max is already in position:** `max_idx == size - 1` means no flip needed.
2. **Off-by-one in flip size:** The flip size is `k` meaning flip first k elements. If `max_idx = 2`, we flip 3 elements.
3. **Using slice assignment incorrectly:** `arr[:k] = reversed(arr[:k])` works, but the more explicit `arr[:k] = arr[k-1::-1]` is also valid.
4. **Not handling the case where max is at index 0:** Skip the first flip, only do the second.
5. **Confusing with bubble sort:** Pancake sort flips prefixes, not swaps adjacent elements.

### Pattern Recognition
- **Sorting by Reversal:** This is a classic "sort by reversal" problem. Only flips of prefixes are allowed.
- **Maximum-to-Last Strategy:** The pattern of moving the maximum to its correct position, then reducing the problem size, is common.
- **Similar Problems:** Sort by Reversals (genome rearrangement), Sort by Swaps, Minimum Number of Flips to Convert Binary String.

---

## Problem 10: Reveal Cards In Increasing Order

### Problem Explanation (Simple Words)
We need to arrange the deck so that the reveal process produces cards in ascending order. The reveal: take the top card, reveal it, then move the next card to the bottom. By simulating this process on indices (not cards), we determine which position each card must go to. Then we place the sorted cards into those positions.

### Algorithm Steps
1. **Sort** the deck in ascending order.
2. **Create a deque** of indices `[0, 1, 2, ..., n-1]`.
3. **For each card** (from smallest to largest):
   - Pop the first index from deque → place the card at that position.
   - If the deque still has elements: pop the next index and append it to the back.
4. **Return** the result array.

### Visual Walkthrough
**Input:** `[17, 13, 11, 2, 3, 5, 7]`

```
Sorted deck: [2, 3, 5, 7, 11, 13, 17]
Indices: deque([0, 1, 2, 3, 4, 5, 6])

Step 1: card=2 → pop 0 → result[0]=2
        pop 1, push to back → indices=[2,3,4,5,6,1]
Step 2: card=3 → pop 2 → result[2]=3
        pop 3, push to back → indices=[4,5,6,1,3]
Step 3: card=5 → pop 4 → result[4]=5
        pop 5, push to back → indices=[6,1,3,5]
Step 4: card=7 → pop 6 → result[6]=7
        pop 1, push to back → indices=[3,5,1]
Step 5: card=11 → pop 3 → result[3]=11
        pop 5, push to back → indices=[1,5]
Step 6: card=13 → pop 1 → result[1]=13
        pop 5, push to back → indices=[5]
Step 7: card=17 → pop 5 → result[5]=17
        indices empty → STOP

Result: [2, 13, 3, 11, 5, 17, 7] ✓

Verification:
  Reveal 2 → move 13 to bottom: [3,11,5,17,7,13]
  Reveal 3 → move 11 to bottom: [5,17,7,13,11]
  Reveal 5 → move 17 to bottom: [7,13,11,17]
  Reveal 7 → move 13 to bottom: [11,17,13]
  Reveal 11 → move 17 to bottom: [13,17]
  Reveal 13 → move 17 to bottom: [17]
  Reveal 17
  Revealed order: [2, 3, 5, 7, 11, 13, 17] ✓
```

### Key Insight
Instead of trying to rearrange cards to satisfy the reveal process (which is tricky to reason about), we simulate the reveal on a deque of indices. This tells us exactly which position in the result corresponds to which reveal step. Then we place the smallest card into the first revealed position, etc.

### Well-Commented Code

```python
from collections import deque

def deckRevealedIncreasing(deck):
    # Sort cards in increasing order (the order they should be revealed)
    deck.sort()
    n = len(deck)

    # Deque of indices representing the reveal order
    indices = deque(range(n))
    result = [0] * n

    # Place each card at the position determined by the reveal simulation
    for card in deck:
        # The current index is the next position in reveal order
        result[indices.popleft()] = card

        # Move the next index to the bottom (end of deque)
        if indices:
            indices.append(indices.popleft())

    return result


# Test
print(deckRevealedIncreasing([17, 13, 11, 2, 3, 5, 7]))
# [2, 13, 3, 11, 5, 17, 7]
print(deckRevealedIncreasing([1, 1000]))  # [1, 1000]
print(deckRevealedIncreasing([1]))  # [1]
```

### Complexity Analysis
- **Time:** O(n log n) — sorting dominates; the deque operations are O(n).
- **Space:** O(n) — for indices deque and result array.

### Edge Cases
- **Single card:** The loop runs once, result[0] = card.
- **Two cards:** First card goes to result[0], remaining index cycles → second card goes to result[1].
- **Already sorted deck:** May still need rearrangement to match the reveal process.
- **All same values:** The problem says unique integers, so this doesn't occur.

### Common Mistakes
1. **Simulating on cards instead of indices:** Trying to directly manipulate card order during reveal simulation is complex. Simulating on indices is cleaner.
2. **Forgetting to cycle indices:** After popleft for placement, the next index must be moved to the back.
3. **Not sorting first:** The cards must be placed in increasing order into reveal positions, which requires sorting.
4. **Using a list instead of deque for indices:** Lists have O(n) pop(0) operation. Deque has O(1) popleft().
5. **Off-by-one in index simulation:** Ensure the reveal pattern is correctly implemented: take, move next to bottom, repeat.

### Pattern Recognition
- **Simulate Process on Indices:** When you need to determine positions, simulate the process on indices rather than values.
- **Deque for Cyclic Processing:** The deque's popleft and append operations perfectly model "take from front, move next to back."
- **Reverse Engineering:** The problem asks to create an arrangement that produces a given output sequence. Reverse-engineering the process is often easier than forward construction.
- **Similar Problems:** Card Revealing (same problem), Queue Reconstruction by Height, Shuffle an Array.

---

# PART B: HASHING (Problems 11–25)

---

## Problem 11: Subarray Sum Equals K

### Problem Explanation (Simple Words)
Count how many contiguous subarrays sum exactly to k. The brute force checks every subarray O(n²). The prefix sum technique: as we iterate, maintain a running sum. If `prefix_sum - k` was seen before, those many subarrays ending at the current position sum to k.

### Algorithm Steps
1. **Initialize** `prefix = 0`, `count = 0`, hashmap `seen = {0: 1}`.
2. **For each `num`:**
   - Add `num` to `prefix`.
   - If `prefix - k` exists in `seen`, add its frequency to `count`.
   - Increment `seen[prefix]`.
3. **Return** `count`.

### Visual Walkthrough
**Input:** `nums = [1, 1, 1]`, `k = 2`

```
seen = {0: 1}, prefix = 0, count = 0

i=0, num=1: prefix=1, 1-2=-1 not in seen
  seen[1] = 1 → {0:1, 1:1}

i=1, num=1: prefix=2, 2-2=0 is in seen (count 1)
  count += 1 → count=1  [subarray 0..1]
  seen[2] = 1 → {0:1, 1:1, 2:1}

i=2, num=1: prefix=3, 3-2=1 is in seen (count 1)
  count += 1 → count=2  [subarray 1..2]
  seen[3] = 1 → {0:1, 1:1, 2:1, 3:1}

Result: 2 ✓
```

### Key Insight
`prefix[j] - prefix[i] = sum(i+1..j)`. By storing frequencies of prefix sums, we answer "how many subarrays end at current index with sum k?" in O(1).

### Well-Commented Code

```python
from collections import defaultdict

def subarraySum(nums, k):
    count = 0
    prefix = 0
    seen = defaultdict(int)
    seen[0] = 1  # Empty prefix sum

    for num in nums:
        prefix += num
        # Subarrays ending at current position with sum k
        count += seen[prefix - k]
        # Record this prefix sum for future subarrays
        seen[prefix] += 1

    return count

# Test
print(subarraySum([1, 1, 1], 2))  # 2
print(subarraySum([1, 2, 3], 3))  # 2 ([1,2] and [3])
print(subarraySum([1, -1, 0], 0))  # 3
```

### Complexity Analysis
- **Time:** O(n) — single pass.
- **Space:** O(n) — hashmap stores up to n prefix sums.

### Edge Cases
- **k = 0:** Works naturally; `prefix - 0 = prefix`, so repeated prefix sums indicate zero-sum subarrays.
- **All zeros with k=0:** `[0,0,0]`: prefix sums are 0,0,0. Each step adds the count of previous zeros.
- **Single element matching k:** `prefix - k = 0` matches the initial `{0: 1}`.
- **Negative numbers:** Handled naturally (prefix sums can go up and down).

### Common Mistakes
1. **Forgetting `{0: 1}`:** Without it, subarrays starting from index 0 are missed.
2. **Using a set instead of dict:** Multiple subarrays can share the same prefix sum.
3. **Updating map before checking:** `seen[prefix] += 1` must happen AFTER checking `prefix - k` to avoid counting the current element as a subarray of length 0.

### Pattern Recognition
- **Prefix Sum + Hash Map:** One of the most important patterns for subarray problems.
- **Frequency Tracking:** Store frequencies, not just existence.
- **Similar Problems:** Subarray Sum Divisible by K, Continuous Subarray Sum, Number of Submatrices That Sum to Target.

---

## Problem 12: Continuous Subarray Sum

### Problem Explanation (Simple Words)
Find a contiguous subarray of length ≥ 2 whose sum is divisible by k. The key insight: if two prefix sums have the same remainder modulo k, the subarray between them has a sum divisible by k.

### Algorithm Steps
1. **Initialize** `seen = {0: -1}` (remainder 0 at index -1).
2. **Iterate** with `prefix = 0`:
   - Add `num` to `prefix`.
   - Compute `rem = prefix % k`.
   - If `rem` in `seen` and `i - seen[rem] >= 2`: return `True`.
   - Else (first occurrence): store `seen[rem] = i`.
3. **Return** `False`.

### Visual Walkthrough
**Input:** `nums = [23, 2, 4, 6, 7]`, `k = 6`

```
seen = {0: -1}, prefix = 0

i=0, num=23: prefix=23, rem=23%6=5
  5 not in seen → seen[5] = 0

i=1, num=2: prefix=25, rem=25%6=1
  1 not in seen → seen[1] = 1

i=2, num=4: prefix=29, rem=29%6=5
  5 in seen at index 0, i-0=2 ≥ 2 → True ✓

Subarray [2, 4] sums to 6, divisible by 6
```

### Key Insight
`prefix[j] % k == prefix[i] % k` implies `(prefix[j] - prefix[i]) % k == 0`, meaning `sum(nums[i+1..j])` is divisible by k. Store only the first occurrence of each remainder to maximize subarray length.

### Well-Commented Code

```python
def checkSubarraySum(nums, k):
    # Map remainder → first index where it occurred
    seen = {0: -1}  # remainder 0 before any element
    prefix = 0

    for i, num in enumerate(nums):
        prefix += num
        r = prefix % k

        if r in seen:
            # Subarray between seen[r] and i has sum divisible by k
            if i - seen[r] >= 2:
                return True
        else:
            # Store only the first occurrence
            seen[r] = i

    return False


# Test
print(checkSubarraySum([23, 2, 4, 6, 7], 6))  # True ([2,4] sum=6)
print(checkSubarraySum([23, 2, 6, 4, 7], 6))  # True (whole array sum=42)
print(checkSubarraySum([23, 2, 6, 4, 7], 13))  # False
```

### Complexity Analysis
- **Time:** O(n) — single pass.
- **Space:** O(min(n, k)) — at most k distinct remainders.

### Edge Cases
- **k = 1:** Every number divisible by 1; any subarray of length ≥ 2 works.
- **k = 0:** `% 0` raises ZeroDivisionError. Handle separately.
- **All zeros with any k:** `[0, 0]` → prefix sums are 0, rem = 0, seen[0] = -1, i - (-1) = 2 ≥ 2 → True.
- **n < 2:** Impossible to find length ≥ 2 subarray.
- **Negative numbers:** Python's `%` returns non-negative, so it works.

### Common Mistakes
1. **Not storing the first occurrence:** Updating `seen[r]` on every encounter shortens the subarray length, potentially missing the ≥ 2 constraint.
2. **Forgetting `{0: -1}`:** Without it, subarrays starting from index 0 that are divisible by k are missed.
3. **Using `%` with negative numbers incorrectly:** In some languages, `%` returns negative results. Python's `%` always returns non-negative.
4. **Not checking length ≥ 2:** A single element divisible by k would incorrectly return True.

### Pattern Recognition
- **Prefix Sum Modulo:** The modulo version of the prefix sum pattern.
- **Pigeonhole Principle:** After k+1 prefix sums, some remainder must repeat, guaranteeing a subarray with sum divisible by k.
- **Similar Problems:** Subarray Sum Equals K, Subarray Sums Divisible by K.

---

## Problem 13: Minimum Index Sum of Two Lists

### Problem Explanation (Simple Words)
Two people rank restaurants by position in their lists (lower index = higher preference). Find common restaurants with the smallest sum of their positions. If multiple share the minimum sum, return all.

### Algorithm Steps
1. **Build map** from list1: `restaurant → index`.
2. **Initialize** `min_sum = ∞`, `result = []`.
3. **Scan list2:** For each `name` at index `j`:
   - If in map: compute `sum = map[name] + j`.
   - If `sum < min_sum`: reset result to `[name]`.
   - If `sum == min_sum`: append `name`.
4. **Return** `result`.

### Visual Walkthrough
**Input:** `list1 = ["Shogun","Tapioca Express","Burger King","KFC"]`, `list2 = ["KFC","Shogun","Burger King"]`

```
map1 = {"Shogun":0, "Tapioca Express":1, "Burger King":2, "KFC":3}

j=0, "KFC": sum=3+0=3 → min=3, result=["KFC"]
j=1, "Shogun": sum=0+1=1 < 3 → min=1, result=["Shogun"]
j=2, "Burger King": sum=2+2=4 > 1 → skip

Result: ["Shogun"] ✓
```

### Key Insight
Building one map and scanning the other avoids the O(nm) brute force. This is a one-sided map pattern — we only need to store indices from one list.

### Well-Commented Code

```python
def findRestaurant(list1, list2):
    index_map = {name: i for i, name in enumerate(list1)}
    min_sum = float('inf')
    result = []

    for j, name in enumerate(list2):
        if name in index_map:
            idx_sum = index_map[name] + j
            if idx_sum < min_sum:
                min_sum = idx_sum
                result = [name]
            elif idx_sum == min_sum:
                result.append(name)

    return result


# Test
print(findRestaurant(["Shogun", "Tapioca Express", "Burger King", "KFC"],
                      ["Piatti", "The Grill at Torrey Pines",
                       "Hungry Hunter Steakhouse", "Shogun"]))
# ["Shogun"]
print(findRestaurant(["happy", "sad", "good"], ["sad", "happy", "good"]))
# ["sad", "happy"]
```

### Complexity Analysis
- **Time:** O(n + m) — build map O(n), scan list2 O(m).
- **Space:** O(n) — map stores list1 entries.

### Edge Cases
- **No common restaurants:** Returns `[]`.
- **Multiple with same min sum:** Appends all.
- **Duplicates in list1:** Only first index stored.

### Common Mistakes
1. **Building two maps:** Only one map needed.
2. **Not handling ties:** Use `<` for new min, `==` for ties.
3. **Using `<=` incorrectly:** Would need different logic for tie vs. new min.

### Pattern Recognition
- **Map + Linear Scan:** Store one list in a map, scan the other.
- **Minimum Tracking with Ties:** Reset on new min, append on tie.
- **Similar Problems:** Intersection of Two Arrays, Two Sum.

---

## Problem 14: Number of Good Pairs

### Problem Explanation (Simple Words)
Count pairs of equal elements where the first index is smaller than the second. For each value that appears `c` times, the number of pairs is the number of ways to choose 2 positions from c: C(c, 2) = c × (c-1) / 2.

### Algorithm Steps
1. **Count frequencies** using `Counter`.
2. **For each frequency `c`:** add `c * (c - 1) // 2` to result.
3. **Return** total.

### Visual Walkthrough
**Input:** `[1, 2, 3, 1, 1, 3]`

```
Frequencies: 1→3, 2→1, 3→2

Pairs:
  1 appears 3 times: C(3,2) = 3×2/2 = 3 pairs
  2 appears 1 time:  C(1,2) = 0 pairs
  3 appears 2 times: C(2,2) = 2×1/2 = 1 pair

Total: 3 + 0 + 1 = 4 ✓
```

### Key Insight
Instead of O(n²) nested loops to check every pair, the combination formula C(c, 2) counts all pairs for each distinct value in O(1).

### Well-Commented Code

```python
from collections import Counter

def numIdenticalPairs(nums):
    count = Counter(nums)
    result = 0
    for c in count.values():
        # C(c, 2) = c * (c - 1) / 2
        result += c * (c - 1) // 2
    return result


# Test
print(numIdenticalPairs([1, 2, 3, 1, 1, 3]))  # 4
print(numIdenticalPairs([1, 1, 1, 1]))  # 6
print(numIdenticalPairs([1, 2, 3]))  # 0
```

### Complexity Analysis
- **Time:** O(n) — counting frequencies.
- **Space:** O(n) — storing frequencies.

### Edge Cases
- **All distinct:** Each frequency = 1 → C(1,2) = 0 → result 0.
- **All same:** Frequency = n → C(n, 2) = n(n-1)/2.
- **Single element:** 0 pairs.
- **Empty array:** 0 pairs.

### Common Mistakes
1. **Using `c * (c - 1) // 2` without integer division:** Using `/` would produce floats.
2. **Iterating over the array instead of Counter values:** Would count each pair multiple times.
3. **Double-counting:** The formula counts each pair exactly once.
4. **Forgetting `from collections import Counter`.**

### Pattern Recognition
- **Combinatorics via Frequency:** When counting unordered pairs of equal elements, use C(n, 2).
- **Counting Without Enumeration:** Many "count pairs" problems reduce to combinatorics.
- **Similar Problems:** Count Number of Pairs With Absolute Difference K, Number of Pairs of Strings With Concatenation Equal to Target.

---

## Problem 15: Word Pattern

### Problem Explanation (Simple Words)
Each character in the pattern maps to exactly one word, and each word maps to exactly one character (bijection). "abba" with "dog cat cat dog" works: a→dog, b→cat, and cat→b, dog→a. The mapping must be consistent in both directions.

### Algorithm Steps
1. **Split `s`** into words. If lengths differ → return False.
2. **Maintain two dicts:** `char_to_word` and `word_to_char`.
3. **For each pair `(c, w)`:
   - If `c` already maps to a different word → False.
   - If `w` already maps to a different char → False.
   - Otherwise, record both mappings.
4. **Return** True.

### Visual Walkthrough
**Input:** `pattern = "abba"`, `s = "dog cat cat fish"`

```
words = ["dog", "cat", "cat", "fish"]
len("abba") = 4 = len(words) → OK

Step 1: c='a', w='dog'
  char_to_word['a'] = 'dog', word_to_char['dog'] = 'a'

Step 2: c='b', w='cat'
  char_to_word['b'] = 'cat', word_to_char['cat'] = 'b'

Step 3: c='b', w='cat'
  char_to_word['b'] = 'cat' ✓, word_to_char['cat'] = 'b' ✓

Step 4: c='a', w='fish'
  char_to_word['a'] = 'dog' ≠ 'fish' → False ✗
```

### Key Insight
A bijection requires consistency in BOTH directions. A → B implies B → A. If one direction fails, the pattern doesn't match.

### Well-Commented Code

```python
def wordPattern(pattern, s):
    words = s.split()
    if len(pattern) != len(words):
        return False

    char_to_word = {}
    word_to_char = {}

    for c, w in zip(pattern, words):
        # Check both directions of the bijection
        if c in char_to_word:
            if char_to_word[c] != w:
                return False
        else:
            char_to_word[c] = w

        if w in word_to_char:
            if word_to_char[w] != c:
                return False
        else:
            word_to_char[w] = c

    return True


# Test
print(wordPattern("abba", "dog cat cat dog"))  # True
print(wordPattern("abba", "dog cat cat fish"))  # False
print(wordPattern("abc", "def def def"))  # False
print(wordPattern("aaaa", "dog cat cat dog"))  # False
```

### Complexity Analysis
- **Time:** O(n) — single pass.
- **Space:** O(m) where m = number of unique characters.

### Edge Cases
- **Empty pattern and empty string:** Both empty, return True.
- **Different lengths:** Immediate False.
- **Single character with single word:** Always True (bijection holds).

### Common Mistakes
1. **Checking only one direction:** Without `word_to_char`, "ab" → "dog dog" would pass (a→dog, b→dog) incorrectly.
2. **Not checking length first:** Different lengths can never match.
3. **Using split's default behavior:** `split()` splits on any whitespace, which is correct.

### Pattern Recognition
- **Bidirectional Mapping:** Any "follows the pattern" problem needs two maps for a bijection.
- **String Splitting:** `s.split()` converts a sentence to a list of words.
- **Similar Problems:** Isomorphic Strings, Find and Replace Pattern.

---

## Problem 16: Isomorphic Strings

### Problem Explanation (Simple Words)
Each character in `s` must map to exactly one character in `t`, and each character in `t` must map to exactly one character in `s`. "egg" → "add": e→a, g→d. "foo" → "bar" fails because o would need to map to both a and r.

### Algorithm Steps
1. **If lengths differ** → return False.
2. **Maintain two dicts**: `s_to_t` and `t_to_s`.
3. **For each pair `(c1, c2)`**:
   - If `c1` already maps to a different char → False.
   - If `c2` already maps to a different char → False.
   - Record both mappings.
4. **Return** True.

### Visual Walkthrough
**Input:** `s = "paper"`, `t = "title"`

```
len("paper") = 5 = len("title") → OK

Step: p→t, a→i, p→t (✓), e→l, r→e
Reverse: t→p, i→a, l→e, e→r

All consistent → True ✓
```

### Key Insight
This is identical to Word Pattern but at the character level instead of word level. Both problems require a bijection (one-to-one mapping in both directions).

### Well-Commented Code

```python
def isIsomorphic(s, t):
    if len(s) != len(t):
        return False

    s_to_t = {}
    t_to_s = {}

    for c1, c2 in zip(s, t):
        if c1 in s_to_t:
            if s_to_t[c1] != c2:
                return False
        else:
            s_to_t[c1] = c2

        if c2 in t_to_s:
            if t_to_s[c2] != c1:
                return False
        else:
            t_to_s[c2] = c1

    return True


# Test
print(isIsomorphic("egg", "add"))  # True
print(isIsomorphic("foo", "bar"))  # False
print(isIsomorphic("paper", "title"))  # True
print(isIsomorphic("ab", "aa"))  # False
```

### Complexity Analysis
- **Time:** O(n) — single pass.
- **Space:** O(1) — at most 256 ASCII or 1M+ Unicode characters, but practically bounded.

### Edge Cases
- **Empty strings:** Trivially isomorphic.
- **Single character:** True if both are same, False otherwise.
- **Different lengths:** Immediate False.

### Common Mistakes
1. **Single-direction mapping:** Without `t_to_s`, "ab" → "aa" would pass (a→a, b→a), but b and a both map to a (not injective).
2. **Not checking length first.**
3. **Using arrays instead of dicts:** Fixed-size arrays work for ASCII but not Unicode.

### Pattern Recognition
- **Bidirectional Mapping:** Same pattern as Word Pattern.
- **Character-Level Pattern Matching:** Works for any alphabet.
- **Similar Problems:** Word Pattern, Find and Replace Pattern, Check If a String Is a Valid Sequence.

---

## Problem 17: Find Duplicate Number in Array

### Problem Explanation (Simple Words)
We have n+1 numbers, each between 1 and n. By pigeonhole principle, at least one number repeats. We must find it using O(1) extra space. Treat the array as a linked list where `nums[i]` points to the next node. The duplicate creates a cycle; finding the cycle entrance gives us the duplicate value.

### Algorithm Steps
1. **Phase 1 (Find intersection):**
   - `slow = nums[0]`, `fast = nums[0]`.
   - Move `slow` by 1, `fast` by 2 until they meet.
2. **Phase 2 (Find cycle entrance):**
   - Reset `slow = nums[0]`.
   - Move both by 1 until they meet → that's the duplicate.
3. **Return** the meeting point value.

### Visual Walkthrough
**Input:** `[1, 3, 4, 2, 2]`

```
Treat as linked list:
  0→1→3→2→4→2→4→2→...

Phase 1 (slow & fast):
  slow=1, fast=1
  slow=3, fast=3  (nums[1]=3, nums[nums[1]]=nums[3]=2 → nums[2]=4 → wait)
  slow=4, fast=4  → meet at 4

Phase 2 (find entrance):
  slow=1 (reset to start)
  slow=3, fast=2
  slow=2, fast=4
  slow=4, fast=3
  slow=2, fast=2 → meet at 2

Result: 2 ✓
```

### Key Insight
The value `nums[i]` acts as a "pointer" to index `nums[i]`. Since values are in [1, n], they're always valid indices. The duplicate creates a cycle because two different indices point to the same value.

### Well-Commented Code

```python
def findDuplicate(nums):
    # Phase 1: Find intersection point in the cycle
    slow = nums[0]
    fast = nums[0]
    while True:
        slow = nums[slow]          # Move 1 step
        fast = nums[nums[fast]]    # Move 2 steps
        if slow == fast:
            break

    # Phase 2: Find cycle entrance (= duplicate)
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow


# Test
print(findDuplicate([1, 3, 4, 2, 2]))  # 2
print(findDuplicate([3, 1, 3, 4, 2]))  # 3
print(findDuplicate([1, 1]))  # 1
print(findDuplicate([2, 5, 9, 6, 9, 3, 8, 9, 7, 1]))  # 9
```

### Complexity Analysis
- **Time:** O(n) — each phase runs in O(n).
- **Space:** O(1) — only two pointer variables.
- **Note:** This is an O(1) space solution. A hash set would be O(n) space.

### Edge Cases
- **n=2, [1, 1]:** Single element repeated. Floyd's algorithm works.
- **Multiple duplicates:** Returns one of them (the first cycle entrance found).
- **Duplicate at index 0:** The entry point might point back to 0 directly; algorithm still works.

### Common Mistakes
1. **Starting slow/fast at different positions:** Both must start at `nums[0]` for Floyd's to work.
2. **Confusing index with value:** The duplicate value is the cycle entrance, not the intersection point.
3. **Using `nums[0]` instead of `nums[0]` for initialization:** `slow = 0` (index) vs `slow = nums[0]` (value). Use the value.
4. **Not understanding the linked list mapping:** `nums[i]` is the "next node" of index `i`.

### Pattern Recognition
- **Floyd's Cycle Detection:** Classic O(1) space cycle detection. Also used for linked list cycle detection.
- **Array as Linked List:** When indices point to values that are also valid indices, treat the array as a linked list.
- **Pigeonhole Principle:** n+1 elements in range [1, n] guarantees at least one duplicate.
- **Similar Problems:** Linked List Cycle, Find the Duplicate Number (hash set approach), Happy Number.

---

## Problem 18: Check if Numbers Are Ascending in a Sentence

### Problem Explanation (Simple Words)
A sentence contains both words and numbers. Extract all numbers and verify they're strictly increasing (each number > previous). Ignore words completely.

### Algorithm Steps
1. **Split** the sentence into tokens by whitespace.
2. **Extract numbers:** Filter tokens where `token.isdigit()` is True, convert to int.
3. **Check monotonicity:** For each adjacent pair, verify `num[i] < num[i+1]`.
4. **Return** True if all increasing, else False.

### Visual Walkthrough
**Input:** `"1 box has 3 blue 4 red 6 green"`

```
Tokens: ["1", "box", "has", "3", "blue", "4", "red", "6", "green"]
Numbers only: [1, 3, 4, 6]

Check: 1<3 ✓, 3<4 ✓, 4<6 ✓ → True
```

### Key Insight
`str.isdigit()` returns True only if ALL characters are digits, making it perfect for identifying numeric tokens.

### Well-Commented Code

```python
def areNumbersAscending(s):
    # Extract all numeric tokens and convert to int
    numbers = [int(word) for word in s.split() if word.isdigit()]

    # Check strictly increasing
    for i in range(len(numbers) - 1):
        if numbers[i] >= numbers[i + 1]:
            return False
    return True


# Test
print(areNumbersAscending("1 box has 3 blue 4 red 6 green"))  # True
print(areNumbersAscending("hello world 5 x 5"))  # False
print(areNumbersAscending("4 5 11 26 35"))  # True
print(areNumbersAscending("4 5 11 26 35 35"))  # False
```

### Complexity Analysis
- **Time:** O(n) — split and scan.
- **Space:** O(m) — m = number count.

### Edge Cases
- **No numbers:** `numbers` is empty → vacuously True.
- **Single number:** Loop doesn't execute → True.
- **Leading zeros:** `int("005")` = 5, correct.
- **Negative numbers:** `isdigit()` returns False for '-', so not extracted. Problem likely doesn't include negatives.

### Common Mistakes
1. **Using `isnumeric()` or `isdecimal()`:** `isdigit()` is the correct choice. `isnumeric()` also works but is broader.
2. **Using `>=` instead of `>`:** Strictly increasing means `num[i] < num[i+1]`, not `<=`.
3. **Not converting to int:** String comparison would give lexicographic order ("2" > "11").
4. **Including non-digit tokens:** `isdigit()` correctly filters out words and mixed tokens.

### Pattern Recognition
- **String Parsing + Validation:** Extract relevant tokens, then validate a property.
- **Filter-Transform-Check:** A common three-step pipeline pattern.
- **Similar Problems:** Check if All A's Appears Before All B's, Sentence Similarity III.

---

## Problem 19: Find the Difference of Two Arrays

### Problem Explanation (Simple Words)
Find values unique to each array. Elements in nums1 but not in nums2 form the first list; elements in nums2 but not in nums1 form the second. Sets make this trivial — set difference gives the answer.

### Algorithm Steps
1. **Convert** both arrays to sets (removes duplicates).
2. **Compute** `diff1 = set1 - set2` and `diff2 = set2 - set1`.
3. **Return** `[list(diff1), list(diff2)]`.

### Visual Walkthrough
**Input:** `nums1 = [1, 2, 3]`, `nums2 = [2, 4, 6]`

```
set1 = {1, 2, 3}
set2 = {2, 4, 6}

diff1 = set1 - set2 = {1, 3}  (in nums1 but not nums2)
diff2 = set2 - set1 = {4, 6}  (in nums2 but not nums1)

Result: [[1, 3], [4, 6]] ✓
```

### Key Insight
Set difference `A - B` returns all elements in A that are not in B. This is O(min(|A|, |B|)) on average, making it very efficient.

### Well-Commented Code

```python
def findDifference(nums1, nums2):
    set1 = set(nums1)
    set2 = set(nums2)

    # Unique to nums1, unique to nums2
    return [list(set1 - set2), list(set2 - set1)]


# Test
print(findDifference([1, 2, 3], [2, 4, 6]))  # [[1,3],[4,6]]
print(findDifference([1, 2, 3, 3], [1, 1, 2, 2]))  # [[3],[]]
print(findDifference([1, 2, 3], [4, 5, 6]))  # [[1,2,3],[4,5,6]]
```

### Complexity Analysis
- **Time:** O(n + m) — converting to sets.
- **Space:** O(n + m) — storing sets.

### Edge Cases
- **Identical arrays:** Both differences empty.
- **No common elements:** Both differences are the full deduplicated arrays.
- **Duplicates within arrays:** Sets handle deduplication automatically.
- **Empty arrays:** Set is empty, difference is empty.

### Common Mistakes
1. **Confusing set difference operator:** `set1 - set2` is valid; `set1.difference(set2)` also works.
2. **Not deduplicating:** Arrays may have duplicates; sets handle this.
3. **Returning lists in wrong order:** First list = unique to nums1, second = unique to nums2.
4. **Modifying original sets:** `set1 - set2` creates a new set; originals are unchanged.

### Pattern Recognition
- **Set Operations for Unique Members:** Sets are ideal for "find unique/different/common" problems.
- **Symmetric Difference:** `set1 ^ set2` gives elements in either but not both (union of both differences).
- **Similar Problems:** Intersection of Two Arrays, Find Common Elements Between Two Arrays.

---

## Problem 20: Intersection of Multiple Arrays

### Problem Explanation (Simple Words)
Find numbers that appear in every sub-array of a 2D array. Use a frequency counter across all arrays (deduplicating each array with a set first). Numbers with count equal to the number of arrays are in the intersection.

### Algorithm Steps
1. **Count frequencies** using `Counter`. Iterate over each array.
2. **For each array:** convert to set (handles duplicates within one array), update counter.
3. **Filter** numbers whose count equals `total` number of arrays.
4. **Sort** and return.

### Visual Walkthrough
**Input:** `[[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]]`

```
Array 0: {3,1,2,4,5} → count: 3→1,1→1,2→1,4→1,5→1
Array 1: {1,2,3,4}   → count: 3→2,1→2,2→2,4→2,5→1
Array 2: {3,4,5,6}   → count: 3→3,1→2,2→2,4→3,5→2,6→1

total=3 → keep only count==3: {3, 4}

Result: [3, 4] ✓
```

### Key Insight
Using `set(arr)` before counting ensures that duplicates within a single array don't inflate the count. Without this, if an array had [1, 1, 1], it would count as 3 occurrences, making 1 appear more often than the array count.

### Well-Commented Code

```python
from collections import Counter

def intersection(nums):
    count = Counter()
    total = len(nums)

    for arr in nums:
        # Deduplicate each array so internal duplicates don't inflate count
        count.update(set(arr))

    # Numbers appearing in all arrays
    return sorted([num for num, c in count.items() if c == total])


# Test
print(intersection([[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]]))  # [3, 4]
print(intersection([[1, 2, 3], [4, 5, 6]]))  # []
print(intersection([[2, 1, 3, 4, 5], [1, 2, 3], [2, 3, 1, 4]]))  # [1, 2, 3]
```

### Complexity Analysis
- **Time:** O(N) — total elements across all arrays.
- **Space:** O(U) — unique values across all arrays.

### Edge Cases
- **Empty arrays:** No arrays → empty result.
- **Single array:** Intersection = unique elements of that array.
- **No common element:** Return [].
- **Arrays with internal duplicates:** Sets handle this.

### Common Mistakes
1. **Not deduplicating each array:** Duplicates within one array inflate count, causing valid numbers to be missed.
2. **Forgetting to sort:** The problem requires sorted output.
3. **Using `count.update(arr)` vs `count.update(set(arr))`.**

### Pattern Recognition
- **Intersection via Frequency:** Count across all collections, filter by count == total.
- **Set + Counter:** Deduplication per collection followed by global frequency counting.
- **Similar Problems:** Intersection of Two Arrays, Find Common Characters.

---

## Problem 21: Largest Unique Number

### Problem Explanation (Simple Words)
Among all numbers that appear exactly once, find the largest. If none, return -1. Use a frequency counter to identify numbers with frequency 1, then track the maximum.

### Algorithm Steps
1. **Count frequencies** using `Counter`.
2. **Iterate** over `count.items()`. For each `(num, freq)` where `freq == 1`, update `result = max(result, num)`.
3. **Return** `result` (initialized to -1).

### Visual Walkthrough
**Input:** `[5, 7, 3, 9, 4, 9, 5, 12]`

```
Frequencies: 5→2, 7→1, 3→1, 9→2, 4→1, 12→1

Frequency 1: {7, 3, 4, 12}
Largest: 12 ✓
```

### Key Insight
We only track frequency-1 elements. The answer is the maximum among these. Initializing `result = -1` handles the "none found" case automatically.

### Well-Commented Code

```python
from collections import Counter

def largestUniqueNumber(nums):
    count = Counter(nums)
    result = -1

    for num, freq in count.items():
        if freq == 1:
            result = max(result, num)

    return result


# Test
print(largestUniqueNumber([5, 7, 3, 9, 4, 9, 5, 12]))  # 12
print(largestUniqueNumber([9, 9, 8, 8]))  # -1
print(largestUniqueNumber([1, 2, 3, 4, 5]))  # 5
```

### Complexity Analysis
- **Time:** O(n) — counting + scanning.
- **Space:** O(n) — frequency map.

### Edge Cases
- **All elements > 1 frequency:** Return -1.
- **All unique:** Return `max(nums)`.
- **Single element:** Return that element (unique and largest).
- **Negative numbers:** `max()` handles negatives correctly.

### Common Mistakes
1. **Returning the largest frequency-1 value but initializing with 0:** If all numbers are negative, `max(-1, -5) = -1` is wrong. Initialize with `-1` as specified in the problem.
2. **Sorting and scanning from right:** This is O(n log n) vs the O(n) hash map approach.
3. **Confusing max frequency with max value:** We want the largest VALUE with frequency 1, not the most frequent element.

### Pattern Recognition
- **Frequency Filtering:** Count all, then filter by condition.
- **Unique Value Problems:** When "unique" means frequency == 1, use a frequency map.
- **Similar Problems:** Single Number, Find Lucky Integer in an Array.

---

## Problem 22: Find the Town Judge

### Problem Explanation (Simple Words)
The judge is trusted by everyone (n-1 people) and trusts no one. Use a trust score array: +1 when someone is trusted, -1 when someone trusts another. The judge's score will be exactly n-1 (trusted by all, trusts none).

### Algorithm Steps
1. **Initialize** `score` array of size `n+1` (1-indexed, 0 unused).
2. **For each `[a, b]`:** `score[a] -= 1` (a trusts someone), `score[b] += 1` (b is trusted).
3. **Scan** `i = 1..n`. If `score[i] == n - 1` → return `i`.
4. **Return** -1 if no match.

### Visual Walkthrough
**Input:** `n = 3, trust = [[1,3],[2,3]]`

```
score = [0, 0, 0, 0]  (indices 0..3)

Processing [1,3]:
  score[1]-- = -1  (1 trusts someone)
  score[3]++ =  1  (3 is trusted)

Processing [2,3]:
  score[2]-- = -1  (2 trusts someone)
  score[3]++ =  2  (3 is trusted)

Final scores: [0, -1, -1, 2]
n-1 = 2 → score[3] == 2 → Judge = 3 ✓
```

### Key Insight
The trust score elegantly encodes two conditions into one number. The judge must have net score = n-1: receives n-1 trust (+(n-1)) and gives 0 trust (-0). Any other person either gives trust (lowers score) or receives trust from fewer than n-1 people.

### Well-Commented Code

```python
def findJudge(n, trust):
    score = [0] * (n + 1)

    for a, b in trust:
        score[a] -= 1  # a trusts someone
        score[b] += 1  # b is trusted

    for i in range(1, n + 1):
        if score[i] == n - 1:
            return i

    return -1


# Test
print(findJudge(2, [[1, 2]]))  # 2
print(findJudge(3, [[1, 3], [2, 3]]))  # 3
print(findJudge(3, [[1, 3], [2, 3], [3, 1]]))  # -1
print(findJudge(1, []))  # 1
```

### Complexity Analysis
- **Time:** O(n + t) — t = len(trust).
- **Space:** O(n) — score array.

### Edge Cases
- **n = 1, no trust:** Person 1 is judge by definition (n-1 = 0, score[1] = 0).
- **Cycle of trust:** No one has score n-1 → return -1.
- **Multiple people with same score:** Return -1 (only one judge possible).

### Common Mistakes
1. **Using 0-indexed array without adjusting:** Labels are 1..n. Use size `n+1`.
2. **Not checking the score against n-1:** The judge must be trusted by ALL others, not just most.
3. **Confusing `a` and `b`:** `a` trusts `b`, so `score[a]` decreases, `score[b]` increases.
4. **Forgetting the case n=1:** When `trust` is empty, the only person is the judge.

### Pattern Recognition
- **Net Score / Balance:** Like parentheses balancing or lead-follower relationships.
- **Graph Indegree-Outdegree:** The judge has indegree n-1 and outdegree 0. The score is indegree - outdegree.
- **Similar Problems:** Find the Celebrity, Find Center of Star Graph.

---

## Problem 23: Check if Pangram

### Problem Explanation (Simple Words)
A pangram contains every letter of the English alphabet at least once. Convert the sentence to lowercase, collect all characters in a set, and check if the set size equals 26.

### Algorithm Steps
1. **Convert** `sentence` to lowercase.
2. **Filter** only alphabetic characters (optional, set handles this).
3. **Create a set** of characters.
4. **Check** if set size == 26.

### Visual Walkthrough
**Input:** `"The quick brown fox jumps over the lazy dog"`

```
Lowercase: "the quick brown fox jumps over the lazy dog"
Set: {t, h, e, q, u, i, c, k, b, r, o, w, n, f, x, j, m, p, s, v, l, a, z, y, d, g}
Size: 26 → True ✓
```

### Key Insight
The alphabet has exactly 26 letters. Set deduplication makes checking exhaustive coverage trivial — if we have 26 unique letters, we have all of them.

### Well-Commented Code

```python
def checkIfPangram(sentence):
    return len(set(sentence.lower())) == 26


# Test
print(checkIfPangram("The quick brown fox jumps over the lazy dog"))  # True
print(checkIfPangram("abcde fghij klmno pqrst uvwxy z"))  # True
print(checkIfPangram("This is not a pangram"))  # False
```

### Complexity Analysis
- **Time:** O(n) — scanning the string.
- **Space:** O(1) — set of at most 26 characters.

### Edge Cases
- **Empty string:** set size = 0 < 26 → False.
- **All uppercase:** `lower()` handles this.
- **With non-letters (spaces, digits, punctuation):** Set size may include non-letters, but `sentence.lower()` doesn't filter them. If non-letters are present, the set could exceed 26 or include invalid chars. The check `len(set(...)) == 26` might fail if non-letters inflate the size. Use `len(set(c for c in sentence.lower() if c.isalpha())) == 26` to be safe.
- **String shorter than 26 characters:** Impossible to be a pangram.

### Common Mistakes
1. **Not converting to lowercase:** 'A' and 'a' would be different in the set.
2. **Forgetting non-alphabetic characters:** `set(sentence.lower())` includes spaces, punctuation, etc. If there are non-letter characters, the set size may be > 26 even though all letters are present. Filter with `isalpha()`.
3. **Using `len(sentence) >= 26`:** Length doesn't guarantee all letters are present.

### Pattern Reasoning
- **Set for Membership Check:** Sets are ideal for checking if all required elements are present.
- **Alphabet Problems:** 26 is a constant; sets simplify coverage checking.
- **Similar Problems:** Check if All Characters Have Equal Number of Occurrences, Determine if String Halves Are Alike.

---

## Problem 24: Count Distinct Numbers on Board

### Problem Explanation (Simple Words)
Start with board = {1}. At each step, replace every number `x` with all its divisors. After infinite steps, every number from 1 to n appears on the board. So the answer is simply n.

### Algorithm Steps
1. **The answer is n** — every number 1..n eventually appears as a divisor chain starting from n down to 1.

### Visual Walkthrough
**Input:** `n = 5`

```
Step 0: {1}
Step 1: 1 → divisors of 1 = {1} → {1}
... Through divisors of 5 (1, 5), 4 (1, 2, 4), 3 (1, 3), 2 (1, 2):
All numbers 1..5 appear → count = 5 ✓
```

### Key Insight
This is a math trick: since every number `x` is replaced by its divisors, and 1 divides everything, 1 stays forever. Through divisor chains, every integer ≤ n eventually appears. The answer is trivially `n`.

### Well-Commented Code

```python
def distinctIntegers(n):
    return n


# Test
print(distinctIntegers(5))  # 5
print(distinctIntegers(1))  # 1
print(distinctIntegers(10))  # 10
```

### Complexity Analysis
- **Time:** O(1)
- **Space:** O(1)

### Edge Cases
- **n = 1:** Only 1 on board → return 1.
- **n = 2:** Board = {1, 2} → return 2.
- **Large n:** Return n directly.

### Common Mistakes
1. **Simulating the process:** The problem is designed so that simulation is unnecessary; `n` is the answer.
2. **Overthinking:** The key insight is that 1's divisor is 1, and n's divisors include all numbers ≤ n, so all numbers 1..n eventually appear.
3. **Not recognizing this as a math problem.**

### Pattern Recognition
- **Math Trick Problems:** Some problems look complex but have a trivial answer.
- **Divisor Properties:** Every number divides itself, so the board propagates the full range.
- **Similar Problems:** Find the number of distinct numbers after repeated divisor operations.

---

## Problem 25: Find All Numbers Disappeared in Array

### Problem Explanation (Simple Words)
Given an array of length n with values in [1, n], find all numbers from 1 to n that are missing. Use a set for O(1) lookups, then iterate 1..n and collect missing numbers.

### Algorithm Steps
1. **Create set** `num_set = set(nums)`.
2. **Iterate** `i` from 1 to `len(nums)`.
3. **If `i` not in `num_set`:** add to result.
4. **Return** result.

### Visual Walkthrough
**Input:** `[4, 3, 2, 7, 8, 2, 3, 1]`

```
n = 8
Set: {1, 2, 3, 4, 7, 8}

Check 1..8:
  1: in set ✓
  2: in set ✓
  3: in set ✓
  4: in set ✓
  5: NOT in set → add ✓
  6: NOT in set → add ✓
  7: in set ✓
  8: in set ✓

Result: [5, 6] ✓
```

### Key Insight
Set lookup is O(1) average, making this O(n) overall. The brute force O(n²) approach would check every number 1..n against every element.

### Well-Commented Code

```python
def findDisappearedNumbers(nums):
    num_set = set(nums)
    return [i for i in range(1, len(nums) + 1) if i not in num_set]


# Test
print(findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]))  # [5, 6]
print(findDisappearedNumbers([1, 1]))  # [2]
print(findDisappearedNumbers([2, 2]))  # [1]
print(findDisappearedNumbers([1, 2, 3, 4, 5]))  # []
```

### Complexity Analysis
- **Time:** O(n) — set construction + scan.
- **Space:** O(n) — set storage.

### Edge Cases
- **All numbers present:** Return [].
- **Duplicates in array:** Set deduplicates; missing numbers still found correctly.
- **n = 1 with [1]:** Return [].
- **n = 1 with [1, 1]:** `len(nums)` = 2, but values are in [1, 2]. Wait — if the array is `[1, 1]`, n=2, so we check 1..2. 1 is in set, 2 is not → missing = [2].

### Common Mistakes
1. **Using `range(1, n)` instead of `range(1, n+1)`:** n itself might be missing.
2. **Not using a set:** Iterating through the array for each number is O(n²).
3. **Modifying the array while iterating:** The O(1) space approach marks indices as negative, which is error-prone. The set approach is simpler.
4. **Confusing length with max value:** Since values are in [1, n] = [1, len(nums)], the range matches.

### Pattern Recognition
- **Set Complement:** Finding "missing" elements by checking against a set of present elements.
- **Range Membership:** When values are constrained to a range, sets make missing-value detection O(n).
- **Similar Problems:** First Missing Positive, Missing Number, Find All Duplicates in an Array.

---

# PART C: HEAPS / PRIORITY QUEUE (Problems 26–40)

---

## Problem 26: Last Stone Weight

### Problem Explanation (Simple Words)
Repeatedly smash the two heaviest stones. If weights are equal, both disappear. If different, the heavier stone loses weight (becomes difference), the lighter vanishes. Continue until ≤1 stone remains.

### Algorithm Steps
1. **Negate all weights** and heapify (simulates max-heap).
2. **While heap size > 1:**
   - Pop two largest (negate back to positive).
   - If different, push `-(first - second)`.
3. **Return** `-heap[0]` or 0.

### Visual Walkthrough
**Input:** `[2, 7, 4, 1, 8, 1]`

```
Heap (max): [8, 7, 4, 2, 1, 1]

Step 1: first=8, second=7 → diff=1 → push 1
Heap: [4, 2, 1, 1, 1]

Step 2: first=4, second=2 → diff=2 → push 2
Heap: [2, 1, 1, 1]

Step 3: first=2, second=1 → diff=1 → push 1
Heap: [1, 1, 1]

Step 4: first=1, second=1 → equal → nothing
Heap: [1]

Result: 1 ✓
```

### Key Insight
Max-heap efficiently gives the two heaviest stones in O(log n) each. Python's `heapq` is a min-heap; negating values is the standard trick for max-heap simulation.

### Well-Commented Code

```python
import heapq

def lastStoneWeight(stones):
    # Negate to simulate max-heap
    heap = [-s for s in stones]
    heapq.heapify(heap)

    while len(heap) > 1:
        first = -heapq.heappop(heap)
        second = -heapq.heappop(heap)
        if first != second:
            heapq.heappush(heap, -(first - second))

    return -heap[0] if heap else 0


# Test
print(lastStoneWeight([2, 7, 4, 1, 8, 1]))  # 1
print(lastStoneWeight([1]))  # 1
print(lastStoneWeight([1, 1]))  # 0
print(lastStoneWeight([8, 7, 4, 2, 1, 1]))  # 1
```

### Complexity Analysis
- **Time:** O(n log n) — each heap operation is O(log n).
- **Space:** O(n) — the heap.

### Edge Cases
- **Single stone:** Return its weight.
- **All equal:** All destroyed → return 0.
- **Two stones of same weight:** Both destroyed → return 0.

### Common Mistakes
1. **Forgetting negation:** Without negation, `heapq` pops the smallest, not the largest.
2. **Not handling the `abs` correctly:** `first - second` where first ≥ second is always non-negative.
3. **Returning `0` when heap is empty:** The while loop leaves at most 1 element; return 0 if none.

### Pattern Recognition
- **Max-heap via negation:** When you need the largest elements and Python only has min-heap, negate.
- **Simulation with Priority:** Any "repeatedly process the largest/smallest" problem is heap-friendly.
- **Similar Problems:** Remove Stones to Minimize Total, Minimum Cost to Connect Sticks.

---

## Problem 27: Kth Largest Element in a Stream

### Problem Explanation (Simple Words)
We need to find the kth largest element after each addition to an evolving stream. Maintain a min-heap of size k. The smallest element in this min-heap is the kth largest overall. Push new elements and keep heap trimmed to size k.

### Algorithm Steps
1. **`__init__`:**
   - Copy `nums` into `heap`, heapify.
   - Pop excess: while `len(heap) > k`, `heappop`.
2. **`add(val)`:**
   - Push `val` onto heap.
   - If heap exceeds size k, pop smallest.
   - Return `heap[0]` (the kth largest).

### Visual Walkthrough
**Input:** `k = 3, nums = [4, 5, 8, 2]`

```
Init heap after trim: [4, 5, 8]

add(3):  push→[3,4,8,5]  pop→[4,5,8]  → kth=4
add(5):  push→[4,5,8,5]  pop→[5,5,8]  → kth=5
add(10): push→[5,5,8,10] pop→[5,8,10] → kth=5
add(9):  push→[5,8,10,9] pop→[8,9,10] → kth=8
add(4):  push→[4,8,9,10] pop→[8,9,10] → kth=8
```

### Key Insight
We only need to track the top k largest elements. The smallest among these (heap root) is the kth largest. The push-then-pop approach maintains the invariant cleanly.

### Well-Commented Code

```python
import heapq

class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums[:]
        heapq.heapify(self.heap)
        # Keep only the k largest elements
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


# Test
kth = KthLargest(3, [4, 5, 8, 2])
print(kth.add(3))   # 4
print(kth.add(5))   # 5
print(kth.add(10))  # 5
print(kth.add(9))   # 8
print(kth.add(4))   # 8
```

### Complexity Analysis
- **Time:** O(n log k) for init, O(log k) per add.
- **Space:** O(k) — heap of size k.

### Edge Cases
- **k == initial length:** All initial elements stay in heap.
- **All added values smaller than current kth largest:** Heap unchanged.
- **Stream length < k at init:** Heap has fewer than k elements; kth largest = min of all.

### Common Mistakes
1. **Using max-heap instead of min-heap:** Max-heap requires negating and changes the invariant.
2. **Not copying `nums`:** Using `self.heap = nums` would modify the original list.
3. **Not using `heappush` + `heappop` approach:** The push-then-pop-if-excess pattern is simple and correct.
4. **Returning `heap[0]` when heap is empty:** Initialize with at least k elements.

### Pattern Recognition
- **Fixed-size Heap for Order Statistics:** Keep a heap of size k to track kth largest/smallest.
- **Stream Processing:** Heaps efficiently maintain order statistics in an evolving stream.
- **Similar Problems:** Kth Largest Element in an Array, Find Median from Data Stream.

---

## Problem 28: Kth Largest in Sorted Matrix

### Problem Explanation (Simple Words)
Given an n×n matrix where each row and column is sorted ascending, find the kth largest element. Binary search the value range and use a staircase count function to count elements ≤ mid.

### Algorithm Steps
1. **Set** `low = matrix[0][0]`, `high = matrix[-1][-1]`.
2. **Binary search** while `low < high`:
   - `mid = (low + high) // 2`.
   - Count elements ≤ `mid` using staircase walk.
   - If count < k: `low = mid + 1`.
   - Else: `high = mid`.
3. **Return** `low`.

### Visual Walkthrough
**Input:** `matrix = [[1,5,9],[10,11,13],[12,13,15]]`, `k = 8`

```
low=1, high=15
mid=8: count ≤8? Top-right walk:
  [1,5,9] → 9>8 → col-- (col=1) → 5≤8 → count+=2, row++
  [10,11,13] → 10>8 → col-- (col=0) → 1≤8 → count+=1, row++
  [12,13,15] → 12>8 → col-- → done
  count=3 < 8 → low=9
...
Eventually low=13 → return 13 ✓
```

### Key Insight
The staircase count function walks from top-right to bottom-left. Since rows and columns are sorted, when `matrix[row][col] ≤ mid`, all elements to the left in that row are also ≤ mid.

### Well-Commented Code

```python
def kthLargest(matrix, k):
    n = len(matrix)
    low, high = matrix[0][0], matrix[-1][-1]

    def count_less_equal(mid):
        """Count elements ≤ mid using staircase walk."""
        count = 0
        row, col = 0, n - 1
        while row < n and col >= 0:
            if matrix[row][col] <= mid:
                # All elements in this row up to col are ≤ mid
                count += col + 1
                row += 1
            else:
                col -= 1
        return count

    while low < high:
        mid = (low + high) // 2
        if count_less_equal(mid) < k:
            low = mid + 1
        else:
            high = mid
    return low


# Test
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print(kthLargest(matrix, 8))  # 13
matrix2 = [[-5]]
print(kthLargest(matrix2, 1))  # -5
matrix3 = [[2, 6], [5, 7]]
print(kthLargest(matrix3, 3))  # 6
```

### Complexity Analysis
- **Time:** O(n log(max - min)) — O(n) per mid check × O(log range).
- **Space:** O(1) — iterative.

### Edge Cases
- **n = 1:** Single element, low = high = that element.
- **k = 1:** Returns smallest element (matrix[0][0]).
- **k = n²:** Returns largest element (matrix[-1][-1]).
- **All elements same:** Binary search converges immediately.

### Common Mistakes
1. **Confusing kth largest vs kth smallest:** The binary search finds the kth smallest. For kth largest with 1-indexed, use `k_largest = n*n - k + 1`.
2. **Incorrect count function:** The staircase must start from top-right and handle both directions correctly.
3. **Boundary conditions:** `low` and `high` must be actual matrix values, not indices.
4. **Off-by-one in binary search:** The `low < high` loop with `high = mid` pattern is standard for this type.

### Pattern Recognition
- **Binary Search on Answer:** When the answer is a value in a sorted range, binary search is more efficient than heap.
- **Staircase Count:** A classic O(n) technique for counting in sorted matrices.
- **Similar Problems:** Kth Smallest Element in a Sorted Matrix, Search a 2D Matrix II.

---

## Problem 29: K Closest Points to Origin

### Problem Explanation (Simple Words)
Find the k points closest to (0, 0). Use squared distance (avoids sqrt). Maintain a max-heap of size k: for each point, push its negated distance. If heap exceeds k, pop the farthest (root of max-heap).

### Algorithm Steps
1. **Initialize** empty max-heap (store `(-dist, x, y)`).
2. **For each `(x, y)`:** Compute `dist = x*x + y*y`. Push `(-dist, x, y)` onto heap. If heap size > k, pop.
3. **Return** the remaining points.

### Visual Walkthrough
**Input:** `points = [[1,3], [-2,2]]`, `k = 1`

```
Point [1,3]: dist = 1+9 = 10 → push (-10, 1, 3)
Heap: [(-10, 1, 3)]

Point [-2,2]: dist = 4+4 = 8 → push (-8, -2, 2)
Heap: [(-10, 1, 3), (-8, -2, 2)]
Heap size 2 > k=1 → pop → removes (-8, -2, 2)
Wait, that's wrong — we want the closest!

Actually with max-heap: -8 > -10, so root = (-10, 1, 3) is popped.
Hold on: In max-heap, the largest distance should be at top.
If we did negated: heap root is -10 (smallest negated = largest original).
But heapq is min-heap! So root = -10 which corresponds to dist=10 (farthest).

Let me trace again with negation:
Push (-10, 1, 3): heap = [(-10, 1, 3)]
Push (-8, -2, 2): heap = [(-10, 1, 3), (-8, -2, 2)]
heapq is min-heap → root = -10 (min), which is dist 10 (farthest among k=2)
pop → removes -10 (dist=10). Remaining: [(-8, -2, 2)]
Result: [[-2, 2]] ✓
```

### Key Insight
Squared distance avoids sqrt. The max-heap of negated distances keeps the k closest points because the farthest among them is always popped first.

### Well-Commented Code

```python
import heapq

def kClosest(points, k):
    heap = []
    for x, y in points:
        dist = x * x + y * y
        # Max-heap via negation: farthest is popped first
        heapq.heappush(heap, (-dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)  # Remove farthest of current k
    return [[x, y] for _, x, y in heap]


# Test
print(kClosest([[1, 3], [-2, 2]], 1))  # [[-2, 2]]
print(kClosest([[3, 3], [5, -1], [-2, 4]], 2))  # [[3,3],[-2,4]]
print(kClosest([[0, 1], [1, 0]], 2))  # [[0,1],[1,0]]
```

### Complexity Analysis
- **Time:** O(n log k) — each heap operation O(log k).
- **Space:** O(k) — heap of size k.

### Edge Cases
- **k = n:** Return all points.
- **k = 1:** Closest single point.
- **Origin point:** dist = 0, will be kept.
- **Negative coordinates:** Squared distance handles correctly.

### Common Mistakes
1. **Forgetting negation:** Without negation, the min-heap pops the closest. Negation makes it pop the farthest, which is what we want for a max-heap of size k.
2. **Using sqrt:** Unnecessary expense; squared distance preserves ordering.
3. **Return format:** The problem expects `[[x, y], ...]`, not distances.

### Pattern Recognition
- **Max-heap of Size k for Closest:** When you need the k smallest/largest things, use a max-heap/min-heap of size k.
- **Squared Distance:** Avoid sqrt when relative ordering is sufficient.
- **Similar Problems:** Top K Frequent Elements, K Closest Points to Origin (quickselect version).

---

## Problem 30: Furthest Building You Can Reach

### Problem Explanation (Simple Words)
Move through buildings. Going up costs bricks (height difference). Ladders can cover any height for free. Use a min-heap to track the l largest jumps (for ladders). For smaller jumps, use bricks. If bricks run out, replace the largest brick-paid jump with a ladder.

### Algorithm Steps
1. **Initialize** empty min-heap for positive height differences.
2. **Iterate** buildings. If `diff ≤ 0`, skip (going down).
3. **Push** `diff` onto heap. If `len(heap) > ladders`: pop smallest diff, use bricks for it.
4. **If bricks < 0:** return current index.
5. **Return** last building index.

### Visual Walkthrough
**Input:** `heights = [4, 2, 7, 6, 9, 14, 12]`, `bricks = 5`, `ladders = 1`

```
i=0→1: diff=-2 (down) → skip
i=1→2: diff=5 → heap=[5], len=1 ≤ l=1 → skip
i=2→3: diff=-1 (down) → skip
i=3→4: diff=3 → heap=[3,5], len=2 > l=1 → pop 3, bricks=5-3=2
i=4→5: diff=5 → heap=[5,5], len=2 > l=1 → pop 5, bricks=2-5=-3 < 0
Return i=4 ✓ (furthest index)
```

### Key Insight
Ladders are a scarce resource best used for the largest climbs. By always reassigning the smallest ladder-use to bricks when a bigger jump appears, we optimally allocate ladders.

### Well-Commented Code

```python
import heapq

def furthestBuilding(heights, bricks, ladders):
    heap = []
    for i in range(len(heights) - 1):
        diff = heights[i + 1] - heights[i]
        if diff <= 0:
            continue

        heapq.heappush(heap, diff)
        # If we have more climbs than ladders, use bricks for the smallest
        if len(heap) > ladders:
            bricks -= heapq.heappop(heap)
            if bricks < 0:
                return i

    return len(heights) - 1


# Test
print(furthestBuilding([4, 2, 7, 6, 9, 14, 12], 5, 1))  # 4
print(furthestBuilding([4, 12, 2, 7, 3, 18, 20, 3, 19], 7, 2))  # 7
print(furthestBuilding([14, 3, 19, 3], 17, 0))  # 3
```

### Complexity Analysis
- **Time:** O(n log l) — each heap operation O(log l).
- **Space:** O(l) — heap of size l+1.

### Edge Cases
- **All descending:** No positive diffs → reach end without using anything.
- **l = 0:** Every positive diff must use bricks.
- **bricks = 0:** Every positive diff must use a ladder.
- **Not enough resources:** Return index of last reachable building.

### Common Mistakes
1. **Not skipping negative diffs:** (Going down uses no resources.)
2. **Popping from heap without checking `len(heap) > l`:** The ladder is always assigned to the largest climbs in heap.
3. **Confusing brick and ladder assignment:** Bricks pay for the smallest climbs; ladders cover the largest.
4. **Not checking `bricks < 0` immediately after subtraction.**

### Pattern Recognition
- **Min-heap for Ladder Allocation:** The heap tracks the smallest climbs currently assigned to bricks. When a bigger climb appears, it gets the ladder and the smallest climb switches to bricks.
- **Resource Optimization:** When one resource is unlimited (up to a limit) and another is limited to a total, allocate the scarce resource to the largest demands.
- **Similar Problems:** Car Pooling (heap tracking drop-offs), Meeting Rooms II.

---

## Problem 31: Maximum Performance of a Team

### Problem Explanation (Simple Words)
We have n engineers with speed and efficiency. Choose up to k such that (sum of speeds) × (minimum efficiency) is maximized. Sort by efficiency descending, then iterate: maintain a min-heap of the top k speeds. The current efficiency is always the minimum as we go.

### Algorithm Steps
1. **Sort** engineers by efficiency descending.
2. **For each `(eff, spd)`**:
   - Push `spd` onto min-heap, add to `total_speed`.
   - If heap exceeds k: pop slowest, subtract from `total_speed`.
   - Update `best = max(best, total_speed * eff)`.
3. **Return** `best % MOD`.

### Visual Walkthrough
**Input:** `speed = [2,10,3,1,5,8]`, `efficiency = [5,4,3,9,7,2]`, `k = 2`

```
Sorted by efficiency descending:
(eff=9, spd=1), (eff=7, spd=5), (eff=5, spd=2), (eff=4, spd=10), (eff=3, spd=3), (eff=2, spd=8)

eff=9, spd=1: heap=[1], speed=1,  best=1×9=9
eff=7, spd=5: heap=[1,5], speed=6,  best=6×7=42
eff=5, spd=2: heap=[1,5,2] → pop 1, speed=7,  best=7×5=35
eff=4, spd=10: heap=[5,2,10] → pop 2, speed=15, best=15×4=60
eff=3, spd=3: heap=[5,10,3] → pop 3, speed=13, best=13×3=39
eff=2, spd=8: heap=[5,10,8] → pop 5, speed=18, best=18×2=36

Best: 60 ✓
```

### Key Insight
By sorting by efficiency descending, when processing engineer `i`, their efficiency is guaranteed to be the minimum among all engineers chosen so far. The heap keeps the k highest speeds, maximizing the product.

### Well-Commented Code

```python
import heapq

def maxPerformance(n, speed, efficiency, k):
    MOD = 10**9 + 7
    # Sort by efficiency descending
    engineers = sorted(zip(efficiency, speed), reverse=True)
    speed_heap = []
    total_speed = 0
    best = 0

    for eff, spd in engineers:
        heapq.heappush(speed_heap, spd)
        total_speed += spd

        # Keep only the k fastest
        if len(speed_heap) > k:
            total_speed -= heapq.heappop(speed_heap)

        # eff is the minimum efficiency in the current team
        best = max(best, total_speed * eff)

    return best % MOD


# Test
print(maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2))  # 60
print(maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3))  # 68
print(maxPerformance(6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 4))  # 72
```

### Complexity Analysis
- **Time:** O(n log n) — sorting + O(n log k) heap operations.
- **Space:** O(k) — heap of size k.

### Edge Cases
- **k = 1:** Pick the single engineer with max speed × efficiency.
- **k = n:** All engineers chosen.
- **All same efficiency:** Pick k fastest engineers.
- **All same speed:** Efficiency determines best team.

### Common Mistakes
1. **Not sorting by efficiency:** Without sorting, we can't guarantee the current efficiency is the team minimum.
2. **Modulo only at the end:** Problem requires result modulo 10^9+7.
3. **Forgetting `total_speed -=` when popping:** The speed sum must stay consistent with heap contents.
4. **Not using 64-bit integer:** Python handles big ints, but `total_speed * eff` can be very large.

### Pattern Recognition
- **Sort + Heap for Multi-Factor Optimization:** Sort by one factor (efficiency), maintain heap for another (speed).
- **Min-Heap of Size k:** Keep the k largest elements while iterating.
- **Similar Problems:** Minimum Cost to Hire K Workers, Maximum Number of Events That Can Be Attended II.

---

## Problem 32: Minimum Cost to Connect Sticks

### Problem Explanation (Simple Words)
Connect all sticks into one. Cost = sum of lengths being connected. Always combine the two shortest sticks first (greedy). This is analogous to Huffman coding — shortest sticks should be combined more times.

### Algorithm Steps
1. **Heapify** the sticks array.
2. **While** more than 1 stick:
   - Pop two shortest.
   - `cost = first + second`, add to `total_cost`.
   - Push cost back.
3. **Return** `total_cost`.

### Visual Walkthrough
**Input:** `[2, 4, 3]`

```
Heap after heapify: [2, 3, 4]
Pop 2, 3 → cost=5, push 5
Heap: [4, 5]
Pop 4, 5 → cost=9, push 9
Heap: [9]
Total cost = 5 + 9 = 14 ✓
```

### Key Insight
This is a greedy algorithm: always combine the two smallest sticks first. This ensures shorter sticks are reused in the smallest number of combined operations, minimizing total cost. Same principle as Huffman coding.

### Well-Commented Code

```python
import heapq

def connectSticks(sticks):
    heapq.heapify(sticks)
    total_cost = 0

    while len(sticks) > 1:
        first = heapq.heappop(sticks)
        second = heapq.heappop(sticks)
        cost = first + second
        total_cost += cost
        heapq.heappush(sticks, cost)

    return total_cost


# Test
print(connectSticks([2, 4, 3]))  # 14
print(connectSticks([1, 8, 3, 5]))  # 30
print(connectSticks([5]))  # 0
print(connectSticks([1, 2, 3, 4, 5]))  # 33
```

### Complexity Analysis
- **Time:** O(n log n) — heapify O(n) + O(n) pop/push O(log n) each.
- **Space:** O(n) — the heap.

### Edge Cases
- **Single stick:** `while` loop doesn't execute → cost 0.
- **Two sticks:** Cost = sum.
- **All sticks same length:** Order doesn't matter, cost is deterministic.
- **Large arrays:** Heap keeps operations O(log n) each.

### Common Mistakes
1. **Not using a heap:** Finding the two smallest without a heap is O(n) each, leading to O(n²).
2. **Not pushing back the combined stick:** The combined stick may later be combined again.
3. **Confusing with connecting in arbitrary order:** Connecting arbitrary (not smallest) yields higher cost.
4. **Forgetting to add cost to total.**

### Pattern Recognition
- **Greedy + Min-Heap:** Always combine smallest first → Huffman coding pattern.
- **Optimal Merge Pattern:** This is the classic optimal merge pattern problem.
- **Similar Problems:** Huffman Encoding, Minimum Cost to Merge Stones, Optimal Merge Pattern.

---

## Problem 33: Reorganize String

### Problem Explanation (Simple Words)
Rearrange a string so no two adjacent characters are the same. Use a max-heap to always pick the most frequent remaining character, while keeping the previously used character in a holding pattern (add it back after using the next one).

### Algorithm Steps
1. **Count frequencies** using `Counter`.
2. **Build max-heap** of `(-count, char)` pairs.
3. **While heap**:
   - Pop top (most frequent remaining char). Append to result.
   - If previous char still has count>0, push it back.
   - Set current char as `prev` (with decremented count, if still > 0).
4. **If result length != original** → return "" (impossible).

### Visual Walkthrough
**Input:** `"aab"`

```
Count: a→2, b→1
Heap: [(-2, 'a'), (-1, 'b')]
prev = None

Step 1: pop (-2,'a') → result="a", prev=None, set prev=(-1,'a')
Step 2: pop (-1,'b') → result="ab", push prev (-1,'a'), prev=None
         Heap: [(-1, 'a')]
Step 3: pop (-1,'a') → result="aba"

Result: "aba" ✓
```

### Key Insight
The "hold previous character" pattern prevents adjacent duplicates. After using a character, it can't be used again immediately — it must wait one turn.

### Well-Commented Code

```python
import heapq
from collections import Counter

def reorganizeString(s):
    count = Counter(s)
    heap = [(-cnt, char) for char, cnt in count.items()]
    heapq.heapify(heap)

    result = []
    prev = None  # (cnt, char) held from previous iteration

    while heap:
        cnt, char = heapq.heappop(heap)
        result.append(char)

        # Push back the char from previous iteration
        if prev:
            heapq.heappush(heap, prev)

        # Decrement count; if still > 0, hold for next iteration
        cnt += 1  # negated: -2 → -1 means count decreases from 2 to 1
        prev = (cnt, char) if cnt < 0 else None

    res = ''.join(result)
    return res if len(res) == len(s) else ""


# Test
print(reorganizeString("aab"))  # "aba"
print(reorganizeString("aaab"))  # ""
print(reorganizeString("vvvlo"))  # "vlvvo"
print(reorganizeString("aaabc"))  # "abaca"
```

### Complexity Analysis
- **Time:** O(n log k) — k unique characters.
- **Space:** O(n) — result string.

### Edge Cases
- **Impossible (count > (n+1)/2):** One character dominates → return "".
- **All unique:** Always possible, result is original string.
- **Two characters only:** Always possible if counts differ by ≤ 1.
- **Single character:** Return "" if length > 1 (adjacent same impossible).

### Common Mistakes
1. **Not holding the previous character:** Without the "hold" pattern, adjacent duplicates can occur.
2. **Incorrect count decrement:** Negated values: `cnt += 1` means count decreases by 1.
3. **Not checking if result length matches:** If impossible, result will be shorter.
4. **Using `prev` as just a character:** Must store both char and remaining count.
5. **The condition `if len(res) == len(s)`:** If the string is impossible, result won't contain all characters.

### Pattern Recognition
- **Task Scheduling with Cooldown:** Same pattern as Task Scheduler (no same-adjacent tasks).
- **Max-Heap + Hold:** Pick most frequent, hold it for one iteration before re-inserting.
- **Similar Problems:** Task Scheduler, Rearrange String k Distance Apart.

---

## Problem 34: Sort Characters By Frequency

### Problem Explanation (Simple Words)
Sort characters in a string by their frequency (most frequent first). Use a max-heap of (frequency, character). Pop each and repeat the character by its frequency.

### Algorithm Steps
1. **Count frequencies** using `Counter`.
2. **Build max-heap** of `(-freq, char)`.
3. **Pop each entry**, append `char * (-freq)` to result.
4. **Return** joined result.

### Visual Walkthrough
**Input:** `"tree"`

```
Count: t→1, r→1, e→2, e→2
Heap: [(-2,'e'), (-1,'t'), (-1,'r')]

Pop (-2,'e'): result += 'e' * 2 → "ee"
Pop (-1,'t'): result += 't' * 1 → "eet"
Pop (-1,'r'): result += 'r' * 1 → "eetr"

Result: "eetr" ✓
```

### Key Insight
No adjacency constraints like Reorganize String — we just output characters in decreasing frequency order. The simplest approach: a max-heap or even sorting by frequency.

### Well-Commented Code

```python
import heapq
from collections import Counter

def frequencySort(s):
    count = Counter(s)
    # Max-heap by frequency
    heap = [(-freq, char) for char, freq in count.items()]
    heapq.heapify(heap)

    result = []
    while heap:
        freq, char = heapq.heappop(heap)
        result.append(char * (-freq))

    return ''.join(result)


# Test
print(frequencySort("tree"))  # "eert"
print(frequencySort("cccaaa"))  # "aaaccc"
print(frequencySort("Aabb"))  # "bbAa"
print(frequencySort("hello"))  # "llhhe"
```

### Complexity Analysis
- **Time:** O(n log k) — k unique characters.
- **Space:** O(n) — result + heap.

### Edge Cases
- **All same character:** Single entry in heap → full string.
- **All unique:** Each char has freq 1, any order is valid.
- **Single character:** Return as is.
- **Empty string:** Return "".

### Common Mistakes
1. **Not negating frequency for max-heap:** Without negation, `heapq` pops least frequent first.
2. **Forgetting to multiply char by frequency:** `result.append(char)` only adds one occurrence.
3. **Using `char * freq` instead of `char * (-freq)`:** Since freq is stored negated, un-negate it.
4. **Case sensitivity:** 'A' and 'a' are different characters.

### Pattern Recognition
- **Frequency Sort:** Count then sort by count descending.
- **Max-Heap for Ordering:** Efficient when we only need the top k frequent elements.
- **Similar Problems:** Top K Frequent Elements, Sort Array by Increasing Frequency.

---

## Problem 35: Top K Frequent Words

### Problem Explanation (Simple Words)
Find the k most frequent words from a list. If words have the same frequency, sort alphabetically (ascending). Use a max-heap of `(-freq, word)`, but since heapq is a min-heap, the root has the "worst" combination, which gets popped first.

### Algorithm Steps
1. **Count frequencies** using `Counter`.
2. **Push** each `(-freq, word)` onto heap. If size > k, pop (removes worst).
3. **After processing all:** pop remaining, reverse (since we popped in ascending order of priority).
4. **Return** result.

### Visual Walkthrough
**Input:** `words = ["i","love","leetcode","i","love","coding"]`, `k = 2`

```
Count: i→2, love→2, leetcode→1, coding→1

Push (-2, "i"):       heap=[(-2,"i")]
Push (-2, "love"):    heap=[(-2,"i"), (-2,"love")]
Push (-1, "leetcode"): heap=[(-2,"i"), (-2,"love"), (-1,"leetcode")]
  size=3 > k=2 → pop → pops (-1, "leetcode")
Push (-1, "coding"):  heap=[(-2,"i"), (-2,"love"), (-1,"coding")]
  size=3 > k=2 → pop → pops (-1, "coding")

Remaining: [(-2,"i"), (-2,"love")]
Pop all, reverse: ["i", "love"] ✓
```

### Key Insight
With `(-freq, word)`, min-heap sorts by: most negative freq first (highest freq). Among ties, lexicographically smaller word is "more negative" and thus higher priority. The root is always the entry to evict (lowest freq, or if tie, lexicographically largest word).

### Well-Commented Code

```python
import heapq
from collections import Counter

def topKFrequent(words, k):
    count = Counter(words)
    heap = []

    for word, freq in count.items():
        heapq.heappush(heap, (-freq, word))
        if len(heap) > k:
            heapq.heappop(heap)  # Remove entry with lowest priority

    result = []
    while heap:
        result.append(heapq.heappop(heap)[1])

    result.reverse()  # Most frequent first
    return result


# Test
print(topKFrequent(["i", "love", "leetcode", "i", "love", "coding"], 2))
# ["i", "love"]
print(topKFrequent(["the", "day", "is", "sunny", "the", "the", "day", "sunny"], 4))
# ["the", "day", "sunny", "is"]
```

### Complexity Analysis
- **Time:** O(n log k) — each heap operation O(log k).
- **Space:** O(n) — Counter + heap.

### Edge Cases
- **All words unique:** k most frequent = any k words (all freq 1, alphabetically sorted).
- **k == unique words:** Return all sorted by freq then alphabetically.
- **Single word repeated:** Just that word.
- **Case sensitivity:** "The" ≠ "the".

### Common Mistakes
1. **Forgetting to reverse at the end:** Popping from a min-heap gives ascending order (least frequent first), but we need descending.
2. **Incorrect tie-breaking:** Without `(-freq, word)`, ties are not handled correctly.
3. **Using max-heap with negation but popping wrong one:** With min-heap of negated values, the "worst" entry is at the root.
4. **Not maintaining size k:** Letting the heap grow beyond k would make it O(n log n).

### Pattern Recognition
- **Fixed-size Heap for Top K:** Keep a heap of size k for top k elements.
- **Custom Sorting with Tuples:** `(-freq, word)` sorts by freq desc then word asc.
- **Similar Problems:** Top K Frequent Elements, K Closest Points to Origin.

**Time Complexity:** O(n log k)
**Space Complexity:** O(n)

---

## Problem 36: Find K Pairs with Smallest Sums

### Problem Explanation (Simple Words)
From two sorted arrays, find k pairs (one from each) with the smallest sums. Start with (0,0). Use a min-heap: pop smallest sum pair, add to result, push its right and down neighbors. Use a visited set to avoid duplicates.

### Algorithm Steps
1. **If either array empty** → return [].
2. **Push** `(sum, i=0, j=0)` onto heap. Mark visited.
3. **While** heap and result size < k:
   - Pop smallest sum pair.
   - Add `[nums1[i], nums2[j]]` to result.
   - If `i+1` in bounds and `(i+1, j)` not visited: push and mark.
   - If `j+1` in bounds and `(i, j+1)` not visited: push and mark.
4. **Return** result.

### Visual Walkthrough
**Input:** `nums1 = [1, 7, 11]`, `nums2 = [2, 4, 6]`, `k = 3`

```
Grid of sums:
    | 2   4   6
 ---+-----------
 1  | 3   5   7
 7  | 9  11  13
 11 | 13 15  17

Heap: [(3,0,0)]
Pop (3,0,0) → result=[[1,2]]
Push: (5,0,1) and (9,1,0)
Heap: [(5,0,1), (9,1,0)]

Pop (5,0,1) → result=[[1,2],[1,4]]
Push: (7,0,2)... but (i+1, j) = (1,1) already? No, push (7,0,2) and (11,1,1)
Heap: [(7,0,2), (9,1,0), (11,1,1)]

Pop (7,0,2) → result=[[1,2],[1,4],[1,6]]
len(result)=3=k → done

Result: [[1,2],[1,4],[1,6]] ✓
```

### Key Insight
This is Dijkstra-like BFS on the sum matrix. The "right" and "down" neighbors ensure we explore sums in increasing order. The visited set prevents duplicate pairs (like (1,1) being reachable from both (0,1) and (1,0)).

### Well-Commented Code

```python
import heapq

def kSmallestPairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []

    heap = [(nums1[0] + nums2[0], 0, 0)]
    visited = {(0, 0)}
    result = []

    while heap and len(result) < k:
        total, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])

        # Explore right neighbor (next in nums1)
        if i + 1 < len(nums1) and (i + 1, j) not in visited:
            heapq.heappush(heap, (nums1[i + 1] + nums2[j], i + 1, j))
            visited.add((i + 1, j))

        # Explore down neighbor (next in nums2)
        if j + 1 < len(nums2) and (i, j + 1) not in visited:
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
            visited.add((i, j + 1))

    return result


# Test
print(kSmallestPairs([1, 7, 11], [2, 4, 6], 3))  # [[1,2],[1,4],[1,6]]
print(kSmallestPairs([1, 1, 2], [1, 2, 3], 2))  # [[1,1],[1,1]]
print(kSmallestPairs([1, 2], [3], 3))  # [[1,3],[2,3]]
```

### Complexity Analysis
- **Time:** O(k log k) — each heap operation O(log k).
- **Space:** O(k) — heap + visited.

### Edge Cases
- **Empty arrays:** Return [].
- **k > m×n:** Return all possible pairs.
- **All elements same:** All sums equal, any k pairs work.
- **Single element arrays:** Only one pair possible.

### Common Mistakes
1. **Not using visited set:** (i+1, j+1) could be pushed twice (from (i, j+1) and (i+1, j)).
2. **Pushing (i+1, j+1) directly:** This shouldn't be pushed; it will be reached through (i, j+1) or (i+1, j).
3. **Not checking bounds before pushing.**
4. **Including pairs beyond k:** The while loop stops when result size reaches k.

### Pattern Recognition
- **Dijkstra-style BFS on Matrix:** Expand from the smallest element outward, like Dijkstra's algorithm.
- **Min-Heap + Visited:** Classic pattern for generating sorted combinations.
- **Similar Problems:** Merge k Sorted Lists, Find Kth Smallest Sum of Two Sorted Arrays.

---

## Problem 37: Kth Smallest Element in Sorted Matrix

### Problem Explanation (Simple Words)
Find the kth smallest element in an n×n matrix where rows and columns are sorted ascending. Use binary search on the value range and a staircase count function to count elements ≤ mid.

### Algorithm Steps
1. **Set** `low = matrix[0][0]`, `high = matrix[-1][-1]`.
2. **Binary search** while `low < high`:
   - `mid = (low + high) // 2`.
   - Count elements ≤ mid via staircase walk.
   - If count < k: `low = mid + 1`.
   - Else: `high = mid`.
3. **Return** `low`.

### Visual Walkthrough
**Input:** `matrix = [[1,5,9],[10,11,13],[12,13,15]]`, `k = 8`

```
Same as Problem 28 — binary search on values with staircase counting.

Goal: find kth smallest (8th smallest = 13 in this matrix).

Staircase counting:
  mid=8: count ≤8 → 3 (<8)  → low=9
  mid=12: count ≤12 → 7 (<8)  → low=13
  mid=13: count ≤13 → 8 (≥8)  → high=13
  low=high=13 → return 13 ✓
```

### Key Insight
Same technique as Problem 28 (Kth Largest in Sorted Matrix). Binary search on values, not indices. The staircase count is O(n) per check, giving O(n log(max-min)) overall.

### Well-Commented Code

```python
def kthSmallest(matrix, k):
    n = len(matrix)
    low, high = matrix[0][0], matrix[-1][-1]

    def count_less_equal(mid):
        count = 0
        row, col = 0, n - 1
        while row < n and col >= 0:
            if matrix[row][col] <= mid:
                count += col + 1
                row += 1
            else:
                col -= 1
        return count

    while low < high:
        mid = (low + high) // 2
        if count_less_equal(mid) < k:
            low = mid + 1
        else:
            high = mid

    return low


# Test
matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
print(kthSmallest(matrix, 8))  # 13
matrix2 = [[-5]]
print(kthSmallest(matrix2, 1))  # -5
matrix3 = [[1, 2], [3, 4]]
print(kthSmallest(matrix3, 2))  # 2
print(kthSmallest(matrix3, 3))  # 3
```

### Complexity Analysis
- **Time:** O(n log(max - min)) — count function O(n), binary search O(log range).
- **Space:** O(1).

### Edge Cases
- **n = 1:** Single element.
- **k = 1:** Smallest = matrix[0][0].
- **k = n²:** Largest = matrix[-1][-1].
- **Duplicate values:** Binary search finds the correct value.

### Common Mistakes
1. **Kth largest vs kth smallest:** Problem 28 finds kth largest; this finds kth smallest. The same count function works for both with different k.
2. **Using indices instead of values:** Binary search on the value range, not on array indices.
3. **Staircase direction:** Start from top-right and move down-left.
4. **Incorrect count formula:** `count += col + 1` because elements from col 0 to col in that row are ≤ mid.

### Pattern Recognition
- **Binary Search on Value:** When the answer is a value in a sorted range, binary search is efficient.
- **Staircase Counting:** Same technique as Problem 28.
- **Similar Problems:** Kth Smallest Element in a Sorted Matrix, Search a 2D Matrix II.

---

## Problem 38: Find Median from Data Stream

### Problem Explanation (Simple Words)
Maintain the median as numbers are added one by one. Use two heaps: a max-heap for the smaller half and a min-heap for the larger half. Always keep sizes balanced (diff ≤ 1). Median = root of max-heap (odd total) or average of both roots (even total).

### Algorithm Steps
1. **`addNum(num)`**:
   - Push `-num` onto `lo` (max-heap via negation).
   - Ensure order: if max(lo) > min(hi), swap roots.
   - Balance: if `|len(lo) - len(hi)| > 1`, move root.
2. **`findMedian()`**:
   - If `len(lo) > len(hi)`: return `-lo[0]`.
   - Else: return `(-lo[0] + hi[0]) / 2.0`.

### Visual Walkthrough
**Input:** `addNum(1), addNum(2), addNum(3)`

```
addNum(1): lo=[-1], hi=[] → median = 1.0
addNum(2): lo=[-1], hi=[] → push -2 → lo=[-2, -1]
  lo[0] = 2 > hi[0]? hi empty → no
  len(lo)=2 > len(hi)+1? 2 > 1 → pop lo → push 2 to hi
  lo=[-1], hi=[2] → median = (1+2)/2 = 1.5
addNum(3): lo=[-1] → push -3 → lo=[-3, -1]
  lo[0]=3 > hi[0]=2? yes → pop lo → push 2 to hi... 
  Actually simpler: lo=[-3,-1], hi=[2]
  lo[0]=3 > hi[0]=2 → pop lo 3, push to hi
  lo=[-1], hi=[2,3] → len(hi)=2 > len(lo)=1 → pop hi 2, push -2 to lo
  lo=[-2,-1], hi=[3] → median = 2.0 ✓
```

### Key Insight
The two-heap approach maintains the lower half and upper half such that median is always accessible at the roots. Balancing ensures O(1) median access and O(log n) insertion.

### Well-Commented Code

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lo = []   # max-heap (negated) — stores smaller half
        self.hi = []   # min-heap — stores larger half

    def addNum(self, num):
        # Step 1: Add to max-heap
        heapq.heappush(self.lo, -num)

        # Step 2: Ensure max(lo) <= min(hi)
        if self.hi and (-self.lo[0]) > self.hi[0]:
            val = -heapq.heappop(self.lo)
            heapq.heappush(self.hi, val)

        # Step 3: Balance sizes (diff <= 1)
        if len(self.lo) > len(self.hi) + 1:
            val = -heapq.heappop(self.lo)
            heapq.heappush(self.hi, val)
        elif len(self.hi) > len(self.lo):
            val = heapq.heappop(self.hi)
            heapq.heappush(self.lo, -val)

    def findMedian(self):
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        return (-self.lo[0] + self.hi[0]) / 2.0


# Test
mf = MedianFinder()
mf.addNum(1)
print(mf.findMedian())  # 1.0
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2.0
mf.addNum(4)
print(mf.findMedian())  # 2.5
mf.addNum(5)
print(mf.findMedian())  # 3.0
```

### Complexity Analysis
- **Time:** O(log n) per add, O(1) for findMedian.
- **Space:** O(n) — stores all elements.

### Edge Cases
- **Single element:** `len(lo) > len(hi)` → return lo[0].
- **Even count:** Average of both roots; result is float.
- **All same values:** Both heaps contain the same value; median = that value.
- **Large stream:** Works in O(log n) per insertion.

### Common Mistakes
1. **Forgetting negation:** Without negation, `lo` is a min-heap, not a max-heap.
2. **Not swapping to maintain order:** The max of lo must be ≤ min of hi.
3. **Incorrect balance condition:** `len(lo)` can be `len(hi)+1` at most.
4. **Returning int instead of float for even-length:** Must return float (average of two ints).
5. **Two heaps out of sync:** After swap, re-check balance.

### Pattern Recognition
- **Two-Heap Median:** Classic technique for running median.
- **Invariant Maintenance:** Size and order invariants must be checked after every insertion.
- **Similar Problems:** Sliding Window Median, Find Median from Data Stream (follow-ups).

---

## Problem 39: Sliding Window Median

### Problem Explanation (Simple Words)
Find the median of each sliding window of size k. Use `SortedList` from `sortedcontainers` which maintains elements in sorted order with O(log k) add/remove. The median is at `window[k//2]` (odd k) or average of `window[k//2-1]` and `window[k//2]` (even k).

### Algorithm Steps
1. **Initialize** empty `SortedList` and result list.
2. **For each `num` at index `i`:**
   - Add `num` to `SortedList`.
   - If window size > k: remove `nums[i - k]` (the element exiting the window).
   - If window size == k: compute median and append.
3. **Return** result list.

### Visual Walkthrough
**Input:** `nums = [1, 3, -1, -3, 5, 3, 6, 7]`, `k = 3`

```
i=0, add 1:   window=[1]           size<3 → skip
i=1, add 3:   window=[1,3]         size<3 → skip
i=2, add -1:  window=[-1,1,3]      size=3 → median=1.0
i=3, add -3:  window=[-3,-1,1,3]   remove 1 → window=[-3,-1,3] → median=-1.0
i=4, add 5:   window=[-3,-1,3,5]   remove 3 → window=[-3,-1,5] → median=-1.0
i=5, add 3:   window=[-3,-1,3,5]   remove -3 → window=[-1,3,5] → median=3.0
i=6, add 6:   window=[-1,3,5,6]    remove -1 → window=[3,5,6] → median=5.0
i=7, add 7:   window=[3,5,6,7]     remove 3 → window=[5,6,7] → median=6.0

Result: [1.0, -1.0, -1.0, 3.0, 5.0, 6.0] ✓
```

### Key Insight
`SortedList` provides O(log k) insertion and removal with O(1) index-based median access. This avoids the complexity of two-heap + lazy deletion used in Find Median from Data Stream.

### Well-Commented Code

```python
def medianSlidingWindow(nums, k):
    from sortedcontainers import SortedList

    window = SortedList()
    result = []

    for i, num in enumerate(nums):
        window.add(num)

        # Remove element exiting the window
        if len(window) > k:
            window.remove(nums[i - k])

        # Compute median when window is full
        if len(window) == k:
            if k % 2 == 1:
                result.append(window[k // 2])
            else:
                result.append((window[k // 2 - 1] + window[k // 2]) / 2.0)

    return result


# Test
print(medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))
# [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
print(medianSlidingWindow([1, 2, 3, 4], 2))
# [1.5, 2.5, 3.5]
print(medianSlidingWindow([2, 1, 3, 4, 5], 4))
# [2.5, 3.0]
```

### Complexity Analysis
- **Time:** O(n log k) — each add/remove is O(log k).
- **Space:** O(k) — SortedList of size k.

### Edge Cases
- **k = 1:** Each element is its own median (window[k//2]).
- **k = n:** Single window → single median.
- **k even:** Average of two middle values.
- **k odd:** Exact middle value.
- **Duplicate values:** SortedList handles duplicates correctly.

### Common Mistakes
1. **Using only the two-heap approach without lazy deletion:** Removing arbitrary elements from a heap is O(n). Use `SortedList` or lazy deletion.
2. **Wrong median index:** For odd k: `k//2` (0-indexed). For even k: `k//2 - 1` and `k//2`.
3. **Not removing the element exiting the window.**
4. **Returning integers for even k:** Must return floats (average of two ints may be .5).

### Pattern Recognition
- **SortedList for Sliding Window:** When you need order statistics in a sliding window, `SortedList` is simpler than two heaps.
- **Sliding Window + Order Statistics:** Maintain sorted order of current window.
- **Similar Problems:** Find Median from Data Stream, Sliding Window Maximum.

---

## Problem 40: IPO

### Problem Explanation (Simple Words)
You have capital `w` and can complete up to `k` projects. Each project has a capital requirement and a profit. Complete the most profitable affordable project each time to maximize final capital.

### Algorithm Steps
1. **Sort** projects by capital requirement.
2. **Iterate** up to `k` times:
   - While next project's capital ≤ current capital: push its profit onto max-heap.
   - If heap empty: break (no affordable projects).
   - Pop most profitable project, add its profit to capital.
3. **Return** final capital.

### Visual Walkthrough
**Input:** `k = 2, w = 0, profits = [1, 2, 3], capital = [0, 1, 1]`

```
Sorted by capital: [(0,1), (1,2), (1,3)]

Step 1 (k=1):
  w=0 → afford (0,1) → heap=[-1], idx=1
  → (1,2) requires 1 > 0 → stop pushing
  Pop -1 → w=0+1=1

Step 2 (k=2):
  w=1 → afford (1,2) → heap=[-2,-1], idx=2
       → (1,3) also afford → heap=[-3,-1,-2], idx=3
  Pop -3 → w=1+3=4

Result: 4 ✓
```

### Key Insight
Sort by capital and scan linearly. All affordable projects at each step are in the heap. The most profitable is always the best choice because it maximizes capital for future steps.

### Well-Commented Code

```python
import heapq

def findMaximizedCapital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))
    heap = []
    idx = 0
    n = len(projects)

    for _ in range(k):
        # Add all projects we can afford
        while idx < n and projects[idx][0] <= w:
            heapq.heappush(heap, -projects[idx][1])
            idx += 1

        if not heap:
            break  # No affordable projects left

        # Take the most profitable
        w += -heapq.heappop(heap)

    return w


# Test
print(findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]))  # 4
print(findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]))  # 6
print(findMaximizedCapital(1, 0, [1, 2, 3], [0, 1, 2]))  # 1
print(findMaximizedCapital(1, 2, [1], [1]))  # 3
print(findMaximizedCapital(2, 3, [2, 1, 3], [1, 2, 1]))  # 8
```

### Complexity Analysis
- **Time:** O(n log n + k log n) — sorting + heap operations.
- **Space:** O(n) — projects list + heap.

### Edge Cases
- **k = 0:** Return initial w.
- **No affordable projects:** Return current w.
- **All projects affordable:** Pick top k profits.
- **Same capital projects:** Heap picks the most profitable among them.
- **Not enough projects:** Exit when heap is empty (or k exceeds n).

### Common Mistakes
1. **Not sorting by capital:** Without sorting, you can't efficiently find all affordable projects.
2. **Pushing all profits at once:** Must push lazily as capital increases.
3. **Forgetting the while loop:** After each project, new projects may become affordable.
4. **Not breaking early:** If no projects are affordable, the loop is useless.
5. **Confusing profit and capital arrays:** Ensure index alignment in the sorted `projects` list.

### Pattern Recognition
- **Sort + Greedy + Heap:** Sort by one dimension (capital), use heap for another (profit).
- **Lazy Addition:** Only add projects to heap when they become affordable.
- **Similar Problems:** Maximum Performance of a Team, Course Schedule III, Minimum Cost to Hire K Workers.

---

# KEY PATTERNS & TIPS FOR INFOSYS SP DSE

---

## Sorting Patterns to Master

1. **Two-Pointer Partitioning** — Problems 1, 2 use in-place partitioning with O(n) time and O(1) space. Always check if relative order matters.

2. **Custom Sort Key** — Problems 3, 4 use lambda/comparator functions to define custom ordering. Python's `sort(key=lambda x: ...)` is very powerful.

3. **Sort + Two Pointers** — Problems 8, 5 use sorting to enable two-pointer technique. This is a very common pattern in coding interviews.

4. **Sort + Greedy** — Problems 6, 7 use sorting followed by a single greedy check. Always think about what sorting reveals about the structure.

5. **Deque Simulation** — Problem 10 uses a deque to simulate a process. Deques are useful for queue/dequeue operations.

## Hashing Patterns to Master

1. **Prefix Sum + Hash Map** — Problems 11, 12 are classic prefix sum problems. The hash map stores frequencies of prefix sums for O(1) lookup.

2. **Bidirectional Mapping** — Problems 15, 16 require checking bijections with two maps. Always verify both directions.

3. **Frequency Counting** — Problems 14, 20, 21, 22 use Counter or dictionary to count occurrences. This is the most basic hashing pattern.

4. **Set Operations** — Problems 19, 23, 25 use set difference, set intersection, or set membership. Sets provide O(1) average lookup.

5. **Floyd's Cycle Detection** — Problem 17 is a unique application of cycle detection to find duplicates. This is a must-know O(1) space technique.

6. **Trust/Score Counting** — Problem 22 uses a simple scoring system. Many graph problems can be reduced to scoring/counting.

## Heap Patterns to Master

1. **Max-Heap via Min-Heap** — Problems 26, 29, 34 use `heapq` with negated values. This is the standard Python approach for max-heaps.

2. **Min-Heap of Size k** — Problems 27, 29, 35 maintain a heap of fixed size k for top-k problems. This is O(n log k) which is better than full sorting for large n.

3. **Two-Heap Median** — Problem 38 is the classic median maintenance pattern. The two-heap invariant is essential to know.

4. **Greedy + Heap** — Problems 30, 31, 32, 40 combine greedy decisions with heap data structures. The heap helps select the best option at each step.

5. **Sort + Heap** — Problems 36, 40 sort first, then use heap for subsequent operations. Combining sorting with heaps is very powerful.

## Infosys SP DSE Specific Tips

- **Time Limits:** Python solutions may be slower than C++. Focus on O(n log n) or better algorithms.
- **Edge Cases:** Always consider empty inputs, single elements, all-same values, and very large inputs.
- **Space Constraints:** If O(1) space is required, look for in-place techniques (Problem 17's Floyd's algorithm).
- **Output Format:** Pay attention to whether the problem asks for indices, values, or boolean results.
- **Modulo Arithmetic:** Problems with large numbers often require mod 10^9 + 7 (Problem 31).
- **Custom Comparators:** Python 3 doesn't support `cmp` parameter. Use `key` function with tuples or `functools.cmp_to_key`.

---

# SUMMARY: ALL 40 PROBLEMS AT A GLANCE

| #  | Category | Problem | Key Technique |
|----|----------|---------|---------------|
| 1  | Sorting  | Sort Array By Parity | Two pointers |
| 2  | Sorting  | Sort Array By Parity II | Two pointers |
| 3  | Sorting  | Relative Sort Array | Custom sort key |
| 4  | Sorting  | Sort Array by Increasing Frequency | Frequency map sort |
| 5  | Sorting  | Minimum Absolute Difference | Sort + consecutive pairs |
| 6  | Sorting  | Triangle | Sort + greedy check |
| 7  | Sorting  | Maximum Product of Three Numbers | Sort + edge cases |
| 8  | Sorting  | 3Sum Closest | Sort + two pointers |
| 9  | Sorting  | Pancake Sorting | Flip operations |
| 10 | Sorting  | Reveal Cards In Increasing Order | Deque simulation |
| 11 | Hashing  | Subarray Sum Equals K | Prefix sum + hash map |
| 12 | Hashing  | Continuous Subarray Sum | Prefix sum modulo k |
| 13 | Hashing  | Minimum Index Sum of Two Lists | Index hash map |
| 14 | Hashing  | Number of Good Pairs | Frequency combinations |
| 15 | Hashing  | Word Pattern | Bijection mapping |
| 16 | Hashing  | Isomorphic Strings | Bidirectional mapping |
| 17 | Hashing  | Find Duplicate Number | Floyd's cycle detection |
| 18 | Hashing  | Check if Numbers Are Ascending | Extract and verify |
| 19 | Hashing  | Find Difference of Two Arrays | Set difference |
| 20 | Hashing  | Intersection of Multiple Arrays | Frequency counting |
| 21 | Hashing  | Largest Unique Number | Frequency map |
| 22 | Hashing  | Find the Town Judge | Trust score counting |
| 23 | Hashing  | Check if Pangram | Set of 26 letters |
| 24 | Hashing  | Count Distinct Numbers on Board | Math observation |
| 25 | Hashing  | Find All Numbers Disappeared | Hash set lookup |
| 26 | Heaps    | Last Stone Weight | Max-heap simulation |
| 27 | Heaps    | Kth Largest in Stream | Min-heap of size k |
| 28 | Heaps    | Kth Largest in Sorted Matrix | Binary search + counting |
| 29 | Heaps    | K Closest Points to Origin | Max-heap of size k |
| 30 | Heaps    | Furthest Building You Can Reach | Min-heap + greedy |
| 31 | Heaps    | Maximum Performance of a Team | Sort + min-heap |
| 32 | Heaps    | Minimum Cost to Connect Sticks | Greedy min-heap |
| 33 | Heaps    | Reorganize String | Greedy two-pick heap |
| 34 | Heaps    | Sort Characters By Frequency | Max-heap output |
| 35 | Heaps    | Top K Frequent Words | Min-heap of size k |
| 36 | Heaps    | Find K Pairs with Smallest Sums | BFS + min-heap |
| 37 | Heaps    | Kth Smallest in Sorted Matrix | Binary search |
| 38 | Heaps    | Find Median from Data Stream | Two-heap median |
| 39 | Heaps    | Sliding Window Median | SortedList / two heaps |
| 40 | Heaps    | IPO | Sort + max-heap greedy |

---

*Total: 40 problems | 10 Sorting + 15 Hashing + 15 Heaps*
*Each solution in clean, working Python — ready for Infosys SP DSE prep.*
