# Numeric Enums

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Numeric enums auto-number members from `0` (or a custom start) and provide reverse mappings.

## Syntax
```ts
enum Status {
  Idle,      // 0
  Loading,   // 1
  Done,      // 2
}

enum Http {
  Ok = 200,
  NotFound = 404,
  Error = 500,
}
```

## Examples
### Basic
```ts
enum Priority {
  Low,
  Medium,
  High,
}

console.log(Priority.Low);    // 0
console.log(Priority.Medium); // 1
console.log(Priority.High);   // 2
console.log(Priority[2]);     // "High" ✅
```

### Practical
```ts
enum HttpStatus {
  Ok = 200,
  Created = 201,
  BadRequest = 400,
  NotFound = 404,
}

function isSuccess(status: HttpStatus): boolean {
  return status >= 200 && status < 300;
}

console.log(isSuccess(HttpStatus.Created)); // true ✅
```

### Advanced / edge cases
```ts
// Auto-increment continues from the last explicit value
enum Mixed {
  A = 10,
  B,        // 11
  C = 20,
  D,        // 21
}

// Computed members are allowed but cannot precede auto members without a value
enum Flags {
  None = 0,
  Read = 1 << 0,  // 1
  Write = 1 << 1, // 2
}

console.log(Mixed.B, Mixed.D, Flags.Read | Flags.Write); // 11 21 3
```

## Key points
- Auto-numbering starts at `0` unless overridden.
- A following member increments the last explicit value.
- Numeric enums emit a reverse map (`Status[0] === "Idle"`).
- Bit flags are a common numeric-enum pattern.
- Computed members must come after any auto-numbered ones.

## Gotchas
- A `number` variable is assignable to a numeric enum, allowing invalid values.
  ```ts
  enum P { Low, High }
  const n: number = 42;
  const p: P = n; // ✅ compiles; validate at boundaries
  ```
- Auto-numbering breaks if you reorder members.
  ```ts
  enum E { A, B } // A=0, B=1
  ```
- Computed members need explicit values.
  ```ts
  // ❌ Error: Enum member must have initializer.
  // enum E { A = 1 << 0, B }
  ```

## Best practice
- Use explicit numeric values when they are serialized or persisted.
- Use bit flags for combinable options, not for ordinary choices.
