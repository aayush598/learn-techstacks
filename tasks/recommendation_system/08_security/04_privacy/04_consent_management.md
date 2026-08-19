# Consent Management

## 1. Overview

Consent management captures, stores, and enforces user consent for data processing
activities. For recommendation systems, consent management is critical because personalization
requires processing user data that may be subject to privacy regulations. This document
covers consent collection UI, granular consent options, storage, withdrawal, ML processing
consent, and proof of consent.

### 1.1 Consent Requirements by Regulation

| Regulation | Consent Type | Requirements |
|---|---|---|
| GDPR | Explicit, informed | Freely given, specific, informed, unambiguous |
| CCPA | Opt-out | "Do Not Sell" link, GPC support |
| LGPD (Brazil) | Explicit | Similar to GDPR |
| POPIA (South Africa) | Consent or legitimate interest | Specific, informed |
| PIPEDA (Canada) | Meaningful consent | Clear, understandable |

---

## 2. Consent Collection UI

### 2.1 Consent Banner Design

```
┌────────────────────────────────────────────────────────────┐
│  We value your privacy                                      │
│                                                              │
│  We use cookies and similar technologies to provide you     │
│  with a personalized experience.                             │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Accept All       │  │  Customize        │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────────────────────────────┐              │
│  │  Reject Non-Essential                      │              │
│  └──────────────────────────────────────────┘              │
│                                                              │
│  Privacy Policy | Cookie Policy | Manage Preferences        │
└────────────────────────────────────────────────────────────┘
```

### 2.2 Consent Collection Flow

```
User Visits Site → Show Consent Banner → User Makes Choice → Record Consent → Apply Settings
                        ↓                      ↓                  ↓              ↓
                  Detect jurisdiction    Accept/Customize/     Store with     Enable/disable
                  (geo-IP)               Reject               timestamp      tracking
```

### 2.3 Consent UI Requirements

| Requirement | Implementation | Verification |
|---|---|---|
|平等呈现 | Accept and Reject buttons same size/prominence | UI audit |
| Clear language | Plain language, no legal jargon | Readability testing |
| Easy rejection | Reject as easy as accept (max 2 clicks) | UX testing |
| Granular options | Individual consent categories | Feature audit |
| No pre-checked boxes | All options unchecked by default | Automated testing |
| Accessible | WCAG 2.1 AA compliant | Accessibility audit |

### 2.4 Consent Banner Variations by Jurisdiction

| Jurisdiction | Default | Reject Option | Granularity |
|---|---|---|---|
| EU (GDPR) | No consent (opt-in) | Explicit reject button | Required by category |
| California (CCPA) | Opt-out available | "Do Not Sell" link | Required |
| Brazil (LGPD) | No consent (opt-in) | Explicit reject button | Required by category |
| Other | Varies | Best practice: opt-in | Recommended |

---

## 3. Granular Consent Options

### 3.1 Consent Categories for Recommendation Systems

| Category | Description | Default | Impact of Denial |
|---|---|---|---|
| Essential | Basic site functionality | Always on (no consent needed) | Site may not function |
| Analytics | Usage analytics and reporting | Off (consent required) | No analytics data |
| Personalization | Customized recommendations | Off (consent required) | Generic recommendations |
| Marketing | Promotional communications | Off (consent required) | No marketing messages |
| Third-party sharing | Data shared with partners | Off (consent required) | No third-party data |
| Cross-device | Link activity across devices | Off (consent required) | Per-device only |

### 3.2 Consent Configuration

```yaml
consent_categories:
  essential:
    required: true
    description: "Essential for site functionality"
    data_processing: ["authentication", "security", "session_management"]

  analytics:
    required: false
    description: "Help us improve our services"
    data_processing: ["usage_tracking", "performance_monitoring", "error_reporting"]

  personalization:
    required: false
    description: "Receive personalized recommendations"
    data_processing: ["behavior_tracking", "preference_learning", "recommendation_generation"]
    impact_note: "Without this, you'll see generic recommendations"

  third_party:
    required: false
    description: "Share data with trusted partners"
    data_processing: ["partner_analytics", "advertising", "content_syndication"]
    partners: ["Partner A", "Partner B", "Partner C"]
```

### 3.3 Progressive Consent

Allow users to provide consent incrementally:

1. **First visit**: Essential cookies only, prompt for consent
2. **Second visit**: Reminder if consent not provided
3. **Feature usage**: Request consent when feature requires it
4. **Settings page**: Always available for consent management

---

## 4. Consent Storage

### 4.1 Consent Record Schema

```json
{
  "consent_id": "consent_a1b2c3d4",
  "user_id": "usr_x9y8z7w6",
  "consent_version": "v2.1",
  "timestamp": "2026-01-15T10:30:00Z",
  "source": "web_banner",
  "jurisdiction": "EU",
  "ip_address": "192.168.1.100",
  "user_agent": "Mozilla/5.0...",
  "consents": {
    "essential": true,
    "analytics": true,
    "personalization": true,
    "marketing": false,
    "third_party": false,
    "cross_device": true
  },
  "method": "explicit_opt_in",
  "proof": {
    "banner_screenshot": "hash_of_screenshot",
    "consent_text_hash": "hash_of_text_shown",
    "interaction_log": ["banner_shown", "clicked_customize", "toggled_personalization", "clicked_accept"]
  }
}
```

### 4.2 Consent Storage Requirements

| Requirement | Implementation | Rationale |
|---|---|---|
| Immutable records | Append-only audit log | Prove consent history |
| Tamper-proof | Cryptographic signing | Prevent consent modification |
| Version control | Track consent policy versions | Prove what user consented to |
| Cross-device sync | Cloud-based consent store | Consistent consent across devices |
| Retention | Duration of relationship + legal period | Compliance evidence |

### 4.3 Consent Store Architecture

```
Consent Service:
├── API Layer: REST API for consent operations
├── Storage: Append-only database (audit trail)
├── Cache: Redis for fast consent lookups
├── Sync: Cross-device consent synchronization
└── Reporting: Compliance and analytics dashboards
```

---

## 5. Consent Withdrawal

### 5.1 Withdrawal Process

```
User Requests Withdrawal → Process Withdrawal → Update All Systems → Confirm
          ↓                      ↓                    ↓              ↓
   Via UI, email,        Remove consent         Propagate to     Notify user
   or support            record                 all systems      of completion
```

### 5.2 Withdrawal Requirements

| Requirement | Implementation | SLA |
|---|---|---|
| Easy as giving consent | Same number of clicks | Immediate |
| No penalty | No service degradation beyond consent scope | Immediate |
| Complete withdrawal | Remove data from all systems | 48 hours |
| Confirmation | Notify user of completion | Within 24 hours |
| Audit trail | Log withdrawal event | Immediate |

### 5.3 Partial Withdrawal

Users can withdraw specific consents while maintaining others:

| Withdrawal | Impact on Recommendation System |
|---|---|
| Withdraw analytics | Stop analytics tracking, recommendations unaffected |
| Withdraw personalization | Generic recommendations, analytics continues |
| Withdraw third-party | No data sharing, internal processing continues |
| Withdraw all | Minimal data processing, basic service only |

### 5.4 Withdrawal Propagation

After consent withdrawal, propagate to all systems:

```
Consent Withdrawal → Consent Service → Propagation Engine
                           ↓                    ↓
                    Update consent         ┌─────┼─────┐
                    record                 ↓     ↓     ↓
                                    Feature  Model  Analytics
                                    Store    Train  Service
                                    (stop)   (stop) (stop)
```

---

## 6. Consent for ML Processing

### 6.1 ML-Specific Consent

| ML Activity | Consent Required | Description |
|---|---|---|
| Model training on user data | Personalization consent | Using user interactions for training |
| Recommendation generation | Personalization consent | Generating personalized results |
| A/B testing | Analytics consent | Measuring algorithm performance |
| Feature computation | Personalization consent | Computing user-specific features |
| Model improvement | Personalization consent | Using feedback for model updates |

### 6.2 Consent-Aware ML Pipeline

```
User Data → Consent Check → Processing Decision
                ↓                    ↓
         ┌──────┼──────┐      ┌──────┼──────┐
         ↓      ↓      ↓      ↓      ↓      ↓
      Consent Given  Consent Denied
         ↓             ↓
      Process     Use Default/
      with user   Anonymous
      data        processing
```

### 6.3 Consent in Feature Store

| Consent Status | Feature Store Behavior |
|---|---|
| Full consent | Serve personalized features |
| Partial consent | Serve only consented feature types |
| No consent | Serve only anonymous/default features |
| Withdrawn | Remove user features, serve defaults |

---

## 7. Proof of Consent

### 7.1 Proof of Consent Requirements

| Element | Purpose | Storage |
|---|---|---|
| Consent text shown | Prove what user agreed to | Hashed version |
| Timestamp | Prove when consent was given | Append-only log |
| User identity | Prove who gave consent | User ID reference |
| Consent method | Prove how consent was obtained | Interaction log |
| Banner screenshot | Visual proof of consent UI | Image hash |
| Policy version | Prove which policy version | Version reference |

### 7.2 Consent Audit Trail

Every consent event is logged:

```
Consent Audit Events:
├── consent_given: User provided consent
├── consent_updated: User changed consent preferences
├── consent_withdrawn: User withdrew consent
├── consent_expired: Consent expired per policy
├── consent_refreshed: User re-confirmed consent
└── consent_breach: Unauthorized data processing detected
```

### 7.3 Compliance Reporting

| Report | Frequency | Audience | Content |
|---|---|---|---|
| Consent summary | Weekly | Privacy team | Consent rates, changes |
| Withdrawal report | Monthly | Legal | Withdrawal reasons, timing |
| Compliance audit | Quarterly | Regulators | Full consent compliance |
| Data processing audit | Annual | External auditor | Processing vs consent alignment |
