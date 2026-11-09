# Avoiding Ambiguous Unions

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Ambiguous unions have overlapping shapes or weak members, so the compiler cannot tell variants apart reliably.

## Syntax
```ts
type Ambiguous = { id: string } | { id: string; name: string };
```

## Examples
### Basic
```ts
type A = { id: string };
type B = { id: string; name: string };
type Ambiguous = A | B;

declare const value: Ambiguous;

// ❌ Error: Property 'name' does not exist on type 'A | B'.
console.log(value.name);
```

### Practical
```ts
type Event =
  | { type: "created"; id: string }
  | { type: "updated"; id: string; fields: string[] };

function handle(event: Event): string {
  // ✅ the discriminant makes the variant unambiguous
  return event.type === "updated"
    ? `${event.id}: ${event.fields.join(", ")}`
    : event.id;
}

console.log(handle({ type: "updated", id: "e_1", fields: ["title"] }));
```

### Advanced / edge cases
```ts
type Weak = { email?: string } | { phone?: string };

// ✅ all-optional members accept an empty object
const empty: Weak = {};

// ❌ Error: Type '{ role: string; }' has no properties in common with type 'Weak'.
const unrelated: Weak = { role: "admin" };

// Fix: give every variant a required discriminant.
type Strong =
  | { kind: "email"; email: string }
  | { kind: "phone"; phone: string };

const strong: Strong = { kind: "email", email: "ada@example.com" }; // ✅
```

## Key points
- Overlapping object shapes hide variant-specific properties.
- A supertype member absorbs narrower members for reads.
- All-optional unions trigger weak type detection.
- A required literal discriminant removes ambiguity.
- Prefer distinct tags over structural guesswork.

## Gotchas
- Excess property checks catch some mistakes only for fresh literals.
- A union of `{ id: string }` and `{ id: string; name: string }` is effectively `{ id: string }`.

```ts
type A = { id: string };
type B = { id: string; name: string };
type U = A | B;

const b: B = { id: "1", name: "Ada" };
const u: U = b; // ✅ allowed, then name is no longer accessible

// ❌ Error: Property 'name' does not exist on type 'A | B'.
console.log(u.name);
```

## Best practice
- Add a required literal discriminant whenever variants overlap.
- Avoid unions made entirely of optional-property objects.
