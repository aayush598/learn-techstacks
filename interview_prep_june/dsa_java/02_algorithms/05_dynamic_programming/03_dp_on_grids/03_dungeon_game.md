# Dungeon Game

**Problem**: A knight starts at top-left of an m×n dungeon. Each cell has a number (positive = health gain, negative = damage). The knight needs at least 1 health at all times. Find minimum initial health needed to reach bottom-right.

**Example**: dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]] → 7

---

## Key Insight: Reverse DP

We compute from bottom-right to top-left because the minimum health needed at start depends on optimal future choices.

```
dp[i][j] = minimum health needed at (i,j) to reach bottom-right

At bottom-right:
  dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
                = max(1, 1 - (-5)) = max(1, 6) = 6
                (if dungeon value is negative, need more health)

For other cells:
  dp[i][j] = max(1, min(dp[i+1][j], dp[i][j+1]) - dungeon[i][j])
```

**Intuition**: 
- `minHealthNeeded - damage + health = 1` (arrive with exactly enough, end at 1)
- If dungeon[i][j] gives health (+), you need less health before entering
- If dungeon[i][j] takes health (-), you need more health before entering

---

## Bottom-Up DP (Reverse)

```java
public int calculateMinimumHP(int[][] dungeon) {
    int m = dungeon.length, n = dungeon[0].length;
    int[][] dp = new int[m][n];

    // Bottom-right cell
    dp[m - 1][n - 1] = Math.max(1, 1 - dungeon[m - 1][n - 1]);

    // Last row (can only move right)
    for (int j = n - 2; j >= 0; j--) {
        dp[m - 1][j] = Math.max(1, dp[m - 1][j + 1] - dungeon[m - 1][j]);
    }

    // Last column (can only move down)
    for (int i = m - 2; i >= 0; i--) {
        dp[i][n - 1] = Math.max(1, dp[i + 1][n - 1] - dungeon[i][n - 1]);
    }

    // Fill rest from bottom-right to top-left
    for (int i = m - 2; i >= 0; i--) {
        for (int j = n - 2; j >= 0; j--) {
            int minHealth = Math.min(dp[i + 1][j], dp[i][j + 1]);
            dp[i][j] = Math.max(1, minHealth - dungeon[i][j]);
        }
    }

    return dp[0][0];
}
```

### Trace for [[-2,-3,3],[-5,-10,1],[10,30,-5]]

```
dungeon:
 [-2, -3,  3]
 [-5, -10, 1]
 [10, 30, -5]

dp (computed bottom-right to top-left):
 [7,  5,  2]
 [6,  11, 5]
 [1,  1,  6]

Cell by cell:
dp[2][2] = max(1, 1-(-5)) = 6
dp[2][1] = max(1, 6-30) = 1   (30 health gain, so we need just 1 min health)
dp[2][0] = max(1, 1-10) = 1   (10 health gain)
dp[1][2] = max(1, 6-1) = 5    (losing 5 from 6)
dp[0][2] = max(1, min(5,2)-3) = max(1, 2-3) = max(1, -1) = 1
dp[1][1] = max(1, min(11,5)-(-10)) = max(1, 5+10) = 15
Wait...

Let me recalculate more carefully.

dp[2][2] = max(1, 1-(-5)) = 6
dp[1][2] = max(1, dp[2][2] - 1) = max(1, 6-1) = 5
dp[0][2] = max(1, dp[1][2] - 3) = max(1, 5-3) = 2
dp[2][1] = max(1, dp[2][2] - 30) = max(1, 6-30) = 1
dp[1][1] = max(1, min(dp[2][1], dp[1][2]) - (-10)) = max(1, min(1,5)+10) = 11
dp[0][1] = max(1, min(dp[1][1], dp[0][2]) - (-3)) = max(1, min(11,2)+3) = 5
dp[2][0] = max(1, dp[2][1] - 10) = max(1, 1-10) = 1
dp[1][0] = max(1, min(dp[2][0], dp[1][1]) - (-5)) = max(1, min(1,11)+5) = 6
dp[0][0] = max(1, min(dp[1][0], dp[0][1]) - (-2)) = max(1, min(6,5)+2) = 7

Answer: 7
```

---

## Space-Optimized

```java
public int calculateMinimumHP(int[][] dungeon) {
    int m = dungeon.length, n = dungeon[0].length;
    int[] dp = new int[n + 1];
    Arrays.fill(dp, Integer.MAX_VALUE);
    dp[n - 1] = 1; // need at least 1 at the end

    for (int i = m - 1; i >= 0; i--) {
        for (int j = n - 1; j >= 0; j--) {
            int minHealth = Math.min(dp[j], dp[j + 1]);
            dp[j] = Math.max(1, minHealth - dungeon[i][j]);
        }
    }

    return dp[0];
}
```

---

## Complexity

| Version | Time | Space |
|---|---|---|
| Full DP | O(m*n) | O(m*n) |
| 1D DP | O(m*n) | O(n) |

## Key Takeaways

1. **Reverse DP** — compute from bottom-right to top-left
2. **dp[i][j] = min health needed at (i,j)** — thinking of remaining path
3. **Formula**: `max(1, minNeededFromNext - currentCellValue)`
4. **Must keep health ≥ 1 at all times** — the `max(1, ...)` ensures this
5. **Initialization**: dp[m-1][n-1] = max(1, 1 - dungeon[m-1][n-1])
