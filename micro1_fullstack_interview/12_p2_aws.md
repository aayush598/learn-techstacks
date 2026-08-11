# Priority 2 — AWS (Q355–Q373)

**Why these matter for micro1:** AWS is a listed requirement ("cloud environments like AWS"). Expect core services (EC2/S3/RDS/Lambda/ECS/IAM), deployment of FastAPI + React + Postgres, secrets, monitoring, and scaling.

---

## Q355: What AWS services have you used?

**Answer with a story:** "I've deployed and operated services on AWS: **EC2** (compute), **RDS/Aurora PostgreSQL** (databases), **S3** (storage), **ECS/Fargate** (containers), **Lambda** (serverless), **ALB + Target Groups** (routing), **CloudWatch** (metrics/logs/alarms), **IAM** (roles/policies), **Secrets Manager**, **SQS** (queues), **CloudFront/Route 53**."

Then **one concrete example**: "For my resume-processing pipeline I ran FastAPI on ECS behind an ALB, processed jobs with SQS + workers, stored resumes in S3, and used Aurora PostgreSQL with a PgBouncer-style pool."

> Follow-up prep: be ready to describe the architecture diagram and why you chose each service.

---

## Q356: What is EC2?

**Elastic Compute Cloud** — AWS's **virtual servers** (instances).

- Rent VMs by type (CPU/RAM/GPU), size, OS (Amazon Linux, Ubuntu).
- Billing: per-second on-demand; savings with Reserved/Spot instances.
- You manage the OS, runtime, security patches, and scaling (ASG) yourself.
- Use cases: full control workloads, custom runtimes, legacy apps, GPU (LLM inference!).
- **vs container/serverless:** more ops burden; prefer ECS/Lambda unless you need control or a specific runtime.

---

## Q357: What is S3?

**Simple Storage Service** — AWS's **object storage** (files as objects in buckets, with keys).

- **Unlimited scale**, 99.999999999% (11 nines) durability, low cost.
- Features: versioning, lifecycle policies (move to Glacier), server-side encryption, static website hosting, presigned URLs (secure uploads/downloads).
- **Use cases for micro1:** resume PDFs, processed documents, backups, static assets, model artifacts, logs; **presigned URLs** so candidates upload resumes directly to S3 without your API handling bytes.
- Not a filesystem (no POSIX); millions of small objects need different access patterns (e.g., S3 select/athena for analytics).

---

## Q358: What is RDS?

**Relational Database Service** — **managed** relational databases: PostgreSQL, MySQL, SQL Server, MariaDB, Oracle.

- AWS handles: patching, backups (snapshots/PITR), replication, failover, monitoring, auto-scaling storage.
- **Aurora** — AWS's compatible engine (Postgres/MySQL), more performant, scale-out read replicas, serverless option.
- **You still tune:** instance size, parameters, indexes, connection limits (use PgBouncer/`max_connections`).

For micro1: RDS/Aurora PostgreSQL is the standard managed home for the recruiting data.

---

## Q359: What is Lambda?

AWS's **serverless function service** — run code (Python/Node/etc.) in response to events without managing servers.

- Triggers: API Gateway, S3 events, SQS, EventBridge, timers (cron), DynamoDB streams.
- Billed by **invocations + execution time** (ms) + memory; scales automatically to thousands of concurrent invocations.
- **Limits:** max 15-min timeout (now up to 15 min; historically), memory up to 10GB, stateless (no local persistence), cold starts (~100ms–1s, worse for Python + big deps).
- **Best for:** event-driven glue, image/resume processing, webhooks, scheduled jobs, API endpoints (with API Gateway).
- **Not ideal for:** long-running websockets, heavy compute, low-latency hot paths (cold starts).

**For the AI recruiter:** Lambda for event glue (resume upload → trigger parse); heavy/conversational API better on ECS/Fargate.

---

## Q360: What is ECS?

**Elastic Container Service** — run **Docker containers** on AWS.

- Two launch modes: **Fargate** (serverless — AWS runs the containers, you pay per vCPU/RAM; simplest) and **EC2** (you manage the instances; more control/cheaper at scale).
- Orchestration: task definitions (image, CPU/memory, env, ports), services (count + rolling deploy), scaling policies, target groups for ALB.
- **vs EKS** (Kubernetes, Q615–616): ECS is simpler, AWS-managed; EKS is more portable but more ops.
- **For FastAPI at micro1:** Fargate task + ALB + autoscaling is the sweet spot.

---

## Q361: What is CloudWatch?

AWS's **observability service**: metrics, logs, alarms, dashboards, events.

- **Metrics:** CPU, memory (via agent), request counts, custom app metrics; retention tiers.
- **Logs:** CloudWatch Logs — app stdout, query with Logs Insights.
- **Alarms:** threshold → SNS/SES notifications, autoscaling actions.
- **X-Ray:** distributed tracing (optional add-on).
- **For FastAPI:** log structured JSON, publish custom metrics (request latency, queue depth, LLM cost), alarm on 5xx/p95/queue backlog.

---

## Q362: What is IAM?

**Identity and Access Management** — AWS's system for **who can do what** (users, groups, roles, policies).

- **Users** (people), **groups**, **roles** (assumed by services), **policies** (JSON: effect + action + resource).
- **Least privilege** (Q617–618): give only needed permissions.
- **Roles > keys:** EC2/ECS/Lambda assume roles (temporary credentials via STS) instead of storing access keys.
- MFA for humans, password/access-key policies, federation (SSO/OAuth).

```json
{ "Effect": "Allow", "Action": "s3:PutObject",
  "Resource": "arn:aws:s3:::resumes-bucket/*" }
```

**Answer:** "IAM is the security boundary — I use roles with scoped policies for every service, never root, never long-lived keys where a role works."

---

## Q363: What is a security group?

A **virtual firewall** at the ENI (instance/task) level — controls inbound/outbound traffic by port/protocol/source.

```text
Inbound: 443 from 0.0.0.0/0        # public HTTPS
         5432 from sg-app            # Postgres only from the app's SG
Outbound: all (or restricted)
```

- **Stateful:** return traffic auto-allowed.
- **SG-to-SG rules** — reference other security groups instead of IPs (e.g., app SG → DB SG).
- **vs NACL** (stateless, subnet-level): use SGs primarily; NACLs as a second layer.
- Apply **least privilege**: DB ports only reachable from app SG, SSH only from your VPN/office IP.

---

## Q364: How would you deploy a FastAPI application on AWS?

**Reference architecture (state it):**

1. **Code:** Docker image (multi-stage build, Q383).
2. **Registry:** push to **ECR**.
3. **Compute:** **ECS Fargate** service with N tasks (FastAPI + Uvicorn workers).
4. **Routing:** **Application Load Balancer** (HTTPS via ACM cert) → target group → tasks.
5. **DB:** RDS/Aurora PostgreSQL (private subnet).
6. **Secrets:** Secrets Manager, injected as env at task launch (Q367).
7. **Storage:** S3 for resumes/artifacts (Q357).
8. **Queues:** SQS for background jobs (resume parsing, LLM batch) (Q611).
9. **Monitoring:** CloudWatch metrics/logs/alarms (Q368).
10. **Scaling:** autoscaling on CPU/requests (Q369).
11. **Networking:** VPC with public/private subnets (Q600–604).
12. **CI/CD:** GitHub Actions → build → ECR → ECS deploy (Q621).

```yaml
# task definition sketch
{ "family": "zara-api", "taskRoleArn": "arn:...", 
  "containerDefinitions": [{ "image": "ecr.../zara:latest",
    "portMappings": [{"containerPort": 8000}], "cpu": 1024, "memory": 2048,
    "secrets": [{"name": "LLM_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."}] }]}
```

---

## Q365: How would you deploy a React/Next.js application on AWS?

**Options:**

1. **Next.js on ECS/Fargate** (Node server) behind **CloudFront** or ALB — full SSR + route handlers. Best when you need the Node server.
2. **Vercel** (managed) — simplest for Next.js, but micro1/AWS-flavored answers usually stay on AWS.
3. **Static export + S3 + CloudFront** — build with `next export`; serves static files at the edge. Works for CSR/static; not for SSR/route handlers.
4. **Lambda + Next.js** (via serverless adapters/`serverless-nextjs`) — SSR on Lambda behind CloudFront.

**For a chat/dashboard app:** Next.js on Fargate (or Vercel) + CloudFront in front; API calls to FastAPI (Q324); static assets/CDN optimized.

---

## Q366: How would you deploy PostgreSQL on AWS?

1. **RDS PostgreSQL (managed)** — recommended: automated backups/PITR, Multi-AZ failover, patching, monitoring, scaling storage.

```text
RDS: multi-AZ (standby in another AZ), automated snapshots, PITR to 5 min,
read replicas for reporting, encryption at rest (KMS) + in transit (TLS).
```

2. **Aurora PostgreSQL** — higher throughput, auto-scaling readers, serverless v2.
3. **Self-managed on EC2** — full control, but you own backups/patching/failover; only for specific needs (extensions/versions).

**Best practices to mention:** private subnet (only app SG access), **PgBouncer** on EC2/Fargate for connection pooling, `max_connections` awareness, backups + restore drills, monitoring (Q630), no public access.

---

## Q367: How would you store application secrets in AWS?

1. **AWS Secrets Manager** (Q609) — API keys, DB creds; **automatic rotation**; IAM-controlled access.
   - ECS/Lambda read secrets at runtime via `secretsmanager:GetSecretValue` (injected as env or retrieved by the app).
2. **Parameter Store** (Q610) — simpler config strings + secure strings (cheap); use for non-sensitive config, Secrets Manager for real secrets.
3. **Never:** in the Docker image, in code, in env committed to git, in ECS task definitions as plaintext.

```yaml
# ECS task definition
"secrets": [{ "name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:us-east-1:...:secret:prod/db-password" }]
```

- **IAM roles** give the app permission; rotation minimizes blast radius; encrypt at rest with KMS.

---

## Q368: How would you monitor a production application on AWS?

**Layer it:**
1. **CloudWatch metrics** — CPU, memory, request count, 4xx/5xx, latency (ALB), queue depth, DB connections.
2. **Logs** — CloudWatch Logs from ECS/Fargate; structured JSON; Logs Insights queries.
3. **Custom metrics** — publish app-level metrics (LLM latency, token cost, cache hit rate) via `put-metric-data`.
4. **Alarms + notifications** — CloudWatch Alarms → SNS → email/Slack/PagerDuty: 5xx spike, p95 latency, queue backlog, DB disk/connections.
5. **Dashboards** — CloudWatch Dashboard (or Grafana/Prometheus via Prometheus Agent) for the whole system.
6. **Distributed tracing** — AWS X-Ray / OpenTelemetry (Q632).
7. **Health checks** — ALB health check on `/healthz`; auto-restart failed tasks.
8. **Synthetic checks** — Route 53 health checks / CloudWatch Synthetics pinging critical endpoints.
9. **Cost monitoring** — budgets + anomaly detection (Q620).

---

## Q369: How would you scale a backend service on AWS?

1. **Vertical** (upgrade instance size) — quick, limited, expensive (Q371).
2. **Horizontal** — add instances/tasks behind a load balancer (Q370).
3. **Auto Scaling Groups (EC2)** or **ECS service auto-scaling / Application Auto Scaling** — scale on:
   - CPU/memory utilization targets.
   - Request count (per ALB target).
   - **Custom metrics** (queue depth, in-flight LLM calls) for event-driven scaling.
4. **Serverless (Lambda)** — auto-scales implicitly; good for spiky/event-driven work.
5. **Database scaling** — read replicas for reads (Q566); connection pooling (PgBouncer) so scale-out doesn't hit connection limits.
6. **Statelessness** — app must be stateless (sessions/cache in Redis/Elasticache) for horizontal scaling to work (Q582).
7. **Queues for async** — decouple bursts with SQS; workers scale on backlog (Q611, Q431).
8. **Caching** — Redis/CDN to cut origin load (Q248, Q436).

---

## Q370: What is horizontal scaling?

Adding **more instances/nodes** to handle load (scale out/in), each handling a share of requests behind a **load balancer**.

- **Scales beyond a single machine's limit**; high availability (a failed node doesn't take the app down).
- Requires **stateless design** — no per-instance sessions/state (put them in Redis/DB) (Q582).
- Distribution: ALB round-robin/least-connections; database via read replicas; queues via worker instances.
- **vs vertical (Q371):** horizontal = elasticity + resilience; vertical = simple but a single point of failure + hard ceiling.

**For FastAPI:** stateless API tasks + ALB + autoscaling on CPU/requests is textbook horizontal scaling.

---

## Q371: What is vertical scaling?

Upgrading the **size of a single machine** (more CPU/RAM/disk) to handle more load (scale up/down).

- Simple (no architecture change), but:
  - **Hard ceiling** — the biggest instance type caps you.
  - **Single point of failure** — the instance dies, the app dies.
  - **Cost** — large instances have diminishing returns (prices grow super-linearly).
  - Requires **restart/downtime** for the resize (usually).
- Use for: stateful workloads (databases — first lever), small spikes, or when horizontal scaling isn't possible.
- **Rule:** scale DB vertically first, app horizontally.

---

## Q372: What is a load balancer?

A device/service that **distributes incoming traffic across multiple backend targets** (instances/tasks/containers).

- **Application Load Balancer (ALB):** layer 7 (HTTP/HTTPS) — path/host routing, WebSocket support, SSL termination, health checks, sticky sessions.
- **Network Load Balancer (NLB):** layer 4 (TCP/UDP) — ultra-low latency, huge throughput, for raw TCP/gRPC.
- **Gateway Load Balancer / Classic LB** — less common.
- Benefits: HA (targets balanced), **scalability** (add/remove targets), **health checks** (traffic routed only to healthy), SSL termination, routing rules (e.g., `/api` → FastAPI, `/` → Next.js).

---

## Q373: How would you design a highly available backend on AWS?

**HA = no single point of failure across the stack:**

1. **Multi-AZ** — run everything in ≥2 availability zones (VPC across AZs, Q600).
2. **Load balancer (ALB)** in front of the app — distributes traffic, health-checks, removes unhealthy targets.
3. **Stateless app tasks** — ECS/Fargate with ≥2 tasks across AZs; autoscaling (Q369).
4. **Managed DB with Multi-AZ** — RDS/Aurora Multi-AZ: automatic failover to standby; read replicas in another AZ (Q566).
5. **Elasticache Redis** (multi-AZ) for sessions/cache.
6. **Redundancy everywhere:** S3 is redundant by design; SQS/SNS regional; Route 53 DNS failover.
7. **Health + self-healing:** health checks, auto-restart/replace unhealthy tasks, ASG replaces failed EC2.
8. **Backups + DR:** RDS snapshots/PITR, S3 versioning, documented restore playbook (Q619).
9. **Graceful degradation** — circuit breakers + fallbacks so a failing dependency doesn't cascade (Q445, Q740).
10. **Runbooks + monitoring** — alarms trigger the right response (Q368, Q635).
11. **Test it** — chaos drills: kill an AZ/task/DB node and prove the app survives.
