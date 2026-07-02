# 10 Problems, One Pattern — 5 Patterns, 50 Problems

## Pattern A: Sliding Window — 10 Problems

### 1. Maximum Sum Subarray of Size K
**Problem:** Given an array and integer k, find max sum of any contiguous subarray of size k.
**Approach:** Fixed window. Maintain sum, slide one element at a time.

```java
public int maxSumSubarray(int[] arr, int k) {
    int sum = 0;
    for (int i = 0; i < k; i++) sum += arr[i];
    int maxSum = sum;
    for (int i = k; i < arr.length; i++) {
        sum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, sum);
    }
    return maxSum;
}
```

### 2. Longest Substring Without Repeating Characters
**Problem:** Find longest substring without repeating characters.
**Approach:** Variable window. Expand right, when duplicate found, move left past the duplicate.
```java
public int lengthOfLongestSubstring(String s) {
    int[] freq = new int[128];
    int left = 0, maxLen = 0;
    for (int right = 0; right < s.length(); right++) {
        freq[s.charAt(right)]++;
        while (freq[s.charAt(right)] > 1) {
            freq[s.charAt(left)]--;
            left++;
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

### 3. Minimum Window Substring
**Problem:** Find minimum window in s that contains all characters of t.
**Approach:** Expand until all chars in t are covered, then contract to minimize.
```java
public String minWindow(String s, String t) {
    int[] need = new int[128];
    for (char c : t.toCharArray()) need[c]++;
    int required = t.length(), left = 0, start = 0, minLen = Integer.MAX_VALUE;
    for (int right = 0; right < s.length(); right++) {
        if (need[s.charAt(right)]-- > 0) required--;
        while (required == 0) {
            if (right - left + 1 < minLen) {
                minLen = right - left + 1;
                start = left;
            }
            if (++need[s.charAt(left)] > 0) required++;
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? "" : s.substring(start, start + minLen);
}
```

### 4. Find All Anagrams in a String
**Problem:** Find start indices of all anagrams of p in s.
**Approach:** Fixed window of size p.length(), compare frequency arrays.
```java
public List<Integer> findAnagrams(String s, String p) {
    List<Integer> result = new ArrayList<>();
    if (s.length() < p.length()) return result;
    int[] need = new int[26], have = new int[26];
    for (char c : p.toCharArray()) need[c - 'a']++;
    for (int i = 0; i < s.length(); i++) {
        have[s.charAt(i) - 'a']++;
        if (i >= p.length()) have[s.charAt(i - p.length()) - 'a']--;
        if (i >= p.length() - 1 && Arrays.equals(need, have)) result.add(i - p.length() + 1);
    }
    return result;
}
```

### 5. Maximum Number of Occurrences of a Substring
**Problem:** Given constraints on minSize, maxSize, maxLetters — find max frequency substring.
**Approach:** Only minSize matters (any larger includes smaller). Sliding window of size minSize.
```java
public int maxFreq(String s, int maxLetters, int minSize, int maxSize) {
    Map<String, Integer> freq = new HashMap<>();
    int[] count = new int[26];
    int unique = 0, max = 0;
    for (int i = 0; i < s.length(); i++) {
        if (count[s.charAt(i) - 'a']++ == 0) unique++;
        if (i >= minSize) {
            if (--count[s.charAt(i - minSize) - 'a'] == 0) unique--;
        }
        if (i >= minSize - 1 && unique <= maxLetters) {
            String sub = s.substring(i - minSize + 1, i + 1);
            freq.put(sub, freq.getOrDefault(sub, 0) + 1);
            max = Math.max(max, freq.get(sub));
        }
    }
    return max;
}
```

### 6. Max Consecutive Ones III
**Problem:** Flip at most k 0s to 1s, find longest consecutive 1s.
**Approach:** Variable window tracking zero count.
```java
public int longestOnes(int[] nums, int k) {
    int left = 0, zeroCount = 0, maxLen = 0;
    for (int right = 0; right < nums.length; right++) {
        if (nums[right] == 0) zeroCount++;
        while (zeroCount > k) {
            if (nums[left] == 0) zeroCount--;
            left++;
        }
        maxLen = Math.max(maxLen, right - left + 1);
    }
    return maxLen;
}
```

### 7. Fruit Into Baskets
**Problem:** Longest subarray with at most 2 distinct numbers.
**Approach:** Variable window with HashMap counting distinct.
```java
public int totalFruit(int[] fruits) {
    Map<Integer, Integer> count = new HashMap<>();
    int left = 0, max = 0;
    for (int right = 0; right < fruits.length; right++) {
        count.put(fruits[right], count.getOrDefault(fruits[right], 0) + 1);
        while (count.size() > 2) {
            count.put(fruits[left], count.get(fruits[left]) - 1);
            if (count.get(fruits[left]) == 0) count.remove(fruits[left]);
            left++;
        }
        max = Math.max(max, right - left + 1);
    }
    return max;
}
```

### 8. Longest Substring with At Most K Distinct Characters
**Problem:** Find longest substring with at most k distinct chars.
**Approach:** Similar to Fruit Baskets, but k instead of 2.

### 9. Minimum Size Subarray Sum
**Problem:** Find minimum subarray length with sum ≥ target.
**Approach:** Expand right until sum ≥ target, then contract left while maintaining condition.
```java
public int minSubArrayLen(int target, int[] nums) {
    int left = 0, sum = 0, minLen = Integer.MAX_VALUE;
    for (int right = 0; right < nums.length; right++) {
        sum += nums[right];
        while (sum >= target) {
            minLen = Math.min(minLen, right - left + 1);
            sum -= nums[left];
            left++;
        }
    }
    return minLen == Integer.MAX_VALUE ? 0 : minLen;
}
```

### 10. Subarray Product Less Than K
**Problem:** Count subarrays where product of all elements < k.
**Approach:** Sliding window, for each right, count = right - left + 1 new subarrays ending at right.
```java
public int numSubarrayProductLessThanK(int[] nums, int k) {
    if (k <= 1) return 0;
    int left = 0, product = 1, count = 0;
    for (int right = 0; right < nums.length; right++) {
        product *= nums[right];
        while (product >= k) product /= nums[left++];
        count += right - left + 1;
    }
    return count;
}
```

---

## Pattern B: Binary Search on Answer — 10 Problems

### 1. Aggressive Cows
**Problem:** Place k cows in stalls to maximize the minimum distance between them.
**Approach:** Binary search on distance, check if feasible.

```java
boolean canPlace(int[] stalls, int k, int minDist) {
    int count = 1, last = stalls[0];
    for (int i = 1; i < stalls.length; i++) {
        if (stalls[i] - last >= minDist) {
            count++;
            last = stalls[i];
            if (count >= k) return true;
        }
    }
    return false;
}
```

### 2. Book Allocation (Allocate Minimum Number of Pages)
**Problem:** Allocate books to m students, minimize max pages.
**Approach:** Binary search on max pages, check if allocation is possible.

### 3. Split Array Largest Sum
**Problem:** Split array into k subarrays to minimize the largest sum.
**Approach:** Same as book allocation, binary search on max sum.
```java
public int splitArray(int[] nums, int k) {
    int left = 0, right = 0;
    for (int num : nums) {
        left = Math.max(left, num);
        right += num;
    }
    while (left < right) {
        int mid = left + (right - left) / 2;
        if (canSplit(nums, k, mid)) right = mid;
        else left = mid + 1;
    }
    return left;
}
boolean canSplit(int[] nums, int k, int maxSum) {
    int count = 1, sum = 0;
    for (int num : nums) {
        sum += num;
        if (sum > maxSum) {
            count++;
            sum = num;
            if (count > k) return false;
        }
    }
    return true;
}
```

### 4. Koko Eating Bananas
**Problem:** Koko eats piles[i] bananas per hour. Find min speed to eat all in H hours.
**Approach:** Binary search on speed [1, max(piles)].
```java
public int minEatingSpeed(int[] piles, int h) {
    int left = 1, right = 0;
    for (int p : piles) right = Math.max(right, p);
    while (left < right) {
        int mid = left + (right - left) / 2;
        int hours = 0;
        for (int p : piles) hours += (p + mid - 1) / mid;
        if (hours <= h) right = mid;
        else left = mid + 1;
    }
    return left;
}
```

### 5. Minimum Speed to Arrive on Time
**Problem:** Find min speed to reach destination within hour.
**Approach:** Binary search on speed, check total time ≤ hour.

### 6. Nth Root of an Integer
**Problem:** Find nth root of m, accurate to d decimal places.
**Approach:** Binary search on answer [1, m], check mid^n ≤ m.

### 7. Capacity to Ship Packages Within D Days
**Problem:** Ship packages in D days, minimize ship capacity.
**Approach:** Binary search on capacity between max(weights) and sum(weights).

### 8. Smallest Divisor Given a Threshold
**Problem:** Find smallest divisor such that sum of ceil(nums[i]/div) ≤ threshold.
**Approach:** Binary search on divisor [1, max(nums)].

### 9. Magnetic Force Between Two Balls
**Problem:** Place m balls in positions to maximize minimum magnetic force.
**Approach:** Same as aggressive cows, binary search on min distance.

### 10. Kth Smallest Element in a Sorted Matrix
**Problem:** Find kth smallest element in n×n matrix where rows and cols are sorted.
**Approach:** Binary search on value range [matrix[0][0], matrix[n-1][n-1]].
```java
public int kthSmallest(int[][] matrix, int k) {
    int n = matrix.length;
    int left = matrix[0][0], right = matrix[n-1][n-1];
    while (left < right) {
        int mid = left + (right - left) / 2;
        int count = 0, j = n - 1;
        for (int i = 0; i < n; i++) {
            while (j >= 0 && matrix[i][j] > mid) j--;
            count += j + 1;
        }
        if (count >= k) right = mid;
        else left = mid + 1;
    }
    return left;
}
```

---

## Pattern C: 0/1 Knapsack (Subset DP) — 10 Problems

### 1. Subset Sum
**Problem:** Does there exist a subset with sum = target?
**Approach:** 0/1 knapsack (boolean DP).
```java
boolean subsetSum(int[] nums, int target) {
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int num : nums) {
        for (int w = target; w >= num; w--) {
            dp[w] = dp[w] || dp[w - num];
        }
    }
    return dp[target];
}
```

### 2. Partition Equal Subset Sum
**Problem:** Can array be partitioned into two subsets with equal sum?
**Approach:** target = sum/2, check subset sum.

### 3. Target Sum (+/- Assignment)
**Problem:** Assign + or - to each element to reach target.
**Approach:** sum(P) - sum(N) = target → sum(P) = (target + totalSum)/2. Count ways.
```java
public int findTargetSumWays(int[] nums, int target) {
    int sum = 0;
    for (int num : nums) sum += num;
    if (target > sum || (target + sum) % 2 != 0) return 0;
    int s = (target + sum) / 2;
    int[] dp = new int[s + 1];
    dp[0] = 1;
    for (int num : nums) {
        for (int w = s; w >= num; w--) {
            dp[w] += dp[w - num];
        }
    }
    return dp[s];
}
```

### 4. Ones and Zeroes
**Problem:** Find max size of subset with at most m 0's and n 1's.
**Approach:** 2D 0/1 knapsack (m = capacity dimension 1, n = capacity dimension 2).

### 5. Last Stone Weight II
**Problem:** Smash stones, minimize remaining weight.
**Approach:** target = sum/2, find max achievable ≤ target. Answer = sum - 2*maxAchievable.
```java
public int lastStoneWeightII(int[] stones) {
    int sum = 0;
    for (int s : stones) sum += s;
    int target = sum / 2;
    boolean[] dp = new boolean[target + 1];
    dp[0] = true;
    for (int stone : stones) {
        for (int w = target; w >= stone; w--) {
            dp[w] = dp[w] || dp[w - stone];
        }
    }
    int max = 0;
    for (int w = target; w >= 0; w--) {
        if (dp[w]) { max = w; break; }
    }
    return sum - 2 * max;
}
```

### 6. Minimum Subset Sum Difference
**Problem:** Partition array into two subsets to minimize absolute sum difference.
**Approach:** Same as Last Stone Weight II.

### 7. Count Subsets with Given Sum
**Problem:** Count number of subsets with sum = target.
**Approach:** Same as subset sum but count ways.

### 8. Number of Ways to Wear Different Hats
**Problem:** Assign hats to people, each person gets 1 hat, each hat can be used at most once.
**Approach:** Bitmask DP (subset dp with people as bitmask).

### 9. Maximum Profit in Job Scheduling
**Problem:** Schedule non-overlapping jobs to maximize profit.
**Approach:** Sort by end, DP + binary search for last non-conflicting (similar to knapsack).

### 10. Minimum Cost for Tickets
**Problem:** Minimum cost to cover travel days with 1-day, 7-day, 30-day passes.
**Approach:** DP on days, similar to unbounded knapsack.

---

## Pattern D: Topological Sort — 10 Problems

### 1. Course Schedule I
**Problem:** Can all courses be completed given prerequisites?
**Approach:** Check if graph has cycle using Kahn's algorithm.
```java
public boolean canFinish(int numCourses, int[][] prerequisites) {
    List<Integer>[] adj = new List[numCourses];
    int[] indegree = new int[numCourses];
    for (int i = 0; i < numCourses; i++) adj[i] = new ArrayList<>();
    for (int[] p : prerequisites) {
        adj[p[1]].add(p[0]);
        indegree[p[0]]++;
    }
    Queue<Integer> queue = new LinkedList<>();
    for (int i = 0; i < numCourses; i++)
        if (indegree[i] == 0) queue.offer(i);
    int count = 0;
    while (!queue.isEmpty()) {
        int u = queue.poll();
        count++;
        for (int v : adj[u]) {
            if (--indegree[v] == 0) queue.offer(v);
        }
    }
    return count == numCourses;
}
```

### 2. Course Schedule II
**Problem:** Return order of courses to take all.
**Approach:** Kahn's algorithm, collect order.

### 3. Alien Dictionary
**Problem:** Given sorted words in alien language, find character order.
**Approach:** Compare adjacent words, build graph, topological sort.

### 4. Sequence Reconstruction
**Problem:** Is seq the only shortest supersequence of orgs?
**Approach:** Topological sort, check if only one node with indegree 0 at each step.

### 5. Parallel Courses
**Problem:** Minimum semesters to take all courses (can take any number per semester).
**Approach:** Topological sort by levels (BFS level tracking).

### 6. Minimum Height Trees
**Problem:** Find roots that minimize height of tree.
**Approach:** Topologically remove leaves until 1-2 nodes remain.
```java
public List<Integer> findMinHeightTrees(int n, int[][] edges) {
    if (n == 1) return Arrays.asList(0);
    List<Integer>[] adj = new List[n];
    int[] degree = new int[n];
    for (int i = 0; i < n; i++) adj[i] = new ArrayList<>();
    for (int[] e : edges) {
        adj[e[0]].add(e[1]); adj[e[1]].add(e[0]);
        degree[e[0]]++; degree[e[1]]++;
    }
    Queue<Integer> leaves = new LinkedList<>();
    for (int i = 0; i < n; i++)
        if (degree[i] == 1) leaves.offer(i);
    int remaining = n;
    while (remaining > 2) {
        int size = leaves.size();
        remaining -= size;
        for (int i = 0; i < size; i++) {
            int leaf = leaves.poll();
            for (int neighbor : adj[leaf]) {
                if (--degree[neighbor] == 1) leaves.offer(neighbor);
            }
        }
    }
    return new ArrayList<>(leaves);
}
```

### 7. Find All Possible Recipes from Given Supplies
**Problem:** Given recipes, ingredients, and supplies, find all recipes you can make.
**Approach:** Graph with recipe → ingredients, topological sort.

### 8. Longest Increasing Path in a Matrix
**Problem:** Find longest strictly increasing path in matrix moving 4-directionally.
**Approach:** DP with DFS and memoization (topological DP on DAG).

### 9. Sort Items by Groups Respecting Dependencies
**Problem:** Complex dependency sorting with items and groups.
**Approach:** Two levels of topological sort (groups then items within groups).

### 10. Build a Matrix With Conditions
**Problem:** Given row and column conditions, build matrix.
**Approach:** Topological sort for rows and columns separately.

---

## Pattern E: Merge Intervals — 10 Problems

### 1. Merge Intervals
**Problem:** Merge all overlapping intervals.
**Approach:** Sort by start, merge if overlapping.
```java
public int[][] merge(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    List<int[]> merged = new ArrayList<>();
    int[] current = intervals[0];
    for (int i = 1; i < intervals.length; i++) {
        if (current[1] >= intervals[i][0]) {
            current[1] = Math.max(current[1], intervals[i][1]);
        } else {
            merged.add(current);
            current = intervals[i];
        }
    }
    merged.add(current);
    return merged.toArray(new int[merged.size()][]);
}
```

### 2. Insert Interval
**Problem:** Insert new interval into sorted non-overlapping intervals, merge if needed.
**Approach:** Add all intervals before new, merge overlapping, add after.
```java
public int[][] insert(int[][] intervals, int[] newInterval) {
    List<int[]> result = new ArrayList<>();
    int i = 0, n = intervals.length;
    while (i < n && intervals[i][1] < newInterval[0]) result.add(intervals[i++]);
    while (i < n && intervals[i][0] <= newInterval[1]) {
        newInterval[0] = Math.min(newInterval[0], intervals[i][0]);
        newInterval[1] = Math.max(newInterval[1], intervals[i][1]);
        i++;
    }
    result.add(newInterval);
    while (i < n) result.add(intervals[i++]);
    return result.toArray(new int[result.size()][]);
}
```

### 3. Meeting Rooms (Leetcode 252) — Can Attend All?
**Problem:** Can a person attend all meetings?
**Approach:** Sort by start, check if any overlap.
```java
public boolean canAttendMeetings(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[0] - b[0]);
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i-1][1] > intervals[i][0]) return false;
    }
    return true;
}
```

### 4. Meeting Rooms II (Min Rooms Required)
**Problem:** Minimum number of conference rooms required.
**Approach:** Sort start and end times separately, two pointers.
```java
public int minMeetingRooms(int[][] intervals) {
    int n = intervals.length;
    int[] start = new int[n], end = new int[n];
    for (int i = 0; i < n; i++) {
        start[i] = intervals[i][0];
        end[i] = intervals[i][1];
    }
    Arrays.sort(start);
    Arrays.sort(end);
    int rooms = 0, j = 0;
    for (int i = 0; i < n; i++) {
        if (start[i] < end[j]) rooms++;
        else j++;
    }
    return rooms;
}
```

### 5. Interval List Intersections
**Problem:** Given two lists of intervals, find intersection.
**Approach:** Two pointers, check overlap, advance the one ending earlier.
```java
public int[][] intervalIntersection(int[][] A, int[][] B) {
    List<int[]> result = new ArrayList<>();
    int i = 0, j = 0;
    while (i < A.length && j < B.length) {
        int start = Math.max(A[i][0], B[j][0]);
        int end = Math.min(A[i][1], B[j][1]);
        if (start <= end) result.add(new int[]{start, end});
        if (A[i][1] < B[j][1]) i++;
        else j++;
    }
    return result.toArray(new int[result.size()][]);
}
```

### 6. Non-overlapping Intervals
**Problem:** Remove minimum intervals to make rest non-overlapping.
**Approach:** Sort by end, greedily keep as many as possible.
```java
public int eraseOverlapIntervals(int[][] intervals) {
    Arrays.sort(intervals, (a, b) -> a[1] - b[1]);
    int count = 1, end = intervals[0][1];
    for (int i = 1; i < intervals.length; i++) {
        if (intervals[i][0] >= end) {
            count++;
            end = intervals[i][1];
        }
    }
    return intervals.length - count;
}
```

### 7. Minimum Interval to Be Included in a Query
**Problem:** For each query, find min length interval containing the query point.
**Approach:** Sort intervals by start, use priority queue by length, process sorted queries.

### 8. Maximum Number of Events That Can Be Attended
**Problem:** Attend max events by day. Each event can be attended on any day in [start, end].
**Approach:** Sort by start, use min-heap for end dates, process day by day.

### 9. Employee Free Time
**Problem:** Find common free time intervals across all employees.
**Approach:** Flatten all intervals, sort, find gaps.

### 10. Data Stream as Disjoint Intervals
**Problem:** Insert numbers into data stream, maintain merged intervals.
**Approach:** TreeMap of intervals, merge on insertion.
```java
class SummaryRanges {
    TreeMap<Integer, int[]> map;
    public SummaryRanges() { map = new TreeMap<>(); }
    public void addNum(int val) {
        if (map.containsKey(val)) return;
        Integer lowerKey = map.lowerKey(val);
        Integer higherKey = map.higherKey(val);
        if (lowerKey != null && higherKey != null &&
            map.get(lowerKey)[1] + 1 == val && val + 1 == higherKey) {
            map.get(lowerKey)[1] = map.get(higherKey)[1];
            map.remove(higherKey);
        } else if (lowerKey != null && map.get(lowerKey)[1] + 1 >= val) {
            map.get(lowerKey)[1] = Math.max(map.get(lowerKey)[1], val);
        } else if (higherKey != null && val + 1 == higherKey) {
            map.put(val, new int[]{val, map.get(higherKey)[1]});
            map.remove(higherKey);
        } else {
            map.put(val, new int[]{val, val});
        }
    }
    public int[][] getIntervals() {
        return map.values().toArray(new int[map.size()][]);
    }
}
```
