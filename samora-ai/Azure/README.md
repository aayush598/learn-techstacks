# Azure Interview Questions and Answers

## Q1: What is Microsoft Azure?
**A:** Microsoft Azure is a comprehensive cloud computing platform and service offered by Microsoft that provides a wide range of cloud services including computing, analytics, storage, and networking. Users can select and configure these services to meet their specific needs, deploying applications through a global network of Microsoft-managed data centers.

## Q2: What are the main categories of Azure services?
**A:** Azure services are organized into categories: Compute (VMs, App Service, Azure Functions), Storage (Blob, Disk, File, Queue), Databases (SQL Database, Cosmos DB, MySQL), Networking (Virtual Network, Load Balancer, CDN), AI/ML (Cognitive Services, Machine Learning), DevOps (Azure DevOps, Pipelines), and Security (Key Vault, Active Directory).

## Q3: What is the difference between IaaS, PaaS, and SaaS in Azure?
**A:** IaaS (Infrastructure as a Service) provides virtual machines and raw infrastructure (Azure VMs). PaaS (Platform as a Service) provides managed platforms for app deployment without managing infrastructure (Azure App Service, Azure Functions). SaaS (Software as a Service) provides fully managed applications (Microsoft 365, Dynamics 365).

## Q4: What is an Azure Resource Group?
**A:** A Resource Group is a logical container that groups related Azure resources for an application, environment, or project. It simplifies management by allowing you to deploy, update, and delete resources as a unit. Resource groups support role-based access control, tagging, and resource lifecycle management.

## Q5: What is Azure Resource Manager (ARM)?
**A:** Azure Resource Manager is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources. ARM handles API requests, enforces policy, and ensures resources are properly provisioned. All Azure operations go through ARM as the central orchestration point.

## Q6: What is the difference between ARM templates and Bicep?
**A:** ARM templates are JSON-based declarative files that define Azure infrastructure. Bicep is a newer domain-specific language that compiles to ARM templates, offering a simpler, more readable syntax with better authoring features like modules and loops. Bicep is considered the preferred authoring experience for Azure infrastructure-as-code.

## Q7: What is Azure Virtual Machine?
**A:** An Azure Virtual Machine is an IaaS offering that provides on-demand, scalable computing resources in the cloud. VMs give you full control over the operating system, allowing you to install any software and configure the environment. They come in various sizes optimized for different workloads (general purpose, compute optimized, memory optimized).

## Q8: What are Azure VM scale sets?
**A:** Azure Virtual Machine Scale Sets (VMSS) allow you to create and manage a group of identical, load-balanced VMs. The number of VM instances can automatically increase or decrease based on demand or a defined schedule. VMSS integrates with Azure Load Balancer and supports up to 1,000 VM instances.

## Q9: What is Azure App Service?
**A:** Azure App Service is a fully managed PaaS for building, deploying, and scaling web apps, RESTful APIs, and mobile backends. It supports multiple languages (.NET, Java, Node.js, Python, PHP) and provides automatic scaling, deployment slots, custom domains, SSL certificates, and continuous deployment from source control.

## Q10: What are deployment slots in Azure App Service?
**A:** Deployment slots are separate instances of your App Service that you can use to deploy new versions of your app. Each slot has its own hostname and can be warmed up before swapping with production. Swapping slots is instant and allows zero-downtime deployments with automatic rollback capability.

## Q11: What is Azure Functions?
**A:** Azure Functions is a serverless compute service that enables you to run event-driven code without managing infrastructure. Functions execute in response to triggers (HTTP, Timer, Blob, Queue, Event Hub) and scale automatically. You pay only for the execution time consumed, making it cost-effective for variable workloads.

## Q12: What is the difference between Azure Functions and Azure Logic Apps?
**A:** Azure Functions is code-first, supporting multiple languages for custom logic execution. Logic Apps is a no-code/low-code workflow orchestration service with a visual designer and 400+ connectors. Functions are better for complex custom logic; Logic Apps excel at integrating services and orchestrating workflows without code.

## Q13: What is Azure Kubernetes Service (AKS)?
**A:** Azure Kubernetes Service is a managed Kubernetes container orchestration service that simplifies deploying, managing, and scaling containerized applications. AKS handles critical tasks like health monitoring, maintenance, and upgrades of the Kubernetes control plane, while you manage and scale the agent nodes.

## Q14: What is Azure Container Instances (ACI)?
**A:** Azure Container Instances is the fastest and simplest way to run a container in Azure without managing VMs or adopting a higher-level orchestrator. ACI provides per-second billing for Linux and Windows containers, making it ideal for burst compute, task automation, and build jobs that don't require full Kubernetes orchestration.

## Q15: What is the difference between ACI and AKS?
**A:** ACI is for single-container workloads that need quick startup without orchestration overhead. AKS is for complex, multi-container applications requiring orchestration, service discovery, scaling, and rolling updates. ACI is simpler and cheaper for small tasks; AKS is for production microservices architectures.

## Q16: What is Azure Blob Storage?
**A:** Azure Blob Storage is an object storage service optimized for storing massive amounts of unstructured data. It supports three blob types: Block blobs (for text/binary data), Append blobs (for log files), and Page blobs (for random access, used by VM disks). It offers hot, cool, cold, and archive access tiers for cost optimization.

## Q17: What are the access tiers in Azure Blob Storage?
**A:** Hot tier is for frequently accessed data with higher storage costs but lower access costs. Cool tier is for infrequently accessed data stored for at least 30 days. Cold tier is for rarely accessed data stored for at least 90 days. Archive tier is for rarely accessed data stored for at least 180 days with the lowest storage cost but highest retrieval latency.

## Q18: What is Azure Blob Storage lifecycle management?
**A:** Lifecycle management policies automatically move blob data between access tiers and delete blobs based on age or modification date. For example, moving blobs from hot to cool after 30 days, to archive after 90 days, and deleting after 365 days. This optimizes storage costs without manual intervention.

## Q19: What is Azure Queue Storage?
**A:** Azure Queue Storage is a service for storing large numbers of messages accessible via HTTP/HTTPS. Each message can be up to 64 KB, and a queue can contain millions of messages. It's commonly used to decouple application components, providing reliable asynchronous communication between producers and consumers.

## Q20: What is Azure Table Storage?
**A:** Azure Table Storage is a NoSQL key-value store for rapid development using massive semi-structured datasets. It stores schemaless data as key-value pairs organized by partition key and row key, providing fast access by key and efficient range queries. It's suitable for storing structured, non-relational data at scale.

## Q21: What is Azure SQL Database?
**A:** Azure SQL Database is a fully managed relational database service based on the latest stable SQL Server engine. It handles patching, backups, and monitoring automatically. Features include elastic pools for shared resources, serverless compute, auto-tuning, built-in intelligence, and geo-replication for high availability.

## Q22: What is the difference between Azure SQL Database and Azure SQL Managed Instance?
**A:** Azure SQL Database is a single database service with managed maintenance but limited SQL Server feature compatibility. Azure SQL Managed Instance provides near-100% SQL Server compatibility with features like SQL Agent, Service Broker, cross-database queries, and CLR. Managed Instance is better for migrating existing SQL Server workloads.

## Q23: What is Azure Cosmos DB?
**A:** Azure Cosmos DB is a globally distributed, multi-model NoSQL database service. It supports document (SQL API), key-value, graph (Gremlin), and column-family (Cassandra) data models. It offers single-digit millisecond latency, five consistency levels, turnkey global distribution, and automatic scaling.

## Q24: What are consistency levels in Azure Cosmos DB?
**A:** Cosmos DB offers five consistency levels: Strong (linearizable, highest cost), Bounded Staleness (bounded lag), Session (consistent within a session, default), Consistent Prefix (updates seen in order), and Eventual (no guarantee on order, lowest cost). You can choose per-request or per-database to balance consistency and performance.

## Q25: What is Azure Cosmos DB partitioning?
**A:** Partitioning in Cosmos DB distributes data across physical partitions using a partition key. Each logical partition holds items sharing the same partition key value. Choosing a good partition key ensures even data distribution, avoids hot partitions, and optimizes query performance. Physical partitions are automatically managed by Cosmos DB.

## Q26: What is Azure Active Directory (Entra ID)?
**A:** Azure Active Directory (now Microsoft Entra ID) is Microsoft's cloud-based identity and access management service. It handles user authentication, single sign-on, multi-factor authentication, conditional access, and identity governance. It integrates with thousands of SaaS applications and is the foundation of Microsoft 365 security.

## Q27: What is the difference between Azure AD and on-premises Active Directory?
**A:** On-premises AD is a directory service for domain-joined devices and applications within a corporate network. Azure AD is a cloud-native identity service designed for web-based authentication using modern protocols (OAuth 2.0, OpenID Connect, SAML). Azure AD doesn't support NTLM, Kerberos, or Group Policy, and uses a flat structure instead of OUs.

## Q28: What is Azure Virtual Network (VNet)?
**A:** Azure Virtual Network is the fundamental building block for private networks in Azure. It enables Azure resources to securely communicate with each other, the internet, and on-premises networks. VNet features include subnets, network security groups, route tables, service endpoints, and private link.

## Q29: What is a Network Security Group (NSG)?
**A:** A Network Security Group contains security rules that allow or deny inbound/outbound network traffic to or from Azure resources. Rules are evaluated by priority (100-4099) in order, with the first matching rule applied. NSGs can be associated with subnets or network interfaces to filter traffic at the network level.

## Q30: What is Azure Load Balancer?
**A:** Azure Load Balancer distributes inbound traffic among healthy VM instances using a five-tuple hash. It operates at Layer 4 (TCP/UDP) and supports high availability, zone redundancy, and automatic failover. SKUs include Basic (free, manual) and Standard (production, health probes, cross-zone load balancing).

## Q31: What is the difference between Azure Load Balancer and Application Gateway?
**A:** Azure Load Balancer operates at Layer 4 (transport) for raw TCP/UDP traffic distribution. Application Gateway is a Layer 7 (HTTP/HTTPS) load balancer with features like URL-based routing, SSL termination, WebSocket support, WAF integration, and cookie-based session affinity. Load Balancer is for general TCP workloads; Application Gateway is for HTTP applications.

## Q32: What is Azure CDN?
**A:** Azure Content Delivery Network caches static content at edge locations worldwide to reduce latency for end users. It accelerates delivery of web content, images, videos, and downloads. Features include custom domain support, HTTPS, compression, caching rules, and integration with Azure Web Apps and Storage.

## Q33: What is Azure DNS?
**A:** Azure DNS is a hosting service for DNS domains, providing name resolution using Microsoft's global network of DNS servers. It supports public and private DNS zones, alias records to map to Azure resources, DNSSEC, and integration with other Azure services. It offers 100% SLA for DNS query availability.

## Q34: What is Azure Key Vault?
**A:** Azure Key Vault is a service for securely storing and accessing secrets, encryption keys, and certificates. It supports hardware security modules (HSMs) for key protection, integrates with Azure AD for access control, provides audit logging, and enables keys and secrets to be used by applications and services.

## Q35: What is the difference between secrets, keys, and certificates in Key Vault?
**A:** Secrets are small pieces of sensitive data like passwords, connection strings, and API keys stored as key-value pairs. Keys are cryptographic keys (RSA, EC, symmetric) used for encryption, signing, and verification. Certificates are X.509 certificates containing keys and identity information, managed and auto-renewed by Key Vault.

## Q36: What is Azure Monitor?
**A:** Azure Monitor is a comprehensive monitoring solution for collecting, analyzing, and acting on telemetry from cloud and on-premises environments. It includes Metrics (numerical time-series data), Logs (Log Analytics workspace with KQL), Alerts (notification and action rules), and Application Insights (application performance monitoring).

## Q37: What is Application Insights?
**A:** Application Insights is an Application Performance Management (APM) feature of Azure Monitor. It provides distributed tracing, request/response tracking, exception monitoring, dependency tracking, performance metrics, and live metrics. It automatically detects performance anomalies and integrates with CI/CD pipelines for release monitoring.

## Q38: What is Log Analytics in Azure?
**A:** Log Analytics is a tool in the Azure portal for querying and analyzing log data collected by Azure Monitor. It uses Kusto Query Language (KQL) to search, filter, and visualize data. Logs can come from Azure resources, applications, operating systems, and custom sources, enabling deep operational insights.

## Q39: What is Kusto Query Language (KQL)?
**A:** KQL is a read-only query language used in Azure Monitor Log Analytics, Azure Data Explorer, and other services. It supports filtering, grouping, aggregation, joins, and time-series analysis. KQL queries are optimized for fast analysis of large volumes of log data with a syntax similar to SQL but designed for exploration.

## Q40: What is Azure DevOps?
**A:** Azure DevOps is a suite of development tools for planning, building, testing, and deploying applications. It includes Boards (work tracking), Repos (Git repositories), Pipelines (CI/CD), Test Plans (manual/exploratory testing), and Artifacts (package management). It supports any language, platform, and cloud.

## Q41: What is Azure DevOps Pipelines?
**A:** Azure DevOps Pipelines is a CI/CD service that automates building, testing, and deploying code to any target. It supports YAML-based pipeline definitions, multi-stage pipelines, parallel jobs, matrix strategies, and integration with any platform. It connects to GitHub, Bitbucket, and other repositories, and deploys to Azure, AWS, GCP, and on-premises.

## Q42: What is the difference between build and release pipelines in Azure DevOps?
**A:** Build pipelines compile source code, run tests, and produce artifacts (binaries, packages). Release pipelines deploy those artifacts to target environments with approval gates, environment-specific configurations, and deployment strategies (manual, automated, rolling). Build pipelines focus on quality; release pipelines focus on delivery.

## Q43: What is GitHub Actions and how does it compare to Azure Pipelines?
**A:** GitHub Actions is GitHub's native CI/CD platform using YAML workflows triggered by GitHub events. Azure Pipelines is Microsoft's CI/CD service with broader platform support and deeper Azure integration. GitHub Actions has a larger marketplace of community actions; Azure Pipelines has more enterprise features and multi-cloud support.

## Q44: What is Azure Service Bus?
**A:** Azure Service Bus is a fully managed enterprise message broker supporting queues (point-to-point) and topics (publish-subscribe). It provides reliable message delivery, ordering, duplicate detection, sessions, and dead-lettering. It supports AMQP, HTTP, and SBMP protocols and integrates with Azure Functions and Logic Apps.

## Q45: What is the difference between Azure Service Bus and Azure Queue Storage?
**A:** Service Bus is an enterprise message broker with advanced features like topics/subscriptions, sessions, duplicate detection, dead-letter queues, and message deferral. Queue Storage is a simpler, cheaper messaging service for basic queuing with fewer features. Service Bus is for enterprise integration; Queue Storage is for basic task queuing.

## Q46: What is Azure Event Hubs?
**A:** Azure Event Hubs is a big data streaming platform and event ingestion service capable of receiving and processing millions of events per second. It supports real-time and batch processing, event retention of up to 90 days, Kafka compatibility, and capture to Azure Storage and Data Lake. It's designed for high-throughput event streaming scenarios.

## Q47: What is the difference between Event Hubs and Event Grid?
**A:** Event Hubs is a high-throughput event streaming service for ingesting millions of events per second from applications and devices. Event Grid is a lightweight event routing service that delivers events from Azure and custom sources to subscribers using a publish-subscribe model. Event Hubs is for data streaming; Event Grid is for event-driven architecture.

## Q48: What is Azure API Management?
**A:** Azure API Management is a fully managed service for publishing, securing, transforming, maintaining, and monitoring APIs. It provides a gateway for API calls, developer portal for documentation, rate limiting, authentication, caching, request/response transformation, and analytics. It supports REST, SOAP, and GraphQL APIs.

## Q49: What are the tiers of Azure API Management?
**A:** Tiers include Developer (for non-production, single unit), Basic (for entry-level production), Standard (for medium-scale production), Premium (for enterprise features like multi-region, VNet integration), and Consumption (serverless, pay-per-call). Each tier differs in SLA, scale limits, features, and pricing.

## Q50: What is Azure Active Directory B2C?
**A:** Azure AD B2C (Business-to-Consumer) is a customer identity access management (CIAM) service. It handles billions of identities with custom sign-up/sign-in experiences, social identity providers, MFA, and custom policies. It supports OAuth 2.0, OpenID Connect, and SAML, allowing you to customize every authentication flow.

## Q51: What is Azure Logic Apps?
**A:** Azure Logic Apps is a cloud service for automating and orchestrating workflows and business processes. It provides a visual designer with 400+ connectors to SaaS and enterprise systems. Logic Apps can trigger on events, execute scheduled tasks, and handle complex workflows with conditions, loops, and error handling.

## Q52: What is Azure Policy?
**A:** Azure Policy is a service for creating, assigning, and managing policies that enforce rules and effects on Azure resources. Policies ensure resources comply with organizational standards. Built-in policies cover common rules (allowed VM sizes, required tags), and custom policies use JSON definitions. Effects include Deny, Audit, and DeployIfNotExists.

## Q53: What is Azure Blueprints?
**A:** Azure Blueprints enable cloud architects to define a repeatable set of Azure resources that adhere to organizational standards. A blueprint can include role assignments, policy assignments, Azure Resource Manager templates, and resource groups. It provides a governed way to deploy environments with consistent configurations.

## Q54: What is Azure Cost Management?
**A:** Azure Cost Management is a suite of tools for monitoring, allocating, and optimizing cloud costs. It provides cost analysis, budgeting, alerting, recommendations, and export capabilities. It supports cost allocation through tags, departments, and accounts, and integrates with billing to track spending across subscriptions.

## Q55: What is the Azure Well-Architected Framework?
**A:** The Azure Well-Architected Framework is a set of best practices across five pillars: Cost Optimization, Operational Excellence, Performance Efficiency, Reliability, and Security. It provides actionable recommendations for designing and operating cloud workloads on Azure, assessed through the Azure Advisor and Well-Architected Review tools.

## Q56: What is Azure Availability Zones?
**A:** Availability Zones are physically separate locations within an Azure region, each with independent power, networking, and cooling. Deploying resources across multiple zones protects applications from data center failures. Each zone consists of one or more data centers, and they are connected by low-latency fiber networks.

## Q57: What is the difference between Azure Availability Zones and Azure Regions?
**A:** Azure Regions are geographical areas containing one or more data centers (e.g., East US, West Europe). Availability Zones are separate data center facilities within a single region. Regions provide geographic redundancy and data residency compliance. Zones provide high availability within a region against infrastructure failures.

## Q58: What is Azure Site Recovery?
**A:** Azure Site Recovery is a disaster recovery as a service (DRaaS) that replicates workloads running on physical and virtual machines from a primary site to Azure (or secondary site). It supports automatic failover and failback, recovery plan customization, and testing of disaster recovery without downtime.

## Q59: What is Azure Backup?
**A:** Azure Backup is a scalable cloud backup service that protects on-premises servers, VMs, SQL databases, Azure file shares, and more. It provides centralized management, long-term retention, instant restore, and encryption. It supports daily, weekly, monthly, and yearly retention policies with GRS backup vaults.

## Q60: What is Azure Traffic Manager?
**A:** Azure Traffic Manager is a DNS-based traffic load balancer that distributes traffic across multiple Azure regions or endpoints. It supports routing methods: Priority, Weighted, Performance, Geographic, MultiValue, and Subnet. It provides automatic failover and health monitoring to route traffic to healthy endpoints.

## Q61: What is Azure Front Door?
**A:** Azure Front Door is a global, scalable entry point for fast delivery of web applications. It combines global HTTP load balancing with SSL offloading, path-based routing, instant global failover, and WAF protection. It operates at Layer 7 and provides edge caching for static and dynamic content.

## Q62: What is the difference between Traffic Manager, Front Door, and Load Balancer?
**A:** Traffic Manager is DNS-based routing across global endpoints (Layer 7 DNS). Front Door is global HTTP load balancing with edge caching and WAF (Layer 7). Load Balancer is regional TCP/UDP load balancing (Layer 4). Traffic Manager for DNS routing, Front Door for global HTTP applications, Load Balancer for internal or regional TCP workloads.

## Q63: What is Azure Cosmos DB free tier?
**A:** The Cosmos DB free tier provides 1000 RU/s provisioned throughput and 25 GB of storage at no cost. It's ideal for learning, prototyping, and small applications. The free tier applies to the first Cosmos DB account created in a subscription and can be used with any API (SQL, MongoDB, Cassandra, Gremlin, Table).

## Q64: What is Azure Functions Premium plan?
**A:** The Azure Functions Premium (EP1) plan provides pre-warmed instances to eliminate cold start, VNet integration, and unlimited execution duration. It bridges the gap between consumption (serverless, pay-per-use) and dedicated App Service plans. It's ideal for functions that need VNet access or have consistent workloads.

## Q65: What is Azure Static Web Apps?
**A:** Azure Static Web Apps is a service for hosting static websites with built-in CI/CD from GitHub. It supports frameworks like React, Angular, Vue, and Hugo. Features include global CDN, custom domains, SSL, authentication, API integration with Azure Functions, and role-based access control.

## Q66: What is Azure SignalR Service?
**A:** Azure SignalR Service is a managed service for adding real-time web functionality to applications. It provides serverless and managed modes for broadcasting, push notifications, and bidirectional communication over WebSockets, Server-Sent Events, and long polling. It scales automatically to handle millions of concurrent connections.

## Q67: What is Azure Cognitive Services?
**A:** Azure Cognitive Services is a collection of AI services and APIs for adding intelligent features to applications. Categories include Vision (Computer Vision, Face, Custom Vision), Language (Text Analytics, Translator, Language Understanding), Speech (Speech-to-Text, Text-to-Speech), Decision (Anomaly Detector, Content Moderator), and OpenAI Service.

## Q68: What is Azure Machine Learning?
**A:** Azure Machine Learning is a cloud platform for training, deploying, and managing machine learning models. It provides notebooks, automated ML, designer (drag-and-drop), MLOps capabilities, and integration with popular frameworks (TensorFlow, PyTorch, scikit-learn). It supports managed endpoints, managed online endpoints, and Kubernetes deployment.

## Q69: What is Azure OpenAI Service?
**A:** Azure OpenAI Service provides REST API access to OpenAI's language models (GPT-4, GPT-3.5, DALL-E, Whisper) with the security and compliance of Azure. It offers content filtering, data privacy, regional availability, and integration with Azure AI services. Models are accessible via API, Azure SDK, and Azure OpenAI Studio.

## Q70: What is Azure Data Lake Storage?
**A:** Azure Data Lake Storage Gen2 is a scalable and secure data lake for high-performance analytics workloads. It combines the capabilities of Azure Data Lake Storage Gen1 with Azure Blob Storage, providing a hierarchical namespace, POSIX-compliant ACLs, and integration with Apache Spark, Azure Synapse, and HDInsight.

## Q71: What is Azure Synapse Analytics?
**A:** Azure Synapse Analytics is an unlimited analytics service that brings together enterprise data warehousing, big data analytics, and data integration. It provides SQL pools (dedicated and serverless), Spark pools, data exploration, visualization, and pipelines for data integration. It unifies these capabilities in a single workspace.

## Q72: What is the difference between dedicated and serverless SQL pools in Synapse?
**A:** Dedicated SQL pools provide reserved compute capacity for predictable, performance-intensive workloads. Serverless SQL pools use a pay-per-query model with no infrastructure management, ideal for ad-hoc queries and exploration. Dedicated pools are for production data warehousing; serverless pools are for on-demand analytics.

## Q73: What is Azure Data Factory?
**A:** Azure Data Factory (ADF) is a cloud-based ETL/ELT service for orchestrating and automating data movement and transformation. It connects to 100+ data sources, provides a visual authoring experience, and supports complex data pipelines. It integrates with Azure Databricks, Synapse, and HDInsight for compute.

## Q74: What is the difference between ETL and ELT?
**A:** ETL (Extract, Transform, Load) transforms data before loading it into the target system, suitable when processing power is limited. ELT (Extract, Load, Transform) loads raw data first, then transforms it in the target system, leveraging the target system's compute power. ELT is preferred with cloud data warehouses that have powerful compute.

## Q75: What is Azure Databricks?
**A:** Azure Databricks is a fast, easy, and collaborative Apache Spark-based analytics platform optimized for Azure. It provides interactive notebooks, collaborative workspaces, integrated ML tools (MLflow), and SQL analytics. It's ideal for big data processing, data engineering, and machine learning at scale.

## Q76: What is Azure Event Grid?
**A:** Azure Event Grid is a fully managed event routing service that uses a publish-subscribe model. It routes events from Azure services and custom sources to handlers like Azure Functions, Logic Apps, and WebHooks. It provides features like event domains, advanced filtering, retry policies, and dead-lettering.

## Q77: What is Azure Relay?
**A:** Azure Relay enables hybrid applications to securely expose on-premises services to the cloud without opening inbound firewall ports. It provides WCF relay (TCP/HTTP) and Hybrid Connections (WebSocket-based). Hybrid Connections is recommended for new projects, enabling bidirectional communication between cloud and on-premises.

## Q78: What is Azure Private Link?
**A:** Azure Private Link provides private connectivity from a virtual network to Azure PaaS services, customer-owned services, or Microsoft partner services. Traffic between the virtual network and the service travels through the Microsoft backbone network, eliminating public internet exposure and reducing data exfiltration risks.

## Q79: What is Azure Private Endpoint?
**A:** A Private Endpoint is a network interface that uses a private IP address from your VNet to connect to Azure services via Private Link. It provides secure connectivity by keeping traffic within the Azure backbone. Private endpoints are used to access Azure SQL, Storage, Cosmos DB, and other PaaS services privately.

## Q80: What is Azure Bastion?
**A:** Azure Bastion is a fully managed PaaS service that provides secure and seamless RDP and SSH access to VMs directly through the Azure Portal over TLS. It eliminates the need to expose VMs to public IP addresses, reducing attack surface. It's deployed in a VNet and provides native browser-based access.

## Q81: What is Azure Sentinel?
**A:** Azure Sentinel (now Microsoft Sentinel) is a cloud-native SIEM and SOAR solution. It provides intelligent security analytics across the entire enterprise, collecting data at cloud scale, detecting threats with AI, and automating response with playbooks. It integrates with Microsoft 365, Azure, and third-party security tools.

## Q82: What is Azure Firewall?
**A:** Azure Firewall is a managed, cloud-based network security service that protects Azure Virtual Network resources. It provides application FQDN filtering, network traffic filtering, threat intelligence-based filtering, and forced tunneling. Available as Standard and Premium tiers with additional features like TLS inspection and IDPS.

## Q83: What is Azure DDoS Protection?
**A:** Azure DDoS Protection provides enhanced mitigation for DDoS attacks against Azure resources. The Standard tier provides adaptive tuning, attack analytics, cost protection, and rapid support. It automatically detects and mitigates volumetric, protocol, and application layer attacks targeting public IP addresses and VNet resources.

## Q84: What is Azure Web Application Firewall (WAF)?
**A:** Azure WAF protects web applications from common web exploits and vulnerabilities (OWASP Top 10). It provides managed rule sets for SQL injection, XSS, and other attacks, plus custom rules for application-specific protection. WAF can be deployed on Application Gateway, Front Door, and Azure CDN.

## Q85: What is Azure Confidential Computing?
**A:** Azure Confidential Computing protects data in use by performing computation in hardware-based trusted execution environments (TEEs). It ensures that even Azure operators cannot access your data during processing. It uses Intel SGX enclaves or AMD SEV-SNP VMs to encrypt data in memory.

## Q86: What is Azure Cosmos DB serverless?
**A:** Cosmos DB serverless is a capacity model that charges per Request Unit (RU) consumed by database operations without pre-provisioning throughput. It's ideal for workloads with unpredictable or intermittent traffic. You pay only for the operations you perform, making it cost-effective for development, testing, and low-traffic applications.

## Q87: What is the RU/s model in Cosmos DB?
**A:** Request Units per second (RU/s) is the throughput currency in Cosmos DB. 1 RU/s represents the cost of a single point read of a 1 KB item. All operations (reads, writes, queries) are assigned RU costs based on their complexity. You provision RU/s to guarantee performance and pay for what you provision.

## Q88: What is Azure App Configuration?
**A:** Azure App Configuration is a service for centrally managing application settings and feature flags. It provides a key-value store with hierarchical namespaces, labels, and revision history. It integrates with Azure Functions, App Service, and Kubernetes, enabling dynamic configuration changes without redeployment.

## Q89: What are feature flags in Azure App Configuration?
**A:** Feature flags are boolean or percentage-based switches that allow you to dynamically enable or disable features in your application without redeployment. They support gradual rollouts, A/B testing, and ring-based deployments. Feature flags can be targeting-based, percentage-based, or time-window based.

## Q90: What is Azure Event Hubs Capture?
**A:** Event Hubs Capture is a feature that automatically persists event data to Azure Blob Storage or Data Lake Storage in Avro format. It enables near-real-time analytics with Azure Data Explorer, Synapse, or Databricks. Capture reduces the need for custom ingestion code and provides reliable, cost-effective data archival.

## Q91: What is Azure API for FHIR?
**A:** Azure API for FHIR (Fast Healthcare Interoperability Resources) is a managed implementation of the HL7 FHIR standard for health data exchange. It enables healthcare applications to store, retrieve, and exchange clinical data using RESTful APIs. It supports SMART on FHIR and provides compliance with healthcare regulations.

## Q92: What is Azure Digital Twins?
**A:** Azure Digital Twins is a platform for creating digital models of real-world environments using IoT data. It uses a graph-based digital twin ontology (DTDL models) to represent relationships between entities. It enables real-time monitoring, simulation, and optimization of physical systems.

## Q93: What is Azure IoT Hub?
**A:** Azure IoT Hub is a managed service for bidirectional communication between IoT applications and devices. It supports device provisioning, device management, message routing, and integration with other Azure services. It handles millions of devices with per-device authentication and device twin state management.

## Q94: What is Azure Cosmos DB Change Feed?
**A:** The Change Feed in Cosmos DB is a persistent log of items that have been inserted or updated in a container. It enables building event-driven architectures by processing changes in real-time. Consumers can use it for data replication, aggregation, serverless computing, and triggered actions without polling.

## Q95: What is the difference between Azure Storage redundancy options (LRS, GRS, ZRS, GZRS)?
**A:** LRS (Locally Redundant Storage) copies data three times within one data center. GRS (Geo-Redundant Storage) adds async replication to a paired region. ZRS (Zone-Redundant Storage) copies data across three availability zones. GZRS (Geo-Zone-Redundant Storage) combines ZRS within a region with geo-replication for maximum durability.

## Q96: What is Azure Cognitive Search?
**A:** Azure Cognitive Search (now Azure AI Search) is a cloud search service with built-in AI capabilities. It provides full-text search, faceted navigation, filters, and AI-enhanced indexing using built-in skillsets for OCR, entity recognition, key phrase extraction, and language detection. It integrates with Azure OpenAI for chat over your data.

## Q97: What is Azure Communication Services?
**A:** Azure Communication Services is a set of rich communication APIs for adding voice/video calling, SMS, email, chat, and phone number management to applications. It provides client libraries for web, iOS, and Android, and integrates with Microsoft Teams for interoperability. It scales to millions of users globally.

## Q98: What is Azure Cache for Redis?
**A:** Azure Cache for Redis is a managed Redis cache service for improving application performance. It provides in-memory data storage for ultra-fast read/write operations, session management, and message brokering. It supports data structures like strings, hashes, lists, sets, and sorted sets with multiple tiers (Basic, Standard, Premium, Enterprise).

## Q99: What is Azure Dev Box?
**A:** Azure Dev Box is a managed service for creating cloud-based workstations optimized for developer productivity. It provides pre-configured, project-specific development environments with all the tools, code, and dependencies needed. It integrates with Azure DevOps and GitHub for automated setup and compliance.

## Q100: What are the best practices for securing an Azure environment?
**A:** Best practices include: implementing Azure AD with MFA and conditional access, using Azure Policy for governance, encrypting data at rest and in transit with Key Vault, configuring NSGs and Azure Firewall for network security, enabling Azure Defender for threat protection, using Private Endpoints for service access, following least-privilege RBAC, enabling diagnostic logging with Azure Monitor and Sentinel, and regularly reviewing recommendations in Azure Advisor.
