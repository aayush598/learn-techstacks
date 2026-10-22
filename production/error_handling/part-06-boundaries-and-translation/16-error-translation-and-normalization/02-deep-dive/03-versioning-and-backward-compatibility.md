# Versioning and Backward Compatibility of Translations

> Part VI · Chapter 16 · Section 16.18 · _Estimated reading time: 18 min_
> **Prerequisite:** [Vendor Codes, Tables, and Versioning](../01-concepts/05-vendor-codes-tables-and-versioning.md)

## In one sentence

Translation mappings are **contracts**, so changing what a vendor error maps to can break clients —
the safe rule is to **add and deprecate, never redefine**, and to version any change that alters a
public code or status.

## Why this matters in production

Internal adapters are free to change; the *public* mapping (code + HTTP status + category) is not.
A team that "fixes" a mapping from `409` to `422` silently breaks every client that branches on the
status, every SDK generated against it, and every saved automation. Versioning rules make adding a
provider or a code a non-event while making a redefinition an explicit, reviewed decision.

## The boundary between internal and public

| Layer | Mutable freely? | Versioned? |
| ----- | --------------- | ---------- |
| Vendor → adapter code extraction | Yes | No |
| Adapter → internal `AppError` | Mostly yes | Internal contract (Ch. 6.20) |
| Internal → public `code` / status / body | **No** | Yes (Ch. 49) |

The translation table straddles all three. Mark each column accordingly:

```text
Rule.match       (vendor side)   → free to change
Rule.to.category (internal)      → internal contract
Rule.to.code     (public)        → PUBLIC contract — versioned
Rule.to.httpStatus (public)      → PUBLIC contract — versioned
Rule.to.safeMessage (public)     → clients must NOT depend on text
```

## The compatibility matrix

| Change | Impact | Allowed? | Action |
| ------ | ------ | -------- | ------ |
| Add a new vendor | None on consumers | ✅ | Add adapter + rules + coverage |
| Add a new public code | Additive | ✅ | Document; add to registry |
| Map a new vendor code to an **existing** public code | Additive | ✅ | Add rule |
| Change a `safeMessage` wording | Clients must not depend on text | ✅* | Announce; no ID change |
| Change a code's `httpStatus` | Breaking | ⚠️ | Version or avoid; ADR |
| Change a code's `category` | Breaking (retry/status) | ⚠️ | Version or avoid |
| Change a public `code` string | Breaking | ❌ direct | Deprecate old → map to new |
| Remove a code | Breaking | ❌ direct | Deprecate; keep mapping for ≥1 version |
| Reuse a code for a new meaning | Breaking + dangerous | ❌ | Create a new code |

\* Text changes are safe **only if** clients are explicitly barred from depending on messages
(Ch. 49.9, 49.16).

## Additive evolution: the default path

```ts
// Add a new rule; do not touch existing ones.
const RULES: Rule[] = [
  // ... existing ...
  { match: { source: "stripe", code: "new_decline_subtype" },
    to: { code: "PAYMENT_CARD_DECLINED", category: "BUSINESS", transient: false, httpStatus: 402,
          safeMessage: "Your card was declined." } }, // reuses an existing stable code
];
```

Mapping a new vendor condition to an **existing** stable code is the ideal: the public contract is
unchanged, and only the adapter's coverage grows.

## Deprecation: renaming / retiring a code

When you must change a public code, use a two-phase deprecation:

1. **Introduce the successor** alongside the old code.
2. **Mark the old code deprecated**; map the new vendor meaning to the successor.
3. **Honor both** for at least one contract version: an old client still gets the old code.
4. **Remove the old code** only after the deprecation window and after clients have migrated.

```ts
type Deprecation = { from: string; to: string; sunsetContract: string };

const DEPRECATIONS: Deprecation[] = [
  { from: "PAYMENT_DECLINED", to: "PAYMENT_CARD_DECLINED", sunsetContract: "v2026-06" },
];

function applyDeprecation(code: string, apiVersion: string): string {
  const d = DEPRECATIONS.find((x) => x.from === code && apiVersion < x.sunsetContract);
  return d ? d.from : code; // old clients keep the old code until sunset
}
```

The API version selects which side of the deprecation the client sees — this is the standard
versioned-contract technique (Ch. 49).

## Versioning the internal error model

The internal `AppError` (Ch. 6.20) has its own contract across your services. When multiple services
exchange errors (gRPC, message queues), version the model:

- Add fields with defaults; readers tolerate absent fields.
- Never remove or repurpose a field in place.
- Use a schema (protobuf/JSON Schema) and test forward/backward compatibility in CI.

## Forward compatibility on the client

An older client must survive a newer server's codes. The rules (Ch. 19, Ch. 49):

- **Unknown code → fall back to the HTTP status.** Keep the status meaningful so an old client can
  still act (e.g. any `4xx` = user action, any `5xx` = retry/support).
- **Never parse messages** for control flow.
- **Ignore unknown fields** in the error envelope.

```ts
function clientAction(res: Problem): "retry" | "fix" | "support" {
  const known = CODE_ACTIONS[res.title];
  if (known) return known;
  if (res.status >= 500) return "retry";
  if (res.status === 401 || res.status === 403) return "fix";
  return "support"; // unknown 4xx → safest non-destructive default
}
```

## Testing compatibility

| Test | Catches |
| ---- | ------- |
| **Snapshot every public mapping** (`code`, status, category) | Accidental redefinitions |
| **Additive-only diff** on the table in CI | Removed/renamed codes |
| **Old-client fixture** against new envelope | Forward-compat regressions |
| **Deprecation honoring** per API version | Premature sunset |

```ts
test("public mapping is additive-only", () => {
  const current = snapshotPublicMapping(RULES);
  expect(current).toMatchSnapshot(); // any removal/rename fails the diff
});
```

## Key data / numbers

- Deprecation window: keep a deprecated public code for **at least one contract version**.
- Safe additions: new vendor, new code, new vendor→existing-code rule, message wording.
- Breaking: status change, category change, code rename/removal, code reuse.
- Forward-compat rule: **unknown code → fall back to HTTP status class**.

## Real-world use case — Acme SaaS

A well-meaning change mapped Postgres `23503` (FK) from `404` to `422` to "be more accurate." It
was technically reasonable internally but **broke** Acme's mobile client, which retried `404`s
differently and surfaced `422`s as field errors. The team reverted, introduced versioned mapping
(`v2026-06` keeps `404`), and added a snapshot test that fails on any public-mapping change unless
an ADR is attached. Future status reevaluations go through the versioned path.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Add codes and rules; leave old ones intact | Rename/remove a public code directly |
| Map new vendor conditions to existing stable codes | Redefine an existing code's meaning |
| Version changes to status/category | Change a status in place |
| Keep statuses meaningful for old clients | Make clients depend on message text |
| Snapshot the public mapping in CI | Trust review to catch redefinitions |

## Common mistakes

- **"Improving" a status** without versioning — silent client breakage.
- **Reusing a code** for a new meaning, corrupting analytics and clients.
- **Removing a deprecated code** before the sunset.
- **Clients parsing messages** for behavior, then breaking on a wording change.

## Checklist

- [ ] Public mapping (code, status, category) is snapshot-tested in CI.
- [ ] Changes are additive by default; redefinitions require an ADR.
- [ ] Deprecated codes are honored for the full contract window.
- [ ] Clients fall back to status class for unknown codes.
- [ ] Messages are never part of the machine contract.

## Related

- [Vendor Codes, Tables, and Versioning](../01-concepts/05-vendor-codes-tables-and-versioning.md)
- [Translation Tables and Policies](./01-translation-tables-and-policies.md)
- [Part XIX — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
