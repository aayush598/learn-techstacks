# Section 05: Anomaly Detection with Machine Learning

ML-based anomaly detection identifies security threats that don't match known signatures—novel attacks, zero-day exploits, insider threats, and compromised accounts. The system builds behavioral baselines for users, services, and tenants, then detects deviations that indicate compromise.

ML models: user behavior (login times, endpoint access patterns, data volume transferred), API behavior (endpoint call frequency, parameter distributions, error rates), tenant behavior (overall usage patterns, user addition rate, API key creation frequency), and network behavior (connection patterns, protocol distributions, traffic volumes). Models are retrained daily with a 30-day training window.

Model deployment: features extracted from logs → models evaluate in real-time (sub-50ms inference) → anomaly score calculated per event → score compared to dynamic threshold (3σ from baseline) → anomalous events tagged with score and contributing factors → alerts triggered for scores exceeding thresholds. False positive feedback loop: analysts mark alerts as true/false positive → model adjusts weights.
