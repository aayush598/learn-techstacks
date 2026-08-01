# Section 04: Sleeping Barber Problem

> **TL;DR**: A barber sleeps when there are no customers, a customer wakes the barber when arriving, and customers leave if the waiting room is full. The solution uses three semaphores (customers, barber, mutex) — the canonical demo of *rendezvous* and of avoiding busy-waiting: everyone sleeps until someone acts.

## 1. Why Does This Exist?
The sleeping barber tests the *interaction* between a resource (the barber), a queue (waiting room), and producer-consumer-like handoff — specifically, "what happens when the server has nothing to do?" The barber must *sleep* (not busy-wait) when idle, customers must wake it exactly once, and the waiting room capacity must bound the queue (customers leave if full). It exists to teach rendezvous-style synchronization and the discipline of sleeping on empty.

## 2. How Does It Work?
- State: barber chair, waiting room with N seats.
- **Barber loop**: `wait(customers)` (sleep if none) → `signal(barber)` (I'm ready) → `wait(mutex)` → take next customer, free a seat → `signal(mutex)` → cut hair (uninterrupted) → repeat.
- **Customer**: `wait(mutex)` → if seats free, sit, `signal(customers)`, `signal(mutex)`, `wait(barber)` (wait for barber to be ready) → get haircut; else `signal(mutex)`, leave.
- Three semaphores: `customers` (0 = barber sleeps), `barber` (barber ready for a specific customer), `mutex` (protects seat count).
- **Rendezvous**: the `customers`/`barber` pair forces a handshake — the customer and barber both wait for the other to be ready.

## 3. When Is It Used?
- Worker-thread models: a server that sleeps when no requests and wakes on arrival (thread pools, event loops).
- Connection accept loops, mailbox handling, job runners.
- Producer-consumer where the *single server* goes idle (not just a buffer).
- Any "sleep until there's work, and exactly one consumer handles it" pattern.

## 4. Why Wasn't Another Approach Chosen?
- **Busy-wait polling** ("any customers? any customers?"): wastes CPU while idle. Rejected — the barber sleeps.
- **Single semaphore for both capacity and wake**: conflates "customer waiting" with "barber ready" — the rendezvous needs two signals. Rejected.
- **Pure mutex**: doesn't express "sleep until event." Rejected.
- **Condition variables**: a valid alternative (barber waits on a CV with predicate "customers > 0"); the semaphore version teaches counting + rendezvous directly.
The chosen design: **three semaphores** — one for capacity (mutex/seat count), one to wake the barber (customers), one to hand off (barber ready).

## 5. Intuition
**A barber who sleeps in his chair**: when the shop is empty, he naps. A customer arriving wakes him (signal), he says "come sit" (rendezvous), cuts the hair, and if no one else waits, goes back to sleep. A full waiting room means a new customer turns around and leaves (capacity bound). Nobody ever stands around tapping their foot — the barber and the customer both *sleep until they're needed*.

## 6. Real-World Analogy
**A single coffee machine in a break room**: the machine (barber) is idle/sleeping when no one queues. Someone wanting coffee: if the counter (waiting room) has room, they place their cup (customer semaphore) and the machine wakes and brews for them (barber handshake). If the counter is full, they leave. The machine sleeps between brews instead of running constantly — an idle-resource rendezvous.

## 7. Formal Definition
- **State**: `customers = 0` (customers waiting or being served), `barber = 0` (barber ready), `mutex = 1` (guards seat count), `waiting = 0` (free seats = N − waiting).
- **Barber**:
  ```
  while (true) {
      wait(customers);      // sleep if no customers
      signal(barber);       // I'm ready for one
      wait(mutex);
      waiting--;            // free a seat
      signal(mutex);
      cut_hair();
  }
  ```
- **Customer**:
  ```
  wait(mutex);
  if (waiting < N) { waiting++; signal(customers); signal(mutex);
                     wait(barber); get_haircut(); }
  else signal(mutex);       // full room: leave
  ```
- **Invariant**: no busy-waiting anywhere; barber sleeps exactly when `customers == 0`; each `signal(customers)` wakes exactly one barber.

## 8. Example
N=3 seats, all empty. Barber asleep (customers=0).
- C1 arrives: mutex; waiting 0→1; signal(customers)→1; unlock; wait(barber) → sleeps.
- Barber wakes (customers→0): signal(barber)→1; mutex; waiting 1→0; unlock; C1 wakes (barber→0); haircut.
- While cutting: C2, C3 arrive: waiting→2, →3 (signal customers ×2). C4 arrives: waiting==3==N → leaves (room full).
- Barber done → loop: wait(customers) succeeds (customers=2→1); serves C2; ... eventually customers=0 → barber sleeps again.

## 9. Internal Working
1. Semaphores are futex-based (Linux/glibc) or RTOS-native — wait parks the thread, signal wakes one.
2. The `customers` semaphore is the *wake signal* for the barber thread: `signal(customers)` from a customer transitions it from blocked to runnable.
3. The `barber` semaphore is the *handoff*: only after the barber signals ready does the customer proceed to the chair — a rendezvous, not just a count.
4. The mutex protects the seat counter; the arrival path must be atomic (check capacity, reserve seat, signal, release).
5. Correctness: customers never get a haircut before the barber is ready (barber semaphore); the barber never sleeps while customers wait (customers semaphore > 0).

## 10. Time Complexity
- Customer arrival: O(1) (mutex + sem ops).
- Barber cycle: O(1) per customer + haircut time.
- Idle barber: O(1) sleep (no CPU cost).
- Capacity check is O(1); leaving when full is O(1).

## 11. Advantages
- No busy-waiting — idle resources sleep (CPU efficiency).
- Demonstrates rendezvous cleanly (customer↔barber handshake).
- Capacity-bound queue (customers leave when full) = bounded memory/backpressure.
- Simple three-semaphore pattern that maps to worker/event-loop designs.

## 12. Disadvantages
- Single-server bottleneck (one barber) — serializes all work.
- Customers leaving when full = dropped work (needs a policy decision).
- Semaphore order must be exact (mutex around capacity, signals after) — easy to break.
- Rendezvous can deadlock if signals are ordered wrong (barber waits on customers that never get signaled).
- No priorities (VIP customers wait like everyone else).

## 13. Interview Questions
1. **Q: What is the sleeping barber problem?** A: A barber sleeps when no customers; arriving customers wake him; if the waiting room is full, customers leave; everyone sleeps instead of busy-waiting.
2. **Q: Why three semaphores?** A: `customers` (wake the barber), `barber` (rendezvous — barber ready for this customer), `mutex` (protect the seat count). Two signals are needed because both the barber and the customer block on each other.
3. **Q: What is the rendezvous?** A: The customer waits for `barber` ready while the barber waits for a `customer` — a handshake ensuring a customer never gets cut before the barber is ready.
4. **Q: Why does the barber sleep instead of poll?** A: Polling wastes CPU; sleeping (blocking on `customers`) is the efficient idle. This is the "don't busy-wait" lesson.
5. **Q (TRICKY): What happens if the barber signals `barber` before the customer waits on it?** A: The customer still catches it (semaphore counts the signal) — that's the beauty of counting semaphores vs a pure rendezvous flag; the value is sticky.
6. **Q: Why do customers leave when the room is full?** A: To bound the queue (capacity N) — backpressure. If they waited, the queue would grow unboundedly (or block forever).
7. **Q: How does this relate to producer-consumer?** A: Customers = producers, barber = single consumer, waiting room = bounded buffer. But there's an extra handshake (barber-ready) because the consumer is a single persistent server that goes idle.
8. **Q (PRODUCTION): A worker thread should sleep when there's no work and wake on new jobs. Pattern?** A: Exactly this: a job semaphore/CV + a mutex; workers wait on the semaphore, dispatchers signal on enqueue — the sleeping-barber model.
9. **Q: Can the barber miss a customer?** A: No — `signal(customers)` wakes the barber (or increments the count for later). The count is sticky, so no missed wakeups; that's why a semaphore, not a boolean flag, is used.
10. **Q: How would you solve it with condition variables?** A: Barber waits `while (waiting == 0) cv_wait(&has_customers, &mutex);` customers signal `has_customers` — same rendezvous with a predicate.
11. **Q: What happens if two customers arrive exactly when the barber finishes a haircut?** A: They join the waiting room (seats permitting); the barber's next `wait(customers)` succeeds immediately (count ≥ 1) and serves them in FIFO seat order.
12. **Q (TRICKY): Deadlock risk?** A: If the mutex were held while waiting on `customers` (barber) or while waiting on `barber` (customer), deadlock — the ordering (release mutex before blocking on the event semaphores) is essential.

## 14. Follow-Up Questions
1. **Q: What's the difference between this and a plain bounded buffer?** A: The barber is a *single consumer that sleeps*; the buffer solution assumes a pool and doesn't model the server going idle or the customer-barber handshake.
2. **Q: What is "bounded waiting" here?** A: A customer waits at most until all waiting customers ahead are served; the seat FIFO gives a bound (unlike a free-for-all).
3. **Q: How do thread pools relate?** A: Workers = barbers (they wait on a work semaphore/CV); the dispatcher = customers enqueueing; queue capacity = waiting-room size (workers leave/drop on overflow policy).
4. **Q: What's a "rendezvous" generally?** A: A synchronization point where both parties must arrive — neither proceeds until both signal; used for barriers and two-way handoffs.
5. **Q: What if the barber is slow and the room is full — customers leave; is that a problem?** A: It's a policy tradeoff: reject-on-full (drop) vs block. Real systems choose based on whether the work is retryable (drop) or must be done (block/wait).

## 15. Coding Example
```c
/* Sleeping barber with three semaphores */
#include <semaphore.h>
#include <pthread.h>
#include <stdio.h>

#define N 3                      /* waiting-room seats */
sem_t customers, barber_ready, mutex;
int waiting = 0;

void *barber(void *arg) {
    for (;;) {
        sem_wait(&customers);            /* sleep if no customers */
        sem_post(&barber_ready);         /* I'm ready for one */
        sem_wait(&mutex);
        waiting--;
        sem_post(&mutex);
        printf("barber: cutting hair (%d waiting)\n", waiting);
        usleep(1000);                    /* haircut */
    }
}

void *customer(void *arg) {
    int id = (long)arg;
    sem_wait(&mutex);
    if (waiting < N) {
        waiting++;
        sem_post(&customers);            /* wake the barber */
        sem_post(&mutex);
        sem_wait(&barber_ready);         /* rendezvous */
        printf("customer %d: getting haircut\n", id);
    } else {
        sem_post(&mutex);
        printf("customer %d: room full, leaving\n", id);
    }
    return NULL;
}
```

## 16. Industry Usage
- **Thread pools** (Java ThreadPoolExecutor, Go runtime): workers sleep on a work semaphore/CV; tasks are the customers.
- **Event loops / accept loops**: a server sleeps until a connection arrives (epoll/select) — the "barber sleeps" model.
- **I/O completion**: a thread waits on a completion semaphore (the rendezvous).
- **Queue workers**: single-consumer queues (loggers, database writers) that idle.
- **RTOS**: task synchronization with semaphores (FreeRTOS binary/counting) for exactly this pattern.

## 17. References
- Silberschatz, *OS Concepts*, 7.8.4 (Sleeping barber).
- Dijkstra (1965) — semaphore primitives.
- man: `sem_wait(3)`, `sem_post(3)`.
- FreeRTOS docs: semaphores and task synchronization.

## 18. Cheat Sheet
- 3 semaphores: customers (wake barber), barber (handoff), mutex (seats).
- Barber: wait(customers) → signal(barber) → free seat → cut.
- Customer: mutex → if seats: reserve, signal(customers), wait(barber); else leave.
- Idle server sleeps — no busy-wait.
- Rendezvous: customer & barber both block on each other.
- Capacity N → customers leave when full (backpressure).
- Semaphore count is sticky → no missed wakeups.
- Don't hold mutex while waiting on event semaphores (deadlock).
- Maps to worker/event-loop/thread-pool designs.

## 19. Quiz
1. Barber sleeps when: a) seats full b) customers == 0 c) mutex held d) busy → **b**
2. Number of semaphores: a) 1 b) 2 c) 3 d) 4 → **c**
3. `customers` semaphore serves to: a) count seats b) wake the barber c) lock d) priority → **b**
4. `barber` semaphore is the: a) mutex b) rendezvous/handoff c) capacity d) queue → **b**
5. Full room → customer: a) waits b) leaves c) sleeps d) spins → **b**
6. Idle barber: a) polls b) sleeps c) spins d) exits → **b**
7. Sticky signal means: a) missed wake b) no missed wakeups c) overwrite d) lost → **b**
8. Holding mutex while waiting on event sem → a) fine b) deadlock c) faster d) race → **b**
9. This pattern matches: a) thread pools b) sorting c) malloc d) disk → **b**
10. Capacity N gives: a) overflow b) backpressure c) infinite d) priority → **b**

## 20. Flashcards
- **Q: Barber sleeps when?** → **A:** customers == 0.
- **Q: Semaphores?** → **A:** customers, barber, mutex.
- **Q: customers does?** → **A:** Wakes the barber.
- **Q: barber does?** → **A:** Rendezvous handoff.
- **Q: Full room?** → **A:** Customer leaves.
- **Q: Idle server?** → **A:** Sleeps (no busy-wait).
- **Q: Sticky signal?** → **A:** No missed wakeups.
- **Q: Deadlock risk?** → **A:** Holding mutex while waiting on event.

## 21. Revision
The sleeping barber models an idle single server: the barber blocks on `customers` (sleeps when idle), a customer reserves a seat under `mutex`, signals `customers`, then rendezvous via `barber` (the barber signals ready, the customer waits for it). Full room → customer leaves (bounded backpressure). Three semaphores express wake + handoff + capacity; no busy-waiting; sticky counts prevent missed wakeups. This is the template for thread pools, event loops, and single-consumer queues.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is the sleeping barber?" | 13 Q1 / 2 How Does It Work |
| "Why three semaphores?" | 13 Q2 / 7 Formal Definition |
| "What is the rendezvous?" | 13 Q3 / 7 Formal Definition |
| "Why sleep instead of poll?" | 13 Q4 / 5 Intuition |
| "Signal before wait?" | 13 Q5 / 9 Internal Working |
| "Why leave when full?" | 13 Q6 / 6 Real-World Analogy |
| "Relation to producer-consumer?" | 13 Q7 / 7 Formal Definition |
| "Worker thread sleep/wake pattern?" | 13 Q8 / 3 When Is It Used |
| "Can the barber miss a customer?" | 13 Q9 / 9 Internal Working |
| "Deadlock risk?" | 13 Q12 / 12 Disadvantages |
