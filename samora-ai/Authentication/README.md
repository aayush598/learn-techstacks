# Authentication Interview Questions and Answers

## Q1: What is Authentication?
**A:** Authentication is the process of verifying the identity of a user, system, or entity. It ensures that the entity is who they claim to be by validating credentials such as passwords, biometrics, tokens, or certificates.

**Code:**
```python
import bcrypt

stored = bcrypt.hashpw(b"hunter2", bcrypt.gensalt())

def authenticate(username, password):
    return bcrypt.checkpw(password.encode(), stored)  # True == identity verified
```

## Q2: What is the difference between Authentication and Authorization?
**A:** Authentication verifies **who** you are (identity), while Authorization determines **what** you are allowed to do (permissions). Authentication always comes before authorization. For example, logging in with a password is authentication; being granted access to a specific page after login is authorization.

**Code:**
```python
def authenticate(user, password):      # WHO are you?
    return bcrypt.checkpw(password.encode(), user["hash"])

def authorize(user, capability):       # WHAT can you do?
    return capability in user["permissions"]

if all([authenticate(user, pw), authorize(user, "edit:page")]):
    pass  # identity proven AND permission granted
```

## Q3: What are the three main factors of authentication?
**A:** The three factors are: (1) **Something you know** – passwords, PINs, security questions; (2) **Something you have** – smart cards, security tokens, mobile devices; (3) **Something you are** – biometrics like fingerprints, facial recognition, iris scans.

**Code:**
```python
def check_factor(factor_type, credential):
    if factor_type == "know":     return verify_password(credential)
    if factor_type == "have":     return verify_totp_token(credential)
    if factor_type == "are":      return verify_fingerprint(credential)
    return False

# each factor is a different CATEGORY of evidence
authenticated = check_factor("know", password) or check_factor("have", token)
```

## Q4: What is Multi-Factor Authentication (MFA)?
**A:** MFA is a security system that requires two or more authentication factors from different categories to verify a user's identity. For example, combining a password (something you know) with a one-time code sent to your phone (something you have).

**Code:**
```python
def verify_mfa(password_ok, totp_ok):
    return password_ok and totp_ok   # two DIFFERENT categories, both required

if verify_mfa(check_password(user), check_totp(user)):
    grant_access(user)
```

## Q5: What is Two-Factor Authentication (2FA)?
**A:** 2FA is a subset of MFA that uses exactly two distinct authentication factors. Common implementations include password + SMS code, password + authenticator app TOTP, or password + hardware security key.

**Code:**
```python
def verify_2fa(password, sms_code):
    return check_password(password) and check_sms_code(sms_code)  # exactly 2 factors
```

## Q6: What is Single Sign-On (SSO)?
**A:** SSO is an authentication scheme that allows a user to log in once and gain access to multiple independent systems or applications without being prompted to log in again. It uses a central authentication server that issues tokens trusted by all connected services.

**Code:**
```python
import jwt
SSO_SECRET = "central-shared-secret"      # trusted by every connected app

def sso_login(user):                     # central server authenticates once
    return jwt.encode({"sub": user}, SSO_SECRET, algorithm="HS256")

def verify_token_in_any_app(token):      # every app just verifies the token
    return jwt.decode(token, SSO_SECRET, algorithms=["HS256"])
```

## Q7: What is OAuth 2.0?
**A:** OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts on an HTTP service. It works by delegating user authentication to the service that hosts the user account and authorizing third-party applications to access that account. It is not an authentication protocol but is often used for authentication.

**Code:**
```python
import requests

# third-party app asks the resource server's token endpoint for scoped access
resp = requests.post("https://api.example.com/oauth/token", data={
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
})
access_token = resp.json()["access_token"]   # grants LIMITED access
```

## Q8: What is OpenID Connect (OIDC)?
**A:** OpenID Connect is an identity layer built on top of OAuth 2.0. While OAuth 2.0 is about authorization, OIDC adds authentication. It allows clients to verify the identity of the end-user based on the authentication performed by an authorization server, obtaining basic profile information in an ID token (JWT).

**Code:**
```python
import jwt

# OIDC: exchange the OAuth access token for a finished ID token (JWT)
id_token = jwt.encode(
    {"iss": "https://accounts.example.com", "sub": "user-123",
     "aud": CLIENT_ID, "email": "alice@example.com"},
    PRIVATE_KEY, algorithm="RS256")      # signed = identity is verified
```

## Q9: What is a JWT (JSON Web Token)?
**A:** JWT is a compact, URL-safe token format used for representing claims between two parties. It consists of three parts: header (algorithm and token type), payload (claims/data), and signature (created by combining the header, payload, and a secret). JWTs are commonly used for authentication and information exchange.

**Code:**
```python
import jwt

token = jwt.encode({"sub": "user-123", "role": "admin"}, SECRET, algorithm="HS256")
header, payload, signature = token.split(".")   # three segments
claims = jwt.decode(token, SECRET, algorithms=["HS256"])   # verify signature
```

## Q10: How does JWT authentication work?
**A:** The user logs in with credentials; the server validates them and generates a JWT signed with a secret. The client stores the JWT (typically in localStorage or an HTTP-only cookie) and sends it in the Authorization header for subsequent requests. The server verifies the signature and extracts user information from the payload without needing a database lookup.

**Code:**
```python
import jwt

def login(username, password):                 # 1) validate credentials
    if not check_password(username, password):
        raise PermissionError
    return jwt.encode({"sub": username, "exp": now + 3600}, SECRET)  # 2) sign

def current_user(request):                     # 3) verify on each request
    token = request.headers["Authorization"].split(" ")[1]   # "Bearer <jwt>"
    claims = jwt.decode(token, SECRET, algorithms=["HS256"]) # no DB lookup
    return claims["sub"]
```

## Q11: What is a session-based authentication?
**A:** Session-based authentication stores session data on the server. When a user logs in, the server creates a session, stores it in memory/database, and returns a session ID to the client (usually via a cookie). The client sends the session ID with each request, and the server looks up the session to identify the user.

**Code:**
```python
import secrets

sessions = {}                      # server-side session store

def login(user):
    sid = secrets.token_hex(32)    # random session id given to client
    sessions[sid] = user
    return sid

def get_user_from_cookie(sid):     # server looks it up on each request
    return sessions.get(sid)
```

## Q12: What is token-based authentication?
**A:** Token-based authentication uses tokens (like JWTs) that contain user information and are cryptographically signed. The server does not need to store session data — it only needs to verify the token's signature. This makes token-based authentication stateless and more scalable.

**Code:**
```python
import jwt

def login(user):
    return jwt.encode({"sub": user, "exp": now + 3600}, SECRET)  # signed token

def verify(token):                            # stateless: no session lookup
    return jwt.decode(token, SECRET, algorithms=["HS256"])
```

## Q13: What are the advantages of token-based authentication over session-based?
**A:** (1) Stateless — no server-side storage needed; (2) Scalable — tokens work across multiple servers/domains easily; (3) Mobile-friendly — works well with native mobile apps; (4) Performance — no database lookup for each request; (5) CORS-friendly — tokens can be sent via headers.

**Code:**
```python
# any server replica can validate the same token — no shared session store
def authenticate(request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    claims = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    return claims            # works identically on every server / domain
```

## Q14: What is a refresh token?
**A:** A refresh token is a long-lived token used to obtain new access tokens without requiring the user to re-authenticate. Access tokens are short-lived (e.g., 15 minutes), while refresh tokens can last days or months. Refresh tokens are stored securely and rotated periodically.

**Code:**
```python
import jwt

def issue_tokens(user):
    access = jwt.encode({"sub": user, "exp": now + 15 * 60}, ACCESS_SECRET)
    refresh = jwt.encode({"sub": user, "exp": now + 30 * 86400}, REFRESH_SECRET)
    return access, refresh

def refresh_access(refresh_token):
    claims = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=["HS256"])
    return jwt.encode({"sub": claims["sub"], "exp": now + 15 * 60}, ACCESS_SECRET)
```

## Q15: What is an access token?
**A:** An access token is a credential used to access protected resources. It is typically short-lived (minutes to hours) and contains information about the user and their permissions. It is sent with each API request in the Authorization header.

**Code:**
```python
import requests

token = jwt.encode({"sub": user, "scope": "read write", "exp": now + 1800}, SECRET)
resp = requests.get("https://api.example.com/account",
                    headers={"Authorization": f"Bearer {token}"})
```

## Q16: How should you store tokens on the client side?
**A:** The most secure approach is using HTTP-only Secure SameSite cookies, which prevent XSS attacks from stealing tokens. Alternatively, tokens can be stored in memory (most secure for SPAs). localStorage/sessionStorage are convenient but vulnerable to XSS attacks.

**Code:**
```python
from flask import make_response

resp = make_response(redirect("/dashboard"))
resp.set_cookie("session", jw_token,
                httponly=True,   # invisible to JavaScript -> XSS-safe
                secure=True,     # HTTPS only
                samesite="Lax")  # mitigates CSRF
```

## Q17: What is a CSRF attack and how does it relate to authentication?
**A:** Cross-Site Request Forgery (CSRF) is an attack that tricks a user into executing unwanted actions on a web application where they are authenticated. It exploits the fact that browsers automatically include cookies with requests. Protection includes CSRF tokens, SameSite cookies, and checking Origin/Referer headers.

**Code:**
```python
import secrets

CSRF_TOKENS = {}

def issue_csrf_token(session_id):
    token = secrets.token_hex(16)          # unpredictable per-session value
    CSRF_TOKENS[session_id] = token
    return token

def validate_csrf(session_id, submitted):
    return secrets.compare_digest(CSRF_TOKENS.get(session_id, ""), submitted)
```

## Q18: What is an XSS attack in the context of authentication?
**A:** Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users. In authentication contexts, XSS can steal tokens from localStorage, session cookies (if not HTTP-only), or capture keystrokes to steal passwords. HTTP-only cookies and input sanitization help prevent this.

**Code:**
```python
from markupsafe import escape

# never render raw user input; escape it so <script> stays inert
user_comment = "<script>stealToken()</script>"
safe_html = escape(user_comment)          # -> &lt;script&gt;stealToken()&lt;/script&gt;

# and keep tokens out of reach of JS
response.set_cookie("session", token, httponly=True)   # document.cookie stays empty
```

## Q19: What is a brute force attack on authentication?
**A:** A brute force attack attempts to gain access by systematically trying all possible passwords or credentials until the correct one is found. Mitigations include account lockout policies, rate limiting, CAPTCHA, and using strong password policies.

**Code:**
```python
from time import time

failures = {}          # username -> list of timestamps

def login(username, password):
    recent = [t for t in failures.get(username, []) if time() - t < 600]
    if len(recent) >= 5:
        raise AccountLocked                            # lockout/rate-limit
    backed_off_ok = check_password(username, password)
    if not backed_off_ok:
        recent.append(time()); failures[username] = recent
    return backed_off_ok
```

## Q20: What is a dictionary attack?
**A:** A dictionary attack is a type of brute force attack that uses a list of common passwords, words from dictionaries, and previously leaked passwords instead of trying all possible combinations. It is more efficient than a pure brute force attack.

**Code:**
```python
import bcrypt

LEAKED = ["123456", "password", "qwerty", "letmein", "admin"]

def dictionary_attack(hashed):
    for candidate in LEAKED:
        if bcrypt.checkpw(candidate.encode(), hashed):
            return candidate
    return None
```

## Q21: What is password hashing and why is it important?
**A:** Password hashing is the process of converting a plain-text password into a fixed-length string using a one-way cryptographic function. It is important because even if the database is breached, attackers cannot recover the original passwords. Hashing is different from encryption — hashing is irreversible.

**Code:**
```python
import hashlib

users = {}
def store_password(user, plain):
    users[user] = hashlib.sha256(plain.encode()).hexdigest()  # one-way only

def verify(user, plain):
    return hashlib.sha256(plain.encode()).hexdigest() == users[user]
# even with the DB dumped, the plaintext cannot be recovered
```

## Q22: What are the best hashing algorithms for passwords?
**A:** The recommended algorithms are bcrypt, Argon2 (winner of the Password Hashing Competition), scrypt, and PBKDF2. These are designed to be slow and computationally expensive, making brute force attacks difficult. Argon2 is considered the most secure option currently.

**Code:**
```python
import bcrypt
from argon2 import PasswordHasher          # Argon2 = PHC winner

# deliberately SLOW, memory-hard algorithms
h = bcrypt.hashpw(b"password", bcrypt.gensalt(rounds=12))
ph = PasswordHasher(time_cost=3, memory_cost=65536)   # Argon2id
h2 = ph.hash("password")
assert ph.verify(h2, "password")
```

## Q23: What is a salt in password hashing?
**A:** A salt is a random, unique value added to each password before hashing. It ensures that even if two users have the same password, their hashes will be different. Salts prevent rainbow table attacks and make precomputation attacks impractical.

**Code:**
```python
import hashlib, os

def hash_password(password):
    salt = os.urandom(16)                          # random, unique per user
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return salt, digest

# "password" + salt_a != "password" + salt_b -> different hashes, no rainbow tables
```

## Q24: What is a pepper in password hashing?
**A:** A pepper is a secret, fixed value added to passwords before hashing, similar to a salt but kept secret (stored separately from the database, e.g., in environment variables or a hardware security module). If the database is leaked but the pepper remains secret, passwords cannot be cracked.

**Code:**
```python
import hashlib, os
PEPPER = os.environ["PASSWORD_PEPPER"]   # secret, stored SEPARATE from the DB

salt = os.urandom(16)
digest = hashlib.pbkdf2_hmac(
    "sha256", (password + PEPPER).encode(), salt, 100_000)

# if the DB leaks but the pepper stays secret, the hashes are still uncrackable
```

## Q25: What is a rainbow table attack?
**A:** A rainbow table is a precomputed table of hash values for a large set of possible passwords. Attackers use it to reverse a hash back to the original password quickly. Salting passwords makes rainbow table attacks ineffective because each salt produces a unique hash.

**Code:**
```python
# A rainbow table maps hash -> password, precomputed ONCE on an attacker's disk.
import hashlib
table = {hashlib.md5(p.encode()).hexdigest(): p for p in open("wordlist.txt")}

def crack_unsalted(h):
    return table.get(h)          # instant lookup

# With a per-user salt the lookup key is md5(salt+password) ->
# a single global table can never match, so the attack collapses.
```

## Q26: What is LDAP authentication?
**A:** LDAP (Lightweight Directory Access Protocol) authentication uses a directory service to verify user credentials. Users bind to the LDAP server with a DN (Distinguished Name) and password. It is commonly used in enterprise environments for centralizing user management.

**Code:**
```python
import ldap3

server = ldap3.Server("ldap://dc.example.com")
conn = ldap3.Connection(
    server,
    user=f"uid={username},{BASE_DN}",      # bind DN = who you claim to be
    password=password,
    auto_bind=True)                        # verifies credentials against the directory
# conn.bound == True iff the password matched
```

## Q27: What is Kerberos authentication?
**A:** Kerberos is a network authentication protocol that uses tickets and symmetric-key cryptography to verify identities in a non-secure network. It involves a Key Distribution Center (KDC) that issues ticket-granting tickets (TGT) and service tickets. It is the foundation of Windows Active Directory authentication.

**Code:**
```python
from requests_kerberos import HTTPKerberosAuth
import requests

# 1) KDC checks the password and issues a Ticket-Granting Ticket (TGT)
# 2) the TGT is redeemed for a SERVICE ticket for this application
r = requests.get("https://app.example.com", auth=HTTPKerberosAuth())
# the server decrypts the service ticket with its long-term key -> proof of identity
```

## Q28: What is SAML (Security Assertion Markup Language)?
**A:** SAML is an XML-based open standard for exchanging authentication and authorization data between parties, particularly between an identity provider (IdP) and a service provider (SP). It enables SSO across different domains and is commonly used in enterprise applications.

**Code:**
```python
from onelogin.saml2.auth import OneLogin_Saml2_Auth

def verify_saml_assertion(settings, request):
    auth = OneLogin_Saml2_Auth(settings, request)
    auth.process_response()                     # validate the signed XML
    if not auth.is_authenticated():
        raise PermissionError
    return auth.get_attributes()                # user identity from the IdP
```

## Q29: What is the difference between SAML and OIDC?
**A:** SAML uses XML and is heavier, typically used in enterprise environments; OIDC uses JSON and is lighter, designed for modern web and mobile apps. SAML uses browser redirects with SAML assertions; OIDC uses JWTs. OIDC is built on OAuth 2.0, while SAML is a standalone protocol.

**Code:**
```python
# SAML -> XML assertions + browser POST binding (enterprise SSO)
saml = '<saml:Assertion xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">...</saml:Assertion>'

# OIDC -> compact JSON JWT over REST (modern web + mobile)
id_token = jwt.encode({"iss": "https://idp.example", "sub": "u1"},
                      PRIVATE_KEY, algorithm="RS256")
```

## Q30: What is a bearer token?
**A:** A bearer token is a security token that grants the bearer (whoever holds it) access to a protected resource. No additional proof of identity is needed beyond possession of the token. JWTs are commonly used as bearer tokens. Bearer tokens must be transmitted over HTTPS to prevent interception.

**Code:**
```python
import jwt

def protect(request):
    auth = request.headers.get("Authorization", "")
    token = auth.removeprefix("Bearer ")
    claims = jwt.decode(token, SECRET, algorithms=["HS256"])
    return claims                      # possession of the token IS the credential
```

## Q31: What is the Authorization header format for bearer tokens?
**A:** The format is: `Authorization: Bearer <token>`. For example: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`. The server extracts the token from this header, verifies it, and grants or denies access.

**Code:**
```python
import jwt

token = jwt.encode({"sub": "u1"}, SECRET, algorithm="HS256")
header = f"Authorization: Bearer {token}"        # the required format

def extract(request):
    scheme, _, token = request.headers["Authorization"].partition(" ")
    assert scheme == "Bearer"                     # server parses exactly this scheme
    return jwt.decode(token, SECRET, algorithms=["HS256"])
```

## Q32: What is OAuth 2.0 Authorization Code flow?
**A:** The Authorization Code flow is the most secure OAuth 2.0 flow. The client redirects the user to the authorization server, which returns an authorization code after user authentication. The client exchanges this code for an access token (and optionally a refresh token) via a secure back-channel request.

**Code:**
```python
import requests

# 1) user is redirected to /authorize -> authenticates -> returns ?code=
# 2) confidential client exchanges the code over a secure back channel:
resp = requests.post("https://as.example.com/token", data={
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
})
access_token = resp.json()["access_token"]
```

## Q33: What is the OAuth 2.0 Implicit flow?
**A:** The Implicit flow was designed for browser-based applications that couldn't securely store client secrets. The access token was returned directly in the URL fragment after user authentication. This flow is now deprecated due to security concerns — the Authorization Code flow with PKCE is recommended instead.

**Code:**
```python
# LEGACY Implicit flow: the access token came back straight in the URL fragment
#   https://app.example/cb#access_token=...&token_type=Bearer
# Deprecated: tokens leak via browser history, referrers and WebView inspection.

# Modern replacement: Authorization Code + PKCE
url = ("https://as.example.com/authorize"
       "?response_type=code"
       "&code_challenge=" + sha256_b64url(code_verifier))
```

## Q34: What is PKCE (Proof Key for Code Exchange)?
**A:** PKCE is an extension to the OAuth 2.0 Authorization Code flow designed to secure public clients (e.g., mobile apps, SPAs). The client generates a code verifier (random string) and a code challenge (hash of the verifier). The authorization server validates the verifier against the challenge during token exchange, preventing authorization code interception attacks.

**Code:**
```python
import base64, hashlib, secrets, requests

verifier = secrets.token_urlsafe(64)                       # high-entropy random
challenge = base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()

# authorize call carries ONLY the challenge (S256)...
# ...token exchange must present the original verifier:
resp = requests.post("https://as.example.com/token", data={
    "grant_type": "authorization_code",
    "code": code, "code_verifier": verifier, "client_id": CLIENT_ID})
# the AS hashes the verifier and compares it with the stored challenge
```

## Q35: What is the Client Credentials flow in OAuth 2.0?
**A:** The Client Credentials flow is used for machine-to-machine (M2M) communication. The client authenticates directly with the authorization server using its client ID and client secret, receiving an access token without any user involvement. It is commonly used for backend services and APIs.

**Code:**
```python
import requests

# machine-to-machine: no user in the loop, the client authenticates itself
resp = requests.post("https://as.example.com/token", data={
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "reports:read"})
access_token = resp.json()["access_token"]
```

## Q36: What is the Resource Owner Password Credentials (ROPC) flow?
**A:** ROPC allows the client to directly collect the user's username and password and exchange them for an access token. It is considered less secure and should only be used when other flows are not feasible (e.g., for legacy or trusted first-party applications). It is generally not recommended.

**Code:**
```python
import requests

# client collects the RAW username/password and trades them for a token
resp = requests.post("https://as.example.com/token", data={
    "grant_type": "password",
    "username": username,
    "password": password,
    "client_id": CLIENT_ID})
access_token = resp.json()["access_token"]
# discouraged: only first-party, trusted, legacy apps
```

## Q37: What is a client ID and client secret in OAuth?
**A:** A client ID is a public identifier for the app (not secret). A client secret is a confidential key known only to the application and the authorization server. Client secrets are used in confidential clients (server-side apps) to authenticate the application during token exchanges.

**Code:**
```python
import requests

# client_id: public identifier (safe in URLs) - client_secret: confidential
resp = requests.post(
    "https://as.example.com/token",
    auth=(CLIENT_ID, CLIENT_SECRET),            # authenticates the APPLICATION
    data={"grant_type": "client_credentials"})
assert "access_token" in resp.json()
```

## Q38: What is an Identity Provider (IdP)?
**A:** An IdP is a system that creates, maintains, and manages identity information and provides authentication services to relying applications. Examples include Okta, Auth0, Azure AD, Google Identity Platform, and Keycloak.

**Code:**
```python
# An IdP (Auth0, Okta, Keycloak...) authenticates users and issues tokens
import jwt

def login(username, password, totp):
    if check_password(username, password) and verify_totp(username, totp):
        return jwt.encode({"sub": username, "iss": "https://idp.example"},
                          IDP_KEY, algorithm="RS256")
    raise AuthenticationFailed
```

## Q39: What is a Service Provider (SP) in authentication?
**A:** A Service Provider is an application or system that relies on an Identity Provider to authenticate users. The SP trusts the IdP's authentication assertions and grants access based on them. In SAML, the SP and IdP have a pre-established trust relationship.

**Code:**
```python
# The SP validates the IdP assertion and trusts its content
import jwt

def login_via_idp(id_token):
    claims = jwt.decode(id_token, IDP_JWKS, algorithms=["RS256"],
                        audience=SP_CLIENT_ID, issuer="https://idp.example")
    return claims["sub"]               # trust relationship pre-established with the IdP
```

## Q40: What is federated identity?
**A:** Federated identity allows users to use the same identity credentials across multiple systems or organizations. It links a user's identities across different identity management systems, enabling SSO across organizational boundaries. Examples include logging into a website with Google or Facebook credentials.

**Code:**
```python
import requests, jwt

# one identity, many sites: Google is the IdP, this app is a SP
r = requests.post("https://oauth2.googleapis.com/token", data={
    "grant_type": "authorization_code",
    "code": code, "redirect_uri": REDIRECT, "client_id": GOOGLE_CLIENT_ID})
id_token = r.json()["id_token"]                      # Google-signed JWT
email = jwt.decode(id_token, options={"verify_signature": False})["email"]
```

## Q41: What is a session hijacking attack?
**A:** Session hijacking occurs when an attacker steals a user's session identifier (session ID or token) and uses it to impersonate the user. This can happen through packet sniffing, XSS attacks, physical access, or man-in-the-middle attacks. HTTPS, HTTP-only cookies, and session rotation help mitigate this.

**Code:**
```python
import secrets

SESSION_BIND = {}      # sid -> (user, ip, user_agent)
def create_session(user, ip, ua):
    sid = secrets.token_hex(32)                # unpredictable identifier
    SESSION_BIND[sid] = (user, ip, ua)
    return sid

def is_valid(sid, ip, ua):
    _, expected_ip, expected_ua = SESSION_BIND.get(sid, (None, None, None))
    return expected_ip == ip and expected_ua == ua   # mismatch == likely hijack
```

## Q42: What is session fixation?
**A:** Session fixation is an attack where the attacker sets or fixes a user's session ID before the user logs in. After login, the attacker uses the predetermined session ID to access the authenticated session. Protection includes regenerating session IDs after login.

**Code:**
```python
import secrets

def login(user):
    sid = secrets.token_hex(32)      # REGENERATE the ID after login
    SESSIONS[sid] = user             # attacker can no longer fixate the old id
    SESSIONS.pop(request.cookies.get("session"), None)   # discard the pre-login id
    response.set_cookie("session", sid, httponly=True, secure=True)
```

## Q43: What is the difference between horizontal and vertical authentication bypass?
**A:** Horizontal bypass means accessing another user's account at the same privilege level (e.g., User A accessing User B's profile). Vertical bypass means gaining higher privileges than allowed (e.g., a regular user accessing admin functions). Both are authorization issues that occur after authentication.

**Code:**
```python
# Horizontal: same privilege, ANOTHER user
@app.get("/profile/{other}")
def view_profile(actor, other):
    if actor.id != other and not actor.is_admin:
        raise Forbidden                    # Horizontal AuthZ check

# Vertical: HIGHER privilege than allowed
@app.delete("/admin/users/{u}")
def delete_user(actor, u):
    if "admin" not in actor.roles:
        raise Forbidden                    # Vertical AuthZ check
```

## Q44: What is CAPTCHA and how does it help authentication?
**A:** CAPTCHA (Completely Automated Public Turing test to tell Computers and Humans Apart) presents challenges that are easy for humans but hard for bots. It helps prevent automated brute force attacks, credential stuffing, and account creation abuse on login and registration forms.

**Code:**
```python
import requests

def human_check(response_token):
    r = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={"secret": SECRET, "response": response_token,
              "remoteip": client_ip})
    return r.json()["success"]        # CAPTCHA gates the login form for bots
```

## Q45: What is rate limiting in authentication?
**A:** Rate limiting restricts the number of authentication attempts from a single IP address, user account, or device within a specific time window. It prevents brute force attacks, credential stuffing, and DoS attacks. Common limits are 5-10 failed attempts per minute.

**Code:**
```python
from collections import deque
from time import time

_attempts = {}                        # key -> recent timestamps

def rate_limit(key, limit=5, window=60):
    now = time()
    dq = _attempts.setdefault(key, deque())
    while dq and now - dq[0] > window:
        dq.popleft()
    if len(dq) >= limit:
        return False                  # too many tries -> reject
    dq.append(now)
    return True

if not rate_limit(client_ip):         # per-IP, per-account, per-device limits
    raise HTTPException(429, "Too many attempts")
```

## Q46: What is account lockout and its trade-offs?
**A:** Account lockout temporarily disables an account after a certain number of failed login attempts. While it prevents brute force attacks, it also enables denial-of-service attacks where attackers intentionally lock out legitimate users. Rate limiting is often preferred as a more measured approach.

**Code:**
```python
from time import time

FAILS = {}                            # user -> [login failure timestamps]

def login(user, password):
    if len(FAILS.get(user, [])) >= 5 and time() - FAILS[user][-1] < 900:
        raise AccountLocked           # 5 fails -> locked 15 min
    if check_password(user, password):
        FAILS.pop(user, None)
        return True
    FAILS.setdefault(user, []).append(time())
    return False
# trade-off: an attacker can lock out a victim => prefer throttling/rate limits
```

## Q47: What is credential stuffing?
**A:** Credential stuffing is an attack where automated tools use username/password pairs leaked from one service to try to log into other services. It exploits the common practice of password reuse across multiple sites. MFA and breached password detection help mitigate this.

**Code:**
```python
from collections import Counter

LEAKED = [("alice@x.com", "Summer2021!"), ("bob@y.com", "password123")]

def defend(login_events):
    per_ip = Counter(e.ip for e in login_events if not e.ok)
    for ip, fails in per_ip.items():
        if fails > 30:                        # automated velocity => block
            block(ip)
    for user, password in LEAKED:             # cross-check stolen pairs
        if password in breached_check(password):
            revoke(user)                      # force password reset
```

## Q48: What is WebAuthn?
**A:** WebAuthn (Web Authentication) is a W3C standard for passwordless authentication using public-key cryptography. It enables users to authenticate with biometrics, security keys, or platform authenticators (like Apple Touch ID or Windows Hello) instead of passwords.

**Code:**
```python
from webauthn import generate_registration_options, verify_registration_response

options = generate_registration_options(rp_id="example.com", user_name="alice")
# browser: navigator.credentials.create({publicKey: options})
# -> authenticator makes a keypair; only the PUBLIC key is sent back
verify_registration_response(expectations=options, response=client_response)
```

## Q49: What is FIDO2?
**A:** FIDO2 is a set of standards (including WebAuthn and CTAP) that enables passwordless authentication using public-key cryptography. It allows users to register devices (like YubiKeys or built-in platform authenticators) and authenticate with biometrics or PINs, providing phishing-resistant authentication.

**Code:**
```python
from webauthn import generate_authentication_options, verify_authentication_response

options = generate_authentication_options(rp_id="example.com")   # a challenge
# browser: navigator.credentials.get({publicKey: options})
# -> the keypair signs the challenge (FIDO2 = WebAuthn + CTAP)
verify_authentication_response(expectations=options, response=client_response)
```

## Q50: What is a passkey?
**A:** A passkey is a FIDO2-based credential that replaces passwords. It uses public-key cryptography: the private key stays on the user's device, and the public key is stored on the server. Passkeys sync across devices via cloud services (Apple Keychain, Google Password Manager) and are resistant to phishing.

**Code:**
```python
# FIDO2 passkey: the PRIVATE key never leaves the device
def new_passkey(user):
    cred = create_passkey(rp_id="example.com", user=user)
    return {"id": cred.credential_id, "public_key": cred.credential_public_key}

# login = a challenge SIGNATURE made by the private key
def verify_login(credential, signature, rp_id):
    return verify_passkey(credential, signature, rp_id="example.com")
```

## Q51: What is time-based one-time password (TOTP)?
**A:** TOTP is a temporary, one-time password generated using a shared secret key and the current time. It typically produces a 6-digit code valid for 30 seconds. TOTP is used in authenticator apps like Google Authenticator and Authy as a second factor.

**Code:**
```python
import base64, hashlib, hmac, struct, time

def totp(secret: bytes, step: int = 30) -> str:
    counter = int(time.time()) // step                    # time-synchronized
    digest = hmac.new(secret, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1_000_000
    return f"{code:06d}"
# 6 digits, valid for ~30 s, then the time window moves on
```

## Q52: What is HMAC-based one-time password (HOTP)?
**A:** HOTP is an event-based one-time password algorithm that uses a shared secret and a moving counter (incremented after each use). Unlike TOTP, it does not rely on time synchronization. Each code is valid until used, making it suitable for hardware tokens.

**Code:**
```python
import hashlib, hmac, struct

COUNTER = {}                                    # per-user moving counter (event-based)

def hotp(secret: bytes, counter: int) -> str:
    digest = hmac.new(secret, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF) % 1_000_000
    return f"{code:06d}"

def verify(user, secret, submitted):
    if hmac.compare_digest(hotp(secret, COUNTER.get(user, 0)), submitted):
        COUNTER[user] = COUNTER.get(user, 0) + 1          # counter moves on use
        return True
```

## Q53: What is SMS-based 2FA and why is it considered less secure?
**A:** SMS-based 2FA sends a one-time code via text message. It is considered less secure because of SIM swapping attacks (attacker convinces the carrier to transfer the phone number), SS7 protocol vulnerabilities, and the possibility of interception by malware. TOTP or hardware keys are preferred.

**Code:**
```python
import secrets

def send_sms_otp(phone):
    code = f"{secrets.randbelow(1_000_000):06d}"     # over SMS = cleartext
    sms.send(phone, f"Your code: {code}")

# WHY IT'S WEAKER:
#   1) SIM swapping reroutes the texts to the attacker
#   2) SS7 signalling is interceptable
#   3) device malware can read the message
def preferred():
    return totp(secret_from_authenticator_app)     # app-based TOTP instead
```

## Q54: What is SIM swapping?
**A:** SIM swapping (or SIM jacking) is an attack where the fraudster convinces a mobile carrier to transfer the victim's phone number to a SIM card the attacker controls. This allows the attacker to receive SMS-based 2FA codes and reset passwords, gaining access to accounts.

**Code:**
```python
import requests

def phone_carrier(number):
    # check the authoritative number-portability record
    r = requests.get(f"https://api.phone.example/portability/{number}").json()
    return r["carrier_id"]

def flag_sim_swap(user):
    if phone_carrier(user.phone) != user.carrier_on_record:
        user.require_step_up = True               # pause SMS 2FA, force re-verification
        alert(user)
```

## Q55: What is biometric authentication?
**A:** Biometric authentication uses unique biological characteristics to verify identity, such as fingerprints, facial patterns, iris scans, voice recognition, or behavioral patterns (typing rhythm, gait). It offers convenience but raises privacy concerns and cannot be reset like a password if compromised.

**Code:**
```python
# verify a fresh biometric capture against ONE stored template (claimed identity)
def verify(capture, claimed_user, threshold=0.98):
    score = matcher.compare(capture, TEMPLATES[claimed_user])
    return score >= threshold                # "Are you really Alice?"
```

## Q56: What is the difference between verification and identification in biometrics?
**A:** Verification (1:1 matching) confirms "Are you who you claim to be?" — compares the biometric against a specific stored template. Identification (1:N matching) answers "Who are you?" — compares against all stored templates to find a match.

**Code:**
```python
def verify(capture, claimed_id, threshold=0.98):
    # 1:1 - "Are you who you CLAIM to be?" compare against one template
    return matcher.compare(capture, Templates[claimed_id]) >= threshold

def identify(capture):
    # 1:N - "WHO are you?" search against every template
    best, best_score = "", 0.0
    for uid, tpl in Templates.items():
        s = matcher.compare(capture, tpl)
        if s > best_score:
            best, best_score = uid, s
    return best if best_score >= 0.98 else None
```

## Q57: What is a false acceptance rate (FAR) in biometrics?
**A:** FAR (False Acceptance Rate) is the probability that a biometric system incorrectly accepts an unauthorized user as legitimate. A lower FAR means higher security. It trades off against FRR (False Rejection Rate).

**Code:**
```python
def false_acceptance_rate(trials, threshold=0.9):
    impostors = [t for t in trials if t.impostor]
    wrongly_accepted = [t for t in impostors if match(t) >= threshold]
    return len(wrongly_accepted) / len(impostors)   # security: low FAR is better
```

## Q58: What is a false rejection rate (FRR) in biometrics?
**A:** FRR (False Rejection Rate) is the probability that a biometric system incorrectly rejects a legitimate user. A lower FRR means better usability. Systems must balance FAR and FRR based on the application's security requirements.

**Code:**
```python
def false_rejection_rate(trials, threshold=0.9):
    genuine = [t for t in trials if not t.impostor]
    wrongly_rejected = [t for t in genuine if match(t) < threshold]
    return len(wrongly_rejected) / len(genuine)     # usability: high FRR annoys users
```

## Q59: What is mutual authentication?
**A:** Mutual authentication (or two-way authentication) requires both parties in a communication to verify each other's identity before data exchange. In TLS, the server presents a certificate to the client (one-way), but with mutual TLS (mTLS), the client also presents a certificate to the server.

**Code:**
```python
import ssl, socket

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations("/ca.pem")                    # server must prove ITSELF
ctx.load_cert_chain("/client.crt", "/client.key")       # client proves ITSELF too
ctx.check_hostname = True

sock = ctx.wrap_socket(socket.socket(), server_hostname="api.example.com")
sock.connect(("api.example.com", 443))   # BOTH sides authenticated (mTLS)
```

## Q60: What is certificate-based authentication?
**A:** Certificate-based authentication uses digital certificates (X.509) to verify identity. The user presents a certificate signed by a trusted Certificate Authority (CA). The server verifies the certificate's validity, signature chain, and optionally checks revocation status via CRL or OCSP.

**Code:**
```python
from cryptography import x509

def verify_certificate(der, trusted_ca_pem):
    cert = x509.load_der_x509_certificate(der)
    ca = x509.load_pem_x509_certificate(trusted_ca_pem)
    try:
        cert.verify_directly_issued_by(ca)      # trust chain to a trusted CA
    except Exception:
        raise InvalidCertificate
    return cert.subject.rfc4514_string()        # identity from the X.509 subject
```

## Q61: What is client certificate authentication?
**A:** Client certificate authentication (or mutual TLS) is a method where the server requests and validates a certificate from the client during the TLS handshake. It provides strong, phishing-resistant authentication without passwords. It is commonly used in enterprise VPNs and API security.

**Code:**
```python
import ssl

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain("server.crt", "server.key")
ctx.load_verify_locations("client_cas.pem")   # CAs trusted to sign clients
ctx.verify_mode = ssl.CERT_REQUIRED           # no cert => handshake refused

# during the TLS handshake the server REQUESTS and VALIDATES a client certificate
# (mutual TLS / client-cert auth - phishing-resistant, no passwords)
```

## Q62: What is a Certificate Authority (CA)?
**A:** A CA is a trusted entity that issues digital certificates. The CA verifies the identity of the certificate requester and signs the certificate with its own private key. Browsers and operating systems ship with a list of trusted root CAs.

**Code:**
```python
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import NameOID

ca = x509.load_pem_x509_certificate(CA_PEM)
ca_key = serialization.load_pem_private_key(CA_KEY_PEM, password=None)

cert = (x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "api.example.com")]))
        .issuer_name(ca.subject)
        .public_key(server_public_key)
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.utcnow())
        .not_valid_after(datetime.utcnow() + timedelta(days=365))
        .sign(ca_key, hashes.SHA256()))      # the CA's authority makes it trusted
```

## Q63: What is a self-signed certificate?
**A:** A self-signed certificate is a certificate signed by its own creator rather than a trusted CA. It provides encryption but not identity verification. Self-signed certificates trigger browser warnings and are typically used only in development or internal environments.

**Code:**
```python
from datetime import datetime, timedelta
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "dev-server.local")])
self_signed = (x509.CertificateBuilder()
               .subject_name(name).issuer_name(name)      # issuer == subject!
               .public_key(key.public_key())
               .serial_number(x509.random_serial_number())
               .not_valid_before(datetime.utcnow())
               .not_valid_after(datetime.utcnow() + timedelta(days=30))
               .sign(key, hashes.SHA256()))               # signs ITSELF -> untrusted
```

## Q64: What is the difference between authentication and identification?
**A:** Identification is the act of claiming an identity (e.g., providing a username). Authentication is proving that identity claim is valid (e.g., providing the correct password). Identification without authentication carries no proof.

**Code:**
```python
def login(username, password):
    claimed = username                    # IDENTIFICATION: "I am bob"
    if user_exists(claimed) and verify_password(claimed, password):
        return Authenticated(claimed)     # AUTHENTICATION: the password PROVES it
    return None
```

## Q65: What is anonymous authentication?
**A:** Anonymous authentication allows users to access resources without revealing their identity. It is commonly used for public websites or resources that do not require user-specific access control. The system typically assigns a guest or anonymous user context.

**Code:**
```python
GUEST = Identity(anonymous=True)

def access(resource, identity):
    if not resource.requires_auth:
        return allow(identity or GUEST)       # public page, no identity needed
    if identity.is_anonymous:
        raise RequiresLogin
    return allow(identity)
```

## Q66: What is risk-based authentication (adaptive authentication)?
**A:** Risk-based authentication adjusts the authentication requirements based on the risk level of the access attempt. Factors include device, location, time, behavior patterns, and IP reputation. Low-risk actions may proceed without additional verification; high-risk actions trigger step-up authentication (e.g., MFA).

**Code:**
```python
def risk(ip, device, hour, velocity):
    s = 0
    if ip.reputation < 0.5: s += 30           # bad neighborhood IP
    if device not in user.known_devices: s += 30
    if hour in {2, 3, 4}: s += 20             # unusual time
    if velocity > 10: s += 20                 # logins per minute
    return s                                  # 0..100

def login(ip, device, hour, velocity):
    if risk(ip, device, hour, velocity) < 40:
        return issue_session(user)            # low risk: proceed
    return step_up(user)                      # high risk: prompt for MFA
```

## Q67: What is step-up authentication?
**A:** Step-up authentication requires users to provide additional authentication factors when accessing sensitive resources or performing high-risk actions. For example, viewing a profile page may only need a password, but making a payment may require MFA.

**Code:**
```python
AAL = {"aal1": 1, "aal2": 2, "aal3": 3}
REQUIRED = {"view_profile": "aal1", "make_payment": "aal2", "admin": "aal3"}

def check_step_up(claims, operation):
    if AAL[claims["acr"]] < AAL[REQUIRED[operation]]:
        return redirect("https://idp.example/authorize?acr_values=" + REQUIRED[operation])
    return proceed(operation)
```

## Q68: What is a token revocation mechanism?
**A:** Token revocation invalidates a token before its natural expiration. Approaches include: (1) maintaining a blacklist of revoked tokens, (2) using short-lived tokens with refresh token rotation, (3) versioned user secrets (incrementing a version invalidates all previous tokens).

**Code:**
```python
import jwt

REVOKED = set()                      # blacklist (kept small by short TTLs)

def revoke(token):
    REVOKED.add(token)               # immediate invalidation

def validate(token):
    if token in REVOKED:
        raise RevokedToken
    return jwt.decode(token, SECRET, algorithms=["HS256"])
# stateless JWTs can only be revoked this way - or by a very short exp
```

## Q69: What is token rotation?
**A:** Token rotation replaces a token with a new one each time it is used. For refresh tokens, each time a new access token is issued, the old refresh token is invalidated and a new one is returned. This limits the damage if a refresh token is stolen.

**Code:**
```python
import secrets

def refresh(refresh_token, user):
    if refresh_token != user.current_refresh:      # reuse of a consumed token
        revoke_all_for(user)
        raise ReauthenticationRequired             # theft signal
    user.current_refresh = secrets.token_urlsafe(48)     # OLD one is now invalid
    access = jwt.encode({"sub": user.id, "exp": now + 15 * 60}, ACCESS_SECRET)
    return access, user.current_refresh            # rotation: new refresh each time
```

## Q70: What is a refresh token reuse detection?
**A:** Refresh token reuse detection monitors if a revoked/used refresh token is presented again, which indicates token theft. When detected, all refresh tokens for that user are typically revoked, forcing re-authentication. This is a key security measure in OAuth 2.0.

**Code:**
```python
REFRESH_FAMILY = {}    # (client_id, user) -> {"gen": int, "current": hash}

def exchange(refresh_token, family):
    entry = REFRESH_FAMILY[family]
    if refresh_token.gen != entry["gen"]:
        revoke_entire_family(REFRESH_FAMILY, family)   # reuse == token theft
        raise ReauthenticationRequired
    entry["gen"] += 1                                  # rotate
    return issue_access(family), new_refresh_token(entry["gen"])
# a stolen token surfaces on the NEXT (re)use and burns the whole family
```

## Q71: What is a scope in OAuth 2.0?
**A:** A scope defines the specific permissions or access level requested by a client application. When requesting authorization, the client specifies scopes (e.g., `read`, `write`, `email`, `profile`). The authorization server displays these to the user for consent and limits the access token accordingly.

**Code:**
```python
import urllib.parse

url = ("https://as.example.com/authorize?" + urllib.parse.urlencode({
    "client_id": CLIENT_ID,
    "response_type": "code",
    "scope": "openid email write:orders",     # explicit, minimal scopes requested
    "state": state}))

def limit_scope(approved, requested):
    return [s for s in approved.split() if s in requested.split()]  # never grant more
```

## Q72: What is the principle of least privilege in authentication?
**A:** The principle of least privilege means giving users only the minimum permissions needed to perform their tasks. Applied to authentication, it means tokens should have the minimum necessary scopes, sessions should expire when no longer needed, and default access should be denied.

**Code:**
```python
ADMIN_ONLY = {"delete"}

def issue_token(user, requested):
    allowed = set(requested) & set(user.allowed_scopes)   # intersect, never union
    if "admin" not in user.roles:
        allowed -= ADMIN_ONLY                        # default-DENY extra privileges
    return jwt.encode({"sub": user.id, "scope": " ".join(sorted(allowed))}, SECRET)
```

## Q73: What is a service account?
**A:** A service account is a non-human identity used by applications, services, or automated processes to authenticate and interact with systems. Unlike user accounts, service accounts typically use API keys, certificates, or OAuth client credentials for authentication.

**Code:**
```python
# A service account identifies an APPLICATION, not a human
import jwt, requests

def call_payments(customer_id):
    svc_token = jwt.encode({"sub": "svc-billing-01", "aud": "payments-api"},
                           SERVICE_PRIVATE_KEY, algorithm="RS256")
    return requests.get("https://payments.example/api", headers={
        "Authorization": f"Bearer {svc_token}"})
```

## Q74: What is a machine-to-machine (M2M) authentication?
**A:** M2M authentication is the process where services or applications authenticate to each other without human intervention. It commonly uses OAuth 2.0 Client Credentials flow, API keys, mutual TLS, or JWTs signed with service account keys.

**Code:**
```python
import requests

def m2m_token():
    r = requests.post("https://as.example.com/token", data={
        "grant_type": "client_credentials",          # no human involved
        "scope": "inventory:read",
        "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion": signed_jwt(SERVICE_KEY), # JWT client auth (RFC 7523)
    })
    return r.json()["access_token"]
```

## Q75: What is API key authentication?
**A:** API key authentication uses a unique key assigned to a client to identify and authenticate API requests. The key is typically sent in headers (`X-API-Key`), query parameters, or basic auth. API keys are simpler than OAuth but offer less granularity and security.

**Code:**
```python
import hashlib, secrets

KEYS = {}

def issue_api_key(owner):
    key = "sk_live_" + secrets.token_urlsafe(32)     # shown ONCE at creation
    kid = secrets.token_urlsafe(8)
    KEYS[kid] = hashlib.sha256(key.encode()).hexdigest()   # store only the hash
    return key

def authenticate(x_api_key):
    digest = hashlib.sha256(x_api_key.encode()).hexdigest()
    return next((kid for kid, d in KEYS.items() if d == digest), None)
```

## Q76: What is HTTP Basic Authentication?
**A:** HTTP Basic Authentication sends the username and password concatenated with a colon, base64-encoded, in the `Authorization` header (`Authorization: Basic dXNlcjpwYXNz`). It is not secure by itself (base64 is easily decoded) and must only be used over HTTPS.

**Code:**
```python
import base64

# client side - NOT encryption, just encoding (base64 decodes trivially):
header = "Basic " + base64.b64encode(b"user:secret").decode()
# Authorization: Basic dXNlcjpzZWNyZXQ=

def server_verify(authorization):
    _, _, enc = authorization.partition(" ")
    username, _, pw = base64.b64decode(enc).decode().partition(":")
    return check_password(username, pw)         # HTTPS is mandatory
```

## Q77: What is HTTP Digest Authentication?
**A:** HTTP Digest Authentication improves on Basic Auth by using MD5 hashing of the password with a server-provided nonce. It avoids sending the password in plaintext but is still considered outdated and less secure than modern methods like OAuth or JWT.

**Code:**
```python
import hashlib

# server sends a NONCE; the client never transmits the raw password
def digest_response(method, uri, realm, nonce, username, password):
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{uri}".encode()).hexdigest()
    return hashlib.md5(f"{ha1}:{nonce}:{ha2}".encode()).hexdigest()
# the server recomputes the same digest to verify - but MD5 is now archaic
```

## Q78: What is Windows Authentication (NTLM/Kerberos)?
**A:** Windows Authentication includes NTLM (challenge-response) and Kerberos (ticket-based) protocols. NTLM is older and less secure. Kerberos is the default for Active Directory and provides SSO within a Windows domain. Both are commonly used for intranet applications.

**Code:**
```python
import requests
from requests_kerberos import HTTPKerberosAuth

# Kerberos (default in Active Directory): a KDC hands the client a SERVICE
# TICKET, the client presents it to the app -> SSO inside the Windows domain
r = requests.get("https://intranet.corp", auth=HTTPKerberosAuth())
# (NTLM is the older challenge-response variant - no longer recommended)
```

## Q79: What is RADIUS authentication?
**A:** RADIUS (Remote Authentication Dial-In User Service) is a networking protocol that provides centralized AAA (Authentication, Authorization, Accounting) for users connecting to network services. It is commonly used for VPN, Wi-Fi (802.1X), and network device access.

**Code:**
```python
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

client = Client(server="radius.example", secret=b"shared-secret",
                dict=Dictionary("dictionary"))
req = client.CreateAuthPacket(
    code=pyrad.packet.AccessRequest, User_Name="alice", NAS_IP_Address="10.0.0.9")
req["User-Password"] = req.PwCrypt("s3cret")      # encrypted with the shared secret
reply = client.SendPacket(req)                    # Access-Accept / Access-Reject
```

## Q80: What is a token endpoint in OAuth 2.0?
**A:** The token endpoint is an OAuth 2.0 server endpoint where clients exchange authorization codes, refresh tokens, or client credentials for access tokens. Requests to this endpoint are typically POST requests with the grant type and associated parameters.

**Code:**
```python
import requests

# token_endpoint: where codes/refresh/client creds are exchanged for ACCESS tokens
def exchange_auth_code(code):
    r = requests.post("https://as.example.com/token", data={
        "grant_type": "authorization_code",
        "code": code, "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
    return r.json()          # {"access_token": ..., "expires_in": 3600, ...}
```

## Q81: What is the authorization endpoint in OAuth 2.0?
**A:** The authorization endpoint is the OAuth 2.0 server endpoint where the user authenticates and grants consent. The client redirects the user here. After successful authentication and consent, the user is redirected back to the client with an authorization code (in the Authorization Code flow).

**Code:**
```python
import secrets, urllib.parse

state = secrets.token_urlsafe(16)
url = ("https://as.example.com/authorize?" + urllib.parse.urlencode({
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": "openid email",
    "state": state}))          # user authenticates AND consents at this endpoint
redirect(user, url)
```

## Q82: What is a redirect URI in OAuth?
**A:** A redirect URI (or callback URL) is the endpoint on the client application where the authorization server sends the user after authentication. It is registered with the authorization server during client setup and must be validated to prevent open redirect attacks.

**Code:**
```python
# redirect_uri must be REGISTERED with the AS and match EXACTLY
REGISTERED = {"https://app.example.com/callback", "myapp://oauth/callback"}

def validate_redirect_uri(uri):
    if uri not in REGISTERED:              # blocks open-redirect attacks
        raise InvalidRedirectURI
    return True
```

## Q83: What is the state parameter in OAuth 2.0?
**A:** The state parameter is a random value generated by the client and included in the authorization request. It is returned unchanged in the callback. It prevents CSRF attacks by allowing the client to verify that the response matches the original request.

**Code:**
```python
import secrets

state = secrets.token_urlsafe(16)
STORE[state] = request.session            # tie the state to THIS session
auth_url = f"https://as.example.com/authorize?response_type=code&client_id={CID}&state={state}"
redirect(user, auth_url)

def oauth_callback(params):
    if params["state"] not in STORE:      # attacker cannot predict/forge it
        abort(400, "CSRF on OAuth redirect")
    return STORE.pop(params["state"])
```

## Q84: What is a nonce in authentication?
**A:** A nonce (number used once) is a random or semi-random number generated for a specific authentication transaction. It prevents replay attacks by ensuring each authentication request is unique and cannot be reused. Nonces are used in various protocols including HTTP Digest and OIDC.

**Code:**
```python
import secrets

nonce = secrets.token_urlsafe(16)         # "number used ONCE"
# OIDC: the nonce is placed in the auth request and echoed in the ID token
id_claims = jwt.decode(raw_id_token, JWT_VERIFY_KEY, algorithms=["RS256"])
if id_claims["nonce"] != nonce or id_claims["iat"] < now - 300:
    raise ReplayDetected       # an old captured token can't be replayed
```

## Q85: What is a replay attack?
**A:** A replay attack occurs when an attacker intercepts a valid authentication message (e.g., a token or signed request) and retransmits it to trick the system into thinking it is from the original sender. Nonces, timestamps, and short expiration times prevent replay attacks.

**Code:**
```python
import secrets, time

def secure_request(action, payload, seen, ttl=300):
    if time.time() - payload["ts"] > ttl:
        return "expired"
    if payload["nonce"] in seen:
        return "replayed"               # every message carries a fresh nonce
    seen.add(payload["nonce"])
    return call_authenticated_action(action, payload)
```

## Q86: What is a man-in-the-middle (MITM) attack on authentication?
**A:** A MITM attack occurs when an attacker intercepts communication between the user and the server to steal credentials or tokens. HTTPS/TLS prevents MITM attacks by encrypting the communication channel. Public Wi-Fi networks are common vectors for MITM attacks.

**Code:**
```python
import ssl, socket

ctx = ssl.create_default_context()            # TLS = the MITM countermeasure
with ctx.wrap_socket(socket.socket(), server_hostname="api.example.com") as sock:
    sock.connect(("api.example.com", 443))    # encrypted + authenticated channel
    sock.sendall(b"Authorization: Bearer " + token)   # safe even on public Wi-Fi
# without TLS, an attacker sits in the middle of the key exchange
```

## Q87: What is a phishing attack in the context of authentication?
**A:** Phishing attacks trick users into revealing their credentials by presenting fake login pages that mimic legitimate services. Modern phishing can bypass 2FA by using reverse proxies (evilginx). Hardware security keys (FIDO2) are the most effective protection against phishing.

**Code:**
```python
# This is what origin binding looks like on the defence side (WebAuthn):
def verify_phishing_resistant(credential, expected_rp_id="example.com"):
    if credential.rp_id != expected_rp_id:
        raise PhishingAttempted       # a fake page has a different origin
    return verify_signature(credential)   # private key never leaves the authenticator
```

## Q88: What is credential harvesting?
**A:** Credential harvesting is the mass collection of usernames and passwords through phishing, data breaches, malwares, or social engineering. Harvested credentials are typically used for credential stuffing attacks or sold on darknet markets.

**Code:**
```python
# Harvested lists (phishing/breaches/malware) are tested in bulk.
# Defend by checking candidates against known breaches:
import hashlib, requests

def in_known_breach(password):
    h = hashlib.sha1(password.encode()).hexdigest().upper()
    r = requests.get(f"https://api.pwnedpasswords.com/range/{h[:5]}")  # k-anonymity
    return h[5:] in r.text                       # prefix search, nothing leaked
```

## Q89: What is passwordless authentication?
**A:** Passwordless authentication eliminates passwords entirely. Users authenticate using methods like magic links (email), one-time codes (SMS/email), biometrics (fingerprint/face), or security keys (FIDO2/WebAuthn). It improves security and user experience by removing the weakest link — passwords.

**Code:**
```python
import secrets

def passwordless_login(email):
    token = secrets.token_urlsafe(32)         # magic-link / OTP bearer
    store(token, email, ttl=600)
    send(email, f"https://app.example/auth?token={token}")

def redeem(token):
    email = consume(token)                    # one-time use, expires quickly
    return new_session(email) if email else None
```

## Q90: What are magic links?
**A:** Magic links are one-time-use URLs sent to the user's email that automatically authenticate them when clicked. The link contains a unique token, validates the user's email ownership, and logs them in. Magic links are a form of passwordless authentication.

**Code:**
```python
import secrets

def issue_magic_link(user):
    token = secrets.token_urlsafe(32)
    REDIS.setex(f"magic:{token}", 900, user.email)    # 15-minute TTL
    return f"https://app.example/auth?token={token}" # emailed to the user

def redeem(token):
    email = REDIS.get(f"magic:{token}")
    if not email:
        raise InvalidOrExpiredLink
    REDIS.delete(f"magic:{token}")                    # strictly single-use
    return new_session(email)
```

## Q91: What is social login?
**A:** Social login allows users to authenticate using their existing accounts from social platforms (Google, Facebook, GitHub, Apple, etc.) via OAuth 2.0/OIDC. It reduces friction, eliminates password fatigue, and delegates identity management to the social provider.

**Code:**
```python
import requests
# https://accounts.google.com/o/oauth2/v2/auth

def social_login(provider, code):
    cfg = PROVIDERS[provider]                     # OAuth 2.0 + OIDC under the hood
    tok = requests.post(cfg["token_url"], data={"grant_type": "authorization_code",
                                                "code": code,
                                                "redirect_uri": REDIRECT_URI,
                                                "client_id": cfg["client_id"],
                                                "client_secret": cfg["secret"]}).json()
    attrs = requests.get(cfg["userinfo_url"], headers={
        "Authorization": f"Bearer {tok['access_token']}"}).json()
    return find_or_create(provider, attrs["email"])
```

## Q92: How do you handle token expiration on the client side?
**A:** Options include: (1) Intercepting 401 responses and automatically refreshing the token, (2) Checking token expiration client-side (JWTs have an `exp` claim) and refreshing proactively, (3) Using an interceptor or middleware that queues failed requests and retries after refreshing.

**Code:**
```python
import time
import requests
import jwt as pyjwt

def expired(token):
    try:
        pyjwt.decode(token, options={"verify_signature": False, "require": ["exp"]})
        return False
    except pyjwt.ExpiredSignatureError:
        return True

def call(url, token, refresh):
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    if resp.status_code == 401 and expired(token):     # transparent refresh
        token = refresh()
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    return resp
```

## Q93: What is a sliding session expiration?
**A:** Sliding session expiration extends the session lifetime each time the user interacts with the application. If the user is active, the session TTL is reset. If inactive beyond the timeout, the session expires. This balances security with user convenience.

**Code:**
```python
import time

def on_request(sid):
    s = SESSIONS.get(sid)
    if not s or time.time() - s["last_seen"] > SLIDING_TIMEOUT:
        return None                 # idle past the limit -> logged out
    s["last_seen"] = time.time()    # activity RESETS the clock (sliding window)
    return s["user"]
```

## Q94: What is an absolute session timeout?
**A:** An absolute session timeout forces the user to re-authenticate after a fixed period regardless of activity. For example, a banking app might enforce re-authentication every 15 minutes. It provides stronger security than sliding expiration for sensitive applications.

**Code:**
```python
import time

def is_expired(sid):
    s = SESSIONS[sid]
    return time.time() - s["started"] >= ABSOLUTE_LIMIT   # hard cap, ignore activity
# banking example: 15-minute absolute timeout no matter how active the user is
```

## Q95: What is a key rotation strategy for JWT signing keys?
**A:** Key rotation periodically changes the secret key used to sign JWTs. A common strategy uses key IDs (kid) in the JWT header and maintains a list of valid keys. Old keys are kept for a transition period to validate already-issued tokens, then removed.

**Code:**
```python
import jwt

KEYS = {                       # kid -> symmetric secret (overlap during rotation)
    "2026-k1": b"old-key-still-honored",
    "2026-k2": b"new-signing-key",
}

def sign(claims):
    return jwt.encode(claims, KEYS["2026-k2"], algorithm="HS256",
                      headers={"kid": "2026-k2"})   # kid identifies the key

def verify(token):
    kid = jwt.get_unverified_header(token)["kid"]
    return jwt.decode(token, KEYS[kid], algorithms=["HS256"])
# retire "2026-k1" once every token signed with it has expired
```

## Q96: What is HMAC vs RSA for JWT signing?
**A:** HMAC (HS256) uses a symmetric shared secret — the same key signs and verifies tokens. RSA (RS256) uses asymmetric key pairs — the private key signs, the public key verifies. RSA is preferred for multi-service architectures since only the issuer holds the private key.

**Code:**
```python
import jwt

# HS256: ONE shared secret signs AND verifies
token = jwt.encode({"sub": "u1"}, SHARED_SECRET, algorithm="HS256")
jwt.decode(token, SHARED_SECRET, algorithms=["HS256"])

# RS256: private key signs, PUBLIC key verifies (asymmetric)
token = jwt.encode({"sub": "u1"}, PRIVATE_KEY, algorithm="RS256")
jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
# -> many services can verify without ever holding the signing key
```

## Q97: What is a user info endpoint in OIDC?
**A:** The user info endpoint is an OIDC endpoint that returns claims about the authenticated user. It is accessed using the access token. If the ID token contains essential claims, the user info endpoint provides additional profile information via a REST API.

**Code:**
```python
import requests

def fetch_profile(access_token):
    r = requests.get("https://as.example.com/userinfo",
                     headers={"Authorization": f"Bearer {access_token}"})
    return r.json()          # {"sub": "u1", "email": "a@b.co", "name": "Ada"}
```

## Q98: What is an ID token in OIDC?
**A:** An ID token is a JWT issued by the OIDC provider that contains claims about the authenticated user, such as `sub` (subject identifier), `email`, `name`, and `iss` (issuer). It is obtained alongside the access token and is used for authentication (not API access).

**Code:**
```python
import jwt

# ID token = JWT about the USER (authentication), let's claim it:
claims = jwt.decode(raw_id_token, JWKS, algorithms=["RS256"],
                    audience=CLIENT_ID, issuer="https://accounts.example.com")
assert claims["sub"] == "117219219"          # user subject
assert claims["iss"] == "https://accounts.example.com"   # who issued it
# use for identity, never for API authorization (that is the access token's job)
```

## Q99: What is the difference between `sub` and `iss` claims in a JWT?
**A:** `sub` (subject) identifies the user or entity the token is about. `iss` (issuer) identifies who issued the token. Together, `iss` + `sub` provides a globally unique identity. For example, `iss: "https://accounts.google.com"` and `sub: "12345"` uniquely identifies a Google user.

**Code:**
```python
import jwt

claims = jwt.decode(token, JWKS, algorithms=["RS256"], audience=CLIENT_ID)
key = (claims["iss"], claims["sub"])         # issuer + subject = globally unique
# ("https://accounts.google.com", "117219219") pins ONE specific Google user
```

## Q100: What is the authentication flow for a typical SPA (Single Page Application)?
**A:** The recommended flow for SPAs is OAuth 2.0 Authorization Code with PKCE. The SPA redirects the user to the authorization server, the user authenticates, the server returns an authorization code, the SPA exchanges it (with PKCE) for tokens. Access tokens are short-lived. Refresh tokens should be stored securely (preferably HTTP-only cookies from a backend).

**Code:**
```python
import base64, hashlib, secrets, requests

verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()

# 1) SPA (public client) launches Authorization Code + PKCE
auth_url = "https://as.example.com/authorize?response_type=code&client_id=%s&code_challenge=%s" % (
    SPA_CLIENT_ID, challenge)
# 2) code returns -> exchange it:
r = requests.post("https://as.example.com/token", data={
    "grant_type": "authorization_code", "code": code,
    "code_verifier": verifier, "client_id": SPA_CLIENT_ID})
tokens = r.json()          # short-lived access token + refresh token
# 3) keep the refresh token on the BACKEND (BFF / HTTP-only cookie), not in JS
```
