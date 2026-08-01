# Section 01: Bounded-Buffer Problem (Producer-Consumer)

> **TL;DR**: Producers add to a fixed-size buffer, consumers remove from it. Correctness needs three pieces: a mutex for buffer access, a "count of full slots" semaphore (consumer wait), and a "count of empty slots" semaphore (producer wait) — or the equivalent monitor with two condition variables.

## 1. Why Does This Exist?
Any producer-consumer pipeline (message queue, work queue, network buffers) must handle: producers outpacing consumers (buffer overflow) and consumers outpacing producers (busy/idle). The bounded-buffer problem formalizes the solution: a fixed-size buffer plus two counting semaphores that block producers when full and consumers when empty. It's the template for every queue in operating systems and servers.

## 2. How Does It Work?
Classic semaphore solution (buffer size N):
- `empty = N`, `full = 0`, `mutex = 1`.
- **Producer**: `wait(empty)` → `wait(mutex)` → add → `signal(mutex)` → `signal(full)`.
- **Consumer**: `wait(full)` → `wait(mutex)` → remove → `signal(mutex)` → `signal(empty)`.
- `empty` counts free slots (producers wait when 0); `full` counts filled slots (consumers wait when 0); `mutex` protects the array.
Monitor version: `put` waits while full (CV `not_full`), `take` waits while empty (CV `not_empty`); both use `notifyAll`.

## 3. When Is It Used?
- Thread/worker queues: producers enqueue jobs, workers consume.
- Message passing: mailbox queues, MPI-style buffers.
- Network device drivers: ring buffers for TX/RX packets.
- Log/event pipelines, blocking queues in Java (`ArrayBlockingQueue`), Go channels (unbuffered = N=0 rendezvous).

## 4. Why Wasn't Another Approach Chosen?
- **Unbounded buffer**: memory grows without bound — producers can outrun consumers forever. Rejected for backpressure.
- **Busy-wait on "is there space?"**: wastes CPU. Rejected — semaphores/CVs sleep.
- **Single mutex only**: a mutex prevents concurrent buffer access but not the *capacity* problem — producers still overwrite when full. Need counting semantics.
- **Lock-free ring buffer**: possible (SPSC) but hard for MPMC; the semaphore/CV solution is correct and simple for the general case.
The chosen design: **capacity via counting semaphores + mutual exclusion via mutex** — blocks rather than overwrites, sleeps rather than spins.

## 5. Intuition
**A sushi conveyor belt with N plates**: the belt has N slots. A chef (producer) can only put a plate if a slot is empty (`empty > 0`); a diner (consumer) can only take if a plate is there (`full > 0`). Nobody touches the same plate at once (mutex). If the belt is full, the chef waits (sleeps) rather than piling plates on the floor.

## 6. Real-World Analogy
**A parking garage with N spots between two one-way roads**: producers are cars arriving and entering if spots exist (empty count), consumers are cars leaving (full count). If full, arriving cars queue outside (producers block). The gate (mutex) lets only one car move at a time. The two counters — empty (can I enter?) and full (is there a car to leave?) — drive the whole system.

## 7. Formal Definition
- **Problem**: an array of N slots; producers insert at in, consumers remove at out; never produce into a full buffer, never consume from an empty one; no two threads touch the array simultaneously.
- **Semaphore solution**:
  - `empty = N` (available slots), `full = 0` (occupied slots), `mutex = 1`.
  - Producer: P(empty); P(mutex); add; V(mutex); V(full).
  - Consumer: P(full); P(mutex); remove; V(mutex); V(empty).
  - Invariant: `empty + full = N`; buffer access is mutually exclusive; operations never run out of buffer space.
- **Monitor solution**: `put` { while (count == N) wait(not_full); add; signal(not_empty); } and `take` { while (count == 0) wait(not_empty); remove; signal(not_full); }.

## 8. Example
N=2, buffer [_,_]. empty=2, full=0.
- P1: P(empty)→1; P(mutex)→0; add; V(mutex)→1; V(full)→1. Buffer [A,_].
- P2: P(empty)→0; add; V(full)→2. Buffer [A,B] full.
- P3: P(empty)→−1 → **blocks** (buffer full).
- C1: P(full)→1; remove A; V(empty)→0. Buffer [_,B].
- P3 (wakes): P(empty)→−1? no: after V(empty) →0 then P3 retakes → −1? Actually P3 resumes P(empty) which now succeeds (0→−1? P3 is unblocked when empty becomes >0): P3: P(empty)→0 (from −1+1), P(mutex), add, V(full). Correct — no overrun.

## 9. Internal Working
1. `sem_wait` decrements atomically; if negative → futex wait (block). `sem_post` increments; if waiters → wake one (futex wake).
2. Ordering: acquire `empty`/`full` **before** `mutex` — acquiring mutex first would let a producer hold the lock while waiting for empty → deadlock. This ordering is the classic correctness detail.
3. Mutex protects in/out indices + array; semaphores manage capacity.
4. Monitor version: single mutex + two CVs; wait releases the mutex atomically.
5. Performance: contended producers/consumers serialize on the mutex even though capacity is fine — hence lock-free ring buffers (SPSC) for extreme throughput.

## 10. Time Complexity
- Per op (semaphore version): O(1) — two sem ops + mutex op. Uncontended: a few atomics.
- Monitor version: O(1) lock + possibly wait/wake.
- Throughput bounded by mutex contention and cacheline of the buffer indices.

## 11. Advantages
- Backpressure: never overflow/underflow; producers/consumers sleep, not spin.
- Simple, provably correct (invariant empty+full=N).
- Works with multiple producers/consumers.
- Maps to real queues/blocking collections directly.

## 12. Disadvantages
- One mutex serializes buffer access — limited scalability (MPMC).
- Semaphore ordering (capacity before mutex) is easy to get wrong → deadlock.
- Wait/wake latency for blocked producers/consumers.
- Semaphore-based version has no ownership/fairness guarantees.
- Doesn't express *which* item to take (FIFO vs priority) without extra policy.

## 13. Interview Questions
1. **Q: Describe the bounded-buffer problem.** A: Producers add to a fixed N-slot buffer, consumers remove; producers must block when full, consumers when empty, and buffer access must be exclusive.
2. **Q: Why two semaphores plus a mutex?** A: `empty` (capacity available) blocks producers; `full` (items available) blocks consumers; `mutex` ensures only one thread touches the array. The counts enforce the invariant empty+full=N.
3. **Q: What order do you acquire the semaphores?** A: Capacity semaphore (`empty`/`full`) **before** the mutex — else a thread holds the mutex while waiting for capacity → deadlock.
4. **Q (TRICKY): What happens if a producer holds the mutex while waiting for `empty`?** A: All consumers block on the mutex too (they can't remove items), so `empty` can never increase → deadlock. This is why capacity is acquired first.
5. **Q: Why does the consumer wait on `full`, not `empty`?** A: `full` counts filled slots — the consumer needs an item, so it waits until full > 0. Producers wait on `empty` (need a free slot).
6. **Q: What is the invariant?** A: `empty + full = N` at all times (each slot is exactly empty-or-full), plus exclusive buffer access.
7. **Q: How would you do it with a monitor?** A: `put`: while (count==N) wait(not_full); add; notifyAll. `take`: while (count==0) wait(not_empty); remove; notifyAll — mutex implicit, CVs replace semaphores.
8. **Q (PRODUCTION): Your consumer is slower than the producer. What happens?** A: `empty` hits 0 → producers block (backpressure); the buffer stays bounded; memory bounded. This is the *correct* behavior — backpressure is a feature.
9. **Q: What about multiple producers and consumers?** A: The semaphore/monitor solutions handle MPMC directly — the mutex serializes buffer access, semaphores arbitrate capacity.
10. **Q: Why is a lock-free ring buffer faster for single-producer-single-consumer?** A: It avoids the mutex and uses atomic head/tail; with one producer and one consumer, no mutual exclusion is needed — just memory ordering (SPSC).
11. **Q: What's the difference between this and a semaphore alone?** A: Semaphores alone can count capacity but don't protect the array from concurrent access; you still need the mutex for the in/out indices and data.
12. **Q: How does Go's channel relate?** A: `chan T` with capacity N is a bounded buffer; unbuffered (N=0) is a rendezvous — the receiver and sender synchronize directly. Same backpressure semantics.

## 14. Follow-Up Questions
1. **Q: What is the "reader/writer" distinction here?** A: Producer writes slots, consumer reads them — each slot transitions empty→full (write) and full→empty (read) under the mutex.
2. **Q: How do you add priorities (e.g., take highest-priority job)?** A: Change the buffer to a priority queue; the mutex/semaphore structure stays, the dequeue policy changes.
3. **Q: What's the difference between bounded and unbounded queues?** A: Unbounded never blocks producers (memory risk); bounded provides backpressure. BlockingDeque vs LinkedBlockingQueue unbounded.
4. **Q: How is this used in the kernel?** A: Network RX/TX rings, TTY buffers, work queues — producers (interrupts/tasks) and consumers (ksoftirqd/worker threads) with capacity.
5. **Q: What is a "rendezvous" vs bounded buffer?** A: Rendezvous = capacity 0: producer blocks until a consumer takes, and vice versa — direct handoff.

## 15. Coding Example
```c
/* Bounded buffer: semaphore solution */
#include <semaphore.h>
#include <pthread.h>

#define N 8
int buf[N], in = 0, out = 0;
sem_t empty, full;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;

void producer(int item) {
    sem_wait(&empty);                  /* capacity first! */
    pthread_mutex_lock(&m);
    buf[in] = item; in = (in + 1) % N;
    pthread_mutex_unlock(&m);
    sem_post(&full);
}

int consumer(void) {
    sem_wait(&full);
    pthread_mutex_lock(&m);
    int item = buf[out]; out = (out + 1) % N;
    pthread_mutex_unlock(&m);
    sem_post(&empty);
    return item;
}
```
```c
/* Monitor solution (already in section on CVs); here the pattern */
/* put: while(count==N) cvwait(&not_full,&m); add; cvsignal(&not_empty); */
```

## 16. Industry Usage
- **Java**: `ArrayBlockingQueue`, `LinkedBlockingQueue` (monitor solutions); ExecutorService work queues.
- **Go**: channels (bounded = buffered channel).
- **Kernel**: network ring buffers, TTY queues, block I/O queues.
- **Message brokers**: bounded internal queues provide backpressure to producers.
- **Pipeline frameworks**: Kafka consumers, pipeline stages with finite buffers.

## 17. References
- Silberschatz, *OS Concepts*, 7.6 (Bounded-buffer), 7.7 (monitor version).
- Dijkstra (1965) — semaphore-based solution.
- Java: `java.util.concurrent.ArrayBlockingQueue` source/Javadoc.
- Go spec: channels.

## 18. Cheat Sheet
- empty = N, full = 0, mutex = 1.
- Producer: P(empty) → P(mutex) → add → V(mutex) → V(full).
- Consumer: P(full) → P(mutex) → remove → V(mutex) → V(empty).
- Order: capacity semaphore BEFORE mutex (else deadlock).
- Invariant: empty + full = N.
- Blocked producer = backpressure (correct behavior).
- Monitor: while(count==N) wait; notifyAll.
- MPMC supported; SPSC → lock-free ring better.
- Go channel cap N = bounded buffer; 0 = rendezvous.

## 19. Quiz
1. empty counts: a) items b) free slots c) threads d) mutexes → **b**
2. Producer waits on: a) full b) empty c) mutex d) in → **b**
3. Consumer waits on: a) empty b) full c) out d) N → **b**
4. Correct acquisition order: a) mutex then semaphore b) semaphore then mutex c) any d) none → **b**
5. Holding mutex while waiting for empty: a) fine b) deadlock c) faster d) race → **b**
6. Invariant: a) empty = full b) empty+full = N c) full = N d) empty = 0 → **b**
7. Blocked producer when full: a) overflow b) backpressure c) deadlock d) race → **b**
8. MPMC supported: a) no b) yes c) single only d) rare → **b**
9. SPSC faster with: a) mutex b) lock-free ring c) semaphores d) sleep → **b**
10. Go channel cap 0 is: a) bounded b) rendezvous c) infinite d) invalid → **b**

## 20. Flashcards
- **Q: Producer waits on?** → **A:** empty (free slots).
- **Q: Consumer waits on?** → **A:** full (items).
- **Q: Order?** → **A:** Semaphore before mutex.
- **Q: Invariant?** → **A:** empty + full = N.
- **Q: Full buffer + producer?** → **A:** Blocks (backpressure).
- **Q: Monitor version?** → **A:** while + CVs, notifyAll.
- **Q: Deadlock cause?** → **A:** Mutex-first acquisition.
- **Q: Go channel?** → **A:** Buffered = bounded buffer.

## 21. Revision
The bounded-buffer problem pairs a fixed-size array with `empty`/`full` counting semaphores plus a mutex: producers wait on empty, consumers on full, both touch the buffer under the mutex, with the invariant empty+full=N. The classic trap is acquiring the mutex before the capacity semaphore → deadlock. The monitor version uses two condition variables with while-loops and notifyAll. Blocking on full/empty is *backpressure* — correct, not a bug. It's the template for every queue, from kernel rings to Go channels.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Describe bounded-buffer" | 13 Q1 / 7 Formal Definition |
| "Why two semaphores + mutex?" | 13 Q2 / 2 How Does It Work |
| "Acquisition order?" | 13 Q3 / 9 Internal Working |
| "Deadlock if mutex first?" | 13 Q4 / 8 Example |
| "Wait on full or empty?" | 13 Q5 / 7 Formal Definition |
| "What's the invariant?" | 13 Q6 / 7 Formal Definition |
| "Monitor version?" | 13 Q7 / 8 Example |
| "Slower consumer?" | 13 Q8 / 12 Disadvantages |
| "MPMC?" | 13 Q9 / 3 When Is It Used |
| "Lock-free ring better?" | 13 Q10 / 12 Disadvantages |
