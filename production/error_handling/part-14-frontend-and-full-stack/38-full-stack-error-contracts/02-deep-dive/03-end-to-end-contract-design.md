# End-to-End Error Contract Design

> Part XIV · Chapter 38 · Section 38.14 · _Estimated reading time: 16 min_
> **Prerequisite:** [All Chapter 38 concepts](../README.md)

## In one sentence

**Design an end-to-end contract** that defines envelope, codes, versioning, extensibility, correlation, and deprecation — contract is code, tested across frontend/backend, and safe for unknowns.

## Contract elements

| Element | Requirement | Notes |
| ------- | ----------- | ----- |
| **Envelope** | RFC 9457 Problem Details + extensions | `type`, `title`, `status`, `detail`, `instance`, `error_id`, `code` |
| **Error codes** | Shared enum, stable | Additive, versioned on breaking change |
| **Field errors** | `invalid_params[]` with `field`, `code`, `message` | Support nested paths |
| **Correlation** | `error_id`, `traceId`/`requestId` | Link FE logs to BE logs |
| **Versioning** | API version header or URL version | Breaking envelope changes need version bump |
| **Extensibility** | Allow extra fields, ignore unknown | Forward-compatible |
| **Security** | No stack traces/secrets in envelope to clients | Diagnostics separate |
| **i18n** | Codes only for user messages | Never rely on server `detail` |

## Versioning strategy

| Change | Safe? | Action |
| ------ | ----- | ------ |
| Add new code | Yes (additive) | FE ignores unknown if not mapped (fallback) |
| Add optional field | Yes | FE ignores unknown |
| Change code meaning | **No** | Deprecate old code, add new code + version window |
| Rename field | **No** | Add new field, deprecate old, version if required |
| Change status semantics | **No** | New code or API version |

## Contract tests

```ts
// Contract test example
test('unknown code falls back safely', () => {
  const p = { status: 500, code: 'NEW_UNKNOWN_CODE', error_id: 'e1', detail: 'internal' };
  const actions = mapProblemToUi(p);
  expect(actions[0].kind).toBe('fallback');
  expect(actions[0].errorId).toBe('e1');
});

test('422 maps to fields', () => {
  const p = { status: 422, code: 'VALIDATION_FAILED', invalid_params: [{field:'email', code:'EMAIL_TAKEN'}] };
  const actions = mapProblemToUi(p);
  expect(actions[0]).toMatchObject({kind:'field', field:'email'});
});
```

## Real-world use case

**Acme SaaS** publishes error contract in OpenAPI extensions; FE/BE use shared types, contract tests block breaking changes, unknown codes logged with `error_id`.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Unversioned, implicit | Fast | Breaks clients | Never |
| Explicit contract + versioning | Safe evolution | Governance overhead | **Recommended default** |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Version on breaking changes | Silently break old clients |
| Contract tests in CI | Rely on manual integration |
| Unknowns → safe fallback + log | Crash on unknown code/field |
| Correlation via error_id/traceId | Only rely on stack traces |

## Checklist

- [ ] Envelope documented and shared
- [ ] Code registry with ownership/deprecation
- [ ] Versioning policy enforced
- [ ] Contract tests pass
- [ ] Forward/backward compatibility defined

## Related

- [Aligning Taxonomies and Shared Codes](../01-concepts/01-aligning-taxonomies-shared-codes.md)
- [Unknown Codes, Version Incompatibility](../01-concepts/03-unknown-codes-version-incompatibility.md)
- [End-to-End Contract Reference](../05-reference/README.md)
