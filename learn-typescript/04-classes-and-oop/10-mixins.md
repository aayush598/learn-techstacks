# 10 - Mixins in TypeScript

## Table of Contents

- [Introduction](#introduction)
- [What Are Mixins](#what-are-mixins)
- [Mixin Pattern in TypeScript](#mixin-pattern-in-typescript)
- [Mixin Type Definitions](#mixin-type-definitions)
- [Class Expressions as Mixins](#class-expressions-as-mixins)
- [Applying Multiple Mixins](#applying-multiple-mixins)
- [Mixin Inheritance Chain](#mixin-inheritance-chain)
- [Real-World Mixin Examples](#real-world-mixin-examples)
- [Mixin vs Multiple Inheritance](#mixin-vs-multiple-inheritance)
- [Alternatives to Mixins](#alternatives-to-mixins)
- [Interview Questions](#interview-questions)

---

## Introduction

Mixins are a design pattern that allows composing behaviors from multiple sources into a single class. TypeScript doesn't support multiple inheritance, but mixins provide a way to achieve similar functionality by combining class-like building blocks.

---

## What Are Mixins

A mixin is a type that contains methods or properties intended to be mixed into other classes. Unlike interfaces (which define contracts), mixins can provide concrete implementations.

### The Problem Mixins Solve

```typescript
// Without mixins — how do you share behavior across unrelated classes?
class Timestamped {
  createdAt = new Date();
  updatedAt = new Date();
}

class Loggable {
  log(message: string) { console.log(message); }
}

class Serializable {
  serialize() { return JSON.stringify(this); }
}

// Can't extend all three — single inheritance only!
// class UserModel extends Timestamped, Loggable, Serializable {}
```

### Mixin Concept

```typescript
// Mixins are functions that take a base class and return an extended version
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();

    touch() {
      this.updatedAt = new Date();
    }
  };
}

function Loggable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    log(message: string) {
      console.log(`[${new Date().toISOString()}] ${message}`);
    }
  };
}
```

---

## Mixin Pattern in TypeScript

### Basic Mixin Implementation

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

// A mixin that adds timestamp functionality
function TimestampedMixin<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();

    touch(): void {
      this.updatedAt = new Date();
    }

    getAge(): number {
      return Date.now() - this.createdAt.getTime();
    }
  };
}

// Base class
class BaseEntity {
  id = Math.random().toString(36).substring(2, 9);
}

// Apply mixin
const TimestampedEntity = TimestampedMixin(BaseEntity);

// Use the composed class
const entity = new TimestampedEntity();
console.log(entity.id);         // random id
console.log(entity.createdAt);  // current date
entity.touch();                 // updates updatedAt
```

### Mixin with Additional Properties

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function ActivatableMixin<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    isActive = false;

    activate(): void {
      this.isActive = true;
      this.onActivate?.();
    }

    deactivate(): void {
      this.isActive = false;
      this.onDeactivate?.();
    }

    onActivate?(): void;
    onDeactivate?(): void;
  };
}

class Widget {
  constructor(public name: string) {}
}

const ActivatableWidget = ActivatableMixin(Widget);
const widget = new ActivatableWidget("Button");
widget.activate();
console.log(widget.isActive); // true
```

---

## Mixin Type Definitions

### The Constructor Type

```typescript
// The core type used for mixins
type Constructor<T = {}> = new (...args: any[]) => T;

// More specific versions
type NoArgsConstructor<T = {}> = new () => T;
type SingleArgConstructor<T = {}, A = any> = new (arg: A) => T;
```

### Typing Mixin Return Values

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

// Mixin type: takes a constructor, returns a constructor
type Mixin<T extends Constructor> = <U extends Constructor>(
  base: U
) => new (...args: any[]) => InstanceType<U> & T;

// Well-typed mixin
function Auditable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    auditLog: string[] = [];

    audit(action: string): void {
      const entry = `[${new Date().toISOString()}] ${action}`;
      this.auditLog.push(entry);
    }

    getAuditTrail(): readonly string[] {
      return [...this.auditLog];
    }
  };
}
```

### Generic Mixins

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function StorableMixin<TData>(
  tableName: string
) {
  return function <TBase extends Constructor>(Base: TBase) {
    return class extends Base {
      static tableName = tableName;
      data: TData[] = [];

      add(item: TData): void {
        this.data.push(item);
      }

      getAll(): TData[] {
        return [...this.data];
      }

      find(predicate: (item: TData) => boolean): TData | undefined {
        return this.data.find(predicate);
      }
    };
  };
}

class BaseModel {
  id = Math.random().toString(36).substring(2);
}

interface User {
  name: string;
  email: string;
}

const UserStore = StorableMixin<User>("users")(BaseModel);
const store = new UserStore();
store.add({ name: "Alice", email: "alice@test.com" });
console.log(store.getAll());
```

---

## Class Expressions as Mixins

The most common mixin pattern in TypeScript uses class expressions.

### Basic Pattern

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();
  };
}

function Activatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    isActive = false;
    activate() { this.isActive = true; }
    deactivate() { this.isActive = false; }
  };
}

// Each mixin is a function that takes a base class and returns an extended class
```

### Applying Multiple Class Expressions

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function Tagged<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    tags: Set<string> = new Set();

    addTag(tag: string): void {
      this.tags.add(tag);
    }

    removeTag(tag: string): void {
      this.tags.delete(tag);
    }

    hasTag(tag: string): boolean {
      return this.tags.has(tag);
    }
  };
}

function Versioned<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    version = 0;
    private history: any[] = [];

    incrementVersion(): void {
      this.version++;
      this.history.push({ version: this.version, timestamp: new Date() });
    }

    getVersionHistory() {
      return [...this.history];
    }
  };
}

class Article {
  constructor(public title: string, public content: string) {}
}

// Apply multiple mixins
const ArticleV2 = Tagged(Versioned(Article));

const article = new ArticleV2("TypeScript Mixins", "Content here");
article.addTag("typescript");
article.addTag("oop");
article.incrementVersion();
article.incrementVersion();

console.log(article.tags);              // Set { "typescript", "oop" }
console.log(article.version);           // 2
console.log(article.getVersionHistory());
```

---

## Applying Multiple Mixins

### Chaining Mixins

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function Auditable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    private _auditLog: string[] = [];

    audit(message: string): void {
      this._auditLog.push(`[${new Date().toISOString()}] ${message}`);
    }

    getAuditLog(): string[] {
      return [...this._auditLog];
    }
  };
}

function Cacheable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    private _cache = new Map<string, any>();

    cacheGet<T>(key: string): T | undefined {
      return this._cache.get(key) as T | undefined;
    }

    cacheSet<T>(key: string, value: T): void {
      this._cache.set(key, value);
    }

    cacheClear(): void {
      this._cache.clear();
    }
  };
}

function Validatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    private _errors: string[] = [];

    addError(message: string): void {
      this._errors.push(message);
    }

    getErrors(): string[] {
      return [...this._errors];
    }

    isValid(): boolean {
      return this._errors.length === 0;
    }

    clearErrors(): void {
      this._errors = [];
    }
  };
}

// Base class
class Model {
  id = Math.random().toString(36).substring(2, 9);
}

// Apply all three mixins
const EnhancedModel = Auditable(Cacheable(Validatable(Model)));

const model = new EnhancedModel();
model.audit("Model created");
model.cacheSet("key", "value");
model.addError("Name is required");

console.log(model.getAuditLog());
console.log(model.cacheGet("key"));      // "value"
console.log(model.isValid());           // false
console.log(model.getErrors());         // ["Name is required"]
```

### Naming Composed Classes

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
  };
}

function Identifiable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    uid = crypto.randomUUID();
  };
}

class Base {}

// Give meaningful names to composed classes
const TimestampedBase = Timestamped(Base);
const IdentifiableBase = Identifiable(Base);
const TimestampedIdentifiableBase = Identifiable(Timestamped(Base));

console.log(new TimestampedBase().createdAt);
console.log(new IdentifiableBase().uid);
console.log(new TimestampedIdentifiableBase().createdAt);
console.log(new TimestampedIdentifiableBase().uid);
```

---

## Mixin Inheritance Chain

### Order Matters

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function A<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    a() { return "A"; }
  };
}

function B<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    b() { return "B"; }
  };
}

function C<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    c() { return "C"; }
  };
}

class Base {}

// Different order produces different prototypes
const ABC = A(B(C(Base)));
const CBA = C(B(A(Base)));

const abc = new ABC();
const cba = new CBA();

console.log(abc.a()); // "A"
console.log(abc.b()); // "B"
console.log(abc.c()); // "C"

console.log(cba.a()); // "A"
console.log(cba.b()); // "B"
console.log(cba.c()); // "C"

// Both have all methods, but the prototype chain differs
console.log(Object.getPrototypeOf(Object.getPrototypeOf(Object.getPrototypeOf(abc))));
console.log(Object.getPrototypeOf(Object.getPrototypeOf(Object.getPrototypeOf(cba))));
```

### Mixin Inheritance Diagram

```
A(B(C(Base)))
  ↓
A -> B -> C -> Base
  ↓
A has: a() from A
B has: b() from B
C has: c() from C
Base has: nothing
```

---

## Real-World Mixin Examples

### Event Emitter Mixin

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

type EventMap = Record<string, any>;

function EventEmitterMixin<TEvents extends EventMap, TBase extends Constructor>(
  Base: TBase
) {
  return class extends Base {
    private _listeners = new Map<string, Set<Function>>();

    on<K extends keyof TEvents>(
      event: K,
      handler: (payload: TEvents[K]) => void
    ): () => void {
      if (!this._listeners.has(event as string)) {
        this._listeners.set(event as string, new Set());
      }
      this._listeners.get(event as string)!.add(handler);

      // Return unsubscribe function
      return () => {
        this._listeners.get(event as string)?.delete(handler);
      };
    }

    emit<K extends keyof TEvents>(event: K, payload: TEvents[K]): void {
      this._listeners.get(event as string)?.forEach(handler => {
        handler(payload);
      });
    }
  };
}

// Usage
interface UserEvents {
  created: { userId: string };
  deleted: { userId: string };
  updated: { userId: string; changes: string[] };
}

class Base {}

const EventEmitterUser = EventEmitterMixin<UserEvents, typeof Base>(Base);

class UserService extends EventEmitterUser {
  createUser(name: string) {
    const userId = Math.random().toString(36).substring(2);
    this.emit("created", { userId });
    return userId;
  }
}

const service = new UserService();
service.on("created", ({ userId }) => {
  console.log(`User created: ${userId}`);
});

service.createUser("Alice");
```

### Validation Mixin

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function ValidationMixin<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    private _validators = new Map<string, Array<(value: any) => string | null>>();

    addValidator(
      field: string,
      validator: (value: any) => string | null
    ): void {
      if (!this._validators.has(field)) {
        this._validators.set(field, []);
      }
      this._validators.get(field)!.push(validator);
    }

    validate(data: Record<string, any>): Record<string, string[]> {
      const errors: Record<string, string[]> = {};

      for (const [field, validators] of this._validators) {
        const fieldErrors: string[] = [];
        for (const validator of validators) {
          const error = validator(data[field]);
          if (error) fieldErrors.push(error);
        }
        if (fieldErrors.length > 0) {
          errors[field] = fieldErrors;
        }
      }

      return errors;
    }

    isValid(data: Record<string, any>): boolean {
      return Object.keys(this.validate(data)).length === 0;
    }
  };
}

// Usage
class BaseModel {}

const ValidatableModel = ValidationMixin(BaseModel);

class UserForm extends ValidatableModel {
  constructor() {
    super();
    this.addValidator("name", (v) => !v ? "Name is required" : null);
    this.addValidator("email", (v) => v?.includes("@") ? null : "Invalid email");
    this.addValidator("age", (v) => v < 0 || v > 150 ? "Invalid age" : null);
  }
}

const form = new UserForm();
const errors = form.validate({ name: "", email: "invalid", age: -5 });
console.log(errors);
// { name: ["Name is required"], email: ["Invalid email"], age: ["Invalid age"] }
```

---

## Mixin vs Multiple Inheritance

| Feature | Mixins | Multiple Inheritance |
|---|---|---|
| Language support | Pattern (not built-in) | Built-in (C++, Python) |
| Diamond problem | Avoided (linear chain) | Can occur |
| Runtime overhead | Minimal | Can be complex |
| Flexibility | Very high (runtime composition) | Compile-time only |
| TypeScript support | Yes (via pattern) | No |
| Simplicity | More boilerplate | More intuitive syntax |

---

## Alternatives to Mixins

### 1. Composition (HAS-A)

```typescript
class User {
  constructor(
    private timestampService: TimestampService,
    private validator: Validator
  ) {}

  create(data: UserData) {
    this.timestampService.apply(data);
    const errors = this.validator.validate(data);
    // ...
  }
}
```

### 2. Utility Functions

```typescript
function timestamp<T extends object>(obj: T): T & { createdAt: Date } {
  return { ...obj, createdAt: new Date() };
}

function validate<T>(data: T, rules: ValidationRules): string[] {
  // validation logic
  return [];
}
```

### 3. Higher-Order Functions

```typescript
function withTimestamp<T extends Constructor>(Base: T) {
  return class extends Base {
    createdAt = new Date();
  };
}
// This IS the mixin pattern, but framed as a HOF
```

### 4. Decorators (Experimental)

```typescript
function Timestamped(target: any) {
  target.prototype.createdAt = new Date();
}

@Timestamped
class User {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

### 5. Object.assign

```typescript
const timestampBehavior = {
  createdAt: new Date(),
  touch() { this.updatedAt = new Date(); }
};

const user = Object.assign(
  { name: "Alice" },
  timestampBehavior
);
```

---

## Interview Questions

### Q1: What are mixins in TypeScript?

**Answer:** Mixins are a design pattern that allows composing behaviors from multiple sources into a single class. They are implemented as functions that take a base class and return a new class extending it with additional functionality. This provides a way to achieve multiple-inheritance-like behavior in TypeScript.

### Q2: Why doesn't TypeScript support multiple inheritance?

**Answer:** TypeScript (JavaScript) doesn't support multiple inheritance to avoid the diamond problem — where a class inherits from two classes with conflicting implementations of the same method. Mixins provide a controlled alternative with a linear prototype chain.

### Q3: How do you type a mixin in TypeScript?

**Answer:** A mixin is typed as a function that takes a `Constructor<T>` (a type representing a class constructor) and returns a new `Constructor` that extends the input. The core type is: `type Constructor<T = object> = new (...args: any[]) => T`.

### Q4: What is the order of mixin application?

**Answer:** Mixins are applied from the innermost to the outermost. `A(B(C(Base)))` means C extends Base first, then B extends the result, then A extends that result. The order determines the prototype chain and method resolution.

### Q5: What are alternatives to mixins?

**Answer:** Alternatives include: composition (HAS-A relationships), utility functions, higher-order functions, decorators (experimental), and `Object.assign`. Each has trade-offs in terms of type safety, readability, and flexibility.

### Q6: Can mixins have private members?

**Answer:** Yes, mixins can use TypeScript's `private` keyword for compile-time private members. However, these are only enforced at compile time. ECMAScript `#` private fields can also be used in mixins for runtime privacy.

---

**Next:** [Interview Questions](./interview-questions.md)
