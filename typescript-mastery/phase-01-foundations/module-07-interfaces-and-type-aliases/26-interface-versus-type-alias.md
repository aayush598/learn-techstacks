# Interface versus Type Alias

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Both name object shapes, but interfaces extend and merge, while type aliases cover unions, primitives, and computed types.

## Syntax
```ts
interface UserInterface {
  id: string;
}

type UserAlias = {
  id: string;
};
```

## Examples
### Basic
```ts
// Equivalent object contracts
interface PointInterface {
  x: number;
  y: number;
}

type PointAlias = {
  x: number;
  y: number;
};

const a: PointInterface = { x: 1, y: 2 };
const b: PointAlias = { x: 1, y: 2 };
```

### Practical
```ts
interface Entity {
  id: string;
}

interface User extends Entity {
  name: string;
}

// Type-only capabilities: unions, primitives, tuples, mapped types.
type Status = "active" | "inactive";
type Pair = [number, number];
type Nullable<T> = { [K in keyof T]: T[K] | null };

type NullableUser = Nullable<User>;
const draft: NullableUser = { id: null, name: "Ada" };
```

### Advanced / edge cases
```ts
// Interfaces merge; aliases do not.
interface Config {
  env: string;
}
interface Config {
  debug: boolean;
}
const config: Config = { env: "dev", debug: true }; // ✅

// ❌ Error: Duplicate identifier 'Options'
// type Options = { a: string };
// type Options = { b: number };

// Interfaces can extend an object type alias.
type Base = { id: string };
interface User extends Base {
  name: string;
}

// An interface cannot extend a union alias.
type Shape = { kind: "circle" } | { kind: "square" };
// ❌ Error: An interface can only extend an object type
// interface Bad extends Shape {}
```

## Key points
- Both describe object shapes and are structurally checked.
- Interfaces support `extends`, `implements`, merging, and reopening.
- Type aliases support unions, intersections, primitives, tuples, and mapped types.
- Classes can implement either an interface or an object type alias.
- Interface names tend to produce clearer error messages.

## Gotchas
- `// ❌ Error:` redeclaring a type alias; only interfaces merge.
- `// ❌ Error:` extending a union type alias with an interface.
- Neither kind exists at runtime, so neither can be used with `instanceof`.

## Best practice
- Use interfaces for open, extendable object contracts.
- Use type aliases for everything interfaces cannot express.
- Pick one default per codebase and document the exceptions.
