# Section 05: Zero-Downtime Migration Strategies

Zero-downtime migration allows schema or data changes without interrupting tenant service. The strategy uses blue-green deployment patterns applied to data: run old and new schemas simultaneously, dual-write during migration, backfill historical data, then switch reads to the new schema. This eliminates maintenance windows for schema changes.

Zero-downtime approach: create new schema version alongside existing, enable dual-write (write to both old and new), backfill existing data from old to new (batch process), run validation queries comparing old and new, switch reads gradually (10% → 50% → 100% canary), monitor for errors, remove old schema after observation period.

Tools and techniques: PostgreSQL logical replication for live data sync, pgroll for zero-downtime schema changes, feature flags per-tenant to control migration rollout, and automated rollback if error rate exceeds threshold. Enterprise tenants can schedule migration windows for additional safety.
