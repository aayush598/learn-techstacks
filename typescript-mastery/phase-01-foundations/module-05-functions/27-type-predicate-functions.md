# Type Predicate Functions

> Phase 1 · Module 05 · Functions

**TL;DR** — A type predicate returns `value is T` so a successful boolean check narrows the argument's type.

## Syntax
```ts
function isType(value: unknown): value is Type { /* ... */ }
```

## Examples
### Basic
```ts
function isString(value: unknown): value is string {
  return typeof value === "string";
}

function upper(value: unknown): string {
  if (isString(value)) return value.toUpperCase(); // ✅ narrowed
  return "";
}
```

### Practical
```ts
type Cat = { kind: "cat"; meow(): void };
type Dog = { kind: "dog"; bark(): void };
type Pet = Cat | Dog;

function isCat(pet: Pet): pet is Cat {
  return pet.kind === "cat";
}

function speak(pet: Pet): void {
  if (isCat(pet)) pet.meow();
  else pet.bark(); // ✅ narrowed to Dog
}
```

### Advanced / edge cases
```ts
// Predicate over an array filters to the narrowed type
function isNonNull<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

const values = [1, null, 2, undefined].filter(isNonNull); // number[]

// ✅ predicated `this`
class Box<T> {
  value?: T;
  hasValue(): this is { value: T } {
    return this.value !== undefined;
  }
}
```

## Key points
- `value is T` narrows in the true branch; the false branch narrows the complement when possible.
- Predicates work with `filter`, `find`, and user-defined guards.
- The predicate must be truthful; the compiler trusts it.
- `this is T` narrows the receiver in classes.

## Gotchas
- `// ❌ Error:` a boolean-returning function is not a guard unless its return type is a predicate.
- Lying predicates cause runtime bugs the type system cannot catch.
- `// ❌ Error:` `function isT(v: T): v is T` on a generic without care can over-narrow.

## Best practice
- Return a bare boolean expression whose logic matches the predicate exactly.
- Use `value is NonNullable<...>` helpers for array filtering.
