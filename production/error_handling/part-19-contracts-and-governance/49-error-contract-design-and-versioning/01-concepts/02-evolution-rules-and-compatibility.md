# Evolution Rules and Compatibility

> Part XIX · Chapter 49 · Sections 49.7–49.13 · _Estimated reading time: 22 min_
> **Prerequisite:** [Contract Surfaces and Stability Guarantees](./01-contract-surfaces-and-stability.md)

## In one sentence

Every change to an error contract is either **additive** (safe) or **breaking** (a versioned
migration), and compatibility is a two-way obligation: a new consumer must read old producers,
and an old consumer must survive new producers.

## Why this matters in production

Chapter 8's registry told you *what* the codes are. This file tells you **what you are allowed
to do to them** — and the answer is short enough to memorise:

| Change | Breaking? | Why |
| ------ | --------- | --- |
| Add a new code | No | Consumers must tolerate unknown codes |
| Change message wording | No | Messages are not contract |
| Change a code's HTTP status | **Yes** | Clients branch on status (retry vs not) |
| Rename a code | **Yes** | Consumers branch on the code string |
| Change a code's meaning | **Yes** | Consumers branch on the meaning |
| Remove a code | **Yes** | Consumers branch on the code string |
| Add an optional response field | No | Additive |
| Remove or retype a field | **Yes** | Consumers parse it |
| Change a code's retryability | **Yes** | Consumers derive retry policy from it |

Everything else is interpretation. Teams get this wrong because the changes *feel* small: "I
just changed 422 to 409" reads like a status tweak and behaves like a silent behaviour change
in every client that treats 4xx as terminal.

## 49.7 — Adding codes safely

Adding a code is the **only** free change, and it is only free if consumers are already
forward-compatible.

Rules for the producer:

- **One condition, one code.** Never add a code that is a synonym of an existing one.
- **Add the code to the registry *before* it can be thrown.** A registry-first rule (enforced in
  CI) means an added code is already mapped to a status, a retry policy, and a message.
- **Never reuse a retired code.** A retired code keeps its alias forever, precisely so nobody
  can reuse the string with different meaning.
- **Do not encode conditions in the code string.** `PAYMENT_CARD_DECLINED_2` is not a code.

Rules for the consumer (the half people skip):

- **Every code lookup has a default branch.** A `switch` with no `default` is a latent crash.
- **Unknown codes map to a generic safe state**, not an exception and not a blank screen.

## 49.8 — Deprecating codes

Deprecation is a **state**, not an event. The lifecycle and its gates are in
[the deep dive](../02-deep-dive/01-deprecation-mechanics-and-windows.md); the contract-level
rules are:

- A deprecated code **keeps working**: it is still produced (if consumers need it), still
  mapped, still documented with a replacement.
- A deprecated code **gains a replacement pointer** in the registry (`deprecated.replacedBy`).
- A deprecated code is **never repurposed**. New meaning ⇒ new code.
- Removal is **gated on consumption telemetry**, not on the calendar alone.
- Deprecating a code is a **T2/T3 change**: it requires the contract owner's approval and a
  changelog entry.

> ⚠️ **Hazard.** "Deprecation" without dual-emission is a rename with extra steps. If consumers
> need the old code to keep working, you must keep emitting it — announcing is not enough.

## 49.9 — Message wording changes

**Messages are never contract.** This is the single most useful rule in the chapter, because it
frees you to improve wording, localise, and personalise error messages without a migration.

| Change | Breaking? | Note |
| ------ | --------- | ---- |
| Reword `detail` | No | Always safe |
| Rewrite `title` | No | Per RFC 9457, `title` is per problem type, not per occurrence |
| Localise `detail` | No | Prefer a stable message **key**; localisation is the client's job |
| Add a field to `detail` (e.g. `remaining`) | No | Additive |
| Change `detail` to include internal identifiers | **Yes (security)** | Leaks internals; changes the contract's safety promise |

The corollary is a **prohibition**, not just a permission: consumers must never branch on
message text. If you find yourself matching `detail.includes("timed out")`, you need a code
(`EXPORT_STORAGE_UNAVAILABLE`) or a machine-readable field.

## 49.10 — HTTP mapping changes

Changing the status a code maps to is a **breaking change**, because clients derive behaviour
from it:

- A retrying client treats `503` as retryable and `422` as permanent. Changing
  `PAYMENT_CARD_EXPIRED` from `422` to `409` does not move a pixel in the UI — it changes
  whether the SDK auto-retries.
- A monitoring dashboard alerts on `5xx`. Changing a code from `500` to `422` silently removes
  it from an SLO.

The correct move is always the same: **introduce a new code with the new status and deprecate
the old one.** The old code keeps its old status until it is retired.

```ts
// ❌ Breaking: the same code now means a different thing to every client.
const REGISTRY_V2 = { PAYMENT_CARD_EXPIRED: { http: 409 } };  // was 422

// ✅ Safe: old code keeps its meaning; new code carries the new meaning.
const REGISTRY_V2 = {
  PAYMENT_CARD_EXPIRED: { http: 422, deprecated: { replacedBy: "PAYMENT_CARD_EXPIRED_AT_CHECKOUT" } },
  PAYMENT_CARD_EXPIRED_AT_CHECKOUT: { http: 409 },
};
```

## 49.11 — Backward compatibility

**Backward compatibility** = *a new consumer can correctly consume data produced by an older
producer.*

In error terms: the new frontend can still read errors from the old API version; the new
service version can still consume errors from the old service version; the new SDK can still
handle a code from the old server.

Mechanisms:

| Producer side | Consumer side |
| ------------- | ------------- |
| Keep emitting old codes during a window | Keep recognising old codes on input (aliases) |
| Add new fields, never remove | Tolerate missing optional fields |
| Freeze old contracts inside old versions | Default to the old contract when negotiation fails |

Backward compatibility is achieved **in the producer's repository history**: v1 of the API keeps
its error mapping frozen, so a v2 consumer that still calls v1 keeps working.

## 49.12 — Forward compatibility

**Forward compatibility** = *an old consumer can correctly consume data produced by a newer
producer.*

This is the direction teams forget, and it is the one that actually breaks people in the field,
because the new producer is already deployed and the old consumer is on someone's phone.

Requirements on the producer:

- **Additive only** within a contract version: new codes, new optional fields.
- **Never repurpose or remove** within a version.

Requirements on the consumer:

- **Unknown codes are handled**, not fatal.
- **Unknown fields are ignored**, not rejected.
- **Unknown enum values** fall back to a safe default.

## 49.13 — Unknown codes

An unknown code is **normal**, not exceptional. It appears because:

- The consumer is older than the producer.
- The code came from a service that upgraded ahead of the contract.
- The code was hand-crafted, injected by a proxy, or read from a stored job payload.
- The producer emitted a code that was never registered (a bug — see
  [Chapter 8 §8.18](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)).

Consumer obligation:

```ts
type KnownCode = keyof typeof REGISTRY;

function describe(code: string): { message: string; action: ClientAction } {
  const entry = (REGISTRY as Record<string, CodeEntry>)[code];
  if (!entry) {
    // Safe fallback: a generic message, an action that is always safe, and a
    // telemetry signal so the gap is visible to the producer.
    telemetry.increment("error.code.unknown_seen", { code });
    return { message: t("errors.internal.unexpected"), action: "contact_support" };
  }
  return { message: t(entry.messageKey), action: entry.clientAction };
}
```

Producer obligation: **never crash on an unknown code received on input.** If a client sends a
code back (some APIs echo it), canonicalise it or fall back to a safe value — never throw.

## How it works — classifying a change before you ship it

```text
1. Does the change remove, rename, repurpose, or re-status an existing code?
      → BREAKING. New code + deprecation of the old one.
2. Does it change what a code means (retryability, user action, semantics)?
      → BREAKING. New code + deprecation of the old one.
3. Does it remove or retype a field of the error body?
      → BREAKING. New major contract version.
4. Does it only add a code, add an optional field, or reword a message?
      → ADDITIVE. Ship it; ensure consumers have a default branch.
5. Is it a public/T2 surface?
      → Any of the above still requires owner approval + changelog.
```

## Worked example — the status change that broke a partner

```text
Acme's public API returned 422 for "seat count exceeds plan limit".
Partner code (Java SDK v2):

  if (status == 422) { showFormError(); }        // correct today
  else if (status >= 500) { scheduleRetry(); }    // 422 was never retried

Acme wants 409 CONFLICT, because it is a state conflict, not a validation failure.
```

**Step 1 — classify.** Changing the status of a public code is breaking (it changes client
retry and branch behaviour).

**Step 2 — do not mutate.** Introduce `PLAN_SEAT_LIMIT_EXCEEDED` with `409`, keep
`VALIDATION_SEAT_LIMIT` at `422`, and mark the latter deprecated.

**Step 3 — dual-emit.** For 90 days the endpoint returns the **new** code with the **new**
status while continuing to accept the old code on inbound requests.

**Step 4 — publish.** Changelog entry, migration note, and a `Deprecation` header on responses
that still carry the deprecated code.

**Step 5 — measure.** Consumption telemetry for `VALIDATION_SEAT_LIMIT` drops to zero over the
window; removal is scheduled only after 30 further days at zero.

The partner changed one branch and kept everything else.

## Key data / numbers

- **Free change:** add a code · add an optional field · reword a message.
- **Breaking change:** rename · repurpose · remove · change HTTP status · change retryability
  · change a required field.
- **Deprecation window:** **90 days** for T2/T3 surfaces, **30 days** for T1.
- **Telemetry gate:** **30 consecutive days** of zero consumption before removal.
- **Dual-emission:** keeps both codes observable; doubles the emission count for the affected
  code during the window only.
- **Status semantics used by clients:** `4xx` = client-fixable, `5xx` = retryable,
  `429` = back off (`Retry-After`), `409` = state conflict, `422` = semantically invalid.
- **RFC 9457 `type`:** unchanged by a status change — `type` identifies the problem *class*,
  `status` the HTTP semantics. A status change with the same `type` is still breaking.

## Real-world use case — WebhookIngest

Acme's `WebhookIngest` returns `400` for a Stripe signature mismatch and for a malformed
payload. A partner's handler branched on the **status**: `400` → drop the event, `409` → park
it for replay.

Acme's support team wanted `409` for signature failures (replayable) and `400` for malformed
payloads (not replayable). Because both lived under the same status, the partner could not
distinguish them at all — a defect that had been silently discarding replayable events.

The fix was a **contract change, not a status change**:

- Added `WEBHOOK_SIGNATURE_INVALID` (409, `type: "/problems/webhook-signature-invalid"`)
  alongside the existing `WEBHOOK_SIGNATURE_FAILED` (400).
- Added `WEBHOOK_PAYLOAD_MALFORMED` (400, `type: "/problems/malformed-request"`).
- Left the existing code untouched — no repurposing, no status change — so no partner broke.
- Ran a 90-day dual-emit window, measured partner consumption of the legacy code, and only
  then scheduled its retirement.

Two new codes and one untouched code solved a problem that a status change would have turned
into a partner outage.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Add-only, never deprecate | Zero breakage | Registry grows unbounded; meanings drift | Tiny internal systems |
| New code + dual-emit + retire | Correct and safe | Effort, extra emission, longer tail | Public and partner surfaces |
| Change in place (status or meaning) | Fast | Silently breaks consumers | Never, on T2/T3 |
| Version the whole API to fix one code | Simple mental model | Massive blast radius for a small change | Only when many things change together |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every change as additive or breaking | Change a public code's status in place |
| Introduce a new code for a new meaning | Repurpose a retired or deprecated code |
| Keep the old code alive during the window | Delete the old code on the announcement date |
| Gate removal on consumption telemetry | Remove because "we announced it" |
| Have a default branch for every code lookup | Let an unknown code throw |
| Treat message wording as free | Let clients match on message text |
| Document the deprecation in the changelog | Deprecate silently in a refactor |

## Common mistakes

- **The "harmless" status change** — a 4xx→4xx change that flips client retry behaviour.
- **The renamed code** — no alias, so every consumer's branch falls through to a default.
- **The repurposed code** — same string, new meaning, wrong branch taken silently.
- **The strict consumer** — `switch` without `default`; crashes on the first new code.
- **The calendar-only deprecation** — removed on schedule while a partner still used it.
- **The message contract** — a client regexes `detail` and breaks when you reword.

## Checklist

- [ ] Every proposed contract change is classified additive or breaking.
- [ ] Breaking changes produce a **new** code; the old one keeps its meaning.
- [ ] Every code lookup has a default branch with a safe fallback.
- [ ] Unknown inbound codes are canonicalised or defaulted, never thrown.
- [ ] Message wording is free to change; no consumer branches on it.
- [ ] Status changes are treated as breaking, with a new code.
- [ ] Removal is gated on 30 days of zero consumption telemetry.

## Related

- [Contract Surfaces and Stability Guarantees](./01-contract-surfaces-and-stability.md)
- [Ownership, Documentation, and Message Independence](./03-ownership-documentation-and-message-independence.md)
- [Deprecation Mechanics and Windows](../02-deep-dive/01-deprecation-mechanics-and-windows.md)
- [Versioning Error Contracts](../02-deep-dive/02-versioning-error-contracts.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
