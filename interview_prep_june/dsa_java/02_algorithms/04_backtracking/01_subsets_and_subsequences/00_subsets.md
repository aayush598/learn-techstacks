# Subsets (Power Set)

**Problem**: Given an array of distinct integers, return all possible subsets (the power set).

**Example**: `nums = [1, 2, 3]` → `[[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]`

For an array of size n, there are exactly 2^n subsets — each element is either included or excluded.

---

## Approach 1: Recursive (Include/Exclude)

The most intuitive approach: for each element, decide to include it or exclude it.

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    generateSubsets(nums, 0, new ArrayList<>(), result);
    return result;
}

private void generateSubsets(int[] nums, int index,
                             List<Integer> current,
                             List<List<Integer>> result) {
    if (index == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }

    // EXCLUDE current element
    generateSubsets(nums, index + 1, current, result);

    // INCLUDE current element
    current.add(nums[index]);
    generateSubsets(nums, index + 1, current, result);

    // BACKTRACK: undo the inclusion for other branches
    current.remove(current.size() - 1);
}
```

**Note the pattern**: exclude first, then include, then undo. The order doesn't matter for correctness, but it affects the output order.

### Decision Tree for [1,2,3]

```
                             []
                            /  \
                           /    \
                          /      \
                         /        \
                        /          \
                       /            \
                      /              \
                    []               [1]
                   /  \             /    \
                  /    \           /      \
                []     [2]       [1]     [1,2]
               / \     / \       / \      /  \
             []  [3] [2] [2,3] [1] [1,3] [1,2] [1,2,3]
```

Each leaf represents a complete subset after processing all 3 elements.

---

## Approach 2: For-loop with Start Index (Cascading/Backtracking)

This is the standard backtracking template approach. At each step, we add choices in order, growing the current subset.

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
    // Add current subset — note: we add at EVERY node, not just leaves
    result.add(new ArrayList<>(current));

    // Try adding each remaining element
    for (int i = start; i < nums.length; i++) {
        // INCLUDE nums[i]
        current.add(nums[i]);

        // EXPLORE further (pass i+1 to not reuse same element)
        backtrack(nums, i + 1, current, result);

        // BACKTRACK / UNCHOOSE
        current.remove(current.size() - 1);
    }
}
```

**Key difference from include/exclude**: This approach uses a loop to try each element as the "next" element. The recursion tree has fewer levels because we don't branch for "exclude" — exclusion is implicit (we just skip elements by advancing start).

### Decision Tree for For-loop Approach

```
                    []
            /       |       \
           /        |        \
         [1]       [2]       [3]
        /   \       |
      [1,2] [1,3] [2,3]
      /
    [1,2,3]
```

This tree has 8 nodes = 8 subsets. Much more compact because we don't explicitly branch for exclusion.

---

## Approach 3: Iterative (Cascading)

Start with `[[]]`, and for each element, add copies of existing subsets with the new element appended.

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    result.add(new ArrayList<>()); // empty subset

    for (int num : nums) {
        int size = result.size();
        for (int i = 0; i < size; i++) {
            // Create a new subset = existing subset + current element
            List<Integer> newSubset = new ArrayList<>(result.get(i));
            newSubset.add(num);
            result.add(newSubset);
        }
    }

    return result;
}
```

### Trace for [1,2,3]

```
Initial: [[]]

After processing 1:
  Copy [] → add 1 → [1]
  Result: [[], [1]]

After processing 2:
  Copy [] → add 2 → [2]
  Copy [1] → add 2 → [1,2]
  Result: [[], [1], [2], [1,2]]

After processing 3:
  Copy [] → add 3 → [3]
  Copy [1] → add 3 → [1,3]
  Copy [2] → add 3 → [2,3]
  Copy [1,2] → add 3 → [1,2,3]
  Result: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

---

## Approach 4: Bitmask

Each subset corresponds to a binary number from 0 to 2^n - 1.

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    int n = nums.length;
    int total = 1 << n; // 2^n

    for (int mask = 0; mask < total; mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.add(nums[i]);
            }
        }
        result.add(subset);
    }

    return result;
}
```

### Bitmask Table for n=3

| Mask (binary) | Subset | Integer |
|---|---|---|
| 000 | [] | 0 |
| 001 | [3] | 1 |
| 010 | [2] | 2 |
| 011 | [2,3] | 3 |
| 100 | [1] | 4 |
| 101 | [1,3] | 5 |
| 110 | [1,2] | 6 |
| 111 | [1,2,3] | 7 |

**Note**: The order depends on which bit position corresponds to which index. In the code above, bit position `i` corresponds to `nums[i]`. The bitmask approach naturally generates subsets in lexicographic order of their binary representation.

---

## Complexity Analysis

| Approach | Time | Space (excluding output) | Notes |
|---|---|---|---|
| Include/Exclude | O(n * 2^n) | O(n) recursion depth | Simple but deep recursion |
| For-loop Backtracking | O(n * 2^n) | O(n) recursion depth | Standard template |
| Iterative Cascading | O(n * 2^n) | O(1) extra | No recursion, uses result list |
| Bitmask | O(n * 2^n) | O(1) extra | No recursion, simplest code |

**Why O(n * 2^n)?** There are 2^n subsets, and for each subset, we copy it to the result (O(n) per copy in worst case).

**Space**: The output itself is O(n * 2^n) since we store all subsets.

---

## Practical Insights for Interviews

### 1. Which approach to use?

- **For-loop backtracking**: Most versatile — extends naturally to permutations, combinations, and constraint problems
- **Include/Exclude**: Best for teaching the concept, but less practical for variants
- **Bitmask**: Best when N ≤ 20 and you need fast, iterative solution (used in DP with bitmask)
- **Cascading**: Clean iterative solution, easy to understand

### 2. Handling large inputs

If n > 20, generating all 2^n subsets becomes impractical. 2^20 ≈ 1 million, which is manageable. 2^30 ≈ 1 billion — too much.

### 3. Subset vs Subsequence vs Subarray

- **Subset**: Any selection of elements, order doesn't matter, can skip any. 2^n possibilities.
- **Subsequence**: Order preserved, can skip elements. 2^n possibilities (same count).
- **Subarray**: Contiguous, order preserved. n*(n+1)/2 possibilities.

For a set of distinct elements, subsets and subsequences are essentially the same (since the original array gives us a canonical order).

### 4. Modifying for related problems

- **Subsets with duplicates**: Sort + skip consecutive duplicates
- **Subsets of size K**: Only add when size == K (combinations)
- **Subsets with sum constraint**: Add pruning when sum exceeds target

### 5. Generating subsets in lexicographic order

```java
// Sort first, then use backtracking
Arrays.sort(nums);
// The for-loop approach naturally produces lexicographic order when array is sorted
```
