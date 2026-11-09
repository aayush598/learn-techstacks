# null

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `null` is an explicit "no value" and, under `strictNullChecks`, only assignable to types that include it.

## Syntax
```ts
let value: null = null;
let maybe: string | null = null;
function find(id: string): string | null { /* ... */ return null; }
```

## Examples
### Basic
```ts
const nothing: null = null;
let selected: string | null = null;

selected = "row-1"; // ✅
selected = null;    // ✅
console.log(nothing, selected);
```

### Practical
```ts
type User = { id: number; name: string };

function findUser(id: number): User | null {
  return id === 1 ? { id, name: "Ada" } : null;
}

const user = findUser(1);
if (user !== null) {
  console.log(user.name); // ✅ narrowed to User
}
```

### Advanced / edge cases
```ts
type User = { id: number; name: string };

function findUser(id: number): User | null {
  return id === 1 ? { id, name: "Ada" } : null;
}

// Nullish coalescing replaces null and undefined only
const fallback = findUser(2) ?? { id: 0, name: "Guest" };
console.log(fallback.name);

// Optional chaining short-circuits on null
const upper = findUser(1)?.name.toUpperCase();
console.log(upper); // string | undefined

// typeof null is "object" — a historic quirk
console.log(typeof null); // "object"
```

## Key points
- `null` represents an intentional absence of a value.
- With `strictNullChecks`, `null` is not assignable to other types.
- `??` and `?.` are the safe ways to handle nullable values.
- Use `=== null` (or `== null` for null and undefined) to test.
- Prefer `null` for "explicitly empty" and `undefined` for "not provided".

## Gotchas
- `typeof null` is `"object"`, so it fools `typeof` checks.
  ```ts
  // ❌ Error: Object is possibly 'null'.
  // const s: string = null;
  ```
- `JSON.stringify` keeps `null` but drops `undefined`.
  ```ts
  console.log(JSON.stringify({ a: null, b: undefined })); // {"a":null}
  ```
- Comparing with `==` also matches `undefined`.
  ```ts
  console.log(null == undefined); // true
  ```

## Best practice
- Include `null` in the type whenever a value can be absent.
- Handle it at the boundary with `if (x !== null)` or `??`.
