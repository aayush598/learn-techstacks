# Extending Interfaces

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — An interface can `extends` another interface to inherit its members and add or narrow its own.

## Syntax
```ts
interface Entity {
  id: string;
}

interface User extends Entity {
  name: string;
}
```

## Examples
### Basic
```ts
interface Entity {
  id: string;
  createdAt: Date;
}

interface User extends Entity {
  name: string;
  email: string;
}

const user: User = {
  id: "u1",
  createdAt: new Date(),
  name: "Ada",
  email: "ada@example.com",
};
```

### Practical
```ts
interface Shape {
  kind: string;
  area(): number;
}

interface Circle extends Shape {
  kind: "circle";
  radius: number;
}

const circle: Circle = {
  kind: "circle",
  radius: 2,
  area() {
    return Math.PI * this.radius ** 2;
  },
};
```

### Advanced / edge cases
```ts
interface User {
  id: string;
  name: string;
}

interface Repository<T extends { id: string }> {
  find(id: string): T | undefined;
}

interface UserRepository extends Repository<User> {
  findByEmail(email: string): User | undefined;
}

// A derived member may narrow a base member to a compatible subtype.
interface Base {
  status: string;
}

interface Ready extends Base {
  status: "ready"; // ✅ narrower literal is assignable to string
}

// ❌ Error: Interface 'Broken' incorrectly extends interface 'Base'
// interface Broken extends Base {
//   status: number;
// }
```

## Key points
- `extends` copies the base members into the derived type.
- Derived members can add new properties and methods.
- Derived members can narrow a base member to a subtype.
- The derived type is assignable to the base type.
- Generic bases can be extended with concrete type arguments.

## Gotchas
- Widening a base member is an error: `// ❌ Error:` `interface B extends Base { status: number }`.
- Optional base members stay optional unless redeclared.
- Extending does not create runtime inheritance; there is no base object.

## Best practice
- Extend when the child genuinely is a specialization of the parent.
- Keep base interfaces small so derived types stay focused.
