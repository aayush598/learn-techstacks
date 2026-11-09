# Function Type Aliases

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — A function type alias names a signature with `(params) => Return`, making callbacks and handlers reusable.

## Syntax
```ts
type Handler = (event: string) => void;
```

## Examples
### Basic
```ts
type Handler = (event: string) => void;

const log: Handler = (event) => console.log(event);

log("click");
```

### Practical
```ts
type AsyncMapper<T, U> = (value: T) => Promise<U>;

interface Options {
  onSuccess?: (value: string) => void;
  onError?: (error: Error) => void;
}

function fetchText(url: string, options: Options = {}): Promise<string> {
  return fetch(url)
    .then((res) => res.text())
    .then((text) => {
      options.onSuccess?.(text);
      return text;
    })
    .catch((error: Error) => {
      options.onError?.(error);
      throw error;
    });
}

const toLength: AsyncMapper<string, number> = async (value) => value.length;
```

### Advanced / edge cases
```ts
// Generic function alias
type Identity = <T>(value: T) => T;

const identity: Identity = (value) => value;

// Overloads via an object type alias with multiple call signatures.
type Parse = {
  (input: string): number;
  (input: number): string;
};

// Or via an intersection of function types.
type ParseAlt = ((input: string) => number) & ((input: number) => string);

// Explicit `this` typing
type ClickHandler = (this: HTMLElement, event: MouseEvent) => void;

const onClick: ClickHandler = function (event) {
  console.log(this.tagName, event.type);
};
```

## Key points
- Function aliases describe callable values, not implementations.
- Generic aliases keep input and output types linked.
- Overloads are expressible with an object type or an intersection.
- An explicit `this` parameter is part of the signature.
- Contextual typing flows from the alias into parameters.

## Gotchas
- `// ❌ Error:` `const h: Handler = (event: number) => {};` — parameter type mismatch.
- Function aliases cannot be implemented by a class, since instances are not callable.
- Returning `void` does not force the callback to return nothing; it discards any result.

## Best practice
- Name callback types by role: `Handler`, `Reducer`, `Comparator`, `Mapper`.
- Prefer `unknown` over `any` in generic callback inputs.
