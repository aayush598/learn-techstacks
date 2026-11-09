# Combining Object Properties

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Intersections merge object properties into one shape, matching how object spread combines them at runtime.

## Syntax
```ts
type Combined = { a: A } & { b: B };
```

## Examples
### Basic
```ts
type Identifiable = { id: string };
type Timestamped = { createdAt: Date };

type Entity = Identifiable & Timestamped;

// ✅ both property groups are required
const entity: Entity = { id: "e_1", createdAt: new Date() };
console.log(entity);
```

### Practical
```ts
type BaseConfig = { host: string; port: number };
type AuthConfig = { token: string };

type ClientConfig = BaseConfig & AuthConfig;

function createClient(config: ClientConfig): ClientConfig {
  return { ...config };
}

// ✅ spread preserves the combined shape
const client = createClient({
  host: "api.example.com",
  port: 443,
  token: "secret",
});
console.log(client.host);
```

### Advanced / edge cases
```ts
type WithMeta<T> = T & { meta: { version: number } };

function withMeta<T extends object>(value: T): WithMeta<T> {
  return { ...value, meta: { version: 1 } };
}

const doc = withMeta({ title: "Guide", published: true });
// ✅ inferred as { title: string; published: boolean } & { meta: ... }
console.log(doc.title, doc.meta.version);

// Optional properties combine predictably.
type MaybeName = { name?: string };
type MaybeEmail = { email?: string };
type Contact = MaybeName & MaybeEmail;

const contact: Contact = { name: "Ada" }; // ✅ email stays optional
```

## Key points
- Intersections concatenate property sets; duplicate keys must stay compatible.
- Object spread is the natural runtime counterpart to an intersection type.
- Generic intersections preserve the original type parameter.
- Optional properties remain optional after merging.
- Order of members does not change the resulting type.

## Gotchas
- Runtime spread can silently overwrite a key that the type says is compatible.
- Intersecting two different types for the same key yields `never`.

```ts
type A = { status: "draft" };
type B = { status: "published" };
type Post = A & B;

// ❌ Error: Type '"draft"' is not assignable to type 'never'.
const post: Post = { status: "draft" };
```

## Best practice
- Keep shared keys identical across intersected members.
- Build small property-group aliases and compose them instead of one large type.
