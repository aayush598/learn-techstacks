# Section 02: Intrusion Detection System (IDS)

An Intrusion Detection System monitors network traffic and system behavior for malicious activity. The IDS analyzes patterns, signatures, and anomalies to detect attacks in real-time. The platform uses a hybrid approach: signature-based (known attack patterns) and behavior-based (anomaly detection).

IDS components: network IDS (monitor traffic between services for lateral movement, data exfiltration patterns), host IDS (agent on each server monitoring file integrity, process behavior, system calls), and application IDS (application logs analyzed for attack patterns—parameter tampering, authentication bypass attempts).

Signature-based detection: Snort/Suricata rules for known exploit signatures, updated hourly from threat intelligence feeds. Behavior-based detection: ML models trained on normal traffic patterns (request volume, response sizes, API endpoint access patterns) alert on deviations. Alerts are prioritized: critical (confirmed attack, immediate response), high (suspicious pattern, investigate within 1 hour), medium (anomaly, investigate within 8 hours), low (informational, daily review).
