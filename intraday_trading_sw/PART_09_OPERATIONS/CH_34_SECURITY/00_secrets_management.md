# 00 — Secrets Management

## Purpose
Store and use API keys, tokens, and credentials securely — never in code, never
in the repo, never in logs.

## Threat model
- Repo leaks (public open-source repo — assume anyone reads it, CH_12).
- Log leakage (structured logs shared in bug reports).
- Disk access on the server.
- Shoulder-surfing / access control gaps (CH_34/02).

## Secrets policy
- **No secrets in the repo, ever** — not even in `.env` committed files or
  commented code.
- Secrets live in: (a) the OS keyring/secrets-manager, or (b) a permissioned
  file outside the repo (e.g., `~/.config/.../secrets.json`, chmod 600), or
  (c) env vars injected by the process manager (CH_31/02).
- Rotation: keys rotated on schedule and on any suspected exposure; the adapter
  picks up rotation via the SecretsProvider.

## Pseudo-code: secrets provider interface
```
class SecretsProvider:
    def get(self, key) -> str        # e.g., "broker.api_key"
    def set(self, key, value)        # admin only (CLI)
provider = load(provider_from_config())   # keyring | env | file
```

## Logging redaction
- Adapters must redact secrets in any logged payload (structured logs, CH_33/00).
- Add a test: assert no known credential substring appears in sample logs (CH_36).

## Rules
- Default-deny: a missing secret fails fast at startup (never trade "empty").
- Backups (CH_35) must encrypt secrets at rest.
- Access to secrets is logged (who/when) and least-privileged (CH_34/02).
