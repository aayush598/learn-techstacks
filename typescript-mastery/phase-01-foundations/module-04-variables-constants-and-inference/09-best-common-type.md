# Best Common Type

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — When several candidate types exist, TypeScript picks a best common type that all candidates are assignable to.

## Syntax
```ts
const numbers = [1, 2, 3]; // number[]
const mixed = [1, "two"];  // (string | number)[]
```

## Examples
### Basic
```ts
const nums = [1, 2, 3];          // number[]
const strs = ["a", "b"];         // string[]
const flags = [true, false];     // boolean[]

const mixed = [1, "two"];        // (string | number)[]
```

### Practical
```ts
class Animal {
  constructor(public name: string) {}
}
class Dog extends Animal {
  bark(): void {
    console.log("woof");
  }
}

const animals = [new Animal("cat"), new Dog("rex")]; // Animal[]
animals.forEach((a) => console.log(a.name));

const nullable = [1, null, 2]; // (number | null)[] under strict
```

### Advanced / edge cases
```ts
type A = { kind: "a"; a: number };
type B = { kind: "b"; b: number };

const items = [
  { kind: "a", a: 1 } as A,
  { kind: "b", b: 2 } as B,
]; // (A | B)[]

// No common base beyond object -> union is chosen
const mixed = [1, "x", true]; // (string | number | boolean)[]

// If no candidate is assignable to the others, a union is synthesized
const tupleLike = [1, "one"] as const; // readonly [1, "one"]

// Explicit annotation overrides best-common-type selection
const narrowed: Array<number | string> = [1, "one"];

console.log(items, mixed, tupleLike, narrowed);
```

## Key points
- Arrays collect candidates and compute one element type.
- Compatible object types resolve to the common supertype.
- Incompatible candidates produce a union, not `any`.
- Literal candidates widen before the common type is computed.
- An explicit annotation bypasses the algorithm entirely.

## Gotchas
- Best common type can widen away useful literals: `[1, 2]` becomes `number[]`.
- Structurally unrelated classes produce a union, losing shared methods.
- Empty arrays have no candidates and infer `never[]`.

## Best practice
- Annotate arrays when you need a specific element type or literal preservation.
- Prefer `as const` for fixed collections where exact members matter.
