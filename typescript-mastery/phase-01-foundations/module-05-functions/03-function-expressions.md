# Function Expressions

> Phase 1 · Module 05 · Functions

**TL;DR** — A function expression assigns an anonymous or named function to a variable and is typed through the variable's annotation.

## Syntax
```ts
const fn = function name(param: Type): ReturnType {
  return value;
};
```

## Examples
### Basic
```ts
const double = function (n: number): number {
  return n * 2;
};

console.log(double(4)); // 8
```

### Practical
```ts
type Comparator = (a: number, b: number) => number;

const ascending: Comparator = function (a, b) {
  // ✅ params inferred from Comparator
  return a - b;
};

console.log([3, 1, 2].sort(ascending)); // [1, 2, 3]
```

### Advanced / edge cases
```ts
// Named function expressions can recurse by their own name
const factorial = function fact(n: number): number {
  return n <= 1 ? 1 : n * fact(n - 1);
};

// ✅ the inner name is not added to the outer scope
console.log(factorial(5)); // 120
// console.log(fact(5)); // ❌ name not visible here
```

## Key points
- Function expressions are not hoisted; the variable exists only after the assignment.
- Named expressions help with recursion and stack traces.
- The variable's type annotation drives contextual typing of parameters.
- `const` prevents reassignment but not mutation of underlying data.

## Gotchas
- `// ❌ Error:` `const f = function (a: number) { return a; }; f = function () {};` — reassigning a `const`.
- Without an annotation, a recursive expression may infer circularly.
- Arrow functions are often preferred when `this` binding is not needed.

## Best practice
- Prefer `const` for function expressions to avoid accidental reassignment.
- Annotate the variable when the intent should be a specific function type.
