# Record, Pick, and Omit in TypeScript

`Record<K, V>`, `Pick<T, K>`, and `Omit<T, K>` are essential utility types for creating new types from existing ones. Understanding their differences, use cases, and interactions is fundamental to TypeScript mastery.

---

## Table of Contents

1. [Record\<K, V\> Deep Dive](#recordk-v-deep-dive)
2. [Pick\<T, K\> Deep Dive](#pickt-k-deep-dive)
3. [Omit\<T, K\> Deep Dive](#omitt-k-deep-dive)
4. [Record vs Index Signatures](#record-vs-index-signatures)
5. [Pick vs Indexed Access](#pick-vs-indexed-access)
6. [Omit vs Pick with Exclude](#omit-vs-pick-with-exclude)
7. [Omit vs Intersection](#omit-vs-intersection)
8. [Using with Unions](#using-with-unions)
9. [Real-World Patterns](#real-world-patterns)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## Record\<K, V\> Deep Dive

`Record<K, V>` constructs an object type with keys of type `K` and values of type `V`. It's defined as:

```typescript
type Record<K extends keyof any, T> = {
  [P in K]: T;
};
```

### Basic usage

```typescript
// Create a type with specific keys and value type
type UserRoles = Record<"admin" | "user" | "guest", boolean>;
// {
//   admin: boolean;
//   user: boolean;
//   guest: boolean;
// }

const roles: UserRoles = {
  admin: true,
  user: true,
  guest: false,
};
```

### Record with string keys

```typescript
// Map of string keys to a value type
type StringMap = Record<string, number>;
// { [key: string]: number }

const scores: StringMap = {
  alice: 100,
  bob: 85,
  charlie: 92,
};
```

### Record with union keys

```typescript
// Each key maps to the same value type
type StatusMessages = Record<"loading" | "success" | "error", string>;
// {
//   loading: string;
//   success: string;
//   error: string;
// }

const messages: StatusMessages = {
  loading: "Loading...",
  success: "Done!",
  error: "Something went wrong",
};
```

### Record for dictionaries

```typescript
type UserById = Record<string, User>;

const users: UserById = {
  "user-1": { id: 1, name: "Alice", email: "alice@example.com" },
  "user-2": { id: 2, name: "Bob", email: "bob@example.com" },
};

// Type-safe access
const user = users["user-1"]; // User
```

### Record with complex value types

```typescript
type ApiEndpoints = Record<string, {
  method: "GET" | "POST" | "PUT" | "DELETE";
  path: string;
  handler: () => Promise<any>;
}>;

const endpoints: ApiEndpoints = {
  getUsers: { method: "GET", path: "/users", handler: async () => [] },
  createUser: { method: "POST", path: "/users", handler: async () => ({}) },
};
```

---

## Pick\<T, K\> Deep Dive

`Pick<T, K>` constructs a type by picking a subset of properties from `T`. It's defined as:

```typescript
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

### Basic usage

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  password: string;
}

type PublicUser = Pick<User, "id" | "name" | "email">;
// {
//   id: number;
//   name: string;
//   email: string;
// }

const user: PublicUser = {
  id: 1,
  name: "Alice",
  email: "alice@example.com",
  // password is NOT required — it was not picked
};
```

### Pick for API responses

```typescript
interface FullProduct {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  images: string[];
  reviews: Review[];
  inventory: number;
  createdAt: Date;
  updatedAt: Date;
}

// List view — only essential fields
type ProductListItem = Pick<FullProduct, "id" | "name" | "price" | "images">;

// Detail view — more fields
type ProductDetail = Pick<FullProduct, "id" | "name" | "description" | "price" | "reviews">;
```

### Pick for form types

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  avatar: string;
  role: string;
  createdAt: Date;
}

// Form only needs editable fields
type UserFormData = Pick<User, "name" | "email" | "avatar" | "role">;

function createUserForm(data: UserFormData) {
  // ... form logic
}
```

### Pick with multiple keys

```typescript
type UserBasics = Pick<User, "id" | "name">;
type UserContact = Pick<User, "email" | "phone">;
type UserPreview = Pick<User, "id" | "name" | "avatar">;
```

---

## Omit\<T, K\> Deep Dive

`Omit<T, K>` constructs a type by removing a subset of properties from `T`. It's defined as:

```typescript
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;
```

### Basic usage

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
  createdAt: Date;
}

type UserWithoutPassword = Omit<User, "password">;
// {
//   id: number;
//   name: string;
//   email: string;
//   createdAt: Date;
// }

// Safe for API responses — password is excluded
function getUser(id: number): UserWithoutPassword {
  const user = database.get(id);
  const { password, ...rest } = user;
  return rest;
}
```

### Omit for create operations

```typescript
// User creation — id and createdAt are server-generated
type CreateUserInput = Omit<User, "id" | "createdAt">;
// {
//   name: string;
//   email: string;
//   password: string;
// }

function createUser(input: CreateUserInput): User {
  return {
    id: generateId(),
    ...input,
    createdAt: new Date(),
  };
}
```

### Omit multiple properties

```typescript
type SafeUser = Omit<User, "password" | "ssn" | "creditCard">;
type PublicProfile = Omit<User, "password" | "email" | "phone">;
```

---

## Record vs Index Signatures

### Record\<string, T\> vs { [key: string]: T }

```typescript
// These are equivalent:
type A = Record<string, number>;
type B = { [key: string]: number };

// But Record is more expressive:
type C = Record<"a" | "b" | "c", number>;
// { a: number; b: number; c: number } — specific keys!

// Index signatures only allow string or number keys:
type D = { [key: string]: number };
// type E = { [key: "a" | "b"]: number }; // ❌ Not allowed
```

### When to use each

```typescript
// Use Record for specific key sets
type Config = Record<"host" | "port" | "debug", string | number | boolean>;

// Use index signatures for open-ended dictionaries
type Cache = { [key: string]: unknown };

// Record is better for type-safe iteration
type StatusMap = Record<"loading" | "success" | "error", string>;
```

---

## Pick vs Indexed Access

### Pick\<T, K\> vs T[K]

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

// Pick creates a new type with the selected properties
type UserName = Pick<User, "name">;
// { name: string }

// Indexed access extracts the VALUE type
type NameType = User["name"]; // string

// Pick preserves the property structure
// Indexed access gives you the value type
```

### When to use each

```typescript
// Use Pick when you need a type with specific properties
type UserPreview = Pick<User, "id" | "name">;

// Use indexed access when you need the value type
type ValueType = User["name"]; // string

// Combine them:
type UserNames = Pick<User, "id" | "name">;
type NameValue = UserNames["name"]; // string
```

---

## Omit vs Pick with Exclude

`Omit<T, K>` is defined as `Pick<T, Exclude<keyof T, K>>`. They are inverses.

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  password: string;
}

// These are equivalent:
type A = Omit<User, "password">;
type B = Pick<User, Exclude<keyof User, "password">>;
type C = Pick<User, "id" | "name" | "email">;

// But Omit is cleaner and more readable
```

### Using Exclude explicitly

```typescript
// Get all string properties
type StringProps = Pick<User, Exclude<keyof User, "id" | "age">>;
// Picks all properties except id and age

// Get all properties except specific types
type NonFunctionProps = Pick<User, Exclude<keyof User, FunctionKeys<User>>>;
```

---

## Omit vs Intersection

### Omit removes properties

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

type UserWithoutEmail = Omit<User, "email">;
// { id: number; name: string }
```

### Intersection adds properties

```typescript
type Admin = User & {
  role: "admin";
  permissions: string[];
};
// { id: number; name: string; email: string; role: "admin"; permissions: string[] }
```

### Combining Omit and intersection

```typescript
// Replace a property type
type UserWithNumberEmail = Omit<User, "email"> & { email: number };
// { id: number; name: string; email: number }

// Add new properties while removing old ones
type AdminUser = Omit<User, "email"> & {
  adminEmail: string;
  role: "admin";
};
```

---

## Using with Unions

### Pick from a union

```typescript
type Admin = {
  role: "admin";
  name: string;
  permissions: string[];
};

type User = {
  role: "user";
  name: string;
  email: string;
};

type Person = Admin | User;

// Pick common properties
type PersonName = Pick<Person, "name">;
// { name: string } — works because "name" exists on both
```

### Omit from a union

```typescript
// Omit works differently with unions — it removes from each member
type SafePerson = Omit<Person, "role">;
// Admin: { name: string; permissions: string[] }
// User: { name: string; email: string }
```

---

## Real-World Patterns

### API response types

```typescript
interface FullUser {
  id: string;
  name: string;
  email: string;
  avatar: string;
  bio: string;
  role: "admin" | "user" | "guest";
  createdAt: Date;
  updatedAt: Date;
  lastLoginAt: Date;
  settings: UserSettings;
}

// List response — minimal data
type UserListItem = Pick<FullUser, "id" | "name" | "avatar">;

// Detail response — more data
type UserDetail = Pick<FullUser, "id" | "name" | "email" | "avatar" | "bio" | "role">;

// Create input — no server-generated fields
type CreateUserInput = Omit<FullUser, "id" | "createdAt" | "updatedAt" | "lastLoginAt">;

// Update input — partial with exclusions
type UpdateUserInput = Partial<Omit<FullUser, "id" | "createdAt">>;
```

### Form types

```typescript
interface ContactForm {
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
  attachment?: File;
  newsletter: boolean;
}

// Submission type — no attachment
type ContactSubmission = Omit<ContactForm, "attachment">;

// Validation type — all required
type ValidatedContact = Required<ContactForm>;
```

### Configuration objects

```typescript
interface ServerConfig {
  host: string;
  port: number;
  ssl: boolean;
  certPath?: string;
  keyPath?: string;
  db: DatabaseConfig;
  cache: CacheConfig;
}

// User-facing config — only user-settable properties
type UserConfig = Pick<ServerConfig, "host" | "port" | "ssl">;

// Internal config — all properties including computed ones
type InternalConfig = ServerConfig & {
  pid: number;
  uptime: number;
};
```

### Record for maps

```typescript
type Permission = "read" | "write" | "delete" | "admin";

type RolePermissions = Record<"admin" | "user" | "guest", Permission[]>;

const permissions: RolePermissions = {
  admin: ["read", "write", "delete", "admin"],
  user: ["read", "write"],
  guest: ["read"],
};

// Type-safe lookup
function getPermissions(role: keyof RolePermissions): Permission[] {
  return permissions[role];
}
```

---

## Best Practices

1. **Use Pick for public-facing types** — exclude sensitive fields
2. **Use Omit for input types** — exclude server-generated fields
3. **Use Record for dictionaries/maps** — type-safe key-value pairs
4. **Combine Pick and Omit** — for different API response shapes
5. **Use Record with union keys** — for exhaustive status maps
6. **Prefer Omit over Pick when removing many properties** — more concise
7. **Use Pick over indexed access when you need a type** — not just a value type

---

## Interview Questions

### Q1: What is the difference between Record, Pick, and Omit?

**Answer:** `Record<K, V>` creates a type with specific keys and a uniform value type. `Pick<T, K>` selects specific properties from type T. `Omit<T, K>` removes specific properties from type T. Record constructs new types; Pick and Omit transform existing types.

### Q2: How does Omit work internally?

**Answer:** `Omit<T, K>` is defined as `Pick<T, Exclude<keyof T, K>>`. It first gets all keys of T, excludes the keys in K, then picks the remaining properties. This is equivalent to creating a type without the specified properties.

### Q3: What is the difference between Record and an index signature?

**Answer:** `Record<string, T>` and `{ [key: string]: T }` are equivalent for string keys. However, Record can also use union types as keys (e.g., `Record<"a" | "b", number>`), while index signatures only support `string` or `number` keys. Record is more expressive for specific key sets.

### Q4: Can you use Pick and Omit with union types?

**Answer:** Yes, but with caveats. `Pick<A | B, "name">` works if "name" exists on both A and B. `Omit<A | B, "name">` removes "name" from each union member separately. The result is a union of the modified types.

### Q5: When would you use Record over a Map?

**Answer:** Use Record when keys are known at compile time and you want type-safe property access. Use Map when keys are dynamic, you need ordered iteration, or you need Map-specific methods like `has()`, `delete()`, or `size`. Record is better for static configurations; Map is better for dynamic collections.

### Q6: How do you replace a property type in an existing interface?

**Answer:** Use Omit and intersection: `type NewType = Omit<OriginalType, "prop"> & { prop: NewType }`. This removes the old property and adds it back with the new type. For example, `type UserWithNumberEmail = Omit<User, "email"> & { email: number }`.
