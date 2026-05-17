## 13. CI/CD + Docker (351–390)

351. What is CI/CD?
     CI/CD (Continuous Integration/Continuous Deployment) automates building, testing, and deploying code changes. CI automatically builds and tests every commit. CD automatically deploys passing code to staging or production environments.

352. Explain continuous integration.
     Continuous Integration merges all developer code changes into a shared repository multiple times daily. Each merge triggers automated builds and tests, catching integration bugs early and ensuring the codebase remains deployable.

353. What is continuous deployment?
     Continuous Deployment automatically deploys every change that passes the CI pipeline to production. It extends CI by making successful builds go live without manual approval, enabling rapid feature delivery and immediate user feedback.

354. Explain GitHub Actions.
     GitHub Actions is a CI/CD platform integrated with GitHub. Workflows defined in YAML files trigger on events (push, PR, schedule). Jobs run in parallel or sequentially on GitHub-hosted or self-hosted runners with reusable actions from the marketplace.

355. What are CI pipelines?
     CI pipelines are automated sequences of stages that code passes through: lint → test → build → (optional) deploy. Each stage runs specific tasks, and failure at any stage stops the pipeline, preventing bad code from progressing.

356. Explain build stages.
     Build stages are logical phases in a pipeline: install (dependencies), lint (code quality), typecheck (type errors), test (unit/integration), build (production bundles), and deploy (release to environment). Stages can run sequentially or in parallel.

357. What are deployment strategies?
     Strategies include: rolling update (gradually replace instances), blue-green (switch between two identical environments), canary (deploy to small subset first), feature flags (toggle features without deployment), and A/B testing (compare versions).

358. Explain blue-green deployments.
     Blue-green deployment maintains two identical environments. The blue (current) runs live traffic while green (new) is deployed and tested. A router switch moves traffic from blue to green, enabling instant rollback by switching back.

359. What is canary deployment?
     Canary deployment rolls out changes to a small percentage of users first, monitoring for errors and performance issues. If successful, the rollout gradually increases to 100%. If problems arise, only the canary subset is affected.

360. Explain rollback strategies.
     Rollback reverts to a previous known-good version. Strategies include: reverting the git commit (rebuilding), switching back traffic (blue-green), restoring database backups (data rollback), and feature flags to disable broken features instantly.

361. What is Docker?
     Docker is a containerization platform that packages applications and their dependencies into lightweight, portable containers. Containers run consistently across environments, eliminating "works on my machine" problems.

362. Difference between containers and VMs?
     Containers share the host OS kernel, starting in seconds with minimal overhead. VMs include a full guest OS, consuming more resources and starting in minutes. Containers are process-isolated, VMs provide hardware-level isolation.

363. Explain Docker images.
     Docker images are read-only templates with instructions for creating containers. They consist of layers built from a Dockerfile, are stored in registries, and are versioned with tags. Images are immutable and used to instantiate containers.

364. What are Docker layers?
     Each Dockerfile instruction creates a cacheable layer. Layers are stacked for image composition — changes only rebuild affected layers and above. Layer caching speeds up builds, and well-ordered Dockerfiles minimize rebuild time.

365. Explain Dockerfile instructions.
     Key instructions: `FROM` (base image), `WORKDIR` (working directory), `COPY`/`ADD` (files), `RUN` (commands during build), `EXPOSE` (ports), `ENV` (environment variables), `CMD`/`ENTRYPOINT` (container startup command).

366. What is multi-stage build?
     Multi-stage builds use multiple `FROM` statements in one Dockerfile. Earlier stages build artifacts (with build tools), later stages copy only runtime files to a slim final image. This produces smaller production images without build dependencies.

367. Explain Docker Compose.
     Docker Compose defines multi-container applications in a `docker-compose.yml` file. It configures services, networks, volumes, environment variables, and dependencies. `docker-compose up` starts the entire stack with one command.

368. What are container registries?
     Container registries store and distribute Docker images. Examples include Docker Hub, GitHub Container Registry, AWS ECR, and Google Artifact Registry. Registries support versioning, access control, vulnerability scanning, and pull-through caching.

369. Explain image optimization.
     Optimize by: using slim base images (alpine, distroless), multi-stage builds, minimizing layers (combine RUN commands), cleaning package manager caches, removing unnecessary files, and using `.dockerignore` to exclude development files.

370. What are Docker volumes?
     Volumes persist data generated by containers beyond their lifecycle. They are stored on the host filesystem and can be shared between containers. Types include bind mounts (host directory) and named volumes (Docker-managed storage).

371. Explain container networking.
     Docker networks enable communication between containers. Bridge networks connect containers on the same host. Host networks share the host's network stack. Overlay networks connect containers across multiple hosts in a swarm or Kubernetes cluster.

372. What is orchestration?
     Orchestration automates container deployment, scaling, networking, and lifecycle management. It handles service discovery, load balancing, health checks, rolling updates, and resource allocation across clusters of machines.

373. Explain Kubernetes basics.
     Kubernetes is a container orchestration platform. Key concepts: Pods (smallest deployable units), Deployments (declarative updates), Services (stable networking), ConfigMaps/Secrets (configuration), and Ingress (external access).

374. What are pods?
     Pods are the smallest deployable units in Kubernetes, containing one or more containers that share storage, network, and lifecycle. Containers in a pod share the same IP and port space, and are scheduled together on the same node.

375. Explain scaling containers.
     Horizontal scaling adds/removes container instances based on load. Kubernetes `HorizontalPodAutoscaler` adjusts replicas based on CPU/memory metrics. Vertical scaling adjusts container resources (CPU/RAM). Auto-scaling with custom metrics for business-specific triggers.

376. What is infrastructure as code?
     IaC manages infrastructure (servers, networks, databases) through machine-readable definition files rather than manual configuration. Tools like Terraform, Pulumi, and CloudFormation enable versioned, repeatable, and auditable infrastructure provisioning.

377. Explain environment promotion.
     Environment promotion moves code through stages: development → staging → production. Each stage runs tests and validations. Artifacts built once in CI are promoted without rebuilding, ensuring the exact same binary reaches production.

378. What are secrets managers?
     Secrets managers securely store and provide access to sensitive data (API keys, passwords, tokens). Examples: HashiCorp Vault, AWS Secrets Manager, Doppler. They offer encryption, access control, audit logging, and automatic rotation.

379. Explain observability.
     Observability measures system health through three pillars: logs (events), metrics (numerical measurements), and traces (request flows). It enables debugging, performance monitoring, and alerting in production systems.

380. What is centralized logging?
     Centralized logging aggregates logs from all services into one searchable platform (ELK Stack, Grafana Loki, Datadog). It enables correlation across services, historical analysis, real-time monitoring, and alerting on error patterns.

381. Explain metrics and monitoring.
     Metrics are time-series data points (CPU, memory, request latency, error rate). Monitoring collects, visualizes, and alerts on metrics using tools like Prometheus and Grafana. SLIs (indicators), SLOs (targets), and SLAs (agreements) define reliability goals.

382. What are health checks?
     Health checks are endpoints (liveness, readiness, startup) that Kubernetes and load balancers poll to determine container health. Liveness detects crashed containers, readiness determines traffic eligibility, startup delays initial checks for slow-starting apps.

383. Explain zero downtime deployment.
     Zero downtime deployment ensures application availability during updates using rolling updates (gradually replacing instances), blue-green environments, or canary releases. Requires graceful shutdown handling, database migration compatibility, and load balancer draining.

384. What are sidecar containers?
     Sidecar containers run alongside the main application container in the same pod, providing auxiliary functionality. Examples: log shippers (Fluentd), proxy (Envoy), config reloaders, and service mesh proxies (Istio).

385. Explain Docker security best practices.
     Best practices: use minimal base images, run as non-root user, scan for vulnerabilities, sign images, avoid secrets in Dockerfiles (use build args or secrets mounts), restrict capabilities, enable read-only root filesystem, and regularly update base images.

386. What are ephemeral environments?
     Ephemeral environments are short-lived, isolated deployments created per branch or PR that automatically destroy after merging. They enable preview testing in production-like conditions without permanent infrastructure costs.

387. Explain CI caching.
     CI caching stores dependencies (node_modules, pip packages) between pipeline runs. It speeds up builds by avoiding re-downloading packages. Strategies include caching entire directories, layer caching for Docker builds, and incremental compilation.

388. How do you debug CI failures?
     Debug by: checking pipeline logs for error messages, reproducing locally with similar conditions, checking environment variables and secrets, reviewing recent code changes, using `--verbose` flags, adding temporary debug output, and checking runner resource limits.

389. Explain automated testing in pipelines.
     Pipelines run linting, type checking, unit tests, integration tests, E2E tests, and security scans. Tests gate deployments — failures block promotion. Parallel test execution, test splitting, and selective test runs optimize pipeline speed.

390. How do startups structure deployments?
     Startups typically start with simple GitHub Actions or Vercel deployments, adding Docker and staging environments as they grow. Common stack: GitHub Actions → Docker → single server or fly.io/Railway → Kubernetes when needed for scaling.
