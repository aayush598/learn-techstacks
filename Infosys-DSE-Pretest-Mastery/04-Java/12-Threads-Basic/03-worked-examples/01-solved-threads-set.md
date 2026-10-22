# Solved Set — Threads Basics

> Section 4 · Java · Threads Basics · _Estimated reading time: 22 min_
> **Prerequisite:** [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)

## In one sentence

10 fully solved thread questions, with **guaranteed** answers wherever the output order is not
deterministic.

## Why the pre-test tests this

Thread questions are the hardest to *drill* because many of them have no single printed output. The
skill this set teaches is **identifying which statement is guaranteed** — that is exactly what the
exam tests.

## Core concept

- `start()` creates a thread; `run()` does not.
- `join()` is the only reliable "wait for it".
- Output order between threads is **not** deterministic.
- `synchronized` = exclusion + visibility; `volatile` = visibility only.

## Worked example

### Q1 — `start()` vs `run()`

```java
public class Main {
    public static void main(String[] args) {
        Thread t = new Thread(() -> System.out.println(Thread.currentThread().getName()));
        t.run();
        t.start();
    }
}
```

**Options**

| # | Option |
|---|---|
| A | `main` then `Thread-0` |
| B | `Thread-0` then `main` |
| C | `main` then `Thread-0`, but the order of the two is not guaranteed |
| D | A compile error: `run` is not accessible |

**Answer: A** — `main` then `Thread-0`.

**Breakdown**

| Call | Thread that runs the body | Printed |
|---|---|---|
| `t.run()` | the **current** thread (`main`) | `main` |
| `t.start()` | a **new** thread (default name `Thread-0`) | `Thread-0` |

**Why not C:** the *order* here is fixed by the source — `t.run()` completes before `t.start()` is
even called. (The nondeterminism in thread questions is about which thread runs *first when both
are started*; a direct `run()` call is synchronous.)
**Why not D:** `run()` is `public` on `Thread`.

---

### Q2 — The guaranteed-statement pattern

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Thread a = new Thread(() -> System.out.println("A"));
        Thread b = new Thread(() -> System.out.println("B"));
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("C");
    }
}
```

**Options**

| # | Option |
|---|---|
| A | Always `A`, `B`, `C` in that order |
| B | Always `B`, `A`, `C` in that order |
| C | `A` and `B` may appear in either order; `C` is always last |
| D | A compile error: `join` requires the thread to be `Runnable` |

**Answer: C.**

**Breakdown**

| Statement | Guaranteed? | Why |
|---|---|---|
| `A` is printed | ✅ | `a` runs to completion — `join()` proves it |
| `B` is printed | ✅ | same |
| `A` before `B` | ❌ | the scheduler decides |
| `C` is last | ✅ | both `join()` calls complete first |
| Exactly 3 lines | ✅ | |

**Why not A / B:** `start()` order does not imply run order.
**Why not D:** `join()` is defined on `Thread`.

---

### Q3 — `join()` semantics

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Thread t = new Thread(() -> System.out.println("child"));
        t.start();
        t.join();
        System.out.println("parent");
    }
}
```

**Options**

| # | Option |
|---|---|
| A | `child` then `parent`, always |
| B | `parent` then `child`, always |
| C | The order is not guaranteed |
| D | `child` then `parent`, but only if `t` has a higher priority |

**Answer: A** — `child` then `parent`, always.

**Breakdown**

| Step | Why |
|---|---|
| 1 | `t.start()` launches the child thread |
| 2 | `t.join()` blocks the main thread until `t` finishes — so `child` is printed first |
| 3 | `join()` returns, then `parent` is printed |

**Why not C:** `join()` is exactly the tool that removes the uncertainty.
**Why not D:** priority plays no role.

---

### Q4 — Which one is **not** enough for a thread-safe counter?

```java
int counter = 0;                       // incremented by two threads
```

**Options**

| # | Option |
|---|---|
| A | Making the field `volatile` |
| B | Putting the increment inside a `synchronized` method |
| C | Using `AtomicInteger.incrementAndGet()` |
| D | None — all three make the increment safe |

**Answer: A** — `volatile` alone is **not** enough.

**Breakdown**

| Option | Safe? | Why |
|---|---|---|
| A | ❌ | `counter++` is a read-modify-write; `volatile` gives **visibility only**, not atomicity |
| B | ✅ | mutual exclusion + visibility |
| C | ✅ | compare-and-swap makes the increment atomic |
| D | ❌ | `volatile` is the exception |

**Why the exam likes this question:** it separates the candidates who know that `volatile` ≠
atomic.

---

### Q5 — `sleep()` vs `wait()`

**Options**

| # | Option |
|---|---|
| A | `sleep()` releases the lock; `wait()` keeps it |
| B | `sleep()` keeps the lock; `wait()` releases it |
| C | Both release the lock |
| D | Both keep the lock |

**Answer: B.**

**Breakdown**

| Method | Releases the lock? | Needs the monitor? |
|---|---|---|
| `Thread.sleep(ms)` | ❌ keeps it | ❌ no |
| `Object.wait()` | ✅ releases it | ✅ yes — else `IllegalMonitorStateException` |

**Why it matters:** `sleep()` inside a `synchronized` block keeps other threads out for the whole
sleep. `wait()` lets them in.

---

### Q6 — `wait()` without the lock

```java
public class Main {
    public static void main(String[] args) {
        Object o = new Object();
        try {
            o.wait();
        } catch (InterruptedException e) {
            System.out.println("IE");
        } catch (IllegalMonitorStateException e) {
            System.out.println("IMSE");
        }
    }
}
```

**Options**

| # | Option |
|---|---|
| A | `IE` |
| B | `IMSE` |
| C | The program hangs |
| D | A compile error |

**Answer: B** — `IMSE`.

**Breakdown**

| Step | Why |
|---|---|
| 1 | `o.wait()` requires the current thread to hold `o`'s monitor |
| 2 | `main` holds no monitor on `o` → `IllegalMonitorStateException` is thrown **immediately** |
| 3 | `IllegalMonitorStateException` is an unchecked `RuntimeException`, so it is not caught by the `catch (InterruptedException)` clause — the second clause catches it |

**Why not C:** the exception is thrown at once; there is no wait.
**Why not D:** `wait()` is a valid `Object` method.

---

### Q7 — Daemon threads

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Thread t = new Thread(() -> {
            try { Thread.sleep(10000); } catch (InterruptedException e) { }
        });
        t.setDaemon(true);
        t.start();
        System.out.println("main done");
    }
}
```

**Options**

| # | Option |
|---|---|
| A | The program waits 10 seconds, then prints `main done` |
| B | The program prints `main done` and exits immediately — the daemon thread is killed |
| C | A compile error: `setDaemon` must be called before the thread is created |
| D | `IllegalThreadStateException` at `setDaemon` |

**Answer: B.**

**Breakdown**

| Fact | Consequence |
|---|---|
| A daemon thread does not keep the JVM alive | the JVM exits when `main` (the last non-daemon thread) finishes |
| `setDaemon` must be called **before** `start()` | here it is, so no exception |
| The JVM kills the daemon thread on exit | the `sleep(10000)` never finishes |

**Why not A:** a daemon thread never delays shutdown.
**Why not D:** the call is before `start()`, which is legal.

---

### Q8 — Thread states

```java
Thread t = new Thread(() -> { });
System.out.println(t.getState());
t.start();
t.join();
System.out.println(t.getState());
```

**Options**

| # | Option |
|---|---|
| A | `NEW` then `TERMINATED` |
| B | `NEW` then `RUNNABLE` |
| C | `RUNNABLE` then `TERMINATED` |
| D | `NEW` then `WAITING` |

**Answer: A** — `NEW` then `TERMINATED`.

**Breakdown**

| Moment | State | Why |
|---|---|---|
| after `new Thread(...)` | `NEW` | `start()` has not been called |
| after `t.join()` | `TERMINATED` | `run()` has returned |

**Why not B:** by the time `join()` returns, the thread is finished — not `RUNNABLE`.
**Why not D:** `WAITING` means the thread is blocked in `wait()`/`join()`; after the join
completes the thread is dead.

---

### Q9 — Interruption

```java
public class Main {
    public static void main(String[] args) throws Exception {
        Thread t = new Thread(() -> {
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                System.out.println("interrupted");
            }
        });
        t.start();
        Thread.sleep(100);
        t.interrupt();
        t.join();
    }
}
```

**Options**

| # | Option |
|---|---|
| A | Nothing is printed; `t` sleeps the full 5 seconds |
| B | `interrupted` is printed |
| C | A compile error: `interrupt` is not a public method |
| D | `t` keeps sleeping and the flag stays set |

**Answer: B** — `interrupted` is printed.

**Breakdown**

| Step | Why |
|---|---|
| 1 | `t` is inside `Thread.sleep(5000)` |
| 2 | `t.interrupt()` sets the interrupt flag; `sleep` is interruptible, so it throws `InterruptedException` **and clears the flag** |
| 3 | The catch block prints `interrupted` |

**Why not A:** `sleep` is one of the interruptible methods.
**Why not D:** the exception clears the flag.

---

### Q10 — Race condition

```java
public class Main {
    static int counter = 0;
    public static void main(String[] args) throws Exception {
        Runnable task = () -> { for (int i = 0; i < 1000; i++) counter++; };
        Thread t1 = new Thread(task);
        Thread t2 = new Thread(task);
        t1.start(); t2.start();
        t1.join(); t2.join();
        System.out.println(counter);
    }
}
```

**Options**

| # | Option |
|---|---|
| A | Always `2000` |
| B | At most `2000`; possibly less |
| C | Always `1000` |
| D | More than `2000` |

**Answer: B** — at most `2000`, possibly less.

**Breakdown**

| Fact | Consequence |
|---|---|
| `counter++` is a read-modify-write, not atomic | the two threads can interleave the three steps and lose an update |
| `counter` is a plain static field | there is no visibility guarantee either |
| `join()` waits for both threads | the print happens after both finish, so the value is final — but it may be **less than** 2000 |

**Why not A:** without synchronisation, updates can be lost.
**Why not C:** the value is not deterministic, so 1000 is not guaranteed.
**Why not D:** the counter only ever increases, so it can never exceed 2000.

**Fixes:** make `increment()` `synchronized`, use an `AtomicInteger`, or use `LongAdder`.

## Quick rules

- `start()` → new thread; `run()` → current thread.
- `join()` guarantees ordering **after** the join.
- Output order between two started threads is **never** guaranteed.
- `sleep()` keeps the lock; `wait()` releases it.
- `wait()`/`notify()` need the monitor → `IllegalMonitorStateException` otherwise.
- `volatile` = visibility, not atomicity.
- Daemon threads do not keep the JVM alive.
- `getState()` returns one of six values.
- `interrupt()` on a sleeping thread throws `InterruptedException` and clears the flag.

## Common traps

| Trap | Where it appears |
|---|---|
| `run()` starts a thread | Q1 |
| `start()` order fixes run order | Q2 |
| `volatile` makes `counter++` safe | Q4, Q10 |
| `sleep()` releases the lock | Q5 |
| `wait()` outside `synchronized` hangs | Q6 |
| Daemon threads delay shutdown | Q7 |
| `join()` leaves the thread `RUNNABLE` | Q8 |

## Checklist

- [ ] I can answer any thread output question with the guaranteed statements only.
- [ ] I know which of `volatile`/`synchronized`/`AtomicInteger` gives atomicity.
- [ ] I know `sleep()` vs `wait()` from memory.
- [ ] I know the six thread states and when each applies.
- [ ] I know the daemon rule and the interruption rule.

## Related

- [Thread lifecycle and creation](../01-concepts/01-thread-lifecycle-and-creation.md)
- [Synchronization and race conditions](../01-concepts/02-synchronization-and-race-conditions.md)
- [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)
- [Thread traps](../04-pitfalls/01-thread-traps.md)
- [Threads one-pager](../05-reference/01-threads-one-pager.md)
- [Topic overview](../README.md)
