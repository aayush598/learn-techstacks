# Priority 5 — Deep Internals (Q636–Q655)

**Why these matter for micro1:** the deepest tier — bytecode, GC internals, ASGI/WSGI, Uvicorn/Gunicorn workers. Only fully prepared candidates answer these well; they're differentiators.

---

## Q636: What is Python bytecode? How does Python run your code?

**Pipeline:** source → **parse** (AST) → **compile** → **bytecode** → executed by the **CPython virtual machine**.

```text
my.py ──parse──▶ AST ──compile──▶ bytecode (.pyc) ──interpreter (VM)──▶ result
```

- **Bytecode** = a stack-machine instruction set (e.g., `LOAD_FAST`, `BINARY_OP`, `CALL`, `RETURN_VALUE`), stored in `__pycache__/*.pyc` for speed (skips recompile if source unchanged).
- Inspect with `dis.dis(fn)`. The **VM** executes instructions against an evaluation stack and frames (locals, globals, call stack).
- The GIL (Q529) serializes bytecode execution across threads — thread switches happen between instructions (time-sliced).
- **.pyc caching:** timestamp+size check (and content hash in newer versions); you can `import py_compile`/`compileall` to precompile for fast cold starts (relevant for Lambda, Q609).

**Interview answer:** "Python compiles source to stack-based bytecode cached in `.pyc`; the CPython VM executes it instruction by instruction under the GIL — `dis` lets me inspect it for micro-optimizations or debugging weird behavior."

---

## Q637: What is the difference between CPython, PyPy, and Cython?

- **CPython** — the reference implementation (C). Compiles to bytecode, runs on its VM. Most compatible, most common.
- **PyPy** — a **JIT-compiling** Python implementation (RPython). Warms up then runs hot loops much faster than CPython. Downsides: different memory behavior, C-extension (CPython ABI) compatibility issues, slower startup. Best for long-running CPU-heavy Python.
- **Cython** — a **superset/compiler**: Python-ish code compiles to C (with static types → C structs/loops) → huge speedups while keeping Python syntax. Use for hot inner loops that need C speed (e.g., custom scoring kernels) without writing C by hand.

**Answer:** "CPython is the default interpreter; PyPy is a JIT implementation for CPU-heavy workloads; Cython compiles typed Python to C for hot paths — I'd reach for Cython or a C extension only when profiling shows Python is the bottleneck (Q542)."

---

## Q638: How does Python handle function calls at the C level? (Frame/stack)

**Every Python call creates a **frame**:** a stack structure holding the code object, locals, globals, closures, and a `return` slot. Frames live on the call stack (each ~1 KB+).

- `sys._getframe(0)` accesses the current frame; tracebacks walk frames.
- **Deep recursion → `RecursionError`** — the C stack + Python frames grow; default recursion limit ~1000 (and ~3000 in debug builds) — because each Python frame uses real C stack.
- **Generators/coroutines** freeze their frame (locals + state) in a heap object — that's how they resume later (Q545, and the async machinery).
- Frame overhead is why millions of small function calls are slower than inlined/batched code (Q542).

**Interview angle:** "a frame is the runtime record of a call — locals, state, code object — and coroutines keep theirs suspended in memory, which is exactly how async/await and generators work."

---

## Q639: What is `__call__` and how does it relate to callable objects?

- **`__call__`** makes an instance **callable** like a function: `obj(...)` → `type(obj).__call__(obj, ...)`.

```python
class Retry:
    def __init__(self, times=3): self.times = times
    def __call__(self, fn):
        # decorator logic using self.times
        ...
retry3 = Retry(3)
@retry3           # retry3(...) works because of __call__
def fetch(): ...
```

**Uses:**
- Class-based decorators that need configuration/state (Q535).
- **Callable objects with state** — counters, memoized dispatchers, "function factories".
- Functions *are* objects with `__call__`; `callable(x)` checks for it.
- Classes are callable too — `Class(...)` calls `__new__` + `__init__` (Q538).

**Pitfall:** implement `__call__` but forget `functools.wraps`-style metadata when used as a decorator.

---

## Q640: How does the CPython GIL actually get released?

**The GIL is released around operations that block, so other threads make progress:**

1. **I/O** — socket/DB/file read/write: the `selectors`/asyncio loop, `socket.recv`, DB drivers release the GIL during the syscall wait.
2. **C functions that release it explicitly** — many C extensions release the GIL for heavy work: `time.sleep`, most of `ssl`, `hashlib` (for large data), `NumPy` ops, `zlib`, `re` (on big strings), `io` buffering, `subprocess`.
3. **Time-slicing** — the default switch interval (5ms) — the interpreter periodically releases the GIL so other threads can run even without I/O.
4. **Multiprocessing** bypasses the GIL entirely (separate processes, own GILs).

**Consequence:** a pure-Python CPU loop in 8 threads ≈ 1 core of throughput (Q529); an I/O-bound workload gets near-linear thread scaling (Q100). **3.13 free-threaded builds** remove the GIL (experimental) — parallelism without the switch overhead.

---

## Q641: What happens on `import`? (Import system internals)

1. **`sys.modules` lookup** — if the module name is already imported, return the cached module (idempotent).
2. **Find** — `sys.meta_path` finders: built-in → frozen → **path finders** (`PathFinder` scanning `sys.path`, trying `__init__.py` for packages).
3. **Load** — the loader reads source, **compiles to bytecode**, checks/creates `.pyc`.
4. **Execute** — the module's code runs in a fresh module namespace (`__name__`, `__file__`, etc.), registering it in `sys.modules` *before* executing (handles circular imports partially).
5. **Bind** — `import x.y` binds `x` in the local namespace; `from x import y` imports and binds `y`.

**Gotchas:** circular imports work only if one side imports the other at *function* level, not module level (import order matters — `sys.modules` has the partially-executed module). `__all__` controls `from x import *`. `sys.path` order matters (the classic "why is it importing the wrong module" bug — PYTHONPATH, cwd).

---

## Q642: What is the `sys` module? `os` module? When do you use them?

- **`sys`** — Python *interpreter* runtime: `sys.path` (import search path), `sys.argv` (CLI args), `sys.exit()`, `sys.getrecursionlimit`/`setrecursionlimit`, `sys.getsizeof` (object size), `sys.setprofile`/`settrace` (profiling), `sys.stdout/stderr`, `sys.modules`, `sys.platform`/`sys.version`.
- **`os`** — *operating system* interface: `os.getenv`/`os.environ` (env), `os.path` (path utils) / `pathlib` (preferred), `os.makedirs`, `os.listdir`, `os.remove`, `os.chdir`, `os.name`/`os.uname`, subprocess helpers (`os.system` — prefer `subprocess`), file descriptors (`os.open` low-level).

**Interview answer:** "`sys` is Python-runtime state and interpreter settings; `os` is OS-level operations. `sys.path` for imports, `sys.argv` for CLI; `os.environ` for config; I prefer `pathlib` over `os.path` for paths and `subprocess` over `os.system`."

---

## Q643: What is `subprocess` and when would you use it?

**`subprocess`** runs external processes safely and with full control:

```python
import subprocess
r = subprocess.run(["pdfinfo", file], capture_output=True, text=True, timeout=10, check=False)
print(r.returncode, r.stdout, r.stderr)

# capture output safely without shell injection:
with subprocess.Popen(["pandoc", src, "-t", "json"], stdout=subprocess.PIPE) as p:
    data = p.communicate(timeout=30)[0]
```

**Key practices:**
- **Never `shell=True` with string interpolation** — command injection (Q401-adjacent). Pass a list; let Python do the quoting.
- `timeout=` to bound runaway processes; handle `TimeoutExpired` (kill + cleanup).
- `check=True` raises on non-zero exit — or check `returncode` explicitly.
- Streams: `capture_output` vs piping; handle deadlocks with `communicate()` (avoid writing to stdin/reading stdout with plain `PIPE` without draining).

**Your app:** resume conversion (pdftotext, pandoc), OCR tools, image processing — the classic "shell out to a tool" need.

---

## Q644: What is the difference between `await` and `asyncio.run` at the engine level?

- **`asyncio.run(coro)`** — the *entry point*: creates a new **event loop**, runs the coroutine to completion, closes the loop. Only callable from synchronous code, once per program (can't be nested).
- **`await`** — inside a coroutine, *yields control* to the loop, scheduling the awaited task; it can only appear inside an `async def`.

**At the engine level:** `await x` compiles to `YIELD_FROM`-style semantics — the current coroutine suspends (its frame saved, Q638), the loop regains control and runs other ready tasks; when `x`'s future completes, the loop reschedules the waiter.

```text
asyncio.run(main())            # create loop → schedule main → pump loop
└─ await fetch_data()          # suspend main, run other tasks → resume when done
```

**Rules:** `await` outside async → SyntaxError; `asyncio.run` inside a running loop → RuntimeError (use `loop.create_task`/`await` instead). Gunicorn workers / pytest-asyncio / Jupyter each manage their own loop context (Q453).

---

## Q645: What is a Task in asyncio? Task vs Coroutine vs Future?

- **Coroutine** — an `async def` object; does *nothing* until awaited or scheduled. `await` resumes it.
- **Task** — wraps a coroutine and **schedules it on the loop** (`asyncio.create_task`): it runs *concurrently* with other tasks, independently of your `await` point. Has a lifecycle: pending → running → done/cancelled.
- **Future** — the low-level "result later" object (like a JS Promise). A Task *is* a Future subclass; `loop.create_future()` for advanced interop (asyncio.Semaphore/lock internals are future-based).

```python
t1 = asyncio.create_task(parse(cand1))     # scheduled, runs concurrently
t2 = asyncio.create_task(parse(cand2))
results = await asyncio.gather(t1, t2)     # wait for both
```

**Key rules:** a coroutine that's never awaited/created-as-task → **"coroutine was never awaited" warning + wasted work**. Tasks need a **reference** or they get garbage-collected mid-flight (classic bug). Cancel tasks with `task.cancel()`; use `asyncio.wait_for` for timeouts (Q104).

---

## Q646: What is an event loop? How does it dispatch events?

**Event loop** = the core scheduler of asyncio: a single thread that cycles between *ready* tasks and *I/O events*:

```text
loop forever:
    1. run tasks that are ready (scheduled, resumed)
    2. select()/epoll() — wait for I/O readiness (sockets, pipes, timers)
    3. when a socket is readable/writable → resume its waiter task
    4. run timers (timeouts, call_later) that have fired
```

- The loop uses an **I/O reactor** (`epoll` on Linux, kqueue on macOS — via `selectors`) to wait efficiently on many fds at once.
- Everything is cooperative: a task only yields at `await`. **Blocking calls (time.sleep, sync DB) block the WHOLE loop** (Q104).
- `loop.call_soon`, `call_later`, `run_in_executor` (offload blocking work to threads), `create_task`.
- **Alternatives:** `uvloop` — a Cython reimplementation of the loop protocol, ~2x faster for I/O-heavy workloads (FastAPI+uvicorn users often run uvloop).

**Answer:** "The loop multiplexes coroutines and I/O on one thread via epoll: it runs ready tasks, waits for socket/timer events, and resumes waiters — everything cooperates, so any blocking call freezes the whole loop."

---

## Q647: What is the ASGI/WSGI model? Why is FastAPI ASGI?

- **WSGI** (Web Server Gateway Interface) — the *sync* Python web interface: `application(environ, start_response)` → bytes. One request, one call, blocking. Standard for Django/Flask (older). Can't do WebSockets, streaming push, or async frameworks.
- **ASGI** (Asynchronous Server Gateway Interface) — `async def application(scope, receive, send)`. **Scope** = request metadata (type: http/websocket/lifespan); **receive** = async iterator of events; **send** = async send of response events.

```python
async def app(scope, receive, send):
    assert scope["type"] == "http"
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"hello"})
```

**Why ASGI:**
- **HTTP/2, WebSockets, SSE, streaming, lifespan** events (startup/shutdown) — all first-class.
- Async I/O concurrency (Q646) — thousands of concurrent connections per process.
- FastAPI is built on **Starlette** (an ASGI toolkit); frameworks, servers (uvicorn/daphne/hypercorn), and middlewares interoperate (Q648).

---

## Q648: What is Uvicorn? Gunicorn? Hypercorn? How do they relate?

- **Uvicorn** — a *fast ASGI server* (uvloop-backed). Serves the ASGI app directly. No process management; run one process or use it with workers (`--workers`).
- **Gunicorn** — a *WSGI process manager* (pre-fork workers). It does NOT speak ASGI natively — run it with the **`uvicorn` worker class**: `gunicorn -k uvicorn.workers.UvicornWorker` → Gunicorn manages the processes, Uvicorn serves ASGI inside each worker.
- **Hypercorn** — an ASGI server with **HTTP/2 + HTTP/3** and other protocols (best for those needs).

**Production pattern (what they're really asking):**
- **Gunicorn (`-k UvicornWorker`) as process manager + N workers** — one process per CPU core, each running a Uvicorn event loop → you get multi-process concurrency AND async within each process.
- Behind an **nginx/ALB** reverse proxy for TLS, static files, load balancing (Q431, Q602).
- Workers = processes (separate memory) → **no shared in-process cache** between workers; share state via Redis/DB (Q82). Worker count ≈ CPU cores; each worker's loop handles thousands of concurrent *I/O* requests but one CPU-bound request at a time (Q529).

---

## Q649: What is the difference between process, thread, and coroutine?

| | **Process** | **Thread** | **Coroutine** |
|---|---|---|---|
| Unit | OS process | OS thread | Cooperative function |
| Memory | Isolated (own GIL/refcounts) | **Shared** (GIL serializes CPU in Python) | Own frame/stack on the loop |
| Scheduling | OS | OS (preemptive) | **Cooperative** (yields at `await`) |
| CPU-bound | Parallel on multi-core | No (GIL, Q529) | No (single thread) |
| I/O-bound | Parallel | Yes (releases GIL on I/O) | Yes (async, single thread) |
| Cost | Highest | Medium | Lowest |
| Shared state | IPC (queues) | Locks/atomics | Task-safe within loop |

**Decision (Q100, Q430):** CPU-bound → **processes/multiprocessing**; I/O-bound with threads → **threading**; I/O-bound async → **asyncio/coroutines** (the natural FastAPI choice). Mixing is fine: run blocking work off the loop via `run_in_executor` (Q104).

---

## Q650: What is a "pre-fork" web server model?

**Pre-fork** (Gunicorn/uWSGI): the master process **forks N worker processes upfront** (before serving) — each worker is a fresh OS process that accepts connections independently.

**Why it works:**
- **Multi-core utilization** — N workers = N cores for CPU work (GIL per process, Q529).
- **Isolation** — a crashing worker doesn't take down the master or siblings; the master **spawns a replacement** (automatic restarts).
- **Memory sharing via copy-on-write** — forked workers share the loaded app code pages (faster boot, less RSS).

**Tradeoffs:** workers don't share in-memory state (Redis for shared state, Q82); worker count = tuning knob (too many → thrash, too few → underuse cores); needs graceful shutdown/reload for deploys (Q431 connection draining). This is *why* Gunicorn + UvicornWorker is the standard FastAPI prod setup (Q648).

---

## Q651: How does Django's ORM work vs SQLAlchemy? (One of the two ORMs)

**Django ORM (if asked, e.g., because they saw it on your resume):**
- **QuerySet** — lazy: `.filter()`/`.exclude()` build SQL lazily; evaluated on iteration/`.count()`/slicing. **Lazy + evaluated once** (querysets are *not* cached across accesses unless `.all()`).
- **Managers** — `Model.objects`; `objects.filter(...).values(...)` etc.
- **N+1:** Django auto-detects and raises `n_plus_one` warnings for loops hitting relations → use **`select_related`** (JOIN, for FK/OneToOne) and **`prefetch_related`** (separate query batched via IN, for M2M/reverse) (Q341, Q345).
- **Transactions:** `with transaction.atomic():` (nested = savepoints).
- **Migrations:** `makemigrations` + `migrate` (schema diffing).
- **Admin:** the auto-generated admin is a *feature* — recruiters can manage jobs/candidates without custom UI.

**Answer when asked "Django ORM vs SQLAlchemy":** "Django's ORM is model-centric with lazy QuerySets and batteries-included migrations; SQLAlchemy is more explicit — Core vs ORM, session lifecycle, greater control over queries, better async support. I'd pick Django for rapid CRUD apps with its admin/ecosystem; SQLAlchemy for complex queries, async, and fine control (and the micro1 stack uses it)."

---

## Q652: How does `requests` vs `httpx` work? What is connection pooling?

- **`requests`** — the classic sync HTTP client; uses `urllib3` underneath (which has connection pooling).
- **`httpx`** — modern: **sync AND async** (`httpx.Client` / `httpx.AsyncClient`), HTTP/2 support, event hooks, pluggable transports (the `MockTransport` used in tests, Q451), and mirrors `requests` API. **The right choice in an async FastAPI app** — never call a sync `requests` in an async handler (blocks the loop, Q646).
- **Connection pooling:** keep a client and **reuse connections** instead of opening a TCP/TLS handshake per request (Q112): `httpx.AsyncClient` reuses pooled connections across calls; timeouts set at client level.

```python
client = httpx.AsyncClient(timeout=httpx.Timeout(connect=2, read=30), limits=httpx.Limits(max_connections=50))
async with client.stream("POST", llm_url, json=payload) as r:  # streaming to the LLM
    async for chunk in r.aiter_bytes(): ...
```

**Interview answer:** "httpx is requests for the async world — same ergonomics, AsyncClient with connection pooling and streaming; critical so I never block the FastAPI event loop when calling the LLM (Q104, Q399)."

---

## Q653: What is a "coroutine" at the C level? How is `await` implemented?

**Implementation sketch:**
- A coroutine function returns a **coroutine object** wrapping a *suspended frame* (Q638). Nothing runs until scheduled.
- **`await`** compiles to a chain: the awaited object must be **awaitable** — `__await__()` (coroutines, tasks, futures, and any object with `__await__`).
- At `await x`: the caller's frame is suspended and linked to `x`'s future; execution returns to the **loop**. When `x` completes (its `__await__` returns a value, the future resolves), the loop **reschedules the caller** and execution resumes with the awaited value.
- **`yield` vs `await`:** `yield from` (generators) and `await` share the same suspension machinery — asyncio's coroutines historically *were* generators (`types.coroutine`); since 3.5 native coroutines are distinct types but use the same **`gen_send_ex`/`CALL` frame-suspension** core. `__await__` returns an iterator whose `__next__`/`send` drives progress — that's how `async for`/`async with` protocols hook in.

**Interview answer:** "await suspends the caller's frame and hands control to the loop, resuming when the awaited future completes — the same frame-suspension machinery Python uses for generators."

---

## Q654: What is a deadlock in asyncio? How do you avoid it?

**asyncio deadlock = code waits forever on a future/condition that can never resolve because the loop is stuck.**

Common forms:
- **Blocking call in the loop** — `time.sleep(5)` in a handler blocks the loop, so a task waiting on an I/O result never gets scheduled (Q646).
- **Waiting on yourself / circular awaits** — task A awaits task B which awaits A.
- **Lock held across await that nobody else can release** — `await lock.acquire()` while the holder is suspended on the same lock in the same loop (async lock: the acquirer never yields the loop... it does; but a lock acquired then the holder waits on the loop for something the waiter needs).
- **Missing cancellation handling** — `await task` where the task needs you to do something to proceed.
- **asyncio.Queue deadlock** — `await queue.get()` with no producer scheduled.

**Prevention:**
- **`asyncio.wait_for` on any long/untrusted await** (timeouts everywhere — Q104, Q398).
- **Never block** — offload sync work to `run_in_executor` (Q104).
- **Acquire locks at the end / hold them briefly**, use `async with` for release guarantees.
- Watch for **unawaited tasks** (started, forgotten → garbage-collected mid-work, Q645).
- Deadlock detection: `loop.set_debug(True)` / `faulthandler.dump_traceback_later()` to see who's stuck.

**Interview answer:** "async deadlocks come from blocked loops, circular awaits, or locks held across awaits that never yield to the waiter — timeouts on every await, no blocking calls, and debug hooks (`faulthandler`, loop debug mode) are my standard defenses."

---

## Q655: What is the difference between uvicorn workers and a process pool?

- **Uvicorn workers (via Gunicorn `-k UvicornWorker` or `--workers`)** — **processes**, each with its own event loop running the *same ASGI app*; the OS/load-balancer distributes connections. Concurrency across processes; each process handles many concurrent *I/O* requests via asyncio. Used for the **web serving tier** (Q648).
- **Process pool (`concurrent.futures.ProcessPoolExecutor` / multiprocessing Pool)** — a pool of worker *processes that execute individual CPU-bound tasks* (functions) and return results. Used for **CPU-heavy work inside an app** (heavy parsing, hashing, embedding computation).

| | Uvicorn workers | Process pool |
|---|---|---|
| Purpose | Serve web requests | Execute CPU tasks |
| Unit | Full ASGI app per process | Function call per worker |
| Channel | Network/LB | Futures/queues |
| When | Always in prod (Q648) | Only when profiling shows CPU-bound Python (Q542) |

**Answer:** "Uvicorn workers scale the *serving* tier as processes; a process pool offloads *CPU-bound work* from within the app — different problems, both solving the GIL by using multiple processes."
