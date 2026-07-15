# 08 - Polymorphism in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [Method Overriding (Runtime Polymorphism)](#method-overriding-runtime-polymorphism)
- [Compile-Time Polymorphism](#compile-time-polymorphism)
- [Duck Typing](#duck-typing)
- [Structural Polymorphism](#structural-polymorphism)
- [Variant Types](#variant-types)
- [Covariant and Contravariant Properties](#covariant-and-contravariant-properties)
- [SOLID Principles in TypeScript](#solid-principles-in-typescript)
- [Interview Questions](#interview-questions)

---

## Introduction

Polymorphism means "many forms." In OOP, it allows objects of different types to be treated through a uniform interface. TypeScript supports polymorphism through class inheritance, interfaces, generics, and structural typing.

---

## Method Overriding (Runtime Polymorphism)

Runtime polymorphism (dynamic dispatch) occurs when a method call is resolved at runtime based on the actual type of the object, not the declared type.

### Basic Runtime Polymorphism

```typescript
abstract class Shape {
  abstract area(): number;
  abstract describe(): string;
}

class Circle extends Shape {
  constructor(public radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  describe(): string {
    return `Circle with radius ${this.radius}`;
  }
}

class Rectangle extends Shape {
  constructor(public width: number, public height: number) {
    super();
  }

  area(): number {
    return this.width * this.height;
  }

  describe(): string {
    return `Rectangle ${this.width}x${this.height}`;
  }
}

class Triangle extends Shape {
  constructor(public base: number, public height: number) {
    super();
  }

  area(): number {
    return (this.base * this.height) / 2;
  }

  describe(): string {
    return `Triangle (base: ${this.base}, height: ${this.height})`;
  }
}

// Polymorphism in action — same code, different behavior
const shapes: Shape[] = [
  new Circle(5),
  new Rectangle(4, 6),
  new Triangle(3, 8),
];

shapes.forEach(shape => {
  console.log(`${shape.describe()} = area: ${shape.area().toFixed(2)}`);
});
```

### Polymorphism with Interfaces

```typescript
interface PaymentProcessor {
  processPayment(amount: number): Promise<PaymentResult>;
  refund(transactionId: string): Promise<boolean>;
  getProviderName(): string;
}

interface PaymentResult {
  success: boolean;
  transactionId: string;
}

class StripeProcessor implements PaymentProcessor {
  async processPayment(amount: number): Promise<PaymentResult> {
    console.log(`Processing $${amount} via Stripe`);
    return { success: true, transactionId: `stripe_${Date.now()}` };
  }

  async refund(transactionId: string): Promise<boolean> {
    console.log(`Refunding ${transactionId} via Stripe`);
    return true;
  }

  getProviderName(): string {
    return "Stripe";
  }
}

class PayPalProcessor implements PaymentProcessor {
  async processPayment(amount: number): Promise<PaymentResult> {
    console.log(`Processing $${amount} via PayPal`);
    return { success: true, transactionId: `paypal_${Date.now()}` };
  }

  async refund(transactionId: string): Promise<boolean> {
    console.log(`Refunding ${transactionId} via PayPal`);
    return true;
  }

  getProviderName(): string {
    return "PayPal";
  }
}

// Client code doesn't know or care which processor is used
async function checkout(processor: PaymentProcessor, amount: number): Promise<void> {
  console.log(`Using ${processor.getProviderName()}`);
  const result = await processor.processPayment(amount);
  if (result.success) {
    console.log(`Payment successful: ${result.transactionId}`);
  }
}
```

### Polymorphism with instanceof

```typescript
class Error {
  constructor(public message: string) {}
}

class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
  }
}

class NetworkError extends Error {
  constructor(message: string, public statusCode: number) {
    super(message);
  }
}

function handleError(error: Error): string {
  if (error instanceof ValidationError) {
    return `Validation failed on field "${error.field}": ${error.message}`;
  }
  if (error instanceof NetworkError) {
    return `Network error ${error.statusCode}: ${error.message}`;
  }
  return `Error: ${error.message}`;
}
```

---

## Compile-Time Polymorphism

Compile-time polymorphism is achieved through generics and method overloading. The compiler resolves which implementation to use at compile time.

### Generic Polymorphism

```typescript
class DataStore<T> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  get(index: number): T | undefined {
    return this.items[index];
  }

  find(predicate: (item: T) => boolean): T | undefined {
    return this.items.find(predicate);
  }

  filter(predicate: (item: T) => boolean): T[] {
    return this.items.filter(predicate);
  }
}

// Different type parameters — same class, different behavior
const numbers = new DataStore<number>();
numbers.add(1);
numbers.add(2);
numbers.add(3);

const strings = new DataStore<string>();
strings.add("hello");
strings.add("world");

const users = new DataStore<{ id: string; name: string }>();
users.add({ id: "1", name: "Alice" });
```

### Method Overloading

```typescript
class Formatter {
  format(value: string): string;
  format(value: number): string;
  format(value: Date): string;
  format(value: string | number | Date): string {
    if (typeof value === "string") {
      return value.toUpperCase();
    }
    if (typeof value === "number") {
      return value.toFixed(2);
    }
    return value.toISOString().split("T")[0];
  }
}

const formatter = new Formatter();
console.log(formatter.format("hello"));       // "HELLO"
console.log(formatter.format(3.14159));      // "3.14"
console.log(formatter.format(new Date()));   // "2024-01-15"
```

### Generics with Constraints for Type-Safe Polymorphism

```typescript
interface HasId {
  id: string;
}

class EntityService<T extends HasId> {
  private entities: Map<string, T> = new Map();

  add(entity: T): void {
    this.entities.set(entity.id, entity);
  }

  getById(id: string): T | undefined {
    return this.entities.get(id);
  }

  update(id: string, updates: Partial<Omit<T, "id">>): T | undefined {
    const entity = this.entities.get(id);
    if (!entity) return undefined;
    Object.assign(entity, updates);
    return entity;
  }

  delete(id: string): boolean {
    return this.entities.delete(id);
  }
}
```

---

## Duck Typing

TypeScript uses structural typing (duck typing): "If it walks like a duck and quacks like a duck, it's a duck." Objects are compatible based on their structure, not their explicit type declarations.

### Basic Duck Typing

```typescript
interface Duck {
  quack(): string;
  walk(): string;
}

class RealDuck {
  quack(): string {
    return "Quack!";
  }

  walk(): string {
    return "Waddle waddle";
  }
}

class RubberDuck {
  quack(): string {
    return "Squeak!";
  }

  walk(): string {
    return "Can't walk";
  }
}

class Person {
  quack(): string {
    return "I'm quacking like a duck!";
  }

  walk(): string {
    return "Walking normally";
  }
}

// All three work — they satisfy the Duck interface structurally
function watchDuck(duck: Duck): void {
  console.log(duck.quack());
  console.log(duck.walk());
}

watchDuck(new RealDuck());
watchDuck(new RubberDuck());
watchDuck(new Person());
```

### Duck Typing in Practice

```typescript
interface HasLength {
  length: number;
}

function logLength(item: HasLength): void {
  console.log(`Length: ${item.length}`);
}

logLength("hello");       // string has .length
logLength([1, 2, 3]);     // array has .length
logLength({ length: 10 }); // any object with .length
// logLength(42);          // Error: number doesn't have .length
```

### Structural Compatibility

```typescript
interface Point2D {
  x: number;
  y: number;
}

class Point3D {
  constructor(
    public x: number,
    public y: number,
    public z: number
  ) {}
}

function printPoint(point: Point2D): void {
  console.log(`(${point.x}, ${point.y})`);
}

const p3d = new Point3D(1, 2, 3);
printPoint(p3d); // OK: Point3D has x and y, satisfies Point2D structurally
```

---

## Structural Polymorphism

TypeScript's structural type system enables polymorphism without explicit interface implementation.

### Structural Equivalence

```typescript
interface Printable {
  print(): string;
}

// This class doesn't explicitly implement Printable, but it satisfies the interface
class Invoice {
  constructor(public amount: number, public client: string) {}

  print(): string {
    return `Invoice: $${this.amount} for ${this.client}`;
  }
}

class Receipt {
  constructor(public amount: number, public store: string) {}

  print(): string {
    return `Receipt: $${this.amount} at ${this.store}`;
  }
}

function printItem(item: Printable): void {
  console.log(item.print());
}

printItem(new Invoice(100, "Acme")); // OK
printItem(new Receipt(50, "Store")); // OK
```

### Conditional Structural Typing

```typescript
function process<T extends { toString(): string }>(item: T): string {
  return item.toString();
}

process("hello");
process(42);
process(new Date());
process({ toString: () => "custom" });
```

---

## Variant Types

Variance describes how subtyping relationships between complex types relate to subtyping relationships between their component types.

### Invariance

Two types are invariant if neither is a subtype of the other:

```typescript
class MutableBox<T> {
  constructor(public value: T) {}
}

// Invariant: MutableBox<Cat> is NOT assignable to MutableBox<Animal>
// because you could put a Dog into the Animal slot
```

### Covariance

A type is covariant if `SubType` assignable to `SuperType` implies `Container<SubType>` assignable to `Container<SuperType>`:

```typescript
interface Producer<out T> {
  produce(): T;  // T only appears in output position
}

interface Animal { name: string; }
interface Dog extends Animal { breed: string; }

// Producer<Dog> IS assignable to Producer<Animal>
// because Dog extends Animal
declare const dogProducer: Producer<Dog>;
const animalProducer: Producer<Animal> = dogProducer; // OK
```

### Contravariance

A type is contravariant if the relationship is reversed:

```typescript
interface Consumer<in T> {
  consume(item: T): void;  // T only appears in input position
}

// Consumer<Animal> IS assignable to Consumer<Dog>
// because a consumer of Animals can certainly consume Dogs
declare const animalConsumer: Consumer<Animal>;
const dogConsumer: Consumer<Dog> = animalConsumer; // OK
```

### Bivariance

```typescript
interface EventHandler<in out T> {
  handle(event: T): void;  // T in both positions
}
```

### TypeScript's `strictFunctionTypes`

With `strictFunctionTypes` enabled:
- Function parameter types are contravariant
- Function return types are covariant
- Method parameters are bivariant (for pragmatic reasons)

```typescript
class Animal {
  name = "animal";
}

class Dog extends Animal {
  breed = "unknown";
}

class Puppy extends Dog {
  isGoodBoy = true;
}

// With strictFunctionTypes:
type Fn<A, B> = (a: A) => B;

type AnimalToDog = Fn<Animal, Dog>;
type DogToDog = Fn<Dog, Dog>;

// Function parameters are contravariant
let f1: AnimalToDog = (a) => new Dog(); // OK
let f2: DogToDog = f1; // OK: AnimalToDog is assignable to DogToDog
// because Dog (param of f2) extends Animal (param of f1)
```

---

## Covariant and Contravariant Properties

### Property Covariance

```typescript
class Event {
  timestamp = new Date();
}

class ClickEvent extends Event {
  x = 0;
  y = 0;
}

interface EventSource<out E extends Event> {
  latestEvent: E;  // Covariant: E in output position
}

declare const clickSource: EventSource<ClickEvent>;
const eventSource: EventSource<Event> = clickSource; // OK
```

### Method Parameter Contravariance

```typescript
class Processor {
  process(item: Animal): void {
    console.log(`Processing ${item.name}`);
  }
}

class DogProcessor extends Processor {
  // This is a wider method — takes any Animal, not just Dog
  // This is actually an error in strict mode because of contravariance
  // The correct approach:
  processDog(item: Dog): void {
    console.log(`Processing dog: ${item.name}, breed: ${item.breed}`);
  }
}
```

---

## SOLID Principles in TypeScript

### S — Single Responsibility Principle

```typescript
// BAD: Multiple responsibilities
class UserService {
  createUser() {}
  sendEmail() {}
  generateReport() {}
}

// GOOD: Single responsibility
class UserValidator {
  validate(user: CreateUserDTO): boolean { return true; }
}

class UserRepository {
  save(user: User): void { /* ... */ }
  findById(id: string): User | undefined { return undefined; }
}

class EmailNotifier {
  sendWelcome(email: string): Promise<void> { return Promise.resolve(); }
}

class UserService {
  constructor(
    private validator: UserValidator,
    private repository: UserRepository,
    private notifier: EmailNotifier
  ) {}

  async createUser(data: CreateUserDTO): Promise<User> {
    this.validator.validate(data);
    const user = { ...data, id: crypto.randomUUID() } as User;
    this.repository.save(user);
    await this.notifier.sendWelcome(user.email);
    return user;
  }
}
```

### O — Open/Closed Principle

```typescript
// Open for extension, closed for modification
interface DiscountStrategy {
  calculate(price: number): number;
  readonly name: string;
}

class NoDiscount implements DiscountStrategy {
  readonly name = "none";
  calculate(price: number): number { return price; }
}

class PercentageDiscount implements DiscountStrategy {
  constructor(private percentage: number) {}
  readonly name = `${this.percentage}% off`;
  calculate(price: number): number {
    return price * (1 - this.percentage / 100);
  }
}

class FixedDiscount implements DiscountStrategy {
  constructor(private amount: number) {}
  readonly name = `$${this.amount} off`;
  calculate(price: number): number {
    return Math.max(0, price - this.amount);
  }
}

// Adding new discount types doesn't require modifying existing code
class BuyOneGetOneFree implements DiscountStrategy {
  readonly name = "Buy 1 Get 1 Free";
  calculate(price: number): number { return price / 2; }
}

class PriceCalculator {
  calculate(price: number, discount: DiscountStrategy): number {
    return discount.calculate(price);
  }
}
```

### L — Liskov Substitution Principle

```typescript
// Good: Immutable shapes — always substitutable
interface Shape {
  area(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  area(): number { return Math.PI * this.radius ** 2; }
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  area(): number { return this.width * this.height; }
}

// Any function accepting Shape works with any implementation
function totalArea(shapes: Shape[]): number {
  return shapes.reduce((sum, s) => sum + s.area(), 0);
}
```

### I — Interface Segregation Principle

```typescript
// Segregated interfaces
interface Readable<T> {
  read(): Promise<T>;
}

interface Writable<T> {
  write(data: T): Promise<void>;
}

interface Deletable {
  delete(): Promise<boolean>;
}

// Read-only service
class ConfigService implements Readable<Config> {
  async read(): Promise<Config> { return {}; }
}

// Full CRUD
class UserService implements Readable<User>, Writable<User>, Deletable {
  async read(): Promise<User> { return {} as User; }
  async write(data: User): Promise<void> { /* ... */ }
  async delete(): Promise<boolean> { return true; }
}
```

### D — Dependency Inversion Principle

```typescript
// Abstractions
interface MessageBroker {
  publish(topic: string, message: any): Promise<void>;
  subscribe(topic: string, handler: (message: any) => void): void;
}

interface KeyValueStore {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
}

// High-level module depends on abstractions
class OrderService {
  constructor(
    private broker: MessageBroker,
    private cache: KeyValueStore
  ) {}

  async placeOrder(order: Order): Promise<void> {
    await this.cache.set(`order:${order.id}`, JSON.stringify(order));
    await this.broker.publish("orders", order);
  }
}

// Low-level modules implement abstractions
class RabbitMQBroker implements MessageBroker {
  async publish(topic: string, message: any): Promise<void> {
    // RabbitMQ implementation
  }

  subscribe(topic: string, handler: (message: any) => void): void {
    // RabbitMQ implementation
  }
}

class RedisStore implements KeyValueStore {
  async get(key: string): Promise<string | null> {
    // Redis implementation
    return null;
  }

  async set(key: string, value: string): Promise<void> {
    // Redis implementation
  }
}
```

---

## Interview Questions

### Q1: What is polymorphism in TypeScript?

**Answer:** Polymorphism is the ability of objects of different types to be treated through a uniform interface. TypeScript supports runtime polymorphism (method overriding), compile-time polymorphism (generics, overloading), and structural polymorphism (duck typing).

### Q2: What is the difference between compile-time and runtime polymorphism?

**Answer:** Compile-time polymorphism is resolved at compile time through generics and method overloading. Runtime polymorphism is resolved at runtime through method overriding — the actual method called depends on the object's real type, not its declared type.

### Q3: What is duck typing?

**Answer:** Duck typing is TypeScript's structural typing system: objects are compatible based on their shape (structure) rather than explicit type declarations. If an object has the required properties and methods, it satisfies the type, regardless of its class hierarchy.

### Q4: What are covariant and contravariant types?

**Answer:** Covariance means a subtype can be used where a supertype is expected (preserves subtyping direction). Contravariance reverses the direction — a supertype can be used where a subtype is expected. In TypeScript with `strictFunctionTypes`, function parameters are contravariant and return types are covariant.

### Q5: How does the SOLID principle apply to TypeScript?

**Answer:** SRP: Each class has one responsibility. OCP: Extend behavior via interfaces/abstract classes without modifying existing code. LSP: Subtypes must be substitutable for their base types. ISP: Use small, focused interfaces. DIP: Depend on abstractions, not concrete implementations.

### Q6: What is structural polymorphism?

**Answer:** Structural polymorphism uses TypeScript's structural type system to achieve polymorphism without explicit inheritance. Any object that has the required shape satisfies a type, enabling flexible and decoupled code.

---

**Next:** [09 - Composition Over Inheritance](./09-composition-over-inheritance.md)
