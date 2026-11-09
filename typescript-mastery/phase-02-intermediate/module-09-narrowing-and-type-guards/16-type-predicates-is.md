# Type predicates (`is`)

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — `value is T` is the predicate return type that tells TypeScript to narrow `value` to `T` when it returns true.

## Syntax
```ts
function isFoo(value: unknown): value is Foo {
  return true;
}
```

## Examples
### Basic
```ts
type Fish = { swim: () => void };
type Bird = { fly: () => void };

function isFish(pet: Fish | Bird): pet is Fish {
  return "swim" in pet;
}

function move(pet: Fish | Bird): void {
  if (isFish(pet)) {
    pet.swim(); // ✅ Fish
  } else {
    pet.fly(); // ✅ Bird
  }
}
```

### Practical
```ts
type Success = { ok: true; value: string };
type Failure = { ok: false; error: string };

function isSuccess(result: Success | Failure): result is Success {
  return result.ok; // ✅ predicate matches discriminant
}

function unwrap(result: Success | Failure): string {
  if (isSuccess(result)) {
    return result.value; // ✅ Success
  }
  throw new Error(result.error); // ✅ Failure
}
```

### Advanced / edge cases
```ts
function isDefined<T>(value: T | undefined | null): value is T {
  return value !== undefined && value !== null;
}

function compact<T>(values: (T | null | undefined)[]): T[] {
  return values.filter(isDefined); // ✅ T[]
}

type ArrayElement<T> = T extends readonly (infer U)[] ? U : never;

function isArrayOf<T>(
  value: unknown,
  check: (item: unknown) => item is T,
): value is T[] {
  return Array.isArray(value) && value.every(check);
}

const isStringArray = (value: unknown): value is string[] =>
  isArrayOf(value, (item): item is string => typeof item === "string");
```

## Key points
- `x is T` narrows in the true branch; `x is T` false branch gets the complement.
- Works with generic predicates like `value is T`.
- Can combine with `asserts` for throwing guards.
- Predicate must be assignable to the parameter type.
- Arrow functions need an explicit predicate return type.

## Gotchas
- Returning `boolean` instead of a predicate prevents narrowing.
- A predicate on a property does not narrow the parent object.
- `// ❌ Error:` `function isString(v: unknown): v is string { return true; }` compiles, but the wrong logic breaks callers silently.

## Best practice
- Keep predicates narrow and side-effect free.
- Prefer predicate functions for `Array.prototype.filter`.
