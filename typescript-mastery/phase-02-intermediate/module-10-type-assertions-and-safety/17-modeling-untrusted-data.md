# Modeling Untrusted Data

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — Model raw input as `unknown` and only construct trusted types after successful validation.

## Syntax

```ts
type Raw = unknown;
type Trusted<T> = T & { readonly __validated: unique symbol };
```

## Examples

### Basic

```ts
type User = { id: number; name: string };

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function isUser(value: unknown): value is User {
  if (!isRecord(value)) return false;
  return typeof value.id === "number" && typeof value.name === "string";
}

const input: unknown = { id: 1, name: "Ada" };
const user: User | null = isUser(input) ? input : null;
console.log(user?.name); // "Ada"
```

### Practical

```ts
declare const validated: unique symbol;
type Validated<T> = T & { readonly [validated]: true };

type User = { id: number; name: string };
type ValidUser = Validated<User>;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

function validateUser(value: unknown): ValidUser | null {
  if (!isRecord(value)) return null;
  if (typeof value.id !== "number" || typeof value.name !== "string") return null;
  return { id: value.id, name: value.name } as ValidUser; // ✅ confined to the validator
}

function render(user: ValidUser): string {
  return `${user.name} (#${user.id})`;
}

const result = validateUser({ id: 1, name: "Ada" });
if (result) console.log(render(result)); // "Ada (#1)"
```

### Advanced / edge cases

```ts
type RemoteData<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

type User = { id: number; name: string };

function view(state: RemoteData<User>): string {
  switch (state.status) {
    case "idle":
      return "Nothing loaded";
    case "loading":
      return "Loading…";
    case "success":
      return state.data.name; // ✅ discriminated union narrows `data`
    case "error":
      return state.error.message;
  }
}

console.log(view({ status: "success", data: { id: 1, name: "Ada" } })); // "Ada"
```

## Key points

- Untrusted input starts as `unknown`, never `any` or a domain type.
- Validators transform `unknown` into a trusted type or an error.
- Branded types prevent raw and validated values from being mixed accidentally.
- Discriminated unions model async and remote states explicitly.
- Keep one validation function per boundary type.

## Gotchas

- Reusing a domain type for raw data erases the trust distinction.
- Mutating a validated object can break invariants the brand promised.
- A brand created by assertion is only as trustworthy as the validator behind it.

```ts
const fake = { id: 1, name: 42 } as ValidUser;
// ✅ compiles, but the brand is a lie — validation never ran
```

## Best practice

- Export the validator and the trusted type together; keep construction private.
- Make validated types deeply readonly when mutation could invalidate them.
