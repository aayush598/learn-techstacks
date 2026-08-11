# 01 — Network and API Security

## Purpose
Secure the system's network surface: the dashboard, local APIs, and broker
connections — against the internet's default hostility.

## Network posture
- **No public exposure of internal APIs**: the dashboard/API bind to
  localhost or a private interface only.
- If remote access is needed: an encrypted tunnel/VPN (self-hosted) or reverse
  proxy with TLS, never raw HTTP.
- **TLS everywhere**: broker connections (wss/https), dashboard (https when
  exposed), tunnel endpoints. Certificates via a self-hosted CA or trusted CA.
- **Firewall**: allow only required ports (e.g., 22 for admin, 80/443 if
  exposed, outbound to broker/exchange); default-deny inbound.

## API hygiene
- Rate-limit the dashboard API; validate all inputs (no injection).
- Every privileged action requires the authorized session (CH_34/02).
- Keep dependencies minimal (CH_00/02) → smaller attack surface.

## Broker/exchange connections
- Verify server certs (no `verify=False`); pin where the broker allows.
- Use the broker's API per docs; never hardcode keys (CH_34/00).
- WebSocket connections: validate origin/URL against configured endpoints only.

## Pseudo-code: local API guard
```
if not request.remote_addr.is_loopback(): deny
if not request.tls_ok(): deny
if rate_limited(request): deny
if not authorized(request): deny(401) + audit_log
```

## Rules
- Assume the public internet will probe you; default-deny is the baseline.
- No plaintext credentials or tokens on the wire (CH_34/00).
- Periodic security review is part of the release checklist (CH_12/CH_41).
