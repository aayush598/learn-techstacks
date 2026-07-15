# Type Compatibility in TypeScript

Type compatibility determines whether one type can be assigned to another. TypeScript uses a **structural type system** — types are compatible if they have the same structure, regardless of their names. Understanding compatibility rules is essential for writing correct TypeScript code.

---

## Table of Contents

1. [Structural Typing](#structural-typing)
2. [Subtype Compatibility](#subtype-compatibility)
3. [Assignability Rules](#assignability-rules)
4. [any Compatibility](#any-compatibility)
5. [unknown Compatibility](#unknown-compatibility)
6. [never Compatibility](#never-compatibility)
7. [Enum Compatibility](#enum-compatibility)
8. [Class Compatibility](#class-compatibility)
9. [Function Parameter Bivariance](#function-parameter-bivariance)
10. [Strict Function Types Flag](#strict-function-types-flag)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## Structural Typing

TypeScript uses structural typing — if two types have the same shape (same properties with compatible types), they are compatible.

```typescript
interface Point {
  x: number;
  y: number;
}

interface Coordinate {
  x: number;
  y: number;
}

const point: Point = { x: 1, y: 2 };
const coord: Coordinate = point; // OK — same structure!
```

### Extra properties are allowed

```typescript
interface Point {
  x: number;
  y: number;
}

const myPoint = { x: 1, y: 2, z: 3 };
const p: Point = myPoint; // OK — extra property z is allowed

// But not when using object literal directly (excess property check)
// const p: Point = { x: 1, y: 2, z: 3 }; // Error — excess property z
```

### Property compatibility

```typescript
interface Animal {
  name: string;
}

interface Dog {
  name: string;
  breed: string;
}

function processAnimal(animal: Animal) {
  console.log(animal.name);
}

const dog: Dog = { name: "Rex", breed: "Labrador" };
processAnimal(dog); // OK — Dog has all properties of Animal
```

---

## Subtype Compatibility

A type is a subtype if it has all the properties of the supertype (and possibly more).

```typescript
interface Base {
  a: string;
}

interface Extended extends Base {
  b: number;
  c: boolean;
}

function processBase(obj: Base) {
  console.log(obj.a);
}

const extended: Extended = { a: "hello", b: 42, c: true };
processBase(extended); // OK — Extended is a subtype of Base
```

### Property type compatibility

```typescript
interface Container {
  value: string;
}

interface NumberContainer {
  value: number;
}

function process(container: Container) {
  console.log(container.value.toUpperCase());
}

const numContainer: NumberContainer = { value: 42 };
// process(numContainer); // Error — number is not assignable to string
```

### Covariance in arrays

```typescript
interface Animal {
  name: string;
}

interface Dog extends Animal {
  breed: string;
}

const dogs: Dog[] = [{ name: "Rex", breed: "Labrador" }];
const animals: Animal[] = dogs; // OK — Dog[] is subtype of Animal[]
```

---

## Assignability Rules

### Basic assignability

```typescript
// Number types
let x: number = 42;       // OK
let y: number = Infinity; // OK
let z: number = NaN;      // OK

// String types
let s: string = "hello";  // OK
let t: string = "";       // OK

// Boolean types
let b: boolean = true;    // OK
let c: boolean = false;   // OK
```

### Union assignability

```typescript
function process(value: string | number) {
  // ...
}

process("hello"); // OK
process(42);      // OK
// process(true); // Error — boolean not in union
```

### Literal assignability

```typescript
type Direction = "north" | "south" | "east" | "west";

let d: Direction = "north"; // OK
// let d: Direction = "up"; // Error — "up" not in union

// But widening works:
let s = "north";  // type is string (widened)
let dir: Direction = s; // Error — string is not assignable to Direction
```

---

## any Compatibility

`any` is compatible with everything — both assignable to and from any type.

```typescript
let anything: any = 42;
let str: string = anything;   // OK — any is assignable to string
let num: number = anything;   // OK
let bool: boolean = anything; // OK

function process(value: any) {
  // Can use value as anything
  console.log(value.toUpperCase());
  console.log(value.nonExistentMethod());
}

const obj: { name: string } = { name: "Alice" };
const a: any = obj; // OK — anything is assignable to any
```

### any disables type checking

```typescript
let x: any = "hello";
x = 42;       // OK
x = true;     // OK
x = { a: 1 }; // OK

// No compile errors with any
x.foo.bar.baz; // OK at compile time, runtime error!
```

---

## unknown Compatibility

`unknown` is the type-safe counterpart to `any`. It's assignable from everything but assignable to nothing (except `unknown` and `any`).

```typescript
let value: unknown = 42;
let num: number = value;   // Error — unknown not assignable to number
let str: string = value;   // Error — unknown not assignable to string

// But anything is assignable to unknown:
let x: unknown = 42;       // OK
let y: unknown = "hello";  // OK
let z: unknown = true;     // OK
```

### Narrowing unknown

```typescript
function process(value: unknown) {
  if (typeof value === "string") {
    console.log(value.toUpperCase()); // OK — narrowed to string
  }
}
```

### unknown vs any

```typescript
// any — no type checking
function unsafe(value: any) {
  value.foo.bar.baz; // No compile error
}

// unknown — forces type checking
function safe(value: unknown) {
  // value.foo.bar.baz; // Error
  if (typeof value === "object" && value !== null && "foo" in value) {
    const v = value as { foo: { bar: { baz: string } } };
    console.log(v.foo.bar.baz); // OK after narrowing
  }
}
```

---

## never Compatibility

`never` is the bottom type — it's assignable to everything, but nothing is assignable to it (except `never` itself).

```typescript
function throwError(): never {
  throw new Error("oops");
}

let x: string = throwError();   // OK — never assignable to string
let y: number = throwError();   // OK — never assignable to number
let z: unknown = throwError();  // OK

// But nothing is assignable to never:
let n: never;
// let a: never = 42;           // Error
// let b: never = "hello";      // Error
// let c: never = throwError(); // Error — throwError returns never, not a value
```

### never in unions

```typescript
type A = string | never; // string
type B = number | never; // number
type C = never | never;  // never
```

### never in intersections

```typescript
type A = string & never; // never
type B = number & never; // never
```

---

## Enum Compatibility

Enums in TypeScript have specific compatibility rules.

### Numeric enums

```typescript
enum Direction {
  Up,
  Down,
  Left,
  Right,
}

let d: Direction = Direction.Up; // OK
let n: number = Direction.Up;    // OK — numeric enum is assignable to number
let d2: Direction = 0;          // OK — number is assignable to numeric enum

// But numeric enum values are not assignable to other numeric enums
enum Color {
  Red,
  Green,
  Blue,
}

let c: Color = Direction.Up; // Error — Direction not assignable to Color
```

### String enums

```typescript
enum Direction {
  Up = "UP",
  Down = "DOWN",
  Left = "LEFT",
  Right = "RIGHT",
}

let d: Direction = Direction.Up; // OK
let s: string = Direction.Up;   // OK — string enum is assignable to string
// let d2: Direction = "UP";    // Error — string literal not assignable to enum
```

### Const enums

```typescript
const enum Direction {
  Up = "UP",
  Down = "DOWN",
}

let d: Direction = Direction.Up; // OK — but Direction is inlined at compile time
// The enum doesn't exist at runtime
```

---

## Class Compatibility

Classes are compatible based on their structure, not their names.

```typescript
class Animal {
  name: string = "";
  sound: string = "";
}

class Dog {
  name: string = "";
  sound: string = "";
  breed: string = "";
}

const animal: Animal = new Dog(); // OK — Dog has all properties of Animal
```

### Private members break compatibility

```typescript
class Animal {
  private id: string = "";
  name: string = "";
}

class Dog {
  private id: string = "";
  name: string = "";
  breed: string = "";
}

const animal: Animal = new Dog(); // Error — private member 'id' is incompatible
```

### Static members

```typescript
class Animal {
  static create(): Animal {
    return new Animal();
  }
  name: string = "";
}

class Dog extends Animal {
  static create(): Dog {
    return new Dog();
  }
  breed: string = "";
}

const animal: Animal = Dog.create(); // OK — Dog.create() returns Dog, which extends Animal
```

### Class vs interface

```typescript
class User {
  name: string = "";
  email: string = "";
}

interface UserLike {
  name: string;
  email: string;
}

const user: UserLike = new User(); // OK — class implements the interface structurally
```

---

## Function Parameter Bivariance

By default, TypeScript uses **bivariance** for function parameters — a function with a broader parameter type is assignable to a function with a narrower parameter type (and vice versa).

```typescript
interface EventHandler {
  (event: MouseEvent | KeyboardEvent): void;
}

const handler: EventHandler = (event) => {
  // event: MouseEvent | KeyboardEvent
};

// This is allowed due to bivariance:
const mouseHandler: (event: MouseEvent) => void = handler; // OK (but potentially unsafe!)
```

### Why bivariance?

```typescript
// Bivariance allows this pattern:
function addEventHandler(
  element: HTMLElement,
  event: string,
  handler: (event: Event) => void
) {
  element.addEventListener(event, handler);
}

// This would fail with strict contravariance:
addEventHandler(element, "click", (event: MouseEvent) => {
  // event: MouseEvent — but handler expects Event
  // This is actually safe because MouseEvent extends Event
});
```

### The danger of bivariance

```typescript
// With bivariance, this compiles but is unsafe:
let handler: (x: MouseEvent | KeyboardEvent) => void = (e) => console.log(e);
let safeHandler: (x: MouseEvent) => void = handler; // OK due to bivariance

// But this would pass a KeyboardEvent to safeHandler!
safeHandler(new KeyboardEvent("keydown")); // Runtime error if handler checks event type
```

---

## Strict Function Types Flag

The `--strictFunctionTypes` flag makes function parameters **contravariant** instead of bivariant.

### With strictFunctionTypes (default in strict mode)

```typescript
// With --strictFunctionTypes:
type Animal = { name: string };
type Dog = { name: string; breed: string };

// Contravariance — handler for broader type can't be assigned to handler for narrower type
type AnimalHandler = (animal: Animal) => void;
type DogHandler = (dog: Dog) => void;

const animalHandler: AnimalHandler = (a) => console.log(a.name);
const dogHandler: DogHandler = (d) => console.log(d.breed);

// Error with strictFunctionTypes:
// const handler: DogHandler = animalHandler; // Error!
// Because animalHandler might receive an Animal (without breed)
```

### Method bivariance exception

```typescript
// Even with strictFunctionTypes, methods are still bivariant
class Animal {
  name: string = "";
}

class Dog extends Animal {
  breed: string = "";
}

class Kennel {
  process(animal: Animal) {
    console.log(animal.name);
  }
}

// Methods are bivariant:
const kennel: Kennel = {
  process(dog: Dog) {
    console.log(dog.breed); // OK — method parameters are bivariant
  },
};
```

### strictBindCallApply

```typescript
// --strictBindCallApply makes bind, call, and apply strictly typed
function greet(name: string) {
  return `Hello, ${name}`;
}

// With strictBindCallApply:
greet.call(null, "Alice"); // OK
// greet.call(null, 42);   // Error — number not assignable to string
```

---

## Best Practices

1. **Enable `strict` mode** — includes strictFunctionTypes and other safety flags
2. **Use `unknown` over `any`** — forces type narrowing
3. **Be aware of excess property checks** — object literals are checked more strictly
4. **Understand bivariance in callbacks** — it's a pragmatic trade-off
5. **Use private members carefully** — they break structural compatibility
6. **Prefer interfaces over classes** for type definitions — more compatible
7. **Use const enums carefully** — they behave differently at compile time
8. **Test type compatibility** — use assignability checks in your codebase

---

## Interview Questions

### Q1: What is structural typing?

**Answer:** Structural typing means types are compatible based on their structure (properties and methods), not their names. If two types have the same shape, they're interchangeable. This is different from nominal typing (Java, C#) where types are compared by name.

### Q2: What is the difference between any and unknown?

**Answer:** `any` is compatible with everything — assignable to and from any type. It disables type checking. `unknown` is assignable from everything but requires type narrowing before use. Always prefer `unknown` over `any` for type safety.

### Q3: What is function parameter bivariance?

**Answer:** Bivariance means function parameters are compatible in both directions — a function with a broader parameter type can be assigned to one with a narrower type (and vice versa). TypeScript uses bivariance for pragmatic reasons (callback compatibility), but `--strictFunctionTypes` makes parameters contravariant.

### Q4: How do classes work with structural typing?

**Answer:** Classes are structurally typed like interfaces. A class is compatible with another type if it has the same properties. However, private members break compatibility — two classes with private members of the same name are NOT compatible because TypeScript checks the class identity, not just the structure.

### Q5: What is the excess property check?

**Answer:** When you assign an object literal directly to a type, TypeScript checks for extra properties that don't exist on the target type. This prevents typos and accidental extra properties. However, if you assign through a variable, the extra properties are allowed (this is called "fresh object literal" checking).

### Q6: How does `never` work with assignability?

**Answer:** `never` is the bottom type — it's assignable to every type (because you can never actually have a value of type `never`). But nothing is assignable to `never` (except `never` itself), because there's no value that can inhabit `never`. This makes `never` useful for exhaustive checking.
