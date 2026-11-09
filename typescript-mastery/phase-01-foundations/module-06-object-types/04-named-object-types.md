# Named Object Types

> Phase 1 · Module 06 · Object Types and Object Properties

**TL;DR** — Give an object shape a name with a `type` alias so it can be reused and referenced.

## Syntax
```ts
type Name = {
  key: string;
  other?: number;
};
```

## Examples
### Basic
```ts
type User = {
  id: string;
  name: string;
};

const user: User = { id: "u1", name: "Ada" };

console.log(user.name);
```

### Practical
```ts
type Point = { x: number; y: number };

function distance(a: Point, b: Point): number {
  return Math.hypot(a.x - b.x, a.y - b.y);
}

console.log(distance({ x: 0, y: 0 }, { x: 3, y: 4 }));
```

### Advanced / edge cases
```ts
type Tree = {
  value: number;
  children: Tree[];
};

const tree: Tree = {
  value: 1,
  children: [{ value: 2, children: [] }],
};

interface Named {
  name: string;
}

interface Named {
  id: string;
}

const named: Named = { name: "Ada", id: "u1" };

console.log(tree.value, named.id);
```

## Key points
- A `type` alias creates a reusable name for an object shape.
- The alias exists only at compile time and emits no JavaScript.
- Aliases can be recursive when the recursion passes through a property.
- `interface` is an alternative that supports declaration merging.
- Named types improve error messages and editor navigation.

## Gotchas
- `// ❌ Error:` a `type` alias cannot be reopened to add properties.
- `// ❌ Error:` merging interfaces with conflicting property types is rejected.
- A named type is structural: any compatible shape is accepted, not only values declared with that name.

## Best practice
- Use named object types for domain models, function contracts, and shared shapes.
- Prefer `type` for unions, intersections, and computed shapes; `interface` when you need merging or extension.
