# Static blocks

> Phase 2 · Module 12 · Classes

**TL;DR** — `static {}` blocks run once when the class is evaluated and allow multi-step static initialization with access to private statics.

## Syntax
```ts
class C {
  static readonly value: string;
  static {
    C.value = "initialized";
  }
}
```

## Examples
### Basic
```ts
class Config {
  static readonly version: string;

  static {
    Config.version = "1.0.0";
  }
}

console.log(Config.version); // 1.0.0
```

### Practical
```ts
class FeatureFlags {
  static readonly enabled: ReadonlySet<string>;

  static {
    const flags = new Set<string>(["search", "beta-ui"]);
    if (flags.has("beta-ui")) {
      flags.add("preview");
    }
    FeatureFlags.enabled = flags;
  }

  static isOn(flag: string): boolean {
    return FeatureFlags.enabled.has(flag);
  }
}

console.log(FeatureFlags.isOn("preview")); // true
```

### Advanced / edge cases
```ts
class Matrix {
  static readonly size: number;
  static readonly identity: number[][];

  static {
    Matrix.size = 3;
    Matrix.identity = Array.from({ length: Matrix.size }, (_, row) =>
      Array.from({ length: Matrix.size }, (_, col) => (row === col ? 1 : 0)),
    );
  }
}

console.log(Matrix.identity);
// [[1,0,0],[0,1,0],[0,0,1]]

class Secrets {
  static #token: string;

  static {
    Secrets.#token = "generated-once"; // ✅ access to private static
  }

  static reveal(): string {
    return Secrets.#token;
  }
}

console.log(Secrets.reveal()); // generated-once
```

## Key points
- Static blocks execute once, in source order, when the class definition is evaluated.
- They can assign to static fields, including `readonly` and `#private` ones.
- `this` inside a static block refers to the class constructor.
- Returning a value from a static block is not allowed.
- Multiple static blocks run sequentially.

## Gotchas
- Side effects in static blocks run at import time, which can surprise consumers.
- Throwing inside a static block makes the whole class definition fail.
- Static blocks cannot use class type parameters.

## Best practice
- Use static blocks for derived constants and validation that cannot be expressed inline.
- Keep them deterministic and free of I/O so imports stay predictable.
