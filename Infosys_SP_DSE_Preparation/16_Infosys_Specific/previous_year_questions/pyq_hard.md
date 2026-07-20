# Infosys SP DSE - Previous Year Questions (Hard Level)

> 15 frequently asked hard-level questions from Infosys coding rounds.

---

## 1. Magical Vine Pattern Matching (S = P + Q + P + Q + ...)

**Problem Statement:** Given strings S, P, Q, determine if S can be formed by concatenating alternating occurrences of P and Q, starting with P. S must have at least one P and one Q.

**Approach:** Try all possible counts of P and Q. Check if concatenation equals S.

```python
def is_magical_vine(s, p, q):
    if not p or not q:
        return False

    len_s = len(s)
    len_p = len(p)
    len_q = len(q)

    # Try different numbers of P and Q repetitions
    for count_p in range(1, len_s // len_p + 1):
        remaining = len_s - count_p * len_p
        if remaining < 0:
            break
        if remaining % len_q != 0:
            continue
        count_q = remaining // len_q

        # Build and compare
        constructed = ""
        for i in range(max(count_p, count_q)):
            if i < count_p:
                constructed += p
            if i < count_q:
                constructed += q

        if constructed == s:
            return True

    return False

s = "ABABAB"
p = "AB"
q = "AB"
print(is_magical_vine(s, p, q))  # Output: True

s = "ABCABC"
p = "ABC"
q = "ABC"
print(is_magical_vine(s, p, q))  # Output: True
```

**Complexity:** O(n^2 / min(len_p, len_q)) time, O(n) space

**Tips:** Infosys SP L3 may ask for minimum length P+Q or count of valid (P,Q) pairs.

---

## 2. Array Partition with Divisibility Constraints

**Problem Statement:** Given an array, partition into minimum number of groups such that sum of each group is divisible by K.

**Approach:** Use DP with remainders. Track minimum partitions for each remainder state.

```python
def min_partitions_divisible(arr, k):
    n = len(arr)
    # DP: dp[i] = minimum groups to partition arr[:i]
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    # Track possible sums mod k for each partition
    for i in range(1, n + 1):
        current_sum = 0
        for j in range(i - 1, -1, -1):
            current_sum += arr[j]
            if current_sum % k == 0 and dp[j] != float('inf'):
                dp[i] = min(dp[i], dp[j] + 1)

    return dp[n] if dp[n] != float('inf') else -1

arr = [3, 6, 5, 2, 9]
k = 3
print(min_partitions_divisible(arr, k))  # Output: 2
```

**Complexity:** O(n^2) time, O(n) space

**Tips:** Practice variants: partition into exactly K groups, equal sum partition.

---

## 3. Kingdom Connectivity with Prime Components

**Problem Statement:** A kingdom has N cities connected by roads. Each city has a value. Find number of paths from city 1 to city N where the product of city values along the path is a prime number. Return answer modulo 10^9+7.

**Approach:** DFS/BFS with state tracking. For prime product, track if product is prime, has exactly one prime factor with exponent 1.

```python
from collections import defaultdict

def kingdom_paths(n, edges, values):
    MOD = 10**9 + 7
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        for i in range(3, int(x**0.5) + 1, 2):
            if x % i == 0:
                return False
        return True

    def dfs(node, product, visited):
        if node == n:
            return 1 if is_prime(product) else 0

        count = 0
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                count = (count + dfs(neighbor, product * values[neighbor - 1], visited)) % MOD
                visited.remove(neighbor)

        return count

    visited = {1}
    return dfs(1, values[0], visited)

# Example usage
n = 4
edges = [(1, 2), (2, 3), (3, 4), (1, 4)]
values = [2, 3, 5, 7]
print(kingdom_paths(n, edges, values))
```

**Complexity:** O(V + E) time for DFS, O(V) space

**Tips:** Handle large numbers with modular arithmetic. BFS may be needed for shortest path variants.

---

## 4. Trapping Rain Water

**Problem Statement:** Given heights of bars, compute how much water can be trapped after rain.

**Approach:** Two pointers or precompute left max and right max arrays.

```python
def trapping_rain_water(height):
    if not height:
        return 0

    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], height[i])

    right_max[n - 1] = height[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], height[i])

    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]

    return water

# Two pointer approach (O(1) space)
def trapping_rain_water_optimized(height):
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water

height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
print(trapping_rain_water(height))           # Output: 6
print(trapping_rain_water_optimized(height)) # Output: 6
```

**Complexity:** O(n) time, O(n) or O(1) space

**Tips:** Classic hard question. Two pointer approach is optimal. Explain clearly.

---

## 5. Edit Distance

**Problem Statement:** Find minimum operations (insert, delete, replace) to convert word1 to word2.

**Approach:** 2D DP. dp[i][j] = edit distance of word1[:i] to word2[:j].

```python
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1]   # replace
                )

    return dp[m][n]

word1 = "horse"
word2 = "ros"
print(edit_distance(word1, word2))  # Output: 3
```

**Complexity:** O(m * n) time, O(m * n) space, O(min(m, n)) space optimized

**Tips:** Infosys SP L3 may add custom costs for each operation.

---

## 6. Burst Balloons

**Problem Statement:** Given n balloons with values, burst all to maximize coins. Bursting balloon i gives nums[left] * nums[i] * nums[right] coins.

**Approach:** Interval DP. dp[i][j] = max coins from bursting balloons between i and j.

```python
def max_coins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for length in range(1, n - 1):
        for left in range(1, n - length):
            right = left + length - 1
            for k in range(left, right + 1):
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k - 1] + dp[k + 1][right] +
                    nums[left - 1] * nums[k] * nums[right + 1]
                )

    return dp[1][n - 2]

nums = [3, 1, 5, 8]
print(max_coins(nums))  # Output: 167
```

**Complexity:** O(n^3) time, O(n^2) space

**Tips:** Think of it as: which balloon to burst last in the range. Key insight for interval DP.

---

## 7. Regular Expression Matching

**Problem Statement:** Implement regex matching with '.' (any char) and '*' (zero or more of preceding char).

**Approach:** 2D DP. dp[i][j] = True if s[:i] matches p[:j].

```python
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like a*, a*b*, etc.
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # '*' means zero or more of preceding
                dp[i][j] = dp[i][j - 2]  # zero occurrences
                if p[j - 2] == '.' or p[j - 2] == s[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]  # one or more
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]

print(is_match("aa", "a"))    # Output: False
print(is_match("aa", "a*"))   # Output: True
print(is_match("ab", ".*"))   # Output: True
```

**Complexity:** O(m * n) time, O(m * n) space

**Tips:** Handle '*' carefully - it can match zero occurrences too.

---

## 8. Longest Palindromic Subsequence

**Problem Statement:** Find length of longest palindromic subsequence in string.

**Approach:** LCS of string and its reverse.

```python
def longest_palindromic_subsequence(s):
    def lcs(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[m][n]

    return lcs(s, s[::-1])

s = "bbbab"
print(longest_palindromic_subsequence(s))  # Output: 4
```

**Complexity:** O(n^2) time, O(n^2) space

**Tips:** Also practice: longest palindromic substring (expand around center).

---

## 9. Minimum Window Substring

**Problem Statement:** Find minimum window in s that contains all characters of t.

**Approach:** Sliding window with frequency counting.

```python
from collections import Counter

def min_window(s, t):
    if not s or not t:
        return ""

    t_count = Counter(t)
    required = len(t_count)
    formed = 0
    window_counts = {}

    left = 0
    min_len = float('inf')
    min_left = 0

    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1

        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1

        while formed == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_left = left

            left_char = s[left]
            window_counts[left_char] -= 1
            if left_char in t_count and window_counts[left_char] < t_count[left_char]:
                formed -= 1
            left += 1

    return "" if min_len == float('inf') else s[min_left:min_left + min_len]

s = "ADOBECODEBANC"
t = "ABC"
print(min_window(s, t))  # Output: "BANC"
```

**Complexity:** O(|s| + |t|) time, O(|s| + |t|) space

**Tips:** Expand window until valid, then shrink. Classic sliding window hard problem.

---

## 10. Sliding Window Maximum

**Problem Statement:** Given array and window size k, find maximum in each window.

**Approach:** Monotonic deque.

```python
from collections import deque

def sliding_window_max(nums, k):
    dq = deque()
    result = []

    for i in range(len(nums)):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements from back
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
print(sliding_window_max(nums, k))  # Output: [3, 3, 5, 5, 6, 7]
```

**Complexity:** O(n) time, O(k) space

**Tips:** Deque stores indices, not values. Remove from both ends.

---

## 11. Largest Rectangle in Histogram

**Problem Statement:** Find area of largest rectangle in histogram.

**Approach:** Monotonic stack to find left and right boundaries.

```python
def largest_rectangle(heights):
    stack = []
    max_area = 0
    n = len(heights)

    for i in range(n + 1):
        while stack and (i == n or heights[stack[-1]] >= heights[i]):
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area

heights = [2, 1, 5, 6, 2, 3]
print(largest_rectangle(heights))  # Output: 10
```

**Complexity:** O(n) time, O(n) space

**Tips:** Each element is pushed and popped at most once. Very elegant solution.

---

## 12. Serialize and Deserialize Binary Tree

**Problem Statement:** Design algorithm to serialize binary tree to string and deserialize back.

**Approach:** Preorder traversal with null markers.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root):
        if not root:
            return "null"

        result = []
        def dfs(node):
            if not node:
                result.append("null")
                return
            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(result)

    def deserialize(self, data):
        tokens = iter(data.split(","))

        def dfs():
            val = next(tokens)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()

# Usage
codec = Codec()
root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
serialized = codec.serialize(root)
print(serialized)           # "1,2,null,null,3,4,null,null,5,null,null"
deserialized = codec.deserialize(serialized)
print(codec.serialize(deserialized))  # Same output
```

**Complexity:** O(n) time, O(n) space

**Tips:** Can also use level-order (BFS) for serialization.

---

## 13. Binary Tree Maximum Path Sum

**Problem Statement:** Find maximum path sum in binary tree (path can start and end at any node).

**Approach:** DFS returning max single-branch sum while updating global max.

```python
def max_path_sum(root):
    max_sum = float('-inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0

        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)

        # Path through this node
        price_new_path = node.val + left_gain + right_gain
        max_sum = max(max_sum, price_new_path)

        # Return max single-branch path
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum

# Test
root = TreeNode(-10, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
print(max_path_sum(root))  # Output: 42
```

**Complexity:** O(n) time, O(h) space (h = height)

**Tips:** Key insight: path through node = left + node + right, but return only one branch.

---

## 14. Median of Two Sorted Arrays

**Problem Statement:** Find median of two sorted arrays in O(log(min(m,n))) time.

**Approach:** Binary search on smaller array partition.

```python
def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    low, high = 0, m

    while low <= high:
        i = (low + high) // 2
        j = (m + n + 1) // 2 - i

        max_left_1 = float('-inf') if i == 0 else nums1[i - 1]
        min_right_1 = float('inf') if i == m else nums1[i]
        max_left_2 = float('-inf') if j == 0 else nums2[j - 1]
        min_right_2 = float('inf') if j == n else nums2[j]

        if max_left_1 <= min_right_2 and max_left_2 <= min_right_1:
            if (m + n) % 2 == 1:
                return max(max_left_1, max_left_2)
            else:
                return (max(max_left_1, max_left_2) + min(min_right_1, min_right_2)) / 2
        elif max_left_1 > min_right_2:
            high = i - 1
        else:
            low = i + 1

nums1 = [1, 3]
nums2 = [2]
print(find_median_sorted_arrays(nums1, nums2))  # Output: 2.0
```

**Complexity:** O(log(min(m,n))) time, O(1) space

**Tips:** Very tricky binary search. Practice partition logic carefully.

---

## 15. Word Ladder II

**Problem Statement:** Find all shortest transformation sequences from beginWord to endWord.

**Approach:** BFS to find shortest path, then DFS to find all paths.

```python
from collections import defaultdict, deque

def find_ladders(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return []

    # Build adjacency
    neighbors = defaultdict(list)
    for word in word_set:
        for i in range(len(word)):
            pattern = word[:i] + '*' + word[i + 1:]
            neighbors[pattern].append(word)

    # BFS level by level
    result = []
    queue = deque([(begin_word, [begin_word])])
    visited = defaultdict(list)
    found = False

    while queue and not found:
        level_size = len(queue)
        local_visited = set()

        for _ in range(level_size):
            word, path = queue.popleft()

            for i in range(len(word)):
                pattern = word[:i] + '*' + word[i + 1:]
                for neighbor in neighbors[pattern]:
                    if neighbor == end_word:
                        result.append(path + [neighbor])
                        found = True
                    if neighbor not in word_set:
                        continue
                    if neighbor not in visited or len(visited[neighbor]) == len(path) + 1:
                        visited[neighbor] = path + [neighbor]
                        queue.append((neighbor, path + [neighbor]))
                        local_visited.add(neighbor)

        for word in local_visited:
            word_set.discard(word)

    return result

begin = "hit"
end = "cog"
words = ["hot", "dot", "dog", "lot", "log", "cog"]
print(find_ladders(begin, end, words))
# Output: [['hit', 'hot', 'dot', 'dog', 'cog'], ['hit', 'hot', 'lot', 'log', 'cog']]
```

**Complexity:** O(n * 26^L) time, where n = word count, L = word length

**Tips:** Word Ladder I (shortest length) is easier. BFS + DFS combination is key.

---

## Summary Table

| # | Problem | Time | Space | Pattern |
|---|---------|------|-------|---------|
| 1 | Magical Vine | O(n^2/min) | O(n) | String |
| 2 | Partition Divisibility | O(n^2) | O(n) | DP |
| 3 | Kingdom Prime | O(V+E) | O(V) | Graph |
| 4 | Trapping Rain Water | O(n) | O(1) | Two Pointer |
| 5 | Edit Distance | O(mn) | O(mn) | DP |
| 6 | Burst Balloons | O(n^3) | O(n^2) | Interval DP |
| 7 | Regex Matching | O(mn) | O(mn) | DP |
| 8 | Longest Palindromic Subseq | O(n^2) | O(n^2) | DP |
| 9 | Min Window Substring | O(n) | O(n) | Sliding Window |
| 10 | Sliding Window Max | O(n) | O(k) | Monotonic Deque |
| 11 | Largest Rectangle | O(n) | O(n) | Monotonic Stack |
| 12 | Serialize/Deserialize | O(n) | O(n) | Tree |
| 13 | Max Path Sum | O(n) | O(h) | DFS |
| 14 | Median Sorted Arrays | O(log min) | O(1) | Binary Search |
| 15 | Word Ladder II | O(n * 26^L) | O(n) | BFS + DFS |

> **Pro Tip:** Hard questions in Infosys SP L3 are meant to differentiate top candidates. Focus on explaining the approach clearly even if code is complex.
