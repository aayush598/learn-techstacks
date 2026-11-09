# `implements`

> Phase 2 · Module 12 · Classes

**TL;DR** — `implements` verifies that a class satisfies an interface's shape without inheriting any implementation.

## Syntax
```ts
class C implements Interface {
  // must provide all required members
}
```

## Examples
### Basic
```ts
interface Serializable {
  serialize(): string;
}

class User implements Serializable {
  constructor(readonly name: string) {}

  serialize(): string {
    return JSON.stringify({ name: this.name });
  }
}

console.log(new User("Ada").serialize()); // {"name":"Ada"}
```

### Practical
```ts
interface Clock {
  now(): Date;
}

class SystemClock implements Clock {
  now(): Date {
    return new Date();
  }
}

class FixedClock implements Clock {
  constructor(private readonly time: Date) {}

  now(): Date {
    return new Date(this.time);
  }
}

function logTime(clock: Clock): void {
  console.log(clock.now().toISOString());
}

logTime(new SystemClock());
logTime(new FixedClock(new Date("2026-01-01T00:00:00Z")));
```

### Advanced / edge cases
```ts
interface Config {
  readonly name: string;
  readonly retries: number;
}

class AppConfig implements Config {
  constructor(
    readonly name: string,
    readonly retries = 3,
  ) {}
}

class BadClock implements Clock {
  // ❌ Error: Property 'now' is private in type 'BadClock' but not in type 'Clock'.
  // private now(): Date { return new Date(); }
}

// ❌ Error: Class 'Incomplete' incorrectly implements interface 'Clock'.
// class Incomplete implements Clock {}
```

## Key points
- `implements` performs a structural check of the class instance type.
- Interfaces contribute types only; no code is inherited.
- A class can implement multiple interfaces.
- Extra members beyond the interface are allowed.
- `implements` is erased at runtime.

## Gotchas
- Implementing an interface does not make private members public.
- A class must provide every required member; optional interface members may be omitted.
- `implements` does not verify the constructor signature.

## Best practice
- Depend on interfaces in function signatures and implement them in concrete classes.
- Keep interfaces small so implementing classes stay focused.
