# Interface Reopening

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An interface can be reopened by declaring it again later, adding members to the same type across blocks or files.

## Syntax
```ts
interface Registry {
  user: string;
}

// Later, same scope
interface Registry {
  order: string;
}
```

## Examples
### Basic
```ts
interface Registry {
  user: string;
}

interface Registry {
  order: string;
}

const registry: Registry = { user: "users", order: "orders" }; // ✅
```

### Practical
```ts
// theme.ts
export interface Theme {
  colors: {
    primary: string;
  };
}

// brand.ts
import type { Theme } from "./theme";

declare module "./theme" {
  interface Theme {
    logo: string;
  }
}

// Consumers of Theme now see colors and logo.
```

### Advanced / edge cases
```ts
// Generic parameters must match exactly across reopenings.
interface Store<T> {
  get(): T;
}

interface Store<T> {
  set(value: T): void;
}

declare const store: Store<number>;
store.set(1);
const value: number = store.get();

// ❌ Error: All declarations of 'Store' must have identical type parameters
// interface Store<U> {
//   clear(): void;
// }
```

## Key points
- Reopening is declaration merging applied over time or across files.
- Every reopening contributes required members to the final type.
- Generic interfaces must repeat the same type parameter list.
- Cross-file reopening requires module augmentation.
- Reopening is useful for plugin and theme registries.

## Gotchas
- `// ❌ Error:` reopening with a different type parameter name or count.
- A type alias cannot be reopened; only interfaces merge.
- Adding a required member later can break existing object literals.

## Best practice
- Reserve reopening for deliberately extensible contracts.
- Prefer adding optional members when consumers may not supply them yet.
