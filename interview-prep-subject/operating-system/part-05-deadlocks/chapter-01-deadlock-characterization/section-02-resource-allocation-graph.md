# Section 02: Resource Allocation Graph (RAG)

> **TL;DR**: The resource allocation graph shows threads (processes) as circles and resources as squares, with assignment edges (resource→thread) and request edges (thread→resource). A cycle in this graph implies deadlock when every resource has one instance; with multi-instance resources, a cycle is necessary but not sufficient.

## 1. Why Does This Exist?
To *see* deadlock, you need a model. The resource allocation graph turns the four conditions into a picture: threads, resources, what's held, and what's wanted. It exists because the conditions are abstract — the graph gives a concrete, mechanical test (find a cycle) for deadlock, and it's the foundation of both detection algorithms (DFS on the graph) and of the theory (why a cycle in single-instance systems *is* deadlock). DBAs and kernel engineers reason in these terms every day.

## 2. How Does It Work?
- **Nodes**: thread nodes (circles) and resource nodes (squares; dots inside = instances).
- **Edges**: 
  - Request edge: thread → resource (thread waits for the resource).
  - Assignment edge: resource → thread (resource is allocated to thread).
- **State**: the graph at a moment in time.
- **Cycle test**: 
  - If NO cycle exists → no deadlock.
  - If a cycle exists AND all resources are single-instance → deadlock.
  - If a cycle exists with multi-instance resources → deadlock *possible*, not guaranteed.

## 3. When Is It Used?
- Textbook analysis of deadlock conditions (the standard diagram).
- Kernel/DB deadlock detection: build the wait-for graph (threads only, condensed) and search for cycles.
- Resource allocation theory: verification of safe/unsafe states (connects to Banker's).
- Systems: MySQL `SHOW ENGINE INNODB STATUS` shows waits; lock detectors build exactly this graph.

## 4. Why Wasn't Another Approach Chosen?
- **Pure wait-for graph (threads only)**: compact for detection but loses resource detail — you can't see multi-instance semantics or which resource is the tie-breaker. Rejected as the *primary* teaching model (kept as the detection projection).
- **Matrix algebra (allocation/need/available)**: precise for Banker's but less intuitive for humans. Rejected for intuition.
- **Ad-hoc textual descriptions**: no structure, no cycle test. Rejected.
The RAG chosen because it's **visual, complete (threads + resources), and gives the exact cycle criterion** — the natural bridge from conditions to algorithms.

## 5. Intuition
**A flow diagram of who's blocking whom**: draw an arrow from a thread to the resource it's waiting for, and from a resource to the thread holding it. Follow the arrows — if you end up back where you started (a loop), the waiters are all waiting on each other. A loop is the fingerprint of deadlock. With multi-instance resources (like a 3-slot printer pool), a loop might still have a spare instance somewhere — so the loop is a *warning*, not a verdict.

## 6. Real-World Analogy
**A dependency map of team handoffs**: each team (thread) draws an arrow to the machine it needs (resource), and each machine points to the team currently using it (assignment). If you can trace a circle — Team A needs the printer that Team B is using, Team B needs the scanner Team A is using — the handoff chain is stuck. With a 3-printer pool, a circle of teams might still be served by the third printer, so the circle is only a red flag.

## 7. Formal Definition
- **Thread nodes**: T1..Tn; **resource nodes**: R1..Rm with instances (dots).
- **Request edge**: directed T → R (T requests an instance of R).
- **Assignment edge**: directed R → T (an instance of R is allocated to T).
- **State change**: requesting → if available, grant (request edge converts to assignment edge); release → assignment edge removed.
- **Cycle criterion**: 
  - No cycle ⇒ no deadlock.
  - Cycle + single-instance resources ⇒ deadlock.
  - Cycle + multi-instance ⇒ deadlock only if no sequence can break the cycle (not guaranteed).
- **Wait-for graph**: projection where T1→T2 if T1 waits for a resource held by T2 (used for efficient detection).

## 8. Example
Single-instance graph:
```
T1 —(request)→ R1 ←—(assignment)— T2
T2 —(request)→ R2 ←—(assignment)— T1
```
Cycle: T1→R1→T2→R2→T1. Single instance each → deadlock. Indeed T1 holds R2 waits R1; T2 holds R1 waits R2.

Multi-instance counterexample: R1 has 2 instances; T1→R1 (request), R1→T1 (assignment), R1→T2 (assignment), T2→R2 (request), R2→T2 (assignment). A cycle T1→R1→T2→R2→T2? Careful — cycles must traverse properly; the point: with a free instance of R1, T1 can get one and proceed — no deadlock despite a cycle.

## 9. Internal Working
1. Maintain allocation: for each thread, held resources; for each resource, owner(s) and free instances.
2. On request: if a free instance exists, grant (assignment edge); else add a request edge (thread blocks).
3. On release: remove assignment edge; if requesters exist, grant to one (convert edge).
4. Detection: build wait-for graph; run DFS for cycles (O(V+E)); a found cycle with all-single-instance ⇒ deadlock.
5. Banker's uses the same state as matrices: available/allocated/max/need.

## 10. Time Complexity
- Graph construction: O(V+E) (V = threads + resources, E = edges).
- Cycle detection (DFS): O(V+E).
- Grant/release operations: O(1) amortized.
- Banker's safety check: O(n²·m) (n threads, m resources) — why it's rarely used in production.

## 11. Advantages
- Intuitive visualization of the four conditions.
- Exact deadlock test for single-instance systems.
- Foundation for wait-for-graph detection and Banker's.
- Clear multi-instance semantics (cycle ≠ deadlock necessarily).

## 12. Disadvantages
- Static snapshot — doesn't show the *sequence* that led to the state.
- Multi-instance cycles are ambiguous (need extra analysis).
- Doesn't capture resource *types* being held internally (DB row locks), requiring the wait-for projection.
- No temporal information (which wait is old, which is fresh).

## 13. Interview Questions
1. **Q: What does a resource allocation graph show?** A: Threads (circles) and resources (squares with instance dots); request edges (thread→resource) and assignment edges (resource→thread).
2. **Q: What is a request edge?** A: A directed edge from a thread to a resource — the thread is requesting/waits for an instance.
3. **Q: What is an assignment edge?** A: A directed edge from a resource to a thread — the resource instance is allocated to that thread.
4. **Q: When does a cycle imply deadlock?** A: When all resources in the cycle have a single instance — a cycle is then a definite deadlock. With multi-instance resources, a cycle is necessary but not sufficient.
5. **Q: Can there be deadlock with no cycle?** A: No — circular wait is a necessary condition; deadlock always shows a cycle in the RAG.
6. **Q (TRICKY): A cycle exists but there's a free instance of a resource in it. What's the verdict?** A: Not necessarily deadlock — a thread on the cycle could acquire the free instance and break the cycle (the cycle is only necessary with multi-instance).
7. **Q: What is the wait-for graph?** A: The RAG collapsed to threads only: T1→T2 if T1 waits for a resource held by T2; used for efficient deadlock detection.
8. **Q: How do you detect a cycle?** A: DFS (or BFS) on the wait-for graph — O(V+E); a back edge indicates a cycle.
9. **Q (PRODUCTION): MySQL shows a deadlock — what's the graph?** A: Innodb's wait-for graph: transactions (threads) waiting on each other's row locks — a cycle. The DB aborts the victim transaction to break it.
10. **Q: What's the difference between a request edge and an assignment edge?** A: Direction: thread→resource (request/wait) vs resource→thread (granted/held). The edge's orientation encodes the state.
11. **Q: How does the RAG relate to the four conditions?** A: ME = assignment edges (exclusive); hold-and-wait = thread has assignment edges AND request edges; no preemption = assignment edges only removable by holder; circular wait = the cycle.
12. **Q (TRICKY): Can a graph with no assignment edges deadlock?** A: No — without held resources there's no wait-for cycle; threads only deadlock when each holds something the next needs.

## 14. Follow-Up Questions
1. **Q: What's the difference between RAG and wait-for graph?** A: RAG includes resource nodes (complete state); wait-for graph is threads-only (efficient detection). Both express the same cycle condition for single-instance.
2. **Q: How does Banker's use this state?** A: As matrices (available, allocation, max, need) — a safety check searches for an execution order that drains all requests.
3. **Q: What is a "safe state"?** A: A state where there EXISTS a sequence of allocations so every thread can complete — the Banker's criterion; RAG cycles are unsafe-state symptoms.
4. **Q: How do databases convert to wait-for graphs?** A: Transactions = threads; row locks = resources; waiting transactions form edges — Innodb builds and checks this graph per lock wait.
5. **Q: What happens to the graph on deadlock recovery?** A: A victim thread is aborted → its assignment edges removed → resources freed → cycle broken → others proceed.

## 15. Coding Example
```c
/* Cycle detection in a wait-for graph (threads only) */
#include <stdio.h>
#include <stdbool.h>

#define N 4
int graph[N][N] = {   /* graph[i][j]: thread i waits for thread j */
    {0,1,0,0},
    {0,0,1,0},
    {0,0,0,1},
    {1,0,0,0},        /* 3 waits for 0 -> cycle 0->1->2->3->0 */
};
bool visited[N], recStack[N];

bool has_cycle_util(int v) {
    if (!visited[v]) {
        visited[v] = recStack[v] = true;
        for (int j = 0; j < N; j++)
            if (graph[v][j] &&
                ((!visited[j] && has_cycle_util(j)) || recStack[j]))
                return true;
    }
    recStack[v] = false;
    return false;
}

bool has_cycle(void) {
    for (int i = 0; i < N; i++)
        if (has_cycle_util(i)) return true;
    return false;
}

int main(void) {
    printf("cycle: %s\n", has_cycle() ? "yes (deadlock)" : "no");
    return 0;
}
```

## 16. Industry Usage
- **Databases**: MySQL/Postgres build wait-for graphs of transaction locks; detect cycles → abort victim.
- **Linux**: lockdep builds lock graphs (threads/resources) to detect orderings that could deadlock — statically.
- **Distributed systems**: lock wait chains in etcd/ZooKeeper (distributed lock graphs).
- **Debugging**: thread dump analysis reconstructs wait-for graphs from stack traces.
- **RTOS**: resource allocation analysis for deadlock-free designs.

## 17. References
- Silberschatz, *OS Concepts*, 8.2 (Resource allocation graph).
- Holt, "Some deadlock properties of computer systems" (1972) — RAG formalism.
- MySQL docs: `SHOW ENGINE INNODB STATUS` (wait-for graph).
- Linux: lockdep design notes.

## 18. Cheat Sheet
- Nodes: threads (circles), resources (squares + instance dots).
- Request edge: T→R (waiting). Assignment edge: R→T (held).
- No cycle ⇒ no deadlock.
- Cycle + single-instance ⇒ deadlock.
- Cycle + multi-instance ⇒ possible, not certain.
- Wait-for graph: threads only (T→T) for detection.
- Cycle detection: DFS O(V+E).
- Banker's: matrices (available/allocation/max/need) + safety check O(n²·m).
- DBs: transaction wait-for graphs → abort victim.
- Deadlock always has a cycle (circular wait necessary).

## 19. Quiz
1. Request edge: a) R→T b) T→R c) T→T d) R→R → **b**
2. Assignment edge: a) T→R b) R→T c) T→T d) none → **b**
3. No cycle means: a) deadlock b) no deadlock c) unsafe d) starve → **b**
4. Cycle + single instance: a) possible b) deadlock c) safe d) share → **b**
5. Multi-instance cycle: a) guaranteed b) necessary not sufficient c) impossible d) always → **b**
6. Wait-for graph omits: a) threads b) resources c) edges d) nothing → **b**
7. DFS finds: a) shortest path b) cycles c) safe states d) counts → **b**
8. RAG relates to conditions: a) no b) yes (all four) c) one d) two → **b**
9. DB detection: a) RAG cycle b) timeout only c) ignore d) lock-free → **b**
10. No assignment edges → deadlock: a) yes b) no c) possible d) always → **b**

## 20. Flashcards
- **Q: Request edge?** → **A:** T→R (waiting).
- **Q: Assignment edge?** → **A:** R→T (held).
- **Q: No cycle?** → **A:** No deadlock.
- **Q: Cycle + single instance?** → **A:** Deadlock.
- **Q: Multi-instance cycle?** → **A:** Necessary, not sufficient.
- **Q: Wait-for graph?** → **A:** Threads only, T→T.
- **Q: Detection?** → **A:** DFS cycle O(V+E).
- **Q: DBs?** → **A:** Transaction wait-for cycles, abort victim.

## 21. Revision
The RAG models state: threads wait on resources (request edges) and hold them (assignment edges). No cycle ⇒ no deadlock; a cycle with all-single-instance resources is deadlock; with multi-instance resources it's necessary but not sufficient. The wait-for graph (threads-only projection) makes cycle detection efficient via DFS (O(V+E)). Databases and kernels build exactly these graphs to find cycles and abort victims — the same machinery that powers Banker's safety analysis.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does an RAG show?" | 13 Q1 / 7 Formal Definition |
| "Request edge?" | 13 Q2 / 7 Formal Definition |
| "Assignment edge?" | 13 Q3 / 7 Formal Definition |
| "When does a cycle imply deadlock?" | 13 Q4 / 8 Example |
| "Deadlock with no cycle?" | 13 Q5 / 12 Disadvantages |
| "Cycle with free instance?" | 13 Q6 / 8 Example |
| "Wait-for graph?" | 13 Q7 / 7 Formal Definition |
| "How detect a cycle?" | 13 Q8 / 10 Time Complexity |
| "MySQL deadlock graph?" | 13 Q9 / 16 Industry Usage |
| "RAG vs four conditions?" | 13 Q11 / 7 Formal Definition |
