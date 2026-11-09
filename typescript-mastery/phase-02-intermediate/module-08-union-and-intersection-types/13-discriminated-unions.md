# Discriminated Unions

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — A discriminated union is a union of object types sharing a literal property that tells the branches apart.

## Syntax
```ts
type Union =
  | { kind: "a"; /* fields */ }
  | { kind: "b"; /* fields */ };
```

## Examples
### Basic
```ts
type Circle = { kind: "circle"; radius: number };
type Square = { kind: "square"; side: number };

type Shape = Circle | Square;

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.side ** 2;
  }
}

console.log(area({ kind: "circle", radius: 2 }));
console.log(area({ kind: "square", side: 3 }));
```

### Practical
```ts
type Payment =
  | { method: "card"; last4: string; brand: string }
  | { method: "bank"; iban: string }
  | { method: "cash"; currency: string };

function describePayment(payment: Payment): string {
  switch (payment.method) {
    case "card":
      return `${payment.brand} ending ${payment.last4}`;
    case "bank":
      return `IBAN ${payment.iban.slice(-4)}`;
    case "cash":
      return `Cash in ${payment.currency}`;
  }
}

console.log(describePayment({ method: "card", last4: "4242", brand: "Visa" }));
```

### Advanced / edge cases
```ts
type Action =
  | { type: "add"; item: string }
  | { type: "remove"; index: number }
  | { type: "clear" };

type State = { items: string[] };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "add":
      return { items: [...state.items, action.item] };
    case "remove":
      return { items: state.items.filter((_, i) => i !== action.index) };
    case "clear":
      return { items: [] };
  }
}

// ✅ each case sees only its own payload
const next = reducer({ items: [] }, { type: "add", item: "milk" });
console.log(next);
```

## Key points
- Every member has the same discriminant key with a distinct literal type.
- The discriminant must be a literal, not a widened `string`.
- Narrowing works in `switch`, `if`, and ternaries.
- Payloads can differ completely between members.
- Exhaustive switches need no `default`.

## Gotchas
- A non-literal discriminant does not narrow the union.
- Forgetting a discriminant member breaks exhaustiveness checks.

```ts
type Bad = { kind: string; a: number } | { kind: string; b: number };
declare const bad: Bad;

// ❌ Error: Property 'a' does not exist on type 'Bad'.
if (bad.kind === "a") console.log(bad.a);
```

## Best practice
- Use a consistent discriminant name such as `kind`, `type`, or `status`.
- Keep the discriminant `readonly` so it cannot change at runtime.
