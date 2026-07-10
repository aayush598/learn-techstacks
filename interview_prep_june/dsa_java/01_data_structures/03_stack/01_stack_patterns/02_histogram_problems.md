# Histogram Problems

> Histogram problems are the crown jewels of monotonic stack. They test your ability to combine boundary-finding (monotonic stack) with area computation. If you can solve "largest rectangle in histogram," you can solve almost anything.

## Largest Rectangle in Histogram (LeetCode 84)

Given an array of bar heights, find the area of the largest rectangle that fits.

**Key Insight:** For each bar `i`, find:
- `leftSmaller[i]`: index of the first bar to the left that is shorter than `heights[i]`
- `rightSmaller[i]`: index of the first bar to the right that is shorter than `heights[i]`
- Width = `rightSmaller[i] - leftSmaller[i] - 1`
- Area = `heights[i] * width`

### Approach 1: Two-pass with monotonic stacks

```java
public int largestRectangleArea(int[] heights) {
    int n = heights.length;
    int[] leftSmaller = new int[n];
    int[] rightSmaller = new int[n];

    // Pass 1: Find left smaller for each bar
    Deque<Integer> stack = new ArrayDeque<>();
    for (int i = 0; i < n; i++) {
        while (!stack.isEmpty() && heights[stack.peek()] >= heights[i]) {
            stack.pop();
        }
        leftSmaller[i] = stack.isEmpty() ? -1 : stack.peek();
        stack.push(i);
    }

    // Pass 2: Find right smaller for each bar
    stack.clear();
    for (int i = n - 1; i >= 0; i--) {
        while (!stack.isEmpty() && heights[stack.peek()] >= heights[i]) {
            stack.pop();
        }
        rightSmaller[i] = stack.isEmpty() ? n : stack.peek();
        stack.push(i);
    }

    // Pass 3: Compute max area
    int maxArea = 0;
    for (int i = 0; i < n; i++) {
        int width = rightSmaller[i] - leftSmaller[i] - 1;
        maxArea = Math.max(maxArea, heights[i] * width);
    }

    return maxArea;
}

// Example: heights = [2, 1, 5, 6, 2, 3]
//
// leftSmaller:  [-1, -1, 1, 2, 1, 4]
// rightSmaller: [1,  6, 4, 4, 6, 6]
//
// i=0: width = 1-(-1)-1 = 1, area = 2*1 = 2
// i=1: width = 6-(-1)-1 = 6, area = 1*6 = 6  ← the shortest bar spans everything
// i=2: width = 4-1-1   = 2, area = 5*2 = 10  ← winner
// i=3: width = 4-2-1   = 1, area = 6*1 = 6
// i=4: width = 6-1-1   = 4, area = 2*4 = 8
// i=5: width = 6-4-1   = 1, area = 3*1 = 3
//
// Max area = 10
```

### Approach 2: Single-pass (elegant)

The trick: when a bar is popped from the stack, we've found its right boundary. The new stack top is its left boundary. No need for separate arrays.

```java
public int largestRectangleArea(int[] heights) {
    Deque<Integer> stack = new ArrayDeque<>();
    int maxArea = 0;

    for (int i = 0; i <= heights.length; i++) {
        int currHeight = (i == heights.length) ? 0 : heights[i];

        while (!stack.isEmpty() && heights[stack.peek()] > currHeight) {
            int height = heights[stack.pop()];
            int width = stack.isEmpty() ? i : i - stack.peek() - 1;
            maxArea = Math.max(maxArea, height * width);
        }

        stack.push(i);
    }

    return maxArea;
}
```

**Why does this work?** By adding a sentinel (height 0) at the end, we force all remaining bars to be popped. Each pop computes the rectangle using the current index as the right boundary and the stack's new top as the left boundary.

---

## Maximal Rectangle in Binary Matrix (LeetCode 85)

Given a matrix of 0s and 1s, find the largest rectangle containing only 1s.

**Insight:** Treat each row as the base of a histogram. The "height" at each cell is the consecutive 1s above it (including itself).

```java
public int maximalRectangle(char[][] matrix) {
    if (matrix.length == 0) return 0;

    int rows = matrix.length;
    int cols = matrix[0].length;
    int[] heights = new int[cols];
    int maxArea = 0;

    for (int row = 0; row < rows; row++) {
        // Update heights: if matrix[row][col]=='1', add 1, else reset to 0
        for (int col = 0; col < cols; col++) {
            if (matrix[row][col] == '1') {
                heights[col]++;
            } else {
                heights[col] = 0;
            }
        }

        // Apply largest rectangle in histogram on current heights
        maxArea = Math.max(maxArea, largestRectangleArea(heights));
    }

    return maxArea;
}

// Example:
// matrix =       heights at row 0:  heights at row 1:  heights at row 2:
// ["10100"]      [1,0,1,0,0]        [2,0,2,0,0]        [3,0,3,1,0]
// ["10111"]      [1,0,1,1,1]        [2,0,2,2,2]        [3,0,3,3,3]
// ["11101"]      [1,1,1,0,1]        [2,1,2,0,2]        [3,2,3,0,3]
//
// At each row, run histogram algorithm on the heights array
// The answer builds up as you go down
```

### Why this works

```
Row 0: "10100"
Heights: [1, 0, 1, 0, 0]
Histogram: █ █
           (max area = 1)

Row 1: "10111"
Heights: [2, 0, 2, 1, 1]
Histogram: ██   ██ █ █
           (max area = 3 from [2,1,1] at cols 2,3,4... no wait)
           Actually: col 2 has height 2, col 3 height 1, col 4 height 1
           Rectangle of height 1 spanning cols 2-4: area = 3

Row 2: "11101"
Heights: [3, 2, 3, 0, 3]
Histogram: ███ ██ ███   ███
           (max area = 6 from cols 0-2 with height 2: 2*3=6, or col 2 height 3: 3*1=3)
           Actually: cols 0-1 min height = 2, width = 2, area = 4
           Or col 0 height 3, width 1: area = 3
           Best is: cols 0-2, min height = 2, width = 3, area = 6
```

---

## Trapping Rain Water (LeetCode 42 — Stack Approach)

Given `n` non-negative integers representing an elevation map, compute how much water it can trap after rain.

**Stack approach:** Maintain a decreasing stack. When we find a bar taller than the stack top, we've trapped water.

```java
public int trap(int[] height) {
    Deque<Integer> stack = new ArrayDeque<>();
    int water = 0;

    for (int i = 0; i < height.length; i++) {
        while (!stack.isEmpty() && height[stack.peek()] < height[i]) {
            int bottom = stack.pop();

            if (stack.isEmpty()) break;  // no left boundary

            int width = i - stack.peek() - 1;
            int boundedHeight = Math.min(height[i], height[stack.peek()]) - height[bottom];
            water += width * boundedHeight;
        }
        stack.push(i);
    }

    return water;
}

// Example: height = [0,1,0,2,1,0,1,3,2,1,2,1]
//
// i=0: push 0                 stack=[0]
// i=1: h[0]=0 < 1 → pop 0, stack empty → break
//      push 1                 stack=[1]
// i=2: h[1]=1 > 0 → no pop
//      push 2                 stack=[1,2]
// i=3: h[2]=0 < 2 → pop 2, bottom=2
//      stack not empty, stack.peek()=1
//      width = 3-1-1 = 1
//      boundedHeight = min(2,1) - 0 = 1
//      water += 1*1 = 1
//      h[1]=1 < 2 → pop 1, stack empty → break
//      push 3                 stack=[3]
// ... continues...
//
// Total water = 6
```

### How the water calculation works

```
For trapped water at "bottom" bar:
        
        |           i (right boundary)
        |           |
        |  left     |    water = width * boundedHeight
        |  boundary |
        |     ▓▓▓▓▓▓▓▓▓▓▓  ← water level = min(left, right)
        |     ▓▓▓▓▓▓▓▓▓▓▓  ← bottom bar
        |     ▓▓▓▓▓▓▓▓▓▓▓
        
width = i - stack.peek() - 1  (distance between left and right boundaries)
boundedHeight = min(height[left], height[right]) - height[bottom]
```

### Why the stack approach works

The stack maintains a decreasing sequence of heights. When we encounter a taller bar:
1. The stack top is the "bottom" of a potential water pocket
2. The next element in the stack is the left wall
3. The current bar is the right wall
4. Water = distance × min(left wall, right wall) - bottom height

---

## Complexity Summary

| Problem | Time | Space | Key Pattern |
|---------|------|-------|-------------|
| Largest Rectangle in Histogram | O(n) | O(n) | Find left/right smaller boundaries |
| Maximal Rectangle in Matrix | O(rows × cols) | O(cols) | Build heights row by row + histogram |
| Trapping Rain Water | O(n) | O(n) | Decreasing stack, pop when taller found |

---

## Common Mistakes

```java
// 1. Using >= vs > in histogram comparison
// Use >= when you want strictly smaller boundaries (no equal heights extending)
// Use > when equal heights can extend the rectangle

// 2. Forgetting the sentinel (0 at end) in single-pass histogram
// Without it, bars remaining in the stack won't be processed

// 3. Off-by-one in width calculation
// width = rightSmaller - leftSmaller - 1 (not rightSmaller - leftSmaller)

// 4. Not handling empty stack in rain water
// if (stack.isEmpty()) break;  // critical!
```

---

## Key Takeaways

1. **Histogram = find left and right boundaries** for each bar
2. **Single-pass sentinel trick** is elegant — add 0 at the end to flush remaining bars
3. **Matrix problems → build heights row by row**, then apply histogram
4. **Rain water = popping from decreasing stack** — each pop computes a water pocket
5. **Width is always index difference** — this is why we store indices
6. **These are O(n) solutions** to problems that seem to need O(n²) at first glance

These three problems are the "final boss" of monotonic stack. Once you've conquered them, you've truly mastered the pattern.
