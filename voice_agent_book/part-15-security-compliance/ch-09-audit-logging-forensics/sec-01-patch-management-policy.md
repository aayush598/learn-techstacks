# Section 01: Patch Management Policy

A formal patch management policy governs how security patches are evaluated, tested, and deployed across the platform. The policy defines patching priorities based on CVSS severity, patch types (security, critical, routine), deployment windows, and exceptions. The goal is to minimize the window between patch availability and deployment.

Policy rules: critical/high (CVSS 7.0+) patches deployed within 48 hours, medium patches within 7 days, low patches within 30 days. Operating system patches: automated with staged rollout. Application/library patches: tested in staging first, then deployed via CI/CD. Emergency patches (exploited in the wild): deployed within 4 hours using hotfix process.

Exception process: if a patch cannot be applied within SLA (compatibility issues, requires downtime), an exception is requested with compensating controls (virtual patching via WAF, network segmentation, monitoring). Exceptions require CISO approval, have a maximum duration (30 days), and are reviewed weekly. The patch management dashboard shows compliance percentage and overdue patches.
