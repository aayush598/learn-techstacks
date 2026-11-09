# Const Enums

> Phase 2 · Module 13 · Enums and Literal-Based Alternatives

**TL;DR** — `const enum` members are inlined at compile time and emit no runtime object, removing cost but coupling consumers to the compiler and declaration values.

## Syntax
```ts
const enum Direction {
  Up,
  Down,
}

const d = Direction.Up; // inlined as 0
```

## Examples
### Basic
```ts
const enum Direction {
  Up,
  Down,
  Left,
  Right,
}

function label(d: Direction): string {
  switch (d) {
    case Direction.Up:
      return "Up";
    case Direction.Down:
      return "Down";
    case Direction.Left:
      return "Left";
    case Direction.Right:
      return "Right";
  }
}

console.log(label(Direction.Left)); // "Left" ✅
console.log(Direction.Up);         // 0 (inlined)
```

```js
// With normal compilation there is no Direction object:
function label(d) {
    switch (d) {
        case 0 /* Direction.Up */: return "Up";
        case 1 /* Direction.Down */: return "Down";
        case 2 /* Direction.Left */: return "Left";
        case 3 /* Direction.Right */: return "Right";
    }
}
console.log(label(2 /* Direction.Left */));
console.log(0 /* Direction.Up */);
```

### Practical
```ts
const enum ByteOrder {
  LittleEndian = 0,
  BigEndian = 1,
}

function writeFlag(out: Uint8Array, order: ByteOrder): void {
  out[0] = order === ByteOrder.LittleEndian ? 1 : 0;
}

// Hot-path code avoids an object lookup; values are baked into the output.
const buffer = new Uint8Array(1);
writeFlag(buffer, ByteOrder.BigEndian);
console.log(buffer[0]); // 0 ✅
```

### Advanced / edge cases
```ts
const enum Flags {
  None = 0,
  Read = 1 << 0,
  Write = 1 << 1,
}

// Members can be used in constant expressions and as types.
type ReadFlag = typeof Flags.Read;
const flag: Flags = Flags.Read | Flags.Write;

// Ambient const enums describe values supplied elsewhere.
declare const enum BuildFlavor {
  Dev = "dev",
  Prod = "prod",
}
const flavor = BuildFlavor.Prod; // inlined string
```

```js
// Emitted usage:
const flag = 3 /* Flags.Read | Flags.Write */;
const flavor = "prod" /* BuildFlavor.Prod */;
// No runtime enum objects.
```

Enable `preserveConstEnums` to keep the object for debugging while still inlining:

```json
{ "compilerOptions": { "preserveConstEnums": true } }
```

## Key points
- Every `const enum` member must be a constant expression.
- Member references are replaced with literals; no runtime object is emitted.
- `preserveConstEnums` emits the object but does not stop inlining.
- Ambient `const enum` is a declaration-only contract with no local implementation.
- Inlining makes the enum values part of the consumer's compiled output.

## Gotchas
- Computed initializers are rejected.
  ```ts
  // ❌ Error: const enum member initializers must be constant expressions.
  // const enum E { A = Math.random() }
  ```
- Ambient const enums break under `isolatedModules`.
  ```ts
  // ❌ Error TS2748: Cannot access ambient const enums when
  // 'isolatedModules' is enabled.
  // declare const enum E { A = 1 }
  // const a = E.A;
  ```
- Consumers inline old values, so upgrading the enum can leave stale numbers in already-built code.
- A `const enum` is not a runtime object; dynamic indexing is rejected.
  ```ts
  const enum Direction { Up, Down }
  // ❌ Error TS2476: A const enum member can only be accessed using a string literal.
  // const byIndex = (i: Direction) => Direction[i];
  ```

## Best practice
- Keep `const enum` internal to an application; never export one from a published library.
- Prefer a plain `as const` object when you need a runtime value and stable interop.
