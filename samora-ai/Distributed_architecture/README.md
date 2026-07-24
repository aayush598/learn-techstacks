# Distributed Architecture Interview Questions and Answers

## Q1: What is a distributed system?
**A:** A distributed system is a collection of independent computers that communicate and coordinate with each other over a network to achieve a common goal. The components appear to users as a single coherent system. Examples include the internet, cloud computing platforms, and microservices architectures where multiple services work together.

## Q2: What are the advantages of distributed systems?
**A:** Advantages include: scalability (horizontal scaling by adding more machines), reliability (no single point of failure), performance (parallel processing and geographic distribution), resource sharing (hardware and data across nodes), and flexibility (independent components can be developed and deployed separately).

## Q3: What are the challenges of distributed systems?
**A:** Key challenges include: network partitions and latency, partial failures where some components fail while others continue, maintaining data consistency across nodes, ordering and synchronization of events, security across network boundaries, debugging and monitoring complexity, and the inherent unreliability of network communication.

## Q4: What is the CAP theorem?
**A:** The CAP theorem states that a distributed data store can only provide two of three guarantees simultaneously: Consistency (every read receives the most recent write), Availability (every request receives a response), and Partition tolerance (the system continues operating during network partitions). Since network partitions are inevitable, designers must choose between consistency and availability.

## Q5: What is the difference between CP and AP systems?
**A:** CP systems (Consistency + Partition tolerance) sacrifice availability during partitions — examples include HBase, MongoDB (with certain configurations), and Google Spanner. AP systems (Availability + Partition tolerance) sacrifice consistency during partitions — examples include Cassandra, DynamoDB, and CouchDB. The choice depends on whether consistency or availability is more critical.

## Q6: What is the PACELC theorem?
**A:** PACELC is an extension of CAP. It states: if there's a Partition (P), choose between Availability (A) and Consistency (C); Else (E), when running normally, choose between Latency (L) and Consistency (C). This captures the tradeoff even when no partition exists. For example, Cassandra is PA/EL (available during partitions, low latency when running normally).

## Q7: What is the CAP theorem's practical impact on system design?
**A:** In practice, CAP means you must design for network partitions since they inevitably occur. During a partition, you choose between serving potentially stale data (AP) or refusing requests (CP). Most systems adopt eventual consistency as a pragmatic middle ground, providing strong consistency only when needed (like for financial transactions).

## Q8: What is eventual consistency?
**A:** Eventual consistency is a consistency model where, after the last write operation, all replicas will eventually converge to the same state. There's no guarantee about when this will happen, but in practice it typically occurs within milliseconds to seconds. It provides high availability and low latency at the cost of temporarily inconsistent reads.

## Q9: What is the difference between strong and eventual consistency?
**A:** Strong consistency guarantees that every read reflects the most recent write — replicas are always in sync. Eventual consistency allows temporary divergence between replicas, which resolve over time. Strong consistency is achieved through synchronous replication (higher latency), while eventual consistency uses asynchronous replication (lower latency, higher availability).

## Q10: What are the different types of consistency models?
**A:** Consistency models include: strict/linearizable (strongest), sequential, causal, session, eventual (weakest), read-your-writes, monotonic reads, and read-after-write. Each provides different guarantees about the order and visibility of operations across distributed nodes. Stronger models provide more guarantees but at higher performance cost.

## Q11: What is a microservices architecture?
**A:** Microservices architecture structures an application as a collection of small, independent services that communicate over well-defined APIs. Each service is self-contained, independently deployable, organized around business capabilities, and can use different technologies. This contrasts with monolithic architecture where all components are tightly coupled.

## Q12: What is the difference between monolithic and microservices architecture?
**A:** Monolithic architecture bundles all functionality into a single deployable unit — simple to develop and deploy but difficult to scale and maintain at scale. Microservices decompose the application into independent services — easier to scale, deploy, and maintain individually but introduce complexity in communication, data management, and operational overhead.

## Q13: What is service decomposition?
**A:** Service decomposition is the process of breaking a monolithic application into smaller, independent microservices. Common strategies include decomposition by business capability (billing, inventory), by subdomain (DDD bounded contexts), by data ownership (each service owns its data), or by use case. The goal is high cohesion within services and loose coupling between them.

## Q14: What is the strangler fig pattern?
**A:** The strangler fig pattern is a migration strategy for gradually replacing a monolithic system with microservices. New functionality is built as separate services while the monolith continues to handle existing features. Over time, responsibilities are "strangled" from the monolith and migrated to new services until the monolith can be retired.

## Q15: What is an API Gateway?
**A:** An API Gateway is a single entry point for all client requests in a microservices architecture. It handles routing, authentication, rate limiting, load balancing, request aggregation, protocol translation, and caching. Examples include Kong, AWS API Gateway, Azure API Management, and NGINX. It simplifies client communication and centralizes cross-cutting concerns.

## Q16: What is the difference between synchronous and asynchronous communication in distributed systems?
**A:** Synchronous communication (REST, gRPC) requires the caller to wait for a response before continuing — simple but creates tight coupling and can cascade failures. Asynchronous communication (message queues, events) allows the caller to continue processing without waiting — better resilience and decoupling but introduces eventual consistency and complexity in tracking operations.

## Q17: What is a message queue?
**A:** A message queue is a middleware component that enables asynchronous communication between distributed services. Producers send messages to the queue, and consumers retrieve and process them. Queues provide decoupling, buffering, reliability (messages survive consumer failures), and load leveling (absorbing traffic spikes). Examples include RabbitMQ, Amazon SQS, and Azure Service Bus.

## Q18: What is the difference between a message queue and a message broker?
**A:** A message queue is a simple FIFO buffer for point-to-point communication. A message broker is a more comprehensive intermediary that supports multiple messaging patterns (point-to-point, publish-subscribe, request-reply), routing, transformation, and persistence. RabbitMQ and Apache Kafka are brokers; SQS is primarily a queue.

## Q19: What is the publish-subscribe pattern?
**A:** Publish-subscribe (pub-sub) is a messaging pattern where message senders (publishers) send messages to a topic without knowledge of receivers (subscribers). The message broker distributes copies of messages to all subscribers. This provides loose coupling — publishers and subscribers can be developed and scaled independently.

## Q20: What is Apache Kafka?
**A:** Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant, and durable data streaming. It stores messages in a distributed, append-only log across multiple brokers. Producers write to topics partitioned across brokers, and consumers read at their own pace. It supports both stream processing and event-driven architectures.

## Q21: What is the difference between Kafka and RabbitMQ?
**A:** Kafka is a distributed log optimized for high-throughput event streaming with message retention, replay, and ordering guarantees. RabbitMQ is a traditional message broker supporting multiple protocols with complex routing and acknowledgment. Kafka is better for event streaming, log aggregation, and stream processing. RabbitMQ is better for task queuing and complex routing.

## Q22: What is event sourcing?
**A:** Event sourcing is a pattern where state changes are stored as an immutable sequence of events rather than overwriting current state. The current state is derived by replaying events. This provides a complete audit trail, enables temporal queries, supports event replay for debugging, and works well with CQRS. Events are the source of truth.

## Q23: What is CQRS?
**A:** Command Query Responsibility Segregation (CQRS) separates read and write operations into different models. The write model handles commands and stores events or state changes. The read model is optimized for queries, often denormalized for fast reads. This allows independent scaling and optimization of read and write workloads.

## Q24: What is the difference between event sourcing and CQRS?
**A:** Event sourcing stores all state changes as events (the persistence pattern). CQRS separates read and write models (the architectural pattern). They complement each other well — event sourcing provides the event store for writes, while CQRS uses those events to build optimized read models. But each can be used independently.

## Q25: What is a service mesh?
**A:** A service mesh is an infrastructure layer that handles service-to-service communication in a microservices architecture. It provides traffic management (routing, load balancing), security (mTLS, authorization), observability (distributed tracing, metrics), and resilience (retries, circuit breaking) without requiring changes to application code. Examples include Istio, Linkerd, and Consul Connect.

## Q26: What is a circuit breaker pattern?
**A:** The circuit breaker pattern prevents cascading failures by monitoring service calls and "opening" the circuit when failures exceed a threshold. When open, requests fail fast without calling the downstream service. After a timeout, the circuit enters a half-open state to test recovery. This protects failing services from being overwhelmed and allows time for recovery.

## Q27: What is the retry pattern with exponential backoff?
**A:** This pattern automatically retries failed requests with progressively increasing delays between attempts. For example: retry after 1s, then 2s, then 4s, then 8s. The exponential backoff prevents overwhelming a struggling service. Adding jitter (random variation) prevents thundering herd problems where many clients retry simultaneously.

## Q28: What is a timeout pattern?
**A:** The timeout pattern sets a maximum wait time for a response from a remote service. If the service doesn't respond within the timeout period, the request is abandoned. Timeouts prevent requests from hanging indefinitely, free up resources, and enable failover to alternative services or cached responses. Every remote call should have a timeout.

## Q29: What is service discovery?
**A:** Service discovery is the mechanism by which services locate each other in a distributed system. It maintains a registry of available service instances and their locations. Approaches include client-side discovery (client queries a registry, e.g., Eureka), server-side discovery (load balancer routes requests, e.g., AWS ELB), and DNS-based discovery (e.g., Consul DNS).

## Q30: What is the difference between client-side and server-side service discovery?
**A:** In client-side discovery, the client queries a service registry and selects an instance to call directly. The client handles load balancing and failover. In server-side discovery, the client makes a request to a load balancer or router, which queries the registry and forwards the request. Client-side gives more control; server-side simplifies clients.

## Q31: What is distributed caching?
**A:** Distributed caching stores frequently accessed data across multiple nodes in a network to improve read performance and reduce database load. The cache is shared across application instances and provides low-latency data access. Examples include Redis Cluster, Memcached, and Hazelcast. Challenges include cache invalidation, consistency, and cache warming.

## Q32: What is the cache invalidation problem?
**A:** Cache invalidation is the process of removing or updating cached data when the underlying data changes. It's considered one of the hardest problems in computer science because determining when cached data is stale requires tracking all possible data mutations. Strategies include TTL (time-based), event-driven invalidation, and write-through caching.

## Q33: What are cache strategies (write-through, write-behind, write-around)?
**A:** Write-through writes to both cache and database simultaneously, ensuring consistency but adding write latency. Write-behind (write-back) writes to cache first and asynchronously to the database, improving write performance but risking data loss. Write-around writes directly to the database, bypassing the cache, which avoids cache pollution but increases read latency for new data.

## Q34: What is a load balancer?
**A:** A load balancer distributes incoming network traffic across multiple backend servers to ensure high availability, reliability, and performance. It routes requests based on algorithms (round-robin, least connections, IP hash, weighted), performs health checks, and can terminate SSL. Types include Layer 4 (TCP/UDP) and Layer 7 (HTTP) load balancers.

## Q35: What are common load balancing algorithms?
**A:** Round Robin distributes requests sequentially across servers. Least Connections routes to the server with fewest active connections. IP Hash uses a hash of the client IP for session affinity. Weighted Round Robin assigns more requests to powerful servers. Least Response Time routes to the fastest-responding server. Each has tradeoffs for different workload characteristics.

## Q36: What is consistent hashing?
**A:** Consistent hashing maps both servers and data to positions on a ring, minimizing redistribution when servers are added or removed. Instead of remapping all data (as with modular hashing), only a small fraction of keys need to move. This is crucial for distributed caches, distributed databases, and content delivery networks.

## Q37: What is a distributed transaction?
**A:** A distributed transaction spans multiple services or databases and must maintain ACID properties across all participants. The Two-Phase Commit (2PC) protocol coordinates transactions with a prepare phase and commit phase. Distributed transactions are complex, have performance overhead, and many architects prefer the Saga pattern as an alternative.

## Q38: What is the Two-Phase Commit (2PC) protocol?
**A:** 2PC coordinates distributed transactions with a coordinator and participants. Phase 1 (prepare): the coordinator asks all participants to prepare and they vote yes/no. Phase 2 (commit/abort): if all vote yes, the coordinator sends commit; otherwise, it sends abort. Drawbacks include blocking (participants lock resources), single point of failure (coordinator), and performance overhead.

## Q39: What is the Saga pattern?
**A:** The Saga pattern manages distributed transactions as a sequence of local transactions, each with a compensating action for rollback. If a step fails, compensating transactions execute in reverse order. Two implementations: choreography (services emit and listen to events) and orchestration (a central coordinator directs the saga steps). Sagas trade strict consistency for availability and performance.

## Q40: What is the difference between choreography and orchestration in Sagas?
**A:** In choreography-based sagas, each service decides what to do next based on events — services are loosely coupled but the flow is decentralized and hard to understand. In orchestration-based sagas, a central coordinator directs the workflow — easier to understand and modify but introduces a single point of coordination.

## Q41: What is distributed tracing?
**A:** Distributed tracing tracks requests as they flow through multiple services in a distributed system. Each request gets a unique trace ID, and each service creates a span with timing and metadata. Traces reveal the full request path, identify bottlenecks, and diagnose errors. Tools include Jaeger, Zipkin, AWS X-Ray, and OpenTelemetry.

## Q42: What are OpenTelemetry and OpenTracing?
**A:** OpenTelemetry is a vendor-neutral observability framework providing APIs, libraries, and agents for collecting traces, metrics, and logs. It merged OpenTracing and OpenCensus. OpenTracing was the standard API for distributed tracing. OpenTelemetry provides a unified standard for all three pillars of observability (traces, metrics, logs).

## Q43: What is the difference between monitoring and observability?
**A:** Monitoring involves collecting and analyzing predefined metrics and logs to detect known issues (reactive). Observability is the ability to understand a system's internal state from its external outputs — it enables investigating unknown issues and answering questions you didn't anticipate. Monitoring tells you what's wrong; observability tells you why.

## Q44: What are the three pillars of observability?
**A:** The three pillars are: Metrics (numerical time-series data like CPU usage, request latency, error rates), Logs (timestamped event records providing detailed context), and Traces (distributed request paths across services). Together they provide comprehensive visibility into system behavior and enable correlation between symptoms and root causes.

## Q45: What is the leader election pattern?
**A:** Leader election is a pattern where distributed nodes elect one node as the leader to coordinate tasks and avoid conflicts. The leader handles scheduling, coordination, and single-writer scenarios. If the leader fails, a new leader is elected. Implementations use consensus algorithms like Raft, Paxos, or lease-based mechanisms with ZooKeeper or etcd.

## Q46: What is consensus in distributed systems?
**A:** Consensus is the process by which distributed nodes agree on a single value or state despite failures. Key algorithms include Paxos (complex, proven), Raft (understandable alternative to Paxos), and ZAB (used by ZooKeeper). Consensus ensures that decisions are made correctly even with message delays, duplicates, and node failures.

## Q47: What is the Raft consensus algorithm?
**A:** Raft is a consensus algorithm designed for understandability. It elects a leader to manage replication, maintains log consistency across nodes, and handles leader failures through elections. Nodes are in one of three states: leader, follower, or candidate. The leader appends entries to its log and replicates them to followers. A majority is needed for commit.

## Q48: What is distributed locking?
**A:** Distributed locking provides mutual exclusion across multiple nodes to prevent concurrent access to shared resources. Implementations include Redis-based locks (Redlock algorithm), ZooKeeper locks, and etcd locks. Considerations include lock expiration (to prevent deadlocks), fencing tokens (to prevent stale locks), and the tradeoffs between safety and performance.

## Q49: What is the Redlock algorithm?
**A:** Redlock is a distributed locking algorithm using Redis. The client acquires the lock by requesting it from N independent Redis nodes with a TTL. The lock is considered acquired if a majority of nodes grant it and the total time spent acquiring is less than the lock validity time. Controversy exists about its safety guarantees under certain network conditions.

## Q50: What is eventual consistency and when is it acceptable?
**A:** Eventual consistency is acceptable when: stale data doesn't cause critical issues (social media feeds, search indices), high availability is more important than immediate consistency, read-heavy workloads benefit from lower latency, and the application can tolerate brief windows of data divergence (shopping carts, analytics dashboards).

## Q51: What is a distributed database?
**A:** A distributed database stores data across multiple nodes or locations while presenting a unified interface. It provides horizontal scalability, fault tolerance, and geographic distribution. Types include distributed relational databases (CockroachDB, Google Spanner) and NoSQL distributed databases (Cassandra, DynamoDB, MongoDB).

## Q52: What is database sharding?
**A:** Sharding distributes data across multiple database instances (shards) based on a shard key. Each shard contains a subset of the total data, enabling horizontal scaling. Strategies include hash-based (uniform distribution), range-based (ordered data), and directory-based (lookup service). Sharding adds complexity for cross-shard queries, rebalancing, and maintaining consistency.

## Q53: What is the difference between replication and sharding?
**A:** Replication copies the same data across multiple nodes for redundancy and read scaling (all nodes have the same data). Sharding splits data across nodes where each node holds different data for write scaling (each node has different data). Replication improves availability; sharding improves capacity. They can be combined.

## Q54: What is a master-slave replication topology?
**A:** In master-slave (primary-replica) replication, the master node handles all writes and replicates data to slave nodes. Slaves handle read queries, providing read scaling. If the master fails, a slave can be promoted to master. Drawbacks include single point of write failure and potential replication lag causing stale reads from slaves.

## Q55: What is a multi-master replication topology?
**A:** Multi-master replication allows writes to multiple master nodes simultaneously. This provides write availability (if one master fails, others continue), geographic distribution of writes, and reduced write latency. Challenges include conflict resolution (when two masters modify the same data), increased complexity, and potential for write conflicts.

## Q56: What is conflict resolution in multi-master systems?
**A:** Conflict resolution handles simultaneous modifications to the same data on different masters. Strategies include: last-writer-wins (timestamp-based, simple but may lose data), merge functions (custom logic to combine changes), conflict-free replicated data types (CRDTs) that mathematically guarantee convergence, and application-level resolution.

## Q57: What are CRDTs?
**A:** Conflict-free Replicated Data Types (CRDTs) are data structures that can be replicated across nodes and merged without conflicts. They use mathematical properties (commutativity, associativity, idempotency) to guarantee eventual convergence regardless of the order of operations. Examples include G-Counters, PN-Counters, G-Sets, LWW-Registers, and OR-Sets.

## Q58: What is a G-Counter CRDT?
**A:** A Grow-only Counter (G-Counter) is a CRDT that only increments. Each node maintains its own count. The total value is the sum of all node counts. Incrementing adds to only the local node's count. Merge operation takes the maximum of each node's count. It cannot handle decrements (use PN-Counter for that).

## Q59: What is the CAP theorem's impact on database design?
**A:** CAP dictates that distributed databases must choose between consistency and availability during network partitions. CP databases (Spanner, HBase) reject requests during partitions to maintain consistency. AP databases (Cassandra, DynamoDB) serve potentially stale data to maintain availability. Modern systems often use tunable consistency to balance these tradeoffs per operation.

## Q60: What is the BASE model?
**A:** BASE stands for Basically Available, Soft state, Eventually consistent. It's the practical alternative to ACID in distributed systems. Basically Available guarantees a response (even if it's stale data). Soft state means the system state may change over time without input. Eventually consistent means it will converge to the same state given enough time.

## Q61: What is the difference between ACID and BASE?
**A:** ACID (Atomicity, Consistency, Isolation, Durability) prioritizes correctness and is typical of traditional relational databases. BASE (Basically Available, Soft state, Eventually consistent) prioritizes availability and performance, accepting temporary inconsistency for scalability. ACID suits financial transactions; BASE suits high-scale web applications.

## Q62: What is a distributed file system?
**A:** A distributed file system stores files across multiple machines while presenting a unified namespace to users. It provides fault tolerance through replication, scales horizontally, and supports concurrent access. Examples include HDFS (Hadoop Distributed File System), GFS (Google File System), and CephFS. They handle data placement, replication, and failure recovery automatically.

## Q63: What is consistent hashing and why is it important?
**A:** Consistent hashing maps both servers and keys onto a ring, ensuring that when a server is added or removed, only a minimal number of keys need to be remapped. This is critical for distributed caches, databases, and CDNs where naive hashing (key % N) causes massive data redistribution when the number of nodes changes.

## Q64: What is a virtual node (vnode) in consistent hashing?
**A:** Virtual nodes multiply each physical node's presence on the hash ring, creating multiple positions for each server. This improves load distribution (fewer hot spots), makes adding/removing nodes smoother, and allows heterogeneous servers to handle proportionally different amounts of data. More vnodes mean better balance but higher memory overhead.

## Q65: What is idempotency and why is it important in distributed systems?
**A:** Idempotency means an operation produces the same result regardless of how many times it's applied. It's crucial because in distributed systems, network issues can cause retries — an idempotent operation can safely be retried without side effects. Examples: HTTP GET is idempotent; HTTP POST is not. Payment systems use idempotency keys to prevent duplicate charges.

## Q66: What is a dead letter queue (DLQ)?
**A:** A dead letter queue is a special queue that receives messages that couldn't be processed after a maximum number of retries. It isolates poison messages (messages that consistently cause failures) so they don't block other messages. Messages in the DLQ can be inspected, debugged, and reprocessed after fixing the underlying issue.

## Q67: What is the bulkhead pattern?
**A:** The bulkhead pattern isolates components of a system into separate pools so that a failure in one doesn't cascade to others. For example, separate thread pools for different downstream services ensure that if one service is slow, it doesn't exhaust the thread pool for other services. Named after the watertight compartments in ship hulls.

## Q68: What is the sidecar pattern?
**A:** The sidecar pattern deploys helper components alongside the main application in a separate process or container. The sidecar handles cross-cutting concerns like logging, monitoring, security (mTLS), and network proxying. This keeps the main application focused on business logic while the sidecar provides infrastructure services. Common in Kubernetes pods with service mesh sidecars.

## Q69: What is a choke point in distributed systems?
**A:** A choke point is a component that handles disproportionate traffic or is a bottleneck for system throughput. Examples include shared databases, single-instance services, or centralized coordinators. Choke points reduce system resilience (single point of failure) and scalability. Identifying and eliminating choke points is critical in distributed system design.

## Q70: What is data partitioning?
**A:** Data partitioning divides a dataset into smaller partitions distributed across multiple nodes. Strategies include: range partitioning (data divided by value ranges), hash partitioning (data distributed by hash function), and list partitioning (data grouped by predefined categories). Partitioning enables horizontal scaling but complicates cross-partition queries.

## Q71: What is a distributed message streaming platform?
**A:** A distributed message streaming platform (like Apache Kafka, Apache Pulsar) provides durable, ordered, and replayable message streams distributed across multiple nodes. Unlike traditional message queues, streams persist messages for configurable retention, support multiple consumers reading independently, and maintain ordering within partitions.

## Q72: What is exactly-once delivery semantics?
**A:** Exactly-once delivery ensures that each message is processed exactly one time — no duplicates, no misses. Achieving this in distributed systems is extremely difficult due to the network unreliability problem. Kafka achieves it through idempotent producers and transactional APIs. Alternatives include at-least-once delivery with idempotent consumers.

## Q73: What is the difference between at-least-once, at-most-once, and exactly-once delivery?
**A:** At-most-once delivers a message zero or one time — simple but may lose messages. At-least-once delivers one or more times — no message loss but may process duplicates (requires idempotent consumers). Exactly-once delivers exactly one time — ideal but complex and expensive to implement, typically approximated through idempotency.

## Q74: What is a distributed lock service?
**A:** A distributed lock service provides mutual exclusion across nodes for coordinating access to shared resources. Apache ZooKeeper and etcd are common implementations. They use consensus protocols (ZAB, Raft) to maintain consistency and provide features like ephemeral nodes, watchers, and sequential ordering for implementing distributed locks.

## Q75: What is Apache ZooKeeper used for?
**A:** ZooKeeper is a centralized coordination service for distributed applications. It provides: distributed configuration management, naming service (registry), distributed synchronization (locks, barriers), group membership tracking, and leader election. It uses a hierarchical data model (znodes) and ensures consistency through the ZAB protocol.

## Q76: What is the CAP theorem in practice — which databases are CP vs AP?
**A:** CP databases include Google Spanner, HBase, MongoDB (in certain configurations), Redis Cluster, and etcd. AP databases include Cassandra, DynamoDB, CouchDB, and Riak. Some databases like Cosmos DB and YugabyteDB offer tunable consistency levels, allowing you to choose CP or AP behavior per operation.

## Q77: What is a microservices anti-pattern?
**A:** Common anti-patterns include: the distributed monolith (microservices that must be deployed together), nanoservices (services too small to be beneficial), shared databases (violating service autonomy), synchronous chains (long chains of synchronous calls creating latency and fragility), and the god service (one service handling too many responsibilities).

## Q78: What is the strangler fig pattern for migration?
**A:** The strangler fig pattern incrementally replaces a monolith with microservices by intercepting requests and routing them to new services or the monolith. Over time, more functionality migrates to new services while the monolith shrinks. This reduces migration risk compared to a big-bang rewrite and allows gradual validation.

## Q79: What is the difference between horizontal and vertical scaling?
**A:** Vertical scaling (scaling up) adds more resources (CPU, RAM) to a single machine — simple but has hardware limits and creates a single point of failure. Horizontal scaling (scaling out) adds more machines — provides near-unlimited scalability and fault tolerance but requires distributed system design. Cloud-native applications typically favor horizontal scaling.

## Q80: What is the fallacies of distributed computing?
**A:** The eight fallacies (by Peter Deutsch) are: the network is reliable, latency is zero, bandwidth is infinite, the network is secure, topology doesn't change, there's one administrator, transport cost is zero, and the network is homogeneous. Understanding these fallacies helps design robust distributed systems that handle real-world network conditions.

## Q81: What is a circuit breaker's three states?
**A:** Closed state: requests flow normally and failures are counted. Open state: when failures exceed a threshold, the circuit opens and requests fail fast without reaching the downstream service. Half-Open state: after a timeout, a limited number of test requests pass through to check if the downstream service has recovered, transitioning back to closed or open.

## Q82: What is service-level agreement (SLA), SLO, and SLI?
**A:** SLI (Service-Level Indicator) is a metric measuring service performance (e.g., request latency, error rate). SLO (Service-Level Objective) is the target value for an SLI (e.g., 99.9% availability). SLA (Service-Level Agreement) is the contractual commitment with consequences for missing SLOs. SLIs feed SLOs; SLOs define SLAs.

## Q83: What is the difference between latency and throughput?
**A:** Latency is the time for a single operation to complete (e.g., 50ms per request). Throughput is the number of operations per unit time (e.g., 10,000 requests/second). High throughput doesn't guarantee low latency. Optimizing for one may affect the other. Distributed systems must balance both based on application requirements.

## Q84: What is a failure domain?
**A:** A failure domain is the scope of impact when a component fails. Small failure domains limit blast radius — a single server failure shouldn't take down an entire availability zone. Designing with separate failure domains (zones, regions, racks) ensures that failures are isolated. Good architecture means any single failure impacts a minimal portion of the system.

## Q85: What is chaos engineering?
**A:** Chaos engineering is the practice of deliberately injecting failures into a system to test its resilience. By simulating network partitions, server crashes, and latency spikes in production or staging, teams discover weaknesses before they cause real outages. Netflix's Chaos Monkey pioneered this approach. Tools include Chaos Monkey, Litmus, and Gremlin.

## Q86: What is a distributed cache and what are consistency challenges?
**A:** A distributed cache replicates or partitions data across multiple nodes for fast reads. Consistency challenges include: keeping cached data in sync with the database, handling cache misses during node failures, ensuring cache invalidation propagates to all nodes, and managing split-brain scenarios where partitioned cache nodes diverge.

## Q87: What is a read-through vs. cache-aside pattern?
**A:** In read-through caching, the cache is responsible for loading data from the database on a miss — the application only interacts with the cache. In cache-aside (lazy loading), the application checks the cache, and if it's a miss, loads from the database and populates the cache. Cache-aside gives the application more control over caching logic.

## Q88: What is a service catalog in microservices?
**A:** A service catalog is a centralized registry that stores metadata about all microservices — their endpoints, owners, documentation, dependencies, and health status. It enables service discovery, provides a single source of truth for available services, and supports governance. Examples include Backstage, Consul, and custom solutions.

## Q89: What is the API-first design approach?
**A:** API-first design defines the API contract (OpenAPI/Swagger) before implementation. Teams can work in parallel — backend implements the API, frontend consumes it, and tests validate it. This approach improves collaboration, enables contract testing, and ensures API consistency. It naturally supports microservices development.

## Q90: What is a distributed system's failure mode?
**A:** A failure mode describes how a system fails under specific conditions. Examples: fail-stop (node crashes and stops responding), Byzantine (node behaves arbitrarily or maliciously), performance degradation (slow responses), and silent failures (corrupted data without error). Understanding failure modes helps design appropriate recovery mechanisms.

## Q91: What is graceful degradation?
**A:** Graceful degradation is the ability of a system to continue functioning at a reduced level when components fail. Instead of complete failure, non-critical features are disabled while core functionality remains. For example, a recommendation service might return cached results instead of real-time calculations during high load.

## Q92: What is the backpressure pattern?
**A:** Backpressure is a feedback mechanism where a downstream component signals to upstream components to slow down when it's overwhelmed. It prevents queue buildup, memory exhaustion, and cascading failures. Examples include TCP flow control, reactive streams (Reactor, RxJava), and Kafka consumer rate limiting.

## Q93: What is data locality and why does it matter?
**A:** Data locality means processing data where it's stored to minimize network transfer. In distributed systems, moving computation to data is more efficient than moving data to computation. Hadoop's MapReduce, for example, schedules tasks on nodes where the required data resides. Data locality reduces latency and network bandwidth usage.

## Q94: What is a distributed system's partial failure?
**A:** Partial failure occurs when some components of a system fail while others continue operating correctly. This is distinct from total failure and is harder to detect and handle. For example, one node in a cluster may crash while others are healthy, or network partition may isolate a subset of nodes. Partial failures are the defining challenge of distributed computing.

## Q95: What is the Two Generals' problem?
**A:** The Two Generals' Problem is a thought experiment demonstrating that reliable communication over an unreliable channel is impossible. Two armies must agree on a time to attack, but every message acknowledgment can be lost. This fundamental impossibility explains why distributed systems can never guarantee both consistency and availability during network partitions.

## Q96: What is vector clocks?
**A:** Vector clocks are a mechanism for tracking causal ordering of events in a distributed system. Each node maintains a vector of counters (one per node) that increments with each event. By comparing vector clocks, you can determine if events are causally related (happened-before), concurrent (no causal relationship), or identical.

## Q97: What is the gossip protocol?
**A:** The gossip protocol is a communication protocol where nodes periodically exchange state information with randomly selected peers. Information spreads exponentially through the network like gossip. It's used for membership management, failure detection, and data dissemination in distributed systems (e.g., Cassandra, Consul). It's scalable and fault-tolerant but eventually consistent.

## Q98: What is the difference between synchronous and asynchronous replication?
**A:** Synchronous replication writes data to all replicas before confirming success — provides strong consistency but higher latency and reduced availability. Asynchronous replication writes to the primary and replicates to secondaries after confirmation — lower latency and higher availability but risk of data loss on primary failure. Most systems use a hybrid approach.

## Q99: What is a distributed system's network partition?
**A:** A network partition occurs when a network failure divides nodes into two or more groups that cannot communicate with each other. Each group can still operate independently, potentially making conflicting decisions. The CAP theorem dictates that during a partition, the system must choose between consistency (reject conflicting operations) or availability (serve potentially inconsistent data).

## Q100: What are the best practices for designing distributed systems?
**A:** Best practices include: designing for failure (assume components will fail), embracing eventual consistency where appropriate, using circuit breakers and retries with backoff, implementing comprehensive monitoring and tracing, using idempotent operations, partitioning data for scalability, maintaining loose coupling between services, automating deployment and recovery, and testing resilience with chaos engineering.
