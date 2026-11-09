# Function Return Type Compatibility

> Phase 1 · Module 05 · Functions

**TL;DR** — Return types are covariant: a function returning a subtype can stand in for one returning a supertype.

## Syntax
```ts
type Factory<T> = () => T;

const makeDog: Factory<Dog> = () => dog;
const makeAnimal: Factory<Animal> = makeDog; // ✅ Dog is an Animal
```

## Examples
### Basic
```ts
type Animal = { name: string };
type Dog = Animal & { bark(): void };

type Factory<T> = () => T;

const makeDog: Factory<Dog> = () => ({ name: "Rex", bark() {} });
const makeAnimal: Factory<Animal> = makeDog; // ✅

console.log(makeAnimal().name); // "Rex"
```

### Practical
```ts
// Returning a union is assignable to the matching union target
type Status = "ok" | "error";
const getStatus = (): Status => "ok";

const asString = (): string => "ok";
const wider: () => string = asString; // ✅

// ✅ A value return satisfies a void target
type Notify = (msg: string) => void;
const notify: Notify = (msg) => msg.length; // return discarded
```

### Advanced / edge cases
```ts
// Functions returning `never` are assignable to anything
type Thrower = () => never;
const fail: Thrower = () => {
  throw new Error("boom");
};

const numFactory: () => number = fail; // ✅ never <: number

// ❌ Error: string is not a number
// const f: () => number = (): string => "x";
```

## Key points
- Return types are covariant: `() => Dog` is assignable to `() => Animal`.
- A `never` return is assignable to every return type.
- A value-returning function is assignable to a `void`-returning target.
- The reverse direction (supertype return to subtype target) is unsafe.

## Gotchas
- `// ❌ Error:` `const f: Factory<Dog> = makeAnimal;` — the animal may not bark.
- `void` targets discard the return, which can hide side effects.
- `Promise<T>` return compatibility follows the same covariance rule.

## Best practice
- Return precise subtypes from implementations; let callers widen.
- Prefer `void` only when the result truly does not matter.
