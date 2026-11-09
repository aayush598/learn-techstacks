# any

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `any` disables type checking, so use it only as a deliberate escape hatch.

## Syntax
```ts
let value: any = 42;
value = "text";      // ✅
value = { a: 1 };    // ✅
value.whatever();    // ✅ no checks
```

## Examples
### Basic
```ts
let data: any = 42;
data = "now a string"; // ✅
data = [1, 2, 3];      // ✅

console.log(data.length); // ✅ unchecked
```

### Practical
```ts
// Narrow at the boundary as soon as possible
function parseJson(raw: string): unknown {
  return JSON.parse(raw); // unknown, safer than any
}

const payload: any = JSON.parse('{"id":1,"name":"Ada"}');
const id: number = payload.id; // ✅ but unchecked
console.log(id);

const safe = parseJson('{"id":1}');
if (typeof safe === "object" && safe !== null && "id" in safe) {
  console.log((safe as { id: number }).id);
}
```

### Advanced / edge cases
```ts
// any propagates through operations and contaminates results
const a: any = 1;
const b = a + 1;         // any
const c = a.map((x: number) => x); // any, even though a is a number
console.log(b, c);

// Explicit any[] is still unsafe
const list: any[] = [1, "two", null];
list.push({}); // ✅ accepted

// `noImplicitAny` catches accidental anys, not explicit ones
function identity(value: any): any {
  return value;
}
console.log(identity(1));
```

## Key points
- `any` is compatible with every type in both directions.
- Operations on `any` produce `any`, spreading unsafety.
- `noImplicitAny` bans inferred `any`, but explicit `any` remains.
- Prefer `unknown` when you need to accept arbitrary input safely.
- Migrating JS often starts with `any`, then tightens.

## Gotchas
- `any` silences errors that will crash at runtime.
  ```ts
  const user: any = {};
  // ❌ Runtime TypeError, no compile error:
  user.profile.name;
  ```
- `any` defeats IntelliSense and refactoring.
- Arrays of `any` hide element type mismatches.
  ```ts
  const xs: any[] = [1];
  xs.push("oops"); // ✅ compiles, ❌ at runtime logic
  ```

## Best practice
- Reach for `unknown` first; use `any` only when truly unavoidable.
- Isolate `any` at the edge and narrow immediately.
