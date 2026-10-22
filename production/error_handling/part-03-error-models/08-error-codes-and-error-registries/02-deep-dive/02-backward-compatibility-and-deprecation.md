# Backward Compatibility and Deprecation Mechanics

> Part III · Chapter 8 · Sections 8.15–8.16 · _Estimated reading time: 17 min_
> **Prerequisite:** [Deprecating Codes, Compatibility, and Detection](../01-concepts/05-deprecation-compatibility-and-detection.md)

## In one sentence

Backward compatibility means **old clients keep working when codes change**, and deprecation
mechanics are the staged, telemetry-gated process that lets you retire a code without a support
incident.

## Why this matters in production

Your server evolves faster than your clients. A mobile app from eighteen months ago, a partner
integration, an internal dashboard, a webhook consumer — all may still branch on codes you want to
change. Breaking them turns an internal refactor into a customer-visible outage. Compatibility and
deprecation are how you make code changes safe across a versioned world.

## The compatibility matrix

| Producer change | Old client behavior | Safe? | Mitigation |
| --------------- | ------------------- | ----- | ---------- |
| Add a new code | Falls back on unknown | ✅ | Ensure graceful fallback |
| Change a code's message | Ignores (uses own UI) | ✅ | Never a contract |
| Change a code's HTTP status | Behavior may change | ⚠️ | New code, not a status change |
| Rename a code | Unknown code | ❌ | Alias + dual-emit window |
| Change a code's meaning | Wrong handling | ❌ | New code; deprecate old |
| Remove a code | Unknown on input | ❌ | Retire, then remove after telemetry |

The rule: **additive is safe; reductive/repurposing is a versioned migration.**

## Producer-side mechanics

### 1. Dual emission during a rename

```ts
function emitDeprecated(err: AppError, sink: ErrorSink): void {
  sink.emit(err); // canonical (new) code
  const old = OLD_OF_NEW[err.code as ErrorCode];
  if (old) sink.emit({ ...toClientJSON(err), code: old }); // legacy consumers
}

const OLD_OF_NEW: Partial<Record<ErrorCode, string>> = {
  USER_NOT_FOUND: "USER_DOES_NOT_EXIST",
};
```

Emit both for a window; measure; stop when the old code's consumption falls to zero.

### 2. Alias acceptance on input

```ts
const ALIASES: Record<string, ErrorCode> = {
  USER_DOES_NOT_EXIST: "USER_NOT_FOUND",
  WEBHOOK_ERROR: "WEBHOOK_PROCESSING_FAILED",
};

function acceptIncoming(raw: string): ErrorCode {
  if (raw in REGISTRY) return raw as ErrorCode;   // canonical
  return ALIASES[raw] ?? "INTERNAL_UNEXPECTED";   // legacy or safe fallback
}
```

If a client sends an old code back (some APIs echo codes), canonicalize it.

### 3. Deprecation metadata in the registry

```ts
USER_DOES_NOT_EXIST: {
  // ...full entry...
  deprecated: {
    since: "2026.03",
    replacedBy: "USER_NOT_FOUND",
    removeAfter: "2026.09",
    reason: "Renamed for consistency with USER_* domain.",
  },
},
```

Generated docs render a deprecation banner; a lint can warn when new code emits a deprecated code.

## Consumer-side mechanics

Consumers must be **forward-compatible**: they tolerate codes they have never seen.

```ts
type KnownCode = keyof typeof REGISTRY;

function handleClientError(code: string): { message: string; action: ClientAction } {
  const entry = (REGISTRY as Record<string, CodeEntry>)[code];
  if (!entry) {
    return { message: t("errors.internal.unexpected"), action: "contact_support" };
  }
  return { message: t(entry.messageKey), action: entry.clientAction };
}
```

Rules for consumers:

- **Never `throw` on unknown codes.** Fall back to a generic message and a safe action.
- **Never assume the full code set.** A server may add codes without a client release.
- **Branch on `code`, not on messages** (messages change freely).
- **Pin to a documented behavior**, and use a "unknown → generic" mapping for anything else.

## Telemetry-gated removal

Removal is safe only with data.

```text
TRACK:  error.code.consumed   { code }    // from clients, dashboards, partners
GATE:   remove code only when consumption = 0 for 30 consecutive days
ACT:    mark RETIRED (keep alias) → after another cycle, REMOVE
```

```ts
function canRemove(code: ErrorCode, windowDays = 30): boolean {
  const stats = telemetry.query(`error.code.consumed{code="${code}"}`, { lastDays: windowDays });
  return stats.max === 0;
}
```

> ⚠️ **Hazard.** "We announced it" is not telemetry. Clients you cannot see (cached mobile apps,
> partner scripts, internal tools) will break silently unless you measure consumption.

## Worked example — full lifecycle

```text
2026.01  REGISTER USER_DOES_NOT_EXIST (public).
2026.03  Register USER_NOT_FOUND. Mark USER_DOES_NOT_EXIST deprecated{replacedBy: USER_NOT_FOUND}.
         Emit BOTH from the boundary. Docs show a migration note.
2026.04  Telemetry: USER_DOES_NOT_EXIST consumed by mobile v3.0–v3.2 (~4% traffic).
2026.06  Mobile v3.2 < 0.1%. Stop emitting USER_DOES_NOT_EXIST. Keep alias on input.
2026.09  Zero consumption for 30 days. Mark RETIRED. Keep alias.
2026.12  REMOVE from registry + alias. Update generated docs + changelog.
```

Every step reversible until the final removal; every step backed by a metric.

## Key data / numbers

- **Deprecation windows:** external clients **90 days** (announce + dual-emit), internal **30
  days**; keep alias through the window.
- **Telemetry gate:** zero consumption for **30 consecutive days** before removal.
- **Dual-emit cost:** doubles error-emission volume for affected codes; acceptable for the window.
- **Alias map:** a small runtime `Record<string, ErrorCode>`; remove entries with the code.
- **Forward-compat fallback:** every consumer needs one; unknown → generic message + safe action.

## Real-world use case — WebhookIngest

Acme renamed `WEBHOOK_SIGNATURE_FAILED` to `WEBHOOK_SIGNATURE_INVALID`. A partner integration
consuming their webhook errors keyed on the old code and silently sent all failures to a "unknown
error" bucket. Because Acme had **dual-emitted** during the deprecation window, the partner saw no
breakage; telemetry showed the old code still consumed for six more weeks, delaying removal until
the partner updated. Without the compatibility window, the partner's error handling would have
quietly degraded the day of the rename.

## Trade-offs

| Strategy | Safety | Cost | When to use |
| -------- | ------ | ---- | ----------- |
| Dual-emit + alias | Highest | Extra volume, longer tail | Public/partner codes |
| Alias only | High | Simpler | Internal codes |
| Hard cutover | None | Zero | No known consumers (rare) |
| Never remove | Total | Unbounded registry | Very small systems |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Dual-emit during a rename window | Rename in one deploy |
| Gate removal on consumption telemetry | Remove because "we announced it" |
| Keep aliases until zero consumption | Delete the alias with the code |
| Make consumers forward-compatible | Throw on unknown codes |
| Version meaning via a new code | Repurpose an existing code |

## Common mistakes

- **Hard rename** with no alias/dual-emit.
- **Removal without telemetry**, breaking invisible consumers.
- **Repurposing** a deprecated code with new meaning.
- **Clients that crash** on unknown codes.
- **Alias deleted too early**, so an old client's input becomes `INTERNAL_UNEXPECTED`.

## Checklist

- [ ] Do all changes follow the compatibility matrix (additive or versioned)?
- [ ] Are deprecated codes dual-emitted or aliased through a window?
- [ ] Is removal gated on 30-day zero-consumption telemetry?
- [ ] Are consumers forward-compatible with unknown codes?
- [ ] Is deprecation metadata in the registry and generated docs?
- [ ] Is there a changelog entry for each rename/removal?

## Related

- [Deprecating Codes, Compatibility, and Detection](../01-concepts/05-deprecation-compatibility-and-detection.md)
- [Registry-as-Code and Collision Testing](./01-registry-as-code-and-collision-testing.md)
- [Chapter 49 — Error Contract Design and Versioning](../../../part-19-contracts-and-governance/49-error-contract-design-and-versioning/README.md)
