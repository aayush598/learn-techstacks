# Chapter 49 — Reference

> Part XIX · Chapter 49 · Error contract versioning guide, decision tables, and glossary.

## Cheat sheet — contract anatomy

```text
contract:
  surface      public-api
  tier         T3
  version      1.4.0
  owner        api-platform
  since        2025-03-03
  typeUriBase  /problems
  windowDays   90
  removalGate  30 consecutive days at zero consumption
```

## Cheat sheet — per-code contract row

```text
code · type URI · http status · retryable · idempotent · clientAction · messageKey
     · description · owner · since · deprecated{ since, replacedBy, sunset } · removedIn
```

## Decision table — change → compatibility → mechanism

| Change | Breaking? | Contract bump | Mechanism |
| ------ | --------- | ------------- | --------- |
| Add a code | No | MINOR | Register, document, emit |
| Add an optional field | No | MINOR | Additive serialization |
| Add a `type` URI | No | MINOR | New problem class |
| Reword `title` / `detail` | No | PATCH | Free |
| Correct a description | No | PATCH | Documentation |
| Rename a code | **Yes** | MAJOR | New code + alias + dual-emit |
| Repurpose a code | **Yes** | MAJOR | New code; deprecate the old |
| Change a code's HTTP status | **Yes** | MAJOR | New code with the new status |
| Change a code's retryability | **Yes** | MAJOR | New code |
| Remove a code | **Yes** | MAJOR | Deprecate → sunset → remove |
| Add/remove a `clientAction` value | **Yes** | MAJOR | New contract version |
| Make a field required | **Yes** | MAJOR | New contract version |
| Remove or retype a field | **Yes** | MAJOR | New contract version |

## Decision table — semver for the contract

| Bump | Trigger | Consumer impact |
| ---- | ------- | --------------- |
| PATCH | Wording, descriptions, docs | None |
| MINOR | New code, new optional field, new `type` | None (if consumers tolerate unknowns) |
| MAJOR | Removal, rename, re-meaning, re-status, enum change | Migration required |

## Decision table — stability tier

| Tier | Consumer | Guarantee | Window | Approval |
| ---- | -------- | --------- | ------ | -------- |
| T0 | Same process | None | — | — |
| T1 | Another team / module | Append-only within a version | 30 days | Team review |
| T2 | First-party web/mobile | Append-only; status frozen; unknown tolerated | 90 days | Contract owner |
| T3 | Public / partners | Semver-guaranteed; published catalogue | ≥ 90 days | Owner + review + changelog |

## Decision table — deprecation state

| State | Produced | Mapped | Accepted on input | Gate to advance |
| ----- | -------- | ------ | ----------------- | --------------- |
| ACTIVE | Yes | Yes | Yes | — |
| DEPRECATED | Yes (or dual-emitted) | Yes | Yes | Owner approval + changelog + announcement |
| RETIRED | No | Yes | Yes (alias) | 30 days at zero consumption |
| REMOVED | No | No | No | One further window at zero |

## Decision table — HTTP status changes

| Situation | Correct action |
| --------- | -------------- |
| Status is wrong for a new code | Set it correctly on the new code |
| Status of an existing public code is wrong | New code with the correct status; deprecate the old |
| Status differs between surfaces (API vs webhook) | Different contracts, different codes |
| Status differs between contract versions | Allowed inside a MAJOR version |

## Cheat sheet — `type` URI conventions (RFC 9457)

```text
/problems/{problem-class}          root-relative, version-independent, one per class
/problems/{domain}-{condition}     kebab-case, ASCII, ≤ 64 chars
about:blank                       only for genuinely untyped problems

MUST:  one `type` per class · stable across contract versions · no host · no API version
MUST NOT:  version the URI · rename a class in place · encode a code string
```

## Cheat sheet — header fields

| Header | Standard | Meaning |
| ------ | -------- | ------- |
| `Error-Contract-Version` | private | Contract version that produced this response |
| `Deprecation` | RFC 9745 | Epoch seconds; the resource/contract is deprecated |
| `Sunset` | RFC 8594 | HTTP-date; when the deprecated behaviour is removed |
| `Link rel="sunset"` | RFC 8594 | Link to the deprecation notice |
| `Retry-After` | HTTP semantics | Delay before retrying; not a deprecation signal |
| `Content-Type: application/problem+json` | RFC 9457 | Media type of the error body |

## Cheat sheet — the five-phase deprecation workflow

```text
0 TRIAGE     additive? → ship.  breaking? → new code replaces old.
1 INTRODUCE  registry row · type URI · mapping · catalogue · test. Old code frozen.
2 DUAL-EMIT  canonical code + legacy field; telemetry on both; announce today.
3 MEASURE    consumption by consumer; record the query and the date.
4 SUNSET     stop dual-emitting; Deprecation/Sunset headers; state = RETIRED.
5 REMOVE     after 30 days at zero: delete row + alias; regenerate catalogue; MAJOR bump.
```

## Decision table — unknown codes

| Role | Obligation |
| ---- | ---------- |
| Consumer | Default branch; generic message; safe action; never throw |
| Consumer (inbound) | Canonicalise or default; never throw |
| Producer | Never emit an unregistered code; never reuse a removed code |
| Producer (observability) | Emit a metric for every unknown code seen |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| Error contract | The set of promises a producer makes about the failures it emits |
| Contract surface | Where an error crosses a boundary: internal, module, service, backend↔frontend, public |
| Stability tier | T0 unstable · T1 internal-stable · T2 consumer-stable · T3 public |
| Contract owner | The single team that approves changes to a contract |
| Code steward | The owner of a family of codes |
| Additive change | A change old consumers tolerate (add code, add optional field, reword) |
| Breaking change | A change old consumers do not tolerate (rename, re-meaning, remove, re-status) |
| Dual-emission | Emitting the canonical code plus the legacy code during a window |
| Alias | Accepting a retired code on input and mapping it to the canonical one |
| Retirement | Stopping production of a code while keeping its mapping and alias |
| Consumption telemetry | Evidence that a consumer branched on a code |
| Sunset header | HTTP header announcing when deprecated behaviour will be removed |
| Error contract version | The semver of the contract, independent of API and package versions |
| Unknown code | A code a consumer does not recognise; must degrade, never throw |
| Guarantee | A binding promise about the contract's behaviour |
| Observation | Non-binding description of typical behaviour |

## Standard references (by name, no links)

- **RFC 9457** Problem Details — `type`, `title`, `status`, `detail`, `instance`; media type
  `application/problem+json`.
- **RFC 9745** — the `Deprecation` HTTP response header field.
- **RFC 8594** — the `Sunset` HTTP response header field and `Link rel="sunset"`.
- **HTTP `Retry-After`** — delay before a retry; used with `429` and `503`.
- **SemVer** — MAJOR.MINOR.PATCH semantics, applied to contracts and packages.
- **Chapter 8** — code naming, registry structure, and code-level deprecation.

## Signposts

- Codes and registries → [Ch. 8](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- Problem Details body → [Ch. 20](../../../part-08-http-and-api/20-standardized-api-error-responses/README.md)
- HTTP status semantics → [Ch. 19](../../../part-08-http-and-api/19-http-error-semantics/README.md)
- Frontend alignment → [Ch. 38](../../../part-14-frontend-and-full-stack/38-full-stack-error-contracts/README.md)
- Org-wide standards → [Ch. 50](../50-error-handling-as-an-engineering-standard/README.md)

## Related

- [Chapter 49 Do's and Don'ts](../04-dos-and-donts/README.md)
- [The Error Contract Spec and the ADR That Adopted It](../03-practical-examples/02-error-contract-spec-and-adr.md)
- [Chapter 49 Overview](../README.md)
