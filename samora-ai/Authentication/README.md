# Authentication Interview Questions and Answers

## Q1: What is Authentication?
**A:** Authentication is the process of verifying the identity of a user, system, or entity. It ensures that the entity is who they claim to be by validating credentials such as passwords, biometrics, tokens, or certificates.

## Q2: What is the difference between Authentication and Authorization?
**A:** Authentication verifies **who** you are (identity), while Authorization determines **what** you are allowed to do (permissions). Authentication always comes before authorization. For example, logging in with a password is authentication; being granted access to a specific page after login is authorization.

## Q3: What are the three main factors of authentication?
**A:** The three factors are: (1) **Something you know** – passwords, PINs, security questions; (2) **Something you have** – smart cards, security tokens, mobile devices; (3) **Something you are** – biometrics like fingerprints, facial recognition, iris scans.

## Q4: What is Multi-Factor Authentication (MFA)?
**A:** MFA is a security system that requires two or more authentication factors from different categories to verify a user's identity. For example, combining a password (something you know) with a one-time code sent to your phone (something you have).

## Q5: What is Two-Factor Authentication (2FA)?
**A:** 2FA is a subset of MFA that uses exactly two distinct authentication factors. Common implementations include password + SMS code, password + authenticator app TOTP, or password + hardware security key.

## Q6: What is Single Sign-On (SSO)?
**A:** SSO is an authentication scheme that allows a user to log in once and gain access to multiple independent systems or applications without being prompted to log in again. It uses a central authentication server that issues tokens trusted by all connected services.

## Q7: What is OAuth 2.0?
**A:** OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts on an HTTP service. It works by delegating user authentication to the service that hosts the user account and authorizing third-party applications to access that account. It is not an authentication protocol but is often used for authentication.

## Q8: What is OpenID Connect (OIDC)?
**A:** OpenID Connect is an identity layer built on top of OAuth 2.0. While OAuth 2.0 is about authorization, OIDC adds authentication. It allows clients to verify the identity of the end-user based on the authentication performed by an authorization server, obtaining basic profile information in an ID token (JWT).

## Q9: What is a JWT (JSON Web Token)?
**A:** JWT is a compact, URL-safe token format used for representing claims between two parties. It consists of three parts: header (algorithm and token type), payload (claims/data), and signature (created by combining the header, payload, and a secret). JWTs are commonly used for authentication and information exchange.

## Q10: How does JWT authentication work?
**A:** The user logs in with credentials; the server validates them and generates a JWT signed with a secret. The client stores the JWT (typically in localStorage or an HTTP-only cookie) and sends it in the Authorization header for subsequent requests. The server verifies the signature and extracts user information from the payload without needing a database lookup.

## Q11: What is a session-based authentication?
**A:** Session-based authentication stores session data on the server. When a user logs in, the server creates a session, stores it in memory/database, and returns a session ID to the client (usually via a cookie). The client sends the session ID with each request, and the server looks up the session to identify the user.

## Q12: What is token-based authentication?
**A:** Token-based authentication uses tokens (like JWTs) that contain user information and are cryptographically signed. The server does not need to store session data — it only needs to verify the token's signature. This makes token-based authentication stateless and more scalable.

## Q13: What are the advantages of token-based authentication over session-based?
**A:** (1) Stateless — no server-side storage needed; (2) Scalable — tokens work across multiple servers/domains easily; (3) Mobile-friendly — works well with native mobile apps; (4) Performance — no database lookup for each request; (5) CORS-friendly — tokens can be sent via headers.

## Q14: What is a refresh token?
**A:** A refresh token is a long-lived token used to obtain new access tokens without requiring the user to re-authenticate. Access tokens are short-lived (e.g., 15 minutes), while refresh tokens can last days or months. Refresh tokens are stored securely and rotated periodically.

## Q15: What is an access token?
**A:** An access token is a credential used to access protected resources. It is typically short-lived (minutes to hours) and contains information about the user and their permissions. It is sent with each API request in the Authorization header.

## Q16: How should you store tokens on the client side?
**A:** The most secure approach is using HTTP-only Secure SameSite cookies, which prevent XSS attacks from stealing tokens. Alternatively, tokens can be stored in memory (most secure for SPAs). localStorage/sessionStorage are convenient but vulnerable to XSS attacks.

## Q17: What is a CSRF attack and how does it relate to authentication?
**A:** Cross-Site Request Forgery (CSRF) is an attack that tricks a user into executing unwanted actions on a web application where they are authenticated. It exploits the fact that browsers automatically include cookies with requests. Protection includes CSRF tokens, SameSite cookies, and checking Origin/Referer headers.

## Q18: What is an XSS attack in the context of authentication?
**A:** Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users. In authentication contexts, XSS can steal tokens from localStorage, session cookies (if not HTTP-only), or capture keystrokes to steal passwords. HTTP-only cookies and input sanitization help prevent this.

## Q19: What is a brute force attack on authentication?
**A:** A brute force attack attempts to gain access by systematically trying all possible passwords or credentials until the correct one is found. Mitigations include account lockout policies, rate limiting, CAPTCHA, and using strong password policies.

## Q20: What is a dictionary attack?
**A:** A dictionary attack is a type of brute force attack that uses a list of common passwords, words from dictionaries, and previously leaked passwords instead of trying all possible combinations. It is more efficient than a pure brute force attack.

## Q21: What is password hashing and why is it important?
**A:** Password hashing is the process of converting a plain-text password into a fixed-length string using a one-way cryptographic function. It is important because even if the database is breached, attackers cannot recover the original passwords. Hashing is different from encryption — hashing is irreversible.

## Q22: What are the best hashing algorithms for passwords?
**A:** The recommended algorithms are bcrypt, Argon2 (winner of the Password Hashing Competition), scrypt, and PBKDF2. These are designed to be slow and computationally expensive, making brute force attacks difficult. Argon2 is considered the most secure option currently.

## Q23: What is a salt in password hashing?
**A:** A salt is a random, unique value added to each password before hashing. It ensures that even if two users have the same password, their hashes will be different. Salts prevent rainbow table attacks and make precomputation attacks impractical.

## Q24: What is a pepper in password hashing?
**A:** A pepper is a secret, fixed value added to passwords before hashing, similar to a salt but kept secret (stored separately from the database, e.g., in environment variables or a hardware security module). If the database is leaked but the pepper remains secret, passwords cannot be cracked.

## Q25: What is a rainbow table attack?
**A:** A rainbow table is a precomputed table of hash values for a large set of possible passwords. Attackers use it to reverse a hash back to the original password quickly. Salting passwords makes rainbow table attacks ineffective because each salt produces a unique hash.

## Q26: What is LDAP authentication?
**A:** LDAP (Lightweight Directory Access Protocol) authentication uses a directory service to verify user credentials. Users bind to the LDAP server with a DN (Distinguished Name) and password. It is commonly used in enterprise environments for centralizing user management.

## Q27: What is Kerberos authentication?
**A:** Kerberos is a network authentication protocol that uses tickets and symmetric-key cryptography to verify identities in a non-secure network. It involves a Key Distribution Center (KDC) that issues ticket-granting tickets (TGT) and service tickets. It is the foundation of Windows Active Directory authentication.

## Q28: What is SAML (Security Assertion Markup Language)?
**A:** SAML is an XML-based open standard for exchanging authentication and authorization data between parties, particularly between an identity provider (IdP) and a service provider (SP). It enables SSO across different domains and is commonly used in enterprise applications.

## Q29: What is the difference between SAML and OIDC?
**A:** SAML uses XML and is heavier, typically used in enterprise environments; OIDC uses JSON and is lighter, designed for modern web and mobile apps. SAML uses browser redirects with SAML assertions; OIDC uses JWTs. OIDC is built on OAuth 2.0, while SAML is a standalone protocol.

## Q30: What is a bearer token?
**A:** A bearer token is a security token that grants the bearer (whoever holds it) access to a protected resource. No additional proof of identity is needed beyond possession of the token. JWTs are commonly used as bearer tokens. Bearer tokens must be transmitted over HTTPS to prevent interception.

## Q31: What is the Authorization header format for bearer tokens?
**A:** The format is: `Authorization: Bearer <token>`. For example: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`. The server extracts the token from this header, verifies it, and grants or denies access.

## Q32: What is OAuth 2.0 Authorization Code flow?
**A:** The Authorization Code flow is the most secure OAuth 2.0 flow. The client redirects the user to the authorization server, which returns an authorization code after user authentication. The client exchanges this code for an access token (and optionally a refresh token) via a secure back-channel request.

## Q33: What is the OAuth 2.0 Implicit flow?
**A:** The Implicit flow was designed for browser-based applications that couldn't securely store client secrets. The access token was returned directly in the URL fragment after user authentication. This flow is now deprecated due to security concerns — the Authorization Code flow with PKCE is recommended instead.

## Q34: What is PKCE (Proof Key for Code Exchange)?
**A:** PKCE is an extension to the OAuth 2.0 Authorization Code flow designed to secure public clients (e.g., mobile apps, SPAs). The client generates a code verifier (random string) and a code challenge (hash of the verifier). The authorization server validates the verifier against the challenge during token exchange, preventing authorization code interception attacks.

## Q35: What is the Client Credentials flow in OAuth 2.0?
**A:** The Client Credentials flow is used for machine-to-machine (M2M) communication. The client authenticates directly with the authorization server using its client ID and client secret, receiving an access token without any user involvement. It is commonly used for backend services and APIs.

## Q36: What is the Resource Owner Password Credentials (ROPC) flow?
**A:** ROPC allows the client to directly collect the user's username and password and exchange them for an access token. It is considered less secure and should only be used when other flows are not feasible (e.g., for legacy or trusted first-party applications). It is generally not recommended.

## Q37: What is a client ID and client secret in OAuth?
**A:** A client ID is a public identifier for the app (not secret). A client secret is a confidential key known only to the application and the authorization server. Client secrets are used in confidential clients (server-side apps) to authenticate the application during token exchanges.

## Q38: What is an Identity Provider (IdP)?
**A:** An IdP is a system that creates, maintains, and manages identity information and provides authentication services to relying applications. Examples include Okta, Auth0, Azure AD, Google Identity Platform, and Keycloak.

## Q39: What is a Service Provider (SP) in authentication?
**A:** A Service Provider is an application or system that relies on an Identity Provider to authenticate users. The SP trusts the IdP's authentication assertions and grants access based on them. In SAML, the SP and IdP have a pre-established trust relationship.

## Q40: What is federated identity?
**A:** Federated identity allows users to use the same identity credentials across multiple systems or organizations. It links a user's identities across different identity management systems, enabling SSO across organizational boundaries. Examples include logging into a website with Google or Facebook credentials.

## Q41: What is a session hijacking attack?
**A:** Session hijacking occurs when an attacker steals a user's session identifier (session ID or token) and uses it to impersonate the user. This can happen through packet sniffing, XSS attacks, physical access, or man-in-the-middle attacks. HTTPS, HTTP-only cookies, and session rotation help mitigate this.

## Q42: What is session fixation?
**A:** Session fixation is an attack where the attacker sets or fixes a user's session ID before the user logs in. After login, the attacker uses the predetermined session ID to access the authenticated session. Protection includes regenerating session IDs after login.

## Q43: What is the difference between horizontal and vertical authentication bypass?
**A:** Horizontal bypass means accessing another user's account at the same privilege level (e.g., User A accessing User B's profile). Vertical bypass means gaining higher privileges than allowed (e.g., a regular user accessing admin functions). Both are authorization issues that occur after authentication.

## Q44: What is CAPTCHA and how does it help authentication?
**A:** CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) presents challenges that are easy for humans but hard for bots. It helps prevent automated brute force attacks, credential stuffing, and account creation abuse on login and registration forms.

## Q45: What is rate limiting in authentication?
**A:** Rate limiting restricts the number of authentication attempts from a single IP address, user account, or device within a specific time window. It prevents brute force attacks, credential stuffing, and DoS attacks. Common limits are 5-10 failed attempts per minute.

## Q46: What is account lockout and its trade-offs?
**A:** Account lockout temporarily disables an account after a certain number of failed login attempts. While it prevents brute force attacks, it also enables denial-of-service attacks where attackers intentionally lock out legitimate users. Rate limiting is often preferred as a more measured approach.

## Q47: What is credential stuffing?
**A:** Credential stuffing is an attack where automated tools use username/password pairs leaked from one service to try to log into other services. It exploits the common practice of password reuse across multiple sites. MFA and breached password detection help mitigate this.

## Q48: What is WebAuthn?
**A:** WebAuthn (Web Authentication) is a W3C standard for passwordless authentication using public-key cryptography. It enables users to authenticate with biometrics, security keys, or platform authenticators (like Apple Touch ID or Windows Hello) instead of passwords.

## Q49: What is FIDO2?
**A:** FIDO2 is a set of standards (including WebAuthn and CTAP) that enables passwordless authentication using public-key cryptography. It allows users to register devices (like YubiKeys or built-in platform authenticators) and authenticate with biometrics or PINs, providing phishing-resistant authentication.

## Q50: What is a passkey?
**A:** A passkey is a FIDO2-based credential that replaces passwords. It uses public-key cryptography: the private key stays on the user's device, and the public key is stored on the server. Passkeys sync across devices via cloud services (Apple Keychain, Google Password Manager) and are resistant to phishing.

## Q51: What is time-based one-time password (TOTP)?
**A:** TOTP is a temporary, one-time password generated using a shared secret key and the current time. It typically produces a 6-digit code valid for 30 seconds. TOTP is used in authenticator apps like Google Authenticator and Authy as a second factor.

## Q52: What is HMAC-based one-time password (HOTP)?
**A:** HOTP is an event-based one-time password algorithm that uses a shared secret and a moving counter (incremented after each use). Unlike TOTP, it does not rely on time synchronization. Each code is valid until used, making it suitable for hardware tokens.

## Q53: What is SMS-based 2FA and why is it considered less secure?
**A:** SMS-based 2FA sends a one-time code via text message. It is considered less secure because of SIM swapping attacks (attacker convinces the carrier to transfer the phone number), SS7 protocol vulnerabilities, and the possibility of interception by malware. TOTP or hardware keys are preferred.

## Q54: What is SIM swapping?
**A:** SIM swapping (or SIM jacking) is an attack where the fraudster convinces a mobile carrier to transfer the victim's phone number to a SIM card the attacker controls. This allows the attacker to receive SMS-based 2FA codes and reset passwords, gaining access to accounts.

## Q55: What is biometric authentication?
**A:** Biometric authentication uses unique biological characteristics to verify identity, such as fingerprints, facial patterns, iris scans, voice recognition, or behavioral patterns (typing rhythm, gait). It offers convenience but raises privacy concerns and cannot be reset like a password if compromised.

## Q56: What is the difference between verification and identification in biometrics?
**A:** Verification (1:1 matching) confirms "Are you who you claim to be?" — compares the biometric against a specific stored template. Identification (1:N matching) answers "Who are you?" — compares against all stored templates to find a match.

## Q57: What is a false acceptance rate (FAR) in biometrics?
**A:** FAR (False Acceptance Rate) is the probability that a biometric system incorrectly accepts an unauthorized user as legitimate. A lower FAR means higher security. It trades off against FRR (False Rejection Rate).

## Q58: What is a false rejection rate (FRR) in biometrics?
**A:** FRR (False Rejection Rate) is the probability that a biometric system incorrectly rejects a legitimate user. A lower FRR means better usability. Systems must balance FAR and FRR based on the application's security requirements.

## Q59: What is mutual authentication?
**A:** Mutual authentication (or two-way authentication) requires both parties in a communication to verify each other's identity before data exchange. In TLS, the server presents a certificate to the client (one-way), but with mutual TLS (mTLS), the client also presents a certificate to the server.

## Q60: What is certificate-based authentication?
**A:** Certificate-based authentication uses digital certificates (X.509) to verify identity. The user presents a certificate signed by a trusted Certificate Authority (CA). The server verifies the certificate's validity, signature chain, and optionally checks revocation status via CRL or OCSP.

## Q61: What is client certificate authentication?
**A:** Client certificate authentication (or mutual TLS) is a method where the server requests and validates a certificate from the client during the TLS handshake. It provides strong, phishing-resistant authentication without passwords. It is commonly used in enterprise VPNs and API security.

## Q62: What is a Certificate Authority (CA)?
**A:** A CA is a trusted entity that issues digital certificates. The CA verifies the identity of the certificate requester and signs the certificate with its own private key. Browsers and operating systems ship with a list of trusted root CAs.

## Q63: What is a self-signed certificate?
**A:** A self-signed certificate is a certificate signed by its own creator rather than a trusted CA. It provides encryption but not identity verification. Self-signed certificates trigger browser warnings and are typically used only in development or internal environments.

## Q64: What is the difference between authentication and identification?
**A:** Identification is the act of claiming an identity (e.g., providing a username). Authentication is proving that identity claim is valid (e.g., providing the correct password). Identification without authentication carries no proof.

## Q65: What is anonymous authentication?
**A:** Anonymous authentication allows users to access resources without revealing their identity. It is commonly used for public websites or resources that do not require user-specific access control. The system typically assigns a guest or anonymous user context.

## Q66: What is risk-based authentication (adaptive authentication)?
**A:** Risk-based authentication adjusts the authentication requirements based on the risk level of the access attempt. Factors include device, location, time, behavior patterns, and IP reputation. Low-risk actions may proceed without additional verification; high-risk actions trigger step-up authentication (e.g., MFA).

## Q67: What is step-up authentication?
**A:** Step-up authentication requires users to provide additional authentication factors when accessing sensitive resources or performing high-risk actions. For example, viewing a profile page may only need a password, but making a payment may require MFA.

## Q68: What is a token revocation mechanism?
**A:** Token revocation invalidates a token before its natural expiration. Approaches include: (1) maintaining a blacklist of revoked tokens, (2) using short-lived tokens with refresh token rotation, (3) versioned user secrets (incrementing a version invalidates all previous tokens).

## Q69: What is token rotation?
**A:** Token rotation replaces a token with a new one each time it is used. For refresh tokens, each time a new access token is issued, the old refresh token is invalidated and a new one is returned. This limits the damage if a refresh token is stolen.

## Q70: What is a refresh token reuse detection?
**A:** Refresh token reuse detection monitors if a revoked/used refresh token is presented again, which indicates token theft. When detected, all refresh tokens for that user are typically revoked, forcing re-authentication. This is a key security measure in OAuth 2.0.

## Q71: What is a scope in OAuth 2.0?
**A:** A scope defines the specific permissions or access level requested by a client application. When requesting authorization, the client specifies scopes (e.g., `read`, `write`, `email`, `profile`). The authorization server displays these to the user for consent and limits the access token accordingly.

## Q72: What is the principle of least privilege in authentication?
**A:** The principle of least privilege means giving users only the minimum permissions needed to perform their tasks. Applied to authentication, it means tokens should have the minimum necessary scopes, sessions should expire when no longer needed, and default access should be denied.

## Q73: What is a service account?
**A:** A service account is a non-human identity used by applications, services, or automated processes to authenticate and interact with systems. Unlike user accounts, service accounts typically use API keys, certificates, or OAuth client credentials for authentication.

## Q74: What is a machine-to-machine (M2M) authentication?
**A:** M2M authentication is the process where services or applications authenticate to each other without human intervention. It commonly uses OAuth 2.0 Client Credentials flow, API keys, mutual TLS, or JWTs signed with service account keys.

## Q75: What is API key authentication?
**A:** API key authentication uses a unique key assigned to a client to identify and authenticate API requests. The key is typically sent in headers (`X-API-Key`), query parameters, or basic auth. API keys are simpler than OAuth but offer less granularity and security.

## Q76: What is HTTP Basic Authentication?
**A:** HTTP Basic Authentication sends the username and password concatenated with a colon, base64-encoded, in the `Authorization` header (`Authorization: Basic dXNlcjpwYXNz`). It is not secure by itself (base64 is easily decoded) and must only be used over HTTPS.

## Q77: What is HTTP Digest Authentication?
**A:** HTTP Digest Authentication improves on Basic Auth by using MD5 hashing of the password with a server-provided nonce. It avoids sending the password in plaintext but is still considered outdated and less secure than modern methods like OAuth or JWT.

## Q78: What is Windows Authentication (NTLM/Kerberos)?
**A:** Windows Authentication includes NTLM (challenge-response) and Kerberos (ticket-based) protocols. NTLM is older and less secure. Kerberos is the default for Active Directory and provides SSO within a Windows domain. Both are commonly used for intranet applications.

## Q79: What is RADIUS authentication?
**A:** RADIUS (Remote Authentication Dial-In User Service) is a networking protocol that provides centralized AAA (Authentication, Authorization, Accounting) for users connecting to network services. It is commonly used for VPN, Wi-Fi (802.1X), and network device access.

## Q80: What is a token endpoint in OAuth 2.0?
**A:** The token endpoint is an OAuth 2.0 server endpoint where clients exchange authorization codes, refresh tokens, or client credentials for access tokens. Requests to this endpoint are typically POST requests with the grant type and associated parameters.

## Q81: What is the authorization endpoint in OAuth 2.0?
**A:** The authorization endpoint is the OAuth 2.0 server endpoint where the user authenticates and grants consent. The client redirects the user here. After successful authentication and consent, the user is redirected back to the client with an authorization code (in the Authorization Code flow).

## Q82: What is a redirect URI in OAuth?
**A:** A redirect URI (or callback URL) is the endpoint on the client application where the authorization server sends the user after authentication. It is registered with the authorization server during client setup and must be validated to prevent open redirect attacks.

## Q83: What is the state parameter in OAuth 2.0?
**A:** The state parameter is a random value generated by the client and included in the authorization request. It is returned unchanged in the callback. It prevents CSRF attacks by allowing the client to verify that the response matches the original request.

## Q84: What is a nonce in authentication?
**A:** A nonce (number used once) is a random or semi-random number generated for a specific authentication transaction. It prevents replay attacks by ensuring each authentication request is unique and cannot be reused. Nonces are used in various protocols including HTTP Digest and OIDC.

## Q85: What is a replay attack?
**A:** A replay attack occurs when an attacker intercepts a valid authentication message (e.g., a token or signed request) and retransmits it to trick the system into thinking it is from the original sender. Nonces, timestamps, and short expiration times prevent replay attacks.

## Q86: What is a man-in-the-middle (MITM) attack on authentication?
**A:** A MITM attack occurs when an attacker intercepts communication between the user and the server to steal credentials or tokens. HTTPS/TLS prevents MITM attacks by encrypting the communication channel. Public Wi-Fi networks are common vectors for MITM attacks.

## Q87: What is a phishing attack in the context of authentication?
**A:** Phishing attacks trick users into revealing their credentials by presenting fake login pages that mimic legitimate services. Modern phishing can bypass 2FA by using reverse proxies (evilginx). Hardware security keys (FIDO2) are the most effective protection against phishing.

## Q88: What is credential harvesting?
**A:** Credential harvesting is the mass collection of usernames and passwords through phishing, data breaches, malwares, or social engineering. Harvested credentials are typically used for credential stuffing attacks or sold on darknet markets.

## Q89: What is passwordless authentication?
**A:** Passwordless authentication eliminates passwords entirely. Users authenticate using methods like magic links (email), one-time codes (SMS/email), biometrics (fingerprint/face), or security keys (FIDO2/WebAuthn). It improves security and user experience by removing the weakest link — passwords.

## Q90: What are magic links?
**A:** Magic links are one-time-use URLs sent to the user's email that automatically authenticate them when clicked. The link contains a unique token, validates the user's email ownership, and logs them in. Magic links are a form of passwordless authentication.

## Q91: What is social login?
**A:** Social login allows users to authenticate using their existing accounts from social platforms (Google, Facebook, GitHub, Apple, etc.) via OAuth 2.0/OIDC. It reduces friction, eliminates password fatigue, and delegates identity management to the social provider.

## Q92: How do you handle token expiration on the client side?
**A:** Options include: (1) Intercepting 401 responses and automatically refreshing the token, (2) Checking token expiration client-side (JWTs have an `exp` claim) and refreshing proactively, (3) Using an interceptor or middleware that queues failed requests and retries after refreshing.

## Q93: What is a sliding session expiration?
**A:** Sliding session expiration extends the session lifetime each time the user interacts with the application. If the user is active, the session TTL is reset. If inactive beyond the timeout, the session expires. This balances security with user convenience.

## Q94: What is an absolute session timeout?
**A:** An absolute session timeout forces the user to re-authenticate after a fixed period regardless of activity. For example, a banking app might enforce re-authentication every 15 minutes. It provides stronger security than sliding expiration for sensitive applications.

## Q95: What is a key rotation strategy for JWT signing keys?
**A:** Key rotation periodically changes the secret key used to sign JWTs. A common strategy uses key IDs (kid) in the JWT header and maintains a list of valid keys. Old keys are kept for a transition period to validate already-issued tokens, then removed.

## Q96: What is HMAC vs RSA for JWT signing?
**A:** HMAC (HS256) uses a symmetric shared secret — the same key signs and verifies tokens. RSA (RS256) uses asymmetric key pairs — the private key signs, the public key verifies. RSA is preferred for multi-service architectures since only the issuer holds the private key.

## Q97: What is a user info endpoint in OIDC?
**A:** The user info endpoint is an OIDC endpoint that returns claims about the authenticated user. It is accessed using the access token. If the ID token contains essential claims, the user info endpoint provides additional profile information via a REST API.

## Q98: What is an ID token in OIDC?
**A:** An ID token is a JWT issued by the OIDC provider that contains claims about the authenticated user, such as `sub` (subject identifier), `email`, `name`, and `iss` (issuer). It is obtained alongside the access token and is used for authentication (not API access).

## Q99: What is the difference between `sub` and `iss` claims in a JWT?
**A:** `sub` (subject) identifies the user or entity the token is about. `iss` (issuer) identifies who issued the token. Together, `iss` + `sub` provides a globally unique identity. For example, `iss: "https://accounts.google.com"` and `sub: "12345"` uniquely identifies a Google user.

## Q100: What is the authentication flow for a typical SPA (Single Page Application)?
**A:** The recommended flow for SPAs is OAuth 2.0 Authorization Code with PKCE. The SPA redirects the user to the authorization server, the user authenticates, the server returns an authorization code, the SPA exchanges it (with PKCE) for tokens. Access tokens are short-lived. Refresh tokens should be stored securely (preferably HTTP-only cookies from a backend).
