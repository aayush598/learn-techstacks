# Interface vs Type Alias — Detailed Comparison

## Table of Contents

1. [Overview](#overview)
2. [Comparison Table](#comparison-table)
3. [Declaration Merging](#declaration-merging)
4. [Extends vs Intersection](#extends-vs-intersection)
5. [Computed Properties](#computed-properties)
6. [Implementing in Classes](#implementing-in-classes)
7. [Error Messages Comparison](#error-messages-comparison)
8. [Performance Considerations](#performance-considerations)
9. [Community Conventions](#community-conventions)
10. [Decision Guide](#decision-guide)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Overview

Both `interface` and `type` can define object shapes, but they differ in features and use cases. Understanding when to use each is essential for writing idiomatic TypeScript.

---

## Comparison Table

| Feature | Interface | Type Alias |
|---------|-----------|------------|
| Object shapes | ✅ | ✅ |
| Declaration merging | ✅ | ❌ |
| Extends (inheritance) | ✅ `extends` | ❌ (use `&`) |
| Implements in classes | ✅ | ❌ |
| Union types | ❌ | ✅ `\|` |
| Intersection types | ❌ | ✅ `&` |
| Tuple types | ❌ | ✅ `[A, B]` |
| Computed properties | ❌ | ✅ (mapped types) |
| Primitive aliases | ❌ | ✅ |
| Function types | ✅ (call signatures) | ✅ |
| Generic constraints | ✅ | ✅ |
| Declaration hoisting | ✅ | ❌ |
| Error messages | Generally clearer | Can be verbose |
| Performance | Slightly better | Slightly worse |
| Circular references | ✅ | ✅ (since TS 3.7) |

---

## Declaration Merging

Only interfaces support declaration merging.

```typescript
// Interface — declaration merging works
interface User {
  name: string;
}

interface User {
  age: number;
}

// Merged: { name: string; age: number }
const user: User = { name: "Alice", age: 30 }; // ✅ OK

// Type alias — cannot merge
type User2 = { name: string; };
// type User2 = { age: number; }; // ❌ Error: Duplicate identifier 'User2'

// Why declaration merging matters:
// 1. Augmenting third-party library types
// 2. Splitting large interfaces across files
// 3. Plugin systems that extend base types

// Real-world example: Express Request
// In express types, you can augment:
// declare module 'express' {
//   interface Request {
//     user?: { id: string; name: string };
//   }
// }
// Then every Request object has the user property

// With type aliases, you'd need intersection:
type BaseRequest = { body: unknown; params: Record<string, string> };
type AugmentedRequest = BaseRequest & { user?: { id: string; name: string } };
// Less flexible, no merging across files
```

---

## Extends vs Intersection

Both achieve similar results, but with different semantics and limitations.

```typescript
// Interface: extends (explicit inheritance)
interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}
// Dog = { name: string; breed: string }

// Type alias: intersection
type Animal2 = { name: string; };
type Dog2 = Animal2 & { breed: string; };
// Dog2 = { name: string; breed: string }

// Multiple extension
interface A { a: string; }
interface B { b: number; }
interface C extends A, B { c: boolean; }
// C = { a: string; b: number; c: boolean }

type A2 = { a: string; };
type B2 = { b: number; };
type C2 = A2 & B2 & { c: boolean; };
// Same result

// Key difference: extends validates interface-specific constraints
interface Base {
  value: string;
}

interface Extended extends Base {
  value: string; // Must be compatible
  extra: number;
}

// Intersection allows conflicting types (produces never)
type Bad = { value: string } & { value: number };
// Bad.value is never (no value can be both string and number)

// Intersection is more powerful for types
type StringOrNumber = string | number;
type WithPrefix = StringOrNumber & { prefix: string }; // string & { prefix: string } | number & { prefix: string }
// This works because intersection distributes over unions
```

---

## Computed Properties

Only type aliases support computed/mapped properties.

```typescript
// Type alias: computed properties via mapped types
type Keys = "name" | "age" | "email";
type User = { [K in Keys]: string };
// { name: string; age: string; email: string }

// Type alias: conditional types
type IsString<T> = T extends string ? true : false;
type A = IsString<"hello">; // true
type B = IsString<42>;      // false

// Type alias: template literal types
type EventName = `on${Capitalize<string>}`;
// "on" + any capitalized string

// Type alias: recursive types
type Json = string | number | boolean | null | Json[] | { [key: string]: Json };

// Interface: cannot do any of these
// interface User { [K in Keys]: string; } // ❌ Error

// Interface: index signatures (limited)
interface User2 {
  [key: string]: string; // Any string key
  name: string;          // Known key
}
// This is different from mapped types — it allows ANY key

// Practical: derive types from existing types
type UserKeys = keyof User; // "name" | "age" | "email"
type UserValues = User[UserKeys]; // string (if all values are string)

// Type alias: extract specific properties
type UserNameAndEmail = Pick<User, "name" | "email">;
// { name: string; email: string }
```

---

## Implementing in Classes

Only interfaces can be implemented by classes.

```typescript
// Interface: can be implemented
interface Drawable {
  draw(): string;
  resize(factor: number): void;
}

class Circle implements Drawable {
  constructor(private radius: number) {}

  draw(): string {
    return `Circle with radius ${this.radius}`;
  }

  resize(factor: number): void {
    this.radius *= factor;
  }
}

// Type alias: cannot be implemented
type Drawable2 = {
  draw(): string;
  resize(factor: number): void;
};

// class Circle2 implements Drawable2 {} // ❌ Error

// Multiple interface implementation
interface Serializable {
  serialize(): string;
}

interface Validatable {
  validate(): boolean;
}

class User implements Serializable, Validatable {
  constructor(public name: string) {}

  serialize(): string {
    return JSON.stringify({ name: this.name });
  }

  validate(): boolean {
    return this.name.length > 0;
  }
}

// Abstract class implementing interface
interface Storage {
  get(key: string): unknown;
  set(key: string, value: unknown): void;
  delete(key: string): void;
}

abstract class BaseStorage implements Storage {
  abstract get(key: string): unknown;
  abstract set(key: string, value: unknown): void;
  abstract delete(key: string): void;

  // Concrete method
  has(key: string): boolean {
    return this.get(key) !== undefined;
  }
}

class LocalStorage extends BaseStorage {
  get(key: string): unknown {
    return localStorage.getItem(key);
  }
  set(key: string, value: unknown): void {
    localStorage.setItem(key, String(value));
  }
  delete(key: string): void {
    localStorage.removeItem(key);
  }
}
```

---

## Error Messages Comparison

```typescript
// Interface: generally clearer error messages
interface User {
  name: string;
  age: number;
  email: string;
}

// Error: Property 'age' is missing in type '{ name: string; email: string }'
//   but required in type 'User'
const user1: User = { name: "Alice", email: "alice@example.com" };

// Type alias: can be more verbose with intersections
type User2 = { name: string } & { age: number } & { email: string };

// Error: Property 'age' is missing in type '{ name: string; email: string }'
//   but required in type '{ age: number; }'
// (Error points to the intersection member, not the full type)
const user2: User2 = { name: "Alice", email: "alice@example.com" };

// Deep intersection error messages can be confusing
type A = { x: { y: { z: string } } };
type B = { x: { y: { w: number } } };
type C = A & B;

// Error message for C references intersection members, not the merged shape

// Interface: nested errors are clearer
interface Config {
  db: {
    host: string;
    port: number;
  };
}

// Error: Property 'port' is missing in type '{ host: string; }'
//   but required in type '{ host: string; port: number; }'
const config: Config = { db: { host: "localhost" } };
```

---

## Performance Considerations

```typescript
// Interfaces: generally slightly faster for type checking
// - TypeScript maintains a "declaration" for each interface
// - Declaration merging is efficient
// - Structural comparison is optimized

// Type aliases: can be slower with complex intersections
// - Each intersection creates a new type
// - Deeply nested intersections can slow down type checking
// - TypeScript needs to resolve the full type before checking

// Example of performance difference
type DeepIntersection = {
  a: { b: { c: string } };
} & {
  d: { e: { f: number } };
} & {
  g: { h: { i: boolean } };
};

// vs
interface DeepInterface {
  a: { b: { c: string } };
  d: { e: { f: number } };
  g: { h: { i: boolean } };
}

// The interface version is slightly faster to check
// But the difference is negligible for most applications

// Practical advice:
// - Don't optimize based on type/interface performance
// - Choose based on features you need
// - The performance difference is only noticeable in very large codebases
// - TypeScript's compiler is fast enough for both
```

---

## Community Conventions

```typescript
// General TypeScript community conventions:

// 1. Use interfaces for object shapes (most common)
interface User {
  name: string;
  age: number;
}

// 2. Use type for unions and intersections
type StringOrNumber = string | number;
type Nullable<T> = T | null;

// 3. Use type for mapped types and utility types
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type Partial<T> = { [K in keyof T]?: T[K] };

// 4. Use type for tuples
type Pair = [string, number];

// 5. Use type for function types
type Callback = (data: string) => void;

// 6. Use interface for public APIs (better error messages)
interface PublicAPI {
  method(): void;
}

// 7. Use interface for class implementation contracts
interface Repository<T> {
  find(id: string): T | null;
  create(item: T): T;
}

// 8. Use type for enum-like patterns
const Status = { Active: "active", Inactive: "inactive" } as const;
type Status = (typeof Status)[keyof typeof Status];

// Popular style guides:
// - Airbnb: No strong preference
// - Google: Interfaces for objects, types for everything else
// - TypeScript handbook: Interface for objects, type for unions/computed
// - Most open source: Interface for objects, type for everything else

// ESLint rule: @typescript-eslint/consistent-type-definitions
// Can enforce either "interface" or "type" as the default
```

---

## Decision Guide

```
Do you need declaration merging?
  → Use interface

Do you need to implement in a class?
  → Use interface

Do you need union types?
  → Use type

Do you need tuple types?
  → Use type

Do you need mapped/computed properties?
  → Use type

Do you need to alias primitives or functions?
  → Use type

Is it a simple object shape?
  → Use interface (convention)

Is it a complex type with intersections?
  → Use type

Are you defining a public API?
  → Use interface (better error messages)

Do you need both a value and a type?
  → Use type with `as const` object
```

---

## Best Practices

1. **Follow your team's convention** — consistency matters more than the choice
2. **Use interfaces for object shapes** when you might extend or implement
3. **Use type aliases for unions, tuples, and computed types**
4. **Use interfaces for public APIs** for better error messages
5. **Don't mix both** for the same concept in the same codebase
6. **Use declaration merging** to augment third-party types
7. **Use type aliases** for utility types and transformations
8. **Consider error message quality** when defining complex types
9. **Don't worry about performance** — the difference is negligible
10. **Document your choice** — add a note in your style guide

---

## Interview Questions

### Q1: What are the main differences between interfaces and type aliases?

**Answer:** Interfaces support declaration merging, `extends`, and class implementation. Type aliases support unions, intersections, tuples, mapped types, and computed properties. Interfaces generally produce better error messages for object shapes.

### Q2: When should you use a type alias over an interface?

**Answer:** Use type aliases for unions (`string | number`), intersections (`A & B`), tuples (`[string, number]`), mapped types (`{ [K in keyof T]: ... }`), conditional types, and primitive/function aliases.

### Q3: What is declaration merging and why is it useful?

**Answer:** Declaration merging automatically combines multiple interface declarations with the same name into one. It's useful for augmenting third-party library types (e.g., adding properties to Express Request) and splitting large interfaces across files.

### Q4: Can you implement a type alias in a class?

**Answer:** No. Only interfaces can be implemented by classes using the `implements` keyword. If you need to implement a type in a class, define it as an interface.

### Q5: Which produces better error messages?

**Answer:** Interfaces generally produce clearer error messages, especially for complex object types. Error messages for type aliases with intersections can reference individual intersection members rather than the merged type, making them harder to read.
