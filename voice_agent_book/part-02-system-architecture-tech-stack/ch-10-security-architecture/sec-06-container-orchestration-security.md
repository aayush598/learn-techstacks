# Section 06: Container & Orchestration Security

## Container Security

Containers are built with **minimal base images**, scanned for vulnerabilities with **Trivy**, and run with **read-only root filesystems** and **non-root users**. Runtime security is monitored by **Falco** for anomalous behavior.

```
┌─────────────────────────────────────────────────────────────────────┐
│               CONTAINER SECURITY LIFECYCLE                         │
│                                                                     │
│  Build Time                                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  1. Minimal base image (distroless/node:20-debian12)        │   │
│  │  2. Multi-stage build (builder → runtime)                   │   │
│  │  3. No shell, no package manager, no dev tools              │   │
│  │  4. Trivy scan (fail on CRITICAL or HIGH)                  │   │
│  │  5. Image signing (cosign)                                  │   │
│  │  6. Multi-architecture (amd64 + arm64)                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  Deploy Time                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  1. Image signature verification via admission webhook      │   │
│  │  2. Pod security policies enforced                          │   │
│  │  3. Network policies applied                                │   │
│  │  4. Resource limits set (CPU/memory)                        │   │
│  │  5. Secrets injected via External Secrets Operator          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  Runtime                                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  1. Read-only root filesystem                              │   │
│  │  2. Non-root user (UID 1001)                                │   │
│  │  3. Falco agent monitors syscalls                          │   │
│  │  4. Seccomp profile (default-deny with allowlist)          │   │
│  │  5. AppArmor profile for additional confinement            │   │
│  │  6. Liveness/Readiness probes for health                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Dockerfile (Secure)

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY pnpm-lock.yaml package.json ./
RUN pnpm install --frozen-lockfile
COPY . .
RUN pnpm build

# Stage 2: Production
FROM gcr.io/distroless/nodejs20-debian12
USER 1001:1001
WORKDIR /app
COPY --from=builder --chown=1001:1001 /app/.next ./.next
COPY --from=builder --chown=1001:1001 /app/public ./public
COPY --from=builder --chown=1001:1001 /app/node_modules ./node_modules
COPY --from=builder --chown=1001:1001 /app/package.json ./

# Security: read-only filesystem enforced at runtime
# Security: no shell, no package manager
# Security: non-root user

EXPOSE 3000
CMD ["node", "server.js"]
```

## Trivy Scanning (CI)

```yaml
# CI step for container scanning
- name: Scan container image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
    format: sarif
    output: trivy-results.sarif
    severity: CRITICAL,HIGH
    exit-code: 1
    ignore-unfixed: true
    vuln-type: os,library
    scanners: vuln,secret
```

## Pod Security Standards

```yaml
# Pod Security Admission (PSA) — enforce restricted profile
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: v1.29
---
# Per-pod security context
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1001
    runAsGroup: 1001
    fsGroup: 1001
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: call-service
      securityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop: ['ALL']
        readOnlyRootFilesystem: true
        privileged: false
```

## Falco Runtime Security

```yaml
# Falco rules for anomalous behavior detection
# falco_rules.yaml
- rule: Unexpected outbound connection
  desc: Detect unexpected network connections from services
  condition: >
    evt.type=connect and
    proc.name!="kube-proxy" and
    not (fd.sip in (trusted_backends))
  output: >
    Unexpected outbound connection (service=%container.name,
    proc=%proc.name, connection=%fd.name)
  priority: WARNING
  tags: [network, container]

- rule: Shell spawned in container
  desc: Detect shell execution in containers (should not have shell)
  condition: >
    spawned_process and
    proc.name in (shell_binaries) and
    container.id != host
  output: >
    Shell spawned in container (user=%user.name,
    container=%container.name, proc=%proc.name)
  priority: CRITICAL
  tags: [shell, container]

- rule: Read sensitive file
  desc: Detect access to sensitive files (should be read-only)
  condition: >
    open_read and
    fd.name startswith /etc/shadow or
    fd.name startswith /var/run/secrets
  output: >
    Sensitive file read (file=%fd.name, container=%container.name)
  priority: WARNING
  tags: [filesystem, container]
```

## Image Signing

```bash
# Sign images with cosign (keyless via OIDC)
cosign sign \
  --oidc-issuer https://token.actions.githubusercontent.com \
  --oidc-client-id sigstore \
  ghcr.io/voiceagent/call-service:$IMAGE_TAG

# Verify before deployment
cosign verify \
  --oidc-issuer https://token.actions.githubusercontent.com \
  ghcr.io/voiceagent/call-service:$IMAGE_TAG
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Base image | Distroless (Google) | Minimal attack surface, no shell, no package manager |
| Image scanning | Trivy | Comprehensive, fast, CI-native |
| Runtime security | Falco | Syscall-level monitoring, CNCF graduated |
| Pod security | Restricted PSA | Kubernetes-native, admission-time enforcement |
| Image signing | Cosign (keyless) | No key management, OIDC-based identity |

## Integration Points

- **Ch 10 (Network Security)** — Network policies complement container security
- **Ch 10 (Secrets Management)** — Secrets injected at runtime, not in images
- **Ch 10 (Supply Chain)** — Image signing is part of supply chain security
- **Ch 08 (DevOps)** — CI pipeline enforces scanning and signing

## Production Considerations

- **Base Image Updates**: Automated weekly rebuilds with security patches; Trivy scan on every build
- **Falco Alerts**: Critical alerts → PagerDuty; warnings → Slack security channel
- **Pod Security Audit**: Monthly review of security context configurations
- **Container Escape**: Falco detects container escape attempts; automated pod termination + IP blocking
- **Vulnerability Management**: SLA: CRITICAL → 4 hours, HIGH → 24 hours, MEDIUM → 7 days
