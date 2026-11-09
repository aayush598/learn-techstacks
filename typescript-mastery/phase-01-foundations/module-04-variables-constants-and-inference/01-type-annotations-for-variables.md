# Type Annotations for Variables

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — An annotation is an explicit contract stating which type a variable may hold.

## Syntax
```ts
let count: number = 0;
const label: string = "ready";
let pending: boolean;
```

## Examples
### Basic
```ts
let age: number = 30;
let username: string = "ada";
let active: boolean = true;

let tags: string[] = ["ts", "types"];
let pair: [string, number] = ["age", 30];
```

### Practical
```ts
type UserId = string;

let currentUserId: UserId = "u_123";
let scores: Record<string, number> = { math: 95, art: 88 };

function log(message: string): void {
  console.log(`${message}: ${currentUserId} scored ${scores.math}`);
}

log("result");
```

### Advanced / edge cases
```ts
let value: string | number;
value = "hello"; // ✅
value = 42;      // ✅
// value = true; // ❌ Error: Type 'boolean' is not assignable to type 'string | number'.

let maybe: string | undefined;
maybe = undefined; // ✅ under strict

const frozen: readonly number[] = [1, 2, 3];
// frozen.push(4); // ❌ Error: Property 'push' does not exist on type 'readonly number[]'.
```

## Key points
- The annotation wins over the initializer for the declared type.
- An annotation is required when there is no initializer.
- Unions, arrays, tuples, and object types are all valid annotations.
- `readonly` belongs in the annotation, not the value.
- Annotated `const` keeps the annotation, not the literal type.

## Gotchas
- `let x: number;` then reading `x` before assignment fails under `strict` (`used before being assigned`).
- Annotating as `any` silently disables checking for that variable.
- A too-narrow annotation rejects valid later assignments: `let n: 1 = 1; n = 2; // ❌ Error`.

## Best practice
- Annotate public APIs, exports, and variables declared without a value.
- Let inference handle obvious local variables.
