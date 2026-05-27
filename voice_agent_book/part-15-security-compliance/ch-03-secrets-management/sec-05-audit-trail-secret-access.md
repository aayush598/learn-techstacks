# Section 05: Audit Trail for Secret Access

Every access to a secret is logged immutably for security auditing and incident response. The audit trail captures: which service/user accessed which secret, when, from what IP, with what result (success/denied), and the secret version. Audit logs are stored in a separate, append-only system that cannot be modified by the services accessing secrets.

Audit events include: ReadSecret (get secret value), ListSecrets (list available secrets), CreateSecret (new secret created), UpdateSecret (value changed), DeleteSecret (secret removed), RotateSecret (automatic rotation triggered), and AccessDenied (unauthorized access attempt). Each event includes correlation ID for linking to deployments or user actions.

Audit log storage: immutable log store (AWS CloudTrail, Vault audit log, or custom solution using write-once storage). Logs are retained for 7 years (compliance requirement). Automated monitoring alerts on suspicious patterns: repeated AccessDenied events, secret access outside business hours, or access from unexpected IP ranges.
