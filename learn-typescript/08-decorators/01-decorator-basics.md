# Decorator Basics in TypeScript

## Table of Contents

- [Overview](#overview)
- [What Are Decorators](#what-are-decorators)
- [Decorator Syntax](#decorator-syntax)
- [Experimental Decorators Flag](#experimental-decorators-flag)
- [Decorator Metadata](#decorator-metadata)
- [Decorator Execution Order](#decorator-execution-order)
- [Decorator Context](#decorator-context)
- [Stage 3 Decorators vs Legacy Decorators](#stage-3-decorators-vs-legacy-decorators)
- [Types of Decorators](#types-of-decorators)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Decorators are a design pattern in TypeScript that allow you to attach metadata or modify the behavior of classes, methods, properties, accessors, or parameters. They use the `@` syntax and are widely used in frameworks like NestJS, Angular, and TypeORM.

---

## What Are Decorators

A decorator is a special kind of declaration that can be attached to a class declaration, method, accessor, property, or parameter. Decorators use the form `@expression`, where `expression` must evaluate to a function that is called at runtime with information about the decorated declaration.

```typescript
// A decorator is fundamentally a function that receives
// information about what it decorates and optionally modifies it

function sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@sealed
class Greeter {
  greeting: string;
  constructor(message: string) {
    this.greeting = message;
  }
  greet() {
    return `Hello, ${this.greeting}`;
  }
}

// Now Greeter and Greeter.prototype are sealed
// Object.defineProperty(Greeter.prototype, 'newMethod', { value: ... }); // Error!
```

---

## Decorator Syntax

### Class Decorator

```typescript
function Log(target: Function) {
  console.log(`Class created: ${target.name}`);
}

@Log
class UserService {
  constructor() {
    console.log('UserService instantiated');
  }
}

// Output when creating instance:
// "Class created: UserService"
// "UserService instantiated"
```

### Method Decorator

```typescript
function LogMethod(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  const originalMethod = descriptor.value;

  descriptor.value = function (...args: any[]) {
    console.log(`Calling ${propertyKey} with args:`, args);
    const result = originalMethod.apply(this, args);
    console.log(`${propertyKey} returned:`, result);
    return result;
  };
}

class Calculator {
  @LogMethod
  add(a: number, b: number): number {
    return a + b;
  }
}

const calc = new Calculator();
calc.add(2, 3);
// Output:
// "Calling add with args: [2, 3]"
// "add returned: 5"
```

### Property Decorator

```typescript
function Required(target: any, propertyKey: string) {
  // MetadataReflect.defineMetadata('required', true, target, propertyKey);
  console.log(`Property ${propertyKey} is marked as required`);
}

class User {
  @Required
  name!: string;

  @Required
  email!: string;

  age?: number; // not required
}
```

### Parameter Decorator

```typescript
function ValidateParam(
  target: any,
  propertyKey: string | undefined,
  parameterIndex: number
) {
  console.log(
    `Parameter ${parameterIndex} of ${propertyKey ?? 'constructor'} is validated`
  );
}

class UserController {
  getUser(
    @ValidateParam id: string,
    @ValidateParam format: string
  ) {
    return { id, format };
  }
}
```

### Accessor Decorator

```typescript
function Enumerable(enumerable: boolean) {
  return function (
    target: any,
    propertyKey: string,
    descriptor: PropertyDescriptor
  ) {
    descriptor.enumerable = enumerable;
  };
}

class Point {
  private _x: number = 0;
  private _y: number = 0;

  @Enumerable(true)
  get x() { return this._x; }
  set x(value: number) { this._x = value; }

  @Enumerable(false)
  get y() { return this._y; }
  set y(value: number) { this._y = value; }
}
```

---

## Experimental Decorators Flag

### Enabling Experimental Decorators

```jsonc
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,  // Legacy decorators (current default)
    "emitDecoratorMetadata": true    // Emit design-time type metadata
  }
}
```

### What `experimentalDecorators` Enables

```typescript
// Without the flag, this is a syntax error in TypeScript
@sealed
class Greeter { }

// With the flag enabled, TypeScript processes decorator functions
// and emits the appropriate JavaScript
```

### Legacy Decorator Signature

```typescript
// Class decorator (legacy)
function sealed(constructor: Function) {
  Object.seal(constructor);
}

// Method decorator (legacy)
function log(
  target: any,            // The prototype of the class
  propertyKey: string,    // The name of the method
  descriptor: PropertyDescriptor // The method's descriptor
) {
  // ...
}

// Property decorator (legacy)
function required(
  target: any,            // The prototype of the class
  propertyKey: string     // The name of the property
) {
  // ...
}

// Parameter decorator (legacy)
function validate(
  target: any,            // The prototype
  propertyKey: string | undefined, // method name (undefined for constructor)
  parameterIndex: number  // parameter position
) {
  // ...
}
```

---

## Decorator Metadata

### emitDecoratorMetadata

```jsonc
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  }
}
```

### What It Emits

```typescript
// Source
class UserService {
  constructor(
    private database: Database,
    private logger: Logger
  ) {}
}

// Compiled JavaScript (with emitDecoratorMetadata):
class UserService {
  constructor(database, logger) {
    this.database = database;
    this.logger = logger;
  }
}

// Metadata is emitted for constructor parameters:
UserService.__metadata("design:paramtypes", [Database, Logger]);
```

### Using Metadata with reflect-metadata

```typescript
import 'reflect-metadata';

function Inject(token: string) {
  return function (target: any, propertyKey: string | undefined, parameterIndex: number) {
    Reflect.defineMetadata('inject:token', token, target, propertyKey ?? 'constructor', parameterIndex);
  );
}

class UserService {
  constructor(
    @Inject('database') private db: Database,
    @Inject('logger') private logger: Logger
  ) {}
}

// At runtime, you can read the metadata:
const tokens = Reflect.getMetadata(
  'design:paramtypes',
  UserService
);
// [Database, Logger]
```

### Metadata Keys

```typescript
// TypeScript emits these design-time metadata keys:
// "design:type"          — the type of a property or method return
// "design:paramtypes"    — the types of constructor/method parameters
// "design:returntype"    — the return type of a method
```

---

## Decorator Execution Order

### Class Decorator Order

```typescript
function A() {
  console.log('A() evaluated');
  return function (target: Function) {
    console.log('A applied');
  };
}

function B() {
  console.log('B() evaluated');
  return function (target: Function) {
    console.log('B applied');
  };
}

@A()
@B()
class MyClass {}

// Output:
// "A() evaluated"     ← factory called top-to-bottom
// "B() evaluated"
// "B applied"         ← decorators applied bottom-to-top
// "A applied"
```

### Member Decorator Order

```typescript
function MethodDec() {
  return function (target: any, key: string, desc: PropertyDescriptor) {
    console.log(`Method decorator applied to ${key}`);
  };
}

function PropDec() {
  return function (target: any, key: string) {
    console.log(`Property decorator applied to ${key}`);
  };
}

class Example {
  @PropDec()
  name!: string;

  @MethodDec()
  greet() {}

  @PropDec()
  age!: number;
}

// Output:
// "Property decorator applied to name"
// "Method decorator applied to greet"
// "Property decorator applied to age"
```

### Complete Execution Order

```
1. Parameter decorators (in order of declaration, right-to-left for constructors)
2. Method / Accessor / Property decorators (in order of declaration)
3. Class decorators (bottom-to-top when stacked)
```

---

## Decorator Context

The decorator context is a new concept in Stage 3 decorators that provides structured information about the decorated element.

```typescript
// Stage 3 decorator context shape:
interface ClassMethodDecoratorContext {
  kind: 'method';
  name: string | symbol;
  static: boolean;
  private: boolean;
  access: { get(): unknown; has(obj: object): boolean };
  addInitializer(initializer: () => void): void;
}

interface ClassFieldDecoratorContext {
  kind: 'field';
  name: string | symbol;
  static: boolean;
  private: boolean;
  access: { get(): unknown; has(obj: object): boolean };
  addInitializer(initializer: () => void): void;
}

interface ClassDecoratorContext {
  kind: 'class';
  name: string | undefined;
  addInitializer(initializer: () => void): void;
}
```

### Using Context in Stage 3 Decorators

```typescript
function logged(
  value: any,
  context: ClassMethodDecoratorContext
) {
  if (context.kind === 'method') {
    const methodName = String(context.name);

    return function (this: any, ...args: any[]) {
      console.log(`Calling ${methodName}`);
      const result = value.call(this, ...args);
      console.log(`${methodName} returned`);
      return result;
    };
  }
}

class Greeter {
  name: string = 'World';

  @logged
  greet() {
    return `Hello, ${this.name}!`;
  }
}
```

---

## Stage 3 Decorators vs Legacy Decorators

### Legacy Decorators (experimentalDecorators: true)

```typescript
// Legacy: decorator receives raw arguments
function LegacyDec(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
  // target is the prototype
  // propertyKey is a string
  // descriptor is the raw PropertyDescriptor
}

// Legacy: class decorator receives the constructor function
function LegacyClassDec(target: Function) {
  // target is the class constructor
}
```

### Stage 3 Decorators (TC39 standard)

```typescript
// Stage 3: decorator receives (value, context)
function Stage3Dec(value: any, context: DecoratorContext) {
  // value is the method/field getter/setter/class
  // context is a structured object with kind, name, etc.
}

// Stage 3: class decorator receives (value, context)
function Stage3ClassDec(value: Function, context: ClassDecoratorContext) {
  // value is the class constructor
  // context.kind === 'class'
}
```

### Key Differences

| Feature | Legacy | Stage 3 |
|---|---|---|
| Flag | `experimentalDecorators: true` | None (default in TS 5.0+) |
| Method decorator args | `(target, key, descriptor)` | `(value, context)` |
| Class decorator args | `(constructor)` | `(constructor, context)` |
| Return value | Modifies descriptor | Replaces value |
| Metadata | `emitDecoratorMetadata` | `context.metadata` |
| `addInitializer` | No | Yes |
| Specification | TypeScript-specific | TC39 standard |

---

## Types of Decorators

```typescript
// 1. Class Decorator
function Component(target: Function) { /* ... */ }

// 2. Method Decorator
function Get(path: string) {
  return function (target: any, key: string, desc: PropertyDescriptor) { /* ... */ };
}

// 3. Property Decorator
function Model(target: any, key: string) { /* ... */ }

// 4. Parameter Decorator
function Body(target: any, key: string | undefined, index: number) { /* ... */ }

// 5. Accessor Decorator
function Throttle(limit: number) {
  return function (target: any, key: string, desc: PropertyDescriptor) { /* ... */ };
}
```

---

## Best Practices

1. **Use Stage 3 decorators for new projects** — they're the TC39 standard and don't require flags.

2. **Use `reflect-metadata` with `emitDecoratorMetadata`** when you need runtime type information (e.g., for DI containers).

3. **Keep decorators small and focused** — each decorator should do one thing.

4. **Document decorator behavior** — decorators modify code implicitly, which can confuse readers.

5. **Use TypeScript 5.0+** for Stage 3 decorator support.

6. **Be aware of execution order** — stacked decorators execute factory functions top-to-bottom but apply bottom-to-top.

7. **Use `addInitializer`** in Stage 3 decorators instead of modifying prototypes.

8. **Test decorator behavior thoroughly** — they're a common source of subtle bugs.

---

## Interview Questions

### Q1: What are TypeScript decorators?

**Answer**: Decorators are functions that can be attached to class declarations, methods, properties, accessors, or parameters using the `@` syntax. They receive metadata about the decorated element and can modify its behavior, add metadata, or completely replace it. They're commonly used for logging, validation, dependency injection, and framework annotations.

### Q2: What is the difference between legacy and Stage 3 decorators?

**Answer**: Legacy decorators (enabled with `experimentalDecorators`) are TypeScript-specific and receive raw arguments like `(target, key, descriptor)`. Stage 3 decorators are the TC39 standard (default in TypeScript 5.0+) and receive `(value, context)` where context is a structured object with properties like `kind`, `name`, and `addInitializer`. Stage 3 is the future; legacy is being phased out.

### Q3: What does `emitDecoratorMetadata` do?

**Answer**: It emits design-time type metadata for decorated classes, methods, and parameters using `Reflect.metadata`. This metadata includes parameter types, return types, and property types. It's essential for dependency injection frameworks like NestJS that need to resolve types at runtime.

### Q4: What is the execution order of multiple decorators?

**Answer**: For stacked decorators (`@A @B @C`), factory functions execute top-to-bottom (A, B, C), but the resulting decorator functions apply bottom-to-top (C, B, A). For mixed member types, parameter decorators run first, then method/accessor/property decorators, then class decorators.

### Q5: Can decorators change the return value of a method?

**Answer**: Yes. Legacy decorators can modify the `descriptor.value` property. Stage 3 decorators can return a new function that replaces the original. Both approaches allow wrapping the original method to add pre/post-processing.
