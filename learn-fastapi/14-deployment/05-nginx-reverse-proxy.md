# Nginx Reverse Proxy for FastAPI — Complete Guide

## Table of Contents
1. [Why Nginx with FastAPI](#why-nginx)
2. [Basic Configuration](#basic-config)
3. [Upstream Blocks](#upstream)
4. [Load Balancing](#load-balancing)
5. [SSL Termination](#ssl)
6. [Rate Limiting](#rate-limiting)
7. [Gzip Compression](#gzip)
8. [Static Files](#static-files)
9. [WebSocket Proxy](#websocket)
10. [Proxy Headers](#proxy-headers)
11. [Security Headers](#security-headers)
12. [Complete Production Config](#complete)
13. [Docker Compose Setup](#docker-compose)
14. [Best Practices](#best-practices)

---

## Why Nginx with FastAPI <a name="why-nginx"></a>

Uvicorn/Gunicorn serve FastAPI directly, but adding Nginx in front provides:

- **SSL termination** — handle TLS at Nginx, plain HTTP to app
- **Static file serving** — offload static assets from Python
- **Load balancing** — distribute across multiple Uvicorn workers
- **Rate limiting** — protect against abuse
- **Buffering** — absorb slow clients, protect app from slow loris
- **Security headers** — add headers without modifying app code
- **Gzip compression** — compress responses at the proxy level

```
Client → Nginx (SSL, rate limiting, static) → Uvicorn/Gunicorn (FastAPI)
```

---

## Basic Configuration <a name="basic-config"></a>

```nginx
# /etc/nginx/nginx.conf

worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '$request_time $upstream_response_time';

    access_log /var/log/nginx/access.log main;
    error_log  /var/log/nginx/error.log warn;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;

    # Buffers
    client_body_buffer_size 16k;
    client_header_buffer_size 1k;
    client_max_body_size 50m;
    large_client_header_buffers 4 8k;

    # Timeouts
    client_body_timeout 30;
    client_header_timeout 30;
    send_timeout 30;

    include /etc/nginx/conf.d/*.conf;
}
```

---

## Upstream Blocks <a name="upstream"></a>

```nginx
# /etc/nginx/conf.d/fastapi.conf

upstream fastapi_backend {
    # Least connections: sends to server with fewest active connections
    least_conn;

    # Server blocks
    server 127.0.0.1:8000 weight=3 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8001 weight=2 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 weight=1 max_fails=3 fail_timeout=30s;

    # Backup server (only used when all primary servers are down)
    server 127.0.0.1:8003 backup;

    # Keep connections to upstream alive
    keepalive 32;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Upstream Parameters

| Parameter | Description |
|-----------|-------------|
| `weight` | Load balancing weight |
| `max_fails` | Max failures before marking as down |
| `fail_timeout` | Duration to mark as down after max_fails |
| `backup` | Only used when all primary servers are down |
| `down` | Permanently mark server as down |
| `keepalive` | Number of keepalive connections to upstream |

---

## Load Balancing <a name="load-balancing"></a>

```nginx
# Round Robin (default)
upstream backend_rr {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

# Least Connections
upstream backend_lc {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

# IP Hash (sticky sessions)
upstream backend_ip {
    ip_hash;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

# Weighted
upstream backend_weighted {
    server 127.0.0.1:8000 weight=5;   # Gets 5/8 of traffic
    server 127.0.0.1:8001 weight=2;   # Gets 2/8 of traffic
    server 127.0.0.1:8002 weight=1;   # Gets 1/8 of traffic
}

# Generic hash (custom key)
upstream backend_hash {
    hash $request_uri consistent;  # Consistent hashing
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}
```

### Load Balancing Algorithms

| Algorithm | Directive | Best For |
|-----------|-----------|----------|
| Round Robin | (default) | General purpose, equal servers |
| Least Connections | `least_conn` | Varied request durations |
| IP Hash | `ip_hash` | Session affinity |
| Generic Hash | `hash $key` | Cache-friendly routing |
| Random | `random two least_conn` | Large clusters |

---

## SSL Termination <a name="ssl"></a>

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name api.example.com;

    # ACME challenge for Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.example.com;

    # SSL certificates
    ssl_certificate     /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Certbot Auto-Renewal

```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Get certificate
certbot certonly --webroot -w /var/www/certbot \
    -d api.example.com

# Auto-renewal cron job
0 0 1 * * certbot renew --post-hook "nginx -s reload"
```

---

## Rate Limiting <a name="rate-limiting"></a>

```nginx
# Define rate limit zones
http {
    # General API rate limiting: 10 requests/second per IP
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    # Login endpoint: 5 requests/minute per IP
    limit_req_zone $binary_remote_addr zone=login_limit:10m rate=5r/m;

    # Upload endpoint: 2 requests/second per IP
    limit_req_zone $binary_remote_addr zone=upload_limit:10m rate=2r/s;

    # Connection limiting: max 20 concurrent connections per IP
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

server {
    # Apply rate limiting to API endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_req_status 429;

        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Stricter rate limiting for login
    location /api/v1/auth/login {
        limit_req zone=login_limit burst=3 nodelay;
        limit_req_status 429;

        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Upload rate limiting
    location /api/v1/upload {
        limit_req zone=upload_limit burst=5 nodelay;
        limit_req_status 429;
        limit_conn conn_limit 5;

        client_max_body_size 100m;
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Custom rate limit response
    error_page 429 = @rate_limited;
    location @rate_limited {
        default_type application/json;
        return 429 '{"error": "rate_limit_exceeded", "message": "Too many requests"}';
    }
}
```

### Rate Limiting Parameters

| Parameter | Description |
|-----------|-------------|
| `rate` | Request rate (10r/s = 10/sec, 5r/m = 5/min) |
| `burst` | Max burst of requests before rejecting |
| `nodelay` | Process burst requests immediately (don't queue) |
| `burst=20` | Allow 20 requests burst |
| `limit_req_status` | HTTP status for rate-limited requests (default 503) |

---

## Gzip Compression <a name="gzip"></a>

```nginx
http {
    # Enable gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;

    # Compress these MIME types
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml
        application/rss+xml
        application/atom+xml
        image/svg+xml;

    # Don't compress these
    gzip_min_length 256;
    gzip_disable "msie6";

    # Brotli (if compiled)
    # brotli on;
    # brotli_comp_level 6;
    # brotli_types text/plain text/css application/json application/javascript;
}
```

### Compression Comparison

| Algorithm | Level | Ratio | CPU Usage |
|-----------|-------|-------|-----------|
| gzip 1 | Fast | 2.5x | Low |
| gzip 6 | Balanced | 3.5x | Medium |
| gzip 9 | Max | 3.7x | High |
| brotli 4 | Fast | 3.8x | Low |
| brotli 6 | Balanced | 4.2x | Medium |
| brotli 11 | Max | 4.5x | High |

---

## Static Files <a name="static-files"></a>

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # Serve static files directly (bypass FastAPI)
    location /static/ {
        alias /var/www/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;

        # Gzip static files
        gzip_static on;
    }

    # Serve favicon
    location = /favicon.ico {
        alias /var/www/static/favicon.ico;
        expires 365d;
        access_log off;
        log_not_found off;
    }

    # API — proxy to FastAPI
    location /api/ {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Docs UI — proxy to FastAPI
    location /docs {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location /openapi.json {
        proxy_pass http://fastapi_backend;
    }
}
```

---

## WebSocket Proxy <a name="websocket"></a>

```nginx
upstream websocket_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    # WebSocket endpoint
    location /ws {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket-specific timeouts
        proxy_read_timeout 86400s;   # 24 hours
        proxy_send_timeout 86400s;

        # Buffering off for real-time
        proxy_buffering off;
    }
}
```

### FastAPI WebSocket Endpoint

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
```

---

## Proxy Headers <a name="proxy-headers"></a>

```nginx
# Essential proxy headers for FastAPI
location / {
    proxy_pass http://fastapi_backend;

    # Standard proxy headers
    proxy_set_header Host              $host;
    proxy_set_header X-Real-IP         $remote_addr;
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Host  $host;
    proxy_set_header X-Forwarded-Port  $server_port;

    # WebSocket support
    proxy_set_header Upgrade    $http_upgrade;
    proxy_set_header Connection $connection_upgrade;

    # Timeout settings
    proxy_connect_timeout 60s;
    proxy_send_timeout    60s;
    proxy_read_timeout    60s;

    # Buffering
    proxy_buffering on;
    proxy_buffer_size 16k;
    proxy_buffers 4 32k;
    proxy_busy_buffers_size 64k;

    # Handle client body
    proxy_request_buffering on;
    proxy_set_header Content-Length $content_length;
    proxy_set_header Content-Type   $content_type;
}

# WebSocket connection upgrade map
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
```

### FastAPI Reading Headers

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/info")
async def get_client_info(request: Request):
    return {
        "client_ip": request.headers.get("X-Real-IP"),
        "forwarded_for": request.headers.get("X-Forwarded-For"),
        "forwarded_proto": request.headers.get("X-Forwarded-Proto"),
        "host": request.headers.get("Host"),
    }
```

---

## Security Headers <a name="security-headers"></a>

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'" always;

    # HSTS (only if using HTTPS)
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # Remove server version
    server_tokens off;

    # Prevent access to hidden files
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }

    # Prevent access to sensitive paths
    location ~ ^/(\.env|\.git|docker-compose) {
        deny all;
    }

    # Rate limiting and proxy
    location / {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### CORS Configuration

```nginx
# CORS headers for FastAPI
location /api/ {
    # Handle preflight requests
    if ($request_method = 'OPTIONS') {
        add_header 'Access-Control-Allow-Origin' 'https://myapp.com' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, X-Requested-With' always;
        add_header 'Access-Control-Max-Age' 1728000;
        add_header 'Content-Type' 'text/plain charset=UTF-8';
        add_header 'Content-Length' 0;
        return 204;
    }

    add_header 'Access-Control-Allow-Origin' 'https://myapp.com' always;
    add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
    add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type, X-Requested-With' always;
    add_header 'Access-Control-Expose-Headers' 'Content-Length, Content-Range' always;

    proxy_pass http://fastapi_backend;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## Complete Production Config <a name="complete"></a>

```nginx
# /etc/nginx/nginx.conf
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    multi_accept on;
    use epoll;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    '$request_time $upstream_response_time';

    access_log /var/log/nginx/access.log main buffer=16k flush=5s;
    error_log  /var/log/nginx/error.log warn;

    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 1000;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;

    # Rate limit zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    # Upstream
    upstream fastapi_backend {
        least_conn;
        server 127.0.0.1:8000 max_fails=3 fail_timeout=30s;
        server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
        server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
        keepalive 32;
    }

    # WebSocket upgrade map
    map $http_upgrade $connection_upgrade {
        default upgrade;
        ''      close;
    }

    # HTTP redirect
    server {
        listen 80;
        server_name api.example.com;
        return 301 https://$host$request_uri;
    }

    # HTTPS
    server {
        listen 443 ssl http2;
        server_name api.example.com;

        ssl_certificate     /etc/letsencrypt/live/api.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:10m;

        server_tokens off;

        # Security headers
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;

        # Static files
        location /static/ {
            alias /var/www/static/;
            expires 30d;
            gzip_static on;
            access_log off;
        }

        # WebSocket
        location /ws {
            proxy_pass http://fastapi_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_read_timeout 86400s;
            proxy_buffering off;
        }

        # API
        location / {
            limit_req zone=api_limit burst=20 nodelay;
            limit_conn conn_limit 20;

            proxy_pass http://fastapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 60s;
            proxy_read_timeout 60s;
        }
    }
}
```

---

## Docker Compose Setup <a name="docker-compose"></a>

```yaml
version: "3.9"

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/certs:/etc/nginx/certs:ro
      - ./static:/var/www/static:ro
    depends_on:
      - app1
      - app2
    networks:
      - frontend
    restart: unless-stopped

  app1:
    build: .
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/myapp
    networks:
      - frontend
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

  app2:
    build: .
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/myapp
    networks:
      - frontend
      - backend
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

networks:
  frontend:
  backend:
    internal: true

volumes:
  postgres_data:
```

---

## Best Practices <a name="best-practices"></a>

1. **Always use Nginx in production** — SSL, buffering, static files
2. **Enable keepalive to upstream** — reduce connection overhead
3. **Use least_conn** — better than round-robin for varied request times
4. **Set proper proxy headers** — X-Real-IP, X-Forwarded-For, X-Forwarded-Proto
5. **Enable rate limiting** — protect against abuse, use different limits for different endpoints
6. **Use gzip** — reduce response sizes by 60-80%
7. **Serve static files via Nginx** — offload from Python process
8. **Set security headers** — HSTS, CSP, X-Frame-Options
9. **Use SSL/TLS 1.2+** — disable older protocols
10. **Monitor upstream health** — log upstream_response_time
11. **Use separate error pages** — custom 429, 502, 503 pages
12. **Buffer client body** — protect against slow loris attacks
13. **Set client_max_body_size** — prevent oversized uploads
14. **Use WebSocket upgrade headers** — for real-time features
15. **Test configuration** — always run `nginx -t` before reload
