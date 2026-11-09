# Method return types

> Phase 2 · Module 12 · Classes

**TL;DR** — Annotate return types on public methods to lock the contract and catch accidental widening or missing paths.

## Syntax
```ts
class C {
  method(): Type {
    // must return Type
  }
}
```

## Examples
### Basic
```ts
class MathUtil {
  double(n: number): number {
    return n * 2;
  }

  isEven(n: number): boolean {
    return n % 2 === 0;
  }
}
```

### Practical
```ts
type User = { id: string; name: string };

class UserService {
  constructor(private users: User[] = []) {}

  find(id: string): User | undefined {
    return this.users.find((u) => u.id === id);
  }

  all(): readonly User[] {
    return this.users;
  }

  count(): number {
    return this.users.length;
  }
}
```

### Advanced / edge cases
```ts
class Tree {
  constructor(
    readonly value: number,
    readonly children: Tree[] = [],
  ) {}

  sum(): number {
    return this.value + this.children.reduce((acc, c) => acc + c.sum(), 0);
  }

  fail(): never {
    throw new Error("unreachable");
  }
}

class Builder {
  private parts: string[] = [];

  add(part: string): this {
    this.parts.push(part);
    return this;
  }

  build(): string {
    return this.parts.join("-");
  }
}

const out = new Builder().add("a").add("b").build();
console.log(out); // a-b
```

## Key points
- Without an annotation, the return type is inferred from the implementation.
- `void` means the caller should ignore the result, not that nothing can be returned.
- `never` describes a method that never returns normally.
- `this` as a return type refers to the concrete instance type.
- Async methods must return `Promise<T>`.

## Gotchas
- Recursive methods often need an explicit return annotation to avoid implicit `any`.
- Changing an inferred return type can silently break callers, so annotate public APIs.
- A `void`-returning callback may still be implemented with a value at runtime.

## Best practice
- Annotate every exported or public method return type.
- Prefer the narrowest accurate type, such as `readonly T[]` for exposed collections.
