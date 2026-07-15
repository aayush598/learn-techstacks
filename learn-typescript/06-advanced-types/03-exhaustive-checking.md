# Exhaustive Checking in TypeScript

Exhaustive checking is a TypeScript pattern that uses the `never` type to ensure **every possible case** in a union type is handled. If you add a new variant to a union and forget to handle it, the compiler catches the mistake immediately.

---

## Table of Contents

1. [What is Exhaustive Checking?](#what-is-exhaustive-checking)
2. [The `never` Type](#the-never-type)
3. [exhaustiveCheck Helper](#exhaustivecheck-helper)
4. [Switch Exhaustive Checks](#switch-exhaustive-checks)
5. [if-else Exhaustive Checks](#if-else-exhaustive-checks)
6. [Exhaustive Discrimination](#exhaustive-discrimination)
7. [Compiler-Enforced Completeness](#compiler-enforced-completeness)
8. [Benefits for Refactoring](#benefits-for-refactoring)
9. [When Exhaustive Checking is Critical](#when-exhaustive-checking-is-critical)
10. [Common Pitfalls](#common-pitfalls)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## What is Exhaustive Checking?

Exhaustive checking ensures that you've handled **every possible variant** in a union type. If you miss a case, TypeScript raises a compile-time error.

```typescript
type Direction = "north" | "south" | "east" | "west";

function move(direction: Direction) {
  // If you forget one direction, you get a compile error
  switch (direction) {
    case "north":
      console.log("Moving north");
      break;
    case "south":
      console.log("Moving south");
      break;
    case "east":
      console.log("Moving east");
      break;
    // ❌ Missing "west" case!
  }
}
```

Without exhaustive checking, this compiles fine but is a runtime bug. With the `never` pattern, the compiler catches the missing case.

---

## The `never` Type

`never` is TypeScript's **bottom type** — it represents values that never occur. No value can be assigned to `never` (except `never` itself).

```typescript
let x: never;
// The only way to assign to `never` is by throwing or infinite looping
function throwError(): never {
  throw new Error("oops");
}
```

### How `never` enables exhaustive checking

When a union type has been fully narrowed, the remaining type is `never`:

```typescript
type A = "foo" | "bar";

function example(x: A) {
  if (x === "foo") {
    // x: "foo"
  } else {
    // x: "bar" — the only remaining option
  }
  // After the if-else, x is back to A
}

// But if you capture the narrowed type:
function example2(x: A) {
  let result: never;

  if (x === "foo") {
    // OK
  } else {
    // x: "bar"
    result = x; // ❌ Error: Type '"bar"' is not assignable to type 'never'
  }
}
```

Wait — that should work because `"bar"` is not `never`. The key insight is:

- After handling ALL cases, the remaining type is `never`
- If you HAVEN'T handled all cases, the remaining type is NOT `never`
- Assigning a non-`never` type to `never` causes a compile error

---

## exhaustiveCheck Helper

The standard pattern is a helper function that accepts `never`:

```typescript
function exhaustiveCheck(x: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(x)}`);
}
```

### Usage with switch

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      exhaustiveCheck(shape); // Compile error if a case is missing!
      return 0; // unreachable
  }
}
```

### The helper function pattern

```typescript
// Option 1: Throw an error
function assertNever(value: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(value)}`);
}

// Option 2: Return never and log
function exhaustiveCheck(value: never): never {
  console.error("Unhandled exhaustive case:", value);
  throw new Error("This should never happen");
}

// Option 3: Generic version with a message
function ensureNever(value: never, message?: string): never {
  throw new Error(message ?? `Unexpected value: ${JSON.stringify(value)}`);
}
```

---

## Switch Exhaustive Checks

The most common pattern for exhaustive checking is with `switch` statements on discriminated unions.

### Basic pattern

```typescript
type Status = "pending" | "active" | "completed" | "archived";

function getStatusColor(status: Status): string {
  switch (status) {
    case "pending":
      return "yellow";
    case "active":
      return "green";
    case "completed":
      return "blue";
    case "archived":
      return "gray";
    default:
      exhaustiveCheck(status);
      return "unknown"; // unreachable
  }
}
```

### Complex discriminated union

```typescript
type Notification =
  | { type: "email"; to: string; subject: string; body: string }
  | { type: "sms"; to: string; message: string }
  | { type: "push"; userId: string; title: string; data: Record<string, unknown> }
  | { type: "webhook"; url: string; payload: unknown };

function sendNotification(notification: Notification): void {
  switch (notification.type) {
    case "email":
      console.log(`Email to ${notification.to}: ${notification.subject}`);
      break;
    case "sms":
      console.log(`SMS to ${notification.to}: ${notification.message}`);
      break;
    case "push":
      console.log(`Push to ${notification.userId}: ${notification.title}`);
      break;
    case "webhook":
      console.log(`Webhook to ${notification.url}`);
      break;
    default:
      exhaustiveCheck(notification);
  }
}
```

### Adding a new case breaks the handler ✅

```typescript
// Add a new notification type:
type Notification =
  | { type: "email"; to: string; subject: string; body: string }
  | { type: "sms"; to: string; message: string }
  | { type: "push"; userId: string; title: string; data: Record<string, unknown> }
  | { type: "webhook"; url: string; payload: unknown }
  | { type: "in_app"; userId: string; message: string }; // NEW!

// ❌ Compile error in sendNotification:
// Type '{ type: "in_app"; userId: string; message: string; }' is not assignable to type 'never'
```

---

## if-else Exhaustive Checks

You can also use exhaustive checking with if-else chains.

```typescript
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string; retryable: boolean };

function handleResult(result: Result<string>) {
  if (result.success) {
    console.log(result.data);
  } else {
    console.error(result.error);
    if (result.retryable) {
      console.log("Retrying...");
    }
  }
  // No else needed — all cases are handled
}
```

### With explicit never assignment

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  let result: never;

  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
  } else if (shape.kind === "square") {
    return shape.side ** 2;
  } else {
    result = shape; // Compile error if not all cases handled
    return result;
  }
}
```

### if-else with type guards

```typescript
type Value = string | number | boolean;

function process(value: Value): string {
  if (typeof value === "string") {
    return value.toUpperCase();
  } else if (typeof value === "number") {
    return value.toFixed(2);
  } else if (typeof value === "boolean") {
    return value ? "true" : "false";
  } else {
    exhaustiveCheck(value);
    return ""; // unreachable
  }
}

function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled type: ${typeof x}`);
}
```

---

## Exhaustive Discrimination

Exhaustive discrimination means checking **all properties** of a discriminated union, not just the discriminant.

```typescript
type Config =
  | { mode: "development"; port: number; debug: boolean }
  | { mode: "production"; port: number; ssl: boolean; domain: string }
  | { mode: "test"; port: number; coverage: boolean };

function validateConfig(config: Config): boolean {
  switch (config.mode) {
    case "development":
      // config.port, config.debug are available
      return config.port > 0 && typeof config.debug === "boolean";
    case "production":
      // config.port, config.ssl, config.domain are available
      return config.port > 0 && config.domain.length > 0;
    case "test":
      // config.port, config.coverage are available
      return config.port > 0;
    default:
      exhaustiveCheck(config);
      return false;
  }
}

function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled config mode: ${x}`);
}
```

---

## Compiler-Enforced Completeness

Exhaustive checking provides **compile-time guarantees** that all cases are handled.

### Benefits

1. **No missed cases** — the compiler catches missing branches
2. **No runtime errors** — all code paths are type-safe
3. **Documentation** — the switch statement documents all possible cases
4. **Refactoring safety** — adding new union members forces updates everywhere

### Comparison with runtime checks

```typescript
// ❌ Runtime check — misses cases silently
function process(value: string | number) {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  }
  // Missing number case — no warning!
}

// ✅ Exhaustive check — compile error if missing
function process(value: string | number) {
  if (typeof value === "string") {
    console.log(value.toUpperCase());
  } else if (typeof value === "number") {
    console.log(value.toFixed(2));
  } else {
    exhaustiveCheck(value); // Compile error if a type is missing
  }
}
```

---

## Benefits for Refactoring

Exhaustive checking is especially valuable during refactoring.

### Scenario: Adding a new status

```typescript
// Before refactor
type OrderStatus = "pending" | "shipped" | "delivered";

function getStatusMessage(status: OrderStatus): string {
  switch (status) {
    case "pending": return "Your order is pending";
    case "shipped": return "Your order has shipped";
    case "delivered": return "Your order has been delivered";
    default: return exhaustiveCheck(status);
  }
}

// After refactor — add "cancelled"
type OrderStatus = "pending" | "shipped" | "delivered" | "cancelled";

// ❌ Compile error in getStatusMessage!
// Type '"cancelled"' is not assignable to type 'never'
// Forces you to handle the new case
```

### Scenario: Removing a status

```typescript
// Remove "shipped" from the union
type OrderStatus = "pending" | "delivered";

// The switch still compiles — all remaining cases are handled
// But the "shipped" case is now dead code, which the compiler may warn about
```

---

## When Exhaustive Checking is Critical

### 1. Event/Action Handlers

```typescript
type AppEvent =
  | { type: "USER_LOGIN"; userId: string }
  | { type: "USER_LOGOUT"; userId: string }
  | { type: "PAGE_VIEW"; page: string; referrer?: string }
  | { type: "PURCHASE"; itemId: string; amount: number };

function trackEvent(event: AppEvent) {
  // Missing a case means lost analytics data
  switch (event.type) {
    case "USER_LOGIN":
      analytics.track("login", { userId: event.userId });
      break;
    case "USER_LOGOUT":
      analytics.track("logout", { userId: event.userId });
      break;
    case "PAGE_VIEW":
      analytics.track("page_view", { page: event.page });
      break;
    case "PURCHASE":
      analytics.track("purchase", { itemId: event.itemId, amount: event.amount });
      break;
    default:
      exhaustiveCheck(event);
  }
}
```

### 2. State Machines

```typescript
type FSMState =
  | { state: "idle" }
  | { state: "running"; startTime: number }
  | { state: "paused"; elapsed: number }
  | { state: "finished"; result: string };

function transition(current: FSMState, command: string): FSMState {
  switch (current.state) {
    case "idle":
      if (command === "start") return { state: "running", startTime: Date.now() };
      break;
    case "running":
      if (command === "pause") return { state: "paused", elapsed: Date.now() - current.startTime };
      if (command === "stop") return { state: "finished", result: "done" };
      break;
    case "paused":
      if (command === "resume") return { state: "running", startTime: Date.now() - current.elapsed };
      if (command === "stop") return { state: "finished", result: "paused" };
      break;
    case "finished":
      if (command === "reset") return { state: "idle" };
      break;
    default:
      exhaustiveCheck(current);
  }
  return current;
}

function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled state: ${JSON.stringify(x)}`);
}
```

### 3. Configuration Validation

```typescript
type DBConfig =
  | { type: "sqlite"; path: string }
  | { type: "postgres"; host: string; port: number; database: string }
  | { type: "mysql"; host: string; port: number; database: string; pool: number };

function validateDBConfig(config: DBConfig): boolean {
  switch (config.type) {
    case "sqlite":
      return config.path.length > 0;
    case "postgres":
      return config.host.length > 0 && config.port > 0;
    case "mysql":
      return config.host.length > 0 && config.port > 0 && config.pool > 0;
    default:
      exhaustiveCheck(config);
      return false;
  }
}

function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled DB config type: ${x}`);
}
```

---

## Common Pitfalls

### 1. Using `any` instead of `never`

```typescript
// ❌ Wrong — `any` disables type checking
function exhaustiveCheck(x: any): any {
  throw new Error(`Unhandled: ${x}`);
}

// ✅ Correct — `never` enforces exhaustive checking
function exhaustiveCheck(x: never): never {
  throw new Error(`Unhandled: ${x}`);
}
```

### 2. Forgetting to handle all cases before the default

```typescript
// ❌ Wrong — default before handling all cases
switch (shape.kind) {
  default:
    exhaustiveCheck(shape); // Always triggers, even for handled cases!
    break;
  case "circle":
    return Math.PI * shape.radius ** 2;
}

// ✅ Correct — default at the end
switch (shape.kind) {
  case "circle":
    return Math.PI * shape.radius ** 2;
  default:
    exhaustiveCheck(shape);
    return 0;
}
```

### 3. Not using `return` or `break` in switch cases

```typescript
// ❌ Wrong — fall-through
switch (shape.kind) {
  case "circle":
    console.log("circle");
    // Falls through to square!
  case "square":
    console.log("square");
}

// ✅ Correct — use return or break
switch (shape.kind) {
  case "circle":
    return Math.PI * shape.radius ** 2;
  case "square":
    return shape.side ** 2;
}
```

### 4. Using exhaustive checking with non-union types

```typescript
// ❌ Won't work — string is not a union type
function process(value: string) {
  switch (value) {
    case "a":
      break;
    default:
      exhaustiveCheck(value); // value is string, not never
  }
}
```

---

## Best Practices

1. **Always use `never`, not `any`** — `any` defeats the purpose
2. **Place exhaustive check in `default`** — it catches unhandled cases
3. **Use `return` in switch cases** — avoids fall-through bugs
4. **Combine with discriminated unions** — most powerful pattern
5. **Use a shared `exhaustiveCheck` function** — DRY principle
6. **Add unreachable comments** — mark code after exhaustive check as unreachable
7. **Use with TypeScript strict mode** — `strictNullChecks` and `noImplicitAny`
8. **Document the pattern in your team** — ensure everyone understands it

---

## Interview Questions

### Q1: What is exhaustive checking and why is it important?

**Answer:** Exhaustive checking is a pattern where you use the `never` type to ensure all cases in a union type are handled. A helper function accepts `never` and is placed in the `default` case of a switch. If a new union member is added but not handled, TypeScript raises a compile error. It's important because it prevents missed cases during refactoring and ensures complete handling of all possible values.

### Q2: How does the `never` type enable exhaustive checking?

**Answer:** `never` is the bottom type — no value can be assigned to it. When all union members have been handled, the remaining type is `never`. If a case is missed, the remaining type is NOT `never`, and assigning it to `never` causes a compile error. This compile-time check ensures all cases are covered.

### Q3: Can you use exhaustive checking with if-else?

**Answer:** Yes. You can use exhaustive checking with if-else by assigning the narrowed type to a variable typed as `never` in the final else branch. However, switch statements are more idiomatic because TypeScript can more easily narrow the type in each case.

### Q4: What happens if you add a new member to a discriminated union after writing an exhaustive check?

**Answer:** TypeScript raises a compile error in the `default` case of the switch. The new member's type is not `never`, so it cannot be assigned to the `never` parameter. This forces you to handle the new case before the code compiles.

### Q5: Why should you use `never` instead of `any` for exhaustive checking?

**Answer:** `any` disables type checking entirely — assigning any type to `any` is always valid. `never` is the opposite: no type can be assigned to it (except `never` itself). Using `never` ensures that unhandled cases cause compile errors, while `any` would silently accept them.

### Q6: When is exhaustive checking most critical?

**Answer:** Exhaustive checking is most critical in event handlers, state machines, API response handlers, and configuration validation — anywhere missing a case could cause a bug. It's especially valuable in large codebases where refactoring is frequent and union types evolve over time.
