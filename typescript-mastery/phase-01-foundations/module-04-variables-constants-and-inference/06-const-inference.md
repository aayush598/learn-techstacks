# `const` Inference

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — `const` bindings infer the narrowest type of their initializer, preserving literal types.

## Syntax
```ts
const count = 0;            // 0
const label: string = "ready"; // string
```

## Examples
### Basic
```ts
const id = 42;         // 42
const label = "ready"; // "ready"
const ok = true;       // true

const user = { id: 42, label: "ready" }; // { id: number; label: string }
```

### Practical
```ts
type Status = "idle" | "loading" | "done";

const initialStatus = "idle"; // "idle"
const declared: Status = "idle"; // Status

function setStatus(next: Status): void {
  console.log(next);
}

setStatus(initialStatus); // ✅ literal fits the union

// setStatus("paused");    // ❌ Error: Argument of type '"paused"' is not assignable to parameter of type 'Status'.

const user = { id: 42, label: "ready" };
console.log(user.label);
```

### Advanced / edge cases
```ts
const tuple = [1, "two"];      // (string | number)[]
const fixed = [1, "two"] as const; // readonly [1, "two"]

const nested = {
  tags: ["a", "b"],
}; // { tags: string[] }

const exactNested = {
  tags: ["a", "b"],
} as const; // { readonly tags: readonly ["a", "b"] }

const fromFn = () => "done"; // () => string — return widened
const exactFn = () => "done" as const; // () => "done"

console.log(tuple, fixed, nested, exactNested, fromFn, exactFn);
```

## Key points
- `const` prevents reassignment, so literals need not widen.
- Objects declared with `const` still widen their properties.
- Arrays declared with `const` still widen their elements.
- `as const` extends literal inference to members and makes them `readonly`.
- `const` does not make the value deeply immutable by itself.

## Gotchas
- `const o = { n: 1 }; o.n = 2;` is legal — only the binding is constant.
- `const` arrays are mutable: `const xs = [1]; xs.push(2); // ✅`.
- `const` object properties widen, so `o.mode` is `string`, not `"dark"`.

## Best practice
- Use `const` by default for values that never reassign.
- Add `as const` when literal member types matter to consumers.
