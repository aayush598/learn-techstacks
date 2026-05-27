# Section 07: Multi-Region Data Migration

Multi-region migration moves tenant data between geographic regions for latency optimization, compliance (data sovereignty), or disaster recovery. The migration copies data asynchronously from source region to target region while the tenant continues operating in the source. Cutover switches traffic to the target region with minimal interruption.

Multi-region replication uses: PostgreSQL streaming replication (logical) for database, S3 cross-region replication (CRR) for object storage, and DNS-based traffic routing (GeoDNS) for API traffic. The replication lag is monitored to ensure the target is sufficiently caught up before cutover.

Cutover process: reduce DNS TTL to 60 seconds (24 hours before), pause writes to source, verify replication lag is zero, update DNS records to point target region, verify health checks passing, re-enable writes. Rollback: if issues detected within observation period, revert DNS to source region.
