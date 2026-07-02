# Combination Sum I, II, III

---

## Combination Sum I — Unlimited Usage

**Problem**: Given an array of distinct integers `candidates` and a target `target`, find all unique combinations where candidates sum to target. The same number may be used **unlimited times**.

**Example**: `candidates = [2, 3, 6, 7], target = 7` → `[[2,2,3], [7]]`

### Solution

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(candidates, target, 0, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int target, int start, int sumSoFar,
                       List<Integer> current, List<List<Integer>> result) {
    // Base case: found a valid combination
    if (sumSoFar == target) {
        result.add(new ArrayList<>(current));
        return;
    }

    // Pruning: sum exceeded
    if (sumSoFar > target) return;

    for (int i = start; i < candidates.length; i++) {
        // CHOOSE
        current.add(candidates[i]);

        // EXPLORE — pass i (NOT i+1) to allow unlimited reuse
        backtrack(candidates, target, i, sumSoFar + candidates[i], current, result);

        // UNCHOOSE
        current.remove(current.size() - 1);
    }
}
```

**Key difference from combinations**: We pass `i` instead of `i+1` to allow reusing the same element.

### Decision Tree for [2, 3, 6, 7], target=7

```
                    []
         /          |           |         \
        /           |           |          \
      [2]          [3]        [6]        [7] <= match
     / | \         / \         |
   [2][3][6]    [3][6]       [6]
   /  |   |      |   |
 [2] [3] [6]   [3] [6]
 |   |         |
[2] [3]      [3] sum=12
|   |         |
[2] [3]      prune
|   |
[2] [3]
|   |
[2] [3]
| 
[2] sum=10 prune
```

Wait — that tree would be infinite without pruning! Good thing we prune when sum exceeds target.

### Optimization: Sort + Early Break

```java
public List<List<Integer>> combinationSum(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(candidates); // sort for early break
    backtrack(candidates, target, 0, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int target, int start, int sumSoFar,
                       List<Integer> current, List<List<Integer>> result) {
    if (sumSoFar == target) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i < candidates.length; i++) {
        // EARLY BREAK: since array is sorted, further elements will also exceed
        if (sumSoFar + candidates[i] > target) break;

        current.add(candidates[i]);
        backtrack(candidates, target, i, sumSoFar + candidates[i], current, result);
        current.remove(current.size() - 1);
    }
}
```

**Why `break` instead of `continue`?** Because the array is sorted, if `candidates[i]` exceeds the remaining target, all later elements (which are larger) will also exceed. So we can break entirely.

### Complexity

- **Time**: O(N^(T/M + 1)) where N = number of candidates, T = target, M = minimum candidate
  - In worst case, we can use the smallest element T/M times → branching factor N at each level
  - Very loose bound, actual is much better with pruning
- **Space**: O(T/M) for recursion stack

---

## Combination Sum II — Each Element Once

**Problem**: Given an array of integers (may contain **duplicates**) and a target, find all unique combinations where each element is used **at most once**.

**Example**: `candidates = [10,1,2,7,6,1,5], target = 8`
→ `[[1,1,6], [1,2,5], [1,7], [2,6]]`

### Solution

```java
public List<List<Integer>> combinationSum2(int[] candidates, int target) {
    List<List<Integer>> result = new ArrayList<>();
    Arrays.sort(candidates); // sort to handle duplicates
    backtrack(candidates, target, 0, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] candidates, int target, int start, int sumSoFar,
                       List<Integer> current, List<List<Integer>> result) {
    if (sumSoFar == target) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i < candidates.length; i++) {
        // Pruning: sum would exceed target
        if (sumSoFar + candidates[i] > target) break;

        // SKIP DUPLICATES: at same level, skip if same as previous
        if (i > start && candidates[i] == candidates[i - 1]) continue;

        current.add(candidates[i]);

        // EXPLORE — pass i+1 since each element can only be used once
        backtrack(candidates, target, i + 1, sumSoFar + candidates[i], current, result);

        current.remove(current.size() - 1);
    }
}
```

### Key Differences from Combination Sum I

| Aspect | Combination Sum I | Combination Sum II |
|---|---|---|
| Element reuse | Unlimited | Once |
| Recursive call | `backtrack(..., i, ...)` | `backtrack(..., i + 1, ...)` |
| Duplicate handling | Input has no duplicates | Skip at same level |
| Sorting | Optional (for pruning) | Required (for dup handling) |

### Trace for [1, 1, 2, 5, 6, 7, 10], target=8

```
Sorted: [1, 1, 2, 5, 6, 7, 10]

start=0:
  Pick 1 (i=0): current=[1], sum=1
    start=1:
      Pick 1 (i=1): current=[1,1], sum=2
        start=2:
          Pick 2 (i=2): current=[1,1,2], sum=4
            start=3:
              Pick 5 (i=3): current=[1,1,2,5], sum=9 > 8 → break
          Skip 5 (break after 9>8)
          Pick 6 (i=4): sum=1+1+6=8 → MATCH [1,1,6]
      Skip 2 (i=2): current=[1,2], sum=3
        start=3:
          Pick 5 (i=3): current=[1,2,5], sum=8 → MATCH [1,2,5]
      Skip 5 (i=3): current=[1,5], sum=6
        start=4:
          Pick 6 (i=4): sum=12 > 8 → break
      Skip 6 (i=4): current=[1,6], sum=7
        start=5:
          Pick 7 (i=5): sum=14 > 8 → break
      Skip 7 (i=5): current=[1,7], sum=8 → MATCH [1,7]
  Skip 1 (i=1): DUPLICATE at same level → skip
  Pick 2 (i=2): current=[2], sum=2
    ...
```

### Duplicate Handling Deep Dive

The condition `if (i > start && candidates[i] == candidates[i-1]) continue` skips duplicate elements at the same recursion level. This ensures:

- **At the root (start=0)**: We try `candidates[0]=1` but skip `candidates[1]=1` because starting with either 1 produces the same results
- **At deeper levels**: We can still include the second 1 if the first 1 is already in our combination (like `[1,1,6]`)

This is the **exact same pattern** as subsets with duplicates!

---

## Combination Sum III — Fixed Size, 1-9

**Problem**: Find all combinations of `k` numbers from 1 to 9 that sum to `n`. Each number used at most once.

**Example**: `k = 3, n = 7` → `[[1,2,4]]`
**Example**: `k = 3, n = 9` → `[[1,2,6], [1,3,5], [2,3,4]]`

### Solution

```java
public List<List<Integer>> combinationSum3(int k, int n) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(k, n, 1, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int k, int target, int start, int sumSoFar,
                       List<Integer> current, List<List<Integer>> result) {
    // Pruning: exceeded size or sum
    if (current.size() == k) {
        if (sumSoFar == target) {
            result.add(new ArrayList<>(current));
        }
        return;
    }

    // Pruning: remaining slots vs available numbers
    int needed = k - current.size();

    for (int i = start; i <= 9; i++) {
        // Prune: sum would exceed target
        if (sumSoFar + i > target) break;

        // Prune: not enough remaining numbers to fill slots
        if (9 - i + 1 < needed) break;

        current.add(i);
        backtrack(k, target, i + 1, sumSoFar + i, current, result);
        current.remove(current.size() - 1);
    }
}
```

### With All Three Pruning Conditions

```java
private void backtrack(int k, int target, int start, int sumSoFar,
                       List<Integer> current, List<List<Integer>> result) {
    // Base: found valid combination
    if (current.size() == k && sumSoFar == target) {
        result.add(new ArrayList<>(current));
        return;
    }

    // Pruning 1: too many elements
    if (current.size() >= k) return;

    // Pruning 2: sum exceeded
    if (sumSoFar > target) return;

    int needed = k - current.size();

    for (int i = start; i <= 9; i++) {
        // Pruning 3: even the smallest element would exceed
        if (sumSoFar + i > target) break;

        // Pruning 4: not enough numbers left
        if (i + (needed - 1) > 9) break;

        // Pruning 5: max possible sum with remaining slots < target
        int maxPossible = sumSoFar + i;
        for (int j = 1; j < needed; j++) {
            maxPossible += (i + j);
        }
        if (maxPossible < target) continue;

        current.add(i);
        backtrack(k, target, i + 1, sumSoFar + i, current, result);
        current.remove(current.size() - 1);
    }
}
```

---

## Complexity Comparison

| Problem | Time Complexity | Space |
|---|---|---|
| Combination Sum I | O(N^(T/M + 1)) | O(T/M) |
| Combination Sum II | O(2^N) worst case | O(N) |
| Combination Sum III | O(C(9, k) * k) | O(k) |

---

## Interview Tips

### 1. When to use which?

- **Combination Sum I**: Input has distinct elements, unlimited usage → `i` not `i+1`
- **Combination Sum II**: Duplicates possible, each used once → sort + `i > start` skip + `i+1`
- **Combination Sum III**: Fixed range [1,9], fixed size k → aggressive pruning

### 2. Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| Using `i+1` in CS I | Misses combinations with reused elements | Use `i` instead |
| Not sorting in CS II | Can't detect duplicates | `Arrays.sort(candidates)` |
| Using `continue` instead of `break` | Misses pruning opportunity | `break` when sorted + exceeded |
| Not skipping duplicates | Duplicate solutions | `i > start && nums[i] == nums[i-1]` |

### 3. Optimization Order

For fastest performance:
1. **Sort input** (allows early break)
2. **Check sum before recursive call** (prune early)
3. **Check remaining capacity** (prune impossible branches)
4. **Process larger elements first** (reaches target faster, more pruning)

```java
// Alternative: process in reverse (largest first)
for (int i = candidates.length - 1; i >= start; i--) {
    if (sumSoFar + candidates[i] > target) continue; // doesn't help much
    // ... but if we use descending, break when sumSoFar + candidates[i] < target
    // and remaining elements are even smaller
}
```

### 4. The Three-Break Pattern for CS II

```java
for (int i = start; i < candidates.length; i++) {
    if (sumSoFar + candidates[i] > target) break;        // 1. Sum exceeded
    if (i > start && candidates[i] == candidates[i-1]) continue; // 2. Duplicate
    // 3. Check if remaining sum can possibly reach target
    // (only needed if negative numbers exist)
    current.add(candidates[i]);
    backtrack(candidates, target, i + 1, sumSoFar + candidates[i], current, result);
    current.remove(current.size() - 1);
}
```
