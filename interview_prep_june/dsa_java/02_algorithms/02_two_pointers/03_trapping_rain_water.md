# Trapping Rain Water

This is one of those problems that looks simple but trips people up. Let's break it down properly.

## Problem Statement

Given an array of non-negative integers representing elevation heights, compute how much water can be trapped after raining.

```
Input:  [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
Output: 6

Visual representation:
      
      ■
  ■   ■ ■   ■
_ ■ ■ _ ■ ■ _ ■
```

Each `■` is a building, and `_` is trapped water.

## The Core Insight

Here's the key: **water trapped at any position = min(max height to left, max height to right) - height[i]**

If the left max is 3 and right max is 4, water can only rise to 3 (the shorter wall). If height[i] is 1, water trapped = 3 - 1 = 2.

**If this value is negative, no water is trapped.**

## Approach 1: Brute Force (O(n²), O(1))

```java
public int trapBruteForce(int[] height) {
    int n = height.length;
    int total = 0;

    for (int i = 0; i < n; i++) {
        int leftMax = 0, rightMax = 0;

        for (int j = i; j >= 0; j--) {
            leftMax = Math.max(leftMax, height[j]);
        }

        for (int j = i; j < n; j++) {
            rightMax = Math.max(rightMax, height[j]);
        }

        total += Math.min(leftMax, rightMax) - height[i];
    }

    return total;
}
```

Simple but slow. For each position, we scan left and right. That's O(n²).

## Approach 2: Dynamic Programming (O(n), O(n))

Precompute leftMax and rightMax for each position.

```java
public int trapDP(int[] height) {
    int n = height.length;
    if (n <= 2) return 0;

    int[] leftMax = new int[n];
    int[] rightMax = new int[n];

    leftMax[0] = height[0];
    for (int i = 1; i < n; i++) {
        leftMax[i] = Math.max(leftMax[i - 1], height[i]);
    }

    rightMax[n - 1] = height[n - 1];
    for (int i = n - 2; i >= 0; i--) {
        rightMax[i] = Math.max(rightMax[i + 1], height[i]);
    }

    int total = 0;
    for (int i = 0; i < n; i++) {
        total += Math.min(leftMax[i], rightMax[i]) - height[i];
    }

    return total;
}
```

Two passes to build the arrays, one pass to compute. Clean, but uses O(n) extra space.

## Approach 3: Stack (O(n), O(n))

Use a monotonic decreasing stack.

```java
public int trapStack(int[] height) {
    int n = height.length;
    Stack<Integer> stack = new Stack<>();
    int total = 0;

    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && height[i] > height[stack.peek()]) {
            int bottom = stack.pop();

            if (stack.isEmpty()) break;

            int left = stack.peek();
            int width = i - left - 1;
            int boundedHeight = Math.min(height[left], height[i]) - height[bottom];

            total += width * boundedHeight;
        }
        stack.push(i);
    }

    return total;
}
```

This processes the array left to right, maintaining a stack of decreasing heights. When we find a taller bar, we pop from the stack and calculate water trapped above the popped bar.

## Approach 4: Two Pointers (O(n), O(1)) — THE BEST

This is the interview darling. O(n) time, O(1) space.

```java
public int trap(int[] height) {
    int n = height.length;
    if (n <= 2) return 0;

    int left = 0;
    int right = n - 1;
    int leftMax = 0;
    int rightMax = 0;
    int total = 0;

    while (left < right) {
        if (height[left] < height[right]) {
            // Left side determines the water level
            if (height[left] >= leftMax) {
                leftMax = height[left]; // No water, just update max
            } else {
                total += leftMax - height[left]; // Water trapped!
            }
            left++;
        } else {
            // Right side determines the water level
            if (height[right] >= rightMax) {
                rightMax = height[right];
            } else {
                total += rightMax - height[right];
            }
            right--;
        }
    }

    return total;
}
```

### How Does This Work?

The brilliance: at each step, we know the water level is bounded by the *shorter* of `leftMax` and `rightMax`. 

- If `height[left] < height[right]`, then `rightMax` is at least `height[right]` which is > `height[left]`. So the limiting factor is the left side.
- We only need `leftMax` (which we track) to compute water at the left position.
- After processing left, we move inward.
- Symmetric for the right side.

### Dry Run

```
Height: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
         L                                          R
l=0, r=11, lM=0, rM=0, total=0

h[0]=0 < h[11]=1, h[0]=0 >= lM=0? yes → lM=0, L→1
h[1]=1 < h[11]=1, h[1]=1 >= lM=0? yes → lM=1, L→2
h[2]=0 < h[11]=1, h[2]=0 >= lM=1? no → total+=1-0=1, L→3
h[3]=2 < h[11]=1? NO → else branch
h[11]=1 >= rM=0? yes → rM=1, R→10
h[3]=2 < h[10]=2? no, h[10]=2 >= rM=1? yes → rM=2, R→9
h[3]=2 < h[9]=1? no, h[9]=1 >= rM=2? no → total+=2-1=2, R→8
...and so on

Total = 6 ✓
```

## Complexity Comparison

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force | O(n²) | O(1) | Don't use in interviews |
| DP | O(n) | O(n) | Clean, easy to explain |
| Stack | O(n) | O(n) | Good to mention |
| Two Pointers | O(n) | O(1) | The goal |

## Interview Strategy

1. **Start with the DP approach** — it's the most intuitive and shows you understand the core insight (water = min(leftMax, rightMax) - height[i]).
2. **Then optimize to two pointers** — show you can think about space optimization.
3. **Mention the stack approach** as an alternative data structure perspective.

## Common Mistakes

1. **Forgetting the base case** — if n ≤ 2, no water can be trapped.
2. **Misunderstanding the two-pointer condition** — we compare `height[left]` with `height[right]`, not `leftMax` with `rightMax`.
3. **Using `<=` instead of `<` in while condition** — both work, but `<` is more common since `==` means we can process either side.
4. **Negative water** — always ensure `leftMax - height[left]` or `rightMax - height[right]` is only added when positive.

## Variations

### Trapping Rain Water II (3D)
Same concept but in a 2D matrix. Uses a min-heap instead of two pointers.

```java
// Concept: push all boundary cells into a min-heap
// Process cells in order of increasing height
// Track the maximum boundary height seen so far
// For each popped cell, check neighbors
```

### Pour Water
Given a landscape, repeatedly pour water at a position and see where it settles.

## The Takeaway

Two-pointer trap solution is beautiful because it computes the answer in one pass without knowing the "future" explicitly — each pointer processes its side based on the guarantee provided by the taller bar on the other side.

Memorize the template, understand the intuition, and you'll nail this in any interview.
