# Object Types in TypeScript

## Table of Contents

1. [Overview](#overview)
2. [Object Type Syntax](#object-type-syntax)
3. [Typed Objects](#typed-objects)
4. [Readonly Properties](#readonly-properties)
5. [Optional Properties](#optional-properties)
6. [Index Signatures](#index-signatures)
7. [Record Type](#record-type)
8. [Nested Objects](#nested-objects)
9. [Object Destructuring with Types](#object-destructuring-with-types)
10. [Structural Typing for Objects](#structural-typing-for-objects)
11. [Excess Property Checking](#excess-property-checking)
12. [Object Spread with Types](#object-spread-with-types)
13. [Best Practices](#best-practices)
14. [Interview Questions](#interview-questions)

---

## Overview

TypeScript uses structural typing for objects — objects are typed by their structure, not by explicit declarations. This means any object with the right shape is assignable, regardless of its origin.

---

## Object Type Syntax

```typescript
// Inline object type
const user: { name: string; age: number } = {
  name: "Alice",
  age: 30,
};

// With optional properties
const config: { host: string; port?: number } = {
  host: "localhost",
};

// With readonly properties
const point: { readonly x: number; readonly y: number } = {
  x: 10,
  y: 20,
};
// point.x = 30; // Error: readonly

// Object type as a variable type
type UserProfile = {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
};

const profile: UserProfile = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  isActive: true,
};

// Object type in function parameters
function processUser(user: { name: string; age: number }): string {
  return `${user.name} is ${user.age} years old`;
}

// Object type in return position
function createUser(name: string, age: number): { name: string; age: number } {
  return { name, age };
}

// Empty object type
const empty: {} = {};
// {} accepts any non-nullish value in TypeScript!
// const anything: {} = "hello"; // OK
// const alsoAnything: {} = 42;   // OK
// Use Record<string, never> for truly empty objects

// Object type (lowercase) — restricts to non-primitive values
const obj: object = { a: 1 }; // OK
// const prim: object = 42;    // Error: number is not assignable to object
```

---

## Typed Objects

```typescript
// Interface-style objects
interface User {
  name: string;
  age: number;
  email: string;
}

// Type alias-style objects
type Product = {
  id: number;
  name: string;
  price: number;
  description?: string;
};

// Objects with method signatures
type Calculator = {
  add: (a: number, b: number) => number;
  subtract: (a: number, b: number) => number;
  multiply: (a: number, b: number) => number;
};

const calc: Calculator = {
  add: (a, b) => a + b,
  subtract: (a, b) => a - b,
  multiply: (a, b) => a * b,
};

// Objects with function property syntax
type Logger = {
  log(message: string): void;
  error(message: string, code?: number): void;
};

const logger: Logger = {
  log: (msg) => console.log(msg),
  error: (msg, code) => console.error(`[${code}] ${msg}`),
};

// Objects with computed property names
const prop = "name";
type Obj = { [prop: string]: number };

// Objects with intersection
type Timestamped = { createdAt: Date; updatedAt: Date };
type UserWithTimestamps = User & Timestamped;

// Generic objects
type Container<T> = {
  value: T;
  getValue: () => T;
};

const numContainer: Container<number> = {
  value: 42,
  getValue: () => 42,
};

const strContainer: Container<string> = {
  value: "hello",
  getValue: () => "hello",
};
```

---

## Readonly Properties

```typescript
// readonly modifier prevents modification after creation
interface Config {
  readonly host: string;
  readonly port: number;
  readonly debug: boolean;
}

const config: Config = {
  host: "localhost",
  port: 3000,
  debug: true,
};

// config.host = "example.com"; // Error: Cannot assign to 'host'
// config.port = 8080;          // Error

// readonly with objects
const point: { readonly x: number; readonly y: number } = { x: 10, y: 20 };
// point.x = 30; // Error

// ReadonlyShallow vs ReadonlyDeep
type MutableUser = {
  name: string;
  address: {
    city: string;
    country: string;
  };
};

type ShallowReadonly = Readonly<MutableUser>;
// Only top-level properties are readonly
// address is still mutable (can modify address.city)

type DeepReadonly = ReadonlyDeep<MutableUser>;
// All properties recursively readonly
// address.city is also readonly

// Implementing ReadonlyDeep (not built-in before TS 4.x)
type ReadonlyDeep<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? T[K] extends Function
      ? T[K]
      : ReadonlyDeep<T[K]>
    : T[K];
};

// Practical example
interface AppState {
  readonly user: {
    readonly name: string;
    readonly age: number;
  };
  readonly settings: {
    readonly theme: "light" | "dark";
    readonly language: string;
  };
}

const state: AppState = {
  user: { name: "Alice", age: 30 },
  settings: { theme: "dark", language: "en" },
};

// state.user.name = "Bob"; // Error: readonly
// state.settings.theme = "light"; // Error: readonly

// readonly in class properties
class ImmutablePoint {
  constructor(
    public readonly x: number,
    public readonly y: number
  ) {}
}

const pt = new ImmutablePoint(10, 20);
// pt.x = 30; // Error: readonly
```

---

## Optional Properties

```typescript
// ? makes a property optional (can be undefined)
interface User {
  name: string;
  age: number;
  email?: string;      // optional
  phone?: string;      // optional
  address?: {          // optional nested object
    city: string;
    country: string;
  };
}

const user1: User = {
  name: "Alice",
  age: 30,
}; // OK — email and phone are optional

const user2: User = {
  name: "Bob",
  age: 25,
  email: "bob@example.com",
  phone: "+1234567890",
};

// Accessing optional properties
function greet(user: User): string {
  // user.email is string | undefined
  if (user.email) {
    return `Hello ${user.name} at ${user.email}`;
  }
  return `Hello ${user.name}`;
}

// Optional chaining with optional properties
function getCity(user: User): string | undefined {
  return user.address?.city; // undefined if address is undefined
}

// Type narrowing with optional properties
function processUser(user: User): string {
  let result = user.name;
  if (user.email) {
    result += ` (${user.email})`;
  }
  if (user.phone) {
    result += ` [${user.phone}]`;
  }
  return result;
}

// Optional with default values
function createUser(name: string, email?: string): User {
  return {
    name,
    age: 0,
    email: email ?? "unknown@example.com",
  };
}

// All optional
interface Empty {
  a?: string;
  b?: number;
  c?: boolean;
}

const empty: Empty = {}; // OK

// Partial<T> utility type makes all properties optional
type PartialUser = Partial<User>;
const partial: PartialUser = { name: "Alice" }; // Only name required

// Required<T> utility type makes all properties required
type RequiredUser = Required<User>;
// email and phone are now required
```

---

## Index Signatures

```typescript
// Index signatures allow any string or number key
interface StringMap {
  [key: string]: string;
}

const dict: StringMap = {
  hello: "world",
  foo: "bar",
  anyKey: "anyValue", // OK — index signature allows any string key
};

// Accessing index signature values
const value: string = dict["hello"]; // "world"
// dict.hello; // Also works

// Number index signatures
interface NumberArray {
  [index: number]: string;
}

const arr: NumberArray = ["a", "b", "c"];

// Combined string and number index signatures
interface Both {
  [key: string]: string | number;
  [index: number]: string; // Must be subtype of string index
}

// Index signatures with known properties
interface Dictionary {
  [key: string]: string;
  length: number; // Must be compatible with index signature type
}

// ⚠️ Index signature type must include all named properties
interface Bad {
  name: string;
  [key: string]: number; // Error: 'name' is not assignable to 'number'
}

// ✅ Correct
interface Good {
  name: string;
  [key: string]: string | number; // String key type includes string
}

// Index signatures with readonly
interface ReadonlyMap {
  readonly [key: string]: string;
}

const readonlyDict: ReadonlyMap = { a: "1" };
// readonlyDict["b"] = "2"; // Error: readonly

// Real-world: config objects
interface EnvConfig {
  [key: string]: string | number | boolean | undefined;
  NODE_ENV: string;
  PORT: number;
  DEBUG: boolean;
}

// Nested index signatures
interface NestedDict {
  [key: string]: {
    [subKey: string]: number;
  };
}

const matrix: NestedDict = {
  row1: { a: 1, b: 2 },
  row2: { a: 3, b: 4 },
};
```

---

## Record Type

```typescript
// Record<K, V> is a utility type for objects with known keys and value type
type UserRoles = Record<string, string[]>;

const roles: UserRoles = {
  alice: ["admin", "user"],
  bob: ["user"],
  charlie: ["moderator", "user"],
};

// Record with union keys
type StatusConfig = Record<"active" | "inactive" | "pending", { color: string }>;

const configs: StatusConfig = {
  active: { color: "green" },
  inactive: { color: "gray" },
  pending: { color: "yellow" },
};

// Record with number keys
type ScoreBoard = Record<number, string>;

const scores: ScoreBoard = {
  1: "Alice",
  2: "Bob",
  3: "Charlie",
};

// Record vs manual type
// Equivalent:
type A = Record<string, number>;
type B = { [key: string]: number };

// Record with readonly
type ImmutableMap = Readonly<Record<string, number>>;

// Record with optional values
type Config = Record<string, string | undefined>;

// Record for enum-like objects
const Colors = {
  Red: "#ff0000",
  Green: "#00ff00",
  Blue: "#0000ff",
} as const;

type ColorName = keyof typeof Colors;
type ColorValue = (typeof Colors)[ColorName];

type ColorMap = Record<ColorName, ColorValue>;

// Practical: API response type
type ApiResponse<T> = Record<string, T>;

interface User {
  name: string;
  age: number;
}

const usersById: ApiResponse<User> = {
  "1": { name: "Alice", age: 30 },
  "2": { name: "Bob", age: 25 },
};
```

---

## Nested Objects

```typescript
// Deep object types
interface Company {
  name: string;
  address: {
    street: string;
    city: string;
    country: string;
    zip: string;
  };
  departments: {
    name: string;
    employees: {
      name: string;
      role: string;
      skills: string[];
    }[];
  }[];
}

const company: Company = {
  name: "TechCorp",
  address: {
    street: "123 Main St",
    city: "San Francisco",
    country: "US",
    zip: "94102",
  },
  departments: [
    {
      name: "Engineering",
      employees: [
        {
          name: "Alice",
          role: "Senior Developer",
          skills: ["TypeScript", "React"],
        },
      ],
    },
  ],
};

// Accessing nested properties
const firstEmployee = company.departments[0].employees[0];
console.log(firstEmployee.name); // "Alice"

// Optional chaining for deep access
function getFirstEmployeeName(company: Company): string | undefined {
  return company.departments[0]?.employees[0]?.name;
}

// Deep partial
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

type PartialCompany = DeepPartial<Company>;
// All nested properties become optional

// Deep required
type DeepRequired<T> = {
  [K in keyof T]-?: T[K] extends object ? DeepRequired<T[K]> : T[K];
};

// Modifying nested properties (immutably)
function updateEmployeeName(
  company: Company,
  deptIndex: number,
  empIndex: number,
  newName: string
): Company {
  return {
    ...company,
    departments: company.departments.map((dept, di) =>
      di === deptIndex
        ? {
            ...dept,
            employees: dept.employees.map((emp, ei) =>
              ei === empIndex ? { ...emp, name: newName } : emp
            ),
          }
        : dept
    ),
  };
}
```

---

## Object Destructuring with Types

```typescript
interface User {
  name: string;
  age: number;
  email: string;
  isActive: boolean;
}

// Basic destructuring
function greet({ name, age }: User): string {
  return `Hello, ${name}! You are ${age}.`;
}

// Destructuring with renaming
function extractInfo({ name: userName, age: userAge }: User): string {
  return `${userName} (${userAge})`;
}

// Destructuring with defaults
function createUser({ name, age = 0, email = "", isActive = true }: User): User {
  return { name, age, email, isActive };
}

// Destructuring with rest
function getPublicProfile({ name, age, ...rest }: User): { name: string; age: number } {
  return { name, age };
}

// Nested destructuring
interface Company {
  name: string;
  address: {
    city: string;
    country: string;
  };
}

function getCity({ address: { city } }: Company): string {
  return city;
}

// Destructuring in for-of loops
const users: User[] = [{ name: "Alice", age: 30, email: "a@b.com", isActive: true }];
for (const { name, email } of users) {
  console.log(`${name}: ${email}`);
}

// Destructuring with type assertion
const data = { name: "Alice", age: 30 } as User;
const { name: n, age: a } = data;

// Type-safe destructuring from unknown
function safeDestructure(data: unknown): { name: string; age: number } | null {
  if (
    typeof data === "object" &&
    data !== null &&
    "name" in data &&
    "age" in data
  ) {
    const { name, age } = data as { name: unknown; age: unknown };
    if (typeof name === "string" && typeof age === "number") {
      return { name, age };
    }
  }
  return null;
}
```

---

## Structural Typing for Objects

TypeScript uses structural typing — objects are compatible if they have the same shape.

```typescript
interface Point {
  x: number;
  y: number;
}

interface Point3D {
  x: number;
  y: number;
  z: number;
}

// Point3D has all properties of Point, so it's assignable to Point
const p3d: Point3D = { x: 10, y: 20, z: 30 };
const p2d: Point = p3d; // OK — Point3D is a subtype of Point

// But Point is NOT assignable to Point3D
// const p3d2: Point3D = { x: 10, y: 20 }; // Error: missing z

// Extra properties are OK when assigning to a variable
const point = { x: 10, y: 20, z: 30 }; // Object literal
const p: Point = point; // OK — variable assignment doesn't check excess properties

// But excess property checking applies to object literals (see next section)

// Structural typing with functions
function logPoint(point: Point): void {
  console.log(`(${point.x}, ${point.y})`);
}

class VirtualPoint {
  constructor(public x: number, public y: number) {}
}

logPoint(new VirtualPoint(10, 20)); // OK — VirtualPoint has x and y

// Structural typing with interfaces
interface Printable {
  toString(): string;
}

function print(value: Printable): void {
  console.log(value.toString());
}

print("hello");     // OK — string has toString
print(42);          // OK — number has toString
print({ toString: () => "custom" }); // OK

// Nominal vs Structural typing
// TypeScript uses structural typing (not nominal)
// Two types with the same structure are compatible, even if they have different names
type UserId = string;
type ProductId = string;

// These are structurally identical, so they're interchangeable!
function getUserId(id: UserId): string { return id; }
getUserId("abc" as ProductId); // No error! (might be unwanted)
```

---

## Excess Property Checking

Object literals get special "excess property checking" to catch typos.

```typescript
interface Options {
  color: string;
  width: number;
}

// ✅ Object literal — excess property checking applies
// const opts: Options = { color: "red", width: 100, height: 200 };
// Error: Object literal may only specify known properties, and 'height' does not exist

// ✅ Variable assignment — no excess property checking
const obj = { color: "red", width: 100, height: 200 };
const opts: Options = obj; // OK — obj is a variable, not a literal

// ✅ Spread operator — no excess property checking
const defaults = { color: "blue", width: 50, height: 100 };
const opts2: Options = { ...defaults, width: 200 }; // OK

// Bypassing excess property checking (usually a code smell)
const opts3: Options = { color: "red", width: 100, height: 200 } as Options; // OK

// Excess property checking with union types
type A = { x: number };
type B = { y: number };
type Union = A | B;

// const u: Union = { x: 1, y: 2 }; // Error! (excess property checking with unions)
// Workaround:
const u: Union = { x: 1, y: 2 } as A; // OK

// Real-world: API options pattern
interface RequestOptions {
  method: "GET" | "POST" | "PUT" | "DELETE";
  url: string;
  headers?: Record<string, string>;
  body?: unknown;
}

// Excess properties catch typos
const req: RequestOptions = {
  method: "GET",
  url: "/api/users",
  // heders: {}, // Error: 'heders' does not exist (typo caught!)
  headers: {},  // OK
};
```

---

## Object Spread with Types

```typescript
// Spread preserves the type
interface User {
  name: string;
  age: number;
  email: string;
}

const user: User = { name: "Alice", age: 30, email: "alice@example.com" };

// Spread with overriding properties
const updatedUser: User = {
  ...user,
  age: 31, // Override age
};

// Spread with additional properties
const extended = {
  ...user,
  role: "admin",
  createdAt: new Date(),
};
// Type: User & { role: string; createdAt: Date }

// Spread for immutability
function updateUser(
  user: User,
  updates: Partial<User>
): User {
  return { ...user, ...updates };
}

const olderUser = updateUser(user, { age: 31 });

// Spread with readonly objects
interface ReadonlyUser {
  readonly name: string;
  readonly age: number;
}

const readonlyUser: ReadonlyUser = { name: "Alice", age: 30 };
const mutableUser = { ...readonlyUser }; // Mutable copy

// Spread in generic functions
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}

const merged = merge({ name: "Alice" }, { age: 30 });
// Type: { name: string } & { age: number }

// Nested spread (not deep merge!)
interface Config {
  db: {
    host: string;
    port: number;
  };
  cache: {
    ttl: number;
  };
}

const defaults: Config = {
  db: { host: "localhost", port: 5432 },
  cache: { ttl: 3600 },
};

// Shallow spread only
const custom = {
  ...defaults,
  db: { host: "remote.host.com" }, // Replaces entire db!
  // db.port is lost! Only host is set.
};

// For deep merge, use a library or manual merge
const deepCustom: Config = {
  db: { ...defaults.db, host: "remote.host.com" },
  cache: defaults.cache,
};
```

---

## Best Practices

1. **Use `interface` for object shapes** that may be extended or implemented
2. **Use `type` for objects** with union types, intersections, or computed properties
3. **Use `Readonly<T>`** or `readonly` modifier for immutable data
4. **Use `Partial<T>`** for optional updates, `Required<T>` for required fields
5. **Use `Record<K, V>`** for objects with dynamic keys
6. **Be aware of excess property checking** — it only applies to object literals
7. **Prefer structural typing** — don't fight TypeScript's type system
8. **Use optional chaining** (`?.`) for accessing nested optional properties
9. **Use object spread** for immutable updates instead of mutation
10. **Annotate empty objects** explicitly since `{}` accepts almost anything

---

## Interview Questions

### Q1: What is structural typing in TypeScript?

**Answer:** Structural typing means object compatibility is determined by shape (structure) rather than explicit declaration. If object A has all the properties of object B (with compatible types), A is assignable to B, regardless of their type names.

### Q2: What is excess property checking?

**Answer:** A special check that applies to object literal assignments. It catches typos and extra properties that don't exist on the target type. It doesn't apply to variable assignments or spreads — only object literals.

### Q3: How do you create a deeply readonly object type?

**Answer:** Use a recursive mapped type:
```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
```

### Q4: What is the difference between `{}` and `Record<string, never>`?

**Answer:** `{}` accepts any non-nullish value (string, number, object, etc.). `Record<string, never>` only accepts an empty object `{}`. Use `Record<string, never>` when you want truly empty objects.

### Q5: When do excess properties get checked?

**Answer:** Only when assigning an object literal directly to a typed variable or parameter. Variable assignments, spreads, and function calls don't trigger excess property checking.
