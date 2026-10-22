# Thread Interview Techniques

> Section 4 · Java · Threads Basics · _Estimated reading time: 9 min_
> **Prerequisite:** [Synchronization and race conditions](../01-concepts/02-synchronization-and-race-conditions.md)

## In one sentence

Thread questions are answered with a **classification step**: name the question's type, look it up
in the table, and — for output questions — pick the **guaranteed** statement.

## Why the pre-test tests this

Thread MCQs in the exam are mostly of three types:

1. **Output questions** — the answer is the guaranteed statement, never an ordering.
2. **"Which is thread-safe?"** — a table lookup.
3. **"Which method throws what?"** — a table lookup.

This file gives you all three tables plus the procedure that picks the right one.

## Core concept

### Table 1 — the four thread question types and how to answer them

| Type | How to answer | The trap |
|---|---|---|
| "What is printed?" | list only the statements that are **guaranteed** | picking a specific interleaving |
| "Which is thread-safe?" | Table 2 | assuming `volatile` is enough |
| "Which method throws what?" | Table 3 | swapping `wait()` and `sleep()` |
| "What is the output order?" | the answer is "**not deterministic**" | trusting the priority |

### Table 2 — thread-safety of the common choices

| Choice | Thread-safe? | Notes |
|---|---|---|
| `synchronized` method/block | ✅ | mutual exclusion + visibility |
| `volatile` field | ⚠ visibility only | `count++` is still unsafe |
| `AtomicInteger` | ✅ | `incrementAndGet()` is atomic |
| `ReentrantLock` | ✅ | `tryLock()` avoids deadlock |
| `ConcurrentHashMap` | ✅ | the modern concurrent map |
| `CopyOnWriteArrayList` | ✅ | read-mostly lists |
| `ConcurrentLinkedQueue` | ✅ | non-blocking queue |
| `Collections.synchronizedMap(m)` | ✅ | a wrapper |
| `Vector` / `Hashtable` / `StringBuffer` | ✅ | legacy — every method is `synchronized` |
| `ArrayList` / `HashMap` / `HashSet` | ❌ | never share these between threads |
| `StringBuilder` | ❌ | use one per thread |
| Plain field or static field | ❌ | visibility is not guaranteed |

### Table 3 — which method throws what

| Method | Throws | Notes |
|---|---|---|
| `Thread.sleep(ms)` | `InterruptedException` | **static** — pauses the current thread; releases no lock |
| `Object.wait()` | `InterruptedException` | needs the monitor; **releases** the lock |
| `Object.wait(ms)` | `InterruptedException` | needs the monitor; releases the lock; times out |
| `Thread.join()` | `InterruptedException` | waits for the thread to finish |
| `Object.notify()` | `IllegalMonitorStateException` | needs the monitor |
| `Object.notifyAll()` | `IllegalMonitorStateException` | needs the monitor |
| `Thread.start()` (twice) | `IllegalThreadStateException` | a thread starts once |
| `setDaemon(true)` after start | `IllegalThreadStateException` | set it before `start()` |
| `setPriority(99)` | `IllegalArgumentException` | the range is 1..10 |
| `wait()` without the lock | `IllegalMonitorStateException` | the most-asked trap |

### Table 4 — `sleep()` vs `wait()`

| Aspect | `sleep()` | `wait()` |
|---|---|---|
| Defined on | `Thread` (static) | `Object` (instance) |
| Releases the lock | ❌ keeps it | ✅ releases it |
| Needs the monitor | ❌ | ✅ — else `IllegalMonitorStateException` |
| Woken by | the passage of time | `notify()` / `notifyAll()` / a timeout |
| Can wake spuriously | ❌ | ✅ — so use a `while` loop |
| Thread it affects | the **current** thread | the calling thread |

### Table 5 — the "guaranteed statement" checklist

For any multi-thread output question, go through this list and mark the statements that survive:

| Check | Guaranteed? |
|---|---|
| Statements printed **before** `start()` | ✅ yes |
| Statements printed **after** `join()` on all threads | ✅ yes |
| The **number** of lines printed | ✅ yes (if every thread runs to completion) |
| The **relative order** of two threads' output | ❌ **no** |
| A higher-priority thread runs first | ❌ **no** — priority is a hint |
| `System.out.println` output is split mid-line | ❌ **no** — `PrintStream` synchronises the write |

**The last row is worth memorising:** `System.out` is a `PrintStream` whose `println` is
synchronised, so you will see whole lines, never half-lines.

### Table 6 — thread states

| State | Meaning |
|---|---|
| `NEW` | created, `start()` not called |
| `RUNNABLE` | running or eligible to run |
| `BLOCKED` | waiting to enter a monitor |
| `WAITING` | `wait()`, `join()`, `park()` |
| `TIMED_WAITING` | `sleep(ms)`, `wait(ms)`, `join(ms)` |
| `TERMINATED` | `run()` has returned |

### The 60-second procedure

1. **Is it an output question?** → Table 5. Write down only the guaranteed statements.
2. **Is it "which is thread-safe?"** → Table 2.
3. **Is it "which throws what?"** → Table 3, then Table 4 if it is `sleep` vs `wait`.
4. **Is it about thread state?** → Table 6.
5. **Is it about lifecycle or interruption?** → `start()` vs `run()`, daemon rules, the interrupt
   flag.
6. **Sanity check:** did you accidentally promise an ordering? Remove it.

## Worked example

**Q. Which statement is guaranteed?**

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

**Solution**

| Statement | Guaranteed? | Why |
|---|---|---|
| `A` and `B` are both printed | ✅ | both threads run to completion before `join()` returns |
| Exactly **three** lines are printed | ✅ | `A`, `B`, `C` |
| `A` is printed before `B` | ❌ | the scheduling is not deterministic |
| `A` is printed before `C` | ✅ | `join()` waits for `a` to finish before `C` is printed |
| `C` is printed last | ✅ | both joins precede it |
| `A` is printed before `B` **because** `a.start()` was called first | ❌ | `start()` order does not imply run order |

**The answer: the option stating that `A` and `B` may appear in either order, and `C` is printed
last.**

**Why the distractors fail**

| Option | Why it is wrong |
|---|---|
| `A` then `B` then `C` | The `A`/`B` order is not deterministic |
| `B` then `A` then `C` | Same problem |
| `C` then `A` then `B` | `join()` guarantees both threads finished before `C` |
| The output order is always `A`, `B`, `C` | Same as the first option |

## Quick rules

- Output order between threads is **never** guaranteed.
- `join()` is the only reliable "wait until it finishes".
- `sleep()` keeps the lock; `wait()` releases it.
- `wait()`/`notify()` without the monitor → `IllegalMonitorStateException`.
- `volatile` = visibility, not atomicity.
- `ArrayList`/`HashMap` are not thread-safe.
- `Thread.State` has 6 values.
- `System.out.println` prints whole lines.

## Common traps

| Trap | Fix |
|---|---|
| `start()` order determines run order | It does not |
| Priority determines run order | It is a hint |
| `volatile` makes `count++` atomic | It does not |
| `sleep()` releases the lock | It does not |
| `notify()` wakes a specific thread | It wakes an arbitrary one |
| `if` is fine around `wait()` | Use `while` |

## Checklist

- [ ] I can apply Table 5 to any thread output question.
- [ ] I know Table 2's thread-safe column.
- [ ] I know Table 3's exceptions.
- [ ] I know `sleep()` vs `wait()` from memory.
- [ ] I can list the six thread states.

## Related

- [Thread lifecycle and creation](../01-concepts/01-thread-lifecycle-and-creation.md)
- [Synchronization and race conditions](../01-concepts/02-synchronization-and-race-conditions.md)
- [Solved threads set](../03-worked-examples/01-solved-threads-set.md)
- [Thread traps](../04-pitfalls/01-thread-traps.md)
- [Threads one-pager](../05-reference/01-threads-one-pager.md)
- [Topic overview](../README.md)
