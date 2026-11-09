# Narrowing with literal types

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Literal types let equality checks narrow a value to one exact string, number, or boolean.

## Syntax
```ts
type Direction = "north" | "south" | "east" | "west";
```

## Examples
### Basic
```ts
type Status = "pending" | "active" | "closed";

function label(status: Status): string {
  if (status === "pending") {
    return "Waiting"; // ✅ "pending"
  }
  if (status === "active") {
    return "Running"; // ✅ "active"
  }
  return "Finished"; // ✅ "closed"
}
```

### Practical
```ts
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

function hasBody(method: HttpMethod): boolean {
  switch (method) {
    case "GET":
    case "DELETE":
      return false; // ✅ GET | DELETE
    case "POST":
    case "PUT":
      return true; // ✅ POST | PUT
  }
}
```

### Advanced / edge cases
```ts
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;

function isCritical(roll: DiceRoll): boolean {
  return roll === 6; // ✅ narrows to 6
}

type Flag = true | false;
function toggle(flag: Flag): Flag {
  return flag === true ? false : true; // ✅ literal narrowing
}

function assertStatus(value: string): asserts value is Status {
  if (!["pending", "active", "closed"].includes(value)) {
    throw new Error(`Invalid status: ${value}`);
  }
}
```

## Key points
- Literal unions narrow precisely with `===`, `switch`, and `case`.
- String, number, and boolean literals all work.
- `as const` preserves literals in object and array values.
- Literal narrowing feeds into discriminated unions.
- Widening to `string` loses literal precision.

## Gotchas
- A plain `string` annotation widens literals away.
- Object properties need `as const` or explicit literal types to stay literal.
- `// ❌ Error:` `if (status === "unknown")` when `Status` has no `"unknown"` member.

## Best practice
- Model finite states as literal unions.
- Use `as const` for configuration objects you compare by literal.
