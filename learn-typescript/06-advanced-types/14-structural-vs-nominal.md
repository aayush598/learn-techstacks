# Structural vs Nominal Typing in TypeScript

TypeScript uses **structural typing** (duck typing) — types are compatible if they have the same structure. Most other languages (Java, C#, Swift) use **nominal typing** — types are compatible only if they have the same name or explicit inheritance. Understanding this difference is crucial for writing type-safe TypeScript.

---

## Table of Contents

1. [Structural Typing in TypeScript](#structural-typing-in-typescript)
2. [Nominal Typing Emulation](#nominal-typing-emulation)
3. [Branded/Opaque Types](#brandedopaque-types)
4. [When Structural Typing Causes Issues](#when-structural-typing-causes-issues)
5. [Nominal Libraries](#nominal-libraries)
6. [Nominal Typing Patterns](#nominal-typing-patterns)
7. [Comparison with Java/C#](#comparison-with-javac)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Structural Typing in TypeScript

### How structural typing works

```typescript
interface Point {
  x: number;
  y: number;
}

interface Coordinate {
  x: number;
  y: number;
}

// These are the same type structurally
const point: Point = { x: 1, y: 2 };
const coord: Coordinate = point; // OK — same structure!
```

### Extra properties are fine

```typescript
interface Rectangle {
  width: number;
  height: number;
}

interface Square extends Rectangle {
  side: number;
}

function processShape(shape: Rectangle) {
  console.log(shape.width * shape.height);
}

const square: Square = { width: 5, height: 5, side: 5 };
processShape(square); // OK — Square has all properties of Rectangle
```

### Structural compatibility in function types

```typescript
type StringProcessor = (input: string) => string;
type AnyProcessor = (input: any) => string;

const anyProcessor: AnyProcessor = (input) => String(input);
const stringProcessor: StringProcessor = anyProcessor; // OK — structurally compatible
```

### Classes are structural too

```typescript
class Cat {
  meow() { return "meow"; }
  purr() { return "purrr"; }
}

class Dog {
  bark() { return "woof"; }
  meow() { return "meow"; } // Cats and dogs both meow!
}

function makeAnimalNoise(animal: { meow(): string }) {
  console.log(animal.meow());
}

makeAnimalNoise(new Cat()); // OK
makeAnimalNoise(new Dog()); // OK — Dog has meow()
```

---

## Nominal Typing Emulation

Since TypeScript is structural, you need patterns to emulate nominal typing.

### Branded types with unique symbol

```typescript
declare const UserIdBrand: unique symbol;
declare const PostIdBrand: unique symbol;

type UserId = string & { readonly [UserIdBrand]: true };
type PostId = string & { readonly [PostIdBrand]: true };

function createUserId(id: string): UserId {
  return id as UserId;
}

function createPostId(id: string): PostId {
  return id as PostId;
}

const userId = createUserId("abc");
const postId = createPostId("xyz");

function getUser(id: UserId) { /* ... */ }
function getPost(id: PostId) { /* ... */ }

getUser(userId);  // OK
// getUser(postId); // Error — nominal-like behavior!
```

### Branded types with type parameter

```typescript
declare const __brand: unique symbol;

type Brand<T, B extends string> = T & { readonly [__brand]: B };

type Cents = Brand<number, "Cents">;
type Dollars = Brand<number, "Dollars">;

function Dollars(value: number): Dollars {
  return value as Dollars;
}

function Cents(value: number): Cents {
  return value as Cents;
}

function charge(amount: Dollars) { /* ... */ }

charge(Dollars(5));   // OK
// charge(Cents(500)); // Error!
// charge(5);          // Error!
```

### Opaque types

```typescript
declare const __opaque: unique symbol;

type Opaque<T, K extends string> = T & { readonly [__opaque]: K };

type UserId = Opaque<string, "UserId">;
type Email = Opaque<string, "Email">;

function UserId(value: string): UserId {
  return value as UserId;
}

function Email(value: string): Email {
  return value as Email;
}
```

---

## When Structural Typing Causes Issues

### Problem: Mixing up IDs

```typescript
// Without nominal typing:
type UserId = string;
type OrderId = string;
type ProductId = string;

function getUser(id: UserId) { /* ... */ }
function getOrder(id: OrderId) { /* ... */ }
function getProduct(id: ProductId) { /* ... */ }

const userId = "user-123";
const orderId = "order-456";

getUser(userId);   // OK
getUser(orderId);  // No error! But this is a bug!
getOrder(userId);  // No error! Also a bug!
```

### Problem: Mixing up similar types

```typescript
type RGB = { r: number; g: number; b: number };
type HSL = { h: number; s: number; l: number };

function setRGB(color: RGB) { /* ... */ }
function setHSL(color: HSL) { /* ... */ }

// Structurally compatible — but semantically different!
setRGB({ h: 0, s: 100, l: 50 }); // No error! But wrong!
```

### Problem: Money types

```typescript
type USD = number;
type EUR = number;
type JPY = number;

function chargeUSD(amount: USD) { /* ... */ }
function chargeEUR(amount: EUR) { /* ... */ }

chargeUSD(100); // OK
chargeEUR(100); // No error! But 100 EUR != 100 USD!
```

---

## Nominal Libraries

Some TypeScript libraries provide nominal-like typing.

### io-ts

```typescript
import * as t from "io-ts";

// io-ts branded types
type Int = t.Branded<number, t.IntBrand>;
interface IntBrand {
  readonly Int: unique symbol;
}

function parseInt(value: number): Int {
  if (!Number.isInteger(value)) throw new Error("Not an integer");
  return value as Int;
}
```

### Zod

```typescript
import { z } from "zod";

const UserId = z.string().brand<"UserId">();
type UserId = z.infer<typeof UserId>;

const OrderId = z.string().brand<"OrderId">();
type OrderId = z.infer<typeof OrderId>;

// These are structurally the same but nominally different
const userId = UserId.parse("user-123");
const orderId = OrderId.parse("order-456");
```

### fp-ts

```typescript
import { pipe } from "fp-ts/function";
import * as O from "fp-ts/Option";

// fp-ts uses phantom types for nominal-like behavior
type UUID = string & { readonly UUID: unique symbol };

function UUID(value: string): UUID {
  return value as UUID;
}
```

### Effect

```typescript
import { Effect } from "effect";

// Effect uses branded types for error channels
type ValidationError = {
  readonly _tag: "ValidationError";
  readonly message: string;
};
```

---

## Nominal Typing Patterns

### Pattern 1: Class-based nominal types

```typescript
class UserId {
  private readonly __brand = true;

  constructor(public readonly value: string) {
    if (!value.startsWith("usr_")) {
      throw new Error("Invalid UserId format");
    }
  }
}

class OrderId {
  private readonly __brand = true;

  constructor(public readonly value: string) {
    if (!value.startsWith("ord_")) {
      throw new Error("Invalid OrderId format");
    }
  }
}

function getUser(id: UserId) { /* ... */ }
function getOrder(id: OrderId) { /* ... */ }

getUser(new UserId("usr_123")); // OK
// getUser(new OrderId("ord_456")); // Error!
```

### Pattern 2: Unique property

```typescript
type UserId = string & { readonly __type: "UserId" };
type OrderId = string & { readonly __type: "OrderId" };

function UserId(value: string): UserId {
  return value as UserId;
}

function OrderId(value: string): OrderId {
  return value as OrderId;
}
```

### Pattern 3: Symbol-based branding

```typescript
const UserIdSymbol = Symbol("UserId");
const OrderIdSymbol = Symbol("OrderId");

type UserId = string & { [UserIdSymbol]: never };
type OrderId = string & { [OrderIdSymbol]: never };

function UserId(value: string): UserId {
  return value as UserId;
}

function OrderId(value: string): OrderId {
  return value as OrderId;
}
```

---

## Comparison with Java/C#

### Java (nominal)

```java
// Java — nominal typing
public class UserId {
    private String value;

    public UserId(String value) {
        this.value = value;
    }

    public String getValue() { return value; }
}

public class OrderId {
    private String value;

    public OrderId(String value) {
        this.value = value;
    }

    public String getValue() { return value; }
}

// These are different types even though they have the same structure
UserId userId = new UserId("123");
OrderId orderId = new OrderId("456");
// userId = orderId; // Compile error — different types
```

### C# (nominal)

```csharp
// C# — nominal typing
public class UserId {
    public string Value { get; }

    public UserId(string value) {
        Value = value;
    }
}

public class OrderId {
    public string Value { get; }

    public OrderId(string value) {
        Value = value;
    }
}

// Different types
UserId userId = new UserId("123");
OrderId orderId = new OrderId("456");
// userId = orderId; // Compile error
```

### TypeScript (structural)

```typescript
// TypeScript — structural typing
class UserId {
  constructor(public value: string) {}
}

class OrderId {
  constructor(public value: string) {}
}

// Same structure — compatible!
const userId = new UserId("123");
const orderId = new OrderId("456");
const id: UserId = orderId; // OK — same structure!
```

### Key differences

| Aspect | Structural (TypeScript) | Nominal (Java/C#) |
|---|---|---|
| Compatibility | Based on shape | Based on name/inheritance |
| Explicit implementation | Not needed | Required (implements/extends) |
| Accidental compatibility | Possible | Prevented |
| Flexibility | High | Low |
| Type safety | Requires patterns for nominal | Built-in |

---

## Best Practices

1. **Use branded types for domain IDs** — UserId, OrderId, ProductId
2. **Use nominal typing when structural equivalence is dangerous** — money, coordinates
3. **Leverage structural typing for flexibility** — interfaces, callbacks, duck typing
4. **Use Zod or io-ts for runtime validation + nominal typing** — best of both worlds
5. **Document when structural compatibility is intentional** — prevent confusion
6. **Use unique symbols for brands** — most robust nominal typing pattern
7. **Consider class-based nominal types** — when you need methods and validation

---

## Interview Questions

### Q1: What is the difference between structural and nominal typing?

**Answer:** Structural typing (TypeScript) compares types by their shape — same properties means compatible. Nominal typing (Java, C#) compares by name — two types with the same structure are incompatible unless they share a name or inheritance chain. TypeScript is structural; most other languages are nominal.

### Q2: Why does TypeScript use structural typing?

**Answer:** Structural typing is more flexible and aligns with JavaScript's duck typing philosophy. It allows types to be compatible without explicit declarations, making it easier to work with existing JavaScript code and third-party libraries. However, it can cause issues when you want to distinguish between structurally identical types.

### Q3: How do you emulate nominal typing in TypeScript?

**Answer:** Use branded/opaque types: intersect the base type with an object containing a unique symbol property. For example, `type UserId = string & { readonly __brand: unique symbol }`. The phantom property makes structurally identical types incompatible. Libraries like Zod and io-ts provide this pattern built-in.

### Q4: When is structural typing problematic?

**Answer:** Structural typing is problematic when you need to distinguish between structurally identical types that have different meanings — like UserId vs OrderId, USD vs EUR, or RGB vs HSL. In these cases, accidental type mixing can cause bugs that the compiler won't catch.

### Q5: How do Java/C# handle what TypeScript handles with structural typing?

**Answer:** Java and C# use interfaces and inheritance for type compatibility. A class must explicitly `implement` an interface or `extend` a base class to be compatible. This prevents accidental compatibility but requires more boilerplate code.

### Q6: Should you always prefer structural typing?

**Answer:** No. Use structural typing when flexibility is desired (callbacks, duck typing, interoperability). Use nominal typing (branded types) when you need to prevent accidental compatibility between semantically different types. The best approach depends on the domain and the specific use case.
