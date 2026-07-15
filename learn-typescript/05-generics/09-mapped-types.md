# 09 — Mapped Types

## Table of Contents

1. [Mapped Type Syntax](#mapped-type-syntax)
2. [Mapping Modifiers](#mapping-modifiers)
3. [keyof typeof Pattern](#keyof-typeof-pattern)
4. [Mapped Types with Constraints](#mapped-types-with-constraints)
5. [Mapped Types with Inference](#mapped-types-with-inference)
6. [Key Remapping (as clause)](#key-remapping)
7. [Real-World Mapped Types](#real-world-examples)
8. [Implementing Built-in Types](#implementing-built-in-types)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Mapped Type Syntax

A mapped type iterates over the keys of an existing type and produces a new type
with modified properties.

```typescript
// Basic syntax
type MappedType<T> = {
  [K in keyof T]: T[K];
};

// This is equivalent to just T (identity mapped type)
```

### Making All Properties Optional

```typescript
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};

interface User {
  id: string;
  name: string;
  email: string;
}

type PartialUser = MyPartial<User>;
// {
//   id?: string;
//   name?: string;
//   email?: string;
// }
```

### Making All Properties Required

```typescript
type MyRequired<T> = {
  [K in keyof T]-?: T[K];
};

interface Config {
  apiUrl?: string;
  timeout?: number;
}

type FullConfig = MyRequired<Config>;
// {
//   apiUrl: string;
//   timeout: number;
// }
```

### Making All Properties Readonly

```typescript
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};

type FrozenUser = MyReadonly<User>;
// {
//   readonly id: string;
//   readonly name: string;
//   readonly email: string;
// }
```

### Removing Readonly

```typescript
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

type MutableUser = Mutable<FrozenUser>;
// {
//   id: string;
//   name: string;
//   email: string;
// }
```

---

## Mapping Modifiers

### `+readonly` / `-readonly`

Controls whether properties are readonly:

```typescript
type AddReadonly<T> = {
  +readonly [K in keyof T]: T[K];
};

type RemoveReadonly<T> = {
  -readonly [K in keyof T]: T[K];
};

interface MutablePoint {
  x: number;
  y: number;
}

type ImmutablePoint = AddReadonly<MutablePoint>;
// { readonly x: number; readonly y: number; }

type BackToMutable = RemoveReadonly<ImmutablePoint>;
// { x: number; y: number; }
```

### `+optional` / `-optional`

Controls whether properties are optional:

```typescript
type AllOptional<T> = {
  [K in keyof T]+?: T[K];
};

type AllRequired<T> = {
  [K in keyof T]-?: T[K];
};

interface PartialUser {
  id?: string;
  name?: string;
  email?: string;
}

type StrictUser = AllRequired<PartialUser>;
// { id: string; name: string; email: string }
```

### Combined Modifiers

```typescript
type ReadonlyOptional<T> = {
  readonly [K in keyof T]?: T[K];
};

type MutableRequired<T> = {
  -readonly [K in keyof T]-?: T[K];
};

interface Example {
  a?: string;
  readonly b?: number;
  c: boolean;
}

type Test1 = ReadonlyOptional<Example>;
// { readonly a?: string; readonly b?: number; readonly c?: boolean }

type Test2 = MutableRequired<Example>;
// { a: string; b: number; c: boolean }
```

---

## keyof typeof Pattern

The `keyof typeof` pattern extracts the keys of a runtime value as a type.

### Basic Usage

```typescript
const HTTP_METHODS = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  DELETE: "DELETE",
  PATCH: "PATCH",
} as const;

type HttpMethod = keyof typeof HTTP_METHODS;
// "GET" | "POST" | "PUT" | "DELETE" | "PATCH"

// Usage
function request(method: HttpMethod, url: string): Promise<Response> {
  return fetch(url, { method });
}

request("GET", "/api/users");    // ✅
// request("HEAD", "/api/users"); // ❌ "HEAD" not in HttpMethod
```

### typeof for Class Instances

```typescript
class UserService {
  getUser(id: string): User { /* ... */ }
  createUser(data: CreateUserInput): User { /* ... */ }
  deleteUser(id: string): void { /* ... */ }
}

type UserServiceMethods = keyof UserService;
// "getUser" | "createUser" | "deleteUser"

// Use for method names
function callMethod<K extends keyof UserService>(
  service: UserService,
  method: K,
  ...args: Parameters<UserService[K]>
): ReturnType<UserService[K]> {
  return (service[method] as any)(...args);
}
```

### typeof with Const Assertions

```typescript
const ROUTES = {
  home: "/",
  users: "/users",
  userDetail: "/users/:id",
  posts: "/users/:id/posts",
  settings: "/settings",
} as const;

type Route = keyof typeof ROUTES;
// "home" | "users" | "userDetail" | "posts" | "settings"

type RoutePath = typeof ROUTES[Route];
// "/" | "/users" | "/users/:id" | "/users/:id/posts" | "/settings"
```

---

## Mapped Types with Constraints

You can constrain which keys are mapped using intersection with `keyof`.

```typescript
// Map only specific keys
type PickOnly<T, K extends keyof T> = {
  [P in K]: T[P];
};

interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

type UserPublic = PickOnly<User, "id" | "name" | "email">;
// { id: string; name: string; email: string }
```

### Constrained to Object Types

```typescript
type StringMap<T extends Record<string, unknown>> = {
  [K in keyof T]: string;
};

interface Config {
  apiUrl: string;
  timeout: number;
  retries: boolean;
}

type StringConfig = StringMap<Config>;
// { apiUrl: string; timeout: string; retries: string }
```

### Constrained Mapping with Transformation

```typescript
type Getters<T extends Record<string, unknown>> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

interface User {
  name: string;
  age: number;
  email: string;
}

type UserGetters = Getters<User>;
// {
//   getName: () => string;
//   getAge: () => number;
//   getEmail: () => string;
// }
```

---

## Mapped Types with Inference

Combine mapped types with conditional types and `infer` for powerful transformations.

```typescript
type UnwrapPromises<T> = {
  [K in keyof T]: T[K] extends Promise<infer U> ? U : T[K];
};

interface AsyncTask {
  user: Promise<User>;
  posts: Promise<Post[]>;
  config: Promise<Config>;
}

type SyncTask = UnwrapPromises<AsyncTask>;
// { user: User; posts: Post[]; config: Config }
```

### Deep Transformation

```typescript
type DeepReadonly<T> = T extends object
  ? { readonly [K in keyof T]: DeepReadonly<T[K]> }
  : T;

interface Nested {
  a: {
    b: {
      c: string;
    };
  };
  d: number[];
}

type Frozen = DeepReadonly<Nested>;
// {
//   readonly a: {
//     readonly b: {
//       readonly c: string;
//     };
//   };
//   readonly d: readonly number[];
// }
```

---

## Key Remapping

TypeScript 4.1+ allows remapping keys in mapped types using the `as` clause.

### Prefix/Suffix Keys

```typescript
type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};

type Setters<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (value: T[K]) => void;
};

interface User {
  name: string;
  age: number;
}

type UserGetters = Getters<User>;
// { getName: () => string; getAge: () => number }

type UserSetters = Setters<User>;
// { setName: (value: string) => void; setAge: (value: number) => void }
```

### Filtering Keys

```typescript
type StringKeys<T> = {
  [K in keyof T as T[K] extends string ? K : never]: T[K];
};

interface Mixed {
  name: string;
  age: number;
  email: string;
  active: boolean;
}

type OnlyStrings = StringKeys<Mixed>;
// { name: string; email: string }
```

### Filtering by Value Type

```typescript
type FunctionKeys<T> = {
  [K in keyof T as T[K] extends Function ? K : never]: T[K];
};

interface Service {
  getUser(id: string): User;
  name: string;
  deleteUser(id: string): void;
  version: number;
}

type OnlyFunctions = FunctionKeys<Service>;
// { getUser: (id: string) => User; deleteUser: (id: string) => void }
```

### Removing Specific Keys

```typescript
type OmitByKey<T, K extends keyof T> = {
  [P in keyof T as P extends K ? never : P]: T[P];
};

interface User {
  id: string;
  name: string;
  email: string;
  password: string;
}

type SafeUser = OmitByKey<User, "password">;
// { id: string; name: string; email: string }
```

### Union of New Keys

```typescript
type EventMap<T> = {
  [K in keyof T as `${string & K}Changed`]: {
    previous: T[K];
    current: T[K];
  };
};

interface Settings {
  theme: string;
  fontSize: number;
}

type ChangeEvents = EventMap<Settings>;
// {
//   themeChanged: { previous: string; current: string };
//   fontSizeChanged: { previous: number; current: number };
// }
```

---

## Real-World Examples

### API Query Builder

```typescript
type QueryOperators<T> = T extends string
  ? { eq?: string; contains?: string; startsWith?: string }
  : T extends number
    ? { eq?: number; gt?: number; lt?: number; between?: [number, number] }
    : T extends boolean
      ? { eq?: boolean }
      : never;

type QueryBuilder<T> = {
  [K in keyof T]?: QueryOperators<T[K]>;
};

interface Product {
  name: string;
  price: number;
  inStock: boolean;
}

type ProductQuery = QueryBuilder<Product>;
// {
//   name?: { eq?: string; contains?: string; startsWith?: string };
//   price?: { eq?: number; gt?: number; lt?: number; between?: [number, number] };
//   inStock?: { eq?: boolean };
// }
```

### Form State

```typescript
type FieldState<T> = {
  [K in keyof T]: {
    value: T[K];
    error: string | null;
    touched: boolean;
    dirty: boolean;
  };
};

interface LoginForm {
  email: string;
  password: string;
  rememberMe: boolean;
}

type LoginFormState = FieldState<LoginForm>;
// {
//   email: { value: string; error: string | null; touched: boolean; dirty: boolean };
//   password: { value: string; error: string | null; touched: boolean; dirty: boolean };
//   rememberMe: { value: boolean; error: string | null; touched: boolean; dirty: boolean };
// }
```

### Notification Types

```typescript
type NotificationPayload<T extends Record<string, unknown>> = {
  [K in keyof T]: {
    type: K;
    data: T[K];
    timestamp: number;
  };
};

interface Events {
  userCreated: { userId: string; name: string };
  orderPlaced: { orderId: string; total: number };
  paymentFailed: { transactionId: string; reason: string };
}

type Notifications = NotificationPayload<Events>;
// {
//   userCreated: { type: "userCreated"; data: { userId: string; name: string }; timestamp: number };
//   orderPlaced: { type: "orderPlaced"; data: { orderId: string; total: number }; timestamp: number };
//   paymentFailed: { type: "paymentFailed"; data: { transactionId: string; reason: string }; timestamp: number };
// }
```

---

## Implementing Built-in Types

### Partial

```typescript
type MyPartial<T> = {
  [K in keyof T]?: T[K];
};
```

### Required

```typescript
type MyRequired<T> = {
  [K in keyof T]-?: T[K];
};
```

### Readonly

```typescript
type MyReadonly<T> = {
  readonly [K in keyof T]: T[K];
};
```

### Pick

```typescript
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

### Record

```typescript
type MyRecord<K extends keyof any, V> = {
  [P in K]: V;
};
```

### Omit (using key remapping)

```typescript
type MyOmit<T, K extends keyof T> = {
  [P in keyof T as P extends K ? never : P]: T[P];
};
```

---

## Best Practices

1. **Use mapped types to transform existing types** rather than recreating them.
2. **Combine with conditional types** for powerful type transformations.
3. **Use key remapping (`as`)** to filter and transform keys.
4. **Keep mapped types shallow** unless deep transformation is explicitly needed.
5. **Name mapped types clearly** — their purpose should be obvious from the name.

---

## Interview Questions

**Q1: What is a mapped type?**

A mapped type iterates over the keys of an existing type using `[K in keyof T]` and
produces a new type with modified properties. It is the foundation of `Partial`,
`Required`, `Readonly`, `Pick`, and `Record`.

**Q2: How do you remove optionality in a mapped type?**

Use `-?`: `{ [K in keyof T]-?: T[K] }`. This is how `Required<T>` is implemented.

**Q3: What is the `as` clause in mapped types?**

The `as` clause (TypeScript 4.1+) allows key remapping. You can prefix, suffix,
filter, or transform keys.

**Q4: How does `keyof typeof` work?**

`typeof obj` gets the type of a runtime value. `keyof typeof obj` extracts the keys
of that type as a union of string literals.

**Q5: Can you filter keys in a mapped type?**

Yes. Use `as` with `never`: `[K in keyof T as Condition ? K : never]` keeps only keys
satisfying the condition.
