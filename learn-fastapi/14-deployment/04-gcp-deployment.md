# GCP Deployment for FastAPI — Complete Guide

## Table of Contents
1. [GCP Overview for FastAPI](#overview)
2. [Cloud Run](#cloud-run)
3. [Cloud Functions](#cloud-functions)
4. [GKE — Google Kubernetes Engine](#gke)
5. [Cloud SQL](#cloud-sql)
6. [Cloud Memorystore](#cloud-memorystore)
7. [Cloud Storage](#cloud-storage)
8. [Load Balancing](#load-balancing)
9. [IAM](#iam)
10. [Best Practices](#best-practices)

---

## GCP Overview for FastAPI <a name="overview"></a>

| Service | Type | Best For |
|---------|------|----------|
| Cloud Run | Serverless Containers | Most FastAPI apps, auto-scaling to zero |
| Cloud Functions | Serverless Functions | Simple endpoints, event-driven |
| GKE | Managed Kubernetes | Complex microservices, K8s expertise |
| Compute Engine | VMs | Full control, legacy migration |

---

## Cloud Run <a name="cloud-run"></a>

Cloud Run is GCP's serverless container platform. It's the simplest way to deploy FastAPI on GCP.

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

# Cloud Run injects the PORT environment variable
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

CMD exec gunicorn app.main:app \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 2 \
    --bind 0.0.0.0:$PORT \
    --timeout 120 \
    --graceful-timeout 30 \
    --keep-alive 5
```

### Deploy to Cloud Run

```bash
# Build and deploy in one step
gcloud run deploy fastapi-app \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --min-instances 0 \
    --max-instances 10 \
    --concurrency 80 \
    --timeout 300 \
    --set-env-vars "ENVIRONMENT=production,LOG_LEVEL=INFO" \
    --set-secrets "DATABASE_URL=fastapi-database-url:latest,SECRET_KEY=fastapi-secret-key:latest"
```

### Cloud Run YAML Configuration

```yaml
# service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: fastapi-app
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/execution-gen: n2
        run.googleapis.com/cpu-throttling: "false"  # Always-on CPU
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
        - image: gcr.io/my-project/fastapi-app:latest
          ports:
            - containerPort: 8000
          resources:
            limits:
              cpu: "2"
              memory: "2Gi"
          env:
            - name: ENVIRONMENT
              value: "production"
          volumeMounts:
            - name: config
              mountPath: /app/config
              readOnly: true
          startupProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 0
            periodSeconds: 3
            failureThreshold: 30
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            periodSeconds: 10
      volumes:
        - name: config
          configMap:
            name: fastapi-config
```

```bash
# Apply YAML configuration
gcloud run services replace service.yaml --region us-central1

# View service details
gcloud run services describe fastapi-app --region us-central1

# Update environment variables
gcloud run services update fastapi-app \
    --region us-central1 \
    --update-env-vars "LOG_LEVEL=DEBUG"

# Update secrets
gcloud run services update fastapi-app \
    --region us-central1 \
    --update-secrets "DB_PASSWORD=db-password:latest"

# Set IAM policy (restrict access)
gcloud run services add-iam-policy-binding fastapi-app \
    --region us-central1 \
    --member="user:dev@example.com" \
    --role="roles/run.invoker"
```

### Cloud Run Pricing

```
First 180,000 vCPU-seconds/month: FREE
After that: $0.00002400/vCPU-second

First 360,000 GiB-seconds/month: FREE
After that: $0.00000250/GiB-second

Example: 1 instance, 1 vCPU, 512Mi, always running:
- vCPU: 2,592,000 seconds → 2,412,000 billable → $57.89
- Memory: 1,296,000 GiB-seconds → 936,000 billable → $2.34
- Total: ~$60/month
- With min-instances=0 and sporadic traffic: much less
```

---

## Cloud Functions <a name="cloud-functions"></a>

For simple FastAPI-compatible endpoints using Cloud Functions (2nd gen).

```python
# main.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Cloud Functions!"}

# For Cloud Functions (2nd gen), use functions-framework
from functions_framework import http

@http
def fastapi_app(request):
    """Cloud Functions entry point."""
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
    return handler(request.environ, lambda status, headers: None)
```

```bash
# Deploy Cloud Function
gcloud functions deploy fastapi-app \
    --gen2 \
    --runtime python312 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point fastapi_app \
    --memory 512MB \
    --timeout 60s \
    --min-instances 0 \
    --max-instances 10 \
    --region us-central1
```

---

## GKE — Google Kubernetes Engine <a name="gke"></a>

```bash
# Create GKE cluster
gcloud container clusters create fastapi-cluster \
    --zone us-central1-a \
    --num-nodes 3 \
    --machine-type e2-standard-2 \
    --enable-autoscaling \
    --min-nodes 1 \
    --max-nodes 10 \
    --enable-autorepair \
    --enable-autoupgrade \
    --release-channel regular \
    --enable-network-policy \
    --workload-pool=my-project.svc.id.goog

# Get credentials
gcloud container clusters get-credentials fastapi-cluster \
    --zone us-central1-a
```

### GKE Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      serviceAccountName: fastapi-sa
      containers:
        - name: fastapi
          image: gcr.io/my-project/fastapi-app:latest
          ports:
            - containerPort: 8000
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: fastapi-secrets
                  key: database-url
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
          startupProbe:
            httpGet:
              path: /health/live
              port: 8000
            failureThreshold: 30
            periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: ClusterIP
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

### GKE Ingress with GCE Load Balancer

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-ingress
  annotations:
    kubernetes.io/ingress.class: gce
    kubernetes.io/ingress.global-static-ip-name: fastapi-ip
    networking.gke.io/managed-certificates: fastapi-cert
spec:
  rules:
    - host: api.myapp.com
      http:
        paths:
          - path: /*
            pathType: ImplementationSpecific
            backend:
              service:
                name: fastapi-service
                port:
                  number: 80
```

---

## Cloud SQL <a name="cloud-sql"></a>

```bash
# Create Cloud SQL instance
gcloud sql instances create fastapi-db \
    --database-version=POSTGRES_16 \
    --tier=db-custom-2-4096 \
    --region=us-central1 \
    --storage-size=20GB \
    --storage-auto-increase \
    --backup-start-time=03:00 \
    --enable-point-in-time-recovery \
    --require-ssl \
    --no-assign-ip

# Set root password
gcloud sql users set-password postgres \
    --instance=fastapi-db \
    --password=<password>

# Create database
gcloud sql databases create myapp --instance=fastapi-db
```

### Cloud SQL Auth Proxy

```bash
# Download Cloud SQL Auth Proxy
curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.11.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

# Start proxy (connects to Cloud SQL without public IP)
./cloud-sql-proxy \
    my-project:us-central1:fastapi-db \
    --port 5432
```

```yaml
# GKE sidecar deployment with Cloud SQL
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  template:
    spec:
      serviceAccountName: fastapi-sa
      containers:
        # Cloud SQL Auth Proxy sidecar
        - name: cloud-sql-proxy
          image: gcr.io/cloud-sql-connectors/cloud-sql-proxy:2.11.0
          args:
            - "--port=5432"
            - "my-project:us-central1:fastapi-db"
          securityContext:
            runAsNonRoot: true
          resources:
            limits:
              cpu: "0.5"
              memory: "256Mi"

        # FastAPI application
        - name: fastapi
          image: gcr.io/my-project/fastapi-app:latest
          env:
            - name: DATABASE_URL
              value: "postgresql+asyncpg://postgres:password@localhost:5432/myapp"
```

### Cloud SQL Connection in FastAPI

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine

# When using Cloud SQL Auth Proxy
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/myapp"
)

# When using Cloud SQL Connector (Python library)
from google.cloud.sql.connector import Connector

connector = Connector()

def getconn():
    return connector.connect(
        "my-project:us-central1:fastapi-db",
        "asyncpg",
        user="postgres",
        password="password",
        db="myapp",
    )

engine = create_async_engine(
    "postgresql+asyncpg://",
    async_creator=getconn,
)
```

---

## Cloud Memorystore <a name="cloud-memorystore"></a>

```bash
# Create Redis instance
gcloud redis instances create fastapi-redis \
    --size=1 \
    --region=us-central1 \
    --zone=us-central1-a \
    --tier=standard \
    --redis-version=redis_7_0 \
    --redis-config maxmemory-policy=allkeys-lru \
    --network=default \
    --connect-mode=private-ip
```

```python
# Connect to Memorystore Redis
import redis.asyncio as redis
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "10.0.0.3")  # Private IP
REDIS_PORT = 6379

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=5,
)
```

---

## Cloud Storage <a name="cloud-storage"></a>

```bash
# Create bucket
gsutil mb -l us-central1 gs://fastapi-static-assets/

# Make publicly readable (for static assets)
gsutil iam ch allUsers:objectViewer gs://fastapi-static-assets/

# Upload files
gsutil -m cp -r ./static/* gs://fastapi-static-assets/
gsutil setmeta -h "Cache-Control:public, max-age=31536000" \
    gs://fastapi-static-assets/**
```

### Cloud Storage in FastAPI

```python
from google.cloud import storage
import os

storage_client = storage.Client()

async def upload_to_gcs(bucket_name: str, source_file, destination_blob: str):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_file(source_file)
    blob.cache_control = "public, max-age=31536000"
    blob.patch()
    return f"https://storage.googleapis.com/{bucket_name}/{destination_blob}"

async def download_from_gcs(bucket_name: str, source_blob: str):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob)
    return blob.download_as_bytes()
```

---

## Load Balancing <a name="load-balancing"></a>

### Cloud Run with Load Balancer

```bash
# Map custom domain to Cloud Run
gcloud run domain-mappings create \
    --service fastapi-app \
    --domain api.myapp.com \
    --region us-central1

# Or use Serverless NEG with external ALB
gcloud compute network-endpoint-groups create fastapi-neg \
    --region=us-central1 \
    --network-endpoint-type=serverless \
    --cloud-run-service=fastapi-app

gcloud compute backend-services create fastapi-backend \
    --global \
    --protocol=HTTPS

gcloud compute backend-services add-backend fastapi-backend \
    --global \
    --network-endpoint-group=fastapi-neg \
    --network-endpoint-group-region=us-central1

gcloud compute url-maps create fastapi-lb \
    --default-service=fastapi-backend

gcloud compute target-http-proxies create fastapi-proxy \
    --url-map=fastapi-lb

gcloud compute forwarding-rules create fastapi-forwarding-rule \
    --global \
    --target-http-proxy=fastapi-proxy \
    --ports=80
```

---

## IAM <a name="iam"></a>

### Service Accounts

```bash
# Create service account for FastAPI
gcloud iam service-accounts create fastapi-app \
    --display-name="FastAPI Application"

# Grant roles
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:fastapi-app@my-project.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:fastapi-app@my-project.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:fastapi-app@my-project.iam.gserviceaccount.com" \
    --role="roles/storage.objectAdmin"

# Attach to Cloud Run service
gcloud run services update fastapi-app \
    --service-account=fastapi-app@my-project.iam.gserviceaccount.com \
    --region us-central1
```

### IAM for GKE

```bash
# Create GKE service account
gcloud iam service-accounts create gke-fastapi-sa \
    --display-name="GKE FastAPI SA"

# Grant roles for Cloud SQL, Secret Manager, etc.
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:gke-fastapi-sa@my-project.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

# Use Workload Identity
gcloud iam service-accounts add-iam-policy-binding gke-fastapi-sa@my-project.iam.gserviceaccount.com \
    --role=roles/iam.workloadIdentityUser \
    --member="serviceAccount:my-project.svc.id.goog[default/fastapi-sa]"

# Annotate K8s service account
kubectl annotate serviceaccount fastapi-sa \
    iam.gke.io/gcp-service-account=gke-fastapi-sa@my-project.iam.gserviceaccount.com
```

---

## Best Practices <a name="best-practices"></a>

1. **Use Cloud Run** for most FastAPI workloads — zero infrastructure management
2. **Set min-instances=0** for dev/staging — scale to zero when idle
3. **Use Cloud SQL Auth Proxy** — no public IP needed for database
4. **Enable Workload Identity** — secure IAM for GKE pods
5. **Use Secret Manager** — never store secrets in containers or config
6. **Enable Cloud SQL backups** — automated daily + point-in-time recovery
7. **Use Cloud CDN** — cache static content at edge locations
8. **Set up Cloud Monitoring** — dashboards and alerting for all services
9. **Use VPC Service Controls** — perimeter security for sensitive workloads
10. **Enable Audit Logging** — track all admin and data access
11. **Use Artifact Registry** — private container images with vulnerability scanning
12. **Set up Cloud Armor** — DDoS protection and WAF for external services
13. **Use Cloud Build** — CI/CD pipelines integrated with GCP
14. **Tag resources** — cost management and access control
15. **Enable Budget Alerts** — get notified before overspending
