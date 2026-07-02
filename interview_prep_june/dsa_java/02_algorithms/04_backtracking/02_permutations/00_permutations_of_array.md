# Permutations of an Array

**Problem**: Given an array of distinct integers, return all possible permutations.

**Example**: `nums = [1, 2, 3]` → `[[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]`

For n distinct elements, there are n! permutations.

---

## Approach 1: Used-Array Approach (Most Intuitive)

Maintain a `boolean[] used` array to track which elements we've already placed in the current permutation.

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;

        // CHOOSE
        used[i] = true;
        current.add(nums[i]);

        // EXPLORE
        backtrack(nums, used, current, result);

        // UNCHOOSE
        used[i] = false;
        current.remove(current.size() - 1);
    }
}
```

### Decision Tree for [1, 2, 3]

```
                []
         /       |       \
        /        |        \
      [1]       [2]       [3]
     /   \     /   \     /   \
  [1,2] [1,3] [2,1] [2,3] [3,1] [3,2]
    |     |     |     |     |     |
 [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]
```

Each leaf has all 3 elements — exactly n! leaves.

### Complexity

- **Time**: O(n * n!) — n! permutations, O(n) to copy each
- **Space**: O(n) recursion + O(n) used array + O(n) current list

---

## Approach 2: Swap-Based Approach (No Extra Space)

Instead of a used array, swap elements in the original array to generate permutations. This is more memory efficient.

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    permute(nums, 0, result);
    return result;
}

private void permute(int[] nums, int start, List<List<Integer>> result) {
    if (start == nums.length - 1) {
        List<Integer> permutation = new ArrayList<>();
        for (int num : nums) permutation.add(num);
        result.add(permutation);
        return;
    }

    for (int i = start; i < nums.length; i++) {
        // CHOOSE: swap
        swap(nums, start, i);

        // EXPLORE: generate permutations for remaining positions
        permute(nums, start + 1, result);

        // UNCHOOSE: swap back
        swap(nums, start, i);
    }
}

private void swap(int[] nums, int i, int j) {
    int temp = nums[i];
    nums[i] = nums[j];
    nums[j] = temp;
}
```

### How Swap-Based Works

The idea: fix the element at position `start` by swapping, then recursively permute the remaining positions.

```
Initial: [1, 2, 3]

start=0:
  i=0: swap(0,0) → [1,2,3] → start=1
  i=1: swap(0,1) → [2,1,3] → start=1
  i=2: swap(0,2) → [3,2,1] → start=1

start=1 (from [1,2,3]):
  i=1: swap(1,1) → [1,2,3] → start=2 → add [1,2,3]
  i=2: swap(1,2) → [1,3,2] → start=2 → add [1,3,2]

start=1 (from [2,1,3]):
  i=1: swap(1,1) → [2,1,3] → start=2 → add [2,1,3]
  i=2: swap(1,2) → [2,3,1] → start=2 → add [2,3,1]

start=1 (from [3,2,1]):
  i=1: swap(1,1) → [3,2,1] → start=2 → add [3,2,1]
  i=2: swap(1,2) → [3,1,2] → start=2 → add [3,1,2]
```

### Comparison: Used-Array vs Swap-Based

| Aspect | Used-Array | Swap-Based |
|---|---|---|
| Extra space | O(n) used array | O(1) extra |
| Duplicate handling | Easy (skip if used[i] || skipDup) | Need sorting + skipping logic |
| Preserves original array | Yes (doesn't modify) | Modifies (but restores) |
| Intuitiveness | More intuitive | Less intuitive but elegant |
| Duplicates handling | `if (i > 0 && nums[i] == nums[i-1] && !used[i-1]) continue` | Must be more careful |

---

## Approach 3: Iterative (Building Permutations)

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    result.add(new ArrayList<>());

    for (int num : nums) {
        List<List<Integer>> newResult = new ArrayList<>();

        for (List<Integer> perm : result) {
            for (int i = 0; i <= perm.size(); i++) {
                List<Integer> newPerm = new ArrayList<>(perm);
                newPerm.add(i, num);
                newResult.add(newPerm);
            }
        }

        result = newResult;
    }

    return result;
}
```

### Trace for [1, 2, 3]

```
Start: [[]]

Insert 1 at all positions:
  [] → insert at pos 0 → [1]
  Result: [[1]]

Insert 2 at all positions:
  [1] → insert at pos 0 → [2,1]
  [1] → insert at pos 1 → [1,2]
  Result: [[2,1], [1,2]]

Insert 3 at all positions:
  [2,1] → insert at 0 → [3,2,1]
  [2,1] → insert at 1 → [2,3,1]
  [2,1] → insert at 2 → [2,1,3]
  [1,2] → insert at 0 → [3,1,2]
  [1,2] → insert at 1 → [1,3,2]
  [1,2] → insert at 2 → [1,2,3]
  Result: [[3,2,1], [2,3,1], [2,1,3], [3,1,2], [1,3,2], [1,2,3]]
```

---

## Permutations with Duplicates

When the input array contains duplicates, we need to avoid generating duplicate permutations.

### Used-Array Approach

```java
public List<List<Integer>> permuteUnique(int[] nums) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    boolean[] used = new boolean[nums.length];
    backtrack(nums, used, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, boolean[] used,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;

        // KEY: Skip duplicates — if same value as previous and previous not used
        if (i > 0 && nums[i] == nums[i - 1] && !used[i - 1]) continue;

        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current, result);
        used[i] = false;
        current.remove(current.size() - 1);
    }
}
```

### Why `!used[i-1]`?

The condition `!used[i-1]` ensures we only skip duplicates when the previous identical element was NOT used in the current branch. This means:

- If `used[i-1]` is `true` (previous element is in the current permutation), we allow `nums[i]` because they occupy different positions
- If `used[i-1]` is `false` (previous element was skipped), we skip `nums[i]` because starting a branch with this duplicate would duplicate a branch already explored

### Alternative: Use `used[i-1]` Instead

Some implementations use `used[i-1]` (without `!`):

```java
if (i > 0 && nums[i] == nums[i - 1] && used[i - 1]) continue;
```

Both work, but they prune at different points:
- `!used[i-1]`: Prunes BEFORE generating duplicate branches (more pruning earlier)
- `used[i-1]`: Prunes AFTER generating (more conservative, still correct)

The `!used[i-1]` version is more efficient because it prunes more aggressively.

---

## Complexity Analysis

| Approach | Time | Space | Best For |
|---|---|---|---|
| Used-array | O(n * n!) | O(n) | Easy to write, handles duplicates well |
| Swap-based | O(n * n!) | O(1) extra | Memory efficient, elegant |
| Iterative | O(n * n!) | O(n * n!) | Building iteratively, no recursion |

All approaches are O(n * n!) because:
- n! permutations
- For each permutation, O(n) to copy/build

---

## Practical Interview Tips

### 1. Which approach to use?

- **Used-array** for permutations of array (most common in interviews)
- **Swap-based** for string permutations (avoids extra space)
- **Iterative** when asked for next permutation / kth permutation

### 2. Modifying for permutations of subsets

If you only need permutations of size K (k-permutations):

```java
// Change base case
if (current.size() == K) {  // instead of nums.length
    result.add(new ArrayList<>(current));
    return;
}
```

This gives P(n,k) = n!/(n-k)! permutations.

### 3. Early termination for "find first" permutations

```java
boolean backtrack(...) {
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return true; // found one, stop
    }
    for (...) {
        if (backtrack(...)) return true;
    }
    return false;
}
```

### 4. Counting permutations with constraints

To count permutations with some constraint (e.g., adjacent difference > K), add a validation step:

```java
private void backtrack(int[] nums, boolean[] used, List<Integer> current) {
    if (current.size() == nums.length) {
        count++;
        return;
    }
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;
        // Prune: check constraint
        if (!current.isEmpty() && Math.abs(current.get(current.size()-1) - nums[i]) <= K) {
            continue;
        }
        used[i] = true;
        current.add(nums[i]);
        backtrack(nums, used, current);
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```
