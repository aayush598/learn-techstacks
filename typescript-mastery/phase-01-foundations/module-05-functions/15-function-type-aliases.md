# Function Type Aliases

> Phase 1 · Module 05 · Functions

**TL;DR** — Give a function shape a reusable name with `type Name = (params) => Return`.

## Syntax
```ts
type Fn = (param: Type) => ReturnType;
```

## Examples
### Basic
```ts
type Predicate<T> = (value: T) => boolean;

const isPositive: Predicate<number> = (n) => n > 0;

console.log(isPositive(1)); // true
```

### Practical
```ts
type Reducer<T, A> = (acc: A, item: T, index: number) => A;

function reduce<T, A>(items: T[], fn: Reducer<T, A>, initial: A): A {
  return items.reduce((acc, item, i) => fn(acc, item, i), initial);
}

const total = reduce([1, 2, 3], (acc, n) => acc + n, 0);
console.log(total); // 6
```

### Advanced / edge cases
```ts
// Aliases can compose other aliases
type Async<T> = () => Promise<T>;
type ErrorFirst<T> = (err: Error | null, value?: T) => void;

// ✅ generic alias with a default
type Callback<T = void> = (value: T) => void;

const done: Callback = () => {};
```

## Key points
- Type aliases are erased; they cost nothing at runtime.
- Generic aliases parameterize the input and output types.
- Aliases can reference other aliases for composition.
- Aliases are not declaration-merged (unlike interfaces).

## Gotchas
- `// ❌ Error:` `type Fn = (n: number) => number; type Fn = (n: string) => string;` — duplicate alias.
- Aliases do not create nominal types; structurally identical types are interchangeable.
- Hovering shows the alias, which can hide the expanded shape.

## Best practice
- Name aliases by role (`Predicate`, `Mapper`, `Handler`), not by shape.
- Use generic aliases to avoid repeating unions of function shapes.
