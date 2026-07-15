# Common TypeScript Interview Questions

## 50+ Questions with Detailed Answers

---

## Fundamentals

### Q1: What is TypeScript?
**A**: TypeScript is a statically typed superset of JavaScript that compiles to plain JavaScript. It adds optional type annotations, interfaces, generics, and other features that help catch errors at compile time and improve code tooling.

### Q2: What are the advantages of TypeScript over JavaScript?
**A**:
1. **Static type checking**: Catch errors at compile time
2. **Better IDE support**: Autocomplete, refactoring, navigation
3. **Code documentation**: Types serve as documentation
4. **Safer refactoring**: Change code with confidence
5. **Better collaboration**: Clear interfaces between modules
6. **JavaScript compatibility**: Any valid JS is valid TS

### Q3: What is the difference between `any`, `unknown`, and `never`?
**A**:

```typescript
// any: Disables type checking
let value: any = 'hello';
value = 42; // OK
value.foo(); // OK at compile time (error at runtime)

// unknown: Type-safe any
let unknown: unknown = 'hello';
unknown = 42; // OK
unknown.foo(); // Error — must narrow first
if (typeof unknown === 'string') {
  unknown.toUpperCase(); // OK after narrowing
}

// never: Represents values that never occur
function throwError(): never {
  throw new Error('Error');
}
function infiniteLoop(): never {
  while (true) {}
}
```

### Q4: What is the difference between `interface` and `type`?
**A**:

```typescript
// Interface: Extensible, declaration merging
interface User {
  name: string;
}
interface User {
  age: number; // Merges with previous
}
// User = { name: string; age: number }

// Interface extends
interface Admin extends User {
  role: string;
}

// Type: More powerful, no declaration merging
type UserType = {
  name: string;
};

// Type aliases
type ID = string | number;
type Result<T> = { data: T } | { error: string };

// Intersection
type AdminType = User & { role: string };

// Union
type Status = 'active' | 'inactive' | 'pending';
```

### Q5: What are generics?
**A**: Generics allow you to write reusable code that works with multiple types.

```typescript
// Generic function
function identity<T>(value: T): T {
  return value;
}

identity<string>('hello'); // 'hello'
identity<number>(42); // 42

// Generic interface
interface Container<T> {
  value: T;
  getValue(): T;
}

// Generic class
class Stack<T> {
  private items: T[] = [];
  
  push(item: T): void {
    this.items.push(item);
  }
  
  pop(): T | undefined {
    return this.items.pop();
  }
}
```

### Q6: What is type inference?
**A**: TypeScript automatically determines types based on usage.

```typescript
let x = 5; // TypeScript infers: number
let arr = [1, 2, 3]; // TypeScript infers: number[]
let obj = { name: 'Alice', age: 30 }; // TypeScript infers: { name: string; age: number }

// Function return type inference
function add(a: number, b: number) {
  return a + b; // Return type inferred as number
}

// Contextual typing
const numbers = [1, 2, 3];
numbers.map(x => x * 2); // x inferred as number
```

---

## Type System

### Q7: What are union and intersection types?
**A**:

```typescript
// Union: OR (A | B)
type StringOrNumber = string | number;
type Status = 'active' | 'inactive' | 'pending';

// Intersection: AND (A & B)
type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged; // { name: string; age: number }
```

### Q8: What are literal types?
**A**:

```typescript
// String literal
type Direction = 'up' | 'down' | 'left' | 'right';

// Number literal
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;

// Boolean literal
type Success = true;

// Template literal
type HTTPMethod = `GET` | `POST` | `PUT` | `DELETE`;
type EventName = `on${string}`;
```

### Q9: What are discriminated unions?
**A**:

```typescript
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rectangle'; width: number; height: number }
  | { kind: 'triangle'; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    case 'triangle':
      return (shape.base * shape.height) / 2;
  }
}
```

### Q10: What are conditional types?
**A**:

```typescript
type IsString<T> = T extends string ? true : false;

type T1 = IsString<string>; // true
type T2 = IsString<number>; // false

// More complex
type ArrayOrSingle<T> = T extends any[] ? T : T[];

type T3 = ArrayOrSingle<number>; // number[]
type T4 = ArrayOrSingle<string[]>; // string[]
```

### Q11: What are mapped types?
**A**:

```typescript
// Make all properties optional
type Optional<T> = {
  [P in keyof T]?: T[P];
};

// Make all properties readonly
type Readonly<T> = {
  readonly [P in keyof T]: T[P];
};

// Pick specific properties
type Pick<T, K extends keyof T> = {
  [P in K]: T[P];
};
```

### Q12: What are template literal types?
**A**:

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<'click'>; // 'onClick'
type HoverEvent = EventName<'hover'>; // 'onHover'

// Complex template literals
type CSSProperty = `${string}-${string}`;
type Margin = `margin-${'top' | 'right' | 'bottom' | 'left'}`;
```

### Q13: What is the `infer` keyword?
**A**:

```typescript
// Extract function return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

function add(a: number, b: number): number { return a + b; }
type T1 = ReturnType<typeof add>; // number

// Extract function parameters
type Parameters<T> = T extends (...args: infer P) => any ? P : never;
type T2 = Parameters<typeof add>; // [a: number, b: number]

// Extract array element type
type ElementOf<T> = T extends (infer E)[] ? E : never;
type T3 = ElementOf<string[]>; // string
```

### Q14: What is the `keyof` operator?
**A**:

```typescript
interface User {
  id: number;
  name: string;
  email: string;
}

type UserKeys = keyof User; // 'id' | 'name' | 'email'

// Safe property access
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

const user: User = { id: 1, name: 'Alice', email: 'alice@example.com' };
getProperty(user, 'name'); // ✅ type: string
getProperty(user, 'age'); // ❌ Error
```

### Q15: What are utility types?
**A**:

```typescript
// Partial<T> — All properties optional
// Required<T> — All properties required
// Readonly<T> — All properties readonly
// Pick<T, K> — Select specific properties
// Omit<T, K> — Remove specific properties
// Record<K, V> — Object with keys K and values V
// Extract<T, U> — Extract types assignable to U
// Exclude<T, U> — Exclude types assignable to U
// NonNullable<T> — Remove null and undefined
// ReturnType<T> — Extract return type
// Parameters<T> — Extract parameter types
// Awaited<T> — Unwrap Promise type
```

---

## Generics

### Q16: What are generic constraints?
**A**:

```typescript
// Constrain generic to have certain properties
interface HasLength {
  length: number;
}

function logLength<T extends HasLength>(value: T): void {
  console.log(value.length);
}

logLength('hello'); // ✅
logLength([1, 2, 3]); // ✅
logLength(42); // ❌ Error: number doesn't have length

// Constrain to specific types
function create<T extends { new(): any }>(Constructor: T): InstanceType<T> {
  return new Constructor();
}
```

### Q17: What are generic utility types?
**A**:

```typescript
// Pick specific properties
type UserBasic = Pick<User, 'id' | 'name'>;

// Omit specific properties
type UserWithoutEmail = Omit<User, 'email'>;

// Record type
type UserMap = Record<string, User>;

// Partial type
type PartialUser = Partial<User>;

// Required type
type RequiredUser = Required<User>;
```

### Q18: What are conditional types with generics?
**A**:

```typescript
// Type-safe API response
type APIResponse<T> = T extends 'success'
  ? { data: any; status: 200 }
  : T extends 'error'
  ? { error: string; status: 400 | 500 }
  : never;

function handleResponse<T extends 'success' | 'error'>(
  response: APIResponse<T>
): void {
  // ...
}

handleResponse({ data: {}, status: 200 }); // ✅
handleResponse({ error: 'Not found', status: 404 }); // ❌ Invalid status
```

### Q19: What is the difference between generic constraints and conditional types?
**A**:

```typescript
// Generic constraint: Must satisfy interface
function process<T extends { name: string }>(value: T): void {
  console.log(value.name);
}

// Conditional type: Type-level logic
type IsString<T> = T extends string ? true : false;

// Constraint restricts WHAT can be passed
// Conditional type determines WHAT TYPE is returned
```

### Q20: What are generic inference patterns?
**A**:

```typescript
// Inference from function arguments
function createStore<T>(initial: T): { get: () => T; set: (v: T) => void } {
  let value = initial;
  return {
    get: () => value,
    set: (v) => { value = v; },
  };
}

const store = createStore({ count: 0, name: 'App' });
// Inferred: { get: () => { count: number; name: string }; set: (v: { count: number; name: string }) => void }

// Inference from generic function
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

const num = first([1, 2, 3]); // Inferred: number
const str = first(['a', 'b']); // Inferred: string
```

---

## OOP in TypeScript

### Q21: What are access modifiers?
**A**:

```typescript
class User {
  public name: string;      // Accessible everywhere
  private password: string;  // Accessible only in this class
  protected email: string;   // Accessible in this class and subclasses
  readonly id: number;       // Cannot be modified after initialization

  constructor(name: string, password: string, email: string, id: number) {
    this.name = name;
    this.password = password;
    this.email = email;
    this.id = id;
  }
}
```

### Q22: What are abstract classes?
**A**:

```typescript
abstract class Shape {
  abstract area(): number;
  abstract perimeter(): number;

  describe(): string {
    return `Area: ${this.area()}, Perimeter: ${this.perimeter()}`;
  }
}

class Circle extends Shape {
  constructor(private radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  perimeter(): number {
    return 2 * Math.PI * this.radius;
  }
}
```

### Q23: What are interfaces for classes?
**A**:

```typescript
interface Serializable {
  serialize(): string;
  deserialize(data: string): void;
}

interface Loggable {
  log(): void;
}

class User implements Serializable, Loggable {
  constructor(public name: string, public age: number) {}

  serialize(): string {
    return JSON.stringify(this);
  }

  deserialize(data: string): void {
    const obj = JSON.parse(data);
    this.name = obj.name;
    this.age = obj.age;
  }

  log(): void {
    console.log(`User: ${this.name}, Age: ${this.age}`);
  }
}
```

### Q24: What are parameter properties?
**A**:

```typescript
// Without parameter properties
class User {
  name: string;
  age: number;
  constructor(name: string, age: number) {
    this.name = name;
    this.age = age;
  }
}

// With parameter properties
class User {
  constructor(
    public name: string,
    public age: number,
    private id: string
  ) {}
  // Automatically creates and initializes properties
}
```

### Q25: What are mixins?
**A**:

```typescript
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();
  };
}

function Activatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    isActive = false;
    activate() { this.isActive = true; }
    deactivate() { this.isActive = false; }
  };
}

class BaseUser {
  constructor(public name: string) {}
}

const TimestampedUser = Timestamped(BaseUser);
const ActivatableUser = Activatable(BaseUser);
const FullUser = Activatable(Timestamped(BaseUser));

const user = new FullUser('Alice');
user.activate();
user.createdAt; // ✅
```

---

## Modules

### Q26: What are ES modules?
**A**:

```typescript
// math.ts
export function add(a: number, b: number): number {
  return a + b;
}

export const PI = 3.14159;

export default class Calculator {
  // ...
}

// main.ts
import Calculator, { add, PI } from './math';
import * as MathUtils from './math';
import { add as sum } from './math';
```

### Q27: What is the difference between named and default exports?
**A**:

```typescript
// Named export
export function add(a: number, b: number) { return a + b; }
export const PI = 3.14159;

// Default export
export default class Calculator { /* ... */ }

// Importing
import { add, PI } from './math';      // Named
import Calculator from './math';       // Default
import * as MathUtils from './math';   // Namespace
```

### Q28: What is `esModuleInterop`?
**A**:

```typescript
// Without esesModuleInterop:
import * as express from 'express';

// With esesModuleInterop:
import express from 'express';
// Also allows: import express = require('express');
```

### Q29: What is the difference between `import` and `require`?
**A**:

```typescript
// ES Module (static, tree-shakeable)
import { add } from './math';
import('dynamic-module').then(m => m.doSomething());

// CommonJS (dynamic, not tree-shakeable)
const math = require('./math');
const math = require(condition ? './a' : './b');
```

### Q30: What are barrel files?
**A**:

```typescript
// index.ts (barrel file)
export { add, subtract } from './math';
export { User, Product } from './models';

// Usage
import { add, User } from './index';
```

---

## Error Handling

### Q31: How do you handle errors in TypeScript?
**A**:

```typescript
// Typed errors
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number
  ) {
    super(message);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
  }
}

// Error handling pattern
function processUser(id: string): Result<User> {
  try {
    const user = findUser(id);
    if (!user) {
      return { success: false, error: new NotFoundError('User') };
    }
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error as AppError };
  }
}

// Result type
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: Error };
```

### Q32: What are try-catch types in TypeScript?
**A**:

```typescript
// TypeScript 4.4+ types catch variable as unknown
try {
  // ...
} catch (error) {
  // error is unknown by default
  if (error instanceof Error) {
    console.log(error.message);
  }
  
  // Or use a type guard
  function isError(error: unknown): error is Error {
    return error instanceof Error;
  }
  
  if (isError(error)) {
    console.log(error.message);
  }
}
```

---

## Async/Await

### Q33: How do you type async functions?
**A**:

```typescript
// Async function return type is automatically Promise<T>
async function fetchData(): Promise<User> {
  const response = await fetch('/api/user');
  return response.json();
}

// Promise types
type UserPromise = Promise<User>;

// Async iteration
async function* generateNumbers() {
  yield 1;
  yield 2;
  yield 3;
}

// Promise.all with types
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);
```

### Q34: What are async/await patterns?
**A**:

```typescript
// Sequential
const users = await fetchUsers();
const posts = await fetchPosts();

// Parallel
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
]);

// Error handling
async function safeFetch<T>(url: string): Promise<T | null> {
  try {
    const response = await fetch(url);
    return await response.json();
  } catch {
    return null;
  }
}

// Retry pattern
async function retry<T>(
  fn: () => Promise<T>,
  retries: number
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries <= 0) throw error;
    return retry(fn, retries - 1);
  }
}
```

---

## React + TypeScript

### Q35: How do you type React components?
**A**:

```typescript
// Function component
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
}

function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return <button onClick={onClick}>{label}</button>;
}

// With children
interface CardProps {
  title: string;
  children: React.ReactNode;
}

function Card({ title, children }: CardProps) {
  return <div><h2>{title}</h2>{children}</div>;
}
```

### Q36: How do you type hooks?
**A**:

```typescript
// useState with generic
const [count, setCount] = useState<number>(0);
const [user, setUser] = useState<User | null>(null);

// useRef
const inputRef = useRef<HTMLInputElement>(null);

// useContext
const theme = useContext(ThemeContext);

// Custom hook
function useLocalStorage<T>(key: string, initial: T): [T, (v: T) => void] {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initial;
  });

  const setStored = (newValue: T) => {
    setValue(newValue);
    localStorage.setItem(key, JSON.stringify(newValue));
  };

  return [value, setStored];
}
```

### Q37: How do you type event handlers?
**A**:

```typescript
function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
  console.log(event.target);
}

function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
  console.log(event.target.value);
}

function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
  event.preventDefault();
}
```

---

## Node.js + TypeScript

### Q38: How do you set up TypeScript for Node.js?
**A**:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Q39: How do you type Express routes?
**A**:

```typescript
import { Request, Response, NextFunction } from 'express';

// Typed request handler
function getUser(req: Request<{ id: string }>, res: Response<User>) {
  const user = findUser(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'Not found' });
  }
  res.json(user);
}

// Typed middleware
function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  next();
}

// Typed response
interface ApiResponse<T> {
  data?: T;
  error?: string;
}
```

### Q40: How do you type database queries?
**A**:

```typescript
// With Prisma
const user = await prisma.user.findUnique({
  where: { id: 1 },
  include: { posts: true },
});
// user: User & { posts: Post[] }

// With raw queries (typed manually)
interface User {
  id: number;
  name: string;
  email: string;
}

async function getUser(id: number): Promise<User | null> {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0] || null;
}
```

---

## Design Patterns

### Q41: How do you implement the Singleton pattern?
**A**:

```typescript
class Database {
  private static instance: Database;

  private constructor() {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  query(sql: string): any {
    // ...
  }
}
```

### Q42: How do you implement the Factory pattern?
**A**:

```typescript
interface User {
  name: string;
  role: string;
}

class UserFactory {
  static create(type: 'admin' | 'user', name: string): User {
    switch (type) {
      case 'admin':
        return { name, role: 'admin' };
      case 'user':
        return { name, role: 'user' };
    }
  }
}
```

### Q43: How do you implement the Observer pattern?
**A**:

```typescript
type Observer<T> = (data: T) => void;

class EventEmitter<T> {
  private observers = new Map<string, Observer<T>[]>();

  subscribe(event: string, observer: Observer<T>): () => void {
    if (!this.observers.has(event)) {
      this.observers.set(event, []);
    }
    this.observers.get(event)!.push(observer);

    return () => {
      const observers = this.observers.get(event);
      if (observers) {
        const index = observers.indexOf(observer);
        if (index > -1) observers.splice(index, 1);
      }
    };
  }

  emit(event: string, data: T): void {
    this.observers.get(event)?.forEach(observer => observer(data));
  }
}
```

---

## Performance

### Q44: How do you optimize TypeScript performance?
**A**:

```json
{
  "compilerOptions": {
    "incremental": true,
    "skipLibCheck": true,
    "isolatedModules": true,
    "noEmit": false
  }
}
```

Key optimizations:
- Use `incremental` for caching
- Use `skipLibCheck` to skip .d.ts checking
- Use `isolatedModules` for parallel transpilation
- Use project references for monorepos
- Use `import type` for type-only imports

### Q45: What is tree shaking?
**A**: Tree shaking removes unused exports from the final bundle. Requires ES module syntax and `sideEffects: false` in package.json.

```typescript
// Math.ts — only add and subtract are used
export function add(a: number, b: number) { return a + b; }
export function subtract(a: number, b: number) { return a - b; }
export function multiply(a: number, b: number) { return a * b; }

// main.ts
import { add, subtract } from './math'; // multiply is tree-shaken
```

### Q46: How do you reduce bundle size?
**A**:

1. Use tree shaking (ES modules)
2. Use `import type` for type-only imports
3. Avoid barrel files
4. Use dynamic imports for code splitting
5. Use `sideEffects: false` in package.json
6. Enable minification
7. Remove unused code and types

---

## Advanced

### Q47: What are type guards?
**A**:

```typescript
// typeof guard
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// instanceof guard
function isError(value: unknown): value is Error {
  return value instanceof Error;
}

// Custom type guard
interface User { name: string; age: number; }
interface Admin { name: string; role: string; }

function isAdmin(user: User | Admin): user is Admin {
  return 'role' in user;
}

// Usage
function process(user: User | Admin) {
  if (isAdmin(user)) {
    console.log(user.role); // ✅ TypeScript knows it's Admin
  }
}
```

### Q48: What are assertions?
**A**:

```typescript
// Type assertion
const value = someValue as string;
const element = document.getElementById('app') as HTMLDivElement;

// Non-null assertion
const element = document.getElementById('app')!;
element.classList.add('active');

// Type predicate
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

// Satisfies (TypeScript 4.9+)
const config = {
  port: 3000,
  host: 'localhost',
} satisfies Record<string, string | number>;
```

### Q49: What is declaration merging?
**A**:

```typescript
// Interface merging
interface User {
  name: string;
}
interface User {
  age: number;
}
// User = { name: string; age: number }

// Namespace merging
namespace Utils {
  export function add(a: number, b: number) { return a + b; }
}
namespace Utils {
  export function subtract(a: number, b: number) { return a - b; }
}

// Module augmentation
import express from 'express';
declare module 'express' {
  interface Request {
    userId?: string;
  }
}
```

### Q50: What is the difference between `type` and `interface` for extending?
**A**:

```typescript
// Interface extends (single inheritance)
interface A { a: string; }
interface B extends A { b: number; }

// Type intersection (multiple inheritance)
type A = { a: string; };
type B = A & { b: number; };

// Interface can't extend unions
interface C extends A | B { } // ❌ Error

// Type can use unions
type C = A | B; // ✅ OK
```

### Q51: How do you handle `this` in TypeScript?
**A**:

```typescript
// Using 'this' parameter
function greet(this: { name: string }) {
  console.log(`Hello, ${this.name}`);
}

const obj = { name: 'Alice', greet };
obj.greet(); // ✅

// Arrow functions capture 'this'
class Counter {
  count = 0;
  increment = () => {
    this.count++; // 'this' captured from constructor
  };
}

// Binding
const bound = greet.bind({ name: 'Alice' });
bound(); // ✅
```

### Q52: What is `satisfies` in TypeScript 4.9+?
**A**:

```typescript
// satisfies validates types without widening
const config = {
  port: 3000,
  host: 'localhost',
} satisfies Record<string, string | number>;

// config.port is number (not string | number)
console.log(config.port.toFixed(2)); // ✅

// Without satisfies
const config2 = {
  port: 3000,
  host: 'localhost',
} as Record<string, string | number>;

config2.port.toFixed(2); // ❌ Error: port is string | number
```
