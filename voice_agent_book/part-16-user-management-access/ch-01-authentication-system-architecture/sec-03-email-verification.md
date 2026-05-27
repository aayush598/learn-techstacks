# Section 03: Email Verification & Confirmation

Email verification ensures the user controls the email address they registered with. Unverified accounts have restricted access (cannot create agents, cannot make calls). Verification methods: email with verification link (click to verify, expires in 24 hours) and email with verification code (6-digit code, expires in 10 minutes).

Verification flow: user registers → system sends verification email with unique token (crypto.randomBytes(32), hex) → user clicks link → token validated (exists, not expired, not used) → email marked verified → user granted full access → confirmation page shown. If token expired, user can request new verification email. Resend rate limited: max 3 per hour.

Security: verification tokens are single-use (invalidated after successful verification). Token hashing: stored as SHA-256 in database. Email change requires verification of the new email (send verification to new address) and confirmation from old email (notification that email was changed). Unverified accounts are automatically cleaned up after 7 days.
