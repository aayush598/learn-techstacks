# Section 02: Development Dockerfile

## Overview

The development Dockerfile creates a container environment with hot reload, volume mounts for live code changes, and optimized caching for fast rebuilds. This enables developers to run the application inside a container while still getting instant feedback on code changes.

## Development Dockerfile

```dockerfile
# docker/Dockerfile.dev
FROM node:20-slim AS base

# Install pnpm globally
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && corepack prepare pnpm@9 --activate

# Install system dependencies
RUN apt-get update && apt-get install -y \
  openssl \
  git \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# ── Dependencies layer ─────────────────────────────────────
FROM base AS deps
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY apps/web/package.json ./apps/web/
COPY apps/api/package.json ./apps/api/
COPY packages/*/package.json ./packages/

# Install dependencies (with frozen lockfile for reproducibility)
RUN pnpm install --frozen-lockfile

# ── Development image ──────────────────────────────────────
FROM deps AS dev

# Copy source code (will be overridden by volume mounts)
COPY . .

# Expose application ports
EXPOSE 3000 4000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/api/health || exit 1

# Default command: run in dev mode with hot reload
CMD ["pnpm", "dev"]
```

## Docker Compose Integration

```yaml
# docker/docker-compose.dev.yml
version: "3.9"

services:
  # ── Web App (Next.js Frontend) ──────────────────────────
  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile.dev
      target: dev
    container_name: voice-agent-web
    ports:
      - "3000:3000"
    env_file:
      - ../.env
      - ../.env.development
      - ../.env.local
    environment:
      - NODE_ENV=development
      - WATCHPACK_POLLING=true    # Enable file watching on Docker
    volumes:
      # Source code mounted for hot reload
      - ../apps/web/src:/app/apps/web/src
      - ../packages:/app/packages
      # Next.js build cache (persist between restarts)
      - web-next-cache:/app/apps/web/.next
      # Exclude node_modules (use container's own)
      - /app/node_modules
      - /app/apps/web/node_modules
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - voice-agent-dev

  # ── API App (Next.js API) ───────────────────────────────
  api:
    build:
      context: ..
      dockerfile: docker/Dockerfile.dev
      target: dev
    container_name: voice-agent-api
    ports:
      - "4000:4000"
    env_file:
      - ../.env
      - ../.env.development
      - ../.env.local
    environment:
      - NODE_ENV=development
      - PORT=4000
      - WATCHPACK_POLLING=true
    volumes:
      - ../apps/api/src:/app/apps/api/src
      - ../packages:/app/packages
      - api-next-cache:/app/apps/api/.next
      - /app/node_modules
      - /app/apps/api/node_modules
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      kafka:
        condition: service_healthy
    networks:
      - voice-agent-dev

volumes:
  web-next-cache:
  api-next-cache:
```

## Hot Reload Configuration

### Next.js with Docker

```javascript
// apps/web/next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable React Strict Mode for development
  reactStrictMode: true,

  // Transpile workspace packages
  transpilePackages: [
    "@voice-agent/ui",
    "@voice-agent/db",
    "@voice-agent/types",
    "@voice-agent/voice",
    "@voice-agent/ai",
  ],

  // Webpack configuration for Docker
  webpack: (config, { isServer }) => {
    // Enable polling for file watching in Docker
    config.watchOptions = {
      poll: 1000,
      aggregateTimeout: 300,
      ignored: ["**/node_modules", "**/.next", "**/dist"],
    };
    return config;
  },
};

module.exports = nextConfig;
```

### Turborepo Watch Mode

```jsonc
// turbo.json
{
  "pipeline": {
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

## Node Modules Handling

The `docker-compose.dev.yml` uses anonymous volumes to exclude `node_modules` from bind mounts:

```yaml
volumes:
  - /app/node_modules
  - /app/apps/web/node_modules
  - /app/apps/api/node_modules
```

This ensures the container uses its own `node_modules` (installed during the `deps` stage) rather than trying to use the host's `node_modules`, which may have different binary compatibility.

## Environment Configuration

```yaml
# docker/.env.dev
# Override .env values for Docker environment
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/voice_agent_dev
REDIS_URL=redis://redis:6379
KAFKA_BROKERS=kafka:9092
MINIO_ENDPOINT=minio
MINIO_PORT=9000
```

Note the service names (`postgres`, `redis`, `kafka`, `minio`) instead of `localhost`. These resolve via Docker's internal DNS when the app runs inside a container.

## Development Workflow

```bash
# Start development environment
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.dev.yml up -d

# View logs
docker compose logs -f web api

# Enter a container for debugging
docker exec -it voice-agent-web /bin/bash

# Rebuild after dependency changes
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.dev.yml build --no-cache web

# Stop development environment
docker compose -f docker/docker-compose.yml \
  -f docker/docker-compose.dev.yml down
```

## Debugging in Docker

```yaml
# docker/docker-compose.dev.yml (debug extensions)
services:
  web:
    ports:
      - "9229:9229"   # Node.js debugger
    environment:
      - NODE_OPTIONS=--inspect=0.0.0.0:9229
```

```jsonc
// .vscode/launch.json (Docker debugging)
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Docker: Attach to Web",
      "type": "node",
      "request": "attach",
      "address": "localhost",
      "port": 9229,
      "localRoot": "${workspaceFolder}/apps/web",
      "remoteRoot": "/app/apps/web",
      "sourceMaps": true
    }
  ]
}
```

## Design Decisions

### Why a multi-stage Dockerfile for development?

Multi-stage allows us to separate the heavy dependency installation from the development runtime. The `deps` stage is cached and only rebuilds when `pnpm-lock.yaml` changes. This means most `docker compose build` calls only take a few seconds.

### Why WATCHPACK_POLLING=true?

Docker's filesystem events don't always propagate correctly to Webpack's file watcher. Enabling polling forces Webpack to periodically check for file changes, ensuring hot reload works reliably in Docker.

## Integration Points

- **Docker Compose**: Orchestrates containers
- **Volume mounts**: Enable hot reload
- **Environment files**: Configure service connections
- **Turbo Repo**: Coordinates parallel dev servers
- **VS Code**: Debugger attaches to containerized Node.js

## Production Considerations

1. **Volume performance**: Bind mounts on macOS are slow. For better performance, use Docker's `:cached` or `:delegated` mount flags: `- ../apps/web/src:/app/apps/web/src:cached`
2. **File permissions**: Container processes run as `node` user (UID 1000). If the host has different UIDs, permission issues can arise. Use `user: "${UID:-1000}:${GID:-1000}"` in the Compose service
3. **Cache directories**: Persist `.next`, `.turbo`, and other cache directories in Docker volumes to preserve cache between restarts
4. **Resource limits**: Set resource constraints in Docker Desktop to prevent containers from consuming all host memory: `deploy: { resources: { limits: { memory: "4G" } } }`
5. **Security**: The dev Dockerfile installs additional tools (git, curl) that shouldn't be in production. Use a separate production Dockerfile (see Section 03)
