# IPC Semaphores and Synchronization

> **TL;DR**: IPC semaphores are kernel semaphore objects used by *processes* to coordinate access to shared resources (especially shared memory). **System V**: `semget`/`semop`/`semctl` — arrays of semaphores with atomic multi-op `struct sembuf`. **POSIX**: named `sem_open`/`sem_post`/`sem_wait` and unnamed `sem_init`/`sem_destroy` (which also work for threads). The key value over a mutex: a counting semaphore tracks available units and can be shared across unrelated processes.

## 1. Why Does This Exist?
Shared memory gives processes a common channel but **no coordination** — two processes updating the same counter race and lose updates (Section 03's demo). What's needed is a synchronization primitive that (a) works *across processes* (not just threads — a pthread mutex by default protects one process's threads), (b) is atomic and kernel-backed, and (c) can express both exclusive access (binary semaphore = mutex-like) and counting/limiting (e.g., "at most N slots free"). IPC semaphores are exactly that: kernel objects callable by any process that knows the key/name. They exist to make multi-process critical sections and producer–consumer resource counting correct.

## 2. How Does It Work?
**System V semaphores**:
- `semget(key, nsems, IPC_CREAT|0666)` → `int semid` (array of `nsems` semaphores).
- `semop(semid, struct sembuf *ops, nops)` — atomic batch: each op `{ sem_num, sem_op, sem_flg }`: `sem_op > 0` → add (release); `sem_op < 0` → try subtract (acquire), block if value would go negative; `sem_op == 0` → wait until value is 0. `SEM_UNDO` undoes ops on process exit (crash safety).
- `semctl(semid, num, IPC_RMID, ...)` destroys; `SETVAL`/`GETVAL` set/read.
- Kernel: `struct sem_array` with an array of `struct sem` (value, last op, wait queue).

**POSIX semaphores**:
- **Named**: `sem_t *s = sem_open("/name", O_CREAT, 0666, 1)`; `sem_wait(s)` (decrement, block if 0), `sem_trywait`, `sem_timedwait`, `sem_post(s)` (increment, wake), `sem_getvalue`, `sem_close`, `sem_unlink("/name")`.
- **Unnamed**: `sem_init(&s, pshared, 0/1)` — `pshared` nonzero → shared between processes (must be in shared memory); `sem_destroy`.
- Kernel: for named, files in `semfs`/tmpfs; for processes, the underlying implementation uses futexes (`SYS_futex`) — the semaphore's value is a user-space atomic integer; the kernel is involved only on contention.

**Semaphore vs mutex**:
- Mutex = ownership (the same thread must unlock); counting semaphore = no ownership (any process can post/wait) — more flexible, more error-prone (you can post twice by mistake).
- Semaphore value can be >1 → resource counting ("N available units") — a mutex is binary (locked/unlocked).

## 3. When Is It Used?
- **Protecting shared memory**: mutex-semaphore (value 1) around the critical section in shm.
- **Producer–consumer**: counting semaphore "free slots" + "filled slots" (the classic bounded-buffer; Section 04 / Part 04).
- **Resource limiting**: a "tickets available" semaphore (N max concurrent users of a resource).
- **Ordering/barriers**: `sem_op==0` to wait until a counter hits zero (all tasks done).
- **Cross-process locks in the absence of threads**: POSIX named semaphores coordinate daemons, workers, and clients.
- **Threads too**: unnamed POSIX semaphores (pshared=0) are a valid alternative to pthread mutexes for thread sync.

## 4. Why Wasn't Another Approach Chosen?
- **pthread mutex by default (only threads)**: a process-shared pthread mutex requires `PTHREAD_PROCESS_SHARED` + shared memory setup — POSIX semaphores are the standard cross-process primitive.
- **Futex directly (too low-level)**: futexes are the implementation, not the API.
- **File locking (`flock`/`fcntl`)**: advisory locking on files — works across processes but tied to files, slower, and not a counting resource.
- **Spinlocks (CPU-burn)**: fine for short critical sections on multicore; IPC semaphores block (sleep) properly.
- **Signals as sync (messy)**: signals don't carry state and are unreliable for mutual exclusion.
- **Both SysV + POSIX (chosen)**: System V for the classic array/multi-op + SEM_UNDO features; POSIX for the cleaner, futex-backed, thread+process API — Linux ships both.

## 5. Intuition
**A parking garage ticket machine**: the semaphore value = free spaces. To enter (acquire), a driver takes a ticket — the counter decrements; if it's 0, drivers wait in line (block). Leaving (release) returns a ticket — the counter increments and a waiting driver can enter. A **binary** semaphore is a one-space garage (mutex behavior: only one car inside). The System V `sem_op==0` variant is "wait until the lot is completely empty" — useful as a barrier.

## 6. Real-World Analogy
**A single bathroom with a key**: only one person can be inside (binary semaphore). Whoever wants in takes the key (wait/decrement); if someone else has it, they queue (block); when done they hand it back (post/increment). Unlike a mutex, though, semaphores don't enforce *who* returns the key — a friend could return it for you (any process can post) — which is flexible but demands discipline.

**A restaurant with N tables**: the semaphore counts free tables. Groups wait until a table frees; seating decrements, finishing a meal increments. That's a counting semaphore — a mutex can only say "in/out", not "4 of 8 available."

## 7. Formal Definition
**System V**: `int semget(key_t key, int nsems, int flags)` → semaphore set id. `int semop(int semid, struct sembuf *sops, unsigned nsops)` where each `sembuf = { unsigned short sem_num; short sem_op; short sem_flg; }` — `sem_flg` includes `IPC_NOWAIT` and `SEM_UNDO`. The operation is **atomic as a batch**. `int semctl(int semid, int semnum, int cmd, ...)` (`IPC_SET/GETVAL/GETPID/GETNCNT/SETVAL/...`). Kernel structure: `struct sem_array { struct sem sem_array[]; }` with per-sem wait queues; per-namespace limits (`semmni`, `semmsl`, `semopm`, `semmns`).
**POSIX**: `sem_t *sem_open(const char *name, int oflag, mode_t mode, unsigned value)`; `int sem_wait(sem_t*)`; `int sem_trywait`; `int sem_timedwait`; `int sem_post`; `int sem_getvalue`; `int sem_close`; `int sem_unlink`. Unnamed: `int sem_init(sem_t*, int pshared, unsigned value)`; `int sem_destroy`. On Linux, implemented over `futex(2)` with the value stored in the `sem_t`; named semaphores appear as files in `semfs` (usually mounted `/dev/shm`/`/tmp`).

## 8. Example
Bounded producer–consumer with shared memory + a mutex semaphore + two counting semaphores:
```c
// setup (both processes)
sem_t *mutex = sem_open("/mutex", O_CREAT, 0666, 1);   // binary: protect buffer
sem_t *empty = sem_open("/empty", O_CREAT, 0666, N);   // N free slots
sem_t *full  = sem_open("/full",  O_CREAT, 0666, 0);   // 0 filled slots

// producer
while (1) {
    produce(item);
    sem_wait(empty);        // claim a slot
    sem_wait(mutex);        // enter critical section
    buffer[put] = item;     // write into shared memory
    sem_post(mutex);
    sem_post(full);         // signal a filled slot
}
// consumer
while (1) {
    sem_wait(full);         // wait for a filled slot
    sem_wait(mutex);
    item = buffer[get];
    sem_post(mutex);
    sem_post(empty);        // free a slot
    consume(item);
}
```
The `mutex` serializes the buffer access; `empty`/`full` provide flow control. This is the textbook bounded-buffer (Part 04) done with process-shared semaphores.

System V binary semaphore: `semget(key, 1, IPC_CREAT|0666)`, `semctl(semid, 0, SETVAL, 1)`, then `struct sembuf p = {0, -1, 0}; semop(semid, &p, 1);` (acquire), `struct sembuf v = {0, +1, 0}; semop(semid, &v, 1);` (release).

## 9. Internal Working
1. **System V** `semget` → `newary` (alloc `struct sem_array`, `sems` array) → key→id via `ipcget`. `semop` → `do_semtimedop`: validate all ops, simulate; if any would block and `IPC_NOWAIT` → return `EAGAIN` (atomic all-or-nothing); else update values, enqueue on wait queues (`sem->sem_waiter`), schedule. On wake, re-check (spurious wakeups) — re-run the whole batch. `SEM_UNDO`: record in `struct sem_undo` list, applied at exit → **no leaked lock after crash**.
2. **POSIX named** `sem_open` → `do_sem_open` in `ipc/sem.c` (kernel) / `sem_open` (glibc) — creates a file in `semfs`/tmpfs storing the `sem_t`. `sem_wait` → glibc calls `futex(addr, FUTEX_WAIT_BITSET|PRIVATE...)` when the value is 0; `sem_post` → `futex(FUTEX_WAKE)`. Uncontended fast path is a single `cmpxchg` — **no syscall at all**.
3. Unnamed (pshared=1): the `sem_t` must live in shared memory; `sem_init` sets value; wait/post use futex on that address.
4. All are per IPC-namespace (SysV) / per-mount (POSIX semfs) for container isolation.

## 10. Time Complexity
- Uncontended POSIX semaphore: O(1) atomic op — **no syscall** (futex fast path).
- Contended: one futex syscall — O(1) wait-queue ops (wakeup).
- System V `semop`: O(nsops × nsems) validation + O(1) value update + wait-queue — batch atomic.
- `sem_timedwait`: bounded wait via timeout.
- SEM_UNDO bookkeeping: O(undo list) per semop.

## 11. Advantages
- **Cross-process**: works between unrelated processes (named POSIX, keyed SysV).
- **Counting**: express "N available" (vs binary mutex).
- **Atomic batches** (SysV `semop`): multiple resources acquired/released atomically → deadlock-avoidance building block.
- **SEM_UNDO**: auto-release on process death → crash-safe locking.
- **Futex-backed** (POSIX): fast path is lock-free user space — cheap when uncontended.
- **Standardized**: both families are POSIX/SUSv2 standardized.

## 12. Disadvantages
- **No ownership**: anyone can `sem_post` — misuse (double post) is a bug source (vs mutex ownership check).
- **Priority/fairness**: waiters are FIFO per queue, but there's no strict priority; sysv semops have no timeout by default (SysV: `semtimedop` exists; POSIX: `sem_timedwait`).
- **System V complexity**: `semop` semantics (negative/zero ops, SEM_UNDO) are easy to misuse; the API is dated.
- **Naming/keys**: `ftok` collisions; POSIX names must be cleaned up (`sem_unlink`) or they leak in semfs.
- **Performance under heavy contention**: futex syscalls + wakeups cost; spinlocks/RCU sometimes better for very short critical sections.
- **Deadlocks still possible**: two semaphores acquired in different orders across processes → classic deadlock (Part 05).

## 13. Interview Questions
1. **Q: What is an IPC semaphore?** A: A kernel-backed counter used by processes for synchronization — `sem_wait` decrements (blocks if 0), `sem_post` increments; binary (0/1) = mutex-like, counting (N) = resource limit.
2. **Q: System V vs POSIX semaphores?** A: System V: `semget`/`semop`/`semctl` — arrays, atomic multi-ops, SEM_UNDO. POSIX: `sem_open`/`sem_wait`/`sem_post` — named or unnamed, futex-backed, thread + process capable.
3. **Q: Semaphore vs mutex?** A: A mutex has *ownership* (only the lock-holder can unlock) and is binary; a semaphore has no ownership and can count > 1. Semaphores are for resource counting / cross-process; mutexes for protected sections.
4. **Q: Why do processes need semaphores, not just pthread mutexes?** A: A default pthread mutex is process-private (threads only); cross-process sync needs a shared/process-shared primitive — POSIX named semaphores (or PTHREAD_PROCESS_SHARED mutexes) fill that gap.
5. **Q: What is the bounded-buffer problem and how do semaphores solve it?** A: Producer fills a fixed buffer, consumer drains it. Three semaphores: `mutex` (binary, buffer access), `empty=N` (free slots), `full=0` (filled slots); the producer waits `empty` and posts `full`, the consumer waits `full` and posts `empty` — correct flow control without busy-waiting.
6. **Q: What does `sem_op == 0` do in System V?** A: Blocks until the semaphore's value is 0 — useful for barriers ("wait until all units are released").
7. **Q: What is SEM_UNDO?** A: A flag on System V `semop` so the kernel auto-reverts the op if the process dies — preventing a dead process from leaving a held semaphore forever (crash-safe locking).
8. **Q: What is the POSIX semaphore fast path?** A: Uncontended `sem_post`/`sem_wait` are plain atomic ops (futex) — **no syscall**; only when the value hits 0 does it call `futex(2)` to sleep/wake.
9. **Q: Named vs unnamed POSIX semaphores?** A: Named (`sem_open`): usable by unrelated processes via `/name`, persist until `sem_unlink`. Unnamed (`sem_init`): `pshared=0` for threads, `pshared=1` (in shared memory) for processes.
10. **Q: Can semaphores deadlock?** A: Yes — acquiring two semaphores in different orders across processes is the classic deadlock; SEM_UNDO doesn't fix order-based deadlock, only crash leaks.
11. **Q: What's the difference between `sem_trywait` and `sem_wait`?** A: `trywait` returns `EAGAIN` immediately if the value is 0 (nonblocking); `wait` blocks; `timedwait` blocks with a deadline.
12. **Q: How do containers isolate semaphores?** A: System V semaphores are per IPC namespace (key space isolated); POSIX named semaphores live in the mount namespace's semfs — container processes can't touch the host's.

## 14. Follow-Up Questions
1. **Q: What is the difference between a semaphore and a condition variable?** A: A condition variable has no value/state — it signals events and must pair with a mutex; a semaphore *is* state (a count). CVs can't be used alone across processes as cleanly.
2. **Q: What is a futex?** A: Fast user-space mutex — atomic wait/wake on a shared word; `futex_wait` sleeps only when contended, `futex_wake` wakes. The building block under POSIX semaphores, pthread mutexes, and `rcu`.
3. **Q: What are the SysV limits?** A: `SEMMNI` (max sets), `SEMMSL` (max semaphores/set), `SEMOPM` (max ops per semop), `SEMMNS` (total) — sysctls under `kernel.sem`.
4. **Q: When to prefer file locks vs semaphores?** A: File locks (flock/fcntl) when the resource is a file and you want OS-managed release-on-close; semaphores when you need counting + arbitrary-process coordination.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <semaphore.h>
#include <sys/stat.h>
#include <unistd.h>
#include <sys/wait.h>

#define N 8

int main(void) {
    sem_t *mutex = sem_open("/bq_mutex", O_CREAT, 0666, 1);
    sem_t *empty = sem_open("/bq_empty", O_CREAT, 0666, N);
    sem_t *full  = sem_open("/bq_full",  O_CREAT, 0666, 0);
    int fd = shm_open("/bq_buf", O_CREAT | O_RDWR, 0666);
    ftruncate(fd, N * sizeof(int));
    int *buf = mmap(NULL, N * sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    pid_t pid = fork();
    if (pid == 0) {                       // producer
        for (int i = 0; i < 100; i++) {
            sem_wait(empty); sem_wait(mutex);
            buf[i % N] = i;               // place item
            sem_post(mutex); sem_post(full);
        }
        _exit(0);
    }
    // parent: consumer
    int last = -1;
    for (int i = 0; i < 100; i++) {
        sem_wait(full); sem_wait(mutex);
        last = buf[i % N];                // take item
        sem_post(mutex); sem_post(empty);
    }
    wait(NULL);
    printf("consumed last=%d, all 100 items accounted\n", last);

    munmap(buf, N * sizeof(int));
    shm_unlink("/bq_buf");
    sem_unlink("/bq_mutex"); sem_unlink("/bq_empty"); sem_unlink("/bq_full");
    return 0;
}
```

## 16. Industry Usage
- **Linux kernel**: `ipc/sem.c` (System V), `ipc/sem.c` + glibc (`sem_wait`→futex), `kernel/futex.c`, `include/uapi/linux/sem.h`; semfs via tmpfs.
- **glibc / nptl**: pthread mutexes and POSIX semaphores share the futex implementation.
- **Middleware**: boost.interprocess (named semaphores), Qt, Apache, Redis (no — Redis uses its own; but classic server processes use semaphores for singleton locks).
- **Databases**: PostgreSQL uses semaphores historically (PGSemaphore) for lock manager; MySQL uses mutexes; many DBs still use `semget`/`sem_open` for cross-process locks.
- **Embedded/RTOS**: semaphores are the core primitive (VxWorks, QNX, FreeRTOS).
- **Containers**: per-namespace IPC isolation; systemd-managed `sem` namespace for session scoping.

## 17. References
- `man 2 semget`, `man 2 semop`, `man 2 semctl`, `man 7 sysvipc`.
- `man 3 sem_open`, `man 3 sem_wait`, `man 3 sem_post`, `man 3 sem_init`, `man 3 sem_unlink`, `man 7 sem_overview`.
- Silberschatz, *Operating System Concepts*, Ch. 6 (synchronization tools: semaphores), Ch. 3.5.
- Tanenbaum, *Modern Operating Systems*, Ch. 2.4 (semaphores), Ch. 3.2 (IPC).
- Linux `Documentation/sysctl/kernel.rst` (sem limits), `Documentation/userspace-api/sysvipc.rst`.

## 18. Cheat Sheet
- Binary semaphore = mutex-like; counting = resource count.
- System V: `semget` → `semop` (batch, atomic) → `semctl`; SEM_UNDO.
- POSIX: `sem_open("/n", O_CREAT, 0666, v)` → `sem_wait`/`sem_post` → `sem_unlink`.
- Unnamed: `sem_init(&s, pshared, v)`; pshared=1 → shared memory.
- Bounded buffer: `mutex=1, empty=N, full=0`.
- No ownership: anyone can post (be disciplined).
- Futex fast path: no syscall uncontended.
- Deadlock possible: order of acquisition matters.

## 19. Quiz
1. Semaphore used across processes? a) pthread mutex b) POSIX named sem c) spinlock d) signal → **b**
2. Counting semaphore value 0 means? a) locked b) N resources c) blocked wait d) deadlock → **c** (sem_wait blocks)
3. SEM_UNDO protects against? a) deadlock b) crash-held locks c) starvation d) priority → **b**
4. Bounded buffer uses which count? a) mutex only b) empty=N/full=0 c) one semaphore d) spinlock → **b**
5. POSIX uncontended op cost? a) syscall b) atomic op, no syscall c) copy d) IRQ → **b**
6. Mutex vs semaphore key difference? a) value b) ownership c) speed d) process → **b**

## 20. Flashcards
- **Q: Semaphore?** → **A:** Kernel counter; wait decrements/blocks, post increments.
- **Q: SysV API?** → **A:** semget/semop/semctl; arrays, SEM_UNDO.
- **Q: POSIX API?** → **A:** sem_open/sem_wait/sem_post; named + unnamed.
- **Q: Bounded buffer?** → **A:** mutex=1, empty=N, full=0.
- **Q: No ownership means?** → **A:** Any process can post — discipline required.
- **Q: Fast path?** → **A:** Futex — atomic op, syscall only on contention.

## 21. Revision
IPC semaphores give cross-process synchronization — the piece shared memory is missing. System V offers semaphore *arrays* with atomic batched `semop` (negative = acquire, positive = release, zero = barrier) plus SEM_UNDO for crash-safe release; POSIX offers named (`sem_open`) and unnamed (`sem_init`) semaphores implemented on futexes, so the uncontended fast path is a single atomic op with no syscall. The bounded-buffer pattern (mutex + two counting semaphores) is the canonical use and the interview favorite. Unlike a mutex, semaphores have no ownership, so they're flexible but require discipline — and acquiring them in inconsistent order across processes still deadlocks (Part 05). Use them to make Section 03's shared memory safe.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is an IPC semaphore?" | 13 Q1 / 2 How |
| "SysV vs POSIX semaphores?" | 13 Q2 / 7 Formal |
| "Semaphore vs mutex?" | 13 Q3 / 2 How |
| "Why process-shared primitives?" | 13 Q4 / 1 Why |
| "Bounded-buffer solution?" | 13 Q5 / 8 Example |
| "What is SEM_UNDO?" | 13 Q7 / 9 Internal |
| "Futex fast path?" | 13 Q8 / 9 Internal |
| "Can semaphores deadlock?" | 13 Q10 / 12 Disadvantages |
