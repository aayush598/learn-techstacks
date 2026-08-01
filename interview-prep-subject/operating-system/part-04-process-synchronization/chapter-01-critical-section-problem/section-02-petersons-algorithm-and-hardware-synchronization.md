# Section 02: Peterson's Algorithm and Hardware Synchronization

> **TL;DR**: Peterson's algorithm is the classic two-thread software solution to the critical-section problem using just shared flags and a turn variable — correct but only for 2 threads and not practically scalable. Real systems use hardware atomic instructions: test-and-set (TAS), compare-and-swap (CAS), and fetch-and-add — which are the atomic building blocks for every lock.

## 1. Why Does This Exist?
Before hardware gave us atomic instructions, researchers asked: *can we solve mutual exclusion in pure software?* Peterson's algorithm answered yes (for two threads) — and it's the clearest illustration of what the four requirements mean. But software-only solutions don't survive preemption/optimization subtleties and don't scale. The hardware answer — atomic read-modify-write instructions — exists to give a *primitive* that cannot be interrupted mid-operation, making locks correct, fast, and multiprocessor-safe.

## 2. How Does It Work?
**Peterson's** (for 2 threads, each i ∈ {0,1}):
1. Set `flag[i] = true` (I want in).
2. Set `turn = j` (I defer to the other).
3. Wait while `flag[j] && turn == j`.
4. Enter CS; on exit `flag[i] = false`.
Invariant: only one thread can pass the wait because `turn` has a single value.

**Hardware**: TAS returns old value and sets to 1 atomically; CAS reads, compares, swaps conditionally atomically. A lock: `while (TAS(&lock, 1) == 1) /* spin */` — only the thread that sees old value 0 wins.

## 3. When Is It Used?
- **Peterson's**: pedagogy (interviews, textbook), tiny embedded/two-processor toy systems.
- **TAS**: classic spinlock implementation (though modern CPUs use more efficient variants like `xchg`/`lock cmpxchg`).
- **CAS**: the workhorse of all modern lock-free programming and lock fast-paths (x86 `lock cmpxchg`, ARM `LDXR/STXR`, Java `AtomicReference`).
- Every OS uses these instructions under the hood for futex fast-path, refcounts, seqlocks.

## 4. Why Wasn't Another Approach Chosen?
- **Pure software (Dekker/Peterson)**: works for 2 threads; generalizing to N is messy; needs memory-ordering care (compilers/CPUs reorder!). Rejected for production.
- **Interrupt disabling**: uniprocessor-only, breaks SMP. Rejected.
- **Locks at language level only**: still need hardware atomics underneath. 
- **Test-and-set with `lock` prefix**: guarantees atomicity by locking the memory bus/cacheline — chosen as the primitive. Later refined: CAS enables *optimistic* synchronization (lock-free), which spinning alone can't.

## 5. Intuition
Peterson's is like **two people politely deferring**: each says "you go first" (`turn = other`) and only enters if the other isn't also claiming to defer and hasn't claimed they want in. The hardware primitive is like **one key that can only be grabbed by one person at a time** — the "grab" (TAS/CAS) is an atomic, uninterruptible action, so no two people can ever both hold the key.

## 6. Real-World Analogy
**A single bathroom key in a gym**: the key (lock) hangs on a hook. TAS = "reach for the key; if it's not there, keep trying" — the grab is one atomic motion, so two people can't both walk out with it. CAS = "check it's the key you expect, then grab; if someone else took it, retry." Peterson's = two roommates, each putting a "busy" sign up and a "your turn" note — works between two people, gets chaotic with more.

## 7. Formal Definition
**Peterson's algorithm** (threads i, j; i ≠ j):
```
flag[i] = true;
turn = j;
while (flag[j] && turn == j) ;  // busy wait
   // critical section
flag[i] = false;
```
Satisfies ME, progress, bounded waiting for exactly 2 threads, given sequential consistency (needs memory barriers in practice).

**TAS**: `boolean test_and_set(boolean *target): old = *target; *target = true; return old;` — atomic.
**CAS**: `boolean compare_and_swap(T *p, T expected, T new): if (*p == expected) { *p = new; return true; } return false;` — atomic.
**FA (fetch-and-add)**: `old = *p; *p += n; return old;` — atomic.

## 8. Example
**TAS spinlock**:
```
lock:
  while (test_and_set(&lock, 1) == 1) ;   // spin
  // CS
unlock:
  lock = 0;
```
Thread A: TAS returns 0 → A owns lock. Thread B: TAS returns 1 → spins. A exits, sets 0; B's next TAS returns 0 → B enters. Correct ME.

**CAS counter (lock-free)**:
```
do {
  old = count;
  new = old + 1;
} while (!compare_and_swap(&count, old, new));
```
If another thread changed count, CAS fails → retry with fresh old. No lock needed.

## 9. Internal Working
1. CPU provides an instruction that does read-modify-write **atomically** — x86: `lock cmpxchg`/`lock xchg` (bus/cacheline locked); ARM: exclusive load-store (`ldxr`/`stxr` loop).
2. TAS sets the lock word to 1 and returns the previous value — the winner sees 0.
3. CAS is "read, compare, write-if-equal" — the workhorse for optimistic sync (retry on failure).
4. Cache coherence (MESI) ensures all CPUs see the update — atomics coordinate via the cacheline's M state.
5. Software must add memory barriers (acquire/release semantics) so non-atomic reads/writes around the CS don't leak — compilers/CPUs reorder otherwise.

## 10. Time Complexity
- TAS/CAS: ~1 atomic op (tens of ns), but contended spinlock causes cache-line ping-pong → O(cache miss latency) per attempt, quadratic contention degradation in the worst case.
- CAS retry loop: amortized O(1) when contention is low; unbounded retries under high contention (mitigated by backoff/queued locks).
- Peterson's: O(1) instructions but with memory-barrier overhead and 2-thread limit.

## 11. Advantages
- **Atomicity guaranteed by hardware** — correct, portable-ish primitives.
- **CAS enables lock-free/wait-free designs** (progress without blocking).
- TAS/CAS fast paths are cheap when uncontended.
- Simple to reason about; foundation of all OS sync.

## 12. Disadvantages
- **TAS spinlocks**: waste CPU spinning; cache-line ping-pong scales terribly; unfair (starvation possible).
- **CAS**: ABA problem (see Part 04 Ch 4), retry loops under contention, requires careful memory ordering.
- Atomic ops are more expensive than plain loads/stores.
- Hardware solutions still need correct memory-barrier placement.
- Not composable by themselves (still need wait queues for efficiency → futexes).

## 13. Interview Questions
1. **Q: Describe Peterson's algorithm.** A: Two shared variables per thread (flag[i]) plus a shared turn; each sets flag[i]=true, turn=j, then waits while flag[j] && turn==j. Satisfies ME/progress/bounded waiting for 2 threads.
2. **Q: Why isn't Peterson's used in production?** A: Limited to 2 threads; requires sequential consistency (needs memory barriers); busy-waits; not scalable. It's a pedagogical solution.
3. **Q: What is test-and-set?** A: An atomic read-modify-write returning the old value and setting to true — the classic spinlock primitive.
4. **Q: What is compare-and-swap?** A: Atomic compare-and-write-if-equal; returns success. The workhorse of lock-free programming.
5. **Q: Why do we need hardware atomics at all?** A: Load/store aren't atomic for read-modify-write across CPUs; preemption and SMP interleavings corrupt shared state. Hardware locks the cacheline/bus so the op is indivisible.
6. **Q (TRICKY): Two threads TAS a lock — can both enter?** A: No — TAS is atomic; exactly one sees old value 0 (the other sees 1 and spins). That atomicity is the entire guarantee.
7. **Q: What's the ABA problem?** A: CAS succeeds when the value matches `expected`, but the value may have changed A→B→A meanwhile — a second CAS can't tell. Fix: version counters/tagged pointers.
8. **Q: What's a spinlock?** A: A lock implemented by busy-waiting on TAS — works only if the CS is short and preemption is managed; wasteful on uniprocessor.
9. **Q (SCENARIO): Implement a lock-free counter with CAS.** A: Loop: read old; compute new; CAS(old→new); retry on failure. Multiple threads converge without blocking.
10. **Q: What's the difference between TAS and CAS?** A: TAS unconditionally sets to 1 and returns old; CAS conditionally writes only if current == expected. CAS is more general (supports optimistic loops).
11. **Q: Why are memory barriers needed around atomics?** A: CPUs/compilers reorder loads/stores; without acquire/release barriers, data written in the CS could be read by another thread before the lock release. Barriers order it.
12. **Q: What happens if a spinlock is held by a thread that gets preempted?** A: Other CPUs spin until the preempted thread runs again — priority inversion and wasted CPU. Kernels disable preemption/use queued locks to bound this.

## 14. Follow-Up Questions
1. **Q: What is an exclusive-load/store pair (ARM)?** A: `LDXR`/`STXR` — load-exclusive, store-exclusive with a monitor; the STXR fails if the line was touched → retry. ARM's CAS equivalent.
2. **Q: What's a "ticket lock"?** A: Fair spinlock using fetch-and-add to get a ticket; threads spin until their number is called — adds bounded waiting to TAS.
3. **Q: What is a "queued lock" (MCS)?** A: Spinning thread queues on a per-thread node → O(1) cache traffic, no ping-pong; Linux uses `queued_spinlock`.
4. **Q: What's the difference between a hardware lock and a mutex?** A: A mutex uses atomics only for the fast path; under contention it *sleeps* (futex). A pure spinlock never sleeps.
5. **Q: What is `cmpxchg` on x86?** A: `lock cmpxchg` — atomic compare-exchange (with 8-byte variant `cmpxchg8b/16b`); CAS's hardware form.

## 15. Coding Example
```c
/* Peterson's algorithm for 2 threads */
#include <pthread.h>
#include <stdbool.h>
#include <stdatomic.h>
#include <stdio.h>

volatile bool flag[2] = {false, false};
volatile int turn;
long counter = 0;

void peterson_entry(int me) {
    int other = 1 - me;
    flag[me] = true;
    turn = other;
    while (flag[other] && turn == other)
        ; /* busy wait */
}
void peterson_exit(int me) { flag[me] = false; }

void *worker(void *arg) {
    int me = (long)arg;
    for (int i = 0; i < 1000000; i++) {
        peterson_entry(me);
        counter++;               /* critical section */
        peterson_exit(me);
    }
    return NULL;
}

int main(void) {
    pthread_t t0, t1;
    pthread_create(&t0, NULL, worker, (void*)0);
    pthread_create(&t1, NULL, worker, (void*)1);
    pthread_join(t0, NULL); pthread_join(t1, NULL);
    printf("counter = %ld\n", counter);
    return 0;
}
```
```c
/* Spinlock with TAS; lock-free counter with CAS (C11 atomics) */
#include <stdatomic.h>

atomic_int lock = 0;
void spin_lock(void) {
    while (atomic_exchange(&lock, 1) == 1) ; /* TAS */
}
void spin_unlock(void) { atomic_store(&lock, 0); }

atomic_int count = 0;
void inc(void) {
    int old, want;
    do { old = atomic_load(&count); want = old + 1; }
    while (!atomic_compare_exchange_weak(&count, &old, want)); /* CAS */
}
```

## 16. Industry Usage
- **Every kernel lock**: Linux spinlocks (queued), mutexes' fast paths — all TAS/CAS-based.
- **Java**: `AtomicInteger` (CAS), `synchronized` biased locks (CAS fast path).
- **Go**: sync.Mutex fast path uses CAS (on x86).
- **C++**: std::atomic, std::mutex.
- **Lock-free data structures**: queues, stacks, RCU, seqlocks — CAS-based, in kernels and high-performance systems.
- Databases: optimistic concurrency uses CAS-like version checks.

## 17. References
- Peterson, "Myths about the mutual exclusion problem" (1981).
- Silberschatz, *OS Concepts*, 7.2 (Peterson), 7.3 (hardware sync).
- Herlihy & Shavit, *The Art of Multiprocessor Programming* (TAS/CAS, lock-free).
- Intel SDM: `cmpxchg`, `xchg`, lock prefix.
- ARM ARM: exclusive monitors (LDXR/STXR).

## 18. Cheat Sheet
- Peterson's: flag[i]=true; turn=j; wait while flag[j]&&turn==j. 2 threads only.
- TAS: atomic set-1 return-old → spinlock.
- CAS: atomic compare-and-write-if-equal → lock-free loops.
- FA: atomic add → tickets, counters.
- Hardware atomicity via cacheline/bus lock.
- ABA problem → version tags.
- Spinlocks waste CPU; need short CS + preemption handling.
- Memory barriers (acquire/release) required around atomics.
- ARM: LDXR/STXR loop; x86: lock cmpxchg.
- MCS/ticket locks add fairness to spinning.

## 19. Quiz
1. Peterson's works for: a) N threads b) 2 threads c) 1 d) none → **b**
2. TAS returns: a) new value b) old value c) lock d) thread → **b**
3. CAS succeeds when: a) value != expected b) value == expected c) always d) never → **b**
4. ABA problem affects: a) TAS b) CAS c) mutex d) semaphore → **b**
5. Spinlock does: a) sleep b) busy-wait c) fork d) I/O → **b**
6. ARM atomic pattern: a) xchg b) LDXR/STXR c) cmpxchg d) fetch → **b**
7. x86 atomic CAS: a) mov b) lock cmpxchg c) nop d) push → **b**
8. Ticket lock adds: a) priority b) fairness c) I/O d) memory → **b**
9. Memory barriers needed for: a) speed b) ordering c) memory d) I/O → **b**
10. MCS lock avoids: a) waiting b) cache ping-pong c) spinning d) atomics → **b**

## 20. Flashcards
- **Q: Peterson's?** → **A:** 2-thread software ME: flags + turn.
- **Q: TAS?** → **A:** Atomic set-1, return old → spinlock.
- **Q: CAS?** → **A:** Atomic compare-and-swap-if-equal.
- **Q: ABA?** → **A:** A→B→A undetectable; fix = version.
- **Q: Why atomics?** → **A:** RMW must be indivisible across CPUs.
- **Q: ARM pattern?** → **A:** LDXR/STXR retry loop.
- **Q: Spinlock cost?** → **A:** Busy CPU + ping-pong.
- **Q: MCS?** → **A:** Queued spinlock, O(1) traffic.

## 21. Revision
Peterson's algorithm solves the 2-thread critical-section problem in pure software (flags + turn, satisfying ME/progress/bounded waiting) — pedagogically invaluable, practically limited. Production relies on hardware atomic read-modify-write: TAS (spinlocks), CAS (lock-free loops, with the ABA caveat), and FA (tickets/counters), made atomic via cacheline/bus locking and exclusive-load/conditional-store loops on ARM. Correct use also demands memory barriers; spinning wastes CPU, so contended locks move to futexes/queued designs.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe Peterson's algorithm" | 13 Q1 / 7 Formal Definition |
| "Why not Peterson's in production?" | 13 Q2 / 4 Why Wasn't Another Approach Chosen |
| "What is test-and-set?" | 13 Q3 / 7 Formal Definition |
| "What is compare-and-swap?" | 13 Q4 / 7 Formal Definition |
| "Why hardware atomics?" | 13 Q5 / 9 Internal Working |
| "Can both threads TAS-enter?" | 13 Q6 / 8 Example |
| "ABA problem?" | 13 Q7 / 12 Disadvantages |
| "Implement lock-free counter" | 13 Q9 / 8 Example |
| "Memory barriers needed?" | 13 Q11 / 9 Internal Working |
| "Spinlock held while preempted?" | 13 Q12 / 12 Disadvantages |
