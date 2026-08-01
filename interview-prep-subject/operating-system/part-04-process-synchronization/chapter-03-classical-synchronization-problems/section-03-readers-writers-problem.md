# Section 03: Readers-Writers Problem

> **TL;DR**: Many readers can read shared data concurrently; writers need exclusive access. Two flavors: readers-priority (readers never wait on writers — writer starvation) and writers-priority (writers don't starve — readers may). The classic solution uses a reader-count + mutex + a read/write semaphore; the modern answer is an RW lock or seqlock.

## 1. Why Does This Exist?
Read-mostly data (config tables, caches, routing tables) shouldn't serialize: two readers reading the same value is *safe*, so blocking them wastes the whole point of a shared cache. The readers-writers problem formalizes "many readers or one writer" — an RW lock. It exists because the naive "one mutex for everything" kills read parallelism, and because the naive "unlimited readers" lets writers starve forever. Real systems need both: parallel reads *and* guaranteed writer progress.

## 2. How Does It Work?
**Readers-priority (first flavor)**:
- `readcount` (shared, guarded by `mutex`), `rw_mutex` (binary).
- Reader: `P(mutex); readcount++; if (readcount==1) P(rw_mutex); V(mutex);` read; `P(mutex); readcount--; if (readcount==0) V(rw_mutex); V(mutex);`
- Writer: `P(rw_mutex); write; V(rw_mutex);`
- The *first* reader takes the writer lock (so subsequent readers join without blocking); the *last* reader releases it. Writers must wait for all readers to finish.
**Writers-priority (second flavor)**: a writer-waiting flag/counter makes new readers wait if a writer is pending.

## 3. When Is It Used?
- Read-mostly shared data: caches, config, lookup tables, routing tables.
- Databases: many-reader concurrent access, one writer.
- File systems: read-mostly metadata.
- pthread `pthread_rwlock_t`, Java `ReentrantReadWriteLock`, Linux rwsem/seqlock.
- Preference policy chosen by workload: read-heavy with rare writes → readers-priority; writers must be timely → writers-priority.

## 4. Why Wasn't Another Approach Chosen?
- **Single mutex**: correct but serializes all reads — unacceptable for read-mostly. Rejected.
- **Readers-priority (naive)**: readers never block writers→writer starvation. Rejected for write timeliness.
- **Writers-priority**: writers jump ahead — readers can starve under write floods. Rejected for read-heavy balance.
- **Seqlock/RCU**: lock-free reads (retry or defer) — excellent for read-mostly but complex; RW locks are the pragmatic default.
The chosen design: **RW lock with a configurable preference** — parallel readers by default, with writer-priority variants when writers matter.

## 5. Intuition
**A library reading room**: many people can read at once (readers share), but only one person edits the books (writer). If readers keep streaming in, the librarian never gets a chance to fix the shelves (writer starvation). So the rule is either "readers always get seats first" (readers-priority) or "if the librarian is waiting, don't let more readers in until they've worked" (writers-priority).

## 6. Real-World Analogy
**A wiki page**: any number of people can view it simultaneously (reads). Only one editor can save changes (write), and while saving, no one can view a half-updated version (writer excludes readers). If thousands of viewers stream in, the editor could starve forever (readers-priority problem); wikis implement "an edit is pending → stop new reads of the old version" (writers-priority) so edits always land.

## 7. Formal Definition
- **Shared**: data D; **readers**: all read D concurrently; **writers**: exclusive.
- **First flavor (readers-priority)**: no reader waits for a writer; writers may starve.
  - `readcount` + `mutex` (guards readcount) + `rw_mutex` (binary).
  - Reader: P(mutex); ++readcount; if (readcount == 1) P(rw_mutex); V(mutex); read; P(mutex); --readcount; if (readcount == 0) V(rw_mutex); V(mutex).
  - Writer: P(rw_mutex); write; V(rw_mutex).
- **Second flavor (writers-priority)**: if a writer is waiting, new readers block → readers may starve under write floods.
- **Invariants**: (readers ≥ 1 ⇒ no writer active) and (writer active ⇒ readers == 0).

## 8. Example
Readers-priority trace: readers=0, rw_mutex free.
- R1: readcount 0→1, takes rw_mutex, reads. [enter]
- R2: readcount 1→2 (≠1, no wait), reads. [enter — parallel!]
- W: P(rw_mutex) blocks (readcount ≥ 1). [waits]
- R1: readcount→1; R2: readcount→0, releases rw_mutex. [last reader releases]
- W: acquires rw_mutex, writes. [writer enters]
Key: writers can't enter until all readers leave; readers never block on pending writers.

## 9. Internal Working
1. `readcount` increments/decrements under `mutex` (a small critical section of its own).
2. The first reader acquires the writer lock, making later readers "piggyback" — only one writer-lock acquisition per reader batch.
3. The last reader releases the writer lock, letting a waiting writer in.
4. Writers-priority: a `writercount`/flag makes the *next* reader wait if a writer is queued — new readers arrive behind the writer.
5. Real implementations (pthread_rwlock, Linux rwsem): futex-based, writer-first wait queue, plus a "reader/writer bias" config.

## 10. Time Complexity
- Reader fast path: O(1) — atomic readcount inc, no contention on the writer lock.
- Writer: O(1) acquisition (if no readers) + wait for readers to drain.
- Under read concurrency: excellent (readers parallel); writer waits O(readers) to drain.
- Starvation: readers-priority can postpone writers unboundedly; writers-priority can postpone readers.

## 11. Advantages
- Parallel reads → big win on read-mostly workloads (a mutex would serialize).
- Simple model, maps to pthread_rwlock/ReentrantReadWriteLock.
- Policy selection: choose priority flavor for your writer cadence.
- seqlock variant gives lock-free reads.

## 12. Disadvantages
- Writer starvation (readers-priority) or reader starvation (writers-priority) — policy-dependent.
- Shared `readcount` is itself a contention point (cacheline).
- Writers wait for ALL readers to drain — write latency unbounded under read load.
- Heavier than a plain mutex; write-heavy workloads do worse.
- No ordering guarantees without extra queuing (fairness variant: queued writers/readers).

## 13. Interview Questions
1. **Q: What is the readers-writers problem?** A: Many readers can access shared data concurrently, but a writer needs exclusive access; solution must allow parallel reads and serialized writes.
2. **Q: Why can't a plain mutex solve it well?** A: It serializes all readers too — read-mostly data loses all parallelism. The RW lock shares reads.
3. **Q: How does readers-priority work?** A: A readcount (guarded by a mutex) tracks active readers; the first reader takes the writer lock, the last releases it. Readers never wait for writers.
4. **Q: What's the downside of readers-priority?** A: Writer starvation — a stream of readers postpones the writer forever.
5. **Q (TRICKY): How does writers-priority avoid writer starvation?** A: If a writer is waiting, new readers are blocked until the writer completes — writers jump the reader queue.
6. **Q: Why does the first reader acquire the writer lock?** A: To gate writers: as long as any reader is active, the writer lock is held; subsequent readers just increment readcount (no lock contention).
7. **Q: Why does the last reader release the writer lock?** A: When readcount hits 0, no readers remain — a waiting writer can now proceed.
8. **Q (PRODUCTION): A config cache is read 1000x/sec and written 1x/hour. Which flavor?** A: Readers-priority (or a seqlock/RCU) — writers are rare, starvation is a non-issue; maximize read throughput.
9. **Q: What is a seqlock here?** A: Writers bump a sequence; readers read optimistically and retry if the sequence changed — lock-free reads, at the risk of retry. Great for read-mostly.
10. **Q: When is a plain mutex better than an RW lock?** A: Write-heavy or balanced workloads — the readcount cacheline contention makes RW locks slower than a simple mutex.
11. **Q: How does pthread_rwlock relate?** A: `pthread_rwlock_rdlock/wrlock/unlock` — the OS-level RW lock with configurable preference (default is typically writer-preferring/fair).
12. **Q (TRICKY): Can both readers-priority and writers-priority deadlock?** A: No — with the correct implementation (no circular wait), neither deadlocks; they only risk *starvation* of one side, which is the policy tradeoff.

## 14. Follow-Up Questions
1. **Q: What's a "fair" RW lock?** A: Queues both readers and writers (FIFO) so neither class can leapfrog — bounds starvation for both.
2. **Q: What's the difference between an RW lock and RCU?** A: RCU readers run lock-free and writers defer reclamation until all old readers leave (grace period) — better read scaling, more complexity.
3. **Q: How do databases implement readers-writers?** A: Row-level read locks (shared) and write locks (exclusive); MVCC gives readers a consistent snapshot without blocking writers.
4. **Q: What is the "read-copy-update" grace period?** A: The time until all pre-update readers finish; reclamation happens after it — the RCU mechanism.
5. **Q: What happens to write latency under continuous reads with readers-priority?** A: Unbounded — the writer waits indefinitely; that's exactly why writers-priority/fair variants exist.

## 15. Coding Example
```c
/* Readers-writers, readers-priority (classic semaphore solution) */
#include <pthread.h>
#include <semaphore.h>

sem_t rw_mutex, mutex;
int readcount = 0;

void reader(void) {
    sem_wait(&mutex);
    readcount++;
    if (readcount == 1) sem_wait(&rw_mutex);   /* first reader gates writer */
    sem_post(&mutex);

    /* read shared data */

    sem_wait(&mutex);
    readcount--;
    if (readcount == 0) sem_post(&rw_mutex);   /* last reader frees writer */
    sem_post(&mutex);
}

void writer(void) {
    sem_wait(&rw_mutex);
    /* write shared data (exclusive) */
    sem_post(&rw_mutex);
}
```
```c
/* pthread RW lock: the practical API */
#include <pthread.h>
pthread_rwlock_t rw = PTHREAD_RWLOCK_INITIALIZER;

void read_path(void)  { pthread_rwlock_rdlock(&rw); /* read */ pthread_rwlock_unlock(&rw); }
void write_path(void) { pthread_rwlock_wrlock(&rw); /* write */ pthread_rwlock_unlock(&rw); }
```

## 16. Industry Usage
- **Linux kernel**: rwsem (filesystem metadata), seqlock (timekeeping), RCU (read-mostly paths).
- **Databases**: read/write transactions; MVCC for modern systems.
- **Caches**: local cache invalidation (write path) vs lookup (read path).
- **Java**: ReentrantReadWriteLock, StampedLock.
- **Config services**: read-mostly config caches with rare updates.

## 17. References
- Silberschatz, *OS Concepts*, 7.8.2 (Readers-writers).
- Courtois et al., "Concurrent control with readers and writers" (1971).
- man: `pthread_rwlock_rdlock(3)`, `pthread_rwlock_wrlock(3)`.
- Linux: `kernel/locking/rwsem.c`, seqlock, RCU docs.

## 18. Cheat Sheet
- Readers parallel; writer exclusive.
- readcount + mutex + rw_mutex.
- First reader takes rw_mutex; last reader releases it.
- Readers-priority: readers never wait → writer starvation.
- Writers-priority: writers jump ahead → reader starvation possible.
- Fair variant: FIFO queue for both.
- seqlock: optimistic reads, retry on seq change.
- RCU: lock-free reads, deferred reclamation.
- RW beats mutex only when read-heavy (≥ ~10:1).
- No deadlock in correct impls — only starvation policy.

## 19. Quiz
1. Readers can: a) exclude each other b) run concurrently c) write d) wait → **b**
2. First reader: a) waits b) takes writer lock c) sleeps d) exits → **b**
3. Last reader: a) exits b) releases writer lock c) writes d) spins → **b**
4. Readers-priority starves: a) readers b) writers c) both d) none → **b**
5. Writers-priority starves: a) writers b) readers c) both d) none → **b**
6. readcount guarded by: a) rw_mutex b) mutex c) semaphore d) spin → **b**
7. seqlock reads: a) lock b) optimistic + retry c) sleep d) wait → **b**
8. RW beats mutex when: a) write-heavy b) read-heavy c) equal d) never → **b**
9. Fair RW lock: a) FIFO b) priority c) random d) none → **b**
10. Writers-priority fix: a) more readers b) block new readers while writer waits c) fewer writers d) spin → **b**

## 20. Flashcards
- **Q: Problem?** → **A:** Many readers OR one writer.
- **Q: First reader?** → **A:** Takes writer lock.
- **Q: Last reader?** → **A:** Releases writer lock.
- **Q: Readers-priority?** → **A:** Writer starvation.
- **Q: Writers-priority?** → **A:** Reader starvation risk.
- **Q: seqlock?** → **A:** Optimistic reads, retry.
- **Q: When RW?** → **A:** Read-heavy (≥10:1).
- **Q: Starvation?** → **A:** Policy-dependent, not deadlock.

## 21. Revision
The readers-writers problem needs parallel readers plus exclusive writers. The classic solution uses readcount (under a mutex) and a binary rw_mutex: the first reader takes the writer lock, the last releases it. Preference policy is the design axis — readers-priority (writers starve), writers-priority (readers may starve), or fair FIFO. Modern tools: pthread_rwlock, Java ReentrantReadWriteLock, and for extreme read-mostly, seqlocks (optimistic reads) or RCU (lock-free reads). Correct implementations never deadlock — the risk is starvation, which is why preference matters.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is readers-writers?" | 13 Q1 / 7 Formal Definition |
| "Why not a plain mutex?" | 13 Q2 / 4 Why Wasn't Another Approach Chosen |
| "How does readers-priority work?" | 13 Q3 / 2 How Does It Work |
| "Downside of readers-priority?" | 13 Q4 / 12 Disadvantages |
| "Writers-priority mechanics?" | 13 Q5 / 2 How Does It Work |
| "Why first reader takes writer lock?" | 13 Q6 / 7 Formal Definition |
| "Why last reader releases?" | 13 Q7 / 9 Internal Working |
| "Config cache read-heavy — which?" | 13 Q8 / 3 When Is It Used |
| "What is a seqlock?" | 13 Q9 / 7 Formal Definition |
| "When is mutex better?" | 13 Q10 / 12 Disadvantages |
