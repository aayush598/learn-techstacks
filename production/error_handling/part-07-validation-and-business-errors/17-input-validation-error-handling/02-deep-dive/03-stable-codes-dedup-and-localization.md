# Stable Codes, Duplicate Detection, and Localization

> Part VII · Chapter 17 · Sections 17.14, 17.15, 17.20, 17.22 · _Estimated reading time: 20 min_
> **Prerequisite:** [Aggregation, Field-Level Representation, and Stable Codes](../01-concepts/04-aggregation-and-field-error-representation.md)

## In one sentence

A validation code is a **versioned contract identifier** — one per rule, never per field, never a
message — and keeping it stable requires a **registry with CI checks**, while keeping it usable
across locales requires moving every human sentence into **`message`/`params` separation**.

## Why this matters in production

Field codes are the most-consumed part of your API surface: SDKs branch on them, frontends render
by them, analytics counts them, and support macros grep them. When a code is renamed for style or
a message is used as a key, every one of those consumers breaks **silently** — a client that
matched `EMAIL_FORMAT` simply stops matching, and users see a raw fallback. The discipline cost is
small (a table and two tests); the drift cost is a quarterly migration.

## The registry discipline (17.14)

One table, owned like an API definition:

```sql
CREATE TABLE validation_codes (
  code          text PRIMARY KEY,          -- 'format_invalid'
  rule          text NOT NULL UNIQUE,      -- 'email-format' (one rule → one code)
  category      text NOT NULL,             -- 'VALIDATION'
  message_key   text NOT NULL,             -- 'validation.format_invalid'
  docs_anchor   text,                      -- link into published contract docs
  added_in      text NOT NULL,             -- 'v3.14'
  deprecated_at text                       -- NULL = active
);
```

Lifecycle rules:

| Change | Compatibility | Allowed? |
| ------ | ------------- | -------- |
| Add new code | Additive | ✅ Anytime (minor version) |
| Reword `message` | None (message is not contract) | ✅ Freely |
| Add new `params` member | Additive | ✅ (clients must ignore unknown params) |
| Rename code | **Breaking** | ❌ Deprecate old, dual-emit, sunset (Ch. 49) |
| Reuse a retired code for a new rule | **Breaking** | ❌ Ever — reserve tombstones |
| Change code casing (`EMAIL` → `email`) | Breaking in practice | ❌ |

## Duplicate detection (17.15) as CI, not vigilance

Four mechanical checks kill the whole duplicate family:

```ts
// 1. Emission ⊆ registry: every emitted code is declared.
// 2. Uniqueness: one rule per code (see SQL UNIQUE above).
// 3. Anti-pattern lint: reject per-field codes in source.
const FORBIDDEN_CODE = /^[A-Z]+_[A-Z_]+_(INVALID|REQUIRED|ERROR)$/; // NAME_REQUIRED, SLUG_INVALID…
const FORBIDDEN_MESSAGE_AS_CODE = /\s|[a-z]{4,}\s[A-Z]/;           // 'Please enter a name'

// 4. Runtime sample check in staging: run a corpus of bad payloads; assert every
//    (pointer, code) pair against the registry and assert one primary code per pointer.
```

The lint deserves emphasis: **per-field codes are the #1 registry rot source**. If someone adds
`INVOICE_NUMBER_FORMAT`, the lint fails and the review conversation is "use `format_invalid` +
`params.format`" — which is exactly the policy, enforced before merge rather than in a retro.

Duplicate *emissions* (same rule firing twice) are handled in the accumulator, not the registry:

```ts
// Dedup at the accumulator: keyed on (pointer, code); also one primary code per pointer.
if (!seen.has(`${pointer}::${code}`)) { seen.add(`${pointer}::${code}`); issues.push(issue); }
```

## Localization by design (17.20)

The contract-level split:

```json
{
  "pointer": "/seats",
  "code": "out_of_range",
  "messageKey": "validation.out_of_range",
  "message": "Seats must be between 1 and 500.",
  "params": { "min": 1, "max": 500 }
}
```

| Member | Locale-aware? | Stability |
| ------ | ------------- | --------- |
| `pointer`, `code` | Never | Contract |
| `params` | Values only, no prose | Contract (additive) |
| `messageKey` | Key itself is locale-free | Semi-contract |
| `message` | Fully replaceable | Not contract |

Client algorithm (what we recommend every Acme client implements):

```ts
function renderFieldError(e: FieldError, dict: Dict): string {
  const template = dict[e.messageKey] ?? dict[`validation.${e.code}`] ?? e.message ?? e.code;
  return interpolate(template, e.params);   // {min} {max} interpolation from params
}
```

Consequences:

- The **server may ship English defaults**; clients with dictionaries fully localize.
- A translation can never break branching, because branches never read `message`.
- `params` must be **interpolation-complete**: if a translator needs the limit, the limit is in
  `params` — never parse it out of the English sentence.

Server-side localization (`Accept-Language`) is a valid maturity step, with two gotchas: CDN
caching of error responses keyed only by URL (add `Vary: Accept-Language`), and the temptation to
put localized text into logs (log `code`+`params`, not the sentence).

## Contract consistency mechanics (17.22)

Consistency is enforced, not hoped for:

```text
1. One envelope builder      toValidationProblem(acc, ctx)  — used by every route
2. One status policy table   parse→400, schema→422, …        (see Ch. 19/20)
3. One pointer convention    RFC 6901, container = "/"
4. One cap + truncation flag MAX_ISSUES, errorsTruncated
5. Golden snapshots in CI    one 422 fixture per endpoint family, diff = review
```

```ts
// The only place a 422 is ever constructed — drift becomes a diff, not a surprise.
export function toValidationProblem(acc: ValidationAccumulator, ctx: Ctx) {
  return {
    status: 422,
    body: {
      type: "https://errors.acme.example/validation",
      title: "VALIDATION_FAILED",
      status: 422,
      detail: `The request contains ${acc.list.errors.length} invalid field(s).`,
      instance: ctx.path,
      requestId: ctx.requestId,
      ...acc.list,                       // errors[] + optional errorsTruncated
    },
  };
}
```

Versioning in one paragraph: additive members are safe; a *second* envelope shape is not
"additive", it is a fork. If a mobile client needs the legacy shape, version the **path**
(`/v1/projects` keeps old behavior) rather than branching the envelope per client header.

## Key data / numbers

- Registry columns: `code` (PK), `rule` (UNIQUE), `message_key`, `added_in`, `deprecated_at`.
- Stability: `pointer`+`code`+`params` = contract; `message` = presentation; unknown `params`
  members must be ignored by clients.
- Recommended cap (repeated for the contract): **100 issues**, flag `errorsTruncated: true`.
- CI checks: emission⊆registry, uniqueness lint, anti-pattern lint, golden 422 snapshots.

## Real-world use case — Acme SaaS

Two Acme teams shipped email validation the same quarter: `EMAIL_FORMAT_INVALID` (web team) and
`format_invalid` + `params.format=email` (API team). Frontend code special-cased both; a third
team later added `INVALID_EMAIL` for a bulk importer and the special-casing grew to three. The
registry + anti-pattern lint landed with the v3 contract: existing codes were frozen as tombstones
and dual-emitted for two minor versions, then removed. Client code collapsed to one branch, and
localization shipped a month later without server changes because every message was already a
replaceable string over stable `params`.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Registry + CI discipline | Drift impossible by construction | Small upfront cost | ✅ Any API with clients |
| Convention-only (docs) | Zero setup | Rot within quarters | Toy projects |
| Client-side dicts over codes | Server stays locale-free | Clients lag translations | ✅ Default strategy |
| Server-side per-locale text | Instant wording control | Cache/pipeline complexity | Mature global products |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Register codes before first emission; CI-verify | Let string literals be the registry |
| Tombstone retired codes forever | Reuse or silently rename a code |
| Put fixable values in `params` | Embed limits inside `message` prose |
| Build every 422 through one function | Hand-construct envelopes per handler |
| Snapshot golden responses per family | Assume consistency will hold by review |

## Common mistakes

- **Lint that only checks casing** — misses `INVALID_EMAIL` (per-field) shaped like a fine code.
- **Renaming for aesthetics mid-version** — every rename is a client migration you just scheduled.
- **Localized `code`s** — `code: "erforderlich"` breaks all branching.
- **Forgetting `Vary` on localized error responses** — one user's language leaks into another's
  cached 422.

## Checklist

- [ ] Every code exists in the registry with exactly one rule.
- [ ] Emission ⊆ registry is a CI test; anti-pattern lint rejects per-field codes.
- [ ] Retired codes are tombstoned, never reused.
- [ ] Every response carries interpolation-complete `params`.
- [ ] One `toValidationProblem` builder; golden snapshots per endpoint family.
- [ ] Localization strategy (client-dict vs server) documented and uniform.

## Related

- [Aggregation, Field-Level Representation, and Stable Codes](../01-concepts/04-aggregation-and-field-error-representation.md)
- [Trust Boundaries, Untrusted Clients, and the Validation Contract](../01-concepts/05-trust-boundaries-clients-and-contracts.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
