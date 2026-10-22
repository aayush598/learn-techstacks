# Localization, Diagnostics vs User Messages

> Part XIV · Chapter 38 · Sections 38.12–38.13 · _Estimated reading time: 14 min_
> **Prerequisite:** [Mapping API→UI](../01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md)

## In one sentence

**Separate concerns strictly:** user-facing messages are localized and safe (keyed by error code), diagnostics are for logs/telemetry (include `error_id`, traceId, stack, request context) and must never leak PII or internals to end users.

## Localization (38.12)

| Practice | Guidance |
| -------- | -------- |
| **Key by code** | `errors.codes.SLUG_TAKEN` not server strings |
| **Fallbacks** | Code → English default → generic safe message |
| **Parameterization** | Interpolate safely; never interpolate raw server details |
| **RTL/pluralization** | Use ICU/messageformat as needed |
| **Consistency** | Same keys across web/mobile |

## Diagnostics vs User Messages (38.13)

| Aspect | User Messages | Diagnostics |
| ------ | ------------- | ----------- |
| **Audience** | End user | Support/eng/on-call |
| **Content** | Actionable, safe, localized | Full context, `error_id`, traceId, correlationId, stack, route, userId hash, request id |
| **Source** | Frontend i18n + code mapping | `componentDidCatch`, API errors, global handlers |
| **PII** | **Never** | Minimize, hash/redact |
| **Leakage** | Must be safe | Stored in secure logs/telemetry |

```ts
// Safe user message
function getUserMessage(p: ProblemDetails, locale: string) {
  const code = p.code;
  const key = `errors.codes.${code || 'UNKNOWN'}`;
  return i18n.t(key, { defaultValue: i18n.t('errors.codes.UNKNOWN') });
}

// Diagnostics
function report(p: ProblemDetails | Error, ctx: Ctx) {
  telemetry.capture({
    error_id: (p as any).error_id,
    traceId: ctx.traceId,
    code: (p as any).code,
    route: ctx.route,
    status: (p as any).status,
    componentStack: ctx.componentStack,
    // no PII
  });
}
```

## Real-world use case

500 from **ExportJob**: user sees "Something went wrong. Try again. Reference ID: err_abc123" (localized, safe). Support looks up `err_abc123` + traceId in logs for full details.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Use server messages directly | Quick | Not localized, may leak details | Never for users |
| Separate by code + diagnostics | Safe, localizable, debuggable | More work | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Localize by error code | Show raw exception/stack to users |
| Include `error_id` on unrecoverable for support | Include emails/tokens/PII in client-visible messages |
| Log full diagnostics server-side/telemetry | Trust `p.detail` as user copy |

## Checklist

- [ ] All user messages keyed by code + i18n
- [ ] `error_id`/traceId used for correlation
- [ ] PII redaction in diagnostics
- [ ] Safe fallbacks for unknown locales/codes

## Related

- [Mapping API→UI](../01-concepts/02-mapping-api-to-ui-and-validation-to-fields.md)
- [Unknown Codes, Version Incompatibility](../01-concepts/03-unknown-codes-version-incompatibility.md)
- [Chapter 37 — Render Failures/Boundaries](../../37-frontend-error-handling/02-deep-dive/04-render-failures-and-outside-boundaries.md)
