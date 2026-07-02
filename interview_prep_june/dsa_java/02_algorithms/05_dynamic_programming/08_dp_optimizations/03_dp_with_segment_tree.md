# DP with Segment Tree

Used when: dp[i] depends on a range query, e.g., dp[i] = max(dp[j]) for j in range.

## Template

```java
int n = nums.length;
int[] dp = new int[n];
int size = maxValue; // or coordinate-compressed value

SegmentTree st = new SegmentTree(size);

for (int i = 0; i < n; i++) {
    // Query max in range [0, nums[i]-1]
    int best = st.query(0, nums[i] - 1);
    dp[i] = best + 1;
    st.update(nums[i], dp[i]);
}

return max(dp);
```

## LIS with Segment Tree

```java
public int lengthOfLIS(int[] nums) {
    // Coordinate compression
    int[] sorted = nums.clone();
    Arrays.sort(sorted);
    Map<Integer, Integer> map = new HashMap<>();
    for (int i = 0; i < sorted.length; i++) {
        map.put(sorted[i], i + 1);
    }

    int n = nums.length;
    int[] bit = new int[n + 2];
    int maxLen = 0;

    for (int num : nums) {
        int idx = map.get(num);
        int best = query(bit, idx - 1); // max in [1, idx-1]
        int len = best + 1;
        update(bit, idx, len);
        maxLen = Math.max(maxLen, len);
    }

    return maxLen;
}

void update(int[] bit, int idx, int val) {
    while (idx < bit.length) {
        bit[idx] = Math.max(bit[idx], val);
        idx += idx & -idx;
    }
}

int query(int[] bit, int idx) {
    int max = 0;
    while (idx > 0) {
        max = Math.max(max, bit[idx]);
        idx -= idx & -idx;
    }
    return max;
}
```

## Common Problems

| Problem | Range Query |
|---|---|
| LIS (O(n log n)) | Max dp for values < current |
| Max Sum with K distance | Max dp[j] for j in [i-K, i-1] |
| Job Scheduling | Max profit for non-conflicting jobs |

## Key Insight

> When dp[i] = max/min(dp[j] + something) and j must satisfy a range condition, a segment tree or Fenwick tree can answer the range query in O(log n).
