# Modeling Complex Object Structures

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Combine naming, nesting, unions, intersections, generics, and index signatures to model real-world data safely.

## Syntax
```ts
type ApiResult<T> = { ok: true; data: T } | { ok: false; error: { code: string; message: string } };
type Config = { services: Record<string, { url: string }> };
```

## Examples
### Basic
```ts
type ApiResponse<T> =
  | { ok: true; data: T }
  | { ok: false; error: { code: string; message: string } };

type User = {
  id: string;
  name: string;
  roles: readonly string[];
  profile: {
    email: string;
    avatarUrl?: string;
  };
};

const response: ApiResponse<User> = {
  ok: true,
  data: {
    id: "u1",
    name: "Ada",
    roles: ["admin"],
    profile: { email: "ada@example.com" },
  },
};

if (response.ok) {
  console.log(response.data.name);
}
```

### Practical
```ts
type Environment = "development" | "staging" | "production";

type ServiceConfig = {
  url: string;
  timeoutMs: number;
  retries?: number;
};

type AppConfig = {
  environment: Environment;
  services: Record<string, ServiceConfig>;
  features: Partial<Record<"billing" | "search", boolean>>;
  readonly version: string;
};

const config: AppConfig = {
  environment: "production",
  services: {
    auth: { url: "https://auth.example.com", timeoutMs: 3000 },
    mail: { url: "https://mail.example.com", timeoutMs: 5000, retries: 2 },
  },
  features: { billing: true },
  version: "1.0.0",
};

console.log(config.services.auth.url, config.features.search ?? false);
```

### Advanced / edge cases
```ts
type DeepPartial<T> = T extends readonly unknown[]
  ? T
  : T extends object
    ? { [K in keyof T]?: DeepPartial<T[K]> }
    : T;

type Entity<TId extends string | number> = {
  id: TId;
  createdAt: Date;
};

type User = Entity<string> & {
  name: string;
  tags: readonly string[];
};

type UserPatch = DeepPartial<Omit<User, "id" | "createdAt">>;

const patch: UserPatch = { name: "Grace", tags: ["admin"] };

type Repository<T extends { id: string | number }> = {
  get(id: T["id"]): T | undefined;
  save(value: T): void;
};

const users: Repository<User> = {
  get(id) {
    return id === "u1"
      ? { id: "u1", createdAt: new Date(), name: "Ada", tags: [] }
      : undefined;
  },
  save(value) {
    console.log(value.id);
  },
};

users.save({ id: "u1", createdAt: new Date(), name: "Ada", tags: [] });
console.log(patch);
```

## Key points
- Start with small named types for each concept, then compose outward.
- Use discriminated unions for results and variant-specific data.
- Use `Record` and index signatures for dynamic key spaces.
- Use generics to reuse a structure across payload types.
- Keep read-only and optional modifiers at the level where they apply.

## Gotchas
- Deep recursive types need guards for arrays and built-ins; naive recursion can be expensive or wrong.
- `// ❌ Error:` widening a generic constraint too far causes property access errors inside the implementation.
- Excess properties and index signatures can silently admit data you did not model.

## Best practice
- Model external data at the boundary, validate it at runtime, then pass narrower domain types inward.
- Prefer many small composable types over a single deeply nested literal.
