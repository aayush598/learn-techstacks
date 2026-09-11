# Dbms — Database Basics Interview Questions and Answers

## Q1: What is a database and a DBMS?
**A:** A database is an organised collection of data; a DBMS is software to create, manage, query, and secure databases (e.g., PostgreSQL, MySQL). It enforces constraints, transactions, and concurrency.

## Q2: What is the difference between a database and a DBMS?
**A:** Database = the stored data itself; DBMS = the software system managing the data (storage, retrieval, integrity, concurrency). One DBMS can manage many databases.

## Q3: What is a relational database?
**A:** A database storing data in tables (relations) with rows (tuples) and columns (attributes), linked by keys, queried with SQL, guaranteed by ACID transactions — e.g., PostgreSQL.

## Q4: What is a NoSQL database? Give types.
**A:** Non-relational, schema-flexible, horizontally scalable stores: document (MongoDB), key-value (Redis), columnar (Cassandra), graph (Neo4j). Chosen for scale/velocity/flexibility.

## Q5: What is a primary key?
**A:** A column (or combination) that uniquely identifies each row — non-null and unique. It is the relational backbone for foreign-key references and fast lookup.

## Q6: What is a foreign key?
**A:** A column referencing the primary key of another table, enforcing referential integrity — ensuring a child row always points at an existing parent.

## Q7: What is a candidate key vs super key?
**A:** Super key: any set of columns that uniquely identifies rows. Candidate key: a minimal super key (no column can be removed). Primary key = chosen candidate key.

## Q8: What is a composite key?
**A:** A primary/unique key formed by two or more columns jointly identifying a row (e.g., (student_id, course_id) in enrollment).

## Q9: What is a unique key vs primary key?
**A:** Both enforce uniqueness; primary key is non-null and only one per table; unique keys allow a single NULL, and a table may have several.

## Q10: Explain entity, attribute, and relationship.
**A:** Entity = a thing stored in its own table; attribute = a property column; relationship = an association (one-to-one, one-to-many, many-to-many).

## Q11: What is a view in SQL?
**A:** A virtual table defined by a stored SELECT query. It presents a logically filtered/projected subset without duplicating data, hiding complexity and enforcing row/col security.

## Q12: Data types: INT, VARCHAR, DATE — when to use each?
**A:** INT for whole numbers/counter keys; VARCHAR(n) for bounded variable text; DATE/TIMESTAMP for time-based logic. Choose the tightest correct type to save storage and index size.

## Q13: What is the difference between TRUNCATE and DELETE?
**A:** TRUNCATE removes all rows quickly by deallocating pages, can't be filtered, resets identity, and is not per-row logged like DELETE; DELETE is DML, filterable, with WHERE and triggers.

## Q14: What is a DROP vs DELETE vs TRUNCATE?
**A:** DROP removes the whole table (structure+data) permanently; TRUNCATE empties the data quickly, keeps structure; DELETE removes specific rows and can be rolled back with a transaction.

## Q15: What is data integrity?
**A:** Correctness and consistency guaranteed by constraints: entity (PK), referential (FK), domain (types/CHECK), user-defined — the DBMS enforces them on write.

## Q16: How does PostgreSQL differ from SQLite?
**A:** PostgreSQL is a client-server DB with advanced features (full-text, JSONB, MVCC, extensive indexing, concurrency); SQLite is an embedded file-based engine — zero admin, single-file, lighter concurrency.

## Q17: What is a snapshot isolation / MVCC at a high level?
**A:** Multi-version concurrency control gives each reader a consistent snapshot of committed data without locks — writers don't block readers; PostgreSQL uses this.

## Q18: What is database connection pooling?
**A:** Reusing a cache of open DB connections rather than creating/freeing them per request — dramatically reduces latency and server load in API backends.

## Q19: What is an ORM and why use it?
**A:** A library mapping tables to objects (SQLAlchemy, Django ORM) so application code uses Python objects instead of raw SQL strings — safer, portable, but must watch for N+1.

## Q20: What is the N+1 query problem?
**A:** Loading a collection, then fetching one extra query per row (N queries) instead of one joined query — a classic performance trap; solve with eager loading/joins.

## Q21: Explain database normalization in one sentence.
**A:** Organising schema to minimise redundancy and dependency anomalies by splitting tables according to normal forms — a central Infosys DBMS question.

## Q22: What is denormalization and when is it used?
**A:** Intentionally merging/duplicating data to reduce JOINs or reads at scale (reporting, caching) — trading write overhead and consistency for read speed.

## Q23: What is a stored procedure?
**A:** Precompiled SQL logic stored and executed on the server (loops, transactions, business checks) — reduces network chatter and centralises rules.

## Q24: What is a trigger?
**A:** Server-side code automatically executed on INSERT/UPDATE/DELETE events — used for audits, cascades, and integrity constraints without app changes.

## Q25: What is a transaction?
**A:** A unit of work executed atomically with ACID guarantees (BEGIN...COMMIT/ROLLBACK) — the fundamental safety unit a bank transfer demonstrates.

## Q26: Define 01 database basics in one line and then expand with a real-world example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q27: Why is 01 database basics important in real production systems?
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q28: What are the advantages and disadvantages of 01 database basics?
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q29: Compare 01 database basics with alternatives and state when to prefer which.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q30: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q31: What common misconceptions exist about 01 database basics?
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q32: How would you test correctness of a system that relies on 01 database basics?
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q33: Describe 01 database basics as if explaining to a new hire.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q34: How does 01 database basics interact with performance (time/space trade-off)?
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q35: What would you change about how 01 database basics is taught, based on your experience?
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q36: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q37: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q38: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q39: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q40: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q41: What common misconceptions exist about 01 database basics? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q42: How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q43: Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q44: How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q45: What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q46: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q47: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q48: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q49: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q50: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q51: What common misconceptions exist about 01 database basics? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q52: How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q53: Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q54: How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q55: What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q56: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q57: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q58: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q59: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q60: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q61: What common misconceptions exist about 01 database basics? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q62: How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q63: Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q64: How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q65: What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q66: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q67: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q68: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q69: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q70: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q71: What common misconceptions exist about 01 database basics? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q72: How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q73: Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q74: How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q75: What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q76: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q77: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q78: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q79: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q80: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q81: What common misconceptions exist about 01 database basics? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q82: How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q83: Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q84: How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q85: What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q86: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q87: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q88: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q89: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q90: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

## Q91: What common misconceptions exist about 01 database basics? Extend your answer with a second example.
**A:** People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

## Q92: How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.
**A:** Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

## Q93: Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.
**A:** Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

## Q94: How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.
**A:** Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

## Q95: What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.
**A:** Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

## Q96: Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.
**A:** One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

## Q97: Why is 01 database basics important in real production systems? Extend your answer with a second example.
**A:** It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

## Q98: What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.
**A:** Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

## Q99: Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.
**A:** Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

## Q100: Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.
**A:** In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.
