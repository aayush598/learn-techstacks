# Security Consulting Proposal Template

## How to Use This Template

Security is sold through fear, compliance pressure, and risk quantification. Your proposal must make the client feel the pain of inaction more than the pain of investment. Use concrete numbers, regulatory references, and worst-case scenarios — but always offer a clear path to safety.

---

## Proposal Header

```
PROPOSAL FOR: [Client Company Name]
PROJECT: [Security Engagement Name — e.g., "SOC 2 Readiness Assessment" / "Penetration Testing" / "Security Architecture Review"]
PREPARED BY: [Your Name / Company]
CONFIDENTIALITY: CONFIDENTIAL — Contains security-sensitive information
DATE: [Date]
PROPOSAL VALID UNTIL: [Date — 14 days, security timelines change fast]

VERSION: 1.0
CLASSIFICATION: [Client-Facing / Internal Use Only]
```

---

## Executive Summary

```
Thank you for the opportunity to propose a security engagement for [Company Name].

After our initial conversations, here's my assessment of your current security posture:

[Brief summary of key risks, compliance gaps, or vulnerabilities identified]

This proposal outlines a [assessment type] engagement that will:
• Identify critical vulnerabilities before attackers do
• [Achieve compliance milestone]
• Reduce your risk exposure by [X]%
• Provide a prioritized remediation roadmap

Investment: $[X]
Timeline: [X] weeks
Deliverable: Comprehensive report with executive summary, technical findings, and remediation plan.

In today's threat landscape, the question isn't if you'll be targeted — it's when. This engagement gives you the visibility and roadmap to defend effectively.
```

---

## Threat Landscape & Business Case

```
THE CASE FOR ACTION
──────────────────

YOUR CURRENT RISK PROFILE:
Based on our preliminary assessment and industry benchmarks for [industry/company size]:

RISK 1: [Specific vulnerability / gap]
• Likelihood: [High/Medium/Low]
• Impact: [High/Medium/Low]
• Business consequence: [What happens if exploited]
• Regulatory consequence: [Fines, audits, loss of certification]

RISK 2: [Specific vulnerability / gap]
• Likelihood: [High/Medium/Low]
• Impact: [High/Medium/Low]
• Business consequence: [What happens if exploited]
• Regulatory consequence: [Fines, audits, loss of certification]

RISK 3: [Specific vulnerability / gap]
• Likelihood: [High/Medium/Low]
• Impact: [High/Medium/Low]
• Business consequence: [What happens if exploited]
• Regulatory consequence: [Fines, audits, loss of certification]

INDUSTRY CONTEXT:
• [X]% of companies in [industry] experienced a breach in the last year
• Average cost of a breach in [industry]: $[X million]
• Average time to detect a breach: [X] months
• [Specific regulation] fines: up to $[X] per violation

COST OF INACTION:
• Financial: Potential breach cost of $[X] — [Y]x the cost of this engagement
• Reputational: [Quantified impact — customer churn, stock price, trust]
• Operational: [Days/weeks of downtime, recovery costs]
• Legal: [Potential lawsuits, regulatory fines, shareholder actions]

TREATMENT RECOMMENDATION:
[Immediate action required / Medium-term priority / Low risk — monitor only]
```

---

## Engagement Scope

```
SCOPE OF WORK
─────────────

IN-SCOPE ASSETS & SYSTEMS:

NETWORK:
• [X] external IP addresses / ranges
• [X] internal network segments
• [Firewall / VPN / WAF configuration review]

APPLICATIONS:
• [Application 1] — [URL/IP, purpose]
• [Application 2] — [URL/IP, purpose]
• [Application 3] — [URL/IP, purpose]

INFRASTRUCTURE:
• [Cloud provider accounts]
• [X] servers / instances
• [Database systems]
• [Container environments]

IDENTITY & ACCESS:
• [Identity provider — Okta, Azure AD, etc.]
• [X] user accounts
• [Privileged access management review]

POLICIES & PROCEDURES:
• Security policies review
• Incident response plan review
• Disaster recovery / BC plan review

OUT OF SCOPE:
• [Systems explicitly excluded]
• [Source code review (separate engagement)]
• [Physical security assessment]
• [Social engineering testing]
• [Third-party vendor risk assessment]

TESTING CONSTRAINTS:
• Testing window: [Dates and times]
• Excluded test types: [DoS testing, destructive tests, etc.]
• Emergency contacts: [Name, phone, email]
```

---

## Methodology

```
METHODOLOGY
──────────

My security assessment methodology follows industry standards (OWASP, NIST, PTES, OSSTMM) and consists of:

PHASE 1: RECONNAISSANCE & INTELLIGENCE GATHERING (Days 1-2)
• Passive reconnaissance: OSINT, DNS enumeration, subdomain discovery
• Active reconnaissance: Port scanning, service identification, version detection
• Technology stack fingerprinting
• Third-party dependency analysis
• DELIVERABLE: Reconnaissance report with attack surface map

PHASE 2: VULNERABILITY ASSESSMENT (Days 3-5)
• Automated scanning with [Nessus / Qualys / OpenVAS / Nuclei]
• Manual verification of all findings (eliminate false positives)
• Configuration review against CIS benchmarks
• Patch level audit
• DELIVERABLE: Vulnerability scan results (verified, no false positives)

PHASE 3: MANUAL TESTING & EXPLOITATION (Days 6-10)
• OWASP Top 10 web application testing
• API security testing
• Business logic flaw analysis
• Authentication & authorization testing
• Session management testing
• Injection testing (SQL, NoSQL, OS command, LDAP)
• Privilege escalation attempts
• Lateral movement testing
• DELIVERABLE: Detailed findings with proof-of-concept evidence

PHASE 4: REMEDIATION VALIDATION (Days 11-12)
• Client remediates critical findings
• Re-testing of all findings
• Validation of fixes
• DELIVERABLE: Re-test results and final status

PHASE 5: REPORTING & PRESENTATION (Days 13-14)
• Executive summary with risk scores
• Technical findings with detailed reproduction steps
• Remediation roadmap (immediate, short-term, long-term)
• Strategic recommendations
• DELIVERABLES:
  - Executive report (non-technical, board-ready)
  - Technical report (for engineering team)
  - Remediation plan with effort estimates
  - 30-minute findings presentation
```

---

## Engagement Types & Pricing

```
ENGAGEMENT OPTIONS
─────────────────

OPTION A: VULNERABILITY ASSESSMENT ($[X])
Best for: Organizations with established security programs needing regular scanning
Includes:
• Automated scanning with manual verification
• OWASP Top 10 coverage
• Configuration review
• Executive and technical reports
• Timeline: [X] days
• Deliverable: Assessment report

OPTION B: PENETRATION TEST ($[X]) ← RECOMMENDED
Best for: Organizations needing deep manual testing
Includes:
• Everything in Option A
• Full manual penetration testing
• Business logic testing
• API security testing
• Authentication bypass attempts
• Privilege escalation testing
• Remediation re-testing
• Timeline: [X] days
• Deliverable: Full pentest report + presentation

OPTION C: COMPREHENSIVE SECURITY ASSESSMENT ($[X])
Best for: Organizations needing complete security posture evaluation
Includes:
• Everything in Option B
• Architecture review
• Cloud security assessment
• Container security review
• IAM audit
• Policy and procedure review
• 30-day retesting window
• Timeline: [X] days
• Deliverable: Full assessment + remediation roadmap

OPTION D: COMPLIANCE READINESS ASSESSMENT ($[X])
Best for: Organizations pursuing certification
Compliance targets available:
• SOC 2 Type I/II readiness
• HIPAA security assessment
• PCI DSS gap analysis
• ISO 27001 pre-assessment
• GDPR readiness
Includes:
• Gap analysis against framework
• Evidence gathering support
• Policy template updates
• Remediation roadmap
• Timeline: [X] weeks
• Deliverable: Readiness report + gap analysis
```

---

## Deliverables

```
DELIVERABLES
───────────

All engagements include:

1. EXECUTIVE REPORT
   • One-page risk summary (board-ready)
   • Overall security score
   • Key findings by priority
   • Business impact analysis
   • Recommended budget allocation

2. TECHNICAL REPORT
   • Full findings list with CVSS scores
   • Step-by-step reproduction for each finding
   • Screenshots and proof-of-concept
   • Recommended fix for each finding
   • Effort estimate for each fix

3. REMEDIATION ROADMAP
   • Immediate actions (24-48 hours)
   • Short-term (1-4 weeks)
   • Medium-term (1-3 months)
   • Long-term (3-12 months)
   • Dependencies and recommended order

4. FINDINGS PRESENTATION
   • 30-minute slide deck
   • Live Q&A session
   • Recorded for absent stakeholders

5. RAW DATA
   • Scan results (if applicable)
   • Testing logs
   • Methodology documentation
```

---

## Timeline

```
PROJECT TIMELINE
───────────────

TOTAL DURATION: [X] weeks

WEEK 1: RECONNAISSANCE & SCANNING
• OSINT and passive recon
• Automated scanning
• Manual verification of findings
• Client notification of critical findings (within 24 hours of discovery)

WEEK 2: MANUAL TESTING
• Deep-dive manual testing
• Business logic analysis
• Attempted exploitation
• Ongoing client communication for clarification

WEEK 3: REPORTING
• Report compilation
• Executive summary
• Remediation roadmap
• Internal review and quality assurance

WEEK 4: PRESENTATION & RE-TESTING
• Findings presentation
• Client remediation period
• Re-testing of fixed findings
• Final report delivery

SCHEDULING NOTES:
• Testing occurs during [client's preferred window]
• Emergency findings reported within 24 hours
• Re-testing window: [X] days after initial report delivery
```

---

## Investment

```
INVESTMENT
─────────

SELECTED OPTION: [Option A/B/C/D]
TOTAL INVESTMENT: $[X]

BREAKDOWN:
• Reconnaissance & scanning: $[X]
• Manual testing: $[X]
• Reporting & presentation: $[X]
• Remediation re-testing: $[X]

ADDITIONAL SERVICES (if needed):
• Extended re-testing window: $[X]/month
• Additional application: $[X] each
• Social engineering add-on: $[X]
• Source code review: $[X]/app
• Cloud security review: $[X]
• Emergency retainer (incident response): $[X]/month

PAYMENT TERMS:
• 50% upon engagement kickoff
• 50% upon report delivery
• Net 15 invoicing

VOLUME DISCOUNTS:
• Quarterly engagements: 10% discount
• Bi-annual engagements: 15% discount
• Annual retainer: 20% discount + priority scheduling
```

---

## Credentials & Social Proof

```
QUALIFICATIONS
─────────────

CERTIFICATIONS:
• OSCP (Offensive Security Certified Professional)
• CISSP (Certified Information Systems Security Professional)
• CEH (Certified Ethical Hacker)
• AWS Security Specialty
• [Other relevant certs]

EXPERIENCE:
• [X] years in information security
• [X] penetration tests conducted
• [X] organizations assessed
• [Industries covered]

NOTABLE ENGAGEMENTS:
• [Engagement 1]: [Description, scope, result]
• [Engagement 2]: [Description, scope, result]
• [Engagement 3]: [Description, scope, result]

RECOGNITION:
• [CVE disclosures, if any]
• [Conference talks / training delivered]
• [Publication / blog / research]

TESTIMONIALS:
"[Security assessment feedback]"
— [Name], [Title] at [Company]

"[Testimonial about remediation support]"
— [Name], [Title] at [Company]
```

---

## Legal & Compliance

```
TERMS & CONDITIONS
─────────────────

AUTHORIZATION:
By signing this proposal, [Client Company] authorizes [Your Company/Name] to perform security testing against the systems listed in the scope section. This authorization includes permission to attempt to penetrate, access, and extract data from the specified systems within the agreed-upon testing parameters.

RULES OF ENGAGEMENT:
• Testing will be conducted within the agreed testing window
• No social engineering without explicit authorization
• No denial-of-service testing unless explicitly authorized
• No destruction or modification of production data
• Any customer PII encountered will be immediately reported and not stored
• [Your Company] will not use any exploits that cause service degradation

CONFIDENTIALITY:
All findings, data, and reports are confidential and will not be disclosed to third parties without written consent, except as required by law.

LIABILITY:
Liability is limited to the value of the engagement. [Your Company] is not liable for:
• Existing vulnerabilities exploited by third parties during testing
• Service disruptions caused by authorized testing activities
• Vulnerabilities introduced by client remediation efforts

DATA HANDLING:
• All testing data will be encrypted at rest and in transit
• Data will be retained for [X] months, then securely deleted
• Client may request earlier deletion at any time

REPORTING OBLIGATIONS:
[Your Company] is required by law to report:
• Child exploitation material (if discovered)
• Imminent threat to life or property
• Court-ordered disclosure

INSURANCE:
• Professional Liability / Errors & Omissions: $[X million]
• Cyber Liability: $[X million]
• General Liability: $[X million]
```

---

## Next Steps

```
NEXT STEPS
─────────

1. Schedule a 30-minute scope clarification call
   [Calendly Link]

2. I'll refine the scope based on our conversation

3. Sign the SOW and scope agreement

4. Schedule the testing window

5. Testing begins on [preferred date]

TIMING CONSIDERATIONS:
• I typically schedule engagements [X] weeks in advance
• Current lead time: [X] weeks
• I recommend confirming within [X] days to secure your preferred testing window

Let's make your systems resilient.

[Your Name]
[Title]
[Contact Info]
[Security-focused website / LinkedIn / GitHub]
```

---

## Appendix: Common Compliance Frameworks

### SOC 2 Readiness Checklist

| Control Area | Key Requirements | Typical Gaps |
|-------------|-----------------|--------------|
| Security | Firewall, IDS/IPS, access control, encryption | Missing logging, no incident response plan |
| Availability | Monitoring, capacity planning, DR plan | No DR testing, insufficient monitoring |
| Processing Integrity | Input validation, error handling, quality assurance | No formal QA process |
| Confidentiality | Encryption, access controls, data classification | No data classification policy |
| Privacy | Notice, choice, consent, access, disclosure | Incomplete privacy policy |

### HIPAA Security Rule Coverage

| Standard | Implementation | Evidence |
|----------|---------------|----------|
| Administrative Safeguards | Security management process, workforce training | Policies, training records |
| Physical Safeguards | Facility access controls, workstation security | Access logs, camera records |
| Technical Safeguards | Access control, audit controls, integrity controls | System logs, encryption |
| Policies & Procedures | Written policies, periodic review | Policy documents, review records |

### PCI DSS High-Level Requirements

| Requirement | Focus Area |
|-------------|-----------|
| Build and Maintain a Secure Network | Firewall, secure config |
| Protect Cardholder Data | Encryption at rest and in transit |
| Maintain Vulnerability Management | AV, patching, secure coding |
| Implement Strong Access Control | Need-to-know, unique IDs, physical security |
| Regularly Monitor and Test Networks | Logging, monitoring, testing |
| Maintain an Information Security Policy | Policy, risk assessment |

## Security Pricing Guide

| Service Type | Typical Range | Key Factors |
|-------------|--------------|-------------|
| External pentest (web app, single) | $5,000-$15,000 | Complexity, number of roles/functions |
| External pentest (network, /24) | $4,000-$10,000 | Number of hosts, services |
| Internal pentest | $6,000-$18,000 | Network size, AD complexity |
| Mobile app pentest | $8,000-$20,000 | iOS vs Android, API complexity |
| Cloud security review | $10,000-$30,000 | Number of accounts, services |
| Source code review | $8,000-$25,000 | Lines of code, languages |
| SOC 2 readiness | $15,000-$40,000 | Company size, existing controls |
| Red team engagement | $25,000-$100,000 | Duration, scope, stealth requirements |
| Incident response retainer | $3,000-$10,000/month | Response time, hours included |

## Security Proposal Objections

| Objection | Response |
|-----------|----------|
| "We haven't been breached yet" | "That's what every breached company said before they found out. Average detection time is [X] months. You may already be compromised." |
| "It's too expensive" | "The average breach cost in your industry is $[X]. This assessment costs [Y]% of that. Can you afford NOT to know?" |
| "Our developers handle security" | "Developers are great at building features. Security testing requires adversarial thinking — a completely different mindset. Would you have your developers defend you in court?" |
| "We're too small to be targeted" | "60% of cyber attacks target small and medium businesses. Automated attacks don't discriminate by size." |
| "Our cloud provider handles security" | "Cloud providers use a shared responsibility model. They secure the cloud. You secure what's in the cloud." |
