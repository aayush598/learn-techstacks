# Exhaustiveness Checking Using `never`

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Assign the remaining value to `never` so any unhandled union member becomes a compile error.

## Syntax
```ts
function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${String(value)}`);
}
```

## Examples
### Basic
```ts
type Status = "idle" | "loading" | "success" | "error";

function label(status: Status): string {
  switch (status) {
    case "idle":
      return "Idle";
    case "loading":
      return "Loading";
    case "success":
      return "Done";
    case "error":
      return "Failed";
    default:
      return assertNever(status); // ✅ status is never here
  }
}

function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${String(value)}`);
}

console.log(label("success"));
```

### Practical
```ts
type Action =
  | { type: "add"; item: string }
  | { type: "remove"; id: string };

function reduce(action: Action): string {
  switch (action.type) {
    case "add":
      return `add ${action.item}`;
    case "remove":
      return `remove ${action.id}`;
    default:
      return assertNever(action);
  }
}

function assertNever(value: never): never {
  throw new Error(`Unhandled action: ${JSON.stringify(value)}`);
}

console.log(reduce({ type: "add", item: "milk" }));
```

### Advanced / edge cases
```ts
type Status = "idle" | "loading" | "success" | "error";

function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${String(value)}`);
}

declare const status: Status;

switch (status) {
  case "idle":
  case "loading":
    break;
  case "success":
  case "error":
    break;
  default:
    // ✅ compiles while all members are handled
    assertNever(status);
}

type Extended = Status | "cancelled";

// ❌ Error: Argument of type '"cancelled"' is not assignable to parameter of type 'never'.
assertNever("cancelled" as Extended);
```

## Key points
- `never` is assignable to every type, but only `never` is assignable to `never`.
- In an exhaustive branch, the remaining value narrows to `never`.
- `assertNever` both proves exhaustiveness and throws at runtime if reached.
- This catches newly added union members at compile time.
- Works with `switch`, `if` chains, and ternaries.

## Gotchas
- A `default` that throws without calling `assertNever` does not check exhaustiveness.
- Type assertions can smuggle non-`never` values past the check.

```ts
type Status = "idle" | "error";

function label(status: Status): string {
  switch (status) {
    case "idle":
      return "Idle";
    default:
      // ❌ Error: Argument of type 'Status' is not assignable to parameter of type 'never'.
      return assertNever(status);
  }
}

function assertNever(value: never): never {
  throw new Error(String(value));
}
```

## Best practice
- Keep one shared `assertNever` utility instead of duplicating it.
- Put it in `default` so future union members fail the build.
