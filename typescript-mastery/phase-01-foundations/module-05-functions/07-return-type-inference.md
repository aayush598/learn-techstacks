# Return Type Inference

> Phase 1 · Module 05 · Functions

**TL;DR** — TypeScript infers the return type from `return` statements when you omit the annotation.

## Syntax
```ts
function fn(param: Type) {
  return value; // inferred return type
}
```

## Examples
### Basic
```ts
function triple(n: number) {
  return n * 3;
}

// ✅ inferred as number
const x: number = triple(2);
```

### Practical
```ts
function toPair(a: number) {
  return [a, a] as const;
}

// inferred as readonly [number, number]
const pair = toPair(5);

// ✅ multiple returns unite into a union
function pick(flag: boolean) {
  return flag ? 1 : "none"; // number | string
}
```

### Advanced / edge cases
```ts
// Async functions infer Promise<...>
async function load(id: number) {
  return { id, ok: true };
}
// inferred: Promise<{ id: number; ok: boolean }>

// ✅ recursive functions may need an explicit annotation
function depth(node: { children: { children: unknown[] }[] }): number {
  return 1;
}
```

## Key points
- Inference walks every `return` statement and unions the results.
- No `return` (or only bare `return;`) infers `void`.
- Async functions wrap the inferred type in `Promise`.
- Inference can widen literals to their base type unless `as const` is used.

## Gotchas
- `// ❌ Error:` recursive functions without annotations can fail with "implicitly has return type `any`".
- Returning object literals infers mutable properties, not literals.
- Inferred unions can be broader than intended.

## Best practice
- Annotate public APIs and recursive functions; let private one-liners infer.
- Add `as const` when literal tuple/object types are required.
