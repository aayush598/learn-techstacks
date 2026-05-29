# Section 05: Security Information & Event Management (SIEM)

SIEM integration streams audit events to the organization's security operations center for real-time threat detection and correlation. The platform exports events in standard formats (CEF, LEEF, JSON) compatible with major SIEMs (Splunk, Elastic SIEM, Datadog Security, Sentinel). Tenants can also receive their own audit stream for self-monitoring.

SIEM pipeline: events are published to a message bus (Kafka) → SIEM connector (syslog, HTTP, or direct Kafka consumer) transforms to target format → sends to SIEM with tenant context → SIEM correlates with other data sources (cloud logs, network logs) → alerts on suspicious patterns. A separate SIEM instance for the SOC monitors platform-level events.

Tenant-specific SIEM: enterprise tenants can subscribe to a filtered audit stream containing only their tenant's events. Events are sent to the tenant's SIEM via syslog or HTTPS with HMAC authentication. This supports the tenant's own security monitoring and compliance requirements. The tenant SIEM integration is configured in the enterprise settings.
