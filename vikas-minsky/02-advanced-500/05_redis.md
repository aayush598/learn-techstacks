## 24. Redis Advanced (641–670)

641. Explain Redis replication internals.
   Redis replication uses a leader-follower model. The leader sends a full RDB snapshot to followers on initial sync, then streams incremental commands via a replication buffer. Followers acknowledge offsets to track progress.

642. How does Redis achieve high performance?
   Redis achieves high performance through in-memory data storage, an event-driven single-threaded reactor model (avoiding locks), efficient data structures (skip lists, hash tables), and O(1) operations on core data types.

643. Explain single-threaded architecture.
   Redis uses a single thread for command execution, eliminating race conditions and locking overhead. I/O is handled via epoll/kqueue, while blocking operations like `SAVE` fork a child process.

644. What are Redis modules?
   Redis modules are dynamic libraries (written in C/Rust) that extend Redis with new commands, data types, and capabilities. Examples include RediSearch, RedisJSON, RedisGraph, and RedisBloom.

645. Explain HyperLogLog.
   HyperLogLog is a probabilistic data structure for cardinality estimation (counting unique elements) using ~12KB of memory. It provides approximate counts (0.81% error) with `PFADD`, `PFCOUNT`, and `PFMERGE` commands.

646. What are geospatial indexes?
   Redis geospatial indexes store latitude/longitude coordinates in sorted sets using geohash encoding. Commands like `GEOADD`, `GEORADIUS`, and `GEODIST` enable location-based queries.

647. Explain distributed caching.
   Distributed caching spans multiple nodes (Redis Cluster or client-side sharding). It distributes keys across shards, providing horizontal scalability but requiring careful handling of cache invalidations and consistency.

648. How do cache warming strategies work?
   Cache warming pre-populates the cache before traffic arrives by replaying recent queries from logs or seeding critical data on startup. It prevents cold-start cache misses that degrade performance.

649. Explain consistency problems in caching.
   Cache consistency issues include stale data (cache not updated after DB write), thundering herd (many requests miss cache simultaneously), and eventual consistency when replicas serve outdated values.

650. What are write-behind caches?
   Write-behind caches write data to the primary cache first and asynchronously flush to the database. This reduces write latency but risks data loss if the cache fails before flushing.

651. Explain Redis failover scenarios.
   Redis Sentinel monitors the primary, triggers automatic failover by promoting a replica, and updates clients with the new primary address. During failover, writes may be lost if not fully replicated.

652. How does Redis clustering partition data?
   Redis Cluster uses 16,384 hash slots, assigned to nodes. Each key's hash slot is computed via CRC16 modulo 16384. Operations on multi-key commands require keys in the same slot (using hash tags).

653. Explain gossip protocols.
   Redis Cluster nodes exchange state information (node health, slot assignments) via a gossip protocol. Each node periodically pings random peers, spreading cluster changes without a central coordinator.

654. What are quorum writes?
   Quorum writes in Redis Cluster require acknowledgment from a majority of replicas. With `WAIT`, you can ensure a minimum number of replicas acknowledge before the primary confirms the write.

655. Explain eviction tuning.
   Eviction policies like `allkeys-lru`, `volatile-ttl`, `noeviction` control how Redis frees memory. Tuning includes setting `maxmemory`, choosing the right policy for access patterns, and monitoring `evicted_keys`.

656. What causes memory fragmentation?
   Memory fragmentation occurs when Redis allocates and frees varying sizes of memory, leaving gaps. Jemalloc allocator reduces fragmentation, but high fragmentation ratio (>1.5) may require `MEMORY PURGE`.

657. Explain Redis latency spikes.
   Latency spikes stem from fork-based `BGSAVE` (copy-on-write overhead), AOF rewrite, large key operations, swap usage, or network congestion. Monitoring with `LATENCY DOCTOR` helps diagnose causes.

658. How do pipelines reduce RTT?
   Pipelines batch multiple commands into a single network round trip, reducing latency from cumulative RTT. Commands are sent together and responses read afterward, improving throughput for bulk operations.

659. Explain Redis benchmarking.
   Benchmarking uses `redis-benchmark` to test throughput (ops/sec) under various payload sizes, connection counts, and pipelines. Metrics include latency percentiles (p50, p99) and max throughput.

660. What are cache penetration attacks?
   Cache penetration occurs when attackers request non-existent keys, causing repeated database misses. Mitigations include Bloom filters, null-value caching with short TTL, and rate limiting.

661. Explain cache poisoning.
   Cache poisoning happens when malicious data is stored in the cache (via compromised input or headers). It spreads to users reading the cache. Validate all data before caching, and use short TTLs.

662. How do token buckets work?
   Token bucket rate limiting maintains a bucket with a maximum capacity that refills at a fixed rate. Each request consumes a token; if empty, the request is denied. Redis `INCR` with expiry implements it.

663. Explain sliding window rate limiting.
   Sliding window tracks request timestamps in a sorted set per user. It counts requests in the last N seconds using `ZCOUNT` or `ZREMRANGEBYSCORE`, offering precise rate limiting without clock boundaries.

664. What are delayed queues?
   Delayed queues hold tasks scheduled for future execution. Redis sorted sets with timestamps as scores enable polling: workers pop items where `score <= now`.

665. Explain pub/sub delivery guarantees.
   Redis pub/sub provides at-most-once delivery — messages are lost if subscribers are disconnected. It doesn't persist messages or acknowledge consumption, making it unsuitable for reliable messaging.

666. How do streams support consumer groups?
   Redis Streams with `XREADGROUP` support consumer groups: each message is delivered to one consumer per group, with pending entries (PEL) for acknowledgment. `XACK` marks messages as processed.

667. Explain Redis backup strategies.
   Redis backups use RDB snapshots (periodic `SAVE`/`BGSAVE`) or AOF logs (append-only command sequences). Best practice combines both: RDB for fast recovery and AOF for durability.

668. What are persistence tradeoffs?
   RDB trades durability for performance (snapshot intervals mean possible data loss). AOF provides better durability (configurable fsync policy) but larger files and slower recovery. Use both for most critical data.

669. Explain Redis observability metrics.
   Key metrics include `used_memory`, `hit_rate`, `evicted_keys`, `connected_clients`, `replication_lag`, `instantaneous_ops_per_sec`, and `latency_percentiles`. Redis `INFO` and `MONITOR` provide full observability.

670. How do you optimize Redis costs?
   Optimize costs by right-sizing instances (monitor memory usage), using eviction policies to limit maxmemory, consolidating small instances, enabling compression for large values, and leveraging Redis on shared infrastructure.
