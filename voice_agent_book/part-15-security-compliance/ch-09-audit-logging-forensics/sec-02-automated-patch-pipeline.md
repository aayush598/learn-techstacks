# Section 02: Automated Patch Deployment Pipeline

The automated patch deployment pipeline reduces the time from patch release to production deployment. Patches flow through: detection → testing → staging → canary → production. The pipeline is fully automated for routine patches, with manual approval gates for critical production deployments.

Pipeline stages: 1) Vulnerability scanner identifies patchable CVE in inventory, 2) Patch downloaded into artifact repository, 3) Automated tests (unit, integration, security) run against patched system, 4) Deployed to staging environment (production mirror), 5) Integration and load tests pass, 6) Canary deployment (10% of instances, monitored for 1 hour), 7) Production rollout (25% → 50% → 100% over 2 hours), 8) Post-deployment monitoring (4 hour watch period).

Automation tooling: Ansible/Chef for OS patches, renovate/dependabot for dependency patches, Kubernetes rolling updates for container patches, and Terraform for infrastructure patches. Failed patches are auto-rolled back. The pipeline generates a patch report for each cycle: CVEs addressed, systems patched, rollout timeline, and any issues encountered.
