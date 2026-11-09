# Access modifiers

> Phase 2 · Module 12 · Classes

**TL;DR** — `public`, `private`, and `protected` control compile-time visibility of class members, not runtime access.

## Syntax
```ts
class C {
  public a = 1;
  private b = 2;
  protected c = 3;
}
```

## Examples
### Basic
```ts
class Base {
  public visible = "yes";
  private secret = "no";
  protected shared = "subclasses";

  describe(): string {
    return `${this.visible} ${this.secret} ${this.shared}`;
  }
}

const b = new Base();
console.log(b.visible); // yes
// ❌ Error: Property 'secret' is private and only accessible within class 'Base'.
// b.secret;
```

### Practical
```ts
class BankAccount {
  private balance = 0;

  public deposit(amount: number): void {
    if (amount <= 0) throw new Error("Positive amounts only");
    this.balance += amount;
  }

  public withdraw(amount: number): void {
    if (amount > this.balance) throw new Error("Insufficient funds");
    this.balance -= amount;
  }

  public getBalance(): number {
    return this.balance;
  }
}

const account = new BankAccount();
account.deposit(100);
account.withdraw(30);
console.log(account.getBalance()); // 70
```

### Advanced / edge cases
```ts
class Secretive {
  private token = "abc";
  protected scope = "internal";
}

const s = new Secretive();
console.log(Object.keys(s)); // ["token", "scope"] — still present at runtime
console.log((s as unknown as { token: string }).token); // "abc" — unsafe bypass

class Child extends Secretive {
  readScope(): string {
    return this.scope; // ✅ protected accessible in subclass
  }
}
```

## Key points
- `public` is the default and allows access anywhere.
- `private` restricts access to the declaring class body.
- `protected` allows access in the declaring class and subclasses.
- Modifiers are erased at runtime and are purely compile-time checks.
- Members are public unless explicitly marked otherwise.

## Gotchas
- TypeScript `private` does not prevent runtime access via casts or index access.
- `private` and `protected` members make class compatibility nominal, not structural.
- Access modifiers cannot reduce visibility when overriding a base member.

## Best practice
- Default to the most restrictive visibility that still works.
- Expose behavior through public methods instead of public mutable fields.
