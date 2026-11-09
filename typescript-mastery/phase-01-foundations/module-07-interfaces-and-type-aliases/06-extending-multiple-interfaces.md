# Extending Multiple Interfaces

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An interface can extend several interfaces at once, combining all their members into one contract.

## Syntax
```ts
interface Readable {
  read(): string;
}

interface Writable {
  write(data: string): void;
}

interface Stream extends Readable, Writable {
  close(): void;
}
```

## Examples
### Basic
```ts
interface Named {
  name: string;
}

interface Aged {
  age: number;
}

interface Person extends Named, Aged {
  email: string;
}

const person: Person = { name: "Ada", age: 36, email: "ada@example.com" };
```

### Practical
```ts
interface Readable {
  read(): string;
}

interface Writable {
  write(data: string): void;
}

interface Stream extends Readable, Writable {
  close(): void;
}

const stream: Stream = {
  read: () => "data",
  write: (data) => console.log(data),
  close: () => console.log("closed"),
};
```

### Advanced / edge cases
```ts
interface Timestamped {
  createdAt: Date;
  updatedAt: Date;
}

interface Identified {
  id: string;
}

interface SoftDeletable {
  deletedAt?: Date;
}

interface AuditEntry extends Identified, Timestamped, SoftDeletable {
  payload: unknown;
}

// Identical members from multiple bases collapse into one.
interface Left {
  shared: string;
}
interface Right {
  shared: string;
}
interface Both extends Left, Right {} // ✅ shared: string

// ❌ Error: Interface 'Conflict' cannot simultaneously extend types
// interface First { value: string }
// interface Second { value: number }
// interface Conflict extends First, Second {}
```

## Key points
- All listed bases contribute their members.
- Duplicate members with identical types are allowed.
- Conflicting member types are a compile error.
- Same-named methods from multiple bases become overloads.
- The result is assignable to every base interface.

## Gotchas
- `// ❌ Error:` extending two interfaces that declare the same property with different types.
- Member order across bases does not resolve conflicts.
- Multiple inheritance here is type-only; no runtime behavior is inherited.

## Best practice
- Compose small capability interfaces (`Readable`, `Writable`) and combine them.
- Prefer many narrow bases over one wide base with optional members.
