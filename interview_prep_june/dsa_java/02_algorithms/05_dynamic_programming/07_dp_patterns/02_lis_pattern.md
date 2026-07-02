# LIS Pattern

## When to Use

Look for:
- "Longest increasing/decreasing subsequence"
- "Maximum chain length"
- "Russian doll envelopes" (sort + LIS)
- "Maximum number of events/boxes that can be stacked"

## Derivative Problems

| Problem | Approach |
|---|---|
| LIS | dp[i] = 1 + max(dp[j]) for j < i and arr[j] < arr[i] |
| Russian Doll | Sort by w asc, h desc → LIS on h |
| Max Chain Length | Sort by first element → LIS on second |
| Number of LIS | length[i] + count[i] DP |
| Min Deletions to Make Sorted | n - LIS |

## O(n log n) Template (Length Only)

```java
int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;
    for (int num : nums) {
        int i = Arrays.binarySearch(tails, 0, size, num);
        if (i < 0) i = -(i + 1);
        tails[i] = num;
        if (i == size) size++;
    }
    return size;
}
```

## Key Insight

> LIS O(n log n) uses patience sorting. tails[i] = smallest possible last element of an increasing subsequence of length i+1. Not reconstructable by itself.
