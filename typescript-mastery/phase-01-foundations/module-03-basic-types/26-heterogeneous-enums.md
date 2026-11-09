# Heterogeneous Enums

> Phase 1 · Module 03 · Basic Types

**TL;DR** — Heterogeneous enums mix string and numeric members; TypeScript allows it, but it is rarely a good idea.

## Syntax
```ts
enum Mixed {
  No = 0,
  Yes = "YES",
}
```

## Examples
### Basic
```ts
enum Answer {
  No = 0,
  Yes = "YES",
}

console.log(Answer.No);  // 0
console.log(Answer.Yes); // "YES" ✅
```

### Practical
```ts
// Useful only when bridging legacy numeric codes and labels
enum LegacyCode {
  Success = 200,
  Failure = "FAIL",
}

function describe(code: LegacyCode): string {
  return code === LegacyCode.Success ? "ok" : String(code);
}

console.log(describe(LegacyCode.Success)); // "ok" ✅
console.log(describe(LegacyCode.Failure)); // "FAIL"
```

### Advanced / edge cases
```ts
// Only numeric members get reverse mappings
enum Mixed {
  Zero = 0,
  Name = "name",
}

console.log(Mixed[0]);        // "Zero" ✅
console.log((Mixed as Record<string, unknown>)["name"]); // undefined
console.log(Object.values(Mixed)); // [0, "name"]

// Auto-numbering only applies to uninitialized members after a numeric one
enum Weird {
  A = 0,
  B,          // 1
  C = "c",
}
console.log(Weird.B, Weird.C);
```

## Key points
- Heterogeneous enums contain both numeric and string members.
- Only numeric members produce reverse mappings.
- Auto-increment stops at a string member.
- The resulting union type is a mix of `number` and `string`.
- They complicate switch exhaustiveness and serialization.

## Gotchas
- The mixed value type makes comparisons and formatting awkward.
  ```ts
  enum M { A = 0, B = "b" }
  const v: string = M.A; // ❌ number is not a string
  ```
- Reverse lookups are inconsistent.
  ```ts
  enum M { A = 0, B = "b" }
  console.log(M[0], (M as Record<string, unknown>)["b"]); // "A", undefined
  ```
- Tooling and schema generators handle mixed enums poorly.

## Best practice
- Avoid heterogeneous enums; pick all-numeric or all-string.
- Prefer a literal union when the set is simple.
