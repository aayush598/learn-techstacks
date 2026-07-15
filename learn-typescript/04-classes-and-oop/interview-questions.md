# OOP Interview Questions — TypeScript

## Table of Contents

- [Class Basics](#class-basics)
- [Access Modifiers](#access-modifiers)
- [Getters and Setters](#getters-and-setters)
- [Static Members](#static-members)
- [Inheritance](#inheritance)
- [Abstract Classes](#abstract-classes)
- [Interfaces in OOP](#interfaces-in-oop)
- [Polymorphism](#polymorphism)
- [Composition Over Inheritance](#composition-over-inheritance)
- [Mixins](#mixins)

---

## Class Basics

### Q1: What is a class in TypeScript? How does it differ from a JavaScript class?

**Answer:** A class in TypeScript is a blueprint for creating objects that encapsulate data (properties) and behavior (methods). TypeScript adds type annotations, access modifiers (public/private/protected), abstract classes, generics, parameter properties, and static type checking on top of JavaScript's ES6 class syntax. At runtime, a TypeScript class compiles to a JavaScript class (or constructor function + prototype for older targets).

```typescript
class User {
  constructor(
    public readonly id: string,
    public name: string,
    private _email: string
  ) {}

  greet(): string {
    return `Hello, I'm ${this.name}`;
  }
}
```

Key TypeScript additions: type annotations, access modifiers, `readonly`, abstract classes, generics, parameter properties, `implements`/`extends` with type checking.

---

### Q2: What are parameter properties?

**Answer:** Parameter properties allow you to declare and initialize class properties directly in the constructor parameter list by prefixing with an access modifier (`public`, `private`, `protected`) or `readonly`. This eliminates boilerplate code.

```typescript
// With parameter properties
class User {
  constructor(
    public name: string,
    private age: number,
    readonly id: string
  ) {}
}

// Equivalent without parameter properties
class User {
  public name: string;
  private age: number;
  readonly id: string;

  constructor(name: string, age: number, id: string) {
    this.name = name;
    this.age = age;
    this.id = id;
  }
}
```

Parameter properties can use any combination: `public readonly`, `private readonly`, `protected readonly`, etc.

---

### Q3: What is the difference between `readonly` and `as const`?

**Answer:** `readonly` makes a class property不可 reassignable after initialization, but the type remains as declared (e.g., `string`). `as const` makes all properties readonly AND narrows types to literal types. `readonly` is used in class constructors; `as const` is a type assertion for objects and tuples.

```typescript
class Config {
  readonly host = "localhost"; // type: string, value: "localhost"
}

const CONST = {
  host: "localhost" // type: "localhost" (literal)
} as const;
```

---

### Q4: What happens if you don't initialize a class property in strict mode?

**Answer:** With `strictPropertyInitialization` enabled (part of `strict` mode), TypeScript emits an error if a non-optional class property is not definitely assigned in the constructor. Fixes: (1) initialize in constructor, (2) use property initializer, (3) use definite assignment assertion (`!`), or (4) make it optional (`?`).

```typescript
class Example {
  name!: string; // Definite assignment assertion — use cautiously
}
```

---

### Q5: What is a class expression? How does it differ from a class declaration?

**Answer:** A class expression assigns a class to a variable (`const MyClass = class {}`), while a declaration uses `class MyClass {}`. Named class expressions have the class name accessible only inside the class body. Class expressions are useful for creating anonymous classes and are the foundation for the mixin pattern.

```typescript
const Logger = class {
  log(msg: string) { console.log(msg); }
};

const factory = (prefix: string) => class {
  log(msg: string) { console.log(`[${prefix}] ${msg}`); }
};
```

---

### Q6: What is `typeof ClassName` used for?

**Answer:** `typeof ClassName` gives the type of the constructor/static side of the class. It's useful in factory functions and when you need to reference the class itself as a type (not an instance).

```typescript
class Dog {
  name: string;
  constructor(name: string) { this.name = name; }
}

type DogConstructor = typeof Dog;

function create(Ctor: DogConstructor, name: string): Dog {
  return new Ctor(name);
}
```

---

## Access Modifiers

### Q7: What is the difference between `public`, `private`, and `protected`?

**Answer:**
- **`public`** (default): Accessible everywhere — inside the class, outside, and in subclasses.
- **`private`**: Accessible only within the defining class.
- **`protected`**: Accessible within the defining class and its subclasses.

```typescript
class Example {
  public a = 1;    // everywhere
  private b = 2;   // only in Example
  protected c = 3; // Example + subclasses
}
```

---

### Q8: Are TypeScript access modifiers enforced at runtime?

**Answer:** No. TypeScript's `public`, `private`, and `protected` are compile-time only. At runtime, all properties are accessible. You can bypass them with `as any`:

```typescript
class Secret {
  private value = 42;
}
const s = new Secret();
console.log((s as any).value); // 42 — runtime access
```

For true runtime privacy, use ECMAScript's `#` private fields.

---

### Q9: What is the difference between `private` and `#` (ECMAScript private fields)?

**Answer:** TypeScript's `private` is compile-time only — bypassable with `as any`. ECMAScript's `#` creates truly private fields inaccessible even at runtime. However, `#` fields can't be used in parameter properties or declaration merging, and they have different syntax.

```typescript
class TS {
  private x = 1; // compile-time only
}

class ES {
  #y = 2; // runtime private
}

const ts = new TS();
console.log((ts as any).x); // 1

const es = new ES();
console.log((es as any).y); // undefined
```

---

### Q10: Can accessors have different visibility?

**Answer:** Yes. A getter and setter for the same property can have different modifiers. A common pattern is a public getter with a private setter:

```typescript
class Temperature {
  private _celsius = 0;

  get celsius(): number { return this._celsius; }
  private set celsius(v: number) { this._celsius = v; }
}
```

---

### Q11: When should you use `protected` instead of `private`?

**Answer:** Use `protected` when subclasses genuinely need access to a member. If a member is only used within the defining class, keep it `private`. Overusing `protected` weakens encapsulation and makes refactoring harder.

---

## Getters and Setters

### Q12: What is the difference between a getter and a method?

**Answer:** A getter uses the `get` keyword and is accessed like a property (`obj.prop`) without parentheses, takes no parameters. A method is called with parentheses (`obj.method()`) and can take parameters. Use getters for computed properties that feel like attributes; use methods for actions with parameters or significant side effects.

---

### Q13: Can a setter have a different type than its getter?

**Answer:** Yes. A setter can accept a broader type and convert it:

```typescript
class FormattedDate {
  private _date = new Date();

  get date(): Date { return new Date(this._date); }
  set date(value: Date | string | number) { this._date = new Date(value); }
}
```

---

### Q14: How do you implement a cached getter?

**Answer:** Use a private backing field initialized to `null`. On first access, compute and store the value. On subsequent accesses, return the cached value. Invalidate when underlying data changes:

```typescript
class Expensive {
  private _cache: number | null = null;

  get value(): number {
    if (this._cache === null) {
      this._cache = this.computeExpensiveValue();
    }
    return this._cache;
  }

  invalidate(): void { this._cache = null; }

  private computeExpensiveValue(): number {
    return 42; // expensive computation
  }
}
```

---

### Q15: When should you use a setter vs a method for validation?

**Answer:** Use a setter when the operation is conceptually a property assignment and validation is quick. Use a method when the operation is complex, might throw, or should be called explicitly (e.g., `changePassword()` vs `set password()`).

---

## Static Members

### Q16: What is the difference between static and instance members?

**Answer:** Static members belong to the class itself, shared across all instances. Instance members belong to individual objects. Static members are accessed via `ClassName.member`, instance members via `instance.member`. Static methods don't participate in runtime polymorphism.

```typescript
class Example {
  static count = 0;   // shared
  value = 0;          // per-instance

  constructor() { Example.count++; }
}
```

---

### Q17: Can static methods be overridden?

**Answer:** In TypeScript/JavaScript, static methods are not polymorphically overridden. If a subclass defines a static method with the same name, it shadows the parent's method. Calling via the parent class name always calls the parent's version.

```typescript
class Base {
  static create() { return "Base"; }
}
class Child extends Base {
  static create() { return "Child"; }
}

Base.create();   // "Base"
Child.create();  // "Child"
```

---

### Q18: What are static blocks?

**Answer:** Static blocks (TypeScript 4.4+) execute once when the class is first loaded. They perform complex initialization for static properties, supporting try/catch, loops, and conditional logic. Multiple static blocks execute top-to-bottom.

```typescript
class Config {
  static dbHost: string;
  static {
    Config.dbHost = process.env.DB_HOST ?? "localhost";
  }
}
```

---

### Q19: When should you use a static factory method instead of a constructor?

**Answer:** Use static factory methods when: (1) descriptive names needed (`Color.fromHex()`), (2) returning cached instances, (3) returning subtypes, (4) validation before construction, (5) controlling new vs existing instance creation.

---

### Q20: Why would you make a constructor private?

**Answer:** A private constructor prevents external instantiation, useful for: (1) singleton pattern, (2) factory methods that control creation, (3) preventing instantiation of abstract or utility classes.

---

## Inheritance

### Q21: What is inheritance in TypeScript?

**Answer:** Inheritance is a mechanism where a child class extends a parent class, inheriting its properties and methods. TypeScript supports single inheritance using `extends`. The child can override parent methods and add new members.

```typescript
class Animal {
  name: string;
  constructor(name: string) { this.name = name; }
}

class Dog extends Animal {
  bark() { return `${this.name} says Woof!`; }
}
```

---

### Q22: What is the `super` keyword used for?

**Answer:** `super` is used to: (1) call the parent class constructor (`super()`), required before accessing `this` in the child constructor, and (2) call parent class methods (`super.method()`) when overriding to extend behavior.

---

### Q23: Why doesn't TypeScript support multiple inheritance?

**Answer:** TypeScript (JavaScript) avoids multiple inheritance to prevent the "diamond problem" — where a class inherits from two classes with conflicting implementations of the same method. Instead, TypeScript uses interfaces, mixins, and composition to achieve similar functionality.

---

### Q24: What is the Liskov Substitution Principle?

**Answer:** LSP states that objects of a subclass should be substitutable for objects of the superclass without breaking the program. If `S` is a subtype of `T`, then objects of type `T` may be replaced with objects of type `S` without altering correctness.

Classic violation: Square inheriting from Rectangle. If you set width on a "rectangle" that's actually a square, the height also changes, breaking client expectations.

---

## Abstract Classes

### Q25: What is an abstract class?

**Answer:** An abstract class cannot be instantiated directly. It contains abstract members (methods/properties without implementation that subclasses must implement) and concrete members (shared implementation). It serves as a blueprint for related classes.

```typescript
abstract class Shape {
  abstract area(): number;      // must implement
  describe() { return `Area: ${this.area()}`; } // shared
}
```

---

### Q26: What is the difference between an abstract class and an interface?

**Answer:** Abstract classes can have implementations, constructors, state, and access modifiers. Interfaces define only contracts. Abstract classes use `extends`, interfaces use `implements`. A class can extend one abstract class but implement multiple interfaces. Interfaces are erased at runtime; abstract classes exist as functions.

| Feature | Abstract Class | Interface |
|---|---|---|
| Implementations | Yes | No |
| Constructors | Yes | No |
| Multiple inheritance | No | Yes |
| Runtime existence | Yes | No |

---

### Q27: What is the Template Method pattern?

**Answer:** The Template Method pattern defines the skeleton of an algorithm in an abstract base class method, deferring specific steps to subclasses. The template method calls abstract methods that subclasses must implement and optional hook methods they can override.

```typescript
abstract class DataExporter {
  export(data: any[]): string {
    const validated = this.validate(data);
    const formatted = this.format(validated);
    return formatted;
  }

  abstract validate(data: any[]): any[];
  abstract format(data: any[]): string;
}
```

---

### Q28: Can abstract classes have no abstract members?

**Answer:** Yes. An abstract class with zero abstract members prevents instantiation while providing shared implementation. This is useful for base classes that should never be instantiated directly.

---

## Interfaces in OOP

### Q29: What is the `implements` keyword?

**Answer:** The `implements` keyword ensures a class satisfies an interface's contract. If the class doesn't implement all required members, TypeScript raises a compile error.

```typescript
interface Printable {
  print(): string;
}

class Document implements Printable {
  print(): string { return "Document content"; }
}
```

---

### Q30: What is the Interface Segregation Principle?

**Answer:** ISP states that no client should be forced to depend on methods it does not use. Instead of one large interface, create multiple small, focused interfaces. Classes implement only the interfaces relevant to them.

```typescript
// Bad: one fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

// Good: segregated interfaces
interface Workable { work(): void; }
interface Eatable { eat(): void; }
interface Sleepable { sleep(): void; }
```

---

### Q31: How do interfaces support Dependency Inversion?

**Answer:** High-level modules depend on interface abstractions rather than concrete implementations. This allows swapping implementations without changing high-level code:

```typescript
interface Database {
  query<T>(sql: string): Promise<T[]>;
}

class UserService {
  constructor(private db: Database) {} // depends on abstraction
}
```

---

### Q32: What is "coding to interfaces"?

**Answer:** Designing code to depend on interface types rather than concrete classes. Function parameters, return types, and class dependencies use interface types, enabling loose coupling and easy testing through mocks.

---

## Polymorphism

### Q33: What is polymorphism in TypeScript?

**Answer:** Polymorphism is the ability of objects of different types to be treated through a uniform interface. TypeScript supports: (1) runtime polymorphism via method overriding, (2) compile-time polymorphism via generics and overloading, (3) structural polymorphism via duck typing.

---

### Q34: What is duck typing?

**Answer:** Duck typing is TypeScript's structural typing: objects are compatible based on their shape, not explicit type declarations. If an object has the required properties and methods, it satisfies the type.

```typescript
interface HasName { name: string; }

function greet(entity: HasName) { console.log(entity.name); }
greet({ name: "Alice" });        // OK
greet(new User("1", "Alice"));   // OK — structurally compatible
```

---

### Q35: What are covariant and contravariant types?

**Answer:** Covariance preserves subtyping direction (SubType → SuperType). Contravariance reverses it. In TypeScript with `strictFunctionTypes`, function parameters are contravariant and return types are covariant.

```typescript
class Animal { name = ""; }
class Dog extends Animal { breed = ""; }

// Function parameters are contravariant
type Fn<A, B> = (a: A) => B;
let f1: Fn<Animal, Dog> = (a) => new Dog(); // OK
let f2: Fn<Dog, Dog> = f1; // OK: AnimalToDog assignable to DogToDog
```

---

### Q36: How do the SOLID principles apply to TypeScript?

**Answer:**
- **S**RP: Each class has one responsibility.
- **O**CP: Extend behavior via interfaces/abstract classes without modifying existing code.
- **L**SP: Subtypes must be substitutable for their base types.
- **I**SP: Use small, focused interfaces.
- **D**IP: Depend on abstractions, not concrete implementations.

---

## Composition Over Inheritance

### Q37: What is composition over inheritance?

**Answer:** Composition is a design principle where complex objects are built by combining simpler, reusable objects rather than through class inheritance. It promotes loose coupling, flexibility, runtime behavior swapping, and easier testing.

```typescript
// Composition: behaviors as components
class Duck {
  private flyBehavior = new WingsFly();
  private quackBehavior = new LoudQuack();

  fly() { return this.flyBehavior.fly(); }
  quack() { return this.quackBehavior.quack(); }
}
```

---

### Q38: What is the Strategy Pattern?

**Answer:** The Strategy Pattern defines a family of algorithms, encapsulates each one, and makes them interchangeable. A context class uses a strategy object to perform an operation, and the strategy can be changed at runtime.

```typescript
interface SortStrategy<T> {
  sort(data: T[]): T[];
}

class QuickSort<T> implements SortStrategy<T> {
  sort(data: T[]): T[] { /* ... */ }
}

class Sorter<T> {
  constructor(private strategy: SortStrategy<T>) {}
  setStrategy(s: SortStrategy<T>) { this.strategy = s; }
  sort(data: T[]) { return this.strategy.sort(data); }
}
```

---

### Q39: What is the difference between pipe and compose?

**Answer:** Both are function composition. Pipe applies functions left-to-right: `pipe(data, fn1, fn2)`. Compose applies functions right-to-left: `compose(fn2, fn1)(data)`. Pipe reads naturally for sequential transformations.

---

### Q40: What is Dependency Injection?

**Answer:** DI is a form of composition where objects receive their dependencies from outside rather than creating them internally. Common forms: constructor injection, property injection, and method injection. DI promotes testability and loose coupling.

```typescript
class UserService {
  constructor(
    private db: Database,    // injected
    private logger: Logger    // injected
  ) {}
}
```

---

## Mixins

### Q41: What are mixins in TypeScript?

**Answer:** Mixins are a design pattern that allows composing behaviors from multiple sources into a single class. They are functions that take a base class and return an extended class with additional functionality, providing multiple-inheritance-like behavior in TypeScript.

```typescript
type Constructor<T = object> = new (...args: any[]) => T;

function Timestamped<TBase extends Constructor>(Base: TBase) {
  return class extends Base {
    createdAt = new Date();
  };
}

const TimestampedEntity = Timestamped(BaseEntity);
```

---

### Q42: Why doesn't TypeScript support multiple inheritance?

**Answer:** To avoid the diamond problem — where a class inherits from two classes with conflicting implementations of the same method. Mixins provide a controlled alternative with a linear prototype chain and explicit composition order.

---

### Q43: What is the order of mixin application?

**Answer:** Mixins are applied from the innermost to the outermost: `A(B(C(Base)))` means C extends Base first, then B extends that result, then A. The order determines the prototype chain and method resolution.

---

### Q44: What are alternatives to mixins?

**Answer:** Alternatives include: (1) composition (HAS-A), (2) utility functions, (3) higher-order functions, (4) decorators (experimental), (5) `Object.assign`. Each has trade-offs in type safety, readability, and flexibility.

---

### Q45: Can mixins have private members?

**Answer:** Yes. Mixins can use TypeScript's `private` keyword for compile-time privacy and ECMAScript `#` for runtime privacy. Both work within the mixin class expression.

---

## Bonus: Mixed Topics

### Q46: Design a simple ORM repository pattern using OOP principles.

**Answer:**

```typescript
interface Entity {
  id: string;
}

interface Repository<T extends Entity> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<void>;
  delete(id: string): Promise<boolean>;
}

abstract class BaseRepository<T extends Entity> implements Repository<T> {
  protected items: Map<string, T> = new Map();

  async findById(id: string): Promise<T | null> {
    return this.items.get(id) ?? null;
  }

  async findAll(): Promise<T[]> {
    return Array.from(this.items.values());
  }

  async save(entity: T): Promise<void> {
    this.items.set(entity.id, entity);
  }

  async delete(id: string): Promise<boolean> {
    return this.items.delete(id);
  }
}

interface User extends Entity {
  name: string;
  email: string;
}

class UserRepository extends BaseRepository<User> {
  async findByEmail(email: string): Promise<User | null> {
    for (const user of this.items.values()) {
      if (user.email === email) return user;
    }
    return null;
  }
}
```

---

### Q47: What is the difference between `extends` and `implements`?

**Answer:** `extends` creates class inheritance — the child inherits implementation from the parent. `implements` ensures a class satisfies an interface's contract — the class must provide all implementations, and no code is inherited.

```typescript
class Base {
  greet() { return "Hello"; }
}

// extends: inherits greet()
class Child extends Base {}

// implements: must implement greet() yourself
interface Greeter {
  greet(): string;
}

class Custom implements Greeter {
  greet() { return "Hi there"; }
}
```

---

### Q48: Explain the SOLID principles with TypeScript examples.

**Answer:**

**S — Single Responsibility:**
```typescript
class UserValidator { validate(user: User): boolean { return true; } }
class UserRepository { save(user: User): void {} }
class EmailService { send(to: string, msg: string): void {} }
```

**O — Open/Closed:**
```typescript
interface Discount { apply(price: number): number; }
class NoDiscount implements Discount { apply(p: number) { return p; } }
class TenPercentDiscount implements Discount { apply(p: number) { return p * 0.9; } }
// Adding new discounts doesn't modify existing code
```

**L — Liskov Substitution:**
```typescript
interface Shape { area(): number; }
class Circle implements Shape { area() { return Math.PI * 5 ** 2; } }
class Rectangle implements Shape { area() { return 4 * 6; } }
// Both substitutable wherever Shape is expected
```

**I — Interface Segregation:**
```typescript
interface Readable<T> { read(): Promise<T>; }
interface Writable<T> { write(data: T): Promise<void>; }
// Instead of one CRUD interface, split into focused ones
```

**D — Dependency Inversion:**
```typescript
interface Database { query<T>(sql: string): Promise<T[]>; }
class UserService {
  constructor(private db: Database) {} // Depends on abstraction
}
```

---

### Q49: When would you use an abstract class vs an interface?

**Answer:** Use an **abstract class** when: you need shared implementation, constructors, access modifiers, or a class hierarchy. Use an **interface** when: defining pure contracts, need multiple type inheritance, no shared code, or maximum flexibility for testing/mocking. In practice, prefer interfaces when possible and use abstract classes when you need code sharing.

---

### Q50: Design a type-safe event emitter using OOP principles.

**Answer:**

```typescript
type EventMap = Record<string, any>;

class TypedEventEmitter<TEvents extends EventMap> {
  private listeners = new Map<string, Set<Function>>();

  on<K extends keyof TEvents>(
    event: K,
    handler: (payload: TEvents[K]) => void
  ): () => void {
    if (!this.listeners.has(event as string)) {
      this.listeners.set(event as string, new Set());
    }
    this.listeners.get(event as string)!.add(handler);

    return () => {
      this.listeners.get(event as string)?.delete(handler);
    };
  }

  emit<K extends keyof TEvents>(event: K, payload: TEvents[K]): void {
    this.listeners.get(event as string)?.forEach(handler => {
      (handler as (payload: TEvents[K]) => void)(payload);
    });
  }

  once<K extends keyof TEvents>(
    event: K,
    handler: (payload: TEvents[K]) => void
  ): () => void {
    const unsubscribe = this.on(event, (payload) => {
      handler(payload);
      unsubscribe();
    });
    return unsubscribe;
  }
}

// Usage
interface AppEvents {
  login: { userId: string; timestamp: Date };
  logout: { userId: string };
  error: { code: number; message: string };
}

const emitter = new TypedEventEmitter<AppEvents>();

const unsub = emitter.on("login", ({ userId, timestamp }) => {
  console.log(`${userId} logged in at ${timestamp}`);
});

emitter.emit("login", { userId: "123", timestamp: new Date() });
unsub(); // unsubscribe
```

---

**End of Interview Questions**

All topics covered: Class Basics, Access Modifiers, Getters/Setters, Static Members, Inheritance, Abstract Classes, Interfaces, Polymorphism, Composition, Mixins, and SOLID principles.
