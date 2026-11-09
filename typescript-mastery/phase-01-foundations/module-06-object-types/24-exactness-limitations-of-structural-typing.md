# Exactness Limitations of Structural Typing

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — TypeScript object types are open, so they cannot guarantee that a value has no properties beyond those declared.

## Syntax
```ts
type User = { name: string };
const user: User = { name: "Ada", role: "admin" }; // ❌ only fresh literals are checked
```

## Examples
### Basic
```ts
type User = { name: string };

// ❌ Error: 'role' does not exist in type 'User'
const user: User = { name: "Ada", role: "admin" };

console.log(user.name);
```

### Practical
```ts
type User = { name: string };

function save(value: User): void {
  console.log(value.name);
}

const payload = { name: "Ada", role: "admin" };
save(payload); // ✅ no excess property check through a variable

console.log(Object.keys(payload)); // ["name", "role"]
```

### Advanced / edge cases
```ts
type Exact<T, U extends T> = U & Record<Exclude<keyof U, keyof T>, never>;

type User = { name: string };

const good: Exact<User, { name: string }> = { name: "Ada" };

// ❌ Error: role must be never to satisfy Exact
const bad: Exact<User, { name: string; role: string }> = { name: "Ada", role: "admin" };

console.log(good.name);
```

## Key points
- Structural object types are open: extra properties are allowed through variables.
- Excess property checking only applies to fresh object literals.
- There is no built-in exact object type or `exact` modifier.
- Extra properties survive at runtime, in spreads, and in serialized data.
- Exactness helpers and branded types are workarounds, not built-in features.

## Gotchas
- `// ❌ Error:` `const u: User = { name: "Ada", role: "admin" };` is rejected, but the same object stored in a variable is accepted.
- `satisfies` validates a fresh literal but still does not make the type exact afterward.
- Runtime data can contain keys your type never mentions.

## Best practice
- Validate and strip unknown keys at runtime when exactness matters.
- Use an `Exact` helper or branded types only where the extra complexity is justified.
