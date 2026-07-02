# Subsets With Duplicates

**Problem**: Given an array of integers that may contain duplicates, return all possible subsets (the power set) **without duplicates**.

**Example**: `nums = [1, 2, 2]` → `[[], [1], [1,2], [1,2,2], [2], [2,2]]`

Without handling duplicates, our algorithm would produce duplicate subsets: `[[], [1], [2], [1,2], [2], [1,2], [2,2], [1,2,2]]` — notice `[2]` and `[1,2]` each appear twice.

---

## Sorting is the First Step

For both recursive and iterative approaches, the first step is always:

```java
Arrays.sort(nums);
```

Sorting ensures duplicates are adjacent, making them easy to skip.

---

## Approach 1: Recursive Backtracking with Duplicate Skipping

The key insight: when processing duplicates, we should skip them if we're at a decision point where the previous same element was considered but NOT chosen.

```java
public List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    result.add(new ArrayList<>(current));

    for (int i = start; i < nums.length; i++) {
        // SKIP DUPLICATES: if same as previous and previous wasn't chosen
        if (i > start && nums[i] == nums[i - 1]) continue;

        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

### Why `i > start` Instead of `i > 0`?

This is the most common point of confusion. Let's understand with an example:

`nums = [1, 2, 2]`, sorted.

Without the skip condition, the recursion tree is:

```
                      []
              /       |        \
             /        |         \
           [1]       [2]       [2] ← duplicate!
          /   \       |          |
      [1,2] [1,2]  [2,2]     [2,2] ← more duplicates!
        |      |      |          |
    [1,2,2] [1,2,2] [2,2]    [2,2]
```

When we use `i > start`:

- At root (start=0): i=0 (1), i=1 (2), i=2 (2, skipped because i=2 > start=0 and nums[2]==nums[1])
- At node [1] (start=1): i=1 (2), i=2 (2, NOT skipped because i=2 > start=1? No, we check i > start — i=2 > start=1, yes, and nums[2]==nums[1], so we skip)

Wait — that doesn't work. Let me re-examine.

Actually, let me trace more carefully with `i > start`:

Root (start=0, current=[]):
- i=0: nums[0]=1 → add [1], recurse with start=1
  - i=1: nums[1]=2 → add [1,2], recurse with start=2
    - i=2: nums[2]=2, i=2 > start=2? No, i=2 is NOT > start=2. So we DON'T skip. Add [1,2,2].
  - i=2: nums[2]=2, i=2 > start=1? Yes. nums[2]==nums[1]? Yes. SKIP.
- i=1: nums[1]=2 → add [2], recurse with start=2
  - i=2: nums[2]=2, i=2 > start=2? No. Add [2,2].
- i=2: nums[2]=2, i=2 > start=0? Yes. nums[2]==nums[1]? Yes. SKIP.

Result: [[], [1], [1,2], [1,2,2], [2], [2,2]] ✓

### The Golden Rule

> **Skip a duplicate element if it is at the same decision level as the previous identical element, AND the previous identical element was NOT included.** In other words, only the first occurrence of a duplicate can start a new branch at any given level.

The condition `i > start` effectively says: "Skip this duplicate choice at this level because the first identical choice at this level already explored this branch."

---

## Approach 2: Iterative Cascading with Duplicate Handling

```java
public List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    result.add(new ArrayList<>());
    int prevCount = 0; // tracks how many subsets were added in previous iteration

    for (int i = 0; i < nums.length; i++) {
        int startIndex = 0;
        int size = result.size();

        // If duplicate, only extend subsets that were ADDED in the previous step
        if (i > 0 && nums[i] == nums[i - 1]) {
            startIndex = size - prevCount;
        }

        prevCount = 0;
        for (int j = startIndex; j < size; j++) {
            List<Integer> newSubset = new ArrayList<>(result.get(j));
            newSubset.add(nums[i]);
            result.add(newSubset);
            prevCount++;
        }
    }

    return result;
}
```

### Trace for [1, 2, 2]

```
Initial: [[]]

i=0 (num=1): not duplicate
  size=1, startIndex=0
  Copy [] → [1] (prevCount=1)
  Result: [[], [1]]

i=1 (num=2): not duplicate
  size=2, startIndex=0
  Copy [] → [2] (prevCount=1)
  Copy [1] → [1,2] (prevCount=2)
  Result: [[], [1], [2], [1,2]]

i=2 (num=2): DUPLICATE
  size=4, startIndex = 4 - 2 = 2
  Only extend [2] and [1,2] (the ones added in previous step)
  Copy [2] → [2,2] (prevCount=1)
  Copy [1,2] → [1,2,2] (prevCount=2)
  Result: [[], [1], [2], [1,2], [2,2], [1,2,2]]
```

**Why does this work?** When a duplicate value appears, we only extend subsets that were created in the previous step (which already contain the previous occurrence of the duplicate). This prevents creating redundant branches.

---

## Approach 3: Using a Set (Not Recommended)

```java
public List<List<Integer>> subsetsWithDup(int[] nums) {
    Arrays.sort(nums);
    Set<List<Integer>> set = new HashSet<>();
    int n = nums.length;
    int total = 1 << n;

    for (int mask = 0; mask < total; mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.add(nums[i]);
            }
        }
        set.add(subset);
    }

    return new ArrayList<>(set);
}
```

**Problem**: Inefficient. We generate all 2^n subsets including duplicates, and then deduplicate with a HashSet. The set comparison is O(n) per subset, making this O(n * 2^n) with potentially large constant factors.

---

## Visual Comparison of Approaches

For `nums = [1, 2, 2]`:

| Approach | Output Order | Efficiency |
|---|---|---|
| Recursive + skip | `[[], [1], [1,2], [1,2,2], [2], [2,2]]` | Best |
| Iterative + startIndex | `[[], [1], [2], [1,2], [2,2], [1,2,2]]` | Best |
| Set-based bitmask | Could be any order | Worst |

---

## Complexity Analysis

- **Time**: O(n * 2^n) — same as distinct subsets in worst case (when no duplicates)
- **Space**: O(n) for recursion + O(n * 2^n) for output

With heavy duplicates (e.g., all elements same), the number of unique subsets reduces to n+1 (subsets of size 0, 1, ..., n), and the algorithm runs much faster.

---

## Common Mistakes

### 1. Using `i > 0` instead of `i > start`

```java
// WRONG: skips valid subsets
if (i > 0 && nums[i] == nums[i - 1]) continue;

// CORRECT: only skip at same level
if (i > start && nums[i] == nums[i - 1]) continue;
```

With `i > 0`, `nums = [1, 2, 2]` would produce only `[[], [1], [1,2], [2]]` — missing `[1,2,2]` and `[2,2]`.

### 2. Forgetting to sort

```java
// WRONG: duplicates may not be adjacent
subsetsWithDup(new int[]{2, 1, 2}); // misses duplicates!

// CORRECT: sort first
Arrays.sort(nums);
subsetsWithDup(new int[]{1, 2, 2}); // handles all cases
```

### 3. Using Set without content-based equality

```java
// This actually works in Java because ArrayList implements equals()
// based on contents. But it's inefficient.
Set<List<Integer>> set = new HashSet<>();
```

---

## Key Takeaway

The `i > start && nums[i] == nums[i-1]` pattern is one of the most useful patterns in all of backtracking. It appears in:
- Subsets with duplicates
- Permutations with duplicates
- Combination Sum II
- Any backtracking problem where the input may contain duplicates

Learn it once, use it everywhere.
