# Excess Property Checking

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Object literals are rejected when they contain properties the target type does not declare, but only while the literal is fresh.

## Syntax
```ts
type Target = { known: string };
const value: Target = { known: "ok", extra: true }; // ❌ Error: 'extra' does not exist
```

## Examples
### Basic
```ts
type User = { name: string };

const ok: User = { name: "Ada" };
// const bad: User = { name: "Ada", age: 36 }; // ❌ Error: 'age' does not exist in type 'User'

console.log(ok.name);
```

### Practical
```ts
type Config = { mode: "light" | "dark" };

function apply(config: Config): void {
  console.log(config.mode);
}

apply({ mode: "dark" }); // ✅ fresh literal is checked
// apply({ mode: "dark", extra: true }); // ❌ Error: 'extra' does not exist

apply({ mode: "dark" });
```

### Advanced / edge cases
```ts
type User = { name: string };

const literal = { name: "Ada", age: 36 };
const user: User = literal; // ✅ not a fresh literal, extras are allowed

function save(value: User): void {
  console.log(value.name);
}

save(literal); // ✅ no excess property check

type Wide = { name: string; [key: string]: unknown };
const wide: Wide = { name: "Ada", age: 36 }; // ✅ index signature absorbs extras

console.log(user, wide);
```

## Key points
- Excess property checking applies to object literals written directly in an expression.
- Assigning through an intermediate variable disables the check.
- The check is about unknown properties, not about exact object types.
- An index signature that covers the extra keys accepts them.
- Function arguments, returns, and variable initializers all participate.

## Gotchas
- Extra properties survive at runtime even when the static type does not mention them.
- `// ❌ Error:` `const u: User = { name: "Ada", role: "admin" };` — fresh literals reject `role`.
- `as` and some spread patterns can suppress the check, hiding mistakes.

## Best practice
- Rely on excess checking for inline literals; it catches typos in property names.
- Validate external data at runtime instead of assuming the static check is enough.
