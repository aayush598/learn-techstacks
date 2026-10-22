# 04-pitfalls — Threads Basics

> Section 4 · Java · Threads Basics · _Estimated reading time: 12 min_

## What lives here

12 traps, each written as **the wrong answer you will pick → the right answer → the one-line
guard**.

## Files

| File | Lines | What it gives you |
|---|---|---|
| [01-thread-traps.md](01-thread-traps.md) | 172 | The 12-trap table, the output-order trap, the `sleep()` vs `wait()` table, the `volatile` table, the lock-identity trap, the four `wait()`/`notify()` rules, the interrupted-flag table, a worked trap |

## The 12 traps in one line each

1. `t.run()` starts a thread → only `start()` does.
2. `start()` order fixes the run order → it does not.
3. Priority decides who runs first → it is a hint.
4. `volatile` makes `count++` atomic → it does not.
5. `sleep()` releases the lock → it does not.
6. `wait()` outside `synchronized` hangs → `IllegalMonitorStateException`.
7. `notify()` wakes the thread you want → an arbitrary one.
8. `if` is fine around `wait()` → use `while`.
9. Daemon threads keep the JVM alive → they are killed on exit.
10. Static and instance `synchronized` exclude each other → different monitors.
11. `join()` leaves the thread `RUNNABLE` → it is `TERMINATED`.
12. `ArrayList`/`HashMap` are safe to share → they are not.

## Related

- [Topic overview](../README.md)
- [Solved threads set](../03-worked-examples/01-solved-threads-set.md)
