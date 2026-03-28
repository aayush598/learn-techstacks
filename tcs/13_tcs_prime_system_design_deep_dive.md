# TCS Prime System Design & Scalability Interview Questions

TCS Prime interviews heavily test your ability to design robust, enterprise-grade systems. Since you know Next.js, FastAPI, Docker, and PostgreSQL, these questions focus on scaling those exact technologies.

## Core System Design Principles
1. **Q:** Monolith vs Microservices? **A:** A monolith binds all logic into a single codebase and deployment. Microservices break the application into small, independent services communicating via APIs (FastAPI). Microservices allow independent scaling and deployment but add complexity.
2. **Q:** What is Horizontal Scaling vs Vertical Scaling? **A:** Vertical scaling (Scale up) means adding more CPU/RAM to an existing server. Horizontal scaling (Scale out) means adding more servers to a cluster to distribute the load.
3. **Q:** What is a Load Balancer? **A:** A device/software (like Nginx, AWS ALB) that distributes incoming network traffic across multiple backend servers to prevent any single server from becoming a bottleneck.
4. **Q:** Explain CAP Theorem. **A:** In a distributed data store, you can only guarantee two of three: Consistency (every read gets the most recent write), Availability (every request receives a response), and Partition tolerance (system continues despite network failures).
5. **Q:** What is an API Gateway? **A:** A server that acts as an API front-end, receiving API requests, enforcing throttling and security policies, passing requests to the back-end service, and then passing the response back to the requester.
6. **Q:** How do you handle Rate Limiting? **A:** Using middleware to track the number of requests per user IP over a time window (e.g., using Redis) and returning an HTTP 429 Too Many Requests error if the limit is exceeded.

## Message Queues & Event-Driven Architecture
7. **Q:** Why use a Message Queue (e.g., RabbitMQ, Kafka) in your FastAPI AI pipeline? **A:** LLM interactions take seconds. Synchronous requests will block FastAPI workers and timeout. A queue decouples the request: FastAPI accepts the request, puts it in the queue, returns a 202 Accepted, and asynchronous workers process the heavy LLM tasks.
8. **Q:** RabbitMQ vs Kafka? **A:** RabbitMQ is a traditional message broker focusing on routing messages and deleting them once consumed. Kafka is a distributed event streaming platform functioning like an append-only log, optimized for massive data throughput and replayability.
9. **Q:** What is a Dead Letter Queue (DLQ)? **A:** A queue where messages are sent if they cannot be routed to their correct destination or if consumer processing repeatedly fails.

## Caching and Performance Optimization
10. **Q:** What is Redis? **A:** An open-source, in-memory data structure store used as a database, cache, and message broker. Because it lives in RAM, reads/writes are lightning fast (sub-millisecond).
11. **Q:** Caching Strategies? **A:** 
    - *Cache-aside:* App checks cache; if miss, fetches from DB, then writes to cache.
    - *Write-through:* App writes to cache, which synchronously writes to DB.
    - *Write-behind:* App writes to cache; cache asynchronously writes to DB.
12. **Q:** How do you handle Cache Invalidation? **A:** Setting an absolute TTL (Time To Live), or actively evicting cache keys upon database updates via application logic.
13. **Q:** CDN vs Cache? **A:** A CDN (Content Delivery Network like Cloudflare/Vercel) caches static assets (Next.js HTML, CSS, JS, Images) globally on edge servers to reduce latency for users. Standard cache (Redis) stores dynamic DB query results.

## Databases & Sharding
14. **Q:** What is Database Replication? **A:** Copying data from a Master database to one or more Read-Replica databases to improve read speeds and provide failover redundancy.
15. **Q:** What is Database Sharding? **A:** Dividing a large database table into smaller chunks (shards) spread across multiple database servers based on a shard key (e.g., user_id) to distribute read/write load.
16. **Q:** Explain the N+1 Query Problem from ORMs. **A:** An ORM executing 1 query to fetch a list of entities, and then N additional queries to fetch related entities in a loop, severely bottlenecking the DB. Fixed using `JOINs` or eager loading.

## Docker & Orchestration
17. **Q:** What is Kubernetes (K8s)? **A:** An open-source container orchestration system for automating software deployment, scaling, and management. It groups Docker containers into logical units (Pods).
18. **Q:** How does Auto-Scaling work? **A:** Services like AWS Auto Scaling or K8s HPA monitor metrics (like CPU > 70% or Queue length > 100), automatically spinning up new Docker instances to handle surges, and tearing them down when traffic lowers.
19. **Q:** What is Blue-Green Deployment? **A:** Running two identical production environments (Blue and Green). Traffic goes to Blue. A new version is deployed to Green. Once tested, the router switches traffic from Blue to Green, ensuring zero downtime.
