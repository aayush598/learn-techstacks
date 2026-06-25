# AWS & Cloud - 200+ Interview Q&A

### Q1: AWS services you've used? (from your resume - ECS)
**Answer:** AWS ECS for container orchestration, ECR for Docker image registry. You deployed FastAPI microservices on ECS with containerized Docker images.

### Q2: What is AWS ECS?
**Answer:** Elastic Container Service. Run Docker containers at scale. Launch types: Fargate (serverless, no EC2 management) or EC2 (more control). Task definitions define containers. Services maintain desired count.

### Q3: VPC basics?
**Answer:** Virtual Private Cloud. Subnets (public/private), Route Tables, Internet Gateway, NAT Gateway, Security Groups (instance firewall), NACLs (subnet firewall). Good practice: private subnets for databases, public for load balancers.

### Q4: S3 basics?
**Answer:** Object storage. Buckets (global name). Objects (key, value, version ID, metadata). 99.999999999% durability. Use cases: static assets, backups, data lake. Storage classes: Standard, IA, Glacier, Deep Archive.

### Q5: Cloud deployment: Vercel vs AWS?
**Answer:** Vercel: simpler, optimized for Next.js/frontend, automatic preview deploys, global CDN. AWS: more control, more services, can be complex. Your projects use Vercel (SaaS Video Editor) for frontend, AWS (ECS) for backend microservices.

### Q6: Auto Scaling groups?
**Answer:** Automatically adjust EC2 instance count based on metrics (CPU, memory, custom). Min/Desired/Max capacity. Launch template. Health checks. Cooldown periods. Integration with Load Balancer.

### Q7: CloudFront (CDN) basics?
**Answer:** Content Delivery Network. Edge locations cache content. Origin: S3/ALB/HTTP server. Benefits: low latency, DDoS protection, SSL termination. Behaviors route by path pattern.

### Q8: RDS vs DynamoDB?
**Answer:** RDS: relational (PostgreSQL, MySQL), ACID, complex queries. DynamoDB: NoSQL, key-value/document, single-digit ms at any scale, auto-scaling. Choose RDS for complex relationships, DynamoDB for high-scale simple access patterns.

### Q9: IAM basics?
**Answer:** Identity and Access Management. Users (people), Groups (collection), Roles (for services), Policies (JSON permissions). Least privilege principle. ARN identifies resources. Trust policies for cross-account access.

### Q10: CI/CD on AWS?
**Answer:** CodeCommit (Git), CodeBuild (build/test), CodeDeploy (deploy to EC2/ECS/Lambda), CodePipeline (orchestrate entire pipeline). CloudFormation/CDK for infrastructure as code. Your experience uses GitHub Actions instead.
