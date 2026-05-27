# Section 06: User Activity Monitoring

User activity monitoring tracks individual user actions within the platform to detect anomalous behavior, insider threats, and compromised accounts. The system builds behavioral baselines per user and alerts on deviations: unusual login times, access to resources the user has never accessed before, bulk data exports, or failed access attempts.

Behavioral baselines: each user profile includes typical login patterns (time of day, IP ranges, device), typical resource access patterns (which agents, which reports), and typical API usage volume. Baselines are calculated over a 30-day rolling window. New users have a 14-day learning period before baselines are enforced.

Alert triggers: login from new geographic location (never seen before), access to resource outside normal scope, export > 10% of tenant data, API call volume > 3x normal, simultaneous logins from different locations, and off-hours activity for users with regular patterns. Alerts can trigger automatic session termination and account suspension.
