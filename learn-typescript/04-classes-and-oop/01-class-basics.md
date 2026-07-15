# 01 - Class Basics in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [Class Declaration](#class-declaration)
- [Constructor](#constructor)
- [Property Declarations](#property-declarations)
- [Parameter Properties](#parameter-properties)
- [Readonly Properties](#readonly-properties)
- [Optional Properties](#optional-properties)
- [Class as a Type](#class-as-a-type)
- [Class Instances and the `new` Keyword](#class-instances-and-the-new-keyword)
- [typeof Class](#typeof-class)
- [Class Expressions](#class-expressions)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Introduction

Classes are the fundamental building block of object-oriented programming in TypeScript. They provide a blueprint for creating objects that encapsulate data (properties) and behavior (methods). TypeScript enhances JavaScript classes with static typing, access modifiers, and other powerful features that make OOP more robust and maintainable.

While JavaScript introduced classes in ES2015 (ES6), TypeScript adds a layer of type safety and additional syntax that makes classes far more expressive and powerful.

---

## Class Declaration

A class is declared using the `class` keyword. The basic syntax follows a familiar OOP pattern:

```typescript
class Person {
  // Properties
  name: string;
  age: number;

  // Constructor
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }

  // Method
  greet(): string {
    return `Hello, my name is ${this.name} and I am ${this.age} years old.`;
  }
}
```

### Empty Classes

You can declare a class with no members, which is useful as a marker or for later extension:

```typescript
class Marker {}
```

### Class with Only Methods

```typescript
class MathUtils {
  add(a: number, b: number): number {
    return a + b;
  }

  subtract(a: number, b: number): number {
    return a - b;
  }
}
```

### Hoisting Behavior

Unlike `function` declarations, class declarations are **not hoisted** in the traditional sense. You cannot use a class before its declaration in the source code:

```typescript
const obj = new MyClass(); // ReferenceError: Cannot access 'MyClass' before initialization

class MyClass {
  value = 42;
}
```

This is because classes are in the TDZ (Temporal Dead Zone) until their declaration is evaluated.

---

## Constructor

The `constructor` is a special method that is called when a new instance of a class is created. It is responsible for initializing the object's properties.

### Basic Constructor

```typescript
class User {
  username: string;
  email: string;

  constructor(username: string, email: string) {
    this.username = username;
    this.email = email;
  }
}

const user = new User("john_doe", "john@example.com");
console.log(user.username); // "john_doe"
console.log(user.email);    // "john@example.com"
```

### Constructor with Default Values

```typescript
class Config {
  host: string;
  port: number;
  debug: boolean;

  constructor(host: string = "localhost", port: number = 3000, debug: boolean = false) {
    this.host = host;
    this.port = port;
    this.debug = debug;
  }
}

const defaultConfig = new Config();             // "localhost", 3000, false
const customConfig = new Config("0.0.0.0", 8080, true); // "0.0.0.0", 8080, true
```

### Constructor with Validation

```typescript
class BankAccount {
  owner: string;
  balance: number;

  constructor(owner: string, balance: number) {
    if (balance < 0) {
      throw new Error("Initial balance cannot be negative");
    }
    if (!owner || owner.trim().length === 0) {
      throw new Error("Owner name cannot be empty");
    }
    this.owner = owner;
    this.balance = balance;
  }
}
```

### Constructor Returning an Object

The constructor implicitly returns the newly created instance (`this`). You **cannot** return a different object from a constructor in TypeScript (same as JavaScript):

```typescript
class Forbidden {
  constructor() {
    return { custom: "object" }; // This would actually work in JS but TypeScript warns against it
  }
}
```

> **Note:** If a constructor returns an object, that object is used instead of `this`. This is a JavaScript behavior, but TypeScript discourages it.

---

## Property Declarations

Properties are variables declared in the class body. TypeScript requires explicit type annotations or initializers for class properties.

### Explicit Type Annotations

```typescript
class Product {
  name: string;
  price: number;
  inStock: boolean;

  constructor(name: string, price: number, inStock: boolean) {
    this.name = name;
    this.price = price;
    this.inStock = inStock;
  }
}
```

### Property Initializers (ECMAScript Feature)

TypeScript allows property initializers, which set default values directly in the class body:

```typescript
class Product {
  name: string = "Unknown";
  price: number = 0;
  inStock: boolean = true;

  constructor(name: string, price: number) {
    this.name = name;
    this.price = price;
  }
}
```

### Strict Property Initialization (`strictPropertyInitialization`)

With `strictPropertyInitialization` enabled (part of `strict` mode), TypeScript ensures that all non-optional properties are initialized in the constructor:

```typescript
class Example {
  name: string; // Error: Property 'name' has no initializer and is not definitely assigned in the constructor

  constructor() {
    // name is never assigned
  }
}
```

To fix this, you can:
1. Initialize the property in the constructor
2. Use a property initializer
3. Use the definite assignment assertion (`!`)

```typescript
class Example {
  name!: string; // Definite assignment assertion - use with caution
}
```

### Property Declarations with Access Modifiers

Properties can have access modifiers (covered in detail in `02-access-modifiers.md`):

```typescript
class Employee {
  public name: string;
  private salary: number;
  protected department: string;

  constructor(name: string, salary: number, department: string) {
    this.name = name;
    this.salary = salary;
    this.department = department;
  }
}
```

---

## Parameter Properties

Parameter properties are one of TypeScript's most powerful class features. They allow you to declare and initialize class properties directly in the constructor parameter list by prefixing with an access modifier or `readonly`.

### Basic Syntax

```typescript
class User {
  constructor(
    public username: string,
    public email: string,
    private password: string
  ) {}
}
```

This is equivalent to:

```typescript
class User {
  public username: string;
  public email: string;
  private password: string;

  constructor(username: string, email: string, password: string) {
    this.username = username;
    this.email = email;
    this.password = password;
  }
}
```

### All Modifiers as Parameter Properties

```typescript
class Configuration {
  constructor(
    public host: string,        // public property
    public port: number,        // public property
    private apiKey: string,     // private property
    protected secret: string,   // protected property
    readonly version: string = "1.0.0" // readonly property with default
  ) {}
}

const config = new Configuration("localhost", 3000, "key123", "secret");
console.log(config.host);     // OK
console.log(config.version);  // OK
// console.log(config.apiKey);  // Error: Property 'apiKey' is private
// config.version = "2.0.0";   // Error: Cannot assign to 'version' because it is read-only
```

### Mixing Parameter Properties with Regular Parameters

```typescript
class Rectangle {
  constructor(
    public readonly width: number,
    public readonly height: number,
    color: string = "black" // regular parameter, not a property
  ) {
    console.log(`Creating a ${color} rectangle`);
  }
}
```

### Limitations

- You cannot use destructuring in parameter properties
- Parameter properties cannot have default values that are complex expressions evaluated at class definition time (they are evaluated at construction time, just like normal defaults)

---

## Readonly Properties

The `readonly` modifier ensures that a property can only be assigned during initialization (in the constructor or at declaration). After that, any attempt to modify the property results in a compile-time error.

### Basic Readonly

```typescript
class Coordinate {
  constructor(
    public readonly x: number,
    public readonly y: number
  ) {}
}

const point = new Coordinate(10, 20);
console.log(point.x); // 10
// point.x = 30;      // Error: Cannot assign to 'x' because it is read-only
```

### Readonly with Initialization

```typescript
class ApiEndpoint {
  readonly baseUrl: string;

  constructor() {
    this.baseUrl = "https://api.example.com";
    // this.baseUrl = "https://other.com"; // Error: already assigned above
  }
}
```

### Readonly vs Immutability

`readonly` is a **shallow** immutability guarantee at the TypeScript level. It does not prevent:

1. Mutating nested objects (since JavaScript objects are references)
2. Runtime modifications (TypeScript types are erased at runtime)

```typescript
class DataStore {
  readonly items: string[] = [];
}

const store = new DataStore();
store.items.push("hello");       // OK! The array is mutable, only the reference is readonly
// store.items = ["hello"];      // Error: Cannot assign to 'items' because it is read-only
```

> **Important:** `readonly` is a compile-time only feature. At runtime, JavaScript does not enforce it. Use `Object.freeze()` for runtime immutability when needed.

### Readonly vs `as const`

```typescript
class Constants {
  readonly PI = 3.14159;         // type is `number`
  readonly E = 2.71828;          // type is `number`
}

const AS_CONST = {
  PI: 3.14159,                   // type is `3.14159` (literal type)
  E: 2.71828                      // type is `2.71828` (literal type)
} as const;
```

---

## Optional Properties

Class properties can be made optional using the `?` modifier. Optional properties may or may not be initialized in the constructor.

### Basic Optional Properties

```typescript
class UserProfile {
  constructor(
    public username: string,
    public email: string,
    public bio?: string,
    public avatarUrl?: string
  ) {}
}

const minimalUser = new UserProfile("alice", "alice@example.com");
const fullUser = new UserProfile("bob", "bob@example.com", "I am Bob", "bob.jpg");

console.log(minimalUser.bio);     // undefined
console.log(fullUser.bio);        // "I am Bob"
```

### Optional Properties with Methods

```typescript
class Notification {
  constructor(
    public message: string,
    public title?: string,
    public priority?: "low" | "medium" | "high"
  ) {}

  getSummary(): string {
    const title = this.title ?? "No Title";
    const priority = this.priority ?? "low";
    return `[${priority.toUpperCase()}] ${title}: ${this.message}`;
  }
}
```

### Checking for Optional Properties

```typescript
class Settings {
  theme?: string;
  language?: string;

  applyDefaults(): void {
    if (this.theme === undefined) {
      this.theme = "light";
    }
    if (this.language === undefined) {
      this.language = "en";
    }
  }
}
```

---

## Class as a Type

In TypeScript, a class serves a dual purpose: it is both a **value** (a constructor function and prototype) and a **type** (the shape of instances).

### Using a Class as a Type

```typescript
class Dog {
  name: string;
  breed: string;

  constructor(name: string, breed: string) {
    this.name = name;
    this.breed = breed;
  }

  bark(): string {
    return `${this.name} says Woof!`;
  }
}

// Using the class as a type for a variable
let myDog: Dog;
myDog = new Dog("Buddy", "Golden Retriever");

// Using the class as a type for a function parameter
function printDogInfo(dog: Dog): void {
  console.log(`${dog.name} is a ${dog.breed}`);
  console.log(dog.bark());
}
```

### Interface vs Class as Type

When you use a class as a type, only the **instance side** is considered. Static members and the constructor are not part of the instance type:

```typescript
class MyClass {
  static staticProp = "static";
  instanceProp = "instance";

  static staticMethod(): void {}
  instanceMethod(): void {}
}

let obj: MyClass;
obj = new MyClass();
obj.instanceProp;     // OK
// obj.staticProp;    // Error: Property 'staticProp' does not exist on type 'MyClass'
// obj.staticMethod;  // Error: Property 'staticMethod' does not exist on type 'MyClass'
```

### Structural Typing with Classes

TypeScript uses structural typing, so a class type is compatible with any object that has the same shape:

```typescript
class Cat {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

interface HasName {
  name: string;
}

function greet(entity: HasName): void {
  console.log(`Hello, ${entity.name}!`);
}

const kitty = new Cat("Whiskers");
greet(kitty); // OK - Cat structurally satisfies HasName

const plainObj = { name: "Rex" };
greet(plainObj); // OK - plain object also satisfies HasName
```

---

## Class Instances and the `new` Keyword

The `new` keyword creates a new instance of a class. It:

1. Creates a new empty object `{}`
2. Sets the prototype of the object to the class's prototype
3. Calls the constructor with `this` bound to the new object
4. Returns the object (unless the constructor explicitly returns a different object)

```typescript
class Vehicle {
  type: string;

  constructor(type: string) {
    this.type = type;
    console.log(`Vehicle created: ${this.type}`);
  }

  describe(): string {
    return `This is a ${this.type}`;
  }
}

const car = new Vehicle("Car");  // Logs: "Vehicle created: Car"
const truck = new Vehicle("Truck");

console.log(car.describe());   // "This is a Car"
console.log(truck.describe()); // "This is a Truck"

// Verify instance relationship
console.log(car instanceof Vehicle); // true
console.log(car instanceof Object);  // true
```

### Multiple Instances

Each `new` call creates a **separate** instance with its own property values:

```typescript
class Counter {
  count = 0;

  increment(): void {
    this.count++;
  }
}

const a = new Counter();
const b = new Counter();

a.increment();
a.increment();

console.log(a.count); // 2
console.log(b.count); // 0 (independent instance)
```

### The `instanceof` Operator

```typescript
class Animal {}
class Dog extends Animal {}
class Cat extends Animal {}

const dog = new Dog();
const cat = new Cat();

console.log(dog instanceof Dog);   // true
console.log(dog instanceof Animal); // true (Dog extends Animal)
console.log(dog instanceof Cat);   // false
```

---

## typeof Class

The `typeof` operator can be used with a class name to get the **constructor function type** (the type of the static side of the class).

### Basic Usage

```typescript
class MyClass {
  static staticMethod(): string {
    return "hello";
  }
  instanceMethod(): number {
    return 42;
  }
}

// typeof MyClass gives us the type of the constructor/static side
type ConstructorType = typeof MyClass;

// This type includes static members and the constructor signature
const ctor: ConstructorType = MyClass; // OK
```

### When to Use `typeof`

The most common use case is when you need to reference a class's constructor as a type, especially in factory patterns:

```typescript
class Animal {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

class Dog extends Animal {
  breed: string;
  constructor(name: string, breed: string) {
    super(name);
    this.breed = breed;
  }
}

// Using typeof to create a factory function
function createInstance<T extends Animal>(
  Constructor: new (...args: any[]) => T,
  ...args: ConstructorParameters<typeof Constructor>
): T {
  return new Constructor(...args);
}

const dog = createInstance(Dog, "Buddy", "Labrador");
console.log(dog.name);  // "Buddy"
console.log(dog.breed); // "Labrador"
```

### typeof vs Instance Type

```typescript
class Example {
  value: number = 10;
  static staticValue: number = 20;
}

type InstanceType = Example;         // { value: number }
type ConstructorType = typeof Example; // { new(): Example; staticValue: number }
```

---

## Class Expressions

Class expressions are similar to function expressions but for classes. They allow you to create a class and optionally assign it to a variable in a single expression.

### Basic Class Expression

```typescript
const Animal = class {
  name: string;

  constructor(name: string) {
    this.name = name;
  }

  speak(): string {
    return `${this.name} makes a sound`;
  }
};

const dog = new Animal("Rex");
console.log(dog.speak()); // "Rex makes a sound"
```

### Named Class Expression

```typescript
const MyClass = class MyClassInner {
  // The name 'MyClassInner' is only accessible inside the class body
  static create(): MyClassInner {
    return new MyClassInner();
  }
};

// console.log(MyClassInner); // ReferenceError: MyClassInner is not defined
const instance = MyClass.create(); // Works fine
```

### Class Expression in Function Arguments

```typescript
function createLogger(prefix: string) {
  return class {
    log(message: string): void {
      console.log(`[${prefix}] ${message}`);
    }
  };
}

const ErrorLogger = createLogger("ERROR");
const logger = new ErrorLogger();
logger.log("Something went wrong"); // "[ERROR] Something went wrong"
```

### Class Expression with Mixins (Preview)

Class expressions are the foundation for the mixin pattern in TypeScript:

```typescript
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();

    getTimestamp(): string {
      return this.createdAt.toISOString();
    }
  };
}

class Base {
  name = "base";
}

const TimestampedBase = Timestamped(Base);
const obj = new TimestampedBase();
console.log(obj.getTimestamp()); // ISO date string
console.log(obj.name);          // "base"
```

---

## Best Practices

### 1. Use Parameter Properties When Appropriate

```typescript
// Good: Concise
class User {
  constructor(
    public readonly id: string,
    public name: string,
    private _email: string
  ) {}
}

// Avoid: Verbose when not needed
class User {
  public readonly id: string;
  public name: string;
  private _email: string;

  constructor(id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this._email = email;
  }
}
```

### 2. Prefer `readonly` for Immutable Data

```typescript
class Point {
  constructor(
    public readonly x: number,
    public readonly y: number
  ) {}
}
```

### 3. Initialize Properties Early

```typescript
// Good
class Service {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger; // Always initialized
  }
}

// Bad
class Service {
  private logger!: Logger; // Definite assignment assertion hides bugs
}
```

### 4. Keep Classes Focused (Single Responsibility)

```typescript
// Bad: Does too much
class UserManager {
  createUser(): void {}
  sendEmail(): void {}
  generateReport(): void {}
  connectToDatabase(): void {}
}

// Good: Separate concerns
class UserService {
  createUser(): void {}
}

class EmailService {
  sendEmail(): void {}
}

class ReportService {
  generateReport(): void {}
}
```

### 5. Use Structural Typing to Your Advantage

```typescript
// Define interfaces for function parameters, not class types
interface Printable {
  toString(): string;
}

function print(item: Printable): void {
  console.log(item.toString());
}

// Any class with a toString() method works
class Invoice implements Printable {
  constructor(public amount: number) {}
  toString(): string {
    return `Invoice: $${this.amount}`;
  }
}
```

---

## Interview Questions

### Q1: What is the difference between a class declaration and a class expression?

**Answer:** A class declaration (`class MyClass {}`) creates a named class that is available in the enclosing scope. A class expression (`const MyClass = class {}`) assigns the class to a variable. Named class expressions have the class name accessible only inside the class body. Class declarations are not hoisted in the traditional sense (they're in the TDZ), while class expressions evaluate the variable assignment at runtime.

### Q2: What are parameter properties in TypeScript?

**Answer:** Parameter properties allow you to declare and initialize class properties directly in the constructor parameter list by prefixing with `public`, `private`, `protected`, `readonly`, or combinations thereof. This eliminates the need for explicit property declarations and assignments in the constructor body.

```typescript
class User {
  constructor(public name: string, private age: number) {}
}
// Equivalent to:
class User {
  public name: string;
  private age: number;
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}
```

### Q3: What is the `typeof` used for with classes?

**Answer:** `typeof ClassName` gives you the type of the constructor/static side of the class. It's useful when you need to reference the class itself as a type (not an instance), such as in factory functions or dependency injection frameworks.

### Q4: Can a constructor return a value?

**Answer:** A constructor implicitly returns `this` (the newly created instance). You should not explicitly return a different object from a constructor as it can lead to unexpected behavior and TypeScript will warn about it. However, returning `this` is fine and is what constructors do implicitly.

### Q5: What is the difference between `readonly` and `as const`?

**Answer:** `readonly` makes a property不可 reassignable, but its type remains the declared type (e.g., `string`). `as const` makes all properties readonly AND narrows their types to literal types. `readonly` works at the property level in classes, while `as const` is a type assertion applied to objects/tuples.

### Q6: What happens if you don't initialize a class property in strict mode?

**Answer:** With `strictPropertyInitialization` enabled, TypeScript will emit an error if a non-optional class property is not definitely assigned in the constructor. You can fix this by: (1) initializing in the constructor, (2) using a property initializer, (3) using the definite assignment assertion (`!`), or (4) making the property optional.

### Q7: Are class property types enforced at runtime?

**Answer:** No. TypeScript types are erased at compile time. At runtime, a class instance is just a plain JavaScript object. The `readonly` modifier is also not enforced at runtime. For runtime type checking, you need to use libraries like `zod` or manual runtime checks.

---

**Next:** [02 - Access Modifiers](./02-access-modifiers.md)
