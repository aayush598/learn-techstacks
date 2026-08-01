# Section 01: The Critical-Section Problem

> **TL;DR**: A critical section is a stretch of code that modifies shared data; it must run atomically with respect to other threads. The critical-section problem asks: how do we guarantee mutual exclusion (one thread inside at a time), progress (someone eventually gets in), and bounded waiting (no infinite bypass)? Getting any of these wrong = race condition = corrupted data.

## 1. Why Does This Exist?
Threads share the address space (Part 02) and preemptive scheduling can switch the CPU between any two instructions (Part 03). So two threads can interleave a read-modify-write like `count++` in arbitrary order, producing wrong results — a **race condition**. The critical-section problem is the formal statement of the fix: identify the shared-data region, ensure only one thread enters at a time, guarantee progress and bounded waiting. Without this, every shared structure (queues, caches, files) corrupts under concurrency.

## 2. How Does It Work?
- **Entry section**: request permission to enter the critical section (lock).
- **Critical section**: modify shared data — must be atomic w.r.t. other threads.
- **Exit section**: release the permission (unlock).
- **Remainder section**: the rest of the thread's work.
The requirements: (1) **Mutual exclusion** — no two threads in their critical sections simultaneously; (2) **Progress** — if no thread is in a critical section and some want to enter, the decision cannot be postponed indefinitely; (3) **Bounded waiting** — there's a bound on how many times other threads can enter before a given waiting thread gets in.

## 3. When Is It Used?
- Every time shared data is touched by >1 thread: in-process (global vars, heaps, caches), cross-process (mmap shared memory, database rows), kernel (task lists, page tables, network buffers).
- The *pattern* generalizes beyond memory: files, DB transactions, distributed locks.

## 4. Why Wasn't Another Approach Chosen?
- **No synchronization (raw races)**: corrupt data, crashes — rejected.
- **Global disable-preemption / single CPU**: safe but kills concurrency (other CPUs still race), rejected for SMP.
- **Per-instruction atomicity**: impossible in general (operations span many instructions; you'd have to make the whole section atomic — that's what locks do, but blocking other CPUs is wasteful).
- **Copy-on-write / no sharing**: the purest solution (functional/data-parallel designs), but general mutable shared state is unavoidable.
So we accept locks/synchronization as the cost of shared mutable state.

## 5. Intuition
A **shared notebook**: two writers updating the same page. If both write simultaneously, the page ends up with interleaved scribbles (race). The critical section is "the time you're writing on the page." The rule "only one pen on the page at once" = mutual exclusion. "The next person waiting is allowed in promptly" = progress. "No one can bypass you repeatedly" = bounded waiting.

## 6. Real-World Analogy
**A single checkout counter**: the counter transaction (reading balance, deducting, writing balance) is the critical section. Two customers deducting from the same account concurrently = a race that can produce a negative balance. The cashier (lock) lets one customer transact at a time (mutual exclusion), the next in line gets served without unfair bypassing (bounded waiting), and as long as someone is waiting, the cashier serves them (progress).

## 7. Formal Definition
- **Race condition**: the outcome of concurrent execution depends on the scheduling/interleaving order — nondeterministic, data corruption.
- **Critical section**: the code segment where shared data is accessed.
- A correct solution satisfies:
  - **Mutual exclusion (ME)**: if P_i is in its CS, no other P_j can be.
  - **Progress**: if no thread is in CS and some threads want in, the choice of who enters cannot wait forever; a thread not in its remainder cannot block others' decisions.
  - **Bounded waiting**: there exists a bound k on the number of times other threads may enter their CS before a requesting thread does.
- (Sometimes listed: **atomicity** — the section appears indivisible.)

## 8. Example
Two threads do `count++` where count starts at 0. In assembly: load count; add 1; store count.
- Interleave: T1 loads 0; T2 loads 0; T1 stores 1; T2 stores 1 → final count = 1, but two increments happened → lost update (race).
- With a mutex around it: only one thread runs the 3-instruction sequence at a time → final = 2. Correct.

## 9. Internal Working
1. Thread enters entry section → tries to acquire lock (e.g., spin on a flag or block in a futex wait).
2. Lock guarantee: the acquire/release operations themselves are **atomic** (hardware TAS/CAS — next section) so two threads can't both "win" the lock.
3. Only the winner executes the CS; the loser waits (spins, or sleeps after a futex wait).
4. On exit, release → wakes a waiter.
5. Correctness is verified by ensuring the four requirements hold under all interleavings; violations = deadlock (nobody proceeds), livelock (everyone busy), or races.

## 10. Time Complexity
- Uncontended lock acquire/release: ~O(1) + atomic op cost (tens of ns) + possible cache-line traffic.
- Contended: wait time depends on the algorithm (spin: busy; sleep: wakeup cost).
- Critical section length is the real cost — keep it short.
- Software solutions (Peterson's) are O(1) but rely on memory-order subtleties and don't scale.

## 11. Advantages
- Simple, uniform mental model for protecting shared data.
- Correctness criteria are testable (ME/progress/bounded waiting).
- Building block for all higher primitives (semaphores, monitors, queues).
- Works across threads and processes (kernel mutexes, shared memory).

## 12. Disadvantages
- Locks serialize → contention kills scalability (Amdahl's law).
- Deadlock risk (two locks, wrong order).
- Performance cliff under high contention (cache-line ping-pong).
- Priority inversion (needs inheritance) and convoy effects.
- Programmer must place entry/exit correctly — a missing unlock is a bug.

## 13. Interview Questions
1. **Q: What is a race condition?** A: When the outcome of concurrent execution depends on the interleaving order — e.g., two threads doing read-modify-write on `count` lose updates. Result is nondeterministic data corruption.
2. **Q: What is a critical section?** A: The code region where shared data is accessed and must run atomically w.r.t. other threads.
3. **Q: What are the requirements for a correct solution?** A: Mutual exclusion, progress, bounded waiting (and the entry/exit structure).
4. **Q: Explain mutual exclusion.** A: At most one thread executes its critical section at any time; others must wait outside.
5. **Q: What is progress?** A: If the CS is free and some threads want to enter, the decision of who enters cannot be postponed indefinitely — no thread outside its CS can block the choice.
6. **Q: What is bounded waiting?** A: There's a bound on how many times other threads can enter their CS before a given waiting thread is admitted — prevents starvation-by-bypass.
7. **Q (TRICKY): Why can't you just disable interrupts to solve it?** A: On a uniprocessor it works (preemption can't interrupt), but SMP: another CPU can run the same CS concurrently — interrupts don't cross CPUs. So hardware atomics/locks are needed on multicore.
8. **Q: What is the entry/exit structure?** A: Entry section (request permission), CS, exit section (release), remainder. The lock/unlock pattern.
9. **Q (SCENARIO): `count++` in two threads, count ends at 1. Explain.** A: Both threads loaded 0 before either stored — interleaved read-modify-write; the increments "lost" an update. This is the classic race.
10. **Q: What's the difference between a critical section and a lock?** A: The critical section is the *protected code*; the lock is the *mechanism* enforcing mutual exclusion around it. Critical sections are entered/exited; locks are acquired/released.
11. **Q: Why is it important to keep critical sections short?** A: Contention time = time other threads wait; long CS hurts throughput and response; also increases deadlock/priority-inversion exposure.
12. **Q: What happens if a thread forgets the exit section (unlock)?** A: Deadlock — other threads wait forever (or until timeout); the shared data is frozen. That's why RAII/`finally` unlock patterns exist.

## 14. Follow-Up Questions
1. **Q: What is a "lock-free" guarantee?** A: At least one thread always makes progress (no blocking); related to progress guarantees (obstruction-freedom, lock-freedom, wait-freedom) — covered in Part 04 Ch 4.
2. **Q: What is the difference between mutual exclusion and atomicity?** A: ME = one thread at a time in CS; atomicity = the CS appears indivisible (which ME provides, if the solution is correct).
3. **Q: Can a race happen in single-threaded code?** A: Not within one thread — but signal handlers, DMA, or hardware concurrent access can still race with the main thread.
4. **Q: What is a "lost update"?** A: Two read-modify-write sequences where both read the old value and write; one update is overwritten — the archetypal race outcome.
5. **Q: How do databases relate to critical sections?** A: DB transactions extend the idea with atomicity/consistency/isolation/durability (ACID); a row lock is a CS over a row.

## 15. Coding Example
```c
/* The archetypal race: unsynchronized increment */
#include <pthread.h>
#include <stdio.h>

#define N 1000000
long counter = 0;

void *worker(void *arg) {
    for (int i = 0; i < N; i++) counter++;   /* read-modify-write */
    return NULL;
}

int main(void) {
    pthread_t t[2];
    pthread_create(&t[0], NULL, worker, NULL);
    pthread_create(&t[1], NULL, worker, NULL);
    pthread_join(t[0], NULL);
    pthread_join(t[1], NULL);
    printf("expected %ld, got %ld\n", 2L * N, counter); /* < 2M */
    return 0;
}
```
```c
/* Fixed with a mutex (entry/exit sections) */
#include <pthread.h>

long counter = 0;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

void *worker(void *arg) {
    for (int i = 0; i < N; i++) {
        pthread_mutex_lock(&m);    /* entry section */
        counter++;                 /* critical section */
        pthread_mutex_unlock(&m);  /* exit section */
    }
    return NULL;
}
```

## 16. Industry Usage
- **Kernel**: every shared structure (task list, page tables, filesystem) is a critical section protected by spinlocks/mutexes.
- **Databases**: row/table locks = CS over rows; MVCC avoids them for reads.
- **Applications**: caches, counters, queues, reference counting, in-flight request tracking.
- **Concurrency frameworks**: Java synchronized, Go channels, Rust std::sync — all build on this problem.
- **Interview angle**: virtually every concurrency question traces back to these four requirements.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 7.1 (Critical-section problem).
- Dijkstra, "Solution of a problem in concurrent programming control" (1965).
- Tanenbaum, *Modern OS*, Ch. 2.3.
- Herlihy & Shavit, *The Art of Multiprocessor Programming*.

## 18. Cheat Sheet
- Race = result depends on interleaving.
- CS structure: entry → CS → exit → remainder.
- Requirements: mutual exclusion, progress, bounded waiting.
- ME: one thread in CS at a time.
- Progress: free CS + waiting threads ⇒ someone enters soon.
- Bounded waiting: bound on bypasses (no starvation).
- Lost update = archetypal race (read-modify-write).
- Interrupt disable ≠ SMP-safe.
- Keep CS short.
- Forget unlock ⇒ deadlock.

## 19. Quiz
1. A race occurs when: a) two threads sleep b) output depends on interleaving c) locks held d) no locks → **b**
2. Mutual exclusion means: a) one thread at a time in CS b) all threads in CS c) fast d) no locks → **a**
3. Progress requires: a) immediate entry b) no infinite postponement c) bounded waiting d) lock-free → **b**
4. Bounded waiting: a) bound on bypasses b) bound on CPU c) no waiting d) immediate → **a**
5. Interrupt-disable fixes: a) SMP b) uniprocessor c) both d) nothing → **b**
6. `count++` needs: a) memory b) read-modify-write atomicity c) CPU d) I/O → **b**
7. Forgetting unlock: a) race b) deadlock c) fast d) priority → **b**
8. The protected code is: a) lock b) critical section c) entry d) thread → **b**
9. Race outcome is: a) deterministic b) nondeterministic c) always correct d) fast → **b**
10. Long CS hurts: a) memory b) scalability/contention c) I/O d) threads → **b**

## 20. Flashcards
- **Q: Race condition?** → **A:** Outcome depends on interleaving.
- **Q: Critical section?** → **A:** Protected shared-data region.
- **Q: Requirements?** → **A:** ME, progress, bounded waiting.
- **Q: Mutual exclusion?** → **A:** One in CS at a time.
- **Q: Progress?** → **A:** No infinite postponement.
- **Q: Bounded waiting?** → **A:** Bound on bypasses.
- **Q: Lost update?** → **A:** Overwritten read-modify-write.
- **Q: Interrupt disable?** → **A:** Uni-CPU only.
- **Q: No unlock?** → **A:** Deadlock.

## 21. Revision
The critical-section problem formalizes protecting shared data: code touching shared state must be enclosed (entry/CS/exit/remainder) and satisfy mutual exclusion (one at a time), progress (no infinite postponement), and bounded waiting (no starvation-by-bypass). Races happen when interleavings corrupt shared data — the lost-update pattern. Interrupt disabling only works uniprocessor; SMP needs atomic instructions and locks. All higher primitives (Part 04 Ch 2) build on these requirements.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a race condition?" | 13 Q1 / 5 Intuition / 8 Example |
| "What is a critical section?" | 13 Q2 / 7 Formal Definition |
| "Requirements for correctness?" | 13 Q3 / 7 Formal Definition |
| "What is mutual exclusion?" | 13 Q4 / 7 Formal Definition |
| "What is progress?" | 13 Q5 / 7 Formal Definition |
| "What is bounded waiting?" | 13 Q6 / 7 Formal Definition |
| "Why not disable interrupts?" | 13 Q7 / 4 Why Wasn't Another Approach Chosen |
| "Explain the lost update" | 13 Q9 / 8 Example |
| "Critical section vs lock?" | 13 Q10 / 7 Formal Definition |
| "What if unlock is forgotten?" | 13 Q12 / 12 Disadvantages |
