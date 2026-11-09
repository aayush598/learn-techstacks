# `in` operator narrowing

> Phase 2 · Module 09 · Type Narrowing and Type Guards

**TL;DR** — The `in` operator narrows unions by checking whether a property exists on the value.

## Syntax
```ts
if ("property" in value) {
  // value has that property
}
```

## Examples
### Basic
```ts
type Cat = { meow: () => void };
type Dog = { bark: () => void };

function speak(animal: Cat | Dog): void {
  if ("meow" in animal) {
    animal.meow(); // ✅ Cat
  } else {
    animal.bark(); // ✅ Dog
  }
}
```

### Practical
```ts
type Success = { data: string };
type Failure = { error: Error };

function unwrap(result: Success | Failure): string {
  if ("error" in result) {
    throw result.error; // ✅ Failure
  }
  return result.data; // ✅ Success
}
```

### Advanced / edge cases
```ts
type TextNode = { text: string };
type ElementNode = { tag: string; children: Node[] };
type Node = TextNode | ElementNode;

function render(node: Node): string {
  if ("children" in node) {
    return `<${node.tag}>${node.children.map(render).join("")}</${node.tag}>`; // ✅ ElementNode
  }
  return node.text; // ✅ TextNode
}

function hasOwn<T extends object>(obj: T, key: PropertyKey): boolean {
  return Object.prototype.hasOwnProperty.call(obj, key);
}
```

## Key points
- `"key" in value` narrows to union members that declare that key.
- Works on object types, including interfaces and type aliases.
- Useful when there is no discriminant field.
- `in` also traverses the prototype chain at runtime.
- Can be combined with `typeof` or truthiness for extra safety.

## Gotchas
- `in` checks existence, not type or truthiness of the value.
- Optional properties make `in` unreliable for discrimination.
- `// ❌ Error:` `"meow" in animal` does not narrow when both members declare an optional `meow`.

## Best practice
- Prefer a discriminant property when you control the types.
- Use `in` for third-party shapes you cannot change.
