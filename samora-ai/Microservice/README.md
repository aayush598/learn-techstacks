# Microservice Interview Questions and Answers

## Q1: What are microservices?
**A:** Microservices is an architectural style that structures an application as a collection of small, autonomous, loosely coupled services. Each service is responsible for a specific business capability, can be developed, deployed, and scaled independently, and communicates with other services through well-defined APIs (typically HTTP/REST, gRPC, or messaging queues).

## Q2: How do microservices differ from monolithic architecture?
**A:** In a monolithic architecture, all components are interconnected and run as a single process, making scaling, deployment, and maintenance difficult. Microservices break the application into independent services, each with its own database, lifecycle, and technology stack, enabling independent scaling, faster deployments, and better fault isolation.

## Q3: What are the key characteristics of microservices?
**A:** Key characteristics include: 1) Single responsibility (each service focuses on one business capability). 2) Loose coupling (services communicate via APIs). 3) Independent deployability. 4) Polyglot persistence (each service can use its own database technology). 5) Polyglot programming (different languages/frameworks per service). 6) Decentralized governance. 7) Fault tolerance and resilience. 8) Automated CI/CD.

## Q4: What are the advantages of microservices?
**A:** Advantages include: 1) Independent scaling of services. 2) Faster development and deployment cycles. 3) Technology diversity (choose best tool for each service). 4) Better fault isolation (one failure doesn't bring down the whole system). 5) Easier onboarding for new developers. 6) Improved maintainability. 7) Better alignment with business boundaries.

## Q5: What are the challenges of microservices?
**A:** Challenges include: 1) Increased complexity (distributed systems are harder to debug). 2) Network latency and communication overhead. 3) Data consistency across services. 4) Distributed tracing and monitoring. 5) Service discovery and orchestration. 6) Testing (integration testing becomes complex). 7) Configuration management. 8) Deployment coordination. 9) Organizational alignment (Conway's Law).

## Q6: What is service discovery in microservices?
**A:** Service discovery is the process of automatically detecting the network locations of service instances. Two main patterns: Client-side discovery (client queries a service registry to find available instances) and Server-side discovery (a load balancer/router queries the registry). Tools include Eureka, Consul, ZooKeeper, and Kubernetes DNS.

## Q7: What is the difference between service discovery and API Gateway?
**A:** Service discovery handles locating service instances by address/port for internal communication. An API Gateway is a single entry point for external clients that handles routing, authentication, rate limiting, and request transformation. API Gateways often use service discovery internally to route requests.

## Q8: What is an API Gateway and what are its benefits?
**A:** An API Gateway is a server that acts as the single entry point for all client requests in a microservices architecture. Benefits include: request routing, authentication and authorization, rate limiting, caching, request/response transformation, API versioning, circuit breaking, load balancing, and centralized logging/monitoring.

## Q9: How do microservices communicate with each other?
**A:** Two main patterns: 1) Synchronous communication using HTTP/REST or gRPC where the caller waits for a response. 2) Asynchronous communication using message brokers (Kafka, RabbitMQ, SQS) where services communicate through events or messages. The choice depends on consistency, latency, and coupling requirements.

## Q10: What is the difference between orchestration and choreography in microservices?
**A:** Orchestration uses a central coordinator (orchestrator) that controls the workflow and tells services what to do (e.g., Saga orchestrator). Choreography has no central coordinator; each service decides when and how to react to events, with services communicating through event channels. Choreography is more decentralized but harder to track.

## Q11: What is the Saga pattern?
**A:** The Saga pattern manages distributed transactions across multiple microservices by breaking the transaction into a series of local transactions, each with a compensating action for rollback. Two implementations: Choreography-based Saga (services listen for events and execute/compensate) and Orchestration-based Saga (a coordinator tells services what to do).

## Q12: What is eventual consistency in microservices?
**A:** Eventual consistency is a consistency model where updates to a distributed system propagate to all nodes eventually (not immediately). In microservices, it means that after an update, different services may see slightly different data for a short time, but will eventually become consistent. It enables higher availability and performance than strong consistency.

## Q13: What is the Circuit Breaker pattern?
**A:** The Circuit Breaker pattern prevents a failure in one service from cascading to other services. It wraps remote calls and monitors for failures. Three states: Closed (normal operation), Open (failures threshold exceeded, requests fail immediately), and Half-Open (testing if the service has recovered). Implementations include Hystrix, Resilience4j, and Istio.

## Q14: What is the Bulkhead pattern?
**A:** The Bulkhead pattern isolates resources within a system to prevent failure in one component from cascading to others. Like ship compartments, each service or thread pool is isolated so that if one fails, others remain unaffected. Implemented through separate thread pools, connection pools, or even separate hardware/containers.

## Q15: What is the Strangler Fig pattern?
**A:** The Strangler Fig pattern is a strategy for incrementally migrating a monolithic application to microservices. You gradually replace pieces of the monolith with new microservices, routing traffic to the new services while the monolith handles the rest. Eventually, the entire monolith is "strangled" and can be decommissioned.

## Q16: What is CQRS (Command Query Responsibility Segregation)?
**A:** CQRS separates read and write operations into different models. Commands handle writes (mutations) and Queries handle reads. This allows optimizing each side independently (e.g., using different databases or schemas). Often combined with Event Sourcing. CQRS is useful when read and write workloads are significantly different.

## Q17: What is Event Sourcing?
**A:** Event Sourcing stores the state of an entity as a sequence of state-changing events. Instead of storing the current state, you store every change event, and the current state is derived by replaying events. Benefits include complete audit trail, temporal queries, and the ability to reconstruct past states.

## Q18: What is the difference between Event Sourcing and CQRS?
**A:** Event Sourcing is a persistence pattern that stores events rather than state. CQRS is a pattern that separates read and write responsibilities. They are often used together but are independent: Event Sourcing provides the event store that CQRS commands write to and queries read from.

## Q19: What is a Sidecar pattern?
**A:** The Sidecar pattern deploys helper components (sidecar containers) alongside the main application container. The sidecar provides supporting features like logging, monitoring, configuration, service discovery, or proxy functionality without modifying the main application code. Commonly used in service mesh implementations (Envoy, Istio).

## Q20: What is the Ambassador pattern?
**A:** The Ambassador pattern creates helper services that handle network communication on behalf of the main service. An ambassador container runs as a proxy, managing connections, retries, circuit breaking, authentication, and routing. It is similar to the Sidecar pattern but specifically focuses on network communication.

## Q21: What is a service mesh?
**A:** A service mesh is a dedicated infrastructure layer for handling service-to-service communication, security, and observability in microservices. It typically uses sidecar proxies (e.g., Envoy) to intercept all network traffic, providing features like mutual TLS, traffic routing, circuit breaking, metrics collection, and distributed tracing.

## Q22: Compare Istio, Linkerd, and Consul for service mesh.
**A:** Istio is feature-rich with mTLS, traffic management, observability, and policy enforcement but has higher complexity and resource usage. Linkerd is lighter, simpler, and faster with a focus on performance and ease of use. Consul provides service mesh with integrated service discovery and multi-cloud support.

## Q23: How do you handle distributed transactions in microservices?
**A:** Traditional ACID transactions are difficult across services. Approaches include: 1) Saga pattern (compensating transactions). 2) Eventual consistency with event-driven design. 3) Two-phase commit (not recommended for microservices). 4) Outbox pattern (write to local DB and publish events atomically). 5) Try-Confirm/Cancel (TCC) pattern.

## Q24: What is the Outbox pattern?
**A:** The Outbox pattern ensures reliable message delivery in microservices. Service writes the event to an "outbox" table in its own database as part of the local transaction. A separate process (poller or CDC) reads the outbox and publishes events to the message broker, ensuring atomicity between DB changes and message publishing.

## Q25: What is Database per Service pattern?
**A:** Each microservice has its own private database, ensuring loose coupling and independent data management. Benefits include schema encapsulation, polyglot persistence (using different database types), and independent scaling. Challenges include maintaining data consistency across services and handling joins across service boundaries.

## Q26: How do you handle data consistency across microservices without distributed transactions?
**A:** Techniques include: 1) Eventual consistency with event-driven architecture. 2) Saga pattern with compensating transactions. 3) Idempotency (design operations to be safely retried). 4) Version vectors and conflict resolution. 5) Read-your-writes consistency guarantees. 6) Distributed sagas with monitoring and recovery.

## Q27: What is the difference between shared database and database per service?
**A:** Shared database means multiple services access the same database, creating tight coupling and making schema changes difficult. Database per service means each service owns its data exclusively, enabling independent schema evolution, technology choice, and scaling, but requiring data synchronization across service boundaries.

## Q28: How do you handle API versioning in microservices?
**A:** Common strategies: 1) URI versioning (/v1/users, /v2/users). 2) Header versioning (Accept: application/vnd.api+json;version=1). 3) Query parameter versioning (?version=1). 4) Content negotiation. URI versioning is the simplest. Header versioning keeps URIs clean. Consider backward compatibility and deprecation policies.

## Q29: What is contract testing in microservices?
**A:** Contract testing verifies that two services (consumer and provider) meet the agreed-upon communication contract. Unlike integration testing, it tests each side independently using stubs. Tools like Pact allow consumers to define expectations (contracts) and providers to verify they satisfy those contracts.

## Q30: What is the difference between integration testing and contract testing?
**A:** Integration testing runs actual services together to verify they work correctly, which is complex, slow, and fragile in microservices. Contract testing verifies service interfaces independently using stubs, ensuring that both sides adhere to the contract without needing full deployment, making tests faster and more reliable.

## Q31: What is distributed tracing?
**A:** Distributed tracing tracks requests as they flow through multiple microservices, providing end-to-end visibility. Each request gets a unique trace ID, and spans represent individual operations within services. Tools like Jaeger, Zipkin, and AWS X-Ray help visualize and debug distributed request flows.

## Q32: How do you implement distributed tracing?
**A:** Implementation involves: 1) Propagating a unique trace context (trace ID, span ID) across service boundaries via HTTP headers or message metadata. 2) Instrumenting service code to create spans for operations. 3) Exporting span data to a centralized backend. 4) Using tools like Jaeger, Zipkin, or OpenTelemetry for visualization.

## Q33: What is OpenTelemetry?
**A:** OpenTelemetry is an open-source observability framework for generating, collecting, and exporting telemetry data (traces, metrics, logs) from applications. It provides a unified standard with vendor-neutral APIs, SDKs, and instrumentation libraries, and supports exporting to multiple backends.

## Q34: What are health checks in microservices?
**A:** Health checks are endpoints that report a service's operational status. Two types: 1) Liveness check - tells the orchestrator if the service is alive (restart if dead). 2) Readiness check - tells the load balancer if the service is ready to receive traffic (remove if not ready). Implemented as /health or /ready endpoints.

## Q35: What is graceful shutdown in microservices?
**A:** Graceful shutdown is the process of stopping a service without dropping active requests. The service stops accepting new requests, completes in-flight requests, releases resources, and then exits. Kubernetes supports this with SIGTERM signals and a terminationGracePeriodSeconds setting.

## Q36: How do you handle configuration management in microservices?
**A:** Approaches include: 1) External configuration service (Spring Cloud Config, Consul KV, etcd). 2) Environment variables (12-factor app). 3) ConfigMaps and Secrets in Kubernetes. 4) Distributed configuration storage (AWS Parameter Store, HashiCorp Vault). Best practice: externalize all configuration from code, enable dynamic updates without restart.

## Q37: What is the 12-Factor App methodology?
**A:** The 12-Factor App is a methodology for building SaaS applications, especially relevant to microservices. The 12 factors: 1) Codebase (one codebase tracked in revision control). 2) Dependencies (explicitly declare and isolate). 3) Config (store config in environment). 4) Backing services (treat as attached resources). 5) Build, release, run. 6) Processes (stateless). 7) Port binding. 8) Concurrency (scale out via processes). 9) Disposability (fast startup/shutdown). 10) Dev/prod parity. 11) Logs (treat as event streams). 12) Admin processes (run as one-off processes).

## Q38: What is the difference between blue-green deployment and canary deployment?
**A:** Blue-green deployment runs two identical environments (blue and green). Traffic is switched from blue to green instantly. Rollback is immediate by switching back. Canary deployment incrementally routes a small percentage of traffic to the new version, gradually increasing if no issues, reducing risk and enabling real-world validation.

## Q39: How do you handle rolling back a microservice deployment?
**A:** Strategies include: 1) Revert the deployment to the previous version (Kubernetes rollout undo). 2) Blue-green switch back. 3) Canary rollback by reducing traffic to zero. 4) Database schema versioning with backward-compatible migrations. 5) Feature flags to disable new functionality without redeploying.

## Q40: What is CI/CD in the context of microservices?
**A:** CI/CD (Continuous Integration/Continuous Deployment) in microservices means each service has its own CI/CD pipeline. Continuous Integration involves automatically building and testing each service on every commit. Continuous Deployment automatically deploys tested changes to production. Pipeline stages typically include lint, test, build, security scan, deploy, and smoke test.

## Q41: What is Docker and why is it important for microservices?
**A:** Docker is a containerization platform that packages applications with their dependencies into isolated containers. It's important for microservices because containers provide: 1) Consistent runtime environments across development, testing, and production. 2) Isolation between services. 3) Lightweight resource usage. 4) Fast startup times. 5) Versioning and reproducibility.

## Q42: What is Kubernetes and why use it for microservices?
**A:** Kubernetes is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. For microservices, Kubernetes provides: service discovery and load balancing, automated rollouts/rollbacks, self-healing, secret/configuration management, horizontal scaling, and resource management.

## Q43: Compare Kubernetes vs. Docker Swarm for microservices.
**A:** Kubernetes is the industry standard with a rich ecosystem, advanced features (service mesh, CRDs, operators), and broad cloud support, but has higher complexity. Docker Swarm is simpler to set up and integrates natively with Docker CLI, but lacks advanced features and has a smaller ecosystem.

## Q44: What is a Pod in Kubernetes?
**A:** A Pod is the smallest deployable unit in Kubernetes, representing one or more containers that share storage, network, and specification for how to run. Containers within a Pod share the same IP address, port space, and storage volumes. In microservices, typically one container per Pod (one service per Pod).

## Q45: What is a Kubernetes Deployment?
**A:** A Deployment provides declarative updates for Pods and ReplicaSets. It manages the desired state (number of replicas, container image version) and handles rolling updates, rollbacks, scaling, and self-healing. Deployments are the primary mechanism for running stateless microservices in Kubernetes.

## Q46: What is a Kubernetes Service?
**A:** A Kubernetes Service is an abstraction that defines a logical set of Pods and a policy for accessing them. It provides stable networking (IP/DNS) regardless of Pod IP changes and load balancing across Pod replicas. Types include ClusterIP (internal only), NodePort (external via node port), LoadBalancer (cloud LB), and ExternalName.

## Q47: What is an Ingress in Kubernetes?
**A:** Ingress manages external access to services within a Kubernetes cluster, typically HTTP/HTTPS routing. It provides host-based and path-based routing, SSL/TLS termination, and load balancing. An Ingress Controller (e.g., NGINX, Traefik, HAProxy) implements the Ingress rules.

## Q48: What is a ConfigMap and Secret in Kubernetes?
**A:** ConfigMap stores non-sensitive configuration data (key-value pairs or files) that can be consumed by Pods as environment variables, command-line arguments, or volumes. Secret stores sensitive data (passwords, API keys, certificates) in base64-encoded format, with encryption at rest and RBAC access control.

## Q49: What is Kubernetes HorizontalPodAutoscaler (HPA)?
**A:** HPA automatically scales the number of Pods in a Deployment based on observed metrics like CPU utilization, memory usage, or custom metrics. It adjusts the replica count to meet demand, ensuring resources are efficiently used. HPA is a key mechanism for achieving elasticity in microservices.

## Q50: What is the difference between readiness, liveness, and startup probes?
**A:** Liveness probe checks if the container is alive (restarts if fails). Readiness probe checks if the container is ready to serve traffic (removes from Service if fails). Startup probe checks if the application has started (delays liveness/readiness checks until success). Startup probe is useful for slow-starting applications.

## Q51: How do you handle secrets management in microservices?
**A:** Options include: 1) Kubernetes Secrets with encryption at rest. 2) HashiCorp Vault for dynamic secrets and rotation. 3) AWS Secrets Manager / Azure Key Vault / GCP Secret Manager. 4) Sealed Secrets (encrypt secrets in Git). 5) External secrets operator (sync secrets from external stores to K8s). 6) Service mesh mTLS for identity.

## Q52: What is the Ambassador API Gateway pattern?
**A:** The Ambassador pattern places an API Gateway at the edge of the system (entry point for external traffic). It handles cross-cutting concerns like authentication, rate limiting, TLS termination, routing, caching, and monitoring. Tools include Kong, Ambassador (Envoy-based), Apigee, AWS API Gateway, and NGINX.

## Q53: What is rate limiting in microservices and how do you implement it?
**A:** Rate limiting controls the number of requests a client can make within a time window, preventing abuse and ensuring fair resource usage. Implementation patterns: 1) Token bucket algorithm. 2) Leaky bucket algorithm. 3) Fixed/sliding window counters. Can be implemented at API Gateway, application code, or using Redis-based distributed rate limiting.

## Q54: What is the difference between authentication and authorization in microservices?
**A:** Authentication (AuthN) verifies who the user is (identity). Authorization (AuthZ) determines what they can do (permissions). In microservices, authentication is typically handled at the API Gateway (JWT validation) and authorization is often delegated to individual services or a centralized policy engine (OPA, Casbin).

## Q55: What is JWT and how is it used in microservices?
**A:** JSON Web Token (JWT) is a compact, URL-safe token format for representing claims between parties. In microservices, JWT is used for stateless authentication: the API Gateway validates credentials and issues a signed JWT containing user identity and claims. Services verify the JWT signature without needing a session store.

## Q56: What is OAuth 2.0 and how does it relate to microservices?
**A:** OAuth 2.0 is an authorization framework that enables third-party applications to obtain limited access to resources. In microservices, OAuth 2.0 is commonly used with JWT for securing APIs. The API Gateway acts as the resource server, validating access tokens issued by an authorization server.

## Q57: What is OpenID Connect (OIDC)?
**A:** OpenID Connect is an identity layer built on top of OAuth 2.0 that provides authentication. It adds an ID token (JWT) containing user identity information. In microservices, OIDC is used with API Gateways to authenticate users and propagate identity to downstream services.

## Q58: How do you secure inter-service communication?
**A:** Approaches include: 1) Mutual TLS (mTLS) for authenticated encrypted communication. 2) Service mesh (Istio, Linkerd) for automatic mTLS. 3) JWT-based service-to-service tokens. 4) API keys for service authentication. 5) Network policies (Kubernetes NetworkPolicies) to restrict traffic. 6) VPN or private networks.

## Q59: What is Zero Trust Security in microservices?
**A:** Zero Trust is a security model that assumes no implicit trust, even within the network perimeter. Every request must be authenticated, authorized, and encrypted. In microservices, this means: mTLS between all services, continuous identity verification, least-privilege access, micro-segmentation, and comprehensive audit logging.

## Q60: What is the principle of least privilege in microservices?
**A:** The principle of least privilege means each service should only have the minimum permissions necessary to perform its function. Applied to: 1) IAM roles (EC2 to access only needed S3 buckets). 2) Kubernetes RBAC (service accounts with limited permissions). 3) Database access (read-only vs read-write). 4) Network access (only required ports/protocols).

## Q61: How do you handle monitoring and logging in microservices?
**A:** Implement centralized logging (ELK stack, Loki, CloudWatch), metrics collection (Prometheus, Datadog), and distributed tracing (Jaeger, Zipkin). Use structured logging with request IDs. Aggregated dashboards (Grafana) provide visibility. Alerting based on SLOs/SLIs. Each service should expose health and metrics endpoints.

## Q62: What are the three pillars of observability?
**A:** 1) Logs: structured, timestamped records of discrete events. 2) Metrics: numeric measurements over time (latency, error rate, request count). 3) Traces: end-to-end tracking of requests across distributed services. Together they provide comprehensive insight into system behavior.

## Q63: What is the ELK Stack (Elasticsearch, Logstash, Kibana)?
**A:** ELK is a popular logging solution. Elasticsearch stores and indexes logs. Logstash ingests, transforms, and ships logs. Kibana provides visualization and dashboards. Filebeat (or Fluentd) often replaces Logstash for lightweight log shipping. The modern variant is Elastic Stack.

## Q64: What is the EFK Stack (Elasticsearch, Fluentd, Kibana)?
**A:** EFK replaces Logstash with Fluentd, a CNCF-graduated data collector. Fluentd provides unified logging with a pluggable architecture, handling data collection, transformation, and forwarding. Both ELK and EFK serve the same purpose; the choice depends on ecosystem preferences.

## Q65: What is Prometheus and Grafana?
**A:** Prometheus is a time-series database and monitoring system that collects metrics from services via pull model (HTTP scraping). Grafana is a visualization and dashboard tool that queries Prometheus (and other data sources). Together they form a standard monitoring stack for microservices.

## Q66: What is the difference between black-box and white-box monitoring?
**A:** Black-box monitoring observes the system from the outside (e.g., external uptime checks, synthetic transactions) without knowing internal details. White-box monitoring examines internal metrics (CPU, memory, request latency, error rates) exposed by the application. Both approaches complement each other in microservices monitoring.

## Q67: What are SLOs, SLIs, and SLAs?
**A:** SLI (Service Level Indicator) is a measured metric (e.g., 99.9% of requests complete in under 200ms). SLO (Service Level Objective) is the target value for the SLI (e.g., 99.9% of requests under 200ms over 30 days). SLA (Service Level Agreement) is the contractual commitment to the SLO, with consequences for violation.

## Q68: How do you ensure high availability in microservices?
**A:** Strategies include: 1) Run multiple instances across availability zones. 2) Use load balancers for traffic distribution. 3) Implement circuit breakers and retries with exponential backoff. 4) Stateless services for easy scaling. 5) Database replication and failover. 6) Health checks and auto-recovery. 7) Graceful degradation and fallbacks.

## Q69: What is the difference between fault tolerance and resilience?
**A:** Fault tolerance means a system can continue operating correctly in the presence of failures (no downtime). Resilience means a system can recover quickly from failures and continue operating, possibly with reduced functionality. In microservices, fault tolerance prevents cascading failures, while resilience ensures fast recovery.

## Q70: How do you test microservices?
**A:** The test pyramid: 1) Unit tests (test individual functions). 2) Integration tests (test service interactions with databases, message queues). 3) Contract tests (verify service API contracts). 4) Component tests (test service in isolation). 5) End-to-end tests (test full system). Use consumer-driven contract tests (Pact) and test containers.

## Q71: What is the difference between unit, integration, and end-to-end testing in microservices?
**A:** Unit tests test individual functions in isolation (mocked dependencies). Integration tests test a service's interaction with real dependencies (DB, message queue). End-to-end tests test complete business flows across multiple services in a production-like environment. Microservices require more integration and contract tests.

## Q72: What is Testcontainers?
**A:** Testcontainers is a Java library (also .NET, Go, Node) that provides lightweight, throwaway instances of databases, message brokers, and other services for integration testing. It uses Docker containers to spin up dependencies during tests, ensuring consistent test environments.

## Q73: How do you handle database migrations in microservices?
**A:** Each service manages its own database schema independently. Tools like Flyway or Liquibase version database migrations. Migrations should be backward-compatible (additive changes first, then remove old columns after deployment). Never break existing queries. Use expand-migrate-contract pattern (add, migrate, remove).

## Q74: What is the expand-migrate-contract pattern for database changes?
**A:** Also called parallel change or phased migration. Phase 1 (Expand): Add new schema elements (columns, tables) without removing old ones. Phase 2 (Migrate): Deploy updated code that uses both old and new. Phase 3 (Contract): Remove old schema elements after all code is updated. Ensures zero-downtime database changes.

## Q75: How do you handle polyglot persistence in microservices?
**A:** Each service chooses the best database technology for its needs. For example: User service uses PostgreSQL (relational), Product catalog uses MongoDB (document), Analytics uses Cassandra (wide-column), Search uses Elasticsearch. This provides optimization but adds complexity in data synchronization and operations.

## Q76: What is the difference between a repository and a service in DDD?
**A:** In Domain-Driven Design, a Repository provides an abstraction for persisting and retrieving domain objects (aggregates). A Service (domain service) encapsulates business logic that doesn't naturally fit within an entity or value object. Application services orchestrate use cases, domain services implement domain logic.

## Q77: What is Bounded Context in DDD?
**A:** A Bounded Context is a logical boundary within which a particular domain model applies. Each microservice should align with one bounded context. Within a context, terms have specific meanings. Different contexts can use the same term differently. Bounded contexts communicate through integration events or APIs.

## Q78: What is an Aggregate in DDD?
**A:** An Aggregate is a cluster of domain objects treated as a single unit for data changes. Each aggregate has a root entity (Aggregate Root) that enforces invariants. External references only go to the aggregate root, not internal entities. Aggregates are a natural unit for consistency boundaries and repositories.

## Q79: What is Domain Events in DDD?
**A:** Domain Events are records of something significant that happened in the domain. In microservices, domain events are published to notify other services of state changes. They enable eventual consistency and choreography-based sagas. Examples: OrderPlaced, PaymentCompleted, InventoryReserved.

## Q80: How do you split a monolith into microservices?
**A:** Steps: 1) Identify bounded contexts and business capabilities. 2) Extract one service at a time using Strangler Fig pattern. 3) Create well-defined APIs for the new service. 4) Move data ownership to the new service's database. 5) Implement communication between monolith and new service. 6) Gradually migrate functionality.

## Q81: What are the common migration strategies from monolith to microservices?
**A:** 1) Strangler Fig (incremental replacement). 2) Extract services by business capability. 3) Split by domain (bounded contexts). 4) Split by traffic patterns (high-traffic modules first). 5) Split by change frequency (volatile modules first). 6) Event-driven decomposition (extract event producers/consumers).

## Q82: What is Conway's Law and how does it affect microservices?
**A:** Conway's Law states: "Organizations design systems that mirror their communication structure." For microservices, this means service boundaries should align with team boundaries. Autonomous teams own end-to-end services. Poor alignment leads to tightly coupled services and integration issues.

## Q83: What is the Inverse Conway Maneuver?
**A:** The Inverse Conway Maneuver is the practice of restructuring teams to match the desired architecture. If you want loosely coupled microservices, reorganize teams to be loosely coupled and aligned with service boundaries. The architecture will naturally follow the team structure.

## Q84: What is Team Topologies?
**A:** Team Topologies is a model for organizing teams around microservices. Four team types: 1) Stream-aligned teams (own a service/feature stream). 2) Enabling teams (help stream-aligned teams with specialized skills). 3) Complicated subsystem teams (manage complex subsystems). 4) Platform teams (provide internal platforms for other teams).

## Q85: How do you handle error handling in microservices?
**A:** Best practices: 1) Return consistent error responses (standard error format). 2) Use appropriate HTTP status codes (400, 401, 403, 404, 409, 500, 503). 3) Include error codes, messages, and correlation IDs. 4) Implement retry with exponential backoff and jitter. 5) Use circuit breakers for failing dependencies. 6) Graceful degradation.

## Q86: What is the Retry pattern with exponential backoff?
**A:** When a request fails, retry with increasing delays between attempts (e.g., 100ms, 200ms, 400ms, 800ms). Jitter adds randomness to prevent the thundering herd problem. Exponential backoff reduces load on failing services and increases the chance of success when the service recovers.

## Q87: What is the Thundering Herd problem?
**A:** The Thundering Herd problem occurs when many clients simultaneously retry a failing service, overwhelming it and preventing recovery. Mitigation strategies include: 1) Exponential backoff with jitter. 2) Circuit breakers to stop retrying. 3) Rate limiting. 4) Bulkheads to isolate clients.

## Q88: What is the Timeout pattern?
**A:** Timeouts prevent a client from waiting indefinitely for a response. Set appropriate timeouts for each external call based on expected response times and SLAs. Use shorter timeouts for synchronous calls and longer for async. Implement timeout cascading (shorter timeouts for critical paths).

## Q89: How do you handle idempotency in microservices?
**A:** An idempotent operation produces the same result regardless of how many times it's executed. Implementation: 1) Client sends a unique idempotency key (UUID) with requests. 2) Server checks if key was already processed and returns cached result. 3) Use database unique constraints to prevent duplicate processing.

## Q90: What is the Competing Consumers pattern?
**A:** The Competing Consumers pattern uses a message queue with multiple consumer instances. Messages are distributed across consumers, each processing independently. Benefits: horizontal scaling of consumers, load leveling, and fault tolerance. Used for processing orders, sending emails, or any parallelizable task.

## Q91: What is the Fan-Out pattern?
**A:** The Fan-Out pattern delivers a single message to multiple consumers simultaneously. In microservices, a service publishes an event to a message broker (like Kafka), and multiple consumer services independently process the event. This enables the Publish-Subscribe pattern for event-driven architectures.

## Q92: What is the difference between a message broker and an event bus?
**A:** A message broker (RabbitMQ, ActiveMQ) manages message queues with routing, persistence, and delivery guarantees, supporting both point-to-point (queues) and pub/sub (topics). An event bus (Kafka, EventBridge) is specialized for event streaming, providing event ordering, replay, and long-term storage.

## Q93: What is Apache Kafka and why is it popular for microservices?
**A:** Apache Kafka is a distributed event streaming platform with high throughput, fault tolerance, and persistence. It is popular for microservices because it provides: 1) Event sourcing and replay. 2) Ordered message delivery per partition. 3) Long-term storage. 4) High throughput (millions of messages/sec). 5) Exactly-once semantics.

## Q94: What are Kafka topics, partitions, and consumer groups?
**A:** A topic is a category/feed name for messages. Partitions divide a topic for parallelism and ordering (messages within a partition are ordered). Consumer groups are groups of consumers that coordinate to consume from topic partitions, with each partition assigned to one consumer in the group.

## Q95: What is a Dead Letter Queue (DLQ)?
**A:** A DLQ stores messages that cannot be processed successfully. When a consumer fails to process a message after retries, the message is sent to a DLQ for later analysis and reprocessing. DLQs prevent message loss and help debug processing failures.

## Q96: How do you handle backpressure in microservices?
**A:** Backpressure is a mechanism to signal a downstream service to slow down when it's overwhelmed. Techniques include: 1) Limiting queue sizes. 2) Using reactive streams (backpressure-aware frameworks). 3) Rate limiting. 4) Load shedding. 5) Circuit breakers. 6) Consumer-side backpressure in message brokers.

## Q97: What is the correlation ID pattern?
**A:** A correlation ID is a unique identifier attached to a request at the entry point and propagated across all subsequent calls. It allows tracing a single request across multiple services. Correlation IDs are essential for debugging, logging, and understanding request flows in microservices.

## Q98: What is the Health Check API pattern?
**A:** A Health Check API exposes endpoints for checking a service's health. Standard patterns: 1) /health/liveness (is the service running). 2) /health/readiness (is the service ready to serve traffic). 3) /health/startup (has the service started). The endpoint checks dependencies (database, message queue, external services).

## Q99: What is the difference between a proxy and a reverse proxy?
**A:** A forward proxy (proxy) acts on behalf of clients, masking client identity from servers. A reverse proxy acts on behalf of servers, masking server topology from clients. In microservices, API Gateway functions as a reverse proxy, and sidecar proxies (Envoy) handle service-to-service communication.

## Q100: Explain the complete architecture of a typical microservices system.
**A:** A typical microservices architecture includes: 1) Client layer (web/mobile apps). 2) API Gateway (single entry point for requests, handles auth, rate limiting, routing). 3) Service layer (individual microservices, each owning its own data and business logic). 4) Communication layer (synchronous via gRPC/REST, async via Kafka/RabbitMQ). 5) Data layer (each service has its own database, polyglot persistence). 6) Service mesh (sidecar proxies for mTLS, observability, traffic management). 7) Observability stack (Prometheus metrics, ELK logs, Jaeger traces, Grafana dashboards). 8) Orchestration (Kubernetes for container management, auto-scaling, service discovery). 9) CI/CD pipeline (automated build, test, deploy per service). 10) Security layer (OAuth2/OIDC, JWT, mTLS, OPA policy enforcement). 11) External integrations (S3, CDN, third-party APIs).
