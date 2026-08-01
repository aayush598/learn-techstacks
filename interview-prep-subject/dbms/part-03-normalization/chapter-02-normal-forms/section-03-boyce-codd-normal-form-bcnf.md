# Boyce-Codd Normal Form (BCNF)

> **TL;DR**: R is in BCNF iff for every non-trivial FD X→Y, X is a superkey. No exceptions, no "Y is prime" relaxation. It's 3NF plus the removal of *every* redundancy-causing FD — even the ones into key components — at the price that a BCNF decomposition may occasionally lose a functional dependency.

## 1. Why Does This Exist?
3NF relaxes the rule ("Y may be prime") to guarantee dependency preservation — but that relaxation leaves real redundancy behind. In R(A, B, C) with {AB→C, C→A}, both A and C are prime (keys {AB}, {BC}); the FD `C→A` survives 3NF, yet C and A facts can repeat across rows. BCNF was formulated (Boyce & Codd, 1974) to close this gap: **every non-trivial FD must have a superkey LHS**, no exceptions. If a value determines something, that value must be a key. BCNF is the "nothing but the key" rule taken literally — Codd's 3NF was designed before the overlapping-key case was appreciated, and BCNF is the correction.

## 2. How Does It Work?
**Definition (exact)**: R is in BCNF iff for every non-trivial functional dependency X→Y ∈ F⁺, X is a superkey (X⁺ = R).
**Test procedure**: 1) for each non-trivial FD X→Y, compute X⁺; 2) if X⁺ ≠ R → violation. That's it — no prime/transitive analysis needed.
**Violation class**: any FD whose LHS is not a superkey, including `C→A` where C is prime. The "Y is prime" escape hatch of 3NF is gone.
**Fix (decomposition algorithm)**: for each violating FD X→Y, split R into R1(X, Y) (key X) and R2(R − Y, X) — placing X in both relations as the join/FK attribute. Repeat on R2 until every relation is BCNF.
**Caution**: unlike 3NF, the resulting BCNF decomposition can *lose* dependencies (an FD whose attributes straddle the split) — always run the projection test.

## 3. When Is It Used?
- **"Is this BCNF?"** — a top-10 normalization interview question, always with the AB→C / C→A trap.
- **Schema review**: the strictest FD-based standard; used when 3NF's residual key redundancy is unacceptable (rare but real — e.g., overlapping candidate keys in entity-attribute schemas).
- **When dependency preservation isn't needed**: if the lost FD is never enforced in the app, BCNF is clean.
- **Textbook normalization**: exam problems often ask "decompose to BCNF" — you must show the split and the lossless test.
- **Not** the default for most production OLTP — 3NF is. BCNF is the "ideal," invoked when you can get it without sacrifice.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: 3NF.** Rejected for "true" normalization because its prime-attribute relaxation leaves overlapping-key redundancy (the R(A,B,C) case). BCNF is the definition without that compromise.
- **Alternative: keep the violating FD and ignore it.** Rejected — that's exactly the redundancy being paid for.
- **Alternative: stay with 3NF when the BCNF split loses a dependency.** *Chosen in practice* — losing a rule is worse than residual redundancy, so engineers fall back to 3NF (this is the honest trade: BCNF = purity, 3NF = preservation).
- **Alternative: 4NF/5NF.** Those handle *non-functional* dependencies (MVDs/JDs) — BCNF is the FD-based ceiling, not a replacement for them.

## 5. Intuition
3NF said: "every FD with a superkey LHS — plus a polite exception for FDs into keys." BCNF says: **no exceptions**. If a column set determines anything, it must be the whole row. The AB→C / C→A example is the skeleton key: C determines A but C isn't a key, and it survives 3NF only because A happens to be prime. BCNF's intuition: **every arrow must start from a key**. An FD from a non-key is a statement "this column owns these facts" — and if it owns facts, it should be its own table (or part of a key). You can spot BCNF violations just by asking: "does any non-key-looking column determine other columns?" If yes, split.

## 6. Real-World Analogy
A **school timetable printed on a class card**: the card is keyed by (class_id, room) and each card lists the teacher. Rule: class_id → teacher (each class has one teacher). So the card (class_id, room, teacher) has `class_id → teacher` — a non-superkey FD (class_id alone doesn't identify the card, since the same class has multiple rooms). Under 3NF, teacher is "prime-adjacent" and the rule slips through; under BCNF it's flagged: teacher is determined by class_id, not by the card's full key — so teacher must live on a class_id-keyed card instead. BCNF is the auditor who says: "whoever owns a fact must own the row."

## 7. Formal Definition
(Boyce & Codd 1974; Elmasri & Navathe Ch. 14; Silberschatz Ch. 8.)
- **BCNF**: R is in BCNF iff for every non-trivial functional dependency X→Y in F⁺, X is a superkey (i.e., X⁺ = R).
- Equivalently: the only non-trivial FDs allowed are those with a superkey on the left.
- BCNF ⇒ 3NF. A 3NF relation may fail BCNF only via FDs whose RHS is entirely prime.
- The BCNF decomposition algorithm: repeatedly, for a violating FD X→Y, replace R with R1(X∪Y) and R2(R−Y). Result is lossless; may not preserve dependencies.

## 8. Example
`R(A, B, C)`, F = {AB→C, C→A}.
- Candidate keys: {AB}⁺ = {A,B,C}; {BC}⁺ = {B,C,A}. Keys {AB}, {BC}.
- **3NF?** C→A: C⁺={C,A}≠R, A prime → passes 3NF.
- **BCNF?** C→A: C⁺={C,A}≠R, non-trivial, LHS not superkey → **BCNF violation**. BCNF is stricter.
- **Decompose on C→A**: R1 = (C, A) key {C}; R2 = (B, C) — original minus Y={A}, plus X={C} → (B,C). Keys: R1 {C}; R2 {B,C}. Both BCNF ✓. Lossless (join on C). **Dependency preserved?** AB→C: AB appears in neither R1 nor R2 → **lost**. This is exactly why BCNF isn't always dependency-preserving.
- **Takeaway**: you can reach BCNF here, but you pay with the AB→C rule — hence the real-world preference for 3NF in this case.

## 9. Internal Working
1. **Compute closure** for each FD's LHS (Section 02 algorithm).
2. **BCNF test**: flag every non-trivial FD with X⁺ ≠ R.
3. **Decompose** the first violating FD X→Y: R1 = (X ∪ Y) [key X]; R2 = (R − Y) ∪ X [carry X as FK].
4. **Repeat** on R2 (and R1 if needed) until no violations remain.
5. **Verify**:
   - Lossless: join R1 ⋈ R2 on X reproduces R (guaranteed by the algorithm's construction).
   - Dependency-preserving: project F onto each Ri; if some FD's attributes are split across relations → lost. (BCNF: may fail.)
6. **Decision**: if a lost FD matters, backtrack to the 3NF decomposition (or keep R in 3NF).
7. **Alternative check**: use the "prime attribute" analysis — a BCNF violation is any non-trivial FD X→Y with X not a superkey, even when Y ⊆ prime.

## 10. Time Complexity
- **BCNF test**: O(#FDs × closure), same as 3NF — trivial.
- **BCNF decomposition**: worst case exponential in |R| (number of possible splits), but interviews use 2–4 attribute examples.
- **Runtime cost**: none — BCNF is design-time.

## 11. Advantages
- **Zero FD-based redundancy** — the strongest FD normal form; no overlapping-key residue.
- **No anomalies from any non-superkey FD** — update/insert/delete safe to the fullest FD extent.
- **Simple, absolute rule**: "every non-trivial arrow comes from a superkey" — easier to state than 3NF.
- **Cleanest relational algebra semantics**; a classic proof that the DB is honestly keyed.
- **The intellectual answer** to "why do we still have redundancy after 3NF?"

## 12. Disadvantages
- **May lose functional dependencies** during decomposition (the AB→C case) — the defining cost vs 3NF.
- **Overlapping-key pathologies are rare** in real schemas, so BCNF rarely pays off.
- **Forces more relations, more joins** when applied strictly.
- **3NF + safety is usually "good enough"**; BCNF purism can over-engineer a schema.
- **Designing direct-to-BCNF by hand is error-prone** — the "carry X into R2" step is easy to mis-split.

## 13. Interview Questions
1. **Q: Define BCNF.** A: R is in BCNF iff every non-trivial FD X→Y has X a superkey. No exceptions.
2. **Q: What's the difference between BCNF and 3NF?** A: 3NF allows FDs with non-superkey LHS when the RHS is prime; BCNF requires superkey LHS always. BCNF ⊂ 3NF.
3. **Q: Give the classic 3NF-but-not-BCNF relation.** A: R(A,B,C), F={AB→C, C→A}. Keys {AB},{BC}; C→A violates BCNF (C not superkey) but not 3NF (A is prime).
4. **Q: Can BCNF lose dependencies?** A: Yes. R(A,B,C),{AB→C,C→A}: decomposing on C→A loses AB→C. 3NF's synthesis never loses dependencies; BCNF can.
5. **Q: Is every BCNF relation also 3NF?** A: Yes — BCNF's condition is strictly stronger.
6. **Q (tricky): R(A,B,C), F={A→B, B→C}. BCNF?** A: Keys: {A} (A⁺=ABC). A→B ✓ superkey. B→C: B⁺={B,C}≠R → **not BCNF**. Decompose B→C: R1(B,C) key {B}, R2(A,B) key {A}. Both BCNF, lossless, dependency-preserving here.
7. **Q (scenario): Your BCNF decomposition lost AB→C. Fix?** A: Either enforce the FD in the app (check both rows), or — as production does — fall back to the 3NF decomposition that keeps it. Trade redundancy vs rule enforcement.
8. **Q: Why does 3NF exist if BCNF is "better"?** A: Because BCNF can destroy dependency preservation — a database without its rules is worse than one with mild redundancy. 3NF is the sweet spot that keeps both.
9. **Q: How do you test for BCNF efficiently?** A: For each non-trivial FD X→Y compute X⁺; if X⁺ ≠ R → violation. (F⁺ matters, not just F — a superkey by implication counts.)
10. **Q (production): When is BCNF genuinely chosen in production?** A: When the schema is data-modeling-like with overlapping candidate keys and the "lost" FDs are logically implied or enforced in code — e.g., entity-attribute-value redesigns. Rare; 3NF dominates.
11. **Q (tricky): R(A,B,C,D), F={A→B, BC→D}. BCNF?** A: Key: {A,C} (A→B; C with A: AC⁺=ABCD). FDs: A→B: A⁺={A,B}≠R → violation. BC→D: BC⁺={B,C,D}≠R → violation. Not BCNF (not even 2NF? A→B is partial). Decompose both for BCNF.
12. **Q: How do you know a decomposition is lossless?** A: If R is split into R1(X,Y), R2(X,Z) sharing attribute set X and the FD X→(rest) holds appropriately, then R1 ⋈ R2 = R. Chase/test by joining projected tables and comparing to the original.
13. **Q: What does "dependency-preserving" mean?** A: Every FD in F holds in the projected relations (F can be implied by the union of the projections). Lost = some original rule can't be enforced locally in any decomposed table.
14. **Q (scenario): Redundancy persists after 3NF. Why?** A: Overlapping candidate keys — prime attributes involved in non-superkey FDs (C→A). BCNF is the fix.
15. **Q (hard): Give a relation in BCNF where a small redundancy still exists.** A: Not possible via FDs — BCNF is FD-redundancy-free by definition. Residual redundancy (if any) must come from MVDs/JDs → 4NF/5NF territory.
16. **Q: What's the relationship between BCNF and "every arrow from a key"?** A: That IS BCNF. The phrase is the exact plain-language statement: every non-trivial FD must start at a superkey.
17. **Q (tricky): R(A,B,C), F={A→C, C→A} plus B independent. BCNF?** A: Keys: {A,B}, {B,C}. FDs: A→C: A⁺={A,C}≠R → violation (A not superkey in R; {A,B} is). Not BCNF. Decompose R1(A,C), R2(A,B) — both BCNF, lossless, preserved.
18. **Q: Why is BCNF called "Codd's correction"?** A: Codd defined 3NF (1971) with the prime-attribute clause; Boyce and Codd (1974) noticed overlapping-key FDs slipped through, so formulated BCNF with no clause.
19. **Q (production): Should the ORM layer care about BCNF?** A: Indirectly — ORMs map 3NF-ish models to tables; BCNF pathologies (overlapping natural keys) surface as duplicate-valid checks or unique constraints the ORM must encode since the FD is lost.
20. **Q: Full normalization ladder by FD only?** A: 1NF (atomic) → 2NF (no partial) → 3NF (no transitive) → BCNF (every arrow from a key). Beyond that you need MVDs (4NF) and JDs (5NF) — not FD-based.

## 14. Follow-Up Questions
1. **Q: When is a BCNF decomposition guaranteed dependency-preserving?** A: When no FD's attributes straddle the split — e.g., decomposing on FDs whose attributes are fully contained in one output relation. The C→A split straddles AB→C, hence the loss.
2. **Q: Can the BCNF algorithm be modified to preserve dependencies?** A: Not in general (it's provably impossible to always get both). The standard fix is: do 3NF synthesis and accept mild redundancy, or enforce the lost FD in the app.
3. **Q: BCNF vs 4NF — what's left after BCNF?** A: Multi-valued dependencies: independent multi-valued facts (skills × languages) are invisible to FDs, so BCNF doesn't catch them; 4NF does.
4. **Q: How do overlapping keys arise in practice?** A: Entity-attribute-value tables, synonyms, natural keys — e.g., R(ssn, email, name) with ssn↔email both keys.
5. **Q: Is BCNF the same as "no redundancy at all"?** A: No — only FD-based redundancy. Cross-tuple duplication from MVDs/JDs (4NF/5NF) or intentional denormalization (performance) remains.

## 15. Coding Example
```sql
-- R(A,B,C) = books(book_id, author_id, author_name)? No—that's a transitive 3NF fix.
-- BCNF pathology: R(A,B,C) as (teacher_id, course_id, dept_id) with F={teacher_id→dept_id, (teacher_id,course_id)→?}
-- Concrete: EXAM(date, room, instructor) with date→instructor not allowed by BCNF.
-- Instead: the classic C→A as SQL unique constraints:
CREATE TABLE r_abc (
  a TEXT, b TEXT, c TEXT,
  PRIMARY KEY (a, b), PRIMARY KEY (b, c)  -- (illustrative: two keys overlap)
);
-- BCNF test on F={AB→C, C→A}: C→A (C not a key) => split:
CREATE TABLE r1_ca (c TEXT PRIMARY KEY, a TEXT);
CREATE TABLE r2_bc (b TEXT, c TEXT REFERENCES r1_ca(c), PRIMARY KEY (b, c));
-- AB→C is LOST in the split; enforce app-side:
-- INSERT INTO r2_bc ... requires: EXISTS(SELECT 1 FROM r1_ca JOIN ... checking AB→C)
```
```python
def decompose_bcnf(attrs, fds):
    out = [set(attrs)]
    for rel in list(out):
        for x, y in fds:
            if not y <= x and closure(x, fds) != rel:
                # violate: split rel on X->Y
                out.remove(rel)
                out.append(set(x) | set(y))          # R1(X,Y), key X
                out.append(rel - set(y) | set(x))    # R2((R-Y)+X)
                break
    return [''.join(sorted(r)) for r in out]   # ['AC','BC'] for AB→C,C→A
```

## 16. Industry Usage
- **The textbook standard** every database exam and interview ladder references; knowing "when BCNF and when 3NF" is a marker of senior schema skill.
- **Rare-but-real production use**: overlapping-key schemas (EAV designs, mapping tables with two natural keys) where 3NF's residual redundancy actually bites at scale.
- **Postgres/MySQL enforcement**: when an FD can't be preserved, production encodes it with `UNIQUE` constraints + triggers or app-level checks — that's "living with a BCNF loss."
- **Schema normalization audits**: data-modeling teams run BCNF as the FD ceiling; anything past it (4NF/5NF) is almost never applied in production.
- **Interview batteries** (Amazon, Google, Meta, Microsoft) test BCNF via the AB→C/C→A trap and the "decompose to BCNF" drill — it's one of the most-repeated normalization questions.

## 17. References
- Codd, E. F., "Further Normalization of the Data Base Relational Model", 1971 (3NF).
- Boyce, R. F. & Codd, E. F., "Applying Relational Algebra to Database Design" (IBM, 1974) — BCNF.
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14 (BCNF; decomposition algorithm).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 8.4.2.
- Kent, W., "A Simple Guide to Five Normal Forms", CACM 1983.

## 18. Cheat Sheet
- BCNF: every non-trivial FD X→Y has X a superkey. No clauses.
- BCNF ⇒ 3NF; the only gap = FDs with prime RHS (overlapping keys).
- Classic violation: R(A,B,C), {AB→C, C→A} — C→A, C not a key.
- Decompose on X→Y: R1(X,Y) + R2((R−Y)∪X); repeat.
- BCNF decomposition is always lossless but may lose dependencies.
- Lost AB→C ⇒ fall back to 3NF or enforce the rule in the app.
- FDs only: 1NF → 2NF → 3NF → BCNF. MVDs/JDs next.

## 19. Quiz
1. BCNF requires for every non-trivial FD X→Y: a) X prime b) X superkey c) Y prime d) X=Y → **b**
2. R(A,B,C), {AB→C,C→A}: a) BCNF b) 3NF not BCNF c) 2NF d) 1NF → **b**
3. BCNF decomposition is always: a) dependency-preserving b) lossless c) 4NF d) trivial → **b**
4. The lost FD in R(A,B,C),{AB→C,C→A} split is: a) C→A b) AB→C c) both d) neither → **b**
5. Every BCNF relation is: a) 3NF b) 4NF c) 2NF only d) none → **a**
6. BCNF's "prime relaxation" is: a) same as 3NF b) none — no relaxation c) for MVDs d) for NULLs → **b**
7. R(A,B,C), F={A→B, B→C} key {A}: a) BCNF b) 3NF not BCNF c) not 3NF d) 1NF → **c** (transitive B→C)
8. BCNF removes redundancy from: a) prime attrs b) non-prime c) both a and b d) keys only → **c**
9. What survives BCNF but not 4NF? a) transitive deps b) partial deps c) MVDs d) NULLs → **c**
10. When production keeps 3NF over BCNF: a) speed b) dependency preservation c) disk d) style → **b**

## 20. Flashcards
- **Q: BCNF definition?** → **A:** Every non-trivial FD X→Y has X a superkey.
- **Q: 3NF vs BCNF?** → **A:** 3NF allows Y-prime FDs; BCNF doesn't. BCNF ⊂ 3NF.
- **Q: Classic BCNF violation?** → **A:** R(A,B,C), {AB→C, C→A} — C→A, C not a key.
- **Q: BCNF decomposition guarantee?** → **A:** Always lossless; may lose dependencies.
- **Q: BCNF decomposing on X→Y?** → **A:** R1(X,Y) + R2((R−Y)∪X).
- **Q: What if a dependency is lost?** → **A:** Fall back to 3NF or enforce in the app.
- **Q: FD ladder?** → **A:** 1NF → 2NF → 3NF → BCNF (FDs stop here; MVDs need 4NF).
- **Q: Redundancy left after BCNF?** → **A:** Only from MVDs/JDs or intentional denormalization.

## 21. Revision
BCNF is **3NF with no exceptions**: every non-trivial FD X→Y must have X a superkey. The entire BCNF-vs-3NF gap is captured by one relation — R(A,B,C), {AB→C, C→A} — where C→A (C not a key) violates BCNF but survives 3NF because A is prime (overlapping keys {AB},{BC}). **Decompose** on the violating X→Y: R1 = (X∪Y), R2 = ((R−Y)∪X), repeat. Guaranteed **lossless**, but **may lose dependencies** — here AB→C is lost. That's the real trade: **BCNF = purity, 3NF = dependency preservation**, and production overwhelmingly picks 3NF. Interview script: state the no-exceptions rule → give the classic AB→C/C→A counterexample → decompose and show the lost FD → explain why 3NF wins in practice. Past BCNF, only MVDs (4NF) and JDs (5NF) matter — FDs can't go further.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Define BCNF / 3NF vs BCNF?" | 7 / 13 Q1–Q2 |
| "Classic 3NF-not-BCNF example?" | 13 Q3 |
| "Can BCNF lose dependencies?" | 13 Q4 |
| "Decompose R(A,B,C),{AB→C,C→A} to BCNF?" | 8 / 13 Q3 |
| "Why keep 3NF instead of BCNF?" | 13 Q8, Q10 |
| "BCNF test procedure?" | 9 / 13 Q9 |
| "Redundancy after BCNF?" | 13 Q15 |
| "Why is BCNF 'Codd's correction'?" | 13 Q18 |
