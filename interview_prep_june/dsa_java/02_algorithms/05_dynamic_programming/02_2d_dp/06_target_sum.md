# Target Sum

**Problem**: Given an array of integers and a target, assign either '+' or '-' before each integer to make the sum equal to target. Count the number of ways.

**Example**: `nums = [1, 1, 1, 1, 1], target = 3` → 5

```
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
```

---

## Approach 1: Backtracking (Exponential)

```java
public int findTargetSumWays(int[] nums, int target) {
    return backtrack(nums, target, 0, 0);
}

private int backtrack(int[] nums, int target, int index, int sum) {
    if (index == nums.length) {
        return sum == target ? 1 : 0;
    }

    int add = backtrack(nums, target, index + 1, sum + nums[index]);
    int subtract = backtrack(nums, target, index + 1, sum - nums[index]);

    return add + subtract;
}
```

**Time**: O(2^n) — each element can be + or -, so 2 choices per element.

---

## Approach 2: DP with Memoization

```java
public int findTargetSumWays(int[] nums, int target) {
    // Map of (index, sum) → count
    Map<String, Integer> memo = new HashMap<>();
    return backtrack(nums, target, 0, 0, memo);
}

private int backtrack(int[] nums, int target, int index, int sum,
                      Map<String, Integer> memo) {
    if (index == nums.length) {
        return sum == target ? 1 : 0;
    }

    String key = index + "," + sum;
    if (memo.containsKey(key)) return memo.get(key);

    int add = backtrack(nums, target, index + 1, sum + nums[index], memo);
    int subtract = backtrack(nums, target, index + 1, sum - nums[index], memo);

    memo.put(key, add + subtract);
    return add + subtract;
}
```

**Time**: O(n * totalSum) — states are (index, sum), each computed once.

---

## Approach 3: DP with Subset Sum (Optimal)

### Mathematical Transformation

Let's partition the numbers into two sets:
- P = numbers assigned '+'
- N = numbers assigned '-'

```
sum(P) - sum(N) = target
sum(P) + sum(N) = total

Adding: 2 * sum(P) = total + target
sum(P) = (total + target) / 2
```

So the problem reduces to: **count subsets that sum to (total + target) / 2**.

```java
public int findTargetSumWays(int[] nums, int target) {
    int total = 0;
    for (int num : nums) total += num;

    // If total + target is odd or target > total, impossible
    if (total < Math.abs(target) || (total + target) % 2 != 0) return 0;

    int sum = (total + target) / 2;
    return countSubsets(nums, sum);
}

private int countSubsets(int[] nums, int target) {
    int[] dp = new int[target + 1];
    dp[0] = 1;

    for (int num : nums) {
        for (int w = target; w >= num; w--) {
            dp[w] += dp[w - num];
        }
    }

    return dp[target];
}
```

### Trace for nums = [1, 1, 1, 1, 1], target = 3

```
total = 5
sum = (5 + 3) / 2 = 4

Count subsets that sum to 4 from [1,1,1,1,1]:

dp[0] = 1
After 1: dp[1]=1
After 1: dp[1]=2, dp[2]=1
After 1: dp[1]=3, dp[2]=3, dp[3]=1
After 1: dp[1]=4, dp[2]=6, dp[3]=4, dp[4]=1
After 1: dp[1]=5, dp[2]=10, dp[3]=10, dp[4]=5

Answer: dp[4] = 5 ✓
```

---

## Why the Transformation Works

```
Let P = set of numbers with '+' sign
Let N = set of numbers with '-' sign

sum(P) - sum(N) = target   ... (1)
sum(P) + sum(N) = total    ... (2)

(1) + (2): 2 * sum(P) = total + target
sum(P) = (total + target) / 2
```

We need `(total + target)` to be even and non-negative. `sum(P)` must be ≥ 0.

The number of ways to assign signs = number of subsets with sum = sum(P).

---

## Comparison of Approaches

| Approach | Time | Space | When to Use |
|---|---|---|---|
| Backtracking | O(2ⁿ) | O(n) | Small n (≤ 20) |
| Memoization | O(n*total) | O(n*total) | Medium n, first approach |
| Subset Sum DP | O(n*total) | O(total) | Best — space efficient |

## Edge Cases

```java
// target larger than total sum → impossible
nums = [1, 2, 3], target = 10 → 0

// total + target is odd → impossible
nums = [1, 2], target = 2 → total=3, 3+2=5 odd → 0

// All zeros
nums = [0, 0, 0], target = 0 → 8 (each zero can be + or -)

// Large target negative
nums = [1, 2], target = -3 → 1 (-1 + -2 = -3, but target is -3 → 1 way)
```

## Key Takeaways

1. **Target Sum reduces to Subset Sum** via mathematical transformation
2. **The key insight**: `sum(P) = (total + target) / 2`
3. **Constraints**: check that `total >= |target|` and `(total + target) % 2 == 0`
4. **Same pattern**: subset sum DP with 1D array, iterate backwards
5. **For n ≤ 20**: backtracking is fine. For n > 20 and small total: DP is better
