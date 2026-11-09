# Choosing Between Interface and Type

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Choose an interface for public object contracts that may be extended or merged, and a type alias for unions, functions, tuples, and computed types.

## Syntax
```ts
// Object contract
interface User {
  id: string;
}

// Any other type expression
type UserStatus = "active" | "invited" | "disabled";
type UserHandler = (user: User) => void;
```

## Examples
### Basic
```ts
// ✅ Public object contract: interface
export interface User {
  readonly id: string;
  name: string;
  email: string;
}

// ✅ Finite states: type alias
export type UserStatus = "active" | "invited" | "disabled";

// ✅ Callback: type alias
export type UserHandler = (user: User) => void;
```

### Practical
```ts
interface BaseEntity {
  readonly id: string;
  readonly createdAt: Date;
}

interface User extends BaseEntity {
  name: string;
  role: "admin" | "member";
}

// Derived state is a union, so it must be a type alias.
type LoadState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "loaded"; user: User }
  | { status: "failed"; error: string };

function label(state: LoadState): string {
  switch (state.status) {
    case "idle":
      return "Not loaded";
    case "loading":
      return "Loading";
    case "loaded":
      return state.user.name;
    case "failed":
      return state.error;
  }
}
```

### Advanced / edge cases
```ts
interface User {
  id: string;
  name: string;
}

// Computed types require an alias.
type PublicUser = Omit<User, "id"> & { readonly id: string };
type UserPatch = Partial<Pick<User, "name">>;
type UserKeys = keyof User;

// An interface can extend an object alias, but not a union alias.
type Audited = { updatedAt: Date };
interface AuditedUser extends User, Audited {
  updatedAt: Date;
}

// Validate a value against a contract without widening it.
interface AppConfig {
  readonly port: number;
  readonly debug: boolean;
}

const config = {
  port: 3000,
  debug: false,
} satisfies AppConfig; // ✅ checked, keeps literal types
```

## Key points
- Default to `interface` for exported object contracts.
- Use `type` when a union, tuple, primitive, or mapped type is involved.
- Use `type` for function signatures reused as callbacks.
- Both work for object shapes; consistency matters more than dogma.
- `satisfies` validates a value without changing its inferred type.

## Gotchas
- `// ❌ Error:` `interface Status extends ("on" | "off") {}` — interfaces cannot extend unions.
- `// ❌ Error:` trying to merge two aliases when an interface was needed.
- Mixing conventions in one module makes the public surface harder to learn.

## Best practice
- Write down a one-line rule for your team and apply it consistently.
- Refactor to an interface only when extension or merging is actually required.
