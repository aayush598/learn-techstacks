# Common Python Patterns for Infosys SP DSE Preparation

## 1. Prefix Sum Pattern

```python
# ============================================
# Problem: Range sum queries — answer multiple queries
# about sum of elements in range [l, r]
# Time: O(n) precompute + O(1) per query
# ============================================

def build_prefix_sum(arr):
    """Build prefix sum array."""
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

def range_sum(prefix, l, r):
    """Get sum of arr[l..r] using prefix sums."""
    return prefix[r + 1] - prefix[l]

# ============================================
# Example
# ============================================
arr = [2, 4, 6, 8, 10]
prefix = build_prefix_sum(arr)

print(range_sum(prefix, 1, 3))  # 4+6+8 = 18
print(range_sum(prefix, 0, 4))  # 2+4+6+8+10 = 30

# ============================================
# 2D Prefix Sum — for matrix range queries
# ============================================
def build_2d_prefix(grid):
    """Build 2D prefix sum matrix."""
    n = len(grid)
    m = len(grid[0])
    prefix = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n):
        for j in range(m):
            prefix[i+1][j+1] = (grid[i][j] + prefix[i][j+1] +
                                prefix[i+1][j] - prefix[i][j])
    return prefix

def range_sum_2d(prefix, r1, c1, r2, c2):
    """Get sum of submatrix from (r1,c1) to (r2,c2)."""
    return (prefix[r2+1][c2+1] - prefix[r1][c2+1] -
            prefix[r2+1][c1] + prefix[r1][c1])

# ============================================
# When to use: Range sum queries, subarray sum problems
# ============================================
```

## 2. Two Pointer Pattern

```python
# ============================================
# Two pointers on sorted array — O(n)
# ============================================

# Problem: Find pair with given sum
def two_sum_sorted(arr, target):
    """Find pair that sums to target in sorted array."""
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

arr = [1, 2, 3, 4, 6]
print(two_sum_sorted(arr, 6))  # [1, 3] → arr[1]=2 + arr[3]=4 = 6

# ============================================
# Problem: Container with most water
# ============================================
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        water = min(height[left], height[right]) * (right - left)
        max_water = max(max_water, water)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))  # 49

# ============================================
# Problem: Remove duplicates from sorted array
# ============================================
def remove_duplicates(arr):
    slow = 0
    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]
    return slow + 1

arr = [1, 1, 2, 2, 3]
length = remove_duplicates(arr)
print(arr[:length])  # [1, 2, 3]

# ============================================
# When to use: Sorted array problems, pair finding
# ============================================
```

## 3. Sliding Window Pattern

```python
# ============================================
# Fixed-size sliding window — O(n)
# ============================================

# Problem: Maximum sum subarray of size k
def max_subarray_sum(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum

arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
print(max_subarray_sum(arr, 4))  # 39

# ============================================
# Variable-size sliding window — O(n)
# ============================================

# Problem: Longest substring with at most k distinct chars
def longest_substring(s, k):
    char_count = {}
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_len = max(max_len, right - left + 1)
    
    return max_len

print(longest_substring("eceba", 2))  # 3 → "ece"

# ============================================
# Problem: Minimum window substring
# ============================================
from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""
    
    need = Counter(t)
    missing = len(t)
    left = 0
    start, end = 0, float('inf')
    
    for right in range(len(s)):
        if need[s[right]] > 0:
            missing -= 1
        need[s[right]] -= 1
        
        while missing == 0:
            if right - left < end - start:
                start, end = left, right
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    
    return s[start:end + 1] if end < float('inf') else ""

print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"

# ============================================
# When to use: Substring/subarray problems, window constraints
# ============================================
```

## 4. Fast and Slow Pointer

```python
# ============================================
# Cycle detection — Floyd's algorithm
# ============================================

# Problem: Detect cycle in linked list
def has_cycle(head):
    if not head or not head.next:
        return False
    
    slow = head
    fast = head.next
    
    while slow != fast:
        if not fast or not fast.next:
            return False
        slow = slow.next
        fast = fast.next.next
    
    return True

# ============================================
# Find middle of linked list
# ============================================
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# ============================================
# Find cycle start
# ============================================
def find_cycle_start(head):
    slow = fast = head
    
    # Phase 1: Detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    else:
        return None
    
    # Phase 2: Find start
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next
    
    return slow

# ============================================
# Problem: Happy number
# ============================================
def is_happy(n):
    def get_next(num):
        total = 0
        while num > 0:
            num, digit = divmod(num, 10)
            total += digit ** 2
        return total
    
    slow = fast = n
    while True:
        slow = get_next(slow)
        fast = get_next(get_next(fast))
        if slow == fast:
            return slow == 1

print(is_happy(19))  # True

# ============================================
# When to use: Linked list cycle, middle element, palindrome check
# ============================================
```

## 5. Dutch National Flag (3-Way Partition)

```python
# ============================================
# Problem: Sort array of 0s, 1s, 2s in single pass
# ============================================

def sort_colors(arr):
    """Dutch National Flag algorithm."""
    low = 0       # boundary for 0s
    mid = 0       # current element
    high = len(arr) - 1  # boundary for 2s
    
    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:  # arr[mid] == 2
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
    
    return arr

print(sort_colors([2, 0, 2, 1, 1, 0]))  # [0, 0, 1, 1, 2, 2]

# ============================================
# Generalized: 3-way partition around pivot
# ============================================
def three_way_partition(arr, pivot):
    low = 0
    mid = 0
    high = len(arr) - 1
    
    while mid <= high:
        if arr[mid] < pivot:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == pivot:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
    
    return low, high  # Elements equal to pivot: arr[low..high]

# ============================================
# When to use: Sorting with 3 categories, partition problems
# ============================================
```

## 6. Kadane's Algorithm Template

```python
# ============================================
# Problem: Maximum subarray sum — O(n)
# ============================================

def kadane(arr):
    """Find maximum sum of contiguous subarray."""
    max_sum = arr[0]
    current_sum = arr[0]
    
    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

print(kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6 → [4, -1, 2, 1]

# ============================================
# Kadane's with indices
# ============================================
def kadane_with_indices(arr):
    max_sum = arr[0]
    current_sum = arr[0]
    start = end = temp_start = 0
    
    for i in range(1, len(arr)):
        if arr[i] > current_sum + arr[i]:
            current_sum = arr[i]
            temp_start = i
        else:
            current_sum += arr[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, arr[start:end + 1]

# ============================================
# Maximum product subarray
# ============================================
def max_product(arr):
    max_prod = arr[0]
    min_prod = arr[0]
    result = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] < 0:
            max_prod, min_prod = min_prod, max_prod
        
        max_prod = max(arr[i], max_prod * arr[i])
        min_prod = min(arr[i], min_prod * arr[i])
        
        result = max(result, max_prod)
    
    return result

print(max_product([2, 3, -2, 4]))  # 6

# ============================================
# Minimum subarray sum
# ============================================
def min_subarray_sum(arr):
    min_sum = arr[0]
    current_sum = arr[0]
    
    for i in range(1, len(arr)):
        current_sum = min(arr[i], current_sum + arr[i])
        min_sum = min(min_sum, current_sum)
    
    return min_sum

# ============================================
# When to use: Subarray/subsequence optimization problems
# ============================================
```

## 7. Boyer-Moore Majority Vote Algorithm

```python
# ============================================
# Problem: Find element appearing more than n/2 times — O(n) time, O(1) space
# ============================================

def majority_element(arr):
    """Find majority element (appears > n/2 times)."""
    # Phase 1: Find candidate
    candidate = arr[0]
    count = 1
    
    for i in range(1, len(arr)):
        if arr[i] == candidate:
            count += 1
        else:
            count -= 1
            if count == 0:
                candidate = arr[i]
                count = 1
    
    # Phase 2: Verify candidate
    count = sum(1 for x in arr if x == candidate)
    if count > len(arr) // 2:
        return candidate
    return -1  # No majority

print(majority_element([3, 3, 4, 2, 3, 3, 3]))  # 3
print(majority_element([1, 2, 3, 4]))  # -1

# ============================================
# Problem: Elements appearing more than n/3 times
# ============================================
def majority_elements_n3(arr):
    """Find elements appearing > n/3 times (at most 2 such elements)."""
    # Phase 1: Find candidates
    candidate1 = candidate2 = None
    count1 = count2 = 0
    
    for x in arr:
        if candidate1 == x:
            count1 += 1
        elif candidate2 == x:
            count2 += 1
        elif count1 == 0:
            candidate1, count1 = x, 1
        elif count2 == 0:
            candidate2, count2 = x, 1
        else:
            count1 -= 1
            count2 -= 1
    
    # Phase 2: Verify
    result = []
    for c in [candidate1, candidate2]:
        if c is not None and arr.count(c) > len(arr) // 3:
            result.append(c)
    
    return result

print(majority_elements_n3([1, 1, 1, 3, 3, 2, 2, 2]))  # [1, 2]

# ============================================
# When to use: Finding majority elements, frequency problems
# ============================================
```

## 8. Fisher-Yates Shuffle

```python
import random

# ============================================
# Problem: Shuffle an array uniformly at random — O(n)
# ============================================

def fisher_yates_shuffle(arr):
    """In-place unbiased shuffle."""
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(fisher_yates_shuffle(arr))

# ============================================
# Shuffle with seed for reproducibility
# ============================================
random.seed(42)
arr = [1, 2, 3, 4, 5]
fisher_yates_shuffle(arr)
print(arr)  # Same result every time with seed 42

# ============================================
# CP Usage: Random testing, randomized algorithms
# ============================================

# When to use: Testing, random sampling, game theory problems
```

## 9. Union-Find Template

```python
# ============================================
# Union-Find (Disjoint Set Union) — nearly O(1) per operation
# ============================================

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.num_components = n
    
    def find(self, x):
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank. Returns True if merged."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        
        self.num_components -= 1
        return True
    
    def connected(self, x, y):
        """Check if x and y are in same component."""
        return self.find(x) == self.find(y)
    
    def get_size(self, x):
        """Get size of component containing x."""
        return self.size[self.find(x)]

# ============================================
# Example: Number of islands
# ============================================
def num_islands(grid):
    if not grid:
        return 0
    
    n, m = len(grid), len(grid[0])
    uf = UnionFind(n * m)
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    water_count = 0
    
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 0:
                water_count += 1
                continue
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 1:
                    uf.union(r * m + c, nr * m + nc)
    
    # Count unique roots among land cells
    roots = set()
    for r in range(n):
        for c in range(m):
            if grid[r][c] == 1:
                roots.add(uf.find(r * m + c))
    
    return len(roots)

# ============================================
# Example: Accounts merge
# ============================================
def accounts_merge(accounts):
    from collections import defaultdict
    
    email_to_id = {}
    email_to_name = {}
    id_counter = 0
    
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            email_to_name[email] = name
            if email not in email_to_id:
                email_to_id[email] = id_counter
                id_counter += 1
    
    uf = UnionFind(id_counter)
    
    for account in accounts:
        first_email = account[1]
        for email in account[2:]:
            uf.union(email_to_id[first_email], email_to_id[email])
    
    groups = defaultdict(list)
    for email, id in email_to_id.items():
        root = uf.find(id)
        groups[root].append(email)
    
    return [[email_to_name[emails[0]]] + sorted(emails)
            for emails in groups.values()]

# ============================================
# When to use: Connected components, cycle detection in undirected graph
# ============================================
```

## 10. Topological Sort Template

```python
from collections import deque, defaultdict

# ============================================
# BFS-based Topological Sort (Kahn's Algorithm)
# ============================================

def topological_sort_bfs(n, edges):
    """
    n: number of nodes (0 to n-1)
    edges: list of (u, v) meaning u -> v
    Returns: topological order, or empty list if cycle exists
    """
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    order = []
    
    while queue:
        node = queue.popleft()
        order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(order) != n:
        return []  # Cycle exists!
    
    return order

# ============================================
# Example: Course schedule
# ============================================
def can_finish(num_courses, prerequisites):
    """Can you finish all courses?"""
    order = topological_sort_bfs(num_courses, prerequisites)
    return len(order) > 0

print(can_finish(4, [[1,0], [2,0], [3,1], [3,2]]))  # True
print(can_finish(2, [[1,0], [0,1]]))  # False — cycle

# ============================================
# DFS-based Topological Sort
# ============================================

def topological_sort_dfs(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
    
    visited = [0] * n  # 0=unvisited, 1=visiting, 2=done
    order = []
    
    def dfs(node):
        visited[node] = 1
        for neighbor in graph[node]:
            if visited[neighbor] == 1:
                return False  # Cycle detected!
            if visited[neighbor] == 0:
                if not dfs(neighbor):
                    return False
        visited[node] = 2
        order.append(node)
        return True
    
    for i in range(n):
        if visited[i] == 0:
            if not dfs(i):
                return []  # Cycle!
    
    return order[::-1]

# ============================================
# Example: Task ordering with dependencies
# ============================================
def task_order(tasks, dependencies):
    """Find valid order to complete tasks."""
    n = len(tasks)
    order = topological_sort_bfs(n, dependencies)
    return [tasks[i] for i in order] if order else []

tasks = ["A", "B", "C", "D"]
deps = [(0, 1), (0, 2), (1, 3), (2, 3)]  # A->B, A->C, B->D, C->D
print(task_order(tasks, deps))  # ['A', 'B', 'C', 'D'] or ['A', 'C', 'B', 'D']

# ============================================
# When to use: Task scheduling, build systems, course prerequisites
# ============================================
```

## 11. Binary Search on Answer

```python
# ============================================
# Pattern: Binary search on answer space
# When the answer is monotonic (if X works, X+1 also works or vice versa)
# ============================================

# Problem: Minimum capacity to ship packages within D days
def ship_within_days(weights, days):
    def can_ship(capacity):
        current_load = 0
        days_needed = 1
        
        for weight in weights:
            if current_load + weight > capacity:
                days_needed += 1
                current_load = 0
            current_load += weight
        
        return days_needed <= days
    
    lo = max(weights)
    hi = sum(weights)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(mid):
            hi = mid
        else:
            lo = mid + 1
    
    return lo

print(ship_within_days([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5))  # 15

# ============================================
# Problem: Koko eating bananas
# ============================================
def min_eating_speed(piles, h):
    def can_finish(speed):
        hours = 0
        for pile in piles:
            hours += (pile + speed - 1) // speed
        return hours <= h
    
    lo, hi = 1, max(piles)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid
        else:
            lo = mid + 1
    
    return lo

print(min_eating_speed([3, 6, 7, 11], 8))  # 4

# ============================================
# When to use: Optimization problems where answer has monotonic property
# ============================================
```

## 12. Quick Reference — When to Use Each Pattern

```
Pattern                    | When to Use
--------------------------|--------------------------------------------------
Prefix Sum                | Range sum queries, subarray sum problems
Two Pointer               | Sorted array pair finding, removing duplicates
Sliding Window            | Substring/subarray with constraints
Fast/Slow Pointer         | Linked list cycle, middle element
Dutch National Flag       | 3-way partition, sorting with 3 categories
Kadane's Algorithm        | Maximum/minimum subarray sum
Boyer-Moore               | Majority element (> n/2 or > n/3)
Fisher-Yates              | Array shuffling
Union-Find                | Connected components, cycle detection
Topological Sort          | Task scheduling, dependency resolution
Binary Search on Answer   | Optimization with monotonic property
```
