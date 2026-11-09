# Definite Assignment Assertions

> Phase 2 · Module 10 · Type Assertions and Type Safety

**TL;DR** — A `!` on a declaration tells the compiler a variable or property will be assigned before use, disabling definite-assignment checks.

## Syntax

```ts
let value!: Type;
class Service {
  private dependency!: Dependency;
}
```

## Examples

### Basic

```ts
let userId!: number;

function init(): void {
  userId = 1;
}

init();
console.log(userId.toFixed()); // "1"
```

### Practical

```ts
type Database = { query(sql: string): unknown[] };

class UserRepository {
  private db!: Database; // initialized by `init` before any query

  init(db: Database): void {
    this.db = db;
  }

  findAll(): unknown[] {
    return this.db.query("SELECT * FROM users");
  }
}

const repo = new UserRepository();
repo.init({ query: () => [] });
console.log(repo.findAll()); // []
```

### Advanced / edge cases

```ts
// Frameworks often assign properties after construction.
class Controller {
  readonly name!: string;

  constructor() {
    // `name` is populated by a decorator or subclass after `super()`.
  }
}

// Use `declare` when a property exists only for typing.
class Config {
  declare readonly port: number;
}

console.log(typeof Controller, typeof Config);
```

## Key points

- `!` on a declaration suppresses `strictPropertyInitialization` errors.
- It asserts assignment will happen, not that it already happened.
- Works on `let`/`var` declarations and class fields, not on `const` values.
- It is distinct from the postfix non-null assertion on an expression.
- Common in dependency injection, frameworks, and lifecycle-based initialization.

## Gotchas

- If initialization never runs, the property is `undefined` at runtime.

```ts
class Config {
  port!: number;
}

const config = new Config();
console.log(config.port.toFixed());
// throws at runtime: Cannot read properties of undefined (reading 'toFixed')
```

- The assertion survives refactors even if the initializer is removed.
- Using `!` where a constructor assignment is possible hides a real ordering bug.

## Best practice

- Prefer constructor parameters or initializers so the compiler can verify assignment.
- Reserve `!` for lifecycle hooks you cannot express in the type system, and document them.
