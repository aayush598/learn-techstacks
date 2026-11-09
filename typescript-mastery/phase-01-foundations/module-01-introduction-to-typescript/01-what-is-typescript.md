# What is TypeScript?

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript is JavaScript plus a static type system that is checked at compile time and erased before execution.

## Syntax

```ts
const greeting: string = "hello";
```

## Examples

### Basic

```ts
function add(a: number, b: number): number {
  return a + b;
}

const total: number = add(2, 3); // => 5
```

### Practical

```ts
type User = { id: number; name: string };

function formatUser(user: User): string {
  return `${user.id}: ${user.name}`;
}

console.log(formatUser({ id: 1, name: "Ada" }));
```

### Advanced / edge cases

```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: Error };

function unwrap<T>(result: Result<T>): T {
  if (result.ok) return result.value;
  throw result.error;
}

const value = unwrap({ ok: true, value: 42 }); // => 42
```

## Key points

- TypeScript is a typed superset of JavaScript that compiles to plain JavaScript.
- Types are checked statically; they do not exist in the emitted output.
- It adds annotations, interfaces, generics, and tooling support without changing JavaScript semantics.
- The compiler can target different ECMAScript versions and emit declaration files.
- Any valid JavaScript is intended to run as TypeScript, though `strict` may reject untyped patterns.

## Gotchas

- Types are erased, so you cannot use a type alias as a runtime value.

```ts
type User = { name: string };
// ❌ Error: 'User' only refers to a type, but is being used as a value here. (TS2693)
const userType = User;
```

- Type annotations do not validate data received from APIs, files, or user input.
- `as` assertions change the compiler's view, not the runtime value.

## Best practice

- Treat TypeScript as JavaScript with compile-time guarantees, not as a runtime validation layer.
- Validate untrusted data at the boundary, then let the type system protect the interior.
