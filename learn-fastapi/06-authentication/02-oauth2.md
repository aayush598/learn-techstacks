# OAuth2 with FastAPI

## Table of Contents

1. [OAuth2 Flows](#oauth2-flows)
2. [OAuth2 with FastAPI](#oauth2-with-fastapi)
3. [OAuth2PasswordRequestForm](#oauth2passwordrequestform)
4. [OAuth2PasswordBearer](#oauth2passwordbearer)
5. [Scopes](#scopes)
6. [OAuth2 with Third-Party Providers](#oauth2-with-third-party-providers)
7. [PKCE](#pkce)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## OAuth2 Flows

OAuth2 is an authorization framework that allows third-party applications to obtain limited access to a service.

### Authorization Code Flow

```
1. User clicks "Login with Google"
2. Redirect to Google's authorization endpoint
3. User authenticates with Google
4. Google redirects back with authorization code
5. App exchanges code for tokens
6. App uses access token to call API
```

**Used for:** Web applications, mobile apps with PKCE

### Client Credentials Flow

```
1. Application sends client_id + client_secret to token endpoint
2. Token endpoint validates and returns access token
3. Application uses access token to call API
```

**Used for:** Machine-to-machine (M2M), backend services

### Password Grant (Resource Owner)

```
1. User sends username + password directly to application
2. Application sends credentials to authorization server
3. Authorization server returns access token
4. Application uses access token to call API
```

**Used for:** Trusted first-party applications only (deprecated in OAuth 2.1)

### Implicit Flow (Deprecated)

```
1. User redirected to authorization endpoint
2. User authenticates
3. Access token returned directly in URL fragment
4. Application extracts token from URL
```

**Used for:** Legacy SPA apps (use Authorization Code + PKCE instead)

---

## OAuth2 with FastAPI

### Complete Setup

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",          # Endpoint to get token
    scopes={"read": "Read access", "write": "Write access"},
)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Authenticate user
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Create token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected/")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # Token is automatically extracted from Authorization header
    user = get_current_user(token)
    return {"user": user}
```

### Custom OAuth2 Scheme

```python
from fastapi.security import OAuth2

class CustomOAuth2(OAuth2):
    def __init__(self):
        super().__init__(
            tokenUrl="token",
            scheme_name="CustomOAuth2",
            scopes={
                "user:read": "Read user data",
                "user:write": "Write user data",
                "admin": "Admin access",
            },
        )

custom_oauth2 = CustomOAuth2()

@app.get("/users/")
async def list_users(token: str = Depends(custom_oauth2)):
    ...
```

---

## OAuth2PasswordRequestForm

### Form Fields

```python
from fastapi.security import OAuth2PasswordRequestForm

# Expects form data with:
# - username (required)
# - password (required)
# - grant_type (required, must be "password")
# - scope (optional, space-delimited)
# - client_id (optional)
# - client_secret (optional)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # form_data.username
    # form_data.password
    # form_data.scopes  # List of requested scopes
    # form_data.client_id
    # form_data.client_secret
    ...
```

### Custom Form Model

```python
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str
    device_id: str | None = None

@app.post("/token")
async def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401)

    token = create_access_token(
        data={
            "sub": user.username,
            "device_id": data.device_id,
        }
    )
    return {"access_token": token, "token_type": "bearer"}
```

---

## OAuth2PasswordBearer

### Configuration Options

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",                          # Token endpoint
    scheme_name="Bearer",                      # Scheme name for OpenAPI
    description="JWT Bearer token",            # Description for docs
    auto_error=True,                           # Auto-raise 401 if no token
    scopes={
        "read": "Read access",
        "write": "Write access",
    },
)

# auto_error=False: Returns None if no token (allows anonymous access)
# auto_error=True: Raises 401 if no token (default)
```

### With Authorization Header

```python
# Client sends:
# Authorization: Bearer <token>

# FastAPI extracts the token automatically
@app.get("/me")
async def get_me(token: str = Depends(oauth2_scheme)):
    # token = "<token>" (without "Bearer " prefix)
    user = decode_token(token)
    return user
```

---

## Scopes

### Defining Scopes

```python
from fastapi import Security

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "user:read": "Read user information",
        "user:write": "Modify user information",
        "item:read": "Read items",
        "item:write": "Create and modify items",
        "admin:read": "Read admin data",
        "admin:write": "Modify admin data",
    },
)

@app.get("/users/")
async def list_users(
    token: str = Security(oauth2_scheme, scopes=["user:read"])
):
    ...

@app.post("/users/")
async def create_user(
    token: str = Security(oauth2_scheme, scopes=["user:write"])
):
    ...

@app.get("/admin/")
async def admin_dashboard(
    token: str = Security(oauth2_scheme, scopes=["admin:read", "admin:write"])
):
    ...
```

### Token with Scopes

```python
def create_access_token(data: dict, scopes: list[str] = None):
    to_encode = data.copy()
    if scopes:
        to_encode["scopes"] = scopes
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# Include scopes in token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    scopes = get_user_scopes(user)  # Get user's allowed scopes
    access_token = create_access_token(
        data={"sub": user.username},
        scopes=scopes,
    )
    return {"access_token": access_token, "token_type": "bearer"}
```

### Scope Validation

```python
from fastapi import Security

def verify_scope(required_scopes: list[str]):
    def scope_checker(
        token: str = Security(oauth2_scheme, scopes=required_scopes)
    ):
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        token_scopes = payload.get("scopes", [])

        for scope in required_scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=403,
                    detail=f"Missing required scope: {scope}",
                )
        return payload
    return scope_checker

@app.get("/admin/")
async def admin_route(
    payload: dict = Depends(verify_scope(["admin:read", "admin:write"]))
):
    return {"message": "Admin access granted"}
```

---

## OAuth2 with Third-Party Providers

### Google OAuth2

```python
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

config = Config(environ={
    "GOOGLE_CLIENT_ID": "your-client-id",
    "GOOGLE_CLIENT_SECRET": "your-client-secret",
})

oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

@app.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    # Find or create user
    user = await get_or_create_user(
        email=user_info["email"],
        name=user_info["name"],
        provider="google",
    )

    # Create JWT
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

### GitHub OAuth2

```python
oauth.register(
    name="github",
    client_id="your-github-client-id",
    client_secret="your-github-client-secret",
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com/",
    client_kwargs={"scope": "user:email"},
)

@app.get("/auth/github")
async def github_login(request: Request):
    redirect_uri = request.url_for("github_callback")
    return await oauth.github.authorize_redirect(request, redirect_uri)

@app.get("/auth/github/callback")
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    resp = await oauth.github.get("user", token=token)
    profile = resp.json()

    user = await get_or_create_user(
        email=profile["email"],
        name=profile["name"],
        provider="github",
    )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## PKCE

### What is PKCE?

Proof Key for Code Exchange (RFC 7636) protects the authorization code flow from interception attacks. Required for public clients (mobile apps, SPAs).

### Implementation

```python
import hashlib
import base64
import secrets

def generate_pkce():
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = (
        base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        )
        .rstrip(b"=")
        .decode()
    )
    return code_verifier, code_challenge

@app.get("/auth/authorize")
async def authorize(request: Request):
    code_verifier, code_challenge = generate_pkce()

    # Store code_verifier in session
    request.session["code_verifier"] = code_verifier

    # Redirect to provider with code_challenge
    redirect_url = (
        f"https://provider.com/authorize?"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )
    return RedirectResponse(redirect_url)

@app.get("/auth/callback")
async def callback(request: Request, code: str):
    code_verifier = request.session["code_verifier"]

    # Exchange code with code_verifier
    token = await exchange_code(code, code_verifier)
    return token
```

---

## Best Practices

### 1. Always Use HTTPS

```python
# Production: Force HTTPS
@app.middleware("http")
async def https_redirect(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url)
    return await call_next(request)
```

### 2. Validate Redirect URIs

```python
ALLOWED_REDIRECT_URIS = [
    "https://myapp.com/callback",
    "https://myapp.com/auth/callback",
]

@app.get("/auth/authorize")
async def authorize(redirect_uri: str):
    if redirect_uri not in ALLOWED_REDIRECT_URIS:
        raise HTTPException(400, "Invalid redirect URI")
```

### 3. Use PKCE for Public Clients

```python
# Always use PKCE for:
# - Single Page Applications (SPAs)
# - Mobile applications
# - Desktop applications
# - Any client that can't securely store a client_secret
```

### 4. Store Secrets Securely

```python
# Use environment variables
import os

CLIENT_SECRET = os.getenv("OAUTH_CLIENT_SECRET")

# Or use a secrets manager
from aws_secretsmanager import get_secret
CLIENT_SECRET = get_secret("oauth/client_secret")
```

---

## Interview Questions

### Q1: What is OAuth2?
**Answer:** OAuth2 is an authorization framework that allows third-party applications to obtain limited access to a service. It provides flows for different client types (web, mobile, server) and supports delegated authorization.

### Q2: What is the difference between OAuth2 and OpenID Connect?
**Answer:** OAuth2 is for authorization (what you can access). OpenID Connect is built on OAuth2 and adds authentication (who you are). OIDC provides ID tokens and standard claims like `email`, `name`, `profile`.

### Q3: When should you use Client Credentials flow?
**Answer:** For machine-to-machine (M2M) communication where no user is involved. Backend services authenticating with other backend services. No user interaction required.

### Q4: What is PKCE and why is it needed?
**Answer:** Proof Key for Code Exchange protects the authorization code flow from interception. The client generates a code_verifier, sends its hash (code_challenge) with the authorization request, and proves possession of the original during token exchange.

### Q5: Why was the Password Grant deprecated?
**Answer:** It requires users to send credentials directly to the client application, which is a security risk. It doesn't support multi-factor authentication. OAuth 2.1 removes it in favor of Authorization Code + PKCE.

### Q6: How do scopes work in OAuth2?
**Answer:** Scopes define the level of access granted. The client requests specific scopes during authorization. The user approves scopes. The token contains granted scopes. The API validates scopes for each request.

### Q7: What is the difference between OAuth2 Bearer token and API key?
**Answer:** OAuth2 Bearer tokens are short-lived, revocable, and carry user identity. API keys are long-lived, tied to an application (not user), and simpler. OAuth2 is for user authorization; API keys are for application identification.

### Q8: How do you implement refresh token rotation?
**Answer:** Issue a new refresh token with each access token refresh. Revoke the old refresh token. Store token family for revocation chains. If a reused old refresh token is detected, revoke the entire family.

---

## Summary

OAuth2 in FastAPI provides flexible authorization for different client types. Use Authorization Code + PKCE for web/mobile apps, Client Credentials for M2M. Always validate redirect URIs, use PKCE, and store secrets securely. For third-party login, use libraries like Authlib.
