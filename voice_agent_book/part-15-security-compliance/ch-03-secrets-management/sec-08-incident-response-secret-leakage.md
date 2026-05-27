# Section 08: Incident Response for Secret Leakage

Secret leakage incident response defines procedures for detecting, containing, and recovering from exposed secrets. When a secret is suspected compromised, the response team follows a runbook to minimize damage, rotate affected secrets, and investigate the cause. Automated detection reduces response time from hours to minutes.

Detection signals: git commit containing secret pattern (pre-commit hooks + secret scanning), unexpected secret access patterns (geographic anomaly, volume spike), credential usage from unknown IPs, secrets appearing in error logs or stack traces, and third-party breach notifications involving integrated services.

Incident response runbook: 1) Confirm compromise (verify secret was exposed), 2) Rotate secret immediately (generate new value, update services), 3) Revoke compromised secret (add to revocation list), 4) Investigate scope (what data was accessed with compromised credential), 5) Notify affected parties (tenants if their data was exposed), 6) Conduct post-mortem (root cause analysis, preventive measures). Target: under 5 minutes to rotate, under 1 hour to contain.
