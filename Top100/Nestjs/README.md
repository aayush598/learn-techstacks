# NestJS Interview Questions and Answers

## Q1: What is NestJS?
**A:** NestJS is a progressive Node.js framework for building efficient, reliable, and scalable server-side applications. It uses TypeScript by default and combines elements of OOP, FP, and FRP. It is built on top of Express (or Fastify) and uses decorators heavily.

## Q2: What are the core building blocks of NestJS?
**A:** The core building blocks are: Modules (organize code), Controllers (handle incoming requests), Providers/Services (business logic), Middleware (request processing), Guards (authentication), Interceptors (transform results), Pipes (validation/transformation), and Filters (error handling).

## Q3: What is a Module in NestJS?
**A:** A Module is a class annotated with `@Module()` decorator that organizes related components (controllers, providers, exports) into a cohesive unit. Every NestJS app has at least one root module. Modules can import other modules, making them the fundamental organizational unit.

## Q4: What is a Controller in NestJS?
**A:** A Controller is a class annotated with `@Controller()` that handles incoming HTTP requests and returns responses. It uses route decorators like `@Get()`, `@Post()`, `@Put()`, `@Delete()` to map methods to routes. Controllers should be lightweight, delegating business logic to providers.

## Q5: What is a Provider in NestJS?
**A:** A Provider is a class annotated with `@Injectable()` that contains business logic, database access, or utility functions. Providers are dependency-injected into controllers or other providers. Services are the most common type of provider.

## Q6: How does Dependency Injection work in NestJS?
**A:** NestJS uses constructor-based DI. Providers are registered in modules and injected via constructor parameters using TypeScript type annotations. The NestJS IoC container resolves dependencies automatically, managing object creation and lifecycle.

## Q7: What are the scopes for providers in NestJS?
**A:** Singleton (default): one instance shared across the app; Request: a new instance per incoming request; Transient: a new instance per injection. Scopes are set via the `@Injectable({ scope: Scope.REQUEST })` decorator.

## Q8: What is a Middleware in NestJS?
**A:** Middleware is a function that runs before the route handler. It has access to the request and response objects. Implemented as either a class with `@Injectable()` implementing `NestMiddleware` or a function. Used for logging, parsing, session management, etc.

## Q9: What is a Guard in NestJS?
**A:** A Guard is a class annotated with `@Injectable()` implementing `CanActivate`. It determines whether a request should be handled by the route handler based on conditions (permissions, roles, authentication). Guards run after middleware but before interceptors and pipes.

## Q10: What is an Interceptor in NestJS?
**A:** An Interceptor is a class annotated with `@Injectable()` implementing `NestInterceptor`. It wraps request/response handling, allowing transformation of results, binding extra logic before/after method execution, or transforming errors. Inspired by Aspect Oriented Programming.

## Q11: What is a Pipe in NestJS?
**A:** A Pipe is a class annotated with `@Injectable()` implementing `PipeTransform`. It transforms input data or validates it, throwing exceptions for invalid data. Built-in pipes: `ValidationPipe`, `ParseIntPipe`, `ParseUUIDPipe`, etc.

## Q12: What is a Filter in NestJS?
**A:** An Exception Filter is a class annotated with `@Catch()` implementing `ExceptionFilter`. It handles uncaught exceptions and returns appropriate responses. NestJS provides a built-in global exception filter, but custom filters allow fine-grained error handling.

## Q13: How do you create a basic NestJS application?
**A:** Install CLI: `npm i -g @nestjs/cli`, create project: `nest new project-name`. The CLI generates a scaffold with a root module, controller, and service. Start with `npm run start:dev` for development with hot-reload.

## Q14: What is the difference between NestJS and Express.js?
**A:** Express is unopinionated and minimal, requiring developers to structure the app manually. NestJS is opinionated, providing a modular architecture (Modules, Controllers, Providers), built-in DI, decorators, and support for GraphQL, WebSockets, and microservices out of the box.

## Q15: How does NestJS support TypeScript?
**A:** NestJS is built with TypeScript and uses decorators extensively for metadata definition. It provides strong typing, interfaces, generics, and enables compile-time error checking. While NestJS can be used with JavaScript, TypeScript is the primary language.

## Q16: What decorators does NestJS provide for routing?
**A:** `@Controller('prefix')` defines a controller and its route prefix. Method decorators: `@Get()`, `@Post()`, `@Put()`, `@Delete()`, `@Patch()`, `@Options()`, `@Head()`, `@All()`. Parameter decorators: `@Param()`, `@Query()`, `@Body()`, `@Headers()`, `@Req()`, `@Res()`.

## Q17: How do you handle validation in NestJS?
**A:** Using the `ValidationPipe` with class-validator decorators. Define DTOs as classes with decorators like `@IsString()`, `@IsInt()`. Apply the pipe globally, at the controller level, or at the method parameter level with `@Body(new ValidationPipe())`.

## Q18: What is the `@Injectable()` decorator?
**A:** `@Injectable()` marks a class as a provider that can be managed by the NestJS IoC container and injected as a dependency. It is used for services, repositories, guards, interceptors, pipes, and filters.

## Q19: What is the `@Module()` decorator?
**A:** `@Module()` defines a module's metadata object with properties: `imports` (imported modules), `controllers` (controllers in this module), `providers` (providers to be instantiated), and `exports` (providers visible to other modules).

## Q20: How do you share providers between modules?
**A:** Export the provider in the module's `exports` array and import that module in the consuming module. NestJS reuses the same provider instance (singleton scope) across all modules that import it.

## Q21: What is a circular dependency and how to solve it?
**A:** Circular dependency occurs when Module A imports Module B and Module B imports Module A. Solutions: use `forwardRef(() => ModuleB)` in the imports array, restructure modules to extract shared components, or use `@Inject(forwardRef(() => ServiceB))` at the provider level.

## Q22: How does NestJS handle asynchronous providers?
**A:** Use `useFactory` with `async` in the provider definition. The factory function can return a Promise. NestJS awaits the promise before using the provider. Common for database connections: `{ provide: 'DB_CONNECTION', useFactory: async () => createConnection() }`.

## Q23: What are custom providers in NestJS?
**A:** Custom providers allow non-standard provider definitions: `useValue` (constants/config), `useClass` (dynamic class selection), `useFactory` (factory functions with DI), and `useExisting` (aliases). They use the same `@Injectable()` and DI system.

## Q24: How do you use environment variables in NestJS?
**A:** Using the `@nestjs/config` package (which wraps dotenv). Install, import `ConfigModule.forRoot()` in the root module, then inject `ConfigService` to access `configService.get('PORT')`. Supports `.env` files, validation, and custom config files.

## Q25: What is the difference between `@Req()` and `@Request()`?
**A:** They are aliases - both inject the Express (or Fastify) request object. Similarly, `@Res()` / `@Response()` inject the response object. Using them in route handlers opts NestJS out of framework-specific response handling for that method.

## Q26: How do you handle file uploads in NestJS?
**A:** Use the built-in `FileInterceptor()` (from `@nestjs/platform-express`) with `@UseInterceptors(FileInterceptor('file'))` and `@UploadedFile() file` parameter. For multiple files: `FilesInterceptor()`. Configure storage options from multer.

## Q27: What is the `@HttpCode()` decorator?
**A:** `@HttpCode(204)` overrides the default HTTP status code for a successful response. Normally NestJS returns 200 for GET, 201 for POST, etc. This decorator allows custom status codes on a per-route basis.

## Q28: What is the `@Redirect()` decorator?
**A:** `@Redirect('url', statusCode)` instructs NestJS to redirect the response. The URL can be a string or a function that returns an object with `url` and `statusCode`. Useful for legacy route migrations and URL shortening services.

## Q29: How do you implement authentication in NestJS?
**A:** Common approach: use `@nestjs/passport` with Passport strategies (JWT, OAuth, local). Create an AuthModule with AuthService, JwtStrategy, and Guards. Protect routes with `@UseGuards(AuthGuard('jwt'))`. JWT tokens are validated in the strategy's validate method.

## Q30: What is Passport.js integration in NestJS?
**A:** `@nestjs/passport` wraps Passport.js as a NestJS module. It provides `AuthGuard()` and passport strategies as injectable providers. NestJS simplifies Passport's callback-based API into a declarative, decorator-based approach.

## Q31: How do you implement JWT authentication in NestJS?
**A:** Install `@nestjs/jwt` and `@nestjs/passport`. Create a JwtStrategy that extends PassportStrategy, configure JWT secret and expiration. The AuthService handles login (validate user, sign JWT). Use `@UseGuards(AuthGuard('jwt'))` to protect routes.

## Q32: What is the `@AuthGuard()` in NestJS?
**A:** `AuthGuard('strategy-name')` is a built-in guard from `@nestjs/passport` that triggers the specified Passport strategy. It validates the request (extracting and verifying tokens) and attaches the user to `req.user` on success.

## Q33: How do you implement role-based authorization in NestJS?
**A:** Create a custom `@Roles('admin')` decorator (using `@SetMetadata()`), then a `RolesGuard` that reads the metadata and checks the user's roles against required roles. Apply `@UseGuards(RolesGuard)` along with the `@Roles()` decorator on controllers or methods.

## Q34: What is the `@SetMetadata()` decorator?
**A:** `@SetMetadata(key, value)` attaches custom metadata to a route handler or class. This metadata can be read by guards, interceptors, or filters at runtime to make decisions (like role-based access control).

## Q35: How do you handle database operations in NestJS?
**A:** NestJS integrates with many ORMs and databases. Common options: TypeORM (SQL), Sequelize (SQL), Mongoose (MongoDB), Prisma, and MikroORM. Each has a dedicated `@nestjs/` package providing module integration and DI support.

## Q36: How does NestJS integrate with TypeORM?
**A:** Install `@nestjs/typeorm` and `typeorm`. Import `TypeOrmModule.forRoot()` in the root module. Use `@InjectRepository(Entity)` and `TypeOrmModule.forFeature([Entity])` in feature modules. Repositories are injectable providers.

## Q37: What is the Repository pattern in NestJS with TypeORM?
**A:** Each entity has a Repository that provides CRUD operations. Inject via `@InjectRepository(Entity) private repo: Repository<Entity>`. The repository abstracts database queries behind an injectable interface, promoting testability and separation of concerns.

## Q38: How does NestJS integrate with Mongoose?
**A:** Install `@nestjs/mongoose` and `mongoose`. Import `MongooseModule.forRoot()` in root module. Define schemas with `@Schema()` decorator, create model classes with `@Prop()` decorators. Inject models with `@InjectModel(Model.name)` in services.

## Q39: How do you perform CRUD operations with Prisma in NestJS?
**A:** Install Prisma CLI and `@prisma/client`. Create a `PrismaService` that extends `PrismaClient` and implements `OnModuleInit` for connection. Inject `PrismaService` into services and use `prisma.user.findMany()`, `prisma.user.create()`, etc.

## Q40: What is the `OnModuleInit` lifecycle hook?
**A:** `OnModuleInit` is a lifecycle interface. When a class implements it (via `implements OnModuleInit`), the `onModuleInit()` method is called after the module's dependencies are resolved. Used for setup tasks like establishing database connections.

## Q41: What lifecycle hooks does NestJS provide?
**A:** `OnModuleInit` (module initialized), `OnApplicationBootstrap` (app fully started), `OnModuleDestroy` (module destruction), `BeforeApplicationShutdown` (shutdown signal received), `OnApplicationShutdown` (connections closed). Implemented from lifecycle interfaces.

## Q42: How do you implement logging in NestJS?
**A:** NestJS provides a built-in `Logger` class. Use `Logger.log()`, `Logger.warn()`, `Logger.error()`. Or create custom loggers implementing `LoggerService`. The `@nestjs/common` Logger can be used in services or as a global interceptor.

## Q43: What is the `@nestjs/common` Logger?
**A:** A built-in logger with methods: `log()`, `warn()`, `error()`, `debug()`, `verbose()`. It respects the NestJS log level setting. Can be injected as `Logger` or used statically. Supports custom context names for identifying log sources.

## Q44: How do you handle CORS in NestJS?
**A:** Enable CORS when creating the NestJS app: `const app = await NestFactory.create(AppModule, { cors: true })`. For fine-grained control, pass a configuration object with `origin`, `methods`, `credentials`, etc.

## Q45: How do you set up global pipes in NestJS?
**A:** `app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))` in the main.ts bootstrap function. This applies validation to all incoming requests across all controllers.

## Q46: What is the WHITELIST option in ValidationPipe?
**A:** `whitelist: true` strips any properties from the incoming DTO that don't have class-validator decorators. `forbidNonWhitelisted: true` throws an error if non-whitelisted properties are present, providing strict request validation.

## Q47: What is the TRANSFORM option in ValidationPipe?
**A:** `transform: true` automatically transforms incoming payloads to their DTO class instances, and performs type conversions (e.g., string "123" to number 123). This allows using TypeScript types and methods on the validated DTO object.

## Q48: How do you implement pagination in NestJS?
**A:** Create a pagination DTO with `@Type(() => Number)` and `@IsOptional()` decorators on `page` and `limit` fields. In the service, use `skip: (page - 1) * limit, take: limit` for database queries. Return data with total count and pagination metadata.

## Q49: How do you handle soft deletes in NestJS?
**A:** With TypeORM, use `@DeleteDateColumn()` decorator (creates `deletedAt` column). Queries with `withDeleted: true` include soft-deleted records, `find()` excludes them by default. Restore with `repository.restore(id)`.

## Q50: What is the `@nestjs/swagger` package?
**A:** It integrates Swagger/OpenAPI documentation generation. Use decorators like `@ApiTags()`, `@ApiOperation()`, `@ApiResponse()`, `@ApiBearerAuth()` on controllers and methods. The SwaggerModule sets up the UI endpoint with `SwaggerModule.setup('api', app, document)`.

## Q51: How do you test NestJS applications?
**A:** Use Jest (built-in) for unit and integration tests. `Test.createTestingModule()` from `@nestjs/testing` creates a testing module with mocked dependencies. Override providers with `overrideProvider().useValue(mock)`. Use Supertest for e2e HTTP tests.

## Q52: What is `Test.createTestingModule()`?
**A:** A NestJS testing utility that creates a module similar to `@Module()` but for testing. It allows importing modules, configuring providers, and overriding dependencies. Returns a `TestingModule` from which controllers/services can be retrieved.

## Q53: How do you create unit tests for a NestJS service?
**A:** Create a testing module: `Test.createTestingModule({ providers: [UserService, { provide: Repository, useValue: mockRepo }] }).compile()`. Get the service instance with `module.get(UserService)`. Test methods with jest assertions.

## Q54: How do you create e2e tests in NestJS?
**A:** Create an `app.e2e-spec.ts` file. Use `Test.createTestingModule({ imports: [AppModule] }).compile()`. Create a `NestExpressApplication` and use `request(app.getHttpServer()).get('/endpoint')` with Supertest for HTTP assertions.

## Q55: What is the `@nestjs/graphql` package?
**A:** It provides GraphQL integration with two approaches: code-first (use decorators on TypeScript classes) and schema-first (write SDL schema manually). Supports Apollo Server and Mercurius. Includes `@Query()`, `@Mutation()`, `@ResolveField()` decorators.

## Q56: What is the difference between code-first and schema-first GraphQL in NestJS?
**A:** Code-first: generate GraphQL schema from TypeScript classes and decorators (`@ObjectType()`, `@Field()`). Schema-first: write SDL files manually and implement resolvers matching the schema. Code-first is preferred for TypeScript projects.

## Q57: How do you implement GraphQL resolvers in NestJS?
**A:** Create a resolver class with `@Resolver(() => User)`. Use `@Query(() => [User])` for queries, `@Mutation(() => User)` for mutations, `@ResolveField()` for field resolvers. Inject services to handle business logic.

## Q58: What is the `@Args()` decorator in GraphQL?
**A:** `@Args()` injects arguments from a GraphQL query/mutation into the resolver method. Can use a dedicated args class with `@ArgsType()` decorator. Supports validation via class-validator and type transformation.

## Q59: How does NestJS support WebSockets?
**A:** Using `@nestjs/websockets` and `@nestjs/platform-socket.io` (or `@nestjs/platform-ws`). Create gateways with `@WebSocketGateway()`. Use `@SubscribeMessage('event')` for event handlers. Gateways can inject services like any other provider.

## Q60: What is a WebSocket Gateway in NestJS?
**A:** A class annotated with `@WebSocketGateway(port, options)` that handles WebSocket connections. It can use lifecycle hooks (`handleConnection`, `handleDisconnect`) and decorators (`@SubscribeMessage`, `@ConnectedSocket`, `@MessageBody`).

## Q61: How do you implement a microservice in NestJS?
**A:** Use `@nestjs/microservices`. Create a microservice app with `app.connectMicroservice({ transport: Transport.TCP, options: { port: 3001 } })`. Use `@MessagePattern({ cmd: 'sum' })` decorators in controllers. Client modules use `ClientProxy` to send messages.

## Q62: What transport layers does NestJS support for microservices?
**A:** TCP (built-in default), Redis (pub/sub), RabbitMQ, Kafka, MQTT, NATS, gRPC, and custom transports. Each has a dedicated microservice module and transport-specific configuration options.

## Q63: What is the difference between `@MessagePattern()` and `@EventPattern()`?
**A:** `@MessagePattern()` expects a response (request-response pattern, like RPC). `@EventPattern()` is fire-and-forget (event-based, no response expected). Both are defined in microservice controllers.

## Q64: How do you handle errors in NestJS microservices?
**A:** Throw `RpcException` in message handlers for Transport.TCP/RMQ/Kafka. For HTTP-based microservices, throw regular HTTP exceptions. The client catches exceptions via `catchError` from RxJS or try-catch with `toPromise()`.

## Q65: What is the `@nestjs/cqrs` package?
**A:** It implements the CQRS (Command Query Responsibility Segregation) pattern. Provides `CommandBus`, `QueryBus`, and `EventBus`. Commands mutate state, queries read state, and events notify of state changes. Each has dedicated handlers.

## Q66: What are Commands in NestJS CQRS?
**A:** Commands represent write operations that change state. A Command is a plain class with properties. Command handlers implement `ICommandHandler<Command>` and are decorated with `@CommandHandler(Command)`. The CommandBus dispatches commands.

## Q67: What are Queries in NestJS CQRS?
**A:** Queries represent read operations that return data without side effects. A Query is a class implementing `IQuery`. Query handlers implement `IQueryHandler<Query>` with `@QueryHandler()`. The QueryBus dispatches queries.

## Q68: What are Events in NestJS CQRS?
**A:** Events represent things that have happened (past tense, like `UserCreatedEvent`). Event handlers implement `IEventHandler<Event>` with `@EventHandler()`. Multiple handlers can handle the same event. Events are published via the EventBus.

## Q69: How do you implement caching in NestJS?
**A:** Use the built-in CacheModule: `CacheModule.register({ ttl: 60, max: 100 })`. Inject `CacheService` to get/set cache. For distributed caching, configure with `store: redisStore` using `cache-manager-redis-store`. Use `@UseInterceptors(CacheInterceptor)` for automatic caching.

## Q70: What is the `CacheInterceptor` in NestJS?
**A:** `CacheInterceptor` automatically caches GET endpoint responses based on the route. Subsequent identical requests return cached data. The cache key is based on the request URL. TTL and cache store are configurable via CacheModule.

## Q71: How do you implement rate limiting in NestJS?
**A:** Use the `@nestjs/throttler` package. Import `ThrottlerModule.forRoot({ limit: 10, ttl: 60 })`. Apply `@Throttle()` decorator or `@UseGuards(ThrottlerGuard)` to controllers/routes. Supports custom limits per route and storage backends.

## Q72: What is the `@nestjs/schedule` package?
**A:** It provides task scheduling capabilities. Use `@Cron('0 * * * *')` for cron jobs, `@Interval(10000)` for interval tasks, and `@Timeout(5000)` for timeout tasks. All are defined in `@Injectable()` classes.

## Q73: How do you use the `@Cron()` decorator?
**A:** `@Cron('0 0 * * *', { name: 'daily-task', timeZone: 'UTC' })` on a method. The cron expression follows standard 6-field format (second, minute, hour, dayOfMonth, month, dayOfWeek). The decorated class must be a provider and use `@Injectable()`.

## Q74: What is the `@nestjs/serve-static` package?
**A:** It serves static files (SPA builds, images) from the NestJS backend. `ServeStaticModule.forRoot({ rootPath: join(__dirname, '..', 'frontend') })`. Useful for deploying full-stack apps as a single unit.

## Q75: How do you implement request lifecycle hooks?
**A:** Implement `OnModuleInit`, `OnApplicationBootstrap`, etc. for app lifecycle. For request lifecycle: Guards run first, then Interceptors (pre-handler), then Pipes, then the route handler, then Interceptors (post-handler), then Exception Filters if errors occur.

## Q76: What is the request lifecycle order in NestJS?
**A:** Incoming request -> Middleware -> Guards -> Interceptors (pre) -> Pipes -> Route Handler -> Interceptors (post) -> Exception Filter (if error) -> Response. Each layer can short-circuit the request.

## Q77: How do you create a custom decorator in NestJS?
**A:** Use `createParamDecorator` from `@nestjs/common`. Example: `export const User = createParamDecorator((data, ctx) => { const request = ctx.switchToHttp().getRequest(); return request.user; })`. Use as `@User()` in route handlers.

## Q78: What is the `@nestjs/passport` `@UseGuards()` for social login?
**A:** Use `@UseGuards(AuthGuard('facebook'))` or `@UseGuards(AuthGuard('google'))` with the corresponding Passport strategies. The guard redirects to the OAuth provider, and the callback URL handles token exchange and user creation.

## Q79: How do you implement a custom Guard in NestJS?
**A:** Create a class implementing `CanActivate`. Implement `canActivate(context)` returning boolean or Promise<boolean>. Use `@Injectable()` decorator. Access request via `context.switchToHttp().getRequest()`. Apply with `@UseGuards(MyGuard)`.

## Q80: How do you implement a custom Pipe in NestJS?
**A:** Create a class implementing `PipeTransform<T, R>` with `transform(value, metadata)` method. Use `@Injectable()`. Can throw `BadRequestException` for invalid values. Apply via `@Body(new MyPipe())` or globally.

## Q81: How do you implement a custom Exception Filter in NestJS?
**A:** Create a class implementing `ExceptionFilter` with `catch(exception, host)` method. Use `@Catch(NotFoundException)` to target specific exceptions. Access response via `host.switchToHttp().getResponse()` for customized error formatting.

## Q82: How do you implement a custom Interceptor in NestJS?
**A:** Create a class implementing `NestInterceptor` with `intercept(context, next)` method. Use `@Injectable()`. Call `next.handle()` and use RxJS `pipe()` with `map()` or `tap()` operators to transform or observe the response stream.

## Q83: How do you handle multiple database connections in NestJS?
**A:** With TypeORM: configure multiple connections in `TypeOrmModule.forRoot()` with different names (defaults to 'default'). Use `@InjectRepository(Entity, 'connectionName')` to specify the connection. Each connection gets its own database configuration.

## Q84: What is the `@nestjs/elasticsearch` package?
**A:** It integrates Elasticsearch with NestJS. Provides `ElasticsearchModule.forRoot({ node: '...' })` and injectable `ElasticsearchService` for search operations. Supports indexing, searching, and aggregation queries with NestJS module patterns.

## Q85: How do you implement WebSocket authentication in NestJS?
**A:** Validate JWT tokens in the gateway's `handleConnection` method. Extract the token from the handshake headers/query. Use a guard or custom logic to disconnect unauthorized clients. Attach user data to the socket instance for later use.

## Q86: What is the `@nestjs/config` package?
**A:** A configuration module that loads environment variables from `.env` files, supports validation with Joi/Zod, and provides a `ConfigService` for typed access. Supports partial registration, namespaced configs, and custom config files.

## Q87: How do you validate environment variables in NestJS?
**A:** Use `ConfigModule.forRoot({ validationSchema: Joi.object({ PORT: Joi.number().default(3000), DB_URL: Joi.string().required() }) })`. Invalid environment variables cause the app to fail to start with clear error messages.

## Q88: What is the `@nestjs/terminus` package?
**A:** Health checks. Provides `HealthController`, `@HealthCheck()`, and health indicators (TypeOrmHealthIndicator, MongooseHealthIndicator, etc.). Exposes a `/health` endpoint that reports the status of configured dependencies.

## Q89: How do you implement graceful shutdown in NestJS?
**A:** Enable shutdown hooks: `app.enableShutdownHooks()`. Implement `OnApplicationShutdown` in services. When Node.js receives SIGTERM, NestJS calls cleanup methods in reverse dependency order. Database connections are closed gracefully.

## Q90: What is the `@nestjs/serializer` package?
**A:** It provides class-serializer integration using `class-transformer`. The `@UseInterceptors(ClassSerializerInterceptor)` transforms response objects based on `@Exclude()` and `@Expose()` decorators on entity/DTO classes.

## Q91: What is the `@nestjs/compiler` package?
**A:** It handles TypeScript compilation for NestJS projects, particularly for standalone builds and monorepo management. It's used internally by the CLI to compile and bundle NestJS applications for production deployment.

## Q92: How do you use DTOs in NestJS?
**A:** DTOs (Data Transfer Objects) are classes that define the shape of request/response data. Used with `@Body()`, `@Query()`, `@Param()`. Decorate fields with class-validator for validation and class-transformer for transformation.

## Q93: What is the `@nestjs/mapped-types` package?
**A:** Provides utility functions to create DTO variants: `PartialType` (makes all fields optional), `PickType` (selects fields), `OmitType` (omits fields), `IntersectionType` (combines types). Works with both validation and Swagger decorators.

## Q94: How do you handle file streaming in NestJS?
**A:** Use `@Res()` to get the response object and pipe a readable stream: `const file = createReadStream(path); file.pipe(res)`. Or use built-in `StreamableFile` class: `return new StreamableFile(fileBuffer)` with `@Header('Content-Type', 'application/pdf')`.

## Q95: What is dynamic module registration in NestJS?
**A:** Modules can have static methods like `forRoot()`, `forFeature()`, `register()` that return `DynamicModule` with configurable providers, imports, and exports. This pattern is used by `TypeOrmModule`, `ConfigModule`, `MongooseModule`, etc.

## Q96: How do you create a dynamic module?
**A:** Create a static method that accepts options and returns `DynamicModule`: `static register(options): DynamicModule`. Use `ConfigurableModuleBuilder` to simplify creation with `@Module()` metadata that includes providers configured from options.

## Q97: What is the difference between `forRoot()` and `forFeature()`?
**A:** `forRoot()` configures a module globally (usually with providers, imports, exports). `forFeature()` configures module-level features (like specific repositories or models). `forRoot()` is called once in the root module; `forFeature()` is called in each feature module.

## Q98: How do you implement transactions in NestJS with TypeORM?
**A:** Use `@Transactional()` decorator from `typeorm-transactional-cls-hooked`. Or use `QueryRunner` directly: inject `DataSource`, create `queryRunner = dataSource.createQueryRunner()`, call `queryRunner.startTransaction()`, execute queries, and commit/rollback.

## Q99: What is the `@nestjs/testing` package?
**A:** Provides utilities for unit and integration testing. Key functions: `Test.createTestingModule()`, `Test.createTestingModule().overrideProvider()`, `Test.createTestingModule().compile()`. Enables creating isolated module instances with mocked dependencies.

## Q100: What are the advantages of using NestJS over Express?
**A:** NestJS provides: modular architecture (modules), dependency injection, built-in support for GraphQL/WebSockets/Microservices, TypeScript-first design, decorator-based routing, integrated validation (pipes), security (guards), request transformation (interceptors), testing utilities, comprehensive documentation, and an opinionated structure that scales well for enterprise applications.
