# Advanced TypeScript Patterns

## Table of Contents

- [Result/Either Pattern](#resul Either-pattern)
- [Algebraic Data Types](#algebraic-data-types)
- [Builder with Type-State](#builder-with-type-state)
- [Phantom Types](#phantom-types)
- [Type-Safe State Machines](#type-safe-state-machines)
- [Type-Safe SQL Builders](#type-safe-sql-builders)
- [Type-Safe Routing](#type-safe-routing)
- [Type-Safe i18n](#type-safe-i18n)
- [Advanced Middleware Patterns](#advanced-middleware-patterns)
- [Interview Questions](#interview-questions)

---

## Result/Either Pattern

```typescript
// Functional error handling without exceptions
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Result constructors
function Ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Result operations
function map<T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> {
  return result.ok ? Ok(fn(result.value)) : result;
}

function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return result.ok ? fn(result.value) : result;
}

function mapError<T, E, F>(result: Result<T, E>, fn: (error: E) => F): Result<T, F> {
  return result.ok ? result : Err(fn(result.error));
}

function unwrap<T, E>(result: Result<T, E>): T {
  if (result.ok) return result.value;
  throw result.error;
}

function unwrapOr<T, E>(result: Result<T, E>, defaultValue: T): T {
  return result.ok ? result.value : defaultValue;
}

// Usage
function divide(a: number, b: number): Result<number, string> {
  if (b === 0) return Err("Division by zero");
  return Ok(a / b);
}

function parseJSON<T>(json: string): Result<T, Error> {
  try {
    return Ok(JSON.parse(json) as T);
  } catch (error) {
    return Err(error as Error);
  }
}

// Chaining operations
const result = pipe(
  divide(10, 2),
  (r) => map(r, (n) => n * 10),
  (r) => map(r, (n) => n.toString()),
  (r) => mapError(r, (e) => new Error(e))
);

// pipe utility
function pipe<T>(value: T, ...fns: Array<(arg: T) => T>): T {
  return fns.reduce((acc, fn) => fn(acc), value);
}

// Async result
async function asyncDivide(a: number, b: number): Promise<Result<number, string>> {
  if (b === 0) return Err("Division by zero");
  return Ok(a / b);
}

async function asyncMap<T, U, E>(
  result: Promise<Result<T, E>>,
  fn: (value: T) => U | Promise<U>
): Promise<Result<U, E>> {
  const r = await result;
  return r.ok ? Ok(await fn(r.value)) : r;
}
```

---

## Algebraic Data Types

```typescript
// Sum types (discriminated unions)
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

// Exhaustive pattern matching
function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return 0.5 * shape.base * shape.height;
    default:
      const _exhaustive: never = shape;
      return _exhaustive;
  }
}

// Generic sum type
type Either<L, R> =
  | { tag: "left"; value: L }
  | { tag: "right"; value: R };

function Left<L>(value: L): Either<L, never> {
  return { tag: "left", value };
}

function Right<R>(value: R): Either<never, R> {
  return { tag: "right", value };
}

// Product types with generics
type Pair<A, B> = [A, B];
type Triple<A, B, C> = [A, B, C];

// Maybe type
type Maybe<T> = T | null | undefined;

function mapMaybe<T, U>(value: Maybe<T>, fn: (value: T) => U): Maybe<U> {
  return value != null ? fn(value) : value;
}

// List type
type NonEmptyArray<T> = [T, ...T[]];

function head<T>(array: NonEmptyArray<T>): T {
  return array[0];
}

// Recursive types
type JSONValue =
  | string
  | number
  | boolean
  | null
  | JSONValue[]
  | { [key: string]: JSONValue };

type Tree<T> =
  | { kind: "leaf"; value: T }
  | { kind: "node"; value: T; children: Tree<T>[] };

function treeSize<T>(tree: Tree<T>): number {
  switch (tree.kind) {
    case "leaf":
      return 1;
    case "node":
      return 1 + tree.children.reduce((sum, child) => sum + treeSize(child), 0);
  }
}
```

---

## Builder with Type-State

```typescript
// Compile-time enforcement of build steps
type BuilderState = {
  hasUrl: boolean;
  hasMethod: boolean;
  hasHeaders: boolean;
};

class HTTPBuilder<TState extends BuilderState = {
  hasUrl: false;
  hasMethod: false;
  hasHeaders: false;
}> {
  private config: {
    url?: string;
    method?: string;
    headers?: Record<string, string>;
    body?: unknown;
  } = {};

  url(url: string): HTTPBuilder<TState & { hasUrl: true }> {
    this.config.url = url;
    return this as any;
  }

  method(method: string): HTTPBuilder<TState & { hasMethod: true }> {
    this.config.method = method;
    return this as any;
  }

  headers(headers: Record<string, string>): HTTPBuilder<TState & { hasHeaders: true }> {
    this.config.headers = headers;
    return this as any;
  }

  body(body: unknown): this {
    this.config.body = body;
    return this;
  }

  build(this: HTTPBuilder<{ hasUrl: true; hasMethod: true }>): Request {
    return {
      url: this.config.url!,
      method: this.config.method!,
      headers: this.config.headers ?? {},
      body: this.config.body,
    } as Request;
  }
}

// Usage
const request = new HTTPBuilder()
  .url("https://api.example.com")  // ✅ hasUrl = true
  .method("POST")                   // ✅ hasMethod = true
  .headers({ "Content-Type": "application/json" })
  .body({ name: "Alice" })
  .build();                         // ✅ All required fields present

// new HTTPBuilder().build(); // ❌ Error: missing url and method
// new HTTPBuilder().url("x").build(); // ❌ Error: missing method
```

---

## Phantom Types

```typescript
// Types that exist only at compile time
type Validated = { readonly _brand: unique symbol };
type Unvalidated = { readonly _brand: unique symbol };
type Sanitized = { readonly _brand: unique symbol };

// Type-safe validation
function validateEmail(email: string): Result<Validated, string> {
  if (!email.includes("@")) return Err("Invalid email");
  return Ok(email as any);
}

function sanitizeInput(input: string): Sanitized {
  return input.replace(/[<>]/g, "") as any;
}

// Functions that require specific types
function sendEmail(to: Validated, subject: string, body: string): void {
  console.log(`Sending email to ${to}`);
}

function saveToDatabase(data: Sanitized): void {
  console.log("Saving:", data);
}

// Usage
const email = "user@example.com";
const validated = validateEmail(email);
if (validated.ok) {
  sendEmail(validated.value, "Hello", "World"); // ✅
}

// sendEmail("user@example.com", "Hello", "World"); // ❌ Error: string is not Validated

const sanitized = sanitizeInput("<script>alert('xss')</script>");
saveToDatabase(sanitized); // ✅

// saveToDatabase("<script>"); // ❌ Error: string is not Sanitized

// Phantom types for units
type Meters = { readonly _unit: "meters" };
type Seconds = { readonly _unit: "seconds" };
type MetersPerSecond = { readonly _unit: "m/s" };

function meters(value: number): Meters { return value as any; }
function seconds(value: number): Seconds { return value as any; }

function speed(distance: Meters, time: Seconds): MetersPerSecond {
  return (distance as any / time as any) as any;
}

function distance traveled(speed: MetersPerSecond, time: Seconds): Meters {
  return (speed as any * time as any) as any;
}

const d = distance(speed(meters(100), seconds(10)), seconds(5)); // 50 meters
// const bad = distance(seconds(10), meters(100)); // ❌ Type error
```

---

## Type-Safe State Machines

```typescript
// State machine with compile-time safety
type StateConfig = {
  [state: string]: {
    [event: string]: {
      target: string;
      guard?: (context: any) => boolean;
      action?: (context: any) => any;
    };
  };
};

type StateOf<T extends StateConfig> = keyof T & string;
type EventOf<T extends StateConfig> = {
  [S in keyof T]: keyof T[S];
}[keyof T] & string;

class TypedStateMachine<T extends StateConfig> {
  private state: StateOf<T>;
  private context: any;
  private transitions: T;
  private listeners: Array<(state: StateOf<T>, context: any) => void> = [];

  constructor(transitions: T, initial: StateOf<T>, context: any = {}) {
    this.transitions = transitions;
    this.state = initial;
    this.context = context;
  }

  getState(): StateOf<T> {
    return this.state;
  }

  getContext(): Readonly<any> {
    return this.context;
  }

  send(event: EventOf<T>): StateOf<T> {
    const transition = this.transitions[this.state]?.[event];
    if (!transition) {
      throw new Error(`Invalid event '${event}' in state '${this.state}'`);
    }

    // Check guard
    if (transition.guard && !transition.guard(this.context)) {
      throw new Error(`Guard failed for event '${event}' in state '${this.state}'`);
    }

    // Execute action
    if (transition.action) {
      const newContext = transition.action(this.context);
      if (newContext) {
        this.context = { ...this.context, ...newContext };
      }
    }

    this.state = transition.target as StateOf<T>;
    this.listeners.forEach((l) => l(this.state, this.context));
    return this.state;
  }

  canHandle(event: EventOf<T>): boolean {
    return event in (this.transitions[this.state] ?? {});
  }

  subscribe(listener: (state: StateOf<T>, context: any) => void): () => void {
    this.listeners.push(listener);
    return () => {
      this.listeners = this.listeners.filter((l) => l !== listener);
    };
  }
}

// Usage
type OrderStates = {
  pending: {
    confirm: { target: "confirmed"; action: (ctx: any) => { confirmedAt: Date } };
    cancel: { target: "cancelled" };
  };
  confirmed: {
    ship: { target: "shipped"; action: (ctx: any) => { shippedAt: Date } };
    cancel: { target: "cancelled" };
  };
  shipped: {
    deliver: { target: "delivered"; action: (ctx: any) => { deliveredAt: Date } };
  };
  delivered: {};
  cancelled: {};
};

const orderMachine = new TypedStateMachine<OrderStates>(
  {
    pending: {
      confirm: { target: "confirmed", action: () => ({ confirmedAt: new Date() }) },
      cancel: { target: "cancelled" },
    },
    confirmed: {
      ship: { target: "shipped", action: () => ({ shippedAt: new Date() }) },
      cancel: { target: "cancelled" },
    },
    shipped: {
      deliver: { target: "delivered", action: () => ({ deliveredAt: new Date() }) },
    },
    delivered: {},
    cancelled: {},
  },
  "pending"
);

orderMachine.subscribe((state, ctx) => console.log(`State: ${state}`, ctx));
orderMachine.send("confirm"); // State: confirmed { confirmedAt: ... }
orderMachine.send("ship");    // State: shipped { shippedAt: ... }
orderMachine.send("deliver"); // State: delivered { deliveredAt: ... }
```

---

## Type-Safe SQL Builders

```typescript
// Compile-time safe SQL query builder
interface TableSchema {
  [tableName: string]: {
    [columnName: string]: any;
  };
}

class SQLBuilder<TSchema extends TableSchema> {
  private query = "";
  private params: unknown[] = [];

  select<K extends keyof TSchema>(
    table: K,
    ...columns: Array<keyof TSchema[K] & string>
  ): this {
    this.query = `SELECT ${columns.join(", ")} FROM ${table as string}`;
    return this;
  }

  where(
    condition: string,
    ...values: unknown[]
  ): this {
    this.query += ` WHERE ${condition}`;
    this.params.push(...values);
    return this;
  }

  orderBy(
    column: string,
    direction: "ASC" | "DESC" = "ASC"
  ): this {
    this.query += ` ORDER BY ${column} ${direction}`;
    return this;
  }

  limit(n: number): this {
    this.query += ` LIMIT ${n}`;
    return this;
  }

  build(): { sql: string; params: unknown[] } {
    return { sql: this.query, params: this.params };
  }
}

// Schema definition
interface MySchema {
  users: {
    id: string;
    name: string;
    email: string;
    age: number;
  };
  posts: {
    id: string;
    title: string;
    content: string;
    authorId: string;
  };
}

// Usage
const builder = new SQLBuilder<MySchema>();
const query = builder
  .select("users", "id", "name", "email")
  .where("age > ?", 18)
  .orderBy("name")
  .limit(10)
  .build();

// builder.select("users", "invalid"); // ❌ Error: "invalid" is not a column of users
// builder.select("invalid", "id"); // ❌ Error: "invalid" is not a table
```

---

## Type-Safe Routing

```typescript
// Type-safe route definitions
type RouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof RouteParams<Rest>]: string }
    : T extends `${string}:${infer Param}`
      ? { [K in Param]: string }
      : {};

interface Route<TPath extends string> {
  path: TPath;
  params: RouteParams<TPath>;
  handler: (params: RouteParams<TPath>) => any;
}

function route<TPath extends string>(
  path: TPath,
  handler: (params: RouteParams<TPath>) => any
): Route<TPath> {
  return { path, params: {} as RouteParams<TPath>, handler };
}

// Usage
const userRoute = route("/users/:id", (params) => {
  console.log(params.id); // ✅ TypeScript knows id is string
});

const postRoute = route("/users/:userId/posts/:postId", (params) => {
  console.log(params.userId);  // ✅
  console.log(params.postId);  // ✅
});

// Type-safe router
class TypedRouter {
  private routes: Array<{ pattern: RegExp; handler: (params: any) => any }> = [];

  add<TPath extends string>(
    path: TPath,
    handler: (params: RouteParams<TPath>) => any
  ): void {
    const pattern = path.replace(/:(\w+)/g, "(?<$1>[^/]+)");
    this.routes.push({
      pattern: new RegExp(`^${pattern}$`),
      handler,
    });
  }

  match(url: string): { handler: (params: any) => any; params: Record<string, string> } | null {
    for (const route of this.routes) {
      const match = url.match(route.pattern);
      if (match?.groups) {
        return { handler: route.handler, params: match.groups };
      }
    }
    return null;
  }
}
```

---

## Type-Safe i18n

```typescript
// Type-safe internationalization
type Translations = {
  [locale: string]: {
    [key: string]: string | ((params: Record<string, string>) => string);
  };
};

class I18n<T extends Translations> {
  private translations: T;
  private locale: keyof T;

  constructor(translations: T, locale: keyof T) {
    this.translations = translations;
    this.locale = locale;
  }

  t<K extends keyof T[typeof locale] & string>(
    key: K,
    params?: T[typeof locale][K] extends (p: infer P) => string
      ? P extends Record<string, string>
        ? P
        : never
      : never
  ): string {
    const value = this.translations[this.locale][key];
    if (typeof value === "function") {
      return value(params!);
    }
    return value as string;
  }

  setLocale(locale: keyof T): void {
    this.locale = locale;
  }
}

// Usage
const translations = {
  en: {
    greeting: "Hello, {name}!",
    farewell: "Goodbye, {name}!",
    itemCount: (params: { count: string }) =>
      `${params.count} item${params.count === "1" ? "" : "s"}`,
  },
  es: {
    greeting: "¡Hola, {name}!",
    farewell: "¡Adiós, {name}!",
    itemCount: (params: { count: string }) =>
      `${params.count} artículo${params.count === "1" ? "" : "s"}`,
  },
} as const;

const i18n = new I18n(translations, "en");

console.log(i18n.t("greeting", { name: "Alice" })); // "Hello, Alice!"
console.log(i18n.t("itemCount", { count: "5" })); // "5 items"

i18n.setLocale("es");
console.log(i18n.t("greeting", { name: "Carlos" })); // "¡Hola, Carlos!"
```

---

## Advanced Middleware Patterns

```typescript
// Middleware with typed context and error handling
type Middleware<TContext, TError = Error> = (
  context: TContext,
  next: () => Promise<void>
) => Promise<void>;

class TypedPipeline<TContext, TError = Error> {
  private middlewares: Middleware<TContext, TError>[] = [];
  private errorHandler?: (error: TError, context: TContext) => Promise<void>;

  use(...middlewares: Middleware<TContext, TError>[]): this {
    this.middlewares.push(...middlewares);
    return this;
  }

  onError(handler: (error: TError, context: TContext) => Promise<void>): this {
    this.errorHandler = handler;
    return this;
  }

  async execute(context: TContext): Promise<void> {
    let index = 0;

    const next = async (): Promise<void> => {
      if (index < this.middlewares.length) {
        const middleware = this.middlewares[index++];
        try {
          await middleware(context, next);
        } catch (error) {
          if (this.errorHandler) {
            await this.errorHandler(error as TError, context);
          } else {
            throw error;
          }
        }
      }
    };

    await next();
  }
}

// Conditional middleware
function when<TContext>(
  condition: (ctx: TContext) => boolean,
  middleware: Middleware<TContext>
): Middleware<TContext> {
  return async (ctx, next) => {
    if (condition(ctx)) {
      await middleware(ctx, next);
    } else {
      await next();
    }
  };
}

// Composable middleware
function compose<TContext>(
  ...middlewares: Middleware<TContext>[]
): Middleware<TContext> {
  return async (ctx, next) => {
    let index = 0;

    const composedNext = async (): Promise<void> => {
      if (index < middlewares.length) {
        const middleware = middlewares[index++];
        await middleware(ctx, composedNext);
      } else {
        await next();
      }
    };

    await composedNext();
  };
}

// Usage
interface RequestContext {
  method: string;
  path: string;
  user?: { id: string; role: string };
  response?: { status: number; body: unknown };
}

const pipeline = new TypedPipeline<RequestContext, ApiError>();

pipeline
  .use(async (ctx, next) => {
    console.log(`[LOG] ${ctx.method} ${ctx.path}`);
    await next();
  })
  .use(
    when(
      (ctx) => ctx.path.startsWith("/admin"),
      async (ctx, next) => {
        if (!ctx.user || ctx.user.role !== "admin") {
          ctx.response = { status: 403, body: "Forbidden" };
          return;
        }
        await next();
      }
    )
  )
  .use(async (ctx, next) => {
    ctx.response = { status: 200, body: "OK" };
    await next();
  })
  .onError(async (error, ctx) => {
    console.error(`Error processing ${ctx.path}:`, error);
    ctx.response = { status: 500, body: "Internal Server Error" };
  });
```

---

## Interview Questions

1. **What is the Result/Either pattern?**
   A functional error handling pattern using discriminated unions to represent success or failure without exceptions.

2. **What are phantom types?**
   Type parameters that exist only at compile time, providing type safety without runtime overhead.

3. **What is the type-state pattern?**
   Using TypeScript's type system to enforce state transitions at compile time, preventing invalid state combinations.

4. **How do you implement exhaustive pattern matching?**
   Use `switch` with a `never` type check in the `default` case to ensure all variants are handled.

5. **What is the advantage of algebraic data types?**
   They make invalid states unrepresentable and provide compile-time safety for data modeling.

6. **How do you build a type-safe SQL query builder?**
   Use template literal types, mapped types, and generics to enforce table/column names at compile time.

7. **What is type-safe routing?**
   A routing system where route parameters are typed at compile time, preventing invalid parameter access.

8. **How do you implement type-safe i18n?**
   Use mapped types to ensure translation keys exist and parameter types are correct.

9. **What is the difference between Result and exceptions?**
   Result makes error handling explicit and composable. Exceptions are implicit and can be missed.

10. **When should you use advanced type patterns?**
    When building libraries, when type safety is critical, or when you want to prevent entire classes of bugs at compile time.
