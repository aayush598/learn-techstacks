# Partial, Required, and Readonly in TypeScript

TypeScript provides built-in utility types `Partial<T>`, `Required<T>`, and `Readonly<T>` that transform all properties of a type. Understanding their shallow behavior, implementing deep versions, and knowing when to use each is essential for TypeScript mastery.

---

## Table of Contents

1. [Partial\<T\> Deep Dive](#partialt-deep-dive)
2. [Required\<T\> Deep Dive](#requiredt-deep-dive)
3. [Readonly\<T\> Deep Dive](#readonlyt-deep-dive)
4. [Shallow vs Deep Versions](#shallow-vs-deep-versions)
5. [Implementing Deep Versions](#implementing-deep-versions)
6. [When to Use Each](#when-to-use-each)
7. [Mutable Utility Type](#mutable-utility-type)
8. [Freeze with Types](#freeze-with-types)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## Partial\<T\> Deep Dive

`Partial<T>` makes all properties optional. It's defined as:

```typescript
type Partial<T> = {
  [P in keyof T]?: T[P];
};
```

### Basic usage

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

type PartialUser = Partial<User>;
// {
//   id?: number;
//   name?: string;
//   email?: string;
//   age?: number;
// }

// Use for update operations
function updateUser(id: number, updates: Partial<User>): User {
  const user = findUser(id);
  return { ...user, ...updates };
}

updateUser(1, { name: "Bob" });           // OK
updateUser(1, { email: "new@email.com" }); // OK
updateUser(1, {});                        // OK — no changes
```

### Partial with nested types (shallow!)

```typescript
interface Config {
  db: {
    host: string;
    port: number;
  };
  cache: {
    ttl: number;
  };
}

type PartialConfig = Partial<Config>;
// {
//   db?: { host: string; port: number }; // db is optional, but NOT deeply partial
//   cache?: { ttl: number };
// }

// ⚠️ You can't partially update nested properties
// updateUser({ db: { port: 5432 } }); // Error — host is required in db
```

### Partial for React props

```typescript
interface ButtonProps {
  variant: "primary" | "secondary" | "danger";
  size: "sm" | "md" | "lg";
  onClick: () => void;
  label: string;
  disabled?: boolean;
}

// Partial for default props
const defaultProps: Partial<ButtonProps> = {
  variant: "primary",
  size: "md",
  disabled: false,
};
```

---

## Required\<T\> Deep Dive

`Required<T>` makes all properties required (removes optional modifiers). It's defined as:

```typescript
type Required<T> = {
  [P in keyof T]-?: T[P];
};
```

The `-?` syntax removes the optional modifier.

### Basic usage

```typescript
interface UserConfig {
  host?: string;
  port?: number;
  debug?: boolean;
  timeout?: number;
}

type StrictConfig = Required<UserConfig>;
// {
//   host: string;
//   port: number;
//   debug: boolean;
//   timeout: number;
// }

function createServer(config: Required<UserConfig>) {
  // All properties are guaranteed to exist
  console.log(`Server at ${config.host}:${config.port}`);
}
```

### Required for validation

```typescript
interface CreateUserData {
  name?: string;
  email?: string;
  password?: string;
}

type ValidatedData = Required<CreateUserData>;
// All fields required after validation

function validate(data: CreateUserData): ValidatedData {
  if (!data.name) throw new Error("Name is required");
  if (!data.email) throw new Error("Email is required");
  if (!data.password) throw new Error("Password is required");
  return data as ValidatedData;
}
```

### Required is also shallow

```typescript
interface Config {
  db?: {
    host?: string;
    port?: number;
  };
}

type StrictConfig = Required<Config>;
// {
//   db: { host?: string; port?: number }; // db is required, but properties inside are still optional
// }
```

---

## Readonly\<T\> Deep Dive

`Readonly<T>` makes all properties readonly (cannot be reassigned). It's defined as:

```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};
```

### Basic usage

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

type ReadonlyUser = Readonly<User>;
// {
//   readonly id: number;
//   readonly name: string;
//   readonly email: string;
// }

const user: ReadonlyUser = { id: 1, name: "Alice", email: "alice@example.com" };
// user.name = "Bob"; // Compile error — Cannot assign to 'name'
```

### Readonly for function parameters

```typescript
function processUser(user: Readonly<User>) {
  // user.name = "Bob"; // Compile error — can't modify
  console.log(user.name); // OK — reading is fine
}
```

### Readonly for React state

```typescript
// React's useState returns Readonly state
const [user, setUser] = useState<User>({ id: 1, name: "Alice" });
// user.name = "Bob"; // Compile error

// Must use setter to update
setUser({ ...user, name: "Bob" });
```

### Readonly is also shallow

```typescript
interface Config {
  db: {
    host: string;
    port: number;
  };
}

type ReadonlyConfig = Readonly<Config>;
// {
//   readonly db: { host: string; port: number }; // db is readonly, but db.host is NOT
// }

const config: ReadonlyConfig = {
  db: { host: "localhost", port: 5432 },
};

// config.db = { host: "other", port: 1234 }; // Error — db is readonly
config.db.host = "other"; // OK — db.host is NOT readonly (shallow!)
```

---

## Shallow vs Deep Versions

All three utility types are **shallow** — they only affect the top-level properties.

### The shallow problem

```typescript
interface Nested {
  a: {
    b: {
      c: string;
    };
  };
}

type P = Partial<Nested>;
// { a?: { b: { c: string } } }
// a is optional, but a.b and a.b.c are NOT optional

type R = Required<P>;
// { a: { b: { c: string } } }
// a is required, but nested is NOT deeply required

type RO = Readonly<Nested>;
// { readonly a: { b: { c: string } } }
// a is readonly, but a.b and a.b.c are NOT readonly
```

---

## Implementing Deep Versions

### DeepPartial

```typescript
type DeepPartial<T> = T extends object
  ? {
      [P in keyof T]?: DeepPartial<T[P]>;
    }
  : T;

interface Config {
  db: {
    host: string;
    port: number;
    ssl: { enabled: boolean; cert: string };
  };
  cache: { ttl: number; keys: string[] };
}

type PartialConfig = DeepPartial<Config>;
// {
//   db?: {
//     host?: string;
//     port?: number;
//     ssl?: { enabled?: boolean; cert?: string };
//   };
//   cache?: { ttl?: number; keys?: string[] };
// }

// Now you can partially update nested properties
function updateConfig(base: Config, overrides: DeepPartial<Config>): Config {
  return deepMerge(base, overrides) as Config;
}
```

### DeepRequired

```typescript
type DeepRequired<T> = T extends object
  ? {
      [P in keyof T]-?: DeepRequired<T[P]>;
    }
  : T;

type StrictConfig = DeepRequired<Partial<Config>>;
// All properties at all levels are required
```

### DeepReadonly

```typescript
type DeepReadonly<T> = T extends (infer U)[]
  ? ReadonlyArray<DeepReadonly<U>>
  : T extends Map<infer K, infer V>
  ? ReadonlyMap<DeepReadonly<K>, DeepReadonly<V>>
  : T extends Set<infer V>
  ? ReadonlySet<DeepReadonly<V>>
  : T extends object
  ? {
      readonly [P in keyof T]: DeepReadonly<T[P]>;
    }
  : T;

type FrozenConfig = DeepReadonly<Config>;
// All properties at all levels are readonly
// Including arrays (readonly arrays) and Maps/Sets (ReadonlyMap/ReadonlySet)
```

### DeepMutable (reverse of DeepReadonly)

```typescript
type DeepMutable<T> = T extends readonly (infer U)[]
  ? Mutable<U>[]
  : T extends ReadonlyMap<infer K, infer V>
  ? Map<DeepMutable<K>, DeepMutable<V>>
  : T extends ReadonlySet<infer V>
  ? Set<DeepMutable<V>>
  : T extends object
  ? {
      -readonly [P in keyof T]: DeepMutable<T[P]>;
    }
  : T;
```

---

## When to Use Each

### Partial — for updates

```typescript
// ✅ Update operations
function updateUser(id: string, updates: Partial<User>): User { ... }
function patchConfig(config: Partial<AppConfig>): AppConfig { ... }

// ✅ Default values with spread
const defaults: User = { id: "", name: "", email: "" };
const overrides: Partial<User> = { name: "Alice" };
const user = { ...defaults, ...overrides };
```

### Required — for validation

```typescript
// ✅ After validation
function validateInput(input: Partial<Form>): Required<Form> { ... }

// ✅ Ensure all options are provided
function createServer(options: Required<ServerOptions>): Server { ... }
```

### Readonly — for immutability

```typescript
// ✅ Immutable state
type AppState = Readonly<{
  user: User | null;
  todos: Todo[];
  loading: boolean;
}>;

// ✅ Constants and configuration
type ImmutableConfig = Readonly<{
  apiUrl: string;
  timeout: number;
}>;

// ✅ Function parameters you won't modify
function process(data: Readonly<Data>) { ... }
```

---

## Mutable Utility Type

The reverse of `Readonly<T>` — removes readonly modifiers.

```typescript
type Mutable<T> = {
  -readonly [P in keyof T]: T[P];
};

interface ReadonlyUser {
  readonly id: number;
  readonly name: string;
  readonly email: string;
}

type MutableUser = Mutable<ReadonlyUser>;
// {
//   id: number;
//   name: string;
//   email: string;
// }

const readonlyUser: ReadonlyUser = { id: 1, name: "Alice", email: "alice@example.com" };
const mutableUser: MutableUser = { ...readonlyUser };
mutableUser.name = "Bob"; // OK
```

### DeepMutable

```typescript
type DeepMutable<T> = T extends object
  ? {
      -readonly [P in keyof T]: DeepMutable<T[P]>;
    }
  : T;
```

---

## Freeze with Types

TypeScript's `Object.freeze()` and the `Readonly` type work together.

### Runtime freeze with type safety

```typescript
function freeze<T extends object>(obj: T): Readonly<T> {
  return Object.freeze(obj) as Readonly<T>;
}

const config = freeze({
  apiUrl: "https://api.example.com",
  timeout: 5000,
});

// config.apiUrl = "other"; // Compile error (Readonly)
// Object.freeze also prevents runtime modification
```

### Deep freeze

```typescript
function deepFreeze<T extends object>(obj: T): DeepReadonly<T> {
  Object.freeze(obj);
  Object.keys(obj).forEach((key) => {
    const value = (obj as any)[key];
    if (typeof value === "object" && value !== null && !Object.isFrozen(value)) {
      deepFreeze(value);
    }
  });
  return obj as DeepReadonly<T>;
}

const config = deepFreeze({
  db: { host: "localhost", port: 5432 },
  cache: { ttl: 3600 },
});

// config.db.host = "other"; // Compile error AND runtime error
```

### const assertions (alternative to freeze)

```typescript
// As a type-level alternative to Object.freeze
const ROUTES = {
  home: "/",
  about: "/about",
} as const;

// Equivalent to:
type Routes = Readonly<{
  readonly home: "/";
  readonly about: "/about";
}>;
```

---

## Best Practices

1. **Use Partial for update/patch operations** — most common use case
2. **Use Required after validation** — ensure all fields exist
3. **Use Readonly for immutable state** — especially in React/Redux
4. **Implement deep versions when needed** — DeepPartial, DeepReadonly
5. **Combine with other utility types** — `Readonly<Partial<User>>`
6. **Use `as const` for immutable constants** — alternative to Readonly
7. **Freeze runtime objects** — for true immutability at runtime
8. **Don't overuse Partial** — it can hide missing required fields

---

## Interview Questions

### Q1: What is the difference between Partial and Required?

**Answer:** `Partial<T>` makes all properties optional (adds `?`). `Required<T>` makes all properties required (removes `?`). They are inverses of each other. `Partial` is useful for update operations; `Required` is useful after validation.

### Q2: Are Partial, Required, and Readonly shallow or deep?

**Answer:** All three are shallow — they only affect the top-level properties. For example, `Readonly<{ a: { b: string } }>` makes `a` readonly but `a.b` is still mutable. You need custom deep versions (DeepPartial, DeepReadonly) for recursive transformations.

### Q3: How do you implement DeepPartial?

**Answer:** Use a recursive mapped type: `type DeepPartial<T> = T extends object ? { [K in keyof T]?: DeepPartial<T[K]> } : T`. This recursively applies the optional modifier to all properties at all levels of nesting.

### Q4: What is the difference between Readonly and Object.freeze?

**Answer:** `Readonly<T>` is a compile-time check only — it prevents reassignment in TypeScript but has no runtime effect. `Object.freeze()` prevents modifications at runtime but has no TypeScript type impact. For both compile-time and runtime immutability, use both together.

### Q5: When would you use Partial in a React application?

**Answer:** `Partial` is commonly used for: (1) component default props, (2) update functions that accept partial state, (3) form state where fields are filled in incrementally, (4) configuration objects where only some values override defaults.

### Q6: How do you remove readonly from a type?

**Answer:** Use the `-readonly` modifier in a mapped type: `type Mutable<T> = { -readonly [K in keyof T]: T[K] }`. For deep mutable, extend this recursively.
