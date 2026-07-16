# Kubernetes for FastAPI — Complete Deployment Guide

## Table of Contents
1. [K8s Fundamentals](#fundamentals)
2. [Deployment YAML](#deployment)
3. [Service](#service)
4. [Ingress](#ingress)
5. [ConfigMap and Secret](#configmap-secret)
6. [Horizontal Pod Autoscaler](#hpa)
7. [Probes](#probes)
8. [Resource Limits](#resource-limits)
9. [Rolling Updates](#rolling-updates)
10. [Kustomize](#kustomize)
11. [Helm Chart Basics](#helm)
12. [Complete Production Manifest](#complete)
13. [Best Practices](#best-practices)

---

## K8s Fundamentals <a name="fundamentals"></a>

Kubernetes orchestrates containers across a cluster of machines. For FastAPI, K8s handles scaling, self-healing, rolling updates, and service discovery.

**Core Objects:**
- **Pod**: Smallest deployable unit; one or more containers
- **Deployment**: Manages ReplicaSets; declares desired state
- **Service**: Stable network endpoint for a set of Pods
- **Ingress**: HTTP routing rules (host/path → Service)
- **ConfigMap**: Non-sensitive configuration data
- **Secret**: Sensitive data (passwords, tokens)
- **HPA**: Auto-scales Pods based on metrics

---

## Deployment YAML <a name="deployment"></a>

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  namespace: production
  labels:
    app: fastapi-app
    version: v1.2.0
    environment: production
  annotations:
    deployment.kubernetes.io/revision: "3"
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1            # One extra pod during update
      maxUnavailable: 0      # Never reduce below desired count
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
        version: v1.2.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      # Security context at pod level
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000

      # Service account
      serviceAccountName: fastapi-sa

      # Termination grace period
      terminationGracePeriodSeconds: 60

      # Anti-affinity: spread pods across nodes
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values:
                        - fastapi-app
                topologyKey: kubernetes.io/hostname

      # Init containers (run before main container)
      initContainers:
        - name: wait-for-db
          image: busybox:1.36
          command: ['sh', '-c', 'until nc -z postgres-service 5432; do echo waiting for db; sleep 2; done']

      containers:
        - name: fastapi
          image: registry.example.com/fastapi-app:v1.2.0
          imagePullPolicy: Always

          ports:
            - name: http
              containerPort: 8000
              protocol: TCP

          # Environment from ConfigMap and Secret
          envFrom:
            - configMapRef:
                name: fastapi-config
            - secretRef:
                name: fastapi-secrets

          # Additional env vars
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace

          # Resource limits
          resources:
            requests:
              cpu: "250m"       # 0.25 CPU cores
              memory: "256Mi"
            limits:
              cpu: "1000m"      # 1 CPU core
              memory: "512Mi"

          # Liveness probe: is the container alive?
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 15
            timeoutSeconds: 5
            failureThreshold: 3
            successThreshold: 1

          # Readiness probe: is the container ready for traffic?
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
            successThreshold: 1

          # Startup probe: has the container finished starting?
          startupProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
            failureThreshold: 30   # 30 * 5s = 150s max startup time

          # Volume mounts
          volumeMounts:
            - name: tmp-dir
              mountPath: /app/tmp
            - name: config-volume
              mountPath: /app/config
              readOnly: true

          # Lifecycle hooks
          lifecycle:
            preStop:
              exec:
                command: ["sh", "-c", "sleep 5"]

      volumes:
        - name: tmp-dir
          emptyDir:
            sizeLimit: 100Mi
        - name: config-volume
          configMap:
            name: fastapi-config-file
```

---

## Service <a name="service"></a>

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  namespace: production
  labels:
    app: fastapi-app
  annotations:
    # For cloud load balancers
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
spec:
  type: ClusterIP        # Internal only; use LoadBalancer for external
  selector:
    app: fastapi-app
  ports:
    - name: http
      port: 80            # Service port
      targetPort: 8000     # Container port
      protocol: TCP
  # Session affinity (rarely needed for stateless APIs)
  # sessionAffinity: ClientIP
```

### Service Types

| Type | Description | Use Case |
|------|-------------|----------|
| `ClusterIP` | Internal IP, accessible within cluster | Default for internal services |
| `NodePort` | Exposes on each node's IP at a static port | Development, simple access |
| `LoadBalancer` | Provisions cloud load balancer | Direct cloud exposure |
| `ExternalName` | Maps to a DNS name | External service alias |

---

## Ingress <a name="ingress"></a>

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-ingress
  namespace: production
  annotations:
    # NGINX Ingress Controller annotations
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"

    # TLS
    cert-manager.io/cluster-issuer: letsencrypt-prod

    # CORS
    nginx.ingress.kubernetes.io/enable-cors: "true"
    nginx.ingress.kubernetes.io/cors-allow-origin: "https://myapp.com"
    nginx.ingress.kubernetes.io/cors-allow-methods: "GET, POST, PUT, DELETE, OPTIONS"

    # Proxy settings
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"

spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.myapp.com
      secretName: api-tls-cert
  rules:
    - host: api.myapp.com
      http:
        paths:
          - path: /api/v1(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: fastapi-service
                port:
                  number: 80
          - path: /docs(/|$)(.*)
            pathType: ImplementationSpecific
            backend:
              service:
                name: fastapi-service
                port:
                  number: 80
```

---

## ConfigMap and Secret <a name="configmap-secret"></a>

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-config
  namespace: production
data:
  ENVIRONMENT: "production"
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  DATABASE_NAME: "myapp"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  LOG_LEVEL: "INFO"
  WORKERS: "4"
  # Config file as ConfigMap
  app.conf: |
    [server]
    host = 0.0.0.0
    port = 8000
    workers = 4
    timeout = 120
```

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: fastapi-secrets
  namespace: production
type: Opaque
# Values are base64-encoded
data:
  DATABASE_URL: cG9zdGdyZXNxbDpcL2FzeW5jcGdcL3VzZXI6cGFzc0BkYjpsc3RhN2RiOjU0MzIvbXlhcHA=
  SECRET_KEY: c3VwZXItc2VjcmV0LWtleS1pbi1wcm9kdWN0aW9u
  REDIS_PASSWORD: cmVkaXMtcGFzc3dvcmQ=
  SENTRY_DSN: aHR0cHM6Ly94eHhAaG9zdC5pby94eHg=
```

```bash
# Create secret from command line
kubectl create secret generic fastapi-secrets \
    --from-literal=DATABASE_URL='postgresql+asyncpg://user:pass@db:5432/myapp' \
    --from-literal=SECRET_KEY='my-secret-key' \
    --from-literal=REDIS_PASSWORD='redis-pass'

# Create from file
kubectl create secret generic fastapi-tls \
    --from-file=tls.crt=./certs/tls.crt \
    --from-file=tls.key=./certs/tls.key

# Create from .env file
kubectl create secret generic fastapi-secrets \
    --from-env-file=.env.production

# Encode values
echo -n 'my-secret-value' | base64

# Decode values
echo 'bXktc2VjcmV0LXZhbHVl' | base64 -d
```

---

## Horizontal Pod Autoscaler <a name="hpa"></a>

```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 2
  maxReplicas: 20
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 4
          periodSeconds: 60
        - type: Percent
          value: 100
          periodSeconds: 60
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300    # Wait 5 min before scaling down
      policies:
        - type: Pods
          value: 1
          periodSeconds: 120             # Remove 1 pod every 2 min
      selectPolicy: Min
  metrics:
    # CPU-based scaling
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70

    # Memory-based scaling
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80

    # Custom metric: requests per second
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "1000"
```

### Metric Server Setup

```bash
# Install metrics server (required for HPA)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Verify metrics
kubectl top pods -n production
kubectl top nodes

# Check HPA status
kubectl get hpa -n production
kubectl describe hpa fastapi-hpa -n production
```

---

## Probes <a name="probes"></a>

### Three Types of Probes

```yaml
containers:
  - name: fastapi
    # STARTUP PROBE: Runs first. Disables liveness/readiness until it passes.
    # Use for slow-starting apps.
    startupProbe:
      httpGet:
        path: /health/live
        port: 8000
      initialDelaySeconds: 0
      periodSeconds: 5
      failureThreshold: 30    # 30 * 5 = 150s max startup
      successThreshold: 1

    # LIVENESS PROBE: Is the container alive?
    # Failure triggers container restart.
    livenessProbe:
      httpGet:
        path: /health/live
        port: 8000
      initialDelaySeconds: 0  # Startup probe handles initial delay
      periodSeconds: 15
      timeoutSeconds: 5
      failureThreshold: 3
      successThreshold: 1

    # READINESS PROBE: Is the container ready for traffic?
    # Failure removes pod from Service endpoints.
    readinessProbe:
      httpGet:
        path: /health/ready
        port: 8000
      initialDelaySeconds: 0
      periodSeconds: 10
      timeoutSeconds: 5
      failureThreshold: 3
      successThreshold: 1
```

### Probe Behaviors

| Event | Liveness | Readiness | Startup |
|-------|----------|-----------|---------|
| Passing | No action | Pod added to Service | Liveness & Readiness enabled |
| Failing | Container restarted | Pod removed from Service | Liveness & Readiness disabled |

### TCP and Exec Probes

```yaml
# TCP probe (if app doesn't have HTTP health endpoint)
livenessProbe:
  tcpSocket:
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10

# Exec probe (run a command)
livenessProbe:
  exec:
    command:
      - python
      - -c
      - "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
  initialDelaySeconds: 10
  periodSeconds: 15
```

---

## Resource Limits <a name="resource-limits"></a>

```yaml
resources:
  requests:
    # Minimum resources guaranteed to the container
    # K8s uses this for scheduling decisions
    cpu: "250m"       # 0.25 cores (250 millicores)
    memory: "256Mi"   # 256 mebibytes

  limits:
    # Maximum resources the container can use
    # CPU can be throttled; memory OOMKills the container
    cpu: "1000m"      # 1 full core
    memory: "512Mi"   # 512 mebibytes
```

### Resource Planning

```
Rule of thumb for FastAPI:
- requests.cpu: 250m (start small)
- requests.memory: 256Mi (base Python + FastAPI)
- limits.cpu: 1000m (allow bursting)
- limits.memory: 512Mi (prevent OOM)

For CPU-intensive workloads:
- Increase CPU limits
- Consider more pods rather than bigger pods

For memory-intensive workloads (large payloads, caching):
- Increase memory limits
- Monitor for memory leaks
```

### LimitRanges and ResourceQuotas

```yaml
# LimitRange: default resource limits for pods in a namespace
apiVersion: v1
kind: LimitRange
metadata:
  name: fastapi-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "256Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      max:
        cpu: "2000m"
        memory: "1Gi"

---
# ResourceQuota: total resources for a namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: fastapi-quota
  namespace: production
spec:
  hard:
    requests.cpu: "10"
    requests.memory: "20Gi"
    limits.cpu: "20"
    limits.memory: "40Gi"
    pods: "50"
```

---

## Rolling Updates <a name="rolling-updates"></a>

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1         # Allow 1 extra pod during update
      maxUnavailable: 0   # Never reduce below desired count
```

### Rolling Update Commands

```bash
# Update image
kubectl set image deployment/fastapi-app \
    fastapi=registry.example.com/fastapi-app:v1.3.0 \
    -n production

# Watch rollout status
kubectl rollout status deployment/fastapi-app -n production

# View rollout history
kubectl rollout history deployment/fastapi-app -n production

# Rollback to previous version
kubectl rollout undo deployment/fastapi-app -n production

# Rollback to specific revision
kubectl rollout undo deployment/fastapi-app --to-revision=2 -n production

# Pause a rollout
kubectl rollout pause deployment/fastapi-app -n production

# Resume a paused rollout
kubectl rollout resume deployment/fastapi-app -n production
```

### Deployment Strategies Comparison

```
Rolling Update (default):
  - Gradually replaces old pods with new ones
  - Zero downtime
  - Both versions run simultaneously during update
  - Rollback is easy

Recreate:
  - Terminates all old pods, then creates new ones
  - Downtime during update
  - Simple, no version mixing
  - Use when two versions can't coexist

Blue-Green:
  - Deploy new version alongside old
  - Switch traffic all at once
  - Instant rollback by switching back
  - Requires double resources
  - Use Ingress or Service selector for switching
```

---

## Kustomize <a name="kustomize"></a>

Kustomize customizes YAML manifests without templating. Built into `kubectl`.

```
fastapi-app/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── development/
    │   ├── kustomization.yaml
    │   ├── configmap-patch.yaml
    │   └── deployment-patch.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   ├── configmap-patch.yaml
    │   └── hpa.yaml
    └── production/
        ├── kustomization.yaml
        ├── configmap-patch.yaml
        ├── deployment-patch.yaml
        ├── hpa.yaml
        └── ingress.yaml
```

### Base Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app: fastapi-app
  managed-by: kustomize

namespace: default
```

### Overlay Kustomization

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base
  - hpa.yaml
  - ingress.yaml

namespace: production

patches:
  - path: deployment-patch.yaml
  - path: configmap-patch.yaml

commonLabels:
  environment: production

commonAnnotations:
  owner: platform-team
```

### Deployment Patch

```yaml
# overlays/production/deployment-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: fastapi
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
```

### Kustomize Commands

```bash
# Build and view output
kubectl kustomize overlays/production/

# Apply
kubectl apply -k overlays/production/

# Build with images override
kubectl kustomize overlays/production/ \
    --load-restrictor None \
    2>/dev/null | kubectl apply -f -
```

---

## Helm Chart Basics <a name="helm"></a>

Helm is a package manager for Kubernetes. Charts are templates with values.

```
fastapi-chart/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── NOTES.txt
└── .helmignore
```

### Chart.yaml

```yaml
# Chart.yaml
apiVersion: v2
name: fastapi-app
description: A Helm chart for FastAPI application
type: application
version: 0.1.0       # Chart version
appVersion: "1.2.0"  # App version
maintainers:
  - name: Platform Team
    email: platform@example.com
```

### values.yaml

```yaml
# values.yaml
replicaCount: 2

image:
  repository: registry.example.com/fastapi-app
  pullPolicy: IfNotPresent
  tag: "1.2.0"

service:
  type: ClusterIP
  port: 80
  targetPort: 8000

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.myapp.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.myapp.com

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 20
  targetCPUUtilizationPercentage: 70

env:
  ENVIRONMENT: production
  LOG_LEVEL: INFO

secrets:
  DATABASE_URL: ""
  SECRET_KEY: ""
```

### Deployment Template

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "fastapi.fullname" . }}
  labels:
    {{- include "fastapi.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "fastapi.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "fastapi.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
          {{- if .Values.env }}
          env:
            {{- range $key, $value := .Values.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
          {{- end }}
          {{- if .Values.secrets }}
          envFrom:
            - secretRef:
                name: {{ include "fastapi.fullname" . }}-secrets
          {{- end }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
```

### Helm Commands

```bash
# Install chart
helm install fastapi-app ./fastapi-chart \
    -n production \
    -f values-prod.yaml

# Upgrade chart
helm upgrade fastapi-app ./fastapi-chart \
    -n production \
    -f values-prod.yaml

# Dry run
helm install fastapi-app ./fastapi-chart \
    --dry-run --debug

# List releases
helm list -n production

# Rollback
helm rollback fastapi-app 1 -n production

# Uninstall
helm uninstall fastapi-app -n production
```

---

## Complete Production Manifest <a name="complete"></a>

```yaml
# All-in-one production manifest
---
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    name: production
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-config
  namespace: production
data:
  ENVIRONMENT: "production"
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  DATABASE_NAME: "myapp"
  REDIS_HOST: "redis-service"
  LOG_LEVEL: "INFO"
---
apiVersion: v1
kind: Secret
metadata:
  name: fastapi-secrets
  namespace: production
type: Opaque
data:
  DATABASE_URL: <base64-encoded>
  SECRET_KEY: <base64-encoded>
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      terminationGracePeriodSeconds: 60
      containers:
        - name: fastapi
          image: registry.example.com/fastapi-app:v1.2.0
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: fastapi-config
            - secretRef:
                name: fastapi-secrets
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: 1000m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
  namespace: production
spec:
  selector:
    app: fastapi-app
  ports:
    - port: 80
      targetPort: 8000
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

---

## Best Practices <a name="best-practices"></a>

1. **Always set resource requests and limits** — prevents resource starvation and OOM kills
2. **Use namespaces** — separate environments (dev, staging, production)
3. **Implement all three probes** — startup, liveness, and readiness
4. **Use ConfigMaps and Secrets** — never hardcode config in images
5. **Enable HPA** — auto-scale based on CPU and custom metrics
6. **Set pod anti-affinity** — spread replicas across nodes
7. **Use rolling updates with maxUnavailable: 0** — zero-downtime deployments
8. **Implement PDB (Pod Disruption Budget)** — ensure availability during maintenance
9. **Use network policies** — restrict inter-pod traffic
10. **Enable RBAC** — least-privilege access for service accounts
11. **Use init containers** — for dependency checking and setup
12. **Monitor with Prometheus** — scrape `/metrics` endpoint
13. **Use linter tools** — kubeval, kube-linter, kubesec for manifest validation
14. **Keep images small** — multi-stage Docker builds, distroless base images
15. **Use GitOps** — ArgoCD or Flux for declarative, auditable deployments
