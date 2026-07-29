# CCPA/CPRA Compliance for Solo SaaS Founders

## What is CCPA/CPRA?

The California Consumer Privacy Act (CCPA) and its amendment, the California Privacy Rights Act (CPRA), give California residents specific rights over their personal information. While it's a California state law, it affects any business that collects data from California residents — regardless of where the business is located.

### Does CCPA Apply to Your SaaS?

CCPA applies if you meet ANY of these thresholds:

1. **$25M+ annual gross revenue** (most solo founders are below this)
2. **Buy, receive, or sell the personal information of 100,000+ California residents/households annually**
3. **Derive 50%+ of annual revenue from selling or sharing personal information**

**Good news for solo founders:** Most solo SaaS founders with under $25M revenue and fewer than 100k CA users are NOT subject to CCPA.

**But you should still aim for compliance because:**
- You may have CA residents using your product (especially B2C)
- Enterprise customers may require CCPA compliance
- It's good privacy practice that aligns with other laws
- The thresholds may change or your business may grow

### CCPA vs CPRA vs GDPR

| Aspect | CCPA | CPRA (2023 amendment) | GDPR |
|--------|------|----------------------|------|
| **Effective** | January 2020 | January 2023 | May 2018 |
| **Scope** | California residents | California residents | EU/EEA residents |
| **Revenue threshold** | $25M+ | $25M+ | None |
| **Data subject threshold** | 100k+ consumers | 100k+ consumers | Any |
| **Rights** | Right to know, delete, opt-out | Adds: correction, opt-out of automated profiling | More comprehensive rights |
| **Enforcement** | California AG + private right of action | CPRA Agency (new enforcement body) | DPA in each member state |
| **Penalties** | $2,500-$7,500 per violation | $2,500-$7,500 per violation | €10M-€20M or 2-4% revenue |
| **Sensitive data** | Not defined | New category with opt-out | Special categories |

## CCPA Rights for Consumers

### Right to Know (Access)

Consumers can request:
- Categories of personal information collected
- Categories of sources
- Business purpose for collection
- Categories of third parties shared with
- Specific pieces of personal information collected

### Right to Delete

Consumers can request deletion of their personal information, with exceptions:
- Complete transaction
- Detect security incidents
- Debug/debug errors
- Exercise free speech
- Comply with legal obligations
- Internal use consistent with context

### Right to Opt-Out of Sale/Sharing

Consumers can opt out of the "sale" or "sharing" of their personal information.

**Important:** "Sale" is defined broadly — it includes sharing data for monetary OR other valuable consideration. "Sharing" includes cross-context behavioral advertising.

**Most SaaS businesses don't sell data.** If you don't sell or share data, you don't need a "Do Not Sell My Personal Information" link. But you should still document that you don't sell data.

### Right to Correct

Consumers can request correction of inaccurate personal information.

### Right to Limit Use of Sensitive Personal Information

If you collect sensitive data (SSN, precise geolocation, health, etc.), consumers can limit how you use it.

### Right to Non-Discrimination

You cannot discriminate against consumers for exercising their CCPA rights. This means:
- Cannot deny goods or services
- Cannot charge different prices
- Cannot provide different quality

**Exception:** You can charge different prices if the difference is reasonably related to the value of the data.

## CCPA Compliance Steps for Solo Founders

### Step 1: Determine If You're Subject

Calculate:

```
1. Annual gross revenue: $[amount]
   → If > $25M: CCPA applies
   → If < $25M: Check next threshold

2. California users/consumers:
   → Total users: [number]
   → Estimated CA users: [total × 12% (CA ≈ 12% of US population)]
   → If > 100k: CCPA applies

3. Do you sell or share personal data:
   → If > 50% of revenue from data sales: CCPA applies
   → For most SaaS: No (you sell software, not data)
```

**If you're below ALL thresholds:** CCPA doesn't apply, but maintain good practices.

**If you meet ANY threshold:** Full compliance required.

### Step 2: Update Your Privacy Policy

CCPA requires specific disclosures in your Privacy Policy:

```
Required CCPA Disclosures

1. Categories of personal information collected (last 12 months)
   → List each category with examples

2. Categories of sources of personal information
   → Directly from consumer, automatically, from third parties

3. Business or commercial purpose for collection/sale

4. Categories of third parties with whom you share data

5. Specific pieces of personal information collected (upon request)

6. Whether you sell or share personal information
   → If yes: categories sold/shared in last 12 months
   → If no: state "We do not sell your personal information"

7. Consumer rights under CCPA/CPRA

8. Methods for submitting requests (email, web form, toll-free number)

9. Designated Request Methods URL for CA residents

10. Metrics from previous calendar year (if 10M+ requests received annually)

11. Contact information for questions or concerns
```

**Sample CCPA section for Privacy Policy:**

```markdown
California Privacy Rights (CCPA/CPRA)

If you are a California resident, you have the following rights under
the California Consumer Privacy Act (CCPA) and California Privacy Rights
Act (CPRA):

Right to Know:
You may request that we disclose what personal information we collect,
use, disclose, and sell. You may request:
  → Categories of personal information collected
  → Categories of sources
  - Business purpose for collection
  → Categories of third parties with whom we share
  → Specific pieces of personal information

Right to Delete:
You may request deletion of your personal information, subject to
certain exceptions.

Right to Correct:
You may request correction of inaccurate personal information.

Right to Opt-Out:
We do NOT sell your personal information. We do NOT share your personal
information for cross-context behavioral advertising.

Right to Non-Discrimination:
We will not discriminate against you for exercising your CCPA rights.

How to Exercise Your Rights:
Email: privacy@[yourdomain].com
Web: [link to privacy request form]
Response time: We will confirm receipt within 10 days and respond
within 45 days (extendable by another 45 days with notice).

Authorized Agent:
You may designate an authorized agent to submit requests on your behalf.
We will require verification of your identity and the agent's authority.

Contact:
For questions about these rights, contact us at privacy@[yourdomain].com.
```

### Step 3: Create a "Do Not Sell My Personal Information" Link

**If you sell or share personal data:** You must provide a clear "Do Not Sell My Personal Information" link on your website homepage and in your Privacy Policy.

**If you DON'T sell or share personal data:** You don't need the link, but many businesses include a notice stating "We do not sell your personal information."

**Where to place it:**
- Website footer (conspicuous, not buried)
- Privacy Policy
- Cookie consent banner (if you use cookies that constitute "sale" or "sharing")

### Step 4: Implement a CCPA Request Process

**For solo founders, this can be simple:**

```
Request Process:

1. User submits request via:
   → Email: privacy@[yourdomain].com
   → Web form: [yourdomain].com/privacy-request
   → Toll-free number (optional, not required for small businesses)

2. Verify identity:
   → Ask for account email
   → Send verification email
   → Only proceed if verified

3. Acknowledge receipt within 10 days:
   → "We received your [request type] request on [date]"
   → "We will respond within 45 days"

4. Fulfill request within 45 days (extendable to 90 with notice):
   → Right to know: Provide data from your systems
   → Right to delete: Delete and confirm
   → Right to correct: Update the data
   → Right to opt-out: Honor the opt-out

5. Document the request and response for compliance records
```

### Step 5: Update Your Cookie Policy

CCPA/CPRA affects how you manage cookies, especially those used for analytics, advertising, or sharing data with third parties.

**CCPA cookie requirements:**
- Disclose all cookies in your Privacy/Cookie Policy
- Provide opt-out for cookies that constitute "sale" or "sharing"
- If you use Google Analytics, Facebook Pixel, or similar — these may be considered "sharing" under CPRA

**Cookie categories under CCPA:**

| Cookie Type | CCPA Implication | Action |
|-------------|-----------------|--------|
| Essential (auth, security) | Not sale/sharing | No opt-out needed |
| Analytics (PostHog, GA) | May be "sharing" | Provide opt-out |
| Marketing/advertising | Likely "sharing" | Provide opt-out |
| Third-party cookies | Likely "sharing" | Provide opt-out |

**Cookie consent tool recommendations:**
- **Cookiebot** — Free for small sites, auto-detects cookies
- **Osano** — CCPA-compliant consent management
- **Termly** — Cookie consent + CCPA compliance

### Step 6: Update Your Contracts

If you share data with third parties (processors), update your contracts:

```
Contract Updates for CCPA/CPRA:

1. Add CCPA-specific provisions:
   → Third parties cannot sell data shared with them
   → Third parties cannot use data outside of contracted purposes
   → Right to take reasonable steps to ensure compliance

2. Flow-down clauses:
   → Sub-processors must comply with CCPA requirements
   → Notification of any changes in data handling

3. Audit rights:
   → Right to verify third-party compliance
   → Reasonable advance notice
```

### Step 7: Data Mapping (CCPA Version)

Similar to GDPR data mapping, but with CCPA-specific categories.

```
CCPA Data Mapping

Category: Identifiers
  → Collected: Name, email, IP address, account ID
  - Source: User, automatic
  → Purpose: Service delivery, analytics
  → Shared with: Help Scout, PostHog
  → Sold/Shared: No

Category: Commercial Information
  → Collected: Subscription plan, payment history
  → Source: User, Stripe
  → Purpose: Billing, customer management
  → Shared with: Stripe
  → Sold/Shared: No

Category: Internet/Electronic Activity
  → Collected: Browsing history, search history, interactions
  → Source: Automatic (PostHog)
  → Purpose: Product improvement
  → Shared with: PostHog
  → Sold/Shared: No

Category: Geolocation Data
  → Collected: IP-based approximate location
  → Source: Automatic
  → Purpose: Analytics, security
  → Shared with: PostHog
  → Sold/Shared: No

Category: Professional/Employment Information
  → Collected: Company name, job title (if provided)
  → Source: User
  → Purpose: Service delivery
  → Shared with: None
  → Sold/Shared: No
```

### Step 8: Handle Opt-Out Requests

If you sell or share data, you must honor opt-out requests within 15 business days.

**Opt-out process:**
```
1. User clicks "Do Not Sell My Personal Information" link
2. User submits their email/identifier
3. You add to your suppression list (do not sell/sharing list)
4. You propagate the opt-out to third parties (within 90 days)
5. You confirm to the user
6. You do not ask for consent again for 12 months
```

**For sole founders who don't sell data:**
If you truly don't sell or share data, you can simply state this in your Privacy Policy and not build the full opt-out infrastructure. But keep documentation that you've assessed this.

## CPRA-Specific Requirements

The CPRA (effective January 2023) added:

### New Enforcement Agency
- California Privacy Protection Agency (CPPA)
- Dedicated enforcement body (separate from Attorney General)
- More resources for enforcement

### Sensitive Personal Information
- New category with additional protections
- Includes: SSN, precise geolocation, health, race, religion, sexual orientation, citizenship, genetic data, biometric data, union membership
- Right to limit use of sensitive data
- Most SaaS businesses don't collect this data

### Contractual Requirements (for data sharing)
- Contracts with third parties must include:
  - Purpose specification
  - No further processing without notice
  - No cross-context behavioral advertising without consent
  - Certification of compliance

### Automated Decision-Making
- Right to opt-out of automated profiling
- Applies to profiling for employment, housing, lending, insurance
- Most SaaS products don't do this kind of profiling

### Data Minimization and Retention
- Must limit collection to what is "reasonably necessary"
- Must specify retention periods
- Already good practice — align with GDPR

## CCPA Compliance Checklist for Solo Founders

### If You're Below Thresholds (Good Practice)

```
☐ Privacy Policy includes basic CCPA information
☐ You know your user count and CA percentage
☐ Documented: you don't sell or share data
☐ Privacy email established (privacy@[domain])
☐ Basic request process documented
```

### If You're Above Thresholds (Full Compliance)

```
☐ Privacy Policy updated with all CCPA disclosures
☐ Data mapping completed (CCPA categories)
☐ "Do Not Sell/Share My Personal Information" link on homepage
☐ Request process implemented (acknowledge 10 days, respond 45 days)
☐ Verification process for identity
☐ Opt-out process (propagate to third parties within 90 days)
☐ User training on handling requests
☐ Contract updates with third parties
☐ Metrics tracking (if >10M requests/year)
☐ Records of requests maintained
☐ Cookie consent updated for CCPA
☐ Notice at collection (point-of-collection notice)
☐ Sensitive data audit (do you collect any?)
☐ Automated decision-making audit (do you do any?)
```

## CCPA vs Other State Laws

Several other states have passed privacy laws. Here's how they compare:

| State | Law | Effective | Revenue Threshold | Key Differences from CCPA |
|-------|-----|-----------|-------------------|--------------------------|
| **California** | CCPA/CPRA | 2020/2023 | $25M | Original, most comprehensive |
| **Virginia** | CDPA | 2023 | No revenue threshold, 100k+ consumers | More like GDPR, private right of action |
| **Colorado** | CPA | 2023 | $25M+ OR data of 100k+ | Universal opt-out, rulemaking not final |
| **Connecticut** | CTDPA | 2023 | $25M+ AND data of 100k+ OR revenue from data sales | Similar to Virginia |
| **Utah** | UCPA | 2023 | $25M+ | Less comprehensive, no private right of action |
| **Iowa** | ICDPA | 2025 | $25M+ AND data of 100k+ | Similar to Utah |
| **Tennessee** | TIPA | 2025 | $25M+ AND data of 175k+ | Non-profit exemption |
| **Texas** | TDPSA | 2024 | No threshold (all businesses) | Very broad applicability |
| **Oregon** | OCPA | 2024 | $25M+ AND data of 100k+ OR revenue from data sales | |
| **Montana** | MCDPA | 2025 | No threshold | Applies to all businesses |
| **Delaware** | DPDSA | 2025 | No revenue threshold, 35k+ consumers | Low threshold |

**For solo founders:**
- Most state laws don't apply if you're under $25M revenue
- Texas and Montana laws apply regardless of revenue
- Best practice: implement GDPR-level compliance (it exceeds most state requirements)

## Handling CCPA Requests as a Solo Founder

### Request Volume Estimation

```
Users: 5,000
Estimated CA users (12%): 600
Estimated annual CCPA requests (1% of CA users): 6 requests/year
Time per request: 1 hour
Total annual CCPA workload: 6 hours
```

Most solo founders receive fewer than 10 CCPA requests per year. This is manageable as a part-time task.

### Request Response Templates

**Acknowledgment of receipt (within 10 days):**

```
Subject: Your California Privacy Rights Request — [Reference Number]

Dear [Name],

We received your California Consumer Privacy Act (CCPA) request on
[date]. Your request is:

[ ] Request to know what personal information we collect/use/share
[ ] Request to delete your personal information
[ ] Request to correct your personal information

We will verify your identity and respond within 45 days. If we need
additional time, we will notify you.

To verify your identity, please respond with the email address associated
with your account.

Thank you,
[Your Name]
[Company Name]
```

**Verification request:**

```
Subject: Identity Verification Required — CCPA Request [Reference]

Dear [Name],

To process your CCPA [request type] request, we need to verify your
identity. Please provide:

1. The email address associated with your account
2. [Optional: Any additional verification needed]

We will not process your request until identity is verified.

Thank you,
[Your Name]
```

**Response to verification (if unable to verify):**

```
Subject: Unable to Verify Identity — CCPA Request [Reference]

Dear [Name],

Unfortunately, we were unable to verify your identity based on the
information provided. For security reasons, we cannot process your
CCPA request without identity verification.

If you can provide additional identifying information, please reply
to this email.

Thank you for understanding.
[Your Name]
```

**Fulfillment of request:**

```
Subject: Completed — CCPA Request [Reference]

Dear [Name],

We have completed your CCPA [request type] request.

[If right to know: Attached is the personal information we have collected
about you in the last 12 months.]

[If right to delete: We have deleted your personal information from our
systems. Residual copies may remain in backups for up to 90 days before
being overwritten.]

[If right to correct: We have updated your personal information as
requested.]

If you have any questions or concerns, please contact us at
privacy@[yourdomain].com.

Thank you,
[Your Name]
```

## CCPA Tools for Solo Founders

| Tool | Purpose | Cost |
|------|---------|------|
| **Termly** | CCPA compliance + Privacy Policy | $14/month |
| **Iubenda** | CCPA + GDPR privacy policy | $10-30/month |
| **Cookiebot** | Cookie consent (CCPA-compliant) | Free for small sites |
| **Osano** | Consent management + CCPA | Free for basic |
| **DataGrail** | Privacy request management | $600+/month (enterprise) |
| **OneTrust** | Full privacy management | Enterprise pricing |
| **Simple (email + spreadsheet)** | Manual request handling | Free |

## Resources

- [California Privacy Protection Agency](https://cppa.ca.gov/) — Official CPRA guidance
- [California AG CCPA Page](https://oag.ca.gov/privacy/ccpa) — Official CCPA resources
- [CCPA Regulations](https://cppa.ca.gov/regulations/) — Final regulations
- [IAPP CCPA Resource](https://iapp.org/resources/topics/ccpa/) — Professional guidance
- [Termly CCPA Guide](https://termly.io/resources/articles/ccpa/) — Practical compliance guide
- [Osano CCPA Guide](https://www.osano.com/ccpa) — Compliance roadmap
- [Cookiebot CCPA Guide](https://www.cookiebot.com/en/ccpa/) — Cookie compliance
