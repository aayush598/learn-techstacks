# Function Compatibility

> Phase 1 · Module 05 · Functions

**TL;DR** — Functions are assignable when parameters are compatible in reverse and returns are compatible forward.

## Syntax
```ts
let target: (a: A) => R;
let source: (b: B) => S;
// assignable when A is assignable to B and S is assignable to R
```

## Examples
### Basic
```ts
type NumToNum = (n: number) => number;

const square: NumToNum = (n) => n * n;

// ✅ identical shapes are interchangeable
const alias: NumToNum = square;
console.log(alias(3)); // 9
```

### Practical
```ts
type Handler = (event: { type: string }) => void;

const log: Handler = (e) => console.log(e.type);

// ✅ a handler needing less can stand in for one that gets more
const detailed: (event: { type: string; time: number }) => void = log;

// ❌ Error: target may pass { type } without a `time`
// const h: Handler = (e: { type: string; time: number }) => {};
```

### Advanced / edge cases
```ts
// Fewer parameters are allowed
type Pair = (a: number, b: number) => number;
const one: Pair = (a) => a; // ✅ ignores the second argument

// Optional and rest parameters widen compatibility
type Args = (a: number, ...rest: string[]) => void;
const plain: Args = (a) => console.log(a);

// ✅ `void` targets accept any return
type Sink = (n: number) => void;
const double: Sink = (n) => n * 2;
```

## Key points
- Same-shape functions are mutually assignable (structural typing).
- A function may accept fewer parameters than its target.
- Parameter types are checked contravariantly (under `strictFunctionTypes` for function types).
- Return types are checked covariantly, with a `void` exception.

## Gotchas
- `// ❌ Error:` `const f: (a: number) => number = (a: number | string) => 1;` — target passes `number`, source may need `string`.
- Method parameters are bivariant, so some unsafe assignments slip through.
- Optionalized targets can reject sources requiring those parameters.

## Best practice
- Type against the narrowest parameter and widest return you actually need.
- Prefer function-type properties over methods when you want strict variance.
