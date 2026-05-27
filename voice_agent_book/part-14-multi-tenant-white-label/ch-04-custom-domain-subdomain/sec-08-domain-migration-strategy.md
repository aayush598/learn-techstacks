# Section 08: Domain Migration Strategy

## Overview

Domain migration involves moving a tenant's custom domain from one platform to another, or between different environments within the same platform (e.g., sandbox to production). The migration must be seamless for end users, with zero downtime and no loss of SSL connectivity. A domain migration typically involves changing DNS records to point to the new platform's infrastructure, which requires careful coordination between the old and new environments.

For a voice agent platform, domain migration also includes migrating associated services: WebSocket endpoints for real-time events, SIP endpoints for telephony integration, webhook URLs configured in third-party services, and any hardcoded URLs in the tenant's applications. A comprehensive migration plan accounts for all of these.

The migration process: pre-migration verification (DNS, SSL, service configuration), cutover window (typically DNS TTL + propagation buffer), post-migration verification, and rollback plan. DNS TTL is the critical factor—if the TTL is set to 24 hours, that's how long it takes for all users to see the new IP address.

## Design Decisions

**Decision 1: DNS TTL reduction before migration.** Reduce the TTL on the DNS record to 60 seconds at least 48 hours before the scheduled cutover. This ensures fast propagation when the record changes.

**Decision 2: Staged migration for multi-service domains.** If the domain serves multiple services (web app, API, WebSocket), migrate one service at a time using different subdomains or paths.

**Decision 3: Rollback window of 72 hours.** Keep the old infrastructure running for 72 hours after migration. Monitor for traffic spikes and errors. Only decommission after the rollback window expires.

## Implementation Approach

```typescript
interface DomainMigration {
  tenantId: string;
  domain: string;
  targetEnvironment: string;
  scheduledAt: Date;
  steps: MigrationStep[];
  status: 'planning' | 'preparing' | 'ready' | 'in_progress' | 'completed' | 'rolled_back';
}

class DomainMigrationService {
  async planMigration(tenantId: string, domain: string, targetEnv: string): Promise<DomainMigration> {
    const currentMapping = await this.domainService.getDomainMapping(tenantId, domain);

    // Create migration plan
    const steps: MigrationStep[] = [
      { order: 1, name: 'Reduce DNS TTL', action: 'dns_ttl', duration: '48h before' },
      { order: 2, name: 'Pre-migration validation', action: 'validation', duration: '1h before' },
      { order: 3, name: 'Configure new environment', action: 'provision', duration: '30min before' },
      { order: 4, name: 'Update DNS record', action: 'dns_update', duration: 'cutover time' },
      { order: 5, name: 'Verify SSL certificate', action: 'ssl_verify', duration: '5min after' },
      { order: 6, name: 'Monitor traffic migration', action: 'monitor', duration: '24h after' },
      { order: 7, name: 'Decommission old environment', action: 'cleanup', duration: '72h after' },
    ];

    return {
      tenantId,
      domain,
      targetEnvironment: targetEnv,
      scheduledAt: new Date(),
      steps,
      status: 'planning',
    };
  }

  async executeMigration(migration: DomainMigration): Promise<void> {
    // Step 1: Ensure TTL is low
    await this.setDnsTtl(migration.domain, 60);
    
    // Wait 48 hours (or verify TTL has propagated)
    await this.waitForTtlPropagation(migration.domain);

    // Step 2: Pre-migration validation
    await this.validatePreMigration(migration);

    // Step 3: Configure new environment
    await this.configureTargetEnvironment(migration);

    // Step 4: DNS cutover
    await this.updateDnsRecord(migration.domain, migration.targetEnvironment);

    // Step 5: SSL verification
    await this.waitForSslIssuance(migration.domain);
    const sslValid = await this.verifySsl(migration.domain);
    if (!sslValid) {
      await this.rollbackMigration(migration);
      throw new Error('SSL certificate verification failed after DNS update');
    }

    // Step 6: Monitor for issues
    await this.startMigrationMonitoring(migration);

    // Step 7: Schedule decommission
    await this.scheduleDecommission(migration, 72 * 60 * 60 * 1000);
  }

  private async validatePreMigration(migration: DomainMigration): Promise<void> {
    const checks = [
      this.checkDnsResolution(migration.domain),
      this.checkSslCertificate(migration.domain),
      this.checkBackendConnectivity(migration.tenantId),
      this.checkThirdPartyIntegrations(migration.tenantId),
    ];

    const results = await Promise.all(checks);

    const failed = results.filter(r => !r.success);
    if (failed.length > 0) {
      throw new Error(`Pre-migration validation failed: ${failed.map(f => f.message).join(', ')}`);
    }
  }

  private async rollbackMigration(migration: DomainMigration): Promise<void> {
    // Restore old DNS records
    await this.restoreDnsRecord(migration.domain);
    
    // Wait for DNS propagation
    await this.sleep(300000); // 5 minutes

    // Verify old configuration works
    const verified = await this.verifyDns(migration.domain);
    if (!verified) {
      await this.alertService.send({
        type: 'domain_migration_rollback_failed',
        tenantId: migration.tenantId,
        domain: migration.domain,
        severity: 'critical',
      });
    }

    migration.status = 'rolled_back';
  }
}
```

## Open-Source Tools

- **dnscontrol** — DNS migration automation across providers
- **octoDNS** — Multi-provider DNS management for migrations
- **certbot** — SSL certificate transfer between environments
- **curl + openssl** — Manual verification tools
- **Cloudflare API** — Programmatic DNS management for migration

## Production Considerations

- **Communication Plan:** Notify tenants 2 weeks before scheduled migration, with reminders at 1 week, 2 days, and 1 hour before. Include expected downtime (if any) and what they need to do.
- **DNS TTL Reduction:** Remember to increase the TTL back to a reasonable value (300-3600s) after migration completes. Low TTL forever increases DNS lookup costs.
- **Monitoring During Migration:** Set up real-time dashboard showing traffic distribution between old and new environments. Alert on error rate increases, latency spikes, or traffic drops.
- **Rollback Procedure:** Document and test the rollback procedure before the migration. Rollback should be possible within 5 minutes if issues are detected early.
- **Third-Party Services:** Identify all third-party services (webhooks, integrations) that reference the domain and may need URL updates. This is often the most overlooked aspect of domain migration.
- **SSL Certificate Transfer:** If the old platform has the SSL certificate, ensure it's exported and imported to the new platform. Let's Encrypt certificates can be reissued on the new platform using DNS-01 challenge.
