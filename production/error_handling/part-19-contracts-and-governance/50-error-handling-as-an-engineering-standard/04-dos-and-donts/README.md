# Chapter 50 — Do's and Don'ts

> Part XIX · Chapter 50 · All sections

A condensed rule set for writing, enforcing, and evolving an error-handling standard.

## Writing the standard

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write a small set of numbered, enforceable rules | Write a handbook nobody can cite |
| Give each rule an id, a check, and a reason | Publish a rule with no way to verify it |
| Use MUST / MUST NOT / SHOULD / MAY deliberately | Use "should" for something that is binding |
| Specify observable behaviour, not implementation | Demand one library or one pattern |
| Label uncheckable guidance as guidance | Dress guidance up as a rule |
| Budget the number of rules and prune on evidence | Add a rule per incident forever |
| Name the failure each rule prevents | Cite "best practice" as the reason |

## Structure and naming

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every condition a registered, unique code | Invent a code string at the throw site |
| Name the condition, not the mechanism | Use `SELECT_USER_RETURNED_NO_ROWS` |
| Keep one error module per service | Scatter error classes across `utils/` |
| Make codes and messages part of the contract | Build a message from a template literal |
| Mark a retired code with its date and successor | Reuse a retired code for a new meaning |
| Keep severity out of the code | Encode `FATAL_USER_NOT_FOUND` |

## Propagation and translation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Translate upstream errors at your boundary | Re-export a provider's error verbatim |
| Attach the originating error as the cause | Flatten a dependency failure into a generic one |
| Make every deliberate ignore explicit and logged | Swallow an error in a `catch {}` |
| Report a partial failure as a partial failure | Return success after half the work failed |
| Propagate the request id through every layer | Start a new trace id in each service |

## Retry and timeout

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Retry only codes explicitly marked retryable | Retry everything that fails |
| Use a named policy from the shared registry | Write a literal attempt count in a call site |
| Cap attempts at 5 and the retry budget at 10% of the deadline | Let retries consume the whole request budget |
| Use exponential backoff with jitter | Use a fixed 1 s delay in a loop |
| Retry only idempotent work, or carry an idempotency key | Retry a charge because the response was slow |
| Time out a dependency before the caller's own deadline | Let one dependency hold the request open |

## Response format

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return the standard problem body | Invent a per-service error shape |
| Keep `4xx` actionable and `5xx` retryable | Return `400` for a server-side failure |
| Return `429` with `Retry-After` when throttling | Return `500` for throttling |
| Return all field-level validation details | Return only the first validation error |
| Say "not found" the same way for missing and invisible | Reveal whether an account exists |
| Put the request id in the response and the logs | Ask support to search for a message string |

## Recovery posture

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Declare fail-closed or fail-open per operation | Choose a posture per call site |
| Make a fail-open fallback observable | Fall back silently and hope nobody notices |
| Expose a degraded mode to the caller | Hide degradation from the API surface |
| Keep compensating actions idempotent | Retry a refund from an inconsistent state |
| Stop recovering at the declared ceiling | Keep compensating after the budget is gone |

## Security

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Mark the security floor as non-exceptable | Let a team waive a redaction rule locally |
| Keep stack traces, SQL, and hostnames out of responses | Return the raw exception message |
| Redact secrets before logging | Log the request body "for debugging" |
| Raise a security event for auth failures | Log a failed login as an ordinary error |
| Keep customer data out of the registry and the standard | Paste a real production example into the doc |

## Enforcement and exceptions

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Run a new rule in warning mode for two releases | Switch a rule on as an error on day one |
| Write the CI check before announcing the rule | Announce a rule with no enforcement |
| Keep every exception narrow, owned, and dated | File one exception for a whole service |
| Give every exception compensating controls | Treat an exception as a waiver |
| Break the build for expired exceptions | Renew exceptions silently |
| Express context differences as surface profiles | Bend a global rule to fit one caller |

## Change management

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Version the standard and publish a changelog | Edit the standard in a pull request |
| Give a tightening two releases of warning | Break every team in one release |
| Record rule decisions as ADRs | Let a meeting be the only record |
| Give a removal 90 days of notice | Remove a rule the day you dislike it |
| Retire a rule when its skip rate passes 20% | Keep a rule nobody applies |
| Review the whole standard quarterly | Review it only when it is convenient |

## Adoption — the reusable playbook (50.13)

The standard is not the deliverable; the **playbook** is. It is the same ordered steps, the same
artifacts, and the same rule ids in every repository, so a team that joins in year three runs the
same process as the team that founded it.

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Ship the playbook as the same files the CI checks read | Keep the playbook on a wiki page and the rules in the repo |
| Run the same six steps in the same order in every project | Invent a local onboarding checklist per service |
| Reuse the rule ids, the exception register, and the retry registry verbatim | Fork the rule catalogue so each project reads its own version |
| Start a new project at the latest published version | Ask a new project to port last year's version first |
| Measure adoption with the standard's own metrics | Measure adoption by counting who read the document |

The six steps, in order:

1. **Inventory** the error surface: every throw site, every exit path, every external call.
2. **Classify** each failure point by category, severity, and owner.
3. **Decide** the posture: fail, retry, compensate, degrade, terminate, or resolve later.
4. **Encode** the decision as a rule row, a registry entry, and a named error type.
5. **Enforce** it: a CI check for the mechanical rules, a review checklist for the rest.
6. **Measure** it: skip rate, exception count and age, time-to-close, and the error budget spent.

## One standard across many projects (50.14)

The same rules apply everywhere, but the *surface* may differ: a public API, a batch job, and a
webhook receiver do not emit the same response body. A **standard** fixes the rule and its id; a
**surface profile** fixes the shape.

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Publish one versioned standard that every project pins | Copy the document into each repository |
| Keep one rule id per rule, in every project | Renumber rules per project so reports cannot be compared |
| Express a different shape as a surface profile of the same rule | Edit the rule to fit one caller |
| Give each project an adoption level: advise, warn, then enforce | Enforce everywhere the day the standard is published |
| Publish a migration deadline per standard version | Let old versions live forever, unannounced |
| Let one team own the catalogue and the checks | Let every team own a copy of the checks |

## Anti-patterns in the wild

- **The Decorative Standard.** Sixty pages, four CI checks, quoted in two incident reviews it
  could not have prevented.
- **The Wall of Prose.** Every rule needs a paragraph of context, so none of them can be cited.
- **The Unnumbered Rule.** "Errors must be consistent" cannot appear in a review comment or a
  violation report.
- **The Exception Ratchet.** Each quarter adds exceptions and none close, because there is no
  expiry.
- **The Shadow Standard.** Forty approved exceptions, none expiring, none owned.
- **The Deadline Rule.** A rule that appeared as a build failure the same week it was proposed —
  and was skipped, filed around, and cited anyway.
- **The Silent Edit.** The standard changed in a pull request; one of two services learned
  about it from a failing build.
- **The Copy-Paste Fork.** Two teams each copied the standard into their repo and edited it.
- **The Standards Editor.** A rule that is edited the moment it catches a real problem, so it
  only ever catches hypothetical ones.

## Quick self-check

Before publishing or tightening a rule, answer these five questions:

1. **Can a tool check it?** If not, can a reviewer decide it in under a minute? If neither, it
   is guidance.
2. **What failure does it prevent?** If you cannot name one, delete the rule.
3. **Who is exceptable?** If the answer is "nobody", say so in the rule.
4. **What happens when it is violated?** A red build, a review comment, or nothing?
5. **When will we retire it?** A rule with no exit condition becomes folklore.

## Related

- [Chapter 50 — Error Handling as an Engineering Standard](../README.md)
- [Standards and ADR Templates](../03-practical-examples/01-standards-and-adr-templates.md)
- [Durable Rules, Exceptions, and Change Management](../02-deep-dive/01-durable-vs-ceremonial-rules.md)
- [Chapter 46 — Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
