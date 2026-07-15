# Decorators — Interview Questions

## Overview

This document contains 25+ interview questions covering TypeScript decorators: basics, class decorators, method decorators, property decorators, parameter decorators, decorator factories, and NestJS decorators.

---

## Questions

### Q1: What are TypeScript decorators?

**Answer**: Decorators are functions that can be attached to class declarations, methods, properties, accessors, or parameters using the `@` syntax. They receive metadata about the decorated element and can modify its behavior, add metadata, or replace it entirely. They're widely used for logging, validation, dependency injection, and framework annotations.

---

### Q2: What is the difference between legacy and Stage 3 decorators?

**Answer**: Legacy decorators (`experimentalDecorators: true`) are TypeScript-specific and receive raw arguments: `(target, key, descriptor)` for methods, `(constructor)` for classes. Stage 3 decorators (TC39 standard, default in TS 5.0+) receive `(value, context)` where context is a structured object with `kind`, `name`, and `addInitializer()`. Stage 3 is the future; legacy is being phased out.

---

### Q3: How do you enable decorators in TypeScript?

**Answer**: For legacy decorators, set `"experimentalDecorators": true` in tsconfig. For Stage 3 decorators, no flag is needed (they're enabled by default in TypeScript 5.0+). If you need runtime type metadata, also set `"emitDecoratorMetadata": true` and install `reflect-metadata`.

---

### Q4: What is the execution order of decorators?

**Answer**: Factory functions execute top-to-bottom. Decorator application executes bottom-to-top (for stacked class decorators). For mixed member types: parameter decorators first (right-to-left for constructors), then method/accessor/property decorators (in declaration order), then class decorators (bottom-to-top).

---

### Q5: Can a class decorator prevent instantiation?

**Answer**: Yes. The decorator can replace the constructor with one that throws an error, or modify the prototype to prevent `new`. Example:
```typescript
function PreventInstantiation(constructor: Function) {
  return class { constructor() { throw new Error(`Cannot instantiate ${constructor.name}`); } };
}
```

---

### Q6: What is the purpose of `emitDecoratorMetadata`?

**Answer**: It emits design-time type metadata for decorated classes, methods, and parameters. This metadata includes parameter types (`design:paramtypes`), return types (`design:returntype`), and property types (`design:type`). Essential for DI frameworks like NestJS that need to resolve types at runtime without explicit tokens.

---

### Q7: How do you create a method decorator that logs calls?

**Answer**: Save the original method from `descriptor.value`, replace it with a wrapper that logs arguments and return value, then calls the original with `apply(this, args)` to preserve `this` context. The wrapper can add timing, error handling, and conditional logging.

---

### Q8: Can property decorators modify property values?

**Answer**: In legacy decorators, they can use `Object.defineProperty` to intercept reads/writes but can't observe the initial value. In Stage 3, they can return an initializer function that sets a default value. Neither can directly read the value at decoration time since class fields are initialized in the constructor.

---

### Q9: What is a decorator factory?

**Answer**: A decorator factory is a function that returns a decorator. It allows passing configuration: `@Decorator(options)` calls the factory with options, which returns the actual decorator. This enables configurable, reusable decorators — the factory captures options in a closure.

---

### Q10: How does `@Inject()` work in NestJS?

**Answer**: It stores metadata about which token to inject for a specific constructor parameter using `Reflect.defineMetadata`. At runtime, NestJS reads this metadata and resolves the token from the IoC container. Without `@Inject()`, NestJS uses the parameter's TypeScript type for automatic resolution.

---

### Q11: What is module augmentation with decorators?

**Answer**: Module augmentation uses `declare module` to extend existing module types. Combined with decorators, you can add new properties to third-party interfaces (like Express's `Request`) or extend library types. The `declare module 'express'` block adds type declarations that merge with the original module.

---

### Q12: Can you use decorators on arrow functions or anonymous classes?

**Answer**: Stage 3 decorators support anonymous classes (`const MyClass = class { }` decorated inline). Legacy decorators require named class declarations. Neither supports arrow functions or plain functions — decorators only work on class-related declarations.

---

### Q13: How do you make a method decorator work with async methods?

**Answer**: Make the wrapper function `async` and `await` the original method's result:
```typescript
descriptor.value = async function(...args) {
  console.log('before');
  const result = await originalMethod.apply(this, args);
  console.log('after');
  return result;
};
```
Always use `async/await` instead of `.then()` for cleaner error handling.

---

### Q14: What is the `addInitializer` method in Stage 3 decorators?

**Answer**: `context.addInitializer(fn)` registers a function that runs during class definition or instance construction. For class decorators, it runs after the class is fully defined. For field decorators, it runs during instance construction (after `super()`). It replaces the pattern of modifying the constructor in legacy decorators.

---

### Q15: How do decorators interact with inheritance?

**Answer**: Decorators applied to a parent class are NOT inherited by child classes. Method decorators on parent methods ARE visible to children (since methods are on the prototype). Property decorators apply per-class, not per-instance. Returning a new class from a decorator breaks `instanceof` unless it properly extends the original.

---

### Q16: What is `Reflect.metadata` and how does it relate to decorators?

**Answer**: `Reflect.metadata(key, value)` creates a metadata decorator that stores key-value pairs on targets. It's emitted by `emitDecoratorMetadata` for design-time types. In decorators, you use `Reflect.defineMetadata()` to store custom data and `Reflect.getMetadata()` to retrieve it. It's the standard way decorators communicate metadata.

---

### Q17: Can you apply the same decorator multiple times?

**Answer**: Yes. Each application creates a separate invocation. For method decorators, each wrapper wraps the previous result. For property decorators, each stores metadata (later ones may overwrite). For class decorators, each modifies the constructor. Be careful with ordering — multiple applications can cause unexpected behavior.

---

### Q18: How do you test code that uses decorators?

**Answer**: Test the decorated behavior, not the decorator itself in isolation. Create instances of decorated classes and verify the expected behavior. For metadata-based decorators, test that metadata is stored correctly using `Reflect.getMetadata()`. Use dependency injection to mock services that decorators interact with.

---

### Q19: What are the performance implications of decorators?

**Answer**: Decorators add minimal runtime overhead — they run once during class definition (not per instance). The main cost is in method decorators that wrap calls (extra function call per invocation). Metadata storage uses memory. In hot paths, the wrapper function overhead can be measurable. Profile before optimizing.

---

### Q20: How do you combine multiple decorators on the same target?

**Answer**: Stack them vertically: `@A @B @C method()`. Or compose them in a single decorator that applies multiple concerns. For repeated use, create a "meta-decorator" factory that combines several decorations. NestJS uses `@UseGuards()`, `@UseInterceptors()` which accept arrays of decorators.

---

### Q21: What happens if a decorator throws an error?

**Answer**: In legacy decorators, a thrown error during decoration prevents the class/method from being defined — it results in a runtime error. In Stage 3, errors in `addInitializer` functions throw during class instantiation. Errors in the decorator function itself (not in the wrapped method) prevent the class from being available.

---

### Q22: How do you use decorators for dependency injection without a framework?

**Answer**: Create a simple IoC container that uses `Reflect.getMetadata('design:paramtypes', ...)` to resolve constructor parameters. Register implementations with `container.register(Token, Implementation)`. Use a `@Inject(Token)` decorator to specify tokens. The container creates instances by resolving each parameter.

---

### Q23: What is the relationship between decorators and Symbol.metadata?

**Answer**: Stage 3 decorators use `Symbol.metadata` as the key for storing metadata on classes. `context.metadata` is an object attached to the class via `Symbol.metadata`. All decorators can contribute to this shared metadata object, which is accessible as `MyClass[Symbol.metadata]`.

---

### Q24: Can decorators modify a class's constructor behavior?

**Answer**: Yes. Class decorators can: (1) seal/freeze the class, (2) add properties to the prototype, (3) replace the constructor by returning a new class that extends it, (4) use `addInitializer` (Stage 3) to run code during construction. The key is that the decorator receives the constructor function and can modify or wrap it.

---

### Q25: How does NestJS's `@SetMetadata` work with guards?

**Answer**: `@SetMetadata(key, value)` stores metadata on the handler/class using `Reflect.defineMetadata`. A guard reads this metadata with `this.reflector.getAllAndOverride(key, [context.getHandler(), context.getClass()])`. This allows guards to make decisions based on metadata attached via decorators, enabling declarative authorization.

---

### Q26: What is the difference between `@UseGuards` and `@UseInterceptors`?

**Answer**: `@UseGuards` wraps the handler in a guard that returns `boolean` — if false, the request is rejected (403). `@UseInterceptors` wraps the handler in an interceptor that can observe/transform the request and response (logging, caching, transformation). Guards are for authorization; interceptors are for cross-cutting concerns.

---

### Q27: When should you avoid using decorators?

**Answer**: Avoid decorators when: (1) the same effect can be achieved with clearer, explicit code, (2) the team isn't familiar with the decorator pattern, (3) debugging needs to be straightforward (decorators add implicit behavior), (4) the project uses a framework that doesn't support them, or (5) performance in hot paths is critical.
