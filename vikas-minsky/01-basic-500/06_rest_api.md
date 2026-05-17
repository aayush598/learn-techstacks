## 6. REST API (171–200)

171. What is REST?
     REST (Representational State Transfer) is an architectural style for designing networked applications. It uses stateless, cacheable client-server communication over HTTP, where resources are identified by URLs and manipulated through standard HTTP methods.

172. What are REST constraints?
     The six constraints are: Uniform Interface (consistent resource identification), Stateless (no client context stored server-side), Cacheable (responses marked as cacheable or not), Client-Server (separation of concerns), Layered System (intermediaries like proxies), and Code on Demand (optional, executable code from server).

173. Difference between REST and GraphQL?
     REST uses fixed endpoints returning predefined data structures, while GraphQL uses a single endpoint where clients specify exactly what data they need. REST is simpler but can over/under-fetch; GraphQL is flexible but has more complex caching and rate limiting.

174. Explain idempotency.
     Idempotency means making the same request multiple times produces the same result as making it once. GET, PUT, DELETE, and PATCH are idempotent (with proper implementation) — repeating them doesn't cause different side effects. POST is not idempotent.

175. Difference between PUT and PATCH?
     PUT replaces the entire resource with the request body — omitting fields sets them to null or defaults. PATCH applies partial modifications to a resource, updating only the specified fields while leaving others unchanged.

176. What are HTTP status codes?
     Status codes indicate request outcomes: 1xx (informational), 2xx (success — 200 OK, 201 Created, 204 No Content), 3xx (redirection), 4xx (client error — 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 429 Rate Limited), 5xx (server error — 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable).

177. Explain authentication vs authorization.
     Authentication verifies identity ("who you are") through credentials like passwords, tokens, or biometrics. Authorization determines permissions ("what you can do") based on roles, scopes, or policies — typically enforced through access control mechanisms.

178. What is JWT?
     JWT (JSON Web Token) is a compact, self-contained token format with three parts: header (algorithm + type), payload (claims like user ID, role, expiry), and signature (verifies integrity). It is used for stateless authentication — the server validates the signature without storing session data.

179. Explain OAuth.
     OAuth 2.0 is an authorization framework that allows third-party applications to access resources on behalf of a user without sharing credentials. It uses authorization grants like Authorization Code, Client Credentials, and Refresh Tokens with specific flows.

180. What are refresh tokens?
     Refresh tokens are long-lived tokens that obtain new access tokens without requiring the user to re-authenticate. They are stored securely (often HTTP-only cookies) and exchanged for short-lived access tokens (typically 15-60 minutes), balancing security and user experience.

181. Explain API versioning.
     API versioning manages changes to APIs over time, ensuring backward compatibility. Strategies include URL versioning (`/v1/users`, `/v2/users`), header-based versioning (`Accept: application/vnd.api.v2+json`), and query parameter versioning (`?version=2`).

182. What are rate limits?
     Rate limits restrict how many API requests a client can make in a time window. They prevent abuse and ensure fair resource allocation. Limits are communicated via headers like `X-RateLimit-Remaining` and enforced with status code 429.

183. Explain pagination strategies.
     Pagination strategies include offset-based (page/offset parameters — simple but inconsistent with data changes), cursor-based (cursor parameter — consistent for real-time data), and keyset pagination (using last seen ID — efficient for ordered data).

184. What is cursor pagination?
     Cursor pagination uses a unique pointer (cursor) from the last item to fetch the next page. It's more consistent than offset pagination because adding or removing items doesn't shift results. Cursors are often opaque encoded strings.

185. Explain HATEOAS.
     HATEOAS (Hypermedia As The Engine Of Application State) is a REST constraint where API responses include links to related actions. Clients navigate the API dynamically through these hypermedia links rather than hardcoding URL patterns.

186. What are webhooks?
     Webhooks are HTTP callbacks triggered by events — instead of polling, the server sends POST requests to a registered URL when something happens. They are used for real-time notifications, event-driven integrations, and async processing.

187. Explain API caching.
     API caching stores responses to reduce server load and improve latency. Strategies include HTTP caching with `Cache-Control` headers, response-level caching in Redis, CDN caching for GET endpoints, and ETags for conditional requests.

188. What are ETags?
     ETags are response headers that uniquely identify a resource version. Clients send the ETag in `If-None-Match` headers, and the server returns 304 Not Modified if the resource hasn't changed, saving bandwidth and processing time.

189. Explain CORS.
     CORS (Cross-Origin Resource Sharing) is a browser security mechanism that controls which domains can access resources. The server sets `Access-Control-Allow-Origin` and related headers to permit specific origins, methods, and headers for cross-origin requests.

190. What are API gateways?
     API gateways are entry points that route requests to backend services. They handle authentication, rate limiting, load balancing, request transformation, caching, monitoring, and aggregation — simplifying client code and centralizing cross-cutting concerns.

191. Explain request validation.
     Request validation checks incoming data against defined rules before processing. It validates types, formats, ranges, and required fields, returning clear error messages for invalid data. Validation prevents malformed data from reaching business logic.

192. What are API contracts?
     API contracts are formal agreements defining request/response formats, endpoints, authentication methods, and error codes. They enable parallel frontend/backend development, automated testing, and are documented via OpenAPI/Swagger specs.

193. Explain OpenAPI/Swagger.
     OpenAPI (formerly Swagger) is a specification language for describing REST APIs in a machine-readable format (JSON/YAML). It documents endpoints, request/response schemas, authentication, and generates interactive API documentation, client SDKs, and server stubs.

194. How do you secure APIs?
     Secure APIs with authentication (JWT/OAuth), authorization (RBAC/scopes), input validation, rate limiting, HTTPS/TLS, CORS configuration, security headers (Helmet), API keys for machine-to-machine, encryption at rest and transit, and regular security audits.

195. Explain API monitoring.
     API monitoring tracks metrics like request volume, latency, error rates, and availability. It uses health check endpoints, synthetic monitoring (automated probes), real-user monitoring (RUM), logging, alerting, and dashboards (Datadog, Grafana, Sentry).

196. What are retries and backoff strategies?
     Retries resend failed requests automatically. Backoff strategies determine wait time between retries: fixed (constant delay), exponential (doubling delay), jitter (randomizing delay to avoid thundering herd), and immediate (no delay, for idempotent operations).

197. Explain circuit breakers.
     Circuit breakers prevent cascading failures by monitoring error rates. When failures exceed a threshold, the circuit "opens" and subsequent requests fail immediately without hitting the service. After a timeout, it "half-opens" to test recovery before fully closing.

198. What are distributed systems failures?
     Common failures include network partitions, node crashes, latency spikes, data inconsistency, race conditions, and cascading failures. Mitigation strategies include redundancy, graceful degradation, bulkheads, timeouts, retries with backoff, and circuit breakers.

199. Explain API testing strategies.
     Strategies include unit tests for validation logic, integration tests for endpoints, contract tests for API agreements, E2E tests for full workflows, performance tests for load handling, and security tests for authentication, authorization, and injection vulnerabilities.

200. How do you design scalable APIs?
     Design with statelessness (horizontal scaling), caching (reduce load), rate limiting (prevent abuse), pagination (limit payloads), async processing (background jobs), database optimization (indexes, query tuning), CDN for static content, and microservices decomposition for independent scaling.
