# Avoiding Unnecessary Annotations

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Skip annotations when inference already produces the right type; annotate only where it adds information.

## Syntax
```ts
const x = 1;            // ✅ inference is enough
const y: number = 1;    // redundant
const z: 1 = 1;         // useful if 1 is the contract
```

## Examples
### Basic
```ts
// ❌ Redundant
const title: string = "ada";
const count: number = 3;
const flag: boolean = true;

// ✅ Inferred
const title2 = "ada";
const count2 = 3;
const flag2 = true;
```

### Practical
```ts
// ❌ Redundant return and variable annotations
function double(n: number): number {
  const result: number = n * 2;
  return result;
}

// ✅ Let inference do the work
function double2(n: number) {
  const result = n * 2;
  return result;
}

// ✅ Keep annotations where they add value
const ids: number[] = []; // empty array needs a type
const nameOrNull: string | null = null; // null would infer any

console.log(double(2), double2(2), ids, nameOrNull);
```

### Advanced / edge cases
```ts
// Annotations that narrow the contract are valuable
type Status = "idle" | "loading" | "done";
const status: Status = "idle"; // constrains to the union

// Annotations that widen are usually harmful
const loose: string = "idle"; // loses the literal
const precise = "idle";       // "idle"

// Public APIs benefit from explicit return types
export function parseCount(input: string): number {
  const n = Number(input);
  return Number.isFinite(n) ? n : 0;
}

// Callbacks get types from context; no need to annotate
const lengths = ["a", "bb"].map((s) => s.length); // s: string

// Generic constraints document intent
function first<T>(items: readonly T[]): T | undefined {
  return items[0];
}

console.log(status, loose, precise, parseCount("3"), lengths, first([1]));
```

## Key points
- Inference already handles locals with clear initializers.
- Annotating with a wider type can lose useful precision.
- Keep annotations for empty values, unions, and public boundaries.
- Return annotations on exported functions document the contract.
- Parameter annotations are still required unless context supplies them.

## Gotchas
- Removing a needed annotation can cause implicit `any` or `never[]`.
- Public return annotations prevent accidental API changes.
- `const x: string = "a"` widens and may break literal-based consumers.

## Best practice
- Annotate the contract, not the obvious implementation.
- Let inference handle the rest and review diffs for widened types.
