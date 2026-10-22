# Ownership, Documentation, and Message Independence

> Part XIX · Chapter 49 · Sections 49.14–49.16 · _Estimated reading time: 18 min_
> **Prerequisite:** [Evolution Rules and Compatibility](./02-evolution-rules-and-compatibility.md)

## In one sentence

Every contract has a **named owner** who approves changes, every contract **documents what
consumers may rely on**, and **messages are never part of that promise** — because wording
changes for good reasons and machine logic should never depend on it.

## Why this matters in production

An unowned contract is a contract nobody defends. When Acme's platform team changed the
meaning of `PAYMENT_CARD_DECLINED` in a "small cleanup", nobody was in a position to say no,
because nobody owned the public error catalogue. The partner who relied on it found out from
their own customers.

Documentation suffers the same way. If the error catalogue says only "returns 400 on failure",
then every consumer is guessing at the parts that matter: is it retryable? is it safe to retry?
does the code still exist? will it change? A contract document is not documentation for humans'
benefit — it is **the input to other people's code**.

## 49.14 — Ownership

Ownership answers three questions that a contract cannot answer for itself:

1. **Who may approve a breaking change?**
2. **Who answers "is this code still supported?"?**
3. **Who is paged when a consumer reports the contract is broken?**

### The three roles

| Role | Owns | Typical holder |
| ---- | ---- | -------------- |
| **Contract owner** (team) | The whole surface: stability policy, deprecation windows, major versions | Platform, API, or product team |
| **Code steward** (person/rotation) | Specific code families: naming, registry rows, deprecation state | The team that owns the domain |
| **Escalation path** | Being reachable when a consumer breaks | On-call for the owning team |

**Every contract has exactly one contract owner.** Not two, not "the backend team". Two owners
means nobody decides.

### What ownership buys

- **A review gate.** Changing a T3 code's status requires the owner's approval — the same way
  changing a public endpoint requires API review.
- **A changelog author.** The owner writes the migration note when a code is deprecated.
- **A sunset authority.** Only the owner can approve removal, and only on telemetry evidence.
- **A migration budget.** Deprecations cost the *consumer* time; the owner owes them a window
  long enough to absorb it.

### Making ownership real

Ownership that lives only in a wiki does not survive reorganisation. Encode it where the work
happens:

```yaml
# Ownership travels with the code, not with a document.
# .error-contract.yaml (per surface)
surface: public-api
owner:
  team: api-platform
  contact: api-platform@acme.example
stewards:
  PAYMENT: billing-team
  EXPORT:  data-team
  AGENT:   ai-platform
stability_tier: T3
deprecation_window_days: 90
```

```text
# CODEOWNERS (or equivalent) — the same team reviews the contract
/packages/errors/            @acme/api-platform
/packages/errors/payment.*   @acme/billing-team
```

### Changing ownership

Ownership transfers **with the domain**, not with the person. When Acme moved billing out of
the monolith, the `PAYMENT_*` code family moved with it: new steward, new owner, same codes,
same meanings, same public promises. Transferring a code family **must not change its
meaning** — that would be a breaking change disguised as a reorganisation.

## 49.15 — Documenting behaviour

A contract document states **guarantees**, not observations. The distinction is what makes it
worth writing.

| Category | Example | Stability |
| -------- | ------- | --------- |
| **Guarantee** | "Every error response has a `code` field." | Binding; changing it is breaking |
| **Guarantee** | "`code` values are append-only within contract version 1.x." | Binding |
| **Guarantee** | "Unknown `code` values must be treated as a generic internal error." | Binding on consumers |
| **Observation** | "Most validation failures are `422`." | Non-binding; changes with traffic |
| **Observation** | "Database errors usually surface as `503`." | Non-binding; an implementation detail |

Documenting an observation as a guarantee is how a contract becomes a trap: the first time the
implementation deviates, either the code is wrong or the contract is. **Do not promise what you
do not control.**

### The per-code contract row

Every public code needs at least this much:

```text
code · since · status · type URI · retryable · idempotent · clientAction · messageKey
     · description · deprecated? · replacedBy · owner
```

And the surface-level document needs:

```text
1. Stability tier and what is guaranteed
2. The error body shape (fields, optionality, types)
3. The code catalogue (per-code rows)
4. The change policy (what breaks, what needs a window, how long)
5. The unknown-code obligation
6. The deprecation and sunset process
7. The contact and escalation path
```

### Versioning the document

The contract document has its own version, and it moves only when the contract moves:

| Document change | Contract version |
| --------------- | ---------------- |
| New code, new optional field | MINOR |
| Wording of descriptions, examples | PATCH |
| Code removed, status changed, meaning changed | MAJOR |

A document that changes weekly without a version bump trains readers to ignore it.

## 49.16 — Not relying on messages

This is the rule that is violated most often and costs the most, because the violation is
invisible until the wording changes.

### Why message-branching is tempting

The message is right there, human-readable, and already localized by the platform team. It looks
like the cheapest possible integration point. And it works — until it doesn't.

| Failure | What happens |
| ------- | ------------ |
| Rewording | `"Request timed out"` → `"The operation timed out"` — a `startsWith` check stops matching |
| Localisation | The server returns the user's locale — a client comparing to an English literal breaks for non-English users |
| Interpolation | `"User 'bob' not found"` — a client extracting the username with a regex now parses user-supplied text |
| Multi-error detail | `"Card declined: insufficient funds, retry after 2026-04-01"` — one message, three meanings |
| Provider passthrough | `"Your card was declined"` (Stripe) becomes your contract by accident |

### What to branch on instead

Use a **hierarchy**, from most stable to least:

```text
1. code        → the condition            (append-only, stable)
2. type        → the problem class         (RFC 9457 URI, stable)
3. status      → the HTTP semantics        (stable per code)
4. errors[]    → field-level validation    (structured)
5. detail      → human prose              (MAY change; never branch)
```

If the information you need is not in levels 1–4, **the contract is missing a field**. Adding a
structured field is an additive change; branching on prose is a latent outage.

```ts
// ❌ Fragile: breaks on a wording change, on localisation, on interpolation.
if (err.detail?.includes("timed out")) return retry();

// ✅ Robust: a code, plus a structured field for the varying part.
if (err.code === "EXPORT_STORAGE_UNAVAILABLE") {
  return retryAfter(err.errors?.[0]?.details?.retryAfterSeconds ?? 30);
}
```

### Keeping messages out of the logic

Enforcement is mechanical, not cultural:

- **Lint rule:** flag string comparisons against `detail`/`title`/`message`.
- **Type rule:** model the human-facing text as a **message key**, not a string, so the client
  resolves it locally and the server never ships prose into logic.

```ts
// The server sends a key; the client owns the words.
type ClientAction = "retry" | "reauthenticate" | "fix_input" | "choose_alternative"
                   | "contact_support" | "none";

// detail is prose for humans; code + action are for machines.
interface ErrorResponse {
  code: string;
  type: string;
  status: number;
  title: string;
  detail: string;
  instance?: string;
  errors?: FieldError[];
}
```

> ⚠️ **Hazard.** A message that contains user input, a provider's raw text, or an internal
> identifier is not only unstable — it is a **disclosure channel** (Chapter 34). Branching on
> it also means reflecting untrusted content into your logic.

## Worked example — an AgentRun that kept its contract

`AgentRun` calls an LLM provider. The provider's errors arrive as prose:

```text
"rate limit exceeded for model gpt-x"
"Your input exceeded the context window"
"tool 'search' returned a non-JSON payload"
```

Acme's first implementation embedded the provider's text in `detail` and let the frontend
branch on it. When the provider changed `"rate limit exceeded"` to `"too many requests"`, the
Acme dashboard stopped counting rate-limit failures and the on-call engineer saw a silent drop
in volume for six days.

The contract fix:

- Provider prose → `detail` (truncated, sanitised), for humans only.
- Provider conditions → Acme codes: `AGENT_PROVIDER_RATE_LIMITED`,
  `AGENT_CONTEXT_LENGTH_EXCEEDED`, `AGENT_TOOL_OUTPUT_INVALID`.
- Each code carries a stable `type` URI: `/problems/agent-provider-rate-limited`.
- Retry decisions read the **code**, never the prose.

The provider can reword everything it likes; Acme's contract does not move.

## Key data / numbers

- **One contract owner per surface**, named as a team; one steward per code family.
- **Code family transfer keeps meanings intact** — a reorganisation is not a breaking change.
- **Contract document fields:** code · since · status · type URI · retryable · idempotent ·
  clientAction · messageKey · description · deprecated/replacedBy · owner.
- **Guarantee vs observation:** document guarantees for what you control; observations belong
  in runbooks, not in contracts.
- **Message hierarchy:** `code` > `type` > `status` > `errors[]` > `detail` (last one is prose).
- **Message key, not message:** the client resolves localized text; the server ships the key.
- **RFC 9457 `type`:** one URI per problem class, root-relative by default
  (`/problems/agent-provider-rate-limited`); `title` fixed per type, `detail` per occurrence.

## Real-world use case — ExportJob

Acme's `ExportJob` API returned `detail: "Export could not be generated"` for a storage
outage, a column-mapping bug, and a tenant quota breach. The web dashboard matched
`detail.includes("could not be generated")` to show "retry" — so a permanent mapping bug was
retried 12 times by three customers, and a quota breach was retried forever.

The contract work:

- Three codes with three meanings: `EXPORT_STORAGE_UNAVAILABLE` (retryable),
  `EXPORT_MAPPING_INVALID` (permanent, `clientAction: "contact_support"`),
  `EXPORT_QUOTA_EXCEEDED` (`clientAction: "none"`).
- A `type` URI per class under `/problems/…`, one per code family.
- A `clientAction` field so the dashboard no longer needs to reason about prose — it maps the
  action directly to a button label.
- A lint rule blocking string comparisons against `detail` in the frontend package.

Result: permanent failures stopped being retried, and the "unknown error" bucket in Acme's
support dashboard fell from 11% of jobs to under 1%, because the codes were finally
distinguishable.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Document only guarantees | No false promises | Less informative for consumers | Public contracts |
| Document behaviour too | More useful docs | Creates traps; readers rely on it | Runbooks, not contracts |
| Branch on messages | Zero schema work | Breaks on wording, leaks, localises badly | Never |
| Structured `clientAction` field | Clients stop interpreting | One more field to maintain | Any surface with a UI |
| Message keys resolved client-side | Proper localisation | Needs a catalog | Multi-language products |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name one owning team per contract | Let contracts be "owned by the backend team" |
| Have a steward per code family | Leave a family with no steward |
| Document guarantees, not observations | Promise the typical status for a condition |
| Version the contract document | Rewrite the contract doc without a bump |
| Branch on `code`, then `type`, then `status` | Branch on `detail` or `title` |
| Ship message keys, resolve client-side | Ship English prose as the contract |
| Treat a code-family transfer as meaning-preserving | Rename codes during a reorg |

## Common mistakes

- **The message contract** — clients regex prose; a reword breaks them silently.
- **The promise you do not control** — "validation failures are always 422" becomes false.
- **The ownerless catalogue** — anyone can change anything.
- **The org reorg rename** — codes renamed because the team moved.
- **The unversioned document** — nobody knows which promise they are reading.
- **The English-only contract** — non-English users get an unmatchable message.

## Checklist

- [ ] Each surface has exactly one owning team and a named escalation path.
- [ ] Each code family has a steward.
- [ ] The contract document lists guarantees, and observations live elsewhere.
- [ ] Every public code row carries status, `type`, retryability, action, owner, and `since`.
- [ ] The document has its own version and changelog.
- [ ] No consumer branches on `detail`, `title`, or `message` text.
- [ ] Missing machine-readable information is added as a structured field, not parsed from prose.

## Related

- [Evolution Rules and Compatibility](./02-evolution-rules-and-compatibility.md)
- [Contract Surfaces and Stability Guarantees](./01-contract-surfaces-and-stability.md)
- [Durable vs Ceremonial Rules](../02-deep-dive/03-durable-vs-ceremonial-rules.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Chapter 34 — Security Principles for Error Handling](../../../part-13-security-aware/34-security-principles-for-error-handling/README.md)
