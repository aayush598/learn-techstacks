# String Enums

> Phase 1 · Module 03 · Basic Types

**TL;DR** — String enums assign explicit string values, producing readable logs and stable serialized data.

## Syntax
```ts
enum Direction {
  Up = "UP",
  Down = "DOWN",
}

let d: Direction = Direction.Up;
```

## Examples
### Basic
```ts
enum Color {
  Red = "red",
  Green = "green",
  Blue = "blue",
}

console.log(Color.Green); // "green" ✅
```

### Practical
```ts
enum OrderStatus {
  Pending = "pending",
  Shipped = "shipped",
  Delivered = "delivered",
}

function describe(status: OrderStatus): string {
  switch (status) {
    case OrderStatus.Pending:
      return "Awaiting shipment";
    case OrderStatus.Shipped:
      return "On the way";
    case OrderStatus.Delivered:
      return "Complete";
  }
}

console.log(describe(OrderStatus.Shipped)); // ✅
```

### Advanced / edge cases
```ts
// String enums have no reverse mapping
enum Role {
  Admin = "admin",
  User = "user",
}

console.log(Object.values(Role)); // ["admin", "user"] ✅
console.log(Role.Admin);          // "admin"
// console.log(Role["admin"]);    // undefined at runtime

// Each member must be initialized explicitly
enum Code {
  Ok = "OK",
  Fail = "FAIL",
}
console.log(Code.Fail);
```

## Key points
- Every string enum member needs an explicit string value.
- No auto-numbering and no reverse mapping.
- Values serialize cleanly to JSON and logs.
- Members remain distinct from raw string literals in strict enum typing.
- Ideal for API-facing and persisted values.

## Gotchas
- Raw strings are not assignable to the enum type.
  ```ts
  enum E { A = "a" }
  // ❌ Error: Type '"a"' is not assignable to type 'E'.
  // const e: E = "a";
  ```
- Duplicate string values are allowed and collapse at runtime.
  ```ts
  enum E { A = "x", B = "x" } // both "x"
  ```
- String enums cannot have computed values from other enums in all cases.

## Best practice
- Use string enums when values cross a serialization boundary.
- Consider a literal union when you do not need a runtime object.
