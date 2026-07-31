# Infosys SP/DSE Exam Pattern 2026

## Overview

| Detail | Info |
|--------|------|
| **Conducting Body** | Infosys |
| **Exam Name** | HackWithInfy (SP/DSE Hiring) |
| **Total Duration** | 3 Hours |
| **Number of Problems** | 3–4 Coding Problems |
| **Languages Allowed** | Python 3, Java, C++, C |
| **Platform** | HackerEarth or Infosys Wingspan |
| **Negative Marking** | None |
| **Partial Scoring** | Yes — passing test cases earn marks |
| **Mode** | Online (Remote / On-campus depending on drive) |

---

## Difficulty Mapping & Role Allocation

The exam is a single test, but your performance across difficulty tiers determines your band:

| Band | Role | CTC (Approx.) | What You Need to Solve |
|------|------|----------------|------------------------|
| **DSE** | Digital Specialist Engineer | ₹6.25 LPA | Easy + Medium problems (1–2 problems) |
| **SP L1** | Specialist Programmer L1 | ₹10 LPA | Easy + Medium + at least 1 Hard problem |
| **SP L2** | Specialist Programmer L2 | ₹16 LPA | Easy + Medium + Hard + partial Complex |
| **SP L3** | Specialist Programmer L3 | ₹21 LPA | All 3–4 problems with optimal solutions, including Complex |

### What This Means

- Solving only Easy → You land in DSE band (₹6.25 LPA)
- Solving Easy + Medium → Strong DSE, borderline SP L1
- Solving up to Hard → SP L1 (₹10 LPA) guaranteed
- Solving Hard + Complex (optimal) → SP L2/L3 (₹16–21 LPA)
- **SP L3 requires ALL problems solved with optimal time/space complexity**

---

## Topic Frequency Analysis (2022–2025 Drives)

Based on analysis of previous HackWithInfy and Infosys SP drive papers:

| Topic | Frequency | Difficulty Range | Priority |
|-------|-----------|------------------|----------|
| **Arrays & Strings** | ~28% | Easy → Medium | 🔴 Critical |
| **Dynamic Programming** | ~20% | Medium → Complex | 🔴 Critical |
| **Linked Lists** | ~12% | Easy → Medium | 🟡 High |
| **Trees & BST** | ~10% | Medium → Hard | 🟡 High |
| **Recursion & Backtracking** | ~9% | Medium → Hard | 🟡 High |
| **Sorting & Searching** | ~8% | Easy → Medium | 🟢 Medium |
| **Hashing / HashMap** | ~7% | Easy → Medium | 🟢 Medium |
| **Graphs (BFS/DFS)** | ~6% | Hard → Complex | 🟢 Medium |

### Key Observations

1. **Arrays + DP = ~48% of all questions.** Master these two and you cover nearly half the exam.
2. DP questions appear in every single Infosys drive. You cannot skip DP.
3. Linked Lists and Trees are the most common "Medium" tier questions.
4. Graphs appear rarely but almost always as Complex tier (SP L2/L3 level).
5. Hashing is almost always part of Easy or as a sub-technique in harder problems.

---

## Test Structure Breakdown

### Problem Distribution (Typical)

```
Problem 1: Easy (100 marks)       — Arrays / Strings / Hashing
Problem 2: Medium (200 marks)     — Linked List / Trees / Basic DP
Problem 3: Hard (300 marks)       — Advanced DP / Trees / Recursion
Problem 4: Complex (400 marks)    — Graphs / Bitmask DP / Multi-concept (optional in some drives)
```

> **Note:** Some drives have 3 problems, some have 4. The 4th problem (Complex) is often the differentiator for SP L2/L3.

### Scoring Weightage

- Easy problems are worth fewer marks but are quick to solve
- Hard and Complex problems carry significantly more weight
- **Partial test case scoring means even 60% on a Hard problem beats 0% on it**

---

## Python-Specific Exam Setup

### Pre-Exam Environment Checklist

```python
# First thing to write when exam starts:
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations, permutations
from functools import lru_cache
import heapq

# Increase recursion limit for recursive solutions
sys.setrecursionlimit(10**6)

# Fast I/O for Python
input = sys.stdin.readline
```

### Why This Matters

- Python's default recursion limit is 1000. Most Hard/Complex DP solutions need 10^5+ depth.
- Fast I/O (`sys.stdin.readline`) saves critical seconds on large inputs.
- Having all common imports ready saves time during the exam.

---

## Platform-Specific Notes

### HackerEarth

- Code editor with syntax highlighting
- Custom input/output support
- Test cases run after submission (not during)
- Compilation errors shown before execution
- **Tip:** Always compile-check before final submit

### Infosys Wingspan

- Integrated coding environment
- May have in-built test case validation
- Timer visible on screen
- Auto-save is NOT always reliable — copy code periodically

---

## Historical Cut-off Trends (Approximate)

| Year | DSE Cut-off (approx.) | SP L1 Cut-off (approx.) | SP L2/L3 Cut-off (approx.) |
|------|-----------------------|-------------------------|----------------------------|
| 2022 | 1 Easy problem | 1 Easy + 1 Medium | 3 problems optimal |
| 2023 | 1 Easy problem | 1 Easy + 1 Medium + partial Hard | 3–4 problems optimal |
| 2024 | 1 Easy + partial Medium | 2 problems clean | 3–4 problems clean |
| 2025 | 1 Easy + partial Medium | 2 problems clean + partial Hard | All problems optimal |

> **Trend:** Cut-offs are increasing every year. Don't aim for minimum — aim for maximum.

---

## Summary: What to Target

| Your Goal | Minimum Target | Ideal Target |
|-----------|---------------|--------------|
| DSE (₹6.25 LPA) | Solve Easy fully + partial Medium | Easy + Medium fully |
| SP L1 (₹10 LPA) | Easy + Medium + partial Hard | Easy + Medium + Hard fully |
| SP L2 (₹16 LPA) | All 3 problems | All problems, Hard optimal |
| SP L3 (₹21 LPA) | All problems + optimal | All problems + optimal + clean code |

**Bottom line:** If you want SP L3, you need to solve ALL 3–4 problems with optimal solutions. There is no shortcut.
