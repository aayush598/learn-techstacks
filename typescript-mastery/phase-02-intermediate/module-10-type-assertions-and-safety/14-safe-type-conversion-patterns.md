# Safe Type Conversion Patterns

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Convert values with explicit parsing and runtime checks instead of asserting them into a type.

## Syntax

```ts
const parsed = Number(input); // real conversion
const checked = isUser(value) ? value : null; // real validation
```

## Examples

### Basic

```ts
const count = Number("42"); // 42
const label = String(42); // "42"
const flag = Boolean(0); // false

console.log(count, label, flag);
```

### Practical

```ts
function toNumber(input: string): number | null {
  const value = Number(input);
  return Number.isFinite(value) ? value : null;
}

console.log(toNumber("42")); // 42
console.log(toNumber("abc")); // null
console.log(toNumber("")); // null — Number("") is 0, so guard whitespace too
```

### Advanced / edge cases

```ts
type User = { id: number; name: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isUser(value: unknown): value is User {
  if (!isRecord(value)) return false;
  return typeof value.id === "number" && typeof value.name === "string";
}

function parseUser(raw: string): User | null {
  const data: unknown = JSON.parse(raw);
  return isUser(data) ? data : null;
}

console.log(parseUser('{"id":1,"name":"Ada"}')); // { id: 1, name: "Ada" }
console.log(parseUser('{"id":"1"}')); // null
```

## Key points

- Use `Number`, `String`, and `Boolean` for actual runtime conversion.
- Prefer `Number.isFinite` over truthiness when validating numeric strings.
- Guard `JSON.parse` output as `unknown`, then narrow with predicates.
- Return `T | null` or a `Result` instead of asserting `T`.
- Type predicates centralize validation and make it reusable.

## Gotchas

- `Boolean("false")` is `true`; parse strings explicitly.

```ts
const enabled = Boolean("false"); // true — likely not intended
console.log(enabled);
```

- `Number("")` and `Number(" ")` are both `0`.
- `parseInt("12px", 10)` returns `12`, silently accepting partial input.

```ts
const width = parseInt("12px", 10); // 12 — no error for the trailing "px"
```

## Best practice

- Convert and validate at the boundary, then pass typed values inward.
- Return explicit failures (`null`, `Result`, or throws) rather than asserting success.
