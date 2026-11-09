# Unsafe Type Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — An assertion is unsafe when it claims a type the runtime value may not have, turning a compile error into a production failure.

## Syntax

```ts
const trusted = untrustedValue as TrustedType; // unverified
```

## Examples

### Basic

```ts
type User = { name: string };

const json = '{"name":123}';
const user = JSON.parse(json) as User;

console.log(user.name.toUpperCase());
// compiles, throws at runtime: user.name.toUpperCase is not a function
```

### Practical

```ts
const button = document.querySelector("#save");

button?.addEventListener("click", (event) => {
  const target = event.target as HTMLButtonElement;
  target.disabled = true; // unsafe: target may be a child node or null
});
```

A safer version checks the runtime type:

```ts
button?.addEventListener("click", (event) => {
  if (event.target instanceof HTMLButtonElement) {
    event.target.disabled = true; // ✅ narrowed
  }
});
```

### Advanced / edge cases

```ts
type Draft = { id: number };
type Published = { id: string };

const draft: Draft = { id: 1 };
const published = draft as unknown as Published;

// No compiler error, but the representation is wrong.
console.log(typeof published.id); // "number"
```

## Key points

- Unsafe assertions bypass the compiler's overlap and compatibility checks.
- Common sources: `JSON.parse`, DOM queries, event targets, `postMessage`, env vars.
- `as any` is the most dangerous form because it disables checks downstream.
- Unsafe casts hide regressions when a type or API changes.
- An assertion is only as safe as the invariant you can prove about the value.

## Gotchas

- Casting an event target is a frequent source of `null` and wrong-element bugs.
- Chained `as any as` casts can make an entire expression unchecked.
- Casting a partial object to a full interface leaves missing fields as `undefined`.

```ts
interface Account { id: number; email: string }
const partial = { id: 1 } as Account;
console.log(partial.email.toLowerCase());
// throws at runtime: Cannot read properties of undefined (reading 'toLowerCase')
```

## Best practice

- Replace unsafe assertions with validation, guards, or corrected types.
- If a cast is unavoidable, keep it at the smallest possible scope and add a comment.
