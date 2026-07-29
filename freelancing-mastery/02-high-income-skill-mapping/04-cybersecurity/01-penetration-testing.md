# Penetration Testing Freelancing

## Overview

Penetration testing (pentesting) is one of the most in-demand cybersecurity freelancing niches. Companies need to identify vulnerabilities before attackers do — and they're required to by compliance frameworks (SOC 2, HIPAA, PCI DSS).

This guide covers how to build a pentesting freelancing practice, the certifications that matter, rates, and client acquisition.

## Why Pentesting Pays Well

1. **Legal/compliance requirement**: Many industries require regular pentests (PCI DSS, SOC 2, FedRAMP)
2. **High stakes**: A breach costs millions — companies invest in prevention
3. **Insurance requirement**: Cyber insurance policies often require pentesting
4. **Scarcity**: Good pentesters who can write quality reports are rare
5. **Recurring revenue**: Companies need pentests annually or quarterly

### Rate Reality

| Service | Junior (1-2yr) | Mid (3-5yr) | Senior (5-10yr) | Expert (10yr+) |
|---------|---------------|-------------|-----------------|----------------|
| Web App Pentest | $75-125/hr | $125-175/hr | $150-250/hr | $200-350/hr |
| Network Pentest | $75-125/hr | $125-175/hr | $150-250/hr | $200-350/hr |
| Mobile App Pentest | $100-150/hr | $150-200/hr | $175-275/hr | $225-400/hr |
| Cloud Security Review | $100-150/hr | $150-225/hr | $200-300/hr | $250-500/hr |
| Social Engineering | $100-150/hr | $150-200/hr | $175-275/hr | $225-400/hr |
| Red Team Engagement | $150-200/hr | $200-300/hr | $250-400/hr | $300-500/hr |

**Typical project pricing**:
- Basic web app pentest: $3-10K
- Standard web/API pentest: $5-20K
- Mobile app pentest: $8-25K
- Cloud infrastructure review: $10-30K
- Full red team engagement: $30-150K
- PCI DSS pentest: $5-15K
- SOC 2 pentest: $8-20K

## Certifications That Matter

### Tier 1 (Highest Value)

**OSCP (Offensive Security Certified Professional)**
- The gold standard entry-level cert for pentesters
- 24-hour practical exam — proves you can actually hack
- Cost: $1,600 (one attempt + 90 days lab)
- Requirement for many pentesting roles
- Without this, you'll struggle to get clients

**OSEP (Offensive Security Experienced Professional)**
- Advanced pentesting with evasion techniques
- Much harder than OSCP
- Commands higher rates ($50-100/hr premium over OSCP)
- Differentiator for red team roles

**CREST CCT (CREST Certified Tester)**
- Required by some enterprise clients (banking, UK government)
- Practical and written exam
- More recognized in UK/Europe than US

### Tier 2 (Valuable Specializations)

**OSWE (Offensive Security Web Expert)**
- Web application pentesting specific
- Source code review and white-box testing

**GPEN (GIAC Penetration Tester)**
- Good for government/enterprise clients
- Expensive ($8K+ per attempt)
- Less respected than OSCP in the community

**GWAPT (GIAC Web Application Penetration Tester)**
- Web app pentesting focus
- Good complement to GPEN

**PNPT (Practical Network Penetration Tester)**
- Newer cert from TCM Security
- Practical exam, more affordable
- Growing in recognition

### Tier 3 (Nice to Have)

- CEH (Certified Ethical Hacker) — basic, but required by some government contracts
- CISSP — broad security knowledge, shows you understand the bigger picture
- AWS Security / Azure Security — if specializing in cloud pentesting

### Certification Strategy

1. **First**: OSCP (non-negotiable for credibility)
2. **Second**: OSWE or PNPT (depending on specialty)
3. **Third**: AWS Security or Azure Security (cloud is growing fast)
4. **Optional**: CREST CCT (if pursuing UK/European enterprise clients)

**Note**: Certifications open doors. Real skill keeps clients. Your reports need to be excellent — that's what clients actually pay for.

## Service Offerings

### Service 1: Web Application Pentesting

**What you do**: Test web applications for vulnerabilities.

**Standard scope**:
- OWASP Top 10 vulnerabilities
- Authentication and session management
- Access control and privilege escalation
- Input validation (XSS, SQLi, SSTI, etc.)
- API security (REST, GraphQL)
- Business logic flaws
- File upload and SSRF vulnerabilities

**Methodology**:
1. Reconnaissance and information gathering
2. Automated scanning (Burp Suite, custom tools)
3. Manual testing (deep dive on business logic, auth, etc.)
4. Exploitation (prove vulnerabilities exist)
5. Reporting (detailed findings with remediation)

**Deliverables**:
- Executive summary (1-2 pages, non-technical)
- Technical report (10-50 pages with evidence and remediation)
- Verified finding list with CVSS scores
- Retesting after fixes (usually 30 days)

**Pricing**: $5-20K depending on application complexity

### Service 2: API Security Testing

**What you do**: Specifically test APIs (REST, GraphQL, gRPC, WebSocket).

**Why this is in demand**: Most modern apps are API-driven, but most pentesters focus on traditional web apps.

**API-specific testing**:
- Authentication and authorization (broken object-level auth, broken function-level auth)
- Mass assignment
- Rate limiting and abuse
- Injection (SQLi, NoSQLi, command injection)
- Excessive data exposure
- GraphQL introspection and query depth attacks

**Tools**: Burp Suite, Postman, custom scripts, inql (GraphQL), graphql-hackerone

### Service 3: Mobile Application Pentesting

**What you do**: Test iOS and Android applications.

**Scope**:
- Static analysis (reverse engineering, code review)
- Dynamic analysis (runtime manipulation)
- Network traffic analysis
- Local storage analysis
- API security (shared with backend)

**Tools**: Frida, objection, MobSF, APKTool, jadx, Hopper (iOS)

**Pricing**: $8-25K per platform (iOS or Android), $12-35K for both

### Service 4: Network Penetration Testing

**What you do**: Test internal and external network infrastructure.

**Scope**:
- External perimeter testing
- Internal network testing
- Wireless network testing
- VPN and remote access testing
- Active Directory security assessment

**Tools**: Nmap, BloodHound, Responder, CrackMapExec, Metasploit, Impacket

**Pricing**: $5-20K (external), $8-25K (internal), $12-35K (full)

### Service 5: Cloud Security Review

**What you do**: Review cloud infrastructure for misconfigurations and vulnerabilities.

**This is a growing niche** — most pentesters don't know cloud well.

**Scope**:
- IAM policy review (over-permissive roles, unused permissions)
- Storage security (public S3 buckets, unencrypted data)
- Network security (security groups, NACLs, VPC peering)
- Logging and monitoring (is it possible to detect an attack?)
- Container security (Kubernetes misconfigurations, container vulnerabilities)
- CI/CD pipeline security

**Tools**: ScoutSuite, Prowler, CloudSploit, kube-hunter, Trivy

**Pricing**: $10-30K depending on environment size and complexity

### Service 6: Red Team Engagement

**What you do**: Full-scope attack simulation — test people, processes, and technology.

**This is the highest-ticket pentesting service.**

**Scope**:
- Social engineering (phishing, vishing, physical)
- Web and network exploitation
- Persistence (maintain access and achieve objectives)
- Lateral movement
- Data exfiltration (simulated)
- Full report with timeline and recommendations

**Duration**: 2-6 weeks
**Pricing**: $30-150K depending on scope and duration

### Service 7: PCI DSS / Compliance Pentesting

**What you do**: Pentesting required for compliance certifications.

**PCI DSS requirements for pentesting** (what clients need):
- External and internal network pentesting (at least annually)
- Web application pentesting (at least annually and after changes)
- Segmentation testing (for CDE isolation)
- Methodology must follow NIST, OWASP, or similar

**Other compliance pentesting**:
- SOC 2 pentesting (usually less prescriptive)
- HIPAA security assessment
- GDPR security review

**Pricing**: $5-15K for PCI DSS scope (typically less complex than full pentest)

## Client Acquisition

### Where Pentesting Clients Come From

**1. Compliance referrals** (40%)
- Companies need pentests for SOC 2, HIPAA, PCI DSS, ISO 27001
- Their compliance consultant or auditor refers you
- **Build**: Network with compliance consultants and auditors

**2. Direct outreach** (25%)
- Target companies that recently got funded, grew significantly
- Target companies in regulated industries (fintech, healthtech, crypto)
- **Build**: Cold email with specific findings (without being creepy)

**3. Referrals from other pentesters** (15%)
- Other pentesters who are too busy or don't do certain types of testing
- **Build**: Network with other pentesters

**4. Content marketing** (10%)
- Blog posts about vulnerabilities you've found
- Write-ups of CTF challenges
- Conference talks
- **Build**: Start a blog, speak at security conferences

**5. Upwork / platforms** (10%)
- Good for building initial portfolio
- Low rates, high competition

### Ideal Client Profile

- SaaS companies preparing for SOC 2 certification
- Fintech companies (Plaid, Stripe integrations, crypto)
- Healthtech companies (HIPAA compliance)
- E-commerce companies (PCI DSS)
- Enterprise companies with regular pentesting requirements
- VC-backed startups (they have budget and compliance needs)

### Outreach Script

```
Subject: Security assessment for [Company]

Hi [Name],

I'm a penetration tester specializing in [web/mobile/cloud] security.

I noticed [Company] is [growing/got funded/recently launched].
Many companies at your stage benefit from a proactive security
assessment before compliance requirements force one.

My approach:
1. Test your [app/API/infrastructure] for OWASP Top 10 and
   business logic vulnerabilities
2. Provide detailed findings with proof-of-concept and remediation
3. Deliver an executive summary for stakeholders and a technical
   report for your engineering team

Recent engagement found [X] critical vulnerabilities for a similar
company. All were fixed within 2 weeks of the report.

Would you be open to a brief call to discuss your security needs?

Best,
[Your Name]
[OSCP | OSWE | Certifications]
[Link to portfolio]
```

## Pricing Strategy

### Hourly vs Project Pricing

**Project pricing is standard in pentesting.** Few clients want hourly. They want a fixed price for a specific scope.

**Pricing factors**:
1. Application complexity (simple CRUD vs complex microservices)
2. Number of user roles and permission levels
3. API depth (number of endpoints)
4. Authentication complexity (SSO, OAuth, MFA)
5. Compliance requirements (PCI DSS, SOC 2, etc.)
6. Your experience and certifications

### Pricing by Application Type

| Application Type | Price Range | Typical Hours |
|-----------------|-------------|---------------|
| Simple brochure/landing page | $2-5K | 20-40 |
| Standard CRUD web app | $5-10K | 40-60 |
| Complex web app (multi-tenant, roles) | $10-20K | 60-100 |
| API-only (microservices) | $8-15K | 40-80 |
| Mobile app (one platform) | $8-15K | 40-80 |
| Mobile app (both platforms) | $12-25K | 60-120 |
| Cloud infrastructure review | $10-30K | 60-120 |
| Full external + internal network | $10-25K | 60-100 |
| Red team engagement | $30-150K | 200-600 |

### What Affects Your Rate

**Increases your rate**:
- OSCP or equivalent
- Published CVEs (shows you find real vulnerabilities)
- Experience in their industry (fintech, healthcare)
- Compliance expertise (PCI DSS, SOC 2, HIPAA)
- Fast turnaround time (rush engagement = 1.5-2x)
- Bug bounty program reputation (HackerOne, Bugcrowd ranking)

**Decreases your rate**:
- No certifications
- No public portfolio/demonstrable experience
- Client has a lot of pentesters to choose from
- Large scope with low budget (walk away, not worth it)

## Building a Pentesting Lab

### Hardware

- **Laptop**: 32GB+ RAM, 8+ cores, 512GB+ SSD (for running VMs)
- **Secondary machine**: For authenticated testing (Windows VM for AD environments)
- **Cloud lab**: AWS/Azure accounts for testing cloud-specific issues

### Software Stack

**Essential tools**:
- Burp Suite Professional ($449/year — non-negotiable, needed for web testing)
- Kali Linux (pentesting OS, pre-loaded with tools)
- Python (for writing custom scripts and exploits)

**Web testing**:
- Burp Suite Pro (primary)
- OWASP ZAP (backup, free)
- Custom scripts for specific tasks

**Network testing**:
- Nmap (scanning)
- Responder/Impacket (Windows AD)
- BloodHound (AD attack paths)
- CrackMapExec (post-exploitation)
- Metasploit (exploitation framework)

**Mobile testing**:
- Frida (dynamic instrumentation)
- objection (mobile exploration)
- MobSF (static analysis)
- APKTool/jadx (Android reverse engineering)
- Hopper/Ghidra (iOS binary analysis)

**Cloud testing**:
- ScoutSuite (AWS/GCP/Azure review)
- Prowler (AWS security)
- kube-hunter (Kubernetes)

**Automation and reporting**:
- Custom Python scripts
- Serp/LaTeX for report generation
- Markdown + Pandoc for PDF conversion
- PwnDoc (pentest documentation)

### Building Your Methodology

Your methodology is your product. It needs to be:
1. Repeatable (you don't miss things)
2. Defensible (you can justify your coverage)
3. Efficient (you're profitable at your rate)

**Sample web app methodology outline**:
1. **Recon** (10% of time): Subdomain enumeration, tech stack identification, endpoint discovery
2. **Automated scanning** (10%): Burp Scanner, ZAP, custom scripts
3. **Manual testing** (60%): Auth, access control, injection, business logic, SSRF, XXE
4. **Exploitation** (10%): Prove vulnerabilities are exploitable (without causing damage)
5. **Reporting** (10%): Write findings, create PoCs, recommend fixes

## Report Writing

A pentest is only as good as its report. Clients judge you on the report quality.

### Excellent Report Structure

1. **Executive Summary** (1-2 pages)
   - Overview of engagement
   - Key findings (top 3-5 risks)
   - Risk score (overall, with comparison to industry)
   - Business impact of vulnerabilities
   - Recommendations (non-technical)

2. **Scope and Methodology** (1-2 pages)
   - What was tested (URLs, IPs, app versions)
   - What was out of scope
   - Testing dates and methodology
   - Tools used

3. **Finding Summary** (1 page)
   - Table with all findings, severity, status
   - Breakdown by severity (Critical, High, Medium, Low, Info)
   - Statistics (total findings, by category)

4. **Detailed Findings** (bulk of report)
   - Each finding on 2-4 pages:
     - Title and severity (with CVSS score)
     - Description (what it is, why it matters)
     - Proof of concept (step-by-step with screenshots)
     - Impact (what an attacker could do)
     - Remediation (specific, actionable fix)
     - References (OWASP, CWE, CVE)

5. **Retest Results** (if applicable)
   - What was fixed, what wasn't
   - Verification method
   - New issues discovered

### Report Template (Finding Section)

```
## [CVSS Score] [Severity] — [Finding Title]

**CWE**: [CWE-ID]
**OWASP**: [OWASP Category]
**Location**: [URL/Endpoint]

### Description
[Clear description of the vulnerability and its implications]

### Proof of Concept
1. Step 1
2. Step 2
3. [Screenshot showing the vulnerability]

### Impact
[What an attacker could achieve with this vulnerability]

### Remediation
[Specific, actionable recommendation for fixing this issue]

### References
- [Link to OWASP page]
- [Link to CWE]
```

## Building a Portfolio

### Without Clients

- **Bug bounty hunting**: Find vulnerabilities on HackerOne/Bugcrowd programs. Even one valid finding proves you can hack.
- **CTF write-ups**: Capture The Flag competitions. Write detailed walkthroughs.
- **Open-source tools**: Contribute to or build pentesting tools.
- **Personal projects**: Set up a vulnerable web app (DVWA, WebGoat) and document your testing process.
- **Blog**: Write about vulnerabilities you find, techniques you use.

### With Your First Client

- Document everything (with permission)
- Get a testimonial
- Write a case study (anonymized if needed)
- Use the report as a portfolio sample (redacted)

## Compliance-Driven Pentesting

### SOC 2 Pentesting

SOC 2 doesn't explicitly require pentesting, but it's expected as part of security monitoring. This is a growing market as more SaaS companies pursue SOC 2.

**What SOC 2 clients need**:
- Pentesting at least annually
- Coverage of critical systems
- Evidence of remediation

**Pricing**: $5-15K for SOC 2 scope

### PCI DSS Pentesting

PCI DSS explicitly requires pentesting (requirement 11). This is a steady, recurring market.

**What PCI DSS clients need**:
- External and internal network pentesting (11.1)
- Web application pentesting (11.3)
- Segmentation testing (11.3.4)
- Annual testing + after significant changes

**Pricing**: $5-15K for PCI DSS scope

### HIPAA Security Assessment

HIPAA requires a security risk analysis. Pentesting is part of this.

**Pricing**: $8-20K depending on scope

## Legal and Ethical Considerations

### Essential Legal Protections

1. **Get it in writing**: Statement of Work (SOW) with clear scope, rules of engagement, and out-of-bounds
2. **Insurance**: Professional liability insurance with cybersecurity coverage ($1-2M minimum)
3. **NDA**: Sign client's NDA or provide your own
4. **Permission**: Written authorization to test specific systems at specific times
5. **Data handling**: Never exfiltrate actual customer data. Use dummy data or metadata.
6. **Rules of engagement**: Define what's allowed (testing times, DoS, social engineering, etc.)

### Sample Rules of Engagement Clause

```
Rules of Engagement:
1. Testing limited to: [list IPs, URLs, app versions]
2. Testing hours: [times and timezone]
3. Prohibited actions: DoS attacks, social engineering without written approval,
   modification/deletion of production data, access to PII/PCI data
4. Communication: Findings reported immediately if critical
5. Escalation: [Name] is primary contact; [Name] is escalation for critical findings
6. Evidence: All evidence will be encrypted and deleted 90 days after engagement
```

## Quick-Start Action Plan

### Month 1-2: Skills and Certification
- [ ] Earn OSCP (or pass at least 3 HackTheBox/Proving Grounds machines)
- [ ] Set up your pentesting lab
- [ ] Develop your methodology (documented, repeatable)
- [ ] Create report template

### Month 3-4: Portfolio
- [ ] Find 3 valid vulnerabilities on bug bounty programs
- [ ] Write 3 detailed bug bounty write-ups
- [ ] Build a website with your services and past findings
- [ ] Write 5 blog posts about pentesting techniques

### Month 5-6: First Clients
- [ ] Network with compliance consultants (referrals)
- [ ] Send 20 cold emails to startups in regulated industries
- [ ] Offer first engagement at 50% discount (for portfolio/case study)
- [ ] Deliver exceptional report — get testimonial

### Month 7-12: Build Practice
- [ ] 3-5 engagements completed
- [ ] Raise rates to market level
- [ ] Build referral relationships
- [ ] Specialize (cloud, mobile, or specific industry)
- [ ] Speak at a security conference

## Final Word

Pentesting freelancing offers high rates, interesting work, and the satisfaction of making systems more secure. The barrier to entry is real — you need certifications, skills, and a portfolio to build trust — but the rewards are correspondingly high.

The key insight: Your report is your product. A mediocre pentester with excellent reports will outsell an excellent pentester with mediocre reports. Invest in your report writing.

Start with the OSCP, build your methodology, and find your first client through compliance referrals. The demand will only grow as more companies pursue security certifications and face regulatory requirements.
