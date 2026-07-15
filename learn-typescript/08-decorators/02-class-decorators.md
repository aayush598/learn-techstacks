# Class Decorators in TypeScript

## Table of Contents

- [Overview](#overview)
- [Class Decorator Function Signature](#class-decorator-function-signature)
- [Modifying Class Behavior](#modifying-class-behavior)
- [Sealed Classes](#sealed-classes)
- [Registration Pattern](#registration-pattern)
- [Class Decorator with Return Value](#class-decorator-with-return-value)
- [Replacing Class Constructor](#replacing-class-constructor)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Class decorators are applied to class declarations. They receive the class constructor as their argument and can modify, extend, or replace the class. They're the simplest form of decorators but can have the most far-reaching effects on a class.

---

## Class Decorator Function Signature

### Legacy Decorator Signature

```typescript
// Legacy class decorator: receives the constructor function
function MyDecorator(constructor: Function) {
  // constructor is the class itself
  console.log(`Decorating class: ${constructor.name}`);
}

@MyDecorator
class MyClass {
  name: string = 'test';
}
```

### Stage 3 Decorator Signature

```typescript
// Stage 3 class decorator: receives (constructor, context)
function MyDecorator(
  constructor: Function,
  context: ClassDecoratorContext
) {
  // context.kind === 'class'
  // context.name === 'MyClass'
  // context.addInitializer(fn) — runs after class definition
  console.log(`Decorating ${context.name}`);
}

@MyDecorator
class MyClass {
  name: string = 'test';
}
```

### Decorator Factory Signature

```typescript
// Factory that returns a class decorator
function Component(name: string) {
  return function (constructor: Function) {
    constructor.prototype.componentName = name;
    constructor.prototype.version = '1.0.0';
  };
}

@Component('UserService')
class UserService {
  name!: string;
  componentName!: string;
  version!: string;
}

const service = new UserService();
console.log(service.componentName); // 'UserService'
console.log(service.version);       // '1.0.0'
```

---

## Modifying Class Behavior

### Adding Properties and Methods

```typescript
function Timestamped(constructor: Function) {
  constructor.prototype.createdAt = new Date();
  constructor.prototype.getCreatedAt = function () {
    return this.createdAt;
  };
}

@Timestamped
class User {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}

const user = new User('Alice');
console.log(user.createdAt);       // Date object
console.log(user.getCreatedAt());  // Date object
```

### Modifying Prototype Methods

```typescript
function AutoBind(constructor: Function) {
  const methods = Object.getOwnPropertyNames(constructor.prototype)
    .filter((name) => name !== 'constructor');

  for (const method of methods) {
    const descriptor = Object.getOwnPropertyDescriptor(
      constructor.prototype,
      method
    );
    if (descriptor && typeof descriptor.value === 'function') {
      Object.defineProperty(constructor.prototype, method, {
        value: descriptor.value.bind(undefined),
        writable: true,
        configurable: true,
      });
    }
  }
}

@AutoBind
class Calculator {
  value: number = 0;

  add(n: number): Calculator {
    this.value += n;
    return this;
  }
}
```

### Adding Static Members

```typescript
function StaticMethods(constructor: Function) {
  // Add static factory method
  (constructor as any).create = function (name: string) {
    return new constructor(name);
  };
}

@StaticMethods
class Entity {
  constructor(public name: string) {}
}

// Now has a static create method
const entity = (Entity as any).create('test');
```

---

## Sealed Classes

```typescript
function Sealed(constructor: Function) {
  Object.seal(constructor);
  Object.seal(constructor.prototype);
}

@Sealed
class Greeter {
  greeting: string;
  constructor(message: string) {
    this.greeting = message;
  }
  greet() {
    return `Hello, ${this.greeting}`;
  }
}

// Cannot add new properties to Greeter or Greeter.prototype
Object.defineProperty(Greeter.prototype, 'newMethod', {
  value: function () {},
  writable: false,
}); // Error in strict mode
```

### Frozen Classes

```typescript
function Frozen(constructor: Function) {
  Object.freeze(constructor);
  Object.freeze(constructor.prototype);
}

@Frozen
class Config {
  apiUrl: string = 'https://api.example.com';
  timeout: number = 5000;
}

// Config is completely immutable
new Config().apiUrl = 'other'; // Error: Cannot assign to read only property
```

---

## Registration Pattern

### Class Registration for Factory Pattern

```typescript
const classRegistry = new Map<string, Function>();

function Register(name: string) {
  return function (constructor: Function) {
    classRegistry.set(name, constructor);
  };
}

@register('user')
class User {
  constructor(public name: string) {}
}

@register('post')
class Post {
  constructor(public title: string) {}
}

// Factory using registry
function createInstance(name: string, ...args: any[]) {
  const Constructor = classRegistry.get(name);
  if (!Constructor) throw new Error(`Unknown class: ${name}`);
  return new Constructor(...args);
}

const user = createInstance('user', 'Alice') as User;
console.log(user.name); // 'Alice'
```

### Plugin Registration

```typescript
const plugins = new Map<string, any>();

function Plugin(name: string) {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    plugins.set(name, constructor);
    return constructor;
  };
}

@Plugin('logger')
class Logger {
  log(msg: string) { console.log(msg); }
}

@Plugin('cache')
class Cache {
  get(key: string) { return undefined; }
  set(key: string, value: any) {}
}

// List all registered plugins
console.log([...plugins.keys()]); // ['logger', 'cache']
```

---

## Class Decorator with Return Value

### Returning a Modified Constructor

```typescript
// Legacy: return a new constructor to replace the original
function Extended(baseConstructor: Function) {
  return class extends baseConstructor {
    extendedProperty = 'I was added by decorator';

    extendedMethod() {
      return 'I was added by decorator';
    }
  };
}

@Extended
class Original {
  originalProperty = 'I was original';
}

const instance = new Original() as Original & {
  extendedProperty: string;
  extendedMethod: () => string;
};

console.log(instance.originalProperty);   // 'I was original'
console.log(instance.extendedProperty);   // 'I was added by decorator'
console.log(instance.extendedMethod());   // 'I was added by decorator'
```

### Returning a Completely New Class

```typescript
function withTimestamp<T extends new (...args: any[]) => any>(constructor: T) {
  return class extends constructor {
    _createdAt: Date;
    _updatedAt: Date;

    constructor(...args: any[]) {
      super(...args);
      this._createdAt = new Date();
      this._updatedAt = new Date();
    }

    getTimestamp() {
      return {
        created: this._createdAt,
        updated: this._updatedAt,
      };
    }
  };
}

@withTimestamp
class Document {
  constructor(public title: string, public content: string) {}
}

const doc = new Document('Hello', 'World');
console.log(doc.getTimestamp()); // { created: Date, updated: Date }
```

---

## Replacing Class Constructor

### Complete Constructor Replacement (Stage 3)

```typescript
function replaceConstructor(
  value: Function,
  context: ClassDecoratorContext
) {
  if (context.kind === 'class') {
    // Return a new class to completely replace the original
    return class extends value {
      constructor(...args: any[]) {
        super(...args);
        console.log('Constructor replaced!');
      }
    };
  }
}

@replaceConstructor
class MyClass {
  constructor() {
    console.log('Original constructor');
  }
}

// new MyClass() →
// "Constructor replaced!"
// "Original constructor"
```

### Conditional Constructor Modification

```typescript
function conditional<T extends new (...args: any[]) => any>(
  condition: boolean
) {
  return function (constructor: T) {
    if (condition) {
      return class extends constructor {
        constructor(...args: any[]) {
          super(...args);
          console.log('Additional behavior added');
        }
      };
    }
    return constructor; // return original if condition is false
  };
}

@conditional(process.env.NODE_ENV === 'development')
class ApiService {
  constructor() {
    console.log('API Service initialized');
  }
}
```

---

## Real-World Examples

### Component Registration

```typescript
function Component(name: string, version: string = '1.0') {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    return class extends constructor {
      static componentName = name;
      static componentVersion = version;

      getComponentInfo() {
        return `${name}@${version}`;
      }
    };
  };
}

@Component('Button', '2.1.0')
class Button {
  constructor(public label: string) {}
}

const btn = new Button('Click me');
console.log(btn.getComponentInfo()); // 'Button@2.1.0'
```

### Serialization Decorator

```typescript
function Serializable(constructor: Function) {
  constructor.prototype.serialize = function () {
    const obj: Record<string, any> = {};
    for (const key of Object.keys(this)) {
      obj[key] = this[key];
    }
    return JSON.stringify(obj);
  };

  constructor.prototype.deserialize = function (json: string) {
    const obj = JSON.parse(json);
    for (const key of Object.keys(obj)) {
      this[key] = obj[key];
    }
    return this;
  };
}

@Serializable
class User {
  constructor(
    public name: string,
    public email: string
  ) {}
}

const user = new User('Alice', 'alice@example.com');
const json = user.serialize();
console.log(json); // '{"name":"Alice","email":"alice@example.com"}'
```

---

## Best Practices

1. **Use decorator factories** instead of bare decorators for configurable behavior.

2. **Be careful with return values** — returning a new class changes the class identity (`instanceof` checks may fail).

3. **Document side effects** — class decorators can modify the class prototype, which affects all instances.

4. **Prefer Stage 3 pattern** for new code — use `context.addInitializer()` instead of modifying the constructor.

5. **Don't stack too many class decorators** — they become hard to debug.

6. **Test `instanceof` behavior** after decorator returns a new class.

---

## Interview Questions

### Q1: What arguments does a class decorator receive?

**Answer**: Legacy: a single `constructor: Function` argument. Stage 3: `(constructor: Function, context: ClassDecoratorContext)` where context has `kind`, `name`, and `addInitializer`. The decorator can modify the constructor directly or return a new constructor to replace it.

### Q2: Can a class decorator prevent instantiation?

**Answer**: Yes. The decorator can throw an error in the constructor or replace the constructor with one that throws:

```typescript
function PreventInstantiation(constructor: Function) {
  return class {
    constructor() {
      throw new Error(`Cannot instantiate ${constructor.name}`);
    }
  };
}
```

### Q3: What happens if a class decorator returns a value?

**Answer**: If a class decorator returns a function (constructor), that function replaces the original class. This is useful for extending classes, but it changes the class identity — `instanceof` checks against the original class will fail if the returned class doesn't properly extend it.
