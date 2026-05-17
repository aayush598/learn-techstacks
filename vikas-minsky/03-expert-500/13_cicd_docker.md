## 51. CI/CD + Docker Expert Topics (1351–1390)

1351. How do distributed build systems work?

   **Answer:** Distributed build systems (Bazel, Nx, Turborepo) split build tasks into a dependency graph executed across multiple workers. Remote caching stores artifacts in shared storage (S3, GCS), so workers fetch pre-built outputs instead of rebuilding.

1352. Explain hermetic builds.

   **Answer:** Hermetic builds execute in isolated environments with pinned toolchains and explicit dependencies, producing identical outputs regardless of the host machine. This eliminates "works on my machine" problems and enables deterministic caching.

1353. What are reproducible deployment pipelines?

   **Answer:** Reproducible pipelines use version-locked base images, checksummed dependencies, and idempotent scripts to ensure the same commit always produces the same deployment artifact, regardless of when or where it's built.

1354. Explain ephemeral preview environments.

   **Answer:** Ephemeral preview environments spin up per-pull-request stacks with isolated databases, services, and DNS names. They auto-destroy when the PR merges or closes, providing realistic integration testing without permanent resource cost.

1355. How does deployment orchestration coordinate services?

   **Answer:** Deployment orchestration (Kubernetes, Nomad) coordinates service rollouts by managing dependencies, health checks, and rollout order (canary → staging → production). Failed checks pause the pipeline and trigger automatic rollback.

1356. Explain deployment dependency graphs.

   **Answer:** Dependency graphs model which services must be deployed before or after others based on API dependencies, database migrations, and message queue schemas. Tools like Argo Rollups and Spinnaker enforce this ordering.

1357. What are release orchestration strategies?

   **Answer:** Release strategies include blue/green (full environment swap), canary (gradual traffic shifting), rolling (instance-by-instance), and A/B testing (route-based). Each balances deployment speed, risk, and rollback complexity.

1358. Explain progressive traffic shifting.

   **Answer:** Progressive traffic shifting moves a percentage of traffic to the new version incrementally (1% → 5% → 25% → 100%), monitoring error rates and latency at each step. Automatic rollback occurs if metrics degrade.

1359. How do service meshes control traffic?

   **Answer:** Service meshes (Istio, Linkerd) inject sidecar proxies that manage traffic routing, retries, timeouts, and mTLS between services declaratively. This decouples traffic management from application code.

1360. Explain Kubernetes reconciliation loops.

   **Answer:** Reconciliation loops in controllers continuously observe cluster state, compare it to desired state (defined in specs), and take action to converge them. This event-driven loop handles failures, scaling, and configuration changes.

1361. What are controller patterns?

   **Answer:** Controller patterns implement a control loop that watches resources, reads desired state from specs, and writes status updates. Custom controllers extend Kubernetes for domain-specific automation like database backups.

1362. Explain autoscaler decision-making.

   **Answer:** Horizontal Pod Autoscaler monitors metrics (CPU, memory, custom metrics) and computes desired replica count using the formula: `ceil(currentReplicas × currentMetric / targetMetric)`. Cooldown periods prevent thrashing.

1363. How does Kubernetes etcd store state?

   **Answer:** etcd stores all cluster state as key-value pairs with watch support for change notifications. It uses the Raft consensus protocol for consistency, and its performance depends on disk I/O latency—slow disks can bottleneck the control plane.

1364. Explain pod disruption budgets.

   **Answer:** Pod Disruption Budgets (PDBs) limit how many pods can be unavailable simultaneously during voluntary disruptions (node drain, cluster upgrades). `minAvailable` or `maxUnavailable` guarantees service availability during maintenance.

1365. What are topology spread constraints?

   **Answer:** Topology spread constraints enforce pod distribution across failure domains (zones, regions, nodes) to improve resilience. `maxSkew` limits how imbalanced the distribution can be, while `whenUnsatisfiable` defines behavior when constraints can't be met.

1366. Explain horizontal pod autoscaling metrics.

   **Answer:** HPA can use resource metrics (CPU, memory), custom metrics (requests per second, queue length), or external metrics (SQS queue depth, Cloud Monitoring). Multiple metrics are evaluated, and the highest desired replica count wins.

1367. How do node pools improve scalability?

   **Answer:** Node pools group nodes by hardware type (GPU, high-memory) or region, enabling workload-specific placement. Cluster autoscaler scales node pools independently, adding nodes when pending pods request pool resources.

1368. Explain workload affinity rules.

   **Answer:** Affinity rules include `nodeAffinity` (prefer/require specific nodes), `podAffinity` (co-locate related pods), and `podAntiAffinity` (spread pods across failure domains). These optimize latency and availability.

1369. What are immutable deployment patterns?

   **Answer:** Immutable deployments replace entire instances instead of updating in-place. New instances are created with the new version, health-checked, and traffic is switched over, enabling instant rollback by reverting to the old instance group.

1370. Explain cluster observability pipelines.

   **Answer:** Cluster observability pipelines collect logs (Fluentd, Vector), metrics (Prometheus), traces (OpenTelemetry), and events, forwarding them to centralized stores (Elasticsearch, Grafana Loki, Tempo) for querying and alerting.

1371. How do tracing systems correlate services?

   **Answer:** Distributed tracing propagates a trace ID through HTTP headers (W3C trace context), correlating spans across services. Each service enriches the trace with its span ID, duration, and metadata for end-to-end request visualization.

1372. Explain centralized metrics aggregation.

   **Answer:** Prometheus scrapes metrics from exporters at regular intervals, storing them as time-series data. Thanos or Cortex provide long-term storage and global querying across multiple clusters, while Grafana visualizes dashboards.

1373. What are deployment rollback guarantees?

   **Answer:** Rollback guarantees require the previous deployment artifact to be immediately available, database migrations to be backward-compatible, and health checks to validate the rollback succeeded. Canary analyses can trigger automatic rollback.

1374. Explain CI pipeline bottleneck analysis.

   **Answer:** Bottleneck analysis identifies slow stages using timing metrics, parallelization opportunities, cache hit rates, and dependency resolution overhead. Tracing pipeline executions reveals optimization targets.

1375. How do monorepo pipelines scale?

   **Answer:** Monorepo pipelines scale with affected-project detection (Nx, Turborepo), parallel task execution, distributed caching, and selective CI that only builds/test changed projects and their dependents.

1376. Explain artifact signing.

   **Answer:** Artifact signing uses cryptographic signatures (GPG, Sigstore/Cosign) to verify artifact integrity and provenance. Signatures are attached to container images, binaries, and packages, verified at deployment time to prevent tampered artifacts.

1377. What are software supply chain attacks?

   **Answer:** Supply chain attacks compromise dependencies or build infrastructure to inject malicious code. Mitigations include dependency pinning, SBOM generation, signed commits, image scanning (Trivy, Snyk), and SLSA compliance.

1378. Explain infrastructure policy enforcement.

   **Answer:** Policy enforcement (OPA/Gatekeeper, Kyverno) defines rules for resource configurations—ensuring all containers have resource limits, no privileged containers, required labels, and approved registries—denying non-compliant resources.

1379. How do startup teams manage cloud governance?

   **Answer:** Startup teams manage cloud governance with infrastructure-as-code (Terraform/Pulumi), tagging strategies for cost allocation, budget alerts, and IaC policy checks in CI that prevent costly misconfigurations before deployment.

1380. Explain disaster recovery planning.

   **Answer:** Disaster recovery defines RTO (Recovery Time Objective) and RPO (Recovery Point Objective) with strategies like active-passive (warm standby), active-active (multi-region), and periodic backup restoration testing.

1381. What are region failover strategies?

   **Answer:** Region failover strategies route traffic to a secondary region when the primary degrades. Approaches include DNS-based failover (Route53), global load balancers, and database replication lag monitoring to determine failover readiness.

1382. Explain infrastructure scalability testing.

   **Answer:** Scalability testing uses load tools (k6, Locust, wrk2) to identify breaking points, combined with horizontal pod autoscaling and cluster autoscaler validation. Tests measure latency, error rate, and resource utilization under increasing load.

1383. How do cost-aware schedulers work?

   **Answer:** Cost-aware schedulers (Karpenter, CAST AI) select instance types and regions based on spot pricing, reserved instance availability, and workload resource requirements. They balance cost reduction with availability and performance.

1384. Explain container image provenance.

   **Answer:** Image provenance tracks the origin and history of a container image through signed metadata, including the build system, base images, source commit, and build environment. This is verified before deployment.

1385. What are runtime sandboxing strategies?

   **Answer:** Runtime sandboxing strategies use gVisor, Kata Containers, or Firecracker microVMs to isolate containers with additional kernel-level security boundaries. These prevent container escapes from compromising the host.

1386. Explain Kubernetes operator patterns.

   **Answer:** Operators extend Kubernetes with custom controllers that manage complex stateful applications (databases, message queues). They encode domain knowledge into reconciliation logic, automating backups, upgrades, and scaling.

1387. How do platform engineering teams operate?

   **Answer:** Platform engineering teams build internal developer platforms (IDPs) with self-service infrastructure, golden paths, and paved roads. They abstract cloud complexity behind a unified API, providing templates and guardrails.

1388. Explain deployment dependency isolation.

   **Answer:** Dependency isolation ensures that changes to one service's deployment don't cascade to others. Techniques include API versioning, schema compatibility checks, contract testing, and independent release cycles.

1389. What are infrastructure anti-patterns?

   **Answer:** Infrastructure anti-patterns include snowflake servers (manual configuration), pet vs cattle (treating instances as irreplaceable), over-provisioning (wasting cost), under-provisioning (affecting reliability), and ignoring cost visibility.

1390. How do elite startups engineer deployment systems?

   **Answer:** Elite startups engineer deployment systems with fully automated CI/CD, canary deployments with observability-driven promotion, ephemeral environments per PR, infrastructure-as-code with policy enforcement, and post-mortem driven improvement.
