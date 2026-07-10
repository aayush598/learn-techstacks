# Fenwick Tree (Binary Indexed Tree)

## What is a Fenwick Tree?

A Fenwick Tree (also called Binary Indexed Tree or BIT) is a data structure that efficiently supports **prefix sum queries** and **point updates**. It's simpler to implement than a segment tree and uses less memory.

**The magic**: It exploits the binary representation of indices to organize cumulative sums cleverly.

## Why Fenwick Tree Over Segment Tree?

| Feature | Fenwick Tree | Segment Tree |
|---------|-------------|--------------|
| Code complexity | ~20 lines | ~60 lines |
| Space | O(n) | O(4n) |
| Constant factor | Smaller | Larger |
| Range updates | With tricks | Lazy propagation |
| Range min/max | Not directly | Yes |

**Rule of thumb**: If you only need prefix sums + point updates, use Fenwick. If you need range updates or range min/max, use Segment Tree.

## The Key Insight: Binary Representation

Each index `i` is responsible for a range of elements. The range length is determined by the **lowest set bit** of `i`.

```
Index (binary)    Range it stores        Length
1  (001)          tree[1] = arr[1]        1
2  (010)          tree[2] = arr[1]+arr[2] 2
3  (011)          tree[3] = arr[3]        1
4  (100)          tree[4] = arr[1..4]     4
5  (101)          tree[5] = arr[5]        1
6  (110)          tree[6] = arr[5]+arr[6] 2
7  (111)          tree[7] = arr[7]        1
8  (1000)         tree[8] = arr[1..8]     8
```

The **lowest set bit** of `i` (written `i & -i`) determines the range length.

## Implementation

```java
class FenwickTree {
    private int[] tree;
    private int n;

    public FenwickTree(int size) {
        this.n = size;
        this.tree = new int[n + 1]; // 1-indexed
    }

    // Build from array — O(n)
    public FenwickTree(int[] nums) {
        this.n = nums.length;
        this.tree = new int[n + 1];

        for (int i = 0; i < n; i++) {
            add(i + 1, nums[i]); // 1-indexed
        }
    }

    // Add delta to element at index (1-indexed)
    // Update all responsible ranges
    public void add(int index, int delta) {
        while (index <= n) {
            tree[index] += delta;
            index += index & (-index); // move to parent range
        }
    }

    // Prefix sum: sum of elements from 1 to index
    public int sum(int index) {
        int result = 0;
        while (index > 0) {
            result += tree[index];
            index -= index & (-index); // move to next range
        }
        return result;
    }

    // Range sum: sum of elements from l to r (1-indexed)
    public int rangeSum(int l, int r) {
        return sum(r) - sum(l - 1);
    }

    // Update element at index to val (point update)
    public void update(int index, int val) {
        int delta = val - rangeSum(index, index);
        add(index, delta);
    }
}
```

## Visual Walkthrough

```
Array: [1, 3, 5, 7, 9, 11]

Build Fenwick Tree (1-indexed):
arr:    [_, 1, 3, 5, 7, 9, 11]
index:   0  1  2  3  4  5   6

tree[1] = arr[1] = 1           (covers 1)
tree[2] = arr[1] + arr[2] = 4  (covers 1-2)
tree[3] = arr[3] = 5           (covers 3)
tree[4] = arr[1..4] = 16       (covers 1-4)
tree[5] = arr[5] = 9           (covers 5)
tree[6] = arr[5] + arr[6] = 20 (covers 5-6)

Query: sum(4) — prefix sum of first 4 elements
  Start at index 4: result += tree[4] = 16
  4 - (4&-4) = 4 - 4 = 0 → done
  Result: 16 ✓

Query: sum(6) — prefix sum of all 6 elements
  Start at index 6: result += tree[6] = 20
  6 - (6&-6) = 6 - 2 = 4: result += tree[4] = 16 → 36
  4 - (4&-4) = 4 - 4 = 0 → done
  Result: 36 ✓
```

## The Lowbit Function

```java
// The lowest set bit of x
// Example: lowbit(12) = lowbit(1100) = 100 = 4
int lowbit(int x) {
    return x & (-x);
}

// Or equivalently:
int lowbit2(int x) {
    return x & ~(x - 1);
}
```

## 0-indexed Version

```java
class FenwickTree0Indexed {
    private int[] tree;
    private int n;

    public FenwickTree0Indexed(int size) {
        this.n = size;
        this.tree = new int[n];
    }

    // Add delta at index (0-indexed)
    // Internally, tree is 1-indexed but we map i → i+1
    public void add(int index, int delta) {
        int i = index + 1; // convert to 1-indexed
        while (i <= n) {
            tree[i] += delta;
            i += i & (-i);
        }
    }

    // Prefix sum [0, index] inclusive (0-indexed)
    public int sum(int index) {
        int result = 0;
        int i = index + 1; // convert to 1-indexed
        while (i > 0) {
            result += tree[i];
            i -= i & (-i);
        }
        return result;
    }

    // Range sum [l, r] inclusive (0-indexed)
    public int rangeSum(int l, int r) {
        return sum(r) - (l > 0 ? sum(l - 1) : 0);
    }
}
```

## Find Index by Prefix Sum (Binary Search on BIT)

```java
class FenwickTreeWithFind {

    // Find smallest index such that prefix sum >= target
    // This is the "find by order" operation
    public int findByPrefixSum(int target) {
        int idx = 0;
        int bitMask = Integer.highestOneBit(n); // largest power of 2 <= n

        while (bitMask != 0) {
            int nextIdx = idx + bitMask;

            if (nextIdx <= n && tree[nextIdx] < target) {
                idx = nextIdx;
                target -= tree[nextIdx];
            }

            bitMask >>= 1;
        }

        return idx + 1; // 1-indexed result
    }
}
```

## Range Update + Point Query

With a clever trick, we can do range updates (add delta to all elements in [l, r]) and point queries:

```java
class RangeUpdatePointQueryBIT {
    private int[] tree;
    private int n;

    public RangeUpdatePointQueryBIT(int size) {
        this.n = size;
        this.tree = new int[n + 1];
    }

    // Add delta to all elements in range [l, r] (1-indexed)
    public void rangeAdd(int l, int r, int delta) {
        add(l, delta);
        add(r + 1, -delta);
    }

    // Point query: value at index (1-indexed)
    public int pointQuery(int index) {
        int result = 0;
        while (index > 0) {
            result += tree[index];
            index -= index & (-index);
        }
        return result;
    }

    private void add(int index, int delta) {
        while (index <= n) {
            tree[index] += delta;
            index += index & (-index);
        }
    }
}
```

## 2D Fenwick Tree

For 2D range queries (sum of submatrix):

```java
class FenwickTree2D {
    private int[][] tree;
    private int n, m;

    public FenwickTree2D(int n, int m) {
        this.n = n;
        this.m = m;
        this.tree = new int[n + 1][m + 1];
    }

    // Add delta at (x, y) — 1-indexed
    public void add(int x, int y, int delta) {
        for (int i = x; i <= n; i += i & (-i)) {
            for (int j = y; j <= m; j += j & (-j)) {
                tree[i][j] += delta;
            }
        }
    }

    // Prefix sum from (1,1) to (x,y) — 1-indexed
    public int sum(int x, int y) {
        int result = 0;
        for (int i = x; i > 0; i -= i & (-i)) {
            for (int j = y; j > 0; j -= j & (-j)) {
                result += tree[i][j];
            }
        }
        return result;
    }

    // Range sum for rectangle (x1,y1) to (x2,y2) — 1-indexed
    public int rangeSum(int x1, int y1, int x2, int y2) {
        return sum(x2, y2) - sum(x1 - 1, y2) - sum(x2, y1 - 1) + sum(x1 - 1, y1 - 1);
    }
}
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build (from array) | O(n log n) | O(n) |
| Build (optimized) | O(n) | O(n) |
| Point update | O(log n) | O(1) |
| Prefix sum query | O(log n) | O(1) |
| Range sum query | O(log n) | O(1) |
| 2D point update | O(log n * log m) | O(1) |
| 2D prefix sum | O(log n * log m) | O(1) |

## When to Use Fenwick Tree

- Prefix sum queries + point updates
- Counting inversions (with coordinate compression)
- Order statistics (find k-th element)
- 2D range sum queries
- Simple to implement, fast in practice

## Fenwick Tree vs Segment Tree

- **Fenwick**: Simpler, faster constant, O(n) space, limited to sum-like operations
- **Segment Tree**: More flexible, supports range updates (lazy), range min/max, O(4n) space
