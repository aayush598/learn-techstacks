# Priority 1 — Python Fundamentals (Q1–Q40)

**Why these matter for micro1:** the role is Python-first. Expect quick-fire fundamentals, then a drill-down on *how* things work internally and what fails at scale. Answer structure: define → example → nuance/tradeoff.

---

## Q1: Tell me about your experience with Python.

**Answer framework (3–5 sentences, evidence-based):**

1. **Duration + depth:** "I've been using Python for X years, primarily for backend API development, data processing, and automation."
2. **What you built:** FastAPI/Flask/Django backends, async services, data pipelines, ETL, scripts, tests (pytest), deployment.
3. **Specifics they care about:** async programming (`asyncio`), performance optimization (profiling, caching, query tuning), SQL + ORMs (SQLAlchemy), LLM API integration, Docker/AWS.
4. **Bring your projects:** name 1–2 concrete systems (reference `31_p5_own_projects.md`).
5. **Close with motivation:** "I enjoy Python because it lets me move fast from prototype to production while staying readable and maintainable."

> **Follow-up prep:** be ready for "what was the hardest bug?", "how did you measure performance?", "what would you optimize next?"

---

## Q2: What are the main differences between lists, tuples, sets, and dictionaries?

| | **list** | **tuple** | **set** | **dict** |
|---|---|---|---|---|
| Mutable | Yes | No | Yes | Yes |
| Ordered | Yes (insertion) | Yes | No (unordered) | Yes (insertion order, Py3.7+) |
| Indexed by | Position | Position | Value (hash) | Key |
| Duplicates | Yes | Yes | No | Keys unique |
| Hashing | No | Yes (if contents hashable) | Elements must be hashable | Keys must be hashable |
| Typical use | Dynamic sequences, stacks, queues | Fixed records, keys of sets/dicts | Membership tests, dedupe | Key→value lookup |

```python
l = [1, 2, 2]      # list
t = (1, 2, 2)      # tuple
s = {1, 2}         # set  ({} is a dict! use set())
d = {"a": 1}       # dict
```

**Key nuances:**
- `list`/`dict`/`set` are **mutable**; `tuple` is **immutable** (its elements may still be mutable).
- Sets and dicts have **O(1)** average lookup via hashing; lists/tuples are **O(n)** for `in` checks.
- `dict` preserves insertion order since Python 3.7 (language spec) — earlier it was an implementation detail (Py3.6).
- Tuples of length 1 need a trailing comma: `(1,)`.
- Frozen counterpart: `frozenset` is an immutable set (hashable, usable as a dict key).

---

## Q3: What is the time complexity of lookup in a Python dictionary?

**O(1) average**, **O(n) worst case**.

- **Average case:** key hashes to a slot directly — constant time. Collisions are resolved via open addressing, keeping chain length short.
- **Worst case:** pathological collisions (e.g., a custom `__hash__` returning a constant) degrade to O(n) linear probing.
- **Why it matters:** this is why dicts/sets are the workhorse for fast lookups vs lists' O(n).

> **Follow-up prep:** "why is it O(1)?" → hash function + hash table with open addressing; see Q4.

---

## Q4: How does a Python dictionary work internally?

1. A dict is a **hash table** backed by a compact array of entries (PyPy/CPython: a "combined" table of hashes, keys, values).
2. When you insert, Python calls `hash(key)` → integer.
3. The hash is reduced (masked) to an **index** into the table.
4. **Collision handling:** CPython uses **open addressing** with **perturbation** — on collision it probes the next slot deterministically rather than chaining linked lists.
5. On load (used slots / capacity) crossing ~2/3, the table **resizes** (usually ~2× or 4×) and re-hashes everything — amortized O(1).
6. **Hash randomization:** string hashing is salted per-process (PYTHONHASHSEED) to prevent DoS via hash-collision attacks.
7. Since Py3.7 dicts maintain **insertion order** (a separate compact array of indices).
8. Lookup does: `hash(key)` → probe slot → compare `==` on candidates (hash equality is checked first, then `==`).

**Why keys must be immutable:** if a key's hash changed after insertion, it would become unfindable (hash computed at insert, stored).

---

## Q5: What is the difference between `==` and `is`?

- `==` → **value equality**: "do these two objects have equal values?" (delegates to `__eq__`).
- `is` → **identity equality**: "are these the *same* object in memory?" (compares `id()`/pointers).

```python
a = [1, 2, 3]
b = [1, 2, 3]
a == b  # True  (equal values)
a is b  # False (different objects)

x = 5; y = 5
x is y  # True — small ints (-5..256) are cached/interend, so they're the same object
```

**Nuances:**
- `is` is faster (no `__eq__` call) — use it for **singletons**: `x is None`, `x is True`.
- `None`, `True`, `False` are singletons — always use `is None`, never `== None`.
- `==` on objects without `__eq__` falls back to identity (`is`).
- `is` can be surprising with interned strings and small integers — don't rely on it for values.

---

## Q6: What are mutable and immutable objects in Python?

- **Mutable:** can be changed in place after creation. `list`, `dict`, `set`, `bytearray`, and any user class instance with mutable attrs.
- **Immutable:** cannot change after creation; any "change" creates a new object. `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`, `bool`, `complex`.

```python
l = [1, 2]; l.append(3)   # mutates in place, same object
s = "ab"; s2 = s + "c"    # new string object created
```

**Why it matters (interview gold):**
- Immutable objects can be used as **dict keys / set members** (hashable).
- Immutable objects are safe to share across threads/copies.
- **Gotcha:** a tuple's *contents* can be mutable — `t = ([1], 2); t[0].append(3)` works! Only the tuple's references are fixed.
- Mutable objects are passed by reference → functions can modify them (see Q8).
- Python "variables" are actually **names bound to objects** — reassignment rebinds the name; it never mutates.

---

## Q7: Which Python types are immutable?

`int`, `float`, `complex`, `str`, `tuple`, `frozenset`, `bytes`, `bool`, `NoneType`, `range`, and `Ellipsis`/`NotImplemented` singletons.

- `int`/`str` are immutable — that's why `x += 1` creates a new int and rebinds `x`.
- `tuple` is immutable but may *contain* mutable objects.
- `frozenset` is the immutable sibling of `set`.
- `bytes` is the immutable sibling of `bytearray`.
- Fun nuance: even `str` methods never mutate — `s.upper()` returns a new string.

---

## Q8: What happens when you pass a mutable object to a function?

**Pass-by-object-reference** (a.k.a. "pass by assignment", not pass-by-value and not strict pass-by-reference).

- The *reference* (pointer) to the object is copied into the parameter; both caller and callee refer to **the same object**.
- Mutating the object **inside** the function **is visible** to the caller.
- **Reassigning** the parameter inside the function only rebinds the local name — **not visible** to the caller.

```python
def mutate(l):
    l.append(3)      # visible outside
def rebind(l):
    l = [99]         # NOT visible outside — only local rebinding
def no_mutate(x):
    x = x + 1        # int is immutable → new object, local only
```

**Implications:**
- Use this deliberately (return in-place changes) or defensively — copy inputs if you must not mutate them.
- This is why **mutable default arguments** are dangerous (see Q21).
- For immutable types, passing to a function behaves like pass-by-value (new object created on any change).

---

## Q9: What is shallow copy vs deep copy?

- **Shallow copy** — copies the outer object but shares the **same inner references**.
  - `l.copy()`, `list(l)`, `dict.copy()`, `copy.copy(x)`.
- **Deep copy** — recursively copies everything; inner objects are new.
  - `copy.deepcopy(x)`.

```python
import copy
l = [[1, 2], [3, 4]]
s = l.copy()          # new outer list, SAME inner lists
d = copy.deepcopy(l)  # new outer AND new inner lists
s[0].append(99)       # l[0] now also [1,2,99]  (shared)
d[0].append(99)       # l unaffected
```

**Gotchas:**
- Deepcopy can fail/be slow on recursive structures, singletons, or objects holding locks/connections; it may invoke `__deepcopy__`/`__reduce__` and can be overridden.
- Deepcopy of a module or a lock raises errors — you often want shallow copies for those.
- Slicing `l[:]` and `list(l)` are shallow copies too.

---

## Q10: How do you copy a Python object?

| Technique | Kind | Use |
|---|---|---|
| `obj.copy()` / `list(obj)` / `dict(obj)` / `set(obj)` | shallow | built-in containers |
| `obj[:]` (slice) | shallow | lists |
| `copy.copy(x)` | shallow | generic |
| `copy.deepcopy(x)` | deep | nested structures |
| `constructor(iterable)` | shallow | e.g., `list(other_list)` |
| `copy.copy`/`deepcopy` with `__copy__`/`__deepcopy__` overrides | custom | classes with special needs |

- For immutable types copying is trivial (may return the same object — e.g., `(1,2)[:] is (1,2)` → True).
- For your own classes, implement `__copy__`/`__deepcopy__` when default behavior is wrong (e.g., deep-copying a connection).
- Numpy arrays: `.copy()` is deep by default (note: `np.array(a)` is NOT a copy for arrays).

---

## Q11: What are list comprehensions?

A compact way to build a list by transforming/filtering an iterable in one expression.

```python
squares = [x**2 for x in range(10)]            # [0,1,4,...81]
evens   = [x for x in range(20) if x % 2 == 0] # with filter
nested  = [c for row in matrix for c in row]   # flatten (order = nesting)
```

- Readability: `[expr for item in iterable if cond]`.
- Usually **faster** than `for`-loop + `.append()` because the loop runs in C without repeated method lookups and list resizes are amortized.
- Can have multiple `for` clauses and multiple `if`s; avoid more than ~2 levels for readability.

---

## Q12: What are dictionary comprehensions?

Same idea, producing a dict: `{key_expr: value_expr for item in iterable if cond}`.

```python
squares = {x: x**2 for x in range(5)}          # {0:0, 1:1, 2:4, ...}
even_str = {x: str(x) for x in range(10) if x % 2 == 0}
```

- Keys are deduplicated (later wins).
- Use to transform/map an existing dict: `{k: v*2 for k, v in d.items() if v > 0}`.

---

## Q13: What are set comprehensions?

`{expr for item in iterable if cond}` — note braces, but no colon → a set.

```python
{x % 5 for x in range(20)}   # {0, 1, 2, 3, 4} — duplicates removed, unordered
```

- Same comprehension mechanics; result is a `set` (dedup, O(1) membership).
- For an immutable variant, wrap in `frozenset(...)`.

---

## Q14: What is the difference between a list comprehension and a generator expression?

| | **List comprehension** | **Generator expression** |
|---|---|---|
| Syntax | `[...]` | `(...)` |
| Produces | Materialized list (eager) | Lazy iterator (one item at a time) |
| Memory | Full list in RAM | O(1) — items produced on demand |
| Speed | Faster for small/single-pass | Slightly slower per item, huge savings at scale |
| Reusable | Yes (list) | One-shot (iterator exhausted) |
| Best for | Need random access / reuse / length | Large or infinite streams |

```python
lc = [x*2 for x in range(10)]   # eager list
ge = (x*2 for x in range(10))   # lazy generator (adds ~1 byte for 1M vs 8MB list)
```

**Interview angle (micro1 cares about this):** "Which should you use for a 10M-row dataset?" → generator, then stream it; a list would blow memory. `sum(x*x for x in range(10**9))` works with a generator but kills RAM with a list.

---

## Q15: What does `enumerate()` do?

Pairs each item with its index, returning an iterable of `(index, value)` tuples.

```python
for i, v in enumerate(fruits):          # enumerate(fruits, start=0)
    print(i, v)
```

- Pass `start` to change the starting index: `enumerate(fruits, 1)`.
- Avoids manual counter bookkeeping and is more readable/idiomatic.
- Note it's lazy — wrap with `list()` to materialize.

---

## Q16: What does `zip()` do?

Pairs elements from multiple iterables positionally into tuples, **stopping at the shortest** iterable.

```python
names = ["a", "b", "c"]; scores = [90, 80, 70]
list(zip(names, scores))        # [('a',90), ('b',80), ('c',70)]

for n, s in zip(names, scores): ...
```

- `zip(*pairs)` **unzips** (transpose): `list(zip(*[('a',90),('b',80)]))`.
- **Strictness (Py3.10+):** `zip(..., strict=True)` raises `ValueError` if lengths differ — good for catching data bugs.
- Lazy: returns an iterator.
- Use `itertools.zip_longest` to pair up to the longest iterable (fills with fillvalue).

---

## Q17: What is the difference between `sort()` and `sorted()`?

- `list.sort()` — **in-place** on a list, returns `None`, faster (no copy), only works on lists.
- `sorted(iterable)` — returns a **new sorted list**, works on any iterable (tuple, dict, generator, set), leaves the original unchanged.

```python
l.sort()                 # in-place
new = sorted(l)          # new list
sorted(d.items(), key=lambda kv: kv[1])   # sort dict by value
```

- Both accept `key=` (callable) and `reverse=`.
- `key=str.lower`, `key=lambda x: x[1]` etc. Key is computed **once per element** (decorate-sort-undecorate), so it's efficient even for expensive key functions.

---

## Q18: What are `*args` and `**kwargs`?

- `*args` collects **extra positional** arguments into a tuple.
- `**kwargs` collects **extra keyword** arguments into a dict.

```python
def f(*args, **kwargs):
    print(args, kwargs)
f(1, 2, x=3)   # (1, 2) {'x': 3}
```

- Used for wrapper/decorator signatures that forward arbitrary args.
- Also used for **unpacking** in calls: `f(*lst)` and `f(**dct)` spread a sequence/dict into arguments.
- Order matters: `def f(a, *args, b=1, **kwargs)` — positional-only/pos-or-kw, then `*args`, then keyword-only after `*`.
- The names `args`/`kwargs` are convention only.
- `*` alone enforces keyword-only args: `def f(a, *, b)` → `b` must be passed by keyword.

---

## Q19: What are positional and keyword arguments?

- **Positional:** matched by order — `f(1, 2)`.
- **Keyword:** matched by name — `f(a=1, b=2)`.
- A single argument can be called either way *unless* restricted.

```python
def f(a, b, /, c, *, d):   # a,b positional-only; c positional-or-keyword; d keyword-only
```

- **Positional-only (`/`):** cannot be passed by keyword. Used for order-sensitive params and to allow param-name changes.
- **Keyword-only (`*`):** must be passed by name — improves readability and safety (e.g., flags).
- Order in a call: positional first, then keyword; keywords can be in any order.
- Can't pass the same parameter twice (e.g., `f(1, a=1)` → TypeError).

---

## Q20: What are default arguments in Python?

Parameters given a default value, evaluated **once at function definition time**; callable without them.

```python
def connect(host="localhost", port=5432, timeout=5): ...
```

- Rules: parameters with defaults must come after those without (except keyword-only).
- **Critical nuance:** defaults are evaluated **at definition time** — which is why mutable defaults are dangerous (Q21).
- Common use: optional config, flags, callbacks; use `None` sentinel when you need a runtime default or want to distinguish "not passed".

---

## Q21: What problem can mutable default arguments cause?

The default is **created once at definition time and shared** across all calls → state leaks between calls.

```python
def add_item(item, lst=[]):   # BAD
    lst.append(item)
    return lst

add_item(1)   # [1]
add_item(2)   # [1, 2]  ← previous call's data leaks in!
```

**Why:** the default list object is one object stored on the function; every call that doesn't pass `lst` uses that same list.

**Fix (idiomatic):** use `None` and create inside the function.

```python
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

**Also dangerous as defaults:** `{}`, `set()`, mutable class instances. Safe defaults: `None`, numbers, strings, tuples, frozensets.

---

## Q22: What is variable scope in Python?

Scope defines where a name is visible. Python has four nested scopes (see LEGB, Q23): local, enclosing (closure), global/module, and built-in. Assignment binds a name in the **current** scope unless declared otherwise.

```python
x = 10            # global
def f():
    x = 20        # NEW local x (shadowing) — not the global!
    return x
```

- Reading a name searches LEGB outward.
- To mutate a global from inside: `global x`. To mutate an enclosing nonlocal: `nonlocal x`.
- Scope is decided at **compile time** (a variable is local to a function if assigned anywhere in it) — this can surprise: referencing a global *before* assigning it locally raises `UnboundLocalError`.
- Class bodies create their own scope but **do not** nest for methods (methods are functions with their own local scope).
- `del` removes a name; comprehension variables (Py3) are scoped to the comprehension, not the outer scope.

---

## Q23: Explain the LEGB rule.

Name lookup order in Python:

1. **L — Local:** current function/body locals.
2. **E — Enclosing:** enclosing functions' locals (closures) — innermost outward.
3. **G — Global:** module-level names.
4. **B — Built-in:** `builtins` (`len`, `print`, `range`, ...).

```python
x = "global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"     # shadows enclosing & global
        return x        # L → "local"
    return inner
```

**Nuances:**
- If `inner` only *read* `x` (no assignment), it finds the enclosing value.
- Assignment inside `inner` without `nonlocal` creates a **new local** (doesn't modify enclosing).
- `nonlocal x` lets an inner function rebind an enclosing function's variable; `global x` rebinds a module variable.

---

## Q24: What is a lambda function?

An anonymous single-expression function defined inline with `lambda args: expression`.

```python
add = lambda a, b: a + b
sorted(pairs, key=lambda p: p[1])
```

- Limited to a **single expression** (no statements, no assignment, no `return`).
- Most useful as a throwaway for `key=`, `map`/`filter`, `sorted`.
- Readability rule: if the logic is complex or reused, use a named `def` instead.
- Lambdas can still have defaults (`lambda x, y=2: x+y`) and be immediately invoked `(lambda x: x*2)(5)` (rarely worth it).

---

## Q25: What are first-class functions in Python?

Functions are **first-class citizens**: they are objects — you can assign them, pass them as arguments, return them from functions, and store them in data structures.

```python
def square(x): return x * x
f = square           # assign
funcs = [square, abs]  # store
apply = lambda fn, x: fn(x)
apply(square, 5)     # pass as argument → 25
```

**Why it matters:** this is the foundation of higher-order functions, decorators, `map`/`filter`/`sorted(key=)`, and callback patterns.

---

## Q26: What is a higher-order function?

A function that **takes a function as an argument** and/or **returns a function**.

```python
def apply_twice(fn, x): return fn(fn(x))   # takes fn
def make_adder(n):                         # returns fn (closure)
    def adder(x): return x + n
    return adder
```

- Built-ins: `map`, `filter`, `sorted(key=)`, `functools.partial`, `functools.reduce`.
- Decorators (Q28) are the classic higher-order use-case (a function that takes a function and returns a wrapper).

---

## Q27: What is a closure?

A nested function that **captures free variables** from its enclosing scope, which remain accessible after the enclosing function returns.

```python
def counter():
    count = 0
    def inc():
        nonlocal count     # needed to rebind captured var
        count += 1
        return count
    return inc

c = counter(); c(); c()   # 1, 2 — `count` survives because inc closes over it
```

**Mechanics:** the cell holding `count` is kept alive by the returned function's closure (function object stores a reference to the cells). Without `nonlocal`, incrementing would create a local.

**Gotcha — late binding:** closures capture the **variable** (cell), not the value at creation.

```python
funcs = [lambda: i for i in range(3)]   # all return 2 (i is shared cell)
funcs = [lambda i=i: i for i in range(3)]  # fix: bind default at creation → 0,1,2
```

---

## Q28: What is a decorator?

A callable (usually a function) that **takes a function and returns a function**, adding behavior without changing the original source. Syntax sugar for `f = decorator(f)`.

```python
@timer            # equivalent to: my_func = timer(my_func)
def my_func(): ...
```

- Reusable cross-cutting concerns: logging, timing, auth/access checks, retries, caching, rate limiting, input validation.
- Applied bottom-up, executed top-down: `@a @b def f()` → `a(b(f))`.
- Can be parameterized (`@retry(times=3)`) via a factory: `@decorator(args)` returns the actual decorator.

---

## Q29: How do Python decorators work?

1. `@deco` applies `deco(func)` at **definition time** (module import).
2. `deco` returns a **wrapper** function that usually calls the original with `*args, **kwargs`.
3. The name `func` is rebound to the wrapper — so `func.__name__` is the wrapper's unless preserved.

```python
import functools, time
def timer(func):
    @functools.wraps(func)          # copies __name__, __doc__, __wrapped__ etc.
    def wrapper(*args, **kwargs):
        t = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            print(f"{func.__name__}: {time.perf_counter()-t:.4f}s")
    return wrapper
```

**Why `functools.wraps` matters:** keeps introspection correct (`help()`, logging, debugging), and `func.__wrapped__` enables wrapt-style unwrapping. Without it, signatures/metadata break.

---

## Q30: How would you create a custom decorator?

Give a concrete, production-style example — e.g., retry with delay:

```python
import functools, time, random

def retry(times=3, delay=1.0, backoff=2.0, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == times - 1:
                        raise
                    time.sleep(delay * (backoff ** attempt))
            # unreachable
        return wrapper
    return decorator

@retry(times=5, exceptions=(TimeoutError, ConnectionError))
def fetch(url): ...
```

Also mention a **class-based decorator** (callable instance with `__call__` and/or `__init__`) and **decorators with arguments** as the factory pattern above.

---

## Q31: What is duck typing?

"If it walks like a duck and quacks like a duck, it's a duck." Python relies on **behavior** rather than declared type: an object's suitability is decided by *which methods/attributes it has*, at runtime.

```python
def play(x):
    return x.play()   # works for any object with .play() — no isinstance needed

play(Dog()); play(Piano())  # both work if they have .play()
```

- Contrast with **nominal typing** (Java/C++: must declare/implements).
- Python's `len()` uses the `__len__` protocol; `for` loops need `__iter__`/`__next__`.
- **EAFP** (Easier to Ask Forgiveness than Permission — `try/except`) pairs with duck typing.
- **LBYL** (Look Before You Leap — check `hasattr`) is the alternative.
- `typing.Protocol` (Q539) lets you make duck typing explicit/static.

---

## Q32: What is the difference between an iterable and an iterator?

- **Iterable:** an object that can produce an iterator. Has `__iter__()` (or the old `__getitem__` sequence protocol). Lists, tuples, dicts, sets, strings, files, generators.
- **Iterator:** an object that produces values one at a time; has `__next__()` returning the next value or raising `StopIteration`, plus `__iter__()` returning itself.

```python
lst = [1, 2, 3]
it = iter(lst)        # lst.__iter__() → iterator
next(it)              # 1
next(it)              # 2
```

- **Key difference:** iterables are reusable; iterators are **one-shot** (exhausted after consumption).
- A list is iterable but not an iterator (`iter(lst)` gives the iterator).
- A generator is both an iterator and an iterable.

---

## Q33: What does `yield` do?

Pauses a function, yielding a value to the caller, and **preserves state** so execution resumes right after `yield` on the next `next()` call. Any function containing `yield` becomes a **generator function**.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1
```

- Calling a generator function **does not run** it — it returns a generator object; execution happens on iteration.
- `yield` is the basis of generators (Q34), generator expressions, and coroutine-like pipelines.
- A generator can also **receive values** via `gen.send(value)` (the value becomes the result of the `yield` expression), used in more advanced coroutine patterns.

---

## Q34: What is a generator?

A lazy iterator produced by a generator function (`yield`) or a generator expression. Values are produced **on demand** rather than materialized.

```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b          # infinite generator — never materializes

g = fib(); next(g)  # 0; next(g)  # 1; ...
```

- Single-use, forward-only, can be infinite.
- `yield from gen` delegates to a sub-generator (flattening/splicing).
- `return value` inside a generator sets `StopIteration.value`.
- Combined with `send()`, `throw()`, `close()` for cooperative pipelining.
- In the async world: **async generators** (`async def` with `yield`) and `async for`.

---

## Q35: Why are generators memory efficient?

Because they compute **one item at a time** — never storing the whole sequence.

- A list of 10M ints: ~80 MB+ (list pointers + int objects).
- A generator producing 10M ints: **constant** memory (frame + current values), ~a few hundred bytes.

```python
total = sum(i for i in range(10**7))   # generator: O(1) memory
total = sum([i for i in range(10**7)]) # list: O(n) memory spike
```

- Memory is freed progressively; items can be **infinite** (streams, sensor data, log files).
- This is the standard answer for "how would you process a file too big for RAM?" — stream it line-by-line with a generator.

---

## Q36: What is the difference between `yield` and `return`?

- `return` — exits the function, optionally with a value; caller gets the value immediately. State is gone.
- `yield` — produces a value but **suspends** the function; caller resumes it later. State is preserved.

```python
def a(): return [1, 2, 3]      # eager — whole list at call time
def b():
    for x in [1, 2, 3]: yield x  # lazy — one at a time on iteration
```

- A function with any `yield` is a generator; `return` (with value) inside it just ends iteration.
- `yield` → lazy/memory-efficient/one-shot; `return` → eager/full materialization/reusable result.
- You can use both in one generator: `yield` during iteration, `return` to signal completion.

---

## Q37: What are Python context managers?

Objects (or generator-based functions) that manage **setup/cleanup** around a block of code — guaranteeing release even on exceptions. They define `__enter__`/`__exit__` (or are created with `@contextmanager`).

```python
with open("f.txt") as f:      # __enter__ → f; __exit__ → closes even on error
    data = f.read()
```

- Classic uses: files, DB connections/sessions (commit/rollback), locks, transactions, network clients, temp dirs.
- `__exit__(exc_type, exc, tb)` returning `True` **suppresses** the exception (rare — don't swallow exceptions silently).
- `contextlib.contextmanager` converts a generator with a single `yield` into a context manager.
- `contextlib.ExitStack` dynamically combines an arbitrary number of context managers.
- `contextlib.suppress`, `contextlib.redirect_stdout` are handy helpers.

---

## Q38: What does the `with` statement do?

It is syntax for the **context manager protocol**:

1. Evaluates the expression → calls `obj.__enter__()`.
2. Binds `__enter__`'s return to the `as` target (if given).
3. Runs the suite.
4. In `finally`-like fashion calls `obj.__exit__(...)`, **always** — on normal exit, `return`/`break`, and exceptions.
5. If the suite raised, `__exit__` receives the exception info; if it returns truthy, the exception is swallowed.

```python
# equivalent of `with open(...) as f:`:
f = open(...).__enter__()  # concept only
try:
    pass
finally:
    f.__exit__(None, None, None)
```

Multiple managers: `with A() as a, B() as b:` (enter A then B; exit B then A — reverse order). Parentheses allow line breaks.

---

## Q39: What are magic/dunder methods?

Special methods with double-underscore names (`__init__`, `__len__`, `__eq__`, `__str__`) that Python calls **implicitly** to implement language operations. They are the hooks that let your objects integrate with Python syntax and built-ins.

```python
class Money:
    def __init__(self, amount): self.amount = amount
    def __add__(self, other):   return Money(self.amount + other.amount)
    def __eq__(self, other):    return self.amount == other.amount
    def __hash__(self):         return hash(self.amount)
    def __repr__(self):         return f"Money({self.amount})"
```

- **Lifecycle:** `__new__`, `__init__`, `__del__`.
- **Operators:** `__add__`, `__mul__`, `__eq__`, `__lt__`, `__contains__`, `__getitem__`, `__call__`.
- **Representation:** `__str__` (user-facing), `__repr__` (developer-facing).
- **Context:** `__enter__`, `__exit__`.
- **Attribute access:** `__getattr__`, `__setattr__`, `__getattribute__`.
- **Descriptor:** `__get__`, `__set__`, `__delete__`.
- **Serialization:** `__reduce__`, `__getstate__`/`__setstate__`.
- Naming convention: avoid inventing your own dunders (reserved names); use single-underscore conventions instead.

---

## Q40: What is the difference between `__str__` and `__repr__`?

- `__repr__` — **developer-facing**; unambiguous; used by `repr()`, the REPL, and inside f-string `!r`. Convention: aim to reconstruct the object (`eval(repr(x)) == x`) and show the class name + key fields.
- `__str__` — **user-facing**; readable; used by `str()`, `print()`, f-strings (default `!s`). Falls back to `__repr__` if not defined.

```python
class Point:
    def __repr__(self): return f"Point({self.x}, {self.y})"   # unambiguous
    def __str__(self):  return f"({self.x}, {self.y})"        # pretty

p = Point(1, 2)
print(p)      # (1, 2)     → __str__
repr(p)       # Point(1, 2) → __repr__
f"{p!r}"      # Point(1, 2)
```

- Containers call `__repr__` of elements when printing the container.
- Rule of thumb: always implement `__repr__` (debugging); implement `__str__` when there's a nicer user-facing form.
