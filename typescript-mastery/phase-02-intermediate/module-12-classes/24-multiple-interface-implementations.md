# Multiple interface implementations

> Phase 2 · Module 12 · Classes

**TL;DR** — A class can implement several interfaces at once, composing capabilities without multiple inheritance.

## Syntax
```ts
class C implements A, B, C2 {
  // satisfy all three interfaces
}
```

## Examples
### Basic
```ts
interface Readable {
  read(): string;
}

interface Writable {
  write(data: string): void;
}

class Buffer implements Readable, Writable {
  private data = "";

  read(): string {
    return this.data;
  }

  write(data: string): void {
    this.data += data;
  }
}

const buffer = new Buffer();
buffer.write("hello");
console.log(buffer.read()); // hello
```

### Practical
```ts
interface Entity {
  readonly id: string;
}

interface Timestamped {
  readonly createdAt: Date;
  updatedAt: Date;
}

interface SoftDeletable {
  deletedAt: Date | null;
}

class Document implements Entity, Timestamped, SoftDeletable {
  readonly createdAt = new Date();
  updatedAt = new Date();
  deletedAt: Date | null = null;

  constructor(readonly id: string) {}

  softDelete(): void {
    this.deletedAt = new Date();
  }
}

const doc = new Document("d1");
doc.softDelete();
console.log(doc.deletedAt instanceof Date); // true
```

### Advanced / edge cases
```ts
interface Named {
  name: string;
}

interface Aged {
  age: number;
}

class Person implements Named, Aged {
  constructor(
    public name: string,
    public age: number,
  ) {}
}

const person: Named & Aged = new Person("Ada", 36);
console.log(person.name, person.age);

interface HasString {
  value: string;
}

interface HasNumber {
  value: number;
}

// ❌ Error: Class 'Conflict' incorrectly implements interface 'HasNumber'.
// class Conflict implements HasString, HasNumber {
//   value = "text";
// }
```

## Key points
- List interfaces after `implements`, separated by commas.
- The class instance type must satisfy every interface simultaneously.
- Conflicting member types across interfaces make implementation impossible.
- Interface inheritance can reduce duplication before implementing.
- Multiple interfaces compose behavior without a class hierarchy.

## Gotchas
- Two interfaces requiring the same property with incompatible types cannot be combined in one class.
- Overlapping method signatures must remain compatible.
- `implements` provides no runtime metadata about the interfaces.

## Best practice
- Compose small, orthogonal interfaces rather than one large interface.
- Use `interface X extends A, B` to name common combinations reused across classes.
