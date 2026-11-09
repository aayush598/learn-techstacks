# Type Assertion Limitations

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Assertions affect only the compile-time type and cannot validate data, add behavior, or survive type erasure.

## Syntax

```ts
const value = expression as Type; // compile-time only
```

## Examples

### Basic

```ts
const looksNumeric = "42" as unknown as number;

console.log(looksNumeric + 1); // "421" — string concatenation
console.log(typeof looksNumeric); // "string"
```

### Practical

```ts
interface User {
  name: string;
}

const data = {} as User;
console.log(data.name); // undefined — no property was created
console.log("name" in data); // false
```

### Advanced / edge cases

```ts
const service = {} as { run(): void };

// The type says `run` exists, but the object has no such method.
service.run();
// throws at runtime: TypeError: service.run is not a function

// Assertions cannot change the emitted JavaScript.
const badge = 123 as unknown as string;
console.log(badge.length); // undefined at runtime
```

## Key points

- Assertions are erased; emitted JavaScript keeps the original value.
- They do not create properties, methods, or prototype links.
- They do not validate structure, types, ranges, or nullability at runtime.
- They cannot be used to inspect or reflect on types at runtime.
- They cannot make a value satisfy a type it does not actually have.

## Gotchas

- A successful compile is not evidence that the value is correct.

```ts
const payload = JSON.parse("null") as { id: number };
console.log(payload.id);
// throws at runtime: Cannot read properties of null (reading 'id')
```

- Assertions do not add type metadata to the output bundle.
- Private-branded or nominal types cannot be asserted into existence meaningfully.

## Best practice

- Validate runtime data before treating it as a trusted type.
- Use assertions only to express facts already guaranteed by surrounding code.
