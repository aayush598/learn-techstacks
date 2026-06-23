# micro1 Python Developer — Interview Q&A

**Focus Areas:** Advanced Python Development (Scalable Systems) | Python & Data Structures | Version Control & Collaborative Engineering | Model Tuning & Optimization

---

## 1. ADVANCED PYTHON DEVELOPMENT (SCALABLE SYSTEMS)

### Q1: What are Python generators and how do they help with scalability?
**A:** Generators (`yield`) produce items lazily — one at a time — instead of building a full list in memory. This is critical for scalability when processing large datasets or streams.

```python
def read_large_file(file_path):
    with open(file_path) as f:
        for line in f:
            yield line.strip()
```

**Memory comparison:** A list of 10M integers ~ 80MB; a generator producing them is ~ a few hundred bytes.

### Q2: Explain the GIL (Global Interpreter Lock). How do you work around it?
**A:** The GIL allows only one thread to execute Python bytecode at a time. For CPU-bound work, use `multiprocessing` (separate processes, each with its own GIL). For I/O-bound work, use `threading` or `asyncio`.

```python
from multiprocessing import Pool
with Pool(4) as p:
    results = p.map(cpu_intensive_func, data)

import asyncio
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
```

### Q3: Describe `asyncio` vs threading vs multiprocessing.
| Feature | threading | multiprocessing | asyncio |
|---|---|---|---|
| Concurrency model | Preemptive | Preemptive | Cooperative |
| GIL impact | Blocked for CPU | Bypassed (separate processes) | Single-threaded, non-blocking |
| Best for | I/O-bound | CPU-bound | I/O-bound (many connections) |
| Overhead | Low (threads share memory) | High (process isolation) | Lowest (single thread) |

### Q4: What are decorators? Write a decorator that measures execution time.
**A:** Decorators wrap functions to extend behavior.

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

### Q5: Explain context managers and the `with` statement. Write one for a database connection.
**A:** Context managers handle setup/teardown. Use `__enter__` / `__exit__` or `@contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def db_connection(conn_string):
    conn = create_connection(conn_string)
    try:
        yield conn
    finally:
        conn.close()

with db_connection("postgresql://...") as conn:
    conn.execute("SELECT * FROM users")
```

### Q6: What is `__slots__` and when would you use it?
**A:** `__slots__` restricts attribute creation to a fixed set, reducing memory per instance (no per-instance `__dict__`). Use when creating millions of objects.

```python
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y
# ~40-50% memory reduction vs. standard class
```

### Q7: Describe Python's memory management and garbage collection.
**A:** Python uses **reference counting** (immediate deallocation when refcount hits 0) + **generational GC** (cyclic garbage). The `gc` module exposes the collector. Use `gc.get_objects()`, `gc.collect()` for debugging. `weakref` avoids circular references.

### Q8: What's the difference between `deepcopy` and `shallow copy`?
**A:** Shallow copy creates a new object but inserts references to the original's child objects. Deep copy recursively copies everything.

```python
import copy
original = {'a': [1, 2, 3]}
shallow = copy.copy(original)
deep = copy.deepcopy(original)
shallow['a'].append(4)  # Also mutates original['a']
deep['a'].append(5)     # Doesn't affect original
```

### Q9: How do you design a rate-limited API client in Python?
**A:** Use a token bucket or sliding window with `asyncio.Semaphore` or `time.sleep` with `functools.lru_cache`.

```python
import asyncio
import time

class RateLimiter:
    def __init__(self, calls_per_second):
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0

    async def acquire(self):
        now = time.monotonic()
        wait = self.min_interval - (now - self.last_call)
        if wait > 0:
            await asyncio.sleep(wait)
        self.last_call = time.monotonic()
```

### Q10: Explain metaclasses. When would one use them?
**A:** Metaclasses (`type` subclasses) control class creation — they're the "classes of classes." Used in ORMs (SQLAlchemy), Django models, and singleton/registry patterns.

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    pass
```

---

## 2. PYTHON & DATA STRUCTURES

### Q11: What is the time complexity of list, dict, and set operations?
| Operation | list | dict | set |
|---|---|---|---|
| Access | O(1) | O(1) | N/A |
| Search | O(n) | O(1) avg | O(1) avg |
| Insert | O(1) amortized | O(1) avg | O(1) avg |
| Delete | O(n) | O(1) avg | O(1) avg |

**Key insight:** Dicts and sets are hash tables. Lists are dynamic arrays.

### Q12: Reverse a linked list. Write the code.
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev
# Time: O(n), Space: O(1)
```

### Q13: Find the first non-repeating character in a string.
```python
from collections import Counter

def first_unique_char(s: str) -> int:
    count = Counter(s)
    for i, ch in enumerate(s):
        if count[ch] == 1:
            return i
    return -1
# Time: O(n), Space: O(1) — fixed alphabet size
```

### Q14: Implement a LRU (Least Recently Used) Cache.
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
# get/put both O(1)
```

### Q15: Two-sum problem (all approaches).
```python
def two_sum(nums, target):
    seen = {}
    for i, v in enumerate(nums):
        diff = target - v
        if diff in seen:
            return [seen[diff], i]
        seen[v] = i
    return []
# Time: O(n), Space: O(n)
```

### Q16: Merge two sorted arrays in-place (no extra space).
```python
def merge(nums1, m, nums2, n):
    p1, p2, p = m - 1, n - 1, m + n - 1
    while p2 >= 0:
        if p1 >= 0 and nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
# Time: O(m+n), Space: O(1)
```

### Q17: Explain BFS vs DFS with use cases.
| Algorithm | Data Structure | Use Case |
|---|---|---|
| BFS | Queue | Shortest path, level-order traversal |
| DFS | Stack/Recursion | Topological sort, maze solving, tree traversals |

```python
from collections import deque

def bfs(graph, start):
    visited, queue = set(), deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node] - visited)
    return visited
```

### Q18: Determine if a binary tree is balanced.
```python
def is_balanced(root):
    def dfs(node):
        if not node:
            return 0
        left = dfs(node.left)
        right = dfs(node.right)
        if left == -1 or right == -1 or abs(left - right) > 1:
            return -1
        return max(left, right) + 1
    return dfs(root) != -1
```

### Q19: Find all anagrams in a string.
```python
from collections import Counter

def find_anagrams(s, p):
    result = []
    p_count = Counter(p)
    s_count = Counter()

    for i, ch in enumerate(s):
        s_count[ch] += 1
        if i >= len(p):
            if s_count[s[i - len(p)]] == 1:
                del s_count[s[i - len(p)]]
            else:
                s_count[s[i - len(p)]] -= 1
        if s_count == p_count:
            result.append(i - len(p) + 1)
    return result
# Time: O(n), Space: O(k) where k = alphabet size
```

### Q20: Valid parentheses problem.
```python
def is_valid(s: str) -> bool:
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    for ch in s:
        if ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack
```

---

## 3. VERSION CONTROL & COLLABORATIVE ENGINEERING

### Q21: What's the difference between `git merge` and `git rebase`?
| Operation | Pros | Cons |
|---|---|---|
| `merge` | Preserves history, safe | Creates merge commits, messy log |
| `rebase` | Clean linear history | Rewrites commits, dangerous on shared branches |

**Rule:** Rebase locally, merge publicly.

### Q22: You accidentally committed to `main`. How do you fix it?
```bash
git reset HEAD~1 --soft   # Keep changes staged, undo commit
git stash
git checkout -b feature-branch
git stash pop
git add . && git commit -m "fix: move to correct branch"
# Then push feature-branch, and if main already has the commit:
git push origin :main     # Only if you have force-push access
```

Or safer: `git revert HEAD` on `main`, then `git cherry-pick` the commit to the correct branch.

### Q23: What is an interactive rebase used for?
```bash
git rebase -i HEAD~5
# Allows: pick, reword, edit, squash, fixup, drop
# Used to clean up commits before PR: squash WIP commits, reword messages
```

### Q24: Describe a healthy code review workflow.
1. **Small PRs** (< 400 lines) — reviewed faster, fewer defects
2. **Descriptive title + description** explaining what and why
3. **Self-review first** before requesting reviewers
4. **Address all comments** — resolve or reply
5. **No merge until CI passes** and at least one approval
6. **Use squash merge** to keep main history clean

### Q25: How do you handle merge conflicts?
```bash
git fetch origin
git merge origin/main
# Resolve conflicts in files, then:
git add <resolved-files>
git commit
```
Or use `git mergetool` (vimdiff, VSCode, etc.).

### Q26: What's the difference between `git stash pop` and `git stash apply`?
- `apply` keeps the stash entry
- `pop` applies and drops it
- Use `apply` when you might need the same stash on multiple branches

### Q27: What is CI/CD and how would you set it up for a Python project?
**CI:** Automatically run tests, lint, type-check on every PR.
**CD:** Deploy to staging/production after merge.

Example `.github/workflows/ci.yml`:
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: mypy src/
      - run: pytest --cov=src/
```

### Q28: Explain GitFlow vs Trunk-Based Development.
| Strategy | Branches | Deploy frequency | Best for |
|---|---|---|---|
| GitFlow | main, develop, feature, release, hotfix | Scheduled releases | Enterprise, release cycles |
| Trunk-Based | main + short-lived feature branches | Multiple times/day | Startups, SaaS, CI/CD |

**micro1 context:** Trunk-based is common in fast-paced remote teams.

### Q29: What does `git bisect` do?
Binary searches through history to find the commit that introduced a bug.
```bash
git bisect start
git bisect bad              # current commit is bad
git bisect good v1.0        # known good commit
# Git checks out midpoint — test, then:
git bisect good             # or git bisect bad
git bisect reset            # when done
```

### Q30: What information should a good commit message contain?
Conventional Commits format:
```
<type>(<scope>): <short summary> (max 50 chars)

<body> — explains what and why (not how), wrap at 72 chars
```
Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`

---

## 4. MODEL TUNING & OPTIMIZATION

### Q31: How do you profile Python code?
**Built-in:** `cProfile`, `timeit`, `tracemalloc`.
**Third-party:** `py-spy`, `memory_profiler`, `line_profiler`.

```python
import cProfile, pstats
cProfile.run('my_func()', 'output.prof')
p = pstats.Stats('output.prof')
p.sort_stats('cumtime').print_stats(10)
```

### Q32: Find the bottleneck in this code and optimize it.
```python
# Original — O(n²) string concatenation
def build_string(n):
    result = ""
    for i in range(n):
        result += str(i)  # Creates new string each iteration
    return result

# Optimized — O(n)
def build_string(n):
    return "".join(str(i) for i in range(n))
```

### Q33: How do you optimize a slow database query in a Python app?
1. **Profile first** — use `EXPLAIN ANALYZE` in SQL
2. **Add indexes** — on columns used in `WHERE`, `JOIN`, `ORDER BY`
3. **N+1 problem** — use eager loading (SQLAlchemy `joinedload`)
4. **Connection pooling** — use `HikariConnectionPool` / `psycopg2.pool`
5. **Caching** — Redis/memcached for hot data
6. **Batch operations** — `bulk_insert`, `bulk_update`

```python
# Bad: N+1
for user in session.query(User):
    print(user.addresses)  # Fires query each iteration

# Good: eager load
for user in session.query(User).options(joinedload(User.addresses)):
    print(user.addresses)
```

### Q34: What is memoization? Implement it.
**A:** Caching function results based on input.

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Q35: How do you handle large datasets that don't fit in memory?
1. **Use generators** (lazy evaluation)
2. **Process in chunks** — `pandas.read_csv(chunksize=10000)`
3. **Use streaming** — `requests.Response.iter_content()`
4. **Database-level aggregation** — push computation to SQL
5. **Use memory-efficient data structures** — `array`, `__slots__`, `numpy`
6. **Use distributed computing** — Dask, Ray, Spark

### Q36: Optimize this list comprehension.
```python
# Original — builds full list, then filters
result = [x for x in range(10_000_000) if x % 2 == 0][:100]

# Optimized — generator + islice
from itertools import islice
result = list(islice((x for x in range(10_000_000) if x % 2 == 0), 100))
```

### Q37: Explain the difference between CPU-bound and I/O-bound, with optimization strategies.
| Type | Limiter | Python solution |
|---|---|---|
| CPU-bound | Processor speed | `multiprocessing`, C extensions (Cython, PyPy), vectorization (NumPy) |
| I/O-bound | Network/disk latency | `asyncio`, `threading`, connection pooling |

### Q38: How do you optimize API response times in a Python web service?
1. **Caching** — Redis for computed results, HTTP caching headers
2. **Database optimization** — indexes, materialized views, read replicas
3. **Asynchronous processing** — background tasks (Celery) for non-critical work
4. **Pagination** — never return unbounded lists
5. **Gzip compression** — `Content-Encoding: gzip`
6. **Connection pooling** — reuse HTTP connections
7. **CDN** — for static assets
8. **Database connection pooling** — pgbouncer, SQLAlchemy pool

### Q39: Explain the `@functools.lru_cache` decorator internals.
**A:** Uses a dict to store results keyed by arguments. When `maxsize` is reached, it evicts the least-recently-used entry. Thread-safe for CPython. `maxsize=None` stores unlimited entries (use with caution).

### Q40: How would you implement a simple in-memory cache with TTL?
```python
import time
from functools import wraps

def ttl_cache(ttl_seconds=60):
    def decorator(func):
        cache = {}
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs.items()))
            now = time.monotonic()
            if key in cache:
                result, expiry = cache[key]
                if now < expiry:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now + ttl_seconds)
            return result
        return wrapper
    return decorator
```

---

## 5. PYTHON OOP & DESIGN PATTERNS

### Q41: Explain MRO (Method Resolution Order) in Python.
**A:** Python uses C3 linearization. `ClassName.__mro__` shows the order. Used by `super()`.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
print(D.__mro__)
# D -> B -> C -> A -> object
```

### Q42: What are abstract base classes (ABCs)?
**A:** Define interfaces that subclasses must implement.

```python
from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> dict:
        ...
```

### Q43: Implement the Singleton pattern in Python (thread-safe).
```python
import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### Q44: What is the Factory pattern? When is it useful?
**A:** Encapsulates object creation logic. Useful when the exact type depends on runtime data.

```python
class DataParserFactory:
    @staticmethod
    def get_parser(file_type: str):
        parsers = {
            'json': JSONParser,
            'csv': CSVParser,
            'xml': XMLParser,
        }
        return parsers[file_type]()
```

### Q45: Explain the difference between `classmethod` and `staticmethod`.
- `@classmethod` receives `cls` as first arg — can access/modify class state
- `@staticmethod` receives nothing — just a function living in the class namespace

```python
class Config:
    env = "production"

    @classmethod
    def is_production(cls):
        return cls.env == "production"

    @staticmethod
    def validate_port(port):
        return 1024 <= port <= 65535
```

---

## 6. SYSTEM DESIGN (SCALABLE SYSTEMS)

### Q46: Design a URL shortener (like TinyURL).
**Components:** API gateway, web server, DB, cache.
- **Encoding:** Base62 encode auto-increment ID or use hash (MD5 → first 7 chars)
- **DB:** Primary key (short code) → long URL + created_at + click_count
- **Cache:** Redis — `{short_code: long_url}`, TTL 24h
- **Redirect:** 301 (permanent) or 302 (temporary) to long URL
- **Scale:** Read replicas for DB, consistent hashing for cache sharding

### Q47: Design a rate limiter.
**Algorithms:**
1. **Token Bucket** — tokens refill at fixed rate; request consumes a token
2. **Sliding Window Log** — timestamps per user in a sorted set; count in window
3. **Sliding Window Counter** — Redis sorted set with `ZREMRANGEBYSCORE` + `ZCARD`

**Python + Redis:**
```python
import time
import redis

r = redis.Redis()

def is_rate_limited(user_id, max_requests=10, window=60):
    key = f"ratelimit:{user_id}"
    now = time.time()
    r.zadd(key, {now: now})
    r.zremrangebyscore(key, 0, now - window)
    r.expire(key, window)
    return r.zcard(key) > max_requests
```

### Q48: How would you design a task queue for background jobs?
Use **Celery** with Redis/RabbitMQ as broker:
```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def process_data(user_id):
    # Expensive operation
    pass

# Call: process_data.delay(user_id)
```
**Key concepts:** Task idempotency, retries with backoff, dead-letter queues, worker concurrency.

### Q49: Explain horizontal vs vertical scaling.
| | Vertical | Horizontal |
|---|---|---|
| What | Bigger machine | More machines |
| Limit | Hardware cap | Theoretically infinite |
| Complexity | Low | High (load balancer, sharding) |
| Cost | Expensive at high end | Cheaper (commodity hardware) |

### Q50: What is eventual consistency? When is it acceptable?
**A:** After a write, reads may not immediately see it, but will eventually converge. Acceptable for: social media feeds, analytics dashboards, DNS. Not acceptable for: banking transactions, inventory (strong consistency needed).

---

## 7. SYSTEM DESIGN & CODING CHALLENGES (WHITEBOARD)

### Q51: Design a thread-safe producer-consumer queue.
```python
import threading
import queue

def producer(q, items):
    for item in items:
        q.put(item)

def consumer(q):
    while True:
        item = q.get()
        if item is None:  # Poison pill
            break
        process(item)
        q.task_done()

q = queue.Queue(maxsize=100)
# queue.Queue is already thread-safe
```

### Q52: Implement a thread pool from scratch.
```python
import threading
from queue import Queue

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        self.workers = [
            threading.Thread(target=self._worker)
            for _ in range(num_threads)
        ]
        for w in self.workers:
            w.daemon = True
            w.start()

    def _worker(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}")
            self.tasks.task_done()

    def submit(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def wait_completion(self):
        self.tasks.join()
```

### Q53: Design a web scraper that respects `robots.txt` and rate limits.
```python
import asyncio
import aiohttp
from urllib.robotparser import RobotFileParser

class PoliteScraper:
    def __init__(self, delay=1.0):
        self.delay = delay
        self.last_access = {}
        self.robots = {}

    async def fetch(self, url):
        domain = urlparse(url).netloc
        await self._respect_rate_limit(domain)
        # Check robots.txt
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()

    async def _respect_rate_limit(self, domain):
        now = time.monotonic()
        last = self.last_access.get(domain, 0)
        wait = self.delay - (now - last)
        if wait > 0:
            await asyncio.sleep(wait)
        self.last_access[domain] = time.monotonic()
```

### Q54: Implement a simple dependency injection container.
```python
class Container:
    def __init__(self):
        self._services = {}

    def register(self, name, factory, singleton=False):
        self._services[name] = {
            'factory': factory,
            'singleton': singleton,
            'instance': None
        }

    def resolve(self, name):
        service = self._services[name]
        if service['singleton'] and service['instance']:
            return service['instance']
        instance = service['factory'](self)
        if service['singleton']:
            service['instance'] = instance
        return instance

# Usage
container = Container()
container.register('db', lambda c: Database(), singleton=True)
container.register('repo', lambda c: UserRepository(c.resolve('db')))
```

### Q55: Write a function that finds the k most frequent elements.
```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
# Time: O(n log k), Space: O(n)
```

---

## 8. PYTHON TRICKS & BEST PRACTICES

### Q56: Explain `*args` and `**kwargs`.
```python
def func(*args, **kwargs):
    # args → tuple of positional args
    # kwargs → dict of keyword args
    pass
```

### Q57: What's the difference between `is` and `==`?
- `is` — identity (same object in memory)
- `==` — equality (same value)

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True
a is b  # False
```

### Q58: What is a `namedtuple`?
```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(10, 20)
p.x  # 10
p[0]  # 10
# Immutable, lightweight, readable
```

### Q59: Explain `zip`, `map`, `filter`, `reduce`.
```python
list(zip([1, 2], ['a', 'b']))       # [(1, 'a'), (2, 'b')]
list(map(str.upper, ['a', 'b']))    # ['A', 'B']
list(filter(lambda x: x > 0, [-1, 0, 1]))  # [1]
from functools import reduce
reduce(lambda a, b: a * b, [1, 2, 3, 4])   # 24
```

### Q60: What is a `frozenset`?
Immutable version of `set` — hashable, can be used as dict key or in another set.

### Q61: Difference between `defaultdict` and regular `dict`.
```python
from collections import defaultdict
d = defaultdict(list)
d['key'].append(1)  # No KeyError — auto-creates empty list
```

### Q62: Explain `async` / `await` in Python.
```python
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com') as resp:
            return await resp.json()

async def main():
    tasks = [fetch_data() for _ in range(10)]
    results = await asyncio.gather(*tasks)
```

### Q63: What's the Walrus Operator `:=`?
Assignment expression — assign and use in one expression:
```python
if (n := len(items)) > 10:
    print(f"Too many: {n}")
```

### Q64: Explain the `@property` decorator.
```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9
```

### Q65: What is `__init__.py` used for?
Marks a directory as a Python package. Can also define `__all__` to control what's exported with `from package import *`.

---

## 9. MICRO1-SPECIFIC & AI-CONTEXT QUESTIONS

### Q66: How would you build a pipeline to process and clean large-scale training data?
1. **Streaming reads** — generators, not loading everything
2. **Validation** — pydantic/schema enforcement
3. **Deduplication** — hash-based or Bloom filter
4. **Normalization** — consistent formatting, encoding
5. **Parallel processing** — multiprocessing / Dask
6. **Quality scoring** — heuristics or ML model
7. **Output** — write in efficient format (Parquet, TFRecord)

### Q67: How do you ensure data quality in an ML pipeline?
- Schema validation (Great Expectations, Pandera)
- Outlier detection (Z-score, IQR)
- Missing value strategy (drop, impute, flag)
- Distribution monitoring (KS test, drift detection)
- Versioning data (DVC, LakeFS)

### Q68: You have a slow Python script used in production. Walk through your debugging process.
1. **Profile** — `cProfile` + `snakeviz` to visualize
2. **Identify hot spots** — functions with highest cumtime
3. **Add logging** — pinpoint what's slow
4. **Check I/O** — is the DB slow? Are we making too many calls?
5. **Memory** — are we hitting swap? `tracemalloc`
6. **Parallelize** — can work be done concurrently?
7. **Optimize algorithm** — can we reduce complexity?
8. **Cache** — are we recomputing the same thing?

### Q69: Describe experience with cloud platforms relevant to Python.
- **AWS Lambda** — serverless Python functions
- **S3** — store/retrieve data at scale
- **EC2 / ECS** — running Python services
- **RDS / Aurora** — managed databases
- **SQS / SNS** — async messaging
- **CloudWatch** — logging/monitoring

### Q70: How do you handle secrets/config in a Python application?
- **Never hardcode** — not in code, not in .env committed to git
- **Environment variables** — via `os.environ` or `python-dotenv` for local dev
- **Secret managers** — AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager
- **Config libraries** — `pydantic-settings`, `dynaconf`

---

## 10. SAMPLE CODING EXERCISES (EXPECTED FORMAT)

### Q71: Serialize and deserialize a binary tree.
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val; self.left = left; self.right = right

def serialize(root):
    def dfs(node):
        if not node:
            return "null"
        return f"{node.val},{dfs(node.left)},{dfs(node.right)}"
    return dfs(root)

def deserialize(data):
    def dfs():
        val = next(vals)
        if val == "null":
            return None
        node = TreeNode(int(val))
        node.left = dfs()
        node.right = dfs()
        return node
    vals = iter(data.split(","))
    return dfs()
```

### Q72: Word Ladder (BFS).
```python
from collections import deque

def ladder_length(begin_word, end_word, word_list):
    word_set = set(word_list)
    if end_word not in word_set:
        return 0
    q = deque([(begin_word, 1)])
    while q:
        word, length = q.popleft()
        if word == end_word:
            return length
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                new_word = word[:i] + c + word[i+1:]
                if new_word in word_set:
                    word_set.remove(new_word)
                    q.append((new_word, length + 1))
    return 0
```

### Q73: Design a logger with rate limiting.
```python
from collections import defaultdict

class Logger:
    def __init__(self):
        self.last_seen = {}

    def should_print(self, timestamp, message):
        if message not in self.last_seen or timestamp - self.last_seen[message] >= 10:
            self.last_seen[message] = timestamp
            return True
        return False
```

### Q74: Find the longest substring without repeating characters.
```python
def length_of_longest_substring(s):
    char_set = set()
    left = max_len = 0
    for right, ch in enumerate(s):
        while ch in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(ch)
        max_len = max(max_len, right - left + 1)
    return max_len
```

### Q75: Implement `pow(x, n)` efficiently.
```python
def my_pow(x, n):
    if n < 0:
        x, n = 1 / x, -n
    result = 1
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1
    return result
# Time: O(log n), Space: O(1)
```

---

## QUICK REFERENCE CARD

### Time Complexities to Memorize
| Structure | Get | Search | Insert | Delete |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | O(n) |
| Stack/Queue | O(1) top/front | O(n) | O(1) | O(1) |
| Hash Table | O(1) | O(1) | O(1) | O(1) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) |
| Heap | O(1) min | O(n) | O(log n) | O(log n) |

### Big-O Cheat Sheet
- O(1) — Constant: array access, hash lookup
- O(log n) — Logarithmic: binary search, balanced BST
- O(n) — Linear: simple search, string concatenation
- O(n log n) — Linearithmic: merge sort, heapsort
- O(n²) — Quadratic: nested loops, bubble sort

### Python Built-in Sorting
- `sorted()` / `.sort()` — Timsort, O(n log n), stable

### Must-Know Standard Library Modules
`collections`, `itertools`, `functools`, `asyncio`, `multiprocessing`, `threading`, `re`, `json`, `pickle`, `pathlib`, `typing`, `dataclasses`, `abc`, `fractions`, `decimal`, `enum`, `hashlib`, `struct`, `os`, `sys`, `argparse`, `logging`, `unittest`, `pytest`

### CLI Tools to Be Fluent With
`git`, `grep`, `awk`, `sed`, `jq`, `curl`, `docker`, `psql`, `redis-cli`, `tmux`/`screen`

---

*Good luck with the micro1 interview! Focus on writing clean, efficient, and well-structured Python code. Communicate your thought process clearly — they value both technical skill and collaboration.*
