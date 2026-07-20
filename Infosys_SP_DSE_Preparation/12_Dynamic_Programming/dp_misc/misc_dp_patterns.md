# DP Misc Patterns

## Digit DP

Count numbers in [0, high] satisfying a property, digit by digit.

State: dp[pos][tight][leading_zero][state]

### Template

def digit_dp(high, is_valid):
    digits = list(map(int, str(high)))
    n = len(digits)
    memo = {}
    def pos_func(pos, tight, state):
        if pos == n:
            return 1 if state condition else 0
        key = (pos, tight, state)
        if key in memo: return memo[key]
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            new_state = transition(state, d)
            if is_valid(new_state):
                total += pos_func(pos+1, tight and d==limit, new_state)
        memo[key] = total
        return total
    return pos_func(0, True, 0)

### Example: Count numbers with digit sum = target

def count_digit_sum(high, target):
    digits = list(map(int, str(high)))
    n = len(digits)
    memo = {}
    def dfs(pos, tight, sum_sofar):
        if sum_sofar > target: return 0
        if pos == n:
            return 1 if sum_sofar == target else 0
        key = (pos, tight, sum_sofar)
        if key in memo: return memo[key]
        limit = digits[pos] if tight else 9
        total = 0
        for d in range(limit + 1):
            total += dfs(pos+1, tight and d==limit, sum_sofar+d)
        memo[key] = total
        return total
    return dfs(0, True, 0)

### Example: Count numbers with no consecutive ones

def count_non_consecutive_ones(n):
    """Count binary strings of length n with no consecutive 1s"""
    if n <= 0: return 1
    dp0 = 1  # ends with 0
    dp1 = 1  # ends with 1
    for _ in range(2, n+1):
        new_dp0 = dp0 + dp1
        dp1 = dp0
        dp0 = new_dp0
    return dp0 + dp1

# Equivalent to fib(n+2) or fib(n+1) + fib(n)

---

## Interval DP

State: dp[i][j] over interval [i, j]

for length in range(2, n+1):
    for i in range(n-length+1):
        j = i + length - 1
        for k in range(i, j):
            dp[i][j] = min(dp[i][j], combine(dp[i][k], dp[k+1][j]))

### Matrix Chain Multiplication

def matrix_chain(p):
    """p = dimensions: p[0]xp[1], p[1]xp[2], ..."""
    n = len(p) - 1
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n+1):
        for i in range(n-length+1):
            j = i + length - 1
            dp[i][j] = float("inf")
            for k in range(i, j):
                q = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]
                if q < dp[i][j]: dp[i][j] = q
    return dp[0][n-1]

### Minimum Cost to Cut a Stick

def min_cost_to_cut(n, cuts):
    """n = stick length, cuts = positions to cut"""
    cuts = [0] + sorted(cuts) + [n]
    m = len(cuts)
    dp = [[0]*m for _ in range(m)]
    for length in range(2, m):
        for i in range(m-length):
            j = i + length
            dp[i][j] = float("inf")
            for k in range(i+1, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cuts[j] - cuts[i])
    return dp[0][m-1]

---

## Probability DP

### Dice Throw (n dice, each k faces, sum = target)

def dice_sum_prob(n, k, target):
    """Probability/ways to get target sum with n dice of k faces (1..k)"""
    dp = [0] * (target + 1)
    dp[0] = 1
    for die in range(n):
        new = [0] * (target + 1)
        for s in range(0, target+1):
            if dp[s] == 0: continue
            for face in range(1, k+1):
                if s + face <= target:
                    new[s+face] += dp[s]
        dp = new
    return dp[target]

---

## String DP

### Regular Expression Matching

Implement regex with "." (any char) and "*" (zero or more of preceding).

def regex_match(s, p):
    m, n = len(s), len(p)
    memo = {}
    def dfs(i, j):
        if j == n:
            return i == m
        if (i, j) in memo: return memo[(i, j)]
        first_match = i < m and (s[i] == p[j] or p[j] == ".")
        if j+1 < n and p[j+1] == "*":
            ans = dfs(i, j+2) or (first_match and dfs(i+1, j))
        else:
            ans = first_match and dfs(i+1, j+1)
        memo[(i, j)] = ans
        return ans
    return dfs(0, 0)

def regex_match_tab(s, p):
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True
    for j in range(2, n+1):
        if p[j-1] == "*":
            dp[0][j] = dp[0][j-2]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == s[i-1] or p[j-1] == ".":
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == "*":
                dp[i][j] = dp[i][j-2]
                if p[j-2] == s[i-1] or p[j-2] == ".":
                    dp[i][j] = dp[i][j] or dp[i-1][j]
    return dp[m][n]

---

### Wildcard Matching

Implement wildcard with "?" (any single char) and "*" (any sequence).

def wildcard_match(s, p):
    m, n = len(s), len(p)
    memo = {}
    def dfs(i, j):
        if j == n: return i == m
        if i == m: return all(p[k] == "*" for k in range(j, n))
        if (i, j) in memo: return memo[(i, j)]
        if p[j] == "*":
            ans = dfs(i+1, j) or dfs(i, j+1)
        else:
            ans = (s[i] == p[j] or p[j] == "?") and dfs(i+1, j+1)
        memo[(i, j)] = ans
        return ans
    return dfs(0, 0)

def wildcard_match_tab(s, p):
    m, n = len(s), len(p)
    dp = [[False]*(n+1) for _ in range(m+1)]
    dp[0][0] = True
    for j in range(1, n+1):
        if p[j-1] == "*":
            dp[0][j] = dp[0][j-1]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == s[i-1] or p[j-1] == "?":
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == "*":
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
    return dp[m][n]

---

## Summary Table
| Pattern | Technique | Example | Complexity |
|---------|-----------|---------|------------|
| Digit DP | pos+tight+state | Count range numbers | O(pos*10*states) |
| Interval DP | length, i, k | MCM, palindrome | O(n^3) |
| Probability DP | dp[s] += dp[s-face] | Dice sum | O(n*k*target) |
| String DP | 2D match | Regex, wildcard | O(m*n) |
