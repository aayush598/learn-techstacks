# Combinations — C(n,k)

**Problem**: Given two integers n and k, return all combinations of k numbers chosen from the range [1, n].

**Example**: `n = 4, k = 2` → `[[1,2], [1,3], [1,4], [2,3], [2,4], [3,4]]`

There are C(n,k) = n! / (k! * (n-k)!) combinations.

---

## Backtracking with Start Index

This is the classic "for-loop with start index" pattern. We maintain a `start` parameter to ensure we only pick elements that come after the last picked element (preventing permutations of the same combination).

```java
public List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(n, k, 1, new ArrayList<>(), result);
    return result;
}

private void backtrack(int n, int k, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    // Leaf node: we have k elements
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i <= n; i++) {
        current.add(i);
        backtrack(n, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

### Why `start = i + 1`?

Because combinations don't care about order. `[1, 2]` and `[2, 1]` are the same combination. By only picking elements that come AFTER the current one, we ensure each combination is generated exactly once.

### Decision Tree for C(4, 2)

```
                    []
         /          |           |         \
        /           |           |          \
      [1]          [2]         [3]        [4]
     / | \         / \          |
   [2][3][4]    [3][4]        [4]
```

Valid combinations: [1,2], [1,3], [1,4], [2,3], [2,4], [3,4]

Total nodes = C(4,1) + C(4,2) = 4 + 6 = 10, but actual recursive calls = 4 + 3 + 2 + 1 + 3 + 2 + 1 + 2 + 1 + 1 = more due to internal nodes.

---

## Optimization: Pruning

We can prune branches that don't have enough remaining elements to reach k.

```java
private void backtrack(int n, int k, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }

    // PRUNE: if remaining elements < needed elements, stop
    int needed = k - current.size();
    for (int i = start; i <= n - needed + 1; i++) {
        current.add(i);
        backtrack(n, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

**Why `n - needed + 1`?**
- We need `needed` more elements
- The largest we can start at is `n - needed + 1`
- Example: n=5, k=3, current.size()=1 → needed=2 → largest start = 5-2+1 = 4
  - If start=4, remaining are [4,5] → we can pick {4,5} → total {x,4,5} ✓
  - If start=5, remaining is [5] → only 1 left, not enough

### Pruning Effect

For C(5, 3) with current = [1]:
- Without pruning: tries i=2,3,4,5
- With pruning: needed=2, n-needed+1=4 → tries i=2,3,4 (skips 5 which would fail)

This eliminates many dead-end branches.

---

## Complexity Analysis

- **Time**: O(k * C(n,k)) — C(n,k) combinations, O(k) to copy each
- **Space**: O(k) for recursion + current list

### Growth of C(n,k)

| n | k | C(n,k) | Calls (with pruning) |
|---|---|---|---|
| 10 | 5 | 252 | Manageable |
| 20 | 10 | 184,756 | Moderate |
| 30 | 15 | 155M | Too large |
| 50 | 25 | 1.26 × 10¹⁴ | Impossible |

---

## Iterative Approach

```java
public List<List<Integer>> combine(int n, int k) {
    List<List<Integer>> result = new ArrayList<>();
    if (k <= 0 || k > n) return result;

    int[] indices = new int[k];
    for (int i = 0; i < k; i++) {
        indices[i] = i + 1;
    }

    while (true) {
        // Add current combination
        List<Integer> comb = new ArrayList<>();
        for (int idx : indices) comb.add(idx);
        result.add(comb);

        // Find rightmost position we can increment
        int pos = k - 1;
        while (pos >= 0 && indices[pos] == n - k + pos + 1) {
            pos--;
        }

        if (pos < 0) break; // no more combinations

        indices[pos]++;
        for (int i = pos + 1; i < k; i++) {
            indices[i] = indices[i - 1] + 1;
        }
    }

    return result;
}
```

### How the Iterative Approach Works

We maintain an array of k indices in increasing order. Each iteration:
1. Record the current combination
2. Find the rightmost index that hasn't reached its maximum value
3. Increment it
4. Reset all subsequent indices to be sequential

For C(5, 3):
```
[1,2,3] → [1,2,4] → [1,2,5] → [1,3,4] → [1,3,5] → [1,4,5] → [2,3,4] → ...
```

---

## Combinations from Array

When input is an array instead of range [1,n]:

```java
public List<List<Integer>> combineFromArray(int[] nums, int k) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, k, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int k, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

### With Duplicates in Array

```java
public List<List<Integer>> combineWithDuplicates(int[] nums, int k) {
    Arrays.sort(nums);
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, k, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int k, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i < nums.length; i++) {
        // Skip duplicates at same level
        if (i > start && nums[i] == nums[i - 1]) continue;

        current.add(nums[i]);
        backtrack(nums, k, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

---

## Variants

### All Combinations of All Sizes (Power Set)

If we don't have a fixed k, collect at every node:

```java
public List<List<Integer>> allCombinations(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    // Add EVERY node (not just leaves)
    result.add(new ArrayList<>(current));

    for (int i = start; i < nums.length; i++) {
        current.add(nums[i]);
        backtrack(nums, i + 1, current, result);
        current.remove(current.size() - 1);
    }
}
```

### Combinations with Repetition (Combinations of Multiset)

When elements can be reused:

```java
public List<List<Integer>> combineWithRepetition(int n, int k) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(n, k, 1, new ArrayList<>(), result);
    return result;
}

private void backtrack(int n, int k, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == k) {
        result.add(new ArrayList<>(current));
        return;
    }

    for (int i = start; i <= n; i++) {
        current.add(i);
        // i instead of i+1 — allows reuse
        backtrack(n, k, i, current, result);
        current.remove(current.size() - 1);
    }
}
```

### Combinations with Sum Constraint

Find all combinations of k numbers from 1-9 that sum to n:

```java
public List<List<Integer>> combinationSum3(int k, int n) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(k, n, 1, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int k, int target, int start, int sumSoFar,
                       List<Integer> current,
                       List<List<Integer>> result) {
    if (current.size() == k) {
        if (sumSoFar == target) {
            result.add(new ArrayList<>(current));
        }
        return;
    }

    // Pruning: remaining elements needed vs available
    int needed = k - current.size();
    for (int i = start; i <= 9; i++) {
        if (sumSoFar + i > target) break; // sum already exceeded
        if (9 - i + 1 < needed) break; // not enough remaining numbers

        current.add(i);
        backtrack(k, target, i + 1, sumSoFar + i, current, result);
        current.remove(current.size() - 1);
    }
}
```

---

## Combinations vs Permutations — Key Differences

| Aspect | Combinations | Permutations |
|---|---|---|
| Order matters? | No | Yes |
| Count | C(n,k) = n!/(k!(n-k)!) | P(n,k) = n!/(n-k)! |
| Start index | Always `i + 1` (ascending) | Always `0` (any position) |
| Used array? | No (start index is enough) | Yes (or swap) |
| Duplicate skip | `i > start && nums[i]==nums[i-1]` | `i > 0 && nums[i]==nums[i-1] && !used[i-1]` |

## Key Takeaways

1. **For-loop + start index** is the standard pattern for combinations
2. **Prune aggressively** — `remaining >= needed` reduces branches significantly
3. **C(n, k) is symmetric** — C(n, k) = C(n, n-k). If k > n/2, it might be faster to generate C(n, n-k) complements
4. **The iterative approach** uses less memory but is harder to modify for constraints
5. **Combinations with sum constraint** always benefit from pruning
