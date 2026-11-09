# Discriminant Properties

> Phase 2 · Module 08 · Union and Intersection Types

**TL;DR** — The discriminant property is the shared literal key TypeScript uses to tell union members apart.

## Syntax
```ts
type Union =
  | { readonly kind: "a"; /* ... */ }
  | { readonly kind: "b"; /* ... */ };
```

## Examples
### Basic
```ts
type Task =
  | { state: "todo"; title: string }
  | { state: "done"; title: string; completedAt: Date };

function isDone(task: Task): boolean {
  return task.state === "done"; // ✅ literal comparison
}

declare const task: Task;
console.log(isDone(task));
```

### Practical
```ts
type Notification =
  | { channel: "email"; address: string; subject: string }
  | { channel: "sms"; phone: string }
  | { channel: "push"; deviceId: string };

function destination(notification: Notification): string {
  switch (notification.channel) {
    case "email":
      return notification.address;
    case "sms":
      return notification.phone;
    case "push":
      return notification.deviceId;
  }
}

console.log(destination({ channel: "sms", phone: "+15551234" }));
```

### Advanced / edge cases
```ts
type Event =
  | { readonly type: "created"; id: string }
  | { readonly type: "updated"; id: string; fields: string[] }
  | { readonly type: "deleted"; id: string };

function audit(event: Event): string {
  // id is available on every member, so it needs no narrowing.
  const base = `[${event.type}] ${event.id}`;
  if (event.type === "updated") {
    return `${base}: ${event.fields.join(", ")}`; // ✅ narrowed
  }
  return base;
}

console.log(audit({ type: "updated", id: "e_1", fields: ["title"] }));
```

## Key points
- The discriminant must be a literal type such as `"card"` or `42`.
- All members should share the same property name.
- It must be required; optional discriminants weaken narrowing.
- `readonly` prevents accidental reassignment.
- It can be a string, number, or boolean literal.

## Gotchas
- `kind: string` is not a discriminant and will not narrow.
- Optional or union-typed discriminants make exhaustiveness unreliable.

```ts
type Bad =
  | { kind: "a" | "b"; a: number }
  | { kind: "b" | "c"; b: number };
declare const bad: Bad;

// ❌ Error: Property 'a' does not exist on type 'Bad'.
if (bad.kind === "a") console.log(bad.a);
```

## Best practice
- Declare discriminants as `readonly` and required.
- Reuse one conventional key name across a domain.
