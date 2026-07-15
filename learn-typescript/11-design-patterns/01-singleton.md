# Singleton Pattern in TypeScript

## Table of Contents

- [What is a Singleton?](#what-is-a-singleton)
- [Implementation Approaches](#implementation-approaches)
- [Private Constructor](#private-constructor)
- [Static Instance](#static-instance)
- [Lazy Initialization](#lazy-initialization)
- [Thread Safety](#thread-safety)
- [Singleton vs Module](#singleton-vs-module)
- [Testing Problems](#testing-problems)
- [Alternatives](#alternatives)
- [When to Use](#when-to-use)
- [Interview Questions](#interview-questions)

---

## What is a Singleton?

A Singleton ensures a class has only one instance and provides a global point of access to it.

```typescript
// Classic use cases:
// - Database connection pool
// - Logger
// - Configuration manager
// - Cache
// - State manager
```

---

## Implementation Approaches

### Basic Singleton

```typescript
class Database {
  private static instance: Database;

  private constructor(private connectionString: string) {
    // Private constructor prevents external instantiation
  }

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database("postgresql://localhost:5432/mydb");
    }
    return Database.instance;
  }

  query(sql: string): unknown[] {
    console.log(`Executing: ${sql}`);
    return [];
  }
}

// Usage
const db1 = Database.getInstance();
const db2 = Database.getInstance();
console.log(db1 === db2); // true

// Cannot do: new Database() // Error: Constructor is private
```

### Singleton with Generics

```typescript
class Singleton<T> {
  private static instances = new Map<Function, Singleton<any>>();

  private constructor(private instance: T) {}

  static getInstance<T>(factory: () => T): Singleton<T> {
    if (!Singleton.instances.has(factory)) {
      Singleton.instances.set(factory, new Singleton(factory()));
    }
    return Singleton.instances.get(factory)! as Singleton<T>;
  }

  get value(): T {
    return this.instance;
  }
}

// Usage
const logger = Singleton.getInstance(() => ({
  log: (msg: string) => console.log(msg),
}));

const config = Singleton.getInstance(() => ({
  apiUrl: "https://api.example.com",
}));

logger.value.log("hello"); // "hello"
```

---

## Private Constructor

```typescript
class Logger {
  private static instance: Logger;
  private logs: string[] = [];

  // Private constructor prevents 'new Logger()'
  private constructor() {}

  static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  log(message: string): void {
    const entry = `[${new Date().toISOString()}] ${message}`;
    this.logs.push(entry);
    console.log(entry);
  }

  getLogs(): readonly string[] {
    return [...this.logs];
  }
}

// TypeScript also allows static class properties
class StrictSingleton {
  private static _instance: StrictSingleton | null = null;

  private constructor() {}

  static get instance(): StrictSingleton {
    if (!StrictSingleton._instance) {
      StrictSingleton._instance = new StrictSingleton();
    }
    return StrictSingleton._instance;
  }

  // Prevent cloning
  private clone(): never {
    throw new Error("Cannot clone a singleton");
  }
}
```

---

## Static Instance

```typescript
// Eager initialization - instance created at class load time
class Config {
  static readonly instance = new Config();

  private constructor() {
    // Load configuration
  }

  get(key: string): string {
    return process.env[key] ?? "";
  }
}

// Usage - no getInstance() needed
const value = Config.instance.get("API_URL");

// Lazy initialization with getter
class LazySingleton {
  private static _instance: LazySingleton | null = null;

  static get instance(): LazySingleton {
    if (!LazySingleton._instance) {
      LazySingleton._instance = new LazySingleton();
    }
    return LazySingleton._instance;
  }

  private constructor() {}
}

// Double-checked locking (TypeScript/JavaScript doesn't need this,
// but useful to know for other languages)
class DCLSingleton {
  private static instance: DCLSingleton | null = null;
  private static initPromise: Promise<DCLSingleton> | null = null;

  static async getInstanceAsync(): Promise<DCLSingleton> {
    if (!DCLSingleton.instance) {
      if (!DCLSingleton.initPromise) {
        DCLSingleton.initPromise = (async () => {
          const instance = new DCLSingleton();
          await instance.initialize();
          return instance;
        })();
      }
      DCLSingleton.instance = await DCLSingleton.initPromise;
    }
    return DCLSingleton.instance;
  }

  private async initialize(): Promise<void> {
    // Expensive initialization
  }

  private constructor() {}
}
```

---

## Lazy Initialization

```typescript
// Lazy singleton with async initialization
class DatabasePool {
  private static instance: DatabasePool | null = null;
  private static initPromise: Promise<DatabasePool> | null = null;

  private pool: Connection[] = [];

  private constructor() {}

  static async getInstance(): Promise<DatabasePool> {
    if (!DatabasePool.instance) {
      if (!DatabasePool.initPromise) {
        DatabasePool.initPromise = (async () => {
          const pool = new DatabasePool();
          await pool.connect();
          return pool;
        })();
      }
      DatabasePool.instance = await DatabasePool.initPromise;
    }
    return DatabasePool.instance;
  }

  private async connect(): Promise<void> {
    console.log("Connecting to database...");
    // Simulate connection setup
    this.pool = Array.from({ length: 5 }, (_, i) => ({
      id: i,
      active: false,
    }) as unknown as Connection);
  }

  getConnection(): Connection {
    const available = this.pool.find((c) => !c.active);
    if (!available) throw new Error("No connections available");
    available.active = true;
    return available;
  }
}

// Module-level lazy singleton (simpler)
class AppConfig {
  private static _instance: AppConfig | null = null;

  readonly apiUrl: string;
  readonly timeout: number;

  private constructor() {
    this.apiUrl = process.env.API_URL ?? "https://api.example.com";
    this.timeout = parseInt(process.env.TIMEOUT ?? "5000");
  }

  static get instance(): AppConfig {
    if (!AppConfig._instance) {
      AppConfig._instance = new AppConfig();
    }
    return AppConfig._instance;
  }
}
```

---

## Thread Safety

```typescript
// JavaScript is single-threaded, so traditional thread safety isn't an issue.
// However, with async initialization, race conditions can occur.

// ❌ Race condition in async singleton
class BadAsyncSingleton {
  private static instance: BadAsyncSingleton | null = null;

  static async getInstance(): Promise<BadAsyncSingleton> {
    if (!BadAsyncSingleton.instance) {
      // If two calls happen simultaneously, both might create an instance
      const instance = new BadAsyncSingleton();
      await instance.init();
      BadAsyncSingleton.instance = instance;
    }
    return BadAsyncSingleton.instance;
  }

  private async init(): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  private constructor() {}
}

// ✅ Safe async singleton
class SafeAsyncSingleton {
  private static instance: SafeAsyncSingleton | null = null;
  private static initPromise: Promise<SafeAsyncSingleton> | null = null;

  static getInstance(): Promise<SafeAsyncSingleton> {
    if (SafeAsyncSingleton.instance) {
      return Promise.resolve(SafeAsyncSingleton.instance);
    }

    if (!SafeAsyncSingleton.initPromise) {
      SafeAsyncSingleton.initPromise = (async () => {
        const instance = new SafeAsyncSingleton();
        await instance.init();
        SafeAsyncSingleton.instance = instance;
        return instance;
      })();
    }

    return SafeAsyncSingleton.initPromise;
  }

  private async init(): Promise<void> {
    await new Promise((resolve) => setTimeout(resolve, 100));
  }

  private constructor() {}
}

// Memoized singleton factory
function createSingleton<T>(factory: () => T): () => T {
  let instance: T | null = null;
  return () => {
    if (instance === null) {
      instance = factory();
    }
    return instance;
  };
}

const getLogger = createSingleton(() => ({
  log: (msg: string) => console.log(`[LOG] ${msg}`),
  error: (msg: string) => console.error(`[ERROR] ${msg}`),
}));

const logger1 = getLogger();
const logger2 = getLogger();
console.log(logger1 === logger2); // true
```

---

## Singleton vs Module

```typescript
// Module-based singleton (often preferred in TypeScript/JavaScript)

// config.ts - Module is naturally a singleton
interface Config {
  apiUrl: string;
  timeout: number;
}

const config: Config = {
  apiUrl: process.env.API_URL ?? "https://api.example.com",
  timeout: parseInt(process.env.TIMEOUT ?? "5000"),
};

export default config;

// logger.ts - Module singleton
class Logger {
  private logs: string[] = [];

  log(message: string): void {
    const entry = `[${new Date().toISOString()}] ${message}`;
    this.logs.push(entry);
    console.log(entry);
  }

  getLogs(): readonly string[] {
    return [...this.logs];
  }
}

export const logger = new Logger();

// Usage
import config from "./config";
import { logger } from "./logger";

console.log(config.apiUrl);
logger.log("Application started");

// Comparison:
// Module singleton: Simpler, naturally lazy, but harder to reset for testing
// Class singleton: More explicit, easier to understand lifecycle, testable
```

---

## Testing Problems

```typescript
// Problem: Singletons make testing difficult

class UserService {
  private static instance: UserService;

  private constructor(private db: Database) {}

  static getInstance(): UserService {
    if (!UserService.instance) {
      UserService.instance = new UserService(Database.getInstance());
    }
    return UserService.instance;
  }

  getUser(id: string): User | null {
    return this.db.query(`SELECT * FROM users WHERE id = '${id}'`)[0] as User;
  }
}

// ❌ Hard to test - can't mock the database
test("getUser returns user", () => {
  const service = UserService.getInstance();
  const user = service.getUser("1");
  expect(user).toBeDefined();
});

// ✅ Better: Dependency Injection (testable)
class TestableUserService {
  constructor(private db: Database) {}

  getUser(id: string): User | null {
    return this.db.query(`SELECT * FROM users WHERE id = '${id}'`)[0] as User;
  }
}

test("getUser returns user", () => {
  const mockDb = { query: () => [{ id: "1", name: "Test User" }] };
  const service = new TestableUserService(mockDb as Database);
  const user = service.getUser("1");
  expect(user?.name).toBe("Test User");
});

// Reset singleton for testing
class ResettableSingleton {
  private static instance: ResettableSingleton | null = null;

  static getInstance(): ResettableSingleton {
    if (!ResettableSingleton.instance) {
      ResettableSingleton.instance = new ResettableSingleton();
    }
    return ResettableSingleton.instance;
  }

  // For testing only
  static resetInstance(): void {
    ResettableSingleton.instance = null;
  }

  private constructor() {}
}
```

---

## Alternatives

```typescript
// 1. Dependency Injection (preferred)
class UserService {
  constructor(private db: Database) {}
}

// 2. Module singleton
export const logger = new Logger();

// 3. Inversion of Control
class Container {
  private services = new Map<string, unknown>();

  register<T>(name: string, instance: T): void {
    this.services.set(name, instance);
  }

  resolve<T>(name: string): T {
    const service = this.services.get(name);
    if (!service) throw new Error(`Service ${name} not found`);
    return service as T;
  }
}

const container = new Container();
container.register("logger", new Logger());
container.register("db", new Database());

const logger = container.resolve<Logger>("logger");

// 4. Factory pattern
function createLogger(): Logger {
  return new Logger();
}
```

---

## When to Use

```typescript
// Use singleton when:
// - You truly need exactly one instance
// - The instance manages shared resources (DB connection, thread pool)
// - You need centralized state (configuration, cache)
// - The lifecycle is simple and long-lived

// Avoid singleton when:
// - You can use dependency injection
// - You need multiple instances for testing
// - The "singleton" state needs to be reset
// - The class has many responsibilities

// Decision checklist:
// ✅ Database connection pool - YES
// ✅ Logger - YES
// ✅ Configuration - YES (but module is simpler)
// ❌ UserService - NO (use DI)
// ❌ ShoppingCart - NO (each user has their own)
// ❌ HTTP Client - NO (usually stateless)
```

---

## Interview Questions

1. **What is the Singleton pattern?**
   A creational pattern that ensures a class has only one instance and provides a global point of access to it.

2. **How do you implement a singleton in TypeScript?**
   Use a private constructor and a static method/property that creates the instance lazily.

3. **What are the problems with singletons?**
   Testing difficulties, hidden dependencies, tight coupling, global state, and lifecycle management.

4. **What is the difference between a singleton and a module?**
   Modules are naturally singletons in JavaScript/TypeScript. They're simpler and don't require the Singleton pattern's ceremony.

5. **How do you make a singleton testable?**
   Use dependency injection, provide a reset method, or use an interface that can be mocked.

6. **When should you NOT use a singleton?**
   When you can use DI, when you need multiple instances, when state needs resetting, or when the class has many responsibilities.

7. **What is lazy initialization in the context of singletons?**
   Creating the instance only when it's first needed, not at class load time.

8. **What is thread safety and why does it matter for singletons?**
   In multi-threaded environments, two threads might simultaneously create instances. JavaScript is single-threaded, but async operations can cause similar issues.

9. **What is the difference between eager and lazy initialization?**
   Eager creates the instance at class load. Lazy creates it on first access. Lazy is more memory-efficient but slightly more complex.

10. **What is the Service Locator pattern?**
    A centralized registry where services register themselves and are looked up by name. Similar to singleton but more flexible.
