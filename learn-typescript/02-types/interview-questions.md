# TypeScript Types — Interview Questions

## Table of Contents

1. [Primitive Types](#primitive-types)
2. [any, unknown, never, void](#any-unknown-never-void)
3. [Arrays and Tuples](#arrays-and-tuples)
4. [Enums](#enums)
5. [Objects](#objects)
6. [Type Aliases and Interfaces](#type-aliases-and-interfaces)
7. [Union and Intersection Types](#union-and-intersection-types)
8. [Literal Types](#literal-types)
9. [Type Guards](#type-guards)
10. [Type Assertions](#type-assertions)
11. [Non-Null Assertion, Optional Chaining, Nullish Coalescing](#non-null-assertion-optional-chaining-nullish-coalescing)
12. [Mixed / Advanced](#mixed--advanced)

---

## Primitive Types

### Q1: What are the primitive types in TypeScript?

**Answer:** TypeScript has 7 primitive types: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, and `bigint`. Primitives are immutable — operations on them return new values.

```typescript
const s: string = "hello";
const n: number = 42;
const b: boolean = true;
const sym: symbol = Symbol("id");
const big: bigint = 100n;
```

### Q2: What is the difference between `string` and `String`?

**Answer:** `string` (lowercase) is the primitive type. `String` (uppercase) is the wrapper object type. Always use `string`. The wrapper type can cause unexpected comparison behavior: `"hello" === new String("hello")` is `false` because one is a primitive and the other is an object.

### Q3: Can `null` be assigned to `string` type?

**Answer:** Only with `strictNullChecks: false`. With `strictNullChecks: true` (recommended), you must use `string | null` to allow null values. This flag makes TypeScript much safer by forcing you to handle nullability explicitly.

### Q4: What is `typeof null` in JavaScript and how does TypeScript handle it?

**Answer:** `typeof null` returns `"object"` — a historical bug in JavaScript. TypeScript inherits this behavior. To check for null, use `value === null` instead of `typeof value === "object"`.

---

## any, unknown, never, void

### Q5: What is the difference between `any` and `unknown`?

**Answer:** `any` disables all type checking — you can assign it to anything and call any methods on it. `unknown` accepts any value but requires type narrowing before use. `unknown` is the type-safe alternative to `any`.

```typescript
const a: any = "hello";
a.toUpperCase(); // OK
a.foo.bar();      // OK (runtime crash)

const u: unknown = "hello";
// u.toUpperCase(); // Error — must narrow first
if (typeof u === "string") {
  u.toUpperCase(); // OK
}
```

### Q6: When would you use `never`?

**Answer:** `never` represents values that never occur. Use it for:
- Functions that always throw or have infinite loops
- Exhaustive checking in switch statements
- Conditional types that filter out types (e.g., `Exclude<T, U>`)

```typescript
function throwError(msg: string): never {
  throw new Error(msg);
}

function assertNever(value: never): never {
  throw new Error(`Unexpected: ${value}`);
}
```

### Q7: What is the difference between `void` and `undefined`?

**Answer:** `void` is the return type of functions that don't return a value. `undefined` is a specific value. A function typed as `() => void` can return any value (it's ignored), but `() => undefined` must explicitly return `undefined`.

### Q8: What is `noImplicitAny`?

**Answer:** A TypeScript compiler option that prevents variables, parameters, and return types from being implicitly typed as `any`. When enabled, every declaration must have an explicit type annotation or be inferrable. It catches bugs where TypeScript would silently allow any operation on untyped values.

---

## Arrays and Tuples

### Q9: What is the difference between `Array<T>` and `T[]`?

**Answer:** They are completely equivalent. `T[]` is syntactic sugar for `Array<T>`. Most codebases prefer `T[]` for its brevity. Both produce the same type.

### Q10: How do you make an array readonly in TypeScript?

**Answer:** Three ways:
```typescript
const a: readonly number[] = [1, 2, 3];
const b: ReadonlyArray<number> = [1, 2, 3];
const c = [1, 2, 3] as const; // readonly [1, 2, 3] (tuple)
```
The `readonly` modifier prevents mutation methods (`push`, `pop`, `splice`, etc.) from being called.

### Q11: What is a tuple and how is it different from an array?

**Answer:** A tuple is a fixed-length array where each element has a specific type at a specific index. An array has a variable length with all elements of the same type. Tuple access returns the exact type at that index, while array access returns the union of all element types.

```typescript
const tuple: [string, number] = ["Alice", 30]; // Fixed
const arr: (string | number)[] = ["Alice", 30]; // Variable
```

### Q12: What are variadic tuple types?

**Answer:** A TypeScript 4.0+ feature that allows tuple types to use rest elements and spread other tuple types. They enable powerful type-level manipulation like concatenation, reversal, and mapping over tuples.

```typescript
type Concat<A extends any[], B extends any[]> = [...A, ...B];
type Result = Concat<[1, 2], [3, 4]>; // [1, 2, 3, 4]
```

---

## Enums

### Q13: What is a TypeScript enum?

**Answer:** An enum defines a set of named constants. TypeScript supports numeric (auto-incremented) and string enums. Numeric enums support reverse mapping (value to name).

```typescript
enum Direction {
  Up,     // 0
  Down,   // 1
  Left,   // 2
  Right,  // 3
}

enum Color {
  Red = "RED",
  Green = "GREEN",
  Blue = "BLUE",
}
```

### Q14: What is the difference between a regular enum and a const enum?

**Answer:** A regular enum generates a JavaScript object at runtime. A const enum is fully erased at compile time and values are inlined. Const enums have limitations: no reverse mapping, no iteration, and issues with `--isolatedModules`.

### Q15: Why might you prefer string literal unions over enums?

**Answer:** String literal unions have zero runtime overhead, are tree-shakeable, and provide the same type safety. Enums generate JavaScript objects and are not tree-shakeable. The `as const` object + union type pattern gives you both runtime values and types.

---

## Objects

### Q16: What is structural typing in TypeScript?

**Answer:** Structural typing means object compatibility is determined by shape (structure) rather than explicit declaration. If object A has all the properties of object B (with compatible types), A is assignable to B, regardless of their type names.

### Q17: What is excess property checking?

**Answer:** A special check that applies to object literal assignments. It catches typos and extra properties that don't exist on the target type. It doesn't apply to variable assignments or spreads — only object literals.

```typescript
interface Options { color: string; width: number; }
// const opts: Options = { color: "red", width: 100, height: 200 }; // Error!
const obj = { color: "red", width: 100, height: 200 };
const opts: Options = obj; // OK — variable, not literal
```

### Q18: What is the difference between `{}` and `Record<string, never>`?

**Answer:** `{}` accepts any non-nullish value (string, number, object, etc.). `Record<string, never>` only accepts an empty object `{}`. Use `Record<string, never>` when you want truly empty objects.

---

## Type Aliases and Interfaces

### Q19: Explain the difference between type aliases and interfaces.

**Answer:**

| Feature | Interface | Type Alias |
|---------|-----------|------------|
| Declaration merging | ✅ Yes | ❌ No |
| Extends | ✅ Yes | ❌ (use `&`) |
| Implements in classes | ✅ Yes | ❌ No |
| Union types | ❌ No | ✅ Yes |
| Tuple types | ❌ No | ✅ Yes |
| Computed properties | ❌ No | ✅ Yes |
| Error messages | Better for objects | Can be verbose |

Use interfaces for object shapes that may be extended or implemented. Use type aliases for unions, tuples, mapped types, and computed properties.

### Q20: What is declaration merging?

**Answer:** A feature where multiple interface declarations with the same name are automatically merged into a single interface. This is useful for augmenting third-party library types (e.g., adding properties to Express Request) and splitting large interfaces across files.

### Q21: Can you implement a type alias in a class?

**Answer:** No. Only interfaces can be implemented by classes using the `implements` keyword. If you need to implement a type in a class, define it as an interface.

---

## Union and Intersection Types

### Q22: What is a union type?

**Answer:** A union type represents a value that can be one of several types, created with the `|` operator. `string | number` means the value can be either a string or a number.

### Q23: What is a discriminated union?

**Answer:** A union of object types that share a common discriminant property (a literal type field). TypeScript uses the discriminant to narrow the union and enable exhaustive checking.

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.radius ** 2;
    case "square": return shape.side ** 2;
  }
}
```

### Q24: What is the difference between `&` and `|`?

**Answer:** `&` (intersection) means ALL of the types — the value must satisfy every type. `|` (union) means ANY of the types — the value must satisfy at least one type. Intersection is more restrictive, union is less restrictive.

### Q25: What is exhaustive checking?

**Answer:** Using `never` in a default switch case to ensure all union members are handled. If a new member is added to the union and not handled in the switch, TypeScript produces a compile error.

```typescript
function handle(value: "a" | "b"): string {
  switch (value) {
    case "a": return "A";
    case "b": return "B";
    default: return assertNever(value); // Compile error if missing
  }
}
```

---

## Literal Types

### Q26: What are literal types?

**Answer:** Types that represent exactly one specific value. `"hello"` is a literal string type, `42` is a literal number type. They're created by using specific values instead of general types like `string` or `number`.

### Q27: How do you preserve literal types from runtime values?

**Answer:** Use `as const`:
```typescript
const x = "hello" as const; // "hello" (not string)
const arr = [1, 2, 3] as const; // readonly [1, 2, 3]
```
You can also use explicit type annotations or the `satisfies` operator.

### Q28: What are template literal types?

**Answer:** Types created by combining string literals and types using backtick syntax. They enable type-level string manipulation:
```typescript
type Color = "red" | "blue";
type ColorClass = `color-${Color}`; // "color-red" | "color-blue"
```

---

## Type Guards

### Q29: What are type guards in TypeScript?

**Answer:** Runtime checks that narrow the type within a control flow block. They include `typeof`, `instanceof`, `in`, custom type guards with `is`, and assertion functions.

### Q30: What is the difference between a type guard and a type assertion?

**Answer:** A type guard (`if (typeof x === "string")`) is a runtime check that safely narrows the type. A type assertion (`x as string`) is a compile-time hint that tells TypeScript to treat a value as a specific type without runtime verification. Type guards are safer.

### Q31: What is an assertion function?

**Answer:** A function that returns `void` and uses `asserts` to narrow a parameter's type. If the assertion fails, it throws an error. If it succeeds, the parameter is narrowed:
```typescript
function assertString(v: unknown): asserts v is string {
  if (typeof v !== "string") throw new Error("Expected string");
}
```

---

## Type Assertions

### Q32: What is `as const`?

**Answer:** A type assertion that makes values as narrow and immutable as possible. Objects become deeply readonly with literal types, arrays become readonly tuples. It's the primary way to get literal types from runtime values.

### Q33: What is `satisfies` and when would you use it?

**Answer:** `satisfies` (TS 4.9+) validates that a value matches a type while preserving the narrow literal type. Unlike type annotations, it doesn't widen types. Use it when you want type validation without losing literal types.

```typescript
const config = { mode: "production" } satisfies Record<string, string>;
// config.mode is "production" (not string)
```

### Q34: What is a non-null assertion?

**Answer:** The `!` operator tells TypeScript a value is not `null` or `undefined`. It's a compile-time hint with no runtime effect. It's dangerous because it can cause runtime crashes. Prefer optional chaining, nullish coalescing, or type guards.

---

## Non-Null Assertion, Optional Chaining, Nullish Coalescing

### Q35: What is the difference between `||` and `??`?

**Answer:** `||` triggers on all falsy values (`false`, `0`, `""`, `null`, `undefined`, `NaN`). `??` only triggers on `null` and `undefined`. This means `0 ?? "default"` returns `0`, while `0 || "default"` returns `"default"`.

### Q36: How do you handle null/undefined safely?

**Answer:** Multiple strategies:
1. Optional chaining (`?.`) for safe property access
2. Nullish coalescing (`??`) for default values
3. Type guards (`if (value !== null)`) for explicit narrowing
4. Assertion functions for preconditions
5. `strictNullChecks: true` compiler option

```typescript
function getLength(value: string | null): number {
  return value?.length ?? 0; // Safe
}
```

### Q37: What does `?.` return when it short-circuits?

**Answer:** `undefined`. For example, `null?.a` returns `undefined`, and `undefined?.a?.b` also returns `undefined`. The entire expression short-circuits — no side effects on the right-hand side are executed.

---

## Mixed / Advanced

### Q38: When would you use `any`?

**Answer:** Rarely. Acceptable cases:
1. During JavaScript-to-TypeScript migration (temporary)
2. Working with untyped third-party libraries (prefer `@types` first)
3. At API boundaries where type information is truly unknown (prefer `unknown`)
4. In test files for mock data (less critical)

### Q39: What is the `never` type used for in conditional types?

**Answer:** `never` is used as a filter in conditional types to remove members from unions:
```typescript
type Exclude<T, U> = T extends U ? never : T;
type Result = Exclude<"a" | "b" | "c", "a">; // "b" | "c"
```
The matching type is replaced with `never`, which disappears from the union.

### Q40: What is the difference between `readonly` and `Readonly<T>`?

**Answer:** `readonly` is a modifier applied to individual properties: `{ readonly x: number }`. `Readonly<T>` is a utility type that makes all properties of an object type readonly: `Readonly<{ x: number; y: number }>` becomes `{ readonly x: number; readonly y: number }`.

### Q41: How do you create a deeply readonly object type?

**Answer:** Use a recursive mapped type:
```typescript
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};
```
TypeScript 4.7+ also has built-in `Readonly` which is shallow — you need a custom type or library for deep readonly.

### Q42: What is the difference between `type` and `interface` for public APIs?

**Answer:** Interfaces are generally preferred for public APIs because they produce better error messages, support declaration merging for augmentation, and can be implemented by classes. Type aliases are better for unions, tuples, and computed types.

### Q43: What is `as const` and how does it differ from `readonly`?

**Answer:** `as const` makes values deeply readonly AND preserves literal types. `readonly` only makes properties immutable (not deep). `as const` on an array gives `readonly [1, 2, 3]`, while `readonly` on a property gives `readonly number[]`.

### Q44: How do you type a function that returns different types based on input?

**Answer:** Use function overloads or discriminated unions:
```typescript
// Overloads
function parse(input: string): string;
function parse(input: number): number;
function parse(input: string | number): string | number {
  return typeof input === "string" ? JSON.parse(input) : input.toString();
}

// Discriminated union
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };
```

### Q45: What is the `satisfies` operator and why was it added?

**Answer:** Added in TypeScript 4.9, `satisfies` validates that a value matches a type without widening it. Before `satisfies`, you had to choose between type annotation (validates but widens) and no annotation (preserves narrow type but no validation). `satisfies` gives you both: validation AND narrow types.
