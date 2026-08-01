# Chapter: Interview Question Bank

## What you'll learn
- **Top 100 DBMS interview questions**: every classic — ACID, transactions, isolation, indexing, B-trees, normalization, joins, EXPLAIN, recovery, NoSQL — with crisp answer keys you can rehearse.
- **DBMS system-design questions**: how the database pieces of "design Twitter / design an e-commerce checkout / design a ride-hailing app" are answered (sharding, caching, consistency, replication).
- **SQL coding challenges**: realistic take-home/live problems with optimized, commented solutions and the "trap" each one tests.
- **Company-specific questions**: what differentiates the DBMS rounds at major companies.
- **A crash-course revision guide**: the entire syllabus condensed to a revisable, high-signal artifact for the 24-48 hours before an interview.

## Prerequisites (linked)
- All of Parts 01-08 — this chapter is the *synthesis*; each question maps back to a specific part/section.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Top 100 DBMS Interview Questions](section-01-top-100-dbms-interview-questions-and-answers.md) | What are the must-know questions and their answers? |
| 02 | [DBMS System Design Questions](section-02-dbms-system-design-questions.md) | How do you answer the database half of design interviews? |
| 03 | [SQL Coding Challenges](section-03-sql-coding-challenges-and-solutions.md) | What do live/take-home SQL rounds actually test? |
| 04 | [Company-specific DBMS Questions](section-04-company-specific-dbms-questions.md) | What differs by company and how do you prepare? |
| 05 | [DBMS Crash-course Revision](section-05-dbms-crash-course-revision.md) | How do I review the whole syllabus fast? |

## One-paragraph narrative connecting all sections
Everything before this chapter built the concepts; this chapter turns them into *interview fluency*. Section 01 is the core: 100 questions spanning fundamentals, normalization, indexing, transactions, recovery, query processing, and NoSQL — each with a tight answer you can say out loud, plus difficulty tiers so you can target your level. Section 02 applies it to *design*: real "design X" problems where the database is 40% of the answer (sharding, caches, consistency choices, replication topology) — answered with the vocabulary from Parts 04-08. Section 03 is the hands-on round: SQL coding challenges that test window functions, recursion, gaps-and-islands, and index-awareness — the traps interviewers plant. Section 04 surveys how companies differentiate (search/graph at some, distributed consistency at others, heavy SQL at finance). Section 05 closes with the crash course: the entire syllabus reduced to a dense, high-signal revision sheet organized by the 8 parts — the artifact you run 24-48h before the interview, backed by the 100 questions as your rehearsal script.

## Common interview trap in this chapter
**Trap:** Memorizing *answers* instead of *reasoning*. Interviewers hear the same ACID recitation from everyone; what differentiates candidates is the *why* — "read committed stops dirty reads but allows non-repeatable reads *because* each statement sees a new snapshot," or "a covering index avoids the heap fetch because all needed columns live in the index leaves." This chapter's answers are written to be *rehearsed aloud* (say them, don't just read them), and the "trap" callouts mark where candidates most often slip (index vs scan, LWW loss, work_mem per-operation, CAP during partitions). Also: don't skip Section 05 — a coherent one-pass revision beats scattered deep-dives when interview day arrives.

## Checklist before moving on
- [ ] I can answer 100 core DBMS questions aloud without notes.
- [ ] I can structure a "design a database for X" answer (patterns → consistency → sharding → cache).
- [ ] I can solve SQL challenges including window functions, recursion, and gaps-and-islands.
- [ ] I know the company-specific angles relevant to my targets.
- [ ] I can run the crash-course revision in under two hours.
