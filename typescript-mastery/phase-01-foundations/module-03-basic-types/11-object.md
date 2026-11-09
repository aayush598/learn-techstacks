# object

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `object` means any non-primitive value; it says nothing about which properties exist.

## Syntax
```ts
let value: object = { id: 1 };
value = [1, 2, 3]; // ✅ arrays are objects
value = () => {};  // ✅ functions are objects
// value = 42;     // ❌ primitives are not objects
```

## Examples
### Basic
```ts
const config: object = { host: "localhost", port: 3000 };
const list: object = [1, 2, 3];
const fn: object = () => "hi";

console.log(config, list, fn);
```

### Practical
```ts
// Use object to accept "something structured" then narrow keys
function hasId(value: object): value is { id: number } {
  return "id" in value && typeof (value as { id: unknown }).id === "number";
}

function describe(value: object): string {
  return hasId(value) ? `id=${value.id}` : "no id";
}

console.log(describe({ id: 1 })); // ✅
console.log(describe({ name: "Ada" }));
```

### Advanced / edge cases
```ts
// `object` excludes primitives but includes functions and arrays
type NonPrimitive = object;
const arr: NonPrimitive = [];
const f: NonPrimitive = () => {};
console.log(arr, f);

// `Object` and `{}` are different, looser types
const a: {} = 42;     // ✅ any non-null value
const b: Object = 42; // ✅ boxed; avoid
const c: object = {}; // ✅ only non-primitives
console.log(a, b, c);

// Index access still requires a narrower type
function keys(value: object): string[] {
  return Object.keys(value);
}
console.log(keys({ x: 1, y: 2 })); // ✅
```

## Key points
- `object` accepts objects, arrays, functions, and class instances.
- It rejects `string`, `number`, `boolean`, `symbol`, `bigint`, `null`, and `undefined`.
- `object` does not describe properties; use a shape type for that.
- `Object` (capitalized) and `{}` are broader and usually a mistake.
- `Object.keys` works on `object` and returns `string[]`.

## Gotchas
- `object` does not let you access arbitrary properties.
  ```ts
  const o: object = { id: 1 };
  // ❌ Error: Property 'id' does not exist on type 'object'.
  // o.id;
  ```
- `null` and `undefined` are not assignable to `object`.
  ```ts
  // ❌ Error: Type 'null' is not assignable to type 'object'.
  // const n: object = null;
  ```
- `{}` accepts primitives, so it is not "an empty object".
  ```ts
  const e: {} = "not empty"; // ✅ surprising
  ```

## Best practice
- Use a concrete shape (`{ id: number }`) instead of bare `object` when possible.
- Use `object` only for generic "any non-primitive" parameters.
