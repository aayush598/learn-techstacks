# Assertion versus Narrowing

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Narrowing proves a type with runtime checks, while an assertion simply declares it.

## Syntax

```ts
if (typeof value === "string") {
  value.toUpperCase(); // narrowed
}

(value as string).toUpperCase(); // asserted
```

## Examples

### Basic

```ts
function describe(value: string | number): string {
  if (typeof value === "string") {
    return value.toUpperCase(); // ✅ narrowed to string
  }
  return value.toFixed(2); // ✅ narrowed to number
}

console.log(describe(12.345)); // "12.35"
```

### Practical

```ts
function unsafeLength(value: string | number): number {
  // ❌ Asserts string without checking; wrong for numbers.
  return (value as string).length;
}

function safeLength(value: string | number): number {
  return typeof value === "string" ? value.length : String(value).length;
}

console.log(unsafeLength(42)); // undefined at runtime
console.log(safeLength(42)); // 2
```

### Advanced / edge cases

```ts
type User = { kind: "user"; name: string };
type Admin = { kind: "admin"; permissions: string[] };
type Account = User | Admin;

// A user-defined guard narrows through a reusable check.
function isAdmin(account: Account): account is Admin {
  return account.kind === "admin";
}

function show(account: Account): string {
  if (isAdmin(account)) {
    return account.permissions.join(", "); // ✅ narrowed
  }
  return account.name; // ✅ narrowed
}

console.log(show({ kind: "admin", permissions: ["read"] })); // "read"
```

## Key points

- Narrowing is control-flow analysis driven by actual runtime checks.
- Assertions are erased and do not influence control-flow narrowing.
- Guards (`typeof`, `in`, `instanceof`, discriminated unions) compose well.
- User-defined type guards return `value is Type` and narrow at call sites.
- Assertions should be used only where a runtime check is impossible or already guaranteed.

## Gotchas

- Assertions can disable safety that narrowing would have provided.

```ts
const value: string | number = 42;
const text = (value as string).toUpperCase();
// compiles, but throws at runtime: value.toUpperCase is not a function
```

- Narrowing can be invalidated by reassignment or by mutation inside a closure.

```ts
function maybe(value: string | null): string {
  if (value === null) return "";
  value = null; // reassignment after narrowing
  return value.toUpperCase();
  // ❌ Error: 'value' is possibly 'null'. (TS18047)
}
```

- A type predicate that is not backed by a real check is just an assertion in disguise.

## Best practice

- Prefer narrow types and guards over casts so the compiler keeps tracking the value.
- Use assertions only when a check has already happened outside the current expression.
