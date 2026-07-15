# 02 - Access Modifiers in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [The `public` Keyword](#the-public-keyword)
- [The `private` Keyword](#the-private-keyword)
- [The `protected` Keyword](#the-protected-keyword)
- [Parameter Property Modifiers](#parameter-property-modifiers)
- [Private Fields vs `#` (ECMAScript Private Fields)](#private-fields-vs-ecmascript-private-fields)
- [Protected and Inheritance](#protected-and-inheritance)
- [Accessor Visibility](#accessor-visibility)
- [Default Visibility](#default-visibility)
- [Access Modifier Best Practices](#access-modifier-best-practices)
- [Encapsulation Principles](#encapsulation-principles)
- [Interview Questions](#interview-questions)

---

## Introduction

Access modifiers are keywords that control the visibility and accessibility of class members (properties and methods). They are a cornerstone of encapsulation — one of the four pillars of object-oriented programming. TypeScript provides three access modifiers: `public`, `private`, and `protected`.

TypeScript's access modifiers are enforced **only at compile time**. At runtime, JavaScript does not have native access modifiers (until ECMAScript's `#` private fields), so all properties and methods are technically accessible. This is an important distinction for understanding the boundaries of TypeScript's type system.

---

## The `public` Keyword

Members declared as `public` are accessible from anywhere — inside the class, outside the class, and in subclasses. This is the **default** access level if no modifier is specified.

### Basic Usage

```typescript
class Person {
  public name: string;
  public age: number;

  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  public greet(): string {
    return `Hi, I'm ${this.name}`;
  }
}

const person = new Person("Alice", 30);
console.log(person.name);      // "Alice" - accessible
console.log(person.age);       // 30 - accessible
console.log(person.greet());   // "Hi, I'm Alice" - accessible
```

### Implicit Public

When no access modifier is specified, members are `public` by default:

```typescript
class User {
  name: string;   // implicitly public
  email: string;  // implicitly public

  constructor(name: string, email: string) {
    this.name = name;
    this.email = email;
  }
}

const user = new User("Bob", "bob@example.com");
console.log(user.name);   // OK
console.log(user.email);  // OK
```

### When to Use `public` Explicitly

While TypeScript allows omitting `public`, explicitly marking members as `public` improves readability and makes intent clear:

```typescript
// Explicit - clear intent
class ApiClient {
  public baseUrl: string;
  public timeout: number;

  constructor(baseUrl: string, timeout: number) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }
}

// Implicit - relies on default behavior
class ApiClient {
  baseUrl: string;
  timeout: number;

  constructor(baseUrl: string, timeout: number) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }
}
```

---

## The `private` Keyword

Members declared as `private` can only be accessed within the class that defines them. They cannot be accessed from outside the class or from subclasses.

### Basic Usage

```typescript
class BankAccount {
  private balance: number;

  constructor(initialBalance: number) {
    this.balance = initialBalance;
  }

  deposit(amount: number): void {
    if (amount <= 0) {
      throw new Error("Deposit amount must be positive");
    }
    this.balance += amount;
  }

  withdraw(amount: number): void {
    if (amount > this.balance) {
      throw new Error("Insufficient funds");
    }
    this.balance -= amount;
  }

  getBalance(): number {
    return this.balance;
  }
}

const account = new BankAccount(1000);
account.deposit(500);
console.log(account.getBalance()); // 1500
// console.log(account.balance);   // Error: Property 'balance' is private
// account.balance = 1000000;      // Error: Property 'balance' is private
```

### Private Methods

```typescript
class Logger {
  private formatMessage(level: string, message: string): string {
    return `[${level.toUpperCase()}] ${new Date().toISOString()}: ${message}`;
  }

  info(message: string): void {
    console.log(this.formatMessage("info", message));
  }

  error(message: string): void {
    console.error(this.formatMessage("error", message));
  }
}

const logger = new Logger();
logger.info("Application started");
// logger.formatMessage("info", "test"); // Error: Method 'formatMessage' is private
```

### Private Constructor (Singleton Pattern)

A `private` constructor prevents external instantiation, which is useful for the singleton pattern:

```typescript
class DatabaseConnection {
  private static instance: DatabaseConnection;

  private constructor(
    private connectionString: string
  ) {}

  static getInstance(): DatabaseConnection {
    if (!DatabaseConnection.instance) {
      DatabaseConnection.instance = new DatabaseConnection("postgres://localhost:5432");
    }
    return DatabaseConnection.instance;
  }

  query(sql: string): any {
    console.log(`Executing: ${sql}`);
  }
}

// const db = new DatabaseConnection("..."); // Error: Constructor is private
const db = DatabaseConnection.getInstance();  // OK
```

### Private Properties with Getters/Setters

A common pattern is to make properties private and expose them through getters and setters:

```typescript
class Temperature {
  private _celsius: number;

  constructor(celsius: number) {
    this._celsius = celsius;
  }

  get fahrenheit(): number {
    return this._celsius * 9 / 5 + 32;
  }

  set celsius(value: number) {
    if (value < -273.15) {
      throw new Error("Temperature below absolute zero is not possible");
    }
    this._celsius = value;
  }

  get celsius(): number {
    return this._celsius;
  }
}

const temp = new Temperature(100);
console.log(temp.fahrenheit); // 212
temp.celsius = 0;
console.log(temp.fahrenheit); // 32
```

---

## The `protected` Keyword

Members declared as `protected` can be accessed within the class that defines them AND within subclasses (classes that extend it). They cannot be accessed from outside the class hierarchy.

### Basic Usage

```typescript
class Animal {
  protected name: string;

  constructor(name: string) {
    this.name = name;
  }

  protected eat(): void {
    console.log(`${this.name} is eating`);
  }
}

class Dog extends Animal {
  breed: string;

  constructor(name: string, breed: string) {
    super(name);
    this.breed = breed;
  }

  bark(): void {
    console.log(`${this.name} says Woof!`); // OK: 'name' is protected, accessible in subclass
    this.eat(); // OK: 'eat' is protected, accessible in subclass
  }
}

const dog = new Dog("Buddy", "Labrador");
dog.bark();         // OK
// dog.name;        // Error: Property 'name' is protected
// dog.eat();       // Error: Method 'eat' is protected
```

### Protected Constructor

A `protected` constructor can only be called from within the class or its subclasses:

```typescript
class Base {
  protected constructor(public value: number) {}
}

class Derived extends Base {
  static create(value: number): Derived {
    return new Derived(value); // OK: Derived extends Base
  }
}

// const base = new Base(10); // Error: Constructor is protected
const derived = Derived.create(10); // OK
```

### Protected vs Private Decision Tree

```
Should this member be accessible in subclasses?
├── YES → Use `protected`
└── NO → Use `private`
    └── Should this be accessible outside the class?
        ├── YES → Use `public`
        └── NO → Use `private`
```

### Protected with Interface Segregation

```typescript
abstract class Repository<T> {
  protected abstract findAll(): T[];
  protected abstract findById(id: string): T | undefined;

  // Public API that uses protected methods
  public getAll(): T[] {
    return this.findAll();
  }

  public getOne(id: string): T {
    const item = this.findById(id);
    if (!item) {
      throw new Error(`Item with id ${id} not found`);
    }
    return item;
  }
}

class User {
  constructor(public id: string, public name: string) {}
}

class UserRepository extends Repository<User> {
  private users: User[] = [
    new User("1", "Alice"),
    new User("2", "Bob"),
  ];

  protected findAll(): User[] {
    return this.users; // OK: protected method
  }

  protected findById(id: string): User | undefined {
    return this.users.find(u => u.id === id);
  }
}
```

---

## Parameter Property Modifiers

As seen in the previous chapter, access modifiers can be applied directly to constructor parameters to create parameter properties. Here is a comprehensive overview of all combinations:

### Complete Reference

```typescript
class Example {
  constructor(
    public a: string,              // public property
    private b: string,             // private property
    protected c: string,           // protected property
    readonly d: string,            // public readonly property
    public readonly e: string,     // public readonly (explicit)
    private readonly f: string,    // private readonly
    protected readonly g: string,  // protected readonly
  ) {}
}
```

### Common Combinations

```typescript
class User {
  constructor(
    public readonly id: string,        // ID is public but immutable
    public name: string,               // Name is public and mutable
    private _password: string,         // Password is private
    protected role: string,            // Role is accessible in subclasses
    public readonly createdAt: Date = new Date() // Read-only with default
  ) {}

  verifyPassword(input: string): boolean {
    return this._password === input;
  }
}
```

---

## Private Fields vs `#` (ECMAScript Private Fields)

TypeScript has two ways to create private members:

1. **`private` keyword** — TypeScript's compile-time privacy
2. **`#` prefix** — ECMAScript's runtime private fields (ES2022+)

### TypeScript `private` Keyword

```typescript
class TSPrivate {
  private value: string = "secret";

  getValue(): string {
    return this.value;
  }
}

const ts = new TSPrivate();
// ts.value;          // Error at compile time
// However, at runtime:
console.log((ts as any).value); // "secret" — accessible via type assertion
```

### ECMAScript `#` Private Fields

```typescript
class ESPrivate {
  #value: string = "secret";

  getValue(): string {
    return this.#value;
  }
}

const es = new ESPrivate();
// es.#value;         // SyntaxError at compile time AND runtime
console.log((es as any).value); // undefined — truly private at runtime
```

### Key Differences

| Feature | `private` keyword | `#` private fields |
|---|---|---|
| Compile-time check | Yes | Yes |
| Runtime enforcement | No | Yes |
| Available in all JS engines | N/A (TypeScript only) | ES2022+ |
| Can be accessed via `as any` | Yes | No |
| Declaration style | `private field` | `#field` |
| Can use in parameter properties | Yes | No |
| Works with declaration merging | Limited | No |

### When to Use Which

```typescript
// Use `private` for most cases (TypeScript project, compile-time is sufficient)
class UserService {
  private repository: UserRepository;

  constructor(repository: UserRepository) {
    this.repository = repository;
  }
}

// Use `#` when runtime privacy is critical (library code, security-sensitive)
class SecureToken {
  #secret: string;

  constructor(secret: string) {
    this.#secret = secret;
  }

  // Even runtime manipulation cannot access #secret
  toString(): string {
    return "SecureToken [hidden]";
  }
}
```

---

## Protected and Inheritance

The `protected` modifier interacts with inheritance in important ways. Subclasses can access protected members of their parent class, but there are some nuances to understand.

### Protected in the Inheritance Chain

```typescript
class Base {
  protected data: number[] = [1, 2, 3];

  protected process(): number[] {
    return this.data.map(x => x * 2);
  }
}

class Middle extends Base {
  protected transform(): number[] {
    return this.process(); // OK: accessing Base's protected method
  }
}

class Child extends Middle {
  doWork(): number[] {
    return this.transform(); // OK: accessing Middle's protected method
  }

  accessAll(): void {
    console.log(this.data);      // OK: inherited protected property
    console.log(this.process()); // OK: inherited protected method
    console.log(this.transform()); // OK: inherited protected method
  }
}

const child = new Child();
child.doWork();           // OK (public method)
// child.data;            // Error: Property 'data' is protected
// child.transform();     // Error: Property 'transform' is protected
```

### Protected Access and Class Hierarchy

Protected members are accessible anywhere within the class hierarchy. This means sibling classes can access each other's protected members through inheritance:

```typescript
class Shape {
  protected color: string;

  constructor(color: string) {
    this.color = color;
  }
}

class Circle extends Shape {
  protected radius: number;

  constructor(color: string, radius: number) {
    super(color);
    this.radius = radius;
  }

  describe(): string {
    return `Circle: color=${this.color}, radius=${this.radius}`;
  }
}

class Rectangle extends Shape {
  protected width: number;
  protected height: number;

  constructor(color: string, width: number, height: number) {
    super(color);
    this.width = width;
    this.height = height;
  }

  // Rectangle can access Shape's protected members
  describe(): string {
    return `Rectangle: color=${this.color}, ${this.width}x${this.height}`;
  }
}
```

---

## Access Modifier Visibility Matrix

Here's a comprehensive matrix of where each modifier can be accessed:

| Member Location | `public` | `private` | `protected` |
|---|---|---|---|
| Same class | Yes | Yes | Yes |
| Subclass (child class) | Yes | No | Yes |
| Unrelated class | Yes | No | No |
| Outside the class hierarchy | Yes | No | No |

---

## Accessor Visibility

Getters and setters can also have access modifiers:

```typescript
class Employee {
  private _name: string;
  private _salary: number;

  constructor(name: string, salary: number) {
    this._name = name;
    this._salary = salary;
  }

  // Public getter
  get name(): string {
    return this._name;
  }

  // Private setter (can only be modified internally)
  set name(value: string) {
    if (!value || value.trim().length === 0) {
      throw new Error("Name cannot be empty");
    }
    this._name = value;
  }

  // Public getter with controlled access
  get salary(): number {
    return this._salary;
  }

  // Private setter - salary can only be changed via method
  private set salary(value: number) {
    this._salary = value;
  }

  // Public method to give raise
  giveRaise(percentage: number): void {
    if (percentage < 0 || percentage > 100) {
      throw new Error("Invalid raise percentage");
    }
    this.salary = this._salary * (1 + percentage / 100);
  }
}

const emp = new Employee("Alice", 75000);
console.log(emp.name);     // "Alice"
emp.name = "Alice Smith";  // OK: public setter
console.log(emp.salary);   // 75000
// emp.salary = 100000;    // Error: setter is private
emp.giveRaise(10);         // OK: public method controls access
console.log(emp.salary);   // 82500
```

### Protected Accessors in Subclasses

```typescript
class Base {
  protected _value: number = 0;

  get value(): number {
    return this._value;
  }

  protected set value(v: number) {
    this._value = v;
  }
}

class Derived extends Base {
  increment(): void {
    this.value = this._value + 1; // Can use the protected setter
  }
}

const d = new Derived();
d.increment();
console.log(d.value); // 1
// d.value = 5;       // Error: setter is protected
```

---

## Default Visibility

In TypeScript, when no access modifier is specified, the default is `public`:

```typescript
class DefaultExample {
  name: string;     // public by default
  age: number;      // public by default

  greet() {}        // public by default
}
```

### Configuring Default with `noImplicitAny` and `strict`

While TypeScript doesn't have a "no default public" option, you can enforce explicit modifiers with linting:

```json
// .eslintrc.json
{
  "rules": {
    "@typescript-eslint/explicit-member-accessibility": ["error", {
      "accessibility": "explicit",
      "overrides": {
        "accessors": "explicit",
        "constructors": "no-public"
      }
    }]
  }
}
```

This forces you to write:

```typescript
class ExplicitExample {
  public name: string;      // Must specify public
  private _age: number;     // Must specify private

  constructor(name: string, age: number) {
    this.name = name;
    this._age = age;
  }
}
```

---

## Access Modifier Best Practices

### 1. Prefer `private` by Default, Open Up as Needed

```typescript
// Good: Start private, expose via public API
class UserService {
  private users: Map<string, User> = new Map();

  addUser(user: User): void {
    this.validateUser(user);
    this.users.set(user.id, user);
    this.logActivity(user);
  }

  getUser(id: string): User | undefined {
    return this.users.get(id);
  }

  private validateUser(user: User): void {
    if (!user.name) throw new Error("User must have a name");
  }

  private logActivity(user: User): void {
    console.log(`User added: ${user.name}`);
  }
}
```

### 2. Use `protected` Sparingly

```typescript
// Good: Only use protected when subclasses genuinely need access
class BaseRepository<T> {
  protected constructor(protected db: Database) {}

  protected async executeQuery<R>(sql: string): Promise<R> {
    return this.db.query(sql);
  }

  // Public API
  async findAll(): Promise<T[]> {
    return this.executeQuery<T[]>('SELECT * FROM table');
  }
}
```

### 3. Encapsulate State Changes

```typescript
// Good: Control how state changes
class Order {
  private status: OrderStatus = "pending";
  private items: OrderItem[] = [];

  addItem(item: OrderItem): void {
    if (this.status !== "pending") {
      throw new Error("Cannot add items after order is confirmed");
    }
    this.items.push(item);
  }

  confirm(): void {
    if (this.items.length === 0) {
      throw new Error("Cannot confirm empty order");
    }
    this.status = "confirmed";
  }

  cancel(): void {
    if (this.status === "shipped") {
      throw new Error("Cannot cancel shipped order");
    }
    this.status = "cancelled";
  }
}
```

### 4. Don't Over-Expose with `public`

```typescript
// Bad: Everything is public
class Account {
  public id: string;
  public password: string;
  public ssn: string;
  public email: string;
}

// Good: Protect sensitive data
class Account {
  public readonly id: string;
  private _password: string;
  private _ssn: string;
  public email: string;

  verifyPassword(input: string): boolean {
    return this._password === input;
  }

  // Provide a safe way to display SSN
  getMaskedSSN(): string {
    return "***-**-" + this._ssn.slice(-4);
  }
}
```

---

## Encapsulation Principles

Encapsulation is the practice of bundling data and methods that operate on that data, while restricting direct access to some components. This leads to:

### 1. Data Integrity

Private state ensures objects remain in valid states:

```typescript
class Temperature {
  private _celsius: number;

  constructor(celsius: number) {
    this.setCelsius(celsius);
  }

  setCelsius(value: number): void {
    if (value < -273.15) {
      throw new Error("Below absolute zero");
    }
    this._celsius = value;
  }

  getCelsius(): number {
    return this._celsius;
  }
}
```

### 2. Implementation Hiding

Users of a class don't need to know how it works internally:

```typescript
class Sorter {
  private data: number[] = [];

  add(value: number): void {
    this.data.push(value);
  }

  // Users don't need to know the sorting algorithm
  getSorted(): number[] {
    return [...this.data].sort((a, b) => a - b);
  }
}
```

### 3. Flexibility to Change

Private internals can be changed without affecting the public API:

```typescript
// V1: Simple implementation
class Cache {
  private data: Map<string, any> = new Map();

  get(key: string): any { return this.data.get(key); }
  set(key: string, value: any): void { this.data.set(key, value); }
}

// V2: Changed internal implementation (LRU cache)
// Public API remains the same
class Cache {
  private data: Map<string, any> = new Map();
  private accessOrder: string[] = [];
  private maxSize: number;

  get(key: string): any {
    if (!this.data.has(key)) return undefined;
    this.promote(key);
    return this.data.get(key);
  }

  set(key: string, value: any): void {
    if (this.data.size >= this.maxSize) {
      this.evict();
    }
    this.data.set(key, value);
    this.accessOrder.push(key);
  }

  private promote(key: string): void {
    this.accessOrder = this.accessOrder.filter(k => k !== key);
    this.accessOrder.push(key);
  }

  private evict(): void {
    const oldest = this.accessOrder.shift();
    if (oldest) this.data.delete(oldest);
  }
}
```

### 4. Interface-Based Design

Use interfaces to define public contracts while keeping implementations private:

```typescript
interface ILogger {
  info(message: string): void;
  error(message: string): void;
}

class ConsoleLogger implements ILogger {
  info(message: string): void {
    console.log(`[INFO] ${message}`);
  }

  error(message: string): void {
    console.error(`[ERROR] ${message}`);
  }
}

class FileLogger implements ILogger {
  // Completely different implementation
  // But same public interface
  info(message: string): void {
    // Write to file
  }

  error(message: string): void {
    // Write to file with error prefix
  }
}
```

---

## Interview Questions

### Q1: What is the difference between `public`, `private`, and `protected`?

**Answer:**
- **`public`**: Accessible from anywhere (default in TypeScript)
- **`private`**: Accessible only within the defining class
- **`protected`**: Accessible within the defining class and its subclasses

```typescript
class Example {
  public a = 1;    // everywhere
  private b = 2;   // only in Example
  protected c = 3; // Example + subclasses
}
```

### Q2: Are TypeScript access modifiers enforced at runtime?

**Answer:** No. TypeScript's `public`, `private`, and `protected` are compile-time only. At runtime, all properties are accessible. For true runtime privacy, use ECMAScript's `#` private fields syntax.

```typescript
class Secret {
  private value = 42;
}
const s = new Secret();
console.log((s as any).value); // 42 — bypasses private
```

### Q3: What is the difference between `private` and `#`?

**Answer:** TypeScript's `private` keyword is compile-time only — you can bypass it with `as any`. ECMAScript's `#` prefix creates truly private fields that are inaccessible even at runtime. However, `#` fields cannot be used in parameter properties, declaration merging, or some TypeScript-specific features.

### Q4: When should you use `protected` instead of `private`?

**Answer:** Use `protected` when subclasses genuinely need access to a member. If a member is only used within the defining class, keep it `private`. Overusing `protected` weakens encapsulation and makes the class harder to refactor.

### Q5: Can a constructor be `protected`? When would you do that?

**Answer:** Yes. A protected constructor prevents direct instantiation from outside the class hierarchy while allowing subclasses to call `super()`. This is useful for abstract base classes or when you want to control instantiation through factory methods:

```typescript
class Base {
  protected constructor(public value: number) {}
}

class Derived extends Base {
  static create(value: number): Derived {
    return new Derived(value);
  }
}
```

### Q6: Can accessors (getters/setters) have different visibility?

**Answer:** Yes. A getter and setter for the same property can have different access modifiers. For example, a public getter with a private setter allows reading from outside while restricting writes to within the class:

```typescript
class Example {
  private _value = 0;
  get value(): number { return this._value; }
  private set value(v: number) { this._value = v; }
}
```

### Q7: How can you enforce explicit access modifiers in your project?

**Answer:** Use ESLint with the `@typescript-eslint/explicit-member-accessibility` rule set to `"error"` with `"accessibility": "explicit"`. This forces developers to declare `public`, `private`, or `protected` on every class member.

---

**Next:** [03 - Getters and Setters](./03-getters-and-setters.md)
