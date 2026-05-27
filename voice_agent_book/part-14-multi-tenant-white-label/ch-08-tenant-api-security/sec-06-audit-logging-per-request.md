# Section 06: Audit Logging per Request

Per-request audit logging captures every API call with tenant context, identity, action, resource, and outcome. The audit trail provides accountability, supports security investigations, and meets compliance requirements (SOC 2, HIPAA). Each audit event is immutable and stored in a dedicated append-only audit store.

Audit event schema: event ID (UUID v7), timestamp, tenant ID, user ID (or API key ID), HTTP method, request path, request parameters (sanitized of secrets), response status code, response size, latency, client IP, user agent, and correlation ID (for tracing across services). Sensitive data (passwords, tokens, PII) is redacted before logging.

The audit pipeline uses a separate write-ahead log for reliability. Events are buffered in a message queue (Kafka/Redis) and batch-written to the audit store. The audit store is a time-series database optimized for append-heavy workloads with immutable retention policies.
