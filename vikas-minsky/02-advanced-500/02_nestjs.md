## 21. NestJS Advanced (541–580)

541. How does NestJS metadata reflection work?

   **Answer:** NestJS uses `reflect-metadata` to store decorator metadata at design time. Decorators like `@Controller()` and `@Injectable()` attach metadata on class prototypes, which the runtime reads to build the DI container and route map.

542. Explain inversion of control containers.

   **Answer:** The IoC container manages dependency resolution by instantiating providers and injecting them into constructors. NestJS scans modules, registers providers, and resolves the dependency tree at startup.

543. How do scoped providers work?

   **Answer:** Scoped providers control instance lifetimes: `DEFAULT` (singleton per app), `REQUEST` (new instance per incoming request), and `TRANSIENT` (new instance per injection). Request-scoped providers access per-request context via `REQUEST` token.

544. Explain singleton vs transient providers.

   **Answer:** Singletons share one instance across the entire app, efficient for stateless services. Transient providers create a new instance for every injection, useful for stateful services but increasing memory overhead.

545. How do custom transport layers work?

   **Answer:** Custom transport layers extend NestJS's `Server` and `ClientProxy` classes to support protocols beyond HTTP/TCP. You implement `listen()` and `close()` in the server, and patterns for message handling.

546. Explain message brokers in NestJS.

   **Answer:** NestJS integrates with brokers like RabbitMQ, Kafka, and Redis via transport strategies. It uses `@MessagePattern()` and `@EventPattern()` decorators to define handlers, abstracting broker-specific APIs.

547. How do interceptors transform responses?

   **Answer:** Interceptors implement `NestInterceptor` with `intercept()` returning an `Observable`. They wrap request handling, allowing response mapping, caching, logging, or transformation using `map()` and `tap()` RxJS operators.

548. Explain execution context.

   **Answer:** `ExecutionContext` extends `ArgumentsHost` with details about the current handler: the controller class, method, and argument types. It's used in guards, interceptors, and filters to make context-aware decisions.

549. What are hybrid applications in NestJS?

   **Answer:** Hybrid applications combine multiple transport strategies (HTTP + WebSocket + microservice) in a single NestJS app. You call `app.connectMicroservice()` to add listeners, enabling multi-protocol support.

550. Explain gRPC integration.

   **Answer:** NestJS's gRPC transport uses `@nestjs/microservices` with protobuf-defined services. It generates TypeScript types from `.proto` files, supports bidirectional streaming, and offers efficient binary serialization.

551. How do Kafka integrations work?

   **Answer:** NestJS Kafka uses `@nestjs/microservices` transport with Kafka clients. `@MessagePattern()` handles consumed topics, while `ClientProxy` emits messages. It supports consumer groups, auto-offset commits, and partition assignments.

552. Explain RabbitMQ architecture.

   **Answer:** In NestJS, RabbitMQ uses the `amqplib` transport with exchanges, queues, and bindings. `@RabbitSubscribe` decorators bind handlers to queues, supporting topic, direct, fanout, and headers exchanges.

553. How do event patterns work?

   **Answer:** Event patterns use `@EventPattern()` for fire-and-forget messaging where no response is expected. They are ideal for notifications, logging, and asynchronous side effects in microservice architectures.

554. Explain command handlers.

   **Answer:** Command handlers in CQRS use `@CommandHandler()` decorators to process commands. Each command is a plain object with data; the handler validates, processes, and emits events through the command bus.

555. What are sagas in CQRS?

   **Answer:** Sagas orchestrate long-running transactions by listening to events and issuing commands. They use `@Saga()` decorators with RxJS pipes to react to event streams and coordinate distributed workflows.

556. Explain domain-driven design with NestJS.

   **Answer:** DDD in NestJS structures modules around business domains with entities, value objects, aggregates, repositories, and domain events. NestJS modules serve as bounded contexts with explicit dependencies.

557. How do aggregates work?

   **Answer:** Aggregates are clusters of domain objects treated as a single unit. In NestJS, they are plain classes with invariant logic, ensuring consistency boundaries. Changes go through the aggregate root with event emission.

558. Explain repository patterns.

   **Answer:** Repositories abstract data access behind a collection-like interface. In NestJS, custom repository classes inject database clients and expose domain methods like `findById()` or `save()`, keeping persistence logic out of services.

559. What are anti-corruption layers?

   **Answer:** Anti-corruption layers (ACL) translate between bounded contexts to prevent external model pollution. NestJS implements ACLs as dedicated services or modules that map foreign types to local domain types.

560. Explain transactional outbox patterns.

   **Answer:** The outbox pattern writes events to a database table within the same transaction as the business operation. A separate process (e.g., NestJS scheduler) polls and publishes events, ensuring exactly-once delivery.

561. How do distributed transactions work?

   **Answer:** Distributed transactions coordinate multiple services using the Saga pattern or two-phase commit. NestJS implements sagas with event-driven compensation logic, avoiding distributed locks and long-held DB transactions.

562. Explain eventual consistency.

   **Answer:** Eventual consistency accepts temporary data staleness across services in exchange for availability. NestJS handles this with event-driven architectures where secondary services update asynchronously after domain events.

563. What are idempotent consumers?

   **Answer:** Idempotent consumers track processed message IDs (e.g., in Redis or DB) to safely reprocess duplicates. NestJS microservices implement idempotency keys to ensure at-least-once delivery doesn't cause side effects.

564. Explain OpenTelemetry integration.

   **Answer:** NestJS integrates OpenTelemetry via `@opentelemetry/instrumentation-nestjs-core`. It auto-instruments HTTP, gRPC, and database calls, exporting trace spans to backends like Jaeger or Datadog for observability.

565. How do you implement request tracing?

   **Answer:** Request tracing assigns a unique trace ID per request, propagated via headers like `x-request-id`. NestJS middleware generates the ID, stores it in a context (using `AsyncLocalStorage`), and injects into logs and downstream calls.

566. Explain multi-tenant architecture.

   **Answer:** Multi-tenancy isolates data per tenant (customer). NestJS supports it via middleware deriving tenant from request domain/header, dynamic database selection, or schema-per-tenant using TypeORM's `getRepository()` calls.

567. How do custom adapters work?

   **Answer:** Custom adapters extend NestJS to non-Express frameworks. Implement the `INestApplication` interface and the `HttpServer` abstraction. Plug into lifecycle hooks, and register custom request/response handling.

568. Explain Fastify vs Express adapters.

   **Answer:** Fastify is faster (up to 2x throughput) with lower overhead and built-in schema validation. Express has richer middleware ecosystem. NestJS supports both via `NestFactory.create()` vs `NestFactory.create<NestFastifyApplication>()`.

569. How do async queues integrate?

   **Answer:** Async queues (Bull, Bee, Agenda) integrate via `@nestjs/bull` or custom providers. Jobs are created with `@InjectQueue()` and processed by `@Process()` decorators, supporting concurrency, delays, and repeatable jobs.

570. Explain cron jobs in NestJS.

   **Answer:** Cron jobs use `@nestjs/schedule` with the `@Cron()` decorator accepting cron expressions or time intervals. They run in the Node.js event loop and can integrate with queues or services for scheduled tasks.

571. What are serialization interceptors?

   **Answer:** Serialization interceptors use `ClassSerializerInterceptor` with `@Exclude()` and `@Expose()` decorators to control response output. They automatically strip sensitive fields (e.g., passwords) and transform data shapes.

572. Explain throttler internals.

   **Answer:** NestJS ThrottlerModule tracks request counts per IP/route using an in-memory store or Redis. It compares against the configured `limit` and `ttl`, throwing `HttpException` when exceeded.

573. How do global modules work?

   **Answer:** Global modules decorated with `@Global()` are registered in all modules without re-importing. Their providers are universally available, useful for shared services like logging, config, and database connections.

574. Explain modular monolith architecture.

   **Answer:** A modular monolith structures a single deployable unit into domain modules with explicit boundaries. NestJS modules with `@Module()` define public providers via `exports` and private implementation via internal providers.

575. How do you manage secrets securely?

   **Answer:** Secrets are managed via environment variables loaded from vaults (HashiCorp Vault, AWS Secrets Manager). NestJS's `@nestjs/config` loads validated `.env` files, and production secrets are injected at deploy time.

576. Explain feature module boundaries.

   **Answer:** Feature modules group related controllers, services, and providers. Strict boundaries enforce separation: modules export only what other modules need, using `forRoot()` or `forFeature()` patterns for configuration.

577. What are anti-patterns in NestJS?

   **Answer:** Common anti-patterns include giant controllers, circular dependencies between modules, leaking infrastructure logic into services, over-using `REQUEST` scope hurting performance, and bypassing the DI container.

578. Explain backend observability.

   **Answer:** Observability aggregates logs, metrics, and traces. NestJS uses `@nestjs/common` Logger for structured logs, OpenTelemetry for distributed traces, and `@opentelemetry/metrics` for request rates, latencies, and error counts.

579. How do you profile CPU-heavy requests?

   **Answer:** Profile CPU-heavy requests using Node.js `--prof` and `clinic.js` flamegraphs. In NestJS, wrap suspect code with `console.time()` pairs or use `@opentelemetry` spans to pinpoint slow zones.

580. Explain production hardening techniques.

   **Answer:** Hardening includes rate limiting (ThrottlerModule), input validation (ValidationPipe with whitelist), helmet security headers, CSRF protection, logging sanitization, shutting down gracefully with `enableShutdownHooks()`, and using distroless Docker images.
