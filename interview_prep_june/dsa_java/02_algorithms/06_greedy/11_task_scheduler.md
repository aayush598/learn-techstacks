# Task Scheduler (LeetCode 621)

## Problem

Given a character array `tasks` representing tasks a CPU needs to do, and a cooldown interval `n`, each task takes one unit of time. Between two same tasks, there must be at least `n` units of cooldown. Return the **least number of intervals** the CPU will take to finish all tasks.

**Example**:
```
tasks = ['A','A','A','B','B','B'], n = 2
Answer: 8

Execution: [A, B, _, A, B, _, A, B]
            ↑  ↑     ↑  ↑     ↑  ↑
            t1 t2   t3 t4   t5 t6
```

The CPU must idle (represented by `_`) during cooldown periods.

---

## Approach 1: Formula-Based (Math)

### Key Insight

The task with the **maximum frequency** determines the structure of the schedule. Think of it as placing the most frequent task in "slots" with `n` gaps between occurrences, then filling the gaps with other tasks.

### Derivation

Let `maxFreq` = frequency of the most frequent task, and `k` = number of tasks that share `maxFreq`.

1. **Frame**: Place `maxFreq` occurrences of the most frequent task with `n` gaps:
   ```
   A _ _ A _ _ A
     ↑     ↑
     gap   gap
   ```
   Total slots = `(maxFreq - 1) * (n + 1) + k`
   The `+ k` accounts for the last row where all max-frequency tasks run in parallel.

2. **Idle time**: If total slots > number of tasks, fill extras with idles:
   ```
   idle = (maxFreq - 1) * (n + 1) + k - totalTasks
   ```

3. **Result**: `max(totalTasks, (maxFreq - 1) * (n + 1) + k)`

If there are enough different tasks to fill all cooldown gaps, no idles needed — result is just `totalTasks`.

---

## Approach 2: Max Heap (Simulation)

### Idea

Always run the task with the **highest remaining count** (that isn't in cooldown). Use a max-heap for task selection and a queue to track tasks in cooldown.

### Algorithm

1. Count task frequencies, push all into a max-heap.
2. While heap is not empty:
   - Pop up to `n+1` tasks (run one of each in a "round").
   - For each task run, decrement count; if count > 0, add to a waiting queue.
   - After `n+1` slots, tasks in the waiting queue re-enter the heap.
3. The total rounds give the answer.

---

## Complete Java Implementations

### Formula Approach

```java
import java.util.*;

public class TaskSchedulerFormula {

    public int leastInterval(char[] tasks, int n) {
        int[] freq = new int[26];
        for (char c : tasks) freq[c - 'A']++;

        int maxFreq = 0;
        int maxCount = 0;
        for (int f : freq) {
            if (f > maxFreq) {
                maxFreq = f;
                maxCount = 1;
            } else if (f == maxFreq) {
                maxCount++;
            }
        }

        // Formula: (maxFreq - 1) * (n + 1) + maxCount
        int frameSize = (maxFreq - 1) * (n + 1) + maxCount;
        return Math.max(tasks.length, frameSize);
    }
}
```

### Max Heap Approach

```java
import java.util.*;

public class TaskSchedulerHeap {

    public int leastInterval(char[] tasks, int n) {
        int[] freq = new int[26];
        for (char c : tasks) freq[c - 'A']++;

        // Max-heap (use negative for Java's PriorityQueue)
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        for (int f : freq) {
            if (f > 0) maxHeap.offer(f);
        }

        int time = 0;

        while (!maxHeap.isEmpty()) {
            List<Integer> temp = new ArrayList<>();

            // One round: process up to n+1 tasks
            for (int i = 0; i <= n; i++) {
                if (!maxHeap.isEmpty()) {
                    int count = maxHeap.poll() - 1;
                    if (count > 0) temp.add(count);
                }
            }

            // Re-insert processed tasks back into heap
            for (int count : temp) {
                maxHeap.offer(count);
            }

            // Time taken for this round
            if (maxHeap.isEmpty()) {
                // Last round: only count actual tasks, not trailing idles
                time += temp.size();
            } else {
                // Full round including cooldown slots
                time += (n + 1);
            }
        }

        return time;
    }
}
```

---

## Step-by-Step Walkthrough (Formula)

```
tasks = ['A','A','A','B','B','B','C','C'], n = 2

Frequencies: A=3, B=3, C=2
maxFreq = 3, maxCount = 2 (A and B both have freq 3)

Frame:
  Row 1: A  B  _       (3 tasks with max freq, 1 idle)
  Row 2: A  B  _
  Row 3: A  B           (last row: no trailing idles needed)

Frame size = (3-1) * (2+1) + 2 = 6 + 2 = 8
Total tasks = 8

Result = max(8, 8) = 8
Schedule: [A, B, C, A, B, C, A, B]
```

---

## Step-by-Step Walkthrough (Heap)

```
tasks = ['A','A','A','B','B'], n = 2
Heap: [3, 2]

Round 1 (time 0-2):
  Pop A(3), B(2) → run A, B
  A→2, B→1 → push back: [2, 1]
  time += 3 → time = 3

Round 2 (time 3-5):
  Pop A(2), B(1) → run A, B
  A→1, B→0 → push back: [1]
  time += 3 → time = 6

Round 3 (time 6-7):
  Pop A(1) → run A
  A→0 → temp = [] (empty)
  Heap now empty
  time += 1 → time = 7

Result: 7
Schedule: [A, B, _, A, B, _, A]
```

---

## Why the Formula Works

```
Most frequent task: A (freq = 3), n = 2

Imagine a grid with n+1 columns per row:

  Col 0   Col 1   Col 2
  ┌─────┬─────┬─────┐
  │  A  │  B  │     │  ← row 0
  ├─────┼─────┼─────┤
  │  A  │  B  │     │  ← row 1
  ├─────┼─────┼─────┤
  │  A  │  B  │     │  ← row 2 (partial)
  └─────┴─────┴─────┘

Each row = one cooldown cycle (n+1 time units)
(maxFreq - 1) full rows + partial last row

The last row has `maxCount` tasks (all tasks with maxFreq).
```

---

## Edge Cases

| Case | Input | Output | Notes |
|------|-------|--------|-------|
| `n = 0` | `['A','A']` | 2 | No cooldown, just run all |
| All same | `['A','A','A']`, n=2 | 7 | `[A,_,_,A,_,_,A]` |
| All different | `['A','B','C']`, n=2 | 3 | No idle needed, each task unique |
| maxFreq > n | `['A','A','A','B']`, n=1 | `max(4, (3-1)*2+1)` = 5 | `[A,B,A,_,A]` |
| maxFreq ≤ n | `['A','B']`, n=5 | 2 | Fewer tasks than slots |
| Many ties | `['A','A','B','B','C','C']`, n=1 | 6 | All freq=2, all fit |
| Single task | `['A']`, n=5 | 1 | Only one task, no cooldown needed |

---

## Variants

### Variant 1: Different Cooldown Per Task

If each task type has its own cooldown `n_i`, the formula breaks down. You need a **simulation with per-task cooldown tracking** (map of task → next available time).

### Variant 2: Return the Actual Schedule

Instead of just the count, return the actual task sequence. Use the heap approach — each time you pick a task, append it to the result list.

### Variant 3: K CPUs (Parallel Scheduling)

With `k` CPUs, `k` tasks can run simultaneously each time slot. The formula generalizes:
```
frames = ceil(totalTasks / k)
idle per frame = max(0, (maxFreq - 1) * (n+1) + maxCount - k)
```

---

## Complexity

| Approach | Time | Space |
|----------|------|-------|
| Formula | O(n) — single pass through tasks | O(1) — fixed 26-char array |
| Heap | O(n log 26) ≈ O(n) — heap ops on at most 26 elements | O(1) |

---

## Common Pitfalls

1. **Not handling `maxCount > 1`**: Multiple tasks with the same max frequency all go in the last row. Missing this gives wrong answers for ties.

2. **Using the heap approach and adding trailing idles**: The last round doesn't need full `n+1` slots — just count the actual tasks processed.

3. **Forgetting `n = 0`**: Formula still works: `(maxFreq-1)*1 + maxCount = maxFreq - 1 + maxCount`. But be careful with the heap — if `n = 0`, every task runs immediately.
