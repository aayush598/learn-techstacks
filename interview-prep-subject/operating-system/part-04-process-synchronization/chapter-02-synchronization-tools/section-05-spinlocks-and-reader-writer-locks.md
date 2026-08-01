# Section 05: Spinlocks and Reader-Writer Locks

> **TL;DR**: Spinlocks busy-wait with atomics — correct and fast for microsecond kernel critical sections, wasteful otherwise. Reader-writer (RW) locks allow many concurrent readers or one writer, optimizing read-heavy workloads but risking writer starvation and cache contention.

## 1. Why Does This Exist?
Two common situations aren't served by plain sleeping mutexes: (1) tiny critical sections (updating a counter, a page-table bit) where the overhead of a futex sleep/wake exceeds the CS itself — a spinlock's busy-wait is cheaper; (2) read-mostly data (config tables, caches, routing tables) where *reads* can safely proceed in parallel — an RW lock's many-readers/single-writer model unlocks concurrency that a mutex serializes. Both exist to squeeze parallelism out of otherwise-correct-but-slow locking.

## 2. How Does It Work?
**Spinlock**:
- `lock`: `while (TAS(&lock, 1) == 1) ;` — spin until old value was 0.
- `unlock`: `lock = 0;` (with release barrier).
- Requires preemption disabled in kernel (a preempted spinner with preemption disabled would deadlock); short CS only.
- Modern variants: ticket locks (fairness), MCS/queued locks (O(1) cache traffic).

**RW lock**:
- State: readers count + writer bit (or writer-first wait queue).
- `read_lock`: if no writer and no writer waiting → increment readers; else wait.
- `read_unlock`: decrement; if last reader and a writer waits → wake writer.
- `write_lock`: wait until readers == 0 and no writer; then set writer.
- Policy choices: reader-preferring (readers don't wait — writer starvation) vs writer-preferring (writers jump the queue — reader starvation) vs fair.

## 3. When Is It Used?
- **Spinlock**: kernel paths too short to sleep — per-cpu refcounts, interrupt-safe updates, RCU read-side, freelist operations.
- **RW lock**: read-mostly structures — routing/config tables, caches, filesystem metadata (Linux rwsem), databases (row-level read locks in serializable mode).
- pthread: `pthread_rwlock_t`; kernel: `rwlock_t`, `rwsem`.

## 4. Why Wasn't Another Approach Chosen?
- **Mutex for tiny CS**: sleeping cost (syscall + wakeup) >> CS time — wasteful; spin wins. Rejected for micro-CS.
- **Mutex for read-mostly**: serializes all reads — loses massive parallelism; RW lock wins. Rejected.
- **Lock-free/RCU**: superior for some read-mostly cases, but harder and not always applicable (writers need to modify in place); RW lock is the pragmatic middle.
- **Writer-preferring vs reader-preferring**: neither wins always; both exist because the tradeoff is workload-dependent.
So we keep *both* spinlocks (for the irreducible short CS) and RW locks (for the reader/writer ratio), with lock-free/RCU as the advanced alternative.

## 5. Intuition
**Spinlock**: a busy doorman who never sleeps — if the VIP room (CS) frees in a nanosecond, waiting at the door (spinning) beats walking to a waiting room (sleeping). **RW lock**: a library reading room — many people can read simultaneously (readers), but only one person can *edit* the books (writer), and while an edit happens, everyone must step out.

## 6. Real-World Analogy
**A parking-lot gate**: spinlock = a driver who keeps pressing the button (TAS) until the gate opens — fine if the car ahead is seconds away, maddening if it's minutes. **RW lock** = a shared whiteboard: anyone can read it (many readers), only the owner writes (one writer) — readers can all look together, but a writer erases/rewrites and everyone must stop reading briefly.

## 7. Formal Definition
- **Spinlock**: a lock held by busy-waiting on an atomic flag: `while (test_and_set(&lock,1)) ;` — release `lock = 0`. No scheduling, no queue. Requires short CS + (kernel) preemption/IRQ considerations.
- **Ticket lock**: fetch-and-add a ticket; spin until your number == serving → FIFO fairness, O(1) but ping-pong.
- **MCS/queued spinlock**: each waiter spins on its own node; unlock hands off → O(1) cacheline traffic, no shared-line ping-pong.
- **RW lock**: state (readers, writer); invariants: (readers > 0 ∧ writer == 0) ∨ (readers == 0 ∧ writer == 1).
  - Reader-preferring: readers proceed unless a writer holds; writer waits for all readers — writer starvation possible.
  - Writer-preferring: pending writers block new readers — reader starvation possible (usually bounded via queues).
- **seqlock**: a variant — readers may see stale data and *retry* (optimistic read); writers just increment a sequence — for very read-heavy data.

## 8. Example
**RW lock, reader-preferring**:
```
Initially: readers=0, writer=0
T1 read_lock -> no writer -> readers=1  [enter]
T2 read_lock -> no writer -> readers=2  [enter]   (both read concurrently)
W  write_lock -> readers != 0 -> W waits
T1 read_unlock -> readers=1
T2 read_unlock -> readers=0 -> wake W
W  write_lock -> writer=1 -> [write critical section] -> writer=0, wake waiters
```
Reads scale in parallel; writes exclude both.

## 9. Internal Working
1. **Spinlock**: `arch_spin_lock` → `LOCK xchg`/`cmpxchg` loop (x86 `lock bts`); tick_lock uses `xadd` for tickets; MCS allocates a per-CPU node, spins on it, unlock hands off via the node.
2. Linux marks spinlocks with `preempt_disable()` — a spinholder won't be preempted (avoids deadlock when the holder would never run); IRQ safety via `spin_lock_irqsave`.
3. **rwsem/RW lock**: counter encodes readers/writer; read path: atomic add, if negative (writer active) → wait queue; write path: CAS to writer state → wait queue. Writer-first wakes writers before readers.
4. Userspace pthread_rwlock: futex-based; writer starvation policies per implementation.

## 10. Time Complexity
- Spinlock uncontended: O(1) atomic op. Contended: spins — each iteration ~cache-miss latency; ticket/MCS reduce traffic to O(1) per acquisition vs O(n) ping-pong for naive TAS.
- RW read: O(1) atomic inc (fast path). Write: O(1) atomic + wait.
- RW lock contention: read-heavy scales well; a writer stall costs all readers.

## 11. Advantages
**Spinlock**: minimal latency for short CS (no syscall); deterministic; interrupt-safe usage.
**RW lock**: parallel reads → huge speedup on read-mostly data; writer exclusion preserved; simple API; seqlock variant gives lock-free reads.

## 12. Disadvantages
**Spinlock**: burns CPU (unusable for long CS); preemption danger in kernel; cache ping-pong (naive); starvation (naive TAS — ticket/MCS fix).
**RW lock**: reader/writer starvation depending on policy; cacheline contention on the shared readers counter; writers pay full exclusion cost; biased to reads — write-heavy workloads do worse than a plain mutex.

## 13. Interview Questions
1. **Q: What is a spinlock?** A: A lock implemented by busy-waiting (TAS loop) until the atomic flag is free — no sleep, minimal overhead for very short critical sections.
2. **Q: When is a spinlock better than a mutex?** A: When the CS is shorter than the sleep/wake cost (kernel micro-sections). If the CS can block (I/O) or is long, spinlocks waste CPU — use a mutex.
3. **Q: Why must kernel spinlocks disable preemption?** A: If the holder is preempted, other CPUs spin until it runs again — deadlock-like (or long stalls). Disabling preemption keeps the holder on the CPU.
4. **Q: What is the ticket lock?** A: A fair spinlock: fetch-and-add a ticket; spin until your ticket number is served — FIFO order, prevents starvation.
5. **Q: What is an MCS lock?** A: A queued spinlock where each waiter spins on its own node and unlock hands off — eliminates shared-cacheline ping-pong (O(1) traffic).
6. **Q: What is a reader-writer lock?** A: A lock allowing many concurrent readers OR one writer; read_lock/read_unlock, write_lock/write_unlock.
7. **Q (TRICKY): Why can writer starvation happen?** A: Reader-preferring policies let new readers jump ahead of a waiting writer; continuous read arrivals postpone the writer forever. Writer-preferring policies fix it (new readers wait).
8. **Q: When use an RW lock vs a mutex?** A: Read-mostly data (many readers, few writers): RW lock parallelizes reads. Write-heavy or mixed-equal: a plain mutex is simpler and often faster.
9. **Q: What is a seqlock?** A: A writer-optimistic lock: writers bump a sequence; readers read optimistically and *retry* if the sequence changed — lock-free reads, at the cost of possible retries.
10. **Q (PRODUCTION): Your cache is read 100x more than written. What locking?** A: Reader-writer lock (or RCU/lock-free read path if writes must not block readers at all). Measure contention; if writers still stall, switch to sharding or lock-free.
11. **Q: What are the read/write invariants of an RW lock?** A: Either readers > 0 and no writer, or a single writer and zero readers — never both.
12. **Q (TRICKY): Can a spinlock be held across a context switch?** A: No (in kernel, preemption is disabled while holding). A spinlock held while sleeping is a bug — use mutex/sleepable locks for code that blocks.

## 14. Follow-Up Questions
1. **Q: What's the difference between a spinlock and a mutex in Linux?** A: spinlock: no sleep, preemption disabled, for short CS; mutex: sleepable, PI-capable, for longer CS.
2. **Q: What is `spin_lock_irqsave`?** A: Spinlock variant that also disables local interrupts (saves flags) — needed when a handler running on the same CPU could re-enter the lock.
3. **Q: What is a "seqlock writer-fair" variant?** A: Writers are serialized and readers may retry; writers don't starve. Used in Linux for timekeeping (`ktime`).
4. **Q: How does RCU relate to RW locks?** A: RCU gives readers lock-free access and defers reclamation — stronger for read-mostly; RW locks are the simpler blocking alternative.
5. **Q: When does an RW lock outperform?** A: When read:write ratio is high (e.g., 10:1+) and CS is meaningful; below that, counter contention makes it worse than a mutex.

## 15. Coding Example
```c
/* Spinlock using C11 atomics (test-and-set) */
#include <stdatomic.h>
#include <stdbool.h>

typedef struct { atomic_bool flag; } spinlock_t;
void spin_init(spinlock_t *s) { atomic_init(&s->flag, false); }

void spin_lock(spinlock_t *s) {
    while (atomic_exchange(&s->flag, true))   /* TAS */
        ;                                     /* spin */
}
void spin_unlock(spinlock_t *s) {
    atomic_store(&s->flag, false);            /* release */
}
```
```c
/* Pthread reader-writer lock */
#include <pthread.h>
#include <stdio.h>

pthread_rwlock_t rw = PTHREAD_RWLOCK_INITIALIZER;
long data = 0;

void *reader(void *arg) {
    pthread_rwlock_rdlock(&rw);
    printf("read %ld\n", data);               /* many readers in parallel */
    pthread_rwlock_unlock(&rw);
    return NULL;
}
void *writer(void *arg) {
    pthread_rwlock_wrlock(&rw);
    data++;                                   /* exclusive */
    pthread_rwlock_unlock(&rw);
    return NULL;
}
```

## 16. Industry Usage
- **Linux kernel**: spinlocks everywhere (per-CPU accounting, list manipulation, RCU update side); rwsem for filesystem/virtual-memory locks; seqlock for timekeeping.
- **Databases**: rw latches on B-tree pages; reader-writer transactions.
- **Java**: ReentrantReadWriteLock, StampedLock (seqlock-like).
- **C++**: std::shared_mutex (RW).
- **Config/cache lookups**: hot-path reads use RW locks or seqlocks.

## 17. References
- Silberschatz, *OS Concepts*, 7.3 (spinlocks), 7.9 (RW locks).
- Linux: `include/linux/spinlock.h`, `kernel/locking/rwsem.c`, seqlock docs.
- Herlihy & Shavit, *The Art of Multiprocessor Programming* (locks ch.).
- man: `pthread_rwlock_rdlock(3)`, `pthread_spin_lock(3)`.

## 18. Cheat Sheet
- Spinlock: busy-wait TAS; short CS; no sleep; preemption disabled in kernel.
- Ticket lock: fair FIFO spin; MCS: queued, O(1) traffic.
- RW lock: many readers XOR one writer.
- read_lock: no writer → readers++. write_lock: wait readers==0.
- Reader-preferring → writer starvation; writer-preferring → reader starvation.
- seqlock: writers bump seq, readers retry (optimistic).
- Spinlock for micro-CS; mutex for blocking CS; RW for read-mostly.
- Invariants: (r>0 ∧ w=0) ∨ (r=0 ∧ w=1).
- RW good at high read:write ratio; worse otherwise.
- Never sleep while holding a spinlock.

## 19. Quiz
1. Spinlock waits by: a) sleeping b) busy-waiting c) yielding d) I/O → **b**
2. Spinlock CS must be: a) long b) very short c) blocking d) I/O-heavy → **b**
3. Kernel spinlock disables: a) interrupts only b) preemption c) memory d) nothing → **b**
4. Ticket lock provides: a) speed b) fairness c) sleep d) priority → **b**
5. MCS lock avoids: a) deadlock b) cache ping-pong c) waiting d) atomics → **b**
6. RW lock: a) one reader b) many readers or one writer c) many writers d) none → **b**
7. Writer starvation from: a) writer-preferring b) reader-preferring c) both d) tickets → **b**
8. seqlock readers: a) lock b) optimistic + retry c) sleep d) wait → **b**
9. RW lock beats mutex when: a) write-heavy b) read-heavy c) equal d) never → **b**
10. Sleep while holding spinlock: a) fine b) bug c) faster d) only SMP → **b**

## 20. Flashcards
- **Q: Spinlock?** → **A:** Busy-wait TAS; short CS.
- **Q: Ticket lock?** → **A:** Fair FIFO spinning.
- **Q: MCS?** → **A:** Queued, O(1) cache traffic.
- **Q: RW lock?** → **A:** Many readers XOR one writer.
- **Q: Starvation?** → **A:** Policy-dependent (reader/writer-preferring).
- **Q: seqlock?** → **A:** Optimistic reads, retry.
- **Q: When RW?** → **A:** Read-heavy workloads.
- **Q: Spin + sleep?** → **A:** Bug (deadlock).

## 21. Revision
Spinlocks busy-wait on an atomic flag — minimal-latency exclusion for microsecond CS (kernel preemption disabled), refined into ticket (fair) and MCS (cache-friendly) forms. Reader-writer locks let many readers or one writer in, parallelizing read-mostly workloads; policy choice (reader vs writer preferring) trades off starvation, and seqlocks make reads optimistic with retries. Match the tool to the workload: spinlock for tiny CS, mutex for blocking CS, RW/seqlock for read-heavy data.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a spinlock?" | 13 Q1 / 7 Formal Definition |
| "Spinlock vs mutex?" | 13 Q2 / 4 Why Wasn't Another Approach Chosen |
| "Why disable preemption?" | 13 Q3 / 9 Internal Working |
| "Ticket lock?" | 13 Q4 / 7 Formal Definition |
| "MCS lock?" | 13 Q5 / 7 Formal Definition |
| "What is an RW lock?" | 13 Q6 / 7 Formal Definition |
| "Writer starvation?" | 13 Q7 / 12 Disadvantages |
| "RW lock vs mutex?" | 13 Q8 / 4 Why Wasn't Another Approach Chosen |
| "What is a seqlock?" | 13 Q9 / 7 Formal Definition |
| "Cache read-heavy — which lock?" | 13 Q10 / 3 When Is It Used |
