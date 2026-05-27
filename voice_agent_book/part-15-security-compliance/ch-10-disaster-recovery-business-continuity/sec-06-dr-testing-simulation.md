# Section 06: DR Testing & Simulation

Regular DR testing validates that the recovery plan works under realistic conditions. Tests range from tabletop exercises (discussion-based) to full-scale simulations (actual failover and recovery). Testing identifies gaps in documentation, tooling, and team readiness before a real disaster occurs.

Test types: tabletop (team walks through DR scenario, discusses response steps, identifies gaps—quarterly), component test (failover a single service, e.g., database failover—monthly), integration test (failover a dependent group of services—quarterly), full-scale simulation (complete region failover, run from standby for 4+ hours—annually), and chaos engineering (introduce failures randomly in production-like environment—ongoing).

Test documentation: each test has a scenario (what failed), expected behavior (RTO/RPO targets), actual results (time to recover, data loss), observations (what went well, what went wrong), and action items (improvements needed). Tests are scored: pass (met all RTO/RPO), partial (met some), fail (missed critical targets). Failed tests require immediate remediation with re-test within 30 days.
