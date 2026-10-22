# Do / Don't — Reusable Error-Handling Infrastructure

> Part XXI · Chapter 54 · _Reference list of rules for packages, adapters, and versioning_

## Packaging

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ship a package with one core and one adapter per vendor | Ship a framework with plugins and a config file |
| Keep the core free of vendor and framework imports | Import a Stripe SDK in the core |
| Keep the export surface at or below 25 symbols | Export every helper "for convenience" |
| Keep the package stateless | Add runtime configuration flags |
| Version the package with semver and publish a changelog | Ship breaking changes as a patch |
| Document the deprecation window in the package | Remove a code in a minor release |

## Core library

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Keep the core to types, factories, interfaces, and tables | Put application logic in the core |
| Make the category table total (`Record<Category, Policy>`) | Leave a category to be decided at the boundary |
| Redact context by allowlist inside the factory | Redact at the boundary where it can be forgotten |
| Serialise the cause into a structured record | Attach a native `Error` and hope it survives a queue |
| Keep the error type immutable | Mutate an error after creating it |
| Throw on an unregistered code | Default an unknown code to `internal` silently |
| Let consumers add codes, not categories | Let a consumer define its own category table |

## Adapters

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Implement the shared `ErrorMapper` interface | Write ad-hoc `instanceof` checks at call sites |
| Give every adapter a timeout, a retry policy, and a fallback | Let the adapter retry forever |
| Put the vendor-specific knowledge in the adapter | Put the vendor's error names in the core |
| Keep the HTTP adapter free of stack traces and internal messages | Add `stack: err.stack` "just for debugging" |
| Give the job adapter a fixed field set and three statuses | Let job failures carry arbitrary shapes |
| Classify a duplicate-key violation as a dependency error and let the domain decide | Map every SQLSTATE to a domain code |

## Policies

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry only idempotent operations | Retry a write that may have succeeded |
| Honour `Retry-After` when the provider sends it | Ignore the server's backoff hint |
| Bound retries with a total deadline, not just an attempt count | Retry until the request times out |
| Put the shared policies in the package and the local ones in the service | Put a service's special case in the shared table |
| Preserve the original error after the last attempt | Replace it with "retries exhausted" |

## Versioning and adoption

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify a change as additive, behaviour-changing, or breaking | Decide the version number after the diff is written |
| Ship a migration table with every major | Ship a major with a prose changelog |
| Give deprecated codes at least two minor releases | Remove a code in the same release that deprecates it |
| Publish deprecation telemetry to the consumers | Remove a code and find out who used it from a crash |
| Generate per-language clients from one contract | Hand-maintain the same table in three languages |
| Keep a starter template under 15 files | Ship a 47-file "standard project" template |
| Re-sync copied templates on a fixed cadence | Assume a copied template stays current |
| Record a deviation from the shared contract in one file | Let deviations live in code |

## Common mistakes

- **The core that imports a framework.** The first consumer on a different framework cannot
  use the package, and the framework's upgrade cycle becomes everyone's.
- **The category per service.** A service that defines its own category table re-creates the
  original divergence problem *inside* the package.
- **The mutable error.** An error enriched after creation can have a log line and a response
  body that disagree.
- **The catch-all core.** The moment the core contains an "application errors" section, it is
  an application, not a core.
- **The silent major.** A status change shipped as a patch, and the divergence was found by
  a client six weeks later.
- **The fork that was not a fork.** `packages/errors` copied into a service, edited, and
  described in a comment as "temporary".

## Review checklist

- [ ] The core imports no vendor SDK and no web framework.
- [ ] The export surface is ≤ 25 symbols.
- [ ] The category table is total.
- [ ] The factory redacts by allowlist and truncates the cause.
- [ ] An unregistered code throws at creation time.
- [ ] Every adapter declares a timeout, a retry policy, and a fallback.
- [ ] The HTTP adapter contains no stack traces or internal messages.
- [ ] The job adapter produces one of three statuses with a fixed field set.
- [ ] The change is classified as additive, behaviour-changing, or breaking.
- [ ] A breaking change ships with a before → after migration table.
- [ ] A deprecated code survives at least two minor releases.
- [ ] Consumers add codes, not categories.

## Related

- [Chapter 54 — Reusable Error-Handling Infrastructure](../README.md)
- [Infrastructure Reference](../05-reference/README.md)
- [The Starter Template and Customization Rules](../02-deep-dive/02-starter-template-and-customization-rules.md)
