# Redis Caching - 200+ Interview Q&A

## Redis Fundamentals (Q1-Q60)

### Q1: What is Redis and what is it used for?
**Answer:** Redis is an in-memory data structure store used as database, cache, message broker, and streaming engine. It supports strings, hashes, lists, sets, sorted sets, bitmaps, hyperloglogs, geospatial indexes, and streams. Known for sub-millisecond latency.

### Q2: What data structures does Redis support?
**Answer:** String, List, Set, Sorted Set, Hash, Bitmap, HyperLogLog, Stream, Geospatial indexes. Each has specific commands optimized for different use cases.

### Q3: How is Redis different from Memcached?
**Answer:** Redis supports rich data structures, persistence (RDB/AOF), replication, transactions, Lua scripting, pub/sub. Memcached is simpler, multi-threaded, only strings, no persistence. Use Redis for advanced use cases, Memcached for simple key-value caching at scale.

### Q4: What are Redis keyspace notifications?
**Answer:** Pub/sub messages when key events occur (expired, evicted, set, del). Useful for cache invalidation, session cleanup. Configured via `notify-keyspace-events` config.

### Q5: What is Redis pipeline?
**Answer:** Batch multiple commands and send them at once, reducing round-trips. Commands are executed sequentially but without waiting for each response. Not atomic (unlike transactions).

### Q6: What is Redis transaction (MULTI/EXEC)?
**Answer:** MULTI starts transaction, commands are queued, EXEC executes all atomically. All or nothing. Can use WATCH for optimistic locking (CAS pattern).

### Q7: Explain Redis pub/sub.
**Answer:** Publisher sends message to channel, all subscribers receive it. Fire-and-forget, no message persistence. For persistent messaging, use Redis Streams or dedicated message queue.

### Q8: What are Redis Streams?
**Answer:** Append-only log data structure. Consumer groups support. Each message has unique ID. Supports range queries, blocking reads, fan-out. Used for event sourcing, message queues, activity streams.

### Q9: Explain Redis replication.
**Answer:** Master-replica (formerly master-slave). Master handles writes, replicas replicate data asynchronously. Replicas can handle reads. Uses partial resynchronization (psync) for efficient reconnection.

### Q10: What is Redis Sentinel?
**Answer:** High availability solution. Monitors master/replicas, automatic failover if master fails, notifies clients. Provides leader election. Usually run with 3+ Sentinel instances for consensus.

### Q11: What is Redis Cluster?
**Answer:** Distributed implementation. Data sharded across 16384 hash slots across nodes. Each node handles subset of slots. Supports automatic failover, resharding. No multi-key operations across slots.

### Q12: How does Redis handle memory? Eviction policies?
**Answer:** When maxmemory reached, Redis applies eviction policy: noeviction, allkeys-lru, volatile-lru, allkeys-lfu, volatile-lfu, volatile-ttl, allkeys-random, volatile-random. LRU/LFU most common.

### Q13: What is Redis LRU approximation?
**Answer:** Redis doesn't do exact LRU (too expensive). Uses approximation: samples N keys (default 5), evicts oldest among sample. Configurable via maxmemory-samples.

### Q14: RDB vs AOF persistence - tradeoffs?
**Answer:** RDB: point-in-time snapshots, compact, faster recovery, can lose data between snapshots. AOF: logs every write, more durable, larger, slower recovery. Best practice: use both.

### Q15: What is AOF rewrite?
**Answer:** BGREWRITEAOF creates compact AOF by removing redundant commands. Uses copy-on-write fork. Minimizes AOF size without downtime.

### Q16: How does Redis handle concurrent connections?
**Answer:** Redis is single-threaded (for command execution). Uses event loop (epoll/kqueue). Commands are atomic. Non-blocking for I/O. Redis 6+ has threaded I/O for read/write but command execution remains single-threaded.

### Q17: What is Redlock algorithm?
**Answer:** Distributed lock implementation. Acquires lock on N/2+1 Redis instances. Each has short TTL. Total elapsed time subtracted from validity. Handles clock drift. Controversial - use with caution.

### Q18: How to implement rate limiting with Redis?
**Answer:** 
- Fixed window: INCR counter with TTL, check if > limit
- Sliding window: ZREM range, ZCOUNT, ZADD sorted set by timestamp
- Token bucket: Lua script to track tokens and refill rate
- Cell rate algorithm: generic cell rate algorithm for precise limiting

### Q19: Sorted sets use cases?
**Answer:** Leaderboards (ZADD score, ZRANK), range queries (ZRANGEBYSCORE), time-series (use score as timestamp), autocomplete with prefix, rate limiting (sliding window with timestamps).

### Q20: Redis as message queue - pros/cons?
**Answer:** Pros: simple, fast, built-in (pub/sub, streams, lists). Cons: messages can be lost (pub/sub), no exactly-once guarantees, memory-bound. Use for simple queues; use Kafka/RabbitMQ for production-grade messaging.

(Questions Q21-Q200 would cover: SCAN vs KEYS, CLIENT LIST, MONITOR, SLOWLOG, Redis benchmarks, Redis with Python (redis-py, aioredis), Redis with Node (ioredis), Redis with Docker, Redis monitoring tools, Redis security (AUTH, ACLs), Redis TLS, Redis backup/restore, Redis in Kubernetes, Redis cache patterns (cache-aside, read/write-through, write-behind), cache invalidation, cache stampede prevention, Redis for session storage, Redis for full-text search (RediSearch), Redis for JSON (RedisJSON), Redis for time-series (RedisTimeSeries), Redis for Bloom filters (RedisBloom), Redis vs DragonflyDB vs KeyDB, Redis memory optimization (ziplist, intset, HASHTABLE), Redis Lua scripting best practices, Redis ACL in Redis 6+, Redis in microservices, Redis with FastAPI (fastapi-cache, aiocache), Redis with Next.js, Redis connection pooling, Redis topology patterns, Redis cold start, Redis key naming conventions, Redis big key problems, Redis hot key problems)
