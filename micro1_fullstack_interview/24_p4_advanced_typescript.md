# Priority 4 — Advanced TypeScript (Q589–Q599)

**Why these matter for micro1:** the recruiter UI is React+TypeScript; deeper TS questions test senior level. Expect generics, conditional/mapped/template-literal types, `infer`, overloads, and type-vs-runtime thinking.

---

## Q589: What are generics? Give a real-world example.

**Generics** parameterize a type by another type — the function/class works for *any* T while keeping the relationship precise.

```ts
function first<T>(items: T[]): T | undefined {
  return items[0];
}
const a = first([1, 2, 3]);        // number | undefined
const b = first(["x"]);            // string | undefined

function getById<T extends { id: string }>(items: T[], id: string): T | undefined {
  return items.find(x => x.id === id);
}
```

**Real examples in your app:**
- API wrappers: `async function apiGet<T>(path: string): Promise<T>` → typed responses.
- `useState<Candidate>` infers from `useState<Candidate | null>(null)`.
- Generic components: `<List<T> items={...} render={...} />`.
- **`async` + generics:** `getMatch<T = MatchResult>(...)` lets callers opt into a specific result type.

**The point:** generics encode *relationships* (input → output), not just "any". Combined with `extends` constraints and `infer` (Q590), they build type *transformations*.

---

## Q590: What is `infer`? When do you use it?

**`infer`** extracts a type *out of another type* inside a **conditional type** — pattern-matching on structure.

```ts
// get the element type of an array
type ElementOf<T> = T extends Array<infer E> ? E : never;
type A = ElementOf<string[]>;        // string
type B = ElementOf<number[]>;        // number

// get the return type of a function (like ReturnType)
type Ret<T> = T extends (...args: any[]) => infer R ? R : never;
type R = Ret<() => string>;          // string

// get the value type of a Promise (like Awaited)
type Unwrap<T> = T extends Promise<infer U> ? U : T;
type C = Unwrap<Promise<MatchResult>>;  // MatchResult
```

**Built-ins built on `infer`:** `ReturnType<T>`, `Parameters<T>`, `Awaited<T>`, `InstanceType<T>`.

**Use in your app:** unwrapping `Promise<ApiResponse<T>>` to its payload; extracting the element type from an API list response; library-authoring utilities. Rule: `infer` lives *only* in the `extends` clause of a conditional type.

---

## Q591: What are conditional types?

**Conditional types** select a type based on a type-level boolean:

```ts
type IsString<T> = T extends string ? "yes" : "no";
type A = IsString<"hi">;     // "yes"
type B = IsString<42>;       // "no"

// distributed over unions automatically:
type IsStringDist<T> = T extends string ? true : false;
type C = IsStringDist<"a" | 1 | null>;   // true | false | false
```

**Key behavior — **distribution**:** when the *checked type* is a union, the conditional applies to each member separately. **Distributive conditional types** are the foundation of utility types:
- `Exclude<T, U>` = `T extends U ? never : T`
- `Extract<T, U>` = `T extends U ? T : never`
- `NonNullable<T>` = `T extends null | undefined ? never : T`
- `Filter<T, U>` (custom): pick only members matching a shape.

**Where they matter:** typing discriminated unions, "remove these fields from the type", API response narrowing, and writing reusable type utilities (Q589/Q590 build on them).

---

## Q592: What are mapped types? Give examples.

**Mapped types** transform an object type by iterating over its keys:

```ts
type Optional<T> = { [K in keyof T]?: T[K] };
type Readonly<T> = { readonly [K in keyof T]: T[K] };
```

**Built-ins (know these cold):**
- `Partial<T>` — all props optional.
- `Required<T>` — all props required.
- `Readonly<T>` — all props readonly.
- `Pick<T, K>` — subset of keys.
- `Omit<T, K>` — remove keys.
- `Record<K, V>` — object with keys K and values V.
- `NonNullable<T>` — strip null/undefined.

```ts
type Job = { title: string; status: "open" | "closed"; salary?: number };
type JobForm = Partial<Job>;                    // all optional (form state)
type JobSummary = Pick<Job, "title" | "status">; // summary card
type JobNoSalary = Omit<Job, "salary">;
type StatusMap = Record<Job["status"], number>;  // { open: number; closed: number }
```

**Custom mapped types:** transform values (`{ [K in keyof T]: Promise<T[K]> }` = "async-ify" a DTO — useful for `getCandidate(): Promise<...>` wrappers). Combined with `as` (key remapping, TS 4.1+) and template literals (Q593), mapped types build API/DTO transformers.

---

## Q593: What are template literal types?

**Template literal types** build string types from other types — powerful with key remapping and API typing.

```ts
type Endpoint = `/api/v1/${string}`;
type Status = "open" | "closed";
type EventName = `candidate_${Status}`;      // "candidate_open" | "candidate_closed"

// key remapping in mapped types (TS 4.1+):
type WithId<T> = { [K in keyof T as `id_${K extends string ? K : never}`]: T[K] };
type A = WithId<{ user: number }>;           // { id_user: number }
```

**Real uses:**
- **Typed API routes:** `type ApiRoute = \`/applications/${string}\`` → type-safe `fetch`.
- **Typed event/action names** (state machines, analytics, message bus): `Message = { type: \`interview:${Stage}\`; payload: ... }`.
- **CSS/semantic class names**, typed i18n keys (`t(\`errors.${code}\`)`).
- Combine with `Uppercase/Lowercase/Capitalize/Uncapitalize` intrinsic string types.

**Interview answer:** "template literal types make string unions derive from other types — I use them to type event names and API routes so typos fail at compile time."

---

## Q594: What is type variance (covariant/contravariant)? Why does it matter?

**Variance** describes how a compound type behaves when its parts change — e.g., can `Array<Cat>` be used as `Array<Animal>`?

- **Covariant** (`out`): `A <: B` ⇒ `Box<A> <: Box<B>`. **Reads** are safe this way. Arrays/functions' return types are covariant in TS.
- **Contravariant** (`in`): `A <: B` ⇒ `Box<B> <: Box<A>`. **Writes**/parameter positions behave this way.
- **Invariant:** neither — e.g., mutable generic containers that both read and write.

**Why it matters (function parameters):** a handler that accepts `Animal` can safely be used where a handler accepting `Cat` is expected — because it can handle *any* Animal including Cat (parameter positions are contravariant under strict function type rules; TS is *bivariant* for method parameters for compatibility, but `strictFunctionTypes` makes standalone function types contravariant).

```ts
type Handler<T> = (x: T) => void;
// Handler<Animal> is assignable to Handler<Cat> (params: contravariant)
```

**Interview value:** naming it precisely shows real TS depth; relate it to "a callback for all animals can stand in for a callback needing cats, but a callback for only cats can't serve the animals callback."

---

## Q595: What are function overloads? When do you use them?

**Overloads** declare multiple signatures for one implementation — the implementation is checked against the union, and callers get the precise return type.

```ts
function parse(input: string): string;                    // overload 1
function parse(input: string[]): string[];                // overload 2
function parse(input: string | string[]): string | string[] {  // impl
  return typeof input === "string" ? input.trim() : input.map(s => s.trim());
}
const a = parse(" x ");    // string
const b = parse(["a", "b"]); // string[]
```

**When to use:** the same function legitimately behaves differently per input type (mapped by argument shape, not just union-typed — overloads give *per-call* narrowing that a single union signature can't). **When NOT:** prefer union/optional params + generics for most cases — overloads add complexity. Classic real case: `fetch`-style APIs with optional options that change the return type, or a function accepting a string OR an object with different results (like Axios).

---

## Q596: What are utility types you'd use with a React component?

Typing component props precisely with the standard utilities:

```ts
type Candidate = { id: string; name: string; email: string; score?: number; status: string };

type CardProps = {
  candidate: Candidate;
  onShortlist: (id: string) => void;
};

// child component that only needs a slice:
const ScoreBadge = ({ candidate }: { candidate: Pick<Candidate, "id" | "score"> }) => ...;

// optional handler:
type WithOptionalShortlist = Partial<Pick<CardProps, "onShortlist">>;

// readonly input to avoid mutation bugs:
type ReadonlyCandidate = Readonly<Candidate>;

// event handlers:
onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
onClick: React.MouseEventHandler<HTMLButtonElement>;
```

**Patterns worth naming:** `Pick`/`Omit` for prop slices, `React.ComponentProps<typeof Button>` to extend a component's props, `Record<Status, JSX.Element>` for status → icon maps, `UseState`-style generics, and `PropsWithChildren<P>`. Keep the **domain types** (`Candidate`) in one place and derive UI types from them (single source of truth, Q582).

---

## Q597: How do you type a fetch/API layer?

**The pattern:** generic `api<T>` returning typed data + typed errors + narrow result on failure.

```ts
type ApiError = { code: string; message: string; request_id?: string };

async function apiGet<T>(path: string, token?: string): Promise<T> {
  const res = await fetch(path, {
    headers: { Authorization: `Bearer ${token}`, Accept: "application/json" },
  });
  if (!res.ok) {
    const err = (await res.json().catch(() => null)) as ApiError | null;
    throw new ApiErrorResult(res.status, err?.message ?? res.statusText);
  }
  return (await res.json()) as T;
}

// usage — type flows from the call site:
const job = await apiGet<Job>("/api/v1/jobs/1");
const matches = await apiGet<MatchResult[]>("/api/v1/candidates/me/matches");
```

**Best practices:**
- **Never `any`** the response — decode with **zod** (`z.object({...}).parse(data)`) so runtime data *and* types agree; `z.infer<typeof Schema>` derives the TS type (Q582 link).
- Type errors with a discriminated union: `type Result<T> = { ok: true; data: T } | { ok: false; error: ApiError }`.
- Reflect FastAPI's response models (Pydantic) — the zod schema mirrors the Pydantic model.

---

## Q598: `type` vs `interface` — when do you use which?

**`interface`:** can be **extended/merged** (declaration merging — augment third-party types), best for **object shapes**, public API contracts, and OOP-style hierarchies.

```ts
interface Candidate { id: string; name: string }
interface Candidate { score?: number }   // merges (adds score)
interface PremiumCandidate extends Candidate { tier: "premium" }
```

**`type`:** **unions, intersections, primitives, tuples, functions, mapped/conditional types** — anything *not* an object, and object types you don't want merged.

```ts
type Status = "open" | "closed" | "archived";
type Id = string;
type [number, number]  // tuple — types only
type CardProps = Pick<Candidate, "id" | "name"> & { onClick: () => void };
```

**Rule (pragmatic):** use `interface` for object contracts (public API/DTOs) that may be extended/merged; use `type` for everything else (unions, tuples, computed types, aliases). Modern guidance: "interface for object shapes, type for the rest" — or pick `type` consistently for app-internal code and `interface` for public boundaries. **Know the merging difference** — it's the question they probe.

---

## Q599: What are the differences between `any`, `unknown`, `never`, and `void`?

- **`any`** — escape hatch: no type checking at all. **Avoid** except incremental migration/boundaries you consciously own.
- **`unknown`** — "some value of unknown type": you **must narrow before using** (type-safe `any`). Use for JSON.parse results, catch blocks, external input.
```ts
const data: unknown = JSON.parse(text);
if (typeof data === "object" && data && "email" in data) { /* narrowed */ }
```
- **`never`** — the bottom type: **no value** can be this type. Used for: functions that never return (`throw`, `process.exit`), exhaustive switch defaults, and as the "impossible" branch in conditionals.
```ts
function exhaustive(x: never): never { throw new Error(`unhandled: ${x}`); }
```
- **`void`** — the *return* type meaning "return value is not meaningful" (a function that returns `undefined`). Used for callbacks, effects, event handlers.

**Interview favorite:** `unknown` vs `any` ("any kills checking; unknown forces narrowing"), and `never` in exhaustive switch (catches new union members at compile time).