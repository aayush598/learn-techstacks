# Section 02: Uptime Monitoring per Tenant

Per-tenant uptime monitoring tracks the availability of services from each tenant's perspective. Synthetic probes simulate tenant API calls and media streams, measuring actual end-to-end availability rather than just infrastructure metrics. This provides SLA-aligned monitoring that reflects the tenant's real experience.

Monitoring probes run from multiple geographic regions every 60 seconds. Each probe executes tenant-specific test scenarios: API health check with tenant authentication, call flow test (initiate call, verify media path), and recording playback test. Results are published to a time-series database with tenant tags.

Uptime calculation uses sliding windows (30-day rolling for monthly SLA reporting). Downtime is tracked per-incident with start/end timestamps. Scheduled maintenance is excluded from uptime calculations if properly notified. The system calculates SLA compliance per tenant and generates breach reports automatically.
