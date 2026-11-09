# Numeric Enums

> Phase 2 · Module 13 · Enums and Literal-Based Alternatives

**TL;DR** — Numeric enums map names to numbers and emit a bidirectional object at runtime, which is convenient but unsound at the type boundary.

## Syntax
```ts
enum Direction {
  Up,        // 0
  Down,      // 1
}

enum HttpStatus {
  Ok = 200,
  NotFound = 404,
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

const p: Priority = Priority.Medium;
console.log(p);           // 1
console.log(Priority[1]); // "Medium" ✅
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

function describe(status: HttpStatus): string {
  switch (status) {
    case HttpStatus.Ok:
      return "OK";
    case HttpStatus.Created:
      return "Created";
    case HttpStatus.BadRequest:
      return "Bad Request";
    case HttpStatus.NotFound:
      return "Not Found";
    default: {
      const exhaustive: never = status;
      return exhaustive;
    }
  }
}

console.log(isSuccess(HttpStatus.Created)); // true ✅
```

### Advanced / edge cases
```ts
// Bit flags: a legitimate numeric-enum use case.
enum Permission {
  None = 0,
  Read = 1 << 0,    // 1
  Write = 1 << 1,   // 2
  Execute = 1 << 2, // 4
}

function hasPermission(mask: Permission, flag: Permission): boolean {
  return (mask & flag) === flag;
}

const mask = Permission.Read | Permission.Write; // 3
console.log(hasPermission(mask, Permission.Write)); // true ✅

// Auto-increment resumes from the last explicit member.
enum Mixed {
  A = 5,
  B,     // 6
  C = 10,
  D,     // 11
}
```

```js
// enum Direction { Up, Down } emits:
var Direction;
(function (Direction) {
    Direction[Direction["Up"] = 0] = "Up";
    Direction[Direction["Down"] = 1] = "Down";
})(Direction || (Direction = {}));
```

## Key points
- Members auto-number from `0`, continuing after the last explicit value.
- Numeric enums emit both a forward map and a reverse map (`Direction[0] === "Up"`).
- Bit flags (`1 << n`) are the strongest case for numeric enums.
- The enum type is a union of its member types, so `switch` exhaustiveness works.
- Explicit values are required for anything persisted, logged, or sent over a wire.

## Gotchas
- Plain `number` is assignable to a numeric enum, so invalid values compile.
  ```ts
  enum E { A, B }
  const raw: number = 99;
  const e: E = raw; // ✅ compiles — no runtime check
  ```
- Reordering members silently changes persisted values.
- A computed member cannot be followed by an uninitialized member.
  ```ts
  function next(): number { return 1; }
  // ❌ Error: Enum member must have initializer.
  // enum E { A = next(), B }
  ```

## Best practice
- Set explicit values for anything crossing a process or storage boundary.
- Reserve numeric enums for protocols and bit flags; prefer string unions for domain states.
