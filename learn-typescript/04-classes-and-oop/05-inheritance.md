# 05 - Inheritance in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [The `extends` Keyword](#the-extends-keyword)
- [The `super` Constructor](#the-super-constructor)
- [Overriding Methods](#overriding-methods)
- [Property Inheritance](#property-inheritance)
- [Constructor Chaining](#constructor-chaining)
- [Single Inheritance Limitation](#single-inheritance-limitation)
- [Types of Inheritance](#types-of-inheritance)
- [Liskov Substitution Principle](#liskov-substitution-principle)
- [Interview Questions](#interview-questions)

---

## Introduction

Inheritance is one of the four pillars of object-oriented programming. It allows a class (child/subclass/derived class) to inherit properties and methods from another class (parent/superclass/base class). TypeScript supports single inheritance using the `extends` keyword.

Inheritance promotes code reuse and establishes an "IS-A" relationship between classes:

- A `Dog` **IS-A** `Animal`
- A `Circle` **IS-A** `Shape`
- A `SavingsAccount` **IS-A** `BankAccount`

---

## The `extends` Keyword

The `extends` keyword establishes an inheritance relationship between two classes.

### Basic Inheritance

```typescript
class Animal {
  name: string;
  sound: string;

  constructor(name: string, sound: string) {
    this.name = name;
    this.sound = sound;
  }

  speak(): string {
    return `${this.name} says ${this.sound}`;
  }

  move(): string {
    return `${this.name} moves`;
  }
}

class Dog extends Animal {
  breed: string;

  constructor(name: string, breed: string) {
    super(name, "Woof");
    this.breed = breed;
  }

  fetch(item: string): string {
    return `${this.name} fetches the ${item}`;
  }
}

class Cat extends Animal {
  constructor(name: string) {
    super(name, "Meow");
  }

  purr(): string {
    return `${this.name} purrs`;
  }
}

const dog = new Dog("Buddy", "Labrador");
console.log(dog.speak());     // "Buddy says Woof" — inherited from Animal
console.log(dog.move());      // "Buddy moves" — inherited from Animal
console.log(dog.fetch("ball")); // "Buddy fetches the ball" — Dog's own method

const cat = new Cat("Whiskers");
console.log(cat.speak());     // "Whiskers says Meow"
console.log(cat.purr());      // "Whiskers purrs"
```

### What Gets Inherited

Everything from the parent class is inherited, **except**:
1. Constructors (you must call `super()` to initialize the parent)
2. Private members (accessible only within the defining class)
3. Static members are inherited but shadowed, not overridden polymorphically

```typescript
class Base {
  public publicProp = "public";
  protected protectedProp = "protected";
  private privateProp = "private"; // NOT accessible in child

  publicMethod() { return "public method"; }
  protectedMethod() { return "protected method"; }
  privateMethod() { return "private method"; } // NOT accessible in child
}

class Child extends Base {
  demo() {
    console.log(this.publicProp);     // OK
    console.log(this.protectedProp);  // OK
    // console.log(this.privateProp);  // Error: private
    console.log(this.publicMethod());  // OK
    console.log(this.protectedMethod()); // OK
    // console.log(this.privateMethod()); // Error: private
  }
}
```

### Multi-Level Inheritance

```typescript
class LivingThing {
  isAlive = true;

  breathe(): string {
    return "Breathing...";
  }
}

class Animal extends LivingThing {
  name: string;

  constructor(name: string) {
    super();
    this.name = name;
  }

  move(): string {
    return `${this.name} moves`;
  }
}

class Dog extends Animal {
  breed: string;

  constructor(name: string, breed: string) {
    super(name);
    this.breed = breed;
  }

  bark(): string {
    return `${this.name} barks`;
  }
}

const dog = new Dog("Rex", "German Shepherd");
console.log(dog.breathe());  // "Breathing..." — from LivingThing
console.log(dog.move());     // "Rex moves" — from Animal
console.log(dog.bark());     // "Rex barks" — from Dog
console.log(dog.isAlive);    // true — from LivingThing
```

---

## The `super` Constructor

The `super()` call in a constructor invokes the parent class's constructor. It **must** be called before accessing `this` in the child constructor.

### Basic super() Usage

```typescript
class Person {
  constructor(
    public name: string,
    public age: number
  ) {
    console.log(`Person constructor called for ${name}`);
  }
}

class Student extends Person {
  constructor(
    name: string,
    age: number,
    public school: string
  ) {
    super(name, age); // MUST call super() before using 'this'
    console.log(`Student constructor called for ${name}`);
  }
}

const student = new Student("Alice", 20, "MIT");
// Output:
// "Person constructor called for Alice"
// "Student constructor called for Alice"
```

### super() with Default Parameters

```typescript
class Base {
  value: number;

  constructor(value: number = 10) {
    this.value = value;
  }
}

class Child extends Base {
  constructor(value?: number) {
    super(value); // Pass through to parent, using its default if undefined
  }
}

const child1 = new Child();     // value = 10 (parent default)
const child2 = new Child(42);   // value = 42
```

### super() Must Be Called Before `this`

```typescript
class Base {
  x = 10;
}

class Child extends Base {
  constructor() {
    // this.y = 5;          // Error: 'this' cannot be accessed before 'super()'
    super();                // OK: super() called first
    this.y = 5;             // Now 'this' is available
  }

  y: number = 0;
}
```

---

## Overriding Methods

A child class can override a parent class's method to provide specialized behavior.

### Basic Method Overriding

```typescript
class Shape {
  constructor(public color: string) {}

  area(): number {
    return 0; // Base implementation
  }

  describe(): string {
    return `A ${this.color} shape with area ${this.area()}`;
  }
}

class Circle extends Shape {
  constructor(color: string, public radius: number) {
    super(color);
  }

  // Override area()
  area(): number {
    return Math.PI * this.radius ** 2;
  }
}

class Rectangle extends Shape {
  constructor(color: string, public width: number, public height: number) {
    super(color);
  }

  // Override area()
  area(): number {
    return this.width * this.height;
  }
}

class Triangle extends Shape {
  constructor(
    color: string,
    public base: number,
    public height: number
  ) {
    super(color);
  }

  // Override area()
  area(): number {
    return (this.base * this.height) / 2;
  }
}

const shapes: Shape[] = [
  new Circle("red", 5),
  new Rectangle("blue", 4, 6),
  new Triangle("green", 3, 8),
];

shapes.forEach(shape => {
  console.log(shape.describe());
});
// "A red shape with area 78.53981633974483"
// "A blue shape with area 24"
// "A green shape with area 12"
```

### Using `super.method()` to Extend (Not Replace)

```typescript
class Logger {
  log(message: string): void {
    console.log(`[LOG] ${message}`);
  }
}

class TimestampedLogger extends Logger {
  log(message: string): void {
    const timestamp = new Date().toISOString();
    super.log(`[${timestamp}] ${message}`); // Call parent's log
  }
}

class FileLogger extends TimestampedLogger {
  log(message: string): void {
    super.log(message); // Call parent's log (which adds timestamp)
    // Also write to file
    console.log(`  → Written to log file`);
  }
}

const logger = new FileLogger();
logger.log("Application started");
// "[LOG] [2024-01-15T10:30:00.000Z] Application started"
// "  → Written to log file"
```

### The `override` Keyword (TypeScript 4.3+)

TypeScript 4.3 introduced the `override` keyword to make method overriding explicit and safer:

```typescript
class Base {
  greet(): string {
    return "Hello from Base";
  }
}

class Child extends Base {
  override greet(): string {  // Explicitly marks this as an override
    return "Hello from Child";
  }

  // override nonExistent(): void {} // Error: This member cannot have an 'override' modifier
}

// Enable with tsconfig:
// { "compilerOptions": { "noImplicitOverride": true } }
```

### Preventing Override with `sealed` (Nonexistent in TS, but...)

TypeScript doesn't have a `sealed` keyword for classes, but you can prevent method overriding by:

```typescript
class Final {
  // Not truly sealed — just a convention
  method(): string {
    return "final";
  }
}

// TypeScript doesn't support final/sealed classes
// The equivalent in TS is to not use 'extends'
```

---

## Property Inheritance

All instance properties from the parent class are inherited by child classes.

### Property Inheritance with Initializers

```typescript
class Base {
  x = 10;
  y = "hello";
}

class Child extends Base {
  z = true;
}

const child = new Child();
console.log(child.x);  // 10
console.log(child.y);  // "hello"
console.log(child.z);  // true
```

### Overriding Property Initializers

```typescript
class Animal {
  legs = 4;
}

class Spider extends Animal {
  legs = 8; // Overrides Animal's default
}

class Bird extends Animal {
  legs = 2; // Overrides Animal's default
}
```

### Overriding Property Accessors

```typescript
class Base {
  private _value = 0;

  get value(): number {
    return this._value;
  }

  set value(v: number) {
    this._value = v;
  }
}

class Child extends Base {
  // Override getter and setter
  get value(): number {
    return super.value * 2;
  }

  set value(v: number) {
    super.value = v / 2;
  }
}

const child = new Child();
child.value = 10;
console.log(child.value); // 20 (set 10 → stored as 5, get returns 5*2)
```

---

## Constructor Chaining

Constructor chaining is the process of calling parent constructors up the inheritance chain. In TypeScript, this is done explicitly with `super()`.

### Basic Chaining

```typescript
class A {
  constructor() {
    console.log("A constructor");
  }
}

class B extends A {
  constructor() {
    super(); // Calls A's constructor
    console.log("B constructor");
  }
}

class C extends B {
  constructor() {
    super(); // Calls B's constructor, which calls A's constructor
    console.log("C constructor");
  }
}

new C();
// Output:
// "A constructor"
// "B constructor"
// "C constructor"
```

### Chaining with Parameters

```typescript
class Vehicle {
  constructor(
    public type: string,
    public wheels: number
  ) {
    console.log(`Vehicle: ${type} with ${wheels} wheels`);
  }
}

class Car extends Vehicle {
  constructor(
    public make: string,
    public model: string
  ) {
    super("Car", 4);
    console.log(`Car: ${make} ${model}`);
  }
}

class Truck extends Vehicle {
  constructor(
    public make: string,
    public payloadCapacity: number
  ) {
    super("Truck", 6);
    console.log(`Truck: ${make} with ${payloadCapacity}kg capacity`);
  }
}

new Car("Toyota", "Camry");
// "Vehicle: Car with 4 wheels"
// "Car: Toyota Camry"
```

### Chaining with Complex Initialization

```typescript
class BaseRepository<T> {
  protected items: T[] = [];

  constructor(protected tableName: string) {
    console.log(`Repository initialized for ${tableName}`);
  }

  protected seed(): void {
    console.log(`Seeding ${this.tableName}...`);
  }
}

class UserRepository extends BaseRepository<{ id: string; name: string }> {
  private index: Map<string, { id: string; name: string }> = new Map();

  constructor() {
    super("users");
    this.seed();
    this.buildIndex();
  }

  private buildIndex(): void {
    for (const item of this.items) {
      this.index.set(item.id, item);
    }
  }

  findById(id: string) {
    return this.index.get(id);
  }
}
```

---

## Single Inheritance Limitation

TypeScript (like JavaScript) supports only **single inheritance** — a class can extend only one parent class. This is a deliberate design decision to avoid the "diamond problem."

### The Problem Multiple Inheritance Solves

```typescript
// This is NOT possible in TypeScript
// class FlyingSwimmingCreature extends Bird, Fish {}
```

### Alternative: Interfaces for Multiple Contracts

```typescript
interface Flyable {
  fly(): string;
}

interface Swimmable {
  swim(): string;
}

interface Walkable {
  walk(): string;
}

class Duck implements Flyable, Swimmable, Walkable {
  fly(): string { return "Duck flies"; }
  swim(): string { return "Duck swims"; }
  walk(): string { return "Duck walks"; }
}

class Penguin implements Swimmable, Walkable {
  fly(): string { return "Penguin cannot fly"; } // Penguin doesn't implement Flyable
  swim(): string { return "Penguin swims"; }
  walk(): string { return "Penguin waddles"; }
}
```

### Alternative: Composition

```typescript
class FlyingBehavior {
  fly(): string {
    return "Flying high!";
  }
}

class SwimmingBehavior {
  swim(): string {
    return "Swimming fast!";
  }
}

class Duck {
  private flying = new FlyingBehavior();
  private swimming = new SwimmingBehavior();

  fly(): string { return this.flying.fly(); }
  swim(): string { return this.swimming.swim(); }
}
```

---

## Types of Inheritance

### Implementation Inheritance (extends)

A child class inherits and can override the parent's method implementations:

```typescript
class Base {
  doWork(): string {
    return "Base implementation";
  }
}

class Child extends Base {
  override doWork(): string {
    return "Child implementation";
  }
}
```

### Interface Inheritance (extends interface)

An interface can extend one or more interfaces:

```typescript
interface Shape {
  area(): number;
  perimeter(): number;
}

interface ColoredShape extends Shape {
  color: string;
}

interface ResizableShape extends Shape {
  scale(factor: number): void;
}

class ColoredResizableCircle implements ColoredShape, ResizableShape {
  constructor(public color: string, private radius: number) {}

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  perimeter(): number {
    return 2 * Math.PI * this.radius;
  }

  scale(factor: number): void {
    this.radius *= factor;
  }
}
```

### Abstract Class Inheritance

Abstract classes provide a mix of implementation and contract:

```typescript
abstract class Repository<T> {
  protected items: T[] = [];

  abstract findById(id: string): T | undefined;
  abstract findAll(): T[];

  add(item: T): void {
    this.items.push(item);
  }

  count(): number {
    return this.items.length;
  }
}

class UserRepository extends Repository<{ id: string; name: string }> {
  findById(id: string) {
    return this.items.find(item => item.id === id);
  }

  findAll() {
    return [...this.items];
  }
}
```

---

## Liskov Substitution Principle (LSP)

The Liskov Substitution Principle states that objects of a subclass should be replaceable with objects of the superclass without breaking the application.

### The Classic Example: Square and Rectangle

```typescript
// BAD: Violates LSP
class Rectangle {
  constructor(
    protected width: number,
    protected height: number
  ) {}

  setWidth(width: number): void {
    this.width = width;
  }

  setHeight(height: number): void {
    this.height = height;
  }

  getArea(): number {
    return this.width * this.height;
  }
}

class Square extends Rectangle {
  constructor(side: number) {
    super(side, side);
  }

  // This breaks the Rectangle contract!
  override setWidth(width: number): void {
    this.width = width;
    this.height = width; // Square must maintain equal sides
  }

  override setHeight(height: number): void {
    this.width = height;
    this.height = height;
  }
}

function increaseRectangleWidth(rect: Rectangle): void {
  rect.setWidth(rect["width"] + 1); // Accessing protected for demonstration
}

const rect = new Rectangle(10, 20);
increaseRectangleWidth(rect);
console.log(rect.getArea()); // 220 — Expected ✓

const square = new Square(10);
increaseRectangleWidth(square);
console.log(square.getArea()); // 121 — Unexpected! (11 * 11, not 10 * 11)
// Square is NOT a proper substitute for Rectangle here
```

### Correct LSP Implementation

```typescript
// GOOD: Follows LSP
interface Shape {
  area(): number;
  clone(): Shape;
}

class Rectangle implements Shape {
  constructor(
    private readonly width: number,
    private readonly height: number
  ) {}

  area(): number {
    return this.width * this.height;
  }

  clone(): Rectangle {
    return new Rectangle(this.width, this.height);
  }
}

class Square implements Shape {
  constructor(private readonly side: number) {}

  area(): number {
    return this.side ** 2;
  }

  clone(): Square {
    return new Square(this.side);
  }
}

class Circle implements Shape {
  constructor(private readonly radius: number) {}

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  clone(): Circle {
    return new Circle(this.radius);
  }
}

// Now any Shape can be substituted without surprises
function printArea(shape: Shape): void {
  console.log(`Area: ${shape.area()}`);
}

function doubleArea(shape: Shape): Shape {
  // For immutable shapes, we create a new one
  // This works correctly for ALL shapes
  const clone = shape.clone();
  // Implementation depends on specific shape
  return clone;
}
```

### LSP Rules

1. **Preconditions** cannot be strengthened in a subtype
2. **Postconditions** cannot be weakened in a subtype
3. **Invariants** of the supertype must be preserved in the subtype
4. **History constraint** (the "history rule"): The subtype should not allow state changes that the supertype doesn't allow

### Practical LSP in TypeScript

```typescript
// BAD: LSP Violation
class BaseProcessor {
  process(data: string): string {
    return data.toUpperCase();
  }
}

class StrictProcessor extends BaseProcessor {
  process(data: string): string {
    if (data.length === 0) {
      throw new Error("Empty data not allowed"); // Strengthened precondition!
    }
    return data.toUpperCase();
  }
}

function useProcessor(processor: BaseProcessor): void {
  const result = processor.process(""); // Might throw if StrictProcessor!
}

// GOOD: LSP Compliant
class FlexibleProcessor extends BaseProcessor {
  process(data: string): string {
    if (data.length === 0) {
      return ""; // Weakened postcondition for empty — doesn't throw
    }
    return data.toUpperCase();
  }
}
```

---

## Best Practices for Inheritance

### 1. Favor Composition Over Inheritance

```typescript
// Prefer this:
class Logger {
  private formatter = new MessageFormatter();
  private transport = new ConsoleTransport();

  log(message: string): void {
    const formatted = this.formatter.format(message);
    this.transport.send(formatted);
  }
}

// Over this:
class Logger extends MessageFormatter extends ConsoleTransport { /* ... */ }
```

### 2. Use `override` Keyword

Enable `noImplicitOverride` in tsconfig and use `override` explicitly:

```typescript
class Child extends Base {
  override method(): void { /* ... */ }
}
```

### 3. Keep Inheritance Hierarchies Shallow

```typescript
// Bad: Deep hierarchy
class A {}
class B extends A {}
class C extends B {}
class D extends C {}  // Too deep

// Good: Flat hierarchy + composition
class Base {}
class Feature1 { /* ... */ }
class Feature2 { /* ... */ }

class Combined extends Base {
  private feature1 = new Feature1();
  private feature2 = new Feature2();
}
```

### 4. Design for Substitution (LSP)

```typescript
// Ensure subclasses can be used wherever the parent is expected
abstract class PaymentProcessor {
  abstract processPayment(amount: number): Promise<PaymentResult>;
}

class StripeProcessor extends PaymentProcessor {
  async processPayment(amount: number): Promise<PaymentResult> {
    // Stripe implementation — no surprises for callers
    return { success: true, transactionId: "stripe_123" };
  }
}

class PayPalProcessor extends PaymentProcessor {
  async processPayment(amount: number): Promise<PaymentResult> {
    // PayPal implementation — same contract
    return { success: true, transactionId: "paypal_456" };
  }
}
```

---

## Interview Questions

### Q1: What is inheritance in TypeScript?

**Answer:** Inheritance is a mechanism where a child class extends a parent class, inheriting its properties and methods. TypeScript supports single inheritance using the `extends` keyword. The child class can override parent methods and add new members.

### Q2: Why does TypeScript not support multiple inheritance?

**Answer:** TypeScript (JavaScript) avoids multiple inheritance to prevent the "diamond problem" — where a class inherits from two classes that have conflicting implementations of the same method. Instead, TypeScript uses interfaces and mixins to achieve similar functionality.

### Q3: What is the Liskov Substitution Principle?

**Answer:** LSP states that objects of a subclass should be substitutable for objects of a superclass without breaking the program. If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without altering the correctness of the program.

### Q4: When should you use inheritance vs composition?

**Answer:** Use inheritance when there's a clear "IS-A" relationship and the subclass truly is a specialization of the parent. Use composition when there's a "HAS-A" relationship or when you need to combine behaviors from multiple sources. Composition is generally more flexible and easier to maintain.

### Q5: What is the `super` keyword used for?

**Answer:** `super` is used to: (1) call the parent class constructor (`super()`), which must be done before accessing `this` in the child constructor, and (2) call parent class methods (`super.method()`) when overriding to extend rather than replace behavior.

### Q6: Can a child class access private members of its parent?

**Answer:** No. Private members are only accessible within the class that defines them. If a child class needs access to parent internals, the parent should use `protected` instead of `private`.

---

**Next:** [06 - Abstract Classes](./06-abstract-classes.md)
