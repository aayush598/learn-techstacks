# Narrowing limitations

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — Narrowing is a compile-time heuristic; aliasing, mutation, structural overlap, and generics can block or invalidate it.

## Syntax
```ts
const alias = value; // narrowing of value may not transfer
```

## Examples
### Basic
```ts
function demo(value: string | number): void {
  if (typeof value === "string") {
    const alias = value; // ✅ const alias keeps string
    console.log(alias.toUpperCase());
  }
}
```

### Practical
```ts
type Box = { value: string | number };

function read(box: Box): string {
  if (typeof box.value === "string") {
    box.value = 42; // mutation changes the flow type
    return box.value.toFixed(); // ✅ number
  }
  return box.value.toString();
}
```

### Advanced / edge cases
```ts
interface A { id: string }
interface B { id: string }

function isA(value: A | B): value is A {
  return true; // ⚠️ structurally identical, narrowing is meaningless
}

function mutateLater(): void {
  let value: string | number = "text";
  const read = () => value.toUpperCase(); // ⚠️ closure sees the union, not narrowed
  value = 10;
  read();
}

function generic<T>(value: T): T {
  if (typeof value === "string") {
    return value; // ✅ works for T & string
  }
  return value;
}
```

## Key points
- Structurally identical union members cannot be distinguished.
- Mutating a narrowed object property resets that property's type.
- Aliases do not always share the narrowed type.
- Generic narrowing is limited to intersections with the guard type.
- Closures and async boundaries lose narrowing of mutable variables.

## Gotchas
- A guard that always returns `true` narrows nothing meaningful.
- Aliasing through function parameters can drop narrowing.
- `// ❌ Error:` `const a: A = b;` where `b: A | B` and the members are structurally identical gives no useful discrimination.

## Best practice
- Add discriminants to types that must be distinguished.
- Avoid mutating values after narrowing; derive new values instead.
