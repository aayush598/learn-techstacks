# Optional and Default Parameters in TypeScript

## Table of Contents

1. [Optional Parameters](#optional-parameters)
2. [Default Parameters](#default-parameters)
3. [Required vs Optional Ordering](#required-vs-optional-ordering)
4. [Default Parameter Types](#default-parameter-types)
5. [Optional Parameters in Callbacks](#optional-parameters-in-callbacks)
6. [Undefined as Optional](#undefined-as-optional)
7. [Optional Chaining in Function Results](#optional-chaining-in-function-results)
8. [Advanced Patterns](#advanced-patterns)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Optional Parameters

Optional parameters are denoted with `?` and can be omitted when calling the function.

```typescript
// Basic optional parameter
function greet(name: string, greeting?: string): string {
  if (greeting) {
    return `${greeting}, ${name}!`;
  }
  return `Hello, ${name}!`;
}

console.log(greet("Alice"));           // "Hello, Alice!"
console.log(greet("Alice", "Hi"));     // "Hi, Alice!"
console.log(greet("Alice", undefined)); // "Hello, Alice!"
```

### Optional Parameters in Function Signatures

```typescript
// Multiple optional parameters
function createURL(
  base: string,
  path?: string,
  query?: string,
  fragment?: string
): string {
  let url = base;
  if (path) url += path;
  if (query) url += `?${query}`;
  if (fragment) url += `#${fragment}`;
  return url;
}

console.log(createURL("https://api.com"));                    // "https://api.com"
console.log(createURL("https://api.com", "/users"));          // "https://api.com/users"
console.log(createURL("https://api.com", "/users", "page=1"));// "https://api.com/users?page=1"
console.log(createURL("https://api.com", "/users", "page=1", "top"));
// "https://api.com/users?page=1#top"
```

### Optional Object Properties in Parameters

```typescript
interface Options {
  timeout?: number;
  retries?: number;
  cache?: boolean;
}

function fetchData(url: string, options?: Options): void {
  const timeout = options?.timeout ?? 30000;
  const retries = options?.retries ?? 3;
  const cache = options?.cache ?? true;

  console.log(`Fetching ${url} with timeout=${timeout}, retries=${retries}, cache=${cache}`);
}

fetchData("/api/data");                         // Uses all defaults
fetchData("/api/data", { timeout: 5000 });     // Custom timeout
fetchData("/api/data", { cache: false });       // No cache
```

### Optional Parameters with Type Guards

```typescript
function processValue(value?: string | number): string {
  // TypeScript narrows the type after checking
  if (value === undefined) {
    return "No value provided";
  }

  if (typeof value === "string") {
    return value.toUpperCase();
  }

  return value.toFixed(2);
}

console.log(processValue());          // "No value provided"
console.log(processValue("hello"));   // "HELLO"
console.log(processValue(3.14159));   // "3.14"
```

---

## Default Parameters

Default parameters provide a fallback value when no argument is passed or `undefined` is explicitly passed.

```typescript
// Basic default parameter
function createUser(
  name: string,
  role: string = "user",
  active: boolean = true
): User {
  return {
    name,
    role: role as "admin" | "user" | "guest",
    active,
    createdAt: new Date(),
  };
}

console.log(createUser("Alice"));
// { name: "Alice", role: "user", active: true, createdAt: ... }

console.log(createUser("Bob", "admin"));
// { name: "Bob", role: "admin", active: true, createdAt: ... }

console.log(createUser("Charlie", "guest", false));
// { name: "Charlie", role: "guest", active: false, createdAt: ... }
```

### Default Parameters with Expressions

```typescript
// Default value can be any expression
function createGreeting(
  name: string,
  timeOfDay: string = new Date().getHours() < 12 ? "morning" : "afternoon"
): string {
  return `Good ${timeOfDay}, ${name}!`;
}

// Default value computed at call time
function generateId(prefix: string = `id-${Date.now()}`): string {
  return prefix;
}

// Default value using another parameter
function repeatString(
  str: string,
  count: number = 1
): string {
  return str.repeat(count);
}

console.log(repeatString("hello"));     // "hello"
console.log(repeatString("hello", 3));  // "hellohellohello"
```

### Default Parameters with Destructuring

```typescript
interface Config {
  host: string;
  port: number;
  secure: boolean;
  maxRetries: number;
  timeout: number;
}

function connectToServer({
  host = "localhost",
  port = 3000,
  secure = false,
  maxRetries = 3,
  timeout = 30000,
}: Partial<Config> = {}): void {
  console.log(
    `Connecting to ${secure ? "https" : "http"}://${host}:${port}` +
    ` (retries: ${maxRetries}, timeout: ${timeout}ms)`
  );
}

connectToServer();                                      // All defaults
connectToServer({ host: "production.com", port: 443 }); // Partial override
connectToServer({});                                     // All defaults (empty object)
```

---

## Required vs Optional Ordering

TypeScript requires optional parameters to come after required parameters.

```typescript
// VALID: Required parameters first, then optional
function createUser(
  name: string,        // required
  email: string,       // required
  age?: number,        // optional
  bio?: string         // optional
): User {
  return { name, email, age, bio };
}

// INVALID: Optional before required
// function broken(
//   name?: string,    // Error: A required parameter cannot follow an optional parameter
//   email: string
// ): void {}

// SOLUTION: Use overloads or union types for complex cases
function createOrFindUser(
  nameOrId: string | number,
  email?: string
): User {
  if (typeof nameOrId === "number") {
    // Find by ID
    return db.findUser(nameOrId)!;
  }
  // Create new user
  return { name: nameOrId, email: email ?? "" };
}

// SOLUTION 2: Use an options object
interface UserConfig {
  name: string;
  email: string;
  age?: number;
  bio?: string;
}

function buildUser(config: UserConfig): User {
  return config;
}

buildUser({ name: "Alice", email: "alice@example.com" });
```

### Using Rest Parameters to Work Around Ordering

```typescript
// Flexible parameter ordering with rest
function log(level: string, ...messages: unknown[]): void {
  console.log(`[${level.toUpperCase()}]`, ...messages);
}

log("info", "Server started", "on port 3000");
log("error", "Connection failed", { retries: 3 });
```

---

## Default Parameter Types

TypeScript infers the type of default parameters from the default value.

```typescript
// Type is inferred from default
function configure(config = { debug: false, verbose: true }) {
  // config is { debug: boolean, verbose: boolean }
  console.log(config.debug, config.verbose);
}

// Explicit type with default value
function setInterval(
  callback: () => void,
  interval: number = 1000
): void {
  // ...
}

// Union type with default
function setStatus(
  status: "active" | "inactive" | "pending" = "active"
): void {
  console.log(`Status set to: ${status}`);
}

// Complex default types
interface DatabaseConfig {
  host: string;
  port: number;
  ssl: boolean;
}

function connectDatabase(
  config: DatabaseConfig = {
    host: "localhost",
    port: 5432,
    ssl: false,
  }
): void {
  console.log(`Connecting to ${config.host}:${config.port}`);
}
```

### Narrowing with Default Values

```typescript
// Default values help TypeScript narrow types
function processInput(
  input: string | number = "default"
): string {
  // input is string | number (not undefined)
  if (typeof input === "string") {
    return input.toUpperCase();
  }
  return input.toFixed(2);
}

// Without default, input could be undefined
function processInputBad(
  input?: string | number
): string {
  // input is string | number | undefined
  if (input === undefined) {
    return "DEFAULT";
  }
  if (typeof input === "string") {
    return input.toUpperCase();
  }
  return input.toFixed(2);
}
```

---

## Optional Parameters in Callbacks

Optional parameters are commonly used in callback function types.

```typescript
// Array methods with optional callback parameters
const numbers = [1, 2, 3, 4, 5];

// forEach callback has optional second and third parameters
numbers.forEach((value, index?, array?) => {
  console.log(`${index}: ${value}`);
});

// map callback has optional second parameter
const doubled = numbers.map((value, index?) => {
  return value * 2;
});

// filter callback has optional second and third parameters
const evens = numbers.filter((value, index?, array?) => {
  return value % 2 === 0;
});

// Event handler with optional event parameter
type ClickHandler = (event?: MouseEvent) => void;

const handleClick: ClickHandler = (event) => {
  if (event) {
    console.log(`Clicked at (${event.clientX}, ${event.clientY})`);
  } else {
    console.log("Clicked (no event data)");
  }
};

// Promise callbacks
type ResolveFunction<T> = (value?: T | PromiseLike<T>) => void;
type RejectFunction = (reason?: unknown) => void;

const promise = new Promise<string>((resolve?, reject?) => {
  resolve?.("success");
});
```

### Optional Parameters in Higher-Order Functions

```typescript
// Factory function with optional configuration
function createLogger(
  prefix: string = "LOG",
  options?: {
    timestamp?: boolean;
    level?: "info" | "warn" | "error";
  }
): (message: string) => void {
  const showTimestamp = options?.timestamp ?? true;
  const level = options?.level ?? "info";

  return (message: string) => {
    const timestamp = showTimestamp ? `[${new Date().toISOString()}]` : "";
    const prefixStr = `[${prefix}]`;
    const levelStr = `[${level.toUpperCase()}]`;
    console.log(`${timestamp}${prefixStr}${levelStr} ${message}`);
  };
}

const logger = createLogger("APP");
logger("Application started"); // [timestamp][APP][INFO] Application started

const errorLogger = createLogger("ERROR", { timestamp: false, level: "error" });
errorLogger("Something went wrong"); // [ERROR][ERROR] Something went wrong
```

---

## Undefined as Optional

Understanding how `undefined` interacts with optional parameters.

```typescript
// Passing undefined explicitly triggers default values
function greet(name: string = "World"): string {
  return `Hello, ${name}!`;
}

greet();          // "Hello, World!" (default used)
greet(undefined); // "Hello, World!" (default used)
greet("Alice");   // "Hello, Alice!"

// Undefined vs null vs empty string
function process(value?: string): string {
  if (value === undefined) return "was undefined";
  if (value === null) return "was null";
  if (value === "") return "was empty string";
  return `was: ${value}`;
}

process();            // "was undefined"
process(undefined);   // "was undefined"
process(null as any); // "was null" (if you force it)
process("");          // "was empty string"
```

### Undefined in Conditional Types

```typescript
// Using undefined to check if parameter was provided
function fetchData(
  url: string,
  options?: { cache?: boolean; timeout?: number }
): void {
  const cache = options?.cache;
  const timeout = options?.timeout;

  // Check if specific options were provided
  if (cache !== undefined) {
    console.log(`Cache: ${cache}`);
  } else {
    console.log("Using default cache settings");
  }

  if (timeout !== undefined) {
    console.log(`Timeout: ${timeout}ms`);
  } else {
    console.log("Using default timeout");
  }
}

// Strict checking with in operator
function configure(settings?: Record<string, unknown>): void {
  if (settings && "debug" in settings) {
    console.log("Debug mode explicitly set");
  }
}
```

---

## Optional Chaining in Function Results

Using optional chaining with function return values.

```typescript
interface User {
  name: string;
  address?: {
    street?: string;
    city?: string;
    zip?: string;
  };
  getFullName?: () => string;
}

// Optional chaining on function calls
function getUserFullName(user: User): string {
  return user.getFullName?.() ?? user.name;
}

// Optional chaining on nested properties
function getCity(user: User): string {
  return user.address?.city ?? "Unknown";
}

// Optional chaining with method calls
function getFormattedAddress(user: User): string {
  const street = user.address?.street;
  const city = user.address?.city;
  const zip = user.address?.zip;

  if (!street && !city) return "No address available";

  return [street, city, zip].filter(Boolean).join(", ");
}

// Chaining optional function calls
function createPipeline(...steps: ((data: any) => any)[]): (data: any) => any {
  return (data: any) => {
    return steps.reduce((result, step) => step(result), data);
  };
}

const process = createPipeline(
  (data) => data.trim?.() ?? data,
  (data) => (typeof data === "string" ? data.toUpperCase() : data),
  (data) => (typeof data === "string" ? data.split(" ").join("_") : data)
);
```

---

## Advanced Patterns

```typescript
// Discriminated unions with optional parameters
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function divide(
  a: number,
  b: number,
  onError?: (error: Error) => void
): Result<number> {
  if (b === 0) {
    const error = new Error("Division by zero");
    onError?.(error);
    return { success: false, error };
  }
  return { success: true, data: a / b };
}

// Optional parameters with overloads
function createElement(tag: "div"): HTMLDivElement;
function createElement(tag: "span"): HTMLSpanElement;
function createElement(tag: string, className?: string): HTMLElement;
function createElement(tag: string, className?: string): HTMLElement {
  const el = document.createElement(tag);
  if (className) el.className = className;
  return el;
}

// Builder pattern with optional parameters
class QueryBuilder {
  private _table: string = "";
  private _conditions: string[] = [];
  private _orderBy?: string;
  private _limit?: number;

  from(table: string): this {
    this._table = table;
    return this;
  }

  where(condition: string): this {
    this._conditions.push(condition);
    return this;
  }

  orderBy(field: string, direction: "ASC" | "DESC" = "ASC"): this {
    this._orderBy = `${field} ${direction}`;
    return this;
  }

  limit(count: number): this {
    this._limit = count;
    return this;
  }

  build(): string {
    let query = `SELECT * FROM ${this._table}`;
    if (this._conditions.length) {
      query += ` WHERE ${this._conditions.join(" AND ")}`;
    }
    if (this._orderBy) query += ` ORDER BY ${this._orderBy}`;
    if (this._limit) query += ` LIMIT ${this._limit}`;
    return query;
  }
}

const query = new QueryBuilder()
  .from("users")
  .where("age > 18")
  .where("active = true")
  .orderBy("name")
  .limit(10)
  .build();

console.log(query);
// "SELECT * FROM users WHERE age > 18 AND active = true ORDER BY name ASC LIMIT 10"
```

---

## Best Practices

```typescript
// 1. Use optional parameters sparingly - prefer options objects for 3+ optional params
// BAD
function create(
  name: string,
  type?: string,
  color?: string,
  size?: string,
  weight?: number
): Item { /* ... */ }

// GOOD
function create(
  name: string,
  options?: {
    type?: string;
    color?: string;
    size?: string;
    weight?: number;
  }
): Item { /* ... */ }

// 2. Always handle the undefined case
function processName(name?: string): string {
  // BAD - might return undefined
  return name?.toUpperCase();

  // GOOD - always returns a string
  return name?.toUpperCase() ?? "UNKNOWN";
}

// 3. Document what defaults are used
interface CreateOptions {
  /** @default "user" */
  role?: string;
  /** @default true */
  active?: boolean;
  /** @default 30000 */
  timeout?: number;
}

// 4. Use default parameters over checking undefined
// BAD
function log(message: string, level?: string) {
  const actualLevel = level || "info";
  // ...
}

// GOOD
function log(message: string, level: string = "info"): void {
  // ...
}

// 5. Consider using required parameters for critical values
// BAD - might cause runtime errors
function send(to?: string, subject?: string, body?: string): void { /* ... */ }

// GOOD - required params ensure correctness
function send(to: string, subject: string, body: string): void { /* ... */ }
```

---

## Interview Questions

### Q1: What is the difference between optional parameters and default parameters?

**Answer:** Optional parameters (`?`) indicate a parameter can be omitted, making it `undefined` if not provided. Default parameters (`= value`) provide a fallback value when the parameter is omitted or `undefined` is passed.

```typescript
// Optional - value is undefined if not provided
function greet(name?: string): string {
  return `Hello, ${name ?? "World"}`; // Must handle undefined
}

// Default - has a fallback value
function greet(name: string = "World"): string {
  return `Hello, ${name}`; // Never undefined
}
```

### Q2: Why must optional parameters come after required parameters?

**Answer:** TypeScript enforces this because JavaScript has no way to distinguish between "missing argument" and "undefined argument" in positional parameters. If optional parameters came first, the compiler couldn't determine which arguments were intended for which parameters.

### Q3: How do you handle 4+ optional parameters in a function?

**Answer:** Use an options object pattern:

```typescript
// BAD: Hard to remember parameter order
function connect(host, port, secure, timeout, retries) {}

// GOOD: Self-documenting and order-independent
interface ConnectOptions {
  host: string;
  port?: number;
  secure?: boolean;
  timeout?: number;
  retries?: number;
}

function connect(options: ConnectOptions): Connection { /* ... */ }
```

### Q4: What happens when you pass `undefined` to a parameter with a default value?

**Answer:** The default value is used. This is a key feature - default parameters apply when the value is `undefined`, not just when it's omitted.
