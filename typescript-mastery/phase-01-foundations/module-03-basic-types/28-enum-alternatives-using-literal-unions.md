# Enum Alternatives Using Literal Unions

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A `const` object plus a literal union gives enum-like ergonomics with full type safety and tree-shaking.

## Syntax
```ts
const Direction = {
  Up: "UP",
  Down: "DOWN",
} as const;

type Direction = (typeof Direction)[keyof typeof Direction];
// "UP" | "DOWN"
```

## Examples
### Basic
```ts
const Color = {
  Red: "red",
  Green: "green",
  Blue: "blue",
} as const;

type Color = (typeof Color)[keyof typeof Color];

const c: Color = Color.Green; // ✅
console.log(c); // "green"
```

### Practical
```ts
const OrderStatus = {
  Pending: "pending",
  Shipped: "shipped",
  Delivered: "delivered",
} as const;

type OrderStatus = (typeof OrderStatus)[keyof typeof OrderStatus];

function describe(status: OrderStatus): string {
  switch (status) {
    case OrderStatus.Pending:
      return "Awaiting";
    case OrderStatus.Shipped:
      return "In transit";
    case OrderStatus.Delivered:
      return "Done";
  }
}

console.log(describe(OrderStatus.Shipped)); // ✅
```

### Advanced / edge cases
```ts
// A pure union works when you do not need runtime values
type Method = "GET" | "POST" | "PUT" | "DELETE";
const m: Method = "GET"; // ✅

// Derive a runtime list for validation
const Statuses = ["idle", "loading", "done"] as const;
type Status = (typeof Statuses)[number]; // "idle" | "loading" | "done"

function isStatus(value: string): value is Status {
  return (Statuses as readonly string[]).includes(value);
}

console.log(m, isStatus("done")); // ✅
```

## Key points
- `as const` preserves literal values; the indexed access builds the union.
- You get both a runtime object and a precise type.
- Works with `isolatedModules` and modern bundlers.
- Raw strings are assignable, unlike strict string enums.
- Pure unions are the simplest option when no runtime lookup is needed.

## Gotchas
- Forgetting `as const` widens values to `string`.
  ```ts
  const Color = { Red: "red" };
  type Color = (typeof Color)[keyof typeof Color]; // string
  ```
- The type and value can share a name only via declaration merging rules.
  ```ts
  const E = { A: "a" } as const;
  type E = (typeof E)[keyof typeof E]; // ✅ valid
  ```
- Union members are structurally open; any matching string is accepted.

## Best practice
- Prefer `as const` objects over enums for new code.
- Use a plain literal union when you do not need runtime values.
