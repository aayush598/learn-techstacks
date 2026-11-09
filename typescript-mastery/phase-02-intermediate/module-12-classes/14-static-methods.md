# Static methods

> Phase 2 · Module 12 · Classes

**TL;DR** — Static methods live on the constructor and are used for factories, parsing, and class-level utilities.

## Syntax
```ts
class C {
  static method(args): ReturnType {
    // no instance `this`
  }
}
```

## Examples
### Basic
```ts
class MathUtil {
  static clamp(value: number, min: number, max: number): number {
    return Math.min(Math.max(value, min), max);
  }
}

console.log(MathUtil.clamp(15, 0, 10)); // 10
```

### Practical
```ts
class User {
  private constructor(readonly name: string) {}

  static fromJSON(json: string): User {
    const data = JSON.parse(json) as { name?: unknown };
    if (typeof data.name !== "string") {
      throw new Error("Invalid user payload");
    }
    return new User(data.name);
  }

  static anonymous(): User {
    return new User("anonymous");
  }
}

const user = User.fromJSON('{"name":"Ada"}');
console.log(user.name); // Ada
console.log(User.anonymous().name); // anonymous
```

### Advanced / edge cases
```ts
class BaseModel {
  static create<T extends BaseModel>(this: new () => T): T {
    return new this();
  }
}

class UserModel extends BaseModel {
  name = "anonymous";
}

const model = UserModel.create(); // UserModel
console.log(model.name); // anonymous

class Config {
  // ❌ Error: 'static' members cannot reference class type parameters.
  // static empty<T>(): T[] { return []; }

  static empty<T>(): T[] {
    return []; // ✅ generic on the method itself
  }
}
```

## Key points
- Static methods are invoked on the class, not on instances.
- They cannot access instance properties through `this` unless passed an instance.
- A `this` parameter can type the constructor for polymorphic factories.
- Static methods can be generic independently of the class.
- Static methods are inherited by subclasses.

## Gotchas
- Static methods do not participate in instance method overriding.
- Abstract static methods are not supported.
- Using `this` in a static method refers to the constructor and can be a subclass.

## Best practice
- Use static factories to enforce validation and keep constructors private.
- Keep static utilities stateless and free of hidden shared state.
