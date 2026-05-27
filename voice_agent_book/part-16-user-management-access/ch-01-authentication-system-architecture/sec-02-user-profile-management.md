# Section 02: User Profile Management

User profiles store identity information, preferences, and account settings. Each user has a profile within their tenant context. Profile fields include: basic info (name, email, phone, avatar), contact preferences (email notifications, SMS alerts, in-app notifications), localization (timezone, language, date format), and security settings (MFA, password, sessions).

Profile API: GET /users/me (current user profile), PATCH /users/me (update profile fields), POST /users/me/avatar (upload avatar, stored in object storage with CDN URL), GET /users/me/preferences (user-specific settings). Profile fields can be extended with custom fields defined by tenant admins.

Profile validation: email uniqueness (per tenant), phone format validation (libphonenumber), avatar upload restrictions (max 2MB, PNG/JPG/WebP, 500×500px). Profile changes are audited. Users can view their profile, recent activity, and active sessions from the profile page. GDPR: users can download their profile data in JSON format.
