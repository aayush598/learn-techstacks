# Chapter: DBMS Architecture

## What you'll learn
- The internal anatomy of a DBMS: the component block diagram (query processor, storage manager, transaction manager, buffer manager, metadata manager) and how a query flows through it.
- The data dictionary / system catalog: what it stores, why the DBMS *itself* depends on it, and who can read/write it.
- The four SQL language families (DDL, DML, DCL, TCL) with real commands for each, and the design decision behind separating them.
- Client-server architecture in DBMS (why it won over terminal-mainframe and file-server models), the tiers (2-tier, 3-tier), and the six roles of database users from casual to DBA.

## Prerequisites (linked)
- [Chapter 01 (Introduction to Databases)](../chapter-01-introduction-to-databases/README.md) — this chapter dissects the DBMS that Chapter 01 defined.
- Feeds into [Part 02 (Relational Model & SQL)](../../part-02-relational-model-and-sql/README.md), which makes the DDL/DML languages from Section 03 concrete.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — DBMS Components and Architecture](section-01-dbms-components-and-architecture.md) | The block diagram: query processor, storage manager, transaction manager; the query path |
| [Section 02 — Data Dictionary and Metadata](section-02-data-dictionary-and-metadata.md) | The catalog tables, `pg_catalog`/`information_schema`, who maintains and reads them |
| [Section 03 — DBMS Languages: DDL, DML, DCL, TCL](section-03-dbms-languages-ddl-dml-dcl-tcl.md) | The 4 language families, commands, and why separation of concerns matters |
| [Section 04 — Client-Server Architecture and Database Users](section-04-client-server-architecture-and-database-users.md) | 1/2/3-tier models, why client-server won, the 6 user roles |

## One-paragraph narrative connecting all sections
A DBMS is a software stack, and this chapter is its anatomy (Section 01): a query arrives at the query processor, is parsed, optimized, and executed by the storage manager against disk pages managed by the buffer manager. For the optimizer to work it needs to know what exists — tables, columns, indexes, users — and that knowledge lives in the system catalog, the database's self-describing metadata (Section 02). Humans talk to this machine through a set of languages, partitioned into DDL (structure), DML (data), DCL (permissions), and TCL (transactions) so that each concern can be scoped, secured, and audited independently (Section 03). The whole thing is physically deployed as a client-server system — the server owns the data and each client talks to it over a protocol — and the people touching it range from naive end-users to DBAs, each needing different powers (Section 04). Every later part (SQL execution, transactions, recovery, distributed systems) is a zoom-in on a component from this chapter.

## Common interview trap in this chapter
Candidates answer "what is a data dictionary?" with "a dictionary of data" — too vague. The catalog is *data about the schema* (metadata): table names, column types, constraints, indexes, and privileges. It is the reason the DBMS is **self-describing** — the DBMS reads its own catalog to optimize and enforce integrity. Also, "DDL vs DML" gets muddled: DDL changes *structure* (schema), DML changes *rows* (data). `ALTER TABLE` is DDL; `UPDATE` is DML. Get both crisp.

## Checklist before moving on
- [ ] I can draw the DBMS component diagram and trace one query through every box.
- [ ] I can name 5 things stored in the system catalog and explain self-description.
- [ ] I can classify 10 real commands into DDL/DML/DCL/TCL without hesitation.
- [ ] I can explain why client-server replaced file-server and mainframe models.
- [ ] I can name all 6 database user roles and one responsibility of each.
- [ ] I can describe the 2-tier vs 3-tier trade-off for a web application.
