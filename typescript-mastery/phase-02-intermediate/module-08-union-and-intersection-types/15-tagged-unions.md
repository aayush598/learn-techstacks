# Tagged Unions

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — A tagged union is a discriminated union whose discriminant is a descriptive tag, often used at API and event boundaries.

## Syntax
```ts
type Message =
  | { tag: "created"; /* ... */ }
  | { tag: "deleted"; /* ... */ };
```

## Examples
### Basic
```ts
type Shape =
  | { tag: "circle"; radius: number }
  | { tag: "rect"; width: number; height: number };

function area(shape: Shape): number {
  switch (shape.tag) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rect":
      return shape.width * shape.height;
  }
}

console.log(area({ tag: "rect", width: 2, height: 5 }));
```

### Practical
```ts
type WebhookEvent =
  | { event: "user.created"; payload: { id: string; email: string } }
  | { event: "user.deleted"; payload: { id: string } }
  | { event: "invoice.paid"; payload: { invoiceId: string; amount: number } };

function handle(event: WebhookEvent): string {
  switch (event.event) {
    case "user.created":
      return `created ${event.payload.email}`;
    case "user.deleted":
      return `deleted ${event.payload.id}`;
    case "invoice.paid":
      return `paid ${event.payload.amount}`;
  }
}

console.log(handle({ event: "user.deleted", payload: { id: "u_1" } }));
```

### Advanced / edge cases
```ts
type Shape =
  | { tag: "circle"; radius: number }
  | { tag: "rect"; width: number; height: number };

type Drawing =
  | { tag: "shape"; shape: Shape }
  | { tag: "group"; children: Drawing[] };

function area(drawing: Drawing): number {
  switch (drawing.tag) {
    case "shape":
      return drawing.shape.tag === "circle"
        ? Math.PI * drawing.shape.radius ** 2
        : drawing.shape.width * drawing.shape.height;
    case "group":
      return drawing.children.reduce((sum, child) => sum + area(child), 0);
  }
}

// ✅ tags compose through nested structures
console.log(
  area({
    tag: "group",
    children: [
      { tag: "shape", shape: { tag: "circle", radius: 1 } },
      { tag: "shape", shape: { tag: "rect", width: 2, height: 3 } },
    ],
  }),
);
```

## Key points
- "Tagged union" and "discriminated union" describe the same pattern.
- Tags are usually string literals such as `"user.created"`.
- Tags can be nested to model recursive structures.
- Tags make JSON payloads self-describing.
- Narrowing works identically to any discriminated union.

## Gotchas
- An untrusted API payload needs runtime validation; the tag type alone proves nothing.
- Renaming a tag is a breaking change across producers and consumers.

```ts
type Event = { event: "created" } | { event: "deleted" };

const raw: unknown = JSON.parse('{"event":"archived"}');

// ❌ Error: Type 'unknown' is not assignable to type 'Event'.
const event: Event = raw;
```

## Best practice
- Validate external tagged payloads at the boundary before trusting the tag.
- Use dotted, namespaced tags for event streams and webhooks.
