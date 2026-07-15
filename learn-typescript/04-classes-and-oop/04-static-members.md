# 04 - Static Members in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [Static Properties](#static-properties)
- [Static Methods](#static-methods)
- [Static Blocks (TypeScript 4.4+)](#static-blocks-typescript-44)
- [Static Factory Methods](#static-factory-methods)
- [Singleton Pattern with Static](#singleton-pattern-with-static)
- [Math Class Example](#math-class-example)
- [Static vs Instance](#static-vs-instance)
- [Static Generic Members](#static-generic-members)
- [Private Static](#private-static)
- [Interview Questions](#interview-questions)

---

## Introduction

Static members belong to the **class itself** rather than to instances of the class. They are shared across all instances and can be accessed without creating an instance. Static members are useful for:

- Class-level data and configuration
- Utility functions related to the class
- Factory methods
- Singleton patterns
- Constants shared across all instances

```typescript
class MyClass {
  static instanceCount = 0;

  constructor() {
    MyClass.instanceCount++;
  }
}

const a = new MyClass();
const b = new MyClass();
console.log(MyClass.instanceCount); // 2
console.log(a.instanceCount);       // undefined — not on instances
```

---

## Static Properties

Static properties are variables declared with the `static` keyword. They belong to the class constructor, not to instances.

### Basic Static Properties

```typescript
class User {
  static totalCount: number = 0;

  constructor(public name: string) {
    User.totalCount++;
  }
}

const alice = new User("Alice");
const bob = new User("Bob");

console.log(User.totalCount); // 2
// alice.totalCount;          // Error: Property 'totalCount' does not exist on type 'User'
```

### Static Configuration

```typescript
class ApiClient {
  static baseUrl: string = "https://api.example.com";
  static timeout: number = 5000;
  static retries: number = 3;

  constructor(private endpoint: string) {}

  getUrl(): string {
    return `${ApiClient.baseUrl}${this.endpoint}`;
  }
}

// Configuration is shared across all instances
const client1 = new ApiClient("/users");
const client2 = new ApiClient("/posts");

console.log(client1.getUrl()); // "https://api.example.com/users"
console.log(client2.getUrl()); // "https://api.example.com/posts"

// Change configuration for all clients
ApiClient.baseUrl = "https://v2.api.example.com";
console.log(client1.getUrl()); // "https://v2.api.example.com/users"
```

### Static Constants

```typescript
class HttpStatus {
  static readonly OK = 200;
  static readonly NOT_FOUND = 404;
  static readonly SERVER_ERROR = 500;
  static readonly UNAUTHORIZED = 401;
  static readonly FORBIDDEN = 403;
}

console.log(HttpStatus.OK);         // 200
// HttpStatus.OK = 201;             // Error: Cannot assign to 'OK' because it is read-only
```

### Static Properties and Inheritance

```typescript
class Base {
  static baseProp = "base";
  static overrideProp = "base";

  static getBaseProp(): string {
    return Base.baseProp;
  }
}

class Child extends Base {
  static overrideProp = "child"; // Shadows Base's static property
}

console.log(Base.baseProp);     // "base"
console.log(Child.baseProp);    // "base" — inherited
console.log(Base.overrideProp); // "base"
console.log(Child.overrideProp); // "child" — overridden
```

### Static Properties on Instances (Not Recommended)

```typescript
class Foo {
  static bar = 42;
}

const foo = new Foo();
console.log(foo.bar); // 42 — TypeScript allows this but it's misleading
// TypeScript doesn't error here, but bar is actually on Foo, not foo
// This works due to how prototype chain works in JavaScript
```

---

## Static Methods

Static methods are functions defined with the `static` keyword. They are called on the class itself, not on instances.

### Basic Static Methods

```typescript
class MathHelper {
  static add(a: number, b: number): number {
    return a + b;
  }

  static subtract(a: number, b: number): number {
    return a - b;
  }

  static multiply(a: number, b: number): number {
    return a * b;
  }

  static clamp(value: number, min: number, max: number): number {
    return Math.min(Math.max(value, min), max);
  }
}

console.log(MathHelper.add(2, 3));         // 5
console.log(MathHelper.clamp(15, 0, 10)); // 10
```

### Static Methods That Create Instances

```typescript
class User {
  constructor(
    public name: string,
    public email: string,
    public role: string
  ) {}

  static createAdmin(name: string, email: string): User {
    return new User(name, email, "admin");
  }

  static createGuest(): User {
    return new User("Guest", "guest@example.com", "guest");
  }

  static fromJSON(json: string): User {
    const data = JSON.parse(json);
    return new User(data.name, data.email, data.role);
  }
}

const admin = User.createAdmin("Alice", "alice@example.com");
const guest = User.createGuest();
const fromStorage = User.fromJSON('{"name":"Bob","email":"bob@test.com","role":"user"}');
```

### Static Methods Cannot Access Instance Members

```typescript
class Example {
  instanceProp = "instance";

  static staticMethod(): string {
    // return this.instanceProp; // Error: 'instanceProp' is an instance member
    return "static";
  }

  instanceMethod(): void {
    console.log(this.instanceProp);      // OK
    console.log(Example.staticMethod());  // OK: accessing static via class name
  }
}
```

### Static Methods and Polymorphism

Static methods do **not** participate in polymorphism. They are resolved at compile time based on the declared type:

```typescript
class Animal {
  static create(): string {
    return "Animal";
  }
}

class Dog extends Animal {
  static create(): string {
    return "Dog";
  }
}

const a: Animal = new Dog(); // Variable is typed as Animal
// Animal.create();          // "Animal" — called based on declared type
// Dog.create();             // "Dog" — called based on Dog type
// a.constructor.create();   // Would use runtime type, but TypeScript doesn't allow this directly
```

### Static Methods with `this` Reference

When a static method uses `this`, `this` refers to the **class constructor**, not an instance:

```typescript
class Counter {
  static count = 0;

  static increment(): typeof Counter {
    Counter.count++;
    return Counter; // Returns the class for chaining
  }

  static reset(): typeof Counter {
    Counter.count = 0;
    return Counter;
  }
}

Counter.increment().increment().increment();
console.log(Counter.count); // 3
```

---

## Static Blocks (TypeScript 4.4+)

Static blocks provide a way to perform complex initialization logic for static properties. They run once when the class is first loaded, similar to static constructors in languages like C# or Java.

### Basic Static Block

```typescript
class DatabaseConfig {
  static connectionPool: ConnectionPool;
  static maxRetries: number;

  static {
    // Complex initialization logic
    console.log("Initializing database config...");

    const host = process.env.DB_HOST ?? "localhost";
    const port = parseInt(process.env.DB_PORT ?? "5432");

    DatabaseConfig.connectionPool = new ConnectionPool(host, port);
    DatabaseConfig.maxRetries = parseInt(process.env.DB_RETRIES ?? "3");
  }
}

// The static block runs when DatabaseConfig is first referenced
```

### Multiple Static Blocks

```typescript
class Config {
  static dbHost: string;
  static dbPort: number;
  static redisUrl: string;

  static {
    console.log("Loading environment variables...");
    Config.dbHost = process.env.DB_HOST ?? "localhost";
    Config.dbPort = parseInt(process.env.DB_PORT ?? "5432");
  }

  static {
    console.log("Loading cache configuration...");
    Config.redisUrl = process.env.REDIS_URL ?? "redis://localhost:6379";
  }
}

// Static blocks execute in order from top to bottom
```

### Static Blocks vs Static Initializers

```typescript
// Static initializer (expression)
class A {
  static value = (() => {
    // Complex IIFE
    return Math.random() * 100;
  })();
}

// Static block (statement block)
class B {
  static value: number;

  static {
    // Can contain statements, try/catch, loops, etc.
    try {
      B.value = JSON.parse(process.env.CONFIG ?? "{}").value;
    } catch {
      B.value = 42;
    }
  }
}
```

### Private Static Members with Static Blocks

```typescript
class PrivateStaticExample {
  private static instanceCount = 0;
  private static readonly instances: PrivateStaticExample[] = [];

  static {
    console.log("PrivateStaticExample class loaded");
  }

  constructor() {
    PrivateStaticExample.instanceCount++;
    PrivateStaticExample.instances.push(this);
  }

  static getStats(): { count: number; instances: PrivateStaticExample[] } {
    return {
      count: PrivateStaticExample.instanceCount,
      instances: [...PrivateStaticExample.instances],
    };
  }
}
```

### Static Blocks and Inheritance

Each class in an inheritance hierarchy has its own static blocks that execute independently:

```typescript
class Base {
  static baseInitialized: boolean;

  static {
    console.log("Base static block");
    Base.baseInitialized = true;
  }
}

class Child extends Base {
  static childInitialized: boolean;

  static {
    console.log("Child static block");
    Child.childInitialized = true;
  }
}

// When Child is loaded:
// 1. Base static block runs first → "Base static block"
// 2. Child static block runs → "Child static block"
console.log(Base.baseInitialized);    // true
console.log(Child.childInitialized); // true
```

---

## Static Factory Methods

Static factory methods are class methods that create and return instances of the class. They provide alternative constructors with descriptive names.

### Named Constructors

```typescript
class Color {
  private constructor(
    public readonly r: number,
    public readonly g: number,
    public readonly b: number,
    public readonly a: number = 1
  ) {}

  static fromRGB(r: number, g: number, b: number): Color {
    return new Color(r, g, b);
  }

  static fromRGBA(r: number, g: number, b: number, a: number): Color {
    return new Color(r, g, b, a);
  }

  static fromHex(hex: string): Color {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!result) {
      throw new Error(`Invalid hex color: ${hex}`);
    }
    return new Color(
      parseInt(result[1], 16),
      parseInt(result[2], 16),
      parseInt(result[3], 16)
    );
  }

  static fromHSL(h: number, s: number, l: number): Color {
    // HSL to RGB conversion
    const rgb = Color.hslToRgb(h, s, l);
    return new Color(rgb.r, rgb.g, rgb.b);
  }

  static readonly WHITE = new Color(255, 255, 255);
  static readonly BLACK = new Color(0, 0, 0);
  static readonly RED = new Color(255, 0, 0);

  private static hslToRgb(h: number, s: number, l: number) {
    // Conversion logic here
    return { r: 0, g: 0, b: 0 };
  }

  toString(): string {
    return `rgba(${this.r}, ${this.g}, ${this.b}, ${this.a})`;
  }
}

// Usage — descriptive factory methods
const red = Color.fromHex("#FF0000");
const blue = Color.fromRGB(0, 0, 255);
const semiTransparent = Color.fromRGBA(0, 255, 0, 0.5);
const predefined = Color.WHITE;
```

### Factory Methods with Validation

```typescript
class PositiveNumber {
  private constructor(public readonly value: number) {}

  static create(value: number): PositiveNumber {
    if (value <= 0) {
      throw new Error(`Expected positive number, got ${value}`);
    }
    return new PositiveNumber(value);
  }

  static tryCreate(value: number): PositiveNumber | null {
    return value > 0 ? new PositiveNumber(value) : null;
  }
}

const price = PositiveNumber.create(9.99);
// const invalid = PositiveNumber.create(-5); // Error: Expected positive number
```

### Factory Methods for Deserialization

```typescript
class User {
  private constructor(
    public readonly id: string,
    public readonly name: string,
    public readonly email: string,
    public readonly createdAt: Date
  ) {}

  static fromDatabase(row: DatabaseRow): User {
    return new User(
      row.id,
      row.name,
      row.email,
      new Date(row.created_at)
    );
  }

  static fromJSON(json: string): User {
    const data = JSON.parse(json);
    return new User(data.id, data.name, data.email, new Date(data.createdAt));
  }

  static fromAPIResponse(response: APIResponse): User {
    return new User(
      response.data.id,
      response.data.attributes.name,
      response.data.attributes.email,
      new Date(response.data.attributes.created_at)
    );
  }
}
```

### Polymorphic Factory Methods

```typescript
abstract class Shape {
  abstract get area(): number;
  abstract get type(): string;

  static create(type: "circle" | "rectangle" | "triangle", ...args: number[]): Shape {
    switch (type) {
      case "circle":
        return new CircleImpl(args[0]);
      case "rectangle":
        return new RectangleImpl(args[0], args[1]);
      case "triangle":
        return new TriangleImpl(args[0], args[1], args[2]);
      default:
        throw new Error(`Unknown shape type: ${type}`);
    }
  }
}
```

---

## Singleton Pattern with Static

The singleton pattern ensures that only one instance of a class exists. Static members are essential for implementing singletons in TypeScript.

### Basic Singleton

```typescript
class Singleton {
  private static instance: Singleton;

  private constructor(public value: string) {}

  static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton("initialized");
    }
    return Singleton.instance;
  }
}

const a = Singleton.getInstance();
const b = Singleton.getInstance();
console.log(a === b); // true — same instance
```

### Singleton with Lazy Initialization

```typescript
class Configuration {
  private static instance: Configuration | null = null;

  private settings: Map<string, any> = new Map();

  private constructor() {
    this.loadDefaults();
  }

  static getInstance(): Configuration {
    if (Configuration.instance === null) {
      Configuration.instance = new Configuration();
    }
    return Configuration.instance;
  }

  private loadDefaults(): void {
    this.settings.set("debug", false);
    this.settings.set("logLevel", "info");
    this.settings.set("maxRetries", 3);
  }

  get<T>(key: string): T {
    return this.settings.get(key) as T;
  }

  set(key: string, value: any): void {
    this.settings.set(key, value);
  }
}

// Usage
const config = Configuration.getInstance();
config.set("debug", true);
console.log(Configuration.getInstance().get("debug")); // true
```

### Thread-Safe Singleton (for Async Contexts)

```typescript
class Database {
  private static instance: Database | null = null;
  private static initPromise: Promise<Database> | null = null;

  private constructor(private connection: any) {}

  static async getInstance(): Promise<Database> {
    if (Database.instance) {
      return Database.instance;
    }

    if (Database.initPromise) {
      return Database.initPromise;
    }

    Database.initPromise = (async () => {
      const connection = await Database.createConnection();
      Database.instance = new Database(connection);
      return Database.instance;
    })();

    return Database.initPromise;
  }

  private static async createConnection(): Promise<any> {
    // Simulate async initialization
    return { host: "localhost", port: 5432 };
  }
}
```

### Singleton Anti-Pattern Warning

```typescript
// Anti-pattern: Global mutable state makes testing difficult
class GlobalState {
  private static instance: GlobalState;
  public data: any = {};

  static getInstance(): GlobalState {
    if (!GlobalState.instance) {
      GlobalState.instance = new GlobalState();
    }
    return GlobalState.instance;
  }
}

// Better: Use dependency injection
class AppState {
  constructor(public data: Record<string, any> = {}) {}
}

function createService(state: AppState) {
  // Depends on injected state, not global singleton
  return { getState: () => state };
}
```

---

## Math Class Example

The JavaScript `Math` class is a perfect example of a utility class with only static members. Let's look at how you'd create something similar in TypeScript.

### Utility Class Pattern

```typescript
class MathUtils {
  // Prevent instantiation
  private constructor() {}

  static readonly PI = Math.PI;
  static readonly E = Math.E;

  static abs(x: number): number {
    return Math.abs(x);
  }

  static max(...values: number[]): number {
    return Math.max(...values);
  }

  static min(...values: number[]): number {
    return Math.min(...values);
  }

  static clamp(value: number, min: number, max: number): number {
    return MathUtils.min(MathUtils.max(value, min), max);
  }

  static lerp(start: number, end: number, t: number): number {
    return start + (end - start) * t;
  }

  static degToRad(degrees: number): number {
    return degrees * (Math.PI / 180);
  }

  static radToDeg(radians: number): number {
    return radians * (180 / Math.PI);
  }

  static randomInt(min: number, max: number): number {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  static randomFloat(min: number, max: number): number {
    return Math.random() * (max - min) + min;
  }

  static average(...values: number[]): number {
    if (values.length === 0) return 0;
    return values.reduce((a, b) => a + b, 0) / values.length;
  }

  static median(...values: number[]): number {
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 !== 0
      ? sorted[mid]
      : (sorted[mid - 1] + sorted[mid]) / 2;
  }

  static standardDeviation(...values: number[]): number {
    const avg = MathUtils.average(...values);
    const squareDiffs = values.map(v => Math.pow(v - avg, 2));
    const avgSquareDiff = MathUtils.average(...squareDiffs);
    return Math.sqrt(avgSquareDiff);
  }
}

// Usage
console.log(MathUtils.PI);                    // 3.14159...
console.log(MathUtils.clamp(15, 0, 10));     // 10
console.log(MathUtils.lerp(0, 100, 0.5));    // 50
console.log(MathUtils.average(1, 2, 3, 4)); // 2.5
console.log(MathUtils.median(1, 3, 5));     // 3
```

### Generic Math Utilities

```typescript
class ArrayUtils {
  private constructor() {}

  static chunk<T>(array: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }

  static unique<T>(array: T[]): T[] {
    return [...new Set(array)];
  }

  static groupBy<T, K extends string | number>(
    array: T[],
    keyFn: (item: T) => K
  ): Record<K, T[]> {
    return array.reduce((groups, item) => {
      const key = keyFn(item);
      groups[key] = groups[key] || [];
      groups[key].push(item);
      return groups;
    }, {} as Record<K, T[]>);
  }

  static flatten<T>(array: T[][]): T[] {
    return array.reduce((acc, curr) => acc.concat(curr), []);
  }

  static sortBy<T>(array: T[], keyFn: (item: T) => number | string): T[] {
    return [...array].sort((a, b) => {
      const aKey = keyFn(a);
      const bKey = keyFn(b);
      if (aKey < bKey) return -1;
      if (aKey > bKey) return 1;
      return 0;
    });
  }
}
```

---

## Static vs Instance

Understanding when to use static vs instance members is crucial for good class design.

### When to Use Static

- **Utility functions** that don't need instance state
- **Factory methods** with descriptive names
- **Constants** shared across all instances
- **Singleton access** (getInstance)
- **Class-level tracking** (instance counts, registries)

### When to Use Instance

- **State** that varies per object
- **Behavior** that depends on instance data
- **Methods** that modify instance state
- **Configuration** that's specific to an instance

### Comparison Table

| Feature | Static | Instance |
|---|---|---|
| Accessed via | `ClassName.member` | `instance.member` |
| Shared | Yes (class-level) | No (per-instance) |
| `this` refers to | Class constructor | Instance |
| Polymorphism | No (compile-time) | Yes (runtime) |
| Memory | One copy | One per instance |
| Inheritance | Inherited but not overridden in JS prototypes | Overridden via prototype chain |

### Complete Example

```typescript
class Employee {
  // Static: shared across all employees
  static company = "TechCorp";
  static employeeCount = 0;
  private static readonly allEmployees: Employee[] = [];

  static getAverageSalary(): number {
    const total = Employee.allEmployees.reduce((sum, emp) => sum + emp.salary, 0);
    return total / Employee.allEmployees.length;
  }

  static findById(id: string): Employee | undefined {
    return Employee.allEmployees.find(emp => emp.id === id);
  }

  // Instance: unique per employee
  id: string;
  name: string;
  private _salary: number;

  constructor(name: string, salary: number) {
    this.id = `EMP-${Employee.employeeCount++}`;
    this.name = name;
    this._salary = salary;
    Employee.allEmployees.push(this);
  }

  get salary(): number {
    return this._salary;
  }

  giveRaise(percentage: number): void {
    this._salary *= 1 + percentage / 100;
  }

  getInfo(): string {
    return `${this.name} (${this.id}) - $${this._salary.toLocaleString()} at ${Employee.company}`;
  }
}
```

---

## Static Generic Members

TypeScript supports generic static methods, but not generic static properties (since properties must have a single type, not a family of types).

### Static Generic Methods

```typescript
class Serializer {
  static serialize<T>(data: T): string {
    return JSON.stringify(data);
  }

  static deserialize<T>(json: string): T {
    return JSON.parse(json) as T;
  }

  static deepClone<T>(obj: T): T {
    return JSON.parse(JSON.stringify(obj));
  }

  static pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
    const result = {} as Pick<T, K>;
    for (const key of keys) {
      result[key] = obj[key];
    }
    return result;
  }
}

interface User {
  name: string;
  email: string;
  age: number;
}

const user: User = { name: "Alice", email: "alice@test.com", age: 30 };
const cloned = Serializer.deepClone(user);
const partial = Serializer.pick(user, ["name", "email"]);
```

### Static Generic Factory

```typescript
class Factory {
  static create<T>(Constructor: new (...args: any[]) => T, ...args: any[]): T {
    return new Constructor(...args);
  }

  static createArray<T>(Constructor: new (...args: any[]) => T, count: number, ...args: any[]): T[] {
    return Array.from({ length: count }, () => new Constructor(...args));
  }
}

class Box {
  constructor(public value: number) {}
}

const boxes = Factory.createArray(Box, 5, 42);
console.log(boxes.length); // 5
console.log(boxes[0].value); // 42
```

---

## Private Static

Private static members are accessible only within the class itself. They are useful for implementation details that should not be exposed.

### Basic Private Static

```typescript
class TokenManager {
  private static tokenStore: Map<string, string> = new Map();
  private static readonly EXPIRY_MS = 3600000; // 1 hour

  static generateToken(userId: string): string {
    const token = TokenManager.generateRandomString(32);
    TokenManager.tokenStore.set(token, userId);
    return token;
  }

  static validateToken(token: string): string | null {
    const userId = TokenManager.tokenStore.get(token);
    return userId ?? null;
  }

  static revokeToken(token: string): boolean {
    return TokenManager.tokenStore.delete(token);
  }

  private static generateRandomString(length: number): string {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let result = "";
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  }
}

const token = TokenManager.generateToken("user123");
console.log(TokenManager.validateToken(token)); // "user123"
// TokenManager.generateRandomString(10); // Error: Property 'generateRandomString' is private
```

### Private Static Registry Pattern

```typescript
class ServiceRegistry {
  private static services: Map<string, any> = new Map();
  private static middleware: Array<(service: any) => any> = [];

  static register<T>(name: string, service: T): void {
    let instance = service;
    for (const mw of ServiceRegistry.middleware) {
      instance = mw(instance);
    }
    ServiceRegistry.services.set(name, instance);
  }

  static get<T>(name: string): T {
    const service = ServiceRegistry.services.get(name);
    if (!service) {
      throw new Error(`Service '${name}' not found`);
    }
    return service as T;
  }

  static addMiddleware(middleware: (service: any) => any): void {
    ServiceRegistry.middleware.push(middleware);
  }

  private static clearAll(): void {
    ServiceRegistry.services.clear();
    ServiceRegistry.middleware = [];
  }
}
```

---

## Interview Questions

### Q1: What is the difference between static and instance members?

**Answer:** Static members belong to the class itself and are shared across all instances. Instance members belong to individual objects created from the class. Static members are accessed via `ClassName.member`, while instance members are accessed via `instance.member`.

### Q2: Can static methods be overridden?

**Answer:** In TypeScript/JavaScript, static methods are not overridden in the OOP sense. If a subclass defines a static method with the same name, it **shadows** the parent's method. However, calling the method via the parent class name will call the parent's version (no runtime polymorphism for statics).

### Q3: What are static blocks?

**Answer:** Static blocks (introduced in TypeScript 4.4) are code blocks that execute once when the class is first loaded. They are useful for complex initialization of static properties, including try/catch, loops, and conditional logic. Multiple static blocks execute in order from top to bottom.

### Q4: When should you use a static factory method instead of a constructor?

**Answer:** Use static factory methods when: (1) you need descriptive names (`Color.fromHex()` is clearer than `new Color(...)`), (2) you want to return cached instances, (3) you want to return subtypes, (4) you need to perform validation before construction, or (5) you want to control whether to create a new object or return an existing one.

### Q5: Can a class have both static and instance members?

**Answer:** Yes. A class can have both static and instance members. Static members are shared across all instances, while instance members are unique to each object. Common patterns include utility methods (static) and data/behavior (instance).

### Q6: Why would you make a constructor private?

**Answer:** A private constructor prevents direct instantiation from outside the class. This is useful for: (1) singleton pattern (enforcing single instance), (2) factory methods that control how instances are created, (3) preventing instantiation of abstract or utility classes.

---

**Next:** [05 - Inheritance](./05-inheritance.md)
