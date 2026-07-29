# Data Processing Agreement (DPA) Template

## DISCLAIMER
This is a template for reference. It does not constitute legal advice. Have it reviewed by a qualified attorney.

---

# DATA PROCESSING AGREEMENT

**Last Updated: [Date]**

## 1. Parties

This Data Processing Agreement ("DPA") forms part of the Terms of Service (the "Agreement") between:

**Data Controller (Customer):**
[Customer Company Name]
[Address]
[Contact Email]

**Data Processor (Company):**
[Company Name]
[Address]
[Contact Email: privacy@company.com]

## 2. Definitions

- **"Data Controller"** means the entity that determines the purposes and means of processing Personal Data.
- **"Data Processor"** means the entity that processes Personal Data on behalf of the Data Controller.
- **"Personal Data"** means any information relating to an identified or identifiable natural person.
- **"Processing"** means any operation performed on Personal Data.
- **"Data Subject"** means the identified or identifiable person to whom Personal Data relates.
- **"GDPR"** means the EU General Data Protection Regulation (2016/679).
- **"CCPA"** means the California Consumer Privacy Act.
- **"Standard Contractual Clauses (SCCs)"** means the EU-approved standard contractual clauses for data transfers.
- **"Sub-processor"** means a third party engaged by the Data Processor to process Personal Data.
- **"Data Breach"** means a breach of security leading to destruction, loss, alteration, unauthorized disclosure of, or access to Personal Data.

## 3. Scope and Purpose

### 3.1 Purpose
The Data Processor will process Personal Data on behalf of the Data Controller to provide the Service described in the Agreement.

### 3.2 Duration
Processing will occur during the term of the Agreement plus any post-termination data retention period.

### 3.3 Nature of Processing
The Data Processor provides SaaS [Product] which processes Personal Data as part of the Service.

### 3.4 Categories of Data Subjects
- Authorized Users of the Data Controller
- End users/customers of the Data Controller (as applicable)
- Any individuals whose data is uploaded to the Service by Data Controller

### 3.5 Types of Personal Data Processed
- Name, email address, job title
- Account credentials
- Usage data and logs
- Any other data uploaded by Data Controller

## 4. Processor Obligations

The Data Processor agrees to:

### 4.1 Compliance
Process Personal Data only on documented instructions from the Data Controller, unless required by law.

### 4.2 Confidentiality
Ensure all personnel authorized to process Personal Data are bound by confidentiality obligations.

### 4.3 Security
Implement appropriate technical and organizational security measures.

### 4.4 Sub-processors
Not engage another processor without prior authorization.

### 4.5 Assistance
Assist the Data Controller in responding to Data Subject requests and ensuring compliance.

### 4.6 Breach Notification
Notify the Data Controller of any Data Breach without undue delay.

### 4.7 Data Deletion
Delete or return all Personal Data after termination of the Service.

### 4.8 Audit
Make available information necessary to demonstrate compliance.

## 5. Data Subject Rights

### 5.1 Cooperation
The Data Processor will assist the Data Controller in fulfilling obligations to respond to Data Subject requests under GDPR and other applicable laws.

### 5.2 Process for Requests
- Data Controller notifies Data Processor of a Data Subject request
- Data Processor responds within [72] hours with available options
- Data Processor implements required actions within [30] days
- No additional fee for reasonable requests

### 5.3 Types of Requests Covered
- Access requests
- Correction requests
- Deletion requests ("right to be forgotten")
- Data portability requests
- Objection to processing
- Restriction of processing

## 6. Security Measures

### 6.1 Technical Measures
- Access controls and authentication mechanisms
- Encryption of Personal Data at rest (AES-256) and in transit (TLS 1.2+)
- Network security controls and firewalls
- Intrusion detection and prevention systems
- Regular vulnerability assessments and penetration testing
- Secure development lifecycle
- Logging and monitoring systems
- Backup and disaster recovery procedures

### 6.2 Organizational Measures
- Data protection policies and procedures
- Employee training on data protection
- Background checks for employees with data access
- Incident response plan
- Regular compliance reviews

## 7. Sub-processors

### 7.1 Authorized Sub-processors
The Data Controller authorizes the following sub-processors:

| Sub-processor | Service | Location | Purpose |
|--------------|---------|----------|---------|
| [AWS / GCP / Azure] | Cloud Infrastructure | [US/EU] | Data hosting |
| [Stripe / Paddle] | Payment Processing | [US/EU] | Payment data |
| [SendGrid / Mailgun] | Email Delivery | [US/EU] | Service emails |
| [Sentry / Datadog] | Error Monitoring | [US/EU] | Error tracking |

### 7.2 Notification of New Sub-processors
The Data Processor will notify the Data Controller [30] days before engaging any new sub-processor.

### 7.3 Objection Right
The Data Controller may object to a new sub-processor within [15] days of notification. If reasonable objection cannot be resolved, the Data Controller may terminate the Agreement.

## 8. Data Transfers

### 8.1 Transfer Safeguards
For transfers of Personal Data from the EEA to countries not deemed adequate by the European Commission, the parties rely on Standard Contractual Clauses (SCCs) as approved by the European Commission.

### 8.2 SCCs
The SCCs are incorporated by reference and take precedence over any conflicting provision in this DPA.

### 8.3 Transfer Mechanism
Data transfers are governed by:
- EU Standard Contractual Clauses (Module 2: Controller-to-Processor)
- UK Addendum to the EU SCCs (for UK transfers)
- Swiss Federal Data Protection Act (for Swiss transfers)

## 9. Data Breach Notification

### 9.1 Notification
The Data Processor will notify the Data Controller without undue delay (and within [72] hours) after becoming aware of a Data Breach.

### 9.2 Notification Contents
Notification will include:
- Description of the Data Breach
- Categories and approximate number of Data Subjects affected
- Categories and approximate amount of Personal Data affected
- Likely consequences of the Data Breach
- Measures taken or proposed to address the Data Breach
- Contact information for further information

### 9.3 Data Controller Obligations
The Data Controller is responsible for notifying supervisory authorities and Data Subjects as required by applicable law.

## 10. Data Retention and Deletion

### 10.1 Retention Period
The Data Processor will retain Personal Data for the duration of the Agreement plus [90] days post-termination.

### 10.2 Deletion
Within [90] days of termination, the Data Processor will delete all Personal Data from its systems, unless applicable law requires retention.

### 10.3 Deletion Certification
At the Data Controller's request, the Data Processor will provide written certification of deletion.

## 11. Audit Rights

### 11.1 Right to Audit
The Data Controller may audit the Data Processor's compliance with this DPA, at the Data Controller's expense, no more than once per [12] months.

### 11.2 Audit Process
- Data Controller provides [30] days notice
- Audit conducted during business hours
- Data Processor's premises and systems
- Use of independent third-party auditor (mutually agreed)
- Confidentiality agreement required

### 11.3 SOC 2 Reports
In lieu of an on-site audit, the Data Processor may provide its most recent SOC 2 Type II report or equivalent certification.

## 12. Liability

### 12.1 Liability Cap
Each party's liability under this DPA is subject to the liability limitations in the Agreement.

### 12.2 Direct Damages
Each party is liable for damages caused by its breach of this DPA.

### 12.3 Indemnification
The Data Processor indemnifies the Data Controller for claims arising from the Data Processor's breach of this DPA.

## 13. Termination

### 13.1 Termination for Breach
Either party may terminate this DPA if the other party materially breaches and fails to cure within [30] days.

### 13.2 Suspension
If the Data Processor believes an instruction from the Data Controller violates applicable law, it may suspend processing pending clarification.

### 13.3 Effect of Termination
On termination, the Data Processor will delete or return all Personal Data as directed by the Data Controller.

## 14. Governing Law

This DPA is governed by the laws of [Ireland / Netherlands / State] (EU Member State for GDPR purposes).

## 15. Contact Information

**Data Processor:**
[Company Name]
[Address]
[Email: privacy@company.com]
[Phone: (555) 123-4567]

**Data Protection Officer (if required):**
[Name]
[Email: dpo@company.com]

## APPENDIX A: Description of Processing Activities

**Data Controller:**
- Name: [Customer Company]
- Contact: [Customer Contact]
- Activities: [Customer's business activities]

**Data Processor:**
- Name: [Company Name]
- Contact: [Company Contact]
- Activities: Providing [Product] SaaS platform

**Processing Details:**
- Purpose: Providing SaaS Service
- Categories of Data Subjects: Authorized users, end customers
- Categories of Personal Data: Names, emails, usage data
- Retention Period: Term + 90 days
- Location of Processing: [AWS region / data center location]

## APPENDIX B: Technical and Organizational Security Measures

1. **Access Control:** Role-based access, MFA, least privilege
2. **Data Encryption:** AES-256 at rest, TLS 1.2+ in transit
3. **Network Security:** Firewalls, WAF, DDoS protection
4. **Monitoring:** 24/7 monitoring, intrusion detection
5. **Incident Response:** Documented IR plan, tested quarterly
6. **Backup:** Daily automated backups, weekly full backups
7. **Disaster Recovery:** RPO [4 hours], RTO [24 hours]
8. **Vulnerability Management:** Quarterly scans, annual pen testing
9. **Development Security:** Code review, SAST, dependency scanning
10. **Personnel Security:** Background checks, confidentiality agreements, annual training

## APPENDIX C: Sub-processor Notification Process

1. Data Processor identifies need for new sub-processor
2. Data Processor emails Data Controller at [customer contact email]
3. Notification includes: sub-processor name, service, location, purpose
4. Data Controller has 15 days to object
5. If no objection, sub-processor engagement proceeds
6. If objection, parties discuss in good faith for 30 days
7. If unresolved, Data Controller may terminate affected services

---

*This DPA template is provided for reference. Have it reviewed by a qualified attorney before use. Data protection laws vary by jurisdiction.*
