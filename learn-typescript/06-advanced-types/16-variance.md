# Variance in TypeScript

## Table of Contents

1. [What is Variance](#what-is-variance)
2. [Types of Variance](#types-of-variance)
3. [Function Variance](#function-variance)
4. [Generic Variance](#generic-variance)
5. [Variance of Built-in Types](#variance-of-built-in-types)
6. [Real-World Examples](#real-world-examples)
7. [Interview Questions](#interview-questions)

---

## What is Variance

Variance is a concept from type theory that describes how subtyping relationships between
compound types relate to subtyping relationships between their constituent types. In
TypeScript, it determines whether `Type<A>` is assignable to `Type<B>` when `A` is
assignable to `B`.

### Why It Matters for Type Safety

Consider a `Cat` that extends `Animal`. If `Cat` is a subtype of `Animal`, the question
becomes: is `Array<Cat>` a subtype of `Array<Animal>`? The answer depends on variance:

- **Covariant**: `Array<Cat>` is a subtype of `Array<Animal>` (preserves direction)
- **Contravariant**: `Array<Animal>` is a subtype of `Array<Cat>` (reverses direction)
- **Invariant**: Neither is a subtype of the other

Getting variance wrong leads to runtime errors that TypeScript should catch at compile time.

### Variance in TypeScript vs Other Languages

TypeScript has unique variance behavior compared to most typed languages:

```typescript
// In TypeScript, Array<T> is mutable but treated as COVARIANT
// This is UNSOUND — it's a pragmatic compromise for DX
const animals: Animal[] = [new Cat()];
const cats: Cat[] = animals; // Type error (but only because of array literal checking)

// In Java/C#, List<Cat> is NOT assignable to List<Animal> (invariant by default)
// In Scala, List[Cat] IS assignable to List[Animal] (immutable = covariant)
// In C#, IEnumerable<Cat> IS assignable to IEnumerable<Animal> (covariant via `out`)
```

TypeScript prioritizes developer experience over strict soundness. Mutable containers are
treated as covariant, which is technically unsound but rarely causes issues in practice
because of additional checks on assignment sites.

---

## Types of Variance

### 1. Invariant

A type parameter is invariant when it appears in both covariant and contravariant
positions. Neither subtyping direction is preserved.

```typescript
// A mutable array is conceptually invariant
// You can't safely assign Animal[] to Cat[] or vice versa

interface MutableBox<T> {
  value: T;
  setValue(v: T): void;
}

// MutableBox<Cat> is NOT assignable to MutableBox<Animal>
// MutableBox<Animal> is NOT assignable to MutableBox<Cat>
// Because T appears in both read (value) and write (setValue) positions
```

**Why mutable arrays are technically invariant:**

```typescript
const animals: Animal[] = [new Cat()];
// If TypeScript allowed this:
// animals.push(new Dog()); // Runtime error! We're putting a Dog in a Cat[]

// TypeScript prevents this through array literal checking:
const cats: Cat[] = animals; // Error: Type 'Animal[]' is not assignable to type 'Cat[]'

// But it allows this (unsound):
animals.push(new Dog()); // No error! Animal[] allows any Animal
// Now cats[1] is a Dog, not a Cat — runtime crash waiting to happen
```

### 2. Covariant

A type parameter is covariant when it only appears in read/output positions.
The subtyping direction is preserved: `Type<Subtype>` extends `Type<Supertype>`.

```typescript
// ReadonlyArray is covariant
function processAnimals(animals: ReadonlyArray<Cat>): void {
  const allAnimals: ReadonlyArray<Animal> = animals; // ✅ OK — covariant
  allAnimals.forEach(a => a.eat()); // ✅ OK — Cat has eat()
}

// Promise is covariant
async function handleCat(cat: Promise<Cat>): Promise<Animal> {
  const animal: Promise<Animal> = cat; // ✅ OK — Promise<T> is covariant in T
  return animal;
}
```

### 3. Contravariant

A type parameter is contravariant when it only appears in write/input positions.
The subtyping direction is reversed: `Type<Supertype>` extends `Type<Subtype>`.

```typescript
// Function parameters are contravariant
type Handler<T> = (event: T) => void;

declare function handleAnimal(handler: Handler<Animal>): void;
declare function handleCat(handler: Handler<Cat>): void;

// Handler<Cat> is assignable to Handler<Animal>
// Because if you can handle ANY Animal, you can certainly handle a Cat
const animalHandler: Handler<Animal> = (a) => a.eat();
handleCat(animalHandler); // ✅ OK — contravariant

// Handler<Animal> is NOT assignable to Handler<Cat>
// Because a handler that only knows about Animals might not handle Cat.scratch()
const catHandler: Handler<Cat> = (c) => { c.eat(); c.scratch(); };
handleAnimal(catHandler); // ❌ Error — Handler<Animal> doesn't know about scratch()
```

### 4. Bivariant

A type parameter is bivariant when it's assignable in both directions. In TypeScript,
this only happens with method syntax when `--strictFunctionTypes` is disabled.

```typescript
interface Processor {
  // Method syntax — bivariant (even with strictFunctionTypes)
  process(value: Animal): void;

  // Property syntax — contravariant (with strictFunctionTypes)
  processFn: (value: Animal) => void;
}

// With --strictFunctionTypes: true (default in strict mode):
// process: contravariant
// processFn: contravariant
//
// With --strictFunctionTypes: false:
// process: bivariant (unsound!)
// processFn: contravariant
```

---

## Function Variance

### Parameter Contravariance Explained Deeply

The fundamental rule: **function parameters are contravariant** because of the
Liskov Substitution Principle (LSP). If `Sub` extends `Super`, then a function that
accepts `Super` can be used where a function accepting `Sub` is expected, but NOT
the reverse.

```typescript
class Animal {
  eat(): void { console.log('eating'); }
}

class Cat extends Animal {
  scratch(): void { console.log('scratching'); }
}

class Dog extends Animal {
  bark(): void { console.log('barking'); }
}

// A function that processes any Animal
function processAnimal(animal: Animal): void {
  animal.eat(); // ✅ Animal has eat()
}

// A function that processes only Cats
function processCat(cat: Cat): void {
  cat.eat();     // ✅ Cat has eat()
  cat.scratch(); // ✅ Cat has scratch()
}

// Contravariance: processAnimal can be used where processCat is expected
const processCatFn: (cat: Cat) => void = processAnimal; // ✅ OK
// Why? Wherever we expect to call processCat(cat), passing processAnimal works
// because processAnimal can handle any Animal, and Cat is an Animal

// The reverse is NOT true:
const processAnimalFn: (animal: Animal) => void = processCat; // ❌ Error
// Why? Wherever we expect to call processAnimal(animal), passing processCat fails
// because we might pass a Dog, and processCat doesn't handle Dogs
```

### Return Type Covariance

Return types are covariant because they appear in output/read positions:

```typescript
class Animal {
  eat(): void {}
}

class Cat extends Animal {
  scratch(): void {}
}

function getAnimal(): Animal {
  return new Animal();
}

function getCat(): Cat {
  return new Cat();
}

// Covariance: getCat can be used where getAnimal is expected
const getAnimalFn: () => Animal = getCat; // ✅ OK
// Why? getCat returns a Cat, which IS an Animal

// The reverse is NOT true:
const getCatFn: () => Cat = getAnimal; // ❌ Error
// Why? getAnimal returns an Animal, which might NOT be a Cat
```

### `strictFunctionTypes` Flag

The `--strictFunctionTypes` flag enables proper contravariance checking for function
parameters. Without it, function parameters are checked bivariantly (unsound).

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strictFunctionTypes": true // Enabled by default with "strict": true
  }
}

// With strictFunctionTypes: true
type Callback<T> = (data: T) => void;

declare function onAnimalEvent(cb: Callback<Animal>): void;
declare function onCatEvent(cb: Callback<Cat>): void;

const catCallback: Callback<Cat> = (cat) => cat.scratch();
onAnimalEvent(catCallback); // ❌ Error — Callback<Cat> not assignable to Callback<Animal>

// With strictFunctionTypes: false (UNSOUND)
onAnimalEvent(catCallback); // ✅ No error — but dangerous!
// If onAnimalEvent calls cb(new Dog()), we'd have a Dog where a Cat is expected
```

### Method Bivariance (Method Syntax vs Property Syntax)

TypeScript treats method declarations differently from function properties. Methods use
"bivariant" checking for practical reasons (DOM APIs, event handlers):

```typescript
interface EventTarget {
  // Method syntax — bivariant (practical compromise for DOM APIs)
  addEventListener(type: string, listener: (e: Event) => void): void;
}

interface EventEmitter {
  // Property syntax — strictly contravariant with strictFunctionTypes
  on: (event: string, listener: (e: Event) => void) => void;
}

// With strictFunctionTypes, methods are still bivariant:
interface StrictProcessor {
  // This is checked bivariantly:
  process(value: Animal): void;
}

interface StrictCatProcessor {
  process(value: Cat): void;
}

// Method syntax allows this (unsound but practical):
declare const animalProc: StrictProcessor;
const catProc: StrictCatProcessor = animalProc; // ✅ OK with method syntax

// Property syntax would catch this:
interface StrictProcessorFn {
  process: (value: Animal) => void;
}
interface StrictCatProcessorFn {
  process: (value: Cat) => void;
}

declare const animalProcFn: StrictProcessorFn;
const catProcFn: StrictCatProcessorFn = animalProcFn; // ❌ Error with strictFunctionTypes
```

**Why methods are bivariant:**

The TypeScript team made this decision because the DOM API uses methods extensively,
and making them strictly contravariant would break too much existing code. The trade-off
is soundness for practicality.

### `--strictBindCallApply`

This flag makes `.bind()`, `.call()`, and `.apply()` respect the same strict type
checking as regular function calls:

```typescript
// With strictBindCallApply: true (default in strict mode)
function greet(name: string, age: number): string {
  return `Hello ${name}, age ${age}`;
}

// .bind() is fully typed
const greetAlice = greet.bind(null, 'Alice');
greetAlice(30); // ✅ OK
greetAlice('30'); // ❌ Error — age must be number

// .call() is fully typed
greet.call(null, 'Alice', 30); // ✅ OK
greet.call(null, 'Alice', '30'); // ❌ Error

// .apply() is fully typed
greet.apply(null, ['Alice', 30]); // ✅ OK
greet.apply(null, ['Alice']); // ❌ Error — missing age argument
```

---

## Generic Variance

### How Generics Inherit Variance from Usage

A generic type parameter's variance is determined by how it's used in the type
definition. This is called "use-site variance" in languages like Kotlin and C#.

```typescript
// Covariant: T only appears in output positions
interface Producer<T> {
  produce(): T; // T in output position
}

// Contravariant: T only appears in input positions
interface Consumer<T> {
  consume(item: T): void; // T in input position
}

// Invariant: T appears in both input and output positions
interface Transformer<T> {
  transform(input: T): T; // T in both positions
}

// Bivariant: T doesn't appear at all (or appears only in unused positions)
interface Logger<T> {
  log(message: string): void; // T is not used
}
```

### Variance Annotations with `in` and `out` Keywords (TS 4.7+)

TypeScript 4.7 introduced explicit variance annotations. These are both documentation
and enforcement mechanisms:

```typescript
// Covariant: T only used in output positions
interface Producer<out T> {
  produce(): T; // ✅ T in output — matches `out` annotation
}

// Contravariant: T only used in input positions
interface Consumer<in T> {
  consume(item: T): void; // ✅ T in input — matches `in` annotation
}

// Invariant: T used in both positions
interface Transformer<in out T> {
  transform(input: T): T; // ✅ T in both — matches `in out` annotation
}

// ERROR: Violating variance annotation
interface BadProducer<out T> {
  consume(item: T): void; // ❌ Error: T is contravariant but annotated as covariant
}

interface BadConsumer<in T> {
  produce(): T; // ❌ Error: T is covariant but annotated as contravariant
}
```

### Why Variance Annotations Matter for Performance

Variance annotations help the TypeScript compiler optimize type checking:

```typescript
// Without annotations, TypeScript must check all usages of T
// With annotations, TypeScript can make quick decisions:
// - `out T`: If Assignable(A, B), then Assignable(Provider<A>, Provider<B>)
// - `in T`: If Assignable(A, B), then Assignable(Consumer<B>, Consumer<A>)

// Performance impact with deep type hierarchies:
interface DeepCovariant<out T> {
  level1: {
    level2: {
      value: T;
    };
  };
}

// With `out T`, TypeScript knows this is covariant and can short-circuit
// Without annotations, it would need to inspect the entire structure
```

### Common Errors When Variance Is Wrong

```typescript
// Error 1: Violating out annotation
interface Producer<out T> {
  produce(): T;
  consume(item: T): void; // ❌ Error: T is contravariant here
}

// Error 2: Violating in annotation
interface Consumer<in T> {
  consume(item: T): void;
  produce(): T; // ❌ Error: T is covariant here
}

// Error 3: Mixed variance without in out
interface Weird<T> {
  read(): T;      // covariant position
  write(item: T): void; // contravariant position
}
// T is invariant — can't annotate as `in T` or `out T`
// Must use `in out T` or no annotation

// Error 4: Using variance annotations with wrong variance
interface Container<out T> {
  items: T[]; // ❌ Error: Array<T> is covariant, but T is in a mutable property
  // T[] is covariant, but the array is mutable, so it's effectively invariant
}
```

---

## Variance of Built-in Types

### Array\<T\> vs ReadonlyArray\<T\>

```typescript
// Array<T> is MUTABLE — TypeScript treats it as covariant (unsound!)
const cats: Cat[] = [new Cat()];
const animals: Animal[] = cats; // ✅ No error (covariant, but unsound!)
animals.push(new Dog()); // ✅ No error — Dog extends Animal
cats[1].scratch(); // 💥 Runtime error! Dog has no scratch()

// ReadonlyArray<T> is IMMUTABLE — safely covariant
const readonlyCats: ReadonlyArray<Cat> = [new Cat()];
const readonlyAnimals: ReadonlyArray<Animal> = readonlyCats; // ✅ OK
// readonlyAnimals.push(new Dog()); // ❌ Error — no push on ReadonlyArray

// The key difference: mutability makes invariance necessary
// TypeScript sacrifices soundness for Array<T> convenience
```

### Promise\<T\> Covariance

```typescript
// Promise<T> is covariant — T only appears in the resolve callback
async function getCats(): Promise<Cat[]> {
  return [new Cat()];
}

async function getAnimals(): Promise<Animal[]> {
  return getCats(); // ✅ OK — Promise<Cat[]> assignable to Promise<Animal[]>
}

// Promise is safe to be covariant because you can only read from it
// You can't push into a Promise
```

### Map\<K,V\> and Set\<T\> Variance

```typescript
// Map<K, V> is invariant in practice
// K appears in contravariant position (get, has, delete)
// V appears in covariant position (get returns V)
// But Map also has set(key, value) where V is in contravariant position

const catMap = new Map<string, Cat>();
// const animalMap: Map<string, Animal> = catMap; // ❌ Error in strict mode

// Set<T> is similarly invariant
// T appears in both add(item: T) and has(item: T)
const catSet = new Set<Cat>();
// const animalSet: Set<Animal> = catSet; // ❌ Error
```

### Function Variance in Detail

```typescript
// Function<Args, Return> is:
// - Contravariant in Args (parameters)
// - Covariant in Return (return type)

type AnimalHandler = (animal: Animal) => Animal;
type CatHandler = (cat: Cat) => Cat;

// CatHandler is assignable to AnimalHandler because:
// - CatHandler's parameter (Cat) is a subtype of Animal (contravariant — reversed)
// - CatHandler's return (Cat) is a subtype of Animal (covariant — preserved)

const animalHandler: AnimalHandler = (a) => a;
const catHandler: CatHandler = animalHandler; // ✅ OK

// But AnimalHandler is NOT assignable to CatHandler:
const catHandler2: CatHandler = (c) => c;
const animalHandler2: AnimalHandler = catHandler2; // ❌ Error
// Why? catHandler2 expects Cat, but we'd pass Animal which might be Dog
```

---

## Real-World Examples

### Event Handler Compatibility

```typescript
// Real-world: DOM event handlers
interface MouseEvent {
  x: number;
  y: number;
  button: number;
}

interface ClickEvent extends MouseEvent {
  detail: number;
}

// Contravariance in action:
type MouseEventHandler = (e: MouseEvent) => void;
type ClickEventHandler = (e: ClickEvent) => void;

// ClickEventHandler is assignable to MouseEventHandler
const handleMouse: MouseEventHandler = (e) => {
  console.log(e.x, e.y);
};

const handleClick: ClickEventHandler = handleMouse; // ✅ OK
// Why? If handleMouse can process any MouseEvent, it can certainly process ClickEvent

// The reverse fails:
const handleClickStrict: ClickEventHandler = (e) => {
  console.log(e.detail); // ClickEvent has detail
};

const handleMouseStrict: MouseEventHandler = handleClickStrict; // ❌ Error
// Why? handleMouseStrict might receive a plain MouseEvent without detail
```

### Callback Compatibility

```typescript
// Real-world: API callback compatibility
interface ApiResponse {
  data: unknown;
  status: number;
}

interface UserResponse extends ApiResponse {
  data: {
    id: string;
    name: string;
  };
}

// Contravariance allows flexible callback usage
type ApiCallback = (response: ApiResponse) => void;
type UserCallback = (response: UserResponse) => void;

function fetchData(callback: ApiCallback): void {
  // ...
}

// UserCallback is assignable to ApiCallback
const handleUser: UserCallback = (res) => {
  console.log(res.data.name);
};

fetchData(handleUser); // ✅ OK — contravariance allows this

// But ApiCallback is NOT assignable to UserCallback
const handleApi: ApiCallback = (res) => {
  console.log(res.status);
};

function fetchUserData(callback: UserCallback): void {
  // ...
}

fetchUserData(handleApi); // ❌ Error — handleApi doesn't know about .data.name
```

### Container/Collection Variance

```typescript
// Real-world: Repository pattern
interface Repository<T> {
  findById(id: string): T | null;
  findAll(): T[];
  save(item: T): void; // Makes T invariant
}

interface CatRepository extends Repository<Cat> {
  findByBreed(breed: string): Cat[];
}

interface AnimalRepository extends Repository<Animal> {
  findBySpecies(species: string): Animal[];
}

// Repository<Cat> is NOT assignable to Repository<Animal>
// Because save(item: Cat) conflicts with save(item: Animal)
// This is correct! We can't save a Dog through a CatRepository

// But if we make it read-only (covariant):
interface ReadRepository<out T> {
  findById(id: string): T | null;
  findAll(): T[];
}

// Now ReadRepository<Cat> IS assignable to ReadRepository<Animal> ✅
```

### React Component Variance

```typescript
// Real-world: React component types
import { ComponentType, FC, ReactNode } from 'react';

// ComponentType<P> is contravariant in P (with strictFunctionTypes)
type CatComponent = ComponentType<{ cat: Cat }>;
type AnimalComponent = ComponentType<{ animal: Animal }>;

// AnimalComponent is assignable to CatComponent
const AnimalComp: AnimalComponent = ({ animal }) => <div>{animal.name}</div>;
const CatComp: CatComponent = AnimalComp; // ✅ OK — contravariant

// FC<P> is contravariant in P
type CatFC = FC<{ cat: Cat }>;
type AnimalFC = FC<{ animal: Animal }>;

const AnimalFCComp: AnimalFC = ({ animal }) => <div>{animal.name}</div>;
const CatFCComp: CatFC = AnimalFCComp; // ✅ OK

// This makes sense: if a component accepts any Animal,
// it can certainly handle a Cat
```

---

## Interview Questions

### Q1: What is the difference between covariance and contravariance?

**A:** Covariance preserves the subtyping direction — if `A` extends `B`, then
`Type<A>` extends `Type<B>`. Contravariant reverses it — if `A` extends `B`, then
`Type<B>` extends `Type<A>`. Covariant positions are output/read positions; contravariant
positions are input/write positions.

```typescript
interface Covariant<out T> { get(): T; }        // T covariant
interface Contravariant<in T> { set(v: T): void; } // T contravariant
```

### Q2: Why are function parameters contravariant?

**A:** Because of the Liskov Substitution Principle. If function `f` accepts `Animal` and
function `g` accepts `Cat`, then `g` is more specific. A function that handles any
`Animal` can certainly handle a `Cat`, but a function that only handles `Cat` cannot
necessarily handle any `Animal` (like a `Dog`). Therefore `f` can be used where `g` is
expected, but not the reverse.

### Q3: What does `strictFunctionTypes` do?

**A:** It enables strict contravariance checking for function parameters when using
property syntax (`fn: (x: T) => void`). Without it, function parameters are checked
bivariantly (both directions allowed), which is unsound. Note that method syntax still
uses bivariant checking even with this flag enabled.

### Q4: What are variance annotations in TypeScript 4.7?

**A:** The `in` and `out` keywords on type parameters that explicitly declare expected
variance. `out T` means T should only be used in covariant (output) positions. `in T`
means T should only be used in contravariant (input) positions. `in out T` means
invariant. TypeScript enforces these annotations and errors if the actual usage violates
them.

### Q5: Is Array\<T\> covariant or contravariant? Why is this a problem?

**A:** Array\<T\> is treated as covariant in TypeScript, but this is technically unsound.
Since arrays are mutable, you can push a supertype into a covariant array, breaking type
safety:

```typescript
const cats: Cat[] = [new Cat()];
const animals: Animal[] = cats; // Allowed (covariant)
animals.push(new Dog()); // Allowed — Dog extends Animal
cats[1].scratch(); // Runtime error! Dog doesn't have scratch()
```

ReadonlyArray\<T\> is safely covariant because immutability prevents this issue.

### Q6: What is bivariance and why does TypeScript allow it?

**A:** Bivariance means a type is considered assignable in both directions. TypeScript
allows this for method syntax (`method(x: T): void`) even with `strictFunctionTypes`
enabled. This is a deliberate compromise for practicality — many DOM APIs and existing
codebases rely on this behavior. Making methods strictly contravariant would break too
much code.

### Q7: How do you make a generic type covariant?

**A:** Ensure the type parameter only appears in output/read positions, or use the `out`
annotation:

```typescript
interface Producer<out T> {
  produce(): T; // T only in output position
}

// With `out T`, TypeScript enforces that T is only used covariantly
```

### Q8: What happens when you violate variance rules?

**A:** TypeScript will error if you use variance annotations and the actual usage violates
them. Without annotations, TypeScript may allow unsound assignments (like `Array<Cat>`
to `Array<Animal>`), which can lead to runtime errors when operations assume the wrong
type.

### Q9: Explain with a real-world example why contravariance of function parameters makes sense.

**A:** Consider event handlers: a handler that processes any `MouseEvent` can certainly
process a `ClickEvent` (which extends `MouseEvent`). But a handler that only processes
`ClickEvent` cannot necessarily process a plain `MouseEvent` (which might not have
`detail` property). This is why `ClickEventHandler` is assignable to
`MouseEventHandler`, but not vice versa — contravariance.

### Q10: What is the relationship between variance and the Liskov Substitution Principle?

**A:** LSP states that objects of a subtype should be substitutable for objects of a
supertype. Variance formalizes this for type constructors. Contravariance of function
parameters ensures that a function accepting a supertype can be used where a function
accepting a subtype is expected. Covariance of return types ensures that returning a
subtype is safe where a supertype is expected. Both preserve LSP.

### Q11: How does TypeScript 4.7's `in`/`out` syntax differ from Kotlin's `in`/`out`?

**A:** They're conceptually the same but syntactically different. Kotlin uses declaration-site
variance (`class Producer<out T>`), while TypeScript 4.7 also uses declaration-site syntax
(`interface Producer<out T>`). The key difference is that TypeScript enforces variance
annotations at the declaration site and reports errors if the usage violates them, while
Kotlin's variance is more permissive with type projections.

### Q12: Can a type parameter be both covariant and contravariant?

**A:** Yes — this is called invariance. It happens when a type parameter appears in both
input and output positions. For example, `interface Transformer<T> { transform(v: T): T; }`
has T in both positions, making it invariant. You can explicitly annotate this with
`in out T`.
