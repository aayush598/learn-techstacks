# The `keyof` Operator in TypeScript

`keyof` is a type-level operator that produces a union of string literal types representing the keys of a given type. It's one of the most commonly used TypeScript features for writing generic, type-safe code.

---

## Table of Contents

1. [What is `keyof`?](#what-is-keyof)
2. [keyof with Interfaces](#keyof-with-interfaces)
3. [keyof with Type Aliases](#keyof-with-type-aliases)
4. [keyof with Classes](#keyof-with-classes)
5. [keyof with Generic Constraints](#keyof-with-generic-constraints)
6. [keyof as Type vs Value](#keyof-as-type-vs-value)
7. [Keyof<T> Pattern](#keyoft-pattern)
8. [Combined with Mapped Types](#combined-with-mapped-types)
9. [Real-World keyof Usage](#real-world-keyof-usage)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What is `keyof`?

`keyof` takes a type and returns a union of its keys' string literal types.

```typescript
type Person = {
  name: string;
  age: number;
  email: string;
};

type PersonKeys = keyof Person; // "name" | "age" | "email"
```

At runtime, `keyof` maps to JavaScript property names. At compile time, it gives you a union of string literals.

### Basic usage

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

type UserKeys = keyof User; // "id" | "name" | "email"

// You can use this union type for type-safe property access
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { id: 1, name: "Alice", email: "alice@example.com" };
const name = getProperty(user, "name"); // string
const id = getProperty(user, "id");     // number

// ❌ Compile error — "foo" is not a key of User
// const foo = getProperty(user, "foo");
```

---

## keyof with Interfaces

`keyof` works with interfaces just like type aliases.

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
}

type UserKeys = keyof User; // "id" | "name" | "email" | "isActive"

// Type-safe access
function getValue<T extends keyof User>(key: T): User[T] {
  // ... implementation
  throw new Error("not implemented");
}

const name = getValue("name"); // string
const active = getValue("isActive"); // boolean
```

### Interface with optional properties

```typescript
interface Config {
  host: string;
  port?: number;
  debug?: boolean;
}

type ConfigKeys = keyof Config; // "host" | "port" | "debug"
// Optional properties are still included in keyof
```

### Interface with methods

```typescript
interface Calculator {
  add(a: number, b: number): number;
  subtract(a: number, b: number): number;
  multiply(a: number, b: number): number;
}

type CalculatorKeys = keyof Calculator; // "add" | "subtract" | "multiply"
// Methods are included as string literal types
```

---

## keyof with Type Aliases

```typescript
type Status = "pending" | "active" | "completed";

type StatusKeys = keyof Status; // never
// ⚠️ Status is a union of string literals, not an object type
// keyof on a union of primitives returns never

// To get keys of an object type alias:
type User = {
  id: number;
  name: string;
  email: string;
};

type UserKeys = keyof User; // "id" | "name" | "email"
```

### Important distinction

```typescript
// ❌ keyof on a string union returns never
type Direction = "north" | "south" | "east" | "west";
type DirectionKeys = keyof Direction; // never

// ✅ keyof on an object type returns the keys
type Config = {
  host: string;
  port: number;
};
type ConfigKeys = keyof Config; // "host" | "port"
```

---

## keyof with Classes

`keyof` works with class types and includes both public and private members (though you can only use public ones).

```typescript
class User {
  public name: string;
  public email: string;
  private password: string;

  constructor(name: string, email: string, password: string) {
    this.name = name;
    this.email = email;
    this.password = password;
  }
}

type UserKeys = keyof User; // "name" | "email" | "password"
// ⚠️ Private members are included in keyof!
// But you can't access them outside the class

// Type-safe access for public members
function getPublicProperty<K extends keyof Pick<User, "name" | "email">>(
  user: User,
  key: K
): User[K] {
  return user[key];
}
```

### Using keyof with class instances

```typescript
class EventBus {
  listeners: Map<string, Function[]> = new Map();

  on(event: string, callback: Function) {
    const list = this.listeners.get(event) || [];
    list.push(callback);
    this.listeners.set(event, list);
  }

  emit(event: string, ...args: any[]) {
    const list = this.listeners.get(event) || [];
    list.forEach((cb) => cb(...args));
  }
}

type EventBusKeys = keyof EventBus; // "listeners" | "on" | "emit"
```

---

## keyof with Generic Constraints

One of the most powerful uses of `keyof` is constraining generic type parameters.

```typescript
// Constrain K to be a key of T
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Usage
const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // string
const age = getProperty(user, "age");   // number
// ❌ getProperty(user, "email") — compile error
```

### Multiple generic constraints with keyof

```typescript
function setProperty<T, K extends keyof T>(
  obj: T,
  key: K,
  value: T[K]
): void {
  obj[key] = value;
}

const user = { name: "Alice", age: 30 };
setProperty(user, "name", "Bob");   // ✅
setProperty(user, "age", 25);      // ✅
// ❌ setProperty(user, "age", "old") — value type mismatch
```

### keyof with extends constraint

```typescript
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

const user = { id: 1, name: "Alice", email: "alice@example.com", age: 30 };
const picked = pick(user, ["name", "email"]); // { name: string; email: string }
```

### keyof with multiple types

```typescript
function merge<T, U, K extends keyof T & keyof U>(
  target: T,
  source: U,
  key: K
): T[K] | U[K] {
  return source[key] ?? target[key];
}

const config = { host: "localhost", port: 3000 };
const overrides = { host: "example.com", timeout: 5000 };
const host = merge(config, overrides, "host"); // string
```

---

## keyof as Type vs Value

`keyof` is a **type operator** — it's used in type positions, not value positions.

```typescript
type User = {
  id: number;
  name: string;
};

// ✅ Type position — keyof is valid
type Keys = keyof User; // "id" | "name"

// ❌ Value position — keyof is not valid
// const keys = keyof User; // Compile error!
// const keys: keyof User = ["id", "name"]; // This works because it's a type annotation
```

### Using keyof in runtime code

```typescript
function getKeys<T>(obj: T): Array<keyof T> {
  return Object.keys(obj) as Array<keyof T>;
}

const user = { id: 1, name: "Alice", email: "alice@example.com" };
const keys = getKeys(user); // ("id" | "name" | "email")[]
```

### keyof in type annotations

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

// As a function parameter type
function logProperty(key: keyof User) {
  console.log(key);
}

logProperty("id");    // ✅
logProperty("name");  // ✅
// logProperty("foo"); // ❌ Compile error
```

---

## Keyof<T> Pattern

The `Keyof<T>` pattern is a utility type pattern where you extract and use keys in various ways.

### Pick by value type

```typescript
type PickByValueType<T, ValueType> = {
  [K in keyof T as T[K] extends ValueType ? K : never]: T[K];
};

type User = {
  id: number;
  name: string;
  email: string;
  age: number;
  isActive: boolean;
};

type StringKeys = PickByValueType<User, string>; // { name: string; email: string }
type NumberKeys = PickByValueType<User, number>; // { id: number; age: number }
```

### Omit by value type

```typescript
type OmitByValueType<T, ValueType> = {
  [K in keyof T as T[K] extends ValueType ? never : K]: T[K];
};

type NonStringKeys = OmitByValueType<User, string>; // { id: number; age: number; isActive: boolean }
```

### Deep keys

```typescript
type Nested = {
  a: {
    b: {
      c: string;
      d: number;
    };
  };
  e: string;
};

type DeepKeys<T> = T extends object
  ? {
      [K in keyof T & string]: K | `${K}.${DeepKeys<T[K]> & string}`;
    }[keyof T & string]
  : never;

type NestedKeys = DeepKeys<Nested>;
// "a" | "a.b" | "a.b.c" | "a.b.d" | "e"
```

---

## Combined with Mapped Types

`keyof` is the foundation of mapped types.

### Basic mapped type

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

// Make all properties optional
type PartialUser = {
  [K in keyof User]?: User[K];
};

// Make all properties required
type RequiredUser = {
  [K in keyof User]: User[K];
};

// Make all properties readonly
type ReadonlyUser = {
  readonly [K in keyof User]: User[K];
};
```

### Transform property types

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

// Convert all properties to strings
type StringifiedUser = {
  [K in keyof User]: string;
};

// Convert all properties to promises
type AsyncUser = {
  [K in keyof User]: Promise<User[K]>;
};
```

### Key remapping with `as`

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

// Prefix all keys
type PrefixedUser = {
  [K in keyof User as `user_${K}`]: User[K];
};
// { user_id: number; user_name: string; user_email: string }

// Filter by value type
type StringUser = {
  [K in keyof User as User[K] extends string ? K : never]: User[K];
};
// { name: string; email: string }
```

### Getters pattern

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type UserGetters = Getters<User>;
// { getId: () => number; getName: () => string; getEmail: () => string }
```

---

## Real-World keyof Usage

### 1. Type-safe object accessor

```typescript
function get<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

function set<T, K extends keyof T>(obj: T, key: K, value: T[K]): void {
  obj[key] = value;
}

const config = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
};

const url = get(config, "apiUrl"); // string
set(config, "timeout", 10000);    // ✅
// set(config, "timeout", "fast"); // ❌ Type error
```

### 2. Event emitter

```typescript
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string; ctrlKey: boolean };
  scroll: { scrollTop: number };
};

class TypedEventEmitter<Events extends Record<string, any>> {
  private listeners: Map<string, Function[]> = new Map();

  on<K extends keyof Events>(
    event: K,
    callback: (payload: Events[K]) => void
  ): void {
    const list = this.listeners.get(event as string) || [];
    list.push(callback);
    this.listeners.set(event as string, list);
  }

  emit<K extends keyof Events>(event: K, payload: Events[K]): void {
    const list = this.listeners.get(event as string) || [];
    list.forEach((cb) => cb(payload));
  }
}

const emitter = new TypedEventEmitter<EventMap>();
emitter.on("click", (payload) => {
  console.log(payload.x, payload.y); // ✅ Typed
});
// emitter.on("click", (payload) => {
//   console.log(payload.key); // ❌ Compile error
// });
```

### 3. Form validation

```typescript
type UserForm = {
  name: string;
  email: string;
  age: number;
  bio: string;
};

type ValidationRules<T> = {
  [K in keyof T]?: (value: T[K]) => string | null;
};

const rules: ValidationRules<UserForm> = {
  name: (value) => (value.length < 2 ? "Name too short" : null),
  email: (value) => (!value.includes("@") ? "Invalid email" : null),
  age: (value) => (value < 18 ? "Must be 18+" : null),
};

function validate<T>(data: T, rules: ValidationRules<T>): string[] {
  const errors: string[] = [];
  for (const key in rules) {
    const rule = rules[key];
    if (rule) {
      const error = rule(data[key]);
      if (error) errors.push(error);
    }
  }
  return errors;
}
```

### 4. Type-safe localStorage

```typescript
type StorageSchema = {
  user: { id: string; name: string; email: string };
  theme: "light" | "dark";
  token: string;
  preferences: { notifications: boolean; newsletter: boolean };
};

function getStorage<K extends keyof StorageSchema>(
  key: K
): StorageSchema[K] | null {
  const value = localStorage.getItem(key);
  if (value === null) return null;
  return JSON.parse(value);
}

function setStorage<K extends keyof StorageSchema>(
  key: K,
  value: StorageSchema[K]
): void {
  localStorage.setItem(key, JSON.stringify(value));
}

const user = getStorage("user"); // { id: string; name: string; email: string } | null
const theme = getStorage("theme"); // "light" | "dark" | null
// setStorage("theme", "blue"); // ❌ Compile error
```

### 5. Query builder

```typescript
type TableSchema = {
  users: { id: number; name: string; email: string };
  posts: { id: number; title: string; body: string; userId: number };
};

function select<T extends keyof TableSchema>(
  table: T
): TableSchema[T][] {
  // ... SQL query builder
  return [];
}

const users = select("users"); // { id: number; name: string; email: string }[]
const posts = select("posts"); // { id: number; title: string; body: string; userId: number }[]
```

---

## Best Practices

1. **Use keyof with generics for type-safe property access** — `T[K]` pattern
2. **Use keyof to constrain generic parameters** — `K extends keyof T`
3. **Use keyof with mapped types** — for transforming object types
4. **Use keyof for runtime property names** — with `Object.keys()` and type assertions
5. **Avoid `keyof` on non-object types** — returns `never` for primitive unions
6. **Use keyof with Extract/Exclude** — for filtering keys
7. **Combine with key remapping** — `as` clause for prefix/suffix patterns

---

## Interview Questions

### Q1: What does `keyof` do?

**Answer:** `keyof` is a type operator that produces a union of string literal types representing the keys of a given type. For `type User = { id: number; name: string }`, `keyof User` is `"id" | "name"`. It's used for type-safe property access and generic constraints.

### Q2: What is the difference between `keyof T` and `keyof any`?

**Answer:** `keyof T` returns the keys of type `T`. `keyof any` returns `string | number | symbol` — the universal set of possible property keys. `keyof any` is useful as a constraint when you want to accept any valid JavaScript property key.

### Q3: How does `keyof` work with classes?

**Answer:** `keyof` on a class type returns all public and private member names as string literals. However, private members can't be accessed outside the class, so using them with `keyof` at runtime will cause issues. Use `Pick` to filter to only public members if needed.

### Q4: What is the `T[K]` pattern?

**Answer:** `T[K]` is an indexed access type that extracts the type of property `K` from type `T`. Combined with `keyof`, it allows you to write generic functions that return the correct type for any property key: `function get<T, K extends keyof T>(obj: T, key: K): T[K]`.

### Q5: How do you get all string keys of an object?

**Answer:** Use `keyof T` to get a union of string literal types. For runtime keys, use `Object.keys(obj)` and cast to `(keyof typeof obj)[]`. TypeScript's `Object.keys()` returns `string[]`, so a type assertion is needed.

### Q6: Can `keyof` be used with index signatures?

**Answer:** Yes. For `{ [key: string]: number }`, `keyof` returns `string`. For `{ [key: number]: string }`, `keyof` returns `number`. For types with both named properties and index signatures, `keyof` returns the union of the named keys and the index signature key type.
