## 5. Redis (141–170)

141. What is Redis?
     R**Answer:** Redis is an in-memory data structure store used as a database, cache, and message broker. It supports data structures like strings, hashes, lists, sets, sorted sets, streams, and bitmaps with sub-millisecond latency and built-in replication.

142. Explain Redis data structures.
     R**Answer:** Redis supports Strings (text/numbers), Hashes (field-value maps), Lists (ordered sequences), Sets (unique unordered elements), Sorted Sets (unique elements with scores), Bitmaps (bit-level operations), HyperLogLogs (cardinality estimation), Streams (append-only logs), and Geospatial indexes.

143. Difference between Redis and PostgreSQL?
     R**Answer:** Redis is an in-memory store optimized for speed, best for caching, real-time data, and ephemeral state. PostgreSQL is a disk-based relational database for persistent, complex, ACID-compliant data with rich querying, while Redis trades durability and query complexity for performance.

144. Explain Redis caching strategies.
     C**Answer:** Common strategies include Cache Aside (app checks cache first, then DB), Read-Through (cache loads from DB automatically), Write-Through (cache updated synchronously on write), Write-Behind (async write to DB), and Refresh-Ahead (cache pre-fetches expiring keys).

145. What is cache invalidation?
     C**Answer:** Cache invalidation removes or updates cached data when the underlying source changes. Strategies include TTL-based expiration, event-driven invalidation (purging on data update), and key-based invalidation (deleting specific keys related to changed data).

146. Explain TTL in Redis.
     T**Answer:** TTL (Time-To-Live) sets an expiration time on keys using `EXPIRE`, `SETEX`, or `SET ... EX`. Redis automatically deletes expired keys, with active expiration (checked on access) and lazy expiration (periodic sampling of expiring keys).

147. What are Redis hashes?
     H**Answer:** Hashes are maps of field-value pairs, ideal for storing objects like user profiles. They allow `HGET`, `HSET`, `HGETALL` operations and are memory-efficient for small objects, supporting partial reads and writes without transferring entire objects.

148. Explain Redis pub/sub.
     P**Answer:** Pub/Sub enables publisher-subscriber messaging where publishers send messages to channels and subscribers receive them in real time. It's fire-and-forget — messages are not persisted, and disconnected subscribers miss messages. Used for real-time notifications and event broadcasting.

149. What are sorted sets?
     S**Answer:** Sorted sets are collections of unique elements with associated float scores, ordered by score. They support range queries, rank operations, and score-based commands like `ZADD`, `ZRANGE`, `ZRANK`, `ZINCRBY`, making them ideal for leaderboards and priority queues.

150. Explain Redis persistence.
     R**Answer:** Redis offers two persistence options: RDB (snapshots at intervals) and AOF (logs every write operation). They can be used separately or together. RDB is faster for recovery, while AOF provides better durability with configurable fsync policies.

151. Difference between RDB and AOF?
     R**Answer:** RDB creates point-in-time snapshots of the dataset, which are compact and fast to load but may lose data between snapshots. AOF logs every write operation, providing better durability with second-level granularity, but produces larger files and slower recovery.

152. What are Redis streams?
     S**Answer:** Streams are append-only logs that store ordered messages with unique IDs. They support consumer groups for distributed processing, blocking reads, range queries, and message acknowledgment — making them suitable for event sourcing, message queues, and activity feeds.

153. Explain Redis clustering.
     R**Answer:** Redis Cluster automatically shards data across multiple nodes using hash slots (16384 total). It provides high availability through automatic failover, linear scalability by adding nodes, and maintains performance while handling partial node failures.

154. What is Redis Sentinel?
     S**Answer:** Sentinel provides high availability by monitoring Redis masters and replicas, automatically performing failover when a master fails. It handles leader election, configuration propagation, and client discovery via its API.

155. How does rate limiting work with Redis?
     R**Answer:** Rate limiting uses `INCR` with TTL — increment a key per user/IP, check against the limit, and expire after the window. Advanced sliding window approaches use sorted sets to track timestamps of recent requests for precise counting.

156. Explain distributed locks.
     D**Answer:** Distributed locks use Redis's `SET key value NX EX <ttl>` command with Redlock algorithm for consensus across multiple nodes. Locks prevent race conditions in distributed systems by ensuring exclusive access to shared resources, with proper timeout handling.

157. What are Redis transactions?
     T**Answer:** Transactions use `MULTI` to queue commands, `EXEC` to execute atomically, and `DISCARD` to cancel. They guarantee isolation but not rollback — if one command fails, others still execute. Optimistic locking with `WATCH` provides conditional execution.

158. Explain Lua scripting in Redis.
     L**Answer:** Lua scripts (`EVAL`/`EVALSHA`) run atomically on the Redis server, combining multiple commands into a single atomic operation. They reduce network round trips, ensure atomicity for complex operations, and can conditionally execute based on key values.

159. How do you secure Redis?
     S**Answer:** Secure Redis by setting a strong `requirepass`, disabling dangerous commands via `rename-command`, binding to localhost or using firewalls, enabling TLS for connections, and never exposing Redis to the public internet without authentication.

160. Explain memory eviction policies.
     E**Answer:** Eviction policies control what data is removed when memory is full: `noeviction` (returns errors), `allkeys-lru` (evicts least recently used), `volatile-lru` (LRU among keys with TTL), `allkeys-lfu` (least frequently used), `volatile-ttl` (shortest TTL first).

161. What causes cache stampede?
     C**Answer:** Cache stampede (thundering herd) occurs when many requests simultaneously miss the cache and hit the database, overwhelming it. Solutions include request coalescing (single request reloads cache), early recomputation (renewing cache before expiry), and locks.

162. Explain cache aside pattern.
     C**Answer:** Cache Aside (lazy loading) is the most common pattern: application checks cache first, returns cached data if hit, queries the database on miss, stores result in cache with TTL, and invalidates cache on writes. The cache is passive.

163. What is write-through caching?
     W**Answer:** Write-through cache updates both cache and database synchronously on every write, ensuring consistency at the cost of write latency. It guarantees the cache is always fresh but writes must succeed in both locations.

164. Explain Redis pipelines.
     P**Answer:** Pipelines batch multiple commands into a single network round trip, reducing latency. Unlike transactions, pipelines don't guarantee atomic execution — they simply send commands together and read all responses at once, improving throughput.

165. How do you monitor Redis?
     M**Answer:** Monitor using `INFO` for server stats, `MONITOR` for real-time commands, `SLOWLOG` for slow queries, Redis CLI for live metrics, and tools like RedisInsight, Grafana with Prometheus exporters, and cloud provider monitoring for memory, CPU, and hit rate.

166. Explain session management with Redis.
     R**Answer:** Redis stores session data as key-value pairs with TTL for automatic expiration. Its fast read/write and built-in expiration make it ideal for session storage. Session IDs are stored in cookies and looked up on each request.

167. What are Bloom filters?
     B**Answer:** Bloom filters are probabilistic data structures that test set membership with no false negatives but possible false positives. They use multiple hash functions and a bit array, efficiently checking if an item is "definitely not in set" or "probably in set."

168. Explain Redis in microservices.
     R**Answer:** Redis serves as a shared cache, session store, rate limiter, message broker (pub/sub/streams), and distributed lock manager across microservices. It enables fast data sharing between services and supports event-driven architectures.

169. What are hot keys?
     H**Answer:** Hot keys are frequently accessed keys that cause disproportionate load on a single Redis node in a cluster. Mitigation includes splitting hot keys (key:shard:1, key:shard:2), adding local caches (client-side caching), or replicating read-only copies.

170. How do you scale Redis?
     S**Answer:** Scale Redis vertically (more memory/CPU on single node), horizontally with Redis Cluster (sharding), or using read replicas for read-heavy workloads. For write-heavy workloads, shard application-level data across multiple clusters by business domain.
