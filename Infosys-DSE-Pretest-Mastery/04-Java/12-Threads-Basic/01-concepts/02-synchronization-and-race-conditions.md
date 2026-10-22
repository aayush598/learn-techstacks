# Synchronization and Race Conditions

> Section 4 · Java · Threads Basics · _Estimated reading time: 13 min_
> **Prerequisite:** [Thread lifecycle and creation](01-thread-lifecycle-and-creation.md)

## In one sentence

`synchronized` gives you **mutual exclusion + visibility**; `volatile` gives you **visibility
only**; and `wait()`/`notify()` are the only way to hand a lock over politely.

## Why the pre-test tests this

- "Which of these is thread-safe?" is a standard MCQ with `synchronized`, `volatile`, `AtomicInteger`
  and `synchronizedList` as the options.
- "What happens if two threads increment the same counter?" is the race-condition question, and
  the answer is "the result is unpredictable, and may even be less than the sum" — not "it works
  eventually".
- `wait()`/`notify()` are a classic trap because of the `IllegalMonitorStateException` rule.

## Core concept

### The race condition

```java
static int counter = 0;
static void increment() {
    counter++;          // read, add, write — three steps
}
```

Two threads calling `increment()` a thousand times each may produce a result **less than 2000**.
`counter++` is not atomic — it is a read-modify-write, and the three steps can interleave.

**The fix:** `synchronized`, `AtomicInteger`, or `LongAdder`.

### `synchronized` — the three forms

```java
// 1. instance method — locks `this`
public synchronized void m() { }

// 2. static method — locks the Class object (ClassName.class)
public static synchronized void m() { }

// 3. block — locks the object you name
synchronized (lockObject) { }
```

| Form | The monitor locked |
|---|---|
| `synchronized void m()` | `this` |
| `static synchronized void m()` | `ClassName.class` |
| `synchronized (obj) { }` | `obj` |
| `synchronized (this) { }` | `this` — same as form 1 |

**Two different lock objects mean two different locks.** A static synchronized method and an
instance synchronized method on the same class do **not** exclude each other.

**What `synchronized` guarantees**

| Guarantee | Meaning |
|---|---|
| Mutual exclusion | only one thread at a time holds that monitor |
| Visibility | a write by one thread is visible to the next thread that acquires the same lock |
| Happens-before | everything before the unlock is visible to the next acquirer |
| Reentrancy | a thread already holding the lock can re-acquire it (no self-deadlock) |

### `volatile`

```java
volatile boolean running = true;
```

| Property | `volatile` | `synchronized` |
|---|---|---|
| Mutual exclusion | ❌ | ✅ |
| Visibility | ✅ | ✅ |
| Atomicity of `count++` | ❌ | ✅ |
| Cost | cheap | heavier |

**`volatile` does NOT make compound operations atomic.** `volatileCount++` is still a
read-modify-write and can still lose updates. Use `volatile` for a **flag** (a value that is only
written once and read many times), not for a counter.

### `AtomicInteger`

```java
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();     // returns the new value
count.getAndIncrement();     // returns the old value
count.addAndGet(5);
count.get();                 // read
count.compareAndSet(5, 10); // CAS — compare and swap
```

`incrementAndGet()` is atomic — it uses compare-and-swap internally, so no update is lost.

### `wait()`, `notify()`, `notifyAll()`

These are the **three** methods every `Object` has.

| Method | What it does | Throws |
|---|---|---|
| `wait()` | release the monitor and wait until notified | `InterruptedException` |
| `wait(timeout)` | same, but give up after the timeout | `InterruptedException` |
| `notify()` | wake **one** waiting thread (arbitrary) | `IllegalMonitorStateException` if you don't hold the lock |
| `notifyAll()` | wake **all** waiting threads | `IllegalMonitorStateException` if you don't hold the lock |

**The four rules you must not break:**

1. `wait()`/`notify()`/`notifyAll()` must be called **inside** a `synchronized` block or method
   that holds the monitor of the **same object** you call them on.
2. Calling them without the lock throws `IllegalMonitorStateException`.
3. `wait()` **releases** the lock and reacquires it before returning — that is the whole point.
4. `wait()` can wake up **spuriously**, so always guard with a `while` loop, never an `if`.

```java
synchronized (lock) {
    while (!condition) {       // while, NOT if
        lock.wait();
    }
}
```

**`notify()` vs `notifyAll()`:** `notify()` wakes exactly one waiter — but you do not control
*which* one, so it can wake a thread that is not the one you wanted. `notifyAll()` is safer, but
can cause a thundering herd. In an exam, "which is correct?" → **`notifyAll()` is the safe
choice**.

### Deadlock

A deadlock is when two (or more) threads each hold a lock the other needs.

```java
synchronized (lockA) {
    synchronized (lockB) { }     // thread 1
}
synchronized (lockB) {
    synchronized (lockA) { }     // thread 2 → deadlock
}
```

**How to avoid it:**

| Technique | How |
|---|---|
| Consistent lock ordering | always acquire locks in the same global order |
| One lock | use a single monitor for everything |
| `tryLock()` with a timeout | `ReentrantLock.tryLock()` returns `false` instead of blocking forever |
| Avoid nested locks | keep the critical sections short and flat |

Java can detect a deadlock: `Thread.getAllStackTraces()` plus `ThreadMXBean.findDeadlockedThreads()`
(or `Thread.deadlock()` in older versions).

### Thread-safe collections

| Collection | Thread-safe? | Notes |
|---|---|---|
| `ArrayList` | ❌ | not safe for concurrent use |
| `Vector` | ✅ | legacy; every method is `synchronized` |
| `HashMap` | ❌ | corruption under concurrent writes |
| `Hashtable` | ✅ | legacy |
| `ConcurrentHashMap` | ✅ | the modern choice for concurrent maps |
| `CopyOnWriteArrayList` | ✅ | best for read-mostly, iterate without locking |
| `Collections.synchronizedMap(m)` | ✅ | a wrapper |
| `ConcurrentLinkedQueue` | ✅ | a non-blocking queue |

**`StringBuilder` vs `StringBuffer`:** `StringBuilder` is **not** thread-safe (and is faster);
`StringBuffer` is thread-safe (its methods are `synchronized`).

### `ThreadLocal`

```java
private static final ThreadLocal<Integer> count = ThreadLocal.withInitial(() -> 0);
```

Each thread sees its **own** value of the variable. Used for per-request contexts, transaction
IDs, and SimpleDateFormat instances.

### `ExecutorService`

```java
ExecutorService pool = Executors.newFixedThreadPool(4);
pool.execute(() -> doWork());              // no result
Future<String> f = pool.submit(() -> "x"); // returns a Future
pool.shutdown();                            // no new tasks; existing ones finish
pool.shutdownNow();                         // interrupt running tasks
pool.awaitTermination(5, TimeUnit.SECONDS);
```

| `Executors` factory | Pool |
|---|---|
| `newFixedThreadPool(n)` | exactly `n` threads, reused |
| `newCachedThreadPool()` | grows as needed, reuses idle threads |
| `newSingleThreadExecutor()` | one thread, tasks run in order |
| `newScheduledExecutor()` | supports `schedule` / `scheduleAtFixedRate` |

## Worked example

**Q. What is printed?**

```java
public class Main {
    static int counter = 0;
    static synchronized void increment() { counter++; }
    public static void main(String[] args) throws Exception {
        Thread t1 = new Thread(Main::run);
        Thread t2 = new Thread(Main::run);
        t1.start(); t2.start();
        t1.join(); t2.join();
        System.out.println(counter);
    }
    static void run() {
        for (int i = 0; i < 1000; i++) increment();
    }
}
```

**Solution**

| Step | Reasoning |
|---|---|
| 1 | Both threads call `increment()`, which is `static synchronized` → both lock the **same** monitor (`Main.class`) |
| 2 | The lock serialises the 2000 increments, so **no** increment is lost |
| 3 | `join()` guarantees both threads finish before the print |
| 4 | `counter` is exactly 2000 |

**Output (exact):**

```
2000
```

**Now the contrast question** — remove `synchronized`:

| Version | Guaranteed result? |
|---|---|
| `static synchronized void increment()` | ✅ exactly `2000` |
| `static void increment()` | ❌ **not guaranteed** — the result may be **less than 2000** (lost updates) |
| `static void increment()` with `counter` also `volatile` | ❌ still not guaranteed — `volatile` does not make `++` atomic |

**That third row is the classic trap**: making the field `volatile` fixes *visibility*, not
*atomicity*.

## Quick rules

- `synchronized` = mutual exclusion **+** visibility **+** happens-before.
- `volatile` = visibility **only**; `count++` is still not atomic.
- `AtomicInteger` makes `incrementAndGet()` atomic.
- `wait()`/`notify()` need the monitor — else `IllegalMonitorStateException`.
- `wait()` releases the lock; `notify()` wakes one waiter; `notifyAll()` wakes all.
- Always guard `wait()` with a **`while`** loop (spurious wakeups).
- `volatile` flag + `synchronized` block is the canonical producer/consumer shape.
- `ArrayList` and `HashMap` are not thread-safe; use `ConcurrentHashMap` /
  `CopyOnWriteArrayList`.
- `StringBuilder` is not thread-safe; `StringBuffer` is.
- Acquire multiple locks in a consistent order to avoid deadlock.

## Common traps

| Trap | What you pick | The truth |
|---|---|---|
| `volatile` makes `count++` atomic | it is safe | It is not |
| `notify()` wakes the thread you want | the waiting thread | It wakes an **arbitrary** one |
| `wait()` keeps the lock | it holds the lock | It **releases** the lock |
| An `if` is fine around `wait()` | `if` | Use `while` — spurious wakeups |
| `static synchronized` and instance `synchronized` exclude each other | they do | Different monitors |
| `synchronized` on two objects is one lock | one lock | One lock per object |

## Checklist

- [ ] I can state exactly what `synchronized` and `volatile` each guarantee.
- [ ] I know the four `wait()`/`notify()` rules.
- [ ] I know why `while` and not `if` around `wait()`.
- [ ] I know which collections are thread-safe.
- [ ] I can describe a deadlock and two ways to avoid it.

## Related

- [Thread lifecycle and creation](01-thread-lifecycle-and-creation.md)
- [Thread interview techniques](../02-techniques/01-thread-interview-techniques.md)
- [Solved threads set](../03-worked-examples/01-solved-threads-set.md)
- [Thread traps](../04-pitfalls/01-thread-traps.md)
- [Threads one-pager](../05-reference/01-threads-one-pager.md)
- [Topic overview](../README.md)
