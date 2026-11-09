# Object Type Composition

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Build complex object types from small pieces using intersections, unions, utility types, and generics.

## Syntax
```ts
type Base = { id: string; name: string };
type Extra = { active: boolean };
type Composed = Base & Extra;
type Picked = Pick<Base, "id">;
type Partialized = Partial<Omit<Base, "id">>;
```

## Examples
### Basic
```ts
type Timestamps = { createdAt: Date; updatedAt: Date };
type SoftDelete = { deletedAt: Date | null };
type Entity = { id: string } & Timestamps & SoftDelete;

const entity: Entity = {
  id: "u1",
  createdAt: new Date(),
  updatedAt: new Date(),
  deletedAt: null,
};

console.log(entity.id);
```

### Practical
```ts
type User = { id: string; name: string; email: string; age: number };

type UserPreview = Pick<User, "id" | "name">;
type UserUpdate = Partial<Omit<User, "id">>;

const preview: UserPreview = { id: "u1", name: "Ada" };
const update: UserUpdate = { name: "Grace" };

console.log(preview, update);
```

### Advanced / edge cases
```ts
type WithId<T> = T & { id: string };
type Nullable<T> = { [K in keyof T]: T[K] | null };

type BaseUser = { name: string; email: string };
type DbUser = WithId<BaseUser>;
type FormUser = Nullable<BaseUser>;

const dbUser: DbUser = { id: "u1", name: "Ada", email: "ada@example.com" };
const formUser: FormUser = { name: "Ada", email: null };

console.log(dbUser.id, formUser.email);
```

## Key points
- Compose small named types instead of writing one large literal.
- Intersections add capabilities; unions express alternatives.
- `Pick`, `Omit`, `Partial`, and `Required` transform existing shapes.
- Generic wrappers compose metadata or modifiers onto any base type.
- Mapped types apply a transformation to every property.

## Gotchas
- `Omit` is not exact: the result may still be assignable from objects with extra properties.
- Conflicting intersections produce `never` for the conflicting property.
- Deep composition usually needs explicit recursive types; utility types are shallow.

## Best practice
- Keep base types focused and compose at the edges where contracts differ.
- Prefer `Pick`/`Omit` over re-declaring fields that already exist elsewhere.
