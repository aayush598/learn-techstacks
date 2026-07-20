# Greedy & Backtracking Problems — Infosys SP DSE Preparation

> **38 Problems** | Greedy (18) + Backtracking (20)
> Every problem: Statement → Approach → Code → Complexity → Tip

---

# ═══════════════════════════════════════════════════════════════
# PART A: GREEDY PROBLEMS (18)
# ═══════════════════════════════════════════════════════════════

---

## Problem 1 — Maximum Units on a Truck (Easy)

**Statement:** You have `n` boxes, each described by `[boxes_i, units_i]`. You have a truck with capacity `maxBoxes`. Return the **maximum total number of units** you can load.

**Approach:** Greedily pick boxes with the most units first. Sort by `units_i` descending, then take as many as capacity allows.

```python
def maximumUnits(boxTypes, truckCapacity):
    boxTypes.sort(key=lambda x: x[1], reverse=True)
    total = 0
    for boxes, units in boxTypes:
        take = min(boxes, truckCapacity)
        total += take * units
        truckCapacity -= take
        if truckCapacity == 0:
            break
    return total
```

- **Time:** O(n log n) | **Space:** O(1)
- **Tip:** Sort by units per box descending. Greedy is optimal here because every box position is interchangeable — no ordering constraint.

---

## Problem 2 — Best Time to Buy and Sell Stock (Easy)

**Statement:** Given `prices[i]` = price on day `i`. You may buy once and sell once. Return the **maximum profit**. Return 0 if no profit possible.

**Approach:** Track minimum price seen so far. At each day, compute `price - min_so_far` and update max profit.

```python
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit
```

- **Time:** O(n) | **Space:** O(1)
- **Tip:** This is the classic "track the minimum" greedy. You don't need to actually buy — just track the best possible profit.

---

## Problem 3 — Jump Game (Easy)

**Statement:** Array `nums[i]` = max jump length from index `i`. Starting at index 0, return `True` if you can reach the last index.

**Approach:** Track the farthest reachable index. If current index exceeds farthest, return False.

```python
def canJump(nums):
    farthest = 0
    for i, jump in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True
```

- **Time:** O(n) | **Space:** O(1)
- **Tip:** Greedily extend your reach. If `farthest >= last_index` at any point, you can stop early.

---

## Problem 4 — Lemonade Change (Easy)

**Statement:** Customers pay with `$5`, `$10`, or `$20` bills. Each lemonade costs `$5`. Return `True` if you can give every customer correct change (starting with no bills).

**Approach:** Track count of $5 and $10 bills. For $20, prefer giving one $10 + one $5 over three $5s.

```python
def lemonadeChange(bills):
    fives = tens = 0
    for b in bills:
        if b == 5:
            fives += 1
        elif b == 10:
            if fives == 0:
                return False
            fives -= 1
            tens += 1
        else:
            if tens > 0 and fives > 0:
                tens -= 1
                fives -= 1
            elif fives >= 3:
                fives -= 3
            else:
                return False
    return True
```

- **Time:** O(n) | **Space:** O(1)
- **Tip:** Always try to keep $5 bills since they are the most versatile for making change. Never break a $5 when you can break a $10.

---

## Problem 5 — Assign Cookies (Easy)

**Statement:** Each child `i` has greed `g[i]`; each cookie `j` has size `s[j]`. A child is content if `s[j] >= g[i]`. Maximize the number of content children.

**Approach:** Sort both arrays. Use two pointers to assign the smallest sufficient cookie to each child.

```python
def findContentChildren(g, s):
    g.sort()
    s.sort()
    child = cookie = 0
    while child < len(g) and cookie < len(s):
        if s[cookie] >= g[child]:
            child += 1
        cookie += 1
    return child
```

- **Time:** O(n log n + m log m) | **Space:** O(1)
- **Tip:** Always give the smallest cookie that satisfies a child — this preserves larger cookies for pickier children.

---

## Problem 6 — Maximum 69 Number (Easy)

**Statement:** Given a positive integer made of only `6` and `9`, you may change **at most one** digit. Return the **maximum number** you can obtain.

**Approach:** Convert to string, replace the first `6` with `9`, convert back.

```python
def maximum69Number(num):
    s = list(str(num))
    for i in range(len(s)):
        if s[i] == '6':
            s[i] = '9'
            break
    return int(''.join(s))
```

- **Time:** O(d) where d = digits | **Space:** O(d)
- **Tip:** Changing the leftmost `6` always gives the maximum number due to positional value.

---

## Problem 7 — Jump Game II (Medium)

**Statement:** Same as Jump Game but return the **minimum number of jumps** to reach the last index. Assume it's always possible.

**Approach:** BFS-style greedy: track the current range and the farthest reachable in the next jump.

```python
def jump(nums):
    jumps = end = farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == end:
            jumps += 1
            end = farthest
    return jumps
```

- **Time:** O(n) | **Space:** O(1)
- **Tip:** This is a "level-by-level" BFS done greedily. `end` marks the boundary of the current jump level.

---

## Problem 8 — Gas Station (Medium)

**Statement:** `gas[i]` = gas at station `i`, `cost[i]` = cost to travel to station `i+1`. Find the **starting station index** to complete a full circuit, or `-1` if impossible.

**Approach:** If total gas >= total cost, a solution exists. Track `tank` and reset when it goes negative — the next station is the new candidate.

```python
def canCompleteCircuit(gas, cost):
    total_tank = curr_tank = start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total_tank += diff
        curr_tank += diff
        if curr_tank < 0:
            start = i + 1
            curr_tank = 0
    return start if total_tank >= 0 else -1
```

- **Time:** O(n) | **Space:** O(1)
- **Tip:** The key insight: if the total surplus is non-negative, there IS exactly one valid starting point. When your tank goes negative, every station before (including current) cannot be the answer.

---

## Problem 9 — Task Scheduler (Medium)

**Statement:** You have tasks `['A','A','B','B']` and cooldown `n`. Between two same tasks, there must be at least `n` intervals. Return the **least number of intervals** to finish all tasks.

**Approach:** The most frequent task dictates the minimum. Formula: `max(len(tasks), (max_count - 1) * (n + 1) + count_of_max)`.

```python
from collections import Counter

def leastInterval(tasks, n):
    freq = Counter(tasks)
    max_freq = max(freq.values())
    max_count = sum(1 for v in freq.values() if v == max_freq)
    result = max(len(tasks), (max_freq - 1) * (n + 1) + max_count)
    return result
```

- **Time:** O(n) | **Space:** O(1) (at most 26 letters)
- **Tip:** The formula `(max_freq - 1) * (n + 1) + max_count` represents laying out the most frequent tasks with `n` gaps, then filling the last row. If other tasks fill all gaps, total tasks length dominates.

---

## Problem 10 — Queue Reconstruction by Height (Medium)

**Statement:** People described as `[h, k]` where `h` = height, `k` = number of people in front who are >= h. Reconstruct the queue.

**Approach:** Sort by height descending (ties by k ascending). Insert each person at index `k` in the result.

```python
def reconstructQueue(people):
    people.sort(key=lambda x: (-x[0], x[1]))
    queue = []
    for p in people:
        queue.insert(p[1], p)
    return queue
```

- **Time:** O(n²) | **Space:** O(n)
- **Tip:** Taller people are placed first and are unaffected by shorter people inserted later. Inserting at index `k` directly places them correctly relative to taller people.

---

## Problem 11 — Hand of Straights (Medium)

**Statement:** Alice has cards (integer array). Can she rearrange them into groups of `groupSize` where each group is a consecutive sequence?

**Approach:** Use a min-heap. Always try to form a group starting from the smallest card.

```python
import heapq
from collections import Counter

def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize != 0:
        return False
    count = Counter(hand)
    heap = list(count.keys())
    heapq.heapify(heap)
    while heap:
        first = heap[0]
        for i in range(groupSize):
            card = first + i
            if count[card] == 0:
                return False
            count[card] -= 1
            if count[card] == 0 and card != heap[0]:
                return False
            if count[card] == 0:
                heapq.heappop(heap)
    return True
```

- **Time:** O(n log n) | **Space:** O(n)
- **Tip:** Always start building a group from the smallest available card. If any card in the consecutive sequence is missing, it's impossible.

---

## Problem 12 — Minimum Number of Arrows to Burst Balloons (Medium)

**Statement:** Each balloon `[start, end]` is an interval. An arrow shot at position `x` bursts all balloons where `start <= x <= end`. Find the **minimum arrows** to burst all.

**Approach:** Sort by end. Shoot at the end of the first balloon; skip all overlapping ones.

```python
def findMinArrowShots(points):
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    for s, e in points[1:]:
        if s > end:
            arrows += 1
            end = e
    return arrows
```

- **Time:** O(n log n) | **Space:** O(1)
- **Tip:** This is the classic "interval scheduling" greedy — sorting by end point maximizes the number of non-overlapping intervals (and minimizes arrows).

---

## Problem 13 — Non-overlapping Intervals (Medium)

**Statement:** Given intervals, return the **minimum number to remove** so the rest don't overlap.

**Approach:** Sort by end. Count how many you can keep (non-overlapping). Answer = total - kept.

```python
def eraseOverlapIntervals(intervals):
    intervals.sort(key=lambda x: x[1])
    end = intervals[0][1]
    kept = 1
    for s, e in intervals[1:]:
        if s >= end:
            kept += 1
            end = e
    return len(intervals) - kept
```

- **Time:** O(n log n) | **Space:** O(1)
- **Tip:** Minimizing removals = maximizing non-overlapping kept. Same greedy as interval scheduling: sort by end.

---

## Problem 14 — Meeting Rooms II (Medium)

**Statement:** Given meetings `[start, end]`, return the **minimum number of conference rooms** required.

**Approach:** Sort start and end times separately. Use a sweep-line: if a meeting starts before another ends, you need another room.

```python
import heapq

def minMeetingRooms(intervals):
    intervals.sort()
    heap = []
    for s, e in intervals:
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)
        else:
            heapq.heappush(heap, e)
    return len(heap)
```

- **Time:** O(n log n) | **Space:** O(n)
- **Tip:** The heap always holds the end times of ongoing meetings. Its size = rooms needed at any point. `heapreplace` is O(log n) vs push+pop being O(2 log n).

---

## Problem 15 — Candy (Hard)

**Statement:** `n` children with ratings. Each child must have at least 1 candy. Children with higher rating get more candy than their neighbors. Return the **minimum total candy**.

**Approach:** Two passes: left-to-right (ensure right neighbor gets more if rating is higher), then right-to-left.

```python
def candy(ratings):
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return sum(candies)
```

- **Time:** O(n) | **Space:** O(n)
- **Tip:** The two-pass approach handles the "valley" case (a child lower than both neighbors gets 1 candy from both sides without conflict).

---

## Problem 16 — IPO (Hard)

**Statement:** You start with capital `w`. `n` projects each give `profits[i]` and require `capital[i]`. You can fund at most `k` projects. Return the **maximum capital** you can achieve.

**Approach:** Min-heap of affordable projects (by capital). Max-heap of profits from affordable ones. Pick best profit k times.

```python
import heapq

def findMaximizedCapital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))
    max_heap = []
    idx = 0
    for _ in range(k):
        while idx < len(projects) and projects[idx][0] <= w:
            heapq.heappush(max_heap, -projects[idx][1])
            idx += 1
        if not max_heap:
            break
        w -= heapq.heappop(max_heap)
    return w
```

- **Time:** O(n log n) | **Space:** O(n)
- **Tip:** Two-heap approach: min-heap to filter affordable, max-heap to greedily pick the most profitable. This is essentially a priority queue-based greedy.

---

## Problem 17 — Minimum Cost to Hire K Workers (Hard)

**Statement:** Each worker has `quality[i]` and `wage[i]` (minimum wage). A "paid ratio" is `wage/quality`. Form a group of K workers where all are paid by the same ratio. Return the **minimum total cost**.

**Approach:** Sort by ratio `wage/quality`. Use a max-heap of quality. For each worker as the "ratio-setter", maintain the K smallest qualities.

```python
import heapq

def mincostToHireWorkers(quality, wage, k):
    workers = sorted([(w / q, q) for q, w in zip(quality, wage)])
    heap = []
    total_q = 0
    result = float('inf')
    for ratio, q in workers:
        heapq.heappush(heap, -q)
        total_q += q
        if len(heap) > k:
            total_q += heapq.heappop(heap)
        if len(heap) == k:
            result = min(result, ratio * total_q)
    return result
```

- **Time:** O(n log n) | **Space:** O(n)
- **Tip:** By fixing the ratio (using the highest-ratio worker in the group), we only need to minimize total quality. Max-heap of size K keeps the smallest K qualities.

---

## Problem 18 — Course Schedule III (Hard)

**Statement:** `n` courses with `[duration, lastDay]`. Take a course before its lastDay. Return the **maximum number of courses** you can take.

**Approach:** Sort by end day. Use a max-heap of durations. If total time exceeds deadline, remove the longest course.

```python
import heapq

def scheduleCourse(courses):
    courses.sort(key=lambda x: x[1])
    heap = []
    total = 0
    for dur, end in courses:
        if total + dur <= end:
            heapq.heappush(heap, -dur)
            total += dur
        elif heap and -heap[0] > dur:
            total += heapq.heappop(heap) + dur
            heapq.heappush(heap, -dur)
    return len(heap)
```

- **Time:** O(n log n) | **Space:** O(n)
- **Tip:** This is a classic exchange argument greedy. If adding a course exceeds the deadline, swapping it with the longest course already chosen (if longer) can only improve or maintain the count while freeing time.

---

# ═══════════════════════════════════════════════════════════════
# PART B: BACKTRACKING PROBLEMS (20)
# ═══════════════════════════════════════════════════════════════

---

## Problem 19 — Subsets (Easy)

**Statement:** Given a list of **unique** integers, return all possible subsets (the power set).

**Approach:** At each element, choose to include or exclude it. Classic backtracking.

```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

- **Time:** O(n × 2ⁿ) | **Space:** O(n)
- **Tip:** Use `start` index to avoid duplicates. Each recursive call adds the current path to results before exploring further.

---

## Problem 20 — Subsets II (Easy)

**Statement:** Given a list of integers that **may contain duplicates**, return all unique subsets.

**Approach:** Sort first. Skip duplicate values at the same level.

```python
def subsetsWithDup(nums):
    nums.sort()
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

- **Time:** O(n × 2ⁿ) | **Space:** O(n)
- **Tip:** Sort + skip consecutive duplicates at the same recursion level. `i > start` ensures we only skip within the same level, not across levels.

---

## Problem 21 — Permutations (Easy)

**Statement:** Given a list of **unique** integers, return all possible permutations.

**Approach:** Swap-based or visited-array backtracking.

```python
def permute(nums):
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

- **Time:** O(n × n!) | **Space:** O(n)
- **Tip:** Track used elements to ensure each appears exactly once per permutation. The result has n! permutations.

---

## Problem 22 — Permutations II (Medium)

**Statement:** Given a list of integers that **may contain duplicates**, return all unique permutations.

**Approach:** Sort first. Skip duplicates at the same level.

```python
def permuteUnique(nums):
    nums.sort()
    result = []
    def backtrack(path, used):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            path.append(nums[i])
            backtrack(path, used)
            path.pop()
            used[i] = False
    backtrack([], [False] * len(nums))
    return result
```

- **Time:** O(n × n!) worst case | **Space:** O(n)
- **Tip:** The condition `nums[i] == nums[i-1] and not used[i-1]` ensures we skip a duplicate only when the previous identical element is not used in the current path (same level).

---

## Problem 23 — Letter Combinations of a Phone Number (Easy)

**Statement:** Given a string of digits `2-9`, return all possible letter combinations (phone keypad mapping).

**Approach:** Map digits to letters. Backtrack by appending each possible letter for each digit.

```python
def letterCombinations(digits):
    if not digits:
        return []
    mapping = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
               '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
    result = []
    def backtrack(index, path):
        if index == len(digits):
            result.append(''.join(path))
            return
        for ch in mapping[digits[index]]:
            path.append(ch)
            backtrack(index + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

- **Time:** O(4ⁿ × n) | **Space:** O(n)
- **Tip:** Each digit maps to 3-4 letters. The total combinations = product of all mapping lengths. Maximum 4⁷ = 16384 for 7 digits.

---

## Problem 24 — Combination Sum (Medium)

**Statement:** Given candidates (unique) and a target, return all unique combinations where candidates can be **reused** and sum to target.

**Approach:** Backtrack with `start` index. Allow reusing by passing `i` (not `i+1`) as next start.

```python
def combinationSum(candidates, target):
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])
            path.pop()
    candidates.sort()
    backtrack(0, [], target)
    return result
```

- **Time:** O(N^(T/M)) where N=candidates, T=target, M=min | **Space:** O(T/M)
- **Tip:** Sort + early break (`if candidates[i] > remaining: break`) prunes the search tree significantly.

---

## Problem 25 — Combination Sum II (Medium)

**Statement:** Given candidates (may have duplicates) and a target, return all unique combinations that sum to target. Each number used **at most once**.

**Approach:** Sort. Skip duplicates at same level. Use `i+1` to prevent reuse.

```python
def combinationSum2(candidates, target):
    candidates.sort()
    result = []
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()
    backtrack(0, [], target)
    return result
```

- **Time:** O(2ⁿ) | **Space:** O(target)
- **Tip:** Key difference from Combination Sum: `i+1` prevents reuse. The duplicate skip prevents same-level duplicates.

---

## Problem 26 — Combination Sum III (Medium)

**Statement:** Find all combinations of `k` numbers from 1-9 that sum to `n`. Each number used at most once.

**Approach:** Backtrack from 1 to 9. Prune when remaining < 0 or count exceeds k.

```python
def combinationSum3(k, n):
    result = []
    def backtrack(start, path, remaining):
        if len(path) == k and remaining == 0:
            result.append(path[:])
            return
        if len(path) > k or remaining < 0:
            return
        for i in range(start, 10):
            path.append(i)
            backtrack(i + 1, path, remaining - i)
            path.pop()
    backtrack(1, [], n)
    return result
```

- **Time:** O(C(9, k)) | **Space:** O(k)
- **Tip:** Since k ≤ 9 and numbers are 1-9, the search space is tiny. Early pruning on count and remaining makes this very efficient.

---

## Problem 27 — Palindrome Partitioning (Medium)

**Statement:** Given a string `s`, partition it such that every substring is a palindrome. Return all valid partitioning.

**Approach:** Backtrack: try every prefix. If palindrome, recurse on the remainder.

```python
def partition(s):
    result = []
    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if sub == sub[::-1]:
                path.append(sub)
                backtrack(end, path)
                path.pop()
    backtrack(0, [])
    return result
```

- **Time:** O(n × 2ⁿ) | **Space:** O(n)
- **Tip:** Precomputing palindrome checks (DP table) can reduce the O(n) check to O(1), but `sub == sub[::-1]` is fast enough for most cases.

---

## Problem 28 — Word Search (Medium)

**Statement:** Given a 2D board of characters and a word, return `True` if the word exists in the board. You can use each cell **at most once**.

**Approach:** DFS from each cell. Mark visited cells, explore 4 directions, backtrack.

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False
        temp = board[r][c]
        board[r][c] = '#'
        found = (dfs(r + 1, c, idx + 1) or dfs(r - 1, c, idx + 1) or
                 dfs(r, c + 1, idx + 1) or dfs(r, c - 1, idx + 1))
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

- **Time:** O(m × n × 4^L) where L = word length | **Space:** O(L)
- **Tip:** In-place marking (`'#'`) avoids a separate visited set. The 4^L factor is the branching factor at each step.

---

## Problem 29 — N-Queens (Medium)

**Statement:** Place `n` queens on an `n×n` chessboard so no two queens attack each other. Return all **distinct solutions**.

**Approach:** Backtrack row by row. Use sets to track used columns, positive diagonals, and negative diagonals.

```python
def solveNQueens(n):
    result = []
    cols = set()
    pos_diag = set()
    neg_diag = set()
    board = [['.'] * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = 'Q'
            backtrack(row + 1)
            board[row][col] = '.'
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)

    backtrack(0)
    return result
```

- **Time:** O(n!) | **Space:** O(n²)
- **Tip:** Diagonal property: cells on the same `\` diagonal have the same `row - col`; on the same `/` diagonal have the same `row + col`.

---

## Problem 30 — Sudoku Solver (Hard)

**Statement:** Fill a 9×9 Sudoku grid so each row, column, and 3×3 box contains 1-9 exactly. The input has empty cells marked as `'.'`. Guaranteed to have a unique solution.

**Approach:** Backtrack on empty cells. Try digits 1-9, validate row/col/box constraints.

```python
def solveSudoku(board):
    def is_valid(row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
            br, bc = 3 * (row // 3) + i // 3, 3 * (col // 3) + i % 3
            if board[br][bc] == num:
                return False
        return True

    def solve():
        for r in range(9):
            for c in range(9):
                if board[r][c] == '.':
                    for ch in '123456789':
                        if is_valid(r, c, ch):
                            board[r][c] = ch
                            if solve():
                                return True
                            board[r][c] = '.'
                    return False
        return True

    solve()
```

- **Time:** O(9^(empty cells)) worst case | **Space:** O(1) (in-place)
- **Tip:** Optimization: precompute which cells are empty and iterate only over them. Also, try digits that actually appear less frequently first.

---

## Problem 31 — Restore IP Addresses (Medium)

**Statement:** Given a string `s` of digits, restore all possible valid IP addresses.

**Approach:** Backtrack: try segments of length 1-3 at each position. Validate each segment.

```python
def restoreIpAddresses(s):
    result = []
    def backtrack(start, path):
        if len(path) == 4:
            if start == len(s):
                result.append('.'.join(path))
            return
        for length in range(1, 4):
            if start + length > len(s):
                break
            seg = s[start:start + length]
            if len(seg) > 1 and seg[0] == '0':
                break
            if int(seg) > 255:
                continue
            path.append(seg)
            backtrack(start + length, path)
            path.pop()
    backtrack(0, [])
    return result
```

- **Time:** O(1) (at most 3⁴ = 81 combinations) | **Space:** O(1)
- **Tip:** Leading zeros are invalid for segments longer than 1 character. The small search space makes this very fast.

---

## Problem 32 — Generate Parentheses (Medium)

**Statement:** Given `n` pairs of parentheses, generate all combinations of **well-formed** parentheses.

**Approach:** Backtrack: add `(` if count_open < n, add `)` if count_close < count_open.

```python
def generateParenthesis(n):
    result = []
    def backtrack(path, open_count, close_count):
        if len(path) == 2 * n:
            result.append(''.join(path))
            return
        if open_count < n:
            path.append('(')
            backtrack(path, open_count + 1, close_count)
            path.pop()
        if close_count < open_count:
            path.append(')')
            backtrack(path, open_count, close_count + 1)
            path.pop()
    backtrack([], 0, 0)
    return result
```

- **Time:** O(4ⁿ / √n) — Catalan number | **Space:** O(n)
- **Tip:** The Catalan number C(n) = (2n)! / ((n+1)! * n!) counts valid parentheses. For n=8, that's 1430 combinations.

---

## Problem 33 — Expression Add Operators (Hard)

**Statement:** Given a string of digits `num` and target `target`, insert `+`, `-`, or `*` between digits to form expressions that evaluate to target. Return all valid expressions.

**Approach:** Backtrack with tracking of previous operand (for multiplication precedence).

```python
def addOperators(num, target):
    result = []

    def backtrack(index, path, prev, curr):
        if index == len(num):
            if curr == target:
                result.append(path)
            return
        for i in range(index, len(num)):
            if i != index and num[index] == '0':
                break
            seg = num[index:i + 1]
            val = int(seg)
            if index == 0:
                backtrack(i + 1, seg, val, val)
            else:
                backtrack(i + 1, path + '+' + seg, val, curr + val)
                backtrack(i + 1, path + '-' + seg, -val, curr - val)
                backtrack(i + 1, path + '*' + seg, prev * val, curr - prev + prev * val)

    backtrack(0, '', 0, 0)
    return result
```

- **Time:** O(4ⁿ) (3 operators × n split points) | **Space:** O(n)
- **Tip:** For multiplication, undo the previous addition: `curr - prev + prev * val`. This handles operator precedence correctly without building an AST.

---

## Problem 34 — Word Search II (Hard)

**Statement:** Given a 2D board and a list of words, return all words from the list that can be found on the board. Each cell used at most once per word.

**Approach:** Build a Trie from the words. DFS from each cell following the Trie, pruning branches early.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

def buildTrie(words):
    root = TrieNode()
    for w in words:
        node = root
        for ch in w:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.word = w
    return root

def findWords(board, words):
    root = buildTrie(words)
    rows, cols = len(board), len(board[0])
    result = []

    def dfs(r, c, node):
        ch = board[r][c]
        if ch not in node.children:
            return
        node = node.children[ch]
        if node.word:
            result.append(node.word)
            node.word = None
        board[r][c] = '#'
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, node)
        board[r][c] = ch

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)
    return result
```

- **Time:** O(m × n × 3^L) where L = max word length | **Space:** O(total chars in words)
- **Tip:** Trie pruning is the key optimization — once a path doesn't match any word prefix, we stop. Setting `node.word = None` after finding prevents duplicates.

---

## Problem 35 — N-Queens II (Hard)

**Statement:** Same as N-Queens but return only the **count** of distinct solutions.

**Approach:** Same backtracking as N-Queens but increment a counter instead of storing board states.

```python
def totalNQueens(n):
    count = [0]
    cols = set()
    pos_diag = set()
    neg_diag = set()

    def backtrack(row):
        if row == n:
            count[0] += 1
            return
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            backtrack(row + 1)
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)

    backtrack(0)
    return count[0]
```

- **Time:** O(n!) | **Space:** O(n)
- **Tip:** Known answers: n=1→1, n=2→0, n=3→0, n=4→2, n=5→10, n=6→4, n=7→40, n=8→92, n=9→352.

---

## Problem 36 — Alien Dictionary (Hard)

**Statement:** Given a sorted list of words in an alien language, derive the character order (a valid topological sort of character dependencies).

**Approach:** Compare adjacent words to build directed edges. Then topological sort (Kahn's or DFS).

```python
from collections import defaultdict, deque

def alienOrder(words):
    adj = defaultdict(set)
    in_degree = {c: 0 for w in words for c in w}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if len(w1) > len(w2) and w1.startswith(w2):
            return ""
        for c1, c2 in zip(w1, w2):
            if c1 != c2 and c2 not in adj[c1]:
                adj[c1].add(c2)
                in_degree[c2] += 1

    queue = deque([c for c in in_degree if in_degree[c] == 0])
    order = []
    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return ''.join(order) if len(order) == len(in_degree) else ""
```

- **Time:** O(C) where C = total chars in all words | **Space:** O(1) (at most 26 chars)
- **Tip:** The invalid case `len(w1) > len(w2) and w1.startswith(w2)` catches the scenario where a longer word comes before its prefix — this is never valid in any ordering.

---

## Problem 37 — Factor Combinations (Hard)

**Statement:** Given an integer `n > 1`, return all possible factorizations (all ways to write n as a product of factors > 1).

**Approach:** Backtrack: try dividing by factors from `start` to `sqrt(remaining)`.

```python
def getFactors(n):
    result = []
    def backtrack(start, remaining, path):
        if path:
            result.append(path + [remaining])
        for i in range(start, int(remaining**0.5) + 1):
            if remaining % i == 0:
                path.append(i)
                backtrack(i, remaining // i, path)
                path.pop()
    backtrack(2, n, [])
    return result
```

- **Time:** O(√n × log n) branches | **Space:** O(log n)
- **Tip:** Only try factors up to `sqrt(remaining)` — if `i` is a factor, `remaining // i` is also a factor and will be handled naturally. Starting from `i` (not 2) ensures non-decreasing order.

---

## Problem 38 — Crossword Solver (Hard)

**Statement:** Given a crossword grid (2D array with `'+'` as blocked, `'-'` as empty, letters as filled) and a list of words, place all words on the board in across/down positions to fill all `'-'` cells.

**Approach:** Find all slots (horizontal/vertical consecutive empty cells). Backtrack: assign words to slots checking compatibility.

```python
def solveCrossword(board, words):
    rows, cols = len(board), len(board[0])

    def find_slots():
        slots = []
        # Horizontal
        for r in range(rows):
            count = 0
            for c in range(cols + 1):
                if c < cols and board[r][c] == '-':
                    count += 1
                else:
                    if count > 1:
                        slots.append(('h', r, c - count, count))
                    count = 0
        # Vertical
        for c in range(cols):
            count = 0
            for r in range(rows + 1):
                if r < rows and board[r][c] == '-':
                    count += 1
                else:
                    if count > 1:
                        slots.append(('v', r - count, c, count))
                    count = 0
        return slots

    def can_place(slot, word):
        direction, r, c, length = slot
        if len(word) != length:
            return False
        for i in range(length):
            cr = r + (i if direction == 'v' else 0)
            cc = c + (i if direction == 'h' else 0)
            if board[cr][cc] != '-' and board[cr][cc] != word[i]:
                return False
        return True

    def place(slot, word):
        direction, r, c, length = slot
        placed = []
        for i in range(length):
            cr = r + (i if direction == 'v' else 0)
            cc = c + (i if direction == 'h' else 0)
            if board[cr][cc] == '-':
                board[cr][cc] = word[i]
                placed.append((cr, cc))
        return placed

    def unplace(placed):
        for cr, cc in placed:
            board[cr][cc] = '-'

    def backtrack(idx, remaining_words):
        if not remaining_words:
            return True
        # Find first unfilled slot
        slots = find_slots()
        if not slots:
            return len(remaining_words) == 0
        slot = slots[0]
        for word in list(remaining_words):
            if can_place(slot, word):
                placed = place(slot, word)
                remaining_words.remove(word)
                if backtrack(idx + 1, remaining_words):
                    return True
                remaining_words.add(word)
                unplace(placed)
        return False

    word_set = set(words)
    backtrack(0, word_set)
    return board
```

- **Time:** O(m! × n) factorial in worst case | **Space:** O(m × n)
- **Tip:** Always pick the most constrained slot first (shortest or most pre-filled). Use a set for `remaining_words` for O(1) removal.

---

# ═══════════════════════════════════════════════════════════════
# CHEAT SHEET: GREEDY vs BACKTRACKING
# ═══════════════════════════════════════════════════════════════

| Aspect | Greedy | Backtracking |
|--------|--------|--------------|
| **Strategy** | Pick locally optimal, hope for global | Explore all paths, prune invalid |
| **When to use** | Matroid problems, exchange arguments | Constraint satisfaction, combinatorial |
| **Time** | Usually O(n log n) | Usually exponential |
| **Space** | Usually O(1) | O(depth of recursion) |
| **Key proof** | Exchange argument / greedy choice property | Pruning correctness |
| **Examples** | Interval scheduling, coin change (canonical), Huffman | N-Queens, Sudoku, Subset/Permutation |

---

# ═══════════════════════════════════════════════════════════════
# KEY PATTERNS FOR INFOSYS SP DSE
# ═══════════════════════════════════════════════════════════════

### Greedy Patterns:
1. **Sort by end → interval scheduling** (Problems 12, 13)
2. **Sort by value/ratio → priority queue** (Problems 16, 17, 18)
3. **Track min/max while scanning** (Problems 2, 3, 7, 8)
4. **Two-heap approach** (Problems 14, 16, 17)
5. **Frequency-based** (Problems 4, 9, 11)
6. **Two-pass scan** (Problem 15)

### Backtracking Patterns:
1. **Subset/Combination with start index** (Problems 19, 20, 24, 25, 26)
2. **Permutation with visited array** (Problems 21, 22)
3. **Grid DFS with in-place marking** (Problems 28, 34)
4. **Constraint satisfaction** (Problems 29, 30, 35)
5. **String partitioning** (Problems 27, 31, 32, 33)
6. **Trie + DFS** (Problem 34)

---

# ═══════════════════════════════════════════════════════════════
# COMPLEXITY QUICK REFERENCE
# ═══════════════════════════════════════════════════════════════

| # | Problem | Time | Space |
|---|---------|------|-------|
| 1 | Maximum Units Truck | O(n log n) | O(1) |
| 2 | Buy Sell Stock | O(n) | O(1) |
| 3 | Jump Game | O(n) | O(1) |
| 4 | Lemonade Change | O(n) | O(1) |
| 5 | Assign Cookies | O(n log n) | O(1) |
| 6 | Max 69 Number | O(d) | O(d) |
| 7 | Jump Game II | O(n) | O(1) |
| 8 | Gas Station | O(n) | O(1) |
| 9 | Task Scheduler | O(n) | O(1) |
| 10 | Queue Reconstruction | O(n²) | O(n) |
| 11 | Hand of Straights | O(n log n) | O(n) |
| 12 | Min Arrows Balloons | O(n log n) | O(1) |
| 13 | Non-overlapping Intervals | O(n log n) | O(1) |
| 14 | Meeting Rooms II | O(n log n) | O(n) |
| 15 | Candy | O(n) | O(n) |
| 16 | IPO | O(n log n) | O(n) |
| 17 | Min Cost K Workers | O(n log n) | O(n) |
| 18 | Course Schedule III | O(n log n) | O(n) |
| 19 | Subsets | O(n×2ⁿ) | O(n) |
| 20 | Subsets II | O(n×2ⁿ) | O(n) |
| 21 | Permutations | O(n×n!) | O(n) |
| 22 | Permutations II | O(n×n!) | O(n) |
| 23 | Letter Combinations | O(4ⁿ×n) | O(n) |
| 24 | Combination Sum | O(N^(T/M)) | O(T/M) |
| 25 | Combination Sum II | O(2ⁿ) | O(target) |
| 26 | Combination Sum III | O(C(9,k)) | O(k) |
| 27 | Palindrome Partition | O(n×2ⁿ) | O(n) |
| 28 | Word Search | O(m×n×4^L) | O(L) |
| 29 | N-Queens | O(n!) | O(n²) |
| 30 | Sudoku Solver | O(9^empty) | O(1) |
| 31 | Restore IP | O(1) | O(1) |
| 32 | Generate Parentheses | O(4ⁿ/√n) | O(n) |
| 33 | Expression Add Operators | O(4ⁿ) | O(n) |
| 34 | Word Search II | O(m×n×3^L) | O(total chars) |
| 35 | N-Queens II | O(n!) | O(n) |
| 36 | Alien Dictionary | O(C) | O(1) |
| 37 | Factor Combinations | O(√n×log n) | O(log n) |
| 38 | Crossword Solver | O(m!×n) | O(m×n) |

---

# ═══════════════════════════════════════════════════════════════
# INTERVIEW TIPS
# ═══════════════════════════════════════════════════════════════

### Greedy Problems — What to Say:
1. "Can I prove the greedy choice property?"
2. "Does sorting help reveal the structure?"
3. "Can I use an exchange argument to prove optimality?"
4. "Is this a matroid structure?"

### Backtracking Problems — What to Say:
1. "This is a combinatorial problem — let me think about the state space."
2. "At each step, I choose from a set of valid options."
3. "Let me define what 'valid' means and prune early."
4. "The base case is when I've made all n choices."

### Common Mistakes to Avoid:
- Greedy: Assuming greedy works when it doesn't (always verify or prove)
- Backtracking: Forgetting to undo state after recursive call (the pop/unplace step)
- Greedy: Not handling edge cases (empty input, single element)
- Backtracking: Not sorting input when duplicate handling is needed

---

> **Total: 38 problems | ~2100 lines | Ready for Infosys SP DSE**

# ═══════════════════════════════════════════════════════════════
# STEP-BY-STEP DRY RUNS (KEY PROBLEMS)
# ═══════════════════════════════════════════════════════════════

### Dry Run: Problem 2 — Buy Sell Stock
```
prices = [7, 1, 5, 3, 6, 4]

Day 0: p=7, min_price=7, max_profit=0
Day 1: p=1, min_price=1, max_profit=0
Day 2: p=5, min_price=1, max_profit=4  (buy@1 sell@5)
Day 3: p=3, min_price=1, max_profit=4
Day 4: p=6, min_price=1, max_profit=5  (buy@1 sell@6)
Day 5: p=4, min_price=1, max_profit=5

Answer: 5
Key insight: We never actually track buy/sell day,
just the running maximum profit.
```

### Dry Run: Problem 3 — Jump Game
```
nums = [2, 3, 1, 1, 4]

i=0: jump=2, farthest = max(0, 0+2) = 2
i=1: jump=3, farthest = max(2, 1+3) = 4
  4 >= last_index(4) => can reach end!

nums = [3, 2, 1, 0, 4]

i=0: jump=3, farthest = max(0, 0+3) = 3
i=1: jump=2, farthest = max(3, 1+2) = 3
i=2: jump=1, farthest = max(3, 2+1) = 3
i=3: jump=0, farthest = max(3, 3+0) = 3
i=4: i(4) > farthest(3) => return False!
  Cannot jump over the zero-gap at index 3.
```

### Dry Run: Problem 4 — Lemonade Change
```
bills = [5, 5, 5, 10, 20]

b=5:  fives=1, tens=0
b=5:  fives=2, tens=0
b=5:  fives=3, tens=0
b=10: fives=2, tens=1  (give one $5 change)
b=20: tens>0 && fives>0 => give $10+$5
      fives=1, tens=0

All customers served! Return True.

bills = [5, 5, 10, 10, 20]

b=5:  fives=1
b=5:  fives=2
b=10: fives=1, tens=1
b=10: fives=0, tens=2
b=20: need change for $20
  tens>0 && fives>0? No (fives=0)
  fives>=3? No (fives=0)
  => Return False!

Cannot give change for the $20 bill.
```

### Dry Run: Problem 7 — Jump Game II
```
nums = [2, 3, 1, 1, 4]

jumps=0, end=0, farthest=0

i=0: farthest = max(0, 0+2) = 2
  i==end(0) => jumps=1, end=2
i=1: farthest = max(2, 1+3) = 4
i=2: farthest = max(4, 2+1) = 4
  i==end(2) => jumps=2, end=4
i=3: farthest = max(4, 3+1) = 4

Loop ends (i < len-1 = 4)
Answer: 2 jumps
  Jump 1: index 0 -> index 1 (can reach up to index 2)
  Jump 2: index 1 -> index 4 (can reach up to index 4) done!
```

### Dry Run: Problem 8 — Gas Station
```
gas  = [1, 2, 3, 4, 5]
cost = [3, 4, 5, 1, 2]

diff = [-2, -2, -2, 3, 3]
total_tank = 0

i=0: curr_tank=-2 < 0 => start=1, curr_tank=0
i=1: curr_tank=-2 < 0 => start=2, curr_tank=0
i=2: curr_tank=-2 < 0 => start=3, curr_tank=0
i=3: curr_tank=3
i=4: curr_tank=6

total_tank=6 >= 0 => answer=3

Verification from station 3:
  3->4: gas=4, cost=1, tank=3
  4->0: gas=5, cost=2, tank=6
  0->1: gas=1, cost=3, tank=4
  1->2: gas=2, cost=4, tank=2
  2->3: gas=3, cost=5, tank=0  (Complete circuit!)
```

### Dry Run: Problem 9 — Task Scheduler
```
tasks = ['A','A','A','B','B','B'], n = 2

freq: A=3, B=3
max_freq = 3
max_count = 2 (both A and B have freq 3)

formula = (3-1) * (2+1) + 2 = 2*3 + 2 = 8
actual  = len(tasks) = 6
result  = max(6, 8) = 8

Layout with n=2 cooldown:
  Slot: 0  1  2  3  4  5  6  7
  A:    A  .  .  A  .  .  A  .
  B:    .  B  .  .  B  .  .  B
  Merged: A B . A B . A B = 8 intervals

Without formula: you might think 6 intervals work,
but the cooldown constraint forces idle slots.
```

### Dry Run: Problem 12 — Min Arrows Balloons
```
points = [[10,16],[2,8],[1,6],[7,12]]

Sorted by end: [[1,6],[2,8],[7,12],[10,16]]

arrows=1, end=6
  [2,8]:  2 <= 6? Yes (overlap) => skip
  [7,12]: 7 > 6?  Yes (no overlap) => arrows=2, end=12
  [10,16]: 10 > 12? No (overlap) => skip

Answer: 2 arrows
  Arrow 1 at x=6 bursts [1,6] and [2,8]
  Arrow 2 at x=12 bursts [7,12] and [10,16]
```

### Dry Run: Problem 15 — Candy
```
ratings = [1, 3, 2, 2, 1]

Pass 1 (left to right):
  candies = [1, 2, 1, 1, 1]
  r[1]=3 > r[0]=1 => c[1] = c[0]+1 = 2
  r[2]=2 < r[1]=3 => c[2] = 1 (no change)
  r[3]=2 = r[2]=2 => c[3] = 1 (no change)
  r[4]=1 < r[3]=2 => c[4] = 1 (no change)

Pass 2 (right to left):
  candies = [1, 2, 1, 2, 1]
  r[3]=2 > r[4]=1 => c[3] = max(1, c[4]+1) = 2
  r[2]=2 = r[3]=2 => no change
  r[1]=3 > r[2]=2 => c[1] = max(2, c[2]+1) = 2
  r[0]=1 < r[1]=3 => no change

Total = 1+2+1+2+1 = 7
```

### Dry Run: Problem 17 — Min Cost to Hire K Workers
```
quality = [3,1,10,10,1], wage = [4,8,2,2,7], k = 3

Workers sorted by ratio (wage/quality):
  (2.0, 10), (2.0, 1), (2.33, 3), (2.67, 1), (7.0, 1)

Step 1: ratio=2.0, q=10 => heap=[-10], total_q=10
Step 2: ratio=2.0, q=1  => heap=[-10,-1], total_q=11
  len(2) < k(3) => no result yet
Step 3: ratio=2.33, q=3 => heap=[-10,-1,-3], total_q=14
  len==k => result = min(inf, 2.33*14) = 32.67
Step 4: ratio=2.67, q=1 => heap=[-10,-1,-3,-1], total_q=15
  len>k => pop -10 => total_q=5, heap=[-3,-1,-1]
  result = min(32.67, 2.67*5) = 13.33
Step 5: ratio=7.0, q=1 => heap=[-3,-1,-1,-1], total_q=6
  len>k => pop -3 => total_q=3, heap=[-1,-1,-1]
  result = min(13.33, 7.0*3) = 13.33

Answer: 13.33
```

### Dry Run: Problem 32 — Generate Parentheses (n=3)
```
backtrack(path="", open=0, close=0)
|-- add '(' => path="(", open=1, close=0
|   |-- add '(' => path="((", open=2, close=0
|   |   |-- add '(' => path="(((", open=3, close=0
|   |   |   |-- add ')' => path="((()", open=3, close=1
|   |   |   |   |-- add ')' => path="((())", open=3, close=2
|   |   |   |   |   |-- add ')' => "((()))" -- SOLUTION 1
|   |   |   |   |-- add '(' => open=3==n => skip
|   |   |   |-- add '(' => open=3==n => skip
|   |   |-- add ')' => path="(()", open=2, close=1
|   |       |-- add ')' => path="(())", open=2, close=2
|   |       |   |-- add ')' => open closed, can't
|   |       |   |-- add '(' => path="(()(", open=3, close=2
|   |       |       |-- add ')' => "(()())" -- SOLUTION 2
|   |       |-- add '(' => path="(()(", open=3, close=1
|   |           |-- add ')' => path="(()()", open=3, close=2
|   |               |-- add ')' => "(())" -- nope...
|   |               (continue until "()(())" found)
|   |-- add ')' => path="()", open=1, close=1
|       |-- add '(' => path="()(", open=2, close=1
|       |   |-- add '(' => path="()((", open=3, close=1
|       |   |   |-- add ')' => "()(())" -- SOLUTION 4
|       |   |-- add ')' => path="()()", open=2, close=2
|       |       |-- add '(' => "()()(" , open=3, close=2
|       |       |   |-- add ')' => "()()()" -- SOLUTION 5
|       |-- add ')' => close>open => skip

Result: ["((()))","(()())","(())()","()(())","()()()"]
Count = C(3) = 5
```

### Dry Run: Problem 29 — N-Queens (n=4)
```
Board 4x4, backtrack row by row:

Row 0: Try col=0
  Place Q at (0,0): cols={0}, pos={0}, neg={0}
  Row 1: Try col=1 => pos_diag=2 in set? No
    Place Q at (1,1): cols={0,1}, pos={0,2}, neg={0,0}
    Row 2: col=0 in cols, col=1 in cols, col=2 pos_diag=4, col=3 pos_diag=5
      All fail => backtrack
  Row 1: Try col=2
    Place Q at (1,2): cols={0,2}, pos={0,3}, neg={0,-1}
    Row 2: Try col=1 => pos_diag=3 in set? Yes => skip
      Try col=3 => pos_diag=5, neg_diag=-1 in set! => skip
      No valid => backtrack
  Row 1: Try col=3
    Place Q at (1,3): cols={0,3}, pos={0,4}, neg={0,-2}
    Row 2: Try col=1
      Place Q at (2,1): cols={0,1,3}, pos={0,1,4}, neg={0,-1,-2}
      Row 3: col=2 => pos_diag=5 not in set, neg_diag=1 not in set
        Place Q at (3,2)! cols={0,1,2,3}
        Row 4: row==n => SOLUTION FOUND!
          . Q . .
          . . . Q
          Q . . .
          . . Q .

(Continue exploring to find solution 2...)
```

---

# ═══════════════════════════════════════════════════════════════
# BACKTRACKING TEMPLATE (REUSABLE PATTERN)
# ═══════════════════════════════════════════════════════════════

```python
def backtrack_template(candidates, target, start, path, result):
    """
    Universal backtracking skeleton.
    Modify: the 'for' range, the validity check, and the recursive call.
    """
    # BASE CASE: when to add path to result
    if is_complete(path):
        result.append(path[:])  # or path.copy()
        return

    # PRUNING: early termination
    if is_impossible(path):
        return

    # CHOICE LOOP: iterate over valid options
    for i in range(start, len(candidates)):
        # PRUNE: skip invalid/duplicate choices
        if should_skip(i, candidates, start):
            continue

        # CHOOSE
        path.append(candidates[i])

        # RECURSE (go deeper)
        backtrack(candidates, target, i + 1, path, result)

        # UNCHOOSE (backtrack)
        path.pop()
```

### Template Adaptations by Problem Type:

| Problem Type | start | Loop Range | Reuse? | Duplicate Skip |
|---|---|---|---|---|
| Subsets | 0 | i+1 to n | No | `i > start` check |
| Permutations | 0 | 0 to n (all) | No | `used[]` array |
| Combinations | 0 | i+1 to n | No | `i > start` check |
| Combination Sum | 0 | i to n (reuse) | Yes | Not needed (unique input) |
| Word Search | each cell | 4 directions | No | In-place `'#'` mark |
| N-Queens | row 0 | 0 to n cols | No | `cols`, `diags` sets |

---

# ═══════════════════════════════════════════════════════════════
# GREEDY PROOF TECHNIQUES
# ═══════════════════════════════════════════════════════════════

### 1. Exchange Argument (Problems 12, 13, 18)
```
To prove greedy is optimal:
1. Assume optimal solution O differs from greedy G
2. Find the first point where they differ
3. Show you can "exchange" O's choice for G's choice
   without making the solution worse
4. This means G is at least as good as O
```

Example (Interval Scheduling -- Problem 12):
- Greedy picks interval with earliest end
- If optimal picks a different first interval, we can swap it
  for the greedy one (ends earlier, leaving more room)
- No intervals are lost, so the swap does not hurt

### 2. Greedy Choice Property (Problems 1, 5, 16)
```
There exists an optimal solution that includes
the greedy choice. Once the greedy choice is made,
the remaining subproblem has the same structure.
```

Example (Assign Cookies -- Problem 5):
- Give the smallest cookie to the least greedy child
- If an optimal solution does not do this, we can swap
  cookies without reducing the count of content children

### 3. Matroid Structure (Problems 12, 13)
```
A problem has optimal greedy solution if it has
matroid structure:
1. Empty set is independent
2. Subsets of independent sets are independent (hereditary)
3. If |A| < |B| for independent sets, there exists
   b in B\A such that A union {b} is independent (exchange)
```

Interval scheduling on a matroid means greedy is optimal.

---

# ═══════════════════════════════════════════════════════════════
# PRUNING TECHNIQUES IN BACKTRACKING
# ═══════════════════════════════════════════════════════════════

### 1. Feasibility Pruning
```
If remaining < 0 or remaining < smallest candidate -> prune
Used in: Combination Sum, Combination Sum II/III
Example: if remaining=3 and next candidate=5, skip all remaining (sorted)
```

### 2. Duplicate Pruning
```
Sort input. At each level, skip same value as previous.
Condition: if i > start and nums[i] == nums[i-1]: skip
Used in: Subsets II, Permutations II, Combination Sum II
```

### 3. Symmetry Breaking
```
When choices produce symmetric results, fix one dimension.
Used in: N-Queens (place row by row, not all cells)
         Sudoku (fill cells left-to-right, top-to-bottom)
```

### 4. Constraint Propagation
```
After making a choice, immediately eliminate impossible
options for other cells.
Used in: Sudoku Solver (eliminate from row/col/box)
         N-Queens (eliminate diagonals)
```

### 5. Ordering Heuristic
```
Try the most constrained option first.
If it fails, fail fast. If it succeeds, likely optimal.
Used in: Crossword Solver (pick shortest/most-filled slot)
         Sudoku (try digit with fewest possibilities)
```

---

# ═══════════════════════════════════════════════════════════════
# COMMON PITFALLS AND DEBUGGING TIPS
# ═══════════════════════════════════════════════════════════════

### Greedy Mistakes:
```
1. Assuming greedy works without proof
   - Always verify: does local optimal lead to global optimal?
   - Counter: Coin change with coins [1, 3, 4] and target 6
     Greedy: 4+1+1 = 3 coins (optimal: 3+3 = 2 coins)

2. Wrong sorting criterion
   - Problem 12/13: Sort by END, not by START or LENGTH
   - Problem 10: Sort by HEIGHT descending, then K ascending
   - Problem 17: Sort by RATIO (wage/quality), not by quality

3. Not handling ties properly
   - Problem 9: Multiple tasks with same max frequency
   - Formula uses count_of_max, not just max_freq

4. Forgetting the "total" check
   - Problem 8: Always check total_gas >= total_cost first
   - Without this, you might return an invalid start index
```

### Backtracking Mistakes:
```
1. Forgetting to undo state (the pop/unplace step)
   - Most common bug in backtracking
   - Every append must have a matching pop
   - Every place() must have a matching unplace()

2. Not sorting when handling duplicates
   - Problems 20, 22, 25 all need sorted input
   - Without sorting, duplicate skipping does not work

3. Wrong "start" index causing duplicates or missing solutions
   - Subsets/Combinations: start = i+1 (no reuse)
   - Combination Sum: start = i (allow reuse)
   - Permutations: no start index, use used[] array

4. Off-by-one in base case
   - Subsets: add path at EVERY node, not just leaves
   - Permutations: add path only when len(path) == len(nums)
   - Combinations: add path when remaining == 0

5. Modifying a shared data structure without copying
   - result.append(path) stores a REFERENCE (will change later!)
   - Always use result.append(path[:]) or path.copy()
```

---

# ═══════════════════════════════════════════════════════════════
# INFOSYS SP DSE INTERVIEW SCENARIOS
# ═══════════════════════════════════════════════════════════════

### Scenario 1: "Tell me about greedy algorithms"
```
Good answer:
"Greedy algorithms make locally optimal choices at each step
with the hope of finding a global optimum. They work when
the problem has greedy choice property and optimal substructure.
I've solved problems like interval scheduling (sort by end),
activity selection, and job scheduling using greedy."

Follow-up: "When does greedy fail?"
"Greedy fails when local optimum does not lead to global optimum.
For example, coin change with non-canonical denominations.
In such cases, we need dynamic programming."
```

### Scenario 2: "Explain backtracking with an example"
```
Good answer:
"Backtracking is a systematic way to explore all possible
solutions by building candidates incrementally and abandoning
a candidate as soon as it determines it cannot lead to a valid
solution. For example, in N-Queens, we place queens row by row.
If placing a queen at (row, col) conflicts with an existing
queen, we prune that entire subtree and try the next column."

Follow-up: "How is it different from brute force?"
"Backtracking prunes the search space. Brute force explores
all n^n possibilities for N-Queens. Backtracking only explores
valid partial solutions, reducing it to roughly O(n!)."
```

### Scenario 3: "Which problems use two-pointer technique?"
```
- Assign Cookies (Problem 5): two sorted arrays, two pointers
- Jump Game: implicit two-pointer (i and farthest)
- Non-overlapping Intervals (Problem 13): one pass with end pointer
- Buy Sell Stock (Problem 2): track min, compute max diff
```

### Scenario 4: "When would you use a heap in greedy?"
```
Two-heap pattern (Problems 14, 16, 17):
- Min-heap to filter/select candidates
- Max-heap to greedily pick the best among candidates
- Useful when you need to dynamically select the best
  from a changing set of options

Examples:
- Meeting Rooms II: min-heap tracks end times of active meetings
- IPO: min-heap for affordable, max-heap for profitable
- Min Cost K Workers: max-heap to keep K smallest qualities
```

### Scenario 5: "Walk me through solving Sudoku with backtracking"
```
1. Find the first empty cell (marked '.')
2. Try digits '1' through '9'
3. For each digit, check if valid (row, column, 3x3 box)
4. If valid, place the digit and recurse on next empty cell
5. If recursion returns True, solution found
6. If no digit works, return False (trigger backtracking)
7. The previous cell will try its next digit
8. When all cells are filled, we have a solution

Key optimization: precompute which cells are empty
and iterate only over them, avoiding repeated scanning.
```

---

# ═══════════════════════════════════════════════════════════════
# RECOMMENDED PRACTICE ORDER
# ═══════════════════════════════════════════════════════════════

### Week 1: Foundation (Easy Greedy + Easy Backtracking)
```
Day 1-2: Problems 2, 3, 6 (one-pass greedy)
Day 3-4: Problems 1, 5 (sort-based greedy)
Day 5: Problem 4 (counting greedy)
Day 6-7: Problems 19, 21, 23 (basic backtracking templates)
```

### Week 2: Intermediate (Medium Greedy + Medium Backtracking)
```
Day 1-2: Problems 7, 8 (advanced one-pass greedy)
Day 3: Problems 12, 13 (interval scheduling family)
Day 4: Problems 9, 11 (frequency-based greedy)
Day 5: Problem 10 (insertion-based greedy)
Day 6: Problem 14 (two-heap greedy)
Day 7: Problems 24, 25, 26 (combination family)
```

### Week 3: Advanced (Hard Greedy + Medium/Hard Backtracking)
```
Day 1-2: Problems 15, 16 (two-pass and two-heap greedy)
Day 3: Problems 17, 18 (exchange argument greedy)
Day 4: Problems 27, 28, 29 (grid and string backtracking)
Day 5: Problems 30, 31, 32 (constraint and string backtracking)
Day 6: Problems 33, 34, 35 (advanced backtracking)
Day 7: Problems 36, 37, 38 (graph and complex backtracking)
```

### Week 4: Mock Interviews
```
Day 1: Pick 3 random greedy problems, solve under 15 min each
Day 2: Pick 3 random backtracking problems, solve under 20 min each
Day 3: Pick 1 hard greedy + 1 hard backtracking, solve under 40 min
Day 4: Practice explaining approach before coding (5 min talk)
Day 5: Full mock: 2 problems in 45 minutes
Day 6: Review all mistakes and weak areas
Day 7: Final revision of templates and patterns
```

---

# ═══════════════════════════════════════════════════════════════
# EXPECTED COMPLEXITIES CHEAT SHEET
# ═══════════════════════════════════════════════════════════════

| Pattern | Typical Time | Typical Space | Example Problems |
|---------|-------------|---------------|------------------|
| Sort + linear scan | O(n log n) | O(1) | 1, 5, 12, 13 |
| Single pass | O(n) | O(1) | 2, 3, 4, 7, 8 |
| Sort + heap | O(n log n) | O(n) | 11, 14, 16, 17, 18 |
| Two-pass | O(n) | O(n) | 15 |
| Formula-based | O(n) | O(1) | 9 |
| Insertion-based | O(n^2) | O(n) | 10 |
| Subset enumeration | O(n * 2^n) | O(n) | 19, 20 |
| Permutation | O(n * n!) | O(n) | 21, 22 |
| Backtrack with pruning | Varies widely | O(depth) | 24-38 |
| Trie + DFS | O(m * n * 3^L) | O(words) | 34 |
| Topological sort | O(V + E) | O(V) | 36 |

---

# ═══════════════════════════════════════════════════════════════
# QUICK REFERENCE: WHEN TO USE WHAT
# ═══════════════════════════════════════════════════════════════

### Use GREEDY when:
- Problem asks for min/max of something
- Sorting reveals a natural order
- You can prove local optimal = global optimal
- Problems involve intervals, scheduling, or ratios
- You see "minimum arrows", "minimum removals", "maximum profit"

### Use BACKTRACKING when:
- Problem asks for ALL solutions (not just count/optimal)
- You need to generate combinations, permutations, subsets
- Grid traversal with word matching
- Constraint satisfaction (N-Queens, Sudoku)
- Problem says "find all", "generate all", "return all valid"

### Use HEAP + GREEDY when:
- You need the Kth largest/smallest dynamically
- You are selecting from a changing set of candidates
- Problems involve "minimum rooms", "most profitable", "best ratio"

### Use TWO-PASS when:
- You need information from both directions
- Left-to-right and right-to-left constraints
- Example: Candy problem (rating > left neighbor AND right neighbor)

---

> **Total: 38 problems | Comprehensive preparation guide | Ready for Infosys SP DSE**
