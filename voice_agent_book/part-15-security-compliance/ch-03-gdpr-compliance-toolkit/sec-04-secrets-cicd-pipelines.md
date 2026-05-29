# Section 04: Secrets in CI/CD Pipelines

CI/CD pipelines require access to secrets for building, testing, and deploying applications. These secrets must be carefully managed to prevent exposure in build logs, artifact storage, or source code. The platform uses short-lived tokens and dynamic secrets for CI/CD, not long-lived credentials.

CI/CD secret access: pipeline requests a deployment token from the secrets store at start → token is valid for the pipeline duration (max 1 hour) → token grants access to exactly the secrets needed for that pipeline step → secrets are injected as environment variables visible only to the running process → secrets are masked in build logs → token is revoked when pipeline completes.

Security practices: never store secrets in repository variables (GitHub Actions secrets, GitLab CI variables) for production credentials. Use the cloud provider's native secret integration (AWS IAM + Secrets Manager, GCP Secret Manager). All secrets access in CI/CD is logged and reviewed. Secrets are never written to build artifacts or container images.
