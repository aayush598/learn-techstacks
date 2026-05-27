# Section 04: Runtime Application Self-Protection (RASP)

Runtime Application Self-Protection detects and blocks attacks from within the application runtime. Unlike WAF (external), RASP operates inside the application, giving it full context to distinguish legitimate requests from attacks. RASP agents are embedded in the application server and monitor behavior at the function call level.

RASP capabilities: SQL injection detection (intercept database queries, block malicious patterns), command injection detection (monitor exec/system calls), deserialization attack detection (validate object streams before deserialization), path traversal detection (validate file paths against allowed directories), and authentication bypass detection (monitor authentication logic flow).

RASP response actions: block (prevent the malicious operation), log (record the attack for analysis), alert (notify security team), and simulate (log what would have been blocked, for testing). RASP configuration is tuned per environment: learning mode (record behavior, no blocking) for staging, protection mode (block confirmed attacks) for production. RASP complements WAF by catching attacks that bypass network-level defenses.
