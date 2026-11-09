# Combining Multiple Types

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — Build larger unions by composing aliases, generics, and existing unions into one type.

## Syntax
```ts
type Combined = ExistingA | ExistingB | Extra;
```

## Examples
### Basic
```ts
type TextInput = string;
type NumericInput = number;
type DateInput = Date;

type FieldValue = TextInput | NumericInput | DateInput;

// ✅ aliases make the union readable
const createdAt: FieldValue = new Date();
```

### Practical
```ts
type ApiId = string | number;
type ApiError = { code: string; message: string };

type ApiResponse<T> = { data: T } | ApiError;

function isError<T>(response: ApiResponse<T>): response is ApiError {
  return "code" in response;
}

// ✅ reuse the same generic union at many call sites
const ok: ApiResponse<string[]> = { data: ["a", "b"] };
const failed: ApiResponse<string[]> = { code: "E_NET", message: "offline" };

console.log(isError(ok), isError(failed));
```

### Advanced / edge cases
```ts
type Brand<T, B extends string> = T & { readonly __brand: B };
type UserId = Brand<string, "UserId">;
type PostId = Brand<string, "PostId">;

type EntityId = UserId | PostId;

// ✅ branded members stay distinct even though both wrap string
declare const id: EntityId;
if (typeof id === "string") {
  // still UserId | PostId after the typeof check
  console.log(id);
}
```

## Key points
- Compose unions from named aliases rather than repeating inline shapes.
- Generic unions let one definition serve many payload types.
- Branded types keep structurally identical primitives distinguishable.
- Flattening and deduplication happen automatically.
- Keep each alias focused on one concern.

## Gotchas
- Widening an alias to `string` too early loses literal and branded information.
- Intersecting aliases with conflicting members can produce `never`.

```ts
type A = { kind: "a" };
type B = { kind: "b" };

// ❌ Error: Type '"a"' is not assignable to type '"b"'.
const bad: A & B = { kind: "a" };
```

## Best practice
- Name unions that appear in more than one place.
- Combine aliases at the narrowest useful level, then widen at boundaries.
