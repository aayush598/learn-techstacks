# Section 03: Multi-Region Deployment Architecture

Multi-region deployment ensures service availability even if an entire cloud region fails. The platform runs in at least two geographically separate regions with independent infrastructure. Traffic is distributed via DNS-based routing (active-passive or active-active depending on service). Data is replicated asynchronously between regions.

Multi-region setup: primary region (us-east-1) handles all production traffic. Standby region (eu-west-2) maintains warm infrastructure: database read replicas with WAL streaming, application servers ready to scale, cached data from Redis replication, static assets replicated via S3 CRR. Failover switches the standby to active.

Key considerations: database replication lag (target < 1 second RPO), DNS propagation delay (managed via low TTL + traffic management service), session affinity (stateless applications preferred; state stored in multi-region Redis/ElastiCache), and testing (regular failover drills ensure the standby actually works). Cost optimization: standby runs reduced capacity (50% of active) and scales up during failover.
