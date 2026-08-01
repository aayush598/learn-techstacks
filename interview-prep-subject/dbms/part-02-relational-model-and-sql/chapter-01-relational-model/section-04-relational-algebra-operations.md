# Relational Algebra Operations

> **TL;DR**: Relational algebra is a set of closed operations (select, project, join, rename, union, difference, product, aggregate) on relations — the formal foundation that defines *exactly* what SQL means and the basis the optimizer uses to rewrite queries.

## 1. Why Does This Exist?
Relational algebra exists because SQL's meaning must be **precise and provable**. Natural-language descriptions of queries are ambiguous; an algebra gives every query a rigorous, compositional meaning (what the result *is*). It also gives the optimizer its raw material: algebraic laws — `σ_A(σ_B(R)) = σ_B(σ_A(R))`, `σ(R⋈S) = σ(R)⋈S` under conditions, join commutativity — are provably-correct transformations the planner uses to find a faster plan. And it's a *closed* algebra: operations take relations and return relations, so queries compose. In interviews, relational algebra is how you answer "what does this SQL actually compute?" with zero ambiguity, and how you prove two queries equivalent.

## 2. How Does It Work?
Eight core operations over relations:
- **σ (select / restriction)**: σ_condition(R) — keeps tuples satisfying the predicate (row filter).
- **π (project)**: π_A₁,..,Ak(R) — keeps only the listed columns, *deduplicating* (set semantics).
- **ρ (rename)**: renames relation or attributes (for self-joins and clarity).
- **× (cartesian product)**: all pairs of tuples; usually a building block for joins.
- **⋈ (join)**: σ over × — the general join is `σ_θ(R × S)`; specialized: natural join ⋈ (equijoin on common attributes, one copy kept), theta join, equi-join, semi-join, anti-join.
- **∪ (union)**, **− (set difference)**, **∩ (intersection)**: set operations (same schemas required).
- **Aggregation (γ)**: GROUP BY + aggregate functions (SUM/AVG/COUNT/MIN/MAX) — technically extends the core algebra.
- **Division (÷)**: "tuples that match *all* of another relation" — rarely used directly but asked in theory.

## 3. When Is It Used?
- **Defining SQL semantics**: every `SELECT` maps to σ/π/⋈; `WHERE`→σ, `SELECT cols`→π, `FROM a JOIN b`→⋈, `GROUP BY`→γ. Interviewers ask "translate this SQL to algebra" to test precision.
- **Query optimization**: the optimizer applies algebraic rewrite laws (push σ down, choose join order) — knowing the laws explains *why* plans change.
- **Proving query equivalence**: two SQL queries are equivalent iff their algebra expressions are equivalent under the laws.
- **Theory questions**: division ("customers who ordered every product"), set operations, semi/anti-join semantics.
- **Writing correct complex SQL**: expressing a hard query as algebra first (what do I select, project, join?) almost always produces correct SQL.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: procedural navigation (network model).** Rejected: it specifies *how* to walk pointers, coupling the query to physical layout; algebra is *declarative* — it says what the answer is, letting the optimizer choose how.
- **Alternative: relational calculus (tuple/domain).** Calculus exists and is equivalent in power (Codd's theorem: relational algebra = domain-independent relational calculus), but algebra is *constructive* (gives a recipe/plan), which is why SQL (a hybrid) and optimizers lean on algebra.
- **Alternative: natural-language queries.** Rejected: ambiguous; algebra removes ambiguity — a query means exactly its algebraic expression.
- **Why these eight operations?** Because they're *minimal and closed*: a small set of primitives that can express every relational query, and every result is a relation (composition). SQL's bag extensions, NULLs, and `DISTINCT` are pragmatic additions on top of this pure foundation.

## 5. Intuition
Think of relational algebra as **recipe cards for a database kitchen**. "σ" = sieve (filter ingredients), "π" = trim (keep only the parts you need), "⋈" = combine two bowls by matching a shared ingredient (e.g., match customer-id), "∪" = pour two bowls of the same dish together, "−" = remove what's in the other bowl, "×" = put everything together and see all combinations. Because every step outputs the same kind of thing (a relation), you can keep chaining recipes as long as you want — the algebra is closed. SQL is just the "recipe language" you speak to the kitchen; the algebra is what the head chef (optimizer) actually reasons about to cook it fastest.

## 6. Real-World Analogy
A **library's query process**: σ = "only paperbacks" (filter the shelves); π = "just titles and authors" (pick columns); ⋈ = "join the catalogue with the loans table on ISBN" (match by shared value); ∪ = "all books from both branches"; − = "books that branch A has but B doesn't"; × = "pair every book with every shelf (wasteful — hence joins)". The librarian doesn't describe *how* to physically fetch (walk aisle 3, look at spine, etc.) — the algebra says *what* to compute, and the librarian picks the fastest route. That's exactly the division of labor between algebra (what) and optimizer (how).

## 7. Formal Definition
Relational algebra (Codd 1970; Elmasri & Navathe Ch. 5; Silberschatz Ch. 3.3):
- **Select**: σ_θ(R) = { t ∈ R : t satisfies θ } — schema of R; θ is a Boolean condition on attributes.
- **Project**: π_{A₁,...,Ak}(R) = { t[A₁,...,Ak] : t ∈ R } — keeps listed attributes; duplicates removed (set semantics).
- **Rename**: ρ_{S(B₁,...,Bn)}(R) — renames relation/attributes.
- **Cartesian product**: R × S = { t ∪ s : t ∈ R, s ∈ S } — all pairs.
- **Join**: R ⋈_θ S = σ_θ(R × S). **Natural join** ⋈: equijoin on all common attributes, one copy retained. **Equijoin**: θ is equality.
- **Set ops**: R ∪ S, R − S, R ∩ S — require union-compatible schemas (same arity, comparable domains).
- **Aggregation**: γ_{G; f1(A), f2(B)}(R) — group by G, apply functions (sum/count/avg/min/max).
- **Division**: R ÷ S = { t : t ∈ π_{X}(R) and for every s ∈ S, (t,s) ∈ R }, X = attrs(R) − attrs(S).
- **Codd's theorem**: relational algebra is equivalent in expressive power to domain-independent relational calculus (tuple/domain).

## 8. Example
```
STUDENT(sid, name, dept, gpa)      COURSE(cno, cname)   ENROLL(sid, cno, grade)
S = {(1,Alice,CS,3.8),(2,Bob,EE,3.2),(3,Cara,CS,3.9)}
```
1. **σ**: σ_{gpa>3.5}(S) = {(1,Alice,CS,3.8),(3,Cara,CS,3.9)}.
2. **π**: π_{name}(σ_{dept='CS'}(S)) = {Alice, Cara} (deduped set).
3. **⋈**: ENROLL ⋈ STUDENT on sid = one row per (enroll, student) match.
4. **Natural join** ENROLL ⋈ COURSE on cno — common column cno kept once.
5. **÷**: "students who enrolled in every course": needs π_{sid,cno}(ENROLL) ÷ π_{cno}(COURSE). With courses CS101, EE200: student 1 enrolled both → included; student 2 only CS101 → excluded.
6. **∪ / −**: σ_{dept='CS'}(S) ∪ σ_{dept='EE'}(S) = all students; σ_{CS}(S) − σ_{EE}(S) = CS students only.

## 9. Internal Working
1. **SQL → algebra**: parser translates `SELECT name FROM student WHERE dept='CS'` into `π_name(σ_dept='CS'(student))`.
2. **Optimizer rewrites** using laws:
   - σ push-down: `σ(g ⋈ h)` → `σ(g) ⋈ σ(h)` (filter early, fewer rows).
   - π push-down/projection elimination: drop columns early.
   - Join commutativity/associativity: reorder joins to reduce intermediate size.
   - σσ/ππ simplification and merging.
3. **Physical plan**: algebra operators map to physical operators (IndexScan implements σ+π on an index; HashJoin implements ⋈; GroupAggregate implements γ).
4. **Execution**: operators pull tuples bottom-up; each algebraic result = each operator's output; results remain relations (closed), so operators nest.

## 10. Time Complexity
- **σ with scan**: O(n); with index: O(log n + k).
- **π**: O(n) plus dedup (O(n) hash or O(n log n) sort).
- **R × S**: O(|R|·|S|) — always the most expensive primitive; joins exist to avoid it.
- **⋈ natural/equijoin**: hash join O(n+m); sort-merge O(n log n + m log m); index nested-loop O(n log m); nested-loop O(n·m).
- **∪ / − / ∩**: O(n+m) hashing (after dedup); O(n log n + m log m) via sort.
- **γ group-by**: O(n) hash aggregate or O(n log n) sort aggregate.
- **÷**: O(n·m) in naive form (division is the most expensive op).

## 11. Advantages
- **Precise semantics**: every query has an exact, provable meaning.
- **Compositional & closed**: relations in, relations out — infinite nesting.
- **Optimization substrate**: algebraic laws give provably-correct rewrites (the basis of every query planner).
- **Language-independent**: it's the same foundation under SQL, and even explains NoSQL subset queries.
- **Minimal primitives**: a small set covers all relational querying.
- **Interview precision**: lets you express and verify tricky queries symbolically before writing SQL.

## 12. Disadvantages
- **Set semantics vs SQL bags**: the algebra dedupes automatically; SQL doesn't unless `DISTINCT`. Students must remember the leak.
- **No NULLs in the pure algebra**: NULLs and three-valued logic aren't in Codd's core algebra — SQL extends it, complicating "pure" reasoning.
- **Verbose**: real queries become long expression chains; SQL hides the algebra.
- **π loses columns permanently** — order of σ/π matters and mistakes are easy to make.
- **Not directly executable**: it's a specification, not a language; a cost model + physical operators are required for execution.

## 13. Interview Questions
1. **Q: What is relational algebra?** A: A formal, closed set of operations (σ, π, ⋈, ρ, ×, ∪, −, ∩, γ) on relations that gives SQL its precise semantics and the optimizer its rewrite laws. Every SQL query maps to an algebra expression.
2. **Q: Explain σ, π, ⋈, ρ.** A: σ = select (filter rows by predicate); π = project (keep columns, dedupe); ⋈ = join (combine on a condition/common attributes); ρ = rename (relations/attributes). Plus × (product), ∪ (union), − (difference), ∩ (intersection).
3. **Q: What is the difference between select in algebra and SELECT in SQL?** A: Algebra's *select* (σ) = SQL's `WHERE` (row filter). SQL's `SELECT` = algebra's *project* (π) for the column list. Classic naming trap — say it explicitly.
4. **Q: What is the cartesian product and why is it expensive?** A: R × S = all |R|·|S| pairs; it's the most expensive primitive (O(n·m)) and produces huge useless output unless immediately filtered — which is exactly why joins (σ over ×) exist.
5. **Q: What is a natural join vs an equi-join vs a theta join?** A: Natural join = equijoin on *all common attribute names*, keeping one copy of the join column; equi-join = join where θ is equality on specified columns; theta join = any arbitrary condition (>, <, <>). `ON a.x = b.y` is an equi-join; `ON a.x = b.y AND a.z > b.w` is a theta join.
6. **Q (tricky): What happens to duplicate join columns in a natural join?** A: The common columns are merged into one — the natural join schema drops the duplicate. That's why it's "natural": no `ON` clause, no duplicated column. Beware: it silently joins on *every* common-named attribute, which can be wrong.
7. **Q: What are union-compatible relations?** A: Two relations with the same degree and corresponding attributes from comparable domains — required for ∪, −, ∩. SQL relaxes this with coercion.
8. **Q: What is a semi-join? What is an anti-join?** A: Semi-join returns rows of R that have *a match* in S (without S's columns) — R ⋉ S. Anti-join returns R rows with *no match* — used for "NOT EXISTS". SQL expresses semi-join via `IN`/`EXISTS`, anti-join via `NOT IN`/`NOT EXISTS`.
9. **Q: Translate `SELECT name FROM student WHERE dept='CS'` to algebra.** A: π_name(σ_dept='CS'(student)). (Or with rename as needed.) Precision here is the point.
10. **Q (production): Why does the optimizer "push σ down"?** A: Because σ reduces rows before joins (σ(a)⋈σ(b) instead of σ(a⋈b)) — fewer rows through the expensive join. It's a provably-correct rewrite: `σ_θ(R ⋈ S) = σ_θ(R) ⋈ S` when θ references only R. Explains why `EXPLAIN` shows filters early.
11. **Q: What is division in relational algebra?** A: R ÷ S = the tuples of R's non-S columns that are paired with *every* tuple of S — "customers who bought all products." Used to answer universal quantification ("for all") queries.
12. **Q (scenario): Write division as SQL — "students who enrolled in every course."** A: With a `HAVING` count trick: `SELECT sid FROM enroll GROUP BY sid HAVING COUNT(DISTINCT cno) = (SELECT COUNT(*) FROM course);` Division has no direct SQL operator — this is the standard translation.
13. **Q: What is the expressive relationship between algebra and calculus?** A: Codd's theorem — they're equally powerful (for domain-independent calculus). SQL is a hybrid; the equivalence matters for theory questions about query expressiveness.
14. **Q: How do aggregate functions extend the algebra?** A: Via γ (generalized projection/aggregation): γ_{dept, AVG(gpa)}(S) groups by dept and computes average. SQL's `GROUP BY` maps directly to γ.
15. **Q (tricky): Does π in algebra guarantee distinct output?** A: Yes — algebra is set-based, so π removes duplicates automatically. SQL's `SELECT col` does *not* (bag semantics) — you need `DISTINCT`. This is the single most common algebra↔SQL confusion.
16. **Q: What is the difference between a join and a product?** A: Product = every pair (O(n·m)); join = product filtered by a condition — typically equality on keys, so far fewer results and faster (index/hash algorithms). Join is "meaningful product."
17. **Q: Why is the algebra called "closed"?** A: Because every operation takes relations and returns a relation — so results can be operands of further operations. Closure is what makes query composition possible.
18. **Q (production): What are the main algebraic rewrite laws used by optimizers?** A: σ push-down, π push-down/projection elimination, join associativity/commutativity (reordering), σ/π merging and simplification, and converting subqueries to joins. Each preserves the result while changing cost.
19. **Q: Can relational algebra express `NOT EXISTS`?** A: Yes — anti-join, R − (R ⋉ S)-style: R rows minus rows that matched. In algebra terms `R − π_{R}(R ⋈ S)` (for equi-join). Another reason algebra is precise where SQL is permissive.
20. **Q (hard): Why does the optimizer prefer hash joins over nested-loop joins on big inputs?** A: Nested-loop is O(n·m) — quadratic in join size; hash join builds one hash table (O(n)) and probes with the other (O(m)) → O(n+m). Algebra doesn't choose; the *physical* implementation does — algebra defines what, physical operators define how.

## 14. Follow-Up Questions
1. **Q: Is `COUNT(*)` an algebra operation?** A: It's part of aggregation (γ with no grouping = a single group). Pure Codd algebra had no aggregates; they're a standard extension.
2. **Q: What is "query containment"?** A: Q1 ⊆ Q2 if every answer of Q1 is an answer of Q2 — reasoning about algebra expressions; used in view optimization and data-integration theory.
3. **Q: How does algebra handle NULLs?** A: It doesn't — pure algebra assumes no NULLs; SQL's three-valued logic is an extension that breaks some pure-algebra laws (e.g., NOT IN with NULLs). Know both, and the trap.
4. **Q: What is the difference between a semi-join and a regular join in optimization?** A: Semi-join returns only left rows (no right columns, no duplication if right has many matches) — useful for existence checks; optimizers use it for `EXISTS` to avoid materializing duplicates.
5. **Q: Why teach algebra if everyone writes SQL?** A: Because correctness, equivalence, and optimization are all defined in algebra; SQL is the dialect. Interviews probe it to distinguish memorized SQL from real understanding.

## 15. Coding Example
```sql
-- SQL for each algebra concept (with our schema)
-- σ (WHERE), π (SELECT ...), natural/equi join
SELECT name, cname FROM student s, enroll e, course c
WHERE  s.sid = e.sid AND e.cno = c.cno AND s.dept = 'CS';
--   = π_name,cname( σ_dept='CS'( STUDENT ⋈ ENROLL ⋈ COURSE ) )

-- Semi-join (EXISTS): students who have at least one enrollment
SELECT sid, name FROM student s
WHERE EXISTS (SELECT 1 FROM enroll e WHERE e.sid = s.sid);
-- Anti-join (NOT EXISTS): students with NO enrollment
SELECT sid, name FROM student s
WHERE NOT EXISTS (SELECT 1 FROM enroll e WHERE e.sid = s.sid);

-- Division via COUNT: students who enrolled in ALL courses
SELECT sid FROM enroll
GROUP BY sid
HAVING COUNT(DISTINCT cno) = (SELECT COUNT(*) FROM course);

-- Union / difference
SELECT sid FROM student WHERE dept='CS' UNION      -- set: dedupes
SELECT sid FROM student WHERE gpa > 3.5;
SELECT sid FROM student WHERE dept='CS' EXCEPT     -- difference
SELECT sid FROM student WHERE gpa <= 3.5;
```
```python
# Tiny algebra engine (educational) — operators return sets of frozensets
def select_rel(R, pred):   return {t for t in R if pred(t)}
def project_rel(R, cols):  return {tuple(t[c] for c in cols) for t in R}
def join(R, S, on):
    return {(r, s) for r in R for s in S if r[on] == s[on]}
```
(Every function returns a *set* — the algebra's no-duplicates semantics enforced automatically.)

## 16. Industry Usage
- **PostgreSQL / MySQL / SQL Server / Oracle** all compile SQL to an algebraic logical plan, then rewrite it using exactly the laws in this section before choosing physical operators (`EXPLAIN` shows the physical result of the algebraic optimization).
- **Apache Calcite** (the query engine behind Flink, Druid, Hive) exposes the algebra explicitly: SQL → relational expression tree → optimizer rules (σ push-down, join reorder) → execution. It's the algebra in industrial form.
- **Query rewrite for views / materialized views** uses algebra equivalences: can a new query be answered by an existing materialized view? That's a containment/equivalence check — algebra again.
- **Cost-based optimization** in every warehouse (Snowflake, Redshift, BigQuery) computes join orders over algebra expressions using statistics — the same laws, at exabyte scale.
- **Data-stream engines** (Flink/Kafka Streams) use the same relational algebra over streams — the "relational model for streaming" (streams are infinite relations).

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 5 (Relational Algebra).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 3.3 (Relational Algebra).
- Codd, E. F., "Relational Completeness of Data Base Sublanguages", 1972.
- Date, C. J., *An Introduction to Database Systems*, 8th ed., Ch. 6-7.
- Apache Calcite (SQL → algebra → optimization): https://calcite.apache.org/
- ISO/IEC 9075:2016 (SQL Standard; SQL semantics map to algebra).

## 18. Cheat Sheet
- σ = filter rows (SQL WHERE); π = keep columns, dedupe (SQL SELECT + DISTINCT).
- ⋈ natural/equi/theta join; × product (O(n·m) — expensive).
- ρ rename; ∪ / − / ∩ set ops (union-compatible schemas).
- γ group-by aggregation; ÷ division ("for all" queries).
- Codd's theorem: algebra = domain-independent calculus.
- Optimizer laws: σ push-down, π push-down, join reorder, subquery-to-join.
- Semi-join = EXISTS; anti-join = NOT EXISTS.
- Algebra = set semantics (no dups); SQL = bag semantics (add DISTINCT).

## 19. Quiz
1. Algebra's σ corresponds to SQL's: a) SELECT cols b) WHERE c) JOIN d) GROUP BY → **b**
2. π always outputs: a) bags b) sets (deduped) c) sorted rows d) ordered tuples → **b**
3. Cartesian product R×S has how many tuples? a) |R|+|S| b) |R|·|S| c) max d) min → **b**
4. Natural join joins on: a) a user column b) all common attribute names c) PK d) index → **b**
5. NOT EXISTS in SQL corresponds to: a) natural join b) anti-join c) semi-join d) product → **b**
6. "Customers who bought every product" needs: a) σ b) division c) π d) ρ → **b**
7. Which is O(n·m)? a) hash join b) nested-loop join c) index lookup d) sort → **b**
8. σ push-down is: a) a rewrite law b) an error c) a DDL command d) a constraint → **a**
9. UNION in SQL (without ALL) matches: a) ∪ b) − c) × d) ⋈ → **a**
10. The algebra's closure property means: a) it can't nest b) results are relations c) no joins d) no NULLs → **b**

## 20. Flashcards
- **Q: σ vs π vs ⋈?** → **A:** Filter rows / keep columns (dedupe) / join relations.
- **Q: Algebra SELECT vs SQL SELECT?** → **A:** σ = WHERE; π = SELECT cols.
- **Q: What is O(n·m)?** → **A:** Cartesian product / nested-loop join.
- **Q: Natural join?** → **A:** Equijoin on all common-named attrs, one copy kept.
- **Q: Semi-join vs anti-join?** → **A:** Rows with a match (EXISTS) vs rows without (NOT EXISTS).
- **Q: Division is for?** → **A:** "For all" queries (bought every product).
- **Q: Why push σ down?** → **A:** Fewer rows before joins — provably-correct rewrite.
- **Q: Algebra vs SQL duplicates?** → **A:** Algebra dedupes (set); SQL needs DISTINCT (bag).

## 21. Revision
Relational algebra = the precise semantics under SQL: **σ** (filter rows / WHERE), **π** (keep columns, dedupe / SELECT cols + DISTINCT), **⋈** (join: natural = common attrs, equi = equality, theta = any condition), **ρ** (rename), **×** (product, O(n·m) — why joins exist), **∪ / − / ∩** (set ops), **γ** (group-by aggregates), **÷** (division = "for all"). Codd's theorem: algebra ≡ calculus. The optimizer's rewrite laws (σ push-down, π push-down, join reorder, subquery→join) come straight from this algebra. Interview moves: translate SQL→algebra precisely; state the σ/SELECT naming trap; explain semi/anti-join via EXISTS/NOT EXISTS; write "all courses" division via COUNT; and always flag algebra=set vs SQL=bag. Mention Calcite as algebra in production.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is relational algebra?" | 7 / 13 Q1 |
| "Translate SQL to algebra" | 13 Q9 |
| "Natural vs equi vs theta join" | 13 Q5-6 |
| "What is division?" | 13 Q11-12 |
| "Why push σ down?" | 13 Q10 |
| "Semi/anti-join = EXISTS/NOT EXISTS?" | 13 Q8 |
| "Algebra vs SQL set semantics?" | 13 Q15 |
| "Codd's theorem?" | 13 Q13 |
