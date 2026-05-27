# Section 03: Audit Log Storage Strategy

Audit log storage balances cost, retention requirements, and query performance. Hot storage (Elasticsearch or ClickHouse) provides fast queries for recent data (90 days). Warm storage (compressed Parquet in S3 with Athena queries) for data up to 1 year. Cold storage (Glacier/deep archive) for data up to 7 years for compliance.

Storage tiers: hot (SSD-backed, indexed by tenant+timestamp, real-time search), warm (columnar format, partition by month, queryable with SQL via Presto/Athena), cold (compressed JSON, no direct query, restore on request for investigations). Data moves between tiers automatically based on age policies.

Data lifecycle: events are written to hot storage in real-time → after 90 days, batch job moves to warm storage → after 1 year, moves to cold storage → after 7 years, deleted (or retained based on legal hold). Legal holds override deletion: flagged events are retained indefinitely. Storage costs are tracked per-tenant for potential pass-through billing.
