# Literal Union Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — A literal union enumerates exact allowed values such as strings or numbers.

## Syntax
```ts
type Allowed = "value1" | "value2" | 200 | 404;
```

## Examples
### Basic
```ts
type Direction = "north" | "south" | "east" | "west";

function move(direction: Direction): void {
  console.log(`Moving ${direction}`);
}

// ✅ only the four literals are accepted
move("north");
```

### Practical
```ts
type LogLevel = "debug" | "info" | "warn" | "error";
type HttpStatus = 200 | 201 | 204 | 400 | 401 | 404 | 500;

const level: LogLevel = "warn";
const status: HttpStatus = 404;

// ✅ literal unions document the allowed domain precisely
console.log(level, status);
```

### Advanced / edge cases
```ts
const ROLES = ["admin", "editor", "viewer"] as const;
type Role = (typeof ROLES)[number]; // "admin" | "editor" | "viewer"

function hasRole(role: Role): boolean {
  return ROLES.includes(role);
}

// ✅ derive the union from the runtime source of truth
console.log(hasRole("editor"));

const config = {
  mode: "dark",
  retries: 3,
} as const satisfies { mode: "light" | "dark"; retries: number };

// ✅ satisfies checks the shape while preserving literal types
console.log(config.mode);
```

## Key points
- Literal unions model closed sets: statuses, roles, modes, event names.
- String literals are the most common; number and boolean literals also work.
- `as const` preserves literals that would otherwise widen.
- `(typeof array)[number]` derives a union from a constant array.
- `satisfies` validates a value without widening its literals.

## Gotchas
- A plain `let` widens `"dark"` to `string` unless annotated or `as const`.
- Adding a new value requires updating the union, which is usually the point.

```ts
let mode = "dark"; // type is string
// ❌ Error: Type 'string' is not assignable to type '"light" | "dark"'.
const theme: "light" | "dark" = mode;
```

## Best practice
- Prefer a derived union (`typeof VALUES[number]`) when a runtime array exists.
- Use literal unions at API and configuration boundaries to reject typos early.
