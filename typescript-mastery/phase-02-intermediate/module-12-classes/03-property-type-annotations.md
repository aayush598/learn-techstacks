# Property type annotations

> Phase 2 · Module 12 · Classes

**TL;DR** — Annotate property types when inference widens too much or the value is assigned later, and let inference handle obvious defaults.

## Syntax
```ts
class C {
  id: string;
  status: "idle" | "busy" = "idle";
  items: string[] = [];
}
```

## Examples
### Basic
```ts
class Account {
  id: string;
  balance: number = 0;
  tags: string[] = [];

  constructor(id: string) {
    this.id = id;
  }
}
```

### Practical
```ts
type Role = "admin" | "member" | "guest";

class Session {
  readonly user: string;
  role: Role = "guest";
  expiresAt: Date | null = null;

  constructor(user: string) {
    this.user = user;
  }

  promote(role: Role): void {
    this.role = role; // ✅ only valid Role values
  }
}

const session = new Session("ada");
// ❌ Error: Type '"root"' is not assignable to type 'Role'.
// session.promote("root");
```

### Advanced / edge cases
```ts
class Mutable {
  status = "idle"; // inferred string (widened)
}

class Immutable {
  readonly status = "idle"; // inferred "idle" (literal)
}

const m = new Mutable();
m.status = "busy"; // ✅ string
const i = new Immutable();
i.status = "busy"; // ❌ Error: Cannot assign to 'status' because it is a read-only property.

class Safe {
  data: unknown = null; // ✅ forces narrowing before use
}

class Unsafe {
  data: any = null; // ❌ disables type checking
}
```

## Key points
- Mutable properties infer widened types such as `string` from literal initializers.
- `readonly` properties preserve literal types from their initializers.
- Optional properties (`?`) add `undefined` to the declared type.
- Explicit annotations document the intended contract regardless of initial value.
- `unknown` is the safe annotation for data of uncertain shape.

## Gotchas
- Forgetting an annotation on a mutable field often widens a literal union to `string`.
- Annotating as `any` erases safety for every read and write of the field.
- Assigning `null` requires the property type to include `null` under `strictNullChecks`.

## Best practice
- Annotate public fields that form part of the class API; let trivial private defaults infer.
- Use literal unions and `readonly` instead of broad `string` when values are constrained.
