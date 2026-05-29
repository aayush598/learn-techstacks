# Section 05: DevContainers Setup

## Overview

DevContainers provide a fully configured, reproducible development environment that runs inside Docker. By defining the development container as code, every team member gets the same tools, extensions, and configuration — eliminating "works on my machine" issues entirely.

## DevContainer Configuration

```jsonc
// .devcontainer/devcontainer.json
{
  "name": "Voice Agent Platform",
  "dockerComposeFile": ["../docker/docker-compose.yml", "../docker/docker-compose.dev.yml"],
  "service": "web",
  "workspaceFolder": "/app",

  // Features to install in the container
  "features": {
    "ghcr.io/devcontainers/features/node:1": {
      "version": "20",
      "nodeGypDependencies": true
    },
    "ghcr.io/devcontainers/features/git:1": {},
    "ghcr.io/devcontainers/features/github-cli:1": {},
    "ghcr.io/devcontainers/features/docker-outside-of-docker:1": {
      "version": "latest"
    }
  },

  // Forward ports from the container to the host
  "forwardPorts": [3000, 4000, 5432, 6379, 9000, 9001, 8025, 5050],
  "portsAttributes": {
    "3000": { "label": "Web App", "onAutoForward": "notify" },
    "4000": { "label": "API Server", "onAutoForward": "notify" },
    "5432": { "label": "PostgreSQL", "onAutoForward": "silent" },
    "6379": { "label": "Redis", "onAutoForward": "silent" },
    "9000": { "label": "MinIO API", "onAutoForward": "silent" },
    "9001": { "label": "MinIO Console", "onAutoForward": "openBrowser" },
    "8025": { "label": "Mailpit", "onAutoForward": "notify" },
    "5050": { "label": "pgAdmin", "onAutoForward": "notify" }
  },

  // VS Code extensions to install in the container
  "extensions": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "Prisma.prisma",
    "eamodio.gitlens",
    "ms-azuretools.vscode-docker",
    "ZixuanChen.vitest-explorer",
    "ms-playwright.playwright",
    "yzhang.markdown-all-in-one",
    "streetsidesoftware.code-spell-checker",
    "aaron-bond.better-comments",
    "christian-kohler.path-intellisense",
    "formulahendry.auto-rename-tag",
    "mikestead.dotenv"
  ],

  // VS Code settings for the container
  "settings": {
    "terminal.integrated.defaultProfile.linux": "bash",
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
      "source.fixAll.eslint": "explicit"
    },
    "typescript.enablePromptUseWorkspaceTsdk": true,
    "typescript.tsdk": "/app/node_modules/typescript/lib",
    "files.eol": "\n",
    "files.insertFinalNewline": true,
    "files.trimTrailingWhitespace": true
  },

  // Post-create commands
  "postCreateCommand": "pnpm install --frozen-lockfile && pnpm build",
  "postStartCommand": "pnpm docker:up",

  // Remote user
  "remoteUser": "node",

  // Container environment variables
  "containerEnv": {
    "NODE_ENV": "development",
    "WATCHPACK_POLLING": "true"
  },

  // Customizations
  "customizations": {
    "vscode": {
      "settings": {
        "workbench.colorTheme": "GitHub Dark Default",
        "workbench.iconTheme": "material-icon-theme"
      }
    }
  }
}
```

## Dockerfile for DevContainer

```dockerfile
# .devcontainer/Dockerfile
FROM mcr.microsoft.com/devcontainers/javascript-node:20

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
  openssl \
  postgresql-client \
  redis-tools \
  kafkacat \
  curl \
  jq \
  && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN corepack enable && corepack prepare pnpm@9 --activate

# Install global tools
RUN npm install -g \
  @anthropic-ai/claude-code \
  turbo \
  prisma

# Set up shell
RUN echo 'export PS1="\\w $ "' >> ~/.bashrc
RUN echo 'alias dc="docker compose"' >> ~/.bashrc
RUN echo 'alias dcu="docker compose up -d"' >> ~/.bashrc
RUN echo 'alias dcd="docker compose down"' >> ~/.bashrc
RUN echo 'alias dcl="docker compose logs -f"' >> ~/.bashrc

WORKDIR /app
```

## Lifecycle Scripts

```bash
#!/bin/bash
# .devcontainer/post-create.sh
# Runs after the container is created

set -e

echo "🚀 Setting up Voice Agent Platform development environment..."

# Install pnpm dependencies
echo "📦 Installing dependencies..."
pnpm install --frozen-lockfile

# Generate Prisma client
echo "🗄️  Generating Prisma client..."
pnpm --filter @voice-agent/db run db:generate

# Run database migrations
echo "🔄 Running database migrations..."
pnpm --filter @voice-agent/db run db:migrate

# Seed database
echo "🌱 Seeding database..."
pnpm --filter @voice-agent/db run db:seed

echo ""
echo "✅ Development environment ready!"
echo ""
echo "📋 Available commands:"
echo "   pnpm dev          - Start all dev servers"
echo "   pnpm dev:web      - Start web app only"
echo "   pnpm dev:api      - Start API server only"
echo "   pnpm test         - Run tests"
echo "   pnpm lint         - Lint code"
echo ""
echo "🔗 Service URLs:"
echo "   Web App:    http://localhost:3000"
echo "   API Server: http://localhost:4000"
echo "   MinIO:      http://localhost:9001"
echo "   Mailpit:    http://localhost:8025"
echo "   pgAdmin:    http://localhost:5050"
echo ""
```

## Environment-Specific DevContainers

### Minimal DevContainer (for quick edits)

```jsonc
// .devcontainer/minimal/devcontainer.json
{
  "name": "Voice Agent - Minimal",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "forwardPorts": [3000, 4000],
  "postCreateCommand": "pnpm install",
  "extensions": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

### Database-Only DevContainer

```jsonc
// .devcontainer/db-only/devcontainer.json
{
  "name": "Voice Agent - Database Tools",
  "dockerComposeFile": "../../docker/docker-compose.yml",
  "service": "pgadmin",
  "forwardPorts": [5432, 6379, 9000, 5050],
  "extensions": [
    "ms-azuretools.vscode-docker"
  ]
}
```

## DevContainer Benefits

```text
Without DevContainers:
  1. Install Node.js (correct version?)
  2. Install pnpm (correct version?)
  3. Install Docker
  4. Pull and configure services
  5. Install VS Code extensions
  6. Configure settings.json
  7. Install system deps (openssl)
  8. Run npm install
  9. Run database migrations
  10. Seed database
  Total: 30-60 minutes, error-prone

With DevContainers:
  1. Install VS Code + Docker
  2. "Reopen in Container"
  Total: 5-10 minutes, deterministic
```

## Design Decisions

### Full-stack DevContainer vs. Service-only Compose

**Decision**: The DevContainer runs the application inside the container, while external services run as separate containers in the same Docker network.

**Rationale**: Running the application inside the container ensures consistent runtime behavior (same Node.js version, same system dependencies). External services remain separate because they're shared across all applications and don't need the development tooling.

### Why not use DevContainer features for everything?

DevContainer features are convenient but can be brittle when multiple features interact. For critical tooling (Node.js, pnpm), we use explicit installation in the Dockerfile rather than features.

## Integration Points

- **Docker Compose**: DevContainer references the compose file for service dependencies
- **VS Code**: Everything runs inside the container — editor, terminal, extensions
- **Git**: Git is configured inside the container with the host's credentials forwarded
- **Docker socket**: Docker-outside-of-Docker feature allows running Docker commands from within the container

## Production Considerations

1. **Performance**: DevContainers on macOS use virtiofs for file sharing, which can be slower than native. Use `"workspaceMount": "type=bind,source=${localWorkspaceFolder},target=/app,consistency=cached"` for better performance
2. **Disk space**: DevContainers can consume significant disk space (Docker images, volumes, node_modules). Set Docker Desktop resource limits
3. **Git credential forwarding**: Ensure `git config --global credential.helper` is configured on the host. DevContainers automatically forward credentials
4. **SSH agent forwarding**: For private repository access, enable SSH agent forwarding in devcontainer.json: `"mounts": ["source=${env:HOME}${env:USERPROFILE}/.ssh,target=/home/node/.ssh,type=bind"]`
5. **Team adoption**: Provide documentation and a troubleshooting guide for the DevContainer setup. Schedule a team workshop to ensure everyone can get started
