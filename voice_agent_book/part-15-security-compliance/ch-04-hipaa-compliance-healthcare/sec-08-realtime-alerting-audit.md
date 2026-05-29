# Section 08: Real-Time Alerting on Audit Events

Real-time alerting processes audit events as they occur and triggers notifications for security-relevant patterns. The alert system uses rule-based evaluation (if event matches a rule, fire alert) and machine learning models (for anomaly detection). Alerts are routed to the appropriate response team based on severity.

Alert rules: single-event rules (failed login from unknown IP → high severity, MFA disabled by admin → critical), threshold rules (10+ failed logins in 5 minutes → brute force attack, 5+ API errors in 1 minute → potential scanning), correlation rules (password change followed by export → potential account takeover), and anomaly rules (deviation from user baseline → medium severity).

Alert routing: critical alerts → SMS + phone call to on-call engineer (15-minute response SLA), high alerts → Slack/PagerDuty notification (1-hour response), medium alerts → email + Slack (8-hour response), low alerts → daily digest. Alerts include full context (event details, related events, suggested response). Dashboard shows active alerts, response progress, and resolution status.
