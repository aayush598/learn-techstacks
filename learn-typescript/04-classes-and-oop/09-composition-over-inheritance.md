# 09 - Composition Over Inheritance

## Table of Contents

- [Introduction](#introduction)
- [Why Composition](#why-composition)
- [HAS-A vs IS-A](#has-a-vs-is-a)
- [Composing Behaviors](#composing-behaviors)
- [Strategy Pattern](#strategy-pattern)
- [Dependency Injection](#dependency-injection)
- [Functional Composition](#functional-composition)
- [Pipe and Compose](#pipe-and-compose)
- [Composition with Interfaces](#composition-with-interfaces)
- [Real-World Examples](#real-world-examples)
- [Interview Questions](#interview-questions)

---

## Introduction

Composition is a design principle where complex objects are built by combining simpler, reusable objects rather than through inheritance hierarchies. The principle states: **"Favor composition over inheritance."**

Inheritance creates tight coupling between parent and child classes. Composition creates loosely coupled systems where behaviors can be mixed and matched at runtime.

---

## Why Composition

### Problems with Inheritance

```typescript
// Inheritance creates tight coupling
class Animal {
  eat() { console.log("Eating"); }
  sleep() { console.log("Sleeping"); }
}

class FlyingAnimal extends Animal {
  fly() { console.log("Flying"); }
}

class SwimmingAnimal extends Animal {
  swim() { console.log("Swimming"); }
}

// Problem: What about a duck? It flies AND swims.
// Single inheritance can't handle this cleanly.
class Duck extends FlyingAnimal {
  // Can't also extend SwimmingAnimal
  swim() { console.log("Swimming"); } // Had to duplicate swim
}

// Problem: What about a penguin? It swims but doesn't fly.
class Penguin extends Animal {
  swim() { console.log("Swimming"); }
  // Penguin has a fly() from FlyingAnimal but can't actually fly!
  // This violates the Liskov Substitution Principle
}
```

### Benefits of Composition

```typescript
// Composition: Mix behaviors freely
class FlyBehavior {
  fly(): string {
    return "Flying through the air";
  }
}

class SwimBehavior {
  swim(): string {
    return "Swimming in water";
  }
}

class WalkBehavior {
  walk(): string {
    return "Walking on ground";
  }
}

class Duck {
  private flyBehavior = new FlyBehavior();
  private swimBehavior = new SwimBehavior();
  private walkBehavior = new WalkBehavior();

  fly(): string { return this.flyBehavior.fly(); }
  swim(): string { return this.swimBehavior.swim(); }
  walk(): string { return this.walkBehavior.walk(); }
}

class Penguin {
  private swimBehavior = new SwimBehavior();
  private walkBehavior = new WalkBehavior();

  swim(): string { return this.swimBehavior.swim(); }
  walk(): string { return this.walkBehavior.walk(); }
  // No fly() — penguin doesn't fly
}
```

---

## HAS-A vs IS-A

### IS-A (Inheritance)

```typescript
// Dog IS-A Animal — inheritance makes sense here
class Animal {
  constructor(public name: string) {}
}

class Dog extends Animal {
  bark() { return "Woof!"; }
}
```

### HAS-A (Composition)

```typescript
// Car HAS-A Engine — composition makes sense here
class Engine {
  start() { return "Engine started"; }
  stop() { return "Engine stopped"; }
}

class Transmission {
  shiftGear(gear: number) { return `Shifted to gear ${gear}`; }
}

class Car {
  private engine = new Engine();
  private transmission = new Transmission();
  private currentGear = 0;

  start(): string {
    return this.engine.start();
  }

  stop(): string {
    this.currentGear = 0;
    return this.engine.stop();
  }

  shiftUp(): string {
    this.currentGear++;
    return this.transmission.shiftGear(this.currentGear);
  }

  shiftDown(): string {
    if (this.currentGear > 0) this.currentGear--;
    return this.transmission.shiftGear(this.currentGear);
  }
}
```

### Decision Guide

| Relationship | Use | Example |
|---|---|---|
| IS-A | Inheritance | Dog is an Animal |
| HAS-A | Composition | Car has an Engine |
| USES-A | Dependency | Service uses Logger |
| CAN-DO | Interface | User can Serialize |

---

## Composing Behaviors

### Behavior Objects

```typescript
interface FlyBehavior {
  fly(): string;
}

interface QuackBehavior {
  quack(): string;
}

interface SwimBehavior {
  swim(): string;
}

class WingsFly implements FlyBehavior {
  fly(): string { return "Flapping wings"; }
}

class NoFly implements FlyBehavior {
  fly(): string { return "Can't fly"; }
}

class JetFly implements FlyBehavior {
  fly(): string { return "Flying with jets"; }
}

class LoudQuack implements QuackBehavior {
  quack(): string { return "QUACK!"; }
}

class Squeak implements QuackBehavior {
  quack(): string { return "Squeak!"; }
}

class NoQuack implements QuackBehavior {
  quack(): string { return "Silence"; }
}

class水上Swim implements SwimBehavior {
  swim(): string { return "Paddling"; }
}

class DiveSwim implements SwimBehavior {
  swim(): string { return "Diving deep"; }
}

// Duck class composed of behaviors
class Duck {
  constructor(
    private flyBehavior: FlyBehavior,
    private quackBehavior: QuackBehavior,
    private swimBehavior: SwimBehavior
  ) {}

  fly(): string { return this.flyBehavior.fly(); }
  quack(): string { return this.quackBehavior.quack(); }
  swim(): string { return this.swimBehavior.swim(); }

  performFly(): string { return this.flyBehavior.fly(); }
}

// Create different ducks by composing behaviors
const mallardDuck = new Duck(new WingsFly(), new LoudQuack(), new 水上Swim());
const rubberDuck = new Duck(new NoFly(), new Squeak(), new 水上Swim());
const robotDuck = new Duck(new JetFly(), new NoQuack(), new DiveSwim());
```

### Swapping Behaviors at Runtime

```typescript
class Duck {
  private flyBehavior: FlyBehavior;
  private quackBehavior: QuackBehavior;

  constructor() {
    this.flyBehavior = new WingsFly();
    this.quackBehavior = new LoudQuack();
  }

  setFlyBehavior(behavior: FlyBehavior): void {
    this.flyBehavior = behavior;
  }

  setQuackBehavior(behavior: QuackBehavior): void {
    this.quackBehavior = behavior;
  }

  performFly(): string { return this.flyBehavior.fly(); }
  performQuack(): string { return this.quackBehavior.quack(); }
}

const duck = new Duck();
console.log(duck.performFly()); // "Flapping wings"

duck.setFlyBehavior(new JetFly());
console.log(duck.performFly()); // "Flying with jets"
```

---

## Strategy Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable.

### Basic Strategy Pattern

```typescript
interface SortStrategy<T> {
  sort(data: T[]): T[];
  readonly name: string;
}

class BubbleSort<T> implements SortStrategy<T> {
  readonly name = "Bubble Sort";

  sort(data: T[]): T[] {
    const arr = [...data];
    for (let i = 0; i < arr.length; i++) {
      for (let j = 0; j < arr.length - i - 1; j++) {
        if (arr[j] > arr[j + 1]) {
          [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        }
      }
    }
    return arr;
  }
}

class QuickSort<T> implements SortStrategy<T> {
  readonly name = "Quick Sort";

  sort(data: T[]): T[] {
    if (data.length <= 1) return [...data];
    const pivot = data[0];
    const left = data.slice(1).filter(x => x <= pivot);
    const right = data.slice(1).filter(x => x > pivot);
    return [...this.sort(left), pivot, ...this.sort(right)];
  }
}

class Sorter<T> {
  private strategy: SortStrategy<T>;

  constructor(strategy: SortStrategy<T>) {
    this.strategy = strategy;
  }

  setStrategy(strategy: SortStrategy<T>): void {
    this.strategy = strategy;
    console.log(`Strategy changed to ${strategy.name}`);
  }

  sort(data: T[]): T[] {
    console.log(`Sorting with ${this.strategy.name}`);
    return this.strategy.sort(data);
  }
}

const sorter = new Sorter(new BubbleSort());
sorter.sort([3, 1, 4, 1, 5, 9]);

sorter.setStrategy(new QuickSort());
sorter.sort([3, 1, 4, 1, 5, 9]);
```

### Validation Strategy Pattern

```typescript
interface ValidationStrategy {
  validate(value: string): boolean;
  getMessage(field: string): string;
}

class RequiredValidation implements ValidationStrategy {
  validate(value: string): boolean {
    return value.trim().length > 0;
  }

  getMessage(field: string): string {
    return `${field} is required`;
  }
}

class EmailValidation implements ValidationStrategy {
  private static EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  validate(value: string): boolean {
    return EmailValidation.EMAIL_REGEX.test(value);
  }

  getMessage(field: string): string {
    return `${field} must be a valid email`;
  }
}

class MinLengthValidation implements ValidationStrategy {
  constructor(private minLength: number) {}

  validate(value: string): boolean {
    return value.length >= this.minLength;
  }

  getMessage(field: string): string {
    return `${field} must be at least ${this.minLength} characters`;
  }
}

class FieldValidator {
  private strategies: ValidationStrategy[] = [];

  addStrategy(strategy: ValidationStrategy): this {
    this.strategies.push(strategy);
    return this;
  }

  validate(value: string, fieldName: string): string[] {
    const errors: string[] = [];
    for (const strategy of this.strategies) {
      if (!strategy.validate(value)) {
        errors.push(strategy.getMessage(fieldName));
      }
    }
    return errors;
  }
}

// Usage
const emailValidator = new FieldValidator()
  .addStrategy(new RequiredValidation())
  .addStrategy(new EmailValidation());

const nameValidator = new FieldValidator()
  .addStrategy(new RequiredValidation())
  .addStrategy(new MinLengthValidation(2));

console.log(emailValidator.validate("", "Email"));
// ["Email is required"]

console.log(emailValidator.validate("invalid", "Email"));
// ["Email must be a valid email"]

console.log(nameValidator.validate("A", "Name"));
// ["Name must be at least 2 characters"]
```

---

## Dependency Injection

DI is a form of composition where objects receive their dependencies from outside rather than creating them internally.

### Constructor Injection

```typescript
interface Logger {
  info(msg: string): void;
  error(msg: string): void;
}

interface Database {
  query<T>(sql: string): Promise<T[]>;
}

interface Cache {
  get<T>(key: string): T | null;
  set<T>(key: string, value: T): void;
}

class UserService {
  constructor(
    private logger: Logger,
    private db: Database,
    private cache: Cache
  ) {}

  async getUser(id: string) {
    // Check cache first
    const cached = this.cache.get<User>(`user:${id}`);
    if (cached) {
      this.logger.info(`Cache hit for user ${id}`);
      return cached;
    }

    // Query database
    this.logger.info(`Fetching user ${id} from database`);
    const [user] = await this.db.query<User>(`SELECT * FROM users WHERE id = '${id}'`);

    if (user) {
      this.cache.set(`user:${id}`, user);
    }

    return user;
  }
}
```

### Simple DI Container

```typescript
class Container {
  private services = new Map<string, any>();
  private factories = new Map<string, () => any>();

  register<T>(name: string, factory: () => T): void {
    this.factories.set(name, factory);
  }

  resolve<T>(name: string): T {
    if (!this.services.has(name)) {
      const factory = this.factories.get(name);
      if (!factory) {
        throw new Error(`Service '${name}' not registered`);
      }
      this.services.set(name, factory());
    }
    return this.services.get(name) as T;
  }
}

const container = new Container();

container.register<Logger>("Logger", () => new ConsoleLogger());
container.register<Database>("Database", () => new PostgresDatabase());
container.register<Cache>("Cache", () => new RedisCache());
container.register<UserService>("UserService", () => {
  return new UserService(
    container.resolve<Logger>("Logger"),
    container.resolve<Database>("Database"),
    container.resolve<Cache>("Cache")
  );
});

const userService = container.resolve<UserService>("UserService");
```

---

## Functional Composition

Functions can be composed together to build complex behavior from simple functions.

### Basic Function Composition

```typescript
type Fn<A, B> = (a: A) => B;

function compose<A, B, C>(
  f: Fn<B, C>,
  g: Fn<A, B>
): Fn<A, C> {
  return (a: A) => f(g(a));
}

const trim = (s: string) => s.trim();
const toLowerCase = (s: string) => s.toLowerCase();
const split = (separator: string) => (s: string) => s.split(separator);

const processEmail = compose(
  split("@"),
  compose(toLowerCase, trim)
);

console.log(processEmail("  John.DOE@Example.COM  "));
// ["john.doe@example.com"]
```

### Composing Data Transformations

```typescript
interface Product {
  name: string;
  price: number;
  category: string;
  inStock: boolean;
}

const filterInStock = (products: Product[]): Product[] =>
  products.filter(p => p.inStock);

const sortByPrice = (products: Product[]): Product[] =>
  [...products].sort((a, b) => a.price - b.price);

const formatAsList = (products: Product[]): string[] =>
  products.map(p => `${p.name} - $${p.price.toFixed(2)}`);

// Compose operations
function compose<T>(...fns: Array<(arg: T) => T>): (arg: T) => T {
  return (arg: T) => fns.reduce((result, fn) => fn(result), arg);
}

const getAffordableInStockProducts = compose(
  formatAsList,
  sortByPrice,
  filterInStock
);

const products: Product[] = [
  { name: "Laptop", price: 999, category: "electronics", inStock: true },
  { name: "Mouse", price: 25, category: "electronics", inStock: true },
  { name: "Desk", price: 200, category: "furniture", inStock: false },
  { name: "Keyboard", price: 75, category: "electronics", inStock: true },
];

const result = getAffordableInStockProducts(products);
// ["Mouse - $25.00", "Keyboard - $75.00", "Laptop - $999.00"]
```

---

## Pipe and Compose

### Pipe (Left-to-Right)

```typescript
function pipe<A>(a: A): A;
function pipe<A, B>(a: A, ab: (a: A) => B): B;
function pipe<A, B, C>(a: A, ab: (a: A) => B, bc: (b: B) => C): C;
function pipe(a: any, ...fns: Function[]): any {
  return fns.reduce((result, fn) => fn(result), a);
}

const result = pipe(
  "  Hello, World!  ",
  (s: string) => s.trim(),
  (s: string) => s.toLowerCase(),
  (s: string) => s.replace(/[!,.]/g, ""),
  (s: string) => s.split(" ")
);

console.log(result); // ["hello", "world"]
```

### Compose (Right-to-Left)

```typescript
function compose<A, B>(ab: (a: A) => B): (a: A) => B;
function compose<A, B, C>(
  bc: (b: B) => C,
  ab: (a: A) => B
): (a: A) => C;
function compose(...fns: Function[]): Function {
  return fns.reduce((f, g) => (...args: any[]) => f(g(...args)));
}

const processString = compose(
  (s: string) => s.split(" "),
  (s: string) => s.replace(/[!,.]/g, ""),
  (s: string) => s.toLowerCase(),
  (s: string) => s.trim()
);

console.log(processString("  Hello, World!  "));
// ["hello", "world"]
```

### Real-World Pipe Example

```typescript
interface ValidationError {
  field: string;
  message: string;
}

type Validator = (value: string) => string | null;

const required: Validator = (value) =>
  value.trim() === 0 ? "Field is required" : null;

const minLength = (min: number): Validator => (value) =>
  value.length < min ? `Must be at least ${min} characters` : null;

const maxLength = (max: number): Validator => (value) =>
  value.length > max ? `Must be at most ${max} characters` : null;

const matches = (regex: RegExp, message: string): Validator => (value) =>
  !regex.test(value) ? message : null;

function createValidator(...validators: Validator[]): Validator {
  return (value: string) => {
    for (const validate of validators) {
      const error = validate(value);
      if (error) return error;
    }
    return null;
  };
}

const usernameValidator = createValidator(
  required,
  minLength(3),
  maxLength(20),
  matches(/^[a-zA-Z0-9_]+$/, "Only alphanumeric and underscores")
);

console.log(usernameValidator("ab"));    // "Must be at least 3 characters"
console.log(usernameValidator("a".repeat(21))); // "Must be at most 20 characters"
console.log(usernameValidator("valid_user"));   // null (valid)
```

---

## Composition with Interfaces

Interfaces define the contracts that composed objects must satisfy.

### Composable Interface Design

```typescript
interface Hashable {
  hash(): string;
}

interface Comparable<T> {
  compareTo(other: T): number;
}

interface Serializable {
  serialize(): string;
  deserialize(data: string): void;
}

// A class can compose multiple interface implementations
class CacheEntry<T> implements Hashable, Comparable<CacheEntry<T>>, Serializable {
  constructor(
    public key: string,
    public value: T,
    public expiry: number
  ) {}

  hash(): string {
    return `${this.key}:${this.expiry}`;
  }

  compareTo(other: CacheEntry<T>): number {
    return this.expiry - other.expiry;
  }

  serialize(): string {
    return JSON.stringify({ key: this.key, value: this.value, expiry: this.expiry });
  }

  deserialize(data: string): void {
    const parsed = JSON.parse(data);
    this.key = parsed.key;
    this.value = parsed.value;
    this.expiry = parsed.expiry;
  }
}
```

### Mix of Interface and Composition

```typescript
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<void>;
  delete(id: string): Promise<boolean>;
}

interface EventEmitter {
  on(event: string, handler: (...args: any[]) => void): void;
  emit(event: string, ...args: any[]): void;
}

class EventRepository<T> implements Repository<T> {
  private events: EventEmitter = new EventEmitterImpl();

  constructor(
    private delegate: Repository<T>,
    private entityName: string
  ) {}

  async findById(id: string): Promise<T | null> {
    this.events.emit(`${this.entityName}.findById`, id);
    const result = await this.delegate.findById(id);
    this.events.emit(`${this.entityName}.findById.result`, result);
    return result;
  }

  async findAll(): Promise<T[]> {
    return this.delegate.findAll();
  }

  async save(entity: T): Promise<void> {
    await this.delegate.save(entity);
    this.events.emit(`${this.entityName}.saved`, entity);
  }

  async delete(id: string): Promise<boolean> {
    const result = await this.delegate.delete(id);
    this.events.emit(`${this.entityName}.deleted`, id);
    return result;
  }
}
```

---

## Real-World Examples

### Notification System

```typescript
interface NotificationChannel {
  send(recipient: string, message: string): Promise<void>;
  readonly channelName: string;
}

class EmailChannel implements NotificationChannel {
  readonly channelName = "email";
  async send(recipient: string, message: string): Promise<void> {
    console.log(`Email to ${recipient}: ${message}`);
  }
}

class SMSChannel implements NotificationChannel {
  readonly channelName = "sms";
  async send(recipient: string, message: string): Promise<void> {
    console.log(`SMS to ${recipient}: ${message}`);
  }
}

class PushNotificationChannel implements NotificationChannel {
  readonly channelName = "push";
  async send(recipient: string, message: string): Promise<void> {
    console.log(`Push to ${recipient}: ${message}`);
  }
}

class NotificationService {
  private channels: NotificationChannel[] = [];

  addChannel(channel: NotificationChannel): this {
    this.channels.push(channel);
    return this;
  }

  async notify(recipient: string, message: string): Promise<void> {
    const results = await Promise.allSettled(
      this.channels.map(channel => channel.send(recipient, message))
    );

    results.forEach((result, index) => {
      if (result.status === "rejected") {
        console.error(`Failed to send via ${this.channels[index].channelName}: ${result.reason}`);
      }
    });
  }
}

// Compose notification service with desired channels
const notifier = new NotificationService()
  .addChannel(new EmailChannel())
  .addChannel(new SMSChannel());

notifier.notify("user@example.com", "Your order is ready!");
```

### Plugin System

```typescript
interface Plugin {
  name: string;
  version: string;
  initialize(): void;
  execute(data: any): any;
  destroy(): void;
}

class AnalyticsPlugin implements Plugin {
  name = "analytics";
  version = "1.0.0";

  initialize(): void {
    console.log("Analytics initialized");
  }

  execute(data: any): any {
    console.log("Tracking:", data);
    return data;
  }

  destroy(): void {
    console.log("Analytics destroyed");
  }
}

class CachePlugin implements Plugin {
  name = "cache";
  version = "1.0.0";
  private store = new Map();

  initialize(): void {
    console.log("Cache initialized");
  }

  execute(data: any): any {
    // Check cache, return cached or process
    return data;
  }

  destroy(): void {
    this.store.clear();
    console.log("Cache destroyed");
  }
}

class PluginManager {
  private plugins: Plugin[] = [];

  register(plugin: Plugin): void {
    this.plugins.push(plugin);
    plugin.initialize();
  }

  async process(data: any): Promise<any> {
    let result = data;
    for (const plugin of this.plugins) {
      result = plugin.execute(result);
    }
    return result;
  }

  shutdown(): void {
    this.plugins.forEach(p => p.destroy());
    this.plugins = [];
  }
}
```

---

## Interview Questions

### Q1: What is composition over inheritance?

**Answer:** Composition is a design principle where complex objects are built by combining simpler, reusable objects rather than through class inheritance. It promotes loose coupling, flexibility, and easier testing. Instead of inheriting behavior, objects compose behaviors as internal components.

### Q2: What is the difference between HAS-A and IS-A?

**Answer:** IS-A represents inheritance (Dog IS-A Animal). HAS-A represents composition (Car HAS-A Engine). Use inheritance when there's a clear type hierarchy. Use composition when an object contains other objects or behaviors.

### Q3: What is the Strategy Pattern?

**Answer:** The Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. It lets the algorithm vary independently from clients that use it. In TypeScript, this is typically implemented with interfaces for each strategy and a context class that uses a strategy.

### Q4: What is function composition?

**Answer:** Function composition combines two or more functions to produce a new function. The output of one function becomes the input of the next. This creates data transformation pipelines and is a key concept in functional programming.

### Q5: When is inheritance appropriate?

**Answer:** Inheritance is appropriate when there's a genuine IS-A relationship, the subclass is a true specialization of the parent, and you need polymorphism through the class hierarchy. Use it sparingly — prefer composition for code reuse.

### Q6: What is the difference between pipe and compose?

**Answer:** Both are forms of function composition. Pipe applies functions left-to-right: `pipe(data, fn1, fn2)`. Compose applies functions right-to-left: `compose(fn2, fn1)(data)`. Pipe reads more naturally for sequential data transformations.

---

**Next:** [10 - Mixins](./10-mixins.md)
