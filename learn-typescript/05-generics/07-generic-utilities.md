# 07 — Generic Utility Types

## Table of Contents

1. [Partial\<T\>](#partialt)
2. [Required\<T\>](#requiredt)
3. [Readonly\<T\>](#readonlyt)
4. [Record\<K, V\>](#recordk-v)
5. [Pick\<T, K\>](#pickt-k)
6. [Omit\<T, K\>](#omitt-k)
7. [Exclude\<T, U\>](#excludet-u)
8. [Extract\<T, U\>](#extractt-u)
9. [NonNullable\<T\>](#nonnullablyt)
10. [ReturnType\<T\>](#returntypet)
11. [Parameters\<T\>](#parameterst)
12. [ConstructorParameters\<T\>](#constructorparameterst)
13. [InstanceType\<T\>](#instancetypet)
14. [Awaited\<T\>](#awaitedt)
15. [Implementing Custom Utility Types](#custom-utilities)
16. [Best Practices](#best-practices)
17. [Interview Questions](#interview-questions)

---

## Partial\<T\>

Makes all properties of `T` optional. Useful for update operations where you don't
need to provide every field.

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

type PartialUser = Partial<User>;
// {
//   id?: string;
//   name?: string;
//   email?: string;
//   age?: number;
// }

// Real-world: PATCH endpoint
function updateUser(id: string, updates: Partial<User>): Promise<User> {
  return fetch(`/api/users/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates),
  }).then((r) => r.json());
}

// All valid — partial updates
updateUser("1", { name: "Bob" });
updateUser("1", { email: "bob@example.com", age: 30 });
updateUser("1", {});
```

### Nested Partial

```typescript
type DeepPartial<T> = {
  [K in keyof T]?: T[K] extends object ? DeepPartial<T[K]> : T[K];
};

interface Config {
  server: {
    host: string;
    port: number;
    ssl: {
      cert: string;
      key: string;
    };
  };
  database: {
    url: string;
    pool: number;
  };
}

// All nested properties are optional
const overrides: DeepPartial<Config> = {
  server: {
    port: 8080,
    ssl: {
      cert: "/path/to/cert",
    },
  },
};
```

### Implementation

```typescript
type Partial<T> = {
  [P in keyof T]?: T[P];
};
```

---

## Required\<T\>

Makes all properties of `T` required. The opposite of `Partial<T>`.

```typescript
interface Config {
  apiUrl?: string;
  timeout?: number;
  retries?: number;
  debug?: boolean;
}

// After validation, all fields are guaranteed
function initApp(raw: Config): Required<Config> {
  return {
    apiUrl: raw.apiUrl ?? "https://api.example.com",
    timeout: raw.timeout ?? 5000,
    retries: raw.retries ?? 3,
    debug: raw.debug ?? false,
  };
}

const config = initApp({});
console.log(config.apiUrl);   // string (guaranteed)
console.log(config.timeout);  // number (guaranteed)
```

### Deep Required

```typescript
type DeepRequired<T> = {
  [K in keyof T]-?: T[K] extends object ? DeepRequired<T[K]> : T[K];
};

interface Settings {
  theme?: {
    primary?: string;
    secondary?: string;
  };
  notifications?: {
    email?: boolean;
    push?: boolean;
  };
}

type FullSettings = DeepRequired<Settings>;
// All nested properties are required with -? modifier
```

### Implementation

```typescript
type Required<T> = {
  [P in keyof T]-?: T[P];
};
```

The `-?` modifier removes optionality.

---

## Readonly\<T\>

Makes all properties of `T` readonly (cannot be reassigned after creation).

```typescript
interface Point {
  x: number;
  y: number;
}

const origin: Readonly<Point> = { x: 0, y: 0 };
// origin.x = 5; // ❌ Cannot assign to 'x' because it is a read-only property

// Must create a new object to "update"
const moved: Point = { ...origin, x: 5 };
```

### Readonly with Arrays

```typescript
const items: ReadonlyArray<number> = [1, 2, 3];
// items.push(4);     // ❌ Property 'push' does not exist
// items[0] = 10;     // ❌ Index signature in type 'ReadonlyArray<number>'

// Create new arrays instead
const newItems = [...items, 4];
```

### Deep Readonly

```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

interface AppState {
  user: {
    name: string;
    preferences: {
      theme: string;
    };
  };
  counter: number;
}

const state: DeepReadonly<AppState> = {
  user: {
    name: "Alice",
    preferences: { theme: "dark" },
  },
  counter: 0,
};

// state.counter = 1;          // ❌
// state.user.name = "Bob";    // ❌
// state.user.preferences.theme = "light"; // ❌
```

### Implementation

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

---

## Record\<K, V\>

Constructs an object type with keys of type `K` and values of type `V`.

```typescript
// Basic usage
type UserRoles = Record<"admin" | "user" | "guest", string[]>;

const roles: UserRoles = {
  admin: ["read", "write", "delete", "manage"],
  user: ["read", "write"],
  guest: ["read"],
};

// Record with object values
type UsersById = Record<string, User>;

const users: UsersById = {
  "1": { id: "1", name: "Alice", email: "alice@example.com", age: 30 },
  "2": { id: "2", name: "Bob", email: "bob@example.com", age: 25 },
};

// Record as a map-like structure
type StatusMessages = Record<number, string>;

const httpMessages: StatusMessages = {
  200: "OK",
  201: "Created",
  400: "Bad Request",
  404: "Not Found",
  500: "Internal Server Error",
};
```

### Record with Interface Keys

```typescript
interface Permission {
  resource: string;
  action: string;
}

type PermissionMap = Record<Permission, boolean>;

const permissions: PermissionMap = {
  { resource: "users", action: "read" }: true,
  { resource: "users", action: "write" }: true,
  { resource: "admin", action: "delete" }: false,
};
```

### Implementation

```typescript
type Record<K extends keyof any, V> = {
  [P in K]: V;
};
```

---

## Pick\<T, K\>

Constructs a type by picking a subset of properties from `T` by keys `K`.

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  age: number;
  createdAt: Date;
}

type UserSummary = Pick<User, "id" | "name" | "email">;
// {
//   id: string;
//   name: string;
//   email: string;
// }

// Real-world: API response that only returns certain fields
function getUserSummary(id: string): Promise<UserSummary> {
  return fetch(`/api/users/${id}/summary`).then((r) => r.json());
}

// Useful for forms
type UserForm = Pick<User, "name" | "email" | "age">;

function createUserForm(): UserForm {
  return { name: "", email: "", age: 0 };
}
```

### Multiple Picks

```typescript
type UserContact = Pick<User, "name" | "email">;
type UserAuth = Pick<User, "id" | "email" | "password">;
type UserProfile = Pick<User, "id" | "name" | "age" | "createdAt">;
```

### Implementation

```typescript
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

---

## Omit\<T, K\>

Constructs a type by removing a set of properties from `T`. The opposite of `Pick`.

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

// Remove sensitive fields
type UserPublic = Omit<User, "password" | "createdAt">;
// {
//   id: string;
//   name: string;
//   email: string;
// }

function toPublicUser(user: User): UserPublic {
  const { password, createdAt, ...publicUser } = user;
  return publicUser;
}

// For create endpoints (omit auto-generated fields)
type CreateUserInput = Omit<User, "id" | "createdAt">;

const newUser: CreateUserInput = {
  name: "Alice",
  email: "alice@example.com",
  password: "hashed_password",
};
```

### Omit vs Pick

```typescript
// These are equivalent for this specific case:
type A = Pick<User, "id" | "name" | "email">;
type B = Omit<User, "password" | "createdAt" | "age">;

// But Omit is better when the list of included fields is long
// Pick is better when the list of excluded fields is long
```

### Implementation

```typescript
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;
```

---

## Exclude\<T, U\>

Extracts all types from `T` that are **not assignable** to `U`. Works with union types.

```typescript
type T = "a" | "b" | "c" | "d";
type Excluded = Exclude<T, "a" | "c">;
// "b" | "d"

type Numbers = number | string | boolean;
type NoStrings = Exclude<Numbers, string>;
// number | boolean

// Real-world: exclude specific status codes
type HttpStatus = 200 | 201 | 204 | 400 | 401 | 403 | 404 | 500;
type SuccessStatus = Exclude<HttpStatus, 400 | 401 | 403 | 404 | 500>;
// 200 | 201 | 204
```

### Implementation

```typescript
type Exclude<T, U> = T extends U ? never : T;
```

This is a **distributive conditional type**. It distributes over the union, excluding
any members assignable to `U`.

---

## Extract\<T, U\>

Extracts all types from `T` that **are assignable** to `U`. The opposite of `Exclude`.

```typescript
type T = "a" | "b" | "c" | "d";
type Extracted = Extract<T, "a" | "c" | "f">;
// "a" | "c"

type Mixed = string | number | boolean | null;
type Nullable = Extract<Mixed, null | undefined>;
// null

// Real-world: extract only certain event types
type EventType = "click" | "hover" | "focus" | "blur" | "scroll";
type MouseEvents = Extract<EventType, "click" | "hover">;
// "click" | "hover"
```

### Implementation

```typescript
type Extract<T, U> = T extends U ? T : never;
```

---

## NonNullable\<T\>

Removes `null` and `undefined` from `T`.

```typescript
type MaybeString = string | null | undefined;
type DefiniteString = NonNullable<MaybeString>;
// string

type MaybeUser = User | null | undefined;
type DefiniteUser = NonNullable<MaybeUser>;
// User

// Real-world: API responses
function processInput(input: string | null | undefined): NonNullable<string | null | undefined> {
  const value: string = input ?? "default"; // narrows to string
  return value.toUpperCase();
}
```

### Implementation

```typescript
type NonNullable<T> = T & {};
```

In modern TypeScript, this is equivalent to `T extends null | undefined ? never : T`.

---

## ReturnType\<T\>

Extracts the return type of a function type.

```typescript
function createUser() {
  return {
    id: crypto.randomUUID(),
    name: "Alice",
    email: "alice@example.com",
    createdAt: new Date(),
  };
}

type NewUser = ReturnType<typeof createUser>;
// {
//   id: string;
//   name: string;
//   email: string;
//   createdAt: Date;
// }

// With arrow functions
const fetchUser = (id: string): Promise<User> =>
  fetch(`/api/users/${id}`).then((r) => r.json());

type FetchUserReturn = ReturnType<typeof fetchUser>;
// Promise<User>
```

### Extracting Promise Resolution Type

```typescript
type Unwrap<T> = T extends Promise<infer U> ? Unwrap<U> : T;

type Result = Unwrap<Promise<Promise<string>>>; // string
```

### Implementation

```typescript
type ReturnType<T extends (...args: any) => any> = T extends (
  ...args: any
) => infer R
  ? R
  : any;
```

---

## Parameters\<T\>

Extracts the parameter types of a function type as a tuple.

```typescript
function createUser(name: string, age: number, email: string): User {
  return { id: crypto.randomUUID(), name, age, email, createdAt: new Date() };
}

type CreateUserParams = Parameters<typeof createUser>;
// [name: string, age: number, email: string]

// Usage: ensure type safety when calling with stored args
const args: CreateUserParams = ["Alice", 30, "alice@example.com"];
const user = createUser(...args); // Spread the tuple

// With destructured params
type Fn = (a: string, b: number, c: boolean) => void;
type Params = Parameters<Fn>;
// [a: string, b: number, c: boolean]
```

### Implementation

```typescript
type Parameters<T extends (...args: any) => any> = T extends (
  ...args: infer P
) => any
  ? P
  : never;
```

---

## ConstructorParameters\<T\>

Extracts the parameter types of a constructor function type as a tuple.

```typescript
class User {
  constructor(
    public name: string,
    public age: number,
    public email: string
  ) {}
}

type UserConstructorParams = ConstructorParameters<typeof User>;
// [name: string, age: number, email: string]

// Useful for factory patterns
function createInstance<T extends new (...args: any[]) => any>(
  Ctor: T,
  ...args: ConstructorParameters<T>
): InstanceType<T> {
  return new Ctor(...args);
}

const user = createInstance(User, "Alice", 30, "alice@example.com");
// user: User
```

### Implementation

```typescript
type ConstructorParameters<T extends abstract new (...args: any) => any> =
  T extends abstract new (...args: infer P) => any ? P : never;
```

---

## InstanceType\<T\>

Extracts the instance type of a constructor (class).

```typescript
class Container<T> {
  constructor(public value: T) {}
}

type StringContainer = InstanceType<typeof Container<string>>;
// Container<string>

// Practical usage
class EventBus {
  on(event: string, handler: () => void): void { /* ... */ }
  emit(event: string): void { /* ... */ }
}

function registerHandler(bus: InstanceType<typeof EventBus>): void {
  bus.on("test", () => {});
}
```

### Implementation

```typescript
type InstanceType<T extends abstract new (...args: any) => any> =
  T extends abstract new (...args: any) => infer R ? R : any;
```

---

## Awaited\<T\>

Unwraps the type of a `Promise` or `PromiseLike`, recursively.

```typescript
type A = Awaited<Promise<string>>;             // string
type B = Awaited<Promise<Promise<number>>>;    // number
type C = Awaited<string | Promise<number>>;    // string | number

// Real-world: type the result of async operations
async function getData(): Promise<Promise<string>> {
  return Promise.resolve("hello"); // nested promise
}

type DataType = Awaited<ReturnType<typeof getData>>; // string
```

### Implementation

```typescript
type Awaited<T> = T extends PromiseLike<infer U> ? Awaited<U> : T;
```

---

## Custom Utilities

### DeepOmit

```typescript
type DeepOmit<T, K extends string> = K extends `${infer First}.${infer Rest}`
  ? {
      [P in keyof T]: P extends First
        ? DeepOmit<T[P], Rest>
        : T[P];
    }
  : Omit<T, K>;

interface Config {
  server: {
    host: string;
    port: number;
    ssl: {
      cert: string;
      key: string;
    };
  };
  database: {
    url: string;
  };
}

type SafeConfig = DeepOmit<Config, "server.ssl">;
// {
//   server: { host: string; port: number; };
//   database: { url: string; };
// }
```

### Merge

```typescript
type Merge<A, B> = Omit<A, keyof B> & B;

interface Base {
  id: string;
  name: string;
}

interface Extended {
  name: number; // Override name type
  age: number;
}

type Merged = Merge<Base, Extended>;
// { id: string; name: number; age: number }
```

### StrictOmit

```typescript
type StrictOmit<T, K extends keyof T> = Omit<T, K>;

interface User {
  id: string;
  name: string;
  email: string;
}

// ✅ Valid keys
type A = StrictOmit<User, "id" | "name">;

// ❌ "phone" is not a key of User
// type B = StrictOmit<User, "phone">;
```

### ValueOf

```typescript
type ValueOf<T> = T[keyof T];

interface HTTPStatus {
  OK: 200;
  NotFound: 404;
  ServerError: 500;
}

type Status = ValueOf<HTTPStatus>; // 200 | 404 | 500
```

### OptionalExcept

```typescript
type OptionalExcept<T, K extends keyof T> = Omit<T, K> &
  Partial<Pick<T, K>>;

interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
}

// id is required, everything else is optional
type UserCreate = OptionalExcept<User, "id">;
// { id: string } & { name?: string; email?: string; avatar?: string }
```

---

## Best Practices

1. **Use built-in utilities** before writing custom ones — they're well-tested and
   well-understood.
2. **Combine utilities** for powerful types: `Partial<Pick<User, "name" | "email">>`.
3. **Prefer `Omit` over `Pick`** when you want most fields but need to exclude a few.
4. **Use `ReturnType` and `Parameters`** to extract types from existing functions
   without duplicating signatures.
5. **Document custom utilities** — non-standard types need explanations.

---

## Interview Questions

**Q1: What does `Partial<T>` do?**

It makes all properties of `T` optional. Implemented as `{ [P in keyof T]?: T[P] }`.

**Q2: How does `Exclude<T, U>` work?**

It distributes over the union `T`, keeping only members not assignable to `U`.
Implemented as `T extends U ? never : T`.

**Q3: How do you extract the return type of a function?**

Use `ReturnType<typeof fn>`. It uses `infer` to capture the return type.

**Q4: What is the difference between `Pick<T, K>` and `Omit<T, K>`?**

`Pick` keeps only the specified keys. `Omit` removes the specified keys. `Omit` is
defined in terms of `Pick` and `Exclude`.

**Q5: How do you unwrap nested Promises?**

Use `Awaited<T>`: `Awaited<Promise<Promise<string>>>` resolves to `string`.
