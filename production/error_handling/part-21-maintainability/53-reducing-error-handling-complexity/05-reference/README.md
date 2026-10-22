# Chapter 53 — Reference

> Part XXI · Chapter 53 · Worksheets, decision tables, thresholds, and the chapter glossary.

## Cheat sheet — the duplication report

```text
DECISION                    COPIES  LOC SAVED IF EXTRACTED   DRIFT OBSERVED
pg unique → conflict          4          40 LOC             yes (400 vs 409)
provider 429 → retry          3          25 LOC             yes (Retry-After ignored)
http status by category       2          30 LOC             no
retry attempts by category    3          20 LOC             yes (3 vs 5 vs 5)
```

Columns: **decision** (the question) · **copies** · **LOC saved** · **drift observed**.
A row with `drift: yes` is a defect that already reached production.

## Cheat sheet — the duplication report procedure

```text
  1. Pick a question, not a file.
  2. Find the sites:  rg "23505|P2002|statusCode|maxAttempts"
  3. Record each answer.  (the answers will not match)
  4. Decide: delete | delegate | extract | keep-and-document.
  5. Verify with one test asserting all sites agree.
```

## Cheat sheet — the three-question fast filter

| Question | Pass condition | Fail ⇒ |
| -------- | -------------- | ------ |
| Does the decision have a natural key? | code, category, provider, dependency | Keep it inline |
| Do all call sites answer the same question about that key? | yes | Extract the key, not the answer |
| Would a new call site need a new argument? | no, a new key | Stop — you are building a config surface |

## Cheat sheet — the abstraction cost analysis

```text
  COST (what you add)                BENEFIT (what you remove)
    A1  implementation lines            B1  duplicated lines removed
    A2  call-site changes (×2)         B2  decision sites collapsed (×2)
    A3  new concepts (×3)              B3  drift risk removed (×3)
    A4  indirection per reader         B4  onboarding time saved
    A5  maintenance cost               B5  review time saved

  A = A1 + 2·A2 + 3·A3 + A4 + A5
  B = B1 + 2·B2 + 3·B3 + B4 + B5
  NET = A − B   →   accept when NET ≤ 0
```

## Cheat sheet — break-even thresholds

| Threshold | Value |
| --------- | ----- |
| Minimum call sites for an extraction | **3** |
| Minimum LOC saved to justify an extraction | **80** |
| Maximum new concepts in one extraction | **1** |
| Maximum parameters in a policy object | **5** |
| Maximum indirection depth | **1 hop** |
| Re-analysis trigger | call sites exceed 2× the original count |
| Drift evidence required for the benefit | **1 observed** divergence |

## Decision table — shape choice

| Situation | Shape | Example |
| --------- | ----- | ------- |
| Same subject, same question, ≥ 3 sites | **table** | `CATEGORY_HTTP` |
| Precedence genuinely matters | predicate chain | first-match-wins mapping |
| Behaviour varies by runtime state | strategy | per-tenant override |
| Two sites, different needs | **no abstraction** | request fails fast, job retries |
| New failure mode added to an interface | **re-scope to a map** | `FALLBACKS[category]` |

## Decision table — decision site → owner

| Question | Owner | Shape |
| -------- | ----- | ----- |
| What category is this? | domain registry | `Record<code, Category>` |
| What does the client see? | platform mapping | `Record<Category, {status, publicCode}>` |
| Is it retryable? | platform policy | `Record<Category, RetryPolicy>` |
| What is the recovery? | platform policy | `Record<Category, Recovery>` |
| What is attached? | platform enrichment | allowlist of context keys |
| What does this vendor error mean? | the provider adapter | `Record<vendorCode, Category>` |
| What is the fallback? | the provider adapter | `Record<Category, Fallback>` |

**One question, one owner.** Two owners for one question is a defect.

## Cheat sheet — the change cost of growth

| Event | Files | Target |
| ----- | ----- | ------ |
| Add a new error code | 2–3 | ≤ 3 |
| Add a new provider | 3–5 | ≤ 5 |
| Add a new failure mode to a dependency | 1 (adapter) | 1 |
| Change a status for one category | 1 (mapping table) | 1 |
| Change a retry limit | 1 (policy table) | 1 |
| Add a new job type | 2–3 | ≤ 3 |

## Cheat sheet — the complexity budget

```yaml
features:
  checkout:
    max_error_files: 3
    max_error_lines: 120
    max_decision_sites: 6
    max_failure_branch_ratio: 0.20
```

| Feature shape | Decision sites | Error lines |
| ------------- | -------------- | ----------- |
| Simple CRUD | 3–4 | ≤ 60 |
| Checkout / payments | 6–8 | ≤ 120 |
| Background export | 6–8 | ≤ 150 |
| Webhook ingest | 5–7 | ≤ 120 |
| LLM agent | 8–10 | ≤ 180 |

## Cheat sheet — the cost ledger row

```yaml
- subject: "Postgres unique violation → conflict"
  key: category
  shape: table
  net_score: -41
  call_sites: 4
  re_analyse_when: "call sites exceed 8"
  owner: platform
  added: "2026-03-11"
```

## Cheat sheet — the check rules (CI-enforceable)

```text
  error-code-unregistered      a thrown code has no registry row
  registry-incomplete          a category has no row in the status table
  status-literal-outside-map   res.status(4xx) in a feature file
  decision-site-budget         a feature exceeds its decision-site budget
  error-file-budget            a feature exceeds its error-file budget
  provider-leak                a feature imports a provider SDK
  outcome-not-mapped           an outcome variant has no mapping arm
```

## Cheat sheet — limits and defaults

| Limit | Value |
| ----- | ----- |
| Nesting depth in error handling | ≤ 2 (0 inside policy functions) |
| Branches per decision site | ≤ 4 |
| Lines per decision site | ≤ 20 |
| Failure branches in business logic | ≤ 20% of the function's lines |
| `ProblemStatus` union size | 14 status codes |
| Domain codes per union file | ~40 (typed factory) |
| Tables per domain | 1 registry; shared category tables in the platform layer |
| Retry attempts per policy | ≤ 5 |
| Retry budget | ≤ 10% of request volume |
| Check runtime | < 10 s |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Decision site** | A place in the code that answers a failure question (category, status, retry, recovery, context) |
| **Duplication report** | The list of decisions made in more than one place, with copy counts and observed drift |
| **Policy** | A named, table-driven answer to "what should happen for this kind of failure" |
| **Extraction** | Replacing repeated decisions with one shared decision |
| **Abstraction cost analysis** | The calculation that prices an extraction: added complexity vs removed complexity |
| **Vocabulary cost** | The ongoing cost of a new word every reader must learn; weighted 3× |
| **Removal test** | Paste the abstraction's body back at each call site; if no site gets worse, it was ceremony |
| **Exhaustiveness check** | A type-level or lint-level guarantee that every subject has a row |
| **Change cost** | The number of files that must change to add an error code or a provider |
| **Complexity budget** | A per-feature limit on error-handling files, lines, decision sites, and branch ratio |
| **Decision-site budget** | The budget dimension that directly measures duplication risk |
| **Failure-branch ratio** | Failure branches ÷ total lines in a feature; a measure of how buried the domain rule is |
| **Ledger row** | The repository record of an accepted abstraction: its score, owner, and re-analysis trigger |
| **Re-analysis trigger** | The condition that forces an abstraction to be re-scored, e.g. "call sites exceed 8" |
| **Default** | The conservative answer a policy gives when its subject is not listed |
| **Vendor-agnostic decision** | The decision that survives a change of vendor; what should actually be extracted |

## Related

- [Chapter 53 — Reducing Error-Handling Complexity](../README.md)
- [Abstraction Cost Analysis](../02-deep-dive/01-abstraction-cost-analysis.md)
- [A Complexity Budget for a Feature](../03-practical-examples/02-a-complexity-budget-for-a-feature.md)
- [Chapter 45 — Reference](../../part-17-organization/45-organizing-error-handling-modules/05-reference/README.md)
