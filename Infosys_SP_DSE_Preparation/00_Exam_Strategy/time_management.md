# Time Management Strategy — Infosys SP/DSE Exam (3 Hours)

## Time Allocation Overview

| Phase | Problem Tier | Time Budget | Cumulative |
|-------|-------------|-------------|------------|
| Phase 1 | Easy | 30 minutes | 0:00 – 0:30 |
| Phase 2 | Medium | 60 minutes | 0:30 – 1:30 |
| Phase 3 | Hard | 60 minutes | 1:30 – 2:30 |
| Phase 4 | Complex | 25 minutes | 2:30 – 2:55 |
| Buffer | Review & Debug | 5 minutes | 2:55 – 3:00 |

---

## Detailed Phase Breakdown

### Phase 1: Easy Problem (0:00 – 0:30)

**Goal:** Solve completely and correctly in under 25 minutes, leaving 5 minutes buffer.

| Step | Time | Action |
|------|------|--------|
| Read problem | 3 min | Read full problem, identify input/output format |
| Identify pattern | 2 min | Determine if it's Arrays, Strings, or Hashing |
| Write brute force | 8 min | Write working solution (even if not optimal) |
| Test with examples | 3 min | Run all sample test cases manually |
| Optimize if needed | 5 min | If brute force is O(n²), try to bring to O(n) |
| Submit | 2 min | Compile check → submit |

**Rules for Phase 1:**
- Do NOT spend more than 25 minutes on Easy
- If you cannot solve Easy in 25 minutes, submit brute force and move on
- Easy problems are usually Array/String manipulation — patterns are straightforward
- Don't overthink — the solution is usually simple

**Common Easy Patterns to Recognize Quickly:**

```
✅ Two-pointer technique → Sorted array problems
✅ Sliding window → Subarray/substring problems
✅ HashMap counting → Frequency-based problems
✅ Prefix sum → Range sum queries
✅ Sorting → Pair/group problems
```

---

### Phase 2: Medium Problem (0:30 – 1:30)

**Goal:** Solve completely with optimal or near-optimal solution in 55 minutes.

| Step | Time | Action |
|------|------|--------|
| Read problem | 3 min | Read full problem, note constraints |
| Identify pattern | 5 min | Linked List? Tree? Basic DP? |
| Design approach | 7 min | Think through algorithm, consider edge cases |
| Write solution | 25 min | Code the full solution |
| Test & debug | 10 min | Run examples, check edge cases |
| Optimize | 5 min | If time/space is not optimal, optimize |

**Rules for Phase 2:**
- Medium problems are where most people get stuck — don't let this happen
- If after 15 minutes you have no clear approach, write brute force and move on
- Common Medium patterns: Linked List reversal, BST traversal, 1D DP, Stack-based problems
- Always handle edge cases: empty input, single element, negative numbers

**Common Medium Patterns:**

```
✅ Linked List → Fast/slow pointer, reversal, merge
✅ BST → Inorder traversal, LCA, validation
✅ Stack/Queue → Next greater element, parentheses
✅ Basic DP → Climbing stairs, house robber, coin change
✅ Recursion → Subsets, permutations, combinations
```

---

### Phase 3: Hard Problem (1:30 – 2:30)

**Goal:** Solve completely with optimal solution, or solve 60%+ test cases if full solution isn't possible.

| Step | Time | Action |
|------|------|--------|
| Read problem | 3 min | Read carefully, note ALL constraints |
| Identify pattern | 8 min | Advanced DP? Trees + DP? Backtracking? |
| Design approach | 10 min | Sketch algorithm on paper (mental or scratch) |
| Write solution | 25 min | Code optimal solution |
| Test & debug | 10 min | Test thoroughly |
| Partial submit | 4 min | If not fully working, submit partial |

**Rules for Phase 3:**
- This is the SP L1 differentiator — solving this gets you ₹10 LPA
- If you cannot find optimal approach, ALWAYS submit brute force for partial marks
- Don't spend more than 10 minutes debugging — if it's not working, submit what you have
- Partial scoring means 60% test cases passed > 0% (no submission)

**Common Hard Patterns:**

```
✅ 2D DP → LCS, edit distance, knapsack variants
✅ DP on strings → Palindrome, subsequences
✅ Advanced recursion → N-Queens, Sudoku solver
✅ Tree DP → Diameter, path sum variants
✅ Interval DP / Matrix chain multiplication
```

---

### Phase 4: Complex Problem (2:30 – 2:55)

**Goal:** Solve 30%+ test cases for partial marks, or fully solve if you're fast.

| Step | Time | Action |
|------|------|--------|
| Read problem | 2 min | Quick scan, identify if familiar pattern |
| Write brute force | 10 min | Always write brute force first |
| Optimize if possible | 8 min | Try to improve beyond brute force |
| Submit | 5 min | Submit whatever works |

**Rules for Phase 4:**
- Complex problems are SP L2/L3 differentiators
- Most candidates skip this — solving even partially gives you an edge
- Brute force on Complex often passes 20–40% test cases
- Don't waste time — if you don't recognize the pattern in 5 minutes, just write brute force

**Common Complex Patterns:**

```
✅ Graph algorithms → BFS/DFS on complex graphs
✅ Bitmask DP → Subset enumeration, TSP
✅ Advanced DP → Multi-dimensional, optimization
✅ Segment trees / Fenwick trees (rare but possible)
✅ String algorithms → Suffix arrays, KMP (rare)
```

---

## The "Move On" Decision Framework

Use this decision tree during the exam:

```
┌─────────────────────────────────────────┐
│          Problem Difficulty             │
├─────────────────────────────────────────┤
│                                         │
│  Easy: Solved in 25 min?                │
│    YES → Submit, move to Medium         │
│    NO  → Submit brute force, move on    │
│                                         │
│  Medium: Approach clear in 15 min?      │
│    YES → Code it, optimize, move to Hard│
│    NO  → Submit brute force, move to    │
│          Hard                           │
│                                         │
│  Hard: Approach clear in 20 min?        │
│    YES → Code it carefully              │
│    NO  → Write brute force, submit,     │
│          move to Complex                │
│                                         │
│  Complex: Recognize pattern in 5 min?   │
│    YES → Code optimal                   │
│    NO  → Brute force, submit, done      │
│                                         │
└─────────────────────────────────────────┘
```

---

## Debug Checklist

When your solution fails test cases, follow this checklist in order:

### 1. Compilation/Runtime Errors
```python
# Check these first:
- [ ] Indentation correct (Python-specific)
- [ ] All variables defined before use
- [ ] No division by zero possible
- [ ] sys.setrecursionlimit set (for recursive solutions)
- [ ] Correct function signature matches expected
```

### 2. Wrong Answer — Common Bugs
```python
# Check in this order:
- [ ] Off-by-one errors (n vs n-1, 0-indexed vs 1-indexed)
- [ ] Integer overflow (Python handles big ints, but check logic)
- [ ] Empty input handling (n=0, n=1 cases)
- [ ] Negative number handling
- [ ] Sorted vs unsorted assumption
- [ ] Duplicate elements handling
- [ ] Return type matches expected (int vs list vs string)
```

### 3. Time Limit Exceeded
```python
# Optimization checklist:
- [ ] Nested loops that can be reduced to single pass
- [ ] Redundant computations (use memoization/dp)
- [ ] String concatenation in loop (use list + join)
- [ ] Sorting when not needed
- [ ] Using O(n²) when O(n log n) or O(n) exists
```

### 4. Memory Limit Exceeded
```python
# Memory optimization:
- [ ] Unnecessary data structures created
- [ ] Deep copies when shallow copies work
- [ ] Global lists that grow unboundedly
- [ ] Recursion depth too high (use iterative approach)
```

---

## Handling Partial Scoring

### Strategy: Always Submit Something

```
┌────────────────────────────────────────────────┐
│              Partial Scoring Strategy           │
├────────────────────────────────────────────────┤
│                                                │
│  1. ALWAYS write brute force first             │
│  2. Submit brute force immediately             │
│  3. THEN try to optimize                       │
│  4. If optimization works, submit again        │
│  5. Final submission = best solution           │
│                                                │
│  Why? Because:                                 │
│  - 60% test cases passed = 60% of marks        │
│  - 0% test cases = 0 marks                     │
│  - Partial > Nothing, ALWAYS                    │
│                                                │
└────────────────────────────────────────────────┘
```

### What to Submit When Stuck

| Situation | Action |
|-----------|--------|
| Can't find optimal approach | Submit brute force immediately |
| Optimal code has bug, can't fix | Submit brute force, debug in parallel |
| Optimal works for 80% cases | Submit, don't waste time on remaining 20% |
| Time running out | Submit whatever you have |
| Code compiles but uncertain | Submit anyway — partial > 0 |

---

## Pre-Test Checklist

### Night Before

- [ ] Python environment tested (if using local IDE)
- [ ] Common imports template saved (copy-paste ready)
- [ ] `sys.setrecursionlimit(10**6)` tested
- [ ] Fast I/O template ready
- [ ] Calculator handy (for constraint analysis)
- [ ] Water bottle ready
- [ ] Good sleep (7+ hours)

### 30 Minutes Before

- [ ] Login to platform, verify credentials
- [ ] Stable internet connection tested
- [ ] Browser updated, no notifications
- [ ] Scratch paper and pen ready
- [ ] Timer visible (phone or second screen)
- [ ] Template code copied to clipboard

### When Exam Starts

- [ ] Read ALL problems first (5 minutes total scan)
- [ ] Identify which is Easy, Medium, Hard, Complex
- [ ] Start with Easy — build confidence
- [ ] Follow time allocation strictly
- [ ] Don't get emotional about any single problem
- [ ] Submit partial solutions — never leave blanks

---

## Template Code (Copy-Paste Ready)

```python
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations, permutations
from functools import lru_cache
import heapq

sys.setrecursionlimit(10**6)
input = sys.stdin.readline

# ===== YOUR SOLUTION GOES HERE =====

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    # Solution logic here
    print(result)

t = int(input()) if True else 1  # Set to 1 if single test case
for _ in range(t):
    solve()
```

> **Note:** Some problems have multiple test cases, some don't. Read the input format carefully before writing the driver code.
