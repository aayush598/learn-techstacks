# Segment Tree

## Why Segment Tree?

Suppose you have an array and need to support two operations frequently:
1. **Range query**: What's the sum/min/max of elements in range [l, r]?
2. **Point update**: Change one element's value.

With a plain array: Query is O(n), Update is O(1). With prefix sums: Query is O(1), Update is O(n). Neither is great when both are frequent. **Segment tree gives O(log n) for both!**

## Core Idea

A segment tree is a **perfect binary tree** stored in an array where:
- Each leaf represents a single element
- Each internal node represents a range/segment
- The root represents the entire array [0, n-1]

```
Array: [1, 3, 5, 7, 9, 11]

Segment Tree (for sum):
              [0,5] = 36
             /        \
        [0,2]=9      [3,5]=27
       /     \       /     \
    [0,1]=4 [2,2]=5 [3,4]=16 [5,5]=11
    /    \
 [0,0]=1 [1,1]=3
```

## Array Representation

For a node at index `i`:
- **Left child**: `2*i`
- **Right child**: `2*i + 1`
- **Parent**: `i/2`

We allocate **4*n** space to be safe (the tree needs at most 4*n nodes).

```java
class SegmentTree {
    private int[] tree;
    private int n;

    public SegmentTree(int[] nums) {
        this.n = nums.length;
        this.tree = new int[4 * n];
        build(nums, 1, 0, n - 1);
    }

    // Build the segment tree recursively
    // node: current node index in tree array
    // start, end: the range [start, end] this node covers
    private void build(int[] nums, int node, int start, int end) {
        if (start == end) {
            // Leaf node — store the element directly
            tree[node] = nums[start];
            return;
        }

        int mid = start + (end - start) / 2;

        // Build left child (covers [start, mid])
        build(nums, 2 * node, start, mid);

        // Build right child (covers [mid+1, end])
        build(nums, 2 * node + 1, mid + 1, end);

        // Internal node = combine children
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
}
```

## Range Sum Query

```java
class RangeSumSegmentTree {
    private int[] tree;
    private int n;

    public RangeSumSegmentTree(int[] nums) {
        this.n = nums.length;
        this.tree = new int[4 * n];
        build(nums, 1, 0, n - 1);
    }

    private void build(int[] nums, int node, int start, int end) {
        if (start == end) {
            tree[node] = nums[start];
            return;
        }

        int mid = start + (end - start) / 2;
        build(nums, 2 * node, start, mid);
        build(nums, 2 * node + 1, mid + 1, end);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }

    // Query sum of range [l, r]
    public int query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }

    private int query(int node, int start, int end, int l, int r) {
        // Case 1: Range completely outside → contribute nothing
        if (r < start || end < l) {
            return 0; // Identity element for sum
        }

        // Case 2: Range completely inside → return this node's value
        if (l <= start && end <= r) {
            return tree[node];
        }

        // Case 3: Partial overlap → recurse both children
        int mid = start + (end - start) / 2;
        int leftSum = query(2 * node, start, mid, l, r);
        int rightSum = query(2 * node + 1, mid + 1, end, l, r);

        return leftSum + rightSum;
    }

    // Update element at index idx to val
    public void update(int idx, int val) {
        update(1, 0, n - 1, idx, val);
    }

    private void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            // Leaf node — update directly
            tree[node] = val;
            return;
        }

        int mid = start + (end - start) / 2;

        if (idx <= mid) {
            update(2 * node, start, mid, idx, val);
        } else {
            update(2 * node + 1, mid + 1, end, idx, val);
        }

        // Propagate the change upward
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
}
```

## The Three Cases Explained

```
Query range [l, r] on node covering [start, end]:

Case 1: NO OVERLAP (r < start OR end < l)
   [start...end]
                 [l...r]
   → Return identity (0 for sum, +∞ for min, -∞ for max)

Case 2: TOTAL OVERLAP (l <= start AND end <= r)
              [start...end]
          [l..............r]
   → Return tree[node]

Case 3: PARTIAL OVERLAP (neither case 1 nor case 2)
      [start...end]
            [l...r]
   → Recurse to both children, combine results
```

## Range Minimum Query (RMQ)

Just change the combination from `+` to `Math.min`:

```java
class RMQSegmentTree {
    private int[] tree;
    private int n;

    public RMQSegmentTree(int[] nums) {
        this.n = nums.length;
        this.tree = new int[4 * n];
        build(nums, 1, 0, n - 1);
    }

    private void build(int[] nums, int node, int start, int end) {
        if (start == end) {
            tree[node] = nums[start];
            return;
        }

        int mid = start + (end - start) / 2;
        build(nums, 2 * node, start, mid);
        build(nums, 2 * node + 1, mid + 1, end);
        tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    }

    public int query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }

    private int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) {
            return Integer.MAX_VALUE; // Identity for min
        }

        if (l <= start && end <= r) {
            return tree[node];
        }

        int mid = start + (end - start) / 2;
        int leftMin = query(2 * node, start, mid, l, r);
        int rightMin = query(2 * node + 1, mid + 1, end, l, r);

        return Math.min(leftMin, rightMin);
    }

    public void update(int idx, int val) {
        update(1, 0, n - 1, idx, val);
    }

    private void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }

        int mid = start + (end - start) / 2;
        if (idx <= mid) {
            update(2 * node, start, mid, idx, val);
        } else {
            update(2 * node + 1, mid + 1, end, idx, val);
        }

        tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    }
}
```

## Generic Segment Tree (Any Operation)

```java
class GenericSegmentTree {
    private int[] tree;
    private int n;
    private java.util.function.BinaryIntegerOperator combine;

    // Functional interface for combining two values
    @FunctionalInterface
    interface BinaryIntegerOperator {
        int apply(int a, int b);
    }

    public GenericSegmentTree(int[] nums, BinaryIntegerOperator combineOp) {
        this.n = nums.length;
        this.tree = new int[4 * n];
        this.combine = combineOp;
        build(nums, 1, 0, n - 1);
    }

    private void build(int[] nums, int node, int start, int end) {
        if (start == end) {
            tree[node] = nums[start];
            return;
        }
        int mid = start + (end - start) / 2;
        build(nums, 2 * node, start, mid);
        build(nums, 2 * node + 1, mid + 1, end);
        tree[node] = combine.apply(tree[2 * node], tree[2 * node + 1]);
    }

    public int query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }

    private int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];

        int mid = start + (end - start) / 2;
        int leftResult = query(2 * node, start, mid, l, r);
        int rightResult = query(2 * node + 1, mid + 1, end, l, r);

        return combine.apply(leftResult, rightResult);
    }

    public void update(int idx, int val) {
        update(1, 0, n - 1, idx, val);
    }

    private void update(int node, int start, int end, int idx, int val) {
        if (start == end) {
            tree[node] = val;
            return;
        }
        int mid = start + (end - start) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, val);
        else update(2 * node + 1, mid + 1, end, idx, val);

        tree[node] = combine.apply(tree[2 * node], tree[2 * node + 1]);
    }
}

// Usage:
// int[] arr = {1, 3, 5, 7, 9};
// var sumTree = new GenericSegmentTree(arr, (a, b) -> a + b);
// var minTree = new GenericSegmentTree(arr, Integer::min);
// var maxTree = new GenericSegmentTree(arr, Integer::max);
// var gcdTree = new GenericSegmentTree(arr, (a, b) -> gcd(a, b));
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| Build | O(n) | O(4n) |
| Query | O(log n) | O(1) |
| Update | O(log n) | O(1) |

## When to Use Segment Tree

- Range queries + point updates
- Need to support different operations (sum, min, max, gcd)
- Array size up to ~10^5
- Need range updates → use lazy propagation variant

## Common Mistakes

1. **Array size**: Always allocate 4*n. The actual tree can use up to ~4*n nodes
2. **Index out of bounds**: Be careful with 0-indexed vs 1-indexed node numbering
3. **Identity element**: Wrong identity breaks queries. Sum→0, Min→+∞, Max→-∞, GCD→0
4. **Off-by-one errors**: The mid split should be `[start, mid]` and `[mid+1, end]`
