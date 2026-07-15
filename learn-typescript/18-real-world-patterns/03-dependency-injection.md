# Dependency Injection in TypeScript

## Table of Contents

- [DI Container with Types](#di-container-with-types)
- [InversifyJS](#inversifyjs)
- [tsyringe](#tsyringe)
- [Typed Service Locator](#typed-service-locator)
- [Constructor Injection](#constructor-injection)
- [Property Injection](#property-injection)
- [DI vs Service Locator](#di-vs-service-locator)
- [DI in NestJS](#di-in-nestjs)
- [Interview Questions](#interview-questions)

---

## DI Container with Types

```typescript
// Simple type-safe DI container
type Constructor<T> = new (...args: any[]) => T;

class Container {
  private services = new Map<string, { factory: () => any; singleton: boolean }>();
  private singletons = new Map<string, any>();

  register<T>(name: string, factory: () => T, singleton: boolean = false): void {
    this.services.set(name, { factory, singleton });
  }

  registerClass<T>(name: string, cls: Constructor<T>, singleton: boolean = false): void {
    this.register(name, () => new cls(), singleton);
  }

  resolve<T>(name: string): T {
    const service = this.services.get(name);
    if (!service) throw new Error(`Service '${name}' not registered`);

    if (service.singleton) {
      if (!this.singletons.has(name)) {
        this.singletons.set(name, service.factory());
      }
      return this.singletons.get(name);
    }

    return service.factory();
  }

  has(name: string): boolean {
    return this.services.has(name);
  }

  clear(): void {
    this.services.clear();
    this.singletons.clear();
  }
}

// Type-safe registration with interfaces
interface Logger {
  log(message: string): void;
  error(message: string): void;
}

interface Database {
  query<T>(sql: string): Promise<T[]>;
  close(): Promise<void>;
}

interface UserService {
  getUser(id: string): Promise<User | null>;
  createUser(data: CreateUserDTO): Promise<User>;
}

// Registration with type assertions
const container = new Container();

container.register<Logger>("logger", () => ({
  log: (msg) => console.log(`[LOG] ${msg}`),
  error: (msg) => console.error(`[ERROR] ${msg}`),
}));

container.register<Database>("database", () => ({
  query: async (sql) => [],
  close: async () => {},
}));

container.register<UserService>("userService", () => ({
  getUser: async (id) => null,
  createUser: async (data) => ({ id: "1", ...data }),
}));

// Resolution with type inference
const logger = container.resolve<Logger>("logger");
const db = container.resolve<Database>("database");
const userService = container.resolve<UserService>("userService");

logger.log("Hello"); // ✅ TypeScript knows this is a Logger
```

---

## InversifyJS

```typescript
import { Container, injectable, inject, interfaces } from "inversify";
import "reflect-metadata";

// Symbols for injection tokens
const TYPES = {
  Logger: Symbol.for("Logger"),
  Database: Symbol.for("Database"),
  UserService: Symbol.for("UserService"),
  UserRepository: Symbol.for("UserRepository"),
};

// Interfaces
interface ILogger {
  log(message: string): void;
}

interface IDatabase {
  query<T>(sql: string): Promise<T[]>;
}

interface IUserRepository {
  findById(id: string): Promise<User | null>;
  create(data: CreateUserDTO): Promise<User>;
}

interface IUserService {
  getUser(id: string): Promise<User | null>;
  createUser(data: CreateUserDTO): Promise<User>;
}

// Implementations
@injectable()
class ConsoleLogger implements ILogger {
  log(message: string): void {
    console.log(`[LOG] ${new Date().toISOString()} ${message}`);
  }
}

@injectable()
class PostgresDatabase implements IDatabase {
  constructor(@inject("connectionString") private connectionString: string) {}

  async query<T>(sql: string): Promise<T[]> {
    // Database query implementation
    return [];
  }
}

@injectable()
class UserRepository implements IUserRepository {
  constructor(@inject(TYPES.Database) private db: IDatabase) {}

  async findById(id: string): Promise<User | null> {
    const results = await this.db.query<User>(
      "SELECT * FROM users WHERE id = $1"
    );
    return results[0] ?? null;
  }

  async create(data: CreateUserDTO): Promise<User> {
    const results = await this.db.query<User>(
      "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *"
    );
    return results[0];
  }
}

@injectable()
class UserService implements IUserService {
  constructor(
    @inject(TYPES.UserRepository) private userRepo: IUserRepository,
    @inject(TYPES.Logger) private logger: ILogger
  ) {}

  async getUser(id: string): Promise<User | null> {
    this.logger.log(`Fetching user ${id}`);
    return this.userRepo.findById(id);
  }

  async createUser(data: CreateUserDTO): Promise<User> {
    this.logger.log(`Creating user ${data.name}`);
    return this.userRepo.create(data);
  }
}

// Container setup
const container = new Container();

container.bind<ILogger>(TYPES.Logger).to(ConsoleLogger).inSingletonScope();
container.bind<IDatabase>(TYPES.Database).to(PostgresDatabase).inSingletonScope();
container.bind<IUserRepository>(TYPES.UserRepository).to(UserRepository);
container.bind<IUserService>(TYPES.UserService).to(UserService);
container.bind<string>("connectionString").toConstantValue(
  "postgresql://localhost:5432/mydb"
);

// Resolution
const userService = container.get<IUserService>(TYPES.UserService);
const user = await userService.getUser("1");
```

---

## tsyringe

```typescript
import "reflect-metadata";
import { container, injectable, inject } from "tsyringe";

// Registration
container.register<Logger>("Logger", { useClass: ConsoleLogger });
container.register<Database>("Database", { useClass: PostgresDatabase });
container.register("connectionString", { useValue: "postgresql://localhost" });

// Injection
@injectable()
class UserService {
  constructor(
    @inject("Logger") private logger: Logger,
    @inject("Database") private db: Database
  ) {}

  async getUser(id: string): Promise<User | null> {
    this.logger.log(`Fetching user ${id}`);
    return this.db.query("SELECT * FROM users WHERE id = ?", [id]);
  }
}

// Resolution
const userService = container.resolve(UserService);
const user = await userService.getUser("1");

// Factory registration
container.registerFactory("UserRepository", (deps) => {
  return new UserRepository(deps.db);
});

// Singleton registration
container.register<Config>("Config", { useClass: Config }, { singleton: true });

// Named registrations
container.register<Cache>("Cache", { useClass: RedisCache }, { name: "redis" });
container.register<Cache>("Cache", { useClass: MemcachedCache }, { name: "memcached" });

const redisCache = container.resolve<Cache>("Cache", { name: "redis" });
```

---

## Typed Service Locator

```typescript
// Service Locator pattern (alternative to DI)
class ServiceLocator {
  private static services = new Map<string, unknown>();

  static register<T>(name: string, service: T): void {
    ServiceLocator.services.set(name, service);
  }

  static resolve<T>(name: string): T {
    const service = ServiceLocator.services.get(name);
    if (!service) throw new Error(`Service '${name}' not found`);
    return service as T;
  }

  static has(name: string): boolean {
    return ServiceLocator.services.has(name);
  }
}

// Type-safe service locator
interface ServiceMap {
  logger: Logger;
  database: Database;
  userService: UserService;
  emailService: EmailService;
}

class TypedServiceLocator {
  private static services = new Map<string, unknown>();

  static register<K extends keyof ServiceMap>(
    name: K,
    service: ServiceMap[K]
  ): void {
    TypedServiceLocator.services.set(name, service);
  }

  static resolve<K extends keyof ServiceMap>(name: K): ServiceMap[K] {
    const service = TypedServiceLocator.services.get(name);
    if (!service) throw new Error(`Service '${name}' not found`);
    return service as ServiceMap[K];
  }
}

// Usage
TypedServiceLocator.register("logger", new ConsoleLogger());
TypedServiceLocator.register("database", new PostgresDatabase());

const logger = TypedServiceLocator.resolve("logger"); // Logger type
const db = TypedServiceLocator.resolve("database"); // Database type
```

---

## Constructor Injection

```typescript
// Most common DI pattern in TypeScript
interface UserServiceDeps {
  logger: Logger;
  database: Database;
  cache: Cache;
}

class UserService {
  private logger: Logger;
  private database: Database;
  private cache: Cache;

  constructor(deps: UserServiceDeps) {
    this.logger = deps.logger;
    this.database = deps.database;
    this.cache = deps.cache;
  }

  async getUser(id: string): Promise<User | null> {
    const cached = await this.cache.get(`user:${id}`);
    if (cached) return cached as User;

    const user = await this.database.query<User>(
      "SELECT * FROM users WHERE id = ?",
      [id]
    );

    if (user) {
      await this.cache.set(`user:${id}`, user, 3600);
    }

    return user[0] ?? null;
  }
}

// Alternative: parameter properties
class UserService2 {
  constructor(
    private logger: Logger,
    private database: Database,
    private cache: Cache
  ) {}

  async getUser(id: string): Promise<User | null> {
    return null;
  }
}

// Factory function with DI
function createUserService(
  logger: Logger,
  database: Database,
  cache: Cache
): UserService {
  return new UserService({ logger, database, cache });
}
```

---

## Property Injection

```typescript
// Less common but useful for optional dependencies
@injectable()
class NotificationService {
  @inject("EmailProvider") emailProvider?: EmailProvider;
  @inject("SMSProvider") smsProvider?: SMSProvider;
  @inject("PushProvider") pushProvider?: PushProvider;

  async notify(user: User, message: string): Promise<void> {
    if (this.emailProvider) {
      await this.emailProvider.send(user.email, message);
    }
    if (this.smsProvider && user.phone) {
      await this.smsProvider.send(user.phone, message);
    }
    if (this.pushProvider && user.pushToken) {
      await this.pushProvider.send(user.pushToken, message);
    }
  }
}

// DI container with property injection
class PropertyContainer {
  private services = new Map<string, unknown>();

  resolve<T>(target: T, properties: Record<string, string>): void {
    for (const [property, serviceName] of Object.entries(properties)) {
      const service = this.services.get(serviceName);
      if (service) {
        (target as any)[property] = service;
      }
    }
  }
}
```

---

## DI vs Service Locator

```typescript
// DI: Dependencies are provided (inverted control)
class UserServiceDI {
  constructor(
    private logger: Logger,  // Provided externally
    private db: Database
  ) {}
}

// Service Locator: Dependencies are fetched (active lookup)
class UserServiceSL {
  private logger = ServiceLocator.resolve<Logger>("logger");
  private db = ServiceLocator.resolve<Database>("database");
}

// DI Advantages:
// - Explicit dependencies (visible in constructor)
// - Easier to test (can inject mocks)
// - Follows Inversion of Control principle
// - Better separation of concerns

// Service Locator Advantages:
// - Less constructor clutter
// - Can resolve dependencies anywhere
// - Easier for legacy code integration

// When to use which:
// DI: New code, testable code, complex dependency graphs
// Service Locator: Legacy integration, simple apps, plugin systems
```

---

## DI in NestJS

```typescript
// NestJS has built-in DI
import { Injectable, Module } from "@nestjs/common";

// Service with DI
@Injectable()
class UserService {
  constructor(
    private readonly database: DatabaseService,
    private readonly logger: LoggerService
  ) {}

  async getUser(id: string): Promise<User | null> {
    this.logger.log(`Fetching user ${id}`);
    return this.database.query("SELECT * FROM users WHERE id = $1", [id]);
  }
}

// Module definition
@Module({
  imports: [DatabaseModule, LoggerModule],
  providers: [UserService],
  exports: [UserService],
})
class UserModule {}

// Custom providers
@Module({
  providers: [
    UserService,
    {
      provide: "EMAIL_SERVICE",
      useClass: process.env.NODE_ENV === "production"
        ? SendGridEmailService
        : MockEmailService,
    },
    {
      provide: "CONFIG",
      useValue: { apiUrl: "https://api.example.com" },
    },
    {
      provide: "DATABASE_URL",
      useFactory: (config: ConfigService) => config.get("DATABASE_URL"),
      inject: [ConfigService],
    },
  ],
})
class AppModule {}
```

---

## Interview Questions

1. **What is Dependency Injection?**
   A design pattern where dependencies are provided to a class rather than created internally. It inverts the control of object creation.

2. **What is the difference between DI and Service Locator?**
   DI provides dependencies (passive). Service Locator fetches dependencies (active). DI is generally preferred for testability.

3. **What are the types of DI?**
   Constructor injection (most common), property injection, and method injection.

4. **How do you implement DI in TypeScript without a framework?**
   Use constructor injection with interfaces and a simple container or factory functions.

5. **What is an IoC container?**
   Inversion of Control container manages object creation and dependency resolution automatically.

6. **What is the difference between singleton and transient scope?**
   Singleton: one instance shared across the app. Transient: new instance each time it's resolved.

7. **How does NestJS DI work?**
   NestJS uses decorators (@Injectable, @Inject) and modules to manage dependencies automatically.

8. **What are the advantages of DI?**
   Loose coupling, testability, flexibility, and adherence to SOLID principles.

9. **What are the disadvantages of DI?**
   Added complexity, learning curve, and potential performance overhead from container resolution.

10. **When should you NOT use DI?**
    Simple applications, when the overhead isn't justified, or when working with simple utility functions.
