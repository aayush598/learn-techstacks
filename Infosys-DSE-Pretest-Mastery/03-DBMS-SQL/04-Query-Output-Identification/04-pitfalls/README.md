# 04-pitfalls — Query Output Identification

The traps: each one mapped to the execution stage where the trace went wrong.

| File | What it covers |
|---|---|
| [01-output-identification-traps.md](01-output-identification-traps.md) | Stopped after stage 1, counted entities not rows, `WHERE` deleted the NULL row, NULL comparisons treated as "kept", `COUNT(*)` vs `COUNT(col)`, forgot `GROUP BY` collapses, `DISTINCT` on one column, `LIMIT` before sorting, aggregate without `GROUP BY`, `HAVING` vs `WHERE` |

**Back to:** [Query Output Identification topic](../README.md)
