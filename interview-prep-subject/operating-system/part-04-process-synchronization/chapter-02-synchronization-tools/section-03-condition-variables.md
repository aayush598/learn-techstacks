# Section 03: Condition Variables

> **TL;DR**: A condition variable lets a thread wait for a *state change* while atomically releasing a mutex: `wait(mutex, cond)` blocks until another thread `signal(cond)`/`broadcast(cond)`. The crucial rule — always check the condition in a loop (while, not if) and use signal when exactly one waiter can proceed, broadcast otherwise.

## 1. Why Does This Exist?
A mutex alone can't express "wait until a queue is non-empty" — you'd have to spin/poll, wasting CPU, or sleep incorrectly. A condition variable exists to make *waiting for a predicate* correct and efficient: the thread atomically releases the mutex and sleeps (so others can make the state change), then wakes and re-checks. It's the standard primitive for producer-consumer, thread pools, and any "wait until X happens" logic.

## 2. How Does It Work?
- Used *with* a mutex.
- `pthread_cond_wait(&cond, &mutex)`: atomically (1) release mutex, (2) sleep on cond. On wakeup: (3) re-acquire mutex, (4) return.
- `pthread_cond_signal(&cond)`: wake *one* waiter.
- `pthread_cond_broadcast(&cond)`: wake *all* waiters.
- **Rule**: the predicate (e.g., `!queue.empty()`) must be checked in a `while` loop around wait — because of spurious wakeups and lost-wakeup races.
- **Rule**: signal only while holding the mutex (common practice) and only if a waiter exists.

## 3. When Is It Used?
- Wait-for-state patterns: producer waits when the buffer is full; consumer waits when empty; worker waits for work items.
- Thread pools: workers wait for tasks, dispatcher signals.
- Any condition that's a *state* (buffer non-empty, flag set, data available) rather than a count/resource (that's semaphore territory).

## 4. Why Wasn't Another Approach Chosen?
- **Polling/busy-wait**: wastes CPU and adds latency. Rejected.
- **Semaphore signaling**: expresses "event happened" but the count can accumulate and doesn't map cleanly to predicates; CVs are designed for *state* waiting. Both exist because they solve different problems.
- **Sleep with a fixed timeout**: fragile and slow. Rejected.
- **Monitors**: CVs *are* the monitor's condition mechanism; the standalone CV is the portable version.
CV wins because it couples mutex release + sleep + predicate recheck into one correct atomic operation — eliminating lost-wakeup races.

## 5. Intuition
**Waiting for your number to be called at a deli counter**: you "wait" (leave the counter and sit down — release the mutex) until the clerk calls your number (signal). When called, you get up (re-acquire the mutex) and *check the ticket* again — because maybe they called another number that just happened to be displayed too, or you got woken for the wrong reason (spurious wakeup). So you always verify the condition after waking.

## 6. Real-World Analogy
**A bus stop with a queue**: each passenger "waits" for the bus (the wait call parks them, letting the stop's bench — the mutex — be used by others). The bus arriving is the signal (waking one passenger). But buses can be crowded — when a passenger wakes, they must *check again* whether there's actually room (re-check the predicate in a while loop); a full bus means re-waiting. Broadcasting = a shuttle calls all waiting passengers at once (each then re-checks room).

## 7. Formal Definition
- **Condition variable**: a synchronization object on which a thread waits until another signals that a condition may be true. Not a lock itself — always paired with a mutex.
- **wait(cond, mutex)**: atomically release mutex, enqueue on cond's wait list, sleep. On wake: reacquire mutex.
- **signal(cond)**: wake one waiting thread (if any).
- **broadcast(cond)**: wake all waiting threads.
- **Mesa semantics** (most systems, incl. POSIX): waiter re-checks predicate after wakeup (signal is a hint). **Hoare semantics**: waiter runs immediately with predicate guaranteed (signal transfers lock).
- **Lost wakeup**: if signal happens between the predicate check and wait's sleep, the waiter misses it — prevented because wait releases the mutex *atomically with sleeping*, and the predicate is only checked under the mutex.

## 8. Example
**Producer-consumer with a bounded queue**:
```
producer:  lock(m); while (queue.full()) cond_wait(&not_full, &m);
           enqueue(); cond_signal(&not_empty); unlock(m);
consumer:  lock(m); while (queue.empty()) cond_wait(&not_empty, &m);
           item = dequeue(); cond_signal(&not_full); unlock(m);
```
- `while` (not `if`): multiple consumers + spurious wakes → must re-check.
- Wait atomically drops the lock so producers can run.
- Signal wakes a waiter; broadcast wakes all (safe when many waiters).

## 9. Internal Working
1. User thread calls cond_wait under the mutex; it adds itself to the CV's wait queue; kernel-level: futex wait on a wake word *after* dropping the mutex — glibc does a futex wait keyed on the CV.
2. The mutex is released atomically with the sleep decision (no lost wakeup: the producer's signal either happens before we sleep — then the predicate changed and our re-check succeeds — or after we're asleep — then futex wakes us).
3. signal/broadcast: futex wake one/all — threads re-acquire the mutex (they contend for it) and return from wait.
4. Spurious wakeup: the thread may wake without any signal (signals, scheduler) — hence the `while` loop.
5. Implementation is futex-based in glibc; kernel cond vars similar (wait queue + wake).

## 10. Time Complexity
- wait: O(1) (futex wait + enqueue) + reacquire.
- signal/broadcast: O(1) per waiter; broadcast wakes all → O(k) woken threads contend.
- Total wakeup latency ≈ syscall + scheduling (µs) — the cost of not busy-waiting.

## 11. Advantages
- Efficient blocking (no CPU waste) for state-waiting.
- Atomic release+sleep prevents lost-wakeup races.
- Works with any predicate; composable.
- Broadcast enables multi-consumer correctness.
- Portable across languages (pthread, C++ std::condition_variable, Java wait/notify).

## 12. Disadvantages
- **Easy to misuse**: forgetting `while` (or the mutex) causes lost wakes/races.
- Signal vs broadcast choice matters: signal with multiple waiters of different predicates → lost wakeup (must broadcast or use per-predicate CVs).
- Mesa semantics mean the predicate can change after wakeup (needs re-check).
- Heavier than a mutex (syscall when actually waiting).
- Priority handling: no built-in ordering (plain FIFO usually).

## 13. Interview Questions
1. **Q: What is a condition variable?** A: A wait/signal object used with a mutex to wait for a state predicate: wait atomically releases the mutex and sleeps; signal/broadcast wakes waiters.
2. **Q: Why must you wait in a loop (while, not if)?** A: Mesa semantics + spurious wakeups mean the condition may be false when you wake — always re-check the predicate.
3. **Q: wait's atomicity?** A: cond_wait atomically releases the mutex and sleeps, preventing lost wakeup (a signal in between can't be missed).
4. **Q: Signal vs broadcast?** A: signal wakes one waiter; broadcast wakes all. Use broadcast when multiple waiters could proceed or predicates differ; signal when exactly one can consume.
5. **Q (TRICKY): What is a lost wakeup?** A: A signal occurring between the predicate check and the sleep — the waiter misses it and sleeps forever. Avoided because wait drops the mutex atomically with sleeping, and the predicate is checked under the mutex.
6. **Q: What is a spurious wakeup?** A: A wakeup with no corresponding signal (OS/signal handling); the while loop handles it safely.
7. **Q: Mesa vs Hoare semantics?** A: Mesa (POSIX/Java): signal is a hint — waiter re-checks; Hoare: waiter runs immediately with the condition guaranteed. Mesa is simpler and used everywhere.
8. **Q (SCENARIO): Producer-consumer with multiple consumers — signal or broadcast?** A: With identical predicates, signal is fine (one consumes); if consumers wait on different predicates, broadcast (or one CV per predicate) to avoid missing wakeups.
9. **Q: Can a CV be used without a mutex?** A: No — the mutex protects the predicate; wait must atomically drop it so state can change; without it, races on the predicate.
10. **Q: How is a CV implemented in Linux?** A: Futex-based in glibc (pthread_cond_wait uses futex wait/wake with a sequence number); kernel CVs use wait queues + wake_up.
11. **Q: What happens if you signal with no waiters?** A: Nothing — the signal is lost. That's why the predicate is checked under the mutex (the producer's enqueue changes the state; the consumer re-checks it).
12. **Q (TRICKY): Two threads wait; one signal. Which runs?** A: One waiter wakes, re-acquires the mutex (contending with any other holder), re-checks the predicate, and proceeds. The other waits for its own wake.

## 14. Follow-Up Questions
1. **Q: Difference between CV and semaphore?** A: CV = wait on a *state* (with mutex, no count); semaphore = wait on a *count* (signal consumes). For events, semaphores count occurrences; CVs signal state changes.
2. **Q: What is the "forgotten predicate" bug?** A: Waiting without checking the condition — you wake only on the first signal and may act on stale state. Always check the predicate in the loop.
3. **Q: How does Java relate?** A: `Object.wait()/notify()/notifyAll()` inside `synchronized` — the same semantics; notifyAll ≈ broadcast (Java's recommended default for safety).
4. **Q: What is the "thundering herd"?** A: broadcast wakes many waiters, but only some can proceed (predicate) — others re-wait; wasteful but correct. 
5. **Q: How do C++ std::condition_variable_any differ?** A: Works with any lockable (not just std::mutex); same semantics.

## 15. Coding Example
```c
/* Bounded producer-consumer with mutex + condition variables */
#include <pthread.h>
#include <stdio.h>

#define CAP 4
int buf[CAP], head = 0, count = 0;
pthread_mutex_t m = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t not_full = PTHREAD_COND_INITIALIZER;
pthread_cond_t not_empty = PTHREAD_COND_INITIALIZER;

void produce(int item) {
    pthread_mutex_lock(&m);
    while (count == CAP)                /* while, not if */
        pthread_cond_wait(&not_full, &m);
    buf[(head + count) % CAP] = item;
    count++;
    pthread_cond_signal(&not_empty);    /* wake a consumer */
    pthread_mutex_unlock(&m);
}

int consume(void) {
    pthread_mutex_lock(&m);
    while (count == 0)
        pthread_cond_wait(&not_empty, &m);
    int item = buf[head];
    head = (head + 1) % CAP;
    count--;
    pthread_cond_signal(&not_full);     /* wake a producer */
    pthread_mutex_unlock(&m);
    return item;
}
```
```c
/* Broadcasting to all waiters */
pthread_mutex_lock(&m);
pthread_cond_broadcast(&shutdown_cond);   /* wake all workers to exit */
pthread_mutex_unlock(&m);
```

## 16. Industry Usage
- **Thread pools** (Java ExecutorService, Go runtime internals, .NET ThreadPool): workers wait on a condition, dispatcher signals.
- **Message queues**: consumers wait for messages; producers signal.
- **DB connection pools**: wait-for-free-connection via CV.
- **OS scheduling**: kernel wait queues + wake_up are the CV equivalent.
- **Async I/O completions**: wait for completions.

## 17. References
- Silberschatz, *OS Concepts*, 7.6 (Condition Variables).
- man: `pthread_cond_wait(3)`, `pthread_cond_signal(3)`, `pthread_cond_broadcast(3)`.
- Linux/glibc: futex-based condvar implementation.
- C++: `std::condition_variable` (cppreference).

## 18. Cheat Sheet
- CV + mutex, always.
- wait: atomically drop mutex + sleep; reacquire on wake.
- signal: wake one; broadcast: wake all.
- **while(predicate) wait(...)** — never if.
- Lost wakeup: signal between check & sleep → prevented by atomic drop.
- Spurious wakeup: re-check predicate.
- Mesa semantics: signal is a hint.
- Producer-consumer: not_full / not_empty CVs.
- Broadcast when many/different predicates; signal when one consumer.
- No CV without a mutex.

## 19. Quiz
1. CV is used with: a) semaphore b) mutex c) spinlock d) no lock → **b**
2. wait atomically: a) sleeps only b) releases mutex + sleeps c) spins d) signals → **b**
3. Spurious wakeup handled by: a) if b) while re-check c) sleep d) ignore → **b**
4. Signal wakes: a) all b) one c) none d) self → **b**
5. Lost wakeup prevented by: a) broadcast b) atomic mutex-drop c) spin d) timer → **b**
6. Mesa semantics: a) guaranteed b) hint → re-check c) no wake d) instant → **b**
7. Broadcast wakes: a) one b) all c) none d) two → **b**
8. Multiple consumers, same predicate: a) broadcast needed b) signal ok c) both bad d) no CV → **b**
9. CV without mutex: a) fine b) races on predicate c) faster d) kernel-only → **b**
10. Signal with no waiters: a) queues b) lost c) crashes d) spins → **b**

## 20. Flashcards
- **Q: CV + what?** → **A:** Mutex (protects predicate).
- **Q: wait does?** → **A:** Atomic drop-mutex + sleep.
- **Q: while or if?** → **A:** while (spurious + Mesa).
- **Q: signal vs broadcast?** → **A:** One vs all.
- **Q: Lost wakeup?** → **A:** Missed signal; fixed by atomic drop.
- **Q: Spurious wakeup?** → **A:** Re-check predicate.
- **Q: Mesa?** → **A:** Signal is a hint.
- **Q: No waiters signal?** → **A:** Lost — hence predicate check.

## 21. Revision
Condition variables make *state waiting* correct and efficient: paired with a mutex, cond_wait atomically releases the lock and sleeps (no lost wakeup), and on wake the thread re-acquires and re-checks the predicate in a `while` loop (spurious wakeups, Mesa semantics). signal wakes one waiter, broadcast all — choose broadcast when predicates differ or many can proceed. Implementation is futex-based (glibc). CVs are the backbone of thread pools, queues, and producer-consumer designs; the biggest interview trap is `if` instead of `while`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a condition variable?" | 13 Q1 / 7 Formal Definition |
| "Why while, not if?" | 13 Q2 / 5 Intuition / 8 Example |
| "wait's atomicity?" | 13 Q3 / 9 Internal Working |
| "Signal vs broadcast?" | 13 Q4 / 7 Formal Definition |
| "Lost wakeup?" | 13 Q5 / 8 Example |
| "Spurious wakeup?" | 13 Q6 / 12 Disadvantages |
| "Mesa vs Hoare?" | 13 Q7 / 7 Formal Definition |
| "Multi-consumer signal/broadcast?" | 13 Q8 / 8 Example |
| "CV without mutex?" | 13 Q9 / 12 Disadvantages |
| "How implemented in Linux?" | 13 Q10 / 9 Internal Working |
