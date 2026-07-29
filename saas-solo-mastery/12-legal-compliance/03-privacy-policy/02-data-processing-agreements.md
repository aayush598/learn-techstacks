# Data Processing Agreements (DPA) for Solo Founders

## What is a DPA?

A Data Processing Agreement (DPA) is a legally binding contract between you (the "Data Processor" or "Data Controller") and your customers (the "Data Controller") that governs how you process their personal data.

**Solo founder translation:** When a customer signs up for your SaaS and uploads data that includes personal information (names, emails, etc.), they need a contract with you that promises you'll handle that data responsibly and in compliance with GDPR (or similar laws).

### When You Need a DPA

You need a DPA if:
- You have customers in the EU/EEA or UK
- You process personal data of EU/UK residents
- You are a "Data Processor" for your customers
- Your customers have GDPR compliance obligations

**Even if you don't have EU customers yet, have a DPA ready.** Enterprise customers and privacy-conscious companies will require one.

### What Happens Without a DPA

- Your customers are violating GDPR (they must have DPAs with all processors)
- Your customers may be fined for using you without a DPA
- You will lose enterprise deals (procurement requires DPAs)
- You could be liable for GDPR fines up to €20M or 4% of global revenue

## Controller vs Processor

This distinction is critical:

| Role | Definition | Examples |
|------|-----------|---------|
| **Data Controller** | Determines the purposes and means of processing personal data | Your customer (they decide what data to upload) |
| **Data Processor** | Processes personal data on behalf of the controller | You (you store/process the data they upload) |
| **Sub-processor** | Engaged by the processor to help process data | AWS (hosting), Stripe (payments), SendGrid (email) |

**You are the Processor when:**
- A customer creates an account and adds their team members' data
- A customer uses your service to process their customers' data
- A customer stores business data that includes personal information

**You are the Controller when:**
- You collect customer email addresses for your own marketing
- You collect analytics about how customers use your service
- You handle support tickets from your customers

**In practice for SaaS:** You're BOTH a controller (for your own customer data) AND a processor (for the data your customers upload). Your DPA covers the processor role.

## DPA Requirements Under GDPR Article 28

A valid DPA must include:

```
Required DPA Clauses (GDPR Article 28):

1. Subject matter and duration of processing
2. Nature and purpose of processing
3. Type of personal data and categories of data subjects
4. Obligations and rights of the controller

Processor Obligations:
5. Process data only on documented instructions from controller
6. Ensure confidentiality of personnel authorized to process data
7. Implement appropriate technical and organizational measures
8. Not engage another processor (sub-processor) without controller's authorization
9. Assist controller with data subject requests
10. Assist controller with compliance obligations (security, breach notification, DPIAs)
11. Delete or return data at end of services
12. Demonstrate compliance (maintain records, accept audits)
```

## What Your DPA Should Include

### 1. Definitions

```
Definitions

"Personal Data": Any information relating to an identified or identifiable
natural person, as defined by applicable data protection laws.

"Processing": Any operation performed on personal data, including
collection, storage, use, disclosure, and deletion.

"Data Controller": The customer who determines the purposes and means
of processing personal data.

"Data Processor": [Company Name], who processes personal data on behalf
of the Data Controller.

"Sub-processor": A third party engaged by the Data Processor to process
personal data under the terms of this DPA.

"Data Subject": The individual to whom the personal data relates.
```

### 2. Details of Processing

```
Details of Processing

Subject Matter: Provision of [Product Name] SaaS platform and related
services as described in the Terms of Service.

Duration: The term of the agreement between Controller and Processor,
plus the period until data is deleted per the terms.

Nature and Purpose: Processing personal data solely to provide, maintain,
and support the Service as instructed by the Controller.

Type of Personal Data:
  → Names, email addresses, and contact information
  → Account login credentials
  → Usage data and interaction with the Service
  → Any other data uploaded by Controller through the Service
  → (Note: We do not intentionally process sensitive data categories)

Categories of Data Subjects:
  → Controller's employees, contractors, and agents
  → Controller's customers and end users
  → Any other individuals whose data is uploaded by Controller
```

### 3. Processor Obligations

```
Processor Obligations

1. Processing Instructions
   Processor shall process personal data only on documented instructions
   from Controller, unless required by law (in which case Processor shall
   inform Controller of that legal requirement before processing).

2. Confidentiality
   Processor shall ensure that all personnel authorized to process
   personal data have committed to confidentiality obligations.

3. Security Measures
   Processor shall implement appropriate technical and organizational
   measures to ensure a level of security appropriate to the risk.
   [See Security Measures section]

4. Sub-processing
   Controller provides general authorization for Processor to engage
   sub-processors. Processor will:
   → Maintain a list of sub-processors (see Sub-processors section)
   → Notify Controller of any changes (minimum 30 days notice)
   → Allow Controller to object to changes
   → Ensure sub-processors are bound by equivalent obligations

5. Data Subject Rights
   Processor shall assist Controller in responding to data subject
   requests (access, rectification, erasure, restriction, portability,
   objection) by providing tools and responding to reasonable requests.

6. Breach Notification
   Processor shall notify Controller without undue delay (within 48 hours
   of becoming aware) of any personal data breach affecting Controller's
   data.

7. Data Protection Impact Assessment
   Processor shall assist Controller with DPIAs and prior consultations
   with supervisory authorities, taking into account the nature of
   processing and information available.

8. Deletion or Return
   At the end of services, Processor shall delete or return all personal
   data to Controller per the Terms of Service (typically 30-day grace
   period for export, then deletion).

9. Demonstration of Compliance
   Processor shall make available all information necessary to demonstrate
   compliance and allow for audits by Controller or an independent
   auditor, subject to reasonable notice and confidentiality.
```

### 4. Technical and Organizational Measures

```
Technical and Organizational Measures

1. Access Control (Preventing unauthorized access)
   → Unique user IDs and strong password policies
   → Multi-factor authentication for administrative access
   → Role-based access controls
   → Automatic session timeout

2. Pseudonymization and Encryption
   → Encryption in transit: TLS 1.2+ for all data transmission
   → Encryption at rest: AES-256 for stored data
   → Database encryption at rest

3. Availability and Resilience
   → Redundant infrastructure across availability zones
   → Daily automated backups
   → Disaster recovery plan with regular testing
   → 99.9% uptime target (or best effort)

4. Incident Response
   → 24/7 monitoring and alerting
   → Documented incident response plan
   → Breach notification within 48 hours

5. Testing and Assessment
   → Regular security assessments
   → Dependency vulnerability scanning
   → Penetration testing (at least annually)

6. Organizational Measures
   → Data protection training for personnel
   → Confidentiality agreements for all employees
   → Security policies and procedures
```

### 5. Sub-processors

```
Sub-processors

Current Sub-processors:
  - Amazon Web Services (AWS): Cloud hosting and infrastructure
  - Stripe, Inc.: Payment processing
  - SendGrid (Twilio): Email delivery
  - Sentry: Error monitoring
  - PostHog: Product analytics
  - Help Scout: Customer support platform
  - [Any others]

Engagement of New Sub-processors:
  → We will notify you of any changes to sub-processors
  → Notification will be via email or in-app notification
  → You may object within 14 days of notification
  → If reasonable objection cannot be resolved, either party may
    terminate the affected services without penalty

Due Diligence:
  → We conduct security assessments of all sub-processors
  → Sub-processors are contractually bound to data protection obligations
    equivalent to those in this DPA
```

### 6. International Transfers

```
International Transfers

Data is primarily processed in the United States.

For personal data originating in the EEA, UK, or Switzerland:
  → Transfers are protected by Standard Contractual Clauses (SCCs)
    as adopted by the European Commission
  → Controller enters into SCCs with Processor (incorporated by reference)
  → Sub-processor transfers are covered by SCCs between Processor and
    sub-processor
  → Alternatively, sub-processors may rely on:
    → Adequacy decisions (e.g., UK adequacy for US under Data Bridge)
    → Binding Corporate Rules (for larger processors)

Transfer Impact Assessment:
  → Processor will conduct a Transfer Impact Assessment (TIA) upon
    reasonable request
```

### 7. Liability and Indemnification

```
Liability

Processor's liability shall be governed by the Terms of Service.
Processor's total liability for all claims under this DPA shall not
exceed the amounts paid by Controller to Processor in the [12] months
preceding the claim.

This cap does not apply to:
  → Claims arising from Processor's breach of Section 3 (Processor Obligations)
  → Claims arising from Processor's failure to comply with applicable
    data protection law
  → Claims arising from Processor's gross negligence or willful misconduct
```

### 8. Termination

```
Termination

This DPA shall terminate automatically with the termination of the
underlying Terms of Service.

Upon termination:
  → Processor shall delete all personal data per the Terms of Service
  → Upon request, Processor shall certify deletion has occurred

Survival:
  → Sections on confidentiality, liability, and governing law survive
```

## How to Offer Your DPA

### Make It Accessible

```markdown
1. Link in your website footer:
   Terms of Service | Privacy Policy | DPA

2. Link in your product (Settings/Account page):
   Legal Documents → DPA

3. Link in your Terms of Service:
   "For our Data Processing Agreement, see [link]"

4. Include in onboarding:
   Enterprise customers: Send DPA with contract
```

### Signature-Free vs Signed DPA

**Signature-free (recommended for self-service):**
The DPA is incorporated into your ToS by reference. When a customer accepts your ToS, they automatically accept the DPA. This is legally valid under GDPR for standard services.

**Signed DPA (for enterprise customers):**
Some customers will require a signed DPA. Use a service like DocuSign or HelloSign to manage this.

**Template DPA signature block:**

```
IN WITNESS WHEREOF, the parties have executed this Data Processing
Agreement as of the date of acceptance of the Terms of Service.

[Company Name]
By: _______________________
Name: _____________________
Title: ____________________
Date: _____________________
```

## DPA Template for Solo Founders

Here is a complete, ready-to-use DPA template. Customize the bracketed sections.

```markdown
DATA PROCESSING AGREEMENT

This Data Processing Agreement ("DPA") is entered into between:

[Company Name] ("Processor")
[Customer] ("Controller")

and supplements the Terms of Service between the parties.

1. DEFINITIONS

Capitalized terms not defined here have the meanings in the Terms of
Service or applicable data protection law.

2. DETAILS OF PROCESSING

Subject Matter: Provision of [Product Name] SaaS platform
Duration: Term of the Terms of Service
Purpose: Providing the Service to Controller
Personal Data: Names, email addresses, account details, usage data,
and any data uploaded by Controller
Data Subjects: Controller's employees, customers, and end users

3. PROCESSOR OBLIGATIONS

3.1 Processor shall process personal data only on Controller's documented
instructions.

3.2 Processor shall ensure all personnel with access to personal data
are bound by confidentiality.

3.3 Processor shall implement appropriate technical and organizational
measures as described in Appendix A.

3.4 Processor shall not engage sub-processors without Controller's
general authorization. Current sub-processors are listed in Appendix B.

3.5 Processor shall assist Controller with data subject requests.

3.6 Processor shall notify Controller within 48 hours of becoming aware
of a personal data breach.

3.7 Processor shall assist Controller with DPIAs.

3.8 Processor shall delete or return personal data at the end of services.

4. SUB-PROCESSORS

Controller provides general authorization for Processor to engage
sub-processors. Processor shall notify Controller of changes with
30 days notice. Controller may object within 14 days.

5. INTERNATIONAL TRANSFERS

For data from EEA/UK: Standard Contractual Clauses (EU 2021/914)
apply and are incorporated by reference.

6. LIABILITY

Processor's liability under this DPA is subject to the limitations
in the Terms of Service.

7. TERMINATION

This DPA terminates with the Terms of Service.

APPENDIX A: TECHNICAL AND ORGANIZATIONAL MEASURES
[Describe your security measures]

APPENDIX B: SUB-PROCESSORS
[List all sub-processors]

APPENDIX C: STANDARD CONTRACTUAL CLAUSES (if applicable)
[Attach SCCs or incorporate by reference]
```

## Handling Enterprise DPA Requests

Enterprise procurement teams will often request changes to your DPA. Common requests and how to handle them:

| Enterprise Request | Recommended Response |
|-------------------|---------------------|
| "We need you to sign our DPA instead" | Expensive (legal review). Politely decline and offer yours. |
| "Add more data categories" | Fine if they're categories you actually process |
| "List every sub-processor" | Fine — keep a current list |
| "Remove right to change sub-processors" | Problematic. Offer 30-day notice instead. |
| "Audit rights (unlimited, at our expense)" | Offer limited audit (annually, at their expense, with NDA) |
| "Higher liability cap" | Can increase (e.g., to 2-3x annual fees) |
| "Require 24-hour breach notification" | 48 hours is standard. 24 hours is achievable for serious breaches. |
| "Cybersecurity insurance requirements" | Reasonable if you have it. Minimum $1-2M coverage. |
| "Specific technical controls (encryption, access)" | Only if they're capabilities you actually have |
| "Data residency (keep data in specific region)" | Costly. Charge more for this. |

## When to Upgrade Your DPA

| Stage | DPA Approach |
|-------|-------------|
| Pre-revenue / MVP | Have a basic DPA ready (template from Avodocs) |
| First customers ($0-5k MRR) | Self-serve DPA (incorporated into ToS) |
| Growth ($5-20k MRR) | Started having it signed by enterprise customers |
| Scale ($20k+ MRR) | Lawyer-reviewed DPA, handle custom requests |

## Resources

- [GDPR Article 28](https://gdpr-info.eu/art-28-gdpr/) — The legal basis for DPAs
- [UK ICO DPA Guidance](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/contracts/) 
- [EU Standard Contractual Clauses](https://ec.europa.eu/info/law/law-topic/data-protection/international-dimension-data-protection/standard-contractual-clauses-scc_en)
- [Avodocs DPA Template](https://www.avodocs.com/) — Free DPA templates
- [Ironclad DPA Template](https://ironcladapp.com/) — DPA management
- [Vendr DPA Repository](https://www.vendr.com/) — Enterprise DPA requirements reference
