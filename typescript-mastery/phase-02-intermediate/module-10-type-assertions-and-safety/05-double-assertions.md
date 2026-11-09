# Double Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — A double assertion (`as unknown as T`) chains two casts to bypass the compiler's overlap check, and is a strong signal to re-examine the design.

## Syntax

```ts
const value = expression as unknown as Target;
```

## Examples

### Basic

```ts
const raw = "42";
const numeric = raw as unknown as number;

console.log(numeric); // "42"
console.log(typeof numeric); // "string" — the cast lies
```

### Practical

```ts
// A DOM lookup returns a generic element; we know the template guarantees a canvas.
const canvas = document.querySelector("#chart") as unknown as HTMLCanvasElement;
const ctx = canvas.getContext("2d");

if (ctx) {
  ctx.fillStyle = "#0af";
  ctx.fillRect(0, 0, 10, 10);
}
```

A checked alternative avoids the double cast:

```ts
const el = document.querySelector("#chart");
if (el instanceof HTMLCanvasElement) {
  el.getContext("2d"); // ✅ narrowed safely
}
```

### Advanced / edge cases

```ts
type Celsius = { unit: "C"; value: number };
type Fahrenheit = { unit: "F"; value: number };

const celsius: Celsius = { unit: "C", value: 20 };

// The compiler cannot see a relationship, so it permits the bypass.
const fahrenheit = celsius as unknown as Fahrenheit;
console.log(fahrenheit.unit); // "C" — still Celsius at runtime
```

## Key points

- The first cast widens to `unknown`, the supertype of every type.
- The second cast narrows from `unknown` to anything, so no overlap check runs.
- `as any as T` achieves the same bypass but leaks `any` into the expression.
- The value is never converted; only its compile-time type changes.
- Prefer `unknown` over `any` when a double cast is genuinely required.

## Gotchas

- Two direct, unrelated casts are rejected — which is why the intermediate step exists.

```ts
const n = "42" as string as number;
// ❌ Error: Conversion of type 'string' to type 'number' may be a mistake because neither type sufficiently overlaps with the other. (TS2352)
```

- Double assertions silence the exact warning that would catch a refactor.
- Runtime consumers still see the original shape, so methods may not exist.

## Best practice

- Treat `as unknown as` as a code smell to remove, not a convenience.
- Replace it with a type guard, a validator, or a corrected type definition.
