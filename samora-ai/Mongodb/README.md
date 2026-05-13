# MongoDB Interview Questions and Answers

## Q1: What is MongoDB?
**A:** MongoDB is a NoSQL, document-oriented database that stores data in flexible, JSON-like BSON documents. It is designed for high performance, high availability, and easy scalability, using a document model with optional schemas.

## Q2: What is a document in MongoDB?
**A:** A document is a set of key-value pairs stored in BSON format. It is the basic unit of data in MongoDB, analogous to a row in relational databases. Documents have a dynamic schema, meaning fields can vary across documents in the same collection.

## Q3: What is a collection in MongoDB?
**A:** A collection is a grouping of MongoDB documents, analogous to a table in relational databases. Collections do not enforce a schema — documents within a collection can have different fields.

## Q4: What is BSON?
**A:** BSON (Binary JSON) is a binary representation of JSON-like documents used by MongoDB. It extends JSON with additional data types such as Date, Binary, ObjectId, and Decimal128, enabling efficient storage and traversal.

## Q5: What is the difference between MongoDB and a relational database?
**A:** MongoDB uses a document-oriented model with dynamic schemas, while relational databases use tables with fixed schemas. MongoDB supports nested documents and arrays natively, scales horizontally via sharding, and uses a query language based on JSON, whereas relational databases use SQL and scale vertically.

## Q6: What is an ObjectId in MongoDB?
**A:** ObjectId is a 12-byte unique identifier used as the default primary key (`_id`) for MongoDB documents. It consists of: a 4-byte timestamp, a 5-byte random value, and a 3-byte incrementing counter, ensuring uniqueness across distributed systems.

## Q7: How does MongoDB ensure high availability?
**A:** MongoDB ensures high availability through replica sets. A replica set is a group of mongod instances that maintain the same data set, with one primary node accepting writes and multiple secondary nodes replicating data. Automatic failover occurs if the primary becomes unavailable.

## Q8: What is sharding in MongoDB?
**A:** Sharding is MongoDB's approach to horizontal scaling. It distributes data across multiple servers (shards) using a shard key. Each shard holds a subset of the data, and a config server maintains metadata about which shard holds which data range.

## Q9: What is a shard key?
**A:** A shard key is a field or compound field that determines how data is distributed across shards. It is used to partition documents across shards using range-based or hashed-based partitioning. Choosing a good shard key is critical for performance and even distribution.

## Q10: What is an index in MongoDB?
**A:** An index is a special data structure that stores a small portion of a collection's data in an efficient form to enable fast queries. MongoDB supports various index types: single field, compound, multikey, text, geospatial, hashed, and TTL (Time-To-Live) indexes.

## Q11: What is a compound index?
**A:** A compound index is an index on multiple fields within a document. The order of fields in a compound index matters — it determines how queries can use the index effectively (prefix matching). For example, an index on `{ name: 1, age: -1 }` supports queries on `name` alone or `name` + `age`.

## Q12: What is the aggregation pipeline?
**A:** The aggregation pipeline is a framework for data processing and transformation. Documents pass through a series of stages (`$match`, `$group`, `$sort`, `$project`, etc.), each transforming the data. It is MongoDB's equivalent of SQL's GROUP BY and complex joins.

## Q13: What is `$lookup` in MongoDB?
**A:** `$lookup` is an aggregation stage that performs a left outer join between collections. It matches documents from the source collection with documents from a related collection based on a specified field, enabling relational-style queries within the aggregation pipeline.

## Q14: What is the difference between `$lookup` and embedded documents?
**A:** `$lookup` performs a join at query time, referencing separate collections. Embedded documents store related data directly within a parent document. Embedding offers faster reads (single query) but limits document size, while `$lookup` offers more flexibility at the cost of additional query overhead.

## Q15: How does MongoDB handle transactions?
**A:** Since version 4.0, MongoDB supports multi-document ACID transactions for replica sets, and since 4.2, for sharded clusters. Transactions allow multiple operations (inserts, updates, deletes) across multiple documents/collections to be committed atomically.

## Q16: What is the difference between MongoDB's WiredTiger and MMAPv1 storage engines?
**A:** WiredTiger (default since MongoDB 3.2) offers document-level concurrency, compression, and better memory management. MMAPv1 (deprecated) used collection-level locking and memory-mapped files, lacking compression and efficient concurrent write support.

## Q17: What is the `explain()` method used for?
**A:** `explain()` is used to return query execution statistics, including which indexes were used, the number of documents examined, the number of documents returned, and query execution time. It helps in optimizing slow queries.

## Q18: What is covered query?
**A:** A covered query is a query where all required fields are present in the index used, and no documents need to be fetched from the collection. This results in the fastest possible query performance since MongoDB only reads from the index.

## Q19: What is the `$text` index?
**A:** `$text` index enables full-text search on string content. It supports stemming, stop words, and text search operators (`$search`, `$textScore`). A collection can have only one text index, but that index can cover multiple fields.

## Q20: What is the difference between `$set` and `$unset`?
**A:** `$set` replaces the value of a field or adds a new field to a document. `$unset` removes a specified field from a document entirely.

## Q21: What is `$push` and `$pull`?
**A:** `$push` adds an element to an array field. `$pull` removes all array elements that match a specified condition. `$push` can be used with `$each` to add multiple elements, while `$pull` supports query conditions.

## Q22: What is the `$addToSet` operator?
**A:** `$addToSet` adds a value to an array only if the value is not already present, ensuring uniqueness. It can be combined with `$each` to add multiple unique values.

## Q23: What is the difference between `$inc` and `$mul`?
**A:** `$inc` increments a numeric field by a specified value (positive or negative). `$mul` multiplies a numeric field by a specified value. Both are atomic update operators.

## Q24: How do you handle schema validation in MongoDB?
**A:** MongoDB supports schema validation using JSON Schema (via `$jsonSchema`). Validation rules can be specified at collection creation or added later using the `collMod` command. Validation can be set to `strict` (reject invalid documents) or `moderate` (warn but accept).

## Q25: What is a TTL index?
**A:** A TTL (Time-To-Live) index is a special index on a date field. MongoDB automatically removes documents when the indexed date field value is older than the specified TTL (in seconds). It is commonly used for expiring session data, logs, or temporary records.

## Q26: What is the difference between `find()` and `findOne()`?
**A:** `find()` returns a cursor to all matching documents (can be iterated). `findOne()` returns the first matching document directly as an object. `findOne()` is syntactic sugar for `find().limit(1)`.

## Q27: What is a cursor in MongoDB?
**A:** A cursor is an object that enables iteration over query results. It does not retrieve all results at once; instead, it fetches documents in batches. Cursors support methods like `limit()`, `skip()`, `sort()`, and `count()`.

## Q28: How does MongoDB handle failover?
**A:** When a primary node in a replica set becomes unreachable, the remaining secondaries hold an election to select a new primary. Elections use a majority-based consensus protocol (Raft-based). Once elected, the new primary begins accepting writes.

## Q29: What is the read concern in MongoDB?
**A:** Read concern controls the consistency and isolation of data read from replica sets and sharded clusters. Levels include: `local` (default, returns most recent data from that node), `majority` (only returns data confirmed by majority), `linearizable` (most consistent), and `snapshot` (for transactions).

## Q30: What is the write concern in MongoDB?
**A:** Write concern specifies the level of acknowledgment requested from MongoDB for write operations. Options: `w: 1` (acknowledgment from primary), `w: majority` (majority of replica set members), `w: 0` (no acknowledgment), `w: <number>` (specific number of members).

## Q31: What is the difference between `w: "majority"` and `j: true`?
**A:** `w: "majority"` ensures the write is propagated to a majority of replica set members. `j: true` requires the write to be committed to the journal on disk before acknowledging. They serve different purposes: majority ensures durability across nodes, journaling ensures recovery after a crash.

## Q32: What is `mongosh`?
**A:** `mongosh` is the official MongoDB shell (replacing the legacy `mongo` shell). It provides a JavaScript/Node.js REPL environment for interacting with MongoDB, running queries, administration commands, and scripting.

## Q33: What is the maximum document size in MongoDB?
**A:** The maximum document size is 16 MB. This limit ensures that a single document does not use excessive RAM or network bandwidth during transmission. For larger files, MongoDB recommends using GridFS.

## Q34: What is GridFS?
**A:** GridFS is a specification for storing and retrieving files that exceed the 16 MB BSON document size limit. It divides a file into chunks (default 255 KB each) and stores them in two collections: `fs.files` (metadata) and `fs.chunks` (chunk data).

## Q35: How does MongoDB handle indexing on an array field?
**A:** MongoDB creates multikey indexes for array fields. A multikey index creates index entries for each element in the array, enabling efficient queries on array contents. A collection can have only one array field per compound multikey index.

## Q36: What is the `$exists` operator?
**A:** `$exists` matches documents that have (or do not have) a specified field. For example, `{ field: { $exists: true } }` returns documents where the field exists, even if its value is `null`.

## Q37: What is the `$type` operator?
**A:** `$type` selects documents where a field has a specific BSON type. For example, `{ age: { $type: "int" } }` matches documents where `age` is a 32-bit integer. It supports BSON type aliases like `"string"`, `"object"`, `"array"`, `"date"`, etc.

## Q38: What is the `$regex` operator?
**A:** `$regex` provides regular expression pattern matching for string fields in queries. For example, `{ name: { $regex: /^john/i } }` matches names starting with "john" case-insensitively. It can leverage indexes only for prefix patterns.

## Q39: What is the `$in` and `$nin` operator?
**A:** `$in` selects documents where a field value equals any value in a specified array. `$nin` selects documents where a field value does not equal any value in a specified array. Both are commonly used for filtering against multiple values.

## Q40: What is the difference between `$elemMatch` and a simple array query?
**A:** `{ arr: { $elemMatch: { a: 1, b: 2 } } }` ensures both conditions apply to the same array element. A simple query like `{ "arr.a": 1, "arr.b": 2 }` could match across different elements in the array.

## Q41: How do you create a backup in MongoDB?
**A:** Backups can be created using `mongodump` (logical backup as BSON files), file-system snapshots (physical backup), or MongoDB Atlas continuous backups. For replica sets, backups should be taken from a secondary node to avoid impacting the primary.

## Q42: What is `mongodump` and `mongorestore`?
**A:** `mongodump` creates a BSON export of a database's data. `mongorestore` imports data from a BSON dump into a MongoDB instance. They operate at the database/collection level and are suitable for small to medium datasets.

## Q43: What is `mongoexport` and `mongoimport`?
**A:** `mongoexport` exports data from MongoDB to JSON or CSV format. `mongoimport` imports JSON, CSV, or TSV data into a MongoDB collection. These tools work at the collection level and output human-readable formats.

## Q44: What is the Role-Based Access Control (RBAC) in MongoDB?
**A:** RBAC controls access to MongoDB resources based on user roles. A role grants privileges (actions on resources). Built-in roles include `read`, `readWrite`, `dbAdmin`, `userAdmin`, `clusterAdmin`. Custom roles can be created to fine-tune permissions.

## Q45: How do you monitor MongoDB performance?
**A:** MongoDB provides several monitoring tools: `mongostat` (real-time server stats), `mongotop` (read/write activity per collection), `serverStatus` command, `currentOp` command, and the built-in profiling system. MongoDB Atlas and Ops Manager offer graphical monitoring dashboards.

## Q46: What is the MongoDB profiling level?
**A:** Profiling levels: 0 (off, default), 1 (logs slow operations exceeding a threshold), and 2 (logs all operations). The profiling data is stored in the `system.profile` capped collection.

## Q47: What is the `$hint` method?
**A:** `$hint` forces MongoDB to use a specific index for a query. It is useful when the query optimizer selects a suboptimal index. It should be used cautiously and typically only after analyzing query patterns.

## Q48: What is a covered query in MongoDB?
**A:** A covered query is a query that is satisfied entirely using an index, without scanning any documents. All fields required by the query (including projection) must be in the index. Covered queries offer the best possible read performance.

## Q49: What is the `$natural` sort?
**A:** `$natural` sort returns documents in the order they appear on disk. For a forward `$natural` sort (1), documents are returned in insertion order. For a reverse sort (-1), they are returned in reverse order. It cannot use indexes.

## Q50: What is the difference between `$project` and `$addFields`?
**A:** `$project` specifies which fields to include/exclude in the output and can compute new fields. `$addFields` adds new fields to documents while preserving all existing fields (no need to explicitly include other fields).

## Q51: What is `$bucket` in the aggregation pipeline?
**A:** `$bucket` categorizes documents into groups (buckets) based on specified boundaries. It is similar to SQL's `CASE` + `GROUP BY`. Each bucket represents a range of values, and documents are counted or aggregated within each range.

## Q52: What is `$facet` in the aggregation pipeline?
**A:** `$facet` allows multiple separate aggregation pipelines to be executed on the same set of input documents in a single stage. Each sub-pipeline produces its own output, enabling multi-dimensional aggregations like paginated results with total counts.

## Q53: What is the `$sample` stage?
**A:** `$sample` randomly selects a specified number of documents from the input. When used with a small size, it uses a random cursor; for larger samples, it performs a reservoir sampling algorithm.

## Q54: How does MongoDB handle data consistency across shards?
**A:** MongoDB uses distributed transactions (since 4.2) to ensure ACID consistency across shards. Read concerns (`majority`, `linearizable`) and write concerns (`majority`) help maintain consistency. The config server maintains metadata for routing queries correctly.

## Q55: What is a balancer in MongoDB?
**A:** The balancer is a background process in sharded clusters that ensures even distribution of data across shards. It migrates chunks from overloaded shards to underloaded shards based on the shard key range distribution.

## Q56: What is a chunk in MongoDB sharding?
**A:** A chunk is a contiguous range of shard key values. Data is partitioned into chunks, which are distributed across shards. When a chunk exceeds the specified chunk size (default 64 MB), it splits into smaller chunks automatically.

## Q57: What is the difference between range-based and hashed sharding?
**A:** Range-based sharding partitions data by shard key value ranges (e.g., A-M on shard1, N-Z on shard2). Hashed sharding uses a hash of the shard key to distribute data, providing better distribution for monotonically increasing keys (e.g., ObjectIds).

## Q58: What is a zone in MongoDB sharding?
**A:** A zone (formerly tag) allows associating ranges of shard key values with specific shards. Zones enable locality-aware sharding, where data can be pinned to specific shards based on geographic location or hardware capacity.

## Q59: What is a change stream in MongoDB?
**A:** A change stream allows applications to watch for real-time data changes (inserts, updates, deletes, replaces) on collections, databases, or entire deployments. It uses the aggregation pipeline's `$changeStream` stage and is built on the oplog.

## Q60: What is the oplog in MongoDB?
**A:** The oplog (operations log) is a special capped collection (`local.oplog.rs`) in a replica set that records all write operations. Secondary nodes use the oplog to replicate data from the primary. It is critical for replication and change streams.

## Q61: How can you prevent SQL/NoSQL injection in MongoDB?
**A:** MongoDB prevents injection when using the driver's BSON query builders (parameterized queries). Avoid building queries with string concatenation or `$where` clauses with user input. Use `mongosh`'s parameterized queries and validate/sanitize all user inputs.

## Q62: What is the `$where` operator, and why should it be avoided?
**A:** `$where` allows executing JavaScript expressions in queries. It should be avoided because: (1) it cannot use indexes, (2) it executes JavaScript which is slower, (3) it poses security risks if user input is involved, (4) it prevents query optimization.

## Q63: What is the Aggregation Pipeline's `$merge` stage?
**A:** `$merge` outputs the results of an aggregation pipeline into a collection. It can merge results (insert new documents, merge with existing, replace, keep existing, or fail on conflict). It is commonly used for materialized views and ETL pipelines.

## Q64: What is a view in MongoDB?
**A:** A view is a read-only, virtual collection created from an aggregation pipeline. Views do not store data; they compute results on-the-fly when queried. They support the same query interface as collections but cannot have write operations performed on them.

## Q65: What is an on-demand materialized view?
**A:** An on-demand materialized view is a collection that stores the pre-computed results of an aggregation pipeline for faster read performance. It is created using `$merge` or `$out` stages and must be refreshed manually or on a schedule.

## Q66: How does MongoDB handle duplicate keys on insert?
**A:** If a document with a duplicate `_id` (or unique index key) is inserted, MongoDB throws a duplicate key error. Using `insertMany()` with `ordered: false` continues processing remaining documents after a duplicate error.

## Q67: What is the `bulkWrite()` method?
**A:** `bulkWrite()` performs multiple write operations (insert, update, delete, replace) in a single batch. It supports `ordered` (default: true, stops on first error) and `unordered` (continues on error) modes, reducing network round trips.

## Q68: What is the `$convert` operator in aggregation?
**A:** `$convert` converts a value between BSON types. It supports type conversion with error handling using `onError` and `onNull` parameters. It is more robust than `$toString`, `$toInt`, etc., which throw errors on invalid input.

## Q69: What is the `$cond` operator in aggregation?
**A:** `$cond` is a ternary operator (if-then-else) in the aggregation pipeline. It evaluates a boolean expression and returns one value if true and another if false. It can be used within `$project`, `$addFields`, `$group`, etc.

## Q70: What is the `$switch` operator in aggregation?
**A:** `$switch` evaluates a series of cases and returns a result for the first matching case. It has a `default` branch for fallback. It is the aggregation equivalent of a `switch` or `case` statement in programming.

## Q71: How do you optimize slow queries in MongoDB?
**A:** Steps: (1) Use `explain()` to analyze query execution, (2) Ensure appropriate indexes exist, (3) Check for covered queries, (4) Limit returned fields with projection, (5) Use `$match` early in pipelines, (6) Avoid `$where`, (7) Monitor with the profiler and `mongostat`.

## Q72: What is query selectivity?
**A:** Query selectivity refers to the percentage of documents matched by a query. A highly selective query (matching few documents) can use an index efficiently. A query with low selectivity (matching many documents) may perform a collection scan, often requiring index optimization.

## Q73: What is the difference between `$group` and `$project` in terms of performance?
**A:** `$group` requires grouping all documents, often involving sorting and memory-intensive operations. `$project` simply transforms fields per document. `$group` should be used only when necessary, and `$match` should be applied before `$group` to reduce input documents.

## Q74: What is the `allowDiskUse` option in aggregation?
**A:** `allowDiskUse: true` permits aggregation stages to write temporary data to disk when memory limits (default 100 MB per stage) are exceeded. It is essential for large dataset aggregations that involve sorting or grouping.

## Q75: What is the difference between `ObjectId.getTimestamp()` and storing a separate date field?
**A:** `ObjectId.getTimestamp()` extracts the creation timestamp from the ObjectId (first 4 bytes). While convenient, it provides only second-level precision and cannot be modified. A dedicated date field offers millisecond precision, flexibility, and better indexing options.

## Q76: What is the recommended way to model relationships in MongoDB?
**A:** MongoDB offers two approaches: embedding (denormalization) for one-to-one and one-to-few relationships, and referencing (normalization) for one-to-many and many-to-many relationships. The choice depends on access patterns, data size, and update frequency.

## Q77: How do you implement pagination in MongoDB?
**A:** Approaches: (1) `skip()` + `limit()` — simple but inefficient for large offsets, (2) cursor-based (range queries) using `_id` or a timestamp field — efficient and stable, (3) `$facet` in aggregation for total count + paginated results.

## Q78: What is a runbook in MongoDB Ops Manager?
**A:** Ops Manager provides automated runbooks for deployment, backup, monitoring, and alerting. It enables rolling upgrades, backup scheduling, point-in-time recovery, and performance monitoring across on-premises MongoDB deployments.

## Q79: How does MongoDB handle CPU-bound workloads?
**A:** MongoDB is I/O bound for most workloads, but CPU-bound scenarios arise from indexing, aggregation (`$group`, `$sort`), JavaScript execution (`$where`), and complex queries. Solutions: optimize indexes, avoid `$where`, use covered queries, and scale horizontally.

## Q80: What is the `maxTimeMS()` cursor method?
**A:** `maxTimeMS()` sets a time limit (in milliseconds) for query execution on the server. If the query exceeds the limit, MongoDB kills the operation and returns an error. It is used to prevent long-running queries from degrading server performance.

## Q81: What is the `currentOp` command?
**A:** `currentOp` returns a list of currently running operations on a MongoDB instance. It is used to identify long-running queries, active connections, and blocking operations. Operations can be killed using `db.killOp()`.

## Q82: What is the difference between `validator` and `validationAction`?
**A:** `validator` defines the schema validation rules using `$jsonSchema` or query operators. `validationAction` specifies the action when validation fails: `"error"` (reject the write) or `"warn"` (log a warning but allow the write).

## Q83: How do you secure a MongoDB deployment?
**A:** Security measures include: (1) enable authentication (SCRAM, x.509, LDAP, or Kerberos), (2) enable TLS/SSL for encryption, (3) configure network access (firewall, bind to specific IPs), (4) implement RBAC with least privilege, (5) enable auditing, (6) encrypt data at rest.

## Q84: What is SCRAM authentication?
**A:** SCRAM (Salted Challenge Response Authentication Mechanism) is MongoDB's default authentication mechanism. It uses a challenge-response protocol that never sends the password over the network, providing protection against eavesdropping and replay attacks.

## Q85: What is the `$currentDate` operator?
**A:** `$currentDate` sets a field's value to the current date/timestamp during an update. It can be used with `$type: "date"` or `$type: "timestamp"`. It is equivalent to `$set: { field: new Date() }` but uses the server's time.

## Q86: What is the `$slice` operator in projection?
**A:** `$slice` limits the number of elements returned from an array field. It supports: positive/negative skip and limit values. For example, `{ arr: { $slice: [2, 5] } }` skips 2 elements and returns the next 5.

## Q87: What is the difference between `$unset` and setting a field to `null`?
**A:** `$unset` completely removes the field from the document. Setting a field to `null` keeps the field with a null value. Queries using `$exists` differ: `$unset` causes `$exists: true` to return false, while `null` keeps it true.

## Q88: What is the `$mergeObjects` operator?
**A:** `$mergeObjects` combines multiple documents into a single document, merging their fields. If there are conflicting fields, later documents overwrite earlier ones. It is useful in `$group` and `$replaceRoot` stages.

## Q89: How does MongoDB handle time-series data?
**A:** MongoDB has a dedicated time-series collection type (since 5.0) optimized for time-series data. It automatically organizes data for efficient queries, stores measurements and metadata separately, and supports downsampling, retention policies, and columnar compression.

## Q90: What is the `$out` stage in aggregation?
**A:** `$out` writes the results of an aggregation pipeline to a new or existing collection. It replaces the entire collection (or a specific collection in a different database). It is commonly used for ETL, data transformation, and creating summary collections.

## Q91: What is the transaction `maxTransactionLockRequestTimeoutMillis` setting?
**A:** This setting controls how long a transaction waits to acquire locks (default: 5ms). If a transaction cannot acquire all required locks within this timeout, it is aborted. It helps prevent transaction starvation and deadlocks in concurrent environments.

## Q92: What is the `$function` operator in aggregation?
**A:** `$function` (since 4.4) allows defining custom JavaScript functions in the aggregation pipeline. It is used when built-in operators cannot express the required logic. It should be used sparingly due to performance and security implications.

## Q93: How does MongoDB handle schema migrations?
**A:** MongoDB's flexible schema allows gradual migrations without downtime. Strategies include: (1) additive migration (add new fields while keeping old ones), (2) lazy migration (update documents on read), (3) batch migration (background jobs), (4) application-level versioning.

## Q94: What is the `db.collection.estimatedDocumentCount()` vs `db.collection.countDocuments()`?
**A:** `estimatedDocumentCount()` returns an approximate count based on collection metadata (fast, no filtering). `countDocuments()` performs an actual aggregation query with optional filters (accurate but potentially slower).

## Q95: What is a covered query vs an index-only query?
**A:** A covered query requires all returned and filtered fields to be in the index, and MongoDB does not need to fetch documents from the collection. An index-only query implies the query engine never needs to fetch documents from disk because all required fields exist in the index.

## Q96: What is the `$planCacheStats` command?
**A:** `$planCacheStats` returns information about the query plan cache for a collection. It reveals cached query plans, their shapes, and creation times. It is useful for debugging why the query optimizer chose a particular plan.

## Q97: How do you handle full-text search beyond `$text` index?
**A:** For advanced full-text search, MongoDB Atlas Search (built on Lucene) provides tokenization, stemming, fuzzy matching, autocomplete, faceted search, synonyms, and relevance scoring. On-premises deployments can use `$text` indexes for basic search needs.

## Q98: What is the `restore` command's `--oplogReplay` option?
**A:** `--oplogReplay` replays the oplog after restoring a dump, enabling point-in-time recovery. This is critical when restoring from a snapshot that is not the latest state — the oplog replay brings the database to the desired point in time.

## Q99: What is a zombie shard in MongoDB?
**A:** A zombie shard is a shard that was removed from a cluster but still holds data and configuration metadata. It can cause issues if not fully decommissioned. Proper removal requires `removeShard` to drain data and update config servers.

## Q100: What is the difference between `wtimeout` and `w: "majority"` in write concern?
**A:** `wtimeout` specifies a time limit (ms) for write concern acknowledgment. If the specified number of members does not acknowledge within the timeout, the write returns an error but is still applied to nodes that did acknowledge. `w: "majority"` waits for majority acknowledgment with no time limit unless `wtimeout` is set.
