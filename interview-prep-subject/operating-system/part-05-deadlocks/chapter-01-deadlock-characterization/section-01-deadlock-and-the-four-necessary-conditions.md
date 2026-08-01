# Section 01: Deadlock and the Four Necessary Conditions

> **TL;DR**: A deadlock is when every thread in a set waits for a resource held by another thread in the set — nothing can proceed. Four conditions are all necessary: mutual exclusion, hold-and-wait, no preemption, and circular wait. Break any one and deadlock becomes impossible; that's the basis of deadlock prevention.

## 1. Why Does This Exist?
Concurrency without deadlock awareness is a ticking bug: one wrong lock order and a production system freezes permanently, with every thread blocked. Deadlock theory exists to (1) *recognize* the failure mode precisely, (2) *prove* the conditions that make it possible, and (3) give engineers a toolkit — prevention, avoidance, detection — to make systems robust. Every locking library, database, and kernel has deadlock-avoidance built in for exactly this reason.

## 2. How Does It Work?
- A deadlock is characterized by the **wait-for** relationship: thread A waits for a resource B holds; B waits for C; ... back to A.
- **Four necessary conditions** (Coffman et al. 1971), ALL must hold:
  1. **Mutual exclusion** — resources are non-shareable (only one holder at a time).
  2. **Hold-and-wait** — a thread holds resources while waiting for more.
  3. **No preemption** — resources can't be forcibly taken from a holder.
  4. **Circular wait** — a cycle of threads each waiting on the next's resource.
- If any condition is absent, deadlock can't occur (necessary, not sufficient: all four can hold without deadlock).

## 3. When Is It Used?
- Analyzing lock-heavy code (two mutexes in conflicting orders — Part 04 philosophers).
- Database transactions (row locks), filesystem locks, network resource allocation.
- Diagnosing production freezes ("all threads blocked in lock_wait").
- Designing OS resources: memory, files, printers, semaphores — any non-preemptible, exclusive resource.

## 4. Why Wasn't Another Approach Chosen?
- **Just preventing it by discipline ("be careful")**: insufficient at scale — bugs slip in. Rejected.
- **Single global lock**: eliminates cycles but kills concurrency. Rejected.
- **Copy resources instead of locking**: works sometimes but impractical for mutable shared state. Rejected.
- **The four-conditions framework**: chosen because it's *actionable* — prevention breaks one condition (atomic acquisition kills hold-and-wait; ordering kills circular wait; preemption handles "no preemption"). It turns an invisible bug into an engineering checklist.

## 5. Intuition
**Four drivers at a four-way intersection, each needing the road the other holds**: no one can move because each waits for the car in front to clear a road they're holding. That's circular wait (the cycle). If any single thing changed — roads could be shared (no ME), a driver could back up (preemption), or one driver refused to enter until all roads were free (no hold-and-wait) — the gridlock dissolves.

## 6. Real-World Analogy
**A meeting-room booking trap**: Team A holds Room 1 and waits for Room 2; Team B holds Room 2 and waits for Room 1. No team can get both rooms; both meetings are blocked forever. Conditions: rooms are exclusive (ME), each team holds one while waiting for the other (hold-and-wait), nobody's evicted (no preemption), A→B→A circular wait. Fixing any one — share rooms, book both at once, or evict on a deadline — resolves it.

## 7. Formal Definition
- **Deadlock**: a set of threads D such that each thread T ∈ D waits for a resource held by some thread in D; no thread in D can release resources it holds without receiving a resource it waits for → permanent blocking.
- **Necessary conditions** (all four):
  1. **Mutual exclusion**: each resource is assigned to at most one thread at a time (or is non-shareable).
  2. **Hold-and-wait**: a thread holding at least one resource waits to acquire others.
  3. **No preemption**: a resource cannot be forcibly removed; only the holder releases it voluntarily.
  4. **Circular wait**: a cycle T0 → T1 → ... → Tn → T0 exists where Ti waits for a resource held by Ti+1.
- **Not sufficient**: all four can hold without deadlock (e.g., threads can always finish eventually).
- **Starvation vs deadlock**: starvation = some thread never gets a resource but others progress; deadlock = no one in the set progresses.

## 8. Example
Threads T1, T2; resources R1, R2.
```
T1: lock(R1); lock(R2); ...
T2: lock(R2); lock(R1); ...
Interleave: T1 grabs R1, T2 grabs R2; then T1 waits for R2 (held by T2),
T2 waits for R1 (held by T1). Circular wait: T1→R2→T2→R1→T1. Deadlock.
```
Conditions: R1/R2 exclusive (ME ✓), each holds one while waiting (hold-and-wait ✓), no preemption ✓, cycle ✓. All four → deadlock.

## 9. Internal Working
1. A lock's `lock()` call blocks the thread (futex wait / spin) — the "waits for" edge.
2. The resource graph (allocation + request edges) builds up; a **cycle** in the wait-for projection indicates deadlock potential.
3. Detection: OS/database scans the wait-for graph for cycles (or uses timeouts).
4. Prevention: code/enforcement layer prevents one condition (e.g., lockdep enforces global ordering).
5. Recovery: on detected cycle, abort a thread or preempt/rollback a resource.

## 10. Time Complexity
- Detection via wait-for graph: O(V+E) DFS cycle detection.
- Timeout-based detection: O(1) per waiter.
- Prevention (ordering): O(1) per acquisition (with lockdep checking O(lock set)).
- Recovery: O(1) per aborted thread (rollback cost varies).

## 11. Advantages
- Precisely characterizes the failure — the four conditions make it diagnosable.
- Actionable: breaking one condition gives four independent prevention strategies.
- Applies across locks, DBs, filesystems, networks.
- Cycle-based detection is efficient (graph algorithms).

## 12. Disadvantages
- Conditions are *necessary*, not sufficient — a system can satisfy all four yet never deadlock (over-conservative analysis).
- Prevention costs: atomic acquisition/ordering restrict concurrency; preemption needs rollback support.
- Detection + recovery is expensive and disruptive (aborts).
- Real systems rarely have single-instance resources — cycles in multi-instance graphs don't guarantee deadlock.

## 13. Interview Questions
1. **Q: What is a deadlock?** A: A set of threads, each waiting for a resource held by another in the set — no one can progress; permanent blocking.
2. **Q: What are the four necessary conditions?** A: Mutual exclusion, hold-and-wait, no preemption, circular wait. All four must hold for deadlock.
3. **Q: Why are they "necessary" and not sufficient?** A: A system can satisfy all four yet never deadlock (e.g., threads happen to finish); the conditions are required, not guaranteed, for deadlock.
4. **Q (TRICKY): Two threads lock two mutexes in opposite order. Deadlock?** A: Not necessarily — only if the specific interleaving happens (both grab their first lock before either grabs the second). The *potential* is there; the four conditions describe the danger.
5. **Q: Deadlock vs starvation?** A: Deadlock: all in the set block — no progress for anyone in the set. Starvation: some thread never gets the resource but others keep progressing.
6. **Q: Give the classic lock-order deadlock.** A: T1 locks A then B; T2 locks B then A. Interleaved, T1 holds A waits B, T2 holds B waits A — circular wait.
7. **Q: What does "hold-and-wait" mean?** A: Holding one resource while waiting to acquire another — the thread doesn't release what it has before requesting more.
8. **Q: Why does mutual exclusion matter?** A: If resources were shareable (readers), threads wouldn't block each other — no wait-for edges. Non-shareable resources are the precondition.
9. **Q (PRODUCTION): All threads stuck in mutex_lock. How do you diagnose?** A: Dump the wait-for state: each thread's held locks + what it waits for (gdb/thread dumps, lockdep). Find the cycle; look for opposite lock ordering.
10. **Q: Can semaphores deadlock?** A: Yes — same four conditions apply; e.g., two counting semaphores acquired in conflicting order (the philosophers setup).
11. **Q: Is a cycle in the wait-for graph always deadlock?** A: With single-instance resources, yes (each edge is a definite wait). With multi-instance, a cycle is *necessary but not sufficient* — a resource with free instances could break it.
12. **Q (TRICKY): Does disabling preemption prevent deadlock?** A: It reduces hold-and-wait windows but doesn't remove the cycle; deadlock can still occur if a thread blocks on a lock while holding another (user mode). Preemption control is about scheduling, not deadlock.

## 14. Follow-Up Questions
1. **Q: What is the wait-for graph?** A: A directed graph T→T' if T waits for a resource held by T' — the allocation graph projected onto threads; cycles = deadlock (single-instance).
2. **Q: How do timeouts relate?** A: A lock-acquire timeout lets a thread abandon and retry — it converts "wait forever" into "back off," addressing no-preemption indirectly (still requires rollback).
3. **Q: What is lock ordering?** A: A total order on locks; every thread acquires in that order → no cycles → no deadlock. This breaks condition 4.
4. **Q: What is "attack one condition"?** A: Each prevention strategy targets one condition: share (1), atomic acquire (2), preempt/rollback (3), order (4).
5. **Q: How do databases apply this?** A: Row locks are exclusive (ME); transactions hold locks while acquiring more (hold-and-wait); DBs detect cycles (deadlock victim rollback) — detection + recovery.

## 15. Coding Example
```c
/* Demonstrating a deadlock (runs forever) — for teaching only */
#include <pthread.h>
#include <stdio.h>

pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t B = PTHREAD_MUTEX_INITIALIZER;

void *t1(void *arg) {
    pthread_mutex_lock(&A);
    usleep(1000);                    /* encourage the bad interleave */
    pthread_mutex_lock(&B);          /* T1 holds A, waits B */
    printf("t1 done\n");
    pthread_mutex_unlock(&B);
    pthread_mutex_unlock(&A);
    return NULL;
}
void *t2(void *arg) {
    pthread_mutex_lock(&B);
    usleep(1000);
    pthread_mutex_lock(&A);          /* T2 holds B, waits A */
    printf("t2 done\n");
    pthread_mutex_unlock(&A);
    pthread_mutex_unlock(&B);
    return NULL;
}

int main(void) {
    pthread_t p1, p2;
    pthread_create(&p1, NULL, t1, NULL);
    pthread_create(&p2, NULL, t2, NULL);
    pthread_join(p1, NULL);          /* never returns: deadlock */
    pthread_join(p2, NULL);
    return 0;
}
```
Fix: both threads acquire in the SAME order (A then B) — breaks the cycle.

## 16. Industry Usage
- **Linux**: lockdep statically checks lock ordering (breaks circular wait); RT mutexes handle inversion.
- **Databases** (Postgres, MySQL, Oracle): detect deadlocks and abort a victim transaction (detection + recovery).
- **Distributed systems**: leader election + distributed locks (etcd/ZooKeeper) with leases (preemption via expiry).
- **Java**: synchronized/lock ordering by convention; LockSupport, tryLock to avoid cycles.
- **Filesystems**: inode/superblock lock ordering tables.

## 17. References
- Coffman, Elphick, Shoshani, "System Deadlocks" (Computing Surveys 1971).
- Silberschatz, *OS Concepts*, Ch. 8 (Deadlocks).
- Tanenbaum, *Modern OS*, Ch. 6 (Deadlocks).
- Linux: `tools/locking/lockdep.c`, `Documentation/locking/`.

## 18. Cheat Sheet
- Deadlock = all in a set block, each waits on another's resource.
- Four conditions (all necessary): ME, hold-and-wait, no preemption, circular wait.
- Necessary ≠ sufficient.
- Classic: two locks in opposite order.
- Wait-for graph: T→T' = T waits on T's-held-by-T'; cycle = deadlock (single-instance).
- Deadlock vs starvation: all blocked vs some blocked.
- Break any condition → prevention.
- Detection: DFS cycle O(V+E); timeouts.
- DBs: detect + abort victim.
- lockdep: static lock-ordering enforcement.

## 19. Quiz
1. Deadlock means: a) some blocked b) all in set blocked permanently c) slow d) priority → **b**
2. Conditions count: a) 2 b) 3 c) 4 d) 5 → **c**
3. Hold-and-wait means: a) wait only b) hold while waiting c) share d) preempt → **b**
4. Cycle in wait-for graph (single-instance): a) possible b) deadlock c) safe d) starve → **b**
5. Necessary vs sufficient: a) same b) necessary only c) sufficient only d) unrelated → **b**
6. Break one condition: a) still deadlock b) prevents c) slows d) no effect → **b**
7. Deadlock vs starvation: a) same b) different c) opposites d) none → **b**
8. Classic cause: a) lock order b) semaphore size c) memory d) I/O → **b**
9. DBs handle via: a) prevention b) detect+abort c) ignore d) lock-free → **b**
10. lockdep enforces: a) ME b) lock ordering c) preemption d) timeouts → **b**

## 20. Flashcards
- **Q: Deadlock?** → **A:** Set of threads each waiting on another's resource — all blocked.
- **Q: Four conditions?** → **A:** ME, hold-and-wait, no preemption, circular wait.
- **Q: Necessary vs sufficient?** → **A:** All four required, not sufficient.
- **Q: Classic example?** → **A:** Two locks in opposite order.
- **Q: Wait-for cycle?** → **A:** Deadlock (single-instance).
- **Q: Starvation?** → **A:** Some blocked, others progress.
- **Q: Fix?** → **A:** Break any condition.
- **Q: DB approach?** → **A:** Detect + abort victim.

## 21. Revision
A deadlock is permanent blocking: a set of threads where each waits for a resource another holds. Four necessary conditions — mutual exclusion, hold-and-wait, no preemption, circular wait — must all hold; the classic manifestation is two locks acquired in opposite order (the dining philosophers). The wait-for graph reveals cycles that are deadly for single-instance resources. Prevention breaks one condition (atomic acquire, lock ordering, preemption), avoidance (Banker's) checks safety beforehand, and detection+recovery (databases abort victims) is the pragmatic fallback.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a deadlock?" | 13 Q1 / 7 Formal Definition |
| "Four conditions?" | 13 Q2 / 7 Formal Definition |
| "Necessary not sufficient?" | 13 Q3 / 7 Formal Definition |
| "Opposite lock order — deadlock?" | 13 Q4 / 8 Example |
| "Deadlock vs starvation?" | 13 Q5 / 7 Formal Definition |
| "Classic example?" | 13 Q6 / 8 Example |
| "What is hold-and-wait?" | 13 Q7 / 7 Formal Definition |
| "Diagnose all threads stuck?" | 13 Q9 / 16 Industry Usage |
| "Can semaphores deadlock?" | 13 Q10 / 12 Disadvantages |
| "Cycle always deadlock?" | 13 Q11 / 10 Time Complexity |
