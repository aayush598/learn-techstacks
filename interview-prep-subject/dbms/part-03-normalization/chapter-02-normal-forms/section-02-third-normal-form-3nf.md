# Third Normal Form (3NF)

> **TL;DR**: A relation is in 3NF iff it's in 2NF and no *non-prime* attribute is *transitively* dependent on any candidate key — equivalently, every non-trivial FD X→Y has X a superkey OR Y prime — removing "A determines B determines C" chains that repeat facts like department names.

## 1. Why Does This Exist?
2NF removed partial dependencies, but a subtler redundancy survives: **transitive dependency** — emp_id → dept_id, dept_id → dept_name. Here `emp_id → dept_name` holds *through* dept_id, so dept_name gets repeated for every employee in the department. Renaming the department means updating every employee row (update anomaly); adding an empty department is impossible without an employee (insert anomaly). 3NF exists to cut transitive chains: a fact (dept_name) should be owned by its true determiner (dept_id), stored once in its own relation. It's the "every non-key fact depends on the key, the whole key, and nothing but the key" discipline — the famous rule of thumb for the normal forms up to 3NF.

## 2. How Does It Work?
**Definition (exact)**: R is in 3NF iff for every non-trivial FD X→Y ∈ F⁺, at least one of: (a) X is a superkey (X⁺ = R), or (b) Y is **prime** (every attribute of Y belongs to some candidate key). This is the *relaxed* condition that makes 3NF dependency-preservation possible.
**Test procedure**: 1) find all candidate keys (closure); 2) list candidate-key members → prime attributes; 3) for each non-trivial FD X→Y: if X⁺ ≠ R (X not superkey) AND Y has a non-prime attribute → **violation** (transitive dependency).
**Intuition of the violation**: X→Y with X not a superkey and Y non-prime means Y is "owned by" X, but the relation's key is elsewhere — so Y repeats whenever X repeats.
**Fix**: decompose the transitive chain — pull the chain (X, Y) into its own relation keyed by X, and remove Y from the original.

## 3. When Is It Used?
- **Schema design**: the target normal form for the vast majority of OLTP schemas (3NF is "good enough" — dependency-preserving, no transitive redundancy).
- **The 3NF test** is the single most-asked normalization interview question ("is R in 3NF?").
- **Repair**: "why does dept_name repeat?" → transitive chain → decompose.
- **Synthesis**: the 3NF *synthesis algorithm* (canonical cover → relations) is used when a BCNF decomposition can't preserve dependencies.
- **Production**: almost every well-designed transactional schema is 3NF; 3NF violations in legacy schemas are the classic migration targets.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: allow transitive dependencies (stay in 2NF).** Rejected: dept_name duplication causes the same anomaly family as partial dependency — 3NF exists specifically because 2NF wasn't enough.
- **Alternative: enforce 3NF's stricter cousin BCNF everywhere.** Rejected (often): BCNF *can* lose dependencies in corner cases (the classic R(A,B,C), {AB→C, C→A}); 3NF's "or Y is prime" relaxation guarantees a dependency-preserving decomposition always exists. Production usually prefers 3NF over a dependency-losing BCNF.
- **Alternative: denormalize (skip 3NF).** Rejected for OLTP — write correctness wins; denormalization is chosen only when reads dominate (Section 06).
- **Why "prime or superkey"?** It's the *minimum relaxation* that still kills transitive redundancy for non-prime attributes while allowing dependency preservation. FDs into key components are "safe" redundancy — they don't repeat non-key facts.

## 5. Intuition
3NF is the "**no middleman**" rule. If employee determines dept_id and dept_id determines dept_name, then employee is secretly determining dept_name *through a middleman*. The database is storing the middleman's facts (dept) inside the employee's table — so a department's name appears as many times as it has employees. 3NF says: *facts should live with their true owner*. dept_name belongs to dept_id; so make a DEPT table keyed by dept_id, and let EMPLOYEE just reference it. The "nothing but the key" phrase captures it: each non-key fact depends on the key (employee → dept_id ✓), the whole key (2NF ✓), and **nothing but the key** — not on some other non-key fact (3NF).

## 6. Real-World Analogy
A **warehouse catalog**: each item card (keyed by SKU) lists the item and its *category*. But the card also writes the *category manager's name*. Manager depends on category, not on SKU — a transitive chain: SKU → category → manager. If 200 SKUs share "Electronics", the electronics manager's name appears 200 times; promoting them means editing 200 cards. 3NF fixes it: a separate category card (category → manager), and the item cards just name the category. The manager is stored once, on the card that truly owns it. That's the entire idea: don't let facts ride along on a key that isn't their owner.

## 7. Formal Definition
(Elmasri & Navathe Ch. 14; Silberschatz Ch. 8; Codd 1971.)
- **Prime attribute**: member of some candidate key. **Non-prime**: member of no candidate key.
- **Transitive dependency**: X→Z holds transitively if there exist FDs X→Y and Y→Z with Y not a (super)key and Z ∉ Y.
- **3NF**: R is in 3NF iff for every non-trivial functional dependency X→Y ∈ F⁺, either (a) X is a superkey, or (b) every attribute in Y is prime. Equivalently: R is in 2NF and no non-prime attribute is transitively dependent on a candidate key.
- **Key property**: the 3NF synthesis algorithm always produces a lossless, dependency-preserving decomposition into 3NF (unlike BCNF).

## 8. Example
`EMPLOYEE(emp_id, name, dept_id, dept_name)` with key {emp_id}; FDs: `emp_id → name, dept_id, dept_name`; `dept_id → dept_name`.
```
(1, 'Alice', 10, 'Engineering')
(2, 'Bob',   10, 'Engineering')    -- dept_name repeats: transitive!
(3, 'Cara',  20, 'Sales')
```
- **2NF?** Yes (single-attribute key → no partial deps).
- **3NF?** FD `dept_id → dept_name`: dept_id⁺ = {dept_id, dept_name} ≠ R → dept_id not a superkey; dept_name non-prime → **3NF violation** (transitive: emp_id → dept_id → dept_name).
- **Redundancy**: 'Engineering' stored twice; renaming → 2 updates.
- **Fix** — decompose:
  - `DEPT(dept_id, dept_name)` — key {dept_id}.
  - `EMPLOYEE(emp_id, name, dept_id)` — key {emp_id}; FK dept_id → DEPT.
- **Verify**: lossless (join on dept_id recovers rows); dependency-preserving (dept_id → dept_name still in DEPT); 3NF ✓.

## 9. Internal Working
1. **Find all candidate keys** (closure algorithm, Section 02).
2. **Mark prime attributes** = union of all candidate keys.
3. **For each non-trivial FD X→Y**: compute X⁺; if X⁺ ≠ R and some Y attribute is non-prime → violation.
4. **Transitive-chain decomposition**: for each violating chain X→Y (Y non-prime, X not superkey): create relation (X, Y) with X as key; remove Y from the original relation; keep a FK from the original's X to the new table.
5. **Verify the result**: (a) each decomposed relation is 3NF (re-test); (b) join test for losslessness; (c) projection test for dependency preservation.
6. **Synthesis alternative**: compute canonical cover F_c; group FDs by LHS → one relation per LHS; add a relation with a candidate key if no existing relation contains one. Guarantees 3NF + lossless + dependency-preserving.

## 10. Time Complexity
- **3NF test**: O(#FDs × closure cost) — each closure O(|F|·|R|²); trivial for interview sizes.
- **Canonical cover**: O(|F|²·|R|) worst; fine in practice.
- **Synthesis decomposition**: O(|F_c| + |R|) after the cover.
- **Production cost**: none at runtime — 3NF is a design-time property.

## 11. Advantages
- **No transitive redundancy**: non-key facts stored once at their true owner.
- **Dependency-preserving decomposition always exists** — 3NF's defining advantage over BCNF.
- **Lossless join guaranteed** by the synthesis algorithm.
- **The OLTP sweet spot**: write-correct, read-decent, easy to reason about.
- **Anomaly-free for non-prime attributes**: update/insert/delete anomalies from transitive chains eliminated.

## 12. Disadvantages
- **3NF ≠ BCNF**: some 3NF relations still have redundancy in *prime* attributes (overlapping candidate keys) — BCNF fixes that.
- **Slight complexity of definition**: the "or Y is prime" clause confuses people — many mistakenly demand BCNF's superkey-only rule.
- **Join cost**: decomposition adds joins vs a denormalized design.
- **Not automatically dependency-preserving when decomposed by hand** — the naive "split on the transitive FD" needs verification.

## 13. Interview Questions
1. **Q: What is 3NF?** A: 2NF + no transitive dependency of a non-prime attribute on a candidate key. Formally: every non-trivial FD X→Y has X a superkey OR every attribute of Y prime.
2. **Q: What is a transitive dependency?** A: X→Y, Y→Z where Y is not a superkey and Z ∉ Y — X determines Z through a middleman. E.g., emp_id → dept_id, dept_id → dept_name ⇒ emp_id → dept_name transitively.
3. **Q: Is EMPLOYEE(emp_id, name, dept_id, dept_name) in 3NF?** A: No — `dept_id → dept_name` is non-trivial, dept_id isn't a superkey, dept_name is non-prime → violation. Fix: DEPT(dept_id, dept_name) + EMPLOYEE(emp_id, name, dept_id).
4. **Q: Why does 3NF allow "Y is prime" FDs?** A: To guarantee dependency-preserving decompositions exist. Allowing FDs *into* key components sacrifices a little redundancy (in keys only, never in non-prime facts) in exchange for always being able to decompose without losing rules. That's the 3NF-vs-BCNF trade.
5. **Q (tricky): 3NF but not BCNF — give the classic example.** A: R(A, B, C) with F = {AB→C, C→A}. Candidate keys: {AB}, {BC}. C is prime (in {BC}). FD `C→A`: C⁺={C,A}≠R (not superkey), but A is prime → passes 3NF. Yet `C→A` is a non-trivial FD with a non-superkey LHS → **not BCNF**. This is *the* canonical "3NF but not BCNF" relation.
6. **Q (scenario): Design a schema where "each dept has a manager, each employee works in one dept."** A: EMPLOYEE(emp_id, name, dept_id), DEPT(dept_id, dept_name, manager). FDs: emp_id→dept_id; dept_id→dept_name, manager. No transitive chain into non-prime attrs → 3NF ✓. (Note `dept_id → manager` is keyed in DEPT.)
7. **Q: What's the difference between 2NF and 3NF?** A: 2NF bans *partial* dependencies (X ⊂ key); 3NF bans *transitive* dependencies (X→Y→Z). 2NF fixes composite-key redundancy; 3NF fixes middleman redundancy. 3NF subsumes 2NF.
8. **Q: How do you test 3NF algorithmically?** A: Find candidate keys → mark primes → for each non-trivial FD X→Y: violation iff X⁺ ≠ R AND Y has a non-prime attribute. If no violations → 3NF.
9. **Q (production): Renaming a department requires updating 5000 rows. What's wrong?** A: Classic transitive redundancy — dept_name lives in EMPLOYEE instead of a DEPT table. Fix: decompose DEPT(dept_id, dept_name); update once; join for the name.
10. **Q: What is the 3NF synthesis algorithm?** A: Compute a canonical cover F_c; create one relation per F_c FD (grouped by LHS); if no relation contains a candidate key, add one. Guarantees: lossless join + dependency preservation + 3NF. Used when BCNF would lose dependencies.
11. **Q (tricky): Is a relation with a single candidate key automatically 3NF if no transitive FD exists?** A: Yes — with one key, "Y prime" = "Y in that key"; a transitive dependency into non-prime attrs is exactly what the test catches. Single-key + no transitive chain ⇒ 3NF.
12. **Q: What anomalies does 3NF fix?** A: Update (rename dept in every employee row), insert (can't add an empty department), delete (removing last employee loses the dept's name). All from the transitive chain.
13. **Q (scenario): Your 3NF decomposition lost an FD. What went wrong?** A: You hand-split without the projection test — an FD whose attributes straddle the split is lost. Use the synthesis algorithm (or verify each original FD holds in the projected sets via closure). This is why "3NF = dependency-preserving" is a property, not a freebie.
14. **Q: How is 3NF related to "the key, the whole key, and nothing but the key"?** A: That phrase is exactly: depends on the key (1NF-ish/BCNF candidate-key rule), the whole key (2NF: no partial), and nothing but the key (3NF: no transitive) — with the prime-attribute caveat. It's the mnemonic for the ladder up to 3NF.
15. **Q: What is a canonical cover and why does synthesis need it?** A: F_c is a minimal equivalent FD set (no redundant FDs/attributes). Synthesis needs it so you don't create redundant relations from implied FDs. Computation: split, trim, delete-redundant, iterate.
16. **Q (hard): Can a 3NF design still have redundancy?** A: Yes — in *prime* attributes when candidate keys overlap (the R(A,B,C), {AB→C,C→A} case stores C and A facts that could repeat). 3NF trades this residual key redundancy for dependency preservation; BCNF removes it but may lose FDs.
17. **Q (production): When would you settle for 3NF over BCNF in production?** A: When the BCNF decomposition loses a dependency you need (the overlapping-key case) or produces an unintuitive join-heavy split. 3NF is the safe, standard choice; BCNF when you can get it without losing FDs.
18. **Q: Given R(A,B,C,D), F={A→B, B→C, C→D}, is it 3NF?** A: Candidate key {A} (A⁺=all). FDs: A→B (superkey LHS ✓), B→C: B⁺={B,C,D}≠R, C non-prime → **violation** (transitive A→B→C). Not 3NF. Fix: decompose C→D and B→C chains.
19. **Q (tricky): R(A,B,C), F={AB→C, C→B}. Candidate keys? 3NF? BCNF?** A: {AB}⁺=all; {AC}⁺=all (C→B) → keys {AB},{AC}. C is prime. FD C→B: C⁺={C,B}≠R (not superkey), but B is prime → 3NF ✓. Non-superkey LHS → not BCNF. Another 3NF-not-BCNF instance.
20. **Q: How do you decompose R(A,B,C,D), F={A→B, B→C} to 3NF?** A: Keys: {A,D}. Violation: B→C (B⁺={B,C}≠R, C non-prime). Split: R1(B,C) key {B}; R2(A,B,D) — check A→B: A⁺ in R2 = {A,B,D} (no C in R2) ✓ superkey there. Both 3NF; lossless; dependency-preserving. Result: R1(B,C), R2(A,B,D).

## 14. Follow-Up Questions
1. **Q: What exactly is the "prime-attribute relaxation" doing?** A: It exempts FDs whose RHS is part of a key — those never duplicate *non-key* facts (the expensive kind). This is the minimal relaxation that keeps dependency preservation achievable.
2. **Q: When does 3NF coincide with BCNF?** A: Whenever every FD's LHS is a superkey — i.e., no non-trivial FD with a non-superkey LHS exists (e.g., single candidate key without overlapping-key cases). For most real schemas 3NF = BCNF; the difference is exotic.
3. **Q: What's the difference between the decomposition algorithm and the synthesis algorithm?** A: Decomposition starts from the original relation and splits violating FDs (BCNF-style, may lose deps); synthesis builds new relations from a canonical cover (guaranteed 3NF + preservation). Different methods, both valid for 3NF.
4. **Q: Does 3NF handle multi-valued dependencies?** A: No — MVDs (independent variation, e.g., skills × languages) need 4NF. 3NF is purely FD-based.
5. **Q: Why is 3NF the "industry default" more than BCNF?** A: Dependency preservation + simplicity. Real schemas rarely hit the overlapping-key pathologies where BCNF differs; when they do, engineers usually keep 3NF to avoid losing rules.

## 15. Coding Example
```sql
-- 3NF violation: transitive chain (before)
CREATE TABLE emp_bad (
  emp_id    INT PRIMARY KEY,
  name      TEXT,
  dept_id   INT,
  dept_name TEXT   -- depends on dept_id, not emp_id (transitive)
);

-- 3NF fix: decompose (after)
CREATE TABLE dept (dept_id INT PRIMARY KEY, dept_name TEXT);
CREATE TABLE emp (
  emp_id  INT PRIMARY KEY,
  name    TEXT,
  dept_id INT REFERENCES dept(dept_id)
);
-- 'Engineering' now stored exactly once; rename = one UPDATE on dept.

-- Query that motivated the split (one join, not a repeated column)
SELECT e.name, d.dept_name
FROM   emp e JOIN dept d ON d.dept_id = e.dept_id;
```
```python
# 3NF violation test (educational)
def is_3nf(all_attrs, fds, keys):
    primes = {a for k in keys for a in k}
    for x, y in fds:
        non_triv = not (y <= x)
        lhs_not_super = closure(x, fds) != set(all_attrs)
        rhs_has_nonprime = any(a not in primes for a in y)
        if non_triv and lhs_not_super and rhs_has_nonprime:
            return False, (x, y)      # 3NF violation found
    return True, None
```

## 16. Industry Usage
- **The default target form** for nearly all OLTP schemas (Postgres/MySQL/Oracle/SQL Server): order→customer→address chains are decomposed exactly like emp→dept.
- **ORM migration** (Prisma/Hibernate) models end up 3NF: "belongs_to" and "has_one" associations ARE the 3NF decompositions.
- **Data modeling standards** (Kimball star schema) keep *dimensions* in 3NF-like form (dim_customer, dim_product) before denormalizing into fact tables — the warehouse reuses 3NF thinking.
- **Schema review checklists** at Amazon/Google include "is this 3NF? any transitive chains?" as a standard gate.
- **Legacy repair**: thousands of production databases are migrated from 2NF/denormalized to 3NF to kill update anomalies — the exact "decompose the transitive chain" move.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14 (3NF; synthesis).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 8.4 (Third Normal Form).
- Codd, E. F., "Further Normalization of the Data Base Relational Model", 1971.
- Kent, W., "A Simple Guide to Five Normal Forms", CACM 1983.
- Bernstein, P., "Synthesizing Third Normal Form Relations from Functional Dependencies", TODS 1976.

## 18. Cheat Sheet
- 3NF: 2NF + no transitive dependency (non-prime on key through a middleman).
- Formal: every non-trivial X→Y has X superkey OR all of Y prime.
- Prime = in some candidate key; non-prime = not.
- Violation example: emp_id → dept_id, dept_id → dept_name.
- Fix: decompose chain into DEPT(dept_id, dept_name) + EMPLOYEE(emp_id, name, dept_id).
- 3NF guarantees a dependency-preserving decomposition; BCNF doesn't.
- The classic "3NF not BCNF": R(A,B,C), {AB→C, C→A}.
- Mnemonic: depends on the key, the whole key, and nothing but the key.

## 19. Quiz
1. 3NF bans: a) partial deps b) transitive deps c) MVDs d) JDs → **b**
2. R(A,B,C), F={AB→C, C→A} is: a) 3NF & BCNF b) 3NF not BCNF c) not 3NF d) 1NF only → **b**
3. `dept_id → dept_name` with key {emp_id} is: a) full b) partial c) transitive d) trivial → **c**
4. 3NF's "Y prime" clause exists for: a) performance b) dependency preservation c) security d) 1NF → **b**
5. Prime attribute =: a) member of some candidate key b) non-null c) indexed d) FK → **a**
6. The 3NF fix for emp→dept→name: a) add dept to key b) decompose DEPT(dept_id, dept_name) c) drop name d) merge → **b**
7. Which is NOT guaranteed by 3NF synthesis? a) lossless b) dependency-preserving c) BCNF d) 3NF → **c**
8. An empty department can't be inserted = : a) update anomaly b) insert anomaly c) delete anomaly d) FK → **b**
9. R(A,B,C), F={AB→C, C→B}: a) 3NF b) BCNF c) 2NF only d) 1NF → **a** (C→B has B prime)
10. 3NF may still have redundancy in: a) non-prime attrs b) prime attrs c) keys only d) never → **b**

## 20. Flashcards
- **Q: What is 3NF?** → **A:** 2NF + no transitive dependency of a non-prime attribute on a candidate key.
- **Q: Formal 3NF condition?** → **A:** Every non-trivial X→Y: X superkey OR Y prime.
- **Q: Transitive dependency example?** → **A:** emp_id → dept_id → dept_name.
- **Q: 3NF vs BCNF?** → **A:** 3NF allows Y-prime FDs; guarantees dependency preservation; BCNF stricter.
- **Q: Classic 3NF-not-BCNF relation?** → **A:** R(A,B,C), {AB→C, C→A}.
- **Q: 3NF fix for transitive chain?** → **A:** Decompose into DEPT(dept_id, dept_name) + EMPLOYEE(emp_id, name, dept_id).
- **Q: What is synthesis?** → **A:** Build relations from canonical cover — guarantees 3NF + lossless + preserved.
- **Q: Mnemonic?** → **A:** The key, the whole key, and nothing but the key.

## 21. Revision
3NF = 2NF + **no transitive dependency**: no chain X→Y→Z with Y not a key and Z non-prime. Formal: every non-trivial FD X→Y has X a **superkey** OR **Y prime** (the relaxation that buys dependency preservation). The emp→dept→dept_name chain is the canonical violation → decompose into DEPT(dept_id, dept_name) + EMPLOYEE(emp_id, name, dept_id). **3NF vs BCNF**: the classic R(A,B,C), {AB→C, C→A} is 3NF (C and A prime) but not BCNF (C→A, C not superkey). **Synthesis** (from canonical cover) always gives lossless + dependency-preserving 3NF — which BCNF can't guarantee. Interview moves: state the exact condition (superkey OR prime); give the transitive example; name the "3NF-not-BCNF" relation; and explain why 3NF (not BCNF) is the safe production default.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is 3NF?" | 7 / 13 Q1 |
| "What is a transitive dependency?" | 13 Q2 |
| "Is EMPLOYEE(..., dept_name) in 3NF?" | 13 Q3 |
| "Why the prime-attribute clause?" | 13 Q4 |
| "Classic 3NF-not-BCNF example?" | 13 Q5 |
| "Synthesis algorithm?" | 13 Q10 |
| "What anomalies does 3NF fix?" | 13 Q12 |
| "Can 3NF still be redundant?" | 13 Q16 |
