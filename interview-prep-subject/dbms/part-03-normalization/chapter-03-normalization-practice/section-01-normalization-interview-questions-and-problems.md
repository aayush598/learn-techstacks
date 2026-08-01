# Normalization Interview Questions and Problems

> **TL;DR**: A drill bank of normalization problems — key/prime identification, the 2NF/3NF/BCNF/4NF tests, decomposition with lossless + preservation checks, and the "3NF vs BCNF" judgment calls — each with worked solutions and the exact reasoning interviewers want spoken aloud.

## 1. Why Does This Exist?
Normalization is the single most-tested database topic in interviews because it tests *three* skills at once: whether you can apply a precise formal rule (the FD tests), whether you can see redundancy in a messy real-world schema, and whether you can justify a design trade (3NF vs BCNF vs denormalization). Textbooks give definitions; interviews give *relations and FDs and ask you to act*. This section compiles the highest-signal problems — the ones that recur at Amazon, Google, Meta, and Microsoft — with complete worked solutions, so the pattern recognition (compute closure → find keys → mark primes → test each FD → decompose → verify) becomes automatic.

## 2. How Does It Work?
Every problem follows the same 6-step drill:
1. **List attributes and FDs**; normalize the FD set if needed.
2. **Find all candidate keys** via closure (start with obvious candidates; extend).
3. **Mark prime attributes** = union of candidate keys.
4. **Test each non-trivial FD**: 2NF (no partial dep — proper subset of key → non-prime), 3NF (LHS superkey OR RHS prime), BCNF (LHS superkey only), 4NF (MVD LHS superkey).
5. **If violating, decompose** (on the violating FD, or transitive chain); carry attributes correctly.
6. **Verify**: lossless (shared key rule) + dependency preservation (projection test).
This is the "algorithmic normalization" that eliminates guesswork — the exact procedure below.

## 3. When Is It Used?
- **Interview drills**: practice problems mirror real questions (this is the section to reread before any DB interview).
- **Schema reviews**: running the drill on a proposed table catches violations before they ship.
- **Homework/exams**: the 6-step method is exactly what normalized answers grade for.
- **Peer design discussions**: "is this in BCNF?" resolves arguments with closure, not opinions.
- **Building the mental model**: the drill makes the formal definitions *usable*.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: memorize definitions.** Rejected — interviewers ask "is R in 3NF?" not "state 3NF." You need the procedure.
- **Alternative: eyeball the schema.** Rejected — transitive/partial dependencies hide; only the closure-based test is reliable (and shows rigor).
- **Alternative: memorize this section's answers.** Rejected — new relations appear every interview; the *method* transfers, the answers don't.
- **Why the exact 6-step order?** Because keys first (to mark primes) is what makes 2NF/3NF tests fast and correct; reversing the order (testing FDs before keys) is the classic mistake.

## 5. Intuition
Think of normalization as **a checklist for each arrow (FD)** in your schema:
- Does any *part* of the key determine a non-key column? → **2NF violation** (partial dep).
- Does a *non-key* column determine another non-key column? → **3NF violation** (transitive dep).
- Does *anything* that isn't a full key determine anything? → **BCNF violation**.
- Does a *column set* that isn't a key determine a set of independent values? → **4NF violation** (MVD).
Every problem is: find the keys, then run each arrow through these four gates. The gate that fails names the violation; the fix is always "split so the arrow starts at a key."

## 6. Real-World Analogy
The normalization drill is like **auditing a spreadsheet**: each column is a fact, each key is a row ID, and each rule "column determines column" is a dependency. The auditor (you) checks every fact against the row's ID: "does this fact depend on the *whole* ID? (2NF) on the ID *and nothing else*? (3NF) and is the fact's owner itself an ID? (BCNF)". Problems in this section are the auditor's case files — same six steps, different businesses, and the answer format (keys → violations → split → verify) is the auditor's report.

## 7. Formal Definition
- **Key**: minimal superkey (closure of key = all attributes; removing any attribute breaks closure).
- **Prime**: in some candidate key. **Non-prime**: in none.
- **Partial dep**: X ⊂ key, X→Y, Y non-prime (2NF violation).
- **Transitive dep**: X→Y, Y→Z, Y non-superkey, Z non-prime (3NF violation).
- **BCNF**: every non-trivial FD X→Y has X superkey.
- **3NF**: every non-trivial X→Y has X superkey OR Y prime.
- **Lossless binary split** (R1(X,Y), R2(X,Z)): X→Y or X→Z ∈ F⁺.
- **Dependency preservation**: projected FDs imply F.

## 8. Example — a full worked problem
**Problem**: R(A, B, C, D), F = {A→B, BC→D, D→C}. Highest normal form? Decompose to BCNF if possible.
- **Closures**: A⁺ = {A,B}; BC⁺ = {B,C,D}; D⁺={D,C}; so A alone insufficient. Try {A,?}: need C and D. A,BC→D gives D; D→C gives C; so {A,B,C}? Check: {A,B,C}⁺ = A,B,C,D → all. Is it minimal? Remove C: {A,B}⁺={A,B} ✗; remove B: {A,C}⁺={A,C} (D? BC→D needs B) → {A,C} not key. So {A,B,C} is a candidate key (but check smaller: {A,D}? A⁺={A,B}, D→C gives C, so {A,D}⁺ = A,B,C,D ✓!). Minimal {A,D}: remove A → {D}⁺={D,C} ✗; remove D → {A}⁺={A,B} ✗. So **keys = {A,D}, {A,B,C}**. Hmm wait — also check {A,D} then primes = A,B,C,D (all prime!). So every attribute is prime.
- **Test BCNF**: A→B: A⁺={A,B} ≠ R → **not BCNF** (violation). BC→D: BC⁺={B,C,D}≠R → not BCNF. D→C: D⁺={D,C}≠R → not BCNF.
- **Test 3NF**: A→B: B prime ✓ (so 3NF passes); BC→D: D prime ✓; D→C: C prime ✓. All RHS prime → **3NF ✓**.
- **Decompose to BCNF** on D→C: R1(D,C) key {D}; R2(A,B,D) — remove C, keep D (the LHS): R2(A,B,D). Check R2 FDs: A→B ✓ (A⁺ in R2 = {A,B}); D→C? C gone from R2 — D→C lives in R1. R2 keys: {A,D} (A⁺={A,B}, D gives... R2 has A,B,D: {A,D}⁺ = A,B,D ✓). R1(D,C): key {D}, D→C ✓ BCNF. R2: A→B: A⁺(in R2)={A,B}≠R2 → still violates → split on A→B: R2a(A,B) key {A}; R2b(A,D) key {A,D}. All three pieces BCNF.
- **Verify lossless**: D→C split (shared D: D→C ✓) lossless; A→B split (shared A: A→B ✓) lossless → overall lossless.
- **Dependency preservation**: D→C (R1 ✓), A→B (R2a ✓), BC→D: attributes B,C,D — C in R1, B in R2a, D in R1/R2b — **straddles → LOST**. So BCNF here is lossless but loses BC→D; the 3NF schema (no split) preserves it. **Decision**: keep 3NF unless BC→D can be app-enforced.

## 9. Internal Working — the drill in detail
1. **Normalize FDs**: strip extraneous attributes, drop redundant FDs (canonical cover) so the set is clean.
2. **Find keys**: compute closures of plausible candidates; a candidate key's closure must be all attributes; check minimality.
3. **Mark primes**: union all candidate keys.
4. **Gate each FD** (non-trivial only): partial? transitive? non-superkey-LHS? non-superkey-LHS-with-prime-RHS?
5. **Decompose**: on the violating FD X→Y: R1(X,Y), R2((R−Y)∪X); on a transitive chain X→Y→Z: R1(Y,Z), R2(R−Z... careful — R2 keeps X,Y).
6. **Verify** lossless + preservation; if preservation fails and it matters, backtrack to 3NF.

## 10. Time Complexity
- **Closure**: O(|F|·|R|) with a set-based loop — instant for exam sizes.
- **Key finding**: O(2^|R|) worst-case in theory; interviews use ≤ 6 attributes.
- **Per-FD test**: one closure each; 6-step drill runs in seconds by hand.
- **Decomposition + verify**: O(#FDs × closure); trivial.

## 11. Advantages
- **Pattern recognition**: the drill applies to any relation — no memorization needed.
- **Rigor that interviewers reward**: naming "D→C has non-superkey LHS" beats guessing.
- **Full-ladder coverage**: 2NF→BCNF→4NF tests in one method.
- **Judgment built-in**: the lossless/preservation checks teach when to *stop* decomposing (the 3NF-vs-BCNF call).
- **Immediate self-check**: answers can be verified mechanically.

## 12. Disadvantages
- **Detail-sensitive**: an off-by-one attribute in the split breaks losslessness.
- **Decomposition can explode** for big relations — interviews avoid > 6 attributes.
- **F⁺ vs F**: testing only F (not F⁺) can miss implied violations — always use closures.
- **Doesn't cover MVDs/JDs** — for 4NF/5NF you need the swap/join tests.
- **The "3NF or BCNF?" judgment** has no single right answer — it's a stated trade, which can feel unsatisfying.

## 13. Interview Questions
1. **Q: R(A,B,C,D), F={A→B, BC→D, D→C}. Find keys; highest normal form.** A: Keys {A,D} and {A,B,C} (all attributes prime). BCNF fails (A→B, BC→D, D→C all non-superkey LHS). 3NF holds (all RHS prime). See Section 8 for the full decomposition.
2. **Q: R(A,B,C), F={AB→C, C→A}. 3NF? BCNF?** A: Keys {AB},{BC}. C→A: C not superkey, A prime → 3NF ✓; BCNF ✗. Classic "3NF not BCNF."
3. **Q: R(A,B,C,D), F={A→B, B→C}. 2NF?** A: Key {A,D}. B→C transitive (A→B→C) → not 3NF. Partial? A→B is a full dependency on {A} which is part of {A,D}? A⊂key and A→B → **partial** → not even 2NF. (Also B→C transitive.) Fix: R1(A,B), R2(A,C)?? no — proper: split B→C: R1(B,C), R2(A,B,D); then A→B in R2 (A superkey there ✓).
4. **Q (tricky): R(A,B,C,D), F={AB→C, C→D, D→A}. Keys?** A: AB⁺: A,B → C→D → A: AB⁺=ABCD ✓ minimal? {A}✗,{B}✗ → {AB} key. Also {C,B}? C→D→A, B: {B,C}⁺=A,B,C,D ✓ → {BC} key. Also {B,D}? D→A, B: {B,D}⁺=A,B,C,D ✓ → {BD} key. Keys {AB},{BC},{BD}; primes A,B,C,D. FDs: C→D (D prime ✓ 3NF; C not superkey ✗ BCNF), D→A (A prime ✓ 3NF; ✗ BCNF). Highest = **3NF, not BCNF**.
5. **Q: R(A,B,C,D,E), F={AB→C, C→D, D→E}. Normalize to 3NF.** A: Key {A,B}. Violations: C→D (transitive A→B→C→D), D→E. Decompose D→E: R1(D,E) key {D}; R2(A,B,C,D). Then C→D: C⁺ in R2 = {C,D}≠R2 → split R2: R2a(C,D) key {C}; R2b(A,B,C). All 3NF; lossless; preserved.
6. **Q (scenario): A table has (order_id, customer_id, customer_city, product_id, qty) with order_id→customer_id and customer_id→customer_city. Issues?** A: Transitive: order_id→customer_id→customer_city → customer_city repeats per order; rename city = update every order. 3NF fix: CUSTOMER(customer_id, city), ORDERS(order_id, customer_id, product_id, qty).
7. **Q: Is R(A,B,C), F={A→B, B→C, C→A} BCNF?** A: A⁺=ABC → {A} key; B⁺=ABC → {B} key; C⁺=ABC → {C} key. Every FD LHS is a key → **BCNF** (and 3NF, 2NF).
8. **Q (tricky): R(A,B,C,D), F={A→C, D→B}. 2NF?** A: Keys? {A,D} (A→C, D→B) → {A,D}⁺=ABCD ✓ minimal. Partial: A⊂{A,D}, A→C, C non-prime → **partial → not 2NF**. Decompose: R1(A,C), R2(A,B,D); then R2: D→B partial (D⊂key {A,D}) → split R2a(D,B), R2b(A,D). Result R1(A,C), R2a(D,B), R2b(A,D) — all 2NF; actually each BCNF; lossless + preserved.
9. **Q: What if a decomposition is lossless but not dependency-preserving?** A: You chose a split where an FD straddles tables (AB→C). Fix: pick the 3NF synthesis (preserves), or enforce the lost FD in the app. (Sections 02/05.)
10. **Q (hard): R(A,B,C,D), F={A→B, B→C, C→D}. Decompose to BCNF.** A: Key {A}. Chain A→B→C→D. Decompose C→D: R1(C,D), R2(A,B,C); then B→C in R2: B⁺(R2)={B,C}≠R2 → split R2: R2a(B,C), R2b(A,B). Result: R1(C,D), R2a(B,C), R2b(A,B) — each BCNF; lossless; preserved. (This is the standard transitive-chain collapse.)
11. **Q: When is a relation automatically BCNF?** A: When every non-trivial FD has a superkey LHS — e.g., single-attribute keys everywhere, or no FDs beyond key-implied ones (like R(A,B,C) with only key FD ABC→{...}).
12. **Q (tricky): R(A,B,C), F={A→B, B→C, C→B}. Keys? Normal form?** A: A⁺=ABC → {A} key; {B,C}? B⁺=BC, C⁺=CB → {B,C}⁺=ABC → also key? check C→B, B→C so {B,C} minimal → {B,C} key too. Keys {A}, {B,C}. Primes A,B,C. FDs: A→B (superkey ✓); B→C: B not superkey, C prime → 3NF ✓, BCNF ✗; C→B: C not superkey, B prime → 3NF ✓, BCNF ✗. **3NF not BCNF**.
13. **Q: Why does BCNF decomposition sometimes lose AB→C but 3NF never loses it?** A: 3NF's synthesis groups FDs by full LHS into relations, so each FD is fully contained somewhere; BCNF splits on non-superkey LHS, which can separate an FD's attributes. (Sections 02–03.)
14. **Q (scenario): table(emp_id, dept_id, dept_name, project_id, role) with emp_id→dept_id, dept_id→dept_name, (emp_id,project_id)→role. Find normal form.** A: Key {emp_id, project_id}. Partial: emp_id→dept_id (emp_id ⊂ key, dept_id non-prime) → **not 2NF**. Transitive: emp_id→dept_id→dept_name. Fix: DEPT(dept_id, dept_name); EMP_PROJECT(emp_id, dept_id, project_id, role) → then key {emp_id,project_id}, no partial/transitive → 3NF. Each table BCNF.
15. **Q: How do you quickly spot a transitive dependency in a schema?** A: Chain pattern: a non-key column (dept_id) followed by a column it owns (dept_name) — "X → Y → Z where Y isn't a key." Same as renaming Y forcing many updates.
16. **Q (tricky): R(A,B,C,D,E), F={A→B, BC→D, DE→A}. Keys?** A: {C,E}? need A,B,D: DE→A gives A; A→B; BC→D needs C and B — {C,E}+D→A→B: wait start {C,E}: CE→A (DE→A needs D) no. Try {B,C,E}: BC→D, DE→A, A→B: BCE⁺= A,B,C,D,E ✓. Minimal? Remove C: {B,E}? need C... ✗. Remove B: {C,E}? need D first ✗. So {B,C,E} key (check {D,E}? DE→A→B, then need C ✗; {A,C,E}? A→B, BC→D: {A,C,E}⁺=A,B,C,D,E ✓ → also key! remove C? {A,E}⁺={A,E} ✗). Keys {B,C,E}, {A,C,E}. Primes A,B,C,E (D non-prime!). FDs: A→B (B prime ✓ 3NF; A not superkey ✗ BCNF); BC→D (D non-prime, BC not superkey → **3NF violation!**); DE→A (A prime, DE not superkey → 3NF ✓, BCNF ✗). **Not 3NF** (BC→D). Highest 2NF. Fix: decompose on BC→D etc.
17. **Q: Define and detect the three anomaly types.** A: Update (change dept_name once → many rows), Insert (can't add empty dept), Delete (last employee erases dept name). All from transitive/partial redundancy; normalization removes them.
18. **Q (production): Is there ever a case to STOP at 2NF?** A: Rarely, but read-heavy 1:1 attribute panels might intentionally store redundant cheap facts (Section 06 denormalization); otherwise the target is 3NF/BCNF.
19. **Q (hard): R(A,B,C), F={A→B, B→C, C→A} vs R(A,B,C), F={A→B, B→C}. Difference in normal form?** A: First is BCNF (all LHS keys). Second: key {A}; B→C transitive (B not superkey, C non-prime) → **not 3NF**. Same attributes, different FDs — normal form is a property of the FDs, not the relation shape.
20. **Q: Walk me through the exact answer format for "normalize this."** A: (1) state keys; (2) name primes; (3) test each non-trivial FD by gate (partial/transitive/BCNF/3NF clause); (4) name the highest NF; (5) decompose the violating FDs, carry LHS into both parts; (6) verify lossless + preservation; (7) state the trade if BCNF loses a dependency.

## 14. Follow-Up Questions
1. **Q: How do implied FDs (F⁺) change the test?** A: A superkey might be implied (e.g., C→A makes {C,B} a key), and violations can be discovered via closure (X⁺ covers the RHS) — always compute closures, never just scan listed FDs.
2. **Q: Can two relations have the same FDs but different normal forms?** A: Normal form depends only on the FD set + attributes, so identical FDs give identical normal forms; different *instances* don't change NF (NF is a schema property).
3. **Q: What's the difference between a superkey and candidate key in decomposition?** A: Decomposition splits on FDs where X must be a superkey (BCNF); for 3NF, X may be non-superkey if RHS is prime. Candidate keys matter for *marking primes*, not for the FD tests directly.
4. **Q: How do MVDs change these drills?** A: If the relation has no non-trivial FDs but still multiplies rows (skills×languages), run the MVD swap test and 4NF split (Section 04).
5. **Q: What should the final answer always include?** A: Highest normal form + justification (which FD violates what) + the decomposition + the two verification properties — completeness is what earns the "strong hire."

## 15. Coding Example
```python
# The full normalization drill as code
def closure(x, fds):
    res = set(x); changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= res and not rhs <= res:
                res |= rhs; changed = True
    return res

def normalize(attrs, fds):
    attrs = set(attrs)
    non_triv = [(l, r) for (l, r) in fds if not r <= l]
    report = {}
    # gate each FD
    for l, r in non_triv:
        cl = closure(l, fds)
        report[(l, r)] = {
            'closure': cl,
            'superkey': cl == attrs,
        }
    # 2NF/3NF/BCNF gates need keys+primes: (illustrative; keys computed below)
    return report

# Candidate keys via minimal superkeys
from itertools import combinations
def candidate_keys(attrs, fds):
    attrs = set(attrs); keys = []
    for k in range(1, len(attrs) + 1):
        for combo in combinations(attrs, k):
            if closure(set(combo), fds) == attrs:
                if not any(set(ck) < set(combo) for ck in keys):
                    keys.append(set(combo))
        if keys: break
    return keys   # e.g., R(A,B,C),{AB->C,C->A} -> [{A,B},{B,C}]
```
```sql
-- Verifying a decomposition in SQL: lossless check by comparing counts
-- Source R(A,B,C) with F={AB->C, C->A}
CREATE VIEW v_ac AS SELECT DISTINCT c,a FROM r;
CREATE VIEW v_bc AS SELECT DISTINCT b,c FROM r;
SELECT (SELECT count(*) FROM r) = (SELECT count(*) FROM v_ac JOIN v_bc USING (c)) AS lossless_ok;
-- 't' means joining the pieces reproduces the original row count.
```

## 16. Industry Usage
- **Schema design interviews**: every big-tech DB round includes at least one "normalize R(A,B,C,D), F=..." question — this drill is the preparation.
- **Data-modeling reviews**: teams gate PRs on "is this 3NF/BCNF?"; the 6-step drill is the shared vocabulary.
- **ORM/Prisma model reviews**: generated models get checked for transitive/partial deps using the same gates.
- **Legacy migration**: normalizing a messy legacy table is a documented application of this exact procedure.
- **The 3NF-vs-BCNF judgment** shows up in system design ("would you keep this in 3NF?") — knowing the trade reads as senior.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14 (normal forms, decomposition algorithms).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 7 (normalization).
- Ullman, *Principles of Database and Knowledge-Base Systems*, Ch. 7.
- Codd 1970/1971; Boyce-Codd 1974; Fagin 1977 (original papers).
- Maier, *The Theory of Relational Databases*, Ch. 6–7 (closure, chase, algorithms).

## 18. Cheat Sheet
- Drill: keys → primes → gate each FD → decompose → verify lossless+preserve.
- 2NF: no partial (X⊂key → non-prime). 3NF: no transitive (X→Y→Z). BCNF: every arrow from a superkey.
- Decompose on X→Y: R1(X,Y), R2((R−Y)∪X).
- Lossless binary: shared X is key of a side. Preservation: no FD straddles tables.
- Classic traps: AB→C/C→A (3NF not BCNF); skills×languages (4NF); the chain A→B→C→D collapse.
- Always compute closures; never eyeball.
- 3NF keeps dependencies; BCNF may not — state the trade.

## 19. Quiz
1. R(A,B,C), F={AB→C, C→A}: highest NF? a) BCNF b) 3NF c) 2NF d) 1NF → **b**
2. R(A,B,C), F={A→B, B→C}: highest NF? a) BCNF b) 3NF c) 2NF d) 1NF → **c** (transitive B→C)
3. R(A,B,C), F={A→B, B→C, C→A}: NF? a) BCNF b) 3NF c) 2NF d) 1NF → **a** (all LHS keys)
4. R(A,B,C,D), F={A→C, D→B}: key? a) {A,D} b) {A,B} c) {C,D} d) {A} → **a**
5. Partial dependency means: a) subset of key → non-prime b) transitive c) MVD d) JD → **a**
6. {AC},{BC} split of R(A,B,C),{AB→C,C→A} is: a) lossless+preserved b) lossless, not preserved c) not lossless d) 4NF → **b**
7. R(A,B,C,D), F={A→B, BC→D, D→C}: primes? a) all b) A,B only c) D,C d) none → **a** (keys {A,D},{A,B,C})
8. The transitive chain in emp(dept) problem: a) emp→dept→city b) key→key c) nothing d) MVD → **a**
9. Decompose on X→Y yields: a) (X,Y)+(R−Y∪X) b) (X,Y)+(R) c) merge d) keep → **a**
10. BCNF vs 3NF trade: a) BCNF preserves more deps b) 3NF preserves deps, BCNF may lose c) identical d) 3NF faster → **b**

## 20. Flashcards
- **Q: 6-step normalization drill?** → **A:** Keys → primes → gate FDs → decompose → verify lossless+preserve → state trade.
- **Q: 2NF violation?** → **A:** Partial dep: subset of key → non-prime.
- **Q: 3NF violation?** → **A:** Transitive: X→Y→Z, Y non-key.
- **Q: BCNF rule?** → **A:** Every non-trivial FD from a superkey.
- **Q: Classic 3NF-not-BCNF?** → **A:** R(A,B,C), {AB→C, C→A}.
- **Q: Decompose on X→Y?** → **A:** R1(X,Y), R2((R−Y)∪X).
- **Q: Lossless test?** → **A:** Shared X is a key of one side.
- **Q: Why 3NF over BCNF?** → **A:** 3NF preserves dependencies; BCNF may not.

## 21. Revision
Master the **6-step drill**: (1) keys via closure, (2) primes = union of keys, (3) gate every non-trivial FD — partial (2NF), transitive (3NF), non-superkey-LHS (BCNF), MVD (4NF), (4) decompose on the violator with R1(X,Y)+R2((R−Y)∪X), (5) verify **lossless** (shared X is a key of a side) and **preservation** (no FD straddles), (6) name the highest NF and state the trade. The three exam archetypes: **A→B→C chain** (collapse to R1(B,C),R2(A,B)); **AB→C/C→A** (3NF not BCNF — C→A has prime RHS); **all-LHS-keys** (automatic BCNF). Always use closures (F⁺), never eyeball. Final answers include the decomposition AND both verifications — that completeness is the difference between a pass and a strong hire.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Normalize R, find keys / NF" | 8 / 13 Q1, Q4, Q16 |
| "Classic 3NF-not-BCNF trap" | 13 Q2 |
| "Transitive/partial spot-checks" | 13 Q3, Q6, Q15 |
| "BCNF decomposition & lost dep" | 8 / 13 Q9, Q10 |
| "A→B→C chain collapse" | 13 Q10 |
| "When is a relation auto-BCNF?" | 13 Q11 |
| "Anomaly types" | 13 Q17 |
| "Answer format for normalize-this" | 13 Q20 / 14 Q5 |
