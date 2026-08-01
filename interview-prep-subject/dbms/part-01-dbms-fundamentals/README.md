# Part: DBMS Fundamentals

## What this part covers
Everything you need to survive the **first five minutes of any DBMS interview**: what a database and a DBMS actually are, why data outgrew file systems, how a database is architected (external/conceptual/internal layers), the data models that have existed and why the relational one won, and the internal anatomy of a DBMS (components, data dictionary, languages, client-server topology, database users). This part gives you the vocabulary every later part — SQL, normalization, indexing, transactions — assumes you already have.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Introduction to Databases | What is a database & why DBMS, three-schema architecture, data models (hierarchical/network/relational/object), file system vs DBMS | Define DB/DBMS in one sentence, draw the 3-schema architecture and explain data/instance/schema, compare data models, list why file systems fail |
| ch-02 DBMS Architecture | Components & architecture, data dictionary & metadata, DDL/DML/DCL/TCL, client-server architecture & database users | Draw the DBMS component block diagram, explain the catalog's role, classify the 4 SQL language families, name the 6 database user roles |

## Study order
1. **ch-01** first — it builds the *why*: the pain (file systems) that created the DBMS, and the core abstraction (schema over data) everything else uses.
2. **ch-02** second — now you know *what* a DBMS is, learn *how it is built*: components, catalog, languages, and who uses it.
Read every section in numbered order within a chapter; each section assumes the previous one.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐ (3/5)** — low *difficulty* but extremely high *frequency*: "What is a DBMS? / Why not a file system?" is often the very first DBMS question, and the three-schema architecture is a favorite follow-up.
- **Emphasized by**: every backend/data interview (Amazon, Google, Microsoft, Meta) as warm-up; **data-platform teams** (Snowflake, Databricks, MongoDB, Postgres/Mongo core) treat this part as 4-5 stars because they want you to speak the vocabulary of data independence.
- Typical asked: "DBMS vs file system", "three-schema architecture", "what is the difference between schema, instance and state?", "DML vs DDL".

## How the parts connect (roadmap)
- Part 01 is the **foundation**: it defines data, schema, DBMS, and the layered architecture.
- **Part 02 (Relational Model & SQL)** is exactly what Parts 01's relational model + DDL/DML chapters promised: the concrete algebra and SQL on top of relations.
- **Part 03 (Normalization)** answers the design question Part 01 raised implicitly — *how do I design good schemas?* — using functional dependencies.
- **Part 04 (Indexing & File Organization)** explains the physical layer that Part 01's "internal schema" mentioned: how rows are stored and found.
- Later parts (transactions, concurrency, recovery, distributed) will explain the components of Part 01's architecture diagram in depth.
