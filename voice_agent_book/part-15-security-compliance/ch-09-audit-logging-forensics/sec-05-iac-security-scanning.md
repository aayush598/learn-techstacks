# Section 05: Infrastructure as Code (IaC) Security Scanning

IaC security scanning detects misconfigurations and security issues in infrastructure definitions before deployment. Terraform, CloudFormation, Kubernetes manifests, and Dockerfiles are scanned for: overly permissive IAM policies, publicly accessible storage, unencrypted data volumes, insecure network configurations, and container privilege escalation risks.

Scanning tools: Checkov (Terraform, CloudFormation, Kubernetes), tfsec (Terraform security), terrascan (IaC compliance), kube-bench (Kubernetes CIS benchmark), kube-hunter (Kubernetes penetration testing), and Docker Bench (container security). Scans run in CI/CD as part of the infrastructure pipeline. Critical findings block deployment.

Policy examples: S3 buckets must have public access blocked, database instances must have encryption enabled, Kubernetes pods cannot run as root, network ACLs must restrict SSH to bastion hosts, IAM roles must use least privilege policies, and load balancers must have WAF enabled. Policy violations are reported with the specific resource, line number, and remediation guidance.
