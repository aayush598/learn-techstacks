# 03 — Generic Interfaces

## Table of Contents

1. [Generic Interface Syntax](#generic-interface-syntax)
2. [Generic Interfaces for API Responses](#api-responses)
3. [Generic Interfaces for Collections](#collections)
4. [Generic Interfaces with Constraints](#constraints)
5. [Extending Generic Interfaces](#extending-generic-interfaces)
6. [Generic Index Signatures](#generic-index-signatures)
7. [Generic Interfaces vs Generic Type Aliases](#interfaces-vs-type-aliases)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Generic Interface Syntax

A generic interface declares one or more type parameters that can be used throughout
the interface definition.

```typescript
interface Container<T> {
  value: T;
  getValue(): T;
}

// Implementing with concrete types
const stringContainer: Container<string> = {
  value: "hello",
  getValue() {
    return this.value;
  },
};

const numberContainer: Container<number> = {
  value: 42,
  getValue() {
    return this.value;
  },
};
```

### Multiple Type Parameters

```typescript
interface Pair<T, U> {
  first: T;
  second: U;
  asTuple(): [T, U];
}

const pair: Pair<string, number> = {
  first: "hello",
  second: 42,
  asTuple() {
    return [this.first, this.second];
  },
};
```

---

## Generic Interfaces for API Responses

One of the most common use cases is typing API responses.

### Basic API Response

```typescript
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
  timestamp: string;
}

interface User {
  id: string;
  name: string;
  email: string;
}

interface Post {
  id: string;
  title: string;
  body: string;
  authorId: string;
}

const userResponse: ApiResponse<User> = {
  data: {
    id: "1",
    name: "Alice",
    email: "alice@example.com",
  },
  status: 200,
  message: "Success",
  timestamp: "2026-01-15T10:30:00Z",
};

const postResponse: ApiResponse<Post[]> = {
  data: [
    { id: "1", title: "Hello", body: "World", authorId: "1" },
    { id: "2", title: "TypeScript", body: "Rocks", authorId: "2" },
  ],
  status: 200,
  message: "Success",
  timestamp: "2026-01-15T10:31:00Z",
};
```

### Typed Error Response

```typescript
interface ApiError {
  code: string;
  details: string;
}

interface ApiResponse<T, E = ApiError> {
  data: T | null;
  error: E | null;
  status: number;
}

function handleResponse<T>(response: ApiResponse<T>): void {
  if (response.error) {
    console.error(`Error ${response.error.code}: ${response.error.details}`);
    return;
  }
  console.log(response.data);
}

const successResponse: ApiResponse<User> = {
  data: { id: "1", name: "Alice", email: "alice@example.com" },
  error: null,
  status: 200,
};

const errorResponse: ApiResponse<User> = {
  data: null,
  error: { code: "NOT_FOUND", details: "User not found" },
  status: 404,
};
```

### Paginated Response

```typescript
interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
    hasNext: boolean;
    hasPrevious: boolean;
  };
}

interface Product {
  id: string;
  name: string;
  price: number;
}

const productsPage: PaginatedResponse<Product> = {
  items: [
    { id: "1", name: "Widget", price: 9.99 },
    { id: "2", name: "Gadget", price: 19.99 },
  ],
  pagination: {
    page: 1,
    pageSize: 20,
    total: 100,
    totalPages: 5,
    hasNext: true,
    hasPrevious: false,
  },
};
```

### GraphQL Response

```typescript
interface GraphQLResponse<TData> {
  data: TData | null;
  errors?: Array<{
    message: string;
    locations?: Array<{ line: number; column: number }>;
    path?: (string | number)[];
  }>;
}

interface UserQueryResult {
  user: {
    id: string;
    name: string;
    posts: Array<{
      id: string;
      title: string;
    }>;
  };
}

const graphqlResponse: GraphQLResponse<UserQueryResult> = {
  data: {
    user: {
      id: "1",
      name: "Alice",
      posts: [{ id: "1", title: "Hello" }],
    },
  },
};
```

---

## Generic Interfaces for Collections

Generic interfaces model collections where the element type varies.

```typescript
interface Stack<T> {
  push(item: T): void;
  pop(): T | undefined;
  peek(): T | undefined;
  size(): number;
  isEmpty(): boolean;
}

interface Queue<T> {
  enqueue(item: T): void;
  dequeue(): T | undefined;
  peek(): T | undefined;
  size(): number;
  isEmpty(): boolean;
}

interface LinkedList<T> {
  head: ListNode<T> | null;
  append(value: T): void;
  prepend(value: T): void;
  find(predicate: (item: T) => boolean): ListNode<T> | null;
  toArray(): T[];
}

interface ListNode<T> {
  value: T;
  next: ListNode<T> | null;
}

// Usage
const numberStack: Stack<number> = {
  push(item) { /* ... */ },
  pop() { return undefined; },
  peek() { return undefined; },
  size() { return 0; },
  isEmpty() { return true; },
};
```

### Map-like Interface

```typescript
interface TypedMap<K, V> {
  set(key: K, value: V): void;
  get(key: K): V | undefined;
  has(key: K): boolean;
  delete(key: K): boolean;
  entries(): Array<[K, V]>;
  keys(): K[];
  values(): V[];
}
```

---

## Generic Interfaces with Constraints

You can constrain the type parameters of an interface.

```typescript
interface Comparable<T> {
  compare(other: T): -1 | 0 | 1;
}

interface SortableCollection<T extends Comparable<T>> {
  items: T[];
  sort(): T[];
  add(item: T): void;
  remove(item: T): boolean;
}

// Must implement Comparable
class SortedList<T extends Comparable<T>> implements SortableCollection<T> {
  items: T[] = [];

  sort(): T[] {
    return this.items.sort((a, b) => a.compare(b));
  }

  add(item: T): void {
    this.items.push(item);
  }

  remove(item: T): boolean {
    const index = this.items.findIndex(
      (i) => i.compare(item) === 0
    );
    if (index !== -1) {
      this.items.splice(index, 1);
      return true;
    }
    return false;
  }
}
```

### Constrained Key-Value Store

```typescript
interface KeyValueStore<K extends string | number, V> {
  get(key: K): V | undefined;
  set(key: K, value: V): void;
  getAll(): Record<K, V>;
}

// Keys must be strings or numbers, values can be anything
const store: KeyValueStore<string, number> = {
  get(key) { return undefined; },
  set(key, value) { /* ... */ },
  getAll() { return {} as Record<string, number>; },
};
```

---

## Extending Generic Interfaces

Generic interfaces can extend other generic interfaces, reusing or adding type
parameters.

### Basic Extension

```typescript
interface BaseEntity {
  id: string;
  createdAt: Date;
  updatedAt: Date;
}

interface TimestampedEntity<T extends BaseEntity> extends BaseEntity {
  metadata: T;
}

interface UserMetadata {
  lastLogin: Date;
  loginCount: number;
}

interface User extends TimestampedEntity<UserMetadata> {
  name: string;
  email: string;
}
```

### Multiple Extension

```typescript
interface Serializable {
  serialize(): string;
}

interface Validatable {
  validate(): boolean;
  errors: string[];
}

interface BaseModel<T> {
  id: string;
  data: T;
}

interface ApiModel<T> extends BaseModel<T>, Serializable, Validatable {
  version: number;
  lastSynced: Date | null;
}

const user: ApiModel<User> = {
  id: "1",
  data: { id: "1", name: "Alice", email: "alice@example.com", createdAt: new Date(), updatedAt: new Date() },
  version: 1,
  lastSynced: null,
  serialize() { return JSON.stringify(this); },
  validate() { return this.errors.length === 0; },
  errors: [],
};
```

### Override with Narrower Types

```typescript
interface Container<T> {
  value: T;
  getValue(): T;
}

interface OptionalContainer<T> extends Container<T | undefined> {
  hasValue(): boolean;
}

const optionalString: OptionalContainer<string> = {
  value: undefined,
  getValue() { return this.value; },
  hasValue() { return this.value !== undefined; },
};
```

---

## Generic Index Signatures

Generic interfaces can have index signatures that use type parameters.

```typescript
interface StringMap<T> {
  [key: string]: T;
}

interface NumberKeyMap<T> {
  [key: number]: T;
}

// Usage
const cache: StringMap<string> = {
  "user:1": "Alice",
  "user:2": "Bob",
};

const lookup: NumberKeyMap<User> = {
  1: { id: "1", name: "Alice", email: "alice@example.com", createdAt: new Date(), updatedAt: new Date() },
};
```

### Generic Interface with Known and Unknown Keys

```typescript
interface Config<T extends Record<string, unknown>> {
  defaults: T;
  overrides: Partial<T>;
  environment: "development" | "staging" | "production";
  get(key: keyof T): T[keyof T];
}

interface AppConfig {
  apiUrl: string;
  timeout: number;
  retries: number;
}

const config: Config<AppConfig> = {
  defaults: {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3,
  },
  overrides: {
    timeout: 10000,
  },
  environment: "production",
  get(key) {
    return this.overrides[key] ?? this.defaults[key];
  },
};
```

---

## Generic Interfaces vs Generic Type Aliases

| Feature | Interface | Type Alias |
|---|---|---|
| Declaration merging | ✅ Yes | ❌ No |
| Extends/implements | ✅ Yes | ⚠️ Intersection only |
| Tuple types | ❌ No | ✅ Yes |
| Union types | ❌ No | ✅ Yes |
| Mapped types | ❌ No | ✅ Yes |
| Conditional types | ❌ No | ✅ Yes |
| Readability (objects) | ✅ Better | ⚠️ Okay |
| Performance | ✅ Faster (lazy) | ⚠️ Eagerly resolved |

### When to Use Interfaces

```typescript
// ✅ Good: object shape, implementable by classes
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(item: T): Promise<T>;
  update(id: string, item: Partial<T>): Promise<T>;
  delete(id: string): Promise<boolean>;
}

// ✅ Good: extends other interfaces
interface CrudRepository<T> extends Repository<T> {
  count(): Promise<number>;
  exists(id: string): Promise<boolean>;
}
```

### When to Use Type Aliases

```typescript
// ✅ Good: union types
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// ✅ Good: mapped types
type Optional<T> = {
  [K in keyof T]?: T[K];
};

// ✅ Good: conditional types
type IsString<T> = T extends string ? true : false;

// ✅ Good: tuples
type Pair<T> = [T, T];
```

### The Same Thing, Two Ways

```typescript
// Interface
interface StringArray {
  [index: number]: string;
  length: number;
}

// Type alias
type StringArray = {
  [index: number]: string;
  length: number;
};

// Both work the same for basic object shapes.
// The type alias allows more advanced features but loses declaration merging.
```

---

## Best Practices

1. **Use interfaces for object shapes** that might be implemented by classes or
   extended by other interfaces.
2. **Use type aliases for unions, intersections, mapped types, and conditional types**.
3. **Provide default type parameters** when there's a common case (e.g.,
   `interface ApiResponse<T, E = ApiError>`).
4. **Name generic parameters meaningfully** in complex interfaces — `TData`, `TError`,
   `TKey`, `TValue`.
5. **Keep the number of type parameters small** — if you need more than 3, consider
   nesting or restructuring.
6. **Use constraints** to document and enforce valid type combinations.

---

## Interview Questions

**Q1: What is a generic interface?**

A generic interface is an interface that declares one or more type parameters, making
its shape reusable across different types. For example, `interface Box<T> { value: T }`
can hold any type.

**Q2: When should you prefer an interface over a type alias for generics?**

Use interfaces when you need declaration merging, class implementation, or extension
via `extends`. Use type aliases for unions, intersections, mapped types, conditional
types, and tuples.

**Q3: Can you extend a generic interface with a concrete type?**

Yes. `interface StringBox extends Box<string>` narrows the generic to a specific type.

**Q4: How do you add a default type parameter to an interface?**

Use the `=` syntax: `interface Response<T = unknown>`. When no type argument is given,
`T` defaults to `unknown`.

**Q5: What are the limitations of generic interfaces?**

They cannot express union types, conditional types, mapped types, or tuple types.
For those, use type aliases.
