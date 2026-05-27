# Section 02: SSO / SAML / OIDC Integration

Single Sign-On (SSO) allows users to authenticate using their organization's identity provider (IdP) via SAML 2.0 or OpenID Connect (OIDC). SSO streamlines user management for enterprise tenants: users are provisioned/deprovisioned from the IdP, and the platform never handles passwords for those users.

SAML 2.0 flow: user clicks "Login with SSO" → redirected to IdP login page → IdP authenticates → SAML assertion POSTed back to platform → assertion verified (signature, audience, expiry) → user mapped to tenant → session created. Metadata exchange: platform provides ACS URL and entity ID; tenant provides IdP metadata URL or XML.

OIDC flow: user clicks SSO login → platform redirects to IdP's authorization endpoint → user authenticates → IdP redirects with authorization code → platform exchanges code for ID token and access token → ID token verified (signature via JWKS, issuer, audience) → user authenticated. OIDC supports refresh tokens for long-lived sessions.

SCIM integration for user provisioning: when users are added/removed in the IdP, SCIM calls create/update/delete user accounts on the platform. This automates onboarding and offboarding for enterprise tenants.
