# Priority 4 — Advanced AWS (Q600–Q620)

**Why these matter for micro1:** the Zara platform runs on AWS (that's the stack in the job description). Deeper AWS questions: networking (VPC), load balancing + autoscaling, CDN, messaging, IAM, disaster recovery, and cost.

---

## Q600: What is a VPC, and why do you need one?

**VPC (Virtual Private Cloud)** = your **isolated private network** inside AWS — your own subnet, IP ranges, routing, and security boundaries.

**Core concepts:**
- **CIDR block** — the IP range (`10.0.0.0/16` = 65k addresses).
- **Subnets** — partitions within the VPC. **Public subnets** have an internet gateway (for load balancers/NAT); **private subnets** don't (for app servers, DBs).
- **Route tables** — where traffic goes (internet, NAT, peered VPC).
- **Internet Gateway (IGW)** — the door to the internet (public).
- **NAT Gateway** — lets *private* instances reach the internet outbound (pull images, call APIs) without being reachable inbound.
- **Security Groups** (instance firewalls) + **NACLs** (subnet firewalls).
- **VPC Peering / Transit Gateway** — connect VPCs.

**Why you need it (security):** put the DB in a **private subnet with no internet route** — only the app (same VPC, via SG allowlist) can reach it; bastion/VPN for admin access; never expose Postgres publicly (Q402).

---

## Q601: Security groups vs NACLs?

| | **Security Group (SG)** | **NACL** |
|---|---|---|
| Level | **Instance** (virtual firewall) | **Subnet** |
| State | **Stateful** (return traffic auto-allowed) | **Stateless** (must allow both directions explicitly) |
| Rules | Allow only | Allow + Deny |
| Default | Deny inbound, allow all outbound | Allow all |
| Evaluated | At instance | At subnet (before SG) |
| Use | Per-service firewall (DB only from app SG) | Coarse subnet-level guard / deny lists |

**Rules of thumb:** use SGs for virtually everything (DB SG allows 5432 from only the app SG, Q600); use NACLs for a cheap global deny (block known-bad CIDRs) or when you need explicit DENY. Remember **stateless** — a NACL must have matching inbound+outbound rules or you'll mysteriously lose connectivity.

---

## Q602: How does an Application Load Balancer (ALB) work?

**ALB (L7, HTTP/HTTPS)** distributes traffic to targets:

- **Listeners** — port/protocol (e.g., `HTTPS :443`).
- **Rules** — path/host/header-based routing (`/api/*` → backend, `/*` → frontend, `ws` upgrade handling for WebSockets).
- **Target groups** — instances (ASG, Q604) or IPs; **health checks** (HTTP `GET /health`) mark unhealthy targets out; **connection draining** lets in-flight requests finish before a target is de-registered (critical for your SSE streams — Q431).
- **Sticky sessions** (if needed) via cookie; **TLS termination** at the ALB (certificates via ACM).
- Scales automatically to traffic; free with EC2 usage.

**Your architecture:** one ALB in public subnets; rules: `/api/*` → FastAPI target group, `/ws` → chat service, everything else → Next.js. Health checks on `/healthz`; WebSocket + streaming supported (target keepalive/timeouts tuned, Q399).

---

## Q603: How does an Auto Scaling Group (ASG) work?

**ASG** maintains a **minimum/maximum/desired** number of instances and scales based on triggers:

- **Launch template** — AMI, instance type, key, SG, user-data.
- **Scaling policies:**
  - **Target tracking** — keep avg CPU at 50% (or requests/instance, custom metric).
  - **Scheduled** — predictable ramp-ups (hiring season peaks).
  - **Manual/step** — alerts-driven.
- **Health checks** — instance + ELB health; replaces unhealthy instances.
- **Availability zones** — spreads across AZs for HA (Q436).
- **Cooldowns** — don't scale down/up too fast (flapping).

**Design for scale-out to *work*:** instances must come up **stateless** (config from launch template + env; DB/Redis/cache external — Q82, Q430). Slow boots (a 5-minute image build) mean you need to **pre-warm** or use target-tracking with headroom. Scale-in **must be safe**: connection draining (Q602) so streaming chats aren't cut.

---

## Q604: How do you deploy a web app on AWS? (overall)

**The standard production path (this is the "how would you deploy the recruiter" answer):**

1. **Code → CI** (GitHub Actions/CodePipeline): lint, typecheck, tests.
2. **Build artifacts:** container images (Docker) pushed to **ECR**; frontend static build to **S3**.
3. **Compute options:**
   - **ECS/Fargate** (containers, easiest ops) or **EKS** (k8s, if you need the ecosystem) — **recommended for FastAPI + workers**: same image runs API *and* the queue workers (different task defs).
   - **EC2 + ASG** (classic; more ops) — behind ALB.
   - **Lambda** for the parsing/notification workers (serverless, Q366).
4. **Frontend:** Next.js either on the same containers (SSR) or **static export on S3 + CloudFront** — or Next.js on Vercel (if allowed); your stack says AWS → put it behind **CloudFront**.
5. **Data layer:** **RDS Postgres** (Multi-AZ), **ElastiCache Redis**, **S3** for resumes.
6. **Routing:** **Route 53** → **CloudFront**/**ALB** → services. **WAF** + Shield in front.
7. **Deploy method:** blue/green or rolling via ECS/CodeDeploy; **canary** for risky AI-feature changes (Q621).
8. **Secrets + config:** **Secrets Manager/Parameter Store** (Q417); IAM roles for everything.

---

## Q605: What is CloudFront? When would you use it?

**CloudFront** = AWS's **CDN** (Q494): caches content at ~300+ **edge locations** worldwide and serves users from the nearest one.

**Uses:**
- **Static assets** — JS/CSS/images/resumes served from edge caches (huge latency + origin savings).
- **Dynamic/API acceleration** — TLS, HTTP/2/3, connection multiplexing to origin; it *can* cache API GETs with `Cache-Control` (public listings, Q495).
- **Web application firewall** (CloudFront + WAF: rate limits, OWASP rules).
- **Geographic restrictions, signed URLs** (private resume downloads — time-limited, per-user).
- **Lambda@Edge / CloudFront Functions** — rewrite/cache at the edge (A/B headers, redirects).

**For your app:** CloudFront in front of Next.js/ALB; **never** cache user-specific API responses at the edge (Q495 — resumes/scores are private); use **signed URLs** for private resume downloads from S3. Also cheap origin shield to protect the API from cache-miss storms.

---

## Q606: SQS vs SNS? When do you use each?

- **SQS (Simple Queue Service)** — a **queue** (at-least-once, one consumer per message, visibility timeouts, DLQ, retries). **Point-to-point:** producer → **one** consumer. This is your **work queue** (Q433): `parse_resume`, `match_candidate`, `send_email`.
- **SNS (Simple Notification Service)** — a **pub/sub topic** (fan-out): one publish → **many** subscribers (SQS queues, Lambda, email, HTTP). **Topic→subscribers.**
- **SNS + SQS = the classic pattern:** publish once to a topic → multiple SQS queues → each consumer gets a copy (event → parsers, notifiers, analytics all independently subscribe).

```text
resume_uploaded (SNS topic)
  ├──→ SQS: parse_resume       → parser worker
  ├──→ SQS: notify_candidate   → notifier
  └──→ Lambda: audit_index     → analytics
```

**Interview answer:** "SQS = work queue, one-to-one, with DLQ + visibility timeout; SNS = fan-out pub/sub; combine them when multiple downstream systems must react to one event."

---

## Q607: What is S3? What are the storage classes?

**S3 (Simple Storage Service)** — object storage: store any bytes under a key in a bucket, globally unique bucket names, 99.99% availability / 11-nines durability. **Objects, not files** — no POSIX, no mounting (unless you use EFS for that).

**Storage classes (cost vs access):**
- **Standard** — hot data (resumes being processed).
- **Intelligent-Tiering** — auto-moves between tiers by access pattern (no lifecycle config).
- **Standard-IA / One Zone-IA** — infrequent access, cheaper storage + retrieval fee.
- **Glacier Instant/ Flexible / Deep Archive** — archival: old transcripts, audit logs, 90-day-old resumes (retention policies, Q445).

**Key features:** versioning (recover overwrites/deletes), lifecycle rules (auto-move/expire), bucket policies + IAM (Q611), SSE encryption, presigned URLs (Q434), multipart upload, event notifications → SNS/SQS/Lambda (Q606), **eventual consistency** (read-your-writes now strong for new PUTs since 2020).

---

## Q608: What is IAM? Give the least-privilege pattern.

**IAM = Identity and Access Management** — who (identity) can do what (action) on which resource (ARN), governed by **policies** (JSON).

**Key pieces:**
- **Users** — humans/service accounts; **Groups** — bundle users with shared permissions; **Roles** — identities *assumed* by services/instances (preferred over storing keys).
- **Policies** — attach to users/groups/roles: `{Effect: Allow, Action: ["s3:GetObject"], Resource: "arn:aws:s3:::resumes/*"}`.
- **Trust policy** — who may assume a role.

**Least privilege pattern:**
- **Never use root creds / access keys in code** — every service assumes an **instance role** (EC2 role, ECS task role, Lambda role).
- **Scope actions + resources:** `s3:GetObject` only on the `resumes` bucket (not `s3:*`), `sqs:ReceiveMessage` only on its queue.
- **Scoped condition keys:** `aws:SourceIp`, `aws:ResourceTag`.
- **Rotate keys**; use **IAM Identity Center** for humans (SSO).
- **Audit** with CloudTrail (who did what, when).

**Interview answer:** "IAM grants access via policies; I use roles with least-privilege scoped to exact ARNs, never access keys in code, and audit everything with CloudTrail."

---

## Q609: What is a Lambda? What are its limits?

**Lambda** = serverless compute: run a function (Python, Node, etc.) on demand, pay per invocation+duration, auto-scale.

**Limits (name a few):**
- **Timeout** — max **15 min** (default 3s) → fine for notifications, not for long parsing batches.
- **Memory** — 128 MB – **10,240 MB** (proportional CPU).
- **Payload** — 6 MB sync, **256 KB async** (this breaks naive "put the whole resume in the event").
- **Concurrency** — account-level; **reserved concurrency** per function prevents one function starving another.
- **Ephemeral storage** — 512 MB – 10 GB (`/tmp`).
- **Cold starts** — first call spins a new sandbox (added latency; mitigate: provisioned concurrency, smaller deps).

**Your app:** notifications, webhook handlers, resume *trigger* (S3 event → enqueue), audit writes. **Not for:** the streaming AI chat (needs a long-lived connection) or long parses → use ECS/Fargate workers (Q604).

---

## Q610: How does S3 presigned URL work? Why use it?

**Presigned URL** = a URL with a **temporary signature** (the requester's credentials sign `GET`/`PUT` for a specific object, valid until expiry).

**Why:** you never stream file bytes through your API server — **offload the data path**:
- **Upload:** API authenticates the user, generates a `PUT` presigned URL (5 min TTL) → the **client uploads straight to S3** → API only stores the key → enqueues parse. Your servers never touch the MBs (Q434).
- **Download:** a short-lived `GET` URL for private resumes/transcripts — no public bucket, no long-lived links (Q495, Q607).

**Implementation notes:** sign with the app's IAM role (S3 keys not needed); scope the URL to the exact object; expiry 1–15 min (uploads) / 1–24h (downloads); log the grants (audit). This is the standard pattern for any media/document-heavy app.

---

## Q611: How do you secure S3? (bucket policies vs ACLs)

1. **Block all public access** by default (`BlockPublicAccess`) — the single biggest S3 security win; accidentally-public buckets are the classic breach.
2. **Bucket policy** — the access control document (allow/deny at bucket level, e.g., CloudFront-only via `aws:CloudFrontOriginAccessIdentity`, encryption requirements via `s3:x-amz-server-side-encryption` condition).
3. **IAM policies** — control *who* (roles) can access; combine with bucket policies.
4. **SSE-KMS / SSE-S3** — encryption at rest; **bucket versioning** + **MFA delete** for durability.
5. **Prevent leaks:** no real `resumes` bucket open; use **presigned URLs** (Q610) for user access; enable **S3 Access Logs / CloudTrail data events** for audit.
6. **ACLs** — legacy, disabled by default now; prefer bucket policies + IAM.

**Answer:** "Default-deny: block public access, IAM roles with scoped policies, presigned URLs for object access, KMS encryption, versioning, and data-plane logging."

---

## Q612: What is CloudWatch? What would you monitor?

**CloudWatch** = AWS's **metrics, logs, and alarms** service (Q631-adjacent):

- **Metrics** — standard (EC2 CPU, RDS, Lambda invocations/errors/duration, ALB request count/latency, SQS queue depth) + **custom metrics** (your app: `p95 latency`, `llm_cost_per_hour`, `queue_depth`, `screen_success_rate`).
- **Logs** — collect app/nginx/DB logs to **Log Groups**; searchable (CloudWatch Logs Insights).
- **Alarms** — threshold → SNS → pager/email/Slack; e.g., `SQS ApproximateNumberOfMessages > 5000 for 5 min` (worker backlog, Q439), `ALB 5xx > 1%`, `DB CPU > 80%`.
- **Dashboards** — one pane: QPS, error rate, latency p95/p99, LLM cost, queue depth, replication lag.

**What to monitor for the recruiter:** request/error/latency per endpoint (Q444), **time-to-first-token** for streaming, LLM spend, queue depths, worker success rates, DB connections + replica lag, **alarm on symptoms not metrics** (a queue at depth 5k means *something* is broken — alert on that).

---

## Q613: What is CloudTrail? Why does it matter?

**CloudTrail** records **API calls on your AWS account** — the audit log of *who did what*: `s3:PutObject` by role X, `iam:CreateUser`, console logins, and (with data events) S3 object access.

**Why it matters:**
- **Security/audit:** answer "who changed that bucket policy / deleted that object?" (Q608, Q631).
- **Incident response:** reconstruct timelines after a breach.
- **Compliance:** evidence for SOC2/GDPR audits.
- **Cost attribution:** correlation with CloudWatch for root-cause analysis.

**Practice:** enable in **all regions + organization-wide**, ship to S3 + SIEM/analytics, alert on sensitive actions (`iam:*`, `s3:*BucketPolicy`, security-group changes), guard access with least privilege (CloudTrail logs must be tamper-evident). CloudTrail answers "what happened"; CloudWatch answers "is it healthy now" — together they're observability (Q444).

---

## Q614: What is a circuit breaker in the cloud context? (Fault isolation)

**Cloud-native circuit breaker** = the same idea as Q438 applied to AWS dependencies, plus the *infrastructure* version:

- **App-level:** stop hammering a failing dependency (LLM provider, vector DB) — open circuit, fail fast, fall back (Q438).
- **AWS-level fault isolation:** **Multi-AZ** (an AZ failure shouldn't take you down), **availability zones as blast-radius boundaries** (spread ASG across AZs, DB standby in another AZ, Q436).
- **AWS-managed circuit-breaker-ish services:** ALB health checks + target de-registration; Route 53 **health-check failover** (route to a standby region if the primary is unhealthy); **autoscaling** as automatic fault replacement.

**Answer:** "I isolate failures with health checks (ALB/R53), redundant AZs/regions for the infrastructure, and app-level circuit breakers with timeouts + fallbacks for external dependencies — each layer stops cascading failure."

---

## Q615: What is the shared responsibility model?

**AWS is responsible for security OF the cloud; you're responsible FOR security IN the cloud.**

**AWS:**
- Physical data centers, hardware, network, **managed services'** core (RDS patches the DB engine, S3 infrastructure, Lambda runtime).
**You:**
- **Your data**, your IAM/users/policies, your app code and config, your network config (VPC, SGs, NACLs), your encryption choices (whether to use KMS, key rotation), your patch *schedule* for things you run (EC2 instances — you patch the OS; RDS AWS patches).

**Practical:** a breach isn't "AWS's fault" if the S3 bucket is public (Q611) or an IAM key leaked in code (Q608). Interviewers love this framing: "AWS secures the physical/managed layer; I own identity, data, and app-layer security."

---

## Q616: How do you implement disaster recovery (DR)?

**RPO (Recovery Point Objective)** — max acceptable data loss; **RTO (Recovery Time Objective)** — max acceptable downtime.

**Strategies (cost ↔ speed):**
1. **Backup & Restore** (cheapest, slowest): RDS automated snapshots + S3 bucket versioning; RTO hours, RPO ~minutes.
2. **Pilot light:** replicas (or a tiny replica stack) running in another region, ready to scale up. RTO ~tens of minutes.
3. **Warm standby:** a scaled-down but *running* full stack in DR region; RTO minutes.
4. **Multi-site active-active:** traffic split across two regions (Route 53 weighted + health checks); RTO ~0, highest cost/complexity.

**For your app:** RDS **Multi-AZ** handles AZ loss (not region loss). For regional DR: cross-region **read replicas** (promotable), S3 cross-region replication (or versioning + backup), AMIs/ECS images in the DR region, Route 53 failover. **Test the runbook** — an untested DR plan is a hope, not a plan. Answer with **"RPO/RTO first, then pick the tier that fits the budget."**

---

## Q617: How do you handle secrets in AWS?

**Secrets Manager** (preferred) / **Parameter Store** (cheaper, parameter-style):

- Store: DB passwords, API keys (LLM keys!), JWT secrets, OAuth client secrets (Q417).
- **Secrets Manager adds:** automatic **rotation** (e.g., rotate RDS passwords with Lambda), cross-account grants, versioning, audit.
- **Access pattern:** app *assumes an IAM role* (ECS task role / Lambda role) with a scoped `secretsmanager:GetSecretValue` on the exact ARN — **no env-file-with-keys in ECS** (env vars end up inspectable).
- **Inject at runtime**, not build: the image is generic; the task definition references the secret ARN → AWS injects it.
- **Local dev:** `.env` gitignored + `.env.example`; tools like `aws-vault`/`chamber` for parity.

**Interview answer:** "Secrets Manager + IAM role per service, injected at task launch, auto-rotation, no keys in images or env — and I'd never log or commit them (Q417, Q480)."

---

## Q618: How do you estimate AWS cost? How do you control it?

**Cost modeling (think "what drives spend"):**
- **LLM calls** — the real cost driver (Q445), not infrastructure.
- **Compute:** ECS/Fargate (instance-hours × price × scale) vs Lambda (invocations × duration × memory).
- **Data:** S3 storage + GET/PUT/egress costs (egress is the sneaky one — CloudFront reduces it), RDS instance hours + storage + IOPs.
- **Networking:** NAT Gateway (~per hour + per GB), data transfer between AZs.
- **Supporting:** CloudWatch, CloudTrail, secrets, ECR storage.

**Controls:**
- **Budgets + alarms** (Cost Anomaly Detection) — alert at 80% forecast.
- **Rightsizing** — is the DB over-provisioned? are workers idle at night (autoscale down)?
- **Lifecycle rules** — move old resumes/transcripts to Glacier (Q607).
- **Savings Plans / Reserved Instances** for steady-state (DB, ALB).
- **Egress optimization** — CDN for static, keep data transfer in-region.
- **Per-tenant cost tracking** — resource tags → Cost Explorer (charge per customer).

**Answer pattern:** "model the two biggest lines (LLM, then compute/data), set budget alarms, tag resources, and put lifecycle + autoscaling policies on the biggest spend."

---

## Q619: ECS vs EKS vs Lambda — how do you choose?

| | **ECS/Fargate** | **EKS (k8s)** | **Lambda** |
|---|---|---|---|
| Ops overhead | Low (managed) | High (control plane + add-ons) | None |
| Model | Long-running containers | Containers + k8s ecosystem | Event-driven functions |
| Scaling | Service autoscaling | HPA + cluster autoscaler | Inherent (per-invocation) |
| Cost | Always-on billing (Fargate fine) | Always-on workers + control plane | Pay-per-invocation (idle = free) |
| Timeouts | None | None | 15 min max |
| Best for | **API + workers (your case)** | Multi-team/multi-service orgs, complex orchestration | Notifications, webhooks, bursty short jobs |

**Your pick:** **ECS/Fargate** for FastAPI + the parse/screen **workers** (long-lived, streaming, queues); **Lambda** for notifications/webhook triggers; skip EKS until you have a real reason (many services, need k8s ecosystem). State that tradeoff explicitly — "I'd start with Fargate because it has the least ops for our shape, and would revisit EKS only if we outgrew it."

---

## Q620: How would you secure a web application on AWS end-to-end?

**Full layered answer (compose from this file):**
1. **Perimeter:** Route 53 → **CloudFront + WAF** (rate limiting, OWASP rules, geo blocks) → Shield (DDoS).
2. **Network:** VPC with public/private subnets (Q600); ALB in public, app+DB private; SGs with least privilege (Q601); NACLs for deny lists.
3. **TLS:** ACM certs at CloudFront/ALB (Q487, Q602); HSTS.
4. **Identity:** IAM roles, no keys in code (Q608); **app-level authN/authZ**: JWT + refresh rotation (Q406–411), RBAC (Q395).
5. **Data:** encryption at rest (S3 SSE-KMS, RDS KMS) + in transit (Q416); secrets in Secrets Manager (Q617); bucket security (Q611).
6. **App security:** input validation (Pydantic), parameterized SQL (Q401), prompt-injection + PII redaction for LLM (Q419), SSRF guards on URL fetches (Q418).
7. **Audit & response:** CloudTrail (Q613), CloudWatch alarms (Q612), access logs on S3/ALB, DLQ + alerting for processing failures (Q561).
8. **DR:** Multi-AZ + backups + DR plan (Q616).