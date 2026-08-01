# Serializability: Conflict and View

> **TL;DR**: Serializability is the formal yardstick for concurrent correctness — a schedule is safe if it's equivalent to running transactions one-at-a-time — and conflict serializability (checked via a precedence graph) plus view serializability are the two precise definitions, with conflict being the one 2PL actually enforces.

## 1. Why Does This Exist?
A DBMS lets transactions interleave for performance. But "interleaving" can produce results no serial (one-at-a-time) run would ever produce — lost updates, incorrect balances. We need a *criterion* to declare an interleaved schedule safe. Serializability exists to answer precisely: "is this execution as good as some serial execution?" It's the formal contract behind every concurrency control protocol: 2PL, timestamp ordering, MVCC all exist to *ensure* the schedules they produce are serializable. Without serializability, "isolation" in ACID would be undefined; with it, isolation has a precise, testable meaning.

## 2. How Does It Work?
Two operations **conflict** if they belong to different transactions, operate on the same data item, and at least one is a write. A schedule is **conflict serializable** if, by only swapping the order of *non-conflicting* adjacent operations, it can be transformed into a serial schedule. Equivalently: build a **precedence (conflict) graph** — one node per transaction, an edge Tᵢ→Tⱼ whenever a conflicting pair of operations is ordered Tᵢ-before-Tⱼ — and the schedule is conflict serializable iff the graph is **acyclic**; the topological order gives a serial order. **View serializability** is a weaker equivalence: two schedules are view-equivalent if every transaction reads the same value (from the same writer) for each data item and final writes produce the same values. Conflict serializability ⊆ view serializability; view serializable is harder to test (NP-complete), so conflict is used in practice.

## 3. When Is It Used?
- **Inside every real DBMS**: the lock protocols (2PL family, Chapter 02) generate only conflict-serializable schedules, which is the practical guarantee of isolation.
- **To test protocols in research/textbooks**: proving a protocol produces acyclic conflict graphs is the standard correctness proof.
- **In interviews**: "is this schedule serializable?", "draw the precedence graph", "what's the difference between conflict and view serializability?", "is a schedule that's view serializable always conflict serializable?"
- **MVCC validation**: snapshot isolation is *not* conflict serializable in general — that's why it allows write skew — and SSI (Serializable Snapshot Isolation) was built to fix it (Chapter 03).

## 4. Why Wasn't Another Approach Chosen?
- *Requiring literally serial schedules:* trivially safe, kills concurrency. We want interleaving.
- *View serializability as the target:* it's the "correct" semantic equivalence, but testing it is NP-complete, and protocols can't easily enforce it. Conflict serializability is polynomial and structurally enforced by locks — a practical trade of some safe schedules for implementability. (Blind writes are the classic schedule that's view-serializable but not conflict-serializable.)
- *Checking equivalence by "same final database state":* final-state equivalence is too weak — it ignores *what each transaction read*, allowing a transaction to read wrong intermediate values as long as the final state matches. Conflict/view equivalence are stricter precisely because they track reads.
- *Linearity/linearizability (distributed sense):* stricter than serializability (adds real-time ordering) and unnecessary within a single DB; Spanner-style systems *do* pursue stricter orderings via commit-wait.

## 5. Intuition
Imagine a **conveyor belt with labeled boxes** (operations). You may swap the positions of any two adjacent boxes only if they don't "touch" — i.e., they don't conflict (same data item, one a write). If, by a sequence of such swaps, you can line up all of T₁'s boxes before all of T₂'s (and so on) — the schedule is conflict serializable. The precedence graph is a courtroom sketch: draw an arrow from T₁ to T₂ whenever T₁ must have happened first (they touched the same item). If the arrows form a loop (T₁ before T₂ before T₃ before T₁), there's a contradiction — no serial order exists — and the schedule is *not* serializable.

## 6. Real-World Analogy
A **two-person editing a shared document**. Conflicting edits: two people editing the same paragraph (one must come after the other; order matters). Non-conflicting: edits to different paragraphs — you can reorder them freely. The doc's history is "serializable" if you can compress the chaotic timeline into "person A did all their edits, then person B did all theirs" without changing who-sees-what. If the timeline requires "A before B, B before C, and C before A" (a cycle), it's impossible — the edits are entangled beyond repair, i.e., non-serializable.

## 7. Formal Definition
- **Conflicting operations**: operations from *different* transactions, on the *same* data item, at least one of which is a `write` — the ordering of these matters for correctness.
- **Conflict equivalence**: schedules S and S' are conflict-equivalent if they involve the same operations, and every pair of conflicting operations is ordered the same way in both.
- **Conflict serializability**: S is conflict serializable if S is conflict-equivalent to a serial schedule. Test: precedence graph is acyclic (equivalently, no cycle in the "must come before" relation). Decidable in polynomial time.
- **View equivalence**: S and S' are view-equivalent if (1) for each data item, if Tᵢ reads its initial value in S it does so in S'; (2) if Tᵢ reads the value written by Tⱼ in S it reads that same Tⱼ-written value in S'; (3) the same transactions do the final writes in both.
- **View serializability**: S is view serializable if it is view-equivalent to some serial schedule. **Note**: view serializability does not imply conflict serializability (the blind-write schedule is the canonical counterexample).
- **Recoverable schedules / cascadeless schedules**: a schedule is recoverable if a transaction commits only after all transactions whose data it read have committed (prevents dirty reads of aborted data); cascadeless if it only reads committed data (prevents cascading rollbacks). Strict schedules additionally ensure no reads or writes until the prior writer commits. These are *weaker* correctness properties layered under serializability.

## 8. Example
Transactions:
- T₁: `read(A); write(A); read(B); write(B)`
- T₂: `read(A); write(A); read(B); write(B)`

Schedule S: `r₁(A) w₁(A) r₂(A) w₂(A) r₁(B) w₁(B) r₂(B) w₂(B)`.
Conflicting pairs and their order: (r₁(A),w₂(A)) → T₁ before T₂; (w₁(A),w₂(A)) → T₁ before T₂; (w₁(A),r₂(A)) → T₁ before T₂; (w₁(B),r₂(B)) → T₁ before T₂; (w₁(B),w₂(B)) → T₁ before T₂. Precedence graph: single edge T₁→T₂, acyclic → **conflict serializable**, equivalent to serial schedule `T₁ T₂`.

Non-serializable schedule S': `r₁(A) w₁(A) r₂(A) w₂(A) r₂(B) w₂(B) r₁(B) w₁(B)` (T₂ finishes B before T₁ does). Conflicts create edges T₁→T₂ (on A) and T₂→T₁ (on B) → cycle → **not conflict serializable**. This is the classic lost-update/shared-write hazard.

Blind-write counterexample (view-serializable but NOT conflict-serializable): T₁: `write(A)`, T₂: `write(A)`, T₃: `read(A)`. Schedule S: `w₁(A) w₂(A) w₃(A) r₃(A)` — wait, use the classic: T₁ writes A, T₂ reads A and writes A, T₃ writes A. Schedule: `w₁(A) w₂(A) w₃(A)` (all writes, T₂'s read hidden). With T₁: w(A); T₂: r(A) w(A); T₃: w(A), the schedule `w₁(A) w₃(A) r₂(A) w₂(A)` is view-equivalent to the serial schedule `T₁ T₃ T₂` (final write = T₂ in both; r₂ reads the T₃ value in both) but is NOT conflict serializable (w₁→w₃→r₂ conflicts form a cycle with w₂). This is why conflict-serializability testing is "complete enough" but not "everything safe."

## 9. Internal Working
1. The scheduler receives operations from transactions.
2. It determines conflicts: same data item, different transactions, at least one write.
3. For **testing** (textbook/static): build precedence graph; run topological sort / cycle detection (Kahn's algorithm or DFS) — if a cycle exists, non-serializable.
4. For **enforcement** (real DBMS): protocols don't build the graph per-execution; instead they constrain ordering (2PL: a transaction can't acquire conflicting locks after it releases one; timestamp: monotone timestamps order conflicts) so that any schedule *produced* is provably conflict-serializable without runtime graph checks.
5. At runtime, engines implement isolation *weaker* than serializable by default (read committed) — the schedule-test machinery is the *spec*; the lock protocol is the *enforcement*.

## 10. Time Complexity
- Conflict detection: O(1) per operation pair with a hash on (transaction, data item, type).
- Precedence graph + cycle check: O(N + E), N transactions, E conflicting edges — polynomial.
- View serializability testing: NP-complete in general (why it's never the enforcement target).
- Protocol enforcement (2PL, timestamp): amortized O(1) per operation plus lock manager overhead.

## 11. Advantages
- Gives a *precise, machine-checkable* definition of "safe concurrency" — the theoretical backbone of all protocols.
- Conflict serializability is polynomial and directly enforceable by locking, making it the practical gold standard.
- View serializability captures schedules that conflict-testing rejects but are semantically fine (useful for MVCC/validation designs).
- Enables formal proofs ("2PL ⇒ conflict serializable ⇒ acyclic graph") you can cite in interviews.

## 12. Disadvantages
- Conflict serializability is *stronger* than semantic correctness — it rejects some schedules that produce correct results (e.g., blind-write view-serializable schedules).
- View serializability is NP-complete to test, so it's only used theoretically.
- Real engines don't run at serializable by default (performance), so the definition describes the ideal, not the default.
- Snapshot isolation (MVCC default) violates conflict serializability in the write-skew case — you must know the *gap* between the theory and MySQL/Postgres defaults.

## 13. Interview Questions
1. **Q: What is serializability?** A: A schedule is serializable if it's equivalent to a serial schedule — i.e., its result is the same as executing the transactions one at a time. It's the formal definition of isolation.
2. **Q: Define conflicting operations.** A: Two operations conflict if they come from different transactions, act on the same data item, and at least one is a write. Only conflicting operations' order affects correctness.
3. **Q: How do you test conflict serializability?** A: Build the precedence graph (nodes = transactions, edges = conflict order) and check for cycles with topological sort/DFS. Acyclic ⇒ conflict serializable; the topological order is a serialization order.
4. **Q: Give an example of a non-serializable schedule.** A: T₁: r(A) w(A) r(B) w(B); T₂: r(A) w(A) r(B) w(B) with interleaving where T₁ and T₂ both write A and B in opposite orders (T₁ writes A, T₂ writes B first) — the conflict graph has edges T₁→T₂ and T₂→T₁ (a cycle), so no serial order works.
5. **Q: Difference between conflict and view serializability?** A: Conflict: ordering of *conflicting pairs* must match a serial schedule. View: transactions must read the same values (same writer for each read, same initial reads, same final writes). Conflict ⇒ view, but view ⇏ conflict (blind-write example). Conflict is what 2PL enforces; view is the semantic ideal.
6. **Q: TRICKY: Why is view serializability not used for enforcement?** A: Because determining whether a schedule is view serializable is NP-complete (reduces to a decision problem on the dependency structure), and no simple lock protocol enforces it. Conflict serializability is polynomial and structurally enforced — a deliberate engineering trade.
7. **Q: What is the precedence graph?** A: Directed graph: each node is a transaction; an edge Tᵢ→Tⱼ means a conflicting operation pair where Tᵢ's operation precedes Tⱼ's on the same item. A cycle ⇒ non-serializable.
8. **Q: What is a recoverable schedule?** A: A transaction commits only after every transaction whose data it read has committed. Prevents the situation where T₂ commits having read T₁'s uncommitted data, then T₁ aborts — which would leave a "committed read of aborted data" (dirty read persisted). Recoverability is a *minimum* requirement below serializability.
9. **Q: What is a cascading rollback?** A: If T₁ writes, T₂ reads T₁'s uncommitted value, T₃ reads T₂'s value, and T₁ aborts — T₂ and T₃ must also roll back, cascading. **Cascadeless schedules** (transactions only read *committed* data) prevent this. This is why engines read committed data even at READ COMMITTED.
10. **Q: Is snapshot isolation conflict serializable?** A: No, in general — two transactions can both modify disjoint data and create a **write skew** that no serial execution produces. Postgres's `REPEATABLE READ` is snapshot isolation; only `SERIALIZABLE` (SSI) is fully serializable. This is a favorite "tricky" question.
11. **Q: PRACTICAL: If 2PL guarantees serializable, why is MySQL's default only REPEATABLE READ?** A: Because 2PL with full serializability is expensive (lock contention, no phantom protection without extra machinery), and most apps tolerate weaker isolation. The DB trades a *known, bounded* anomaly for throughput. Only when apps set SERIALIZABLE does the engine pay for full isolation.
12. **Q: What's the difference between serializability and final-state equivalence?** A: Final-state equivalence only compares the ending database state. It's too weak: two schedules could end with the same state while a transaction read *wrong* intermediate values (that's the difference between "same result" and "same reads"). Conflict/view equivalence track what each transaction *saw*.
13. **Q: TRICKY: Give a schedule that is view serializable but not conflict serializable.** A: The classic blind-write: T₁: write(A); T₂: read(A), write(A); T₃: write(A), with schedule w₁(A) w₃(A) r₂(A) w₂(A). It's view-equivalent to serial `T₁,T₃,T₂` (final writer is T₂ in both; r₂ sees T₃'s value in both) but the conflict graph has a cycle.
14. **Q: What is a strict schedule?** A: A schedule is strict if a transaction neither reads nor writes an item until the transaction that last wrote it commits/aborts. Strict schedules are cascadeless and recoverable; strict 2PL (releasing locks only at commit) produces them — that's what real engines use.
15. **Q: PRODUCTION: How does Postgres's SERIALIZABLE differ from its REPEATABLE READ?** A: REPEATABLE READ = snapshot isolation (no dirty/non-repeatable/phantom *reads* within a snapshot, but write-skew possible). SERIALIZABLE uses SSI: it tracks read/write dependencies on snapshots and aborts one transaction when it detects a serialization anomaly — giving true serializability.
16. **Q: Why do we need both "recoverable" and "serializable"?** A: Serializability handles *interleaving correctness*; recoverability handles *crash/abort correctness*. A serializable schedule that isn't recoverable can still commit a read of data from a transaction that later aborts — both properties are needed for full ACID isolation.

## 14. Follow-Up Questions
1. **Q: Can a schedule be conflict serializable but not view serializable?** A: No — conflict serializability is a subset of view serializability. Every conflict-serializable schedule is view serializable (with the same serialization order).
2. **Q: What does "blind write" mean and why does it break conflict tests?** A: A transaction writes an item without reading it. Because the write order doesn't depend on prior reads, view equivalence can hold while conflict edges cycle — the gap between the two definitions.
3. **Q: How does MVCC relate to serializability?** A: MVCC provides snapshot isolation by reading old versions; this is equivalent to conflict serializable only in restricted cases. SSI extends MVCC's bookkeeping to detect and abort write-skew cycles, achieving serializable without blocking.

## 15. Coding Example
```python
# Conflict-serializability check: precedence graph + cycle detection
from collections import defaultdict, deque

def is_conflict_serializable(schedule):
    """schedule: list of ops as (txid, data, 'r'|'w'). Returns (bool, order)."""
    ops = schedule
    n = max(t for t, _, _ in ops) + 1
    graph = defaultdict(set)
    # record last operation per data item
    for i, (t1, d1, op1) in enumerate(ops):
        for j, (t2, d2, op2) in enumerate(ops[i+1:], start=i+1):
            if t1 != t2 and d1 == d2 and (op1 == 'w' or op2 == 'w'):
                graph[t1].add(t2)          # t1's op precedes t2's on same item
    # Kahn's topological sort → cycle?
    indeg = {v: 0 for v in range(n)}
    for u in graph:
        for v in graph[u]:
            indeg[v] += 1
    q = deque(v for v in range(n) if indeg[v] == 0)
    order = []
    while q:
        u = q.popleft(); order.append(u)
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return len(order) == n, order           # len(order)==n ⇒ acyclic ⇒ serializable

s = [(0,'A','r'), (0,'A','w'), (1,'A','r'), (1,'A','w'),
     (0,'B','r'), (0,'B','w'), (1,'B','r'), (1,'B','w')]
print(is_conflict_serializable(s))          # (True, [0, 1])
```

## 16. Industry Usage
- **PostgreSQL**: default READ COMMITTED (recoverable, cascadeless, per-statement snapshots), REPEATABLE READ (SSI-free snapshot isolation), SERIALIZABLE (SSI — full serializability with actual conflict-graph reasoning done at runtime).
- **MySQL InnoDB**: REPEATABLE READ default (via next-key locks, stronger than standard), SERIALIZABLE uses `LOCK IN SHARE MODE`-style read locking — it enforces conflict-serializable schedules through locking.
- **SQL Server / Oracle**: Oracle's SERIALIZABLE is actually snapshot (write-skew risk); SQL Server's SERIALIZABLE is true 2PL-based serializable with range locks. Knowing *which engine maps which level to which guarantee* is a differentiator.
- **Distributed**: Google Spanner publishes serializability + linearizability; CockroachDB targets serializable via MVCC + per-epoch commits. The theoretical framework here is what they verify against.

## 17. References
- Silberschatz, *Database System Concepts*, 7th ed., Ch. 15.3–15.4 (serializability, conflict & view equivalence).
- Elmasri & Navathe, *Fundamentals of Database Systems*, Ch. 20.
- P. A. Bernstein, V. Hadzilacos, N. Goodman, *Concurrency Control and Recovery in Database Systems* (1987).
- Cahill, Röhm, Fekete, "Serializable Isolation for Snapshot Databases" (SSI, SIGMOD 2009) — basis of Postgres SERIALIZABLE.
- Berenson et al., "A Critique of ANSI SQL Isolation Levels" (SIGMOD 1995) — the anomalies paper.

## 18. Cheat Sheet
- Conflict = different txns, same item, one is a write.
- Conflict serializable ⇔ precedence graph acyclic ⇔ ∃ topological serial order.
- Conflict ⇒ view; view ⇏ conflict (blind writes).
- 2PL enforces conflict serializability; MVCC+SSI gives serializable at REPEATABLE READ cost.
- Recoverable: commit only after reading-committed-others; Cascadeless: read only committed data; Strict: nothing until prior writer commits.
- Test is O(N+E); view-serializability test is NP-complete.
- Cycle in precedence graph = contradiction = non-serializable.

## 19. Quiz
1. Two operations conflict if: a) same transaction b) different txns, same item, one a write c) any two writes d) any two reads → **b**
2. A cycle in the precedence graph means the schedule is: a) serial b) serializable c) not conflict serializable d) recoverable → **c**
3. Which is a subset of the other? a) view ⊆ conflict b) conflict ⊆ view c) equal d) disjoint → **b**
4. A blind-write schedule is the counterexample that proves: a) conflict ⇒ view is false b) view ⇏ conflict c) both are equal d) nothing → **b**
5. What guarantees a recoverable schedule? a) only reads committed data b) commit only after readers of your data commit c) both a and b d) neither → **b** (cascadeless = a)
6. Postgres SERIALIZABLE uses: a) 2PL b) SSI c) no isolation d) timestamp → **b**
7. Testing conflict serializability is: a) exponential b) polynomial c) undecidable d) O(1) → **b**
8. A strict schedule requires: a) reads of committed data only b) no read/write until prior writer commits c) all-or-nothing d) none → **b**

## 20. Flashcards
- **Q: When do two operations conflict?** → **A:** Different transactions, same data item, at least one a write.
- **Q: How do you test conflict serializability?** → **A:** Build precedence graph; acyclic = conflict serializable (topological order = serial order).
- **Q: Conflict vs view serializability.** → **A:** Conflict = conflicting-pair ordering matches serial; view = same reads/final writes. Conflict ⊆ view.
- **Q: What is a recoverable schedule?** → **A:** A transaction commits only after all transactions it read from commit.
- **Q: What prevents cascading rollbacks?** → **A:** Cascadeless schedules (only read committed data).
- **Q: Why is view serializability impractical?** → **A:** Testing it is NP-complete; no lock protocol enforces it.
- **Q: How does SSI achieve serializability in Postgres?** → **A:** Detects serialization anomalies on MVCC snapshots and aborts one transaction.

## 21. Revision
Serializability: a schedule is safe iff equivalent to a serial schedule. Conflicting ops = different transactions, same item, one a write. Conflict serializable ⇔ acyclic precedence graph (test O(N+E)). Conflict ⇒ view, not vice versa (blind writes). Weaker but necessary properties: recoverable (commit after the txns you read), cascadeless (only read committed), strict (wait for prior writer). Real engines: Postgres READ COMMITTED = cascadeless, per-statement snapshot; SERIALIZABLE = SSI. MySQL default REPEATABLE READ uses next-key locks. Interview killer answers: draw the graph, name the blind-write counterexample, explain snapshot-isolation write skew.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Is this schedule serializable?" | 2, 8, 15 |
| "What is a precedence/conflict graph?" | 2, 8, 13 |
| "Conflict vs view serializability." | 4, 7, 13 |
| "Give a view-but-not-conflict serializable schedule." | 8, 13 |
| "What is a recoverable / cascadeless / strict schedule?" | 7, 13 |
| "Why can't we enforce view serializability?" | 4, 13 |
| "Is snapshot isolation serializable? (write skew)" | 13, 16 |
| "How does Postgres SERIALIZABLE work?" | 13, 16 |
