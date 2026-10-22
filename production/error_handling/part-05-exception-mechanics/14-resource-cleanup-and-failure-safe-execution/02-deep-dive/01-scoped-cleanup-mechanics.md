# Scoped Cleanup Mechanics

> Part V · Chapter 14 · Sections 14.1–14.4 (mechanics) · _Estimated reading time: 20 min_
> **Prerequisite:** [Acquire/Release and Guaranteed Cleanup](../01-concepts/01-acquire-release-and-guaranteed-cleanup.md)

## In one sentence

`try/finally`, `using` / try-with-resources, `defer`, and context managers all implement the same
guarantee — **release at scope exit, including during unwinding** — but differ in ordering,
exception handling, and when they *don't* run.

## Why this matters in production

Knowing exactly when cleanup runs (and when it does not) prevents two opposite bugs: believing a
resource is released when it was not (leak), and releasing a resource twice (error). The mechanics
also determine error ordering: whether the body error or the cleanup error wins, and how both are
preserved. This file is the reference for that behavior.

## Core concept

All four mechanisms are **scope-managed cleanup**: acquire, register release, and the runtime
guarantees release when the scope ends.

| Mechanism | Registration | Order | Runs on hard exit? | Cleanup throw behavior |
| --------- | ------------ | ----- | ------------------ | ---------------------- |
| `try/finally` | `finally` block | Last-in, one block | No (`os.Exit`/`SIGKILL`) | Replaces body error |
| `using`/try-with-resources | resource declaration | Reverse (LIFO) | No | Attached as suppressed |
| `defer` (Go) | `defer` statement | LIFO | Not on `os.Exit`/`log.Fatal` | Runs; if it panics, that panic wins |
| Context manager (`with`) | `__enter__`/`__exit__` | LIFO (nested `with`) | No | `__exit__` result decides |

The **ordering** is the crucial detail: modern scoped mechanisms release in **reverse order of
acquisition** (LIFO), which mirrors the stack of resources.

## How it works (mechanics)

### `try/finally`

```text
enter try
  ├─ normal end    ─▶ finally ─▶ done
  └─ throw E       ─▶ finally ─▶ if finally throws F: F replaces E  (⚠ unless suppressed)
                                 else: E resumes unwinding
```

`finally` runs even on `return`, `break`, `continue`.

### try-with-resources (Java)

```java
try (A a = openA(); B b = openB()) {
    body();
} // b.close() then a.close() — reverse order
```

If `body()` throws and `b.close()` throws, `b`'s exception is **suppressed by** the body exception.
If only close throws, that exception propagates.

### `defer` (Go)

```go
a := openA()
defer a.Close()   // runs 2nd (LIFO)
b := openB()
defer b.Close()   // runs 1st
body()
```

`defer` runs on panic (during unwinding). It does **not** run if the process exits via `os.Exit`,
`log.Fatal`, or a `SIGKILL`.

### Context managers (Python)

```python
with open_a() as a, open_b() as b:   # __exit__ called in reverse
    body()
```

`__exit__(exc_type, exc, tb)` can suppress an exception by returning truthy — **usually wrong for
cleanup**, because it converts a failure into a success. Use it deliberately, if ever.

### The "acquire before try" rule

```ts
// ❌ acquire inside try: if acquire throws, finally releases an unacquired resource
try {
  const c = await pool.acquire();
  work();
} finally {
  c.release();   // ReferenceError if acquire threw
}

// ✅ acquire before try
const c = await pool.acquire();
try {
  work(c);
} finally {
  c.release();
}
```

Some languages (`using`, try-with-resources) put acquisition inside the construct safely because
they track whether acquisition succeeded.

## Worked example — resource ordering and error preservation

Java try-with-resources correctly handles a failing close:

```java
class Conn implements AutoCloseable {
    public void work() { throw new PrimaryException("work failed"); }
    public void close() { throw new CloseException("close failed"); }
}

try (Conn c = new Conn()) {
    c.work();                       // PrimaryException
}
// Result: PrimaryException propagates;
//         CloseException is in primary.getSuppressed()
```

Equivalent in Go, where you must preserve ordering yourself:

```go
func run() (err error) {
    a := openA()
    defer a.Close()

    b := openB()
    defer func() {
        if cerr := b.Close(); cerr != nil && err == nil {
            err = fmt.Errorf("close b: %w", cerr)   // only if body succeeded
        } else if cerr != nil {
            err = errors.Join(err, fmt.Errorf("close b: %w", cerr)) // body failed: attach
        }
    }()

    return body()               // named return lets defers inspect/attach
}
```

The named return `err` lets deferred cleanup add its failure *without discarding* the body error.

## Before/after — the same function

```text
BEFORE (manual)                      AFTER (scoped)
────────────────                     ──────────────
c = acquire()                        c = acquire()
work(c)                              try { work(c) }
# throw here → c leaked              finally { release(c) }
release(c)                           # released on every path
```

## Key data / numbers

- **Java try-with-resources**: close exceptions are suppressed by the primary, per the language
  spec (JLS 14.20.3).
- **Go**: `defer` is LIFO; runs on panic but not `os.Exit`; a deferred function can recover a panic.
- **Python `with`**: `__exit__` returning a truthy value suppresses the exception; default is
  `False` (do not suppress).
- **Node**: `try/finally` is the only synchronous guarantee; explicit resource management
  (`using`) is a newer stage-3 feature — verify your runtime's support before relying on it.

## Real-world use case — Acme SaaS

Acme migrated a data-access helper from manual acquire/release to Go `defer`. They initially
registered `defer conn.Release()` but kept releasing again at the end of the function, causing a
double release that panicked in the pool under load. Understanding that `defer` already covers the
normal path (and that release must be idempotent) removed the duplicate. The same review found a
`defer` placed *after* a possible `os.Exit` call, which never ran — moved earlier.

## Trade-offs

| Mechanism | Pros | Cons | When |
| --------- | ---- | ---- | ---- |
| `try/finally` | Universal | Manual ordering; overrides primary | Simple single resource |
| try-with-resources / `using` | Safe ordering + suppression | Needs an interface | Resource classes |
| `defer` | Concise; panic-safe | Not on hard exit; ordering subtle | Go |
| Context manager | Explicit `__exit__` semantics | Truthy can suppress | Python |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Acquire before the try where required | Acquire inside `try` then release in `finally` |
| Rely on LIFO for nested resources | Release in acquisition order |
| Use `using` to get suppression for free | Hand-roll close handling |
| Trust `defer` on panic | Trust `defer` after `os.Exit`/`log.Fatal` |
| Make release idempotent | Release twice |

## Common mistakes

- **Acquire inside `try`** — `finally` releases something never acquired.
- **Double release** — manual release plus `defer`/`using`.
- **Expecting `defer` after `os.Exit`** — it never runs.
- **`__exit__` returning truthy** — suppresses a real failure.
- **Manual close handling** when the language would suppress correctly for you.

## Checklist

- [ ] Acquire precedes the cleanup scope.
- [ ] Release ordering is LIFO for nested resources.
- [ ] No double release.
- [ ] Cleanup runs on panic (where the language allows).
- [ ] No reliance on cleanup after a hard process exit.

## Related

- [Acquire/Release and Guaranteed Cleanup](../01-concepts/01-acquire-release-and-guaranteed-cleanup.md)
- [Primary vs Secondary Errors](./02-primary-vs-secondary-errors.md)
- [try/finally and using Patterns](../03-practical-examples/01-try-finally-and-using-patterns.md)
- [Language-Level Error Semantics (Part XVIII)](../../../part-18-languages-and-frameworks/47-language-level-error-semantics/README.md)
