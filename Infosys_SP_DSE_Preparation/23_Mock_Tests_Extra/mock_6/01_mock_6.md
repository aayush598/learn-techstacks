# Mock Test 6 - Infosys SP DSE Style

**Duration:** 3 Hours  
**Total Questions:** 3  
**Total Marks:** 100  
**Instructions:** Write complete, optimized solutions. Handle edge cases. Analyze time and space complexity.

---

## Question 1: Even-Odd Index Sort (Easy)

**Time:** 30 minutes  
**Marks:** 20

### Problem Statement

Given an integer array `arr` of length `n`, rearrange elements such that:
- Elements at **even indices** (0, 2, 4, ...) are sorted in **ascending order**
- Elements at **odd indices** (1, 3, 5, ...) are sorted in **descending order**

Return the rearranged array. If there are multiple valid arrangements, return any one.

### Input Format
- First line: Integer `n`
- Second line: `n` space-separated integers

### Output Format
- `n` space-separated integers representing the rearranged array

### Constraints
- `1 ≤ n ≤ 10^5`
- `1 ≤ arr[i] ≤ 10^6`

### Sample Input 1
```
7
5 1 3 7 2 8 4
```

### Sample Output 1
```
1 8 2 7 3 5 4
```

### Explanation
- Even-indexed positions (0, 2, 4, 6) get values: 1, 2, 3, 4 (ascending) ✓
- Odd-indexed positions (1, 3, 5) get values: 8, 7, 5 (descending) ✓
- Result: [1, 8, 2, 7, 3, 5, 4]

### Sample Input 2
```
5
9 6 3 5 1
```

### Sample Output 2
```
3 6 1 5 9
```

### Explanation
- Sorted even positions: [3, 5, 9] (ascending) → indices 0, 2, 4
- Sorted odd positions: [6, 1] (descending) → indices 1, 3
- Result: [3, 6, 1, 5, 9]

### Sample Input 3
```
4
10 20 30 40
```

### Sample Output 3
```
10 40 20 30
```

### Explanation
- Sorted even positions: [10, 20] (ascending) → indices 0, 2
- Sorted odd positions: [40, 30] (descending) → indices 1, 3
- Result: [10, 40, 20, 30]

---

### Approach 1: Sort Separately and Merge

**Idea:** Extract elements at even indices, sort them ascending. Extract elements at odd indices, sort them descending. Place them back at their respective positions.

```python
def rearrange_separate_sort(arr):
    n = len(arr)
    even_vals = sorted([arr[i] for i in range(0, n, 2)])
    odd_vals = sorted([arr[i] for i in range(1, n, 2)], reverse=True)
    
    result = [0] * n
    even_idx = 0
    odd_idx = 0
    
    for i in range(n):
        if i % 2 == 0:
            result[i] = even_vals[even_idx]
            even_idx += 1
        else:
            result[i] = odd_vals[odd_idx]
            odd_idx += 1
    
    return result
```

**Time Complexity:** O(N log N) - sorting dominates  
**Space Complexity:** O(N) - for the two extracted lists

---

### Approach 2: Two-Pointer Assignment

**Idea:** Sort the entire array. Use two pointers from sorted ends — smallest values go to even positions, largest values go to odd positions. This achieves the same result without extracting separate lists.

```python
def rearrange_two_pointer(arr):
    n = len(arr)
    sorted_arr = sorted(arr)
    
    result = [0] * n
    left = 0
    right = n - 1
    
    for i in range(n):
        if i % 2 == 0:
            result[i] = sorted_arr[left]
            left += 1
        else:
            result[i] = sorted_arr[right]
            right -= 1
    
    return result
```

**Time Complexity:** O(N log N) - sorting  
**Space Complexity:** O(N) - for the sorted copy

---

### Complete Solution

```python
import sys
from typing import List

def rearrange_even_odd(arr: List[int]) -> List[int]:
    """
    Rearrange array so even-indexed positions have ascending values
    and odd-indexed positions have descending values.
    
    Args:
        arr: Input integer array
    
    Returns:
        Rearranged array
    """
    n = len(arr)
    if n <= 1:
        return arr[:]
    
    # Extract and sort even-index values ascending
    even_vals = sorted(arr[i] for i in range(0, n, 2))
    # Extract and sort odd-index values descending
    odd_vals = sorted((arr[i] for i in range(1, n, 2)), reverse=True)
    
    result = [0] * n
    even_ptr = 0
    odd_ptr = 0
    
    for i in range(n):
        if i % 2 == 0:
            result[i] = even_vals[even_ptr]
            even_ptr += 1
        else:
            result[i] = odd_vals[odd_ptr]
            odd_ptr += 1
    
    return result


def solve():
    """Main solution function for competitive programming."""
    n = int(input().strip())
    arr = list(map(int, input().strip().split()))
    
    result = rearrange_even_odd(arr)
    print(*result)


# Test cases
def test():
    assert rearrange_even_odd([5, 1, 3, 7, 2, 8, 4]) == [1, 8, 2, 7, 3, 5, 4]
    assert rearrange_even_odd([9, 6, 3, 5, 1]) == [3, 6, 1, 5, 9]
    assert rearrange_even_odd([10, 20, 30, 40]) == [10, 40, 20, 30]
    assert rearrange_even_odd([1]) == [1]
    assert rearrange_even_odd([2, 1]) == [1, 2]
    assert rearrange_even_odd([3, 2, 1]) == [1, 3, 2]
    assert rearrange_even_odd([1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1]
    assert rearrange_even_odd([5, 4, 3, 2, 1, 6]) == [1, 6, 2, 5, 3, 4]
    print("All test cases passed!")


if __name__ == "__main__":
    test()
    # Uncomment for competitive programming:
    # solve()
```

### Complexity Analysis
- **Time:** O(N log N) — sorting the extracted values
- **Space:** O(N) — storing the extracted even and odd values

### Tips for Infosys Test
- This is a pattern recognition problem — identify that even and odd indices are independent
- Sort separately approach is cleaner and less error-prone than the two-pointer trick
- Edge cases: single element, two elements, all identical values
- Both approaches are O(N log N); the two-pointer variant saves a constant factor but is less intuitive

---

## Question 2: Longest Rearrangeable Palindrome Substring (Medium)

**Time:** 60 minutes  
**Marks:** 35

### Problem Statement

Given a string `S` of lowercase English letters and an integer `K`, find the length of the **longest substring** such that the characters of that substring can be **rearranged** to form a palindrome.

A string can be rearranged into a palindrome if **at most one character has an odd frequency** (i.e., the string has at most one character with odd count).

### Input Format
- First line: String `S`
- Second line: Integer `K` (minimum length, but we need to find the maximum length substring that satisfies the property)

**Note:** The parameter `K` is not used as a constraint — we want the overall longest valid substring regardless of `K`.

### Output Format
- Single integer: length of the longest substring whose characters can form a palindrome

### Constraints
- `1 ≤ |S| ≤ 10^5`
- `1 ≤ K ≤ |S|`
- `S` consists of lowercase English letters only

### Sample Input 1
```
aabbc
3
```

### Sample Output 1
```
5
```

### Explanation
The entire string "aabbc" has frequencies: a=2, b=2, c=1. Only one character (c) has odd frequency. So the entire string can be rearranged into a palindrome (e.g., "abcba"). Length = 5.

### Sample Input 2
```
abccba
2
```

### Sample Output 2
```
6
```

### Explanation
"abccba" frequencies: a=2, b=2, c=2. Zero characters have odd frequency. The entire string is a rearrangeable palindrome. Length = 6.

### Sample Input 3
```
abcde
2
```

### Sample Output 3
```
4
```

### Explanation
No substring of length 5 works (all chars have odd freq). Longest valid substring: "abcd" or "bcde" — each has 4 chars with odd frequency counts, which is more than 1. Actually "abca" type substrings don't exist. The best is length 1 (any single char). But wait — "abcd" has 4 odd freq chars, "abc" has 3, "ab" has 2, "a" has 1. So longest is 1. Let me recalculate: actually substrings are contiguous. Best we can do is length 1. But let me reconsider — "ab" has a=1,b=1 (2 odd) — no. So answer is 1. Let me use a better example:

Actually for "abcde", every single char has freq 1. No 2-char substring works (both odd). So max = 1.

Let me fix: use "abcdabc" → "abcda" has a=2,b=1,c=1,d=1 (3 odd, no). "bcdab" similar. "cdabc" c=1,d=1,a=1,b=1,c=1 → 3 odd. Best: "a" or "b" etc = 1.

Better example:

```
abcba
2
```

Output: 5 ("abcba" already palindrome, a=2,b=2,c=1 → 1 odd ✓)

---

### Approach 1: Brute Force — Check All Substrings

**Idea:** Enumerate all O(N²) substrings, check each for rearrangeable-palindrome property using a frequency array.

```python
def longest_rpal_brute(s):
    n = len(s)
    max_len = 0
    
    for i in range(n):
        freq = [0] * 26
        for j in range(i, n):
            freq[ord(s[j]) - ord('a')] += 1
            odd_count = sum(1 for f in freq if f % 2 == 1)
            if odd_count <= 1:
                max_len = max(max_len, j - i + 1)
    
    return max_len
```

**Time Complexity:** O(N² × 26) — O(N²) substrings, O(26) to count odd freq  
**Space Complexity:** O(26) = O(1)

---

### Approach 2: Optimized Sliding Window with Bitmask

**Idea:** Use a bitmask to track parity of character frequencies. A bitmask has at most 1 bit set if and only if the corresponding characters can form a rearrangeable palindrome. Use the fact that for each starting position, we can expand the window. However, since we want the maximum length, we iterate from large to small, or use the bitmask + hash set approach.

**Key Insight:** For a substring `s[i..j]`, compute XOR of bitmasks. If the XOR result has 0 or 1 bits set, the substring is valid. Use prefix XOR bitmask array.

```python
def longest_rpal_bitmask(s):
    n = len(s)
    if n == 0:
        return 0
    
    # prefix_xor[i] = XOR bitmask of s[0..i-1]
    prefix_xor = [0] * (n + 1)
    for i in range(n):
        bit = 1 << (ord(s[i]) - ord('a'))
        prefix_xor[i + 1] = prefix_xor[i] ^ bit
    
    max_len = 0
    
    for i in range(n):
        for j in range(i, n):
            xor_val = prefix_xor[j + 1] ^ prefix_xor[i]
            # Check if xor_val has at most 1 bit set
            if xor_val == 0 or (xor_val & (xor_val - 1)) == 0:
                max_len = max(max_len, j - i + 1)
    
    return max_len
```

**Time Complexity:** O(N²)  
**Space Complexity:** O(N) for prefix array

---

### Approach 3: Binary Search + Bitmask Check (Optimized)

**Idea:** Binary search on the answer (substring length). For a given length L, check if any substring of length L is a rearrangeable palindrome using prefix XOR bitmask and a hash set.

```python
def longest_rpal_binary_search(s):
    n = len(s)
    
    def has_valid_substring(length):
        """Check if any substring of given length is rearrangeable-palindrome."""
        seen = set()
        # Empty prefix
        seen.add(0)
        bitmask = 0
        for i in range(n):
            bitmask ^= 1 << (ord(s[i]) - ord('a'))
            if i >= length:
                bitmask ^= 1 << (ord(s[i - length]) - ord('a'))
            # Check current bitmask or any single-bit-flip variant
            if bitmask in seen:
                return True
            for c in range(26):
                if bitmask ^ (1 << c) in seen:
                    return True
            seen.add(bitmask)
        return False
    
    lo, hi = 1, n
    result = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if has_valid_substring(mid):
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    return result
```

**Time Complexity:** O(26 × N × log N) — binary search × sliding window × 26 flips  
**Space Complexity:** O(N)

---

### Complete Solution

```python
import sys
from typing import List

def longest_rpalindrome_substring(s: str, k: int) -> int:
    """
    Find length of longest substring whose characters can be rearranged
    into a palindrome (at most one character has odd frequency).
    
    Args:
        s: Input string of lowercase English letters
        k: Parameter given in problem (unused, we find global maximum)
    
    Returns:
        Length of longest valid substring
    """
    n = len(s)
    if n == 0:
        return 0
    
    # Approach: Prefix XOR bitmask + brute force check
    # For larger N, use binary search + sliding window (Approach 3 above)
    
    # Build prefix XOR bitmask
    prefix_xor = [0] * (n + 1)
    for i in range(n):
        bit = 1 << (ord(s[i]) - ord('a'))
        prefix_xor[i + 1] = prefix_xor[i] ^ bit
    
    max_len = 1  # At least one character is always valid
    
    for i in range(n):
        for j in range(i + 1, n):
            xor_val = prefix_xor[j + 1] ^ prefix_xor[i]
            # Check if at most 1 bit is set
            if xor_val == 0 or (xor_val & (xor_val - 1)) == 0:
                max_len = max(max_len, j - i + 1)
    
    return max_len


def longest_rpalindrome_optimized(s: str, k: int) -> int:
    """
    Optimized approach using binary search + bitmask hash set.
    O(26 * N * log N) time.
    """
    n = len(s)
    if n == 0:
        return 0
    
    def has_valid(length: int) -> bool:
        """Check if any substring of given length is rearrangeable-palindrome."""
        seen = set()
        seen.add(0)
        bitmask = 0
        for i in range(n):
            bitmask ^= 1 << (ord(s[i]) - ord('a'))
            if i >= length:
                bitmask ^= 1 << (ord(s[i - length]) - ord('a'))
            if bitmask in seen:
                return True
            for c in range(26):
                if bitmask ^ (1 << c) in seen:
                    return True
            seen.add(bitmask)
        return False
    
    lo, hi = 1, n
    result = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if has_valid(mid):
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    return result


def solve():
    """Main solution function for competitive programming."""
    s = input().strip()
    k = int(input().strip())
    result = longest_rpalindrome_optimized(s, k)
    print(result)


# Test cases
def test():
    assert longest_rpalindrome_substring("aabbc", 3) == 5
    assert longest_rpalindrome_substring("abccba", 2) == 6
    assert longest_rpalindrome_substring("abcba", 2) == 5
    assert longest_rpalindrome_substring("a", 1) == 1
    assert longest_rpalindrome_substring("aa", 1) == 2
    assert longest_rpalindrome_substring("ab", 1) == 1
    assert longest_rpalindrome_substring("abc", 1) == 1
    assert longest_rpalindrome_substring("aaaa", 2) == 4
    assert longest_rpalindrome_substring("aba", 2) == 3
    assert longest_rpalindrome_substring("abcabc", 3) == 6  # abcabc: a=2,b=2,c=2 → 0 odd ✓
    print("All test cases passed!")


if __name__ == "__main__":
    test()
    # Uncomment for competitive programming:
    # solve()
```

### Complexity Analysis

**Approach 1: Brute Force**
- Time: O(N² × 26) — check all substrings
- Space: O(26) = O(1)

**Approach 2: Prefix XOR Bitmask**
- Time: O(N²) — two nested loops with O(1) bitmask check
- Space: O(N) — prefix array

**Approach 3: Binary Search + Bitmask Hash Set**
- Time: O(26 × N × log N) — binary search × sliding window × 26 character flips
- Space: O(N) — hash set

### Tips for Infosys Test
- Recognize the "rearrangeable palindrome" condition: at most 1 character has odd frequency
- The bitmask trick (XOR) is key — toggling a bit represents toggling parity of a character count
- `(x & (x-1)) == 0` checks if x has at most 1 bit set — this is a must-know bitwise trick
- For N ≤ 10^5, the O(N²) prefix XOR approach may TLE; prefer the binary search approach
- Edge cases: single character (always valid), all same characters, all unique characters

---

## Question 3: Maximum Edge Weight on Tree Path (Hard)

**Time:** 90 minutes  
**Marks:** 45

### Problem Statement

You are given a tree with `N` nodes (numbered 1 to N) and `N-1` weighted edges. Answer `Q` queries. Each query gives two nodes `u` and `v`, and you need to find the **maximum edge weight** on the unique path between `u` and `v`.

### Input Format
- First line: Two integers `N` and `Q`
- Next `N-1` lines: Three integers `u`, `v`, `w` — an edge between nodes `u` and `v` with weight `w`
- Next `Q` lines: Two integers `u`, `v` — a query

### Output Format
- `Q` lines, each containing the maximum edge weight on the path between the queried nodes

### Constraints
- `2 ≤ N ≤ 10^5`
- `1 ≤ Q ≤ 10^5`
- `1 ≤ w ≤ 10^9`
- The graph is guaranteed to be a tree

### Sample Input 1
```
5 3
1 2 3
2 3 7
2 4 1
4 5 5
1 3
3 5
1 5
```

### Sample Output 1
```
7
7
7
```

### Explanation
- Query (1,3): Path 1→2→3, max edge = max(3,7) = 7
- Query (3,5): Path 3→2→4→5, max edge = max(7,1,5) = 7
- Query (1,5): Path 1→2→4→5, max edge = max(3,1,5) = 5... wait, let me recalculate
  - Actually path 1→2→4→5: edges are (1,2,3), (2,4,1), (4,5,5). Max = max(3,1,5) = 5

Let me fix the expected output:
```
7
7
5
```

### Sample Input 2
```
4 2
1 2 10
2 3 20
3 4 30
1 4
2 3
```

### Sample Output 2
```
30
20
```

### Explanation
- Query (1,4): Path 1→2→3→4, max edge = max(10,20,30) = 30
- Query (2,3): Path 2→3, max edge = 20

### Sample Input 3
```
6 3
1 2 5
1 3 10
2 4 3
2 5 8
3 6 1
1 6
4 5
4 6
```

### Sample Output 3
```
10
8
10
```

### Explanation
- Query (1,6): Path 1→3→6, max edge = max(10,1) = 10
- Query (4,5): Path 4→2→5, max edge = max(3,8) = 8
- Query (4,6): Path 4→2→1→3→6, max edge = max(3,5,10,1) = 10

---

### Approach 1: BFS/DFS per Query (Naive)

**Idea:** For each query, run BFS or DFS from `u` to find the path to `v`, then compute the maximum edge weight along that path.

```python
from collections import defaultdict, deque

def max_edge_naive(n, edges, queries):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    def bfs_max_edge(start, end):
        visited = set()
        queue = deque([(start, 0)])
        visited.add(start)
        parent = {start: None}
        parent_weight = {start: 0}
        
        while queue:
            node, max_w = queue.popleft()
            if node == end:
                return max_w
            for neighbor, weight in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    parent_weight[neighbor] = weight
                    queue.append((neighbor, max(max_w, weight)))
        
        return -1
    
    results = []
    for u, v in queries:
        results.append(bfs_max_edge(u, v))
    
    return results
```

**Time Complexity:** O(Q × (N + E)) — BFS per query  
**Space Complexity:** O(N + E)

---

### Approach 2: Binary Lifting for LCA + Maximum Edge

**Idea:** Preprocess the tree using binary lifting to answer LCA queries in O(log N). For each node, store the maximum edge weight on the path to its 2^k-th ancestor. To find max edge on path (u, v):
1. Find LCA of u and v
2. Max edge = max(max edge from u to LCA, max edge from v to LCA)

```python
import sys
from collections import defaultdict

def build_binary_lifting(n, adj, root=1):
    LOG = 20  # 2^20 > 10^5
    depth = [0] * (n + 1)
    parent = [[0] * (n + 1) for _ in range(LOG)]
    max_edge = [[0] * (n + 1) for _ in range(LOG)]
    
    # BFS to set depth and immediate parents
    from collections import deque
    visited = [False] * (n + 1)
    queue = deque([root])
    visited[root] = True
    parent[0][root] = 0
    
    while queue:
        node = queue.popleft()
        for neighbor, weight in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                depth[neighbor] = depth[node] + 1
                parent[0][neighbor] = node
                max_edge[0][neighbor] = weight
                queue.append(neighbor)
    
    # Binary lifting table
    for k in range(1, LOG):
        for v in range(1, n + 1):
            mid = parent[k - 1][v]
            parent[k][v] = parent[k - 1][mid]
            max_edge[k][v] = max(max_edge[k - 1][v], max_edge[k - 1][mid])
    
    return depth, parent, max_edge


def max_on_path(u, v, depth, parent, max_edge):
    """Find maximum edge weight on path between u and v."""
    LOG = len(parent)
    
    if depth[u] < depth[v]:
        u, v = v, u
    
    # Lift u to same depth as v
    max_w = 0
    diff = depth[u] - depth[v]
    for k in range(LOG):
        if diff & (1 << k):
            max_w = max(max_w, max_edge[k][u])
            u = parent[k][u]
    
    if u == v:
        return max_w
    
    # Lift both until LCA
    for k in range(LOG - 1, -1, -1):
        if parent[k][u] != parent[k][v]:
            max_w = max(max_w, max_edge[k][u], max_edge[k][v])
            u = parent[k][u]
            v = parent[k][v]
    
    # One more step to reach LCA
    max_w = max(max_w, max_edge[0][u], max_edge[0][v])
    return max_w
```

---

### Complete Solution

```python
import sys
from collections import defaultdict, deque
from typing import List, Tuple

def solve():
    """Main solution function for competitive programming."""
    input_data = sys.stdin.read().split()
    idx = 0
    
    n = int(input_data[idx]); idx += 1
    q = int(input_data[idx]); idx += 1
    
    adj = defaultdict(list)
    for _ in range(n - 1):
        u = int(input_data[idx]); idx += 1
        v = int(input_data[idx]); idx += 1
        w = int(input_data[idx]); idx += 1
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    queries = []
    for _ in range(q):
        u = int(input_data[idx]); idx += 1
        v = int(input_data[idx]); idx += 1
        queries.append((u, v))
    
    LOG = 20
    depth = [0] * (n + 1)
    parent = [[0] * (n + 1) for _ in range(LOG)]
    max_edge_table = [[0] * (n + 1) for _ in range(LOG)]
    
    # BFS from node 1
    visited = [False] * (n + 1)
    queue = deque([1])
    visited[1] = True
    parent[0][1] = 0
    
    while queue:
        node = queue.popleft()
        for neighbor, weight in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                depth[neighbor] = depth[node] + 1
                parent[0][neighbor] = node
                max_edge_table[0][neighbor] = weight
                queue.append(neighbor)
    
    # Build binary lifting table
    for k in range(1, LOG):
        for v in range(1, n + 1):
            mid = parent[k - 1][v]
            parent[k][v] = parent[k - 1][mid]
            max_edge_table[k][v] = max(max_edge_table[k - 1][v], max_edge_table[k - 1][mid])
    
    results = []
    for u, v in queries:
        max_w = 0
        
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if diff & (1 << k):
                max_w = max(max_w, max_edge_table[k][u])
                u = parent[k][u]
        
        if u == v:
            results.append(max_w)
            continue
        
        # Lift both until they share a parent
        for k in range(LOG - 1, -1, -1):
            if parent[k][u] != parent[k][v]:
                max_w = max(max_w, max_edge_table[k][u], max_edge_table[k][v])
                u = parent[k][u]
                v = parent[k][v]
        
        # Final step to LCA
        max_w = max(max_w, max_edge_table[0][u], max_edge_table[0][v])
        results.append(max_w)
    
    print('\n'.join(map(str, results)))


# Test cases
def test():
    # Test 1: Sample 1
    adj1 = defaultdict(list)
    for u, v, w in [(1,2,3),(2,3,7),(2,4,1),(4,5,5)]:
        adj1[u].append((v,w))
        adj1[v].append((u,w))
    
    LOG = 20
    n = 5
    depth = [0]*(n+1)
    parent = [[0]*(n+1) for _ in range(LOG)]
    max_et = [[0]*(n+1) for _ in range(LOG)]
    
    visited = [False]*(n+1)
    queue = deque([1])
    visited[1] = True
    while queue:
        node = queue.popleft()
        for nb, wt in adj1[node]:
            if not visited[nb]:
                visited[nb] = True
                depth[nb] = depth[node]+1
                parent[0][nb] = node
                max_et[0][nb] = wt
                queue.append(nb)
    
    for k in range(1, LOG):
        for v in range(1, n+1):
            mid = parent[k-1][v]
            parent[k][v] = parent[k-1][mid]
            max_et[k][v] = max(max_et[k-1][v], max_et[k-1][mid])
    
    def query(u, v):
        mw = 0
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u]-depth[v]
        for k in range(LOG):
            if diff & (1<<k):
                mw = max(mw, max_et[k][u])
                u = parent[k][u]
        if u == v:
            return mw
        for k in range(LOG-1,-1,-1):
            if parent[k][u] != parent[k][v]:
                mw = max(mw, max_et[k][u], max_et[k][v])
                u = parent[k][u]
                v = parent[k][v]
        mw = max(mw, max_et[0][u], max_et[0][v])
        return mw
    
    assert query(1, 3) == 7
    assert query(3, 5) == 7
    assert query(1, 5) == 5
    
    # Test 2: Sample 2
    adj2 = defaultdict(list)
    for u, v, w in [(1,2,10),(2,3,20),(3,4,30)]:
        adj2[u].append((v,w))
        adj2[v].append((u,w))
    
    depth2 = [0]*5
    parent2 = [[0]*5 for _ in range(LOG)]
    max_et2 = [[0]*5 for _ in range(LOG)]
    visited2 = [False]*5
    queue2 = deque([1])
    visited2[1] = True
    while queue2:
        node = queue2.popleft()
        for nb, wt in adj2[node]:
            if not visited2[nb]:
                visited2[nb] = True
                depth2[nb] = depth2[node]+1
                parent2[0][nb] = node
                max_et2[0][nb] = wt
                queue2.append(nb)
    
    for k in range(1, LOG):
        for v in range(1, 5):
            mid = parent2[k-1][v]
            parent2[k][v] = parent2[k-1][mid]
            max_et2[k][v] = max(max_et2[k-1][v], max_et2[k-1][mid])
    
    def query2(u, v):
        mw = 0
        if depth2[u] < depth2[v]:
            u, v = v, u
        diff = depth2[u]-depth2[v]
        for k in range(LOG):
            if diff & (1<<k):
                mw = max(mw, max_et2[k][u])
                u = parent2[k][u]
        if u == v:
            return mw
        for k in range(LOG-1,-1,-1):
            if parent2[k][u] != parent2[k][v]:
                mw = max(mw, max_et2[k][u], max_et2[k][v])
                u = parent2[k][u]
                v = parent2[k][v]
        mw = max(mw, max_et2[0][u], max_et2[0][v])
        return mw
    
    assert query2(1, 4) == 30
    assert query2(2, 3) == 20
    
    # Test 3: Two nodes
    adj3 = defaultdict(list)
    adj3[1].append((2, 42))
    adj3[2].append((1, 42))
    
    depth3 = [0]*3
    parent3 = [[0]*3 for _ in range(LOG)]
    max_et3 = [[0]*3 for _ in range(LOG)]
    visited3 = [False]*3
    queue3 = deque([1])
    visited3[1] = True
    while queue3:
        node = queue3.popleft()
        for nb, wt in adj3[node]:
            if not visited3[nb]:
                visited3[nb] = True
                depth3[nb] = depth3[node]+1
                parent3[0][nb] = node
                max_et3[0][nb] = wt
                queue3.append(nb)
    
    for k in range(1, LOG):
        for v in range(1, 3):
            mid = parent3[k-1][v]
            parent3[k][v] = parent3[k-1][mid]
            max_et3[k][v] = max(max_et3[k-1][v], max_et3[k-1][mid])
    
    def query3(u, v):
        mw = 0
        if depth3[u] < depth3[v]:
            u, v = v, u
        diff = depth3[u]-depth3[v]
        for k in range(LOG):
            if diff & (1<<k):
                mw = max(mw, max_et3[k][u])
                u = parent3[k][u]
        if u == v:
            return mw
        for k in range(LOG-1,-1,-1):
            if parent3[k][u] != parent3[k][v]:
                mw = max(mw, max_et3[k][u], max_et3[k][v])
                u = parent3[k][u]
                v = parent3[k][v]
        mw = max(mw, max_et3[0][u], max_et3[0][v])
        return mw
    
    assert query3(1, 2) == 42
    
    print("All test cases passed!")


if __name__ == "__main__":
    test()
    # Uncomment for competitive programming:
    # solve()
```

### Complexity Analysis

**Naive BFS per Query:**
- Time: O(Q × N) — BFS for each query
- Space: O(N)

**Binary Lifting (Optimal):**
- Time: O(N log N + Q log N) — preprocessing + O(log N) per query
- Space: O(N log N) — parent and max_edge tables

**For N = Q = 10^5:**
- Naive: 10^5 × 10^5 = 10^10 (TLE)
- Binary Lifting: 10^5 × 20 ≈ 2 × 10^6 (fast)

### Tips for Infosys Test
- Binary lifting is a must-know pattern for tree path queries
- The key insight: store not just the 2^k-th ancestor, but also the maximum edge on that jump
- LOG = 20 is sufficient for N ≤ 10^5 (2^20 ≈ 10^6)
- Root the tree arbitrarily (node 1) — BFS/DFS from root sets depth and parent
- Edge case: query (u, u) — answer is 0 (no edges on path)
- Alternative: Disjoint Set Union (DSU) on sorted edges for offline queries — also O(N log N + Q α(N))

---

## Time Management Guide

### 3-Hour Allocation

| Phase | Duration | Activity |
|-------|----------|----------|
| **Read All Problems** | 5 min | Skim all 3 problems, identify difficulty levels |
| **Q1 (Easy)** | 30 min | Solve, test, move on |
| **Q2 (Medium)** | 55 min | Solve, optimize, test edge cases |
| **Q3 (Hard)** | 75 min | Implement binary lifting, test thoroughly |
| **Buffer** | 15 min | Review, fix bugs, optimize |
| **Total** | 180 min | |

### Detailed Breakdown

**0:00 – 0:05** (5 min): Read all three problems. Identify which is easy/medium/hard.

**0:05 – 0:35** (30 min): **Q1 — Even-Odd Sort**
- 5 min: Understand problem and design approach
- 15 min: Code the solution
- 10 min: Test with given samples + edge cases

**0:35 – 1:30** (55 min): **Q2 — Rearrangeable Palindrome Substring**
- 10 min: Understand problem, recognize bitmask trick
- 25 min: Code the optimized solution
- 10 min: Test with samples
- 10 min: Optimize if TLE, handle edge cases

**1:30 – 2:45** (75 min): **Q3 — Maximum Edge on Tree Path**
- 15 min: Understand problem, design binary lifting approach
- 40 min: Code binary lifting preprocessing + query
- 10 min: Test with samples + edge cases
- 10 min: Debug any issues

**2:45 – 3:00** (15 min): **Buffer**
- Review all solutions
- Fix any remaining bugs
- Ensure I/O format is correct
- Check time/space complexity requirements

### Key Reminders
1. **Never spend more than allocated time** — partial marks exist
2. **Q1 should be free points** — do it fast and correctly
3. **Q2 is the differentiator** — bitmask XOR trick is essential
4. **Q3 is the hardest** — binary lifting template should be memorized
5. **Always test with sample inputs** before moving on
6. **Handle edge cases**: empty input, single element, all same values
7. **Use fast I/O** (`sys.stdin.read()`) for large inputs in Python
