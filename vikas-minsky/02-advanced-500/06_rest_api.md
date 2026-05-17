## 25. REST API Advanced (671–700)

671. Explain Richardson maturity model.

   **Answer:** The model has four levels: Level 0 (single endpoint with tunneling), Level 1 (resource-based URIs), Level 2 (HTTP verbs + status codes), and Level 3 (hypermedia controls). APIs evolve toward level 3 for self-discoverability.

672. How do hypermedia APIs work?

   **Answer:** Hypermedia APIs (HATEOAS) include links in responses that guide clients to related actions (e.g., `{"next": "/orders/123"}`). Clients navigate by following links rather than hardcoding URLs.

673. Explain API discoverability.

   **Answer:** Discoverability allows clients to explore API capabilities dynamically via well-known endpoints (e.g., `/docs`, `/schema`, `/health`) and hypermedia links, reducing the need for external documentation.

674. What are safe HTTP methods?

   **Answer:** Safe methods (GET, HEAD, OPTIONS) don't modify server state. They should be idempotent and cacheable. Unsafe methods (POST, PUT, PATCH, DELETE) alter resources and require appropriate safeguards.

675. Explain API idempotency keys.

   **Answer:** Idempotency keys (e.g., `Idempotency-Key` header) ensure that retrying a request produces the same result. The server stores processed keys for a window, rejecting duplicate requests safely.

676. How do distributed rate limits work?

   **Answer:** Distributed rate limits use a centralized store like Redis for atomic counters. Token bucket or sliding window algorithms track usage per user/IP/API key across multiple service instances.

677. Explain request signing.

   **Answer:** Request signing cryptographically signs HTTP requests using HMAC or asymmetric keys. The receiver verifies the signature, ensuring request integrity and authenticity. AWS SigV4 is a common implementation.

678. What are replay attacks?

   **Answer:** Replay attacks resend captured valid requests to trick the server. Mitigations include timestamps (reject old requests), nonces (one-time tokens), and signature expiration windows.

679. Explain API federation.

   **Answer:** API federation unifies multiple services behind a single graph/API, allowing clients to query across domains. GraphQL federation and Apollo Federation are examples, enabling separation of concerns at the service level.

680. How do API aggregators work?

   **Answer:** API aggregators combine responses from multiple backend services into a single client response. They reduce network round trips for the client but can become bottlenecks if not designed with parallel execution.

681. Explain backend-for-frontend architecture.

   **Answer:** BFF creates dedicated API layers per client type (web, mobile, IoT). Each BFF tailors data aggregation, authentication, and response shapes to its client's specific needs, avoiding one-size-fits-all APIs.

682. What are API composition patterns?

   **Answer:** API composition includes client-side composition (multiple calls), server-side aggregation (BFF pattern), GraphQL query resolution, and API gateway composition with response merging.

683. Explain API throttling strategies.

   **Answer:** Throttling strategies include rate limiting (requests per time window), concurrency limiting (max in-flight requests), quota management (daily/monthly allowances), and adaptive throttling based on system load.

684. How do reverse proxies work?

   **Answer:** Reverse proxies (Nginx, HAProxy) sit in front of API servers, handling TLS termination, load balancing, caching, request routing, and rate limiting. They shield backend services from direct client exposure.

685. Explain CDN integration with APIs.

   **Answer:** CDNs cache API responses at edge nodes, reducing latency and origin load. Cacheable responses (GET, with `Cache-Control` headers) are served from the edge, while dynamic requests pass through to origin.

686. What are eventual consistency APIs?

   **Answer:** Eventual consistency APIs return stale data immediately and propagate updates asynchronously. They use patterns like CQRS, event sourcing, and webhooks to reconcile state over time.

687. Explain API contract testing.

   **Answer:** Contract testing validates that API providers and consumers adhere to a shared specification (OpenAPI, Pact). It catches breaking changes early by testing consumer expectations against provider responses.

688. How do webhooks ensure reliability?

   **Answer:** Webhooks achieve reliability with retry mechanisms (exponential backoff), idempotency headers (`Idempotency-Key`), delivery receipts, payload signing for verification, and dead-letter queues for failed deliveries.

689. Explain dead-letter queues.

   **Answer:** Dead-letter queues (DLQs) store messages that failed processing after exhausting retries. They enable manual inspection, reprocessing, or auditing without losing data or blocking the main queue.

690. What are compensating transactions?

   **Answer:** Compensating transactions undo the effects of a previous operation in a distributed system. They implement the Saga pattern: each transaction has a compensating action (e.g., "cancel order" reverses "create order").

691. Explain webhook signature validation.

   **Answer:** Webhook signatures use HMAC with a shared secret to sign payloads. The receiver computes the HMAC of the body and compares it to the `X-Signature` header, ensuring payload integrity and sender authenticity.

692. What are anti-patterns in REST?

   **Answer:** Common REST anti-patterns include using GET for mutations, ignoring HTTP status codes (always returning 200), monolithic endpoints carrying redundant data, overly nested resources, and lacking hypermedia.

693. Explain API deprecation strategies.

   **Answer:** Deprecation strategies include versioning (`/v1/` → `/v2/`), `Sunset` and `Deprecation` headers, migration guides, parallel support periods, and usage monitoring before removing old endpoints.

694. How do API gateways handle auth?

   **Answer:** API gateways centralize authentication by validating tokens (JWT, OAuth2), forwarding user identity to services via headers, and enforcing RBAC/ABAC policies before requests reach upstream services.

695. Explain service mesh basics.

   **Answer:** A service mesh (Istio, Linkerd) abstracts inter-service communication via sidecar proxies. It handles service discovery, mTLS, traffic splitting, observability, and circuit breaking without application changes.

696. What are distributed tracing IDs?

   **Answer:** Trace IDs uniquely identify a request across multiple services. Each service propagates the ID via headers (e.g., `x-trace-id`), and tracing systems (Jaeger, Zipkin) correlate spans to reconstruct request flows.

697. Explain API observability.

   **Answer:** API observability encompasses logs (structured requests/responses), metrics (latency, error rate, throughput), and distributed tracing. Together they enable debugging, capacity planning, and SLA monitoring.

698. How do retries cause duplicate writes?

   **Answer:** Retries can cause duplicate writes if the first request succeeded but the client timeout occurred before receiving the response. Idempotency keys and deduplication logic prevent duplicate processing.

699. Explain chaos engineering for APIs.

   **Answer:** Chaos engineering intentionally injects failures (latency, crashes, throttling) to test API resilience. Tools like Chaos Monkey verify that timeouts, retries, circuit breakers, and fallbacks work correctly.

700. How do large startups structure APIs?

   **Answer:** Large startups use domain-oriented API gateways with BFF per client, internal microservices communicating via gRPC, event-driven patterns for async workflows, GraphQL for complex queries, and OpenAPI for documentation.
