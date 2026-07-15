# Branded Types in TypeScript

Branded types (also called **opaque types** or **nominal types**) add a unique identifier to a type so that two structurally identical types are treated as different. This is essential in TypeScript's structural type system where `string` is interchangeable with any other `string` type.

---

## Table of Contents

1. [What Are Branded Types?](#what-are-branded-types)
2. [Unique Symbol Branding](#unique-symbol-branding)
3. [Nominal Typing in Structural System](#nominal-typing-in-structural-system)
4. [Opaque Types](#opaque-types)
5. [Brand vs Nominal](#brand-vs-nominal)
6. [Real-World Branded Types](#real-world-branded-types)
7. [Validation with Branded Types](#validation-with-branded-types)
8. [Parsing Libraries](#parsing-libraries)
9. [Best Practices](#best-practices)
10. [Interview Questions](#interview-questions)

---

## What Are Branded Types?

In TypeScript, types are **structural** — if two types have the same shape, they're compatible. Branded types add a phantom property that makes structurally identical types incompatible.

```typescript
// Without branding — these are the same type!
type UserId = string;
type PostId = string;

function getUser(id: UserId) { /* ... */ }
function getPost(id: PostId) { /* ... */ }

const userId: UserId = "abc-123";
const postId: PostId = "abc-123";

getUser(postId); // No error! But this is a bug — wrong ID type!
getPost(userId); // No error! Also a bug!
```

### With branding

```typescript
type UserId = string & { readonly __brand: unique symbol };
type PostId = string & { readonly __brand: unique symbol };

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

const userId = createUserId("abc-123");
const postId = createPostId("xyz-789");

getUser(userId); // OK
// getUser(postId); // Compile error!
```

---

## Unique Symbol Branding

The most robust way to create branded types is using `unique symbol` as the brand property.

```typescript
declare const __brand: unique symbol;

type Brand<T, B extends string> = T & { readonly [__brand]: B };

type UserId = Brand<string, "UserId">;
type PostId = Brand<string, "PostId">;
type Email = Brand<string, "Email">;
type Money = Brand<number, "Money">;

// Factory functions
function UserId(id: string): UserId {
  return id as UserId;
}

function PostId(id: string): PostId {
  return id as PostId;
}

function Email(email: string): Email {
  if (!email.includes("@")) throw new Error("Invalid email");
  return email as Email;
}

function Money(amount: number): Money {
  if (amount < 0) throw new Error("Money cannot be negative");
  return amount as Money;
}
```

### Using the branded types

```typescript
const userId = UserId("user-123");
const postId = PostId("post-456");
const email = Email("alice@example.com");
const price = Money(29.99);

function getUser(id: UserId) { /* ... */ }
function getPost(id: PostId) { /* ... */ }
function sendEmail(to: Email) { /* ... */ }
function charge(amount: Money) { /* ... */ }

getUser(userId);   // OK
// getUser(postId); // Compile error!
sendEmail(email);  // OK
// sendEmail(userId); // Compile error!
charge(price);     // OK
// charge(100);    // Compile error — must use Money()
```

---

## Nominal Typing in Structural System

Branded types emulate **nominal typing** in TypeScript's structural system.

### The problem with structural typing

```typescript
type Cents = number;
type Dollars = number;

function payDollars(amount: Dollars) {
  console.log(`Paying $${amount}`);
}

const cents: Cents = 500;
payDollars(cents); // No error! But 500 cents != 500 dollars!
```

### The branded solution

```typescript
type Cents = number & { readonly __brand: "Cents" };
type Dollars = number & { readonly __brand: "Dollars" };

function Cents(value: number): Cents {
  return value as Cents;
}

function Dollars(value: number): Dollars {
  return value as Dollars;
}

function payDollars(amount: Dollars) {
  console.log(`Paying $${amount}`);
}

const cents = Cents(500);
const dollars = Dollars(5);

payDollars(dollars); // OK
// payDollars(cents); // Compile error!
// payDollars(5);     // Compile error — must use Dollars()
```

### Extending branded types

```typescript
type USD = Dollars & { readonly currency: "USD" };
type EUR = Dollars & { readonly currency: "EUR" };

function Dollars(amount: number, currency: string): Dollars {
  return amount as Dollars;
}
```

---

## Opaque Types

Opaque types are branded types where the internal structure is hidden from the outside.

```typescript
type Opaque<T, TBrand extends string> = T & { readonly __opaque: TBrand };

type UserId = Opaque<string, "UserId">;
type PostId = Opaque<string, "PostId">;

// You can't accidentally create these — you need a factory function
function createUserId(raw: string): UserId {
  // validation logic here
  return raw as UserId;
}

// The raw value is not accessible without casting
function getUserId(id: UserId): string {
  return id as unknown as string; // Must explicitly unwrap
}
```

### Opaque type builder pattern

```typescript
declare const __opaque: unique symbol;

type Opaque<K extends string, T> = T & { readonly [__opaque]: K };

type UserId = Opaque<"UserId", string>;
type OrderId = Opaque<"OrderId", string>;
type TransactionId = Opaque<"TransactionId", string>;

function createUserId(value: string): UserId {
  if (!value.startsWith("usr_")) throw new Error("Invalid user ID format");
  return value as UserId;
}

function createOrderId(value: string): OrderId {
  if (!value.startsWith("ord_")) throw new Error("Invalid order ID format");
  return value as OrderId;
}
```

---

## Brand vs Nominal

Both terms are used interchangeably, but there are subtle differences:

| Aspect | Branded Type | Nominal Type |
|---|---|---|
| Mechanism | Phantom property | Compiler-enforced name |
| Implementation | Intersection with object | Language feature (Java, C#) |
| TypeScript | Emulated via `&` | Not natively supported |
| Runtime cost | Zero | Zero |

### Nominal libraries

Some TypeScript libraries use nominal typing:

```typescript
// io-ts style
type Int = number & { readonly Int: unique symbol };
type Float = number & { readonly Float: unique symbol };

// Zod branded types
import { z } from "zod";

const UserIdSchema = z.string().brand<"UserId">();
type UserId = z.infer<typeof UserIdSchema>;
// string & { readonly __brand: "UserId" }
```

---

## Real-World Branded Types

### UserId and PostId

```typescript
declare const UserIdBrand: unique symbol;
declare const PostIdBrand: unique symbol;

type UserId = string & { readonly [UserIdBrand]: true };
type PostId = string & { readonly [PostIdBrand]: true };

function UserId(id: string): UserId {
  if (!id) throw new Error("UserId cannot be empty");
  return id as UserId;
}

function PostId(id: string): PostId {
  if (!id) throw new Error("PostId cannot be empty");
  return id as PostId;
}

// API functions
async function getUser(id: UserId) { /* ... */ }
async function getPost(id: PostId) { /* ... */ }
async function getUserPosts(userId: UserId) { /* ... */ }
```

### Email

```typescript
declare const EmailBrand: unique symbol;

type Email = string & { readonly [EmailBrand]: true };

function Email(value: string): Email {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(value)) {
    throw new Error(`Invalid email: ${value}`);
  }
  return value as Email;
}

function sendEmail(to: Email, subject: string, body: string) {
  // ...
}

const email = Email("alice@example.com");
sendEmail(email, "Hello", "World");
// sendEmail("not-an-email", "Hello", "World"); // Compile error
// sendEmail("alice@example.com", "Hello", "World"); // Compile error — must use Email()
```

### Money

```typescript
declare const MoneyBrand: unique symbol;

type Money = number & { readonly [MoneyBrand]: true };

function Money(amount: number): Money {
  if (!Number.isFinite(amount)) throw new Error("Amount must be finite");
  if (amount < 0) throw new Error("Amount cannot be negative");
  return amount as Money;
}

function formatMoney(amount: Money, currency: string): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(amount);
}

function addMoney(a: Money, b: Money): Money {
  return Money(a + b);
}

const price = Money(29.99);
const tax = Money(2.50);
const total = addMoney(price, tax);

formatMoney(total, "USD"); // "$32.49"
// addMoney(29.99, 2.50); // Compile error — must use Money()
```

### URL

```typescript
declare const UrlBrand: unique symbol;

type Url = string & { readonly [UrlBrand]: true };

function Url(value: string): Url {
  try {
    new URL(value);
    return value as Url;
  } catch {
    throw new Error(`Invalid URL: ${value}`);
  }
}

function fetchUrl(url: Url) {
  return fetch(url);
}

const apiUrl = Url("https://api.example.com/users");
fetchUrl(apiUrl);
// fetchUrl("not-a-url"); // Compile error
```

### UUID

```typescript
declare const UUIDBrand: unique symbol;

type UUID = string & { readonly [UUIDBrand]: true };

function UUID(value: string): UUID {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (!uuidRegex.test(value)) {
    throw new Error(`Invalid UUID: ${value}`);
  }
  return value as UUID;
}

function getUserById(id: UUID) { /* ... */ }

const userId = UUID("550e8400-e29b-41d4-a716-446655440000");
getUserById(userId);
// getUserById("not-a-uuid"); // Compile error
```

---

## Validation with Branded Types

Branded types ensure that values are validated before being used.

### Runtime validation + compile-time safety

```typescript
declare const PositiveNumberBrand: unique symbol;
type PositiveNumber = number & { readonly [PositiveNumberBrand]: true };

function PositiveNumber(value: number): PositiveNumber {
  if (value <= 0) throw new Error("Must be positive");
  return value as PositiveNumber;
}

function setQuantity(qty: PositiveNumber) { /* ... */ }

setQuantity(PositiveNumber(5));  // OK
setQuantity(PositiveNumber(0));  // Runtime error — Must be positive
// setQuantity(5);               // Compile error — must validate
```

### Validation with error types

```typescript
type ValidationError = { field: string; message: string };
type ValidEmail = { value: string; errors: ValidationError[] };

function validateEmail(input: string): ValidEmail {
  const errors: ValidationError[] = [];
  if (!input.includes("@")) {
    errors.push({ field: "email", message: "Must contain @" });
  }
  return { value: input, errors };
}
```

---

## Parsing Libraries

Libraries like Zod and io-ts provide branded types out of the box.

### Zod

```typescript
import { z } from "zod";

const UserId = z.string().brand<"UserId">();
type UserId = z.infer<typeof UserId>;

const Email = z.string().email().brand<"Email">();
type Email = z.infer<typeof Email>;

const Money = z.number().positive().brand<"Money">();
type Money = z.infer<typeof Money>;

// Parse and validate
const userId = UserId.parse("user-123"); // UserId
const email = Email.parse("alice@example.com"); // Email
const money = Money.parse(29.99); // Money

// Type-safe API
function getUser(id: UserId) { /* ... */ }
function sendEmail(to: Email) { /* ... */ }
function charge(amount: Money) { /* ... */ }
```

### io-ts

```typescript
import * as t from "io-ts";

const UserId = new t.Type<string, string, unknown>(
  "UserId",
  (input): input is string => typeof input === "string" && input.startsWith("usr_"),
  (input, context) => {
    const str = t.string.validate(input, context);
    if (str._tag === "Left") return str;
    if (!str.value.startsWith("usr_")) {
      return t.failure(input, context, "Must start with usr_");
    }
    return t.success(str.value);
  },
  (value) => value
);

type UserId = t.TypeOf<typeof UserId>;
```

### Valibot

```typescript
import * as v from "valibot";

const UserIdSchema = v.pipe(v.string(), v.brand("UserId"));
type UserId = v.InferOutput<typeof UserIdSchema>;

const userId = v.parse(UserIdSchema, "user-123");
```

---

## Best Practices

1. **Use branded types for domain-specific IDs** — UserId, PostId, OrderId, etc.
2. **Always create branded types through factory functions** — validates at runtime
3. **Use `unique symbol` for the brand** — ensures uniqueness across types
4. **Combine with validation libraries** — Zod, io-ts, or Valibot for automatic branding
5. **Document the branding convention** — so your team understands the pattern
6. **Use branded types for money, email, URL** — where structural equivalence is dangerous
7. **Avoid over-branding** — not every type needs a brand

---

## Interview Questions

### Q1: What are branded types and why use them?

**Answer:** Branded types add a phantom property to a type to prevent accidental assignment between structurally identical types. They're used for domain-specific IDs (UserId vs PostId), money (dollars vs cents), and other cases where structural equivalence is incorrect. They emulate nominal typing in TypeScript's structural system.

### Q2: How do you create a branded type?

**Answer:** Intersect the base type with an object containing a unique symbol property: `type UserId = string & { readonly [__brand]: unique symbol }`. The `unique symbol` ensures the brand is unique and cannot be accidentally replicated.

### Q3: What is the difference between branded and nominal types?

**Answer:** Nominal types are a language feature (Java, C#) where types are compared by name, not structure. TypeScript uses structural typing. Branded types emulate nominal typing by adding a phantom property. The effect is the same — two types with different names but the same structure are incompatible.

### Q4: How do parsing libraries help with branded types?

**Answer:** Libraries like Zod, io-ts, and Valibot provide built-in support for branded types. They validate input at runtime and produce branded types at compile time, ensuring both runtime safety and type safety without manual casting.

### Q5: Can branded types have runtime overhead?

**Answer:** No. Branded types are erased at compile time — the phantom property doesn't exist at runtime. The only runtime cost is in the factory/validation function, which is explicit and intentional.

### Q6: When should you NOT use branded types?

**Answer:** Don't use branded types when structural equivalence is correct (e.g., simple configuration objects), when the type is internal to a single module, or when the overhead of creating factory functions isn't justified. Over-branding makes code harder to read and maintain.
