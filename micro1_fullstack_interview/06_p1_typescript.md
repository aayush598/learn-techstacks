# Priority 1 — TypeScript (Q216–Q242)

**Why these matter for micro1:** the role requires TypeScript with React/Next.js. Expect type-system fundamentals, generics, narrowing, utility types, and typing React props/handlers/API responses.

---

## Q216: Why use TypeScript with React?

1. **Compile-time safety** — catches prop typos, undefined access, shape mismatches before runtime.
2. **Autocompletion & refactoring** — editors understand component contracts; renaming is safe.
3. **Self-documenting code** — types describe data contracts (props, API responses, state).
4. **Confidence in changes** — large codebases stay maintainable; `strict` mode catches null/undefined bugs.
5. **Shared contracts** — types mirror backend models (Q242), reducing integration bugs.
6. **Better DX** with hooks: typed `useState`, typed event handlers, generic `useQuery`.

For micro1's chat/dashboard UI with fast-moving data shapes, TS is near-mandatory.

---

## Q217: What is the difference between JavaScript and TypeScript?

| | **JavaScript** | **TypeScript** |
|---|---|---|
| Type checking | Runtime only (dynamic) | **Compile-time** (static, optional-but-encouraged) |
| Runtime | Interpreted by JS engines | Compiled/transpiled **to JavaScript** (no TS runtime) |
| Features | ES spec | Everything JS + types, enums, interfaces, generics, decorators |
| Safety | Errors surface at runtime | Many errors caught before running |
| Tooling | Weaker inference | Rich IntelliSense from types |

- **Key point:** TypeScript is a **superset** — valid JS is valid TS. TS is erased at compile time (types are not real values).
- `tsc` (or esbuild/SWC) compiles TS → JS; type errors don't stop output unless configured.

---

## Q218: What is a type?

A **description of the shape of a value** — what properties/methods it has and their kinds. TS infers most types from usage; you can also declare them explicitly.

```ts
let count: number = 5;
const user: { name: string; age: number } = { name: "Ada", age: 36 };
type ID = string | number;              // alias
```

- Categories: primitives (`string`, `number`, `boolean`, `null`, `undefined`, `symbol`, `bigint`), object types, arrays (`string[]` / `Array<T>`), tuples, unions, functions, generics.
- Types exist **only at compile time** — erased in output JS.

---

## Q219: What is an interface?

A named **object-type declaration** — describes the shape of an object/class contract.

```ts
interface User {
  id: number;
  email: string;
  roles: string[];
}
```

- Supports **declaration merging** (redeclaring the same interface adds members) and **`extends`**.
- Primarily for objects/classes.

---

## Q220: What is the difference between `type` and `interface`?

Both describe object shapes. Key differences:

| | `type` | `interface` |
|---|---|---|
| Extends | `type B = A & {...}` (intersection) | `interface B extends A {}` |
| Can describe | Unions, tuples, primitives, mapped types, functions | Objects/classes only |
| Declaration merging | No (duplicate → error) | Yes (merges) |
| Computed/conditional | Yes | No |
| Interop with React | Both fine | Slightly preferred for classes/extends |

**Modern guidance:** prefer `interface` for **object shapes/class contracts** (merging, performance of error messages); use `type` for **unions, intersections, tuples, and anything derived**. For React props, either works — pick one and be consistent.

```ts
type Status = "pending" | "active" | "rejected";          // union → type
interface Props { user: User; onSave: (u: User) => void } // object → interface
```

---

## Q221: What are union types?

A value that can be **one of several types**: `A | B`.

```ts
type ID = string | number;
type Status = "pending" | "active" | "closed";

function print(id: ID) {
  if (typeof id === "string") console.log(id.toUpperCase());   // narrow
  else console.log(id);
}
```

- With object unions + discriminants → **discriminated unions** (Q233).
- Must **narrow** to use type-specific operations.

---

## Q222: What are intersection types?

Combine multiple types into **one** (must satisfy all): `A & B`.

```ts
interface Base { id: number }
interface WithTimestamps { createdAt: Date; updatedAt: Date }

type Auditable = Base & WithTimestamps;   // has id + createdAt + updatedAt
```

- Useful for composing mixins/overlays; can produce never when conflicting primitives (`string & number`).

---

## Q223: What are optional properties?

Properties that may be absent — `?` marks them optional (type becomes `T | undefined`).

```ts
interface Profile {
  name: string;
  bio?: string;          // optional — may be undefined
  phone: string | null;  // present but nullable — different!
}
```

- **`bio?: string` vs `phone: string | null`:** optional = key may not exist; nullable = key exists with null value. Know the difference when consuming API data.
- Accessing an optional property yields `string | undefined` → narrow before use.

---

## Q224: What are generics?

Type **parameters** — a way to write components/functions/types that work with **any type** while preserving that type.

```ts
function identity<T>(value: T): T { return value; }
identity<number>(5);          // T = number
identity("hello");            // T inferred = string

interface Box<T> { value: T }
```

- Used everywhere in TS: `Array<T>`, `Promise<T>`, `Record<K, V>`, React `useState<T>`.
- Constraints: `function f<T extends HasId>(x: T)` — restrict what T can be.
- Generic hooks, generic API clients (Q597) are standard patterns.

---

## Q225: How do generics work?

1. **Declaration:** you introduce a type parameter (`<T>`) that stands for a type supplied later.
2. **Instantiation:** callers provide the type explicitly or TS **infers** it from arguments.
3. **Erasure:** like all types, generics are erased at compile time — they're purely a compile-time feature (no runtime reflection).
4. **Constraints** (`extends`) limit what types T may be and unlock operations on them.

```ts
function getFirst<T>(arr: T[]): T | undefined { return arr[0]; }
getFirst([1, 2, 3]);          // T inferred number → number | undefined
getFirst(["a"]);              // string

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  return (await res.json()) as T;
}
```

- Behind the scenes TS performs **type inference + unification** at compile time; the runtime code is just plain JS.

---

## Q226: What is `any`?

The **opt-out type** — accepts and allows anything; disables type checking entirely for that value.

```ts
let x: any = 5;
x = "text"; x.bad.method;     // no errors — dangerous
```

- Escapes all safety; makes errors silent. **Avoid** — use `unknown` when you don't know the type.

---

## Q227: What is `unknown`?

The **type-safe counterpart to `any`** — accepts anything, but you must **narrow before using** it.

```ts
let x: unknown = JSON.parse('{"a":1}');   // anything can be assigned
x.a;                                      // ERROR — unknown not safe to use
if (typeof x === "object" && x && "a" in x) console.log(x.a);  // OK after narrow
```

- Ideal for: API/JSON responses, user input, error catches (`catch (e: unknown)`).

---

## Q228: What is the difference between `any` and `unknown`?

| | `any` | `unknown` |
|---|---|---|
| Assignable to | Anything, freely usable | Anything can be assigned to it; must be narrowed to use |
| Safety | None — checks disabled | Full — forces narrowing |
| Use case | Opt-out (avoid) | Unknown data (JSON, errors) |

```ts
let a: any;     let u: unknown;
a.foo;          // allowed
u.foo;          // error — must narrow first
```

Rule: **never `any`; prefer `unknown`** when you truly don't know the shape.

---

## Q229: What is `never`?

The type of values that **can never occur** — the bottom type.

- A function that never returns: `function fail(): never { throw new Error(); }` (or infinite loop).
- **Exhaustive checking:** after narrowing all union members, the "else" branch has type `never`.
- A narrowing that leaves an empty set produces `never` (`string & number` → `never`).

```ts
function assertNever(x: never): never { throw new Error(`Unexpected: ${x}`); }

switch (status) {
  case "active": break;
  case "closed": break;
  default: assertNever(status);   // compile error if a new case is added
}
```

---

## Q230: What is type narrowing?

TS **refining a value's type** at runtime check points, so you can safely use type-specific operations.

```ts
function handle(x: string | number | null) {
  if (x === null) return;
  if (typeof x === "string") return x.toUpperCase();   // narrowed to string
  return x.toFixed(2);                                 // narrowed to number
}
```

Narrowing tools: `typeof`, `instanceof`, `in`, equality, truthiness, discriminated-union discriminant checks, custom **type guards** (Q231), `Array.isArray`.

---

## Q231: What are type guards?

Functions that **narrow a type** via a type predicate `x is T`.

```ts
function isUser(value: unknown): value is User {
  return !!value && typeof value === "object" && "email" in value;
}

if (isUser(data)) {
  data.email;   // TS knows it's User
}
```

- Built-in guards: `typeof`, `instanceof`, `Array.isArray`.
- Custom guards let you validate runtime data (API responses) and inform the type system safely.

---

## Q232: What is type inference?

TS **deducing types from usage** without explicit annotations.

```ts
let count = 5;            // inferred number
const name = "Ada";       // literal type "Ada" for const
const arr = [1, 2, 3];    // number[]
function add(a: number, b: number) { return a + b; }   // return inferred number
```

- `const` infers literal types; `let` widens (`string`).
- **Best practice:** let TS infer where obvious; annotate function params/returns for public APIs.

---

## Q233: What is a discriminated union?

A union of objects distinguished by a **common discriminant field** (a literal type), enabling precise narrowing.

```ts
type Message =
  | { kind: "user"; text: string }
  | { kind: "ai"; text: string; tokens: number }
  | { kind: "system"; code: number };

function render(m: Message) {
  switch (m.kind) {          // narrows by discriminant
    case "user": return m.text;
    case "ai": return `${m.text} (${m.tokens} tokens)`;
    case "system": return `code ${m.code}`;
  }
}
```

- Also known as **tagged unions**. Combined with `never` (Q229/Q599) → exhaustive, refactor-safe handling.
- Perfect for chat messages, API event types, state machines.

---

## Q234: What are utility types?

Built-in **generic type transformers** that derive new types from existing ones.

```ts
interface User { id: number; name: string; email: string; createdAt: Date }

type PartialUser = Partial<User>;     // all props optional
type PublicUser  = Pick<User, "id" | "name">;
type WithoutEmail = Omit<User, "email">;
type UserMap     = Record<number, User>;
type ReadonlyUser = Readonly<User>;   // all props readonly
type Names = User["name"];            // indexed access
```

Others: `Required<T>`, `Exclude<T, U>`, `Extract<T, U>`, `NonNullable<T>`, `ReturnType<F>`, `Parameters<F>`, `Awaited<T>`, `NoInfer<T>`.

---

## Q235: What does `Partial<T>` do?

Makes **every property optional**: `Partial<T>` = `{ [K in keyof T]?: T[K] }`.

```ts
interface User { name: string; age: number; email: string }

const update: Partial<User> = { age: 37 };   // any subset — perfect for PATCH bodies
```

- Opposite: `Required<T>`. Use for update payloads, form states, progressive configs.

---

## Q236: What does `Pick<T>` do?

Selects a **subset of properties** by key: `Pick<T, K>`.

```ts
type PublicUser = Pick<User, "id" | "name">;   // { id: number; name: string }
```

- Use to expose a limited view of a type (public API, list rows).

---

## Q237: What does `Omit<T>` do?

Removes given keys, keeping the rest: `Omit<T, K>`.

```ts
type NewUser = Omit<User, "id" | "createdAt">;  // create payload (no server fields)
type SafeUser = Omit<User, "passwordHash">;     // strip secrets from API types
```

- The inverse of `Pick`; great for "server-owned fields excluded from client types."

---

## Q238: What does `Record<K, T>` do?

Builds an object type with keys of type `K` and values of type `T`.

```ts
type ScoreMap = Record<string, number>;
const scores: ScoreMap = { python: 90, react: 85 };

type StatusMap = Record<"pending" | "active", string>;   // keyed by union → exhaustive
```

- Use for dictionaries/lookup maps and maps keyed by a finite union (catches missing keys).

---

## Q239: How do you type React props?

Interface/type + `PropsWithChildren`/`ComponentProps` as needed:

```tsx
interface UserCardProps {
  user: User;
  showEmail?: boolean;
  onSelect: (userId: string) => void;
  children?: React.ReactNode;          // for nested content
}

function UserCard({ user, showEmail, onSelect, children }: UserCardProps) {
  return <div onClick={() => onSelect(user.id)}>{children}</div>;
}
```

- Optional callbacks: `onSelect?: (id: string) => void`.
- Event handler types: `React.MouseEventHandler<HTMLButtonElement>` or the handler type directly (Q240).
- For component-library props reuse: `React.ComponentProps<typeof Button>`.
- With `React.FC` (discouraged now): `const C: React.FC<Props> = ...` — prefer plain function + explicit props type.

---

## Q240: How do you type React event handlers?

Use React's handler types, or infer from the event param:

```tsx
// inline — inferred
<button onClick={(e) => console.log(e.currentTarget.value)} />

// named handler
const handleChange: React.ChangeEventHandler<HTMLInputElement> = (e) => {
  setValue(e.target.value);
};

// event object typed explicitly
function onSubmit(e: React.FormEvent<HTMLFormElement>) {
  e.preventDefault();
}
```

Common handler types: `React.MouseEventHandler<T>`, `React.ChangeEventHandler<T>`, `React.KeyboardEventHandler<T>`, `React.FormEventHandler<T>`, `React.DragEventHandler<T>`. If a custom handler prop, type it as `() => void` or `(arg) => void` — never `Function`.

---

## Q241: How do you type API responses?

Combine generics + runtime validation for safety:

```ts
// 1. Shape it
interface ListUsersResponse {
  items: User[];
  page: number;
  total: number;
}

// 2. Generic client preserves the type
async function getUsers(page: number): Promise<ListUsersResponse> {
  const res = await fetch(`/api/users?page=${page}`);
  if (!res.ok) throw new ApiError(res.status);
  return (await res.json()) as ListUsersResponse;   // cast — TS trusts you
}

// 3. Prefer runtime validation for untrusted data
import { z } from "zod";
const UserSchema = z.object({ id: z.number(), email: z.string().email() });
const data = UserSchema.parse(await res.json());    // typed + validated
```

- **Best practice:** validate at the boundary (Zod/io-ts or generated types from OpenAPI, Q242) so types reflect reality; invalid data fails loudly.
- For React Query: `useQuery<ListUsersResponse>` uses the generic.

---

## Q242: How would you share types between frontend and backend?

1. **OpenAPI / codegen (recommended):** FastAPI auto-generates OpenAPI schema → `openapi-typescript` (frontend) generates TS types/API client; a CI check fails if backend changes break contracts.

```bash
npx openapi-typescript http://localhost:8000/openapi.json -o src/api/schema.d.ts
```

2. **Shared package/monorepo:** a `packages/contracts` workspace holding TS types; backend (Python) mirrors them — but Python needs its own schema (Pydantic), so codegen usually wins.
3. **Codegen from Pydantic:** tools like `pydantic2ts` generate TS types from your Pydantic models directly.
4. **`zod` shared schemas** in a JS/TS monorepo — validate on both sides.
5. **Runtime contract testing** (Pact-style) to catch drift even with codegen.

**Key for micro1:** FastAPI + Next.js/TS → OpenAPI codegen keeps frontend/backend in sync automatically.
