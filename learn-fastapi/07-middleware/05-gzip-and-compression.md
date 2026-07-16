# GZip and Compression Middleware in FastAPI

## Table of Contents
1. [Why Compression Matters](#why-compression-matters)
2. [GZipMiddleware](#gzipmiddleware)
3. [BrotliMiddleware](#brotlimiddleware)
4. [Compression Levels](#compression-levels)
5. [When to Compress](#when-to-compress)
6. [Static File Compression](#static-file-compression)
7. [Response Streaming with Compression](#response-streaming-with-compression)
8. [Best Practices](#best-practices)
9. [Interview Questions](#interview-questions)

---

## Why Compression Matters

Compression reduces the size of HTTP responses, improving:
- **Bandwidth usage**: Less data transferred
- **Load times**: Faster page loads for users
- **Server costs**: Lower bandwidth bills
- **User experience**: Especially on mobile networks

### Compression Ratio Examples

```
Text/HTML:   60-80% reduction
JSON:        60-75% reduction
CSS:         60-80% reduction
JavaScript:  60-75% reduction
SVG:         50-70% reduction
Images:      Already compressed (minimal benefit)
Binary:      20-50% reduction
```

### How Compression Works

1. Client sends `Accept-Encoding: gzip, br` header
2. Server compresses response body
3. Server adds `Content-Encoding: gzip` header
4. Client decompresses the response

---

## GZipMiddleware

### Basic Setup

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=500)
```

### Configuration Options

```python
app.add_middleware(
    GZipMiddleware,
    minimum_size=500,      # Minimum response size (bytes) to compress
    compresslevel=6,        # Compression level (1-9, default 6)
)
```

### How GZipMiddleware Works

```python
# 1. Checks if client accepts gzip encoding
# 2. Checks if response size >= minimum_size
# 3. Compresses the response body
# 4. Sets Content-Encoding: gzip header
# 5. Updates Content-Length header

# The middleware handles:
# - Checking Accept-Encoding header
# - Compressing the response body
# - Setting appropriate headers
# - Streaming responses
```

### Complete Example

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import json

app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=500)

@app.get("/api/large-data")
async def get_large_data():
    # This response will be automatically compressed
    data = {
        "items": [
            {"id": i, "name": f"Item {i}", "description": "x" * 100}
            for i in range(1000)
        ]
    }
    return JSONResponse(content=data)
```

---

## BrotliMiddleware

### What is Brotli?

Brotli is a compression algorithm developed by Google. It typically achieves better compression ratios than GZip, especially for text content.

### Setup

```python
from fastapi.middleware.brotli import BrotliMiddleware

app.add_middleware(
    BrotliMiddleware,
    minimum_size=500,
    compresslevel=4,  # Brotli uses 0-11
)
```

### GZip vs Brotli

| Feature | GZip | Brotli |
|---------|------|--------|
| Compression speed | Fast | Slower |
| Decompression speed | Fast | Fast |
| Compression ratio | Good | Better |
| Browser support | Universal | Modern browsers |
| CPU usage | Lower | Higher |
| Best for | General use | Static content |

### Configuration

```python
app.add_middleware(
    BrotliMiddleware,
    minimum_size=500,
    compresslevel=6,  # 0-11, default 6
)
```

### Using Both

```python
# Brotli for modern browsers, GZip for older ones
from fastapi.middleware.brotli import BrotliMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Brotli first (checked first by browsers that support it)
app.add_middleware(BrotliMiddleware, minimum_size=500)
# GZip as fallback
app.add_middleware(GZipMiddleware, minimum_size=500)
```

---

## Compression Levels

### GZip Compression Levels

```python
# Level 1: Fastest, least compression
app.add_middleware(GZipMiddleware, compresslevel=1)

# Level 6: Default, balanced (recommended)
app.add_middleware(GZipMiddleware, compresslevel=6)

# Level 9: Slowest, best compression
app.add_middleware(GZipMiddleware, compresslevel=9)
```

### Compression Level Comparison

```
Level 1: ~75% of original size, very fast
Level 3: ~70% of original size, fast
Level 6: ~65% of original size, balanced (default)
Level 9: ~60% of original size, slow
```

### When to Use Different Levels

```python
# Development: Fast compression
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=1)

# Production: Balanced
app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=6)

# Static assets (pre-compressed): Maximum
app.add_middleware(GZipMiddleware, minimum_size=100, compresslevel=9)
```

### Brotli Compression Levels

```python
# Brotli levels 0-11
# Level 0: No compression
# Level 1-4: Fast compression
# Level 5-7: Balanced (default 6)
# Level 8-11: Best compression (slow)

app.add_middleware(BrotliMiddleware, compresslevel=4)  # Fast
app.add_middleware(BrotliMiddleware, compresslevel=6)  # Balanced
app.add_middleware(BrotliMiddleware, compresslevel=11) # Best
```

---

## When to Compress

### Should You Compress This Content?

```python
# YES: Text-based content
# - HTML, JSON, XML, SVG
# - CSS, JavaScript
# - Plain text

# NO: Already compressed content
# - JPEG, PNG, GIF images
# - MP4, WebM video
# - WOFF2 fonts (already compressed)
# - ZIP, GZ files

# MAYBE: Binary content
# - PDF files (slight compression possible)
# - Large binary data
```

### Content-Type Based Compression

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Types that should NOT be compressed
SKIP_COMPRESSION_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "video/mp4",
    "font/woff2",
    "application/zip",
    "application/gzip",
}

class SmartCompressionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        content_type = response.headers.get("content-type", "")

        # Skip compression for already-compressed content
        if any(t in content_type for t in SKIP_COMPRESSION_TYPES):
            # Remove any compression headers
            response.headers.pop("content-encoding", None)
            response.headers.pop("content-length", None)

        return response
```

### Minimum Size Threshold

```python
# Don't compress small responses (overhead isn't worth it)
app.add_middleware(GZipMiddleware, minimum_size=500)  # 500 bytes minimum

# For high-traffic APIs, increase threshold
app.add_middleware(GZipMiddleware, minimum_size=1024)  # 1KB minimum
```

---

## Static File Compression

### Pre-Compressed Static Files

```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve pre-compressed files
# Nginx/CDN should serve .gz or .br files when Accept-Encoding matches
app.mount("/static", StaticFiles(directory="static"), name="static")
```

### Building Pre-Compressed Files

```bash
# Build script for pre-compressed static files
find ./static -type f \( -name "*.js" -o -name "*.css" -o -name "*.html" \) -exec gzip -k -9 {} \;
find ./static -type f \( -name "*.js" -o -name "*.css" -o -name "*.html" \) -exec brotli -k -Z {} \;
```

### Nginx Configuration for Pre-Compressed Files

```nginx
# Nginx serves pre-compressed files when available
location /static/ {
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    gzip_min_length 500;

    # Serve pre-compressed files
    gzip_static on;
    brotli_static on;
}
```

### CDN Integration

```python
# With Cloudflare or AWS CloudFront
# Compression is handled at the CDN edge
# Server should still compress for direct requests

# Cloudflare automatically compresses most content types
# Just enable "Auto Minify" and "Brotli" in Cloudflare dashboard
```

---

## Response Streaming with Compression

### Streaming Large Responses

```python
from fastapi.responses import StreamingResponse
import gzip

async def generate_data():
    for i in range(1000000):
        yield f"Line {i}\n"

@app.get("/stream")
async def stream_data():
    return StreamingResponse(
        generate_data(),
        media_type="text/plain",
        headers={"Content-Encoding": "gzip"}
    )

# GZipMiddleware will compress streaming responses
```

### Chunked Transfer Encoding

```python
async def large_csv_generator():
    yield "id,name,value\n"
    for i in range(100000):
        yield f"{i},item_{i},{i * 1.5}\n"

@app.get("/export")
async def export_csv():
    return StreamingResponse(
        large_csv_generator(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )
    # GZipMiddleware compresses each chunk
```

### Memory-Efficient Streaming

```python
import io

async def generate_pdf():
    # Generate PDF in chunks
    buffer = io.BytesIO()
    # ... generate PDF content
    buffer.seek(0)

    async def file_generator():
        while chunk := buffer.read(8192):
            yield chunk

    return StreamingResponse(
        file_generator(),
        media_type="application/pdf",
    )
    # Compression middleware handles the streaming
```

---

## Best Practices

### 1. Always Compress Text Content

```python
# Text content benefits most from compression
app.add_middleware(GZipMiddleware, minimum_size=500)
```

### 2. Don't Compress Already Compressed Content

```python
# Skip compression for images, videos, fonts
# Use minimum_size to avoid compressing small responses
```

### 3. Use Brotli for Static Assets

```python
# Brotli achieves better compression for static content
# GZip is fine for dynamic content
```

### 4. Set Appropriate Minimum Size

```python
# Too low: Wastes CPU on tiny responses
# Too high: Misses compression benefits
# 500-1000 bytes is a good range
```

### 5. Monitor Compression Ratios

```python
# Track how much bandwidth you're saving
# Adjust settings based on actual data patterns
```

### 6. Consider CDN Compression

```python
# CDNs often handle compression at the edge
# Server-side compression still helps for direct requests
```

### 7. Test with Different Accept-Encoding Headers

```python
# Test that responses work with:
# - Accept-Encoding: gzip
# - Accept-Encoding: br
# - Accept-Encoding: gzip, br
# - No Accept-Encoding header
```

---

## Interview Questions

### Q1: Why use compression in APIs?
**Answer:** Compression reduces response size, improving load times, reducing bandwidth costs, and enhancing user experience, especially on slow networks.

### Q2: What's the difference between GZip and Brotli?
**Answer:** Brotli typically achieves better compression ratios but is slower to compress. GZip is faster and universally supported. Brotli is better for static content, GZip for dynamic.

### Q3: When should you NOT compress?
**Answer:** Don't compress already-compressed content (images, videos, fonts), very small responses (<500 bytes), or when CPU is the bottleneck rather than bandwidth.

### Q4: What is minimum_size in GZipMiddleware?
**Answer:** The minimum response size (in bytes) below which the middleware won't compress. This avoids wasting CPU on tiny responses where compression provides minimal benefit.

### Q5: How does the client indicate it accepts compressed responses?
**Answer:** Via the `Accept-Encoding` header (e.g., `Accept-Encoding: gzip, br`). The server checks this before compressing.

### Q6: What happens if the client doesn't support compression?
**Answer:** The server sends uncompressed responses. The middleware checks the `Accept-Encoding` header and only compresses if the client supports it.

### Q7: How does compression affect streaming responses?
**Answer:** GZipMiddleware can compress streaming responses by compressing each chunk. This maintains memory efficiency while still providing compression benefits.

### Q8: What compression level should you use in production?
**Answer:** Level 6 (default) is a good balance. Higher levels use more CPU for slightly better compression. For static assets, level 9 is fine. For dynamic content, levels 4-6 are recommended.

### Q9: Can you compress WebSocket messages?
**Answer:** Standard HTTP compression middleware doesn't apply to WebSocket. WebSocket has its own per-message compression extension (permessage-deflate) which must be configured separately.

### Q10: How do you test compression is working?
**Answer:** Check the `Content-Encoding` response header. Use `curl -H "Accept-Encoding: gzip" --compressed` to test. Compare response sizes with and without compression.

### Q11: What are the CPU trade-offs of compression?
**Answer:** Compression uses CPU on the server, decompression uses CPU on the client. For text content, the bandwidth savings usually outweigh the CPU cost. For already-compressed content, it wastes CPU.

### Q12: How do CDNs handle compression?
**Answer:** Most CDNs (Cloudflare, CloudFront) can compress at the edge. They may also serve pre-compressed files. Server-side compression still helps for direct requests and for the CDN to cache compressed versions.

### Q13: What is pre-compression?
**Answer:** Compressing static assets during the build process and serving the pre-compressed files. This avoids runtime compression overhead. Nginx's `gzip_static` directive serves pre-compressed `.gz` files.

### Q14: How do you handle compression with FastAPI's StreamingResponse?
**Answer:** FastAPI's GZipMiddleware automatically handles StreamingResponse by compressing chunks as they're generated. No special configuration is needed.

### Q15: What is the Content-Encoding header?
**Answer:** A response header indicating the encoding applied to the response body (e.g., `Content-Encoding: gzip`). The client uses this to know how to decompress.

### Q16: Can compression cause security issues?
**Answer:** BREACH and CRIME attacks exploit compression with secret tokens. These mainly affect TLS-compressed pages with reflected user input. Mitigate with CSRF tokens and masking.

### Q17: How does compression interact with caching?
**Answer:** Compressed responses should be cached with their Content-Encoding. The Vary header should include Accept-Encoding so caches serve the right version for each client.

### Q18: What is the difference between compression and minification?
**Answer:** Compression (GZip/Brotli) reduces file size at transfer time. Minification removes whitespace and comments at build time. Both should be used together for optimal performance.

### Q19: How do you compress JSON responses specifically?
**Answer:** GZipMiddleware automatically compresses JSON responses. Ensure the response size exceeds `minimum_size` and the client accepts gzip encoding.

### Q20: What's the typical compression ratio for JSON?
**Answer:** JSON typically compresses 60-75% with GZip and 70-80% with Brotli. Repetitive JSON compresses better than random data.

### Q21: How do you handle compression errors?
**Answer:** GZipMiddleware handles errors gracefully. If compression fails, it sends the uncompressed response. Monitor for compression errors in logs.

### Q22: Can you compress specific endpoints only?
**Answer:** Standard GZipMiddleware compresses all responses above the minimum size. For selective compression, write custom middleware that checks the request path.

### Q23: What is the relationship between compression and Content-Length?
**Answer:** After compression, the Content-Length header reflects the compressed size. If you remove Content-Length and use chunked encoding, the transfer uses Transfer-Encoding: chunked.

### Q24: How do you handle compression in a load-balanced setup?
**Answer:** Compression can happen at any layer: application server, reverse proxy (Nginx), or CDN. Ensure only one layer compresses to avoid double-compression.

### Q25: What are compression best practices for mobile apps?
**Answer:** Use Brotli where supported (most modern mobile browsers). Set appropriate minimum sizes. Consider that compression uses more CPU, which affects battery life on mobile devices.
