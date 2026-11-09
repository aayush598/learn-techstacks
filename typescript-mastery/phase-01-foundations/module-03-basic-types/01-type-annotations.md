# Type Annotations

> Phase 1 · Module 03 · Basic Types

**TL;DR** — An annotation states a type explicitly so the compiler checks every value against your declared intent.

## Syntax
```ts
let name: string;
const count: number = 0;

function add(a: number, b: number): number {
  return a + b;
}

type User = { id: number; name: string };
const user: User = { id: 1, name: "Ada" };
```

## Examples
### Basic
```ts
let title: string = "TypeScript";
let version: number = 5.4;
let isStable: boolean = true;

console.log(`${title} v${version} stable=${isStable}`);
```

### Practical
```ts
type Order = { id: string; total: number };

function formatTotal(order: Order): string {
  return `#${order.id}: $${order.total.toFixed(2)}`;
}

const order: Order = { id: "A-1", total: 19.5 };
console.log(formatTotal(order)); // ✅
```

### Advanced / edge cases
```ts
// Annotations on arrow params, returns, and destructuring patterns
const parse = (input: string): number[] =>
  input.split(",").map((part: string): number => Number(part));

const { length }: { length: number } = [1, 2, 3];
console.log(parse("1,2,3"), length); // ✅

// A union annotation may be left unassigned until a valid value arrives
let nickname: string | undefined;
nickname = "TS"; // ✅
```

## Key points
- Annotations appear after a colon: `let x: number`.
- Functions annotate parameters and, optionally, the return type.
- Annotations are compile-time only; they are erased from the emitted JavaScript.
- `strict` mode makes unannotated parameters and uninitialized variables errors.
- Use annotations where inference cannot see your intent.

## Gotchas
- Annotating a variable with a wider type can hide a mistake.
  ```ts
  let id: string | number = 42; // ✅ but loses precision about intent
  ```
- A wrong annotation is an error even if the runtime value looks fine.
  ```ts
  // ❌ Error: Type 'string' is not assignable to type 'number'.
  const n: number = "42";
  ```
- Reassigning to a different type is rejected.
  ```ts
  let x: number = 1;
  // ❌ Error: Type 'string' is not assignable to type 'number'.
  x = "one";
  ```

## Best practice
- Annotate public boundaries (exports, function signatures); let inference handle locals.
- Prefer the narrowest annotation that expresses intent.
