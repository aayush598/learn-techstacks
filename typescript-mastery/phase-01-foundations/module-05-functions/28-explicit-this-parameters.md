# Explicit `this` Parameters

> Phase 1 · Module 05 · Functions

**TL;DR** — Declare a fake first parameter named `this` to state what the receiver must be, without changing arity.

## Syntax
```ts
function fn(this: Context, param: Type): ReturnType { /* ... */ }
```

## Examples
### Basic
```ts
interface Counter {
  count: number;
}

function increment(this: Counter, by: number): number {
  this.count += by;
  return this.count;
}

const c: Counter = { count: 0 };
console.log(increment.call(c, 2)); // 2
```

### Practical
```ts
type Button = { label: string; disabled: boolean };

function click(this: Button): string {
  return this.disabled ? "blocked" : `clicked ${this.label}`;
}

const b: Button = { label: "OK", disabled: false };
console.log(click.call(b)); // "clicked OK"
```

### Advanced / edge cases
```ts
// `this` is erased at runtime and not counted in arity
function tag(this: { name: string }, suffix: string): string {
  return this.name + suffix;
}

// ✅ methods can declare their receiver too
const obj = {
  name: "Ada",
  greet(this: { name: string }): string {
    return `Hi ${this.name}`;
  },
};

// ❌ Error: 'this' context of type 'void' is not assignable
const detached = obj.greet;
// detached();
```

## Key points
- `this` parameters are type-only and disappear at runtime.
- They do not count toward the parameter list length.
- Calling with `.call`, `.apply`, or a method receiver checks the `this` type.
- `noImplicitThis` under `strict` flags untyped `this`.

## Gotchas
- `// ❌ Error:` `increment(2)` without a receiver when `this: Counter` is declared.
- Detached methods lose their receiver and fail the `this` check.
- Arrow functions cannot declare a `this` parameter.

## Best practice
- Use `this` parameters on functions meant to be called as methods.
- Prefer plain parameters when a function does not need `this`.
