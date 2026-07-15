# Interfaces in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Interface Declaration](#interface-declaration)
3. [Extending Interfaces](#extending-interfaces)
4. [Interface Inheritance](#interface-inheritance)
5. [Interface Merging](#interface-merging)
6. [Interface vs Type Alias](#interface-vs-type-alias)
7. [Function Interfaces](#function-interfaces)
8. [Indexable Interfaces](#indexable-interfaces)
9. [Implementing Interfaces in Classes](#implementing-interfaces-in-classes)
10. [Readonly Interfaces](#readonly-interfaces)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Overview

Interfaces define the **shape** of objects — describing what properties and methods an object must have. Interfaces are one of TypeScript's most powerful features for defining contracts.

```typescript
// Basic interface
interface User {
  name: string;
  age: number;
  email: string;
}

// Using the interface
const user: User = {
  name: "Alice",
  age: 30,
  email: "alice@example.com",
};

// Interface in function parameters
function greet(user: User): string {
  return `Hello, ${user.name}!`;
}

// Interface as return type
function getUser(): User {
  return {
    name: "Alice",
    age: 30,
    email: "alice@example.com",
  };
}
```

---

## Interface Declaration

```typescript
// Basic declaration
interface Point {
  x: number;
  y: number;
}

// With optional properties
interface Config {
  host: string;
  port: number;
  debug?: boolean; // optional
}

// With readonly properties
interface ImmutablePoint {
  readonly x: number;
  readonly y: number;
}

// With method signatures
interface Calculator {
  add(a: number, b: number): number;
  subtract(a: number, b: number): number;
  multiply(a: number, b: number): number;
}

// With call signatures
interface Formatter {
  (value: number): string;
  (value: Date): string;
}

// With construct signatures
interface ClockConstructor {
  new (hour: number, minute: number): ClockInterface;
}

interface ClockInterface {
  tick(): void;
}

// With index signatures
interface StringDictionary {
  [key: string]: string;
  length: number; // Must be compatible with index signature
}

// With nested interfaces
interface Company {
  name: string;
  address: {
    street: string;
    city: string;
    country: string;
  };
  departments: Department[];
}

interface Department {
  name: string;
  headcount: number;
}

// Generic interfaces
interface Repository<T> {
  findById(id: string): T | null;
  findAll(): T[];
  create(item: T): T;
  update(id: string, item: Partial<T>): T;
  delete(id: string): boolean;
}

// Generic interface with constraints
interface Sortable<T extends { compareTo(other: T): number }> {
  items: T[];
  sort(): T[];
}
```

---

## Extending Interfaces

```typescript
// Basic extends
interface Animal {
  name: string;
  age: number;
}

interface Dog extends Animal {
  breed: string;
  bark(): void;
}

// Using extended interface
const dog: Dog = {
  name: "Rex",
  age: 5,
  breed: "German Shepherd",
  bark() {
    console.log("Woof!");
  },
};

// Multiple extends
interface Printable {
  print(): void;
}

interface Serializable {
  serialize(): string;
}

interface Document extends Printable, Serializable {
  title: string;
  content: string;
}

// Using multiply extended interface
const doc: Document = {
  title: "My Doc",
  content: "Hello world",
  print() {
    console.log(this.content);
  },
  serialize() {
    return JSON.stringify(this);
  },
};

// Extending with overrides (narrowing)
interface Base {
  value: string;
}

interface Extended extends Base {
  value: string | number; // Allowed: widening
  extra: boolean;
}

// Interface extending a generic interface
interface Container<T> {
  value: T;
}

interface NumberContainer extends Container<number> {
  format(): string;
}

const numContainer: NumberContainer = {
  value: 42,
  format() {
    return this.value.toFixed(2);
  },
};

// Deep extension
interface A {
  x: number;
}

interface B extends A {
  y: number;
}

interface C extends B {
  z: number;
}

const point: C = { x: 1, y: 2, z: 3 };
```

---

## Interface Inheritance

```typescript
// Inheritance chain
interface Shape {
  area(): number;
  perimeter(): number;
}

interface Circle extends Shape {
  radius: number;
}

interface ColoredCircle extends Circle {
  color: string;
}

const coloredCircle: ColoredCircle = {
  radius: 10,
  color: "red",
  area() {
    return Math.PI * this.radius ** 2;
  },
  perimeter() {
    return 2 * Math.PI * this.radius;
  },
};

// Inheritance with generic types
interface EventEmitter<T> {
  on(event: string, handler: (data: T) => void): void;
  emit(event: string, data: T): void;
}

interface TypedEventEmitter<T, U> extends EventEmitter<T> {
  on(event: string, handler: (data: T) => void): void;
  on(event: string, handler: (data: U) => void): void;
  emit(event: string, data: T | U): void;
}

// Using inherited interface
const emitter: TypedEventEmitter<string, number> = {
  on(event, handler) {},
  emit(event, data) {},
};

// Inheritance vs composition
// Inheritance: Dog extends Animal (IS-A relationship)
// Composition: Dog has-a Tail (HAS-A relationship)

interface Tail {
  length: number;
  wag(): void;
}

interface Dog2 extends Animal {
  breed: string;
  tail: Tail; // Composition
}
```

---

## Interface Merging

Declaration merging allows you to extend existing interfaces by redeclaring them.

```typescript
// Basic declaration merging
interface User {
  name: string;
}

interface User {
  age: number;
}

// Merged result: { name: string; age: number }
const user: User = { name: "Alice", age: 30 };

// Merging with different member kinds
interface User2 {
  name: string;
}

interface User2 {
  greet(): string; // Method
}

interface User2 {
  age: number; // Property
}

// Merged: { name: string; greet(): string; age: number }

// ⚠️ Merging with conflicting types is an error
interface Bad {
  value: string;
}

interface Bad {
  value: number; // Error: Subsequent property declaration must have type
}

// Merging with optional vs required
interface Config {
  host: string;
}

interface Config {
  port?: number; // Optional
}

// Merged: { host: string; port?: number }

// Merging with readonly
interface Immutable {
  readonly id: number;
}

interface Immutable {
  name: string; // Not readonly
}

// Merged: { readonly id: number; name: string }

// Merging with index signatures
interface Dict {
  [key: string]: string;
}

interface Dict {
  length: number; // Must be compatible with string index
}

// Real-world: augmenting existing interfaces
// Extending Window interface
interface Window {
  myCustomProperty: string;
}

// Now window.myCustomProperty is typed

// Extending Express Request
// interface Request {
//   user?: { id: string; name: string };
// }

// Merging in libraries
// Declaration merging is used extensively in libraries like Express, React, etc.
```

---

## Interface vs Type Alias

| Feature | Interface | Type Alias |
|---------|-----------|------------|
| Declaration merging | ✅ Yes | ❌ No |
| Extends | ✅ Yes (`extends`) | ✅ Yes (`&` intersection) |
| Implements in classes | ✅ Yes | ❌ No |
| Computed properties | ❌ No | ✅ Yes |
| Union types | ❌ No | ✅ Yes |
| Tuple types | ❌ No | ✅ Yes |
| Mapping/primitive types | ❌ No | ✅ Yes |
| Error messages | Better for objects | Worse for complex types |
| Performance | Slightly better | Slightly worse |

```typescript
// Interface: can be merged
interface User { name: string; }
interface User { age: number; }
// OK: { name: string; age: number }

// Type alias: cannot be merged
type User2 = { name: string; };
// type User2 = { age: number; }; // Error: Duplicate identifier

// Interface: can extend
interface Animal { name: string; }
interface Dog extends Animal { breed: string; }

// Type alias: uses intersection
type Animal2 = { name: string; };
type Dog2 = Animal2 & { breed: string; };

// Interface: can be implemented in classes
interface Printable { print(): void; }
class Document implements Printable {
  print() { console.log("printing"); }
}

// Type alias: cannot be implemented in classes
type Printable2 = { print(): void; };
// class Doc implements Printable2 {} // Error

// Type alias: can create unions
type StringOrNumber = string | number;
// interface cannot do this

// Type alias: can create tuples
type Pair = [string, number];
// interface cannot do this

// Type alias: can use computed properties
type PropName = "name" | "age";
type Obj = { [K in PropName]: string };
// interface cannot do this
```

---

## Function Interfaces

```typescript
// Interface with call signature
interface SearchFunc {
  (source: string, subString: string): boolean;
}

const search: SearchFunc = (source, subString) => {
  return source.includes(subString);
};

// Generic function interface
interface Transform<T, U> {
  (input: T): U;
}

const stringToNumber: Transform<string, number> = (s) => parseInt(s);
const numberToString: Transform<number, string> = (n) => n.toString();

// Interface with overloads
interface OverloadedFunc {
  (x: string): string;
  (x: number): number;
  (x: boolean): boolean;
}

// Interface for class constructor
interface ClockConstructor {
  new (hour: number, minute: number): Clock;
}

interface Clock {
  tick(): void;
}

function createClock(ctor: ClockConstructor, hour: number, minute: number): Clock {
  return new ctor(hour, minute);
}

// Interface for event handlers
interface EventHandler<T = Event> {
  (event: T): void;
}

interface EventTarget {
  addEventListener(type: string, handler: EventHandler): void;
  removeEventListener(type: string, handler: EventHandler): void;
}

// Interface for middleware
interface Middleware<T> {
  (context: T, next: () => Promise<void>): Promise<void>;
}

// Interface for validators
interface Validator<T> {
  validate(value: T): boolean;
  message: string;
}
```

---

## Indexable Interfaces

```typescript
// String indexable
interface StringMap {
  [index: string]: string;
}

const dict: StringMap = { key: "value" };

// Number indexable
interface NumberIndexed {
  [index: number]: string;
}

const arr: NumberIndexed = ["a", "b", "c"];

// Combined indexable
interface Both {
  [key: string]: string | number;
  [index: number]: string; // Must be subtype of string index
}

// Readonly indexable
interface ReadonlyDict {
  readonly [key: string]: string;
}

// Indexable with known properties
interface Dictionary {
  [key: string]: unknown;
  length: number;
  push(item: unknown): void;
}

// Class-like interface with indexable
interface List<T> {
  [index: number]: T;
  length: number;
  push(item: T): void;
  pop(): T | undefined;
}

// Real-world: typed event emitter
interface EventMap {
  [event: string]: (...args: any[]) => void;
}

interface TypedEmitter<Events extends EventMap> {
  on<K extends keyof Events>(event: K, handler: Events[K]): void;
  emit<K extends keyof Events>(event: K, ...args: Parameters<Events[K]>): void;
}

interface MyEvents extends EventMap {
  click: (x: number, y: number) => void;
  keydown: (key: string) => void;
}
```

---

## Implementing Interfaces in Classes

```typescript
// Basic implementation
interface Animal {
  name: string;
  speak(): string;
}

class Dog implements Animal {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  speak(): string {
    return `${this.name} says Woof!`;
  }
}

// Implementing multiple interfaces
interface Printable {
  print(): string;
}

interface Serializable {
  serialize(): string;
}

class User implements Printable, Serializable {
  constructor(public name: string, public age: number) {}

  print(): string {
    return `User: ${this.name}, Age: ${this.age}`;
  }

  serialize(): string {
    return JSON.stringify({ name: this.name, age: this.age });
  }
}

// Generic class implementing generic interface
interface Repository<T> {
  findById(id: string): T | null;
  findAll(): T[];
  create(item: T): T;
}

class InMemoryRepository<T extends { id: string }> implements Repository<T> {
  private items: T[] = [];

  findById(id: string): T | null {
    return this.items.find((item) => item.id === id) ?? null;
  }

  findAll(): T[] {
    return [...this.items];
  }

  create(item: T): T {
    this.items.push(item);
    return item;
  }
}

interface User2 {
  id: string;
  name: string;
}

class UserRepository extends InMemoryRepository<User2> {}

// Implementing with access modifiers
interface Component {
  render(): string;
  destroy(): void;
}

class UIComponent implements Component {
  private destroyed = false;

  constructor(private name: string) {}

  render(): string {
    if (this.destroyed) throw new Error("Component destroyed");
    return `<${this.name}/>`;
  }

  destroy(): void {
    this.destroyed = true;
  }
}
```

---

## Readonly Interfaces

```typescript
// All properties readonly
interface ImmutableUser {
  readonly name: string;
  readonly age: number;
  readonly email: string;
}

const user: ImmutableUser = {
  name: "Alice",
  age: 30,
  email: "alice@example.com",
};

// user.name = "Bob"; // Error: readonly

// Partially readonly
interface PartiallyImmutable {
  readonly id: number;
  name: string; // mutable
  readonly email: string;
}

// Readonly<T> utility type
interface MutableUser {
  name: string;
  age: number;
  email: string;
}

type ImmutableMutableUser = Readonly<MutableUser>;
// All properties become readonly

// ReadonlyArray in interfaces
interface DataStore<T> {
  readonly items: T[];
  readonly size: number;
}

// Readonly with nested objects
interface DeepImmutable {
  readonly config: {
    readonly host: string;
    readonly port: number;
  };
}

// Practical: immutable API response
interface APIResponse<T> {
  readonly data: T;
  readonly status: number;
  readonly timestamp: number;
  readonly meta?: {
    readonly page: number;
    readonly total: number;
  };
}
```

---

## Best Practices

1. **Use interfaces for object shapes** that may be extended or implemented
2. **Use interfaces for public APIs** — they produce better error messages
3. **Use declaration merging** to augment existing interfaces (e.g., Express Request)
4. **Use generic interfaces** for reusable data structures
5. **Name interfaces with nouns** (User, Product, Config) — not verbs
6. **Keep interfaces small** — prefer composition over deep inheritance
7. **Use `extends`** for inheritance, not `&` intersection (for objects)
8. **Use `readonly`** for immutable data in interfaces
9. **Use index signatures** when keys are dynamic and known
10. **Document interface contracts** — JSDoc comments for public interfaces

---

## Interview Questions

### Q1: What is an interface in TypeScript?

**Answer:** An interface defines the shape of an object — describing what properties and methods it must have. Interfaces create a contract that objects must follow. They support declaration merging, inheritance via `extends`, and can be implemented by classes.

### Q2: Can you extend multiple interfaces?

**Answer:** Yes. `interface C extends A, B {}` inherits all members from both A and B. If there are conflicting member types, TypeScript will report an error.

### Q3: What is declaration merging?

**Answer:** A feature where multiple interface declarations with the same name are automatically merged into a single interface. This is useful for augmenting third-party types (e.g., adding properties to Express Request).

### Q4: When should you use an interface over a type alias?

**Answer:** Use interfaces when you need declaration merging, when the type will be implemented by classes, or when defining object shapes in public APIs. Use type aliases for unions, tuples, mapped types, and computed properties.

### Q5: Can an interface have a construct signature?

**Answer:** Yes. `interface ClockConstructor { new (hour: number, minute: number): Clock; }` defines the shape of a class constructor. You can pass classes as values matching this interface.
