# Section 01: Multi-Factor Authentication (MFA)

Multi-factor authentication adds a second verification layer beyond passwords, requiring users to provide something they know (password) and something they have (TOTP, SMS code, hardware key). MFA reduces account takeover risk by 99.9% and is mandatory for admin accounts and recommended for all users.

MFA methods: TOTP (Time-based One-Time Password via authenticator apps like Google Authenticator, Authy), SMS codes (fallback, sent to verified phone), backup codes (10 one-time use codes for recovery), and hardware security keys (WebAuthn/FIDO2 for phishing-resistant auth). The system enforces at least one configured method before requiring MFA on login.

MFA enrollment flow: user enables MFA in settings → scans QR code for TOTP → enters verification code to confirm → optionally configures backup methods → generates backup codes. Subsequent logins: password → MFA challenge → session token issued. Remember device cookies (trusted for 30 days) reduce MFA frequency on trusted devices.
