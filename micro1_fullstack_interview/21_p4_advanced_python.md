# Priority 4 — Advanced Python (Q529–Q548)

**Why these matter for micro1:** lower priority but they probe real depth — the AI interviewer digs past "I use Python." Expect GIL, memory, metaclasses, descriptors, slots, pickling, ABCs, and performance internals.

---

## Q529: What is the GIL? How does it affect Python programs?

**GIL (Global Interpreter Lock):** a mutex in CPython that allows **only one thread to execute Python bytecode at a time**, even on multi-core CPUs.

**Why it exists:** CPython's memory management (refcounting, Q533) isn't thread-safe; the GIL makes every object operation safe by serializing bytecode execution.

**Effects:**
- **CPU-bound** work in threads → no speedup (threads take turns) → use **multiprocessing** or async.
- **I/O-bound** work in threads → threads *release* the GIL during I/O waits (socket, file, DB, HTTP) → threading *does* help (Q100).
- **C extensions** (NumPy, cryptography, uvloop) can release the GIL during heavy C work → real parallelism.

**Current status (impress them):** Python 3.13 added **free-threaded builds** (no GIL, `PYTHON_GIL=0`, experimental); the GIL is still default. Also the GIL is released for 5ms intervals (time-slicing), and around I/O and C calls.

---

## Q530: How does Python manage memory?

**Layers:**
1. **Private heap** — all objects live in CPython's heap.
2. **Allocator hierarchy:** `PyMem` (raw) → `PyObject` allocator (object-level) → **pymalloc** (small-object pools ≤ 512 bytes, fast reuse) → system `malloc`. Small objects are allocated from pre-allocated memory *arenas* to avoid frequent syscalls.
3. **Object lifecycle:** allocation → refcount hits 0 → `__del__`/deallocation → memory returned to the pool (small objects stay in pools; big ones returned to OS).

**You can't easily see it as a user — but awareness matters for:**
- Creating millions of small objects (per-request dicts) is cheap-ish due to pools but still GC pressure.
- **Weakrefs, slots, pools, `gc.collect`** are your levers (Q536, Q542).
- Tools: `tracemalloc` (allocation traces), `sys.getsizeof`, memory_profiler, `resource`.

---

## Q531: What's the difference between `==`, `is`, and `is not`?

- **`==`** — **value equality**: uses `__eq__` (e.g., `[1,2] == [1,2]` → True).
- **`is`** — **identity**: is it the *same object*? (`x is y` checks `id(x) == id(y)`).
- **`is not`** — negated identity.

```python
a = [1, 2]; b = [1, 2]
a == b   # True  (values match)
a is b   # False (different objects)

x = 256; y = 256
x is y   # True — small ints (-5..256) are interned/cached singletons!

s = "hi"; t = "hi"
s is t   # often True — short strings may be interned (implementation detail)
```

**Rules:** use `is` for singletons — `None`, `True`, `False` (the PEP 8 standard); use `==` for everything else. Never rely on interning for `is` comparisons of values.

---

## Q532: What is `__eq__` and how does hashing relate?

- **`__eq__`** defines value equality (`==`). **`__hash__`** defines behavior in sets/dict keys.
- **The invariant:** if `a == b`, then `hash(a) == hash(b)` — *equal objects must have equal hashes*.
- **Rule:** if you define `__eq__`, you should define `__hash__` (or set `__hash__ = None` to make it unhashable). Default: `__eq__` sets `__hash__` to None implicitly.

```python
class Candidate:
    def __init__(self, email, name):
        self.email, self.name = email, name
    def __eq__(self, other):
        return isinstance(other, Candidate) and self.email == other.email
    def __hash__(self):
        return hash(self.email)   # hash by the same field used in __eq__
```

**Dict lookup:** Python computes `hash(key)`, finds the bucket, then confirms with `==` — so a bad hash (e.g., hashing on a mutable field) breaks lookups or causes collisions → O(n) buckets. Don't put mutable objects in sets/dict keys.

---

## Q533: How does reference counting and garbage collection work?

**Reference counting:** each object has `ob_refcnt`; incremented on new reference, decremented on drop; at 0 → deallocated immediately. **Limitation:** doesn't handle **reference cycles** (`a.b = b; b.a = a`) — refcounts never reach 0.

**Cyclic garbage collector (GC):** a separate, generational collector detects cycles:
- **Generations (0, 1, 2):** new objects start in gen 0; survivors promote. Collecting young generations frequently (cheap), old rarely (expensive) → most objects die young.
- Triggers: allocation thresholds (`gc.get_threshold()` ≈ 700/10/10 per allocation count).
- In CPython **3.12+**: the GC is **generational with reference counting**... plus **3.13 added a multi-threaded parallel GC** for free-threaded builds.

**Your levers:** `gc.disable()` to speed up short-lived scripts (dangerous — cycles leak), `gc.collect()` before measuring memory, `weakref` to break cycles. Also: `__del__` + cycles = memory leak (the object can't be collected cleanly).

---

## Q534: What is `weakref`? When would you use it?

**`weakref`** — a reference that **doesn't keep the object alive**. When all strong references die, the object is collected and the weakref returns `None`.

```python
import weakref
class Cache: pass
c = Cache()
ref = weakref.ref(c)
del c
assert ref() is None      # object was collected
```

**Use cases:**
- **Caches** (object identity cache / LRU by weakref) — cached objects can be collected when not used elsewhere (Q250/Q251).
- **Breaking reference cycles** — parent→child strong, child→parent weak (common in trees, object graphs).
- **Event listeners / observers** — don't keep dead subscribers alive.
- `weakref.WeakValueDictionary` — value-keyed auto-cleaning dicts.

**Limits:** not all types are weakref-able (built-ins like `list`, `dict` aren't by default; subclasses are).

---

## Q535: What are decorators? How do they work internally?

**Decorators = functions that take a function and return a (usually wrapped) function.** `@decorator` is syntactic sugar for `f = decorator(f)`.

```python
def log_calls(fn):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} took {time.perf_counter()-start:.3f}s")
        return result
    return wrapper

@log_calls                 # fetch_candidate = log_calls(fetch_candidate)
def fetch_candidate(id): ...
```

**Key subtleties:**
- **Preserve metadata:** `functools.wraps(fn)` copies `__name__`, `__doc__`, `__dict__` (otherwise the stack trace shows `wrapper`, and docs break).
- **Decorators with arguments** = a function returning a decorator: `@retry(times=3)` → `retry(times=3)` returns the decorator.
- **Class-based decorators:** implement `__call__`.
- **Order matters:** `@a @b f` = `a(b(f))` — bottom-up application.
- **In FastAPI:** dependencies (Q60) fill a similar role — and FastAPI routes are decorated functions; keep decorated handlers thin.

---

## Q536: What is `__slots__` and when do you use it?

**`__slots__`** — declare fixed instance attributes; replaces the per-instance `__dict__` with a compact descriptor-based layout.

```python
class Candidate:
    __slots__ = ("email", "name")     # no __dict__ per instance
    def __init__(self, email, name):
        self.email, self.name = email, name
```

**Benefits:**
- **Memory:** each instance saves the dict (~100+ bytes) → significant when you hold millions of objects (parsed resume rows, match results).
- **Faster** attribute access (fixed descriptors).

**Costs/limits:**
- No arbitrary new attributes (`c.x = 1` → `AttributeError`).
- No `__dict__` unless you add it to slots explicitly.
- Slower `pickle` (needs `__getstate__`/`__setstate__`) and weakref (add `__weakref__` to slots).
- Inheritance: slots don't apply to a child unless the child declares its own.

**Rule:** use for hot, data-only classes at scale — but profile first; the win is memory, not always speed.

---

## Q537: What is the difference between a classmethod, staticmethod, and instance method?

```python
class DB:
    pool = None
    def __init__(self, dsn):            # instance method — bound to self
        self.dsn = dsn
    @classmethod
    def connect(cls, dsn):              # classmethod — bound to the CLASS
        return cls(dsn)
    @staticmethod
    def sanitize(sql):                  # staticmethod — no self/cls, pure helper
        return sql.replace(";", "")
```

- **Instance method:** gets `self`; operates on instance state.
- **`@classmethod`:** gets `cls` (the class, or subclass); works on class state, factory methods; **polymorphic** — called on a subclass, `cls` is that subclass (key difference from staticmethod).
- **`@staticmethod`:** gets neither; a namespaced free function; no access to class or instance state.

**Interview answer:** "classmethod gets the class and respects inheritance — perfect for factories; staticmethod is just a namespaced helper; instance methods carry state."

---

## Q538: What is `__new__` vs `__init__`?

- **`__new__`** — **creates** the instance (first; returns an object). Used for immutable types and singleton/instance control. Implicitly `__new__(cls, ...)`.
- **`__init__`** — **initializes** the created instance (sets state). Returns nothing.

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Rules:**
- If `__new__` returns an instance of `cls`, Python calls `__init__` on it; if it returns a *different* type or object, `__init__` is skipped.
- Override `__new__` rarely — singletons, immutable subclasses (tuple/int), and when you must control allocation. Prefer a module-level instance or class attribute over a singleton when possible (testability).

---

## Q539: What are metaclasses? When would you use one?

**A metaclass is the class of a class** — by default `type`. `class A: pass` → `type(A) is type`. Metaclasses control **how classes themselves are created** (intercept `__new__`/`__init__` at class-definition time).

```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kw):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kw)
        return cls._instances[cls]

class Config(metaclass=SingletonMeta): ...
```

**Real uses (rare — reach for them sparingly):**
- ORMs/dataclasses: auto-generate attributes/`__init__`/validation from declarations (Pydantic v1's `ModelMetaclass`; SQLAlchemy declarative base).
- Registries: collect all subclasses of a marked class automatically.
- Frameworks: class-level hooks, adding methods/properties at definition.

**Why they're a "depth" question:** the interviewer wants to know you understand class creation, not that you use metaclasses daily. Correct answer: "metaclass = a class whose instances are classes; I'd use one for a framework-level registry or auto-generation, but rarely in application code."

---

## Q540: What are Abstract Base Classes (ABCs)? Why use them?

**ABCs** define an interface that subclasses must implement — enforced at instantiation.

```python
from abc import ABC, abstractmethod

class Parser(ABC):
    @abstractmethod
    def parse(self, text: str) -> dict: ...

class PdfParser(Parser):
    def parse(self, text): ...     # must implement, else can't instantiate

# Parser()  → TypeError: Can't instantiate abstract class
```

**Benefits:**
- Enforce a contract → a `MatchEngine` can depend on any `Parser` safely.
- Document intent; static tools (mypy) catch missing methods.
- `@abstractmethod` + `@classmethod`/`@staticmethod` combos for class-level contracts.
- `isinstance` checks against the ABC work with `__subclasshook__` (duck-typing-friendly).

**Interview angle:** contrast with **duck typing** — Python is dynamically typed, so ABCs are *optional* contracts: "protocols" (PEP 544 / `typing.Protocol`) are the structural alternative — `Protocol` doesn't require inheritance, just structure.

---

## Q541: What is the difference between `__str__` and `__repr__`?

- **`__repr__`** — unambiguous, developer-facing; should (ideally) let you *reconstruct* the object: `Candidate(email='a@b.co')`. Used by `repr()`, and by **`str()` fallback** and containers (`print([obj])` shows repr).
- **`__str__`** — readable, user-facing. Used by `str()` and `print()`.

```python
def __repr__(self):
    return f"Candidate(email={self.email!r})"   # unambiguous
def __str__(self):
    return f"Candidate: {self.name} <{self.email}>"  # human
```

**Golden rule:** always define `__repr__` (default is useless `<Candidate object at 0x...>`); define `__str__` only when humans will print it. If only `__repr__` exists, it's used for both.

---

## Q542: How do you make Python code faster? (memory/perf profiling)

**Process: measure first — `profile`, don't guess:**

1. **Profile CPU:** `cProfile -m cProfile app.py`, then `pstats`; find the top-3 hot functions; in production use **py-spy** (no code changes).
2. **Profile memory:** `tracemalloc` (allocations), `memory_profiler`, `objgraph` for leaks.
3. **Then optimize the actual hotspot:**
   - Replace Python loops with **vectorized/lib calls** (NumPy, `map`, comprehensions).
   - Use the **right data structures** (set membership vs list scan, dicts) (Q3).
   - **Batch I/O** — fewer round trips to DB/network (Q112, Q250).
   - **Cache** repeated results (functools.lru_cache, Redis) (Q432).
   - **Async** for I/O-bound work; **multiprocessing** for CPU-bound (Q100).
   - Move hot logic into **C-extension/Cython/Rust** only if truly needed.
   - Avoid per-iteration allocations (`__slots__`, Q536).

**Answer:** "I profile first and optimize the top 1–2 hotspots; premature optimization without profiling is the classic mistake."

---

## Q543: What are context managers? How do you write one?

**Context managers** encapsulate setup/teardown via `with` — guaranteed cleanup even on exceptions.

```python
@contextlib.contextmanager
def db_transaction(conn):
    try:
        conn.begin()
        yield conn                  # the with-block runs here
        conn.commit()
    except Exception:
        conn.rollback()             # cleanup on failure
        raise

with db_transaction(conn) as tx:    # finally guaranteed
    tx.execute(...)
```

**Two ways to write one:**
1. Class with `__enter__` / `__exit__(exc_type, exc_val, tb)` — `__exit__` returning True swallows the exception.
2. **`@contextlib.contextmanager`** generator with `yield` — cleaner for most cases.

**Built-ins:** `open()`, locks (`threading.Lock`), `transaction.atomic()` (Django), SQLAlchemy `session.begin()`, `asyncio.timeout()`.

**Why interviewers ask:** ownership of resources — DB connections, file handles, locks — is what separates real backend code from toy code.

---

## Q544: How does `pickle` work, and why is it dangerous?

**`pickle`** serializes arbitrary Python objects to bytes and back — *including executable code paths*: unpickling runs `__reduce__` on attacker-controlled classes, so **unpickling untrusted data = remote code execution**.

```python
import pickle
data = pickle.dumps(obj)     # → bytes
obj = pickle.loads(data)     # arbitrary code if data is malicious
```

**Danger:** never `pickle.loads` anything from users, the network, or unverified sources. This is a classic security question (OWASP A08, unsafe deserialization).

**Safer alternatives:**
- **JSON** — safe, universal, but limited to JSON types.
- **MessagePack / protobuf** — compact, cross-language.
- For caches/queues: use JSON (or typed serialization) — and if you must pass objects around, use a **whitelist of classes** or a custom `__reduce__` guard.

**Gotcha for your stack:** Redis and SQS payloads are often pickled by default in some libs — prefer JSON with Pydantic models on both ends.

---

## Q545: What are generators and iterators? How do they differ?

- **Iterator:** an object with `__iter__` + `__next__` — produces a stream of values.
- **Generator:** an *iterator factory* written with `yield` — lazy, one value at a time, no list materialized.

```python
def read_lines(path):                    # generator — lazy
    with open(path) as f:
        for line in f:
            yield line.strip()

lines = read_lines("big.txt")            # nothing read yet
first = next(lines)                      # reads until first yield
```

**Key properties:**
- **Lazy** — values produced on demand → memory O(1) for huge streams (parsing 500 MB resumes).
- **Single-use** — can't rewind; `list(gen)` consumes it.
- **`send`/`throw`/`close`** — generators are also coroutines (the async machinery is generator-based under the hood in older Python; native coroutines in 3.5+).
- `yield from` / `yield` in async generators (`async for`).
- **Generators vs list comprehension** memory difference: `[x for x in r]` vs `(x for x in r)`.

---

## Q546: What are `functools` tools you use daily?

- **`lru_cache`** — memoize pure functions (`@lru_cache(maxsize=128)`) — cache repeated computations (regex compiles, parsing lookups, expensive pure math) (Q432).
- **`partial`** — pre-bind arguments: `send_email = partial(notify, channel="email")`.
- **`wraps`** — preserve metadata in decorators (Q535).
- **`cached_property`** — compute once per instance, cache on the instance.
- **`reduce`** — fold a sequence (rarely needed; prefer comprehensions).
- **`singledispatch`** — runtime overload by type: `@singledispatch def score(x): ...` then `@score.register(Resume)`.

**Interview angle:** `lru_cache` + `functools.wraps` are the ones they probe — know their limits (lru_cache keys must be hashable; don't cache impure functions).

---

## Q547: What are dataclasses? When would you prefer them over dicts or namedtuples?

**`@dataclass`** — auto-generates `__init__`, `__repr__`, `__eq__`, and optionally ordering/frozen/hash.

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)             # immutable + hashable
class MatchResult:
    candidate_id: str
    score: float
    reasons: list[str] = field(default_factory=list)
```

**vs namedtuple:** namedtuple is immutable and tuple-based (fast, unpackable, but can't add methods/defaults easily, awkward field defaults via `__new__`). Dataclass is mutable by default, has types + defaults + factories, and is much more ergonomic.

**vs dict:** dicts are flexible but untyped — no autocomplete, no validation, silent typos (`d["candidte_id"]`). Dataclass + `__post_init__`/validation gives structure and safety.

**vs Pydantic:** dataclasses don't validate/coerce — Pydantic models do (used in FastAPI). Use Pydantic for API boundaries, dataclasses for internal value objects where you want lightweight structure.

**When to use:** DTOs, value objects, internal config, immutable results. **Frozen** for hashable values (dict keys, sets, cache keys).

---

## Q548: What is the difference between `typing` / type hints and how do they get enforced?

- **Type hints** are **metadata** — Python ignores them at runtime (they don't slow or constrain anything). Tools enforce them:
  - **mypy / pyright / pytype** — static analysis: catch wrong argument types, missing returns, `Optional` handling before runtime.
  - **Pydantic** — *runtime* validation: coerces and checks types on data boundaries (FastAPI request/response, Q46).
- **`Optional[X]`** = `X | None`; **`Union[X, Y]`** = `X | Y`; **`list[int]`**, **`dict[str, Any]`**, **`Callable[..., R]`**, **`Literal["a","b"]`**, **`TypedDict`** (dict with a shape), **`Protocol`** (structural typing, Q540).
- **`Any`** — escape hatch, defeats checking; use `Unknown`/`object` where possible.
- **Generics:** `TypeVar("T")` + `Generic[T]` for reusable containers (Q589).

**Interview answer:** "Type hints are checked by static tools (mypy), not the interpreter; FastAPI/Pydantic gives me runtime validation at boundaries; I use mypy in CI so type errors fail the build."
