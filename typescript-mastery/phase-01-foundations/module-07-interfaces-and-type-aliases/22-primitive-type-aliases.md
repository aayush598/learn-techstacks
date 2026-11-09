# Primitive Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A primitive type alias gives a meaningful name to a primitive, documenting intent without changing runtime behavior.

## Syntax
```ts
type UserId = string;
type Milliseconds = number;
```

## Examples
### Basic
```ts
type UserId = string;
type Milliseconds = number;
type IsActive = boolean;

const id: UserId = "u1";
const timeout: Milliseconds = 5_000;
const active: IsActive = true;
```

### Practical
```ts
type Email = string;
type Cents = number;

interface Invoice {
  id: string;
  customerEmail: Email;
  total: Cents;
}

function formatCents(value: Cents): string {
  return `$${(value / 100).toFixed(2)}`;
}

const invoice: Invoice = {
  id: "inv-1",
  customerEmail: "ada@example.com",
  total: 1999,
};

console.log(formatCents(invoice.total)); // "$19.99"
```

### Advanced / edge cases
```ts
// Plain aliases are structural, so they do not stop mixing.
type UserId = string;
type OrderId = string;

const userId: UserId = "u1";
const orderId: OrderId = userId; // ✅ allowed: both are just string

// Branded types add a compile-time identity.
type Brand<T, B extends string> = T & { readonly __brand: B };
type BrandedUserId = Brand<string, "UserId">;
type BrandedOrderId = Brand<string, "OrderId">;

function asUserId(value: string): BrandedUserId {
  return value as BrandedUserId;
}

const brandedUser = asUserId("u2");
// ❌ Error: Type 'BrandedUserId' is not assignable to type 'BrandedOrderId'
// const brandedOrder: BrandedOrderId = brandedUser;
```

## Key points
- Aliases improve readability and document units or meaning.
- They are erased and add no runtime checks.
- Structural typing makes plain aliases interchangeable.
- Branding with a unique property simulates nominal typing.
- Branding requires an explicit cast at the validation boundary.

## Gotchas
- `// ❌ Error:` expecting `type Age = number` to reject negative numbers.
- `type A = string` and `type B = string` are fully assignable to each other.
- Branded values are still plain strings at runtime; validate before casting.

## Best practice
- Alias units and identifiers (`Cents`, `Milliseconds`, `UserId`) for clarity.
- Use brands only where mixing identifiers would be a real bug.
