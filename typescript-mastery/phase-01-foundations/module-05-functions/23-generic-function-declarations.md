# Generic Function Declarations

> Phase 1 · Module 05 · Functions

**TL;DR** — Add type parameters before the parameter list to relate input and output types.

## Syntax
```ts
function fn<T>(param: T): T { /* ... */ }
function fn<T extends Constraint>(param: T): T { /* ... */ }
```

## Examples
### Basic
```ts
function identity<T>(value: T): T {
  return value;
}

const n = identity(1);        // number
const s = identity("hi");     // string
```

### Practical
```ts
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [{ id: 1, name: "Ada" }, { id: 2, name: "Bob" }];
console.log(pluck(users, "name")); // ["Ada", "Bob"]
```

### Advanced / edge cases
```ts
// Multiple type parameters with a default
function pair<A, B = A>(a: A, b: B): [A, B] {
  return [a, b];
}

console.log(pair(1, "x")); // [number, string]
console.log(pair(1, 2));   // [number, number]

// ✅ const type parameter keeps literal types (TS 5.0+)
function tuple<const T extends readonly unknown[]>(items: T): T {
  return items;
}

const t = tuple([1, "a"] as const); // readonly [1, "a"]
```

## Key points
- Type arguments are usually inferred from the call.
- Constraints (`extends`) restrict what `T` can be.
- Defaults (`T = string`) apply when inference fails.
- Type parameters only exist at compile time.

## Gotchas
- `// ❌ Error:` `fn<string>(1)` — explicit type argument conflicts with the argument.
- Unconstrained `T` cannot access properties; add a constraint.
- Generic inference can widen literals unless `const` is used.

## Best practice
- Constrain generics to the smallest useful shape (`{ length: number }`).
- Let inference do the work; annotate type arguments only when necessary.
