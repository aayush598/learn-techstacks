# DBMS Interview Questions (Top 100)

## 1. What is a DBMS?
A Database Management System (DBMS) is software that allows users to define, create, maintain, and control access to the database. It provides an interface between the data and the user or application.

## 2. What is a database?
A database is an organized collection of structured data stored electronically, typically in a computer system, and managed by a DBMS.

## 3. What are the advantages of DBMS over file systems?
Data redundancy control, data consistency, data sharing, security, backup or recovery, concurrency control, and data independence.

## 4. What is RDBMS?
Relational DBMS stores data in tables (relations) with rows and columns, and relationships are established using keys. Examples: MySQL, Oracle, PostgreSQL.

## 5. What is a primary key?
A primary key is a column or set of columns that uniquely identifies each row in a table. It cannot be NULL and must be unique.

## 6. What is a foreign key?
A foreign key is a column that creates a link between two tables. It references the primary key of another table to enforce referential integrity.

## 7. What is a candidate key?
A candidate key is a set of attributes that can uniquely identify a row. A table may have multiple candidate keys; one becomes the primary key.

## 8. What is a super key?
A super key is any set of attributes that uniquely identifies rows. It may contain extra attributes not needed for uniqueness.

## 9. What is an alternate key?
An alternate key is a candidate key not chosen as the primary key.

## 10. What is a composite key?
A composite key is a primary key made of two or more columns together to uniquely identify a row.

## 11. What is a surrogate key?
A surrogate key is an artificial key (for example, auto-increment ID) used as a primary key, having no business meaning.

## 12. What is normalization?
Normalization is the process of organizing data to minimize redundancy and dependency by dividing tables into smaller related tables.

## 13. What is 1NF?
First Normal Form: each table cell holds a single atomic value, and each record is unique.

## 14. What is 2NF?
Second Normal Form: table is in 1NF and all non-key attributes are fully functionally dependent on the primary key (no partial dependency).

## 15. What is 3NF?
Third Normal Form: table is in 2NF and has no transitive dependency (non-key attributes depend only on the key).

## 16. What is BCNF?
Boyce-Codd Normal Form: a stronger 3NF; for every functional dependency X to Y, X must be a super key.

## 17. What is 4NF?
Fourth Normal Form: table is in BCNF and has no multi-valued dependencies.

## 18. What is 5NF?
Fifth Normal Form: table is in 4NF and cannot be decomposed into smaller tables without loss (join dependency).

## 19. What is denormalization?
Denormalization is the process of adding redundant data to tables to improve read performance at the cost of write complexity.

## 20. What is a transaction?
A transaction is a logical unit of work consisting of one or more database operations (read or write) executed as a whole.

## 21. What are ACID properties?
Atomicity, Consistency, Isolation, Durability — guarantees a transaction is reliable.

## 22. Explain Atomicity.
Atomicity ensures a transaction is all-or-nothing; either all operations complete or none do.

## 23. Explain Consistency.
Consistency ensures a transaction brings the database from one valid state to another, preserving invariants.

## 24. Explain Isolation.
Isolation ensures concurrent transactions do not interfere; each appears to run independently.

## 25. Explain Durability.
Durability ensures once a transaction commits, its changes persist even after a system failure.

## 26. What is a join?
A join combines rows from two or more tables based on a related column.

## 27. What is an inner join?
Inner join returns only rows with matching values in both tables.

## 28. What is a left join?
Left join returns all rows from the left table and matched rows from the right; unmatched right side is NULL.

## 29. What is a right join?
Right join returns all rows from the right table and matched rows from the left; unmatched left side is NULL.

## 30. What is a full outer join?
Full outer join returns all rows from both tables, with NULLs where there is no match.

## 31. What is a self join?
A self join joins a table with itself to compare rows within the same table.

## 32. What is a cross join?
A cross join returns the Cartesian product of two tables (every row combined with every row).

## 33. What is SQL?
SQL (Structured Query Language) is used to manage and manipulate relational databases.

## 34. What are DDL commands?
Data Definition Language commands define structure: CREATE, ALTER, DROP, TRUNCATE.

## 35. What are DML commands?
Data Manipulation Language commands manage data: SELECT, INSERT, UPDATE, DELETE.

## 36. What are DCL commands?
Data Control Language commands manage access: GRANT, REVOKE.

## 37. What are TCL commands?
Transaction Control Language: COMMIT, ROLLBACK, SAVEPOINT, SET TRANSACTION.

## 38. Difference between TRUNCATE and DELETE?
TRUNCATE removes all rows without logging individual deletions (cannot roll back in some DBs), resets identity; DELETE removes specific rows with logging and can be rolled back.

## 39. Difference between DROP and TRUNCATE?
DROP removes the table structure and data; TRUNCATE removes only data, keeping the structure.

## 40. What is an index?
An index is a data structure (often B-tree) that improves query speed by providing fast lookup on columns.

## 41. What is a clustered index?
A clustered index determines the physical order of data in a table; a table can have only one.

## 42. What is a non-clustered index?
A non-clustered index stores a separate structure with pointers to the actual data rows; a table can have many.

## 43. What is a unique index?
A unique index ensures the indexed column has no duplicate values.

## 44. When should you avoid indexes?
On small tables, columns with few distinct values, or frequently updated columns where write overhead outweighs read benefit.

## 45. What is a view?
A view is a virtual table based on a SQL query; it does not store data itself (except materialized views).

## 46. What is a materialized view?
A materialized view stores the query result physically and must be refreshed; good for expensive aggregations.

## 47. What is a stored procedure?
A stored procedure is a precompiled set of SQL statements stored in the database, callable by name.

## 48. What is a trigger?
A trigger is a stored procedure that automatically executes in response to INSERT, UPDATE, or DELETE events.

## 49. What is a cursor?
A cursor is a database object used to retrieve and process rows one at a time within a result set.

## 50. What is a constraint?
Constraints enforce rules on data: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT.

## 51. What is the difference between WHERE and HAVING?
WHERE filters rows before aggregation; HAVING filters groups after aggregation.

## 52. What are aggregate functions?
Functions that compute a single value from a set: COUNT, SUM, AVG, MIN, MAX.

## 53. What is GROUP BY?
GROUP BY groups rows sharing a value so aggregate functions can be applied to each group.

## 54. What is a subquery?
A subquery is a query nested inside another query, used to return data the outer query needs.

## 55. What is a correlated subquery?
A subquery that references columns from the outer query and executes once per outer row.

## 56. Difference between subquery and join?
Subqueries are nested and often used for existence checks; joins combine datasets and are usually faster for large sets.

## 57. What is a UNION?
UNION combines results of two queries and removes duplicates.

## 58. What is UNION ALL?
UNION ALL combines results including duplicates and is faster than UNION.

## 59. What is a schema?
A schema is the logical structure or blueprint of a database: tables, views, indexes, and relationships.

## 60. What is a data dictionary?
A data dictionary (system catalog) stores metadata about the database structure.

## 61. What is concurrency control?
Techniques to manage simultaneous transactions so they do not conflict, preserving consistency.

## 62. What is a lock?
A lock restricts access to data by a transaction to prevent conflicts during concurrent operations.

## 63. What is a shared lock?
A shared lock allows multiple transactions to read but not modify the data.

## 64. What is an exclusive lock?
An exclusive lock allows a transaction to read and write; no other transaction can lock it.

## 65. What is deadlock?
A deadlock occurs when two or more transactions wait indefinitely for each other to release locks.

## 66. How are deadlocks resolved?
Databases use detection (wait-for graph) and resolution by aborting or rolling back a transaction (victim selection).

## 67. What is a deadlock prevention method?
Use consistent lock ordering, wait-die or wound-wait schemes, or acquire all locks upfront.

## 68. What is two-phase locking (2PL)?
A concurrency protocol: growing phase (acquire locks) then shrinking phase (release locks); guarantees serializability.

## 69. What is a dirty read?
A dirty read occurs when a transaction reads uncommitted data from another transaction that may roll back.

## 70. What is a lost update?
A lost update happens when two transactions read and write the same data, and one update is overwritten.

## 71. What is a phantom read?
A phantom read occurs when a transaction re-executes a query and finds new rows inserted by another transaction.

## 72. What is a non-repeatable read?
A non-repeatable read happens when a transaction reads the same row twice and gets different values due to another transaction's update.

## 73. What are transaction isolation levels?
READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — controlling anomalies.

## 74. What does READ COMMITTED prevent?
Prevents dirty reads but allows non-repeatable and phantom reads.

## 75. What does SERIALIZABLE guarantee?
The highest isolation; transactions behave as if executed serially, preventing all anomalies.

## 76. What is a database anomaly?
Anomalies are problems in data (insertion, update, deletion) caused by poor design or redundancy.

## 77. What is functional dependency?
A functional dependency X to Y means the value of X uniquely determines Y.

## 78. What is a candidate key in normalization?
A minimal set of attributes that can uniquely identify a tuple and has no proper subset with that property.

## 79. What is referential integrity?
A rule ensuring foreign key values match a primary key value in the referenced table or are NULL.

## 80. What is a checkpoint in databases?
A checkpoint is a point where all dirty pages are written to disk, shortening recovery time.

## 81. What is a log file?
A log records all transaction operations for recovery and rollback purposes.

## 82. What is write-ahead logging (WAL)?
WAL ensures changes are written to the log before they are written to the database, enabling recovery.

## 83. What is a backup?
A copy of the database saved to restore data in case of failure or loss.

## 84. What is a full backup?
A complete copy of the entire database at a point in time.

## 85. What is an incremental backup?
A backup of only the data changed since the last backup.

## 86. What is database replication?
Replication copies and maintains database data across multiple servers for availability and load distribution.

## 87. What is master-slave replication?
One master handles writes; slaves replicate and handle reads.

## 88. What is sharding?
Sharding horizontally partitions data across multiple databases or servers based on a shard key.

## 89. What is partitioning?
Partitioning divides a table into smaller pieces (by range, list, hash) within the same database.

## 90. What is a NoSQL database?
NoSQL databases store non-relational data (document, key-value, columnar, graph) and scale horizontally.

## 91. Difference between SQL and NoSQL?
SQL is relational, schema-based, ACID; NoSQL is flexible-schema, distributed, often BASE.

## 92. What is CAP theorem?
In distributed systems, you can have only two of Consistency, Availability, and Partition tolerance.

## 93. What is BASE?
BASE (Basically Available, Soft state, Eventual consistency) is the consistency model for many NoSQL systems.

## 94. What is a query optimizer?
A component that determines the most efficient execution plan for a SQL query.

## 95. What is a query execution plan?
A step-by-step strategy the DBMS uses to execute a query, showing operations like scans and joins.

## 96. What is cardinality in SQL?
Cardinality refers to the number of distinct rows or the relationship count (one-to-one, one-to-many).

## 97. What is a clustered versus heap table?
A clustered table orders data by the clustered index; a heap has no clustering, data stored unordered.

## 98. What is a NULL value?
NULL represents missing or unknown data, not zero or empty string.

## 99. What is the difference between CHAR and VARCHAR?
CHAR is fixed-length (padded); VARCHAR is variable-length, storing only used space.

## 100. What is database tuning?
Database tuning optimizes performance via indexing, query rewriting, configuration, and schema design.
