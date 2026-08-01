# First Normal Form (1NF) and Second Normal Form (2NF)

> **TL;DR**: 1NF requires every attribute value to be atomic (no lists, sets, or nested structures), and 2NF additionally forbids *partial dependencies* — non-key attributes depending on only part of a composite primary key — the two lowest rungs of the normalization ladder.

## 1. Why Does This Exist?
Normalization starts where SQL itself starts: a relation's attributes must hold *single values*. 1NF exists because relational algebra and SQL are defined over **atomic** values — a cell containing "CS101, CS102" is not addressable, joinable, or indexable. 2NF exists because the moment a table has a *composite key*, some attributes may depend on only part of it — `student(ssn, course_id, student_name, teacher)` has student_name depending on ssn alone, so it repeats on every course the student takes. That repetition is an *update anomaly* (change the name in one row, miss the others). 2NF exists to remove that class of redundancy; 1NF+2NF together say "flat, atomic tables where non-key attributes depend on the *whole* key."

## 2. How Does It Work?
**1NF**: every attribute takes only atomic (single, indivisible) values — no arrays, lists, or nested records in a cell. Fixes: separate tables (child table for the list), a `VALUES`-style normalized child, or (modern) JSON with care — strictly, a relation in 1NF cannot have a list-valued attribute; a JSON *column containing a document* is atomic only if treated as an opaque blob (which forfeits relational semantics).
**2NF**: relation is in 1NF **and** every non-prime attribute (not part of any candidate key) is *fully functionally dependent* on every candidate key — i.e., **no partial dependency** (X→Y where X ⊂ candidate key, Y non-prime). Fix: decompose so each partial dependency becomes a full dependency on its own key — the "extract the partial FD into its own table" move.

## 3. When Is It Used?
- **1NF**: any schema where a column hides multiple values (comma-separated tags, multi-valued "phones", JSON-with-arrays used relationally). The first check in any normalization exercise.
- **2NF**: any composite-key table — enrollment, order lines, bookings — the classic partial-dependency hotspot.
- **Design review**: "why is `student_name` on every enrollment row?" → partial dependency → 2NF fix.
- **Interview screens**: "normalize this to 2NF" is the standard entry-level normalization question.
- **Production**: your *orders/order_items/students/enrollments* table split is precisely the 1NF+2NF discipline applied.

## 4. Why Wasn't Another Approach Chosen?
- **Alternative: allow list-valued attributes (non-1NF).** Rejected: can't reference, index, or join a list element; updates are positional gymnastics; SQL's set operations assume atomic cells. (Modern SQL has arrays/JSON *as extensions*, but using them relationally breaks the model — you opt out of 1NF knowingly, e.g., PostgreSQL ARRAY for read-mostly denormalized data.)
- **Alternative: leave `student_name` on the enrollment table (violating 2NF).** Rejected: update anomalies (rename in one row), insert anomalies (can't add a student without an enrollment), delete anomalies (deleting the last course deletes the name). Decomposing removes all three.
- **Alternative: go straight to 3NF/BCNF without 2NF.** Rejected pedagogically and practically: 2NF is the *minimal* fix for composite-key redundancy; jumping ahead skips a step students need to see, and 3NF's transitive-dependency test builds on "full dependency" which 2NF establishes.
- **Why "normal form" at all?** A normal form is a *testable* property — you can prove a design is 2NF. Without forms, "clean design" is a taste judgment.

## 5. Intuition
1NF is the "**one cell, one value**" rule — the spreadsheet cell can't hold "apple, banana, orange"; it holds one fruit, and other fruits get their own rows. 2NF is the "**don't repeat facts owned by part of the key**" rule — if the key is (student, course) and student_name belongs to *student* alone, then writing it on every (student, course) row means the same fact is stored many times, and updating it means remembering to update every copy. 2NF says: pull each "owned by one key part" fact into its own table, keyed by exactly what owns it. It's the database saying: every fact should be stored once, at the key that truly determines it.

## 6. Real-World Analogy
A **restaurant order ticket**: the ticket key is (table_number, dish). If the ticket also repeated the waiter's *name* on every line item, that's a partial dependency — the waiter belongs to the table, not the dish — so a table's waiter would be repeated once per dish and renaming the waiter means editing every line. 1NF is the rule that a ticket line can't say "2× pizza, 1× pasta" in one cell — each line is one dish. 2NF is the rule that facts like waiter (table-owned) or dish name (dish-owned) live in their own lists — a table card (table → waiter) and a menu (dish → name) — referenced by the ticket, not copied onto it. The restaurant keeps one source of truth per fact; the database should too.

## 7. Formal Definition
(Elmasri & Navathe Ch. 14; Silberschatz Ch. 8; Codd 1971.)
- **1NF**: A relation is in first normal form iff every attribute has an **atomic domain** — each tuple holds a single value per attribute; no repeating groups, no nested relations, no sets/lists as values.
- **Prime attribute**: an attribute that is a member of *any* candidate key. **Non-prime**: not in any candidate key.
- **Full functional dependency**: Y is fully dependent on X iff X→Y and no proper subset X' ⊂ X has X'→Y.
- **Partial dependency**: Y is partially dependent on X iff X→Y but some proper subset X' ⊂ X has X'→Y (Y depends on part of the key).
- **2NF**: R is in 2NF iff R is in 1NF and every **non-prime** attribute is fully functionally dependent on every candidate key — equivalently, **no non-prime attribute is partially dependent on any candidate key**.

## 8. Example
Relation `ENROLL(ssn, course_id, student_name, teacher, grade)` with key {ssn, course_id}:
```
(100, 'DB',   'Alice', 'ProfA', 'A')
(100, 'OS',   'Alice', 'ProfB', 'B')
(101, 'DB',   'Bob',   'ProfA', 'B')
```
- **1NF?** Yes — all values atomic.
- **Partial dependencies**: `ssn → student_name` (student_name depends on ssn ⊂ key) — **partial**. `course_id → teacher` (teacher depends on course_id ⊂ key) — **partial**.
- **Not 2NF**: non-prime attrs student_name and teacher are partially dependent.
- **Redundancy visible**: 'Alice' and 'ProfA' repeated.
- **2NF fix** — decompose into three relations:
  - `STUDENT(ssn, student_name)` — key {ssn}, full deps only.
  - `COURSE(course_id, teacher)` — key {course_id}, full deps only.
  - `ENROLL(ssn, course_id, grade)` — key {ssn, course_id}, grade fully dependent (grade depends on both student and course).
- **Result**: every non-prime attribute now depends on the *whole* key of its table. Update anomalies gone.

## 9. Internal Working
1. **Check 1NF**: scan attributes for set/list/nested values; if found, flatten — either into a child table (the list becomes rows) or by repeating rows (still need unique keys).
2. **Find candidate keys** (closure, Section 02) — identify all candidate keys, not just the declared PK.
3. **Find prime attributes** — union of all candidate keys' members.
4. **Find partial dependencies** — for each FD X→Y (Y non-prime), check whether X ⊂ some candidate key; if yes → partial.
5. **Decompose**: for each partial dependency X→Y, create relation (X, Y) with key X; remove Y from the original; ensure the original still has a key (it does — the original key minus the removed non-prime attrs).
6. **Verify**: the decomposition is lossless (the join on X recovers the original rows) — X is a key of the new relation and remains a foreign key anchor.

## 10. Time Complexity
- **1NF check**: O(n·a) scan of rows×attributes for multi-valued cells (in practice, a schema-level structural check — O(1) per attribute).
- **2NF test**: O(candidate-keys × FDs) closure checks — each closure O(|F|·|R|²); trivial for interview sizes.
- **Decomposition**: O(#partial FDs × |R|) — linear in the number of bad FDs.
- **In production**: no runtime cost — 1NF/2NF are *design-time* properties enforced by schema shape.

## 11. Advantages
- **Addressable cells**: every value can be compared, indexed, joined, aggregated (1NF is the price of SQL).
- **No composite-key redundancy**: each fact stored once, owned by the right key (2NF).
- **Anomaly elimination**: update/insert/delete anomalies from partial dependency disappear.
- **Simpler queries**: no string-splitting or "first element" logic; joins are natural.
- **Foundational**: every higher form assumes 1NF+2NF; the ladder is clean.

## 12. Disadvantages
- **1NF can be verbose**: flattening lists adds rows and joins; for *read-only* nested data (tags, JSON), the denormalized form is often faster (a deliberate trade).
- **2NF only fixes partial dependency**: it says nothing about transitive dependency (that's 3NF) — so 2NF alone can still hide redundancy.
- **Composite keys proliferate**: full decomposition can create many small tables and join-heavy queries (trade-off vs denormalization).
- **Not a design end-state**: production systems usually target 3NF/BCNF; 1NF/2NF are steps, not goals.

## 13. Interview Questions
1. **Q: What is 1NF?** A: Every attribute holds only atomic (single, indivisible) values — no lists, sets, arrays, or nested structures in a cell. The price of SQL's relational semantics (addressable, joinable, indexable values).
2. **Q: Why must 1NF hold?** A: Because relational algebra and SQL operate on single values: you can't join on, filter, or index an element inside a comma-separated cell. Non-atomic cells break every set operation.
3. **Q (tricky): Is a JSON column in PostgreSQL a 1NF violation?** A: Depends on intent: if the JSON is treated as an opaque atomic value (stored/retrieved whole), it *is* atomic — arguably 1NF-ok but not relational. If you query *inside* it (jsonb_path, indexing sub-fields), you've opted out of 1NF semantics deliberately. State the distinction.
4. **Q: What is a partial dependency?** A: X→Y where X is a *proper subset* of a candidate key and Y is a non-prime attribute — the attribute depends on only part of the key. E.g., `ssn → student_name` in ENROLL(ssn, course_id, ...).
5. **Q: What is 2NF?** A: 1NF + every non-prime attribute is *fully* functionally dependent on every candidate key — i.e., no partial dependency of a non-prime attribute on any candidate key.
6. **Q (scenario): Is ENROLL(ssn, course_id, student_name, teacher, grade) in 2NF?** A: No — `ssn → student_name` and `course_id → teacher` are partial dependencies (non-prime attributes depend on parts of the composite key). Decompose into STUDENT(ssn, name), COURSE(course_id, teacher), ENROLL(ssn, course_id, grade).
7. **Q: What is a prime vs non-prime attribute?** A: Prime = member of any candidate key; non-prime = in no candidate key. 2NF/3NF constraints apply to *non-prime* attributes (keys can do anything).
8. **Q: Why is the partial dependency on *composite keys* the real 2NF trigger?** A: Partial dependency requires a subset of a key — which only exists if a key has 2+ attributes. Single-attribute-key tables are automatically 2NF (nothing is a proper subset of the key). That's why 2NF is a *composite-key* phenomenon.
9. **Q: What anomalies does 2NF fix?** A: Update anomaly (rename a student in one enrollment row — others stay stale), insert anomaly (can't add a student without enrolling them), delete anomaly (deleting their last course deletes their name). Decomposition removes all three.
10. **Q (production): You see the same `teacher` repeated across many rows with same `course_id`. What's the diagnosis?** A: Partial dependency `course_id → teacher` (assuming one teacher per course) in a composite-key table — 2NF violation. Fix: split COURSE(course_id, teacher) out; join when needed.
11. **Q: Normalize `ORDERS(order_id, product_id, customer_name, product_price)` to 2NF.** A: Key {order_id, product_id}. Partial deps: `order_id → customer_name`, `product_id → product_price`. Decompose: ORDERS(order_id, customer_name), PRODUCT(product_id, product_price), ORDER_ITEMS(order_id, product_id). All three in 2NF.
12. **Q (tricky): A single-attribute-key table has duplicated data. Can it be a 2NF problem?** A: No — with a single-attribute key there are no partial dependencies (no proper key subsets), so it's automatically 2NF (if 1NF). Duplication there is a *transitive* or *denormalization* issue (3NF/design), not 2NF.
13. **Q: How do you find partial dependencies systematically?** A: (1) Find all candidate keys (closure); (2) list all FDs X→Y with Y non-prime; (3) check each X against every candidate key: X ⊂ key and X ≠ key → partial. Then decompose each offender.
14. **Q (scenario): A table is in 1NF but has `course_id → teacher`. Is it necessarily violating 2NF?** A: Only if there's a composite candidate key for which course_id is a proper subset. If the key is just {course_id}, then `course_id → teacher` is *full* (X = key) and 2NF is fine (3NF/BCNF questions come later). The 2NF test is key-relative.
15. **Q: What does "fully functionally dependent" mean vs "partially"?** A: Y is fully dependent on X iff X→Y and no proper subset of X determines Y. Partially dependent = some proper subset does. 2NF bans the latter for non-prime Y.
16. **Q (production): Should production OLAP schemas be in 2NF?** A: Rarely — warehouses deliberately denormalize for reads (star schemas, Section 06). 2NF discipline governs *OLTP* (write-correctness); OLAP trades it for query speed consciously.
17. **Q: How do you verify a 1NF violation in a live table?** A: Schema-level: check for array/text columns containing delimiters; a "contains list" check via `POSITION(',', col) > 0` finds comma-list columns. Real fix is schema redesign (child table), not data scrubbing.
18. **Q (hard): Can a relation be in 2NF but still have huge redundancy?** A: Yes — 2NF only kills *partial* dependency. Transitive dependencies (dept_id → dept_name with emp_id → dept_id) survive 2NF — that's 3NF's job. Always continue the ladder.
19. **Q: What's the relationship between 1NF/2NF and real-world "flat file" data?** A: Spreadsheets/CSVs with repeated groups (one cell = "CS101;OS;DB") and column-repeated facts are precisely 1NF/2NF violations; the normalization steps are the "convert this spreadsheet to a proper database" playbook interviewers love.
20. **Q (scenario): Design a 2NF schema for "students take courses, each course has one teacher, each student has one name."** A: STUDENT(ssn, name), COURSE(course_id, teacher), ENROLL(ssn, course_id, grade). Note: this is also 3NF/BCNF here — but 2NF is where the composite-key work happens; 3NF handles the teacher-of-course (already fully keyed).

## 14. Follow-Up Questions
1. **Q: Why is 2NF often "skipped" in interviews?** A: Because many interview relations have single-attribute keys (auto-2NF), so interviewers jump to 3NF/BCNF. But when a composite key appears, 2NF is the test they expect. Know both, answer per-key-shape.
2. **Q: Does normalization ever produce a *worse* design?** A: For write-heavy OLTP, almost never. For read-heavy analytics, sometimes — joins cost more than the redundancy saved. That's the denormalization trade (Section 06).
3. **Q: What happens if a partial dependency is left in place?** A: Redundancy persists and update anomalies bite in production (rename = multi-row updates, missed = inconsistency). It "works" until it silently corrupts.
4. **Q: Are arrays in Postgres always a 1NF violation?** A: Only if you use them relationally (filter/join on elements). Used as opaque blobs, they're atomic values. The violation is a *usage* decision, not a syntax.
5. **Q: What is the "repeating group" concept in 1NF?** A: A group of attributes repeated per entry (e.g., phone1, phone2, phone3 columns, or a single cell with a list). 1NF forbids both; the fix is a child table (normalization) or an array column (denormalization).

## 15. Coding Example
```sql
-- 1NF violation: a single cell holding a list
CREATE TABLE bad_1nf (student_id INT PRIMARY KEY, courses TEXT);
INSERT INTO bad_1nf VALUES (1, 'CS101;OS;DB');   -- non-atomic cell

-- 1NF fix: child table (rows, not lists)
CREATE TABLE enrollment_1nf (
  student_id INT, course_id TEXT, PRIMARY KEY (student_id, course_id)
);

-- 2NF violation: composite key, partial dependencies
CREATE TABLE bad_2nf (
  ssn INT, course_id TEXT,
  student_name TEXT,      -- depends on ssn alone  (partial)
  teacher TEXT,           -- depends on course_id alone (partial)
  grade TEXT,             -- fully dependent on (ssn, course_id)
  PRIMARY KEY (ssn, course_id)
);

-- 2NF fix: three relations, each fully keyed
CREATE TABLE student (ssn INT PRIMARY KEY, student_name TEXT);
CREATE TABLE course  (course_id TEXT PRIMARY KEY, teacher TEXT);
CREATE TABLE enroll  (
  ssn INT REFERENCES student(ssn),
  course_id TEXT REFERENCES course(course_id),
  grade TEXT,
  PRIMARY KEY (ssn, course_id)
);
-- Now 'Alice' and 'ProfA' exist exactly once each.
```

## 16. Industry Usage
- **Every OLTP schema** (e-commerce, banking, SaaS) is effectively 1NF+2NF+3NF: order_lines and enrollments are the composite-key tables 2NF shaped.
- **ORM models** (Prisma/Hibernate/Django) map these decomposed tables to objects; the "many-to-many join table" is 2NF's canonical output.
- **Data cleaning pipelines** convert 1NF-violating CSVs (pivoted/repeated-group Excel exports) into normalized models — the "tidy data" (Wickham) movement is 1NF for statistics.
- **Warehouses** trade 2NF for star schemas deliberately — but the *raw/source* layers still store 2NF-clean data before marts denormalize.
- **Interview panels** at Amazon/Google/Meta use 2NF precisely because it forces composite-key reasoning — the differentiator between memorized definitions and real understanding.

## 17. References
- Elmasri & Navathe, *Fundamentals of Database Systems*, 7th ed., Ch. 14 (Normalization; 1NF, 2NF).
- Silberschatz, Korth & Sudarshan, *Database System Concepts*, 7th ed., Ch. 8.1 (Normal Forms).
- Codd, E. F., "Further Normalization of the Data Base Relational Model", 1971.
- Date, C. J., *An Introduction to Database Systems*, 8th ed., Ch. 11-12.
- Kent, W., "A Simple Guide to Five Normal Forms in Relational Database Theory", CACM 1983.

## 18. Cheat Sheet
- 1NF = atomic values: one cell, one value; no lists/nested/repeating groups.
- Prime = in some candidate key; non-prime = in none.
- Partial dependency = X→Y with X ⊂ candidate key, Y non-prime.
- 2NF = 1NF + no partial dependency of any non-prime attribute.
- 2NF only matters for composite keys (single-attr keys are auto-2NF).
- Fix: decompose each partial FD into its own (X, Y) table.
- 2NF removes update/insert/delete anomalies.
- 2NF ≠ no redundancy — transitive deps survive (3NF's job).

## 19. Quiz
1. 1NF requires: a) no transitive deps b) atomic values c) single-attr keys d) BCNF → **b**
2. A partial dependency is: a) X→Y, X ⊂ key, Y non-prime b) X→Y, X = key c) Y⊆X d) X→→Y → **a**
3. A table with a single-attribute PK is automatically: a) 3NF b) 2NF (given 1NF) c) BCNF d) 4NF → **b**
4. Prime attribute =: a) in every key b) in some candidate key c) non-null d) indexed → **b**
5. `ssn → student_name` in ENROLL(ssn, course_id, student_name) is: a) full b) partial c) trivial d) transitive → **b**
6. 2NF fixes: a) transitive deps b) partial deps c) MVDs d) JDs → **b**
7. Deleting a student's last course deletes their name = : a) update anomaly b) delete anomaly c) insert anomaly d) deadlock → **b**
8. A JSON column used relationally: a) always 1NF b) opts out of 1NF semantics c) 3NF d) 4NF → **b**
9. The 2NF fix for `course_id → teacher`: a) add course to key b) decompose COURSE(course_id, teacher) c) drop teacher d) add teacher to key → **b**
10. 2NF alone can still have: a) transitive redundancy b) no redundancy c) MVDs only d) no anomalies → **a**

## 20. Flashcards
- **Q: 1NF definition?** → **A:** Every attribute value is atomic — no lists, sets, or nested structures.
- **Q: Partial dependency?** → **A:** X→Y where X is a proper subset of a candidate key (Y non-prime).
- **Q: 2NF definition?** → **A:** 1NF + no non-prime attribute partially depends on any candidate key.
- **Q: When does 2NF matter?** → **A:** Composite keys — single-attr keys are auto-2NF.
- **Q: Prime attribute?** → **A:** Member of some candidate key.
- **Q: 2NF fix?** → **A:** Decompose each partial FD into its own (X, Y) table.
- **Q: What anomalies does 2NF fix?** → **A:** Update/insert/delete anomalies from partial dependency.
- **Q: What survives 2NF?** → **A:** Transitive dependencies — 3NF's problem.

## 21. Revision
1NF = atomic cells (no lists/nested — the price of SQL semantics). Prime = in some candidate key; non-prime = not. **Partial dependency** = X→Y, X a proper subset of a candidate key, Y non-prime. **2NF** = 1NF + no partial dependency of non-prime attributes. Only matters for composite keys (single-key tables auto-2NF). Fix = decompose each partial FD into its own (X,Y) table; the classic result is STUDENT / COURSE / ENROLL split. 2NF kills update/insert/delete anomalies but *not* transitive redundancy (that's 3NF). Interview moves: spot `ssn → name` in a composite-key table instantly; explain why single-key tables are auto-2NF; and always continue to 3NF/BCNF after the 2NF fix.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is 1NF?" | 7 / 13 Q1-3 |
| "What is a partial dependency?" | 13 Q4 |
| "What is 2NF / is this in 2NF?" | 13 Q5-6 |
| "Prime vs non-prime attribute?" | 13 Q7 |
| "Normalize ORDERS/ENROLL to 2NF" | 13 Q10-11 |
| "Single-key tables auto-2NF?" | 13 Q8, Q12 |
| "Anomalies 2NF fixes?" | 13 Q9 |
| "Can 2NF still be redundant?" | 13 Q18 |
