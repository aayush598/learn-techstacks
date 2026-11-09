# Named Tuple Elements

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Naming tuple positions documents intent and improves editor hints without changing runtime shape.

## Syntax
```ts
let point: [x: number, y: number] = [10, 20];
let range: [start: number, end: number] = [0, 100];
```

## Examples
### Basic
```ts
const point: [x: number, y: number] = [10, 20];
const [x, y] = point;

console.log(`(${x}, ${y})`); // ✅
```

### Practical
```ts
type Range = [start: number, end: number];

function overlaps(a: Range, b: Range): boolean {
  const [aStart, aEnd] = a;
  const [bStart, bEnd] = b;
  return aStart <= bEnd && bStart <= aEnd;
}

const first: Range = [0, 10];
const second: Range = [5, 15];
console.log(overlaps(first, second)); // ✅
```

### Advanced / edge cases
```ts
// Names are documentation; positional types still rule
const p: [lat: number, lng: number] = [51.5, -0.12]; // ✅
// ❌ Error: Type 'string' is not assignable to type 'number'.
// const q: [lat: number, lng: number] = ["51.5", "-0.12"];

// Names combine with optional and rest elements
type Row = [id: number, label?: string, ...tags: string[]];
const row: Row = [1, "user", "admin", "active"]; // ✅

console.log(p, row);
```

## Key points
- Names appear in editor signatures and hover info.
- They do not change the tuple's runtime representation.
- Each element may have a distinct name.
- Names combine with optional and rest elements.
- Destructured names are independent of tuple labels.

## Gotchas
- Names are not enforced during destructuring.
  ```ts
  const point: [x: number, y: number] = [10, 20];
  const [y, x] = point; // ✅ compiles; names do not bind
  ```
- Mismatched labels are still compatible if types align.
  ```ts
  const a: [x: number, y: number] = [1, 2];
  const b: [lat: number, lng: number] = a; // ✅ labels are not checked
  ```
- Labels are erased, so runtime cannot see them.

## Best practice
- Name tuple elements whenever the positions are not obvious.
- Prefer objects when callers benefit from named properties at runtime.
