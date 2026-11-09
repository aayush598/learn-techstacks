# undefined

> Phase 1 · Module 03 · Basic Types

**TL;DR** — `undefined` means a value was never set or is missing, and it is separate from `null` under `strict`.

## Syntax
```ts
let value: undefined = undefined;
let maybe: string | undefined;

function greet(name?: string): string {
  return `Hello, ${name ?? "stranger"}`;
}
```

## Examples
### Basic
```ts
let pending: string | undefined;
console.log(pending); // undefined

pending = "done"; // ✅
pending = undefined; // ✅
```

### Practical
```ts
type Config = { host: string; port?: number };

function baseUrl(config: Config): string {
  const port = config.port ?? 80;
  return `http://${config.host}:${port}`;
}

console.log(baseUrl({ host: "localhost" })); // http://localhost:80
console.log(baseUrl({ host: "localhost", port: 3000 })); // ✅
```

### Advanced / edge cases
```ts
// Optional properties and parameters are `T | undefined`
function greet(name?: string): string {
  return `Hello, ${name ?? "stranger"}`;
}

// A missing property and an explicit undefined are both undefined
const obj: { a?: number } = { a: undefined };
console.log(obj.a, greet(), greet("Ada"));

// void-returning functions produce undefined at runtime
const result: void = (() => {})();
console.log(result);
```

## Key points
- Uninitialized `let` variables and missing object keys are `undefined`.
- Optional properties and parameters implicitly include `undefined`.
- `undefined` is falsy but not the same as `null`.
- `??` falls back for both `undefined` and `null`.
- Functions without a `return` return `undefined`.

## Gotchas
- `strictNullChecks` blocks implicit undefined usage.
  ```ts
  // ❌ Error: Variable 'x' is used before being assigned.
  let x: number;
  // console.log(x + 1);
  ```
- Destructuring a missing key yields `undefined`.
  ```ts
  const { missing }: { missing?: number } = {};
  // ❌ Error: 'missing' is possibly 'undefined'.
  // console.log(missing.toFixed());
  ```
- `undefined` is not valid JSON and is dropped.
  ```ts
  console.log(JSON.stringify([undefined])); // [null]
  ```

## Best practice
- Use optional `?` for genuinely optional data instead of `| undefined` everywhere.
- Default with `??`, not `||`, so `0` and `""` survive.
