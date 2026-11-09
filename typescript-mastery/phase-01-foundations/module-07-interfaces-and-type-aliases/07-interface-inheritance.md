# Interface Inheritance

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Interface inheritance builds a chain of increasingly specific contracts, where each derived type is usable anywhere its ancestor is expected.

## Syntax
```ts
interface Animal {
  name: string;
}

interface Mammal extends Animal {
  warmBlooded: boolean;
}

interface Dog extends Mammal {
  breed: string;
}
```

## Examples
### Basic
```ts
interface Animal {
  name: string;
}

interface Mammal extends Animal {
  warmBlooded: true;
}

interface Dog extends Mammal {
  breed: string;
}

const dog: Dog = { name: "Rex", warmBlooded: true, breed: "Husky" };
const animal: Animal = dog; // ✅ Dog is assignable to Animal
```

### Practical
```ts
interface Node {
  id: string;
}

interface DocumentNode extends Node {
  title: string;
}

interface PageNode extends DocumentNode {
  slug: string;
  published: boolean;
}

function render(node: DocumentNode): string {
  return node.title;
}

const page: PageNode = {
  id: "p1",
  title: "Home",
  slug: "home",
  published: true,
};

console.log(render(page)); // "Home"
```

### Advanced / edge cases
```ts
interface EventBase {
  type: string;
  timestamp: number;
}

interface UserEvent extends EventBase {
  userId: string;
}

interface LoginEvent extends UserEvent {
  type: "login";
  method: "password" | "oauth";
}

// Derived types can be discriminated by narrowing a base member.
function describe(event: EventBase): string {
  return `${event.type} at ${event.timestamp}`;
}

const login: LoginEvent = {
  type: "login",
  timestamp: Date.now(),
  userId: "u1",
  method: "oauth",
};

console.log(describe(login)); // "login at ..."
```

## Key points
- Inheritance creates an `is-a` relationship in the type system.
- A derived interface has every member of every ancestor.
- Values of a derived type are assignable to ancestor types.
- Overriding is allowed only when the new type is compatible.
- Deep chains increase coupling; keep them shallow.

## Gotchas
- `// ❌ Error:` assigning a base value to a derived type: `const dog: Dog = animal;` — missing derived members.
- Overriding a property with an incompatible type breaks the chain.
- Structural typing means unrelated types with the same shape are also assignable.

## Best practice
- Model true specialization with inheritance; model shared data with composition.
- Limit chains to two or three levels before refactoring.
