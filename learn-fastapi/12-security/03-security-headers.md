# Security Headers

## Table of Contents

1. [Introduction](#1-introduction)
2. [Security Headers Middleware](#2-middleware)
3. [Content-Security-Policy](#3-csp)
4. [X-Frame-Options](#4-x-frame)
5. [X-Content-Type-Options](#5-content-type)
6. [Strict-Transport-Security](#6-hsts)
7. [X-XSS-Protection](#7-xss-protection)
8. [Referrer-Policy](#8-referrer)
9. [Permissions-Policy](#9-permissions)
10. [Additional Headers](#10-additional)
11. [Helmet-Style Middleware](#11-helmet)
12. [Best Practices](#12-best-practices)

---

## 1. Introduction <a name="1-introduction"></a>

Security headers are HTTP response headers that tell browsers how to behave when
handling your site's content. They protect against common attacks like XSS, clickjacking,
MIME sniffing, and more.

### Why Security Headers Matter

- **XSS Protection**: Prevent injection of malicious scripts
- **Clickjacking Prevention**: Stop embedding in iframes
- **MIME Sniffing Prevention**: Force browser to respect declared content types
- **HTTPS Enforcement**: Ensure encrypted connections
- **Information Disclosure**: Limit what browsers can share with other sites

### Testing Security Headers

```bash
# Online tools
# https://securityheaders.com
# https://www.ssllabs.com/ssltest/

# Command line
curl -I https://yourapp.com
```

---

## 2. Security Headers Middleware <a name="2-middleware"></a>

### Basic Middleware

```python
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

app = FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains; preload"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### Advanced Middleware with Configuration

```python
from pydantic_settings import BaseSettings

class SecuritySettings(BaseSettings):
    # CSP
    CSP_DEFAULT_SRC: str = "'self'"
    CSP_SCRIPT_SRC: str = "'self'"
    CSP_STYLE_SRC: str = "'self' 'unsafe-inline'"
    CSP_IMG_SRC: str = "'self' data: https:"
    CSP_FONT_SRC: str = "'self' data:"
    CSP_CONNECT_SRC: str = "'self'"
    CSP_FRAME_ANCESTORS: str = "'none'"
    CSP_BASE_URI: str = "'self'"
    CSP_FORM_ACTION: str = "'self'"
    CSP_UPGRADE_INSECURE_REQUESTS: bool = True

    # HSTS
    HSTS_MAX_AGE: int = 31536000
    HSTS_INCLUDE_SUBDOMAINS: bool = True
    HSTS_PRELOAD: bool = True

    # Other headers
    X_FRAME_OPTIONS: str = "DENY"
    REFERRER_POLICY: str = "strict-origin-when-cross-origin"

    class Config:
        env_prefix = "SECURITY_"

settings = SecuritySettings()

def get_csp_header() -> str:
    """Build Content-Security-Policy header."""
    directives = [
        f"default-src {settings.CSP_DEFAULT_SRC}",
        f"script-src {settings.CSP_SCRIPT_SRC}",
        f"style-src {settings.CSP_STYLE_SRC}",
        f"img-src {settings.CSP_IMG_SRC}",
        f"font-src {settings.CSP_FONT_SRC}",
        f"connect-src {settings.CSP_CONNECT_SRC}",
        f"frame-ancestors {settings.CSP_FRAME_ANCESTORS}",
        f"base-uri {settings.CSP_BASE_URI}",
        f"form-action {settings.CSP_FORM_ACTION}",
    ]

    if settings.CSP_UPGRADE_INSECURE_REQUESTS:
        directives.append("upgrade-insecure-requests")

    return "; ".join(directives)

def get_hsts_header() -> str:
    """Build Strict-Transport-Security header."""
    parts = [f"max-age={settings.HSTS_MAX_AGE}"]
    if settings.HSTS_INCLUDE_SUBDOMAINS:
        parts.append("includeSubDomains")
    if settings.HSTS_PRELOAD:
        parts.append("preload")
    return "; ".join(parts)

class ConfigurableSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["Content-Security-Policy"] = get_csp_header()
        response.headers["Strict-Transport-Security"] = get_hsts_header()
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = settings.X_FRAME_OPTIONS
        response.headers["Referrer-Policy"] = settings.REFERRER_POLICY
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        return response

app.add_middleware(ConfigurableSecurityMiddleware)
```

---

## 3. Content-Security-Policy <a name="3-csp"></a>

### What It Is

CSP prevents XSS, clickjacking, and other code injection attacks by specifying
which dynamic resources are allowed to load.

### Common Directives

```python
csp_header = {
    # Default - applies to all resource types
    "default-src": "'self'",

    # JavaScript
    "script-src": "'self' 'unsafe-inline' https://cdn.example.com",

    # CSS
    "style-src": "'self' 'unsafe-inline' https://fonts.googleapis.com",

    # Images
    "img-src": "'self' data: https: blob:",

    # Fonts
    "font-src": "'self' data: https://fonts.gstatic.com",

    # AJAX/WebSocket
    "connect-src": "'self' https://api.example.com wss://ws.example.com",

    # Frames
    "frame-src": "'self' https://www.youtube.com",
    "frame-ancestors": "'none'",

    # Media
    "media-src": "'self' https://cdn.example.com",

    # Objects
    "object-src": "'none'",

    # Base URI
    "base-uri": "'self'",

    # Form submission
    "form-action": "'self'",

    # Upgrade insecure requests
    "upgrade-insecure-requests": "",
}
```

### CSP in FastAPI

```python
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class CSPMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, csp_config: dict = None):
        super().__init__(app)
        self.csp_config = csp_config or {
            "default-src": "'self'",
            "script-src": "'self'",
            "style-src": "'self' 'unsafe-inline'",
            "img-src": "'self' data:",
            "font-src": "'self' data:",
            "connect-src": "'self'",
            "frame-ancestors": "'none'",
            "base-uri": "'self'",
            "form-action": "'self'",
        }

    def build_csp_header(self) -> str:
        directives = []
        for directive, value in self.csp_config.items():
            if value:
                directives.append(f"{directive} {value}")
            else:
                directives.append(directive)
        return "; ".join(directives)

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = self.build_csp_header()
        return response

app.add_middleware(CSPMiddleware)
```

### CSP Reporting

```python
class CSPReportMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/csp-report":
            body = await request.body()
            report = json.loads(body)
            logger.warning("CSP Violation", report=report)
            return Response(status_code=204)

        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "..."
        response.headers["Content-Security-Policy-Report-Only"] = (
            "default-src 'self'; report-uri /csp-report"
        )
        return response

@app.post("/csp-report")
async def csp_report(request: Request):
    body = await request.body()
    report = json.loads(body)
    # Log or store the CSP violation
    logger.warning("CSP Violation", report=report)
    return Response(status_code=204)
```

---

## 4. X-Frame-Options <a name="4-x-frame"></a>

### What It Is

Prevents your site from being embedded in iframes, preventing clickjacking attacks.

### Values

- `DENY`: Cannot be framed at all
- `SAMEORIGIN`: Can only be framed by same origin
- `ALLOW-FROM https://example.com`: Can only be framed by specified origin (deprecated)

### Implementation

```python
class XFrameOptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        return response

# Or allow same-origin only
class XFrameSameOriginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        return response
```

### CSP Alternative

```python
# Modern approach using CSP
response.headers["Content-Security-Policy"] = "frame-ancestors 'none'"

# Or allow specific origins
response.headers["Content-Security-Policy"] = "frame-ancestors 'self' https://trusted.com"
```

---

## 5. X-Content-Type-Options <a name="5-content-type"></a>

### What It Is

Prevents browsers from MIME-sniffing a response away from the declared content type,
protecting against MIME confusion attacks.

### Implementation

```python
class ContentTypeOptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response
```

### Why It Matters

Without this header, a browser might:
1. Receive a file declared as `text/plain`
2. "Sniff" that it's actually HTML
3. Execute the HTML, leading to XSS

With `nosniff`, the browser strictly follows the declared Content-Type.

---

## 6. Strict-Transport-Security <a name="6-hsts"></a>

### What It Is

HSTS tells browsers to only use HTTPS for the specified period, preventing
protocol downgrade attacks and cookie hijacking.

### Implementation

```python
class HSTSMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        max_age: int = 31536000,  # 1 year
        include_subdomains: bool = True,
        preload: bool = True,
    ):
        super().__init__(app)
        self.max_age = max_age
        self.include_subdomains = include_subdomains
        self.preload = preload

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        hsts_value = f"max-age={self.max_age}"
        if self.include_subdomains:
            hsts_value += "; includeSubDomains"
        if self.preload:
            hsts_value += "; preload"

        response.headers["Strict-Transport-Security"] = hsts_value
        return response

app.add_middleware(
    HSTSMiddleware,
    max_age=31536000,
    include_subdomains=True,
    preload=True,
)
```

### Production Configuration

```python
# Always redirect HTTP to HTTPS first
@app.middleware("http")
async def redirect_to_https(request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)
```

---

## 7. X-XSS-Protection <a name="7-xss-protection"></a>

### What It Is

Enables the browser's built-in XSS filter (deprecated in modern browsers, but
still useful for older ones).

### Implementation

```python
class XSSProtectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        # Enable XSS protection and block the page if detected
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
```

### Modern Alternative

Use Content-Security-Policy instead, as `X-XSS-Protection` is deprecated:

```python
# CSP is the modern approach
response.headers["Content-Security-Policy"] = "script-src 'self'"
```

---

## 8. Referrer-Policy <a name="8-referrer"></a>

### What It Is

Controls how much referrer information browsers include with requests.

### Values

- `no-referrer`: Never send referrer
- `no-referrer-when-downgrade`: No referrer for HTTP→HTTPS
- `origin`: Send only origin (not full URL)
- `origin-when-cross-origin`: Full URL for same-origin, origin for cross-origin
- `same-origin`: Referrer for same-origin only
- `strict-origin`: Send origin for HTTPS, nothing for HTTP
- `strict-origin-when-cross-origin`: Best balance of security and functionality

### Implementation

```python
class ReferrerPolicyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, policy: str = "strict-origin-when-cross-origin"):
        super().__init__(app)
        self.policy = policy

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Referrer-Policy"] = self.policy
        return response

app.add_middleware(ReferrerPolicyMiddleware, policy="strict-origin-when-cross-origin")
```

---

## 9. Permissions-Policy <a name="9-permissions"></a>

### What It Is

Controls which browser features and APIs can be used by the page and its iframes.

### Common Directives

```python
permissions_policy = {
    "camera": "()",
    "microphone": "()",
    "geolocation": "()",
    "payment": "()",
    "usb": "()",
    "magnetometer": "()",
    "gyroscope": "()",
    "accelerometer": "()",
    "autoplay": "()",
    "fullscreen": "(self)",
    "picture-in-picture": "(self)",
    "screen-wake-lock": "(self)",
    "web-share": "(self)",
}

# Build header
policy_header = ", ".join(
    f"{feature}={value}" for feature, value in permissions_policy.items()
)
```

### Implementation

```python
class PermissionsPolicyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, policy: dict = None):
        super().__init__(app)
        self.policy = policy or {
            "camera": "()",
            "microphone": "()",
            "geolocation": "()",
            "payment": "()",
        }

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        policy_str = ", ".join(
            f"{k}={v}" for k, v in self.policy.items()
        )
        response.headers["Permissions-Policy"] = policy_str
        return response
```

---

## 10. Additional Headers <a name="10-additional"></a>

### Cross-Origin Policies

```python
class CrossOriginMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Prevent Spectre attacks
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # Prevent cross-domain policy loading
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        return response
```

### Cache Control for Sensitive Data

```python
class CacheControlMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, private_paths: list[str] = None):
        super().__init__(app)
        self.private_paths = private_paths or [
            "/api/", "/auth/", "/admin/"
        ]

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Set cache control for sensitive paths
        if any(request.url.path.startswith(path) for path in self.private_paths):
            response.headers["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, private"
            )
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        return response
```

### Additional Security Headers

```python
class FullSecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # Core security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # HSTS (only for HTTPS)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )

        # Referrer
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        # Cross-origin isolation
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

        # Information leakage prevention
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        # Remove server header (if present)
        if "server" in response.headers:
            del response.headers["server"]

        return response
```

---

## 11. Helmet-Style Middleware <a name="11-helmet"></a>

### Complete Security Headers Package

```python
from pydantic_settings import BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersConfig(BaseSettings):
    """Configuration for all security headers."""

    # CSP
    csp_default_src: str = "'self'"
    csp_script_src: str = "'self'"
    csp_style_src: str = "'self' 'unsafe-inline'"
    csp_img_src: str = "'self' data: https:"
    csp_font_src: str = "'self' data:"
    csp_connect_src: str = "'self'"
    csp_frame_ancestors: str = "'none'"
    csp_base_uri: str = "'self'"
    csp_form_action: str = "'self'"
    csp_upgrade_insecure: bool = True

    # HSTS
    hsts_max_age: int = 31536000
    hsts_include_subdomains: bool = True
    hsts_preload: bool = True

    # Frame
    x_frame_options: str = "DENY"

    # Referrer
    referrer_policy: str = "strict-origin-when-cross-origin"

    # Permissions
    permissions_policy: str = "camera=(), microphone=(), geolocation=()"

    # XSS
    x_xss_protection: str = "1; mode=block"

    # Content Type
    x_content_type_options: str = "nosniff"

    # Cross-origin
    coep: str = "require-corp"
    coop: str = "same-origin"
    corp: str = "same-origin"

    class Config:
        env_prefix = "SECURITY_HEADERS_"

class HelmetMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, config: SecurityHeadersConfig = None):
        super().__init__(app)
        self.config = config or SecurityHeadersConfig()

    def build_csp(self) -> str:
        directives = [
            f"default-src {self.config.csp_default_src}",
            f"script-src {self.config.csp_script_src}",
            f"style-src {self.config.csp_style_src}",
            f"img-src {self.config.csp_img_src}",
            f"font-src {self.config.csp_font_src}",
            f"connect-src {self.config.csp_connect_src}",
            f"frame-ancestors {self.config.csp_frame_ancestors}",
            f"base-uri {self.config.csp_base_uri}",
            f"form-action {self.config.csp_form_action}",
        ]
        if self.config.csp_upgrade_insecure:
            directives.append("upgrade-insecure-requests")
        return "; ".join(directives)

    def build_hsts(self) -> str:
        parts = [f"max-age={self.config.hsts_max_age}"]
        if self.config.hsts_include_subdomains:
            parts.append("includeSubDomains")
        if self.config.hsts_preload:
            parts.append("preload")
        return "; ".join(parts)

    async def dispatch(self, request, call_next):
        response = await call_next(request)

        # CSP
        response.headers["Content-Security-Policy"] = self.build_csp()

        # HSTS (HTTPS only)
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = self.build_hsts()

        # Frame protection
        response.headers["X-Frame-Options"] = self.config.x_frame_options

        # XSS protection
        response.headers["X-XSS-Protection"] = self.config.x_xss_protection

        # Content type
        response.headers["X-Content-Type-Options"] = self.config.x_content_type_options

        # Referrer
        response.headers["Referrer-Policy"] = self.config.referrer_policy

        # Permissions
        response.headers["Permissions-Policy"] = self.config.permissions_policy

        # Cross-origin
        response.headers["Cross-Origin-Embedder-Policy"] = self.config.coep
        response.headers["Cross-Origin-Opener-Policy"] = self.config.coop
        response.headers["Cross-Origin-Resource-Policy"] = self.config.corp

        # Remove server identification
        response.headers.pop("server", None)

        return response

# Usage
app = FastAPI()
config = SecurityHeadersConfig()
app.add_middleware(HelmetMiddleware, config=config)
```

### Testing Security Headers

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)

def test_security_headers_present(client):
    response = client.get("/")
    assert "x-content-type-options" in response.headers
    assert response.headers["x-content-type-options"] == "nosniff"

def test_csp_header(client):
    response = client.get("/")
    assert "content-security-policy" in response.headers
    csp = response.headers["content-security-policy"]
    assert "default-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp

def test_hsts_header(client):
    response = client.get("/")
    assert "strict-transport-security" in response.headers

def test_no_server_header(client):
    response = client.get("/")
    assert "server" not in response.headers

def test_x_frame_options(client):
    response = client.get("/")
    assert response.headers["x-frame-options"] == "DENY"

def test_referrer_policy(client):
    response = client.get("/")
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
```

---

## 12. Best Practices <a name="12-best-practices"></a>

### 1. Always Use HTTPS in Production

```python
# Redirect HTTP to HTTPS
@app.middleware("http")
async def https_redirect(request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url, status_code=301)
    return await call_next(request)
```

### 2. Set CSP in Report-Only Mode First

```python
# Test CSP without breaking functionality
response.headers["Content-Security-Policy-Report-Only"] = csp_header
response.headers["Content-Security-Policy-Report-Only"] += "; report-uri /csp-report"
```

### 3. Use Environment-Based Configuration

```python
# Different headers for different environments
if settings.ENVIRONMENT == "production":
    app.add_middleware(HelmetMiddleware, config=ProductionSecurityConfig())
else:
    app.add_middleware(HelmetMiddleware, config=DevelopmentSecurityConfig())
```

### 4. Don't Block Everything

```python
# Too strict CSP breaks functionality
# "default-src 'none'" - This will break everything!

# Better: Start permissive, gradually tighten
csp = {
    "default-src": "'self'",
    "script-src": "'self' https://cdn.trusted.com",
    "style-src": "'self' 'unsafe-inline'",
    "img-src": "'self' data: https:",
}
```

### 5. Monitor CSP Reports

```python
@app.post("/csp-report")
async def csp_report(request: Request):
    body = await request.body()
    report = json.loads(body)

    # Log to monitoring system
    logger.warning(
        "CSP Violation",
        report=report,
        url=report.get("document-uri"),
        violated_directive=report.get("violated-directive"),
    )

    # Alert on repeated violations
    # Store in database for analysis
    return Response(status_code=204)
```

---

## Summary

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| Content-Security-Policy | XSS prevention | `default-src 'self'` |
| X-Frame-Options | Clickjacking | `DENY` |
| X-Content-Type-Options | MIME sniffing | `nosniff` |
| Strict-Transport-Security | HTTPS enforcement | `max-age=31536000; includeSubDomains; preload` |
| X-XSS-Protection | XSS filter (legacy) | `1; mode=block` |
| Referrer-Policy | Referrer control | `strict-origin-when-cross-origin` |
| Permissions-Policy | Feature control | `camera=(), microphone=()` |
| Cross-Origin-Opener-Policy | Cross-origin isolation | `same-origin` |
| Cross-Origin-Resource-Policy | Resource isolation | `same-origin` |

### Quick Implementation

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
        }
        for key, value in headers.items():
            response.headers[key] = value
        return response

app.add_middleware(SecurityHeadersMiddleware)
```
