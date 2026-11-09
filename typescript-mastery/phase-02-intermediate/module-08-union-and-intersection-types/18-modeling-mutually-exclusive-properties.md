# Modeling Mutually Exclusive Properties

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Model "exactly one of these" with union variants, optionally using `never` to forbid the other property.

## Syntax
```ts
type Credentials =
  | { apiKey: string; token?: never }
  | { token: string; apiKey?: never };
```

## Examples
### Basic
```ts
type Payment =
  | { method: "card"; cardNumber: string; iban?: never }
  | { method: "bank"; iban: string; cardNumber?: never };

const card: Payment = { method: "card", cardNumber: "4242" };
const bank: Payment = { method: "bank", iban: "DE89370400440532013000" };

// ✅ each value uses exactly one payment method
console.log(card, bank);
```

### Practical
```ts
type Credentials =
  | { apiKey: string; token?: never }
  | { token: string; apiKey?: never };

function authenticate(credentials: Credentials): string {
  if ("apiKey" in credentials) {
    return `key:${credentials.apiKey}`; // ✅ narrowed
  }
  return `token:${credentials.token}`;
}

console.log(authenticate({ apiKey: "sk_live_123" }));
console.log(authenticate({ token: "jwt_abc" }));
```

### Advanced / edge cases
```ts
type Contact =
  | { email: string; phone?: never; handle?: never }
  | { phone: string; email?: never; handle?: never }
  | { handle: string; email?: never; phone?: never };

const byEmail: Contact = { email: "ada@example.com" }; // ✅
const byPhone: Contact = { phone: "+15551234" }; // ✅

// ✅ optional never forbids the other properties
// ❌ Error: Type 'string' is not assignable to type 'undefined'.
const both: Contact = { email: "ada@example.com", phone: "+15551234" };
```

## Key points
- Union variants express exclusivity that optional properties cannot.
- `other?: never` forbids a property while keeping the object literal ergonomic.
- Narrow with a discriminant or the `in` operator.
- Three or more exclusive options scale with more variants.
- `never` optional properties are absent at runtime, not `undefined` by contract.

## Gotchas
- Optional properties alone allow neither option and both options.
- Excess property checks only catch fresh object literals, not variables.

```ts
type Loose = { cardNumber?: string; iban?: string };

const empty: Loose = {}; // ✅ compiles, but has no payment method
const both: Loose = { cardNumber: "4242", iban: "DE00" }; // ✅ compiles, ambiguous

console.log(empty, both);
```

## Best practice
- Prefer explicit variants with a discriminant over `never` tricks for readability.
- Use `?: never` when callers construct literals and ergonomics matter.
