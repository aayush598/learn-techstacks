# Ansible Playbooks

Ansible is an agentless automation tool that manages infrastructure and configuration via SSH. For recommendation systems, Ansible handles tasks that fall outside Kubernetes — provisioning VMs for training clusters, configuring databases, setting up monitoring stacks, managing secrets, and bootstrapping nodes. While Terraform provisions infrastructure and Kubernetes orchestrates containers, Ansible configures the systems those services run on. This document covers playbook structure, role organization, inventory management, variables, secrets, idempotency, and the Ansible vs Terraform decision.

---

## 1. Playbook Structure

### 1.1 Anatomy of a Playbook

A playbook is a YAML file defining a series of plays. Each play maps a set of hosts to a set of tasks.

**Structural hierarchy:**

| Level | Element | Purpose |
|---|---|---|
| 1 | Play | Maps hosts to tasks (runs on a group of hosts) |
| 2 | Task | Single unit of work (calls a module) |
| 3 | Module | Executable unit (apt, pip, template, copy, etc.) |
| 4 | Handler | Task triggered by `notify` (runs once at end of play) |
| 5 | Role | Reusable collection of tasks, handlers, templates, variables |

### 1.2 Playbook Organization for Recommendation Systems

| Playbook | Purpose | Target Hosts |
|---|---|---|
| `site.yml` | Master playbook, includes all others | All |
| `webservers.yml` | Configure API server hosts | API servers |
| `modelservers.yml` | Configure ML serving hosts | Model servers |
| `databases.yml` | Configure PostgreSQL hosts | Database servers |
| `monitoring.yml` | Configure Prometheus, Grafana | Monitoring servers |
| `training.yml` | Configure GPU training cluster | Training nodes |
| `security.yml` | Apply security hardening | All |

### 1.3 Task Design Principles

| Principle | Example | Anti-Pattern |
|---|---|---|
| Idempotent | `apt: name=nginx state=present` | `shell: apt-get install -y nginx` |
| Declarative | `file: path=/etc/nginx state=directory` | `shell: mkdir -p /etc/nginx` |
| Parameterized | `pip: name={{ item }} state=latest` with loop | Separate task for each package |
| Checked | `stat` module before modifying files | Blindly overwriting configuration |
| Logged | Use `register` to capture output | Ignoring command results |

---

## 2. Role Organization

### 2.1 Role Directory Structure

```
roles/
├── postgresql/
│   ├── tasks/
│   │   ├── main.yml           # Entry point
│   │   ├── install.yml        # Package installation
│   │   ├── configure.yml      # Configuration
│   │   └── secure.yml         # Security hardening
│   ├── handlers/
│   │   └── main.yml           # Service restart handlers
│   ├── templates/
│   │   ├── postgresql.conf.j2 # Configuration template
│   │   └── pg_hba.conf.j2     # Authentication template
│   ├── files/
│   │   └── backup.sh          # Static files to deploy
│   ├── vars/
│   │   └── main.yml           # Role variables
│   ├── defaults/
│   │   └── main.yml           # Default variables (overridable)
│   └── meta/
│       └── main.yml           # Role dependencies
```

### 2.2 Key Roles for Recommendation Systems

| Role | Purpose | Key Tasks |
|---|---|---|
| `common` | Base OS configuration | NTP, timezone, sysctl tuning, users |
| `postgresql` | Database setup and config | Install, configure replication, backups |
| `redis` | Cache layer setup | Install, configure persistence, replication |
| `kafka` | Event streaming setup | Install Zookeeper/Kafka, topic creation |
| `python` | Python environment | Install Python, pip, virtualenvs |
| `model_artifacts` | Model artifact management | Download from S3, verify checksums, place on disk |
| `monitoring_agent` | Node-level monitoring | Install Prometheus node_exporter, configure |
| `log_shipping` | Centralized logging | Install Fluent Bit, configure forwarding |
| `firewall` | Network security | UFW/iptables rules, port management |
| `ssl_certificates` | TLS certificate management | Generate/request certificates, auto-renewal |

### 2.3 Role Dependencies

Define dependencies in `meta/main.yml`:

- `common` runs before all other roles
- `python` runs before `model_artifacts`
- `firewall` runs before any service role
- `postgresql` and `redis` run before application roles

### 2.4 Galaxy and Collections

- Use `ansible-galaxy role install` for community roles
- Use `ansible-galaxy collection install` for namespace-scoped collections
- Pin versions in `requirements.yml` for reproducibility
- Verify role checksums before installing in production

---

## 3. Inventory Management

### 3.1 Static Inventory

Define hosts directly in INI or YAML format:

**INI format:**

```
[api_servers]
api-1 ansible_host=10.0.1.10
api-2 ansible_host=10.0.1.11
api-3 ansible_host=10.0.1.12

[model_servers]
model-1 ansible_host=10.0.2.10 gpu_type=v100
model-2 ansible_host=10.0.2.11 gpu_type=a10g

[databases]
db-primary ansible_host=10.0.3.10
db-replica ansible_host=10.0.3.11

[training]
train-gpu-[01:08] ansible_host=10.0.4.{1..8}
```

### 3.2 Dynamic Inventory

Query cloud APIs to generate inventory at runtime:

| Plugin | Cloud | Use Case |
|---|---|---|
| `amazon.aws.aws_ec2` | AWS | Auto-discover EC2 instances by tags |
| `azure.azcollection.azure_rm` | Azure | Auto-discover Azure VMs |
| `google.cloud.gcp_compute` | GCP | Auto-discover GCE instances |
| `kubernetes.core.k8s` | Kubernetes | Discover pods, services, nodes |
| Custom script | Any | Query internal CMDB or service registry |

### 3.3 Inventory Patterns for ML Infrastructure

| Group | Dynamic Source | Tag/Label Filter |
|---|---|---|
| Training nodes | AWS EC2 | `role=training`, `gpu=true` |
| Serving nodes | EC2 or K8s nodes | `role=serving`, `env=prod` |
| Database nodes | RDS endpoints or EC2 | `role=database`, `env=prod` |

---

## 4. Variable Management

### 4.1 Variable Precedence (Highest to Lowest)

| Level | Location | Example |
|---|---|---|
| 1 | Extra vars (`-e`) | `ansible-playbook site.yml -e "debug=true"` |
| 2 | Task-level vars | `vars:` section in a task |
| 3 | Role defaults | `roles/x/defaults/main.yml` |
| 4 | Inventory vars | Host/group vars in inventory |
| 5 | Play vars | `vars:` section in a play |
| 6 | Extra vars file | `vars_files: group_vars/all.yml` |

### 4.2 Group Variables Structure

```
group_vars/
├── all.yml                 # Variables for all hosts
├── api_servers.yml         # Variables for API servers
├── model_servers.yml       # Variables for model servers
├── databases.yml           # Variables for databases
├── prod.yml                # Production-specific overrides
└── stg.yml                 # Staging-specific overrides
```

### 4.3 Host Variables

Individual host overrides in `host_vars/`:

```
host_vars/
├── db-primary.yml          # Primary DB-specific config
└── model-gpu-1.yml         # GPU type, memory for specific node
```

### 4.4 Variable Naming Conventions

| Scope | Prefix | Example |
|---|---|---|
| Application | `app_` | `app_port: 8080` |
| Database | `db_` | `db_host: postgres.internal` |
| Model | `model_` | `model_path: /opt/models/latest` |
| Feature store | `feature_` | `feature_store_ttl: 3600` |
| Environment | `env_` | `env_name: production` |

---

## 5. Secrets Management with Ansible Vault

### 5.1 Vault Usage Patterns

| Pattern | Implementation | Security Level |
|---|---|---|
| Encrypted files | `ansible-vault encrypt group_vars/prod/vault.yml` | Good |
| Encrypted strings | `!vault` inline in YAML files | Good |
| External secret lookup | `community.general.hashi_vault` lookup | Best |
| AWS Secrets Manager | `amazon.aws.secretsmanager_secret` | Best |

### 5.2 Vault File Organization

```
group_vars/
├── prod/
│   ├── vars.yml           # Non-secret variables (plain YAML)
│   └── vault.yml          # Encrypted secrets (vault-encrypted)
├── stg/
│   ├── vars.yml
│   └── vault.yml
└── all/
    └── vault.yml          # Shared secrets (encrypted)
```

### 5.3 Vault Best Practices

- Use different vault passwords per environment (prod, staging, dev)
- Rotate vault passwords quarterly
- Store vault passwords in a password manager, not in Git
- Never log vault-encrypted content in verbose mode
- Use `ansible-vault view` instead of decrypting entire files
- Separate secret and non-secret variables into different files

---

## 6. Idempotent Playbooks

### 6.1 Idempotency Principles

An idempotent playbook produces the same result whether run once or many times.

| Module | Idempotent? | Notes |
|---|---|---|
| `apt` | Yes | Checks if package is already installed |
| `copy` | Yes | Compares checksums before overwriting |
| `template` | Yes | Compares rendered output before writing |
| `service` | Yes | Checks current state before starting/stopping |
| `user` | Yes | Checks if user exists before creating |
| `shell` | **No** | Always executes — avoid or use `creates`/`removes` |

### 6.2 Ensuring Idempotency

- Use declarative modules (`apt`, `file`, `template`) instead of imperative (`shell`, `command`)
- When using `shell`/`command`, always provide `creates`, `removes`, or `when` conditions
- Use `changed_when` and `failed_when` to properly report state
- Test playbooks by running them twice — second run should report zero changes

---

## 7. Ansible vs Terraform

| Dimension | Ansible | Terraform |
|---|---|---|
| Primary purpose | Configuration management | Infrastructure provisioning |
| Approach | Imperative (procedural tasks) | Declarative (desired state) |
| State management | Stateless (re-runs are idempotent) | State file (tracks real infrastructure) |
| Execution | SSH to target hosts | API calls to cloud providers |
| Best for | Software configuration, deployment | VMs, networks, storage, DNS |
| ML use case | Configure training servers, deploy models | Provision GPU instances, VPCs, S3 buckets |
| Learning curve | Lower (YAML + Jinja2) | Moderate (HCL, state management) |
| Testing | `molecule` (Docker-based) | `terratest` (Go-based) |

### 7.1 When to Use Each

| Task | Use | Rationale |
|---|---|---|
| Create VPC and subnets | Terraform | Cloud resource provisioning |
| Install PostgreSQL on a VM | Ansible | Configuration management |
| Provision GPU instances | Terraform | Cloud resource provisioning |
| Configure CUDA drivers | Ansible | Software configuration |
| Create S3 bucket for models | Terraform | Cloud resource provisioning |
| Deploy model files to S3 | Ansible (or AWS CLI) | Data/config management |
| Create Kubernetes cluster | Terraform | Infrastructure provisioning |
| Deploy apps to Kubernetes | Helm/ArgoCD (not Ansible) | Container orchestration |

### 7.2 Combined Terraform + Ansible Workflow

1. **Terraform** provisions infrastructure (VMs, networks, storage)
2. **Terraform** generates dynamic inventory for Ansible
3. **Ansible** configures provisioned infrastructure
4. **Ansible** deploys application code and model artifacts
5. **Ansible** runs health checks and validation
