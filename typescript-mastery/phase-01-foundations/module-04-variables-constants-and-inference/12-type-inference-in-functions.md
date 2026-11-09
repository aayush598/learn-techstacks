# Type Inference in Functions

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — Parameter types must be annotated or contextual; return types are inferred from returned expressions.

## Syntax
```ts
function add(a: number, b: number) { return a + b; }
const double = (n: number) => n * 2;
function label(value: number): string { return `${value}`; }
```

## Examples
### Basic
```ts
function add(a: number, b: number) {
  return a + b; // number
}

const double = (n: number) => n * 2; // (n: number) => number

function log(message: string) {
  console.log(message); // void
}
```

### Practical
```ts
function firstOf<T>(items: readonly T[]): T | undefined {
  return items[0];
}

const first = firstOf([1, 2, 3]); // number | undefined

function parse(input: string) {
  try {
    return JSON.parse(input) as unknown;
  } catch {
    return null; // inferred: unknown | null
  }
}

const parsed = parse('{"ok":true}');

console.log(first, parsed);
```

### Advanced / edge cases
```ts
// Literal returns widen
function readStatus() {
  return "ready"; // string
}

function exactStatus(): "ready" {
  return "ready"; // ✅
}

// Union returns are inferred
function idOrName(id: number | string) {
  return typeof id === "number" ? id : id.toUpperCase(); // string | number
}

// Recursive functions need a return annotation
function depth(node: { children: { children: unknown[] }[] }): number {
  return node.children.length;
}

// Arrow with contextual return type
const makeUser: () => { id: number } = () => ({ id: 1 });

console.log(readStatus(), exactStatus(), idOrName(1), depth({ children: [] }), makeUser());
```

## Key points
- Parameters are never inferred from the body; annotate them.
- Return types are inferred from all return expressions.
- Literal returns widen unless the return type is annotated.
- Recursive and mutually recursive functions need return annotations.
- Overloads and contextual types also drive return inference.

## Gotchas
- Missing return on some paths yields `undefined` in the union.
- `return` with no value infers `void`, not `undefined`.
- Inference cannot see call sites, so generic returns may widen.

## Best practice
- Annotate parameters always; annotate returns at public boundaries.
- Let inference handle small local helpers with obvious returns.
