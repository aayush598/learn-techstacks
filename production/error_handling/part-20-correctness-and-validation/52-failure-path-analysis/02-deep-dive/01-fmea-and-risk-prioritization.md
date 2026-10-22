# FMEA, the Failure-Mode Inventory, and Risk Prioritization

> Part XX · Chapter 52 · Sections 52.13–52.15 · _Estimated reading time: 24 min_
> **Prerequisite:** [Unhandled Paths, Nested Operations, Workflows, and Dependency Boundaries](../01-concepts/03-unhandled-nested-and-multi-step-paths.md)

## In one sentence

FMEA turns an enumerated failure matrix into a **ranked backlog**: every failure mode gets a
severity, an occurrence, and a detectability score, the product becomes an **RPN**, and the rows
that score highest become the work for the next sprint.

## Why this matters in production

A failure matrix with 40 rows is not a plan. It is a list, and lists do not get worked. The
matrix tells you *what exists*; something has to tell you *what to do on Tuesday*. Without
prioritisation, teams do what humans always do under pressure: they fix the failure they
remember, the one that happened to them, and the one that was easiest to reproduce. That is not
the same as the one that costs the most.

Prioritisation also makes the analysis **survivable**. The first analysis of a large flow finds
more than 100 candidate modes. Nobody maintains 100 rows, so the document decays and stops being
trusted. A scored list with a threshold can be **pruned honestly**: rows below the line are
accepted, monitored, and documented as known limitations.

## Core concept

### 52.13 — FMEA, applied to an operation

FMEA is a *failure mode and effects analysis*: for each failure mode, ask three questions.

| Factor | The question | 1 | 5 | 10 |
| ------ | ------------ | - | - | -- |
| **Severity** | How bad is the outcome if this happens? | Cosmetic message | Degraded feature | Money lost, data lost, or a security breach |
| **Occurrence** | How often does it happen? | Never observed | Weekly | Every call |
| **Detection** | How likely is it to escape unnoticed? | Caught by a test | Found in review | Found in production |

```text
RPN = severity × occurrence × detection        (each factor 1–10 → 1..1000)
```

Severity is the only factor that is mostly objective, and it is the one that decides the argument
when the other two are contested. Occurrence needs evidence: incident counts, alert rates, or a
code-reading argument for "has never happened". Detection asks a brutal question — *if this
happened tonight, would anybody know before a customer complained?*

Two adjustments keep the number honest:

- **Detection 10 for silent modes.** A mode that succeeds quietly and corrupts data is a 10,
  even if it is rare.
- **Occurrence 5 for "unmeasured".** If nobody has instrumented the path, 5 is the honest
  answer; 1 and 10 are both claims.

⚠️ **Hazard.** RPN is a *ranking device*, not a probability. Multiplying ordinal scales
produces a number with no units. Teams that treat RPN as a risk percentage end up defending
arithmetic instead of fixing systems.

### 52.14 — The failure-mode inventory

The matrix is an analysis artefact; the **inventory** is the durable artefact. It lives in the
repository, it has one row per failure mode, and it is the thing a CI check reads.

```yaml
# error-handling/failure-modes.yaml
failure_modes:
  - id: FM-004
    flow: checkout
    point: FP-04                    # chargeStripe
    mode: success_but_response_lost
    category: external_api_ambiguous
    recovery: resolve_later
    severity: 9
    occurrence: 4
    detection: 8
    rpn: 288
    risk: 16                       # severity(1-5) x likelihood(1-5)
    owner: payments
    status: open                    # open | mitigated | accepted | retired
    mitigation: resolve by Stripe charge id before retrying
    regression_test: checkout/ambiguous-charge.spec.ts
    last_reviewed: 2026-04-02
```

Six fields make it useful: **identity** (`id`, `flow`, `point`), **classification** (`mode`,
`category`, `recovery`), **scores** (`severity`, `occurrence`, `detection`, `rpn`, `risk`),
**ownership** (`owner`, `status`), and **evidence** (`mitigation`, `regression_test`,
`last_reviewed`). A row without `owner` is a wish; a row without `regression_test` is a promise
nobody has made yet.

The inventory has a **lifecycle**:

```text
  discovered ──▶ scored ──▶ open ──▶ mitigated ──▶ verified
      │             │          │           │            │
  an analysis    threshold   a sprint    a fix ships   a test proves it
  or an incident decides      item                        stays fixed
```

New rows enter from two directions: an **analysis** (a flow you have not modelled yet) and an
**incident** (a mode you did not know existed). An incident that does not become a row means the
same incident will happen again with the same mystery.

### 52.15 — Turning scores into a backlog

Two scores, two jobs. **Risk = severity × likelihood** (both 1–5, so 1..25) answers *how much
does this hurt and how often* — it decides the sprint priority. **RPN** adds detectability and
answers *how quietly would this fail* — it decides whether the fix is urgent even when the
frequency is unknown.

| Risk | Action |
| ---- | ------ |
| 15–25 | Fix in the current sprint; add a regression test |
| 8–14 | Schedule; add evidence in the meantime |
| 1–7 | Accept and monitor, or document as a known limitation |

| RPN | Action |
| --- | ------ |
| ≥ 400 | **Blocks the release.** Fix before shipping the change that touches this path |
| 200–399 | Needs a named owner and a dated mitigation plan |
| 100–199 | Backlog; revisit next quarter |
| < 100 | Accept, monitor, document |

The two scores disagree often, and the disagreement is the useful part. A row with **high
severity, low occurrence, and bad detection** (a lost charge response) scores badly on risk and
terribly on RPN — that is the row that stays unfixed in every organisation, and the row that
costs the most when it finally happens. Put it in the sprint anyway.

**Blast radius** is the third input, and it is not a number: how many customers, how much data,
and how long does it take to detect. Multiply the score by the radius in your head. A mode that
affects 40% of tenants outranks one that affects 1%, even at a lower RPN.

## How it works (mechanics)

The triage loop runs weekly and takes about 30 minutes:

1. **Pull the new rows.** Everything discovered since the last triage: analyses, incidents,
   customer reports, and the rows the CI check flagged.
2. **Score them.** Three numbers each, written down. Disagreement is resolved by writing down
   the *evidence*, not by averaging the opinions.
3. **Apply the thresholds.** RPN ≥ 400 blocks the release; risk ≥ 15 goes into the sprint.
4. **Assign owners and dates.** A row without an owner is not a backlog item.
5. **Move the accepted ones.** Risk ≤ 7 rows are marked `accepted` with a monitoring signal and
   a note — an accepted risk that nobody monitors is just an ignored one.
6. **Update the CI check.** Any new row above the threshold without a `mitigation` fails the
   build.

```ts
// CI: a high-risk row must have an owner and a mitigation.
export function assertInventoryHealthy(rows: FailureMode[]): void {
  for (const row of rows) {
    if (row.rpn < 200) continue;
    if (!row.owner) throw new Error(`${row.id}: RPN ${row.rpn} has no owner`);
    if (row.status === "open" && !row.mitigation) {
      throw new Error(`${row.id}: RPN ${row.rpn} is open with no mitigation`);
    }
  }
}
```

## Worked example — Checkout, scored

Ten rows from the `Checkout` matrix, scored. The RPN column is the interesting one:

| ID | Point | Mode | Sev | Occ | Det | RPN | Risk | Decision |
| -- | ----- | ---- | --- | --- | --- | --- | ---- | -------- |
| FM-004 | FP-04 charge | success, response lost | 9 | 4 | 8 | **288** | 16 | Sprint: resolve by charge id |
| FM-007 | FP-03 insert | unique violation on retry | 7 | 6 | 3 | 126 | 12 | Sprint: idempotency key |
| FM-011 | FP-08 publish | event published twice | 8 | 5 | 6 | **240** | 16 | Sprint: consumer dedupe |
| FM-014 | FP-05 insert | subscription row written, entitlement not | 6 | 5 | 9 | **270** | 15 | Sprint: one transaction |
| FM-019 | FP-09 email | receipt email fails | 2 | 6 | 4 | 48 | 6 | Accept: retry in background |
| FM-023 | FP-10 respond | response write fails | 3 | 2 | 8 | 48 | 4 | Accept: client retries |
| FM-026 | FP-01 auth | identity provider slow | 5 | 3 | 2 | 30 | 6 | Schedule: raise timeout |
| FM-031 | FP-02 validate | body too large | 3 | 7 | 1 | 21 | 7 | Accept: 413 documented |

Read the table in order of RPN and the priority looks wrong: `FM-004` (a lost charge response)
is above `FM-007` (a duplicate row), but it scores lower on occurrence. Read it by risk, and
`FM-004`, `FM-011`, and `FM-014` are the three rows that actually lose money — a duplicate charge,
a doubled event, and a subscription without an entitlement. The triage took both scores and used
the table order only to decide *within* the top three.

## Key data / numbers

- **RPN = severity × occurrence × detection**, each **1–10** → **1..1000**. RPN ≥ **200** needs
  an action; ≥ **400** blocks the release.
- **Risk = severity × likelihood**, both **1–5** → **1..25**. Bands: **15–25** fix now,
  **8–14** schedule, **1–7** accept and monitor.
- **Scoring cost**: **5–8 minutes** per row for a scored row; **30 minutes** to triage 40 rows.
- **Inventory size**: a mature inventory holds **50–300 rows** for a whole organisation; one
  flow usually settles at **15–25**.
- **Review cadence**: rows are re-scored **quarterly**; occurrence and detection change, severity
  rarely does.
- **Pruning**: a mode marked `accepted` for **2 consecutive quarters** with no incident is
  retired from the active list.
- **Retry ceilings in the matrix**: a `retry` recovery MUST declare `maxAttempts` ≤ **5** and
  `total_deadline_ms` ≤ **30000**; a retry budget MUST stay ≤ **10%** of the request deadline.
- **Status codes in the matrix**: `422` validation · `409` conflict · `402` payment declined ·
  `429` throttled (with `Retry-After`) · `503` transient, retryable · `202` accepted for later
  resolution (ambiguous outcome) · `499` client closed the request · `500` unexpected bug.
- **SQLSTATE in the matrix**: `08` connection (transient → `retry`) · `23` constraint (permanent
  → `fail`, `409`) · `40` rollback and `40001` serialization failure (transient → `retry` after
  rollback) · `42` syntax or access error (permanent → `fail`, `500`).
- **SLO and error budget**: a **99.9%** availability SLO allows **43.8 min** of error budget per
  month; a `degrade` recovery MUST NOT consume more than **10%** of that budget without the SLO
  owner's sign-off.

## Real-world use case — Acme SaaS `ExportJob`

`ExportJob` was a background job that produced a CSV and emailed a link. It had four failure
points, a `catch` block per step, and no inventory at all. The first analysis produced **16
modes**; scoring them took an afternoon.

Two rows dominated:

- **`FM-021`, the S3 upload succeeds and the response is lost.** Severity 9, occurrence 3,
  detection 9 → **RPN 243**, risk 12. The customer got *no* export for a job that had actually
  succeeded, and support could not tell why. The mitigation was a **read-back**: on a lost
  response, list the bucket for an object with the job's prefix before declaring failure.
- **`FM-024`, the "mark job done" write fails.** Severity 7, occurrence 5, detection 6 →
  **RPN 210**. The export was produced, the row still said `running`, and the cleanup job
  eventually deleted the file. The mitigation was to make the completion write part of the same
  transaction as the "job handed to the uploader" write, so the state machine cannot disagree
  with itself.

The third row nobody expected was **`FM-009`, the temp file delete fails** — severity 2, RPN 24,
accepted. It was accepted *deliberately*, with a monitoring signal on bucket size, because the
cleanup job was rewritten to tolerate a failed delete. Writing that down as an accepted risk,
with a metric watching it, is what stopped it from being rediscovered as an incident every
quarter.

Six months later the inventory held **62 rows** for the whole platform, **9** of them `accepted`
with monitoring attached, and **0** open rows above RPN 400. The other benefit was quieter: the
team stopped arguing about priorities, because the argument now had a table.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| FMEA with RPN | Comparable; forces explicit scoring | Ordinal maths; false precision | Every flow worth analysing |
| Risk (severity × likelihood) only | Simpler; closer to how people argue | Ignores how quietly it fails | First pass, or a tiny team |
| Frequency from incident data only | Objective | Blind to the failures that were never detected | Mature services with good telemetry |
| Occurrence from code reading | Available immediately | Biased toward what you remember | Services without telemetry |
| Manual judgement, no scores | Fast, flexible | Not comparable across teams | One-off triage of a small flow |
| Automated scoring from logs | Scales | Garbage in; needs a stable taxonomy | After the inventory exists |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Score severity first | Let a noisy detection score inflate the ranking |
| Write down the evidence for each score | Split the difference in a disagreement |
| Treat RPN as a ranking, not a probability | Report RPN as "the probability of failure" |
| Put a number on unmeasured occurrence | Claim occurrence 1 for something you never measured |
| Give every row above the threshold an owner and a date | Leave high-RPN rows in a backlog with no owner |
| Record accepted risks with a monitoring signal | Accept a risk and stop watching it |
| Re-score quarterly | Freeze the scores after the first analysis |
| Keep the inventory in the repo | Keep it in a spreadsheet nobody can diff |

## Common mistakes

- **Severity shopping.** Teams inflate severity to win the argument about priority. Fix the scale
  once, in writing, and reference it.
- **Detection 1 by default.** A mode with no test and no alert is not well detected; it is
  *undetected*, and that is a 10.
- **Scoring the fix, not the failure.** Severity describes the outcome, not the effort to fix it.
- **One number per team.** Scores are only comparable when the scale is shared. Agree the scale
  once, org-wide.
- **The spreadsheet.** An inventory in a spreadsheet is a snapshot; in the repository it is a
  diff, reviewable in a pull request, and checkable by CI.
- **Analysis without ownership.** A matrix with 100 rows and no owners is a research project.

## Checklist

- [ ] Every failure mode has an id, a flow, a point, a category, and a recovery.
- [ ] Every row has severity, occurrence, detection, RPN, and risk scores with a written reason.
- [ ] Occurrence uses "5, unmeasured" wherever nobody has instrumented the path.
- [ ] Every row above RPN 200 has an owner and a dated mitigation.
- [ ] Every RPN ≥ 400 row is fixed or explicitly accepted by the release owner.
- [ ] Every `accepted` row has a monitoring signal attached.
- [ ] The inventory is in the repository and a CI check fails on an unowned high-risk row.
- [ ] Rows are re-scored quarterly, and retired modes keep their history.

## Related

- [Enumerating Failure Points and Failure Modes (52.1–52.2)](../01-concepts/01-enumerating-failure-points-and-modes.md)
- [Mapping Modes to Categories and Recovery (52.3–52.4)](../01-concepts/02-mapping-modes-to-categories-and-recovery.md)
- [Failure-Path Analysis of the Checkout Flow](../03-practical-examples/01-checkout-failure-path-analysis.md)
- [Chapter 51 — Correctness Properties](../../51-correctness-properties-of-error-handling/README.md)
