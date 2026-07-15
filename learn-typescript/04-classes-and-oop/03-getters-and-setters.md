# 03 - Getters and Setters in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [The `get` and `set` Keywords](#the-get-and-set-keywords)
- [Readonly Properties vs Getters](#readonly-properties-vs-getters)
- [Computed Properties](#computed-properties)
- [Validation in Setters](#validation-in-setters)
- [Getter-Only Properties](#getter-only-properties)
- [Getter/Setter with Private Backing Field](#getter-setter-with-private-backing-field)
- [Accessor vs Method](#accessor-vs-method)
- [Performance Considerations](#performance-considerations)
- [Interview Questions](#interview-questions)

---

## Introduction

Getters and setters (also called **accessors**) are special class methods that provide controlled access to an object's properties. They allow you to define custom logic for reading (get) and writing (set) property values while maintaining the appearance of direct property access.

```typescript
const obj = new Example();
console.log(obj.value);  // Uses getter
obj.value = 42;          // Uses setter
```

Getters and setters bridge the gap between method functionality and property syntax, enabling encapsulation without sacrificing clean API design.

---

## The `get` and `set` Keywords

### Basic Getter

A getter is defined using the `get` keyword. It takes no parameters and is invoked when you access the property:

```typescript
class Circle {
  constructor(public radius: number) {}

  get area(): number {
    return Math.PI * this.radius ** 2;
  }

  get circumference(): number {
    return 2 * Math.PI * this.radius;
  }
}

const circle = new Circle(5);
console.log(circle.area);          // 78.53981633974483
console.log(circle.circumference); // 31.41592653589793

// Note: area is NOT stored - it's computed on each access
console.log(circle); // Circle { radius: 5 } — no 'area' property stored
```

### Basic Setter

A setter is defined using the `set` keyword. It takes one parameter (the value being assigned):

```typescript
class User {
  private _username: string = "";

  get username(): string {
    return this._username;
  }

  set username(value: string) {
    this._username = value.toLowerCase();
  }
}

const user = new User();
user.username = "JohnDoe";
console.log(user.username); // "johndoe" — automatically lowercased
```

### Getter and Setter Together

```typescript
class Temperature {
  private _celsius: number = 0;

  get celsius(): number {
    return this._celsius;
  }

  set celsius(value: number) {
    if (value < -273.15) {
      throw new Error("Temperature below absolute zero is not possible");
    }
    this._celsius = value;
  }

  get fahrenheit(): number {
    return this._celsius * 9 / 5 + 32;
  }

  set fahrenheit(value: number) {
    this.celsius = (value - 32) * 5 / 9; // Uses the celsius setter for validation
  }
}

const temp = new Temperature();
temp.fahrenheit = 212;
console.log(temp.celsius);   // 100
console.log(temp.fahrenheit); // 212
```

### Accessors in Interfaces

TypeScript supports `get` and `set` in interfaces:

```typescript
interface PersonLike {
  name: string;
  get age(): number;
  set age(value: number);
}

class Person implements PersonLike {
  private _age: number = 0;

  constructor(public name: string) {}

  get age(): number {
    return this._age;
  }

  set age(value: number) {
    if (value < 0) throw new Error("Age cannot be negative");
    this._age = value;
  }
}
```

### Accessors with Inheritance

```typescript
class Base {
  private _value: number = 0;

  get value(): number {
    return this._value;
  }

  set value(v: number) {
    this._value = v;
  }
}

class Derived extends Base {
  private _multiplier: number = 1;

  get value(): number {
    return super.value * this._multiplier;
  }

  set value(v: number) {
    super.value = v / this._multiplier;
  }

  get multiplier(): number {
    return this._multiplier;
  }

  set multiplier(v: number) {
    this._multiplier = v;
  }
}

const d = new Derived();
d.value = 10;
d.multiplier = 3;
console.log(d.value); // 30 (10 * 3)
```

---

## Readonly Properties vs Getters

Both `readonly` and getters can provide read-only access, but they serve different purposes.

### `readonly` Properties

```typescript
class User {
  readonly id: string;
  readonly createdAt: Date;

  constructor(id: string) {
    this.id = id;
    this.createdAt = new Date();
  }
}

const user = new User("123");
console.log(user.id);         // "123"
// user.id = "456";           // Error: Cannot assign to 'id' because it is read-only
```

### Getter-Only Properties (Computed)

```typescript
class Rectangle {
  constructor(public width: number, public height: number) {}

  get area(): number {
    return this.width * this.height;
  }

  get isSquare(): boolean {
    return this.width === this.height;
  }

  get diagonal(): number {
    return Math.sqrt(this.width ** 2 + this.height ** 2);
  }
}

const rect = new Rectangle(3, 4);
console.log(rect.area);     // 12
console.log(rect.isSquare); // false
console.log(rect.diagonal); // 5
```

### When to Use Which

| Feature | `readonly` | Getter |
|---|---|---|
| Stores a value | Yes | No (computed or from backing field) |
| Computed on access | No | Yes |
| Can enforce validation | No | Yes |
| Performance | O(1) | O(n) depending on computation |
| Use case | Immutable data | Computed/derived values |

### Performance Difference

```typescript
class ExpensiveComputation {
  private _data: number[] = Array.from({ length: 1_000_000 }, (_, i) => i);

  // Computed every access — expensive
  get sum(): number {
    console.log("Computing sum..."); // Called every time!
    return this._data.reduce((a, b) => a + b, 0);
  }

  // Cached after first computation — efficient
  private _sumCache: number | null = null;

  get cachedSum(): number {
    if (this._sumCache === null) {
      console.log("Computing sum (once)...");
      this._sumCache = this._data.reduce((a, b) => a + b, 0);
    }
    return this._sumCache;
  }
}
```

---

## Computed Properties

Getters (and setters) can compute values dynamically based on the object's internal state.

### Simple Computed Properties

```typescript
class Person {
  constructor(
    public firstName: string,
    public lastName: string,
    public birthYear: number
  ) {}

  get fullName(): string {
    return `${this.firstName} ${this.lastName}`;
  }

  get age(): number {
    const currentYear = new Date().getFullYear();
    return currentYear - this.birthYear;
  }

  get initials(): string {
    return `${this.firstName[0]}${this.lastName[0]}`;
  }
}

const person = new Person("John", "Doe", 1990);
console.log(person.fullName); // "John Doe"
console.log(person.age);      // 36 (varies by current year)
console.log(person.initials); // "JD"
```

### Computed Properties with DOM/UI Logic

```typescript
class ShoppingCart {
  private items: Array<{ name: string; price: number; quantity: number }> = [];

  get total(): number {
    return this.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );
  }

  get itemCount(): number {
    return this.items.reduce((count, item) => count + item.quantity, 0);
  }

  get summary(): string {
    return `${this.itemCount} items — Total: $${this.total.toFixed(2)}`;
  }

  get isEmpty(): boolean {
    return this.items.length === 0;
  }

  addItem(name: string, price: number, quantity: number = 1): void {
    const existing = this.items.find(item => item.name === name);
    if (existing) {
      existing.quantity += quantity;
    } else {
      this.items.push({ name, price, quantity });
    }
  }
}

const cart = new ShoppingCart();
cart.addItem("Laptop", 999.99);
cart.addItem("Mouse", 29.99, 2);
console.log(cart.summary); // "3 items — Total: $1059.97"
```

### Computed Properties That Read from External State

```typescript
class Sensor {
  private readings: number[] = [];

  addReading(value: number): void {
    this.readings.push(value);
  }

  get current(): number {
    return this.readings[this.readings.length - 1] ?? 0;
  }

  get min(): number {
    return this.readings.length > 0
      ? Math.min(...this.readings)
      : 0;
  }

  get max(): number {
    return this.readings.length > 0
      ? Math.max(...this.readings)
      : 0;
  }

  get average(): number {
    if (this.readings.length === 0) return 0;
    return this.readings.reduce((a, b) => a + b, 0) / this.readings.length;
  }

  get trend(): "rising" | "falling" | "stable" {
    if (this.readings.length < 2) return "stable";
    const last = this.readings[this.readings.length - 1];
    const prev = this.readings[this.readings.length - 2];
    const diff = last - prev;
    if (diff > 0.5) return "rising";
    if (diff < -0.5) return "falling";
    return "stable";
  }
}
```

---

## Validation in Setters

One of the primary uses of setters is to validate data before assigning it to a property. This prevents invalid states and ensures data integrity.

### Basic Validation

```typescript
class Person {
  private _name: string = "";

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    if (!value || value.trim().length === 0) {
      throw new Error("Name cannot be empty");
    }
    if (value.length > 100) {
      throw new Error("Name cannot exceed 100 characters");
    }
    this._name = value.trim();
  }
}

const p = new Person();
p.name = "Alice";   // OK
p.name = "  Bob  "; // Trims to "Bob"
// p.name = "";      // Error: Name cannot be empty
// p.name = "x".repeat(101); // Error: Name cannot exceed 100 characters
```

### Numeric Range Validation

```typescript
class Percentage {
  private _value: number = 0;

  get value(): number {
    return this._value;
  }

  set value(v: number) {
    if (v < 0 || v > 100) {
      throw new Error(`Percentage must be between 0 and 100, got ${v}`);
    }
    this._value = v;
  }
}

const pct = new Percentage();
pct.value = 75;   // OK
// pct.value = 150; // Error
// pct.value = -10; // Error
```

### Type Validation and Transformation

```typescript
class Email {
  private _address: string = "";

  private static readonly EMAIL_REGEX =
    /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  get address(): string {
    return this._address;
  }

  set address(value: string) {
    const normalized = value.toLowerCase().trim();
    if (!Email.EMAIL_REGEX.test(normalized)) {
      throw new Error(`Invalid email address: ${value}`);
    }
    this._address = normalized;
  }
}

const email = new Email();
email.address = "  John.Doe@Example.COM  ";
console.log(email.address); // "john.doe@example.com"
// email.address = "not-an-email"; // Error: Invalid email address
```

### Cascading Validation

Setters can trigger validation in related properties:

```typescript
class DateRange {
  private _start: Date = new Date();
  private _end: Date = new Date();

  get start(): Date {
    return this._start;
  }

  set start(value: Date) {
    this._start = value;
    if (this._end < this._start) {
      this._end = new Date(this._start);
      this._end.setDate(this._end.getDate() + 1);
    }
  }

  get end(): Date {
    return this._end;
  }

  set end(value: Date) {
    if (value < this._start) {
      throw new Error("End date cannot be before start date");
    }
    this._end = value;
  }

  get durationDays(): number {
    const diff = this.end.getTime() - this.start.getTime();
    return Math.ceil(diff / (1000 * 60 * 60 * 24));
  }
}

const range = new DateRange();
range.start = new Date("2024-01-01");
range.end = new Date("2024-01-15");
console.log(range.durationDays); // 14
```

### Setter with Side Effects

```typescript
class FormField {
  private _value: string = "";
  private _dirty: boolean = false;
  private _errors: string[] = [];

  get value(): string {
    return this._value;
  }

  set value(v: string) {
    this._value = v;
    this._dirty = true;
    this.validate();
  }

  get isValid(): boolean {
    return this._errors.length === 0;
  }

  get errors(): readonly string[] {
    return [...this._errors];
  }

  get isDirty(): boolean {
    return this._dirty;
  }

  private validate(): void {
    this._errors = [];
    if (this._value.length === 0) {
      this._errors.push("Field is required");
    }
    if (this._value.length > 255) {
      this._errors.push("Field exceeds maximum length of 255 characters");
    }
  }

  reset(): void {
    this._value = "";
    this._dirty = false;
    this._errors = [];
  }
}

const field = new FormField();
field.value = "";
console.log(field.isValid);   // false
console.log(field.errors);    // ["Field is required"]

field.value = "Hello";
console.log(field.isValid);   // true
console.log(field.isDirty);   // true
```

---

## Getter-Only Properties

Sometimes you want a property that can be read but never set. This is achieved with a getter that has no corresponding setter.

### Basic Getter-Only

```typescript
class Circle {
  constructor(public radius: number) {}

  get area(): number {
    return Math.PI * this.radius ** 2;
  }

  get diameter(): number {
    return this.radius * 2;
  }
}

const c = new Circle(5);
console.log(c.area);     // 78.54
// c.area = 100;         // Error: Area is a read-only property
// c.diameter = 10;      // Error: Diameter is a read-only property
```

### Getter-Only with External Data

```typescript
class UserProfile {
  constructor(
    private firstName: string,
    private lastName: string,
    private email: string
  ) {}

  get displayName(): string {
    return `${this.firstName} ${this.lastName}`;
  }

  get emailDomain(): string {
    return this.email.split("@")[1];
  }

  get initials(): string {
    return `${this.firstName[0]}${this.lastName[0]}`.toUpperCase();
  }

  // These are getter-only — no setters exist
  // Users of this class cannot modify them directly
}
```

### Getter-Only in Abstract Classes

```typescript
abstract class Shape {
  abstract get area(): number;
  abstract get perimeter(): number;

  get description(): string {
    return `Shape with area ${this.area.toFixed(2)} and perimeter ${this.perimeter.toFixed(2)}`;
  }
}

class Circle extends Shape {
  constructor(public radius: number) {
    super();
  }

  get area(): number {
    return Math.PI * this.radius ** 2;
  }

  get perimeter(): number {
    return 2 * Math.PI * this.radius;
  }
}

class Rectangle extends Shape {
  constructor(public width: number, public height: number) {
    super();
  }

  get area(): number {
    return this.width * this.height;
  }

  get perimeter(): number {
    return 2 * (this.width + this.height);
  }
}
```

---

## Getter/Setter with Private Backing Field

The most common pattern for getters and setters is to use a private backing field (typically prefixed with `_`) that stores the actual value.

### Standard Pattern

```typescript
class User {
  private _username: string = "";
  private _email: string = "";
  private _age: number = 0;

  get username(): string {
    return this._username;
  }

  set username(value: string) {
    const normalized = value.toLowerCase().trim();
    if (!/^[a-z0-9_]{3,20}$/.test(normalized)) {
      throw new Error(
        "Username must be 3-20 characters, lowercase alphanumeric and underscores"
      );
    }
    this._username = normalized;
  }

  get email(): string {
    return this._email;
  }

  set email(value: string) {
    const normalized = value.toLowerCase().trim();
    if (!normalized.includes("@")) {
      throw new Error("Invalid email");
    }
    this._email = normalized;
  }

  get age(): number {
    return this._age;
  }

  set age(value: number) {
    if (value < 0 || value > 150) {
      throw new Error("Invalid age");
    }
    this._age = value;
  }
}
```

### Lazy Initialization Pattern

```typescript
class DataProcessor {
  private _processedData: string[] | null = null;

  get processedData(): string[] {
    if (this._processedData === null) {
      console.log("Processing data for the first time...");
      this._processedData = this.processRawData();
    }
    return this._processedData;
  }

  private processRawData(): string[] {
    // Expensive computation
    return Array.from({ length: 1000 }, (_, i) => `item_${i}`);
  }
}

const processor = new DataProcessor();
// Data is processed only on first access
console.log(processor.processedData.length); // Logs "Processing data for the first time..."
console.log(processor.processedData.length); // Uses cached result
```

### Computed Cache Pattern

```typescript
class TreeNode<T> {
  children: TreeNode<T>[] = [];
  constructor(public value: T) {}

  private _depth: number | null = null;

  get depth(): number {
    if (this._depth === null) {
      this._depth =
        this.children.length === 0
          ? 0
          : 1 + Math.max(...this.children.map(c => c.depth));
    }
    return this._depth;
  }

  invalidateCache(): void {
    this._depth = null;
  }

  addChild(child: TreeNode<T>): void {
    this.children.push(child);
    this.invalidateCache();
  }
}
```

---

## Accessor vs Method

Understanding when to use accessors vs methods is important for API design.

### When to Use Accessors

Use accessors when:
- The operation looks like a property access
- There are no required parameters
- The operation has minimal side effects
- The operation is fast and idempotent

```typescript
class Vector {
  constructor(public x: number, public y: number) {}

  // Good as accessor — reads like a property
  get magnitude(): number {
    return Math.sqrt(this.x ** 2 + this.y ** 2);
  }

  get angle(): number {
    return Math.atan2(this.y, this.x);
  }

  get normalized(): Vector {
    const mag = this.magnitude;
    return new Vector(this.x / mag, this.y / mag);
  }
}
```

### When to Use Methods

Use methods when:
- The operation takes parameters
- The operation has significant side effects
- The operation performs I/O
- The operation name reads as a verb

```typescript
class Calculator {
  private _value: number = 0;

  // Good as accessor
  get value(): number {
    return this._value;
  }

  // Good as method — takes parameter, has side effects
  add(n: number): this {
    this._value += n;
    return this;
  }

  multiply(n: number): this {
    this._value *= n;
    return this;
  }

  reset(): void {
    this._value = 0;
  }
}
```

### Decision Table

| Criteria | Accessor | Method |
|---|---|---|
| Takes parameters | No | Yes |
| Side effects | Minimal/None | Yes |
| Speed | Fast | Can be slow |
| Naming convention | Noun/adjective | Verb |
| Caching behavior | Common | Less common |
| Chaining | Less common | Common (`builder` pattern) |

---

## Performance Considerations

### 1. Getters Are Not Cached by Default

Every access to a getter re-executes the function:

```typescript
class Expensive {
  get computed(): number {
    // This runs EVERY time .computed is accessed
    let sum = 0;
    for (let i = 0; i < 1_000_000; i++) {
      sum += Math.sqrt(i);
    }
    return sum;
  }
}
```

### 2. Implement Caching When Needed

```typescript
class Optimized {
  private _cache: Map<string, any> = new Map();

  get expensiveValue(): string {
    if (!this._cache.has("expensiveValue")) {
      this._cache.set("expensiveValue", this.computeExpensiveValue());
    }
    return this._cache.get("expensiveValue");
  }

  private computeExpensiveValue(): string {
    // Expensive computation
    return "result";
  }

  invalidateCache(key?: string): void {
    if (key) {
      this._cache.delete(key);
    } else {
      this._cache.clear();
    }
  }
}
```

### 3. Setters with Side Effects Can Be Slow

```typescript
// Slow: Triggers re-render on every keystroke
class ReactiveComponent {
  private _data: any;

  get data(): any {
    return this._data;
  }

  set data(value: any) {
    this._data = value;
    this.reRender(); // Expensive!
  }

  private reRender(): void {
    // DOM manipulation — expensive
  }
}

// Better: Debounce updates
class OptimizedComponent {
  private _data: any;
  private _updatePending = false;

  get data(): any {
    return this._data;
  }

  set data(value: any) {
    this._data = value;
    if (!this._updatePending) {
      this._updatePending = true;
      queueMicrotask(() => {
        this.reRender();
        this._updatePending = false;
      });
    }
  }

  private reRender(): void {
    // Only called once per microtask batch
  }
}
```

---

## Interview Questions

### Q1: What is the difference between a getter and a method?

**Answer:** A getter uses `get` keyword and is accessed like a property (`obj.prop`), takes no parameters, and cannot be called with parentheses. A method is called with parentheses (`obj.method()`) and can take parameters. Use getters for computed properties that feel like attributes; use methods for actions that take parameters or have significant side effects.

### Q2: Can a setter have a different type than its getter?

**Answer:** Yes. The getter and setter can have different types. A common pattern is a setter that accepts a broader type and converts it:

```typescript
class FormattedDate {
  private _date: Date = new Date();

  get date(): Date {
    return new Date(this._date); // Return copy
  }

  set date(value: Date | string | number) {
    this._date = new Date(value); // Accept multiple types
  }
}
```

### Q3: Can you have a getter without a setter?

**Answer:** Yes. A getter-only property is read-only. Attempting to set it results in a compile-time error. This is useful for computed properties that should not be directly settable.

### Q4: How do you implement a cached getter?

**Answer:** Use a private backing field initialized to `null`. On first access, compute and store the value. On subsequent accesses, return the cached value. Invalidate the cache when underlying data changes.

### Q5: When should you use a setter vs a method for validation?

**Answer:** Use a setter when the operation is conceptually a property assignment and the validation is quick. Use a method when the operation is more complex, might throw, or should be called explicitly (e.g., `updatePassword()` vs `set password()`).

### Q6: What is the relationship between accessors and `Object.defineProperty`?

**Answer:** TypeScript accessors compile down to `Object.defineProperty` calls with `get` and `set` descriptors. The compiled JavaScript uses the same `get`/`set` syntax that ES5+ supports.

---

**Next:** [04 - Static Members](./04-static-members.md)
