# Section 02: Network Security Architecture

## Network Segmentation

The network is divided into **three tiers**: public subnet (load balancers, CDN), private subnet (application services), and data subnet (databases, caches). Each tier has strict firewall rules and no direct access between tiers except through defined gateways.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    NETWORK SEGMENTATION                             │
│                                                                     │
│  Internet                                                           │
│     │                                                               │
│     ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  TIER 1: PUBLIC SUBNET                                       │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │  CDN     │  │  Cloud   │  │  DDoS    │  │  WAF       │  │   │
│  │  │ (Static) │  │  LB      │  │  Shield  │  │ (ModSec)   │  │   │
│  │  └──────────┘  └────┬─────┘  └──────────┘  └────────────┘  │   │
│  │                     │                                         │   │
│  │                     ▼                                         │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  API Gateway (Next.js middleware, TLS termination)     │  │   │
│  │  │  Ingress: 443 (HTTPS), 80→443 redirect                │  │   │
│  │  │  WAF: SQL injection, XSS, path traversal rules        │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                    ┌─────────┴─────────┐                          │
│                    │   Security Group   │                          │
│                    │   Allow: 443 from  │                          │
│                    │   LB only          │                          │
│                    └─────────┬─────────┘                          │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  TIER 2: PRIVATE SUBNET (Application)                       │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │  Agent   │  │   Call   │  │  Voice   │  │    AI      │  │   │
│  │  │  Service │  │  Service │  │  Service │  │   Service  │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │ Billing  │  │  Notif.  │  │WebSocket │  │  Media     │  │   │
│  │  │ Service  │  │ Service  │  │ Server   │  │  Server    │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                    ┌─────────┴─────────┐                          │
│                    │   Security Group   │                          │
│                    │   Allow: 443 from  │                          │
│                    │   Tier 2 only     │                          │
│                    └─────────┬─────────┘                          │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  TIER 3: DATA SUBNET                                        │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │PostgreSQL│  │  Redis   │  │  MinIO   │  │ClickHouse  │  │   │
│  │  │ (Port    │  │ (Port    │  │ (Port    │  │ (Port      │  │   │
│  │  │  5432)   │  │  6379)   │  │  9000)   │  │  8123)    │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  Apache Kafka (Port 9092, 9093 for mTLS)              │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Security Group Configuration

```hcl
# Terraform security group rules
resource "hcloud_firewall" "public_tier" {
  name = "public-tier"

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "443"
    source_ips = ["0.0.0.0/0"]
    description = "HTTPS from internet"
  }

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "80"
    source_ips = ["0.0.0.0/0"]
    description = "HTTP redirect to HTTPS"
  }

  rule {
    direction = "out"
    protocol  = "tcp"
    port      = "443"
    destination_ips = [var.private_subnet_cidr]
    description = "Egress to private tier"
  }

  rule {
    direction = "out"
    protocol  = "udp"
    port      = "53"
    destination_ips = ["8.8.8.8", "1.1.1.1"]
    description = "DNS resolution"
  }
}

resource "hcloud_firewall" "private_tier" {
  name = "private-tier"

  rule {
    direction = "in"
    protocol  = "tcp"
    port      = "3000-3100"
    source_ips = [var.public_subnet_cidr]
    description = "Inbound from API gateway"
  }

  rule {
    direction = "out"
    protocol  = "tcp"
    port      = "5432"
    destination_ips = [var.data_subnet_cidr]
    description = "Egress to PostgreSQL"
  }

  rule {
    direction = "out"
    protocol  = "tcp"
    port      = "6379"
    destination_ips = [var.data_subnet_cidr]
    description = "Egress to Redis"
  }

  rule {
    direction = "out"
    protocol  = "tcp"
    port      = "9092-9093"
    destination_ips = [var.data_subnet_cidr]
    description = "Egress to Kafka"
  }
}
```

## VPN Access (Bastion)

```typescript
// Developer VPN access via WireGuard
// Bastion host: bastion.voiceagent.dev (only accessible via VPN)

interface VpnAccess {
  user: string;
  role: 'developer' | 'admin' | 'readonly';
  publicKey: string;
  allowedCIDRs: string[];       // e.g., ['10.0.1.0/24'] — private subnet
  allowedPorts: number[];       // e.g., [5432] — PostgreSQL
  expiresAt: Date;
}

// Access is time-limited and revoked on role change or termination
// All actions through bastion are logged to audit trail
```

## DDoS Protection

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DDoS PROTECTION LAYERS                           │
│                                                                     │
│  Layer 1: Cloud Edge                                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  • Anycast DNS (Cloudflare or similar)                      │   │
│  │  • Traffic filtering based on reputation                   │   │
│  │  • L3/L4 DDoS mitigation (SYN flood, UDP amplification)    │   │
│  │  • Rate limiting at edge (1000 req/s per IP)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Layer 2: Load Balancer                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  • Connection limiting (100 concurrent per IP)              │   │
│  │  • Slow loris protection (request timeout: 10s)             │   │
│  │  • TLS termination at LB (CPU offload, resumption)         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Layer 3: Application (WAF)                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  • ModSecurity / Coraza ruleset                             │   │
│  │  • Rate limiting per API key (see Ch 07)                    │   │
│  │  • Request size limit: 1MB                                  │   │
│  │  • Path validation: reject non-API paths                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Segmentation | 3-tier (public, private, data) | Industry best practice, limits blast radius |
| Firewall | Hetzner Cloud Firewalls + K8s NetworkPolicies | Defense in depth at cloud and application level |
| VPN | WireGuard (Bastion host) | Minimal overhead, modern crypto, audited access |
| DDoS | Cloud edge + LB + WAF | Multi-layer protection, no single point of failure |
| TLS version | TLS 1.3 only | Modern, faster handshake, no deprecated ciphers |

## Integration Points

- **Ch 10 (Zero-Trust)** — Network segmentation enforces micro-perimeters
- **Ch 10 (API Security)** — WAF rules protect API endpoints
- **Ch 05 (Service Mesh)** — mTLS between services in private subnet
- **Ch 08 (DevOps)** — Terraform manages firewall rules as code

## Production Considerations

- **Encryption at Rest**: All data subnet volumes encrypted with AES-256; keys in Vault
- **Encryption in Transit**: TLS 1.3 for external, mTLS for internal — no plaintext traffic
- **Network Monitoring**: Prometheus blackbox_exporter probes all services; alert on connectivity loss
- **Incident Response**: Network partition simulated during chaos engineering drills
- **Compliance**: Network architecture designed for SOC 2, HIPAA readiness (dedicated data subnet, access logging)
