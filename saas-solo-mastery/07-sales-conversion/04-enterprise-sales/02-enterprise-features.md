# Enterprise Features

## The Enterprise Feature Dilemma

Enterprise customers demand features that individual users and small teams don't need. Building these features takes time — time you could spend on your core product. The key is to build the right enterprise features at the right time.

This guide covers the most commonly requested enterprise features, how to prioritize them, and how to build them efficiently as a solo founder.

## Feature Prioritization Framework

### Enterprise Feature Categories

**Table Stakes (must-have for any enterprise deal):**
- Single Sign-On (SSO / SAML)
- Role-based access control (RBAC)
- Audit logs
- Data export
- Uptime SLA

**Differentiators (nice-to-have, can close deals):**
- SOC 2 compliance
- Data residency
- Advanced permissions
- SCIM provisioning
- Custom terms and contracts

**Aspirational (enterprise wants, but you can defer):**
- On-premise deployment
- Dedicated infrastructure
- Enterprise SSO (beyond SAML — OIDC, LDAP)
- Advanced compliance (HIPAA, FedRAMP)
- Multi-region active-active deployments

### Build Decision Framework

When deciding whether to build an enterprise feature, ask:

1. **How many enterprise deals are blocked by this feature?**
   - If 3+ deals worth $10k+ each are waiting, build it
   - If one deal is waiting, offer a workaround or custom solution

2. **Does this feature benefit all customers or just enterprise?**
   - If it benefits everyone (e.g., better permissions), prioritize
   - If it only benefits enterprise, consider billing a setup fee

3. **How long will it take to build?**
   - Under 40 hours: Consider building
   - 40-100 hours: Only if multiple deals depend on it
   - 100+ hours: Hire a contractor or raise prices to fund it

4. **Can you achieve the same outcome without the feature?**
   - Workaround exists: "We currently handle this through [process]"
   - No workaround: Feature becomes higher priority

## Single Sign-On (SSO)

### Why Enterprise Needs SSO

- Centralized user management
- Passwordless authentication
- Compliance requirements (user lifecycle management)
- Reduced IT support burden

### SSO Options

**Option 1: SAML 2.0 (Most Common Enterprise Requirement)**
- Industry standard for B2B SSO
- Supported by Okta, Azure AD, OneLogin, Google Workspace
- Requires: Identity Provider (IdP) configuration + Service Provider (SP) setup

**Option 2: OIDC / OAuth 2.0 (Modern Alternative)**
- Used by Google, Auth0, Microsoft
- Simpler than SAML for developers
- Growing adoption but SAML is still dominant in enterprise

**Option 3: Just-in-Time (JIT) Provisioning**
- Creates user accounts on first SSO login
- Eliminates need for user import
- Combine with SCIM for full lifecycle management

### Building SSO as a Solo Founder

**Don't build SSO yourself. Use a provider.**

**Provider options:**

**Auth0 ($0-300/mo for SSO):**
- Full SSO support (SAML, OIDC, social)
- Built-in user management
- Can handle SCIM provisioning
- Free tier covers basic SSO

**WorkOS ($0-500/mo):**
- Purpose-built for B2B SSO
- Handles SAML, OIDC, SCIM
- Directory sync with Okta, Azure AD
- Free for first 10 domains
- This is likely your best option as a solo founder

**Clerk ($0-95/mo):**
- Good for Next.js apps
- Supports SAML, OIDC
- Simple integration

**DIY (not recommended for solo founders):**
- Implementing SAML from scratch: 80-120 hours
- Maintaining it: Ongoing
- If you must, use passport-saml or samlify library

### SSO Setup Flow (WorkOS Example)

1. Add WorkOS SDK to your app (1-2 days)
2. Configure SAML connection in dashboard (30 min)
3. Enterprise customer configures their IdP (they do this)
4. Test the connection together (30 min call)
5. Done

**Total time investment:** 2-3 days initial setup, then 30 min per customer.

### SSO Pricing for Enterprise

- Include SSO in your "Enterprise" tier only (not lower tiers)
- This creates a reason to upgrade to Enterprise
- Some charge a flat $500/mo for SSO access
- WorkOS charges per active domain connection

## Audit Logs

### Why Enterprise Needs Audit Logs

- Compliance requirements (SOC 2, HIPAA, SOX)
- Security incident investigation
- User activity monitoring
- IT governance

### Minimum Viable Audit Log

At minimum, log these events:

**Authentication events:**
- User login (success/failure)
- User logout
- Password change
- SSO login

**Data events:**
- Create, read, update, delete on core entities
- Data export
- Data import
- Configuration changes

**Admin events:**
- User role changes
- Permission changes
- Team member add/remove
- Billing changes

**Security events:**
- API key creation/revocation
- MFA change
- IP address changes
- Suspicious activity flags

### Audit Log Data Structure

```json
{
  "id": "evt_12345",
  "timestamp": "2026-07-29T10:30:00Z",
  "actor": {
    "id": "user_789",
    "email": "admin@company.com",
    "name": "Jane Smith"
  },
  "action": "project.deleted",
  "target": {
    "id": "proj_456",
    "type": "project",
    "name": "Q3 Marketing Campaign"
  },
  "context": {
    "ip_address": "203.0.113.42",
    "user_agent": "Mozilla/5.0...",
    "location": "San Francisco, CA"
  },
  "metadata": {
    "reason": "Project completed",
    "team_id": "team_101"
  }
}
```

### Building Audit Logs

**Store in:**
- Your main database (simple, works for early stage)
- Separate database (better isolation, used at scale)
- Log service (LogDNA, Datadog, Splunk) — enterprise wants integration here

**Retention:**
- Minimum: 90 days
- Standard: 1 year
- Enterprise request: 3-7 years

**Export:**
- CSV download (in-app)
- API access (programmatic retrieval)
- Webhook streaming (real-time to their SIEM)

### Audit Log UI

For enterprise customers, provide:
- Searchable log viewer in app
- Filters by date, action, actor, target
- Export button
- Event details modal
- PDF report generation

### Building Audit Logs Efficiently

**Phase 1 (MVP):**
- Log to database table
- Simple admin view with search
- CSV export
- Time: 20-40 hours

**Phase 2 (Enterprise-ready):**
- Structured events with schema
- Retention policies
- API access for SIEM integration
- Time: Additional 20-40 hours

## Role-Based Access Control (RBAC)

### Why Enterprise Needs RBAC

- Principle of least privilege
- Compliance with access control requirements
- Segregation of duties
- Multi-department usage of same account

### RBAC Levels

**Level 1: Owner / Admin / Member (simple, 3-5 roles)**
- Owner: Full access, billing, team management
- Admin: Full access except billing
- Member: Limited to their own work
- Viewer: Read-only access

**Level 2: Custom Roles (best for most B2B enterprise)**
- Admin-created roles with configurable permissions
- Granular: Can view reports, can edit projects, can delete data
- Good for businesses with established IT governance

**Level 3: Hierarchical RBAC (complex, rare)**
- Organization → Teams → Projects → Documents
- Each level has its own permission set
- Enterprise-grade, but complex to build

### Building RBAC

**Data model:**
```
Roles table: id, name, description, permissions (JSON), created_at
UserRoles table: id, user_id, role_id, scope_id, scope_type, created_at
Permissions: can_create_project, can_delete_report, can_manage_team, etc.
```

**Provide defaults:**
- Pre-define Admin, Member, Viewer roles
- Allow admins to create custom roles (for Level 2)
- Document permissions clearly for each role

**Implement in middleware:**
```javascript
// Check permission middleware
function requirePermission(permission) {
  return (req, res, next) => {
    const userRole = getUserRole(req.user.id, req.params.teamId);
    if (!userRole.permissions.includes(permission)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}
```

## SLA Commitments

### What Enterprise SLAs Cover

**Uptime / Availability:**
- Standard: 99.5% uptime (monthly)
- Good: 99.9% uptime
- Enterprise: 99.95%-99.99%

**Support response times:**
- Critical: 1-4 hours
- High: 4-8 hours
- Normal: 8-24 hours
- Low: 24-48 hours

**Support hours:**
- Standard: Business hours (9-5 ET)
- Enterprise: 24/5 or 24/7

### Structuring Your SLA

| Tier | Uptime | Critical Response | Normal Response | Support Hours |
|------|--------|-------------------|-----------------|---------------|
| Free | None | Best effort | Best effort | Email only |
| Pro | 99.5% | 4 hours | 24 hours | Business hours |
| Business | 99.9% | 2 hours | 12 hours | Extended hours |
| Enterprise | 99.95% | 1 hour | 8 hours | 24/7 |

### SLA Credits

Standard structure:
- < 99.9% but > 99.5%: 5% credit
- < 99.5% but > 99.0%: 10% credit
- < 99.0%: 25% credit
- Maximum credit: 100% of monthly fee

### Measuring Uptime

Use a third-party monitoring service:
- Better Uptime
- Pingdom
- Statuspage
- Checkly

Provide a public status page for transparency.

### As a Solo Founder, Be Realistic

"Enterprise SLA of 99.95% is effectively < 4.5 hours downtime per year. This requires redundant infrastructure across multiple regions. I can offer 99.5% today with 99.9% as a target. Here's my infrastructure architecture..."

Don't commit to SLAs you can't meet. Start with 99.5% and improve over time.

## Data Residency

### Why Enterprise Needs Data Residency

- GDPR (data must stay in EU)
- Industry regulations (finance, healthcare, government)
- Company policy (data cannot leave certain countries)
- Latency requirements

### Data Residency Options

**Option 1: Single region (simple, start here)**
- All data in one region (US, EU, or APAC)
- Customer chooses at account level
- No cross-region replication

**Option 2: Region selection (common enterprise requirement)**
- Customer selects region during onboarding
- Data stays in that region
- Supports 2-4 regions

**Option 3: Multi-region (complex, rarely needed)**
- Active-active across multiple regions
- Data replicated between regions
- Disaster recovery use case

### Data Residency Implementation

**As a solo founder, use your cloud provider's regions:**

"Data residency is handled through our cloud infrastructure. We use AWS/Azure/GCP and can deploy to [US-EAST-1, EU-WEST-1, AP-SOUTHEAST-1]. Your data never leaves the selected region. We configure region at the account level during setup."

**Setup per new region:**
1. Deploy infrastructure in new region (using Terraform or similar)
2. Configure database in that region
3. Update DNS routing
4. Configure backups in-region

**Time investment:** 1-2 days per new region after the first region is automated.

**Cost:** Each new region doubles some infrastructure costs.

### Data Residency Pricing

- Upgrade requirement: Usually requires Business or Enterprise plan
- Justification: Infrastructure cost for multiple regions

## SCIM Provisioning

### What Is SCIM?

System for Cross-domain Identity Management (SCIM) is a standard for automating user provisioning and de-provisioning.

**What SCIM enables:**
- When IT adds a user in Okta/Azure AD, they're automatically created in your app
- When IT removes a user in their IdP, they're automatically deactivated in your app
- Keeps user directories in sync without manual work

### Building SCIM

**Use WorkOS:**
WorkOS handles SCIM provisioning out of the box. You create users/groups via WorkOS API, and WorkOS syncs with the enterprise IdP.

Or build it yourself:

**SCIM endpoints to implement:**

```
POST /scim/v2/Users — Create user
GET /scim/v2/Users — List users
GET /scim/v2/Users/:id — Get user
PUT /scim/v2/Users/:id — Update user
PATCH /scim/v2/Users/:id — Partial update
DELETE /scim/v2/Users/:id — Delete user

POST /scim/v2/Groups — Create group
GET /scim/v2/Groups — List groups
etc.
```

**Implementation time with WorkOS:** 2-3 days
**Implementation time from scratch:** 40-80 hours

## Advanced Permissions / Granular Access Control

### Beyond RBAC: Permission Levels

**Object-level permissions:**
- User A can view Project X but not Project Y
- User B can edit Documents in Project Z

**Feature-level permissions:**
- Admin can export data, Member cannot
- Manager can delete documents, Contributor cannot

**Time-based permissions:**
- Temporary access grants
- Access expires after [time]

### Building Advanced Permissions

Start with simple RBAC and evolve. Most enterprises start with simple needs.

**Evolution path:**
1. Simple roles (Owner, Admin, Member) — 1 week
2. Custom role creation — 2 weeks
3. Object-level permissions — 4 weeks
4. Time-based access — 2 weeks

**Only build what customers specifically request.** Don't build Level 4 until a paying customer asks for it.

## Compliance Certifications

### SOC 2

**What is SOC 2?**
Audit report certifying that a service organization has controls in place for:
- Security (mandatory)
- Availability (optional)
- Confidentiality (optional)
- Processing Integrity (optional)
- Privacy (optional)

**Do you need SOC 2?**
- Mid-market and above often require it
- Can close deals without it if you're transparent
- Becomes table stakes above $5M ARR

**Getting SOC 2 as a solo founder:**
- Use compliance automation (Vanta, Drata, Secureframe)
- Costs: $500-1,000/month for tooling + $5,000-10,000 for audit
- Time: 3-6 months to prepare
- Focus on Security + Confidentiality (most common)

**Until you have SOC 2:**
- Document your security practices thoroughly
- Provide your cloud provider's SOC 2 report
- Offer a security call with you (the founder) as the engineer

### GDPR Compliance

**Requirements:**
- Data Processing Agreement (DPA)
- Data inventory and mapping
- User data access and deletion requests
- Breach notification process
- Privacy policy and cookie consent

**Implementation:**
- DPA template (get from OneTrust or law firm)
- Self-serve data export/deletion in product (GDPR Right of Access)
- Document processing activities

### HIPAA Compliance

Only build if you're selling to healthcare. Adds significant complexity:
- BAA (Business Associate Agreement) required
- Audit controls
- Access controls
- Data encryption
- Breach notification

**For most B2B SaaS, HIPAA is not needed.**

## Custom Contracts and Terms

### Enterprise Contract Requirements

- **MSA (Master Services Agreement):** Framework contract covering legal terms
- **Order Form:** Specific to each deal (pricing, scope, term)
- **DPA (Data Processing Agreement):** GDPR/privacy terms
- **SLA:** Service level commitments

### Building Contract Templates

**Have a lawyer draft:**
- Standard MSA (favorable to you, but reasonable)
- Standard DPA
- Standard Order Form

**Cost:** $2,000-5,000 for all three templates (one-time investment)

**Then reuse for every deal.** Enterprise legal will mark them up; negotiate from your standard terms.

### Key Terms to Protect

**Limitation of liability:**
"Ideally capped at fees paid in last 12 months. Never uncapped."

**Indemnification:**
"You indemnify them for IP infringement. They indemnify you for data misuse. Mutually."

**Payment terms:**
"Net 30 for annual contracts. Net 15 preferred. No payment, no service."

**Term and termination:**
"Annual with auto-renewal. 30-60 day notice for non-renewal. Termination for breach with 30-day cure period."

## On-Premise / Self-Hosted

### What Enterprise Really Wants

When enterprise asks for on-premise, they usually mean:
- Data stays in their control (security)
- No data leaves their network (compliance)
- Works in air-gapped environment (military/govt)

### Before Building On-Premise

**Offer these alternatives first:**
- Single-tenant cloud deployment (dedicated infrastructure)
- Data residency (choose region)
- Enhanced data retention and export
- SOC 2 report showing your security controls

### If You Must Build On-Premise

- Package as Docker containers
- Use Docker Compose for single-server deployment
- Use Kubernetes for enterprise deployment
- Provide configuration documentation
- Offer installation support calls
- Charge significantly more (5-10x) for on-premise

**Warning:**
On-premise creates long-term support burden. Every customer has a unique environment. You'll debug infrastructure issues for years. Only do this for deals > $50k/year.

## Feature Roadmap Alignment

### Building the Right Features at the Right Time

**Stage 1 (< $100k ARR):**
- Core product only
- Basic user roles (Owner/Member)
- No enterprise features

**Stage 2 ($100k-$500k ARR):**
- SSO (use WorkOS)
- Basic audit logs
- Simple RBAC (3 roles)
- Standard SLA

**Stage 3 ($500k-$2M ARR):**
- SAML + OIDC SSO
- Full audit logs with retention
- Custom roles (RBAC Level 2)
- Data residency (2 regions)
- SOC 2 Type I

**Stage 4 ($2M+ ARR):**
- SCIM provisioning
- Advanced audit (SIEM integration)
- SOC 2 Type II
- Multi-region support
- Enterprise contract templates
- Dedicated support SLA

### Feature Triage for Enterprise Requests

When an enterprise prospect requests a feature:

1. **Is this a deal-breaker?**
   - "If we don't have [feature], you won't buy?" → Yes? Add to critical list
   - No? → Offer workaround

2. **Is there a workaround?**
   - "Here's how current customers handle this without the feature..."
   - "I can configure this manually for your account..."

3. **How many other customers need this?**
   - One customer: Consider custom build (charge for it)
   - Multiple customers: Add to roadmap
   - Many customers: Build for the product

4. **What's the deal size?**
   - < $10k/year: Offer workaround or defer
   - $10k-50k/year: Consider building at standard priority
   - $50k+/year: Build it (bill for it if possible)

## Pitching Enterprise Features

### In Sales Conversations

"We support enterprise-grade security and administration features including SAML-based SSO, role-based access control with custom roles, comprehensive audit logging, and 99.5% uptime SLA with [X] hour support response."

### On Your Pricing Page

Enterprise tier features (own row or section):
- SAML / SSO
- Audit logs
- Custom roles
- Data residency
- SLA
- Dedicated support
- Custom contract

For features you don't have yet, don't list them. List only what you deliver.

### Competitive Positioning

| Feature | Us | Competitor A | Competitor B |
|---------|----|--------------|--------------|
| SSO | ✓ (SAML + OIDC) | ✓ | ✓ |
| Audit logs | ✓ (90-day retention) | ✓ (30-day) | ✓ (1-year) |
| Custom roles | ✓ | Limited | ✓ |
| SOC 2 | ✓ (Type II) | ✓ (Type I) | ✓ |
| Data residency | 3 regions | 2 regions | 1 region |

Emphasize features where you win. Downplay where you're weaker.

## Conclusion

Enterprise features don't have to be a massive undertaking. Start with the highest-impact, lowest-effort features (SSO through WorkOS, simple audit logs, basic RBAC). Add more as enterprise revenue justifies the investment.

The solo founder advantage: you can build exactly what enterprise customers need, without the bloat of a product designed by a committee. Prioritize ruthlessly, use third-party services where possible, and never forget that your core product is why enterprise customers are interested in the first place.
