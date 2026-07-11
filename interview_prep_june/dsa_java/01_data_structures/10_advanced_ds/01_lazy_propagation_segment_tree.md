# Lazy Propagation Segment Tree

## Why Lazy Propagation?

Without lazy propagation, range updates are O(n log n). With lazy, range updates are O(log n).

## Implementation: Range Add + Range Sum Query

```java
class LazySegmentTree {
    private long[] tree;
    private long[] lazy;
    private int n;
    
    LazySegmentTree(int[] arr) {
        n = arr.length;
        tree = new long[4 * n];
        lazy = new long[4 * n];
        build(arr, 1, 0, n - 1);
    }
    
    private void build(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }
        int mid = (start + end) / 2;
        build(arr, 2 * node, start, mid);
        build(arr, 2 * node + 1, mid + 1, end);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
    
    private void push(int node, int start, int end) {
        if (lazy[node] != 0) {
            tree[node] += lazy[node] * (end - start + 1);
            
            if (start != end) {  // not a leaf → propagate to children
                lazy[2 * node] += lazy[node];
                lazy[2 * node + 1] += lazy[node];
            }
            
            lazy[node] = 0;
        }
    }
    
    void update(int l, int r, int val) {
        update(1, 0, n - 1, l, r, val);
    }
    
    private void update(int node, int start, int end, int l, int r, int val) {
        push(node, start, end);
        
        if (r < start || end < l) return;  // no overlap
        if (l <= start && end <= r) {       // complete overlap
            lazy[node] += val;
            push(node, start, end);
            return;
        }
        
        // partial overlap
        int mid = (start + end) / 2;
        update(2 * node, start, mid, l, r, val);
        update(2 * node + 1, mid + 1, end, l, r, val);
        tree[node] = tree[2 * node] + tree[2 * node + 1];
    }
    
    long query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }
    
    private long query(int node, int start, int end, int l, int r) {
        push(node, start, end);
        
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        
        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r) + 
               query(2 * node + 1, mid + 1, end, l, r);
    }
}
```

## Complexity

- Build: O(n)
- Range Update: O(log n)
- Range Query: O(log n)
- Space: O(n)
