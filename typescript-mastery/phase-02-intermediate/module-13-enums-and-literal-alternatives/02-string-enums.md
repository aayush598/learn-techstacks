# String Enums

> Phase 2 · Module 13 · Enums and Literal-Based Alternatives

**TL;DR** — String enums give every member a readable string value, serialize cleanly, and emit no reverse mapping.

## Syntax
```ts
enum LogLevel {
  Debug = "DEBUG",
  Info = "INFO",
  Error = "ERROR",
}
```

## Examples
### Basic
```ts
enum LogLevel {
  Debug = "DEBUG",
  Info = "INFO",
  Error = "ERROR",
}

console.log(LogLevel.Debug);        // "DEBUG"
console.log(LogLevel["Error"]);     // "ERROR"
console.log((LogLevel as any)[0]);  // undefined — no reverse map
```

### Practical
```ts
enum OrderState {
  Pending = "pending",
  Paid = "paid",
  Shipped = "shipped",
  Cancelled = "cancelled",
}

type Order = { id: string; state: OrderState };

function canCancel(order: Order): boolean {
  return order.state === OrderState.Pending || order.state === OrderState.Paid;
}

const order: Order = { id: "o-1", state: OrderState.Paid };
console.log(JSON.stringify(order)); // {"id":"o-1","state":"paid"} ✅
```

### Advanced / edge cases
```ts
enum LogLevel {
  Debug = "DEBUG",
  Info = "INFO",
}

type LogLevelName = keyof typeof LogLevel;      // "Debug" | "Info"
type LogLevelValue = `${LogLevel}`;             // "DEBUG" | "INFO"
type ApiPath = `/api/logs/${LogLevel}`;         // "/api/logs/DEBUG" | ...

const names = Object.keys(LogLevel);            // ["Debug", "Info"]
const values = Object.values(LogLevel);         // ["DEBUG", "INFO"]

// Look up a member name from an external string value.
function nameOf(value: LogLevelValue): LogLevelName | undefined {
  return (Object.keys(LogLevel) as LogLevelName[]).find(
    (key) => LogLevel[key] === value,
  );
}

console.log(nameOf("INFO")); // "Info" ✅
```

```js
// enum LogLevel { Debug = "DEBUG" } emits:
var LogLevel;
(function (LogLevel) {
    LogLevel["Debug"] = "DEBUG";
})(LogLevel || (LogLevel = {}));
// no LogLevel["DEBUG"] entry: string enums have no reverse map
```

## Key points
- Every member needs an explicit string initializer.
- No reverse mapping is emitted, so lookups by value need `Object.entries`.
- Values are JSON-friendly and stable if you never rename them.
- `keyof typeof E` yields member names; template literal types yield member values.
- String enums are not assignable from arbitrary string literals.

## Gotchas
- A matching string literal does not type-check.
  ```ts
  enum Level { Info = "INFO" }
  // ❌ Error: Type '"INFO"' is not assignable to type 'Level'.
  // const l: Level = "INFO";
  ```
- Indexing a string enum by number is a type error.
  ```ts
  // ❌ Error: Element implicitly has an 'any' type ... index type '0'.
  // const x = Level[0];
  ```
- Changing a value is a breaking wire-format change even if the member name stays.

## Best practice
- Use `PascalCase` member names with `UPPER_SNAKE_CASE` or lowercase string values.
- Treat the string values as a public contract once persisted or logged.
