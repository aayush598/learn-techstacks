# Combination Sum Variants

---

## Combination Sum IV — Actually DP (Permutation Sum)

**Problem**: Given an array of distinct integers and a target, find the **number of possible combinations** that sum to target. Order matters (this is actually counting permutations).

**Example**: `nums = [1, 2, 3], target = 4`
- All possible combinations where order matters: 
  (1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (1,3), (3,1), (2,2)
- Output: 7

### Why This Is Not Backtracking

A naive backtracking solution would work but time out for larger targets:

```java
// This works but is too slow for target > 30
public int combinationSum4(int[] nums, int target) {
    return backtrack(nums, target, 0);
}

private int backtrack(int[] nums, int remaining, int count) {
    if (remaining == 0) return 1;
    if (remaining < 0) return 0;

    int total = 0;
    for (int num : nums) {
        total += backtrack(nums, remaining - num, count);
    }
    return total;
}
```

**Problem**: Exponential time. For target = 35 and nums = [1, 2, 3], this would make billions of calls.

### DP Solution

This is actually a DP problem because it counts permutations with overlapping subproblems:

```java
public int combinationSum4(int[] nums, int target) {
    int[] dp = new int[target + 1];
    dp[0] = 1; // one way to make sum 0: choose nothing

    for (int amount = 1; amount <= target; amount++) {
        for (int num : nums) {
            if (amount >= num) {
                dp[amount] += dp[amount - num];
            }
        }
    }

    return dp[target];
}
```

**Key Insight**: `dp[amount]` = number of ways to sum to `amount` using any elements in any order. Since we iterate `amount` in the outer loop and `nums` in the inner loop, order matters — this counts permutations, not combinations.

### Why It's Called "Combination Sum IV"

The problem is misnamed. It should be "Permutation Sum" because:
- Combination Sum I: unlimited usage, order doesn't matter → combinations
- Combination Sum II: limited usage, order doesn't matter → combinations
- Combination Sum III: fixed size, order doesn't matter → combinations
- Combination Sum IV: unlimited usage, **order matters** → permutations

The confusion arises because the LeetCode problem statement says "The order of sequences does NOT matter" but the test cases actually count different orderings as different.

### Backtracking + Memoization (Alternative)

```java
public int combinationSum4(int[] nums, int target) {
    Integer[] memo = new Integer[target + 1];
    return backtrack(nums, target, memo);
}

private int backtrack(int[] nums, int remaining, Integer[] memo) {
    if (remaining == 0) return 1;
    if (remaining < 0) return 0;
    if (memo[remaining] != null) return memo[remaining];

    int total = 0;
    for (int num : nums) {
        total += backtrack(nums, remaining - num, memo);
    }

    memo[remaining] = total;
    return total;
}
```

This is essentially the top-down DP version.

---

## Factor Combinations

**Problem**: Given an integer n, return all possible combinations of factors (greater than 1) that multiply to n.

**Example**: `n = 12` → `[[2,6], [2,2,3], [3,4]]`

Note: `[2,6]` and `[6,2]` are the same — order doesn't matter.

### Solution

```java
public List<List<Integer>> getFactors(int n) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(n, 2, new ArrayList<>(), result);
    return result;
}

private void backtrack(int n, int start,
                       List<Integer> current,
                       List<List<Integer>> result) {
        // Base case: we have found a factorization
        if (current.size() > 0) {
            List<Integer> copy = new ArrayList<>(current);
            copy.add(n);
            result.add(copy);
        }

    for (int i = start; i * i <= n; i++) {
        if (n % i == 0) {
            // i is a factor — add it and recurse with n/i
            current.add(i);
            backtrack(n / i, i, current, result);
            current.remove(current.size() - 1);
        }
    }
}
```

### Trace for n=12

```
backtrack(12, 2, [])
├── i=2 (12%2==0)
│   ├── current=[2], call backtrack(6, 2, [2])
│   │   ├── i=2 (6%2==0)
│   │   │   ├── current=[2,2], call backtrack(3, 2, [2,2])
│   │   │   │   └── n not divisible, no loop
│   │   │   └── add [2,2,3] ← factor combination
│   │   └── i=3 (6%3==0) — but i*i=9 > 6, loop condition fails
│   └── add [2,6] ← factor combination
├── i=3 (12%3==0)
│   ├── current=[3], call backtrack(4, 3, [3])
│   │   └── i=3 (4%3!=0), no loop. i*i=9 > 4, loop ends
│   └── add [3,4] ← factor combination
└── i=4 (12%4==0) — but i*i=16 > 12, loop ends

Result: [[2,6], [2,2,3], [3,4]]
```

### Why `i * i <= n`?

This is a critical optimization. In factorization, if we check all factors up to √n, we ensure:
1. Each factor, when paired with n/i, gives the full factorization
2. Since we include the complementary factor in the base case (`current.add(n)`), we don't need to check i > √n

This also prevents duplicate work: `[2,6]` is found when i=2 (with complementary factor 6), and we won't also find `[6,2]` because we never start with i=6 > √12.

---

## Letter Combinations of a Phone Number

**Problem**: Given a string containing digits from 2-9, return all possible letter combinations that the number could represent.

**Example**: `"23"` → `["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]`

```
2 → abc
3 → def
4 → ghi
5 → jkl
6 → mno
7 → pqrs
8 → tuv
9 → wxyz
```

### Backtracking Solution

```java
public List<String> letterCombinations(String digits) {
    if (digits == null || digits.isEmpty()) return new ArrayList<>();

    String[] mapping = {
        "", "", "abc", "def", "ghi", "jkl",
        "mno", "pqrs", "tuv", "wxyz"
    };

    List<String> result = new ArrayList<>();
    backtrack(digits, mapping, 0, new StringBuilder(), result);
    return result;
}

private void backtrack(String digits, String[] mapping, int index,
                       StringBuilder current, List<String> result) {
    if (index == digits.length()) {
        result.add(current.toString());
        return;
    }

    String letters = mapping[digits.charAt(index) - '0'];

    for (char c : letters.toCharArray()) {
        current.append(c);
        backtrack(digits, mapping, index + 1, current, result);
        current.deleteCharAt(current.length() - 1);
    }
}
```

### Iterative (BFS) Approach

```java
public List<String> letterCombinations(String digits) {
    if (digits == null || digits.isEmpty()) return new ArrayList<>();

    String[] mapping = {
        "", "", "abc", "def", "ghi", "jkl",
        "mno", "pqrs", "tuv", "wxyz"
    };

    List<String> result = new ArrayList<>();
    result.add("");

    for (char digit : digits.toCharArray()) {
        String letters = mapping[digit - '0'];
        List<String> newResult = new ArrayList<>();

        for (String prefix : result) {
            for (char c : letters.toCharArray()) {
                newResult.add(prefix + c);
            }
        }

        result = newResult;
    }

    return result;
}
```

### Complexity

- **Time**: O(4^n) where n = number of digits (4 = max letters per digit)
  - For "23": 3 × 3 = 9 combinations
  - For "79": 4 × 4 = 16 combinations
  - For "2379": 3 × 3 × 4 × 4 = 144 combinations
- **Space**: O(n) for recursion + O(4^n) for output

### Variations

#### With Digit Press Count (Old Phones)

If we need to consider that pressing '2' once gives 'a', twice gives 'b', etc.:

```java
public List<String> letterCombinationsWithPauses(String digits) {
    // Each digit press is separate: "22" could be "aa" or "b"
    // This is actually the same as the standard problem
    // because each digit position is independent
    return letterCombinations(digits);
}
```

#### With Dictionary Filtering

If we only want valid words:

```java
public List<String> letterCombinations(String digits, Set<String> dictionary) {
    List<String> all = letterCombinations(digits);
    List<String> valid = new ArrayList<>();
    for (String word : all) {
        if (dictionary.contains(word)) {
            valid.add(word);
        }
    }
    return valid;
}
```

Or prune during backtracking:

```java
private void backtrack(String digits, String[] mapping, int index,
                       StringBuilder current, Set<String> dictionary,
                       List<String> result) {
    if (index == digits.length()) {
        String word = current.toString();
        if (dictionary.contains(word)) {
            result.add(word);
        }
        return;
    }
    // Prune: check if current prefix is a valid prefix of any dictionary word
    String prefix = current.toString();
    if (!hasPrefixInDictionary(dictionary, prefix)) return;

    String letters = mapping[digits.charAt(index) - '0'];
    for (char c : letters.toCharArray()) {
        current.append(c);
        backtrack(digits, mapping, index + 1, current, dictionary, result);
        current.deleteCharAt(current.length() - 1);
    }
}
```

---

## Comparison of All Variants

| Problem | Input | Usage | Order | Approach |
|---|---|---|---|---|
| Combination Sum I | Distinct, target | Unlimited | Doesn't matter | Backtracking |
| Combination Sum II | Duplicates, target | Once | Doesn't matter | Backtracking |
| Combination Sum III | 1-9, k, target | Once | Doesn't matter | Backtracking |
| Combination Sum IV | Distinct, target | Unlimited | Matters | DP (permutations) |
| Factor Combinations | Integer n | Unlimited | Doesn't matter | Backtracking |
| Letter Combinations | Digit string | Once per position | Matters | Backtracking |

## Key Takeaways

1. **Combination Sum IV is misnamed** — it actually counts permutations. Use DP, not backtracking
2. **Factor combinations** use `i*i ≤ n` for efficient pruning — a different pattern from sum problems
3. **Letter combinations** is the simplest backtracking — fixed depth, no constraints, just all combinations
4. **The differentiating factor** is: order matters? → permutations (DP), order doesn't matter → combinations (backtracking)
5. **Always consider** whether the problem needs all solutions (backtracking) or just the count (DP/memoization)
