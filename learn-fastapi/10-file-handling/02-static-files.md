# Static Files in FastAPI

## Table of Contents
1. [StaticFiles Mount](#staticfiles-mount)
2. [Serving Static Assets](#serving-static-assets)
3. [SPA Support](#spa-support)
4. [Media Files](#media-files)
5. [Cache Headers](#cache-headers)
6. [CDN Integration](#cdn-integration)
7. [Best Practices](#best-practices)
8. [Interview Questions](#interview-questions)

---

## StaticFiles Mount

### Basic Setup

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Multiple Static Directories

```python
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="build/assets"), name="assets")
app.mount("/media", StaticFiles(directory="media"), name="media")
```

### With HTML Mode

```python
# Enable HTML mode for serving index.html for directories
app.mount("/", StaticFiles(directory="public", html=True), name="public")
```

---

## Serving Static Assets

### Project Structure

```
project/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   ├── images/
│   │   └── logo.png
│   └── index.html
├── app/
│   └── main.py
└── requirements.txt
```

### Serving CSS/JS/Images

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <img src="/static/images/logo.png" alt="Logo">
        <script src="/static/js/app.js"></script>
    </body>
    </html>
    """
```

### Serving Build Assets

```python
# For React/Vue/Angular builds
app.mount(
    "/assets",
    StaticFiles(directory="build/assets"),
    name="build-assets",
)
```

---

## SPA Support

### Single Page Application Routing

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Serve static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# SPA fallback - serve index.html for all non-API routes
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Check if the file exists in static directory
    file_path = f"static/{full_path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    # Otherwise serve index.html (SPA routing)
    return FileResponse("static/index.html")
```

### Vue Router / React Router Support

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# API routes first
@app.get("/api/users")
async def get_users():
    return {"users": []}

# Static assets
app.mount("/assets", StaticFiles(directory="build/assets"), name="assets")

# SPA catch-all (must be last)
@app.get("/{path:path}")
async def serve_spa(path: str):
    # Try to serve the exact file
    file_path = f"build/{path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)

    # Serve index.html for SPA routing
    return FileResponse("build/index.html")
```

### Hashicorp-style SPA Serving

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException:
            index_path = os.path.join(self.directory, "index.html")
            if os.path.exists(index_path):
                return FileResponse(index_path)
            raise

app.mount("/", SPAStaticFiles(directory="build", html=True), name="spa")
```

---

## Media Files

### User Uploads

```python
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import uuid

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

app = FastAPI()

@app.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(MEDIA_DIR, unique_name)

    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "filename": unique_name,
        "url": f"/media/{unique_name}",
    }

# Serve media files
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
```

### Profile Pictures

```python
@app.post("/profile/picture")
async def upload_profile_picture(
    user_id: int,
    file: UploadFile = File(...),
):
    # Validate image type
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Must be an image")

    # Save with user ID
    ext = os.path.splitext(file.filename)[1]
    filename = f"profile_{user_id}{ext}"
    file_path = os.path.join(MEDIA_DIR, "avatars", filename)

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"url": f"/media/avatars/{filename}"}
```

---

## Cache Headers

### Custom Cache Control

```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response

app = FastAPI()

class CacheControlStaticFiles(StaticFiles):
    def __init__(self, *args, cache_control: dict = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_control = cache_control or {}

    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)

        # Add cache headers based on file type
        if path.endswith(('.js', '.css')):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif path.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            response.headers["Cache-Control"] = "public, max-age=86400"
        elif path.endswith('.html'):
            response.headers["Cache-Control"] = "no-cache, must-revalidate"

        return response

app.mount("/static", CacheControlStaticFiles(directory="static"), name="static")
```

### Content Hash for Cache Busting

```python
import hashlib

def get_file_hash(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

@app.get("/assets/{path:path}")
async def serve_asset(path: str):
    file_path = f"static/assets/{path}"
    if not os.path.exists(file_path):
        raise HTTPException(404)

    response = FileResponse(file_path)

    # Set long cache for files with hash in name
    if "." in path and len(path.split(".")[0]) > 10:
        response.headers["Cache-Control"] = "public, max-age=31536000, immutable"

    return response
```

### ETag Support

```python
import hashlib
from fastapi import Request
from fastapi.responses import Response

@app.get("/static/{path:path}")
async def serve_with_etag(path: str, request: Request):
    file_path = f"static/{path}"
    if not os.path.exists(file_path):
        raise HTTPException(404)

    # Generate ETag
    with open(file_path, "rb") as f:
        content = f.read()
        etag = hashlib.md5(content).hexdigest()

    # Check If-None-Match
    if_none_match = request.headers.get("if-none-match")
    if if_none_match == etag:
        return Response(status_code=304)

    response = Response(content=content)
    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=3600"
    return response
```

---

## CDN Integration

### Cloudflare Configuration

```python
# In Cloudflare dashboard:
# 1. Enable Caching
# 2. Set Browser Cache TTL to "Respect Existing Headers"
# 3. Enable "Always Use HTTPS"
# 4. Enable "Auto Minify" for CSS/JS

# Application still sets cache headers
# Cloudflare respects and applies them
```

### AWS CloudFront

```python
# CloudFront distribution config
# Origin: your FastAPI server
# Cache behaviors:
#   /static/* -> Long TTL (1 year)
#   /media/*  -> Medium TTL (1 day)
#   /api/*    -> No caching

# Application headers that CloudFront respects:
response.headers["Cache-Control"] = "public, max-age=31536000"
```

### Serving from CDN

```python
import os

CDN_URL = os.getenv("CDN_URL", "")

@app.get("/")
async def root():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="{CDN_URL}/static/css/style.css">
    </head>
    <body>
        <img src="{CDN_URL}/static/images/logo.png" alt="Logo">
        <script src="{CDN_URL}/static/js/app.js"></script>
    </body>
    </html>
    """)
```

---

## Best Practices

### 1. Serve Static Files Separately

```python
# Use Nginx or CDN for static files in production
# FastAPI should focus on API endpoints

# Nginx config:
# location /static/ {
#     alias /path/to/static/;
#     expires 30d;
# }
```

### 2. Use Cache Busting

```python
# Include file hash in filename
# style.a1b2c3d4.css instead of style.css
# Allows long cache times without stale content
```

### 3. Compress Static Files

```python
# Use Brotli/GZip compression
# Pre-compress during build process
# Enable gzip_static in Nginx
```

### 4. Set Appropriate Cache Headers

```python
# Static assets (JS/CSS): 1 year (with cache busting)
# Images: 1 day to 1 week
# HTML: no-cache (always check for updates)
```

### 5. Use CDN for Global Distribution

```python
# Deploy static files to CDN
# Reduce latency for global users
# Offload bandwidth from origin server
```

### 6. Separate Static from API

```python
# Don't serve static files from FastAPI in production
# Use Nginx, Apache, or CDN
# FastAPI should only handle API requests
```

---

## Interview Questions

### Q1: How do you serve static files in FastAPI?
**Answer:** Use `app.mount("/static", StaticFiles(directory="static"))`. This serves all files in the static directory under the /static URL path.

### Q2: What is the difference between StaticFiles and FileResponse?
**Answer:** StaticFiles serves entire directories. FileResponse serves individual files. Use StaticFiles for directories, FileResponse for specific files.

### Q3: How do you support SPA routing in FastAPI?
**Answer:** Mount StaticFiles with `html=True` or implement a catch-all route that serves index.html for non-API paths, allowing client-side routing.

### Q4: How do you set cache headers for static files?
**Answer:** Create a custom StaticFiles subclass that adds Cache-Control headers based on file type. Use long cache times for assets with content hashing.

### Q5: What is cache busting?
**Answer:** Including a unique identifier (hash) in filenames (e.g., style.a1b2c3.css). Allows setting long cache times because the filename changes when content changes.

### Q6: How do you serve media files uploaded by users?
**Answer:** Save uploads to a media directory and mount it with StaticFiles. Use unique filenames to prevent conflicts. Consider cloud storage for production.

### Q7: How do you handle ETags for static files?
**Answer:** Generate ETag from file content hash. Check If-None-Match header. Return 304 Not Modified if ETag matches, avoiding unnecessary file transfers.

### Q8: How do you integrate with CDN?
**Answer:** Set cache headers in FastAPI. Deploy static files to CDN. Configure CDN to respect origin headers. Use CDN URLs in HTML templates.

### Q9: How do you compress static files?
**Answer:** Pre-compress during build (gzip, brotli). Use Nginx's gzip_static or brotli_static. Enable compression in CDN settings.

### Q10: Should you serve static files from FastAPI in production?
**Answer:** Generally no. Use Nginx, Apache, or CDN for static files. FastAPI should focus on API endpoints. Static file serving adds unnecessary overhead.

### Q11: How do you handle multiple static directories?
**Answer:** Mount each directory separately with different URL prefixes: `app.mount("/css", StaticFiles(directory="css"))`.

### Q12: How do you serve a React/Vue build?
**Answer:** Mount the build directory with `html=True` for SPA routing. Mount assets directory separately. Implement catch-all route for client-side routing.

### Q13: How do you prevent directory listing?
**Answer:** StaticFiles doesn't list directories by default. Only existing files are served. Requests for directories return 404.

### Q14: How do you serve files with specific content types?
**Answer:** FastAPI auto-detects content types. For custom types, subclass StaticFiles and override get_response to set Content-Type header.

### Q15: How do you handle CORS for static files?
**Answer:** If static files are on a different domain, add CORS headers. Use CORSMiddleware. CDN configurations may need CORS setup.

### Q16: How do you optimize static file delivery?
**Answer:** Use CDN, enable compression, set cache headers, use HTTP/2, minimize file sizes, and serve from edge locations close to users.

### Q17: How do you handle large media files?
**Answer:** Use streaming responses. Implement range requests for video. Consider cloud storage (S3) for scalability. Use CDN for distribution.

### Q18: How do you secure static file serving?
**Answer:** Validate file paths to prevent traversal. Restrict file types. Use authentication for private files. Scan uploads for malware.

### Q19: How do you monitor static file serving?
**Answer:** Track request counts, bandwidth, cache hit rates, and response times. Use CDN analytics. Monitor origin server load.

### Q20: How do you handle static files during deployment?
**Answer:** Build and optimize during CI/CD. Deploy to CDN or static hosting. Use cache busting to ensure users get latest versions.
