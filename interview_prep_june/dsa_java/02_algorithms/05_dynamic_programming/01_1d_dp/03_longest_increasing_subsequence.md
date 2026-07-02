# Longest Increasing Subsequence (LIS)

**Problem**: Find the length of the longest strictly increasing subsequence in an array.

**Example**: `nums = [10, 9, 2, 5, 3, 7, 101, 18]` → LIS = 4 `[2, 3, 7, 101]`

---

## O(n²) DP Solution

**State**: `dp[i]` = length of LIS ending at position i
**Recurrence**: `dp[i] = 1 + max(dp[j])` for all `j < i` and `nums[j] < nums[i]`

```java
public int lengthOfLIS(int[] nums) {
    int n = nums.length;
    if (n == 0) return 0;

    int[] dp = new int[n];
    int maxLen = 1;

    for (int i = 0; i < n; i++) {
        dp[i] = 1; // every element is an increasing subsequence of length 1
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }

    return maxLen;
}
```

### Trace for [10, 9, 2, 5, 3, 7, 101, 18]

```
dp[0] (10): 1  → [10]
dp[1] (9):  1  → [9] (no smaller element before it)
dp[2] (2):  1  → [2]
dp[3] (5):  max(1, dp[2]+1=2) = 2 → [2,5]
dp[4] (3):  max(1, dp[2]+1=2) = 2 → [2,3]
dp[5] (7):  max(1, dp[2]+1=2, dp[3]+1=3, dp[4]+1=3) = 3 → [2,5,7] or [2,3,7]
dp[6] (101): max(1, dp[0..5]+1) = 4 → [2,5,7,101] or [2,3,7,101]
dp[7] (18): max(1, dp[2]+1=2, dp[3]+1=3, dp[4]+1=3, dp[5]+1=4) = 4 → [2,5,7,18]

maxLen = 4
```

### Reconstruct LIS

```java
public List<Integer> getLIS(int[] nums) {
    int n = nums.length;
    int[] dp = new int[n];
    int[] prev = new int[n];
    Arrays.fill(prev, -1);

    int maxLen = 0;
    int lastIdx = 0;

    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                prev[i] = j;
            }
        }
        if (dp[i] > maxLen) {
            maxLen = dp[i];
            lastIdx = i;
        }
    }

    // Reconstruct
    List<Integer> lis = new ArrayList<>();
    while (lastIdx != -1) {
        lis.add(0, nums[lastIdx]);
        lastIdx = prev[lastIdx];
    }
    return lis;
}
```

---

## O(n log n) Solution (Patience Sorting)

**Idea**: Maintain an array `tails` where `tails[i]` = the smallest tail of all increasing subsequences of length i+1.

```java
public int lengthOfLIS(int[] nums) {
    int[] tails = new int[nums.length];
    int size = 0;

    for (int num : nums) {
        // Binary search: find first tail >= num
        int left = 0, right = size;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (tails[mid] < num) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        tails[left] = num;
        if (left == size) size++;
    }

    return size;
}
```

### Trace for [10, 9, 2, 5, 3, 7, 101, 18]

```
Processing each number:

10 → tails = [10]           (new sequence of length 1)
 9 → replace 10: [9]        (smaller tail for length 1)
 2 → replace 9:  [2]        (even smaller tail for length 1)
 5 → tails = [2, 5]         (extend: new length 2)
 3 → replace 5:  [2, 3]     (better tail for length 2)
 7 → tails = [2, 3, 7]      (extend: new length 3)
101 → tails = [2, 3, 7, 101] (extend: new length 4)
18 → replace 101: [2, 3, 7, 18] (better tail for length 4)

size = 4
```

**Important**: `tails` does NOT contain the actual LIS. It only tells us the length. The elements in `tails` are the smallest possible tails for each length.

### Why Binary Search Works

For each number, we find the position where it fits in the tails array:
- If it's larger than all tails, we append (new longer subsequence)
- Otherwise, we replace the first tail that's >= it (improving future prospects)

### Why It's Correct

The `tails` array maintains the invariant: `tails[i]` is the smallest possible last element of an increasing subsequence of length i+1. By keeping tails small, we maximize the chance of extending subsequences.

---

## Applications

### Russian Doll Envelopes

**Problem**: Given envelopes with [w, h], place one inside another if both w and h are strictly smaller.

**Approach**: Sort by width ascending, then by height descending. Find LIS of heights.

```java
public int maxEnvelopes(int[][] envelopes) {
    Arrays.sort(envelopes, (a, b) -> a[0] == b[0] ? b[1] - a[1] : a[0] - b[0]);

    int[] heights = new int[envelopes.length];
    for (int i = 0; i < envelopes.length; i++) {
        heights[i] = envelopes[i][1];
    }

    return lengthOfLIS(heights);
}
```

**Key**: Sort by width ascending, but for equal widths, sort by height descending. This prevents nesting envelopes with the same width.

### Maximum Length of Pair Chain

**Problem**: Given pairs [a, b] where a < b, find longest chain of pairs where pair2 can follow pair1 if pair1[1] < pair2[0].

```java
public int findLongestChain(int[][] pairs) {
    Arrays.sort(pairs, (a, b) -> a[0] - b[0]);
    int n = pairs.length;
    int[] dp = new int[n];
    int maxLen = 1;

    for (int i = 0; i < n; i++) {
        dp[i] = 1;
        for (int j = 0; j < i; j++) {
            if (pairs[j][1] < pairs[i][0]) {
                dp[i] = Math.max(dp[i], dp[j] + 1);
            }
        }
        maxLen = Math.max(maxLen, dp[i]);
    }

    return maxLen;
}
```

### Number of LIS

**Problem**: Count the number of longest increasing subsequences.

```java
public int findNumberOfLIS(int[] nums) {
    int n = nums.length;
    int[] length = new int[n]; // LIS length ending at i
    int[] count = new int[n];  // number of LIS ending at i

    int maxLen = 0;
    int result = 0;

    for (int i = 0; i < n; i++) {
        length[i] = 1;
        count[i] = 1;

        for (int j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                if (length[j] + 1 > length[i]) {
                    length[i] = length[j] + 1;
                    count[i] = count[j];
                } else if (length[j] + 1 == length[i]) {
                    count[i] += count[j];
                }
            }
        }

        if (length[i] > maxLen) {
            maxLen = length[i];
            result = count[i];
        } else if (length[i] == maxLen) {
            result += count[i];
        }
    }

    return result;
}
```

### Minimum Number of Increasing Subsequences

Equivalent to: find the size of the longest **non-increasing** subsequence (Dilworth's theorem).

Or: the minimum number of increasing subsequences needed to partition the array = length of LDS (longest decreasing subsequence).

---

## Complexity

| Approach | Time | Space | Notes |
|---|---|---|---|
| DP O(n²) | O(n²) | O(n) | Simple, reconstructable |
| Patience Sorting | O(n log n) | O(n) | Length only, not reconstructable |

## Key Patterns

### Identifying LIS Problems

Look for:
- "Increasing", "growing", "chain"
- "Maximum length" of something that must be ordered
- Pair/envelope problems

### The O(n log n) Trick

Use patience sorting when:
- n is large (> 10,000)
- Only the length is needed
- The input can be transformed into a 1D LIS problem

### When O(n²) Is Fine

- n ≤ 5000 (O(n²) ≈ 25 million operations)
- Need to reconstruct the actual LIS
- Additional constraints (like counting) are needed
