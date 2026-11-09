# Abstract methods

> Phase 2 · Module 12 · Classes

**TL;DR** — Abstract methods declare a signature every concrete subclass must implement, enabling template-method designs.

## Syntax
```ts
abstract class Base {
  abstract method(args): ReturnType;
}
```

## Examples
### Basic
```ts
abstract class Logger {
  abstract log(message: string): void;

  info(message: string): void {
    this.log(`INFO ${message}`);
  }

  error(message: string): void {
    this.log(`ERROR ${message}`);
  }
}

class ConsoleLogger extends Logger {
  log(message: string): void {
    console.log(message);
  }
}

new ConsoleLogger().info("started"); // INFO started
```

### Practical
```ts
abstract class DataImporter {
  async run(source: string): Promise<void> {
    const rows = await this.parse(source);
    this.validate(rows);
    await this.save(rows);
  }

  protected abstract parse(source: string): Promise<string[]>;
  protected abstract validate(rows: string[]): void;
  protected abstract save(rows: string[]): Promise<void>;
}

class CsvImporter extends DataImporter {
  protected async parse(source: string): Promise<string[]> {
    return source.split("\n").filter(Boolean);
  }

  protected validate(rows: string[]): void {
    if (rows.length === 0) throw new Error("No rows");
  }

  protected async save(rows: string[]): Promise<void> {
    console.log(`Saved ${rows.length} rows`);
  }
}
```

### Advanced / edge cases
```ts
abstract class Formatter {
  abstract format(value: string): string;
  abstract format(value: number): string;
}

class JsonFormatter extends Formatter {
  format(value: string | number): string {
    return JSON.stringify(value); // ✅ implements both overloads
  }
}

abstract class Broken {
  // ❌ Error: Method 'run' cannot have an implementation because
  // it is marked abstract.
  // abstract run(): void {}
}

class NotAbstract {
  // ❌ Error: Abstract methods can only appear within an abstract class.
  // abstract stop(): void;
}
```

## Key points
- Abstract methods have no implementation and end with a semicolon.
- Subclasses must implement every abstract method unless they are abstract too.
- Abstract methods can be protected, generic, and overloaded.
- Calls from concrete base methods dispatch to the subclass implementation.
- Abstract methods can be called before subclass fields initialize if invoked from the base constructor.

## Gotchas
- Abstract methods cannot have a body.
- Calling an overridden abstract method from a base constructor can observe uninitialized subclass fields.
- Abstract methods are erased at runtime; there is no built-in runtime check.

## Best practice
- Use protected abstract methods for template-method hooks.
- Keep abstract method signatures minimal so subclasses stay easy to implement.
