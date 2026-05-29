# Section 05: IP Whitelisting & Restriction

IP whitelisting restricts API access to trusted network sources. Tenants can configure allowed IP addresses or CIDR ranges that are permitted to call the API using their keys. Requests from IPs outside the whitelist are rejected before any processing occurs. This is enforced at the API gateway (CDN/load balancer layer).

IP restriction flow: API gateway extracts client IP from connection or X-Forwarded-For header, looks up tenant's allowed IPs from cache (Redis, refreshed from DB every 5 minutes), matches against CIDR list (binary search for efficiency), rejects with 403 if not matched. Wildcard support allows specific IPs, CIDR blocks, or "any" (disabled IP restriction).

IP list management includes: configurable via dashboard or API, audit log of changes, validation of CIDR format, support for IPv4 and IPv6, and bulk import. The platform also supports geo-restriction (allow only specific countries) as an additional security layer for compliance requirements.
