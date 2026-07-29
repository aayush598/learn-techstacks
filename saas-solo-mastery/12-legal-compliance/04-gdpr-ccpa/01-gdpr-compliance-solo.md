# GDPR Compliance for Solo Founders

## Understanding GDPR for Your SaaS

The General Data Protection Regulation (GDPR) is the EU's data protection law. Despite being an EU regulation, it affects ANY SaaS business that serves users in the EU — regardless of where you're based.

**Key insight:** GDPR compliance does not require a lawyer, a Data Protection Officer, or a million-dollar compliance budget. What it requires is awareness, documentation, and good data hygiene.

### Does GDPR Apply to You?

GDPR applies if you:

1. **Offer goods or services to individuals in the EU** — even if free (e.g., a free trial available in EU countries)
2. **Monitor the behavior of individuals in the EU** — e.g., tracking, analytics, cookies

**There is no revenue threshold.** A free SaaS tool used by 10 EU residents is subject to GDPR.

**Territorial scope (Article 3):**
- You don't need an office in the EU
- You don't need to charge EU users
- Using EU-issued credit cards or EU domain names (.eu) suggests targeting the EU
- Having the service available in EU languages or currencies suggests targeting

### Penalties

| Violation | Maximum Fine | Examples |
|-----------|-------------|----------|
| Less severe | €10M or 2% of global revenue | Failure to maintain records, not notifying breach |
| Severe | €20M or 4% of global revenue | Processing without legal basis, violating data subject rights |
| **For a solo founder with $100k revenue** | **Max €10-20M (unlikely)** | Realistic fine: €500-€50,000 for first offense |

**Reality check for solo founders:** The ICO (UK) and DPC (Ireland) typically issue warnings and corrective orders for first-time small business offenders. Fines are reserved for willful, systematic violations. But don't gamble — compliance is achievable with moderate effort.

## Step-by-Step GDPR Compliance

### Step 1: Data Mapping

Know what personal data you collect, where it comes from, where it goes, and how long you keep it.

**Create a data inventory:**

```markdown
Data Inventory for [Product Name]

1. Account Registration Data
  → What: Name, email, company, password (hashed)
  → Source: User during signup
  → Where stored: PostgreSQL on AWS (us-east-1)
  → Retention: Until account deletion + 30 days
  - Purpose: Service delivery

2. Payment Data
  → What: Payment method, billing address, transaction history
  → Source: User during payment
  → Where stored: Stripe (not on our servers)
  → Retention: Stripe retains per their policy
  → Purpose: Payment processing

3. Product Usage Data
  → What: Feature usage, page views, session recordings
  → Source: Automatic (PostHog analytics)
  → Where stored: PostHog cloud (US)
  → Retention: 12 months
  → Purpose: Product improvement

4. Support Data
  → What: Support tickets, email correspondence
  → Source: User contacting support
  → Where stored: Help Scout (US)
  → Retention: 3 years after resolution
  → Purpose: Customer support

5. Email Communications
  → What: Opens, clicks, unsubscribes
  → Source: Automatic (SendGrid)
  → Where stored: SendGrid (US)
  → Retention: Until unsubscribe
  - Purpose: Product communication, marketing

6. Cookies
  → What: Session cookies, analytics cookies
  → Source: Browser
  → Where stored: User's browser
  → Retention: Session to 2 years depending on cookie type
  → Purpose: Authentication, analytics
```

**Data flow diagram (text version):**

```
User → Signup → [Your App] → Stripe (payment)
                           → AWS RDS (user data)
                           → PostHog (analytics)
                           → SendGrid (email)

User → Support → [Help Scout]

[Your App] → User dashboard (shows their data)
```

### Step 2: Establish a Legal Basis for Processing

GDPR requires a legal basis for each processing activity. The most common for SaaS:

| Legal Basis | When to Use | Example |
|-------------|-------------|---------|
| **Consent** | When no other basis fits; must be freely given, specific, informed, unambiguous | Marketing emails, non-essential cookies |
| **Contractual necessity** | Processing necessary to fulfill your contract with the user | Account creation, payment processing, service delivery |
| **Legitimate interest** | Processing that is necessary for your legitimate business interests, balanced against user rights | Product analytics, fraud prevention, security |
| **Legal obligation** | Processing required by law | Tax records, legal compliance |

**For a typical SaaS:**

```
Processing Activity              → Legal Basis
Account creation and management  → Contractual necessity
Payment processing               → Contractual necessity
Product analytics                → Legitimate interest (with opt-out)
Marketing emails                → Consent
Essential cookies                → Legitimate interest
Non-essential cookies            → Consent
Support communications           → Contractual necessity
Security monitoring              → Legitimate interest
```

### Step 3: Update Your Privacy Policy

Your Privacy Policy must include specific GDPR-required information:

```
Required GDPR Privacy Policy Information:

1. Identity and contact details of the controller (you)
2. Contact details of DPO (if you have one — most solo founders don't)
3. Purposes and legal basis for each processing activity
4. Legitimate interests pursued (if relying on legitimate interest)
5. Recipients or categories of recipients (list all third parties)
6. International transfer safeguards (SCCs, adequacy decisions)
7. Data retention period or criteria
8. Existence of each data subject right
9. Right to withdraw consent (if processing based on consent)
10. Right to lodge complaint with supervisory authority
11. Whether providing data is a contractual requirement
12. Existence of automated decision-making (if applicable)
13. Source of data (if not collected from the data subject)
```

**Add to your Privacy Policy:**

```
Your Rights Under GDPR

If you are in the European Economic Area (EEA) or United Kingdom, you
have the following rights under the General Data Protection Regulation:

Right to Access: You can request a copy of the personal data we hold
about you.

Right to Rectification: You can ask us to correct inaccurate or
incomplete data.

Right to Erasure ("Right to be Forgotten"): You can ask us to delete
your personal data, subject to legal obligations.

Right to Restrict Processing: You can ask us to limit how we use
your data.

Right to Data Portability: You can request your data in a machine-readable
format (CSV, JSON) to transfer to another service.

Right to Object: You can object to processing based on legitimate
interests or for direct marketing.

Right to Withdraw Consent: If processing is based on consent, you
may withdraw at any time without affecting the lawfulness of prior
processing.

To exercise any of these rights, contact privacy@[yourdomain].com.
We will respond within 30 days.

You also have the right to lodge a complaint with your local data
protection authority. Contact details: [link to EDPB list]
```

### Step 4: Implement Data Subject Access Request (DSAR) Process

You must respond to data subject requests within 30 days (one month).

**DSAR workflow for solo founders:**

```
1. User submits request to privacy@[yourdomain].com
   → You have 30 days to respond
   → If complex, you can extend by 60 days (notify user)

2. Verify identity:
   → Ask for account email
   → Send verification email to that address
   → Only process if identity is confirmed

3. Fulfill the request:
   → Access: Extract all user data from your systems
   → Deletion: Delete account (with 30-day grace for backup)
   → Portability: Export data to CSV/JSON
   → Rectification: Update the data they want changed
   → Restriction: Flag account as restricted (no processing beyond storage)

4. Track the request:
   → Log the request date and type
   → Log your response date
   → Document what actions were taken
   → Store records for compliance
```

**Quick reference for common requests:**

| Request Type | Action | Time Required |
|-------------|--------|--------------|
| Access (right to know) | Export user data from all systems | 1-2 hours |
| Deletion (right to be forgotten) | Delete account + notify sub-processors | 30 min - 1 hour |
| Portability | Export to CSV/JSON | 30 min |
| Rectification | Update specific data fields | 15 min |
| Object to marketing | Unsubscribe + add to suppression list | 5 min |
| Restrict processing | Flag account | 15 min |

### Step 5: Get a Data Processing Agreement (DPA)

Your customers (controllers) need a DPA with you (processor). See the DPA guide for details.

### Step 6: Manage Consent

**Consent requirements:**
- Freely given (not bundled with acceptance of ToS)
- Specific (separate consent for different purposes)
- Informed (clear what they're consenting to)
- Unambiguous (affirmative action, not pre-ticked boxes)
- Withdrawable (as easy to withdraw as to give)

**Where you need consent:**
- Marketing emails
- Non-essential cookies (analytics, tracking)
- Data processing not covered by contract or legitimate interest

**Consent management for solo founders:**

```markdown
Consent Record
  → Date consent given
  → What they consented to
  → How they consented (clicked button, checked box)
  → Link to consent mechanism
  → When/if consent was withdrawn
```

**Tools for consent management:**
- **Cookiebot** — Free for small sites, auto-scans cookies
- **Osano** — Consent management platform
- **Fireshark** — Open source consent manager
- **Built-in** — Simple checkbox on signup form

### Step 7: Handle Data Breaches

**When to notify:**
- GDPR requires notification to supervisory authority within 72 hours
- Notification to affected individuals "without undue delay" if high risk

**What qualifies as a breach:**
- Unauthorized access to personal data
- Accidental deletion or loss of personal data
- Disclosure of personal data to unauthorized recipients
- Ransomware attack (if personal data is encrypted)

**Breach notification template (to authority):**

```
To: [Supervisory Authority]
Date: [Date of notification]
Reference: [Your internal reference]

1. Description of the breach:
   [What happened, when, how discovered]

2. Categories and approximate number of data subjects affected:
   [Number and type]

3. Categories and approximate number of personal data records affected:
   [Number and type of data]

4. Contact person:
   [Name, email, phone]

5. Likely consequences:
   [Risk assessment — what harm could come to data subjects]

6. Measures taken or proposed:
   [Steps to address the breach and mitigate harm]

7. Documentation:
   [Attached: incident report, timeline, evidence]
```

**Breach notification template (to individuals):**

```
Subject: Data Security Incident — [Reference]

Dear [Name],

We are writing to inform you of a data security incident involving your
personal data. We take your privacy seriously and sincerely apologize.

What happened:
[Brief, clear description of the breach]

What data was involved:
[List of data categories that were accessed or compromised]

What we have done:
[Steps taken to contain and address the breach]

What you should do:
[Recommended actions: change passwords, monitor accounts, etc.]

Contact:
[Contact information for questions]

We will provide updates as we learn more.
```

**For solo founders — breach response checklist:**

```
Immediate (within 24 hours):
  ☐ Identify the breach — what happened, when, what data
  ☐ Contain the breach — patch vulnerability, revoke access
  ☐ Preserve evidence — logs, screenshots, error reports

Within 48 hours:
  ☐ Assess risk — what harm could come to data subjects
  ☐ Determine if notification is required
  ☐ Notify DPA (if required) within 72 hours

Within 7 days:
  ☐ Notify affected individuals (if required)
  ☐ Document everything — incident report
  ☐ Implement changes to prevent recurrence

Within 30 days:
  ☐ Complete incident report and post-mortem
  ☐ Update security measures
  ☐ Update incident response plan
```

### Step 8: Appoint a Representative (if outside EU/UK)

If you're outside the EU/UK and process EU/UK data, you must appoint a representative in the EU/UK.

**Requirements:**
- Must be established in an EU member state where you offer services
- Must be named in your Privacy Policy
- Can be a service (many companies offer GDPR representation)

**Representation services:**
| Service | Cost | Best For |
|---------|------|----------|
| **DataRep** | €500-2000/year | EU + UK representation |
| **DPO Centre** | £500-3000/year | UK representation |
| **Prighter** | €490/year | GDPR representation |

**Are you exempt?** If you process data occasionally and at low volume (not on a "large scale"), you may not need a representative. Most solo SaaS founders process data as part of their core business, so this exemption rarely applies.

### Step 9: Records of Processing Activities (ROPA)

If you have 250+ employees, you must maintain a ROPA. Under 250 employees, you're exempt UNLESS you process:
- Special categories of data (health, biometrics, etc.)
- Criminal conviction data
- Data likely to result in risk to individuals' rights

**Even if exempt, maintain a ROPA anyway.** It's good practice and helps with data mapping.

**Simple ROPA template:**

```markdown
Records of Processing Activities

Activity 1: User Account Management
  Purpose: Create and manage user accounts
  Legal basis: Contractual necessity
  Data categories: Name, email, password (hashed)
  Data subjects: Users
  Recipients: AWS (hosting)
  Retention: Account duration + 30 days
  Security: Encryption at rest and in transit

Activity 2: Payment Processing
  Purpose: Process subscription payments
  Legal basis: Contractual necessity
  Data categories: Payment card info (via Stripe)
  Data subjects: Paying users
  Recipients: Stripe
  Retention: As per Stripe's policy
  Security: PCI DSS (handled by Stripe)

Activity 3: Product Analytics
  Purpose: Improve product based on usage
  Legal basis: Legitimate interest
  Data categories: Usage data, page views, interactions
  Data subjects: All users
  Recipients: PostHog
  Retention: 12 months
  Security: Anonymized where possible

Activity 4: Customer Support
  Purpose: Resolve user issues
  Legal basis: Contractual necessity
  Data categories: User data, support correspondence
  Data subjects: Users submitting support requests
  Recipients: Help Scout
  Retention: 3 years
```

### Step 10: Data Protection Impact Assessment (DPIA)

A DPIA is required when processing is "likely to result in high risk" to individuals.

**When you need a DPIA:**
- Systematic profiling of individuals
- Large-scale processing of special categories of data
- Systematic monitoring of publicly accessible areas
- **Most SaaS products do NOT need a DPIA**

**When you don't need one:**
- Standard account management
- Payment processing
- Basic analytics
- Customer support

**If you need a DPIA, keep it simple:**

```markdown
Data Protection Impact Assessment

Project: [Product Name]
Date: [Date]

1. Describe the processing:
   [What data, how it's collected, why it's processed]

2. Necessity and proportionality:
   [Why this processing is necessary for the service]

3. Risk assessment:
   [Identify risks to data subjects' rights and freedoms]

4. Measures to address risks:
   [Security measures, data minimization, retention limits]

5. Conclusion:
   [Processing is/is not high risk after mitigation]
```

## GDPR Compliance Checklist for Solo Founders

### Must-Do (Legal Requirements)

```
☐ Data Mapping — Document what data you collect, where it goes
☐ Legal Basis — Document legal basis for each processing activity
☐ Privacy Policy — Updated with GDPR-required information
☐ Data Subject Rights Process — Can handle access, deletion, portability requests
☐ Data Processing Agreement — DPA in place for your customers
☐ Consent Management — Proper consent for marketing, non-essential cookies
☐ Breach Notification — Process in place to notify within 72 hours
☐ Data Security — Appropriate technical and organizational measures
☐ International Transfers — SCCs or other lawful transfer mechanism
☐ Cookie Compliance — Cookie consent for non-essential cookies
```

### Should-Do (Best Practices)

```
☐ Records of Processing — Maintain ROPA (even if exempt)
☐ Vendor Assessments — Review sub-processors' data practices
☐ Privacy by Design — Consider privacy when building new features
☐ Data Minimization — Only collect what you need
☐ Retention Schedule — Regular data deletion per policy
☐ Employee Training — Understand data protection basics
☐ Incident Response Plan — Documented and tested
☐ Regular Review — Annual GDPR compliance review
```

### Nice-to-Have (For Enterprise/Growth)

```
☐ EU Representative — Appointed if outside EU
☐ DPIA — Completed for high-risk processing
☐ ISO 27001 — Formal security certification
☐ SOC 2 — Formal security certification
☐ DPO — Data Protection Officer appointed
☐ Data mapping software — Automated data discovery
☐ Consent management platform — Osano, Cookiebot
☐ Privacy dashboard — User-facing privacy controls
```

## GDPR Considerations by SaaS Feature

| Feature | GDPR Implication | Action Required |
|---------|-----------------|-----------------|
| User signup/login | Collecting personal data | Privacy notice, legal basis |
| Email notifications | Direct marketing | Consent for marketing, unsubscribe in all |
| Analytics (PostHog/GA) | Tracking user behavior | Cookie consent, opt-out mechanism |
| Session recording | Recording user interactions | Consent (high risk), notice in Privacy Policy |
| Cookie-based auth | Essential cookies | Information in Cookie Policy (no consent needed) |
| Marketing cookies | Non-essential tracking | Opt-in consent required |
| API that processes user data | Data processor obligations | DPA for API customers |
| File uploads/storage | Storing potentially personal data | Data classification, security measures |
| Third-party integrations | Data sharing with sub-processors | List in DPA, notice to users |
| AI/ML processing | Automated decision-making | Article 22 requirements if solely automated |
| Team/collaboration features | Multiple data subjects | Clear who is controller/processor |

## GDPR Tools for Solo Founders

| Tool | Purpose | Cost |
|------|---------|------|
| **Cookiebot** | Cookie consent, cookie scanning | Free for small sites |
| **Osano** | Consent management | Free for basic |
| **Iubenda** | Privacy policy, consent, cookie policy | $10-30/month |
| **Termly** | Privacy policy + GDPR compliance | $14/month |
| **DataRep** | EU/UK representation | €500-2000/year |
| **Prighter** | EU representation | €490/year |
| **Simple Analytics** | Privacy-focused analytics | $10/month (GDPR-compliant out of box) |
| **Plausible** | Privacy-focused analytics | €9/month (no cookies needed) |
| **PostHog** (self-hosted) | Analytics without data leaving your server | Free (self-hosted) |

## Common GDPR Myths

| Myth | Reality |
|------|---------|
| "GDPR doesn't apply to US companies" | It applies if you serve EU residents |
| "I need a DPO" | Most solo founders don't — only if large-scale processing of special data |
| "I need consent for everything" | Most processing can use contract or legitimate interest |
| "I need ISO 27001" | Not required, but helps with enterprise sales |
| "I need to store data in the EU" | No, but you need transfer safeguards |
| "GDPR fines are always millions" | First offenses for small businesses are usually warnings or modest fines |
| "I need a lawyer to be compliant" | You can achieve basic compliance yourself with the right tools |
| "GDPR means no tracking at all" | It means proper disclosure and consent/opt-out |

## Resources

- [GDPR.eu](https://gdpr.eu/) — Practical GDPR guide for small businesses
- [UK ICO Guide to GDPR](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- [European Data Protection Board](https://edpb.europa.eu/) — Official guidance
- [CNIL GDPR Guide](https://www.cnil.fr/en/professionals) — French DPA's practical guides
- [Data Protection Commissioner (Ireland)](https://www.dataprotection.ie/) — Major EU DPA
- [Cookiebot](https://www.cookiebot.com/) — Cookie consent
- [PostHog GDPR Guide](https://posthog.com/docs/privacy) — GDPR-compliant product analytics
- [Simple Analytics](https://simpleanalytics.com/) — Privacy-first analytics
