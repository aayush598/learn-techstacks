# Section 07: Custom Domain Health Checks

## Overview

Custom domain health monitoring ensures that tenant-configured domains remain properly resolved, SSL certificates are valid, and traffic is correctly routed. Proactive health checking detects issues before users report them: DNS resolution failures, expired SSL certificates, misconfigured CNAME records, and backend service unavailability. For enterprise tenants with SLA commitments (Part 14, Ch 09), domain health is a critical component of uptime measurement.

The health check system runs periodic checks against each active custom domain: DNS resolution (does the domain resolve to the expected IP?), SSL certificate validity (is the certificate valid and not expiring soon?), certificate chain completeness (is the full chain present?), HTTP endpoint check (does the domain return a valid response?), and certificate expiry forecasting. Failed checks trigger alerts, automatic remediation attempts, and status page updates.

For a voice agent platform, domain health also includes verifying that any subdomains used for voice services (e.g., `wss.voiceagent.acmecorp.com` for WebSocket connections) are properly configured.

## Design Decisions

**Decision 1: Multi-layer health checking.** Check DNS resolution, SSL validity, and HTTP response as separate layers. A domain can have issues at any layer, and each requires different remediation.

**Decision 2: Proactive certificate renewal monitoring.** Don't wait for the browser to complain. Monitor certificate expiry and trigger renewal at 30 days.

**Decision 3: Tenant-facing health dashboard.** Show domain health status in the tenant's dashboard. Enterprise tenants appreciate transparency into their domain configuration status.

## Implementation Approach

```typescript
interface DomainHealthCheck {
  domainId: string;
  domain: string;
  timestamp: Date;
  status: 'healthy' | 'degraded' | 'down';
  checks: {
    dns: { status: string; resolver: string; ip?: string; latency?: number };
    ssl: { status: string; issuer?: string; expiresAt?: Date; daysRemaining?: number };
    certificate: { status: string; chainComplete?: boolean; ocspStatus?: string };
    http: { status: string; statusCode?: number; responseTime?: number };
  };
  issues: HealthIssue[];
}

class DomainHealthChecker {
  private checkInterval = 5 * 60 * 1000; // 5 minutes

  async runFullCheck(domain: DomainMapping): Promise<DomainHealthCheck> {
    const issues: HealthIssue[] = [];
    
    // 1. DNS Resolution
    const dnsResult = await this.checkDns(domain.domain);
    if (dnsResult.status !== 'ok') {
      issues.push({ type: 'dns', severity: 'critical', message: dnsResult.error! });
    }

    // 2. SSL Certificate
    const sslResult = await this.checkSsl(domain.domain);
    if (sslResult.daysRemaining && sslResult.daysRemaining < 30) {
      issues.push({
        type: 'ssl_expiry',
        severity: sslResult.daysRemaining < 7 ? 'critical' : 'warning',
        message: `SSL certificate expires in ${sslResult.daysRemaining} days`,
      });
    }

    // 3. HTTP Endpoint
    const httpResult = await this.checkHttp(domain.domain);
    if (httpResult.status !== 'ok') {
      issues.push({ type: 'http', severity: 'critical', message: httpResult.error! });
    }

    // 4. Certificate Chain
    const chainResult = await this.checkCertificateChain(domain.domain);
    if (!chainResult.complete) {
      issues.push({ type: 'ssl_chain', severity: 'warning', message: 'Incomplete certificate chain' });
    }

    const status: DomainHealthCheck['status'] = 
      issues.some(i => i.severity === 'critical') ? 'down' :
      issues.length > 0 ? 'degraded' : 'healthy';

    const healthCheck: DomainHealthCheck = {
      domainId: domain.id,
      domain: domain.domain,
      timestamp: new Date(),
      status,
      checks: { dns: dnsResult, ssl: sslResult, certificate: chainResult, http: httpResult },
      issues,
    };

    // Store check result
    await this.storeCheckResult(healthCheck);

    // Alert if issues found
    if (issues.length > 0) {
      await this.handleIssues(domain, healthCheck);
    }

    return healthCheck;
  }

  private async checkDns(domain: string): Promise<CheckResult> {
    try {
      const start = Date.now();
      const addresses = await dns.resolve4(domain);
      const latency = Date.now() - start;
      return { status: 'ok', ip: addresses[0], latency };
    } catch (error) {
      return { status: 'error', error: `DNS resolution failed: ${error.message}` };
    }
  }

  private async checkSsl(domain: string): Promise<SslCheckResult> {
    try {
      const socket = tls.connect(443, domain, { servername: domain, rejectUnauthorized: true });
      return new Promise((resolve) => {
        socket.on('secureConnect', () => {
          const cert = socket.getPeerCertificate();
          const daysRemaining = Math.floor(
            (new Date(cert.valid_to).getTime() - Date.now()) / (1000 * 60 * 60 * 24)
          );
          socket.end();
          resolve({
            status: 'ok',
            issuer: cert.issuer?.O,
            expiresAt: new Date(cert.valid_to),
            daysRemaining,
          });
        });
        socket.on('error', (error) => {
          resolve({ status: 'error', error: `SSL check failed: ${error.message}` });
        });
        setTimeout(() => {
          socket.destroy();
          resolve({ status: 'error', error: 'SSL check timed out' });
        }, 10000);
      });
    } catch (error) {
      return { status: 'error', error: error.message };
    }
  }

  private async checkHttp(domain: string): Promise<CheckResult> {
    try {
      const start = Date.now();
      const response = await fetch(`https://${domain}/health`, { 
        method: 'HEAD',
        timeout: 5000,
      });
      const responseTime = Date.now() - start;
      return { status: 'ok', statusCode: response.status, responseTime };
    } catch (error) {
      return { status: 'error', error: `HTTP check failed: ${error.message}` };
    }
  }

  private async handleIssues(domain: DomainMapping, healthCheck: DomainHealthCheck): Promise<void> {
    // Send alert to tenant
    await this.notificationService.send({
      tenantId: domain.tenant_id,
      type: 'domain_health_issue',
      data: {
        domain: domain.domain,
        issues: healthCheck.issues,
      },
    });

    // Log to audit
    await this.auditService.log('domain.health_issue', {
      domainId: domain.id,
      domain: domain.domain,
      issues: healthCheck.issues,
    });

    // Update domain status if down
    if (healthCheck.status === 'down') {
      await this.domainMappingService.updateDomainStatus(domain.id, 'suspended');
    }
  }

  async startPeriodicChecks(): Promise<void> {
    setInterval(async () => {
      const activeDomains = await this.getActiveDomains();
      
      // Process in batches to avoid overwhelming DNS resolvers
      for (const batch of this.chunk(activeDomains, 10)) {
        await Promise.all(batch.map(d => this.runFullCheck(d)));
      }
    }, this.checkInterval);
  }
}
```

## Open-Source Tools

- **Node.js dns module** — DNS resolution for health checks
- **Node.js tls module** — SSL/TLS certificate inspection
- **UptimeRobot / Better Uptime** — External domain monitoring services
- **Prometheus Blackbox Exporter** — Infrastructure-level domain health monitoring
- **Grafana** — Domain health dashboards

## Production Considerations

- **Check Distribution:** Stagger health checks across the interval to avoid a thundering herd at check time. Randomize the offset for each domain.
- **False Positive Prevention:** A single failed check should not trigger alerts. Require 3 consecutive failures before alerting. Use circuit breaker pattern for check execution.
- **DNS Resolver Redundancy:** Use multiple upstream DNS resolvers. A single resolver outage should not cause false domain-down alerts.
- **Monitoring External Dependencies:** If a domain's DNS resolves correctly but the SSL certificate is valid for the wrong domain, that's a configuration error the tenant must fix.
- **Check Origin Diversity:** Run health checks from multiple geographic locations. A domain might be reachable from us-east-1 but not from eu-west-1.
