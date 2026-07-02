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
