# Scoring & Band Allocation Strategy — Infosys SP/DSE Exam

## How Band Mapping Works

Your band is NOT determined by total marks alone. It's determined by **which difficulty levels you solve**.

### Band Determination Logic

```
┌──────────────────────────────────────────────────────────┐
│                    BAND ALLOCATION FLOW                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Solved Easy only?          → DSE  (₹6.25 LPA)          │
│  Solved Easy + Medium?      → DSE (strong) / SP L1       │
│  Solved up to Hard?         → SP L1 (₹10 LPA)           │
│  Solved Hard + Complex?     → SP L2 (₹16 LPA)           │
│  All problems optimal?      → SP L3 (₹21 LPA)           │
│                                                          │
│  Note: Exact boundaries vary by drive and competition.   │
│  Always aim higher than your target band.                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Marks Distribution (Typical)

| Problem | Tier | Max Marks | % of Total |
|---------|------|-----------|------------|
| Problem 1 | Easy | 100 | ~11% |
| Problem 2 | Medium | 200 | ~22% |
| Problem 3 | Hard | 300 | ~33% |
| Problem 4 | Complex | 300 | ~33% |
| **Total** | | **900** | **100%** |

> Note: Exact marks vary by drive. The ratio matters more than absolute numbers.

---

## Partial Scoring Optimization

### The Golden Rule

```
ALWAYS SUBMIT BRUTE FORCE BEFORE TRYING TO OPTIMIZE
```

### Why Partial Scoring Changes Everything

| Scenario | Brute Force | Optimal | Winner |
|----------|------------|---------|--------|
| Submit only optimal (fails) | 0 marks | 0 marks | ❌ Nothing |
| Submit only brute force | 60 marks | 0 marks | ✅ Brute force |
| Submit brute, then optimal | 60 marks | 100 marks | ✅ Optimal |
| Submit optimal, then brute | 0 marks | 60 marks | ✅ Brute force |

### Partial Scoring Strategy by Problem

#### Easy Problem (100 marks)
```
Time: 0-25 minutes
Strategy:
  1. Write brute force (5 min) → Submit → Gets ~80-100 marks
  2. Optimize if needed (10 min) → Resubmit → Gets 100 marks
  3. Move on — don't spend more time

Expected: 80-100 marks (80-100%)
```

#### Medium Problem (200 marks)
```
Time: 25-85 minutes
Strategy:
  1. Write brute force (10 min) → Submit → Gets ~100-120 marks
  2. Optimize approach (15 min) → Write optimized code
  3. Test thoroughly (10 min) → Resubmit → Gets ~160-200 marks
  4. Move on

Expected: 140-200 marks (70-100%)
```

#### Hard Problem (300 marks)
```
Time: 85-145 minutes
Strategy:
  1. Write brute force (10 min) → Submit → Gets ~90-150 marks
  2. Design optimal approach (15 min) → Code it
  3. Debug & test (15 min) → Resubmit → Gets ~240-300 marks
  4. If optimal fails, keep brute force submission

Expected: 150-300 marks (50-100%)
```

#### Complex Problem (300 marks)
```
Time: 145-170 minutes
Strategy:
  1. Write brute force immediately (10 min) → Submit → Gets ~60-120 marks
  2. Try optimization only if time permits
  3. Don't get stuck — partial marks here are bonus

Expected: 60-180 marks (20-60%)
```

---

## Edge Cases to Always Test

### Universal Edge Cases (Every Problem)

```python
# These edge cases appear in ALMOST every problem:

# 1. Empty / Zero input
n = 0          # Empty array
arr = []       # No elements

# 2. Single element
n = 1
arr = [5]      # Only one element

# 3. Two elements
n = 2
arr = [1, 2]   # Minimum for pair operations

# 4. All elements same
arr = [5, 5, 5, 5, 5]

# 5. Already sorted
arr = [1, 2, 3, 4, 5]

# 6. Reverse sorted
arr = [5, 4, 3, 2, 1]

# 7. Negative numbers
arr = [-3, -1, -4, -1, -5]

# 8. Maximum constraints
n = 10**5      # Largest possible input
```

### Problem-Type Specific Edge Cases

#### Arrays / Strings
```python
- Single character string: "a"
- Palindrome check: "a", "aa", "aba"
- All same characters: "aaaa"
- No repeating characters: "abcdef"
- Maximum length string (10^5 chars)
- Spaces in string (if applicable)
- Uppercase vs lowercase
```

#### Linked Lists
```python
- Empty list: None
- Single node: 1 -> None
- Two nodes: 1 -> 2 -> None
- Cycle in list (for cycle detection)
- Cycle at head (edge case for Floyd's)
- All same values
- Already sorted / reverse sorted
```

#### Trees / BST
```python
- Empty tree: None
- Single node
- Left-skewed tree (like linked list)
- Right-skewed tree
- Complete binary tree
- All same values
- Maximum depth tree
- LCA when nodes are same
```

#### Dynamic Programming
```python
- n = 0 or n = 1 (base cases)
- All elements = 0
- All elements = 1
- Very large n with small values
- Negative values (if applicable)
- Single element target match
```

#### Graphs
```python
- Single node graph
- Disconnected graph
- Graph with cycles
- Complete graph
- Self-loops
- Multiple edges between same nodes
- Directed vs undirected confusion
```

---

## Time & Space Complexity Targets

### For Each Difficulty Level

| Level | Time Target | Space Target | Acceptable |
|-------|------------|--------------|------------|
| **Easy** | O(n) or O(n log n) | O(n) | O(n²) might pass |
| **Medium** | O(n log n) or O(n) | O(n) | O(n²) borderline |
| **Hard** | O(n) or O(n log n) | O(n) | O(n²) usually fails |
| **Complex** | O(n) to O(n log n) | O(n) | Depends on constraints |

### Constraint → Complexity Guide

| Constraint (n) | Required Time | Allowed Algorithms |
|----------------|---------------|-------------------|
| n ≤ 10 | O(n!) | Brute force, permutations |
| n ≤ 20 | O(2ⁿ × n) | Bitmask DP, subsets |
| n ≤ 500 | O(n³) | Floyd-Warshall, interval DP |
| n ≤ 5000 | O(n²) | 2D DP, nested loops |
| n ≤ 10⁵ | O(n log n) | Sorting, binary search, segment trees |
| n ≤ 10⁶ | O(n) | Two-pointer, sliding window, hashing |
| n ≤ 10⁸ | O(1) or O(log n) | Math, bit manipulation |

### Python-Specific Complexity Considerations

```
⚠️ Python is ~10-50x slower than C++ for same algorithm.

Implications:
- If C++ solution at O(n) works, Python needs O(n) too
- O(n²) in Python fails at n=5000 (C++ might handle n=10000)
- Always aim for optimal — Python's speed disadvantage is real

Workarounds:
- Use sys.setrecursionlimit for deep recursion
- Use sys.stdin.readline for fast I/O
- Use list instead of string concatenation
- Use collections module (Counter, defaultdict, deque)
- Use heapq for priority queue operations
```

---

## When to Optimize vs When to Move On

### Decision Matrix

```
┌─────────────────────────────────────────────────────┐
│          OPTIMIZE vs MOVE ON DECISION                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Current solution passes < 50% test cases?          │
│    YES → Optimize if time left for this problem     │
│    NO  → Move on (you likely have enough marks)     │
│                                                     │
│  Time left for this problem > 15 min?               │
│    YES → Try optimization                           │
│    NO  → Move on, optimize later if time permits    │
│                                                     │
│  Optimization is a small change (e.g., add memo)?   │
│    YES → Do it now                                  │
│    NO  → Move on, come back if time                 │
│                                                     │
│  Already solved Easy + Medium fully?                │
│    YES → Spend extra time optimizing Hard/Complex   │
│    NO  → Go back and fully solve lower tiers first  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Priority Order for Optimization

```
1. Fix compilation errors (highest priority — free marks)
2. Fix wrong answer bugs on Easy/Medium (guaranteed marks)
3. Optimize Medium from brute force to optimal (easy wins)
4. Optimize Hard from brute force to optimal (big mark jump)
5. Optimize Complex (only if everything else is done)
```

---

## Python-Specific Tips for Maximum Score

### 1. Recursion Limit

```python
import sys
sys.setrecursionlimit(10**6)  # CRITICAL for recursive DP solutions

# Without this, any recursive solution with depth > 1000 WILL crash
# Most tree/graph DFS and recursive DP go beyond 1000 depth
```

### 2. Fast I/O

```python
import sys
input = sys.stdin.readline

# For reading large inputs:
n = int(input())
arr = list(map(int, input().split()))

# For multiple test cases:
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    # solve and print
```

### 3. Use Built-in Efficient Structures

```python
from collections import defaultdict, deque, Counter

# defaultdict — avoid key errors
d = defaultdict(int)        # default 0
d = defaultdict(list)       # default empty list

# deque — O(1) append/pop from both ends
q = deque()
q.append(1)         # O(1)
q.appendleft(1)     # O(1)
q.pop()             # O(1)
q.popleft()         # O(1)

# Counter — frequency counting in one line
freq = Counter(arr)  # {element: count}

# heapq — min heap (use negative for max heap)
import heapq
heap = []
heapq.heappush(heap, val)
min_val = heapq.heappop(heap)
```

### 4. String Operations

```python
# DON'T do this (O(n²) string concatenation):
result = ""
for s in strings:
    result += s        # BAD — creates new string each time

# DO this instead (O(n) total):
result = "".join(strings)  # GOOD — single allocation

# For building list of strings:
parts = []
for i in range(n):
    parts.append(str(arr[i]))
print(" ".join(parts))
```

### 5. Memoization for DP

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def dp(state):
    if base_case:
        return base_value
    # recursive case
    return optimize(dp(state1), dp(state2))

# Remember to convert unhashable args:
# For arrays/lists as DP state, convert to tuple:
@lru_cache(maxsize=None)
def dp(i, j, tuple(arr)):
    ...
```

### 6. Avoid Common Python Pitfalls

```python
# ❌ DON'T: Using 'in' on list (O(n) each time)
if x in my_list:  # O(n) per check → O(n²) in loop

# ✅ DO: Convert to set first
my_set = set(my_list)
if x in my_set:  # O(1) per check

# ❌ DON'T: Sorting when you don't need to
arr.sort()  # O(n log n) — only sort if necessary

# ✅ DO: Use heap for just finding min/max
import heapq
min_val = min(arr)  # O(n) — faster than sorting for single min

# ❌ DON'T: Using recursion for simple iteration
def solve(arr, i):
    if i == len(arr):
        return
    # process
    solve(arr, i + 1)

# ✅ DO: Use iteration when recursion isn't needed
for i in range(len(arr)):
    # process
```

---

## Final Scoring Summary

| Band | Minimum Score Needed | Strategy |
|------|---------------------|----------|
| **DSE** | ~30-40% total | Easy fully + partial Medium |
| **SP L1** | ~50-60% total | Easy + Medium fully + partial Hard |
| **SP L2** | ~70-80% total | All problems, Hard/Complex partial optimal |
| **SP L3** | ~85-95% total | All problems fully optimal |

### The Math

```
Total marks: ~900 (approximate)

DSE target:  270-360 marks  (solve Easy + partial Medium)
SP L1 target: 450-540 marks (solve Easy + Medium + partial Hard)
SP L2 target: 630-720 marks (solve all with 70-80% efficiency)
SP L3 target: 765-855 marks (solve all fully optimal)
```

> **Bottom line:** Partial scoring is your best friend. Never leave a problem blank. Always submit brute force. Then optimize if time permits.
