# 06 — Generic Defaults

## Table of Contents

1. [Default Type Parameters](#default-type-parameters)
2. [Default with Constraints](#default-with-constraints)
3. [Default in Interfaces](#default-in-interfaces)
4. [Default in Classes](#default-in-classes)
5. [Default in Functions](#default-in-functions)
6. [Interaction with Inference](#interaction-with-inference)
7. [Real-World Default Patterns](#real-world-defaults)
8. [Partial<T> and Built-in Types with Defaults](#built-in-with-defaults)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Default Type Parameters

Default type parameters provide a fallback type when no type argument is supplied and
TypeScript cannot infer one. They follow the same syntax as default function parameters.

```typescript
// T defaults to string if not specified
function identity<T = string>(value: T): T {
  return value;
}

// Uses default (string)
const a = identity("hello");        // T = string (inferred)

// Explicit override
const b = identity<number>(42);     // T = number

// Default when no argument
const c = identity("default");      // T = string (inferred)
```

### When Defaults Kick In

The default is used when:
1. No type argument is provided **AND**
2. TypeScript cannot infer the type from the arguments

```typescript
function createState<T = string>(initial?: T): T {
  return (initial ?? "default") as T;
}

// Inferred from argument
const a = createState(42);          // T = number

// Default used — no argument, no inference
const b = createState();            // T = string (default)

// Explicit override
const c = createState<boolean>();   // T = boolean
```

---

## Default with Constraints

You can combine defaults and constraints. The default must satisfy the constraint.

```typescript
// Default unknown satisfies the constraint object
function process<T extends object = Record<string, unknown>>(
  data: T
): T {
  return data;
}

// Uses default
const data1 = process({ key: "value" }); // { key: string }

// Explicit type
const data2 = process<User>({ id: "1", name: "Alice" });
// data2: User
```

### Default Must Satisfy Constraint

```typescript
// ✅ Default satisfies constraint
function wrap<T extends HasLength = string>(value: T): T {
  return value;
}

interface HasLength {
  length: number;
}

// ❌ This would be an error — number doesn't satisfy HasLength
// function broken<T extends HasLength = number>(value: T): T { ... }
```

### Multiple Defaults with Constraints

```typescript
interface ApiResponse<TData, TError = Error, TMeta = Record<string, unknown>> {
  data: TData;
  error: TError | null;
  meta: TMeta;
  status: number;
}

// All defaults
const response1: ApiResponse<string> = {
  data: "hello",
  error: null,
  meta: {},
  status: 200,
};

// Override first two, default meta
const response2: ApiResponse<User[], ApiError> = {
  data: [],
  error: { code: "NOT_FOUND", message: "No users" },
  meta: {},
  status: 404,
};

// Override all three
const response3: ApiResponse<User[], ApiError, { requestId: string }> = {
  data: [],
  error: null,
  meta: { requestId: "abc-123" },
  status: 200,
};
```

---

## Default in Interfaces

Interfaces support default type parameters, making them highly reusable.

```typescript
interface Cache<TValue, TKey = string, TOptions = { ttl: number }> {
  get(key: TKey): TValue | undefined;
  set(key: TKey, value: TValue, options?: TOptions): void;
  delete(key: TKey): boolean;
  has(key: TKey): boolean;
}

// Uses defaults for TKey (string) and TOptions ({ ttl: number })
const stringCache: Cache<number> = {
  get(key) { return undefined; },
  set(key, value, options) { /* options.ttl is number */ },
  delete(key) { return false; },
  has(key) { return false; },
};

// Override TKey to number
const numericCache: Cache<string, number> = {
  get(key) { return undefined; },
  set(key, value) { /* ... */ },
  delete(key) { return false; },
  has(key) { return false; },
};
```

### Cascading Defaults

```typescript
interface EventPayload<
  TName extends string = "default",
  TData = unknown,
  TSource = "system"
> {
  name: TName;
  data: TData;
  source: TSource;
  timestamp: number;
}

// All defaults
const event1: EventPayload = {
  name: "default",
  data: null,
  source: "system",
  timestamp: Date.now(),
};

// Override name and data
const event2: EventPayload<"userCreated", { userId: string }> = {
  name: "userCreated",
  data: { userId: "123" },
  source: "system",
  timestamp: Date.now(),
};

// Override all
const event3: EventPayload<"orderPlaced", Order, "api"> = {
  name: "orderPlaced",
  data: order,
  source: "api",
  timestamp: Date.now(),
};
```

---

## Default in Classes

Generic classes with defaults allow creating instances without specifying types when
the default is appropriate.

```typescript
class Result<TSuccess = string, TError = Error> {
  constructor(
    private success: TSuccess | null,
    private error: TError | null
  ) {}

  isSuccess(): this is { success: TSuccess } {
    return this.success !== null;
  }

  isError(): this is { error: TError } {
    return this.error !== null;
  }

  unwrap(): TSuccess {
    if (this.success === null) {
      throw new Error("Called unwrap on error result");
    }
    return this.success;
  }

  unwrapOr(defaultValue: TSuccess): TSuccess {
    return this.success ?? defaultValue;
  }
}

// Default: Result<string, Error>
const success = new Result("Done", null);
if (success.isSuccess()) {
  console.log(success.unwrap().toUpperCase()); // "DONE"
}

// Override both
interface ApiError {
  code: number;
  message: string;
}

const errorResult = new Result<User[], ApiError>(null, {
  code: 404,
  message: "Not found",
});

if (errorResult.isError()) {
  console.log(errorResult.error.code); // 404
}
```

### Class with Complex Defaults

```typescript
class EventBus<
  TEvents extends Record<string, unknown> = Record<string, unknown>,
  TContext = Record<string, never>
> {
  private listeners = new Map<keyof TEvents, Set<Function>>();
  private context: TContext;

  constructor(context?: TContext) {
    this.context = (context ?? {}) as TContext;
  }

  on<K extends keyof TEvents>(
    event: K,
    handler: (payload: TEvents[K], ctx: TContext) => void
  ): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(handler);
  }

  emit<K extends keyof TEvents>(event: K, payload: TEvents[K]): void {
    this.listeners.get(event)?.forEach((fn) => fn(payload, this.context));
  }
}

// Simple usage with defaults
const bus = new EventBus();
bus.on("anything", (payload) => console.log(payload));

// Typed usage
interface AppEvents {
  login: { userId: string };
  logout: { userId: string };
}

const appBus = new EventBus<AppEvents, { requestId: string }>({
  requestId: "abc",
});

appBus.on("login", (payload, ctx) => {
  console.log(`${payload.userId} logged in, request: ${ctx.requestId}`);
});
```

---

## Default in Functions

Function generics with defaults reduce verbosity for common cases.

```typescript
function createStore<TState = Record<string, unknown>>(
  initialState: TState
): {
  getState: () => TState;
  setState: (updater: TState | Partial<TState>) => void;
} {
  let state = { ...initialState };
  return {
    getState: () => state,
    setState: (updater) => {
      if (typeof updater === "object" && updater !== null) {
        state = { ...state, ...updater };
      } else {
        state = updater as TState;
      }
    },
  };
}

// Default TState = Record<string, unknown>
const store1 = createStore({ count: 0 });
store1.getState();       // { count: number }

// Explicit type
interface AppState {
  user: User | null;
  theme: "light" | "dark";
  notifications: string[];
}

const store2 = createStore<AppState>({
  user: null,
  theme: "light",
  notifications: [],
});
```

### Function with Multiple Defaults

```typescript
function buildUrl<
  TBase extends string = "https://api.example.com",
  TPath extends string = "/"
>(base: TBase, path: TPath): `${TBase}${TPath}` {
  return `${base}${path}` as `${TBase}${TPath}`;
}

// All defaults (conceptual — inference provides the literal types)
const url1 = buildUrl("https://api.example.com", "/users");
// "https://api.example.com/users"

const url2 = buildUrl("http://localhost:3000", "/api/data");
// "http://localhost:3000/api/data"
```

---

## Interaction with Inference

TypeScript uses a priority order: **inference > explicit type argument > default**.

```typescript
function create<T = "default">(value?: T): T {
  return (value ?? "default") as T;
}

// 1. Inferred from argument
const a = create(42);            // T = number

// 2. Explicit type argument
const b = create<string>();     // T = string

// 3. Default — no argument, no explicit type
const c = create();             // T = "default"
```

### Inference Overrides Default

```typescript
function pair<T = string>(a: T, b: T): [T, T] {
  return [a, b];
}

// Inferred from arguments — default is ignored
const p1 = pair(1, 2);          // [number, number]
const p2 = pair(true, false);   // [boolean, boolean]

// Default used when no arguments
const p3 = pair<string>();      // [string, string]
```

### When Inference Gives Union Instead of Expected Type

```typescript
function createTuple<T = string>(a: T, b: T): [T, T] {
  return [a, b];
}

// Inferred as [string | number, string | number] — not ideal
const t1 = createTuple("hello", 42);

// Provide explicit type to avoid union
const t2 = createTuple<string | number>("hello", 42);
// Still a union, but explicit

// Use overloads or separate parameters for independent types
function createTuple2<T, U>(a: T, b: U): [T, U] {
  return [a, b];
}
const t3 = createTuple2("hello", 42); // [string, number]
```

---

## Real-World Default Patterns

### REST Client with Defaults

```typescript
interface RestConfig<
  TBaseUrl extends string = "https://api.example.com",
  THeaders extends Record<string, string> = Record<string, string>
> {
  baseUrl: TBaseUrl;
  headers: THeaders;
  timeout?: number;
  retries?: number;
}

function createClient<TConfig extends RestConfig>(
  config: TConfig
): {
  get: <T>(path: string) => Promise<T>;
  post: <T>(path: string, body: unknown) => Promise<T>;
} {
  return {
    get: async (path) => {
      const response = await fetch(`${config.baseUrl}${path}`, {
        headers: config.headers,
      });
      return response.json();
    },
    post: async (path, body) => {
      const response = await fetch(`${config.baseUrl}${path}`, {
        method: "POST",
        headers: { ...config.headers, "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      return response.json();
    },
  };
}

const client = createClient({
  baseUrl: "https://api.myapp.com",
  headers: { Authorization: "Bearer token123" },
});

const users = await client.get<User[]>("/users");
```

### Form Builder with Defaults

```typescript
interface FieldConfig<
  TType extends string = "text",
  TValue = string,
  TValidations = {}
> {
  name: string;
  type: TType;
  label: string;
  defaultValue?: TValue;
  validations?: TValidations;
  required?: boolean;
}

function createField<
  TType extends string = "text",
  TValue = string,
  TValidations = {}
>(
  config: FieldConfig<TType, TValue, TValidations>
): FieldConfig<TType, TValue, TValidations> {
  return config;
}

// Default type
const nameField = createField({
  name: "name",
  type: "text",
  label: "Full Name",
  required: true,
});

// Override types
const ageField = createField<"number", number, { min: number; max: number }>({
  name: "age",
  type: "number",
  label: "Age",
  defaultValue: 0,
  validations: { min: 0, max: 150 },
});
```

---

## Partial<T> and Built-in Types with Defaults

Many built-in utility types accept optional type parameters with defaults.

### Partial<T>

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  age: number;
}

// All properties optional
function updateUser(id: string, updates: Partial<User>): Promise<User> {
  return fetch(`/api/users/${id}`, {
    method: "PATCH",
    body: JSON.stringify(updates),
  }).then((r) => r.json());
}

// ✅ All valid — each field is optional
updateUser("1", { name: "Bob" });
updateUser("1", { email: "bob@example.com" });
updateUser("1", { age: 25, name: "Bob" });
// updateUser("1", { id: "2" }); // ❌ id is readonly in Partial
```

### Required<T>

```typescript
interface Config {
  apiUrl?: string;
  timeout?: number;
  retries?: number;
}

// All properties required
function initApp(config: Required<Config>): void {
  console.log(config.apiUrl);   // string (guaranteed)
  console.log(config.timeout);  // number (guaranteed)
  console.log(config.retries);  // number (guaranteed)
}

initApp({
  apiUrl: "https://api.example.com",
  timeout: 5000,
  retries: 3,
});
```

### Record<K, V> with Defaults

```typescript
// V defaults to never if not provided (in some implementations)
// In practice, V is always provided
type UserRoles = Record<"admin" | "user" | "guest", string[]>;

const roles: UserRoles = {
  admin: ["read", "write", "delete"],
  user: ["read", "write"],
  guest: ["read"],
};
```

### Pick<T, K> and Omit<T, K>

```typescript
interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

// Only specific fields
type UserSummary = Pick<User, "id" | "name" | "email">;

// Without sensitive fields
type UserPublic = Omit<User, "password">;

function toPublic(user: User): UserPublic {
  const { password, ...publicUser } = user;
  return publicUser;
}
```

### Readonly<T>

```typescript
interface GameState {
  score: number;
  level: number;
  lives: number;
}

const state: Readonly<GameState> = {
  score: 0,
  level: 1,
  lives: 3,
};

// state.score = 10; // ❌ Cannot assign to 'score' because it is a read-only property

// To update, create a new object
const newState: GameState = { ...state, score: 10 };
```

---

## Best Practices

1. **Use defaults for the most common case** — reduce boilerplate for the 80% case.
2. **Ensure defaults satisfy constraints** — TypeScript will error if they don't.
3. **Don't over-default** — if the user must provide a type, don't default to
   something misleading.
4. **Document the default** — JSDoc should explain what the default is and why.
5. **Consider inference priority** — the default is only used when inference and
   explicit arguments both fail.

---

## Interview Questions

**Q1: When does a default type parameter kick in?**

When no explicit type argument is provided AND TypeScript cannot infer the type from
the function arguments or context.

**Q2: Can a default type parameter violate a constraint?**

No. TypeScript requires the default to satisfy the constraint. `<T extends object = number>`
is an error because `number` doesn't satisfy `object` (in strict mode).

**Q3: How do defaults interact with inference?**

Inference takes priority. If TypeScript can infer the type from arguments, the default
is ignored. The default is only a fallback.

**Q4: Can you have defaults on all parameters of a generic interface?**

Yes. `interface Response<T = string, E = Error, M = {}>` is valid. Each parameter
defaults independently.

**Q5: What is `Partial<T>` and how does it relate to defaults?**

`Partial<T>` makes all properties optional. It's a built-in mapped type that doesn't
have a default type parameter itself, but is commonly used in generic contexts where
optional overrides are needed.
