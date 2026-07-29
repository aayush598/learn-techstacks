# SaaS-Specific Clauses for Terms of Service

## Beyond the Basics

While the previous guide covered standard ToS sections, SaaS businesses have unique characteristics that require additional clauses. This guide covers the SaaS-specific provisions that protect your business, manage customer expectations, and reduce legal risk.

## Uptime SLAs (Service Level Agreements)

### Should You Offer an SLA?

| Stage | Recommendation | Rationale |
|-------|---------------|-----------|
| Pre-revenue / MVP | No SLA | You can't guarantee reliability yet |
| First customers ($0-5k MRR) | Best effort (no contractual SLA) | Manage expectations without liability |
| Growth ($5-20k MRR) | Internal SLA (track, don't promise) | Know your reliability before committing |
| Scale ($20k+ MRR) | Simple SLA (99.5-99.9%) | Enterprise customers may require it |

### What a Good SLA Looks Like

```
Service Level Commitment

1. Uptime Commitment
   We commit to [99.5 / 99.9]% monthly uptime for the core Service.
   
   "Uptime" is defined as the ability to authenticate, access core features,
   and process API requests. Planned maintenance (with 24h notice),
   emergency security patches, and force majeure events are excluded.

2. Exclusions (Downtime that doesn't count)
   → Scheduled maintenance (notified 24h in advance)
   → Emergency maintenance (critical security or stability fixes)
   → Force majeure (AWS outage, DDoS attack, natural disaster)
   → Beta features (not covered by SLA)
   → Customer-caused issues (misconfiguration, exceeding limits)
   → Third-party integrations beyond our control

3. Service Credits (your only remedy)
   | Uptime %       | Credit |
   |----------------|--------|
   | 99.0 - 99.9%  | 5% of monthly fee |
   | 95.0 - 99.0%  | 10% of monthly fee |
   | < 95.0%       | 25% of monthly fee |
   
   Credits cap: Maximum credit is [50%] of the monthly fee in any month.
   Credits are the sole and exclusive remedy for SLA breaches.

4. How to Request Credits
   → Submit request within 7 days of the month end
   → Include dates and times of downtime
   → We will verify and respond within 7 business days
```

### SLA Negotiation for Enterprise Customers

Enterprise buyers often want better SLAs. Common requests and responses:

| Enterprise Request | Your Response |
|-------------------|---------------|
| "We need 99.99% uptime" | "We can discuss this for an Enterprise plan with dedicated infrastructure" |
| "Double the credit percentages" | "We can increase credits in exchange for a longer contract term" |
| "No credit cap" | "We can increase the cap to 100% of monthly fees, but not beyond" |
| "Penalties for SLA breach" | "Service credits are standard. We don't do cash penalties." |
| "SLA for support response time" | "We can commit to different support SLAs for different tiers" |

## Data Ownership and Usage

### Standard Data Ownership Clause

```
Data Ownership

1. Your Data
   You retain all right, title, and interest in and to your data.
   We do not claim any ownership over your data.

2. License to Us
   You grant us a non-exclusive, worldwide, royalty-free license to
   access, use, process, copy, store, and transmit your data solely
   to provide, maintain, and improve the Service.

3. Aggregated/Anonymized Data
   We may use aggregated, de-identified data that does not identify you
   or your end users for analytics, benchmarking, and product improvement.
   This data cannot be reverse-engineered to identify specific users.

4. Data Portability
   During your subscription and for [30] days after termination, you
   may export your data using our built-in export tools. We will provide
   data in a standard format (CSV, JSON).

5. Data Deletion
   [30] days after termination, we will delete your data from our active
   systems. Residual copies may remain in backups for up to [90] days
   before being overwritten. We are not obligated to recover deleted data.

6. Data Processing
   To the extent we process personal data on your behalf, the terms of
   our Data Processing Agreement (DPA) apply and are incorporated by
   reference.
```

### IP Protection for User Content

If your SaaS lets users create content (write, design, code), you need clauses about ownership of what they create and your right to display it:

```
User Content License

1. User Content License to Us
   You grant us a worldwide, non-exclusive, royalty-free license to
   use, reproduce, modify, adapt, publish, and display your User Content
   solely for the purpose of operating and promoting the Service.
   
   Example: If you write a public document, we may feature it in our
   showcase or testimonials.

2. User Content License to Other Users
   If you make User Content publicly available (e.g., via templates,
   integrations), you grant other users a non-exclusive license to use
   that content within the Service.

3. Your Warranties
   You warrant that you own or have the necessary rights to your User
   Content, and that it does not infringe any third-party rights.
```

## Acceptable Use Policy (Detailed)

### General Prohibitions

```
Prohibited Activities

You may not use the Service to:
1. Violate any law, regulation, or government order
2. Infringe any intellectual property or privacy rights
3. Transmit malware, viruses, or any code designed to disrupt the Service
4. Send unsolicited commercial communications (spam)
5. Engage in phishing, fraud, or deceptive practices
6. Harass, abuse, or harm others
7. Impersonate any person or entity
8. Access the Service through unauthorized means (scraping, bots)
9. Interfere with the Service's operation (DDoS, overloading)
10. Reverse engineer, decompile, or disassemble the Service
11. Use the Service for competitive analysis or benchmarking
12. Resell or sublicense the Service (unless on a reseller plan)
```

### Industry-Specific Restrictions

Depending on your SaaS, you may need additional restrictions:

**If you offer a communication/collaboration tool:**
```
  → No sending illegal or obscene content
  → No coordinating criminal activity
  → No distributing child exploitation material (report to NCMEC)
  → No doxxing or sharing private information without consent
```

**If you offer a data/analytics tool:**
```
  → No storing sensitive financial data (PCI) without compliance
  → No storing protected health information (HIPAA) without BAA
  → No processing children's data without parental consent (COPPA)
  → No storing government-classified information
```

**If you offer a developer tool:**
```
  → No using the API to build a competing product
  → No circumventing rate limits or security measures
  → No using the API for unauthorized data collection
```

### Enforcement

```
Enforcement

We reserve the right to investigate and take appropriate action for
violations of this Acceptable Use Policy. Actions may include:

1. Warning the user
2. Removing or disabling access to content
3. Suspending the user's account temporarily
4. Terminating the user's account permanently
5. Reporting to law enforcement or relevant authorities
6. Pursuing legal action for damages

We may modify this AUP at any time with notice.
```

## API Rate Limits and Usage

### Rate Limit Clause

```
API Rate Limits

1. Rate Limits
   We enforce rate limits to ensure fair usage and service stability.
   Current rate limits are documented at [link to docs].
   
   Free plan: [100] requests per minute
   Pro plan: [1000] requests per minute
   Enterprise: Custom limits

2. Rate Limit Headers
   Our API includes standard rate limit headers:
   → X-RateLimit-Limit: requests allowed per window
   → X-RateLimit-Remaining: requests remaining in current window
   → X-RateLimit-Reset: time when the window resets (Unix timestamp)

3. Exceeding Limits
   If you exceed rate limits, we may:
   → Return HTTP 429 (Too Many Requests)
   → Temporarily suspend API access
   → Reduce your rate limit
   → Terminate access for repeated or intentional abuse

4. Fair Use
   We reserve the right to update rate limits at any time with [30] days
   notice. Rate limit changes for abusive behavior may take effect
   immediately.

5. API Deprecation
   We will announce API endpoint deprecations [90] days in advance.
   During this period, the endpoint will remain functional but will not
   receive new features. After the deprecation period, the endpoint may
   be removed.
```

### Usage-Based Pricing Terms

If you use usage-based pricing (not just flat subscriptions):

```
Usage-Based Pricing

1. Units of Usage
   Usage is measured in [requests / storage / API calls / active users /
   documents / compute time].

2. Usage Calculation
   We calculate usage based on our internal measurements. Our records
   are the definitive source for billing calculations.

3. Overage
   If you exceed your plan's included usage, you will be billed for
   overages at the rates specified on our pricing page.
   
   Overage rates: [e.g., $0.01 per additional API call]
   
   We will notify you when you reach [50/75/90/100]% of your included
   usage.

4. Usage Cap
   You may set a usage cap in your account settings to prevent
   unexpected overages. We will suspend service when the cap is reached
   (subject to [X] hour grace period for billing processing).

5. Changes
   We may change usage pricing with [30] days notice. Changes will not
   apply to your current contract term if on an annual plan.
```

## Service Modifications and Discontinuation

### Service Modifications

```
Service Changes

1. Product Evolution
   We continuously improve the Service. This means we may:
   → Add new features and functionality
   → Modify or remove existing features
   → Change the user interface
   → Integrate or deprecate third-party services

2. Notice of Material Changes
   For material changes that negatively affect functionality, we will
   provide [30] days advance notice via email or in-app notification.

3. Beta Features
   We may offer beta or preview features. These are provided "AS IS"
   with no warranty or SLA. We may modify or discontinue beta features
   at any time without notice.
```

### Service Discontinuation

```
Service Discontinuation

1. Right to Discontinue
   We reserve the right to discontinue the Service with [90] days
   advance notice to all active subscribers.

2. Data Export Period
   During the discontinuation notice period, you may export your data.
   After the discontinuation date, the Service will be shut down and
   data will be permanently deleted.

3. Refunds for Prepaid Periods
   If we discontinue the Service, you will receive a prorated refund
   for any prepaid fees covering the period after discontinuation.

4. Acquisition
   In the event of an acquisition, the acquiring company may continue,
   modify, or discontinue the Service per these Terms.
```

**Solo founder note:** As a solo founder, the discontinuation clause is crucial. You need the ability to shut down the service if it's not sustainable. Give yourself 90 days notice (enough for customers to export data, short enough that you're not paying for servers for months after shutting down).

## Support Terms

```
Support

1. Support Channels
   Support is available via:
   → Email: support@[yourdomain].com
   → In-app chat: (during business hours)
   → Knowledge base: [link to KB]

2. Support Hours
   Standard support: [e.g., Monday-Friday, 9 AM - 5 PM ET]
   For critical issues, we respond as soon as possible, including
   weekends and holidays.

3. Response Times
   | Priority | Response Time | Examples |
   |----------|--------------|----------|
   | Critical | < 4 hours | Service down, data loss |
   | High | < 8 hours | Feature broken, major bug |
   | Normal | < 24 hours | Questions, minor issues |
   | Low | < 48 hours | Feature requests, feedback |

4. Response Time Commitment
   Response times are targets, not guarantees, unless specified in
   an Enterprise Support SLA.

5. Self-Service
   We encourage using our knowledge base and community forums for
   faster resolution.
```

## Free Trial and Freemium Terms

```
Free Trial and Freemium

1. Trial Period
   New users may access the Service for a [14/30]-day free trial.
   Trial accounts have access to [full features / limited features].

2. Conversion
   At the end of the trial, you must upgrade to a paid plan to
   continue using the Service. If you don't upgrade, your account
   will be downgraded to the free plan (if available) or suspended.

3. Free Plan (if applicable)
   The free plan includes:
   → [Feature 1] (limited: [limit])
   → [Feature 2] (limited: [limit])
   → Community support only
   
   We may modify or discontinue the free plan at any time with [30]
   days notice.

4. Trial Extensions
   Trial extensions are at our discretion. Contact support to request.

5. Multiple Trials
   Users may not create multiple accounts to obtain multiple trials.
   We reserve the right to reduce or remove trial access for suspected
   abuse.
```

## Non-Disclosure and Confidentiality

If your SaaS involves sharing proprietary information with customers:

```
Confidentiality

1. Definition
   "Confidential Information" includes:
   → Your data (as defined in Section X)
   → Our proprietary technology, algorithms, and business processes
   → Pricing, contracts, and business strategies
   → Any information marked as confidential or that should reasonably
     be considered confidential

2. Exclusions
   Confidential Information does not include:
   → Information that becomes public through no fault of the receiving party
   → Information independently developed without use of confidential information
   → Information rightfully received from a third party without restriction
   → Information required to be disclosed by law

3. Obligations
   Each party agrees to:
   → Use Confidential Information only for purposes of these Terms
   → Not disclose Confidential Information to third parties
   → Protect Confidential Information using reasonable care
   → Limit access to those who need to know

4. Duration
   These confidentiality obligations survive termination for [2] years.
```

## Beta Program Terms

```
Beta Program Agreement

1. Beta Features
   Beta features are pre-release versions offered for testing.
   "Beta" includes alpha, beta, preview, early access, and trial features.

2. No Warranty
   BETA FEATURES ARE PROVIDED "AS IS," WITH ALL FAULTS, AND WITHOUT
   ANY WARRANTY. WE MAY DISCONTINUE BETA FEATURES AT ANY TIME.

3. No SLA
   Beta features are not covered by any SLA or uptime commitment.

4. Feedback
   You grant us the right to use your feedback about beta features
   without compensation or restriction.

5. Confidentiality
   Beta features, their existence, and their functionality may be
   confidential until general availability.

6. Data
   Data created during beta may not be preserved upon general
   availability. We may delete beta data at any time.
```

## Third-Party Links and Integrations

```
Third-Party Services

1. Integrations
   The Service may integrate with third-party services (e.g., Slack,
   Zapier, Salesforce). These integrations are provided as a convenience.

2. No Responsibility
   We are not responsible for:
   → The availability, reliability, or security of third-party services
   → Any data loss or damage caused by third-party services
   → Changes in third-party APIs that affect our integration

3. User Responsibility
   Your use of integrated third-party services is subject to their
   terms of service and privacy policies. You are responsible for
   maintaining your accounts with these services.

4. Third-Party Content
   The Service may contain links to third-party websites or resources.
   We do not endorse and are not responsible for their content.
```

## Non-Solicitation

Protect your team (future employees) from being poached by customers:

```
Non-Solicitation

During the term of this agreement and for [12] months after termination,
you agree not to directly or indirectly solicit, recruit, or hire any
of our employees or contractors with whom you had contact during your
use of the Service.

This does not apply to general job postings not targeted at our personnel.
```

## Independent Development

```
Independent Development

We are continuously developing new features and products. This agreement
does not impair our right to develop, acquire, or market products or
services that may compete with your business or ideas you share with us.

We are not obligated to incorporate your suggestions or feedback into
the Service.
```

## Export Compliance

```
Export Compliance

The Service may be subject to US export control laws and sanctions
programs. You represent that you are:
→ Not located in a US-sanctioned country
→ Not on any US sanctions list (OFAC, Denied Persons List, etc.)
→ Will not use the Service in violation of export laws

You agree to comply with all applicable export and import laws.
```

## Service-Specific Additional Clauses

### Marketplace / Platform SaaS

If your SaaS connects buyers and sellers:
```
  → Seller terms and qualifications
  → Transaction fees and handling
  → Dispute resolution between users
  → Refund and chargeback handling
  → Rating and review policies
```

### Collaboration / Team SaaS

If your SaaS has team/collaboration features:
```
  → Account owner has administrative control
  → Team members must adhere to the same terms
  → Data visibility within the team
  → Transfer of ownership
```

### White-Label / Reseller SaaS

If you offer white-label or reseller options:
```
  → Reseller must maintain confidentiality
  → Reseller is responsible for their end users
  → White-label branding guidelines
  → Minimum order requirements
```

## Jurisdiction-Specific Considerations

### EU/EEA Customers
- GDPR compliance clauses (see DPA guide)
- Consumer rights: EU users have 14-day withdrawal right (with exceptions for digital services)
- Data localization requirements (if applicable)
- Right to data portability (GDPR Article 20)

### UK Customers
- UK GDPR (post-Brexit) compliance
- Consumer Rights Act 2015 protections

### California Customers
- CCPA compliance (see CCPA guide)
- Special arbitration rules for California consumers

### Canada Customers
- PIPEDA compliance
- Quebec-specific privacy requirements (Law 25)

## When to Update Your SaaS Clauses

| Trigger | What to Update |
|---------|---------------|
| Adding new features | Service description, API terms (if applicable) |
| Changing pricing | Payment terms, usage limits |
| Adding enterprise tier | SLA, support terms, data processing |
| Expanding to new country | Jurisdiction-specific clauses, privacy |
| New regulations | GDPR, CCPA, industry-specific laws |
| New integration types | Third-party clauses, data sharing |
| Customer requests certain terms | Negotiate addendum rather than revising ToS |
| You get acquired | Assignment clause, discontinuation |

## Resources

- [Iubenda](https://www.iubenda.com/) — Automated ToS updates for regulatory changes
- [Termly](https://termly.io/) — SaaS-specific ToS generator
- [Avodocs](https://www.avodocs.com/) — Free SaaS ToS templates
- [Stripe Services Agreement](https://stripe.com/legal) — Reference for payment-related terms
- [AWS Service Terms](https://aws.amazon.com/service-terms/) — Reference for infrastructure SLAs
- [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms) — Reference for developer tools
