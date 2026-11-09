# Rest Elements in Tuples

> Phase 1 · Module 03 · Basic Types

**TL;DR** — A rest element (`...T[]`) lets a tuple start with fixed positions and end with a variable-length tail.

## Syntax
```ts
let row: [string, ...number[]] = ["scores", 90, 85, 77];
let pair: [...string[], number] = ["a", "b", 1];
```

## Examples
### Basic
```ts
const row: [string, ...number[]] = ["scores", 90, 85, 77];
const [label, ...values] = row;

console.log(label, values); // scores [90, 85, 77] ✅
```

### Practical
```ts
type LogEntry = [level: "info" | "warn", ...messages: string[]];

function log([level, ...messages]: LogEntry): void {
  console.log(`[${level}]`, messages.join(" "));
}

log(["info", "server", "started"]); // ✅
log(["warn"]);                      // ✅
```

### Advanced / edge cases
```ts
// Rest can be in the middle, with fixed trailing elements
type Command = [...flags: string[], name: string];
const cmd: Command = ["--verbose", "--fast", "build"]; // ✅
console.log(cmd.at(-1)); // "build"

// A generic rest tuple captures any arguments
function tuple<T extends unknown[]>(...args: T): T {
  return args;
}
const t = tuple("a", 1, true); // [string, number, boolean]

// Empty rest is allowed
const justLabel: [string, ...number[]] = ["none"];
console.log(justLabel, t);
```

## Key points
- Rest elements capture zero or more trailing values.
- A tuple may have at most one rest element.
- Rest can appear mid-tuple when a fixed tail follows.
- Destructuring separates fixed heads from the rest array.
- Rest tuples pair with generics to type variadic functions.

## Gotchas
- Only one rest element is allowed.
  ```ts
  // ❌ Error: A rest element cannot follow another rest element.
  // type Bad = [...string[], ...number[]];
  ```
- The rest type must be an array type.
  ```ts
  // ❌ Error: A rest element type must be an array type.
  // type Bad = [string, ...number];
  ```
- A mid-tuple rest forces the tail to be fixed.
  ```ts
  // ❌ Error: An optional element cannot follow a rest element.
  // type Bad = [...string[], number?];
  ```

## Best practice
- Use rest tuples for variadic functions with typed leading args.
- Prefer named tuple elements to keep the intent readable.
