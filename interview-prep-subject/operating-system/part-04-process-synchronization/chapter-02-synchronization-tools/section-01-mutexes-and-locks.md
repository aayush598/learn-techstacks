# Section 01: Mutexes and Locks

> **TL;DR**: A mutex (mutual exclusion) is the fundamental lock: only one thread holds it at a time. Implementations use an atomic fast path (TAS/CAS) and, under contention, put the waiter to sleep in a kernel wait queue (futex on Linux) — plus priority inheritance and recursive variants for correctness.

## 1. Why Does This Exist?
The critical-section problem needs a practical "one at a time" gate that scales beyond spinning. A mutex exists to (1) guarantee mutual exclusion with a simple acquire/release API, and (2) do it *efficiently*: uncontended acquires are a single atomic op, while contended ones block the waiter (sleep) instead of burning CPU. It's the most common synchronization primitive in every OS and every threaded application.

## 2. How Does It Work?
- State: locked/unlocked (often a 32-bit word: 0 free, 1 locked, 2+ waiting).
- `lock()`: fast path — CAS 0→1; if it fails, go slow path: register in kernel wait queue (futex) and sleep.
- `unlock()`: CAS 1→0; if waiters exist, wake one (futex wake).
- Ownership: kernel mutexes track the owner (needed for priority inheritance); userland PTHREAD_MUTEXES have normal (deadlock on re-acquire), recursive (owner can re-acquire), and error-checking types.
- Queue fairness: waiter handoff avoids starvation (futex queue FIFO).

## 3. When Is It Used?
- Default exclusive lock for any shared structure: linked lists, hash tables, sockets, caches.
- Short or long critical sections both work (sleeping when contended).
- Cross-thread (pthread_mutex_t), cross-process (robust mutexes, futex in shared memory), kernel (`struct mutex`).
- When the CS can block (I/O inside) — a spinlock can't be held across a sleep.

## 4. Why Wasn't Another Approach Chosen?
- **Spinlock**: wastes CPU if CS is long or contended — rejected for general use (kept for tiny kernel CS).
- **Semaphore(1)**: functionally similar but semantically weaker (no ownership → PI impossible, easier to misuse). Rejected as the default.
- **Disable preemption/interrupts**: uniprocessor-only. Rejected.
- **Language monitors**: nicer but not available cross-language/cross-process; mutex is the portable base.
The mutex wins as the *exclusive, ownership-tracking, sleeping* primitive — with a cheap atomic fast path and kernel sleep fallback.

## 5. Intuition
**A hotel room key**: one guest holds the key at a time (mutual exclusion). If the room is occupied, a new guest waits — ideally sitting in the lobby (sleeping) rather than pacing the hallway (spinning). When the current guest leaves, the front desk wakes the next guest and hands them the key (handoff). "Recursive" = the guest can re-enter the room as long as they still hold the key.

## 6. Real-World Analogy
**A single checkout line with a "lane open" sign**: if the lane is open (uncontended), the next customer walks straight up (fast path CAS). If it's busy, customers wait in a queue (futex wait list) — reading a book (sleeping), not tapping their feet (spinning). When the cashier finishes, they signal the first in line (futex wake). If a VIP is waiting but a slow customer is being served by the only cashier, the VIP priority is inherited so the cashier finishes faster (priority inheritance).

## 7. Formal Definition
- **Mutex**: a lock with state {unlocked, locked} and ownership. Operations: acquire (wait until free, then lock), release (unlock). At most one owner at a time.
- **Recursive mutex**: the owner may acquire again; each acquire must be matched by a release (owner + count).
- **Fast path**: atomic `CAS(state, 0, 1)` succeeds → owner. **Slow path**: futex wait (kernel enqueues, sleeps, wakes on futex wake).
- **Robust mutex**: if the owner dies holding it, waiters get EOWNERDEAD (recoverable) — for cross-process locks.
- **Priority inheritance (PI)**: if a higher-priority thread waits on a mutex held by a lower-priority thread, the holder's priority is raised — prevents priority inversion (Part 03 Ch 2 Sec 4).

## 8. Example
```
Thread A: lock() -> fast CAS 0->1 wins, A owns.   [A in CS]
Thread B: lock() -> CAS fails (state=1), futex_wait. B sleeps.   [B waiting]
Thread A: unlock() -> state=0, futex_wake -> B wakes, CAS 0->1, B owns. [B in CS]
```
Both threads never in CS simultaneously; B burned no CPU while waiting.

## 9. Internal Working
1. **Fast path** (userland, `pthread_mutex_lock` on Linux): try `cmpxchg` the word 0→1. Success → done (no syscall).
2. **Slow path**: `futex(FUTEX_WAIT)` syscall — kernel adds the task to the futex's wait queue and sleeps it.
3. On **unlock**: userland `cmpxchg` 1→0; if the word had "waiters" flag, `futex(FUTEX_WAKE)` wakes one.
4. Kernel `struct mutex`: uses optimistic spinning — the waiter spins briefly (like MCS) hoping the holder finishes fast, then sleeps in the wait queue (`MUTEX_FLAG_WAITERS`).
5. **PI**: `rt_mutex` for PI-capable; `__mutex_lock` tracks owner for `owner` field; sleepers boost owner.
6. Robust/futex-shared: word lives in shared memory (MAP_SHARED); kernel validates owner identity.

## 10. Time Complexity
- Uncontended acquire/release: O(1) (one atomic op, ~tens of ns; no syscall).
- Contended: O(syscall + wakeup latency) ≈ µs — plus queue handoff O(1).
- Optimistic spinning: bounded spin time then sleep.
- Contention cost dominates: each lock/unlock pair costs a cacheline transfer between CPUs.

## 11. Advantages
- Simple, portable, correct abstraction for exclusive access.
- Cheap when uncontended (no syscall).
- Sleeping waiters → no CPU waste under contention.
- Ownership tracking enables PI and recursive locks.
- Robust variants survive holder death.

## 12. Disadvantages
- Serializes access — contention kills parallelism (Amdahl).
- Overhead of syscall + wakeup when contended (latency ~µs).
- Deadlock if used incorrectly (wrong order, missing unlock).
- Priority inversion still needs PI to be safe.
- Fairness (FIFO wakeup) can hurt throughput under high contention (handoff lock).
- Not composable: holding two mutexes invites deadlock.

## 13. Interview Questions
1. **Q: What is a mutex?** A: An exclusive lock — only one thread owns it at a time; acquire/release with atomic fast path and sleep fallback.
2. **Q: Mutex vs spinlock?** A: Mutex sleeps when contended (fine for long CS); spinlock busy-waits (only for very short kernel CS). Mutex costs a syscall when contended.
3. **Q: How does a mutex avoid spinning when contended?** A: The waiter calls futex_wait → kernel parks it; unlock does futex_wake → kernel unparks one waiter.
4. **Q (TRICKY): What's the fast path?** A: `cmpxchg` the lock word 0→1 in userland — if it succeeds, no syscall at all. Only contended acquires pay the futex syscall.
5. **Q: What is a recursive mutex?** A: The owner can acquire multiple times; needs matching releases. Default pthread mutexes deadlock on re-acquire; PTHREAD_MUTEX_RECURSIVE allows it.
6. **Q: Why does a kernel mutex track the owner?** A: For priority inheritance — if a higher-priority thread waits, the holder's priority is raised so it finishes sooner (bounded inversion).
7. **Q: What is a robust mutex?** A: A mutex that detects its owner died (EOWNERDEAD) so the waiting process can recover state instead of deadlocking forever.
8. **Q (PRODUCTION): A mutex is contended heavily and latency spikes. What do you do?** A: Reduce contention: shrink CS, use RW locks/read-mostly, shard data, or use optimistic/lock-free paths (Part 04 Ch 4).
9. **Q: What's the difference between a mutex and a binary semaphore?** A: A mutex has ownership (only the lock holder unlocks; enables PI, recursive); a binary semaphore is a signaling counter with no owner. Mutex = exclusion; semaphore = signaling/coordination.
10. **Q: Can a mutex be held across a sleep?** A: Yes in userland (threads sleep); in the kernel, a `struct mutex` may be held across schedule() (it's a sleeping lock), but a spinlock cannot.
11. **Q: What is optimistic spinning in kernel mutexes?** A: The waiter spins briefly on the holder's CPU state (MCS-style) before sleeping — avoids syscall latency if the holder finishes quickly.
12. **Q (TRICKY): Two mutexes, threads lock in different order — what happens?** A: Deadlock: A holds M1 waits M2; B holds M2 waits M1. Fix: consistent lock ordering or trylock/timeout.

## 14. Follow-Up Questions
1. **Q: What is a "handoff" or "fair" lock?** A: The lock is passed directly to the next waiter (futex queue handoff) instead of letting anyone race — prevents starvation, costs throughput.
2. **Q: What is `futex`?** A: Fast Userspace Mutex — kernel wait/wake on a userspace word; the mechanism behind pthread_mutex contention (detail in Part 04 Ch 4).
3. **Q: What's the difference between PTHREAD_MUTEX_NORMAL and ERRORCHECK?** A: NORMAL = no checking (deadlock on re-acquire); ERRORCHECK = returns EDEADLK instead of deadlocking; RECURSIVE = allows re-acquire.
4. **Q: How do you avoid deadlock with multiple locks?** A: Order locks consistently, use trylock with backoff, or hold a single lock covering all operations.
5. **Q: What is a "lock convoy"?** A: After release, wakeups serialize as threads re-contend — throughput collapses under load; mitigated by handoff and shorter CS.

## 15. Coding Example
```c
/* Pthread mutex: uncontended fast path + proper usage */
#include <pthread.h>
#include <stdio.h>

#define N 1000000
long counter = 0;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

void *worker(void *arg) {
    for (int i = 0; i < N; i++) {
        pthread_mutex_lock(&m);
        counter++;
        pthread_mutex_unlock(&m);
    }
    return NULL;
}

int main(void) {
    pthread_t t[4];
    for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, worker, NULL);
    for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);
    printf("counter = %ld (expect %ld)\n", counter, 4L * N);
    return 0;
}
```
```c
/* Kernel-style mutex API (Linux) */
#include <linux/mutex.h>
static struct mutex my_lock;
mutex_init(&my_lock);

void update(void) {
    mutex_lock(&my_lock);
    /* critical section — safe to block here */
    mutex_unlock(&my_lock);
}
```

## 16. Industry Usage
- **Every thread-safe library** uses mutexes (or RW locks) for shared structures.
- **Linux kernel**: `struct mutex` (sleeping) vs spinlock (short CS).
- **glibc/pthread**: futex-based mutexes; glibc 2.34+ "generic" mutexes use futex2.
- **Databases**: buffer pool latch (a mutex) protecting pages.
- **Language runtimes**: Go's sync.Mutex, Java's ReentrantLock, Rust's std::sync::Mutex — all futex/atomic-backed.

## 17. References
- Silberschatz, *OS Concepts*, 7.4 (Mutexes).
- Linux: `kernel/locking/mutex.c`, `include/linux/mutex.h`, futex docs.
- man: `pthread_mutex_lock(3)`, `futex(2)`.
- Russinovich, *Windows Internals* (dispatcher synchronization — the OS equivalent).

## 18. Cheat Sheet
- Mutex: exclusive owner; fast-path CAS, slow-path sleep (futex).
- Uncontended: O(1), no syscall. Contended: syscall + wake (~µs).
- Mutex vs spinlock: sleep vs spin — mutex for long CS, spin for short kernel CS.
- Recursive: owner re-acquires with count.
- Robust: owner death → EOWNERDEAD recoverable.
- PI: holder inherits waiter priority (bounded inversion).
- Optimistic spinning: spin-then-sleep.
- Hold-many-locks → order consistently or deadlock.
- Binary semaphore ≠ mutex (no ownership/signaling semantics).

## 19. Quiz
1. Mutex allows: a) many owners b) one owner c) zero d) readers → **b**
2. Contended mutex waiter: a) spins b) sleeps (futex) c) busy-loop d) dies → **b**
3. Fast path is: a) syscall b) atomic CAS c) I/O d) sleep → **b**
4. Recursive mutex lets: a) anyone acquire b) owner re-acquire c) readers d) none → **b**
5. Robust mutex handles: a) contention b) owner death c) priority d) recursion → **b**
6. PI fixes: a) deadlock b) priority inversion c) race d) spin → **b**
7. Mutex vs spinlock: a) same b) sleep vs spin c) spin better d) none → **b**
8. Optimistic spinning: a) never sleeps b) spins briefly then sleeps c) spins forever d) polls → **b**
9. Binary semaphore vs mutex: a) same b) no ownership in semaphore c) semaphore faster d) none → **b**
10. Wrong lock order causes: a) race b) deadlock c) faster d) priority → **b**

## 20. Flashcards
- **Q: Mutex?** → **A:** Exclusive lock; fast CAS + futex sleep.
- **Q: Fast path?** → **A:** Atomic CAS 0→1, no syscall.
- **Q: Contended?** → **A:** futex wait/wake, sleeps.
- **Q: Recursive?** → **A:** Owner re-acquires with count.
- **Q: Robust?** → **A:** Owner death → EOWNERDEAD.
- **Q: PI?** → **A:** Holder inherits waiter priority.
- **Q: Spin vs sleep?** → **A:** Spin=short CS; mutex=long.
- **Q: Deadlock cause?** → **A:** Wrong lock ordering.

## 21. Revision
A mutex is the exclusive lock: an atomic fast path (CAS 0→1, no syscall) and a sleep-based slow path (futex wait/wake) — making uncontended use cheap and contended use CPU-free. Kernel mutexes track ownership for priority inheritance and support recursive/robust variants. The design tension: spinlocks only for tiny kernel CS; mutexes for everything that may block. Misuse (wrong lock order, missing unlock) produces deadlock; contention management is the scalability story (RW locks, sharding, lock-free — later chapters).

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a mutex?" | 13 Q1 / 7 Formal Definition |
| "Mutex vs spinlock?" | 13 Q2 / 4 Why Wasn't Another Approach Chosen |
| "How avoid spinning?" | 13 Q3 / 9 Internal Working |
| "What is the fast path?" | 13 Q4 / 9 Internal Working |
| "Recursive mutex?" | 13 Q5 / 7 Formal Definition |
| "Why track owner?" | 13 Q6 / 9 Internal Working |
| "Robust mutex?" | 13 Q7 / 7 Formal Definition |
| "Contention spikes — fix?" | 13 Q8 / 12 Disadvantages |
| "Mutex vs binary semaphore?" | 13 Q9 / 7 Formal Definition |
| "Different lock order — deadlock?" | 13 Q12 / 12 Disadvantages |
