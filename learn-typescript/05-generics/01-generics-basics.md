# 01 — Generics Basics

## Table of Contents

1. [What Are Generics?](#what-are-generics)
2. [Why Generics?](#why-generics)
3. [The Problem Without Generics](#the-problem-without-generics)
4. [Type Parameters (T, K, V, U, R)](#type-parameters)
5. [The Generic Identity Function](#the-generic-identity-function)
6. [Generic Inference](#generic-inference)
7. [Multiple Type Parameters](#multiple-type-parameters)
8. [Naming Conventions](#naming-conventions)
9. [Generic vs `any`](#generic-vs-any)
10. [Best Practices](#best-practices)
11. [Interview Questions](#interview-questions)

---

## What Are Generics?

Generics allow you to write **reusable, type-safe** code components that work across
multiple types while preserving type information. They are essentially **type-level
parameters** — just as functions accept value parameters, generics accept type
parameters.

```typescript
// A function that accepts a value of ANY type
// and returns it back — but with full type safety.
function identity<T>(value: T): T {
  return value;
}

const num = identity<number>(42);        // type: number
const str = identity<string>("hello");   // type: string
const obj = identity({ a: 1, b: 2 });   // type: { a: number, b: number }
```

Think of `T` as a **placeholder** for a type that gets filled in at the call site.

---

## Why Generics?

Without generics you are forced into one of three bad options:

| Approach | Problem |
|---|---|
| Use `any` | Lose all type safety |
| Use `unknown` | Lose convenience — must narrow everywhere |
| Write duplicate functions | One per type — not scalable |

Generics solve all three problems: they preserve type safety, keep convenience, and
eliminate duplication.

---

## The Problem Without Generics

```typescript
// BAD: using any
function identityAny(value: any): any {
  return value;
}

const result = identityAny("hello");
result.toUpperCase(); // works at compile time but any[] would also "work"
// No type safety at all.

// BAD: duplicating
function identityString(value: string): string {
  return value;
}
function identityNumber(value: number): number {
  return value;
}
// Doesn't scale to 10, let alone 100 types.

// GOOD: generic
function identityGeneric<T>(value: T): T {
  return value;
}
// One implementation, every type, full safety.
```

---

## Type Parameters

TypeScript has **conventional** single-letter names for type parameters. These are
not keywords — they can be any valid identifier — but the conventions communicate
intent.

| Parameter | Common Meaning |
|---|---|
| `T` | **T**ype — the primary generic type |
| `U` | **U**nused / second type (follows T) |
| `V` | **V**alue (often used with `K` for key-value maps) |
| `K` | **K**ey |
| `R` | **R**eturn type |
| `E` | **E**lement (common in collection types) |
| `P` | **P**roperty |
| `N` | **N**umber |

```typescript
function map<T, R>(items: T[], fn: (item: T) => R): R[] {
  return items.map(fn);
}

const lengths = map(["hello", "world"], (s) => s.length);
// lengths: number[]
```

You can also use **meaningful names** instead of single letters:

```typescript
function getProperty<TObj, TKey extends keyof TObj>(
  obj: TObj,
  key: TKey
): TObj[TKey] {
  return obj[key];
}
```

Meaningful names improve readability in complex signatures. There is no performance
difference.

---

## The Generic Identity Function

The identity function is the "hello world" of generics. It takes a value and
returns it unchanged — but the generic signature preserves the input type.

```typescript
function identity<T>(value: T): T {
  return value;
}

// Explicit type argument
const a = identity<number>(42);            // number

// Let TypeScript infer the type
const b = identity("hello");              // string

// Works with complex types too
interface User {
  id: number;
  name: string;
}

const user = identity<User>({ id: 1, name: "Alice" });
// user.name is typed as string, user.id as number
```

### Arrow Function Version

```typescript
const identity = <T>(value: T): T => value;

// ⚠️ In .tsx files, the <T> can confuse JSX parsing.
// Workaround: use a trailing comma or constraint.
const identity = <T,>(value: T): T => value;
const identity = <T extends unknown>(value: T): T => value;
```

---

## Generic Inference

TypeScript can **infer** the type parameter from the argument you pass. You do not
always need to specify the type argument explicitly.

```typescript
function wrap<T>(value: T): { value: T; timestamp: number } {
  return { value, timestamp: Date.now() };
}

// TypeScript infers T = number
const result = wrap(42);
// result.value: number
// result.timestamp: number

// TypeScript infers T = string[]
const result2 = wrap(["a", "b", "c"]);
// result2.value: string[]
```

### When Inference Fails

Sometimes inference gives you a type that is too broad or too narrow. In those cases,
provide the type argument explicitly:

```typescript
function createPair<T>(a: T, b: T): [T, T] {
  return [a, b];
}

// TypeScript infers T = string | number (union)
const pair = createPair("hello", 42);
// pair: [string | number, string | number]

// If you want strict typing, provide T explicitly:
const strictPair = createPair<string>("hello", "world");
// strictPair: [string, string]
```

### Inference from Context

TypeScript infers generic types from **contextual positions** such as callback
parameters:

```typescript
function filter<T>(items: T[], predicate: (item: T) => boolean): T[] {
  return items.filter(predicate);
}

// T is inferred from the array, not the callback
const numbers = [1, 2, 3, 4, 5];
const evens = filter(numbers, (n) => n % 2 === 0);
// T = number, evens: number[]
```

---

## Multiple Type Parameters

Functions and types can have **multiple** type parameters separated by commas.

```typescript
function merge<T, U>(obj1: T, obj2: U): T & U {
  return { ...obj1, ...obj2 };
}

const merged = merge({ name: "Alice" }, { age: 30 });
// merged: { name: string } & { age: number }
// merged.name — string
// merged.age  — number
```

### Real-World: A `map` Function

```typescript
function map<TInput, TOutput>(
  items: TInput[],
  transform: (item: TInput) => TOutput
): TOutput[] {
  const result: TOutput[] = [];
  for (const item of items) {
    result.push(transform(item));
  }
  return result;
}

const lengths = map(["hello", "world"], (s) => s.length);
// lengths: number[]

const uppercased = map([1, 2, 3], (n) => n.toString());
// uppercased: string[]
```

### Real-World: A `reduce` Function

```typescript
function reduce<TInput, TAccumulator>(
  items: TInput[],
  reducer: (acc: TAccumulator, item: TInput) => TAccumulator,
  initialValue: TAccumulator
): TAccumulator {
  let accumulator = initialValue;
  for (const item of items) {
    accumulator = reducer(accumulator, item);
  }
  return accumulator;
}

const sum = reduce([1, 2, 3, 4], (acc, n) => acc + n, 0);
// sum: number (= 10)

const grouped = reduce(
  ["apple", "banana", "avocado"],
  (acc, word) => {
    const firstLetter = word[0];
    return { ...acc, [firstLetter]: [...(acc[firstLetter] ?? []), word] };
  },
  {} as Record<string, string[]>
);
// grouped: { a: string[], b: string[] }
```

---

## Naming Conventions

### Single-Letter Convention

Use single letters for short, obvious contexts:

```typescript
function identity<T>(value: T): T {
  return value;
}
```

### Meaningful Names for Complex Signatures

When signatures grow complex, switch to descriptive names:

```typescript
type EventHandler<TEvent extends string, TPayload> = {
  [K in TEvent]: (payload: TPayload) => void;
};

function createStore<TState, TAction extends string>(
  initialState: TState,
  reducer: (state: TState, action: TAction) => TState
) {
  let state = initialState;
  return {
    getState: () => state,
    dispatch: (action: TAction) => {
      state = reducer(state, action);
    },
  };
}
```

### Rules

- Type parameter names must be **valid identifiers** (no spaces, no dashes).
- They **shadow** outer types of the same name within their scope.
- They are **scoped** to the generic declaration (function, interface, class, type).

---

## Generic vs `any`

| Feature | `any` | Generic `<T>` |
|---|---|---|
| Type safety | ❌ None | ✅ Full |
| Inference | ❌ No | ✅ Yes |
| Reusability | ⚠️ Accidental | ✅ Intentional |
| IDE support | ❌ Minimal | ✅ Autocomplete, error checking |
| Runtime cost | Same | Same (erased at compile time) |

```typescript
// any: type safety is gone
function processAny(value: any): any {
  return value.foo.bar.baz; // no error at compile time, crashes at runtime
}

// generic: full type safety
function processGeneric<T extends { foo: { bar: { baz: string } } }>(
  value: T
): T {
  return value.foo.bar.baz; // TypeScript knows this structure exists
}
```

**Rule of thumb**: if you find yourself writing `any`, ask whether a generic
parameter would be more appropriate.

---

## Best Practices

1. **Prefer inference** — only provide type arguments when inference gives the wrong
   type.
2. **Constrain early** — use `extends` to narrow the type parameter when the function
   only works with a subset of types.
3. **Keep it simple** — avoid more than 3 type parameters; if you need more, refactor
   into multiple functions or use an interface.
4. **Use meaningful names** in complex signatures; single letters in simple ones.
5. **Avoid `any` as a type parameter** — that defeats the purpose of generics.
6. **Document edge cases** — generics can make error messages cryptic; add JSDoc to
   clarify intent.

---

## Interview Questions

**Q1: What is a generic in TypeScript?**

A generic is a type-level parameter that allows you to write reusable code that works
with a variety of types while preserving type safety. It is erased at runtime and has
zero performance cost.

**Q2: Why use generics over `any`?**

`any` disables type checking. Generics preserve it — the compiler knows exactly what
type flows through the code, enabling autocomplete, compile-time error detection, and
refactoring safety.

**Q3: What are the conventional type parameter names?**

`T` (Type), `U` (second type), `V` (Value), `K` (Key), `R` (Return), `E` (Element).
Any valid identifier works, but conventions aid readability.

**Q4: Can TypeScript infer generic types?**

Yes. TypeScript infers type parameters from function arguments, contextual positions
(callbacks), and return type usage. You only need to provide explicit type arguments
when inference is ambiguous.

**Q5: What is the difference between `<T>` and `<T extends unknown>`?**

Functionally identical. `<T>` is shorthand for `<T extends unknown>`. The explicit
form is sometimes used in `.tsx` files to avoid JSX parsing conflicts.
