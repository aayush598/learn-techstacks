# Chapter 30 — Do's and Don'ts

> Part XI · Chapter 30 · All sections

A condensed rule set distilled from the chapter. Use it as a degradation review checklist.

## Classification

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every capability as required/important/optional | Treat all dependencies as critical |
| Let product own the classification | Decide criticality only in code |
| Preserve correctness over completeness | Serve wrong data to stay available |
| Review classification on product changes | Set it once and forget |

## Fallback responses

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Label every degraded response | Present stale data as live |
| Return the same schema | Change the shape for fallbacks |
| Include `source` and `as_of` | Return a bare value |
| Prefer a correct degraded result | Invent data |
| Bound the fallback | Let it run unbounded |
| Make empty results distinguishable from failure | Return `[]` for everything |

## Cached fallbacks

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Set per-dataset stale tolerance | Use one TTL for all data |
| Write the cache only on success | Cache degraded responses |
| Include age in the response | Show "updated recently" |
| Fail closed when stale beyond tolerance | Serve week-old data silently |
| Use `stale-if-error` only for public content | Use it for balances or prices |

## Partial features and modes

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Define named levels with a matrix | Invent states during an incident |
| Shed non-essential work first | Disable auth or payments to save capacity |
| Defer work instead of dropping it | Fail exports silently |
| Cache feature flags (last-known) | Fail all flags on/off when flags are down |
| Use hysteresis between levels | Flap modes every few seconds |
| Surface mode in HTTP, UI, logs, metrics | Keep mode in a config file only |

## Fallback chains

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Share one deadline across the chain | Give each step a fresh timeout |
| Cap chain length at 2–4 | Let fallbacks recurse |
| Skip steps whose breaker is open | Try every step blindly |
| Record skipped steps | Swallow every failure |
| End in an explicit terminal error | Loop back to the primary |
| Test each step failing | Test only the happy path |

## Fail-open vs fail-closed

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Decide per capability, in writing | Use one global default |
| Fail closed for auth, payments, security | Fall back to stale permissions |
| Fail open for optional features | Hide required failures |
| Prefer last-known or local-fallback states | Assume a binary choice |
| Count and alert every fail-open | Allow invisible fail-open |
| Review after incidents | Treat the choice as permanent |

## Communication

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Use one header/field vocabulary | Invent a new field per endpoint |
| Make degraded markers machine-readable | Put prose in headers |
| Tell the user what is missing | Blank the widget silently |
| Give operators a single mode number | Require reading three dashboards |
| Keep internal provider names out of notices | Leak hostnames or stack traces |

## Observability and testing

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Count fallback use and failure | Wait for a customer report |
| Alert when a fallback itself fails | Alert only on 5xx |
| Inject faults for every level | Test only the happy path |
| Verify degraded paths in staging | Assume fallbacks work |
| Track stale-served data by age | Treat stale as fresh |

## Incident response

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Pin a higher level if auto is too low | Force normal while a dependency is down |
| Clear manual pins after recovery | Leave the system degraded for days |
| Verify mode on every surface | Update only the status page |
| Review the matrix in the postmortem | Blame the dependency only |
