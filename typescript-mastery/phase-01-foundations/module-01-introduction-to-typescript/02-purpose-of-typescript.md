# Purpose of TypeScript

> Phase 1 · Module 01 · Introduction to TypeScript

**TL;DR** — TypeScript catches likely mistakes before execution, documents intent in code, and gives editors enough information to assist safely.

## Syntax

```ts
function repeat(text: string, times: number): string {
  return text.repeat(times);
}
```

## Examples

### Basic

```ts
function area(width: number, height: number): number {
  return width * height;
}

const result: number = area(3, 4); // => 12
```

### Practical

```ts
type ApiResponse =
  | { status: "ok"; data: string[] }
  | { status: "error"; message: string };

function render(response: ApiResponse): string {
  return response.status === "ok"
    ? response.data.join(", ")
    : `Error: ${response.message}`;
}
```

### Advanced / edge cases

```ts
type Cents = number & { readonly __brand: unique symbol };

function cents(value: number): Cents {
  if (!Number.isInteger(value) || value < 0) {
    throw new RangeError("Cents must be a non-negative integer");
  }
  return value as Cents;
}

function charge(amount: Cents): void {
  console.log(`Charging ${amount}`);
}

charge(cents(500)); // ✅
// ❌ Error: Argument of type 'number' is not assignable to parameter of type 'Cents'. (TS2345)
charge(500);
```

## Key points

- Moves many type errors from production into the editor and CI.
- Serves as executable documentation for function contracts and data shapes.
- Enables reliable refactors through rename, go-to-definition, and find-references.
- Improves autocomplete and API discovery in editors.
- Supports gradual adoption: JavaScript and TypeScript can coexist.

## Gotchas

- Types disappear at runtime, so they cannot replace tests or input validation.
- `any` and unchecked assertions silently discard the safety you are paying for.
- Types describe what the compiler believes, not what the network actually sends.

## Best practice

- Spend type effort at module boundaries and public APIs where mistakes are expensive.
- Pair static types with runtime validation for external data.
