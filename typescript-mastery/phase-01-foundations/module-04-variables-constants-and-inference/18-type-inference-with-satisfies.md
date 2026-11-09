# Type Inference with `satisfies`

> Phase 1 · Module 04 · Variables, Constants, and Type Inference

**TL;DR** — `satisfies` lets the target type guide checking while inference keeps the most precise type of the value.

## Syntax
```ts
const mode = "dark" satisfies "light" | "dark";
const frozen = { mode: "dark" } as const satisfies { mode: string };
```

## Examples
### Basic
```ts
type Point = { x: number; y: number };

const p = { x: 1, y: 2 } satisfies Point; // { x: number; y: number }

type Mode = "light" | "dark";
const mode = "dark" satisfies Mode; // "dark"
```

### Practical
```ts
type Palette = Record<"primary" | "secondary", string>;

const palette = {
  primary: "#0af",
  secondary: "#f0a",
} satisfies Palette;

type Primary = typeof palette.primary; // string
type Keys = keyof typeof palette;      // "primary" | "secondary"

// Literal members stay literal
const sizes = {
  sm: 4,
  lg: 8,
} satisfies Record<string, number>;

type Sm = typeof sizes.sm; // number

console.log(palette, sizes, null as unknown as Primary, null as unknown as Keys, null as unknown as Sm);
```

### Advanced / edge cases
```ts
type EventMap = {
  click: { x: number; y: number };
  keydown: { key: string };
};

const handlers = {
  click: (e: { x: number; y: number }) => e.x,
  keydown: (e: { key: string }) => e.key.length,
} satisfies { [K in keyof EventMap]: (e: EventMap[K]) => unknown };

type HandlerKeys = keyof typeof handlers; // "click" | "keydown"

// Literal inference is preserved inside arrays too
const levels = ["low", "high"] as const satisfies readonly string[];
type Level = (typeof levels)[number]; // "low" | "high"

// Missing keys are still rejected
// const broken = { click: () => 0 } satisfies {
//   [K in keyof EventMap]: (e: EventMap[K]) => unknown;
// };
// ❌ Error: Property 'keydown' is missing.

const lvl: Level = "high";
console.log(handlers, levels, lvl, null as unknown as HandlerKeys);
```

## Key points
- The target type drives contextual typing of the expression.
- The resulting type is the expression's inferred type, not the target.
- Literal and tuple precision survive the check.
- Works with mapped and indexed target types.
- `as const satisfies T` combines precision with validation.

## Gotchas
- Inference is still subject to widening for `let` and mutable members.
- `satisfies` checks assignability, so extra properties can pass via variables.
- An annotation plus `satisfies` is redundant; choose one.

## Best practice
- Use `satisfies` on constant maps and configs where exact keys matter.
- Pair with `as const` when consumers need literal unions.
