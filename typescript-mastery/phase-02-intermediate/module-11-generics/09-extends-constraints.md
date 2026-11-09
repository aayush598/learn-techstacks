# `extends` Constraints

> Phase 2 · Module 11 · Generics

**TL;DR** — An `extends` constraint requires a type argument to be assignable to a shape, enabling safe access to that shape's members.

## Syntax
```ts
function log<T extends { id: string }>(entity: T): void {
  console.log(entity.id);
}
```

## Examples
### Basic
```ts
function prop<T extends { name: string }>(value: T): string {
  return value.name;
}

prop({ name: "Ada", age: 36 }); // ✅

// ❌ Error: Property 'name' is missing in type '{ age: number; }'.
// prop({ age: 36 });
```

### Practical
```ts
abstract class Shape {
  abstract area(): number;
}

class Circle extends Shape {
  constructor(private readonly radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }
}

function totalArea<T extends Shape>(shapes: readonly T[]): number {
  return shapes.reduce((sum, shape) => sum + shape.area(), 0);
}

totalArea([new Circle(1), new Circle(2)]); // ✅
```

### Advanced / edge cases
```ts
// A constraint can reference an earlier parameter.
function merge<T extends object, U extends Partial<T>>(base: T, patch: U): T {
  return { ...base, ...patch };
}

const user = merge({ name: "Ada", age: 36 }, { age: 37 });
// { name: string; age: number }

// Union constraints accept a family of compatible types.
function format<T extends string | number>(value: T): string {
  return typeof value === "string" ? value.trim() : value.toFixed(2);
}

// ❌ Error: Type 'number' is not assignable to type 'string'.
// merge({ name: "Ada" }, { name: 1 });
```

## Key points
- `T extends Shape` means "every `T` is assignable to `Shape`".
- Class constraints are structural: any compatible shape passes.
- Constraints can reference other parameters (`U extends Partial<T>`).
- Unions and intersections are valid constraints.
- The inferred type stays concrete; the constraint only gates acceptance.

## Gotchas
- `extends` checks structure, not inheritance, even with classes.
- A too-narrow constraint rejects valid inputs.
- In conditional types, `extends` means assignability, not a runtime subclass check.

## Best practice
- Prefer small structural constraints over concrete classes.
- Name reusable constraints so signatures stay readable.
