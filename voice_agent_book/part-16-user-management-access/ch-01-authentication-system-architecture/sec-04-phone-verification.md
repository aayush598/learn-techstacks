# Section 04: Phone Number Verification

Phone number verification confirms the user's phone for SMS notifications, MFA fallback, and caller ID configuration. The verification process sends a one-time code via SMS and validates the user's response. Phone numbers are formatted and stored in E.164 format.

Verification flow: user enters phone number → system validates format (libphonenumber) → sends SMS with 6-digit code → user enters code → system verifies (code matches, not expired) → phone marked verified → phone number stored (encrypted at rest). Resend cooldown: 60 seconds. Max attempts: 5 per phone per hour.

Integration: SMS delivery via Twilio/Vonage/Amazon SNS. Delivery tracking: verify SMS was delivered (delivery receipt webhook). If SMS fails, offer voice call fallback (call phone number, speak code). Phone number verification is required for: SMS-based MFA, caller ID configuration, and outbound call routing.
