# Topic 12 — Threads Basics

> Section 4 · Java · Topic 12 · _Estimated reading time: 18 min_

## What this topic covers

1. **Thread lifecycle** — creating a thread, the six states, `start()` vs `run()`, daemon threads,
   and interruption.
2. **Synchronization** — `synchronized`, `volatile`, `AtomicInteger`, `wait()`/`notify()`, deadlocks,
   and thread-safe collections.

## Why the pre-test tests this

- Section 4 thread questions are always one of three shapes: an output question, a "which is
  thread-safe?" question, or a "which throws what?" question.
- The output questions have **no single ordering** — the exam's correct option is the one that
  states what is *guaranteed*. Learning to spot that is the entire skill.
- Concurrency is a common differentiator between candidates who score 70% and 85%.

## What you must be able to do

| Skill | Where it is drilled |
|---|---|
| Explain `start()` vs `run()` | [01-concepts/01-thread-lifecycle-and-creation.md](01-concepts/01-thread-lifecycle-and-creation.md) |
| Name the six `Thread.State` values | [01-concepts/01-thread-lifecycle-and-creation.md](01-concepts/01-thread-lifecycle-and-creation.md) |
| State exactly what `synchronized` and `volatile` guarantee | [01-concepts/02-synchronization-and-race-conditions.md](01-concepts/02-synchronization-and-race-conditions.md) |
| Use `wait()`/`notify()` without breaking the rules | [01-concepts/02-synchronization-and-race-conditions.md](01-concepts/02-synchronization-and-race-conditions.md) |
| Pick the **guaranteed** statement in an output question | [02-techniques/01-thread-interview-techniques.md](02-techniques/01-thread-interview-techniques.md) |
| Recognise the thread-safe collections | [02-techniques/01-thread-interview-techniques.md](02-techniques/01-thread-interview-techniques.md) |

## Folder map

| Folder | Contents | Read when |
|---|---|---|
| [01-concepts](01-concepts/README.md) | 2 files: lifecycle & creation, synchronization & race conditions | First pass |
| [02-techniques](02-techniques/README.md) | 1 file: 6 tables + the 60-second procedure | Before the exam |
| [03-worked-examples](03-worked-examples/README.md) | 1 file: 10 fully solved questions | Practice |
| [04-pitfalls](04-pitfalls/README.md) | 1 file: 12 traps with guards | Last night |
| [05-reference](05-reference/README.md) | 1 file: the printable one-pager | Exam morning |

## The 10-second answer

| Question shape | The rule |
|---|---|
| "What is printed?" with 2 threads | Only the **guaranteed** statements are defensible |
| "Does `t.run()` start a thread?" | No — only `start()` does |
| "Is `volatile` enough for a counter?" | No — visibility only |
| "Does `sleep()` release the lock?" | No — `wait()` does |
| "What happens if `wait()` is called without the lock?" | `IllegalMonitorStateException` |
| "Is `ArrayList` thread-safe?" | No |
| "How many thread states?" | 6 |

## Common mistakes to avoid

- ❌ Assuming `t1.start()` before `t2.start()` means `t1` prints first.
- ❌ Assuming priority controls the order.
- ❌ Believing `volatile` makes `count++` atomic.
- ❌ Believing `sleep()` releases the lock.
- ❌ Calling `wait()` outside a `synchronized` block.
- ❌ Using `if` instead of `while` around `wait()`.

## Related topics

- [07 — Exceptions & Error Handling](../07-Exceptions-Error-Handling/README.md)
- [08 — Output Prediction Patterns](../08-Output-Prediction-Patterns/README.md)
- [10 — Static, Final, Varargs & Operators](../10-Static-Final-Varargs-Operators/README.md)
- [11 — Arrays, ArrayList & Loops](../11-Arrays-ArrayList-Loops/README.md)
- [13 — Java Question Bank](../13-Question-Bank/README.md)
