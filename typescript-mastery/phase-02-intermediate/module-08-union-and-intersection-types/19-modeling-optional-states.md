# Modeling Optional States

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Represent states as distinct union variants instead of piling optional fields onto one object.

## Syntax
```ts
type State<T> =
  | { status: "idle" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };
```

## Examples
### Basic
```ts
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

const idle: RequestState<string[]> = { status: "idle" };
const loading: RequestState<string[]> = { status: "loading" };
const success: RequestState<string[]> = { status: "success", data: ["a"] };

// ✅ each state carries exactly the fields it needs
console.log(idle, loading, success);
```

### Practical
```ts
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function render(state: RequestState<string[]>): string {
  switch (state.status) {
    case "idle":
      return "Press search";
    case "loading":
      return "Loading...";
    case "success":
      return state.data.join(", "); // ✅ data exists only here
    case "error":
      return `Failed: ${state.error.message}`; // ✅ error exists only here
  }
}

console.log(render({ status: "success", data: ["types", "unions"] }));
```

### Advanced / edge cases
```ts
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function retry<T>(state: RequestState<T>): RequestState<T> {
  switch (state.status) {
    case "idle":
    case "loading":
      return state;
    case "success":
      return { status: "loading" }; // ✅ drop stale data on retry
    case "error":
      return { status: "loading" }; // ✅ clear the error
  }
}

// ✅ transitions are explicit and total
console.log(retry({ status: "error", error: new Error("timeout") }));
```

## Key points
- Each state carries only the data valid in that state.
- The discriminant makes impossible combinations unrepresentable.
- `switch` over `status` narrows payloads automatically.
- Generic state unions work for any fetched type.
- State transitions become explicit, testable functions.

## Gotchas
- Optional fields let `data` and `error` exist simultaneously.
- A boolean like `isLoading` does not prevent contradictory fields.

```ts
type LooseState<T> = {
  isLoading: boolean;
  data?: T;
  error?: Error;
};

// ✅ compiles, but loading with data and an error is nonsense
const broken: LooseState<string> = {
  isLoading: true,
  data: "stale",
  error: new Error("boom"),
};
```

## Best practice
- Make `status` the single source of truth for UI state.
- Model transitions as pure functions returning the next state union.
