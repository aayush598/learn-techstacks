# TypeScript Coding Challenges

## 20+ Challenges with Solutions

---

## Challenge 1: Implement DeepPartial

**Problem**: Create a utility type that makes all properties of an object optional, recursively.

```typescript
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Test
interface Config {
  database: {
    host: string;
    port: number;
    credentials: {
      user: string;
      password: string;
    };
  };
  cache: {
    ttl: number;
  };
}

const config: DeepPartial<Config> = {
  database: {
    credentials: {
      user: 'admin', // OK — partial
    },
  },
};
```

---

## Challenge 2: Implement Pick

**Problem**: Create a utility type that picks specific properties from an object.

```typescript
type MyPick<T, K extends keyof T> = {
  [P in K]: T[P];
};

// Test
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

type UserBasic = MyPick<User, 'id' | 'name'>;
// { id: number; name: string }
```

---

## Challenge 3: Implement Omit

**Problem**: Create a utility type that omits specific properties from an object.

```typescript
type MyOmit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// Test
type UserWithoutEmail = MyOmit<User, 'email' | 'age'>;
// { id: number; name: string }
```

---

## Challenge 4: Implement Flatten

**Problem**: Flatten a nested array type into a single level.

```typescript
type Flatten<T extends any[]> = T extends [infer First, ...infer Rest]
  ? First extends any[]
    ? [...Flatten<First>, ...Flatten<Rest>]
    : [First, ...Flatten<Rest>]
  : T;

// Test
type Nested = [[1, 2], [3, [4, 5]], 6];
type Flat = Flatten<Nested>; // [1, 2, 3, 4, 5, 6]
```

---

## Challenge 5: Implement Currying

**Problem**: Create a type for curried functions.

```typescript
type Curried<T> = T extends (...args: infer Args) => infer Return
  ? Args extends [infer First, ...infer Rest]
    ? (arg: First) => Curried<(...args: Rest) => Return>
    : Return
  : never;

// Test
function add(a: number, b: number, c: number): number {
  return a + b + c;
}

type CurriedAdd = Curried<typeof add>;
// (arg: number) => (arg: number) => (arg: number) => number
```

---

## Challenge 6: Implement Event Emitter

**Problem**: Create a type-safe event emitter.

```typescript
type EventMap = Record<string, any>;

class TypedEmitter<Events extends EventMap> {
  private listeners = new Map<keyof Events, Set<Function>>();

  on<K extends keyof Events>(
    event: K,
    listener: (data: Events[K]) => void
  ): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]): void {
    this.listeners.get(event)?.forEach(listener => listener(data));
  }

  off<K extends keyof Events>(event: K, listener: (data: Events[K]) => void): void {
    this.listeners.get(event)?.delete(listener);
  }
}

// Test
interface AppEvents {
  login: { userId: string; timestamp: number };
  logout: { userId: string };
  error: { message: string; code: number };
}

const emitter = new TypedEmitter<AppEvents>();
emitter.on('login', (data) => {
  console.log(data.userId); // ✅ Type-safe
});
emitter.emit('login', { userId: '123', timestamp: Date.now() }); // ✅
emitter.emit('login', { userId: '123' }); // ❌ Missing timestamp
```

---

## Challenge 7: Implement Promise.all

**Problem**: Create a type-safe implementation of Promise.all.

```typescript
function typedPromiseAll<T extends readonly Promise<any>[]>(
  promises: [...T]
): Promise<{ -readonly [K in keyof T]: Awaited<T[K]> }> {
  return Promise.all(promises) as any;
}

// Test
const p1 = Promise.resolve(1);
const p2 = Promise.resolve('hello');
const p3 = Promise.resolve(true);

const result = await typedPromiseAll([p1, p2, p3]);
// type: [number, string, boolean]
```

---

## Challenge 8: Implement LRU Cache

**Problem**: Create a type-safe LRU cache.

```typescript
class LRUCache<K, V> {
  private cache = new Map<K, V>();
  private maxSize: number;

  constructor(maxSize: number) {
    this.maxSize = maxSize;
  }

  get(key: K): V | undefined {
    const value = this.cache.get(key);
    if (value !== undefined) {
      // Move to end (most recently used)
      this.cache.delete(key);
      this.cache.set(key, value);
    }
    return value;
  }

  set(key: K, value: V): void {
    if (this.cache.has(key)) {
      this.cache.delete(key);
    } else if (this.cache.size >= this.maxSize) {
      // Delete least recently used (first item)
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, value);
  }

  has(key: K): boolean {
    return this.cache.has(key);
  }

  delete(key: K): boolean {
    return this.cache.delete(key);
  }

  get size(): number {
    return this.cache.size;
  }
}

// Test
const cache = new LRUCache<string, number>(3);
cache.set('a', 1);
cache.set('b', 2);
cache.set('c', 3);
cache.get('a'); // 1 (moves 'a' to end)
cache.set('d', 4); // Evicts 'b' (least recently used)
cache.has('b'); // false
```

---

## Challenge 9: Implement DeepReadonly

**Problem**: Make all properties deeply readonly.

```typescript
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};

// Test
interface Mutable {
  nested: {
    items: string[];
    config: {
      debug: boolean;
    };
  };
}

type Immutable = DeepReadonly<Mutable>;
// All properties are readonly, including nested ones
```

---

## Challenge 10: Implement Type-safe SQL Builder

**Problem**: Create a type-safe SQL query builder.

```typescript
type TableSchema = Record<string, any>;

class QueryBuilder<T extends TableSchema> {
  private tableName: string;
  private conditions: string[] = [];
  private selectedFields: (keyof T)[] = [];

  constructor(tableName: string) {
    this.tableName = tableName;
  }

  select<K extends keyof T>(...fields: K[]): QueryBuilder<T> {
    this.selectedFields.push(...fields);
    return this;
  }

  where(field: keyof T, value: T[keyof T]): QueryBuilder<T> {
    this.conditions.push(`${String(field)} = '${value}'`);
    return this;
  }

  build(): string {
    const fields = this.selectedFields.length
      ? this.selectedFields.join(', ')
      : '*';
    const where = this.conditions.length
      ? ` WHERE ${this.conditions.join(' AND ')}`
      : '';
    return `SELECT ${fields} FROM ${this.tableName}${where}`;
  }
}

// Test
interface User {
  id: number;
  name: string;
  email: string;
}

const query = new QueryBuilder<User>('users')
  .select('id', 'name')
  .where('name', 'Alice')
  .build();

console.log(query); // SELECT id, name FROM users WHERE name = 'Alice'
```

---

## Challenge 11: Implement Type-safe Route Parameters

**Problem**: Parse route parameters from a route string.

```typescript
type ParseRoute<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? { [K in Param | keyof ParseRoute<Rest>]: string }
    : T extends `${string}:${infer Param}`
    ? { [K in Param]: string }
    : {};

// Test
type UserRoute = ParseRoute<'/users/:id/posts/:postId'>;
// { id: string; postId: string }
```

---

## Challenge 12: Implement Type-safe Store

**Problem**: Create a type-safe state management store.

```typescript
type State = Record<string, any>;

class Store<S extends State> {
  private state: S;
  private listeners = new Set<() => void>();

  constructor(initialState: S) {
    this.state = initialState;
  }

  get<K extends keyof S>(key: K): S[K] {
    return this.state[key];
  }

  set<K extends keyof S>(key: K, value: S[K]): void {
    this.state[key] = value;
    this.listeners.forEach(listener => listener());
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  getState(): Readonly<S> {
    return { ...this.state };
  }
}

// Test
const store = new Store({ count: 0, name: 'App' });
store.set('count', 1); // ✅
store.set('count', 'wrong'); // ❌ Type error
store.get('name'); // ✅ type: string
```

---

## Challenge 13: Implement Type-safe Builder Pattern

**Problem**: Create a type-safe builder for complex objects.

```typescript
type Builder<T> = {
  [K in keyof T]-?: (value: T[K]) => Builder<T>;
} & {
  build(): T;
};

function createBuilder<T extends Record<string, any>>(): Builder<T> {
  const data = {} as T;
  const builder: any = {};

  for (const key of Object.keys(data)) {
    builder[key] = (value: any) => {
      data[key as keyof T] = value;
      return builder;
    };
  }

  builder.build = () => ({ ...data });
  return builder;
}

// Test
interface UserBuilder {
  id: number;
  name: string;
  email: string;
}

const user = createBuilder<UserBuilder>()
  .id(1)
  .name('Alice')
  .email('alice@example.com')
  .build();

// user: { id: 1; name: 'Alice'; email: 'alice@example.com' }
```

---

## Challenge 14: Implement Type-safe JSON Parser

**Problem**: Parse JSON and infer types.

```typescript
type ParseJSON<T extends string> =
  T extends 'true' ? true :
  T extends 'false' ? false :
  T extends 'null' ? null :
  T extends `${number}` ? number :
  T extends `"${infer S}"` ? S :
  string;

// Test
type T1 = ParseJSON<'42'>; // number
type T2 = ParseJSON<'"hello"'>; // "hello"
type T3 = ParseJSON<'true'>; // true
type T4 = ParseJSON<'null'>; // null
```

---

## Challenge 15: Implement Type-safe API Client

**Problem**: Create a type-safe API client with method/endpoint typing.

```typescript
interface ApiEndpoints {
  'GET /users': {
    response: User[];
    query: { page?: number; limit?: number };
  };
  'POST /users': {
    response: User;
    body: { name: string; email: string };
  };
  'GET /users/:id': {
    response: User;
    params: { id: string };
  };
}

type ExtractMethod<T extends string> =
  T extends `${infer M} ${string}` ? M : never;

type ExtractPath<T extends string> =
  T extends `${string} ${infer P}` ? P : never;

class ApiClient {
  async request<K extends keyof ApiEndpoints>(
    endpoint: K,
    options?: Omit<ApiEndpoints[K], 'response'>
  ): Promise<ApiEndpoints[K]['response']> {
    const [method, path] = (endpoint as string).split(' ');
    const response = await fetch(path, { method, ...options });
    return response.json();
  }
}

// Test
const client = new ApiClient();
const users = await client.request('GET /users', {
  query: { page: 1, limit: 10 },
});
// users: User[]
```

---

## Challenge 16: Implement Type-safe Middleware

**Problem**: Create a type-safe middleware chain.

```typescript
type Context = Record<string, any>;

type Middleware<Ctx extends Context> = (
  ctx: Ctx,
  next: () => Promise<void>
) => Promise<void>;

class Pipeline<Ctx extends Context> {
  private middlewares: Middleware<Ctx>[] = [];

  use(middleware: Middleware<Ctx>): this {
    this.middlewares.push(middleware);
    return this;
  }

  async execute(ctx: Ctx): Promise<Ctx> {
    const run = async (index: number): Promise<void> => {
      if (index >= this.middlewares.length) return;
      const middleware = this.middlewares[index];
      await middleware(ctx, () => run(index + 1));
    };
    await run(0);
    return ctx;
  }
}

// Test
interface RequestContext extends Context {
  user?: { id: string; name: string };
  response?: any;
}

const pipeline = new Pipeline<RequestContext>();
pipeline
  .use(async (ctx, next) => {
    ctx.user = { id: '1', name: 'Alice' };
    await next();
  })
  .use(async (ctx, next) => {
    ctx.response = `Hello ${ctx.user?.name}`;
    await next();
  });

const result = await pipeline.execute({});
console.log(result.response); // "Hello Alice"
```

---

## Challenge 17: Implement Type-safe Form Validator

**Problem**: Create a type-safe form validation system.

```typescript
type ValidationRules<T> = {
  [K in keyof T]?: {
    required?: boolean;
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    custom?: (value: T[K]) => boolean;
    message?: string;
  };
};

type ValidationErrors<T> = {
  [K in keyof T]?: string;
};

class FormValidator<T extends Record<string, any>> {
  private rules: ValidationRules<T>;

  constructor(rules: ValidationRules<T>) {
    this.rules = rules;
  }

  validate(data: T): { valid: boolean; errors: ValidationErrors<T> } {
    const errors: ValidationErrors<T> = {};
    let valid = true;

    for (const [field, rule] of Object.entries(this.rules)) {
      const value = data[field as keyof T];
      const fieldRules = rule as any;

      if (fieldRules.required && (value === undefined || value === null)) {
        errors[field as keyof T] = fieldRules.message || `${field} is required`;
        valid = false;
      }

      if (fieldRules.minLength && typeof value === 'string' && value.length < fieldRules.minLength) {
        errors[field as keyof T] = `${field} must be at least ${fieldRules.minLength} characters`;
        valid = false;
      }

      if (fieldRules.pattern && typeof value === 'string' && !fieldRules.pattern.test(value)) {
        errors[field as keyof T] = fieldRules.message || `${field} is invalid`;
        valid = false;
      }

      if (fieldRules.custom && !fieldRules.custom(value)) {
        errors[field as keyof T] = fieldRules.message || `${field} is invalid`;
        valid = false;
      }
    }

    return { valid, errors };
  }
}

// Test
interface LoginForm {
  email: string;
  password: string;
}

const validator = new FormValidator<LoginForm>({
  email: {
    required: true,
    pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    message: 'Invalid email address',
  },
  password: {
    required: true,
    minLength: 8,
  },
});

const result = validator.validate({ email: 'bad', password: '123' });
// { valid: false, errors: { email: 'Invalid email address', password: '...' } }
```

---

## Challenge 18: Implement Type-safe Debounce

**Problem**: Create a type-safe debounce function.

```typescript
function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}

// Test
function search(query: string, limit: number): void {
  console.log(`Searching: ${query}`);
}

const debouncedSearch = debounce(search, 300);
debouncedSearch('hello', 10); // ✅ Type-safe
debouncedSearch(123, 'wrong'); // ❌ Type error
```

---

## Challenge 19: Implement Type-safe Event System

**Problem**: Create a type-safe publish/subscribe system.

```typescript
type Events = Record<string, any>;

class TypedPubSub<Events extends Record<string, any>> {
  private subscribers = new Map<keyof Events, Set<Function>>();

  subscribe<K extends keyof Events>(
    event: K,
    handler: (data: Events[K]) => void
  ): () => void {
    if (!this.subscribers.has(event)) {
      this.subscribers.set(event, new Set());
    }
    this.subscribers.get(event)!.add(handler);

    return () => {
      this.subscribers.get(event)?.delete(handler);
    };
  }

  publish<K extends keyof Events>(event: K, data: Events[K]): void {
    this.subscribers.get(event)?.forEach(handler => handler(data));
  }
}

// Test
interface AppEvents {
  userCreated: { id: string; name: string };
  userDeleted: { id: string };
  error: { message: string };
}

const pubsub = new TypedPubSub<AppEvents>();
const unsubscribe = pubsub.subscribe('userCreated', (data) => {
  console.log(data.id); // ✅ Type-safe
});

pubsub.publish('userCreated', { id: '1', name: 'Alice' }); // ✅
pubsub.publish('userCreated', { id: '1' }); // ❌ Missing name
unsubscribe();
```

---

## Challenge 20: Implement Type-safeORM Query Builder

**Problem**: Create a type-safe ORM-style query builder.

```typescript
type Schema = Record<string, { type: any; nullable?: boolean }>;

class QueryBuilder<T extends Schema> {
  private table: string;
  private selectFields: (keyof T)[] = [];
  private whereConditions: string[] = [];
  private orderByField?: keyof T;
  private limitValue?: number;

  constructor(table: string) {
    this.table = table;
  }

  select<K extends keyof T>(...fields: K[]): this {
    this.selectFields.push(...fields);
    return this;
  }

  where<K extends keyof T>(field: K, op: '=' | '>' | '<' | '!=', value: T[K]['type']): this {
    this.whereConditions.push(`${String(field)} ${op} ${JSON.stringify(value)}`);
    return this;
  }

  orderBy(field: keyof T): this {
    this.orderByField = field;
    return this;
  }

  limit(n: number): this {
    this.limitValue = n;
    return this;
  }

  toSQL(): string {
    const fields = this.selectFields.length
      ? this.selectFields.join(', ')
      : '*';
    const where = this.whereConditions.length
      ? ` WHERE ${this.whereConditions.join(' AND ')}`
      : '';
    const order = this.orderByField ? ` ORDER BY ${String(this.orderByField)}` : '';
    const limit = this.limitValue ? ` LIMIT ${this.limitValue}` : '';
    return `SELECT ${fields} FROM ${this.table}${where}${order}${limit}`;
  }
}

// Test
interface UserSchema {
  id: { type: number };
  name: { type: string };
  email: { type: string };
}

const query = new QueryBuilder<UserSchema>('users')
  .select('id', 'name')
  .where('name', '=', 'Alice')
  .orderBy('id')
  .limit(10)
  .toSQL();

console.log(query);
// SELECT id, name FROM users WHERE name = "Alice" ORDER BY id LIMIT 10
```

---

## Challenge 21: Implement Type-safe Pipe Function

**Problem**: Create a type-safe pipe function that chains functions.

```typescript
type Pipe<T extends any[]> = T extends [infer First, ...infer Rest]
  ? First extends (...args: any[]) => infer Return
    ? Rest extends [(...args: [Return]) => any, ...any[]]
      ? [First, ...Pipe<Rest>]
      : [First]
    : never
  : [];

function pipe<Fns extends ((...args: any[]) => any)[]>(
  ...fns: Fns
): (...args: Parameters<Fns[0]>) => ReturnType<Fns[Fns['length'] - 1]> {
  return (...args: any[]) => {
    return fns.reduce((acc, fn) => fn(acc), fns[0](...args));
  };
}

// Test
const process = pipe(
  (x: number) => x + 1,
  (x: number) => x * 2,
  (x: number) => x.toString()
);

const result = process(5); // "12" (type: string)
```

---

## Complexity Analysis

| Challenge | Time | Space | Difficulty |
|-----------|------|-------|------------|
| DeepPartial | O(n) | O(n) | Easy |
| Pick/Omit | O(n) | O(k) | Easy |
| Flatten | O(n) | O(n) | Medium |
| Currying | O(n) | O(n) | Medium |
| Event Emitter | O(1) | O(n) | Medium |
| Promise.all | O(n) | O(n) | Medium |
| LRU Cache | O(1) | O(k) | Medium |
| DeepReadonly | O(n) | O(n) | Easy |
| SQL Builder | O(n) | O(n) | Medium |
| Route Parser | O(n) | O(n) | Hard |
