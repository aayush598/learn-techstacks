# Section 03: Production Dockerfile

## Overview

The production Dockerfile uses multi-stage builds to create minimal, secure images. By separating dependency installation, build, and runtime stages, we produce images that contain only what's necessary to run the application — no build tools, no source code, no development dependencies.

## Production Dockerfile (Next.js Multi-Stage)

```dockerfile
# docker/Dockerfile.prod
# ================================================================
# Stage 1: Base — shared tooling
# ================================================================
FROM node:20-slim AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9 --activate

# Install OpenSSL (required by Prisma)
RUN apt-get update && apt-get install -y openssl curl && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ================================================================
# Stage 2: Dependencies — install all deps (including dev)
# ================================================================
FROM base AS deps

COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./

# Copy package.json files for all workspaces
COPY apps/web/package.json ./apps/web/
COPY apps/api/package.json ./apps/api/
COPY packages/ui/package.json ./packages/ui/
COPY packages/db/package.json ./packages/db/
COPY packages/voice/package.json ./packages/voice/
COPY packages/ai/package.json ./packages/ai/
COPY packages/types/package.json ./packages/types/
COPY packages/config/package.json ./packages/config/

# Install ALL dependencies (including devDependencies needed for build)
RUN pnpm install --frozen-lockfile

# ================================================================
# Stage 3: Builder — compile TypeScript, run Next.js build
# ================================================================
FROM deps AS builder

# Copy all source code
COPY . .

# Generate Prisma client
RUN pnpm --filter @voice-agent/db run db:generate

# Build all packages and apps
RUN pnpm build

# ================================================================
# Stage 4: Production dependencies — only production deps
# ================================================================
FROM base AS prod-deps

COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY apps/web/package.json ./apps/web/
COPY apps/api/package.json ./apps/api/
COPY packages/*/package.json ./packages/

# Install ONLY production dependencies
RUN pnpm install --frozen-lockfile --prod

# ================================================================
# Stage 5: Runtime — minimal image for running the app
# ================================================================
FROM base AS runner

# Use non-root user for security
RUN groupadd --system --gid 1001 nodejs && \
  useradd --system --uid 1001 --gid nodejs voiceagent

# Set Node.js to production mode
ENV NODE_ENV=production

# Copy production dependencies
COPY --from=prod-deps --chown=voiceagent:nodejs /app/node_modules ./node_modules
COPY --from=prod-deps --chown=voiceagent:nodejs /app/packages ./packages

# Copy built artifacts
COPY --from=builder --chown=voiceagent:nodejs /app/apps/web/.next ./apps/web/.next
COPY --from=builder --chown=voiceagent:nodejs /app/apps/web/public ./apps/web/public
COPY --from=builder --chown=voiceagent:nodejs /app/apps/web/package.json ./apps/web/
COPY --from=builder --chown=voiceagent:nodejs /app/apps/web/next.config.js ./apps/web/

# Copy Prisma client (needed at runtime)
COPY --from=builder --chown=voiceagent:nodejs /app/packages/db/node_modules/.prisma ./packages/db/node_modules/.prisma
COPY --from=builder --chown=voiceagent:nodejs /app/packages/db/dist ./packages/db/dist

# Switch to non-root user
USER voiceagent

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["node", "apps/web/server.js"]
```

## Production Docker Compose

```yaml
# docker/docker-compose.prod.yml
version: "3.9"

name: voice-agent-prod

services:
  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile.prod
      target: runner
    image: voice-agent/web:${TAG:-latest}
    ports:
      - "3000:3000"
    env_file:
      - ../.env.production
    environment:
      - NODE_ENV=production
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "1"
          memory: "1G"
        reservations:
          cpus: "0.5"
          memory: "512M"
      restart_policy:
        condition: any
        max_attempts: 3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - voice-agent-prod

  reverseproxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ../docker/nginx/ssl:/etc/nginx/ssl
    depends_on:
      - web
    networks:
      - voice-agent-prod

networks:
  voice-agent-prod:
    driver: overlay
```

## Image Size Optimization

```text
Stage-by-stage image size comparison:

base (node:20-slim)          ~150 MB
deps (with all deps)         ~800 MB
builder (with source)        ~950 MB
prod-deps (production only)  ~400 MB
runner (final image)         ~350 MB

Savings: ~600 MB (60% reduction from builder stage)
```

### Optimization Techniques

```dockerfile
# Compress .next output
RUN pnpm build && \
  # Remove source maps from production
  find .next -name "*.map" -delete && \
  # Remove .turbo cache
  rm -rf .turbo

# Use Alpine for smaller base image
FROM node:20-alpine AS base
RUN apk add --no-cache openssl curl
# Alpine image: ~50 MB vs. ~150 MB for slim
```

## Security Hardening

```dockerfile
# Security best practices
FROM base AS runner

# Run as non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Remove unnecessary capabilities
RUN apk add --no-cache libcap && \
  setcap -r /usr/local/bin/node

# Read-only root filesystem (when using Docker run)
# --read-only --tmpfs /tmp --tmpfs /var/run

# No shell in production
RUN rm -f /bin/sh /bin/bash
```

## CI/CD Build

```yaml
# .github/workflows/docker-build.yml
name: Docker Build
on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}/web
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,format=short
            type=ref,event=branch

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/Dockerfile.prod
          target: runner
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            NODE_ENV=production
```

## Design Decisions

### Multi-stage vs. single-stage builds

**Decision**: Multi-stage with 5 stages.

**Rationale**: Each stage has a specific purpose and can be cached independently. Changes to source code only invalidate the `builder` stage — all previous stages remain cached. The final `runner` stage contains only runtime essentials.

### Why not use a single base image for all services?

Different services have different requirements:
- Web app needs Next.js runtime
- API app needs the same but can run on different hardware
- Background workers only need Prisma + service clients

However, the current approach creates a unified image. For more granular control, split into per-service Dockerfiles.

### Prisma in production

Prisma needs the generated client and the query engine binary. The `prod-deps` stage installs production Prisma deps, and the builder generates the client. Both are copied to the runner stage.

## Integration Points

- **Docker Compose**: Production override file orchestrates services
- **CI/CD**: GitHub Actions builds and pushes images
- **Kubernetes**: Uses the runner image for pods
- **Health checks**: Dockerfile includes HEALTHCHECK instruction

## Production Considerations

1. **Image scanning**: Run `trivy` or `snyk` on built images to detect vulnerabilities before pushing to registry
2. **Tagging strategy**: Use semantic versioning tags (`v1.2.3`) and short SHA tags for traceability. Never use `:latest` in production
3. **Layer caching**: Docker layer caching dramatically speeds up builds. GitHub Actions uses `type=gha` cache, which persists between workflow runs
4. **Base image updates**: Regularly update the base `node:20-slim` image for security patches. Use Dependabot or Renovate for automated Docker image updates
5. **Distroless images**: For maximum security, use `gcr.io/distroless/nodejs` base images. These contain only the application runtime and glibc — no shell, no package manager, no utilities
