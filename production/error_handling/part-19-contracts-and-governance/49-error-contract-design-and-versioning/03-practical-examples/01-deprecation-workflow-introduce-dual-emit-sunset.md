# The Deprecation Workflow: Introduce → Dual-Emit → Sunset

> Part XIX · Chapter 49 · Sections 49.7–49.11 · _Estimated reading time: 22 min_
> **Prerequisite:** [Deprecation Mechanics and Windows](../02-deep-dive/01-deprecation-mechanics-and-windows.md)

## In one sentence

A deprecation is a **five-phase workflow** — introduce, dual-emit, measure, sunset, remove —
where each phase has a defined artifact, a defined gate, and a named owner, and no phase is
skipped because "the date arrived".

## Why this matters in production

Most deprecations fail at the same place: **phase 3**. The change is made, the announcement is
sent, and then everyone assumes the ecosystem has adapted. Nobody measures who is still
depending on the old behaviour, so the code is removed on schedule and an unmonitored consumer
breaks.

The workflow below is written so that each phase produces an artifact you can point at in a
code review. It is intentionally bureaucratic in exactly one place — the gates — and
deliberately lazy everywhere else.

## Phase 0 — Triage: is this a deprecation at all?

| Situation | Action |
| --------- | ------ |
| New condition, no predecessor | **Add a code.** No deprecation needed (additive change) |
| Same condition, different wording | Change the wording. No deprecation |
| Same condition, different status | **New code + deprecation of the old** |
| Same condition, different name | **New code + alias + deprecation** |
| One condition becomes two | **Keep the old as umbrella + add two new codes** |
| Condition disappears entirely | **Deprecate, then remove after the window** |

The triage output is a one-line decision: *"additive"* or *"breaking, new code `X` replaces
`Y`"*. Write it in the PR description. If the line says "additive", there is no deprecation
workflow to run.

## Phase 1 — Introduce

Artifacts: registry entry, `type` URI, mapping, catalogue entry, unit test.

```ts
// registry/errors.ts
export const REGISTRY = {
  // The OLD code: unchanged meaning, unchanged status. It is now scheduled for removal.
  EXPORT_FORMAT_UNSUPPORTED: {
    domain: "EXPORT",
    category: "validation",
    http: 422,
    retryable: false,
    visibility: "public",
    clientAction: "contact_support",
    messageKey: "errors.export.formatUnsupported",
    description: "The requested export format is not supported.",
    owner: "data-team",
    since: "2024-11",
    deprecated: {
      since: "2026-05-06",
      replacedBy: "EXPORT_COLUMN_MAPPING_INVALID",
      sunset: "2026-09-01",
      reason: "Split into precise conditions; 422 → per-condition codes.",
    },
  },

  // The NEW code: precise meaning, new type URI, new catalogue entry.
  EXPORT_COLUMN_MAPPING_INVALID: {
    domain: "EXPORT",
    category: "validation",
    http: 422,
    retryable: false,
    visibility: "public",
    clientAction: "contact_support",
    messageKey: "errors.export.columnMappingInvalid",
    description: "One or more requested columns could not be mapped to the export schema.",
    owner: "data-team",
    since: "2026-05-06",
  },
} as const;
```

Checks at this phase:

- [ ] The old code's **meaning and status are untouched**.
- [ ] The new code has a `type` URI in the catalogue (`/problems/export-column-mapping-invalid`).
- [ ] The new code is emitted by exactly one code path (the serializer), not by hand.
- [ ] A test asserts the old code still maps to `422` and the new code maps to `422`.

## Phase 2 — Dual-emit

Artifacts: serializer change, legacy-field handling, telemetry for both codes.

```ts
// The canonical code is always in `code`; the legacy code rides along in a
// supplementary field so existing consumers keep their branch working.
const LEGACY_OF: Partial<Record<ErrorCode, string>> = {
  EXPORT_COLUMN_MAPPING_INVALID: "EXPORT_FORMAT_UNSUPPORTED",
};

export function toProblem(err: AppError): ErrorResponse {
  const body: ErrorResponse = {
    code: err.code,
    type: TYPE_BY_CODE[err.code],
    status: STATUS_BY_CODE[err.code],
    title: TITLE_BY_CODE[err.code],
    detail: safeDetail(err),
    instance: err.requestId,
  };
  const legacy = LEGACY_OF[err.code];
  if (legacy) body.legacyCode = legacy;
  return body;
}
```

**Telemetry for both.** The measurement phase reads two series:

```text
error.code.emitted{code="EXPORT_COLUMN_MAPPING_INVALID"}
error.code.consumed{code="EXPORT_FORMAT_UNSUPPORTED"}   ← the one that gates removal
```

If your telemetry only counts emissions, you can never observe the end of consumption, because
you keep emitting the legacy code while dual-emitting.

**Announcement.** Same day as the dual-emit deploy:

```text
To: partners@, api-announce@
Subject: [Deprecation] EXPORT_FORMAT_UNSUPPORTED → EXPORT_COLUMN_MAPPING_INVALID
Body:
  The error code EXPORT_FORMAT_UNSUPPORTED is deprecated and will be removed on 2026-09-01.
  New responses include code=EXPORT_COLUMN_MAPPING_INVALID (HTTP 422, unchanged status).
  Responses also carry the legacy code in the "legacyCode" field until removal.
  No action is required to keep working; to migrate, branch on the new code.
  Sunset date: 2026-09-01. Contract version: 1.5.0 (MINOR — additive).
```

## Phase 3 — Measure

Artifact: a measurement snapshot attached to the removal PR.

```text
Snapshot date        2026-08-01
Consumers of legacy  3 partners · 6.2% of export failures
  - partner A: nightly export script        4.1%
  - partner B: dashboard widget             1.7%
  - partner C: internal ops tool            0.4%
Consumers in-app     0.9% (mobile v3.2 and earlier)
Removal eligible?    NO — consumption > 0
```

Rules for the measurement:

- **Measure consumption, not emission.** Consumption = a consumer branched on the code.
- **Measure for at least one full window** before declaring the code removable.
- **Segment by consumer** where you can. "Partner A at 4.1%" is actionable; "6.2% total" is
  not.
- **Record the source of the data.** When someone asks "how do you know nobody uses it?", the
  answer is a query and a date, not a memory.

## Phase 4 — Sunset

Trigger: consumption has reached the threshold for the window (here: < 0.1% for 30 days).

Artifacts: dual-emit removed, sunset headers emitted, changelog updated, second announcement.

```ts
// Phase 4: the legacy code is no longer produced, but is still accepted on input
// and still mapped, so anything echoing it keeps working.
const LEGACY_OF: Partial<Record<ErrorCode, string>> = {}; // emptied
```

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json
Deprecation: @1767225600
Sunset: Tue, 01 Sep 2026 00:00:00 GMT
Link: <https://api.acme.example/problems/export-format-unsupported>; rel="sunset"
```

Note what Phase 4 does **not** do: it does not delete the registry row, the alias, or the
mapping. The code moves to **RETIRED** — recognised, documented, no longer produced.

## Phase 5 — Remove

Trigger: 30 consecutive days at zero consumption *after* Phase 4.

Artifacts: registry row deleted, alias deleted, catalogue regenerated, contract version MAJOR
(or a scheduled MAJOR), changelog entry.

```text
2026-10-01  REMOVED.
  - registry row EXPORT_FORMAT_UNSUPPORTED deleted
  - alias EXPORT_FORMAT_UNSUPPORTED → EXPORT_COLUMN_MAPPING_INVALID deleted
  - catalogue and generated SDK types regenerated
  - changelog: contract 2.0.0 (MAJOR) — removed EXPORT_FORMAT_UNSUPPORTED
  - the 2.0.0 release is the first one where the code cannot appear in a response
```

Removal is the only irreversible phase, which is why it is the only one gated on evidence.

## Variant — changing an HTTP status

The same workflow applies, with one extra constraint: **the HTTP status belongs to the code**.

```text
OLD: EXPORT_QUOTA_EXCEEDED  → 422   (validation framing)
NEW: EXPORT_QUOTA_EXCEEDED  → 403   (entitlement framing)  ← breaking

Correct handling:
  - do NOT change the status on the existing code
  - add EXPORT_ENTITLEMENT_MISSING with 403
  - keep EXPORT_QUOTA_EXCEEDED at 422 until it is removed
  - during dual-emit, the response carries ONE status (the new one) plus legacyCode
    → consumers that branch on the legacy code must also branch on the new status
    or on the clientAction field; document this explicitly
```

The one thing that cannot be dual-emitted is the status itself, because a response has exactly
one status code. That is the mechanical reason a status change always needs a new code.

## Key data / numbers

- **Phases:** 0 triage · 1 introduce · 2 dual-emit · 3 measure · 4 sunset · 5 remove.
- **Window:** 90 days for T2/T3 surfaces, 30 days for T1; the window starts at announcement.
- **Removal threshold:** consumption < 0.1% of the affected traffic, then **30 consecutive days**
  at zero before the registry row is deleted.
- **Dual-emit field:** one supplementary legacy field, removed with the legacy code.
- **Contract bumps:** additive (new code) → MINOR; removal → MAJOR; wording → PATCH.
- **Headers:** `Deprecation` (epoch seconds), `Sunset` (HTTP-date), `Link rel="sunset"`.
- **Rule of one:** an HTTP response carries exactly one status code — a status change always
  requires a new code.

## Real-world use case — Checkout

Acme's `Checkout` returned `PAYMENT_CARD_DECLINED` with HTTP `402` for every issuer decline. A
partner needed to distinguish *insufficient funds* (the customer can top up) from *expired
card* (the customer must update details), and asked for separate codes.

Acme's temptation was to add a field to the response — `declineReason: "expired_card"` — which
would have been additive and safe. It was rejected because the issuer's decline reasons are
enumerated by the payment provider, and a provider adding a new reason would silently break
every consumer that switches exhaustively over that field.

Instead they used codes:

```text
Introduce  PAYMENT_CARD_INSUFFICIENT_FUNDS (402, /problems/payment-insufficient-funds)
           PAYMENT_CARD_EXPIRED           (402, /problems/payment-card-expired)
Dual-emit  both new codes, legacyCode = PAYMENT_CARD_DECLINED
Measure    3 weeks: legacy consumed by 2 partners and the mobile app
Sunset     dual-emit stopped 2026-08-01; Deprecation + Sunset headers emitted
Remove     2026-10-15 after 30 days at zero consumption
```

Throughout the window, `PAYMENT_CARD_DECLINED` continued to mean exactly one thing — "the
issuer declined the card" — which is why the partner's existing branch kept working. The
precision the partner wanted arrived without a single consumer changing code.

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write the triage decision in the PR | Start editing a public code "quickly" |
| Freeze the old code's meaning and status | Improve the deprecated code in the same PR |
| Emit and measure both codes | Measure only the new code |
| Start the window at announcement | Start the window at the deploy |
| Delete the registry row only after the window | Delete the row when the dual-emit stops |
| Add a new code for a status change | Change the status in place |
| Regenerate the catalogue from the registry | Edit the catalogue by hand |

## Common mistakes

- **The single-step deprecation.** New code and old code removed in the same deploy.
- **The consumption-blind removal.** "Nobody complained" is not telemetry.
- **The meaning drift.** The deprecated code quietly got clearer or vaguer mid-window.
- **The status mutation.** The one thing dual-emission cannot carry.
- **The hand-edited catalogue.** The published contract drifts from the registry within weeks.
- **The announcement nobody receives.** Sent to a mailing list that stopped being read in 2024.

## Checklist

- [ ] The triage decision (additive vs breaking) is written in the PR.
- [ ] The old code's meaning and status are unchanged.
- [ ] The new code has a `type` URI, a `clientAction`, and a catalogue entry.
- [ ] Dual-emission is implemented in one place and telemetry counts both codes.
- [ ] The announcement went out on the day of the dual-emit deploy.
- [ ] Measurement is by consumer, with a date and a query recorded.
- [ ] Removal is gated on 30 days at zero consumption after sunset.
- [ ] The catalogue and generated types are regenerated, never hand-edited.

## Related

- [Deprecation Mechanics and Windows](../02-deep-dive/01-deprecation-mechanics-and-windows.md)
- [Evolution Rules and Compatibility](../01-concepts/02-evolution-rules-and-compatibility.md)
- [The Error Contract Spec and the ADR That Adopted It](./02-error-contract-spec-and-adr.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
