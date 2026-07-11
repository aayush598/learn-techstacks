# Weak Area Analysis

## How to Identify Weak Areas

### Method 1: Topic Accuracy Analysis
After 50+ problems, calculate accuracy per topic:
```
Arrays:     42/50 = 84% ✅
Strings:    38/45 = 84% ✅
Trees:      25/35 = 71% ⚠️
DP:         15/30 = 50% ❌
Graphs:     12/25 = 48% ❌
```

### Method 2: Time Analysis
```
Average time per problem:
Arrays:     12 min ✅
Strings:    15 min ✅
Trees:      22 min ⚠️
DP:         35 min ❌
Graphs:     30 min ❌
```

### Method 3: Pattern Recognition Audit
For each pattern, rate yourself:
- **Sliding Window**: 5/5 (can solve any variant)
- **Two Pointers**: 4/5
- **Knapsack DP**: 2/5 (struggle)
- **Dijkstra**: 3/5

## Targeted Improvement Plan

### If DP is weak (most common):
1. **Week 1**: Master memoization on Fibonacci → coin change → climb stairs
2. **Week 2**: Learn DP patterns (knapsack, LCS, LIS, interval)
3. **Week 3**: Solve 5 DP problems daily, categorize by pattern
4. **Week 4**: Re-solve week 1-2 problems from memory

### If Graphs are weak:
1. Master BFS/DFS on grid (number of islands = 5 times)
2. Learn adjacency list representation
3. Master Dijkstra on grid and graph
4. Topological sort for dependency problems

### If Trees are weak:
1. Code all traversals (recursive + iterative) daily for a week
2. BST operations (insert, delete, validate)
3. Tree construction from traversals

## The 80/20 Rule

80% of interview problems come from 20% of patterns:
1. **HashMap** (frequency, two-sum, grouping)
2. **Sliding Window** (substrings, subarrays)
3. **Two Pointers** (sorted arrays, linked lists)
4. **Binary Search** (search + answer optimization)
5. **BFS/DFS** (trees and graphs)
6. **DP Basics** (1D, knapsack, LCS)

Master these 6 patterns first before deep-diving into niche topics.

## When to Move On vs. Drill Deeper

**Move on** if:
- You can solve 60%+ of medium problems in the topic within 25 minutes
- You can identify the pattern within 2 minutes of reading the problem

**Drill deeper** if:
- Below 40% accuracy
- Take >30 minutes per problem
- Can't identify the pattern without hints
