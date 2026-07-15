# 05 — Generic Constraints

## Table of Contents

1. [The `extends` Keyword in Generics](#extends-keyword)
2. [keyof Constraint](#keyof-constraint)
3. [typeof Constraint](#typeof-constraint)
4. [Constraint with Interfaces](#constraint-with-interfaces)
5. [Multiple Constraints](#multiple-constraints)
6. [Constraint Chaining](#constraint-chaining)
7. [Constraint with Union Types](#constraint-with-union-types)
8. [When to Add Constraints](#when-to-add-constraints)
9. [Common Constraint Patterns](#common-constraint-patterns)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## The `extends` Keyword in Generics

The `extends` keyword in a generic context means `T` must be a **subtype of** (or
assignable to) the constraint type. It is not the same as class inheritance.

```typescript
// T must have a .length property
function logLength<T extends { length: number }>(value: T): void {
  console.log(`Length: ${value.length}`);
}

logLength("hello");        // ✅ string has length
logLength([1, 2, 3]);      // ✅ array has length
logLength({ length: 10 }); // ✅ matches shape
// logLength(42);           // ❌ number has no length
```

### Constrained to a Specific Type

```typescript
function double<T extends number>(value: T): number {
  return value * 2;
}

double(5);       // ✅
// double("5");  // ❌ string is not assignable to number
```

### Constrained to an Interface

```typescript
interface HasId {
  id: string;
}

function findById<T extends HasId>(items: T[], id: string): T | undefined {
  return items.find((item) => item.id === id);
}

const users = [{ id: "1", name: "Alice" }, { id: "2", name: "Bob" }];
findById(users, "1"); // ✅ returns { id: string, name: string }

const numbers = [1, 2, 3];
// findById(numbers, "1"); // ❌ number[] doesn't satisfy HasId
```

---

## keyof Constraint

The `keyof` constraint ensures that a type parameter is a key of another type.

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user = { name: "Alice", age: 30, email: "alice@example.com" };

getProperty(user, "name");  // ✅ string
getProperty(user, "age");   // ✅ number
// getProperty(user, "phone"); // ❌ "phone" not in keyof typeof user
```

### keyof with Strings

```typescript
function pick<T, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const key of keys) {
    result[key] = obj[key];
  }
  return result;
}

const user = { name: "Alice", age: 30, email: "alice@example.com" };
const summary = pick(user, ["name", "email"]);
// summary: { name: string; email: string }
```

### keyof with Constraints

```typescript
interface Config {
  apiUrl: string;
  timeout: number;
  retries: number;
}

function getConfigValue<K extends keyof Config>(key: K): Config[K] {
  const defaults: Config = {
    apiUrl: "https://api.example.com",
    timeout: 5000,
    retries: 3,
  };
  return defaults[key];
}

const url = getConfigValue("apiUrl");      // string
const timeout = getConfigValue("timeout"); // number
// getConfigValue("unknown"); // ❌
```

### Dynamic keyof with Mapped Types

```typescript
function createGetters<T extends Record<string, unknown>>(obj: T): {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
} {
  const result = {} as any;
  for (const key of Object.keys(obj)) {
    const getterName = `get${key.charAt(0).toUpperCase()}${key.slice(1)}`;
    result[getterName] = () => (obj as any)[key];
  }
  return result;
}

const user = { name: "Alice", age: 30 };
const getters = createGetters(user);
getters.getName(); // "Alice"
getters.getAge();  // 30
```

---

## typeof Constraint

Use `typeof` to constrain a type parameter to match the type of a specific value.

```typescript
function createEqual<T>(a: T, b: T): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

// Constrain to a specific value's type
const defaultConfig = {
  apiUrl: "https://api.example.com",
  timeout: 5000,
};

function mergeConfig<T extends typeof defaultConfig>(
  base: T,
  overrides: Partial<T>
): T {
  return { ...base, ...overrides };
}

const config = mergeConfig(defaultConfig, { timeout: 10000 });
// config.apiUrl: string, config.timeout: number
```

### typeof for Instance Type

```typescript
class Calculator {
  private result = 0;

  add(n: number): this {
    this.result += n;
    return this;
  }

  subtract(n: number): this {
    this.result -= n;
    return this;
  }

  getResult(): number {
    return this.result;
  }
}

function chainOperations<T extends Calculator>(
  calculator: T,
  operations: Array<(calc: T) => T>
): T {
  return operations.reduce((calc, op) => op(calc), calculator);
}

const calc = new Calculator();
const result = chainOperations(calc, [
  (c) => c.add(10),
  (c) => c.subtract(3),
  (c) => c.add(5),
]);
result.getResult(); // 12
```

---

## Constraint with Interfaces

Interfaces make excellent constraints because they describe the shape that a type
must have.

```typescript
interface Serializable {
  serialize(): string;
}

interface Deserializable {
  deserialize(data: string): this;
}

class DataStore<T extends Serializable & Deserializable> {
  private items: T[] = [];

  add(item: T): void {
    this.items.push(item);
  }

  save(): string {
    return JSON.stringify(this.items.map((item) => item.serialize()));
  }

  load(data: string): void {
    const parsed = JSON.parse(data) as string[];
    this.items = parsed.map((s) => {
      const item = {} as T;
      return item.deserialize(s);
    });
  }
}
```

### Constrained to Function Signature

```typescript
interface AsyncFunction<TArgs extends unknown[], TResult> {
  (...args: TArgs): Promise<TResult>;
}

async function withTimeout<TArgs extends unknown[], TResult>(
  fn: AsyncFunction<TArgs, TResult>,
  timeoutMs: number,
  ...args: TArgs
): Promise<TResult> {
  return Promise.race([
    fn(...args),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error("Timeout")), timeoutMs)
    ),
  ]);
}
```

---

## Multiple Constraints

You can combine multiple constraints using intersection (`&`).

```typescript
interface HasLength {
  length: number;
}

interface Printable {
  toString(): string;
}

function process<T extends HasLength & Printable>(value: T): void {
  console.log(`Length: ${value.length}, Value: ${value.toString()}`);
}

process("hello");   // ✅ string has both
process([1, 2, 3]); // ✅ array has both
// process(42);     // ❌ number has length (via coercion) but not reliably
```

### Multiple Constraints with Different Shapes

```typescript
interface HasId {
  id: string;
}

interface Timestamped {
  createdAt: Date;
  updatedAt: Date;
}

interface SoftDeletable {
  deletedAt: Date | null;
}

type BaseEntity = HasId & Timestamped & SoftDeletable;

function restoreEntity<T extends BaseEntity>(entity: T): T {
  return { ...entity, deletedAt: null };
}

const user = {
  id: "1",
  name: "Alice",
  createdAt: new Date(),
  updatedAt: new Date(),
  deletedAt: new Date(),
};

restoreEntity(user); // ✅
```

---

## Constraint Chaining

You can build complex constraint hierarchies by composing interfaces.

```typescript
// Level 1: Basic shape
interface Identifiable {
  id: string;
}

// Level 2: Extends Identifiable
interface Auditable extends Identifiable {
  createdAt: Date;
  updatedAt: Date;
}

// Level 3: Extends Auditable
interface Versionable extends Auditable {
  version: number;
}

// Constraint uses the most specific interface
function updateVersion<T extends Versionable>(entity: T): T {
  return {
    ...entity,
    version: entity.version + 1,
    updatedAt: new Date(),
  };
}

// Works with any type that satisfies Versionable
const doc = {
  id: "doc-1",
  createdAt: new Date(),
  updatedAt: new Date(),
  version: 3,
  title: "TypeScript Guide",
};

updateVersion(doc); // version becomes 4
```

### Functional Constraint Chaining

```typescript
interface Readable {
  read(): string;
}

interface Writable extends Readable {
  write(data: string): void;
}

interface Seekable extends Writable {
  seek(position: number): void;
  position(): number;
}

function copyBetween<TSrc extends Readable, TDest extends Writable>(
  source: TSrc,
  dest: TDest,
  length: number
): void {
  const data = source.read().slice(0, length);
  dest.write(data);
}
```

---

## Constraint with Union Types

Constraints can reference union types to limit T to a specific set.

```typescript
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE" | "PATCH";

function makeRequest<TBody, TMethod extends HttpMethod>(
  method: TMethod,
  url: string,
  body?: TMethod extends "GET" | "DELETE" ? never : TBody
): Promise<Response> {
  const options: RequestInit = { method };
  if (body && method !== "GET" && method !== "DELETE") {
    options.body = JSON.stringify(body);
  }
  return fetch(url, options);
}

// ✅ GET with no body
makeRequest("GET", "/api/users");

// ✅ POST with body
makeRequest("POST", "/api/users", { name: "Alice" });

// ❌ GET with body (type error)
// makeRequest("GET", "/api/users", { name: "Alice" });
```

### Union Constraint for Discriminated Types

```typescript
type ShapeKind = "circle" | "rectangle" | "triangle";

interface Circle {
  kind: "circle";
  radius: number;
}

interface Rectangle {
  kind: "rectangle";
  width: number;
  height: number;
}

interface Triangle {
  kind: "triangle";
  base: number;
  height: number;
}

type Shape = Circle | Rectangle | Triangle;

function createShape<TKind extends ShapeKind>(
  kind: TKind,
  dimensions: Omit<Extract<Shape, { kind: TKind }>, "kind">
): Shape {
  return { kind, ...dimensions } as Shape;
}

const circle = createShape("circle", { radius: 5 });
const rect = createShape("rectangle", { width: 10, height: 20 });
// createShape("pentagon", {}); // ❌ "pentagon" not in ShapeKind
```

---

## When to Add Constraints

### Add constraints when:

1. **The function/class only works with certain shapes** — prevents runtime errors.
2. **You need to access specific properties** — TypeScript requires proof the property
   exists.
3. **You want to prevent misuse** — make invalid states unrepresentable.
4. **Error messages need to be clear** — constraints produce better error messages than
   runtime crashes.

### Don't add constraints when:

1. **The function works with any type** — unnecessary constraints reduce flexibility.
2. **The constraint would just be `object`** — too broad to be useful.
3. **The constraint adds no safety** — if it doesn't prevent errors, it's noise.

```typescript
// ✅ No constraint needed — works with any type
function identity<T>(value: T): T {
  return value;
}

// ✅ Constraint needed — accesses .length
function first<T extends { length: number }>(items: T): T {
  return items;
}

// ❌ Bad: constraint adds no value
function echo<T extends object>(value: T): T {
  return value;
}
```

---

## Common Constraint Patterns

### Pattern 1: Has Property

```typescript
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const users = [{ name: "Alice", age: 30 }, { name: "Bob", age: 25 }];
pluck(users, "name"); // ["Alice", "Bob"]
pluck(users, "age");  // [30, 25]
```

### Pattern 2: Has Method

```typescript
interface Convertible {
  toLocaleString(): string;
}

function formatAll<T extends Convertible>(items: T[]): string[] {
  return items.map((item) => item.toLocaleString());
}

formatAll([new Date(), new Date()]); // ["1/15/2026", "1/15/2026"]
formatAll([1000, 2000, 3000]);       // ["1,000", "2,000", "3,000"]
```

### Pattern 3: Constructor Constraint

```typescript
interface Constructable<T> {
  new (...args: any[]): T;
}

function createInstance<T>(Ctor: Constructable<T>): T {
  return new Ctor();
}

class MyClass {
  name = "instance";
}

const instance = createInstance(MyClass); // MyClass { name: "instance" }
```

### Pattern 4: Array-like

```typescript
function first<T>(items: { [0]: T; length: number }): T {
  return items[0];
}

first([1, 2, 3]);   // 1
first("hello");     // "h"
first({ 0: "a", length: 1 }); // "a"
```

### Pattern 5: Numeric

```typescript
function clamp<T extends number>(value: T, min: number, max: number): T {
  return Math.min(Math.max(value, min), max) as T;
}

clamp(15, 0, 10);  // 10
clamp(-5, 0, 10);  // 0
```

---

## Best Practices

1. **Constrain as narrowly as possible** — don't accept `object` when `{ length: number }` suffices.
2. **Use keyof for property access** — it's the safest way to index into objects.
3. **Compose constraints** — use intersection (`&`) to combine multiple requirements.
4. **Document why** — add JSDoc explaining why the constraint exists.
5. **Test edge cases** — ensure your constraints correctly reject invalid types.

---

## Interview Questions

**Q1: What does `extends` mean in a generic context?**

It means `T` must be assignable to the constraint type. For `<T extends { length: number }>`,
`T` must have a `length` property. It does not mean `T` inherits from the constraint.

**Q2: How do you constrain a type parameter to be a key of another type?**

Use `keyof`: `<T, K extends keyof T>`. This ensures `K` is a valid key of `T`.

**Q3: Can you use `typeof` in generic constraints?**

Yes. `<T extends typeof defaultValue>` constrains `T` to the type of `defaultValue`.

**Q4: How do you combine multiple constraints?**

Use intersection: `<T extends A & B>`. The type parameter must satisfy both A and B.

**Q5: When should you not use constraints?**

When the function works correctly with any type. Unnecessary constraints reduce
flexibility and produce confusing error messages for callers.
