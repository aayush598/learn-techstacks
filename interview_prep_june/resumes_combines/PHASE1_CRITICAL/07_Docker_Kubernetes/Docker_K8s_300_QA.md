# Docker & Kubernetes — 300+ Interview Q&A (YC Startup Level)

> **Level**: YC Startup / Senior Engineer  
> **Focus**: Deep understanding, real-world production patterns, CLI commands, YAML manifests, troubleshooting  
> **Total Questions**: 300+

---

# DOCKER (Q1–Q160)

---

## 1. What is Docker?

Docker is a containerization platform that packages applications and their dependencies into lightweight, portable containers. Containers run consistently across any system with a Docker runtime — developer laptops, CI/CD, staging, or production servers.

**Key Components:**
- **Docker Engine** — the runtime that builds and runs containers
- **Docker Images** — read-only templates (layered filesystem)
- **Docker Containers** — running instances of images
- **Docker Registry** — stores and distributes images (Docker Hub, ECR, GCR)
- **Dockerfile** — declarative recipe to build an image

---

## 2. Containers vs Virtual Machines — Detailed Comparison

| Feature | Containers | VMs |
|---|---|---|
| **OS Overhead** | Share host OS kernel; no guest OS | Each VM runs full guest OS |
| **Startup Time** | Milliseconds to seconds | Minutes |
| **Size** | MB to low GB | GB to tens of GB |
| **Isolation** | Process-level (kernel namespaces + cgroups) | Hardware-level hypervisor isolation |
| **Resource Usage** | Lightweight; only what the app needs | Heavy; reserves resources for full OS |
| **Portability** | Runs anywhere with container runtime | Requires compatible hypervisor |
| **Security Boundary** | Shared kernel — weaker isolation (but improving with gVisor, Kata) | Stronger; each VM has its own kernel |
| **Density** | 10s–100s per host | 1–10 per host typical |
| **Persistent Storage** | Volumes / bind mounts | Virtual disks |
| **Management** | Orchestrators (K8s, Swarm, Nomad) | Hypervisor (vSphere, Hyper-V, KVM) |

**When to use which?**  
- Containers: microservices, stateless apps, CI/CD, fast dev workflows  
- VMs: workloads requiring full OS isolation, legacy apps, running different kernels, security-hardened multi-tenant scenarios

---

## 3. Docker Architecture

```
+-----------------+     +---------------------+     +----------------+
|  Docker CLI     |---->|  Docker Daemon      |---->|  Registry      |
|  (client)       |     |  (dockerd)          |     |  (Hub/ECR)     |
+-----------------+     +---------------------+     +----------------+
                        |  Images | Containers |
                        |  Volumes| Networks   |
                        +------------------------+
```

- **Docker Daemon (dockerd)**: Background service managing images, containers, networks, volumes. Listens on /var/run/docker.sock.
- **Docker Client (docker)**: CLI that talks to daemon via REST API (Unix socket or TCP).
- **Registry**: Stores/distributes images. Default: Docker Hub.
- **Images**: Read-only templates built from Dockerfile instructions.
- **Containers**: Runnable instance of an image — isolated via namespaces, constrained via cgroups.

---

## 4. Dockerfile Instructions — Complete Reference

```dockerfile
FROM python:3.11-slim AS builder
LABEL maintainer="team@startup.com"
ARG APP_ENV=production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
ADD https://example.com/setup.sh /tmp/setup.sh
RUN pip install --no-cache-dir -r requirements.txt
RUN addgroup --system app && adduser --system --group app
EXPOSE 8000
VOLUME ["/app/data"]
USER app
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key Instructions:**
- **FROM**: Base image. Can use `AS <name>` for multi-stage.
- **ARG**: Build-time variables (not persisted).
- **ENV**: Runtime environment variables (persisted in image).
- **WORKDIR**: Sets working directory (creates if missing).
- **COPY**: Copies local files into image.
- **ADD**: Like COPY but supports URLs and tar auto-extraction.
- **RUN**: Executes commands during build (creates a layer).
- **EXPOSE**: Documentation only — declares port.
- **VOLUME**: Declares mount point for persistent data.
- **USER**: Switches to non-root user.
- **HEALTHCHECK**: Docker daemon health check.
- **CMD**: Default command (can be overridden).
- **ENTRYPOINT**: Main executable (harder to override).
- **LABEL**: Metadata key-value pairs.
- **SHELL**: Changes default shell (useful for Windows).
- **STOPSIGNAL**: Custom stop signal.

---

## 5. CMD vs ENTRYPOINT — Deep Dive

| | CMD | ENTRYPOINT |
|---|---|---|
| **Purpose** | Default arguments / default command | Main executable for the container |
| **Override on docker run** | Full CMD is replaced | Only appended after ENTRYPOINT unless --entrypoint flag used |
| **Syntaxes** | CMD command param1 (shell), CMD ["exec","param1"] (exec), CMD ["param1"] (default args for ENTRYPOINT) | ENTRYPOINT command (shell), ENTRYPOINT ["exec","param1"] (exec) |
| **Combined behavior** | If ENTRYPOINT is set, CMD becomes default args for ENTRYPOINT | If CMD is set alone, it's the main command |

**Combined Example:**
```dockerfile
ENTRYPOINT ["curl"]
CMD ["--help"]
```
- `docker run myimage` -> runs `curl --help`
- `docker run myimage http://example.com` -> runs `curl http://example.com`

**Best Practice:** Use ENTRYPOINT for the binary, CMD for default flags. Always prefer exec form over shell form.

---

## 6. Docker Image Layers and Layer Caching

Every Dockerfile instruction creates a read-only **layer**. Layers are stacked via UnionFS (Overlay2). If a layer hasn't changed, Docker reuses it from cache.

**Layer chain:**
```
FROM python:3.11-slim          # Layer A (base)
WORKDIR /app                   # Layer B
COPY requirements.txt .        # Layer C
RUN pip install -r req.txt     # Layer D
COPY . .                       # Layer E
CMD ["python", "app.py"]       # metadata (thin layer)
```

**Caching Rules:**
- Docker compares instruction text and file checksums
- If COPY/ADD source files changed, cache invalidates from that point
- RUN cache busts if preceding layer changed

**Optimization:** Order from least to most frequently changing:
```dockerfile
# BAD
COPY . .
RUN pip install -r requirements.txt

# GOOD
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

View layers: `docker history <image>`

---

## 7. Multi-Stage Builds

Build with multiple FROM statements; only the final stage's files are kept.

```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Python multi-stage:**
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

**Benefits:** Smaller images (no build tools), reduced attack surface, faster deploys.

---

## 8. Docker Compose — Defining Multi-Container Apps

```yaml
version: "3.9"
services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    env_file: .env
    volumes:
      - ./api:/app
      - /app/__pycache__
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - app-net
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: myapp
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-net

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    networks:
      - app-net

networks:
  app-net:
    driver: bridge

volumes:
  pgdata:
  redis-data:
```

### Compose Profiles
```yaml
services:
  api:
    image: myapp-api
    profiles: ["prod", "dev"]
  debug-tools:
    image: busybox
    profiles: ["dev"]
```
Run: `docker compose --profile dev up`

### depends_on Conditions
- `service_started` (default)
- `service_healthy` — waits for healthcheck
- `service_completed_successfully` — waits for zero exit

---

## 9. Docker Networking Drivers

| Driver | Use Case | Details |
|---|---|---|
| **bridge** | Default; single-host | Containers on same bridge see each other by name |
| **host** | No isolation; container uses host IP | Performance; port conflicts possible |
| **overlay** | Multi-host (Swarm) | Encrypted option available |
| **macvlan** | Assign MAC addresses to containers | Containers appear as physical devices |
| **ipvlan** | Like macvlan, same MAC | Higher scalability |
| **none** | No networking | Loopback only; security-isolated batch jobs |

**Custom bridge:**
```bash
docker network create --driver bridge --subnet 172.20.0.0/16 mynet
docker run --network mynet --name app1 nginx
docker run --network mynet --name app2 nginx
# app2 resolves app1 by DNS name
```

---

## 10. Docker Volumes vs Bind Mounts vs tmpfs

| Feature | Volumes | Bind Mounts | tmpfs |
|---|---|---|---|
| Managed by Docker | Yes (/var/lib/docker/volumes/) | No (any host path) | In-memory only |
| Backup/Restore | Easy (--volumes-from) | Manual | Not persistent |
| Sharing across containers | Yes | Yes | Not possible |
| Performance | Native | Native (bypasses storage driver) | Fast (RAM) |
| Use Case | Database data, persistent storage | Live code reload, config files | Secrets, temp data, scratch |

**Commands:**
```bash
docker volume create mydata
docker run -v mydata:/data nginx
docker run -v $(pwd):/app nginx
docker run --tmpfs /tmp:size=100m nginx
docker run -v $(pwd):/app:ro nginx
```

---

## 11. Docker Registry (Docker Hub, ECR, GCR, Private)

```bash
# Login
docker login
docker login myregistry.com -u user -p pass

# Tag and push
docker tag myapp:latest myregistry.com/myapp:1.0
docker push myregistry.com/myapp:1.0

# Pull
docker pull myregistry.com/myapp:1.0

# Run local registry
docker run -d -p 5000:5000 --name registry registry:2
docker tag myapp localhost:5000/myapp:1.0
docker push localhost:5000/myapp:1.0
```

**Cloud Registries:**
- **ECR**: aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
- **GCR**: gcloud auth configure-docker
- **ACR**: az acr login --name <name>

---

## 12. Dockerfile Best Practices

1. **Minimize layers**: Combine RUN commands with &&
2. **Use .dockerignore** to exclude unnecessary files
3. **Separate dependency install from code copy** (leverage caching)
4. **Use specific base image tags** (not `latest`)
5. **Run as non-root**: adduser + USER
6. **Multi-stage builds** for smaller images
7. **Pin base image digests** for reproducibility
8. **Use WORKDIR** instead of RUN cd
9. **Prefer COPY over ADD**
10. **Use --no-cache-dir** for pip, --no-cache for apt
11. **Include HEALTHCHECK** instruction

---

## 13. Essential Docker Commands

```bash
# Build
docker build -t myapp:latest .
docker build --no-cache -t myapp:latest .
docker build --target builder -t myapp:builder .
docker build -f Dockerfile.prod -t myapp:prod .

# Run
docker run -d --name myapp -p 8080:80 myapp:latest
docker run --rm -it myapp sh
docker run -e "VAR=val" -v /host:/container myapp
docker run --network mynet --restart always myapp
docker run --cpus=1 --memory=512m myapp

# List
docker ps           # running
docker ps -a        # all
docker images       # all images

# Manage
docker stop myapp && docker rm myapp
docker start myapp
docker restart myapp
docker rm -f myapp

# Execute
docker exec -it myapp bash
docker exec myapp ls /app

# Logs
docker logs myapp
docker logs --tail 100 -f myapp
docker logs --since 5m myapp

# Inspect
docker inspect myapp
docker inspect --format '{{.State.Status}}' myapp

# Stats
docker stats
docker stats myapp

# Copy
docker cp myapp:/app/config.json ./local-config.json

# Clean up
docker system prune -af
docker volume prune -f
```

---

## 14. Docker Health Checks

**In Dockerfile:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8080/health || exit 1
```

**In docker-compose:**
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

Check status: `docker inspect --format='{{json .State.Health}}' <container>`

---

## 15. Docker Resource Constraints

```bash
docker run --cpus=1.5 myapp
docker run --cpuset-cpus=0-1 myapp
docker run --memory=256m myapp
docker run --memory-reservation=128m myapp
docker run --memory-swap=512m myapp
docker run --cpus=0.5 --memory=256m --memory-swap=384m myapp
```

**docker-compose:**
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: "0.5"
          memory: 256M
        reservations:
          cpus: "0.25"
          memory: 128M
```

---

## 16. Docker Tags and Versioning

```bash
docker build -t myapp:1.0.0 -t myapp:latest .
docker tag myapp:1.0.0 myapp:stable
```

**Best practice tags:**
- `:latest` — recent stable (avoid in prod)
- `:1.0.0` — semantic version
- `:sha-abc1234` — commit hash
- `:1.0.0-alpine` — version + variant
- `:prod-123456` — build number

For immutability: `docker pull myapp@sha256:abc123...`

---

## 17. docker commit, save/load, export/import

```bash
# Commit: create image from container state
docker commit CONTAINER new-image:tag
docker commit --change "CMD [\"nginx\",\"-g\",\"daemon off;\"]" CONTAINER new-image

# Save/Load: image -> tar -> image (preserves layers, history)
docker save myapp:1.0 | gzip > myapp.tar.gz
docker load < myapp.tar.gz
docker load -i myapp.tar.gz

# Export/Import: container -> tar -> filesystem (loses history)
docker export CONTAINER > export.tar
cat export.tar | docker import - myapp:imported
```

---

## 18. Docker Swarm Basics

```bash
# Initialize
docker swarm init --advertise-addr eth0

# Join workers
docker swarm join-token worker
docker swarm join --token <TOKEN> <IP>:2377

# Deploy stack
docker stack deploy -c docker-compose.yml mystack

# List services
docker service ls
docker service ps myservice

# Scale
docker service scale myservice=5

# Update
docker service update --image myapp:2.0 myservice
docker service update --replicas 3 myservice

# Logs
docker service logs --follow myservice

# Leave
docker swarm leave --force
```

**Swarm vs K8s:** Swarm is simpler, built into Docker CLI, but lacks the ecosystem, auto-healing, and extensibility of Kubernetes.

---

## 19. Docker Secrets Management

**In Swarm:**
```bash
echo "mypassword" | docker secret create db_pass -
docker service create --secret db_pass --name myapp nginx
```

**In Docker Compose:**
```yaml
version: "3.9"
services:
  app:
    image: myapp
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Secrets mounted as tmpfs at /run/secrets/<name> inside container.

---

## 20. Docker Logging Drivers

| Driver | Command | Use Case |
|---|---|---|
| **json-file** (default) | docker logs | Local dev, single host |
| **journald** | --log-driver journald | Linux with systemd |
| **syslog** | --log-driver syslog | Centralized syslog |
| **fluentd** | --log-driver fluentd --log-opt fluentd-address=localhost:24224 | Unified logging |
| **awslogs** | --log-driver awslogs --log-opt awslogs-group=mygroup | ECS/EC2 |
| **gelf** | --log-driver gelf --log-opt gelf-address=udp://graylog:12201 | Graylog/ELK |
| **splunk** | --log-driver splunk | Splunk |
| **gcplogs** | --log-driver gcplogs | GCP |
| **none** | --log-driver none | Performance (no logs) |

**Global config (/etc/docker/daemon.json):**
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

---

## 21. Docker with FastAPI/Flask Apps

**FastAPI Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**FastAPI with Gunicorn:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
```

**Flask Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

---

## 22. Docker with Next.js Apps

**Multi-stage Dockerfile:**
```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production

FROM node:20-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT=3000
CMD ["node", "server.js"]
```

**next.config.js must have:**
```js
module.exports = {
  output: 'standalone',
}
```

---

## 23. Docker Debugging

```bash
# Exec into running container
docker exec -it container_name sh
docker exec -it container_name /bin/bash

# Inspect container state
docker inspect container_name | jq .State
docker inspect --format '{{.State.Status}}' container_name

# View logs
docker logs --tail 100 -f container_name
docker logs --since 1h container_name

# Check resource usage
docker stats container_name

# Port mapping
docker port container_name

# Copy files out
docker cp container_name:/app/logs ./logs

# Debug startup failure
docker run -it --entrypoint sh image_name

# Process list
docker top container_name

# Filesystem diff
docker diff container_name

# Events
docker events --filter 'container=name'
```

---

## 24. Docker Security Best Practices

1. **Don't run as root** — use USER directive
2. **Use read-only rootfs**: --read-only --tmpfs /tmp
3. **Drop capabilities**: --cap-drop ALL --cap-add NET_BIND_SERVICE
4. **Use seccomp profiles**: --security-opt seccomp=./profile.json
5. **Use AppArmor/SELinux**
6. **Don't mount docker.sock** inside containers
7. **Scan images**: docker scan, trivy, grype
8. **Use distroless or slim base images**
9. **Pin base image digests**
10. **Enable content trust**: export DOCKER_CONTENT_TRUST=1
11. **Set resource limits**
12. **Use secrets, not env vars for sensitive data**
13. **Set WORKDIR to non-root path**

---

## 25. Docker vs Podman vs containerd

| Feature | Docker | Podman | containerd |
|---|---|---|---|
| **Daemon** | Requires dockerd (root) | Daemonless (rootless by default) | Daemon (containerd) |
| **OCI Compliant** | Yes | Yes | Yes |
| **Kubernetes CRI** | Via cri-dockerd | Via CRI-O | Native CRI |
| **Rootless** | Available (complex) | Native | Via user namespaces |
| **Pod Concept** | No native | Yes (like K8s) | No |
| **Systemd Integration** | Manual | Native (podman generate systemd) | Manual |
| **Build** | Built-in | buildah | nerdctl build or buildkit |
| **CLI Compatibility** | Standard | alias docker=podman works | nerdctl (Docker-compatible) |

---

## 26. COPY vs ADD — When to Use Each

| | COPY | ADD |
|---|---|---|
| **Local files** | Yes | Yes |
| **URL sources** | No | Yes (fetches remote files) |
| **Tar auto-extraction** | No | Yes (tar.gz, tar.bz2, etc.) |
| **Best practice** | Always prefer COPY | Only when URL fetch or auto-extract needed |

```dockerfile
# Prefer COPY
COPY ./app /app

# Use ADD for remote files
ADD https://example.com/install.sh /tmp/install.sh

# Use ADD for auto-extraction
ADD app.tar.gz /app/
```

---

## 27. Layer Caching Optimization

**Golden Rules:**
1. Copy dependency files first
2. Install dependencies in separate layer
3. Copy application code last
4. Combine RUN commands
5. Use .dockerignore to exclude irrelevant files

```dockerfile
# Optimized
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --production && npm cache clean --force
COPY . .
CMD ["node", "server.js"]
```

**Force cache bust:**
```bash
docker build --build-arg CACHE_BUST=$(date +%s) -t myapp .
```
```dockerfile
ARG CACHE_BUST
RUN echo "Cache bust: $CACHE_BUST"
```

---

## 28. Reducing Docker Image Size

| Technique | Before | After |
|---|---|---|
| **Alpine base** | python:3.11 (1GB) | python:3.11-alpine (150MB) |
| **Slim variant** | — | python:3.11-slim (120MB) |
| **Distroless** | — | gcr.io/distroless/python3 (50MB) |
| **Multi-stage** | 1GB+ | <200MB |
| **Combine RUN** | Multiple layers | Single layer |
| **Remove caches** | apt-get install | with rm -rf /var/lib/apt/lists/* |
| **--no-install-recommends** | Extra packages | Minimal |
| **.dockerignore** | Large context | Minimal |

**Distroless example:**
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM gcr.io/distroless/python3
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["app.py"]
```

---

## 29. Docker with GPU Support (nvidia-docker)

```bash
# Install
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update && sudo apt install -y nvidia-docker2
sudo systemctl restart docker

# Verify
docker run --rm --gpus all nvidia/cuda:12.0-runtime nvidia-smi

# Specific GPU
docker run --gpus "device=0" nvidia/cuda:12.0-runtime nvidia-smi
```

**docker-compose:**
```yaml
services:
  train:
    image: myapp
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

---

## 30. Docker Context and Buildx

**Docker Context:** Switch between Docker endpoints.
```bash
docker context create remote --docker "host=ssh://user@host"
docker context use remote
docker context ls
```

**Buildx:** Extended build capabilities (multi-platform, buildkit).
```bash
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap
docker buildx build --platform linux/amd64,linux/arm64 -t myapp:latest --push .
```

**docker buildx bake:**
```hcl
# docker-bake.hcl
group "default" {
  targets = ["app"]
}
target "app" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

---

## 31. Docker Restart Policies

| Policy | Behavior |
|---|---|
| no | Don't restart (default) |
| on-failure[:max-retries] | Restart if exit code != 0 |
| always | Always restart unless stopped |
| unless-stopped | Like always, but not if daemon stopped manually |

```bash
docker run --restart always nginx
docker run --restart on-failure:5 myapp
docker run --restart unless-stopped myapp
```

---

## 32. Docker ARG vs ENV

| | ARG | ENV |
|---|---|---|
| **Scope** | Build-time only | Build-time + runtime |
| **Persistence** | Not in final image | Persists in image and container |
| **Override** | --build-arg VAR=val | -e VAR=val |
| **Inspect** | Not visible in docker inspect | Visible in docker inspect |

```dockerfile
ARG BUILD_VERSION=1.0
ENV APP_ENV=production
ARG DB_URL
ENV DATABASE_URL=$DB_URL
```

```bash
docker build --build-arg BUILD_VERSION=2.0 -t myapp .
docker run -e APP_ENV=staging myapp
```

---

## 33. Docker Troubleshooting Common Issues

| Issue | Diagnosis | Fix |
|---|---|---|
| **Container exits immediately** | docker logs <container> | Debug with --entrypoint sh |
| **Port already allocated** | docker ps, netstat -tlnp | Change host port or stop conflicted container |
| **Disk space** | docker system df | docker system prune -af --volumes |
| **Network unreachable** | docker exec -it <c> ping google.com | Check DNS, network driver |
| **Permission denied** | docker exec ls -la /data | Fix UID/GID, run as correct user |
| **OOMKilled** | docker inspect <c> -> OOMKilled | Increase --memory or fix leak |
| **Layer cache not used** | Build output shows no cache | Fix .dockerignore, check file changes |
| **429 image pull** | Too Many Requests | Login, use mirror, upgrade tier |
| **docker-compose not found** | which docker-compose | Use docker compose (v2 built-in) |

---

## 34-50. Additional Docker Q&A

### 34. What is the difference between docker run and docker start?

docker run = docker create + docker start (creates new container). docker start starts an existing stopped container.

### 35. How do you pass arguments to a Docker container?

- Environment: `docker run -e MY_VAR=value`
- CMD override: `docker run image arg1 arg2`
- ENTRYPOINT override: `docker run --entrypoint '' image cmd`
- Files: `docker run -v /host/file:/container/file`

### 36. How does Docker use cgroups?

cgroups (control groups) limit and isolate resource usage (CPU, memory, disk I/O, network) per container, preventing one container from starving others.

### 37. How does Docker use namespaces?

Namespaces provide isolation:
- PID: separate process trees
- Network: separate network stacks
- Mount: separate filesystem mounts
- UTS: separate host/domain names
- IPC: separate inter-process communication
- User: separate user/group IDs

### 38. What is BuildKit?

A modern builder backend (DOCKER_BUILDKIT=1 or default in newer Docker). Features: parallel builds, cache mounts, SSH mounts, secrets, multi-platform.

### 39. How do you cache pip packages across builds?

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
```
Requires BuildKit.

### 40. What is the ONBUILD instruction?

Sets a trigger that runs when the image is used as a base for another build. Example: ONBUILD COPY . /app

### 41. What is a dangling image?

An image with no tag and no child image. docker image prune removes them.

### 42. What is the difference between docker-compose and docker stack?

docker-compose = single-host orchestration (dev). docker stack = Swarm multi-host deployment (prod), uses similar compose file.

### 43. What is a scratch image?

FROM scratch — the smallest possible image, empty filesystem. Used for statically compiled Go binaries.

```dockerfile
FROM scratch
COPY mybinary /
CMD ["/mybinary"]
```

### 44. How do you set up Docker to use a proxy?

Systemd: HTTP_PROXY in /etc/systemd/system/docker.service.d/proxy.conf
Docker CLI: `docker build --build-arg HTTP_PROXY=http://proxy:8080 .`

### 45. What is docker trust?

Docker Content Trust (Notary) — sign and verify images. `docker trust sign myapp:1.0`

### 46. How do you run a container as a specific user?

```bash
docker run --user 1001:1001 myapp
```

### 47. What is the difference between pause and stop?

docker pause freezes processes using SIGSTOP. docker stop sends SIGTERM then SIGKILL.

### 48. How do you share data between two containers?

Use a shared volume: `docker volume create shared`, then both containers mount `-v shared:/data`.

### 49. What is docker compose down -v?

Stops and removes containers, networks, and volumes (deletes persistent data).

### 50. How do you validate a compose file?

```bash
docker compose config
```

---

# KUBERNETES (Q161–Q300)

---

## 51. What is Kubernetes?

Kubernetes (K8s) is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

**Why use it?**
- **Self-healing**: Restarts failed containers, replaces nodes, reschedules pods
- **Scaling**: Horizontal (replicas) and vertical (resource adjustments)
- **Rolling updates/rollbacks**: Zero-downtime deployments
- **Service discovery and load balancing**: DNS-based resolution
- **Secret and config management**: Without rebuilding images
- **Storage orchestration**: Mount any storage system
- **Batch execution**: Jobs, CronJobs
- **Multi-cloud/hybrid**: Consistent across on-prem, AWS, GCP, Azure

---

## 52. Kubernetes Architecture

```
CONTROL PLANE:
+-------------+ +---------------+ +------------------+
| API Server  | | Controller    | | Scheduler        |
| (kube-      | | Manager       | | (kube-scheduler) |
| apiserver)  | |               | |                  |
+------+------+ +---------------+ +------------------+
       |
+------+----+
|   etcd    |
+-----------+
       |
       v
WORKER NODES:
+----------+ +----------+ +---------------+
| kubelet  | | kube-proxy| | Container    |
|          | |           | | Runtime      |
+----------+ +----------+ +---------------+
| Pods (containers)                        |
+------------------------------------------+
```

**Components:**
- **kube-apiserver**: Front-end for control plane. Handles REST calls, validates/processes requests.
- **etcd**: Distributed key-value store — cluster state, configs, secrets.
- **kube-scheduler**: Assigns pods to nodes based on resources, policies, affinity, taints.
- **kube-controller-manager**: Runs controller processes (Node, Replication, Endpoint, etc.).
- **kubelet**: Agent on each node ensures containers are running as defined.
- **kube-proxy**: Network proxy — maintains iptables/IPVS rules for Services.

---

## 53. What is a Pod?

A Pod is the smallest deployable unit in Kubernetes — one or more containers sharing network namespace, storage, and lifecycle.

**Why pods, not containers directly?**
- Sidecar pattern (logging, proxy, metrics alongside main container)
- Tight coupling — helper containers share resources with main app
- Atomic scheduling — all containers in a pod land on the same node

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 8080
    resources:
      requests:
        cpu: "250m"
        memory: "128Mi"
      limits:
        cpu: "500m"
        memory: "256Mi"
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 3
      periodSeconds: 5
  initContainers:
  - name: init-db
    image: busybox
    command: ['sh', '-c', 'until nc -z db-service 5432; do echo waiting; sleep 2; done;']
  restartPolicy: Always
```

---

## 54. Deployments — Rolling Updates, Rollbacks, Strategies

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:1.0
        ports:
        - containerPort: 8080
```

**Key commands:**
```bash
kubectl create deployment myapp --image=myapp:1.0
kubectl apply -f deployment.yaml
kubectl set image deployment/myapp myapp=myapp:2.0
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2
kubectl scale deployment/myapp --replicas=5
kubectl autoscale deployment/myapp --min=3 --max=10 --cpu-percent=70
```

**Strategies:**
- **RollingUpdate** (default): Gradually replaces pods
- **Recreate**: Deletes all old pods before creating new ones (downtime)

**maxSurge:** Pods above desired count (default 25%)
**maxUnavailable:** Pods below desired count (default 25%)

---

## 55. Services — ClusterIP, NodePort, LoadBalancer, ExternalName

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

| Type | Access | Use Case |
|---|---|---|
| **ClusterIP** | Inside cluster only | Internal microservice communication |
| **NodePort** | Node IP + port (30000-32767) | Dev/test, direct node access |
| **LoadBalancer** | External LB (cloud) | Production external access |
| **ExternalName** | DNS alias | Aliasing external services |

**Headless Service** (clusterIP: None) — direct pod-to-pod DNS.

---

## 56. Ingress Controllers and Ingress Resources

Ingress exposes HTTP/HTTPS routes to services. Requires an Ingress Controller (NGINX, Traefik, ALB).

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-service
            port:
              number: 80
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
```

**Install NGINX Ingress Controller:**
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.0/deploy/static/provider/cloud/deploy.yaml
```

---

## 57. ConfigMaps and Secrets

**ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: production
  LOG_LEVEL: info
```

**Secret:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
data:
  DB_PASSWORD: c3VwZXJzZWNyZXQK
stringData:
  API_KEY: abc123
```

**Using in pods:**
```yaml
spec:
  containers:
  - name: app
    env:
    - name: APP_ENV
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_ENV
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secret
          key: DB_PASSWORD
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
      readOnly: true
  volumes:
  - name: config-volume
    configMap:
      name: app-config
```

**Commands:**
```bash
kubectl create configmap app-config --from-literal=key=val --from-file=config.properties
kubectl create secret generic app-secret --from-literal=DB_PASSWORD=supersecret
```

---

## 58. Persistent Volumes and Persistent Volume Claims

```yaml
# PV (cluster storage resource)
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-nfs
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteMany
  nfs:
    server: nfs.example.com
    path: /exports/data
  persistentVolumeReclaimPolicy: Retain

# PVC (user request)
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

**Access Modes:** ReadWriteOnce (RWO), ReadOnlyMany (ROX), ReadWriteMany (RWX)
**Reclaim Policies:** Retain, Delete, Recycle (deprecated)

---

## 59. StorageClasses

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  fsType: ext4
  encrypted: "true"
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

**Common provisioners:** aws-ebs, gce-pd, azure-disk, nfs, csi-hostpath
**volumeBindingMode:** Immediate (default) or WaitForFirstConsumer (avoids zone mismatches)

---

## 60. Namespaces — When and Why?

Namespaces virtualize a cluster for isolation:
- Multi-environment (dev, staging, prod on one cluster)
- Team boundaries (with RBAC)
- Multi-tenancy
- System components (kube-system, kube-public)

```bash
kubectl create namespace staging
kubectl config set-context --current --namespace=staging
```

**ResourceQuota example:**
```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: dev
spec:
  hard:
    pods: "20"
    requests.cpu: "4"
    requests.memory: "8Gi"
```

---

## 61. StatefulSets vs Deployments

| Feature | Deployment | StatefulSet |
|---|---|---|
| Pod identity | Random names, interchangeable | Sticky (web-0, web-1, ...) |
| Storage | Shared PVC | Each pod gets own PVC |
| Ordering | All pods created simultaneously | Ordered, graceful |
| DNS | No stable per-pod DNS | web-0.mysql.default.svc.cluster.local |
| Scaling | Any pod removable | Pods removed in reverse order |
| Use case | Stateless apps, web servers | Databases, Kafka, ZooKeeper |

---

## 62. DaemonSets

Ensures all (or some) nodes run a copy of a pod. Used for:
- Log collection (Fluentd, Filebeat)
- Monitoring agents (Prometheus Node Exporter)
- Network plugins (Calico, Flannel)
- Security agents (Falco)

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      tolerations:
      - key: node-role.kubernetes.io/control-plane
        effect: NoSchedule
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.16
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

---

## 63. Jobs and CronJobs

**Job:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 4
  activeDeadlineSeconds: 300
  template:
    spec:
      containers:
      - name: migration
        image: myapp:1.0
        command: ["python", "migrate.py"]
      restartPolicy: Never
```

**CronJob:**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-cleanup
spec:
  schedule: "0 3 * * *"
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cleanup
            image: busybox
            command: ["sh", "-c", "find /tmp -type f -mtime +7 -delete"]
          restartPolicy: OnFailure
```

---

## 64. Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
    scaleUp:
      stabilizationWindowSeconds: 0
```

**Commands:**
```bash
kubectl autoscale deployment myapp --min=3 --max=20 --cpu-percent=70
kubectl get hpa -w
kubectl describe hpa myapp-hpa
```

**Prerequisites:** Metrics Server installed.

---

## 65. Vertical Pod Autoscaler (VPA)

Adjusts CPU/memory requests/limits automatically.

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: "100m"
        memory: "128Mi"
      maxAllowed:
        cpu: "4"
        memory: "8Gi"
```

**Modes:** Off (recommend only), Initial (at creation), Auto (evict and update)

---

## 66. Resource Requests and Limits

**Requests** = guaranteed minimum (used by scheduler).
**Limits** = maximum allowed (enforced by kubelet).

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

**QoS Classes (from best to worst eviction priority):**
- **Guaranteed**: requests == limits
- **Burstable**: requests != limits
- **BestEffort**: no requests/limits

---

## 67. Liveness, Readiness, and Startup Probes

```yaml
livenessProbe:           # Restart if fails (deadlock detection)
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:          # Remove from Service if fails
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5

startupProbe:            # Delays liveness/readiness for slow-starting apps
  httpGet:
    path: /startup
    port: 8080
  periodSeconds: 10
  failureThreshold: 30
```

**Probe types:** httpGet, tcpSocket, exec, grpc

---

## 68. Kubernetes RBAC

**Role (namespace-scoped) and ClusterRole (cluster-scoped):**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: dev
  name: pod-manager
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
```

**RoleBinding:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: dev
  name: dev-pod-managers
subjects:
- kind: User
  name: "alice@example.com"
- kind: ServiceAccount
  name: ci-deployer
  namespace: dev
roleRef:
  kind: Role
  name: pod-manager
  apiGroup: rbac.authorization.k8s.io
```

---

## 69. Network Policies

Control traffic flow between pods.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-policy
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

Requires CNI plugin with NetworkPolicy support (Calico, Cilium, Weave, Antrea).

---

## 70. Service Accounts

Non-human identities for pods.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
---
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  serviceAccountName: myapp-sa
  containers:
  - name: app
    image: myapp
```

---

## 71. Helm Basics

```bash
# Install
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-nginx bitnami/nginx
helm install my-app ./my-chart --values prod-values.yaml

# Upgrade/Rollback
helm upgrade my-app ./my-chart -f prod-values.yaml --set image.tag=2.0
helm rollback my-app 1

# Manage
helm ls
helm uninstall my-app
helm create my-chart
```

**Chart structure:**
```
my-chart/
  Chart.yaml       # metadata
  values.yaml      # default config
  charts/          # sub-charts
  templates/       # Go templates -> K8s YAML
    deployment.yaml
    service.yaml
    _helpers.tpl
```

---

## 72. kubectl Cheat Sheet

```bash
# Cluster
kubectl cluster-info
kubectl get nodes -o wide
kubectl top node

# Pods
kubectl get pods -w -o wide
kubectl describe pod pod-name
kubectl logs --tail=50 -f pod-name
kubectl exec -it pod-name -- sh
kubectl port-forward pod/pod-name 8080:80
kubectl cp pod-name:/path ./local

# Deployments
kubectl get deployments
kubectl rollout status deployment/web
kubectl rollout history deployment/web
kubectl rollout undo deployment/web --to-revision=2
kubectl scale deployment/web --replicas=5

# Services
kubectl get svc -o wide
kubectl port-forward svc/svc-name 8080:80

# Config/Secrets
kubectl get cm,secrets
kubectl describe cm config

# Debug
kubectl get events --sort-by='.lastTimestamp'
kubectl logs pod-name --previous
kubectl debug node/node-name -ti --image=busybox

# Context
kubectl config get-contexts
kubectl config use-context my-cluster
kubectl config set-context --current --namespace=prod
```

---

## 73. Pod Lifecycle

**Phases:** Pending -> Running -> Succeeded/Failed/Unknown
**Container states:** Waiting, Running, Terminated
**CrashLoopBackOff:** Container crashes repeatedly. Debug with `kubectl logs --previous`.

---

## 74. Init Containers, Sidecar, Ambassador, Adapter Patterns

**Init containers:** Run before app containers, must complete successfully.
```yaml
initContainers:
- name: init-db
  image: busybox
  command: ['sh', '-c', 'until nc -z db 5432; do sleep 2; done;']
```

**Sidecar:** Helper alongside main container (logging, proxy, metrics).
**Ambassador:** Proxy container for external communication.
**Adapter:** Transforms main container's output (e.g., metrics format conversion).

---

## 75. Kubernetes DNS and Service Discovery

Each Service gets DNS: `<service>.<namespace>.svc.cluster.local`
StatefulSet pods: `<statefulset-name-0>.<service>.<namespace>.svc.cluster.local`

**CoreDNS** is the default cluster DNS. ConfigMap in kube-system/coredns.

---

## 76. ConfigMap vs Secret

| | ConfigMap | Secret |
|---|---|---|
| Data | Plain text config | Sensitive data |
| Encoding | Plain text | Base64 (optional KMS encryption) |
| Size limit | 1 MiB | 1 MiB |
| Rotation | Pod restart needed | Can be live-mounted |
| Security | No special handling | Encrypted at rest option |

---

## 77. Taints and Tolerations

**Taints repel pods from nodes (unless tolerated).**

```bash
kubectl taint nodes node1 key=value:NoSchedule
kubectl taint nodes node1 key=value:NoExecute
kubectl taint nodes node1 key=value:PreferNoSchedule
```

```yaml
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
  - key: "key2"
    operator: "Exists"
    effect: "NoExecute"
    tolerationSeconds: 300
```

---

## 78. Node Affinity and Anti-Affinity

```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - us-west-1a
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: app
              operator: In
              values:
              - web
          topologyKey: kubernetes.io/hostname
```

---

## 79. etcd Backup and Restore

```bash
# Backup
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-snapshot.db

# Status check
ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snapshot.db

# Restore (stop API server first)
etcdctl snapshot restore /backup/etcd-snapshot.db \
  --data-dir=/var/lib/etcd-restored
systemctl start etcd kube-apiserver
```

---

## 80. Kubernetes Monitoring (Prometheus + Grafana)

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace
```

**Custom metrics (Python):**
```python
from prometheus_client import Counter, Histogram, start_http_server
REQUESTS = Counter('http_requests_total', 'Total HTTP requests')
start_http_server(8000)
```

---

## 81. Kubernetes Logging (EFK, Loki)

**EFK:** Elasticsearch + Fluentd (DaemonSet) + Kibana
**Loki:** Grafana Loki + Promtail (DaemonSet) + Grafana — lighter alternative.

```bash
helm install loki grafana/loki-stack --namespace logging --create-namespace
```

---

## 82. Kubernetes Security

**Pod Security Standards (built-in, v1.23+):**
```bash
kubectl label ns default pod-security.kubernetes.io/enforce=restricted
```

**Levels:** Privileged, Baseline, Restricted

**OPA/Gatekeeper:** Policy engine for K8s using Rego language.

---

## 83. CNI Plugins

| Plugin | Type | Key Features |
|---|---|---|
| **Calico** | L3/L4 | NetworkPolicy, BGP, eBPF, Wireguard |
| **Flannel** | L3 overlay | Simple, VXLAN, no NetworkPolicy |
| **Cilium** | L3-L7 (eBPF) | NetworkPolicy, Hubble, ServiceMesh |
| **Weave** | L3 overlay | Simple, includes DNS, NetworkPolicy |
| **Amazon VPC CNI** | Native AWS | VPC IP per pod, high performance |
| **Azure CNI** | Native Azure | VNet IPs |

---

## 84. Service Mesh (Istio, Linkerd)

**Istio:** Sidecar Envoy proxy, mTLS, traffic management, observability.
```bash
istioctl install --set profile=demo -y
kubectl label ns default istio-injection=enabled
```

**Linkerd:** Lighter, Rust-based proxy.
```bash
linkerd install | kubectl apply -f -
linkerd inject deployment/myapp
```

---

## 85. Kubernetes Operators and CRDs

**CRD:** Extends K8s API with custom resources.
**Operator:** Custom controller that watches CRDs and reconciles state.

**Popular operators:** Prometheus, PostgreSQL (CrunchyData), Elasticsearch, Kafka (Strimzi), Cert-Manager.

---

## 86. Kubernetes Troubleshooting

```bash
# Pod issues
kubectl describe pod <pod>
kubectl logs <pod> --previous

# Node issues
kubectl describe node <node>
kubectl cordon/drain <node>

# Networking
kubectl run test-pod --image=busybox --rm -it -- sh
kubectl get endpoints <service>

# Storage
kubectl describe pvc <pvc>

# Ephemeral debug container
kubectl debug -it <pod> --image=busybox --target=<container>

# Port forwarding
kubectl port-forward pod/<pod> 8080:80
kubectl port-forward svc/<svc> 8080:80
```

---

## 87. EKS vs AKS vs GKE

| Feature | EKS | AKS | GKE |
|---|---|---|---|
| Control plane | $0.10/hr | Free | Free |
| Default CNI | AWS VPC CNI | Azure CNI | kubenet/VPC-native |
| Ingress | ALB Ingress | App Gateway Ingress | GCE Ingress/GCLB |
| Storage | EBS, EFS, FSx | Azure Disk/Files | Persistent Disk, Filestore |
| Auto-scaling | Cluster Autoscaler + Karpenter | Cluster Autoscaler | Cluster Autoscaler |
| Security | IRSA | Azure AD + Managed Identity | Workload Identity |
| Serverless | Fargate | Virtual Nodes (ACI) | Autopilot |

---

## 88. Kubeconfig File Structure

```yaml
apiVersion: v1
kind: Config
current-context: prod-cluster
clusters:
- cluster:
    certificate-authority-data: <base64>
    server: https://<api-server>:6443
  name: prod-cluster
users:
- name: admin
  user:
    exec:
      command: aws
      args: ["eks", "get-token", "--cluster-name", "prod"]
contexts:
- context:
    cluster: prod-cluster
    namespace: prod
    user: admin
  name: prod-cluster
```

---

## 89. Kubernetes Secrets Encryption

**Encryption at rest with EncryptionConfiguration:**
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-32-byte-key>
  - identity: {}
```

**KMS provider** for cloud KMS integration (AWS KMS, GCP KMS, Azure Key Vault).

---

## 90. Kubernetes Backup (Velero)

```bash
velero install --provider aws --bucket velero-backups
velero backup create daily-backup --ttl=720h
velero schedule create daily --schedule="0 2 * * *"
velero restore create --from-backup daily-backup
```

---

## 91. Kubernetes Upgrade Strategy

**Managed:** Provider handles control plane. Upgrade node pools sequentially.
**Self-managed (kubeadm):**
```bash
kubeadm upgrade plan
kubeadm upgrade apply v1.29.0
kubectl drain node-name --ignore-daemonsets
kubeadm upgrade node
systemctl restart kubelet
kubectl uncordon node-name
```

**Best practices:** One minor version at a time, backup etcd, test in non-prod first, use PDB.

---

## 92. Pod Priority and Preemption

Higher priority pods can preempt (evict) lower-priority pods when resources are scarce.

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
preemptionPolicy: PreemptLowerPriority
---
spec:
  priorityClassName: high-priority
```

**Default classes:** system-cluster-critical (2000000000), system-node-critical (2000001000)

---

## 93-160. Additional K8s Q&A

### 93. What is a PodDisruptionBudget (PDB)?

Ensures minimum pod availability during voluntary disruptions:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: myapp
```

### 94. What is kubectl proxy?

Creates HTTP proxy to API server on localhost:8001.

### 95. What is the difference between kubectl apply and kubectl create?

create = imperative (error if exists). apply = declarative (create or update).

### 96. What is a ReplicaSet?

Ensures specified number of pod replicas run. Deployments manage ReplicaSets.

### 97. How do you update a ConfigMap without restarting pods?

ConfigMaps mounted as volumes auto-update (symlink swap). SubPath mounts and env vars require restart.

### 98. What is a rolling restart?

```bash
kubectl rollout restart deployment/myapp
```

### 99. What is kubectl diff?

Shows differences between local manifests and cluster state.

### 100. What is kubectl wait?

Waits for condition: `kubectl wait --for=condition=Ready pod -l app=myapp`

### 101. What is kubectl auth can-i?

Checks if user can perform action: `kubectl auth can-i create deployments`

### 102. What is emptyDir?

Ephemeral volume created when pod starts, deleted when pod removed. Shared among containers in pod.

### 103. What is hostPath?

Mounts host node filesystem into pod. Used by DaemonSets.

### 104. What is kubectl cordon?

Marks node as unschedulable. Existing pods continue running.

### 105. What is kubectl drain?

Evicts all pods from node (cordon + graceful eviction). For maintenance.

### 106. What is a mutating webhook?

Mutates resources before storage (inject sidecar, set defaults).

### 107. What is a validating webhook?

Validates resources after mutation but before storage.

### 108. What is the difference between RunAsUser and runAsGroup?

Pod security context settings for user/group IDs:
```yaml
spec:
  securityContext:
    runAsUser: 1001
    runAsGroup: 3001
    fsGroup: 2001
```

### 109. What is PodSecurityPolicy (PSP)?

Deprecated (removed in v1.25). Replaced by Pod Security Standards and OPA/Gatekeeper.

### 110. What is a limitRange?

Sets default resource requests/limits per namespace:
```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-limits
  namespace: dev
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "200m"
      memory: "256Mi"
    type: Container
```

### 111. How do you expose a pod without a Service?

kubectl port-forward: `kubectl port-forward pod/myapp 8080:80`

### 112. What is kubelet?

Agent on each node that ensures containers are running as defined by pod specs.

### 113. What is kube-proxy?

Network agent that maintains iptables/IPVS rules for Service traffic.

### 114. How do you delete all pods in a namespace?

```bash
kubectl delete pods --all -n dev
```

### 115. How do you get logs from all pods of a deployment?

```bash
kubectl logs -l app=myapp --tail=10 -f
```

### 116. What is a rolling update strategy?

Gradually replaces pods with new version. Configured via maxSurge and maxUnavailable.

### 117. How do you run a pod on a specific node?

```yaml
spec:
  nodeName: worker-2
```

Or use nodeSelector/affinity.

### 118. What is kubectl annotate?

Adds annotations (metadata) to resources: `kubectl annotate pod myapp description="my app"`

### 119. What is kubectl label?

Adds/updates labels: `kubectl label pod myapp env=prod`

### 120. How do you check API server health?

```bash
kubectl get componentstatuses
curl -k https://localhost:6443/healthz
```

### 121. How do you check which node a pod is on?

```bash
kubectl get pod myapp -o wide
kubectl describe pod myapp | grep Node
```

### 122. What is the default namespace in kubectl?

The `default` namespace.

### 123. How do you permanently save a namespace context?

```bash
kubectl config set-context --current --namespace=prod
```

### 124. How do you merge kubeconfig files?

```bash
export KUBECONFIG=$HOME/.kube/config:$HOME/.kube/config-eks
kubectl config view --flatten > merged.yaml
```

### 125. What is kustomize?

Native K8s configuration management without templates. Uses kustomization.yaml for overlays.

### 126. What is the difference between kustomize and Helm?

Kustomize = native YAML patching (no templating). Helm = package manager with Go templates.

### 127. How do you use a private image registry in K8s?

```yaml
spec:
  imagePullSecrets:
  - name: regcred
---
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64 docker config>
```

### 128. What is a headless service?

Service with clusterIP: None. Used for StatefulSets, direct pod-to-pod DNS.

### 129. What is clusterIP?

Virtual IP for a Service, only reachable within the cluster.

### 130. What is the default service type?

ClusterIP.

### 131. How do you debug DNS issues in K8s?

```bash
kubectl run dns-test --image=busybox --rm -it -- nslookup kubernetes.default
kubectl describe configmap coredns -n kube-system
```

### 132. What is the purpose of readinessProbe?

Determines if a pod is ready to receive traffic. If fails, pod is removed from Service endpoints.

### 133. What is the purpose of livenessProbe?

Determines if a pod is healthy. If fails, pod is restarted.

### 134. What is startupProbe?

Used for slow-starting containers. Disables liveness/readiness probes until it succeeds.

### 135. Can you have multiple containers in a pod?

Yes. They share network namespace, storage, and lifecycle.

### 136. How do containers in a pod communicate?

Via localhost (shared network namespace), shared volumes, or IPC.

### 137. What is a downward API?

Exposes pod metadata (name, namespace, labels) to containers via env vars or files.

### 138. What is a projected volume?

Combines multiple volume sources (Secret, ConfigMap, downward API) into one mount.

### 139. What is a persistentVolumeReclaimPolicy?

What happens to PV when PVC is deleted: Retain, Delete, or Recycle (deprecated).

### 140. What is a storage class?

Defines storage provisioner and parameters for dynamic PV provisioning.

### 141. What is the difference between a Deployment and a StatefulSet?

Deployment = stateless, random names, shared storage. StatefulSet = ordered, sticky identities, per-pod storage.

### 142. What is a DaemonSet good for?

Log collection, monitoring agents, networking daemons, security agents.

### 143. What is a Job?

Runs one or more pods to completion. For batch processing, migrations, backups.

### 144. What is a CronJob?

Runs Jobs on a schedule (cron format).

### 145. What is HPA good for?

Automatically scaling replicas based on CPU, memory, or custom metrics.

### 146. What is VPA good for?

Automatically adjusting CPU/memory requests to match actual usage.

### 147. Can you use HPA and VPA together?

For CPU/memory? No — use one or the other. VPA for CPU/memory + HPA for custom metrics is fine.

### 148. What happens when a pod exceeds memory limit?

OOMKilled by kubelet. Pod restarts if restartPolicy is Always/OnFailure.

### 149. What happens when a pod exceeds CPU limit?

CPU throttled — no kill, just slower.

### 150. What is Quality of Service (QoS)?

K8s classifies pods: Guaranteed, Burstable, BestEffort. Determines eviction priority.

### 151. How do you set resource requests and limits?

```yaml
resources:
  requests:
    cpu: "250m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### 152. What is etcd?

Distributed key-value store storing all cluster state. Must be backed up.

### 153. How do you backup etcd?

```bash
ETCDCTL_API=3 etcdctl snapshot save /backup/snapshot.db
```

### 154. What is the role of the scheduler?

Assigns pods to nodes based on resources, constraints, affinity, data locality.

### 155. What is the role of the controller manager?

Runs controllers that watch API server and reconcile desired state.

### 156. What is a controller?

Control loop that watches shared state and makes changes toward desired state.

### 157. What is the control plane?

The brain of the cluster (API server, scheduler, controller manager, etcd). User workloads don't run here.

### 158. What are worker nodes?

Machines that run user containers via kubelet, kube-proxy, container runtime.

### 159. What is a node?

A worker machine in Kubernetes (physical or virtual).

### 160. How do you add a node to a cluster?

```bash
kubeadm token create --print-join-command
# Run output on new node
```

---

## 161-210. Additional Questions

### 161. What is Kubernetes Ingress?

API object that manages external access to Services, typically HTTP/HTTPS.

### 162. What is an Ingress Controller?

The actual implementation that processes Ingress resources (NGINX, Traefik, HAProxy, ALB).

### 163. How does TLS termination work in Ingress?

Ingress uses a Secret containing TLS certificate and key. NGINX/Traefik terminates TLS at ingress.

### 164. What is a Kubernetes network policy?

A firewall rule for pods — what traffic is allowed in/out.

### 165. How do you allow all traffic to a pod?

Don't create NetworkPolicy (default allow). Or create policy with empty podSelector.

### 166. How do you deny all traffic to a pod?

```yaml
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
```

### 167. What is RBAC and why use it?

Role-Based Access Control for fine-grained permissions. Follow least-privilege.

### 168. What is a ClusterRole?

Like a Role, but cluster-scoped (nodes, PVs, namespaces).

### 169. What is a ClusterRoleBinding?

Binds ClusterRole to users/service accounts across all namespaces.

### 170. What is a RoleBinding?

Binds Role to users/service accounts in a specific namespace.

### 171. What is a ServiceAccount?

Identity for pods. Each pod has a service account token mounted.

### 172. Can a pod authenticate to the API server?

Yes, via its ServiceAccount token mounted at /var/run/secrets/kubernetes.io/serviceaccount/

### 173. What is Helm?

Kubernetes package manager. Charts = packages, Releases = deployed instances.

### 174. What is Tiller in Helm v2?

Helm v2 had server-side Tiller. Helm v3 removed it for better security.

### 175. What are Helm hooks?

Actions triggered at specific points (install, upgrade, delete): pre-install, post-install, etc.

### 176. What is a Helm values file?

YAML file with configuration values used in Go templates.

### 177. What is a Helm chart repository?

HTTP server hosting index.yaml + packaged charts (.tgz).

### 178. What is Helm Rollback?

Revert a release to a previous revision: `helm rollback my-release 1`

### 179. How do you structure a Helm chart?

Chart.yaml, values.yaml, templates/, charts/, templates/NOTES.txt, templates/_helpers.tpl

### 180. What is the Helm built-in object Release?

Exposes release metadata: Release.Name, Release.Namespace, Release.IsInstall, Release.IsUpgrade.

### 181. What are Helm dependencies?

Charts that depend on other charts. Defined in Chart.yaml dependencies.

### 182. How do you update Helm dependencies?

```bash
helm dependency update
```

### 183. What is kubectl drain?

Safely evict all pods from a node for maintenance.

### 184. How do you add a node to a cluster?

Join with token: `kubeadm join <master>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>`

### 185. What is cluster autoscaler?

Adjusts the number of nodes based on pending pods.

### 186. What is Karpenter?

AWS open-source node autoscaler — provisions optimal nodes instantly.

### 187. What is a node pool?

Group of nodes with same configuration (instance type, labels, taints).

### 188. How do you upgrade a K8s cluster?

One minor version at a time. Control plane first, then nodes.

### 189. What is a pod security policy (deprecated)?

Deprecated. Replaced by Pod Security Standards.

### 190. What is Pod Security Standards admission?

Built-in admission controller enforcing Privileged, Baseline, or Restricted levels.

### 191. What is OPA Gatekeeper?

Policy engine for K8s using OPA (Open Policy Agent) with Rego language.

### 192. What is Kyverno?

Kubernetes-native policy engine (no Rego needed, uses YAML).

### 193. How do you encrypt secrets in etcd?

Enable EncryptionConfiguration with aescbc or KMS provider.

### 194. What is Velero?

Backup and restore tool for K8s resources and persistent volumes.

### 195. How do you backup persistent volumes with Velero?

Use volume snapshots (EBS snapshots, PD snapshots, Azure Disk snapshots).

### 196. How do you restore a namespace with a different name?

```bash
velero restore create --from-backup daily --namespace-mappings prod:staging
```

### 197. What is Prometheus?

CNCF monitoring system — scrapes metrics, stores time-series, supports alerts.

### 198. What is Grafana?

Visualization dashboard for Prometheus and other data sources.

### 199. What is kube-state-metrics?

Exposes K8s object metrics (deployment replicas, pod status, etc.).

### 200. What is node_exporter?

Prometheus exporter for hardware and OS metrics.

### 201. What is the EFK stack?

Elasticsearch (storage) + Fluentd (log collector) + Kibana (visualization).

### 202. What is Loki?

Log aggregation system by Grafana — lightweight, cheaper than Elasticsearch.

### 203. What is Promtail?

Agent that ships logs to Loki (similar to Fluentd).

### 204. How do you collect logs in Kubernetes?

DaemonSet (Fluentd/Promtail) reads /var/log/containers/*.log on each node.

### 205. What is a sidecar logging pattern?

Logging agent runs as sidecar container in the same pod as the app.

### 206. What is Cilium?

eBPF-based CNI plugin with advanced networking, security, and observability.

### 207. What is Hubble?

Network observability platform for Cilium — provides service map, flow logs.

### 208. What is eBPF?

In-kernel virtual machine allowing safe execution of programs in the Linux kernel.

### 209. What is Calico?

Network plugin using BGP for routing, supports NetworkPolicy, encryption.

### 210. What is Flannel?

Simple overlay network plugin using VXLAN — no NetworkPolicy support.

### 211. What is Istio?

Service mesh with Envoy sidecars. Traffic management, mTLS, observability.

### 212. What is Linkerd?

Lightweight service mesh with Rust-based proxy. mTLS, metrics, basic traffic management.

### 213. What is a service mesh?

Dedicated infrastructure layer for service-to-service communication (security, observability, traffic management).

### 214. What is mTLS?

Mutual TLS — both sides authenticate each other. Used in service mesh for pod-to-pod encryption.

### 215. What is a VirtualService (Istio)?

Defines traffic routing rules (weighted routing, retries, timeouts).

### 216. What is a DestinationRule (Istio)?

Defines policies for traffic after routing (load balancing, circuit breaking).

### 217. What is a CRD?

Custom Resource Definition — extends K8s API with custom resource types.

### 218. What is an operator?

A controller that watches CRDs and automates application management.

### 219. What is the operator pattern?

CRD + controller = operator. Encodes domain knowledge for running complex stateful apps.

### 220. What is cert-manager?

Operator that automates TLS certificate management (Let's Encrypt, HashiCorp Vault).

### 221. What is Prometheus Operator?

Manages Prometheus instances, ServiceMonitors, Alertmanager via CRDs.

### 222. What is Strimzi?

Operator for running Apache Kafka on Kubernetes.

### 223. What is a custom controller?

Program that watches resources via API server and reconciles desired state.

### 224. How do you write a custom controller?

Using client-go library. Watch events on resources, enqueue work, reconcile.

### 225. What is the reconciler pattern?

Controller's main loop: observe current state, compute desired state, apply changes.

### 226. What is client-go?

Go library for interacting with K8s API server (informer, lister, work queues).

### 227. What is the shared informer pattern?

Efficient way to watch resources — uses list-watch, local cache, reduces API server load.

### 228. What is a work queue?

Rate-limited, retry-friendly queue for processing items in controllers.

### 229. How do you manage operator dependencies?

Using operator-lifecycle-manager (OLM) or Helm charts.

### 230. What is OLM?

Operator Lifecycle Manager — manages operators' installation, upgrade, RBAC.

### 231. What is Kustomize?

Native K8s YAML patching — overlays, patches, transformers.

### 232. What is kustomization.yaml?

```yaml
resources:
- deployment.yaml
- service.yaml
patches:
- path: patch-replicas.yaml
```

### 233. What is the difference between Kustomize and Helm?

Kustomize = native, no templating. Helm = package manager with Go templates.

### 234. What is server-side apply?

kubectl apply uses server-side diff and merge, managed via managedFields.

### 235. What is OpenAPI schema validation?

K8s validates resources against OpenAPI schemas defined in CRDs or built-in types.

### 236. How do you check API versions?

```bash
kubectl api-versions
kubectl api-resources
```

### 237. What is a webhook?

HTTP callback that mutates or validates resources before persistence.

### 238. What is AdmissionReview?

Request/response format for admission webhooks. Contains the object being reviewed.

### 239. What is dynamic admission control?

Webhooks that intercept API requests to mutate (mutating) or validate (validating).

### 240. What is initializer?

Deprecated admission mechanism. Replaced by mutating webhooks.

### 241. What is OwnerReference?

Links child resources to parent (e.g., pods owned by ReplicaSet). Cascading deletion.

### 242. What is garbage collection?

K8s automatically deletes resources owned by deleted parent (cascading deletion).

### 243. What is a finalizer?

Prevents deletion until certain condition is met. Controller removes finalizer when done.

### 244. How do you use finalizers?

```yaml
metadata:
  finalizers:
  - my-finalizer.example.com
```

### 245. What is a preStop hook?

Command executed before container terminates (graceful shutdown).

### 246. What is a postStart hook?

Command executed after container starts (not guaranteed before ENTRYPOINT).

### 247. What is a lifecycle hook?

postStart and preStop hooks for running commands at specific lifecycle events.

### 248. How do you do graceful shutdown in K8s?

preStop hook + SIGTERM handling + terminationGracePeriodSeconds.

```yaml
spec:
  containers:
  - name: app
    lifecycle:
      preStop:
        exec:
          command: ["/bin/sh", "-c", "sleep 10"]
  terminationGracePeriodSeconds: 60
```

### 249. What is a terminationGracePeriodSeconds?

Time K8s waits between SIGTERM and SIGKILL during pod shutdown.

### 250. What is the default termination grace period?

30 seconds.

### 251. How do you handle SIGTERM in Python?

```python
import signal, sys
def handler(signum, frame):
    print("Shutting down gracefully...")
    sys.exit(0)
signal.signal(signal.SIGTERM, handler)
```

### 252. What is kube-dns?

Deprecated cluster DNS. Replaced by CoreDNS.

### 253. What is CoreDNS?

Default cluster DNS (since K8s 1.13). Extensible via plugins.

### 254. How do you configure CoreDNS?

Edit ConfigMap in kube-system/coredns.

### 255. What is NodeLocal DNSCache?

DaemonSet that caches DNS queries on each node, reducing load on CoreDNS.

### 256. What is the default pod DNS policy?

ClusterFirst — query cluster DNS first, fallback to upstream.

### 257. What is podAntiAffinity?

Spread pods across topology (nodes, zones) for high availability.

### 258. What is podAffinity?

Co-locate pods on same topology for performance.

### 259. What is topologyKey?

Node label used for affinity/anti-affinity (kubernetes.io/hostname, topology.kubernetes.io/zone).

### 260. How do you ensure pods are spread across nodes?

```yaml
affinity:
  podAntiAffinity:
    requiredDuringScheduling:
    - labelSelector: { matchLabels: { app: myapp } }
      topologyKey: kubernetes.io/hostname
```

### 261. What is a priority class?

Defines scheduling priority. Higher value = more important pod.

### 262. What happens when a high-priority pod can't be scheduled?

Scheduler preempts (evicts) lower-priority pods.

### 263. How do you disable preemption?

```yaml
kind: PriorityClass
spec:
  preemptionPolicy: Never
```

### 264. What is the default priority for pods?

0 (if no priorityClassName set).

### 265. What is system-cluster-critical?

Built-in priority class for critical system pods.

### 266. What is a container runtime?

Software that runs containers (containerd, CRI-O, Docker).

### 267. What is CRI?

Container Runtime Interface — standard for K8s to talk to runtimes.

### 268. What is CRI-O?

Lightweight CRI-compatible runtime optimized for K8s.

### 269. What is containerd?

Industry-standard container runtime (used by Docker, K8s).

### 270. What is a pod sandbox?

CRI abstraction for pod-level isolation (Linux namespaces, cgroups).

### 271. What is runc?

Low-level OCI runtime that actually creates and runs containers.

### 272. What is gVisor?

Sandbox runtime for extra security (user-space kernel intercepts syscalls).

### 273. What is Kata Containers?

Lightweight VM runtime that combines VM security with container speed.

### 274. What is the OCI specification?

Open Container Initiative standards for image format and runtime.

### 275. What is containerd vs Docker?

Docker = full platform (build, ship, run). containerd = just runtime (used by K8s via CRI).

### 276. How do you configure container runtime?

Kubelet flag: --container-runtime=remote --container-runtime-endpoint=unix:///run/containerd/containerd.sock

### 277. What is kubelet garbage collection?

Removes unused images and dead containers to free disk space.

### 278. What is eviction?

Kubelet kills pods when node resources are low (memory, disk, PID).

### 279. What are eviction signals?

MemoryPressure, DiskPressure, PIDPressure — trigger pod eviction.

### 280. What is kube-reserved?

Resources reserved for K8s daemons (kubelet, kube-proxy, container runtime).

### 281. What is system-reserved?

Resources reserved for OS system daemons (sshd, udev, etc.).

### 282. What is allocatable?

Node resources available for pods = capacity - (kube-reserved + system-reserved + eviction threshold).

### 283. How do you protect system pods from eviction?

Use priority classes (system-cluster-critical) and resource reservations.

### 284. What is kubelet resource reservation config?

```yaml
kubeReserved:
  cpu: 500m
  memory: 512Mi
systemReserved:
  cpu: 300m
  memory: 256Mi
evictionHard:
  memory.available: "500Mi"
```

### 285. What is a static pod?

Pod managed directly by kubelet from a manifest file (not via API server). Used for control plane components.

### 286. Where are static pod manifests?

/etc/kubernetes/manifests/ on the node.

### 287. What is the difference between static pods and DaemonSets?

Static pods = kubelet-managed, no API server. DaemonSets = API server-managed, full lifecycle.

### 288. How do you add a static pod?

Place manifest file in /etc/kubernetes/manifests/. Kubelet picks it up automatically.

### 289. What is a mirror pod?

API server representation of a static pod. Read-only.

### 290. What is the Kubernetes API?

RESTful API that exposes all cluster operations via HTTP/HTTPS.

### 291. What is API aggregation?

Extending K8s API with additional API servers (metrics-server, service-catalog).

### 292. What is an APIService?

Registers an aggregated API server with the main API server.

### 293. What is an admission controller?

Plugin that intercepts API requests after authentication/authorization.

### 294. What are the default admission controllers?

NamespaceLifecycle, LimitRanger, ServiceAccount, NodeRestriction, etc.

### 295. How do you enable admission controllers?

API server flag: --enable-admission-plugins=PodSecurity,NodeRestriction

### 296. What is a resource quota?

Limits total resources in a namespace (pods, CPU, memory, PVCs).

### 297. How does quota interact with requests/limits?

Quota sums requests across pods. Each pod counts against the namespace quota.

### 298. What is the Kubernetes control plane HA?

Multiple API server instances behind load balancer, etcd cluster, leader-elected controllers.

### 299. How many nodes for HA control plane?

At least 3 nodes for etcd quorum (odd number).

### 300. What is a multi-cluster setup?

Multiple K8s clusters managed together (federation, service mesh, or just separate clusters for isolation).
