# Backtracking Template

Backtracking is a systematic way to explore all possible configurations of a problem by incrementally building candidates and abandoning them ("backtracking") as soon as we determine they cannot lead to a valid solution.

## The Core Template: Choose - Explore - Unchoose

Every backtracking algorithm follows this three-step pattern:

```
void backtrack(candidate, result) {
    if (isLeaf(candidate)) {
        result.add(new candidate); // or process solution
        return;
    }
    for (nextChoice : choices) {
        makeChoice(nextChoice);
        backtrack(nextCandidate, result);
        unmakeChoice(nextChoice);
    }
}
```

Let's break down each part:

1. **Choose**: Make a decision — pick an element, assign a value, make a move
2. **Explore**: Recursively explore all possibilities from this choice
3. **Unchoose**: Undo the choice to try the next option (backtrack)

## Decision Tree Visualization

For generating subsets of [1,2,3]:

```
                 root
                /    \
           include 1   exclude 1
           /      \    /        \
       inc 2  exc 2  inc 2   exc 2
       /  \   /  \   /  \    /  \
     inc3...  ...  ...  ... ...  ...
```

Each leaf is a complete subset. Each internal node represents a decision point.

## Generic Template in Java

```java
public class BacktrackingTemplate {
    public List<List<Integer>> solve(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        List<Integer> candidate = new ArrayList<>();
        backtrack(nums, 0, candidate, result);
        return result;
    }

    private void backtrack(int[] nums, int start,
                           List<Integer> candidate,
                           List<List<Integer>> result) {
        // Leaf node: process current candidate
        // Not all problems collect at leaves — sometimes at every node
        result.add(new ArrayList<>(candidate));

        // Explore choices
        for (int i = start; i < nums.length; i++) {
            // MAKE CHOICE
            candidate.add(nums[i]);

            // EXPLORE — pass i+1 to avoid reusing same element
            backtrack(nums, i + 1, candidate, result);

            // UNMAKE CHOICE (backtrack)
            candidate.remove(candidate.size() - 1);
        }
    }
}
```

## Key Variants

### 1. Pass by copy vs pass by reference + undo

```java
// Pass by copy (creates new list each time — more memory but simpler)
void backtrack(int[] nums, int i, List<Integer> candidate, List<List<Integer>> result) {
    if (i == nums.length) {
        result.add(candidate);
        return;
    }
    // Include
    List<Integer> include = new ArrayList<>(candidate);
    include.add(nums[i]);
    backtrack(nums, i + 1, include, result);
    // Exclude
    backtrack(nums, i + 1, candidate, result);
}

// Pass by reference + undo (saves memory, more efficient)
void backtrack(int[] nums, int i, List<Integer> candidate, List<List<Integer>> result) {
    if (i == nums.length) {
        result.add(new ArrayList<>(candidate)); // MUST copy here
        return;
    }
    // Include
    candidate.add(nums[i]);
    backtrack(nums, i + 1, candidate, result);
    candidate.remove(candidate.size() - 1); // undo
    // Exclude
    backtrack(nums, i + 1, candidate, result);
}
```

### 2. Leaf collection vs every node collection

```java
// Collect at every node (subsets — every prefix is a subset)
void backtrack(...) {
    result.add(new ArrayList<>(candidate)); // every call adds
    for (choices) { ... }
}

// Collect only at leaves (combinations of exact size K)
void backtrack(...) {
    if (candidate.size() == K) {
        result.add(new ArrayList<>(candidate)); // only at leaf
        return;
    }
    for (choices) { ... }
}
```

## Optimization Techniques

### 1. Pruning (Branch and Bound)

Stop exploring when we know a branch cannot yield a solution.

```java
void backtrack(int[] nums, int start, int target, int sumSoFar, ...) {
    // Prune: if sum already exceeds target, stop
    if (sumSoFar > target) return;

    // Prune: if remaining elements can't reach target, stop
    if (sumSoFar + remainingSum(nums, start) < target) return;

    for (int i = start; i < nums.length; i++) {
        candidate.add(nums[i]);
        backtrack(nums, i, target, sumSoFar + nums[i], ...);
        candidate.remove(candidate.size() - 1);
    }
}
```

### 2. Ordering of Choices

```java
// Sort to enable pruning and duplicate handling
Arrays.sort(nums); // critical for duplicates and pruning

// Process larger elements first for faster pruning (in combination sum)
for (int i = start; i < nums.length; i++) {
    // Skip duplicates
    if (i > start && nums[i] == nums[i - 1]) continue;
    // ...
}
```

### 3. Early Termination

```java
boolean backtrack(...) {
    if (isSolution) return true; // stop early — found one solution
    for (choices) {
        if (backtrack(...)) return true; // propagate success
    }
    return false;
}
```

## Complexity Analysis

- **Time**: O(branches^depth) in worst case, often O(choices! * pathLength) for permutations
- **Space**: O(depth) for recursion stack + O(solutions) if storing all

## When to Use Backtracking

| Problem Characteristic | Use Backtracking |
|---|---|
| Need ALL solutions | ✅ Yes |
| Need ONE solution (any) | ✅ Yes (with early termination) |
| Need OPTIMAL solution | ❌ Use DP instead |
| Count number of solutions | ✅ Yes (with or without memo) |
| Overlapping subproblems | ⚠️ Add memoization → becomes DP |

## Common Pitfalls

1. **Forgetting to copy the candidate** when adding to result
2. **Not undoing a choice** (pass by reference without remove)
3. **Infinite recursion** — forgetting base case
4. **Off-by-one in start index** — reusing elements when we shouldn't
5. **Not handling duplicates** properly leads to duplicate solutions

## Real Interview Problems Using This Template

| Problem | Pattern |
|---|---|
| Subsets | Every node is a solution |
| Permutations | All orderings with used[] array |
| Combinations | Fixed size, start index |
| Combination Sum | Unlimited/limited usage with pruning |
| N-Queens | Constraint satisfaction, validation at each step |
| Sudoku Solver | Fill empty cells, validate row/col/box |
| Palindrome Partitioning | Partition at each index |
| Word Search | Grid traversal with visited marks |

Remember: BACKTRACKING = BRUTE FORCE + PRUNING. Without pruning, it's just trying everything. The art is in identifying which branches will never yield solutions and cutting them early.
