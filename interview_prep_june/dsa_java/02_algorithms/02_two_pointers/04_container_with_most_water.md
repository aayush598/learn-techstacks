# Container With Most Water

This is the friendly cousin of Trapping Rain Water. If Trapping Rain Water asks "how much water can be trapped?", Container With Most Water asks "which two lines form the container that holds the most water?"

It's simpler, cleaner, and a perfect introduction to the opposite-direction two-pointer pattern.

## Problem Statement

Given an array of non-negative integers where each represents a vertical line at position `i`, find two lines that together with the x-axis form a container that holds the most water.

```
Input:  [1, 8, 6, 2, 5, 4, 8, 3, 7]
Output: 49

Visual:
  |
  |       ■               ■
  |       ■               ■     ■
  |       ■     ■         ■     ■
  |       ■     ■   ■     ■     ■
  |       ■     ■   ■   ■ ■     ■
  |       ■   ■ ■   ■   ■ ■     ■
  |   ■   ■   ■ ■   ■   ■ ■   ■ ■
  |_ _ ■ _ ■ _ ■ _ ■ _ ■ _ ■ _ ■ _ ■
```

The max area is between the lines at index 1 (height 8) and index 8 (height 7): 
height = min(8, 7) = 7, width = 8 - 1 = 7, area = 7 × 7 = 49

## Brute Force (O(n²))

```java
public int maxAreaBruteForce(int[] height) {
    int n = height.length;
    int maxArea = 0;

    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            int h = Math.min(height[i], height[j]);
            int w = j - i;
            maxArea = Math.max(maxArea, h * w);
        }
    }

    return maxArea;
}
```

Checks every pair. Works but O(n²) is too slow for large inputs.

## Two Pointers (O(n), O(1))

```java
public int maxArea(int[] height) {
    int left = 0;
    int right = height.length - 1;
    int maxArea = 0;

    while (left < right) {
        int h = Math.min(height[left], height[right]);
        int w = right - left;
        maxArea = Math.max(maxArea, h * w);

        // Move the pointer with the smaller height
        if (height[left] < height[right]) {
            left++;
        } else {
            right--;
        }
    }

    return maxArea;
}
```

### Why Move the Smaller Height?

This is the critical insight. At any state `(left, right)`, the area is: `min(height[left], height[right]) * (right - left)`.

If we move the **taller** line inward:
- Width decreases (always bad for area)
- Height stays ≤ the shorter line (never increases)
- Area can only stay the same or decrease

If we move the **shorter** line inward:
- Width decreases (bad)
- But height *might* increase (good!)
- If we find a taller line, the area could increase

So we always move the pointer with the smaller height.

### Formal Reasoning

Let `h[i]` be the height at index `i`. Suppose `h[left] < h[right]`. The area is `h[left] * (right - left)`.

For any `k` where `left < k < right`:
- Area with `k` and `right` = `min(h[k], h[right]) * (right - k)`
- Since `right - k < right - left` and `min(h[k], h[right]) ≤ h[right]`, the area with `(k, right)` could theoretically be larger if `h[k] > h[left]`.
- But area with `(left, k)` = `min(h[left], h[k]) * (k - left)`. Since `min(h[left], h[k]) ≤ h[left]` and `k - left < right - left`, this is *definitely* smaller than `h[left] * (right - left)`.

So `(left, right)` is the best possible area involving `left`. We can safely discard `left` and move inward.

## Dry Run

```
Height: [1, 8, 6, 2, 5, 4, 8, 3, 7]

left=0, right=8 → h=min(1,7)=1, w=8-0=8, area=8,  max=8
  height[0]=1 < height[8]=7 → left++ (1)

left=1, right=8 → h=min(8,7)=7, w=8-1=7, area=49, max=49
  height[1]=8 > height[8]=7 → right-- (7)

left=1, right=7 → h=min(8,3)=3, w=7-1=6, area=18, max=49
  height[1]=8 > height[7]=3 → right-- (6)

left=1, right=6 → h=min(8,8)=8, w=6-1=5, area=40, max=49
  height[1]=8 == height[6]=8 → either:
  Let's say right-- (5)

left=1, right=5 → h=min(8,4)=4, w=5-1=4, area=16, max=49
  height[1]=8 > height[5]=4 → right-- (4)

left=1, right=4 → h=min(8,5)=5, w=4-1=3, area=15, max=49
  height[1]=8 > height[4]=5 → right-- (3)

left=1, right=3 → h=min(8,2)=2, w=3-1=2, area=4,  max=49
  height[1]=8 > height[3]=2 → right-- (2)

left=1, right=2 → h=min(8,6)=6, w=2-1=1, area=6,  max=49
  height[1]=8 > height[6]=6 → right-- (1)
  left < right? no → exit

Result: 49
```

Only 7 iterations instead of checking all 36 pairs. Not bad at all!

## Complete Solution with Optimization

```java
public int maxArea(int[] height) {
    int left = 0;
    int right = height.length - 1;
    int maxArea = 0;

    while (left < right) {
        int h = Math.min(height[left], height[right]);
        int w = right - left;

        if (h * w > maxArea) {
            maxArea = h * w;
        }

        if (height[left] < height[right]) {
            // Skip elements that can't beat the current max
            // (optimization — optional, but demonstrates deeper thinking)
            int currentLeft = height[left];
            while (left < right && height[left] <= currentLeft) {
                left++;
            }
        } else {
            int currentRight = height[right];
            while (left < right && height[right] <= currentRight) {
                right--;
            }
        }
    }

    return maxArea;
}
```

The optimization skips consecutive heights that are shorter than the current one, since they can't possibly increase the area. This doesn't change the worst-case O(n) but helps in practice.

## Comparison with Trapping Rain Water

| Aspect | Container With Most Water | Trapping Rain Water |
|--------|--------------------------|---------------------|
| Goal | Max area between two lines | Total water trapped |
| Two-pointer logic | Move shorter height inward | Compare heights, process shorter side |
| Formula | `min(h[l], h[r]) * (r-l)` | `min(leftMax, rightMax) - h[i]` |
| Track | Just max area | Cumulative total |

## Variations

### Container With Most Water II
Multiple containers — same concept, pick the best pair.

### Pair with Maximum Product of Indices
Sometimes framed as water but asks about different formulas.

### With Negative Numbers
If heights could be negative (unlikely but possible in variations), treat negative as 0.

## Edge Cases

```java
// Two elements
int[] h1 = {1, 1}; // area = min(1,1) * (1-0) = 1

// Descending heights
int[] h2 = {5, 4, 3, 2, 1}; // max area = min(5,1)*4 = 4

// Ascending heights
int[] h3 = {1, 2, 3, 4, 5}; // max area = min(1,5)*4 = 4

// All same height
int[] h4 = {3, 3, 3, 3}; // area = 3*3 = 9

// Zero heights
int[] h5 = {0, 0, 0, 0}; // area = 0
```

## Interview Tips

1. **Start with brute force** — show you can get to a working solution
2. **Explain the intuition** — "we move the shorter line because it's the limiting factor"
3. **Prove correctness** — "the current left position can never form a larger area with any line to its right, so we safely discard it"
4. **Mention the optimization** — skip consecutive shorter lines (shows attention to detail)
5. **Compare with trapping rain water** — shows you understand both problems

This problem is a favorite at **Google, Amazon, Facebook, and Microsoft**. It tests your ability to find an elegant optimization of a straightforward brute-force solution. The two-pointer approach is simple but the reasoning behind *why* it works is what interviewers want to see.
