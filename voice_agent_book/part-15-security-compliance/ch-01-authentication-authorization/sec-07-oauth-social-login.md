# Section 07: OAuth 2.0 / Social Login

OAuth 2.0 enables users to authenticate via social providers (Google, GitHub, Microsoft) or third-party identity services. The platform acts as an OAuth client, handling the authorization code flow to obtain user identity information. Social login reduces friction for self-service signup and is often preferred for lower-tier plans.

OAuth flow: user clicks "Login with Google" → platform redirects to Google's authorization endpoint with client_id, redirect_uri, scope, and state parameter → user consents → Google redirects with authorization code → platform exchanges code for access token and ID token → platform verifies ID token (JWT signature, issuer, audience) → extracts user info (email, name, avatar) → links to existing account or creates new.

Multiple providers can be linked to a single account, allowing users to authenticate with any of their configured providers. Account linking requires email verification to prevent account takeover. Social login is implemented using the Passport.js middleware with provider-specific strategies.
