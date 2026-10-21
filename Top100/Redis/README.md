# Redis Interview Questions and Answers

## Q1: What is Redis?
**A:** Redis (Remote Dictionary Server) is an open-source, in-memory data structure store used as a database, cache, and message broker. It supports data structures like strings, hashes, lists, sets, sorted sets, bitmaps, hyperloglogs, and geospatial indexes with built-in replication, persistence, and clustering.

## Q2: What are the main features of Redis?
**A:** (1) In-memory storage for high performance. (2) Rich data structures (strings, hashes, lists, sets, sorted sets, etc.). (3) Persistence (RDB snapshots, AOF logs). (4) Replication (master-slave). (5) High availability via Redis Sentinel. (6) Partitioning via Redis Cluster. (7) Pub/Sub messaging. (8) Lua scripting. (9) TTL/expiry for keys.

## Q3: What data structures does Redis support?
**A:** Strings, Hashes, Lists, Sets, Sorted Sets, Bitmaps (bit operations on strings), HyperLogLogs (probabilistic cardinality estimation), Geospatial indexes, Streams (append-only log), and Bloom Filters (via modules).

## Q4: What is the difference between Redis and Memcached?
**A:** Redis supports rich data structures while Memcached only supports simple key-value strings. Redis has persistence, replication, clustering, and Lua scripting. Memcached is purely in-memory with no persistence. Redis is single-threaded for commands; Memcached is multi-threaded.

## Q5: What is Redis persistence?
**A:** Redis offers two persistence mechanisms: RDB (Redis Database) — point-in-time snapshots at configured intervals; AOF (Append-Only File) — logs every write operation for replay. Both can be combined for durability. RDB is faster to restart; AOF provides better durability.

## Q6: What is RDB persistence?
**A:** RDB performs point-in-time snapshots of the dataset to disk. It is triggered by configured save intervals (e.g., save 900 1 = save if at least 1 key changed in 900 seconds), manual `SAVE`/`BGSAVE` commands, or shutdown. RDB files are compact and ideal for backups.

## Q7: What is AOF persistence?
**A:** AOF logs every write operation to an append-only file. Redis replays the AOF on startup to reconstruct the dataset. AOF provides better durability (configurable fsync: every second, always, or never). AOF files are larger than RDB but can be rewritten to compact them.

## Q8: What is AOF rewrite?
**A:** AOF rewrite compacts the AOF file by creating a minimal version from the current dataset. It reads the current keys and generates the minimum set of commands needed to recreate them, eliminating redundant operations. Redis can perform rewrites in the background (`BGREWRITEAOF`).

## Q9: What is the difference between RDB and AOF?
**A:** RDB produces compact single-file snapshots with faster recovery but potential data loss (snapshot interval). AOF logs every write with better durability but larger files and slower recovery. RDB is better for backups; AOF is better for crash recovery. Using both is possible.

## Q10: What is Redis replication?
**A:** Redis replication allows a replica (slave) to copy the exact data from a primary (master). Replicas accept read-only queries. Replication is asynchronous by default. It provides data redundancy, read scaling, and backups. Replicas can be promoted to masters in failover.

## Q11: How does Redis replication work?
**A:** The replica connects to the master and issues a `PSYNC` command. The master forks a background process to create an RDB snapshot while buffering new writes. The snapshot is sent to the replica, followed by the buffered writes. After the initial sync, the master streams ongoing writes to the replica.

## Q12: What is Redis Sentinel?
**A:** Redis Sentinel provides high availability for Redis. It monitors master and replica instances, performs automatic failover (promoting a replica to master if the master fails), notifies administrators, and acts as a configuration provider for clients to discover the current master.

## Q13: How does Redis Sentinel achieve high availability?
**A:** A cluster of Sentinel processes (typically 3 or 5 for quorum) monitors the master. If the master is unreachable (subjectively down by one Sentinel, objectively down by quorum), Sentinels agree on a failover, elect a replica as the new master, and reconfigure other replicas.

## Q14: What is Redis Cluster?
**A:** Redis Cluster is a distributed implementation of Redis that automatically shards data across multiple nodes. It provides horizontal scalability, automatic partitioning, and some degree of availability (node failures are handled). Data is split into 16384 hash slots distributed across nodes.

## Q15: How does Redis Cluster partition data?
**A:** Redis Cluster uses hash slot partitioning. The key space is divided into 16384 slots. A hash function (CRC16 mod 16384) determines which slot a key belongs to. Each node in the cluster is responsible for a subset of slots. Clients use the `CLUSTER SLOTS` command to know where to route requests.

## Q16: What happens when a Redis Cluster node fails?
**A:** If a master node fails, its replicas (if any) will be promoted. If a node fails and has no replica, the cluster becomes unavailable for the hash slots served by that node (unless cluster-require-full-coverage is set to no). Cluster nodes gossip to detect failures (via `CLUSTER MEET`).

## Q17: What is a Redis hash slot?
**A:** A hash slot is a unit of data partitioning in Redis Cluster. There are 16384 fixed slots. Each key is assigned to a slot using `HASH_SLOT = CRC16(key) % 16384`. Hash tags (e.g., `{user:123}.name`) allow multiple keys to be in the same slot for multi-key operations.

## Q18: What is a hash tag in Redis?
**A:** A hash tag ensures that related keys are stored in the same hash slot. If a key contains `{...}`, only the substring inside the braces is hashed. For example, `user:{123}.profile` and `user:{123}.settings` will be in the same slot, enabling multi-key operations.

## Q19: What is Redis Pub/Sub?
**A:** Redis Pub/Sub is a messaging paradigm where publishers send messages to channels without knowing who the subscribers are. Subscribers listen to channels and receive messages in real-time. Messages are fire-and-forget — they are not persisted. It is used for real-time messaging, notifications, and event broadcasting.

## Q20: What is the difference between Pub/Sub and Redis Streams?
**A:** Pub/Sub is fire-and-forget — messages are lost if no subscriber is listening. Streams persist messages, support consumer groups, acknowledgment, and replay. Streams are better for reliable messaging and event sourcing. Pub/Sub is simpler for real-time broadcasting.

## Q21: What are Redis Streams?
**A:** Redis Streams is an append-only log data structure introduced in Redis 5.0. Each entry has a unique ID (timestamp-sequence). Streams support consumer groups for distributing messages among consumers, acknowledgment, pending entries, and blocking reads. They enable event sourcing and message queuing.

## Q22: What is a consumer group in Redis Streams?
**A:** A consumer group is a mechanism for distributing stream messages among multiple consumers. Messages are automatically load-balanced across consumers. Each message is delivered to only one consumer in the group. Consumers acknowledge processed messages, and pending entries (not acknowledged) can be claimed by other consumers.

## Q23: What is the `XREAD` vs `XREADGROUP` command?
**A:** `XREAD` reads messages from a stream independently (no consumer group). `XREADGROUP` reads messages as part of a consumer group, receiving only messages assigned to that consumer. `XREADGROUP` supports acknowledgment, pending list, and delivery tracking.

## Q24: What is Redis as a cache?
**A:** Redis is commonly used as a cache due to its in-memory speed. Caching patterns include: (1) Cache-aside (lazy loading) — application checks cache first, loads from DB on miss, and updates cache. (2) Write-through — writes go to both cache and DB simultaneously. (3) Write-behind — writes go to cache and are asynchronously written to DB.

## Q25: What is cache-aside (lazy loading) in Redis?
**A:** In cache-aside, the application checks Redis first. On cache hit, data is returned. On cache miss, the application loads data from the database, stores it in Redis with a TTL, and returns it. This is the most common caching pattern but can result in stale data if the DB is updated directly.

## Q26: What is cache penetration?
**A:** Cache penetration occurs when requests target data that doesn't exist in either cache or database. Every request hits the database because Redis never has the data. Attackers can exploit this by requesting non-existent keys. Solutions: cache null values briefly, use Bloom filters, or validate requests early.

## Q27: What is a Bloom filter in Redis?
**A:** A Bloom filter is a probabilistic data structure that tests whether an element is definitely not in a set (false negatives impossible) or possibly in a set (false positives possible). Redis modules like RedisBloom provide Bloom filters. They prevent cache penetration by quickly rejecting non-existent keys.

## Q28: What is cache avalanche?
**A:** Cache avalanche occurs when many cached entries expire at the same time, causing a massive wave of requests to hit the database simultaneously. This can overwhelm the database. Prevention: use different TTLs with random offsets, or use Redis Cluster to distribute load.

## Q29: What is cache stampede (thundering herd)?
**A:** Cache stampede happens when a popular cached key expires and many concurrent requests all try to regenerate the cache simultaneously, overloading the backend. Solutions: (1) Mutex/locking — only one request regenerates, others wait. (2) Early recomputation — refresh cache before expiration.

## Q30: What is a cache miss?
**A:** A cache miss occurs when a requested key is not found in the cache. The application must retrieve the data from the primary datastore and optionally populate the cache. High cache miss rates indicate poor cache efficiency or cold start.

## Q31: What is cache hit ratio?
**A:** Cache hit ratio is the percentage of requests served from the cache: `hits / (hits + misses) * 100`. A high ratio (90%+) indicates efficient caching. Low ratios suggest the cache is too small, TTLs are too short, or the access pattern is not cache-friendly.

## Q32: What is TTL in Redis?
**A:** TTL (Time To Live) is the expiration time of a key. After the TTL expires, the key is automatically deleted. Commands: `EXPIRE key seconds`, `TTL key` (check remaining time), `PERSIST key` (remove TTL). TTL is critical for cache management and temporary data.

## Q33: How does Redis handle key expiration?
**A:** Redis uses two strategies: (1) Lazy expiration — keys are checked when accessed; if expired, they are deleted. (2) Active expiration — Redis periodically (every 100ms) samples keys with TTLs from a subset and deletes expired ones. This balances CPU usage and memory cleanup.

## Q34: What is the maximum number of keys Redis can store?
**A:** The maximum is limited by available memory (RAM). Redis can handle billions of keys with appropriate memory sizing. A practical limit depends on key size, value size, and overhead (approximately 100 bytes per key overhead). The `maxmemory` configuration sets the upper limit.

## Q35: What happens when Redis reaches maxmemory?
**A:** When `maxmemory` is reached, Redis applies the configured eviction policy to free memory. Options include: `noeviction` (return errors), `allkeys-lru` (evict least recently used), `volatile-lru` (evict LRU among keys with TTL), `allkeys-lfu`, `volatile-lfu`, `allkeys-random`, `volatile-random`, `volatile-ttl`.

## Q36: What is LRU eviction in Redis?
**A:** LRU (Least Recently Used) eviction removes keys that haven't been accessed the longest. Redis uses an approximated LRU algorithm — it samples a small set of keys (default 5) and evicts the least recently used among them. This is efficient and nearly as good as true LRU.

## Q37: What is LFU eviction in Redis?
**A:** LFU (Least Frequently Used) eviction removes keys that are accessed least frequently. Introduced in Redis 4.0, it tracks access frequency using a probabilistic counter. LFU is better for workloads where frequently accessed keys should stay regardless of recent access pattern.

## Q38: What is Redis transaction?
**A:** Redis transactions allow executing a group of commands atomically using `MULTI`, `EXEC`, `DISCARD`, and `WATCH`. Commands are queued after `MULTI` and executed sequentially when `EXEC` is called. Transactions are atomic but not isolated — other clients can see intermediate results.

## Q39: What is `WATCH` in Redis?
**A:** `WATCH` provides optimistic locking for Redis transactions. It monitors one or more keys for changes. If any watched key is modified before `EXEC`, the transaction is aborted (returns nil). This enables a CAS (compare-and-set) pattern without pessimistic locking.

## Q40: What is optimistic locking in Redis?
**A:** Optimistic locking uses `WATCH` to check that keys haven't been modified during a transaction. The transaction is retried if a conflict is detected. This avoids the overhead of traditional locks while preventing race conditions in concurrent scenarios.

## Q41: What is a Redis pipeline?
**A:** A pipeline batches multiple Redis commands together and sends them to the server in a single network round trip, reducing latency. Responses are received in a batch. Pipelining does not guarantee atomic execution (unlike transactions) — it only batches network communication.

## Q42: What is the difference between pipelining and transactions in Redis?
**A:** Pipelining reduces network latency by batching commands but does not guarantee atomic execution. Transactions (`MULTI`/`EXEC`) guarantee atomic execution (all or nothing) but may involve multiple round trips. They can be combined — a pipelined transaction is possible.

## Q43: What is a Redis Lua script?
**A:** Redis supports executing Lua scripts server-side using `EVAL` or `EVALSHA`. Lua scripts run atomically, like transactions, and can include complex logic. They are often used for implementing custom atomic operations that would require multiple round trips otherwise.

## Q44: What are the advantages of Lua scripting in Redis?
**A:** (1) Atomic execution — script runs without interference from other commands. (2) Reduced network round trips — complex logic runs server-side. (3) Reusable — scripts are cached and can be executed by SHA digest. (4) Flexibility — custom data structures and operations.

## Q45: What is `EVALSHA` in Redis?
**A:** `EVALSHA` executes a Lua script by its SHA1 hash. Scripts are loaded with `SCRIPT LOAD` and cached on the server. `EVALSHA` avoids sending the script source over the network on each call, reducing bandwidth. `EVAL` sends the full script each time.

## Q46: What is a Redis lock and how do you implement a distributed lock?
**A:** A Redis lock is typically implemented using `SET key value NX EX timeout` (NX = create only if not exists, EX = expiry). The key acts as a lock. To release: delete the key only if it matches the owner's value (using Lua for atomicity). Redlock is Redis's distributed lock algorithm for multi-master setups.

## Q47: What is Redlock?
**A:** Redlock is a distributed lock algorithm proposed by Redis's creator. It acquires locks on an odd number (typically 5) of independent Redis masters. A lock is considered acquired if a majority (N/2 + 1) of instances respond successfully. This provides fault tolerance in distributed systems.

## Q48: What are the alternatives to Redlock?
**A:** Alternatives include: (1) Using a single Redis instance with replication (simpler but less fault-tolerant). (2) Using ZooKeeper or etcd for distributed locks (stronger consistency guarantees). (3) Using database-based locks (PostgreSQL advisory locks). Redlock has been debated for its correctness in certain failure scenarios.

## Q49: What is a Redis sorted set?
**A:** A sorted set is a collection of unique strings (members) each associated with a floating-point score. Members are ordered by score. Commands: `ZADD key score member`, `ZRANGE key start stop`, `ZRANK key member`, `ZSCORE key member`. Used for leaderboards, rate limiting, and priority queues.

## Q50: What are common use cases for Redis sorted sets?
**A:** (1) Leaderboards — gaming scores ordered by rank. (2) Rate limiting — sliding window with timestamps as scores. (3) Autocomplete with weights — weighted suggestions. (4) Priority queues — processing items by priority score. (5) Time-based event ordering.

## Q51: What is a Redis HyperLogLog?
**A:** HyperLogLog is a probabilistic data structure that estimates the cardinality (unique count) of a set using very little memory (12KB per key, regardless of element count). Error rate is approximately 0.81%. Commands: `PFADD`, `PFCOUNT`, `PFMERGE`. Used for unique visitor counting.

## Q52: What is a Redis bitmap?
**A:** A bitmap is a string on which bit-level operations can be performed. Redis treats strings as arrays of bits (up to 2^32 bits). Commands: `SETBIT`, `GETBIT`, `BITCOUNT`, `BITOP`, `BITFIELD`. Used for feature flags, user sign-in tracking, and real-time analytics.

## Q53: What is Redis Geospatial indexing?
**A:** Redis geospatial support allows storing and querying location data (longitude, latitude). Commands: `GEOADD`, `GEORADIUS`, `GEODIST`, `GEOPOS`. Internally uses sorted sets with Geohash encoding. Used for location-based features, nearby searches, and mapping applications.

## Q54: What is Redis as a message broker?
**A:** Redis can act as a lightweight message broker using Pub/Sub for real-time broadcasting or Lists/Streams for reliable message queues. Lists with `BLPOP`/`BRPOP` provide blocking pop operations suitable for simple work queues. Streams with consumer groups provide robust message delivery.

## Q55: How do you implement a queue with Redis Lists?
**A:** Producer uses `LPUSH` to add items to a list. Consumer uses `RPOP` (or `BRPOP` for blocking). For reliable queues, items are popped and processed with acknowledgment. For delayed retry, a separate "pending" or "retry" list can be used.

## Q56: What is `BRPOP` and `BLPOP`?
**A:** `BRPOP` and `BLPOP` are blocking list pop operations. They remove and return the last/first element of a list, but block the connection if the list is empty until an element is available (or a timeout is reached). They are used for implementing blocking queues.

## Q57: What is `RPOPLPUSH` and `BRPOPLPUSH`?
**A:** `RPOPLPUSH` atomically pops the last element of a source list and pushes it to the front of a destination list. `BRPOPLPUSH` is the blocking variant. This is useful for reliable message delivery — if a consumer crashes, the message remains in the destination list for reprocessing.

## Q58: What is Redis as a session store?
**A:** Redis is widely used for storing user sessions due to its speed and TTL support. Sessions are stored as hashes or strings with a session ID as the key and a TTL matching the session timeout. Redis-session stores are used in Express, Django, Spring, and other frameworks.

## Q59: How does Redis handle concurrency?
**A:** Redis is single-threaded for command execution, meaning commands are serialized — no race conditions within a single Redis instance. However, client-side race conditions can occur (e.g., read-modify-write patterns). Transactions, Lua scripts, or WATCH are used for atomic operations.

## Q60: Why is Redis single-threaded and how does it perform well?
**A:** Redis is single-threaded for command execution because most operations are in-memory and fast — the bottleneck is typically network I/O, not CPU. Single-threaded design eliminates locking overhead and simplifies code. I/O multiplexing (epoll/kqueue) handles thousands of connections efficiently.

## Q61: What is Redis I/O multiplexing?
**A:** Redis uses I/O multiplexing (epoll on Linux, kqueue on macOS/FreeBSD, select on other platforms) to handle many client connections in a single thread. It monitors multiple file descriptors and processes ready connections, achieving high throughput without multi-threading.

## Q62: What is Redis 6's threaded I/O?
**A:** Redis 6 introduced threaded I/O for reading/writing data from/to sockets. While command execution remains single-threaded, I/O operations (network reads and writes) can use multiple threads. This improves performance on multi-core systems with many concurrent connections.

## Q63: What is Redis RESP protocol?
**A:** RESP (REdis Serialization Protocol) is the protocol used by Redis clients to communicate with the server. It is a text-based protocol with binary-safe payloads. RESP3 (introduced in Redis 6) is the newer version supporting typed replies and push notifications.

## Q64: What is Redis Modules API?
**A:** The Redis Modules API allows extending Redis with custom data structures and commands written in C. Popular modules include RediSearch (full-text search), RedisJSON (native JSON operations), RedisGraph (graph database), RedisTimeSeries, RedisBloom, and RedisAI.

## Q65: What is RediSearch?
**A:** RediSearch is a Redis module that provides full-text search, secondary indexing, and query capabilities. It supports tokenization, stemming, fuzzy matching, auto-complete, sorting, aggregations, and vector similarity search. It is built on top of Redis.

## Q66: What is RedisJSON?
**A:** RedisJSON is a Redis module that provides native JSON data type and operations. It allows storing, querying, and manipulating JSON documents at the field level (e.g., `JSON.GET doc $.field`, `JSON.SET doc $.field "value"`). It supports JSONPath expressions.

## Q67: What is RedisGraph?
**A:** RedisGraph is a Redis module that implements a graph database. It uses sparse adjacency matrices and the Property Graph model. Queries are expressed in Cypher (graph query language). It supports nodes, relationships, and graph algorithms like shortest path.

## Q68: What is a Redis backup strategy?
**A:** A Redis backup strategy includes: (1) Regular RDB snapshots (scheduled `BGSAVE`). (2) AOF persistence for crash recovery. (3) Replication (read replicas for failover). (4) Periodic backup copies of RDB/AOF files to offsite storage (S3, etc.). (5) Testing backups by restoring to a different instance.

## Q69: How do you monitor Redis?
**A:** Monitoring tools and methods: (1) `INFO` command — detailed server stats. (2) `MONITOR` — real-time command tracing (use cautiously in production). (3) `SLOWLOG` — slow queries. (4) `CLIENT LIST` — connected clients. (5) `LATENCY` commands — latency spikes. (6) Redis Insight — GUI tool. (7) Prometheus + Grafana with redis_exporter.

## Q70: What is Redis `SLOWLOG`?
**A:** `SLOWLOG` captures commands that exceed a specified execution time threshold (configurable via `slowlog-log-slower-than`, default 10ms). It records the command, timestamp, duration, and client info. Use `SLOWLOG GET N` to retrieve entries. It helps identify performance issues.

## Q71: What are Redis keyspace notifications?
**A:** Keyspace notifications allow clients to subscribe to events like key expiration, eviction, creation, or modification via Pub/Sub. Configured with `notify-keyspace-events` option (e.g., `Ex` for expiration events). Used for cache invalidation, session cleanup, and reactive programming.

## Q72: What is Redis `SCAN` command?
**A:** `SCAN` iterates over keys in the database incrementally, returning batches of keys. Unlike `KEYS` (which blocks the server), `SCAN` is cursor-based and non-blocking. Variants: `SSCAN` (sets), `HSCAN` (hashes), `ZSCAN` (sorted sets). It is the recommended way to iterate large datasets.

## Q73: Why is `KEYS` command dangerous in production?
**A:** `KEYS pattern` scans all keys and blocks Redis entirely until complete. On a large database, this can block for seconds or minutes, causing all other operations to queue. `SCAN` should be used instead as it returns results incrementally without blocking.

## Q74: What is `INFO` command in Redis?
**A:** `INFO` returns detailed statistics about the Redis server, including: server info, clients, memory usage, persistence stats, replication status, CPU usage, keyspace stats, and cluster info. Sections can be queried individually (e.g., `INFO memory`).

## Q75: What is Redis memory optimization?
**A:** Techniques include: (1) Using appropriate data structures (hashes for objects instead of many strings). (2) Using `ziplist` encoding for small hashes/lists/sorted sets. (3) Setting `maxmemory` with appropriate eviction. (4) Using `MEMORY USAGE` to inspect key memory. (5) Sharding large datasets across instances.

## Q76: What is Redis `ziplist` encoding?
**A:** Ziplist is a memory-efficient encoding for small hashes, lists, and sorted sets. It stores data as a contiguous byte array instead of linked structures. Redis automatically converts to ziplist when elements are small (configurable thresholds: `hash-max-ziplist-entries`, etc.).

## Q77: What is Redis `intset` encoding?
**A:** Intset is a memory-efficient encoding for sets containing only integer members. It stores integers in a sorted, contiguous array. When non-integer elements are added or the set exceeds the threshold, it converts to a regular hash table.

## Q78: What is Redis memory fragmentation?
**A:** Memory fragmentation occurs when allocated memory exceeds the actual data size. Redis reports fragmentation ratio via `INFO memory` (`mem_fragmentation_ratio`). A ratio significantly > 1.5 indicates fragmentation. Causes: frequent alloc/free of varying sizes. Restarting or using jemalloc helps.

## Q79: What is Jemalloc?
**A:** Jemalloc is the default memory allocator for Redis. It is optimized for reducing memory fragmentation in multi-threaded applications and performs better than glibc's malloc for Redis workloads. Jemalloc provides detailed memory statistics via `INFO MEMORY`.

## Q80: What is Redis security best practices?
**A:** (1) Set a strong `requirepass`. (2) Bind to localhost/internal IPs only. (3) Disable `CONFIG` command via rename. (4) Use TLS for in-transit encryption. (5) Use ACLs (Redis 6+) for per-user permissions. (6) Disable dangerous commands via rename. (7) Run Redis as a non-root user.

## Q81: What are Redis ACLs?
**A:** Redis ACLs (Access Control Lists), introduced in Redis 6, allow per-user permission management. Users can be created with specific command permissions (e.g., `+GET -DEL` for allow GET, deny DEL) and key pattern restrictions (e.g., `~cache:*` for keys matching a pattern).

## Q82: What is Redis `rename-command`?
**A:** `rename-command` is a configuration option that renames or disables dangerous commands. Example: `rename-command FLUSHALL ""` disables FLUSHALL. `rename-command CONFIG 3a4b5c6d` renames CONFIG to a hard-to-guess string to prevent accidental or malicious use.

## Q83: What is Redis overcommit memory setting?
**A:** Redis requires the Linux kernel `vm.overcommit_memory = 1` setting when persistence is enabled. This allows background saving (fork) to succeed even if memory is overcommitted. Without it, `BGSAVE` and `BGREWRITEAOF` may fail if memory is low.

## Q84: What is the `transparent_hugepage` issue with Redis?
**A:** Transparent Huge Pages (THP) in Linux causes very slow fork times and high memory usage for Redis. It should be disabled (`echo never > /sys/kernel/mm/transparent_hugepage/enabled`) on Redis servers to improve performance and reduce latency.

## Q85: What is Redis latency monitoring?
**A:** Redis latency monitoring tracks command execution times and reports latency spikes. Commands include `LATENCY LATEST` (latest latency events), `LATENCY HISTORY` (history for a specific event), `LATENCY GRAPH` (ASCII graph), and `LATENCY DOCTOR` (advice on latency issues).

## Q86: What is a hot key in Redis?
**A:** A hot key is a key that receives a disproportionately high number of requests, potentially overloading a single Redis node. Solutions: (1) Local client-side caching. (2) Replicating the hot key across multiple shards. (3) Using read replicas to distribute reads.

## Q87: What is a big key in Redis?
**A:** A big key is a key with a very large value (e.g., a huge list, set, or string). Big keys cause memory imbalance, slow operations (e.g., `DEL`), and replication lag. Detection: `redis-cli --bigkeys` or `MEMORY USAGE key`. Split big keys into smaller chunks.

## Q88: How do you delete a big key without blocking Redis?
**A:** Use `UNLINK` instead of `DEL` — it deletes the key in a background thread, returning immediately. `DEL` is synchronous and blocks Redis for large keys. Alternatively, iteratively delete elements from the data structure in batches.

## Q89: What is `UNLINK` in Redis?
**A:** `UNLINK` is a non-blocking delete introduced in Redis 4.0. It reclaims memory in a background thread. The key is immediately unlinked from the keyspace (becomes inaccessible), and memory is freed asynchronously. Use `UNLINK` for large keys, `DEL` for small ones.

## Q90: What is the difference between `DEL` and `UNLINK`?
**A:** `DEL` is synchronous — it blocks Redis until the key is fully deleted (problematic for large keys). `UNLINK` is asynchronous — it unlinks the key immediately and reclaims memory in a background thread. Both remove the key from the keyspace.

## Q91: What is Redis connection pooling?
**A:** Connection pooling maintains a pool of Redis connections that can be reused, avoiding the overhead of creating new connections for each operation. Most Redis client libraries (Jedis, ioredis, redis-py) support connection pooling. Pool size should match workload and Redis capacity.

## Q92: What is Redis Client Side Caching?
**A:** Introduced in Redis 6, client-side caching allows clients to cache data locally. Redis tracks keys accessed by clients and sends invalidation messages when those keys change. This reduces network round trips and latency for frequently accessed keys.

## Q93: What is Redis on Flash?
**A:** Redis on Flash (part of Redis Enterprise) extends RAM with flash storage (SSD/NVMe). Hot data stays in RAM, while less-frequently accessed data is stored on flash. This provides larger capacity at lower cost while maintaining low latency for active data.

## Q94: What is Redis Enterprise?
**A:** Redis Enterprise is a commercial offering by Redis Labs that extends open-source Redis with: active-active geo-distribution, Redis on Flash, faster clustering, advanced security (RBAC, audit logs), multi-tenant management, and 24/7 support. It is available as self-hosted or cloud service.

## Q95: What is Redis Time Series?
**A:** RedisTimeSeries is a Redis module for time-series data. It supports high-throughput ingestion, downsampling/aggregation, retention policies, labels for metadata, and integration with Prometheus and Grafana. Used for IoT, monitoring, and financial data.

## Q96: How do you migrate data between Redis instances?
**A:** Methods include: (1) `MIGRATE` command — atomically transfers a key to another instance. (2) `DUMP`/`RESTORE` — serialize and deserialize keys. (3) RDB file transfer — copy the dump file. (4) Replication — set up the new instance as a replica, then promote it. (5) Redis Enterprise's built-in migration.

## Q97: What is Redis Persistence for caching?
**A:** When Redis is used as a cache, persistence may be unnecessary — if data is lost, it can be rebuilt from the source database. However, some caches benefit from persistence to avoid cold starts. The trade-off is between durability and write performance.

## Q98: What is Redis Cluster resharding?
**A:** Resharding moves hash slots between nodes in a Redis Cluster, typically to rebalance data when adding or removing nodes. Redis Cluster supports online resharding using `redis-cli --cluster reshard`. Slots are migrated incrementally without cluster downtime.

## Q99: What is the gossip protocol in Redis Cluster?
**A:** Redis Cluster nodes use a gossip protocol to exchange information about cluster state, node health, and configuration. Nodes periodically ping random other nodes, exchanging `PONG` messages with cluster information. This enables decentralized failure detection and configuration propagation.

## Q100: What is the difference between Redis and other NoSQL databases?
**A:** Unlike document DBs (MongoDB) or wide-column stores (Cassandra), Redis is primarily an in-memory data structure store optimized for speed. It sacrifices query complexity and storage capacity for sub-millisecond latency. Redis excels at caching, real-time analytics, and transient data. Other NoSQL DBs offer richer queries, larger capacity, and different consistency models.
