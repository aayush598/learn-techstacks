# Property Decorators in TypeScript

## Table of Contents

- [Overview](#overview)
- [Property Decorator Signature](#property-decorator-signature)
- [Property Initialization](#property-initialization)
- [Validation Decorators](#validation-decorators)
- [Observable Pattern](#observable-pattern)
- [Property Decorator vs Method Decorator](#property-decorator-vs-method-decorator)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)
- [Interview Questions](#interview-questions)

---

## Overview

Property decorators are applied to property declarations in a class. Unlike method decorators, they don't receive a property descriptor — they only receive the prototype and property name. Property decorators are commonly used for validation, serialization, ORM mappings, and reactive patterns.

---

## Property Decorator Signature

### Legacy Signature

```typescript
function MyPropertyDecorator(
  target: any,            // The prototype of the class (for instance properties)
                          // The constructor function (for static properties)
  propertyKey: string     // The name of the property
) {
  // Note: no descriptor — you can't observe the property value
}
```

### Stage 3 Signature

```typescript
function MyPropertyDecorator(
  value: any,             // undefined for instance fields (value not yet assigned)
  context: ClassFieldDecoratorContext
  // context.kind === 'field'
  // context.name === propertyKey
  // context.static === boolean
  // context.access === { get(), has() }
  // context.addInitializer(fn) — runs during instance construction
) {
  // Return undefined to keep original behavior, or return a new initializer
}
```

### Basic Example

```typescript
function LogProperty(
  target: any,
  propertyKey: string
) {
  console.log(
    `Property decorator applied to ${propertyKey} on ${target.constructor.name}`
  );
}

class User {
  @LogProperty
  name!: string;

  @LogProperty
  email!: string;

  age!: number; // no decorator
}

// Output:
// "Property decorator applied to name on User"
// "Property decorator applied to email on User"
```

---

## Property Initialization

### Stage 3 Property Initializer

```typescript
// In Stage 3, a property decorator can return an initializer function
function initializeValue(defaultValue: string) {
  return function (value: any, context: ClassFieldDecoratorContext) {
    // Return an initializer that sets the default value
    return function (initialValue: any) {
      return initialValue ?? defaultValue;
    };
  };
}

class User {
  @initializeValue('Anonymous')
  name!: string;

  @initializeValue('no-email@example.com')
  email!: string;
}

const user = new User();
console.log(user.name);  // 'Anonymous' (if not set in constructor)
```

### Legacy Property Initializer Workaround

```typescript
// In legacy decorators, you can't directly initialize properties
// But you can use a class decorator pattern:

function WithDefaults(defaults: Record<string, any>) {
  return function <T extends new (...args: any[]) => any>(constructor: T) {
    return class extends constructor {
      constructor(...args: any[]) {
        super(...args);
        // Apply defaults for any undefined properties
        for (const [key, value] of Object.entries(defaults)) {
          if ((this as any)[key] === undefined) {
            (this as any)[key] = value;
          }
        }
      }
    };
  };
}

@WithDefaults({ name: 'Anonymous', email: 'no-email@example.com' })
class User {
  name!: string;
  email!: string;
}
```

---

## Validation Decorators

### Required Field Validation

```typescript
const requiredFields = new Map<string, string[]>();

function Required(message?: string) {
  return function (target: any, propertyKey: string) {
    const className = target.constructor.name;
    const existing = requiredFields.get(className) || [];
    existing.push(propertyKey);
    requiredFields.set(className, existing);

    // Store validation message
    Reflect.defineMetadata(
      `validation:${propertyKey}`,
      message ?? `${propertyKey} is required`,
      target,
      propertyKey
    );
  };
}

function validate(instance: any): string[] {
  const className = instance.constructor.name;
  const fields = requiredFields.get(className) || [];
  const errors: string[] = [];

  for (const field of fields) {
    const value = instance[field];
    if (value === undefined || value === null || value === '') {
      const message = Reflect.getMetadata(
        `validation:${field}`,
        instance,
        field
      );
      errors.push(message);
    }
  }

  return errors;
}

class CreateUserDto {
  @Required('Name is required')
  name!: string;

  @Required('Email is required')
  email!: string;

  age?: number; // not required
}

const dto = new CreateUserDto();
dto.name = '';
dto.email = '';

const errors = validate(dto);
console.log(errors); // ['Name is required', 'Email is required']
```

### Type Validation

```typescript
function IsType(expectedType: 'string' | 'number' | 'boolean') {
  return function (target: any, propertyKey: string) {
    Reflect.defineMetadata('validation:type', expectedType, target, propertyKey);
  };
}

class Config {
  @IsType('string')
  apiUrl!: string;

  @IsType('number')
  timeout!: number;

  @IsType('boolean')
  debug!: boolean;
}

function validateTypes(instance: any): string[] {
  const errors: string[] = [];
  const keys = Object.keys(instance);

  for (const key of keys) {
    const expectedType = Reflect.getMetadata('validation:type', instance, key);
    if (expectedType && typeof instance[key] !== expectedType) {
      errors.push(
        `${key} should be ${expectedType}, got ${typeof instance[key]}`
      );
    }
  }

  return errors;
}
```

---

## Observable Pattern

### React-Style State Management

```typescript
type Observer<T> = (value: T, oldValue: T) => void;

function Observable<T>(
  target: any,
  propertyKey: string
) {
  let value: T;
  const observers = new Map<string, Observer<any>[]>();

  const getter = function () {
    return value;
  };

  const setter = function (newValue: T) {
    const oldValue = value;
    value = newValue;

    const propertyObservers = observers.get(propertyKey) || [];
    for (const observer of propertyObservers) {
      observer(newValue, oldValue);
    }
  };

  Object.defineProperty(target, propertyKey, {
    get: getter,
    set: setter,
    enumerable: true,
    configurable: true,
  });

  // Add subscribe method
  if (!target.addObserver) {
    target.addObserver = function (
      prop: string,
      observer: Observer<any>
    ) {
      const list = observers.get(prop) || [];
      list.push(observer);
      observers.set(prop, list);
    };
  }
}

class TodoStore {
  @Observable
  todos: string[] = [];

  @Observable
  filter: string = 'all';
}

const store = new TodoStore();
store.addObserver('todos', (newVal, oldVal) => {
  console.log(`Todos changed from ${oldVal} to ${newVal}`);
});

store.todos = ['Learn TypeScript']; // Logs the change
store.todos = ['Learn TypeScript', 'Learn Decorators']; // Logs the change
```

### Property Change Tracker

```typescript
function TrackChanges(
  target: any,
  propertyKey: string
) {
  const changesKey = `__changes_${propertyKey}`;
  const historyKey = `__history_${propertyKey}`;

  // Initialize change tracking
  Object.defineProperty(target, historyKey, {
    value: [],
    writable: true,
    enumerable: false,
  });

  Object.defineProperty(target, changesKey, {
    value: false,
    writable: true,
    enumerable: false,
  });

  // Define getter/setter for change tracking
  const descriptor = Object.getOwnPropertyDescriptor(target, propertyKey) || {
    value: undefined,
    writable: true,
  };

  let currentValue = descriptor.value;

  Object.defineProperty(target, propertyKey, {
    get() {
      return currentValue;
    },
    set(newValue) {
      const oldValue = currentValue;
      currentValue = newValue;

      if (oldValue !== newValue) {
        (target as any)[historyKey].push({
          from: oldValue,
          to: newValue,
          timestamp: new Date(),
        });
        (target as any)[changesKey] = true;
      }
    },
    enumerable: true,
    configurable: true,
  });

  // Add methods to check changes
  if (!target.hasChanges) {
    target.hasChanges = function () {
      return (target as any)[changesKey];
    };
    target.getHistory = function (prop: string) {
      return (target as any)[`__history_${prop}`] || [];
    };
  }
}

class Document {
  @TrackChanges
  title!: string;

  @TrackChanges
  content!: string;
}
```

---

## Property Decorator vs Method Decorator

| Feature | Property Decorator | Method Decorator |
|---|---|---|
| Target | Property declaration | Method declaration |
| Receives descriptor | No | Yes |
| Can modify behavior | Limited (defineProperty) | Yes (replace value) |
| Access to arguments | No (no function) | Yes |
| Common uses | Validation, ORM, serialization | Logging, caching, timing |
| Stage 3 return | Initializer function | Replacement function |

```typescript
// Property decorator: can't observe calls, only the declaration
function PropDec(target: any, key: string) {
  // We know a property named `key` exists on the prototype
  // We CAN modify how it's stored/accessed via defineProperty
  // We CANNOT intercept individual reads/writes without defineProperty
}

// Method decorator: can intercept every call
function MethodDec(target: any, key: string, desc: PropertyDescriptor) {
  // We have the actual function in desc.value
  // We can wrap it to intercept calls
}
```

---

## Real-World Examples

### ORM Column Mapping

```typescript
const columnMetadata = new Map<string, Map<string, string>>();

function Column(columnName: string) {
  return function (target: any, propertyKey: string) {
    const className = target.constructor.name;
    if (!columnMetadata.has(className)) {
      columnMetadata.set(className, new Map());
    }
    columnMetadata.get(className)!.set(propertyKey, columnName);
  };
}

class User {
  @Column('user_id')
  id!: number;

  @Column('user_name')
  name!: string;

  @Column('user_email')
  email!: string;
}

function getColumns(instance: any): Record<string, string> {
  const className = instance.constructor.name;
  const meta = columnMetadata.get(className);
  if (!meta) return {};

  const columns: Record<string, string> = {};
  for (const [prop, col] of meta) {
    columns[col] = instance[prop];
  }
  return columns;
}

const user = new User();
user.id = 1;
user.name = 'Alice';
user.email = 'alice@example.com';

console.log(getColumns(user));
// { user_id: 1, user_name: 'Alice', user_email: 'alice@example.com' }
```

### URL Parameter Binding

```typescript
function FromQuery(target: any, propertyKey: string) {
  Reflect.defineMetadata('binding:query', propertyKey, target, propertyKey);
}

function FromBody(target: any, propertyKey: string) {
  Reflect.defineMetadata('binding:body', propertyKey, target, propertyKey);
}

class GetUserDto {
  @FromQuery
  userId!: string;

  @FromQuery
  format!: string;

  @FromBody
  preferences!: Record<string, any>;
}
```

### Auto-Generated Getter/Setter

```typescript
function AutoGetSet(
  target: any,
  propertyKey: string
) {
  const backingField = `_${propertyKey}`;

  Object.defineProperty(target, backingField, {
    value: undefined,
    writable: true,
    enumerable: false,
    configurable: true,
  });

  Object.defineProperty(target, propertyKey, {
    get() {
      return (this as any)[backingField];
    },
    set(value) {
      (this as any)[backingField] = value;
      console.log(`${propertyKey} set to ${JSON.stringify(value)}`);
    },
    enumerable: true,
    configurable: true,
  });
}

class Settings {
  @AutoGetSet
  theme!: string;

  @AutoGetSet
  language!: string;
}

const settings = new Settings();
settings.theme = 'dark'; // "theme set to dark"
settings.language = 'en'; // "language set to en"
```

---

## Best Practices

1. **Use property decorators for metadata** — validation rules, ORM mappings, serialization hints.

2. **Use `Reflect.defineMetadata`** to store property-level metadata for runtime access.

3. **Be aware that property decorators don't receive descriptors** — use `Object.defineProperty` if you need to intercept reads/writes.

4. **For reactive patterns**, use Stage 3's `addInitializer` or define getters/setters.

5. **Combine with method decorators** — property decorator marks the property, method decorator does the validation.

---

## Interview Questions

### Q1: Why don't property decorators receive a descriptor?

**Answer**: In TypeScript's design, property decorators only identify which property is being decorated — they don't have access to the property's value or how it's accessed. The property hasn't been initialized yet (class fields are set in the constructor). You can use `Object.defineProperty` in the decorator to intercept future reads/writes.

### Q2: How do you validate properties with decorators?

**Answer**: Use `Reflect.defineMetadata` to attach validation rules to properties during decoration, then write a validation function that reads the metadata at runtime and checks the actual values on the instance.

### Q3: Can a property decorator change a property's default value?

**Answer**: In Stage 3 decorators, yes — return an initializer function from the decorator. In legacy decorators, you need to use a class decorator or `Object.defineProperty` to intercept and set the value, since legacy property decorators don't have a natural hook into initialization.
