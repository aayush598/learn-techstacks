# Type Assignability

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Assignability answers "can a value of type `S` be used where type `T` is expected?" and is what the compiler checks on every assignment.

## Syntax
```ts
type Source = { id: number; name: string };
type Target = { id: number };

const source: Source = { id: 1, name: "Ada" };
const target: Target = source; // Source is assignable to Target
```

## Examples
### Basic
```ts
let wide: string | number = "text";
let narrow: string = "text";

wide = narrow;  // ✅ string → string | number
// ❌ Error: Type 'string | number' is not assignable to type 'string'.
// narrow = wide;

console.log(wide, narrow);
```

### Practical
```ts
type User = { id: number; name: string; email: string };
type UserPreview = { id: number; name: string };

const user: User = { id: 1, name: "Ada", email: "ada@example.com" };
const preview: UserPreview = user; // ✅ more properties satisfy fewer

function render(p: UserPreview): string {
  return `${p.id}: ${p.name}`;
}

console.log(render(user)); // ✅
```

### Advanced / edge cases
```ts
// `never` is assignable to everything; `unknown` accepts everything
const a: number = (() => { throw new Error("x"); })(); // never → number
const b: unknown = 42; // number → unknown
// ❌ Error: Type 'unknown' is not assignable to type 'number'.
// const c: number = b;

// Optional and excess-property rules
type Opt = { id?: number };
const req: { id: number } = { id: 1 };
const opt: Opt = req; // ✅

// `as const` narrows, changing assignability
const literal = "dark" as const; // "dark"
const theme: string = literal;   // ✅

console.log(a, b, opt, theme);
```

## Key points
- Assignability is checked at assignments, calls, and returns.
- A narrower source is assignable to a wider target.
- `never` → any type; any type → `unknown`.
- Extra properties are allowed except on fresh object literals.
- `any` is assignable both ways, bypassing checks.

## Gotchas
- Fresh object literals trigger excess property checks.
  ```ts
  type Id = { id: number };
  // ❌ Error: 'extra' does not exist in type 'Id'.
  // const x: Id = { id: 1, extra: true };
  ```
- `unknown` cannot be assigned to a specific type without narrowing.
  ```ts
  const u: unknown = "x";
  // ❌ Error: Type 'unknown' is not assignable to type 'string'.
  // const s: string = u;
  ```
- Union assignability is directional.
  ```ts
  let u: string | number = 1;
  // ❌ Error: 'string | number' is not assignable to 'number'.
  // const n: number = u;
  ```

## Best practice
- Think "source must satisfy target" when debugging assignment errors.
- Narrow `unknown` before assigning it to a concrete type.
