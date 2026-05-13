# AWS Interview Questions and Answers

## Q1: What is AWS?
**A:** AWS (Amazon Web Services) is a comprehensive cloud computing platform offered by Amazon. It provides over 200 fully featured services from data centers globally, including compute, storage, databases, networking, machine learning, and security services. AWS follows a pay-as-you-go pricing model and is the market leader in cloud computing.

## Q2: What are the main categories of AWS services?
**A:** The main categories include Compute (EC2, Lambda, ECS), Storage (S3, EBS, EFS), Database (RDS, DynamoDB, Aurora), Networking (VPC, CloudFront, Route 53), Security (IAM, KMS, Shield), Analytics (EMR, Redshift, Athena), Machine Learning (SageMaker, Rekognition), and Application Integration (SQS, SNS, Step Functions).

## Q3: What is Amazon EC2?
**A:** Amazon Elastic Compute Cloud (EC2) is a web service that provides resizable compute capacity in the cloud. It allows users to launch virtual servers called instances, choose from various instance types optimized for different workloads, and pay only for what they use. EC2 provides complete control over the operating system and software stack.

## Q4: Explain the different EC2 instance purchasing options.
**A:** On-Demand (pay by the hour/second with no long-term commitment), Reserved Instances (1-3 year commitment with significant discount), Spot Instances (up to 90% discount but can be terminated at any time), Dedicated Hosts (physical server dedicated to you), and Savings Plans (flexible pricing model across compute services).

## Q5: What is Amazon S3 and what are its storage classes?
**A:** Amazon Simple Storage Service (S3) is an object storage service offering industry-leading scalability, durability (99.9999999999%), and security. Storage classes include S3 Standard (frequent access), S3 Intelligent-Tiering (auto cost optimization), S3 Standard-IA (infrequent access), S3 One Zone-IA, S3 Glacier (archival), S3 Glacier Deep Archive (lowest cost archival), and S3 Outposts.

## Q6: What is the difference between scalability and elasticity in AWS?
**A:** Scalability is the ability of a system to handle increased load by adding resources (vertical scaling) or adding more instances (horizontal scaling). Elasticity is the ability to automatically scale resources up or down based on demand. AWS Auto Scaling provides elasticity, while services like EC2 and RDS offer scalability.

## Q7: What is Amazon VPC?
**A:** Amazon Virtual Private Cloud (VPC) lets you provision a logically isolated section of the AWS cloud where you can launch AWS resources in a virtual network that you define. You have complete control over IP addressing, subnets, route tables, network gateways, and security settings.

## Q8: Explain the difference between a public subnet and a private subnet.
**A:** A public subnet has a route to an Internet Gateway (IGW), allowing instances to receive inbound traffic from the internet. A private subnet does not have a direct route to an IGW; instances in private subnets can access the internet through a NAT Gateway/Instance but cannot be directly accessed from the internet.

## Q9: What is an Internet Gateway and a NAT Gateway?
**A:** An Internet Gateway (IGW) is a horizontally scaled, redundant VPC component that allows communication between your VPC and the internet. A NAT Gateway enables instances in a private subnet to connect to the internet or other AWS services but prevents the internet from initiating connections with those instances.

## Q10: What is AWS IAM?
**A:** AWS Identity and Access Management (IAM) is a web service that helps you securely control access to AWS resources. It enables you to create and manage users, groups, roles, and policies to grant or deny permissions to AWS resources. IAM follows the principle of least privilege.

## Q11: What is an IAM role and how is it different from an IAM user?
**A:** An IAM user is a permanent identity with long-term credentials associated with a specific person or application. An IAM role is a temporary identity that can be assumed by trusted entities (users, applications, or AWS services) to obtain temporary security credentials. Roles do not have permanent credentials and are ideal for cross-account access and EC2 instance permissions.

## Q12: What is the difference between a security group and a NACL?
**A:** Security Groups act as a virtual firewall at the instance level (stateful), support allow rules only, and evaluate all rules before deciding. Network ACLs (NACLs) act at the subnet level (stateless), support both allow and deny rules, and evaluate rules in order (lowest number first).

## Q13: What is Amazon RDS and what database engines does it support?
**A:** Amazon Relational Database Service (RDS) is a managed service that makes it easy to set up, operate, and scale relational databases. It supports Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle, and SQL Server. RDS automates backups, patching, replication, and failover.

## Q14: What is Amazon DynamoDB?
**A:** Amazon DynamoDB is a fully managed NoSQL key-value and document database that delivers single-digit millisecond performance at any scale. It supports both document and key-value store models, offers built-in security, backup/restore, in-memory caching (DAX), and global tables for multi-region deployments.

## Q15: Explain the difference between DynamoDB RCU and WCU.
**A:** Read Capacity Units (RCU) measure throughput for reads: 1 RCU = 1 strongly consistent read per second for items up to 4KB, or 2 eventually consistent reads. Write Capacity Units (WCU) measure throughput for writes: 1 WCU = 1 write per second for items up to 1KB. These can be provisioned or use on-demand capacity mode.

## Q16: What is Amazon Aurora?
**A:** Amazon Aurora is a MySQL and PostgreSQL-compatible relational database built for the cloud, combining the speed and reliability of high-end commercial databases with the simplicity and cost-effectiveness of open-source databases. It provides 5x better performance than MySQL and 3x better than PostgreSQL with auto-scaling storage up to 128TB.

## Q17: What is AWS Lambda?
**A:** AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources. You can use Lambda to execute code for virtually any application or backend service with zero administration. Lambda supports multiple programming languages and charges only for compute time used.

## Q18: What are the limitations of AWS Lambda?
**A:** Key limitations include: maximum execution timeout of 15 minutes, maximum memory of 10,240 MB, maximum deployment package size of 50 MB (zipped) or 250 MB (unzipped), maximum concurrent executions (soft limit of 1,000), and temporary storage of 512 MB to 10,240 MB in /tmp directory.

## Q19: What is Amazon API Gateway?
**A:** Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. It handles API version management, traffic management, authorization, throttling, monitoring, and supports RESTful and WebSocket APIs.

## Q20: Explain the difference between REST API and HTTP API in API Gateway.
**A:** REST APIs offer more features including API keys, usage plans, request validation, and WAF integration, but have higher latency and cost. HTTP APIs are simpler, cheaper, and faster with lower latency, supporting OIDC/OAuth2 authentication and CORS but lacking some advanced features like usage plans and API keys.

## Q21: What is Amazon CloudFront?
**A:** Amazon CloudFront is a fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs to customers globally with low latency and high transfer speeds. It integrates with AWS Shield, Lambda@Edge, and provides DDoS protection.

## Q22: What is Amazon Route 53?
**A:** Amazon Route 53 is a scalable and highly available Domain Name System (DNS) web service. It connects user requests to AWS resources (EC2, ELB, S3, CloudFront) and also monitors the health of resources. Route 53 supports routing policies like Simple, Weighted, Latency-based, Failover, Geolocation, Geoproximity, and Multi-value.

## Q23: What is an Elastic Load Balancer (ELB) and what types exist?
**A:** ELB automatically distributes incoming traffic across multiple targets. Three types: Application Load Balancer (ALB) for HTTP/HTTPS traffic at Layer 7, Network Load Balancer (NLB) for TCP/UDP traffic at Layer 4 with ultra-low latency, and Gateway Load Balancer (GWLB) for third-party virtual appliances.

## Q24: What is the difference between horizontal and vertical scaling?
**A:** Horizontal scaling (scale out/in) adds or removes instances to handle load changes, providing better fault tolerance and elasticity. Vertical scaling (scale up/down) increases or decreases the capacity of a single instance (e.g., upgrading from t2.micro to t2.large) and has an upper limit.

## Q25: What is AWS Auto Scaling?
**A:** AWS Auto Scaling monitors applications and automatically adjusts capacity to maintain steady, predictable performance at the lowest possible cost. It works with EC2, DynamoDB, Aurora, ECS, and Spot Fleet. Scaling policies include target tracking, step scaling, and simple scaling.

## Q26: What is the difference between a Launch Template and a Launch Configuration?
**A:** Launch Templates are the newer, recommended approach offering versioning, support for multiple instance types, T2/T3 unlimited credits, and placement group configuration. Launch Configurations are older, do not support versioning, and are being deprecated.

## Q27: What is Amazon EBS and what volume types are available?
**A:** Amazon Elastic Block Store provides persistent block storage volumes for EC2 instances. Volume types: gp2/gp3 (general purpose SSD), io1/io2 (provisioned IOPS SSD for high-performance), st1 (throughput optimized HDD for big data), sc1 (cold HDD for infrequent access).

## Q28: What is the difference between EBS and instance store?
**A:** EBS provides persistent, durable block storage that can be detached and reattached to instances, with data surviving instance termination. Instance store provides temporary, ephemeral storage physically attached to the host, offering higher IOPS but data is lost on instance stop/termination.

## Q29: What is Amazon EFS?
**A:** Amazon Elastic File System is a scalable, fully managed elastic NFS file system for use with AWS Cloud services and on-premises resources. It grows and shrinks automatically as files are added/removed, supports NFSv4 protocol, and offers Standard and Infrequent Access storage classes.

## Q30: What is AWS CloudFormation?
**A:** AWS CloudFormation is an infrastructure-as-code (IaC) service that allows you to model and provision AWS resources using template files (JSON or YAML). It automates resource creation in the correct order with dependencies, supports change sets for previewing changes, and handles stack updates and deletions.

## Q31: What is the difference between CloudFormation and Terraform?
**A:** CloudFormation is AWS-native with deep AWS service integration, drift detection, and stack sets for multi-account deployment, but is AWS-only. Terraform is multi-cloud (AWS, Azure, GCP), uses HCL language, has a larger community, and better state management but requires separate state file management.

## Q32: What is AWS Elastic Beanstalk?
**A:** AWS Elastic Beanstalk is a Platform-as-a-Service (PaaS) that automates the deployment and scaling of web applications. You upload your code and Elastic Beanstalk handles capacity provisioning, load balancing, auto-scaling, and health monitoring while giving you full control over the underlying resources.

## Q33: What is Amazon SQS?
**A:** Amazon Simple Queue Service (SQS) is a fully managed message queuing service for decoupling application components. It supports two queue types: Standard (high throughput, at-least-once delivery, best-effort ordering) and FIFO (first-in-first-out, exactly-once processing, limited to 300 TPS).

## Q34: What is Amazon SNS?
**A:** Amazon Simple Notification Service (SNS) is a fully managed pub/sub messaging service for sending notifications to subscribers via multiple protocols (email, SMS, HTTP/HTTPS, Lambda, SQS, etc.). It supports message filtering, fan-out patterns, and FIFO topics.

## Q35: What is the difference between SQS and SNS?
**A:** SQS is a message queue where messages are pulled by consumers (polling model), and messages remain in the queue until deleted. SNS is a pub/sub system where messages are pushed to subscribers (push model), and messages are not persisted if subscribers are unavailable.

## Q36: What is Amazon Kinesis?
**A:** Amazon Kinesis is a platform for streaming data on AWS, making it easy to collect, process, and analyze real-time streaming data. Services include Kinesis Data Streams (real-time data ingestion), Kinesis Data Firehose (loading streaming data into data stores), Kinesis Data Analytics (real-time analytics with SQL/ML), and Kinesis Video Streams.

## Q37: What is the difference between Kinesis Data Streams and Kinesis Data Firehose?
**A:** Kinesis Data Streams is a real-time streaming service where consumers pull data, data is stored for up to 365 days, and you manage shard scaling. Kinesis Data Firehose automatically loads streaming data into destinations (S3, Redshift, Elasticsearch, Splunk) with near-real-time delivery and no persistent storage.

## Q38: What is Amazon ElastiCache?
**A:** Amazon ElastiCache is a managed in-memory caching service supporting Redis and Memcached. It improves application performance by retrieving information from fast, managed, in-memory caches instead of slower disk-based databases. Use cases include session management, database query caching, and real-time analytics.

## Q39: What is Amazon Redshift?
**A:** Amazon Redshift is a fast, fully managed, petabyte-scale cloud data warehouse. It uses columnar storage, massively parallel processing (MPP), and automatic compression. Redshift Spectrum allows querying data directly in S3, and Redshift RA3 nodes separate compute and storage.

## Q40: What is Amazon Athena?
**A:** Amazon Athena is a serverless, interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. It uses Presto under the hood, charges only for queries executed, and can query structured, semi-structured, and unstructured data in formats like CSV, JSON, Parquet, and ORC.

## Q41: What is AWS Glue?
**A:** AWS Glue is a fully managed extract, transform, and load (ETL) service that makes it easy to prepare and load data for analytics. It provides a data catalog, automatic schema discovery (crawlers), and a serverless Spark-based ETL engine. Glue Jobs can transform data between S3, Redshift, RDS, and other sources.

## Q42: What is Amazon EMR?
**A:** Amazon EMR (Elastic MapReduce) is a managed big data platform that simplifies running distributed processing frameworks like Apache Hadoop, Spark, HBase, Presto, and Flink on AWS. It can process petabytes of data across hundreds of EC2 instances and integrates with S3, DynamoDB, and other AWS services.

## Q43: What is AWS Data Pipeline?
**A:** AWS Data Pipeline is a web service that helps you reliably process and move data between different AWS compute and storage services, as well as on-premises data sources, at specified intervals. It handles task dependencies, retries, failure notifications, and scheduling.

## Q44: What is Amazon CloudWatch?
**A:** Amazon CloudWatch is a monitoring and observability service for AWS resources and applications. It collects metrics, logs, and events, sets alarms, and provides dashboards. CloudWatch Logs centralizes log management, CloudWatch Events (now EventBridge) provides event-driven automation, and Container Insights monitors containers.

## Q45: What is AWS CloudTrail?
**A:** AWS CloudTrail is a service that enables governance, compliance, operational auditing, and risk auditing of your AWS account. It logs every API call made in your account, including the identity, time, source IP, and request/response details. CloudTrail logs can be stored in S3 for long-term retention.

## Q46: What is the difference between CloudWatch and CloudTrail?
**A:** CloudWatch monitors performance and operational health (metrics, logs, alarms) while CloudTrail audits API activity and provides an audit trail of who did what, when, and from where. CloudWatch answers "what is happening now?" while CloudTrail answers "who did what?"

## Q47: What is AWS Config?
**A:** AWS Config is a service that assesses, audits, and evaluates the configurations of your AWS resources. It continuously monitors and records resource configuration changes, evaluates configurations against desired policies (AWS Config Rules), and provides compliance reports and notifications.

## Q48: What is AWS Key Management Service (KMS)?
**A:** AWS KMS is a managed service that makes it easy to create and control cryptographic keys used for data encryption. It integrates with most AWS services for encryption at rest, supports automatic key rotation, and uses Hardware Security Modules (HSMs) to protect keys. KMS is FIPS 140-2 compliant.

## Q49: What is the difference between KMS, CloudHSM, and Secrets Manager?
**A:** KMS is a managed key store for encryption keys with automatic key rotation and AWS service integration. CloudHSM provides dedicated hardware security modules for FIPS 140-2 Level 3 compliance and full control over cryptographic operations. Secrets Manager manages secrets (database credentials, API keys) with automatic rotation.

## Q50: What is AWS WAF?
**A:** AWS Web Application Firewall (WAF) is a web application firewall that helps protect web applications from common web exploits that could affect application availability, compromise security, or consume excessive resources. It monitors HTTP/HTTPS requests and allows blocking, allowing, or counting based on customizable rules.

## Q51: What is AWS Shield?
**A:** AWS Shield is a managed DDoS protection service. Shield Standard is automatically included at no cost and protects against common DDoS attacks. Shield Advanced provides enhanced protection, cost protection against scaling charges, 24/7 access to the DDoS Response Team (DRT), and detailed attack diagnostics.

## Q52: What is Amazon GuardDuty?
**A:** Amazon GuardDuty is a managed threat detection service that continuously monitors for malicious activity and unauthorized behavior across AWS accounts, workloads, and data stores. It uses machine learning, anomaly detection, and threat intelligence feeds to identify threats.

## Q53: What is AWS Organizations?
**A:** AWS Organizations helps you centrally govern your environment as you grow and scale your AWS resources. It enables you to create accounts, apply service control policies (SCPs), consolidate billing, and automate account creation. SCPs can restrict what services and actions accounts can use.

## Q54: Explain the Shared Responsibility Model.
**A:** AWS is responsible for security OF the cloud (hardware, software, networking, and facilities). Customers are responsible for security IN the cloud (data, encryption, OS patches, network configuration, IAM, and application code). The division varies by service (e.g., Lambda shifts more responsibility to AWS than EC2).

## Q55: What is a Service Control Policy (SCP)?
**A:** SCPs are policy-based controls available through AWS Organizations that specify the maximum permissions for member accounts. SCPs do not grant permissions but set boundaries. They can be used to restrict access to specific services, regions, or actions across all member accounts.

## Q56: What is the Well-Architected Framework?
**A:** The AWS Well-Architected Framework provides best practices for designing and operating reliable, secure, efficient, cost-effective, and sustainable systems in the cloud. It consists of six pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability.

## Q57: Explain each pillar of the Well-Architected Framework.
**A:** 1) Operational Excellence: run and monitor systems to deliver business value. 2) Security: protect data, systems, and assets. 3) Reliability: recover from failures, scale, and meet demand. 4) Performance Efficiency: use computing resources efficiently. 5) Cost Optimization: avoid unnecessary costs. 6) Sustainability: minimize environmental impact.

## Q58: What is the AWS Pricing Model?
**A:** AWS follows a pay-as-you-go model with three fundamental cost drivers: compute (charged per hour/second), storage (charged per GB), and data transfer (outbound data transfer charged, inbound is typically free). Pricing varies by service, region, and purchasing option (On-Demand, Reserved, Spot).

## Q59: What is Total Cost of Ownership (TCO) in AWS?
**A:** TCO is a financial estimate used to compare the cost of running infrastructure on-premises versus on AWS. It includes hardware, software, maintenance, power, cooling, labor, and facility costs. AWS provides a TCO calculator to compare on-premises costs with AWS costs.

## Q60: What is AWS Budgets and Cost Explorer?
**A:** AWS Budgets allows you to set custom budgets to track your cost and usage, and receive alerts when thresholds are exceeded. AWS Cost Explorer is a visualization tool that helps you understand and analyze your AWS costs and usage over time with filtering, grouping, and forecasting capabilities.

## Q61: What is Amazon Route 53 routing policy - Weighted?
**A:** Weighted routing lets you assign weights to multiple resources (e.g., 80% to one server, 20% to another) to control traffic distribution. Useful for A/B testing, canary deployments, or gradually migrating traffic between environments.

## Q62: What is Amazon Route 53 routing policy - Latency-based?
**A:** Latency-based routing directs traffic to the AWS region that provides the lowest latency for the end user. AWS Route 53 measures latency between users and regions, and routes to the region with the best performance. Useful for global applications with users worldwide.

## Q63: What is Amazon Route 53 routing policy - Failover?
**A:** Failover routing directs traffic to a primary resource, and if the primary is unhealthy (as determined by health checks), automatically routes traffic to a secondary (backup) resource. This enables active-passive disaster recovery configurations.

## Q64: What is Amazon Route 53 routing policy - Geolocation?
**A:** Geolocation routing directs traffic based on the geographic location of the user (country, continent, or U.S. state). Useful for localizing content, restricting content based on location, or complying with data sovereignty regulations.

## Q65: What is AWS Direct Connect?
**A:** AWS Direct Connect is a cloud service that makes it easy to establish a dedicated network connection from your on-premises data center to AWS. This private connection reduces network costs, increases bandwidth throughput, and provides a more consistent network experience than internet-based connections.

## Q66: What is a VPN Connection in AWS?
**A:** AWS Site-to-Site VPN creates secure connections between your on-premises network and your Amazon VPC over the internet using IPsec tunnels. It provides encrypted communication and can be used as a backup to AWS Direct Connect or as the primary connection.

## Q67: What is Amazon ECS?
**A:** Amazon Elastic Container Service (ECS) is a fully managed container orchestration service that supports Docker containers. It integrates with AWS services, supports both Fargate (serverless) and EC2 launch types, and provides service discovery, load balancing, and auto-scaling.

## Q68: What is Amazon EKS?
**A:** Amazon Elastic Kubernetes Service (EKS) is a managed Kubernetes service that makes it easy to run Kubernetes on AWS without needing to install, operate, and maintain your own Kubernetes control plane. EKS is certified Kubernetes conformant and supports both EC2 and Fargate.

## Q69: What is the difference between ECS and EKS?
**A:** ECS is AWS's native container orchestration with simpler setup, tighter AWS integration, and lower operational overhead. EKS runs standard Kubernetes, offering portability across clouds and on-premises, a larger ecosystem/tools, and is preferred if you need Kubernetes-native features.

## Q70: What is Amazon ECR?
**A:** Amazon Elastic Container Registry (ECR) is a fully managed Docker container registry that stores, manages, and deploys container images. It integrates with ECS and EKS, supports image scanning for vulnerabilities, and uses IAM for access control.

## Q71: What is AWS Fargate?
**A:** AWS Fargate is a serverless compute engine for containers that works with both ECS and EKS. It eliminates the need to manage underlying EC2 instances - you just define your container, assign CPU/memory, and Fargate runs it. You pay only for the resources your containers use.

## Q72: What is the difference between EC2 and Lambda?
**A:** EC2 provides virtual servers with complete control over the OS and environment, supports any workload, and runs continuously. Lambda is serverless, runs only in response to events, has execution limits (15 min timeout, memory limits), and you only pay for execution time.

## Q73: What is Amazon S3 Transfer Acceleration?
**A:** S3 Transfer Acceleration uses AWS CloudFront's globally distributed edge locations to accelerate uploads to S3. Data travels from the user to an edge location, then over the AWS optimized network to the S3 bucket. It is useful for uploading large files from geographically distant locations.

## Q74: What is S3 presigned URL?
**A:** A presigned URL is a URL that grants temporary permissions to access an S3 object. It is generated by an IAM user with access to the object and includes a signature that expires after a specified time. Presigned URLs are commonly used for secure file uploads/downloads without exposing AWS credentials.

## Q75: What is S3 Versioning?
**A:** S3 Versioning is a feature that preserves, retrieves, and restores every version of every object stored in a bucket. When enabled, overwriting an object creates a new version instead of replacing it. It protects against accidental deletion and enables easy rollback to previous versions.

## Q76: What is S3 Cross-Region Replication (CRR)?
**A:** CRR automatically replicates objects from a source S3 bucket in one region to a destination bucket in a different region. It is used for compliance, disaster recovery, reduced latency for geographically distributed users, and data sovereignty requirements.

## Q77: What is S3 Lifecycle Policy?
**A:** An S3 Lifecycle Policy is a set of rules that automate the transition of objects between storage classes or the expiration/deletion of objects. Common patterns: move objects to Standard-IA after 30 days, Glacier after 90 days, and delete after 365 days.

## Q78: What is Amazon S3 Object Lock?
**A:** S3 Object Lock prevents objects from being deleted or overwritten for a fixed time or indefinitely. It supports two retention modes: Governance (special permissions can override) and Compliance (no one can override). It also supports Legal Hold. Useful for regulatory compliance and WORM storage.

## Q79: What is Amazon Macie?
**A:** Amazon Macie is a fully managed data security and data privacy service that uses machine learning and pattern matching to discover, classify, and protect sensitive data stored in S3. It automatically detects personally identifiable information (PII), financial data, and intellectual property.

## Q80: What is AWS Certificate Manager (ACM)?
**A:** AWS Certificate Manager is a service that lets you provision, manage, and deploy public and private SSL/TLS certificates for use with AWS services (ELB, CloudFront, API Gateway). ACM handles certificate renewals automatically and supports custom CAs.

## Q81: What is the difference between a public and private hosted zone in Route 53?
**A:** A public hosted zone manages DNS records for a public domain (accessible from the internet). A private hosted zone manages DNS records for a domain within one or more VPCs (not accessible from the internet). Private hosted zones are used for internal service discovery.

## Q82: What is AWS Step Functions?
**A:** AWS Step Functions is a serverless orchestration service that lets you coordinate multiple AWS services into flexible, visual workflows. It supports sequential, parallel, branching, and error-handling logic. Standard workflows have a 1-year execution limit; Express workflows run up to 5 minutes.

## Q83: What is the difference between Standard and Express Workflows in Step Functions?
**A:** Standard Workflows have a 1-year execution limit, cost per state transition, exactly-once execution, and are suitable for long-running, auditable processes. Express Workflows have a 5-minute limit, cost per execution, at-least-once execution, and are suitable for high-volume, short-duration event processing.

## Q84: What is Amazon EventBridge?
**A:** Amazon EventBridge is a serverless event bus that connects applications using events. It replaces CloudWatch Events with enhanced capabilities including schema registry, schema discovery, and support for third-party SaaS event sources (Zendesk, Shopify, PagerDuty, etc.).

## Q85: What is AWS AppSync?
**A:** AWS AppSync is a fully managed GraphQL service that provides real-time data synchronization and offline programming features. It enables applications to access, manipulate, and combine data from one or more data sources (DynamoDB, Lambda, RDS, HTTP APIs) using GraphQL.

## Q86: What is AWS SAM (Serverless Application Model)?
**A:** AWS SAM is an open-source framework for building serverless applications. It extends CloudFormation with simplified syntax for defining serverless resources (Lambda, API Gateway, DynamoDB) and provides a local testing environment (sam local invoke/start-api).

## Q87: What is the AWS CDK?
**A:** The AWS Cloud Development Kit (CDK) is an open-source software development framework that lets you define cloud infrastructure using familiar programming languages (TypeScript, Python, Java, C#, Go). It generates CloudFormation templates and provides high-level constructs for common patterns.

## Q88: What is Amazon Cognito?
**A:** Amazon Cognito provides identity, authentication, and authorization for web and mobile applications. Cognito User Pools manages user sign-up/sign-in. Cognito Identity Pools grants temporary AWS credentials to authenticated/unauthorized users. It supports social identity providers, SAML, and OIDC.

## Q89: What is the difference between Cognito User Pools and Identity Pools?
**A:** User Pools is a fully managed user directory for authentication (sign-up, sign-in, password recovery). Identity Pools provides temporary AWS credentials to access AWS services. They are often used together: User Pools authenticates users, and Identity Pools grants AWS access to authenticated users.

## Q90: What is AWS Systems Manager?
**A:** AWS Systems Manager is a unified interface for operational management of AWS resources. It provides capabilities including Parameter Store (secure hierarchical parameter storage), Patch Manager (automated OS patching), Run Command (remote command execution), and Session Manager (secure shell access without SSH).

## Q91: What is AWS Systems Manager Parameter Store?
**A:** Parameter Store provides secure, hierarchical storage for configuration data and secrets (database strings, passwords, license codes). It supports plaintext and encrypted parameters (using KMS), versioning, and tiered pricing (Standard and Advanced). It is often used as a lightweight alternative to Secrets Manager.

## Q92: What is AWS Lake Formation?
**A:** AWS Lake Formation is a service that makes it easy to set up a secure data lake in days. It collects and catalogs data from databases and object storage, moves data to S3, cleans and classifies data using machine learning, and provides fine-grained access control to the data lake.

## Q93: What is Amazon QuickSight?
**A:** Amazon QuickSight is a fast, cloud-powered business analytics service that makes it easy to build visualizations, perform ad-hoc analysis, and get business insights from your data. It supports SPICE (in-memory calculation engine) for fast performance and integrates with numerous data sources.

## Q94: What is the difference between a public and private subnet in terms of routing?
**A:** A public subnet has a route table entry pointing 0.0.0.0/0 to an Internet Gateway, making instances reachable from the internet (if they have public IPs). A private subnet routes 0.0.0.0/0 to a NAT Gateway/Instance or has no internet route, making instances unreachable from the internet.

## Q95: What is a Bastion Host (Jump Box)?
**A:** A Bastion Host is a special-purpose EC2 instance in a public subnet that serves as a secure gateway for accessing instances in private subnets. Users SSH/RDP to the Bastion Host first, then connect to private instances. It is a single entry point that can be heavily secured and monitored.

## Q96: What is VPC Peering?
**A:** VPC Peering is a networking connection between two VPCs that enables routing traffic between them using private IPv4/IPv6 addresses. Peered VPCs can be in the same or different accounts/regions. Transitive peering is not supported (VPC A cannot reach VPC C through VPC B).

## Q97: What is AWS Transit Gateway?
**A:** AWS Transit Gateway is a network transit hub that connects VPCs, VPN connections, and Direct Connect in a hub-and-spoke model. It simplifies network architecture by replacing complex VPC peering mesh networks with a single gateway, and supports transitive routing across all attachments.

## Q98: What is Amazon MQ?
**A:** Amazon MQ is a managed message broker service for Apache ActiveMQ and RabbitMQ. It is suitable for migrating on-premises applications that use standard messaging protocols (AMQP, MQTT, STOMP, OpenWire) and need compatibility with existing message brokers.

## Q99: What is AWS Global Accelerator?
**A:** AWS Global Accelerator improves global application availability and performance by directing traffic over the AWS global network to the optimal endpoint based on health, geography, and routing policies. It provides static IP addresses and integration with CloudFront, ALB, NLB, and EC2.

## Q100: Explain how you would design a highly available and fault-tolerant architecture on AWS.
**A:** A well-architected HA/FT design includes: 1) Multi-AZ deployment for all critical resources (EC2 Auto Scaling across AZs, RDS Multi-AZ). 2) ELB for traffic distribution and health checks. 3) Route 53 with health checks and failover routing for DNS. 4) S3 for durable object storage with Cross-Region Replication. 5) RDS Multi-AZ or Aurora Global Database for database HA. 6) Auto Scaling for compute elasticity. 7) CloudFront for CDN and DDoS protection. 8) Backup and disaster recovery strategy (pilot light, warm standby, or multi-region active-active). 9) CloudWatch for monitoring and automated remediation. 10) Infrastructure as Code (CloudFormation/CDK) for reproducible deployments.
