# Object Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An object type alias names an object shape with `type Name = { ... }`, supporting optional, readonly, and method members.

## Syntax
```ts
type User = {
  id: string;
  email?: string;
  readonly createdAt: Date;
  greet(message: string): string;
};
```

## Examples
### Basic
```ts
type Point = {
  x: number;
  y: number;
};

const origin: Point = { x: 0, y: 0 };
```

### Practical
```ts
type User = {
  readonly id: string;
  name: string;
  email?: string;
};

type UserWithEmail = User & { email: string };

function sendWelcome(user: UserWithEmail): void {
  console.log(`Welcome ${user.name} <${user.email}>`);
}

const user: UserWithEmail = { id: "u1", name: "Ada", email: "ada@example.com" };
sendWelcome(user);
```

### Advanced / edge cases
```ts
type Point = {
  x: number;
  y: number;
};

type Dictionary = {
  [key: string]: string;
};

type Callable = {
  (value: number): string;
  readonly label: string;
};

const format: Callable = Object.assign(
  (value: number) => value.toFixed(2),
  { label: "fixed" }
);

// Mapped types are only expressible with aliases.
type Nullable<T> = { [K in keyof T]: T[K] | null };

type NullablePoint = Nullable<Point>;
const point: NullablePoint = { x: null, y: 2 };

// Class can implement an object type alias.
class Origin implements Point {
  x = 0;
  y = 0;
}
```

## Key points
- Object aliases describe structural shapes, same as interfaces.
- They can include optional, readonly, index, call, and construct signatures.
- Mapped and conditional types are available on the right-hand side.
- Classes can implement an object type alias.
- Aliases cannot be declaration-merged.

## Gotchas
- `// ❌ Error:` `type Point = { x: number }; type Point = { y: number };` — no merging.
- Object literal excess-property checks still apply.
- Intersecting object aliases with conflicting members yields `never` for that member.

## Best practice
- Use object aliases for computed shapes (mapped, conditional, unions).
- Use interfaces for plain, extendable object contracts.
