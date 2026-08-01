# Part: NoSQL Databases & Interview Question Bank

## What this part covers (TL;DR)
- **NoSQL databases** — why they exist, the four major families (key-value, document, wide-column/columnar, graph), how each trades ACID/consistency for scale, and a decision guide for when to use SQL vs NoSQL.
- **A comprehensive interview question bank** — 100+ curated questions with answers, system-design scenarios, SQL coding challenges, company-specific questions, and a crash-course revision guide tying the entire DBMS syllabus together.

## Chapter map
| Chapter | Focus | Sections |
|---|---|---|
| 01 — NoSQL Overview & Types | The NoSQL landscape | 01 NoSQL Overview & Types, 02 Key-Value & Document Stores, 03 Wide-Column & Columnar, 04 Graph Databases, 05 SQL vs NoSQL Decision Guide |
| 02 — Interview Question Bank | Everything that gets asked | 01 Top 100 Questions, 02 System Design, 03 SQL Coding Challenges, 04 Company-specific, 05 Crash-course Revision |

## Study order
1. **Chapter 01, Section 01** first — the taxonomy and trade-offs (CAP, PACELC, ACID vs BASE) frame everything.
2. Sections 02-04 — the four families: pick two to go deep (Key-Value + Document and Wide-Column are the most common in interviews).
3. Section 05 — the SQL vs NoSQL decision guide; this is where "should we use Mongo here?" questions live.
4. **Chapter 02, Section 01** — Top 100 Q&A; use it to self-test all of Part 01-08.
5. Sections 02-04 — scenario/coding/company practice.
6. Section 05 — the crash-course revision; run it 24-48h before the interview.

## Interview importance
- NoSQL: **High** — "MongoDB vs PostgreSQL?", CAP, eventual consistency, document modeling appear constantly in backend interviews; knowing *why* a family exists (read/write patterns, horizontal scaling) is what separates candidates.
- Question bank: **Critical** — the whole point of this repo; the 100 questions span every earlier part and give you a rehearsable answer key.
- System design (Section 02): **High** — the DBMS parts of "design X" interviews (sharding, caching, consistency) are concentrated here.
- SQL coding (Section 03): **Very High** — most companies give a live SQL round; these are realistic take-home-style problems with optimized solutions.

## How the parts connect
- Parts 01-04 (fundamentals, relational model, normalization, indexing) give the *relational* baseline; Part 08's NoSQL chapters exist *in contrast* to that baseline.
- Parts 05-06 (transactions, concurrency, recovery) supply the ACID/consistency vocabulary that NoSQL relaxes — you can't explain "eventual consistency" without understanding "isolation".
- Part 07 (query processing/optimization) explains why SQL engines do the hard lifting; NoSQL trades that generality for scale/simplicity.
- The Interview Question Bank (Chapter 02) closes the loop on *every* prior part — it's the final synthesis and your exam-day artifact.
