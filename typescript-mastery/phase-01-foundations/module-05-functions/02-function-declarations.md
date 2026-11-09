# Function Declarations

> Phase 1 · Module 05 · Functions

**TL;DR** — A `function` statement is hoisted, names itself, and can carry explicit parameter and return annotations.

## Syntax
```ts
function name(param: Type): ReturnType {
  return value;
}
```

## Examples
### Basic
```ts
function square(n: number): number {
  return n * n;
}

// ✅ hoisted: callable before its declaration
console.log(square(3)); // 9
```

### Practical
```ts
function greet(name: string, title = "Mr."): string {
  return `Hello, ${title} ${name}`;
}

console.log(greet("Ada"));        // "Hello, Mr. Ada"
console.log(greet("Ada", "Dr.")); // "Hello, Dr. Ada"
```

### Advanced / edge cases
```ts
// Declarations merge — an overload set can be built from repeated declarations
function parse(input: string): number;
function parse(input: number): number;
function parse(input: string | number): number {
  return typeof input === "string" ? Number(input) : input;
}

// ✅ named function declarations keep their name in stack traces
console.log(parse("42")); // 42
```

## Key points
- Declarations are hoisted, so they can be used before their line.
- They create a named binding in the enclosing scope.
- Return type is inferred when omitted, but annotating documents intent.
- Multiple declarations with the same name form an overload set (with one implementation).

## Gotchas
- Block-scoped function declarations behave differently in strict mode than `var`-style hoisting.
- `// ❌ Error:` `function f(): void { return 1; }` — a `void` function cannot return a value.
- Duplicate implementations of the same declaration are an error.

## Best practice
- Annotate public/exported functions; let trivial local ones infer.
- Keep declarations small and use overloads only when the return type truly changes by input.
