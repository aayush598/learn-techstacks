# Range Query Problems

## Problem 1: Range Sum Query — Mutable (LeetCode 307)

Use a Fenwick Tree or Segment Tree for O(log n) update and query.

```java
class NumArray {
    private FenwickTree bit;

    public NumArray(int[] nums) {
        bit = new FenwickTree(nums.length);
        for (int i = 0; i < nums.length; i++) {
            bit.add(i + 1, nums[i]);
        }
    }

    public void update(int index, int val) {
        int current = bit.rangeSum(index + 1, index + 1);
        bit.add(index + 1, val - current);
    }

    public int sumRange(int left, int right) {
        return bit.rangeSum(left + 1, right + 1);
    }

    // Inner Fenwick Tree class
    private static class FenwickTree {
        int[] tree;
        int n;

        FenwickTree(int size) {
            this.n = size;
            this.tree = new int[n + 1];
        }

        void add(int index, int delta) {
            while (index <= n) {
                tree[index] += delta;
                index += index & (-index);
            }
        }

        int sum(int index) {
            int result = 0;
            while (index > 0) {
                result += tree[index];
                index -= index & (-index);
            }
            return result;
        }

        int rangeSum(int l, int r) {
            return sum(r) - sum(l - 1);
        }
    }
}
```

## Problem 2: Count of Smaller Numbers After Self (LeetCode 315)

Use BIT with coordinate compression.

```java
class CountSmaller {
    public List<Integer> countSmaller(int[] nums) {
        int n = nums.length;
        int[] result = new int[n];

        // Coordinate compression: map values to ranks
        int[] sorted = nums.clone();
        Arrays.sort(sorted);
        Map<Integer, Integer> rank = new HashMap<>();
        int r = 1;
        for (int val : sorted) {
            if (!rank.containsKey(val)) {
                rank.put(val, r++);
            }
        }

        // BIT for counting (size = number of unique values)
        FenwickTree bit = new FenwickTree(r);

        // Process from right to left
        for (int i = n - 1; i >= 0; i--) {
            int rankVal = rank.get(nums[i]);
            // Count numbers with rank < rankVal (smaller numbers)
            result[i] = bit.sum(rankVal - 1);
            // Add current number to BIT
            bit.add(rankVal, 1);
        }

        List<Integer> res = new ArrayList<>();
        for (int val : result) {
            res.add(val);
        }
        return res;
    }

    private static class FenwickTree {
        int[] tree;
        int n;

        FenwickTree(int size) {
            this.n = size;
            this.tree = new int[n + 1];
        }

        void add(int index, int delta) {
            while (index <= n) {
                tree[index] += delta;
                index += index & (-index);
            }
        }

        int sum(int index) {
            int result = 0;
            while (index > 0) {
                result += tree[index];
                index -= index & (-index);
            }
            return result;
        }
    }
}
```

## Problem 3: Reverse Pairs (LeetCode 493)

Count pairs (i, j) where i < j and nums[i] > 2 * nums[j].

```java
class ReversePairs {
    public int reversePairs(int[] nums) {
        if (nums == null || nums.length <= 1) return 0;
        return mergeSortCount(nums, 0, nums.length - 1);
    }

    private int mergeSortCount(int[] nums, int left, int right) {
        if (left >= right) return 0;

        int mid = left + (right - left) / 2;
        int count = mergeSortCount(nums, left, mid)
                  + mergeSortCount(nums, mid + 1, right);

        // Count reverse pairs crossing the split
        int j = mid + 1;
        for (int i = left; i <= mid; i++) {
            while (j <= right && (long) nums[i] > 2L * nums[j]) {
                j++;
            }
            count += j - (mid + 1);
        }

        // Merge (standard merge sort)
        int[] temp = new int[right - left + 1];
        int p = left, q = mid + 1, k = 0;
        while (p <= mid && q <= right) {
            if (nums[p] <= nums[q]) temp[k++] = nums[p++];
            else temp[k++] = nums[q++];
        }
        while (p <= mid) temp[k++] = nums[p++];
        while (q <= right) temp[k++] = nums[q++];

        System.arraycopy(temp, 0, nums, left, right - left + 1);
        return count;
    }
}
```

## Problem 4: Range Minimum Query (Segment Tree)

```java
class RMQ {
    private int[] tree;
    private int n;

    public RMQ(int[] nums) {
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
        if (r < start || end < l) return Integer.MAX_VALUE;
        if (l <= start && end <= r) return tree[node];

        int mid = start + (end - start) / 2;
        return Math.min(
            query(2 * node, start, mid, l, r),
            query(2 * node + 1, mid + 1, end, l, r)
        );
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
        tree[node] = Math.min(tree[2 * node], tree[2 * node + 1]);
    }
}
```

## Problem 5: My Calendar I (LeetCode 729)

Use TreeMap for O(log n) booking check.

```java
class MyCalendar {
    private TreeMap<Integer, Integer> bookings;

    public MyCalendar() {
        bookings = new TreeMap<>();
    }

    public boolean book(int start, int end) {
        // Find the event that starts just before or at start
        Map.Entry<Integer, Integer> prev = bookings.floorEntry(start);

        // Check if it overlaps with previous event
        if (prev != null && prev.getValue() > start) {
            return false;
        }

        // Find the event that starts just after start
        Map.Entry<Integer, Integer> next = bookings.ceilingEntry(start);

        // Check if it overlaps with next event
        if (next != null && next.getKey() < end) {
            return false;
        }

        bookings.put(start, end);
        return true;
    }
}
```

## Problem 6: My Calendar II (LeetCode 731)

Track double-booked intervals separately.

```java
class MyCalendarTwo {
    private TreeMap<Integer, Integer> bookings;
    private TreeMap<Integer, Integer> doubleBookings;

    public MyCalendarTwo() {
        bookings = new TreeMap<>();
        doubleBookings = new TreeMap<>();
    }

    public boolean book(int start, int end) {
        // Check if this would create a triple booking
        Map.Entry<Integer, Integer> prev = doubleBookings.floorEntry(start);
        if (prev != null && prev.getValue() > start) return false;

        Map.Entry<Integer, Integer> next = doubleBookings.ceilingEntry(start);
        if (next != null && next.getKey() < end) return false;

        // Add to double bookings where overlap exists
        addBooking(bookings, doubleBookings, start, end);

        // Add to regular bookings
        addBooking(bookings, new TreeMap<>(), start, end);

        return true;
    }

    private void addBooking(TreeMap<Integer, Integer> main,
                           TreeMap<Integer, Integer> overlap,
                           int start, int end) {
        Map.Entry<Integer, Integer> entry = main.floorEntry(start);

        if (entry != null && entry.getValue() > start) {
            int overlapStart = Math.max(start, entry.getKey());
            int overlapEnd = Math.min(end, entry.getValue());
            overlap.merge(overlapStart, overlapEnd, Integer::max);
        }

        main.merge(start, end, Integer::max);
    }
}
```

## Problem 7: My Calendar III (LeetCode 732)

Count maximum k-booking using difference array + TreeMap.

```java
class MyCalendarThree {
    private TreeMap<Integer, Integer> diff;

    public MyCalendarThree() {
        diff = new TreeMap<>();
    }

    public int book(int start, int end) {
        diff.merge(start, 1, Integer::sum);
        diff.merge(end, -1, Integer::sum);

        int maxBooking = 0;
        int current = 0;

        for (int count : diff.values()) {
            current += count;
            maxBooking = Math.max(maxBooking, current);
        }

        return maxBooking;
    }
}
```

## Problem 8: Range Sum Query 2D — Immutable (LeetCode 304)

Prefix sum matrix for O(1) range sum queries.

```java
class NumMatrix {
    private int[][] prefixSum;

    public NumMatrix(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        prefixSum = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                prefixSum[i][j] = matrix[i-1][j-1]
                    + prefixSum[i-1][j]
                    + prefixSum[i][j-1]
                    - prefixSum[i-1][j-1];
            }
        }
    }

    public int sumRegion(int row1, int col1, int row2, int col2) {
        return prefixSum[row2+1][col2+1]
             - prefixSum[row1][col2+1]
             - prefixSum[row2+1][col1]
             + prefixSum[row1][col1];
    }
}
```

## Summary: Which Data Structure to Use?

| Problem Type | Best Structure | Time |
|-------------|---------------|------|
| Range sum + point update | Fenwick Tree | O(log n) |
| Range sum + range update | Lazy Segment Tree | O(log n) |
| Range min/max + point update | Segment Tree | O(log n) |
| Range min + range update | Lazy Segment Tree | O(log n) |
| 2D Range sum + point update | 2D Fenwick Tree | O(log²n) |
| Count inversions | Fenwick + compression | O(n log n) |
| Interval scheduling | TreeMap | O(n log n) |
