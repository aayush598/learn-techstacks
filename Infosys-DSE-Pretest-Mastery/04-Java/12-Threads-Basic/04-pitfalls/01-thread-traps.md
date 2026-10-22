# Threads Basics — Traps

> Section 4 · Java · Threads Basics · _Estimated reading time: 12 min_
> **Prerequisite:** [Solved threads set](../03-worked-examples/01-solved-threads-set.md)

## In one sentence

12 traps, each written as **the wrong answer you will pick → the right answer → the one-line
guard**.

## Why the pre-test tests this

Thread traps are unusually dangerous because the wrong answer is *usually* the one that "looks
right" to a programmer's intuition. Lock in the guards and the thread section is safe.

## Core concept

### The 12 traps

| # | Trap | The wrong answer you pick | The right answer | The one-line guard |
|---|---|---|---|---|
| 1 | `t.run()` starts a new thread | a new thread starts | Only `t.start()` does | "`run()` = a plain method call" |
| 2 | `start()` order fixes the run order | `Thread-0` always first | Not guaranteed | "Scheduling is the JVM's choice" |
| 3 | Priority decides who runs first | the higher priority runs first | Priority is a **hint** only | "No ordering guarantee" |
| 4 | `volatile` makes `count++` atomic | it is thread-safe | Visibility only | "Use `AtomicInteger`" |
| 5 | `sleep()` releases the lock | it releases | It **keeps** the lock | "`wait()` releases" |
| 6 | `wait()` outside `synchronized` hangs | it hangs | `IllegalMonitorStateException` | "You must hold the monitor" |
| 7 | `notify()` wakes the thread you want | that thread | An **arbitrary** waiter | "Use `notifyAll()`" |
| 8 | `if` is fine around `wait()` | `if` | `while` — spurious wakeups | "Always `while`" |
| 9 | Daemon threads keep the JVM alive | the program waits | They are killed on exit | "Last non-daemon thread" |
| 10 | `static synchronized` and instance `synchronized` exclude each other | they do | Different monitors | "One lock per object" |
| 11 | `join()` leaves the thread `RUNNABLE` | `RUNNABLE` | `TERMINATED` | "Finished = terminated" |
| 12 | `ArrayList`/`HashMap` are safe to share | they are | They are not | "Use `ConcurrentHashMap`" |

### The output-order trap — the most important one

```java
t1.start();
t2.start();
```

**Never** write an answer that depends on whether `t1` or `t2` runs first. The only defensible
answers are:

| Statement | Guaranteed? |
|---|---|
| Both threads complete before the following `join()` calls return | ✅ |
| The number of printed lines is fixed | ✅ |
| `t1` printed before `t2` | ❌ |
| `t2` printed before `t1` | ❌ |
| A higher-priority thread prints first | ❌ |

**The exam's correct option will be the one that says "the order is not deterministic"** (or the
option listing the statements that are guaranteed). If you see an option with a fixed order, it is
the distractor.

### `sleep()` vs `wait()` — the four differences

| | `sleep()` | `wait()` |
|---|---|---|
| Owner | `Thread` (static) | `Object` (instance) |
| Releases the lock | ❌ | ✅ |
| Needs the monitor | ❌ | ✅ |
| Spurious wakeups | ❌ | ✅ → use `while` |
| Woken by | time passing | `notify()` / `notifyAll()` |

### The volatile trap

```java
volatile int count = 0;
count++;          // ❌ still racy
```

| Mechanism | Gives visibility | Gives atomicity of `count++` |
|---|---|---|
| `volatile` | ✅ | ❌ |
| `synchronized` | ✅ | ✅ |
| `AtomicInteger` | ✅ | ✅ |
| `LongAdder` | ✅ | ✅ (for counting) |

**The pattern to remember:** `volatile` is for **flags** ("should I keep running?"), not for
**counters**.

### The lock-identity trap

```java
class C {
    synchronized void a() { }              // locks `this`
    static synchronized void b() { }        // locks C.class
    void c() { synchronized (this) { } }    // locks `this`
}
```

`a()` and `c()` exclude each other. `b()` does **not** exclude them — it uses a different monitor.

### The `wait()`/`notify()` rules — all four

1. Must hold the monitor of the object you call them on.
2. Otherwise → `IllegalMonitorStateException`.
3. `wait()` releases the monitor; `notify()` does not.
4. Always use a `while` loop, because spurious wakeups happen.

### The interrupted flag

| Call | Reads the flag | Clears the flag |
|---|---|---|
| `Thread.currentThread().isInterrupted()` | ✅ | ❌ |
| `Thread.interrupted()` | ✅ | ✅ (static — the current thread only) |
| `interrupt()` on another thread | sets it | ❌ |
| `sleep()`/`wait()`/`join()` throwing `InterruptedException` | — | ✅ the exception clears it |

## Worked example

**The trap in action.** A question says:

> ```java
> synchronized (lock) {
>     while (!ready) {
>         lock.wait();
>     }
>     consume();
> }
> ```
> Which is true?
> Options: (a) `wait()` keeps the lock, (b) `wait()` releases the lock and `notify()` must be called under the same lock, (c) `wait()` may throw `IllegalMonitorStateException` if the lock is not held, (d) `wait()` can wake up spuriously.

**The trap:** you pick (a) because the code is inside `synchronized` — "of course it keeps the
lock".

**The right reasoning:**

| Option | Verdict |
|---|---|
| (a) | ❌ `wait()` **releases** the monitor — that is the whole point of it |
| (b) | ✅ `wait()` releases the lock, and `notify()` must be called while holding the same monitor |
| (c) | ✅ if you call `wait()` without holding that monitor, it throws `IllegalMonitorStateException` |
| (d) | ✅ spurious wakeups are possible, which is exactly why the code uses `while` |

**Answers: (b), (c) and (d).** Only (a) is wrong.

## Quick rules

- `start()` → new thread; `run()` → current thread.
- Output order between threads is **never** guaranteed.
- `sleep()` keeps the lock; `wait()` releases it.
- `wait()`/`notify()` need the monitor → `IllegalMonitorStateException` otherwise.
- `volatile` = visibility, not atomicity.
- Daemon threads die with the last non-daemon thread.
- One lock per object; static and instance `synchronized` are different locks.
- `join()` returning means the thread is `TERMINATED`.
- `ArrayList`/`HashMap` are not thread-safe.

## Common traps

See the 12-row table above — each row is a one-line guard you can recite.

## Checklist

- [ ] I can answer any thread output question with the guaranteed statements only.
- [ ] I know the five differences in the `sleep()`/`wait()` table.
- [ ] I know the four `wait()`/`notify()` rules.
- [ ] I know which collections are thread-safe.
- [ ] I know the daemon and interruption rules.

## Related

- [Thread lifecycle and creation](../01-concepts/01-thread-lifecycle-and-creation.md)
- [Synchronization and race conditions](../01-concepts/02-synchronization-and-race-conditions.md)
- [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)
- [Solved threads set](../03-worked-examples/01-solved-threads-set.md)
- [Threads one-pager](../05-reference/01-threads-one-pager.md)
- [Topic overview](../README.md)
