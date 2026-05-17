## 43. Redis Expert Topics (1141–1170)

1141. How does Redis replication backlog work?

   **Answer:** The replication backlog is a fixed-size circular buffer on the primary that stores recent WAL-style commands. When a replica reconnects, it can use the backlog ID to catch up incrementally from its last offset, avoiding a full resync.

1142. Explain Redis event loop architecture.

   **Answer:** Redis uses a single-threaded event loop with multiplexed I/O (epoll/kqueue) that processes client commands, timer events, and background tasks sequentially. This eliminates locking overhead but means any slow command blocks all other operations.

1143. What are Redis latency monitors?

   **Answer:** Latency monitors sample command execution times and report percentiles when latency exceeds configurable thresholds. They help identify slow commands, fork delays from persistence, and system-level issues like swapping.

1144. Explain fork-based persistence costs.

   **Answer:** RDB snapshots and AOF rewrites fork a child process that writes the dataset copy-on-write. Forking doubles memory temporarily if pages are modified during the save, causing CPU spikes and potential OOM under memory pressure.

1145. How does copy-on-write affect Redis memory?

   **Answer:** When the parent process modifies a page after forking, the OS duplicates that page, increasing RSS. Heavy write traffic during persistence can cause the parent to grow to nearly double its original memory size.

1146. Explain Redis cluster failover election.

   **Answer:** In Redis Cluster, replicas monitor their primary via gossip protocol. If a primary is unreachable for `cluster-node-timeout`, replicas hold an election using a Raft-like mechanism where the replica with the most up-to-date replication offset wins.

1147. What are replication consistency windows?

   **Answer:** Asynchronous replication creates a window where acknowledged writes on the primary haven't reached the replica. A primary failure during this window causes data loss, proportional to network latency and write throughput.

1148. Explain cache hierarchy design.

   **Answer:** Cache hierarchies use multiple layers: L1 (in-memory app cache), L2 (Redis), and L3 (CDN). Requests hit the fastest layer first, falling through on miss, with each layer having different size, latency, and eviction characteristics.

1149. How do distributed locks fail?

   **Answer:** Distributed locks fail when the lock holder pauses (GC pause, network delay) beyond the lock TTL, another client acquires the lock, and the original holder resumes believing it still holds the lock. This violates mutual exclusion.

1150. Explain Redlock controversies.

   **Answer:** Redlock aims to provide distributed locks across multiple Redis nodes but is controversial because its correctness depends on synchronized clocks and network assumptions that don't hold in asynchronous systems. Many experts recommend alternatives.

1151. What are token revocation strategies?

   **Answer:** Token revocation strategies include blacklisting in Redis with TTL, short-lived tokens with refresh rotation, and bloom filters for revoked JWT IDs. Redis's atomic operations make it ideal for fast distributed revocation checks.

1152. Explain Redis as a primary database.

   **Answer:** Using Redis as a primary database requires understanding that it sacrifices durability (async persistence), consistency (eventual in cluster mode), and query flexibility for speed. Best suited for session stores, leaderboards, and realtime counters.

1153. How does append-only rewrite work?

   **Answer:** AOF rewrite compacts the append-only log by creating a new AOF file containing only the current dataset state, discarding redundant commands. This runs in a child process with copy-on-write, then atomically swaps the new file.

1154. Explain Redis stream consumer balancing.

   **Answer:** Stream consumer groups automatically distribute messages among consumers using pending entries and delivery acknowledgments. Failed consumers have their pending messages reassigned after a configured idle timeout.

1155. What are delayed job queue patterns?

   **Answer:** Delayed job queues use Redis sorted sets with timestamps as scores. Workers poll for jobs with scores ≤ now, process them, and remove completed entries. Streams with `XREAD BLOCK` provide an alternative with blocking semantics.

1156. Explain cache synchronization across regions.

   **Answer:** Cross-region cache synchronization uses active-passive replication or dual-write patterns where writes update both local and remote caches. Redis CRDT-based active-active replication (Redis Enterprise) resolves conflicts automatically.

1157. How do Redis shards rebalance?

   **Answer:** In Redis Cluster, hash slots are distributed across nodes. Rebalancing moves hash slots (and their keys) from overloaded nodes to underutilized ones using `CLUSTER SETSLOT` commands with incremental key migration.

1158. Explain large key management.

   **Answer:** Large keys (>10MB) cause network and memory issues: they block the event loop during transfer, fragment memory, and slow replication. Best practices include splitting them into smaller chunks, using compression, or moving to blob storage.

1159. What are Redis anti-patterns?

   **Answer:** Anti-patterns include using KEYS in production (blocking scan), storing unlimited data without eviction, overusing large hashes, not setting TTLs, running under-persistent configs, and mixing cache and data-store use in the same instance.

1160. Explain write amplification in persistence.

   **Answer:** Each write to Redis may be written to the AOF buffer, periodically synced to disk, and included in RDB snapshots. Frequent AOF fsyncs and large RDB saves amplify write I/O, impacting throughput.

1161. How do Redis pipelines affect throughput?

   **Answer:** Pipelines batch multiple commands into a single network round trip, dramatically increasing throughput by reducing latency overhead. They're not atomic—commands execute sequentially—but provide significant throughput gains.

1162. Explain active-active Redis architecture.

   **Answer:** Active-active architecture runs multiple writable Redis instances across regions that synchronize via CRDTs (Conflict-Free Replicated Data Types). Each node accepts writes locally, and conflicts are automatically resolved using data-type-specific merge strategies.

1163. What are split-brain scenarios?

   **Answer:** Split-brain occurs when a network partition isolates Redis cluster nodes into multiple groups, each believing it's the primary. This can cause data divergence when both groups accept writes, resolved by manual intervention or CRDT-based merging.

1164. Explain cache miss amplification.

   **Answer:** Cache miss amplification happens when one cache miss triggers multiple backend queries or cascading cache lookups, overwhelming the database. Mitigations include request coalescing, randomized TTLs, and pre-warming caches.

1165. How do ephemeral sessions scale?

   **Answer:** Ephemeral sessions scale by storing session data in Redis with short TTLs (15-60 min) that auto-renew on activity. Sharding sessions across a Redis Cluster distributes load, while persistent fallback (PostgreSQL) stores durable session state.

1166. Explain Redis ACL security.

   **Answer:** Redis ACLs (Access Control Lists) restrict user access to specific commands, keys (via glob patterns), and pub/sub channels. This limits blast radius in multi-tenant setups and prevents accidental destructive operations.

1167. What are observability best practices for Redis?

   **Answer:** Best practices include monitoring memory fragmentation ratio, cache hit rate, eviction rate, connected clients, replication lag, and slowlog. Tools like RedisInsight and Prometheus exporters provide comprehensive visibility.

1168. Explain memory allocator fragmentation.

   **Answer:** Redis's default allocator (jemalloc) can fragment memory when objects of varying sizes are allocated and freed, wasting up to 30% of RSS. Using `--maxmemory` with `pagesize` alignment and avoiding oversized keys reduces fragmentation.

1169. How do you benchmark Redis realistically?

   **Answer:** Realistic benchmarks use `redis-benchmark` with production-like payload sizes, pipeline depths, and concurrent client counts. They test the critical path with network latency simulation (via loopback or real network) and measure both latency and throughput.

1170. How do large SaaS companies structure caching?

   **Answer:** Large SaaS companies use multi-tier caching with Redis as a distributed L2 cache behind local L1 caches. They shard by tenant ID, enforce cache budgets per tenant, and use write-through patterns with async background refresh.
