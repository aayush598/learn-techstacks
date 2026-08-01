# Functional Dependencies in Depth

> **TL;DR**: An FD X→Y states that each value of X determines exactly one value of Y (functionality), capturing an *invariant of the mini-world* — and every normal form is defined by forbidding certain FDs.

## 1. Why Does This Exist?
Normalization exists because some FDs create redundancy — and you can't discuss redundancy without first naming the *cause*: functional dependencies. An FD X→Y exists to capture a real-world invariant: "employee number determines name", "social security number determines address". It matters because these invariants *are* the schema's logic: if `emp_id → dept`, then dept is a fact about the employee, not about the row — and storing it per-row risks duplication. FDs exist as the formal vocabulary for (a) finding candidate keys, (b) judging normal forms (every form = a constraint on FDs), and (c) designing decompositions that don't lose rules. Without FDs, schema design is vibes; with them, it's a theorem.

## 2. How Does It Work?
Given relation R and attribute sets X, Y: **X → Y** (X determines Y) holds iff for every legal instance, any two tuples that agree on all attributes of X also agree on all attributes of Y. Practically: pick X, check that no two rows share X-values but differ in any Y-value. Types: **trivial** if Y ⊆ X (always true); **non-trivial** otherwise; **fully non-trivial** if X ∩ Y = ∅. An FD set F is the collection of invariants that must always hold. From F we can (a) find keys (X is a key if X⁺ = all attributes and minimal), (b) test normal forms, and (c) reason with Armstrong's axioms (Section 02).

## 3. When Is It Used?
- **Key discovery**: candidate keys are found via closure over FDs — the entry point of every normalization problem.
- **Normal-form testing**: 2NF/3NF/BCNF are defined as constraints on which FDs exist (partial, transitive, non-superkey LHS).
- **Schema repair**: "why is this data duplicated?" → find the bad FD → decompose to remove it.
- **Decomposition design**: choose which relations to split into by looking at FD clusters.
- **Interview screens**: "given these FDs, is R in 3NF? find the candidate keys" — the standard normalization question shape.
- **DB design tools**: normalizing from requirements = deciding FDs from the business rules.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: "design by intuition" (just split tables when it feels right).** Rejected: intuition doesn't guarantee redundancy is gone or rules preserved; FDs give *testable* criteria — you can prove a design correct.
- **Alternative: rely only on sample data to infer FDs.** Rejected: absence of a violation in today's rows doesn't prove an invariant — FDs are *semantic* constraints from the mini-world (a bank's "one account number → one customer" holds even if no dup exists yet). Data confirms; semantics dictate.
- **Alternative: formal logic (first-order) for every constraint.** Rejected: too heavy; FDs are the *minimum useful fragment* — expressive enough for normalization, simple enough for humans.
- **Why "functional"?** Because it's literally a function: X → Y means Y is a *function of* X — same input, same output. That functionality is the redundancy trigger: if Y is a function of X and X isn't a key, Y repeats.

## 5. Intuition
An FD is a **rule of the world being modeled**: "each student number has exactly one name." Think of X as the *input* and Y as the *determined output* — like a dictionary where the key (word) determines the definition. If two dictionary entries have the same word but different definitions, the dictionary is broken. If your table has two rows with the same `emp_id` but different `dept`, then `emp_id → dept` is violated and your data is lying. The whole point: FDs tell you *what belongs together* — a dept is a property of an employee (determined by emp_id), so it should be stored with the employee, once, not repeated per paycheck.

## 6. Real-World Analogy
The **passport office**: passport number → (name, nationality, photo) — one passport number, one identity. Social security number → name. Now imagine a *file* listing each flight a person took, and each line also repeats their name and passport number. The name is a *function of* the passport number — the FD `passport → name` holds — but because the file stores per-flight rows, the name gets duplicated on every flight. The FD reveals the redundancy: name belongs to the person record, not the flight record. FDs are how you notice "this fact is being repeated because it's determined by the wrong key."

## 7. Formal Definition
Let R be a relation schema and X, Y ⊆ R. **X → Y** holds in R if for every legal instance r of R, for all tuples t₁, t₂ ∈ r: t₁[X] = t₂[X] ⟹ t₁[Y] = t₂[Y]. (X's values *functionally determine* Y's values.) An FD is **trivial** if Y ⊆ X, and **non-trivial** otherwise. A **set of FDs F** is the set of invariants required by the mini-world. The FD is the foundation of: keys (K is a superkey iff K → all attributes; candidate key = minimal such K), normal forms (defined by forbidden FD shapes), and decomposition (FDs must be preserved). (Armstrong 1974; Elmasri & Navathe Ch. 14; Silberschatz Ch. 8.)

## 8. Example
Relation `ENROLL(sid, cname, teacher)` with the mini-world rule "a course has exactly one teacher":
```
(1, 'DB', 'ProfA')
(2, 'DB', 'ProfA')
(1, 'OS', 'ProfB')
```
- Does `cname → teacher` hold? Check: every 'DB' row has teacher 'ProfA' → YES (in the sample). Is it a *real* FD? Yes — the rule says one teacher per course.
- Does `sid → teacher` hold? sid=1 has both ProfA and ProfB → NO (sample proves it can't hold).
- Is `cname → teacher` trivial? No (teacher ∉ {cname}). Non-trivial → subject to normalization rules.
- Keys: is {sid, cname} a candidate key? `{sid,cname}⁺ = {sid,cname,teacher}` = all → superkey. Minimal? Remove sid → `{cname}⁺ = {cname, teacher}` ≠ all (no sid) → still need sid. So {sid,cname} is a candidate key.
- The catch: `cname → teacher` has LHS not a superkey → this relation is NOT in BCNF (Part 03 §03 shows the fix: split into (cname, teacher) and (sid, cname)).

## 9. Internal Working
1. **State the FDs**: from business rules, decide the invariants (one dept per emp, one course per teacher).
2. **Verify against sample data**: no counterexample in the data = consistent (not proof of the FD's truth, just consistency).
3. **Find keys via closure**: compute X⁺ (Section 02) for each attribute set; the sets whose closure = R and which are minimal = candidate keys.
4. **Classify FDs**: trivial vs non-trivial; partial vs full (dependency on part of a key); transitive (X→Y, Y→Z, Y not part of a key, X not a key).
5. **Normalize**: remove the forbidden FD shapes by decomposition (Sections 05).
6. **In production**: FDs manifest as constraints (PK/UNIQUE/FK) and inform which relations to create — the DDL *is* the FD set made executable.

## 10. Time Complexity
- **Checking one FD on n rows**: O(n) to group by X and detect Y-conflicts (hash) — practical verification is linear.
- **Computing X⁺**: O(#FDs × #attributes) per iteration, O(attributes) iterations → polynomial; trivial for interview-sized problems.
- **Finding all candidate keys**: exponential in the worst case (#subsets), but the "attributes never on RHS" heuristic makes real problems fast.
- **Verifying X→Y holds (logical, from mini-world)**: O(1) — it's a semantic statement, not a computation.

## 11. Advantages
- **Precise vocabulary**: redundancy and bad design become *testable* conditions, not opinions.
- **Foundation for all normal forms**: one concept, six forms.
- **Key discovery**: candidate keys fall out of closure, mechanically.
- **Decomposition correctness**: FD preservation gives a criterion for "did I break the rules?"
- **Business-rule encoding**: FDs *are* the mini-world invariants — documenting them documents the domain.
- **Interview-provable**: you can demonstrate correctness step by step.

## 12. Disadvantages
- **Semantics required**: FDs can't be auto-discovered reliably from data (spurious FDs in samples).
- **Not all constraints**: FDs exclude other rules (e.g., "salary ≤ 2× average"), which need CHECKs/triggers.
- **Exponential candidate-key search** for adversarial FD sets.
- **Nuance-heavy**: partial vs full vs transitive distinctions trip people up.
- **Abstraction cost**: translating business rules into FD notation takes practice; interviewers love this as a differentiator.

## 13. Interview Questions
1. **Q: What is a functional dependency?** A: X→Y means every value of X determines exactly one value of Y — formally, any two tuples agreeing on X agree on Y. It captures an invariant of the mini-world: "emp_id determines name."
2. **Q: How do you test if X→Y holds in a given instance?** A: Group rows by X; if any group has more than one distinct Y value, the FD is violated. Absence of violation in the sample is *consistent* but doesn't prove the FD — FDs come from semantics.
3. **Q: What is a trivial FD?** A: Y ⊆ X — e.g., `{emp_id, name} → name` is trivial (always true). Trivial FDs carry no information and are dropped from normalization reasoning.
4. **Q: What is the difference between trivial and fully non-trivial?** A: Trivial: Y ⊆ X. Non-trivial: Y ⊄ X. Fully non-trivial: X ∩ Y = ∅ (no overlap). Normal forms care about *non-trivial* FDs.
5. **Q (tricky): If sample data has no FD violation, is the FD true?** A: No — only *consistent* with the sample. FDs are declared from the mini-world semantics ("one course has one teacher"). A future row can violate a false assumption. This is why FDs come from requirements, not `SELECT DISTINCT` analysis.
6. **Q: Why do FDs cause redundancy?** A: If X→Y and X is not a key, then every time X recurs, Y recurs — the same fact (teacher of DB) is stored on multiple rows. Updating it in one row and missing another = update anomaly. Normalization removes exactly these.
7. **Q (production): A table has duplicate data for `teacher` per course. What FD tells you the problem?** A: `cname → teacher` is non-trivial and its LHS isn't a key → the redundancy is real. Fix: decompose into (cname, teacher) and the rest — Part 03 §05.
8. **Q: What is the relationship between FDs and keys?** A: K is a superkey iff K → all attributes of R; K is a candidate key iff K → all and no proper subset does. So keys are FDs with maximal RHS and minimal LHS — keys are the "complete determiners".
9. **Q: Can you infer new FDs from given ones?** A: Yes — via Armstrong's axioms (reflexivity, augmentation, transitivity) and derived rules (union, decomposition, pseudo-transitivity). The set of all FDs implied by F is F⁺.
10. **Q (tricky): Does `A→B` and `B→C` imply `A→C`?** A: Yes — by transitivity. And `A→C` is *non-trivial* if C ∉ A. This is the classic "derive FDs" question.
11. **Q: What is a partial dependency?** A: An FD X→Y where X is a *proper subset* of a candidate key — Y depends on *part* of the key. E.g., with key (sid, cno), `cno → credits` is partial. Partial dependencies are what 2NF forbids.
12. **Q: What is a transitive dependency?** A: X→Y, Y→Z where Y is not a (super)key and Z ∉ Y — X determines Y determines Z, so Z depends on X *transitively*. E.g., emp_id → dept_id, dept_id → dept_name ⇒ emp_id transitively determines dept_name. 3NF forbids this.
13. **Q (scenario): Given FDs A→B, B→C, C→D, find candidate keys of R(A,B,C,D).** A: Closure of {A} = {A,B,C,D} = all → {A} is a candidate key (nothing before it; minimal). Answer: A.
14. **Q: Given FDs AB→C, C→A, find candidate keys of R(A,B,C).** A: {AB}⁺ = {A,B,C} = all. {C}⁺ = {C,A} ≠ all. {B} alone? {B}⁺={B}. So candidate keys: {AB} and... check {BC}: {B,C}⁺ = {A,B,C} = all → {BC} is also a candidate key! Answer: {AB} and {BC}.
15. **Q (production): Why is it risky to infer FDs from a data dump?** A: (1) Sample absence of violation ≠ invariant; (2) NULLs complicate "agree on X" checks; (3) future data shapes differ; (4) you miss semantic FDs no current row triggers. Always confirm with domain owners.
16. **Q: What is an FD set "F⁺"?** A: The closure of F: all FDs logically implied by F (via Armstrong's axioms). We work with F directly but reason about F⁺ when testing keys/normal forms.
17. **Q (tricky): Is `X→Y` with Y having a NULL value valid?** A: In the standard definition, "agree on X" still holds; NULLs complicate equality — most textbooks assume no NULLs for FD reasoning. In practice, a NULL Y means "not yet determined" — treat FD analysis on non-null assumptions and note the caveat.
18. **Q: How do FDs relate to normal forms?** A: Each normal form forbids a class of FDs: 2NF forbids partial (non-key-subset LHS) dependencies; 3NF forbids transitive dependencies; BCNF forbids *any* non-trivial FD whose LHS isn't a superkey. BCNF is the FD-maximal form.
19. **Q (scenario): Redesign a redundant `teacher` column. What's the first question you ask?** A: "Is `cname → teacher` an invariant of the business?" If yes, it's an FD, and teacher belongs in a `course` relation (determined by cname). If a course could have multiple teachers, it's *not* an FD — different problem (multivalued, Part 03 §04).
20. **Q (hard): Can FDs capture "each employee has exactly one department, each department one manager"?** A: Yes: emp_id → dept_id; dept_id → dept_name, dept_id → manager. Note the transitive chain emp_id → dept_id → manager: this makes `emp_id → manager` transitive → the design needs care (3NF vs BCNF analysis, Part 03 §03).

## 14. Follow-Up Questions
1. **Q: What is "inference" vs "discovery" of FDs?** A: Inference = deriving new FDs from F via axioms (logical). Discovery = observing patterns in data (statistical — unreliable). Interviews test inference; production should use discovery only to *flag* candidates.
2. **Q: What is the difference between an FD and a multivalued dependency (MVD)?** A: X→→Y (MVD) means Y's values vary *independently* with X — e.g., a person's skills and languages vary independently. FDs are a special case; MVDs are what 4NF addresses.
3. **Q: Why does normalization care only about non-trivial FDs?** A: Trivial FDs (Y ⊆ X) can never cause redundancy — the determined attributes are already there. Redundancy requires a non-trivial dependency, hence normal forms constrain non-trivial FDs.
4. **Q: Can two different FDs sets be equivalent (same F⁺)?** A: Yes — e.g., {A→B, B→C} and {A→B, A→C, B→C} may have the same closure. Deciding F₁ ≡ F₂ is the FD-equivalence problem (by closure comparison).
5. **Q: What is the "closure of a relation" vs "closure of an attribute set"?** A: Attribute-set closure X⁺ = all attributes derivable from X (used for keys). Relation closure F⁺ = all implied FDs. Different objects, same word "closure" — name which you mean.

## 15. Coding Example
```python
# FD checking on an instance (educational)
def holds_fd(rows, X, Y):
    seen = {}
    for r in rows:
        key = tuple(r[a] for a in X)
        val = tuple(r[a] for a in Y)
        if key in seen and seen[key] != val:
            return False          # two rows agree on X, differ on Y
        seen[key] = val
    return True                   # consistent with sample (not proof!)

rows = [
    {"sid": 1, "cname": "DB", "teacher": "ProfA"},
    {"sid": 2, "cname": "DB", "teacher": "ProfA"},
    {"sid": 1, "cname": "OS", "teacher": "ProfB"},
]
print(holds_fd(rows, ["cname"], ["teacher"]))  # True
print(holds_fd(rows, ["sid"], ["teacher"]))    # False
```
```sql
-- SQL check for X->Y consistency on a table
SELECT 1 FROM enroll e1
JOIN enroll e2 ON e1.cname = e2.cname          -- agree on X
WHERE  e1.teacher IS DISTINCT FROM e2.teacher  -- differ on Y
LIMIT 1;  -- returns a row => FD violated
```

## 16. Industry Usage
- **Database normalization at design time** in every shop: ER design → FD analysis → relations. Migration tools and ORM models encode FDs as constraints.
- **Data-warehouse design** (star schemas) is the *deliberate* choice to relax FDs (denormalize) for query speed — understanding FDs is what makes that a reasoned choice, not a mistake.
- **Data quality checks** re-implement FD validation in warehouses (dbt tests like `unique`, `not_null`, and custom FD tests) because warehouses often skip constraints.
- **Schema linting tools** flag probable FD violations (e.g., repeated `teacher` with same `cname`) — FD thinking automated.
- **Interview standard at Google/Amazon/Meta**: FD + closure + normal form questions are the purest way to test "does this candidate understand relational design theory?" — this chapter is the exact syllabus.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14 (Functional Dependencies and Normalization).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 8 (Relational Database Design).
- Armstrong, W. W., "Dependency Structures of Data Base Relationships", IFIP 1974.
- Date, C. J., *An Introduction to Database Systems*, 8th ed., Ch. 10-11.
- ISO/IEC 9075:2016 (SQL constraints that encode FDs).

## 18. Cheat Sheet
- X→Y: same X ⇒ same Y; an invariant of the mini-world, not a data observation.
- Trivial: Y ⊆ X (drop it). Fully non-trivial: X ∩ Y = ∅.
- Keys: K superkey ⟺ K → all; candidate key = minimal superkey (closure-based).
- Partial dependency: X ⊂ candidate key, Y not in X (→ 2NF violation).
- Transitive dependency: X→Y, Y→Z, Y not a key (→ 3NF violation).
- Every normal form = a ban on one FD shape.
- FDs come from semantics; sample data only confirms.
- Redundancy ⟺ a non-key LHS determines stored attributes.

## 19. Quiz
1. X→Y holds iff: a) data has no violation b) same X ⇒ same Y in every legal instance c) Y ⊆ X d) X is a key → **b**
2. `{a,b} → b` is: a) non-trivial b) trivial c) invalid d) transitive → **b**
3. FDs are declared from: a) sample data b) mini-world semantics c) indexes d) query plans → **b**
4. A partial dependency is: a) X→Y with X ⊂ key b) Y ⊂ X c) X = key d) X→→Y → **a**
5. A transitive dependency is: a) X→Y, Y→Z b) X→Y only c) Z→X d) Y→X → **a**
6. K is a superkey iff: a) K→all attrs b) K→Y only c) K ⊆ Y d) K trivial → **a**
7. With FDs A→B, B→C, the candidate key of (A,B,C) is: a) A b) B c) C d) ABC → **a**
8. Which does NOT cause redundancy? a) trivial FD b) partial FD c) transitive FD d) non-key X→Y → **a**
9. `cname → teacher` with key (sid,cname) is: a) full b) partial c) trivial d) multivalued → **b** (wait: cname ⊂ key, teacher ∉ → partial? Actually it's "not partial with respect to the key"—cname is part of key, teacher is outside → the FD has LHS ⊆ key but not = key, and it doesn't *depend on part of the key only*... careful: partial means X ⊂ key. cname ⊂ (sid,cname) → partial, yes) → **b**
10. FD inference uses: a) Armstrong's axioms b) EXPLAIN c) DISTINCT d) triggers → **a**

## 20. Flashcards
- **Q: What is an FD?** → **A:** X→Y: same X values always give same Y values — a mini-world invariant.
- **Q: Trivial FD?** → **A:** Y ⊆ X — always true, no redundancy, droppable.
- **Q: Where do FDs come from?** → **A:** Business semantics, not sample data.
- **Q: How are keys related to FDs?** → **A:** K is a superkey iff K→all attrs; candidate = minimal superkey.
- **Q: Partial dependency?** → **A:** X→Y where X is a proper subset of a candidate key.
- **Q: Transitive dependency?** → **A:** X→Y, Y→Z with Y not a key.
- **Q: Why do bad FDs cause redundancy?** → **A:** Non-key X repeats Y's stored value on every X occurrence.
- **Q: How to check FD consistency on data?** → **A:** Group by X; any group with 2+ Y values = violation.

## 21. Revision
FD: X→Y = "X determines Y" — a semantic invariant (same X ⇒ same Y). **Trivial** = Y⊆X (ignore). Keys: K superkey ⟺ K→all; candidate key = minimal superkey (via closure X⁺). The normal-form ladder: 2NF bans **partial** deps (X ⊂ key), 3NF bans **transitive** deps (X→Y, Y→Z, Y not key), BCNF bans any non-trivial FD with non-superkey LHS. Critical: FDs come from the *mini-world*, not sample rows. Interview moves: state the definition with the two-tuple test; give the partial/transitive examples; find keys from closure; and always translate "why redundant?" into "which FD has a non-key LHS?". Sample data only confirms; semantics dictate.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a functional dependency?" | 7 / 13 Q1 |
| "Trivial vs non-trivial FD?" | 13 Q3-4 |
| "Where do FDs come from?" | 13 Q2, Q5 |
| "FDs and keys?" | 13 Q8 |
| "Partial / transitive dependencies?" | 13 Q11-12 |
| "Find candidate keys from FDs?" | 13 Q13-14 |
| "Why do FDs cause redundancy?" | 13 Q6 |
| "Infer new FDs (Armstrong)?" | 13 Q10 |
