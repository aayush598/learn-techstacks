# Section 01: Deadlock Prevention

> **TL;DR**: Prevention makes deadlock *impossible* by breaking one of the four conditions: share resources (ME), acquire everything at once (hold-and-wait), allow preemption/rollback (no preemption), or enforce a global lock order (circular wait). Each fix has a cost — the ordering rule (breaking circular wait) is the one real systems actually use.

## 1. Why Does This Exist?
The strongest deadlock defense is to make the failure *unreachable*. Prevention exists because detection + recovery is expensive and disruptive, and because a disciplined design can guarantee — by construction — that the four conditions can never all hold. It's the "belt-and-suspenders" philosophy: rather than detect a frozen system, design a system that can't freeze. Linux lock ordering (enforced by lockdep) and "acquire locks in a fixed order" conventions are prevention in practice.

## 2. How Does It Work?
Break exactly one of the four conditions:
1. **Mutual exclusion** → make resources shareable (readers/writers instead of exclusive; spooling for printers). Only works for some resources.
2. **Hold-and-wait** → request ALL resources before starting (or release everything and retry). Kills concurrency (a thread can't proceed until it has everything).
3. **No preemption** → allow the OS to steal a resource (with rollback/undo) when a deadlock would occur; requires the resource state be saveable/restorable.
4. **Circular wait** → impose a total order on resources (R1 < R2 < ...); every thread acquires strictly in that order → no cycle possible. This is the practical favorite.

## 3. When Is It Used?
- **Lock ordering**: kernels (lockdep), databases (index/row ordering), filesystems (inode order) — the standard.
- **Resource sharing**: where exclusive access is unnecessary (reader-writer locks, spooling).
- **Transactional systems**: hold-and-wait via transactions (all-or-nothing) with rollback.
- **Embedded/RTOS**: bounded, well-defined resource sets → prevention is affordable.

## 4. Why Wasn't Another Approach Chosen?
- **Detection + recovery**: works but aborts/rollbacks are disruptive (users lose work) — rejected as the primary strategy for safety-critical paths.
- **Banker's avoidance**: needs full future knowledge (max claim per thread) — rarely available. Rejected for general use.
- **Do nothing**: deadlocks happen; production incidents. Rejected.
- **Prevention (ordering)**: chosen because a *static rule* (always lock in order) has near-zero runtime cost and eliminates the failure class — the best risk/benefit in practice.

## 5. Intuition
**Elevator etiquette rule**: "always take the elevator from floor 1 to your floor; never call it downward past you." If everyone follows one order, no two people can block each other's ride (no circular wait). Alternatively, "book all three rooms before the meeting" (hold-and-wait broken — but now one meeting hoards all rooms). Or "anyone can be asked to give up a room" (preemption — but that wastes setups).

## 6. Real-World Analogy
**A highway merge rule**: to prevent gridlock, the rule "always yield to the right" — or a strict merge order — ensures no circular blocking pattern can form. Compare with the intersection-gridlock example (Part 05 Ch 1 Sec 1): one simple ordering rule (always take the left road first) makes the four-way deadlock structurally impossible. Cost: cars must sometimes wait even when a road is clear (the ordering restriction).

## 7. Formal Definition
- **Prevention**: design the system so at least one necessary condition can never hold.
- **Break ME**: non-shareable → shareable (read-only copies, spooled output).
- **Break hold-and-wait**: a thread requests all resources in one atomic step before starting; or releases all and retries on failure. Cost: low resource utilization, potential starvation.
- **Break no preemption**: if a thread requests a held resource, the OS may preempt (withdraw) it from the holder, which rolls back; the holder then re-requests. Requires resource state save/restore.
- **Break circular wait**: assign a total order R1 < R2 < ... < Rm; each thread acquires resources in increasing order. No cycle can form (cycle would require a descending acquisition). Cost: flexibility loss; a thread may hold a lower-ordered resource while waiting for a higher one — but that's exactly the (allowed) non-circular pattern.

## 8. Example
Resources R1 < R2 < R3. Rule: acquire in increasing order.
- T1: lock(R1) then lock(R2) — OK.
- T2: must lock R2 only after R1 if it holds R1; it may lock R2 then R3.
- Could T1 hold R1 waiting R2, and T2 hold R2 waiting R1? T2 can't — it holds R2, meaning it already acquired R2 before R1? T2 could hold R2 only if it acquired R1 first (order) — but R1 is held by T1. So T2 can't hold R2 while T1 holds R1 → no cycle → no deadlock.

## 9. Internal Working
1. **Lock ordering**: `lockdep` instruments every lock acquire, builds a lock graph, and warns (or panics) on a detected ordering inversion — statically enforcing the order rule at runtime.
2. **Atomic request**: acquire all resources under a single meta-lock, or pre-scan and hold all before use.
3. **Preemption/rollback**: on conflict, the OS saves the resource's state, revokes it, lets the waiter use it, and restores it — CPU registers (context switch) and memory (virtual memory paging) are the classic preemptible resources.
4. **Total order assignment**: designers map resources to integers (e.g., by type/address); code must acquire in that order; violations are code-review/lockdep errors.

## 10. Time Complexity
- Lock ordering: O(1) per acquire (plus lockdep O(lock set) checking when enabled).
- Atomic multi-resource acquire: O(r) to acquire r resources (no retries if one step).
- Preemption: O(state save/restore) per preemption.
- No asymptotic cost — the cost is *concurrency/utilization*, not time.

## 11. Advantages
- Deadlock is **impossible** — no runtime detection needed.
- Simple to reason about and enforce (a rule, not a solver).
- Deterministic, low overhead.
- lockdep makes violations catchable at development time.

## 12. Disadvantages
- **Ordering restricts flexibility**: a thread may hold a low resource while waiting for a high one (reduced concurrency).
- **Atomic acquisition hurts utilization**: threads hoard resources (hold-and-wait broken but wasteful).
- **Preemption needs rollback support**: not all resources are saveable.
- Shareability has limits: exclusive hardware can't be shared.
- Starvation risk (a thread perpetually re-requesting).

## 13. Interview Questions
1. **Q: What is deadlock prevention?** A: Making at least one of the four necessary conditions impossible — so deadlock can never occur — via sharing, atomic acquisition, preemption, or lock ordering.
2. **Q: How do you prevent circular wait?** A: Total order on resources; every thread acquires in increasing order — no cycle can form.
3. **Q: What does breaking hold-and-wait look like?** A: Request all resources in one atomic step before running, or release everything and retry if blocked. Cost: lower utilization, hoarding.
4. **Q: What does breaking no preemption look like?** A: The OS can withdraw a resource from a holder (with state save/rollback), letting the waiting thread proceed. Needs reversible resources.
5. **Q (TRICKY): Why is lock ordering the practical favorite?** A: Near-zero runtime cost (a static rule), no rollback machinery, and easy to enforce (lockdep) — unlike preemption (needs save/restore) or atomic acquisition (hurts concurrency).
6. **Q: Can you break mutual exclusion?** A: For some resources: make them shareable (readers-writers), or spool output to a buffer device so no exclusive hold is needed. Hardware exclusives can't be shared.
7. **Q: What's the cost of ordering?** A: Flexibility/concurrency — a thread can hold a lower-ordered resource while waiting for a higher one; that's the (safe) non-circular pattern.
8. **Q: What is lockdep?** A: A Linux lock-ordering validator that instruments acquisitions and flags cyclic orderings — statically preventing this deadlock class.
9. **Q (PRODUCTION): A DB gives "deadlock detected, retry" — is that prevention?** A: No — that's detection + recovery (it finds the cycle and aborts a victim). Prevention would be ordering transactions so the cycle can't form.
10. **Q: Does prevention eliminate starvation?** A: No — hold-and-wait broken can cause a thread to wait indefinitely for a full set of resources; ordering doesn't guarantee fairness either.
11. **Q: Why is prevention better than detection for safety-critical code?** A: Determinism — the failure is structurally impossible; detection only finds it *after* it happens (and recovery is disruptive).
12. **Q (TRICKY): If ME, hold-and-wait, and no preemption all hold but threads are ordered, can deadlock still occur?** A: No — the cycle (circular wait) is impossible under a total ordering, and all four are required. Deadlock is prevented even though three conditions remain.

## 14. Follow-Up Questions
1. **Q: What's the difference between prevention and avoidance?** A: Prevention breaks a condition structurally (deadlock impossible). Avoidance (Banker's) checks each grant against a *safe state* criterion using max claims — deadlock avoided at runtime.
2. **Q: What is starvation from prevention?** A: E.g., atomic acquisition: a thread that can never gather all resources waits forever; needs aging/ordering fairness.
3. **Q: How do databases order locks?** A: Sort tables/rows by key (or index order) so all transactions acquire in the same order — the ordering rule.
4. **Q: What's a "total order" vs "partial order"?** A: Total: every resource pair is comparable (any two have an order). Partial: some incomparable (only a subset ordered) — still prevents cycles if respected.
5. **Q: What's the role of spooling?** A: Printers etc. are made "shareable" by spooling to disk — the exclusive device is only touched by the spooler, breaking ME at the application level.

## 15. Coding Example
```c
/* Lock ordering: always acquire A before B — prevention of circular wait */
#include <pthread.h>
#include <stdio.h>

#define ORDER_A 1   /* lower order */
#define ORDER_B 2   /* higher order */

pthread_mutex_t A = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t B = PTHREAD_MUTEX_INITIALIZER;

/* Rule: if you need both A and B, acquire A (lower) first, then B. */
void ordered_work(void) {
    pthread_mutex_lock(&A);    /* lower order first */
    pthread_mutex_lock(&B);    /* higher order second */
    /* critical section */
    pthread_mutex_unlock(&B);
    pthread_mutex_unlock(&A);
}

/* Never write: lock(B); lock(A);  <-- violates ordering, deadlock risk */
```
```bash
# lockdep reports ordering violations at boot/development
dmesg | grep -i "possible circular locking"
```

## 16. Industry Usage
- **Linux kernel**: `LOCKDEP` (lock ordering validation), documented lock hierarchies (mm→fs→net etc.).
- **Databases**: index/key-ordered lock acquisition.
- **Filesystems**: inode→superblock ordering.
- **RTOS**: fixed resource sets with defined acquisition order.
- **Distributed**: consistent ordering of distributed locks (etcd transaction ordering).

## 17. References
- Coffman et al. (1971) — the conditions; prevention derivations.
- Silberschatz, *OS Concepts*, 8.3 (Deadlock Prevention).
- Linux: `Documentation/locking/lockdep-design.rst`.
- Tanenbaum, *Modern OS*, 6.1 (deadlock prevention).

## 18. Cheat Sheet
- Prevention = break one of the 4 conditions.
- Break ME: share/spool.
- Break hold-and-wait: atomic acquire (cost: hoarding).
- Break no preemption: revoke + rollback (needs saveable state).
- Break circular wait: total order on resources (the practical one).
- Ordering cost: reduced flexibility/concurrency.
- lockdep enforces ordering statically.
- Prevention ≠ fairness (starvation still possible).
- Prevention = no runtime detection needed.
- Not to be confused with detection/avoidance.

## 19. Quiz
1. Prevention breaks: a) one condition b) all c) none d) detection → **a**
2. Ordering breaks: a) ME b) hold-and-wait c) circular wait d) preemption → **c**
3. Atomic acquisition breaks: a) ME b) hold-and-wait c) ordering d) nothing → **b**
4. Spooling breaks: a) ME b) circular wait c) preemption d) share → **a**
5. Preemption needs: a) ordering b) save/restore c) more locks d) share → **b**
6. lockdep enforces: a) ME b) ordering c) preemption d) timeouts → **b**
7. Ordering cost: a) deadlock b) concurrency/flexibility c) memory d) speed → **b**
8. Prevention removes: a) starvation b) deadlock possibility c) races d) memory → **b**
9. "Deadlock detected, retry" is: a) prevention b) detection+recovery c) avoidance d) ordering → **b**
10. Ordering guarantees: a) fairness b) no circular wait c) speed d) sharing → **b**

## 20. Flashcards
- **Q: Prevention?** → **A:** Break one of four conditions.
- **Q: Ordering breaks?** → **A:** Circular wait.
- **Q: Atomic acquire?** → **A:** Hold-and-wait.
- **Q: Spooling?** → **A:** Mutual exclusion.
- **Q: Preemption needs?** → **A:** Save/restore (rollback).
- **Q: lockdep?** → **A:** Ordering validator.
- **Q: Cost?** → **A:** Concurrency/flexibility.
- **Q: Still possible?** → **A:** Starvation (not deadlock).

## 21. Revision
Prevention eliminates deadlock by construction: break one necessary condition. Sharing/spooling kills ME, atomic acquisition kills hold-and-wait (at hoarding cost), revocation + rollback kills no preemption (needs reversible resources), and a total resource order kills circular wait — the cheap, enforceable favorite, backed by lockdep. Prevention guarantees no deadlock but not fairness (starvation remains). It's the deterministic alternative to Banker's avoidance and to database-style detection + recovery.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is prevention?" | 13 Q1 / 7 Formal Definition |
| "Prevent circular wait?" | 13 Q2 / 7 Formal Definition |
| "Break hold-and-wait?" | 13 Q3 / 2 How Does It Work |
| "Break no preemption?" | 13 Q4 / 2 How Does It Work |
| "Why ordering is practical?" | 13 Q5 / 4 Why Wasn't Another Approach Chosen |
| "Break mutual exclusion?" | 13 Q6 / 2 How Does It Work |
| "What is lockdep?" | 13 Q8 / 9 Internal Working |
| "DB 'retry' — prevention?" | 13 Q9 / 16 Industry Usage |
| "Prevention vs starvation?" | 13 Q10 / 12 Disadvantages |
| "Three conditions + ordering?" | 13 Q12 / 8 Example |
