# Class declarations

> Phase 2 · Module 12 · Classes

**TL;DR** — A class declaration defines a named blueprint whose properties and methods are used to create instances with `new`.

## Syntax
```ts
class Name {
  field: Type = value;

  constructor(args) {
    // initialization
  }

  method(): ReturnType {
    // behavior
  }
}
```

## Examples
### Basic
```ts
class Point {
  x = 0;
  y = 0;
}

const origin = new Point();
console.log(origin.x, origin.y); // 0 0
```

### Practical
```ts
class User {
  name: string;
  email: string;

  constructor(name: string, email: string) {
    this.name = name;
    this.email = email;
  }

  greet(): string {
    return `Hello, ${this.name}`;
  }
}

const user = new User("Ada", "ada@example.com");
console.log(user.greet()); // Hello, Ada
```

### Advanced / edge cases
```ts
class Box {
  constructor(public value: number) {}
}

const box = new Box(1);
const Ctor = Box; // ✅ a class is also a value (its constructor)
console.log(typeof Ctor); // "function"

// ❌ Error: Block-scoped variable 'Service' used before its declaration.
// new Service();

class Service {
  run(): void {}
}

const instance = new Service(); // ✅ after declaration
console.log(instance instanceof Service); // true
```

## Key points
- A class declaration creates both a type (the instance shape) and a value (the constructor).
- Class declarations are block-scoped and not hoisted for runtime use like function declarations.
- Instances are created with `new`; calling without `new` is an error.
- Members can include fields, constructors, methods, accessors, and static members.
- TypeScript adds type checking on top of the ECMAScript class semantics.

## Gotchas
- Using a class before its declaration in the same scope fails at runtime even though types are known.
- `typeof SomeClass` is `"function"`; classes are not a distinct runtime primitive.
- A class declaration cannot be re-declared or merged the way an interface can.

## Best practice
- Keep one primary class per module and name it after the domain concept.
- Declare the class before code that instantiates it to avoid temporal dead zone issues.
