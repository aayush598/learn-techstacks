# Aggregation Mechanics — Accumulation, Ordering, Caps, and Bulk

> Part VII · Chapter 17 · Sections 17.11–17.13 · _Estimated reading time: 20 min_
> **Prerequisite:** [Aggregation, Field-Level Representation, and Stable Codes](../01-concepts/04-aggregation-and-field-error-representation.md)

## In one sentence

Aggregated validation is a **pipeline of accumulators**: each stage appends typed issues to a list
instead of throwing, cross-field rules run only over inputs that passed, collection guards run
before per-item work, and a **cap** bounds what finally leaves the process.

## Why this matters in production

Throw-based validation *cannot* aggregate — the first exception unwinds the stack and every
remaining defect waits for another round trip. Teams that discover this late retrofit
`safeParse`-style accumulation across dozens of handlers. The mechanics below are what "retrofit"
should have looked like from day one: cheap, uniform, and bounded (an unbounded accumulator is
just a slower DoS vector — the response cap is part of correctness, not polish).

## The accumulator shape

```ts
type Issue = { pointer: string; code: string; params?: Record<string, unknown> };

class ValidationAccumulator {
  private issues: Issue[] = [];
  private byPointer = new Map<string, number>();   // primary-code-per-pointer dedup

  add(pointer: string, code: string, params?: Record<string, unknown>) {
    const key = `${pointer}::${code}`;
    if (this.byPointer.has(key)) return;               // dedup: one pointer+code pair
    if (this.issues.length >= MAX_ISSUES) { this.truncated = true; return; }
    this.byPointer.set(key, this.issues.length);
    this.issues.push({ pointer, code, params });
  }

  get ok()    { return this.issues.length === 0 && !this.truncated; }
  get list()  { return this.truncated ? { errors: this.issues, errorsTruncated: true }
                                      : { errors: this.issues }; }
}
```

Properties that matter: **O(1) dedup by (pointer, code)**, **hard cap with an explicit truncated
flag**, and no throw-path anywhere in the validator.

## Stage pipeline with dependencies

```text
 Stage 1  guards      fail fast (throw/return) — no accumulation
 Stage 2  parse       fail fast
 Stage 3  per-field   accumulate required → type → range → format
 Stage 4  cross-field accumulate, inputs = fields that PASSED stage 3
 Stage 5  conditional accumulate, evaluate in declared dependency order
 Stage 6  convert     accumulator → 422 Problem Details (never from stages 1–2)
```

```python
# Stage 3–5 in one pass: per-field first, then dependent rules over clean values only.
acc, values = ValidationAccumulator(), {}

for spec in FIELD_SPECS:                       # ordered: required, type, range, format
    ok, value, issue = run_field(spec, body)
    if ok:
        values[spec.name] = value
    else:
        acc.add(f"/{spec.name}", issue.code, issue.params)

if "startDate" in values and "endDate" in values:
    if values["endDate"] < values["startDate"]:
        acc.add("/endDate", "cross_field_invalid", {"rule": "end_after_start"})

if values.get("plan") == "enterprise" and "seats" not in values:
    acc.add("/seats", "conditional_rule_failed", {"when": "plan=enterprise"})
```

Ordering rules encoded here:

1. **Per-field issues come first** (users scan top-down by field).
2. **Dependent rules see only clean values** — this is what prevents derivative duplicates
   (17.15).
3. **Conditional `required` is emitted only when the condition's inputs are clean** (if `plan`
   itself failed `type_mismatch`, do not also claim seats is required for it).

## Per-field primary code

When one field fails multiple rules, report the **first by stage order** as primary; optionally
carry the rest in `params.secondary` if truly needed:

```json
{ "pointer": "/seats", "code": "required", "params": { "secondary": ["format_invalid"] } }
```

Usually `secondary` is noise — an absent value failing format is obvious. Prefer **silently
suppressing** later-stage checks for that field entirely.

## Bulk mechanics (17.11)

```text
 rows[] ──▶ size guard (too_many_items) ──▶ per-row accumulate ──▶ policy
                                                          │
              ┌───────────────────────────────────────────┤
              ▼                                           ▼
        all clean → proceed to write            any invalid → 422 + summary
              │                                    (all-or-nothing default)
              ▼
        partial policy (opt-in): write valid rows, return 200 + per-row results
```

```ts
// Per-row accumulation with row-scoped pointers and a global cap.
const acc = new ValidationAccumulator();
const rows = body.rows as unknown[];

if (!Array.isArray(rows))            { acc.add("/", "type_mismatch", { expected: "array" }); }
else if (rows.length > MAX_ROWS)     { acc.add("/rows", "too_many_items", { max: MAX_ROWS }); }
else {
  rows.forEach((row, i) => {
    const rowIssues = validateRow(row);            // each issue pointer starts with /rows/{i}/
    for (const issue of rowIssues) acc.add(issue.pointer, issue.code, issue.params);
  });
}

const summary = {
  total:   Array.isArray(rows) ? rows.length : 0,
  invalid: new Set(acc.list.errors.map(e => e.pointer.split("/")[2])).size,
  valid:   0, filled: true,
};
```

Mechanical details teams forget:

- **Count invalid rows, not issues** in `summary.invalid` (one row may have three issues).
- **`/rows` vs `/rows/i`**: the size guard points at the container; row issues at indexed paths.
- **Do not start writing valid rows before the policy is chosen.** All-or-nothing is decided
  *before* any INSERT; partial mode writes and returns `200` with per-row outcomes, never `422`.

## Cost control

| Guard | Bound | Why |
| ----- | ----- | --- |
| `MAX_ISSUES` (e.g. 100) | response bytes, serializer CPU | Pathological bodies with 10⁵ defects |
| `MAX_ROWS` | validator CPU | Per-row work is linear by definition |
| `MAX_DEPTH`, `MAX_KEYS` | parser CPU/memory | Nesting bombs |
| Early `too_many_items` | skips all per-item work | Largest single win |

⚠️ **Hazard.** Cap enforcement must happen **in the accumulator**, not only at serialization —
otherwise you pay to *create* a million issues and then throw them away.

## Key data / numbers

- Recommended caps: **100 issues/response**, **1000 rows/bulk request**, **depth ≤ 16** —
  recommendations; publish your real numbers in the contract.
- Dedup key: `(pointer, code)` — O(1) via map.
- Cross-field rules evaluate **after** all referenced fields pass.
- Partial bulk success returns **`200` + results**, never a bare `422`.

## Real-world use case — ExportJob

`ExportJob`'s spec validator originally used a `try { validate() } catch { 400 }` pattern: each
run surfaced exactly one bad column. Analysts with 30-column specs averaged 2.8 attempts per
submit. Replacing it with the accumulator cut attempts to 1.1 and surfaced a surprise: the
response had been hitting an informal 20-error limit imposed by an earlier serializer "cleanup"
with no truncation flag — clients believed they had fixed everything. Adding `errorsTruncated`
removed that silent lie within one release.

## Trade-offs

| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|
| Throw-first validator | Simple control flow | Cannot aggregate; N round trips | Scripts, one-off tools |
| Accumulator (recommended) | Complete answers, dedupable, capped | More plumbing | ✅ APIs, bulk, forms |
| Two-pass (collect all, then filter) | Very explicit ordering | Double validation cost | Huge DTOs with heavy rules |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Accumulate via issue lists (`safeParse`, validators with `.issues`) | Catch `ValidationException` to simulate aggregation |
| Dedup by (pointer, code) in the accumulator | Rely on the serializer to remove duplicates |
| Cap inside the accumulator; set a truncation flag | Build a million issues then slice at the edge |
| Run dependent rules over clean values only | Evaluate cross-field rules against raw input |

## Common mistakes

- **Aggregating at the HTTP layer but fail-fast in the DTO** — the outer layer never sees issues 2+
  because the inner `throw` already fired.
- **Counting issues as rows** in bulk summaries — misleads import UIs.
- **Partial-write + `422`** — contract contradiction (see 17.11 hazard in the concepts file).
- **Uncapped nested accumulation** — one bad row with 10k issues blows the response.

## Checklist

- [ ] Validator has no throw path for field-level issues.
- [ ] Cross-field/conditional rules gate on clean inputs.
- [ ] Accumulator enforces the cap; response carries `errorsTruncated`.
- [ ] Bulk size guard precedes per-row work; summary counts rows, not issues.
- [ ] Write policy (all-or-nothing vs partial) decided before any write.

## Related

- [Cross-Field, Conditional, Nested, and List Rules](../01-concepts/03-cross-field-conditional-nested-and-lists.md)
- [Bulk, Cross-Field, and Cast Examples](../03-practical-examples/02-bulk-cross-field-and-cast.md)
- [Validation Reference](../05-reference/README.md)
- [Chapter 31 — Asynchronous Error Handling (collect-all patterns)](../../../part-12-async-and-background-jobs/31-asynchronous-error-handling/README.md)
