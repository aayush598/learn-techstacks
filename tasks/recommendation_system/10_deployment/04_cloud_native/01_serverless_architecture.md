# Serverless Architecture for Recommendations

## Overview

Serverless computing offers a compelling model for recommendation systems by eliminating infrastructure management overhead and providing automatic scaling. However, serverless is not universally optimal — it introduces trade-offs in latency, cold starts, execution duration, and cost at scale. This document examines when and how to use serverless technologies effectively for recommendation workloads.

## Serverless Computing Models

### Function-as-a-Service (FaaS)

**AWS Lambda**

- Maximum execution duration: 15 minutes (configurable from 1 second).
- Memory allocation: 128 MB to 10,240 MB (CPU scales proportionally).
- Cold start latency: 100ms-2s depending on runtime, package size, and VPC configuration.
- Concurrency: 1,000 default account limit (adjustable via AWS support).
- Ephemeral storage: 512 MB to 10,240 MB `/tmp` space.

**Cloudflare Workers**

- Execution time limit: 30 seconds (CPU time), 30 seconds (wall clock for free plan).
- Memory: 128 MB per isolate.
- Cold start: Sub-millisecond due to V8 isolate architecture.
- Global distribution: Automatically deployed to 300+ edge locations.
- Ideal for lightweight recommendation scoring at the edge.

### Container-based Serverless

**AWS Fargate**

- Run containers without managing EC2 instances.
- Support for long-running processes (hours, not minutes).
- Memory: Up to 120 GB per task.
- vCPU: Up to 16 vCPUs per task.
- Persistent storage via EFS mount.
- Better suited for model inference workloads requiring consistent latency.

**Google Cloud Run**

- Container-based serverless with automatic scaling to zero.
- Concurrency: Up to 1,000 requests per instance.
- Request timeout: Up to 60 minutes.
- GPU support available for ML inference workloads.
- Always-on instances available to eliminate cold starts.

### Workflow Orchestration

**AWS Step Functions**

- Orchestrate multi-step ML pipelines as state machines.
- Support for parallel execution, error handling, and human approval steps.
- Standard workflows: up to 25,000 events, 1-year duration.
- Express workflows: up to 100,000 events/second, 5-minute duration.
- Integration with Lambda, Step Functions, SQS, DynamoDB, and 200+ AWS services.

**Apache Airflow (Managed)**

- Amazon Managed Workflows for Apache Airflow (MWAA) for complex ML pipelines.
- DAG-based workflow definition with Python.
- Better suited for complex, long-running ML pipelines than Step Functions.
- Built-in retry logic, dependency management, and monitoring.

## Recommendation API Patterns with Serverless

### Pattern 1: API Gateway + Lambda

**Architecture**

- API Gateway handles HTTP routing, authentication, rate limiting, and request/response transformation.
- Lambda functions implement the recommendation logic.
- DynamoDB or ElastiCache for user/item data and precomputed recommendations.
- SQS for asynchronous notification processing.

**Request Flow**

1. Client sends recommendation request to API Gateway.
2. API Gateway authenticates the request (Cognito, API keys, or custom authorizer).
3. API Gateway invokes the Lambda function with the request payload.
4. Lambda retrieves user features from DynamoDB/DAX cache.
5. Lambda retrieves candidate items from ElastiCache or precomputed recommendations.
6. Lambda scores and ranks candidates using the model.
7. Lambda returns the ranked list to API Gateway.
8. API Gateway returns the response to the client.

**Optimization Strategies**

- Use Lambda provisioned concurrency to eliminate cold starts for critical paths.
- Keep Lambda deployment packages under 50 MB (unzipped) for faster cold starts.
- Use Lambda SnapStart for Java-based inference functions.
- Implement connection reuse for database connections across invocations.
- Use DynamoDB DAX for microsecond-latency caching.

### Pattern 2: Edge Computing with Cloudflare Workers

**Architecture**

- Deploy lightweight recommendation models (tree-based, linear) as WebAssembly modules at the edge.
- Use Cloudflare KV or Workers KV for feature storage at the edge.
- Use Cloudflare Durable Objects for user session state.
- Leverage Cloudflare R2 for model artifact storage.

**Use Cases**

- Simple content-based recommendations with precomputed scores.
- A/B test variant assignment at the edge.
- Personalized content ordering based on user segments.
- Real-time feature computation for lightweight models.

**Limitations**

- Cannot run GPU-accelerated models at the edge.
- Limited to 128 MB memory per request.
- Cannot maintain persistent connections to backend services.
- Cold starts are fast but CPU time is limited (10-50ms on free plan).

### Pattern 3: Step Functions for ML Pipelines

**Pipeline Stages**

1. **Data Validation**: Lambda validates input data schema and quality.
2. **Feature Computation**: Lambda or ECS Fargate task computes features.
3. **Model Inference**: ECS Fargate task runs the model inference.
4. **Post-processing**: Lambda applies business rules (diversity, freshness, filters).
5. **Result Storage**: Lambda stores results in DynamoDB or S3.
6. **Notification**: Lambda sends results via SNS or WebSocket.

**Error Handling**

- Implement Catch states for each stage with specific error handlers.
- Use Retry states with exponential backoff for transient failures.
- Implement dead-letter queues for failed pipeline executions.
- Add human approval states for high-risk decisions (model promotion).

## Kinesis for Event Processing

### Real-time Event Streaming

- Use Kinesis Data Streams for high-throughput event ingestion (user interactions, impressions).
- Partition events by user ID for ordered processing per user.
- Use Kinesis Data Firehose for near-real-time delivery to S3/OpenSearch.
- Implement Kinesis Analytics for real-time aggregate computation.

### Stream Processing with Lambda

- Configure Lambda event source mapping with Kinesis as the trigger.
- Set batch size to balance throughput and processing latency (100-1000 records).
- Use parallelization factor to scale processing within a shard.
- Implement tumbling windows for time-based aggregation (hourly CTR computation).
- Handle shard splitting/merging gracefully with checkpoint management.

### Event-Driven Architecture Patterns

| Event Type | Source | Consumer | Action |
|------------|--------|----------|--------|
| Page View | Web App | Kinesis → Lambda | Update user session |
| Add to Cart | Web App | Kinesis → Lambda | Update user preferences |
| Purchase | Payment Service | SQS → Lambda | Update purchase history |
| Search | Web App | Kinesis → Lambda | Update search preferences |
| Model Trained | Training Pipeline | SNS → Lambda | Update serving endpoints |

## Fargate for Container Workloads

### When to Choose Fargate Over Lambda

- **Duration**: Workloads running longer than 15 minutes (model training, batch inference).
- **Memory**: Workloads requiring more than 10 GB of memory.
- **State**: Workloads requiring persistent connections or shared state.
- **Binary Size**: Containers with large Docker images (>500 MB).
- **GPU**: ML inference workloads requiring GPU acceleration.

### Fargate Recommendation Serving

- Deploy model inference containers as ECS Fargate services.
- Use Application Load Balancer for traffic distribution across tasks.
- Configure Service Auto Scaling based on CPU/memory utilization.
- Use EFS for shared model artifact storage across tasks.
- Implement health checks for container readiness.

### Batch Processing with Fargate

- Use ECS RunTask for batch recommendation generation.
- Schedule batch jobs with EventBridge (CloudWatch Events) for periodic execution.
- Process items in parallel with configurable concurrency.
- Use Step Functions to orchestrate batch pipeline stages.
- Store batch results in S3 for offline serving or DynamoDB for online serving.

## Cost Optimization

### Lambda Cost Model

- Pricing: $0.20 per 1M requests + $0.0000166667 per GB-second.
- A recommendation API handling 10M requests/month with 256MB memory:
  - Request cost: 10 × $0.20 = $2.00
  - Compute cost: 10M × 100ms avg × 0.25 GB × $0.0000166667 = $41.67
  - **Total: ~$44/month**
- At 1B requests/month, Lambda becomes more expensive than container-based alternatives.

### Fargate Cost Model

- Pricing: $0.04048/vCPU/hour + $0.004445/GB/hour.
- A 2-vCPU, 4GB recommendation task running 24/7:
  - Cost: (2 × $0.04048 + 4 × $0.004445) × 730 = $70.98/month
- Compare with EC2 equivalent: m5.large on-demand ≈ $70/month.
- Fargate savings with Savings Plans: up to 50% discount.

### Cost Decision Matrix

| Monthly Requests | Avg Latency | Best Option | Estimated Cost |
|-----------------|-------------|-------------|----------------|
| <10M | <1s | Lambda | $20-50 |
| 10M-100M | <500ms | Lambda + Provisioned | $100-500 |
| 100M-1B | <200ms | Fargate or EKS | $500-2,000 |
| >1B | <100ms | EKS (dedicated) | $2,000+ |

## Cold Start Mitigation

### Understanding Cold Starts

- **Init Phase**: Downloading and unpacking the deployment package (~100ms-2s).
- **Extension Init**: Starting runtime extensions (monitoring, tracing) (~50ms-500ms).
- **Runtime Init**: Initializing the runtime and loading dependencies (~50ms-500ms).
- **Function Init**: Running your initialization code (model loading, connection setup).

### Mitigation Strategies

**Provisioned Concurrency**

- Pre-initialize a specified number of Lambda instances.
- Guarantees zero cold starts for provisioned instances.
- Cost: ~$15/month per 1GB provisioned instance.
- Configure via Terraform or AWS Console.

**SnapStart (Java/JVM)**

- Snapshot initialized JVM state for fast startup.
- Reduces cold start from seconds to ~200ms.
- Limited to Java 11+ runtimes.

**Package Optimization**

- Minimize deployment package size by removing unused dependencies.
- Use Lambda Layers for shared dependencies.
- Use compiled runtimes (Rust, Go) for fastest cold starts.
- Avoid VPC configuration unless necessary (adds 1-2s to cold starts).

**Architectural Solutions**

- Use warming pings to keep Lambda instances alive (every 5 minutes).
- Implement circuit breakers to fallback to cached recommendations during cold starts.
- Precompute recommendations for popular items to reduce real-time Lambda invocations.
- Use CloudFront or edge caching to serve cached recommendations.

## Serverless vs Containers Decision Framework

### Choose Serverless When

- Traffic is variable or unpredictable (spiky workloads).
- Development velocity is prioritized over cost at scale.
- Workloads are short-lived (<15 minutes for Lambda).
- Team lacks Kubernetes expertise.
- Quick prototyping and MVP development.
- Event-driven architectures (stream processing, async workflows).

### Choose Containers When

- Traffic is consistent and high-volume (>100M requests/month).
- Latency requirements are strict (<50ms P99).
- Workloads require GPU acceleration.
- Long-running processes (>15 minutes).
- Need for persistent connections (WebSocket, gRPC streaming).
- Complex inter-service communication patterns.
- Fine-grained control over resource allocation.

### Hybrid Approach

- Use Lambda for lightweight API routing, authentication, and post-processing.
- Use Fargate or EKS for model inference and heavy computation.
- Use Step Functions to orchestrate across Lambda and ECS.
- Use edge functions (Cloudflare Workers) for simple personalization.
- Evolve from serverless to containers as scale requirements grow.

## Operational Considerations

### Monitoring Serverless

- Use AWS X-Ray for distributed tracing across Lambda, API Gateway, and downstream services.
- Monitor Lambda metrics: invocations, duration, errors, throttles, concurrent executions.
- Set up CloudWatch Alarms for error rates exceeding 0.1%.
- Track cold start frequency and duration as key operational metrics.

### Debugging Serverless

- Use CloudWatch Logs for Lambda function logging.
- Implement structured logging (JSON) for log aggregation and analysis.
- Use Lambda Powertools for standardized logging, tracing, and metrics.
- Test locally with SAM CLI or LocalStack before deployment.

### Security Considerations

- Implement least-privilege IAM roles for each Lambda function.
- Use VPC endpoints for accessing AWS services without internet exposure.
- Enable AWS WAF on API Gateway for protection against common attacks.
- Rotate API keys and secrets regularly using Secrets Manager.
- Implement request validation at the API Gateway level.
