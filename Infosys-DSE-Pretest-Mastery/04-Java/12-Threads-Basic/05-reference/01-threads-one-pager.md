# Threads Basics — One-Page Revision Sheet

> Section 4 · Java · Threads Basics · _Estimated reading time: 5 min_
> **Prerequisite:** [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)

## In one sentence

Print this page and threads collapse to **five tables**: question types, thread safety, exceptions,
`sleep()` vs `wait()`, and thread states.

## Why the pre-test tests this

Thread questions look scary and are actually very narrow. They are either "which is thread-safe?",
"which throws what?", or "which statement is guaranteed?". All three are table lookups.

## Core concept

### Table 1 — the question types

| Question type | How to answer |
|---|---|
| "What is printed?" | list only the **guaranteed** statements |
| "Which is thread-safe?" | Table 2 |
| "Which throws what?" | Table 3 |
| "What is the state?" | Table 5 |

### Table 2 — thread safety

| Choice | Safe? |
|---|---|
| `synchronized` | ✅ |
| `AtomicInteger` | ✅ |
| `ReentrantLock` | ✅ |
| `ConcurrentHashMap` | ✅ |
| `CopyOnWriteArrayList` | ✅ |
| `Collections.synchronizedMap(m)` | ✅ |
| `Vector` / `Hashtable` / `StringBuffer` | ✅ (legacy) |
| `volatile` field | ⚠ visibility only |
| `ArrayList` / `HashMap` / `HashSet` | ❌ |
| `StringBuilder` | ❌ |
| plain field / static field | ❌ |

### Table 3 — which method throws what

| Method | Throws |
|---|---|
| `Thread.sleep(ms)` | `InterruptedException` |
| `Object.wait()` | `InterruptedException` |
| `Thread.join()` | `InterruptedException` |
| `Object.notify()` / `notifyAll()` | `IllegalMonitorStateException` without the monitor |
| `Object.wait()` without the monitor | `IllegalMonitorStateException` |
| `start()` twice | `IllegalThreadStateException` |
| `setDaemon` after `start()` | `IllegalThreadStateException` |
| `setPriority(99)` | `IllegalArgumentException` |

### Table 4 — `sleep()` vs `wait()`

| | `sleep()` | `wait()` |
|---|---|---|
| Owner | `Thread` (static) | `Object` (instance) |
| Releases the lock | ❌ | ✅ |
| Needs the monitor | ❌ | ✅ |
| Spurious wakeups | ❌ | ✅ → use `while` |
| Woken by | time | `notify()` / `notifyAll()` |

### Table 5 — thread states

| State | Meaning |
|---|---|
| `NEW` | created, not started |
| `RUNNABLE` | running or eligible to run |
| `BLOCKED` | waiting to enter a monitor |
| `WAITING` | `wait()`, `join()`, `park()` |
| `TIMED_WAITING` | `sleep(ms)`, `wait(ms)`, `join(ms)` |
| `TERMINATED` | `run()` returned |

### Table 6 — the guaranteed-statement checklist

| Statement | Guaranteed? |
|---|---|
| Printed before `start()` | ✅ |
| Printed after `join()` returns | ✅ |
| The number of printed lines | ✅ |
| The relative order of two threads' output | ❌ |
| A higher-priority thread runs first | ❌ |
| `System.out.println` output is split mid-line | ❌ (whole lines only) |

### 60-second budget

| Phase | Seconds | Action |
|---|---|---|
| Classify | 10 | output? safety? exception? state? |
| Table lookup | 20 | Tables 1–6 |
| Strike out order-dependent claims | 15 | the real work |
| Write | 15 | exact statements |
| **Total** | **~60** | |

## Worked example

**Q. Which statements are guaranteed?**

```java
public class Main {
    static int n = 0;
    public static void main(String[] args) throws Exception {
        Thread t = new Thread(() -> { n = 1; });
        t.start();
        t.join();
        System.out.println(n);
    }
}
```

**Output (exact):**

```
1
```

`join()` guarantees the thread finished before the print, so `n` is definitely `1`. (Without the
`join()`, `n` would be `0` or `1` — an unspecified value.)

## Quick rules

- `start()` → new thread; `run()` → current thread.
- Output order between threads is **never** guaranteed.
- `join()` is the only reliable "wait until it finishes".
- `sleep()` keeps the lock; `wait()` releases it.
- `wait()`/`notify()` need the monitor.
- `volatile` = visibility, not atomicity.
- Daemon threads die with the last non-daemon thread.
- `Thread.State` has 6 values.
- `isInterrupted()` does not clear the flag; `Thread.interrupted()` does.

## Common traps

| Trap | Fix |
|---|---|
| `t.run()` starts a thread | Only `start()` does |
| `start()` order fixes run order | It does not |
| Priority fixes run order | It is a hint |
| `volatile` makes `count++` atomic | It does not |
| `sleep()` releases the lock | It does not |
| `wait()` outside `synchronized` hangs | `IllegalMonitorStateException` |
| `notify()` wakes the right thread | It wakes an arbitrary one |
| `ArrayList` is safe to share | It is not |

## Checklist

- [ ] I can apply Table 6 to any thread output question.
- [ ] I know Table 2's safe column.
- [ ] I know Table 3's exceptions.
- [ ] I know `sleep()` vs `wait()`.
- [ ] I know the six thread states.

## Related

- [Thread lifecycle and creation](../01-concepts/01-thread-lifecycle-and-creation.md)
- [Synchronization and race conditions](../01-concepts/02-synchronization-and-race-conditions.md)
- [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)
- [Solved threads set](../03-worked-examples/01-solved-threads-set.md)
- [Thread traps](../04-pitfalls/01-thread-traps.md)
- [Topic overview](../README.md)
