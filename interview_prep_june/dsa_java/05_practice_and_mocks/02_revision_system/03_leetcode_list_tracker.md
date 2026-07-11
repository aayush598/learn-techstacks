# LeetCode List Tracker & Effective Usage Guide

How to organize, track, and maximize your LeetCode practice for interview preparation.

---

## 1. Problem Organization

### By Topic & Pattern

```
ARRAYS & HASHING
├── Two Sum (1)
├── Contains Duplicate (217)
├── Product of Array Except Self (238)
├── Maximum Subarray (53)
├── Merge Intervals (56)
└── Non-overlapping Intervals (435)

TWO POINTERS
├── Valid Palindrome (125)
├── Two Sum II (167)
├── 3Sum (15)
├── Container With Most Water (11)
└── Trapping Rain Water (42)

SLIDING WINDOW
├── Best Time to Buy and Sell Stock (121)
├── Longest Substring Without Repeating Characters (3)
├── Minimum Window Substring (76)
└── Sliding Window Maximum (239)

BINARY SEARCH
├── Binary Search (704)
├── Search in Rotated Sorted Array (33)
├── Find Minimum in Rotated Sorted Array (153)
├── Search a 2D Matrix (74)
└── Koko Eating Bananas (875)

STACK
├── Valid Parentheses (20)
├── Min Stack (155)
├── Daily Temperatures (739)
├── Largest Rectangle in Histogram (84)
└── Car Fleet (853)

LINKED LIST
├── Reverse Linked List (206)
├── Merge Two Sorted Lists (21)
├── Linked List Cycle (141)
├── Reorder List (143)
└── LRU Cache (146)

TREES
├── Invert Binary Tree (226)
├── Maximum Depth of Binary Tree (104)
├── Binary Tree Level Order Traversal (102)
├── Validate BST (98)
├── Lowest Common Ancestor (236)
└── Serialize and Deserialize Binary Tree (297)

GRAPH
├── Number of Islands (200)
├── Clone Graph (133)
├── Course Schedule (207)
├── Pacific Atlantic Water Flow (417)
└── Alien Dictionary (269)

HEAP / PRIORITY QUEUE
├── Kth Largest Element (215)
├── Find Median from Data Stream (295)
├── Task Scheduler (621)
└── Reorganize String (767)

DYNAMIC PROGRAMMING
├── Climbing Stairs (70)
├── Coin Change (322)
├── Longest Increasing Subsequence (300)
├── Unique Paths (62)
├── Word Break (139)
└── Edit Distance (72)

GREEDY
├── Jump Game (55)
├── Jump Game II (45)
├── Gas Station (134)
├── Hand of Straights (846)
└── Valid Parenthesis String (678)

BACKTRACKING
├── Subsets (78)
├── Combination Sum (39)
├── Permutations (46)
├── Word Search (79)
└── N-Queens (51)

TRIE
├── Implement Trie (208)
├── Design Add and Search Words (211)
└── Word Search II (212)
```

---

## 2. Review Strategy

### Problem Categories

```
NEW PROBLEMS (Never seen before)
├── Solve without hints
├── Time yourself (target: 20 min easy, 35 min medium, 50 min hard)
├── If stuck > 50% of target time: read hints, then solve
├── Track: solved/attempted, time taken, hints used

REVIEW PROBLEMS (Previously solved)
├── Re-solve from memory (no peeking at solution)
├── Target: solve in < 10 min for easy, < 20 min for medium
├── If you can't solve: re-read solution, then re-solve tomorrow
├── Track: time to solve, confidence level (1-5)

COMPANY-SPECIFIC
├── Filter by company tag (LeetCode Premium)
├── Prioritize by frequency (solve high-frequency first)
├── Group by company for focused prep
├── Track: company, difficulty, your score

PATTERN PRACTICE
├── Pick one pattern per session
├── Solve 3-4 problems of same pattern
├── Note common templates and tricks
├── Build muscle memory for pattern recognition
```

### Spaced Repetition Schedule

```
Day 0:  Solve problem → note solution approach
Day 1:  Re-solve from memory
Day 3:  Re-solve from memory
Day 7:  Re-solve from memory
Day 14: Re-solve from memory
Day 30: Re-solve from memory

If you fail any review: restart from Day 1
If you pass all: move to "mastered" category
```

---

## 3. Progress Tracking

### Weekly Tracker Template

```markdown
## Week of [DATE]

### Target: 15-20 problems

| # | Problem | Topic | Difficulty | Status | Time | Hints |
|---|---------|-------|------------|--------|------|-------|
| 1 | Two Sum | Array/HashMap | Easy | ✅ | 8 min | No |
| 2 | 3Sum | Two Pointer | Medium | ✅ | 25 min | No |
| 3 | Container With Most Water | Two Pointer | Medium | ✅ | 18 min | No |
| 4 | Trapping Rain Water | Stack/Two Pointer | Hard | ❌→✅ | 45 min | Yes |
| 5 | Valid Parentheses | Stack | Easy | ✅ | 5 min | No |
| ... | ... | ... | ... | ... | ... | ... |

### Summary
- Total attempted: 20
- First-try solve rate: 75%
- Average time: 18 min
- Patterns practiced: Two Pointer, Stack, Sliding Window
- Weak areas: Hard problems, dynamic programming
```

### Monthly Dashboard

```markdown
## Month of [DATE]

### Overall Stats
- Total problems solved: 72
- Easy: 30/50 (60%)
- Medium: 35/75 (47%)
- Hard: 7/30 (23%)

### By Topic
| Topic | Solved | Accuracy | Avg Time | Confidence |
|-------|--------|----------|----------|------------|
| Array | 15 | 85% | 12 min | ⭐⭐⭐⭐ |
| String | 8 | 70% | 15 min | ⭐⭐⭐ |
| Tree | 10 | 80% | 20 min | ⭐⭐⭐⭐ |
| Graph | 5 | 60% | 30 min | ⭐⭐⭐ |
| DP | 8 | 50% | 35 min | ⭐⭐ |
| Greedy | 6 | 75% | 18 min | ⭐⭐⭐ |

### Weak Areas to Focus
- Dynamic Programming: state transitions
- Graph: topological sort, union-find
- Hard problems: need more practice with complex logic

### Goals for Next Month
- Solve 80+ problems
- Focus on DP patterns
- Improve Hard solve rate to 30%
```

---

## 4. Focus on Weak Areas

### Identifying Weaknesses

```java
// After each problem, rate yourself
enum Confidence {
    STUCK,       // Couldn't solve without help
    STRUGGLED,   // Solved but took too long or needed hints
    COMFORTABLE, // Solved in reasonable time
    EASY         // Solved quickly and correctly
}

// Track by pattern
Map<String, int[]> patternStats = new HashMap<>();
// key: pattern name, value: [solved, total, avgTime]

// Identify patterns with lowest solve rate
patternStats.entrySet().stream()
    .sorted((a, b) -> {
        double rateA = (double) a.getValue()[0] / a.getValue()[1];
        double rateB = (double) b.getValue()[0] / b.getValue()[1];
        return Double.compare(rateA, rateB);
    })
    .forEach(e -> System.out.println(e.getKey() + ": " + 
        (double) e.getValue()[0] / e.getValue()[1] * 100 + "%"));
```

### Targeted Practice Plan

```
Week 1: Focus on weakest pattern (e.g., DP)
├── Day 1-2: Study DP templates (1D, 2D, knapsack)
├── Day 3-4: Solve 5 easy DP problems
├── Day 5-6: Solve 5 medium DP problems
└── Day 7: Review all DP problems solved

Week 2: Focus on second weakest (e.g., Graph)
├── Day 1-2: Study graph templates (BFS, DFS, Union-Find)
├── Day 3-4: Solve 5 easy graph problems
├── Day 5-6: Solve 5 medium graph problems
└── Day 7: Review all graph problems solved

Week 3: Mixed practice (all patterns)
├── Alternate between patterns
├── Include 1-2 hard problems
└── Review weak areas from weeks 1-2

Week 4: Mock interviews + review
├── 2 mock interviews (45 min each)
├── Review all problems from month
└── Retest problems you struggled with
```

---

## 5. LeetCode Features

### Filter by Company (Premium)

```
Top companies to filter by:
├── FAANG: Facebook, Apple, Amazon, Netflix, Google
├── Microsoft, Uber, Airbnb, Stripe, Twitter
├── Startup: Datadog, Snowflake, Databricks, Coinbase
└── Bank: Goldman Sachs, JPMorgan, Capital One

Strategy:
1. Filter by target company
2. Sort by acceptance rate (lower = harder but more representative)
3. Sort by frequency (higher = more likely to be asked)
4. Solve top 30 problems for each target company
```

### Filter by Frequency

```
High frequency problems are asked repeatedly at companies.
These are your highest priority.

Priority 1: Frequency > 500 (asked weekly at multiple companies)
Priority 2: Frequency 200-500 (asked monthly)
Priority 3: Frequency 50-200 (asked occasionally)
Priority 4: Frequency < 50 (rarely asked)
```

### Mock Interviews

```
LeetCode Mock Interview Schedule:
├── Weekly: 1 easy + 1 medium (45 min total)
├── Bi-weekly: 1 medium + 1 hard (60 min total)
├── Monthly: Full mock (2 problems, 45 min each)
└── Before interview: Simulate real interview conditions

During mock:
├── Time yourself strictly
├── No phone/distractions
├── Talk out loud (practice communication)
├── Write code on paper/whiteboard
└── Review solution after
```

### Discuss Section

```
Use Discuss to:
├── Learn alternative approaches
├── Understand common mistakes
├── Find optimal solutions
├── See different coding styles
└── Get unstuck (but only after attempting!)

When reading solutions:
├── Don't just copy — understand the logic
├── Note the pattern/template used
├── Add to your Anki cards
└── Re-solve tomorrow from memory
```

---

## 6. Session Plan

### Daily Session Template

```
Session Duration: 2-3 hours

Warm-up (15 min):
├── 1 easy problem from previously solved topic
├── Goal: get into problem-solving mode
└── Target: solve in < 10 min

New Problems (90 min):
├── 2 medium problems from current focus area
├── 1 hard problem (if confident) or 1 more medium
├── Time yourself for each
└── If stuck > 30 min: read hints, understand, then solve

Review (30 min):
├── Re-solve 2-3 problems from last week
├── Focus on problems you struggled with
└── Test memory retention

Reflection (15 min):
├── Update progress tracker
├── Note patterns learned
├── Identify weak areas for next session
└── Set goals for tomorrow
```

### Weekly Schedule

```
Monday:    Arrays + Hashing (warm-up week)
Tuesday:   Two Pointers + Sliding Window
Wednesday: Binary Search + Stack
Thursday:  Linked List + Trees
Friday:    Graphs + BFS/DFS
Saturday:  Dynamic Programming
Sunday:    Review + Mock Interview
```

---

## 7. Weekly Targets

### Realistic Weekly Targets

```
Beginner (0-50 problems solved):
├── Target: 10 problems/week
├── Focus: Easy problems
├── Time: 1-2 hours/day
└── Goal: Build fundamentals

Intermediate (50-150 problems solved):
├── Target: 15 problems/week
├── Focus: Medium problems
├── Time: 2-3 hours/day
└── Goal: Pattern recognition

Advanced (150+ problems solved):
├── Target: 20 problems/week
├── Focus: Hard problems
├── Time: 2-4 hours/day
└── Goal: Optimize and speed

Interview prep (1-2 months out):
├── Target: 25 problems/week
├── Focus: Company-specific + weak areas
├── Time: 3-5 hours/day
└── Goal: Interview readiness
```

### Monthly Milestones

```
Month 1: Foundation
├── Solve 60 problems (mostly Easy + some Medium)
├── Master: Arrays, Strings, Two Pointers, Basic Trees
├── Confidence: 70% on Easy, 40% on Medium
└── Milestone: Can solve most Easy problems without help

Month 2: Pattern Building
├── Solve 80 problems (mix of Easy, Medium, Hard)
├── Master: Binary Search, Stack, Linked List, Basic DP
├── Confidence: 85% on Easy, 60% on Medium
└── Milestone: Recognize patterns quickly

Month 3: Speed & Accuracy
├── Solve 100 problems (focus on Medium + Hard)
├── Master: Advanced DP, Graph, Greedy, Backtracking
├── Confidence: 90% on Easy, 75% on Medium, 40% on Hard
└── Milestone: Can solve Medium problems in 20 min

Month 4: Interview Ready
├── Solve 60 problems (review + company-specific)
├── Master: All patterns, focus on weak areas
├── Confidence: 95% on Easy, 85% on Medium, 55% on Hard
└── Milestone: Can solve any Medium in 15 min, confident in interviews
```

---

## 8. Monthly Review

### Random Problem Retest

```
At end of each month:
├── Pick 3 random problems from each topic you've solved
├── Re-solve without looking at solution
├── Track: solve time, confidence, mistakes
└── Update your spaced repetition schedule

If you fail a retest:
├── Re-study the pattern
├── Solve 2-3 similar problems
├── Add to "needs review" list
└── Retest in 1 week
```

### Pattern Mastery Check

```java
// Self-assessment after each problem
public class ProblemReview {
    String problemName;
    String pattern;
    int difficulty;  // 1=easy, 2=medium, 3=hard
    int timeTaken;   // minutes
    boolean solvedWithoutHints;
    boolean solvedFirstTry;
    int confidenceLevel;  // 1-5

    // After 10+ problems of same pattern, calculate mastery
    public double getMasteryScore() {
        double firstTryRate = getFirstTryRate();
        double avgTimeScore = getAvgTimeScore();
        double confidenceScore = getAvgConfidence() / 5.0;
        return (firstTryRate * 0.4 + avgTimeScore * 0.3 + confidenceScore * 0.3) * 100;
    }
}

// Mastery levels
// 90-100%: Mastered — can solve any problem of this pattern
// 70-89%:  Proficient — solve most problems, struggle with hard
// 50-69%:  Developing — need more practice
// <50%:    Beginner — study pattern templates, solve easy problems first
```

### Retrospective Questions

```
Monthly Review Questions:
├── What patterns did I master this month?
├── What patterns am I still struggling with?
├── Which problems took too long? Why?
├── Did I solve any problems I couldn't solve before?
├── What new approaches did I learn?
├── Am I on track for my interview date?
├── Should I adjust my study plan?
└── What's my biggest weakness to focus on next month?
```

---

## 9. Problem Difficulty Strategy

### Difficulty Distribution

```
Easy problems: Foundation
├── Purpose: Build confidence, learn basic patterns
├── Target time: < 10 minutes
├── Expected accuracy: 90%+
├── When to stop: Can solve 90% of Easy in < 10 min

Medium problems: Core interview material
├── Purpose: Most asked in interviews, pattern recognition
├── Target time: < 25 minutes
├── Expected accuracy: 70%+
├── When to stop: Can solve 70% of Medium in < 25 min

Hard problems: Differentiator
├── Purpose: Stand out, handle tough interviews
├── Target time: < 45 minutes
├── Expected accuracy: 40%+
├── When to stop: Can solve 40% of Hard in < 45 min
```

### When to Move Up in Difficulty

```
Move to Medium when:
├── You can solve 90% of Easy problems
├── Average solve time for Easy is < 10 min
├── You recognize patterns quickly
└── You're not making silly mistakes

Move to Hard when:
├── You can solve 70% of Medium problems
├── Average solve time for Medium is < 25 min
├── You can optimize solutions to Medium
└── You're comfortable with advanced data structures
```

---

## 10. Common Mistakes to Avoid

```
❌ Solving problems passively (reading solutions without coding)
❌ Not timing yourself (no urgency = no improvement)
❌ Skipping Easy problems (they build fundamentals)
❌ Only solving one difficulty level
❌ Not reviewing solved problems
❌ Copying solutions without understanding
❌ Not tracking progress (no data = no improvement)
❌ Solving random problems without pattern focus
❌ Ignoring company-specific problems
❌ Not simulating interview conditions
```

```
✅ Solve actively (write code, not just read)
✅ Time every problem (builds speed)
✅ Mix Easy/Medium/Hard appropriately
✅ Review solved problems regularly
✅ Understand before copying
✅ Track everything (progress data = improvement)
✅ Focus on patterns, not just problems
✅ Filter by company and frequency
✅ Simulate real interview conditions
✅ Reflect on what you learned each session
```
