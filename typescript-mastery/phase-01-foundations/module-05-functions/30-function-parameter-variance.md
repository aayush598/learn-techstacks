# Function Parameter Variance

> Phase 1 · Module 05 · Functions

**TL;DR** — Function parameters are contravariant under `strictFunctionTypes`: a handler may accept a supertype, not a subtype.

## Syntax
```ts
type Handler<T> = (value: T) => void;

const wider: Handler<Super> = (v) => {};
const narrow: Handler<Sub> = wider; // ✅ Super accepted where Sub is passed
```

## Examples
### Basic
```ts
type Animal = { name: string };
type Dog = Animal & { bark(): void };

type Handler<T> = (value: T) => void;

const animalHandler: Handler<Animal> = (a) => console.log(a.name);
const dogHandler: Handler<Dog> = (d) => d.bark();

const acceptsDog: Handler<Dog> = animalHandler; // ✅
// const acceptsAnimal: Handler<Animal> = dogHandler; // ❌
```

### Practical
```ts
// Contravariance keeps callbacks safe
function subscribe(handler: Handler<{ id: number }>): void {
  handler({ id: 1 });
}

const logId: Handler<{ id: number; name: string }> = (e) => console.log(e.name);

// ❌ Error: the source would read `name`, which is absent
// subscribe(logId);

subscribe((e) => console.log(e.id)); // ✅
```

### Advanced / edge cases
```ts
type Animal = { name: string };
type Dog = Animal & { bark(): void };

// Method syntax is bivariant even under strictFunctionTypes
interface Bivariant {
  handle(value: Dog): void;
}

interface Strict {
  handle: (value: Dog) => void;
}

// ✅ optional parameters also accept the matching superset
type Maybe<T> = (value?: T) => void;
const m: Maybe<number> = (value) => console.log(value);
```

## Key points
- Contravariance: if `Dog <: Animal`, then `(Animal) => void <: (Dog) => void`.
- `strictFunctionTypes` enables strict checking for function-type properties.
- Methods declared with method syntax stay bivariant for backward compatibility.
- Return types are covariant (see return type compatibility).

## Gotchas
- `// ❌ Error:` `const h: Handler<Animal> = (d: Dog) => d.bark();` — callers may pass a non-Dog.
- Bivariant methods silently permit unsound assignments.
- Arrays of callbacks inherit the same variance rules.

## Best practice
- Use function-type properties instead of methods to get strict variance checks.
- Declare callback parameters as the widest type the callback actually reads.
