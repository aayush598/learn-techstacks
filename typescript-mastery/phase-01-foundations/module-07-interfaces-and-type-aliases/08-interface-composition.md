# Interface Composition

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Compose interfaces by making one interface a property of another, so small contracts combine without inheritance.

## Syntax
```ts
interface Address {
  city: string;
}

interface Customer {
  id: string;
  address: Address;
}
```

## Examples
### Basic
```ts
interface Address {
  street: string;
  city: string;
}

interface Contact {
  email: string;
  phone?: string;
}

interface Customer {
  id: string;
  address: Address;
  contact: Contact;
}

const customer: Customer = {
  id: "c1",
  address: { street: "1 Main St", city: "Springfield" },
  contact: { email: "c@example.com" },
};
```

### Practical
```ts
interface Money {
  amount: number;
  currency: "USD" | "EUR";
}

interface LineItem {
  sku: string;
  quantity: number;
  unitPrice: Money;
}

interface Order {
  id: string;
  items: LineItem[];
  total: Money;
}

function orderTotal(items: LineItem[]): Money {
  const amount = items.reduce((sum, item) => sum + item.unitPrice.amount * item.quantity, 0);
  return { amount, currency: "USD" };
}
```

### Advanced / edge cases
```ts
interface Customer {
  id: string;
}

const customer: Customer = { id: "c1" };

interface PageMeta {
  page: number;
  pageSize: number;
  total: number;
}

interface Page<T> {
  items: T[];
  meta: PageMeta;
}

interface WithAudit {
  createdBy: string;
  updatedBy: string;
}

// Composition can be nested arbitrarily deep.
interface AuditedPage<T> {
  page: Page<T>;
  audit: WithAudit;
}

const result: AuditedPage<Customer> = {
  page: { items: [customer], meta: { page: 1, pageSize: 20, total: 1 } },
  audit: { createdBy: "system", updatedBy: "system" },
};
```

## Key points
- Composition models `has-a` relationships.
- Each interface stays small and independently reusable.
- Nested objects are accessed through property paths.
- Composition avoids the fragility of deep inheritance chains.
- Generic containers compose cleanly with concrete element types.

## Gotchas
- `// ❌ Error:` `const c: Customer = { id: "c1", address: { city: "X" } };` — nested required members still apply.
- Composition is not the same as intersection; it adds a property level.
- Over-nesting makes access paths long; flatten when a level adds no meaning.

## Best practice
- Build small interfaces for address, money, audit, and pagination, then compose them.
- Prefer composition when types share data but not behavior.
