# Fourth Normal Form (4NF) and Fifth Normal Form (5NF)

> **TL;DR**: 4NF and 5NF go beyond functional dependencies. 4NF removes redundancy from **multi-valued dependencies (MVDs)** — independent multi-valued facts (a person's skills × languages) that cause row multiplication. 5NF removes redundancy from **join dependencies (JDs)** — facts recoverable only by joining three or more relations. In practice both are rare: 3NF/BCNF handle virtually all real schemas.

## 1. Why Does This Exist?
BCNF is the FD-based ceiling, but some redundancy isn't visible to functional dependencies at all. Take `PERSON(name, skill, language)`: name determines *a set* of skills and *a set* of languages, independently. The FD `name → skill` doesn't hold (one name, many skills) — yet storing all pairs creates the Cartesian-product redundancy: Alice's 3 skills × 2 languages = 6 rows, each skill repeated with each language. If Alice learns a 3rd language, 3 new rows. That's an **MVD** (multi-valued dependency), and only **4NF** sees it. **5NF** then handles *join dependencies*: when a fact can only be reassembled by joining three tables (the classic suppliers-parts-projects ternary), even 4NF can't split without either losing data or duplicating it. Both forms complete normalization theory — elegant, exam-relevant, and deliberately rare in production.

## 2. How Does It Work?
**MVD (exact)**: X ↠ Y holds in R iff, for any two tuples agreeing on X, their Y values can be swapped to produce tuples still in R. Equivalently: Y depends on X, *independently* of Z = R − (X ∪ Y). So X ↠ Y means "the set of Y-values associated with each X-value is independent of Z."
**4NF (exact)**: R is in 4NF iff for every non-trivial MVD X ↠ Y (with X∪Y ⊂ R), X is a superkey. Every FD X→Y is also an MVD X↠Y, so BCNF ⊂ 4NF.
**Fix**: decompose R into R1(X∪Y) and R2(X∪Z) — remove the cross-product.
**JD (exact)**: R satisfies a join dependency ⋈{R1, R2, ..., Rn} iff R equals the natural join of those projections. A JD is trivial if one Ri = R.
**5NF (exact)**: R is in 5NF iff every non-trivial JD ⋈{R1,...,Rn} is implied by candidate keys (each Ri's attributes include a candidate key of R). 5NF = "no non-trivial JD at all" (every non-trivial JD must be key-implied).
**Fix**: split R into the JD's projections; each is 5NF.

## 3. When Is It Used?
- **Interviews/exams**: "explain 4NF and 5NF" and "give an MVD example" (person-name-skills-languages) are the standard questions — 4NF is a Top-15 normalization question.
- **When a BCNF schema still grows rows**: if a relation's row count multiplies even though FDs are fine, suspect an MVD → 4NF.
- **Ternary fact schemas** (supplier–part–project): JD discussions belong to 5NF.
- **Production**: almost never needed — real schemas rarely have non-key-implied MVDs/JDs. You should know *when* to invoke them and when to say "3NF is enough."
- **Data warehouses**: array/list attributes (JSON) deliberately skip 4NF for practicality — good interview contrast.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: model skills and languages as separate 1:N tables.** *Chosen in practice* — that's exactly what 4NF decomposition produces (PERSON_SKILL, PERSON_LANG), and it's what ORMs do. 4NF just formalizes it.
- **Alternative: keep the Cartesian table and dedupe with DISTINCT.** Rejected — the redundancy persists at write time; updates multiply rows.
- **Alternative: stop at BCNF.** Rejected for correctness — BCNF genuinely can't see MVDs; the redundancy is invisible to FDs, so BCNF alone is provably insufficient.
- **For 5NF: alternative, just merge to one wide table.** Rejected — that reintroduces redundancy when the pieces vary independently; the JD formalism states exactly when the join is safe.
- **Why so rare?** Because MVDs in real data are usually "real" N:M associations that designers split by instinct — 4NF/5NF codify the instinct.

## 5. Intuition
- **4NF**: think of **two phone books** a person belongs to — skills and languages. If I ask for "Alice's skills and languages," listing them side-by-side forces a cross-product (every skill paired with every language). The truth is two *independent lists*. 4NF says: a table must not merge two independent multi-valued facts; each fact gets its own table keyed by the shared X. **Redundancy by multiplication** is the smell.
- **5NF**: imagine **suppliers, parts, projects**: a supplier may supply part P to project J, but not every combination is valid — it's a true 3-way fact that *can't* be split into binary tables without losing or inventing rows. 5NF says: if the truth is genuinely n-ary, keep (or re-form) the n-ary relation; only split when the JD holds. **"Can this be losslessly reassembled only at three tables?"** is the smell.

## 6. Real-World Analogy
- **4NF = a whiteboard that asks "how many lists am I storing in one column pair?"** A teacher writes each student's name with *all* their club memberships and *all* their sport teams in one grid. Skills (clubs) and sports are independent: the grid lists every club×sport pair. The fix is two columns/keyed lists per student — each list independent. 4NF is the "one row pair per independent fact" discipline.
- **5NF = a shared calendar spanning three teams.** An event needs organizer + room + speaker; no pair alone determines the third, and the true combination only exists when all three meet. If you split the event into three pair-tables and rejoin, you may produce combinations that never existed. 5NF is the rule that says "some facts are genuinely three-way — keep the triple."

## 7. Formal Definition
(Elmasri & Navathe Ch. 15; Silberschatz Ch. 8.5–8.6; Fagin 1977, 1979.)
- **MVD**: X ↠ Y holds iff given tuples t1,t2 with t1[X]=t2[X], the tuples t3 (t1[X], t1[Y], t2[Z]) and t4 (t2[X], t2[Y], t1[Z]) are in R, where Z = R−(X∪Y). Symmetry of X↠Y and X↠Z.
- **Trivial MVD**: X∪Y = R (then Z = ∅, always holds).
- **4NF**: for every non-trivial MVD X↠Y, X is a superkey. Since X→Y ⇒ X↠Y, 4NF ⇒ BCNF.
- **Join dependency**: R ⊨ ⋈{R1,…,Rn} iff R = π_R1(R) ⋈ … ⋈ π_Rn(R).
- **Trivial JD**: some Ri = R.
- **5NF (Project-Join NF)**: every non-trivial JD ⋈{R1,…,Rn} is implied by the candidate keys (each Ri contains a candidate key of R). No non-trivial JD can exist that isn't key-implied.

## 8. Example
**4NF** — `PERSON(name, skill, language)`:
```
('Alice','SQL','English')
('Alice','SQL','Hindi')
('Alice','Python','English')
('Alice','Python','Hindi')   -- 2 skills × 2 languages = 4 rows (Cartesian)
```
- FDs: none besides name→nothing (name is NOT a key; a name has many rows).
- BCNF? Trivially yes (no non-trivial FDs) — **yet redundancy persists** → MVD smell.
- MVD: `name ↠ skill` and `name ↠ language` hold (non-trivial: name∪skill ⊂ R). LHS `name` is not a superkey → **4NF violation**.
- **Fix**: `PERSON_SKILL(name, skill)` and `PERSON_LANGUAGE(name, language)` — 2 + 2 = 4 rows, no cross-product.

**5NF** — Suppliers(P), Parts(Pt), Projects(J): tuples (s1,p1,j1), (s1,p2,j1), (s1,p1,j2) but NOT (s1,p2,j2).
- Binary projections (SP, SJ, PJ) each hold; but rejoining **invents** (s1,p2,j2) — so the JD over the three projections does NOT hold.
- 4NF-fine (no MVD), yet the ternary fact is the true atomic unit → keep the 3-column relation, or split ONLY if the JD holds. That "should I split into binaries?" decision is 5NF.

## 9. Internal Working
**Detect MVD (4NF):**
1. For candidate X, test: for any two tuples sharing X, does swapping Y (keeping Z) stay in R? If yes for Y and for Z = R−(X∪Y) independently → X↠Y non-trivial MVD.
2. Check X⁺/superkey status. If X not a superkey → 4NF violation.
3. Decompose: R1(X∪Y), R2(X∪Z); repeat until no non-trivial MVD with non-superkey LHS.
4. Verify losslessness via the MVD property (X↠Y guarantees the split is lossless).
**Detect JD (5NF):**
1. Candidate decomposition: choose projections; test if R = join of projections (chase algorithm).
2. If a non-trivial JD holds and some projection lacks a candidate key → 5NF violation → split.
3. If no non-trivial JD holds → 5NF already.

## 10. Time Complexity
- **MVD test**: O(|R|²) tuple-pair scans for a candidate X; trivial at interview sizes.
- **JD test**: exponential in general (chase is PSPACE-hard in the abstract), but textbook examples are tiny.
- **Design/runtime cost**: none — 4NF/5NF are design-time properties.

## 11. Advantages
- **Complete normalization theory**: 4NF/5NF close the loop after BCNF; you can state "FDs→MVDs→JDs" with confidence.
- **No cross-product explosion**: 4NF kills row multiplication from independent multi-valued facts.
- **5NF = "atomic facts"**: guarantees no information is ever invented or lost by joins.
- **Strong interview signal**: knowing when (and when NOT) to use them shows real depth.
- **Formal justification** for the "split every N:M into a junction table" practice.

## 12. Disadvantages
- **Rare in production**: most real schemas never have non-key MVDs/JDs — applying them is over-engineering.
- **5NF's definition is subtle**: "JD implied by candidate keys" is harder to state than BCNF.
- **Testing is non-obvious**: MVD/JD detection requires tuple-swap/join tests, not closure.
- **Joins increase**: more relations, more join cost for rare benefits.
- **Overhead**: many engineers wrongly split ternary facts, *losing* valid combinations — 5NF warns against premature splitting.

## 13. Interview Questions
1. **Q: What is an MVD? Give an example.** A: X↠Y: Y's values vary independently of Z with X fixed. PERSON(name, skill, language): name↠skill, name↠language — skills and languages are independent lists.
2. **Q: Define 4NF.** A: R is in 4NF iff every non-trivial MVD X↠Y has X a superkey. Since FDs are MVDs, 4NF ⇒ BCNF.
3. **Q: Why is BCNF not enough here?** A: BCNF only sees FDs. PERSON(name,skill,language) has no non-trivial FDs (BCNF ✓) yet stores Cartesian-product redundancy from independent multi-valued facts — invisible to FDs, visible to MVDs.
4. **Q (scenario): Alice has 3 skills and 2 languages. How many rows in the naive table?** A: 6 — the cross product. Every new skill × every language. 4NF fixes by splitting into PERSON_SKILL (3) + PERSON_LANGUAGE (2) = 5 rows.
5. **Q: What's a trivial MVD?** A: X∪Y = R (Z empty) — always holds, ignored by 4NF's condition.
6. **Q: What is a join dependency?** A: R = π_R1(R) ⋈ … ⋈ π_Rn(R) — R is exactly recoverable from its projections' natural join.
7. **Q: Define 5NF.** A: Every non-trivial JD ⋈{R1,…,Rn} is implied by the candidate keys (each Ri contains a candidate key). No non-trivial JD that isn't key-implied.
8. **Q (classic): Suppliers–parts–projects — can we split into binaries?** A: Only if the JD holds. (s1,p1,j1),(s1,p2,j1),(s1,p1,j2) with no (s1,p2,j2): binary splits rejoin to invent (s1,p2,j2) → JD doesn't hold → keep the ternary relation.
9. **Q: 4NF vs 5NF?** A: 4NF kills MVD redundancy (independent multi-valued lists); 5NF kills JD redundancy (facts only recoverable by 3+ joins). 4NF ⇒ BCNF; 5NF ⇒ 4NF (5NF implies 4NF because an MVD is a binary JD).
10. **Q (tricky): Does 5NF imply 4NF?** A: Yes — a non-trivial MVD X↠Y is exactly a binary JD ⋈{XY, XZ}; if every non-trivial JD is key-implied (5NF), MVDs are covered too.
11. **Q: When would you actually use 4NF in production?** A: When you see an N:M×N:M table with row multiplication — e.g., user×skills×languages flattened in one table. Answer: split into two junction tables. 4NF names the rule you're applying.
12. **Q: Is a table with JSON arrays (skills, languages) in 4NF?** A: Not in the relational sense — arrays break 1NF and hide the MVD; Postgres JSON is a deliberate non-relational choice. If queried relationally, split the arrays into child tables (the 4NF decomposition).
13. **Q (hard): Prove every FD is an MVD.** A: If X→Y, fix two tuples sharing X: their Y agree, so swapping Y yields the same tuples, which exist in R. Hence X→Y ⇒ X↠Y — so BCNF relations trivially satisfy the "FD part" of 4NF.
14. **Q: What's the chase algorithm used for?** A: Testing whether a JD holds (or an FD is implied by a decomposition) — apply the projections' join constraints to a probe tuple until stable or contradiction.
15. **Q (scenario): Splitting a ternary fact caused wrong data. Why?** A: The JD didn't hold — binary projections reintroduced invalid combinations on join. 5NF's rule ("only split on key-implied JDs") exists precisely to prevent this.
16. **Q: How do 1NF–5NF map to FD/MVD/JD?** A: 1NF atomic values; 2NF/3NF/BCNF = functional dependencies; 4NF = multi-valued dependencies; 5NF = join dependencies. Each form handles the next dependency class.
17. **Q: Why don't production schemas target 5NF?** A: Real data's n-ary facts are rare; the join cost of ultra-split schemas exceeds the redundancy saved; and 3NF/BCNF remove the redundancy that actually occurs. 5NF is the theoretical ideal, 3NF the practical target.
18. **Q (tricky): R(A,B,C) with exactly the 8 possible tuples. 4NF? 5NF?** A: Full table = all combinations → every MVD/JD holds trivially but is key-implied? With all tuples, ABC is the only key-relevant relation; non-trivial MVDs with non-superkey LHS exist (A↠B, A not superkey) → not 4NF/5NF (still reducible to binary tables that rejoin to the full set).
19. **Q: What does a "lossless join" mean for 4NF splits?** A: The MVD X↠Y guarantees R1(X,Y) ⋈ R2(X,Z) = R exactly — no invented rows, no lost rows. That's why 4NF decompositions are always lossless.
20. **Q: Give the normalization answer to "how do I model many-to-many?"** A: 4NF thinking: split into two junction tables. "User has many skills and many languages" ⇒ USER_SKILL(user_id, skill), USER_LANGUAGE(user_id, language) — exactly the 4NF decomposition, stated in ORM terms.

## 14. Follow-Up Questions
1. **Q: What is the relationship between MVDs and N:M relationships?** A: An N:M relationship is a trivial-ish MVD (X↠Y with Z = key attributes). When two N:M facts coexist on the same X, the cross-product MVD problem appears — 4NF demands separate tables.
2. **Q: Can 5NF be violated while 4NF holds?** A: Yes — a genuine 3-way JD with no binary MVD: the ternary suppliers-parts-projects example satisfies 4NF but violates 5NF if it can't be split.
3. **Q: What does "JD implied by candidate keys" mean practically?** A: Splitting is only safe if each piece is determined by a key of the whole — i.e., no piece is an arbitrary recombination. If keys don't justify the split, the "fact" is genuinely n-ary.
4. **Q: How do FDs arise from MVDs?** A: If Z = ∅ (X∪Y = R) the MVD is trivial; if Z ≠ ∅ but the MVD happens to be an FD (Y single-valued per X), it's an FD — FDs are the single-valued special case.
5. **Q: Should I ever denormalize INTO a 4NF-violating table for performance?** A: Yes — e.g., analytics denormalization (Redshift/ClickHouse arrays) trades 4NF for scan speed. Know that you're deliberately storing a cross-product.

## 15. Coding Example
```sql
-- 4NF violation: flattening two independent lists
CREATE TABLE person (name TEXT, skill TEXT, language TEXT);  -- Cartesian rows

-- 4NF fix (the decomposition):
CREATE TABLE person_skill    (name TEXT, skill TEXT, PRIMARY KEY(name, skill));
CREATE TABLE person_language (name TEXT, language TEXT, PRIMARY KEY(name, language));
-- Alice 3 skills + 2 languages: 5 rows total, not 6; adding a language adds 1 row, not 3.

-- 5NF illustration: ternary fact, DON'T split into binaries when the JD fails
CREATE TABLE spj (
  supplier TEXT, part TEXT, project TEXT,
  PRIMARY KEY (supplier, part, project),
  UNIQUE (supplier, part),   -- caution: only add if these ARE valid binary facts
  UNIQUE (supplier, project),
  UNIQUE (part, project)
);
-- If (s1,p2,j2) must be impossible while the three pairings each exist,
-- a JD does NOT hold => keep SPJ as one 3-keyed relation (5NF-compatible).
```
```python
def is_mvd(table, x_idx, y_idx):      # table: list of tuples; z = rest
    from itertools import groupby
    z_idx = [i for i in range(len(table[0])) if i not in (x_idx, y_idx)]
    for x, grp in groupby(sorted(table, key=lambda t: t[x_idx]), lambda t: t[x_idx]):
        rows = list(grp)
        yvals = {r[y_idx] for r in rows}; zvals = {r[z_idx[0]] for r in rows}
        # swapping must stay in R for all pairs
        for y in yvals:
            for z in zvals:
                if not any(r[x_idx]==x[0] if False else r[x_idx]==x and r[y_idx]==y and r[z_idx[0]]==z for r in rows):
                    return False, (x,)
    return True, None   # MVD holds (if also non-trivial and X non-superkey => 4NF violation)
```

## 16. Industry Usage
- **The "does this need 4NF?" heuristic** appears in every schema-design review when an N:M table unexpectedly multiplies rows.
- **ORMs hide 4NF**: Rails `has_and_belongs_to_many` generates junction tables — engineers implement 4NF decomposition without naming it.
- **Analytics engines** (BigQuery, Snowflake) happily use arrays and nested types — a deliberate 4NF exception for scan performance; knowing the trade is a senior signal.
- **5NF is almost purely theoretical** in industry; its one real home is data-warehouse fact/dimension modeling where n-ary facts (order = customer × product × store) justify multi-key fact tables.
- **Interview expectation** (Amazon/Google/Meta): define MVD, give the skills×languages example, decompose it, and state when 5NF applies — plus the judgment that "production uses 3NF/BCNF and rarely beyond."

## 17. References
- Fagin, R., "Multivalued Dependencies and a New Normal Form for Relational Databases", TODS 1977 (4NF).
- Fagin, R., "Normal Forms and Relational Database Operators", SIGMOD 1979 (5NF/PJNF).
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 15.1–15.4.
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 8.5–8.6.
- Kent, W., "A Simple Guide to Five Normal Forms", CACM 1983.

## 18. Cheat Sheet
- MVD X↠Y: Y's values vary independently of Z (with X fixed).
- 4NF: every non-trivial MVD X↠Y has X a superkey. 4NF ⇒ BCNF.
- Fix MVD: split into R1(X,Y) + R2(X,Z). Always lossless.
- Smell: BCNF-fine table whose rows multiply (skills × languages).
- JD ⋈{R1..Rn}: R = join of its projections.
- 5NF: every non-trivial JD is implied by candidate keys.
- 5NF ⇒ 4NF (MVD = binary JD).
- Production: 3NF/BCNF target; 4NF for N:M×N:M; 5NF near-theoretical.
- FD → MVD → JD: the three dependency classes.

## 19. Quiz
1. MVD stands for: a) missing-value dependency b) multi-valued dependency c) minimal-value dependency d) many-vertical dependency → **b**
2. 4NF requires for every non-trivial MVD X↠Y: a) Y prime b) X superkey c) X prime d) Y superkey → **b**
3. PERSON(name,skill,language) with 3 skills & 2 langs has: a) 3 rows b) 5 rows c) 6 rows d) 2 rows → **c**
4. Every FD is: a) an MVD b) a JD c) neither d) both a and b → **d** (FD ⇒ MVD ⇒ binary JD)
5. 4NF decomposition of (name,skill,language): a) 3 tables b) 2 tables c) 1 table d) none → **b**
6. 5NF handles: a) FDs b) MVDs c) JDs d) NULLs → **c**
7. The (s1,p1,j1) family shows a JD that: a) holds b) fails c) is trivial d) is an FD → **b**
8. 5NF ⇒ 4NF? a) yes b) no c) only with BCNF d) only with 1NF → **a**
9. BCNF handles MVDs? a) yes b) no c) partly d) always → **b**
10. Production schema target is usually: a) 5NF b) 4NF c) 3NF/BCNF d) 1NF → **c**

## 20. Flashcards
- **Q: What is an MVD?** → **A:** X↠Y — Y varies independently of Z with X fixed (skills × languages).
- **Q: 4NF definition?** → **A:** Every non-trivial MVD X↠Y has X a superkey.
- **Q: Why is BCNF insufficient for MVDs?** → **A:** BCNF only sees FDs; MVD redundancy is invisible to FDs.
- **Q: 4NF fix?** → **A:** Split into R1(X,Y) and R2(X,Z).
- **Q: What is a JD?** → **A:** R = natural join of its projections.
- **Q: 5NF definition?** → **A:** Every non-trivial JD implied by candidate keys.
- **Q: Is 5NF used in production?** → **A:** Rarely — 3NF/BCNF dominate; 5NF is theoretical.
- **Q: Dependency ladder?** → **A:** FD (→2NF..BCNF), MVD (→4NF), JD (→5NF).

## 21. Revision
**MVD**: X↠Y — with X fixed, Y varies independently of Z; PERSON(name,skill,language) is the canonical example (no FDs, yet 3×2 Cartesian rows). **4NF**: every non-trivial MVD X↠Y has X a superkey ⇒ split into PERSON_SKILL(name,skill) + PERSON_LANGUAGE(name,language) (always lossless). **JD**: R = join of its projections; the suppliers–parts–projects ternary is the canonical test — binary splits rejoin to invent (s1,p2,j2), so the JD fails and you keep the ternary. **5NF**: every non-trivial JD is implied by candidate keys. Remember **FD ⇒ MVD ⇒ (binary) JD**, so 4NF ⇒ BCNF and 5NF ⇒ 4NF. Interview script: define MVD with the skills/languages table, decompose it for 4NF, then state 5NF's JD condition and the "production rarely needs past 3NF/BCNF" judgment. The three dependency classes close the normalization ladder.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is an MVD?" | 2 / 13 Q1 |
| "Define 4NF / when is BCNF not enough?" | 7 / 13 Q2–Q3 |
| "How many rows in skills×languages?" | 13 Q4 |
| "What is a JD / 5NF?" | 13 Q6–Q7 |
| "Can we split supplier-part-project?" | 8 / 13 Q8 |
| "5NF ⇒ 4NF?" | 13 Q10 |
| "When to use 4NF in production?" | 13 Q11 |
| "MVD in JSON/arrays?" | 13 Q12 |
