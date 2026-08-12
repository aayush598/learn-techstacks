# Priority 5 — Coding Exercises (Q685–Q720)

**Why these matter for micro1:** the interview includes a coding exercise (up to 48 min total). These are the classic patterns — strings, arrays, hashing, linked lists, trees, concurrency, schedulers. For each: **narrate approach → complexity → edge cases → code → test mentally**.

**Golden rules for live coding (Q421, and the "Golden rules" in README):**
1. Clarify constraints (input size, empty/None inputs, duplicates, unicode).
2. Say the approach + time/space complexity *before* coding.
3. Write clean, simple code — no cleverness.
4. Test with a small example by hand, then edge cases.

---

## Q685: Reverse a string (in place / without slicing shortcut).

**Approach:** two pointers swap from both ends toward the middle — O(n) time, O(1) space.

```python
def reverse(s: list[str]) -> None:      # list = mutable char array (Python str is immutable)
    i, j = 0, len(s) - 1
    while i < j:
        s[i], s[j] = s[j], s[i]
        i += 1; j -= 1
```

**Edge cases:** empty, single char, even/odd length. **Note the Python detail:** strings are immutable — use `s[::-1]` (O(n)) or a list; the two-pointer version is the interview answer.

---

## Q686: Check if a string is a palindrome.

**Approach:** two pointers comparing from both ends; skip non-alphanumerics and case-fold if asked ("valid palindrome", ignoring punctuation).

```python
def is_palindrome(s: str) -> bool:
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum(): i += 1
        while i < j and not s[j].isalnum(): j -= 1
        if s[i].lower() != s[j].lower(): return False
        i += 1; j -= 1
    return True
```

**Complexity:** O(n) time, O(1) space. **Edge cases:** `""`, `" "`, `"a"`, `"A man, a plan..."`, all-punctuation input.

---

## Q687: Find the first non-repeating character in a string.

**Approach:** count frequencies in one pass (dict), then scan again for the first char with count 1. O(n) time, O(1) space (alphabet-bounded, or O(k) with a dict).

```python
from collections import Counter
def first_non_repeat(s: str) -> int:
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1: return i
    return -1
```

**Edge cases:** empty, all-same, all-repeat, one char.

---

## Q688: Two Sum — return indices of two numbers that add to a target.

**Approach:** hash map value → index; for each element check if `target - n` is in the map. O(n) time, O(n) space.

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []
```

**Edge cases:** no solution, duplicates (e.g., `[3,3]`, `target=6` — the map stores the *first* index, so fine), negative numbers. **Follow-ups:** sorted array → two-pointer O(1) space; "all pairs" → sort + two pointers (Q693).

---

## Q689: Best time to buy and sell stock (one transaction).

**Approach:** track the min price seen so far and the max profit. O(n) time, O(1) space.

```python
def max_profit(prices: list[int]) -> int:
    best, low = 0, float("inf")
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

**Edge cases:** empty, one day, decreasing prices (profit 0), all equal. **Follow-up (multiple transactions):** greedy sum of positive deltas: `sum(max(0, p[i]-p[i-1])`.

---

## Q690: Valid parentheses (balanced brackets).

**Approach:** stack; push openers, pop-and-match on closers. O(n) time, O(n) space.

```python
def is_valid(s: str) -> bool:
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]: return False
        else:
            stack.append(ch)
    return not stack
```

**Edge cases:** empty, `"(]"`, `"([)]"`, `")("`, unclosed `"((("`. **Follow-ups:** count-only version (O(1) space for one bracket type), longest-valid-substring (stack with indices).

---

## Q691: Implement a function to check if two strings are anagrams.

**Approach:** counter compare — O(n) time, O(1) space (fixed alphabet); or sort both O(n log n).

```python
from collections import Counter
def is_anagram(a: str, b: str) -> bool:
    return Counter(a) == Counter(b)
```

**Edge cases:** different lengths (quick exit), empty, unicode/case sensitivity (ask!), "aab" vs "abb". **Follow-ups:** group anagrams (map sorted-string → list), find all anagram substrings in a window (sliding window with counter).

---

## Q692: Merge two sorted arrays in place (nums1 has trailing zeros).

**Approach:** three pointers from the **end** (fill backwards) — O(m+n) time, O(1) space.

```python
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]; i -= 1
        else:
            nums1[k] = nums2[j]; j -= 1
        k -= 1
```

**Edge cases:** empty nums2, empty nums1, duplicates. **The trick to mention:** filling from the back avoids overwriting unread nums1 elements.

---

## Q693: Find all pairs in a sorted array that sum to a target.

**Approach:** two pointers (sorted input) — O(n) time, O(1) space.

```python
def pair_sum(a: list[int], target: int) -> list[tuple[int, int]]:
    res, i, j = [], 0, len(a) - 1
    while i < j:
        s = a[i] + a[j]
        if s == target:
            res.append((a[i], a[j])); i += 1; j -= 1
        elif s < target: i += 1
        else: j -= 1
    return res
```

**Edge cases:** duplicates (dedupe with a set of seen pairs or skip-equal-while-loop), no pairs, target smaller than min sum. **Follow-up:** unsorted input → sort (O(n log n)) or hash set (O(n)).

---

## Q694: Find the maximum subarray sum (Kadane's).

**Approach:** Kadane — running sum, reset to 0 if it goes negative; track max. O(n) time, O(1) space.

```python
def max_subarray(nums: list[int]) -> int:
    best, cur = float("-inf"), 0
    for n in nums:
        cur = max(n, cur + n)
        best = max(best, cur)
    return best
```

**Edge cases:** all negative (answer = max element), single element, zeros. **Follow-ups:** return the subarray itself (track start/end), circular variant, 2D variant (Kadane per row-pair).

---

## Q695: Contains Duplicate — detect duplicates in an array.

**Approach:** set as you scan — O(n) time, O(n) space. Sorted variant O(n log n)/O(1).

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen = set()
    for n in nums:
        if n in seen: return True
        seen.add(n)
    return False
```

**Follow-ups:** **sliding window "contains duplicate II"** — value within k distance: dict value→index, check `i - idx <= k`. Duplicates in a *sorted window* — use a **sorted structure** (heap/TreeMap) since the window has many values.

---

## Q696: Move zeroes to the end preserving order.

**Approach:** one pointer for the write position, one for scanning; swap non-zeroes forward. O(n) time, O(1) space.

```python
def move_zeroes(nums: list[int]) -> None:
    w = 0
    for r in range(len(nums)):
        if nums[r] != 0:
            nums[w], nums[r] = nums[r], nums[w]
            w += 1
```

**Edge cases:** all zeroes, no zeroes, leading/trailing zeroes. **Follow-ups:** stable partition by arbitrary predicate; two-pivot variants (zeros + ones, Dutch flag, Q698).

---

## Q697: Product of array except self (no division).

**Approach:** left-pass builds prefix products, right-pass multiplies suffix — O(n) time, O(1) extra space (output array aside).

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n
    pref = 1
    for i in range(n):
        res[i] = pref; pref *= nums[i]
    suff = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suff; suff *= nums[i]
    return res
```

**Edge cases:** zeros (works naturally), single element, negatives. **Why no division:** division is undefined at zero — the interviewer wants the two-pass technique, not `total//x`.

---

## Q698: Sort colors (Dutch national flag) — [0,1,2] in one pass.

**Approach:** three pointers — `low`/`mid` scan, `high` boundary for 2s. O(n) time, O(1) space.

```python
def sort_colors(nums: list[int]) -> None:
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1
```

**Edge cases:** all one color, empty. **This is the canonical "partition into 3 regions in one pass" problem** — the technique appears in many follow-ups.

---

## Q699: Merge intervals (e.g., [1,3],[2,6] → [1,6]).

**Approach:** sort by start, merge when `cur.end >= next.start`. O(n log n) time (sort dominates), O(n) space worst case.

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort()
    out = [intervals[0]]
    for s, e in intervals[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

**Edge cases:** touching intervals `[1,2],[2,3]` (overlap by problem definition — clarify!), nested intervals `[1,10],[2,3]`, single interval. **Follow-ups:** insert interval, min meeting rooms (heap, Q712), employee free time.

---

## Q700: Maximum product subarray.

**Approach:** track max-so-far AND min-so-far (a negative × negative flips sign). O(n) time, O(1) space.

```python
def max_product(nums: list[int]) -> int:
    best = cur_max = cur_min = nums[0]
    for n in nums[1:]:
        if n < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(n, cur_max * n)
        cur_min = min(n, cur_min * n)
        best = max(best, cur_max)
    return best
```

**Edge cases:** zeros (reset window), negative numbers, single element, `[-1, -2]` (→ 2). **Why min matters:** `[-2, 3, -4]` — the running max alone misses the double-negative.

---

## Q701: Implement a stack with push, pop, min in O(1).

**Approach:** a parallel "min stack" — push the running min alongside each value. O(1) for all ops.

```python
class MinStack:
    def __init__(self):
        self.data: list[int] = []
        self.mins: list[int] = []
    def push(self, x: int) -> None:
        self.data.append(x)
        self.mins.append(x if not self.mins else min(x, self.mins[-1]))
    def pop(self) -> int:
        self.mins.pop()
        return self.data.pop()
    def top(self) -> int: return self.data[-1]
    def get_min(self) -> int: return self.mins[-1]
```

**Edge cases:** pop below min, duplicate mins (`[2,2]` → pop keeps min). **Follow-up:** queue with O(1) min (two stacks or monotonic deque, Q711).

---

## Q702: Implement a queue using two stacks.

**Approach:** `inbox` for pushes; on pop, if `outbox` empty, drain `inbox` into it (reverses order). Amortized O(1) per op.

```python
class MyQueue:
    def __init__(self):
        self.ins, self.outs = [], []
    def push(self, x): self.ins.append(x)
    def pop(self):
        self._move()
        return self.outs.pop()
    def peek(self):
        self._move()
        return self.outs[-1]
    def _move(self):
        if not self.outs:
            while self.ins:
                self.outs.append(self.ins.pop())
```

**Complexity reasoning to state:** each element moves at most twice (in→out), so amortized O(1); worst-case single pop O(n). **Follow-ups:** stack using two queues (push costlier); min-queue.

---

## Q703: Implement a LRU cache (get/put in O(1)).

**Approach:** hash map (key → node) + **doubly linked list** for recency order — get moves to head; put evicts tail when full. O(1) both ops.

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, Node] = {}
        self.head, self.tail = Node(), Node()   # sentinels
        self.head.next = self.tail; self.tail.prev = self.head
    def get(self, key: int) -> int:
        if key not in self.map: return -1
        n = self.map[key]; self._move_to_head(n)
        return n.value
    def put(self, key: int, value: int) -> None:
        if key in self.map:
            n = self.map[key]; n.value = value; self._move_to_head(n); return
        if len(self.map) >= self.cap:
            old = self.tail.prev; self._remove(old); del self.map[old.key]
        n = Node(key, value)
        self.map[key] = n; self._add_to_head(n)
```

**Why linked list + map:** a deque alone can't do O(1) "move to front" (no O(1) middle access) and can't update recency on *get*. **Real-world tie-in:** this is *exactly* a response/RAG cache (Q432) — and `functools.lru_cache` is the Python built-in.

---

## Q704: Reverse a linked list (iterative and recursive).

**Iterative (O(n) time, O(1) space):**
```python
def reverse_list(head: ListNode | None) -> ListNode | None:
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev, head = head, nxt
    return prev
```

**Recursive:** reverse `head.next`, then point that tail back at head (`head.next.next = head; head.next = None`).

**Edge cases:** empty, single node, two nodes. **Follow-ups:** reverse k-group, reverse a sublist (m..n), palindrome linked list (reverse half), detect cycle (Q706).

---

## Q705: Detect a cycle in a linked list (Floyd's).

**Approach:** slow + fast pointers; they collide if a cycle exists. O(n) time, O(1) space. To *find the start*: after collision, reset one pointer to head, advance both one step — they meet at the cycle start.

```python
def has_cycle(head: ListNode | None) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast: return True
    return False
```

**Edge cases:** empty, single node self-loop, tail→head (full cycle), tail→middle. **Interview note:** the hash-set version is O(n) space and acceptable to mention first, but Floyd's is the expected answer.

---

## Q706: Merge two sorted linked lists.

**Approach:** two pointers + a dummy head (avoids the empty-head special case). O(n+m) time, O(1) space.

```python
def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    dummy = cur = ListNode()
    while a and b:
        if a.val <= b.val:
            cur.next, a = a, a.next
        else:
            cur.next, b = b, b.next
        cur = cur.next
    cur.next = a or b
    return dummy.next
```

**Edge cases:** one empty, both empty, duplicates, all-of-a-then-all-of-b. **Follow-ups:** merge k sorted lists — heap of heads, O(n log k) (Q712).

---

## Q707: Find the middle of a linked list (one pass).

**Approach:** slow/fast — fast moves 2, slow moves 1; when fast ends, slow is the middle. O(n) time, O(1) space.

```python
def middle_node(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

**Edge cases:** empty, single node, even length (returns the *second* middle — state this, it matters for palindrome reversal, Q704). **Uses:** palindrome check, split into halves.

---

## Q708: Find the nth node from the end of a linked list.

**Approach:** two pointers separated by n — advance first n, then walk both until the first ends. O(n) time, O(1) space.

```python
def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    dummy = ListNode(next=head)
    first = second = dummy
    for _ in range(n): first = first.next
    while first.next:
        first, second = first.next, second.next
    second.next = second.next.next
    return dummy.next
```

**Edge cases:** n = length (remove head — dummy handles it), n = 1 (tail), n > length (invalid → error by contract).

---

## Q709: Maximum depth of a binary tree.

**Approach:** recursive DFS — `1 + max(depth(l), depth(r))`; or iterative BFS counting levels. O(n) time, O(height) space (stack) / O(width) (queue).

```python
def max_depth(root: TreeNode | None) -> int:
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

**Edge cases:** empty tree (0), single node (1), skewed tree (depth = n — recursion depth becomes n, mind the limit). **Follow-ups:** balanced-tree check (height per node, early-exit -1), diameter.

---

## Q710: Check if a binary tree is a valid BST.

**Approach:** in-order traversal must be strictly increasing — pass down a valid range, or track prev during in-order. O(n) time, O(height) space.

```python
def is_valid_bst(root: TreeNode | None,
                lo=float("-inf"), hi=float("inf")) -> bool:
    if not root: return True
    if not (lo < root.val < hi): return False
    return (is_valid_bst(root.left, lo, root.val)
            and is_valid_bst(root.right, root.val, hi))
```

**Common trap to mention:** checking only `left < node < right` is wrong — you must enforce the *ancestor* bound (pass range). **Edge cases:** equal values (invalid unless stated), very large values (float bounds), single node.

---

## Q711: Implement a queue with O(1) min (monotonic deque).

**Approach:** a FIFO queue (collections.deque) + a **monotonic deque** storing candidate minimums in increasing order; on push, pop values ≥ new (they'll never be the min), on pop, if the popped value equals the deque front, pop front. All ops amortized O(1).

```python
from collections import deque

class MinQueue:
    def __init__(self):
        self.q: deque[int] = deque()
        self.mins: deque[int] = deque()
    def push(self, x: int) -> None:
        self.q.append(x)
        while self.mins and self.mins[-1] > x:   # keep increasing
            self.mins.pop()
        self.mins.append(x)
    def pop(self) -> int:
        v = self.q.popleft()
        if self.mins[0] == v: self.mins.popleft()
        return v
    def get_min(self) -> int: return self.mins[0]
```

**Why monotonic:** any element popped from `mins` is older than a smaller-or-equal later element, so it can never be the window min. This is also the sliding-window-maximum engine (Q716).

---

## Q712: Merge k sorted lists (min-heap).

**Approach:** push each list's head into a heap by value; pop-min, append, push its `next`. O(n log k) time, O(k) space.

```python
import heapq

def merge_k(lists: list[list[int]]) -> list[int]:
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    out = []
    while heap:
        v, li, idx = heapq.heappop(heap)
        out.append(v)
        if idx + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][idx + 1], li, idx + 1))
    return out
```

**Edge cases:** empty lists, k=1, all-but-one empty, duplicates. **Alternative:** divide-and-conquer pairwise merge (O(n log k) too, no heap). **Real-world:** this pattern = merging streams of ranked candidates from multiple sources.

---

## Q713: Find the k-th largest element in an array.

**Approach (mention all three):**
1. Sort → `arr[-k]` — O(n log n), trivial.
2. **Min-heap of size k** — O(n log k), works streaming.
3. **Quickselect** — O(n) average (O(n²) worst), O(1) space. Expected answer.

```python
def find_kth_largest(nums: list[int], k: int) -> int:
    k = len(nums) - k            # k-th smallest index for quickselect
    def qs(lo: int, hi: int) -> int:
        pivot, i = nums[hi], lo
        for j in range(lo, hi):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]; i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == k: return nums[i]
        return qs(lo, i - 1) if i > k else qs(i + 1, hi)
    return qs(0, len(nums) - 1)
```

**Edge cases:** k=1 (max), k=n (min), duplicates. **Why this pattern matters:** it's the same "partition" idea as Q698 (Dutch flag) — partitioning is a top interview skill.

---

## Q714: Top K frequent elements.

**Approach:** Counter (O(n)) then a **min-heap of size k** keyed by frequency (O(n log k)), or **bucket sort** by frequency (O(n)). Bucket sort is the O(n) expected answer.

```python
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    freq = Counter(nums)
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for val, count in freq.items():
        buckets[count].append(val)
    out = []
    for count in range(len(buckets) - 1, 0, -1):
        for val in buckets[count]:
            out.append(val)
            if len(out) == k: return out
    return out
```

**Edge cases:** all-same-frequency, k = n, negative numbers. **Follow-up (sorted by frequency):** same buckets, emit in order.

---

## Q715: Find all anagram substrings (sliding window with fixed alphabet).

**Problem:** in string `s`, find all start indices of anagrams of pattern `p`. **Approach:** fixed window of len(p); maintain a **Counter** diff — slide and update the diff for the char leaving/entering; when the diff is zero, it's an anagram. O(n) time, O(alphabet) space.

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    need = Counter(p)
    have = Counter()
    out = []
    for i, ch in enumerate(s):
        have[ch] += 1
        if i >= len(p):
            c = s[i - len(p)]
            have[c] -= 1
            if have[c] == 0: del have[c]
        if have == need: out.append(i - len(p) + 1)
    return out
```

**Edge cases:** len(p) > len(s), p == s, all-same letters (`"aaaa"`, `"aa"`). **This is the canonical "sliding window + counter" problem** — the technique powers many string questions.

---

## Q716: Sliding window maximum (monotonic deque).

**Approach:** a deque storing *indices* with decreasing values; window front = max. Each index added/removed once → O(n) time, O(k) space.

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()   # indices, values decreasing
    out = []
    for i, n in enumerate(nums):
        while dq and nums[dq[-1]] <= n: dq.pop()
        dq.append(i)
        if dq[0] <= i - k: dq.popleft()      # out of window
        if i >= k - 1: out.append(nums[dq[0]])
    return out
```

**Edge cases:** k=1, k=n, all-increasing (deque stays size 1), empty. **Real-world:** streaming windows over scores/time-series — same structure as MinQueue (Q711) mirrored.

---

## Q717: Implement a task scheduler / rate limiter.

**Problem variants (ask which):**
- **CPU-style round-robin/task scheduler:** a ready queue, pick next by priority/time.
- **Rate limiter:** N requests per window (fixed window, sliding window, token bucket) — likely the one they mean.

```python
# Token bucket (single-user):
class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate, self.capacity = rate, capacity
        self.tokens, self.last = capacity, time.monotonic()
    def allow(self) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

**Interview framing:** state the algorithm, the per-user key (Q393), where it runs (middleware/Redis), and the headers (Limit/Remaining/Reset + 429 + Retry-After).

---

## Q718: Implement a concurrent counter (thread-safe increments).

**Approach (compare the three):**
- **Lock (`threading.Lock`):** serialize increments — correct, simple, blocks threads.
- **Atomic via GIL (`+=` is NOT atomic across load/inc/store)** — so use `itertools.count()`? No — the reliable trick: **`queue` or a lock**.
- **True atomic increment:** use `multiprocessing` primitives, or the atomic exchange in `asyncio.Lock` for coroutines (single-threaded event loop → a plain int is atomic per turn).

```python
import threading

class Counter:
    def __init__(self):
        self._n = 0
        self._lock = threading.Lock()
    def inc(self) -> int:
        with self._lock:
            self._n += 1
            return self._n
```

**Interview insight to name:** in **asyncio** (your FastAPI workers), there's one thread per loop → increments between `await`s are safe without a lock; with *threads* you need the lock; with **processes** you need IPC (queue/shared memory). Matching the concurrency model to the right primitive is the whole question (Q649).

---

## Q719: Implement a producer–consumer with a bounded queue.

**Approach:** a bounded queue + condition/`queue.Queue(maxsize=N)` with `put`/`get` blocking semantics — the Python built-in does the waiting. Show the manual version to demonstrate the mechanism.

```python
import asyncio

async def worker(q: asyncio.Queue, name: str):
    while True:
        item = await q.get()
        try:
            await process(item)          # your work
        finally:
            q.task_done()

async def main():
    q = asyncio.Queue(maxsize=100)       # bounded = backpressure (Q439)
    producers = [asyncio.create_task(produce(q)) for _ in range(2)]
    workers = [asyncio.create_task(worker(q, f"w{i}")) for i in range(8)]
    await asyncio.gather(*producers)
    await q.join()                       # wait until all items done
    for w in workers: w.cancel()
```

**Concepts to name:** bounded queue = backpressure (Q439), at-least-once + idempotency for workers (Q396, Q433), graceful shutdown on cancel, and this pattern = the *exact* shape of your resume-parsing pipeline (S3 event → queue → worker, Q427).

---

## Q720: Design a rate limiter for an API (full design).

**Requirements:** per-user and per-IP limits, different tiers, bursty-but-bounded, distributed.

**Design:**
1. **Where:** middleware in the API (Q393) + edge (WAF/nginx) for DDoS-ish protection.
2. **Algorithm:** **token bucket** (burst + steady rate) for per-user; **sliding window** (Redis ZSET or fixed-window INCR) for per-IP/tier accounting.
3. **Distributed store:** Redis — atomic INCR/EXPIRE (fixed window) or sorted-set timestamps (sliding window); works across app instances (Q393).
4. **Response:** on success include `X-RateLimit-Limit/Remaining/Reset`; on limit → **429** + `Retry-After`; client honors Retry-After (Q398).
5. **Tiers:** anonymous < authenticated < paid; read vs write; **LLM endpoints capped tighter** (cost, Q272/Q393).
6. **Config + monitor:** per-user limits from the user record; alert on repeated 429s (abuse); metrics per key (Q631).
7. **Edge cases:** clock skew (use Redis time), memory bounds (TTL on keys), auth-less requests (IP fallback).

**Code (fixed window, Redis):**
```python
key = f"rl:{user_id}:{int(now // window)}"
n = await redis.incr(key)
if n == 1: await redis.expire(key, window)
if n > limit: raise RateLimited(retry_after=window - (now % window))
```

