# Chapter: Normal Forms

## What you'll learn
- **1NF & 2NF**: atomic values, no partial dependencies on the primary key — with precise definitions and worked relations.
- **3NF**: no transitive dependencies, and why the "X→Y with X a superkey OR Y part of a key" relaxation exists.
- **BCNF**: the stricter 3NF — X→Y where X must be a superkey — with the classic cases where 3NF isn't BCNF.
- **4NF & 5NF**: multi-valued dependencies and join dependencies — the exotic normal forms that fix redundancy no FD-based form catches.
- **Decomposition**: lossless-join and dependency-preservation — the *algorithms* and how to prove them.
- **Denormalization**: when and why production systems deliberately leave BCNF for read performance.

## Prerequisites (linked)
- [Chapter 01 (Functional Dependencies)](../chapter-01-functional-dependencies/README.md) — closure and candidate-key finding are required for *every* classification in this chapter.
- Feeds into [Chapter 03 (Practice)](../chapter-03-normalization-practice/README.md).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — 1NF and 2NF](section-01-first-normal-form-1nf-and-second-normal-form-2nf.md) | Atomicity; no partial dependencies on the PK |
| [Section 02 — 3NF](section-02-third-normal-form-3nf.md) | No transitive dependencies; the key-nondeterministic relaxation |
| [Section 03 — BCNF](section-03-boyce-codd-normal-form-bcnf.md) | X→Y where X is a superkey — fixing 3NF's remaining redundancy |
| [Section 04 — 4NF and 5NF](section-04-fourth-and-fifth-normal-forms-4nf-5nf.md) | MVDs, JDs, and why they're rarely needed in practice |
| [Section 05 — Decomposition: Lossless & Dependency Preservation](section-05-decomposition-lossless-join-and-dependency-preservation.md) | The two decomposition properties + algorithms |
| [Section 06 — Denormalization and When to Use](section-06-denormalization-and-when-to-use.md) | Star schemas, materialized aggregations, read-vs-write trade-offs |

## One-paragraph narrative connecting all sections
Normalization is a ladder where each rung forbids one class of bad FD: 1NF forbids non-atomic values, 2NF forbids partial dependencies (fixing redundancy when a composite key exists), 3NF forbids transitive dependencies, BCNF closes the last FD-based gap (every X must be a superkey), and 4NF/5NF attack even subtler *multi-valued* and *join* dependencies. Sections 01-04 define the ladder; Section 05 supplies the engineering: when you decompose to reach 3NF/BCNF, you must preserve the data (lossless join) and the rules (dependency preservation) — and sometimes you can't have both. Section 06 is the reality check: production OLAP schemas *intentionally* denormalize for speed, which is why interviewers ask "why did you leave 3NF?" as a design question, not an error.

## Common interview trap in this chapter
Three classics: (1) saying "it's in 3NF because it has no composite keys" — 3NF/BCNF are defined by *FDs*, not by key shape; test with X→Y where X isn't a superkey. (2) Claiming a relation in 3NF is automatically in BCNF — false; the classic `(student, course, teacher)` case is 3NF but not BCNF. (3) Calling a decomposition "good" without checking lossless join AND dependency preservation — a decomposition that loses an FD is still a decomposition, just a leaky one. Always run the two tests.

## Checklist before moving on
- [ ] I can classify any given relation into its highest normal form in under 2 minutes.
- [ ] I can state the exact definitions: 2NF (no partial dep), 3NF (no transitive dep), BCNF (X→Y ⇒ X superkey).
- [ ] I can give the classic "3NF but not BCNF" example from memory.
- [ ] I can test a decomposition for lossless join (join test) and dependency preservation (projection test).
- [ ] I can explain 4NF/5NF at the concept level (MVD/JD) without the full formalism.
- [ ] I can argue *when* denormalization is justified with a concrete production example.
