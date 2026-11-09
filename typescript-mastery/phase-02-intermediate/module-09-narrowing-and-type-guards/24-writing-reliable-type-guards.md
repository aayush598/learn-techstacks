# Writing reliable type guards

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — A reliable type guard is pure, checks every required field, handles `null`, and is tested because the compiler trusts it blindly.

## Syntax
```ts
function isModel(value: unknown): value is Model {
  return runtimeChecks(value);
}
```

## Examples
### Basic
```ts
type User = { id: string; name: string };

function isUser(value: unknown): value is User {
  if (typeof value !== "object" || value === null) return false;
  const user = value as Record<string, unknown>;
  return typeof user.id === "string" && typeof user.name === "string";
}
```

### Practical
```ts
type Post = {
  id: string;
  title: string;
  tags: string[];
  published: boolean;
};

function isPost(value: unknown): value is Post {
  if (typeof value !== "object" || value === null) return false;
  const post = value as Record<string, unknown>;
  return (
    typeof post.id === "string" &&
    typeof post.title === "string" &&
    Array.isArray(post.tags) &&
    post.tags.every((tag) => typeof tag === "string") &&
    typeof post.published === "boolean"
  );
}

function assertPost(value: unknown): asserts value is Post {
  if (!isPost(value)) {
    throw new TypeError("Invalid post payload");
  }
}
```

### Advanced / edge cases
```ts
type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: Error };

function isResult<T>(
  value: unknown,
  isValue: (input: unknown) => input is T,
): value is Result<T> {
  if (typeof value !== "object" || value === null) return false;
  const result = value as Record<string, unknown>;
  if (result.ok === true) return isValue(result.value);
  if (result.ok === false) return result.error instanceof Error;
  return false;
}

const isNumber = (v: unknown): v is number => typeof v === "number";

function readResult(input: unknown): number {
  if (isResult(input, isNumber)) {
    return input.ok ? input.value : 0; // ✅ Result<number>
  }
  return 0;
}
```

## Key points
- Check `typeof`, `null`, arrays, and each required field.
- Keep guards pure and side-effect free.
- Prefer predicates for composition; add `asserts` wrappers when you need to throw.
- Test guards with valid, invalid, and edge-case inputs.
- Never widen a guard's claim beyond what it verifies.

## Gotchas
- The compiler cannot detect a guard that lies.
- Checking only one field leaves the type unsound.
- `// ❌ Error:` `function isPost(value: unknown): value is Post { return true; }` compiles but is unsound.

## Best practice
- Build guards from small, reusable validators.
- Pair every predicate guard with a test suite.
