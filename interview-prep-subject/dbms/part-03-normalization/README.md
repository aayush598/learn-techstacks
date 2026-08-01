# Part: Normalization

## What this part covers
The **theory of good schema design** — the difference between a schema that survives 5 years of production and one that rots into duplicate, contradictory rows. It covers functional dependencies and how to reason about them (Armstrong's axioms, closure, candidate keys), the normal forms (1NF → BCNF → 4NF/5NF) with their precise, exam-able definitions, lossless-join & dependency-preserving decomposition, and finally denormalization: when you deliberately *break* the rules because reads beat writes. This is where interviewers probe whether you *understand* design trade-offs, not just memorize definitions.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Functional Dependencies | FDs in depth, Armstrong's axioms & closure of attribute sets | Find all FDs in a relation, prove closure with pseudocode, find all candidate keys from FDs |
| ch-02 Normal Forms | 1NF & 2NF, 3NF, BCNF, 4NF & 5NF, decomposition (lossless & dependency preserving), denormalization | Classify any relation into its highest normal form, prove 2NF (no partial deps) / 3NF (no transitive deps) / BCNF (X→Y where X is superkey), decompose with the correct algorithm, argue when to denormalize |
| ch-03 Normalization Practice | Normalization interview questions & problems | Solve 15+ step-by-step normalization problems under time pressure |

## Study order
1. **ch-01** first — every normal form is *defined* in terms of functional dependencies, so FDs are non-negotiable.
2. **ch-02** second — go form by form; each builds on the previous (2NF fixes part of 1NF, 3NF fixes 2NF, BCNF refines 3NF, 4NF/5NF fix MVDs/JDs).
3. **ch-03** last — drill problems until classification is instant and automatic.
Read every section in numbered order within a chapter; each section assumes the previous one.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐ (4/5)** — a guaranteed 1-2 questions in most DBMS rounds, and a *favorite screener*: "Is this relation in 3NF?" is easy to ask and instantly separates people who memorized from people who understood.
- **Emphasized by**: **Google, Amazon, Microsoft, Meta** (system design follow-ups: "your schema — is it normalized? why not?"), **data-engineering shops** (Snowflake, Databricks, dbt ecosystems) that live in star schemas, and **all DB core teams**.
- Typical asked: "define 3NF", "is this in BCNF?", "why did you denormalize the orders table?", "is this decomposition lossless?".

## How the parts connect (roadmap)
- Uses **Part 02's** keys and relation vocabulary as raw material.
- **Part 04 (Indexing)** frequently pairs with denormalization — you denormalize for read speed, you index for read speed.
- Later **transaction/concurrency** parts assume your schema has integrity (constraints from Part 02, normal forms here) so that concurrent writes stay consistent.
- **System design interviews** reuse this part's star-schema/denormalization reasoning for OLAP vs OLTP.
