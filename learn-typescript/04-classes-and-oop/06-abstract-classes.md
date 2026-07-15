# 06 - Abstract Classes in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [The abstract Keyword](#the-abstract-keyword)
- [Abstract Methods](#abstract-methods)
- [Abstract Properties](#abstract-properties)
- [Abstract Class vs Interface](#abstract-class-vs-interface)
- [When to Use Abstract Classes](#when-to-use-abstract-classes)
- [Abstract Factory Pattern](#abstract-factory-pattern)
- [Template Method Pattern](#template-method-pattern)
- [Abstract Class with Generics](#abstract-class-with-generics)
- [Interview Questions](#interview-questions)

---

## Introduction

Abstract classes are classes that cannot be instantiated directly. They serve as base classes providing partial implementations and defining contracts (abstract methods/properties) that derived classes **must** implement. They combine the benefits of interfaces (contract enforcement) with the benefits of classes (code sharing).

---

## The abstract Keyword

The `abstract` keyword marks a class as non-instantiable and class members as requiring implementation in subclasses.

### Abstract Class Declaration

```typescript
abstract class Animal {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  abstract makeSound(): string;
  abstract move(): string;

  greet(): string {
    return `Hello, I'm ${this.name}`;
  }
}

// const animal = new Animal("Test"); // Error: Cannot create an instance of an abstract class
```

### Abstract Class with Constructor

```typescript
abstract class BaseComponent {
  protected id: string;
  protected createdAt: Date;

  constructor(id?: string) {
    this.id = id ?? crypto.randomUUID();
    this.createdAt = new Date();
  }

  abstract render(): string;

  getAge(): number {
    return Date.now() - this.createdAt.getTime();
  }
}

class Button extends BaseComponent {
  constructor(
    public label: string,
    public onClick: () => void
  ) {
    super();
  }

  render(): string {
    return `<button id="${this.id}">${this.label}</button>`;
  }
}
```

### Multiple Levels of Abstraction

```typescript
abstract class Vehicle {
  abstract start(): void;
  abstract stop(): void;
}

abstract class MotorizedVehicle extends Vehicle {
  protected engineOn = false;

  start(): void {
    this.startEngine();
    this.engineOn = true;
  }

  stop(): void {
    this.stopEngine();
    this.engineOn = false;
  }

  protected abstract startEngine(): void;
  protected abstract stopEngine(): void;
}

class Car extends MotorizedVehicle {
  protected startEngine(): void {
    console.log("Car engine started");
  }

  protected stopEngine(): void {
    console.log("Car engine stopped");
  }
}
```

---

## Abstract Methods

Abstract methods are method signatures without implementations that force derived classes to provide their own.

### Basic Abstract Methods

```typescript
abstract class Database {
  abstract connect(): Promise<void>;
  abstract disconnect(): Promise<void>;
  abstract query<T>(sql: string): Promise<T[]>;
  abstract execute(sql: string): Promise<void>;

  async withConnection<T>(fn: () => Promise<T>): Promise<T> {
    await this.connect();
    try {
      return await fn();
    } finally {
      await this.disconnect();
    }
  }
}

class PostgresDatabase extends Database {
  async connect(): Promise<void> {
    console.log("Connecting to PostgreSQL...");
  }

  async disconnect(): Promise<void> {
    console.log("Disconnecting from PostgreSQL...");
  }

  async query<T>(sql: string): Promise<T[]> {
    console.log(`Executing query: ${sql}`);
    return [] as T[];
  }

  async execute(sql: string): Promise<void> {
    console.log(`Executing: ${sql}`);
  }
}

class MongoDatabase extends Database {
  async connect(): Promise<void> {
    console.log("Connecting to MongoDB...");
  }

  async disconnect(): Promise<void> {
    console.log("Disconnecting from MongoDB...");
  }

  async query<T>(sql: string): Promise<T[]> {
    console.log(`Finding: ${sql}`);
    return [] as T[];
  }

  async execute(sql: string): Promise<void> {
    console.log(`Inserting: ${sql}`);
  }
}
```

### Abstract Methods with Parameters

```typescript
abstract class Validator<T> {
  abstract validate(value: T): boolean;
  abstract getErrorMessage(value: T): string;

  validateOrThrow(value: T): void {
    if (!this.validate(value)) {
      throw new Error(this.getErrorMessage(value));
    }
  }
}

class EmailValidator extends Validator<string> {
  private static EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  validate(value: string): boolean {
    return EmailValidator.EMAIL_REGEX.test(value);
  }

  getErrorMessage(value: string): string {
    return `"${value}" is not a valid email address`;
  }
}

class AgeValidator extends Validator<number> {
  validate(value: number): boolean {
    return value >= 0 && value <= 150;
  }

  getErrorMessage(value: number): string {
    return `Age must be between 0 and 150, got ${value}`;
  }
}
```

### Abstract Class with No Abstract Members

An abstract class can have zero abstract members. Its purpose is solely to prevent instantiation:

```typescript
abstract class UtilityClass {
  static helper(): string {
    return "help";
  }
}
```

---

## Abstract Properties

Abstract classes can declare abstract properties (accessors) that subclasses must implement.

### Abstract Accessors

```typescript
abstract class Vehicle {
  abstract get speed(): number;
  abstract set speed(value: number);
  abstract get isMoving(): boolean;

  accelerate(amount: number): void {
    this.speed = this.speed + amount;
  }

  brake(amount: number): void {
    this.speed = Math.max(0, this.speed - amount);
  }
}

class Car extends Vehicle {
  private _speed = 0;

  get speed(): number {
    return this._speed;
  }

  set speed(value: number) {
    this._speed = Math.max(0, value);
  }

  get isMoving(): boolean {
    return this._speed > 0;
  }
}
```

### Abstract Getters for Computed Values

```typescript
abstract class Shape {
  abstract get area(): number;
  abstract get perimeter(): number;
  abstract get type(): string;

  get description(): string {
    return `${this.type}: area=${this.area.toFixed(2)}, perimeter=${this.perimeter.toFixed(2)}`;
  }
}

class Circle extends Shape {
  constructor(private radius: number) {
    super();
  }

  get area(): number {
    return Math.PI * this.radius ** 2;
  }

  get perimeter(): number {
    return 2 * Math.PI * this.radius;
  }

  get type(): string {
    return "Circle";
  }
}
```

### Abstract vs Concrete Properties

```typescript
abstract class Base {
  abstract name: string;   // Must be overridden
  version = "1.0.0";      // Concrete shared
  readonly createdAt = new Date(); // Readonly concrete
  protected internalId = Math.random().toString(36); // Protected concrete
}

class Derived extends Base {
  name = "derived"; // Must implement abstract property
}
```

---

## Abstract Class vs Interface

| Feature | Abstract Class | Interface |
|---|---|---|
| Implementations | Yes | No |
| Constructors | Yes | No |
| State (property values) | Yes | No |
| Multiple inheritance | No (single extends) | Yes (multiple extends) |
| Runtime existence | Yes | No (erased) |
| Access modifiers | Yes | No |

### When to Use Which

```typescript
// Interface: contract without implementation
interface Serializable {
  serialize(): string;
}

interface Deserializable<T> {
  deserialize(data: string): T;
}

// Abstract class: shared implementation across subclasses
abstract class BaseRepository<T> {
  protected items: T[] = [];

  abstract findById(id: string): T | undefined;
  abstract findAll(): T[];

  add(item: T): void {
    this.items.push(item);
  }

  remove(item: T): void {
    this.items = this.items.filter(i => i !== item);
  }

  count(): number {
    return this.items.length;
  }
}
```

### Combining Both

```typescript
interface Loggable {
  log(message: string): void;
}

interface Serializable {
  serialize(): string;
}

abstract class BaseComponent implements Loggable, Serializable {
  abstract name: string;

  log(message: string): void {
    console.log(`[${this.name}] ${message}`);
  }

  serialize(): string {
    return JSON.stringify({ name: this.name });
  }
}
```

---

## When to Use Abstract Classes

### 1. Shared Implementation Across Related Classes

```typescript
abstract class Cache<T> {
  protected store = new Map<string, { value: T; expiry: number }>();

  abstract get(key: string): T | undefined;
  abstract set(key: string, value: T): void;

  has(key: string): boolean {
    const item = this.store.get(key);
    if (!item) return false;
    if (Date.now() > item.expiry) {
      this.store.delete(key);
      return false;
    }
    return true;
  }

  clear(): void {
    this.store.clear();
  }
}
```

### 2. Enforcing a Common Interface with Shared Logic

```typescript
abstract class EventSource<T> {
  private listeners: Array<(event: T) => void> = [];

  abstract getEvents(): T[];

  subscribe(listener: (event: T) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener);
    };
  }

  protected emit(event: T): void {
    this.listeners.forEach(listener => listener(event));
  }
}
```

### 3. Defining Skeleton Algorithms

```typescript
abstract class DataProcessor<TInput, TOutput> {
  abstract validate(input: TInput): boolean;
  abstract transform(input: TInput): TOutput;

  process(input: TInput): TOutput | null {
    if (!this.validate(input)) {
      console.error("Validation failed");
      return null;
    }
    return this.transform(input);
  }

  processAll(inputs: TInput[]): (TOutput | null)[] {
    return inputs.map(input => this.process(input));
  }
}
```

---

## Abstract Factory Pattern

The Abstract Factory pattern provides an interface for creating families of related objects without specifying concrete classes.

### Basic Abstract Factory

```typescript
abstract class Button {
  abstract render(): string;
  abstract onClick(handler: () => void): void;
}

abstract class Dialog {
  abstract open(): string;
  abstract close(): string;
  abstract addButton(button: Button): void;
}

class WindowsButton extends Button {
  render(): string {
    return "<windows-button/>";
  }
  onClick(handler: () => void): void {
    console.log("Windows button clicked");
  }
}

class LinuxButton extends Button {
  render(): string {
    return "<linux-button/>";
  }
  onClick(handler: () => void): void {
    console.log("Linux button clicked");
  }
}

class WindowsDialog extends Dialog {
  private buttons: Button[] = [];

  open(): string {
    return "Windows dialog opened";
  }

  close(): string {
    return "Windows dialog closed";
  }

  addButton(button: Button): void {
    this.buttons.push(button);
  }
}

class LinuxDialog extends Dialog {
  private buttons: Button[] = [];

  open(): string {
    return "Linux dialog opened";
  }

  close(): string {
    return "Linux dialog closed";
  }

  addButton(button: Button): void {
    this.buttons.push(button);
  }
}

// Abstract Factory
abstract class UIFactory {
  abstract createButton(): Button;
  abstract createDialog(): Dialog;
}

class WindowsUIFactory extends UIFactory {
  createButton(): Button {
    return new WindowsButton();
  }

  createDialog(): Dialog {
    return new WindowsDialog();
  }
}

class LinuxUIFactory extends UIFactory {
  createButton(): Button {
    return new LinuxButton();
  }

  createDialog(): Dialog {
    return new LinuxDialog();
  }
}

// Client code — depends only on abstract types
function buildUI(factory: UIFactory): void {
  const dialog = factory.createDialog();
  const button = factory.createButton();
  dialog.addButton(button);
  console.log(dialog.open());
  button.onClick(() => console.log("clicked"));
}
```

### Factory Registration Pattern

```typescript
abstract class Product {
  abstract name: string;
  abstract price: number;
}

class PhysicalProduct extends Product {
  constructor(
    public name: string,
    public price: number,
    public weight: number
  ) {
    super();
  }
}

class DigitalProduct extends Product {
  constructor(
    public name: string,
    public price: number,
    public downloadUrl: string
  ) {
    super();
  }
}

abstract class ProductFactory {
  private static factories = new Map<string, ProductFactory>();

  static register(type: string, factory: ProductFactory): void {
    ProductFactory.factories.set(type, factory);
  }

  static create(type: string, ...args: any[]): Product {
    const factory = ProductFactory.factories.get(type);
    if (!factory) {
      throw new Error(`No factory registered for type: ${type}`);
    }
    return factory.create(...args);
  }

  abstract create(...args: any[]): Product;
}
```

---

## Template Method Pattern

The Template Method pattern defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the algorithm's structure.

### Basic Template Method

```typescript
abstract class DataExporter {
  // Template method — defines the algorithm skeleton
  export(data: Record<string, any>[]): string {
    const validated = this.validate(data);
    const transformed = this.transform(validated);
    const formatted = this.format(transformed);
    this.postProcess(formatted);
    return formatted;
  }

  // Abstract steps — must be implemented by subclasses
  protected abstract validate(data: Record<string, any>[]): Record<string, any>[];
  protected abstract transform(data: Record<string, any>[]): Record<string, any>[];
  protected abstract format(data: Record<string, any>[]): string;

  // Hook — optional override
  protected postProcess(formatted: string): void {
    // Default: no-op
  }
}

class CSVExporter extends DataExporter {
  protected validate(data: Record<string, any>[]): Record<string, any>[] {
    return data.filter(row => Object.keys(row).length > 0);
  }

  protected transform(data: Record<string, any>[]): Record<string, any>[] {
    return data.map(row => {
      const transformed: Record<string, any> = {};
      for (const [key, value] of Object.entries(row)) {
        transformed[key] = String(value);
      }
      return transformed;
    });
  }

  protected format(data: Record<string, any>[]): string {
    if (data.length === 0) return "";
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map(row => Object.values(row).join(","));
    return [headers, ...rows].join("\n");
  }
}

class JSONExporter extends DataExporter {
  protected validate(data: Record<string, any>[]): Record<string, any>[] {
    return data;
  }

  protected transform(data: Record<string, any>[]): Record<string, any>[] {
    return data;
  }

  protected format(data: Record<string, any>[]): string {
    return JSON.stringify(data, null, 2);
  }

  protected postProcess(formatted: string): void {
    console.log("JSON export completed");
  }
}
```

### Template Method with Hook Methods

```typescript
abstract class GameAI {
  // Template method
  turn(): void {
    this.collectResources();
    this.buildStructures();
    this.trainUnits();
    this.attack();
    this.endTurn();
  }

  protected collectResources(): void {
    console.log("Collecting resources...");
  }

  protected buildStructures(): void {
    console.log("Building structures...");
  }

  // Hook methods — subclasses can optionally override
  protected trainUnits(): void {
    console.log("Training units...");
  }

  protected attack(): void {
    console.log("Attacking...");
  }

  protected endTurn(): void {
    console.log("Turn ended.");
  }
}

class AggressiveAI extends GameAI {
  protected override trainUnits(): void {
    console.log("Training ONLY offensive units!");
  }

  protected override attack(): void {
    console.log("Full-scale attack!");
  }
}

class DefensiveAI extends GameAI {
  protected override buildStructures(): void {
    console.log("Building walls and turrets!");
  }

  protected override attack(): void {
    console.log("Counter-attack only when provoked.");
  }
}
```

---

## Abstract Class with Generics

Abstract classes can be generic, allowing subclasses to specify concrete types.

### Generic Repository Pattern

```typescript
abstract class Repository<T, TId> {
  protected items: Map<TId, T> = new Map();

  abstract findById(id: TId): T | undefined;
  abstract findAll(): T[];
  abstract save(item: T): void;
  abstract delete(id: TId): boolean;

  exists(id: TId): boolean {
    return this.items.has(id);
  }

  count(): number {
    return this.items.size;
  }

  find(predicate: (item: T) => boolean): T | undefined {
    return this.findAll().find(predicate);
  }

  filter(predicate: (item: T) => boolean): T[] {
    return this.findAll().filter(predicate);
  }
}

interface User {
  id: string;
  name: string;
  email: string;
}

class InMemoryUserRepository extends Repository<User, string> {
  findById(id: string): User | undefined {
    return this.items.get(id);
  }

  findAll(): User[] {
    return Array.from(this.items.values());
  }

  save(user: User): void {
    this.items.set(user.id, user);
  }

  delete(id: string): boolean {
    return this.items.delete(id);
  }

  findByEmail(email: string): User | undefined {
    return this.find(user => user.email === email);
  }
}
```

### Generic Abstract Class with Constraints

```typescript
abstract class SortableCollection<T extends { compareTo(other: T): number }> {
  protected items: T[] = [];

  abstract add(item: T): void;

  sort(): T[] {
    return [...this.items].sort((a, b) => a.compareTo(b));
  }

  first(): T | undefined {
    return this.items[0];
  }

  last(): T | undefined {
    return this.items[this.items.length - 1];
  }
}

class Scoreboard extends SortableCollection<{ name: string; score: number; compareTo(other: any): number }> {
  add(item: { name: string; score: number; compareTo(other: any): number }): void {
    this.items.push(item);
  }
}
```

### Multi-Type Generic Abstract Class

```typescript
abstract class Mapper<TSource, TTarget> {
  abstract map(source: TSource): TTarget;
  abstract mapReverse(target: TTarget): TSource;

  mapArray(sources: TSource[]): TTarget[] {
    return sources.map(source => this.map(source));
  }

  mapArrayReverse(targets: TTarget[]): TSource[] {
    return targets.map(target => this.mapReverse(target));
  }
}

interface CreateUserDTO {
  name: string;
  email: string;
}

interface UserEntity {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

class UserMapper extends Mapper<CreateUserDTO, UserEntity> {
  private nextId = 1;

  map(dto: CreateUserDTO): UserEntity {
    return {
      id: this.nextId++,
      name: dto.name,
      email: dto.email,
      createdAt: new Date(),
    };
  }

  mapReverse(entity: UserEntity): CreateUserDTO {
    return {
      name: entity.name,
      email: entity.email,
    };
  }
}
```

---

## Interview Questions

### Q1: What is an abstract class in TypeScript?

**Answer:** An abstract class is a class that cannot be instantiated directly. It can contain both abstract members (methods/properties without implementation that subclasses must implement) and concrete members (with implementation that subclasses inherit). It serves as a blueprint for related classes.

### Q2: What is the difference between an abstract class and an interface?

**Answer:** Abstract classes can have implementations, constructors, state, and access modifiers. Interfaces define only contracts (types). Abstract classes use `extends`, interfaces use `implements`. A class can extend one abstract class but implement multiple interfaces. Interfaces are erased at runtime; abstract classes exist as functions.

### Q3: Can an abstract class have no abstract members?

**Answer:** Yes. An abstract class with no abstract members simply prevents instantiation while providing shared implementation. This is useful for base classes that should not be instantiated directly but provide common functionality.

### Q4: What is the Template Method pattern?

**Answer:** The Template Method pattern defines the skeleton of an algorithm in an abstract base class method (the template method), while deferring specific steps to subclasses. The template method calls abstract methods that subclasses must implement, and optional hook methods that subclasses can override.

### Q5: What is the Abstract Factory pattern?

**Answer:** The Abstract Factory pattern provides an interface for creating families of related objects without specifying concrete classes. An abstract factory class defines creation methods, and concrete factories implement them to produce specific product variants. This decouples client code from concrete implementations.

### Q6: Can abstract classes have static members?

**Answer:** Yes. Abstract classes can have static members. Static members belong to the class itself and are accessible without instantiation. This is useful for utility methods or constants shared across all subclasses.

### Q7: When should you choose an abstract class over an interface?

**Answer:** Choose an abstract class when you need to share implementation code among related classes, when you need constructors or access modifiers, or when you need to enforce a class hierarchy. Choose interfaces when defining pure contracts, when you need multiple inheritance of type, or when you want maximum flexibility.

---

**Next:** [07 - Interfaces in OOP](./07-interfaces-in-oop.md)
