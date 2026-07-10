# First Negative in Every Window of Size K

This is a fixed-size sliding window problem that introduces the **Deque (double-ended queue)** pattern. When you need to track the *first* or *maximum* or *minimum* element in a sliding window, think Deque.

## Problem Statement

Given an array and a window size `k`, find the first negative number in every subarray of size `k`. If a window has no negative number, output 0.

```
Input:  arr = [12, -1, -7, 8, -15, 30, 16, 28], k = 3
Output: [-1, -1, -7, -15, -15, 0]

Windows:
[12, -1, -7] → first negative = -1
[-1, -7, 8]  → first negative = -1
[-7, 8, -15] → first negative = -7
[8, -15, 30] → first negative = -15
[-15, 30, 16] → first negative = -15
[30, 16, 28] → first negative = 0 (none)
```

## Brute Force (O(n·k))

```java
public int[] firstNegativeBrute(int[] arr, int k) {
    int n = arr.length;
    int[] result = new int[n - k + 1];

    for (int i = 0; i <= n - k; i++) {
        int firstNegative = 0;
        for (int j = i; j < i + k; j++) {
            if (arr[j] < 0) {
                firstNegative = arr[j];
                break;
            }
        }
        result[i] = firstNegative;
    }

    return result;
}
```

For each window, we scan `k` elements. If `k` is large, this is O(nk). We can do better.

## Deque-Based Solution (O(n))

The key insight: we maintain a deque of indices of negative numbers. When the window slides:
- Remove indices that fell out of the window (from the front)
- Add new negative number indices (to the back)
- The first negative in the window is always at the front

```java
public int[] firstNegativeInWindow(int[] arr, int k) {
    int n = arr.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // Stores indices of negative numbers

    int resultIdx = 0;

    for (int i = 0; i < n; i++) {
        // Remove indices outside the current window
        while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
            deque.pollFirst();
        }

        // If current element is negative, add its index
        if (arr[i] < 0) {
            deque.offerLast(i);
        }

        // If window is formed, record the result
        if (i >= k - 1) {
            if (deque.isEmpty()) {
                result[resultIdx++] = 0;
            } else {
                result[resultIdx++] = arr[deque.peekFirst()];
            }
        }
    }

    return result;
}
```

### What's a Deque?

A Deque (pronounced "deck") is a double-ended queue. You can add/remove from both ends.

```
      pollFirst()          pollLast()
          ↓                    ↓
    ← [--- deque ---] ←
          ↑                    ↑
      offerFirst()          offerLast()
```

### Why Deque?

For this specific problem, we only ever remove from the front and add to the back. A regular `Queue` would work too. But for the more general "sliding window maximum" problem, we need to remove from the back as well (to maintain decreasing order). Using a Deque from the start is good practice.

### Alternative: Just a Queue

```java
public int[] firstNegativeInWindowQueue(int[] arr, int k) {
    int n = arr.length;
    int[] result = new int[n - k + 1];
    Queue<Integer> queue = new LinkedList<>(); // Indices of negative numbers

    for (int i = 0; i < n; i++) {
        if (arr[i] < 0) {
            queue.offer(i);
        }

        if (i >= k - 1) {
            // Remove indices that are out of the window
            while (!queue.isEmpty() && queue.peek() < i - k + 1) {
                queue.poll();
            }
            result[i - k + 1] = queue.isEmpty() ? 0 : arr[queue.peek()];
        }
    }

    return result;
}
```

### Dry Run

```
arr = [12, -1, -7, 8, -15, 30, 16, 28], k = 3

i=0 (arr[0]=12): deque=[], not negative
  i<k-1 (0<2) → no result yet

i=1 (arr[1]=-1): deque=[1], added index 1
  i<k-1 → no result yet

i=2 (arr[2]=-7): deque=[1, 2], added index 2
  i>=k-1 → window formed!
  deque not empty → result[0] = arr[1] = -1

i=3 (arr[3]=8):
  Remove from front: is 1 < 3-3+1=1? No (1 is not < 1)
  deque=[1,2], not negative
  result[1] = arr[1] = -1

i=4 (arr[4]=-15):
  deque=[1,2], then add 4 → deque=[1,2,4]
  Check front: is 1 < 4-3+1=2? Yes → remove 1
  deque=[2,4]
  result[2] = arr[2] = -7

i=5 (arr[5]=30):
  deque=[2,4], not negative
  Check front: is 2 < 5-3+1=3? Yes → remove 2
  deque=[4]
  result[3] = arr[4] = -15

i=6 (arr[6]=16):
  deque=[4], not negative
  Check front: is 4 < 6-3+1=4? No
  result[4] = arr[4] = -15

i=7 (arr[7]=28):
  deque=[4], not negative
  Check front: is 4 < 7-3+1=5? Yes → remove 4
  deque=[]
  result[5] = 0 (empty deque)

Result: [-1, -1, -7, -15, -15, 0] ✓
```

## Generalization: Sliding Window Maximum

The same Deque pattern solves "Maximum in every window of size k":

```java
public int[] maxSlidingWindow(int[] nums, int k) {
    int n = nums.length;
    int[] result = new int[n - k + 1];
    Deque<Integer> deque = new ArrayDeque<>(); // Store indices, decreasing values
    int ri = 0;

    for (int i = 0; i < n; i++) {
        // Remove indices out of window
        while (!deque.isEmpty() && deque.peekFirst() < i - k + 1) {
            deque.pollFirst();
        }

        // Remove smaller elements from back (maintain decreasing order)
        while (!deque.isEmpty() && nums[deque.peekLast()] < nums[i]) {
            deque.pollLast();
        }

        deque.offerLast(i);

        if (i >= k - 1) {
            result[ri++] = nums[deque.peekFirst()];
        }
    }

    return result;
}
```

For sliding window maximum, the deque maintains indices of elements in **decreasing** order of value. The front is always the maximum for the current window.

## Time & Space Complexity

| Solution | Time | Space |
|----------|------|-------|
| Brute Force | O(n·k) | O(1) |
| Deque | O(n) | O(k) |
| Queue | O(n) | O(k) |

Each element is added to the deque once and removed at most once → O(n).

## Interview Tips

1. **Start with brute force** — shows you understand the problem
2. **Introduce the deque** — "we need a data structure that supports removing from both ends"
3. **Explain index management** — "we store indices, not values, to easily check if an element is out of the window"
4. **Mention the generalization** — sliding window maximum/minimum use the same pattern
5. **Edge cases**: empty array, k=1 (result is just the array), k=n (result is a single value), no negatives in array

## Common Mistakes

1. **Storing values instead of indices** — makes it hard to track window boundaries
2. **Forgetting to remove out-of-window indices** — leads to stale values
3. **Using ArrayList and scanning** — defeats the purpose; you need O(1) front/back operations
4. **Not handling empty deque** — check `isEmpty()` before accessing `peekFirst()`

The deque-based sliding window is a powerful pattern. Master it here, and you'll be ready for all "first/max/min in window" problems.
