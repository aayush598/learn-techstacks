# Section 04: Change Management Process

Change management ensures all production changes follow a controlled process: request, review, approve, test, deploy, and verify. SOC 2 CC7.1 requires documented change management. The platform enforces this via the CI/CD pipeline: every production deployment must be linked to an approved change request.

Change types: standard (pre-approved, low-risk: config changes, dependency updates—follow runbook), normal (requires approval: new features, infrastructure changes—change advisory board review), emergency (requires expedited approval: security patches, hotfixes—post-hoc documentation). Each type has a defined workflow and approval requirements.

Change workflow: developer creates change request in ticketing system → automated testing (unit, integration, security scan) → peer review (code review with at least one senior engineer) → CAB approval (for normal changes, meeting weekly) → deployment to staging → integration tests pass → deployment to production (canary, 10% → 50% → 100%) → monitoring period (30 minutes with error budget) → change closure and documentation.
