# Microservices Architecture - 200+ Interview Q&A

### Q1: Monolith vs Microservices?
**Answer:** Monolith: single deployable unit, simpler to start, easier debugging, shared code. Microservices: independent deployable services, each owns its data, independent scaling, polyglot tech stacks. Start with monolith, split when needed.

### Q2: How do microservices communicate?
**Answer:** Synchronous: REST, gRPC (HTTP/2, protobuf, streaming). Asynchronous: message queues (Kafka, RabbitMQ, SQS, Redis Streams). Prefer async for decoupling. gRPC for high-performance internal communication.

### Q3: Service discovery patterns?
**Answer:** Client-side: services register with registry (Consul, etcd, Eureka), client queries and load balances. Server-side: load balancer (AWS ALB, Nginx) routes to service. Kubernetes uses DNS + kube-proxy.

### Q4: What is the API Gateway pattern?
**Answer:** Single entry point for all clients. Routes requests to appropriate services. Handles auth, rate limiting, logging, request transformation, aggregation. Examples: Kong, AWS API Gateway, Nginx, Traefik.

### Q5: Database per service pattern?
**Answer:** Each service owns its database. No direct access to other services' databases. Communication only via APIs. Prevents tight coupling. Challenge: maintaining consistency across services.

### Q6: Distributed transactions (Saga pattern)?
**Answer:** Choreography: services publish events, others listen and act. Orchestration: central coordinator tells services what to do. Each step publishes compensating action on failure. Example: order → payment → inventory.

### Q7: Circuit breaker pattern?
**Answer:** Prevent cascading failures. States: Closed (normal), Open (failing, reject immediately), Half-Open (test if recovered). Libraries: Hystrix (Java), resilience4j. Implement with counters in Redis.

### Q8: Event sourcing + CQRS?
**Answer:** Event sourcing: store state changes as events, current state = fold events. CQRS: separate read/write models. Often used together. Benefits: audit trail, temporal queries, complex reads simplified.

### Q9: Docker Compose vs Kubernetes?
**Answer:** Docker Compose: single machine, development/test. Kubernetes: multi-machine, production, auto-scaling, self-healing, service discovery, rolling updates. K8s complex but powerful.

### Q10: Observability in microservices?
**Answer:** Three pillars: Logging (structured, centralized - ELK/Loki), Metrics (Prometheus, Grafana), Tracing (distributed tracing - Jaeger, Zipkin, OpenTelemetry). Correlation IDs across services for request tracing.
