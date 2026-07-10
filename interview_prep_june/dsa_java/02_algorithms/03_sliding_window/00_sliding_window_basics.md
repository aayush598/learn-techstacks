# Sliding Window - The Basics

If Two Pointers is about two specific positions, **Sliding Window** is about a contiguous *range* that moves through the data structure. Think of it as a window pane that slides — you see new elements on the right and lose old ones on the left.

## The Core Idea

A sliding window is a subarray defined by a `[left, right]` range that moves through the array. As it moves, you **add** the new element on the right and **remove** the element that fell out on the left.

```
Array:  [2, 5, -1, 3, 7, 2, 4, 6]
Window (size 3):
Step 1: [2, 5, -1] → sum = 6
Step 2: [5, -1, 3] → sum = 6 - 2 + 3 = 7 → slide!
Step 3: [-1, 3, 7] → sum = 7 - 5 + 7 = 9
```

You never recompute the whole window. You just update the edges. That's O(n) instead of O(n·k).

## Two Flavors

### 1. Fixed Size Window

The window size is constant (`k`). You slide one element at a time.

```
[—window—]
[—window—]
 [—window—]
  [—window—]
```

**When to use**: the problem explicitly says "subarray of size k" or "every window of size k".

### 2. Variable Size Window

The window expands or contracts based on a condition.

```
[—window—]
[———window—————]
[window—]
  [——window——]
```

**When to use**: the problem says "longest subarray with property X" or "shortest subarray with property X".

## Template: Fixed Size Window

```java
public int fixedSlidingWindow(int[] arr, int k) {
    int n = arr.length;
    if (n < k) return -1;

    // Compute the first window
    int sum = 0;
    for (int i = 0; i < k; i++) {
        sum += arr[i];
    }

    int maxSum = sum;

    // Slide the window
    for (int i = k; i < n; i++) {
        sum += arr[i] - arr[i - k]; // Add new, remove old
        maxSum = Math.max(maxSum, sum);
    }

    return maxSum;
}
```

The key line is `sum += arr[i] - arr[i - k]`. That's the entire sliding window pattern in a nutshell.

## Template: Variable Size Window

```java
public int variableSlidingWindow(int[] arr, int target) {
    int left = 0;
    int sum = 0;
    int maxLen = 0;

    for (int right = 0; right < arr.length; right++) {
        // Add the new element to the window
        sum += arr[right];

        // Shrink until condition is valid
        while (sum > target) {
            sum -= arr[left];
            left++;
        }

        // Update the answer if condition is met
        if (sum == target) {
            maxLen = Math.max(maxLen, right - left + 1);
        }
    }

    return maxLen;
}
```

### The Flow

```
for each right:
  add arr[right]
  while window is invalid:
    remove arr[left]
    left++
  update answer
```

That's it. Every variable-size sliding window problem follows this exact structure. The only things that change are:
1. What "add" means
2. What "invalid" means
3. What "update answer" means

## When to Use Sliding Window

Use sliding window when:
- **Contiguous subarray/substring** problems
- **"Subarray with property X"** (longest, shortest, count)
- The property can be **efficiently maintained** as the window slides

Don't use it when:
- The problem involves **non-contiguous** elements (use DP or greedy instead)
- The window property can't be updated incrementally (frequent count reset needed)

## Complexity Analysis

| Window Type | Time | Space | 
|-------------|------|-------|
| Fixed | O(n) | O(1) or O(k) |
| Variable | O(n) | O(1) or O(k) |

The O(n) time holds because each element is added to the window once and removed at most once. Even with the inner `while` loop, each element moves `left->right` once and `left->right+1` once — two movements total.

## Common Pitfalls

1. **Window size validation** — for fixed windows, check `n < k` upfront
2. **Forgetting to handle empty windows** — when `left > right`, the window is empty
3. **Infinite loops** — the `while` loop that shrinks must always advance `left`
4. **HashMap key management** — when removing from HashMap, remove keys when count reaches 0
5. **Edge cases** — k=0, k=n, empty array, single element

## The Mentality Shift

When you see a subarray problem:
1. Can I check all subarrays? O(n²) — too slow
2. Can I slide a window? O(n) — much better!

The insight is that sliding window avoids recomputing the same subarray information. If I know the sum of `arr[2..5]`, I can compute the sum of `arr[2..6]` just by adding `arr[6]`. This seems trivial but it's the foundation of all sliding window solutions.

## Detection Cheat Sheet

| Problem Signal | Window Type |
|----------------|-------------|
| "Exactly K" | Fixed |
| "At most K" | Variable |
| "Longest subarray with..." | Variable (expand, contract) |
| "Every window of size K" | Fixed |
| "Minimum window containing..." | Variable (contract to minimize) |
| "At least one occurrence" | Variable |

## Common Problem Patterns

| # | Pattern | Window Type | Example |
|---|---------|-------------|---------|
| 1 | Max/Min sum of size K | Fixed | Max sum subarray |
| 2 | First/Max/Min in every window | Fixed with deque | First negative, max in window |
| 3 | Anagram/substring match | Fixed | Find anagrams |
| 4 | Longest subarray with sum K (+ve) | Variable | Largest subarray sum K |
| 5 | Longest substring without repeat | Variable with map | No repeating chars |
| 6 | Minimum window with condition | Variable (expand/contract) | Min window substring |
| 7 | At most K distinct | Variable with map | Longest K unique chars |
| 8 | Count subarrays with condition | Variable + atMost trick | Nice subarrays |

## More Template Examples

### Fixed Window: Generic Template

```java
public List<Integer> fixedWindow(/* params */) {
    int n = arr.length;
    List<Integer> result = new ArrayList<>();
    
    // Build initial window
    for (int i = 0; i < k; i++) {
        // process arr[i]
    }
    
    if (/* condition for first window */) {
        result.add(/* value */);
    }
    
    // Slide
    for (int i = k; i < n; i++) {
        // add arr[i]
        // remove arr[i-k]
        if (/* condition */) {
            result.add(/* value */);
        }
    }
    
    return result;
}
```

### Variable Window: Generic Template

```java
public int variableWindow(/* params */) {
    int left = 0;
    int result = 0;
    // State variables (sum, map, etc.)
    
    for (int right = 0; right < n; right++) {
        // expand: add arr[right] to state
        
        // shrink: while condition is INVALID
        while (/* condition invalid */) {
            // remove arr[left] from state
            left++;
        }
        
        // update result using valid window
        result = Math.max(result, right - left + 1);
        // or: result += right - left + 1 (for counting)
    }
    
    return result;
}
```

## The Intuition Behind O(n)

Why is sliding window O(n) when it has a nested loop? Because:

1. **`right`** moves from 0 to n-1 — n total steps forward
2. **`left`** also moves from 0 to n-1 at most — n total steps forward
3. **Each element is processed twice** — once when `right` passes it, once when `left` passes it

The total work is 2n = O(n). The inner `while` loop isn't resetting — it's just `left` catching up.

## When NOT to Use Sliding Window

- **Non-contiguous elements**: subsets, subsequences (not subarrays) → use DP or backtracking
- **Expensive window state updates**: if updating the window state takes O(k) or O(log n), the total could become O(nk) or O(n log n)
- **The condition isn't monotonic**: if expanding the window can both help and hurt the condition, sliding window won't work

## Sliding Window vs Two Pointers

These overlap a lot. The distinction:

- **Two Pointers**: pointers move independently, often from opposite ends
- **Sliding Window**: one pointer chases the other, maintaining a contiguous range

In practice? Sliding window **is** a type of two-pointer technique. But the naming helps clarify which pattern to use.

## Summary

| | Fixed Window | Variable Window |
|--|-------------|----------------|
| Window size | Constant k | Changes based on condition |
| Inner loop | None (direct slide) | while loop to shrink |
| Update | add new, remove old | add right, shrink left, then update |
| Example | Max sum of size k | Longest substring without repeat |
| Template | `sum += arr[i] - arr[i-k]` | Expand-contract-update |

Master these two templates, and you can solve 90% of sliding window problems.

Let's dive into specific problems to see these templates in action!
