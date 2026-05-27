# Section 01: Self-Service Registration

Self-service registration allows new users to create accounts without manual approval. The registration flow collects essential information (email, name, password), verifies the email address, and provisions the user account. For multi-tenant platforms, registration can create a new tenant or join an existing one.

Registration flow: user clicks "Sign Up" → enters email, name, password → email verification (send 6-digit code) → verify code → create user record → create tenant (if self-service) or request to join existing tenant → welcome email → redirect to onboarding. Progressive profiling: collect minimal info first, request more during onboarding (company name, phone, payment method).

Validation: email format validation, email domain blocklist (disposable email domains), password strength check, rate limiting (max 3 registrations per email per hour), CAPTCHA (reCAPTCHA v3), and duplicate detection (existing account with same email → suggest login). Post-registration: welcome tour, first-agent creation prompt, documentation links.
