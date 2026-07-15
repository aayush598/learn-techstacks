# Discriminated Unions in TypeScript

Discriminated unions (also called **tagged unions** or **sum types**) are one of the most powerful patterns in TypeScript. They model data that can be one of several variants, where each variant is identified by a common **discriminant** property (a literal type).

---

## Table of Contents

1. [What Are Discriminated Unions?](#what-are-discriminated-unions)
2. [The Discriminant Property](#the-discriminant-property)
3. [Basic Pattern](#basic-pattern)
4. [Switch with Discriminated Unions](#switch-with-discriminated-unions)
5. [Exhaustive Pattern Matching](#exhaustive-pattern-matching)
6. [Discriminated Unions with React](#discriminated-unions-with-react)
7. [API Response Modeling](#api-response-modeling)
8. [State Machines with Discriminated Unions](#state-machines-with-discriminated-unions)
9. [Real-World Examples](#real-world-examples)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What Are Discriminated Unions?

A discriminated union is a union of types that all share a common property with a **literal type**. TypeScript uses this common property to narrow the union to a specific variant.

```typescript
type Circle = {
  kind: "circle";    // discriminant
  radius: number;
};

type Square = {
  kind: "square";    // discriminant
  sideLength: number;
};

type Triangle = {
  kind: "triangle";  // discriminant
  base: number;
  height: number;
};

type Shape = Circle | Square | Triangle;
```

Here, `kind` is the **discriminant** — each variant has a unique string literal type for `kind`.

---

## The Discriminant Property

The discriminant must be:
1. A **common property** across all union members
2. A **literal type** (`string`, `number`, or `boolean` literal)
3. **Unique** per variant — each variant has a different literal value

```typescript
// ✅ Valid discriminated union
type Result<T> =
  | { status: "ok"; data: T }
  | { status: "error"; message: string };

// ✅ Using number as discriminant
type HTTPStatus =
  | { code: 200; body: string }
  | { code: 404; error: string }
  | { code: 500; error: string };

// ❌ NOT a discriminated union — no common discriminant
type Invalid =
  | { name: string }
  | { age: number };
// `name` and `age` are different properties, no common discriminant
```

### Common discriminant names

| Discriminant | Use Case |
|---|---|
| `kind` | Geometric shapes, UI elements |
| `type` | Actions, events, API responses |
| `status` | Result types, async states |
| `tag` | Generic tagged unions |
| `__typename` | GraphQL responses |

---

## Basic Pattern

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      // shape: { kind: "circle"; radius: number }
      return Math.PI * shape.radius ** 2;

    case "square":
      // shape: { kind: "square"; side: number }
      return shape.side ** 2;

    case "triangle":
      // shape: { kind: "triangle"; base: number; height: number }
      return (shape.base * shape.height) / 2;
  }
}
```

### Using if-else

```typescript
function area(shape: Shape): number {
  if (shape.kind === "circle") {
    // shape: Circle
    return Math.PI * shape.radius ** 2;
  } else if (shape.kind === "square") {
    // shape: Square
    return shape.side ** 2;
  } else {
    // shape: Triangle
    return (shape.base * shape.height) / 2;
  }
}
```

---

## Switch with Discriminated Unions

Switch statements are the most idiomatic way to work with discriminated unions.

```typescript
type Action =
  | { type: "INCREMENT"; amount: number }
  | { type: "DECREMENT"; amount: number }
  | { type: "SET"; value: number }
  | { type: "RESET" };

function reducer(state: number, action: Action): number {
  switch (action.type) {
    case "INCREMENT":
      return state + action.amount;
    case "DECREMENT":
      return state - action.amount;
    case "SET":
      return action.value;
    case "RESET":
      return 0;
    default:
      // exhaustive check — compile error if a case is missing
      const _exhaustive: never = action;
      return _exhaustive;
  }
}
```

---

## Exhaustive Pattern Matching

When using a switch on a discriminated union, you can use `never` to ensure all cases are handled.

```typescript
function assertNever(x: never): never {
  throw new Error(`Unexpected value: ${x}`);
}

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
    case "triangle":
      return (shape.base * shape.height) / 2;
    default:
      // If you add a new shape but forget to handle it,
      // TypeScript will error here
      return assertNever(shape);
  }
}
```

### Adding a new variant breaks the handler

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number }
  | { kind: "rectangle"; width: number; height: number }; // NEW

// The switch in the `area` function will now have a compile error
// because "rectangle" is not handled
```

---

## Discriminated Unions with React

Discriminated unions are extremely useful for modeling component props, state, and events in React.

### Component Props

```typescript
type ButtonProps =
  | { variant: "primary"; onClick: () => void; label: string }
  | { variant: "danger"; onClick: () => void; label: string }
  | { variant: "ghost"; href: string; label: string };

function Button(props: ButtonProps) {
  if (props.variant === "ghost") {
    return <a href={props.href}>{props.label}</a>;
  }
  return (
    <button
      className={`btn-${props.variant}`}
      onClick={props.onClick}
    >
      {props.label}
    </button>
  );
}
```

### Component State

```typescript
type ConnectionState =
  | { status: "disconnected" }
  | { status: "connecting"; attempt: number }
  | { status: "connected"; socketId: string; username: string }
  | { status: "error"; error: Error; retryAt: Date };

function ConnectionStatus({ state }: { state: ConnectionState }) {
  switch (state.status) {
    case "disconnected":
      return <p>Not connected</p>;
    case "connecting":
      return <p>Connecting (attempt {state.attempt})...</p>;
    case "connected":
      return <p>Connected as {state.username}</p>;
    case "error":
      return <p>Error: {state.error.message}</p>;
  }
}
```

### Event Handling

```typescript
type FormEvent =
  | { kind: "submit"; values: Record<string, string> }
  | { kind: "field_change"; field: string; value: string }
  | { kind: "validation_error"; field: string; message: string }
  | { kind: "reset" };

function handleFormEvent(event: FormEvent) {
  switch (event.kind) {
    case "submit":
      console.log("Submitting:", event.values);
      break;
    case "field_change":
      console.log(`Field ${event.field} changed to ${event.value}`);
      break;
    case "validation_error":
      console.error(`${event.field}: ${event.message}`);
      break;
    case "reset":
      console.log("Form reset");
      break;
  }
}
```

---

## API Response Modeling

Discriminated unions are perfect for modeling API responses that can succeed or fail in different ways.

```typescript
type ApiResponse<T> =
  | { status: "success"; data: T; statusCode: 200 }
  | { status: "not_found"; message: string; statusCode: 404 }
  | { status: "unauthorized"; message: string; statusCode: 401 }
  | { status: "server_error"; error: string; statusCode: 500 };

interface User {
  id: string;
  name: string;
  email: string;
}

async function fetchUser(id: string): Promise<ApiResponse<User>> {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (response.ok) {
      const data = await response.json();
      return { status: "success", data, statusCode: 200 };
    }

    if (response.status === 404) {
      return { status: "not_found", message: "User not found", statusCode: 404 };
    }

    if (response.status === 401) {
      return { status: "unauthorized", message: "Unauthorized", statusCode: 401 };
    }

    return { status: "server_error", error: "Unknown error", statusCode: 500 };
  } catch (error) {
    return { status: "server_error", error: String(error), statusCode: 500 };
  }
}

async function loadUser(id: string) {
  const result = await fetchUser(id);

  switch (result.status) {
    case "success":
      console.log(`User: ${result.data.name}`);
      break;
    case "not_found":
      console.error(result.message);
      break;
    case "unauthorized":
      console.error(result.message);
      break;
    case "server_error":
      console.error(result.error);
      break;
  }
}
```

### Generic discriminated union for API responses

```typescript
type APIResult<T, E = string> =
  | { ok: true; data: T; timestamp: number }
  | { ok: false; error: E; retryable: boolean };

type UserResult = APIResult<User, { code: string; message: string }>;

function handleResult(result: UserResult) {
  if (result.ok) {
    // result.data is User
    console.log(result.data.name);
  } else {
    // result.error is { code: string; message: string }
    console.error(`Error ${result.error.code}: ${result.error.message}`);
  }
}
```

---

## State Machines with Discriminated Unions

Model complex state transitions using discriminated unions.

```typescript
type TodoState =
  | { status: "idle" }
  | { status: "loading"; query: string; page: number }
  | { status: "success"; todos: Todo[]; page: number; hasMore: boolean }
  | { status: "error"; error: string; page: number };

type Todo = {
  id: string;
  title: string;
  completed: boolean;
};

type TodoAction =
  | { type: "SEARCH"; query: string }
  | { type: "LOAD_MORE" }
  | { type: "SUCCESS"; todos: Todo[]; hasMore: boolean }
  | { type: "ERROR"; error: string }
  | { type: "RESET" };

function todoReducer(state: TodoState, action: TodoAction): TodoState {
  switch (action.type) {
    case "SEARCH":
      return { status: "loading", query: action.query, page: 1 };

    case "LOAD_MORE":
      if (state.status !== "success") return state;
      return {
        status: "loading",
        query: state.page.toString(),
        page: state.page + 1,
      };

    case "SUCCESS":
      return {
        status: "success",
        todos: action.todos,
        page: state.status === "loading" ? state.page : 1,
        hasMore: action.hasMore,
      };

    case "ERROR":
      return {
        status: "error",
        error: action.error,
        page: state.status === "loading" ? state.page : 1,
      };

    case "RESET":
      return { status: "idle" };

    default:
      const _exhaustive: never = action;
      return _exhaustive;
  }
}
```

---

## Real-World Examples

### Payment Processing

```typescript
type PaymentResult =
  | { status: "pending"; paymentId: string }
  | { status: "completed"; paymentId: string; receipt: string }
  | { status: "failed"; paymentId: string; reason: string; canRetry: boolean }
  | { status: "refunded"; paymentId: string; refundAmount: number };

function processPayment(paymentId: string): PaymentResult {
  // ... payment logic
  return { status: "pending", paymentId };
}

function handlePaymentResult(result: PaymentResult) {
  switch (result.status) {
    case "pending":
      console.log(`Payment ${result.paymentId} is pending...`);
      break;
    case "completed":
      console.log(`Payment ${result.paymentId} completed! Receipt: ${result.receipt}`);
      break;
    case "failed":
      console.error(`Payment ${result.paymentId} failed: ${result.reason}`);
      if (result.canRetry) {
        console.log("Retrying...");
      }
      break;
    case "refunded":
      console.log(`Payment ${result.paymentId} refunded: $${result.refundAmount}`);
      break;
  }
}
```

### WebSocket Messages

```typescript
type WSMessage =
  | { type: "welcome"; userId: string; sessionId: string }
  | { type: "chat"; from: string; content: string; timestamp: number }
  | { type: "typing"; userId: string }
  | { type: "presence"; userId: string; online: boolean }
  | { type: "error"; code: number; message: string };

function handleMessage(msg: WSMessage) {
  switch (msg.type) {
    case "welcome":
      console.log(`Welcome! User: ${msg.userId}, Session: ${msg.sessionId}`);
      break;
    case "chat":
      console.log(`${msg.from}: ${msg.content}`);
      break;
    case "typing":
      console.log(`${msg.userId} is typing...`);
      break;
    case "presence":
      console.log(`${msg.userId} is now ${msg.online ? "online" : "offline"}`);
      break;
    case "error":
      console.error(`Error ${msg.code}: ${msg.message}`);
      break;
  }
}
```

### Form Validation

```typescript
type ValidationResult =
  | { valid: true }
  | { valid: false; errors: { field: string; message: string }[] };

function validateForm(data: Record<string, string>): ValidationResult {
  const errors: { field: string; message: string }[] = [];

  if (!data.name) errors.push({ field: "name", message: "Name is required" });
  if (!data.email) errors.push({ field: "email", message: "Email is required" });

  if (errors.length > 0) {
    return { valid: false, errors };
  }
  return { valid: true };
}

function handleSubmit(data: Record<string, string>) {
  const result = validateForm(data);

  if (result.valid) {
    console.log("Form is valid! Submitting...");
  } else {
    result.errors.forEach((err) => {
      console.error(`${err.field}: ${err.message}`);
    });
  }
}
```

---

## Best Practices

1. **Always use a common discriminant** — `kind`, `type`, `status`, or `__typename`
2. **Use `never` for exhaustive checks** — catch missing cases at compile time
3. **Keep discriminants as literal types** — not `string`, but `"circle"`, `"square"`, etc.
4. **Model API responses as discriminated unions** — success/error variants are natural fit
5. **Use discriminated unions for state** — eliminates impossible state combinations
6. **Use with switch for clean pattern matching** — most readable form
7. **Name properties consistently across variants** — shared properties should have the same name and type

---

## Interview Questions

### Q1: What is a discriminated union in TypeScript?

**Answer:** A discriminated union is a union type where each member has a common property (the discriminant) with a unique literal type. TypeScript uses this discriminant to narrow the union to the correct variant. It's similar to sum types in languages like Rust or Haskell, and is used for modeling state machines, API responses, and events.

### Q2: How do you create an exhaustive discriminated union handler?

**Answer:** Use a `switch` statement on the discriminant, and in the `default` case, assign the value to a variable typed as `never`. If a new variant is added to the union but not handled in the switch, TypeScript will produce a compile error because the type is not `never`.

### Q3: What are the benefits of discriminated unions over interfaces with optional properties?

**Answer:** Discriminated unions eliminate impossible states — each variant is self-contained and guarantees certain properties exist. Optional properties can be combined in ways that don't make sense (e.g., both `data` and `error` being present). Discriminated unions also enable exhaustive checking, ensuring all cases are handled.

### Q4: Can you use number literals as discriminants?

**Answer:** Yes. You can use string, number, or boolean literal types as discriminants. For example, HTTP status codes like `200`, `404`, `500` can serve as discriminants, or boolean flags like `true`/`false`.

### Q5: How do discriminated unions differ from regular unions?

**Answer:** Regular unions don't have a common property that TypeScript can use for narrowing. With regular unions, you'd need to use type assertions or type guards. Discriminated unions have a common property with literal types, allowing TypeScript to automatically narrow the union in switch/if-else blocks.

### Q6: How do you use discriminated unions with React state?

**Answer:** Define a union type for the component state where each variant represents a different state (e.g., `loading`, `success`, `error`). Use the discriminant to determine which state the component is in and render accordingly. This eliminates impossible states and ensures exhaustive rendering.
