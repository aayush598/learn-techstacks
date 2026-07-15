# The `typeof` Operator in TypeScript

The `typeof` operator in TypeScript is a **type query** that retrieves the type of a variable, function, or import at the type level. It's different from JavaScript's `typeof` (which is a runtime operator) — TypeScript's `typeof` works at compile time to extract types.

---

## Table of Contents

1. [typeof in JavaScript vs TypeScript](#typeof-in-javascript-vs-typescript)
2. [typeof as a Type Query](#typeof-as-a-type-query)
3. [typeof with Variables](#typeof-with-variables)
4. [typeof with Imports](#typeof-with-imports)
5. [keyof typeof Pattern](#keyof-typeof-pattern)
6. [Const Assertions with typeof](#const-assertions-with-typeof)
7. [typeof for Configuration Objects](#typeof-for-configuration-objects)
8. [Type Inference with typeof](#type-inference-with-typeof)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## typeof in JavaScript vs TypeScript

### JavaScript typeof (runtime)

```typescript
// JavaScript typeof returns a string at runtime
typeof "hello"     // "string"
typeof 42          // "number"
typeof true        // "boolean"
typeof undefined   // "undefined"
typeof null        // "object" (historical bug)
typeof {}          // "object"
typeof []          // "object"
typeof function(){} // "function"
```

### TypeScript typeof (compile-time type query)

```typescript
const name = "Alice";
type NameType = typeof name; // string

const age = 30;
type AgeType = typeof age; // number

const config = {
  host: "localhost",
  port: 3000,
};
type ConfigType = typeof config; // { host: string; port: number }
```

### Key differences

| Aspect | JavaScript `typeof` | TypeScript `typeof` |
|---|---|---|
| When | Runtime | Compile-time |
| Returns | String (`"string"`, `"number"`, etc.) | Type (`string`, `number`, etc.) |
| Used in | Expressions | Type positions |
| Example | `typeof x` | `type T = typeof x` |

---

## typeof as a Type Query

Use `typeof` in type positions to extract the type of an existing variable or expression.

```typescript
// Extract type from a variable
const user = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  address: {
    street: "123 Main St",
    city: "Springfield",
  },
};

type UserType = typeof user;
// {
//   id: number;
//   name: string;
//   email: string;
//   address: { street: string; city: string };
// }

// Use the extracted type
function processUser(user: UserType) {
  console.log(user.name);
}

// Extract type from a function
function greet(name: string, age: number): string {
  return `Hello ${name}, age ${age}`;
}

type GreetType = typeof greet; // (name: string, age: number) => string
type GreetReturnType = ReturnType<typeof greet>; // string
type GreetParams = Parameters<typeof greet>; // [name: string, age: number]
```

### typeof with different value types

```typescript
// Primitives
const str = "hello";
type StrType = typeof str; // "hello" (literal type!)

const num = 42;
type NumType = typeof num; // 42

// Arrays
const arr = [1, 2, 3];
type ArrType = typeof arr; // number[]

// Tuples
const tuple = [1, "hello", true];
type TupleType = typeof tuple; // [number, string, boolean]

// Functions
function add(a: number, b: number) {
  return a + b;
}
type AddType = typeof add; // (a: number, b: number) => number

// Classes
class MyClass {
  x = 10;
  y = "hello";
}
type MyClassType = typeof MyClass; // typeof MyClass (constructor type)
type MyClassInstance = InstanceType<typeof MyClass>; // MyClass
```

---

## typeof with Variables

`typeof` is most commonly used to extract the type of a variable without manually defining the type.

```typescript
// Without typeof — you must define the type manually
interface User {
  id: number;
  name: string;
  email: string;
}

const user: User = { id: 1, name: "Alice", email: "alice@example.com" };
// Duplicate definition!

// With typeof — extract from the variable
const user = { id: 1, name: "Alice", email: "alice@example.com" };
type User = typeof user;
// Single source of truth!
```

### typeof with complex variables

```typescript
const defaultConfig = {
  database: {
    host: "localhost",
    port: 5432,
    ssl: false,
  },
  cache: {
    host: "localhost",
    port: 6379,
    ttl: 3600,
  },
  logging: {
    level: "info" as const,
    format: "json" as const,
  },
};

type Config = typeof defaultConfig;
// {
//   database: { host: string; port: number; ssl: boolean };
//   cache: { host: string; port: number; ttl: number };
//   logging: { level: "info"; format: "json" };
// }

// Use the type
function createConfig(overrides: Partial<Config>): Config {
  return { ...defaultConfig, ...overrides };
}
```

### typeof with const assertions

```typescript
const ROUTES = {
  home: "/",
  about: "/about",
  contact: "/contact",
  blog: "/blog",
} as const;

type Routes = typeof ROUTES;
// {
//   readonly home: "/";
//   readonly about: "/about";
//   readonly contact: "/contact";
//   readonly blog: "/blog";
// }

type RouteKey = keyof Routes; // "home" | "about" | "contact" | "blog"
type RouteValue = Routes[keyof Routes]; // "/" | "/about" | "/contact" | "/blog"
```

---

## typeof with Imports

You can use `typeof` to extract types from imported modules without importing the values.

```typescript
// utils.ts
export function formatDate(date: Date): string {
  return date.toLocaleDateString();
}

export function parseDate(str: string): Date {
  return new Date(str);
}

export const DEFAULT_LOCALE = "en-US";

// app.ts
import * as utils from "./utils";

// Extract the type of the entire module
type UtilsType = typeof utils;
// {
//   formatDate: (date: Date) => string;
//   parseDate: (str: string) => Date;
//   DEFAULT_LOCALE: string;
// }

// Extract a specific function's type
type FormatDateType = typeof utils.formatDate; // (date: Date) => string
```

### typeof with named imports

```typescript
import { formatDate, parseDate } from "./utils";

type FormatDateType = typeof formatDate; // (date: Date) => string
type ParseDateType = typeof parseDate; // (str: string) => Date
```

### typeof with default exports

```typescript
// myModule.ts
export default {
  name: "myModule",
  version: "1.0.0",
};

// app.ts
import myModule from "./myModule";
type MyModuleType = typeof myModule; // { name: string; version: string }
```

---

## keyof typeof Pattern

The `keyof typeof` pattern is one of the most common TypeScript patterns. It extracts the keys of a runtime value as a type.

```typescript
const COLORS = {
  red: "#FF0000",
  green: "#00FF00",
  blue: "#0000FF",
  white: "#FFFFFF",
  black: "#000000",
};

type ColorName = keyof typeof COLORS;
// "red" | "green" | "blue" | "white" | "black"

// Use for type-safe access
function getColor(name: ColorName): string {
  return COLORS[name];
}

getColor("red");    // ✅
getColor("green");  // ✅
// getColor("yellow"); // ❌ Compile error
```

### Practical example: API routes

```typescript
const API_ROUTES = {
  users: "/api/users",
  posts: "/api/posts",
  comments: "/api/comments",
  auth: "/api/auth",
} as const;

type APIRoute = keyof typeof API_ROUTES;
// "users" | "posts" | "comments" | "auth"

function fetchAPI(route: APIRoute) {
  return fetch(API_ROUTES[route]);
}

fetchAPI("users");  // ✅
fetchAPI("posts");  // ✅
// fetchAPI("invalid"); // ❌ Compile error
```

### With nested objects

```typescript
const CONFIG = {
  development: {
    apiUrl: "http://localhost:3000",
    debug: true,
  },
  production: {
    apiUrl: "https://api.example.com",
    debug: false,
  },
  test: {
    apiUrl: "http://localhost:3001",
    debug: true,
  },
};

type Environment = keyof typeof CONFIG;
// "development" | "production" | "test"

type ConfigForEnv<T extends Environment> = typeof CONFIG[T];
// ConfigForEnv<"development"> = { apiUrl: string; debug: boolean }
```

---

## Const Assertions with typeof

`as const` makes values deeply readonly and narrows literal types. Combined with `typeof`, it creates precise types.

```typescript
// Without as const
const STATUS = {
  loading: "LOADING",
  success: "SUCCESS",
  error: "ERROR",
};
type Status = typeof STATUS[keyof typeof STATUS]; // string (too broad!)

// With as const
const STATUS = {
  loading: "LOADING",
  success: "SUCCESS",
  error: "ERROR",
} as const;
type Status = typeof STATUS[keyof typeof STATUS]; // "LOADING" | "SUCCESS" | "ERROR"
```

### Array const assertions

```typescript
// Without as const
const ROLES = ["admin", "user", "guest"];
type Role = typeof ROLES[number]; // string

// With as const
const ROLES = ["admin", "user", "guest"] as const;
type Role = typeof ROLES[number]; // "admin" | "user" | "guest"
```

### Tuple const assertions

```typescript
const POINT = [10, 20] as const;
type Point = typeof POINT; // readonly [10, 20]
type X = Point[0]; // 10
type Y = Point[1]; // 20
```

### Deep const assertions

```typescript
const ROUTES = {
  home: "/",
  user: {
    list: "/users",
    detail: "/users/:id",
    edit: "/users/:id/edit",
  },
  post: {
    list: "/posts",
    detail: "/posts/:id",
  },
} as const;

type Routes = typeof ROUTES;
type UserRoutes = typeof ROUTES.user;
type UserDetail = typeof ROUTES.user.detail; // "/users/:id"
```

---

## typeof for Configuration Objects

`typeof` is perfect for creating types from configuration objects — single source of truth.

```typescript
// Define the config as a value
const DEFAULT_CONFIG = {
  api: {
    baseUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3,
  },
  auth: {
    tokenExpiry: 3600,
    refreshExpiry: 86400,
  },
  features: {
    darkMode: true,
    notifications: true,
    analytics: false,
  },
} as const;

// Extract the type
type AppConfig = typeof DEFAULT_CONFIG;

// Use the type for overrides
function createConfig(overrides: Partial<AppConfig>): AppConfig {
  return { ...DEFAULT_CONFIG, ...overrides };
}

// Use with environment-specific configs
type Environment = "development" | "production" | "test";
type EnvConfig = {
  [K in Environment]: Partial<AppConfig>;
};

const envConfigs: EnvConfig = {
  development: {
    api: { baseUrl: "http://localhost:3000" },
    features: { darkMode: false },
  },
  production: {
    api: { baseUrl: "https://api.production.com" },
  },
  test: {
    api: { baseUrl: "http://localhost:3001" },
  },
};
```

### Enum-like patterns with typeof

```typescript
// Instead of enums, use const objects with typeof
const HttpMethod = {
  GET: "GET",
  POST: "POST",
  PUT: "PUT",
  DELETE: "DELETE",
  PATCH: "PATCH",
} as const;

type HttpMethod = typeof HttpMethod[keyof typeof HttpMethod];
// "GET" | "POST" | "PUT" | "DELETE" | "PATCH"

function request(method: HttpMethod, url: string) {
  console.log(`${method} ${url}`);
}

request("GET", "/api/users");    // ✅
request("POST", "/api/users");   // ✅
// request("OPTIONS", "/api/users"); // ❌ Compile error
```

---

## Type Inference with typeof

TypeScript can infer types from `typeof` in various contexts.

### Inferred return types

```typescript
function createUser(name: string, age: number) {
  return {
    id: Math.random().toString(36),
    name,
    age,
    createdAt: new Date(),
  };
}

type User = ReturnType<typeof createUser>;
// { id: string; name: string; age: number; createdAt: Date }
```

### Inferred parameter types

```typescript
function process(data: { items: string[]; count: number }) {
  return data.items.slice(0, data.count);
}

type ProcessData = Parameters<typeof process>[0];
// { items: string[]; count: number }
```

### Inferred from class instances

```typescript
class User {
  constructor(
    public name: string,
    public age: number,
    public email: string
  ) {}
}

const user = new User("Alice", 30, "alice@example.com");
type UserType = typeof user; // User (the instance type, not the constructor)

// For the constructor type:
type UserConstructor = typeof User;
// new (name: string, age: number, email: string) => User

// For the instance type:
type UserInstance = InstanceType<typeof User>; // User
```

### Inferred from module namespaces

```typescript
// math.ts
export function add(a: number, b: number) { return a + b; }
export function subtract(a: number, b: number) { return a - b; }
export const PI = 3.14159;

// app.ts
import * as math from "./math";
type MathModule = typeof math;
// { add: (a: number, b: number) => number; subtract: (a: number, b: number) => number; PI: number }
```

---

## Best Practices

1. **Use `typeof` to avoid duplicating types** — define the value, extract the type
2. **Use `as const` with `typeof`** — for literal types and readonly arrays
3. **Use `keyof typeof`** — for extracting keys from runtime objects
4. **Use `typeof` for config objects** — single source of truth pattern
5. **Use `ReturnType<typeof fn>`** — for extracting function return types
6. **Use `typeof` with imports** — for extracting types from modules
7. **Don't overuse `typeof`** — sometimes a manual interface is clearer

---

## Interview Questions

### Q1: What is the difference between `typeof` in JavaScript and TypeScript?

**Answer:** JavaScript's `typeof` is a runtime operator that returns a string like `"string"`, `"number"`, `"object"`, etc. TypeScript's `typeof` is a compile-time type query that extracts the type of a variable or expression. JavaScript `typeof` is used in expressions; TypeScript `typeof` is used in type positions.

### Q2: What is the `keyof typeof` pattern?

**Answer:** `keyof typeof obj` extracts the keys of a runtime object as a union of string literal types. For example, if `const STATUS = { loading: "LOADING", success: "SUCCESS" }`, then `keyof typeof STATUS` is `"loading" | "success"`. This is used for type-safe access to object keys.

### Q3: How does `typeof` work with `as const`?

**Answer:** `as const` makes values deeply readonly and narrows literal types. When combined with `typeof`, you get precise types like `"LOADING" | "SUCCESS"` instead of `string`. This is useful for creating enum-like patterns without actual enums.

### Q4: Can you use `typeof` on an imported module?

**Answer:** Yes. `typeof importedModule` extracts the type of the entire module. You can then use indexed access or `keyof` to extract specific types. This is useful for extracting types from third-party libraries without re-exporting them.

### Q5: How do you extract a function's return type using `typeof`?

**Answer:** Use `ReturnType<typeof functionName>`. This extracts the return type of the function without manually defining it. For example, `type Result = ReturnType<typeof fetchUser>` gives you the return type of the `fetchUser` function.

### Q6: When would you use `typeof` vs manually defining a type?

**Answer:** Use `typeof` when you have an existing value (variable, function, class instance) and want to extract its type without duplicating the definition. It's especially useful for config objects, default values, and imported modules. Use manual type definitions when you need to document the shape explicitly or when the type doesn't correspond to a runtime value.
