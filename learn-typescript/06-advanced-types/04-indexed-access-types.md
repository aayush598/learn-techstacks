# Indexed Access Types in TypeScript

Indexed access types (`T[P]`) allow you to look up the type of a property in another type using a key. This is one of TypeScript's most powerful features for working with object types dynamically.

---

## Table of Contents

1. [What Are Indexed Access Types?](#what-are-indexed-access-types)
2. [T[P] Syntax](#tp-syntax)
3. [Accessing Nested Types](#accessing-nested-types)
4. [Indexed Access with Unions](#indexed-access-with-unions)
5. [Numeric Indexing](#numeric-indexing)
6. [keyof with Indexed Access](#keyof-with-indexed-access)
7. [Dynamic Property Access](#dynamic-property-access)
8. [String Index Signatures](#string-index-signatures)
9. [Number Index Signatures](#number-index-signatures)
10. [Real-World Use Cases](#real-world-use-cases)
11. [Best Practices](#best-practices)
12. [Interview Questions](#interview-questions)

---

## What Are Indexed Access Types?

Indexed access types let you extract the type of a specific property from an object type using bracket notation — similar to how you access a property value at runtime.

```typescript
type Person = {
  name: string;
  age: number;
  address: {
    street: string;
    city: string;
    zip: string;
  };
};

// Indexed access type
type NameType = Person["name"]; // string
type AgeType = Person["age"];   // number
type AddressType = Person["address"]; // { street: string; city: string; zip: string }
```

This is a **compile-time operation** — no runtime code is generated.

---

## T[P] Syntax

The syntax is `Type[Key]` where:
- `Type` is an object type, tuple, or any type with an index signature
- `Key` is a string literal, number literal, or union of literals

### Basic usage

```typescript
type User = {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
};

type IdType = User["id"];       // number
type NameType = User["name"];   // string
type EmailType = User["email"]; // string
```

### With type aliases

```typescript
type StringOrNumber = {
  value: string | number;
  label: string;
};

type ValueType = StringOrNumber["value"]; // string | number
type LabelType = StringOrNumber["label"]; // string
```

### With union keys

```typescript
type User = {
  id: number;
  name: string;
  email: string;
  age: number;
};

type IdOrName = User["id" | "name"]; // number | string
type IdOrAge = User["id" | "age"];   // number (both are number)
```

### The result is a union of the property types

```typescript
type User = {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
};

type StringProps = User["name" | "email"]; // string | string = string
type AllProps = User["id" | "name" | "email" | "isActive"]; // number | string | boolean
```

---

## Accessing Nested Types

You can chain indexed access to reach deep properties.

```typescript
type Company = {
  name: string;
  address: {
    street: string;
    city: string;
    country: {
      name: string;
      code: string;
    };
  };
  employees: Array<{
    name: string;
    role: string;
  }>;
};

// Direct access
type CompanyName = Company["name"]; // string

// Nested access
type CompanyCity = Company["address"]["city"]; // string
type CompanyCountryCode = Company["address"]["country"]["code"]; // string

// Array element type
type Employee = Company["employees"][number]; // { name: string; role: string }
```

### With type aliases for readability

```typescript
type Address = Company["address"];
type Country = Company["address"]["country"];
type CountryName = Country["name"]; // string
```

### Nested with unions

```typescript
type Config = {
  db: {
    host: string;
    port: number;
  };
  cache: {
    host: string;
    ttl: number;
  };
};

type HostConfig = Config["db" | "cache"]["host"]; // string
```

---

## Indexed Access with Unions

When you use a union as the key, the result is a union of the property types.

```typescript
type Person = {
  name: string;
  age: number;
  email: string;
  phone: string;
};

type ContactInfo = Person["email" | "phone"]; // string | string = string
type NameOrAge = Person["name" | "age"]; // string | number
```

### With union types on the object side

```typescript
type Admin = {
  role: "admin";
  permissions: string[];
  name: string;
};

type User = {
  role: "user";
  name: string;
  email: string;
};

type AdminOrUser = Admin | User;

type NameType = AdminOrUser["name"]; // string (both have `name: string`)
type RoleType = AdminOrUser["role"]; // "admin" | "user"

// ⚠️ Properties not shared by all union members
// type PermissionsType = AdminOrUser["permissions"]; // Error! "permissions" doesn't exist on User
```

### Accessing common properties from union types

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; side: number };

type KindType = Shape["kind"]; // "circle" | "square"
type RadiusOrSide = Shape["radius" | "side"]; // number | number = number
```

---

## Numeric Indexing

You can use numeric index access to get tuple element types.

```typescript
type Tuple = [string, number, boolean];

type First = Tuple[0];   // string
type Second = Tuple[1];  // number
type Third = Tuple[2];   // boolean

// With a union of indices
type FirstOrSecond = Tuple[0 | 1]; // string | number
```

### With arrays

```typescript
type StringArray = string[];
type ElementType = StringArray[number]; // string

type NumberTuple = [number, number, number];
type TupleElement = NumberTuple[number]; // number

// Generic array element type
type ArrayElement<T> = T[number];
type MyString = ArrayElement<string[]>; // string
```

### With readonly arrays

```typescript
type ReadonlyTuple = readonly [string, number, boolean];
type First = ReadonlyTuple[0]; // string
```

### Dynamic index access

```typescript
type Tuple = [string, number, boolean, null];

// Access with a numeric literal
type T0 = Tuple[0]; // string
type T1 = Tuple[1]; // number

// Access with a union of indices
type T01 = Tuple[0 | 1]; // string | number

// Access with keyof
type TupleKeys = keyof Tuple; // "0" | "1" | "2" | "3"
```

---

## keyof with Indexed Access

Combining `keyof` with indexed access is extremely powerful.

```typescript
type User = {
  id: number;
  name: string;
  email: string;
  age: number;
};

// Get all value types
type UserValues = User[keyof User]; // number | string | number = number | string

// Get a specific subset
type UserStringValues = User[Extract<keyof User, "name" | "email">]; // string | string = string
```

### Using with mapped types

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

// Get all property keys as a union
type UserKeys = keyof User; // "id" | "name" | "email"

// Get all property values as a union
type UserValues = User[keyof User]; // number | string
```

### Practical example: picking values

```typescript
interface Product {
  id: number;
  name: string;
  price: number;
  description: string;
  inStock: boolean;
}

type ProductValues = Product[keyof Product]; // number | string | boolean

// Get only string values
type ProductStrings = Product[Extract<keyof Product, {
  [K in keyof Product]: Product[K] extends string ? K : never;
}[keyof Product]>]; // string
```

---

## Dynamic Property Access

Indexed access types work with computed types, not just literal keys.

```typescript
type Person = {
  name: string;
  age: number;
  email: string;
};

// Dynamic key
type PropertyName = "name"; // or could be a type parameter
type NameType = Person[PropertyName]; // string

// With a union
type Keys = "name" | "email";
type NameOrEmail = Person[Keys]; // string | string = string
```

### Using with type parameters

```typescript
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key]; // return type is T[K]
}

const user = { name: "Alice", age: 30 };
const name = getProperty(user, "name"); // string
const age = getProperty(user, "age");   // number
```

### With conditional types

```typescript
type PickByType<T, U> = {
  [K in keyof T as T[K] extends U ? K : never]: T[K];
};

type User = {
  id: number;
  name: string;
  email: string;
  age: number;
  isActive: boolean;
};

type StringProps = PickByType<User, string>; // { name: string; email: string }
type NumberProps = PickByType<User, number>; // { id: number; age: number }
```

---

## String Index Signatures

When a type has a string index signature, you can access any `string` key.

```typescript
type Dictionary = {
  [key: string]: string;
};

type Value = Dictionary[string]; // string

// Any string key returns string
type AnyValue = Dictionary["anything"]; // string
```

### With specific properties

```typescript
type Config = {
  host: string;
  port: number;
  [key: string]: string | number; // index signature must be compatible
};

type HostType = Config["host"]; // string
type PortType = Config["port"]; // number
type AnyType = Config[string]; // string | number (union of index signature and named properties)
```

### Intersection of named and index access

```typescript
type Config = {
  host: string;
  port: number;
  debug: boolean;
  [key: string]: string | number | boolean;
};

// Config[string] gives you the index signature type
type AllValues = Config[string]; // string | number | boolean
```

---

## Number Index Signatures

Types with numeric index signatures allow numeric key access.

```typescript
type NumberMap = {
  [key: number]: string;
};

type Value = NumberMap[42]; // string

// Works with any number
type AnyValue = NumberMap[0]; // string
```

### Tuple types with number index

```typescript
type Tuple = [string, number, boolean];

// Tuple[number] gives you the union of all element types
type TupleValues = Tuple[number]; // string | number | boolean
```

### Arrays with number index

```typescript
type StringArray = string[];
type Element = StringArray[number]; // string

type NumberArray = number[];
type NumElement = NumberArray[number]; // number
```

---

## Real-World Use Cases

### 1. Getting all property values from a config

```typescript
type AppConfig = {
  apiUrl: string;
  timeout: number;
  retries: number;
  debug: boolean;
};

type ConfigValue = AppConfig[keyof AppConfig]; // string | number | boolean

function getConfigValue<K extends keyof AppConfig>(
  config: AppConfig,
  key: K
): AppConfig[K] {
  return config[key];
}
```

### 2. Extracting event handler parameter types

```typescript
type EventHandlers = {
  click: (event: MouseEvent) => void;
  keydown: (event: KeyboardEvent) => void;
  scroll: (event: Event) => void;
};

type ClickHandler = EventHandlers["click"]; // (event: MouseEvent) => void
type ClickEvent = Parameters<EventHandlers["click"]>[0]; // MouseEvent
```

### 3. Type-safe route parameters

```typescript
type Routes = {
  "/": void;
  "/users/:id": { id: string };
  "/users/:id/posts/:postId": { id: string; postId: string };
  "/search": { q: string; page: number };
};

type RouteParams<T extends string> = Routes[T];

function navigate<T extends keyof Routes>(route: T, params: RouteParams<T>) {
  // ...
}

navigate("/users/:id", { id: "123" });
navigate("/search", { q: "hello", page: 1 });
```

### 4. Extracting nested property types

```typescript
type DatabaseConfig = {
  connection: {
    host: string;
    port: number;
    ssl: boolean;
  };
  pool: {
    min: number;
    max: number;
    idle: number;
  };
};

type ConnectionConfig = DatabaseConfig["connection"];
type HostType = DatabaseConfig["connection"]["host"]; // string
type PoolMin = DatabaseConfig["pool"]["min"]; // number
```

### 5. Mapping over object values

```typescript
type User = {
  id: number;
  name: string;
  email: string;
};

type UserValues = User[keyof User]; // number | string

// Get all keys whose values are strings
type StringKeys = {
  [K in keyof User]: User[K] extends string ? K : never;
}[keyof User]; // "name" | "email"

// Pick only string properties
type UserStrings = Pick<User, StringKeys>; // { name: string; email: string }
```

### 6. Type-safe API responses

```typescript
type APIEndpoints = {
  "/users": { id: string; name: string }[];
  "/posts": { id: string; title: string; body: string }[];
  "/comments": { id: string; text: string; postId: string }[];
};

type ResponseType<T extends keyof APIEndpoints> = APIEndpoints[T];

async function fetchEndpoint<T extends keyof APIEndpoints>(
  endpoint: T
): Promise<ResponseType<T>> {
  const response = await fetch(endpoint);
  return response.json();
}

const users = await fetchEndpoint("/users"); // { id: string; name: string }[]
```

---

## Best Practices

1. **Use indexed access types to extract property types** — avoid duplicating type definitions
2. **Chain indexed access for deep properties** — `T["a"]["b"]["c"]`
3. **Combine with `keyof` for generic utility functions** — `T[K]` is extremely common
4. **Use with union keys for extracting multiple property types** — `T["a" | "b"]`
5. **Use `[number]` to get array/tuple element types** — `T[number]`
6. **Prefer indexed access over manual type definitions** — keeps types in sync with the source
7. **Use with conditional types for advanced filtering** — `T[K] extends U ? K : never`

---

## Interview Questions

### Q1: What are indexed access types?

**Answer:** Indexed access types (`T[P]`) extract the type of a property from an object type using bracket notation. They work at compile time and return the type of the property at the given key. You can use string literals, number literals, or unions as keys.

### Q2: How do you get the type of a nested property?

**Answer:** Chain indexed access types: `T["a"]["b"]["c"]`. Each bracket access returns the type of that property, which can then be further indexed. For example, `Company["address"]["city"]` returns `string` if `address.city` is typed as `string`.

### Q3: How do you get all values of an object type?

**Answer:** Use `T[keyof T]`. For example, `User[keyof User]` returns the union of all property value types. If `User = { id: number; name: string }`, then `User[keyof User]` is `number | string`.

### Q4: What does `T[number]` do?

**Answer:** `T[number]` extracts the element type of an array or tuple. For `string[]`, it returns `string`. For `[string, number]`, it returns `string | number`. For `readonly [boolean, string]`, it returns `boolean | string`.

### Q5: How do indexed access types work with union types?

**Answer:** When the object type is a union, indexed access returns the union of the property types from each member. `Admin | User["name"]` returns `string | string = string` if both have `name: string`. If a property doesn't exist on all members, you get a compile error.

### Q6: Can you use indexed access types dynamically?

**Answer:** Yes, with type parameters. `T[K]` where `K extends keyof T` allows dynamic property access at the type level. This is the basis for type-safe getter functions like `getProperty<T, K extends keyof T>(obj: T, key: K): T[K]`.
