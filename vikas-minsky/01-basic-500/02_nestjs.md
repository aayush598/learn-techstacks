## 2. NestJS (41–80)

41. What is NestJS and why is it popular?
    N**Answer:** NestJS is a progressive Node.js framework for building efficient, scalable server-side applications. It is popular because it uses TypeScript, follows modular architecture inspired by Angular, and provides built-in support for dependency injection, WebSockets, GraphQL, microservices, and testing.

42. Explain the modular architecture of NestJS.
    N**Answer:** NestJS applications are organized into modules, each encapsulating a domain feature. Modules group related controllers, providers, and imports, enabling separation of concerns, reusability, and lazy loading. The root module bootstraps the application, while feature modules organize business logic.

43. What are providers in NestJS?
    P**Answer:** Providers are classes annotated with `@Injectable` that can be injected into other classes through dependency injection. They include services, repositories, factories, and helpers — any class that provides functionality to other parts of the application.

44. Explain dependency injection in NestJS.
    D**Answer:** Dependency Injection (DI) is a design pattern where NestJS automatically provides dependencies to classes via the constructor. The IoC container manages provider instantiation and lifecycle, resolving the dependency graph without manual wiring.

45. What are decorators in NestJS?
    D**Answer:** Decorators are TypeScript functions that attach metadata to classes, methods, or properties. NestJS uses decorators like `@Controller`, `@Get`, `@Injectable`, `@Module`, and `@Body` to define routes, inject services, and configure modules declaratively.

46. Difference between middleware, guards, interceptors, and pipes?
    M**Answer:** Middleware runs before route handlers for request/response manipulation. Guards determine if a request should proceed based on permissions. Interceptors transform responses or add logic before/after handler execution. Pipes validate and transform incoming data.

47. What are guards used for?
    G**Answer:** Guards determine whether a request should be handled based on conditions like authentication status or user roles. They return a boolean, and if false, NestJS automatically returns a 403 Forbidden response.

48. Explain interceptors with examples.
    I**Answer:** Interceptors wrap request handling to add cross-cutting logic. Examples include logging execution time, transforming response data, caching responses, or wrapping responses in a standard envelope like `{ data, timestamp }`.

49. What are pipes in NestJS?
    P**Answer:** Pipes transform input data or validate it before the route handler receives it. Built-in pipes include `ValidationPipe`, `ParseIntPipe`, and `ParseUUIDPipe`. Custom pipes implement `PipeTransform` for custom validation or transformation logic.

50. What is the request lifecycle in NestJS?
    T**Answer:** The request lifecycle flows through: incoming request → middleware → guards → interceptors (pre-handler) → pipes → route handler → interceptors (post-handler) → exception filters (if error) → response.

51. Explain DTOs in NestJS.
    D**Answer:** DTOs (Data Transfer Objects) are classes that define the shape of data received in requests. They are used with `ValidationPipe` and class-validator decorators to enforce type safety and validation rules on incoming payloads.

52. Why is class-validator used?
    c**Answer:** class-validator provides decorator-based validation like `@IsString()`, `@IsEmail()`, and `@MinLength()` on DTOs. When combined with NestJS's `ValidationPipe`, it automatically validates incoming requests and returns structured error responses.

53. Explain custom decorators.
    C**Answer:** Custom decorators in NestJS are created using `createParamDecorator` or `SetMetadata`. They extract and transform request data, such as `@CurrentUser()` to get the authenticated user from the request object, reducing boilerplate in handlers.

54. How do you implement authentication?
    A**Answer:** Authentication in NestJS typically uses Passport strategies via `@nestjs/passport`. A local strategy validates credentials, while JWT strategy validates tokens. Guards protect routes, and a JWT token is issued on successful login.

55. Explain JWT strategy in NestJS.
    T**Answer:** The JWT strategy extends PassportStrategy, extracts the token from the Authorization header, validates it using a secret or public key, and attaches the decoded payload to the request. It's protected by `@AuthGuard('jwt')`.

56. How do you implement RBAC?
    R**Answer:** RBAC (Role-Based Access Control) is implemented using custom guards that check the user's role from the JWT payload. Roles are defined via `@SetMetadata('roles', ['admin'])` decorators and the guard compares them against the user's roles.

57. Explain exception filters.
    E**Answer:** Exception filters catch thrown exceptions and transform them into structured HTTP responses. NestJS has a built-in global exception filter, but custom filters allow consistent error formatting, logging, and different responses per exception type.

58. How does caching work in NestJS?
    N**Answer:** NestJS provides a `CacheModule` that integrates with stores like Redis. The `@CacheTTL()` and `@CacheKey()` decorators configure caching behavior, and the `CacheInterceptor` automatically caches GET responses based on route and query parameters.

59. Explain microservices support in NestJS.
    N**Answer:** NestJS supports microservices via transport layers like TCP, Redis, RabbitMQ, Kafka, and NATS. It uses `@MessagePattern()` and `@EventPattern()` decorators to define handlers, enabling request-response and event-based communication between services.

60. Difference between REST and GraphQL in NestJS?
    R**Answer:** REST uses controllers with HTTP decorators like `@Get()` and `@Post()`. GraphQL uses resolvers with `@Query()`, `@Mutation()`, and `@Subscription()` decorators, with the `@nestjs/graphql` package providing schema generation from decorators.

61. Explain WebSockets in NestJS.
    W**Answer:** WebSockets are implemented using `@WebSocketGateway()` decorators that create WebSocket servers. Gateways use `@SubscribeMessage()` for event handlers, and support middleware, guards, and interceptors similar to HTTP controllers.

62. How do you use Prisma with NestJS?
    P**Answer:** Prisma integrates via a custom provider that instantiates `PrismaClient` and makes it injectable across the application. The provider handles connection lifecycle, and services use the injected Prisma client for database operations.

63. Explain database transactions in NestJS.
    T**Answer:** Transactions are handled using the `Transactional` decorator from the `typeorm-transactional` package or manually using Prisma's `$transaction` API. They ensure multiple database operations succeed or fail atomically.

64. How do you structure large NestJS projects?
    L**Answer:** Large projects follow modular architecture with feature modules, shared modules for common utilities, database modules for data access, and configuration modules for environment settings. Each module has its own controllers, services, DTOs, and tests.

65. Explain CQRS in NestJS.
    C**Answer:** CQRS (Command Query Responsibility Segregation) separates read and write operations. Commands handle mutations, queries handle reads, and events propagate state changes. NestJS's `@nestjs/cqrs` package provides command/query/event buses.

66. What is EventEmitter in NestJS?
    E**Answer:** EventEmitter (`@nestjs/event-emitter`) enables event-driven communication within the same application process. Services emit events using `eventEmitter.emit()`, while handlers decorated with `@OnEvent()` listen and react asynchronously.

67. How do async providers work?
    A**Answer:** Async providers use `useFactory` with async/await to create dependencies that require asynchronous initialization, like database connections. NestJS awaits the factory result before injecting the provider into dependent classes.

68. Explain custom pipes.
    C**Answer:** Custom pipes implement `PipeTransform<T, R>` interface with a `transform(value, metadata)` method. They receive the input value and either return the transformed value or throw an exception for validation failures.

69. What are dynamic modules?
    D**Answer:** Dynamic modules are modules configured at runtime using a static `register()` or `forRoot()` method that returns a module definition with custom providers, exports, and imports. They enable library configuration like `TypeOrmModule.forRoot()`.

70. Explain middleware execution order.
    M**Answer:** Middleware executes in registration order: globally-bound middleware runs first, then module-level middleware, then controller-level middleware. Middleware registered earlier executes before route handlers and later middleware.

71. How do you test NestJS applications?
    T**Answer:** Testing uses Jest with the `@nestjs/testing` package to create a `TestModule` with mocked providers. Unit tests isolate services, while integration tests create a full NestJS application instance with real or mocked dependencies.

72. Explain unit vs e2e testing.
    U**Answer:** Unit tests test individual classes with mocked dependencies for fast execution. E2E tests create a full application instance (using `createTestingModule` with `supertest`) and test complete request-response cycles against the real API.

73. What is Reflector in NestJS?
    R**Answer:** Reflector is a utility class that retrieves metadata set by decorators. Guards and interceptors use Reflector to read custom metadata, like required roles, from route handlers to make authorization decisions.

74. Explain OpenAPI integration.
    N**Answer:** NestJS integrates with OpenAPI via `@nestjs/swagger`, which generates Swagger documentation from decorators like `@ApiTags()`, `@ApiResponse()`, and DTOs. The Swagger UI is available at a configurable endpoint for API exploration.

75. How do you secure APIs?
    A**Answer:** APIs are secured using guards for authentication and RBAC, Helmet for HTTP headers, rate limiting with `@nestjs/throttler`, input validation with pipes, CORS configuration, and encryption of sensitive data at rest and in transit.

76. Explain throttling in NestJS.
    T**Answer:** Throttling (rate limiting) is implemented via `@nestjs/throttler` module which tracks request counts per IP or user. Exceeding the configured limit results in a 429 Too Many Requests response, preventing abuse and brute force attacks.

77. What are lifecycle hooks?
    N**Answer:** NestJS provides lifecycle hooks like `OnModuleInit`, `OnModuleDestroy`, `OnApplicationBootstrap`, and `OnApplicationShutdown`. Modules and providers implement these interfaces to execute code during application startup and graceful shutdown.

78. How do you handle file uploads?
    F**Answer:** File uploads use the built-in `FileInterceptor` from `@nestjs/platform-express`, which processes multipart/form-data. Files are saved to disk or cloud storage, validated for size and type using pipes, and metadata is stored in the database.

79. Explain validation pipelines.
    V**Answer:** Validation pipelines use the `ValidationPipe` globally, which automatically validates all incoming requests against DTO decorators. It supports whitelisting (stripping unknown properties), transformation (converting strings to numbers), and custom error messages.

80. How do you optimize NestJS performance?
    P**Answer:** Performance optimizations include enabling compression, caching frequent responses, using lazy loading for modules, optimizing database queries with indexes, enabling clustering for multi-core CPU usage, and using the fastify adapter instead of Express.
