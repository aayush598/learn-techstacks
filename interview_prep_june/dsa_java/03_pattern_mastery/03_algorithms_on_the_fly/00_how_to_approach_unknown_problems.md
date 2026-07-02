# How to Approach Unknown Problems

## Table of Contents
1. The Step-by-Step Framework
2. Step 1: Understand the Problem
3. Step 2: Identify Input Size → Complexity Bound
4. Step 3: Brute Force First (Don't Code, Just Think)
5. Step 4: Look for Patterns/Constraints
6. Step 5: Map to Known Pattern
7. Step 6: Consider Data Structures Needed
8. Step 7: Code the Solution
9. Step 8: Test with Examples
10. Step 9: Optimize if Needed
11. The Mental Checklist

---

## 1. The Step-by-Step Framework

```
┌─────────────────────────────────────────────────────┐
│ 1. Understand the problem                          │
│    (Read carefully, clarify, write examples)        │
├─────────────────────────────────────────────────────┤
│ 2. Identify input size → complexity bound          │
│    (n ≤ 20, n ≤ 1000, n ≤ 10^5, etc.)              │
├─────────────────────────────────────────────────────┤
│ 3. Brute force first (think, don't code)           │
│    (What's the simplest way to solve?)              │
├─────────────────────────────────────────────────────┤
│ 4. Look for patterns/constraints                   │
│    (Sorted? Distinct? Range? Contiguous?)           │
├─────────────────────────────────────────────────────┤
│ 5. Map to known pattern                            │
│    (This looks like Sliding Window / DP / Graph)   │
├─────────────────────────────────────────────────────┤
│ 6. Consider data structures needed                 │
│    (HashMap, Heap, Stack, Queue, Set, etc.)         │
├─────────────────────────────────────────────────────┤
│ 7. Code the solution                               │
│    (Start coding, handle edge cases)                │
├─────────────────────────────────────────────────────┤
│ 8. Test with examples                              │
│    (Run through examples, check edge cases)         │
├─────────────────────────────────────────────────────┤
│ 9. Optimize if needed                              │
│    (Time/space trade-offs, prune search space)      │
└─────────────────────────────────────────────────────┘
```

---

## 2. Step 1: Understand the Problem

**Before coding, make sure you understand:**

### What is the input?
- Type: array, string, linked list, tree, graph
- Size: variable, fixed, constraints
- Properties: sorted, distinct, positive, range bound

### What is the output?
- Single value (max, min, count, boolean)
- Structure (list, tree, modified array)
- All valid solutions (backtracking)

### What are the rules?
- Read the problem statement 2-3 times
- Restate in your own words
- Write 1-2 examples with inputs and outputs
- Identify constraints and edge cases

### Clarifying questions to ask:
```
1. Can the input be empty/null? What should I return?
2. Are there duplicates? How should they be handled?
3. Is the input sorted? If not, can I sort it?
4. What if there's no valid answer?
5. Can I modify the input array/structure?
6. Are negative numbers allowed? Zero?
7. What is the expected time/space complexity?
```

**Example: "Given an array of integers, return indices of two numbers that add up to target."**

Clarify:
- Is the array sorted? (Not specified)
- Can there be multiple pairs? (Assume one)
- Can the same element be used twice? (No)
- What if no pair exists? (Assume one exists)

---

## 3. Step 2: Identify Input Size → Complexity Bound

The input size is the single biggest hint about the expected algorithm.

| Input Size | Allowed Complexity | Likely Algorithm |
|-----------|-------------------|-----------------|
| n ≤ 10 | O(n!), O(n⁶) | Brute force, permutations, subsets |
| n ≤ 20 | O(2ⁿ), O(n!) | Backtracking, bitmask DP |
| n ≤ 100 | O(n³), O(n² log n) | Floyd-Warshall, DP |
| n ≤ 1000 | O(n²) | DP, nested loops |
| n ≤ 10⁵ | O(n log n), O(n) | Sorting, binary search, greedy, two pointers |
| n ≤ 10⁶ | O(n), O(n log n) | Hash table, linear scan |
| n ≤ 10⁷ | O(n) | Single pass |
| n ≤ 10⁸ | O(log n), O(1) | Math, binary search |

**Examples:**
```
"n ≤ 10^5" → O(n) or O(n log n) expected → Sliding window, two pointers, heap, sort
"n ≤ 10" → Could be backtracking/bitmask → Try all subsets
"n ≤ 10^3" → O(n²) OK → Nested DP, interval DP
```

**Memory constraints:**
- Java: ~50M ints ≈ 200MB (usually too much)
- dp[1000][1000] ≈ 4MB (acceptable)
- dp[10000][10000] ≈ 400MB (too much)

---

## 4. Step 3: Brute Force First (Think, Don't Code)

"Brute force" means the simplest correct solution, not necessarily efficient.

**Why think brute force:**
- Ensures you understand the problem
- Gives you a correctness baseline
- Often reveals redundant work → optimization target
- Can be used for testing your optimal solution

**Example workflow:**
```
Problem: Longest Substring Without Repeating Characters

Brute force (think):
- Generate all substrings: O(n²)
- For each, check if all chars unique: O(n)
- Total: O(n³) → too slow

Observation:
- When sliding window has duplicate, all larger windows containing this 
  substring also have the duplicate
- We can skip them → sliding window O(n)
```

**Common brute forces:**
| Problem | Brute Force | Optimal |
|---------|-------------|---------|
| Two Sum | O(n²) check all pairs | O(n) HashMap |
| Max Subarray | O(n³) all subarrays | O(n) Kadane |
| LIS | O(2ⁿ) all subsets | O(n²) DP / O(n log n) |
| Edit Distance | O(3ⁿ) recursive | O(mn) DP |
| Longest Substr | O(n³) all substrings | O(n) sliding window |

---

## 5. Step 4: Look for Patterns/Constraints

### Keywords to Watch For

| Keyword | Suggests Pattern |
|---------|-----------------|
| "Contiguous subarray" | Sliding window, prefix sum, Kadane |
| "Subsequence" | DP (LCS, LIS) |
| "Sorted" | Binary search, two pointers |
| "Rotated" | Modified binary search |
| "Shortest/longest path" | BFS (unweighted), Dijkstra |
| "Count ways / max profit" | DP |
| "All subsets/permutations" | Backtracking |
| "Top/least K" | Heap, quickselect |
| "Overlapping intervals" | Merge intervals, sweep line |
| "Connected" | Union-Find, graph traversal |
| "Dependencies / prerequisites" | Topological sort |
| "Palindrome" | Two pointers, DP |
| "Anagram" | Frequency counting, hash map |
| "Find if there exists" | Set, HashMap, binary search |
| "Design a ..." | OOP + appropriate data structures |

### Constraint Patterns

| Constraint | Implication |
|-----------|-------------|
| "Non-negative" Range [1, n] | Could use array as hash, cyclic sort |
| Values in [0, n] | Cyclic sort or boolean array |
| "Exactly k" | Sliding window, two pointers |
| "At most k" | Sliding window with condition |
| "Increasing/decreasing" | Monotonic stack, LIS |
| "Without extra space" | In-place algorithms |
| "Linear time" | Hash table, two pointers |
| "O(log n)" | Binary search |

---

## 6. Step 5: Map to Known Pattern

### The Pattern Decision Tree

```
What is the data structure?
├── Array / String
│   ├── Looking for subarray/substring?
│   │   ├── YES → Sliding Window
│   │   └── NO → ↓
│   ├── Need pair/triplet?
│   │   ├── YES → Two Pointers (sort first)
│   │   └── NO → ↓
│   ├── Need to find max/min with condition?
│   │   ├── YES → Binary Search on Answer or DP
│   │   └── NO → ↓
│   ├── Looking for subsequence?
│   │   ├── YES → DP (LIS, LCS) or Two Pointers
│   │   └── NO → ↓
│   └── Need optimal path/sum?
│       └── YES → DP or Greedy
│
├── Linked List
│   ├── Reversal? → In-place reversal
│   ├── Cycle? → Fast & Slow
│   ├── Merge? → Two pointers or K-way merge
│   └── Palindrome? → Middle → Reverse → Compare
│
├── Tree
│   ├── Need property from children? → Post-order DFS
│   ├── Need level processing? → Level-order BFS
│   ├── BST in-order? → Sorted order
│   └── Serialize? → Preorder
│
├── Graph
│   ├── Shortest path? → BFS / Dijkstra / Bellman-Ford
│   ├── Dependencies? → Topological sort
│   ├── Activity? components → Union-Find
│   └── All paths? → DFS / Backtracking
│
└── None obvious?
    └── Backtracking (generate all), then optimize
```

---

## 7. Step 6: Consider Data Structures Needed

### Data Structure Decision Guide

| Need | Data Structure | Why |
|------|---------------|-----|
| O(1) lookup by key | HashMap | Fastest random access |
| Track frequency | HashMap / int[26] for chars | Count occurrences |
| Maintain order of insertion | LinkedHashMap | Predictable iteration |
| Sorted keys | TreeMap | O(log n) insert + sorted iteration |
| Unique elements | HashSet | O(1) add, contains, remove |
| First-in-first-out | Queue (LinkedList) | Level-order BFS |
| Last-in-first-out | Stack / ArrayDeque | DFS, matching problems |
| K largest/smallest | PriorityQueue (Heap) | O(log n) push/pop |
| Sliding window max/min | Deque | O(1) front/back operations |
| Fast parent finding | Union-Find | Near O(1) amortized |
| Prefix search | Trie | O(L) search by prefix |
| Range queries | Segment Tree / Fenwick Tree | O(log n) update/query |
| Store K-V with TTL | LinkedHashMap + timer | LRU Cache |

### Pattern + Data Structure Combos

| Pattern | Primary DS | Auxiliary DS |
|---------|-----------|-------------|
| Sliding window | int[] freq / HashMap | Deque (for min/max) |
| Two pointers | Array pointers | None or HashSet |
| Binary search | None | Arrays.sort |
| Backtracking | List for path | boolean[] used |
| Graph BFS | Queue | boolean[] visited |
| Graph Dijkstra | PriorityQueue | int[] dist |
| Union-Find | int[] parent | int[] rank |
| Top K | PriorityQueue | HashMap for freq |
| LRU Cache | LinkedHashMap | DoublyLinkedList |
| Monotonic Stack | Stack/Deque | int[] result |

---

## 8. Step 7: Code the Solution

### Coding Tips
1. **Define method signature first**
2. **Handle edge cases upfront** (null, empty, single element)
3. **Use meaningful variable names** (left/right, slow/fast, curr/prev)
4. **Write comments for non-obvious logic** (in interviews, explain as you go)
5. **Start with a simple version, then optimize**

### Edge Cases Checklist
```
[ ] Empty input / null
[ ] Single element
[ ] All same values
[ ] Already sorted
[ ] Reverse sorted
[ ] Negative numbers
[ ] Overflow
[ ] Duplicates
[ ] Target not present
[ ] Large input size
[ ] Minimum/maximum constraints
```

---

## 9. Step 8: Test with Examples

### Dry Run Process
1. Trace through your example step by step
2. Check that each variable updates correctly
3. Verify the output matches expected

### Example: Two Sum (HashMap approach)
```
nums = [2, 7, 11, 15], target = 9

Step 1: map = {}
Step 2: i=0, nums[0]=2, need=9-2=7, 7 not in map → map.put(2,0)
Step 3: i=1, nums[1]=7, need=9-7=2, 2 in map → return [0, 1]
```

### What to test:
- Given example from problem
- Simple case (n = 1, 2)
- Edge case (all same, empty)
- No valid answer
- Large values (overflow check)

---

## 10. Step 9: Optimize if Needed

### Optimization Techniques

| Technique | When to Use | Example |
|-----------|------------|---------|
| Space-time tradeoff | Repeated calculations | DP (memoization) |
| Preprocessing | Multiple queries on same data | Prefix sum, sorting |
| Two-pass to one-pass | Need left + right info | Product except self |
| Early termination | Result found before full traversal | Kth smallest |
| Lazy evaluation | Expensive operations | Deferred counting |
| In-place operations | Memroy constrained | Array modification |
| Pruning | Search problems | Backtracking bounds |

### After optimization, verify:
- Correctness still holds
- Edge cases still pass
- Complexity meets requirements

---

## 11. The Mental Checklist

### 30-Second Initial Scan
```
[ ] What is the input type?
[ ] What is the output?
[ ] Input size → complexity bound
[ ] Keywords suggesting a pattern
[ ] Edge cases
```

### 2-Minute Pattern Matching
```
[ ] Brute force identified
[ ] Redundant work identified
[ ] Pattern mapped from constraint keywords
[ ] Data structures selected
```

### When Stuck
```
1. Write a brute force solution first (never leave a blank page)
2. Try a simpler version of the problem (1D instead of 2D, ignore one constraint)
3. Work backward from the output (what do I need to compute this?)
4. Draw it out (visualize on paper/whiteboard)
5. Think about subproblems (what would help me solve this?)
6. What would a human do with a giant sheet of paper?
7. Check if you've seen a similar problem (reduce to known)
```

### The 5-Minute Rule
If you can't identify a pattern in 5 minutes:
- Pick the most obvious pattern (usually brute force or greedy)
- Start coding the brute force
- Optimize as you go
- Most interview problems have at least an O(n²) or O(2ⁿ) solution that works
