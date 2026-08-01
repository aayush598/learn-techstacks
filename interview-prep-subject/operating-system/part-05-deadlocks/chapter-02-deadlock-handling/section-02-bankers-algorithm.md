# Section 02: Banker's Algorithm (Deadlock Avoidance)

> **TL;DR**: Banker's avoids deadlock by refusing any resource grant that would put the system into an *unsafe state* — one where no sequence of completions exists. It requires each process to declare its maximum future claim; the safety check runs in O(n²·m), which is why real OSes rarely use it but it's a classic interview favorite.

## 1. Why Does This Exist?
Prevention is cheap but restrictive; detection + recovery is disruptive. Banker's is the third path: *avoidance* — at every grant, check whether giving the resource keeps the system in a **safe state** (a state from which all processes can eventually finish). It exists because Dijkstra (1965) wanted a formally correct allocator: given each process's *maximum claim*, you can decide per-request whether granting it risks deadlock. It's the intellectual bridge between the RAG (state) and real allocation policy.

## 2. How Does It Work?
- Data: `Available` (vector of free resources), `Allocation[i]` (per process), `Max[i]` (per process's max claim), `Need[i] = Max[i] - Allocation[i]`.
- On request from P_i: check `Request <= Available`; tentatively grant; run the **safety algorithm**; if safe, commit; else deny and let P_i wait.
- **Safety algorithm**: repeatedly find a process whose `Need <= Work` (where Work = Available + freed allocations); simulate finishing it (Work += Allocation); if all finish → safe state.
- If no such process exists → unsafe → deny the grant.

## 3. When Is It Used?
- **Theoretically**: OS resource allocation (the textbook solution), where processes declare max claims.
- **Practically**: rarely in general-purpose OSes (claims are unknown/lying), but the *concept* appears in:
  - databases (optimistic concurrency / MVCC safety reasoning),
  - distributed resource schedulers (admission control with max requests),
  - embedded systems with fixed, declared resource needs.

## 4. Why Wasn't Another Approach Chosen?
- **Prevention**: cheaper but over-restrictive (ordering/hoarding). Banker's allows more concurrency when the system is in a safe state.
- **Detection + recovery**: finds deadlock after the fact (disruptive aborts). Banker's prevents *entering* unsafe states entirely.
- **Per-request O(n²·m) check**: the real-world killer — general OSes can't afford per-acquire safety scans with unknown maxima. Rejected for production; kept for correctness-bound niches.
Banker's is chosen where **max claims are known and the state must never be unsafe** — determinism beats throughput.

## 5. Intuition
**A bank cashier with a rule**: you declare your total credit limit upfront (max claim). The cashier never approves a loan that could, combined with others' limits, exhaust the vault (unsafe state) — even if the current request is affordable. The rule: "I will only approve if, even in the worst case, every customer can still eventually get all their money." That worst-case simulation is the safety check.

## 6. Real-World Analogy
**An airline oversell policy with declared itineraries**: each passenger's Max = the flights they might take. Before selling any seat, the system simulates the worst case — can every passenger still be accommodated (all complete)? If not, the sale is declined (unsafe). It's conservative: it denies some requests that would actually have worked, but it guarantees no one is ever stranded (no deadlock).

## 7. Formal Definition
- **Safe state**: a state for which there exists a sequence P1..Pn such that each Pi's Need can be satisfied from the resources Available + resources freed by P1..P(i-1). If such a sequence exists, no deadlock can occur from this state.
- **Unsafe state**: no such sequence exists — a deadlock *may* (not must) occur later.
- **Banker's request handling**:
  1. `if (Request_i > Need_i) error`.
  2. `if (Request_i > Available) wait`.
  3. Pretend to grant: `Available -= Request; Allocation_i += Request; Need_i -= Request`.
  4. Run safety check; if safe → grant; else → rollback the pretend and make P_i wait.
- **Safety algorithm**: 
  - `Work = Available`; `Finish[i] = false`.
  - Find i with `!Finish[i] && Need_i <= Work`; if found: `Work += Allocation_i; Finish[i] = true;` repeat.
  - If all Finish → safe.
- Complexity: O(n²·m) worst case (n processes, m resource types).

## 8. Example
n=5 (P0..P4), m=3 resources. Available = [3,3,2].
```
        Allocation   Max        Need
P0:     0 1 0       7 5 3      7 4 3
P1:     2 0 0       3 2 2      1 2 2
P2:     3 0 2       9 0 2      6 0 0
P3:     2 1 1       2 2 2      0 1 1
P4:     0 0 2       4 3 3      4 3 1
```
Safety: P1 (Need 1,2,2 ≤ 3,3,2): Work→5,3,2. P3 (0,1,1): Work→7,4,3. P4: →7,4,5. P0: →7,5,5. P2: →10,5,7. All finish → SAFE. Sequence <P1,P3,P4,P0,P2>.
If P1 then requests (1,0,2): Need 1,2,2 → available [2,3,0]; check → still safe → grant.

## 9. Internal Working
1. Maintain Available/Allocation/Max/Need matrices (shared kernel state).
2. Every `Request` runs the O(n²·m) safety check (find-a-completable-process loop).
3. The check is *conservative*: it only simulates completions; a safe state guarantees no deadlock, and unsafe states only *may* deadlock.
4. Real systems rarely do this per-acquire; they approximate with resource limits or per-domain allocation.
5. Distributed/DB variants: transaction managers check whether granting a lock could strand transactions (max-claim analog).

## 10. Time Complexity
- Safety check: O(n²·m) (n processes, m resource types).
- Request handling: O(n²·m) plus O(m) comparisons.
- Space: O(n·m) for the matrices.
- This per-request cost is the reason general OSes skip Banker's.

## 11. Advantages
- **Guarantees no deadlock** while allowing more concurrency than prevention.
- Formal, provable (safe-state theorem).
- Handles *any* resource types (uniform model).
- Conservative but correct — never grants into an unsafe state.

## 12. Disadvantages
- **Requires max claims** — processes must declare (and not exceed) their maximum; impractical/lying processes break it.
- O(n²·m) per request — too slow for high-frequency allocation.
- Resources must have *fixed* numbers (can't model dynamic resources like memory overcommit).
- Processes' requests must be independent and fixed for the analysis.
- Rarely implemented in real OSes — mostly theory/interviews.

## 13. Interview Questions
1. **Q: What is Banker's algorithm?** A: A deadlock-avoidance allocator that grants a request only if the resulting state is *safe* (some completion sequence exists for all processes, given declared max claims).
2. **Q: What is a safe state?** A: A state where there's an execution sequence in which every process can finish with the resources available + freed. Safe states can't deadlock.
3. **Q: Safe vs unsafe state?** A: Safe = a completion sequence exists (no deadlock possible). Unsafe = none exists (deadlock *may* occur). Unsafe doesn't imply deadlock.
4. **Q: Why does Banker's need max claims?** A: The safety check simulates the worst case (each process eventually needs its full Max) — without declared maxima there's nothing to simulate.
5. **Q: Walk through the safety check.** A: Work = Available; loop finding an unfinished process whose Need ≤ Work; add its Allocation to Work and mark finished; if all finish → safe.
6. **Q (TRICKY): What's the time complexity?** A: O(n²·m) — n processes, m resource types — the reason it's rarely used in real OSes.
7. **Q: Does an unsafe state mean deadlock?** A: No — only that a deadlock *could* occur depending on future requests; safe states rule it out entirely.
8. **Q: Why don't real OSes use Banker's?** A: Processes can't (or won't) declare accurate max claims; the per-request O(n²·m) check is too slow; resources are dynamic. It's used where claims are bounded and determinism matters.
9. **Q (PRODUCTION): Where does the idea survive?** A: Admission control and schedulers with declared budgets (kubernetes resource requests), DB transaction managers reasoning about lock granting, embedded systems with fixed resource sets.
10. **Q: What happens if a process exceeds its declared Max?** A: It breaks the model's guarantee — Banker's assumes claims are respected; exceeding could push the system into an unsafe state (contract violation).
11. **Q: How does Banker's compare to prevention?** A: Prevention forbids structures (ordering/atomic); Banker's permits any state that's safe — more concurrency, but needs the runtime check + max claims.
12. **Q (TRICKY): A request is affordable (Request ≤ Available) but the state becomes unsafe. What does Banker's do?** A: Deny and make the process wait — affordability isn't enough; safety (a completion sequence must still exist) is the criterion.

## 14. Follow-Up Questions
1. **Q: What's the difference between safe and deadlock-free?** A: A safe state guarantees no deadlock can occur from it; a deadlock-free system never deadlocks but individual states may be unsafe. Safe ⇒ deadlock-free from that state.
2. **Q: How does the safety algorithm avoid exponential search?** A: Greedy: repeatedly picking any completable process is sufficient (the order is interchangeable) — a polynomial O(n²·m) simulation.
3. **Q: Can Banker's handle multiple resource instances?** A: Yes — that's exactly what the vectors do (the RAG cycle criterion couldn't decide multi-instance; Banker's does).
4. **Q: What is "overcommit"?** A: Allocating more than physically available on the promise that not all Max claims are used simultaneously — the opposite of Banker's conservatism (that's why memory uses overcommit, not Banker's).
5. **Q: How do databases emulate it?** A: With declared transactions (known row sets), lock managers can refuse a grant that would strand another transaction — a max-claim admission policy.

## 15. Coding Example
```c
/* Banker's safety check (simplified) */
#include <stdio.h>
#include <stdbool.h>

#define N 5  /* processes */
#define M 3  /* resources */

int available[M] = {3,3,2};
int allocation[N][M] = {{0,1,0},{2,0,0},{3,0,2},{2,1,1},{0,0,2}};
int max[N][M]        = {{7,5,3},{3,2,2},{9,0,2},{2,2,2},{4,3,3}};

bool is_safe(void) {
    int work[M];
    bool finish[N] = {false};
    int safe_seq[N];
    for (int i = 0; i < M; i++) work[i] = available[i];

    int done = 0;
    while (done < N) {
        bool progress = false;
        for (int i = 0; i < N; i++) {
            if (finish[i]) continue;
            bool ok = true;
            for (int j = 0; j < M; j++)
                if (max[i][j] - allocation[i][j] > work[j]) { ok = false; break; }
            if (ok) {
                for (int j = 0; j < M; j++) work[j] += allocation[i][j];
                finish[i] = true; safe_seq[done++] = i; progress = true;
            }
        }
        if (!progress) return false;   /* no completable process -> unsafe */
    }
    printf("safe sequence: ");
    for (int i = 0; i < N; i++) printf("P%d ", safe_seq[i]);
    printf("\n");
    return true;
}

int main(void) {
    printf("%s\n", is_safe() ? "SAFE" : "UNSAFE");
    return 0;
}
```

## 16. Industry Usage
- **Theory/textbooks**: the canonical avoidance algorithm.
- **Kubernetes/schedulers**: resource *requests/limits* = max claims; admission control refuses overcommit at the pod level (a Banker's-like guarantee).
- **Databases**: transaction admission with declared read/write sets.
- **Embedded/RTOS**: fixed resource allocations with declared maxima (deterministic).
- **Research**: deadlock-avoidance literature builds on Banker's.

## 17. References
- Dijkstra, "Cooperating sequential processes" (1965) — Banker's algorithm.
- Silberschatz, *OS Concepts*, 8.5 (Deadlock Avoidance, Banker's).
- Tanenbaum, *Modern OS*, 6.1.3.
- Habermann, "Prevention of System Deadlocks" (1969) — safety analysis.

## 18. Cheat Sheet
- Avoidance = never grant into an unsafe state.
- Safe state: ∃ completion sequence (Work = Available; loop Need ≤ Work).
- Unsafe ≠ deadlock (may deadlock later).
- Matrices: Available, Allocation, Max, Need = Max − Allocation.
- Request: check ≤ Need, ≤ Available; pretend-grant; safety check; commit or rollback+wait.
- Complexity: O(n²·m).
- Requires declared max claims (rarely available).
- Not used in general OSes (too slow, claims unknown).
- Survives in schedulers/admission control with declared budgets.
- Safe ⇒ no deadlock from that state.

## 19. Quiz
1. Banker's avoids: a) races b) unsafe states c) starvation d) preemption → **b**
2. Safe state means: a) fast b) completion sequence exists c) no locks d) share → **b**
3. Unsafe state: a) deadlock guaranteed b) may deadlock c) no deadlock d) impossible → **b**
4. Need = a) Max+Alloc b) Max−Alloc c) Alloc−Max d) Available → **b**
5. Safety complexity: a) O(n) b) O(n²·m) c) O(nm) d) O(n³) → **b**
6. Banker's requires: a) timeouts b) max claims c) ordering d) preemption → **b**
7. Request ≤ Available but unsafe: a) grant b) deny/wait c) ignore d) rollback always → **b**
8. Safe state deadlock: a) possible b) impossible c) certain d) random → **b**
9. Real OSes: a) use it b) rarely c) always d) for memory → **b**
10. Overcommit is: a) Banker's b) opposite of conservative c) same d) prevention → **b**

## 20. Flashcards
- **Q: Banker's?** → **A:** Avoidance via safe-state checks.
- **Q: Safe state?** → **A:** ∃ completion sequence.
- **Q: Unsafe?** → **A:** May deadlock, not guaranteed.
- **Q: Need?** → **A:** Max − Allocation.
- **Q: Complexity?** → **A:** O(n²·m).
- **Q: Requirement?** → **A:** Declared max claims.
- **Q: Real OSes?** → **A:** Rarely (too slow).
- **Q: Survives where?** → **A:** Admission control/schedulers.

## 21. Revision
Banker's algorithm is deadlock *avoidance*: it only grants a resource request if the resulting state is safe — meaning a completion sequence exists for all processes given declared max claims. Matrices (Available/Allocation/Max/Need) drive a greedy O(n²·m) safety simulation. Safe states can't deadlock; unsafe states only may. It requires accurate max claims and per-request checks, which is why general OSes avoid it — but the idea survives in schedulers and admission control with declared budgets. Interview favorite for its clean formalism.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is Banker's algorithm?" | 13 Q1 / 7 Formal Definition |
| "What is a safe state?" | 13 Q2 / 7 Formal Definition |
| "Safe vs unsafe?" | 13 Q3 / 7 Formal Definition |
| "Why max claims?" | 13 Q4 / 4 Why Wasn't Another Approach Chosen |
| "Walk the safety check" | 13 Q5 / 9 Internal Working |
| "Time complexity?" | 13 Q6 / 10 Time Complexity |
| "Unsafe = deadlock?" | 13 Q7 / 7 Formal Definition |
| "Why not in real OSes?" | 13 Q8 / 12 Disadvantages |
| "Where does it survive?" | 13 Q9 / 16 Industry Usage |
| "Exceed declared Max?" | 13 Q10 / 12 Disadvantages |
