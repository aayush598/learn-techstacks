# Heterogeneous Enums

> Phase 2 · Module 13 · Enums and Literal-Based Alternatives

**TL;DR** — Heterogeneous enums mix string and numeric members, producing an inconsistent runtime shape with reverse mappings only for the numeric side.

## Syntax
```ts
enum Result {
  Failure = 0,
  Success = 1,
  Unknown = "UNKNOWN",
}
```

## Examples
### Basic
```ts
enum Mixed {
  No = 0,
  Yes = "YES",
}

console.log(Mixed.No);      // 0
console.log(Mixed.Yes);     // "YES"
console.log(Mixed[0]);      // "No" ✅ numeric member
console.log((Mixed as any)["YES"]); // undefined — no reverse mapping
```

### Practical
```ts
// Sometimes seen when migrating legacy numeric codes to readable values.
enum LegacyStatus {
  Active = 1,
  Inactive = 0,
  Deleted = "deleted",
}

function isDeleted(status: LegacyStatus): boolean {
  return status === LegacyStatus.Deleted;
}

console.log(isDeleted(LegacyStatus.Deleted)); // true ✅
```

### Advanced / edge cases
```ts
enum ResponseCode {
  Ok = 0,
  Created = 1,
  Unknown = "UNKNOWN",
}

const keys = Object.keys(ResponseCode);
// ["0", "1", "Ok", "Created", "Unknown"]

const values = Object.values(ResponseCode);
// ["Ok", "Created", "Unknown", 0, 1]

// Numeric members still accept arbitrary numbers; string members do not.
const a: ResponseCode = 42;         // ✅ compiles (numeric side)
// ❌ Error: Type '"UNKNOWN"' is not assignable to type 'ResponseCode'.
// const b: ResponseCode = "UNKNOWN";

// The enum type is a union, so narrowing matches concrete member types.
function normalize(code: ResponseCode): string {
  return typeof code === "number" ? `code:${code}` : code;
}
```

```js
var ResponseCode;
(function (ResponseCode) {
    ResponseCode[ResponseCode["Ok"] = 0] = "Ok";
    ResponseCode[ResponseCode["Created"] = 1] = "Created";
    ResponseCode["Unknown"] = "UNKNOWN";
})(ResponseCode || (ResponseCode = {}));
```

## Key points
- Members may be numeric or string, but not both in one member.
- Reverse mappings exist only for numeric members.
- `Object.keys`/`Object.values` return a mix of names, numeric strings, and values.
- The enum type is still a union of the member types.
- Heterogeneous enums are almost always a sign of an unclear wire format.

## Gotchas
- Runtime shape differs per member, so generic iteration is unreliable.
- Numeric members keep the `number` assignability hole while string members are closed.
  ```ts
  enum E { A = 0, B = "b" }
  const bad: E = 123; // ✅ compiles — numeric side leaks
  ```
- Serialized output is not uniform, which breaks schemas and validators.

## Best practice
- Avoid heterogeneous enums; split into a numeric enum and a string union.
- If you inherit one, convert it at the boundary before it spreads.
