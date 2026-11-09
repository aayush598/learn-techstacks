# Typed Rest Parameters

> Phase 1 · Module 05 · Functions

**TL;DR** — Type a rest parameter as a tuple to give each position its own type, including optionals and tails.

## Syntax
```ts
function fn(...args: [TypeA, TypeB?, ...TypeC[]]): ReturnType { /* ... */ }
```

## Examples
### Basic
```ts
function point(...coords: [number, number]): [number, number] {
  return coords;
}

console.log(point(1, 2)); // [1, 2]
```

### Practical
```ts
function createUser(...args: [name: string, age?: number]): string {
  const [name, age = 0] = args;
  return `${name} (${age})`;
}

console.log(createUser("Ada"));      // "Ada (0)"
console.log(createUser("Ada", 36));  // "Ada (36)"
```

### Advanced / edge cases
```ts
function point(...coords: [number, number]): [number, number] {
  return coords;
}

// Leading fixed element plus a variadic tail
function log(level: string, ...messages: [string, ...number[]]): string {
  return `${level}: ${messages[0]} [${messages.slice(1).join(",")}]`;
}

console.log(log("warn", "disk", 1, 2)); // "warn: disk [1,2]"

// ✅ spread a matching tuple
const coords: [number, number] = [1, 2];
console.log(point(...coords)); // [1, 2]
```

## Key points
- Tuple rest types enforce arity and per-position types.
- `?` inside a tuple marks optional positions.
- `...T[]` inside a tuple allows trailing values.
- Named tuple members document meaning at the signature.

## Gotchas
- `// ❌ Error:` `point(1, 2, 3)` — tuple length is fixed at two.
- `// ❌ Error:` `point(1)` — second tuple element is required.
- Casting to force unrelated tuple types defeats the purpose.

## Best practice
- Use labeled tuple members (`[name: string, age?: number]`) for readability.
- Prefer tuple rest for positional APIs; use an options object for many fields.
