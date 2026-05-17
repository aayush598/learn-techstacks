## 32. CI/CD + Docker Advanced (851–890)

851. Explain immutable infrastructure.

   **Answer:** Immutable infrastructure replaces servers entirely rather than updating them in place. Deployments create new instances with the latest code, and old instances are terminated, eliminating configuration drift.

852. How do GitOps workflows work?

   **Answer:** GitOps uses a Git repository as the single source of truth for infrastructure. Changes are made via PRs, and an operator (ArgoCD, Flux) syncs the cluster state to match the repository.

853. Explain deployment drift.

   **Answer:** Deployment drift occurs when the actual running environment diverges from the declared configuration. GitOps detects drift via periodic reconciliation and automatically reverts unauthorized changes.

854. What are release trains?

   **Answer:** Release trains are time-based releases (e.g., every 2 weeks) regardless of feature completeness. They reduce variability in deployments and force smaller, more predictable changes.

855. Explain progressive delivery.

   **Answer:** Progressive delivery rolls out changes gradually using canary releases, feature flags, and percentage-based traffic shifting. It monitors metrics and auto-rolls back if errors spike.

856. How do feature flags reduce deployment risk?

   **Answer:** Feature flags decouple deployment from release. Code is deployed dark (disabled), then toggled on for subsets of users. This enables instant rollback without redeployment and safe A/B testing.

857. Explain artifact repositories.

   **Answer:** Artifact repositories (Docker Hub, ECR, GHCR, Nexus) store built artifacts (Docker images, npm packages) with versioning. They provide immutable, signed, and scanned storage for the deployment pipeline.

858. What are build reproducibility concerns?

   **Answer:** Build reproducibility ensures the same commit produces identical artifacts every time. Issues include timestamp injection, network-dependent builds, differing tool versions, and non-deterministic toolchains.

859. Explain Docker build cache invalidation.

   **Answer:** Docker caches each layer based on build context and Dockerfile instructions. Cache is invalidated when the layer's context changes (e.g., modified `package.json` causes `npm install` to rerun). Order layers by volatility to optimize caching.

860. How do distroless images improve security?

   **Answer:** Distroless images contain only the application and its runtime dependencies — no shell, package manager, or OS utilities. This dramatically reduces the attack surface and vulnerability footprint.

861. Explain rootless containers.

   **Answer:** Rootless containers run without root privileges inside the container and on the host. They use user namespaces to map container root to a non-root host user, preventing container escape escalation.

862. What are OCI image standards?

   **Answer:** The Open Container Initiative (OCI) defines specifications for image format and runtime. OCI-compliant images work across any container runtime (Docker, Podman, containerd) without vendor lock-in.

863. Explain container runtime interfaces.

   **Answer:** CRI (Container Runtime Interface) is a Kubernetes API for container runtimes. Implementations include containerd (default), CRI-O, and Docker via dockershim (deprecated). CRI standardizes image and container lifecycle.

864. How does Kubernetes scheduling work?

   **Answer:** The scheduler assigns pods to nodes based on resource requests, taints/tolerations, node affinity, and scoring algorithms (e.g., least-requested, most-requested). It respects pod topology constraints and spread constraints.

865. Explain autoscaling strategies.

   **Answer:** Autoscaling includes HPA (Horizontal Pod Autoscaler) based on CPU/memory/custom metrics, VPA (Vertical Pod Autoscaler) for resource sizing, and Cluster Autoscaler for node scaling.

866. What are taints and tolerations?

   **Answer:** Taints repel pods from nodes unless the pod has matching tolerations. They are used to dedicate nodes to specific workloads (e.g., GPU-only, system-critical) and handle node maintenance.

867. Explain ingress controllers.

   **Answer:** Ingress controllers (NGINX, Traefik, AWS ALB) route external traffic to Kubernetes services based on ingress resource rules. They handle TLS termination, path-based routing, and load balancing.

868. What are service meshes?

   **Answer:** Service meshes (Istio, Linkerd) add a sidecar proxy to each pod, handling mTLS, traffic splitting, observability, and circuit breaking. They abstract networking concerns from application code.

869. Explain rolling update mechanics.

   **Answer:** Rolling updates replace pods incrementally using `maxSurge` (excess pods) and `maxUnavailable` (offline pods). Kubernetes monitors readiness probes; if new pods fail, the rollout pauses or rolls back.

870. How do init containers work?

   **Answer:** Init containers run sequentially before app containers start. They perform setup tasks (database migrations, permission fixes, config generation) and must complete successfully for the pod to start.

871. Explain liveness vs readiness probes.

   **Answer:** Liveness probes restart unhealthy pods (deadlock detection). Readiness probes control whether a pod receives traffic (temporary unavailability). Startup probes delay liveness checks for slow-starting containers.

872. What are sidecar proxies?

   **Answer:** Sidecar proxies are additional containers injected alongside the main app container. They intercept network traffic for logging, metrics, mTLS, and traffic routing without app modification.

873. Explain ephemeral storage.

   **Answer:** Ephemeral storage (`emptyDir`) exists only as long as the pod runs. It's used for scratch space, caching, or shared inter-container files. Contents are lost on pod deletion.

874. How do secrets mount into containers?

   **Answer:** Kubernetes secrets are mounted as files (in `/etc/secrets/`) or environment variables. Secrets are base64-encoded in etcd and should be encrypted at rest with KMS or external secret stores.

875. Explain Docker networking drivers.

   **Answer:** Bridge (default per container), host (shares host network), overlay (multi-host), macvlan (MAC per container), and none (isolated). Drivers isolate networking with different performance and capability tradeoffs.

876. What are container escape vulnerabilities?

   **Answer:** Container escape breaks out of the isolated namespace to access the host. Common vectors include privileged containers, insecure mounts, kernel exploits, and misconfigured capabilities.

877. Explain supply chain security.

   **Answer:** Supply chain security secures the software pipeline from source to deployment. Practices include signed commits, dependency scanning (Dependabot, Snyk), SBOM generation, image signing, and registry scanning.

878. What are SBOMs?

   **Answer:** A Software Bill of Materials (SBOM) is a nested inventory of all components and dependencies in an application. It enables vulnerability tracking, license compliance, and fast incident response.

879. Explain infrastructure observability.

   **Answer:** Observability combines logs (structured events), metrics (time-series data), and traces (request journeys). Tools like Prometheus + Grafana, Loki, and Tempo provide a unified observability stack.

880. How do distributed logs work?

   **Answer:** Distributed logs aggregate logs from multiple services using structured formats (JSON) with correlation IDs. The log pipeline (Fluentd, Logstash) ships to Elasticsearch or Loki for centralized querying.

881. Explain SLI, SLO, and SLA.

   **Answer:** SLI (Service Level Indicator) measures service performance (e.g., latency p99). SLO (Objective) is the target SLI value (e.g., 99.9% uptime). SLA (Agreement) is the contractual commitment with consequences for breach.

882. What are golden signals?

   **Answer:** The four golden signals are latency (response time), traffic (request rate), errors (failure rate), and saturation (resource utilization). Monitoring these provides a comprehensive service health view.

883. Explain incident response workflows.

   **Answer:** Incident workflows include detection (alert monitoring), triage (severity assessment), mitigation (rollback/hotfix), resolution, postmortem (blameless root cause analysis), and follow-up items.

884. How do startups optimize cloud costs?

   **Answer:** Optimize with right-sizing instances, reserved instances/committed use discounts, spot instances for batch workloads, auto-scaling to match demand, elimination of zombie resources, and multi-cloud arbitrage.

885. Explain Kubernetes namespaces.

   **Answer:** Namespaces provide virtual cluster isolation within a physical cluster. They scope resource quotas, network policies, RBAC, and object names. Common patterns include per-environment and per-team namespaces.

886. What are Helm charts?

   **Answer:** Helm charts package Kubernetes resources as reusable templates. Parameters are injected via `values.yaml`, enabling environment-specific configurations for the same application.

887. Explain Terraform basics.

   **Answer:** Terraform uses declarative HCL to provision infrastructure (AWS, GCP, K8s). It tracks state in `terraform.tfstate`, plans changes with `terraform plan`, and applies with `terraform apply`.

888. What are CI anti-patterns?

   **Answer:** Anti-patterns include building artifacts in production, long pipeline runtimes without parallel stages, hardcoded secrets, unreliable flaky tests, and deploying without versioned artifacts.

889. Explain deployment freeze strategies.

   **Answer:** Deployment freezes pause production deployments during high-risk periods (holidays, major events). During a freeze, only critical hotfixes go through expedited review and deployment.

890. How do you design enterprise CI/CD pipelines?

   **Answer:** Enterprise pipelines include lint → typecheck → unit test → build → integration test → security scan → SBOM generation → staging deploy → e2e test → canary deploy → production rollout with automatic rollback and approval gates.
