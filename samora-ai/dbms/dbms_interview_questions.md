# DBMS — 100 Interview Q&A

---

## Q1: What is a DBMS?
**A:** A Database Management System (DBMS) is software that allows users to define, create, maintain, and control access to the database. It provides an interface between the data and the user or application.

## Q2: What is a database?
**A:** A database is an organized collection of structured data stored electronically, typically in a computer system, and managed by a DBMS.

## Q3: What are the advantages of DBMS over file systems?
**A:** Data redundancy control, data consistency, data sharing, security, backup or recovery, concurrency control, and data independence.

## Q4: What is RDBMS?
**A:** Relational DBMS stores data in tables (relations) with rows and columns, and relationships are established using keys. Examples: MySQL, Oracle, PostgreSQL.

## Q5: What is a primary key?
**A:** A primary key is a column or set of columns that uniquely identifies each row in a table. It cannot be NULL and must be unique.

## Q6: What is a foreign key?
**A:** A foreign key is a column that creates a link between two tables. It references the primary key of another table to enforce referential integrity.

## Q7: What is a candidate key?
**A:** A candidate key is a set of attributes that can uniquely identify a row. A table may have multiple candidate keys; one becomes the primary key.

## Q8: What is a super key?
**A:** A super key is any set of attributes that uniquely identifies rows. It may contain extra attributes not needed for uniqueness.

## Q9: What is an alternate key?
**A:** An alternate key is a candidate key not chosen as the primary key.

## Q10: What is a composite key?
**A:** A composite key is a primary key made of two or more columns together to uniquely identify a row.

## Q11: What is a surrogate key?
**A:** A surrogate key is an artificial key (for example, auto-increment ID) used as a primary key, having no business meaning.

## Q12: What is normalization?
**A:** Normalization is the process of organizing data to minimize redundancy and dependency by dividing tables into smaller related tables.

## Q13: What is 1NF?
**A:** First Normal Form: each table cell holds a single atomic value, and each record is unique.

## Q14: What is 2NF?
**A:** Second Normal Form: table is in 1NF and all non-key attributes are fully functionally dependent on the primary key (no partial dependency).

## Q15: What is 3NF?
**A:** Third Normal Form: table is in 2NF and has no transitive dependency (non-key attributes depend only on the key).

## Q16: What is BCNF?
**A:** Boyce-Codd Normal Form: a stronger 3NF; for every functional dependency X to Y, X must be a super key.

## Q17: What is 4NF?
**A:** Fourth Normal Form: table is in BCNF and has no multi-valued dependencies.

## Q18: What is 5NF?
**A:** Fifth Normal Form: table is in 4NF and cannot be decomposed into smaller tables without loss (join dependency).

## Q19: What is denormalization?
**A:** Denormalization is the process of adding redundant data to tables to improve read performance at the cost of write complexity.

## Q20: What is a transaction?
**A:** A transaction is a logical unit of work consisting of one or more database operations (read or write) executed as a whole.

## Q21: What are ACID properties?
**A:** Atomicity, Consistency, Isolation, Durability — guarantees a transaction is reliable.

## Q22: Explain Atomicity.
**A:** Atomicity ensures a transaction is all-or-nothing; either all operations complete or none do.

## Q23: Explain Consistency.
**A:** Consistency ensures a transaction brings the database from one valid state to another, preserving invariants.

## Q24: Explain Isolation.
**A:** Isolation ensures concurrent transactions do not interfere; each appears to run independently.

## Q25: Explain Durability.
**A:** Durability ensures once a transaction commits, its changes persist even after a system failure.

## Q26: What is a join?
**A:** A join combines rows from two or more tables based on a related column.

## Q27: What is an inner join?
**A:** Inner join returns only rows with matching values in both tables.

## Q28: What is a left join?
**A:** Left join returns all rows from the left table and matched rows from the right; unmatched right side is NULL.

## Q29: What is a right join?
**A:** Right join returns all rows from the right table and matched rows from the left; unmatched left side is NULL.

## Q30: What is a full outer join?
**A:** Full outer join returns all rows from both tables, with NULLs where there is no match.

## Q31: What is a self join?
**A:** A self join joins a table with itself to compare rows within the same table.

## Q32: What is a cross join?
**A:** A cross join returns the Cartesian product of two tables (every row combined with every row).

## Q33: What is SQL?
**A:** SQL (Structured Query Language) is used to manage and manipulate relational databases.

## Q34: What are DDL commands?
**A:** Data Definition Language commands define structure: CREATE, ALTER, DROP, TRUNCATE.

## Q35: What are DML commands?
**A:** Data Manipulation Language commands manage data: SELECT, INSERT, UPDATE, DELETE.

## Q36: What are DCL commands?
**A:** Data Control Language commands manage access: GRANT, REVOKE.

## Q37: What are TCL commands?
**A:** Transaction Control Language: COMMIT, ROLLBACK, SAVEPOINT, SET TRANSACTION.

## Q38: Difference between TRUNCATE and DELETE?
**A:** TRUNCATE removes all rows without logging individual deletions (cannot roll back in some DBs), resets identity; DELETE removes specific rows with logging and can be rolled back.

## Q39: Difference between DROP and TRUNCATE?
**A:** DROP removes the table structure and data; TRUNCATE removes only data, keeping the structure.

## Q40: What is an index?
**A:** An index is a data structure (often B-tree) that improves query speed by providing fast lookup on columns.

## Q41: What is a clustered index?
**A:** A clustered index determines the physical order of data in a table; a table can have only one.

## Q42: What is a non-clustered index?
**A:** A non-clustered index stores a separate structure with pointers to the actual data rows; a table can have many.

## Q43: What is a unique index?
**A:** A unique index ensures the indexed column has no duplicate values.

## Q44: When should you avoid indexes?
**A:** On small tables, columns with few distinct values, or frequently updated columns where write overhead outweighs read benefit.

## Q45: What is a view?
**A:** A view is a virtual table based on a SQL query; it does not store data itself (except materialized views).

## Q46: What is a materialized view?
**A:** A materialized view stores the query result physically and must be refreshed; good for expensive aggregations.

## Q47: What is a stored procedure?
**A:** A stored procedure is a precompiled set of SQL statements stored in the database, callable by name.

## Q48: What is a trigger?
**A:** A trigger is a stored procedure that automatically executes in response to INSERT, UPDATE, or DELETE events.

## Q49: What is a cursor?
**A:** A cursor is a database object used to retrieve and process rows one at a time within a result set.

## Q50: What is a constraint?
**A:** Constraints enforce rules on data: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT.

## Q51: What is the difference between WHERE and HAVING?
**A:** WHERE filters rows before aggregation; HAVING filters groups after aggregation.

## Q52: What are aggregate functions?
**A:** Functions that compute a single value from a set: COUNT, SUM, AVG, MIN, MAX.

## Q53: What is GROUP BY?
**A:** GROUP BY groups rows sharing a value so aggregate functions can be applied to each group.

## Q54: What is a subquery?
**A:** A subquery is a query nested inside another query, used to return data the outer query needs.

## Q55: What is a correlated subquery?
**A:** A subquery that references columns from the outer query and executes once per outer row.

## Q56: Difference between subquery and join?
**A:** Subqueries are nested and often used for existence checks; joins combine datasets and are usually faster for large sets.

## Q57: What is a UNION?
**A:** UNION combines results of two queries and removes duplicates.

## Q58: What is UNION ALL?
**A:** UNION ALL combines results including duplicates and is faster than UNION.

## Q59: What is a schema?
**A:** A schema is the logical structure or blueprint of a database: tables, views, indexes, and relationships.

## Q60: What is a data dictionary?
**A:** A data dictionary (system catalog) stores metadata about the database structure.

## Q61: What is concurrency control?
**A:** Techniques to manage simultaneous transactions so they do not conflict, preserving consistency.

## Q62: What is a lock?
**A:** A lock restricts access to data by a transaction to prevent conflicts during concurrent operations.

## Q63: What is a shared lock?
**A:** A shared lock allows multiple transactions to read but not modify the data.

## Q64: What is an exclusive lock?
**A:** An exclusive lock allows a transaction to read and write; no other transaction can lock it.

## Q65: What is deadlock?
**A:** A deadlock occurs when two or more transactions wait indefinitely for each other to release locks.

## Q66: How are deadlocks resolved?
**A:** Databases use detection (wait-for graph) and resolution by aborting or rolling back a transaction (victim selection).

## Q67: What is a deadlock prevention method?
**A:** Use consistent lock ordering, wait-die or wound-wait schemes, or acquire all locks upfront.

## Q68: What is two-phase locking (2PL)?
**A:** A concurrency protocol: growing phase (acquire locks) then shrinking phase (release locks); guarantees serializability.

## Q69: What is a dirty read?
**A:** A dirty read occurs when a transaction reads uncommitted data from another transaction that may roll back.

## Q70: What is a lost update?
**A:** A lost update happens when two transactions read and write the same data, and one update is overwritten.

## Q71: What is a phantom read?
**A:** A phantom read occurs when a transaction re-executes a query and finds new rows inserted by another transaction.

## Q72: What is a non-repeatable read?
**A:** A non-repeatable read happens when a transaction reads the same row twice and gets different values due to another transaction's update.

## Q73: What are transaction isolation levels?
**A:** READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE — controlling anomalies.

## Q74: What does READ COMMITTED prevent?
**A:** Prevents dirty reads but allows non-repeatable and phantom reads.

## Q75: What does SERIALIZABLE guarantee?
**A:** The highest isolation; transactions behave as if executed serially, preventing all anomalies.

## Q76: What is a database anomaly?
**A:** Anomalies are problems in data (insertion, update, deletion) caused by poor design or redundancy.

## Q77: What is functional dependency?
**A:** A functional dependency X to Y means the value of X uniquely determines Y.

## Q78: What is a candidate key in normalization?
**A:** A minimal set of attributes that can uniquely identify a tuple and has no proper subset with that property.

## Q79: What is referential integrity?
**A:** A rule ensuring foreign key values match a primary key value in the referenced table or are NULL.

## Q80: What is a checkpoint in databases?
**A:** A checkpoint is a point where all dirty pages are written to disk, shortening recovery time.

## Q81: What is a log file?
**A:** A log records all transaction operations for recovery and rollback purposes.

## Q82: What is write-ahead logging (WAL)?
**A:** WAL ensures changes are written to the log before they are written to the database, enabling recovery.

## Q83: What is a backup?
**A:** A copy of the database saved to restore data in case of failure or loss.

## Q84: What is a full backup?
**A:** A complete copy of the entire database at a point in time.

## Q85: What is an incremental backup?
**A:** A backup of only the data changed since the last backup.

## Q86: What is database replication?
**A:** Replication copies and maintains database data across multiple servers for availability and load distribution.

## Q87: What is master-slave replication?
**A:** One master handles writes; slaves replicate and handle reads.

## Q88: What is sharding?
**A:** Sharding horizontally partitions data across multiple databases or servers based on a shard key.

## Q89: What is partitioning?
**A:** Partitioning divides a table into smaller pieces (by range, list, hash) within the same database.

## Q90: What is a NoSQL database?
**A:** NoSQL databases store non-relational data (document, key-value, columnar, graph) and scale horizontally.

## Q91: Difference between SQL and NoSQL?
**A:** SQL is relational, schema-based, ACID; NoSQL is flexible-schema, distributed, often BASE.

## Q92: What is CAP theorem?
**A:** In distributed systems, you can have only two of Consistency, Availability, and Partition tolerance.

## Q93: What is BASE?
**A:** BASE (Basically Available, Soft state, Eventual consistency) is the consistency model for many NoSQL systems.

## Q94: What is a query optimizer?
**A:** A component that determines the most efficient execution plan for a SQL query.

## Q95: What is a query execution plan?
**A:** A step-by-step strategy the DBMS uses to execute a query, showing operations like scans and joins.

## Q96: What is cardinality in SQL?
**A:** Cardinality refers to the number of distinct rows or the relationship count (one-to-one, one-to-many).

## Q97: What is a clustered versus heap table?
**A:** A clustered table orders data by the clustered index; a heap has no clustering, data stored unordered.

## Q98: What is a NULL value?
**A:** NULL represents missing or unknown data, not zero or empty string.

## Q99: What is the difference between CHAR and VARCHAR?
**A:** CHAR is fixed-length (padded); VARCHAR is variable-length, storing only used space.

## Q100: What is database tuning?
**A:** Database tuning optimizes performance via indexing, query rewriting, configuration, and schema design.
