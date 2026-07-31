# Python Essentials — Last-Minute Syntax Cheatsheet

One-page dense reference for writing correct Python 3 in coding interviews. Every snippet is syntactically valid and tested.

## Fast I/O

```python
import sys, io

# Slow for large input — DO NOT use input() in big problems
sys.stdin = io.TextIOWrapper(io.BytesIO(b"42\n"))
n = int(input())

# Fast: read line, split, map to int   ~3-5x faster
sys.stdin = io.TextIOWrapper(io.BytesIO(b"7 8\n9 10\n"))
n, m = map(int, sys.stdin.readline().split())
arr = list(map(int, sys.stdin.readline().split()))

# Fastest: read ALL tokens at once at start
# Real usage: data = sys.stdin.buffer.read().split()  (sys.stdin.buffer in a contest)
raw = io.BufferedReader(io.BytesIO(b"11 12 13 14 15 16 17 18 19 20 21 22 23\n"))  # simulates sys.stdin.buffer
data = raw.read().split()               # list of bytes tokens
it = iter(data)
n = int(next(it))
x = float(next(it))
arr = [int(next(it)) for _ in range(n)]

# Output: one sys.stdout.write call at the end (fast)
ans, result = 42, [1, 2]       # placeholder results
out = []
out.append(str(ans))
out.append(" ".join(map(str, result)))
sys.stdout.write("\n".join(out) + "\n")
```

## Imports — copy this block blindly

```python
from collections import *     # deque, Counter, defaultdict, OrderedDict
from heapq import *           # heapify, heappush, heappop, heappushpop
import math                   # gcd, lcm, comb, perm, isqrt, inf
import bisect                 # bisect_left, bisect_right, insort
import itertools              # permutations, combinations, accumulate, product
```

## List

```python
a = [0] * 5                   # [0,0,0,0,0]
x, i, j = 0, 1, 2             # sample values used below (x is present in a)
b = [6, 7]                    # sample list for extend
grid = [[0] * 3 for _ in range(2)]   # 2D — MUST use comprehension
# WARNING: [[0]*3]*2 aliases the same inner row; mutating one mutates all.

a.append(x)                   # push to end, O(1) amortized
a.pop()                       # remove end, O(1); returns value
a.pop(i)                      # remove index i, O(n)
a.insert(i, x)                # insert at i, shifts right, O(n)
a.remove(x)                   # remove first occurrence by VALUE, O(n)
a.index(x)                    # first index of value x, O(n); ValueError if absent
a.count(x)                    # occurrences of x, O(n)
a.extend(b)                   # append all of b, O(len(b))
a.reverse()                   # in-place reverse, O(n)
a.sort()                      # in-place ascending, O(n log n)
a.sort(reverse=True)          # in-place descending
a.sort(key=lambda x: abs(x))  # sort by key function
b = sorted(a)                 # NEW sorted list, original untouched
b = sorted(a, reverse=True)
b = sorted(a, key=lambda x: -x)
a.clear()
x = a.copy()                  # shallow copy

# Slicing — a[start:stop:step], start inclusive, stop EXCLUSIVE
a = [1, 2, 3, 4, 5]           # fresh list for the slicing demos
b = a[1:4]          # elements at index 1,2,3
b = a[:3]           # first 3
b = a[2:]           # from index 2 to end
b = a[:]            # full copy
b = a[::-1]         # reversed copy
b = a[::2]          # every 2nd element
b = a[-1]           # last element
b = a[-2:]          # last 2 elements
b = a[-3:-1]        # index len-3 .. len-2 (NOT the last)
a[1:3] = [9, 9, 9]  # slice assignment, O(k+n)

# Swaps
a[i], a[j] = a[j], a[i]
```

Complexity: indexing O(1); append/pop-end O(1) amortized; everything by value/position O(n); sort O(n log n).

## Dict

```python
d = {}                         # literal
d["k"] = 1                     # insert/update
v = d["k"]                     # KeyError if missing — avoid
v = d.get("k", 0)              # returns 0 if missing (never raises)
v = d.get("missing", 0)        # 0 — get with default
d.setdefault("new", []).append(1)  # insert default only if key absent, return value
"k" in d                       # membership, O(1)
del d["k"]                     # remove; KeyError if absent
d.pop("k", None)               # remove with default, safe
for k in d:                    # iterate keys
    pass
for k, v in d.items():         # iterate pairs
    pass
for v in d.values():
    pass
len(d)

# Defaultdict — auto-creates missing keys
from collections import defaultdict
x = 1
dd = defaultdict(int)          # factory: missing key -> 0
dd[x] += 1                     # works even if x absent
dl = defaultdict(list)         # missing -> []
dl["k"].append(1)              # 'k' auto-created as []
ds = defaultdict(set)          # missing -> set
ds["k"].add(1)
# NOTE: d[k] auto-inserts on READ; d.get(k, default) never inserts.

# Counter — counting bag
from collections import Counter
c = Counter("aab")             # Counter({'a': 2, 'b': 1})
c["z"]                         # 0 (no KeyError)
c.update("abb")                # add more
c.most_common(2)               # [('a', 2), ('b', 1)]
list(c.elements())             # ['a','a','b'] (order arbitrary)
# Arithmetic (missing keys count as 0):
#   c + d  union of counts; c - d  positive diffs only
#   c & d  min counts;        c | d  max counts
a, b = Counter("abc"), Counter("bcd")
(a + b) == Counter({'a':1,'b':2,'c':2,'d':1})
(a & b) == Counter({'b':1,'c':1})          # intersection
(a - b) == Counter({'a':1})                # difference (never negative)
(a | b) == Counter({'a':1,'b':1,'c':1,'d':1})
c.total()                                  # sum of counts, Py3.10+
```

## Set

```python
x = 4                          # sample value
s = {1, 2, 3}                  # literal; {} is an EMPTY DICT
s.add(x)                       # insert, O(1)
s.discard(99)                  # remove; NO error if missing
s.remove(1)                    # remove; KeyError if missing
x in s                         # membership, O(1)
t = {3, 4}
s | t                          # union, O(len(s)+len(t))
s & t                          # intersection
s - t                          # difference (in s, not in t)
s ^ t                          # symmetric difference
s <= t                         # subset test
frozenset([1, 2])              # immutable/hashable — usable as dict key
```

## Tuple

```python
t = (1, 2, 3)                  # immutable, hashable — great dict key
a, b = 1, 2                    # unpacking / swap
x, y, z = t                    # unpack into three variables
pair = ("a", 1)
k, v = pair                    # unpack in loop: for k, v in d.items()
t = (1,)                       # single-element tuple NEEDS trailing comma
# returns like [a, b] where a, b = two_sum(...) unpack into two variables
```

## String methods

```python
s = "Hello World"
x, y, w = 1, 2, 4              # sample values for f-strings below
s.split()                      # ['Hello','World'] — splits on whitespace
s.split(",")                   # split on delimiter
"a,b,,c".split(",")            # ['a','b','','c']
"-".join(["a", "b"])           # 'a-b'  (join on the separator)
s.strip()                      # trim whitespace both ends
s.lstrip(); s.rstrip()
s.lower(); s.upper()
s.isdigit(); s.isalpha(); s.isalnum(); s.isspace()
s.startswith("He"); s.endswith("ld")
s.count("l")                   # non-overlapping occurrences
s.find("World")                # first index or -1
s.rfind("o")                   # last index or -1
s.replace("l", "L")            # replace ALL occurrences
str(42).zfill(5)               # '00042'
s.swapcase(); s.title()
# Strings are IMMUTABLE — every method returns a new string.

# f-strings
name, n, pi = "a", 42, 3.14159
f"{name}"                      # 'a'
f"{n:05d}"                     # '00042'
f"{pi:.2f}"                    # '3.14'
f"{n:>5}"                      # '   42' right-align width 5
f"{n:<5}"                      # '42   '
f"{n:^5}"                      # '  42 '
f"{255:x}"                     # 'ff' lowercase hex
f"{255:X}"                     # 'FF'
f"{n:>5d}"                     # width via format spec
f"{n:>{w}}"                    # width from variable w
f"{x + y}"                     # any expression inside braces
```

## Type conversions

```python
int("ff", 16)                  # 255 — base conversion
int("101", 2)                  # 5
int("12")                      # 12
float("3.5"); str(7)
ord("a")                       # 97 — char to ASCII code
chr(97)                        # 'a' — code to char
bin(5)                         # '0b101'
hex(255)                       # '0xff'
oct(8)                         # '0o10'
list(map(int, "1 2 3".split()))   # [1,2,3]
"".join(str(x) for x in [1,2,3])  # '123'
list(map(int, str(1234)))      # digits of a number: [1,2,3,4]
int("".join(map(str, [1,2,3])))   # rebuild number from digit list
```

## enumerate, zip, map, filter, sorted

```python
# Sample data
arr, s = [3, 1, 2], "abc"
pairs = [("a", 1), ("b", 2)]
A, B = [1, 2], [3, 4]
matrix = [[1, 2], [3, 4]]
points = [(1, 9), (2, 3)]
words, items = ["bb", "a", "ccc"], [("b", 1), ("a", 2)]

for i, v in enumerate(arr):            # i = index, v = value
    pass
for i, (k, v) in enumerate(pairs):     # unpack nested pairs
    pass
for i, ch in enumerate(s, 1):          # start index at 1
    pass

for a, b in zip(A, B):                 # parallel iteration, stops at shorter
    pass
list(zip([1, 2], [3, 4]))              # [(1,3),(2,4)]
list(zip(*matrix))                     # TRANSPOSE rows->columns

list(map(lambda x: x * 2, [1, 2, 3]))  # [2,4,6]
list(filter(lambda x: x % 2 == 0, [1,2,3,4]))  # [2,4]
# map/filter return iterators — wrap in list() or iterate directly.

# sorted — returns new list; accepts ANY iterable (dict, set, string)
sorted("cba")                              # ['a','b','c']
sorted([3,1,2], reverse=True)              # [3,2,1]
sorted(points, key=lambda p: p[1])         # sort by 2nd element
sorted(words, key=len)                     # by length
sorted(items, key=lambda kv: (-kv[1], kv[0]))  # freq desc, then value asc
max(words, key=len)                        # max by key
min(words)                                 # lexicographic min (works on strings)
```

## List comprehensions

```python
grid = [[1, 2], [3, 4]]
arr = [-2, 1, 0, 3]
[x * x for x in range(5)]                         # [0,1,4,9,16]
[x for x in range(10) if x % 2 == 0]              # with condition (filters AFTER for)
[(i, j) for i in range(2) for j in range(2)]      # nested loops (cartesian)
[x for row in grid for x in row]                  # FLATTEN a 2D grid
# dict comprehension uses BRACES, not brackets:
{k: k * 2 for k in range(3)}                      # {0:0, 1:2, 2:4}  dict comp
{x % 2 for x in range(4)}                         # {0, 1}  set comp
[x for x in arr if x > 0 if x % 2 == 0]           # chained conditions (AND)
[x if x > 0 else 0 for x in arr]                  # if/else — goes BEFORE for
```

## Generator expressions

```python
arr = [1, 2, 3, -4]
words = ["aa", "b"]
gen = (x * 2 for x in range(10**7))    # lazy — one element at a time
sum(gen)                               # no huge list built; sum(x*x for x in arr)
any(x > 5 for x in arr)                # short-circuits True
all(x > 0 for x in arr)
max(len(w) for w in words)
# generator = iterable; memory O(1) vs list O(n). Used once.
```

## *args / **kwargs

```python
def f(*args, **kwargs):          # *args = positional tuple, **kwargs = dict
    total = sum(args)
    if "b" in kwargs:
        return total + kwargs["b"]
f(1, 2, 3, b=4)
def g(a, b, c): return a + b + c
vals = [1, 2, 3]
g(*vals)                         # unpack list into positional args
g(**{"a": 1, "b": 2, "c": 3})    # unpack dict into keyword args
```

## global / nonlocal

```python
count = 0
def inc():
    global count                 # modify module-level variable
    count += 1

def outer():
    x = 0
    def inner():
        nonlocal x               # modify enclosing function's variable
        x += 1
```

## Read-only built-ins worth knowing

```python
arr = [3, 1, 2]
a, b, c = [1, 2], [3, 4], [5]
iterable = "cba"
sum(arr); min(arr); max(arr); abs(-5); len(arr)
divmod(17, 5)                    # (3, 2) quotient+remainder in one call
any([False, True]); all([True, True])
enumerate(arr)                   # lazily yields (index, value)
zip(a, b, c)                     # stop at shortest
sorted(iterable)                 # works on strings, dicts (keys), sets
list(range(5))                   # [0,1,2,3,4]
round(2.5)                       # 2 (banker's rounding); use math.ceil/floor for control
```
