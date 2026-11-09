# Declaring Interfaces

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Declare an interface with the `interface` keyword, a PascalCase name, and a body of members separated by semicolons or commas.

## Syntax
```ts
export interface Account {
  readonly id: string;
  email: string;
  displayName?: string;
  deactivate(reason: string): void;
}
```

## Examples
### Basic
```ts
interface Point {
  x: number;
  y: number;
}

const origin: Point = { x: 0, y: 0 };
```

### Practical
```ts
export interface Account {
  readonly id: string;
  email: string;
  displayName?: string;
  isActive: boolean;
  deactivate(reason: string): void;
}

export function deactivate(account: Account): Account {
  account.deactivate("requested");
  return account;
}
```

### Advanced / edge cases
```ts
interface ApiResponse<T> {
  data: T;
  meta: {
    requestId: string;
    cached: boolean;
  };
}

interface Job {
  id: string;
  // Commas are legal separators too, but stay consistent.
  status: "queued" | "running" | "done",
  onDone?: () => void;
}

const response: ApiResponse<Job[]> = {
  data: [{ id: "j1", status: "queued" }],
  meta: { requestId: "req-1", cached: false },
};
```

## Key points
- Members can end with `;`, `,`, or a newline; pick one style.
- `export interface` makes the type available to importers.
- Interfaces can be generic and can extend other interfaces.
- Method syntax and property-function syntax are interchangeable in practice.
- Declarations are hoisted within their scope.

## Gotchas
- `// ❌ Error:` `interface Point { x: number; x: string; }` — duplicate members must have identical types.
- An interface cannot declare a union: `// ❌ Error: interface Status = "on" | "off";`
- A body is required; `interface Empty;` is invalid. Use `interface Empty {}`.

## Best practice
- Export interfaces that form part of a module's public contract.
- Keep declarations close to the code that consumes them unless shared widely.
