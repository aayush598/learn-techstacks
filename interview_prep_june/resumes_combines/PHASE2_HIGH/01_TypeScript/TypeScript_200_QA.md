# TypeScript Interview Q&A — 200+ Questions (YC Startup Level)

> Detailed answers with code examples. Covers fundamentals, advanced patterns, React integration, and tooling.

---

## Table of Contents

- [TypeScript Fundamentals (Q1–Q80)](#typescript-fundamentals-q1-q80)
- [Advanced TypeScript (Q81–Q140)](#advanced-typescript-q81-q140)
- [TypeScript with React (Q141–Q180)](#typescript-with-react-q141-q180)
- [TypeScript Configuration & Tooling (Q181–Q200)](#typescript-configuration--tooling-q181-q200)

---

# TypeScript Fundamentals (Q1–Q80)

### Q1: What is TypeScript? Why use it over JavaScript?

**TypeScript is a strict superset of JavaScript that adds optional static typing, interfaces, generics, and modern ECMAScript features. It compiles to plain JavaScript.**

**Why use it:**
- Catch bugs at compile time instead of runtime
- Better IDE support (autocomplete, refactoring, navigation)
- Self-documenting code through types
- Enables large-scale codebase maintenance
- Gradual adoption (any JavaScript is valid TypeScript)

```typescript
function add(a: number, b: number): number {
  return a + b;
}
add(1, "2"); // Error: Argument of type 'string' is not assignable to parameter of type 'number'
```

### Q2: TypeScript vs JavaScript — key differences

| Feature | JavaScript | TypeScript |
|---|---|---|
| Typing | Dynamic | Static optional |
| Compilation | Interpreted | Compiles to JS |
| Interfaces | Not supported | Supported |
| Generics | Not supported | Supported |
| Enums | Not supported | Supported |
| Null checking | Runtime | Compile-time with strictNullChecks |
| Learning curve | Low | Moderate |

### Q3: How TypeScript compiles — tsc and tsconfig.json

`tsc` compiles `.ts` to `.js`. Configuration lives in `tsconfig.json`.

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

### Q4: Basic types — string, number, boolean, null, undefined, void, never, any, unknown

```typescript
const name: string = "Alice";
const age: number = 30;
const isActive: boolean = true;
const nothing: null = null;
const notDefined: undefined = undefined;

function log(msg: string): void {
  console.log(msg);
}

function throwError(msg: string): never {
  throw new Error(msg);
}

let data: any = 42;
data = "hello";

let input: unknown = JSON.parse('{"name":"Alice"}');
```

### Q5: any vs unknown — when to use each?

**`any`**: Opts out completely. No type checking. Avoid.

**`unknown`**: Safe counterpart of `any`. Must narrow before use.

```typescript
function parseAny(data: any): string {
  return data.name.toUpperCase(); // runtime crash if no name
}

function parseUnknown(data: unknown): string {
  if (typeof data === "object" && data !== null && "name" in data) {
    return (data as { name: string }).name.toUpperCase();
  }
  return "UNKNOWN";
}
```

### Q6: Type inference vs type annotations

**Inference**: TypeScript deduces types from values.
**Annotations**: You explicitly write the type.

```typescript
let count = 0;           // inferred number
const name = "Alice";    // inferred "Alice" (literal)

function greet(name: string): string {  // annotation on params
  return `Hello ${name}`;
}
```

### Q7: Interfaces vs Types — when to use which?

**Interfaces** — Prefer for object shapes, public APIs. Can be extended/merged.

**Types** — Use for unions, intersections, primitives, tuples, computed properties.

```typescript
interface User { name: string; email: string; }
interface User { age?: number; } // declaration merging

type Status = "active" | "inactive";
type Point = [number, number];

interface Admin extends User { role: "admin"; }
type AdminType = User & { role: "admin" };
```

### Q8: Optional properties, readonly properties

```typescript
interface Config {
  readonly id: string;
  name: string;
  description?: string;
}

const config: Config = { id: "abc", name: "My Config" };
// config.id = "xyz"; // Error: readonly
config.name = "New Name"; // OK
```

### Q9: Union types, Intersection types, Literal types

```typescript
type Status = "success" | "error" | "loading";
type Result = string | number | boolean;

type Named = { name: string };
type Aged = { age: number };
type Person = Named & Aged;

type Direction = "north" | "south" | "east" | "west";
type DiceRoll = 1 | 2 | 3 | 4 | 5 | 6;
```

### Q10: Type aliases vs interfaces — detailed comparison

- **Merging**: Interfaces merge; types cannot.
- **Extends**: Interfaces use `extends`; types use `&`.
- **Computed properties**: Only types support mapped types.
- **Performance**: Interfaces are faster for the compiler.

### Q11: Extending interfaces, extending types

```typescript
interface Base { id: string; }
interface User extends Base { name: string; }
interface Product extends Base, Timestamp { price: number; }

type BaseType = { id: string; };
type UserType = BaseType & { name: string; };
```

### Q12: implements vs extends

- **`extends`**: Class inherits implementation from another class.
- **`implements`**: Class promises to satisfy a contract (interface). No code inherited.

```typescript
interface Flyable { fly(): void; }
abstract class Animal { abstract makeSound(): void; }
class Bird extends Animal implements Flyable {
  makeSound() { console.log("chirp"); }
  fly() { console.log("flying"); }
}
```

### Q13: Generics — basic, constraints, multiple, default types

```typescript
function identity<T>(arg: T): T { return arg; }

function getLength<T extends { length: number }>(arg: T): number {
  return arg.length;
}

function pair<A, B>(a: A, b: B): [A, B] { return [a, b]; }

function createArray<T = string>(length: number, value: T): T[] {
  return Array(length).fill(value);
}
```

### Q14: Generic functions, interfaces, classes

```typescript
function first<T>(arr: T[]): T | undefined { return arr[0]; }

interface Repository<T> {
  getById(id: string): T | undefined;
  save(item: T): void;
}

class Stack<T> {
  private items: T[] = [];
  push(item: T) { this.items.push(item); }
  pop(): T | undefined { return this.items.pop(); }
}
```

### Q15: keyof operator

`keyof T` yields a union of all property keys of `T`.

```typescript
interface User { name: string; age: number; email: string; }
type UserKeys = keyof User; // "name" | "age" | "email"

function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}
```

### Q16: typeof operator in type context

Extracts the type of a value.

```typescript
const config = { apiUrl: "https://api.com", timeout: 5000 };
type Config = typeof config;
// { apiUrl: string; timeout: number; }

function getUser() { return { id: "1", name: "Alice" }; }
type User = ReturnType<typeof getUser>;
```

### Q17: Conditional types (T extends U ? X : Y)

```typescript
type IsString<T> = T extends string ? true : false;
type A = IsString<"hello">; // true
type B = IsString<number>;  // false

type NonNullable<T> = T extends null | undefined ? never : T;
type C = NonNullable<string | null | undefined>; // string
```

### Q18: Mapped types

Transform every property of a type.

```typescript
type Readonly<T> = { readonly [K in keyof T]: T[K]; };
type Optional<T> = { [K in keyof T]?: T[K]; };
type Mutable<T> = { -readonly [K in keyof T]: T[K]; };
type Required<T> = { [K in keyof T]-?: T[K]; };
```

### Q19: Utility types — Partial, Required, Readonly, Pick, Omit, Record, Exclude, Extract, NonNullable, ReturnType, Parameters, Awaited

```typescript
interface User { id: string; name: string; email: string; age: number; }

const partialUser: Partial<User> = { name: "Alice" };
type UserBasic = Pick<User, "id" | "name">;
type UserWithoutEmail = Omit<User, "email">;

type PageInfo = Record<string, { title: string; url: string }>;

type Status = "active" | "inactive" | "pending";
type ActiveStatus = Exclude<Status, "inactive" | "pending">;
type T1 = Extract<"a" | "b" | "c", "a" | "f">; // "a"

type T2 = NonNullable<string | null | undefined>; // string
type PromiseResult = Awaited<Promise<string>>; // string
```

### Q20: Template literal types

```typescript
type EventName = "click" | "focus" | "blur";
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

type Loud = Uppercase<"hello">; // "HELLO"
type Cap = Capitalize<"hello">; // "Hello"
```

### Q21: Enums — numeric vs string vs const enums

```typescript
enum Direction { Up, Down, Left, Right } // 0,1,2,3
enum Color { Red = "RED", Green = "GREEN", Blue = "BLUE" }

const enum HttpMethod { GET = "GET", POST = "POST" }
const method = HttpMethod.GET; // compiles to: "GET"
```

### Q22: Tuple types, labeled tuples, rest elements

```typescript
type Pair = [string, number];
type Range = [start: number, end: number];
type OptTuple = [string, number?];
type Variadic = [string, ...number[], boolean];

function concat<T extends unknown[], U extends unknown[]>(
  arr1: [...T], arr2: [...U]
): [...T, ...U] {
  return [...arr1, ...arr2];
}
```

### Q23: Type assertions (as vs angle bracket)

```typescript
const value: unknown = "hello";
const length = (value as string).length;

const input = document.getElementById("email") as HTMLInputElement;
const data = JSON.parse('{"name":"Alice"}') as { name: string };
```

### Q24: Non-null assertion operator (!)

```typescript
const el = document.getElementById("elementId")!;
el.innerHTML = "Hello";

type User = { name?: string };
function greet(user: User) {
  console.log(user.name!.toUpperCase()); // risky
}
```

### Q25: Definite assignment assertion (!:)

```typescript
class MyComponent {
  name!: string;
  age!: number;

  constructor() { this.init(); }

  init() {
    this.name = "Alice";
    this.age = 30;
  }
}
```

### Q26: const assertions

```typescript
const roles = ["admin", "user", "guest"] as const;
// type: readonly ["admin", "user", "guest"]

const config = { apiUrl: "https://api.com", timeout: 5000 } as const;

type Role = (typeof roles)[number]; // "admin" | "user" | "guest"
```

### Q27: satisfies operator (TS 4.9+)

Checks a value conforms to a type without widening the type.

```typescript
const palette = {
  primary: "blue",
  secondary: "red",
} satisfies Record<string, string>;

palette.primary; // type is "blue" (literal), not string
```

### Q28: Index signatures

```typescript
interface StringMap {
  [key: string]: string;
}

interface Config {
  [key: string]: string | number;
  port: number;
  host: string;
}
```

### Q29: Call signatures, construct signatures

```typescript
type AddFn = {
  (a: number, b: number): number;
  description: string;
};

type PointConstructor = {
  new (x: number, y: number): { x: number; y: number };
};
```

### Q30: Function overloads

```typescript
function reverse(value: string): string;
function reverse<T>(value: T[]): T[];
function reverse<T>(value: string | T[]): string | T[] {
  if (typeof value === "string") return value.split("").reverse().join("");
  return value.slice().reverse();
}
```

### Q31: this parameter in functions

```typescript
function greet(this: { name: string }) {
  console.log(`Hello, ${this.name}`);
}

const obj = { name: "Alice", greet };
obj.greet();
// greet(); // Error: this is undefined
```

### Q32: typeof and instanceof type guards

```typescript
function format(value: string | number): string {
  if (typeof value === "string") return value.toUpperCase();
  return value.toFixed(2);
}

class Animal {}
class Dog extends Animal { bark() {} }

function handle(a: Animal) {
  if (a instanceof Dog) a.bark();
}
```

### Q33: User-defined type guards (value is Type)

```typescript
interface Fish { swim(): void; }
interface Bird { fly(): void; }

function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}

function move(pet: Fish | Bird) {
  if (isFish(pet)) pet.swim();
  else pet.fly();
}

function isDefined<T>(value: T | undefined): value is T {
  return value !== undefined;
}
const items: (number | undefined)[] = [1, undefined, 3];
const defined = items.filter(isDefined); // number[]
```

### Q34: in operator narrowing

```typescript
interface Admin { permissions: string[]; }
interface User { email: string; }

function handle(account: Admin | User) {
  if ("permissions" in account) {
    console.log(account.permissions.join(", "));
  } else {
    console.log(account.email);
  }
}
```

### Q35: Discriminated unions

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    case "triangle": return (shape.base * shape.height) / 2;
  }
}

type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };
```

### Q36: never type and exhaustive checks

```typescript
function throwError(msg: string): never { throw new Error(msg); }

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    default: {
      const _exhaustive: never = shape;
      return _exhaustive;
    }
  }
}
```

### Q37: Module system (import/export)

```typescript
// utils.ts
export function add(a: number, b: number): number { return a + b; }
export default class Logger { log(msg: string) { console.log(msg); } }

// Import
import Logger, { add } from "./utils";
import type { User } from "./types";
import { type User, type Config, createUser } from "./types";

// Dynamic import
async function loadModule() {
  const module = await import("./utils");
}
```

### Q38: Ambient declarations (.d.ts files)

```typescript
// globals.d.ts
declare const API_KEY: string;

declare module "my-lib" {
  export function doSomething(value: string): number;
  export const VERSION: string;
}

interface Window {
  __INITIAL_STATE__: Record<string, unknown>;
}
```

### Q39: Triple-slash directives

```typescript
/// <reference path="./other-types.d.ts" />
/// <reference types="node" />
/// <reference lib="es2020" />
/// <reference types="vite/client" />
```

### Q40: tsconfig.json key options

```json
{
  "compilerOptions": {
    "strict": true,
    "strictNullChecks": true,
    "noImplicitAny": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true,
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "node",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] },
    "outDir": "./dist",
    "rootDir": "./src",
    "declaration": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "isolatedModules": true,
    "skipLibCheck": true,
    "resolveJsonModule": true
  }
}
```

### Q41: Declaration merging

```typescript
interface Box { width: number; }
interface Box { height: number; }
// Box has both width and height

namespace MyNamespace {
  export interface Config { debug: boolean; }
}
namespace MyNamespace {
  export function init(): void {}
}

enum Color { Red = "RED" }
enum Color { Blue = "BLUE" }
```

### Q42: Namespaces vs modules

| Aspect | Namespaces | Modules |
|---|---|---|
| Syntax | `namespace X {}` | `import/export` |
| Scope | Global | File-based |
| Use case | Legacy code | Modern code |
| Recommendation | Avoid | Always prefer |

### Q43: What is the difference between interface and type for objects?

```typescript
interface Person { name: string; age: number; }
type Person = { name: string; age: number; };
// Use interface for objects (merging, extends). Type for unions/intersections.
```

### Q44: How to create type-safe Object.entries?

```typescript
function entries<T extends Record<string, unknown>>(obj: T): [keyof T, T[keyof T]][] {
  return Object.entries(obj) as any;
}
```

### Q45: What does `keyof any` resolve to?

```typescript
type T = keyof any; // string | number | symbol
```

### Q46: What is the difference between `readonly` and `Readonly<T>`?

`readonly` is a property modifier. `Readonly<T>` makes all properties readonly.

### Q47: Explain the `never` type

`never` is the bottom type. Used for:
- Functions that never return (throw, infinite loop)
- Exhaustive conditionals
- Removing members from union types via conditional types

### Q48: What is the `unknown` type?

Safe counterpart of `any`. Forces narrowing before use.

```typescript
let u: unknown = "hello";
// u.toFixed(); // Error: Object is of type 'unknown'
```

### Q49: What is `infer` in conditional types?

```typescript
type Return<T> = T extends (...args: any[]) => infer R ? R : never;
```

### Q50: How to create a type that extracts promise value?

```typescript
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type A = Unwrap<Promise<string>>; // string
```

### Q51: How to make all properties mutable?

```typescript
type Mutable<T> = { -readonly [K in keyof T]: T[K] };
```

### Q52: How to pick properties of a certain type?

```typescript
type PickByType<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};
```

### Q53: What is `exactOptionalPropertyTypes`?

Prevents `undefined` from being assigned to optional properties—they can only be missing.

### Q54: What does `skipLibCheck` do?

Skips type checking of declaration files (`.d.ts`). Speeds up compilation.

### Q55: What is `esModuleInterop`?

Enables better interop between CommonJS and ES Modules, allowing default imports from CJS modules.

### Q56: What is `isolatedModules`?

Ensures each file can be safely transpiled in isolation (required by Babel, esbuild).

### Q57: What is `resolveJsonModule`?

Allows importing `.json` files directly.

```typescript
import data from "./data.json";
```

### Q58: What is `declaration` in tsconfig?

Generates `.d.ts` files alongside compiled JS.

### Q59: What is `moduleResolution`?

How TypeScript resolves module imports. Options: `classic`, `node`, `node16`, `nodenext`, `bundler`.

### Q60: What is `target` vs `module`?

- `target`: output JS version (e.g., ES2020)
- `module`: module code generation (e.g., ESNext, CommonJS)

### Q61: What is `strict` mode?

Enables all strict checking:
- strictNullChecks, noImplicitAny, strictFunctionTypes
- strictBindCallApply, strictPropertyInitialization
- noImplicitThis, alwaysStrict

### Q62: What is `noUnusedLocals`?

Errors on unused local variables.

### Q63: What is `noUnusedParameters`?

Errors on unused function parameters.

### Q64: What is `forceConsistentCasingInFileNames`?

Ensures file names are referenced with consistent casing.

### Q65: What is `rootDir`?

Root directory of input TS files. Output structure mirrors input relative to rootDir.

### Q66: What is `outDir`?

Output directory for compiled JavaScript files.

### Q67: What is `sourceMap`?

Generates `.map` files for debugging TS in browser dev tools.

### Q68: What is `baseUrl` and `paths`?

Allows non-relative imports like `import { Button } from "@/components/Button"`.

### Q69: What is `allowJs`?

Allows TS files to import JS files.

### Q70: What is `lib` in tsconfig?

Specifies type definition libraries to include (e.g., `"ES2020"`, `"DOM"`).

### Q71: What are rest parameters in function types?

```typescript
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### Q72: What is destructuring in TypeScript?

```typescript
const user = { name: "Alice", age: 30, email: "a@b.com" };
const { name, ...rest } = user;
// name: string, rest: { age: number; email: string }
```

### Q73: What is the spread operator in TypeScript?

```typescript
const defaults = { timeout: 5000, retries: 3 };
const config = { ...defaults, url: "https://api.com" };
```

### Q74: How to make a type that requires at least one property?

```typescript
type AtLeastOne<T, U = { [K in keyof T]: Pick<T, K> }> = Partial<T> & U[keyof U];
```

### Q75: What does `Satisfies` keyword best used for?

Validating a value against a type without changing its inferred type.

### Q76: What is `ES2020` target?

Compiles to ES2020 JS — supports optional chaining, nullish coalescing, Promise.allSettled.

### Q77: What is the `as const` suffix?

Makes values deeply readonly and infers literal types.

```typescript
const cities = ["NYC", "LA"] as const;
// type: readonly ["NYC", "LA"]
```

### Q78: What is a branded type?

Simulates nominal typing in TypeScript's structural type system.

```typescript
type Brand<T, B> = T & { __brand: B };
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;
```

### Q79: What is the difference between `never` and `void`?

`void` means the function returns undefined. `never` means the function never returns (throws or infinite loop).

### Q80: What is the `NoInfer` utility type (TS 5.4+)?

Prevents TypeScript from inferring a type from a specific position.

```typescript
function create<T extends string>(items: T[], filter: NoInfer<T>): T[] {
  return items.filter((item) => item !== filter);
}
```

---

# Advanced TypeScript (Q81–Q140)

### Q81: Decorators

```typescript
function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class MyClass { method() {} }

function log(target: Object, propertyKey: string, descriptor: PropertyDescriptor) {
  const original = descriptor.value;
  descriptor.value = function (...args: unknown[]) {
    console.log(`Calling ${propertyKey} with`, args);
    return original.apply(this, args);
  };
}

class Calculator {
  @log
  add(a: number, b: number) { return a + b; }
}
```

### Q82: Decorator factories

```typescript
function throttle(delay: number) {
  return (target: Object, propertyKey: string, descriptor: PropertyDescriptor) => {
    const original = descriptor.value;
    let lastCall = 0;
    descriptor.value = function (...args: unknown[]) {
      const now = Date.now();
      if (now - lastCall >= delay) {
        lastCall = now;
        return original.apply(this, args);
      }
    };
  };
}

class SearchService {
  @throttle(300)
  search(query: string) { console.log(`Searching: ${query}`); }
}
```

### Q83: Abstract classes vs interfaces

```typescript
abstract class Animal {
  constructor(protected name: string) {}
  abstract makeSound(): void;
  move(): void { console.log(`${this.name} moving`); }
}

interface Flyable { fly(): void; }

class Duck extends Animal implements Flyable {
  constructor(name: string) { super(name); }
  makeSound() { console.log("Quack!"); }
  fly() { console.log("Flying"); }
}
```

### Q84: Mixins

```typescript
type Constructor<T = {}> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
    updatedAt = new Date();
    touch() { this.updatedAt = new Date(); }
  };
}

function Activatable<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    isActive = false;
    activate() { this.isActive = true; }
    deactivate() { this.isActive = false; }
  };
}

class BaseEntity {
  id: string;
  constructor(id: string) { this.id = id; }
}

class User extends Timestamped(Activatable(BaseEntity)) {
  constructor(id: string, public name: string) { super(id); }
}

const user = new User("1", "Alice");
user.createdAt; // Date
user.isActive;  // boolean
user.activate();
```

### Q85: Brand/branded types (nominal typing)

```typescript
type Brand<T, B> = T & { __brand: B };
type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function getUserById(id: UserId) {}
function getOrderById(id: OrderId) {}

const userId = "abc123" as UserId;
getUserById(userId);
// getUserById(orderId); // Error
```

### Q86: satisfies operator (deep dive)

```typescript
type Colors = "red" | "green" | "blue";

const palette = {
  primary: "blue",
  secondary: "red",
} satisfies Record<string, Colors>;

palette.primary; // type: "blue" (literal)
// palette.tertiary; // Error: not in type
```

### Q87: Variadic tuple types

```typescript
type Arr = readonly unknown[];
function concat<T extends Arr, U extends Arr>(a: T, b: U): [...T, ...U] {
  return [...a, ...b];
}

const result = concat([1, 2] as const, ["a", "b"] as const);
// readonly [1, 2, "a", "b"]
```

### Q88: Template literal types with inference

```typescript
type ExtractId<T extends string> =
  T extends `${infer Prefix}_${infer Id}_${infer Suffix}`
    ? { prefix: Prefix; id: Id; suffix: Suffix }
    : never;

type Test = ExtractId<"user_abc123_active">;
// { prefix: "user"; id: "abc123"; suffix: "active" }
```

### Q89: Recursive conditional types

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

type JSONValue =
  | string | number | boolean | null
  | JSONValue[]
  | { [key: string]: JSONValue };
```

### Q90: Mapped types with key remapping (as clause)

```typescript
type RemoveFunctions<T> = {
  [K in keyof T as T[K] extends Function ? never : K]: T[K];
};

type AddPrefix<T, P extends string> = {
  [K in keyof T as `${P}${Capitalize<string & K>}`]: T[K];
};

type Getters<T> = {
  [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K];
};
```

### Q91: satisfies vs as

```typescript
// 'as' — assert/override (can be unsafe)
const num = 42 as unknown as string;

// 'satisfies' — validate without changing inferred type
const palette = {
  primary: "red",
} satisfies Record<string, string>;

palette.primary; // type: "red" (literal), not string
```

### Q92: infer keyword

```typescript
type ReturnType<T> = T extends (...args: unknown[]) => infer R ? R : never;
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type ElementType<T> = T extends (infer U)[] ? U : never;
type Params<T> = T extends (...args: infer P) => unknown ? P : never;
type DeepPromise<T> = T extends Promise<infer U> ? DeepPromise<U> : T;
```

### Q93: Distributive conditional types

```typescript
// Naked type parameter distributes over unions
type ToArray<T> = T extends unknown ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]

// Wrapped — does not distribute
type ToArrayNonDist<T> = [T] extends [unknown] ? T[] : never;
type Result2 = ToArrayNonDist<string | number>; // (string | number)[]

type NonNullable<T> = T extends null | undefined ? never : T;
```

### Q94: Covariance and contravariance

```typescript
class Animal { name = ""; }
class Dog extends Animal { bark() {} }

const dogs: Dog[] = [new Dog()];
const animals: Animal[] = dogs; // covariant (arrays)

// Function parameters: contravariant with strictFunctionTypes
type AnimalHandler = (animal: Animal) => void;
type DogHandler = (dog: Dog) => void;

let animalHandler: AnimalHandler = (a) => {};
let dogHandler: DogHandler = (d) => {};

// dogHandler = animalHandler; // OK (contravariance)
// animalHandler = dogHandler; // Error with strictFunctionTypes
```

### Q95: Function parameter bivariance

Methods are bivariant (both co- and contravariance allowed). Function properties are contravariant with strictFunctionTypes.

```typescript
interface Handler { handle(animal: Animal): void; } // method = bivariant
interface HandlerFn { handle: (animal: Animal) => void; } // function = contravariant
```

### Q96: strictFunctionTypes effect

Makes function parameter types contravariant, preventing unsound assignments.

```typescript
type Fn = (x: { name: string }) => void;
type FnNarrow = (x: { name: string; extra: number }) => void;

let fn: Fn = (x) => {};
// fn = (x: { name: string; extra: number }) => {}; // Error with strictFunctionTypes
```

### Q97: Module resolution

```json
{
  "compilerOptions": {
    "moduleResolution": "node",
    "module": "ESNext"
  }
}
```

- `node`: Classic Node.js resolution
- `node16`/`nodenext`: Respects package.json exports
- `bundler`: For Vite, webpack, esbuild

### Q98: Path mapping

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"]
    }
  }
}
```

### Q99: Project references

Split large codebases into smaller projects.

```json
{
  "references": [
    { "path": "./packages/core" },
    { "path": "./packages/app" }
  ],
  "files": []
}
```

### Q100: Type-only imports

```typescript
import type { User } from "./types";
import { type User, type Config, createUser } from "./types";
// No runtime code generated for type-only imports
```

### Q101: const type parameters (TS 5.0+)

```typescript
function tuple<const T extends readonly unknown[]>(...items: T): T {
  return items;
}

const nums = tuple(1, 2, 3);
// type: readonly [1, 2, 3]
```

### Q102: satisfies with exactOptionalPropertyTypes

```typescript
// exactOptionalPropertyTypes: prevents undefined assignment to optional props
interface User { name: string; age?: number; }
// age can be missing but NOT explicitly undefined
```

### Q103: Assertion functions

```typescript
function assert(condition: unknown, msg?: string): asserts condition {
  if (!condition) throw new Error(msg ?? "Assertion failed");
}

function assertIsDefined<T>(value: T): asserts value is NonNullable<T> {
  if (value === null || value === undefined) throw new Error("Not defined");
}

function process(value: unknown) {
  assert(typeof value === "string");
  value.toUpperCase(); // narrowed to string
}
```

### Q104: async/await with TypeScript

```typescript
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) throw new Error(response.statusText);
  return response.json();
}

type AsyncResult<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function safeFetch<T>(url: string): Promise<AsyncResult<T>> {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

### Q105: Error handling patterns (typed errors)

```typescript
class NotFoundError extends Error {
  constructor(public resource: string, public id: string) {
    super(`${resource} ${id} not found`);
    this.name = "NotFoundError";
  }
}

class ValidationError extends Error {
  constructor(public field: string, message: string) {
    super(`Invalid ${field}: ${message}`);
    this.name = "ValidationError";
  }
}

type AppError = NotFoundError | ValidationError;

try {
  throw new NotFoundError("User", "123");
} catch (error) {
  if (error instanceof NotFoundError) {
    console.log(`Missing ${error.resource}`);
  } else if (error instanceof ValidationError) {
    console.log(`Invalid ${error.field}`);
  }
}

type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };
```

### Q106: satisfies with Record and mapped types

```typescript
const palette = {
  red: "#ff0000",
  green: "#00ff00",
} satisfies Record<string, string>;
```

### Q107: Using never for filtered mapped types

```typescript
type FunctionPropertyNames<T> = {
  [K in keyof T]: T[K] extends Function ? K : never;
}[keyof T];

type FunctionProperties<T> = Pick<T, FunctionPropertyNames<T>>;
type NonFunctionProperties<T> = Omit<T, FunctionPropertyNames<T>>;
```

### Q108: Branded types for compile-time safety

```typescript
type Email = string & { readonly __brand: "email" };

function createEmail(value: string): Email {
  if (!value.includes("@")) throw new Error("Invalid email");
  return value as Email;
}

function sendEmail(to: Email, subject: string) {
  console.log(`Sending to ${to}: ${subject}`);
}
```

### Q109: ReadonlyArray / readonly tuples

```typescript
const arr: readonly number[] = [1, 2, 3];
// arr.push(4); // Error

const tuple: readonly [string, number] = ["hello", 42];

type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
```

### Q110: Exhaustive type checking with never

```typescript
function assertNever(value: never): never {
  throw new Error(`Unexpected: ${JSON.stringify(value)}`);
}

type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "rectangle"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "rectangle": return shape.width * shape.height;
    default: return assertNever(shape);
  }
}
```

### Q111: Intersection types with generics

```typescript
function merge<T extends Record<string, unknown>, U extends Record<string, unknown>>(
  obj1: T, obj2: U
): T & U {
  return { ...obj1, ...obj2 };
}
```

### Q112: Self-referential/generic recursion

```typescript
interface TreeNode<T> {
  value: T;
  children?: TreeNode<T>[];
}

type NestedArray<T> = T | NestedArray<T>[];
```

### Q113: Extract and Exclude with conditional types

```typescript
type Status = "active" | "inactive" | "pending" | "deleted";
type ActiveStatuses = Exclude<Status, "deleted" | "inactive">; // "active" | "pending"
type StringsOnly = Extract<string | number | boolean, string>; // string
```

### Q114: NonNullable and Nullish handling

```typescript
type Maybe = string | null | undefined;
type Definitely = NonNullable<Maybe>; // string

function isNonNull<T>(value: T): value is NonNullable<T> {
  return value !== null && value !== undefined;
}
```

### Q115: ReturnType and Parameters utilities

```typescript
function createUser(name: string, age: number) {
  return { id: crypto.randomUUID(), name, age, createdAt: new Date() };
}

type CreateUserReturn = ReturnType<typeof createUser>;
type CreateUserParams = Parameters<typeof createUser>; // [string, number]
```

### Q116: Awaited type

```typescript
type A = Awaited<Promise<string>>; // string
type B = Awaited<Promise<Promise<number>>>; // number
type C = Awaited<string | Promise<number>>; // string | number
```

### Q117: String manipulation utility types

```typescript
type Upper = Uppercase<"hello">; // "HELLO"
type Lower = Lowercase<"HELLO">; // "hello"
type Cap = Capitalize<"hello">;  // "Hello"
type Uncap = Uncapitalize<"Hello">; // "hello"
```

### Q118: Conditional type inference with overloads

```typescript
function overloaded(value: string): number;
function overloaded(value: number): string;
function overloaded(value: string | number): string | number {
  return typeof value === "string" ? value.length : String(value);
}

type OverloadedType = typeof overloaded;
// ((value: string) => number) & ((value: number) => string)
```

### Q119: Mapped types with as for filtering

```typescript
type PickByType<T, V> = {
  [K in keyof T as T[K] extends V ? K : never]: T[K];
};

type OmitByType<T, V> = {
  [K in keyof T as T[K] extends V ? never : K]: T[K];
};
```

### Q120: Constructor parameters and instance types

```typescript
class Service {
  constructor(
    private apiUrl: string,
    private timeout: number = 5000
  ) {}
}

type ServiceParams = ConstructorParameters<typeof Service>;
type ServiceInstance = InstanceType<typeof Service>;
```

### Q121: this type in classes

```typescript
class QueryBuilder {
  constructor(private query: string[] = []) {}

  select(fields: string[]): this {
    this.query.push(`SELECT ${fields.join(", ")}`);
    return this;
  }

  from(table: string): this {
    this.query.push(`FROM ${table}`);
    return this;
  }

  build(): string { return this.query.join(" "); }
}

class ExtendedQueryBuilder extends QueryBuilder {
  orderBy(field: string, dir: "ASC" | "DESC" = "ASC"): this {
    this.query.push(`ORDER BY ${field} ${dir}`);
    return this;
  }
}
```

### Q122: Polymorphic this with generics

```typescript
abstract class Model {
  abstract getAttributes(): Record<string, unknown>;
  toJSON(this: this): ReturnType<this["getAttributes"]> {
    return this.getAttributes() as ReturnType<this["getAttributes"]>;
  }
}

class User extends Model {
  constructor(public id: string, public name: string) { super(); }
  getAttributes() { return { id: this.id, name: this.name }; }
}
```

### Q123: Class type from constructor

```typescript
type Constructor<T> = new (...args: any[]) => T;

function withLogging<T extends Constructor<object>>(Base: T) {
  return class extends Base {
    constructor(...args: any[]) {
      super(...args);
      console.log(`Created ${Base.name}`);
    }
  };
}
```

### Q124: Key remapping with template literals

```typescript
type AddPrefix<T, P extends string> = {
  [K in keyof T & string as `${P}_${K}`]: T[K];
};

type Getters<T> = {
  [K in keyof T & string as `get${Capitalize<K>}`]: () => T[K];
};
```

### Q125: Deep partial, required, readonly

```typescript
type DeepPartial<T> = T extends object
  ? { [K in keyof T]?: DeepPartial<T[K]> }
  : T;

type DeepRequired<T> = T extends object
  ? { [K in keyof T]-?: DeepRequired<T[K]> }
  : T;

type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
```

### Q126: Function overloads with generics

```typescript
function process<T extends string>(input: T): T[];
function process<T extends number>(input: T): T;
function process<T extends boolean>(input: T): boolean;
function process(input: any): any {
  if (typeof input === "string") return [input];
  if (typeof input === "number") return input;
  return !input;
}
```

### Q127: Intersection of discriminated unions

```typescript
type SuccessResponse = { status: "success"; data: unknown; };
type ErrorResponse = { status: "error"; error: { code: number; message: string; }; };
type CommonProps = SuccessResponse & ErrorResponse;
// { status: never; } — "success" & "error" = never
```

### Q128: Recursive type aliases

```typescript
type JSONValue =
  | string | number | boolean | null
  | JSONValue[]
  | { [key: string]: JSONValue };

type Tree<T> = { value: T; children?: Tree<T>[]; };

type LinkedList<T> = { value: T; next?: LinkedList<T>; };
```

### Q129: Intersection with mapped conditional types

```typescript
type Combine<T, U> = {
  [K in keyof T | keyof U]: K extends keyof T
    ? K extends keyof U ? T[K] | U[K] : T[K]
    : K extends keyof U ? U[K] : never;
};
```

### Q130: Branded types with generics

```typescript
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId = Brand<string, "UserId">;
type Meters = Brand<number, "Meters">;
type Seconds = Brand<number, "Seconds">;

function speed(distance: Meters, time: Seconds): number {
  return (distance / time);
}
```

### Q131: Indexed access types with key remapping

```typescript
type ValuesOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? T[K] : never;
}[keyof T];

type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];
```

### Q132: Mapped types with tuples

```typescript
type MapTuple<T extends readonly unknown[], U> = {
  [K in keyof T]: U;
};

type Mapped = MapTuple<[string, number, boolean], string>;
// [string, string, string]
```

### Q133: Generic utility types for state management

```typescript
type ActionMap<M extends Record<string, unknown>> = {
  [Key in keyof M]: M[Key] extends undefined
    ? { type: Key }
    : { type: Key; payload: M[Key] };
};

type CounterActions = ActionMap<{
  increment: undefined;
  decrement: undefined;
  setCount: number;
}>;

type AsyncState<T, E = Error> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: E };
```

### Q134: Type-safe event emitter

```typescript
type EventMap = Record<string, unknown[]>;

class TypedEmitter<T extends EventMap> {
  private listeners = new Map<keyof T, Set<Function>>();

  on<K extends keyof T>(event: K, listener: (...args: T[K]) => void) {
    if (!this.listeners.has(event)) this.listeners.set(event, new Set());
    this.listeners.get(event)!.add(listener);
  }

  emit<K extends keyof T>(event: K, ...args: T[K]) {
    this.listeners.get(event)?.forEach((fn) => fn(...args));
  }
}

interface AppEvents {
  userLogin: [userId: string, timestamp: number];
  error: [error: Error, context?: string];
}

const emitter = new TypedEmitter<AppEvents>();
emitter.on("userLogin", (userId, ts) => console.log(userId, ts));
```

### Q135: Type-safe builder/fluent API

```typescript
class URLBuilder<Query extends Record<string, string> = {}> {
  private params: Query = {} as Query;
  constructor(private base: string) {}

  addParam<K extends string, V extends string>(
    key: K, value: V
  ): URLBuilder<Query & { [P in K]: V }> {
    const builder = new URLBuilder<Query & { [P in K]: V }>(this.base);
    builder.params = { ...this.params, [key]: value } as any;
    return builder;
  }

  build(): string {
    const qs = Object.entries(this.params)
      .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
      .join("&");
    return `${this.base}?${qs}`;
  }
}

const url = new URLBuilder("https://api.com")
  .addParam("search", "typescript")
  .addParam("page", "1")
  .build();
```

### Q136: Type-safe command pattern

```typescript
interface Command<T extends string, P = void> {
  type: T;
  payload: P;
}

type Commands = {
  createUser: Command<"createUser", { name: string; email: string }>;
  deleteUser: Command<"deleteUser", { id: string }>;
};

type CommandUnion = Commands[keyof Commands];

async function dispatch<C extends CommandUnion>(command: C): Promise<void> {
  // dispatch based on command.type
  console.log(command.type, command.payload);
}
```

### Q137: Type-safe dependency injection

```typescript
type ServiceRegistry = Record<string, new (...args: any[]) => any>;

class Container<T extends ServiceRegistry> {
  private instances = new Map<keyof T, InstanceType<T[keyof T]>>();

  register<K extends keyof T>(key: K, instance: InstanceType<T[K]>) {
    this.instances.set(key, instance);
  }

  get<K extends keyof T>(key: K): InstanceType<T[K]> {
    return this.instances.get(key) as InstanceType<T[K]>;
  }
}

interface AppServices { logger: Logger; database: Database; }
const container = new Container<AppServices>();
```

### Q138: Type-safe plugin system

```typescript
interface Plugin<Context, Hooks> {
  name: string;
  version: string;
  apply(context: Context): Partial<Hooks>;
}

type PluginHooks = {
  beforeRequest?: (url: string) => string;
  afterResponse?: (data: unknown) => unknown;
};

class PluginSystem {
  private hooks: PluginHooks = {};

  use<P extends Plugin<{}, PluginHooks>>(plugin: P): this {
    this.hooks = { ...this.hooks, ...plugin.apply({}) };
    return this;
  }
}
```

### Q139: Type-safe finite state machine

```typescript
function createMachine<States extends string>(
  initial: States,
  transitions: Record<States, States>
) {
  let current: States = initial;

  return {
    get state() { return current; },
    transition(event: keyof typeof transitions): States {
      const next = transitions[event as string];
      if (!next) throw new Error("Invalid transition");
      current = next;
      return current;
    },
  };
}

const machine = createMachine("pending" as const, {
  pending: "confirmed" as const,
  confirmed: "shipped" as const,
  shipped: "delivered" as const,
  delivered: "delivered" as const,
  cancelled: "cancelled" as const,
});

machine.transition("pending"); // "confirmed"
```

### Q140: Tuple to union

```typescript
type TupleToUnion<T extends readonly unknown[]> = T[number];

const roles = ["admin", "user", "guest"] as const;
type Role = (typeof roles)[number]; // "admin" | "user" | "guest"

type FeatureConfig = Record<Role, boolean>;
```

---

# TypeScript with React (Q141–Q180)

### Q141: React.FC vs direct type annotations

```typescript
// React.FC (older style, includes children implicitly)
interface Props { name: string; age?: number; }
const UserCard: React.FC<Props> = ({ name, age }) => (
  <div>{name} ({age ?? "N/A"})</div>
);

// Direct annotation (recommended — explicit children)
interface UserCardProps { name: string; age?: number; children?: React.ReactNode; }
function UserCard({ name, age, children }: UserCardProps) {
  return (<div>{name} ({age ?? "N/A"}){children}</div>);
}
```

### Q142: Typing props

```typescript
interface ButtonProps {
  variant: "primary" | "secondary" | "ghost";
  size: "sm" | "md" | "lg";
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  type?: "button" | "submit" | "reset";
}

function Button({ variant = "primary", size = "md", disabled = false, children, onClick }: ButtonProps) {
  return (
    <button className={`btn btn-${variant} btn-${size}`} disabled={disabled} onClick={onClick}>
      {children}
    </button>
  );
}
```

### Q143: useState with TypeScript

```typescript
const [count, setCount] = useState(0); // number (inferred)
const [user, setUser] = useState<User | null>(null);
const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
const [items, setItems] = useState<Item[]>([]);

const [filters, setFilters] = useState<{
  search: string;
  category: string | null;
  priceRange: [number, number];
}>({ search: "", category: null, priceRange: [0, 1000] });
```

### Q144: useReducer with discriminated unions

```typescript
type CounterAction =
  | { type: "increment" }
  | { type: "decrement" }
  | { type: "setCount"; payload: number }
  | { type: "reset" };

interface CounterState { count: number; lastAction: string; }

function counterReducer(state: CounterState, action: CounterAction): CounterState {
  switch (action.type) {
    case "increment": return { ...state, count: state.count + 1, lastAction: "increment" };
    case "decrement": return { ...state, count: state.count - 1, lastAction: "decrement" };
    case "setCount": return { ...state, count: action.payload, lastAction: "setCount" };
    case "reset": return { count: 0, lastAction: "reset" };
    default: {
      const _exhaustive: never = action;
      return state;
    }
  }
}

function Counter() {
  const [state, dispatch] = useReducer(counterReducer, { count: 0, lastAction: "none" });
  return <button onClick={() => dispatch({ type: "increment" })}>+</button>;
}
```

### Q145: useRef types

```typescript
// DOM ref — RefObject
const inputRef = useRef<HTMLInputElement>(null);
// inputRef.current is HTMLInputElement | null

// Mutable ref for values — MutableRefObject
const intervalRef = useRef<number | null>(null);
intervalRef.current = window.setInterval(() => {}, 1000);

// Non-null initial value
const inputRef2 = useRef<HTMLInputElement>(null!);
// inputRef2.current is HTMLInputElement (not null)
```

### Q146: Typing event handlers

```typescript
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value);
};

const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
};

const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.clientX, e.clientY);
};

const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  if (e.key === "Enter") { /* submit */ }
};
```

### Q147: Typing custom hooks

```typescript
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    const item = window.localStorage.getItem(key);
    return item ? JSON.parse(item) as T : initialValue;
  });

  const setValue = (value: T | ((prev: T) => T)) => {
    setStoredValue(prev => {
      const next = value instanceof Function ? value(prev) : value;
      window.localStorage.setItem(key, JSON.stringify(next));
      return next;
    });
  };

  return [storedValue, setValue] as const;
}

function useAsync<T>(fn: () => Promise<T>) {
  const [state, setState] = useState<{
    status: "idle" | "loading" | "success" | "error";
    data?: T;
    error?: Error;
  }>({ status: "idle" });

  const execute = async () => {
    setState({ status: "loading" });
    try {
      const data = await fn();
      setState({ status: "success", data });
    } catch (error) {
      setState({ status: "error", error: error as Error });
    }
  };

  return { ...state, execute };
}
```

### Q148: Generic components

```typescript
interface ListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
}

function List<T>({ items, renderItem, keyExtractor }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={keyExtractor(item)}>{renderItem(item, index)}</li>
      ))}
    </ul>
  );
}

// Usage
<List
  items={users}
  keyExtractor={(user) => user.id}  // user inferred as User
  renderItem={(user) => <span>{user.name}</span>}
/>
```

### Q149: forwardRef with generics

```typescript
interface InputHandle { focus: () => void; reset: () => void; }

const Input = forwardRef<InputHandle, { label: string }>(({ label }, ref) => {
  const inputRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    focus: () => inputRef.current?.focus(),
    reset: () => { if (inputRef.current) inputRef.current.value = ""; },
  }));

  return <div><label>{label}</label><input ref={inputRef} /></div>;
});

function Form() {
  const inputRef = useRef<InputHandle>(null);
  return <><Input ref={inputRef} label="Name" /><button onClick={() => inputRef.current?.focus()}>Focus</button></>;
}
```

### Q150: Typing children

```typescript
import { ReactNode, ReactElement } from "react";

// ReactNode — most permissive
interface CardProps { title: string; children: ReactNode; }

// ReactElement — only JSX elements
interface StrictCardProps { children: ReactElement | ReactElement[]; }

// Children as function (render prop)
interface DataProviderProps<T> {
  children: (data: T) => ReactNode;
}
```

### Q151: Typing context

```typescript
interface AuthContextValue {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const login = async (email: string, password: string) => {
    setUser(await api.login(email, password));
  };
  return (
    <AuthContext.Provider value={{ user, login, logout: () => setUser(null), isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
}
```

### Q152: useCallback and useMemo types

```typescript
// Type inference works
const handleClick = useCallback((e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e.clientX);
}, []);

const sortedItems = useMemo(() => {
  return [...items].sort((a, b) => a.name.localeCompare(b.name));
}, [items]);

// Explicit typing
const handleSubmit = useCallback<(e: React.FormEvent) => void>((e) => {
  e.preventDefault();
}, []);
```

### Q153: Higher-order component typing

```typescript
import { ComponentType } from "react";

interface WithLoadingProps { loading: boolean; }

function withLoading<P extends object>(
  WrappedComponent: ComponentType<P>
): ComponentType<P & WithLoadingProps> {
  return function WithLoadingWrapper(props: P & WithLoadingProps) {
    return props.loading ? <div>Loading...</div> : <WrappedComponent {...props as P} />;
  };
}

// HOC that injects props
interface InjectedProps { timestamp: Date; }

function withTimestamp<P extends object>(
  WrappedComponent: ComponentType<P & InjectedProps>
) {
  return function WithTimestamp(props: P) {
    return <WrappedComponent {...props as P & InjectedProps} timestamp={new Date()} />;
  };
}
```

### Q154: Render prop typing

```typescript
interface MouseTrackerProps {
  render: (state: { x: number; y: number }) => React.ReactNode;
}

function MouseTracker({ render }: MouseTrackerProps) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  return (
    <div onMouseMove={(e) => setPosition({ x: e.clientX, y: e.clientY })}>
      {render(position)}
    </div>
  );
}

// Generic render prop
interface DataProviderProps<T> {
  url: string;
  children: (state: { data: T | null; loading: boolean; error: Error | null }) => React.ReactNode;
}
```

### Q155: TypeScript with Next.js

```typescript
import { GetServerSideProps, GetStaticProps, InferGetServerSidePropsType } from "next";

interface PageProps { user: User; timestamp: number; }

export const getServerSideProps: GetServerSideProps<PageProps> = async (ctx) => {
  const user = await fetchUser(ctx.params?.id as string);
  return { props: { user, timestamp: Date.now() } };
};

function UserPage({ user, timestamp }: InferGetServerSidePropsType<typeof getServerSideProps>) {
  return <div>{user.name}</div>;
}

export const getStaticProps: GetStaticProps<PageProps> = async () => {
  const user = await fetchUser("1");
  return { props: { user, timestamp: Date.now() }, revalidate: 60 };
};
```

### Q156: TypeScript with Zustand

```typescript
import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

interface BearStore {
  bears: number;
  increase: (by?: number) => void;
  reset: () => void;
}

const useBearStore = create<BearStore>()(
  devtools(
    persist(
      (set) => ({
        bears: 0,
        increase: (by = 1) => set((state) => ({ bears: state.bears + by })),
        reset: () => set({ bears: 0 }),
      }),
      { name: "bear-storage" }
    )
  )
);

function BearCounter() {
  const bears = useBearStore((state) => state.bears);
  return <h1>{bears} bears</h1>;
}
```

### Q157: TypeScript with React Query

```typescript
import { useQuery, useMutation } from "@tanstack/react-query";
import { AxiosError } from "axios";

interface User { id: string; name: string; email: string; }

function useUsers() {
  return useQuery<User[], AxiosError>({
    queryKey: ["users"],
    queryFn: () => fetch("/api/users").then((r) => r.json()),
    staleTime: 5 * 60 * 1000,
  });
}

function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation<User, AxiosError, { name: string; email: string }>({
    mutationFn: (input) =>
      fetch("/api/users", {
        method: "POST",
        body: JSON.stringify(input),
        headers: { "Content-Type": "application/json" },
      }).then((r) => r.json()),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["users"] }),
  });
}
```

### Q158: Typing form state with discriminated unions

```typescript
interface FormState {
  values: { name: string; email: string; password: string; };
  errors: Partial<Record<keyof FormState["values"], string>>;
  touched: Partial<Record<keyof FormState["values"], boolean>>;
  status: "idle" | "submitting" | "success" | "error";
}

function useForm(initialValues: FormState["values"]) {
  const [state, setState] = useState<FormState>({
    values: initialValues,
    errors: {},
    touched: {},
    status: "idle",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setState((prev) => ({ ...prev, values: { ...prev.values, [name]: value } }));
  };

  const handleSubmit = (onSubmit: (values: FormState["values"]) => Promise<void>) => {
    return async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      setState((prev) => ({ ...prev, status: "submitting" }));
      try { await onSubmit(state.values); setState((prev) => ({ ...prev, status: "success" })); }
      catch { setState((prev) => ({ ...prev, status: "error" })); }
    };
  };

  return { state, handleChange, handleSubmit };
}
```

### Q159: Typing React Router v6

```typescript
import { useParams, useSearchParams, useNavigate } from "react-router-dom";

function UserProfile() {
  const { userId } = useParams<{ userId: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const page = Number(searchParams.get("page")) || 1;
  // navigate, useParams, useSearchParams are all typed
}

interface LocationState { from: string; searchTerm?: string; }
```

### Q160: Typing Redux Toolkit slices

```typescript
import { createSlice, PayloadAction, createAsyncThunk } from "@reduxjs/toolkit";

interface CounterState { value: number; status: "idle" | "loading" | "failed"; }

const counterSlice = createSlice({
  name: "counter",
  initialState: { value: 0, status: "idle" } as CounterState,
  reducers: {
    increment: (state) => { state.value += 1; },
    incrementByAmount: (state, action: PayloadAction<number>) => { state.value += action.payload; },
  },
});
```

### Q161: Typing form refs and uncontrolled components

```typescript
function LoginForm() {
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const email = emailRef.current?.value ?? "";
    const password = passwordRef.current?.value ?? "";
  };

  return (
    <form onSubmit={handleSubmit}>
      <input ref={emailRef} name="email" type="email" />
      <input ref={passwordRef} name="password" type="password" />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Q162: Typing React portals

```typescript
import { createPortal } from "react-dom";

function Portal({ children, containerId = "portal-root" }: { children: React.ReactNode; containerId?: string }) {
  const container = typeof document !== "undefined" ? document.getElementById(containerId) : null;
  if (!container) return null;
  return createPortal(children, container);
}

function Modal({ isOpen, children }: { isOpen: boolean; children: React.ReactNode }) {
  if (!isOpen) return null;
  return <Portal><div className="modal">{children}</div></Portal>;
}
```

### Q163: Typing React.memo with generics

```typescript
import { memo } from "react";

interface ListItemProps<T extends { id: string }> {
  item: T;
  onSelect: (item: T) => void;
  isSelected: boolean;
}

function ListItemComponent<T extends { id: string }>({ item, onSelect, isSelected }: ListItemProps<T>) {
  return <div onClick={() => onSelect(item)}>{item.id}</div>;
}

const MemoizedListItem = memo(ListItemComponent) as typeof ListItemComponent;
```

### Q164: Typing React.lazy and Suspense

```typescript
import { lazy, Suspense, ComponentType } from "react";

const Dashboard = lazy<ComponentType<{ userId: string }>>(() => import("./Dashboard"));

function LazyLoad({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<div>Loading...</div>}>{children}</Suspense>;
}
```

### Q165: Typing compound components

```typescript
interface TabsContextType { activeTab: string; setActiveTab: (tab: string) => void; }
const TabsContext = createContext<TabsContextType | null>(null);

function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      {children}
    </TabsContext.Provider>
  );
}

function Tab({ value, children }: { value: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useContext(TabsContext)!;
  return <button className={activeTab === value ? "active" : ""} onClick={() => setActiveTab(value)}>{children}</button>;
}

Tabs.Tab = Tab;
```

### Q166: Typing React DnD / dnd-kit

```typescript
import { DndContext, useDraggable, useDroppable, DragEndEvent } from "@dnd-kit/core";

function DraggableItem({ id, children }: { id: string; children: React.ReactNode }) {
  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({ id });
  const style = { transform: `translate3d(${transform?.x ?? 0}px, ${transform?.y ?? 0}px, 0)`, opacity: isDragging ? 0.5 : 1 };
  return <div ref={setNodeRef} style={style} {...listeners} {...attributes}>{children}</div>;
}
```

### Q167: Typing CSS-in-JS with TypeScript

```typescript
// Emotion / styled-components
const Button = styled.button<{ variant: "primary" | "secondary" }>`
  background: ${({ variant }) => variant === "primary" ? "blue" : "gray"};
  color: white;
  padding: 8px 16px;
`;

// CSS Modules
import styles from "./Button.module.css";
// styles is typed as Record<string, string>
```

### Q168: Typing React Testing Library

```typescript
import { render, screen, fireEvent } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

test("button click", async () => {
  const handleClick = vi.fn();
  render(<Button onClick={handleClick}>Click me</Button>);

  await userEvent.click(screen.getByText("Click me"));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

### Q169: Type-safe prop spreading with rest

```typescript
interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "size"> {
  label: string;
  error?: string;
  size?: "sm" | "md" | "lg";
}

function Input({ label, error, size = "md", className, ...props }: InputProps) {
  return (
    <div>
      <label>{label}</label>
      <input className={`input-${size} ${className ?? ""}`} {...props} />
      {error && <span className="error">{error}</span>}
    </div>
  );
}
```

### Q170: Typing polymorphic components (as prop)

```typescript
type PolymorphicProps<T extends React.ElementType> = {
  as?: T;
  children?: React.ReactNode;
} & React.ComponentPropsWithoutRef<T>;

function Box<T extends React.ElementType = "div">({ as, children, ...props }: PolymorphicProps<T>) {
  const Component = as ?? "div";
  return <Component {...props}>{children}</Component>;
}

// Usage
<Box as="button" onClick={() => {}}>Click</Box>
<Box as="a" href="/">Link</Box>
```

### Q171: Typing React table components

```typescript
interface Column<T> {
  key: keyof T;
  header: string;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
  sortable?: boolean;
}

interface TableProps<T extends Record<string, unknown>> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
}

function Table<T extends Record<string, unknown>>({ data, columns, onRowClick }: TableProps<T>) {
  return (
    <table>
      <thead><tr>{columns.map((col) => <th key={String(col.key)}>{col.header}</th>)}</tr></thead>
      <tbody>
        {data.map((row, i) => (
          <tr key={i} onClick={() => onRowClick?.(row)}>
            {columns.map((col) => (
              <td key={String(col.key)}>
                {col.render ? col.render(row[col.key], row) : String(row[col.key])}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### Q172: Typing React hook form

```typescript
import { useForm, SubmitHandler, FieldValues } from "react-hook-form";

interface LoginForm extends FieldValues {
  email: string;
  password: string;
  rememberMe: boolean;
}

function LoginFormComponent() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>();

  const onSubmit: SubmitHandler<LoginForm> = (data) => {
    console.log(data.email, data.password);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email", { required: true })} />
      {errors.email && <span>Email is required</span>}
      <input type="password" {...register("password", { minLength: 8 })} />
      <input type="checkbox" {...register("rememberMe")} />
      <button type="submit">Login</button>
    </form>
  );
}
```

### Q173: Typing React Query with infinite queries

```typescript
import { useInfiniteQuery } from "@tanstack/react-query";

function useInfiniteUsers() {
  return useInfiniteQuery<User[], Error>({
    queryKey: ["users"],
    queryFn: ({ pageParam = 0 }) => fetch(`/api/users?page=${pageParam}`).then(r => r.json()),
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => lastPage.length === 10 ? allPages.length : undefined,
  });
}
```

### Q174: Typing React Router loaders (Remix/React Router v6.4+)

```typescript
import { json, LoaderFunctionArgs } from "react-router-dom";

interface UserLoaderData { user: User; posts: Post[]; }

async function userLoader({ params }: LoaderFunctionArgs): Promise<Response> {
  const [user, posts] = await Promise.all([
    fetchUser(params.userId!),
    fetchPosts(params.userId!),
  ]);
  return json<UserLoaderData>({ user, posts });
}

function UserPage() {
  const { user, posts } = useLoaderData() as UserLoaderData;
  return <div>{user.name}</div>;
}
```

### Q175: Typing event handlers in custom hooks

```typescript
function useKeyboardShortcut(keys: string[], handler: (e: KeyboardEvent) => void) {
  useEffect(() => {
    const listener = (e: KeyboardEvent) => {
      if (keys.includes(e.key)) handler(e);
    };
    window.addEventListener("keydown", listener);
    return () => window.removeEventListener("keydown", listener);
  }, [keys, handler]);
}
```

### Q176: Typing IntersectionObserver hook

```typescript
function useIntersectionObserver<T extends HTMLElement>(
  options?: IntersectionObserverInit
) {
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);
  const ref = useRef<T>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const observer = new IntersectionObserver(([entry]) => setEntry(entry), options);
    observer.observe(element);
    return () => observer.disconnect();
  }, [options]);

  return { ref, entry };
}
```

### Q177: Typing useMediaQuery hook

```typescript
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(() => window.matchMedia(query).matches);

  useEffect(() => {
    const media = window.matchMedia(query);
    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
}

function ResponsiveComponent() {
  const isMobile = useMediaQuery("(max-width: 768px)");
  return <div>{isMobile ? "Mobile" : "Desktop"}</div>;
}
```

### Q178: Typing React Error Boundary

```typescript
import { Component, ErrorInfo, ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("Error caught:", error, info);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (typeof this.props.fallback === "function") {
        return this.props.fallback(this.state.error, this.handleReset);
      }
      return this.props.fallback ?? <div>Something went wrong</div>;
    }
    return this.props.children;
  }
}
```

### Q179: Typing React transitions (useTransition)

```typescript
import { useTransition } from "react";

function SearchComponent() {
  const [isPending, startTransition] = useTransition();
  const [query, setQuery] = useState("");

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    startTransition(() => {
      setQuery(e.target.value); // low-priority update
    });
  };

  return (
    <div>
      <input onChange={handleChange} />
      {isPending && <span>Updating...</span>}
      <ExpensiveList query={query} />
    </div>
  );
}
```

### Q180: Typing React Server Components

```typescript
// Server Component (Next.js App Router)
interface PageProps {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

async function UserPage({ params, searchParams }: PageProps) {
  const user = await fetchUser(params.id);
  return <div>{user.name}</div>;
}

// API route with types
export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;
  const id = params.get("id");
  return NextResponse.json({ id });
}
```

---

# TypeScript Configuration & Tooling (Q181–Q200)

### Q181: tsconfig.json — all important options

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Q182: strict mode family explained

- **strict**: enables all individual strict flags
- **strictNullChecks**: null/undefined not assignable to every type
- **noImplicitAny**: error when type cannot be inferred
- **strictFunctionTypes**: function parameter contravariance
- **strictBindCallApply**: strict checking for bind/call/apply
- **strictPropertyInitialization**: class properties must be initialized
- **noImplicitThis**: `this` has implicit type `any`
- **alwaysStrict**: emit `"use strict"` in output

### Q183: paths and baseUrl

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@utils/*": ["src/utils/*"]
    }
  }
}
```

Allows `import { Button } from "@components/Button"` instead of relative paths.

### Q184: declaration files (--declaration)

Generates `.d.ts` files alongside compiled JS. Essential for library authors.

```bash
tsc --declaration
# Outputs: index.js, index.d.ts, index.js.map
```

### Q185: sourceMap

Generates `.map` files for debugging TypeScript source in browser dev tools.

```json
{ "compilerOptions": { "sourceMap": true } }
```

### Q186: target vs module

- **target**: JS language version for output (ES5, ES2015, ES2020, ES2022)
- **module**: module system (CommonJS, ESNext, Node16)

```json
{
  "target": "ES2022",
  "module": "ESNext"
}
```

### Q187: lib option

Specifies type definitions to include.

```json
{
  "lib": ["ES2022", "DOM", "DOM.Iterable"]
}
```

Without `"DOM"`, you won't have `document`, `fetch`, `window` types.

### Q188: skipLibCheck

Skips type checking of all `.d.ts` files. Significantly speeds up compilation.

```json
{ "compilerOptions": { "skipLibCheck": true } }
```

### Q189: isolatedModules

Ensures each file can be safely transpiled in isolation. Required by Babel, esbuild, Vite.

```json
{ "compilerOptions": { "isolatedModules": true } }
```

When enabled, you cannot use:
- `const enum` exports
- Namespace exports
- `this` in non-function contexts

### Q190: esModuleInterop

Enables `import foo from "bar"` syntax for CommonJS modules.

```json
{ "compilerOptions": { "esModuleInterop": true } }
```

Without it: `import * as foo from "bar"`.

### Q191: TypeScript with ESLint

```bash
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

```javascript
// eslint.config.js
import tseslint from "typescript-eslint";

export default tseslint.config({
  files: ["**/*.ts"],
  extends: [
    ...tseslint.configs.recommended,
  ],
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
  },
});
```

Key rules:
- `@typescript-eslint/no-explicit-any` — ban `any` usage
- `@typescript-eslint/strict-boolean-expressions` — strict boolean checks
- `@typescript-eslint/no-floating-promises` — must await promises
- `@typescript-eslint/consistent-type-imports` — enforce `import type`

### Q192: TypeScript with Prettier

```bash
npm install -D prettier eslint-config-prettier
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

Add `eslint-config-prettier` to avoid ESLint/Prettier conflicts.

### Q193: TypeScript with Jest

```bash
npm install -D jest @types/jest ts-jest
```

```javascript
// jest.config.js
module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  roots: ["<rootDir>/src"],
  testMatch: ["**/*.test.ts"],
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },
};
```

```typescript
// test file
import { sum } from "@/utils/math";

test("adds 1 + 2 = 3", () => {
  expect(sum(1, 2)).toBe(3);
});
```

### Q194: TypeScript with Vitest

```bash
npm install -D vitest
```

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
  },
  resolve: {
    alias: { "@": path.resolve(__dirname, "src") },
  },
});
```

```typescript
// component test
import { render, screen } from "@testing-library/react";
import { Button } from "./Button";

test("renders button", () => {
  render(<Button>Click</Button>);
  expect(screen.getByText("Click")).toBeDefined();
});
```

### Q195: TypeScript with Webpack

```bash
npm install -D ts-loader typescript
```

```javascript
// webpack.config.js
module.exports = {
  entry: "./src/index.ts",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [".tsx", ".ts", ".js"],
    alias: { "@": path.resolve(__dirname, "src") },
  },
};
```

### Q196: TypeScript with Vite

```bash
npm create vite@latest my-app -- --template react-ts
```

```typescript
// vite.config.ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "src") },
  },
});
```

Vite uses esbuild for transpilation (not tsc). Type checking is done separately via `tsc --noEmit`.

### Q197: TypeScript with Babel

```bash
npm install -D @babel/preset-typescript
```

```javascript
// babel.config.js
module.exports = {
  presets: [
    "@babel/preset-env",
    "@babel/preset-react",
    "@babel/preset-typescript",
  ],
};
```

Babel strips TypeScript types without type-checking. Use `tsc --noEmit` separately for type checking.

### Q198: TypeScript with esbuild

```javascript
// build.js
require("esbuild").buildSync({
  entryPoints: ["src/index.ts"],
  bundle: true,
  outfile: "dist/bundle.js",
  loader: { ".ts": "ts" },
});
```

esbuild is very fast but does no type checking. Use `tsc --noEmit` for type checking.

### Q199: TypeScript with SWC

```bash
npm install -D @swc/cli @swc/core
```

```json
// .swcrc
{
  "jsc": {
    "parser": {
      "syntax": "typescript",
      "tsx": true
    },
    "target": "es2020"
  }
}
```

SWC is a fast Rust-based transpiler (used by Next.js). No type checking — use `tsc --noEmit`.

### Q200: Monorepo TypeScript setup

```json
// Root tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "declaration": true,
    "composite": true,
    "declarationMap": true,
    "sourceMap": true,
    "skipLibCheck": true
  },
  "references": [
    { "path": "packages/core" },
    { "path": "packages/utils" },
    { "path": "apps/web" },
    { "path": "apps/api" }
  ],
  "files": []
}
```

```json
// packages/core/tsconfig.json
{
  "extends": "../../tsconfig.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"]
}
```

```bash
# Build all packages
tsc --build

# Build specific package
tsc --build packages/core
```

---

> End of TypeScript 200+ Interview Q&A. This covers fundamentals, advanced patterns, React integration, and configuration/tooling — all at YC startup interview level.
