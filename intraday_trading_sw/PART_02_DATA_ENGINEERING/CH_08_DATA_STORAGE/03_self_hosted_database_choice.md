# 03 — Self-Hosted Database Choice

## Purpose
Choose the right local database per workload while avoiding heavy external
database servers.

## Workloads and choices
| Workload | Choice | Why |
|---|---|---|
| Hot state, checkpoints, metadata, journal | **SQLite** (WAL mode) | file-based, zero daemon, transactional, stdlib-adjacent |
| Bar/feature analytics | **Columnar files** (CH_08/01) | best scan performance, self-contained |
| Search/experiment tracking | SQLite tables or flat files | simple |
| Notifications/timeline | SQLite or log files | simple |

## SQLite operating guidance
- One writer at a time; use WAL mode to allow concurrent readers.
- Enable `busy_timeout`; retry `SQLITE_BUSY` with backoff.
- Transactions: batch inserts; commit per flush window.
- Indexes: symbol+ts (unique), symbol (ranges), status columns.
- Backup: `VACUUM INTO` / online backup API (CH_35).
- Keep the DB small: it holds *state*, not bulk history.

## Pseudo-code: journal insert (batched)
```
with db.transaction():
    for row in batch:
        db.execute("INSERT OR REPLACE INTO journal(...) VALUES(...)", row)
# journal: symbol, ts, action(signal/order/fill/risk), payload_json, created
```

## When to add a heavier DB (and resist it)
- Only if: multi-process writers to the same *state* with transactions across
  processes and you cannot restructure. In an MVP, a single writer process +
  SQLite is sufficient and simpler to trust and back up.

## Rules
- Prefer files + SQLite for the entire MVP; add complexity only when measured need.
- Every DB access goes through a thin repository module (swappable later).
- Test crash recovery: kill the process mid-write, restart, verify integrity (CH_36).
