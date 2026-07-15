# Intersection Types in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Intersection Type Syntax](#intersection-type-syntax)
3. [Intersecting Objects](#intersecting-objects)
4. [Intersecting Primitives](#intersecting-primitives)
5. [Intersection vs Union](#intersection-vs-union)
6. [Combining with Interfaces](#combining-with-interfaces)
7. [Mixin Pattern with Intersections](#mixin-pattern-with-intersections)
8. [Real-World Use Cases](#real-world-use-cases)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Overview

An intersection type combines multiple types into one. The resulting type has **all** properties from all combined types. Use the `&` operator.

```typescript
// Basic intersection
type A = { name: string };
type B = { age: number };
type C = A & B; // { name: string; age: number }

const person: C = {
  name: "Alice",
  age: 30,
};
```

---

## Intersection Type Syntax

```typescript
// Basic intersection
type Person = { name: string } & { age: number };
// Equivalent to: { name: string; age: number }

// Multiple intersections
type User = { name: string } & { age: number } & { email: string };
// { name: string; age: number; email: string }

// Intersection with type aliases
type A = string;
type B = number;
type C = A & B; // string & number = never (no value can be both)

// Intersection with interfaces
interface Printable { print(): string; }
interface Serializable { serialize(): string; }

type Document = Printable & Serializable;
// Must implement both print() and serialize()

// Intersection in function parameters
function process(item: { name: string } & { age: number }): string {
  return `${item.name} (${item.age})`;
}

// Intersection in return types
function createUser(): { name: string } & { age: number } & { id: string } {
  return { name: "Alice", age: 30, id: "abc" };
}

// Nested intersections
type WithTimestamp = { createdAt: Date; updatedAt: Date };
type WithSoftDelete = { deletedAt: Date | null };
type Entity = { id: string } & WithTimestamp & WithSoftDelete;
// { id: string; createdAt: Date; updatedAt: Date; deletedAt: Date | null }

// Intersection with primitives (creates never)
type NeverType = string & number; // never
type NeverType2 = string & { length: number }; // never (string doesn't have a length that satisfies this)
```

---

## Intersecting Objects

```typescript
// Combining object types
type HasName = { name: string };
type HasAge = { age: number };
type HasEmail = { email: string };

type User = HasName & HasAge & HasEmail;
// { name: string; age: number; email: string }

const user: User = {
  name: "Alice",
  age: 30,
  email: "alice@example.com",
};

// Overlapping properties — types must be compatible
type A = { value: string };
type B = { value: string };
type C = A & B; // { value: string } — OK, same type

// Conflicting properties — creates never
type D = { value: string };
type E = { value: number };
type F = D & E; // { value: never } — no value can be both string and number

// Partial overlap — only conflicting props create issues
type G = { name: string; age: number };
type H = { name: string; email: string };
type I = G & H; // { name: string; age: number; email: string } — OK

// Practical: extending object types
type BaseUser = {
  id: string;
  name: string;
  email: string;
};

type UserWithProfile = BaseUser & {
  bio: string;
  avatar: string;
};

type UserWithSettings = BaseUser & {
  theme: "light" | "dark";
  notifications: boolean;
};

type FullUser = UserWithProfile & UserWithSettings;
// Has all properties from all three types
```

---

## Intersecting Primitives

When you intersect primitive types, the result is `never` (for incompatible types).

```typescript
// Incompatible primitives → never
type Never1 = string & number;          // never
type Never2 = string & boolean;         // never
type Never3 = number & boolean;         // never
type Never4 = string & null;            // never
type Never5 = string & undefined;       // never

// Compatible primitives → the primitive
type Str = string & string;             // string
type Num = number & number;             // number

// Never is useful as a "filter"
type Exclude<T, U> = T extends U ? never : T;
type Result = Exclude<"a" | "b" | "c", "a">;
// "b" | "c"

// Intersection with union types
type StringOrNumber = string | number;
type WithLength = { length: number };

// Distributes intersection over union
type Result2 = StringOrNumber & WithLength;
// (string & { length: number }) | (number & { length: number })
// = { length: number } | never = { length: number }
// (string has length, number doesn't — so number & { length: number } = never)

// Practical: filtering union members
type NonNullable2<T> = T extends null | undefined ? never : T;
type Clean = NonNullable2<string | null | undefined | number>;
// string | number
```

---

## Intersection vs Union

| Aspect | Intersection (`&`) | Union (`\|`) |
|--------|-------------------|-------------|
| Meaning | All of these types | One of these types |
| Properties | Has ALL properties | Has properties of ONE member |
| Value space | Smaller (more restrictive) | Larger (less restrictive) |
| Example | `A & B` has all A and B props | `A \| B` has A OR B props |
| Result type | More specific | More general |

```typescript
// Union: value can be one type
type StringOrNumber = string | number;
const a: StringOrNumber = "hello"; // OK (string)
const b: StringOrNumber = 42;      // OK (number)

// Intersection: value must satisfy all types
type WithLengthAndName = { length: number } & { name: string };
const c: WithLengthAndName = { length: 5, name: "hello" }; // Must have both

// Object union vs intersection
type A = { name: string; age: number };
type B = { name: string; email: string };

// Union: can be either A or B
type Union = A | B;
const u1: Union = { name: "Alice", age: 30 };           // OK (matches A)
const u2: Union = { name: "Bob", email: "bob@ex.com" }; // OK (matches B)
// const u3: Union = { name: "Charlie", age: 25, email: "c@ex.com" }; // OK (matches A — excess props OK on variable)

// Intersection: must have all properties from both
type Intersection = A & B;
const i1: Intersection = { name: "Alice", age: 30, email: "alice@ex.com" }; // Must have all
// const i2: Intersection = { name: "Alice", age: 30 }; // Error: missing email

// Practical difference
function handleUnion(value: A | B): string {
  // Can only access common properties
  return value.name; // OK
  // return value.age; // Error: age not on B

  if ("age" in value) {
    return `${value.name} (${value.age})`;
  }
  return `${value.name} (${value.email})`;
}

function handleIntersection(value: A & B): string {
  // Can access ALL properties
  return `${value.name} (${value.age}, ${value.email})`;
}
```

---

## Combining with Interfaces

```typescript
// Interface extends is usually preferred for object composition
interface HasName {
  name: string;
}

interface HasAge {
  age: number;
}

// Using intersection (works but extends is preferred for objects)
type UserIntersection = HasName & HasAge;

// Using extends (preferred for interfaces)
interface UserInterface extends HasName, HasAge {
  email: string;
}

// When to use intersection over extends:
// 1. When you need to combine with non-interface types
type Timestamped = { createdAt: Date; updatedAt: Date };
interface UserWithTimestamp extends HasName, Timestamped {
  // ✅ Can extend both interface and type alias
}

// 2. When you need conditional types
type Conditional<T> = T & { extra: string };

// 3. When you need union + intersection together
type Result<T> = (T & { success: true }) | { success: false; error: string };

// 4. When working with mapped types
type Nullable<T> = T & { nullable: true };
```

---

## Mixin Pattern with Intersections

```typescript
// Mixin pattern using intersection types
type Constructor<T = {}> = new (...args: any[]) => T;

// Timestamp mixin
function Timestamped<T extends Constructor>(Base: T) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();
  };
}

// SoftDelete mixin
function SoftDeletable<T extends Constructor>(Base: T) {
  return class extends Base {
    deletedAt: Date | null = null;

    softDelete() {
      this.deletedAt = new Date();
    }

    restore() {
      this.deletedAt = null;
    }
  };
}

// Base class
class BaseEntity {
  constructor(public id: string) {}
}

// Apply mixins
const TimestampedSoftDeletable = SoftDeletable(Timestamped(BaseEntity));

// Usage
class User extends TimestampedSoftDeletable {
  constructor(id: string, public name: string) {
    super(id);
  }
}

const user = new User("1", "Alice");
console.log(user.createdAt);  // Date
user.softDelete();             // Sets deletedAt

// Alternative: intersection-based mixins (simpler)
type Timestamped2 = {
  createdAt: Date;
  updatedAt: Date;
};

type SoftDeletable2 = {
  deletedAt: Date | null;
  softDelete(): void;
  restore(): void;
};

type UserService = {
  find(id: string): User | null;
  create(data: Omit<User, "id">): User;
};

// Combine all mixins
type FullUserService = Timestamped2 & SoftDeletable2 & UserService;
// Must implement all properties from all types
```

---

## Real-World Use Cases

```typescript
// 1. Extending API response types
type APIResponse<T> = {
  data: T;
  status: number;
  timestamp: number;
};

type Paginated<T> = {
  page: number;
  totalPages: number;
  totalItems: number;
};

type PaginatedResponse<T> = APIResponse<T[]> & Paginated<T>;

// 2. Form field types
type FieldConfig = {
  name: string;
  label: string;
  type: string;
};

type ValidationRules = {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
};

type FormField = FieldConfig & ValidationRules & {
  value?: unknown;
  error?: string;
};

// 3. Configuration objects
type DatabaseConfig = {
  host: string;
  port: number;
  database: string;
};

type AuthConfig = {
  secret: string;
  expiresIn: string;
};

type AppConfig = DatabaseConfig & AuthConfig & {
  nodeEnv: "development" | "production" | "test";
  logLevel: "debug" | "info" | "warn" | "error";
};

const config: AppConfig = {
  host: "localhost",
  port: 5432,
  database: "mydb",
  secret: "super-secret",
  expiresIn: "7d",
  nodeEnv: "development",
  logLevel: "info",
};

// 4. Type-safe event system
type EventPayload = {
  userId: string;
  timestamp: number;
};

type ClickEvent = EventPayload & {
  type: "click";
  x: number;
  y: number;
};

type ScrollEvent = EventPayload & {
  type: "scroll";
  scrollTop: number;
};

type AppEvent = ClickEvent | ScrollEvent;

// 5. Middleware pattern
type Context = {
  req: Request;
  res: Response;
};

type AuthContext = Context & {
  user: { id: string; role: string };
};

type LoggerContext = Context & {
  log: (message: string) => void;
};

type FullContext = AuthContext & LoggerContext;
```

---

## Best Practices

1. **Use intersection for object composition** when you need all properties from multiple types
2. **Prefer `extends` for interface inheritance** — it's more explicit and produces better errors
3. **Use intersection for mixin patterns** — combine multiple behaviors into one type
4. **Be careful with primitive intersections** — they produce `never` if incompatible
5. **Use intersection with utility types** for advanced type transformations
6. **Don't overuse intersections** — too many `&` operators make types hard to read
7. **Use named type aliases** for complex intersections to improve readability
8. **Intersection distributes over unions** — `A | B & C = (A & C) | (B & C)`
9. **Use intersection for extending third-party types** when you can't modify the original
10. **Document complex intersections** — they can be confusing for other developers

---

## Interview Questions

### Q1: What is an intersection type?

**Answer:** An intersection type combines multiple types into one using the `&` operator. The resulting type has all properties from all combined types. `A & B` means a value must satisfy both A and B.

### Q2: What happens when you intersect incompatible types?

**Answer:** The result is `never`. For example, `string & number` is `never` because no value can be both a string and a number.

### Q3: What is the difference between `&` and `|`?

**Answer:** `&` (intersection) means ALL of the types — the value must satisfy every type. `|` (union) means ANY of the types — the value must satisfy at least one type. Intersection is more restrictive (smaller value space), union is less restrictive (larger value space).

### Q4: When would you use intersection over interface extends?

**Answer:** Use intersection when combining with non-interface types, when working with conditional types, when you need union + intersection together, or when extending third-party types you can't modify. Use `extends` for object inheritance when both operands are interfaces.

### Q5: What is the mixin pattern?

**Answer:** A design pattern where you compose behaviors by intersecting multiple type-level functions. Each mixin adds properties/methods to a base type, and the final type is the intersection of all mixins.
