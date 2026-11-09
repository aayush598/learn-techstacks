# Enum Types

> Phase 1 · Module 03 · Basic Types

**TL;DR** — An `enum` defines a named set of related constants that exists at runtime.

## Syntax
```ts
enum Direction {
  Up,
  Down,
  Left,
  Right,
}

let d: Direction = Direction.Up;
```

## Examples
### Basic
```ts
enum Color {
  Red,
  Green,
  Blue,
}

const c: Color = Color.Green;
console.log(c);            // 1
console.log(Color[c]);     // "Green" (reverse mapping) ✅
```

### Practical
```ts
enum LogLevel {
  Debug = "debug",
  Info = "info",
  Error = "error",
}

function log(level: LogLevel, message: string): void {
  console.log(`[${level}] ${message}`);
}

log(LogLevel.Info, "started"); // ✅
log(LogLevel.Error, "failed"); // ✅
```

### Advanced / edge cases
```ts
// Enums are objects at runtime and can be iterated by name
enum Status {
  Active = "active",
  Inactive = "inactive",
}

const values = Object.values(Status); // string[]
console.log(values);

// Enums can be used as types and values
function setStatus(status: Status): Status {
  return status;
}
console.log(setStatus(Status.Active)); // ✅

// A const object with `as const` is a runtime-preserving alternative
const Role = { Admin: "admin", User: "user" } as const;
type Role = (typeof Role)[keyof typeof Role];
console.log(Role.Admin);
```

## Key points
- Enums create both a type and a runtime object.
- Members can be numeric (default) or string-valued.
- Numeric enums get reverse mappings; string enums do not.
- Enums are nominal-ish and stricter than literal unions in some cases.
- `const enum` inlines members and emits no object.

## Gotchas
- A `number` variable is assignable to a numeric enum, so out-of-range values slip in.
  ```ts
  enum Level { Low, High }
  const n: number = 99;
  const x: Level = n; // ✅ compiles, but 99 is not a member
  ```
- String enums do not have reverse mappings.
  ```ts
  enum E { A = "a" }
  // console.log(E["a"]); // undefined at runtime
  ```
- Enum values are not interchangeable with raw strings in strict enum typing.
  ```ts
  enum E { A = "a" }
  // ❌ Error: Type '"a"' is not assignable to type 'E'.
  // const e: E = "a";
  ```

## Best practice
- Prefer string enums or literal unions for readable serialized values.
- Avoid relying on numeric enum reverse mappings in application logic.
