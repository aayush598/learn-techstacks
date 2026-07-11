# Candy Distribution

**Problem**: N children in a line, each has a rating. Each child gets at least 1 candy. Children with higher ratings get more than their neighbors. Minimum total candies?

**Greedy**: Two passes — left to right, then right to left.

```java
public int candy(int[] ratings) {
    int n = ratings.length;
    int[] candies = new int[n];
    Arrays.fill(candies, 1);

    // Left to right: ensure higher rating > left neighbor
    for (int i = 1; i < n; i++) {
        if (ratings[i] > ratings[i - 1]) {
            candies[i] = candies[i - 1] + 1;
        }
    }

    // Right to left: ensure higher rating > right neighbor
    for (int i = n - 2; i >= 0; i--) {
        if (ratings[i] > ratings[i + 1]) {
            candies[i] = Math.max(candies[i], candies[i + 1] + 1);
        }
    }

    int total = 0;
    for (int c : candies) total += c;
    return total;
}
```

## Key Insight

> Two passes ensure both left-to-right and right-to-left constraints are satisfied. The Math.max in the second pass preserves the first pass's result when it's higher.

---

## Detailed Walkthrough

### Example: `ratings = [1, 0, 2]`

```
Step 0 — Initialize:
  ratings:  [1, 0, 2]
  candies:  [1, 1, 1]

Step 1 — Left-to-Right Pass:
  Rule: if ratings[i] > ratings[i-1], candies[i] = candies[i-1] + 1

  i=1: ratings[1]=0, ratings[0]=1 → 0 < 1 → no change
  i=2: ratings[2]=2, ratings[1]=0 → 2 > 0 → candies[2] = candies[1]+1 = 2

  candies after L→R: [1, 1, 2]

Step 2 — Right-to-Left Pass:
  Rule: if ratings[i] > ratings[i+1], candies[i] = max(candies[i], candies[i+1]+1)

  i=1: ratings[1]=0, ratings[2]=2 → 0 < 2 → no change
  i=0: ratings[0]=1, ratings[1]=0 → 1 > 0 → candies[0] = max(1, 1+1) = 2

  candies after R→L: [2, 1, 2]

Total: 2 + 1 + 2 = 5
```

### Why `Math.max` Is Critical in Second Pass

Consider `ratings = [1, 2, 3, 2, 1]`:

```
After L→R: [1, 2, 3, 1, 1]
  - i=1: 2>1 → candies[1] = 2
  - i=2: 3>2 → candies[2] = 3
  - i=3: 2>3? No → candies[3] = 1
  - i=4: 1>2? No → candies[4] = 1

After R→L (with Math.max):
  i=3: 2>1 → max(1, 1+1) = 2  ← L→R gave 1, but R→L needs 2
  i=2: 3>2 → max(3, 2+1) = 3  ← L→R already correct
  i=1: 2>3? No → stays 2
  i=0: 1>2? No → stays 1

Result: [1, 2, 3, 2, 1] = 9
```

Without `Math.max`, `candies[3]` stays 1, violating `ratings[3]=2 > ratings[4]=1` — child 3 needs more than child 4 (who has 1).

---

## Complete Trace (Larger Example)

```
ratings = [1, 3, 2, 2, 1]

Pass 1 — Left to Right:
  i=0: [1, -, -, -, -]
  i=1: 3>1 → [1, 2, -, -, -]
  i=2: 2>3? No → [1, 2, 1, -, -]
  i=3: 2>2? No → [1, 2, 1, 1, -]
  i=4: 1>2? No → [1, 2, 1, 1, 1]

Pass 2 — Right to Left:
  i=3: 2>1 → max(1, 2) = 2 → [1, 2, 1, 2, 1]
  i=2: 2>2? No → stays
  i=1: 3>2 → max(2, 2) = 2 → stays
  i=0: 1>3? No → stays

Total: 1+2+1+2+1 = 7
```

---

## Edge Cases

| Case | ratings | Candies | Total | Notes |
|------|---------|---------|-------|-------|
| All equal | `[3,3,3]` | `[1,1,1]` | 3 | No neighbor has higher rating |
| Strictly increasing | `[1,2,3,4]` | `[1,2,3,4]` | 10 | L→R handles everything |
| Strictly decreasing | `[4,3,2,1]` | `[4,3,2,1]` | 10 | R→L handles everything |
| Single child | `[5]` | `[1]` | 1 | Minimum candy |
| Peak in middle | `[1,2,3,2,1]` | `[1,2,3,2,1]` | 9 | Symmetric |
| Valley in middle | `[3,1,2]` | `[2,1,2]` | 5 | Valley gets 1 |
| Plateau | `[1,2,2,1]` | `[1,2,2,1]` | 6 | Equal neighbors don't need more |

---

## O(1) Space Approach: Slope Concept

Track **slopes** (up-slopes, down-slopes) instead of an array:

```java
public int candySlope(int[] ratings) {
    if (ratings.length <= 1) return ratings.length;

    int total = 1;
    int up = 0, down = 0;

    for (int i = 1; i < ratings.length; i++) {
        if (ratings[i] > ratings[i - 1]) {
            up++;
            down = 0;
            total += 1 + up;
        } else if (ratings[i] < ratings[i - 1]) {
            down++;
            up = 0;
            total += down;
        } else {
            up = 0;
            down = 0;
            total += 1;
        }
    }
    return total;
}
```

**Tradeoff**: O(1) space, but trickier to reason about. The array approach is recommended for interviews.

---

## Variants

### Variant 1: Circular Arrangement (LeetCode 357 variant)

Children sit in a circle. The first and last child are neighbors. Requires adjusting based on both neighbors. **Approach**: Standard two passes, then check if `ratings[0]` vs `ratings[n-1]` needs updating. May need iteration until stable.

### Variant 2: Each Child Gets At Least K Candies

Add `K-1` to every child's candy count at the end (shift all up by K-1).

---

## Common Pitfalls

1. **Single pass only**: A left-to-right pass alone doesn't handle descent-then-ascent patterns.

2. **Using `if` instead of `Math.max` in R→L**: Without `Math.max`, you overwrite a valid L→R assignment with a smaller R→L value.

3. **Equal ratings**: `ratings[i] == ratings[i-1]` means no constraint — reset slopes, don't increment.
