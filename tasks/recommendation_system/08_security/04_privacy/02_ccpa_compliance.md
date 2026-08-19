# CCPA Compliance

## 1. Overview

The California Consumer Privacy Act (CCPA) and its amendment (CPRA) grant California
residents specific rights over their personal information. For recommendation systems
that process user data for personalization, CCPA compliance is mandatory. This document
covers consumer rights implementation, opt-out mechanisms, data sale restrictions, privacy
notice requirements, data inventory, and employee training.

### 1.1 CCPA Applicability

CCPA applies to businesses that:

| Criterion | Threshold |
|---|---|
| Annual gross revenue | > $25 million |
| Personal information processed | > 100,000 consumers/households |
| Revenue from data sales | > 50% of annual revenue from selling PI |

### 1.2 CCPA vs CPRA Key Differences

| Aspect | CCPA (2020) | CPRA (2023+) |
|---|---|---|
| Consumer rights | Know, delete, opt-out | + Correct, limit use |
| Data sale opt-out | Opt-out of sale | + Opt-out of sharing |
| Enforcement | AG + private right | + CPPA enforcement |
| Sensitive data | Limited protection | + Specific protections |
| Risk assessments | Not required | + Required for high-risk processing |

---

## 2. Consumer Rights

### 2.1 Right to Know

Consumers can request disclosure of personal information collected about them.

**Data categories to disclose:**

| Category | Examples | Retention Period |
|---|---|---|
| Identifiers | Name, email, IP, device ID | Account lifetime |
| Commercial information | Purchase history, preferences | 3 years |
| Internet activity | Browsing history, clicks, search | 1 year |
| Geolocation | City-level location | 90 days |
| Inferences | Predicted preferences, segments | Account lifetime |
| Sensitive PI | SSN, precise location, health | Minimized collection |

**Implementation:**

```
Consumer Request → Identity Verification → Data Collection → Format Response → Deliver
       ↓                   ↓                    ↓                ↓              ↓
   Submit via        Verify identity      Query all data     Format per      Secure
   portal/email      (2FA, account)       sources            CCPA spec       delivery
```

### 2.2 Right to Delete

Consumers can request deletion of their personal information.

**Deletion requirements:**

- Delete from all systems (primary, backup, cache, analytics)
- Instruct service providers to delete
- Retain only legally required records
- Complete deletion within 45 days (extendable to 90)
- Confirm deletion to consumer

**Deletion scope:**

```
Deletion Scope:
├── Primary databases (user profiles, interactions)
├── Feature stores (computed features)
├── Analytics databases (aggregated data)
├── Backup systems (within retention cycle)
├── Cache layers (Redis, CDN)
├── Search indices (Elasticsearch)
├── ML training data (retrain without deleted data)
└── Third-party copies (notify service providers)
```

### 2.3 Right to Opt-Out

Consumers can opt-out of the sale or sharing of their personal information.

**Opt-out implementation:**

- **Do Not Sell/Share link** on every page
- **Global Privacy Control (GPC)** signal support
- **Cookie consent banner** with opt-out option
- **API endpoint** for programmatic opt-out
- **Universal opt-out mechanism** support

### 2.4 Right to Correct

Consumers can request correction of inaccurate personal information.

### 2.5 Right to Limit Use

Consumers can limit use and disclosure of sensitive personal information.

---

## 3. Opt-Out Mechanisms

### 3.1 Do Not Sell/Share

```
Implementation Requirements:
1. "Do Not Sell or Share My Personal Information" link in footer
2. Clicking link immediately opts user out
3. No confirmation required (one-click opt-out)
4. Opt-out preference stored in user profile
5. Opt-out respected across all data processing
6. GPC signal automatically treated as opt-out
```

### 3.2 GPC (Global Privacy Control) Support

| Browser/Signal | Detection Method | Response |
|---|---|---|
| GPC header | `Sec-GPC: 1` header | Honor as opt-out |
| Do Not Track | `DNT: 1` header | Check CCPA applicability |
| Privacy setting | Browser privacy settings | Respect per platform |

### 3.3 Opt-Out for Recommendation System

When a user opts out of data sharing:

| Data Processing | Impact | Action |
|---|---|---|
| Personalized recommendations | May continue (not a "sale") | Continue with restrictions |
| Third-party data sharing | Must stop immediately | Remove from all shared datasets |
| Cross-device tracking | Must stop | Unlink device identifiers |
| Analytics sharing | Must stop | Remove from shared analytics |
| Advertising data | Must stop | Remove from ad partner data |

---

## 4. Data Sale Restrictions

### 4.1 What Constitutes a "Sale"?

Under CCPA, "sale" includes:

- Transferring PI for monetary compensation
- Transferring PI for "other valuable consideration"
- Making PI available to third parties for cross-context behavioral advertising

### 4.2 Recommendation System Data Sales

| Data Type | Sale Status | Required Action |
|---|---|---|
| User interaction data shared with partners | Sale | Opt-out required |
| Anonymized aggregate data | Not a sale | No restriction |
| Data used by own recommendation engine | Not a sale | No restriction |
| Data shared for co-marketing | Sale | Opt-out required |
| Data shared with analytics providers | Depends on contract | Review agreements |

### 4.3 Service Provider vs Third Party

| Relationship | CCPA Definition | Obligations |
|---|---|---|
| Service provider | Processes PI on behalf of business | Contractual restrictions, no independent use |
| Third party | Receives PI for own purposes | Must provide opt-out, disclosure required |
| Contractor | Processes PI for specific business purpose | Contractual restrictions, limited use |

---

## 5. Privacy Notice Requirements

### 5.1 Required Disclosures

| Disclosure | Content | Location |
|---|---|---|
| Categories of PI collected | List all categories | Privacy policy |
| Purpose of collection | Why each category is collected | Privacy policy |
| Categories of PI shared | Who receives PI and why | Privacy policy |
| Consumer rights | How to exercise rights | Privacy policy + dedicated page |
| Financial incentive | Any rewards for PI collection | Privacy policy |
| Data retention | How long each category is retained | Privacy policy |

### 5.2 Just-in-Time Notice

For recommendation-specific data collection:

| Collection Point | Notice Required | Content |
|---|---|---|
| Account creation | Yes | What data collected, how used |
| First recommendation request | Yes | Behavioral tracking disclosure |
| Location request | Yes | Why location needed, how used |
| Cross-device linking | Yes | How devices linked, opt-out option |

### 5.3 Privacy Policy Updates

- Review privacy policy quarterly
- Update within 30 days of material changes
- Notify users of material changes 30 days in advance
- Maintain version history of all policy changes
- Make previous versions accessible

---

## 6. Data Inventory

### 6.1 Data Inventory Requirements

| Data Element | Required Information |
|---|---|
| Data category | CCPA category classification |
| Collection source | How the data was collected |
| Business purpose | Why the data is collected |
| Retention period | How long the data is kept |
| Third-party sharing | Who receives the data |
| Sale status | Whether the data is sold |
| Security measures | How the data is protected |

### 6.2 Recommendation System Data Inventory

| Data Type | Category | Purpose | Retention | Shared | Sold |
|---|---|---|---|---|---|
| User profiles | Identifiers | Personalization | Account lifetime | No | No |
| Click history | Internet activity | Feature computation | 1 year | No | No |
| Purchase history | Commercial | Recommendation training | 3 years | No | No |
| Device info | Identifiers | Cross-device linking | 90 days | No | No |
| Location | Geolocation | Context recommendations | 30 days | No | No |
| Inferences | Inferences | Personalization | Account lifetime | No | No |

### 6.3 Data Inventory Maintenance

- **Automated discovery**: Scan databases for PI patterns
- **Change tracking**: Detect new data collection automatically
- **Quarterly review**: Manual review of inventory accuracy
- **Annual audit**: Full audit by privacy team
- **Cross-reference**: Compare inventory against actual data flows

---

## 7. Employee Training

### 7.1 Training Requirements

| Audience | Training | Frequency | Duration |
|---|---|---|---|
| All employees | CCPA awareness | Annual | 1 hour |
| Engineering | Privacy by design | Annual | 4 hours |
| Data team | Data handling & minimization | Annual | 4 hours |
| Customer support | Consumer rights handling | Annual | 2 hours |
| Legal/compliance | CCPA regulatory updates | Semi-annual | 4 hours |
| Leadership | Privacy risk & governance | Annual | 2 hours |

### 7.2 Training Topics

- CCPA consumer rights and business obligations
- Privacy by design principles
- Data minimization practices
- Secure data handling procedures
- Breach notification requirements
- Consumer request handling process
- Privacy impact assessment process
- Consequences of non-compliance

### 7.3 Training Effectiveness

- **Pre/post assessments**: Measure knowledge improvement
- **Phishing simulations**: Test security awareness
- **Compliance audits**: Verify training completion
- **Incident analysis**: Review if incidents relate to training gaps
- **Continuous updates**: Regular communications about privacy news
