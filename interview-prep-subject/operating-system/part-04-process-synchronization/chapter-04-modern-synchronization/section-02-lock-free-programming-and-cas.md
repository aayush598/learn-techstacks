# Section 02: Lock-Free Programming and CAS

> **TL;DR**: Lock-free programming uses atomic operations (CAS) with retry loops so threads make progress without blocking — at least one thread always advances. The hazards are the ABA problem (version tags), memory-ordering errors, and bounded progress under contention; the payoff is no lock contention, no context-switch stalls, and scalability on multicore.

## 1. Why Does This Exist?
Locks serialize and can stall (context switch, priority inversion, convoy). For high-throughput, low-latency systems — kernels, databases, message queues — even a well-tuned mutex costs too much under contention. Lock-free programming exists to make *the data structure itself* safe with atomic instructions: threads never block; they retry. The result: no lock overhead, no deadlock, and graceful behavior under contention. It's how Linux RCU, Java's ConcurrentHashMap, and high-performance queues achieve their scale.

## 2. How Does It Work?
- **Core primitive**: `compare_and_swap(addr, expected, new)` — atomically swap if unchanged.
- **Pattern**: `do { old = load(addr); new = f(old); } while (!CAS(addr, old, new));` — optimistic: compute from a snapshot, retry if someone changed it.
- **Memory ordering**: acquire/release semantics ensure data published under a CAS is visible correctly (no reordering into the atomic).
- **Progress classes**: 
  - *Obstruction-free*: if a thread runs alone it completes (retries only while others interfere).
  - *Lock-free*: at least one thread makes progress in any scheduling; no thread is blocked forever (system-wide progress).
  - *Wait-free*: every thread completes in a bounded number of steps (strongest).

## 3. When Is It Used?
- **Kernel**: RCU read paths (lock-free reads), seqlocks, refcounts (atomic_dec_and_test), sequence counters.
- **Data structures**: concurrent stacks, queues (Michael-Scott), hash maps (Java ConcurrentHashMap), skip lists.
- **Counters/timestamps**: atomic increments for stats, sequence numbers.
- **Reference counting**: atomic refcounts (never block).
- Any hot path where lock contention dominates.

## 4. Why Wasn't Another Approach Chosen?
- **Mutexes**: serialize, stall on context switch, invert priorities, convoy. Rejected for ultra-hot paths.
- **Pure reads (immutable)**: safest but writers can't update in place — copy-on-write + CAS (RCU) is the pragmatic middle.
- **Single-writer assumption**: simple but limited; CAS generalizes to MPMC.
- **Transactional memory**: elegant but not hardware-supported at scale yet; CAS is the practical atomic.
The chosen design: **optimistic concurrency via CAS + retry** — no blocking, no lock state, with carefully ordered memory operations.

## 5. Intuition
**Two people filling a shared form**: each reads the current version (old), fills in their changes (new), and writes with a "check that it's still the version I read" (CAS). If someone else changed it first, you re-read and redo (retry). Nobody ever waits for anybody else — you just keep trying. The guarantee: at least one person's write succeeds each round (lock-free progress).

## 6. Real-World Analogy
**An online seat-selection screen**: you pick seats (read old), the system checks if they're still free and books them atomically (CAS); if someone grabbed one, you're told to re-select (retry). Nobody queues — everyone tries simultaneously, and the atomic booking guarantees only one person gets a given seat. The system always progresses (someone books), even under a stampede.

## 7. Formal Definition
- **CAS**: `bool CAS(T* addr, T expected, T new)` — atomic: if `*addr == expected`, `*addr = new`, return true; else false.
- **Lock-free**: a system in which at least one thread is guaranteed to make progress in every finite schedule (no thread can prevent others' progress indefinitely). No blocking waits.
- **Wait-free**: every thread completes in bounded steps regardless of others.
- **ABA problem**: a thread reads A, another changes A→B→A, the first CAS succeeds wrongly (it sees A but the world changed). Fix: tag/version the word (e.g., `stamp | pointer`), or DCAS.
- **Memory order**: CAS ops pair with acquire/release; publish under release, read under acquire.
- **Hazard pointers / epoch-based reclamation**: safely free memory a thread may still be reading (ABA + use-after-free for lock-free memory management).

## 8. Example
**Lock-free stack (Treiber's)**:
```
push(x): do { old = top; x.next = old; } while (!CAS(&top, old, x));
pop():   do { old = top; if (!old) return EMPTY;
              new = old->next; } while (!CAS(&top, old, new));
         return old;   // needs safe reclamation (hazard ptrs)
```
- Push never blocks — it just retries if `top` moved.
- Pop has the ABA problem (top A→B→A) → uses tagged pointers.

**Lock-free counter**: `while (!CAS(&c, (old=load(&c)), old+1));` — concurrent increments all succeed eventually (retry).

## 9. Internal Working
1. `old = load(addr)` (relaxed or acquire).
2. Compute `new` from `old`.
3. `CAS(addr, old, new)` — if fails, someone else wrote: loop back to 1.
4. On success, the write is published; readers with acquire loads see it.
5. Memory management: a node popped by one thread may be read by another — deferred reclamation (hazard pointers, epoch/RCU, or never-free arenas).
6. Contention: many threads CAS the same line → retry storms; mitigation: backoff, or per-thread structures.

## 10. Time Complexity
- CAS itself: O(1) atomic (tens of ns, cacheline locked).
- Lock-free operation: O(retries) — expected O(1) under low contention; under heavy contention retries grow (worst case unbounded, but progress is still guaranteed lock-free).
- Wait-free: O(bounded steps) per thread.
- Cacheline contention: high when many threads hammer one word (the scaling bottleneck).

## 11. Advantages
- **No blocking** — no context switches, no priority inversion, no deadlock.
- **Scalable** under contention (vs locks that serialize).
- **Graceful degradation** — retries, not stalls.
- Composable primitives (counters, queues, stacks).
- Enables RCU-style read-heavy designs (lock-free reads).

## 12. Disadvantages
- **Hard to get right**: memory ordering, ABA, reclamation bugs are subtle.
- **ABA problem** needs version tags or DCAS.
- **Retry loops** waste CPU under heavy contention (bounded, but can thrash).
- **Cacheline contention** can make lock-free slower than a good lock.
- **Memory reclamation** complexity (hazard pointers, RCU epochs).
- Non-wait-free: a thread can starve (no bounded steps guarantee in lock-free).

## 13. Interview Questions
1. **Q: What is lock-free programming?** A: Using atomic ops (CAS) so threads never block — they retry; guarantee: at least one thread always makes progress.
2. **Q: What does CAS do?** A: Atomically swaps `addr` to `new` if it equals `expected`, returning success — the optimistic-update primitive.
3. **Q: What is the retry loop pattern?** A: `do { old = load(addr); new = f(old); } while (!CAS(addr, old, new));` — recompute if someone changed it.
4. **Q: What is the ABA problem?** A: A thread reads A; another changes A→B→A; the first's CAS sees A and succeeds, but the structure changed underneath. Fix: version/tag the word (e.g., `stamp|pointer`).
5. **Q: Difference between lock-free and wait-free?** A: Lock-free: at least one thread progresses (others may retry). Wait-free: *every* thread completes in bounded steps — stronger.
6. **Q (TRICKY): Why is memory ordering important in lock-free code?** A: Without acquire/release, the CPU/compiler can reorder a data write past the CAS that publishes it — a reader could see the CAS but not the data. Order the operations.
7. **Q: How do you safely free a popped node?** A: Deferred reclamation — hazard pointers, epoch-based reclamation, or RCU — because another thread may still read it (use-after-free and ABA).
8. **Q (PRODUCTION): A lock-free queue shows retry storms under load. Fix?** A: Backoff (exponential), shard by thread, or switch to a queued/blocking design — lock-free isn't automatically faster under extreme contention.
9. **Q: What is Treiber's stack?** A: The classic lock-free stack: push/pop retry on CAS of the top pointer; pop needs tagged pointers (ABA) and hazard-pointer reclamation.
10. **Q: When is a lock better than lock-free?** A: Low contention (lock fast path is cheap), complex mutations, or when memory management dominates. Lock-free wins at high contention and in real-time/latency-critical paths.
11. **Q: What is RCU?** A: Read-copy-update: writers copy, modify, CAS-publish; readers run lock-free; old versions are reclaimed after a grace period — the ultimate read-mostly lock-free pattern.
12. **Q (TRICKY): Can a lock-free algorithm deadlock?** A: No blocking, so no classic deadlock — but it can *live-lock* (retries) under adversarial scheduling; wait-free eliminates that.

## 14. Follow-Up Questions
1. **Q: What is a "seqlock" in lock-free terms?** A: Writers bump a sequence, readers retry on change — the writer isn't blocked by readers (optimistic read).
2. **Q: What are "hazard pointers"?** A: Per-thread registered pointers; a thread sets a hazard pointer before reading a node so reclamation can't free it — used for safe memory reclamation in lock-free structures.
3. **Q: What is an "atomic fetch-and-add" vs CAS?** A: F&A atomically increments; CAS conditionally updates. F&A is better for counters/tickets; CAS is general.
4. **Q: What is "DCAS"/"double-CAS"?** A: Atomically CAS two words (not universally supported) — solves ABA in some designs.
5. **Q: What's the difference between lock-free and non-blocking?** A: "Non-blocking" is the umbrella; lock-free guarantees system progress; obstruction-free guarantees only solo progress; wait-free guarantees per-thread bounded progress.

## 15. Coding Example
```c
/* Lock-free counter with C11 atomics (CAS retry loop) */
#include <stdatomic.h>
#include <pthread.h>
#include <stdio.h>

atomic_long counter = 0;

void bump(void) {
    long old, want;
    do {
        old = atomic_load(&counter);
        want = old + 1;
    } while (!atomic_compare_exchange_weak(&counter, &old, want));
}

void *worker(void *arg) {
    for (int i = 0; i < 1000000; i++) bump();
    return NULL;
}

int main(void) {
    pthread_t t[4];
    for (int i = 0; i < 4; i++) pthread_create(&t[i], NULL, worker, NULL);
    for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);
    printf("counter = %ld\n", atomic_load(&counter));
    return 0;
}
```
```c
/* Treiber's lock-free stack (concept; full impl needs hazard pointers) */
#include <stdatomic.h>
typedef struct node { int val; struct node *next; } node;
atomic_node_p top = NULL;

void push(int v) {
    node *n = malloc(sizeof(node));
    n->val = v;
    node *old;
    do { old = atomic_load(&top); n->next = old; }
    while (!atomic_compare_exchange_weak(&top, &old, n));
}
```

## 16. Industry Usage
- **Linux kernel**: RCU (read-side lock-free), seqlocks, atomic refcounts, per-CPU counters.
- **Java**: `ConcurrentHashMap` (CAS + volatile), `AtomicReference`, `LongAdder` (stripe to avoid contention).
- **Go**: atomic package; sync.Map uses CAS-backed read path.
- **C++**: std::atomic, libstdc++ lock-free queues.
- **Databases**: lock-free queues (MPSC/SPSC), optimistic concurrency control (CAS on versions).

## 17. References
- Herlihy & Shavit, *The Art of Multiprocessor Programming* (CAS, lock-free, wait-free, ABA, hazard pointers).
- Treiber, "Systems Programming: Coping with Parallelism" (1986) — lock-free stack.
- Michael & Scott, "Simple, fast, and practical non-blocking and blocking concurrent queue algorithms" (1996).
- McKenney (RCU): `linux-kernel/RCU` docs and papers.
- Intel SDM / cppreference: atomics, memory order.

## 18. Cheat Sheet
- CAS: atomic compare-and-swap → optimistic updates.
- Pattern: load old → compute new → CAS → retry on fail.
- Lock-free: ≥1 thread progresses; no blocking.
- Wait-free: every thread bounded steps.
- ABA: A→B→A; fix with version/tag or DCAS.
- Memory order: acquire/release around publishing CAS.
- Reclamation: hazard pointers / epochs / RCU.
- Treiber's stack: CAS on top; pop needs tags + hazard pointers.
- Seqlock: optimistic reads + retry.
- Retry storms at high contention → backoff/sharding.
- No deadlock, but possible livelock.

## 19. Quiz
1. CAS conditionally writes when: a) != expected b) == expected c) always d) never → **b**
2. Lock-free guarantees: a) all progress b) at least one progresses c) none d) sleep → **b**
3. Wait-free: a) at least one b) every thread bounded steps c) none d) blocking → **b**
4. ABA fix: a) mutex b) version tag c) spin d) sleep → **b**
5. Memory ordering: a) optional b) required c) harmful d) slow → **b**
6. Popped node reuse risk: a) race b) use-after-free/ABA c) overflow d) priority → **b**
7. Hazard pointers: a) faster b) safe reclamation c) locking d) CAS → **b**
8. Retry loop pattern: a) while true b) do-while CAS c) for d) sleep → **b**
9. Seqlock readers: a) lock b) optimistic retry c) block d) spin → **b**
10. Lock-free deadlock: a) possible b) impossible c) common d) always → **b**

## 20. Flashcards
- **Q: CAS?** → **A:** Atomic compare-and-swap.
- **Q: Lock-free?** → **A:** ≥1 thread progresses, no blocking.
- **Q: Wait-free?** → **A:** Every thread bounded steps.
- **Q: ABA?** → **A:** A→B→A; fix = version tag.
- **Q: Memory order?** → **A:** Acquire/release around CAS.
- **Q: Reclamation?** → **A:** Hazard pointers / RCU.
- **Q: Treiber's stack?** → **A:** CAS on top pointer.
- **Q: Deadlock?** → **A:** Impossible (livelock possible).

## 21. Revision
Lock-free programming replaces locks with CAS retry loops: load a snapshot, compute, attempt the atomic swap, retry on failure. Progress guarantees: lock-free (someone always advances) vs wait-free (everyone bounded). Hazards: ABA (fix with version tags), memory ordering (acquire/release), and safe reclamation (hazard pointers/RCU). It powers RCU, ConcurrentHashMap, lock-free queues — and pays off at high contention or latency-critical paths, though retry storms mean it's not always faster than a good lock.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is lock-free programming?" | 13 Q1 / 7 Formal Definition |
| "What does CAS do?" | 13 Q2 / 7 Formal Definition |
| "Retry loop pattern?" | 13 Q3 / 2 How Does It Work |
| "ABA problem?" | 13 Q4 / 8 Example |
| "Lock-free vs wait-free?" | 13 Q5 / 7 Formal Definition |
| "Why memory ordering?" | 13 Q6 / 9 Internal Working |
| "Safe free of popped node?" | 13 Q7 / 9 Internal Working |
| "Retry storms fix?" | 13 Q8 / 12 Disadvantages |
| "Treiber's stack?" | 13 Q9 / 8 Example |
| "When is a lock better?" | 13 Q10 / 4 Why Wasn't Another Approach Chosen |
