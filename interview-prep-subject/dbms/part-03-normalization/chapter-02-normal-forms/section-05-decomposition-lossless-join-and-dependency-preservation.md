# Decomposition: Lossless-Join and Dependency Preservation

> **TL;DR**: Decomposition splits a relation into smaller ones during normalization, but you must verify two properties: **lossless-join** (joining the parts reproduces exactly the original rows — no invented, no lost data) and **dependency preservation** (every functional dependency can still be enforced within a single decomposed table). Both tests come straight from attribute closure and the chase.

## 1. Why Does This Exist?
Normalization forces you to split relations — but a careless split can silently corrupt data in two ways. **Information loss**: you split R(A,B,C) into R1(A,B) and R2(B,C); if A and C both depend on B but B alone doesn't identify rows, joining back can *invent* combinations that never existed (the suppliers-parts-projects trap) or drop rows. **Rule loss**: an FD like `emp_id → dept_id, dept_name` whose attributes straddle two tables can no longer be enforced by any single table's constraints — your data model "forgot" a business rule. Decomposition theory exists to make splitting *safe*: the lossless-join test guarantees perfect round-tripping, and dependency preservation guarantees your integrity rules survive the split. Every normalization algorithm (3NF synthesis, BCNF decomposition) is judged by whether it satisfies both.

## 2. How Does It Work?
**Lossless-join (exact)**: A decomposition ρ = {R1,…,Rk} of R is lossless iff R = π_R1(R) ⋈ π_R2(R) ⋈ … ⋈ π_Rk(R). Equivalent test for a binary split into R1(X,Y), R2(X,Z): lossless iff `X → Y` or `X → Z` (i.e., X is a superkey of R1 or R2) — the shared attribute set must be a key in at least one part.
**Dependency preservation (exact)**: F' = ∪ projection of F onto each Ri must *imply* F (F ⊆ F'⁺). For every FD X→Y ∈ F, compute X's closure using only FDs that are fully inside some Ri; if Y ⊆ X⁺ computed this way for all FDs, the decomposition preserves dependencies.
**The chase**: a tableau algorithm to test losslessness and dependency implication in one go — align attributes, apply FDs by equating, and check if a goal row of all-unmarked values is derivable.

## 3. When Is It Used?
- **Every normalization exercise**: after decomposing to 3NF/BCNF, verify lossless + preservation — interviewers always ask "is this decomposition good?"
- **Real schema refactors**: splitting a wide table (vertical partitioning, attribute extraction) demands the lossless test before you ship.
- **Designing join tables / junction tables**: the shared-key test justifies the split.
- **Validating ORM model changes**: "can I reconstruct the old row?" is the lossless question.
- **Data warehouses**: fact/dimension splitting must be lossless or analytics counts lie.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: don't decompose (denormalize).** Rejected where normalization matters — you keep anomalies to avoid joins; decomposition theory exists because splitting is otherwise dangerous.
- **Alternative: decompose and hope the FK joins work.** Rejected — FK constraints guarantee referential *integrity*, NOT losslessness. Two tables can be perfectly foreign-keyed yet rejoin into bogus rows.
- **Alternative: reconstruct with DISTINCT or aggregation.** Rejected — deduplicating hides the problem but the join may still drop or invent legitimate rows; correctness must be exact.
- **Why the chase?** Because attribute closure alone tests FDs, but losslessness of *k-way* splits needs a tableau method — the chase is the complete, uniform answer.

## 5. Intuition
- **Lossless-join** = a **jigsaw puzzle**: if I photograph each piece separately and then merge the photos, do I get exactly the original picture? If pieces share a "key line" (a column set that pins down each piece uniquely), the reassembly is perfect. If they share only a common *area* with repeats, merging duplicates and gaps — invented combos and lost rows.
- **Dependency preservation** = the **rule book stays intact**: each business rule must be checkable inside one drawer. If "an employee has one department" is enforced by a UNIQUE/FK in a single table, the rule lives; if it spans two tables, no single drawer can check it, so the app must — and apps forget.

## 6. Real-World Analogy
- **Lossless** — a **chemistry lab inventory**: you split "compound records" into "compound + supplier" and "compound + hazard". Both share `compound_id`. Because compound_id pins each row in both tables, rejoining reproduces every original record exactly. But if you split instead by `supplier_name` (not unique), two suppliers sharing a compound collide and rejoining fabricates cross-products — exactly like the suppliers-parts-projects invention. The shared key is the safety line.
- **Preservation** — a **cafeteria's allergy rules**: "every dish tagged 'nut' must avoid nuts." If the rule lives fully inside the dish table (dish → allergen), the kitchen enforces it locally. If "dish → allergen → nut-free supplier" spans two tables, no single sign enforces the full rule — the kitchen must remember it across both. Preservation is about keeping each rule enforceable in one place.

## 7. Formal Definition
(Elmasri & Navathe Ch. 14–15; Silberschatz Ch. 7.3–7.4; Ullman Ch. 7.3.)
- **Lossless join**: ρ = {R1,…,Rk} is a lossless decomposition of R iff R = ⋈_{i=1..k} π_Ri(R).
- **Binary test**: split into R1(X,Y), R2(X,Z) is lossless iff (X→Y) ∈ F⁺ or (X→Z) ∈ F⁺.
- **Dependency preservation**: (∪_{i=1..k} π_Ri(F))⁺ = F⁺, i.e., F ⊆ F'⁺ where F' = union of projections.
- **Chase test**: build a tableau with one row per Ri; apply each FD by merging column values; the decomposition is lossless iff some row becomes all "distinguished" (a full key row).

## 8. Example
`R(A, B, C)`, F = {AB→C}.
- **Lossless split**: R1(A,B) [key A→B? A⁺=A, so no], R2(B,C)? Shared set {B}: B→C? B⁺={B}≠{B,C} and B→A? no → **NOT lossless** — this split loses AB→C pairing.
- **Lossless split**: R1(A,B), R2(A,C)? Shared {A}: check A→B (no), A→C (no) — **not lossless** either.
- **Correct split**: R1(A,B), R2(A,B,C)... no. For {AB→C}: split R1(A,B) key {A,B} and R2... wait — decompose AB→C: R1 = (A,B,C)? no.
- **Right move**: to split losslessly on AB→C you keep AB together: R1(A,B) + R2(A,B,C) is trivial. **Better example**: F = {AB→C, C→A} from earlier: split on C→A → R1(C,A) key {C}, R2(B,C) key {B,C}. Shared {C}: C→A ∈ F ✓ → **lossless**. Dependency `AB→C` spans both → **not preserved**. Contrast with 3NF synthesis preserving it.

**Verify with chase** (F={AB→C,C→A}, split {AC},{BC}):
- Tableau rows: AC → [a₁,c₂]... chase with C→A forces a-columns equal; C→A forces c equal; AB→C can't apply (A,B not together in any row) — but row 1 becomes (a,c) distinguished ✓ → lossless.

## 9. Internal Working
1. **For a binary split** R1(X,Y) / R2(X,Z): compute X⁺ under F; lossless iff Y ⊆ X⁺ or Z ⊆ X⁺.
2. **For k-way splits**: run the **chase** — tableau of k rows (one per Ri), attributes as columns; values = distinguished for Ri's attributes, non-distinguished otherwise. Apply each FD X→Y: wherever two rows agree on X, make their Y equal. If any row becomes all-distinguished → lossless.
3. **Dependency preservation**: for each FD X→Y in F: compute the closure of X using *only* FDs whose attributes live in a single Ri. If Y ⊆ closure → preserved; else the FD is lost.
4. **If lost**: either fall back to a different decomposition (3NF synthesis preserves by construction) or enforce the FD in the application layer.

## 10. Time Complexity
- **Binary lossless test**: one closure O(|F|·|R|²) — trivial.
- **Chase**: polynomial for typical cases (PSPACE-hard worst-case in the abstract), fine in practice.
- **Preservation test**: O(#FDs × closure) with projected FDs.

## 11. Advantages
- **Guaranteed correct splits**: no invented or lost rows after join.
- **Enforceable rules**: FDs stay checkable inside single tables — the app doesn't silently carry undocumented rules.
- **Foundation of 3NF synthesis**: the algorithm's correctness *is* the lossless + preservation proof.
- **Standard interview math**: closure + chase answers "is this decomposition good?" in seconds.
- **Production-grade refactoring**: vertical partitioning justified by the same test you learned for homework.

## 12. Disadvantages
- **BCNF can't always preserve** — the famous AB→C loss; you must choose (decompose to BCNF and lose a rule, or keep 3NF).
- **Chase is fiddly** by hand for k > 2; error-prone under interview pressure.
- **Lossless ≠ intuitive**: two tables with matching FKs can still rejoin into garbage.
- **Preservation is subtle**: a preserved FD might still be expensive to check (multi-table triggers).
- **Over-decomposition risk**: more tables, more joins — the properties guarantee correctness, not performance.

## 13. Interview Questions
1. **Q: What is a lossless-join decomposition?** A: R = π_R1(R) ⋈ … ⋈ π_Rk(R) — joining the projections reproduces exactly R.
2. **Q: Binary lossless test?** A: Split R1(X,Y), R2(X,Z) is lossless iff X→Y or X→Z ∈ F⁺ (X is a key of one side).
3. **Q: What is dependency preservation?** A: The union of FDs projected onto the Ri must imply all original FDs — every rule enforceable within some single table.
4. **Q (classic): R(A,B,C), F={AB→C,C→A}; is {AC},{BC} lossless?** A: Shared C, C→A ∈ F → lossless. But AB→C spans both tables → dependency **not preserved**.
5. **Q (tricky): split R(A,B,C), F={AB→C} into {AB},{BC}?** A: Shared {B}: B→A? no; B→C? no → **not lossless**. Rejoining invents rows.
6. **Q: Why doesn't an FK guarantee losslessness?** A: FKs ensure referenced values exist, not that the join count matches the original rows. Two valid FK tables can produce extra combos on join.
7. **Q: What is the chase algorithm?** A: A tableau test: build rows from projections, apply FDs by merging values; if a row becomes fully distinguished, the decomposition is lossless.
8. **Q: Can BCNF lose dependencies?** A: Yes — AB→C in the classic example. 3NF's synthesis never loses them (that's its whole point).
9. **Q (scenario): Your 3NF split lost emp_id→dept_name. What do you do?** A: Either re-decompose so the FD's attributes stay together, or enforce via app/trigger. The projection test tells you it's lost.
10. **Q: What does "implied by F" mean for preservation?** A: X→Y is preserved iff Y ⊆ (closure of X using only FDs fully contained in some Ri). You can rebuild the original rules from the pieces.
11. **Q (hard): Is a split into R1(A,B), R2(A,C), R3(B,C) of R(A,B,C) with F={A→B, A→C} lossless?** A: Shared attribute pairs; A→B (in R1 ✓), A→C (in R2 ✓). Check: joins of R1,R2 on A recover A,B,C → lossless (A is a key of R1 and R2).
12. **Q: Why is 3NF synthesis lossless AND preserving by construction?** A: It builds relations around each canonical-cover FD's full LHS and adds a candidate-key relation, so every FD is contained and the key relation pins the join.
13. **Q: Difference between lossless and preserving?** A: Lossless = data integrity (rows round-trip). Preserving = rule integrity (FDs stay enforceable). A decomposition can have one without the other — AB→C case: lossless but not preserving.
14. **Q (tricky): R(A,B,C,D), F={A→B, C→D}; split into {AB},{CD}?** A: No shared attribute → join = Cartesian product → lossless only if R itself is the product (it's not, since AB×CD ⊇ R but R has A,B,C,D with A→B pairing). Not lossless (rows without C→D pairing invented).
15. **Q: When is a decomposition lossless with a shared key?** A: Whenever the shared set X is a superkey in at least one Ri (X→R_i ∈ F⁺). That's the whole binary rule.
16. **Q (production): Vertical partition a table safely?** A: Split on a shared column set that is a key in one partition; keep the key in both; verify with the closure test. That's the lossless rule applied to schema refactoring.
17. **Q: What are the two things to check after ANY decomposition?** A: (1) Lossless join; (2) dependency preservation. If both hold, the split is semantically clean.
18. **Q (hard): Explain the chase with an example.** A: R(A,B,C), F={B→C}; split {AB},{AC}? Tableau rows AB→(a1,b1,c0), AC→(a1,b0,c1). Apply B→C: b1≠b0 so no merge; no row all-distinguished (a1,b1,c1 never forms) → not lossless.
19. **Q: Does losslessness guarantee no duplicate rows after join?** A: Yes for proper lossless (R = join exactly); if a split is lossy, joins may duplicate — deduping with DISTINCT still can't recover dropped/invented rows.
20. **Q: Why is preservation a "nice-to-have" only for BCNF?** A: BCNF correctness is losslessness + (sometimes) you accept a lost FD because no preserving BCNF split exists. Preservation is guaranteed for 3NF, optional for BCNF.

## 14. Follow-Up Questions
1. **Q: How is the chase related to the closure test?** A: The chase is a generalization — closure tests a single FD's implication; the chase tests losslessness and JD implications via the same tableau machinery.
2. **Q: What's the connection to JDs (5NF)?** A: A decomposition's losslessness IS the statement that the corresponding join dependency holds. 5NF asks whether that JD is justified by keys.
3. **Q: Can two lossless decompositions be composed?** A: Yes — a lossless decomposition of a lossless decomposition is lossless (property composes transitively).
4. **Q: Preservation — is it really "all FDs" or "canonical cover"?** A: Checking a canonical cover F_c suffices: if F_c ⊆ F'⁺ then F ⊆ F'⁺. Cheaper in practice.
5. **Q: In production, is a lost FD always fatal?** A: No — if the app enforces the rule (unique checks across tables, service logic), it's acceptable; but schema-level enforcement is safer, which is why 3NF is preferred.

## 15. Coding Example
```sql
-- R(A,B,C), F={AB->C, C->A} as tables:
CREATE TABLE r1_ca (c TEXT PRIMARY KEY, a TEXT);      -- R1(C,A)
CREATE TABLE r2_bc (b TEXT, c TEXT REFERENCES r1_ca(c), PRIMARY KEY (b,c)); -- R2(B,C)
-- Lossless: join on c recovers R exactly.
-- AB->C is NOT preserved in the schema; enforce with an app check:
--   FORBID a new (a,b,c) unless AB->C holds across both tables.

-- Production-safe vertical split (lossless by shared key):
CREATE TABLE emp_core (emp_id INT PRIMARY KEY, name TEXT);
CREATE TABLE emp_detail (emp_id INT PRIMARY KEY REFERENCES emp_core, salary INT);
-- Shared emp_id is a key in BOTH -> trivially lossless; join recovers everything.
```
```python
def closure(x, fds):
    res = set(x)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= res and not rhs <= res:
                res |= rhs; changed = True
    return res

def lossless_binary(r1, r2, shared, fds):
    # lossless iff shared -> r1-others  or  shared -> r2-others
    return closure(shared, fds) >= (r1 | r2)
    # ...returns True iff the split round-trips exactly.
```

## 16. Industry Usage
- **Schema refactors**: splitting wide "god tables" (Postgres/Mongo->relational migrations) is judged by the lossless test — data teams literally verify `SELECT count(*) FROM R = count(*) FROM R1⋈R2`.
- **3NF/BCNF in review checklists**: "is this decomposition lossless and dependency-preserving?" is a standard line in Amazon/Google schema design interviews.
- **Data warehouses**: fact/dimension splitting must be lossless or aggregation counts inflate; the chase-equivalent is routinely run on join tests.
- **ORM migrations** (Prisma/Hibernate): every relation extraction is a decomposition — the shared-key rule explains why FK extraction is safe.
- **The suppliers-parts-projects lesson** is directly cited when teams get burned by multi-table joins producing phantom combinations.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14.5 (lossless), 14.7 (preservation), 15 (chase).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 7.3–7.4.
- Ullman, *Principles of Database and Knowledge-Base Systems*, Ch. 7.3 (chase).
- Maier, *The Theory of Relational Databases*, Ch. 6.
- Bernstein, P., "Synthesizing Third Normal Form Relations", TODS 1976.

## 18. Cheat Sheet
- Lossless: R = π_R1(R) ⋈ … ⋈ π_Rk(R).
- Binary test: split on shared X is lossless iff X→Y or X→Z ∈ F⁺.
- Chase: tableau + FD merges; all-distinguished row ⇒ lossless.
- Preservation: union of projected FDs implies F (test via closure with per-table FDs).
- BCNF may lose deps (AB→C); 3NF synthesis never does.
- FK ≠ lossless. DISTINCT ≠ fix.
- After any decomposition: check BOTH properties.
- Vertical partition: shared key in both parts ⇒ safe.

## 19. Quiz
1. Lossless means: a) no NULLs b) R = join of projections c) no FKs d) 1NF → **b**
2. Split R1(X,Y),R2(X,Z) lossless iff: a) X→Y or X→Z b) Y→X c) XY→Z d) always → **a**
3. Dependency preservation requires: a) no lost FDs b) no lost rows c) no MVDs d) BCNF → **a**
4. {AB},{BC} split of R(A,B,C), F={AB→C}: a) lossless b) lossy c) preserving d) BCNF → **b**
5. FK constraints guarantee: a) losslessness b) referential integrity only c) preservation d) 3NF → **b**
6. The classic lost dependency (AB→C, C→A): a) C→A b) AB→C c) both d) neither → **b**
7. The chase tests: a) only FDs b) losslessness c) only MVDs d) only keys → **b**
8. 3NF synthesis is always: a) BCNF b) lossless + preserving c) 4NF d) denormalized → **b**
9. A split with no shared attributes is: a) always lossless b) always lossy unless R is the product c) preserving d) BCNF → **b**
10. Vertical partition safety rule: a) shared key in both b) shared key in one c) no key d) any split → **b** (shared key is a key in at least one part — for a two-part split with identical shared keys both hold)

## 20. Flashcards
- **Q: Lossless-join definition?** → **A:** R = π_R1 ⋈ … ⋈ π_Rk (exact round-trip).
- **Q: Binary lossless test?** → **A:** Shared X must be a key of one side (X→Y or X→Z).
- **Q: Dependency preservation?** → **A:** Projected FDs imply all original FDs.
- **Q: What is the chase?** → **A:** Tableau + FD merges; distinguished row ⇒ lossless.
- **Q: Can BCNF lose dependencies?** → **A:** Yes (AB→C); 3NF synthesis never does.
- **Q: Does FK = lossless?** → **A:** No — referential integrity only.
- **Q: Checks after any decomposition?** → **A:** Lossless join AND dependency preservation.
- **Q: Safe vertical partition?** → **A:** Shared key in at least one (ideally both) parts.

## 21. Revision
After any decomposition verify **two** properties. **Lossless-join**: R = π_R1 ⋈ … ⋈ π_Rk; binary split on shared X is lossless iff **X→Y or X→Z ∈ F⁺** (shared set is a key of one side). Tested via closure or the **chase** (tableau, apply FDs by merging; a fully-distinguished row ⇒ lossless). **Dependency preservation**: union of FDs projected onto the pieces implies F — check each X→Y by closing X with only per-table FDs; Y inside ⇒ preserved. The AB→C/C→A example: split {AC},{BC} is lossless (C→A) but **loses AB→C** — the canonical "lossless but not preserving" and the reason BCNF yields to 3NF. Remember **FK ≠ lossless** and **DISTINCT ≠ fix**. Production: 3NF synthesis gives both for free; BCNF may not; vertical partitioning is safe when the shared key pins a side.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a lossless decomposition?" | 7 / 13 Q1 |
| "Binary lossless test?" | 13 Q2 |
| "Is {AC},{BC} lossless & preserving?" | 8 / 13 Q4 |
| "Why isn't an FK enough?" | 13 Q6 |
| "What is the chase?" | 13 Q7 |
| "Can BCNF lose dependencies?" | 13 Q8 |
| "What to check after a decomposition?" | 13 Q17 |
| "Vertical partition safely?" | 13 Q16 / 15 |
