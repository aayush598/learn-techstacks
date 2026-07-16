# AWS Deployment for FastAPI — Complete Guide

## Table of Contents
1. [AWS Overview for FastAPI](#overview)
2. [ECR — Container Registry](#ecr)
3. [ECS Fargate](#ecs-fargate)
4. [Lambda with Mangum](#lambda-mangum)
5. [API Gateway](#api-gateway)
6. [ALB — Application Load Balancer](#alb)
7. [RDS — Managed Database](#rds)
8. [ElastiCache — Redis](#elasticache)
9. [S3 and CloudFront](#s3-cloudfront)
10. [IAM Roles](#iam-roles)
11. [ECS Service Discovery](#service-discovery)
12. [AWS App Runner](#app-runner)
13. [Best Practices](#best-practices)

---

## AWS Overview for FastAPI <a name="overview"></a>

AWS offers multiple deployment options for FastAPI, from serverless to container orchestration:

| Service | Type | Best For |
|---------|------|----------|
| ECS Fargate | Serverless Containers | Production workloads, auto-scaling |
| Lambda + Mangum | Serverless Functions | Sporadic traffic, APIs with cold starts |
| EKS | Managed Kubernetes | Teams already using K8s |
| App Runner | Managed Containers | Simple deployments, quick start |
| EC2 | Virtual Machines | Full control, custom networking |

---

## ECR — Container Registry <a name="ecr"></a>

```bash
# Create ECR repository
aws ecr create-repository \
    --repository-name fastapi-app \
    --image-scanning-configuration scanOnPush=true \
    --encryption-configuration encryptionType=AWS_KMS

# Get login token
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build and tag image
docker build -t fastapi-app:latest .
docker tag fastapi-app:latest \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest

# Push to ECR
docker push \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest

# Lifecycle policy to manage old images
aws ecr put-lifecycle-policy \
    --repository-name fastapi-app \
    --lifecycle-policy-text '{
        "rules": [
            {
                "rulePriority": 1,
                "description": "Keep last 10 images",
                "selection": {
                    "tagStatus": "any",
                    "countType": "imageCountMoreThan",
                    "countNumber": 10
                },
                "action": {"type": "expire"}
            }
        ]
    }'
```

---

## ECS Fargate <a name="ecs-fargate"></a>

Fargate runs containers without managing servers. You define CPU/memory, and AWS handles the infrastructure.

### Task Definition

```json
{
    "family": "fastapi-app",
    "networkMode": "awsvpc",
    "requiresCompatibilities": ["FARGATE"],
    "cpu": "512",
    "memory": "1024",
    "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
    "taskRoleArn": "arn:aws:iam::123456789012:role/ecsTaskRole",
    "containerDefinitions": [
        {
            "name": "fastapi",
            "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest",
            "portMappings": [
                {
                    "containerPort": 8000,
                    "protocol": "tcp"
                }
            ],
            "environment": [
                {"name": "ENVIRONMENT", "value": "production"},
                {"name": "LOG_LEVEL", "value": "INFO"}
            ],
            "secrets": [
                {
                    "name": "DATABASE_URL",
                    "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:fastapi/database-url"
                },
                {
                    "name": "SECRET_KEY",
                    "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789012:secret:fastapi/secret-key"
                }
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/fastapi-app",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs",
                    "awslogs-create-group": "true"
                }
            },
            "healthCheck": {
                "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
                "interval": 30,
                "timeout": 10,
                "retries": 3,
                "startPeriod": 60
            },
            "essential": true
        }
    ]
}
```

### ECS Service

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name fastapi-cluster

# Create CloudWatch log group
aws logs create-log-group --log-group-name /ecs/fastapi-app --region us-east-1

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create ECS service
aws ecs create-service \
    --cluster fastapi-cluster \
    --service-name fastapi-service \
    --task-definition fastapi-app:1 \
    --desired-count 3 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={
        subnets=[subnet-xxx,subnet-yyy],
        securityGroups=[sg-xxx],
        assignPublicIp=DISABLED
    }" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=fastapi,containerPort=8000" \
    --health-check-grace-period-seconds 60 \
    --deployment-configuration "maximumPercent=200,minimumHealthyPercent=100"
```

### Fargate Pricing

```
Fargate charges per vCPU-hour and GB-hour:
- vCPU: $0.04048/hour (us-east-1)
- Memory: $0.004445/GB/hour

Example: 3 tasks × 0.5 vCPU × 1GB = ~$0.022/hour = ~$16/month
+ ALB: ~$16/month + LCU charges
+ RDS: ~$15-50/month (db.t3.micro)
```

---

## Lambda with Mangum <a name="lambda-mangum"></a>

Mangum is an adapter that runs ASGI applications (like FastAPI) on AWS Lambda.

### Setup

```bash
pip install mangum
```

```python
# app/main.py
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from Lambda!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Mangum handler — entry point for Lambda
handler = Mangum(app, lifespan="off")
```

### Lambda Deployment Package

```bash
# Using Lambda Container Image (recommended)
# Dockerfile for Lambda
FROM public.ecr.aws/lambda/python:3.12

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ${LAMBDA_TASK_ROOT}/app/

CMD ["app.main.handler"]
```

```bash
# Build and push Lambda container
docker build -t fastapi-lambda -f Dockerfile.lambda .
docker tag fastapi-lambda:latest \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-lambda:latest
docker push \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-lambda:latest

# Create Lambda function
aws lambda create-function \
    --function-name fastapi-app \
    --package-type Image \
    --code "ImageUri=123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-lambda:latest" \
    --role arn:aws:iam::123456789012:role/lambda-execution-role \
    --timeout 30 \
    --memory-size 512 \
    --architectures arm64
```

### Lambda + API Gateway Integration

```python
# app/main.py with API Gateway events
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

handler = Mangum(app, lifespan="off")
```

### Lambda Cold Start Optimization

```
Cold starts in Lambda can be 1-5 seconds for Python.
Optimization strategies:

1. Use ARM64 (Graviton2) — 20% cheaper, faster
2. Minimize package size — remove unused dependencies
3. Use Lambda Provisioned Concurrency — keep warm
4. Use Lambda SnapStart — snapshot initialized state
5. Keep global initialization outside handler
6. Use connection pooling that survives warm invocations
```

---

## API Gateway <a name="api-gateway"></a>

```bash
# Create REST API
aws apigateway create-rest-api \
    --name fastapi-gateway \
    --description "API Gateway for FastAPI"

# Create resource
aws apigateway create-resource \
    --rest-api-id <api-id> \
    --parent-id <root-id> \
    --path-part "{proxy+}"

# Create ANY method (catches all)
aws apigateway put-method \
    --rest-api-id <api-id> \
    --resource-id <resource-id> \
    --http-method ANY \
    --authorization-type NONE

# Integration with Lambda
aws apigateway put-integration \
    --rest-api-id <api-id> \
    --resource-id <resource-id> \
    --http-method ANY \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/<lambda-arn>/invocations"

# Deploy API
aws apigateway create-deployment \
    --rest-api-id <api-id> \
    --stage-name prod
```

### API Gateway with VPC Link (to ECS)

```bash
# Create VPC Link for private integration
aws apigateway create-vpc-link \
    --name fastapi-vpc-link \
    --target-arns <nlb-arn>

# Integration with NLB (for ECS Fargate)
aws apigateway put-integration \
    --rest-api-id <api-id> \
    --resource-id <resource-id> \
    --http-method ANY \
    --type HTTP_PROXY \
    --integration-http-method ANY \
    --uri "http://<nlb-dns>:80/{proxy}" \
    --connection-type VPC_LINK \
    --connection-id <vpc-link-id>
```

---

## ALB — Application Load Balancer <a name="alb"></a>

```bash
# Create ALB
aws elbv2 create-load-balancer \
    --name fastapi-alb \
    --subnets subnet-xxx subnet-yyy \
    --security-groups sg-xxx \
    --scheme internet-facing \
    --type application

# Create target group
aws elbv2 create-target-group \
    --name fastapi-targets \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-xxx \
    --target-type ip \
    --health-check-path /health \
    --health-check-interval-seconds 30 \
    --health-check-timeout-seconds 10 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3

# Create listener with SSL
aws elbv2 create-listener \
    --load-balancer-arn <alb-arn> \
    --protocol HTTPS \
    --port 443 \
    --certificates CertificateArn=<acm-cert-arn> \
    --default-actions Type=forward,TargetGroupArn=<tg-arn>

# HTTP to HTTPS redirect
aws elbv2 create-listener \
    --load-balancer-arn <alb-arn> \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=redirect,RedirectConfig="{Protocol=HTTPS,Port=443,StatusCode=HTTP_301}"
```

### ALB Path-Based Routing

```bash
# Route /api/* to FastAPI, /static/* to S3
aws elbv2 create-rule \
    --listener-arn <https-listener-arn> \
    --priority 1 \
    --conditions Field=path-pattern,Values='/api/*' \
    --actions Type=forward,TargetGroupArn=<fastapi-tg-arn>

aws elbv2 create-rule \
    --listener-arn <https-listener-arn> \
    --priority 2 \
    --conditions Field=path-pattern,Values='/static/*' \
    --actions Type=forward,TargetGroupArn=<s3-tg-arn>
```

---

## RDS — Managed Database <a name="rds"></a>

```bash
# Create DB subnet group
aws rds create-db-subnet-group \
    --db-subnet-group-name fastapi-db-subnet \
    --db-subnet-group-description "Subnets for FastAPI RDS" \
    --subnet-ids subnet-xxx subnet-yyy

# Create RDS instance (PostgreSQL)
aws rds create-db-instance \
    --db-instance-identifier fastapi-db \
    --db-instance-class db.t3.medium \
    --engine postgres \
    --engine-version 16.3 \
    --master-username dbadmin \
    --master-user-password <password> \
    --allocated-storage 20 \
    --max-allocated-storage 100 \
    --storage-type gp3 \
    --storage-encrypted \
    --vpc-security-group-ids sg-xxx \
    --db-subnet-group-name fastapi-db-subnet \
    --backup-retention-period 7 \
    --multi-az \
    --enable-performance-insights \
    --monitoring-interval 60 \
    --deletion-protection \
    --no-publicly-accessible
```

### RDS Connection from ECS

```python
# In your FastAPI app
import os
from sqlalchemy.ext.asyncio import create_async_engine

# Use RDS proxy for connection pooling in serverless
DATABASE_URL = os.environ["DATABASE_URL"]
# postgresql+asyncpg://user:pass@rds-proxy endpoint:5432/myapp

engine = create_async_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
```

---

## ElastiCache — Redis <a name="elasticache"></a>

```bash
# Create ElastiCache subnet group
aws elasticache create-cache-subnet-group \
    --cache-subnet-group-name fastapi-cache-subnet \
    --cache-subnet-group-description "Subnets for FastAPI ElastiCache" \
    --subnet-ids subnet-xxx subnet-yyy

# Create Redis cluster
aws elasticache create-cache-cluster \
    --cache-cluster-id fastapi-redis \
    --engine redis \
    --engine-version 7.0 \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1 \
    --vpc-security-group-ids sg-xxx \
    --cache-subnet-group-name fastapi-cache-subnet \
    --at-rest-encryption-enabled \
    --transit-encryption-enabled
```

```python
# Redis connection from FastAPI
import redis.asyncio as redis

redis_client = redis.from_url(
    os.environ["REDIS_URL"],  # redis://xxx.cache.amazonaws.com:6379
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
)
```

---

## S3 and CloudFront <a name="s3-cloudfront"></a>

### S3 for Static Assets

```bash
# Create S3 bucket
aws s3 mb s3://fastapi-static-assets --region us-east-1

# Enable static website hosting
aws s3 website s3://fastapi-static-assets \
    --index-document index.html \
    --error-document error.html

# Upload static files
aws s3 sync ./static/ s3://fastapi-static-assets/ \
    --cache-control "max-age=31536000"

# Upload with content type
aws s3 cp ./static/app.js s3://fastapi-static-assets/app.js \
    --content-type "application/javascript" \
    --cache-control "max-age=31536000"
```

### CloudFront CDN

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
    --distribution-config '{
        "Origins": {
            "Items": [{
                "DomainName": "fastapi-static-assets.s3.amazonaws.com",
                "Id": "S3-static",
                "S3OriginConfig": {
                    "OriginAccessIdentity": ""
                }
            }],
            "Quantity": 1
        },
        "DefaultCacheBehavior": {
            "TargetOriginId": "S3-static",
            "ViewerProtocolPolicy": "redirect-to-https",
            "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
            "Compress": true
        },
        "Enabled": true,
        "Aliases": {
            "Items": ["static.myapp.com"],
            "Quantity": 1
        },
        "ViewerCertificate": {
            "ACMCertificateArn": "<acm-cert-arn>",
            "SSLSupportMethod": "sni-only",
            "MinimumProtocolVersion": "TLSv1.2_2021"
        }
    }'
```

### FastAPI S3 Uploads

```python
import boto3
from fastapi import UploadFile

s3_client = boto3.client("s3")

async def upload_file(file: UploadFile, bucket: str, key: str):
    s3_client.upload_fileobj(
        file.file,
        bucket,
        key,
        ExtraArgs={
            "ContentType": file.content_type,
            "ServerSideEncryption": "aws:kms",
        }
    )
    return f"https://{bucket}.s3.amazonaws.com/{key}"
```

---

## IAM Roles <a name="iam-roles"></a>

### ECS Task Execution Role

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}
```

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "*"
        }
    ]
}
```

### ECS Task Role (for the application)

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::fastapi-static-assets",
                "arn:aws:s3:::fastapi-static-assets/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": "arn:aws:secretsmanager:us-east-1:123456789012:secret:fastapi/*"
        }
    ]
}
```

---

## ECS Service Discovery <a name="service-discovery"></a>

```bash
# Create private namespace
aws servicediscovery create-private-dns-namespace \
    --name internal.local \
    --vpc vpc-xxx

# Register service
aws servicediscovery create-service \
    --name fastapi-app \
    --namespace-id <namespace-id>

# In ECS service, enable service discovery
aws ecs update-service \
    --cluster fastapi-cluster \
    --service fastapi-service \
    --service-registries "registryArn=arn:aws:servicediscovery:..."
```

```python
# Connect to other services via service discovery
# Service URL: fastapi-app.internal.local
DATABASE_URL = "postgresql+asyncpg://user:pass@postgres-service.internal.local:5432/myapp"
```

---

## AWS App Runner <a name="app-runner"></a>

App Runner is the simplest way to deploy containers on AWS — no cluster, no task definitions.

```bash
# Create App Runner service from ECR
aws apprunner create-service \
    --service-name fastapi-app \
    --source-configuration '{
        "ImageRepository": {
            "ImageIdentifier": "123456789012.dkr.ecr.us-east-1.amazonaws.com/fastapi-app:latest",
            "ImageConfiguration": {
                "Port": "8000"
            },
            "ImageRepositoryType": "ECR"
        },
        "AutoDeploymentsEnabled": true
    }' \
    --instance-configuration '{
        "Cpu": "1 vCPU",
        "Memory": "2 GB"
    }' \
    --health-check-configuration '{
        "Protocol": "HTTP",
        "Path": "/health",
        "Interval": 30,
        "Timeout": 10
    }'
```

### App Runner Pricing

```
- vCPU: $0.064/hour
- Memory: $0.007/GB/hour
- Example: 1 vCPU + 2GB = ~$0.078/hour = ~$56/month
- Includes: auto-scaling, HTTPS, custom domains, deployments
```

---

## Best Practices <a name="best-practices"></a>

1. **Use Fargate** for most FastAPI workloads — no EC2 management
2. **Store secrets in Secrets Manager** — never in environment variables directly
3. **Use RDS Proxy** — connection pooling for Lambda and Fargate
4. **Enable CloudWatch Container Insights** — monitor ECS performance
5. **Use ALB** — health checks, SSL termination, path-based routing
6. **Multi-AZ for RDS** — high availability with automated failover
7. **Enable deletion protection** — prevent accidental RDS deletion
8. **Use VPC endpoints** — avoid NAT Gateway charges for AWS services
9. **Set up AWS X-Ray** — distributed tracing across services
10. **Use ECR image scanning** — catch vulnerabilities before deployment
11. **Configure auto-scaling** — target tracking on CPU/memory
12. **Use CloudFront** — CDN for static assets, reduced ALB traffic
13. **Enable GuardDuty** — threat detection for your AWS account
14. **Use AWS Config** — compliance monitoring for infrastructure
15. **Tag everything** — cost allocation and resource management
