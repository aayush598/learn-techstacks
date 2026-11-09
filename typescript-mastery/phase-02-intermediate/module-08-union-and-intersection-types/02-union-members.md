# Union Members

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Each type inside a union is a member, and every value must match at least one member.

## Syntax
```ts
type Result = MemberA | MemberB;
```

## Examples
### Basic
```ts
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";

// ✅ four literal members, one value
const method: HttpMethod = "POST";
```

### Practical
```ts
type Metric = number | "unknown" | null;

function formatMetric(value: Metric): string {
  if (value === null) return "n/a";
  if (value === "unknown") return "?";
  return value.toFixed(1);
}

// ✅ each member is handled explicitly
console.log(formatMetric(12.34)); // "12.3"
console.log(formatMetric("unknown")); // "?"
console.log(formatMetric(null)); // "n/a"
```

### Advanced / edge cases
```ts
type Primitive = string | number | boolean | bigint | symbol | null | undefined;

// Duplicate members collapse; order does not affect assignability.
type Duplicated = string | string | number;
const value: Duplicated = 10; // ✅ still string | number

// never disappears from a union.
type WithNever = string | never;
const text: WithNever = "ok"; // ✅ equivalent to string

// unknown absorbs every other member.
type WithUnknown = string | unknown;
const anything: WithUnknown = { id: 1 }; // ✅ equivalent to unknown
```

## Key points
- A union has two or more members; each member is a complete type.
- Duplicate members are removed automatically.
- `never` contributes nothing to a union.
- `unknown` absorbs all other members.
- Member order is irrelevant to the type checker.

## Gotchas
- `any` in a union swallows the whole union and disables checking.
- Nested unions are flattened: `(A | B) | C` is `A | B | C`.

```ts
type Bad = string | any;

// ❌ No type error here, because the union collapsed to any.
const value: Bad = { not: "a string" };
value.missing.deeply; // also unchecked
```

## Best practice
- Prefer explicit literal members over broad primitives when the set is closed.
- Avoid `any` as a member; use `unknown` and narrow instead.
