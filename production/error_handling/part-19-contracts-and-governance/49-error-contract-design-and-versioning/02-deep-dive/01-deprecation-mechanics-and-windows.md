# Deprecation Mechanics and Windows

> Part XIX · Chapter 49 · Section 49.8 · _Estimated reading time: 20 min_
> **Prerequisite:** [Evolution Rules and Compatibility](../01-concepts/02-evolution-rules-and-compatibility.md)

## In one sentence

Deprecation is a **four-state lifecycle with gates**, where each transition has a required
action, a required announcement, and — for removal — a **telemetry proof** that nobody is still
depending on the old behaviour.

## Why this matters in production

A deprecation is a promise to your consumers: *this still works, and you have time to move.*
The failure modes are always the same two:

- **The promise is not kept.** The old code is deleted on the announcement date because the
  cleanup ticket said "remove deprecated code" — and a partner's integration dies at 02:00 on a
  Saturday.
- **The promise is kept forever.** The registry grows without bound, every developer is
  unsure which codes are current, and the "temporary" alias becomes permanent architecture.

The difference between these two outcomes is **mechanism**, not intention. This file is the
mechanism.

## The state machine

```text
        register            mark deprecated              stop emitting
ACTIVE ──────────▶ DEPRECATED ──────────────────▶ RETIRED ──────────────▶ REMOVED
   │                    │                             │                      │
   │                    │ dual-emit (if needed)       │ alias still          │ alias still
   │                    │ announce + changelog        │ accepted on input    │ removed too
   │                    │ monitor consumption         │ keep the mapping     │
   │                    │                             │                      │
   └─ never change meaning, never reuse the string ────────────────────────────┘
```

| State | Still produced? | Still mapped? | Still accepted on input? | Gate to advance |
| ----- | --------------- | ------------- | ------------------------ | --------------- |
| **ACTIVE** | Yes | Yes | Yes | — |
| **DEPRECATED** | Yes, or dual-emitted | Yes | Yes | Owner approval + changelog + announcement |
| **RETIRED** | No | Yes | Yes (alias) | Zero consumption for **30 consecutive days** |
| **REMOVED** | No | No | No | Zero consumption for another full window |

Two rules make the machine safe:

1. **Meaning is frozen at the moment of deprecation.** A deprecated code keeps the meaning it
   had when it was deprecated. Changing it later is a silent breaking change.
2. **Every transition is reversible until REMOVED.** If you discover a consumer you could not
   see, you can resume emitting.

## Window arithmetic

"How long?" is not a style choice — it is a function of two measurable things:

```text
window ≥ max(
    announcement + migration time,          # how long consumers need to notice and act
    consumer population × release cadence   # how long old clients stay in the wild
) + safety margin
```

| Consumer type | Migration time | Support tail | Recommended window |
| ------------- | -------------- | ------------ | ----------------- |
| Internal team, same deploy cycle | days | days | **30 days** |
| Other teams in the org, shared release train | 1–2 sprints | 1 quarter | **60–90 days** |
| First-party mobile app | 1 release cycle | **12 months** | **90–180 days** |
| Public API / partners | unknown | unknown | **≥ 90 days**, longer with a published sunset date |

The mobile row is the one teams get wrong. A mobile app version lives on customer phones for
years; a 90-day window does not mean "everyone upgraded", it means "everyone had a fair chance
to".

> ⚠️ **Hazard.** Windows are measured from **announcement**, not from the code change. If you
> ship the deprecation and the announcement in the same week, consumers get less than the
> window you think you gave them.

## Dual-emission mechanics

Dual-emission is how you keep a deprecated code *working* while introducing its replacement.
It works for **one-to-one** renames; it does not work for **splits** (one old code becoming two
new ones) — for those, the old code must remain as an umbrella until consumers migrate.

```ts
// Canonical code is what the contract now promises; the legacy alias is what
// existing consumers still recognise.
const LEGACY_ALIASES: Partial<Record<ErrorCode, string>> = {
  USER_DOES_NOT_EXIST: "USER_NOT_FOUND",
  WEBHOOK_SIGNATURE_FAILED: "WEBHOOK_SIGNATURE_INVALID",
};

function toPublicPayload(err: AppError): ErrorResponse {
  const canonical: ErrorResponse = {
    code: err.code,
    type: TYPE_BY_CODE[err.code],
    status: STATUS_BY_CODE[err.code],
    title: TITLE_BY_CODE[err.code],
    detail: safeDetail(err),
    instance: err.requestId,
  };

  const legacy = LEGACY_ALIASES[err.code];
  if (!legacy) return canonical;

  // Dual-emit: the canonical code is the contract; the legacy code is carried
  // in a non-authoritative field so old clients keep working.
  return { ...canonical, legacyCode: legacy };
}
```

Three rules make dual-emission honest:

- **The canonical code is the one in `code`.** The legacy string is supplementary; consumers
  that ignore it still get a valid, current contract.
- **Both codes are measured.** Consumption telemetry must count the legacy code, or you will
  "measure" zero while consumers still branch on it.
- **The legacy field is removed with the legacy code.** It is not permanent surface area.

### Alias acceptance on input

Some contracts echo codes back to the producer (a retry payload, a stored job, a partner
API). Canonicalise rather than reject:

```ts
function canonicalize(raw: string): ErrorCode {
  if (raw in REGISTRY) return raw as ErrorCode;            // canonical
  const inverse = INVERSE_LEGACY[raw];
  if (inverse) return inverse;                               // legacy → canonical
  telemetry.increment("error.code.unknown_received", { code: raw });
  return "INTERNAL_UNEXPECTED";                             // safe default
}
```

## The telemetry gate

Removal requires evidence. The measure is **consumption**, and consumption must be defined
precisely, because the obvious definition (we emit it) measures the wrong thing:

```text
❌ consumption = "we emitted this code"          → never reaches zero while dual-emitting
✅ consumption = "a consumer branched on it"     → what you actually care about
```

Signals that count as consumption:

| Signal | Where it comes from | Counts? |
| ------ | ------------------- | ------- |
| Client requests carrying the code as a value | API query logs, SDK telemetry | Yes |
| Client requests whose behaviour differs by the code | Hard to observe directly | Yes (proxy for the above) |
| A published endpoint that returns it | Response sampling | Yes |
| Internal dashboards reading it | Internal queries | Yes, but weighted lower |
| Partner scripts you cannot see | — | **No** — this is the blind spot |

Because there is always a blind spot, the gate is **conservative**:

```ts
function canRemove(code: string, windowDays = 30): boolean {
  const stats = telemetry.query(`error.code.consumed{code="${code}"}`, { lastDays: windowDays });
  if (stats.max > 0) return false;
  // Blind-spot guard: require the code to also be rare on the producer side.
  const emitted = telemetry.query(`error.code.emitted{code="${code}"}`, { lastDays: 7 });
  return emitted.max === 0;
}
```

## Signalling deprecation to consumers

Use the HTTP response header fields that exist for exactly this purpose, rather than inventing
a private header:

| Mechanism | Standard | Purpose |
| --------- | -------- | ------- |
| `Deprecation` response header | RFC 9745 | Marks the resource (or the contract) as deprecated |
| `Sunset` response header | RFC 8594 | Communicates the date/time when the deprecated behaviour will be removed |
| `Link` with `rel="sunset"` | RFC 8594 | Alternative to the `Sunset` header, linking to the deprecation notice |
| `Retry-After` response header | HTTP semantics | Not a deprecation signal — used when a request may be retried after a delay |

```http
HTTP/1.1 404 Not Found
Content-Type: application/problem+json
Deprecation: @1767225600
Sunset: Tue, 01 Sep 2026 00:00:00 GMT
Link: <https://api.acme.example/problems/user-not-found>; rel="sunset"
```

The timestamps are Unix epoch seconds for `Deprecation` and an HTTP-date for `Sunset`. Use them
to make the window machine-readable: a partner's tooling can schedule the migration for them.

## Deprecating a status mapping

A status change is the case where dual-emission cannot express the whole truth, because one
code cannot be both `422` and `409`. The mechanic that works:

```text
1. Keep the old code with its old status (400).
2. Add the new code with the new status (409).
3. During the window, emit the NEW code and the NEW status, and include the legacy code
   in the supplementary field so clients that branch on the legacy code still see it.
4. Clients that need the old status must key on the legacy code, not on the status.
```

This is why the compatibility matrix says a status change requires a new code: a single HTTP
response has exactly one status, and one status cannot express two contracts.

## Worked example — deprecating `EXPORT_FORMAT_UNSUPPORTED`

```text
2026-04-02  Registry: EXPORT_FORMAT_UNSUPPORTED (public, 422, since 2024-11).
            Owner: data-team. Contract owner: api-platform.

2026-05-06  Introduce EXPORT_COLUMN_MAPPING_INVALID (public, 422, new type
            /problems/export-column-mapping-invalid).
            Deprecate EXPORT_FORMAT_UNSUPPORTED → replacedBy the new code.
            Changelog + announcement to partners. Deprecation/Sunset headers added
            to responses still carrying the old code.

2026-05-06  Dual-emit active: responses carry code=EXPORT_COLUMN_MAPPING_INVALID
            and legacyCode=EXPORT_FORMAT_UNSUPPORTED.

2026-06-06  Measurement: legacy code consumed by 3 partners, 6% of export failures.
            Removal date 2026-08-04 confirmed; sunset date published.

2026-07-20  Consumption < 0.1%. Stop dual-emitting; legacy code now only accepted
            on input (alias) and only produced by the deprecated v1 endpoint.

2026-08-19  30 consecutive days at zero consumption → state RETIRED.
            Mapping kept; alias kept; docs show "retired, no longer produced".

2026-10-01  After one further full window at zero → REMOVED from the registry.
            Alias deleted. Docs and generated code updated.
```

Note what happened between 2026-05-06 and 2026-07-20: the **new** code was the contract the
whole time. Dual-emission was compatibility scaffolding, not the destination.

## Key data / numbers

- **States:** ACTIVE → DEPRECATED → RETIRED → REMOVED.
- **Windows:** T1 internal **30 days**; T2/T3 **90 days minimum**; mobile **90–180 days**;
  public APIs **≥ 90 days** with a published sunset date.
- **Telemetry gate:** zero consumption for **30 consecutive days** *and* zero emissions for
  **7 days** before RETIRED; another full window before REMOVED.
- **Headers:** `Deprecation` (RFC 9745), `Sunset` (RFC 8594), `Link rel="sunset"`.
- **Dual-emission cost:** doubles the emission count for the affected code during the window;
  acceptable and bounded by the window length.
- **Legacy alias retention:** keep the alias until the code is REMOVED — then delete both.
- **Version carrier:** `Sunset` uses an HTTP-date; `Deprecation` uses Unix epoch seconds.

## Real-world use case — ExportJob

Acme's `ExportJob` API had a public code `EXPORT_FORMAT_UNSUPPORTED` that conflated three
conditions: an unsupported CSV dialect, a column mapping that did not resolve, and a tenant
whose plan had no export entitlement. Support could not tell them apart, so a quota problem
arrived as a "format error" and the customer re-exported for an hour.

Acme's first instinct was to repurpose the code with three new meanings — impossible, one code
carries one meaning — so they added three codes and deprecated the umbrella:

- `EXPORT_FORMAT_UNSUPPORTED` → stays `422`, becomes the umbrella/legacy code.
- `EXPORT_COLUMN_MAPPING_INVALID` → `422`, permanent, `clientAction: "contact_support"`.
- `EXPORT_ENTITLEMENT_MISSING` → `403`, permanent, `clientAction: "none"`.

The umbrella could not be dual-emitted into three codes, so it was retained until telemetry
showed its consumption at zero for 30 consecutive days — which took two full cycles, because a
partner's script was reading it. After removal, "format error" tickets dropped to near zero
because each condition now had its own code, its own status, and its own runbook.

## Trade-offs

| Approach | Safety | Cost | When to use |
| -------- | ------ | ---- | ----------- |
| Dual-emit + alias + retire | Highest | Extra emission, longer tail, two names in docs | Public/partner codes |
| Alias only, no dual-emit | High | Consumers must handle two codes already | Internal codes |
| Hard cutover | None | Zero | Only with provably zero consumers |
| Never remove | Total | Unbounded registry, permanent confusion | Very small systems |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Measure from announcement, not from the change | Start the window on the deploy date |
| Gate removal on consumption telemetry | Remove because the date arrived |
| Keep the deprecated code's meaning frozen | Improve the deprecated code "while we're here" |
| Publish a sunset date in a standard header | Deprecate only in a changelog nobody reads |
| Keep the alias as long as the code exists | Delete the alias with the registry row |
| Dual-emit one-to-one renames | Try to dual-emit a one-to-many split |

## Common mistakes

- **The calendar removal.** The date arrives; consumers are still there.
- **The announcement-free deprecation.** A changelog entry on a page nobody reads.
- **The frozen-in-name-only deprecation.** The code is "deprecated" but its meaning quietly
  changed, so consumers react to the wrong thing.
- **The measurement mistake.** Measuring emissions instead of consumption.
- **The alias deleted too early.** An old client's inbound code becomes `INTERNAL_UNEXPECTED`.
- **The split dual-emit.** Emitting three codes where the client expects one — clients that
  take "the first error" now behave unpredictably.

## Checklist

- [ ] The deprecation state machine is implemented in the registry, not in prose.
- [ ] The window length is derived from the consumer population and release cadence.
- [ ] The announcement channel is identified and dated.
- [ ] Consumption telemetry counts consumer branching, not producer emission.
- [ ] Removal requires 30 days at zero consumption *and* zero emission.
- [ ] `Deprecation` / `Sunset` headers are emitted where the contract is deprecated.
- [ ] The deprecated code's meaning is frozen and the alias lives until REMOVED.

## Related

- [Evolution Rules and Compatibility](../01-concepts/02-evolution-rules-and-compatibility.md)
- [The Deprecation Workflow: Introduce → Dual-Emit → Sunset](../03-practical-examples/01-deprecation-workflow-introduce-dual-emit-sunset.md)
- [Versioning Error Contracts](./02-versioning-error-contracts.md)
- [Chapter 8 — Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
