# Armstrong's Axioms and Closure of Attribute Sets

> **TL;DR**: Armstrong's axioms (reflexivity, augmentation, transitivity) are a sound and complete set of rules for deriving new FDs, and the attribute-closure X⁺ is the O(F·A) algorithm built on them that finds keys and tests normal forms mechanically.

## 1. Why Does This Exist?
Given an FD set F, you can *derive* new FDs (A→B, B→C ⇒ A→C). But which derivations are valid, and how do you know you've found them all? Armstrong's axioms exist to give inference a **sound and complete axiomatization**: sound = only true FDs are derived; complete = every FD in F⁺ can be derived. The *attribute-set closure* X⁺ exists as the algorithmic workhorse built on those axioms — instead of enumerating derivations, you compute "everything X can determine" in one pass. This section exists because (a) key-finding is a closure computation, (b) testing 2NF/3NF/BCNF reduces to closure checks, and (c) interviewers love the "find all candidate keys" question — which is closure in action.

## 2. How Does It Work?
**Armstrong's axioms (A1-A3):**
- **Reflexivity**: Y ⊆ X ⟹ X → Y.
- **Augmentation**: X → Y ⟹ XZ → YZ.
- **Transitivity**: X → Y, Y → Z ⟹ X → Z.
**Derived rules:** union (X→Y, X→Z ⇒ X→YZ), decomposition (X→YZ ⇒ X→Y, X→Z), pseudo-transitivity (X→Y, WY→Z ⇒ WX→Z).
**Attribute closure X⁺ algorithm**: start with X⁺ = X; repeatedly, for each FD `A→B` in F, if A ⊆ X⁺, add B to X⁺; repeat until no change. Result: every attribute functionally determined by X.
**Uses**: (1) X is a superkey ⟺ X⁺ = R; (2) candidate key = minimal superkey; (3) testing X→Y (⟺ Y ⊆ X⁺); (4) decomposing the closure to check dependency preservation.

## 3. When Is It Used?
- **Finding candidate keys** (the #1 normalization interview question) — via X⁺.
- **Testing FD membership**: X→Y ∈ F⁺ ⟺ Y ⊆ X⁺ (no need to derive F⁺ explicitly).
- **Testing normal forms**: an FD violates BCNF iff X⁺ ≠ R (LHS not a superkey); 3NF checks LHS superkey or RHS in a key.
- **Checking a decomposition preserves dependencies**: project F onto each relation, then test each original FD's membership via closure.
- **Schema design tools**: candidate keys and normal form checks are automated closure computations.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: enumerate all derivations of F⁺ manually.** Rejected: F⁺ is exponential; computing X⁺ once is polynomial. Closure is the efficient reformulation of "what does X determine?"
- **Alternative: test keys by trying all subsets of attributes.** Rejected: 2^n subsets; the closure-based heuristic ("start with attributes never on a RHS, close them") prunes to real work.
- **Alternative: other axiomatizations (different rule sets).** Armstrong's is the standard because it's *minimal in spirit* (3 core rules), sound, complete, and easy to reason about; alternatives (e.g., the "extended" rules) are equivalent but less memorable.
- **Why axioms at all?** Because without an axiomatic foundation you can't *prove* the inference is sound — and normalization's guarantee ("my decomposition preserves the rules") rests on those proofs.

## 5. Intuition
Think of X⁺ as **everything you can learn if you only know X**. If you know an employee's emp_id (X = {emp_id}), you can look up their name (emp_id→name), then their dept_id (emp_id→dept_id), then the dept's name (dept_id→dept_name) — chaining FDs like clue-following until nothing new appears. X⁺ is the full set of facts reachable. The axioms are just three common-sense moves: "if you have the whole, you have its parts" (reflexivity); "add context to both sides — truth stays true" (augmentation); "A determines B, B determines C ⇒ A determines C" (transitivity). A candidate key is an X whose closure swallows *the entire schema* — knowing the key, you can learn everything.

## 6. Real-World Analogy
X⁺ is a **detective's deduction closure**: the detective knows a license plate (X). Plate → owner (FD), owner → address (FD), address → voting district (FD). Working the chain, the detective closes on the whole file: plate⁺ = {plate, owner, address, district}. A *candidate key* of the case file is the single clue that lets you deduce *every* field. Transitivity is "if the plate finds the owner and the owner finds the address, the plate finds the address." Augmentation is "also knowing the time of the incident doesn't break any deduction — add it to both sides." The axioms are just formalizing what good detectives already do; the closure algorithm is them doing it exhaustively and fast.

## 7. Formal Definition
Given a relation R and FD set F (Armstrong 1974):
- **F⁺** = { X→Y : F ⊢ X→Y }, the set of all FDs derivable from F.
- **Axioms** (sound & complete for F⁺):
  - (A1) Reflexivity: if Y ⊆ X then X→Y.
  - (A2) Augmentation: if X→Y then XZ→YZ.
  - (A3) Transitivity: if X→Y and Y→Z then X→Z.
- **Closure of attribute set X**: X⁺ = { A : X→A ∈ F⁺ }.
- **Algorithm**: initialize X⁺ = X; repeat for each (α→β) ∈ F: if α ⊆ X⁺ then X⁺ := X⁺ ∪ β; until X⁺ stabilizes.
- **Key tests**: X is a superkey ⟺ X⁺ = R; X is a candidate key ⟺ X⁺ = R and no proper subset Y ⊂ X has Y⁺ = R.
- **FD membership**: X→Y ∈ F⁺ ⟺ Y ⊆ X⁺.
(Soundness & completeness proven by Armstrong; see Elmasri & Navathe Ch. 14, Silberschatz Ch. 8.)

## 8. Example
R(A, B, C, D, E); F = { A→B, B→C, CD→E }.
- **Compute {A}⁺**: start {A}. A→B: A ⊆ {A} → add B → {A,B}. B→C: B ⊆ {A,B} → add C → {A,B,C}. CD→E: CD ⊄ {A,B,C} → no. No more change → **{A}⁺ = {A,B,C}**.
- **Compute {C,D}⁺**: {C,D}. CD→E → add E → {C,D,E}. Others: A→B no (A ∉), B→C no (B ∉). → **{C,D}⁺ = {C,D,E}**.
- **Compute {A,C}⁺**: {A,C} → A→B → {A,B,C} → CD→E? D ∉ → no → **{A,C}⁺ = {A,B,C}**.
- **Find candidate keys**: attributes never on any RHS: A, D. So every key contains A and D. Close {A,D}: {A,D} → A→B → {A,B,D} → B→C → {A,B,C,D} → CD→E → {A,B,C,D,E} = R ✓. Is {A,D} minimal? Remove A: {D}⁺ = {D} ✗. Remove D: {A}⁺ = {A,B,C} ✗. → **{A,D} is the only candidate key**.
- **Is {A,D} a superkey test**: {A,D}⁺ = R ✓.

## 9. Internal Working
1. **Parse F** into a list of (lhs, rhs) pairs; drop trivial FDs (rhs ⊆ lhs) for speed.
2. **Close(X)**: mark members of X; loop over F until a full pass adds nothing; each iteration is O(|F|·|X|); worst-case O(|X|²·|F|) overall, fine for interviews.
3. **Candidate-key search**: let L = attributes never appearing on any RHS (must be in every key), R0 = attributes only on RHS (never in any key). Start candidates from subsets of the "middle" attributes added to L; close each; keep minimal ones.
4. **Membership test X→Y**: compute X⁺, check Y ⊆ X⁺ — used everywhere (normal-form tests, dependency-preservation checks).
5. **Normal-form tests** (Section 02-03): BCNF violation ⟺ some non-trivial X→Y with X⁺ ≠ R; 3NF violation ⟺ X not superkey AND Y not part of any candidate key.
6. **In tools**: engines don't compute this at runtime — it's a *design-time* algorithm applied by normalization utilities and interview solvers.

## 10. Time Complexity
- **X⁺ computation**: O(|F| · |X|) per pass, at most O(|R|) passes → **O(|F| · |R| · |X|)**, polynomial (tiny for interviews).
- **FD membership**: O(X⁺) — same as closure.
- **Candidate-key search (worst case)**: O(2^k) subsets of "middle" attributes in pathological FD sets; with the L-mandatory heuristic, near-linear in practice.
- **F⁺ enumeration**: exponential — never do it; membership tests avoid it.

## 11. Advantages
- **Mechanical correctness**: keys and normal forms become computed facts, not intuition.
- **Sound & complete**: Armstrong's axioms prove you can't derive wrong FDs and can derive all true ones.
- **Efficient membership**: X→Y testing without enumerating F⁺.
- **Foundation for all normal forms**: every form is a closure test away.
- **Interview-friendly**: small inputs, deterministic algorithm, easy to demonstrate step by step.
- **Tool automation**: the exact code behind "suggest keys" features in design tools.

## 12. Disadvantages
- **Exponential worst-case key search** for adversarial FDs.
- **Semantics not captured**: closure works on *given* FDs; wrong FDs in → wrong keys out (garbage in, garbage out).
- **Requires the full FD set**: missing an FD changes every key.
- **NULL handling unmodeled**: closure assumes no NULLs.
- **Conceptual overhead**: candidates must distinguish attribute-closure X⁺ from FD-set closure F⁺.

## 13. Interview Questions
1. **Q: State Armstrong's axioms.** A: Reflexivity (Y ⊆ X ⇒ X→Y), Augmentation (X→Y ⇒ XZ→YZ), Transitivity (X→Y, Y→Z ⇒ X→Z). Sound and complete for FD inference.
2. **Q: What is F⁺?** A: The closure of F: all FDs derivable from F via the axioms. We don't enumerate it (exponential) — we test membership via attribute closure instead.
3. **Q: What is X⁺ and how do you compute it?** A: All attributes functionally determined by X. Algorithm: X⁺ = X; for each FD (α→β) with α ⊆ X⁺, add β; repeat to fixpoint.
4. **Q: Compute {A}⁺ for F = {A→B, B→C}.** A: {A} → add B → {A,B} → B→C fires → {A,B,C}. So {A}⁺ = {A,B,C}.
5. **Q: How do you test if X→Y is in F⁺?** A: Compute X⁺; X→Y ∈ F⁺ ⟺ Y ⊆ X⁺. No need to build F⁺.
6. **Q: How do you find candidate keys with closure?** A: (1) L = attributes on no RHS (mandatory in every key); (2) start subsets from L + other attributes, compute X⁺; (3) X is a candidate key iff X⁺ = R and no proper subset also closes to R; keep minimal ones.
7. **Q (tricky): R(A,B,C), F = {AB→C, C→A}. Find candidate keys.** A: L = {B} (B never on RHS). Try {B}: {B}⁺ = {B} ✗. Add middle: {A,B}: AB→C → {A,B,C} ✓ minimal? {B} alone ✗ → yes. {B,C}: C→A → {A,B,C} ✓. So candidate keys: **{A,B} and {B,C}**.
8. **Q: Does reflexivity ever matter in normalization?** A: Only to drop trivial FDs — normalization reasons about non-trivial FDs; reflexivity guarantees trivial ones are always true and harmless.
9. **Q (scenario): Prove BCNF violation using closure.** A: Find non-trivial X→Y with X⁺ ≠ R. E.g., in R(A,B,C) with {AB→C, C→A}: C→A has C⁺ = {C,A} ≠ R → C isn't a superkey → R is not in BCNF. That's the whole test.
10. **Q: What's the difference between F⁺ and X⁺?** A: F⁺ = the set of all implied FDs (a set of rules); X⁺ = the set of attributes a specific X determines (a set of attributes). Related: X⁺ = {A : X→A ∈ F⁺}.
11. **Q (production): A tool says {A} is a key but your business knows B is also unique. What's the issue?** A: The tool computes closure over the *given* FDs — if the FD set is incomplete (B→all wasn't declared), the answer is wrong. Keys are only as good as the FD set. Always validate with domain semantics.
12. **Q: How does closure test 3NF?** A: R is in 3NF iff for every non-trivial X→Y ∈ F⁺: X is a superkey (X⁺ = R) OR Y ⊆ some candidate key. Both conditions are closure tests.
13. **Q (tricky): Is the union rule derivable from the axioms?** A: Yes — X→Y and X→Z ⇒ X→YZ via augmentation (X→Y ⇒ X→YZ? augment with Z: X→Y ⇒ XZ→YZ, and X→Z ⇒ X→XZ by augmentation with X... the standard proof uses augmentation + transitivity). Derived rules are theorems, not axioms.
14. **Q: Can two different FD sets have the same F⁺?** A: Yes — they're "equivalent FD sets" (e.g., {A→B, B→C} vs {A→B, A→C, B→C} can be equivalent). Equivalent iff each FD of one is in the other's closure.
15. **Q (scenario): Given R(A,B,C,D), F = {A→B, B→C, C→D, D→A}, find all candidate keys.** A: Every attribute appears on RHS → L empty; test singletons: {A}⁺: A→B→C→D = all ✓. {B}⁺: B→C→D→A = all ✓. {C}⁺: C→D→A→B = all ✓. {D}⁺: all ✓. So all four singletons are candidate keys (a cyclic FD ring).
16. **Q: How do you verify a decomposition preserves dependencies?** A: Project F onto each decomposed relation (only FDs whose attributes fit), then for each original FD X→Y, check Y ⊆ X⁺ computed over the union of projected FDs. If all hold, dependencies preserved.
17. **Q (tricky): If X⁺ = R, is X necessarily a candidate key?** A: No — X is a *superkey*. Candidate key requires minimality: no proper subset Y ⊂ X with Y⁺ = R. {A,B} might be a superkey while {A} alone is the candidate key.
18. **Q: Why is checking "X→Y ∈ F⁺" done via closure and not by deriving?** A: F⁺ can be exponential in size; membership via X⁺ is polynomial. Same answer, vastly cheaper.
19. **Q (production): How would you validate a proposed key in a live table?** A: SQL check: `SELECT X_cols, COUNT(*) FROM t GROUP BY X_cols HAVING COUNT(*) > 1;` returns nothing ⇒ X is unique on *current* data (a superkey for the sample). But minimality (candidate) and semantic permanence still need FD reasoning.
20. **Q (hard): Prove that {A,D} in R(A,B,C,D) with F={A→B, B→C, C→D} is NOT a candidate key... wait, is it?** A: {A,D}⁺: A→B→C→D → {A,B,C,D} = R, so {A,D} is a superkey. But minimality: remove D → {A}⁺ = {A,B,C,D} = R too! So {A} is a candidate key and {A,D} is *not* a candidate key (not minimal). The trap: superkey ≠ candidate key.

## 14. Follow-Up Questions
1. **Q: What is "dependency-preserving" exactly?** A: After decomposition, every FD in F is still implied by the projected FDs on the parts — no rule is lost. Tested via closure (Section 05).
2. **Q: When is it impossible to have both BCNF and dependency preservation?** A: The classic counterexample (e.g., R(A,B,C), {AB→C, C→A}) — any BCNF decomposition loses an FD; you settle for 3NF (which is always dependency-preserving via the synthesis algorithm).
3. **Q: What is the 3NF synthesis algorithm?** A: Canonical cover F_c → one relation per FD's lhs → merge → add a relation with a candidate key if none contains one. Guarantees lossless + dependency-preserving 3NF. (Contrast: BCNF decomposition algorithm — Section 05.)
4. **Q: Does SQL enforce FDs beyond keys?** A: PK/UNIQUE/FK/CHECK enforce *some* FDs; general FDs (e.g., `cname → teacher`) need triggers or app logic — part of the reason normalization matters even with constraints.
5. **Q: What's the difference between Armstrong's completeness and soundness proofs?** A: Soundness = every derivable FD is truly implied (easy, by definition of the axioms). Completeness = every implied FD is derivable (proved by constructing a specific relation that violates any non-derivable FD). Interviewers occasionally probe that you know both properties exist.

## 15. Coding Example
```python
def closure(attrs, fds):
    """Compute X⁺ given an attribute set and list of (lhs, rhs) FDs."""
    X = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if lhs <= X and not rhs <= X:
                X |= rhs
                changed = True
    return X

def is_superkey(attrs, all_attrs, fds):
    return closure(attrs, fds) == set(all_attrs)

def is_candidate_key(attrs, all_attrs, fds):
    if not is_superkey(attrs, all_attrs, fds):
        return False
    return not any(is_superkey(set(attrs) - {a}, all_attrs, fds)
                   for a in attrs)

all_attrs = "ABCDE"
fds = [("A", "B"), ("B", "C"), ("CD", "E")]
print(closure("A", fds))            # {'A','B','C'}
print(closure("AD", fds))           # {'A','B','C','D','E'}  -> superkey
print(is_candidate_key("AD", all_attrs, fds))  # True (A and D alone fail)
```

## 16. Industry Usage
- **Design-time normalization tools** (dbdiagram validators, schema linting) compute closure to flag non-normalized tables and suggest keys.
- **Data modeling textbooks/tools** (ERwin, Vertabelo) embed FD-driven key discovery — the closure algorithm is inside every one.
- **Query/view optimization** uses FD reasoning: if a view's schema implies X→Y, the optimizer can substitute or simplify joins (functional-dependency-aware planning in Postgres for `DISTINCT ON`-like rewrites).
- **Inference in dependency theory** underpins schema-integration and data-exchange theory (Chase algorithm) — closure is the primitive.
- **Interview standard**: "find the candidate keys" is *the* classic normalization question — mastery of closure is the difference between guessing and computing.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14 (Relational Database Design; closure, axioms).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 8.2-8.4 (Functional Dependencies; closure).
- Armstrong, W. W., "Dependency Structures of Data Base Relationships", IFIP 1974.
- Date, C. J., *An Introduction to Database Systems*, 8th ed., Ch. 11 (Relational Design Theory).
- PostgreSQL, `DISTINCT ON` + FD-aware planning notes (design rationale).

## 18. Cheat Sheet
- Axioms: Reflexivity (Y⊆X ⇒ X→Y), Augmentation (X→Y ⇒ XZ→YZ), Transitivity (X→Y, Y→Z ⇒ X→Z).
- Derived: union, decomposition, pseudo-transitivity.
- X⁺ = all attributes determined by X (algorithm: add RHS of any FD whose LHS ⊆ X⁺, to fixpoint).
- Superkey ⟺ X⁺ = R; candidate key = minimal superkey.
- X→Y ∈ F⁺ ⟺ Y ⊆ X⁺ (membership via closure).
- Mandatory-in-key attributes: those never on any RHS.
- Closure is polynomial; F⁺ enumeration is exponential — never enumerate.
- BCNF test = every non-trivial FD has X⁺ = R; 3NF test = superkey OR RHS in a key.

## 19. Quiz
1. The three Armstrong axioms: a) reflexivity, augmentation, transitivity b) union, product, join c) select, project, rename d) 1NF,2NF,3NF → **a**
2. `{A,B}⁺` for F={A→C} is: a) {A,B,C} b) {A,B} c) {C} d) {A,C} → **a**
3. X is a superkey iff: a) X⁺ = R b) X ⊆ R c) X has 2 attrs d) X⁺ small → **a**
4. X→Y ∈ F⁺ iff: a) Y ⊆ X⁺ b) X ⊆ Y c) Y = X d) X = R → **a**
5. R(A,B,C), F={A→B, B→C}: candidate key: a) A b) B c) C d) AB → **a**
6. R(A,B,C,D), F={A→B,B→C,C→D,D→A}: candidate keys: a) {A} b) {A,B,C,D} all singletons c) {A,B} d) {B,C,D} → **b**
7. A superkey that's not minimal is: a) candidate b) not a candidate key c) an FD d) a trivial key → **b**
8. Which rule is derived, not axiomatic? a) union b) reflexivity c) augmentation d) transitivity → **a**
9. Membership tests avoid: a) computing F⁺ b) parsing c) indexes d) SQL → **a**
10. Attributes never on any RHS: a) must be in every key b) never in keys c) trivial d) dropped → **a**

## 20. Flashcards
- **Q: Three Armstrong axioms?** → **A:** Reflexivity, Augmentation, Transitivity.
- **Q: What is X⁺?** → **A:** All attributes functionally determined by X; computed by closure iteration.
- **Q: Superkey test?** → **A:** X⁺ = R.
- **Q: Candidate key test?** → **A:** X⁺ = R and no proper subset closes to R.
- **Q: X→Y membership test?** → **A:** Y ⊆ X⁺.
- **Q: Mandatory key attributes?** → **A:** Attributes never on any FD's RHS.
- **Q: Why not enumerate F⁺?** → **A:** Exponential; closure membership is polynomial.
- **Q: 3NF test via closure?** → **A:** Every non-trivial X→Y: X superkey OR Y in a candidate key.

## 21. Revision
Armstrong: **Reflexivity** (Y⊆X ⇒ X→Y), **Augmentation** (X→Y ⇒ XZ→YZ), **Transitivity** (X→Y,Y→Z ⇒ X→Z) — sound + complete. **X⁺** algorithm: X⁺=X; add RHS of any FD whose LHS ⊆ X⁺; repeat to fixpoint. Uses: superkey ⟺ X⁺=R; candidate key = minimal superkey; membership X→Y∈F⁺ ⟺ Y⊆X⁺; BCNF ⟺ every non-trivial FD has X superkey; 3NF ⟺ superkey OR RHS ⊆ some key. Key-finding heuristic: attributes never on a RHS are mandatory in every key. Interview moves: compute X⁺ out loud step by step; find all candidate keys; state axioms from memory; and prove/refute "is this in BCNF?" with a single closure check. Never enumerate F⁺.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "State Armstrong's axioms" | 7 / 13 Q1 |
| "What is X⁺ / how to compute it?" | 7 / 13 Q3-4 |
| "Find all candidate keys from FDs" | 8 / 13 Q6-7, Q15 |
| "How to test X→Y ∈ F⁺?" | 13 Q5 |
| "Prove/refute BCNF via closure?" | 13 Q9 |
| "How to test 3NF?" | 13 Q12 |
| "Superkey ≠ candidate key?" | 13 Q17, Q20 |
| "Dependency-preserving test?" | 13 Q16 |
