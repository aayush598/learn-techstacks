# Function Union Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — A union of function types means the value is one of several callable signatures, and calls must satisfy every possible parameter type.

## Syntax
```ts
type Callback = ((a: A) => R1) | ((b: B) => R2);
```

## Examples
### Basic
```ts
type StringFormatter = (value: string) => string;
type NumberFormatter = (value: number) => string;

type Formatter = StringFormatter | NumberFormatter;

const upper: Formatter = (value: string) => value.toUpperCase();
const fixed: Formatter = (value: number) => value.toFixed(2);

// ✅ each assignment matches one signature
console.log(upper("ok"), fixed(1.5));
```

### Practical
```ts
type NumberCallback = { kind: "number"; fn: (value: number) => void };
type DateCallback = { kind: "date"; fn: (value: Date) => void };

type Callback = NumberCallback | DateCallback;

function invoke(callback: Callback, value: number | Date): void {
  if (callback.kind === "number" && typeof value === "number") {
    callback.fn(value);
  } else if (callback.kind === "date" && value instanceof Date) {
    callback.fn(value);
  }
}

// ✅ pair the discriminant with a matching runtime value
invoke({ kind: "number", fn: (n) => console.log(n + 1) }, 41);
invoke({ kind: "date", fn: (d) => console.log(d.toISOString()) }, new Date());
```

### Advanced / edge cases
```ts
type StringFn = (value: string) => string;
type NumberFn = (value: number) => number;
type MixedFn = StringFn | NumberFn;

declare const mixed: MixedFn;

// The parameter type becomes string & number, which is never.
// ❌ Error: Argument of type 'string' is not assignable to parameter of type 'never'.
mixed("hello");

type SharedParamA = (value: string) => string;
type SharedParamB = (value: string) => number;
type SharedParam = SharedParamA | SharedParamB;

declare const shared: SharedParam;
const output = shared("ok"); // ✅ string | number
```

## Key points
- Calling a function union requires arguments valid for **all** members.
- Parameter types intersect; return types union.
- If parameter types are disjoint, the callable parameter becomes `never`.
- Discriminated wrappers make mixed callbacks safe and ergonomic.
- Overloads are often a better fit than raw function unions.

## Gotchas
- A union of functions with incompatible parameters is practically uncallable.
- Narrowing a bare function value by `typeof` does not select a signature.

```ts
type A = (value: { a: number }) => void;
type B = (value: { b: string }) => void;
declare const fn: A | B;

// ❌ Error: Argument of type '{ a: number; }' is not assignable to parameter of type '{ a: number; } & { b: string; }'.
fn({ a: 1 });
```

## Best practice
- Wrap heterogeneous callbacks in discriminated objects instead of a bare function union.
- Prefer function overloads when one function must accept several signatures.
