# 02 — Access Control and Audit

## Purpose
Ensure only authorized people can change things, and that every change is
recorded — the trust backbone of an open-source trading system.

## Roles (least privilege)
| Role | Can do |
|---|---|
| viewer | read dashboards/reports |
| operator | start/stop services, acknowledge alerts, kill switch |
| strategist | edit strategy manifests, run backtests |
| admin | change risk policy, secrets, deploy, manage users |

Defaults: everyone is a viewer; elevated roles are explicit and logged.

## Action categories and control
- **Read** (dashboards, reports): authenticated viewer+.
- **Write** (manifests, config): strategist/admin.
- **Risk-policy changes**: admin only, and only between sessions; logged with
  before/after diff.
- **Deployments**: admin, through CI/CD gate (CH_12/CH_41).
- **Kill switch**: operator+ — always works, always logged (CH_23/02).

## Audit log (append-only)
- Who, what, when, from where, before/after, decision_id.
- Logged for: all config changes, secrets access, role changes, deployments,
  risk-policy edits, manual orders, kill-switch use.
- The audit log itself is append-only (write-once) and backed up (CH_35).

## Pseudo-code: audit
```
def audit(action, actor, ctx):
    entry = {ts, actor, action, before, after, source_ip, decision_id}
    audit_log.append(entry)       # append-only store
```

## Rules
- No anonymous privileged actions; no shared accounts (unique identities).
- Risk-policy changes require two-person review (one proposes, one approves) —
  enforced by the tooling (CH_12).
- Audit log integrity is checked periodically (hash chain) — tampering detected.
