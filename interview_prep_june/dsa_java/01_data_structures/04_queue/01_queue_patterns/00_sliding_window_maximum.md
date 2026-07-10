# Sliding Window Maximum

> This is the quintessential deque-in-window problem. It appears in interviews at every major tech company. The brute force is O(nk), the heap approach is O(n log k), but the deque solution is O(n) — and it's the one interviewers want to see.

## Problem Statement

Given an array `nums` and a window size `k`, return the maximum value in each sliding window of size `k`.

```
Input: nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3
Output: [3, 3, 5, 5, 6, 7]

Windows:   [1, 3, -1] → 3
            [3, -1, -3] → 3
            [-1, -3, 5] → 5
            [-3, 5, 3] → 5
            [5, 3, 6] → 6
            [3, 6, 7] → 7
```

## Approach 1: Brute Force — O(nk)

```java
public int[] maxSlidingWindowBrute(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];

    for (int i = 0; i <= n - k; i++) {
        int max = nums[i];
        for (int j = i + 1; j < i + k; j++) {
            max = Math.max(max, nums[j]);
        }
        result[i] = max;
    }

    return result;
}
```

Simple but too slow for large inputs.

## Approach 2: Max Heap — O(n log k)

```java
public int[] maxSlidingWindowHeap(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];

    // Max-heap of (value, index)
    PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> b[0] - a[0]);

    // Initialize with first k elements
    for (int i = 0; i < k; i++) {
        maxHeap.offer(new int[]{nums[i], i});
    }
    result[0] = maxHeap.peek()[0];

    for (int i = k; i < n; i++) {
        maxHeap.offer(new int[]{nums[i], i});

        // Remove elements outside the window (lazy removal)
        while (maxHeap.peek()[1] <= i - k) {
            maxHeap.poll();
        }

        result[i - k + 1] = maxHeap.peek()[0];
    }

    return result;
}
```

Better, but O(n log k). We can do O(n).

---

## Approach 3: Monotonic Deque — O(n) ⭐

### The Key Insight

Maintain a **decreasing deque of indices**. For each new element:
1. Remove indices that are outside the window (from the front)
2. Remove indices of elements smaller than the current (from the back) — they'll never be the max
3. Add the current index
4. The front of the deque is always the max of the current window

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>();  // stores indices, values decrease front→back

    for (int i = 0; i < n; i++) {
        // 1. Remove indices that fell out of the window
        while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
            deque.pollFirst();
        }

        // 2. Remove indices of elements smaller than current (from back)
        //    These elements are "dominated" — current is both larger AND newer
        while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
            deque.pollLast();
        }

        // 3. Add current index
        deque.offerLast(i);

        // 4. Window is formed — record the max (front of deque)
        if (i >= k - 1) {
            result[i - k + 1] = nums[deque.peekFirst()];
        }
    }

    return result;
}
```

### Step-by-Step Trace

```
nums = [1, 3, -1, -3, 5, 3, 6, 7], k = 3

i=0, num=1:
  deque empty → add 0
  deque=[0]  → nums[0]=1

i=1, num=3:
  No out-of-window
  3 > nums[0]=1 → pollLast (remove 0)
  deque empty → add 1
  deque=[1]  → nums[1]=3

i=2, num=-1:
  No out-of-window
  -1 < nums[1]=3 → don't remove
  add 2
  deque=[1, 2]  → nums[1]=3, nums[2]=-1
  Window formed! result[0] = nums[1] = 3 ✓

i=3, num=-3:
  Index 1 (value 3) is still in window (i-k+1=1)
  -3 < nums[2]=-1 → don't remove
  add 3
  deque=[1, 2, 3]  → 3, -1, -3
  result[1] = nums[1] = 3 ✓

i=4, num=5:
  No out-of-window
  5 > nums[3]=-3 → pollLast (3)
  5 > nums[2]=-1 → pollLast (2)
  5 > nums[1]=3 → pollLast (1)
  deque empty → add 4
  deque=[4]  → 5
  result[2] = nums[4] = 5 ✓

i=5, num=3:
  No out-of-window
  3 < nums[4]=5 → don't remove
  add 5
  deque=[4, 5]  → 5, 3
  result[3] = nums[4] = 5 ✓

i=6, num=6:
  No out-of-window
  6 > nums[5]=3 → pollLast (5)
  6 > nums[4]=5 → pollLast (4)
  deque empty → add 6
  deque=[6]  → 6
  result[4] = nums[6] = 6 ✓

i=7, num=7:
  No out-of-window
  7 > nums[6]=6 → pollLast (6)
  deque empty → add 7
  deque=[7]  → 7
  result[5] = nums[7] = 7 ✓

Final: [3, 3, 5, 5, 6, 7] ✓
```

### Why this works

The deque maintains a **decreasing sequence of values** (by storing decreasing indices). This means:

1. **Front is always the max** — it's the largest element in the window
2. **Back is always the smallest** — elements are added in decreasing order
3. **Elements are removed from back when dominated** — a larger, newer element makes older smaller elements irrelevant
4. **Elements are removed from front when out of window** — sliding window constraint

Each element is added exactly once and removed at most once → **O(n) total**.

---

## Why Deque and Not Stack?

A stack only allows access from the top. We need to:
- **Remove from the front** (out-of-window elements) — stack can't do this
- **Remove from the back** (dominated elements) — stack can do this
- **Peek the front** (current max) — stack can't do this

Deque allows both ends. Stack only allows one.

---

## Edge Cases

```java
// k == 1: every element is its own max
// k == n: result is one element (global max)
// All equal elements: deque maintains all indices (no removals from back)
// Strictly increasing: deque always has 1 element (front = current max)
// Strictly decreasing: deque has all k elements (front = first in window)
```

---

## Complexity

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(nk) | O(1) |
| Max Heap | O(n log k) | O(k) |
| **Monotonic Deque** | **O(n)** | **O(k)** |

The deque approach is optimal. You can't do better than O(n) since you must look at every element at least once.

---

## Key Takeaways

1. **Monotonic decreasing deque** of indices solves sliding window max
2. **Remove from back** when current element is larger (dominated elements)
3. **Remove from front** when index falls out of window
4. **Front of deque is always the answer** for the current window
5. **O(n) time, O(k) space** — optimal for this problem
6. **This pattern extends** to sliding window min (use increasing deque), sliding window median, and more

This is one of the top 5 most-asked deque problems in interviews. Master it.
