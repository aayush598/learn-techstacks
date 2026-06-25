# Mutex vs Semaphore

## Mutex (Mutual Exclusion)
- A **locking mechanism** — only the **owner** can unlock it
- **Ownership**: tracks which thread holds the lock
- Supports **priority inheritance** (prevents priority inversion)
- Usually implemented with **kernel support** (sleeps when contended)

## Binary Semaphore
- A **signaling mechanism** — any thread can post (signal) even if not the one who waited
- **No ownership** concept
- No priority inheritance
- Can be used for producer-consumer signaling (not just mutual exclusion)

## Key Differences
| Feature | Mutex | Binary Semaphore | Counting Semaphore |
|---------|-------|-----------------|--------------------|
| **Ownership** | Yes | No | No |
| **Unlock by** | Only owner | Any thread | Any thread |
| **Priority inheritance** | Yes (typically) | No | No |
| **Use case** | Mutual exclusion | Signaling / sync | Resource pool |
| **Recursive** | Can be (reentrant) | No | No |
| **Kernel object** | Usually | Sometimes | Sometimes |

## Recursive Mutex (Reentrant Lock)
- Same thread can lock multiple times without deadlock
- Must unlock same number of times
- Java `synchronized`, `ReentrantLock`, C++ `std::recursive_mutex`

## When to Use What
- **Mutex**: protect shared data (critical section)
- **Counting semaphore**: manage a pool of resources (e.g., thread pool, connection pool)
- **Binary semaphore**: signal events between threads (e.g., task completion)

## Common Interview Question
> In Linux, `pthread_mutex_t` vs `sem_t` — a mutex can only be unlocked by the thread that locked it. A semaphore can be posted by any thread. Use mutex for mutual exclusion, semaphore for signaling.
