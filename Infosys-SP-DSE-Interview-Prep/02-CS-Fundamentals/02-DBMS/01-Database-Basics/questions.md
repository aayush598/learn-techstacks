# 01 Database Basics — Dbms

**100 Interview Q&A — Infosys Specialist Programmer (SP) / Digital Specialist Engineer (DSE)**

<details open>
<summary style='cursor:pointer;font-weight:bold;font-size:1.1em'>Tap to expand all 100 questions</summary>

1. **What is a database and a DBMS?**
   - A database is an organised collection of data; a DBMS is software to create, manage, query, and secure databases (e.g., PostgreSQL, MySQL). It enforces constraints, transactions, and concurrency.

2. **What is the difference between a database and a DBMS?**
   - Database = the stored data itself; DBMS = the software system managing the data (storage, retrieval, integrity, concurrency). One DBMS can manage many databases.

3. **What is a relational database?**
   - A database storing data in tables (relations) with rows (tuples) and columns (attributes), linked by keys, queried with SQL, guaranteed by ACID transactions — e.g., PostgreSQL.

4. **What is a NoSQL database? Give types.**
   - Non-relational, schema-flexible, horizontally scalable stores: document (MongoDB), key-value (Redis), columnar (Cassandra), graph (Neo4j). Chosen for scale/velocity/flexibility.

5. **What is a primary key?**
   - A column (or combination) that uniquely identifies each row — non-null and unique. It is the relational backbone for foreign-key references and fast lookup.

6. **What is a foreign key?**
   - A column referencing the primary key of another table, enforcing referential integrity — ensuring a child row always points at an existing parent.

7. **What is a candidate key vs super key?**
   - Super key: any set of columns that uniquely identifies rows. Candidate key: a minimal super key (no column can be removed). Primary key = chosen candidate key.

8. **What is a composite key?**
   - A primary/unique key formed by two or more columns jointly identifying a row (e.g., (student_id, course_id) in enrollment).

9. **What is a unique key vs primary key?**
   - Both enforce uniqueness; primary key is non-null and only one per table; unique keys allow a single NULL, and a table may have several.

10. **Explain entity, attribute, and relationship.**
   - Entity = a thing stored in its own table; attribute = a property column; relationship = an association (one-to-one, one-to-many, many-to-many).

11. **What is a view in SQL?**
   - A virtual table defined by a stored SELECT query. It presents a logically filtered/projected subset without duplicating data, hiding complexity and enforcing row/col security.

12. **Data types: INT, VARCHAR, DATE — when to use each?**
   - INT for whole numbers/counter keys; VARCHAR(n) for bounded variable text; DATE/TIMESTAMP for time-based logic. Choose the tightest correct type to save storage and index size.

13. **What is the difference between TRUNCATE and DELETE?**
   - TRUNCATE removes all rows quickly by deallocating pages, can't be filtered, resets identity, and is not per-row logged like DELETE; DELETE is DML, filterable, with WHERE and triggers.

14. **What is a DROP vs DELETE vs TRUNCATE?**
   - DROP removes the whole table (structure+data) permanently; TRUNCATE empties the data quickly, keeps structure; DELETE removes specific rows and can be rolled back with a transaction.

15. **What is data integrity?**
   - Correctness and consistency guaranteed by constraints: entity (PK), referential (FK), domain (types/CHECK), user-defined — the DBMS enforces them on write.

16. **How does PostgreSQL differ from SQLite?**
   - PostgreSQL is a client-server DB with advanced features (full-text, JSONB, MVCC, extensive indexing, concurrency); SQLite is an embedded file-based engine — zero admin, single-file, lighter concurrency.

17. **What is a snapshot isolation / MVCC at a high level?**
   - Multi-version concurrency control gives each reader a consistent snapshot of committed data without locks — writers don't block readers; PostgreSQL uses this.

18. **What is database connection pooling?**
   - Reusing a cache of open DB connections rather than creating/freeing them per request — dramatically reduces latency and server load in API backends.

19. **What is an ORM and why use it?**
   - A library mapping tables to objects (SQLAlchemy, Django ORM) so application code uses Python objects instead of raw SQL strings — safer, portable, but must watch for N+1.

20. **What is the N+1 query problem?**
   - Loading a collection, then fetching one extra query per row (N queries) instead of one joined query — a classic performance trap; solve with eager loading/joins.

21. **Explain database normalization in one sentence.**
   - Organising schema to minimise redundancy and dependency anomalies by splitting tables according to normal forms — a central Infosys DBMS question.

22. **What is denormalization and when is it used?**
   - Intentionally merging/duplicating data to reduce JOINs or reads at scale (reporting, caching) — trading write overhead and consistency for read speed.

23. **What is a stored procedure?**
   - Precompiled SQL logic stored and executed on the server (loops, transactions, business checks) — reduces network chatter and centralises rules.

24. **What is a trigger?**
   - Server-side code automatically executed on INSERT/UPDATE/DELETE events — used for audits, cascades, and integrity constraints without app changes.

25. **What is a transaction?**
   - A unit of work executed atomically with ACID guarantees (BEGIN...COMMIT/ROLLBACK) — the fundamental safety unit a bank transfer demonstrates.

26. **Define 01 database basics in one line and then expand with a real-world example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

27. **Why is 01 database basics important in real production systems?**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

28. **What are the advantages and disadvantages of 01 database basics?**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

29. **Compare 01 database basics with alternatives and state when to prefer which.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

30. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

31. **What common misconceptions exist about 01 database basics?**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

32. **How would you test correctness of a system that relies on 01 database basics?**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

33. **Describe 01 database basics as if explaining to a new hire.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

34. **How does 01 database basics interact with performance (time/space trade-off)?**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

35. **What would you change about how 01 database basics is taught, based on your experience?**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

36. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

37. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

38. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

39. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

40. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

41. **What common misconceptions exist about 01 database basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

42. **How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

43. **Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

44. **How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

45. **What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

46. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

47. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

48. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

49. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

50. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

51. **What common misconceptions exist about 01 database basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

52. **How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

53. **Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

54. **How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

55. **What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

56. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

57. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

58. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

59. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

60. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

61. **What common misconceptions exist about 01 database basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

62. **How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

63. **Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

64. **How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

65. **What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

66. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

67. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

68. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

69. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

70. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

71. **What common misconceptions exist about 01 database basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

72. **How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

73. **Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

74. **How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

75. **What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

76. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

77. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

78. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

79. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

80. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

81. **What common misconceptions exist about 01 database basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

82. **How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

83. **Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

84. **How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

85. **What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

86. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

87. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

88. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

89. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

90. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

91. **What common misconceptions exist about 01 database basics? Extend your answer with a second example.**
   - People confuse terminologies that sound similar, assume a feature is 'automatic' when it needs configuration, or copy-paste patterns without understanding trade-offs. Clearing each misconception shows depth beyond definitions.

92. **How would you test correctness of a system that relies on 01 database basics? Extend your answer with a second example.**
   - Unit tests for the isolated logic, integration tests for the interplay with other components, plus failure/scenario tests (edge inputs, stress). This matches your pytest/unittest experience with CI pipelines.

93. **Describe 01 database basics as if explaining to a new hire. Extend your answer with a second example.**
   - Start from the goal it serves, add a minimal concrete analogy, state its constraints, then show the simplest possible example — the learning order matters more than dumping terminology.

94. **How does 01 database basics interact with performance (time/space trade-off)? Extend your answer with a second example.**
   - Typically it trades one resource for another (space for speed, or latency for consistency). Quantify with complexity wherever possible and mention measurable impact on the user-facing system.

95. **What would you change about how 01 database basics is taught, based on your experience? Extend your answer with a second example.**
   - Move from memorisation of syntax/terms to practice with small concrete problems, because understanding only solidifies through application — this mirrors how you structured your own learning for placement interviews.

96. **Define 01 database basics in one line and then expand with a real-world example. Extend your answer with a second example.**
   - One line: 01 database basics is a core concept/mechanism in computer science governing how systems organise and process data. Real-world example: it maps to daily objects (library shelves, queues at a counter) so the abstract idea has an intuitive concrete anchor the interviewer can build on.

97. **Why is 01 database basics important in real production systems? Extend your answer with a second example.**
   - It directly affects correctness, performance, resource usage and maintainability. Understanding it lets an engineer reason about trade-offs, anticipate failure modes, and choose the right tool, which is exactly the engineering judgement a Specialist Digital Engineer role needs.

98. **What are the advantages and disadvantages of 01 database basics? Extend your answer with a second example.**
   - Advantages: predictability of behaviour, standardised semantics, widely understood patterns. Disadvantages: each design brings overhead or constraints, so it must be balanced against simplicity and project context whenever an alternative exists.

99. **Compare 01 database basics with alternatives and state when to prefer which. Extend your answer with a second example.**
   - Compare by criteria: speed, memory, complexity, latency, consistency. There is no universal best — the winner depends on the workload (read-heavy vs write-heavy, scale, consistency requirements); state the decision matrix explicitly.

100. **Give a scenario from your own projects (FastAPI services, RAG pipelines, COTS automation) where 01 database basics knowledge applied. Extend your answer with a second example.**
   - In building backend services and AI pipelines, concepts like this guided API design, data flow and error handling; referencing one concrete project decision makes the answer credible and ties theory to your resume.

</details>