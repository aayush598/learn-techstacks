# Chapter: Introduction to Databases

## What you'll learn
- The precise, defensible definitions of *data*, *database*, *schema*, *instance/state*, and *DBMS* — the vocabulary interviewers assume you have.
- Why databases exist: the four concrete pains of file systems (redundancy, inconsistency, no concurrency control, no atomicity) that created the DBMS.
- The three-schema architecture (external / conceptual / internal) and why *data independence* is its whole point — including the distinction between logical and physical data independence.
- The history of data models (hierarchical, network, relational, object) and the exact reasons the relational model won.
- A clear file-system-vs-DBMS comparison table you can rattle off under pressure.

## Prerequisites (linked)
- None. This is the entry point to DBMS. A working knowledge of what "data" means in any CS101 context is enough.
- Continues into [Chapter 02 (DBMS Architecture)](../chapter-02-dbms-architecture/README.md) and the rest of [Part 01](../README.md).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — What is a Database and Why DBMS](section-01-what-is-a-database-and-why-dbms.md) | DB vs DBMS, schema vs instance, the 4 file-system pains, DBMS's 8 jobs |
| [Section 02 — Database Architecture and Three-Schema Architecture](section-02-database-architecture-and-three-schema-architecture.md) | The 3 levels, mappings, and logical vs physical data independence |
| [Section 03 — Data Models: Hierarchical, Network, Relational, Object](section-03-data-models-hierarchical-network-relational-object.md) | Every major data model, its structure, and why relational won |
| [Section 04 — File System vs DBMS](section-04-file-system-vs-dbms.md) | The side-by-side comparison and the DBMS advantages (ACID, concurrency, security, recovery) |

## One-paragraph narrative connecting all sections
A database exists because application data became too big, too shared, and too valuable to keep in files (Section 01 defines the terms and the pain). The answer to "how do we structure the data so apps don't break when the physical layout changes?" is the three-schema architecture, which separates what users see from what is physically stored (Section 02). What sits between the schemas is a *data model* — a way of structuring data — and the relational model, with its simple table metaphor and set semantics, beat trees (hierarchical) and graphs (network) for most workloads (Section 03). The final payoff is the DBMS itself, a layer that gives you ACID, concurrency, security, and recovery for free — the things a file system simply cannot (Section 04). Everything in the rest of the DBMS course is one of these four ideas expanded.

## Common interview trap in this chapter
Candidates conflate **schema** with **instance/state**. Schema is the *blueprint* (table structure) — it changes rarely. Instance is the *data* at a moment — it changes every second. Interviewees also say "DBMS = database" — they are not the same: the *database* is the data; the *DBMS* is the software managing it (MySQL is a DBMS, the rows in `employees` are the database). Name both distinctions explicitly and you've cleared the trap.

## Checklist before moving on
- [ ] I can define database, DBMS, schema, instance, and metadata in one sentence each.
- [ ] I can name the 4 file-system problems and map each to a DBMS feature.
- [ ] I can draw the three-schema architecture and give one real example for each level.
- [ ] I can explain logical vs physical data independence with a concrete scenario.
- [ ] I can compare hierarchical/network/relational/object models and say why relational won.
- [ ] I can give 5+ reasons DBMS beats file system, with a file-system counterexample for each.
