# Section 02: Event Categories & Granularity

Audit events are categorized by domain and severity to enable efficient querying and analysis. Each event captures who performed what action, on what resource, from where, and with what result. The granularity is configurable: full auditing (every API call), security auditing (authentication, authorization, configuration changes), or minimal auditing (compliance-mandated events only).

Event categories: authentication (login, logout, MFA, password change, SSO), authorization (permission change, role assignment, impersonation), data access (export, import, delete, view PII), configuration (tenant settings, agent configuration, integration changes), billing (plan change, payment method, invoice), and security (rate limit breach, suspicious IP, failed login).

Event schema: event_id (UUIDv7 for time-ordered sorting), tenant_id, actor_id (user or service), actor_type (user, api_key, service_account), action (verb: created, updated, deleted, viewed, exported), resource_type (agent, call, recording, user), resource_id, result (success, denied, error), metadata (JSON with action-specific details), client_info (IP, user_agent, geo), correlation_id, and timestamp.
