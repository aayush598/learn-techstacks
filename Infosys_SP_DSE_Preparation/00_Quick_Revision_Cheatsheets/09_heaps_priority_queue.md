# Heaps & Priority Queues — Last-Minute Revision

Copy-paste ready, tested Python 3 templates using the `heapq` module.

## heapq — Complete Module Reference

Python only ships a MIN-HEAP. `heapq` works on plain lists; index 0 is always the smallest.

> All snippets below assume `import heapq` (shown in the first block above).

```python
import heapq

# Core API
heap = []                     # start with an empty list (or heapify an existing list)
heapq.heappush(heap, item)    # push              O(log n)
smallest = heapq.heappop(heap)   # pop smallest   O(log n)
heapq.heapify(lst)            # turn any list into a heap in place, O(n)
top = heap[0]                 # peek (don't pop)  O(1)
replaced = heapq.heapreplace(heap, item)   # pop smallest then push new; O(log n)
pushed = heapq.heappushpop(heap, item)     # push then pop smallest; O(log n)

# Bulk queries (do NOT rely on heap order, but still O(n log k) for k top items)
three_largest = heapq.nlargest(3, [5,1,9,3,7])    # [9,7,5]
three_smallest = heapq.nsmallest(3, [5,1,9,3,7])  # [1,3,5]

# Insort-style helpers exist in heapq only for lists that are already heapified:
heapq.heappush(heap, 10)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)
heapq.heapify([])  # safe no-op on empty list
```

| Function | Behavior | Time |
|---|---|---|
| `heappush(h, x)` | push item | O(log n) |
| `heappop(h)` | pop smallest | O(log n) |
| `heapify(a)` | in-place min-heap build | O(n) |
| `heapreplace(h, x)` | pop smallest, push x | O(log n) |
| `heappushpop(h, x)` | push x, pop smallest | O(log n) |
| `nlargest / nsmallest(k, iter)` | top-k items | O(n log k) |

## Min-Heap (default) and Max-Heap (by negation)

```python
import heapq
min_heap = [3, 1, 2]
heapq.heapify(min_heap)
assert min_heap[0] == 1

max_heap = []                # Python has no max-heap -> store NEGATED values
for x in [3, 1, 2]:
    heapq.heappush(max_heap, -x)   # negate on push
largest = -heapq.heappop(max_heap)  # negate on pop
assert largest == 3
```

| Type | Push | Pop | Peek |
|---|---|---|---|
| min-heap | `heappush(h, x)` | `heappop(h)` | `h[0]` |
| max-heap | `heappush(h, -x)` | `-heappop(h)` | `-h[0]` |

## Heap of Tuples — (priority, value)

When you push tuples, heapq compares element-by-element. So keep the sortable key FIRST.

```python
import heapq
h = []
heapq.heappush(h, (2, "low"))
heapq.heappush(h, (1, "high"))
heapq.heappush(h, (3, "mid"))
while h:
    priority, value = heapq.heappop(h)
    print(value, priority)      # high 1, low 2, mid 3
```

**Sorting with a custom comparator via tuple wrapping** (for reverse-priority, negate the key):

```python
def push_with_custom_order(h, key, tiebreaker, value):
    heapq.heappush(h, (key, tiebreaker, value))
# pushes are ordered by key, then tiebreaker, then value — all ascending.
# Want descending key? push -key. Want alphabetical tiebreak? push the string directly.
```

**NEVER push a bare `ListNode` or a custom object** into a heap — heapq needs `<` to work. If you must, wrap it: `(node.val, index, node)` as done in merge-k-sorted-lists below.

## K Largest / K Smallest Elements

```python
def k_largest(nums, k):                     # O(n log k) time, O(k) space
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:                   # keep only the k biggest by evicting smallest
            heapq.heappop(heap)
    return heap                             # unsorted heap of the k largest

def k_smallest(nums, k):                    # same trick, max-heap via negation
    heap = []
    for x in nums:
        heapq.heappush(heap, -x)
        if len(heap) > k:
            heapq.heappop(heap)
    return [-x for x in heap]

# k_largest([3,2,1,5,6,4], 3) -> [5,6,4] (any order) | k_smallest([3,2,1,5,6,4], 2) -> [1,2]
```

| Template | Time | Space |
|---|---|---|
| k largest / smallest (heap of size k) | O(n log k) | O(k) |

## K Most Frequent Elements (Counter + heap)

```python
from collections import Counter

def top_k_frequent(nums, k):
    freq = Counter(nums)                     # element -> count
    heap = []
    for num, count in freq.items():
        heapq.heappush(heap, (count, num))   # heap sorted by count ascending
        if len(heap) > k:                    # evict least frequent
            heapq.heappop(heap)
    return [num for _, num in heap]

# top_k_frequent([1,1,1,2,2,3], 2) -> [2,1] (either order, both have top-2 counts)
```

| Template | Time | Space |
|---|---|---|
| top k frequent | O(n log k) | O(n) |

## Merge K Sorted Lists / K Sorted Arrays

```python
def merge_k_sorted_lists(lists):             # lists = list of sorted lists
    heap = []
    for i, lst in enumerate(lists):
        if lst:                              # (val, list_index, element_index)
            heapq.heappush(heap, (lst[0], i, 0))
    res = []
    while heap:
        val, i, j = heapq.heappop(heap)
        res.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return res

# merge_k_sorted_lists([[1,4,5],[1,3,4],[2,6]]) -> [1,1,2,3,4,4,5,6]
```

| Template | Time | Space |
|---|---|---|
| merge k sorted | O(n log k) | O(k) |

## Median in a Stream — Two Heaps (full template)

`small` = max-heap of the LOWER half (negated). `large` = min-heap of the UPPER half.
Invariant: `len(small)` equals `len(large)` or is one more. Median is `-small[0]` (odd) or `(-small[0] + large[0]) / 2` (even).

```python
class MedianFinder:
    def __init__(self):
        self.small = []      # max-heap (negated) — lower half
        self.large = []      # min-heap           — upper half

    def add_num(self, num):
        heapq.heappush(self.small, -num)             # put in lower half first
        if self.small and self.large and (-self.small[0] > self.large[0]):
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.small) > len(self.large) + 1:    # rebalance sizes
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0

# mf = MedianFinder(); for x in [5,15,1,3]:
#   add_num(x) → medians: 5.0, 10.0, 5.0, 4.0
```

| Operation | Time | Space |
|---|---|---|
| add_num | O(log n) | O(n) |
| find_median | O(1) | O(n) |

## Top K Frequent Words (tie-break alphabetical using tuple trick)

Tuple `(-count, word)` sorts by frequency first, then alphabetically. Use heapify + pop-k (the size-k push/pop eviction BREAKS when counts tie: popping the smallest tuple would evict a high-frequency word).

```python
from collections import Counter

def top_k_frequent_words(words, k):
    freq = Counter(words)
    heap = [(-count, word) for word, count in freq.items()]  # -count: most frequent first; word: alphabetical
    heapq.heapify(heap)
    return [heapq.heappop(heap)[1] for _ in range(min(k, len(heap)))]

# top_k_frequent_words(["i","love","leetcode","i","love","coding"], 2)
#   -> ["i","love"]
# top_k_frequent_words(["the","day","is","sunny","the","the","the","sunny","is","is"], 4)
#   -> ["the","is","sunny","day"]
```

Exam trap: for the size-k streaming variant you would need `(count, tuple(-ord(c) for c in word))` so the min-heap evicts the alphabetically LARGEST word first. Use the heapify+pop-k version above instead — it is correct and O(n).

| Template | Time | Space |
|---|---|---|
| top k frequent words | O(n + k log n) | O(n) |

## Meeting Rooms / Interval Scheduling Pattern

**Minimum meeting rooms** = number of meetings that overlap at the busiest instant. Sort by start; a min-heap of end times tells you the earliest ending meeting.

```python
def min_meeting_rooms(intervals):              # intervals = [[start, end], ...]
    intervals.sort(key=lambda x: x[0])
    heap = []                                  # holds end times of ongoing meetings
    for start, end in intervals:
        if heap and heap[0] <= start:          # earliest-ending meeting already over
            heapq.heappop(heap)
        heapq.heappush(heap, end)              # this meeting now occupies a room
    return len(heap)

# min_meeting_rooms([[0,30],[5,10],[15,20]]) -> 2
# min_meeting_rooms([[7,10],[2,4]])          -> 1
```

**Merge intervals** (sort + greedy, no heap needed but same exam family):

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    res = []
    for start, end in intervals:
        if res and start <= res[-1][1]:
            res[-1][1] = max(res[-1][1], end)
        else:
            res.append([start, end])
    return res

# merge_intervals([[1,3],[2,6],[8,10],[15,18]]) -> [[1,6],[8,10],[15,18]]
```

| Template | Time | Space |
|---|---|---|
| min meeting rooms | O(n log n) | O(n) |
| merge intervals | O(n log n) | O(n) |

## Task Scheduler

With `n` cooldown between two same tasks: (max_freq - 1) full cycles of (n+1) slots, plus the number of tasks tied for max frequency. Take the max with the bare task count.

```python
from collections import Counter

def least_interval(tasks, n):                  # tasks = list of task letters
    counts = Counter(tasks).values()
    max_freq = max(counts)
    num_max = list(counts).count(max_freq)     # how many tasks share the max frequency
    cycles = (max_freq - 1) * (n + 1) + num_max
    return max(cycles, len(tasks))

# least_interval(["A","A","A","B","B","B"], 2) -> 8
# least_interval(["A","A","A"], 2)             -> 7
```

| Template | Time | Space |
|---|---|---|
| task scheduler (greedy math) | O(n) | O(1) |

## Quick Reference Table

| Template | Key idea | Time | Space |
|---|---|---|---|
| min-heap / max-heap | negate for max | O(log n) per op | O(n) |
| tuple heap | key first, then tiebreakers | O(log n) per op | O(n) |
| k largest / smallest | keep heap at size k | O(n log k) | O(k) |
| top k frequent | Counter + heap of size k | O(n log k) | O(n) |
| merge k sorted | push head of each list | O(n log k) | O(k) |
| median in stream | small (negated) + large | O(log n) add | O(n) |
| top k frequent words | (-count, word) tuple | O(n + k log n) | O(n) |
| meeting rooms | sort starts + min-heap ends | O(n log n) | O(n) |
| task scheduler | (max_freq-1)*(n+1)+num_max | O(n) | O(1) |

Memory hooks:
- **Python heap = min-heap; max-heap = negate on push and negate on pop.**
- **Tuple heaps: put the thing you sort by FIRST.** Never push a custom object bare.
- **The "keep heap size = k" trick** (push then pop when `len > k`) is the universal top-k.
- **Two-heap median:** keep lower half one element bigger; peek answers in O(1).
