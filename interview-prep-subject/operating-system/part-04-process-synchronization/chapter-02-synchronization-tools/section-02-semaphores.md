# Section 02: Semaphores

> **TL;DR**: A semaphore is a counter with two atomic operations — `wait` (down, decrement, block if 0) and `signal` (up, increment, wake a waiter). Binary semaphores do mutual exclusion; counting semaphores do resource-pool accounting and signal/coordination between threads.

## 1. Why Does This Exist?
Mutexes only express "one at a time." Real synchronization needs *counting*: a pool of N buffers, N tickets, or "this event happened" signals. A semaphore exists to generalize the lock into a counter — `wait`/`signal` make counting, resource limiting, and inter-thread signaling trivial. It was Dijkstra's original primitive (P and V), and it remains the standard for controlling access to a finite set of resources.

## 2. How Does It Work?
- State: an integer `S` ≥ 0 + a wait queue.
- `wait(S)` (P, down, acquire): atomically `if (S > 0) S--; else block (enqueue)`.
- `signal(S)` (V, up, release): atomically `S++; if (waiters) wake one`.
- **Binary semaphore**: S ∈ {0,1} — used as a mutex-like lock (but no ownership).
- **Counting semaphore**: S = pool size — used to limit concurrent access to N resources.
- **Signaling**: one thread does signal, another does wait — producer→consumer handoff.

## 3. When Is It Used?
- **Resource pools**: limit connections (max 10 DB connections), N buffers (producer-consumer), ticket counters.
- **Signaling/event notification**: thread B blocks until thread A signals done.
- **Ordering**: force a sequence (T2 waits until T1 finishes).
- **Reader/writer counting** variants, throttling (bounded concurrency).

## 4. Why Wasn't Another Approach Chosen?
- **Mutex**: only one at a time — can't limit to N=5 resources or signal events. Rejected for counting.
- **Condition variables**: perfect for *state*, but signaling CVs without a predicate is error-prone; semaphore's built-in count is simpler for pools/events.
- **Busy-wait counters**: waste CPU; semaphores sleep waiters. 
- **Monitors**: language-level; semaphore is the portable kernel/userland primitive.
The semaphore wins for *counting + blocking + signaling* in one tiny primitive — at the cost of requiring the programmer to get ordering right (unlike monitors).

## 5. Intuition
**A parking garage with N spots**: a counter tracks free spots. `wait` = enter (decrement; if 0, wait outside until a car leaves). `signal` = exit (increment; if cars waiting, let one in). N=1 → a single-spot garage (binary semaphore = mutual exclusion). The counter *is* the resource availability.

## 6. Real-World Analogy
**A row of N identical washing machines in a laundromat**: to start a wash you `wait` for a free machine (decrement the counter; if all N busy, sit and wait). When done you `signal` (increment; the next waiting person proceeds). The machine-count semaphore throttles concurrent "users." A *signaling* semaphore is like a doorbell: one person presses (signal), another who was waiting (wait) knows to proceed — the count (1) is a flag, not a resource.

## 7. Formal Definition
- **Semaphore**: an integer S and atomic operations:
  - `wait(S)`: while (S ≤ 0) block; S--;
  - `signal(S)`: S++; if (blocked waiters) wake one.
- **Binary semaphore**: S ∈ {0,1}; wait blocks when S=0; signal sets S=1 and wakes.
- **Counting semaphore**: S ≥ 0 unbounded (or N).
- **Classical**: P(S) = wait (proberen, "try"); V(S) = signal (verhogen, "increment") — Dijkstra.
- Used for mutual exclusion (binary) and **synchronization** (signaling/counting).

## 8. Example
**Signaling** (thread ordering):
```
T1: do work; signal(S);        // S starts 0
T2: wait(S); continue;         // blocks until T1 signals
```
T2 won't proceed before T1 finishes — ordering guaranteed.

**Counting semaphore, N=3** (pool):
```
wait(S); use_resource(); signal(S);   // at most 3 concurrent users
```
S starts 3; three threads pass, the 4th waits until one signals.

## 9. Internal Working
1. Implementation: kernel object (SysV `semget/semop`, POSIX `sem_init/sem_wait/sem_post`) or userland `futex`-based (glibc semaphores).
2. `sem_wait` fast path: `cmpxchg` decrement; if result < 0 → futex wait (blocked).
3. `sem_post` fast path: atomic increment; if old value < 0 (waiters exist) → futex wake.
4. Negative value convention: value < 0 means |value| threads are blocked waiting.
5. SysV semaphores are arrays (can adjust multiple, undo); POSIX named semaphores work across processes via shared memory.

## 10. Time Complexity
- Fast path (no contention): O(1) atomic op.
- Contended: futex wait/wake → O(1) syscall + scheduler wake.
- Pool of N: each wait/signal O(1); throughput bounded by contention on the counter's cacheline.

## 11. Advantages
- One primitive covers mutual exclusion AND counting AND signaling.
- Blocking waiters (no CPU waste).
- Works cross-process (named POSIX/SysV semaphores).
- O(1) fast path.
- Elegant solution to bounded-buffer / resource pools.

## 12. Disadvantages
- **No ownership**: any thread can signal — wrong ordering bugs are easy.
- **Mixing mutex and signaling** semantics confuses programmers (misused semaphore = deadlock or race).
- **Vulnerable to deadlock** if wait order is wrong (classic: two semaphores acquired in different order).
- Hard to debug (state is a bare counter).
- Unbalanced wait/signal → counter drifts, blocks forever.

## 13. Interview Questions
1. **Q: What is a semaphore?** A: A counter with atomic wait (down/decrement, block if 0) and signal (up/increment, wake a waiter). Binary → exclusion; counting → pools; used for signaling too.
2. **Q: Mutex vs semaphore?** A: Mutex = ownership, exclusion only; semaphore = no owner, counting + signaling. Use mutex for protecting data, semaphore for resource pools/events.
3. **Q: Binary semaphore as mutex — OK?** A: Works mechanically but no ownership — any thread can signal it (unlock someone else's "lock"), enabling misuse; a true mutex is safer for exclusion.
4. **Q (TRICKY): S=0, two threads wait(S). Third signals once. How many proceed?** A: One — signal wakes exactly one waiter (S becomes 1 from -2 → -1, one wakes, then still 1 blocked). Semaphores wake one, not all.
5. **Q: How does a counting semaphore limit a pool?** A: Init S=N; wait to acquire, signal to release — at most N threads hold resources at once.
6. **Q: What is the negative-value convention?** A: S < 0 means |S| threads are blocked waiting; signal increments (reducing the wait count).
7. **Q: How does signal ordering work between threads?** A: T2's wait(S) blocks; T1's signal(S) wakes it — establishes a happens-before/ordering (T2 proceeds only after T1).
8. **Q: What's a named semaphore?** A: A POSIX semaphore with a name shared across processes (in /dev/shm) — usable for cross-process pools.
9. **Q: How is a semaphore implemented?** A: Kernel/futex: atomic decrement with cmpxchg; if negative → futex wait; signal increments and futex wakes if waiters.
10. **Q (SCENARIO): Implement "only 5 concurrent downloads."** A: Counting semaphore S=5; each download thread does sem_wait at start, sem_post at end — at most 5 active.
11. **Q: What happens if you forget a signal?** A: A waiter blocks forever (count never replenished) — deadlock/starvation. Balanced wait/signal is mandatory.
12. **Q (TRICKY): Can a semaphore be used for mutual exclusion across processes?** A: Yes — SysV/POSIX named semaphores live in shared memory, so processes can share a semaphore and exclude each other.

## 14. Follow-Up Questions
1. **Q: What is the "producer-consumer" semaphore setup?** A: full = 0, empty = N; producer: wait(empty), produce, signal(full); consumer: wait(full), consume, signal(empty).
2. **Q: SysV vs POSIX semaphores?** A: SysV: semget/semop arrays with undo; POSIX: sem_init/sem_wait — simpler, thread-safe, preferred in modern code.
3. **Q: What is a "semaphore as a latch"?** A: Init to 0; N threads wait; a controller signals N times → all release at once (rendezvous barrier).
4. **Q: Why do OS courses love semaphores?** A: They express mutual exclusion, counting, and ordering in one tiny primitive — the classic problems (bounded buffer, readers-writers) have clean semaphore solutions.
5. **Q: What's the downside vs monitors/CV?** A: No structural safety — the compiler can't check that wait/signal pair up; monitors (language-level) eliminate the misuse classes.

## 15. Coding Example
```c
/* POSIX counting semaphore: bounded pool (5 concurrent workers) */
#include <semaphore.h>
#include <pthread.h>
#include <stdio.h>

sem_t pool;
int active = 0;

void *worker(void *arg) {
    sem_wait(&pool);              /* acquire slot */
    active++; printf("active=%d\n", active);
    active--;
    sem_post(&pool);              /* release slot */
    return NULL;
}

int main(void) {
    sem_init(&pool, 0, 5);        /* N=5 */
    pthread_t t[20];
    for (int i = 0; i < 20; i++) pthread_create(&t[i], NULL, worker, NULL);
    for (int i = 0; i < 20; i++) pthread_join(t[i], NULL);
    sem_destroy(&pool);
    return 0;
}
```
```c
/* Signaling: T2 waits until T1 signals done */
sem_t done;
void *t1(void *arg) { printf("T1 working\n"); sem_post(&done); return NULL; }
void *t2(void *arg) { sem_wait(&done); printf("T2 proceeds\n"); return NULL; }
```
```bash
# Named semaphores from the shell / inspect
ls /dev/shm/sem.*
```

## 16. Industry Usage
- **Databases**: connection pools, reader-writer gating (in-memory semaphore limiting pool size).
- **OS**: SysV/POSIX semaphores; Linux kernel uses semaphores historically (now mostly mutexes for exclusion).
- **Networking**: rate limiters (semaphore as token bucket), concurrent-request caps.
- **Producers-consumers**: buffer pools, worker queues, message queues.
- **RTOS**: FreeRTOS binary/counting/mutex semaphores — core API.

## 17. References
- Dijkstra, "Cooperating sequential processes" (1965) — P/V.
- Silberschatz, *OS Concepts*, 7.5 (Semaphores).
- man: `sem_init(3)`, `sem_wait(3)`, `sem_post(3)`, `semget(2)`, `semop(2)`.
- FreeRTOS docs: semaphores.

## 18. Cheat Sheet
- wait (P, down): S>0 ? S-- : block. signal (V, up): S++; wake one.
- Binary S∈{0,1} → exclusion; counting S=N → pool.
- Signaling: signal from producer, wait from consumer (ordering).
- No ownership — any thread can signal.
- S<0 ⇒ |S| blocked waiters.
- Init S=N limits concurrent users to N.
- Named semaphores: cross-process (POSIX/SysV).
- Forgot signal → permanent block.
- Full/empty semaphores = bounded buffer solution.

## 19. Quiz
1. wait blocks when: a) S>0 b) S<=0 c) S=1 d) never → **b**
2. signal wakes: a) all b) one waiter c) none d) self → **b**
3. Binary semaphore values: a) any b) 0/1 c) negative d) 2 → **b**
4. S=3 limits pool to: a) 1 b) 3 c) infinite d) 0 → **b**
5. Semaphore ownership: a) yes b) no c) sometimes d) read-only → **b**
6. S=-2 means: a) 2 free b) 2 blocked c) 2 signaled d) 2 dead → **b**
7. POSIX named semaphores: a) thread-only b) cross-process c) kernel-only d) GPU → **b**
8. Semaphore signaling establishes: a) exclusion b) ordering c) priority d) memory → **b**
9. Forgot signal causes: a) race b) permanent block c) boost d) fast → **b**
10. Producer-consumer uses: a) full/empty b) one mutex c) spinlock d) no sync → **a**

## 20. Flashcards
- **Q: wait?** → **A:** Decrement; block if S≤0.
- **Q: signal?** → **A:** Increment; wake one.
- **Q: Binary?** → **A:** 0/1 → exclusion.
- **Q: Counting?** → **A:** S=N → pool limit.
- **Q: Ownership?** → **A:** None (any thread can signal).
- **Q: S<0?** → **A:** |S| blocked.
- **Q: Named?** → **A:** Cross-process via /dev/shm.
- **Q: Missed signal?** → **A:** Permanent block.

## 21. Revision
A semaphore is an atomic counter with wait (down: decrement, block if ≤0) and signal (up: increment, wake one). Binary semaphores approximate exclusion but lack ownership; counting semaphores bound resource pools (S=N) and implement signaling/ordering between threads. Implementation uses cmpxchg fast paths and futex sleep/wake (S<0 ⇔ |S| blocked). Correctness requires balanced wait/signal; misuse (unbalanced or wrong-order waits) deadlocks. It's the workhorse for bounded buffers, pools, and latches.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a semaphore?" | 13 Q1 / 7 Formal Definition |
| "Mutex vs semaphore?" | 13 Q2 / 4 Why Wasn't Another Approach Chosen |
| "Binary semaphore as mutex?" | 13 Q3 / 12 Disadvantages |
| "Two wait, one signal?" | 13 Q4 / 8 Example |
| "Pool limiting?" | 13 Q5 / 5 Intuition |
| "Negative convention?" | 13 Q6 / 9 Internal Working |
| "Signaling/ordering?" | 13 Q7 / 8 Example |
| "Only 5 concurrent downloads?" | 13 Q10 / 8 Example |
| "Forgotten signal?" | 13 Q11 / 12 Disadvantages |
| "Cross-process exclusion?" | 13 Q12 / 3 When Is It Used |
