# 10 — Template Literal Types

## Table of Contents

1. [Template Literal Type Syntax](#template-literal-type-syntax)
2. [Union in Template Literals](#union-in-template-literals)
3. [String Manipulation Types](#string-manipulation-types)
4. [Nested Template Literals](#nested-template-literals)
5. [Practical Uses](#practical-uses)
6. [Building Type-Safe APIs](#type-safe-apis)
7. [Best Practices](#best-practices)
8. [Interview Questions](#interview-questions)

---

## Template Literal Type Syntax

Template literal types use the same backtick syntax as JavaScript template literals,
but operate at the type level.

```typescript
type Greeting = `Hello, ${string}`;
// Matches any string starting with "Hello, "

type Name = "Alice";
type Age = 30;
type Info = `${Name} is ${Age}`;
// "Alice is 30" (exact literal type)
```

### Concatenation

```typescript
type First = "hello";
type Second = "world";
type Combined = `${First} ${Second}`;
// "hello world"
```

### With Unions

```typescript
type Color = "red" | "blue" | "green";
type Size = "sm" | "md" | "lg";

type ColorSize = `${Color}-${Size}`;
// "red-sm" | "red-md" | "red-lg" |
// "blue-sm" | "blue-md" | "blue-lg" |
// "green-sm" | "green-md" | "green-lg"
```

---

## Union in Template Literals

When a union type is used in a template literal, TypeScript produces the **cartesian
product** of all combinations.

```typescript
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiVersion = "v1" | "v2";

type ApiEndpoint = `/${ApiVersion}/${HttpMethod}`;
// "/v1/GET" | "/v1/POST" | "/v1/PUT" | "/v1/DELETE" |
// "/v2/GET" | "/v2/POST" | "/v2/PUT" | "/v2/DELETE"
```

### Large Unions

```typescript
type Direction = "top" | "bottom" | "left" | "right";
type Margin = "auto" | "0" | "1" | "2" | "3" | "4";

type MarginClass = `m-${Direction}-${Margin}`;
// "m-top-auto" | "m-top-0" | ... (32 combinations)
```

### Dynamic CSS Classes

```typescript
type Breakpoint = "sm" | "md" | "lg" | "xl";
type Property = "p" | "m" | "w" | "h";
type Scale = "0" | "1" | "2" | "3" | "4" | "5" | "auto";

type TailwindClass = `${Property}-${Breakpoint}-${Scale}`;
// 4 * 4 * 6 = 96 combinations
```

---

## String Manipulation Types

TypeScript provides built-in intrinsic string manipulation types.

### Uppercase

```typescript
type A = Uppercase<"hello">;       // "HELLO"
type B = Uppercase<"Hello World">; // "HELLO WORLD"
```

### Lowercase

```typescript
type A = Lowercase<"HELLO">;       // "hello"
type B = Lowercase<"Hello World">; // "hello world"
```

### Capitalize

```typescript
type A = Capitalize<"hello">;      // "Hello"
type B = Capitalize<"hello world">; // "Hello world"
```

### Uncapitalize

```typescript
type A = Uncapitalize<"Hello">;    // "hello"
type B = Uncapitalize<"Hello World">; // "hello World"
```

### Combined Usage

```typescript
type EventName<T extends string> = `on${Capitalize<T>}`;

type ClickEvent = EventName<"click">;    // "onClick"
type FocusEvent = EventName<"focus">;    // "onFocus"
type BlurEvent = EventName<"blur">;      // "onBlur"
```

---

## Nested Template Literals

Template literals can be nested for complex type transformations.

### Multi-Level Interpolation

```typescript
type Component = "Button" | "Input" | "Select";
type State = "default" | "hover" | "active" | "disabled";

type ComponentClass = `${Lowercase<Component>}-${State}`;
// "button-default" | "button-hover" | "button-active" | "button-disabled" |
// "input-default" | "input-hover" | "input-active" | "input-disabled" |
// "select-default" | "select-hover" | "select-active" | "select-disabled"
```

### Recursive Template Literals

```typescript
type Split<S extends string, D extends string> =
  S extends `${infer Head}${D}${infer Rest}`
    ? Head | Split<Rest, D>
    : S;

type Colors = Split<"red,blue,green", ",">;
// "red" | "blue" | "green"
```

### Nested Extraction

```typescript
type ExtractAfter<S extends string, D extends string> =
  S extends `${string}${D}${infer Rest}`
    ? Rest
    : never;

type AfterSlash = ExtractAfter<"/users/123/posts", "/">;
// "123/posts"

type AfterSecondSlash = ExtractAfter<AfterSlash, "/">;
// "posts"
```

---

## Practical Uses

### CSS Unit Types

```typescript
type CSSUnit = "px" | "rem" | "em" | "%" | "vh" | "vw" | "vmin" | "vmax";

type CSSValue<T extends CSSUnit> = `${number}${T}`;

type Width = CSSValue<"px">;     // `${number}px`
type FontSize = CSSValue<"rem">; // `${number}rem`

// Usage
function setWidth(el: HTMLElement, width: Width): void {
  el.style.width = width;
}

setWidth(document.body, "100px");  // ✅
// setWidth(document.body, "100"); // ❌ Missing unit
```

### Route Types

```typescript
type ExtractRouteParams<T extends string> =
  T extends `${string}:${infer Param}/${infer Rest}`
    ? Param | ExtractRouteParams<Rest>
    : T extends `${string}:${infer Param}`
      ? Param
      : never;

type Params = ExtractRouteParams<"/users/:userId/posts/:postId">;
// "userId" | "postId"

type RouteSegments<T extends string> =
  T extends `/${infer Segment}/${infer Rest}`
    ? Segment | RouteSegments<`/${Rest}`>
    : T extends `/${infer Segment}`
      ? Segment
      : never;

type Segments = RouteSegments<"/users/123/posts">;
// "users" | "123" | "posts"
```

### Event Names

```typescript
type DOMEvent = "click" | "dblclick" | "mousedown" | "mouseup" |
  "mouseover" | "mouseout" | "keydown" | "keyup" | "focus" | "blur" |
  "submit" | "change" | "input" | "scroll" | "resize";

type ReactEventName<T extends DOMEvent> =
  T extends "dblclick"
    ? "onDoubleClick"
    : T extends "mousedown"
      ? "onMouseDown"
      : T extends "mouseup"
        ? "onMouseUp"
        : T extends "mouseover"
          ? "onMouseOver"
          : T extends "mouseout"
            ? "onMouseOut"
            : `on${Capitalize<T>}`;

type OnClick = ReactEventName<"click">;       // "onClick"
type OnDblClick = ReactEventName<"dblclick">; // "onDoubleClick"
type OnSubmit = ReactEventName<"submit">;     // "onSubmit"
```

### Database Column Names

```typescript
type TableName = "users" | "posts" | "comments";
type ColumnSuffix = "Id" | "Name" | "Email" | "CreatedAt" | "UpdatedAt";

type ForeignKey = `${TableName}_${ColumnSuffix}`;
// "users_Id" | "users_Name" | ... (15 combinations)

type IndexName<T extends string> = `idx_${T}_index`;
type UserIndex = IndexName<"users_email">;
// "idx_users_email_index"
```

### Config Keys

```typescript
type Service = "auth" | "api" | "db" | "cache";
type ConfigSuffix = "url" | "timeout" | "retries" | "apiKey";

type ConfigKey = `${Service}_${ConfigSuffix}`;
// "auth_url" | "auth_timeout" | ... (16 combinations)

type EnvVar<T extends string> = `process.env.${Uppercase<T>}`;
type AuthUrl = EnvVar<"auth_url">;
// "process.env.AUTH_URL"
```

---

## Building Type-Safe APIs

### Type-Safe Event Emitter

```typescript
type EventNames = "user.created" | "user.updated" | "user.deleted" |
  "order.placed" | "order.shipped";

type EventData = {
  "user.created": { userId: string; name: string };
  "user.updated": { userId: string; changes: Record<string, unknown> };
  "user.deleted": { userId: string };
  "order.placed": { orderId: string; total: number };
  "order.shipped": { orderId: string; trackingNumber: string };
};

class TypedEmitter {
  private listeners = new Map<string, Set<Function>>();

  on<T extends EventNames>(
    event: T,
    handler: (data: EventData[T]) => void
  ): void {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(handler);
  }

  emit<T extends EventNames>(event: T, data: EventData[T]): void {
    this.listeners.get(event)?.forEach((fn) => fn(data));
  }
}

const emitter = new TypedEmitter();

emitter.on("user.created", (data) => {
  console.log(data.name); // ✅ string
});

emitter.emit("user.created", { userId: "1", name: "Alice" }); // ✅
// emitter.emit("user.created", { id: "1" }); // ❌ Missing name
```

### Type-Safe Builder Pattern

```typescript
type BuilderMethod<T extends string, V> = `set${Capitalize<T>}`;

type Builder<T> = {
  [K in keyof T as BuilderMethod<string & K, T[K]>]: (value: T[K]) => Builder<T>;
} & {
  build(): T;
};

function createBuilder<T extends Record<string, unknown>>(): Builder<T> {
  const data = {} as T;
  const builder = {} as any;

  for (const key of Object.keys(data)) {
    const methodName = `set${key.charAt(0).toUpperCase()}${key.slice(1)}`;
    builder[methodName] = (value: any) => {
      (data as any)[key] = value;
      return builder;
    };
  }

  builder.build = () => data;
  return builder;
}

interface UserForm {
  name: string;
  email: string;
  age: number;
}

const user = createBuilder<UserForm>()
  .setName("Alice")
  .setEmail("alice@example.com")
  .setAge(30)
  .build();
// { name: "Alice"; email: "alice@example.com"; age: 30 }
```

### Type-Safe API Client

```typescript
type ApiRoutes = {
  "GET /users": { response: User[]; params: never };
  "GET /users/:id": { response: User; params: { id: string } };
  "POST /users": { response: User; body: CreateUserInput };
  "GET /posts": { response: Post[]; params: never };
  "GET /posts/:id": { response: Post; params: { id: string } };
};

type ExtractRoute<T extends string> =
  T extends `${infer Method} ${infer Path}`
    ? { method: Method; path: Path }
    : never;

type ApiClient = {
  [K in keyof ApiRoutes as ExtractRoute<K>["path"] extends string
    ? ExtractRoute<K>["path"]
    : never]: ApiRoutes[K];
};
```

---

## Best Practices

1. **Use template literals for string patterns** — CSS classes, event names, routes.
2. **Combine with unions** for cartesian product types.
3. **Use intrinsic types** (`Uppercase`, `Lowercase`, `Capitalize`) for case
   transformations.
4. **Avoid overly complex template types** — they can slow down the compiler.
5. **Document the expected string format** — template literal types are not self-documenting.

---

## Interview Questions

**Q1: What are template literal types?**

Types that use backtick syntax with `${}` interpolation to construct string literal
types at compile time.

**Q2: What happens when you use a union in a template literal?**

TypeScript produces the cartesian product of all combinations.

**Q3: What built-in string manipulation types exist?**

`Uppercase<T>`, `Lowercase<T>`, `Capitalize<T>`, and `Uncapitalize<T>`.

**Q4: Can you extract parts of a string using template literals?**

Yes, using `infer` in conditional types with template literal patterns:
`T extends \`${infer A}/${infer B}\``.

**Q5: What is a practical use for template literal types?**

Type-safe CSS classes, event handlers, route parameters, API endpoints, and database
column names.
