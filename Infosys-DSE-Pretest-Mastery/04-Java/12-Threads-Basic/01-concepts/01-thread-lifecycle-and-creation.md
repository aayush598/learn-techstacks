# Thread Lifecycle and Creation

> Section 4 · Java · Threads Basics · _Estimated reading time: 12 min_
> **Prerequisite:** none

## In one sentence

A thread is a **separate path of execution**; `start()` launches a new thread, `run()` does not —
and that single distinction is the root of most thread questions.

## Why the pre-test tests this

- Section 4 thread questions always come in the same shape: **two threads printing something**.
- The correct answer is almost always the statement that is **guaranteed** — because the
  interleaving is **not** deterministic.
- "What is the difference between `start()` and `run()`?" and "Which of these is thread-safe?" are
  standard 4-option questions.

## Core concept

### Two ways to create a thread

```java
// 1. Extend Thread
class MyThread extends Thread {
    public void run() { System.out.println("in run"); }
}
new MyThread().start();

// 2. Implement Runnable  (preferred)
class MyTask implements Runnable {
    public void run() { System.out.println("in run"); }
}
new Thread(new MyTask()).start();
```

| Aspect | `extends Thread` | `implements Runnable` |
|---|---|---|
| Java's "single inheritance" | ❌ uses up your one superclass | ✅ leaves `extends` free |
| Task vs worker separated | ❌ | ✅ — the task can be shared |
| Return a value / throw a checked exception | ❌ | ❌ (`Runnable` cannot; use `Callable`) |
| Preferred in interviews | | ✅ |

**A lambda works because `Runnable` is a functional interface:**

```java
new Thread(() -> System.out.println("hello")).start();
```

### `start()` vs `run()` — the core distinction

| Call | What happens | New thread? |
|---|---|---|
| `t.start()` | the JVM creates a new thread and that thread calls `t.run()` | ✅ |
| `t.run()` | the **current** thread calls `run()` as a plain method call | ❌ |

```java
Thread t = new Thread(() -> System.out.println(Thread.currentThread().getName()));
t.run();      // prints "main"  — no new thread
t.start();    // prints "Thread-0" — a new thread
```

Calling `start()` **twice** on the same `Thread` object throws `IllegalThreadStateException`. A
`Thread` can only be started once.

### The thread lifecycle

The `Thread.State` enum has exactly six values:

| State | Meaning | How a thread gets here |
|---|---|---|
| `NEW` | created but `start()` not yet called | `new Thread(...)` |
| `RUNNABLE` | executing (or eligible to run) | after `start()` |
| `BLOCKED` | waiting to enter a `synchronized` monitor | another thread holds the lock |
| `WAITING` | waiting indefinitely for another thread | `wait()`, `join()`, `park()` |
| `TIMED_WAITING` | waiting for a bounded time | `sleep(ms)`, `wait(ms)`, `join(ms)` |
| `TERMINATED` | `run()` has finished | normal end or an uncaught exception |

```java
Thread t = new Thread(() -> { });
System.out.println(t.getState());   // NEW
t.start();
t.join();                            // wait for it to finish
System.out.println(t.getState());   // TERMINATED
```

> ⚠️ `RUNNABLE` in Java means "running **or** eligible to run". A thread waiting for CPU is still
> `RUNNABLE`, not a separate state.

### Useful `Thread` methods

| Method | What it does | Throws |
|---|---|---|
| `start()` | launch the thread; may be called once | `IllegalThreadStateException` if already started |
| `run()` | the task body; called by the thread | — |
| `join()` | block until this thread finishes | `InterruptedException` |
| `join(ms)` | block for at most `ms` milliseconds | `InterruptedException` |
| `sleep(ms)` | pause the **current** thread | `InterruptedException` |
| `yield()` | a *hint* that the thread is willing to give up the CPU | — |
| `interrupt()` | request that a thread stop; sets the interrupt flag | — |
| `isInterrupted()` | read the flag **without** clearing it | — |
| `Thread.interrupted()` | read **and clear** the current thread's flag | — |
| `setDaemon(boolean)` | mark the thread as a daemon | `IllegalThreadStateException` if already started |
| `isDaemon()` | is it a daemon? | — |
| `setPriority(int)` | a **hint**; not guaranteed by the JVM | `IllegalArgumentException` if out of range |
| `getName()` / `setName(String)` | the thread name (default `Thread-0`, `Thread-1`, …) | — |
| `Thread.currentThread()` | the running thread | — |
| `getState()` | the `Thread.State` | — |

### Daemon threads

| Fact | Detail |
|---|---|
| Definition | a thread whose lifetime is bound to its creator |
| When it dies | when the **last non-daemon** thread finishes |
| Example | the JVM's garbage collector, the auto-save thread in an IDE |
| Set it | `t.setDaemon(true)` — **before** `start()` |

```java
Thread t = new Thread(() -> {
    while (true) {
        try { Thread.sleep(100); } catch (InterruptedException e) { break; }
    }
});
t.setDaemon(true);
t.start();
// the program exits when main finishes, even though t is still looping
```

### Interruption

```java
t.interrupt();          // ask t to stop
```

| Situation | Result |
|---|---|
| The target is in `sleep()`, `wait()`, or `join()` | it throws `InterruptedException` **and clears the flag** |
| The target is running normal code | the flag is set; the target must check it itself |

```java
while (!Thread.currentThread().isInterrupted()) {
    // do work
}
```

**Two flag-reading methods, one difference:**

| Call | Clears the flag? |
|---|---|
| `Thread.currentThread().isInterrupted()` | ❌ no |
| `Thread.interrupted()` | ✅ yes (static — always the **current** thread) |

### Priority

```java
t.setPriority(Thread.MAX_PRIORITY);   // 10
```

| Constant | Value |
|---|---|
| `MIN_PRIORITY` | 1 |
| `NORM_PRIORITY` | 5 |
| `MAX_PRIORITY` | 10 |

**Priority is only a hint.** The JVM may ignore it entirely — the specification does not promise
that a higher-priority thread runs first. Never build an exam answer on priority ordering.

### `Callable` and `Future`

```java
Callable<Integer> task = () -> { Thread.sleep(100); return 42; };
ExecutorService pool = Executors.newSingleThreadExecutor();
Future<Integer> f = pool.submit(task);
Integer result = f.get();     // blocks until the task finishes
pool.shutdown();
```

| Aspect | `Runnable` | `Callable<V>` |
|---|---|---|
| Return value | ❌ | ✅ |
| Throw a checked exception | ❌ | ✅ |
| Submitted via | `execute(r)` or `submit(r)` | `submit(c)` |

`Future.get()` throws `InterruptedException` and `ExecutionException` (which wraps the task's
exception).

## Worked example

**Q. What is printed?**

```java
public class Main {
    static class T extends Thread {
        public void run() {
            System.out.println(Thread.currentThread().getName());
        }
    }
    public static void main(String[] args) throws Exception {
        T t1 = new T();
        T t2 = new T();
        System.out.println("start");
        t1.start();
        t2.start();
        t1.join();
        t2.join();
        System.out.println("end");
    }
}
```

**Solution**

| Fact | Consequence |
|---|---|
| `t1.start()` and `t2.start()` launch threads named `Thread-0` and `Thread-1` | the two `run()` bodies race — **their relative order is not guaranteed** |
| `join()` blocks until the thread has finished | after both joins, both `run()` bodies are **done** |
| `println` to `System.out` is synchronised internally | each line appears whole, never interleaved mid-line |

**Guaranteed facts**

| # | Statement | Guaranteed? |
|---|---|---|
| 1 | `start` is printed first | ✅ yes — it is printed before the threads are started |
| 2 | `end` is printed last | ✅ yes — `join()` guarantees both threads finished first |
| 3 | `Thread-0` is printed before `Thread-1` | ❌ **no** — the scheduling is not deterministic |
| 4 | Exactly **three** lines are printed | ✅ yes — `start`, two thread lines, `end` |
| 5 | The two thread lines may appear in either order | ✅ yes |

**The answer to a "what is the output?" MCQ must be one of the guaranteed statements.** Anything
that depends on the order of `Thread-0` and `Thread-1` is a bad question with a bad answer — if
you see such an option, it is the *wrong* option.

## Quick rules

- `start()` → new thread; `run()` → same thread.
- A `Thread` can be started only once → `IllegalThreadStateException` otherwise.
- `Thread.State` = NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.
- `sleep()`/`wait()`/`join()` all throw `InterruptedException`.
- `sleep()` is **static** — it pauses the current thread.
- `join()` is the only reliable way to say "wait for that thread".
- Daemon threads die when the last non-daemon thread finishes.
- `isInterrupted()` does not clear the flag; `Thread.interrupted()` does.
- Priority is a hint, never a guarantee.
- Thread output order is **not** deterministic — pick the guaranteed statement.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| `t.run()` starts a thread | it does | Only `start()` does |
| `Thread-0` always prints before `Thread-1` | that order | Not guaranteed |
| `sleep()` pauses *that* thread | the other thread | It pauses the **current** thread |
| `Thread.State` has 7 values | 7 | It has 6 |
| Priority decides the order | higher priority first | A hint only |

## Checklist

- [ ] I can explain `start()` vs `run()` in one sentence.
- [ ] I can list the six `Thread.State` values.
- [ ] I know which methods throw `InterruptedException`.
- [ ] I know the daemon-thread rule.
- [ ] I know why a thread-order question has no single answer.

## Related

- [Synchronization and Race Conditions](02-synchronization-and-race-conditions.md)
- [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)
- [Solved threads set](../03-worked-examples/01-solved-threads-set.md)
- [Thread traps](../04-pitfalls/01-thread-traps.md)
- [Threads one-pager](../05-reference/01-threads-one-pager.md)
- [Topic overview](../README.md)
