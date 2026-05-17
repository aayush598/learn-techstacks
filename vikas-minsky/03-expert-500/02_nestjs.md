## 40. NestJS Expert Topics (1041–1080)

1041. How do custom parameter decorators work?
   Custom parameter decorators in NestJS are factory functions that return a decorator using `createParamDecorator`, which extracts data from the execution context (request, response, headers) and transforms it before injecting it into the handler. They enable reusable extraction logic like `@CurrentUser()`.

1042. Explain dependency graph resolution.
   NestJS's DI container resolves the dependency graph at startup by analyzing constructor parameters and provider metadata. It topologically sorts providers to ensure each dependency is instantiated before its consumer, detecting circular references.

1043. What are circular dependency issues?
   Circular dependencies occur when two modules or providers depend on each other directly or transitively, causing the DI container to fail during instantiation. NestJS detects these at startup and throws an error unless explicitly resolved.

1044. Explain forwardRef usage.
   `forwardRef` wraps a provider reference in a lazy resolver that NestJS evaluates after the container is fully initialized, breaking circular dependency chains. It's essential for bidirectional module relationships but should be used sparingly.

1045. How does NestJS compile metadata?
   NestJS leverages TypeScript's experimental decorators and `reflect-metadata` to emit design-time type information (parameter types, return types) that the framework reads for runtime injection, validation, and serialization configuration.

1046. Explain request-scoped providers performance tradeoffs.
   Request-scoped providers (`SCOPE.REQUEST`) are instantiated per incoming request, increasing memory allocation and garbage collection overhead compared to singletons. They also bypass DI container optimizations like caching.

1047. What are interceptor chaining patterns?
   Interceptors execute in declaration order around route handlers, forming a middleware-like pipeline. Common patterns include logging, timing, caching, and response transformation, with each interceptor able to modify the observable stream.

1048. Explain protocol abstraction in NestJS.
   NestJS abstracts transport protocols (HTTP, WebSocket, gRPC, TCP, MQTT) behind a common `ExecutionContext` interface, allowing the same interceptors, guards, and pipes to work across different transports without modification.

1049. How does NestJS support hybrid transports?
   Hybrid transports allow a single NestJS application to listen on multiple protocols simultaneously, such as HTTP for REST endpoints and WebSocket for realtime communication, sharing the same DI container and providers.

1050. Explain API gateway microservice architecture.
   In this architecture, a NestJS API gateway receives all client requests and forwards them to internal microservices via transport protocols. The gateway handles auth, rate limiting, aggregation, and protocol translation.

1051. What are bounded contexts?
   Bounded contexts from Domain-Driven Design delineate explicit boundaries where a domain model applies consistently. Each microservice owns its bounded context, preventing model leakage and reducing coupling between teams.

1052. Explain service orchestration patterns.
   Service orchestration uses a central coordinator (orchestrator) that manages the execution flow across multiple services, handling success/failure decisions, compensations, and state management. NestJS implements this through saga patterns.

1053. How do event buses scale?
   Event buses scale horizontally by partitioning events across multiple consumer groups, using message brokers like RabbitMQ or Kafka. NestJS's custom transport layer allows transparent backpressure handling and retry policies.

1054. Explain asynchronous domain events.
   Asynchronous domain events decouple the event publisher from subscribers using message queues, ensuring the publisher doesn't block on subscriber processing. NestJS supports this with `@nestjs/cqrs` EventBus publishing to transport layers.

1055. What are distributed saga patterns?
   Sagas manage long-running business transactions across microservices by defining a sequence of local transactions with compensating actions for rollback. NestJS implements choreographed sagas via event handlers and orchestrator services.

1056. Explain aggregate consistency boundaries.
   Aggregate boundaries define which entities are modified atomically within a single transaction. In NestJS, aggregates are loaded through repositories and their changes are flushed together to maintain consistency.

1057. How does CQRS reduce write contention?
   CQRS separates read and write models, allowing write operations to focus on simple command handlers without read-side concerns. NestJS's CQRS module provides command and event buses that decouple the two paths.

1058. Explain anti-corruption mapping.
   Anti-corruption layers translate between a service's internal domain model and external system models, preventing foreign concepts from leaking into the core domain. In NestJS, these are implemented as translation services or adapters.

1059. What are API composition services?
   API composition services aggregate data from multiple downstream services into a single response, reducing client-side chattiness. NestJS gateways implement this using parallel async requests with error aggregation.

1060. Explain dynamic provider registration.
   Dynamic providers are registered at runtime based on configuration or environment conditions using `useFactory`, `useClass`, or `useExisting` syntax. This enables conditional feature toggling and environment-specific implementations.

1061. How does lazy module loading work?
   Lazy module loading defers module initialization until the first request to its routes, reducing startup memory and time. NestJS supports this through dynamic imports in route configuration, though it's limited compared to framework-native lazy loading.

1062. Explain request tracing correlation IDs.
   Correlation IDs are unique identifiers attached to each incoming request and propagated across all downstream service calls via headers or context. NestJS implements this through middleware that generates and forwards the ID.

1063. What are backend resilience patterns?
   Backend resilience patterns include circuit breakers, retries with exponential backoff, timeouts, bulkheads, and fallback responses. These prevent cascading failures and ensure the system degrades gracefully under stress.

1064. Explain fallback mechanisms.
   Fallback mechanisms provide alternative responses when primary service calls fail, such as cached data, default values, or degraded functionality. NestJS's interceptors can wrap handlers to apply fallback logic transparently.

1065. How does bulkhead isolation work?
   Bulkhead isolation partitions system resources (thread pools, connection pools) into separate compartments so that failure in one partition doesn't exhaust resources for others. NestJS configures this through custom thread pools and connection limits.

1066. Explain token bucket throttling.
   Token bucket throttling limits request rates by issuing tokens at a fixed rate and requiring each request to consume a token. Bursts are allowed up to the bucket capacity, smoothing traffic spikes.

1067. What are asynchronous validation patterns?
   Async validation patterns use validation pipes that return Promises, allowing database lookups or external API calls during validation. NestJS's `ValidationPipe` supports this natively with `async` validator functions.

1068. Explain serialization performance optimization.
   Serialization optimization involves using class-transformer decorators sparingly, excluding unnecessary fields with `@Exclude()`, and leveraging interceptors that skip serialization for non-API responses.

1069. How do backend gateways manage auth?
   Backend gateways manage authentication by validating tokens at the gateway layer before forwarding requests to internal services, typically using JWT validation with public keys. This centralizes auth logic and prevents unauthorized access to microservices.

1070. Explain backend caching layers.
   Backend caching layers use in-memory caches (Redis) at the API gateway and service levels to reduce database load. Cache-aside and write-through patterns with configurable TTLs balance freshness with performance.

1071. What are API orchestration bottlenecks?
   API orchestration bottlenecks include sequential downstream calls, inefficient data aggregation, oversized response payloads, and gateway CPU contention from serialization. Parallel fetching and response streaming mitigate these.

1072. Explain monolith decomposition strategies.
   Decomposition strategies include extracting services by bounded context, by change frequency (Strangler Fig pattern), or by scalability requirements. NestJS's modular architecture makes this incremental extraction simpler.

1073. How does NestJS support modular testing?
   NestJS's `Test` module creates isolated testing modules with custom providers, enabling unit and integration tests without booting the entire application. Mocks replace external dependencies via the DI container.

1074. Explain backend memory leak detection.
   Memory leak detection uses heap snapshots, GC tracing, and monitoring of resident set size over time. Common NestJS leak sources include unclosed event listeners, growing caches, and circular references in providers.

1075. What are health aggregation endpoints?
   Health aggregation endpoints (`/health`) collect status from all service dependencies (databases, caches, external APIs) and return a composite status. NestJS's `@nestjs/terminus` provides structured health checks.

1076. Explain backend startup optimization.
   Startup optimization techniques include lazy-loading non-critical modules, parallelizing provider initialization, reducing import depth, and using faster serialization libraries.

1077. How do you harden public APIs?
   Public APIs are hardened through rate limiting, input validation with strict schemas, CORS configuration, SQL injection prevention, authentication enforcement, response sanitization, and comprehensive error handling.

1078. Explain backend chaos engineering.
   Chaos engineering injects failures (latency, crashes, resource exhaustion) into production systems to test resilience. NestJS applications can integrate chaos libraries that interrupt request processing at defined points.

1079. What are enterprise NestJS governance practices?
   Enterprise governance includes standardized module structure, code generation schematics, shared ESLint/Prettier configs, API versioning strategies, and deprecation policies. Teams enforce consistency through CI lint checks.

1080. How do you evolve backend architecture over time?
   Backend architecture evolves through incremental extraction of bounded contexts into services, adopting event-driven communication, and gradually replacing synchronous calls with async messaging. NestJS's modular design supports this organic growth.
