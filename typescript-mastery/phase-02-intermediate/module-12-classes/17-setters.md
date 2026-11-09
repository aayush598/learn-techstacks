# Setters

> Phase 2 · Module 12 · Classes

**TL;DR** — Setters intercept assignment to a property, letting you validate or transform incoming values.

## Syntax
```ts
class C {
  set name(value: Type) {
    // validate or transform
  }
}
```

## Examples
### Basic
```ts
class Person {
  private _name = "";

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    this._name = value.trim();
  }
}

const p = new Person();
p.name = "  Ada  ";
console.log(p.name); // Ada
```

### Practical
```ts
class Account {
  private _email = "";

  get email(): string {
    return this._email;
  }

  set email(value: string) {
    const trimmed = value.trim();
    if (!trimmed.includes("@")) {
      throw new Error("Invalid email address");
    }
    this._email = trimmed;
  }
}

const account = new Account();
account.email = "ada@example.com";
console.log(account.email); // ada@example.com
// ❌ runtime error: account.email = "not-an-email";
```

### Advanced / edge cases
```ts
class Flag {
  private _value: boolean | string = false;

  get value(): boolean {
    return this._value === true;
  }

  set value(input: boolean | string) {
    this._value = input === "true" ? true : input;
  }
}

const flag = new Flag();
flag.value = "true";
console.log(flag.value); // true

class Range {
  private _value = 0;

  get value(): number {
    return this._value;
  }

  set value(next: number) {
    this._value = Math.min(Math.max(next, 0), 100);
  }
}

const range = new Range();
range.value = 150;
console.log(range.value); // 100
```

## Key points
- Setters take exactly one parameter and return nothing.
- Getter and setter types must be compatible; since TS 4.3 they may differ.
- A setter can validate, clamp, or normalize before storing.
- Setters are invoked by ordinary assignment syntax.
- Accessors are defined on the prototype.

## Gotchas
- Throwing in a setter makes assignment fail at runtime.
- A setter that silently ignores invalid input hides bugs; prefer throwing or clamping intentionally.
- Defining only a setter makes the property unreadable in a useful way.

## Best practice
- Pair setters with getters backed by a clearly named private field.
- Validate invariants in the setter so the object never enters an invalid state.
