# Section 02: Environment Injection & Service Binding

Environment injection delivers secrets to running services without exposing them in plaintext in configuration files, CI/CD logs, or version control. The injection pattern binds secrets to services at deployment time, ensuring each service only receives the secrets it needs. This follows the principle of least privilege for secret access.

Injection patterns: Kubernetes Secrets mounted as volumes (memory-backed tmpfs, never written to disk), environment variables from secrets (injected by the orchestrator at pod start), sidecar containers (Vault Agent or Secret Store CSI driver that fetches and injects secrets), and init containers (fetch secrets before application starts, store in shared memory volume).

Service binding: each service deployment declares required secrets (by name) in its configuration. The deployment pipeline fetches only those secrets from the central store and injects them. Secrets are never written to configuration files or CI/CD artifacts. If a secret cannot be fetched, the deployment is aborted.
