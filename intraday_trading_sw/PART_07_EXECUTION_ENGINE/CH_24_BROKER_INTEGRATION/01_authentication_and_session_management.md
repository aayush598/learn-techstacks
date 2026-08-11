# 01 — Authentication and Session Management

## Purpose
Handle broker authentication securely and reliably, including token lifecycle,
reconnection, and failure behavior.

## Credential handling (security, CH_34)
- Secrets live in a secrets store / env-injected config — never in code or repo.
- Adapters read credentials via a `SecretsProvider` interface (CH_34/00).

## Authentication flows (typical)
- **API key/secret** (HMAC signed requests): sign every request; refresh on
  rotation.
- **OAuth/token**: obtain access + refresh tokens; persist refresh token in the
  secrets store; auto-refresh before expiry.
- **Session cookies** (older APIs): store encrypted; re-auth on 401.

## Session manager responsibilities
- Maintain auth state machine: `DISCONNECTED → AUTHENTICATED → TRADING_ENABLED`.
- Pre-emptively refresh tokens (e.g., refresh at 80% of expiry).
- On 401/403: re-authenticate once; if still failing → circuit breaker on
  trading (CH_23/00) + page a human (CH_30).
- Reconnect with backoff (CH_05/02) and re-establish all subscriptions/orders.

## Pseudo-code: auth state machine
```
on_request():
    if token_expiring_soon(): refresh_token()          # proactive
    try: return broker_call()
    except AuthError:
        refresh_token()
        if retry_fails:
            risk.circuit_breaker("auth_failure")
            alert("auth_failure")
            raise
```

## Rules
- Credentials are loaded once at startup and never logged (mask in logs).
- Token refresh must never block the order path for long (async refresh).
- Auth failure = trading halt until resolved — never trade "blind".
