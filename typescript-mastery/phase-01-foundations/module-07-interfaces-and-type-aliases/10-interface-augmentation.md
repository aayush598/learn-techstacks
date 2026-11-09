# Interface Augmentation

> Phase 1 · Module 07 · Interfaces and Type Aliases

**TL;DR** — Interface augmentation adds members to an interface declared in another module without editing that module's source.

## Syntax
```ts
export {};

declare global {
  interface Window {
    appVersion: string;
  }
}
```

## Examples
### Basic
```ts
export {};

declare global {
  interface Window {
    appVersion: string;
  }
}

// ✅ Window now requires appVersion
window.appVersion = "1.2.3";
console.log(window.appVersion);
```

### Practical
```ts
// src/types/express.d.ts
import "express";

declare module "express-serve-static-core" {
  interface Request {
    user?: {
      id: string;
      role: "admin" | "user";
    };
  }
}

// Elsewhere: request.user is now typed.
```

### Advanced / edge cases
```ts
// Augment a library interface with a generic member.
import "fastify";

declare module "fastify" {
  interface FastifyRequest {
    traceId: string;
  }
}

// Augment multiple interfaces from the same module in one block.
declare module "some-lib" {
  interface Options {
    debug?: boolean;
  }
  interface Result {
    durationMs: number;
  }
}
```

## Key points
- Augmentation targets an existing interface in another module.
- The file must be a module, so include an `import` or `export {}`.
- Use `declare global` to augment global interfaces.
- Added members become part of the original type everywhere.
- Augmentation is erased at runtime; it only changes types.

## Gotchas
- `// ❌ Error:` `declare module "pkg" { interface X { a: number } }` in a script file without `import`/`export` — not a module augmentation.
- Adding a conflicting member type fails: `// ❌ Error:` same property declared as a different type.
- Augmentation cannot add a brand-new exported value; it only extends existing declarations.

## Best practice
- Put augmentations in a dedicated `.d.ts` file under a `types/` directory.
- Augment only stable extension points; avoid patching types you do not own.
