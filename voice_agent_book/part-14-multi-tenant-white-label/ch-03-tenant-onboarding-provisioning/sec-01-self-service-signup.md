# Section 01: Self-Service Signup Flow

## Overview

The self-service signup flow is the primary acquisition funnel for a voice agent SaaS platform. It must balance conversion rate optimization with fraud prevention, data collection requirements with friction minimization, and speed with proper tenant provisioning. A well-designed signup flow guides prospects through tenant creation, email verification, initial configuration, and first-time use within minutes, while collecting the minimum information needed to create a functional tenant environment.

The signup flow consists of sequential stages: account creation (email + password), email verification, tenant configuration (company name, use case), plan/tier selection, payment method collection (if required), and initial setup wizard. Each stage should save progress to allow users to resume if they abandon mid-flow. Progressive profiling collects additional information over time rather than demanding everything at signup.

For a multi-tenant voice agent platform, the signup flow also creates the tenant record, provisions the tenant's database space (shared, schema, or dedicated depending on plan), creates the first admin user, sets default configuration and feature flags, and triggers the welcome automation sequence. This entire process should complete within seconds for self-service tiers.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Canvas   |--->| Node     |--->| Edge     |--->| Validator|--->| Serializ |
| (React   |    | Registry |    | Router   |    | (cycle   |    | ation    |
|  Flow)   |    | (types)  |    | (condit) |    |  detect) |    | (JSON)   |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

**Decision 1: Email-first signup vs SSO.** Start with email+password for self-service. Add SSO/GitHub/Google as social login options in the signup form. Email-first provides wider reach; social login improves conversion.

**Decision 2: Credit card at signup vs trial.** For free trial tiers, do NOT require a credit card at signup. This maximizes signup conversion. Require payment method only for plan upgrades or after trial expiry.

**Decision 3: Tenant creation is async.** Create the tenant record synchronously but provision infrastructure asynchronously. Show a provisioning spinner or progress bar. This keeps signup fast while allowing complex provisioning to complete in the background.

## Integration Points

- **Auth System (Part 16):** User account creation, email verification, password hashing
- **Provisioning Pipeline (Sec 02):** Tenant infrastructure provisioning triggered after signup
- **Email Service (Part 20):** Welcome emails, verification codes, onboarding sequence
- **Billing (Part 17):** Plan selection creates Stripe customer and subscription
- **Analytics:** Signup funnel tracking, conversion metrics, drop-off analysis

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Spam/Abuse Prevention:** Implement rate limiting on signup attempts (3 per email, 10 per IP per hour), email domain validation (disposable email blocking), and CAPTCHA (Turnstile or reCAPTCHA v3).
- **Email Deliverability:** Use dedicated sending domains, SPF/DKIM/DMARC configuration, and warm up sending reputation. Monitor bounce rates and spam complaints per email provider.
- **Signup Abandonment:** Track which stage users abandon. Optimize the highest-drop-off stages. Send abandoned-cart-style recovery emails if the user completed email verification but didn't finish setup.
- **Provisioning Speed:** Target <5 seconds for shared-tier provisioning. Schema and dedicated tiers may take 30-60 seconds. Show a real-time progress indicator for longer provisioning.
- **Multi-Language Support:** Offer signup in the user's detected language. This is critical for global SaaS. Use browser Accept-Language header detection with manual override.
- **GDPR Compliance:** Include privacy policy and terms of service checkboxes. Collect consent for marketing communications separately. Store consent records with timestamps.
