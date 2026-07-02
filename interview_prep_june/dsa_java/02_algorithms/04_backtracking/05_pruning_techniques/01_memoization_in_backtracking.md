# Memoization in Backtracking

When backtracking encounters the same subproblem multiple times, we can cache results to avoid redundant computation. This transforms exponential backtracking into polynomial DP.

---

## When to Add Memoization

**Key question**: Does backtracking encounter the same state multiple times?

- **Yes → Add memoization**: The problem has overlapping subproblems
- **No → Memoization won't help**: Each state is unique (e.g., N-Queens, Sudoku)

### Identifying Overlapping States

Backtracking states overlap when:
1. The same "remaining input" can be reached through different paths
2. The constraints depend only on parameters, not on the order of previous choices

---

## Word Break (Backtracking → DP)

**Problem**: Given a string s and a dictionary of words, determine if s can be segmented into dictionary words.

### Naive Backtracking (Exponential)

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    return backtrack(s, 0, dict);
}

private boolean backtrack(String s, int start, Set<String> dict) {
    if (start == s.length()) return true;

    for (int end = start + 1; end <= s.length(); end++) {
        String prefix = s.substring(start, end);
        if (dict.contains(prefix)) {
            if (backtrack(s, end, dict)) return true;
        }
    }

    return false;
}
```

**Problem**: For s = "aaaaab", dict = ["a", "aa", "aaa", "aaaa", "aaaaa"], this explores the same suffixes repeatedly.

State space: `s.substring(start)` — only n possible values (start ∈ [0, n]).

### With Memoization (Top-Down DP)

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    Boolean[] memo = new Boolean[s.length()];
    return backtrack(s, 0, dict, memo);
}

private boolean backtrack(String s, int start, Set<String> dict, Boolean[] memo) {
    if (start == s.length()) return true;
    if (memo[start] != null) return memo[start];

    for (int end = start + 1; end <= s.length(); end++) {
        String prefix = s.substring(start, end);
        if (dict.contains(prefix)) {
            if (backtrack(s, end, dict, memo)) {
                memo[start] = true;
                return true;
            }
        }
    }

    memo[start] = false;
    return false;
}
```

**Transformation**: O(2^n) → O(n * n) = O(n²) (n starts, each tries O(n) ends)

### Bottom-Up DP

```java
public boolean wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    int n = s.length();
    boolean[] dp = new boolean[n + 1];
    dp[0] = true; // empty string is breakable

    for (int i = 1; i <= n; i++) {
        for (int j = 0; j < i; j++) {
            if (dp[j] && dict.contains(s.substring(j, i))) {
                dp[i] = true;
                break;
            }
        }
    }

    return dp[n];
}
```

---

## Distinct Subsequences (Backtracking → DP)

**Problem**: Given strings s and t, count the number of distinct subsequences of s that equal t.

### Naive Backtracking (Exponential)

```java
public int numDistinct(String s, String t) {
    return backtrack(s, t, 0, 0);
}

private int backtrack(String s, String t, int si, int ti) {
    if (ti == t.length()) return 1;  // matched all of t
    if (si == s.length()) return 0;  // ran out of s

    int count = 0;
    // Skip s[si]
    count += backtrack(s, t, si + 1, ti);
    // Match s[si] with t[ti] (if they match)
    if (s.charAt(si) == t.charAt(ti)) {
        count += backtrack(s, t, si + 1, ti + 1);
    }

    return count;
}
```

State: `(si, ti)` — O(m * n) unique states. But without memoization, we visit many states multiple times.

### With Memoization

```java
public int numDistinct(String s, String t) {
    int[][] memo = new int[s.length()][t.length()];
    for (int[] row : memo) Arrays.fill(row, -1);
    return backtrack(s, t, 0, 0, memo);
}

private int backtrack(String s, String t, int si, int ti, int[][] memo) {
    if (ti == t.length()) return 1;
    if (si == s.length()) return 0;
    if (memo[si][ti] != -1) return memo[si][ti];

    int count = backtrack(s, t, si + 1, ti, memo);
    if (s.charAt(si) == t.charAt(ti)) {
        count += backtrack(s, t, si + 1, ti + 1, memo);
    }

    memo[si][ti] = count;
    return count;
}
```

**Complexity**: O(m * n) instead of O(2^m).

### Bottom-Up DP

```java
public int numDistinct(String s, String t) {
    int m = s.length(), n = t.length();
    int[][] dp = new int[m + 1][n + 1];

    // Empty t can be formed from any prefix of s
    for (int i = 0; i <= m; i++) dp[i][0] = 1;

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            dp[i][j] = dp[i - 1][j]; // skip s[i-1]
            if (s.charAt(i - 1) == t.charAt(j - 1)) {
                dp[i][j] += dp[i - 1][j - 1]; // match
            }
        }
    }

    return dp[m][n];
}
```

---

## General Pattern: Memoizing Backtracking

### State Identification

The state is defined by the parameters that CHANGE during recursion AND determine future results:

```java
// Without memo
int solve(param1, param2, param3, ...)

// With memo
Map<State, Integer> memo = new HashMap<>();

int solve(param1, param2, param3, ...) {
    State key = new State(param1, param2, param3);
    if (memo.containsKey(key)) return memo.get(key);

    // ... compute result ...

    memo.put(key, result);
    return result;
}
```

### Custom State Class

```java
static class State {
    int a, b;
    boolean c;
    State(int a, int b, boolean c) {
        this.a = a; this.b = b; this.c = c;
    }
    @Override
    public boolean equals(Object o) {
        if (!(o instanceof State)) return false;
        State s = (State) o;
        return a == s.a && b == s.b && c == s.c;
    }
    @Override
    public int hashCode() {
        return Objects.hash(a, b, c);
    }
}
```

### Using HashMap for Caching

```java
Map<String, Integer> memo = new HashMap<>();

int solve(int[] nums, int index, int sum) {
    String key = index + "," + sum;
    if (memo.containsKey(key)) return memo.get(key);
    // ... compute ...
    memo.put(key, result);
    return result;
}
```

---

## Word Break II (All Solutions with Memo)

```java
public List<String> wordBreak(String s, List<String> wordDict) {
    Set<String> dict = new HashSet<>(wordDict);
    Map<Integer, List<String>> memo = new HashMap<>();
    return backtrack(s, 0, dict, memo);
}

private List<String> backtrack(String s, int start,
                                Set<String> dict,
                                Map<Integer, List<String>> memo) {
    if (memo.containsKey(start)) return memo.get(start);

    List<String> result = new ArrayList<>();

    if (start == s.length()) {
        result.add(""); // empty string to signal base case
        return result;
    }

    for (int end = start + 1; end <= s.length(); end++) {
        String word = s.substring(start, end);
        if (dict.contains(word)) {
            List<String> subSentences = backtrack(s, end, dict, memo);
            for (String sub : subSentences) {
                if (sub.isEmpty()) {
                    result.add(word);
                } else {
                    result.add(word + " " + sub);
                }
            }
        }
    }

    memo.put(start, result);
    return result;
}
```

---

## Key Indicators: When Memoization Helps

| Situation | Memoization Works? |
|---|---|
| Same subproblem reached via different paths | ✅ Yes |
| State space is small (bounded) | ✅ Yes |
| Each state is visited exactly once | ❌ No benefit |
| State depends on ALL previous choices | ❌ No benefit |

### Quick Check

```
If the recursion parameters can be summarized as (index, some_state)
and index increases monotonically → likely has overlapping subproblems
```

---

## From Backtracking to DP: The Transformation

```
Backtracking with Memoization = Top-Down DP
                                      ↓
                              Bottom-Up DP

Step 1: Write backtracking
Step 2: Identify state parameters
Step 3: Add memo array/dictionary
Step 4: Convert to bottom-up (optional)
```

### Complete Example: Coin Change

```java
// Step 1: Backtracking
int coinChange(int[] coins, int amount) {
    return backtrack(coins, amount);
}
int backtrack(int[] coins, int remaining) {
    if (remaining == 0) return 0;
    int min = Integer.MAX_VALUE;
    for (int coin : coins) {
        if (coin <= remaining) {
            int result = backtrack(coins, remaining - coin);
            if (result != -1) min = Math.min(min, 1 + result);
        }
    }
    return min == Integer.MAX_VALUE ? -1 : min;
}

// Step 2 & 3: Add memoization
int coinChange(int[] coins, int amount) {
    Integer[] memo = new Integer[amount + 1];
    return backtrack(coins, amount, memo);
}
int backtrack(int[] coins, int remaining, Integer[] memo) {
    if (remaining == 0) return 0;
    if (memo[remaining] != null) return memo[remaining];
    int min = Integer.MAX_VALUE;
    for (int coin : coins) {
        if (coin <= remaining) {
            int result = backtrack(coins, remaining - coin, memo);
            if (result != -1) min = Math.min(min, 1 + result);
        }
    }
    memo[remaining] = min == Integer.MAX_VALUE ? -1 : min;
    return memo[remaining];
}

// Step 4: Bottom-up (optional)
int coinChange(int[] coins, int amount) {
    int[] dp = new int[amount + 1];
    Arrays.fill(dp, amount + 1);
    dp[0] = 0;
    for (int i = 1; i <= amount; i++) {
        for (int coin : coins) {
            if (coin <= i) {
                dp[i] = Math.min(dp[i], 1 + dp[i - coin]);
            }
        }
    }
    return dp[amount] > amount ? -1 : dp[amount];
}
```

---

## Common Cache Key Patterns

| Problem | State Parameters | Cache Structure |
|---|---|---|
| Word Break | start index | Boolean[] or List<String>[] |
| Distinct Subsequences | si, ti | int[][] |
| Coin Change | remaining amount | int[] |
| Target Sum | index, current sum | Map<String, Integer> or int[][] |
| Dice Roll | remaining rolls, target | int[][] |
| Interleaving String | i, j | Boolean[][] |

## Rule of Thumb

> If your backtracking function has parameters that can take only O(n × m × ...) distinct values, and you call it more than that many times, you need memoization.

This is how you identify DP problems disguised as backtracking problems!
