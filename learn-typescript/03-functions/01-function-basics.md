# Function Basics in TypeScript

## Table of Contents

1. [Function Declaration Syntax](#function-declaration-syntax)
2. [Function Expressions](#function-expressions)
3. [Typed Parameters](#typed-parameters)
4. [Typed Return Values](#typed-return-values)
5. [Return Type Inference](#return-type-inference)
6. [Void Return Type](#void-return-type)
7. [Explicit Void](#explicit-void)
8. [Function Type Syntax](#function-type-syntax)
9. [Naming Functions](#naming-functions)
10. [IIFE with Types](#iife-with-types)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Function Declaration Syntax

A function declaration defines a named function. Function declarations are hoisted, meaning they can be called before they appear in the code.

```typescript
// Basic function declaration
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// Calling the function
const message = greet("Alice"); // "Hello, Alice!"
```

### Anatomy of a Function Declaration

```typescript
//         function keyword
//              |
//              v
function add(a: number, b: number): number {
//  ^^^^         ^  ^^^^  ^  ^^^^       ^^^^^^
//  name     param1  param2     return type
  return a + b;
}
```

### Multi-line Function Declarations

```typescript
function createFullName(
  firstName: string,
  lastName: string,
  middleName?: string
): string {
  if (middleName) {
    return `${firstName} ${middleName} ${lastName}`;
  }
  return `${firstName} ${lastName}`;
}

console.log(createFullName("John", "Doe"));          // "John Doe"
console.log(createFullName("John", "Michael", "Doe")); // "John Michael Doe"
```

### Function Declarations vs Function Expressions (Hoisting)

```typescript
// This works because function declarations are hoisted
console.log(add(2, 3)); // 5

function add(a: number, b: number): number {
  return a + b;
}

// This does NOT work with function expressions
// console.log(multiply(2, 3)); // Error: multiply is not defined

const multiply = (a: number, b: number): number => {
  return a * b;
};
```

---

## Function Expressions

A function expression defines a function as part of an expression, typically assigned to a variable.

```typescript
// Function expression assigned to a variable
const subtract = function (a: number, b: number): number {
  return a - b;
};

// With explicit type annotation on the variable
const divide: (a: number, b: number) => number = function (a, b) {
  return a / b;
};

console.log(subtract(10, 4)); // 6
console.log(divide(10, 2));   // 5
```

### Anonymous vs Named Function Expressions

```typescript
// Anonymous function expression
const square = function (x: number): number {
  return x * x;
};

// Named function expression (useful for debugging/stack traces)
const cube = function cube(x: number): number {
  return x * x * x;
};

// The name "cube" is available inside the function for recursion
const factorial = function fact(n: number): number {
  if (n <= 1) return 1;
  return n * fact(n - 1); // Can reference itself via the name
};
```

---

## Typed Parameters

Every parameter in a TypeScript function should have a type annotation.

```typescript
// Individual parameter types
function createUser(
  name: string,
  age: number,
  email: string,
  isActive: boolean
): void {
  console.log(`Creating user: ${name}, age ${age}`);
}

// Parameters with complex types
function processItems(
  items: string[],
  callback: (item: string, index: number) => void
): void {
  items.forEach((item, index) => {
    callback(item, index);
  });
}

// Object parameter types
interface Config {
  host: string;
  port: number;
  secure: boolean;
}

function connect(config: Config): void {
  const protocol = config.secure ? "https" : "http";
  console.log(`Connecting to ${protocol}://${config.host}:${config.port}`);
}

connect({ host: "localhost", port: 3000, secure: false });
```

### Destructured Parameters with Types

```typescript
// Destructuring with inline types
function printUser({ name, age, email }: { name: string; age: number; email: string }): void {
  console.log(`${name} (${age}) - ${email}`);
}

// Destructuring with an interface
interface User {
  id: number;
  name: string;
  email: string;
  role: "admin" | "user" | "guest";
}

function greetUser({ name, role }: User): string {
  switch (role) {
    case "admin":
      return `Welcome back, Admin ${name}!`;
    case "user":
      return `Hello, ${name}!`;
    case "guest":
      return `Welcome, guest!`;
  }
}
```

---

## Typed Return Values

You can explicitly specify the return type of a function.

```typescript
// Explicit return type
function calculateTotal(price: number, quantity: number, taxRate: number): number {
  const subtotal = price * quantity;
  const tax = subtotal * taxRate;
  return subtotal + tax;
}

// Returning complex types
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

function fetchData<T>(url: string): ApiResponse<T> {
  // Implementation would make an HTTP request
  return {
    data: {} as T,
    status: 200,
    message: "Success",
  };
}

// Returning union types
function parseInput(input: string): string | number | boolean {
  if (input === "true") return true;
  if (input === "false") return false;
  const num = Number(input);
  if (!isNaN(num)) return num;
  return input;
}
```

### Never Return Type

```typescript
// Functions that never return
function throwError(message: string): never {
  throw new Error(message);
}

function infiniteLoop(): never {
  while (true) {
    // This never terminates
  }
}

// Usage in type narrowing
function processValue(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  }
  if (typeof value === "number") {
    return value.toFixed(2);
  }
  // TypeScript knows this point is unreachable
  const exhaustiveCheck: never = value;
  return exhaustiveCheck;
}
```

---

## Return Type Inference

TypeScript can automatically infer the return type of a function.

```typescript
// TypeScript infers return type as number
function add(a: number, b: number) {
  return a + b; // inferred as number
}

// TypeScript infers return type as string
function formatName(first: string, last: string) {
  return `${first} ${last}`; // inferred as string
}

// TypeScript infers return type as boolean
function isEven(num: number) {
  return num % 2 === 0; // inferred as boolean
}

// Complex inference
function createObject(key: string, value: number) {
  return { [key]: value }; // inferred as { [x: string]: number }
}
```

### When to Use Explicit Return Types

```typescript
// GOOD: Explicit return type for public API functions
export function getUser(id: number): User | null {
  // Implementation details can change without affecting consumers
  return db.findUser(id);
}

// GOOD: Let TypeScript infer for small internal functions
const double = (x: number) => x * 2;

// GOOD: Explicit return type catches bugs
function getData(): { items: string[]; count: number } {
  // If you accidentally return wrong structure, TypeScript catches it
  return {
    items: ["a", "b"],
    count: 2,
  };
}

// BAD: Missing return type can hide bugs
function processData(data: unknown) {
  // No return type annotation - harder to catch errors
  return data; // returns `unknown` which might cause issues downstream
}
```

---

## Void Return Type

The `void` return type indicates that a function does not return a value.

```typescript
// Implicit void (no return statement)
function logMessage(message: string): void {
  console.log(message);
}

// Explicit void with return statement (not returning a value)
function setUserAge(user: User, age: number): void {
  user.age = age;
  return; // Explicit return with no value (optional but clarifying intent)
}

// Void in callback types
functionforEach<T>(items: T[], callback: (item: T) => void): void {
  for (const item of items) {
    callback(item);
  }
}
```

---

## Explicit Void

When and why to use explicit `void` annotations.

```typescript
// Explicit void in function type annotations
const logger: (message: string) => void = (message) => {
  console.log(message);
};

// void in generic context
function identity<T>(arg: T): T {
  return arg;
}

// void callback - promises the function won't use the return value
function setTimeout(callback: () => void, ms: number): void {
  // ...
}

// Important: void-returning callbacks CAN return values
// but the return value is ignored
const numbers = [1, 2, 3];
numbers.forEach((num) => {
  return num * 2; // Return value is ignored, but no error
});

// Strict function types - avoid returning values from void functions
type VoidCallback = () => void;

const cb: VoidCallback = () => {
  return 42; // This is actually allowed with void
};

// To prevent this, use never instead of void
type StrictVoidCallback = () => never;
// const strictCb: StrictVoidCallback = () => 42; // Error!
```

---

## Function Type Syntax

TypeScript provides multiple ways to define function types.

```typescript
// Type alias for a function
type MathOperation = (a: number, b: number) => number;

const add: MathOperation = (a, b) => a + b;
const subtract: MathOperation = (a, b) => a - b;
const multiply: MathOperation = (a, b) => a * b;

// Interface with call signature
interface Comparator<T> {
  (a: T, b: T): number;
}

const stringCompare: Comparator<string> = (a, b) => a.localeCompare(b);
const numberCompare: Comparator<number> = (a, b) => a - b;

// Function type with optional parameters
type Formatter = (value: string, uppercase?: boolean) => string;

const format: Formatter = (value, uppercase = false) => {
  return uppercase ? value.toUpperCase() : value.toLowerCase();
};

// Complex function types
type AsyncOperation<TInput, TOutput> = (
  input: TInput,
  signal?: AbortSignal
) => Promise<TOutput>;

type EventHandler<TEvent> = (event: TEvent) => void;

type Middleware<TContext> = (
  context: TContext,
  next: () => Promise<void>
) => Promise<void>;
```

### Using Function Types as Parameters

```typescript
// Passing functions as parameters
function performOperation(
  a: number,
  b: number,
  operation: (x: number, y: number) => number
): number {
  return operation(a, b);
}

// Using the function type
const result = performOperation(5, 3, (a, b) => a + b); // 8

// Array methods with function types
const numbers = [1, 2, 3, 4, 5];

const doubled = numbers.map((n: number): number => n * 2);
const evens = numbers.filter((n: number): boolean => n % 2 === 0);
const sum = numbers.reduce((acc: number, n: number): number => acc + n, 0);
```

---

## Naming Functions

Best practices for naming functions in TypeScript.

```typescript
// Use descriptive names that explain what the function does
function calculateMonthlyRevenue(transactions: Transaction[]): number {
  return transactions.reduce((sum, t) => sum + t.amount, 0);
}

// Prefix boolean-returning functions with "is", "has", "can", "should"
function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function hasPermission(user: User, resource: string): boolean {
  return user.permissions.includes(resource);
}

// Prefix functions that create new values with "create", "build", "make"
function createUserProfile(data: UserData): UserProfile {
  return { ...data, createdAt: new Date() };
}

// Prefix functions that modify with "set", "update", "delete"
function setUserStatus(userId: string, status: UserStatus): void {
  // ...
}

// Prefix getter functions with "get"
function getUserById(id: string): User | undefined {
  // ...
}

// Prefix predicate functions with "is" or "has"
function isString(value: unknown): value is string {
  return typeof value === "string";
}

// Prefix conversion functions with "to"
function toString(value: number): string {
  return String(value);
}

// Private/internal functions can use underscore prefix
function _validateInput(input: unknown): boolean {
  // ...
}
```

---

## IIFE with Types

Immediately Invoked Function Expressions (IIFEs) with TypeScript type annotations.

```typescript
// Basic IIFE with types
const result = (function (x: number, y: number): number {
  return x + y;
})(10, 20); // result = 30

// Arrow function IIFE with types
const config = (() => {
  const apiUrl = "https://api.example.com";
  const timeout = 5000;

  return {
    apiUrl,
    timeout,
    getHeaders: (): Record<string, string> => ({
      "Content-Type": "application/json",
    }),
  };
})();

console.log(config.apiUrl);    // "https://api.example.com"
console.log(config.timeout);   // 5000

// IIFE for encapsulation
const counter = (function () {
  let count = 0;

  return {
    increment: (): number => ++count,
    decrement: (): number => --count,
    getCount: (): number => count,
    reset: (): void => {
      count = 0;
    },
  };
})();

console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.getCount());  // 2
counter.reset();
console.log(counter.getCount());  // 0

// Async IIFE
(async function (): Promise<void> {
  const response = await fetch("https://api.example.com/data");
  const data = await response.json();
  console.log(data);
})();

// IIFE with type assertions
const sizes = (function () {
  const sizes = ["xs", "sm", "md", "lg", "xl"] as const;
  return sizes;
})();

type Size = (typeof sizes)[number]; // "xs" | "sm" | "md" | "lg" | "xl"
```

---

## Best Practices

```typescript
// 1. Always add return type annotations to exported functions
export function processOrder(order: Order): OrderResult {
  // ...
}

// 2. Use type inference for simple, obvious functions
const double = (x: number) => x * 2;

// 3. Keep functions small and focused
// BAD: Function does too many things
function processEverything(data: unknown): unknown {
  // validates, transforms, saves, sends email, generates report...
}

// GOOD: Single responsibility
function validateData(data: unknown): ValidData { /* ... */ }
function transformData(data: ValidData): TransformedData { /* ... */ }
function saveData(data: TransformedData): SavedRecord { /* ... */ }

// 4. Prefer named functions over anonymous for better stack traces
// BAD
items.map(function (item) { return item.name; });
// GOOD
items.map(function getItemName(item) { return item.name; });

// 5. Use void for functions with side effects
function saveToDatabase(record: Record): void {
  db.insert(record);
}

// 6. Avoid default exports for better refactoring
// BAD
export default function helper() { /* ... */ }
// GOOD
export function helper() { /* ... */ }
```

---

## Interview Questions

### Q1: What is the difference between a function declaration and a function expression?

**Answer:** Function declarations are hoisted (can be called before they appear in code), while function expressions are not. Function declarations create named functions in the scope, while function expressions assign functions to variables.

```typescript
// Declaration - hoisted
greet("Alice"); // Works!
function greet(name: string): string { return `Hello, ${name}`; }

// Expression - NOT hoisted
farewell("Bob"); // Error!
const farewell = function(name: string): string { return `Goodbye, ${name}`; };
```

### Q2: When should you use explicit return types?

**Answer:** Use explicit return types for:
- Exported/public API functions (contract clarity)
- Complex return types (helps documentation)
- Recursive functions (TypeScript may struggle to infer)
- When you want the compiler to catch unintended return type changes

### Q3: What is the `void` return type and when to use it?

**Answer:** `void` means the function doesn't return a meaningful value. Use it for functions that perform side effects (logging, modifying state, etc.). The function may have a `return` statement with no value, or no `return` statement at all.

### Q4: Can a function return both a value and void?

**Answer:** A `void`-typed function can technically return a value, but the return value is ignored when the function is called. However, this is considered bad practice and should be avoided.
