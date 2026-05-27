# Section 04: Forensic Query Engine

The forensic query engine enables security teams to search and analyze audit logs efficiently. It supports complex queries across billions of events: time-range searches, pattern matching, correlation analysis (find all events from a user within 5 minutes of a security alert), and aggregation (count login failures per IP over time).

Query capabilities: full-text search on event metadata, structured queries on event fields (tenant_id, actor_id, action, resource_type), time-range filters, geo-queries (events from specific regions), anomaly detection queries (velocity, volume changes), and join-like correlations between event streams. Results are paginated and can be exported as CSV/JSON.

The query engine is built on Elasticsearch (hot data) with connectors to Athena (warm data). Complex queries spanning hot and warm tiers are executed in parallel and results merged. Query results are cached for commonly used investigations. Access to the query engine is restricted to security team members with MFA.
