## 44. REST API Expert Topics (1171–1200)

1171. How do APIs maintain backward compatibility?
   APIs maintain backward compatibility by following additive-only changes—adding new fields, endpoints, or parameters without modifying existing contracts. Renaming, removing, or changing types of existing fields is avoided, and deprecations follow a documented sunset policy.

1172. Explain semantic API versioning.
   Semantic API versioning uses `v1`, `v2` prefixes in URLs or `Accept` headers, where major version bumps signal breaking changes. Minor revisions are backward-compatible additions, and patch versions cover internal fixes without contract changes.

1173. What are API orchestration gateways?
   API orchestration gateways aggregate responses from multiple downstream services into a single response for the client, reducing network chattiness. They handle composition logic, error aggregation, and protocol translation at the edge.

1174. Explain edge authentication.
   Edge authentication validates tokens at the CDN or API gateway level before requests reach the origin server, reducing unauthorized traffic and offloading auth overhead. Stateless JWT validation with cached public keys enables this at low latency.

1175. How do APIs implement request replay prevention?
   Request replay prevention uses nonces (one-time-use tokens) or timestamp-based signatures with a tolerance window. Idempotency keys allow safe retries by tracking processed requests, while replay attacks reuse captured requests beyond their validity.

1176. Explain API tenancy isolation.
   Tenancy isolation separates data and rate limits per tenant using API keys or JWT claims that identify the tenant ID. Strategies include database row-level security, schema-per-tenant, or dedicated service instances for high-security customers.

1177. What are quota enforcement strategies?
   Quota enforcement uses token bucket or sliding window counters per API key, returning `429 Too Many Requests` with `Retry-After` headers. Distributed counters in Redis ensure accuracy across multiple gateway instances.

1178. Explain API monetization models.
   API monetization models include pay-per-call, tiered subscriptions with rate limits, usage-based pricing with metering, and revenue sharing for marketplace APIs. Each model requires accurate billing integration and usage analytics.

1179. How do signed URLs work?
   Signed URLs embed an expiration timestamp and a cryptographic signature (HMAC) in the query string. The server validates the signature and timestamp before serving the request, enabling temporary access to protected resources without authentication.

1180. Explain distributed authorization systems.
   Distributed authorization systems use policy-based access control (OPA, Casbin) where authorization decisions are made locally using cached policies. This avoids centralized auth bottlenecks and allows consistent enforcement across services.

1181. What are API fan-out problems?
   API fan-out occurs when a single request triggers many downstream calls, multiplying latency and failure risk. Solutions include batching, parallel async calls, caching, and using CQRS with materialized views.

1182. Explain request collapsing in gateways.
   Request collapsing merges concurrent requests for the same resource into a single upstream call, broadcasting the response to all requesters. This reduces backend load during traffic spikes and improves overall throughput.

1183. How do APIs maintain consistency across services?
   Cross-service consistency uses distributed transactions (Saga patterns), event-driven eventual consistency, or two-phase commit for critical paths. Most APIs embrace eventual consistency with idempotent operations and conflict resolution.

1184. Explain API aggregation latency issues.
   Aggregation latency accumulates from each downstream call's network round trip and processing time. Parallelization, streaming responses, and pre-fetched caches reduce this, but the slowest dependency remains the bottleneck.

1185. What are gateway bottlenecks?
   Gateway bottlenecks include CPU-bound serialization/deserialization, I/O on TLS termination, memory limits on concurrent connections, and slow downstream responses blocking worker threads. Horizontal scaling and async I/O patterns mitigate these.

1186. Explain API schema registries.
   Schema registries (Apollo Studio, Confluent Schema Registry) store and version API schemas centrally, enabling contract validation, consumer discovery, and backward-compatibility checks in CI/CD pipelines.

1187. How does API caching interact with auth?
   API caching must consider auth context: private data shouldn't leak between users via shared caches. Strategies include cache-per-user keys, `Vary: Authorization` headers, and edge caching only for public data.

1188. Explain eventual consistency in APIs.
   Eventual consistency means API responses may reflect stale data that will converge over time. APIs signal this through `Last-Modified` headers, ETags, and documentation. Clients must handle stale reads and retry for fresh data.

1189. What are compensating API workflows?
   Compensating workflows reverse previously completed operations when a later step fails, implementing the Saga pattern. Each operation has a corresponding compensation action (e.g., cancel order after payment failure).

1190. Explain idempotent payment APIs.
   Idempotent payment APIs use idempotency keys sent by the client. The server stores the result of the first request with that key and returns the same result for duplicate requests, preventing double charges.

1191. What are webhook replay attacks?
   Webhook replay attacks resend captured webhook payloads to trigger duplicate actions. Mitigations include unique webhook IDs, timestamp validation with tolerance windows, and signature verification (HMAC) over the payload body.

1192. Explain API governance models.
   API governance models define standards for naming conventions, error formats, pagination, authentication, rate limiting, and versioning. Centralized API teams enforce these through linting (Spectral), design reviews, and API scorecards.

1193. How do API contracts evolve safely?
   API contracts evolve by adding optional fields, using `x-` extension properties, and introducing new minor version endpoints. Breaking changes are communicated via deprecation headers (`Sunset`), changelogs, and migration guides.

1194. Explain API-first architecture.
   API-first architecture designs the API contract before implementing backend or frontend, using specification-driven development (OpenAPI). This enables parallel work, automated SDK generation, and contract testing early in the lifecycle.

1195. What are observability pipelines for APIs?
   Observability pipelines collect metrics (latency, error rate, throughput), logs (structured request/response), and traces across API calls. Tools like OpenTelemetry propagate trace context through HTTP headers for distributed tracing.

1196. Explain high-throughput gateway design.
   High-throughput gateways use async I/O, connection pooling, zero-copy serialization (Protobuf, FlatBuffers), and caching at every layer. They're horizontally scaled behind a load balancer with health checks and circuit breakers.

1197. What are API degradation strategies?
   Degradation strategies include graceful degradation (returning partial data when a dependency fails), shedding load via rate limiting, and using stale cache fallbacks when upstream services are unavailable.

1198. Explain traffic shadowing.
   Traffic shadowing duplicates real requests to a new API version or service without affecting the response to the client. This tests the new system under real-world load before switching traffic, with results compared offline.

1199. What are API sandbox environments?
   Sandbox environments provide isolated API instances with synthetic data for client development and testing. They simulate production behavior, including error responses and rate limits, without affecting real users or data.

1200. How do unicorn startups manage API ecosystems?
   Unicorn startups manage API ecosystems with a platform team that owns the gateway, developer portal, and SDK generation. They enforce governance through automated linting and contract tests, while giving product teams autonomy to iterate rapidly.
