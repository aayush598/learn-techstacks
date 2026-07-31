# 17. Python Tricks & Fast I/O

Input/output and built-in tricks that save time in coding rounds.

## Fast input: read everything at once (fastest)

Use when the input can be read as a stream of whitespace-separated tokens.

```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()   # list of bytes tokens
    ip = 0                                   # index pointer

    n = int(data[ip]); ip += 1
    arr = list(map(int, data[ip:ip + n])); ip += n
    s = data[ip].decode(); ip += 1           # bytes -> str for string tokens

    out = []
    out.append(str(sum(arr)))
    out.append(s.upper())
    sys.stdout.write('\n'.join(out))         # one write, no trailing newline needed

solve()
```

Input:
```
3
10 20 30
abc
```
Output:
```
60
ABC
```

Complexity: O(total input bytes) for parsing — roughly 2-4x faster than
`input()` per line for large inputs. `ip` pointer style keeps O(1) lookup and
works with any number of tokens.

## Line-based reading (simpler, fine for most problems)

```python
import sys
input = sys.stdin.readline                   # bind for speed

n = int(input())
arr = list(map(int, input().split()))
print(n, arr)
```

### Multi-integer line

```python
a, b, c = map(int, input().split())
```

### Reading a 2D grid of numbers

```python
r, c = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(r)]
```

### Reading a character grid (no spaces)

```python
r, c = map(int, input().split())
grid = [list(input().strip()) for _ in range(r)]
print(grid[0][1])   # 'B'
```

## Fast output

```python
results = [10, 20, 30]       # whatever your loop produces
out = []
for x in results:
    out.append(str(x))
sys.stdout.write('\n'.join(out))   # single write; add '\n' if trailing newline required

# or: sys.stdout.write('\n'.join(map(str, results)))
```

Never `print` inside a hot loop — string building + one write is much faster.

## Sorting tricks

```python
arr = [(1, 'a'), (3, 'c'), (2, 'b')]
sorted(arr, key=lambda x: x[1])                    # sort by second element
sorted(arr, key=lambda x: (-x[0], x[1]))           # desc by first, asc by second
sorted(arr, reverse=True)                          # desc by whole tuple
arr.sort()                                         # in-place sort of the list

words = ['banana', 'apple', 'cherry']
sorted(words, key=len)                             # by length
sorted(words, key=lambda w: w[::-1])               # by reversed string
```

### Sorting a dict by values

```python
d = {'a': 3, 'b': 1, 'c': 2}
sorted(d, key=d.get)                               # keys sorted by value: ['b', 'c', 'a']
sorted(d.items(), key=lambda kv: kv[1], reverse=True)  # [('a', 3), ('c', 2), ('b', 1)]
sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))  # value desc, key asc
```

### max / min with key

```python
arr = [(1, 'a'), (3, 'c'), (2, 'b')]
max(arr, key=lambda x: x[0])       # (3, 'c')
min(arr, key=lambda x: x[1])       # (1, 'a')
nums = [4, -1, 2, -7]
max(nums, key=abs)                 # -7
```

## itertools essentials

```python
from itertools import product, permutations, combinations, chain, accumulate, combinations_with_replacement

list(product([0, 1], repeat=2))   # [(0,0), (0,1), (1,0), (1,1)]  — bitmask/two-choice loops
list(permutations([1, 2, 3]))     # all 6 orderings (use for small n)
list(permutations([1, 2, 3], 2))  # ordered picks of length 2
list(combinations([1, 2, 3, 4], 2))  # 6 unordered pairs
list(combinations_with_replacement([1, 2, 3], 2))  # [(1,1),(1,2),(1,3),(2,2),(2,3),(3,3)]
list(chain([1, 2], [3, 4]))       # [1, 2, 3, 4]  — flatten
list(accumulate([1, 2, 3, 4]))    # [1, 3, 6, 10] — prefix sums!
list(accumulate([1, 2, 3, 4], max))  # running max: [1, 2, 3, 4]
```

## functools.reduce

```python
from functools import reduce
reduce(lambda a, b: a + b, [1, 2, 3, 4])   # 10
reduce(lambda a, b: a * b, [1, 2, 3, 4])   # 24
reduce(max, [3, 1, 4, 1, 5])               # 5
```

## filter

```python
list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))   # [2, 4]
list(filter(None, [0, 1, '', 'a', None, 3]))          # [1, 'a', 3]  (falsy removed)
```

## groupby — consecutive equal runs

```python
from itertools import groupby

[(k, list(v)) for k, v in groupby([1, 1, 2, 2, 2, 3], lambda x: x)]
# [(1, [1, 1]), (2, [2, 2, 2]), (3, [3])]
# NOTE: only groups CONSECUTIVE equal items — sort first if order-independent
```

## Unpacking and assignment tricks

```python
a, *rest = [1, 2, 3, 4]     # a = 1, rest = [2, 3, 4]
first, *mid, last = [1, 2, 3, 4]   # first=1, mid=[2,3], last=4
x, y = 1, 2
x, y = y, x                 # swap without temp: x, y = 2, 1
f0, f1 = 0, 1
f0, f1 = f1, f0 + f1        # tuple unpacking drives assignment (fib-style): f0, f1 = 1, 1

arr = [10, 20, 30]
d = {"a": 1, "b": 2}
for i, v in enumerate(arr):           # index + value
    print(i, v)
for k, v in d.items():                # dict iteration
    print(k, v)
```

## Negative indexing and slicing

```python
s = 'hello'
s[-1]        # 'o'  (last element)
s[-3:]       # 'llo'
s[::-1]      # 'olleh'  (reverse)
arr[:-1]     # all but last
arr[1:]      # all but first
arr[::2]     # every 2nd element
arr[::-1]    # reversed copy (arr.reverse() reverses in place, returns None)
```

## Chained comparisons

```python
x, r, c, rows, cols = 5, 0, 3, 4, 5
1 < x < 10         # True — no need for (1 < x and x < 10)
0 <= r < rows and 0 <= c < cols    # classic grid bounds check in one line (True)
```

## any / all with generators

```python
nums = [1, 2, 3, 4]
any(x % 2 == 0 for x in nums)      # True — at least one even
all(x > 0 for x in nums)           # True — all positive
any(nums)                          # True if any truthy element
```

## defaultdict of list — grouping pattern

```python
from collections import defaultdict

groups = defaultdict(list)
for word in ['eat', 'tea', 'tan', 'ate']:
    groups[''.join(sorted(word))].append(word)
# {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan']}

# also useful: defaultdict(int), defaultdict(set)
# regular dict .get fallback:  d.get(k, default)  /  d.setdefault(k, [])
```

## Counter

```python
from collections import Counter

c = Counter('aabbbc')
c.most_common()          # [('b', 3), ('a', 2), ('c', 1)]
c.most_common(1)         # [('b', 3)]  top element
c['a']                   # 2
c.update('ab')           # add counts
list(c.elements())       # each element repeated by its count
```

## bisect — binary search on sorted lists

```python
import bisect

arr = [1, 3, 3, 5, 7]
bisect.bisect_left(arr, 3)    # 1  — first index where 3 can be inserted (first 3)
bisect.bisect_right(arr, 3)   # 3  — index after last 3
bisect.bisect_left(arr, 4)    # 3  — insertion point of a missing value
bisect.insort(arr, 4)         # insert keeping order: [1, 3, 3, 4, 5, 7]

# find count of value x:  bisect_right(a, x) - bisect_left(a, x)
# index of first value >= x:  bisect_left
# index of first value >  x:  bisect_right
```

## heapq — priority queue / min-heap

```python
import heapq

h = [5, 3, 8]
heapq.heapify(h)          # O(n) — convert list to a min-heap
heapq.heappush(h, 1)      # O(log n)
smallest = heapq.heappop(h)     # 1 (O(log n))
top2 = heapq.nlargest(2, h)     # O(n log k) top-k elements
top2small = heapq.nsmallest(2, h)
h[0]                        # peek at min without popping (O(1))
```

Max-heap via negation:

```python
h = [-5, -3, -8]
heapq.heapify(h)
max_val = -heapq.heappop(h)   # 8
```

Dijkstra-style push of (priority, item) tuples works directly.

## Quick reference

| Task | Snippet |
|---|---|
| Prefix sums | `list(accumulate(arr))` |
| Flatten list of lists | `list(chain(*lst))` |
| Transpose rows/cols | `list(zip(*mat))` |
| All pairs | `combinations(arr, 2)` |
| Toggle/boolean flip | `x = 1 - x` |
| Clamp value | `max(lo, min(x, hi))` |
| Unique preserving order | `list(dict.fromkeys(arr))` |
| Frequency dict | `{x: arr.count(x)}` is slow — use `Counter` |
| Is sorted | `arr == sorted(arr)` (or check `all(a <= b for a, b in zip(arr, arr[1:]))`) |
