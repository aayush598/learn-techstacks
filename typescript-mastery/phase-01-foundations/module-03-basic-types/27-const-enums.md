# Const Enums

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `const enum` members are inlined at compile time and emit no runtime object.

## Syntax
```ts
const enum Direction {
  Up = "UP",
  Down = "DOWN",
}

const d = Direction.Up; // emitted as "UP"
```

## Examples
### Basic
```ts
const enum Flag {
  Off = 0,
  On = 1,
}

const state: Flag = Flag.On;
console.log(state); // 1 ✅
```

### Practical
```ts
const enum HttpMethod {
  Get = "GET",
  Post = "POST",
}

function request(method: HttpMethod, url: string): string {
  return `${method} ${url}`;
}

console.log(request(HttpMethod.Get, "/users")); // ✅
```

### Advanced / edge cases
```ts
// Members are replaced with literals at every use site
const enum Size {
  Small = 1,
  Large = 10,
}
const total = Size.Small + Size.Large; // emitted as 1 + 10

// `preserveConstEnums` keeps the runtime object for debugging
const enum Mode {
  A = "a",
}
console.log(total, Mode.A);

// `isolatedModules` forbids const enums because they cannot be inlined across files
```

## Key points
- Const enums are fully inlined; no object is emitted.
- They reduce runtime overhead for hot constants.
- `preserveConstEnums` restores a runtime object in the output.
- `isolatedModules` (and bundlers) reject them across module boundaries.
- String and numeric members both inline.

## Gotchas
- `isolatedModules` makes const enums an error.
  ```ts
  // ❌ Error: Cannot access ambient const enums when 'isolatedModules' is enabled.
  ```
- No runtime object means no `Object.values` or reverse mapping.
  ```ts
  const enum E { A = "a" }
  // ❌ Error: 'const' enums can only be used in property or index access.
  // console.log(Object.values(E));
  ```
- Inlining can bloat output if used in many places.

## Best practice
- Prefer `as const` objects for runtime-safe constant maps.
- Use const enums only in projects without `isolatedModules`.
