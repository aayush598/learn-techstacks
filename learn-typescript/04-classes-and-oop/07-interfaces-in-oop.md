# 07 - Interfaces in OOP

## Table of Contents

- [Introduction](#introduction)
- [The implements Keyword](#the-implements-keyword)
- [Multiple Interface Implementation](#multiple-interface-implementation)
- [Interface vs Abstract Class](#interface-vs-abstract-class)
- [Contract Enforcement](#contract-enforcement)
- [Dependency Inversion with Interfaces](#dependency-inversion-with-interfaces)
- [Interface Segregation](#interface-segregation)
- [Coding to Interfaces](#coding-to-interfaces)
- [Interview Questions](#interview-questions)

---

## Introduction

Interfaces in TypeScript define the shape of an object — the types of properties and methods it must have. In OOP, interfaces serve as **contracts** that classes must fulfill. They enable polymorphism, loose coupling, and are fundamental to writing testable, maintainable code.

---

## The implements Keyword

The `implements` keyword ensures a class satisfies an interface's contract.

### Basic Implementation

```typescript
interface Printable {
  toString(): string;
  print(): void;
}

interface Loggable {
  log(message: string): void;
}

class Document implements Printable, Loggable {
  constructor(public title: string, public content: string) {}

  toString(): string {
    return `${this.title}: ${this.content}`;
  }

  print(): void {
    console.log(this.toString());
  }

  log(message: string): void {
    console.log(`[Document: ${this.title}] ${message}`);
  }
}
```

### Interface with Properties

```typescript
interface UserInterface {
  id: string;
  name: string;
  email: string;
  readonly createdAt: Date;
}

class User implements UserInterface {
  readonly createdAt: Date = new Date();

  constructor(
    public id: string,
    public name: string,
    public email: string
  ) {}
}
```

### Interface with Optional Members

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
  metadata?: {
    page?: number;
    totalPages?: number;
    totalItems?: number;
  };
}

class SuccessResponse<T> implements ApiResponse<T> {
  metadata: { page: number; totalPages: number; totalItems: number };

  constructor(
    public data: T,
    public status: number = 200,
    public message?: string
  ) {
    this.metadata = { page: 1, totalPages: 1, totalItems: 1 };
  }
}
```

### Partial Implementation Error

If a class does not implement all required members, TypeScript raises an error:

```typescript
interface Calculator {
  add(a: number, b: number): number;
  subtract(a: number, b: number): number;
}

// Error: Class 'BasicCalc' incorrectly implements interface 'Calculator'
class BasicCalc implements Calculator {
  add(a: number, b: number): number {
    return a + b;
  }
  // Missing: subtract method
}
```

---

## Multiple Interface Implementation

A class can implement multiple interfaces simultaneously, combining multiple contracts.

```typescript
interface Serializable {
  serialize(): string;
}

interface Identifiable {
  readonly id: string;
}

interface Validatable {
  validate(): boolean;
  getErrors(): string[];
}

class UserModel implements Serializable, Identifiable, Validatable {
  private errors: string[] = [];

  constructor(
    public readonly id: string,
    public name: string,
    public email: string
  ) {}

  serialize(): string {
    return JSON.stringify({
      id: this.id,
      name: this.name,
      email: this.email,
    });
  }

  validate(): boolean {
    this.errors = [];
    if (!this.name || this.name.trim().length === 0) {
      this.errors.push("Name is required");
    }
    if (!this.email || !this.email.includes("@")) {
      this.errors.push("Valid email is required");
    }
    return this.errors.length === 0;
  }

  getErrors(): string[] {
    return [...this.errors];
  }
}
```

### Interface Inheritance Chains

```typescript
interface HasId {
  readonly id: string;
}

interface HasTimestamp extends HasId {
  readonly createdAt: Date;
  readonly updatedAt: Date;
}

interface SoftDeletable extends HasTimestamp {
  readonly deletedAt: Date | null;
  isDeleted(): boolean;
}

class BaseEntity implements SoftDeletable {
  deletedAt: Date | null = null;

  constructor(
    public readonly id: string,
    public readonly createdAt: Date,
    public readonly updatedAt: Date
  ) {}

  isDeleted(): boolean {
    return this.deletedAt !== null;
  }
}
```

---

## Interface vs Abstract Class

| Feature | Interface | Abstract Class |
|---|---|---|
| Method implementations | No | Yes |
| Constructor | No | Yes |
| Properties with values | No | Yes |
| Multiple inheritance | Yes | No |
| Access modifiers | No | Yes |
| Runtime existence | No (erased) | Yes |
| Performance overhead | None | Minimal |
| Use case | Pure contract | Shared implementation + contract |

### Decision Guide

```typescript
// Use INTERFACE when:
// - Defining a contract that unrelated classes implement
// - You need multiple inheritance
// - No shared implementation needed

interface Repository<T> {
  findById(id: string): T | undefined;
  save(item: T): void;
  delete(id: string): boolean;
}

// Use ABSTRACT CLASS when:
// - Related classes share common implementation
// - You need constructors or access modifiers
// - You want to provide default behavior

abstract class BaseRepository<T> implements Repository<T> {
  protected items: Map<string, T> = new Map();

  findById(id: string): T | undefined {
    return this.items.get(id);
  }

  save(item: T): void {
    this.items.set((item as any).id, item);
  }

  delete(id: string): boolean {
    return this.items.delete(id);
  }
}
```

### Interface for Testing

Interfaces are invaluable for mocking in tests:

```typescript
interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class NotificationService {
  constructor(private emailService: EmailService) {}

  async sendWelcome(email: string): Promise<void> {
    await this.emailService.send(email, "Welcome!", "Thanks for signing up.");
  }
}

// In production
class SMTPEmailService implements EmailService {
  async send(to: string, subject: string, body: string): Promise<void> {
    // Real SMTP implementation
  }
}

// In tests
class MockEmailService implements EmailService {
  sentEmails: Array<{ to: string; subject: string; body: string }> = [];

  async send(to: string, subject: string, body: string): Promise<void> {
    this.sentEmails.push({ to, subject, body });
  }
}
```

---

## Contract Enforcement

Interfaces enforce that classes adhere to a defined shape. This is critical for large codebases.

### Runtime Shape Enforcement (Type Guard)

```typescript
interface Point {
  x: number;
  y: number;
}

function isPoint(obj: unknown): obj is Point {
  return (
    typeof obj === "object" &&
    obj !== null &&
    "x" in obj &&
    "y" in obj &&
    typeof (obj as Point).x === "number" &&
    typeof (obj as Point).y === "number"
  );
}

function processPoint(input: unknown): void {
  if (isPoint(input)) {
    console.log(`Point: ${input.x}, ${input.y}`);
  } else {
    console.log("Invalid point");
  }
}
```

### Compile-Time Contract Enforcement

```typescript
interface PaymentProcessor {
  charge(amount: number, currency: string): Promise<PaymentResult>;
  refund(transactionId: string): Promise<RefundResult>;
  getBalance(): Promise<number>;
}

interface PaymentResult {
  success: boolean;
  transactionId: string;
}

interface RefundResult {
  success: boolean;
  refundId: string;
}

class StripeProcessor implements PaymentProcessor {
  async charge(amount: number, currency: string): Promise<PaymentResult> {
    // Stripe-specific logic
    return { success: true, transactionId: "stripe_" + Date.now() };
  }

  async refund(transactionId: string): Promise<RefundResult> {
    return { success: true, refundId: "ref_" + Date.now() };
  }

  async getBalance(): Promise<number> {
    return 10000;
  }
}

class PayPalProcessor implements PaymentProcessor {
  async charge(amount: number, currency: string): Promise<PaymentResult> {
    // PayPal-specific logic
    return { success: true, transactionId: "paypal_" + Date.now() };
  }

  async refund(transactionId: string): Promise<RefundResult> {
    return { success: true, refundId: "pp_ref_" + Date.now() };
  }

  async getBalance(): Promise<number> {
    return 8500;
  }
}
```

---

## Dependency Inversion with Interfaces

The Dependency Inversion Principle (DIP) states that high-level modules should not depend on low-level modules. Both should depend on abstractions (interfaces).

### Without DIP (Bad)

```typescript
class MySQLDatabase {
  query(sql: string): any[] {
    return [];
  }
}

class UserService {
  private db = new MySQLDatabase(); // Tightly coupled!

  getUsers() {
    return this.db.query("SELECT * FROM users");
  }
}
```

### With DIP (Good)

```typescript
interface Database {
  query<T>(sql: string): Promise<T[]>;
  execute(sql: string): Promise<void>;
}

class UserService {
  constructor(private db: Database) {} // Depends on abstraction

  async getUsers() {
    return this.db.query<{ id: string; name: string }>("SELECT * FROM users");
  }
}

class MySQLDatabase implements Database {
  async query<T>(sql: string): Promise<T[]> {
    // MySQL implementation
    return [];
  }

  async execute(sql: string): Promise<void> {
    // MySQL implementation
  }
}

class PostgreSQLDatabase implements Database {
  async query<T>(sql: string): Promise<T[]> {
    // PostgreSQL implementation
    return [];
  }

  async execute(sql: string): Promise<void> {
    // PostgreSQL implementation
  }
}

class InMemoryDatabase implements Database {
  private data = new Map<string, any[]>();

  async query<T>(sql: string): Promise<T[]> {
    // In-memory for testing
    return [];
  }

  async execute(sql: string): Promise<void> {
    // In-memory for testing
  }
}
```

### Constructor Injection Pattern

```typescript
interface Logger {
  info(message: string): void;
  error(message: string): void;
  warn(message: string): void;
}

interface Cache {
  get<T>(key: string): T | undefined;
  set<T>(key: string, value: T, ttl?: number): void;
  delete(key: string): void;
}

interface Config {
  get<T>(key: string): T;
}

class Application {
  constructor(
    private logger: Logger,
    private cache: Cache,
    private config: Config
  ) {}

  start(): void {
    this.logger.info("Application starting...");
    const port = this.config.get<number>("port");
    this.logger.info(`Listening on port ${port}`);
  }
}
```

---

## Interface Segregation

The Interface Segregation Principle (ISP) states that no client should be forced to depend on methods it does not use.

### Bad: Fat Interface

```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
  writeCode(): void;
}

// Robot doesn't eat or sleep
class Robot implements Worker {
  work(): void { /* ... */ }
  eat(): void { throw new Error("Robots don't eat"); }     // Forced!
  sleep(): void { throw new Error("Robots don't sleep"); }  // Forced!
  attendMeeting(): void { throw new Error("Robots don't attend meetings"); }
  writeCode(): void { /* ... */ }
}
```

### Good: Segregated Interfaces

```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface MeetingAttendee {
  attendMeeting(): void;
}

interface Coder {
  writeCode(): void;
}

// Human worker — implements all
class HumanWorker implements Workable, Eatable, Sleepable, MeetingAttendee, Coder {
  work(): void { console.log("Working..."); }
  eat(): void { console.log("Eating..."); }
  sleep(): void { console.log("Sleeping..."); }
  attendMeeting(): void { console.log("In meeting..."); }
  writeCode(): void { console.log("Coding..."); }
}

// Robot — only what it needs
class RobotWorker implements Workable, Coder {
  work(): void { console.log("Working..."); }
  writeCode(): void { console.log("Coding..."); }
}
```

### Real-World ISP Example

```typescript
// Segregated interfaces
interface Readable<T> {
  read(id: string): Promise<T | null>;
  list(): Promise<T[]>;
}

interface Writable<T> {
  create(item: Omit<T, "id">): Promise<T>;
  update(id: string, item: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
}

interface Searchable<T> {
  search(query: string): Promise<T[]>;
}

interface Cacheable<T> {
  cache(id: string, item: T, ttl?: number): void;
  getCached(id: string): T | undefined;
  invalidateCache(id: string): void;
}

// Read-only repository
class ConfigRepository implements Readable<Config> {
  async read(id: string): Promise<Config | null> { return null; }
  async list(): Promise<Config[]> { return []; }
}

// Full CRUD repository
class UserRepository implements Readable<User>, Writable<User>, Searchable<User> {
  async read(id: string): Promise<User | null> { return null; }
  async list(): Promise<User[]> { return []; }
  async create(item: Omit<User, "id">): Promise<User> { return item as User; }
  async update(id: string, item: Partial<User>): Promise<User> { return item as User; }
  async delete(id: string): Promise<boolean> { return true; }
  async search(query: string): Promise<User[]> { return []; }
}
```

---

## Coding to Interfaces

"Coding to interfaces" means designing your code to depend on interface types rather than concrete implementations.

### Basic Principle

```typescript
// BAD: Depends on concrete type
function processUser(user: User) {
  console.log(user.name);
}

// GOOD: Depends on interface
interface HasName {
  name: string;
}

function processNamed(entity: HasName) {
  console.log(entity.name);
}

// Any object with a 'name' property works
processNamed({ name: "Alice" });
processNamed(new User("1", "Alice", "alice@test.com"));
processNamed({ name: "Bob", age: 30 }); // Extra properties are fine
```

### Service Layer Pattern

```typescript
// Interfaces define the contract
interface UserService {
  getUser(id: string): Promise<User | null>;
  createUser(data: CreateUserDTO): Promise<User>;
  updateUser(id: string, data: Partial<User>): Promise<User>;
  deleteUser(id: string): Promise<boolean>;
}

interface NotificationService {
  send(to: string, message: string): Promise<void>;
}

interface LoggerService {
  info(message: string): void;
  error(message: string, error?: Error): void;
}

// Controller depends only on interfaces
class UserController {
  constructor(
    private userService: UserService,
    private notificationService: NotificationService,
    private logger: LoggerService
  ) {}

  async handleCreateUser(data: CreateUserDTO) {
    try {
      const user = await this.userService.createUser(data);
      await this.notificationService.send(user.email, "Welcome!");
      return { status: 201, data: user };
    } catch (error) {
      this.logger.error("Failed to create user", error as Error);
      return { status: 500, error: "Internal server error" };
    }
  }
}
```

### Strategy Pattern with Interfaces

```typescript
interface CompressionStrategy {
  compress(data: Buffer): Buffer;
  readonly name: string;
}

class ZipCompression implements CompressionStrategy {
  readonly name = "zip";
  compress(data: Buffer): Buffer {
    console.log("Compressing with ZIP...");
    return data; // simplified
  }
}

class GzipCompression implements CompressionStrategy {
  readonly name = "gzip";
  compress(data: Buffer): Buffer {
    console.log("Compressing with GZIP...");
    return data; // simplified
  }
}

class NoCompression implements CompressionStrategy {
  readonly name = "none";
  compress(data: Buffer): Buffer {
    return data;
  }
}

class FileProcessor {
  private strategy: CompressionStrategy;

  constructor(strategy: CompressionStrategy) {
    this.strategy = strategy;
  }

  setStrategy(strategy: CompressionStrategy): void {
    this.strategy = strategy;
  }

  async processFile(filePath: string): Promise<void> {
    console.log(`Processing ${filePath} with ${this.strategy.name}`);
    // Read, compress, write...
  }
}
```

---

## Interview Questions

### Q1: What is the purpose of the `implements` keyword?

**Answer:** The `implements` keyword ensures a class satisfies the contract defined by an interface. If the class doesn't implement all required members, TypeScript raises a compile error.

### Q2: Can a class implement multiple interfaces?

**Answer:** Yes. A class can implement any number of interfaces, separating concerns into focused contracts. This is TypeScript's way of achieving multiple type inheritance: `class MyClass implements InterfaceA, InterfaceB, InterfaceC {}`.

### Q3: What is the Interface Segregation Principle?

**Answer:** ISP states that no client should be forced to depend on methods it does not use. Instead of one large interface, create multiple small, focused interfaces. Classes then implement only the interfaces relevant to them.

### Q4: How do interfaces support Dependency Inversion?

**Answer:** High-level modules depend on interface abstractions rather than concrete implementations. This allows swapping implementations (e.g., MySQL to PostgreSQL) without changing the high-level code. Dependency injection frameworks often use interfaces to decouple components.

### Q5: What is "coding to interfaces"?

**Answer:** Designing code to depend on interface types rather than concrete classes. Function parameters, return types, and class dependencies use interface types, enabling loose coupling and easy testing through mocks.

### Q6: When should you prefer an interface over an abstract class?

**Answer:** When you need multiple inheritance of type, when no shared implementation is needed, when you want maximum flexibility for mocking/testing, or when the contract might be implemented by unrelated classes.

---

**Next:** [08 - Polymorphism](./08-polymorphism.md)
